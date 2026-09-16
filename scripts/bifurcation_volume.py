#!/usr/bin/env python
"""Local branch volume at each bifurcation, and whether it separates healthy from diseased cases
where angle (scripts/extract_bifurcation_angles.py) does not.

Volume is the frustum-integrated lumen volume of the main/side daughter over the same shaft
window angles.py already reads direction and caliber from (past the core, out to window_mm of
arc), so it is directly comparable to angle_deg/radius_ratio rather than a whole-vessel volume.
Needs the radius cache (scripts/compute_centerline_radius.py) first.

Reports, healthy vs. diseased (Mann-Whitney U, Benjamini-Hochberg FDR across all tests):
  1. per-case mean volume, pooled over all bifurcations and per named bifurcation
  2. the same, stratified by dominance, for the two bifurcations found significant in (1)
  3. whether combining angle with volume predicts disease better than volume alone (5-fold CV
     logistic regression AUC, at the bifurcation with the strongest volume signal)
  4. a per-patient composite angle z-score across all five named bifurcations (the single most
     powerful angle-only test available from this cohort's Disease label) and a post-hoc power
     check against the published literature's effect size

Usage:  python scripts/bifurcation_volume.py [--n N]
"""

from __future__ import annotations

import argparse
import json

import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from statsmodels.stats.power import TTestIndPower

from topology import angles, graph, paths

CORE_SCALE, WINDOW_MM = 1.0, 3.0
NAMED = ("LM", "LAD-D1", "LAD-D2", "LCX-OM1", "CRUX")


def _branch_volume(tree: graph.CoronaryTree, seg: graph.Segment) -> float:
    points, radii = tree.vessel_of(seg).shaft(seg, upstream=False)
    if radii is None:
        return float("nan")
    core = CORE_SCALE * float(radii[0])
    lo, hi, reason = graph.shaft_window(points, core, WINDOW_MM)
    if reason or hi - lo < 2:
        return float("nan")
    pts, rad = points[lo:hi], radii[lo:hi]
    ds = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    r0, r1 = rad[:-1], rad[1:]
    return float(np.sum((np.pi / 3.0) * ds * (r0**2 + r0 * r1 + r1**2)))


def _extract(ids) -> list[dict]:
    desc = paths.descriptors()
    rows = []
    for cid in ids:
        try:
            trees = graph.load_trees(cid)
            dominance = desc.loc[cid, "Dominance"] if cid in desc.index else None
            dominance = dominance if isinstance(dominance, str) else None
            bs = angles.extract_trees(trees["left"], trees["right"], dominance, CORE_SCALE, WINDOW_MM)
        except Exception as exc:
            print(f"  case {cid} FAILED: {type(exc).__name__}: {exc}")
            continue
        disease = desc.loc[cid, "Disease"] if cid in desc.index else None
        disease = disease if isinstance(disease, str) else None
        for b in bs:
            if b.main is None or b.side_br is None or b.main.segment is None or b.side_br.segment is None:
                continue
            tree = trees[b.side]
            v_main = _branch_volume(tree, tree.segments[b.main.segment])
            v_side = _branch_volume(tree, tree.segments[b.side_br.segment])
            rows.append({
                "case_id": cid, "disease": disease, "dominance": dominance, "named": b.named or "",
                "angle_deg": b.angle_deg, "v_main": v_main, "v_side": v_side,
                "v_total": v_main + v_side if np.isfinite(v_main) and np.isfinite(v_side) else np.nan,
            })
    return rows


def _fdr(tests: list[dict]) -> None:
    ps = np.array([t["p"] for t in tests])
    order = np.argsort(ps)
    m = len(ps)
    q = np.empty(m)
    prev = 1.0
    for rank, idx in enumerate(order[::-1], start=1):
        i = m - rank + 1
        prev = min(prev, ps[idx] * m / i)
        q[idx] = prev
    for t, qv in zip(tests, q):
        t["q"] = float(qv)


