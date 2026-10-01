"""Figure: one tortuosity index, many different vessels.

Six synthetic centerlines share the same chord D and the same arc length L, so
they share the same tortuosity index tau = L / D, yet they bend in different
places, by different amounts and in different planes. Each is coloured by its
local curvature on one shared scale, and annotated with the metrics from
discover_tortuosity.py that do tell them apart.

    uv run python scripts/make_tortuosity_ambiguity.py

Writes figures/tortuosity_ambiguity.{pdf,png}. Upload the PDF to
content/background/figures/ in Overleaf.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize
from scipy.optimize import brentq

CHORD_MM = 40.0          # straight-line distance between the segment's ends
TAU = 1.25               # target tortuosity index, shared by every curve
N_SAMPLES = 4000
KAPPA_MAX_SHOWN = 0.5    # colour scale ceiling, 1/mm; anything above saturates

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
INK = "#1f2933"
MUTED = "#7b8794"
# One hue, light to dark: low curvature recedes, sharp bends stand out.
CMAP = LinearSegmentedColormap.from_list("kappa", ["#b9d3ee", "#4a7fc1", "#0b2e6b"])


def bump(center, width):
    return lambda s: np.exp(-((s - center) / width) ** 2)


# Each shape is a unit profile along the chord, scaled by an amplitude that is
# solved for so the arc length comes out at TAU * CHORD_MM. s runs 0..1.
SHAPES = [
    ("Single bend (C)", lambda s: (np.sin(np.pi * s), 0 * s)),
    ("Double bend (S)", lambda s: (np.sin(2 * np.pi * s), 0 * s)),
    ("Many small bends", lambda s: (np.sin(6 * np.pi * s), 0 * s)),
    ("Proximal bend", lambda s: (bump(0.25, 0.11)(s), 0 * s)),
    ("Distal bend", lambda s: (bump(0.75, 0.11)(s), 0 * s)),
    ("Helix (out of plane)",
     lambda s: (np.sin(4 * np.pi * s), 1 - np.cos(4 * np.pi * s))),
]


def build(profile, amplitude):
    s = np.linspace(0.0, 1.0, N_SAMPLES)
    y, z = profile(s)
    return np.column_stack([s * CHORD_MM, amplitude * y, amplitude * z])


def arc_length(points):
    return np.linalg.norm(np.diff(points, axis=0), axis=1).sum()


def solve_amplitude(profile):
    target = TAU * CHORD_MM
    return brentq(lambda a: arc_length(build(profile, a)) - target, 1e-3, CHORD_MM)


def metrics(points):
    """Curvature, inflections and planarity, as in discover_tortuosity."""
    d1 = np.gradient(points, axis=0)
    d2 = np.gradient(d1, axis=0)
    cross = np.cross(d1, d2)
    speed = np.linalg.norm(d1, axis=1)
    kappa = np.linalg.norm(cross, axis=1) / speed ** 3
    # Planar curves: an inflection is a sign change of the in-plane curvature.
    signed = cross[:, 2]
    signed = signed[np.abs(signed) > 1e-6 * np.abs(signed).max()]
    inflections = int(np.sum(np.diff(np.sign(signed)) != 0))
    centered = points - points.mean(axis=0)
    eig = np.sort(np.linalg.eigvalsh(np.cov(centered.T)))
    return {
        "kappa": kappa,
        "kappa_max": kappa[5:-5].max(),
        "inflections": inflections,
        "planar": eig[0] / eig.sum() < 1e-6,
    }


def segments(points):
    return np.stack([points[:-1], points[1:]], axis=1)


def draw_view(ax, xy, colours, label=None):
    """One 2D view of a centerline: chord, curvature-coloured curve, end points."""
    start, end = xy[0], xy[-1]
    ax.plot([start[0], end[0]], [start[1], end[1]], ls=(0, (3, 2)),
            lw=0.8, color=MUTED, zorder=1)
    ax.add_collection(LineCollection(segments(xy), colors=colours, linewidths=2.2,
                                     capstyle="round", zorder=2))
    ax.plot(*start, "o", ms=5, color=INK, zorder=3)
    ax.plot(*end, "o", ms=5, mfc="white", mec=INK, mew=1.2, zorder=3)
    if label:
        ax.text(CHORD_MM / 2, start[1] - 3.5, label, ha="center", va="top",
                fontsize=7, color=MUTED)


def annotate(ax, m):
    shape_line = ("planar" if m["planar"] else "out of plane")
    if m["planar"]:
        shape_line += f", {m['inflections']} inflection" + ("s" if m["inflections"] != 1 else "")
    text = (f"$\\tau = {TAU:.2f}$\n"
            f"$\\kappa_{{max}} = {m['kappa_max']:.2f}$ mm$^{{-1}}$\n"
            f"{shape_line}")
    ax.text(0.5, -0.02, text, transform=ax.transAxes, ha="center", va="top",
            fontsize=8, color=INK, linespacing=1.4)


def main():
    plt.rcParams.update({"font.size": 9, "font.family": "sans-serif"})
    norm = Normalize(0.0, KAPPA_MAX_SHOWN)
    fig = plt.figure(figsize=(6.6, 5.0))
    grid = fig.add_gridspec(2, 3, left=0.02, right=0.98, top=0.93, bottom=0.2,
                            wspace=0.08, hspace=0.75)

    for i, (title, profile) in enumerate(SHAPES):
        points = build(profile, solve_amplitude(profile))
        assert abs(arc_length(points) / CHORD_MM - TAU) < 1e-3
        m = metrics(points)
        colours = CMAP(norm(np.clip(m["kappa"][:-1], 0, KAPPA_MAX_SHOWN)))
        start, end = points[0], points[-1]
        row, col = divmod(i, 3)
        letter = "abcdef"[i]

        ax = fig.add_subplot(grid[row, col])
        if m["planar"]:
            draw_view(ax, points[:, [0, 1]], colours)
        else:
            # Two orthogonal projections of the same curve: a single 2D view
            # (as in a C-/S-shape reading) sees only one of them.
            draw_view(ax, points[:, [0, 2]] + [0, 6], colours, label="side view")
            draw_view(ax, points[:, [0, 1]] + [0, -9], colours, label="top view")
        ax.set_xlim(-3, CHORD_MM + 3)
        ax.set_ylim(-17, 20)
        ax.set_aspect("equal")
        ax.axis("off")
        if i == 0:
            ax.text(start[0], start[1] - 3, "proximal", ha="center", va="top",
                    fontsize=7, color=MUTED)
            ax.text(end[0], end[1] - 3, "distal", ha="center", va="top",
                    fontsize=7, color=MUTED)
            ax.text(CHORD_MM / 2, -2.5, "$D$", ha="center", va="top",
                    fontsize=8, color=MUTED)
            ax.plot([0, 10], [-10, -10], color=INK, lw=1.2)
            ax.text(5, -11, "10 mm", ha="center", va="top", fontsize=7, color=INK)

        ax.set_title(f"({letter}) {title}", fontsize=9, color=INK, pad=2)
        annotate(ax, m)

    cax = fig.add_axes([0.3, 0.07, 0.4, 0.022])
    bar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=CMAP), cax=cax,
                       orientation="horizontal", extend="max")
    bar.set_label("local curvature $\\kappa$ (mm$^{-1}$)", fontsize=8, color=INK)
    bar.ax.tick_params(labelsize=7, colors=INK, length=2)
    bar.outline.set_visible(False)

    os.makedirs(OUT_DIR, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT_DIR, f"tortuosity_ambiguity.{ext}"), dpi=300)
    print("wrote figures/tortuosity_ambiguity.{pdf,png}")


if __name__ == "__main__":
    main()
