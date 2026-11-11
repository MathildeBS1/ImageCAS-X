"""Figure for Section sec:method-curvature (fig:method-turning-3d): one turning angle in 3D and its shadow.

    python Thesis_coronary/content/methodology/figures/turning_angle_3d.py

A made-up artery (no patient data) that runs in the floor plane and then rises out of it. At one point
P the chord ends B and F, 5 mm away in a straight line, come from chord_point of
CGPS_data/thesis_final/curvature_feature.py (until 2026-11-10 _at_chord of tortuosity/curvature.py, the
same solver), and the angle is computed as in curvature_profile (atan2 of |a x b| and a . b) (A). The same three points
seen from above, as on a 2D image, turn by less (B): a projection hides part of the turn. Remade 2026-11-09 from
useful_from_week/turning_angle_3d.png (hand-set vectors) with the real chord code. Writes
turning_angle_3d.{pdf,png} next to this file. Thesis style: serif, white, no title.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import proj3d

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "CGPS_data" / "thesis_final"))
from curvature_feature import CHORD, chord_point as _at_chord  # noqa: E402
sys.path.insert(0, str(ROOT / "Thesis_coronary" / "setup"))
from figure_colours import GRID, INK, INK2, MUTED, SERIES, SHADOW as SH, SURF  # noqa: E402

CA, CB = SERIES[:2]  # arriving chord, leaving chord

plt.rcParams.update({"font.family": "serif", "font.serif": ["STIX Two Text", "STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix", "font.size": 9, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF})

# ---------------------------------------------------------------- made-up artery
# Straight along x in the floor plane (z = 0) up to u = 0, then a circular bend of radius R in a plane
# tilted out of the floor, so the turn goes partly sideways (y) and partly upwards (z).
R, N = 4.0, np.array([0.0, 0.6, 0.8])  # bend radius (mm) and the direction the bend turns towards
u = np.linspace(-9, 7, 4000)
up = np.clip(u, 0, None)
dense = np.where(u[:, None] < 0, np.c_[u, 0 * u, 0 * u],
                 np.c_[R * np.sin(up / R), 0 * u, 0 * u] + (R * (1 - np.cos(up / R)))[:, None] * N)
ds = np.r_[0, np.cumsum(np.linalg.norm(np.diff(dense, axis=0), axis=1))]
rng = np.random.default_rng(4)
s = np.r_[0, np.cumsum(rng.uniform(0.5, 1.6, 40))]
s = s[s <= ds[-1]]
P = np.c_[[np.interp(s, ds, dense[:, k]) for k in range(3)]].T
i = int(np.argmin(np.abs(P[:, 0])))  # the point where the artery starts to rise
Bp, Fp = _at_chord(P, i, CHORD, -1), _at_chord(P, i, CHORD, 1)
a, b = P[i] - Bp, Fp - P[i]
theta = np.arctan2(np.linalg.norm(np.cross(a, b)), a @ b)
a2, b2 = a * [1, 1, 0], b * [1, 1, 0]  # the chords dropped onto the floor
theta2 = np.arctan2(np.linalg.norm(np.cross(a2, b2)), a2 @ b2)
Z0 = 0.0  # floor


def arc(centre, u1, u2, r, n=40):
    """Points of the circular arc of radius r from direction u1 to u2 around centre (in their plane)."""
    u1, u2 = u1 / np.linalg.norm(u1), u2 / np.linalg.norm(u2)
    w = np.arccos(np.clip(u1 @ u2, -1, 1))
    t = np.linspace(0, 1, n)[:, None]
    return centre + r * (np.sin((1 - t) * w) * u1 + np.sin(t * w) * u2) / np.sin(w)


fig = plt.figure(figsize=(6.5, 2.7))
ax = fig.add_axes([0.0, -0.12, 0.60, 1.26], projection="3d")
ax.view_init(elev=24, azim=-62)

# ---------------------------------------------------------------- A: the angle in 3D
# axes first (equal scale, panes off, light grid), so that the label positions below project correctly
lo, hi = P.min(axis=0), P.max(axis=0)
LIM = ((lo[0], hi[0]), (-1.0, 5.0), (Z0, hi[2] + 0.3))
ax.set(xlim=LIM[0], ylim=LIM[1], zlim=LIM[2])
ax.set_box_aspect([l1 - l0 for l0, l1 in LIM])
for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.set_pane_color((1, 1, 1, 0))
    axis._axinfo["grid"].update(color=GRID, linewidth=0.5)
    axis.set_tick_params(colors=INK2, labelsize=7, pad=-2)
    axis.line.set_color(MUTED)
ax.set_xticks([-8, -4, 4, 8])
ax.set_yticks([0, 4])
ax.set_zticks([0, 2, 4])
ax.set_xlabel("x (mm)", color=INK2, fontsize=8, labelpad=-6)
ax.set_ylabel("y (mm)", color=INK2, fontsize=8, labelpad=-9)
ax.set_zlabel("z (mm)", color=INK2, fontsize=8, labelpad=-9)
ax.text2D(0.02, 0.80, "A", transform=ax.transAxes, fontsize=12, color=INK)


def label(xyz, text, dx, dy, color=INK, size=10, ha="center", va="center"):
    """Text at the projected position of the 3D point xyz, shifted by (dx, dy) points on the page."""
    x2, y2, _ = proj3d.proj_transform(*xyz, ax.get_proj())
    ax.annotate(text, (x2, y2), xytext=(dx, dy), textcoords="offset points", color=color, fontsize=size,
                ha=ha, va=va, zorder=10)


ax.plot(P[:, 0], P[:, 1], np.full(len(P), Z0), color=GRID, lw=1.2, zorder=1)  # shadow of the artery
for q in P[P[:, 2] > 0.05][::2]:
    ax.plot([q[0]] * 2, [q[1]] * 2, [Z0, q[2]], ls=":", color=GRID, lw=0.7)
ax.plot(*P.T, color=INK2, lw=1.0, zorder=2)
ax.plot(*P.T, "o", color=INK2, ms=2.4, mew=0, zorder=3)
for start, vec, c in ((Bp, a, CA), (P[i], b, CB)):
    ax.quiver(*start, *vec, color=c, lw=2.0, arrow_length_ratio=0.14, zorder=5)
ext = P[i] + a / np.linalg.norm(a) * CHORD
ax.plot(*np.c_[P[i], ext], ls="--", color=CA, lw=0.9, alpha=0.8)
A3 = arc(P[i], a, b, 2.4)
ax.plot(*A3.T, color=CB, lw=1.4, zorder=6)
ax.scatter(*P[i], s=34, color=INK, zorder=7, depthshade=False)
ax.scatter(*np.c_[Bp, Fp], s=28, facecolor=SURF, edgecolor=INK, marker="D", lw=1.1, zorder=7, depthshade=False)
label(Bp + a / 2, r"$\mathbf{a}$", 0, 9, CA, 11)
label(Bp + a / 2, f"{CHORD:.0f} mm", 0, -9, INK2, 8)
label(P[i] + b / 2, r"$\mathbf{b}$", -10, 7, CB, 11)
label(Fp, rf"$\theta$ = {np.degrees(theta):.1f}°", 4, -24, CB, 10, "left")
label(P[i], "$P$", 2, -11)
label(Bp, "$B$", -8, 8)
label(Fp, "$F$", 9, 6)

# ---------------------------------------------------------------- B: seen from above
ax2 = fig.add_axes([0.705, 0.2, 0.285, 0.62])
ax2.text(-0.12, 1.04, "B", transform=ax2.transAxes, fontsize=12, color=INK, va="bottom")
ax2.plot(P[:, 0], P[:, 1], color=GRID, lw=1.2, zorder=1)
ax2.plot(P[:, 0], P[:, 1], "o", color=MUTED, ms=2.2, mew=0, zorder=2)
for q0, vec in ((Bp, a2), (P[i], b2)):
    ax2.annotate("", (q0 + vec)[:2], q0[:2], arrowprops=dict(arrowstyle="-|>", color=SH, lw=1.8,
                 mutation_scale=9, shrinkA=0, shrinkB=0), zorder=4)
ext2 = P[i] + a2 / np.linalg.norm(a2) * CHORD
ax2.plot(*np.c_[P[i, :2], ext2[:2]], ls="--", color=SH, lw=0.9)
A2 = arc(P[i] * [1, 1, 0], a2, b2, 2.4)
ax2.plot(A2[:, 0], A2[:, 1], color=SH, lw=1.3)
ax2.text(A2[0, 0] + 0.3, A2[0, 1] - 0.35, f"{np.degrees(theta2):.1f}°", color=INK2, fontsize=10,
         ha="left", va="top")
ax2.plot(*P[i, :2], "o", color=INK, ms=5, zorder=5)
ax2.plot(*np.c_[Bp[:2], Fp[:2]], "D", mfc=SURF, mec=INK, ms=4.5, mew=1.1, zorder=5)
for q, t_, dx, dy in ((P[i], "$P$", -0.3, -0.7), (Bp, "$B$", 0, 0.7), (Fp, "$F$", 0.6, 0.3)):
    ax2.text(q[0] + dx, q[1] + dy, t_, color=INK, fontsize=10, ha="center", va="center")
ax2.set(xlim=(-6, 5), ylim=(-2.0, 3.5), aspect="equal")
ax2.set_xticks([-4, 0, 4])
ax2.set_yticks([0, 2])
ax2.tick_params(colors=INK2, labelsize=7, length=2.5)
for k, sp in ax2.spines.items():
    sp.set_visible(k in ("left", "bottom"))
    sp.set_color(MUTED)
ax2.set_xlabel("x (mm)", color=INK2, fontsize=8)
ax2.set_ylabel("y (mm)", color=INK2, fontsize=8)

out = Path(__file__).with_suffix("")
for ext_ in ("pdf", "png"):
    fig.savefig(f"{out}.{ext_}", dpi=220)
print(f"wrote {out}.pdf/.png; theta 3D = {np.degrees(theta):.1f} deg, in the shadow = {np.degrees(theta2):.1f} deg")
