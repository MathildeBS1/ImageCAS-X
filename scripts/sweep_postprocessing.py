#!/usr/bin/env python
"""Screen postprocessing variants (postprocessing/variants.py) against an existing
run's saved predictions, without any new GPU inference. CPU only, login-node safe.

    python scripts/sweep_postprocessing.py -c configs/cas_net.json \
        --src cas_net_pretrained --variants size_200,size_500,close_r2 \
        --subset 40 --workers 4

One worker task per scan (not per variant x scan): the prediction, the resampled
GT mask and the GT's own Betti numbers are each loaded/computed once per scan and
reused across every requested variant, since none of that depends on the variant.
Without this, a 14-variant sweep would reload and re-resample the same GT mask 14
times and recompute the same GT Betti numbers 28 times (betti_error_1 and
betti_error_2 each call the eigenvalue-ish label+euler_number pass independently) -
this version calls it once.

Writes one JSON per (variant, scan) under
$ImageCAS_X_results_path/postproc_sweep/<variant>/<scan_id>.json (crash mid-cohort
loses nothing already written) plus postproc_sweep/<variant>/summary.json, and
prints a comparison table across variants at the end.

`--metrics full` adds hd95 and cl_dice (slower); centerline_md/hd95 and the point
metrics are deliberately not included here (they need centerline_samples/ and the
VTK loads that evaluate.py already does well) - run evaluate.py itself on the
winning variant's materialised predictions for the thesis-quality numbers, see
scripts/materialise_variant.py.
"""
import argparse
import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
from tqdm import tqdm

from utils.config import BenchmarkConfig
from utils import io as bio
from utils.metrics import dice, hausdorff_95, cl_dice, _betti_numbers
from postprocessing.variants import VARIANTS
from evaluate import _load_gt_labels


def _scan_all_variants(config_path, src_run, variant_names, scan_id, root,
                       full_metrics, overwrite):
    """One scan, every requested variant. Returns {variant_name: metrics_dict}."""
    out_paths = {v: os.path.join(root, v, f"{scan_id}.json") for v in variant_names}
    cached = {v: json.load(open(p)) for v, p in out_paths.items()
             if os.path.exists(p) and not overwrite}
    todo = [v for v in variant_names if v not in cached]
    if not todo:
        return scan_id, cached

    cfg = BenchmarkConfig.from_json(config_path)
    cfg.validate()
    src_dir = src_run if os.path.isabs(src_run) else os.path.join(cfg.results_root, src_run)
    pred_path = os.path.join(src_dir, "predictions", f"{scan_id}{cfg.data.file_extension}")
    if not os.path.exists(pred_path):
        return scan_id, {v: None for v in variant_names}

    pred, ref_img = bio.load_mask(pred_path)
    spacing = ref_img.GetSpacing()

    gt = _load_gt_labels(cfg, scan_id, ref_img)
    p = cfg.data.params
    if p.get("binarise_lumen", True):
        gt = bio.binarise_lumen(gt, background_label=p.get("background_label", bio.LUMEN_BACKGROUND_LABEL))
    gt_b0, gt_b1 = _betti_numbers(gt)

    out = dict(cached)
    for v in todo:
        mask = VARIANTS[v](pred, spacing)
        b0, b1 = _betti_numbers(mask)
        metrics = dict(
            dice=float(dice(mask, gt)),
            betti_error_1=float(abs(b0 - gt_b0)),
            betti_error_2=float(abs(b1 - gt_b1)),
            n_fg_voxels=int(mask.sum()),
        )
        if full_metrics:
            try:
                metrics["hd95"] = float(hausdorff_95(mask, gt, spacing=spacing))
            except ValueError:
                metrics["hd95"] = float("nan")
            metrics["cl_dice"] = float(cl_dice(mask, gt))
        os.makedirs(os.path.dirname(out_paths[v]), exist_ok=True)
        with open(out_paths[v], "w") as f:
            json.dump(metrics, f, indent=2)
        out[v] = metrics
    return scan_id, out


def _summarise(per_scan: dict) -> dict:
    keys = set()
    for m in per_scan.values():
        if m:
            keys.update(m.keys())
    out = {}
    for k in keys:
        vals = np.array([m[k] for m in per_scan.values() if m and k in m], dtype=float)
        out[k] = dict(mean=float(np.nanmean(vals)) if vals.size else float("nan"),
                       std=float(np.nanstd(vals)) if vals.size else float("nan"),
                       n=int(np.count_nonzero(~np.isnan(vals))))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", default="configs/cas_net.json")
    ap.add_argument("--src", default="cas_net_pretrained", help="run dir holding the predictions to postprocess")
    ap.add_argument("--variants", default="all", help="comma-separated variant names, or 'all'")
    ap.add_argument("--subset", type=int, default=0, help="evaluate only N evenly-spaced test scans (0 = all)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--metrics", choices=["fast", "full"], default="fast")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    cfg = BenchmarkConfig.from_json(args.config)
    cfg.validate()
    scan_ids = list(cfg.data.test_ids)
    if args.subset > 0:
        scan_ids = scan_ids[:: max(1, len(scan_ids) // args.subset)][: args.subset]

    variant_names = list(VARIANTS.keys()) if args.variants == "all" else args.variants.split(",")
    for v in variant_names:
        if v not in VARIANTS:
            raise SystemExit(f"Unknown variant '{v}'. Available: {list(VARIANTS)}")

    full_metrics = args.metrics == "full"
    root = os.path.join(cfg.results_root, "postproc_sweep")

    per_variant_per_scan = {v: {} for v in variant_names}
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futs = [pool.submit(_scan_all_variants, args.config, args.src, variant_names,
                            sid, root, full_metrics, args.overwrite) for sid in scan_ids]
        for fut in tqdm(as_completed(futs), total=len(futs), desc="scans"):
            sid, by_variant = fut.result()
            for v in variant_names:
                per_variant_per_scan[v][sid] = by_variant.get(v)

    metric_keys = ["dice", "betti_error_1", "betti_error_2"] + (["hd95", "cl_dice"] if full_metrics else [])
    all_summaries = {}
    for v in variant_names:
        per_scan = per_variant_per_scan[v]
        n_missing = sum(1 for m in per_scan.values() if m is None)
        summary = _summarise(per_scan)
        summary["n_scans"] = len(scan_ids) - n_missing
        summary["n_missing_predictions"] = n_missing
        with open(os.path.join(root, v, "summary.json"), "w") as f:
            json.dump(summary, f, indent=2)
        all_summaries[v] = summary

    print(f"\n{'variant':<20}" + "".join(f"{k:>16}" for k in metric_keys) + f"{'n':>6}")
    for v, s in all_summaries.items():
        row = f"{v:<20}"
        for k in metric_keys:
            row += f"{s[k]['mean']:16.4f}" if k in s else f"{'--':>16}"
        row += f"{s['n_scans']:6d}"
        print(row)


if __name__ == "__main__":
    main()
