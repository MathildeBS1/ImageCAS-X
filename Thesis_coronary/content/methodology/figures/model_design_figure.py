"""Figure for Section sec:method-models (fig:method-models, 2026-11-23): the two association models on the tree.

    python Thesis_coronary/content/methodology/figures/model_design_figure.py

A made-up planar coronary tree (no patient data, nothing computed), drawn twice. The arteries are tapered tubes with
a wall edge and shading (2026-11-23, user: "more volume ... look like real arteries ... draw a plaque in them and
have the centerlines run inside"); each centerline runs inside its lumen; short side branches and the aortic root in
grey. Segment boundaries sit at fixed fractions of each artery, for drawing only.
Panels, left to right (no letters, as the feature figures):
- Bifurcation model: close-up of the LM bifurcation. The proximal LAD and proximal LCx in their artery colours on a
  grey area that marks the one outcome per participant, the rest of the arteries grey; the angle theta at O, the two
  daughter diameters behind a, and a plaque on the wall of the proximal LAD.
- Curvature model: the LAD, LCx and RCA divided into proximal, mid and distal segments (series colours), the LM grey;
  thin lines join the nine segments to one participant intercept b_i; a plaque on the wall of the mid LAD.
Style and colours as angle_steps_figure.py. Writes model_design_figure.{pdf,png} next to this file.
"""
import sys
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import Arc, Circle, FancyBboxPatch, Polygon

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "Thesis_coronary" / "setup"))
from figure_colours import INK, INK2, MUTED, PALETTE, SERIES  # noqa: E402

MAIN, SECOND, THIRD = PALETTE[3], PALETTE[1], PALETTE[2]  # purple, pink, green, as angle_steps_figure.py

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
SEG_COL = (darken(SERIES[0], 0.15), darken(SERIES[1], 0.15), SERIES[2])  # proximal, mid, distal
GREY = tint(MUTED, 0.45)
PLAQUE = tint(SERIES[0], 0.45)  # light yellow, as plaque on the wall
LIGHT = np.array([-0.45, 0.89])  # direction of the light for the shading


# ---------------------------------------------------------------- made-up tree
def vessel(start, heading0, bends, length, r0, r1, step=0.25):
    """Planar centerline from start: heading (deg) changing by bends(s) deg per unit of length s; radius r0 to r1."""
    s = np.arange(0, length + step / 2, step)
    h = np.radians(heading0 + np.cumsum(bends(s)) * step)
    Y = start + np.r_[[[0, 0]], np.cumsum(np.c_[np.cos(h), np.sin(h)][:-1] * step, axis=0)]
    return Y, s, r0 + (r1 - r0) * s / s[-1]


def tangent_deg(Y, i):
    t = Y[min(i + 1, len(Y) - 1)] - Y[max(i - 1, 0)]
    return np.degrees(np.arctan2(t[1], t[0]))


O = np.array([9.0, -2.0])
lm = vessel(np.array([0.0, 0.0]), -12, lambda s: 0 * s, np.linalg.norm(O), 2.3, 2.2)
lad = vessel(O, -60, lambda s: -0.30 + 0.8 * np.sin(s / 7), 58, 1.9, 0.8)
cx = vessel(O, 6, lambda s: -1.9 + 1.0 * np.sin(s / 5), 40, 1.7, 0.8)
rca = vessel(np.array([-6.0, 0.5]), -172, lambda s: 3.4 * np.exp(-((s - 20) / 14) ** 2) + 0.4 * np.sin(s / 6), 62,
             2.0, 0.9)
ARTERIES = {"LAD": lad, "LCx": cx, "RCA": rca}
FRACS = {"LAD": (0.32, 0.66), "LCx": (0.40, 0.72), "RCA": (0.34, 0.68)}


def side_branch(parent, s0, turn, length, bend=0.0):
    Y, s, r = parent
    i = int(np.searchsorted(s, s0))
    return vessel(Y[i], tangent_deg(Y, i) + turn, lambda t: bend + 0 * t, length, 0.8 * r[i], 0.45)


