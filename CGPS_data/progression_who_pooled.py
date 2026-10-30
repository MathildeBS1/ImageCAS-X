"""Who, pooled engine (who-progression B2 and G02): does geometry add to the SCORE2 factors in predicting who progresses?

    python progression_who_pooled.py [--src TREE_FOLDER] [--person score2|factors] [--folds 10] [--repeats 50]
                                     [--nodes 30] [--check]
    python progression_who_pooled.py --synthetic      # fitter and pooling self-test, no data needed

Rows: the 9 split trunk segments of each Medis tree (progression_turning.build) with a visual grade at BL and FU;
occluded-at-BL segments are dropped. Segment outcome: higher grade at FU than at BL. Person outcome: any of the
person's graded trunk segments progressed. People without SCORE2, dominance or follow-up are dropped.

Engine (experiments/who-progression/pooled_score2/pooling.md): a segment-level cloglog GLMM with a person random
intercept b ~ N(0, s^2), fitted by Gauss-Hermite quadrature with an analytic gradient, then pooled to person risk
    P_i = 1 - int exp(-e^b sum_j exp(eta_ij)) phi(b; 0, s^2) db.
  B2  = log follow-up + log SCORE2 (score2, else score2_op; z) + dominance (right vs not)
        + segment position (ref pLAD) + log length + BL grade;
        --person factors replaces log SCORE2 by the refitted factors: age, male, current smoking, SBP, total
        cholesterol, HDL (continuous ones z-scored).
  G02 = B2 + mean T5 (z within segment type) + LM bifurcation angle (z, on the pLAD and pCX rows only).
Everything learned (z-score constants, coefficients, s) is fitted on the training persons.

Validation: 10 person folds stratified on the person outcome, repeated with seeds 0..R-1; the same folds for B2 and
G02. Per repeat, from the pooled out-of-fold person risks: C, Brier, log loss, calibration slope and intercept.
Reported as mean and 2.5/97.5 percentiles over repeats, with the paired difference G02 - B2 (an estimate, not a test).
Per segment: the same fits give each segment's marginal risk (integrated over b); AUC per segment type over repeats.
Confusion matrices (person and per segment, repeat 0): cut-off = Youden's J on the training fold's own predictions.
Inference: one likelihood-ratio test of the geometry block on the full-data fits.
--check: refit with doubled nodes, and the person-risk integral with 40 vs 200 nodes.
Aggregates only (counts 1-4 hidden); writes progression_who_pooled.md and progression_who_pooled_*.png.
"""
import argparse
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import check_grad, minimize
from scipy.special import logsumexp
from scipy.stats import chi2

import hoe10y_qc as hq
import progression_angle as pa
import progression_segment_models as psm
import progression_turning as pt
from cgps_stats import MIN_CELL, OUT_DIR, count, num, suppress, yes

PREFIX = "progression_who_pooled"
SCORE2_COLS = {"age": "scan_age", "male": "male", "smoking": "hist_smoking_current", "sbp": "clin_bp_sys_mean",
               "tc": "tot_cholesterol", "hdl": "hdl"}  # refitted SCORE2 factors
CONTINUOUS = ("age", "sbp", "tc", "hdl")  # z-scored on the training persons
ANGLE_SEGS = ("plad", "pcx")  # the rows the LM bifurcation angle can act on
REF_SEG = "plad"
MODELS = ("B2", "G02")
GEOMETRY = {"B2": (), "G02": ("mean T5", "LM angle")}
COLOR = {"B2": pt.MODEL_COLOR["base"], "G02": pt.MODEL_COLOR["turning + angle"]}
LOG_SIGMA_BOUNDS = (-8.0, 3.0)  # s from 3e-4 (no clustering) to 20
NODE_TOL = {"beta": 1e-3, "sigma": 1e-3, "ll": 0.05}  # set before running; optimiser noise alone moves ll ~0.02
RISK_TOL = 1e-6


# ---------------------------------------------------------------- data
def person_covariates():
    """Person table indexed like progression_turning.build: SCORE2 factors and right dominance (NaN = unknown)."""
    bl = hq.load_sheets(hq.ROOT)["BL"]
    bl = bl.assign(id=bl["study_id"].map(hq.norm_id)).drop_duplicates("id").set_index("id")
    P = pd.DataFrame({k: num(bl[c]) for k, c in SCORE2_COLS.items()})
    P["male"], P["smoking"] = yes(bl["male"]), yes(bl["hist_smoking_current"])
    dom = bl["ct_cag_dominance"].astype(str).str.strip().str.lower().where(bl["ct_cag_dominance"].notna())
    P["right"] = dom.str.startswith("r").astype(float).where(dom.notna())
    return P, dom


