#!/usr/bin/env python
"""Turn one postprocessing/variants.py transform into a real run dir, the same shape
evaluate.py already knows how to score: predictions/<id>.nii.gz plus a
postproc_variant_config.json recording what was applied and to what source. Used to
promote a winner from scripts/sweep_postprocessing.py's fast screen to a full
evaluate.py pass (hd95, cl_dice, centerline_md/hd95, volumes, betti, stratified
breakdowns), not just the fast dice/betti sweep metrics.

    python scripts/materialise_variant.py -c configs/cas_net.json \
        --src cas_net_pretrained --variant size_500 -r cas_net_pretrained_size500
    python -m evaluate -c configs/cas_net_size500.json -r cas_net_pretrained_size500

(The second command needs a config whose method_name is unique, e.g. a one-line copy
of cas_net.json with "method_name": "cas_net_size500" -- see configs/cas_net_*.json
for the pattern already used by the Qiu runs.)
"""
import argparse
import json
import os
import time

from utils.config import BenchmarkConfig
from utils import io as bio
from postprocessing.variants import VARIANTS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", default="configs/cas_net.json")
    ap.add_argument("--src", default="cas_net_pretrained")
    ap.add_argument("--variant", required=True, choices=list(VARIANTS))
    ap.add_argument("-r", "--results-dir", required=True)
    ap.add_argument("--split", default="test", choices=("train", "val", "test"))
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    cfg = BenchmarkConfig.from_json(args.config)
    cfg.validate()
    src = args.src if os.path.isabs(args.src) else os.path.join(cfg.results_root, args.src)
    out = args.results_dir if os.path.isabs(args.results_dir) else os.path.join(cfg.results_root, args.results_dir)
    pred_dir = "predictions" if args.split == "test" else f"predictions_{args.split}"
    out_pred_dir = os.path.join(out, pred_dir)
    os.makedirs(out_pred_dir, exist_ok=True)

    ids = getattr(cfg.data, f"{args.split}_ids")
    fn = VARIANTS[args.variant]
    n_done, n_missing = 0, 0
    for sid in ids:
        src_path = os.path.join(src, pred_dir, f"{sid}{cfg.data.file_extension}")
        out_path = os.path.join(out_pred_dir, f"{sid}{cfg.data.file_extension}")
        if not os.path.exists(src_path):
            n_missing += 1
            continue
        if os.path.exists(out_path) and not args.overwrite:
            n_done += 1
            continue
        pred, ref_img = bio.load_mask(src_path)
        mask = fn(pred, ref_img.GetSpacing())
        bio.save_mask(mask, ref_img, out_path)
        n_done += 1

    with open(os.path.join(out, "postproc_variant_config.json"), "w", encoding="utf-8") as f:
        json.dump(dict(variant=args.variant, source_run=src, split=args.split,
                       n_written=n_done, n_missing_source=n_missing,
                       written=time.strftime("%Y-%m-%d %H:%M:%S")), f, indent=2)
    print(f"[materialise] variant={args.variant} src={src} -> {out_pred_dir} "
          f"({n_done} written, {n_missing} missing source predictions)")


if __name__ == "__main__":
    main()
