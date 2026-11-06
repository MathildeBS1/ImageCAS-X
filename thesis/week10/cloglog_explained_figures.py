"""Figures for cloglog_explained.tex. Made-up numbers only: the toy model (segment intercepts, three
people, sigma) and the person risk are those of reports/cloglog_model_explained/figures.py, so the
numbers match that report and cloglog_pooled.tex.

    python3 thesis/week10/cloglog_explained_figures.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "reports" / "cloglog_model_explained"))
from figures import PEOPLE, SEGS, SIGMA, eta_of, person_risk, seg_marginal  # noqa: E402

OUT = Path(__file__).resolve().parent / "week_figure" / "cloglog"
OUT.mkdir(parents=True, exist_ok=True)
INK, INK2, GRID, SURF, MUTED = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb", "#8a8984"
C = ("#2a78d6", "#eb6834", "#1baf7a")
SEG_C = ["#2a78d6"] * 3 + ["#eb6834"] * 3 + ["#1baf7a"] * 3     # LAD, LCx, RCA


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


# ------------------------------------------------------------ toy person A, the numbers used in the text
eta_A = eta_of(PEOPLE["A"])
lam_A = np.exp(eta_A)
S_A = lam_A.sum()
P = {k: person_risk(eta_of(p), SIGMA) for k, p in PEOPLE.items()}
B0 = {k: 1 - np.exp(-np.exp(eta_of(p)).sum()) for k, p in PEOPLE.items()}
PROD = {k: 1 - np.prod(1 - seg_marginal(eta_of(p), SIGMA)) for k, p in PEOPLE.items()}
assert (round(P["A"], 3), round(B0["A"], 3), round(PROD["A"], 3)) == (0.548, 0.534, 0.687)
assert round(S_A, 3) == 0.763 and round(lam_A[0], 3) == 0.278
iP, iD = SEGS.index("pLAD"), SEGS.index("dLCx")
p_seg = 1 - np.exp(-lam_A)                       # segment risk at b = 0
print(f"S_A {S_A:.3f}  P_A {P['A']:.3f}  b=0 {B0['A']:.3f}  product {PROD['A']:.3f}")
print(f"pLAD p {p_seg[iP]:.3f} Lambda {lam_A[iP]:.3f} eta {eta_A[iP]:.2f}; "
      f"dLCx p {p_seg[iD]:.3f} Lambda {lam_A[iD]:.3f} eta {eta_A[iD]:.2f}")

# ------------------------------------------------------------ F1. the name as a chain of steps
fig, ax = plt.subplots(figsize=(10.5, 2.5), facecolor=SURF)
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 2.5)
ax.axis("off")
boxes = [("$p$", "segment risk:\ndevelops plaque", f"{p_seg[iP]:.3f}"),
         ("$1-p$", "stays\nplaque-free", f"{1 - p_seg[iP]:.3f}"),
         (r"$\Lambda=-\log(1-p)$", "hazard built up\nover ~10 years", f"{lam_A[iP]:.3f}"),
         (r"$\eta=\log\Lambda$", "any number:\nterms can be added", f"{eta_A[iP]:.2f}"),
         (r"$\eta=\alpha_j+x^\top\beta+b_i$", "GLMM: fixed terms\n+ person effect", "")]
steps = ["c", "log", "log", "model"]
xs = np.array([0.1, 2.15, 4.2, 6.25, 8.3])
for k, (x, (head, sub, val)) in enumerate(zip(xs, boxes)):
    last = k == len(boxes) - 1
    ax.add_patch(FancyBboxPatch((x, 0.35), 1.95 if last else 1.6, 1.35, boxstyle="round,pad=0.04",
                                fc="#e8f0fa" if last else "white", ec=C[0] if last else MUTED, lw=1.2))
    cx = x + (0.975 if last else 0.8)
    ax.text(cx, 1.42, head, ha="center", va="center", fontsize=10.5, color=INK)
    ax.text(cx, 0.92, sub, ha="center", va="center", fontsize=8, color=INK2)
    if val:
        ax.text(cx, 0.52, f"pLAD: {val}", ha="center", va="center", fontsize=8.5, color=C[1])
for k, s in enumerate(steps):
    a, b = xs[k] + 1.62, xs[k + 1] - 0.02
    ax.annotate("", (b, 1.02), (a, 1.02), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    ax.text((a + b) / 2, 1.95, s, ha="center", fontsize=12, color=C[1] if s != "model" else C[0],
            fontweight="bold")
ax.text(0.1, 2.32, "Reading the name: c (complement), log, log, then the linear mixed model on that scale",
        fontsize=9.5, color=INK)
save(fig, "c1_name_chain")

# ------------------------------------------------------------ F2. the three steps as curves
p = np.linspace(0.001, 0.7, 400)
fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.2), facecolor=SURF)
chain = [(p, 1 - p, "1. c: $p \\to 1-p$", "risk $p$", "stays free $1-p$"),
         (1 - p, -np.log(1 - p), "2. log: $1-p \\to \\Lambda = -\\log(1-p)$", "stays free $1-p$",
          "hazard $\\Lambda$"),
         (-np.log(1 - p), np.log(-np.log(1 - p)), "3. log: $\\Lambda \\to \\eta = \\log\\Lambda$",
          "hazard $\\Lambda$", "$\\eta$ (any number)")]
pts = {"pLAD": p_seg[iP], "dLCx": p_seg[iD]}
for ax, (x, y, title, xl, yl) in zip(axs, chain):
    style(ax, title, xl, yl)
    ax.plot(x, y, color=INK2, lw=1.8)
for (name, q), col in zip(pts.items(), (C[0], C[1])):
    vals = [q, 1 - q, -np.log(1 - q), np.log(-np.log(1 - q))]
    for k, ax in enumerate(axs):
        ax.plot(vals[k], vals[k + 1], "o", color=col, ms=6, zorder=3, label=name if k == 0 else None)
        ax.annotate(f"{vals[k + 1]:.3g}", (vals[k], vals[k + 1]), xytext=(8, -12) if k else (6, 4),
                    textcoords="offset points", fontsize=7.5, color=col)
axs[1].plot([0.3, 1], [0.7, 0], color=MUTED, lw=1, ls=":")
axs[1].text(0.32, 0.12, "dotted: $\\Lambda = p$;\nclose at low risk", fontsize=7.5, color=INK2)
axs[0].legend(frameon=False, fontsize=8, loc="upper right")
save(fig, "c2_three_steps")

# ------------------------------------------------------------ F3. hazard ratio stays, odds ratio drifts
p0 = np.linspace(0.005, 0.8, 400)
HR = 1.5
p1 = 1 - (1 - p0) ** HR
odds = (p1 / (1 - p1)) / (p0 / (1 - p0))
fig, ax = plt.subplots(figsize=(5.2, 3.4), facecolor=SURF)
style(ax, "Same geometry effect, HR 1.5, in segments of different risk", "baseline segment risk",
      "ratio")
ax.plot(p0, np.full_like(p0, HR), color=C[0], lw=2.2, label="hazard ratio (cloglog)")
ax.plot(p0, odds, color=C[1], lw=2, label="odds ratio (logit)")
ax.plot(p0, p1 / p0, color=MUTED, lw=1.5, ls="--", label="risk ratio")
for name, q in pts.items():
    ax.axvline(q, color=GRID, lw=1.2, zorder=0)
    ax.text(q + 0.008, 2.15, name, fontsize=8, color=INK2)
for q in (0.01, 0.10, 0.50):
    o = np.interp(q, p0, odds)
    ax.plot(q, o, "o", color=C[1], ms=4)
    ax.annotate(f"{o:.2f}", (q, o), xytext=(4, 4), textcoords="offset points", fontsize=7.5, color=C[1])
ax.set_ylim(1, 2.3)
ax.legend(frameon=False, fontsize=8, loc="center right")
save(fig, "c3_hr_vs_or")

# ------------------------------------------------------------ F4. hazards add, the person effect multiplies all
fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.6), facecolor=SURF, gridspec_kw={"width_ratios": [1, 1.25]})
style(axs[0], "Toy person A: hazard per segment ($b = 0$)", "hazard $\\Lambda_j = e^{\\eta_j}$")
y = np.arange(9)[::-1]
axs[0].barh(y, lam_A, color=SEG_C, height=0.7)
axs[0].set_yticks(y, SEGS)
for yy, v in zip(y, lam_A):
    axs[0].text(v + 0.004, yy, f"{v:.3f}", va="center", fontsize=7.5, color=INK2)
axs[0].set_xlim(0, 0.34)
style(axs[1], "Stacked: one summed hazard $S$, scaled by $e^{b}$", "summed hazard $e^{b} S$")
for row, b in enumerate((1.0, 0.0, -1.0)):
    left = 0.0
    for v, col in zip(lam_A * np.exp(b), SEG_C):
        axs[1].barh(row, v, left=left, color=col, height=0.6, edgecolor=SURF, lw=0.8)
        left += v
    axs[1].text(left + 0.04, row, f"risk of plaque anywhere\n$1-e^{{-{left:.2f}}}$ = {1 - np.exp(-left):.3f}",
                va="center", fontsize=7.5, color=INK)
axs[1].set_yticks([0, 1, 2], ["$b=+1$\n(×2.72)", "$b=0$\n(×1)", "$b=-1$\n(×0.37)"])
axs[1].set_xlim(0, 3.1)
for lab, col in zip(("LAD", "LCx", "RCA"), C):
    axs[1].barh(-5, 0, color=col, label=lab)
axs[1].set_ylim(-0.6, 2.6)
axs[1].legend(frameon=False, fontsize=8, loc="lower right", ncol=3)
save(fig, "c4_hazards_add")

# ------------------------------------------------------------ F5. averaging over the unknown b
fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.5), facecolor=SURF, gridspec_kw={"width_ratios": [1.3, 1]})
bb = np.linspace(-3.5, 3.5, 400)
ax = axs[0]
style(ax, "Person A: risk for each possible $b$, and how likely each $b$ is", "person effect $b$",
      "person risk")
ax.plot(bb, 1 - np.exp(-np.exp(bb) * S_A), color=C[0], lw=2.2, label="risk $1-\\exp(-e^{b} S_A)$")
dens = norm.pdf(bb, 0, SIGMA)
ax.fill_between(bb, 0, dens / dens.max() * 0.35, color=MUTED, alpha=0.3,
                label=f"spread of $b$: $N(0, {SIGMA}^2)$ (scaled)")
ax.axhline(P["A"], color=C[2], lw=1.8, label=f"average over $b$ = {P['A']:.3f}")
ax.plot(0, B0["A"], "o", color=C[1], ms=6, zorder=3)
ax.annotate(f"$b=0$: {B0['A']:.3f}", (0, B0["A"]), xytext=(10, -14), textcoords="offset points",
            fontsize=8, color=C[1])
ax.set_ylim(0, 1.02)
ax.legend(frameon=False, fontsize=7.5, loc="upper left")
ax = axs[1]
style(ax, "Three made-up people: correct risk and two shortcuts", None, "person risk")
names = list(PEOPLE)
x = np.arange(len(names))
for k, (vals, lab, col) in enumerate(((P, "average over $b$ (used)", C[2]), (B0, "$b$ set to 0", C[0]),
                                      (PROD, "product of segment risks", C[1]))):
    ax.bar(x + (k - 1) * 0.26, [vals[n] for n in names], width=0.26, color=col, label=lab)
ax.set_xticks(x, [f"person {n}" for n in names])
ax.set_ylim(0, 1)
ax.legend(frameon=False, fontsize=7.5, loc="upper left")
save(fig, "c5_average_over_b")

# ------------------------------------------------------------ R2, R3. half-width versions for the one-page note
fig, ax = plt.subplots(figsize=(5.2, 3.4), facecolor=SURF)
style(ax, "Toy person A: nine hazards summed, scaled by $e^{b}$", "summed hazard $e^{b} S$")
for row, b in enumerate((1.0, 0.0, -1.0)):
    left = 0.0
    for v, col in zip(lam_A * np.exp(b), SEG_C):
        ax.barh(row, v, left=left, color=col, height=0.6, edgecolor=SURF, lw=0.8)
        left += v
    ax.text(left + 0.05, row, f"risk {1 - np.exp(-left):.3f}", va="center", fontsize=8, color=INK)
ax.set_yticks([0, 1, 2], ["$b=+1$", "$b=0$", "$b=-1$"])
for lab, col in zip(("LAD", "LCx", "RCA"), C):
    ax.barh(-5, 0, color=col, label=lab)
ax.set_xlim(0, 2.75)
ax.set_ylim(-0.6, 2.6)
ax.legend(frameon=False, fontsize=8, loc="lower right", ncol=3)
save(fig, "r2_hazards_add")

fig, ax = plt.subplots(figsize=(5.2, 3.4), facecolor=SURF)
style(ax, "Toy person A: person risk over the unknown $b$", "person effect $b$", "person risk")
ax.plot(bb, 1 - np.exp(-np.exp(bb) * S_A), color=C[0], lw=2.2, label="risk for a given $b$")
ax.fill_between(bb, 0, dens / dens.max() * 0.35, color=MUTED, alpha=0.3, label="spread of $b$ (scaled)")
ax.axhline(P["A"], color=C[2], lw=1.8, label=f"average over $b$: {P['A']:.3f}")
ax.plot(0, B0["A"], "o", color=C[1], ms=6, zorder=3)
ax.annotate(f"$b=0$: {B0['A']:.3f}", (0, B0["A"]), xytext=(10, -14), textcoords="offset points",
            fontsize=8, color=C[1])
ax.set_ylim(0, 1.02)
ax.legend(frameon=False, fontsize=7.5, loc="upper left")
save(fig, "r3_average_over_b")
print(f"7 figures in {OUT}")
