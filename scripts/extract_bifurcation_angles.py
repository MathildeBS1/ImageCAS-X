#!/usr/bin/env python
"""Extract every bifurcation's angle and caliber panel, for every case.

See topology/angles.py for the definitions and the caliber-conditioning motivation. Needs the
radius cache (scripts/compute_centerline_radius.py) first.

One row per bifurcation (long format): every splitting node in both trees, with the five named
ones (see topology.angles.BIFURCATION_NAMES) flagged via the ``named`` column.

Usage:
  python scripts/extract_bifurcation_angles.py                        # all 800 GT cases
  python scripts/extract_bifurcation_angles.py --core-scale 0.5 --window-mm 5
  python scripts/extract_bifurcation_angles.py --pred RUN_DIR          # predicted centerlines
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

import numpy as np

from topology import angles, paths


def _r(x) -> float | str:
    return round(float(x), 3) if isinstance(x, (int, float)) and np.isfinite(x) else ""


def _row(case_id: int, b: angles.Bifurcation) -> dict:
    parent, main, side = b.parent, b.main, b.side_br
    return {
        "case_id": case_id, "side": b.side or "", "node": b.node if b.node is not None else "",
        "named": b.named or "", "n_daughters": b.n_daughters, "generation": b.generation,
        "dist_from_ostium_mm": _r(b.dist_from_ostium_mm),
        "origin_gap_mm": _r(b.origin_gap_mm) if b.origin_gap_mm is not None else "",
        "parent_name": parent.name if parent else "",
        "parent_radius_mm": _r(parent.radius_mm) if parent else "",
        "main_name": main.name if main else "", "main_radius_mm": _r(main.radius_mm) if main else "",
        "side_name": side.name if side else "", "side_radius_mm": _r(side.radius_mm) if side else "",
        "angle_deg": _r(b.angle_deg), "theta_main_deg": _r(b.theta_main_deg),
        "theta_side_deg": _r(b.theta_side_deg), "out_of_plane_deg": _r(b.out_of_plane_deg),
        "radius_ratio": _r(b.radius_ratio), "area_ratio": _r(b.area_ratio),
        "finet_ratio": _r(b.finet_ratio),
        "reason": b.reason or "", "caliber_anomaly": b.extra.get("caliber_anomaly", ""),
        "note": b.extra.get("note", ""), "im_present": b.extra.get("im_present", ""),
        "dominance_descriptor": b.extra.get("dominance_descriptor") or "",
        "dominance_mismatch": b.extra.get("dominance_mismatch", ""),
    }


def _finite(rows: list[dict], key: str) -> np.ndarray:
    return np.array([r[key] for r in rows if r[key] != ""], float)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--core-scale", type=float, default=1.0,
                    help="core skipped at each junction, in multiples of the junction radius")
    ap.add_argument("--window-mm", type=float, default=3.0, help="length direction/caliber are read over")
    ap.add_argument("--n", type=int, default=0, help="first N cases only (0 = all)")
    ap.add_argument("--pred", default=None, help="run dir of predicted centerlines, instead of GT")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    root = Path(paths.OUTPUT_ROOT / "predicted_centerlines" / args.pred) if args.pred else None
    ids, tag = list(paths.usable_ids()), f"pred_{args.pred}" if args.pred else "gt"
    ids = ids[: args.n or None]
    tag += f"_core{args.core_scale:g}_win{args.window_mm:g}"
    out_dir = Path(args.out) if args.out else paths.output_dir(f"bifurcation_angles/{tag}")
    out_dir.mkdir(parents=True, exist_ok=True)

    t0, rows, errored = time.time(), [], []
    for cid in ids:
        try:
            rows.extend(_row(cid, b) for b in angles.extract_case(cid, root, args.core_scale, args.window_mm))
        except Exception as exc:  # a per-case failure must be reported, not swallowed
            errored.append((cid, f"{type(exc).__name__}: {exc}"))
    n_cases = len(ids) - len(errored)

    csv_path = out_dir / "bifurcation_angles.csv"
    with csv_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    summary = {"code_version": paths.code_version(), "source": tag, "n_cases": n_cases,
               "n_rows": len(rows), "core_scale": args.core_scale, "window_mm": args.window_mm,
               "load_errors": errored, "per_bifurcation": {}, "missing_reasons": {},
               "by_radius_ratio": {}}
    print(f"{n_cases} cases, {len(rows)} bifurcation rows, in {time.time() - t0:.1f}s "
          f"({tag}, code {summary['code_version']})")
    for cid, err in errored:
        print(f"    case {cid:>5}  FAILED: {err}")

    print(f"\nNamed bifurcations, over {n_cases} cases:")
    print(f"{'':>10}{'n':>6}{'missing':>9}{'median':>9}{'IQR':>18}")
    for name in angles.BIFURCATION_NAMES:
        named_rows = [r for r in rows if r["named"] == name]
        vals = _finite(named_rows, "angle_deg")
        q1, med, q3 = np.percentile(vals, [25, 50, 75]) if len(vals) else (np.nan,) * 3
        print(f"  {name:<8}{len(vals):>6}{n_cases - len(vals):>9}{med:>9.1f}   [{q1:.1f}, {q3:.1f}]")
        summary["per_bifurcation"][name] = {
            "n": int(len(vals)), "n_missing": n_cases - len(vals),
            "median_deg": None if not len(vals) else round(float(med), 2),
            "q1_deg": None if not len(vals) else round(float(q1), 2),
            "q3_deg": None if not len(vals) else round(float(q3), 2)}
        counts: dict[str, int] = {}
        for r in named_rows:
            if r["reason"]:
                counts[r["reason"]] = counts.get(r["reason"], 0) + 1
        summary["missing_reasons"][name] = counts

    print("\nMissing-value reasons:")
    for name, counts in summary["missing_reasons"].items():
        for reason, count in sorted(counts.items(), key=lambda kv: -kv[1]):
            print(f"  {name:<8}{count:>4}  {reason}")

    # The point of the caliber panel: does the daughter-daughter angle stay flat across radius
    # ratio while the parent-relative split moves? Over every bifurcation (not just the named
    # five), binned by how asymmetric the daughters are.
    bins = [("thin side (<0.4)", 0.0, 0.4), ("mixed (0.4-0.7)", 0.4, 0.7), ("symmetric (>=0.7)", 0.7, 1.01)]
    print(f"\n{'':>20}{'n':>6}{'angle':>9}{'theta_main':>13}{'theta_side':>13}")
    for label, lo, hi in bins:
        sub = [r for r in rows if r["radius_ratio"] != "" and lo <= r["radius_ratio"] < hi]
        med = {k: (float(np.median(v)) if len(v := _finite(sub, k)) else None)
               for k in ("angle_deg", "theta_main_deg", "theta_side_deg")}
        n = len(sub)
        fmt = lambda v: f"{v:>9.1f}" if v is not None else f"{'--':>9}"
        print(f"  {label:<18}{n:>6}{fmt(med['angle_deg'])}{fmt(med['theta_main_deg']):>13}"
              f"{fmt(med['theta_side_deg']):>13}")
        summary["by_radius_ratio"][label] = {"n": n, "median": med}

    (out_dir / "bifurcation_angles.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"\nWrote {csv_path}\n      {out_dir / 'bifurcation_angles.json'}")


if __name__ == "__main__":
    main()
