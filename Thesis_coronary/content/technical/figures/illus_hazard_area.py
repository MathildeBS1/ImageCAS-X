"""Illustration: three hazard shapes with the same area A on [0, T].
The shape of h(t) (and the path of H(t)) is not identified from the data;
only the area H(T) = A is, which gives P(T_event <= T) = 1 - exp(-A).
Made-up curves. Colours from figure_colours.py (scheme "caroline")."""
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


W, H = 6.3, 3.4
fig = plt.figure(figsize=(W, H))
L, R, GAP = 0.015, 0.985, 0.02
pw = (R - L - 2 * GAP) / 3
PB, PT = 0.015, 0.985
bg = fig.add_axes([0, 0, 1, 1], zorder=-5)
bg.set_axis_off(); bg.set_xlim(0, 1); bg.set_ylim(0, 1)

AX = dict(arrowstyle="-|>,head_length=0.55,head_width=0.16", lw=0.6,
          color=C["text"], shrinkA=0, shrinkB=0)
DASH = (0, (3, 2.5))


def bare(ax):
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.patch.set_alpha(0)
    ax.annotate("", xy=(1, 0), xytext=(0, 0), xycoords="axes fraction", arrowprops=AX)
    ax.annotate("", xy=(0, 1), xytext=(0, 0), xycoords="axes fraction", arrowprops=AX)
    ax.text(1.0, -0.05, r"$t$", transform=ax.transAxes, ha="center", va="top")


def guide(ax, xs, ys):
    ax.plot(xs, ys, ls=DASH, lw=0.6, color=C["text2"], zorder=1)


T, A = 1.0, 0.45                                  # horizon and common area
t = np.linspace(0, 1.12 * T, 450)              # curves run a little past T
shapes = [
    0.12 + 1.6 * np.exp(-4.0 * t),                                                 # decreasing
    0.05 + np.exp(-((t - 0.40) / 0.22) ** 2),                                      # single peak
    0.20 + 0.55 * np.exp(-((t - 0.15) / 0.08) ** 2)
         + 0.80 * np.exp(-((t - 0.52) / 0.10) ** 2)
         + 0.45 * np.exp(-((t - 0.85) / 0.06) ** 2),                               # several peaks
]


def cumint(y):
    return np.concatenate([[0], np.cumsum((y[1:] + y[:-1]) / 2 * np.diff(t))])




def darken(hex_, a=0.3):
    c = np.array(to_rgb(hex_))
    return tuple((1 - a) * c + a * np.array(to_rgb(C["text"])))


inT = t <= T
hz = [s * A / cumint(s)[inT][-1] for s in shapes]   # rescale: area on [0, T] equals A
hmax = 1.12 * max(h.max() for h in hz)
XMAX, HMAX = 1.25 * T, 1.32 * A
worlds = [  # (line, fill, panel colour)
    (C["main"], C["fill_main"], C["main"]),
    (darken(C["second"]), C["fill_second"], C["second"]),
    (C["third"], tint(C["third"], 0.28), C["third"]),
]
TOP = (0.565, 0.37)                                 # axes bottom, height (figure fraction)
BOT = (0.095, 0.34)

for k, (h, (col, fill, pc)) in enumerate(zip(hz, worlds)):
    x0 = L + k * (pw + GAP)
    bg.add_patch(FancyBboxPatch((x0, PB), pw, PT - PB, transform=fig.transFigure,
                 boxstyle="round,pad=0,rounding_size=0.02", fc=tint(pc, 0.08),
                 ec=tint(pc, 0.30), lw=0.8, mutation_aspect=W / H))
    axl, axw = x0 + 0.04, pw - 0.04 - 0.045

    # top: hazard; the shape is not observed, the area up to T is shaded
    ax = fig.add_axes([axl, TOP[0], axw, TOP[1]])
    bare(ax); ax.set_xlim(0, XMAX); ax.set_ylim(0, hmax)
    ax.fill_between(t[inT], 0, h[inT], color=fill, lw=0, zorder=0)
    ax.plot(t[inT], h[inT], color=col, lw=1.4, ls=DASH, zorder=3)
    ax.plot(t[~inT], h[~inT], color=col, lw=1.0, ls=DASH, alpha=0.45, zorder=3)
    win = (t > 0.12 * T) & (t < 0.8 * T)            # label at the tallest part of the area
    j = np.flatnonzero(win)[np.argmax(h[win])]
    ax.text(t[j], 0.38 * h[j], r"$A$", ha="center", va="center", fontsize=11)
    ax.text(0.035, 1.0, r"$h(t)$", transform=ax.transAxes, ha="left", va="center")

    # bottom: cumulative hazard; different paths, the same value A at T
    Hc = cumint(h)
    ax = fig.add_axes([axl, BOT[0], axw, BOT[1]])
    bare(ax); ax.set_xlim(0, XMAX); ax.set_ylim(0, HMAX)
    guide(ax, [0, T], [A, A])
    ax.plot(t[inT], Hc[inT], color=col, lw=1.4, ls=DASH, zorder=3)
    ax.plot(t[~inT], Hc[~inT], color=col, lw=1.0, ls=DASH, alpha=0.45, zorder=3)
    ax.plot([T], [A], "o", ms=5, color=col, mec="white", mew=0.9, zorder=5)
    ax.text(T, -0.05 * HMAX, r"$T$", ha="center", va="top")
    ax.text(-0.03 * XMAX, A, r"$A$", ha="right", va="center")
    ax.text(0.035, 1.0, r"$H(t)$", transform=ax.transAxes, ha="left", va="center")

    # one guide at T running through both rows
    xT = axl + axw * T / XMAX
    bg.plot([xT, xT], [BOT[0], TOP[0] + TOP[1] * 0.93], transform=fig.transFigure,
            ls=DASH, lw=0.6, color=C["text2"], zorder=1)

fig.savefig("illus_hazard_area.pdf")
fig.savefig("illus_hazard_area.png", dpi=200)
