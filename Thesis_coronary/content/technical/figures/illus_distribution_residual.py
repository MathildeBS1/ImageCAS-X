"""Illustration: normal vs binary outcome around the same mean line.
Made-up data. Colours from figure_colours.py (scheme "caroline")."""
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.patches import FancyBboxPatch, Rectangle
from figure_colours import CAROLINE as C

# ---------- typography: Computer Modern ----------
FONTDIR = os.path.join(os.path.dirname(mpl.__file__), "mpl-data/fonts/ttf")
mpl.rcParams.update({
    "font.family": "serif", "font.serif": ["cmr10"],
    "mathtext.fontset": "cm", "axes.unicode_minus": False,
    "font.size": 10, "text.color": C["text"], "pdf.fonttype": 42,
})


def tint(hex_, a):
    """Series colour at fraction a on white."""
    c = np.array(to_rgb(hex_))
    return tuple(1 - a * (1 - c))


def darken(hex_, a=0.3):
    c = np.array(to_rgb(hex_))
    return tuple((1 - a) * c + a * np.array(to_rgb(C["text"])))


rng = np.random.default_rng(7)
W = 6.3
H = 2.6
fig = plt.figure(figsize=(W, H))
L, R, GAP = 0.015, 0.985, 0.03
pw = (R - L - GAP) / 2
PB, PT = 0.015, 0.985          # panel box bottom/top (figure fraction)


def panel_box(x0, col):
    ax = fig.add_axes([0, 0, 1, 1], zorder=-5)
    ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.add_patch(FancyBboxPatch((x0, PB), pw, PT - PB, transform=fig.transFigure,
                 boxstyle="round,pad=0,rounding_size=0.02", fc=tint(col, 0.10),
                 ec=tint(col, 0.30), lw=0.8, mutation_aspect=W / H))


def arrow_axes(ax, xlab, ylab):
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.patch.set_alpha(0)
    kw = dict(arrowstyle="-|>,head_length=0.55,head_width=0.16", lw=0.6,
              color=C["text"], shrinkA=0, shrinkB=0, capstyle="butt")
    ax.annotate("", xy=(1, 0), xytext=(0, 0), xycoords="axes fraction", arrowprops=kw)
    ax.annotate("", xy=(0, 1), xytext=(0, 0), xycoords="axes fraction", arrowprops=kw)
    ax.text(1.0, -0.04, xlab, transform=ax.transAxes, ha="center", va="top")
    ax.text(-0.04, 1.0, ylab, transform=ax.transAxes, ha="right", va="center")


def guide(ax, xs, ys):
    ax.plot(xs, ys, ls=(0, (3, 2.5)), lw=0.6, color=C["text2"], zorder=1)


xk = np.array([0.13, 0.42, 0.71])          # three covariate values
x_end = 0.80                               # where data/line stop; glyphs to the right

# ---------- left: normal outcome ----------
col = C["main"]
panel_box(L, col)
ax = fig.add_axes([L + 0.045, PB + 0.08, pw - 0.07, PT - PB - 0.17])
ax.set_xlim(0, 1); ax.set_ylim(-0.08, 1.08)   # same frame as the binary panel
a, b, sd = 0.10, 0.95, 0.045   # same mean line as the binary panel
mu = lambda x: a + b * x
x = rng.uniform(0.02, x_end, 70)
y = mu(x) + rng.normal(0, sd, x.size)
xx = np.linspace(0.02, x_end, 2)
ax.fill_between(xx, mu(xx) - sd, mu(xx) + sd, color=C["fill_main"], lw=0, zorder=0)
ax.scatter(x, y, s=7, color=col, alpha=0.75, lw=0, zorder=2)
ax.plot(xx, mu(xx), color=col, lw=1.5, zorder=3)
xd, wd = 0.86, 0.11                        # density baseline and peak width
zz = np.linspace(-2.6, 2.6, 300)           # densities drawn on the data scale (sd)
for xv in xk:
    m = mu(xv)
    guide(ax, [xv, xv], [-0.08, m]); guide(ax, [xv, xd + wd], [m, m])
    ax.plot([xv], [m], "o", ms=3.0, color=col, zorder=4)
    dens = np.exp(-zz ** 2 / 2)
    ax.fill_betweenx(m + sd * zz, xd, xd + wd * dens, color=C["fill_main"], lw=0, zorder=2)
    ax.plot(xd + wd * dens, m + sd * zz, color=col, lw=1.0, zorder=3)
    ax.plot([xd, xd], [m - sd * 2.6, m + sd * 2.6], color=C["text"], lw=0.6,
            solid_capstyle="butt", zorder=3)
ax.text(xk[2] - 0.012, mu(xk[2]) + 0.03, r"$\mu$", ha="right", va="bottom")
arrow_axes(ax, r"$x$", r"$y$")

# ---------- right: binary outcome ----------
col = C["second"]; dcol = darken(col)
x0r = L + pw + GAP
panel_box(x0r, col)
ax = fig.add_axes([x0r + 0.045, PB + 0.08, pw - 0.07, PT - PB - 0.17])
ax.set_xlim(0, 1); ax.set_ylim(-0.08, 1.08)
p = lambda x: 0.10 + 0.95 * x              # mean = P(y = 1), stays in (0, 1)
x = rng.uniform(0.02, x_end, 70)
y = (rng.uniform(size=x.size) < p(x)).astype(float)
xx = np.linspace(0.02, x_end, 2)
ax.fill_between(xx, p(xx) - 0.05, p(xx) + 0.05, color=C["fill_second"], lw=0, zorder=0)
ax.scatter(x, y, s=7, color=col, alpha=0.85, lw=0, zorder=2)
ax.plot(xx, p(xx), color=dcol, lw=1.5, zorder=3)
cols_x = [0.85, 0.915, 0.98]               # one Bernoulli column per covariate value
for xv, cx in zip(xk, cols_x):
    m = p(xv)
    guide(ax, [xv, xv], [-0.08, m]); guide(ax, [xv, cx], [m, m])
    ax.plot([xv], [m], "o", ms=3.2, color=dcol, zorder=4)
    ax.plot([cx, cx], [0, 1], color=C["text"], lw=0.8)
    for yv, pv in ((1, m), (0, 1 - m)):
        ax.plot([cx], [yv], "o", ms=2 + 7 * np.sqrt(pv), color=col, mec=dcol,
                mew=0.6, zorder=5, clip_on=False)
ax.text(xk[2] - 0.012, p(xk[2]) + 0.03, r"$\mu$", ha="right", va="bottom")
ax.text(-0.04, 0, r"$0$", ha="right", va="center")
ax.text(-0.04, 1, r"$1$", ha="right", va="center")
arrow_axes(ax, r"$x$", r"$y$")

fig.savefig("illus_distribution_residual.pdf")
fig.savefig("illus_distribution_residual.png", dpi=200)
