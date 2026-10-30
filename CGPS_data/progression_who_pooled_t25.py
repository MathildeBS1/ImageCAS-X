"""Who, pooled engine, T2.5 (who-progression B2 vs G03): does segment turning add to SCORE2 in predicting who progresses?

    python progression_who_pooled_t25.py [--src TREE_FOLDER] [--person score2|factors] [--folds 10] [--repeats 20]
                                         [--boot 200] [--nodes 100]
    python progression_who_pooled_t25.py --synthetic      # fitter and pooling self-test, no data needed

The fixed version of progression_who_pooled.py (issues: reports/Pooled who progression code issues.md); mean T2.5
is the only geometric feature.

Rows: every person with a Medis tree file, times the 9 trunk segments, graded from the sheets: BL none..severe
(BL ct_cag_<seg>_eval == 0 counts as unevaluable) and FU none..occlusion. Segment outcome: higher grade at FU.
Person outcome: any graded trunk segment progressed, from the sheets, whether or not the tree split found the segment.
Segment length and mean T2.5 come from the trunk split (progression_turning.build); a graded segment the split did
not find is kept with not_split = 1, and its length and T2.5 set to the training mean of its segment type.

Engine (experiments/who-progression/pooled_score2/pooling.md): a segment-level cloglog GLMM with a person random
intercept b ~ N(0, s^2), Gauss-Hermite quadrature (--nodes, checked against twice as many on every run), cold start
on every fit, then pooled to person risk P_i = 1 - int exp(-e^b sum_j exp(eta_ij)) phi(b; 0, s^2) db.
  B2  = log follow-up + log SCORE2 (z) + SCORE2-OP used + dominance (right vs not) + segment position (ref pLAD)
        + log length + not split + BL grade (levels with < 5 events or non-events in the training fold merged);
        --person factors: the refitted factors (age, male, smoking, SBP, total cholesterol, HDL) instead of SCORE2.
  G03 = B2 + mean T2.5 (z within segment type).
Everything learned (z constants, grade merging, coefficients, s) is fitted on the training persons.

Point estimates: mean over --repeats CV repeats (10 person folds stratified on the person outcome; fold files reused).
Their spread is split variability, not uncertainty. 95% CIs: paired person bootstrap (--boot replicates, each copy of a
person keeps that person's repeat-0 fold, the full CV rerun per replicate). Per segment: the same fits give each
segment's marginal risk; AUC within a segment type compares people (exploratory). Confusion matrices: repeat 0,
Youden cut-off from inner 5-fold CV on the training fold. Test: LR G03 vs B2 (1 df), all rows and complete cases.
Aggregates only (counts 1-4 hidden); writes progression_who_pooled_t25.md and progression_who_pooled_t25_*.png.
Fold files (person IDs) go to <out>/folds/: they stay on the server.
"""
import argparse
import hashlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import check_grad, minimize
from scipy.special import logsumexp
from scipy.stats import chi2, rankdata

import cgps_stats
import hoe10y_qc as hq
import progression_turning as pt
import split_trunks
from cgps_stats import MIN_CELL, OUT_DIR, count, count_of, num, suppress, yes

PREFIX = "progression_who_pooled_t25"
TRUNK_SEGS = tuple(pt.SEG_ORDER)
VESSEL_COL = {"LAD": "lad", "LCx": "cx", "RCA": "rca"}
BL_GRADED = ("none", "minimal", "mild", "moderate", "severe")  # occluded at BL cannot progress
RANK = {g: i for i, g in enumerate(hq.GRADES)}
GRADES4 = ("none", "minimal", "mild", ">=moderate")  # BL grade as a covariate
SCORE2_COLS = {"age": "scan_age", "male": "male", "smoking": "hist_smoking_current", "sbp": "clin_bp_sys_mean",
               "tc": "tot_cholesterol", "hdl": "hdl"}
CONTINUOUS = ("age", "sbp", "tc", "hdl")
DOMINANCE = (("codominant", ("co", "ko", "ba")), ("right", ("r", "h")), ("left", ("l", "v")))  # English / Danish
REF_SEG = "plad"
FEATURE = "mean_T2.5"
MODELS = ("B2", "G03")
GEOMETRY = {"B2": False, "G03": True}
COLOR = {"B2": pt.MODEL_COLOR["base"], "G03": pt.MODEL_COLOR["mean T2.5"]}
LOG_SIGMA_BOUNDS = (-8.0, 3.0)
SIGMA_FLOOR = 0.01  # below this the fit is redone from log s = 0.5 (s = 0 is a stationary point on the log scale)
RISK_NODES = 200
MAX_NODES = 300  # numpy's hermgauss overflows above about 300
NODE_TOL = {"beta": 1e-3, "sigma": 1e-3, "ll": 0.05}  # fixed before running
RISK_TOL = 1e-6
SEPARATION = 10.0  # |beta| or SE above this flags (quasi-)separation


# ---------------------------------------------------------------- data
def tree_ids(src):
    """Person IDs of the Medis tree files, including trees the trunk split fails on."""
    return sorted({i for i in (hq.id_from_name(f.name) for f in Path(src).rglob("*.vtk")) if i})


def dominance_label(s):
    t = s.astype(str).str.strip().str.lower().where(s.notna())
    out = pd.Series("missing", index=s.index)
    for lab, prefixes in DOMINANCE[::-1]:  # codominant last, so "co..." wins over nothing else
        out[t.str.startswith(prefixes).fillna(False)] = lab
    out[t.notna() & (out == "missing")] = "other"
    return out


def sheets():
    sh = hq.load_sheets(hq.ROOT)
    return [sh[v].assign(id=sh[v]["study_id"].map(hq.norm_id)).drop_duplicates("id").set_index("id")
            for v in ("BL", "FU")]


def person_table(bl, fu):
    P = pd.DataFrame({k: num(bl[c]) for k, c in SCORE2_COLS.items()})
    P["male"], P["smoking"] = yes(bl["male"]), yes(bl["hist_smoking_current"])
    s2, op = num(bl["score2"]), num(bl["score2_op"]) if "score2_op" in bl else pd.Series(np.nan, index=bl.index)
    P["score2"], P["op_used"] = s2.fillna(op), (s2.isna() & op.notna()).astype(float)
    P["dominance"] = dominance_label(bl["ct_cag_dominance"])
    P["right"] = (P["dominance"] == "right").astype(float).where(P["dominance"] != "missing")
    P["years"] = (pd.to_datetime(fu["scandate"], errors="coerce").reindex(bl.index)
                  - pd.to_datetime(bl["scandate"], errors="coerce")).dt.days / 365.25
    return P


