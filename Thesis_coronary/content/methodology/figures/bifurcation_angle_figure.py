"""Figure for Section sec:method-angle (fig:method-angle): the LAD-LCx bifurcation angle from the points 5 to
10 mm from the bifurcation point and a line fitted through each set.

    python Thesis_coronary/content/methodology/figures/bifurcation_angle_figure.py

A made-up left main bifurcation (no patient data), run through the real code of
CGPS_data/thesis_final/bifurcation_angle.py (DEPTHS, point_at_depth, artery_direction, lm_angle).
A, the vessels as a grey lumen with their centerline, the bifurcation point O, the distance along the LAD
centerline from O (bracket with ticks at 0, 5 and 10 mm) and the points every 0.5 mm from 5 to 10 mm on both
arteries; a dotted box marks the region shown in B. B, the same points, the least-squares line through each
set (solid over the stretch, dashed back towards O, which it does not pass through), the unit vectors
u_LAD and u_LCx pointing away from the bifurcation, and the angle theta with its value from lm_angle.
2026-11-11: first version (two panels, centerline dots, floating depth labels).
2026-11-11 (user: one figure of academic standard, slick and minimal, holding all the information in the
text): redrawn as above; arteries made to bend beyond 10 mm so the shape looks anatomical while the
5 to 10 mm stretch stays nearly straight. Colours as in curvature_figure.py: blue LAD, orange LCx.
Writes bifurcation_angle_figure.{pdf,png} next to this file. Thesis style: serif, white, no title.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Rectangle

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "CGPS_data" / "thesis_final"))
from bifurcation_angle import DEPTHS, artery_direction, lm_angle, point_at_depth  # noqa: E402

INK, INK2, MUTED, SURF = "#0b0b0b", "#52514e", "#8a8984", "white"
LUMEN, LUMEN_B, CL_B = "#e6e5e0", "#f1f0ec", "#c9c8c2"  # lumen in A, lumen and centerline faded in B
COL = {"LAD": "#2a78d6", "LCx": "#eb6834"}  # blue and orange of curvature_figure.py

plt.rcParams.update({"font.family": "serif", "font.serif": ["STIX Two Text", "STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix", "font.size": 8.5, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF})


# ---------------------------------------------------------------- made-up left main bifurcation
def path(start, heading_deg, k, length, n=1500):
    """Dense 2D path from start with the given initial heading (degrees) and curvature k(u) (1/mm)."""
    u = np.linspace(0, length, n)
    head = np.radians(heading_deg) + np.r_[0, np.cumsum((k(u[1:]) + k(u[:-1])) / 2 * np.diff(u))]
    return start + np.c_[np.r_[0, np.cumsum(np.cos(head[:-1]) * np.diff(u))],
                         np.r_[0, np.cumsum(np.sin(head[:-1]) * np.diff(u))]]


def arc(Y):
    return np.r_[0, np.cumsum(np.linalg.norm(np.diff(Y, axis=0), axis=1))]


O = np.zeros(2)
lad2 = path(O, 41, lambda u: 0.003 - 0.05 * np.exp(-((u - 21) / 5) ** 2), 32)  # bends beyond about 13 mm
lcx2 = path(O, -45, lambda u: -0.004 + 0.06 * np.exp(-((u - 18) / 5) ** 2), 28)  # wraps back along the groove
lm2 = path(O, 174, lambda u: -0.012 + 0 * u, 15)[::-1]  # drawn only: built from O back to the ostium
lad, cx = [(np.c_[Y, np.zeros(len(Y))], arc(Y)) for Y in (lad2, lcx2)]
theta = lm_angle(lad, cx)
theta_origin = lm_angle(lad, cx, method="origin")
pts = {n: np.array([point_at_depth(Y, s, d) for d in DEPTHS])[:, :2] for n, (Y, s) in (("LAD", lad), ("LCx", cx))}
dirs = {n: artery_direction(Y, s)[:2] for n, (Y, s) in (("LAD", lad), ("LCx", cx))}


def normals(Y):
    t = np.gradient(Y, axis=0)
    t /= np.linalg.norm(t, axis=1)[:, None]
    return np.c_[-t[:, 1], t[:, 0]]


def lumen(ax, Y, width, color):
    """The vessel as a band of the given width (mm) around its centerline."""
    nrm = normals(Y)
    ring = np.r_[Y + width / 2 * nrm, (Y - width / 2 * nrm)[::-1]]
    ax.fill(*ring.T, color=color, lw=0, zorder=1)


def vessels(ax, lumen_c, cl_c, cl_lw):
    for Y, w in ((lm2, 4.2), (lad2, 3.4), (lcx2, 3.0)):
        lumen(ax, Y, w, lumen_c)
    ax.add_patch(plt.Circle(O, 2.1, color=lumen_c, lw=0, zorder=1))  # closes the confluence at O
    for Y in (lm2, lad2, lcx2):
        ax.plot(*Y.T, color=cl_c, lw=cl_lw, solid_capstyle="round", zorder=2)


def letter(ax, c):
    pos = ax.get_position()
    ax.figure.text(pos.x0, 0.985, c, fontsize=11, color=INK, va="top", ha="left")


# ---------------------------------------------------------------- layout: one scale for both panels
XA, YA = (-16.5, 25.5), (-21.0, 22.0)
XB, YB = (-3.5, 14.5), (-12.0, 12.0)
wa, wb = XA[1] - XA[0], XB[1] - XB[0]
fig = plt.figure(figsize=(6.3, 3.05))
gs = fig.add_gridspec(1, 2, width_ratios=[wa / (YA[1] - YA[0]), wb / (YB[1] - YB[0])], wspace=0.06,
                      left=0.01, right=0.99, top=0.93, bottom=0.02)

# ---------------------------------------------------------------- A: O, distance along the centerline, the points
ax = fig.add_subplot(gs[0])
vessels(ax, LUMEN, INK2, 0.9)
for n in ("LAD", "LCx"):
    ax.plot(*pts[n].T, "o", color=COL[n], ms=2.6, mew=0, zorder=4)
ax.plot(*O, "o", color=INK, ms=4.2, zorder=5)
ax.text(O[0] + 0.6, O[1] - 1.0, "$O$", fontsize=10, ha="left", va="top", zorder=6)

# distance along the LAD centerline: a bracket offset to its left side, ticks at 0, 5 and 10 mm
sl = lad[1]
nl = normals(lad2)
m = sl <= 10.0
ax.plot(*(lad2[m] + 3.3 * nl[m]).T, color=INK2, lw=0.6, zorder=3)
for d in (0.0, 5.0, 10.0):
    i = int(np.argmin(np.abs(sl - d)))
    ax.plot(*np.c_[lad2[i] + 2.8 * nl[i], lad2[i] + 3.8 * nl[i]], color=INK2, lw=0.6, zorder=3)
    ax.text(*(lad2[i] + 4.6 * nl[i]), f"{d:.0f}" + (" mm" if d == 10 else ""), fontsize=7, color=INK2,
            ha="right", va="center", zorder=3)

ax.text(*(lm2[0] + [0.0, 3.0]), "LM", fontsize=8.5, color=INK2, ha="left", va="bottom")
ax.text(*(lad2[-1] + [-1.0, 1.2]), "LAD", fontsize=8.5, color=COL["LAD"], ha="center", va="bottom")
ax.text(*(lcx2[-1] + [1.8, 0.0]), "LCx", fontsize=8.5, color=COL["LCx"], ha="left", va="center")
ax.add_patch(Rectangle((XB[0], YB[0]), wb, YB[1] - YB[0], fill=False, ec=MUTED, lw=0.6, ls=(0, (1.5, 1.5)),
                       zorder=0))
ax.plot([XA[0] + 1.0, XA[0] + 6.0], [YA[0] + 1.5] * 2, color=INK, lw=1.0)  # 5 mm scale bar
ax.text(XA[0] + 3.5, YA[0] + 2.2, "5 mm", fontsize=7, color=INK2, ha="center", va="bottom")
ax.set(aspect="equal", xlim=XA, ylim=YA)
ax.axis("off")
letter(ax, "A")

# ---------------------------------------------------------------- B: fitted lines, directions and theta
ax = fig.add_subplot(gs[1])
vessels(ax, LUMEN_B, CL_B, 0.8)
c = {n: pts[n].mean(axis=0) for n in pts}  # each fitted line passes through the mean of its points
X = c["LAD"] + np.linalg.solve(np.c_[dirs["LAD"], -dirs["LCx"]], c["LCx"] - c["LAD"])[0] * dirs["LAD"]
for n, side in (("LAD", 1), ("LCx", -1)):
    u, col = dirs[n], COL[n]
    t0, t1 = (pts[n][0] - c[n]) @ u, (pts[n][-1] - c[n]) @ u
    tx = (X - c[n]) @ u
    ax.plot(*np.c_[c[n] + (tx - 0.8) * u, c[n] + t0 * u], color=col, lw=0.7, ls=(0, (2.5, 1.8)), zorder=3)
    ax.plot(*np.c_[c[n] + t0 * u, c[n] + t1 * u], color=col, lw=1.3, zorder=3)
    ax.plot(*pts[n].T, "o", color=col, ms=3.0, mew=0, zorder=4)
    tip = c[n] + t1 * u
    ax.annotate("", tip + 3.4 * u, tip, zorder=5,
                arrowprops=dict(arrowstyle="-|>,head_length=0.45,head_width=0.22", color=col, lw=1.3,
                                shrinkA=0, shrinkB=0))
    nv = np.array([-u[1], u[0]]) * side
    ax.text(*(tip + 2.0 * u + 1.7 * nv), rf"$\mathbf{{u}}_{{\mathrm{{{n}}}}}$", color=col, fontsize=10,
            ha="center", va="center", zorder=5)
ax.plot(*O, "o", color=MUTED, ms=3.6, zorder=4)
ax.text(O[0] - 0.4, O[1] - 0.9, "$O$", fontsize=10, color=MUTED, ha="right", va="top", zorder=6)
a0 = np.degrees(np.arctan2(dirs["LCx"][1], dirs["LCx"][0]))
a1 = np.degrees(np.arctan2(dirs["LAD"][1], dirs["LAD"][0]))
R = 4.2
ax.add_patch(Arc(X, 2 * R, 2 * R, theta1=a0, theta2=a1, color=INK, lw=0.9, zorder=5))
mid = np.radians((a0 + a1) / 2)
ax.text(*(X + (R + 0.8) * np.array([np.cos(mid), np.sin(mid)])), rf"$\theta = {theta:.1f}^\circ$",
        fontsize=9.5, color=INK, ha="left", va="center", zorder=6,
        bbox=dict(fc=SURF, ec="none", pad=0.5, alpha=0.9))
ax.set(aspect="equal", xlim=XB, ylim=YB)
ax.axis("off")
letter(ax, "B")

out = Path(__file__).with_suffix("")
fig.savefig(f"{out}.pdf")
fig.savefig(f"{out}.png", dpi=300)
print(f"wrote {out}.pdf/.png")
print(f"theta (fit) {theta:.2f} deg, from O {theta_origin:.2f} deg; fitted lines cross at {X.round(2)} mm")
