#!/usr/bin/env python
"""Local branch volume AND mean radius in the same 3 mm shaft window scripts/bifurcation_volume.py
integrates volume over, healthy vs. diseased, for both daughters at each of the 5 named
bifurcations. Volume is the frustum sum used throughout (_branch_volume); radius is the plain mean
of the window's own per-point radii, the same population scripts/named_segment_volume.py reports
for the whole vessel, read here over the bifurcation-local window instead.

Mann-Whitney U, Benjamini-Hochberg FDR across all 20 bifurcation x branch x field tests run
together (5 bifurcations x {main, side} x {volume, radius}). Only rows surviving FDR < 0.05 are
printed, per instruction: this reports where the window differs, not every window.

Usage:  python scripts/bifurcation_window_radius.py [--n N]
"""

from __future__ import annotations

import argparse
import json

import numpy as np
from scipy import stats

from topology import angles, graph, paths

CORE_SCALE, WINDOW_MM = 1.0, 3.0
NAMED = ("LM", "LAD-D1", "LAD-D2", "LCX-OM1", "CRUX")


def _window_volume_radius(tree, seg):
    points, radii = tree.vessel_of(seg).shaft(seg, upstream=False)
    if radii is None:
        return float("nan"), float("nan")
    core = CORE_SCALE * float(radii[0])
    lo, hi, reason = graph.shaft_window(points, core, WINDOW_MM)
    if reason or hi - lo < 2:
        return float("nan"), float("nan")
    pts, rad = points[lo:hi], radii[lo:hi]
    ds = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    r0, r1 = rad[:-1], rad[1:]
    volume = float(np.sum((np.pi / 3.0) * ds * (r0**2 + r0 * r1 + r1**2)))
    return volume, float(rad.mean())


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
        if disease not in ("yes", "no"):
            continue
        for b in bs:
            if b.named not in NAMED or b.main is None or b.side_br is None:
                continue
            if b.main.segment is None or b.side_br.segment is None:
                continue
            tree = trees[b.side]
            v_main, r_main = _window_volume_radius(tree, tree.segments[b.main.segment])
            v_side, r_side = _window_volume_radius(tree, tree.segments[b.side_br.segment])
            rows.append({"case_id": cid, "disease": disease, "named": b.named,
                         "volume_main": v_main, "radius_main": r_main,
                         "volume_side": v_side, "radius_side": r_side})
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=0, help="first N cases only (0 = all)")
    args = ap.parse_args()

    ids = paths.usable_ids()[: args.n or None]
    print(f"=== extracting window volume/radius, {len(ids)} cases ===")
    rows = [r for r in _extract(ids) if np.isfinite(r["volume_main"]) and np.isfinite(r["volume_side"])]
    print(f"{len(rows)} bifurcation rows")

    tests = []
    for named in NAMED:
        for branch in ("main", "side"):
            h = [r for r in rows if r["named"] == named and r["disease"] == "no"]
            d = [r for r in rows if r["named"] == named and r["disease"] == "yes"]
            if len(h) < 5 or len(d) < 5:
                continue
            for field in ("volume", "radius"):
                key = f"{field}_{branch}"
                vh = np.array([r[key] for r in h])
                vd = np.array([r[key] for r in d])
                _, p = stats.mannwhitneyu(vh, vd, alternative="two-sided")
                tests.append({"named": named, "branch": branch, "field": field,
                             "n_h": len(h), "n_d": len(d),
                             "median_h": float(np.median(vh)), "median_d": float(np.median(vd)),
                             "p": float(p)})
    _fdr(tests)

    sig = [t for t in tests if t["q"] < 0.05]
    print(f"\n{len(sig)}/{len(tests)} bifurcation x branch x field tests survive FDR < 0.05:\n")
    print(f"{'bifurcation':<12}{'branch':<8}{'field':<8}{'n_h':>5}{'n_d':>5}"
          f"{'healthy (median)':>18}{'diseased (median)':>19}{'q':>10}")
    for t in sorted(sig, key=lambda t: t["q"]):
        unit = "mm^3" if t["field"] == "volume" else "mm"
        print(f"{t['named']:<12}{t['branch']:<8}{t['field']:<8}{t['n_h']:>5}{t['n_d']:>5}"
              f"{t['median_h']:>15.3f} {unit:<4}{t['median_d']:>16.3f} {unit:<4}{t['q']:>10.3g}")

    out = paths.output_dir("bifurcation_angles/window_volume_radius")
    (out / "summary.json").write_text(json.dumps(tests, indent=2) + "\n")
    print(f"\nWrote {out / 'summary.json'}")


if __name__ == "__main__":
    main()
