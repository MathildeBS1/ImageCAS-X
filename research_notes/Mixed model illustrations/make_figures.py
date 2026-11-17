"""Figures for mixed_model_illustrations.pdf: the parts of the who model, one figure each.

The model drawn is the decided who model (root CLAUDE.md): a segment-level cloglog GLMM over nine
segments with a person random intercept b_i ~ N(0, s^2), segment intercepts, the six risk factors,
curvature per segment, and the LM angle and ln(D_LCx/D_LAD) entering the pLAD and pLCx rows.
Person risk integrates over b as in CGPS_data/progression_who_pooled.py (person_risk).

All numbers are simulated (fixed seed). No CGPS data are read.

    python make_figures.py      # writes fig01_*.pdf ... fig10_*.pdf next to this file
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle
from scipy import stats

OUT = Path(__file__).resolve().parent
RNG = np.random.default_rng(20261116)

# Reference palette (dataviz skill), light mode, first three categorical slots only.
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#a3a29c", "#e6e5e0", "#ffffff"
BLUES = ["#dbe9fa", "#a9cbf2", "#6fa6e6", "#2a78d6", "#1a56a3", "#0f3a73"]

SEGS = ["pLAD", "mLAD", "dLAD", "pLCx", "mLCx", "dLCx", "pRCA", "mRCA", "dRCA"]
ARTERY_COL = {"LAD": BLUE, "LCx": ORANGE, "RCA": AQUA}
ALPHA = np.array([-2.2, -2.5, -3.6, -3.2, -3.6, -4.2, -2.9, -3.1, -3.7])  # illustrative segment intercepts
STAMP = "Simulated numbers, illustrative only. Not CGPS data."

plt.rcParams.update({
    "font.family": "serif", "mathtext.fontset": "cm", "font.size": 9, "axes.titlesize": 9.5,
    "axes.labelsize": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK2, "xtick.color": INK2,
    "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False,
    "grid.color": GRID, "grid.linewidth": 0.6, "legend.frameon": False, "lines.linewidth": 2,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.04, "figure.facecolor": SURF,
})


def inv_cloglog(eta):
    return 1 - np.exp(-np.exp(eta))


def save(fig, name):
    fig.text(0.995, 1.0, STAMP, ha="right", va="bottom", fontsize=6.5, color=MUTED, style="italic",
             transform=fig.transFigure)
    fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)


def artery(name, t):
    """Schematic 2D centerline of one artery, t in [0, 1] from ostium to distal end."""
    if name == "LAD":
        return 0.8 + 0.5 * t + 0.4 * np.sin(np.pi * t), -0.4 - 3.6 * t
    if name == "LCx":
        return 0.8 + 2.4 * np.sin(0.5 * np.pi * t), -0.4 - 0.3 * t - 2.4 * t ** 2
    return -0.8 - 1.5 * np.sin(0.5 * np.pi * t), -0.2 - 0.8 * t - 2.8 * t ** 2


def draw_tree(ax, seg_colors, lw=7, labels=True, label_vals=None):
    """Nine segments (thirds of LAD, LCx, RCA) plus the LM, coloured per segment."""
    ax.plot([0.0, 0.8], [0.0, -0.4], color=MUTED, lw=lw, solid_capstyle="round")
    ax.text(0.3, 0.05, "LM", color=INK2, fontsize=7.5, ha="center", va="bottom")
    for a, name in enumerate(["LAD", "LCx", "RCA"]):
        for s in range(3):
            j = 3 * a + s
            t = np.linspace(s / 3 + 0.012, (s + 1) / 3 - 0.012, 40)
            x, y = artery(name, t)
            ax.plot(x, y, color=seg_colors[j], lw=lw, solid_capstyle="butt")
            if labels:
                xm, ym = artery(name, np.array([(s + 0.5) / 3]))
                dx, dy = {"LAD": (-0.25, 0), "LCx": (0.2, 0.3), "RCA": (-0.25, 0)}[name]
                txt = SEGS[j] if label_vals is None else f"{SEGS[j]} {label_vals[j]}"
                ax.text(xm[0] + dx, ym[0] + dy, txt, fontsize=7, color=INK, ha="right" if dx < 0 else "left",
                        va="center")
    ax.set_aspect("equal")
    ax.axis("off")


# ---------------------------------------------------------------- 1 data layout
def fig_data_layout():
    fig, (a0, a1) = plt.subplots(1, 2, figsize=(7.6, 3.8), gridspec_kw={"width_ratios": [1, 1.5]})
    y = np.array([1, 0, 0, 0, 0, 0, 1, 0, 0])
    draw_tree(a0, [ORANGE if v else GRID for v in y])
    a0.set_xlim(-3.4, 4.6)
    a0.set_ylim(-4.6, 0.4)
    a0.set_title("One person $i$ at follow-up", color=INK)
    a0.plot([], [], color=ORANGE, lw=6, label="developed plaque ($y_{ij}=1$)")
    a0.plot([], [], color=GRID, lw=6, label="no plaque ($y_{ij}=0$)")
    a0.legend(loc="upper center", bbox_to_anchor=(0.5, 0.0), fontsize=7.5, ncol=1)

    # long format: nine rows for this person
    cols = ["person", "segment $j$", "risk factors\n(person)", "curvature\n(segment)", "angle, asym.\n(person)",
            "$y_{ij}$"]
    widths = [1.0, 1.1, 1.5, 1.4, 1.5, 0.6]
    xs = np.r_[0, np.cumsum(widths)]
    a1.set_xlim(0, xs[-1])
    a1.set_ylim(-9.6, 1.6)
    a1.axis("off")
    for c, name in enumerate(cols):
        a1.text((xs[c] + xs[c + 1]) / 2, 0.85, name, ha="center", va="center", fontsize=7, color=INK)
    curv = RNG.normal(0, 1, 9)
    for r in range(9):
        top = -r
        for c in range(6):
            fc = SURF
            if c == 5:
                fc = ORANGE if y[r] else GRID
            a1.add_patch(Rectangle((xs[c] + 0.03, top - 0.94), widths[c] - 0.06, 0.88, fc=fc, ec=GRID, lw=0.6))
        a1.text((xs[1] + xs[2]) / 2, top - 0.5, SEGS[r], ha="center", va="center", fontsize=7.5)
        a1.text((xs[3] + xs[4]) / 2, top - 0.5, f"{curv[r]:+.1f}", ha="center", va="center", fontsize=7.5)
        if SEGS[r] in ("pLAD", "pLCx"):
            a1.text((xs[4] + xs[5]) / 2, top - 0.5, "entered", ha="center", va="center", fontsize=7.5, color=INK)
        else:
            a1.add_patch(Rectangle((xs[4] + 0.03, top - 0.94), widths[4] - 0.06, 0.88, fc="none", ec=MUTED,
                                   lw=0, hatch="////", alpha=0.35))
        a1.text((xs[5] + xs[6]) / 2, top - 0.5, str(y[r]), ha="center", va="center", fontsize=7.5,
                color=SURF if y[r] else INK2)
    # merged person-level cells
    for c, txt in [(0, "$i$"), (2, "same 6 values\nin all 9 rows")]:
        a1.add_patch(Rectangle((xs[c] + 0.03, -8.94), widths[c] - 0.06, 8.88, fc="#f4f3ef", ec=GRID, lw=0.6))
        a1.text((xs[c] + xs[c + 1]) / 2, -4.5, txt, ha="center", va="center", fontsize=7.5, color=INK)
    a1.text(xs[-1] / 2, -9.35, "the same 9 rows for every person; all rows of all people form one data set",
            ha="center", va="center", fontsize=7, color=INK2)
    a1.set_title("Its 9 rows in the model data", color=INK)
    save(fig, "fig01_data_layout")


# ---------------------------------------------------------------- 2 design matrix
def fig_design_matrix():
    names = ["age", "sex", "smoking", "SBP", "TC", "HDL", "curvature", "LM angle", r"$\ln(D_{LCx}/D_{LAD})$"]
    n_people = 3
    rows, labels, people = [], [], []
    for i in range(n_people):
        rf = RNG.normal(0, 1, 6)
        rf[1], rf[2] = RNG.integers(0, 2), RNG.integers(0, 2)
        ang, asym = RNG.normal(0, 1, 2)
        for j, s in enumerate(SEGS):
            g = [RNG.normal(0, 1), ang if s in ("pLAD", "pLCx") else np.nan,
                 asym if s in ("pLAD", "pLCx") else np.nan]
            rows.append(np.r_[rf, g])
            labels.append(s)
            people.append(i)
    M = np.array(rows)
    fig, ax = plt.subplots(figsize=(6.4, 6.6))
    cmap = plt.get_cmap("RdBu_r").copy()
    im = ax.imshow(np.ma.masked_invalid(M), cmap=cmap, vmin=-2.2, vmax=2.2, aspect="auto",
                   interpolation="nearest")
    for (r, c), v in np.ndenumerate(M):
        if np.isnan(v):
            ax.add_patch(Rectangle((c - 0.5, r - 0.5), 1, 1, fc="#f4f3ef", ec="none"))
            ax.text(c, r, "0", ha="center", va="center", fontsize=6.5, color=MUTED)
    for k in range(1, n_people):
        ax.axhline(9 * k - 0.5, color=INK, lw=1.2)
    for c in range(1, 9):
        ax.axvline(c - 0.5, color=SURF, lw=1.5)
    ax.axvline(5.5, color=INK, lw=1.2)
    ax.set_xticks(range(9), names, rotation=40, ha="right")
    ax.set_yticks(range(len(labels)), labels, fontsize=7)
    ax.tick_params(length=0)
    for i in range(n_people):
        ax.text(-2.3, 9 * i + 4, f"person {i + 1}", rotation=90, ha="center", va="center", color=INK,
                transform=ax.transData, clip_on=False)
    ax.text(2.5, -1.2, "six risk factors: constant within a person", ha="center", fontsize=8, color=INK)
    ax.text(7.0, -1.2, "geometry block (3 columns)", ha="center", fontsize=8, color=INK)
    for s in ax.spines.values():
        s.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
    cb.set_label("standardised value (SD)")
    cb.outline.set_visible(False)
    save(fig, "fig02_design_matrix")


# ---------------------------------------------------------------- 3 linear predictor
def fig_linear_predictor():
    j = SEGS.index("mLAD")
    parts = [(r"$\alpha_{\mathrm{mLAD}}$" + "\nsegment intercept", ALPHA[j], MUTED),
             ("+ risk factors\n" + r"$x_i^\top\beta$", 0.55, BLUE),
             ("+ geometry\n" + r"$g_{ij}^\top\gamma$", 0.30, ORANGE),
             ("+ person intercept\n" + r"$b_i$", 0.45, AQUA)]
    eta = sum(p[1] for p in parts)
    fig, (a0, a1) = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw={"width_ratios": [1.7, 1]})
    cum = 0.0
    for k, (lab, v, col) in enumerate(parts):
        start = 0.0 if k == 0 else cum
        a0.barh(-k, v, left=start, height=0.6, color=col, edgecolor=SURF, lw=2)
        a0.text(start + v + (0.06 if v > 0 else -0.06), -k, f"{v:+.2f}", va="center",
                ha="left" if v > 0 else "right", fontsize=8, color=INK2)
        cum = start + v
    a0.barh(-4, eta, height=0.6, color=INK, edgecolor=SURF, lw=2)
    a0.text(eta - 0.06, -4, f"{eta:.2f}", va="center", ha="right", fontsize=8, color=SURF)
    a0.axvline(0, color=MUTED, lw=0.8)
    a0.set_xlim(-3.2, 0.3)
    a0.set_yticks([0, -1, -2, -3, -4], [p[0] for p in parts] + [r"$\eta_{ij}$ (linear predictor)"], fontsize=8)
    a0.tick_params(axis="y", length=0)
    a0.spines["left"].set_visible(False)
    a0.set_xlabel("log-hazard scale")
    a0.set_title("mLAD of person $i$: the terms add up on the log-hazard scale", color=INK, loc="left")

    e = np.linspace(-5, 0.5, 300)
    a1.plot(e, inv_cloglog(e), color=INK)
    p = inv_cloglog(eta)
    a1.plot([eta, eta, -5], [0, p, p], color=MUTED, lw=1, ls="--")
    a1.plot(eta, p, "o", ms=7, color=INK, mec=SURF, mew=2)
    a1.text(-4.9, p + 0.03, f"$p_{{ij}}$ = {p:.3f}", fontsize=8, color=INK)
    a1.set_xlim(-5, 0.5)
    a1.set_ylim(0, 0.8)
    a1.set_xlabel(r"$\eta_{ij}$")
    a1.set_ylabel("P(plaque in segment)")
    a1.set_title(r"$p_{ij}=1-\exp(-e^{\eta_{ij}})$", color=INK)
    save(fig, "fig03_linear_predictor")


# ---------------------------------------------------------------- 4 segment intercepts
def fig_segment_intercepts():
    p = inv_cloglog(ALPHA)
    bins = np.linspace(p.min() - 1e-9, p.max() + 1e-9, len(BLUES) + 1)
    cols = [BLUES[min(np.searchsorted(bins, v) - 1, len(BLUES) - 1)] for v in p]
    fig, (a0, a1) = plt.subplots(1, 2, figsize=(7.4, 3.4), gridspec_kw={"width_ratios": [1.1, 1]})
    draw_tree(a0, cols)
    a0.set_xlim(-3.6, 4.6)
    a0.set_ylim(-4.3, 0.9)
    a0.set_title("Darker = higher baseline risk", color=INK)
    order = np.argsort(ALPHA)
    a1.hlines(range(9), -4.5, ALPHA[order], color=GRID, lw=1)
    for r, j in enumerate(order):
        art = SEGS[j][1:]
        a1.plot(ALPHA[j], r, "o", ms=8, color=ARTERY_COL[art], mec=SURF, mew=2)
        a1.text(ALPHA[j] + 0.08, r, f"{p[j]:.1%}", va="center", fontsize=7.5, color=INK2)
    a1.set_yticks(range(9), [SEGS[j] for j in order])
    a1.set_xlim(-4.5, -1.6)
    a1.set_xlabel(r"segment intercept $\alpha_j$ (log-hazard)")
    for art, c in ARTERY_COL.items():
        a1.plot([], [], "o", color=c, label=art)
    a1.legend(loc="lower right", fontsize=7.5)
    a1.set_title(r"$\alpha_j$ with its risk $1-\exp(-e^{\alpha_j})$", color=INK)
    save(fig, "fig04_segment_intercepts")


# ---------------------------------------------------------------- 5 cloglog link
def fig_link():
    e = np.linspace(-6, 2.5, 400)
    pc, pl = inv_cloglog(e), 1 / (1 + np.exp(-e))
    fig, (a0, a1) = plt.subplots(1, 2, figsize=(7.2, 2.9))
    for ax in (a0, a1):
        ax.plot(e, pc, color=BLUE, label="cloglog")
        ax.plot(e, pl, color=MUTED, ls="--", lw=1.5, label="logit")
        ax.axvspan(-6, -2, color=GRID, alpha=0.6, lw=0)
        ax.set_xlabel(r"linear predictor $\eta$")
    a0.set_ylabel("P(plaque in segment)")
    a0.text(-5.8, 0.9, "the two links agree\nwhere risk is low", fontsize=7.5, color=INK2, va="top")
    a0.text(-1.6, 0.85, r"$1-\exp(-e^{\eta})$", color=BLUE, fontsize=8.5, ha="right")
    a0.text(1.2, 0.55, r"$\frac{e^\eta}{1+e^\eta}$", color=INK2, fontsize=10)
    a0.legend(loc="center left", fontsize=7.5)
    a0.set_title("Probability scale", color=INK)
    a1.set_yscale("log")
    a1.set_ylim(2e-3, 1.2)
    a1.set_title("Log probability scale", color=INK)
    a1.annotate(r"$e^\eta$ = cumulative hazard over follow-up", xy=(-1.0, inv_cloglog(-1.0)),
                xytext=(-5.8, 0.6), fontsize=7.5, color=INK2,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    save(fig, "fig05_cloglog_link")


# ---------------------------------------------------------------- 6 hazard ratio per SD
def fig_hazard_ratio():
    z = np.linspace(-2, 2, 200)
    base = -2.8
    hrs = [(1.0, MUTED), (1.3, BLUE), (1.6, ORANGE)]
    fig, (a0, a1) = plt.subplots(1, 2, figsize=(7.2, 2.9))
    for hr, c in hrs:
        b = np.log(hr)
        a0.plot(z, base + b * z, color=c)
        a1.plot(z, inv_cloglog(base + b * z), color=c)
        a0.text(2.05, base + b * 2, f"HR {hr:.1f}", color=INK, fontsize=7.5, va="center")
        a1.text(2.05, inv_cloglog(base + b * 2), f"HR {hr:.1f}", color=INK, fontsize=7.5, va="center")
    b = np.log(1.6)
    a0.plot([0, 1, 1], [base, base, base + b], color=INK, lw=1)
    a0.text(0.5, base - 0.12, "+1 SD", ha="center", va="top", fontsize=7.5)
    a0.text(1.05, base + b / 2, r"$+\gamma=\ln 1.6$", va="center", fontsize=7.5)
    a0.set_ylabel(r"log hazard $\eta$")
    a0.set_title("Log-hazard scale: a straight line, slope $\\gamma$", color=INK)
    p0, p1 = inv_cloglog(base), inv_cloglog(base + b)
    a1.plot([0, 1], [p0, p1], "o", color=INK, ms=6, mec=SURF, mew=1.5)
    a1.text(-1.95, 0.14, "hazard $\\times e^{\\gamma}$ per SD;\n"
            f"risk {p0:.3f} → {p1:.3f} at 0 → 1 SD", fontsize=7.5, color=INK2, va="top")
    a1.set_ylabel("P(plaque in segment)")
    a1.set_title("Probability scale", color=INK)
    for ax in (a0, a1):
        ax.set_xlabel("curvature (SD from the mean)")
        ax.set_xlim(-2, 2.8)
    save(fig, "fig06_hazard_ratio")


# ---------------------------------------------------------------- 7 random intercept
def fig_random_intercept():
    s = 0.8
    bs = np.array([-1.2, -0.5, 0.0, 0.6, 1.3])
    shades = ["#a9cbf2", "#6fa6e6", "#2a78d6", "#1a56a3", "#0f3a73"]
    fig, (a0, a1, a2) = plt.subplots(1, 3, figsize=(7.4, 2.7), gridspec_kw={"width_ratios": [0.8, 1.2, 1]})
    u = np.linspace(-3, 3, 300)
    a0.fill_between(u, stats.norm.pdf(u, 0, s), color=GRID, lw=0)
    a0.plot(u, stats.norm.pdf(u, 0, s), color=INK2, lw=1.2)
    for b, c in zip(bs, shades):
        a0.plot([b, b], [0, stats.norm.pdf(b, 0, s)], color=c, lw=2)
    a0.set_xlabel("$b_i$")
    a0.set_yticks([])
    a0.spines["left"].set_visible(False)
    a0.set_title(rf"(a) $b_i\sim N(0,\sigma^2)$, $\sigma$={s}", color=INK)

    for b, c in zip(bs, shades):
        a1.plot(range(9), inv_cloglog(ALPHA + b), "-o", color=c, ms=4, lw=1.5)
        a1.text(8.2, inv_cloglog(ALPHA[-1] + b), f"$b$={b:+.1f}", fontsize=7, va="center", color=INK2)
    a1.set_yscale("log")
    a1.set_xticks(range(9), SEGS, rotation=60, fontsize=7)
    a1.set_xlim(-0.3, 9.4)
    a1.set_ylabel("P(plaque in segment)")
    a1.set_title("(b) $b_i$ moves all 9 segments together", color=INK)

    # clustering: number of segments with plaque per person, sigma 0 vs 0.8, same expected total
    m = 40000
    def counts(sig, shift):
        bb = RNG.normal(0, sig, (m, 1)) if sig > 0 else np.zeros((m, 1))
        return (RNG.random((m, 9)) < inv_cloglog(ALPHA + shift + bb)).sum(1)
    nodes, w = np.polynomial.hermite.hermgauss(60)
    def expected(sig, shift):
        bb = np.sqrt(2) * sig * nodes
        return (w / np.sqrt(np.pi) * inv_cloglog(ALPHA[:, None] + shift + bb[None])).sum()
    target = expected(0, 0)
    lo, hi = -2.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if expected(s, mid) < target else (lo, mid)
    c0, c1 = counts(0, 0), counts(s, lo)
    k = np.arange(0, 6)
    f0 = np.array([(c0 == v).mean() if v < 5 else (c0 >= 5).mean() for v in k])
    f1 = np.array([(c1 == v).mean() if v < 5 else (c1 >= 5).mean() for v in k])
    a2.bar(k - 0.2, f0, 0.38, color=MUTED, edgecolor=SURF, lw=1, label=r"$\sigma=0$ (independent)")
    a2.bar(k + 0.2, f1, 0.38, color=BLUE, edgecolor=SURF, lw=1, label=rf"$\sigma={s}$")
    a2.set_xticks(k, ["0", "1", "2", "3", "4", "5+"])
    a2.set_yscale("log")
    a2.set_xlabel("segments with plaque per person")
    a2.set_ylabel("share of people")
    a2.legend(fontsize=7, loc="upper right")
    a2.set_title("(c) segments cluster within people", color=INK)
    fig.tight_layout(w_pad=1.2)
    save(fig, "fig07_random_intercept")


# ---------------------------------------------------------------- 8 conditional vs averaged
def fig_conditional():
    s, g, base = 1.2, np.log(1.6), -3.0
    z = np.linspace(-2, 2, 200)
    nodes, w = np.polynomial.hermite.hermgauss(60)
    bb, ww = np.sqrt(2) * s * nodes, w / np.sqrt(np.pi)
    pm = (ww[None] * inv_cloglog(base + g * z[:, None] + bb[None])).sum(1)
    fig, (a0, a1) = plt.subplots(1, 2, figsize=(7.2, 2.9))
    for q in stats.norm.ppf([0.1, 0.25, 0.5, 0.75, 0.9]) * s:
        a0.plot(z, inv_cloglog(base + q + g * z), color=GRID if q != 0 else BLUE, lw=1.2 if q else 2)
        a1.plot(z, base + q + g * z, color=GRID if q != 0 else BLUE, lw=1.2 if q else 2)
    a0.plot(z, pm, color=ORANGE)
    lm = np.log(-np.log(1 - pm))
    a1.plot(z, lm, color=ORANGE)
    hr_m = np.exp(np.interp(1, z, lm) - np.interp(0, z, lm))
    a1.text(2.1, base + 2 * g - 0.3, "person with $b_i=0$:\nconditional HR 1.60", fontsize=7, color=INK,
            va="center")
    a1.text(2.1, lm[-1] + 0.3, f"average over people:\nHR about {hr_m:.2f}", fontsize=7, color=INK,
            va="center")
    a1.plot(2.0, base + 2 * g, "o", color=BLUE, ms=5)
    a1.plot(2.0, lm[-1], "o", color=ORANGE, ms=5)
    a0.plot([], [], color=BLUE, label="person with $b_i=0$")
    a0.plot([], [], color=ORANGE, label="average over people")
    a0.plot([], [], color=GRID, lw=1.2, label="other people (10th to 90th centile of $b_i$)")
    a0.legend(loc="upper left", fontsize=7)
    a0.set_ylabel("P(plaque in segment)")
    a1.set_ylabel(r"$\ln(-\ln(1-p))$")
    a0.set_title("Probability scale", color=INK)
    a1.set_title("cloglog scale: the averaged line is flatter", color=INK)
    for ax in (a0, a1):
        ax.set_xlabel("curvature (SD)")
    a1.set_xlim(-2, 3.3)
    save(fig, "fig08_conditional_vs_average")


# ---------------------------------------------------------------- 9 pooling to person risk
def fig_pooling():
    s = 0.8
    nodes, w = np.polynomial.hermite.hermgauss(60)
    bb, ww = np.sqrt(2) * s * nodes, w / np.sqrt(np.pi)
    people = {"person A": ALPHA - 0.6 + RNG.normal(0, 0.25, 9), "person B": ALPHA + 0.5 + RNG.normal(0, 0.25, 9)}
    fig, (a0, a1) = plt.subplots(1, 2, figsize=(7.4, 3.1), gridspec_kw={"width_ratios": [1.15, 1]})
    for r, (name, eta) in enumerate(people.items()):
        h = np.exp(eta)
        p_cond = 1 - np.prod(1 - inv_cloglog(eta))
        assert np.isclose(p_cond, 1 - np.exp(-h.sum()))  # product of segment risks = 1 - exp(-sum of hazards)
        left = 0.0
        for j in range(9):
            col = ARTERY_COL[SEGS[j][1:]]
            a0.barh(-r, h[j], left=left, height=0.5, color=col, edgecolor=SURF, lw=1.5,
                    alpha=[1, 0.7, 0.45][j % 3])
            left += h[j]
        a0.text(0, -r + 0.33, f"$H$ = {left:.2f}, so P(any plaque $|$ $b$=0) = {p_cond:.2f}", va="bottom",
                fontsize=7.5, color=INK)
        pb = 1 - np.exp(-np.exp(bb) * h.sum())
        person = (ww * pb).sum()
        u = np.linspace(-2.6, 2.6, 300)
        c = [MUTED, INK][r]
        a1.plot(u, 1 - np.exp(-np.exp(u) * h.sum()), color=c, lw=1.8)
        a1.axhline(person, color=c, lw=1, ls="--")
        a1.text(-2.55, person + 0.015, f"{name}: person risk {person:.2f}", fontsize=7, color=INK)
        yl = [0.7, 0.9][r]
        k = np.argmin(np.abs(1 - np.exp(-np.exp(u) * h.sum()) - yl))
        a1.text(u[k] + 0.12, yl, name, fontsize=7, color=INK, va="top")
    a0.set_yticks([0, -1], list(people))
    a0.set_xlabel(r"sum of segment hazards $H=\sum_j e^{\eta_j}$ (with $b=0$)")
    a0.set_xlim(0, 0.95)
    a0.set_ylim(-1.5, 1.1)
    a0.legend([Rectangle((0, 0), 1, 1, fc=c) for c in ARTERY_COL.values()],
              [f"{a} (p, m, d)" for a in ARTERY_COL], loc="upper right", fontsize=7)
    a0.set_title("(a) segment hazards add up within a person", color=INK, loc="left")
    a0.text(0.01, 1.0, r"$1-\prod_j(1-p_j) = 1-\exp(-H)$", fontsize=8, color=INK2, va="top")
    ax2 = a1.twinx()
    ax2.fill_between(np.linspace(-2.6, 2.6, 300), stats.norm.pdf(np.linspace(-2.6, 2.6, 300), 0, s),
                     color=GRID, lw=0, zorder=0)
    ax2.set_yticks([])
    ax2.spines["right"].set_visible(False)
    a1.set_zorder(ax2.get_zorder() + 1)
    a1.patch.set_visible(False)
    a1.set_xlabel("person intercept $b$ (grey: its density)")
    a1.set_ylabel(r"P(any plaque $|$ $b$) $=1-\exp(-e^{b}H)$")
    a1.set_ylim(0, 1)
    a1.set_title("(b) averaged over $b$ gives the person risk", color=INK, loc="left")
    save(fig, "fig09_pooling")


# ---------------------------------------------------------------- 10 LR test
def fig_lr_test():
    l0, l1 = -2410.6, -2404.9  # illustrative log-likelihoods
    lr = 2 * (l1 - l0)
    crit = stats.chi2.ppf(0.95, 3)
    fig, (a0, a1) = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw={"width_ratios": [1, 1.2]})
    a0.axis("off")
    a0.set_xlim(0, 1)
    a0.set_ylim(0, 1)
    boxes = [(0.62, "Base model", "segment intercepts + 6 risk factors\n+ person intercept ($\\sigma$)",
              rf"$\ell_0$ = {l0:.1f}", MUTED),
             (0.12, "Base + geometry", "the same + curvature, LM angle,\n" + r"$\ln(D_{LCx}/D_{LAD})$",
              rf"$\ell_1$ = {l1:.1f}", BLUE)]
    for y0, title, body, ll, col in boxes:
        a0.add_patch(Rectangle((0.0, y0), 1.0, 0.3, fc=SURF, ec=col, lw=1.6))
        a0.text(0.04, y0 + 0.24, title, fontsize=8.5, color=INK, va="top", weight="bold")
        a0.text(0.04, y0 + 0.14, body, fontsize=7.5, color=INK2, va="top")
        a0.text(0.96, y0 + 0.24, ll, fontsize=8, color=INK, va="top", ha="right")
    a0.add_patch(FancyArrowPatch((0.5, 0.61), (0.5, 0.43), arrowstyle="-|>", mutation_scale=10, color=INK2))
    a0.text(0.53, 0.52, "+3 parameters", fontsize=7.5, color=INK2, va="center")
    a0.text(0.0, 0.0, rf"LR $=2(\ell_1-\ell_0)$ = {lr:.1f}, compared with $\chi^2_3$", fontsize=8, color=INK)

    x = np.linspace(0, 16, 400)
    d = stats.chi2.pdf(x, 3)
    a1.plot(x, d, color=INK2, lw=1.4)
    a1.fill_between(x[x >= crit], d[x >= crit], color=ORANGE, alpha=0.35, lw=0)
    a1.axvline(lr, color=BLUE, lw=2)
    a1.text(crit + 0.2, 0.12, f"upper 5%\n(from {crit:.2f})", fontsize=7.5, color=INK2)
    a1.text(lr + 0.2, 0.2, f"observed LR\n{lr:.1f}, p = {stats.chi2.sf(lr, 3):.3f}", fontsize=7.5, color=BLUE)
    a1.set_xlabel("LR statistic")
    a1.set_yticks([])
    a1.spines["left"].set_visible(False)
    a1.set_title(r"$\chi^2$ distribution with 3 df under no geometry effect", color=INK)
    save(fig, "fig10_lr_test")


if __name__ == "__main__":
    for f in [fig_data_layout, fig_design_matrix, fig_linear_predictor, fig_segment_intercepts, fig_link,
              fig_hazard_ratio, fig_random_intercept, fig_conditional, fig_pooling, fig_lr_test]:
        f()
        print("done", f.__name__)
