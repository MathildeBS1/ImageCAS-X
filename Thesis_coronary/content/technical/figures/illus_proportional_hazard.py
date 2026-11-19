"""Illustration: three possible baseline hazards h_0(t) (increasing, decreasing,
non-monotonic). In each, h_A = h_0 exp(beta x_A) and h_B = h_0 exp(beta x_B), so the
ratio h_A/h_B is the same constant. Made-up curves.
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


W, H = 6.3, 3.4
fig = plt.figure(figsize=(W, H))
L, R, GAP = 0.015, 0.985, 0.02
pw = (R - L - 2 * GAP) / 3
PB, PT = 0.015, 0.985
bg = fig.add_axes([0, 0, 1, 1], zorder=-5)
bg.set_axis_off(); bg.set_xlim(0, 1); bg.set_ylim(0, 1)

AX = dict(arrowstyle="-|>,head_length=0.55,head_width=0.16", lw=0.6,
          color=C["text"], shrinkA=0, shrinkB=0)


def bare(ax):
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.patch.set_alpha(0)
    ax.annotate("", xy=(1, 0), xytext=(0, 0), xycoords="axes fraction", arrowprops=AX)
    ax.annotate("", xy=(0, 1), xytext=(0, 0), xycoords="axes fraction", arrowprops=AX)
    ax.text(1.0, -0.05, r"$t$", transform=ax.transAxes, ha="center", va="top")


# three possible baseline hazards on t in [0, 1]
t = np.linspace(0, 1, 300)
worlds = [
    0.10 + 0.20 * (np.exp(2.2 * t) - 1) / (np.exp(2.2) - 1) * 1.6,                 # increasing
    0.10 + 0.42 * np.exp(-4.5 * t),                                                # decreasing
    0.14 + 0.26 * np.exp(-((t - 0.25) / 0.13) ** 2) + 0.10 * np.exp(-((t - 0.72) / 0.13) ** 2),
]
rA, rB = 2.0, 1.45            # exp(beta x_A), exp(beta x_B): same in every world
hA_col, hB_col, h0_col = C["main"], darken(C["second"]), C["neutral"]
ratio_col = C["third"]

for k, h0 in enumerate(worlds):
    x0 = L + k * (pw + GAP)
    bg.add_patch(FancyBboxPatch((x0, PB), pw, PT - PB, transform=fig.transFigure,
                 boxstyle="round,pad=0,rounding_size=0.02", fc=tint(C["neutral"], 0.08),
                 ec=tint(C["neutral"], 0.30), lw=0.8, mutation_aspect=W / H))
    axl = x0 + 0.03; axw = pw - 0.03 - 0.05

    # top: hazards over time
    ax = fig.add_axes([axl, 0.44, axw, 0.50])
    bare(ax); ax.set_xlim(0, 1.0); ax.set_ylim(0, 1.15)
    ax.plot(t, h0, color=h0_col, lw=1.1, ls=(0, (3, 2.5)))
    ax.plot(t, rB * h0, color=hB_col, lw=1.5)
    ax.plot(t, rA * h0, color=hA_col, lw=1.5)
    for y, s, c in [] if k else ((rA * h0[-1], r"$h_A$", hA_col), (rB * h0[-1], r"$h_B$", hB_col),
                    (h0[-1], r"$h_0$", h0_col)):
        ax.text(1.03, y, s, color=c if c != h0_col else C["text2"], ha="left", va="center")
    if k == 0:
        ax.text(0.04, 1.0, r"$h(t)$", transform=ax.transAxes, ha="left", va="center")

    # bottom: the ratio, constant in time
    ax = fig.add_axes([axl, 0.08, axw, 0.25])
    bare(ax); ax.set_xlim(0, 1.0); ax.set_ylim(0, 1.0)
    ax.plot([0, 0.97], [0.55, 0.55], color=ratio_col, lw=1.5)
    if k == 0:
        ax.text(0.04, 1.0, r"$h_A/h_B$", transform=ax.transAxes, ha="left", va="center")

fig.savefig("illus_proportional_hazard.pdf")
fig.savefig("illus_proportional_hazard.png", dpi=200)
