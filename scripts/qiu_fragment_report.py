#!/usr/bin/env python
"""How much of CAS-Net's Betti-0 error is real, disconnected vessel versus spurious
false-positive components? Reads a run's reconnection_logs/*.json (any mode: keep2 is
the cheapest way to get this, since it needs no classifier and no GPU) and splits
every removed/kept fragment by gt_fraction, the share of its voxels inside the
(1-voxel dilated) GT lumen, annotated post hoc in reconnect.py and never seen by the
reconnection decision itself.

    python scripts/qiu_fragment_report.py -r cas_net_pretrained_keep2

A fragment counts as "true vessel" if gt_fraction >= --true-fraction (default 0.5).
"Not in GT" includes real vessel beyond where the annotators stopped, so a high
spurious share is evidence, not proof, that CAS-Net is hallucinating structure.
"""
import argparse
import glob
import json
import os

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--results-dir", required=True)
    ap.add_argument("--true-fraction", type=float, default=0.5)
    args = ap.parse_args()

    run = args.results_dir
    if not os.path.isabs(run):
        run = os.path.join(os.environ["ImageCAS_X_results_path"], run)
    paths = sorted(glob.glob(os.path.join(run, "reconnection_logs", "*.json")))
    if not paths:
        raise SystemExit(f"No logs in {run}/reconnection_logs/")

    rows, missing_gt = [], 0
    for p in paths:
        with open(p, encoding="utf-8") as f:
            log = json.load(f)
        sid = log.get("scan_id", os.path.basename(p).removesuffix(".json"))
        for fr in log.get("fragments", []):
            if "gt_fraction" not in fr:
                missing_gt += 1
                continue
            rows.append(dict(scan_id=sid, size_vox=fr["size_vox"],
                             gt_fraction=fr["gt_fraction"], decision=fr["decision"]))

    if missing_gt:
        print(f"[warn] {missing_gt} fragments have no gt_fraction "
              f"(run with --no-gt? re-run without it)")
    if not rows:
        raise SystemExit("No fragments with GT annotation found.")

    size = np.array([r["size_vox"] for r in rows])
    frac = np.array([r["gt_fraction"] for r in rows])
    true_mask = frac >= args.true_fraction
    n_scans = len({r["scan_id"] for r in rows})
    n_scans_with_frag = len({r["scan_id"] for r in rows})

    print(f"{n_scans} scans in {run}, {len(rows)} fragments beyond the main tree(s)\n")
    print(f"{'':>10} {'count':>8} {'  %':>6} {'voxels':>10} {'  %':>6}")
    for name, m in [("true vessel", true_mask), ("spurious", ~true_mask)]:
        print(f"{name:>10} {m.sum():8d} {100*m.mean():6.1f} {int(size[m].sum()):10d} "
              f"{100*size[m].sum()/size.sum():6.1f}")
    print(f"{'total':>10} {len(rows):8d} {100.0:6.1f} {int(size.sum()):10d} {100.0:6.1f}\n")

    by_scan = {}
    for r, t in zip(rows, true_mask):
        d = by_scan.setdefault(r["scan_id"], dict(n_true=0, n_spurious=0, true_vox=0))
        if t:
            d["n_true"] += 1
            d["true_vox"] += r["size_vox"]
        else:
            d["n_spurious"] += 1
    n_scans_all_spurious = sum(1 for d in by_scan.values() if d["n_true"] == 0)
    print(f"scans where every fragment is spurious (keep2 loses nothing real): "
          f"{n_scans_all_spurious}/{n_scans}")

    worst = sorted(by_scan.items(), key=lambda kv: -kv[1]["true_vox"])[:10]
    if worst[0][1]["true_vox"] > 0:
        print("\nworst scans by true-vessel voxels lost to removal:")
        print(f"{'scan':>8} {'true frags':>10} {'true vox':>9} {'spurious frags':>14}")
        for sid, d in worst:
            if d["true_vox"] == 0:
                break
            print(f"{sid:>8} {d['n_true']:10d} {d['true_vox']:9d} {d['n_spurious']:14d}")

    out_path = os.path.join(run, "fragment_report.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dict(true_fraction=args.true_fraction, n_scans=n_scans,
                       n_fragments=len(rows), n_true=int(true_mask.sum()),
                       n_spurious=int((~true_mask).sum()),
                       true_voxels=int(size[true_mask].sum()),
                       spurious_voxels=int(size[~true_mask].sum()),
                       n_scans_all_spurious=n_scans_all_spurious,
                       by_scan={k: v for k, v in by_scan.items()}), f, indent=2)
    print(f"\nWritten to {out_path}")


if __name__ == "__main__":
    main()
