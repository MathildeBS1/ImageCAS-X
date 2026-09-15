#!/usr/bin/env python
"""How much error the predicted-mask extraction adds to each bifurcation angle.

Compares the angles measured on centerlines built from a run's predicted masks
(scripts/build_predicted_centerlines.py, ORACLE ostium and names) with those measured on the
delivered GT centerlines of the same cases. Reports, per bifurcation: how often it is found in
one tree and not the other, and |pred - gt| next to the spread between people (GT IQR on the
same cases). Writes validation.csv (per case) and validation.json beside the prediction angles.

Usage:  python scripts/validate_extraction.py [--run cas_net_pretrained] [--core-scale 1] [--window-mm 3]
"""

from __future__ import annotations

import argparse
import json

import numpy as np
import pandas as pd

from topology import angles, paths


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="cas_net_pretrained")
    ap.add_argument("--core-scale", type=float, default=1.0)
    ap.add_argument("--window-mm", type=float, default=3.0)
    args = ap.parse_args()

    setting = f"_core{args.core_scale:g}_win{args.window_mm:g}"
    base = paths.OUTPUT_ROOT / "bifurcation_angles"
    gt = pd.read_csv(base / f"gt{setting}" / "bifurcation_angles.csv").set_index("case_id")
    pred_dir = base / f"pred_{args.run}_oracle{setting}"
    pred = pd.read_csv(pred_dir / "bifurcation_angles.csv").set_index("case_id")
    gt = gt.loc[gt.index.intersection(pred.index)]

    rows, summary = [], {"run": args.run, "providers": "oracle ostium, oracle names",
                         "n_cases": int(len(pred)), "code_version": paths.code_version(),
                         "per_bifurcation": {}}
    print(f"{len(pred)} cases, {args.run} predictions vs delivered GT (ORACLE ostium and names)\n")
    print(f"{'':>10}{'both':>6}{'GT only':>9}{'pred only':>11}{'|diff| median':>15}{'90th':>7}"
          f"{'mean diff':>11}{'GT IQR':>8}")
    for name in angles.BIFURCATION_NAMES:
        g, p = gt[f"{name}_angle_deg"], pred[f"{name}_angle_deg"]
        both = g.notna() & p.notna()
        d = (p - g)[both]
        for cid in gt.index:
            rows.append({"case_id": cid, "bifurcation": name, "gt_deg": g[cid], "pred_deg": p[cid],
                         "diff_deg": p[cid] - g[cid] if both[cid] else np.nan,
                         "pred_reason": pred.loc[cid, f"{name}_reason"]})
        iqr = float(np.subtract(*np.percentile(g.dropna(), [75, 25]))) if g.notna().any() else np.nan
        stats = {"both": int(both.sum()), "gt_only": int((g.notna() & p.isna()).sum()),
                 "pred_only": int((g.isna() & p.notna()).sum()),
                 "abs_diff_median": float(d.abs().median()) if len(d) else None,
                 "abs_diff_p90": float(d.abs().quantile(0.9)) if len(d) else None,
                 "mean_diff": float(d.mean()) if len(d) else None, "gt_iqr": iqr}
        summary["per_bifurcation"][name] = stats
        print(f"  {name:<8}{stats['both']:>6}{stats['gt_only']:>9}{stats['pred_only']:>11}"
              f"{d.abs().median():>15.1f}{d.abs().quantile(0.9):>7.1f}{d.mean():>+11.1f}{iqr:>8.1f}")

    pd.DataFrame(rows).to_csv(pred_dir / "validation.csv", index=False)
    (pred_dir / "validation.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"\nWrote {pred_dir / 'validation.csv'}\n      {pred_dir / 'validation.json'}")


if __name__ == "__main__":
    main()
