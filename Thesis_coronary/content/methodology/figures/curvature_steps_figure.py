"""Figure for Section sec:method-curvature (fig:method-curvature, replaces curvature_figure.py on 2026-11-19):
average curvature of a segment, in the style of surface_cut_figure.py, without panel letters (user).

    python Thesis_coronary/content/methodology/figures/curvature_steps_figure.py

A made-up artery in one plane with points about 0.5 mm apart, as in the tracer output (no patient data), run through the real code of
CGPS_data/thesis_final/curvature_feature.py (chord_point, menger_curvature, curvature_profile, segment_mean,
CHORD). Panels, left to right: the curvature of a circle is 1/R; at a centerline point P_i the points B_i and F_i CHORD mm away in a
straight line, the triangle they span and the circle through them; a straight stretch, a gentle and a tight
bend at the same chord and their curvature; the curvature profile of the whole artery, divided at two
made-up segment boundaries, and the average curvature T of each segment (area under the profile / length).
2026-11-20 (user): points 0.45 to 0.5 mm apart instead of 0.3 to 1.2 mm; the code does not respace them.
2026-11-21 (user: a figure of "the more sharply the artery bends at P_i, the smaller this circle is"): the third
panel now draws a straight stretch, a gentle (R 12 mm) and a tight (R 5 mm) bend through one P_i at one scale,
with their whole circles (were three cropped rows, circles out of view).
2026-11-21 (user: the old circles of radius 20, 10 and 5 mm as one illustration, and a second one with 1/R, the two
points 5 mm ahead and behind and the averaging): two figures. curvature_radius_figure: circles of radius 20, 10 and
5 mm with kappa = 1/R (after panel A of curvature_figure.py). curvature_steps_figure: the triangle and circle at
P_i, the artery by segment with the ends that have no profile value, the profile with T. The nested-circle panel
and the separate curvature_point_figure / curvature_segment_figure of earlier the same day are gone.
2026-11-21 (user: more detail in the radius figure, one centerline through all the circles with the three points):
curvature_radius_figure is now one made-up centerline (0.5 mm points) with a straight stretch (kappa 0) and bends on
R 20, 10 and 5 mm, each with B, P, F 5 mm apart, the triangle, the circle and kappa from the thesis code.
Same day (user): B_i, P_i and F_i each in their own colour (mauve, black, green, the thesis palette) in both
figures, no key;
longer straight stretches (14, 24, 26 mm) so the bends sit further apart.
Same day (user: no proximal, mid, distal before they are introduced; show the triangle sides and the integral):
curvature_steps_figure without segments. Left: the triangle with its three sides in three colours and Menger's
formula below, each length of the denominator in the colour of its side. Middle: the artery, purple where the
profile has values, s_first and s_last marked. Right: the profile with the area under it and the dashed rectangle
of height T over the same stretch (same area).
Same day (user: remove the points, cleaner, softer colours): no B, P, F markers or labels in figure 2 (the side
labels name them), muted side colours, lighter fills, grey labels.
Same day (user: black centerline, fewer points): the drawn centerline is black in both figures, with only every
SHOW-th point marked; the computation is unchanged.
Same day (user: same colours as curvature_radius_figure): figure 2's left panel has the purple dashed circle, the
triangle fill of figure 1 and B_i, P_i, F_i as mauve, black and green points; the sides keep their formula colours.
Style and colours as the Technical Background illustrations (illus_hazard_area.py). Writes
curvature_radius_figure.{pdf,png} and curvature_steps_figure.{pdf,png} next to this file.
"""
import sys
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import FancyBboxPatch, Polygon

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "CGPS_data" / "thesis_final"))
sys.path.insert(0, str(ROOT / "Thesis_coronary" / "setup"))
from curvature_feature import CHORD, chord_point, curvature_profile, menger_curvature, segment_mean  # noqa: E402
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


SIDE = ("#6f97b8", "#c3a052", "#b5698f")  # triangle sides B-P, P-F, B-F: muted blue, ochre, rose
TRI = MAIN
PTC = {"B": darken(SECOND), "P": INK, "F": THIRD}  # B_i, P_i, F_i in every figure
DASH = (0, (3, 2.5))
SHOW = 4  # draw every 4th centerline point (about 2 mm apart); the curvature still uses all of them
AX = dict(arrowstyle="-|>,head_length=0.55,head_width=0.16", lw=0.6, color=INK, shrinkA=0, shrinkB=0)
rng = np.random.default_rng(4)


