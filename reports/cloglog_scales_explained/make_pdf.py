"""Build 'Three scales of the cloglog model' explainer PDF.

Run:  python make_pdf.py            -> cloglog_scales_explained.pdf (+ page PNGs with --png)
All numbers are illustrative; nothing here is fitted to CGPS data.
"""
import sys
import textwrap
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch

HERE = Path(__file__).parent

# Palette: dataviz reference instance (light mode), categorical slots in fixed order.
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#8a8984"
GRID, SURF, SHADE = "#e4e3df", "#fcfcfb", "#efeeea"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans",
    "font.size": 10, "axes.edgecolor": MUTED, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.7, "axes.facecolor": SURF, "figure.facecolor": SURF,
    "lines.linewidth": 2, "axes.titlesize": 10.5, "axes.titleweight": "bold",
    "axes.titlecolor": INK, "axes.titlelocation": "left",
})

W, H = 8.27, 11.69  # A4 portrait, inches
LM, RM = 0.09, 0.91


def cloglog_p(eta):
    return 1 - np.exp(-np.exp(eta))


class Page:
    def __init__(self, pdf, n, title, kicker):
        self.pdf, self.fig = pdf, plt.figure(figsize=(W, H))
        self.fig.text(LM, 0.955, kicker.upper(), color=BLUE, fontsize=8.5, weight="bold")
        self.fig.text(LM, 0.93, title, color=INK, fontsize=17, weight="bold", va="top")
        self.fig.text(RM, 0.025, f"{n}", color=MUTED, fontsize=8.5, ha="right")
        self.fig.text(LM, 0.025, "Three scales of the cloglog model", color=MUTED, fontsize=8.5)
        self.y = 0.885

    def gap(self, d=0.012):
        self.y -= d

    def para(self, s, size=10.3, color=INK, width=92, bold=False):
        lh = size * 1.5 / 72 / H
        for block in s.strip().split("\n\n"):
            for line in textwrap.wrap(" ".join(block.split()), width=width):
                self.fig.text(LM, self.y, line, fontsize=size, color=color, va="top",
                              weight="bold" if bold else "normal")
                self.y -= lh
            self.y -= lh * 0.45

    def callout(self, head, body, width=86):
        lines = textwrap.wrap(" ".join(body.split()), width=width)
        lh = 10 * 1.5 / 72 / H
        h = lh * (len(lines) + 1) + 0.02
        top = self.y
        self.fig.patches.append(FancyBboxPatch(
            (LM, top - h), RM - LM, h, boxstyle="round,pad=0,rounding_size=0.008",
            transform=self.fig.transFigure, facecolor="#eaf2fc", edgecolor="none"))
        self.fig.patches.append(FancyBboxPatch(
            (LM, top - h), 0.006, h, boxstyle="square,pad=0",
            transform=self.fig.transFigure, facecolor=BLUE, edgecolor="none"))
        y = top - 0.012
        self.fig.text(LM + 0.025, y, head, fontsize=10, weight="bold", color=INK, va="top")
        y -= lh
        for line in lines:
            self.fig.text(LM + 0.025, y, line, fontsize=10, color=INK, va="top")
            y -= lh
        self.y = top - h - 0.018

    def axes(self, h, ncols=1, wspace=0.08, left=LM + 0.03, right=RM):
        w = (right - left - wspace * (ncols - 1)) / ncols
        axs = [self.fig.add_axes([left + i * (w + wspace), self.y - h, w, h]) for i in range(ncols)]
        self.y -= h + 0.05
        return axs if ncols > 1 else axs[0]

    def save(self, png_dir=None, n=None):
        self.pdf.savefig(self.fig)
        if png_dir is not None:
            self.fig.savefig(png_dir / f"page_{n}.png", dpi=80)
        plt.close(self.fig)


