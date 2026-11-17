"""Figure for Section sec:method-taper (fig:method-taper): from lumen contours to the taper of each segment.

    python Thesis_coronary/content/methodology/figures/taper_figure.py

A made-up LAD (no patient data) with unevenly spaced points and irregular lumen contours, run through the real
code of CGPS_data/thesis_final/taper_feature.py (keep_mask, segment_taper) and daughter_ratio.contour_diameter.
The lumen narrows by a fixed fraction per mm, widens towards the bifurcation point O and steps down at the
two side-branch origins (D1, D2), which are also the segment boundaries.
A, the artery with its centerline, the side branches and the excluded stretches (first 3 mm and K median radii
either side of each branch origin). B, ln D against arc length, kept points filled and excluded points hollow,
with the Theil-Sen line and tau of each segment.
Writes taper_figure.{pdf,png} next to this file. Thesis style as daughter_ratio_figure.py: serif, white, no title.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import theilslopes

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "CGPS_data" / "thesis_final"))
from daughter_ratio import contour_diameter  # noqa: E402
from taper_feature import K, START_MM, keep_mask, segment_taper  # noqa: E402

INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#dcdbd6", "white"
LUMEN = "#e4e3de"
OUT = "#b9b8b2"  # excluded stretches
SEG = {0: "#2a78d6", 1: "#1a9e77", 2: "#eb6834"}
NAME = {0: "proximal", 1: "mid", 2: "distal"}

plt.rcParams.update({"font.family": "serif", "font.serif": ["STIX Two Text", "STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix", "font.size": 8.5, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF})
rng = np.random.default_rng(5)

# ---------------------------------------------------------------- made-up LAD
L, BR = 80.0, (22.0, 50.0)  # length and the side-branch origins (D1, D2) = segment boundaries
BOUNDS = (0.0, BR[0], BR[1], L)
u = np.linspace(0, L, 4000)
head = np.radians(-8) + 0.10 * np.sin(u / 14)  # a gently bending artery in the plane
dense = np.c_[np.r_[0, np.cumsum(np.cos(head[:-1]) * np.diff(u))], np.r_[0, np.cumsum(np.sin(head[:-1]) * np.diff(u))]]
s = np.r_[0, np.cumsum(rng.uniform(0.3, 0.9, 400))]
s = s[s <= L]
Y = np.c_[np.interp(s, u, dense[:, 0]), np.interp(s, u, dense[:, 1]), np.zeros(len(s))]
T = np.c_[np.cos(np.interp(s, u, head)), np.sin(np.interp(s, u, head)), np.zeros(len(s))]
step = np.where(s > BR[0], 0.86, 1.0) * np.where(s > BR[1], 0.88, 1.0)
d_nom = 3.6 * np.exp(-0.005 * s) * step * (1 + 0.35 * np.exp(-s / 1.5))  # taper, steps, confluence at O
for b in BR:  # the lumen flares into each branch origin
    d_nom *= 1 + 0.30 * np.exp(-((s - b) / 0.9) ** 2)


def ring(y, t, d, m=180):
    """Irregular closed lumen contour around y in the plane perpendicular to t, nominal diameter d."""
    e1 = np.cross(t, [0, 0, 1.0])
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(t, e1)
    a = np.linspace(0, 2 * np.pi, m, endpoint=False)
    ph = rng.uniform(0, 2 * np.pi, 2)
    r = d / 2 * (1 + 0.08 * np.cos(2 * a + ph[0]) + 0.04 * np.sin(3 * a + ph[1])) * np.exp(rng.normal(0, 0.025))
    return y + r[:, None] * (np.cos(a)[:, None] * e1 + np.sin(a)[:, None] * e2)


D = np.array([contour_diameter(ring(y, t, d)) for y, t, d in zip(Y, T, d_nom)])  # the real code
branch_s = (0.0,) + BR  # the LCx leaves at O, s = 0
keep = keep_mask(s, branch_s, D)
tau = [segment_taper(s, D, keep, lo, hi) for lo, hi in zip(BOUNDS[:-1], BOUNDS[1:])]
reach = K * np.nanmedian(D) / 2


def letter(ax, c):
    top = ax.get_subplotspec().get_position(ax.figure).y1
    ax.figure.text(0.015, top, c, fontsize=11, color=INK, va="top", ha="left")


def band(Y, T, d, m):
    N = np.c_[-T[:, 1], T[:, 0]]
    P = Y[:, :2]
    up, dn = P + N * d[:, None] / 2, P - N * d[:, None] / 2
    return np.r_[up[m], dn[m][::-1]]


def runs(mask):
    """(start, end) index pairs of the True runs of mask."""
    e = np.flatnonzero(np.diff(np.r_[0, mask.astype(int), 0]))
    return list(zip(e[::2], e[1::2]))


fig = plt.figure(figsize=(6.4, 4.9))
gs = fig.add_gridspec(2, 1, height_ratios=[0.55, 1.0], hspace=0.16, left=0.10, right=0.98, top=0.99, bottom=0.09)

# ---------------------------------------------------------------- A: the artery and what is left out
ax = fig.add_subplot(gs[0])
letter(ax, "A")
for b, lab in zip(BR, ("D1", "D2")):  # side branches
    j = int(np.argmin(np.abs(s - b)))
    n = np.r_[-T[j, 1], T[j, 0]]
    h = np.arctan2(*(n[:2] * 0.9 + T[j, :2])[::-1])
    w = np.linspace(0, 9, 30)
    st = np.c_[Y[j, 0] + w * np.cos(h), Y[j, 1] + w * np.sin(h), 0 * w]
    Ts = np.c_[np.cos(h) + 0 * w, np.sin(h) + 0 * w, 0 * w]
    ax.fill(*band(st, Ts, np.full(len(w), 1.7), np.ones(len(w), bool)).T, color=LUMEN, lw=0, zorder=1)
    ax.text(*(st[-1, :2] + [0.6, 0.6]), lab, fontsize=7.5, color=INK2, ha="left", va="bottom")
ax.fill(*band(Y, T, d_nom, np.ones(len(s), bool)).T, color=LUMEN, lw=0, zorder=1)
idx = np.arange(len(s))
for a, b in runs(~keep):
    ax.fill(*band(Y, T, d_nom, (idx >= max(a - 1, 0)) & (idx < b)).T, color=OUT, lw=0, zorder=2)
for part, (lo, hi) in enumerate(zip(BOUNDS[:-1], BOUNDS[1:])):
    m = (s >= lo) & (s <= hi)
    ax.plot(*Y[m, :2].T, color=SEG[part], lw=1.1, zorder=3)
    jm = int(np.argmin(np.abs(s - (lo + hi) / 2)))
    n = np.r_[-T[jm, 1], T[jm, 0]]
    ax.text(*(Y[jm, :2] - n[:2] * 3.6), NAME[part], color=SEG[part], fontsize=8, ha="center", va="top")
for b in BR:  # segment boundaries
    j = int(np.argmin(np.abs(s - b)))
    n = np.r_[-T[j, 1], T[j, 0]]
    ax.plot(*np.c_[Y[j, :2] - n[:2] * 2.6, Y[j, :2] + n[:2] * 2.6], color=INK2, lw=0.7, ls=(0, (2, 1.5)), zorder=4)
ax.plot(*Y[:, :2].T, "o", color=SURF, mec=INK2, ms=1.4, mew=0.4, zorder=3)
ax.plot(0, 0, "o", color=INK, ms=4, zorder=5)
ax.text(-1.0, 0.4, "$O$", fontsize=10, ha="right", va="bottom")
ax.text(Y[-1, 0] + 1.0, Y[-1, 1], "LAD", fontsize=9, color=INK2, ha="left", va="center")
ax.add_patch(plt.Rectangle((0.0, -14.5), 1.6, 1.6, color=OUT, lw=0))
ax.text(2.2, -13.7, f"left out: first {START_MM:g} mm and {K:g} median radii\n"
        f"({reach:.1f} mm) either side of a side-branch origin", fontsize=7.5, color=INK2, va="center")
ax.set(aspect="equal", xlim=(-4, Y[-1, 0] + 6), ylim=(-17, 11))
ax.axis("off")

# ---------------------------------------------------------------- B: ln D against arc length, Theil-Sen per segment
ax = fig.add_subplot(gs[1])
letter(ax, "B")
for a, b in runs(~keep):
    ax.axvspan(s[max(a - 1, 0)], s[b - 1], color=OUT, alpha=0.45, lw=0)
for b in BR:
    ax.axvline(b, color=INK2, lw=0.7, ls=(0, (2, 1.5)))
lnD = np.log(D)
for part, (lo, hi) in enumerate(zip(BOUNDS[:-1], BOUNDS[1:])):
    m = (s >= lo) & (s < hi)
    k = m & keep
    ax.plot(s[m & ~keep], lnD[m & ~keep], "o", mfc=SURF, mec=SEG[part], ms=2.6, mew=0.6)
    ax.plot(s[k], lnD[k], "o", color=SEG[part], ms=2.6, mew=0)
    b, a0 = theilslopes(lnD[k], s[k])[:2]
    x = np.array([s[k].min(), s[k].max()])
    ax.plot(x, a0 + b * x, color=INK, lw=1.2)
    ax.text((lo + hi) / 2, 1.43, f"{NAME[part]}\n$\\tau$ = {tau[part]:.3f}", color=SEG[part], ha="center",
            va="top", fontsize=8.5, linespacing=1.4)
ax.set(xlabel="arc length $s$ from $O$ (mm)", ylabel=r"$\ln D$  ($D$ in mm)", xlim=(0, L), ylim=(0.55, 1.47))
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
for sp in ("left", "bottom"):
    ax.spines[sp].set_color(INK2)
ax.tick_params(colors=INK2, labelsize=8)
ax.grid(axis="y", color=GRID, lw=0.5)
ax.set_axisbelow(True)

out = Path(__file__).with_suffix("")
for ext in ("pdf", "png"):
    fig.savefig(f"{out}.{ext}", dpi=220)
print(f"wrote {out}.pdf/.png")
print("tau per segment", [round(t, 4) for t in tau], "true 0.05; reach", round(reach, 2), "mm")
