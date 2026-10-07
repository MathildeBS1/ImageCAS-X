"""Score extracted centerlines against the delivered ones, per case and side.

    python -m bifurcation.score_extraction --dir cas_net_pretrained_t3 --split test
    python -m bifurcation.score_extraction --dir cas_net_pretrained_t3 --split test --against gt_t3

Both curves are resampled to ``STEP_MM`` first, so vertex spacing (about 0.45 mm in the delivered
files) does not show up as distance. The tolerance at a delivered point is its GT lumen radius
(``radius.py``), floored at ``TOL_FLOOR_MM``; an extracted point uses the tolerance of its nearest
delivered point, never its own radius, which would reward over-segmentation.

Measures, CAT08-style (Schaap et al. 2009) where one exists:
- ``ov``: (TPR + TPM) / (TPR + TPM + FN + FP), lengths; ``ot`` the same where GT radius >= 0.75 mm;
- ``of``: mean over ostium-to-terminus paths of the covered fraction before the first miss,
  ignoring the first 5 mm;
- ``ai``: mean distance over covered and correct points only;
- ``centerline_md``/``centerline_hd95`` from ``utils.metrics.compute_centerline_point_metrics``;
- bifurcations by one-to-one Hungarian matching at 1/2/3/5 mm (3 mm primary, a deviation);
- terminal branches found / spurious by the ATM'22 rule: >= 80 % of a branch within tolerance;
- ostium distance; recall per delivered segment label, radius bin and distance from the ostium.

Failures are rows with an ``error``, never dropped. Writes ``scores_<split>.csv`` and
``summary_<split>.json`` (overall and per Descriptors.xlsx group) into the extraction folder.
"""

from __future__ import annotations

import argparse
import json

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from scipy.spatial import cKDTree
from scipy.stats import wilcoxon

from utils.metrics import compute_centerline_point_metrics

from . import graph, io, paths, radius

STEP_MM = 0.1
TOL_FLOOR_MM = 0.35
OT_RADIUS_MM = 0.75
OF_GRACE_MM = 5.0
BRANCH_COVERAGE = 0.8
BIF_GATES_MM = (1, 2, 3, 5)
RADIUS_BINS = (0, 1.0, 1.5, 2.0, np.inf)
DIST_BINS = (0, 20, 50, 100, np.inf)


def resample(points: np.ndarray, step: float = STEP_MM) -> tuple[np.ndarray, np.ndarray]:
    """Points every ``step`` mm along a polyline, and the index of the nearer original vertex."""
    seg = np.linalg.norm(np.diff(points, axis=0), axis=1)
    arc = np.concatenate([[0.0], np.cumsum(seg)])
    s = np.linspace(0, arc[-1], max(int(np.ceil(arc[-1] / step)) + 1, 2))
    out = np.stack([np.interp(s, arc, points[:, k]) for k in range(3)], axis=1)
    src = np.clip(np.searchsorted(arc, s), 1, len(arc) - 1)
    src = np.where(s - arc[src - 1] < arc[src] - s, src - 1, src)
    return out, src


