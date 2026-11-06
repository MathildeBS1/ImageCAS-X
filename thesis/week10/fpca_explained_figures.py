"""Figures for fpca_explained.tex. Made-up data only; the FPCA, scores and K rules are the functions
of CGPS_data/turning_profile_shapes.py and tortuosity/curvature.py.

    python3 thesis/week10/fpca_explained_figures.py
"""
import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "CGPS_data")]
from tortuosity.curvature import _at_chord, chord_resample, profile_thesis, turning_angles  # noqa: E402
import turning_profile_shapes as tps  # noqa: E402

OUT = Path(__file__).resolve().parent / "week_figure" / "fpca"
OUT.mkdir(parents=True, exist_ok=True)
INK, INK2, GRID, SURF, MUTED = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb", "#8a8984"
C = ("#2a78d6", "#eb6834", "#1baf7a")
rng = np.random.default_rng(4)
G = 50
g = (np.arange(G) + 0.5) / G


def style(ax, title=None, xlabel=None, ylabel=None):
    ax.set_facecolor(SURF)
    ax.grid(color=GRID, lw=0.6)
    ax.tick_params(colors=INK2, labelsize=8)
    for sp in ax.spines.values():
        sp.set_color(GRID)
    if title:
        ax.set_title(title, fontsize=9.5, color=INK, loc="left")
    if xlabel:
        ax.set_xlabel(xlabel, color=INK2, fontsize=8.5)
    if ylabel:
        ax.set_ylabel(ylabel, color=INK2, fontsize=8.5)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.png", dpi=170, facecolor=SURF)
    plt.close(fig)


POS = "normalised position u (0 = proximal)"

# ------------------------------------------------------------ 1. turning angle at one point
t = np.linspace(0, 1, 400)
P = np.c_[40 * t, 8 * np.sin(2.2 * np.pi * t) * np.exp(-1.5 * t), 0 * t]
pos1, T1 = profile_thesis(P, 5.0)
i = int(np.argmin(np.abs(np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))] - pos1[np.argmax(T1)])))
B, F = _at_chord(P, i, 5.0, -1), _at_chord(P, i, 5.0, 1)
a, b = P[i] - B, F - P[i]
theta = np.arctan2(np.linalg.norm(np.cross(a, b)), a @ b)
fig, ax = plt.subplots(figsize=(5.2, 3.6), facecolor=SURF)
style(ax, "Turning angle at one centerline point", "x (mm)", "y (mm)")
ax.plot(P[:, 0], P[:, 1], color=MUTED, lw=2, label="centerline")
ax.plot(*zip(B[:2], P[i, :2], F[:2]), color=INK, lw=1.8)
ax.plot(*np.c_[B[:2], P[i, :2], F[:2]], "o", color=INK, ms=4)
ext = P[i] + a / np.linalg.norm(a) * 5
ax.plot([P[i, 0], ext[0]], [P[i, 1], ext[1]], ls=":", color=C[0], lw=1.5, label="direction kept straight")
for pt, lab, off in ((B, "$B_i$", (-2.5, -1.3)), (P[i], "$P_i$", (-1.0, 0.9)), (F, "$F_i$", (0.5, -1.1))):
    ax.annotate(lab, pt[:2], xytext=(pt[0] + off[0], pt[1] + off[1]), fontsize=11, color=INK)
ax.annotate(rf"$\theta_i$ = {np.degrees(theta):.0f}°", P[i, :2], xytext=(P[i, 0] + 5.5, P[i, 1] + 0.6),
            color=C[1], fontsize=11, arrowprops=dict(arrowstyle="-", color=C[1]))
ax.text(0.02, 0.04, "|P_i − B_i| = |F_i − P_i| = l = 5 mm (straight line)", transform=ax.transAxes,
        fontsize=8, color=INK2)
ax.set_aspect("equal")
ax.legend(frameon=False, fontsize=8, loc="upper right")
save(fig, "f1_turning_geometry")


# ------------------------------------------------------------ made-up trunk for the grid figure
def fake_trunk(L=120, step=0.4):
    s = np.linspace(0, L, int(L / step))
    Y = np.c_[s, 9 * np.sin(s / 14) + 4 * np.sin(s / 6.5), 4 * np.cos(s / 21)]
    return Y, np.r_[0, np.cumsum(np.linalg.norm(np.diff(Y, axis=0), axis=1))]


Y, s = fake_trunk()
pos, T = profile_thesis(Y, 5.0, s)
V = chord_resample(Y, 5.0)
vT = turning_angles(V) / 5.0
vpos = s[np.argmin(np.linalg.norm(Y[None] - V[1:-1, None], axis=2), axis=1)]
cuts = (0, 0.3 * s[-1], 0.65 * s[-1], s[-1])

