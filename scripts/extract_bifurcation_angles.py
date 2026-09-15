#!/usr/bin/env python
"""Extract the 5 target bifurcation angles for every case.

See topology/angles.py for the definitions. GT needs the radius cache
(scripts/compute_centerline_radius.py); predicted centerlines carry their own radius
(scripts/build_predicted_centerlines.py).

Usage:
  python scripts/extract_bifurcation_angles.py                        # GT, all 800 cases
  python scripts/extract_bifurcation_angles.py --source pred --run cas_net_pretrained
  python scripts/extract_bifurcation_angles.py --core-scale 0.5 --window-mm 5
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

import numpy as np

from topology import angles, paths


def _row(case_id: int, results: dict[str, angles.BifurcationResult]) -> dict:
    row = {"case_id": case_id}
    for name in angles.BIFURCATION_NAMES:
        r = results[name]
        row[f"{name}_angle_deg"] = round(r.angle_deg, 3) if np.isfinite(r.angle_deg) else ""
        row[f"{name}_side"] = r.side or ""
        row[f"{name}_origin_gap_mm"] = "" if r.origin_gap_mm is None else round(r.origin_gap_mm, 2)
        row[f"{name}_reason"] = r.reason or ""
        row[f"{name}_note"] = r.extra.get("note", "")
    row["LM_im_present"] = results["LM"].extra.get("im_present", "")
    row["CRUX_dominance_descriptor"] = results["CRUX"].extra.get("dominance_descriptor") or ""
    row["CRUX_dominance_mismatch"] = results["CRUX"].extra.get("dominance_mismatch", "")
    return row


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=("gt", "pred"), default="gt")
    ap.add_argument("--run", default="cas_net_pretrained", help="for --source pred")
    ap.add_argument("--core-scale", type=float, default=1.0,
                    help="core skipped at each junction, in multiples of the junction radius")
    ap.add_argument("--window-mm", type=float, default=3.0, help="length the direction is fitted over")
    ap.add_argument("--n", type=int, default=0, help="first N cases only (0 = all)")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    root = None
    if args.source == "pred":
        root = paths.OUTPUT_ROOT / "predicted_centerlines" / f"{args.run}_oracle"
        ids = sorted(int(p.name.split(".")[0]) for p in root.glob("*.json") if p.stem.isdigit())
        tag = f"pred_{args.run}_oracle"
    else:
        ids, tag = list(paths.usable_ids()), "gt"
    ids = ids[: args.n or None]
    tag += f"_core{args.core_scale:g}_win{args.window_mm:g}"
    out_dir = Path(args.out) if args.out else paths.output_dir(f"bifurcation_angles/{tag}")
    out_dir.mkdir(parents=True, exist_ok=True)

    t0, rows, errored = time.time(), [], []
    for cid in ids:
        try:
            rows.append(_row(cid, angles.extract_case(cid, root, args.core_scale, args.window_mm)))
        except Exception as exc:  # a per-case failure must be reported, not swallowed
            errored.append((cid, f"{type(exc).__name__}: {exc}"))

    csv_path = out_dir / "bifurcation_angles.csv"
    with csv_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    summary = {"code_version": paths.code_version(), "source": tag, "n_cases": len(rows),
               "core_scale": args.core_scale, "window_mm": args.window_mm, "load_errors": errored,
               "per_bifurcation": {}, "missing_reasons": {}}
    print(f"{len(rows)} cases in {time.time() - t0:.1f}s  ({tag}, code {summary['code_version']})")
    for cid, err in errored:
        print(f"    case {cid:>5}  FAILED: {err}")
    print(f"\n{'':>10}{'n':>6}{'missing':>9}{'median':>9}{'IQR':>18}")
    for name in angles.BIFURCATION_NAMES:
        vals = np.array([r[f"{name}_angle_deg"] for r in rows if r[f"{name}_angle_deg"] != ""], float)
        q1, med, q3 = np.percentile(vals, [25, 50, 75]) if len(vals) else (np.nan,) * 3
        print(f"  {name:<8}{len(vals):>6}{len(rows) - len(vals):>9}{med:>9.1f}   [{q1:.1f}, {q3:.1f}]")
        summary["per_bifurcation"][name] = {
            "n": int(len(vals)), "n_missing": len(rows) - len(vals),
            "median_deg": None if not len(vals) else round(float(med), 2),
            "q1_deg": None if not len(vals) else round(float(q1), 2),
            "q3_deg": None if not len(vals) else round(float(q3), 2)}
        counts: dict[str, int] = {}
        for r in rows:
            if r[f"{name}_reason"]:
                counts[r[f"{name}_reason"]] = counts.get(r[f"{name}_reason"], 0) + 1
        summary["missing_reasons"][name] = counts
    print("\nMissing-value reasons:")
    for name, counts in summary["missing_reasons"].items():
        for reason, count in sorted(counts.items(), key=lambda kv: -kv[1]):
            print(f"  {name:<8}{count:>4}  {reason}")

    (out_dir / "bifurcation_angles.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"\nWrote {csv_path}\n      {out_dir / 'bifurcation_angles.json'}")


if __name__ == "__main__":
    main()
