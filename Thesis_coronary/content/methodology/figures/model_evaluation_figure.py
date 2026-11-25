"""Figure for Sections sec:method-test and sec:method-added-value (fig:method-evaluation, 2026-11-23): the test
of the geometric features and the estimate of their added predictive value.

    python Thesis_coronary/content/methodology/figures/model_evaluation_figure.py

Schematic with made-up numbers (no patient data). Panels, left to right (no letters, as the feature figures):
- The base and the extended model (risk factors, plus the geometric features) compared by the likelihood ratio
  test, and a hazard ratio per SD with its 95% interval on a log axis with the line at 1.
- 10-fold cross-validation divided by participant: each participant a column of nine segments, so the segments of
  one participant stay together; one fold held out; repeated 50 times.
- Back-to-back histograms of made-up cross-validated risks of the base and the extended model, and the measures
  that compare them.
Style and colours as angle_steps_figure.py. Writes model_evaluation_figure.{pdf,png} next to this file.
"""
import sys
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "Thesis_coronary" / "setup"))
from figure_colours import INK, INK2, MUTED, PALETTE  # noqa: E402

MAIN, SECOND, THIRD = PALETTE[3], PALETTE[1], PALETTE[2]  # purple, pink, green, as angle_steps_figure.py

mpl.rcParams.update({
    "font.family": "serif", "font.serif": ["cmr10"],
    "mathtext.fontset": "cm", "axes.unicode_minus": False, "axes.formatter.use_mathtext": True,
    "font.size": 10, "text.color": INK, "pdf.fonttype": 42,
})


def tint(hex_, a):
    c = np.array(to_rgb(hex_))
    return tuple(1 - a * (1 - c))


BASE_COL, EXT_COL, GREY = INK2, MAIN, tint(MUTED, 0.45)
AX = dict(arrowstyle="-|>,head_length=0.55,head_width=0.16", lw=0.6, color=INK, shrinkA=0, shrinkB=0)
rng = np.random.default_rng(3)

# ---------------------------------------------------------------- layout
W, H = 6.3, 2.5
fig = plt.figure(figsize=(W, H))
L, R, GAP = 0.015, 0.985, 0.02
widths = (0.32, 0.36, 0.32)
avail = R - L - 2 * GAP
PB, PT = 0.02, 0.98
bg = fig.add_axes([0, 0, 1, 1], zorder=-5)
bg.set_axis_off(); bg.set_xlim(0, 1); bg.set_ylim(0, 1)
x0s = L + np.r_[0, np.cumsum(np.array(widths[:-1]) * avail + GAP)]
for x0, w in zip(x0s, widths):
    bg.add_patch(FancyBboxPatch((x0, PB), w * avail, PT - PB, transform=fig.transFigure,
                 boxstyle="round,pad=0,rounding_size=0.02", fc=tint(MUTED, 0.08),
                 ec=tint(MUTED, 0.30), lw=0.8, mutation_aspect=W / H))


def panel(k, pad=0.02, bottom=0.04, top=0.04):
    ax = fig.add_axes([x0s[k] + pad, PB + bottom, widths[k] * avail - 2 * pad, PT - PB - bottom - top])
    ax.set_axis_off()
    return ax