def sort_by_person(d):
    return d.sort_values(["id", "segment"], kind="stable").reset_index(drop=True)


def starts_of(ids):
    """First row of each person in rows sorted by person (for np.add.reduceat)."""
    ids = np.asarray(ids)
    return np.r_[0, np.flatnonzero(ids[1:] != ids[:-1]) + 1]


def person_columns(person):
    """Person columns a row must have for the chosen person block."""
    return (list(SCORE2_COLS) if person == "factors" else ["score2"]) + ["right"]


def design(d, train, terms, segs, grades, person):
    """Fixed-effect design (n, p) and column names; constants learned on the training rows only."""
    people = d[train].drop_duplicates("id")
    X, names = [np.ones(len(d)), np.log(d["years"].to_numpy())], ["intercept", "log follow-up"]
    if person == "factors":
        for c in CONTINUOUS:
            X.append(((d[c] - people[c].mean()) / people[c].std()).to_numpy())
            names.append(f"{c} (per SD)")
        X += [d[c].to_numpy(float) for c in ("male", "smoking")]
        names += ["male", "current smoking"]
    else:
        ls2 = np.log(people["score2"])
        X.append(((np.log(d["score2"]) - ls2.mean()) / ls2.std()).to_numpy())
        names.append("log SCORE2 (per SD)")
    X.append(d["right"].to_numpy(float))
    names.append("right dominance")
    X += pt.dummies(d, "segment", [s for s in segs if s != REF_SEG])
    names += [s for s in segs if s != REF_SEG]
    X.append(np.log(d["length"].clip(lower=1.0)).to_numpy())
    names.append("log length")
    X += pt.dummies(d, "grade", grades[1:])
    names += [f"BL {g}" for g in grades[1:]]
    if "mean T5" in terms:
        X.append(pt.zscore(d, "mean_T5", train))
        names.append("mean T5 (per SD, within type)")
    if "LM angle" in terms:
        a = (d["angle"] - people["angle"].mean()) / people["angle"].std()
        X.append(a.fillna(0).to_numpy() * d["segment"].isin(ANGLE_SEGS).to_numpy())
        names.append("LM angle (per SD, pLAD/pCX rows)")
    return np.column_stack(X), names


# ---------------------------------------------------------------- engine: cloglog GLMM, person random intercept
def _nll(theta, X, y, starts, row_person, x, logw, l2):
    """Negative marginal log-likelihood and its gradient in (beta, log s)."""
    beta, ls = theta[:-1], theta[-1]
    u = np.sqrt(2.0) * np.exp(ls) * x                             # (K,) values of b at the nodes
    eta = np.clip((X @ beta)[:, None] + u[None], -30, 30)          # (n, K)
    mu = np.exp(eta)                                               # segment hazard
    em = np.exp(-mu)
    one = y[:, None] == 1
    lij = np.where(one, np.log(-np.expm1(-mu)), -mu)               # log P(y | b), stable for small and large mu
    a = np.add.reduceat(lij, starts, axis=0) + logw[None]          # (m, K) person log-lik per node
    lse = logsumexp(a, axis=1)
    r = np.exp(a - lse[:, None])[row_person]                       # posterior node weights, per row
    g = np.where(one, mu * em / np.maximum(-np.expm1(-mu), 1e-300), -mu)  # d log P(y | b) / d eta
    rg = r * g
    grad = np.r_[X.T @ rg.sum(1), (rg * u[None]).sum()]
    grad[:-1] -= 2 * l2 * beta
    return -(lse.sum() - l2 * beta @ beta), -grad


def fit_glmm(X, y, ids, nodes, l2=1e-6, theta0=None):
    starts = starts_of(ids)
    row_person = np.repeat(np.arange(len(starts)), np.diff(np.r_[starts, len(ids)]))
    x, w = np.polynomial.hermite.hermgauss(nodes)
    args = (X, y, starts, row_person, x, np.log(w / np.sqrt(np.pi)), l2)
    if theta0 is None:
        theta0 = np.zeros(X.shape[1] + 1)
        theta0[0] = np.log(-np.log(1 - np.clip(y.mean(), 0.01, 0.99)))
    bounds = [(None, None)] * X.shape[1] + [LOG_SIGMA_BOUNDS]
    r = minimize(_nll, theta0, args=args, jac=True, method="L-BFGS-B", bounds=bounds,
                 options={"maxiter": 5000, "maxfun": 10000})
    return {"theta": r.x, "beta": r.x[:-1], "sigma": float(np.exp(r.x[-1])), "ll": -float(r.fun),
            "ok": bool(r.success), "msg": str(r.message), "args": args}