def circumcircle(a, b, c):
    """Centre and radius of the circle through three points in the plane (for drawing only)."""
    (ax_, ay), (bx, by), (cx, cy) = a[:2], b[:2], c[:2]
    d = 2 * (ax_ * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax_ ** 2 + ay ** 2) * (by - cy) + (bx ** 2 + by ** 2) * (cy - ay) + (cx ** 2 + cy ** 2) * (ay - by)) / d
    uy = ((ax_ ** 2 + ay ** 2) * (cx - bx) + (bx ** 2 + by ** 2) * (ax_ - cx) + (cx ** 2 + cy ** 2) * (bx - ax_)) / d
    return np.array([ux, uy]), float(np.hypot(ax_ - ux, ay - uy))


# ---------------------------------------------------------------- made-up artery
xd = np.linspace(0, 70, 7001)  # a planar curve: a gentle wave and one tight bend, finely sampled
yd = 6.0 * np.sin(2 * np.pi * xd / 55) + 5.0 * np.exp(-((xd - 52) / 4.5) ** 2)
sd = np.r_[0, np.cumsum(np.hypot(np.diff(xd), np.diff(yd)))]
s = np.r_[0, np.cumsum(rng.uniform(0.45, 0.5, 400))]
s = s[s <= sd[-1]]  # then read every 0.45 to 0.5 mm, the step of the tracer (tracer_probe.md)
P = np.c_[np.interp(s, sd, xd), np.interp(s, sd, yd), np.zeros_like(s)]
arc = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
pos, kappa = curvature_profile(P)
T = segment_mean(pos, kappa, pos[0], pos[-1] + 1e-9)  # the average over the whole stretch with values

# ---------------------------------------------------------------- layout
W = 6.3
L, R, GAP = 0.015, 0.985, 0.02
PB, PT = 0.02, 0.98
t = np.linspace(0, 2 * np.pi, 300)


def frame(n, h):
    """A figure of n rounded panels side by side; returns the figure and a function placing an axes in panel k."""
    fig = plt.figure(figsize=(W, h))
    pw = (R - L - (n - 1) * GAP) / n
    bg = fig.add_axes([0, 0, 1, 1], zorder=-5)
    bg.set_axis_off(); bg.set_xlim(0, 1); bg.set_ylim(0, 1)
    for k in range(n):
        bg.add_patch(FancyBboxPatch((L + k * (pw + GAP), PB), pw, PT - PB, transform=fig.transFigure,
                     boxstyle="round,pad=0,rounding_size=0.02", fc=tint(MUTED, 0.08),
                     ec=tint(MUTED, 0.30), lw=0.8, mutation_aspect=W / h))

    def panel(k, left=0.02, right=0.02, bottom=0.10, top=0.10):
        x0 = L + k * (pw + GAP)
        return fig.add_axes([x0 + left, PB + bottom, pw - left - right, PT - PB - bottom - top])
    return fig, panel


def dot(ax, q, ms=3.5, col=INK, z=5):
    ax.plot(q[0], q[1], "o", ms=ms, color=col, mec="white", mew=0.6, zorder=z)


def triangle(ax, b, p, f, col=TRI):
    ax.add_patch(Polygon([b[:2], p[:2], f[:2]], closed=True, fc=tint(col, 0.30), ec=col, lw=0.8, zorder=2))


def save(fig, name):
    out = Path(__file__).with_name(name)
    fig.savefig(f"{out}.pdf")
    fig.savefig(f"{out}.png", dpi=200)


# ================================================================ figure 1: curvature is 1/R along one centerline
# A made-up centerline of straight pieces and three circular bends (R 20, 10, 5 mm, alternating sides), read every
# 0.5 mm. At one straight point and at the middle of each bend, B and F are found 5 mm away and kappa computed with
# the thesis code; each bend's half-arc is longer than the arc a 5 mm chord needs, so kappa = 1/R exactly.
PIECES = (("line", 14.0), ("arc", 20.0, np.radians(50)), ("line", 24.0), ("arc", 10.0, -np.radians(110)),
          ("line", 26.0), ("arc", 5.0, np.radians(140)), ("line", 2.0))
pts, head, marks, s0 = [np.zeros(2)], 0.0, [7.0], 0.0
for piece in PIECES:
    if piece[0] == "line":
        n = int(piece[1] / 0.01)
        d = np.array([np.cos(head), np.sin(head)])
        pts += [pts[-1] + d * piece[1] * k / n for k in range(1, n + 1)]
        s0 += piece[1]
    else:
        Rb, turn = piece[1], piece[2]
        sgn = np.sign(turn)
        c = pts[-1] + Rb * np.array([np.cos(head + sgn * np.pi / 2), np.sin(head + sgn * np.pi / 2)])
        a0 = head - sgn * np.pi / 2
        n = int(Rb * abs(turn) / 0.01)
        pts += [c + Rb * np.array([np.cos(a0 + turn * k / n), np.sin(a0 + turn * k / n)]) for k in range(1, n + 1)]
        marks.append(s0 + Rb * abs(turn) / 2)
        s0 += Rb * abs(turn)
        head += turn