# ------------------------------------------------------------ 3. segment onto the grid
lo, hi = cuts[1], cuts[2]
k = (pos >= lo) & (pos < hi)
p, tt = pos[k], T[k]
u = (p - p[0]) / (p[-1] - p[0])
x = np.interp(g, u, tt)
fig, ax = plt.subplots(2, 1, figsize=(5.2, 4.2), facecolor=SURF)
style(ax[0], "Mid segment in mm: one value per centerline point", "arc length (mm)", "$T_5$")
ax[0].plot(p, tt, ".", color=INK, ms=3)
style(ax[1], f"Same segment on the grid: {G} values at $u_j = (j + 0.5)/{G}$", POS, "$T_5$")
ax[1].plot(u, tt, color=MUTED, lw=1, label="profile, position rescaled to 0-1")
ax[1].plot(g, x, "o", color=C[1], ms=3.2, label="grid values $M_{ij}$ (linear interpolation)")
ax[1].legend(frameon=False, fontsize=7.5)
save(fig, "f3_grid")

# ------------------------------------------------------------ made-up group for the FPCA part
N, SD_TRUE = 300, 0.006
base = np.array([np.ones(G), np.cos(np.pi * g), np.cos(2 * np.pi * g)])
avg_true = 0.03 + 0.025 * np.exp(-g / 0.12) + 0.01 * np.exp(-(1 - g) / 0.15)
z_true = rng.normal(size=(N, 3)) * np.array([1.0, 0.7, 0.45])
noise = np.array([np.convolve(rng.normal(0, 0.0025, G + 6), np.ones(7) / 7, "valid") for _ in range(N)])
M = avg_true + SD_TRUE * z_true @ (base / np.sqrt((base ** 2).mean(1, keepdims=True))) + noise
show = rng.choice(N, 25, replace=False)
mean, ev, Vt = tps.pca(M)
D = M - mean

# ------------------------------------------------------------ 4. profiles and deviations
fig, ax = plt.subplots(2, 1, figsize=(5.2, 4.6), facecolor=SURF, sharex=True)
style(ax[0], f"Matrix M: profiles of 25 of the {N} made-up people, average $m$", None, "$T_5$ (rad/mm)")
for r in show:
    ax[0].plot(g, M[r], color=MUTED, lw=0.8, alpha=0.7)
ax[0].plot(g, mean, color=INK, lw=2.2, label="average $m_j$")
ax[0].legend(frameon=False, fontsize=8)
style(ax[1], "Matrix D = M − m: deviations (only these are used)", POS, "$D_{ij}$ (rad/mm)")
for r in show:
    ax[1].plot(g, D[r], color=MUTED, lw=0.8, alpha=0.7)
ax[1].axhline(0, color=INK, lw=1)
save(fig, "f4_profiles_deviations")

# ------------------------------------------------------------ 5. covariance and its eigenvectors
S = D.T @ D / N
fig, ax = plt.subplots(1, 2, figsize=(5.4, 2.8), facecolor=SURF, gridspec_kw=dict(width_ratios=[1, 1.15]))
im = ax[0].imshow(S, origin="lower", extent=(0, 1, 0, 1), cmap="RdBu_r", vmin=-abs(S).max(), vmax=abs(S).max())
ax[0].set_title("covariance S of the deviations", fontsize=9, color=INK, loc="left")
ax[0].set_xlabel("$u_j$", color=INK2)
ax[0].set_ylabel("$u_{j'}$", color=INK2)
ax[0].tick_params(labelsize=7, colors=INK2)
style(ax[1], r"eigenvectors of S = $\varphi_1, \varphi_2, \varphi_3$", POS)
for kk in range(3):
    ax[1].plot(g, Vt[kk], color=C[kk], lw=1.8, label=rf"$\varphi_{kk + 1}$, $\lambda$ share {100 * ev[kk]:.0f}%")
ax[1].axhline(0, color=INK2, lw=0.8)
ax[1].legend(frameon=False, fontsize=7)
save(fig, "f5_covariance")

