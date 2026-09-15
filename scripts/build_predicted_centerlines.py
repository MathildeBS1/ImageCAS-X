#!/usr/bin/env python
"""Build centerlines from a run's predicted masks, in the delivered file layout.

For every <id>.nii.gz under $ImageCAS_X_results_path/<run>/predictions, topology/skeleton.py
skeletonizes and smooths the mask the way ImageCAS-X built its GT centerlines, and writes
<id>.coronary_{left,right}_centerline.vtk (with a radius array) plus <id>.json (notes).

The ostium and segment names use the ORACLE providers (taken from the GT), so the output isolates
the geometric error of the extraction. It goes to $IMAGECASX_OUT/predicted_centerlines/<run>_oracle,
deliberately not beside the predictions, where evaluate.py would read oracle-labelled centerlines
as if they were a model's own.

Usage:  python scripts/build_predicted_centerlines.py --run cas_net_pretrained [--workers 8]
"""

from __future__ import annotations

import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import nibabel as nib
import numpy as np

from topology import io, paths, skeleton


def _one(case_id: int, pred_path: str, out_dir: str) -> tuple[int, str | None]:
    try:
        img = nib.load(pred_path)
        mask = np.asarray(img.dataobj) > 0
        if not mask.any():
            raise ValueError("empty prediction")
        cls, notes = skeleton.centerlines_from_mask(
            case_id, mask, img.affine, io.load_segmentation(case_id), io.load_centerlines(case_id))
        for side, cl in cls.items():
            skeleton.write_centerline_vtk(cl, Path(out_dir) / f"{case_id}.coronary_{side}_centerline.vtk")
        (Path(out_dir) / f"{case_id}.json").write_text(json.dumps(
            {"prediction": pred_path, "providers": "oracle", "notes": notes}, indent=2) + "\n")
        return case_id, None
    except Exception as exc:  # reported per case, never swallowed
        return case_id, f"{type(exc).__name__}: {exc}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="cas_net_pretrained", help="run dir under $ImageCAS_X_results_path")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--n", type=int, default=0, help="first N predictions only (0 = all)")
    args = ap.parse_args()

    pred_dir = Path(os.environ["ImageCAS_X_results_path"]) / args.run / "predictions"
    out_dir = paths.output_dir(f"predicted_centerlines/{args.run}_oracle")
    # Binary predictions only: "<id>.nii.gz", not "<id>.multi_class.nii.gz" or probability maps.
    preds = [p for p in pred_dir.glob("*.nii.gz") if p.name.split(".")[0].isdigit() and p.name.count(".") == 2]
    preds = sorted(preds, key=lambda p: int(p.name.split(".")[0]))[: args.n or None]
    todo = [p for p in preds if args.overwrite or not (out_dir / f"{p.name.split('.')[0]}.json").exists()]
    print(f"{len(preds)} predictions in {pred_dir}; {len(todo)} to build -> {out_dir}")

    t0, failed = time.time(), []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(_one, int(p.name.split(".")[0]), str(p), str(out_dir)) for p in todo]
        for fut in as_completed(futs):
            cid, err = fut.result()
            if err:
                failed.append((cid, err))
    print(f"done in {time.time() - t0:.0f}s; {len(failed)} failed")
    for cid, err in failed:
        print(f"  case {cid}: {err}")
    (out_dir / "failed.json").write_text(json.dumps(failed, indent=2) + "\n")


if __name__ == "__main__":
    main()
