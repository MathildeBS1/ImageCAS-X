"""One model per trunk segment: does geometry add to the base in predicting progression of that segment?

    python progression_segment_models.py [--src TREE_FOLDER] [--outer 5] [--inner 4] [--boot 1000]

Rows: the 9 split trunk segments of each Medis tree (progression_turning.build), same filter as
progression_turning.py. Outcome: higher visual grade at FU than at BL. Each segment is modelled on its own
rows only (one row per person), so there are 9 x 2 = 18 logistic models:
  base       = log follow-up + log SCORE2 + BL grade (a grade level with < 5 rows is merged into the one below);
  + geometry = base + mean T5 of the segment; pLAD and pCX also get the LM bifurcation angle.
Geometry is z-scored on the training rows (missing -> 0, the training mean).

Nested cross-validation, split by person, with the same person folds for all 18 models:
  outer 5 folds (stratified on whether the person had any progressed segment) = test sets;
  inner 4 folds of each outer training set = validation sets. They pick the ridge penalty (highest
  validation AUC) and the confusion-matrix cut-off (Youden's J on the pooled validation predictions);
  the model is then refitted on the whole outer training set and scored on the outer test fold.
Per segment, from the pooled test predictions: AUC base and + geometry, ΔAUC (bootstrap 95% CI, DeLong p),
and both confusion matrices side by side.
Aggregates only (counts 1-4 hidden); writes progression_segment_models.md and progression_segment_*.png.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

import hoe10y_qc as hq
import progression_angle as pa
import progression_turning as pt
from cgps_stats import MIN_CELL, OUT_DIR, count, suppress

PREFIX = "progression_segment"
L2_GRID = (1e-6, 0.01, 0.1, 1.0, 10.0)
ANGLE_SEGS = ("plad", "pcx")  # the segments the LM bifurcation angle can act on
GRADES = ("none", "minimal", "mild", ">=moderate")
MODELS = ("base", "+ geometry")
COLOR = {"base": pt.MODEL_COLOR["base"], "+ geometry": pt.MODEL_COLOR["mean T5"]}


# ---------------------------------------------------------------- models
def merge_grades(g):
    """Merge each BL grade level with fewer than MIN_CELL rows into the level below."""
    g = g.copy()
    for hi, lo in zip(GRADES[:0:-1], GRADES[-2::-1]):
        if 0 < (g == hi).sum() < MIN_CELL:
            g[g == hi] = lo
    return g


def geometry(d, train, seg):
    """Geometry columns (n, k) of one segment, z-scored on the training rows."""
    t = pt.zscore(d, "mean_T5", train)
    if seg not in ANGLE_SEGS:
        return t[:, None]
    a = d.loc[train, "angle"]
    return np.column_stack([t, ((d["angle"] - a.mean()) / a.std()).fillna(0).to_numpy()])


def fit_predict(d, y, tr, te, geo, seg, l2):
    Z = geometry(d, tr, seg) if geo else None
    w = pt.fit(pt.design(d[tr], None if Z is None else Z[tr]), y[tr], l2)[0]
    return pt.predict(pt.design(d[te], None if Z is None else Z[te]), w)


def youden(y, p):
    _, fpr, tpr = pt.auc(y, p)
    cuts = np.r_[np.sort(p)[::-1], -np.inf]  # p > cuts[k] calls the k highest "progresses"
    return cuts[np.argmax(tpr - fpr)]


def nested(d, y, outer, inner, geo, seg):
    """Test predictions and the validation-chosen cut-off of each test row."""
    p, thr = np.zeros(len(d)), np.zeros(len(d))
    for k in np.unique(outer):
        tr, te = outer != k, outer == k
        assert not set(d.loc[tr, "id"]) & set(d.loc[te, "id"]), "a person is in both train and test"
        val = {}
        for l2 in L2_GRID:
            pv = np.full(len(d), np.nan)
            for j in np.unique(inner[tr]):
                itr, iva = tr & (inner != j), tr & (inner == j)
                pv[iva] = fit_predict(d, y, itr, iva, geo, seg, l2)
            val[l2] = pv
        best = max(L2_GRID, key=lambda l2: pt.auc(y[tr], val[l2][tr])[0])
        thr[te] = youden(y[tr], val[best][tr])
        p[te] = fit_predict(d, y, tr, te, geo, seg, best)
    return p, thr


def delong(y, p0, p1):
    """Two-sided p for AUC(p1) - AUC(p0) on the same rows (DeLong 1988)."""
    def parts(p):
        e, ne = p[y == 1], p[y == 0]
        psi = (e[:, None] > ne[None]) + 0.5 * (e[:, None] == ne[None])
        return psi.mean(1), psi.mean(0), psi.mean()
    v1, w1, a1 = parts(p1)
    v0, w0, a0 = parts(p0)
    s10 = np.cov(np.vstack([v0, v1]))
    s01 = np.cov(np.vstack([w0, w1]))
    var = (s10[0, 0] + s10[1, 1] - 2 * s10[0, 1]) / len(v0) + (s01[0, 0] + s01[1, 1] - 2 * s01[0, 1]) / len(w0)
    return 2 * norm.sf(abs(a1 - a0) / np.sqrt(var)) if var > 0 else np.nan


def person_folds(d, k, rng):
    """{id: fold}, k folds stratified on whether the person had any progressed segment."""
    any_prog = d.groupby("id")["y"].max()
    out = {}
    for _, ids in any_prog.groupby(any_prog):
        out.update(zip(rng.permutation(ids.index), np.arange(len(ids)) % k))
    return out


# ---------------------------------------------------------------- figures
def fig_auc(res, segs, out_dir):
    plt = pt._plt()
    fig, ax = plt.subplots(figsize=(7.5, 6.2))
    pt._grid(ax, "x")
    yy = np.arange(len(segs))[::-1].astype(float)
    for y_, sg in zip(yy, segs):
        for k, m in enumerate(MODELS):
            a = res[sg]["auc"][m]
            ax.barh(y_ + (0.18 if k == 0 else -0.18), a - 0.5, left=0.5, height=0.34, color=COLOR[m],
                    label=m if sg == segs[0] else None)
            ax.text(a + 0.005, y_ + (0.18 if k == 0 else -0.18), f"{a:.2f}", va="center", fontsize=7.5, color=pt.INK2)
    ax.axvline(0.5, color=pt.MUTED, lw=1, ls=":")
    ax.set_yticks(yy, [f"{sg}  ({count(res[sg]['k'])}/{count(res[sg]['n'])})" for sg in segs])
    for lab, sg in zip(ax.get_yticklabels(), segs):
        lab.set_color({"LAD": "#2a78d6", "LCx": "#1baf7a", "RCA": "#e34948"}[pt.VESSEL[sg]])
        lab.set_fontweight("bold")
    for i in range(1, len(segs)):
        if pt.VESSEL[segs[i]] != pt.VESSEL[segs[i - 1]]:
            ax.axhline((yy[i] + yy[i - 1]) / 2, color=pt.MUTED, lw=0.8, alpha=0.6)
    ax.set_xlim(min(0.4, min(r["auc"][m] for r in res.values() for m in MODELS) - 0.05), 1.0)
    ax.set_xlabel("AUC on the test folds (0.5 = chance)")
    ax.set_title("AUC per segment: base vs base + geometry")
    ax.legend(fontsize=8, loc="lower right")
    fig.text(0.01, 0.01, "(progressed/segments). Each segment has its own model, fitted on that segment's rows only.",
             fontsize=8, color=pt.INK2)
    pt._save(fig, out_dir / f"{PREFIX}_auc.png", rect=(0, 0.03, 1, 1))


def fig_roc(res, segs, out_dir):
    plt = pt._plt()
    fig, axes = plt.subplots(3, 3, figsize=(11, 10.5), sharex=True, sharey=True)
    grid = np.linspace(0, 1, 21)  # binned so no single person is a visible step
    for ax, sg in zip(axes.ravel(), segs):
        pt._grid(ax, "both")
        ax.plot([0, 1], [0, 1], lw=1, ls=":", color=pt.MUTED)
        for m in MODELS:
            a, fpr, tpr = pt.auc(res[sg]["y"], res[sg]["p"][m])
            ax.plot(grid, [tpr[fpr <= g].max() for g in grid], lw=2.2 if m == "base" else 1.8, color=COLOR[m],
                    label=f"{m}  (AUC {a:.2f})")
        ax.set_title(f"{sg}  ({count(res[sg]['k'])}/{count(res[sg]['n'])})", fontsize=10)
        ax.legend(fontsize=7.5, loc="lower right")
        ax.set(xlim=(0, 1), ylim=(0, 1.02))
    for ax in axes.ravel()[len(segs):]:
        ax.axis("off")
    for ax in axes[-1]:
        ax.set_xlabel("1 - specificity")
    for ax in axes[:, 0]:
        ax.set_ylabel("sensitivity")
    fig.suptitle("ROC per segment on the test folds: base vs base + geometry", x=0.01, ha="left",
                 fontsize=12, fontweight="bold", color=pt.INK)
    pt._save(fig, out_dir / f"{PREFIX}_roc.png")


def fig_confusion(res, segs, out_dir):
    plt = pt._plt()
    fig, axes = plt.subplots(len(segs), 2, figsize=(6.4, 2.3 * len(segs)))
    cell_col = np.array([["#1baf7a", pt.MISSED], ["#e34948", "#1baf7a"]])  # TP, FN / FP, TN
    for row, sg in zip(axes, segs):
        for ax, m in zip(row, MODELS):
            tp, fn, fp, tn = res[sg]["cm"][m]
            M = np.array([[tp, fn], [fp, tn]])
            share = M / np.maximum(M.sum(axis=1, keepdims=True), 1)
            for (i, j), v in np.ndenumerate(suppress(M)):
                ax.add_patch(plt.Rectangle((j - 0.48, i - 0.48), 0.96, 0.96, color=cell_col[i, j],
                                           alpha=0.18 + 0.75 * share[i, j]))
                ax.text(j, i - 0.1, v, ha="center", va="center", fontsize=11, fontweight="bold", color=pt.INK)
                ax.text(j, i + 0.25, f"{100 * share[i, j]:.0f}% of row", ha="center", va="center", fontsize=6.5,
                        color=pt.INK2)
            ax.set_xlim(-0.5, 1.5); ax.set_ylim(1.5, -0.5)
            ax.set_xticks([0, 1], ["called progress", "called stable"], fontsize=7)
            ax.set_yticks([0, 1], ["progressed", "stable"], fontsize=7)
            ax.tick_params(length=0)
            for sp in ax.spines.values():
                sp.set_visible(False)
            ax.set_title(f"{sg}: {m}  (AUC {res[sg]['auc'][m]:.2f})", color=COLOR[m], fontsize=9)
    fig.suptitle("Confusion matrices per segment (test folds)", x=0.01, ha="left", fontsize=12,
                 fontweight="bold", color=pt.INK)
    fig.text(0.01, 0.003, "Cut-off: Youden's J on the validation folds. Green = correct, orange = missed progression,\n"
             "red = false alarm; darker = larger share of its row.", fontsize=7.5, color=pt.INK2)
    pt._save(fig, out_dir / f"{PREFIX}_confusion.png", rect=(0, 0.015, 1, 0.99))


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / f"{PREFIX}_models.md"))
    ap.add_argument("--outer", type=int, default=5)
    ap.add_argument("--inner", type=int, default=4)
    ap.add_argument("--boot", type=int, default=1000)
    args = ap.parse_args()
    out_dir = Path(args.out).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    d0, graded, skipped = pt.build(args.src)
    keep = graded & d0["mean_T5"].notna() & (d0["score2"] > 0) & (d0["years"] > 0)
    d = d0[keep].assign(grade=lambda x: x["bl"].map(pt.GRADE)).reset_index(drop=True)
    d["angle"] = d["id"].map(pa.angles(args.src))
    rng = np.random.default_rng(0)
    outer_of = person_folds(d, args.outer, rng)
    inner_of = {i: j for i, j in zip(rng.permutation(list(outer_of)), np.arange(len(outer_of)) % args.inner)}

    segs = [sg for sg in pt.SEG_ORDER if sg in set(d["segment"])]
    res, left_out = {}, {}
    for sg in segs:
        ds = d[d["segment"] == sg].reset_index(drop=True)
        ds["grade"] = merge_grades(ds["grade"])
        y = ds["y"].to_numpy()
        n, k = len(ds), int(y.sum())
        if min(k, n - k) < MIN_CELL:
            left_out[sg] = (n, k)
            continue
        outer, inner = ds["id"].map(outer_of).to_numpy(), ds["id"].map(inner_of).to_numpy()
        p, thr = {}, {}
        for m in MODELS:
            p[m], thr[m] = nested(ds, y, outer, inner, m != "base", sg)
        bd = []
        for _ in range(args.boot):
            bi = rng.choice(n, n)
            if 0 < y[bi].sum() < n:
                bd.append(pt.auc(y[bi], p["+ geometry"][bi])[0] - pt.auc(y[bi], p["base"][bi])[0])
        res[sg] = {"n": n, "k": k, "y": y, "p": p,
                   "auc": {m: pt.auc(y, p[m])[0] for m in MODELS},
                   "cm": {m: pt.confusion(y, p[m], thr[m]) for m in MODELS},
                   "ci": np.percentile(bd, [2.5, 97.5]), "delong": delong(y, p["base"], p["+ geometry"]),
                   "angle": sg in ANGLE_SEGS}
    fitted = [sg for sg in segs if sg in res]

    rep = ["# One model per segment: base vs base + geometry (Medis trees)\n",
           "Aggregates only; counts 1-4 shown as <5. Outcome = higher visual grade at FU than at BL. The Medis trees "
           "are almost all people with plaque at baseline: this is progression, not new plaque in a clean cohort.\n",
           f"Segments: {count(len(d))} from {count(d['id'].nunique())} people; progressed: {count(int(d['y'].sum()))}. "
           f"Left out: {count(int((~graded).sum()))} without a usable grade or occluded at BL, "
           f"{count(int((graded & ~keep).sum()))} too short for two T5 angles or without SCORE2 / follow-up. "
           f"Trees that could not be split: {count(skipped)}.\n",
           "- *Base*: log follow-up + log SCORE2 + BL grade. *+ geometry*: base + mean T5 of the segment; pLAD and pCX "
           "also get the LM bifurcation angle.",
           f"- Each segment has its own two models, fitted on that segment's rows only. Nested cross-validation split by "
           f"person: {args.outer} outer folds are the test sets, {args.inner} inner folds of each training set are the "
           "validation sets (ridge penalty and cut-off). The same person folds are used in all models.",
           "- AUC and confusion matrices are from the test folds. ΔAUC is an estimate; with 9 segments, expect about "
           "one DeLong p < 0.1 by chance alone.\n",
           "## AUC per segment\n",
           "| segment | progressed / segments | geometry | AUC base | AUC + geometry | ΔAUC (95% bootstrap) | DeLong p |",
           "|---|---|---|---|---|---|---|"]
    for sg in segs:
        if sg in left_out:
            n, k = left_out[sg]
            rep.append(f"| {sg} | {count(k)} / {count(n)} | fewer than {MIN_CELL} progressed or stable: not fitted | | | | |")
            continue
        r = res[sg]
        a0, a1 = r["auc"]["base"], r["auc"]["+ geometry"]
        rep.append(f"| {sg} | {count(r['k'])} / {count(r['n'])} | {'T5 + LM angle' if r['angle'] else 'T5'} | "
                   f"{a0:.3f} | {a1:.3f} | {a1 - a0:+.3f} ({r['ci'][0]:+.3f} to {r['ci'][1]:+.3f}) | {r['delong']:.3g} |")
    rep += ["\n## Confusion matrices per segment\n",
            "Cut-off: Youden's J on the validation folds. Base and + geometry side by side.\n",
            "| segment | base TP | FN | FP | TN | sens | spec | + geometry TP | FN | FP | TN | sens | spec |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for sg in fitted:
        cells = []
        for m in MODELS:
            tp, fn, fp, tn = res[sg]["cm"][m]
            cells += [*map(str, suppress([[tp, fn, fp, tn]])[0]),
                      f"{100 * tp / max(tp + fn, 1):.0f}%", f"{100 * tn / max(tn + fp, 1):.0f}%"]
        rep.append(f"| {sg} | " + " | ".join(cells) + " |")
    if fitted:
        fig_auc(res, fitted, out_dir)
        fig_roc(res, fitted, out_dir)
        fig_confusion(res, fitted, out_dir)
        rep.append(f"\nFigures: {PREFIX}_auc.png, {PREFIX}_roc.png, {PREFIX}_confusion.png.\n")
    Path(args.out).write_text("\n".join(rep))
    print("\n".join(rep))


if __name__ == "__main__":
    main()
