"""Figure for Section sec:method-curvature (fig:method-curvature): curvature as the inverse radius of a circle,
from three centerline points to one average curvature per segment.

    python Thesis_coronary/content/methodology/figures/curvature_figure.py

A made-up artery (no patient data) with unevenly spaced points and made-up p/m/d boundaries, run through the
real code of CGPS_data/thesis_final/curvature_feature.py (chord_point, menger_curvature, curvature_profile,
segment_mean). A, curvature = 1/R on three circles; B, the triangle of a point and its chord ends 5 mm away at
the tight bend, its circle and Menger's formula with its numbers; C, the artery and the circle at a straight,
a gentle and a tight point; D, the curvature profile along the artery and the average curvature T
of each segment. Replaces turning_feature_schematic.py and turning_angle_3d.py in the text (2026-11-10).
2026-11-10 (user): restyled after the inverse-radius sketch (scratchpad inverse_radius.png): coloured circles by
size (blue 20 mm, orange 10 mm, green 5 mm) with their radius and 1/R in A; the green triangle and circle in B;
the gentle (blue) and tight (green) circles on a black artery in C, marked again on the profile in D. Segment
colours dropped from C and D, so the three colours mean circle size only. Panel order and content unchanged, so
the caption and the text still match.
Writes curvature_figure.{pdf,png} next to this file. Thesis style: serif, white, no title.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "CGPS_data" / "thesis_final"))
from curvature_feature import CHORD, chord_point, curvature_profile, menger_curvature, segment_mean  # noqa: E402

INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#dcdbd6", "white"
PMD = ("#2a78d6", "#eb6834", "#1baf7a")  # proximal / mid / distal, as in split_example_figure.py
CIRC = "#52514e"  # circles and triangles: neutral, so they do not compete with the segment colours
NAMES = ("proximal", "mid", "distal")

plt.rcParams.update({"font.family": "serif", "font.serif": ["STIX Two Text", "STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix", "font.size": 8.5, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF})

# ---------------------------------------------------------------- made-up artery
u = np.linspace(0, 92, 20000)  # curvature along the artery (1/mm), integrated to a heading and a path
k_true = 0.05 * np.exp(-((u - 34) / 7) ** 2) - 0.2 * np.exp(-((u - 64) / 3.0) ** 2)
head = np.r_[0, np.cumsum((k_true[1:] + k_true[:-1]) / 2 * np.diff(u))]
dense = np.c_[np.r_[0, np.cumsum(np.cos(head[:-1]) * np.diff(u))], np.r_[0, np.cumsum(np.sin(head[:-1]) * np.diff(u))]]
du = np.r_[0, np.cumsum(np.hypot(*np.diff(dense, axis=0).T))]
rng = np.random.default_rng(7)
sp = np.r_[0, np.cumsum(rng.uniform(0.5, 1.6, 200))]  # unevenly spaced tracer-like points
sp = sp[sp <= du[-1]]
P2 = np.c_[np.interp(sp, du, dense[:, 0]), np.interp(sp, du, dense[:, 1])]
P = np.c_[P2, np.zeros(len(P2))]
s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]  # arc length of the polyline
END = s[-1]
BOUNDS = (0.0, 24.0, 52.0, END)  # made-up p/m and m/d boundaries, mm along the artery
part_of = lambda x: np.searchsorted(BOUNDS[1:-1], x, side="right")  # noqa: E731
pos, kappa = curvature_profile(P, CHORD, s)


def circle_at(i):
    """Chord ends, centre, radius and curvature of the circle through P[i] and its chord ends (2D artery)."""
    B, F = chord_point(P, i, CHORD, -1), chord_point(P, i, CHORD, 1)
    k = menger_curvature(B, P[i], F)
    b, p, f = B[:2], P2[i], F[:2]
    if k < 1e-9:
        return b, p, f, None, np.inf, 0.0
    d = 2 * (b[0] * (p[1] - f[1]) + p[0] * (f[1] - b[1]) + f[0] * (b[1] - p[1]))
    sq = [q @ q for q in (b, p, f)]
    c = np.array([sq[0] * (p[1] - f[1]) + sq[1] * (f[1] - b[1]) + sq[2] * (b[1] - p[1]),
                  sq[0] * (f[0] - p[0]) + sq[1] * (b[0] - f[0]) + sq[2] * (p[0] - b[0])]) / d
    return b, p, f, c, 1 / k, k


def area2d(b, p, f):
    """Area of the triangle b, p, f in the plane."""
    (x1, y1), (x2, y2) = p - b, f - p
    return 0.5 * abs(x1 * y2 - y1 * x2)


def nearest(x):
    return int(np.argmin(np.abs(s - x)))


i_str, i_gen, i_tgt = nearest(12.0), nearest(34.0), nearest(64.0)  # straight, gentle, tight


def letter(ax, c, x=0.0, y=1.0):
    """Panel letter at the left margin of the figure, level with the top of the panel's grid cell."""
    top = ax.get_subplotspec().get_position(ax.figure).y1
    ax.figure.text(0.015, top, c, fontsize=11, color=INK, va="top", ha="left")