dense = np.array(pts)
ds = np.r_[0, np.cumsum(np.linalg.norm(np.diff(dense, axis=0), axis=1))]
u = np.arange(0, ds[-1], 0.5)
for m in marks:  # put the marked points on the sampling grid
    u[np.argmin(np.abs(u - m))] = m
C = np.c_[np.interp(u, ds, dense[:, 0]), np.interp(u, ds, dense[:, 1]), np.zeros_like(u)]

fig, panel = frame(1, 3.3)
ax = panel(0, 0.02, 0.02, 0.03, 0.03)
ax.set_axis_off(); ax.set_aspect("equal")
ax.plot(C[:, 0], C[:, 1], color=INK, lw=1.0, zorder=1)
ax.plot(C[::SHOW, 0], C[::SHOW, 1], "o", ms=1.6, color=INK, zorder=1)
for k, m in enumerate(marks):
    j = int(np.argmin(np.abs(u - m)))
    bb, pp, ff = chord_point(C, j, CHORD, -1), C[j], chord_point(C, j, CHORD, 1)
    kap = menger_curvature(bb, pp, ff)
    print(f"marked point {k}: kappa {kap:.4f} 1/mm")
    if k == 0:  # straight: the three points lie on a line
        ax.plot([bb[0], ff[0]], [bb[1], ff[1]], color=TRI, lw=1.2, zorder=2)
        ax.text(pp[0], pp[1] - 2.2, r"$\kappa = 0$", ha="center", va="top", fontsize=8.5)
    else:
        ctr, rad = circumcircle(bb, pp, ff)
        ax.plot(*(ctr[:, None] + rad * np.vstack([np.cos(t), np.sin(t)])), color=MAIN, lw=0.8, ls=DASH, zorder=1)
        triangle(ax, bb, pp, ff)
        away = (ctr - pp[:2]) / rad  # from P_i through the centre, to the far side of the circle
        ax.annotate("", xy=ctr + rad * away, xytext=ctr, arrowprops=AX, zorder=3)
        dot(ax, ctr, ms=2.2)
        lab = rf"$R = {rad:.0f}$ mm" + "\n" + rf"$\kappa = 1/{rad:.0f} = {kap:.2f}$ mm$^{{-1}}$"
        if k == 3:  # the tight bend: beside its circle, clear of the centerline arriving from above
            ax.text(*(ctr + np.array([rad + 3.0, 0.0])), lab, ha="left", va="center", fontsize=8, linespacing=1.3)
        else:
            ax.text(*(ctr + (rad + 2.0) * away), lab, ha="center", va="bottom" if away[1] > 0 else "top",
                    fontsize=8, linespacing=1.3)
    for q, key in ((bb, "B"), (pp, "P"), (ff, "F")):
        dot(ax, q, ms=4.2, col=PTC[key])
    if k == 1:
        for q, lab in ((bb, r"$B_i$"), (pp, r"$P_i$"), (ff, r"$F_i$")):
            v = (q[:2] - ctr) / np.linalg.norm(q[:2] - ctr)  # outwards from the circle, off the centerline
            ax.text(*(q[:2] + 2.2 * v), lab, ha="center", va="center", fontsize=9, color=PTC[lab[1]])
ax.autoscale_view()
x_lo, x_hi = ax.get_xlim(); y_lo, y_hi = ax.get_ylim()
ax.set_xlim(x_lo - 3, x_hi + 16); ax.set_ylim(y_lo - 9, y_hi + 9)
save(fig, "curvature_radius_figure")

# ================================================================ figure 2: from three points to the average curvature
H2 = 2.9
fig = plt.figure(figsize=(W, H2))
WID = (1.35, 1.0, 1.0)  # the left panel holds the equation
unit = (R - L - 2 * GAP) / sum(WID)
X0 = np.r_[L, L + np.cumsum([w_ * unit + GAP for w_ in WID[:-1]])]
bg = fig.add_axes([0, 0, 1, 1], zorder=-5)
bg.set_axis_off(); bg.set_xlim(0, 1); bg.set_ylim(0, 1)
for x0_, w_ in zip(X0, WID):
    bg.add_patch(FancyBboxPatch((x0_, PB), w_ * unit, PT - PB, transform=fig.transFigure,
                 boxstyle="round,pad=0,rounding_size=0.02", fc=tint(MUTED, 0.08),
                 ec=tint(MUTED, 0.30), lw=0.8, mutation_aspect=W / H2))


