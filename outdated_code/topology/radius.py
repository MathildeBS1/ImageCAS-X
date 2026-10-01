"""Lumen radius at centerline points, measured on a mask.

Neither the delivered centerlines nor a predicted one carry a radius, so both are measured the same
way: the distance from each centerline point to the nearest background voxel centre bordering the
lumen. That is the Euclidean distance transform sampled at the point -- the radius of the largest
sphere centred there that stays inside the mask. It over-reads the lumen radius by up to half a
voxel, identically for GT and prediction.

A full distance transform over the cropped volume took ~30 s per case at native resolution;
querying only the boundary voxels with a k-d tree takes about a second.
"""

from __future__ import annotations

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
