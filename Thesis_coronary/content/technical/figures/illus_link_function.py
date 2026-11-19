"""Illustration: linear predictor eta (unbounded) -> mean mu = g^{-1}(eta) in (0, 1),
with the cloglog inverse link mu = 1 - exp(-exp(eta)).
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


W, H = 6.3, 3.0
fig = plt.figure(figsize=(W, H))
L, R, GAP = 0.015, 0.985, 0.13             # wide gap holds the g^{-1} arrow
pw = (R - L - GAP) / 2
PB, PT = 0.015, 0.985
bg = fig.add_axes([0, 0, 1, 1], zorder=-5)
bg.set_axis_off(); bg.set_xlim(0, 1); bg.set_ylim(0, 1)


def panel_box(x0, col):
    bg.add_patch(FancyBboxPatch((x0, PB), pw, PT - PB, transform=fig.transFigure,
                 boxstyle="round,pad=0,rounding_size=0.02", fc=tint(col, 0.10),
                 ec=tint(col, 0.30), lw=0.8, mutation_aspect=W / H))


AX = dict(arrowstyle="-|>,head_length=0.55,head_width=0.16", lw=0.6,
          color=C["text"], shrinkA=0, shrinkB=0)
AX2 = dict(AX, arrowstyle="<|-|>,head_length=0.55,head_width=0.16")


def bare(ax):
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.patch.set_alpha(0)


def arrow(ax, p0, p1, both=False):
    ax.annotate("", xy=p1, xytext=p0, xycoords="axes fraction",
                arrowprops=AX2 if both else AX)


def guide(ax, xs, ys):
    ax.plot(xs, ys, ls=(0, (3, 2.5)), lw=0.6, color=C["text2"], zorder=1)


AXB, AXH = PB + 0.075, PT - PB - 0.255     # axes bottom/height (room for formula on top)
FY = PT - 0.075                            # formula baseline


def put(ax, x, y, s, **kw):
    ax.text(x, y, s, transform=ax.transAxes, **kw)


# ---------- left: linear predictor, unbounded ----------
col = C["main"]
panel_box(L, col)
fig.text(L + pw / 2, FY, r"$\eta_i = \beta_0 + {\sum}_{k}\, \beta_k\, x_{ik}$",
         ha="center", va="center", fontsize=11)
ax = fig.add_axes([L + 0.05, AXB, pw - 0.075, AXH])
bare(ax); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
arrow(ax, (0, 0), (0, 1), both=True)                 # eta axis: unbounded
arrow(ax, (0, 0.5), (1, 0.5))                        # covariate axis at eta = 0
line = lambda x: 0.5 + 0.95 * (x - 0.45)
xx = np.array([0.03, 0.92])
ax.plot(xx, line(xx), color=col, lw=1.5, zorder=3)
xi = 0.66; ei = line(xi)
guide(ax, [xi, xi], [0.5, ei]); guide(ax, [0, xi], [ei, ei])
ax.plot([xi], [ei], "o", ms=3.2, color=col, zorder=4)
put(ax, -0.04, 1.0, r"$\eta$", ha="right", va="center")
put(ax, 0.035, 0.95, r"$\infty$", ha="left", va="center")
put(ax, 0.035, 0.05, r"$-\infty$", ha="left", va="center")
put(ax, -0.04, ei, r"$\eta_i$", ha="right", va="center")
put(ax, xi, 0.47, r"$x_{ik}$", ha="center", va="top")

# ---------- centre: inverse link ----------
xa0, xa1 = L + pw + 0.015, L + pw + GAP - 0.015
ya = AXB + AXH / 2
bg.annotate("", xy=(xa1, ya), xytext=(xa0, ya), xycoords="figure fraction",
            arrowprops=dict(AX, lw=0.8))
fig.text((xa0 + xa1) / 2, ya + 0.03, r"$g^{-1}$", ha="center", va="bottom", fontsize=11)

# ---------- right: mean, bounded in (0, 1) ----------
col = C["second"]; dcol = darken(col)
x0r = L + pw + GAP
panel_box(x0r, col)
fig.text(x0r + pw / 2, FY, r"$p_i = g^{-1}\!\left(\beta_0 + {\sum}_{k}\, \beta_k\, x_{ik}\right)$",
         ha="center", va="center", fontsize=11)
ax = fig.add_axes([x0r + 0.05, AXB, pw - 0.075, AXH])
bare(ax)
e0, e1 = -4.6, 2.2
ax.set_xlim(e0, e1); ax.set_ylim(-0.08, 1.08)
arrow(ax, (0, 0), (0, 1))
arrow(ax, (0, 0), (1, 0))
for yv in (0, 1):
    guide(ax, [e0, e1], [yv, yv])
cl = lambda e: 1 - np.exp(-np.exp(e))
eta = np.linspace(e0 + 0.08, e1 - 0.05, 400)
ax.plot(eta, cl(eta), color=dcol, lw=1.5, zorder=3)
eti = 0.0; mi = cl(eti)                              # the same eta_i, carried across
guide(ax, [eti, eti], [-0.08, mi]); guide(ax, [e0, eti], [mi, mi])
ax.plot([eti], [mi], "o", ms=3.2, color=dcol, zorder=4)
fx = lambda e: (e - e0) / (e1 - e0)
fy = lambda m: (m + 0.08) / 1.16
put(ax, -0.04, 1.0, r"$p$", ha="right", va="center")
put(ax, -0.04, fy(0), r"$0$", ha="right", va="center")
put(ax, -0.04, fy(1), r"$1$", ha="right", va="center")
put(ax, -0.04, fy(mi), r"$p_i$", ha="right", va="center")
put(ax, 0.015, -0.04, r"$-\infty$", ha="left", va="top")
put(ax, 0.985, -0.04, r"$\infty$", ha="right", va="top")
put(ax, fx(eti), -0.04, r"$\eta_i$", ha="center", va="top")
put(ax, 0.35, -0.04, r"$\eta$", ha="center", va="top")

fig.savefig("illus_link_function.pdf")
fig.savefig("illus_link_function.png", dpi=200)
