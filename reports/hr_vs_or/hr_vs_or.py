"""Constant hazard ratio vs constant odds ratio over a 10-year window (made-up numbers).

Reference group: constant hazard, 42% risk by year 10. Feature group: HR 1.5 (left) or OR 1.5 (right).
"""
import numpy as np
import matplotlib.pyplot as plt

BLUE, ORANGE, VIOLET = "#2a78d6", "#eb6834", "#6250d6"
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"

t = np.linspace(0.01, 10, 400)
lam = -np.log(0.58) / 10
F0 = 1 - np.exp(-lam * t)
odds = lambda F: F / (1 - F)

# Left: constant hazard ratio (cloglog)
F1_ph = 1 - (1 - F0) ** 1.5
hr_ph = np.full_like(t, 1.5)
or_ph = odds(F1_ph) / odds(F0)

# Right: constant odds ratio (logit)
o1 = 1.5 * odds(F0)
F1_po = o1 / (1 + o1)
S1 = 1 - F1_po
h1 = np.gradient(F1_po, t) / S1
hr_po = h1 / lam
or_po = np.full_like(t, 1.5)

plt.rcParams.update({"font.family": "sans-serif", "font.size": 10, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
fig, ax = plt.subplots(2, 2, figsize=(10, 7), sharex=True, facecolor=SURFACE)

def style(a):
    a.set_facecolor(SURFACE)
    a.grid(axis="y", color=GRID, lw=0.8)
    for s in ("top", "right"):
        a.spines[s].set_visible(False)

for col, (F1, hr, orr, title) in enumerate([
        (F1_ph, hr_ph, or_ph, "Constant hazard ratio (cloglog)"),
        (F1_po, hr_po, or_po, "Constant odds ratio (logit)")]):
    top, bot = ax[0, col], ax[1, col]
    style(top); style(bot)
    top.plot(t, 100 * F0, color=INK2, lw=2)
    top.plot(t, 100 * F1, color=VIOLET, lw=2)
    top.text(10.15, 100 * F0[-1], f"Without feature\n{100*F0[-1]:.0f}%", color=INK2, va="center", fontsize=9)
    top.text(10.15, 100 * F1[-1], f"With feature\n{100*F1[-1]:.0f}%", color=INK, va="center", fontsize=9)
    top.set_ylim(0, 70); top.set_ylabel("Risk developed so far (%)")
    top.set_title(title, color=INK, fontsize=12, loc="left", pad=10)

    bot.plot(t, hr, color=BLUE, lw=2)
    bot.plot(t, orr, color=ORANGE, lw=2)
    bot.text(10.15, hr[-1], f"Hazard ratio\n{hr[-1]:.2f}", color=INK, va="center", fontsize=9)
    bot.text(10.15, orr[-1], f"Odds ratio\n{orr[-1]:.2f}", color=INK, va="center", fontsize=9)
    bot.axhline(1, color=INK2, lw=0.8, ls=":")
    bot.set_ylim(0.9, 2.0); bot.set_ylabel("Ratio, with vs without feature")
    bot.set_xlabel("Years since baseline scan")
    bot.set_xlim(0, 10)

ax[1, 0].annotate("assumed flat", (2, 1.5), (2, 1.25), color=INK2, fontsize=9,
                  arrowprops=dict(arrowstyle="->", color=INK2))
ax[1, 0].annotate("drifts up as\nrisk builds", (7, or_ph[np.searchsorted(t, 7)]), (4.5, 1.85), color=INK2,
                  fontsize=9, arrowprops=dict(arrowstyle="->", color=INK2))
ax[1, 1].annotate("assumed flat", (2, 1.5), (2, 1.75), color=INK2, fontsize=9,
                  arrowprops=dict(arrowstyle="->", color=INK2))
ax[1, 1].annotate("fades toward 1", (7, hr_po[np.searchsorted(t, 7)]), (4.5, 1.05), color=INK2,
                  fontsize=9, arrowprops=dict(arrowstyle="->", color=INK2))

fig.text(0.01, 0.005, "Made-up example: without the feature, risk builds at a constant rate to 42% by year 10; "
         "the feature has ratio 1.5 under each assumption.", color=INK2, fontsize=8.5)
fig.tight_layout(rect=(0, 0.02, 0.93, 1))
for ext in ("pdf", "png"):
    fig.savefig(f"hr_vs_or.{ext}", dpi=200, facecolor=SURFACE)
print(f"PH: OR at 10y {or_ph[-1]:.2f}; PO: HR at 10y {hr_po[-1]:.2f}; risks {F1_ph[-1]:.3f} {F1_po[-1]:.3f}")
