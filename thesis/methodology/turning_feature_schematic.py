"""Schematic for Section sec:method-curvature: from centerline points to one mean turning per segment.

    python thesis/methodology/turning_feature_schematic.py

A made-up artery (no patient data) with unevenly spaced points and made-up p/m/d boundaries, run
through the real code: _at_chord and profile_thesis of tortuosity/curvature.py and mean_turning of
CGPS_data/thesis_final/turning_feature.py. A, the trunk; B and C, the angle at one point and at the
next; D, the profile at every point; E, the arc-length mean per segment. The trunk lies in a plane so
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

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "CGPS_data" / "thesis_final"))
from tortuosity.curvature import _at_chord, profile_thesis  # noqa: E402
from turning_feature import CHORD, mean_turning  # noqa: E402

INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#dcdbd6", "white"
PMD = ("#2a78d6", "#eb6834", "#1baf7a")  # proximal / mid / distal, as in split_example_figure.py
HI = ("#5b3cc4", "#b8327a")  # P_i and P_i+1
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
pos, kappa = profile_thesis(P, CHORD, s)
part_of = lambda x: np.searchsorted(BOUNDS[1:-1], x, side="right")  # noqa: E731
i0 = int(np.argmin(np.abs(s - 27.0)))  # P_i: on the sharp bend in the mid segment
HALF = 7.0  # mm, half width of the zoom in B and C


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


fig = plt.figure(figsize=(6.5, 9.0))
gs = fig.add_gridspec(4, 2, height_ratios=[0.9, 1.35, 0.95, 0.95], hspace=0.55, wspace=0.18,
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
box = (P2[i0, 0] - HALF, P2[i0, 1] - HALF)
ax.add_patch(Rectangle(box, 2 * HALF, 2 * HALF, fill=False, ls="--", lw=0.8, color=INK2))
ax.text(box[0] - 0.4, box[1] + 2 * HALF, "B, C", fontsize=8, color=INK2, ha="right", va="top")
ax.text(0.99, 0.02, f"{len(P)} points, spacing {np.diff(s).min():.1f}–{np.diff(s).max():.1f} mm",
        transform=ax.transAxes, ha="right", fontsize=8, color=INK2)
ax.set_aspect("equal")
ax.set_xlim(-2, P2[:, 0].max() + 4)
ax.set_ylim(P2[:, 1].min() - 7, P2[:, 1].max() + 5)
style(ax, "x (mm)", "y (mm)")

# ---------------------------------------------------------------- B, C: angle at P_i and P_i+1
theta_at = {}
for col, i in enumerate((i0, i0 + 1)):
    ax = fig.add_subplot(gs[1, col])
    letter(ax, "BC"[col], -0.14, 1.13)
    c = HI[col]
    Bp, Fp = _at_chord(P, i, CHORD, -1), _at_chord(P, i, CHORD, 1)
    a, b = P[i] - Bp, Fp - P[i]
    theta = np.arctan2(np.linalg.norm(np.cross(a, b)), a @ b)
    theta_at[i] = theta
    trunk(ax, lw=1.0, ms=3.6)
    ax.add_patch(plt.Circle(P[i, :2], CHORD, fill=False, ls=":", color=INK2, lw=0.9))
    for start, vec, name in ((Bp, a, r"$\mathbf{a}$"), (P[i], b, r"$\mathbf{b}$")):
        ax.add_patch(FancyArrowPatch(start[:2], (start + vec)[:2], arrowstyle="-|>", mutation_scale=10,
                                     color=c, lw=1.8, zorder=4, shrinkA=0, shrinkB=0))
        mid = start[:2] + vec[:2] / 2
        nrm = np.array([-vec[1], vec[0]]) / np.linalg.norm(vec[:2])
        ax.text(*(mid + 0.9 * nrm * (1 if name.endswith("a}$") else -1)), name, color=c, fontsize=10,
                ha="center", va="center")
    ext = P[i] + a / np.linalg.norm(a) * CHORD
    ax.plot([P[i, 0], ext[0]], [P[i, 1], ext[1]], ls="--", color=c, lw=0.9, alpha=0.7, zorder=3)
    ax.plot(*P[i, :2], "o", color=c, ms=7, zorder=5)
    ax.plot(*np.c_[Bp[:2], Fp[:2]], "D", mfc=SURF, mec=c, ms=5.5, mew=1.4, zorder=5)
    lab = "i" if col == 0 else "i+1"
    for q, t, dx, dy in ((P[i], rf"$P_{{{lab}}}$", 0.6, -1.0), (Bp, rf"$B_{{{lab}}}$", -1.3, 0.3),
                         (Fp, rf"$F_{{{lab}}}$", 0.2, 1.0)):
        ax.text(q[0] + dx, q[1] + dy, t, color=c, fontsize=9, ha="center", va="center")
    da, db = (np.degrees(np.arctan2(v[1], v[0])) for v in (a, b))
    lo, hi = (da, db) if (db - da) % 360 <= 180 else (db, da)
    ax.add_patch(Arc(P[i, :2], 4.2, 4.2, theta1=lo, theta2=hi, color=c, lw=1.4, zorder=4))
    mid = np.radians(lo + ((hi - lo) % 360) / 2)
    ax.text(P[i, 0] + 2.9 * np.cos(mid), P[i, 1] + 2.9 * np.sin(mid), r"$\theta$", color=c, fontsize=11,
            ha="center", va="center")
    ax.text(0.97, 0.03, rf"$\theta_{{{lab}}}$ = {np.degrees(theta):.1f}°" + "\n"
            + rf"$\kappa_{{{lab}}} = \theta_{{{lab}}}/\ell$ = {theta / CHORD:.3f} rad/mm",
            transform=ax.transAxes, fontsize=8.5, color=c, va="bottom", ha="right")
    if col == 0:
        ax.set_title(r"$B$, $F$: $\ell$ = 5 mm away in a straight line (dotted)," + "\nmostly between two points",
                     fontsize=8, color=INK2, loc="left")
    else:
        ax.set_title(f"the next point, {s[i] - s[i - 1]:.1f} mm further:\nthe window moves with it",
                     fontsize=8, color=INK2, loc="left")
    ax.set(xlim=(P[i0, 0] - HALF, P[i0, 0] + HALF), ylim=(P[i0, 1] - HALF, P[i0, 1] + HALF), aspect="equal")
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
for col, i in enumerate((i0, i0 + 1)):
    ax.plot(s[i], theta_at[i] / CHORD, "o", color=HI[col], ms=6.5, zorder=4)
ax.plot(s, np.full_like(s, ymax * 0.03), "|", color=INK2, ms=4, mew=0.6)
for x in (CHORD / 2, END - CHORD / 2):
    ax.text(x, ymax * 0.5, "no\nvalue", ha="center", va="center", fontsize=7, color=INK2,
            bbox=dict(fc=SURF, ec="none", pad=0.8))
for k in range(3):
    ax.text((BOUNDS[k] + BOUNDS[k + 1]) / 2, ymax * 0.98, NAMES[k], color=PMD[k], fontsize=8.5,
            ha="center", va="top")
style(ax, None, r"$\kappa$ (rad/mm)")
ax.set_title("one value at every point; ticks mark the uneven point spacing", fontsize=8.5, color=INK2, loc="left")

ax = fig.add_subplot(gs[3, :])
letter(ax, "E", -0.06)
segments(ax)
ax.plot(pos, kappa, color=MUTED, lw=0.9, zorder=2)
for k in range(3):
    m = (pos >= BOUNDS[k]) & (pos < BOUNDS[k + 1])
    p, t = pos[m], kappa[m]
    T = mean_turning(pos, kappa, BOUNDS[k], BOUNDS[k + 1])
    ax.fill_between(p, 0, t, color=PMD[k], alpha=0.35, lw=0, zorder=1)
    ax.plot([p[0], p[-1]], [T, T], color=PMD[k], lw=2, zorder=3)
    ax.text((p[0] + p[-1]) / 2, T + ymax * 0.05, rf"$T$ = {T:.3f}", color=PMD[k], fontsize=8.5,
            ha="center", va="bottom", bbox=dict(fc=SURF, ec="none", pad=0.6, alpha=0.85), zorder=4)
ax.text(0.085, 0.95, r"$T_s = \frac{1}{s_{\mathrm{last}} - s_{\mathrm{first}}}\int \kappa(s)\,\mathrm{d}s$", transform=ax.transAxes, ha="left", va="top",
        fontsize=8.5, color=INK, bbox=dict(fc=SURF, ec=GRID, lw=0.6, pad=3))
style(ax, "arc length along the artery (mm)", r"$\kappa$ (rad/mm)")
ax.set_title("one mean turning per segment: the area under the profile divided by the length it covers",
             fontsize=8.5, color=INK2, loc="left")

out = Path(__file__).with_suffix("")
for ext in ("pdf", "png"):
    fig.savefig(f"{out}.{ext}", dpi=200)
print(f"wrote {out}.pdf/.png; segment means:",
      [round(mean_turning(pos, kappa, lo, hi), 4) for lo, hi in zip(BOUNDS[:-1], BOUNDS[1:])])
