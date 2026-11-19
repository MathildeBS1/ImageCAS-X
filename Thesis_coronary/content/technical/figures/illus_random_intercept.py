"""Illustration: from GLM to GLMM. Third panel: P(T_event <= t) = 1 - exp(-H(t)); its value at T is p_i.
 Three people with the same covariates differ only in
their random intercept b_i ~ N(0, sigma_b^2). The intercept shifts eta, multiplies the
hazard by exp(b_i), and so changes how fast the cumulative risk F(t) = 1 - exp(-H(t))
rises. Made-up curves. Colours from figure_colours.py (scheme "caroline")."""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.patches import FancyBboxPatch
from figure_colours import CAROLINE as C

mpl.rcParams.update({
    "font.family": "serif", "font.serif": ["cmr10"],
    "mathtext.fontset": "cm", "axes.unicode_minus": False,
    "font.size": 10, "text.color": C["text"], "pdf.fonttype": 42,
})


def tint(hex_, a):
    c = np.array(to_rgb(hex_))
    return tuple(1 - a * (1 - c))


def darken(hex_, a=0.3):
    c = np.array(to_rgb(hex_))
    return tuple((1 - a) * c + a * np.array(to_rgb(C["text"])))


W, H = 6.3, 2.5
fig = plt.figure(figsize=(W, H))
L, R, GAP = 0.015, 0.985, 0.02
pw = (R - L - 2 * GAP) / 3
PB, PT = 0.015, 0.985
bg = fig.add_axes([0, 0, 1, 1], zorder=-5)
bg.set_axis_off(); bg.set_xlim(0, 1); bg.set_ylim(0, 1)

AX = dict(arrowstyle="-|>,head_length=0.55,head_width=0.16", lw=0.6,
          color=C["text"], shrinkA=0, shrinkB=0)
DASH = (0, (3, 2.5))


def panel(k):
    x0 = L + k * (pw + GAP)
    bg.add_patch(FancyBboxPatch((x0, PB), pw, PT - PB, transform=fig.transFigure,
                 boxstyle="round,pad=0,rounding_size=0.025", fc=tint(C["neutral"], 0.08),
                 ec=tint(C["neutral"], 0.30), lw=0.8, mutation_aspect=W / H))
    return fig.add_axes([x0 + 0.04, 0.12, pw - 0.04 - 0.045, 0.64])


def bare(ax, yaxis=True):
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.patch.set_alpha(0)
    ax.annotate("", xy=(1, 0), xytext=(0, 0), xycoords="axes fraction", arrowprops=AX)
    if yaxis:
        ax.annotate("", xy=(0, 1), xytext=(0, 0), xycoords="axes fraction", arrowprops=AX)


def guide(ax, xs, ys):
    ax.plot(xs, ys, ls=DASH, lw=0.6, color=C["text2"], zorder=1)


# three people, same covariates, different random intercept
sb = 0.6                                       # sd of b_i
bd = 0.95                                      # |b_i| of the low and high person
people = [  # (b_i, colour)
    (-bd, darken(C["second"])),
    (0.0, C["neutral"]),
    (+bd, C["main"]),
]

# ---------- 1: linear predictor and the distribution of b_i ----------
ax = panel(0)
bare(ax, yaxis=False)
ax.set_xlim(-2.6, 2.6); ax.set_ylim(0, 1.25)
e = np.linspace(-2.4, 2.4, 300)
d = np.exp(-e ** 2 / (2 * sb ** 2))
ax.fill_between(e, 0, d, color=tint(C["neutral"], 0.22), lw=0)
ax.plot(e, d, color=C["neutral"], lw=1.1)
for b, col in people:
    yb = np.exp(-b ** 2 / (2 * sb ** 2))
    guide(ax, [b, b], [0, yb]); guide(ax, [b, b], [yb, 1.1]) if b == bd else None
    ax.plot([b], [0], "o", ms=5, color=col, mec="white", mew=0.9, zorder=5, clip_on=False)
# b_i as the shift away from the fixed part
ax.annotate("", xy=(bd, 1.1), xytext=(0, 1.1),
            arrowprops=dict(AX, color=C["main"], lw=0.8))
ax.text(bd / 2, 1.14, r"$b_i$", ha="center", va="bottom")
ax.text(0, -0.06, r"$\beta_0 + \sum_k \beta_k x_{ik}$".replace(r"\sum", r"{\sum}"),
        ha="center", va="top", fontsize=9)
ax.text(2.6, -0.06, r"$\eta$", ha="center", va="top")

# ---------- 2: hazards, the same shape scaled by exp(b_i) ----------
ax = panel(1)
bare(ax)
T = 1.0
t = np.linspace(0, 1.12 * T, 400)
h0 = 0.35 + 0.9 * t ** 1.6                     # reference hazard shape (made up)
hmax = 1.12 * np.exp(bd) * h0.max()
ax.set_xlim(0, 1.22 * T); ax.set_ylim(0, hmax)
for b, col in people:
    ax.plot(t, np.exp(b) * h0, color=col, lw=1.5, zorder=3)
ax.text(0.035, 1.0, r"$h(t)$", transform=ax.transAxes, ha="left", va="center")
ax.text(1.0, -0.05, r"$t$", transform=ax.transAxes, ha="center", va="top")

# ---------- 3: cumulative risk F(t) = 1 - exp(-H(t)) ----------
ax = panel(2)
bare(ax)
ax.set_xlim(0, 1.22 * T); ax.set_ylim(0, 1.18)
H0 = 0.35 * t + 0.9 * t ** 2.6 / 2.6
H0 *= 0.7 / np.interp(T, t, H0)                # reference: H(T) = 0.7, F(T) about 0.5
guide(ax, [0, 1.18 * T], [1, 1])
guide(ax, [T, T], [0, 1.08])
for b, col in people:
    F = 1 - np.exp(-np.exp(b) * H0)
    ax.plot(t, F, color=col, lw=1.5, zorder=3)
    ax.plot([T], [np.interp(T, t, F)], "o", ms=5, color=col, mec="white", mew=0.9, zorder=5)
ax.text(-0.03 * 1.22 * T, 1, r"$1$", ha="right", va="center")
ax.text(T, -0.05 * 1.18, r"$T$", ha="center", va="top")
yhi = 1 - np.exp(-np.exp(bd) * np.interp(T, t, H0))       # the high person's value at T
guide(ax, [0, T], [yhi, yhi])
ax.text(-0.03 * 1.22 * T, yhi, r"$p_i$", ha="right", va="center")

ax.text(1.0, -0.05, r"$t$", transform=ax.transAxes, ha="center", va="top")

# formulas in a band above the axes
FY = PT - 0.085
forms = [r"$\eta_i = \beta_0 + {\sum}_k\, \beta_k x_{ik} + b_i$",
         r"$h_i(t) = h_0(t)\,\exp(\eta_i)$",
         r"$p_i = 1-\exp\{-H_i(T)\}$"]
for k, f in enumerate(forms):
    fig.text(L + k * (pw + GAP) + pw / 2, FY, f, ha="center", va="center",
             fontsize=9.5, linespacing=1.5)

fig.savefig("illus_random_intercept.pdf")
fig.savefig("illus_random_intercept.png", dpi=200)