def segment_grades(bl, fu, ids, use_eval):
    """Long table id x trunk segment: BL / FU grade (eval flag applied at BL when use_eval), FU vessel flag."""
    rows = []
    for seg in TRUNK_SEGS:
        b = bl.reindex(ids)[f"ct_cag_{seg}_stenosis"].map(hq.grade_of)
        e = num(bl.reindex(ids)[f"ct_cag_{seg}_eval"]) if f"ct_cag_{seg}_eval" in bl else pd.Series(np.nan, index=ids)
        f = fu.reindex(ids)[f"ct_cag_{seg}_stenosis"].map(hq.grade_of)
        vcol = f"ct_cag_{VESSEL_COL[pt.VESSEL[seg]]}_uneval"
        v = num(fu.reindex(ids)[vcol]) if vcol in fu else pd.Series(np.nan, index=ids)
        rows.append(pd.DataFrame({"id": ids, "segment": seg, "bl_raw": b.to_numpy(), "eval": e.to_numpy(),
                                  "fu": f.to_numpy(), "fu_vessel_uneval": v.to_numpy()}))
    g = pd.concat(rows, ignore_index=True)
    g["bl"] = g["bl_raw"].where(~(use_eval & (g["eval"] == 0)), "unevaluable")
    g["graded"] = g["bl"].isin(BL_GRADED) & g["fu"].isin(hq.GRADES)
    g["y"] = (g["fu"].map(RANK) > g["bl"].map(RANK)).astype(float)
    return g


def grade_class(s):
    return np.where(s == "none", "none", np.where(s.isin(hq.GRADES), "plaque", "unevaluable / missing"))


def sort_by_person(d):
    return d.sort_values(["id", "segment"], kind="stable").reset_index(drop=True)


def starts_of(ids):
    ids = np.asarray(ids)
    return np.r_[0, np.flatnonzero(ids[1:] != ids[:-1]) + 1]


def merged_grades(d, train):
    """BL grade (4 levels), merging from the top any level with < MIN_CELL events or non-events in the training rows."""
    g = d["bl"].map(pt.GRADE).copy()
    y = d["y"]
    for hi, lo in zip(GRADES4[:0:-1], GRADES4[-2::-1]):
        m = train & (g == hi)
        if m.any() and min(y[m].sum(), m.sum() - y[m].sum()) < MIN_CELL:
            g[g == hi] = lo
    return g


def design(d, train, geo, segs, person):
    """Fixed-effect design (n, p) and column names; every constant learned on the training rows."""
    people = d[train].drop_duplicates("id")
    X, names = [np.ones(len(d)), np.log(d["years"].to_numpy())], ["intercept", "log follow-up"]
    if person == "factors":
        for c in CONTINUOUS:
            X.append(((d[c] - people[c].mean()) / people[c].std()).to_numpy())
            names.append(f"{c} (per SD)")
        X += [d["male"].to_numpy(float), d["smoking"].to_numpy(float)]
        names += ["male", "current smoking"]
    else:
        ls2 = np.log(people["score2"])
        X += [((np.log(d["score2"]) - ls2.mean()) / ls2.std()).to_numpy(), d["op_used"].to_numpy(float)]
        names += ["log SCORE2 (per SD)", "SCORE2-OP used"]
    X.append(d["right"].to_numpy(float))
    names.append("right dominance")
    X += pt.dummies(d, "segment", [s for s in segs if s != REF_SEG])
    names += [s for s in segs if s != REF_SEG]
    ll = np.log(d["length"].clip(lower=1.0))
    fill = ll[train].groupby(d.loc[train, "segment"]).mean()
    X += [ll.fillna(d["segment"].map(fill)).fillna(ll[train].mean()).to_numpy(), d["not_split"].to_numpy(float)]
    names += ["log length", "not split"]
    g = merged_grades(d, train)
    levels = [lv for lv in GRADES4[1:] if (g[train] == lv).any()]
    X += [(g == lv).to_numpy(float) for lv in levels]
    names += [f"BL {lv}" for lv in levels]
    if geo:
        X.append(pt.zscore(d, FEATURE, train))
        names.append("mean T2.5 (per SD, within type)")
    return np.column_stack(X), names


# ---------------------------------------------------------------- engine
def _nll(theta, X, y, starts, row_person, x, logw, l2):
    beta, ls = theta[:-1], theta[-1]
    u = np.sqrt(2.0) * np.exp(ls) * x
    raw = (X @ beta)[:, None] + u[None]
    inside = (raw > -30) & (raw < 30)  # the gradient is zero where the clip is active
    mu = np.exp(np.clip(raw, -30, 30))
    one = y[:, None] == 1
    lij = np.where(one, np.log(-np.expm1(-mu)), -mu)
    a = np.add.reduceat(lij, starts, axis=0) + logw[None]
    lse = logsumexp(a, axis=1)
    r = np.exp(a - lse[:, None])[row_person]
    g = np.where(one, mu * np.exp(-mu) / np.maximum(-np.expm1(-mu), 1e-300), -mu) * inside
    rg = r * g
    grad = np.r_[X.T @ rg.sum(1), (rg * u[None]).sum()]
    grad[:-1] -= 2 * l2 * beta
    return -(lse.sum() - l2 * beta @ beta), -grad


def _minimise(X, y, ids, nodes, theta0, l2):
    starts = starts_of(ids)
    row_person = np.repeat(np.arange(len(starts)), np.diff(np.r_[starts, len(ids)]))
    x, w = np.polynomial.hermite.hermgauss(nodes)
    args = (X, y, starts, row_person, x, np.log(w / np.sqrt(np.pi)), l2)
    r = minimize(_nll, theta0, args=args, jac=True, method="L-BFGS-B",
                 bounds=[(None, None)] * X.shape[1] + [LOG_SIGMA_BOUNDS], options={"maxiter": 5000, "maxfun": 10000})
    return {"theta": r.x, "ll": -float(r.fun), "ok": bool(r.success), "msg": str(r.message), "args": args}


def fit_glmm(X, y, ids, nodes, l2=1e-6, theta0=None):
    """Cold-started fit; columns constant on these rows are dropped (coefficient 0). Refit if s ends near 0."""
    keep = np.r_[True, np.ptp(X[:, 1:], axis=0) > 0]
    Xk = X[:, keep]
    if theta0 is None:
        theta0 = np.zeros(Xk.shape[1] + 1)
        theta0[0] = np.log(-np.log(1 - np.clip(y.mean(), 0.01, 0.99)))
    f = _minimise(Xk, y, ids, nodes, theta0, l2)
    if np.exp(f["theta"][-1]) < SIGMA_FLOOR:
        t1 = theta0.copy(); t1[-1] = 0.5
        f2 = _minimise(Xk, y, ids, nodes, t1, l2)
        f = f2 if f2["ll"] > f["ll"] else f
    beta = np.zeros(X.shape[1]); beta[keep] = f["theta"][:-1]
    return {**f, "beta": beta, "sigma": float(np.exp(f["theta"][-1])), "keep": keep}


