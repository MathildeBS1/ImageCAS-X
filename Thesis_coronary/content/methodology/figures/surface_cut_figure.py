"""Figure for Section sec:method-ratio (fig:method-ratio, replaces daughter_ratio_figure.py on 2026-11-19):
the daughter diameters from plane cuts of the lumen surface.

    python Thesis_coronary/content/methodology/figures/surface_cut_figure.py

A made-up left main bifurcation (no patient data): an LAD and an LCx lumen surface as triangle meshes with
slightly irregular, non-circular cross-sections, run through the real code of
CGPS_data/thesis_final/daughter_ratio.py (section, contour_area, contour_diameter, SECTION_DEPTHS).
Panels, left to right (no letters, user 2026-11-19): the mesh and the plane normal to the LAD centerline at 7.5 mm from O, with the contour it cuts;
that contour in its plane and its area A as the sum of the triangles from its centroid c to each pair of
neighbouring points (contour_area); the circle of equal area, D = 2 sqrt(A / pi); the diameters of the
11 cuts 5 to 10 mm from O for the LAD and the LCx and their medians.
Style and colours as the Technical Background illustrations (illus_hazard_area.py): serif, rounded panels,
bare arrow axes. Writes surface_cut_figure.{pdf,png} next to this file.
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
from daughter_ratio import SECTION_DEPTHS, contour_area, contour_diameter, merge, section  # noqa: E402
from figure_colours import INK, INK2, MUTED, PALETTE  # noqa: E402

MAIN, SECOND, THIRD = PALETTE[3], PALETTE[1], PALETTE[2]  # purple, pink, green, as illus_hazard_area.py

mpl.rcParams.update({
    "font.family": "serif", "font.serif": ["cmr10"],
    "mathtext.fontset": "cm", "axes.unicode_minus": False,
    "font.size": 10, "text.color": INK, "pdf.fonttype": 42,
})


def tint(hex_, a):
    c = np.array(to_rgb(hex_))
    return tuple(1 - a * (1 - c))


def darken(hex_, a=0.3):
    c = np.array(to_rgb(hex_))
    return tuple((1 - a) * c + a * np.array(to_rgb(INK)))


LAD_COL, CX_COL, CUT_COL = MAIN, darken(SECOND), THIRD
DASH = (0, (3, 2.5))
AX = dict(arrowstyle="-|>,head_length=0.55,head_width=0.16", lw=0.6, color=INK, shrinkA=0, shrinkB=0)


# ---------------------------------------------------------------- made-up bifurcation
def centerline(u, bend, L=14.0, step=0.25):
    """Points every step mm from O along direction u, bending slowly towards bend."""
    x = np.arange(0, L + 1e-9, step)
    u = np.asarray(u, float) / np.linalg.norm(u)
    return x[:, None] * u + (x ** 2)[:, None] * np.asarray(bend, float)


def tube(Y, D, phase, m=20, start=0.5):
    """Triangle mesh around the centerline Y: one ring of m points per centerline point beyond start mm,
    in the plane normal to the centerline, radius varying with angle and along the vessel."""
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Y, axis=0), axis=1))]
    T = np.gradient(Y, axis=0)
    T /= np.linalg.norm(T, axis=1)[:, None]
    th = np.linspace(0, 2 * np.pi, m, endpoint=False)
    rings = []
    for y, t, x in zip(Y[s >= start], T[s >= start], s[s >= start]):
        e1 = np.cross(t, [0, 0, 1.0]); e1 /= np.linalg.norm(e1)
        e2 = np.cross(t, e1)
        r = D / 2 * (1 + 0.10 * np.cos(2 * th + phase + 0.15 * x) + 0.05 * np.sin(3 * th - phase)) \
            * (1 + 0.05 * np.sin(0.9 * x + phase))
        rings.append(y + r[:, None] * (np.cos(th)[:, None] * e1 + np.sin(th)[:, None] * e2))
    V = np.concatenate(rings)
    n = len(rings)
    F = [(i * m + j, i * m + (j + 1) % m, (i + 1) * m + j) for i in range(n - 1) for j in range(m)]
    F += [(i * m + (j + 1) % m, (i + 1) * m + (j + 1) % m, (i + 1) * m + j) for i in range(n - 1) for j in range(m)]
    return V, np.array(F), np.array(rings)


lad = centerline([1, 0.45, 0.05], [0, -0.004, 0.006])
cx = centerline([1, -0.7, -0.1], [-0.006, 0.0, -0.004])
d_lad, d_cx = 2.9, 2.3
Vl, Fl, Rl = tube(lad, d_lad, 0.4)
Vc, Fc, Rc = tube(cx, d_cx, 1.7)
V, F = merge([(Vl, Fl), (Vc, Fc)])
arc = lambda Y: np.r_[0, np.cumsum(np.linalg.norm(np.diff(Y, axis=0), axis=1))]  # noqa: E731
s_lad, s_cx = arc(lad), arc(cx)

DEP = 7.5
loop, p, n = section(V, F, lad, s_lad, cx, DEP)
A, D = contour_area(loop), contour_diameter(loop)
D_lad = np.array([contour_diameter(section(V, F, lad, s_lad, cx, x)[0]) for x in SECTION_DEPTHS])
D_cx = np.array([contour_diameter(section(V, F, cx, s_cx, lad, x)[0]) for x in SECTION_DEPTHS])
assert np.isfinite(D_lad).all() and np.isfinite(D_cx).all()

# orthographic view: azimuth about z, then elevation
az, el = np.radians(35), np.radians(30)
Rz = np.array([[np.cos(az), -np.sin(az), 0], [np.sin(az), np.cos(az), 0], [0, 0, 1]])
Rx = np.array([[1, 0, 0], [0, np.cos(el), -np.sin(el)], [0, np.sin(el), np.cos(el)]])
P = (Rx @ Rz)[[0, 2]]
proj = lambda X: np.asarray(X) @ P.T  # noqa: E731


# ---------------------------------------------------------------- layout
W, H = 6.3, 2.5
fig = plt.figure(figsize=(W, H))
L, R, GAP = 0.015, 0.985, 0.02
pw = (R - L - 3 * GAP) / 4
PB, PT = 0.02, 0.98
bg = fig.add_axes([0, 0, 1, 1], zorder=-5)
bg.set_axis_off(); bg.set_xlim(0, 1); bg.set_ylim(0, 1)
for k in range(4):
    x0 = L + k * (pw + GAP)
    bg.add_patch(FancyBboxPatch((x0, PB), pw, PT - PB, transform=fig.transFigure,
                 boxstyle="round,pad=0,rounding_size=0.02", fc=tint(MUTED, 0.08),
                 ec=tint(MUTED, 0.30), lw=0.8, mutation_aspect=W / H))


def panel(k, left=0.02, right=0.02, bottom=0.10, top=0.10):
    x0 = L + k * (pw + GAP)
    return fig.add_axes([x0 + left, PB + bottom, pw - left - right, PT - PB - bottom - top])


def bare(ax, xlab, ylab):
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.patch.set_alpha(0)
    ax.annotate("", xy=(1, 0), xytext=(0, 0), xycoords="axes fraction", arrowprops=AX)
    ax.annotate("", xy=(0, 1), xytext=(0, 0), xycoords="axes fraction", arrowprops=AX)
    ax.text(1.0, -0.05, xlab, transform=ax.transAxes, ha="center", va="top")
    ax.text(0.035, 1.0, ylab, transform=ax.transAxes, ha="left", va="center")


# panel 1: the mesh and the cutting plane
ax = panel(0, 0.01, 0.01, 0.04, 0.04)
ax.set_axis_off(); ax.set_aspect("equal")
for rings, col in ((Rl, LAD_COL), (Rc, CX_COL)):
    wire = tint(col, 0.30)
    for ring in rings[::3]:
        q = proj(np.vstack([ring, ring[:1]]))
        ax.plot(*q.T, color=wire, lw=0.35, zorder=1)
    for j in range(0, rings.shape[1], 2):
        ax.plot(*proj(rings[:, j]).T, color=wire, lw=0.35, zorder=1)
e1 = np.cross(n, [0, 0, 1.0]); e1 /= np.linalg.norm(e1)
e2 = np.cross(n, e1)
h = 2.8
sq = [p + a * h * e1 + b * h * e2 for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
ax.add_patch(Polygon(proj(sq), closed=True, fc=tint(CUT_COL, 0.22), ec=tint(CUT_COL, 0.7), lw=0.7, zorder=2))
ax.plot(*proj(np.vstack([loop, loop[:1]])).T, color=CUT_COL, lw=1.5, zorder=4)
ax.plot(*proj(lad).T, color=LAD_COL, lw=1.4, zorder=3)
ax.plot(*proj(cx).T, color=CX_COL, lw=1.4, zorder=3)
ax.plot(*proj([p]).T, "o", ms=3.5, color=INK, mec="white", mew=0.6, zorder=5)
ax.plot(*proj([[0, 0, 0]]).T, "o", ms=4, color=INK, mec="white", mew=0.7, zorder=5)
o2 = proj([[0, 0, 0]])[0]
ax.text(o2[0] - 0.5, o2[1] + 0.3, r"$O$", ha="right", va="bottom")
for Y, name, col in ((lad, "LAD", LAD_COL), (cx, "LCx", CX_COL)):
    q = proj(Y[-1])
    ax.text(q[0] + 0.4, q[1], name, color=col, ha="left", va="center", fontsize=9)
ax.annotate("", xy=proj(p + 3.2 * n), xytext=proj(p), arrowprops=dict(AX, lw=0.7), zorder=6)
q = proj(p + 3.4 * n)
ax.text(q[0], q[1] + 0.35, r"$\mathbf{n}$", ha="center", va="bottom")
ax.autoscale_view()
x_lo, x_hi = ax.get_xlim(); ax.set_xlim(x_lo - 0.3, x_hi + 2.2)

# panel 2: the area as a fan of triangles from the centroid c
xy = np.c_[(loop - p) @ e1, (loop - p) @ e2]
c = xy.mean(axis=0)
ax = panel(1, 0.01, 0.01, 0.06, 0.06)
ax.set_axis_off(); ax.set_aspect("equal")
ax.fill(*xy.T, color=tint(CUT_COL, 0.12), lw=0, zorder=0)
for q in xy:
    ax.plot([c[0], q[0]], [c[1], q[1]], color=tint(CUT_COL, 0.55), lw=0.4, zorder=1)
i = int(np.argmax(xy[:, 0]))  # one triangle, at the right edge where its labels have room
i0, i1 = i, (i + 1) % len(xy)
ax.add_patch(Polygon([c, xy[i0], xy[i1]], closed=True, fc=tint(CUT_COL, 0.6), ec=CUT_COL, lw=0.6, zorder=2))
ax.plot(*np.vstack([xy, xy[:1]]).T, color=CUT_COL, lw=1.5, zorder=3)
ax.plot(*c, "o", ms=3.5, color=INK, mec="white", mew=0.6, zorder=5)
ax.text(c[0] - 0.12, c[1] + 0.1, r"$c$", ha="right", va="bottom")
along = (xy[i1] - xy[i0]) / np.linalg.norm(xy[i1] - xy[i0])
for j, lab, sgn in ((i0, r"$p_i$", -1), (i1, r"$p_{i+1}$", 1)):
    u = (xy[j] - c) / np.linalg.norm(xy[j] - c)
    ax.text(*(xy[j] + 0.5 * u + sgn * 0.3 * along + [0.12, 0]), lab, ha="center", va="center", fontsize=9)
ax.text(0, -1.95, r"$A = \frac{1}{2}\,\|\sum_i (p_i - c) \times (p_{i+1} - c)\|$",
        ha="center", va="top", fontsize=7.5)
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.6, 1.95)

# panel 3: the circle of equal area
ax = panel(2, 0.01, 0.01, 0.06, 0.06)
ax.set_axis_off(); ax.set_aspect("equal")
ax.fill(*xy.T, color=tint(CUT_COL, 0.28), lw=0, zorder=0)
ax.plot(*np.vstack([xy, xy[:1]]).T, color=CUT_COL, lw=1.5, zorder=3)
t = np.linspace(0, 2 * np.pi, 300)
ax.plot(D / 2 * np.cos(t), D / 2 * np.sin(t), color=INK2, lw=0.8, ls=DASH, zorder=2)
ax.annotate("", xy=(D / 2, -0.0), xytext=(-D / 2, 0.0),
            arrowprops=dict(arrowstyle="<|-|>,head_length=0.45,head_width=0.13", lw=0.6, color=INK,
                            shrinkA=0, shrinkB=0), zorder=4)
ax.text(0, 0.12, r"$D$", ha="center", va="bottom")
ax.text(0.15, -0.55, r"$A$", ha="center", va="center", fontsize=11)
ax.text(0, -1.95, r"$D = 2\sqrt{A/\pi}$", ha="center", va="top")
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.6, 1.95)

# panel 4: the 11 cuts per daughter and their medians
ax = panel(3, 0.045, 0.03, 0.13, 0.08)
XMAX, YMAX = 12.0, 1.3 * max(D_lad.max(), D_cx.max())
bare(ax, r"$s$", r"$D$")
ax.set_xlim(0, XMAX); ax.set_ylim(0, YMAX)
ax.axvspan(SECTION_DEPTHS[0], SECTION_DEPTHS[-1], color=tint(CUT_COL, 0.15), lw=0, zorder=0)
for Dd, col, name in ((D_lad, LAD_COL, "LAD"), (D_cx, CX_COL, "LCx")):
    med = np.median(Dd)
    ax.plot([0, SECTION_DEPTHS[-1]], [med, med], ls=DASH, lw=0.6, color=INK2, zorder=1)
    ax.plot(SECTION_DEPTHS, Dd, "o", ms=3.2, color=col, mec="white", mew=0.5, zorder=3)
    ax.text(-0.03 * XMAX, med, rf"$D_{{\mathrm{{{name}}}}}$", ha="right", va="center", fontsize=9)
for x in (SECTION_DEPTHS[0], SECTION_DEPTHS[-1]):
    ax.text(x, -0.05 * YMAX, f"{x:g}", ha="center", va="top", fontsize=8.5)
ax.text(0, -0.05 * YMAX, r"$O$", ha="center", va="top")

out = Path(__file__).with_suffix("")
fig.savefig(f"{out}.pdf")
fig.savefig(f"{out}.png", dpi=200)
print(f"A = {A:.2f} mm2, D = {D:.2f} mm; D_LAD = {np.median(D_lad):.2f}, D_LCx = {np.median(D_cx):.2f} mm")
