"""Figures for sec:tech-fpca (content/technical/02_fpca.tex). Made-up curves only, no cohort data.

    python3 Thesis_coronary/content/technical/figures/fpca_figures.py

Adapted from outdated/thesis_retired/week10/fpca_explained_figures.py. The FPCA is the grid version of
sec:tech-fpca-grid: G = 50 midpoint positions t_g = (g - 0.5)/G, spacing w = 1/G, eigenvectors of the
sample covariance, then lambda = w * eigenvalue, phi = w^(-1/2) * v, xi = w^(1/2) * v'd.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
INK, INK2, GRID, MUTED = "#0b0b0b", "#52514e", "#e4e3df", "#a3a29d"
C = ("#2a78d6", "#eb6834", "#1baf7a")
plt.rcParams.update({"font.size": 8.5, "axes.titlesize": 9, "axes.titlelocation": "left",
                     "mathtext.fontset": "cm", "pdf.fonttype": 42})
rng = np.random.default_rng(7)
G = 50
t = (np.arange(G) + 0.5) / G
w = 1 / G
POS = "position $t$"


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


def bump(c, h=1.0, s=0.09):
    return h * np.exp(-0.5 * ((t - c) / s) ** 2)


# ------------------------------------------------------------ made-up sample
# Mean: one bump. Variation: the bump's height, a gradual tilt along the domain, and a small
# shift of the bump, plus smooth noise.
N = 200
mu_true = 0.4 + bump(0.5)
f = np.array([bump(0.5), t - 0.5, np.gradient(bump(0.5), t) * 0.04])
z = rng.normal(size=(N, 3)) * np.array([0.4, 0.35, 0.6])
noise = np.array([np.convolve(rng.normal(0, 0.06, G + 8), np.ones(9) / 9, "valid") for _ in range(N)])
X = mu_true + z @ f + noise

mu = X.mean(0)
D = X - mu
ev, V = np.linalg.eigh(D.T @ D / N)
ev, V = ev[::-1], V[:, ::-1]
V *= np.sign(V.sum(0))  # sign convention: each eigenfunction has a positive integral
lam = w * ev
phi = V / np.sqrt(w)
xi = np.sqrt(w) * D @ V
fve = np.cumsum(lam) / lam.sum()
show = rng.choice(N, 15, replace=False)

# ------------------------------------------------------------ 1. curves, mean and deviations
fig, ax = plt.subplots(1, 2, figsize=(6.3, 2.5), sharex=True)
style(ax[0], "Curves and their mean", POS, "$x_i(t)$")
for r in show:
    ax[0].plot(t, X[r], color=MUTED, lw=0.8)
ax[0].plot(t, mu, color=INK, lw=2.2, label=r"mean $\hat\mu(t)$")
ax[0].legend(frameon=False, fontsize=7.5)
style(ax[1], "Deviations from the mean", POS, r"$x_i(t) - \hat\mu(t)$")
for r in show:
    ax[1].plot(t, D[r], color=MUTED, lw=0.8)
ax[1].axhline(0, color=INK, lw=1.2)
save(fig, "fpca_curves")

# ------------------------------------------------------------ 2. covariance function
S = D.T @ D / N
fig, ax = plt.subplots(figsize=(3.4, 2.9))
m = abs(S).max()
im = ax.imshow(S, origin="lower", extent=(0, 1, 0, 1), cmap="RdBu_r", vmin=-m, vmax=m)
ax.plot([0, 1], [0, 1], color=INK, lw=0.6, ls=":")
ax.set_title(r"Covariance $\hat\Gamma(t, u)$", color=INK)
ax.set_xlabel("position $t$", color=INK2)
ax.set_ylabel("position $u$", color=INK2)
ax.tick_params(colors=INK2, labelsize=7.5)
cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cb.ax.tick_params(labelsize=7, colors=INK2)
cb.outline.set_edgecolor(GRID)
save(fig, "fpca_covariance")

# ------------------------------------------------------------ 3. one curve rebuilt from the mean and shapes
sd = xi.std(0)
i = int(np.argmax(np.minimum(np.abs(xi[:, 0]) / sd[0], np.abs(xi[:, 1]) / sd[1])))
fig = plt.figure(figsize=(6.3, 4.2))
gs = fig.add_gridspec(2, 4, height_ratios=[1, 1.35])
top = [fig.add_subplot(gs[0, k]) for k in range(4)]
style(top[0], r"mean $\hat\mu(t)$", POS)
top[0].plot(t, mu, color=INK, lw=1.8)
for k in range(3):
    style(top[k + 1], rf"$\hat\phi_{k + 1}(t)$", POS)
    top[k + 1].text(0.03, 0.95, rf"score $\hat\xi_{{i{k + 1}}}$ = {xi[i, k]:+.2f}", transform=top[k + 1].transAxes,
                    fontsize=7.5, color=C[k], va="top")
    top[k + 1].plot(t, phi[:, k], color=C[k], lw=1.8)
    top[k + 1].axhline(0, color=MUTED, lw=0.8)
lims = (min(a.get_ylim()[0] for a in top[1:]), max(a.get_ylim()[1] for a in top[1:]))
for a in top[1:]:
    a.set_ylim(lims)
bot = fig.add_subplot(gs[1, :])
style(bot, "The curve rebuilt from the mean and $K$ shapes, each weighted by its score", POS, "$x_i(t)$")
bot.plot(t, X[i], "o", color=INK, ms=3, label="observed curve")
bot.plot(t, mu, color=MUTED, lw=1.2, ls="--", label="mean ($K = 0$)")
for K in range(1, 4):
    rebuilt = mu + phi[:, :K] @ xi[i, :K]
    bot.plot(t, rebuilt, color=C[K - 1], lw=1.6, label=f"$K = {K}$")
bot.legend(frameon=False, fontsize=7.5, ncol=1, loc="upper right")
save(fig, "fpca_reconstruction")

# ------------------------------------------------------------ 4. modes of variation and FVE
fig, ax = plt.subplots(1, 3, figsize=(6.3, 2.4), gridspec_kw=dict(width_ratios=[1, 1, 0.9]))
for k in range(2):
    style(ax[k], f"Component {k + 1}", POS, "$x(t)$" if k == 0 else None)
    d = 2 * np.sqrt(lam[k]) * phi[:, k]
    ax[k].plot(t, mu, color=INK, lw=1.8, label="mean")
    ax[k].plot(t, mu + d, color=C[0], lw=1.5, label=r"$+2\sqrt{\lambda_k}\,\phi_k$")
    ax[k].plot(t, mu - d, color=C[1], lw=1.5, ls="--", label=r"$-2\sqrt{\lambda_k}\,\phi_k$")
ax[0].legend(frameon=False, fontsize=7)
style(ax[2], "Variance explained", "component $k$", "share of variance")
ks = np.arange(1, 7)
ax[2].bar(ks, lam[:6] / lam.sum(), color=C[0], width=0.6)
ax[2].plot(ks, fve[:6], "o-", color=INK, ms=3, lw=1.2, label="cumulative FVE")
ax[2].set_ylim(0, 1.05)
ax[2].set_xticks(ks)
ax[2].legend(frameon=False, fontsize=7, loc="center right")
save(fig, "fpca_modes")

# ------------------------------------------------------------ 5. phase: the same bump at different positions
centres = np.linspace(0.3, 0.7, 7)
P = np.array([0.2 + bump(c, 1.0, 0.06) for c in centres])
A = np.array([0.2 + bump(0.5, h, 0.06) for h in np.linspace(0.75, 1.25, 7)])
fig, ax = plt.subplots(1, 2, figsize=(6.3, 2.4), sharey=True)
for a, Y, title in ((ax[0], P, "Same height, different positions (phase)"),
                    (ax[1], A, "Same position, different heights (amplitude)")):
    style(a, title, POS)
    for y in Y:
        a.plot(t, y, color=MUTED, lw=0.9)
    a.plot(t, Y.mean(0), color=INK, lw=2.2, label="mean taken position by position")
ax[0].set_ylabel("$x_i(t)$", color=INK2)
ax[0].legend(frameon=False, fontsize=7.5, loc="upper left")
save(fig, "fpca_phase")

print("FVE:", np.round(fve[:4], 3), "curve", i, "scores", np.round(xi[i, :3], 2))