def segments_line(ax, lw=1.8):
    for k in range(3):
        m = part_of(s) == k
        m[1:] |= m[:-1]  # close the gap at each boundary
        ax.plot(*P2[m].T, color=PMD[k], lw=lw, zorder=2, solid_capstyle="round")


def draw_circle(ax, c, R, **kw):
    t = np.linspace(0, 2 * np.pi, 400)
    ax.plot(c[0] + R * np.cos(t), c[1] + R * np.sin(t), **kw)


SIZE = ("#2a78d6", "#eb6834", "#1baf7a")  # large / medium / small circle, as in the inverse-radius sketch
NEUT = ("#f1f0ec", "#e4e3de", "#f1f0ec")  # segment shading in D: neutral, so it does not reuse the circle colours
fig = plt.figure(figsize=(6.4, 8.6))
gs = fig.add_gridspec(4, 1, height_ratios=[0.78, 0.72, 1.05, 0.85], hspace=0.14,
                      left=0.10, right=0.99, top=0.99, bottom=0.06)

# ---------------------------------------------------------------- A: curvature = 1/R on three circles
ax = fig.add_subplot(gs[0])
letter(ax, "A", -0.085, 1.0)
x0 = 0.0
for R, col in zip((20.0, 10.0, 5.0), SIZE):
    cx = x0 + R
    draw_circle(ax, (cx, 0), R, color=col, lw=1.8)
    ax.plot([cx, cx + R], [0, 0], color=INK2, lw=0.9)
    ax.plot(cx, 0, "o", color=INK2, ms=2.5)
    if R > 15:
        ax.text(cx + R / 2, 0.9, f"$R$ = {R:.0f} mm", ha="center", va="bottom", fontsize=7.5, color=INK2)
    else:  # too small to hold its label
        ax.text(cx + R + 1.5, 0, f"$R$ = {R:.0f} mm", ha="left", va="center", fontsize=7.5, color=INK2)
    ax.text(cx, 23.0, f"radius {R:.0f} mm\n$\\kappa$ = 1/{R:.0f} = {1 / R:.2f} mm$^{{-1}}$", ha="center",
            va="bottom", fontsize=8.5, color=col, linespacing=1.4)
    x0 = cx + R + 22
ax.set(aspect="equal", xlim=(-4, x0 - 16), ylim=(-21, 34))
ax.axis("off")

