"""Figure: what "skeletonized to a one-voxel line and Gaussian-smoothed (sigma = 0.5 mm)"
(coronary_tree_graph.tex) actually does to a centerline.

A synthetic curved vessel, not a real case: the point is the two-step operation itself
(voxel-grid thinning, then Gaussian smoothing of the resulting point sequence), which is
the same regardless of which vessel it is run on. Grid spacing is 0.5 mm, matching the
resampled volumes this pipeline actually runs on, so sigma = 0.5 mm is exactly one voxel
of smoothing, same conversion as topology/tortuosity.py's gaussian_filter1d(sigma_mm /
step_mm, ...).

    uv run python scripts/plot_skeleton_smoothing.py

Writes figures/skeleton_smoothing.{pdf,png}.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
from skimage.morphology import skeletonize

GRID = 60
VOXEL_MM = 0.5
SIGMA_MM = 0.5
RADIUS_MM = 2.0

INK = "#1f2933"
MASK = "#c9d1d9"
RAW = "#d83d29"
SMOOTH = "#2a78d6"


def _rasterize_curve():
    t = np.linspace(0, 1, 600)
    cx = 6 + 46 * t**1.6
    cy = 6 + 46 * t**0.6
    grid = np.zeros((GRID, GRID), dtype=bool)
    yy, xx = np.mgrid[0:GRID, 0:GRID]
    r_px = RADIUS_MM / VOXEL_MM
    for x, y in zip(cx, cy):
        grid |= (xx - x) ** 2 + (yy - y) ** 2 <= r_px**2
    return grid


def _order_skeleton(skel):
    ys, xs = np.nonzero(skel)
    pts = list(zip(ys, xs))
    pset = set(pts)
    neighbors = {p: [q for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy, dx) != (0, 0)
                      and (q := (p[0] + dy, p[1] + dx)) in pset] for p in pts}
    start = next(p for p, n in neighbors.items() if len(n) == 1)
    path, seen, cur = [start], {start}, start
    while len(path) < len(pts):
        nxt = next((n for n in neighbors[cur] if n not in seen), None)
        if nxt is None:
            break
        path.append(nxt)
        seen.add(nxt)
        cur = nxt
    return np.array([(x, y) for y, x in path], dtype=float)  # (x, y), voxel units


def main():
    mask = _rasterize_curve()
    skel = skeletonize(mask)
    raw = _order_skeleton(skel)
    smooth = gaussian_filter1d(raw, SIGMA_MM / VOXEL_MM, axis=0, mode="nearest")

    lo, hi = 15, 40  # a stretch spanning the bend, in voxel units, same window for both panels

    # Axes placed at explicit, pre-computed square positions (inches -> figure fraction) rather
    # than through subplots()+set_aspect: matplotlib's aspect='equal'/adjustable='box' resizing
    # is not accounted for by bbox_inches='tight', which leaves a large phantom margin below the
    # panel. Since the data crop is already square, a pre-sized square axes needs no adjustment.
    panel, gap, left_margin, top_margin, bottom_margin = 4.0, 0.5, 0.15, 0.85, 0.15
    fig_w = 2 * panel + gap + 2 * left_margin
    fig_h = panel + top_margin + bottom_margin
    fig = plt.figure(figsize=(fig_w, fig_h))
    axes = [
        fig.add_axes((left_margin / fig_w, bottom_margin / fig_h, panel / fig_w, panel / fig_h)),
        fig.add_axes(((left_margin + panel + gap) / fig_w, bottom_margin / fig_h, panel / fig_w, panel / fig_h)),
    ]
    for ax, title in zip(axes, ("1. skeletonized (one voxel wide)", "2. Gaussian-smoothed, $\\sigma$ = 0.5 mm")):
        ax.imshow(mask, cmap="Greys", alpha=0.35, origin="lower", extent=(0, GRID, 0, GRID), aspect="auto")
        for g in range(lo, hi + 1):
            ax.axvline(g, color="white", lw=0.4, zorder=0)
            ax.axhline(g, color="white", lw=0.4, zorder=0)
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_title(title, fontsize=10.5, color=INK)

    axes[0].plot(raw[:, 0] + 0.5, raw[:, 1] + 0.5, "-o", color=RAW, ms=3, lw=1.6)
    axes[0].text(lo + 0.6, hi - 0.8, "raw skeleton path\n(voxel centers)", color=RAW,
                 fontsize=8.5, ha="left", va="top")
    axes[1].plot(raw[:, 0] + 0.5, raw[:, 1] + 0.5, "-", color=RAW, lw=1.2, alpha=0.4)
    axes[1].plot(smooth[:, 0] + 0.5, smooth[:, 1] + 0.5, "-", color=SMOOTH, lw=2.4)
    axes[1].text(lo + 0.6, hi - 0.8, "raw skeleton (before)", color=RAW, alpha=0.7,
                 fontsize=8.5, ha="left", va="top")
    axes[1].text(lo + 0.6, hi - 2.4, "after Gaussian smoothing", color=SMOOTH,
                 fontsize=8.5, ha="left", va="top")

    fig.suptitle("Skeletonizing a mask to a one-voxel line staircases at bends; smoothing the point\n"
                 "sequence at 1 voxel ($\\sigma$ = 0.5 mm here) removes that grid artifact",
                 fontsize=10.5, color=INK, y=0.99)

    out_dir = os.path.join(os.path.dirname(__file__), "..", "figures")
    os.makedirs(out_dir, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(out_dir, f"skeleton_smoothing.{ext}"), dpi=300, bbox_inches="tight")
    print("wrote figures/skeleton_smoothing.{pdf,png}")


if __name__ == "__main__":
    main()
