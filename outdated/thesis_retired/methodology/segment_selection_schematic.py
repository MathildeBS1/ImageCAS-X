"""Schematic for Section sec:method-population-segments: from the 17 graded segments to the 9 trunk segments.

    python thesis/methodology/segment_selection_schematic.py

A made-up coronary tree in anterior view (no patient data), drawn three times:
A, all segments of the visual analysis; B, the LAD, LCx and RCA kept; C, those three cut into
proximal, mid and distal at the landmarks of tab:method-segments (02b_segment_split.tex).
Writes segment_selection_schematic.pdf next to this file. Thesis style: serif, white, no title.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#dcdbd6", "white"
GREY = "#a9a8a3"  # panel A: every segment equal
PMD = ("#2a78d6", "#eb6834", "#1baf7a")  # proximal / mid / distal, as in split_example_figure.py

plt.rcParams.update({"font.family": "serif", "font.serif": ["STIX Two Text", "STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix", "font.size": 9, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF})


def curve(*pts, n=300):
    """Catmull-Rom spline through pts, resampled to n points equally spaced in arc length."""
    P = np.array(pts, float)
    P = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    t = np.linspace(0, 1, 60)[:, None]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1:i + 3]
        out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    X = np.vstack(out)
    s = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]
    u = np.linspace(0, s[-1], n)
    return np.c_[np.interp(u, s, X[:, 0]), np.interp(u, s, X[:, 1])]


def at(C, f):
    """Point and unit tangent at arc-length fraction f of curve C."""
    k = min(int(round(f * (len(C) - 1))), len(C) - 2)
    d = C[k + 1] - C[k]
    return C[k], d / np.hypot(*d)


def part(C, a, b):
    return C[int(round(a * (len(C) - 1))):int(round(b * (len(C) - 1))) + 1]


def branch(C, f, *rel):
    """Side branch leaving C at fraction f, through offsets rel from its origin."""
    p, _ = at(C, f)
    return curve(p, *(p + np.array(r) for r in rel), n=120)


# ---- the tree (patient's right on the viewer's left)
BIF = np.array([6.2, 8.0])  # LM bifurcation
LM = curve([5.55, 8.75], [5.95, 8.45], BIF)
LAD = curve(BIF, [5.9, 6.6], [6.0, 4.6], [6.5, 2.6], [7.4, 0.6])
LCX = curve(BIF, [7.6, 8.4], [9.0, 8.0], [9.8, 6.6], [9.9, 4.4])
RCA = curve([4.45, 8.7], [3.3, 8.4], [2.1, 7.3], [1.5, 5.3], [1.7, 3.2], [2.8, 1.8], [4.3, 1.35])
CRUX = RCA[-1]
F = {"D1": 0.27, "D2": 0.56, "OM1": 0.40, "OM2": 0.72, "AM": 0.68}  # landmark fractions along each artery
SIDE = {
    "D1": branch(LAD, F["D1"], [0.7, -0.3], [1.5, -0.8]),
    "D2": branch(LAD, F["D2"], [0.65, -0.3], [1.35, -0.85]),
    "IM": curve(BIF, [6.85, 7.35], [7.2, 6.75], n=120),
    "OM1": branch(LCX, F["OM1"], [-0.3, -0.7], [-0.7, -1.5]),
    "OM2": branch(LCX, F["OM2"], [-0.3, -0.7], [-0.8, -1.4]),
    "PDA": curve(CRUX, [5.2, 0.95], [6.0, 0.6], n=120),
    "PLA": curve(CRUX, [4.9, 1.9], [5.5, 2.3], n=120),
}
CUTS = {"LAD": (LAD, F["D1"], F["D2"]), "LCx": (LCX, F["OM1"], F["OM2"]), "RCA": (RCA, F["AM"] / 2, F["AM"])}

# label anchors (fraction along the piece) and offsets for panel A
LABELS_A = [
    ("LM", LM, 0.5, (0.1, 0.42)), ("IM", SIDE["IM"], 0.5, (0.42, 0.12)),
    ("pLAD", LAD, F["D1"] / 2, (-0.62, 0.0)), ("mLAD", LAD, (F["D1"] + F["D2"]) / 2, (-0.68, 0.0)),
    ("dLAD", LAD, 0.8, (0.62, 0.05)),
    ("D1", SIDE["D1"], 1.0, (0.2, -0.25)), ("D2", SIDE["D2"], 1.0, (0.3, -0.12)),
    ("pLCx", LCX, F["OM1"] / 2, (0.0, 0.4)), ("mLCx", LCX, (F["OM1"] + F["OM2"]) / 2, (0.62, 0.12)),
    ("dLCx", LCX, (F["OM2"] + 1) / 2, (0.6, 0.0)),
    ("OM1", SIDE["OM1"], 1.0, (-0.1, -0.3)), ("OM2", SIDE["OM2"], 1.0, (-0.1, -0.3)),
    ("pRCA", RCA, F["AM"] / 4, (0.0, 0.4)), ("mRCA", RCA, 3 * F["AM"] / 4, (-0.62, 0.0)),
    ("dRCA", RCA, (F["AM"] + 1) / 2, (-0.4, -0.38)),
    ("PDA", SIDE["PDA"], 1.0, (0.1, -0.32)), ("PLA", SIDE["PLA"], 1.0, (0.3, 0.25)),
]
ARTERY_LABELS = (("LAD", LAD, 0.45, (-1.15, 0.0)), ("LCx", LCX, 0.15, (0.1, 0.45)),
                 ("RCA", RCA, 0.4, (1.15, 0.0)))


def draw(ax, C, color, lw, z=2):
    ax.plot(*C.T, color=color, lw=lw, solid_capstyle="round", zorder=z)


def tick(ax, C, f, half=0.2, color=INK, lw=1.0):
    p, d = at(C, f)
    n = np.array([-d[1], d[0]]) * half
    ax.plot(*np.c_[p - n, p + n], color=color, lw=lw, solid_capstyle="butt", zorder=4)


def aorta(ax):
    ax.add_patch(plt.matplotlib.patches.FancyBboxPatch((4.25, 8.6), 1.5, 1.35,
                 boxstyle="round,pad=0,rounding_size=0.35", fc="#f1f0ec", ec=GRID, lw=0.8, zorder=1))
    ax.text(5.0, 9.35, "aorta", ha="center", va="center", color=MUTED, fontsize=7.5, style="italic")


def label(ax, txt, C, f, off, color=INK, size=7.5, **kw):
    p, _ = at(C, f)
    ax.text(p[0] + off[0], p[1] + off[1], txt, ha="center", va="center", color=color, fontsize=size, **kw)


fig, axes = plt.subplots(1, 3, figsize=(6.3, 2.9), gridspec_kw={"wspace": 0.16})
for ax in axes:
    ax.set_xlim(0.2, 10.9)
    ax.set_ylim(-0.2, 10.1)
    ax.set_aspect("equal")
    ax.axis("off")
    aorta(ax)
TRUNK, BR = 2.4, 1.5

# A: the visual analysis, all segments equal
ax = axes[0]
for C in (LM, LAD, LCX, RCA):
    draw(ax, C, GREY, TRUNK)
for C in SIDE.values():
    draw(ax, C, GREY, BR)
for C, a, b in CUTS.values():
    tick(ax, C, a, color=INK2, lw=0.8)
    tick(ax, C, b, color=INK2, lw=0.8)
for txt, C, f, off in LABELS_A:
    label(ax, txt, C, f, off, size=6.8)

# B: the three arteries kept, the rest faded
ax = axes[1]
for C in [LM, *SIDE.values()]:
    draw(ax, C, GRID, BR, z=1)
for name, C, f, off in ARTERY_LABELS:
    draw(ax, C, INK, TRUNK + 0.4)
    label(ax, name, C, f, off, size=8.5, fontweight="bold", fontfamily="STIXGeneral")

# C: proximal / mid / distal at the landmarks
ax = axes[2]
for C in [LM, *SIDE.values()]:
    draw(ax, C, GRID, BR, z=1)
for name, (C, a, b) in CUTS.items():
    for (lo, hi), col in zip(((0, a), (a, b), (b, 1)), PMD):
        draw(ax, part(C, lo, hi), col, TRUNK + 0.4)
    for f in (a, b):
        tick(ax, C, f, half=0.26, color=SURF, lw=2.2)  # surface gap at the cut
for txt, C, f, off in [r for r in LABELS_A if r[0] in ("D1", "D2", "OM1", "OM2", "PDA")]:
    label(ax, txt, C, f, off, color=MUTED, size=6.8)
p, d = at(RCA, F["AM"])
ax.annotate("acute\nmargin", p, (p[0] + 0.75, p[1] + 0.05), ha="left", va="center", fontsize=6.8, color=MUTED,
            arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.6, "shrinkA": 1, "shrinkB": 3})
for name, C, f, off in ARTERY_LABELS:
    label(ax, name, C, f, off, size=8.5, fontweight="bold", fontfamily="STIXGeneral")
ax.legend(handles=[Line2D([], [], color=c, lw=2.8, label=l) for c, l in zip(PMD, ("proximal", "mid", "distal"))],
          loc="upper center", bbox_to_anchor=(0.5, 0.03), ncol=3, frameon=False, fontsize=7.5, handlelength=1.2,
          handletextpad=0.4, columnspacing=0.8, borderaxespad=0)

for ax, letter, sub in zip(axes, "ABC", ("17 segments graded", "3 arteries kept", "9 trunk segments")):
    ax.text(0.0, 1.0, letter, transform=ax.transAxes, fontweight="bold", fontfamily="STIXGeneral", fontsize=11, va="top", color=INK)
    ax.text(0.5, -0.14, sub, transform=ax.transAxes, ha="center", va="top", color=INK2, fontsize=8.5)
for left, right in zip(axes[:-1], axes[1:]):
    x0 = left.get_position().x1
    x1 = right.get_position().x0
    fig.add_artist(plt.matplotlib.patches.FancyArrowPatch(
        (x0 - 0.005, 0.5), (x1 + 0.01, 0.5), transform=fig.transFigure, arrowstyle="-|>",
        mutation_scale=9, color=INK2, lw=0.9))

fig.savefig(Path(__file__).with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.03)
