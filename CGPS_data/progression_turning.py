"""Does a segment's mean turning angle add to SCORE2 and follow-up time in predicting whether that
segment progresses from BL to FU, comparing people at the same segment position?

    python progression_turning.py [--src TREE_FOLDER] [--folds 10] [--boot 500]

Rows: the 9 split trunk segments of each Medis tree (split_trunks.py) with a visual grade at BL and FU;
occluded-at-BL segments are dropped. Outcome: higher grade at FU (none -> minimal counts).
- Base model: segment position + BL grade (none / minimal / mild / >= moderate) + log SCORE2 + log follow-up.
- Full model: base + mean turning angle T5 of the segment (5 mm chords, rad/mm, thesis Section 5.1.1),
  z-scored within segment position. T5 is computed along the whole trunk and averaged inside each segment.
Reported (aggregates only): OR per SD of turning, LR test and person-cluster robust Wald test, and the
cross-validated position-stratified C of both models (pairs of different people at the same position)
with ΔC and a person-bootstrap interval of the out-of-fold predictions (fixed folds: slightly narrow).
Also, on the out-of-fold predictions: confusion matrix (a segment is called "progresses" when its risk is
above the progression rate of its training folds), ROC curve (progression_turning_roc.png, binned), and
which kinds of progression were caught or missed (new plaque vs growth, size of the jump, BL grade,
position).
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, norm

import hoe10y_qc as hq
from cgps_stats import OUT_DIR, count, num, suppress
from split_trunks import NAMES, graph, split

try:
    from tortuosity.curvature import chord_resample, turning_angles
except ImportError:  # flat copy on the server: curvature.py next to this file
    from curvature import chord_resample, turning_angles

CHORD = 5.0
GRADE = {"none": "none", "minimal": "minimal", "mild": "mild", "moderate": ">=moderate", "severe": ">=moderate"}


def segment_turning(Y, s, cuts):
    """Mean turning per mm of each segment, from the whole-trunk T5 profile."""
    V = chord_resample(Y, CHORD)
    theta = turning_angles(V) / CHORD
    pos = s[np.argmin(np.linalg.norm(Y[None] - V[1:-1, None], axis=2), axis=1)]  # arc length of each angle
    return [theta[(pos >= lo) & (pos < hi)].mean() if ((pos >= lo) & (pos < hi)).sum() >= 2 else np.nan
            for lo, hi in zip((0, *cuts[:2]), cuts)]


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
            for seg, t in zip(NAMES[a], segment_turning(Y, s, (pm, md, end))):
                g = [hq.grade_of(d.at[pid, f"ct_cag_{seg}_stenosis"]) if pid in d.index else "missing" for d in (bl, fu)]
                rows.append({"id": pid, "segment": seg, "turning": t, "bl": g[0], "fu": g[1],
                             "score2": score2.get(pid, np.nan), "years": years.get(pid, np.nan)})
    d = pd.DataFrame(rows)
    rank = {g: i for i, g in enumerate(hq.GRADES)}
    d["y"] = (d["fu"].map(rank) > d["bl"].map(rank)).astype(float)
    return d, d["bl"].isin(GRADE) & d["fu"].isin(rank)


def design(d, z):
    X = [np.ones(len(d)), np.log(d["score2"]), np.log(d["years"])]
    X += [(d["segment"] == sg).to_numpy(float) for sg in sorted(d["segment"].unique())[1:]]
    X += [(d["grade"] == g).to_numpy(float) for g in ("minimal", "mild", ">=moderate")]
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
    p = 1 / (1 + np.exp(-X @ w))
    return w, p, np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)), H


def zscore(d, train):
    m, sd = d[train].groupby("segment")["turning"].mean(), d[train].groupby("segment")["turning"].std()
    return ((d["turning"] - d["segment"].map(m)) / d["segment"].map(sd).replace(0, np.nan)).fillna(0).to_numpy()


def strat_c(d, p):
    """Concordance over pairs of different people at the same segment position."""
    num_, den = 0.0, 0
    for _, g in d.assign(p=p).groupby("segment"):
        e, ne = g.p[g.y == 1].to_numpy(), g.p[g.y == 0].to_numpy()
        if len(e) and len(ne):
            diff = e[:, None] - ne[None]
            num_ += (diff > 0).sum() + 0.5 * (diff == 0).sum()
            den += diff.size
    return num_ / den if den else np.nan


def errors(d, y, p_base, p_full, thr):
    """Confusion matrices of both models and what the full model got wrong."""
    pct = lambda k, n: f"{100 * k / n:.0f}%" if n >= 5 else ""
    rep = ["## Confusion matrix (out-of-fold, threshold = training progression rate)\n",
           "| model | TP | FN | FP | TN | sensitivity | specificity | PPV | NPV |", "|---|---|---|---|---|---|---|---|---|"]
    for name, p in (("base", p_base), ("+ turning", p_full)):
        c = p > thr
        tp, fn, fp, tn = (int(x) for x in ((c & (y == 1)).sum(), (~c & (y == 1)).sum(), (c & (y == 0)).sum(), (~c & (y == 0)).sum()))
        rep.append(f"| {name} | {count(tp)} | {count(fn)} | {count(fp)} | {count(tn)} | {pct(tp, tp + fn)} | "
                   f"{pct(tn, tn + fp)} | {pct(tp, tp + fp)} | {pct(tn, tn + fn)} |")
    rank = {g: i for i, g in enumerate(hq.GRADES)}
    e = d.assign(call=p_full > thr, jump=d["fu"].map(rank) - d["bl"].map(rank))
    e["kind"] = np.where(e["bl"] == "none", "new plaque", "growth of existing plaque")
    e["size"] = np.where(e["jump"] >= 2, ">= 2 grades", "1 grade")

    def tab(title, rows, by, col):
        out = [f"\n{title}\n", f"| {by} | n | {col[0]} | {col[1]} | rate |", "|---|---|---|---|---|"]
        for k, g in rows.groupby(by):
            hit = int(g["call"].sum()) if col[0] == "caught" else int((~g["call"]).sum())
            a, b = suppress([[hit, len(g) - hit]])[0]  # a hidden count cannot be worked out from n
            rate = pct(hit, len(g)) if not isinstance(a, str) and not isinstance(b, str) else ""
            out.append(f"| {k} | {count(len(g))} | {a} | {b} | {rate} |")
        return out

    prog, stay = e[e.y == 1], e[e.y == 0]
    rep += ["\n## What the + turning model got wrong (out-of-fold)"]
    rep += tab("Progressed segments by kind (missed = false negatives):", prog, "kind", ("caught", "missed"))
    rep += tab("Progressed segments by size of the jump:", prog, "size", ("caught", "missed"))
    rep += tab("Progressed segments by position:", prog, "segment", ("caught", "missed"))
    rep += tab("Segments that did not progress, by BL grade (false alarm = false positives):", stay, "bl",
               ("correct", "false alarm"))
    rep += tab("Segments that did not progress, by position:", stay, "segment", ("correct", "false alarm"))
    return rep + [""]


def roc_figure(y, p_base, p_full, path):
    """Pooled ROC, binned to a fixed false-positive-rate grid so no single segment is a step."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    grid = np.linspace(0, 1, 21)
    fig, ax = plt.subplots(figsize=(4.6, 4.4))
    for name, p, col in (("SCORE2 + time + position + BL grade", p_base, "#8a8984"), ("+ mean turning angle", p_full, "#2a6fdb")):
        order = np.argsort(-p)
        tpr = np.r_[0, np.cumsum(y[order] == 1) / max((y == 1).sum(), 1)]
        fpr = np.r_[0, np.cumsum(y[order] == 0) / max((y == 0).sum(), 1)]
        t = [tpr[fpr <= g].max() for g in grid]
        auc = float(np.sum(np.diff(fpr) * (tpr[1:] + tpr[:-1]) / 2))
        ax.plot(grid, t, lw=2, color=col, label=f"{name} (AUC {auc:.2f})")
    ax.plot([0, 1], [0, 1], lw=1, ls="--", color="#c8c7c2")
    ax.set_xlabel("False positive rate (1 - specificity)")
    ax.set_ylabel("True positive rate (sensitivity)")
    ax.set_title("Segment progression, out-of-fold", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=8, frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / "progression_turning.md"))
    ap.add_argument("--folds", type=int, default=10)
    ap.add_argument("--boot", type=int, default=500)
    args = ap.parse_args()
    d0, graded = build(args.src)
    keep = graded & d0["turning"].notna() & (d0["score2"] > 0) & (d0["years"] > 0)
    d = d0[keep].assign(grade=lambda x: x["bl"].map(GRADE)).reset_index(drop=True)
    y = d["y"].to_numpy()

    # full-data fit: test and effect size
    z = zscore(d, np.ones(len(d), bool))
    _, _, ll0, _ = fit(design(d, None), y)
    w1, p1, ll1, H = fit(design(d, z), y)
    X1 = design(d, z)
    U = pd.DataFrame(X1 * (y - p1)[:, None]).groupby(d["id"].to_numpy()).sum().to_numpy()
    V = np.linalg.inv(H) @ (U.T @ U) @ np.linalg.inv(H)  # person-cluster robust covariance
    b, se = w1[-1], np.sqrt(V[-1, -1])
    lr = 2 * (ll1 - ll0)

    # person-split cross-validation, then a person bootstrap of the out-of-fold predictions
    rng = np.random.default_rng(0)
    people = d["id"].unique()
    fold = dict(zip(rng.permutation(people), np.arange(len(people)) % args.folds))
    f = d["id"].map(fold).to_numpy()
    p_base, p_full, thr = np.zeros(len(d)), np.zeros(len(d)), np.zeros(len(d))
    for k in range(args.folds):
        tr, te = f != k, f == k
        zk = zscore(d, tr)
        thr[te] = y[tr].mean()  # call "progresses" above the training progression rate
        p_base[te] = 1 / (1 + np.exp(-design(d[te], None) @ fit(design(d[tr], None), y[tr])[0]))
        p_full[te] = 1 / (1 + np.exp(-design(d[te], zk[te]) @ fit(design(d[tr], zk[tr]), y[tr])[0]))
    c0, c1 = strat_c(d, p_base), strat_c(d, p_full)
    rows_of = d.groupby("id").indices
    boot = []
    for _ in range(args.boot):
        idx = np.concatenate([rows_of[i] for i in rng.choice(people, len(people))])
        db = d.iloc[idx].reset_index(drop=True)
        boot.append(strat_c(db, p_full[idx]) - strat_c(db, p_base[idx]))
    lo, hi = np.nanpercentile(boot, [2.5, 97.5])

    per_seg = d.groupby("segment")["y"].agg(["size", "sum"]).reindex([s for v in NAMES.values() for s in v])
    rep = ["# Does segment turning add to SCORE2 + follow-up time for progression?\n",
           "Aggregates only; counts 1-4 shown as <5. Medis trees, split by split_trunks.py; "
           "outcome = higher visual grade at FU.\n",
           f"Segments analysed: {count(len(d))} from {count(d['id'].nunique())} people; progressed: {count(int(y.sum()))}. "
           f"Left out: {count(int((~graded).sum()))} without a usable BL/FU grade or occluded at BL, "
           f"{count(int((graded & ~keep).sum()))} without turning, SCORE2 or follow-up time.\n",
           "| segment | segments | progressed |", "|---|---|---|",
           *[f"| {s} | {count(r['size'])} | {count(r['sum'])} |" for s, r in per_seg.dropna().iterrows()], "",
           "## Effect of turning (full data)\n",
           f"- OR per SD of turning (within position): **{np.exp(b):.2f}** "
           f"(95% CI {np.exp(b - 1.96 * se):.2f}–{np.exp(b + 1.96 * se):.2f}, person-cluster robust)",
           f"- Likelihood-ratio test, 1 df: χ² = {lr:.2f}, p = {chi2.sf(lr, 1):.3g} (assumes independent segments)",
           f"- Robust Wald test: p = {2 * norm.sf(abs(b / se)):.3g} (accounts for segments within a person)\n",
           "## Prediction (person-split cross-validation)\n",
           f"Position-stratified C (pairs of different people at the same position), {args.folds} folds:\n",
           "| model | C |", "|---|---|",
           f"| SCORE2 + follow-up + position + BL grade | {c0:.3f} |", f"| + mean turning angle | {c1:.3f} |",
           f"| ΔC | {c1 - c0:+.3f} (95% {lo:+.3f} to {hi:+.3f}, person bootstrap, {args.boot} replicates) |", "",
           "Read the test, not ΔC, as the evidence: ΔC is an estimate. Medis trees are mostly patients with "
           "plaque at baseline, so this is about progression, not new plaque in a clean cohort.\n"]
    rep += errors(d, y, p_base, p_full, thr)
    roc_figure(y, p_base, p_full, Path(args.out).with_name("progression_turning_roc.png"))
    rep.append("ROC curve: progression_turning_roc.png (all segments pooled, binned at 0.05 false-positive rate).\n")
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(rep), encoding="utf-8")
    print("\n".join(rep))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
