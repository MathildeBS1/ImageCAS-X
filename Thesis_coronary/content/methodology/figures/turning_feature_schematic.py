"""Schematic for Section sec:method-curvature (moved from outdated/thesis_retired/methodology/ 2026-11-09): from centerline points to one average curvature per segment.

    python Thesis_coronary/content/methodology/figures/turning_feature_schematic.py

A made-up artery (no patient data) with unevenly spaced points and made-up p/m/d boundaries, run
through the real code: chord_point, curvature_profile and segment_mean of
CGPS_data/thesis_final/curvature_feature.py (2026-11-10; before, profile_thesis and mean_turning, with
kappa = theta / l). A, the artery; B and C, the circle through the point and its two chord ends (Menger's
formula, menger_curvature) at one point and at a point a few points further on (the earlier window drawn faintly); D, the curvature
profile at every point; E, the arc-length mean per segment. The artery lies in a plane so
that the drawn angles are the computed ones. Writes turning_feature_schematic.{pdf,png} next to this
file. Thesis style: serif, white, no title.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "CGPS_data" / "thesis_final"))
from curvature_feature import CHORD, chord_point as _at_chord, curvature_profile, menger_curvature, segment_mean  # noqa: E402
sys.path.insert(0, str(ROOT / "Thesis_coronary" / "setup"))
from figure_colours import GRID, INK, INK2, MUTED, SERIES as PMD, SURF  # noqa: E402  (PMD: proximal / mid / distal)
HI = (INK, INK2)  # P_i and P_j, kept neutral so they do not clash with the segment colours
NAMES = ("proximal", "mid", "distal")

plt.rcParams.update({"font.family": "serif", "font.serif": ["STIX Two Text", "STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix", "font.size": 9, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF})

# ---------------------------------------------------------------- made-up trunk
u = np.linspace(0, 64, 6000)  # made-up curvature along the trunk, integrated to a heading and a path
k_true = 0.035 * (u < 19) - 0.13 * np.exp(-((u - 30) / 4.0) ** 2) + 0.09 * np.sin(2 * np.pi * (u - 41) / 13) * (u > 41)
head = np.r_[0, np.cumsum((k_true[1:] + k_true[:-1]) / 2 * np.diff(u))] + 0.15
dense = np.c_[np.r_[0, np.cumsum(np.cos(head[:-1]) * np.diff(u))], np.r_[0, np.cumsum(np.sin(head[:-1]) * np.diff(u))]]
ds = np.r_[0, np.cumsum(np.hypot(*np.diff(dense, axis=0).T))]
rng = np.random.default_rng(7)
s = np.r_[0, np.cumsum(rng.uniform(0.4, 1.8, 200))]
s = s[s <= ds[-1]]
P2 = np.c_[np.interp(s, ds, dense[:, 0]), np.interp(s, ds, dense[:, 1])]
P = np.c_[P2, np.zeros(len(P2))]
s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]  # arc length of the polyline itself
END = s[-1]
BOUNDS = (0.0, 20.0, 41.0, END)  # made-up p/m and m/d boundaries, mm along the trunk
pos, kappa = curvature_profile(P, CHORD, s)
part_of = lambda x: np.searchsorted(BOUNDS[1:-1], x, side="right")  # noqa: E731
i0 = int(np.argmin(np.abs(s - 24.5)))  # P_i: on the rising flank of the sharp bend in the mid segment
j0 = int(np.searchsorted(s, s[i0] + 3.0))  # P_j: the first point at least 3 mm further on
CEN = (P2[i0] + P2[j0]) / 2  # centre of the zoom in B and C
HALF = 7.5  # mm, half width of the zoom in B and C


def style(ax, xlabel=None, ylabel=None):
    ax.tick_params(colors=INK2, labelsize=7.5, length=2.5)
    for k, sp in ax.spines.items():
        sp.set_visible(k in ("left", "bottom"))
        sp.set_color(MUTED)
    if xlabel:
        ax.set_xlabel(xlabel, color=INK2, fontsize=8.5)
    if ylabel:
        ax.set_ylabel(ylabel, color=INK2, fontsize=8.5)


def letter(ax, c, x=-0.06, y=1.04):
    ax.text(x, y, c, transform=ax.transAxes, fontsize=12, color=INK, va="bottom")


def trunk(ax, lw=1.4, ms=2.6):
    for k in range(3):
        m = part_of(s) == k
        m[1:] |= m[:-1]  # close the gap at each boundary
        ax.plot(*P2[m].T, color=PMD[k], lw=lw, zorder=1, solid_capstyle="round")
    ax.plot(*P2.T, "o", color=INK2, ms=ms, mew=0, zorder=2)


fig = plt.figure(figsize=(6.5, 8.9))
gs = fig.add_gridspec(4, 2, height_ratios=[1.05, 1.35, 0.9, 0.9], hspace=0.5, wspace=0.16,
                      left=0.09, right=0.98, top=0.97, bottom=0.06)

# ---------------------------------------------------------------- A: the trunk
ax = fig.add_subplot(gs[0, :])
letter(ax, "A", -0.06)
trunk(ax)
for b in BOUNDS[1:-1]:
    q = P2[np.argmin(np.abs(s - b))]
    ax.plot([q[0], q[0]], [q[1] - 1.6, q[1] + 1.6], color=INK, lw=1)
for k, (dx, dy) in enumerate(((3.5, -3.5), (-4, 3), (0, 3))):
    q = P2[np.argmin(np.abs(s - (BOUNDS[k] + BOUNDS[k + 1]) / 2))]
    ax.text(q[0] + dx, q[1] + dy, NAMES[k], color=PMD[k], fontsize=8.5, ha="center", va="center")
ax.annotate("start of artery", P2[0], xytext=(P2[0, 0] + 1, P2[0, 1] - 5.5), fontsize=8, color=INK2,
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
box = (CEN[0] - HALF, CEN[1] - HALF)
ax.add_patch(Rectangle(box, 2 * HALF, 2 * HALF, fill=False, ls="--", lw=0.8, color=INK2))
ax.text(box[0] - 0.4, box[1] + 2 * HALF, "B, C", fontsize=8, color=INK2, ha="right", va="top")
ax.text(0.99, 0.03, f"{len(P)} points, spacing {np.diff(s).min():.1f}–{np.diff(s).max():.1f} mm",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=8, color=INK2)
ax.set_aspect("equal")
ax.set_xlim(-2, P2[:, 0].max() + 4)
ax.set_ylim(P2[:, 1].min() - 6.5, max(P2[:, 1].max(), CEN[1] + HALF) + 1)
style(ax, "x (mm)", "y (mm)")

# ---------------------------------------------------------------- B, C: the circle through B, P, F
def circumcentre(p1, p2, p3):
    """Centre of the circle through three points in the plane."""
    d = 2 * (p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1]))
    sq = [q @ q for q in (p1, p2, p3)]
    return np.array([sq[0] * (p2[1] - p3[1]) + sq[1] * (p3[1] - p1[1]) + sq[2] * (p1[1] - p2[1]),
                     sq[0] * (p3[0] - p2[0]) + sq[1] * (p1[0] - p3[0]) + sq[2] * (p2[0] - p1[0])]) / d


kappa_at, chords = {}, {}
for col, i in enumerate((i0, j0)):
    ax = fig.add_subplot(gs[1, col])
    letter(ax, "BC"[col], -0.14, 1.13)
    c = HI[col]
    Bp, Fp = _at_chord(P, i, CHORD, -1), _at_chord(P, i, CHORD, 1)
    k_i = menger_curvature(Bp, P[i], Fp)
    kappa_at[i], chords[i] = k_i, (Bp, P[i], Fp)
    trunk(ax, lw=1.0, ms=3.6)
    if col == 1:  # the window of B, left behind
        ax.plot(*np.array(chords[i0])[:, :2].T, color=HI[0], lw=1.3, ls=(0, (3, 2)), alpha=0.45, zorder=3)
        ax.plot(*chords[i0][1][:2], "o", color=HI[0], ms=5.5, alpha=0.45, zorder=3)
    ax.add_patch(plt.Circle(P[i, :2], CHORD, fill=False, ls=":", color=INK2, lw=0.9))
    O = circumcentre(Bp[:2], P[i, :2], Fp[:2])
    ax.add_patch(plt.Circle(O, 1 / k_i, fill=False, ls="--", color=c, lw=1.2, zorder=3))
    tri = np.array([Bp[:2], P[i, :2], Fp[:2], Bp[:2]])
    ax.fill(tri[:, 0], tri[:, 1], color=c, alpha=0.12, lw=0, zorder=3)
    ax.plot(tri[:, 0], tri[:, 1], color=c, lw=1.6, zorder=4)
    ax.plot(*P[i, :2], "o", color=c, ms=7, zorder=5, mfc=c if col == 0 else SURF, mew=1.6)
    ax.plot(*np.c_[Bp[:2], Fp[:2]], "D", mfc=SURF, mec=c, ms=5.5, mew=1.4, zorder=5)
    lab = "i" if col == 0 else "j"
    tb, tf = (P[i] - Bp)[:2], (Fp - P[i])[:2]
    tb, tf = tb / np.linalg.norm(tb), tf / np.linalg.norm(tf)
    lft = lambda v: np.array([-v[1], v[0]])  # noqa: E731, left of the chord
    for q, txt, off in ((P[i], rf"$P_{{{lab}}}$", -1.2 * lft(tb + tf) / np.linalg.norm(tb + tf)),
                        (Bp, rf"$B_{{{lab}}}$", 1.1 * lft(tb)), (Fp, rf"$F_{{{lab}}}$", 1.0 * tf + 0.6 * lft(tf))):
        ax.text(*(q[:2] + off), txt, color=c, fontsize=9, ha="center", va="center")
    ax.text(0.03, 0.97, rf"circle through $B_{{{lab}}}$, $P_{{{lab}}}$, $F_{{{lab}}}$: $R$ = {1 / k_i:.1f} mm" + "\n"
            + rf"$\kappa_{{{lab}}} = 1/R$ = {k_i:.3f} mm$^{{-1}}$",
            transform=ax.transAxes, fontsize=8.5, color=c, va="top", ha="left", zorder=6,
            bbox=dict(fc=SURF, ec="none", pad=1.0))
    if col == 0:
        ax.set_title(r"$B$, $F$: $\ell$ = 5 mm away in a straight line (dotted)," + "\nmostly between two points",
                     fontsize=8, color=INK2, loc="left")
    else:
        ax.set_title(f"{j0 - i0} points ({s[j0] - s[i0]:.1f} mm) further on: the window has\nmoved, and the tighter bend gives a smaller circle",
                     fontsize=8, color=INK2, loc="left")
    ax.set(xlim=(CEN[0] - HALF, CEN[0] + HALF), ylim=(CEN[1] - HALF, CEN[1] + HALF), aspect="equal")
    style(ax, "x (mm)", "y (mm)" if col == 0 else None)

# ---------------------------------------------------------------- D, E: profile and segment means
ymax = kappa.max() * 1.18


def segments(ax):
    for k in range(3):
        ax.axvspan(BOUNDS[k], BOUNDS[k + 1], color=PMD[k], alpha=0.07, lw=0)
    for b in BOUNDS[1:-1]:
        ax.axvline(b, color=INK, lw=0.8)
    for lo, hi in ((0, CHORD), (END - CHORD, END)):
        ax.add_patch(Rectangle((lo, 0), hi - lo, ymax, fill=False, hatch="////", ec=GRID, lw=0))
    ax.set_xlim(0, END)
    ax.set_ylim(0, ymax)


ax = fig.add_subplot(gs[2, :])
letter(ax, "D", -0.06)
segments(ax)
ax.plot(pos, kappa, color=MUTED, lw=0.9, zorder=2)
ax.plot(pos, kappa, "o", color=INK2, ms=2.6, mew=0, zorder=3)
for col, i in enumerate((i0, j0)):
    ax.plot(s[i], kappa_at[i], "o", color=HI[col], mfc=HI[col] if col == 0 else SURF, ms=6.5,
            mew=1.6, zorder=4)
    ax.annotate(rf"$P_{{{'ij'[col]}}}$", (s[i], kappa_at[i]), xytext=(-9, 3 if col == 0 else 5),
                textcoords="offset points", ha="right", fontsize=8.5, color=HI[col])
ax.plot(s, np.full_like(s, ymax * 0.03), "|", color=INK2, ms=4, mew=0.6)
for x in (CHORD / 2, END - CHORD / 2):
    ax.text(x, ymax * 0.5, "no\nvalue", ha="center", va="center", fontsize=7, color=INK2,
            bbox=dict(fc=SURF, ec="none", pad=0.8))
for k in range(3):
    ax.text((BOUNDS[k] + BOUNDS[k + 1]) / 2, ymax * 0.98, NAMES[k], color=PMD[k], fontsize=8.5,
            ha="center", va="top")
style(ax, None, r"$\kappa$ (mm$^{-1}$)")
ax.set_title("one value at every point; ticks mark the uneven point spacing", fontsize=8.5, color=INK2, loc="left")

ax = fig.add_subplot(gs[3, :])
letter(ax, "E", -0.06)
segments(ax)
ax.plot(pos, kappa, color=MUTED, lw=0.9, zorder=2)
for k in range(3):
    m = (pos >= BOUNDS[k]) & (pos < BOUNDS[k + 1])
    p, t = pos[m], kappa[m]
    T = segment_mean(pos, kappa, BOUNDS[k], BOUNDS[k + 1])
    ax.fill_between(p, 0, t, color=PMD[k], alpha=0.35, lw=0, zorder=1)
    ax.plot([p[0], p[-1]], [T, T], color=PMD[k], lw=2, zorder=3)
    ax.text((p[0] + p[-1]) / 2, ymax * 0.97, rf"$T$ = {T:.3f}", color=PMD[k], fontsize=8.5,
            ha="center", va="top", zorder=4)
style(ax, "arc length along the artery (mm)", r"$\kappa$ (mm$^{-1}$)")
ax.set_title("one average curvature per segment: the area under the profile divided by the length it covers",
             fontsize=8.5, color=INK2, loc="left")

out = Path(__file__).with_suffix("")
for ext in ("pdf", "png"):
    fig.savefig(f"{out}.{ext}", dpi=200)
print(f"wrote {out}.pdf/.png; segment means:",
      [round(segment_mean(pos, kappa, lo, hi), 4) for lo, hi in zip(BOUNDS[:-1], BOUNDS[1:])])