# side branches at the segment boundaries, where the landmark method places them
BRANCHES = [side_branch(lad, FRACS["LAD"][0] * 58, -38, 11, 1.0), side_branch(lad, FRACS["LAD"][1] * 58, -35, 8, 1.2),
            side_branch(cx, FRACS["LCx"][0] * 40, -50, 8, -1.0), side_branch(rca, FRACS["RCA"][1] * 62, 55, 10, 1.5)]


def parts(name):
    """The proximal, mid and distal pieces (Y, r) of an artery, overlapping by one point so they join."""
    Y, s, r = ARTERIES[name]
    k = [0] + [int(np.searchsorted(s, f * s[-1])) for f in FRACS[name]] + [len(s) - 1]
    return [(Y[k[j]:k[j + 1] + 1], r[k[j]:k[j + 1] + 1]) for j in range(3)]


def normals(Y):
    t = np.gradient(Y, axis=0)
    t /= np.linalg.norm(t, axis=1)[:, None]
    return np.c_[-t[:, 1], t[:, 0]]


def band(Y, r):
    """Outline of a lumen of radius r (number or one per point) around the planar centerline Y."""
    n = normals(Y) * np.reshape(r, (-1, 1))
    return np.vstack([Y + n, (Y - n)[::-1]])


def normal(Y, i):
    return normals(Y)[i]


def tube_edge(ax, Y, r, col, ew):
    """The wall: a slightly wider dark band drawn below every fill, so junctions merge cleanly."""
    ax.add_patch(Polygon(band(Y, r + ew), closed=True, fc=col, ec="none", zorder=1))
    ax.add_patch(Circle(Y[-1], r[-1] + ew, fc=col, ec="none", zorder=1))


def tube_fill(ax, Y, r, col):
    """The lumen, shaded as a cylinder lit from LIGHT: a base tone, a lighter core and a highlight."""
    n = normals(Y)
    lit = (n @ LIGHT)[:, None] * n
    K = 9
    for k in range(K):  # nested bands, each narrower, lighter and shifted towards the light
        f, a, shift = 1 - 0.85 * k / K, 0.50 - 0.44 * k / (K - 1), 0.45 * k / (K - 1)
        C = Y + shift * r[:, None] * lit
        ax.add_patch(Polygon(band(C, f * r), closed=True, fc=tint(col, a), ec="none", zorder=2 + 0.01 * k))
        if k == 0:
            ax.add_patch(Circle(Y[-1], r[-1], fc=tint(col, a), ec="none", zorder=2))


def centerline(ax, Y, col, lw=0.8):
    ax.plot(Y[:, 0], Y[:, 1], color=col, lw=lw, solid_capstyle="round", zorder=5)


def plaque(ax, Y, s, r, s0, s1, side=-1, hmax=0.6):
    """A plaque on one wall between s0 and s1, narrowing the lumen by up to hmax of the radius."""
    k = (s >= s0) & (s <= s1)
    Yk, rk, nk = Y[k], r[k], side * normals(Y)[k]
    h = hmax * rk * np.sin(np.pi * (s[k] - s0) / (s1 - s0)) ** 1.4
    P = np.vstack([Yk + nk * rk[:, None], (Yk + nk * (rk - h)[:, None])[::-1]])
    ax.add_patch(Polygon(P, closed=True, fc=PLAQUE, ec=darken(SERIES[0], 0.25), lw=0.6, zorder=4))