def wald_se(fit, h=1e-5):
    """Standard errors of (beta, log s) from a central-difference Hessian of the analytic gradient."""
    th, k = fit["theta"], len(fit["theta"])
    H = np.zeros((k, k))
    for i in range(k):
        e = np.zeros(k); e[i] = h
        H[:, i] = (_nll(th + e, *fit["args"])[1] - _nll(th - e, *fit["args"])[1]) / (2 * h)
    H = (H + H.T) / 2
    return np.sqrt(np.clip(np.diag(np.linalg.pinv(H)), 0, None))


def segment_risk(X, beta, sigma, nodes=40):
    """Marginal P(segment progresses), integrating over b: the pooled model's prediction for one segment."""
    x, w = np.polynomial.hermite.hermgauss(nodes)
    u, w = np.sqrt(2.0) * sigma * x, w / np.sqrt(np.pi)
    return 1 - (w[None] * np.exp(-np.exp(u)[None] * np.exp(np.clip(X @ beta, -30, 30))[:, None])).sum(1)


def person_risk(X, beta, sigma, ids, nodes=40):
    """P(any segment progresses) per person, integrating over b (pooling.md). Persons in row order."""
    x, w = np.polynomial.hermite.hermgauss(nodes)
    u, w = np.sqrt(2.0) * sigma * x, w / np.sqrt(np.pi)
    S = np.add.reduceat(np.exp(np.clip(X @ beta, -30, 30)), starts_of(ids))
    return 1 - (w[None] * np.exp(-np.exp(u)[None] * S[:, None])).sum(1)


# ---------------------------------------------------------------- metrics
def cal_intercept(y, lp):
    """Calibration-in-the-large: intercept a of logit P(y) = a + lp (offset)."""
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
    return {"C": pt.auc(y, p)[0], "Brier": np.mean((p - y) ** 2),
            "log loss": -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)),
            "cal. slope": pt.fit(np.column_stack([np.ones(len(y)), lp]), y)[0][1], "cal. intercept": cal_intercept(y, lp)}


def person_folds(Y, k, rng):
    """{id: fold}, k folds stratified on the person outcome Y (Series indexed by id)."""
    out = {}
    for _, ids in Y.groupby(Y):
        out.update(zip(rng.permutation(ids.index), np.arange(len(ids)) % k))
    return out


# ---------------------------------------------------------------- figures
def fig_calibration(Y, oof, bins, out_dir):
    """Binned person calibration (repeat 0). A bin with fewer than MIN_CELL events or non-events is not drawn."""
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


def fig_deltas(rep_metrics, out_dir):
    plt = pt._plt()
    keys = ("C", "Brier", "log loss", "cal. slope")
    fig, axes = plt.subplots(1, len(keys), figsize=(11, 3.2))
    for ax, key in zip(axes, keys):
        pt._grid(ax, "y")
        dlt = np.array([r["G02"][key] - r["B2"][key] for r in rep_metrics])
        ax.boxplot(dlt, widths=0.5, medianprops={"color": COLOR["G02"]}, flierprops={"markersize": 3})
        ax.axhline(0, color=pt.MUTED, lw=1, ls=":")
        ax.set_xticks([])
        ax.set_title(f"Δ {key}", fontsize=10)
    fig.suptitle(f"G02 − B2 over {len(rep_metrics)} CV repeats (paired, same folds)", x=0.01, ha="left",
                 fontsize=11, fontweight="bold", color=pt.INK)
    pt._save(fig, out_dir / f"{PREFIX}_deltas.png")


