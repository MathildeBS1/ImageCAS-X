"""Figures for sec:tech-mixed-model (content/technical/01_mixed_model.tex). Made-up data only, no cohort data.

    python3 Thesis_coronary/content/technical/figures/mixed_model_figures.py

Drawn from the model math first, before the section text was rewritten (2026-11-17).
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parents[2] / "setup"))
from figure_colours import FILLS, GRID, INK, INK2, MUTED, SERIES as C  # noqa: E402

plt.rcParams.update({"font.size": 8.5, "axes.titlesize": 9, "axes.titlelocation": "left",
                     "mathtext.fontset": "cm", "pdf.fonttype": 42})
rng = np.random.default_rng(7)


def style(ax, title=None, xlabel=None, ylabel=None):
    ax.grid(color=GRID, lw=0.6)
    ax.tick_params(colors=INK2, labelsize=7.5)
    for sp in ax.spines.values():
        sp.set_color(GRID)
    if title:
        ax.set_title(title, color=INK)
    if xlabel:
        ax.set_xlabel(xlabel, color=INK2)
    if ylabel:
        ax.set_ylabel(ylabel, color=INK2)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)


# ------------------------------------------------------------ 1. normal vs Bernoulli outcome
# Horizontal axis: the linear predictor eta, so the picture holds for any number of covariates.
# Every unit has its own distribution of Y, set by its eta; three are drawn, at the same eta in
# both panels. Left: the linear model, Y ~ N(eta, sigma^2), one common sigma. Right: a GLM with a
# Bernoulli outcome, Y in {0, 1} with P(Y = 1) = p = g^{-1}(eta); the sideways bars at y = 1 and
# y = 0 have lengths p and 1 - p. The curve uses the inverse cloglog, the link of the who model;
# the link itself is the subject of a later figure and is not named here.
N = 60
ETAS = (-1.75, -0.5, 0.75)  # where the distribution of Y is drawn, off the grid lines
LO, HI = -3.0, 2.0
eta = rng.uniform(LO, HI, N)
grid = np.linspace(LO, HI, 200)
sigma = 0.45
W = 0.75  # horizontal length of a probability (or peak density) of 1


def p_of(e):
    return 1 - np.exp(-np.exp(e))


y_lin = eta + rng.normal(0, sigma, N)
y_bin = (rng.uniform(size=N) < p_of(eta)).astype(float)
PT = dict(s=4, color=MUTED, alpha=0.6, lw=0, zorder=2)
GUIDE = dict(color=C[1], lw=0.6, ls=(0, (3, 2)), zorder=1)
NOTE = dict(color=INK2, fontsize=7)

fig, ax = plt.subplots(1, 2, figsize=(6.3, 2.7))
ETA = r"linear predictor $\eta$"

style(ax[0], "Linear model", ETA, "outcome $y$")
ax[0].scatter(eta, y_lin, **PT)
ax[0].plot(grid, grid, color=C[2], lw=1.6, zorder=3)
yy = np.linspace(-3.2, 3.2, 200) * sigma
dens = np.exp(-0.5 * (yy / sigma) ** 2)
for ev in ETAS:
    ax[0].plot([ev, ev], [ev + yy[0], ev + yy[-1]], **GUIDE)
    ax[0].fill_betweenx(ev + yy, ev, ev + W * dens, color=FILLS[1], alpha=0.8, lw=0, zorder=1)
    ax[0].plot(ev + W * dens, ev + yy, color=C[1], lw=1.0, zorder=4)
ev = ETAS[-1]
bx = ev - 0.1
ax[0].plot([bx, bx], [ev, ev + sigma], color=INK2, lw=0.8)
for yv in (ev, ev + sigma):
    ax[0].plot([bx - 0.05, bx + 0.05], [yv, yv], color=INK2, lw=0.8)
ax[0].text(bx - 0.08, ev + sigma / 2, r"$\sigma$", ha="right", va="center", **NOTE)
ax[0].text(HI - 0.05, -0.9, r"$\mathrm{E}(Y) = \eta$", color=C[2], fontsize=8, ha="right", va="top")
ax[0].text(0.03, 0.95, r"$Y \sim \mathrm{N}(\eta,\ \sigma^2)$", transform=ax[0].transAxes,
           color=INK, fontsize=8, va="top")
ax[0].set_xlim(LO, HI)
ax[0].set_ylim(-4.2, 3.6)

style(ax[1], "Generalised linear model", ETA, "outcome $y$")
ax[1].scatter(eta, y_bin + rng.uniform(-0.025, 0.025, N), **PT)
ax[1].plot(grid, p_of(grid), color=C[2], lw=1.6, zorder=3)
for ev in ETAS:
    p = p_of(ev)
    ax[1].plot([ev, ev], [-0.08, 1.08], **GUIDE)
    for level, length in ((0.0, 1 - p), (1.0, p)):
        ax[1].barh(level, W * length, height=0.07, left=ev, color=FILLS[1], edgecolor=C[1], lw=0.9, zorder=4)
ev, p = ETAS[-1], p_of(ETAS[-1])
ax[1].text(ev + W * p / 2, 1.06, "$p$", ha="center", va="bottom", **NOTE)
ax[1].text(ev + W * (1 - p) / 2, 0.06, "$1-p$", ha="center", va="bottom", **NOTE)
ax[1].text(-0.65, 0.62, r"$p = g^{-1}(\eta)$", color=C[2], fontsize=8, ha="right")
ax[1].text(LO + 0.05, 0.9, "observed: 0 or 1", va="top", **NOTE)
ax[1].text(0.03, 0.95, r"$Y \sim \mathrm{Bernoulli}(p)$", transform=ax[1].transAxes,
           color=INK, fontsize=8, va="top")
ax[1].set_xlim(LO, HI)
ax[1].set_ylim(-0.2, 1.45)
ax[1].set_yticks([0, 1])

save(fig, "glm_distribution")


# ------------------------------------------------------------ 2. the link function
# The link g ties the mean mu = E(Y) to the linear predictor: g(mu) = eta, mu = g^{-1}(eta).
# Four equally spaced eta values are carried up to the line or curve and across to the mean axis.
# Left: the normal linear model, identity link, mu = eta: equal steps in eta stay equal steps in mu.
# Right: Bernoulli, mu = p = g^{-1}(eta) with the inverse cloglog of block 1 (the link is not named
# here): equal steps in eta give unequal steps in p, which never leaves (0, 1).
STEPS = (-2.0, -1.0, 0.0, 1.0)
ARROW = dict(arrowstyle="-|>", color=C[1], lw=0.7, ls=(0, (3, 2)), shrinkA=0, shrinkB=0, mutation_scale=7)


def carry(ax, e, m, ylo):
    """Dashed path from eta on the horizontal axis up to the curve and across to the mean axis."""
    ax.annotate("", xy=(e, m), xytext=(e, ylo), arrowprops=ARROW, zorder=2)
    ax.annotate("", xy=(LO, m), xytext=(e, m), arrowprops=ARROW, zorder=2)
    ax.scatter([e], [ylo], s=14, color=C[1], zorder=5, clip_on=False)


fig, ax = plt.subplots(1, 2, figsize=(6.3, 2.7))

ylo = -3.3
style(ax[0], "Normal: identity link", ETA, r"mean $\mu$")
ax[0].plot(grid, grid, color=C[2], lw=1.6, zorder=3)
for e in STEPS:
    carry(ax[0], e, e, ylo)
ax[0].text(HI - 0.05, 1.05, r"$\mu = \eta$", color=C[2], fontsize=8, ha="right", va="top")
ax[0].set_xlim(LO, HI)
ax[0].set_ylim(ylo, 2.3)

ylo = -0.35
style(ax[1], "Bernoulli: link $g$", ETA, r"mean $\mu = p$")
for lo_, hi_ in ((ylo, 0.0), (1.0, 1.35)):
    ax[1].axhspan(lo_, hi_, color=GRID, alpha=0.5, lw=0, zorder=0)
ax[1].text(HI - 0.05, 1.3, r"$p > 1$ impossible", ha="right", va="top", **NOTE)
ax[1].text(HI - 0.05, -0.3, r"$p < 0$ impossible", ha="right", va="bottom", **NOTE)
ax[1].plot(grid, p_of(grid), color=C[2], lw=1.6, zorder=3)
for e in STEPS:
    carry(ax[1], e, p_of(e), ylo)
ax[1].text(HI - 0.05, 0.62, r"$\mu = g^{-1}(\eta)$" "\n" r"$\eta = g(\mu)$", color=C[2], fontsize=8,
           ha="right", va="top", linespacing=1.6)
ax[1].set_xlim(LO, HI)
ax[1].set_ylim(ylo, 1.35)
ax[1].set_yticks([0, 0.5, 1])

save(fig, "glm_link")