def hessian_se(fit, h=1e-5):
    """SEs of the kept betas (NaN for dropped columns) and the minimum Hessian eigenvalue."""
    th, k = fit["theta"], len(fit["theta"])
    H = np.zeros((k, k))
    for i in range(k):
        e = np.zeros(k); e[i] = h
        H[:, i] = (_nll(th + e, *fit["args"])[1] - _nll(th - e, *fit["args"])[1]) / (2 * h)
    H = (H + H.T) / 2
    ev = np.linalg.eigvalsh(H)
    se_k = np.sqrt(np.diag(np.linalg.inv(H)))[:-1] if ev.min() > 0 else np.full(k - 1, np.nan)
    se = np.full(len(fit["keep"]), np.nan); se[fit["keep"]] = se_k
    return se, float(ev.min())


def _nodes(sigma, nodes):
    x, w = np.polynomial.hermite.hermgauss(nodes)
    return np.sqrt(2.0) * sigma * x, w / np.sqrt(np.pi)


def segment_risk(X, beta, sigma, nodes=RISK_NODES):
    """Marginal P(segment progresses), integrated over b."""
    u, w = _nodes(sigma, nodes)
    return 1 - (w[None] * np.exp(-np.exp(u)[None] * np.exp(np.clip(X @ beta, -30, 30))[:, None])).sum(1)


def person_risk(X, beta, sigma, ids, nodes=RISK_NODES):
    """P(any graded trunk segment progresses), integrated over b (pooling.md); persons in row order."""
    u, w = _nodes(sigma, nodes)
    S = np.add.reduceat(np.exp(np.clip(X @ beta, -30, 30)), starts_of(ids))
    return 1 - (w[None] * np.exp(-np.exp(u)[None] * S[:, None])).sum(1)


# ---------------------------------------------------------------- metrics
def auc(y, p):
    """Mann-Whitney AUC, ties counted 1/2."""
    y = np.asarray(y, bool)
    n1, n0 = y.sum(), (~y).sum()
    if not n1 or not n0:
        return np.nan
    return (rankdata(p)[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


def roc(y, p):
    """(fpr, tpr, thresholds) over the unique predicted values, calling p >= threshold positive."""
    y = np.asarray(y, bool)
    thr = np.unique(p)[::-1]
    tpr = np.array([(p[y] >= t).mean() for t in thr])
    fpr = np.array([(p[~y] >= t).mean() for t in thr])
    return np.r_[0, fpr], np.r_[0, tpr], np.r_[np.inf, thr]


def youden(y, p):
    fpr, tpr, thr = roc(y, p)
    return thr[np.argmax(tpr - fpr)]


def confusion(y, p, thr):
    c, y = p >= thr, np.asarray(y, bool)
    return [int(v) for v in ((c & y).sum(), (~c & y).sum(), (c & ~y).sum(), (~c & ~y).sum())]


def cal_intercept(y, lp):
    a = 0.0
    for _ in range(50):
        p = 1 / (1 + np.exp(-(a + lp)))
        step = (y - p).sum() / max((p * (1 - p)).sum(), 1e-12)
        a += step
        if abs(step) < 1e-10:
            break
    return a


def metrics(y, p):
    p = np.clip(p, 1e-9, 1 - 1e-9)
    lp = np.log(p / (1 - p))
    brier = np.mean((p - y) ** 2)
    return {"log loss": -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)), "C": auc(y, p), "Brier": brier,
            "scaled Brier": 1 - brier / max(y.mean() * (1 - y.mean()), 1e-12),
            "cal. slope": pt.fit(np.column_stack([np.ones(len(y)), lp]), y)[0][1], "cal. intercept": cal_intercept(y, lp)}


def person_folds(Y, k, rng):
    out = {}
    for _, ids in Y.groupby(Y):
        out.update(zip(rng.permutation(ids.index), np.arange(len(ids)) % k))
    return out


def load_folds(Y, k, r, folder):
    """{id: fold} of repeat r, read from folder/folds_r{r}.csv if it matches the cohort, else made and written."""
    path = folder / f"folds_r{r}.csv"
    if path.exists():
        f = pd.read_csv(path, dtype={"id": str}).set_index("id")["fold"]
        if set(f.index) == set(Y.index) and f.max() == k - 1:
            return f.to_dict(), path
    fold_of = person_folds(Y, k, np.random.default_rng(r))
    pd.Series(fold_of, name="fold").rename_axis("id").to_csv(path)
    return fold_of, path


# ---------------------------------------------------------------- cross-validation
def cv(d, fold, folds, segs, person, nodes, seg_rows):
    """Out-of-fold person risks, segment risks and fitted s per model, for one fold assignment (per row)."""
    y, ids = d["y"].to_numpy(), d["id"].to_numpy()
    pfold = fold[starts_of(ids)]
    out = {m: {"P": np.zeros(len(pfold)), "seg": np.zeros(len(d)), "sigma": [], "fail": 0} for m in MODELS}
    for m in MODELS:
        for k in range(folds):
            tr, te = fold != k, fold == k
            X, _ = design(d, tr, GEOMETRY[m], segs, person)
            f = fit_glmm(X[tr], y[tr], ids[tr], nodes)
            out[m]["P"][pfold == k] = person_risk(X[te], f["beta"], f["sigma"], ids[te])
            out[m]["seg"][te] = segment_risk(X[te], f["beta"], f["sigma"])
            out[m]["sigma"].append(f["sigma"])
            out[m]["fail"] += not f["ok"]
    for m in MODELS:
        Y = np.maximum.reduceat(y, starts_of(ids))
        out[m]["metrics"] = metrics(Y, out[m]["P"])
        out[m]["seg_auc"] = {s: auc(y[S], out[m]["seg"][S]) for s, S in seg_rows(d).items()}
    return out


def inner_cutoffs(d, fold, folds, segs, person, nodes, seg_rows, rng):
    """Youden cut-offs per outer fold, from inner 5-fold CV predictions on the training persons only."""
    y, ids = d["y"].to_numpy(), d["id"].to_numpy()
    pfold = fold[starts_of(ids)]
    thr = {m: {"person": np.zeros(len(pfold)), "segment": np.zeros(len(d))} for m in MODELS}
    for k in range(folds):
        tr = fold != k
        dt = d[tr].reset_index(drop=True)
        Yt = dt.groupby("id", sort=False)["y"].max()
        inner_of = person_folds(Yt, 5, rng)
        inner = dt["id"].map(inner_of).to_numpy()
        res = cv(dt, inner, 5, segs, person, nodes, seg_rows)
        for m in MODELS:
            thr[m]["person"][pfold == k] = youden(Yt.to_numpy(), res[m]["P"])
            for s, S in seg_rows(d).items():
                St = S[tr]
                thr[m]["segment"][(fold == k) & S] = youden(dt["y"].to_numpy()[St], res[m]["seg"][St])
    return thr