def page1(pdf, png):
    p = Page(pdf, 1, "Is the probability the final scale?", "The short answer")
    p.para("""Yes. The probability p is what the model finally outputs: the chance that a unit has an
    event within its window. It is the number that is reported, and the one that can be compared
    with what actually happened (calibration).""")
    p.para("""But the model is not built on the probability scale. It is built on the linear predictor
    η, a weighted sum of the covariates, and two fixed steps then carry η to p. The figure follows
    six values of η through both steps.""")
    p.gap(0.005)
    ax = p.axes(0.36)
    etas = np.array([-3, -2, -1, 0, 1, 2])
    lam = np.exp(etas)
    pr = 1 - np.exp(-lam)
    rows = [(2.0, etas, (-3.5, 2.5)), (1.0, lam, (0, 8)), (0.0, pr, (0, 1))]
    to01 = lambda v, lo, hi: (v - lo) / (hi - lo)
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.55, 2.6); ax.axis("off")
    labels = [r"Linear predictor  $\eta=\beta_0+\sum\beta_k x_k$", r"Cumulative hazard  $\Lambda=\exp(\eta)$",
              r"Probability  $p=1-\exp(-\Lambda)$"]
    ranges = ["any real number", "any positive number", "between 0 and 1"]
    ticks = [np.arange(-3, 3), np.arange(0, 9, 2), np.linspace(0, 1, 6)]
    fmts = ["{:.0f}", "{:.0f}", "{:.1f}"]
    xs = []
    for (yrow, vals, (lo, hi)), lab, rng, tk, fm in zip(rows, labels, ranges, ticks, fmts):
        ax.plot([0, 1], [yrow, yrow], color=MUTED, lw=1.2)
        for t in tk:
            xt = to01(t, lo, hi)
            ax.plot([xt, xt], [yrow - 0.04, yrow + 0.04], color=MUTED, lw=1)
            ax.text(xt, yrow - 0.1, fm.format(t), ha="center", va="top", fontsize=8, color=INK2)
        ax.text(0, yrow + 0.3, lab, fontsize=10.5, color=INK, weight="bold", va="bottom")
        ax.text(1, yrow + 0.3, rng, fontsize=9, color=INK2, ha="right", va="bottom", style="italic")
        xs.append(to01(vals, lo, hi))
    for i in range(len(etas)):
        for r in range(2):
            ax.annotate("", xy=(xs[r + 1][i], rows[r + 1][0] + 0.07), xytext=(xs[r][i], rows[r][0] - 0.2),
                        arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1, alpha=0.55, shrinkA=0, shrinkB=0))
        for r in range(3):
            ax.plot(xs[r][i], rows[r][0], "o", ms=8, color=BLUE, mec=SURF, mew=2, zorder=5)
    ax.text(0.5, 1.62, r"$\exp(\cdot)$  makes it positive", ha="center", fontsize=9, color=INK2,
            bbox=dict(fc=SURF, ec="none", pad=1))
    ax.text(0.5, 0.62, r"$1-\exp(-\,\cdot)$  squeezes it into (0, 1)", ha="center", fontsize=9, color=INK2,
            bbox=dict(fc=SURF, ec="none", pad=1))
    p.para("""Read the figure from top to bottom. The six points are equally spaced on η, one unit apart.
    After the first step they are spread out to the right; after the second they are crowded
    together near 1. Equal steps on η are not equal steps on p. That bend is what "linear on a
    transformed scale" means: the straight line lives on η, and p is a curved function of it.""")
    p.callout("Each scale has its own job", """η is where the model is fitted, because a weighted sum
    is simple to estimate and test. Λ is where the coefficients are read, because exp(β) is a hazard
    ratio. p is where results are reported, because it is the quantity a reader and the data
    understand. The next pages show why this split is a good idea.""")
    p.save(png, 1)


