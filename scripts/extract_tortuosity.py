#!/usr/bin/env python
"""Extract the tortuosity panel for LM, LAD, LCX and RCA, for every case.

See topology/tortuosity.py for the metric definitions and why both a classical (curvature,
torsion) and an out-of-plane-distance family are reported. One row per named vessel per case
(4 rows/case), written incrementally so a mid-cohort crash does not lose completed cases.

Usage:
  python scripts/extract_tortuosity.py                          # all 800 GT cases
  python scripts/extract_tortuosity.py --sigma 1.5 --window-mm 30
  python scripts/extract_tortuosity.py --pred RUN_DIR            # predicted centerlines
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

import numpy as np

from topology import paths, tortuosity

FIELDNAMES = [
    "case_id", "side", "name", "vessel", "n_segments",
    "sigma_mm", "step_mm", "window_mm",
    "length_mm", "chord_mm", "n_points",
    "distance_metric", "soam_per_mm", "total_turning_deg", "inflections", "icm",
    "curvature_mean", "curvature_max", "curvature_rms", "torsion_mean_abs", "non_planarity",
    "bends_over_45",
    "plane_d_max_mm", "plane_d_rms_mm", "plane_d_rms_norm", "plane_d_max_pos",
    "plane_angle_mean_deg", "plane_angle_max_deg",
    "soam_window_max_per_mm", "soam_window_max_pos",
    "curvature_rms_window_max", "curvature_rms_window_max_pos",
    "reason", "note", "tree_warnings", "plane_degenerate", "plane_eig_ratio",
    "torsion_n_masked", "torsion_n_total", "soam_window_clipped", "curvature_window_clipped",
]

METRICS_FOR_SUMMARY = [
    "distance_metric", "soam_per_mm", "curvature_mean", "curvature_max", "curvature_rms",
    "torsion_mean_abs", "non_planarity", "bends_over_45",
    "plane_d_max_mm", "plane_d_rms_mm", "plane_d_rms_norm",
    "plane_angle_mean_deg", "plane_angle_max_deg",
    "soam_window_max_per_mm", "curvature_rms_window_max",
]


def _r(x) -> float | str:
    return round(float(x), 4) if isinstance(x, (int, float)) and np.isfinite(x) else ""


def _row(case_id: int, v: tortuosity.VesselTortuosity) -> dict:
    return {
        "case_id": case_id, "side": v.side or "", "name": v.name,
        "vessel": v.vessel if v.vessel is not None else "", "n_segments": v.n_segments,
        "sigma_mm": _r(v.sigma_mm), "step_mm": _r(v.step_mm), "window_mm": _r(v.window_mm),
        "length_mm": _r(v.length_mm), "chord_mm": _r(v.chord_mm), "n_points": v.n_points,
        "distance_metric": _r(v.distance_metric), "soam_per_mm": _r(v.soam_per_mm),
        "total_turning_deg": _r(v.total_turning_deg), "inflections": v.inflections, "icm": _r(v.icm),
        "curvature_mean": _r(v.curvature_mean), "curvature_max": _r(v.curvature_max),
        "curvature_rms": _r(v.curvature_rms), "torsion_mean_abs": _r(v.torsion_mean_abs),
        "non_planarity": _r(v.non_planarity), "bends_over_45": v.bends_over_45,
        "plane_d_max_mm": _r(v.plane_d_max_mm), "plane_d_rms_mm": _r(v.plane_d_rms_mm),
        "plane_d_rms_norm": _r(v.plane_d_rms_norm), "plane_d_max_pos": _r(v.plane_d_max_pos),
        "plane_angle_mean_deg": _r(v.plane_angle_mean_deg), "plane_angle_max_deg": _r(v.plane_angle_max_deg),
        "soam_window_max_per_mm": _r(v.soam_window_max_per_mm), "soam_window_max_pos": _r(v.soam_window_max_pos),
        "curvature_rms_window_max": _r(v.curvature_rms_window_max),
        "curvature_rms_window_max_pos": _r(v.curvature_rms_window_max_pos),
        "reason": v.reason or "", "note": v.extra.get("note", ""),
        "tree_warnings": v.extra.get("tree_warnings", ""),
        "plane_degenerate": v.extra.get("plane_degenerate", ""),
        "plane_eig_ratio": v.extra.get("plane_eig_ratio", ""),
        "torsion_n_masked": v.extra.get("torsion_n_masked", ""),
        "torsion_n_total": v.extra.get("torsion_n_total", ""),
        "soam_window_clipped": v.extra.get("soam_window_clipped", ""),
        "curvature_window_clipped": v.extra.get("curvature_window_clipped", ""),
    }


def _finite(rows: list[dict], key: str) -> np.ndarray:
    return np.array([r[key] for r in rows if r[key] != ""], float)


def _fmt(stats: dict, metric: str, nd: int = 3) -> str:
    s = stats.get(metric)
    return f"{s['median']:.{nd}f}" if s else "--"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sigma", type=float, default=tortuosity.DEFAULT_SIGMA_MM,
                    help="smoothing scale in mm before any derivative is taken")
    ap.add_argument("--step-mm", type=float, default=tortuosity.RESAMPLE_MM,
                    help="arc-length resampling grid, mm")
    ap.add_argument("--window-mm", type=float, default=tortuosity.DEFAULT_WINDOW_MM,
                    help="sliding-window width for the windowed SOAM/curvature max, mm")
    ap.add_argument("--n", type=int, default=0, help="first N cases only (0 = all)")
    ap.add_argument("--pred", default=None, help="run dir of predicted centerlines, instead of GT")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    root = Path(paths.OUTPUT_ROOT / "predicted_centerlines" / args.pred) if args.pred else None
    ids, tag = list(paths.usable_ids()), f"pred_{args.pred}" if args.pred else "gt"
    ids = ids[: args.n or None]
    tag += f"_sigma{args.sigma:g}_win{args.window_mm:g}"
    out_dir = Path(args.out) if args.out else paths.output_dir(f"tortuosity/{tag}")
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / "tortuosity.csv"
    t0, all_rows, errored = time.time(), [], []
    with csv_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        for cid in ids:
            try:
                case_rows = [_row(cid, v) for v in tortuosity.extract_case(
                    cid, root, args.sigma, args.step_mm, args.window_mm)]
            except Exception as exc:  # a per-case failure must be reported, not swallowed
                errored.append((cid, f"{type(exc).__name__}: {exc}"))
                continue
            writer.writerows(case_rows)
            fh.flush()
            all_rows.extend(case_rows)
    n_cases = len(ids) - len(errored)

    summary = {"code_version": paths.code_version(), "source": tag, "n_cases": n_cases,
               "n_rows": len(all_rows), "sigma_mm": args.sigma, "step_mm": args.step_mm,
               "window_mm": args.window_mm, "load_errors": errored,
               "per_vessel": {}, "missing_reasons": {}}
    print(f"{n_cases} cases, {len(all_rows)} vessel rows, in {time.time() - t0:.1f}s "
          f"({tag}, code {summary['code_version']})")
    for cid, err in errored:
        print(f"    case {cid:>5}  FAILED: {err}")

    print(f"\nPer-vessel panel, over {n_cases} cases:")
    for name in tortuosity.VESSEL_SIDES:
        vrows = [r for r in all_rows if r["name"] == name]
        stats = {}
        for metric in METRICS_FOR_SUMMARY:
            vals = _finite(vrows, metric)
            if len(vals) == 0:
                stats[metric] = None
                continue
            q1, med, q3, p95 = np.percentile(vals, [25, 50, 75, 95])
            stats[metric] = {"n": int(len(vals)), "median": round(float(med), 4),
                             "q1": round(float(q1), 4), "q3": round(float(q3), 4),
                             "p95_top5pct_threshold": round(float(p95), 4)}
        summary["per_vessel"][name] = stats
        n_missing = len(vrows) - (stats["distance_metric"]["n"] if stats["distance_metric"] else 0)
        print(f"  {name:<5} n={len(vrows):>4}  missing={n_missing:>3}  "
              f"L/D={_fmt(stats,'distance_metric')}  curv_rms={_fmt(stats,'curvature_rms',4)}  "
              f"non_planarity={_fmt(stats,'non_planarity',4)}  "
              f"plane_d_rms_norm={_fmt(stats,'plane_d_rms_norm',4)}")
        counts: dict[str, int] = {}
        for r in vrows:
            if r["reason"]:
                counts[r["reason"]] = counts.get(r["reason"], 0) + 1
        summary["missing_reasons"][name] = counts

    print("\nMissing-value reasons:")
    for name, counts in summary["missing_reasons"].items():
        for reason, count in sorted(counts.items(), key=lambda kv: -kv[1]):
            print(f"  {name:<5}{count:>4}  {reason}")

    (out_dir / "tortuosity.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"\nWrote {csv_path}\n      {out_dir / 'tortuosity.json'}")


if __name__ == "__main__":
    main()
