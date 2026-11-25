"""Figure for Section sec:method-ratio (fig:method-ratio, replaces daughter_ratio_figure.py on 2026-11-19):
the daughter diameters from plane cuts of the lumen surface.

    python Thesis_coronary/content/methodology/figures/surface_cut_figure.py

Made-up meshes (no patient data), run through the real code of CGPS_data/thesis_final/daughter_ratio.py
(section_loops, contour_area, contour_diameter).
Panels, left to right (no letters, user 2026-11-19); 2026-11-20 (user): the first three from the mesh-cut
illustration, the fourth kept from the earlier version of this figure; the panel with the 11 cuts and their
medians dropped (user 2026-11-20).
- A short piece of lumen surface as a triangle mesh, the plane normal to its centerline, the triangles the plane
  cuts and the contour of their cut points (section_loops).
- One cut triangle: the plane crosses two of its edges, at p_i and p_{i+1}.
- The cut triangles seen along the centerline: one contour point on each crossed edge, and the area A as the sum
  of the triangles from the centroid c to each pair of neighbouring points (contour_area; the formula is in the
  text, too wide for the panel).
- The circle of equal area, D = 2 sqrt(A / pi), for the same contour.
Style and colours as the Technical Background illustrations (illus_hazard_area.py): serif, rounded panels. Writes surface_cut_figure.{pdf,png} next to this file.
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
sys.path.insert(0, str(ROOT / "CGPS_data"))
sys.path.insert(0, str(ROOT / "Thesis_coronary" / "setup"))
from daughter_ratio import contour_area, contour_diameter, section_loops  # noqa: E402
from figure_colours import INK, INK2, MUTED, PALETTE  # noqa: E402

MAIN, THIRD = PALETTE[3], PALETTE[2]  # purple, pink, green, as illus_hazard_area.py

mpl.rcParams.update({
    "font.family": "serif", "font.serif": ["cmr10"],
    "mathtext.fontset": "cm", "axes.unicode_minus": False,
    "font.size": 10, "text.color": INK, "pdf.fonttype": 42,
})


def tint(hex_, a):
    c = np.array(to_rgb(hex_))
    return tuple(1 - a * (1 - c))


LAD_COL, CUT_COL = MAIN, THIRD
DASH = (0, (3, 2.5))


# ---------------------------------------------------------------- made-up piece of vessel 
# rings of m points along x, radius varying so neighbouring rings differ
m, xs = 10, np.arange(0, 6.01, 1.0)
th = np.linspace(0, 2 * np.pi, m, endpoint=False)
rad = lambda x, t: 1.4 * (1 + 0.10 * np.cos(2 * t + 0.6 * x) + 0.22 * np.sin(1.3 * x))  # noqa: E731
rings = np.array([[[x, rad(x, t + 0.5 * x) * np.cos(t + 0.11 * k), rad(x, t + 0.5 * x) * np.sin(t + 0.11 * k)]
                   for t in th] for k, x in enumerate(xs)])
Vt = rings.reshape(-1, 3)
Ft = [(i * m + j, i * m + (j + 1) % m, (i + 1) * m + j) for i in range(len(xs) - 1) for j in range(m)]
Ft += [(i * m + (j + 1) % m, (i + 1) * m + (j + 1) % m, (i + 1) * m + j) for i in range(len(xs) - 1) for j in range(m)]
Ft = np.array(Ft)
pt, nt = np.array([2.45, 0, 0]), np.array([1.0, 0, 0])
tloop = section_loops(Vt, Ft, pt, nt)[0]
dt = (Vt - pt) @ nt
cut = (dt[Ft] >= 0).any(1) & ~(dt[Ft] >= 0).all(1)
e1, e2 = np.array([0, 1.0, 0]), np.array([0, 0, 1.0])
q2 = lambda X: np.c_[np.asarray(X) @ e1, np.asarray(X) @ e2]  # noqa: E731  # coordinates in the plane
A, D = contour_area(tloop), contour_diameter(tloop)

az, el = np.radians(35), np.radians(25)
Rz = np.array([[np.cos(az), -np.sin(az), 0], [np.sin(az), np.cos(az), 0], [0, 0, 1]])
Rx = np.array([[1, 0, 0], [0, np.cos(el), -np.sin(el)], [0, np.sin(el), np.cos(el)]])
P = (Rx @ Rz)[[0, 2]]
proj = lambda X: np.asarray(X) @ P.T  # noqa: E731


# ---------------------------------------------------------------- layout
W, H = 6.3, 1.9
fig = plt.figure(figsize=(W, H))
L, R, GAP = 0.012, 0.988, 0.012
NP = 4
pw = (R - L - (NP - 1) * GAP) / NP
PB, PT = 0.02, 0.98
bg = fig.add_axes([0, 0, 1, 1], zorder=-5)
bg.set_axis_off(); bg.set_xlim(0, 1); bg.set_ylim(0, 1)
for k in range(NP):
    x0 = L + k * (pw + GAP)
    bg.add_patch(FancyBboxPatch((x0, PB), pw, PT - PB, transform=fig.transFigure,
                 boxstyle="round,pad=0,rounding_size=0.02", fc=tint(MUTED, 0.08),
                 ec=tint(MUTED, 0.30), lw=0.8, mutation_aspect=W / H))


def panel(k, left=0.01, right=0.01, bottom=0.06, top=0.06):
    x0 = L + k * (pw + GAP)
    return fig.add_axes([x0 + left, PB + bottom, pw - left - right, PT - PB - bottom - top])


# panel 1: the mesh, the plane and the triangles it cuts
ax = panel(0)
ax.set_axis_off(); ax.set_aspect("equal")
for f, c in zip(Ft, cut):
    q = proj(Vt[f])
    if c:
        ax.add_patch(Polygon(q, closed=True, fc=tint(CUT_COL, 0.55), ec=tint(LAD_COL, 0.7), lw=0.45, zorder=3))
    else:
        ax.add_patch(Polygon(q, closed=True, fill=False, ec=tint(LAD_COL, 0.30), lw=0.35, zorder=1))
h = 2.3
sq = [pt + a * h * e1 + b * h * e2 for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
ax.add_patch(Polygon(proj(sq), closed=True, fc=tint(CUT_COL, 0.10), ec=tint(CUT_COL, 0.6), lw=0.7, zorder=2,
                     alpha=0.85))
ax.plot(*proj(np.vstack([tloop, tloop[:1]])).T, color=CUT_COL, lw=1.3, zorder=4)
ax.plot(*proj(tloop).T, "o", ms=2.0, color=CUT_COL, mec="white", mew=0.3, zorder=5)
ax.plot(*proj([[0, 0, 0], [6, 0, 0]]).T, color=LAD_COL, lw=1.1, zorder=6)
ax.autoscale_view()

# panel 2: one cut triangle; the plane crosses two of its edges
f = Ft[cut][np.argmax(Vt[Ft[cut]].mean(1)[:, 2])]  # a triangle on the top of the tube
X = Vt[f]; u = X[1] - X[0]; u /= np.linalg.norm(u)
w = np.cross(np.cross(u, X[2] - X[0]), u); w /= np.linalg.norm(w)
T2 = np.c_[(X - X[0]) @ u, (X - X[0]) @ w]
dd = dt[f]
edges = [(a, b) for a, b in ((0, 1), (1, 2), (2, 0)) if (dd[a] >= 0) != (dd[b] >= 0)]
cr = np.array([T2[a] + dd[a] / (dd[a] - dd[b]) * (T2[b] - T2[a]) for a, b in edges])
ax = panel(1)
ax.set_axis_off(); ax.set_aspect("equal")
ax.add_patch(Polygon(T2, closed=True, fc=tint(CUT_COL, 0.35), ec=LAD_COL, lw=0.8, zorder=1))
dv = cr[1] - cr[0]
ax.plot(*np.array([cr[0] - 0.45 * dv, cr[1] + 0.45 * dv]).T, color=tint(CUT_COL, 0.7), lw=1.0, zorder=2)
ax.plot(*cr.T, color=CUT_COL, lw=1.6, zorder=3)
ax.plot(*cr.T, "o", ms=4.5, color=CUT_COL, mec="white", mew=0.6, zorder=4)
for q in T2:
    ax.plot(*q, "o", ms=3, color=LAD_COL, mec="white", mew=0.5, zorder=4)
for q, lab, ha, dx in zip(cr, (r"$p_i$", r"$p_{i+1}$"), ("left", "right"), (0.1, -0.1)):
    ax.text(q[0] + dx, q[1] + 0.1, lab, ha=ha, va="bottom", fontsize=9)
end = cr[0] - 0.45 * dv
ax.text(end[0] + 0.08, end[1], "plane", color=CUT_COL, ha="left", va="center", fontsize=8.5)
ax.autoscale_view(); x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
ax.set_xlim(x0 - 0.75, x1 + 0.75); ax.set_ylim(y0 - 0.2, y1 + 0.2)

# panel 3: seen along the centerline, one contour point on each crossed edge; the area as a fan from c
ax = panel(2)
ax.set_axis_off(); ax.set_aspect("equal")
i_hi = list(np.where(cut)[0]).index(np.where((Ft == f).all(1))[0][0])
for k, fc in enumerate(Ft[cut]):
    hi = k == i_hi
    ax.add_patch(Polygon(q2(Vt[fc]), closed=True, fc=tint(CUT_COL, 0.35 if hi else 0.12), lw=0, zorder=1))
    ax.add_patch(Polygon(q2(Vt[fc]), closed=True, fill=False, ec=tint(LAD_COL, 0.8), lw=0.45, zorder=3.5))
lp = q2(tloop)
c = lp.mean(axis=0)  # contour_area takes the centroid as the mean of the points
for q in lp:
    ax.plot([c[0], q[0]], [c[1], q[1]], color=tint(CUT_COL, 0.55), lw=0.4, zorder=3)
cr3 = q2([X[a] + dd[a] / (dd[a] - dd[b]) * (X[b] - X[a]) for a, b in edges])
cr3 = cr3[np.argsort(cr3[:, 0])[::-1]]  # p_i to the right, as in panel 2
ax.add_patch(Polygon([c, *cr3], closed=True, fc=tint(CUT_COL, 0.6), ec=CUT_COL, lw=0.6, zorder=3))
ax.plot(*np.vstack([lp, lp[:1]]).T, color=CUT_COL, lw=1.1, zorder=4)
ax.plot(*lp.T, "o", ms=2.6, color=CUT_COL, mec="white", mew=0.4, zorder=5)
ax.plot(*c, "o", ms=3.5, color=INK, mec="white", mew=0.6, zorder=6)
ax.text(c[0] + 0.15, c[1] - 0.12, r"$c$", ha="left", va="top")
along = (cr3[0] - cr3[1]) / np.linalg.norm(cr3[0] - cr3[1])
for q, lab, sgn in zip(cr3, (r"$p_i$", r"$p_{i+1}$"), (1, -1)):
    out_ = (q - c) / np.linalg.norm(q - c)
    ax.text(*(q + 0.5 * out_ + sgn * 0.12 * along), lab, ha="center", va="center", fontsize=9)
ax.set_xlim(-2.1, 2.1); ax.set_ylim(-2.1, 2.2)

# panel 4: the circle of equal area
ax = panel(3)
ax.set_axis_off(); ax.set_aspect("equal")
xy = lp - c
ax.fill(*xy.T, color=tint(CUT_COL, 0.28), lw=0, zorder=0)
ax.plot(*np.vstack([xy, xy[:1]]).T, color=CUT_COL, lw=1.4, zorder=3)
t = np.linspace(0, 2 * np.pi, 300)
ax.plot(D / 2 * np.cos(t), D / 2 * np.sin(t), color=INK2, lw=0.8, ls=DASH, zorder=2)
ax.annotate("", xy=(D / 2, 0.0), xytext=(-D / 2, 0.0),
            arrowprops=dict(arrowstyle="<|-|>,head_length=0.45,head_width=0.13", lw=0.6, color=INK,
                            shrinkA=0, shrinkB=0), zorder=4)
ax.text(0, 0.12, r"$D$", ha="center", va="bottom")
ax.text(0.15, -0.6, r"$A$", ha="center", va="center", fontsize=11)
ax.text(0, -2.15, r"$D = 2\sqrt{A/\pi}$", ha="center", va="top")
ax.set_xlim(-2.3, 2.3); ax.set_ylim(-2.9, 2.35)

out = Path(__file__).with_suffix("")
fig.savefig(f"{out}.pdf")
fig.savefig(f"{out}.png", dpi=600)
print(f"{len(tloop)} contour points on {cut.sum()} cut triangles; A = {A:.2f} mm2, D = {D:.2f} mm")