# ---------------------------------------------------------------- layout
W, H = 6.3, 2.75
fig = plt.figure(figsize=(W, H))
L, R, GAP = 0.015, 0.985, 0.02
widths = (0.5, 0.5)
avail = R - L - GAP
PB, PT = 0.02, 0.98
bg = fig.add_axes([0, 0, 1, 1], zorder=-5)
bg.set_axis_off(); bg.set_xlim(0, 1); bg.set_ylim(0, 1)
x0s = L + np.r_[0, widths[0] * avail + GAP]
for x0, w in zip(x0s, widths):
    bg.add_patch(FancyBboxPatch((x0, PB), w * avail, PT - PB, transform=fig.transFigure,
                 boxstyle="round,pad=0,rounding_size=0.02", fc=tint(MUTED, 0.08),
                 ec=tint(MUTED, 0.30), lw=0.8, mutation_aspect=W / H))


def panel(k, xlim, ylim, pad=0.02, bottom=0.03, top=0.03):
    ax = fig.add_axes([x0s[k] + pad, PB + bottom, widths[k] * avail - 2 * pad, PT - PB - bottom - top])
    ax.set_axis_off(); ax.set_aspect("equal")
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    return ax


def dot(ax, q, ms=3.5, col=INK, z=7):
    ax.plot(q[0], q[1], "o", ms=ms, color=col, mec="white", mew=0.6, zorder=z)


def heading(Y, i):
    d = Y[i] - Y[0]
    return np.degrees(np.arctan2(d[1], d[0]))


EDGE_GREY = tint(MUTED, 0.62)

# left: bifurcation model, close-up of the LM bifurcation
ax = panel(0, (-3, 33), (-27, 4))
EW = 0.22
(pl, rl), (pc, rc) = parts("LAD")[0], parts("LCx")[0]
for Y, s_, r in (lm, lad, cx, *BRANCHES[:3]):
    tube_edge(ax, Y, r, EDGE_GREY, EW)
for Y, s_, r in (lad, cx, *BRANCHES[:3]):
    tube_fill(ax, Y, r, MUTED)
tube_fill(ax, lm[0], lm[2], LM_COL)
for (Y, r), col in (((pl, rl), LAD_COL), ((pc, rc), CX_COL)):
    ax.add_patch(Polygon(band(Y, r + 2.0), closed=True, fc=tint(INK2, 0.10), ec="none", zorder=0))
    tube_edge(ax, Y, r, darken(col, 0.15), EW)
for (Y, r), col in (((pl, rl), LAD_COL), ((pc, rc), CX_COL)):
    tube_fill(ax, Y, r, col)
plaque(ax, *lad, 11.0, 16.5)
for Y, s_, r in (lad, cx):
    centerline(ax, Y, tint(INK2, 0.75), lw=0.7)
centerline(ax, lm[0], INK2, lw=0.7)
centerline(ax, pl, darken(LAD_COL, 0.35), lw=0.9)
centerline(ax, pc, darken(CX_COL, 0.2), lw=0.9)
ax.text(*(pc[-1] + [-3.0, 4.6]), "outcome", color=INK2, ha="left", va="center", fontsize=8)
a_lad, a_cx = heading(lad[0], 12), heading(cx[0], 12)  # directions 3 from O, for drawing the arc
ax.add_patch(Arc(O, 9, 9, theta1=a_lad, theta2=a_cx, color=ANG_COL, lw=1.2, zorder=6))
mid = np.radians((a_lad + a_cx) / 2)
ax.text(*(O + 6.4 * np.array([np.cos(mid), np.sin(mid)])), r"$\theta$", ha="center", va="center", fontsize=10,
        zorder=7)
for (Y, s_, r), col, lab, side, i in ((lad, LAD_COL, r"$D_{\mathrm{LAD}}$", -1, 30),
                                     (cx, CX_COL, r"$D_{\mathrm{LCx}}$", 1, 30)):
    n = normal(Y, i)  # i = 30: 7.5 from O, inside the 5 to 10 stretch of the diameters
    ax.plot(*np.array([Y[i] - r[i] * n, Y[i] + r[i] * n]).T, color=darken(col, 0.3), lw=1.1, zorder=6)
    ax.text(*(Y[i] + side * (r[i] + 2.6) * n), lab, color=darken(col, 0.1), ha="center", va="center", fontsize=8)
