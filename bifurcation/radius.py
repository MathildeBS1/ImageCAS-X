"""Lumen radius at centerline points, measured on a mask.

    python -m bifurcation.radius --split train

Neither the delivered centerlines nor a predicted one carry a radius array, so both are measured
the same way: the distance from each centerline point to the nearest background voxel centre
bordering the lumen. That is the Euclidean distance transform sampled at the point, the radius of
the largest sphere centred there that stays inside the mask. The distance is computed on the union
of the labels, not per label, so an artery boundary never reads as lumen wall.

Two biases to carry into anything built on this. It over-reads by up to half a voxel, identically
for reference and prediction, and the over-read is additive, so it does not cancel in a ratio the
way a scale error does (`knowledge/research_notes/Coronary bifurcation diameter descriptors/
robustness_math_tests.md`). It is also only as good as the vessel is wide: parent calibers agree
between mask and surface methods at ICC 0.87 to 0.95, side branches at 0.58 to 0.73.

A full distance transform over the cropped volume took about 30 s per case at native resolution;
querying only the boundary voxels with a k-d tree takes about a second.
"""

from __future__ import annotations

import argparse
import time

import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree

from . import coords, io, paths


def radius_at(points_lps: np.ndarray, mask: np.ndarray, affine: np.ndarray) -> np.ndarray:
    """Radius (mm) at each (N, 3) LPS point, from a binary mask and its voxel -> RAS affine."""
    mask = np.asarray(mask) > 0
    idx = np.argwhere(mask)
    lo = np.maximum(idx.min(0) - 2, 0)
    hi = np.minimum(idx.max(0) + 3, mask.shape)
    sub = mask[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
    # 26-connected: the nearest background voxel to any interior point touches the mask in that
    # sense, so this shell contains it.
    shell = ndimage.binary_dilation(sub, structure=np.ones((3, 3, 3), bool)) & ~sub
    tree = cKDTree(coords.voxel_to_lps(np.argwhere(shell) + lo, affine))
    dist, _ = tree.query(np.asarray(points_lps, dtype=float))
    return dist


def compute_gt_radius(case_id: int) -> dict[str, np.ndarray]:
    """Radius for both delivered centerlines of a case, measured on its GT mask, and cached."""
    seg = io.load_segmentation(case_id)
    out = {}
    for side in ("left", "right"):
        cl = io.load_centerline(case_id, side)
        r = radius_at(cl.points, seg.labels > 0, seg.affine)
        path = paths.radius_cache_path(case_id, side)
        path.parent.mkdir(parents=True, exist_ok=True)
        np.save(path, r.astype(np.float32))
        out[side] = r
    return out


def cache_split(split: str, overwrite: bool = False) -> None:
    """Fill the radius cache for one split, one .npy per centerline, and log what failed."""
    ids, fails, t0 = paths.split_ids(split), [], time.time()
    done = 0
    for case in ids:
        if not overwrite and all(paths.radius_cache_path(case, s).exists() for s in ("left", "right")):
            continue
        try:
            compute_gt_radius(case)
            done += 1
        except Exception as e:  # a missing or unreadable file: record it, never drop it silently
            fails.append((case, repr(e)))
    paths.RADIUS.mkdir(parents=True, exist_ok=True)
    (paths.RADIUS / f"{split}_failed.txt").write_text("".join(f"{c}\t{r}\n" for c, r in fails))
    print(f"{split}: {len(ids)} cases, {done} computed, {len(fails)} failures, {time.time() - t0:.0f} s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="train", choices=["train", "val", "test"])
    ap.add_argument("--overwrite", action="store_true", help="recompute cases already cached")
    a = ap.parse_args()
    cache_split(a.split, a.overwrite)