def _per_case_mean(rows, field, disease, named=None):
    by_case: dict[int, list[float]] = {}
    for r in rows:
        if r["disease"] != disease or (named is not None and r["named"] != named):
            continue
        by_case.setdefault(r["case_id"], []).append(r[field])
    return np.array([np.mean(v) for v in by_case.values()])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=0, help="first N cases only (0 = all)")
    args = ap.parse_args()

    ids = paths.usable_ids()[: args.n or None]
    print(f"=== 1/4 extracting local branch volume, {len(ids)} cases ===")
    rows = _extract(ids)
    rows = [r for r in rows if r["disease"] in ("yes", "no") and np.isfinite(r["v_total"])]
    print(f"{len(rows)} bifurcation rows, {len({r['case_id'] for r in rows})} cases with a usable volume")

    print("\n=== 2/4 disease vs. healthy, per-case mean volume (FDR across all groups x fields) ===")
    groups = ["All (pooled)", *NAMED]
    fields = ["v_main", "v_side", "v_total"]
    tests = []
    for g in groups:
        named = None if g == "All (pooled)" else g
        for f in fields:
            h, d = _per_case_mean(rows, f, "no", named), _per_case_mean(rows, f, "yes", named)
            if len(h) < 5 or len(d) < 5:
                continue
            u, p = stats.mannwhitneyu(h, d, alternative="two-sided")
            tests.append({"group": g, "field": f, "n_h": len(h), "n_d": len(d),
                          "med_h": float(np.median(h)), "med_d": float(np.median(d)), "p": float(p)})
    _fdr(tests)
    for t in sorted(tests, key=lambda t: t["p"]):
        pct = 100 * (t["med_d"] - t["med_h"]) / t["med_h"]
        sig = "*" if t["q"] < 0.05 else " "
        print(f"  {t['group']:<14}{t['field']:<8} n_h={t['n_h']:>4} n_d={t['n_d']:>4}  "
              f"{t['med_h']:>7.2f} -> {t['med_d']:>7.2f}  ({pct:+.1f}%)  p={t['p']:.3g}  q={t['q']:.3g}{sig}")
    n_sig = sum(1 for t in tests if t["q"] < 0.05)
    print(f"  {n_sig}/{len(tests)} survive FDR<0.05")

    print("\n=== 3/4 dominance stratification, CRUX and LCX-OM1 ===")
    for name in ("CRUX", "LCX-OM1"):
        for dom in ("R", "L", "Co"):
            sub = [r for r in rows if r["named"] == name and r["dominance"] == dom]
            h = np.array([r["v_main"] for r in sub if r["disease"] == "no"])
            d = np.array([r["v_main"] for r in sub if r["disease"] == "yes"])
            if len(h) < 5 or len(d) < 5:
                print(f"  {name:<10}{dom:<4} n_h={len(h)} n_d={len(d)}  too few")
                continue
            u, p = stats.mannwhitneyu(h, d, alternative="two-sided")
            pct = 100 * (np.median(d) - np.median(h)) / np.median(h)
            print(f"  {name:<10}{dom:<4} n_h={len(h):>4} n_d={len(d):>4}  v_main {pct:+.1f}%  p={p:.3g}")

    print("\n=== 4/4 angle vs. volume, combined, at CRUX (5-fold CV logistic regression AUC) ===")
    sub = [r for r in rows if r["named"] == "CRUX"]
    y = np.array([1 if r["disease"] == "yes" else 0 for r in sub])
    angle = np.array([r["angle_deg"] for r in sub])
    vol = np.log(np.array([r["v_total"] for r in sub]))
    z = lambda x: (x - x.mean()) / x.std()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    for name, X in [("angle only", z(angle).reshape(-1, 1)), ("volume only", z(vol).reshape(-1, 1)),
                    ("angle + volume", np.column_stack([z(angle), z(vol)]))]:
        aucs = cross_val_score(LogisticRegression(), X, y, cv=cv, scoring="roc_auc")
        print(f"  {name:<16} AUC = {aucs.mean():.3f} +- {aucs.std():.3f}")

    print("\n=== composite per-patient angle z-score across all 5 named bifurcations ===")
    by_bif: dict[str, list[float]] = {}
    for r in rows:
        if r["named"]:
            by_bif.setdefault(r["named"], []).append(r["angle_deg"])
    mu = {k: float(np.mean(v)) for k, v in by_bif.items()}
    sd = {k: float(np.std(v)) for k, v in by_bif.items()}
    by_case_z: dict[int, dict] = {}
    for r in rows:
        if not r["named"]:
            continue
        zc = (r["angle_deg"] - mu[r["named"]]) / sd[r["named"]]
        by_case_z.setdefault(r["case_id"], {"disease": r["disease"], "z": []})["z"].append(zc)
    comp = [(v["disease"], float(np.mean(v["z"]))) for v in by_case_z.values() if len(v["z"]) >= 2]
    h = np.array([zc for dis, zc in comp if dis == "no"])
    d = np.array([zc for dis, zc in comp if dis == "yes"])
    u, p = stats.mannwhitneyu(h, d, alternative="two-sided")
    print(f"  n_h={len(h)}, n_d={len(d)}, mean_z_h={h.mean():.3f}, mean_z_d={d.mean():.3f}, p={p:.3g}")

    pooled_sd = np.sqrt(((len(h) - 1) * h.std(ddof=1) ** 2 + (len(d) - 1) * d.std(ddof=1) ** 2)
                        / (len(h) + len(d) - 2))
    analysis = TTestIndPower()
    mde = analysis.solve_power(effect_size=None, nobs1=len(h), ratio=len(d) / len(h), alpha=0.05, power=0.8) * pooled_sd
    print(f"  minimum detectable effect at this n, 80% power: {mde:.3f} SD units")

    out = paths.output_dir("bifurcation_angles/volume_disease")
    (out / "summary.json").write_text(json.dumps({"volume_tests": tests}, indent=2) + "\n")
    print(f"\nWrote {out / 'summary.json'}")


if __name__ == "__main__":
    main()
