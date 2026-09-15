#!/usr/bin/env python
"""Compare evaluate.py results across run dirs, paired per scan.

    python scripts/compare_runs.py cas_net_pretrained cas_net_pretrained_qiu
    python scripts/compare_runs.py cas_net_pretrained cas_net_pretrained_keep2 \
        cas_net_pretrained_qiu cas_net_pretrained_qiu_noremove

The first run dir is the baseline; every other run is reported both as a bare
summary (mean +/- std over its own scans) and as a paired delta against the
baseline, matched scan by scan. The paired delta is the number that matters: two
runs' summary means can differ just because one run covers a slightly different
set of scans (a scan qiu_reconnect.py could not process, e.g.), whereas pairing
by scan id cancels out per-scan difficulty and isolates the postprocessing effect.

Reads <results>/<run>/*_results.json (evaluate.py's output, whatever its
method_name prefix) and, if present, <results>/<run>/reconnection_summary.json
for RecAcc/RecSen/RecSpe and the fragment/voxel counts qiu_reconnect.py logs.
"""
import argparse
import glob
import json
import os
import sys

import numpy as np

# "higher"/"lower"/"zero" is better; a metric missing here prints with no verdict.
_DIRECTION = {
    "dice": "higher",
    "cl_dice": "higher",
    "local_dice": "higher",
    "hd95": "lower",
    "betti_error_1": "lower",
    "betti_error_2": "lower",
    "centerline_md": "lower",
    "centerline_hd95": "lower",
    "volume_mad_ml": "lower",
    "volume_bias_ml": "zero",
}


def _load(results_root: str, run: str):
    run_dir = run if os.path.isabs(run) else os.path.join(results_root, run)
    matches = glob.glob(os.path.join(run_dir, "*_results.json"))
    if not matches:
        sys.exit(f"No *_results.json in {run_dir} -- has evaluate.py run for this run yet?")
    if len(matches) > 1:
        sys.exit(f"Ambiguous, multiple *_results.json in {run_dir}: {matches}")
    with open(matches[0], encoding="utf-8") as f:
        results = json.load(f)
    recon = None
    recon_path = os.path.join(run_dir, "reconnection_summary.json")
    if os.path.exists(recon_path):
        with open(recon_path, encoding="utf-8") as f:
            recon = json.load(f)
    return run_dir, results, recon


def _mean_std(summary_entry: dict) -> str:
    return f"{summary_entry['mean']:.3f} +/- {summary_entry['std']:.3f}"


def _verdict(direction: str, delta_mean: float) -> str:
    if direction == "higher":
        return "better" if delta_mean > 0 else ("worse" if delta_mean < 0 else "tie")
    if direction == "lower":
        return "better" if delta_mean < 0 else ("worse" if delta_mean > 0 else "tie")
    if direction == "zero":
        return "closer to 0" if abs(delta_mean) < 1e-9 else ("toward 0" if delta_mean != 0 else "tie")
    return ""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+",
                     help="Run dirs under $ImageCAS_X_results_path; the first is the baseline.")
    ap.add_argument("--metrics", nargs="*", default=None,
                     help="Restrict to these summary metrics (default: every metric common "
                          "to all runs).")
    args = ap.parse_args()

    results_root = os.environ.get("ImageCAS_X_results_path")
    if not results_root:
        sys.exit("ImageCAS_X_results_path is not set -- source env.sh first.")
    if len(args.runs) < 2:
        sys.exit("Need at least a baseline and one run to compare it against.")

    loaded = [_load(results_root, r) for r in args.runs]
    names = args.runs
    baseline_dir, baseline_results, _ = loaded[0]

    metric_names = args.metrics or sorted(baseline_results["summary"].keys())
    for _, res, _ in loaded:
        metric_names = [m for m in metric_names if m in res["summary"]]

    print(f"Baseline: {names[0]}  ({baseline_dir})")
    for name, (run_dir, res, _) in zip(names, loaded):
        cov = res["coverage"]
        tag = "  <-- baseline" if name == names[0] else ""
        print(f"  {name:<32} {cov['n_evaluated']}/{cov['n_test_ids']} scans scored, "
              f"{cov['n_missing_predictions']} missing{tag}")

    print("\n== Summary (own scans, not paired) ==")
    col_w = 20
    header = f"{'metric':<18}{'dir':<7}" + "".join(f"{n:<{col_w}}" for n in names)
    print(header)
    print("-" * len(header))
    for metric in metric_names:
        direction = _DIRECTION.get(metric, "")
        row = f"{metric:<18}{direction:<7}"
        for _, res, _ in loaded:
            row += f"{_mean_std(res['summary'][metric]):<{col_w}}"
        print(row)

    for name, (run_dir, res, _) in zip(names[1:], loaded[1:]):
        common = sorted(set(baseline_results["per_scan"]) & set(res["per_scan"]))
        print(f"\n== {name} vs {names[0]}, paired over {len(common)} scans ==")
        d_header = f"{'metric':<18}{'dir':<7}{'delta mean +/- std':<24}{'verdict':<14}n"
        print(d_header)
        print("-" * len(d_header))
        for metric in metric_names:
            direction = _DIRECTION.get(metric, "")
            diffs = [res["per_scan"][sid][metric] - baseline_results["per_scan"][sid][metric]
                     for sid in common
                     if metric in res["per_scan"].get(sid, {})
                     and metric in baseline_results["per_scan"].get(sid, {})]
            if not diffs:
                print(f"{metric:<18}{direction:<7}{'no paired scans':<24}")
                continue
            d_mean, d_std = float(np.mean(diffs)), float(np.std(diffs))
            verdict = _verdict(direction, d_mean)
            print(f"{metric:<18}{direction:<7}{f'{d_mean:+.3f} +/- {d_std:.3f}':<24}"
                  f"{verdict:<14}{len(diffs)}")

    recon_runs = [(n, recon) for n, (_, _, recon) in zip(names, loaded) if recon is not None]
    if recon_runs:
        print("\n== Reconnection summary (fragments = extra components beyond the 2 main trees) ==")
        r_header = (f"{'run':<32}{'frag_tot':>9}{'attached':>9}{'removed':>9}"
                     f"{'rec_acc':>9}{'rec_sen':>9}{'rec_spe':>9}")
        print(r_header)
        print("-" * len(r_header))
        for name, recon in recon_runs:
            rvg = recon.get("reconnection_vs_gt", {})
            print(f"{name:<32}{recon.get('fragments_total', 0):>9}"
                  f"{recon.get('fragments_attached', 0):>9}{recon.get('fragments_removed', 0):>9}"
                  f"{rvg.get('rec_acc', float('nan')):>9.3f}"
                  f"{rvg.get('rec_sen', float('nan')):>9.3f}"
                  f"{rvg.get('rec_spe', float('nan')):>9.3f}")


if __name__ == "__main__":
    main()
