#!/usr/bin/env python
"""How much the tortuosity panel depends on its two free parameters: smoothing scale and window
width.

Sigma and window affect different metrics, so they are swept independently rather than crossed:
sigma is varied at the default window, window at the default sigma. Vessels are selected once per
case (topology.tortuosity._select_vessel) and re-measured under every setting, so every setting
sees the same anatomy -- the same discipline as scripts/angle_sensitivity.py.

Reports, per vessel name and metric:
  - per-case spread (max - min) across settings, median and 90th percentile
  - Spearman rank correlation of the cohort ordering, sigma=1.0mm against every other setting
  - Jaccard overlap of the top-5% set, sigma=1.0mm against every other setting

The last two are the numbers objective 9's tail flag actually needs: whether the same patients
land in the extreme tail under a different, still-defensible smoothing choice, not just whether
the raw value moves.

Usage:  python scripts/tortuosity_sensitivity.py [--n N]
"""

from __future__ import annotations

import argparse
import json

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from topology import graph, paths, tortuosity

SIGMAS = (0.0, 0.5, 1.0, 2.0)
WINDOWS = (10.0, 20.0, 30.0)
REFERENCE_SIGMA = 1.0
REFERENCE_WINDOW = tortuosity.DEFAULT_WINDOW_MM
TOP_PCT = 5.0

SIGMA_METRICS = ("distance_metric", "soam_per_mm", "curvature_mean", "curvature_max",
                 "curvature_rms", "torsion_mean_abs", "non_planarity",
                 "plane_d_rms_norm", "plane_angle_mean_deg")
WINDOW_METRICS = ("soam_window_max_per_mm", "curvature_rms_window_max")


def _case_vessels(cid: int) -> list[dict]:
    """This case's vessels' points, selected once, each tagged with its name."""
    trees = graph.load_trees(cid)
    out = []
    for name, side in tortuosity.VESSEL_SIDES.items():
        vessel, _reason, _extra = tortuosity._select_vessel(trees[side], name)
        if vessel is not None:
            out.append({"case_id": cid, "name": name, "points": vessel.points})
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=0)
    args = ap.parse_args()

    rows = []
    for cid in paths.usable_ids()[: args.n or None]:
        try:
            vessels = _case_vessels(cid)
        except Exception:
            continue
        for v in vessels:
            row = {"case_id": v["case_id"], "name": v["name"]}
            for sigma in SIGMAS:
                result = tortuosity.measure(v["points"], sigma_mm=sigma, window_mm=REFERENCE_WINDOW)
                for metric in SIGMA_METRICS:
                    row[f"{metric}_sigma{sigma:g}"] = result[metric] if isinstance(result, dict) else np.nan
            for window in WINDOWS:
                result = tortuosity.measure(v["points"], sigma_mm=REFERENCE_SIGMA, window_mm=window)
                for metric in WINDOW_METRICS:
                    row[f"{metric}_win{window:g}"] = result[metric] if isinstance(result, dict) else np.nan
            rows.append(row)

    df = pd.DataFrame(rows)
    out = paths.output_dir("tortuosity/sensitivity")
    df.to_csv(out / "tortuosity_sensitivity.csv", index=False)

    summary = {"code_version": paths.code_version(), "sigmas": SIGMAS, "windows": WINDOWS,
              "reference_sigma": REFERENCE_SIGMA, "top_pct": TOP_PCT, "per_vessel": {}}
    for name, g in df.groupby("name", sort=False):
        print(f"\n{name}  (n = {len(g)})")
        vessel_summary = {}
        for metric in SIGMA_METRICS:
            cols = [f"{metric}_sigma{s:g}" for s in SIGMAS]
            sub = g[cols].dropna()
            if sub.empty:
                continue
            spread = sub.max(axis=1) - sub.min(axis=1)
            ref = f"{metric}_sigma{REFERENCE_SIGMA:g}"
            ref_vals = sub[ref]
            ref_top = set(sub.index[ref_vals >= np.percentile(ref_vals, 100 - TOP_PCT)])
            ranks, jaccards = {}, {}
            for sigma in SIGMAS:
                col = f"{metric}_sigma{sigma:g}"
                if col == ref:
                    continue
                rho, _p = spearmanr(sub[ref], sub[col])
                other_top = set(sub.index[sub[col] >= np.percentile(sub[col], 100 - TOP_PCT)])
                union = ref_top | other_top
                jacc = len(ref_top & other_top) / len(union) if union else float("nan")
                ranks[f"sigma{sigma:g}"] = round(float(rho), 3)
                jaccards[f"sigma{sigma:g}"] = round(float(jacc), 3)
            print(f"  {metric:<22} spread median={spread.median():.4f} 90th={spread.quantile(.9):.4f}  "
                  "rank-vs-sigma1: " + "  ".join(f"{k}={v}" for k, v in ranks.items()) +
                  f"  top{TOP_PCT:g}%-jaccard: " + "  ".join(f"{k}={v}" for k, v in jaccards.items()))
            vessel_summary[metric] = {
                "spread_median": round(float(spread.median()), 4),
                "spread_p90": round(float(spread.quantile(.9)), 4),
                "spearman_vs_sigma1": ranks, "top5pct_jaccard_vs_sigma1": jaccards}
        for metric in WINDOW_METRICS:
            cols = [f"{metric}_win{w:g}" for w in WINDOWS]
            sub = g[cols].dropna()
            if sub.empty:
                continue
            spread = sub.max(axis=1) - sub.min(axis=1)
            print(f"  {metric:<22} spread across window widths: median={spread.median():.4f} "
                  f"90th={spread.quantile(.9):.4f}")
            vessel_summary[metric] = {"spread_median": round(float(spread.median()), 4),
                                      "spread_p90": round(float(spread.quantile(.9)), 4)}
        summary["per_vessel"][name] = vessel_summary

    (out / "tortuosity_sensitivity.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"\nWrote {out / 'tortuosity_sensitivity.csv'}")


if __name__ == "__main__":
    main()