# ---------------------------------------------------------------- B: three points, triangle, Menger
ax = fig.add_subplot(gs[1])
letter(ax, "B", -0.085, 1.0)
b, p, f, c, R, k = circle_at(i_tgt)
col = SIZE[2]
win = (s > s[i_tgt] - 11) & (s < s[i_tgt] + 11)
ax.plot(*P2[win].T, color=INK, lw=2.0, zorder=2)
ax.plot(*P2[win].T, "o", color=SURF, mec=INK2, ms=2.4, mew=0.6, zorder=3)
draw_circle(ax, c, R, color=col, lw=1.1, ls=(0, (4, 2.5)), zorder=1)
ax.plot(*c, "+", color=col, ms=6)
ax.plot(*np.c_[c, p], color=col, lw=0.9)
ax.text(c[0], c[1] - 1.2, f"$R$ = {R:.1f} mm", fontsize=8, color=col, va="top", ha="center")  # below the centre
tri = np.array([b, p, f, b])
ax.fill(tri[:, 0], tri[:, 1], color=col, alpha=0.18, lw=0, zorder=1)
ax.plot(tri[:, 0], tri[:, 1], color=col, lw=1.1, zorder=4)
for q in (b, p, f):
    ax.plot(*q, "o", color=INK, ms=5, zorder=6)
nrm = (p - (b + f) / 2) / np.linalg.norm(p - (b + f) / 2)
ax.text(*(p + 1.3 * nrm), "$P_i$", ha="center", va="center", fontsize=9.5)
for q, name in ((b, "$B_i$"), (f, "$F_i$")):
    ax.text(*(q + 1.3 * nrm + 1.6 * (q - p) / np.linalg.norm(q - p)), name, ha="center", va="center", fontsize=9.5)
ax.annotate("$A_i$", np.mean([b, p, f], axis=0), xytext=(b[0] - 7.0, b[1] - 3.5), fontsize=9, color=col,
            ha="center", arrowprops=dict(arrowstyle="-", color=col, lw=0.6))
bf = np.linalg.norm(f - b)
ax.text(c[0] + R + 6.0, c[1] + 0.5 * R,
        rf"$\kappa_i = \dfrac{{1}}{{R}} = \dfrac{{4A_i}}{{\|P_i-B_i\|\,\|F_i-P_i\|\,\|F_i-B_i\|}}$" + "\n\n"
        + rf"$\;\;\;\;\;\;\;\; = \dfrac{{4 \times {area2d(b, p, f):.2f}}}{{5 \times 5 \times {bf:.2f}}}"
        + rf" = {k:.3f}$ mm$^{{-1}}$",
        ha="left", va="center", fontsize=8.5, color=INK)
ax.set(aspect="equal", xlim=(c[0] - 26, c[0] + 52), ylim=(c[1] - R - 1.5, c[1] + R + 3.5))
ax.axis("off")

# ---------------------------------------------------------------- C: the artery and its circles
ax = fig.add_subplot(gs[2])
letter(ax, "C", -0.085, 1.0)
ax.plot(*P2.T, color=INK, lw=2.0, zorder=2, solid_capstyle="round")
for x in BOUNDS[1:-1]:
    q = P2[nearest(x)]
    ax.plot([q[0], q[0]], [q[1] - 2.0, q[1] + 2.0], color=INK2, lw=0.9, zorder=4)
for k_, (x, y, ha) in enumerate(((6, 3.0, "center"), (45, 4.0, "left"), (82, 12.5, "center"))):
    ax.text(x, y, NAMES[k_], color=INK2, fontsize=8, ha=ha, va="center", style="italic")