def bootstrap(d, fold_of, folds, segs, person, nodes, seg_rows, B, rng):
    """Paired person bootstrap of the whole CV: each copy keeps its person's repeat-0 fold."""
    rows_of = d.groupby("id").indices
    people = np.array(list(rows_of))
    out = []
    for b in range(B):
        pick = rng.choice(people, len(people))
        parts = [d.iloc[rows_of[p]].assign(id=f"{p}#{j}", fold=fold_of[p]) for j, p in enumerate(pick)]
        db = sort_by_person(pd.concat(parts, ignore_index=True))
        res = cv(db, db["fold"].to_numpy(), folds, segs, person, nodes, seg_rows)
        out.append({m: {**res[m]["metrics"], **{f"seg {s}": v for s, v in res[m]["seg_auc"].items()}} for m in MODELS})
        print(f"bootstrap {b + 1}/{B}")
    return out


# ---------------------------------------------------------------- figures
def fig_auc(rows, out_dir):
    """AUC per level (person, then segments): mean over CV repeats; bars = person-bootstrap 95% CI."""
    plt = pt._plt()
    fig, ax = plt.subplots(figsize=(7.8, 0.55 * len(rows) + 1.5))
    pt._grid(ax, "x")
    yy = np.arange(len(rows))[::-1].astype(float)
    lo_all = []
    for y_, (lab, _, est, ci) in zip(yy, rows):
        for k, m in enumerate(MODELS):
            off = 0.18 if k == 0 else -0.18
            ax.barh(y_ + off, est[m] - 0.5, left=0.5, height=0.34, color=COLOR[m], label=m if y_ == yy[0] else None)
            if ci is not None:
                ax.plot(ci[m], [y_ + off] * 2, color=pt.INK2, lw=1)
                lo_all.append(ci[m][0])
            ax.text(max(est[m], ci[m][1] if ci is not None else est[m]) + 0.005, y_ + off, f"{est[m]:.2f}",
                    va="center", fontsize=7.5, color=pt.INK2)
    ax.axvline(0.5, color=pt.MUTED, lw=1, ls=":")
    ax.axhline(yy[0] - 0.5, color=pt.MUTED, lw=0.8)
    ax.set_yticks(yy, [f"{lab}  ({n})" for lab, n, _, _ in rows])
    for t, (lab, _, _, _) in zip(ax.get_yticklabels(), rows):
        t.set_color({"LAD": "#2a78d6", "LCx": "#1baf7a", "RCA": "#e34948"}.get(pt.VESSEL.get(lab), pt.INK))
        t.set_fontweight("bold")
    lo = min([0.4] + lo_all + [min(r[2][m] for r in rows for m in MODELS)]) - 0.03
    ax.set_xlim(max(lo, 0.0), 1.0)
    ax.set_xlabel("AUC on the test folds (0.5 = chance); bars: person-bootstrap 95% CI")
    ax.set_title("AUC per person and per segment: B2 vs G03 (mean T2.5)")
    ax.legend(fontsize=8, loc="lower right")
    fig.text(0.01, 0.01, "(progressed/rows). Segments: the pooled model's segment risk; AUC within a segment compares "
             "people (exploratory).", fontsize=7.5, color=pt.INK2)
    pt._save(fig, out_dir / f"{PREFIX}_auc.png", rect=(0, 0.03, 1, 1))


