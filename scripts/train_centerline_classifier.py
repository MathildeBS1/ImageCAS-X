#!/usr/bin/env python
"""Train the centerline classifier P of Qiu et al. 2025 (eq. 7) on the train split.

Sampling follows their section 4.2: every centerline voxel of a scan (N, capped at
--max-centerline), 2N voxels from the lumen off the centerline, and 2N from outside
the lumen within 7 of their voxels of the wall (2.8 mm at their ~0.4 mm), so about
1:4 positive to negative. Centerline voxels are the dataset's own centerline VTKs
rasterised onto the 0.5 mm grid, kept only where they fall inside the GT lumen so no
voxel carries both labels.

Features come from the 0.5 mm volume cache, in the benchmark's HU window, exactly as
postprocessing/qiu/reconnect.py queries P at walk time.

    python scripts/train_centerline_classifier.py -c configs/cas_net_qiu.json [--workers 16]

Writes <results>/<centerline_classifier.dir>/model.joblib and report.json. Val-split
scans are sampled the same way and only scored, to report how separable P is before
anything depends on it.
"""
import argparse
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import joblib
import numpy as np
from scipy import ndimage as ndi

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from postprocessing.qiu.classifier import CascadeForest, normalise_hu, patch_features  # noqa: E402
from utils import io as bio  # noqa: E402
from utils.config import BenchmarkConfig  # noqa: E402
from utils.seeding import SEED  # noqa: E402

GRID_MM = 0.5
DEFAULTS = dict(dir="qiu_centerline_classifier", n_train_scans=40, n_val_scans=10,
                max_centerline_per_scan=1000, outside_shell_mm=2.8,
                n_trees=100, max_layers=5, min_samples_leaf=1)


def sample_scan(args: tuple) -> dict:
    scan_id, data_root, cfg_data, max_cl, shell_mm, seed = args
    rng = np.random.default_rng(seed)
    vol = np.load(os.path.join(data_root, "volumes_resampled", f"{scan_id}.npy"), mmap_mode="r")
    seg = np.load(os.path.join(data_root, "segmentations_resampled", f"{scan_id}.npy"), mmap_mode="r")
    header = bio.read_image_geometry(bio.resolve_scan_path(
        os.path.join(data_root, cfg_data["volume_dir"]), scan_id, cfg_data["volume_suffix"]))
    geom = bio.resampled_geometry(header, GRID_MM)
    if tuple(geom.GetSize()) != vol.shape:
        raise ValueError(f"{scan_id}: 0.5 mm geometry {geom.GetSize()} != cache {vol.shape}")

    branches = []
    for side in ("left", "right"):
        path = os.path.join(data_root, "centerlines", f"{scan_id}.coronary_{side}_centerline.vtk")
        if os.path.exists(path):
            branches += bio.load_vtk_centerline_branches(path)
    lumen_full = np.asarray(seg) > 0
    cl_full = bio.centerline_points_to_mask(branches, geom).astype(bool) & lumen_full

    margin = int(np.ceil(shell_mm / GRID_MM)) + 8
    nz = np.argwhere(lumen_full)
    lo = np.maximum(nz.min(0) - margin, 0)
    hi = np.minimum(nz.max(0) + margin + 1, np.array(vol.shape))
    sl = tuple(slice(a, b) for a, b in zip(lo, hi))
    lumen, cl = lumen_full[sl], cl_full[sl]
    outside_d = ndi.distance_transform_edt(~lumen, sampling=GRID_MM)

    pools = {
        "centerline": np.argwhere(cl),
        "lumen_off_centerline": np.argwhere(lumen & ~cl),
        "outside_shell": np.argwhere(~lumen & (outside_d <= shell_mm)),
    }
    n = min(len(pools["centerline"]), max_cl)
    take = {"centerline": n, "lumen_off_centerline": 2 * n, "outside_shell": 2 * n}
    pts, y, region = [], [], []
    for r, (name, pool) in enumerate(pools.items()):
        k = min(take[name], len(pool))
        pts.append(pool[rng.choice(len(pool), size=k, replace=False)])
        y.append(np.full(k, int(name == "centerline")))
        region.append(np.full(k, r))
    pts = np.concatenate(pts)
    X = patch_features(normalise_hu(np.asarray(vol[sl])), pts)
    return dict(scan_id=scan_id, X=X, y=np.concatenate(y), region=np.concatenate(region))


