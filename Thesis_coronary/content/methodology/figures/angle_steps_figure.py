"""Figure for Section sec:method-angle (fig:method-angle, replaces bifurcation_angle_figure.py on 2026-11-19):
the bifurcation angle, in the style of surface_cut_figure.py, without panel letters (user).

    python Thesis_coronary/content/methodology/figures/angle_steps_figure.py

A made-up left main bifurcation in one plane with unevenly spaced, gently curving centerlines (no patient
data), run through the real code of CGPS_data/thesis_final/bifurcation_angle.py (DEPTHS, point_at_depth,
artery_direction, lm_angle). Panels, left to right: the lumen and centerlines with the points every 0.5 mm
5 to 10 mm from O; close-up of the least-squares line through each set of points (dashed back towards O) and the unit vectors
u_LAD and u_LCx pointing away from the bifurcation; the two unit vectors from one point, the angle theta
between them and its formula. Style and colours as the Technical Background illustrations
(illus_hazard_area.py). Writes angle_steps_figure.{pdf,png} next to this file.
"""
import sys
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import Arc, FancyBboxPatch, Polygon

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "CGPS_data" / "thesis_final"))
sys.path.insert(0, str(ROOT / "Thesis_coronary" / "setup"))
from bifurcation_angle import DEPTHS, artery_direction, lm_angle, point_at_depth  # noqa: E402
from figure_colours import INK, INK2, MUTED, PALETTE  # noqa: E402

MAIN, SECOND, THIRD = PALETTE[3], PALETTE[1], PALETTE[2]  # purple, pink, green, as illus_hazard_area.py

mpl.rcParams.update({
    "font.family": "serif", "font.serif": ["cmr10"],
    "mathtext.fontset": "cm", "axes.unicode_minus": False, "axes.formatter.use_mathtext": True,
    "font.size": 10, "text.color": INK, "pdf.fonttype": 42,
})


def tint(hex_, a):
    c = np.array(to_rgb(hex_))
    return tuple(1 - a * (1 - c))


def darken(hex_, a=0.3):
    c = np.array(to_rgb(hex_))
    return tuple((1 - a) * c + a * np.array(to_rgb(INK)))


LAD_COL, CX_COL, LM_COL, ANG_COL = MAIN, darken(SECOND), INK2, THIRD
DASH = (0, (3, 2.5))
AX = dict(arrowstyle="-|>,head_length=0.55,head_width=0.16", lw=0.6, color=INK, shrinkA=0, shrinkB=0)
rng = np.random.default_rng(7)


# ---------------------------------------------------------------- made-up bifurcation
def vessel(start, heading0, bend, length):
    """Planar centerline from start: heading (deg) changing by bend (deg/mm), unevenly spaced steps."""
    steps = rng.uniform(0.3, 1.0, 200)
    steps = steps[np.cumsum(steps) <= length]
    h = np.radians(heading0 + bend * np.r_[0, np.cumsum(steps)][:-1])
    Y = np.vstack([start, start + np.cumsum(np.c_[np.cos(h), np.sin(h)] * steps[:, None], axis=0)])
    Y = np.c_[Y, np.zeros(len(Y))]
    return Y, np.r_[0, np.cumsum(np.linalg.norm(np.diff(Y, axis=0), axis=1))]


O = np.zeros(2)
lad, s_lad = vessel(O, 32, -2.6, 22)
cx, s_cx = vessel(O, -70, 3.0, 20)
lm, _ = vessel(O, 168, -0.6, 11)
theta = lm_angle((lad, s_lad), (cx, s_cx))
u_lad, u_cx = artery_direction(lad, s_lad), artery_direction(cx, s_cx)
pts = {n: np.array([point_at_depth(Y, s, d) for d in DEPTHS]) for n, (Y, s) in (("LAD", (lad, s_lad)), ("LCx", (cx, s_cx)))}


def band(Y, r):
    """Outline of a lumen of radius r around the planar centerline Y (for drawing only)."""
    t = np.gradient(Y[:, :2], axis=0)
    t /= np.linalg.norm(t, axis=1)[:, None]
    nrm = np.c_[-t[:, 1], t[:, 0]]
    return np.vstack([Y[:, :2] + r * nrm, (Y[:, :2] - r * nrm)[::-1]])


# ---------------------------------------------------------------- layout
W, H = 6.3, 2.5
fig = plt.figure(figsize=(W, H))
L, R, GAP = 0.015, 0.985, 0.02
widths = (0.40, 0.33, 0.27)  # shares of the width available to the panels
avail = R - L - 2 * GAP
PB, PT = 0.02, 0.98
bg = fig.add_axes([0, 0, 1, 1], zorder=-5)
bg.set_axis_off(); bg.set_xlim(0, 1); bg.set_ylim(0, 1)
x0s = L + np.r_[0, np.cumsum(np.array(widths[:-1]) * avail + GAP)]
for k, (x0, w) in enumerate(zip(x0s, widths)):
    bg.add_patch(FancyBboxPatch((x0, PB), w * avail, PT - PB, transform=fig.transFigure,
                 boxstyle="round,pad=0,rounding_size=0.02", fc=tint(MUTED, 0.08),
                 ec=tint(MUTED, 0.30), lw=0.8, mutation_aspect=W / H))


def panel(k, pad=0.02, bottom=0.06, top=0.06):
    return fig.add_axes([x0s[k] + pad, PB + bottom, widths[k] * avail - 2 * pad, PT - PB - bottom - top])