def box(ax, x, y, w, h, fc, ec, lw=0.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.04", fc=fc, ec=ec, lw=lw))


# left: the likelihood ratio test and the hazard ratio
ax = panel(0)
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
CH = 0.054  # one small square per term: grey the covariates, purple the geometric features


def chips(ax, x, y, n, col):
    for k in range(n):
        ax.add_patch(Rectangle((x + k * 1.3 * CH, y), CH, CH * 1.15, fc=col, ec="none"))


YB, YE, BH = 0.76, 0.50, 0.18  # bottoms of the base and extended boxes, box height
box(ax, 0.04, YB, 0.83, BH, "white", tint(BASE_COL, 0.6))
ax.text(0.08, YB + BH / 2, "base", ha="left", va="center", fontsize=9, color=BASE_COL)
chips(ax, 0.41, YB + BH / 2 - CH * 0.575, 4, GREY)
box(ax, 0.04, YE, 0.83, BH, "white", EXT_COL, lw=1.0)
ax.text(0.08, YE + BH / 2, "extended", ha="left", va="center", fontsize=9, color=EXT_COL)
chips(ax, 0.41, YE + BH / 2 - CH * 0.575, 4, GREY)
chips(ax, 0.41 + 4 * 1.3 * CH, YE + BH / 2 - CH * 0.575, 2, EXT_COL)
# bracket joining the two models, then the test
xb, yt = 0.93, 0.36
ax.plot([0.87, xb, xb, 0.87], [YB + BH / 2, YB + BH / 2, YE + BH / 2, YE + BH / 2], color=INK, lw=0.6)
ax.plot([xb, xb], [YE + BH / 2, yt], color=INK, lw=0.6)
ax.annotate("", xy=(0.66, yt), xytext=(xb, yt), arrowprops=AX)
ax.text(0.63, yt, "LR test", ha="right", va="center", fontsize=9)
# hazard ratio per SD with its interval, log axis, line at 1
hx = lambda hr: 0.10 + 0.55 * (np.log(hr) - np.log(0.6)) / (np.log(2.2) - np.log(0.6))  # noqa: E731
ax.plot([hx(1), hx(1)], [0.07, 0.21], color=INK2, lw=0.6, ls=(0, (2, 2)))
ax.plot([hx(1.12), hx(1.65)], [0.14, 0.14], color=EXT_COL, lw=1.2)
ax.plot(hx(1.36), 0.14, "s", ms=4, color=EXT_COL)
ax.text(hx(1), 0.05, "1", ha="center", va="top", fontsize=7.5, color=INK2)
ax.text(hx(1.65) + 0.04, 0.14, "HR per SD", ha="left", va="center", fontsize=7.5, color=INK2)

# middle: 10-fold cross-validation divided by participant
ax = panel(1)
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
FOLDS, PER, SEG, HELD = 10, 3, 9, 3
cw, gap_p, gap_f = 0.020, 0.008, 0.020
fw = PER * cw + (PER - 1) * gap_p
x_start = (1 - (FOLDS * fw + (FOLDS - 1) * gap_f)) / 2
sh, y0 = 0.042, 0.30
for f in range(FOLDS):
    xf = x_start + f * (fw + gap_f)
    for p in range(PER):
        for j in range(SEG):
            ax.add_patch(Rectangle((xf + p * (cw + gap_p), y0 + j * sh), cw, sh * 0.80,
                                   fc=tint(EXT_COL, 0.75) if f == HELD else GREY, ec="none"))
    if f == HELD:
        ax.add_patch(FancyBboxPatch((xf - 0.010, y0 - 0.022), fw + 0.020, SEG * sh + 0.036,
                     boxstyle="round,pad=0,rounding_size=0.015", fc="none", ec=EXT_COL, lw=0.9))
        ax.text(xf + fw / 2, y0 + SEG * sh + 0.05, "held out", ha="center", va="bottom", fontsize=8, color=EXT_COL)
# one participant: a column of nine segments
xp = x_start + cw / 2
ax.plot([xp, xp], [y0 - 0.02, 0.19], color=INK2, lw=0.5)
ax.text(xp - 0.012, 0.17, "participant", ha="left", va="top", fontsize=7.5, color=INK2)
ax.text(0.97, 0.06, r"10 folds, $\times 50$", ha="right", va="bottom", fontsize=8, color=INK2)

# right: back-to-back histograms of the cross-validated risks
ax = panel(2, bottom=0.10)
risk_b = rng.beta(2.2, 6.5, 400)
risk_e = np.clip(risk_b * np.exp(rng.normal(0, 0.25, 400)), 0.005, 0.95)
bins = np.linspace(0, 0.8, 17)
hb, _ = np.histogram(risk_b, bins)
he, _ = np.histogram(risk_e, bins)
w = np.diff(bins)[0] * 0.9
ax.bar(bins[:-1], hb, width=w, align="edge", color=GREY, edgecolor="none")
ax.bar(bins[:-1], -he, width=w, align="edge", color=tint(EXT_COL, 0.75), edgecolor="none")
ax.axhline(0, color=INK, lw=0.6)
top = max(hb.max(), he.max()) * 1.15
ax.set_ylim(-top, top); ax.set_xlim(-0.02, 0.82)
ax.text(0.80, 0.6 * top, "base", ha="right", va="center", fontsize=8, color=BASE_COL)
ax.text(0.80, -0.6 * top, "extended", ha="right", va="center", fontsize=8, color=EXT_COL)
ax.annotate("", xy=(0.84, 0), xytext=(0.78, 0), arrowprops=AX, annotation_clip=False)
ax.text(0.84, -0.06 * top, "risk", ha="right", va="top", fontsize=8)
ax.text(0.40, -top * 1.12, r"C, calibration, Brier, log loss", ha="center", va="top", fontsize=7.5, color=INK2)

out = Path(__file__).with_suffix("")
fig.savefig(f"{out}.pdf")
fig.savefig(f"{out}.png", dpi=200)
