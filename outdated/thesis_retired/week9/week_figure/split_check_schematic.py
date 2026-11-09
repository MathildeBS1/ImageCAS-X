"""Schematic of split_check.py for the week 9 note: one made-up LAD, no patient data.

    python thesis/week9/week_figure/split_check_schematic.py  ->  split_check_schematic.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, FancyBboxPatch

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e4e3df"
SEG = {"pLAD": "#2a78d6", "mLAD": "#eb6834", "dLAD": "#1baf7a"}  # validated categorical order
CUTS = {"pLAD": (0, 22), "mLAD": (22, 54), "dLAD": (54, 110)}  # split boundaries, mm along the trunk
CONTOURS = {"pLAD": (2, 21), "mLAD": (24, 53)}  # contour extent: starts ~2 mm in, ends ~1 mm early
VISUAL = {"pLAD": "plaque", "mLAD": "plaque", "dLAD": "none"}

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "text.color": INK})
fig = plt.figure(figsize=(9, 6.2), facecolor=SURF)
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1], hspace=0.15)

# ---- A: the tree with split boundaries and the Medis contour rings
ax = fig.add_subplot(gs[0]); ax.set_facecolor(SURF)
t = np.linspace(0, 1, 400)
x, y = 110 * t, 18 * np.sin(2.4 * t) - 10 * t ** 2  # a gently curving LAD, mm
s = np.r_[0, np.cumsum(np.hypot(np.diff(x), np.diff(y)))]
s *= 110 / s[-1]
for name, (lo, hi) in CUTS.items():
    m = (s >= lo) & (s <= hi)
    ax.plot(x[m], y[m], color=SEG[name], lw=4, solid_capstyle="round")
    k = np.argmin(abs(s - (lo + hi) / 2))
    ax.text(x[k], y[k] + 5, name, ha="center", color=INK, fontweight="bold")
for b in (22, 54):  # boundaries where the Medis labels change
    k = np.argmin(abs(s - b))
    ax.plot([x[k]] * 2, [y[k] - 4, y[k] + 3], color=INK, lw=1.5)
    ax.text(x[k], y[k] - 7.5, f"label change\n{b} mm", ha="center", va="top", color=INK2, fontsize=8)
ax.plot(x[0], y[0], "o", color=INK, ms=6); ax.text(x[0], y[0] - 5, "LM bifurcation", ha="center", va="top", color=INK2, fontsize=8)
side = np.argmin(abs(s - 22)); ax.plot([x[side], x[side] + 8], [y[side], y[side] + 14], color=MUTED, lw=2)
ax.text(x[side] + 9, y[side] + 14, "D1", color=MUTED, fontsize=8, va="center")
for name, (lo, hi) in CONTOURS.items():  # lumen rings of the Medis contour named after the segment
    for r in np.arange(lo, hi + 0.1, 2.5):
        k = np.argmin(abs(s - r))
        ang = np.degrees(np.arctan2(np.gradient(y)[k], np.gradient(x)[k]))
        ax.add_patch(Ellipse((x[k], y[k]), 1.2, 6, angle=ang, fill=False, ec=SEG[name], lw=1))
ax.text(60, 22, "rings = Medis lumen contours of the pLAD and mLAD files", color=INK2, fontsize=8)
ax.set_title("A  Medis tree split where its labels change; contour rings drawn on top",
             loc="left", fontsize=10, color=INK, fontweight="bold")
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-8, 118); ax.set_ylim(-14, 26)

# ---- B: straightened trunk, contour extents, visual grades, the check
ax = fig.add_subplot(gs[1]); ax.set_facecolor(SURF)
rows = {"split segments": 3, "Medis contours\n(ring centres projected)": 2, "visual analysis\n(BL grade)": 1}
for label, yy in rows.items():
    ax.text(-3, yy, label, ha="right", va="center", color=INK2, fontsize=8.5)
for name, (lo, hi) in CUTS.items():
    ax.add_patch(FancyBboxPatch((lo + 0.4, 2.75), hi - lo - 0.8, 0.5, boxstyle="round,pad=0,rounding_size=0.15",
                                fc=SEG[name], ec="none"))
    ax.text((lo + hi) / 2, 3, name, ha="center", va="center", color="white", fontweight="bold", fontsize=8.5)
    v = VISUAL[name]
    ax.add_patch(FancyBboxPatch((lo + 0.4, 0.75), hi - lo - 0.8, 0.5, boxstyle="round,pad=0,rounding_size=0.15",
                                fc=INK2 if v == "plaque" else SURF, ec=INK2, lw=1))
    ax.text((lo + hi) / 2, 1, v, ha="center", va="center", color="white" if v == "plaque" else INK2, fontsize=8.5)
for name, (lo, hi) in CONTOURS.items():
    ax.plot([lo, hi], [2, 2], color=SEG[name], lw=6, solid_capstyle="butt")
    ax.text((lo + hi) / 2, 2.32, f"{name} contour", ha="center", va="bottom", color=INK, fontsize=8)
for b in (22, 54):
    ax.axvline(b, color=GRID, lw=1, zorder=0)
ax.annotate("", (2, 1.72), (0, 1.72), arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.8))
ax.text(1, 1.55, "+2 mm", ha="center", va="top", color=INK2, fontsize=7.5)
ax.annotate("", (53, 1.72), (54, 1.72), arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.8))
ax.text(53.5, 1.55, "−1 mm", ha="center", va="top", color=INK2, fontsize=7.5)
ax.text(112, 2, "1  contour lies in the split\n   segment of its name?", va="center", color=INK, fontsize=8)
ax.text(112, 1, "2  visual grade of the named\n   and the holding segment agree?", va="center", color=INK, fontsize=8)
ax.set_xlim(-30, 150); ax.set_ylim(0.3, 3.6)
ax.set_xticks([0, 22, 54, 110]); ax.set_xticklabels(["0", "22", "54", "110 mm"], color=INK2, fontsize=8)
ax.tick_params(length=0); [sp.set_visible(False) for sp in ax.spines.values()]
ax.set_yticks([])
ax.set_title("B  Straightened trunk: where each contour falls, and the visual grade of each segment",
             loc="left", fontsize=10, color=INK, fontweight="bold")
fig.savefig(Path(__file__).with_suffix(".png"), dpi=200, bbox_inches="tight", facecolor=SURF)