# ------------------------------------------------------------ 6. the three steps
R = D.copy()
total = (D ** 2).sum()
fig, ax = plt.subplots(3, 2, figsize=(5.4, 6.6), facecolor=SURF, sharex=True, sharey=True)
for kk in range(3):
    c = R @ Vt[kk]
    sd = c.std()
    a = ax[kk, 0]
    style(a, rf"step {kk + 1}: unexplained, {(R ** 2).sum() / total:.0%}")
    for r in show:
        a.plot(g, R[r], color=MUTED, lw=0.7, alpha=0.7)
    a.plot(g, 2 * sd * Vt[kk], color=C[kk], lw=2.2, label=rf"$\pm 2$SD$\cdot\varphi_{kk + 1}$")
    a.legend(frameon=False, fontsize=7, loc="upper right")
    a.plot(g, -2 * sd * Vt[kk], color=C[kk], lw=2.2, ls="--")
    R = R - np.outer(c, Vt[kk])
    a = ax[kk, 1]
    style(a, rf"minus $c_{{i{kk + 1}}}\varphi_{kk + 1}$: {(R ** 2).sum() / total:.0%} left")
    for r in show:
        a.plot(g, R[r], color=C[kk], lw=0.7, alpha=0.8)
for a in ax[-1]:
    a.set_xlabel(POS, color=INK2, fontsize=8)
save(fig, "f6_steps")

# ------------------------------------------------------------ 7. mean +- 2 SD of each shape
scores = D @ Vt[:3].T
fig, ax = plt.subplots(3, 1, figsize=(5.2, 6.0), facecolor=SURF, sharex=True)
for kk in range(3):
    sd = scores[:, kk].std()
    style(ax[kk], rf"$\varphi_{kk + 1}$: $m \pm 2\,\mathrm{{SD}}_{kk + 1}\,\varphi_{kk + 1}$", None, "$T_5$")
    ax[kk].plot(g, mean, color=INK, lw=1.4, label="average")
    ax[kk].plot(g, mean + 2 * sd * Vt[kk], color=C[kk], lw=2, label="high score")
    ax[kk].plot(g, mean - 2 * sd * Vt[kk], color=C[kk], lw=2, ls="--", label="low score")
    ax[kk].legend(frameon=False, fontsize=7.5, loc="upper center", ncol=3)
ax[-1].set_xlabel(POS, color=INK2)
save(fig, "f7_mean_pm")

# ------------------------------------------------------------ score of one person: multiply and add
r = int(np.argmax(np.min(np.abs(scores) / scores.std(0), axis=1)))
fig, ax = plt.subplot_mosaic([["d", "d"], ["p0", "p1"], ["x0", "x1"]], figsize=(5.4, 5.6), facecolor=SURF)
style(ax["d"], "deviation of one person from the average", None, "$D_{ij}$ (rad/mm)")
ax["d"].plot(g, D[r], color=INK, lw=1.4)
ax["d"].axhline(0, color=INK2, lw=0.8)
for kk in range(2):
    prod = D[r] * Vt[kk]
    z = scores[r, kk] / scores[:, kk].std()
    a = ax[f"p{kk}"]
    style(a, rf"pattern $\varphi_{kk + 1}$", None, "weight" if kk == 0 else None)
    a.plot(g, Vt[kk], color=C[kk], lw=1.8)
    a.axhline(0, color=INK2, lw=0.8)
    a = ax[f"x{kk}"]
    style(a, rf"deviation × $\varphi_{kk + 1}$: sum {z:+.1f} SD", POS, "product" if kk == 0 else None)
    a.fill_between(g, prod, where=prod > 0, color=C[kk], alpha=0.7, lw=0, label="raises the score")
    a.fill_between(g, prod, where=prod < 0, color=MUTED, alpha=0.6, lw=0, label="lowers it")
    a.axhline(0, color=INK2, lw=0.8)
    a.legend(frameon=False, fontsize=6.5, loc="lower right")
save(fig, "f6b_score")

# ------------------------------------------------------------ spread of the scores along each pattern
fig, ax = plt.subplots(figsize=(5.2, 2.8), facecolor=SURF)
style(ax, f"scores of all {N} people along each pattern", "score $c_{ik}$ (rad/mm)", "people")
bins = np.linspace(scores.min(), scores.max(), 40)
for kk in range(3):
    ax.hist(scores[:, kk], bins=bins, histtype="step", lw=1.8, color=C[kk],
            label=rf"$\varphi_{kk + 1}$: SD {scores[:, kk].std():.3f}, share {100 * ev[kk]:.0f}%")
ax.legend(frameon=False, fontsize=7.5)
save(fig, "f6c_spread")