def fig_auc(rows, out_dir):
    """AUC per level (person, then segments): mean over repeats with 2.5/97.5 percentile bars."""
    plt = pt._plt()
    fig, ax = plt.subplots(figsize=(7.5, 0.55 * len(rows) + 1.4))
    pt._grid(ax, "x")
    yy = np.arange(len(rows))[::-1].astype(float)
    for y_, (lab, _, aucs) in zip(yy, rows):
        for k, m in enumerate(MODELS):
            v, off = np.asarray(aucs[m]), (0.18 if k == 0 else -0.18)
            a, lo, hi = v.mean(), np.percentile(v, 2.5), np.percentile(v, 97.5)
            ax.barh(y_ + off, a - 0.5, left=0.5, height=0.34, color=COLOR[m], label=m if y_ == yy[0] else None)
            ax.plot([lo, hi], [y_ + off] * 2, color=pt.INK2, lw=1)
            ax.text(max(hi, a) + 0.005, y_ + off, f"{a:.2f}", va="center", fontsize=7.5, color=pt.INK2)
    ax.axvline(0.5, color=pt.MUTED, lw=1, ls=":")
    ax.axhline(yy[0] - 0.5, color=pt.MUTED, lw=0.8)
    ax.set_yticks(yy, [f"{lab}  ({n})" for lab, n, _ in rows])
    for lab, (name, _, _) in zip(ax.get_yticklabels(), rows):
        lab.set_color({"LAD": "#2a78d6", "LCx": "#1baf7a", "RCA": "#e34948"}.get(pt.VESSEL.get(name), pt.INK))
        lab.set_fontweight("bold")
    ax.set_xlim(min(0.4, min(np.percentile(a[m], 2.5) for _, _, a in rows for m in MODELS) - 0.03), 1.0)
    ax.set_xlabel("AUC on the test folds (0.5 = chance); bars: 2.5th to 97.5th percentile over repeats")
    ax.set_title("AUC per person and per segment: B2 vs G02 (one pooled model)")
    ax.legend(fontsize=8, loc="lower right")
    fig.text(0.01, 0.01, "(progressed/rows). Segment rows use the pooled model's segment risk; AUC within a segment "
             "compares people.", fontsize=7.5, color=pt.INK2)
    pt._save(fig, out_dir / f"{PREFIX}_auc.png", rect=(0, 0.03, 1, 1))