def collect(ids, cfg, params, workers, seed_offset) -> dict:
    data = dict(volume_dir=cfg.data.volume_dir, volume_suffix=cfg.data.volume_suffix)
    jobs = [(sid, cfg.data.data_root, data, params["max_centerline_per_scan"],
             params["outside_shell_mm"], SEED + seed_offset + i) for i, sid in enumerate(ids)]
    out, failed = [], []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for sid, fut in zip(ids, [pool.submit(sample_scan, j) for j in jobs]):
            try:
                out.append(fut.result())
                print(f"  sampled {sid}: {len(out[-1]['y'])} points", flush=True)
            except Exception as e:
                failed.append({"scan_id": sid, "error": str(e)})
                print(f"  [warn] {sid} failed: {e}", flush=True)
    if not out:
        raise RuntimeError("no scan could be sampled")
    return dict(X=np.concatenate([o["X"] for o in out]), y=np.concatenate([o["y"] for o in out]),
                region=np.concatenate([o["region"] for o in out]),
                ids=[o["scan_id"] for o in out], failed=failed)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", required=True)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out-dir", default=None,
                    help="Absolute output dir; defaults to <results>/<centerline_classifier.dir>.")
    for k in ("n_train_scans", "n_val_scans", "max_centerline_per_scan", "n_trees", "max_layers"):
        ap.add_argument(f"--{k.replace('_', '-')}", type=int, default=None)
    args = ap.parse_args()

    with open(args.config, encoding="utf-8") as f:
        params = {**DEFAULTS, **json.load(f).get("centerline_classifier", {})}
    for k in ("n_train_scans", "n_val_scans", "max_centerline_per_scan", "n_trees", "max_layers"):
        if getattr(args, k) is not None:
            params[k] = getattr(args, k)
    cfg = BenchmarkConfig.from_json(args.config)
    out_dir = args.out_dir or os.path.join(cfg.results_root, params["dir"])
    os.makedirs(out_dir, exist_ok=True)

    rng = np.random.default_rng(SEED)
    train_ids = sorted(rng.choice(cfg.data.train_ids, params["n_train_scans"], replace=False).tolist())
    val_ids = sorted(rng.choice(cfg.data.val_ids, params["n_val_scans"], replace=False).tolist())
    print(f"[classifier] train scans: {len(train_ids)}, val scans: {len(val_ids)} -> {out_dir}")

    t0 = time.time()
    train = collect(train_ids, cfg, params, args.workers, 0)
    val = collect(val_ids, cfg, params, args.workers, 10_000)
    t_sample = time.time() - t0
    print(f"[classifier] {len(train['y'])} train / {len(val['y'])} val samples, "
          f"positive fraction {train['y'].mean():.3f}", flush=True)

    model = CascadeForest(n_trees=params["n_trees"], max_layers=params["max_layers"],
                          min_samples_leaf=params["min_samples_leaf"], random_state=SEED)
    t0 = time.time()
    model.fit(train["X"], train["y"])
    t_fit = time.time() - t0

    from sklearn.metrics import roc_auc_score
    prob = model.predict_proba(val["X"])[:, 1]
    pred = (prob > 0.5).astype(int)
    yv = val["y"]
    region_names = ["centerline", "lumen_off_centerline", "outside_shell"]
    report = dict(
        params=params, train_ids=train["ids"], val_ids=val["ids"],
        failed=train["failed"] + val["failed"],
        n_train=int(len(train["y"])), n_val=int(len(yv)),
        n_layers=len(model.layers), layer_oob_accuracy=model.layer_oob_accuracy,
        val_accuracy=float((pred == yv).mean()),
        val_sensitivity=float(pred[yv == 1].mean()),
        val_specificity=float(1 - pred[yv == 0].mean()),
        val_auc=float(roc_auc_score(yv, prob)),
        val_mean_p_by_region={n: float(prob[val["region"] == r].mean())
                              for r, n in enumerate(region_names)},
        seconds_sampling=round(t_sample, 1), seconds_fit=round(t_fit, 1),
    )
    joblib.dump(model, os.path.join(out_dir, "model.joblib"), compress=3)
    with open(os.path.join(out_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(json.dumps({k: v for k, v in report.items() if k not in ("train_ids", "val_ids")},
                     indent=2))


if __name__ == "__main__":
    main()
