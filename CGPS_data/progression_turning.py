"""Does segment turning predict plaque progression (BL -> FU visual grade) in the Medis trees?

    python progression_turning.py [--src TREE_FOLDER] [--folds 10] [--boot 200]

Rows: the 9 split trunk segments of each Medis tree (split_trunks.py) with a visual grade at BL and FU;
occluded-at-BL segments are dropped. Outcome: higher grade at FU (none -> minimal counts).
Turning comes from the whole-trunk turning-angle profile (thesis Section 5.1.1, chord l mm, rad/mm).

Six geometry variants, each added on its own to the same base model and z-scored within position
in the training folds (missing -> 0, the position mean):
  mean T5, 90th percentile of T5 (sharpest bend), fraction of the segment above the cohort 75th
  percentile of T5, mean T2.5, mean T10, mean T5 over the 20 mm upstream of the segment.

1. Between people (logistic): base = position + BL grade + log SCORE2 + log follow-up.
   Per variant: OR per SD, robust p, out-of-fold position-stratified C and ΔC (person bootstrap),
   pooled AUC, confusion matrix (call "progresses" above the training-fold progression rate).
   Figures: progression_roc.png, progression_confusion.png.
2. Within person (conditional logistic, stratified on person): base = position + BL grade + log length.
   Per variant: out-of-fold within-person C, ΔC, top-1 hit rate (the person's highest-ranked segment
   progressed), and how often geometry changes the top-ranked segment and whether the new one progressed.
3. Reclassification: position + follow-up vs + mean T5. Segments whose risk geometry raised most
   (top 10% of the out-of-fold risk change) or lowered most (bottom 10%): did they progress?
Aggregates only (counts 1-4 hidden, also when they could be worked out); writes progression_turning.md.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import chi2, norm

import hoe10y_qc as hq
from cgps_stats import OUT_DIR, count, num, suppress
from split_trunks import NAMES, graph, split

try:
    from tortuosity.curvature import chord_resample, turning_angles
except ImportError:  # flat copy on the server: curvature.py next to this file
    from curvature import chord_resample, turning_angles

GRADE = {"none": "none", "minimal": "minimal", "mild": "mild", "moderate": ">=moderate", "severe": ">=moderate"}
VARIANTS = {"mean_T5": "mean T5", "p90_T5": "90th pct T5", "frac_T5": "fraction above p75",
            "mean_T2.5": "mean T2.5", "mean_T10": "mean T10", "up_T5": "upstream 20 mm T5"}
UPSTREAM = 20.0


# ---------------------------------------------------------------- features
def profile(Y, s, chord):
    V = chord_resample(Y, chord)
    if len(V) < 3:
        return np.zeros(0), np.zeros(0)
    pos = s[np.argmin(np.linalg.norm(Y[None] - V[1:-1, None], axis=2), axis=1)]
    return pos, turning_angles(V) / chord


def segment_features(Y, s, cuts):
    prof = {c: profile(Y, s, c) for c in (2.5, 5.0, 10.0)}
    rows = []
    for lo, hi in zip((0, *cuts[:2]), cuts):
        f = {"length": hi - lo}
        for c, (pos, th) in prof.items():
            seg = th[(pos >= lo) & (pos < hi)]
            f[f"mean_T{c:g}"] = seg.mean() if len(seg) >= 2 else np.nan
            if c == 5.0:
                f["p90_T5"] = np.percentile(seg, 90) if len(seg) >= 2 else np.nan
                f["t5_values"] = seg
                up = th[(pos >= lo - UPSTREAM) & (pos < lo)]
                f["up_T5"] = up.mean() if len(up) >= 2 else np.nan
        rows.append(f)
    return rows


def build(src):
    sheets = hq.load_sheets(hq.ROOT)
    bl, fu = (sheets[v].assign(id=sheets[v]["study_id"].map(hq.norm_id)).drop_duplicates("id").set_index("id")
              for v in ("BL", "FU"))
    score2 = num(bl["score2"]).fillna(num(bl["score2_op"])) if "score2_op" in bl else num(bl["score2"])
    years = (pd.to_datetime(fu["scandate"], errors="coerce").reindex(bl.index)
             - pd.to_datetime(bl["scandate"], errors="coerce")).dt.days / 365.25
    rows = []
    for f in sorted(Path(src).rglob("*.vtk")):
        pid = hq.id_from_name(f.name)
        try:
            res = split(*graph(hq.tree_points(f)))
        except Exception:  # noqa: BLE001 - tree skipped
            continue
        for a, (pm, md, end, _, Y, s) in res.items():
            for seg, feat in zip(NAMES[a], segment_features(Y, s, (pm, md, end))):
                g = [hq.grade_of(d.at[pid, f"ct_cag_{seg}_stenosis"]) if pid in d.index else "missing" for d in (bl, fu)]
                rows.append({"id": pid, "segment": seg, "bl": g[0], "fu": g[1], **feat,
                             "score2": score2.get(pid, np.nan), "years": years.get(pid, np.nan)})
    d = pd.DataFrame(rows)
    thr = np.percentile(np.concatenate([v for v in d["t5_values"] if len(v)]), 75)  # outcome-free threshold
    d["frac_T5"] = [np.mean(v > thr) if len(v) >= 2 else np.nan for v in d["t5_values"]]
    rank = {g: i for i, g in enumerate(hq.GRADES)}
    d["y"] = (d["fu"].map(rank) > d["bl"].map(rank)).astype(float)
    return d.drop(columns="t5_values"), d["bl"].isin(GRADE) & d["fu"].isin(rank)


# ---------------------------------------------------------------- models
def zscore(d, col, train):
    m, sd = d[train].groupby("segment")[col].mean(), d[train].groupby("segment")[col].std()
    return ((d[col] - d["segment"].map(m)) / d["segment"].map(sd).replace(0, np.nan)).fillna(0).to_numpy()


def dummies(d, col, levels):
    return [(d[col] == v).to_numpy(float) for v in levels]


def design(d, z=None, person=True, grade=True):
    """Between-person design. person: log SCORE2 + log follow-up; else only log follow-up."""
    segs = sorted(d["segment"].unique())
    X = [np.ones(len(d)), np.log(d["years"])] + ([np.log(d["score2"])] if person else [])
    X += dummies(d, "segment", segs[1:]) + (dummies(d, "grade", ("minimal", "mild", ">=moderate")) if grade else [])
    return np.column_stack(X + ([z] if z is not None else []))


def fit(X, y, l2=1e-6):
    w = np.zeros(X.shape[1])
    for _ in range(100):
        p = 1 / (1 + np.exp(-np.clip(X @ w, -30, 30)))
        H = X.T @ (X * (p * (1 - p))[:, None]) + l2 * np.eye(len(w))
        step = np.linalg.solve(H, X.T @ (y - p) - l2 * w)
        w += step
        if np.abs(step).max() < 1e-9:
            break
    p = 1 / (1 + np.exp(-np.clip(X @ w, -30, 30)))
    return w, p, np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)), H


def predict(X, w):
    return 1 / (1 + np.exp(-np.clip(X @ w, -30, 30)))


def within_design(d, z=None):
    """Within-person design: no intercept, person terms cancel."""
    X = dummies(d, "segment", sorted(d["segment"].unique())[1:]) + dummies(d, "grade", ("minimal", "mild", ">=moderate"))
    X += [np.log(d["length"].clip(lower=1.0))]
    return np.column_stack(X + ([z] if z is not None else []))


def clogit(X, y, groups, l2=1e-4):
    """Exact conditional logistic regression (strata = persons with some but not all segments progressed)."""
    strata = [np.where(groups == g)[0] for g in np.unique(groups)]
    strata = [i for i in strata if 0 < y[i].sum() < len(i)]

    def nll(b):
        total = l2 * b @ b
        for i in strata:
            eta, k = X[i] @ b, int(y[i].sum())
            E = np.full(k + 1, -np.inf); E[0] = 0.0  # log elementary symmetric polynomials
            for e in eta:
                E[1:] = np.logaddexp(E[1:], E[:-1] + e)
            total -= eta[y[i] == 1].sum() - E[k]
        return total
    r = minimize(nll, np.zeros(X.shape[1]), method="BFGS")
    return r.x, -r.fun


def strat_c(d, p, by):
    """Concordance over (progressed, not progressed) pairs within each group of `by`."""
    num_, den = 0.0, 0
    for _, g in d.assign(p=p).groupby(by):
        e, ne = g.p[g.y == 1].to_numpy(), g.p[g.y == 0].to_numpy()
        if len(e) and len(ne):
            diff = e[:, None] - ne[None]
            num_ += (diff > 0).sum() + 0.5 * (diff == 0).sum()
            den += diff.size
    return num_ / den if den else np.nan


def auc(y, p):
    order = np.argsort(-p)
    tpr = np.r_[0, np.cumsum(y[order] == 1) / max((y == 1).sum(), 1)]
    fpr = np.r_[0, np.cumsum(y[order] == 0) / max((y == 0).sum(), 1)]
    return float(np.sum(np.diff(fpr) * (tpr[1:] + tpr[:-1]) / 2)), fpr, tpr


def boot_delta(d, p0, p1, by, B, rng):
    rows_of, people = d.groupby("id").indices, d["id"].unique()
    out = []
    for _ in range(B):
        idx = np.concatenate([rows_of[i] for i in rng.choice(people, len(people))])
        db = d.iloc[idx].reset_index(drop=True)
        out.append(strat_c(db, p1[idx], by) - strat_c(db, p0[idx], by))
    return np.nanpercentile(out, [2.5, 97.5])


def confusion(y, p, thr):
    c = p > thr
    return [int(x) for x in ((c & (y == 1)).sum(), (~c & (y == 1)).sum(), (c & (y == 0)).sum(), (~c & (y == 0)).sum())]


# ---------------------------------------------------------------- figures
COLORS = ["#8a8984", "#2a6fdb", "#eb6834", "#1baf7a", "#6250d6", "#eda100", "#e87ba4"]


def plots(y, preds, conf, out_dir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    grid = np.linspace(0, 1, 21)  # binned so no single segment is a visible step
    fig, ax = plt.subplots(figsize=(5.2, 4.8))
    for (name, p), col in zip(preds.items(), COLORS):
        a, fpr, tpr = auc(y, p)
        ax.plot(grid, [tpr[fpr <= g].max() for g in grid], lw=2 if name == "base" else 1.5, color=col,
                label=f"{name} (AUC {a:.2f})")
    ax.plot([0, 1], [0, 1], lw=1, ls="--", color="#c8c7c2")
    ax.set(xlabel="False positive rate (1 - specificity)", ylabel="True positive rate (sensitivity)")
    ax.set_title("Segment progression, out-of-fold, between people", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=7, frameon=False, loc="lower right")
    fig.tight_layout(); fig.savefig(out_dir / "progression_roc.png", dpi=150); plt.close(fig)

    fig, axes = plt.subplots(2, 4, figsize=(11, 5.6))
    for ax, (name, (tp, fn, fp, tn)) in zip(axes.ravel(), conf.items()):
        m = np.array([[tp, fn], [fp, tn]])
        shown = suppress(m)
        ax.imshow(m / m.sum(axis=1, keepdims=True), cmap="Blues", vmin=0, vmax=1)
        for (i, j), v in np.ndenumerate(shown):
            ax.text(j, i, v, ha="center", va="center", fontsize=10,
                    color="white" if m[i, j] / m[i].sum() > 0.6 else "#0b0b0b")
        ax.set_xticks([0, 1], ["called progress", "called stable"], fontsize=7)
        ax.set_yticks([0, 1], ["progressed", "stable"], fontsize=7)
        ax.set_title(name, fontsize=9)
    for ax in axes.ravel()[len(conf):]:
        ax.axis("off")
    fig.suptitle("Confusion matrices (out-of-fold; shade = row share)", fontsize=10)
    fig.tight_layout(); fig.savefig(out_dir / "progression_confusion.png", dpi=150); plt.close(fig)


def extra_plots(W, R, n_inf, out_dir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, base_col, geo_col = "#0b0b0b", "#8a8984", "#2a6fdb"
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.2), sharey=True, gridspec_kw={"width_ratios": [1, 1.5]})
    yy = np.arange(len(W))[::-1]
    cols = [base_col] + [geo_col] * (len(W) - 1)
    for ax, key, title, ref in ((axes[0], "C", "Within-person C (0.5 = coin flip)", 0.5),
                                (axes[1], "hit", "Top-ranked segment progressed", None)):
        vals = W[key].to_numpy() * (100 if key == "hit" else 1)
        ax.barh(yy, vals, color=cols, height=0.6)
        ax.axvline(vals[0], color=base_col, lw=1, ls="--")
        if ref is not None:
            ax.axvline(ref, color="#c8c7c2", lw=1)
        notes = [""] + [f"   top changed in {count(r.changed)}: new {count(r.new_ok)} vs old {count(r.old_ok)} progressed"
                        for r in W.iloc[1:].itertuples()]
        for y_, v, note in zip(yy, vals, notes):
            ax.text(v, y_, (f" {v:.2f}" if key == "C" else f" {v:.0f}%" + note), va="center", fontsize=8, color=ink)
        if key == "hit":
            ax.set_xlim(0, 175)
            ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_title(title, fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_yticks(yy, W["model"])
    axes[1].set_xlabel(f"% of {count(n_inf)} people with some but not all segments progressed")
    fig.suptitle("Within one person: does geometry rank the progressing segments first? (grey = base, dashed = base level)",
                 fontsize=10)
    fig.tight_layout(); fig.savefig(out_dir / "progression_within.png", dpi=150); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.2))
    x = np.arange(len(R))
    for off, key, col, lab in ((-0.27, "pt", base_col, "expected: position + time"),
                               (0, "ptg", geo_col, "expected: + mean T5"), (0.27, "obs", ink, "observed")):
        ax.bar(x + off, 100 * R[key], width=0.25, color=col, label=lab)
        for xi, v in zip(x + off, 100 * R[key]):
            ax.text(xi, v, f"{v:.0f}%", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(x, [f"{g}\n(n = {count(n)})" for g, n in zip(R["group"], R["n"])], fontsize=8)
    ax.set_ylabel("segments that progressed (%)")
    ax.set_title("When geometry changes a segment's risk, does the segment do what geometry says?", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=8, frameon=False)
    fig.tight_layout(); fig.savefig(out_dir / "progression_reclass.png", dpi=150); plt.close(fig)


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / "progression_turning.md"))
    ap.add_argument("--folds", type=int, default=10)
    ap.add_argument("--boot", type=int, default=200)
    args = ap.parse_args()
    out_dir = Path(args.out).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    d0, graded = build(args.src)
    keep = graded & d0["mean_T5"].notna() & (d0["score2"] > 0) & (d0["years"] > 0)
    d = d0[keep].assign(grade=lambda x: x["bl"].map(GRADE)).reset_index(drop=True)
    y = d["y"].to_numpy()
    rng = np.random.default_rng(0)
    people = d["id"].unique()
    fold = d["id"].map(dict(zip(rng.permutation(people), np.arange(len(people)) % args.folds))).to_numpy()
    rep = ["# Segment turning and plaque progression (Medis trees)\n",
           "Aggregates only; counts 1-4 shown as <5. Outcome = higher visual grade at FU. Medis trees are mostly "
           "patients with plaque at baseline: this is progression, not new plaque in a clean cohort.\n",
           f"Segments: {count(len(d))} from {count(d['id'].nunique())} people; progressed: {count(int(y.sum()))}. "
           f"Left out: {count(int((~graded).sum()))} without a usable grade or occluded at BL, "
           f"{count(int((graded & ~keep).sum()))} too short for two T5 angles or without SCORE2 / follow-up.\n"]

    # 1. between people
    def cv(z_col, person=True, grade=True):
        p, thr = np.zeros(len(d)), np.zeros(len(d))
        for k in range(args.folds):
            tr, te = fold != k, fold == k
            z = zscore(d, z_col, tr) if z_col else None
            w = fit(design(d[tr], None if z is None else z[tr], person, grade), y[tr])[0]
            p[te] = predict(design(d[te], None if z is None else z[te], person, grade), w)
            thr[te] = y[tr].mean()
        return p, thr

    p_base, thr = cv(None)
    preds, conf = {"base": p_base}, {"base": confusion(y, p_base, thr)}
    c_base = strat_c(d, p_base, "segment")
    rows = []
    _, _, ll0, _ = fit(design(d), y)
    for col, name in VARIANTS.items():
        z = zscore(d, col, np.ones(len(d), bool))
        X = design(d, z)
        w, p_fit, ll1, H = fit(X, y)
        U = pd.DataFrame(X * (y - p_fit)[:, None]).groupby(d["id"].to_numpy()).sum().to_numpy()
        se = np.sqrt((np.linalg.inv(H) @ (U.T @ U) @ np.linalg.inv(H))[-1, -1])
        p_cv, _ = cv(col)
        preds[name], conf[name] = p_cv, confusion(y, p_cv, thr)
        c1 = strat_c(d, p_cv, "segment")
        lo, hi = boot_delta(d, p_base, p_cv, "segment", args.boot, rng)
        rows.append(f"| {name} | {np.exp(w[-1]):.2f} ({np.exp(w[-1] - 1.96 * se):.2f}–{np.exp(w[-1] + 1.96 * se):.2f}) | "
                    f"{2 * norm.sf(abs(w[-1] / se)):.3g} | {chi2.sf(2 * (ll1 - ll0), 1):.3g} | {c1:.3f} | "
                    f"{c1 - c_base:+.3f} ({lo:+.3f} to {hi:+.3f}) | {auc(y, p_cv)[0]:.3f} |")
    rep += ["## 1. Between people: does geometry add to SCORE2 + follow-up (+ position, BL grade)?\n",
            f"Base: position-stratified C {c_base:.3f}, pooled AUC {auc(y, p_base)[0]:.3f}. Each row adds one variant.\n",
            "| variant | OR per SD (95% CI, robust) | robust p | LR p | stratified C | ΔC (95% person bootstrap) | pooled AUC |",
            "|---|---|---|---|---|---|---|", *rows, "",
            "Stratified C = pairs of different people at the same position (the fair test); pooled AUC also rewards "
            "position. Read the robust p as the test and ΔC as an estimate. Six variants are tested: expect about "
            "one p < 0.05 in six by chance alone.\n",
            "Confusion matrices (call \"progresses\" above the training-fold progression rate):\n",
            "| model | TP | FN | FP | TN | sensitivity | specificity |", "|---|---|---|---|---|---|---|"]
    for name, (tp, fn, fp, tn) in conf.items():
        s = suppress([[tp, fn, fp, tn]])[0]
        rep.append(f"| {name} | " + " | ".join(map(str, s)) +
                   f" | {100 * tp / max(tp + fn, 1):.0f}% | {100 * tn / max(tn + fp, 1):.0f}% |")
    plots(y, preds, conf, out_dir)
    rep.append("\nFigures: progression_roc.png (all models), progression_confusion.png.\n")

    # 2. within person
    grp = d["id"].to_numpy()
    informative = d.groupby("id")["y"].agg(lambda v: 0 < v.sum() < len(v))
    n_inf = int(informative.sum())

    def cv_within(z_col):
        eta = np.zeros(len(d))
        for k in range(args.folds):
            tr, te = fold != k, fold == k
            z = zscore(d, z_col, tr) if z_col else None
            b, _ = clogit(within_design(d[tr], None if z is None else z[tr]), y[tr], grp[tr])
            eta[te] = within_design(d[te], None if z is None else z[te]) @ b
        return eta

    def top1(eta):
        top = d.assign(eta=eta).loc[lambda x: x["id"].isin(informative[informative].index)]
        return top.loc[top.groupby("id")["eta"].idxmax()].set_index("id")

    eta0 = cv_within(None)
    t0 = top1(eta0)
    c0w = strat_c(d, eta0, "id")
    _, ll_w0 = clogit(within_design(d), y, grp)
    within = [{"model": "base", "C": c0w, "hit": t0["y"].mean(), "hits": int(t0["y"].sum()), "p": np.nan,
               "changed": 0, "new_ok": 0, "old_ok": 0}]
    for col, name in VARIANTS.items():
        _, ll_w1 = clogit(within_design(d, zscore(d, col, np.ones(len(d), bool))), y, grp)
        eta1 = cv_within(col)
        t1 = top1(eta1)
        changed = t1.index[t1["segment"] != t0.loc[t1.index, "segment"]]
        within.append({"model": name, "C": strat_c(d, eta1, "id"), "hit": t1["y"].mean(), "hits": int(t1["y"].sum()), "p": chi2.sf(2 * (ll_w1 - ll_w0), 1),
                       "changed": len(changed), "new_ok": int(t1.loc[changed, "y"].sum()),
                       "old_ok": int(t0.loc[changed, "y"].sum())})
    W = pd.DataFrame(within)
    rep += ["## 2. Within one person: does geometry pick the right segment?\n",
            "**Question.** Take one person. Their segments differ in position, baseline grade and length, and in "
            "geometry. Does knowing the geometry help rank *that person's* segments, so the ones that progressed come "
            "first? SCORE2 and follow-up time are the same for all of a person's segments, so they play no role here.\n",
            f"**Who counts.** Only people with some but not all segments progressed can be ranked: {count(n_inf)} people.\n",
            "**How to read the columns.**",
            "- *within-person C*: pick one progressed and one stable segment from the same person; the share of such pairs "
            "where the model ranks the progressed one higher. 0.5 = coin flip, 1 = always right.",
            "- *top segment progressed*: share of people whose highest-ranked segment really progressed.",
            "- *top changed / new top progressed / old top progressed*: for how many people adding geometry moved a "
            "different segment to the top, and in how many of those the new top vs the old top had progressed. "
            "Geometry helps if 'new' is larger than 'old'.",
            "- *p*: does geometry improve the within-person fit (likelihood-ratio test)?\n",
            "| model | within-person C | vs base | top segment progressed | top changed | new top progressed | old top progressed | p |",
            "|---|---|---|---|---|---|---|---|"]
    for r in W.itertuples():
        base = r.model == "base"
        rep.append(f"| {r.model} | {r.C:.3f} | {'' if base else f'{r.C - c0w:+.3f}'} | {100 * r.hit:.0f}% "
                   f"({count(r.hits)} of {count(n_inf)}) | {'' if base else count(r.changed)} | "
                   f"{'' if base else count(r.new_ok)} | {'' if base else count(r.old_ok)} | {'' if base else f'{r.p:.3g}'} |")
    best = W.iloc[1:].loc[W.iloc[1:]["C"].idxmax()]
    rep.append(f"\n**In short:** position, baseline grade and length rank the right segment first for "
               f"{100 * W['hit'][0]:.0f}% of people (within-person C {c0w:.2f}). The best geometry variant "
               f"({best['model']}) gives C {best['C']:.2f} ({best['C'] - c0w:+.2f}). Figure: progression_within.png.\n")

    # 3. reclassification: position + time vs + mean T5
    p_pt, _ = cv(None, person=False, grade=False)
    p_ptg, _ = cv("mean_T5", person=False, grade=False)
    delta = p_ptg - p_pt
    q10, q90 = np.percentile(delta, [10, 90])
    groups = {"geometry raised the risk most (top 10%)": delta >= q90, "little change (middle 80%)": (delta > q10) & (delta < q90),
              "geometry lowered the risk most (bottom 10%)": delta <= q10}
    R = pd.DataFrame([{"group": g, "n": int(m.sum()), "k": int(y[m].sum()), "obs": y[m].mean(),
                       "pt": p_pt[m].mean(), "ptg": p_ptg[m].mean()} for g, m in groups.items()])
    rep += ["## 3. When geometry changes a segment's risk, is it right?\n",
            "**Question.** Predict each segment's risk twice, out-of-fold: with position + follow-up time only, and with "
            "mean T5 added. For most segments geometry barely changes the risk. Look at the 10% it pushed up most and the "
            "10% it pushed down most, and check what actually happened.\n",
            "**How to read it.** If geometry is right, segments it pushed *up* progress more often than the position + time "
            "model expected (observed above the grey bar), and segments it pushed *down* progress less often.\n",
            "| segments | n | progressed | observed | expected, position + time | expected, + geometry |",
            "|---|---|---|---|---|---|"]
    for r in R.itertuples():
        rep.append(f"| {r.group} | {count(r.n)} | {count(r.k)} | {100 * r.obs:.0f}% | {100 * r.pt:.0f}% | {100 * r.ptg:.0f}% |")
    up, down = R.iloc[0], R.iloc[2]
    verdict = ("geometry moved the risk in the right direction in both groups" if up.obs > up.pt and down.obs < down.pt
               else "geometry did not consistently move the risk in the right direction")
    rep.append(f"\n**In short:** where geometry raised the risk, {100 * up.obs:.0f}% progressed (position + time expected "
               f"{100 * up.pt:.0f}%); where it lowered the risk, {100 * down.obs:.0f}% progressed (expected "
               f"{100 * down.pt:.0f}%): {verdict}. Figure: progression_reclass.png.\n")
    extra_plots(W, R, n_inf, out_dir)

    Path(args.out).write_text("\n".join(rep), encoding="utf-8")
    print("\n".join(rep))
    print(f"wrote {args.out} and progression_*.png in {out_dir}")


if __name__ == "__main__":
    main()
