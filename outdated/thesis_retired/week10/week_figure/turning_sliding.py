"""Sliding-window turning angle on an unevenly spaced made-up centerline (week10.tex). Uses the real
_at_chord and profile_thesis of tortuosity/curvature.py.

    python3 thesis/week10/week_figure/turning_sliding.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from tortuosity.curvature import _at_chord, profile_thesis  # noqa: E402

INK, INK2, GRID, SURF, MUTED = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb", "#8a8984"
C = ("#2a78d6", "#eb6834")
L = 5.0

rng = np.random.default_rng(3)
t = np.r_[0, np.cumsum(rng.uniform(0.4, 1.8, 40))]
t = t[t <= 32]
P = np.c_[t, 5 * np.sin(t / 4.5), 0 * t]
s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
pos, kappa = profile_thesis(P, L, s)
i0 = int(np.argmin(np.abs(s - 14)))


def style(ax, title, xlabel, ylabel):
    ax.set_facecolor(SURF)
    ax.grid(color=GRID, lw=0.6)
    ax.tick_params(colors=INK2, labelsize=8)
    for sp in ax.spines.values():
        sp.set_color(GRID)
    ax.set_title(title, fontsize=9.5, color=INK, loc="left")
    ax.set_xlabel(xlabel, color=INK2, fontsize=8.5)
    ax.set_ylabel(ylabel, color=INK2, fontsize=8.5)


fig = plt.figure(figsize=(9, 6.4), facecolor=SURF)
gs = fig.add_gridspec(2, 2, height_ratios=[1.25, 1])
for col, i in enumerate((i0, i0 + 1)):
    ax = fig.add_subplot(gs[0, col])
    B, F = _at_chord(P, i, L, -1), _at_chord(P, i, L, 1)
    a, b = P[i] - B, F - P[i]
    theta = np.arctan2(np.linalg.norm(np.cross(a, b)), a @ b)
    step = "" if col == 0 else f", {s[i] - s[i - 1]:.1f} mm further"
    style(ax, f"point $P_{{{'i' if col == 0 else 'i+1'}}}${step}", "x (mm)", "y (mm)")
    ax.plot(P[:, 0], P[:, 1], color=MUTED, lw=1, zorder=1)
    ax.plot(P[:, 0], P[:, 1], "o", color=MUTED, ms=3.5, zorder=2, label="centerline points (uneven)")
    ax.add_patch(plt.Circle(P[i, :2], L, fill=False, ls=":", color=INK2, lw=0.9))
    ax.plot(*np.c_[B[:2], P[i, :2], F[:2]], color=C[col], lw=2, zorder=3)
    ax.plot(*P[i, :2], "o", color=C[col], ms=7, zorder=4)
    ax.plot(*np.c_[B[:2], F[:2]], "D", mfc=SURF, mec=C[col], ms=6, mew=1.5, zorder=4,
            label="5 mm back / ahead (between points)")
    ext = P[i] + a / np.linalg.norm(a) * L
    ax.plot([P[i, 0], ext[0]], [P[i, 1], ext[1]], ls="--", color=C[col], lw=1, alpha=0.6)
    da, db = (np.degrees(np.arctan2(v[1], v[0])) for v in (a, b))
    lo, hi = (da, db) if (db - da) % 360 <= 180 else (db, da)
    ax.add_patch(Arc(P[i, :2], 4, 4, theta1=lo, theta2=hi, color=C[col], lw=1.6, zorder=4))
    mid = np.radians(lo + ((hi - lo) % 360) / 2)
    ax.text(P[i, 0] + 2.8 * np.cos(mid), P[i, 1] + 2.8 * np.sin(mid), r"$\theta$", color=C[col],
            fontsize=11, ha="center", va="center")
    ax.text(0.03, 0.05, rf"$\theta$ = {np.degrees(theta):.1f}°,  $\kappa = \theta/5$ mm = {theta / L:.3f} rad/mm",
            transform=ax.transAxes, fontsize=8.5, color=C[col])
    ax.set(xlim=(P[i, 0] - 7.5, P[i, 0] + 7.5), ylim=(P[i, 1] - 6.5, P[i, 1] + 6.5), aspect="equal")
    ax.legend(frameon=False, fontsize=7, loc="upper left")

ax = fig.add_subplot(gs[1, :])
style(ax, "one value per centerline point: the turning profile (uneven steps along the vessel)",
      "arc length from the start (mm)", r"$\kappa$ (rad/mm)")
ax.plot(pos, kappa, color=MUTED, lw=1)
ax.plot(pos, kappa, "o", color=INK2, ms=3.5)
for col, i in enumerate((i0, i0 + 1)):
    k = np.flatnonzero(pos == s[i])[0]
    ax.plot(pos[k], kappa[k], "o", color=C[col], ms=8, zorder=3)
ax.plot(s, np.full_like(s, -0.004), "|", color=INK2, ms=8)
ax.text(s[-1], -0.004, "  points", fontsize=7, color=INK2, va="center")
ax.set_xlim(-0.5, s[-1] + 3)
ax.set_ylim(-0.009, kappa.max() * 1.15)

fig.tight_layout()
fig.savefig(Path(__file__).with_suffix(".png"), dpi=170, facecolor=SURF)