def page2(pdf, png):
    p = Page(pdf, 2, "Why not fit a straight line to p directly?", "Reason 1: probabilities have walls")
    p.para("""The obvious alternative is to put the weighted sum straight onto the probability,
    p = β0 + β1·x. A straight line has no walls, so for large or small enough x it leaves the
    interval from 0 to 1 and predicts probabilities that cannot exist.""")
    ax = p.axes(0.34)
    x = np.linspace(-3, 10, 400)
    lin = 0.06 + 0.11 * x
    cl = cloglog_p(-2.6 + 0.55 * x)
    ax.axhspan(1, 1.4, color=SHADE, zorder=0); ax.axhspan(-0.4, 0, color=SHADE, zorder=0)
    ax.text(-2.8, 1.2, "impossible: p > 1", color=INK2, fontsize=9, va="center")
    ax.text(-2.8, -0.2, "impossible: p < 0", color=INK2, fontsize=9, va="center")
    ax.plot(x, lin, color=ORANGE, label="Straight line on p")
    ax.plot(x, cl, color=BLUE, label="Straight line on η, then mapped to p (cloglog)")
    ax.axhline(0, color=MUTED, lw=1); ax.axhline(1, color=MUTED, lw=1)
    ax.set_ylim(-0.4, 1.4); ax.set_xlim(-3, 10)
    ax.set_xlabel("Covariate x"); ax.set_ylabel("Predicted probability p")
    ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.27), frameon=False, fontsize=9)
    p.para("""The blue curve is the same idea, a straight line in x, but drawn on η and then carried
    to p through the two steps from page 1. Whatever value η takes, the result stays between 0 and
    1. The model can never predict an impossible probability, by construction and not by luck.""")
    p.para("""There is a second, quieter problem with the orange line. It says that one more unit of x
    always adds the same amount, here 0.11, to the probability. For a unit already at p = 0.95 that
    is impossible, and for a unit at p = 0.01 it would be an elevenfold increase. A constant
    additive effect on p does not make sense across the whole range of risk.""")
    p.callout("In one sentence", """Probabilities are bounded and rates are not, so the model is made
    linear on a scale without bounds and only converted to a probability at the end.""")
    p.save(png, 2)


def page3(pdf, png):
    p = Page(pdf, 3, "One coefficient, many probability changes", "Reason 2: a single number for the effect")
    p.para("""Take a covariate with β = 1. Increasing it by one unit always moves η up by exactly 1,
    wherever the unit starts. On the probability scale the same step is small for a low-risk unit
    and large for a medium-risk unit, and small again near the top.""")
    ax = p.axes(0.36)
    eta = np.linspace(-4.5, 2.2, 400)
    ax.plot(eta, cloglog_p(eta), color=BLUE)
    starts = [(-3.5, ORANGE), (-0.5, AQUA), (1.0, YELLOW)]
    for s, c in starts:
        a, b = cloglog_p(s), cloglog_p(s + 1)
        ax.plot([s, s + 1], [a, a], color=c, lw=2)
        ax.plot([s + 1, s + 1], [a, b], color=c, lw=2)
        ax.plot([s, s + 1], [a, b], "o", color=c, ms=8, mec=SURF, mew=2, zorder=5)
        right = s < 0.5
        ax.text(s + 1.08 if right else s - 0.1, (a + b) / 2 if right else a + 0.02,
                f"Δp = {b - a:+.2f}\n({a:.2f} → {b:.2f})", fontsize=9, color=INK,
                va="center" if right else "bottom", ha="left" if right else "right")
        ax.text(s + 0.5, a - 0.035, "+1 on η", fontsize=8.5, color=INK2, ha="center", va="top")
    ax.set_xlabel("Linear predictor η"); ax.set_ylabel("Probability p")
    ax.set_xlim(-4.6, 3.2); ax.set_ylim(-0.08, 1.05)
    p.para("""All three steps are the same effect, β = 1. On the hazard scale they are also the same:
    each multiplies the hazard by exp(1) ≈ 2.7. Only on the probability scale do they look
    different, because there the effect depends on the starting risk.""")
    p.para("""This is the practical advantage. One coefficient describes the covariate for every unit,
    whatever its baseline risk, and exp(β) is a hazard ratio that can be reported directly. On the
    probability scale a covariate would need a different number for every starting point.""")
    p.callout("Useful approximation for rare events", """When risks are small, p ≈ Λ, because
    1 − exp(−Λ) ≈ Λ for small Λ. The hazard ratio is then close to the ratio of probabilities (the
    relative risk). The orange step on the left shows this: the hazard is multiplied by 2.7 and the
    probability by about 2.6.""")
    p.save(png, 3)