def fig_roc(panels, out_dir):
    """ROC per level on the test folds of repeat 0; binned so no single person is a visible step."""
    plt = pt._plt()
    ncol = 4
    nrow = -(-len(panels) // ncol)
    fig, axes = plt.subplots(nrow, ncol, figsize=(3.3 * ncol, 3.2 * nrow), sharex=True, sharey=True, squeeze=False)
    grid = np.linspace(0, 1, 21)
    for ax, (lab, n, yv, p, _) in zip(axes.ravel(), panels):
        pt._grid(ax, "both")
        ax.plot([0, 1], [0, 1], lw=1, ls=":", color=pt.MUTED)
        for m in MODELS:
            a, fpr, tpr = pt.auc(yv, p[m])
            ax.plot(grid, [tpr[fpr <= g].max() for g in grid], lw=2.2 if m == "B2" else 1.8, color=COLOR[m],
                    label=f"{m}  (AUC {a:.2f})")
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


def fig_confusion(panels, out_dir):
    plt = pt._plt()
    fig, axes = plt.subplots(len(panels), 2, figsize=(6.4, 2.3 * len(panels)), squeeze=False)
    cell_col = np.array([["#1baf7a", pt.MISSED], ["#e34948", "#1baf7a"]])  # TP, FN / FP, TN
    for row, (lab, _, yv, p, thr) in zip(axes, panels):
        for ax, m in zip(row, MODELS):
            tp, fn, fp, tn = pt.confusion(yv, p[m], thr[m])
            M = np.array([[tp, fn], [fp, tn]])
            share = M / np.maximum(M.sum(axis=1, keepdims=True), 1)
            shown = suppress(M)
            row_ok = [all(isinstance(v, (int, np.integer)) for v in r_) for r_ in shown]  # a share would reveal a hidden cell
            for (i, j), v in np.ndenumerate(shown):
                alpha = 0.18 + 0.75 * share[i, j] if row_ok[i] else 0.3
                ax.add_patch(plt.Rectangle((j - 0.48, i - 0.48), 0.96, 0.96, color=cell_col[i, j], alpha=alpha))
                ax.text(j, i - 0.1, v, ha="center", va="center", fontsize=11, fontweight="bold", color=pt.INK)
                if row_ok[i]:
                    ax.text(j, i + 0.25, f"{100 * share[i, j]:.0f}% of row", ha="center", va="center", fontsize=6.5,
                            color=pt.INK2)
            ax.set_xlim(-0.5, 1.5); ax.set_ylim(1.5, -0.5)
            ax.set_xticks([0, 1], ["called progress", "called stable"], fontsize=7)
            ax.set_yticks([0, 1], ["progressed", "stable"], fontsize=7)
            ax.tick_params(length=0)
            for sp in ax.spines.values():
                sp.set_visible(False)
            ax.set_title(f"{lab}: {m}  (AUC {pt.auc(yv, p[m])[0]:.2f})", color=COLOR[m], fontsize=9)
    fig.suptitle("Confusion matrices on the test folds (repeat 0)", x=0.01, ha="left", fontsize=12,
                 fontweight="bold", color=pt.INK)
    fig.text(0.01, 0.003, "Cut-off: Youden's J on the training fold's own predictions (per level). Green = correct, orange = missed\n"
             "progression, red = false alarm; darker = larger share of its row.", fontsize=7.5, color=pt.INK2)
    pt._save(fig, out_dir / f"{PREFIX}_confusion.png", rect=(0, 0.015, 1, 0.99))


# ---------------------------------------------------------------- self-test (no data)
def synthetic(seed=1):
    """Recover a known cloglog GLMM, check the gradient, and show why the two pooling shortcuts fail."""
    rng = np.random.default_rng(seed)
    m, J, sigma = 1500, 9, 1.2
    ids = np.repeat(np.arange(m), J)
    X = np.column_stack([np.ones(m * J), np.repeat(rng.normal(size=m), J), rng.normal(size=m * J),
                         np.tile(np.arange(J) == 0, m).astype(float)])
    beta = np.array([-2.2, 0.4, 0.25, 0.6])
    b = np.repeat(rng.normal(0, sigma, m), J)
    y = (rng.random(m * J) < 1 - np.exp(-np.exp(X @ beta + b))).astype(float)
    Y = np.add.reduceat(y, starts_of(ids)) > 0

    fit = fit_glmm(X, y, ids, 30)
    err = check_grad(lambda t: _nll(t, *fit["args"])[0], lambda t: _nll(t, *fit["args"])[1], fit["theta"] + 0.05)
    se = wald_se(fit)
    print(f"converged: {fit['ok']} ({fit['msg']}); gradient check error {err:.2e}")
    for name, t, e, s in zip(["b0", "person z", "segment z", "segment 1"] + ["log s"], np.r_[beta, np.log(sigma)],
                             fit["theta"], se):
        print(f"  {name:10s} true {t:+.3f}  est {e:+.3f}  (SE {s:.3f})")
    P = person_risk(X, fit["beta"], fit["sigma"], ids)
    x, w = np.polynomial.hermite.hermgauss(40)
    seg = 1 - (w / np.sqrt(np.pi) * np.exp(-np.exp(np.sqrt(2) * fit["sigma"] * x)[None] * np.exp(X @ fit["beta"])[:, None])).sum(1)
    product = 1 - np.exp(np.add.reduceat(np.log1p(-seg), starts_of(ids)))
    b0 = 1 - np.exp(-np.add.reduceat(np.exp(X @ fit["beta"]), starts_of(ids)))
    print(f"observed person prevalence {Y.mean():.3f}; mean risk: integral {P.mean():.3f}, "
          f"product of marginal segment risks {product.mean():.3f}, b = 0 {b0.mean():.3f}")
    print(f"integral 40 vs 200 nodes: max |diff| {np.abs(P - person_risk(X, fit['beta'], fit['sigma'], ids, 200)).max():.1e}")


# ---------------------------------------------------------------- main
def fmt_ci(v):
    return f"{np.mean(v):.3f} ({np.percentile(v, 2.5):.3f} to {np.percentile(v, 97.5):.3f})"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / f"{PREFIX}.md"))
    ap.add_argument("--folds", type=int, default=10)
    ap.add_argument("--repeats", type=int, default=50)
    ap.add_argument("--nodes", type=int, default=30)
    ap.add_argument("--bins", type=int, default=5)
    ap.add_argument("--person", choices=("score2", "factors"), default="score2",
                    help="person block of B2: log SCORE2 (default) or the refitted SCORE2 factors")
    ap.add_argument("--check", action="store_true", help="node-doubling and integral checks on the full-data fits")
    ap.add_argument("--synthetic", action="store_true", help="self-test on simulated data, then exit")
    args = ap.parse_args()
    if args.synthetic:
        synthetic()
        return
    out_dir = Path(args.out).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    # ---- cohort
    d0, graded, skipped = pt.build(args.src)
    P, dom = person_covariates()
    d0 = d0.join(P, on="id")
    d0["angle"] = d0["id"].map(pa.angles(args.src))
    cov_ok = d0[person_columns(args.person)].notna().all(axis=1) & (d0["years"] > 0)
    if args.person == "score2":
        cov_ok &= d0["score2"] > 0
    keep = graded & cov_ok
    d = sort_by_person(d0[keep].assign(grade=lambda x: x["bl"].map(pt.GRADE)))
    d["grade"] = psm.merge_grades(d["grade"])
    grades = [g for g in psm.GRADES if g in set(d["grade"])]
    segs = [REF_SEG] + [s for s in pt.SEG_ORDER if s != REF_SEG and s in set(d["segment"])]
    y, ids = d["y"].to_numpy(), d["id"].to_numpy()
    Y = d.groupby("id", sort=False)["y"].max()  # person outcome, in the row order of the persons
    n_events = int(Y.sum())
    if min(n_events, len(Y) - n_events) < MIN_CELL:
        raise SystemExit(f"fewer than {MIN_CELL} persons with or without progression: not fitted")

    seg_rows = {s: (d["segment"] == s).to_numpy() for s in segs}
    seg_left_out = {s: (int(S.sum()), int(y[S].sum())) for s, S in seg_rows.items()
                    if min(y[S].sum(), S.sum() - y[S].sum()) < MIN_CELL}
    seg_rows = {s: S for s, S in seg_rows.items() if s not in seg_left_out}
    Yv = Y.to_numpy()

    # ---- full-data fits, LR test, checks
    full = np.ones(len(d), bool)
    fits, names, Xs = {}, {}, {}
    for m in MODELS:
        Xs[m], names[m] = design(d, full, GEOMETRY[m], segs, grades, args.person)
        fits[m] = fit_glmm(Xs[m], y, ids, args.nodes)
    df_geo = len(names["G02"]) - len(names["B2"])
    lr = 2 * (fits["G02"]["ll"] - fits["B2"]["ll"])
    p_lr = chi2.sf(max(lr, 0.0), df_geo)
    checks = []
    if args.check:
        for m in MODELS:
            f2 = fit_glmm(Xs[m], y, ids, 2 * args.nodes, theta0=fits[m]["theta"])
            db = np.abs(f2["beta"] - fits[m]["beta"]).max()
            ds, dl = abs(f2["sigma"] - fits[m]["sigma"]), abs(f2["ll"] - fits[m]["ll"])
            r40 = person_risk(Xs[m], fits[m]["beta"], fits[m]["sigma"], ids, 40)
            r200 = person_risk(Xs[m], fits[m]["beta"], fits[m]["sigma"], ids, 200)
            dr = np.abs(r40 - r200).max()
            ok = db < NODE_TOL["beta"] and ds < NODE_TOL["sigma"] and dl < NODE_TOL["ll"] and dr < RISK_TOL
            checks.append(f"| {m} | {args.nodes} vs {2 * args.nodes} | {db:.1e} | {ds:.1e} | {dl:.1e} | {dr:.1e} | "
                          f"{'pass' if ok else 'FAIL'} |")

    # ---- cross-validation
    rep_metrics, seg_auc, fails, first = [], [], {m: 0 for m in MODELS}, None
    for r in range(args.repeats):
        fold_of = person_folds(Y, args.folds, np.random.default_rng(r))
        fold = d["id"].map(fold_of).to_numpy()
        pfold = Y.index.map(fold_of).to_numpy()
        oof = {m: np.zeros(len(Y)) for m in MODELS}
        seg_oof = {m: np.zeros(len(d)) for m in MODELS}
        thr = {m: {"person": np.zeros(len(Y)), "segment": np.zeros(len(d))} for m in MODELS}
        for m in MODELS:
            theta = None
            for k in range(args.folds):
                tr, te = fold != k, fold == k
                assert not set(ids[tr]) & set(ids[te]), "a person is in both train and test"
                X, _ = design(d, tr, GEOMETRY[m], segs, grades, args.person)
                f = fit_glmm(X[tr], y[tr], ids[tr], args.nodes, theta0=theta)
                fails[m] += not f["ok"]
                theta = f["theta"]
                oof[m][pfold == k] = person_risk(X[te], f["beta"], f["sigma"], ids[te])
                seg_oof[m][te] = segment_risk(X[te], f["beta"], f["sigma"])
                thr[m]["person"][pfold == k] = psm.youden(Yv[pfold != k], person_risk(X[tr], f["beta"], f["sigma"], ids[tr]))
                str_ = segment_risk(X[tr], f["beta"], f["sigma"])
                for S in seg_rows.values():
                    thr[m]["segment"][te & S] = psm.youden(y[tr & S], str_[S[tr]])
        rep_metrics.append({m: metrics(Yv, oof[m]) for m in MODELS})
        seg_auc.append({m: {s: pt.auc(y[S], seg_oof[m][S])[0] for s, S in seg_rows.items()} for m in MODELS})
        first = first or (oof, seg_oof, thr)
        print(f"repeat {r + 1}/{args.repeats}: C B2 {rep_metrics[-1]['B2']['C']:.3f}, G02 {rep_metrics[-1]['G02']['C']:.3f}")

    # ---- report
    per_person = d.groupby("id").size().value_counts().reindex(range(1, 10), fill_value=0)
    code = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:12]
    rep = ["# Who, pooled engine: B2 vs G02 on plaque progression (Medis trees)\n",
           f"Aggregates only; counts 1-4 shown as <{MIN_CELL}. Person block: {args.person}. Script sha256 {code}; seeds 0..{args.repeats - 1}. "
           "The Medis trees are almost all people with plaque at baseline: this is progression, not new plaque.\n",
           "## Cohort\n",
           f"- Segments: {count(len(d))} from {count(len(Y))} people. Persons who progressed (any graded trunk segment "
           f"with a higher grade at FU): {count(n_events)}; did not: {count(len(Y) - n_events)}.",
           f"- Left out: {count(int((~graded).sum()))} segment rows without a usable BL/FU grade or occluded at BL; "
           f"{count(int((graded & ~cov_ok).sum()))} rows of {count(d0.loc[graded & ~cov_ok, 'id'].nunique())} people "
           f"without {'all SCORE2 factors' if args.person == 'factors' else 'SCORE2'}, dominance or follow-up. Trees that could not be split: {count(skipped)}.",
           f"- Missing geometry is set to the training mean (z = 0): mean T5 on {count(int(d['mean_T5'].isna().sum()))} "
           f"rows, LM angle for {count(int(d.drop_duplicates('id')['angle'].isna().sum()))} people.",
           f"- BL grade levels in the model: {', '.join(grades)} (a level with < {MIN_CELL} rows is merged into the one below).\n",
           "Graded trunk segments per person (they make up S_i and the person outcome):\n",
           "| " + " | ".join(map(str, per_person.index)) + " |", "|" + "---|" * len(per_person),
           "| " + " | ".join(map(str, suppress([per_person.to_numpy()])[0])) + " |\n",
           "Dominance at BL among the people in the model:\n", "| dominance | people |", "|---|---|"]
    rep += [f"| {k} | {count(v)} |" for k, v in dom.reindex(Y.index).fillna("missing").value_counts().items()]

    rep += ["\n## Full-data fits\n",
            f"Gauss-Hermite with {args.nodes} nodes, cloglog. exp(β) is a hazard ratio for the segment (per SD for z terms).\n",
            "| term | B2 exp(β) (95% CI) | G02 exp(β) (95% CI) |", "|---|---|---|"]
    se = {m: wald_se(fits[m]) for m in MODELS}
    for nm in names["G02"][1:]:
        cells = []
        for m in MODELS:
            if nm in names[m]:
                i = names[m].index(nm)
                b, s = fits[m]["beta"][i], se[m][i]
                cells.append(f"{np.exp(b):.2f} ({np.exp(b - 1.96 * s):.2f} to {np.exp(b + 1.96 * s):.2f})")
            else:
                cells.append("")
        rep.append(f"| {nm} | " + " | ".join(cells) + " |")
    rep.append("| person SD s | " + " | ".join(
        f"{fits[m]['sigma']:.2f} ({np.exp(fits[m]['theta'][-1] - 1.96 * se[m][-1]):.2f} to "
        f"{np.exp(fits[m]['theta'][-1] + 1.96 * se[m][-1]):.2f})" for m in MODELS) + " |")
    rep += ["", "| model | log-likelihood | converged |", "|---|---|---|"]
    rep += [f"| {m} | {fits[m]['ll']:.2f} | {fits[m]['ok']} ({fits[m]['msg']}) |" for m in MODELS]
    rep += [f"\n**Geometry block (G02 vs B2): LR = {lr:.2f}, df = {df_geo}, p = {p_lr:.3g}.** The prespecified test. "
            "s on its lower bound means no detectable clustering; then the product of segment risks is correct.\n"]
    if checks:
        rep += ["### Quadrature checks\n",
                f"Tolerances set before running: β {NODE_TOL['beta']}, s {NODE_TOL['sigma']}, log-lik {NODE_TOL['ll']}, "
                f"person risk {RISK_TOL}.\n",
                "| model | nodes | max Δβ | Δs | Δ log-lik | person risk 40 vs 200 nodes | |", "|---|---|---|---|---|---|---|",
                *checks, ""]

    rep += ["## Cross-validated person metrics\n",
            f"{args.folds} person folds stratified on the person outcome, {args.repeats} repeats; mean (2.5th to 97.5th "
            "percentile over repeats). Δ = G02 − B2 on the same folds: an estimate, not a test. "
            f"Fold fits that did not report convergence: B2 {fails['B2']}, G02 {fails['G02']} of "
            f"{args.repeats * args.folds} each.\n",
            "| metric | B2 | G02 | Δ (G02 − B2) |", "|---|---|---|---|"]
    for key in rep_metrics[0]["B2"]:
        v = {m: [r[m][key] for r in rep_metrics] for m in MODELS}
        rep.append(f"| {key} | {fmt_ci(v['B2'])} | {fmt_ci(v['G02'])} | "
                   f"{fmt_ci(np.subtract(v['G02'], v['B2']))} |")

    # ---- per segment, confusion matrices, figures
    oof0, seg0, thr0 = first
    def n_lab(yv):
        return f"{count(int(yv.sum()))}/{count(len(yv))}"
    auc_rows = [("person", n_lab(Yv), {m: [r[m]["C"] for r in rep_metrics] for m in MODELS})]
    auc_rows += [(s, n_lab(y[S]), {m: [r[m][s] for r in seg_auc] for m in MODELS}) for s, S in seg_rows.items()]
    panels = [("person", n_lab(Yv), Yv, oof0, {m: thr0[m]["person"] for m in MODELS})]
    panels += [(s, n_lab(y[S]), y[S], {m: seg0[m][S] for m in MODELS}, {m: thr0[m]["segment"][S] for m in MODELS})
               for s, S in seg_rows.items()]
    rep += ["\n## Per segment\n",
            "The same pooled fits, read per segment: each segment's marginal risk, integrated over the person intercept. "
            "AUC within a segment type compares people (does the model pick out who progresses in, say, the pLAD). "
            "Mean (2.5th to 97.5th percentile over repeats); ΔAUC is an estimate, not a test. With 9 segments, some "
            "intervals will exclude 0 by chance.\n",
            "| level | progressed / rows | AUC B2 | AUC G02 | ΔAUC (G02 − B2) |", "|---|---|---|---|---|"]
    for lab, n, a in auc_rows:
        rep.append(f"| {lab} | {n} | {fmt_ci(a['B2'])} | {fmt_ci(a['G02'])} | {fmt_ci(np.subtract(a['G02'], a['B2']))} |")
    for s, (n, k) in seg_left_out.items():
        rep.append(f"| {s} | {count(k)}/{count(n)} | fewer than {MIN_CELL} progressed or stable: not scored | | |")
    rep += ["\n## Confusion matrices\n",
            "Test folds of repeat 0 (every person predicted once). Cut-off: Youden's J on the training fold's own "
            "predictions (persons; each segment on its own training rows). B2 and G02 side by side. sens / spec are "
            "hidden when a cell they are computed from is.\n",
            "| level | B2 TP | FN | FP | TN | sens | spec | G02 TP | FN | FP | TN | sens | spec |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for lab, _, yv, p, th in panels:
        cells = []
        for m in MODELS:
            tp, fn, fp, tn = pt.confusion(yv, p[m], th[m])
            shown = suppress([[tp, fn, fp, tn]])[0]
            ok = [isinstance(v, (int, np.integer)) for v in shown]
            cells += [*map(str, shown), f"{100 * tp / max(tp + fn, 1):.0f}%" if ok[0] and ok[1] else "hidden",
                      f"{100 * tn / max(tn + fp, 1):.0f}%" if ok[2] and ok[3] else "hidden"]
        rep.append(f"| {lab} | " + " | ".join(cells) + " |")
    fig_calibration(Yv, oof0, args.bins, out_dir)
    fig_deltas(rep_metrics, out_dir)
    fig_auc(auc_rows, out_dir)
    fig_roc(panels, out_dir)
    fig_confusion(panels, out_dir)
    rep.append(f"\nFigures: {PREFIX}_auc.png, {PREFIX}_roc.png, {PREFIX}_confusion.png, {PREFIX}_calibration.png, "
               f"{PREFIX}_deltas.png.\n")
    Path(args.out).write_text("\n".join(rep))
    print("\n".join(rep))


if __name__ == "__main__":
    main()