def panel2(k, left, right, bottom, top):
    return fig.add_axes([X0[k] + left, PB + bottom, WID[k] * unit - left - right, PT - PB - bottom - top])


# left: B_i, P_i, F_i at the tight bend, the triangle with its sides in three colours, and Menger's formula with
# each length of the denominator in the colour of its side
w = (pos > 45) & (pos < 70)  # the tight bend
i = int(np.argmin(np.abs(arc - pos[w][np.argmax(kappa[w])])))
b, p, f = chord_point(P, i, CHORD, -1), P[i], chord_point(P, i, CHORD, 1)
ctr, rad = circumcircle(b, p, f)
ax = panel2(0, 0.01, 0.01, 0.25, 0.03)
ax.set_axis_off(); ax.set_aspect("equal")
near = np.abs(arc - arc[i]) < 9
ax.plot(P[near, 0], P[near, 1], color=INK, lw=1.0, zorder=1)
shown = near & ((np.arange(len(P)) - i) % SHOW == 0)  # every SHOW-th point, counted from P_i so that it is drawn
ax.plot(P[shown, 0], P[shown, 1], "o", ms=1.8, color=INK, zorder=1)
for q, key in ((b, "B"), (p, "P"), (f, "F")):  # coloured as in curvature_radius_figure; P_i is the top
    dot(ax, q, ms=4.2, col=PTC[key])
ax.plot(*(ctr[:, None] + rad * np.vstack([np.cos(t), np.sin(t)])), color=MAIN, lw=0.8, ls=DASH, zorder=1)
ang = -2.0
ax.annotate("", xy=ctr + rad * np.array([np.cos(ang), np.sin(ang)]), xytext=ctr, arrowprops=AX, zorder=3)
dot(ax, ctr, ms=2.5)
ax.text(*(ctr + 0.5 * rad * np.array([np.cos(ang), np.sin(ang)]) + np.array([0.9, 0.0])), r"$R_i$",
        ha="left", va="center", fontsize=9)
ax.add_patch(Polygon([b[:2], p[:2], f[:2]], closed=True, fc=tint(MAIN, 0.30), ec="none", zorder=2))
cen = (b[:2] + p[:2] + f[:2]) / 3
ax.text(*cen, r"$A_i$", ha="center", va="center", fontsize=8.5, color=INK2, zorder=4)
SIDES = ((b, p, r"$\|P_i - B_i\|$"), (p, f, r"$\|F_i - P_i\|$"), (b, f, r"$\|F_i - B_i\|$"))
for (q0, q1, lab), col in zip(SIDES, SIDE):
    ax.plot([q0[0], q1[0]], [q0[1], q1[1]], color=col, lw=1.3, zorder=3, solid_capstyle="round")
    m_ = (q0[:2] + q1[:2]) / 2
    nrm = np.array([-(q1[1] - q0[1]), q1[0] - q0[0]]); nrm /= np.linalg.norm(nrm)
    if np.dot(nrm, m_ - cen) < 0:  # outwards, away from the triangle
        nrm = -nrm
    if nrm[0] < -0.5:  # a side facing left: right-aligned, clear of the centerline
        ax.text(*(m_ + 1.6 * nrm + np.array([0.0, 1.0])), lab, ha="right", va="center", fontsize=7.5, color=col,
                zorder=4)
    else:
        ax.text(*(m_ + 1.3 * nrm), lab, ha="center", va="center", fontsize=7.5, color=col, zorder=4)
ax.set_xlim(p[0] - 8.0, p[0] + 8.0); ax.set_ylim(p[1] - 12.0, p[1] + 3.6)

# the equation, typeset in pieces so that each length carries the colour of its side
eq = fig.add_axes([X0[0], PB + 0.02, WID[0] * unit, 0.21]); eq.set_axis_off(); eq.set_xlim(0, 1); eq.set_ylim(0, 1)
rend = fig.canvas.get_renderer()
inv = eq.transAxes.inverted()


def width(txt):
    bb_ = txt.get_window_extent(renderer=rend)
    return inv.transform((bb_.x1, 0))[0] - inv.transform((bb_.x0, 0))[0]


