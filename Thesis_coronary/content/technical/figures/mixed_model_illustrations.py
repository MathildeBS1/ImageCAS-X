"""Vector redraws of the four mixed-model illustrations in research_notes/Mixed model illustrations/
(01_distribution_residual.png ... 04_hazard_area.png), in the thesis colours. Made-up data only, no cohort data.

    python3 Thesis_coronary/content/technical/figures/mixed_model_illustrations.py

The layout follows the PNGs as closely as possible; only the colours change (setup/figure_colours.py).
Blue in the PNGs is the main series colour C[2], red is C[1] (darkened for thin lines), green is PALETTE[2].
Not in the thesis text yet; the glm_*.pdf figures of mixed_model_figures.py are separate.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parents[2] / "setup"))
from figure_colours import INK, INK2, MUTED, PALETTE, SERIES as C  # noqa: E402

plt.rcParams.update({"font.size": 8.5, "font.family": "serif", "font.serif": ["cmr10"],
                     "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "pdf.fonttype": 42})
rng = np.random.default_rng(7)
BOLD = dict(family="cmb10")


def tint(c, a):
    """a of colour c on white."""
    return tuple(a * np.array(to_rgb(c)) + (1 - a))


def shade(c, a):
    """Colour c darkened towards INK by a."""
    return tuple((1 - a) * np.array(to_rgb(c)) + a * np.array(to_rgb(INK)))


BLUE, RED, GREEN = C[2], shade(C[1], 0.3), PALETTE[2]
AX = dict(arrowstyle="-|>", color=INK, lw=1.0, mutation_scale=8, shrinkA=0, shrinkB=0)
GUIDE = dict(color=INK2, lw=0.6, ls=(0, (4, 3)))


def arrow(ax, x0, y0, x1, y1, **kw):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops={**AX, **kw}, annotation_clip=False)


def axes_arrows(ax, x0, y0, x1, y1):
    """Horizontal and vertical axis with arrow heads, crossing at (x0, y0)."""
    arrow(ax, x0, y0, x1, y0)
    arrow(ax, x0, y0, x0, y1)


def canvas(fig):
    ax = fig.add_axes([0, 0, 1, 1], zorder=-1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return ax


def box(bg, x, y, w, h, fc, ec=None):
    W, H = bg.figure.get_size_inches()
    bg.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.012", mutation_aspect=W / H,
                                fc=fc, ec=ec or fc, lw=0.8, zorder=0))


def bare(fig, rect, xlim, ylim):
    ax = fig.add_axes(rect)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return ax


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)


# ------------------------------------------------------------ 1. normal outcome vs binary outcome
# Left: points scattered around a straight line (light band), with the normal distribution of y drawn sideways at
# three positions, joined to the line by dashed guides. Right: the same line for 0/1 outcomes (two rows of points);
# at each position the two lollipops have lengths p (at y = 1, top) and 1 - p (at y = 0, bottom).
fig, axs = plt.subplots(1, 2, figsize=(6.3, 4.2))
fig.subplots_adjust(left=0.02, right=0.98, bottom=0.03, top=0.97, wspace=0.08)
for ax in axs:
    ax.set_xlim(-0.1, 9.6)
    ax.set_ylim(-0.1, 10.6)
    ax.axis("off")
    axes_arrows(ax, 0, 0, 9.5, 10.5)
xl = np.array([0.1, 6.8])
BAR = 7.3

ax = axs[0]
line = lambda x: 2.0 + 1.0 * x  # noqa: E731
ax.fill_between(xl, line(xl) - 0.45, line(xl) + 0.45, color=tint(BLUE, 0.15), lw=0, zorder=1)
ax.plot(xl, line(xl), color=BLUE, lw=1.4, zorder=3)
xs = rng.uniform(0.2, 6.6, 110)
ax.scatter(xs, line(xs) + rng.normal(0, 0.8, xs.size), s=9, color=BLUE, alpha=rng.uniform(0.45, 0.95, xs.size),
           lw=0, zorder=2)
sig = 0.33
yy = np.linspace(-2.5, 2.5, 200) * sig
for x0 in (1.2, 3.6, 5.8):
    m = line(x0)
    ax.plot([x0, x0], [0, m], **GUIDE, zorder=1)
    ax.plot([x0, BAR + 1.5], [m, m], **GUIDE, zorder=1)
    ax.fill_betweenx(m + yy, BAR, BAR + 1.6 * np.exp(-0.5 * (yy / sig) ** 2), color=tint(BLUE, 0.3), lw=0, zorder=4)
    ax.plot(BAR + 1.6 * np.exp(-0.5 * (yy / sig) ** 2), m + yy, color=BLUE, lw=1.0, zorder=5)
    ax.plot([BAR, BAR], [m + yy[0], m + yy[-1]], color=INK, lw=1.0, zorder=5)

ax = axs[1]
ROW0, ROW1 = 1.0, 8.4
line = lambda x: 1.6 + 1.1 * x  # noqa: E731
ax.fill_between(xl, line(xl) - 0.45, line(xl) + 0.45, color=tint(BLUE, 0.15), lw=0, zorder=1)
ax.plot(xl, line(xl), color=BLUE, lw=1.4, zorder=3)
xs = np.sort(rng.uniform(0.2, 6.6, 34))
p_x = np.clip((line(xs) - ROW0) / (ROW1 - ROW0), 0, 1)
ys = np.where(rng.uniform(size=xs.size) < p_x, ROW1, ROW0)
ax.scatter(xs, ys, s=12, color=RED, alpha=rng.uniform(0.6, 1.0, xs.size), lw=0, zorder=4)
for x0 in (0.8, 3.4, 6.0):
    m = line(x0)
    p = np.clip((m - ROW0) / (ROW1 - ROW0), 0, 1)
    ax.plot([x0, x0], [0, ROW1], **GUIDE, zorder=1)
    ax.plot([x0, BAR], [m, m], **GUIDE, zorder=1)
    ax.plot([BAR, BAR], [m - 1.25, m + 1.25], color=INK, lw=1.0, zorder=5)
    for dy, length in ((0.85, p), (-0.85, 1 - p)):
        ax.plot([BAR, BAR + 1.6 * length], [m + dy, m + dy], color=RED, lw=0.9, zorder=5)
        ax.scatter([BAR + 1.6 * length], [m + dy], s=12 + 70 * length, color=RED, lw=0, zorder=6)
save(fig, "illus_distribution_residual")


# ------------------------------------------------------------ 2. the link function
# Left box: the linear predictor eta, a straight line on (-inf, inf). Right box: the mean mu = g^{-1}(eta), the
# inverse cloglog, which stays between 0 and 1.
fig = plt.figure(figsize=(6.3, 3.2))
bg = canvas(fig)
ax = bare(fig, [0, 0, 1, 1], (0, 16), (1.5, 9.5))
box(bg, 0.1 / 16, (2.3 - 1.5) / 8, 6.5 / 16, 6.3 / 8, tint(BLUE, 0.12))
box(bg, 9.4 / 16, (2.3 - 1.5) / 8, 6.5 / 16, 6.3 / 8, tint(C[1], 0.15))
ax.text(3.45, 7.6, r"$\eta$", fontsize=24, ha="center", va="center", color=INK)
arrow(ax, 3.45, 3.3, 0.6, 3.3)
arrow(ax, 3.45, 3.3, 6.3, 3.3)
arrow(ax, 3.45, 3.05, 3.45, 6.1)
ax.plot([0.9, 5.9], [3.4, 5.4], color=BLUE, lw=1.6)
ax.text(0.9, 2.8, r"$-\infty$", fontsize=11, ha="center", va="center", color=INK)
ax.text(6.0, 2.8, r"$\infty$", fontsize=11, ha="center", va="center", color=INK)

arrow(ax, 6.95, 4.9, 9.1, 4.9, lw=1.6, mutation_scale=11, color=INK2)
ax.text(8.0, 5.6, r"$g^{-1}(\eta)$", fontsize=14, ha="center", va="center", color=INK)

ax.text(12.55, 7.6, r"$\mu$", fontsize=24, ha="center", va="center", color=INK)
axes_arrows(ax, 10.1, 3.3, 15.6, 6.4)
for yv, lab in ((3.6, "0"), (6.0, "1")):
    ax.plot([10.1, 15.4], [yv, yv], color=MUTED, lw=0.8, ls=(0, (4, 3)))
    ax.text(9.85, yv, lab, fontsize=11, ha="right", va="center", color=INK)
xc = np.linspace(10.1, 15.45, 300)
ec = -3.6 + (xc - 10.1) / (15.45 - 10.1) * 5.0
ax.plot(xc, 3.6 + 2.4 * (1 - np.exp(-np.exp(ec))), color=RED, lw=1.6)
ax.text(10.1, 2.8, r"$-\infty$", fontsize=11, ha="center", va="center", color=INK)
ax.text(12.55, 2.6, r"$\eta$", fontsize=12, ha="center", va="center", color=INK)
ax.text(15.4, 2.8, r"$\infty$", fontsize=11, ha="center", va="center", color=INK)
save(fig, "illus_link_function")


# ------------------------------------------------------------ 3. proportional hazards in three possible worlds
# Three baseline hazards h_0 (increasing, decreasing, non-monotonic); units A and B have h_0(t) exp(x beta) with
# fixed x, so h_A / h_B is the same constant line in every world.
R = 1.8  # h_B / h_0 and h_A / h_B
t = np.linspace(0, 1, 300)
WORLDS = (("Possible world 1", "(increasing hazard)", BLUE, 0.05 + 0.2 * t ** 2.2),
          ("Possible world 2", "(decreasing hazard)", GREEN, 0.07 + 0.18 * np.exp(-4 * t)),
          ("Possible world 3", "(non-monotonic hazard)", C[1],
           0.06 + 0.18 * np.exp(-((t - 0.3) / 0.13) ** 2) + 0.07 * np.exp(-((t - 0.8) / 0.13) ** 2)))
fig = plt.figure(figsize=(6.3, 4.3))
bg = canvas(fig)
X0, CW, GAP = 0.005, 0.326, 0.006
for k, (head, sub, col, h0) in enumerate(WORLDS):
    x = X0 + k * (CW + GAP)
    box(bg, x, 0.235, CW, 0.76, tint(col, 0.08), tint(col, 0.3))
    box(bg, x + 0.01, 0.885, CW - 0.02, 0.095, tint(col, 0.22))
    bg.text(x + CW / 2, 0.945, head, ha="center", va="center", fontsize=9.5, color=INK, **BOLD)
    bg.text(x + CW / 2, 0.91, sub, ha="center", va="center", fontsize=8.5, color=INK)

    ax = bare(fig, [x + 0.05, 0.53, CW - 0.07, 0.33], (0, 1.25), (0, 1.05))
    axes_arrows(ax, 0, 0, 1.15, 1.02)
    hB, hA = R * h0, R * R * h0
    ly = [h0[-1] + 0.02]  # label heights, from the bottom up, at least 0.11 apart and clear of the t axis
    for h in (hB, hA):
        ly.append(max(h[-1], ly[-1] + 0.11))
    ly = ly[::-1]
    ax.fill_between(t, 0, h0, color=tint(MUTED, 0.35), lw=0)
    ax.fill_between(t, h0, hB, color=tint(BLUE, 0.2), lw=0)
    ax.fill_between(t, hB, hA, color=tint(C[1], 0.3), lw=0)
    for (h, c, lab), yl in zip(((hA, RED, "A"), (hB, BLUE, "B"), (h0, INK2, "0")), ly):
        ax.plot(t, h, color=c, lw=1.0, ls=(0, (3, 2)))
        ax.text(1.04, max(yl, 0.1), rf"$h_{lab}(t)$", color=c, fontsize=9, va="center")
    ax.text(-0.04, 0.85, r"$h(t)$", ha="right", va="center", fontsize=9, color=INK)
    ax.text(1.0, -0.1, r"$t$", ha="center", va="top", fontsize=9, color=INK)

    ax = bare(fig, [x + 0.07, 0.29, CW - 0.09, 0.18], (0, 1.12), (0, 1.1))
    axes_arrows(ax, 0, 0, 1.12, 1.08)
    ax.plot([0, 1.0], [0.62, 0.62], color=C[2], lw=1.3)
    ax.text(-0.04, 0.62, r"$\frac{h_A(t)}{h_B(t)}$", ha="right", va="center", fontsize=11, color=INK)
    ax.text(0.5, -0.12, r"$t$", ha="center", va="top", fontsize=9, color=INK)

box(bg, 0.005, 0.01, 0.99, 0.205, tint(MUTED, 0.15), tint(MUTED, 0.35))
bg.text(0.025, 0.15, "Proportional hazards assumption:", fontsize=9, va="center", color=INK, **BOLD)
bg.text(0.15, 0.07, r"$h_i(t) = h_0(t)\,\exp(x_i\beta)$", fontsize=11, ha="center", va="center", color=INK)
bg.plot([0.345, 0.345], [0.035, 0.19], color=MUTED, lw=0.8)
bg.text(0.36, 0.155, "The shape of the baseline hazard $h_0(t)$ over time is unknown (it could be increasing,\n"
        "decreasing, or non-monotonic, among many other possibilities).", fontsize=7.5, va="center",
        color=INK, linespacing=1.4)
bg.text(0.36, 0.065, r"The assumption is about the ratio: for any two units $A$ and $B$, "
        r"$\frac{h_A(t)}{h_B(t)} = \exp\{\beta(x_A - x_B)\}$" "\nis constant over time.", fontsize=7.5,
        va="center", color=INK, linespacing=1.6)
save(fig, "illus_proportional_hazard")


# ------------------------------------------------------------ 4. hazard shapes with the same area
# Three made-up hazards over [0, T] rescaled to the same area A (top row); their cumulative hazards all end at A
# (middle row), so the event probability by T, 1 - exp(-A), is the same whatever the shape.
A = 0.45
SHAPES = ((BLUE, 1 / (t + 0.3)),
          (C[1], 0.25 + np.exp(-((t - 0.42) / 0.28) ** 2)),
          (GREEN, 0.5 + 0.55 * np.exp(-((t - 0.18) / 0.09) ** 2) + 0.8 * np.exp(-((t - 0.6) / 0.1) ** 2)
           + 0.4 * np.exp(-((t - 0.9) / 0.06) ** 2)))
fig = plt.figure(figsize=(6.3, 4.3))
bg = canvas(fig)
LX, LW = 0.005, 0.095
PX, PW, GAP = 0.11, 0.289, 0.007
for y, h, lab in ((0.62, 0.37, "Possible\nhazard\nshapes\n(same area)"),
                  (0.30, 0.31, "Cumulative\nhazard\n$H(t)$\n(area under\n$h(t)$)"),
                  (0.165, 0.12, "Event\nprobability\nby time $T$")):
    box(bg, LX, y, LW, h, tint(MUTED, 0.12), tint(MUTED, 0.3))
    bg.text(LX + LW / 2, y + h / 2, lab, ha="center", va="center", fontsize=8.5, color=INK, linespacing=1.3,
            **BOLD)
for k, (col, raw) in enumerate(SHAPES):
    h = raw * A / np.trapezoid(raw, t)
    cum = np.concatenate([[0], np.cumsum((h[1:] + h[:-1]) / 2 * np.diff(t))])
    assert abs(np.trapezoid(h, t) - A) < 1e-9 and abs(cum[-1] - A) < 1e-9
    line_col = shade(col, 0.3) if col == C[1] else col
    x = PX + k * (PW + GAP)
    box(bg, x, 0.62, PW, 0.37, tint(col, 0.12), tint(col, 0.3))
    box(bg, x, 0.30, PW, 0.31, tint(col, 0.12), tint(col, 0.3))

    ax = bare(fig, [x + 0.05, 0.68, PW - 0.08, 0.28], (0, 1.22), (0, 1.3 * h.max()))
    axes_arrows(ax, 0, 0, 1.2, 1.28 * h.max())
    ax.fill_between(t, 0, h, color=tint(col, 0.35), lw=0)
    ax.plot(t, h, color=line_col, lw=1.2, ls=(0, (4, 2)))
    ax.plot([1, 1], [0, 1.2 * h.max()], color=INK, lw=0.6, ls=(0, (3, 2)))
    ax.text(0.5, 0.18 * h.max(), r"$\int_0^T h(t)\,dt = A$", ha="center", va="center", fontsize=9, color=INK)
    ax.text(-0.05, 1.05 * h.max(), r"$h(t)$", ha="right", va="center", fontsize=9, color=INK)
    for xv, s in ((0, "0"), (1, "$T$")):
        ax.text(xv, -0.06 * h.max(), s, ha="center", va="top", fontsize=9, color=INK)
    ax.text(1.16, -0.1 * h.max(), "$t$", ha="center", va="top", fontsize=9, color=INK)

    ax = bare(fig, [x + 0.05, 0.36, PW - 0.08, 0.22], (0, 1.22), (0, 1.35 * A))
    axes_arrows(ax, 0, 0, 1.2, 1.33 * A)
    ax.plot([0, 1], [A, A], color=INK, lw=0.6, ls=(0, (3, 2)))
    ax.plot([1, 1], [0, 1.3 * A], color=INK, lw=0.6, ls=(0, (3, 2)))
    ax.plot(t, cum, color=line_col, lw=1.4)
    ax.scatter([1], [A], s=16, color=line_col, zorder=5, clip_on=False)
    ax.text(-0.08, A, "$A$", ha="right", va="center", fontsize=9, color=INK)
    ax.text(-0.04, 1.3 * A, "$H(t)$", ha="right", va="center", fontsize=9, color=INK)
    for xv, s in ((0, "0"), (1, "$T$")):
        ax.text(xv, -0.07 * A, s, ha="center", va="top", fontsize=9, color=INK)
    ax.text(1.16, -0.12 * A, "$t$", ha="center", va="top", fontsize=9, color=INK)

box(bg, PX, 0.165, 3 * PW + 2 * GAP, 0.12, tint(C[2], 0.08), tint(C[2], 0.25))
bg.text(PX + (3 * PW + 2 * GAP) / 2, 0.225, r"$P(T_{\mathrm{event}} \leq T) = 1 - \exp(-A)$", ha="center",
        va="center", fontsize=13, color=INK)
box(bg, LX, 0.01, PX + 3 * PW + 2 * GAP - LX, 0.135, tint(MUTED, 0.12), tint(MUTED, 0.3))
bg.text(0.5, 0.0775, "The shape of the hazard over time is unknown, but the total area under the hazard (and thus "
        "the event probability by time $T$) can be estimated.", ha="center", va="center", fontsize=6.6, color=INK)
save(fig, "illus_hazard_area")