for i, col in ((i_str, MUTED), (i_gen, SIZE[0]), (i_tgt, SIZE[2])):
    b, p, f, c, R, k = circle_at(i)
    ax.plot(*p, "o", color=col, ms=6, zorder=6)
    if i == i_str:
        ax.annotate("straight stretch: points on a line,\nno circle, $\\kappa$ = 0", p, xytext=(p[0] + 3, p[1] - 6),
                    fontsize=8, color=INK2, va="top", ha="left", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
        continue
    draw_circle(ax, c, R, color=col, lw=1.1, ls=(0, (4, 2.5)), zorder=1)
    ax.plot(*c, "+", color=col, ms=6, zorder=1)
    ax.plot(*np.c_[c, p], color=col, lw=0.9, zorder=1)
    if i == i_gen:
        ax.text(c[0] - R - 1.5, c[1] + 0.35 * R,
                f"gentle bend: large circle\n$R$ = {R:.0f} mm, $\\kappa$ = {k:.3f} mm$^{{-1}}$",
                fontsize=8, color=col, ha="right", va="center")
    else:
        ax.text(c[0], c[1] - R - 1.5,
                f"tight bend: small circle\n$R$ = {R:.1f} mm, $\\kappa$ = {k:.3f} mm$^{{-1}}$",
                fontsize=8, color=col, ha="center", va="top")
ax.set(aspect="equal", ylim=(P2[:, 1].min() - 13, P2[:, 1].max() + 31))
ax.axis("off")

# ---------------------------------------------------------------- D: profile and segment means
ax = fig.add_subplot(gs[3])
letter(ax, "D", -0.085, 1.0)
ymax = kappa.max() * 1.2
for k_ in range(3):
    ax.axvspan(BOUNDS[k_], BOUNDS[k_ + 1], color=NEUT[k_], lw=0)
    ax.text((BOUNDS[k_] + BOUNDS[k_ + 1]) / 2, ymax * 0.97, NAMES[k_], color=INK2, fontsize=8, ha="center",
            va="top", style="italic")
for x in BOUNDS[1:-1]:
    ax.axvline(x, color=INK2, lw=0.8)
first, last = pos[0], pos[-1]
for lo, hi in ((0, first), (last, END)):
    ax.add_patch(Rectangle((lo, 0), hi - lo, ymax, fc=SURF, hatch="////", ec=GRID, lw=0))
    ax.text((lo + hi) / 2, ymax * 0.5, "no\nvalue", ha="center", va="center", fontsize=7, color=INK2,
            bbox=dict(fc=SURF, ec="none", pad=0.6))
for k_ in range(3):
    m = (pos >= BOUNDS[k_]) & (pos < BOUNDS[k_ + 1])
    T = segment_mean(pos, kappa, BOUNDS[k_], BOUNDS[k_ + 1])
    ax.fill_between(pos[m], 0, kappa[m], color=MUTED, alpha=0.30, lw=0, zorder=1)
    ax.plot([pos[m][0], pos[m][-1]], [T, T], color=INK, lw=1.8, zorder=3)
    tx = (pos[m][0] + pos[m][-1]) / 2 if k_ < 2 else pos[m][0] + 0.78 * (pos[m][-1] - pos[m][0])
    ax.text(tx, T + ymax * 0.04, f"$T$ = {T:.3f}", color=INK, fontsize=8, ha="center", va="bottom", zorder=4,
            bbox=dict(fc=SURF, ec="none", pad=0.6, alpha=0.85))
ax.plot(pos, kappa, color=INK2, lw=0.9, zorder=2)
ax.plot(pos, kappa, "o", color=INK2, ms=1.7, mew=0, zorder=2)
for i, col in ((i_gen, SIZE[0]), (i_tgt, SIZE[2])):  # the two circles of C, found again on the profile
    j = int(np.argmin(np.abs(pos - s[i])))
    ax.plot(pos[j], kappa[j], "o", color=col, ms=5, zorder=5)
ax.set_xlim(0, END)
ax.set_ylim(0, ymax)
ax.tick_params(colors=INK2, labelsize=7.5, length=2.5)
for k_, sp_ in ax.spines.items():
    sp_.set_visible(k_ in ("left", "bottom"))
    sp_.set_color(MUTED)
ax.set_xlabel("arc length along the artery (mm)", color=INK2, fontsize=8.5)
ax.set_ylabel(r"$\kappa$ (mm$^{-1}$)", color=INK2, fontsize=8.5)

out = Path(__file__).with_suffix("")
for ext in ("pdf", "png"):
    fig.savefig(f"{out}.{ext}", dpi=220)
print(f"wrote {out}.pdf/.png")
for i, n in ((i_str, "straight"), (i_gen, "gentle"), (i_tgt, "tight")):
    print(n, "R", round(circle_at(i)[4], 2), "kappa", round(circle_at(i)[5], 4))
print("T", [round(segment_mean(pos, kappa, lo, hi), 4) for lo, hi in zip(BOUNDS[:-1], BOUNDS[1:])])
