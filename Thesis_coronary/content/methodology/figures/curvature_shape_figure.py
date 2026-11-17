"""Figure for Section sec:method-fpca (fig:method-fpca): from the curvature profile of an artery to a curve on
the shared positions 0 to 1.

    python Thesis_coronary/content/methodology/figures/curvature_shape_figure.py

Made-up arteries (no patient data) with unevenly spaced points and made-up p/m boundaries, run through the real
curvature_profile of CGPS_data/thesis_final/curvature_feature.py. A, the curvature profile of one artery in mm,
with its proximal segment shaded; B, that segment placed on 50 positions from its first (0) to its last (1)
profile point, together with the same segment of other made-up arteries and their mean.
on_grid repeats CGPS_data/turning_profile_shapes.on_grid (midpoint positions, linear interpolation), which
cannot be imported here without the server modules.
Writes curvature_shape_figure.{pdf,png} next to this file. Thesis style: serif, white, no title.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "CGPS_data" / "thesis_final"))
sys.path.insert(0, str(ROOT / "Thesis_coronary" / "setup"))
from curvature_feature import CHORD, curvature_profile  # noqa: E402
from figure_colours import GRID, INK, INK2, MUTED, SERIES, SURF  # noqa: E402

GRID_N = 50
MIN_PTS = 5

plt.rcParams.update({"font.family": "serif", "font.serif": ["STIX Two Text", "STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix", "font.size": 8.5, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF})


def artery(rng, bend_at, bend_size, length=70.0):
    """A made-up planar artery: (points, arc length) with a bend of the given size at bend_at mm and a second,
    fixed bend further down, sampled at unevenly spaced points."""
    u = np.linspace(0, length, 15000)
    k = bend_size * np.exp(-((u - bend_at) / 4.0) ** 2) - 0.08 * np.exp(-((u - 48) / 5.0) ** 2)
    head = np.r_[0, np.cumsum((k[1:] + k[:-1]) / 2 * np.diff(u))]
    xy = np.c_[np.r_[0, np.cumsum(np.cos(head[:-1]) * np.diff(u))], np.r_[0, np.cumsum(np.sin(head[:-1]) * np.diff(u))]]
    sp = np.r_[0, np.cumsum(rng.uniform(0.5, 1.6, 200))]
    sp = sp[sp <= u[-1]]
    P = np.c_[np.interp(sp, u, xy[:, 0]), np.interp(sp, u, xy[:, 1]), np.zeros(len(sp))]
    return P, np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]


def on_grid(pos, kappa, lo, hi, n_grid=GRID_N):
    """The profile inside [lo, hi) on n_grid positions between its first (0) and last (1) point."""
    k = (pos >= lo) & (pos < hi)
    if k.sum() < MIN_PTS:
        return None
    p, t = pos[k], kappa[k]
    return np.interp((np.arange(n_grid) + 0.5) / n_grid, (p - p[0]) / (p[-1] - p[0]), t)


rng = np.random.default_rng(3)
t = (np.arange(GRID_N) + 0.5) / GRID_N

# the example artery, and eleven more whose proximal bend differs in place and size
P, s = artery(rng, bend_at=17.0, bend_size=0.14)
pos, kappa = curvature_profile(P, CHORD, s)
PM = 30.0  # made-up proximal/mid boundary, mm along the artery
example = on_grid(pos, kappa, 0.0, PM)
others = []
for _ in range(11):
    Pi, si = artery(rng, bend_at=rng.uniform(11, 23), bend_size=rng.uniform(0.04, 0.18))
    pi, ki = curvature_profile(Pi, CHORD, si)
    others.append(on_grid(pi, ki, 0.0, rng.uniform(26, 36)))
curves = np.array([example] + others)

fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.7), gridspec_kw={"width_ratios": (1.25, 1)})
for ax in (a, b):
    ax.grid(color=GRID, lw=0.5)
    ax.tick_params(colors=INK2, labelsize=7.5)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.set_ylabel(r"curvature (mm$^{-1}$)", color=INK2)

seg = (pos >= 0.0) & (pos < PM)
a.axvspan(pos[seg][0], pos[seg][-1], color=SERIES[0], alpha=0.18, lw=0)
a.axvline(PM, color=MUTED, lw=0.8, ls=":")
a.plot(pos, kappa, color=INK, lw=1.2)
a.plot(pos[seg], kappa[seg], color=SERIES[2], lw=1.6)
top = kappa.max() * 1.22
a.text((pos[seg][0] + pos[seg][-1]) / 2, top * 0.97, "proximal segment", ha="center", va="top", color=INK2, fontsize=8)
a.text(pos[seg][0], -0.012, "0", ha="center", va="top", color=SERIES[2], fontsize=8, fontweight="bold")
a.text(pos[seg][-1], -0.012, "1", ha="center", va="top", color=SERIES[2], fontsize=8, fontweight="bold")
a.set_xlim(0, s[-1])
a.set_ylim(-0.03, top)
a.set_xlabel("distance along the artery (mm)", color=INK2)
a.set_title("A", loc="left", fontsize=10, fontweight="bold", color=INK)

for c in others:
    b.plot(t, c, color=MUTED, lw=0.7, alpha=0.7)
b.plot(t, curves.mean(0), color=INK, lw=1.6, ls="--", label="mean")
b.plot(t, example, color=SERIES[2], lw=1.4)
b.plot(t, example, "o", color=SERIES[2], ms=2.4, label="segment of A")
b.set_xlim(0, 1)
b.set_ylim(-0.03, top)
b.set_xlabel(r"position $t$ along the segment", color=INK2)
b.legend(frameon=False, fontsize=7.5, loc="upper right")
b.set_title("B", loc="left", fontsize=10, fontweight="bold", color=INK)

fig.tight_layout()
out = Path(__file__).with_suffix("")
for ext in ("pdf", "png"):
    fig.savefig(f"{out}.{ext}", dpi=220)
print(f"wrote {out}.pdf and .png; {len(curves)} curves on {GRID_N} positions")
