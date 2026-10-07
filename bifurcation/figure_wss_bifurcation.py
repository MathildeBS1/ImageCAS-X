"""Schematic WSS map on a bifurcation for clinical_background_v2/03_wall_shear_stress.tex.

A simplified redraw of the bifurcation surface in Shen et al. (2026) Fig. 6a, keeping its shape:
a parent entering from the top splits into two daughters, and the left daughter splits again.
Coloured by WSS in the rainbow of Griffo et al. The field is drawn by hand, not simulated: high on
each flow divider, low on the lateral walls just past each split, intermediate elsewhere, as the
section describes. Only the first bifurcation is labelled; the second repeats the pattern.

    python -m bifurcation.figure_wss_bifurcation

Writes figures/wss_bifurcation.{pdf,png}.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from scipy import ndimage
from scipy.interpolate import CubicSpline
from scipy.spatial import cKDTree

from tortuosity import paths
from tortuosity.figure_transformer import RAINBOW
from tortuosity.figure_turning_angle import INK, MUTED, save

# Centerlines traced from the original panel, in its pixel frame (y down). Each daughter starts at
# its junction with the parent's radius and tapers to its own.
J1, J2 = (246, 268), (172, 352)
SEGMENTS = {  # name: (points, radius at start, radius at end, side of the lateral wall)
    "parent": ([(252, -90), (249, 90), (247, 180), J1], 48, 48, 0),
    "right": ([J1, (300, 340), (365, 450), (420, 560), (468, 660), (515, 760)], 48, 42, -1),
    "left": ([J1, (215, 320), J2], 48, 40, +1),
    "side": ([J2, (110, 365), (40, 372), (-200, 378)], 40, 29, +1),
    "down": ([J2, (140, 420), (100, 510), (62, 640), (35, 760)], 40, 38, -1),
}
DIVIDERS = [(J1, (249, 347)), (J2, (103, 392))]  # junction, and roughly where its crotch is


def segment(pts, r0, r1, n=800):
    """Points along a spline through pts, their radius, and the arc length from the first point."""
    pts = np.array(pts, float)
    cs = CubicSpline(np.arange(len(pts)), pts, bc_type="natural")
    t = np.linspace(0, len(pts) - 1, n)
    C = cs(t)
    arc = np.r_[0, np.cumsum(np.linalg.norm(np.diff(C, axis=0), axis=1))]
    r = r1 + (r0 - r1) * np.clip(1 - arc / 90, 0, 1) ** 2  # taper from the parent radius
    return C, r, arc


def main():
    nx, ny = 820, 940
    x, y = np.meshgrid(np.linspace(-120, 560, nx), np.linspace(-60, 720, ny))
    X = np.c_[x.ravel(), y.ravel()]

    # Signed distance to each segment's wall; their union, blurred, fillets every junction and
    # rounds the crotches into flow dividers without moving the straight walls.
    walls, S = [], {}
    for name, (P, r0, r1, wall) in SEGMENTS.items():
        C, R, arc = segment(P, r0, r1)
        d, i = cKDTree(C).query(X)
        S[name] = s = d - R[i]
        if wall:
            j = np.clip(i, 1, len(C) - 2)
            T, off = C[j + 1] - C[j - 1], X - C[j]
            side = np.sign(T[:, 0] * off[:, 1] - T[:, 1] * off[:, 0]) == wall
            lw = np.exp(-((arc[i] - 70) / 35) ** 2) * np.clip(d / R[i], 0, 1) ** 1.2 * side
        else:
            lw = np.zeros(len(X))
        walls.append((name, s, lw))
    sd = ndimage.gaussian_filter(np.min(list(S.values()), axis=0).reshape(ny, nx), 12).ravel()
    inside = sd < 0
    owner = np.argmin([w[1] for w in walls], axis=0)  # each pixel belongs to its nearest segment
    low = ndimage.gaussian_filter(np.choose(owner, [w[2] for w in walls]).reshape(ny, nx), 6).ravel()

    # Each flow divider is the wall point nearest its junction, within 35 degrees of the crotch.
    apexes = []
    for J, g in DIVIDERS:
        u = (np.array(g) - J) / np.linalg.norm(np.array(g) - J)
        rel = X - J
        dist = np.linalg.norm(rel, axis=1)
        cone = (~inside) & (rel @ u > np.cos(np.radians(35)) * dist)
        apexes.append(X[cone][dist[cone].argmin()])
    high = sum(np.exp(-((X - a) ** 2).sum(1) / (2 * 12 ** 2)) for a in apexes)
    v = np.clip(.3 + .7 * high - .3 * low, 0, 1)

    depth = np.clip(-sd / 30, 0, 1)
    shade = .45 + .55 * np.sqrt(depth * (2 - depth))
    rgba = RAINBOW(v)
    rgba[:, :3] *= shade[:, None]
    rgba[:, 3] = inside

    fig, ax = plt.subplots(figsize=(4.6, 4.6))
    fig.subplots_adjust(0, 0, 1, 1)
    ax.imshow(rgba.reshape(ny, nx, 4), extent=(-120, 560, 720, -60), interpolation="bilinear")
    ax.contour(x, y, sd.reshape(ny, nx), levels=[0], colors=INK, linewidths=.8)
    ax.set_xlim(-190, 690), ax.set_ylim(660, -140), ax.set_aspect("equal"), ax.axis("off")

    ax.add_patch(FancyArrowPatch((253, -130), (253, -70), arrowstyle="-|>", mutation_scale=9, lw=1.4, color=INK))
    ax.text(272, -105, "flow", ha="left", va="center", fontsize=9, color=INK)
    lab = dict(fontsize=8.5, color=INK, va="center", ha="center")
    line = dict(arrowstyle="-", color=MUTED, lw=.8)
    tip = {n: X[inside & (owner == k_)][lw[inside & (owner == k_)].argmax()]
           for k_, (n, _, lw) in enumerate(walls) if lw.any()}
    # Only the first bifurcation is labelled; the second repeats the same pattern.
    for text, at, t in (("lateral wall\nlow, oscillating WSS", (-70, 190), tip["left"]),
                        ("lateral wall\nlow, oscillating WSS", (560, 300), tip["right"]),
                        ("flow divider\nhigh WSS", (245, 545), apexes[0])):
        ax.annotate(text, t, at, arrowprops=line, **lab)

    cax = fig.add_axes([.64, .9, .28, .022])
    cb = fig.colorbar(plt.cm.ScalarMappable(cmap=RAINBOW), cax=cax, orientation="horizontal", ticks=[0, 1])
    cb.ax.set_xticklabels(["low", "high"], fontsize=8, color=INK)
    cb.outline.set_linewidth(.5)
    cb.set_label("WSS", fontsize=8.5, color=INK, labelpad=1)
    save(fig, os.path.join(paths.FIGURES, "wss_bifurcation"))


if __name__ == "__main__":
    main()