def page4(pdf, png):
    p = Page(pdf, 4, "The same two units on all three scales", "Seeing the effect from three angles")
    p.para("""Two groups of units differ only in one binary covariate with β = 1.2 (group B has it,
    group A does not). Both also share a continuous covariate x. The three panels plot the same
    model on the three scales.""")
    p.gap(0.025)
    axs = p.axes(0.26, ncols=3, wspace=0.075)
    x = np.linspace(0, 5, 200)
    eA, eB = -3 + 0.5 * x, -3 + 0.5 * x + 1.2
    panels = [(eA, eB, "η  (fitting)", "η"), (np.exp(eA), np.exp(eB), "Λ  (interpreting)", "Λ"),
              (cloglog_p(eA), cloglog_p(eB), "p  (reporting)", "p")]
    for ax, (a, b, t, yl) in zip(axs, panels):
        ax.plot(x, a, color=BLUE); ax.plot(x, b, color=ORANGE)
        ax.set_title(t); ax.set_xlabel("Covariate x"); ax.set_ylabel(yl, rotation=0, labelpad=8)
        ax.text(x[-1], a[-1], " A", color=INK, fontsize=9, va="center")
        ax.text(x[-1], b[-1], " B", color=INK, fontsize=9, va="center")
        ax.set_xlim(0, 5.7)
    for xi in [1, 4]:
        i = np.argmin(abs(x - xi))
        axs[0].annotate("", xy=(xi, eB[i]), xytext=(xi, eA[i]),
                        arrowprops=dict(arrowstyle="<->", color=INK2, lw=1))
        axs[0].text(xi + 0.12, (eA[i] + eB[i]) / 2, "+1.2", fontsize=8.5, color=INK2, va="center")
        axs[1].annotate("", xy=(xi, np.exp(eB[i])), xytext=(xi, np.exp(eA[i])),
                        arrowprops=dict(arrowstyle="<->", color=INK2, lw=1))
        axs[1].text(xi - 0.12, np.exp(eB[i]) + 0.12, "×3.3", fontsize=8.5, color=INK2, ha="right")
        pa, pb = cloglog_p(eA[i]), cloglog_p(eB[i])
        axs[2].annotate("", xy=(xi, pb), xytext=(xi, pa), arrowprops=dict(arrowstyle="<->", color=INK2, lw=1))
        axs[2].text(xi - 0.12, pb + 0.03, f"×{pb / pa:.1f}", fontsize=8.5, color=INK2, ha="right")
    axs[2].set_ylim(0, 1)
    p.para("""Left: on η the two lines are parallel. The gap is 1.2 everywhere, which is exactly what
    "linear in the covariates" means. Effects add.""")
    p.para("""Middle: on the hazard scale the gap grows, but the ratio stays fixed: B always has
    exp(1.2) ≈ 3.3 times the hazard of A. Effects multiply, and the multiplier is the hazard ratio.""")
    r1 = cloglog_p(-3 + 0.5 + 1.2) / cloglog_p(-3 + 0.5)
    r4 = cloglog_p(-3 + 2 + 1.2) / cloglog_p(-3 + 2)
    p.para(f"""Right: on the probability scale neither the gap nor the ratio is constant. At x = 1 the
    probability in B is {r1:.1f} times that in A; at x = 4 it is only {r4:.1f} times, because B is
    approaching 1 and has less room left to grow.""")
    p.callout("Why this is the smart arrangement", """The model is fitted where effects add (η),
    read where effects multiply by a constant (Λ), and reported where the numbers mean something
    to a reader (p). Each scale is used for what it is good at, and the two fixed steps between
    them mean nothing is lost on the way.""")
    p.save(png, 4)


