"""Illustration: the variance of the random intercept is estimated in the training data,
where segments cluster within people. For a new person b is never observed, so the
person risk is averaged over b ~ N(0, sigma_b^2). Made-up data.
Colours from figure_colours.py (scheme "caroline")."""
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
AX2 = dict(AX, arrowstyle="<|-|>,head_length=0.45,head_width=0.14")
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


sb = 0.9                                         # sigma_b used for the made-up data
rng = np.random.default_rng(11)

# ---------- 1: training data, 9 segments per person, clustered within people ----------
ax = panel(0)
bare(ax)
n_p, n_s = 13, 9
b = np.sort(rng.normal(0, sb, n_p))       # sorted so the clustering is visible
eta = -1.5 + rng.normal(0, 0.25, (n_s, 1))       # segment intercepts (made up)
p = 1 - np.exp(-np.exp(eta + b[None, :]))
y = rng.uniform(size=p.shape) < p
ax.set_xlim(0, n_p + 1); ax.set_ylim(0, n_s + 1)
ii, jj = np.meshgrid(np.arange(1, n_p + 1), np.arange(1, n_s + 1))
ax.scatter(ii[~y], jj[~y], s=13, facecolor="white", edgecolor=tint(C["neutral"], 0.7), lw=0.6)
ax.scatter(ii[y], jj[y], s=13, color=C["main"], lw=0)
ax.text(1.0, -0.05, r"$i$", transform=ax.transAxes, ha="center", va="top")
ax.text(-0.04, 1.0, r"$j$", transform=ax.transAxes, ha="right", va="center")

# ---------- 2: estimated distribution of b ----------
ax = panel(1)
bare(ax, yaxis=False)
bb = np.linspace(-2.7, 2.7, 300)
phi = np.exp(-bb ** 2 / (2 * sb ** 2))
ax.set_xlim(-2.8, 2.8); ax.set_ylim(0, 1.3)
ax.fill_between(bb, 0, phi, color=tint(C["neutral"], 0.22), lw=0)
ax.plot(bb, phi, color=C["neutral"], lw=1.2)
yh = np.exp(-0.5)                                # height at +-1 sd
guide(ax, [0, 0], [0, 1.0])
ax.annotate("", xy=(sb, yh), xytext=(0, yh), arrowprops=dict(AX2, color=C["main"], lw=0.8))
ax.text(sb / 2, yh + 0.05, r"$\hat\sigma_b$", ha="center", va="bottom")
ax.text(0, -0.06, r"$0$", ha="center", va="top")
ax.text(2.8, -0.06, r"$b$", ha="center", va="top")

# ---------- 3: new person, b unknown: average the risk over b ----------
ax = panel(2)
bare(ax)
ax.set_xlim(-2.8, 2.8); ax.set_ylim(0, 1.18)
c = np.log(-np.log(1 - 0.30))                    # person risk 0.30 at b = 0 (made up)
pb = 1 - np.exp(-np.exp(c + bb))
w = phi / np.trapezoid(phi, bb)
pbar = np.trapezoid(pb * w, bb)
ax.fill_between(bb, 0, 0.38 * phi, color=tint(C["neutral"], 0.22), lw=0, zorder=0)
ax.plot(bb, 0.38 * phi, color=C["neutral"], lw=1.0, zorder=1)
guide(ax, [-2.8, 2.7], [1, 1])
ax.plot(bb, pb, color=darken(C["second"]), lw=1.5, zorder=3)
guide(ax, [-2.8, 2.7], [pbar, pbar])
ax.text(-2.8 - 0.1, 1, r"$1$", ha="right", va="center")
ax.text(-2.8 - 0.1, pbar, r"$\bar p$", ha="right", va="center")
ax.text(2.8, -0.06, r"$b$", ha="center", va="top")
ax.text(1.4, 1 - np.exp(-np.exp(c + 1.4)) - 0.06, r"$p(b)$", ha="left", va="top",
        color=darken(C["second"]))

# formulas in a band above the axes
FY = PT - 0.085
forms = [r"$y_{ij} \in \{0, 1\}$",
         r"$b \sim N(0, \hat\sigma_b^2)$",
         r"$\bar p = \int\quad p(b)\, \phi(b)\, db$"]
for k, f in enumerate(forms):
    fig.text(L + k * (pw + GAP) + pw / 2, FY, f, ha="center", va="center", fontsize=9.5)

fig.savefig("illus_random_intercept_integration.pdf")
fig.savefig("illus_random_intercept_integration.png", dpi=200)
