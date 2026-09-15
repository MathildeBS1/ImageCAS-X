#!/usr/bin/env python
"""Choose Qiu's evaluation threshold on the val split, not the test split.

Qiu et al. accept a join when mean P along the stitched path + mean P along the
fragment reaches "a predefined threshold (e.g., 1)" raised by two ADF p-values. That
threshold is tied to their classifier's calibration, so it is re-chosen here for ours.

Protocol:
  1. CAS-Net predictions for the val split (jobs/infer_eval_cas_net.sh with SPLIT=val).
  2. A reject-everything reconnection pass over them, so that every candidate of every
     fragment is walked and logged from the same unmodified state:
         python scripts/qiu_reconnect.py -c configs/cas_net_qiu.json --split val \
             --src cas_net_pretrained_val -r cas_net_pretrained_val_qiu_calib \
             --set eval_threshold=99
  3. This script replays the acceptance rule over a threshold grid, with and without
     the ADF penalty, and scores each setting with RecAcc (Qiu eq. 15) against GT:
         python scripts/qiu_calibrate_threshold.py -r cas_net_pretrained_val_qiu_calib

Replaying is exact for a fragment's own decision (its first candidate, in logged order,
whose walk reached and whose score clears the bar), but it ignores two second-order
effects of accepting a join: type-1 fragment-to-fragment merges, and later rounds
joining onto tips that an accepted fragment brought with it. Only type-2/3 attempts
are replayed.
"""
import argparse
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def replay(logs: list, threshold: float, use_adf: bool, true_fraction: float,
           path_fraction: float) -> dict:
    c = dict(tp=0, fp=0, tn=0, fn=0)
    for l in logs:
        by_label = {}
        for a in l.get("attempts", []):
            if len(a["labels"]) == 1:
                by_label.setdefault(a["labels"][0], []).append(a)
        for fr in l.get("fragments", []):
            true = fr["gt_fraction"] >= true_fraction
            chosen = None
            for a in by_label.get(fr["label"], []):
                if a["walk"] != "reached":
                    continue
                bar = threshold + (a["adf_p_prob"] + a["adf_p_grey"] if use_adf else 0.0)
                if a["score"] >= bar:
                    chosen = a
                    break
            if chosen is None:
                c["fn" if true else "tn"] += 1
            else:
                ok = true and chosen.get("path_in_gt_fraction", 0.0) >= path_fraction
                c["tp" if ok else "fp"] += 1
    n = sum(c.values())
    div = lambda a, b: float(a / b) if b else float("nan")  # noqa: E731
    return dict(c, threshold=round(float(threshold), 4), use_adf=use_adf,
                rec_acc=div(c["tp"] + c["tn"], n), rec_sen=div(c["tp"], c["tp"] + c["fn"]),
                rec_spe=div(c["tn"], c["tn"] + c["fp"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--results-dir", required=True,
                    help="The reject-everything val run (absolute, or under $ImageCAS_X_results_path).")
    ap.add_argument("--true-fraction", type=float, default=0.5)
    ap.add_argument("--path-fraction", type=float, default=0.8)
    args = ap.parse_args()

    run = args.results_dir
    if not os.path.isabs(run):
        run = os.path.join(os.environ["ImageCAS_X_results_path"], run)
    with open(os.path.join(run, "reconnection_config.json"), encoding="utf-8") as f:
        rc = json.load(f)
    if rc.get("split") == "test":
        sys.exit("Refusing to calibrate on the test split.")
    if rc["params"].get("eval_threshold", 1.0) < 10:
        print("[warn] this run accepted some joins, so later candidates of accepted fragments "
              "were never tried; rerun with --set eval_threshold=99 for an exact replay.")

    logs = []
    for p in sorted(glob.glob(os.path.join(run, "reconnection_logs", "*.json"))):
        with open(p, encoding="utf-8") as f:
            logs.append(json.load(f))
    if not logs or any("gt_fraction" not in fr for l in logs for fr in l.get("fragments", [])):
        sys.exit("Logs are missing or carry no GT annotation (was --no-gt used?).")
    n_frag = sum(len(l.get("fragments", [])) for l in logs)
    n_true = sum(fr["gt_fraction"] >= args.true_fraction for l in logs for fr in l["fragments"])
    print(f"{len(logs)} scans, {n_frag} fragments, {n_true} of them true vessel "
          f"(>= {args.true_fraction:.0%} in GT lumen)")

    rows = [replay(logs, t, adf, args.true_fraction, args.path_fraction)
            for adf in (True, False) for t in np.arange(0.0, 2.0001, 0.05)]
    print(f"\n{'ADF':>4} {'thr':>5} {'TP':>4} {'FP':>4} {'TN':>4} {'FN':>4} "
          f"{'RecAcc':>7} {'RecSen':>7} {'RecSpe':>7}")
    for r in rows:
        print(f"{'on' if r['use_adf'] else 'off':>4} {r['threshold']:5.2f} {r['tp']:4d} {r['fp']:4d} "
              f"{r['tn']:4d} {r['fn']:4d} {r['rec_acc']:7.3f} {r['rec_sen']:7.3f} {r['rec_spe']:7.3f}")

    # Highest RecAcc; ties go to the higher threshold, i.e. the more conservative bar.
    best = {adf: max((r for r in rows if r["use_adf"] == adf),
                     key=lambda r: (r["rec_acc"], r["threshold"])) for adf in (True, False)}
    paper = {adf: next(r for r in rows if r["use_adf"] == adf and abs(r["threshold"] - 1.0) < 1e-9)
             for adf in (True, False)}
    out = dict(run=run, n_scans=len(logs), n_fragments=n_frag, n_true_fragments=int(n_true),
               true_fraction=args.true_fraction, path_fraction=args.path_fraction,
               best_with_adf=best[True], best_without_adf=best[False],
               paper_threshold_with_adf=paper[True], paper_threshold_without_adf=paper[False],
               grid=rows)
    with open(os.path.join(run, "threshold_calibration.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nbest with ADF:    thr {best[True]['threshold']:.2f}  RecAcc {best[True]['rec_acc']:.3f}")
    print(f"best without ADF: thr {best[False]['threshold']:.2f}  RecAcc {best[False]['rec_acc']:.3f}")
    print(f"paper (1.0, ADF): RecAcc {paper[True]['rec_acc']:.3f}")
    print(f"\nWritten to {os.path.join(run, 'threshold_calibration.json')}. Put the chosen "
          f"threshold (and use_adf) into configs/cas_net_qiu.json before the test run.")


if __name__ == "__main__":
    main()