dot(ax, O, ms=3)
ax.text(*(O + [-0.8, 2.6]), r"$O$", ha="center", va="bottom")
ax.text(*(lm[0][0] + [0.0, 3.0]), "LM", color=LM_COL, ha="center", va="bottom", fontsize=9)
ax.text(*(lad[0][104] + [1.8, -0.8]), "LAD", color=INK2, ha="left", va="top", fontsize=9)
ax.text(*(cx[0][88] + [0.0, 2.8]), "LCx", color=INK2, ha="center", va="bottom", fontsize=9)

# right: curvature model, the whole tree
allY = np.vstack([lm[0], lad[0], cx[0], rca[0]])
lo, hi = allY.min(0), allY.max(0)
span_x = hi[0] - lo[0] + 8
cy, span_y = (lo[1] + hi[1]) / 2 - 1, span_x / 1.15  # 1.15: width over height of the panel axes
ax = panel(1, (lo[0] - 4, hi[0] + 4), (cy - span_y / 2, cy + span_y / 2))
EW = 0.30
aorta = vessel(np.array([-3.0, -1.5]), 90, lambda s: 0 * s, 16, 4.2, 4.2)
for Y, s_, r in (aorta, lm, *BRANCHES):
    tube_edge(ax, Y, r, EDGE_GREY, EW)
for Y, s_, r in (aorta, lm, *BRANCHES):
    tube_fill(ax, Y, r, MUTED)
segs = {name: parts(name) for name in ARTERIES}
for name in ARTERIES:
    for j, (Y, r) in enumerate(segs[name]):
        tube_edge(ax, Y, r, darken(SEG_COL[j], 0.15), EW)
BI = np.array([0.0, -24.0])
for name in ARTERIES:
    for j, (Y, r) in enumerate(segs[name]):
        tube_fill(ax, Y, r, SEG_COL[j])
        centerline(ax, Y, darken(SEG_COL[j], 0.35), lw=0.8)
        m = Y[len(Y) // 2]
        ax.plot([BI[0], m[0]], [BI[1], m[1]], color=tint(INK2, 0.40), lw=0.5, zorder=0.5)
        ax.plot(*m, "o", ms=1.6, color=INK2, zorder=6)
        if j:  # tick across the artery at the boundary to the previous segment
            n = normal(Y, 0)
            ax.plot(*np.array([Y[0] - (r[0] + 1.3) * n, Y[0] + (r[0] + 1.3) * n]).T, color=INK, lw=0.7, zorder=6)
plaque(ax, *lad, 24.0, 32.0, hmax=0.75)
dot(ax, BI, ms=4.5)
ax.text(*(BI + [0.0, -2.4]), r"$b_i$", ha="center", va="top", fontsize=10)
ax.text(*(lm[0][-1] + [0.5, 3.0]), "LM", color=INK2, ha="center", va="bottom", fontsize=9)
ax.text(*(lad[0][-1] + [0.0, -2.2]), "LAD", color=INK2, ha="center", va="top", fontsize=9)
ax.text(*(cx[0][-1] + [-2.2, -0.6]), "LCx", color=INK2, ha="right", va="top", fontsize=9)
ax.text(*(rca[0][-1] + [0.0, -2.2]), "RCA", color=INK2, ha="center", va="top", fontsize=9)
xl, yl = -14, -44
for j, lab in enumerate(("proximal", "mid", "distal")):
    y = yl - 4.2 * j
    ax.plot([xl, xl + 3.5], [y, y], color=SEG_COL[j], lw=2.0, solid_capstyle="butt")
    ax.text(xl + 4.5, y, lab, ha="left", va="center", fontsize=7.5, color=INK2)

out = Path(__file__).with_suffix("")
fig.savefig(f"{out}.pdf")
fig.savefig(f"{out}.png", dpi=200)