FS = 8.5
lhs = eq.text(0.0, 0.5, r"$\kappa_i = \dfrac{1}{R_i} = $", ha="left", va="center", fontsize=FS)
parts = [eq.text(0, 0.28, lab, ha="left", va="center", fontsize=FS, color=col) for (_, _, lab), col in zip(SIDES, SIDE)]
gap = 0.012
den_w = sum(width(x) for x in parts) + gap * (len(parts) - 1)
total = width(lhs) + 0.01 + den_w
x = 0.5 - total / 2
lhs.set_x(x)
x0f = x + width(lhs) + 0.01
for x_ in parts:
    x_.set_x(x0f); x0f += width(x_) + gap
eq.plot([x + width(lhs) + 0.01, x + total], [0.5, 0.5], color=INK, lw=0.7)
eq.text(x + width(lhs) + 0.01 + den_w / 2, 0.72, r"$4A_i$", ha="center", va="center", fontsize=FS, color=INK)

# middle: the whole made-up artery; the profile has values on the purple stretch, from s_first to s_last
ax = panel2(1, 0.02, 0.02, 0.12, 0.10)
ax.set_axis_off(); ax.set_aspect("equal")
has = (arc >= pos[0]) & (arc <= pos[-1])
ax.plot(P[:, 0], P[:, 1], color=tint(INK2, 0.35), lw=1.8, zorder=1, solid_capstyle="round")
ax.plot(P[has, 0], P[has, 1], color=tint(MAIN, 0.7), lw=1.8, zorder=2, solid_capstyle="butt")
for sv, lab, dy in ((pos[0], r"$s_{\mathrm{first}}$", -3.2), (pos[-1], r"$s_{\mathrm{last}}$", 3.2)):
    q = P[np.argmin(np.abs(arc - sv))]
    ax.plot([q[0], q[0]], [q[1] - 1.8, q[1] + 1.8], color=INK, lw=0.8, zorder=3)
    ax.text(q[0], q[1] + dy, lab, ha="center", va="top" if dy < 0 else "bottom", fontsize=8)
ax.set_xlim(-3, 73); ax.set_ylim(-14, 16)

# right: the profile from s_first to s_last; the area under it equals the dashed rectangle of height T
ax = panel2(2, 0.05, 0.03, 0.13, 0.08)
XMAX, YMAX = 1.06 * arc[-1], 1.25 * kappa.max()
for sp in ax.spines.values():
    sp.set_visible(False)
ax.set_xticks([]); ax.set_yticks([]); ax.patch.set_alpha(0)
ax.annotate("", xy=(1, 0), xytext=(0, 0), xycoords="axes fraction", arrowprops=AX)
ax.annotate("", xy=(0, 1), xytext=(0, 0), xycoords="axes fraction", arrowprops=AX)
ax.text(1.0, -0.05, r"$s$", transform=ax.transAxes, ha="center", va="top")
ax.text(0.035, 1.0, r"$\kappa$", transform=ax.transAxes, ha="left", va="center")
ax.set_xlim(0, XMAX); ax.set_ylim(0, YMAX)
ax.fill_between(pos, 0, kappa, color=tint(MAIN, 0.14), lw=0, zorder=0)
ax.plot(pos, kappa, color=tint(MAIN, 0.75), lw=1.0, zorder=2)
ax.plot([pos[0], pos[0], pos[-1], pos[-1]], [0, T, T, 0], color=INK, lw=0.8, ls=DASH, zorder=3)
ax.text(pos[-1] + 1.0, T, r"$T$", ha="left", va="center", fontsize=9)
wide = pos < 22  # the first, broad bend: the arrow from the label ends in its shaded area
xi = pos[wide][np.argmax(kappa[wide])]
ax.annotate(r"$\int \kappa(s)\,\mathrm{d}s$", xy=(xi, 0.35 * kappa[wide].max()), xytext=(xi + 8, 0.78 * YMAX),
            ha="center", va="center", fontsize=8, color=INK2,
            arrowprops=dict(arrowstyle="-|>,head_length=0.4,head_width=0.12", lw=0.6, color=INK2,
                            shrinkA=2, shrinkB=0))
for sv, lab in ((pos[0], r"$s_{\mathrm{first}}$"), (pos[-1], r"$s_{\mathrm{last}}$")):
    ax.plot([sv, sv], [0, -0.025 * YMAX], color=INK, lw=0.8, clip_on=False)
    ax.text(sv, -0.05 * YMAX, lab, ha="center", va="top", fontsize=8)
save(fig, "curvature_steps_figure")

area = ((kappa[1:] + kappa[:-1]) / 2 * np.diff(pos)).sum()
print(f"T = {T:.4f} 1/mm over {pos[0]:.1f} to {pos[-1]:.1f} mm; T x length {T * (pos[-1] - pos[0]):.4f}, "
      f"area under the profile {area:.4f}")
