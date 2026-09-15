"""Candidate postprocessing transforms evaluated in the free-exploration sweep of
2026-09-14/15 (see scripts/sweep_postprocessing.py and
docs_thesis/postprocessing_sweep.md). Each function takes the *already* final mask
from a run's predictions/ dir (i.e. after argmax_binarize +
keep_components_larger_than_100_voxels) plus its native-grid spacing (x, y, z) mm,
and returns a new binary mask of the same shape. Kept separate from
postprocessing/steps.py because these run post hoc over saved predictions, the same
role scripts/qiu_reconnect.py plays, not inside the registry-driven inference-time
pipeline (a step there only ever sees the raw model output once, not a
mask-in-mask-out shape).
"""
import numpy as np
from scipy.ndimage import (label, binary_closing, binary_opening,
                            binary_fill_holes, generate_binary_structure,
                            iterate_structure)


def _keep_components_ge(mask: np.ndarray, min_size: int) -> np.ndarray:
    labeled, n = label(mask, structure=np.ones((3, 3, 3)))
    if n == 0:
        return mask
    sizes = np.bincount(labeled.ravel())
    keep = np.zeros(n + 1, dtype=bool)
    keep[1:] = sizes[1:] >= min_size
    return keep[labeled].astype(np.uint8)


def _keep_top_n(mask: np.ndarray, n_keep: int) -> np.ndarray:
    labeled, n = label(mask, structure=np.ones((3, 3, 3)))
    if n <= n_keep:
        return mask
    sizes = np.bincount(labeled.ravel())
    sizes[0] = 0
    top = np.argsort(sizes)[::-1][:n_keep]
    keep = np.zeros(n + 1, dtype=bool)
    keep[top] = True
    return keep[labeled].astype(np.uint8)


def size_threshold(mask, spacing, min_size=100):
    """Re-apply the connected-component size filter at a different voxel count.
    Strictly stricter than the pipeline default (100) for min_size > 100, since the
    input is already >= 100-voxel components."""
    return _keep_components_ge(mask, int(min_size))


def keep_top_n(mask, spacing, n=2):
    """Keep only the n largest components (n=2 reproduces cas_net_pretrained_keep2's
    rule, included here for a same-code-path cross-check)."""
    return _keep_top_n(mask, int(n))


def morph_close(mask, spacing, radius_vox=1, refilter_min_size=100):
    """Binary closing (dilate then erode) with a solid ball footprint of
    `radius_vox` voxels (isotropic in voxel space; the native grid here is only
    mildly anisotropic, ~0.32-0.43 mm in-plane vs 0.5 mm slice, so a voxel-radius
    ball is close enough to a physical sphere for a screening sweep), then
    re-applied the component size filter since closing can spawn small new debris
    at the boundary of two adjacent structures."""
    struct = iterate_structure(generate_binary_structure(3, 1), int(radius_vox))
    closed = binary_closing(mask.astype(bool), structure=struct)
    return _keep_components_ge(closed.astype(np.uint8), int(refilter_min_size))


def morph_open(mask, spacing, radius_vox=1, refilter_min_size=100):
    """Binary opening (erode then dilate) to strip thin spurious spikes/bridges,
    then re-applied the component size filter (opening can split one component
    into several small ones)."""
    struct = iterate_structure(generate_binary_structure(3, 1), int(radius_vox))
    opened = binary_opening(mask.astype(bool), structure=struct)
    return _keep_components_ge(opened.astype(np.uint8), int(refilter_min_size))


def fill_holes(mask, spacing, refilter_min_size=100):
    """Fill fully enclosed background voxels within the foreground (per connected
    component via the whole-volume flood fill scipy provides), then re-applied the
    size filter (a no-op unless fill_holes itself changes component boundaries,
    which it does not, but kept for a uniform interface)."""
    filled = binary_fill_holes(mask.astype(bool))
    return _keep_components_ge(filled.astype(np.uint8), int(refilter_min_size))


def close_then_keep_top_n(mask, spacing, radius_vox=1, n=2):
    """Closing first (to let a real but disconnected fragment merge into a main
    tree across a small gap), then keep only the top n components (to still drop
    whatever closing did not merge)."""
    struct = iterate_structure(generate_binary_structure(3, 1), int(radius_vox))
    closed = binary_closing(mask.astype(bool), structure=struct).astype(np.uint8)
    return _keep_top_n(closed, int(n))


VARIANTS = {
    "baseline": lambda mask, spacing: mask,
    "size_200": lambda mask, spacing: size_threshold(mask, spacing, 200),
    "size_500": lambda mask, spacing: size_threshold(mask, spacing, 500),
    "size_1000": lambda mask, spacing: size_threshold(mask, spacing, 1000),
    "size_2000": lambda mask, spacing: size_threshold(mask, spacing, 2000),
    "keep_top2": lambda mask, spacing: keep_top_n(mask, spacing, 2),
    "close_r1": lambda mask, spacing: morph_close(mask, spacing, 1),
    "close_r2": lambda mask, spacing: morph_close(mask, spacing, 2),
    "close_r3": lambda mask, spacing: morph_close(mask, spacing, 3),
    "close_r5": lambda mask, spacing: morph_close(mask, spacing, 5),
    "open_r1": lambda mask, spacing: morph_open(mask, spacing, 1),
    "fill_holes": lambda mask, spacing: fill_holes(mask, spacing),
    "close_r2_top2": lambda mask, spacing: close_then_keep_top_n(mask, spacing, 2, 2),
    "close_r3_top2": lambda mask, spacing: close_then_keep_top_n(mask, spacing, 3, 2),
}
