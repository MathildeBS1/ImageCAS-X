"""Figure for app:link (content/appendix/link_choice.tex). Made-up numbers only, no cohort data.

    python3 Thesis_coronary/content/appendix/figures/link_ratios.py

Reference group: constant hazard, 40% event risk by the end of a 10-year window. Second group: hazard ratio 1.5
held constant (left, cloglog) or odds ratio 1.5 held constant (right, logit). Adapted from
reports/hr_vs_or/hr_vs_or.py (which used 42%, the cohort figure; changed to a round 40% for the appendix).
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parents[2] / "setup"))
from figure_colours import GRID, INK, INK2, SERIES as C  # noqa: E402

plt.rcParams.update({"font.size": 8.5, "axes.titlesize": 9, "axes.titlelocation": "left",
                     "mathtext.fontset": "cm", "pdf.fonttype": 42})

t = np.linspace(0.01, 10, 400)
lam = -np.log(0.60) / 10
F0 = 1 - np.exp(-lam * t)
odds = lambda F: F / (1 - F)

F1_ph = 1 - (1 - F0) ** 1.5
hr_ph = np.full_like(t, 1.5)
or_ph = odds(F1_ph) / odds(F0)

o1 = 1.5 * odds(F0)
F1_po = o1 / (1 + o1)
hr_po = np.gradient(F1_po, t) / (1 - F1_po) / lam
or_po = np.full_like(t, 1.5)


def style(ax):
    ax.grid(axis="y", color=GRID, lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=INK2)


fig, ax = plt.subplots(2, 2, figsize=(6.3, 4.6), sharex=True)
for col, (F1, hr, orr, title) in enumerate([
        (F1_ph, hr_ph, or_ph, "Hazard ratio held constant (cloglog)"),
        (F1_po, hr_po, or_po, "Odds ratio held constant (logit)")]):
    top, bot = ax[0, col], ax[1, col]
    style(top); style(bot)
    top.plot(t, 100 * F0, color=INK2, lw=1.6)
    top.plot(t, 100 * F1, color=C[2], lw=1.6)
    top.text(10.2, 100 * F0[-1], f"reference\n{100 * F0[-1]:.0f}%", color=INK2, va="center", fontsize=7.5)
    top.text(10.2, 100 * F1[-1], f"covariate\n{100 * F1[-1]:.0f}%", color=INK, va="center", fontsize=7.5)
    top.set_ylim(0, 65)
    top.set_title(title, color=INK)
    bot.plot(t, hr, color=C[0], lw=1.6)
    bot.plot(t, orr, color=C[1], lw=1.6)
    bot.text(10.2, hr[-1], f"hazard ratio\n{hr[-1]:.2f}", color=INK, va="center", fontsize=7.5)
    bot.text(10.2, orr[-1], f"odds ratio\n{orr[-1]:.2f}", color=INK, va="center", fontsize=7.5)
    bot.axhline(1, color=INK2, lw=0.6, ls=":")
    bot.set_ylim(0.9, 2.0)
    bot.set_xlim(0, 10)
    bot.set_xlabel("time since the start of the window (years)", color=INK2)
ax[0, 0].set_ylabel("event probability so far (%)", color=INK2)
ax[1, 0].set_ylabel("ratio, covariate vs reference", color=INK2)
fig.tight_layout(rect=(0, 0, 0.94, 1))
fig.savefig(OUT / "link_ratios.pdf")
print(f"PH: OR at 10 y {or_ph[-1]:.2f}; PO: HR at 10 y {hr_po[-1]:.2f}; risks {F1_ph[-1]:.3f} {F1_po[-1]:.3f}")