def fig_roc(panels, out_dir):
    plt = pt._plt()
    ncol = 4
    nrow = -(-len(panels) // ncol)
    fig, axes = plt.subplots(nrow, ncol, figsize=(3.3 * ncol, 3.2 * nrow), sharex=True, sharey=True, squeeze=False)
    grid = np.linspace(0, 1, 21)  # binned so no single person is a visible step
    for ax, (lab, n, yv, p, _) in zip(axes.ravel(), panels):
        pt._grid(ax, "both")
        ax.plot([0, 1], [0, 1], lw=1, ls=":", color=pt.MUTED)
        for m in MODELS:
            fpr, tpr, _ = roc(yv, p[m])
            ax.plot(grid, [tpr[fpr <= g].max() for g in grid], lw=2.2 if m == "B2" else 1.8, color=COLOR[m],
                    label=f"{m}  (AUC {auc(yv, p[m]):.2f})")
        ax.set_title(f"{lab}  ({n})", fontsize=10)
        ax.legend(fontsize=7.5, loc="lower right")
        ax.set(xlim=(0, 1), ylim=(0, 1.02))
    for ax in axes.ravel()[len(panels):]:
        ax.axis("off")
    for ax in axes[-1]:
        ax.set_xlabel("1 - specificity")
    for ax in axes[:, 0]:
        ax.set_ylabel("sensitivity")
    fig.suptitle("ROC on the test folds (repeat 0): person, then each segment", x=0.01, ha="left",
                 fontsize=12, fontweight="bold", color=pt.INK)
    pt._save(fig, out_dir / f"{PREFIX}_roc.png")


def shown_confusion(M):
    """Suppressed 2x2; every cell hidden if any is (a share or a margin would give it away)."""
    s = suppress(M)
    if any(not isinstance(v, (int, np.integer)) for v in s.ravel()):
        s = np.full((2, 2), cgps_stats.HIDDEN, dtype=object)
        s[(M > 0) & (M < MIN_CELL)] = cgps_stats.SMALL
    return s


def fig_confusion(panels, out_dir):
    plt = pt._plt()
    fig, axes = plt.subplots(len(panels), 2, figsize=(6.4, 2.3 * len(panels)), squeeze=False)
    cell_col = np.array([["#1baf7a", pt.MISSED], ["#e34948", "#1baf7a"]])
    for row, (lab, _, yv, p, thr) in zip(axes, panels):
        for ax, m in zip(row, MODELS):
            tp, fn, fp, tn = confusion(yv, p[m], thr[m])
            M = np.array([[tp, fn], [fp, tn]])
            shown = shown_confusion(M)
            ok = all(isinstance(v, (int, np.integer)) for v in shown.ravel())
            share = M / np.maximum(M.sum(axis=1, keepdims=True), 1)
            for (i, j), v in np.ndenumerate(shown):
                ax.add_patch(plt.Rectangle((j - 0.48, i - 0.48), 0.96, 0.96, color=cell_col[i, j],
                                           alpha=0.18 + 0.75 * share[i, j] if ok else 0.3))
                ax.text(j, i - 0.1, v, ha="center", va="center", fontsize=11, fontweight="bold", color=pt.INK)
                if ok:
                    ax.text(j, i + 0.25, f"{100 * share[i, j]:.0f}% of row", ha="center", va="center", fontsize=6.5,
                            color=pt.INK2)
            ax.set_xlim(-0.5, 1.5); ax.set_ylim(1.5, -0.5)
            ax.set_xticks([0, 1], ["called progress", "called stable"], fontsize=7)
            ax.set_yticks([0, 1], ["progressed", "stable"], fontsize=7)
            ax.tick_params(length=0)
            for sp in ax.spines.values():
                sp.set_visible(False)
            ax.set_title(f"{lab}: {m}  (AUC {auc(yv, p[m]):.2f})", color=COLOR[m], fontsize=9)
    fig.suptitle("Confusion matrices on the test folds (repeat 0)", x=0.01, ha="left", fontsize=12,
                 fontweight="bold", color=pt.INK)
    fig.text(0.01, 0.003, "Cut-off: Youden's J on inner-CV predictions of the training fold. Green = correct, orange =\n"
             "missed progression, red = false alarm; darker = larger share of its row.", fontsize=7.5, color=pt.INK2)
    pt._save(fig, out_dir / f"{PREFIX}_confusion.png", rect=(0, 0.015, 1, 0.99))


def fig_calibration(Y, oof, bins, out_dir):
    plt = pt._plt()
    fig, ax = plt.subplots(figsize=(5.6, 5.2))
    pt._grid(ax, "both")
    hidden = 0
    for m in MODELS:
        p = oof[m]
        q = pd.qcut(p, bins, labels=False, duplicates="drop")
        xs, ys = [], []
        for b in np.unique(q):
            yb = Y[q == b]
            if min(yb.sum(), len(yb) - yb.sum()) < MIN_CELL:
                hidden += 1
                continue
            xs.append(p[q == b].mean()); ys.append(yb.mean())
        ax.plot(xs, ys, "o-", color=COLOR[m], lw=1.8, label=m)
    lo = min(0.5, ax.get_xlim()[0], ax.get_ylim()[0])
    ax.plot([lo, 1], [lo, 1], ls=":", color=pt.MUTED, lw=1)
    ax.set(xlim=(lo, 1), ylim=(lo, 1), xlabel="mean predicted person risk (out of fold)", ylabel="observed share progressed")
    ax.set_title("Person calibration, pooled engine")
    ax.legend(fontsize=8, loc="upper left")
    fig.text(0.01, 0.01, f"Repeat 0, {bins} risk bins per model; {hidden} bin(s) not drawn (< {MIN_CELL} events or non-events).",
             fontsize=7.5, color=pt.INK2)
    pt._save(fig, out_dir / f"{PREFIX}_calibration.png", rect=(0, 0.03, 1, 1))


def fig_split_variability(reps, out_dir):
    plt = pt._plt()
    keys = ("log loss", "C", "scaled Brier", "cal. slope")
    fig, axes = plt.subplots(1, len(keys), figsize=(11, 3.2))
    for ax, key in zip(axes, keys):
        pt._grid(ax, "y")
        ax.boxplot([r["G03"]["metrics"][key] - r["B2"]["metrics"][key] for r in reps], widths=0.5,
                   medianprops={"color": COLOR["G03"]}, flierprops={"markersize": 3})
        ax.axhline(0, color=pt.MUTED, lw=1, ls=":")
        ax.set_xticks([])
        ax.set_title(f"Δ {key}", fontsize=10)
    fig.suptitle(f"G03 − B2 across {len(reps)} fold splits: split variability, not a confidence interval",
                 x=0.01, ha="left", fontsize=11, fontweight="bold", color=pt.INK)
    pt._save(fig, out_dir / f"{PREFIX}_split_variability.png")


# ---------------------------------------------------------------- self-test (no data)
def synthetic(seed=1):
    rng = np.random.default_rng(seed)
    m, J, sigma = 1500, 9, 1.2
    ids = np.repeat(np.arange(m), J)
    X = np.column_stack([np.ones(m * J), np.repeat(rng.normal(size=m), J), rng.normal(size=m * J),
                         np.tile(np.arange(J) == 0, m).astype(float)])
    beta = np.array([-2.2, 0.4, 0.25, 0.6])
    b = np.repeat(rng.normal(0, sigma, m), J)
    y = (rng.random(m * J) < 1 - np.exp(-np.exp(X @ beta + b))).astype(float)
    Y = np.add.reduceat(y, starts_of(ids)) > 0
    fit = fit_glmm(X, y, ids, 100)
    err = check_grad(lambda t: _nll(t, *fit["args"])[0], lambda t: _nll(t, *fit["args"])[1], fit["theta"] + 0.05)
    se, ev = hessian_se(fit)
    print(f"converged: {fit['ok']}; gradient check error {err:.2e}; min Hessian eigenvalue {ev:.3g}")
    for name, t, e, s in zip(["b0", "person z", "segment z", "segment 1"], beta, fit["beta"], se):
        print(f"  {name:10s} true {t:+.3f}  est {e:+.3f}  (SE {s:.3f})")
    print(f"  s          true {sigma:.3f}  est {fit['sigma']:.3f}")
    t0 = np.r_[fit["theta"][:-1] * 0, -7.0]; t0[0] = np.log(-np.log(1 - y.mean()))
    trap = fit_glmm(X, y, ids, 100, theta0=t0)
    print(f"start at log s = -7: s ends at {trap['sigma']:.3f} (ll {trap['ll']:.2f} vs cold start {fit['ll']:.2f})")
    P = person_risk(X, fit["beta"], fit["sigma"], ids)
    seg = segment_risk(X, fit["beta"], fit["sigma"])
    product = 1 - np.exp(np.add.reduceat(np.log1p(-seg), starts_of(ids)))
    b0 = 1 - np.exp(-np.add.reduceat(np.exp(X @ fit["beta"]), starts_of(ids)))
    print(f"observed person prevalence {Y.mean():.3f}; mean risk: integral {P.mean():.3f}, "
          f"product of segment risks {product.mean():.3f}, b = 0 {b0.mean():.3f}")
    print(f"integral {RISK_NODES} vs {MAX_NODES} nodes: max |diff| "
          f"{np.abs(P - person_risk(X, fit['beta'], fit['sigma'], ids, MAX_NODES)).max():.1e}")
    print(f"auc ties: {auc([1, 0], [0.5, 0.5]):.2f} (should be 0.50)")


# ---------------------------------------------------------------- main
def code_version():
    mods = [Path(__file__), Path(pt.__file__), Path(hq.__file__), Path(cgps_stats.__file__), Path(split_trunks.__file__),
            Path(sys.modules[pt.chord_resample.__module__].__file__)]
    h = hashlib.sha256()
    for p in mods:
        h.update(p.read_bytes())
    return h.hexdigest()[:12], ", ".join(p.name for p in mods)


def ci(v):
    v = np.asarray(v, float)
    v = v[~np.isnan(v)]
    return (np.percentile(v, 2.5), np.percentile(v, 97.5)) if len(v) else (np.nan, np.nan)


def table(header, rows):
    return ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] + ["| " + " | ".join(map(str, r)) + " |" for r in rows]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / f"{PREFIX}.md"))
    ap.add_argument("--folds", type=int, default=10)
    ap.add_argument("--repeats", type=int, default=20)
    ap.add_argument("--boot", type=int, default=200)
    ap.add_argument("--nodes", type=int, default=100, help=f"Gauss-Hermite nodes for fitting (< {MAX_NODES})")
    ap.add_argument("--bins", type=int, default=5)
    ap.add_argument("--person", choices=("score2", "factors"), default="score2")
    ap.add_argument("--no-bl-eval", action="store_true", help="do not apply BL ct_cag_<seg>_eval == 0 as unevaluable")
    ap.add_argument("--synthetic", action="store_true")
    args = ap.parse_args()
    if args.synthetic:
        synthetic()
        return
    out_dir = Path(args.out).parent
    (out_dir / "folds").mkdir(parents=True, exist_ok=True)
    code, mods = code_version()

    # ---- rows, outcome, covariates
    bl, fu = sheets()
    ids_tree = tree_ids(args.src)
    ids = [i for i in ids_tree if i in bl.index and i in fu.index]
    g_eval = segment_grades(bl, fu, ids, use_eval=True)
    g_raw = segment_grades(bl, fu, ids, use_eval=False)
    lost_eval = int(g_raw["graded"].sum() - g_eval["graded"].sum())
    eval_applied = not args.no_bl_eval and lost_eval <= 0.5 * g_raw["graded"].sum()  # guard against a reversed flag
    g = g_eval if eval_applied else g_raw
    d0, _, skipped = pt.build(args.src)
    feats = d0.drop_duplicates(["id", "segment"])[["id", "segment", "length", FEATURE]]
    P = person_table(bl, fu)
    d = g[g["graded"]].merge(feats, on=["id", "segment"], how="left").join(P, on="id")
    d["not_split"] = d["length"].isna().astype(float)
    need = (["score2"] if args.person == "score2" else list(SCORE2_COLS)) + ["right", "years"]
    cov_ok = d[need].notna().all(axis=1) & (d["years"] > 0) & ((d["score2"] > 0) | (args.person == "factors"))
    d = sort_by_person(d[cov_ok])
    if d["right"].nunique() < 2:
        raise SystemExit("right dominance is constant: check the ct_cag_dominance levels")
    y, rid = d["y"].to_numpy(), d["id"].to_numpy()
    Y = d.groupby("id", sort=False)["y"].max()
    Yv = Y.to_numpy()
    if min(Yv.sum(), len(Yv) - Yv.sum()) < MIN_CELL:
        raise SystemExit(f"fewer than {MIN_CELL} persons with or without progression: not fitted")
    segs = [REF_SEG] + [s for s in TRUNK_SEGS if s != REF_SEG and s in set(d["segment"])]
    scored = [s for s in segs if min(y[d["segment"] == s].sum(), (d["segment"] == s).sum() - y[d["segment"] == s].sum()) >= MIN_CELL]

    def seg_rows(dd):
        return {s: (dd["segment"] == s).to_numpy() for s in scored}

    # split-based outcome, as the old script defined it, for the same people
    y_split = d.loc[d["not_split"] == 0].groupby("id")["y"].max().reindex(Y.index).fillna(0)
    discord = int((y_split != Y).sum())

    # ---- full-data fits, LR tests, quadrature check
    full = np.ones(len(d), bool)
    fits, names, Xs, ses, eig, node_rows = {}, {}, {}, {}, {}, []
    node_fail = False
    check_nodes = min(2 * args.nodes, MAX_NODES)
    for m in MODELS:
        Xs[m], names[m] = design(d, full, GEOMETRY[m], segs, args.person)
        fits[m] = fit_glmm(Xs[m], y, rid, args.nodes)
        ses[m], eig[m] = hessian_se(fits[m])
        f2 = fit_glmm(Xs[m], y, rid, check_nodes)
        db = np.abs(f2["beta"] - fits[m]["beta"]).max()
        ds, dl = abs(f2["sigma"] - fits[m]["sigma"]), abs(f2["ll"] - fits[m]["ll"])
        dr = np.abs(person_risk(Xs[m], fits[m]["beta"], fits[m]["sigma"], rid)
                    - person_risk(Xs[m], fits[m]["beta"], fits[m]["sigma"], rid, MAX_NODES)).max()
        ok = db < NODE_TOL["beta"] and ds < NODE_TOL["sigma"] and dl < NODE_TOL["ll"] and dr < RISK_TOL
        node_fail |= not ok
        node_rows.append((m, f"{args.nodes} vs {check_nodes}", f"{db:.1e}", f"{ds:.1e}", f"{dl:.1e}", f"{dr:.1e}",
                          "pass" if ok else "**FAIL**"))
    cc = (d["not_split"] == 0).to_numpy()
    cc_fits = {}
    if cc.any():
        dc = d[cc].reset_index(drop=True)
        for m in MODELS:
            Xc, _ = design(dc, np.ones(len(dc), bool), GEOMETRY[m], segs, args.person)
            cc_fits[m] = fit_glmm(Xc, dc["y"].to_numpy(), dc["id"].to_numpy(), args.nodes)

    def lr_line(fs, label):
        if not fs or not all(f["ok"] for f in fs.values()):
            return f"- {label}: not reported, a fit did not converge."
        lr = 2 * (fs["G03"]["ll"] - fs["B2"]["ll"])
        return f"- {label}: LR = {lr:.2f}, df = 1, p = {chi2.sf(max(lr, 0.0), 1):.3g}."

    # ---- CV repeats, inner cut-offs, bootstrap
    reps, fold_paths = [], []
    for r in range(args.repeats):
        fold_of, path = load_folds(Y, args.folds, r, out_dir / "folds")
        fold_paths.append(path)
        reps.append(cv(d, d["id"].map(fold_of).to_numpy(), args.folds, segs, args.person, args.nodes, seg_rows))
        print(f"repeat {r + 1}/{args.repeats}: C B2 {reps[-1]['B2']['metrics']['C']:.3f}, "
              f"G03 {reps[-1]['G03']['metrics']['C']:.3f}")
    fold0, _ = load_folds(Y, args.folds, 0, out_dir / "folds")
    thr0 = inner_cutoffs(d, d["id"].map(fold0).to_numpy(), args.folds, segs, args.person, args.nodes, seg_rows,
                         np.random.default_rng(10_000))
    boot = bootstrap(d, fold0, args.folds, segs, args.person, args.nodes, seg_rows, args.boot,
                     np.random.default_rng(20_000)) if args.boot else []
    fold_hash = hashlib.sha256(b"".join(p.read_bytes() for p in fold_paths)).hexdigest()[:12]

    # ---- report: cohort
    def n_lab(yv):
        return f"{count_of(int(yv.sum()), len(yv))}/{count(len(yv))}"

    rep = [f"# Who, pooled engine: B2 vs G03 (mean T2.5) on plaque progression\n"]
    if node_fail:
        rep.append("**Quadrature check FAILED (see below): rerun with more --nodes before reading any number.**\n")
    rep += [f"Aggregates only; counts 1-4 shown as <{MIN_CELL}. Person block: {args.person}. Code sha256 {code} ({mods}). "
            f"Fold files sha256 {fold_hash} (seeds 0..{args.repeats - 1}). Exploratory: the Medis trees are people with "
            "plaque at baseline, so this is progression, not new plaque.\n",
            "## Cohort\n",
            f"- Medis tree files: {count(len(ids_tree))} people; in both sheets: {count(len(ids))}. Trees the split "
            f"failed on entirely: {count(skipped)} (their graded segments are kept, not split).",
            f"- Graded trunk segments: {count(int(g['graded'].sum()))}. In the model: {count(len(d))} rows from "
            f"{count(len(Y))} people (others lack {'SCORE2' if args.person == 'score2' else 'a SCORE2 factor'}, "
            "dominance or follow-up).",
            f"- Persons who progressed (any graded trunk segment, from the sheets): {count_of(int(Yv.sum()), len(Yv))}; "
            f"did not: {count_of(int(len(Yv) - Yv.sum()), len(Yv))}.",
            f"- Persons whose outcome differs if only split segments count (the old definition): "
            f"{count_of(discord, len(Yv))}.",
            f"- BL eval flag (ct_cag_<seg>_eval == 0 as unevaluable): {'applied' if eval_applied else 'NOT applied'}; "
            f"it removes {count(lost_eval)} otherwise graded rows."
            + ("" if eval_applied or args.no_bl_eval else " Not applied because it would remove more than half: check "
               "the flag's coding."),
            f"- Missing T2.5 on split rows (too short for two angles): {count(int((d['not_split'].eq(0) & d[FEATURE].isna()).sum()))}; "
            "set to the training mean like the not-split rows.\n",
            "Rows per segment, split by the trunk split or not:\n"]
    sp = np.array([[int(((d["segment"] == s) & (d["not_split"] == v)).sum()) for v in (0, 1)] for s in segs])
    rep += table(["segment", "split", "not split"], [(s, *r) for s, r in zip(segs, suppress(sp))])
    pp = d.groupby("id").size().value_counts().reindex(range(1, 10), fill_value=0)
    rep += ["\nGraded trunk segments per person:\n"] + table(list(map(str, pp.index)), [suppress([pp.to_numpy()])[0]])
    dom = P.loc[Y.index, "dominance"].value_counts().reindex(["right", "left", "codominant", "other", "missing"], fill_value=0)
    rep += ["\nDominance (fixed labels):\n"] + table(list(dom.index), [suppress([dom.to_numpy()])[0]])
    cls = ["none", "plaque", "unevaluable / missing"]
    gr = g_raw.assign(c=grade_class(g_raw["bl_raw"]), e=g_raw["eval"].map({0: "eval 0", 1: "eval 1"}).fillna("eval missing"))
    et = np.array([[int(((gr["e"] == e) & (gr["c"] == c)).sum()) for c in cls] for e in ("eval 0", "eval 1", "eval missing")])
    rep += ["\nBL eval flag against the BL grade (9 trunk segments, all people with a tree):\n"]
    rep += table(["", *cls], [(e, *r) for e, r in zip(("eval 0", "eval 1", "eval missing"), suppress(et))])
    gf = g_raw.assign(c=grade_class(g_raw["fu"]), v=np.where(g_raw["fu_vessel_uneval"] > 0, "vessel flagged",
                                                             np.where(g_raw["fu_vessel_uneval"] == 0, "not flagged", "flag missing")))
    vt = np.array([[int(((gf["v"] == v) & (gf["c"] == c)).sum()) for c in cls] for v in ("vessel flagged", "not flagged", "flag missing")])
    rep += ["\nFU vessel unevaluable flag against the FU segment grade (reported only, not applied):\n"]
    rep += table(["", *cls], [(v, *r) for v, r in zip(("vessel flagged", "not flagged", "flag missing"), suppress(vt))])

    # ---- report: fits
    rep += ["\n## Full-data fits\n",
            f"Gauss-Hermite with {args.nodes} nodes, cold start, cloglog. exp(β) is a segment hazard ratio.\n"]
    rows, flags = [], []
    for nm in names["G03"][1:]:
        cells = []
        for m in MODELS:
            if nm in names[m]:
                i = names[m].index(nm)
                b, s = fits[m]["beta"][i], ses[m][i]
                if not fits[m]["keep"][i]:
                    cells.append("dropped (constant)")
                    continue
                cells.append(f"{np.exp(b):.2f} ({np.exp(b - 1.96 * s):.2f} to {np.exp(b + 1.96 * s):.2f})")
                if abs(b) > SEPARATION or (np.isfinite(s) and s > SEPARATION):
                    flags.append(f"{m}: {nm}")
            else:
                cells.append("")
        rows.append((nm, *cells))
    rows.append(("person SD s", *(f"{fits[m]['sigma']:.2f}" for m in MODELS)))
    rep += table(["term", "B2 exp(β) (95% CI)", "G03 exp(β) (95% CI)"], rows)
    rep += ["", *table(["model", "log-likelihood", "converged", "min Hessian eigenvalue"],
                       [(m, f"{fits[m]['ll']:.2f}", f"{fits[m]['ok']} ({fits[m]['msg']})", f"{eig[m]:.3g}") for m in MODELS])]
    if flags:
        rep.append(f"\n**Possible separation (|β| or SE > {SEPARATION:g}):** {'; '.join(flags)}.")
    if any(eig[m] <= 0 for m in MODELS):
        rep.append("\n**A Hessian is not positive definite: the SEs above are not valid.**")
    rep += ["\n### Test of mean T2.5 (prespecified: all rows)\n",
            lr_line(fits, "All rows (not-split indicator in both models)"),
            lr_line(cc_fits, "Complete cases (split rows only), sensitivity"), "",
            "### Quadrature check (always run)\n",
            f"Tolerances fixed before running: β {NODE_TOL['beta']}, s {NODE_TOL['sigma']}, log-lik {NODE_TOL['ll']}, "
            f"person risk {RISK_TOL}.\n",
            *table(["model", "nodes", "max Δβ", "Δs", "Δ log-lik", f"person risk {RISK_NODES} vs {MAX_NODES}", ""], node_rows)]

    # ---- report: CV metrics
    sig = {m: np.concatenate([r[m]["sigma"] for r in reps]) for m in MODELS}
    fails = {m: sum(r[m]["fail"] for r in reps) for m in MODELS}
    keys = list(reps[0]["B2"]["metrics"])
    est = {m: {k: np.mean([r[m]["metrics"][k] for r in reps]) for k in keys} for m in MODELS}
    rep += ["\n## Cross-validated person metrics\n",
            f"Estimate: mean over {args.repeats} fold splits. 95% CI: person bootstrap, {args.boot} replicates (paired, "
            "the whole CV rerun). Split variability: 2.5-97.5 percentile over the fold splits; it is not a CI. "
            "Δ = G03 − B2; estimates, not tests. Δ log loss is the primary comparison.\n"]
    trows = []
    for k in keys:
        for m in MODELS:
            sv = [r[m]["metrics"][k] for r in reps]
            trows.append((k, m, f"{est[m][k]:.3f}", "%.3f to %.3f" % ci([b[m][k] for b in boot]) if boot else "",
                          "%.3f to %.3f" % ci(sv)))
        dv = [r["G03"]["metrics"][k] - r["B2"]["metrics"][k] for r in reps]
        trows.append((k, "Δ", f"{est['G03'][k] - est['B2'][k]:+.3f}",
                      "%+.3f to %+.3f" % ci([b["G03"][k] - b["B2"][k] for b in boot]) if boot else "", "%+.3f to %+.3f" % ci(dv)))
    rep += table(["metric", "model", "estimate", "95% CI (bootstrap)", "split variability"], trows)
    rep += [f"\nFold fits not reporting convergence: B2 {fails['B2']}, G03 {fails['G03']} of {args.repeats * args.folds} each. "
            f"Fold s: median B2 {np.median(sig['B2']):.2f}, G03 {np.median(sig['G03']):.2f} "
            f"(5th-95th pct B2 {np.percentile(sig['B2'], 5):.2f}-{np.percentile(sig['B2'], 95):.2f}); "
            f"fits with s < {SIGMA_FLOOR} after the refit: {int((sig['B2'] < SIGMA_FLOOR).sum() + (sig['G03'] < SIGMA_FLOOR).sum())}."]

    # ---- report: per segment
    auc_rows = [("person", n_lab(Yv), {m: est[m]["C"] for m in MODELS},
                 {m: ci([b[m]["C"] for b in boot]) for m in MODELS} if boot else None)]
    for s in scored:
        S = (d["segment"] == s).to_numpy()
        auc_rows.append((s, n_lab(y[S]), {m: np.nanmean([r[m]["seg_auc"][s] for r in reps]) for m in MODELS},
                         {m: ci([b[m][f"seg {s}"] for b in boot]) for m in MODELS} if boot else None))
    rep += ["\n## AUC per person and per segment\n",
            "Segments: the same pooled fits, each segment's marginal risk; AUC within a segment type compares people "
            "(who progresses in, say, the pLAD). Exploratory: 9 unadjusted comparisons. Estimate = mean over fold splits; "
            "CI = person bootstrap.\n"]
    arows = []
    for lab, n, e, c in auc_rows:
        dl = ci([b["G03"]["C" if lab == "person" else f"seg {lab}"] - b["B2"]["C" if lab == "person" else f"seg {lab}"]
                 for b in boot]) if boot else (np.nan, np.nan)
        arows.append((lab, n, *(f"{e[m]:.3f}" + (" (%.3f to %.3f)" % c[m] if c else "") for m in MODELS),
                      f"{e['G03'] - e['B2']:+.3f}" + (" (%+.3f to %+.3f)" % dl if boot else "")))
    for s in segs:
        if s not in scored:
            S = (d["segment"] == s).to_numpy()
            arows.append((s, n_lab(y[S]), f"fewer than {MIN_CELL} progressed or stable: not scored", "", ""))
    rep += table(["level", "progressed / rows", "AUC B2", "AUC G03", "ΔAUC"], arows)

    # ---- report: confusion matrices
    r0 = reps[0]
    panels = [("person", n_lab(Yv), Yv, {m: r0[m]["P"] for m in MODELS}, {m: thr0[m]["person"] for m in MODELS})]
    for s in scored:
        S = (d["segment"] == s).to_numpy()
        panels.append((s, n_lab(y[S]), y[S], {m: r0[m]["seg"][S] for m in MODELS}, {m: thr0[m]["segment"][S] for m in MODELS}))
    crows = []
    for lab, _, yv, p, th in panels:
        cells = []
        for m in MODELS:
            tp, fn, fp, tn = confusion(yv, p[m], th[m])
            sh = shown_confusion(np.array([[tp, fn], [fp, tn]])).ravel()
            ok = all(isinstance(v, (int, np.integer)) for v in sh)
            cells += [*map(str, sh), f"{100 * tp / max(tp + fn, 1):.0f}%" if ok else "hidden",
                      f"{100 * tn / max(tn + fp, 1):.0f}%" if ok else "hidden"]
        crows.append((lab, *cells))
    rep += ["\n## Confusion matrices\n",
            "Test folds of repeat 0. Cut-off: Youden's J on inner 5-fold CV predictions of the training fold (persons; "
            "each segment on its own rows). A row with any hidden cell is hidden whole.\n"]
    rep += table(["level", *(f"{m} {c}" for m in MODELS for c in ("TP", "FN", "FP", "TN", "sens", "spec"))], crows)

    fig_auc(auc_rows, out_dir)
    fig_roc(panels, out_dir)
    fig_confusion(panels, out_dir)
    fig_calibration(Yv, {m: r0[m]["P"] for m in MODELS}, args.bins, out_dir)
    fig_split_variability(reps, out_dir)
    rep.append(f"\nFigures: {PREFIX}_auc.png (person and every segment), {PREFIX}_roc.png, {PREFIX}_confusion.png, "
               f"{PREFIX}_calibration.png, {PREFIX}_split_variability.png. Fold files in folds/ hold IDs: do not share.\n")
    Path(args.out).write_text("\n".join(rep))
    print("\n".join(rep))


if __name__ == "__main__":
    main()
