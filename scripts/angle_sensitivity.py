#!/usr/bin/env python
"""How much the GT bifurcation angles depend on the direction's two parameters.

Radius-aware directions over core scale {0.5, 1, 1.5} x window {2, 3, 5} mm, beside the old
3 mm-style secant from the junction point at 1.5 / 3 / 5 mm, which is kept here only as the
reference the new definition is meant to beat. Pairs are chosen once per case, so every setting
measures the same two segments. Reports each setting's median angle, and the per-case spread
(max - min over settings) for both families.

Usage:  python scripts/angle_sensitivity.py [--n N]
"""

from __future__ import annotations

import argparse
import itertools
import json

import numpy as np
import pandas as pd

from topology import angles, graph, paths

CORES, WINDOWS, SECANTS = (0.5, 1.0, 1.5), (2.0, 3.0, 5.0), (1.5, 3.0, 5.0)


def _secant(seg: graph.Segment, span: float) -> np.ndarray:
    step = np.linalg.norm(np.diff(seg.points, axis=0), axis=1)
    take = int(np.searchsorted(np.cumsum(step), span) + 1)
    v = seg.points[min(take, len(seg.points) - 1)] - seg.points[0]
    return v / np.linalg.norm(v)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=0)
    args = ap.parse_args()

    rows = []
    for cid in paths.usable_ids()[: args.n or None]:
        trees = graph.load_trees(cid)
        ref = angles.extract_trees(trees["left"], trees["right"], None)
        for name, r in ref.items():
            if r.segments is None:
                continue
            tree = trees[r.side]
            a, b = (tree.segments[i] for i in r.segments)
            row = {"case_id": cid, "bifurcation": name}
            for c, w in itertools.product(CORES, WINDOWS):
                va, ea = angles.direction(tree, a, c, w)
                vb, eb = angles.direction(tree, b, c, w)
                row[f"core{c:g}_win{w:g}"] = np.nan if ea or eb else np.degrees(np.arccos(np.clip(va @ vb, -1, 1)))
            for s in SECANTS:
                row[f"secant{s:g}"] = np.degrees(np.arccos(np.clip(_secant(a, s) @ _secant(b, s), -1, 1)))
            rows.append(row)

    df = pd.DataFrame(rows)
    new = [f"core{c:g}_win{w:g}" for c, w in itertools.product(CORES, WINDOWS)]
    old = [f"secant{s:g}" for s in SECANTS]
    out = paths.output_dir("bifurcation_angles/sensitivity")
    df.to_csv(out / "angle_sensitivity.csv", index=False)

    summary = {"code_version": paths.code_version(), "per_bifurcation": {}}
    for name, g in df.groupby("bifurcation", sort=False):
        print(f"\n{name}  (n = {len(g)})")
        print("  median angle:  " + "  ".join(f"{k}={g[k].median():.1f}" for k in new))
        print("  old secant:    " + "  ".join(f"{k}={g[k].median():.1f}" for k in old))
        spread_new = (g[new].max(axis=1) - g[new].min(axis=1)).dropna()
        spread_old = g[old].max(axis=1) - g[old].min(axis=1)
        print(f"  per-case spread across settings: radius-aware median {spread_new.median():.1f}, "
              f"90th {spread_new.quantile(.9):.1f}  |  secant median {spread_old.median():.1f}, "
              f"90th {spread_old.quantile(.9):.1f}")
        summary["per_bifurcation"][name] = {
            "n": len(g), "median_by_setting": {k: round(float(g[k].median()), 2) for k in new + old},
            "spread_radius_aware": [round(float(spread_new.median()), 2), round(float(spread_new.quantile(.9)), 2)],
            "spread_secant": [round(float(spread_old.median()), 2), round(float(spread_old.quantile(.9)), 2)]}
    (out / "angle_sensitivity.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"\nWrote {out / 'angle_sensitivity.csv'}")


if __name__ == "__main__":
    main()