def _dense(tree: graph.CoronaryTree) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Dense points of every segment, the source point index of each, and its segment index."""
    pts, src, seg = [], [], []
    for s in tree.segments:
        p, i = resample(s.points)
        pts.append(p), src.append(s.point_indices[i]), seg.append(np.full(len(p), s.index))
    return np.concatenate(pts), np.concatenate(src), np.concatenate(seg)


def _geodesic(tree: graph.CoronaryTree) -> np.ndarray:
    """Arc length from the ostium at every centerline point."""
    d = np.full(len(tree.points), np.nan)
    for s in tree.walk():
        base = 0.0 if s.parent is None else d[tree.segments[s.parent].point_indices[-1]]
        arc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(s.points, axis=0), axis=1))])
        d[s.point_indices] = base + arc
    return d


def _bifurcations(gt: np.ndarray, pr: np.ndarray) -> dict:
    out = {"n_bif_gt": len(gt), "n_bif_pred": len(pr)}
    cost = np.linalg.norm(gt[:, None] - pr[None], axis=2) if len(gt) and len(pr) else np.zeros((len(gt), len(pr)))
    rows, cols = linear_sum_assignment(cost) if cost.size else ([], [])
    matched = cost[rows, cols] if cost.size else np.zeros(0)
    for g in BIF_GATES_MM:
        tp = int((matched <= g).sum())
        out[f"bif_tp_{g}mm"] = tp
        out[f"bif_precision_{g}mm"] = tp / len(pr) if len(pr) else np.nan
        out[f"bif_recall_{g}mm"] = tp / len(gt) if len(gt) else np.nan
    out["bif_matched_dist_median"] = float(np.median(matched[matched <= 3])) if (matched <= 3).any() else np.nan
    return out


def score_side(gt_cl: io.Centerline, gt_tree: graph.CoronaryTree, pr_tree: graph.CoronaryTree) -> dict:
    G, g_src, g_seg = _dense(gt_tree)
    P, _, p_seg = _dense(pr_tree)
    r_g = gt_cl.radius[g_src]
    tol_g = np.maximum(r_g, TOL_FLOOR_MM)
    d_gp = cKDTree(P).query(G)[0]
    d_pg, j = cKDTree(G).query(P)
    cov_g, ok_p = d_gp <= tol_g, d_pg <= tol_g[j]

    row = compute_centerline_point_metrics(P, G)
    tpr, fn, tpm, fp = cov_g.sum(), (~cov_g).sum(), ok_p.sum(), (~ok_p).sum()
    row["ov"] = (tpr + tpm) / (tpr + tpm + fn + fp)
    big_g, big_p = r_g >= OT_RADIUS_MM, r_g[j] >= OT_RADIUS_MM
    row["ot"] = (cov_g[big_g].sum() + ok_p[big_p].sum()) / max(big_g.sum() + big_p.sum(), 1)
    row["ai"] = float(np.concatenate([d_gp[cov_g], d_pg[ok_p]]).mean()) if tpr + tpm else np.nan
    row["recall"], row["precision"] = cov_g.mean(), ok_p.mean()
    row["gt_mm"], row["pred_mm"] = len(G) * STEP_MM, len(P) * STEP_MM

    # OF per ostium-to-terminus path of the delivered tree.
    geo = _geodesic(gt_tree)
    g_geo = geo[g_src]
    ofs = []
    for term in (s for s in gt_tree.segments if s.is_terminal):
        chain, s = [], term
        while s is not None:
            chain.append(s.index)
            s = None if s.parent is None else gt_tree.segments[s.parent]
        on = np.isin(g_seg, chain)
        order = np.argsort(g_geo[on])
        c, gd = cov_g[on][order], g_geo[on][order]
        miss = np.flatnonzero(~c & (gd > OF_GRACE_MM))
        ofs.append((gd[miss[0]] if len(miss) else gd[-1]) / gd[-1])
    row["of"] = float(np.mean(ofs))

    row.update(_bifurcations(np.array([n.position for n in gt_tree.bifurcations()]).reshape(-1, 3),
                             np.array([n.position for n in pr_tree.bifurcations()]).reshape(-1, 3)))

    # Terminal branches, ATM'22 rule, both directions.
    gt_term = [s.index for s in gt_tree.segments if s.is_terminal]
    pr_term = [s.index for s in pr_tree.segments if s.is_terminal]
    found = [cov_g[g_seg == k].mean() >= BRANCH_COVERAGE for k in gt_term]
    real = [ok_p[p_seg == k].mean() >= BRANCH_COVERAGE for k in pr_term]
    row["term_gt"], row["term_found"] = len(gt_term), int(sum(found))
    row["term_missed_mm"] = sum(gt_tree.segments[k].length for k, f in zip(gt_term, found) if not f)
    row["term_pred"], row["term_spurious"] = len(pr_term), int(len(real) - sum(real))
    row["term_spurious_mm"] = sum(pr_tree.segments[k].length for k, r in zip(pr_term, real) if not r)

    # Ostia: each delivered start point to the nearest extracted root.
    roots = np.array([pr_tree.points[r] for r in pr_tree.roots]).reshape(-1, 3)
    gt_starts = np.array([gt_tree.points[r] for r in gt_tree.roots]).reshape(-1, 3)
    row["ostium_dist_mm"] = float(cKDTree(roots).query(gt_starts)[0].max()) if len(roots) else np.nan
    row["n_roots_pred"] = len(roots)

    labels = np.asarray(gt_cl.segment_label, dtype=int)[g_src]
    labels[labels == 0] = 14  # case 272: 0 and 14 both mean "not attributed"
    for lab, name in graph.label_names().items():
        m = labels == lab
        row[f"recall_{name}"] = cov_g[m].mean() if m.any() else np.nan
    for lo, hi in zip(RADIUS_BINS[:-1], RADIUS_BINS[1:]):
        m = (r_g >= lo) & (r_g < hi)
        row[f"recall_r{lo:g}-{hi:g}"] = cov_g[m].mean() if m.any() else np.nan
    for lo, hi in zip(DIST_BINS[:-1], DIST_BINS[1:]):
        m = (g_geo >= lo) & (g_geo < hi)
        row[f"recall_d{lo:g}-{hi:g}"] = cov_g[m].mean() if m.any() else np.nan
    return row


def score_case(case_id: int, pred_dir) -> list[dict]:
    rows = []
    for side in ("left", "right"):
        row = {"case_id": case_id, "side": side}
        try:
            gt_cl = io.load_centerline(case_id, side)
            if gt_cl.radius is None:
                gt_cl.radius = radius.compute_gt_radius(case_id)[side]
            gt_tree, pr_cl = graph.build_tree(gt_cl), io.load_centerline(case_id, side, pred_dir)
            if len(pr_cl.points) == 0:
                raise ValueError("no extracted tree on this side")
            pr_tree = graph.build_tree(pr_cl)
            # A swapped side reads as a better match to the other delivered tree.
            other = io.load_centerline(case_id, "right" if side == "left" else "left")
            d_own = cKDTree(gt_cl.points).query(pr_cl.points)[0].mean()
            d_other = cKDTree(other.points).query(pr_cl.points)[0].mean()
            row["side_swapped"] = bool(d_other < d_own)
            row.update(score_side(gt_cl, gt_tree, pr_tree))
            row["warnings"] = "; ".join(pr_tree.warnings)
        except Exception as exc:
            row["error"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
    return rows


def _summary(df: pd.DataFrame) -> dict:
    num = df.select_dtypes("number").drop(columns=["case_id"], errors="ignore")
    return {"n": int(len(df)), "n_failed": int(df["error"].notna().sum()) if "error" in df else 0,
            "mean": num.mean().round(4).to_dict(), "median": num.median().round(4).to_dict(),
            "q25": num.quantile(0.25).round(4).to_dict(), "q75": num.quantile(0.75).round(4).to_dict()}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="folder under EXTRACTED")
    ap.add_argument("--split", default="test", choices=["train", "val", "test"])
    ap.add_argument("--against", help="another EXTRACTED folder already scored: paired Wilcoxon per metric")
    args = ap.parse_args()

    pred_dir = paths.EXTRACTED / args.dir
    rows = [r for c in paths.split_ids(args.split) for r in score_case(c, pred_dir)]
    df = pd.DataFrame(rows)
    df.to_csv(pred_dir / f"scores_{args.split}.csv", index=False)

    desc = paths.descriptors()
    summary = {"dir": args.dir, "split": args.split, "overall": _summary(df), "by_side": {}, "by_group": {}}
    for side, d in df.groupby("side"):
        summary["by_side"][side] = _summary(d)
    for col in ("Image Quality", "Dominance", "Disease"):
        g = df["case_id"].map(desc[col])
        summary["by_group"][col] = {str(v): _summary(df[g == v]) for v in g.dropna().unique()}
    if args.against:
        other = pd.read_csv(paths.EXTRACTED / args.against / f"scores_{args.split}.csv")
        m = df.merge(other, on=["case_id", "side"], suffixes=("", "_ref"))
        summary["wilcoxon_vs"] = {"against": args.against, "p": {}}
        for col in df.select_dtypes("number").columns.drop("case_id"):
            if f"{col}_ref" in m:
                a, b = m[col].astype(float), m[f"{col}_ref"].astype(float)
                ok = a.notna() & b.notna() & (a != b)
                if ok.sum() >= 10:
                    summary["wilcoxon_vs"]["p"][col] = float(wilcoxon(a[ok], b[ok]).pvalue)
    (pred_dir / f"summary_{args.split}.json").write_text(json.dumps(summary, indent=2, default=float) + "\n")
    print(json.dumps(summary["overall"]["median"], indent=1))


if __name__ == "__main__":
    main()
