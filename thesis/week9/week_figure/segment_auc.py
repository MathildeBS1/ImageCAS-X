"""AUC per trunk segment, base vs base + geometry (progression in the Medis trees).

    python thesis/week9/week_figure/segment_auc.py

Numbers are the aggregates from progression_segment_models.md (dtu-gpu-7, 2026-10-29): nested
cross-validation split by person, AUC on the test folds. Writes segment_auc.pdf next to this file.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent
# segment, progressed, segments, LM angle in the model, AUC base, AUC + geometry, ΔAUC, CI low, CI high
ROWS = [
    ("pLAD", 217, 478, True, 0.684, 0.685, +0.000, -0.012, +0.012),
    ("mLAD", 250, 518, False, 0.648, 0.641, -0.006, -0.017, +0.003),
    ("dLAD", 143, 444, False, 0.569, 0.568, -0.001, -0.020, +0.016),
    ("pCX", 209, 523, True, 0.603, 0.581, -0.022, -0.044, +0.001),
    ("mCX", 75, 356, False, 0.547, 0.554, +0.007, -0.038, +0.045),
    ("dCX", 38, 327, False, 0.573, 0.617, +0.044, -0.013, +0.100),
    ("pRCA", 185, 541, False, 0.698, 0.698, -0.000, -0.007, +0.006),
    ("mRCA", 187, 400, False, 0.644, 0.627, -0.016, -0.033, -0.002),
    ("dRCA", 145, 413, False, 0.623, 0.630, +0.006, -0.021, +0.034),
]
VESSELS = [("LAD", 0), ("LCx", 3), ("RCA", 6)]
BASE, GEOM = "#8a8984", "#2a78d6"  # grey reference, blue for the added geometry
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "mathtext.fontset": "dejavuserif",
    "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False, "legend.frameon": False,
    "pdf.fonttype": 42})

# rows top to bottom, with a gap between vessels
y, pos = [], 0.0
for i in range(len(ROWS)):
    if i and i in dict((s, v) for v, s in VESSELS):
        pos += 0.7
    y.append(-pos)
    pos += 1
y = np.array(y)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.9), sharey=True, gridspec_kw={"width_ratios": [1.25, 1], "wspace": 0.12})
for ax in (a1, a2):
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)

for yi, (seg, k, n, ang, b, g, d, lo, hi) in zip(y, ROWS):
    a1.plot([b, g], [yi, yi], color=GRID, lw=2.2, solid_capstyle="round", zorder=1)
    a1.plot(b, yi, "o", ms=6.5, mfc="white", mec=BASE, mew=1.6, zorder=3)
    a1.plot(g, yi, "o", ms=5.5, color=GEOM, mec="white", mew=0.8, zorder=4)
    excl = hi < 0 or lo > 0
    a2.plot([lo, hi], [yi, yi], color=GEOM, lw=1.6, solid_capstyle="round")
    a2.plot(d, yi, "D", ms=5, color=GEOM if excl else "white", mec=GEOM, mew=1.3, zorder=3)

a1.set_yticks(y, [f"{s}{'$^{*}$' if ang else ''}  ({k}/{n})" for s, k, n, ang, *_ in ROWS])
for v, start in VESSELS:  # vessel name above its group
    a1.text(0.462, y[start] + 0.62, v, fontsize=9, fontweight="bold", color=INK, ha="left", va="bottom")
a1.set_xlim(0.46, 0.75)
a1.set_xticks([0.5, 0.55, 0.6, 0.65, 0.7])
a1.axvline(0.5, color=INK2, lw=0.8, ls=":")
a1.set_xlabel("AUC on the test folds")
a1.set_title("(a) Discrimination per segment", fontsize=9.5, loc="left", color=INK)
a1.plot([], [], "o", ms=6.5, mfc="white", mec=BASE, mew=1.6, label="Base")
a1.plot([], [], "o", ms=5.5, color=GEOM, label="Base + geometry")
a1.legend(loc="upper left", bbox_to_anchor=(0.13, 1.0), fontsize=8, handletextpad=0.3)

a2.axvline(0, color=INK2, lw=0.8)
a2.set_xlim(-0.06, 0.11)
a2.set_xticks([-0.05, 0, 0.05, 0.1], ["$-0.05$", "0", "$+0.05$", "$+0.10$"])
a2.set_xlabel(r"$\Delta$AUC (base + geometry $-$ base), 95% CI")
a2.set_title("(b) Gain from geometry", fontsize=9.5, loc="left", color=INK)
a2.set_ylim(y.min() - 0.7, y.max() + 1.2)

fig.savefig(HERE / "segment_auc.pdf", bbox_inches="tight")
fig.savefig(HERE / "segment_auc.png", dpi=200, bbox_inches="tight")