def dot(ax, q, ms=3.5, col=INK, z=5):
    ax.plot(q[0], q[1], "o", ms=ms, color=col, mec="white", mew=0.6, zorder=z)


# A: lumen, centerlines and the points 5 to 10 mm from O
ax = panel(0)
ax.set_axis_off(); ax.set_aspect("equal")
for Y, r, col in ((lm, 2.0, LM_COL), (lad, 1.6, LAD_COL), (cx, 1.3, CX_COL)):
    ax.add_patch(Polygon(band(Y, r), closed=True, fc=tint(col, 0.14), ec="none", zorder=0))
    ax.plot(Y[:, 0], Y[:, 1], color=col, lw=1.2, zorder=2)
for n, col in (("LAD", LAD_COL), ("LCx", CX_COL)):
    ax.plot(pts[n][:, 0], pts[n][:, 1], "o", ms=2.6, color=col, mec="white", mew=0.4, zorder=4)
dot(ax, O)
ax.text(-0.6, 1.4, r"$O$", ha="center", va="bottom")
ax.text(*(lad[-1, :2] + [0.6, 0.0]), "LAD", color=LAD_COL, ha="left", va="center", fontsize=9)
ax.text(*(cx[-1, :2] + [0.6, 0.0]), "LCx", color=CX_COL, ha="left", va="center", fontsize=9)
ax.text(*(lm[-1, :2] + [0.0, 2.4]), "LM", color=LM_COL, ha="center", va="bottom", fontsize=9)
for n, side in (("LAD", 1), ("LCx", 1)):
    a, b = pts[n][0, :2], pts[n][-1, :2]
    nrm = np.array([-(b - a)[1], (b - a)[0]]) / np.linalg.norm(b - a) * side
    ax.text(*((a + b) / 2 + (2.6 if n == "LAD" else 5.0) * nrm), "5 to 10 mm", ha="center", va="center", fontsize=7.5, color=INK2)
ax.set_xlim(-12, 26); ax.set_ylim(-19, 13)

# B: close-up, the fitted lines and the unit vectors
ax = panel(1)
ax.set_axis_off(); ax.set_aspect("equal")
for (Y, s), n, u, col, lab in (((lad, s_lad), "LAD", u_lad, LAD_COL, r"$\mathbf{u}_{\mathrm{LAD}}$"),
                               ((cx, s_cx), "LCx", u_cx, CX_COL, r"$\mathbf{u}_{\mathrm{LCx}}$")):
    near = s <= 12
    ax.plot(Y[near, 0], Y[near, 1], color=tint(col, 0.45), lw=1.0, zorder=1)
    c = pts[n].mean(axis=0)
    t0, t1 = (pts[n][0] - c) @ u, (pts[n][-1] - c) @ u
    tO = (np.r_[O, 0] - c) @ u
    ax.plot(*np.array([c + t * u for t in (t0 - 0.4, t1 + 0.4)])[:, :2].T, color=col, lw=1.4, zorder=3)
    ax.plot(*np.array([c + t * u for t in (tO, t0 - 0.4)])[:, :2].T, color=col, lw=0.8, ls=DASH, zorder=2)
    ax.plot(pts[n][:, 0], pts[n][:, 1], "o", ms=2.8, color=col, mec="white", mew=0.4, zorder=4)
    tip = c + (t1 + 0.4) * u
    ax.annotate("", xy=(tip + 3.2 * u)[:2], xytext=tip[:2], arrowprops=dict(AX, lw=0.9, color=col), zorder=5)
    ax.text(*(tip + 3.6 * u)[:2] + np.array([0.3, 0.9 if n == "LAD" else -0.9]), lab, color=col,
            ha="left", va="center", fontsize=9)
dot(ax, O)
ax.text(-0.5, 0.7, r"$O$", ha="right", va="bottom")
ax.set_xlim(-2.5, 17); ax.set_ylim(-16.5, 9.5)

# C: the angle between the two unit vectors
ax = panel(2, bottom=0.08, top=0.08)
ax.set_axis_off(); ax.set_aspect("equal")
for u, col in ((u_lad, LAD_COL), (u_cx, CX_COL)):
    ax.annotate("", xy=u[:2], xytext=(0, 0), arrowprops=dict(AX, lw=1.0, color=col), zorder=3)
a1, a2 = np.degrees(np.arctan2(u_cx[1], u_cx[0])), np.degrees(np.arctan2(u_lad[1], u_lad[0]))
ax.add_patch(Arc((0, 0), 0.7, 0.7, theta1=a1, theta2=a2, color=ANG_COL, lw=1.2, zorder=2))
mid = np.radians((a1 + a2) / 2)
ax.text(0.5 * np.cos(mid), 0.5 * np.sin(mid), r"$\theta$", ha="center", va="center", fontsize=11)
dot(ax, (0, 0), ms=3)
ax.text(0.5, -1.25, r"$\theta = \arccos(\mathbf{u}_{\mathrm{LAD}} \cdot \mathbf{u}_{\mathrm{LCx}})$",
        ha="center", va="top", fontsize=8)
ax.set_xlim(-0.35, 1.35); ax.set_ylim(-1.75, 0.95)

out = Path(__file__).with_suffix("")
fig.savefig(f"{out}.pdf")
fig.savefig(f"{out}.png", dpi=200)
print(f"theta = {theta:.1f} deg")