# ------------------------------------------------------------ 8. one person rebuilt pattern by pattern
fig, ax = plt.subplots(2, 2, figsize=(5.4, 4.6), facecolor=SURF, sharex=True, sharey=True)
fit = mean.copy()
tot = (D[r] ** 2).sum()
for kk, a in enumerate(ax.flat):
    if kk:
        fit = fit + scores[r, kk - 1] * Vt[kk - 1]
    gap = ((M[r] - fit) ** 2).sum() / tot
    lab = "average" if kk == 0 else "average + " + " + ".join(rf"$c_{q + 1}\varphi_{q + 1}$" for q in range(kk))
    style(a, f"{kk} pattern{'s' if kk != 1 else ''}: {gap:.0%} left")
    a.plot(g, M[r], color=INK, lw=1.4, label="the person")
    a.plot(g, fit, color=C[kk - 1] if kk else MUTED, lw=2, label=lab)
    a.fill_between(g, M[r], fit, color=MUTED, alpha=0.25, lw=0)
    a.legend(frameon=False, fontsize=6.5, loc="upper right")
for a in ax[-1]:
    a.set_xlabel(POS, color=INK2, fontsize=8)
for a in ax[:, 0]:
    a.set_ylabel("$T_5$ (rad/mm)", color=INK2, fontsize=8)
save(fig, "f8a_rebuild")

# ------------------------------------------------------------ 9-10. choosing K
args = argparse.Namespace(perm=200, boot=200)
res = tps.shape_count(M, np.random.default_rng(0), args)
kx = np.arange(1, res["kmax"] + 1)
fig, ax = plt.subplots(figsize=(5.2, 3.2), facecolor=SURF)
style(ax, f"Share of differences per pattern; Horn: K = {res['K']['horn']}",
      "component k", "share of variance")
ax.semilogy(kx, res["ev"][: res["kmax"]], "o-", color=INK, ms=3.5, label="data")
ax.semilogy(kx, res["horn"][: res["kmax"]], "--", color=C[1], label="by chance (Horn, 95th pct)")
ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
ax.legend(frameon=False, fontsize=8)
save(fig, "f9_scree")

fig, ax = plt.subplots(1, 2, figsize=(5.4, 2.8), facecolor=SURF)
style(ax[0], f"bootstrap: K = {res['K']['boot']}", "component k", "median |cosine|")
ax[0].bar(np.arange(1, len(res["stab"]) + 1), res["stab"], color=MUTED)
ax[0].axhline(tps.STABLE, color=C[1], ls="--", lw=1.2)
ax[0].xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
style(ax[1], f"block CV: K = {res['K']['cv']}", "K", "prediction error / error at K=0")
ax[1].plot(np.arange(len(res["cv"])), res["cv"], "o-", color=INK, ms=3)
ax[1].axvline(res["K"]["cv"], color=C[1], ls="--", lw=1.2)
save(fig, "f10_boot_cv")

# ------------------------------------------------------------ 11. model: cloglog and the weight function
eta = np.linspace(-4, 2, 200)
b = np.array([0.15, -0.10, 0.0])
sds = scores.std(0)
beta = (b / sds) @ Vt[:3]
fig, ax = plt.subplots(2, 1, figsize=(5.2, 4.6), facecolor=SURF)
style(ax[0], r"cloglog link: $p = 1 - \exp(-e^{\eta})$", r"linear predictor $\eta$", "risk p")
ax[0].plot(eta, 1 - np.exp(-np.exp(eta)), color=INK, lw=2)
style(ax[1], r"weight function $\beta_j = \sum_k (b_k/\mathrm{SD}_k)\,\varphi_{kj}$, b = (0.15, -0.10, 0)",
      POS, r"$\beta_j$ (per rad/mm)")
ax[1].plot(g, beta, color=C[1], lw=2)
ax[1].axhline(0, color=INK2, lw=0.8)
save(fig, "f11_model")

# ------------------------------------------------------------ 12. budget (real aggregates, saved.md)
segs = ["pLAD", "mLAD", "dLAD", "pLCx", "mLCx", "dLCx", "pRCA", "mRCA", "dRCA"]
k65 = [5, 4, 1, 1, 0, 0, 1, 2, 0]
k70 = [10, 8, 3, 4, 1, 0, 3, 5, 1]
ev_seg = [275, 201, 90, 99, 40, 12, 88, 123, 42]
fig, ax = plt.subplots(figsize=(5.2, 3.0), facecolor=SURF)
style(ax, "$K_{max}$ per segment model (CGPS aggregates, saved.md)", None, "$K_{max}$")
xx = np.arange(len(segs))
ax.bar(xx - 0.2, k65, 0.4, color=MUTED, label="C = 0.65")
ax.bar(xx + 0.2, k70, 0.4, color=C[0], label="C = 0.70")
ax.set_xticks(xx, [f"{sg}\n{e} ev." for sg, e in zip(segs, ev_seg)], fontsize=7)
ax.legend(frameon=False, fontsize=8)
save(fig, "f12_budget")
print("wrote", sorted(p.name for p in OUT.glob("*.png")))