def page5(pdf, png):
    p = Page(pdf, 5, "Why 9 or 12 years of follow-up does not matter",
             "Reason 3: the effect does not depend on the window")
    p.para("""Two units, A and B, have a constant hazard over time, and B's hazard is 1.8 times A's.
    The longer they are followed, the more likely each is to have had an event. The top panel shows
    their probabilities as the window grows; the dashed lines mark 9 and 12 years.""")
    t = np.linspace(0.2, 25, 400)
    lam0, hr = 0.04, 1.8
    pA, pB = 1 - np.exp(-lam0 * t), 1 - np.exp(-hr * lam0 * t)
    ax = p.axes(0.18, right=RM - 0.12)
    ax.plot(t, pA, color=BLUE); ax.plot(t, pB, color=ORANGE)
    ax.text(25.3, pA[-1], " A", va="center", fontsize=9); ax.text(25.3, pB[-1], " B", va="center", fontsize=9)
    for tt in (9, 12):
        ax.axvline(tt, color=MUTED, ls="--", lw=1)
    ax.set_ylabel("Probability of event"); ax.set_xlim(0, 25); ax.set_ylim(0, 1)
    ax.set_xlabel("Length of observation window (years)")
    p.para("""The bottom panel asks how much riskier B is than A, measured three ways. Only one of
    them gives the same answer at 9 and at 12 years.""")
    ax2 = p.axes(0.2, right=RM - 0.12)
    rr, orr = pB / pA, (pB / (1 - pB)) / (pA / (1 - pA))
    ax2.plot(t, np.full_like(t, hr), color=BLUE)
    ax2.plot(t, rr, color=ORANGE); ax2.plot(t, orr, color=AQUA)
    ax2.text(25.3, hr, " Hazard ratio", va="center", fontsize=9)
    ax2.text(25.3, rr[-1], " Probability ratio", va="center", fontsize=9)
    ax2.text(25.3, orr[-1], " Odds ratio", va="center", fontsize=9)
    for tt in (9, 12):
        ax2.axvline(tt, color=MUTED, ls="--", lw=1)
        i = np.argmin(abs(t - tt))
        for v in (hr, rr[i], orr[i]):
            ax2.plot(tt, v, "o", ms=6, color=INK2, mec=SURF, mew=1.5, zorder=5)
        ax2.text(tt, 0.92, f"{tt} y", ha="center", fontsize=8.5, color=INK2,
                 bbox=dict(fc=SURF, ec="none", pad=1))
    i9, i12 = np.argmin(abs(t - 9)), np.argmin(abs(t - 12))
    ax2.set_xlim(0, 25); ax2.set_ylim(0.85, 3.4)
    ax2.set_xlabel("Length of observation window (years)"); ax2.set_ylabel("B compared with A")
    p.para(f"""The hazard ratio is 1.8 whatever the window. The probability ratio falls (from
    {rr[i9]:.2f} at 9 years to {rr[i12]:.2f} at 12), and the odds ratio rises (from {orr[i9]:.2f}
    to {orr[i12]:.2f}). If patients with different follow-up were pooled on the probability or odds
    scale, part of the estimated effect would really be a difference in follow-up time. On the
    hazard scale it is not.""")
    p.callout("How follow-up then enters the model", """A longer window only adds risk that is the
    same for everyone: η moves up by log(window length). With an offset, a patient followed 12
    years gets +log(12/9) ≈ 0.29 on η relative to one followed 9 years, and every β is left
    untouched. This holds if the hazard ratio really is constant over the window (proportional
    hazards); with one follow-up scan that assumption cannot be checked.""")
    p.save(png, 5)


def page6(pdf, png):
    p = Page(pdf, 6, "Adding up the units of a cluster", "Reason 4: hazards add, probabilities do not")
    p.para("""Often the question is not about one unit but about the whole cluster: does at least one
    of its units have an event? Here the hazard scale pays off a second time.""")
    lam = np.array([0.10, 0.25, 0.05, 0.40])
    pu = 1 - np.exp(-lam)
    ax = p.axes(0.2)
    cols = [BLUE, ORANGE, AQUA, YELLOW]
    left = 0
    for j, (l, c) in enumerate(zip(lam, cols)):
        ax.barh(1, l - 0.006, left=left, color=c, height=0.5)
        ax.text(left + l / 2, 1.38, f"unit {j + 1}\nΛ = {l:.2f}", ha="center", fontsize=8.5, color=INK, va="bottom")
        left += l
    ax.text(left + 0.02, 1, f"cluster Λ = {lam.sum():.2f}", va="center", fontsize=9.5, color=INK, weight="bold")
    ax.set_xlim(0, 1.15); ax.set_ylim(0.5, 2.0); ax.set_yticks([])
    ax.set_xlabel("Cumulative hazard Λ"); ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    p.para("""On the hazard scale the units simply stack: the cluster's cumulative hazard is the sum of
    its units' hazards. One more step gives the cluster probability,
    P(at least one event) = 1 − exp(−ΣΛ), which follows from multiplying the units' chances of
    staying event-free.""")
    p.para("""On the probability scale there is no such shortcut. Adding the unit probabilities
    double-counts the clusters where two units both have an event, so it overstates the risk.""")
    ax2 = p.axes(0.17)
    vals = [pu.sum(), 1 - np.exp(-lam.sum())]
    labs = ["Sum of unit probabilities (wrong)", "1 − exp(−sum of hazards) (correct)"]
    ax2.barh([1, 0], vals, color=[MUTED, BLUE], height=0.5)
    for yy, v in zip([1, 0], vals):
        ax2.text(v + 0.01, yy, f"{v:.2f}", va="center", fontsize=9.5, color=INK)
    ax2.set_yticks([])
    for yy, lab in zip([1, 0], labs):
        ax2.text(0, yy + 0.3, lab, fontsize=9, color=INK2, va="bottom")
    ax2.set_ylim(-0.4, 1.7); ax2.spines["left"].set_visible(False)
    ax2.set_xlim(0, 1); ax2.set_xlabel("Probability that the cluster has at least one event")
    ax2.grid(axis="y", visible=False)
    p.para(f"""With the four units above, adding probabilities gives {vals[0]:.2f}, while the correct
    value is {vals[1]:.2f}. The gap grows as unit risks get larger or clusters get bigger.""")
    p.callout("Link to the thesis text", """This is the step in "From Unit Risk to Cluster Risk":
    given the cluster effect, the product of the units' event-free probabilities collapses to a
    single exponential of the summed hazards. It is exact only because the model is built on the
    hazard scale.""")
    p.save(png, 6)


def page7(pdf, png):
    p = Page(pdf, 7, "Summary", "Putting it together")
    ax = p.axes(0.27)
    ax.axis("off")
    hdr = ["Scale", "Range", "One unit more of x", "Used for"]
    rows = [["η  (linear predictor)", "−∞ to ∞", "adds β", "fitting and testing"],
            ["Λ  (cumulative hazard)", "0 to ∞", "multiplies by exp(β)", "interpreting (hazard ratio)"],
            ["p  (probability)", "0 to 1", "depends on baseline risk", "reporting and calibration"]]
    xc = [0.0, 0.27, 0.38, 0.68]
    ax.set_xlim(0, 1); ax.set_ylim(0, 4)
    for x0, h in zip(xc, hdr):
        ax.text(x0, 3.5, h, weight="bold", fontsize=10, color=INK, va="center")
    ax.plot([0, 1], [3.15, 3.15], color=INK2, lw=1)
    for r, row in enumerate(rows):
        yy = 2.6 - r * 0.9
        for x0, v in zip(xc, row):
            ax.text(x0, yy, v, fontsize=9.6, color=INK, va="center")
        ax.plot([0, 1], [yy - 0.45, yy - 0.45], color=GRID, lw=1)
    p.para("Why fitting on a transformed scale and reporting on the probability scale is smart:", bold=True)
    for b in [
        "1. Predictions can never fall outside 0 and 1, whatever the covariates (page 2).",
        "2. One coefficient describes the effect for every unit, whatever its baseline risk (pages 3–4).",
        "3. exp(β) is a hazard ratio that does not depend on the length of follow-up, so patients "
        "followed 9 and 12 years can be pooled (page 5).",
        "4. Unit hazards add up to a cluster hazard, which gives the cluster risk exactly (page 6).",
        "5. The final answer is still a probability, the scale on which risk is communicated and "
        "checked against outcomes.",
    ]:
        p.para(b, width=88)
    p.gap(0.01)
    p.callout("The thesis sentence, in plain words", """"Rearranging shows that the model is linear
    in the covariates on a transformed scale" means: the covariates are combined as a weighted sum,
    and that sum is set equal to log(−log(1 − p)) rather than to p itself. The probability is
    recovered at the end by undoing the transformation.""")
    p.callout("What the scales do not fix", """All of this rests on proportional hazards: the
    covariate multiplies the hazard by the same factor throughout the window. If that fails, the
    hazard ratio is an average over the window, and the window-length argument on page 5 weakens.""")
    p.save(png, 7)


def main():
    png = None
    if "--png" in sys.argv:
        png = HERE / "png"
        png.mkdir(exist_ok=True)
    out = HERE / "cloglog_scales_explained.pdf"
    with PdfPages(out) as pdf:
        for f in (page1, page2, page3, page4, page5, page6, page7):
            f(pdf, png)
        d = pdf.infodict()
        d["Title"] = "Three scales of the cloglog model"
    print(out)


if __name__ == "__main__":
    main()
