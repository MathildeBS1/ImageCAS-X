"""Five figures explaining `transformer_model.ProfileTransformer`, one stage each, in the visual
language of Griffo et al. (Comput Biol Med 2026, Figs. 1 and 3): the vessel drawn as a shaded
tube with mesh nodes and a rainbow map along it (here the turning per mm), layers as slanted
parallelograms, pooling in pink and copies in grey. Features are stacks of beads, blue because
they belong to the network, while the rainbow stays on geometry.

The overview follows Aida Jimenez's U-Net figure (sizes above each stage); the others work one
operation through on real numbers. Every number is computed here from one small example, so the
figures agree. The example is illustrative: 4 channels where the model uses `HP["d_model"]`, one
attention head where it uses `HP["nhead"]`, random weights, a vessel bent only schematically.

    python -m tortuosity.figure_transformer

Writes figures/transformer_{1_overview,2_tokens,3_attention,4_encoder,5_readout}.{pdf,png}.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PolyCollection
from matplotlib.colors import ListedColormap
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Polygon, Wedge
from scipy.interpolate import CubicSpline, PchipInterpolator

from . import paths
from .figure_turning_angle import HIGH, INK, LOW, MUTED, save
from .transformer_model import HP

W, D = HP["window"], 4
PURPLE, PINK, GREY, LAYER = "#7b4fc4", "#e07bb5", "#9aa3ad", "#e6dcf7"
BLUES, TURBO = plt.get_cmap("Blues"), plt.get_cmap("turbo")
RAINBOW = ListedColormap(TURBO(np.linspace(0.12, 0.92, 64)))
CAP = dict(ha="center", va="center", fontsize=6.5, color=INK, linespacing=1.3)
TH = np.array([.12, .31, .08, .18, .05, .22])  # the six turning-per-mm values of Fig. 2
SIGN = np.array([1, -1, 1, 1, -1, 1])


def ln(a):
    return (a - a.mean(-1, keepdims=True)) / np.sqrt(a.var(-1, keepdims=True) + 1e-5)


def example():
    """One small forward pass through the same operations as the model, kept for every figure."""
    r = np.random.default_rng(3)
    e = dict(E=r.normal(0, 1, (10, D)))  # ten embedded tokens, the last two padding
    Wq, Wk, Wv, Wo = r.normal(0, .7, (4, D, D))
    H = ln(e["E"])
    Q, K, V = H @ Wq, H @ Wk, H @ Wv
    q, ks = 4, np.arange(4 - W, 4 + W + 1)
    e["score"] = Q[q] @ K[ks].T / np.sqrt(D)
    e["weight"] = np.exp(e["score"]) / np.exp(e["score"]).sum()
    e["V"], e["o"] = V[ks], e["weight"] @ V[ks]
    e["x"], e["ln_x"] = e["E"][q], H[q]
    e["a"] = e["o"] @ Wo
    e["x1"] = e["x"] + e["a"]
    e["ln_x1"] = ln(e["x1"])
    W1, W2 = r.normal(0, .7, (D, 2 * D)), r.normal(0, .7, (2 * D, D))
    e["f"] = np.maximum(e["ln_x1"] @ W1, 0) @ W2
    e["y"] = e["x1"] + e["f"]
    e["Y"] = r.normal(0, 1, (4, D))  # the real tokens leaving the last encoder layer
    e["mean"] = e["Y"].mean(0)
    e["len"] = 0.62
    e["vec"] = np.r_[e["mean"], e["len"]]
    e["w"], e["b"] = r.normal(0, .8, D + 1), 0.1
    e["logit"] = e["vec"] @ e["w"] + e["b"]
    e["p"] = 1 / (1 + np.exp(-e["logit"]))
    return e


def canvas(h, ymin=0, w=7.4):
    fig, ax = plt.subplots(figsize=(w, w * (h - ymin) / 100))
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_xlim(0, 100), ax.set_ylim(ymin, h), ax.axis("off")
    return fig, ax


def arrow(ax, p, q, color=INK, lw=1.0, style="-|>", **kw):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=7, lw=lw, color=color, **kw))


def elbow(ax, pts, color=GREY, lw=1.4):
    ax.plot(*np.array(pts[:-1]).T, color=color, lw=lw, solid_capstyle="round")
    arrow(ax, pts[-2], pts[-1], color, lw)


def chain(turns, ell=1.0):
    """Vertices of a polyline whose consecutive chords have length ell and turn by `turns`."""
    ang, p, pts = 0.0, np.zeros(2), [np.zeros(2)]
    for k in range(len(turns) + 1):
        ang += turns[k - 1] if k else 0
        p = p + ell * np.array([np.cos(ang), np.sin(ang)])
        pts.append(p)
    return np.array(pts)


def fit(P, x0, x1, yc):
    s = (x1 - x0) / np.ptp(P[:, 0])
    return (P - [P[:, 0].min(), P[:, 1].mean()]) * s + [x0, yc]


def tube(ax, P, vals=None, r=2.0, K=7, alpha=1.0, taper=(1.0, .8), mesh=True):
    """Shaded tube along a spline through P, as Griffo's surface meshes. `vals` in 0..1 per vertex
    colours it with the rainbow; without it the tube is grey. Rings and edge nodes mark the vertices."""
    cs = CubicSpline(np.arange(len(P)), P, bc_type="natural")
    t = np.linspace(0, len(P) - 1, 260)
    Q, T = cs(t), cs(t, 1)
    N = np.c_[-T[:, 1], T[:, 0]] / np.linalg.norm(T, axis=1)[:, None]
    R = r * np.linspace(*taper, len(t))
    base = np.tile([.8, .82, .85], (len(t), 1)) if vals is None else TURBO(.12 + .8 * PchipInterpolator(np.arange(len(P)), vals)(t))[:, :3]
    polys, cols = [], []
    for k in range(K):
        u0, u1 = -1 + 2 * k / K, -1 + 2 * (k + 1) / K
        sh = .6 + .5 * np.cos((u0 + u1) / 2 * np.pi / 2)
        a, b = Q + u0 * R[:, None] * N, Q + u1 * R[:, None] * N
        polys += [np.array([a[i], a[i + 1], b[i + 1], b[i]]) for i in range(len(t) - 1)]
        c = np.clip(base * sh + .22 * max(0, sh - 1), 0, 1)
        cols += list(c[:-1])
    ax.add_collection(PolyCollection(polys, facecolors=cols, edgecolors=cols, linewidths=.4, alpha=alpha, zorder=2))
    if mesh:
        Tv = cs(np.arange(len(P)), 1)
        Nv = np.c_[-Tv[:, 1], Tv[:, 0]] / np.linalg.norm(Tv, axis=1)[:, None]
        Rv = r * np.interp(np.arange(len(P)), t, np.linspace(*taper, len(t)))
        for p, n, rv in zip(P, Nv, Rv):
            ax.plot(*np.array([p - rv * n, p + rv * n]).T, color="#3b4650", lw=.4, alpha=.55, zorder=3)
            ax.scatter(*np.array([p - rv * n, p, p + rv * n]).T, s=2.2, color="#1f2933", zorder=4)
    return cs


def node(ax, x, y, label="", fc="white", ec=INK, r=1.3, fs=5, ls="-"):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=ec, lw=.9, ls=ls, zorder=6))
    ax.text(x, y, label, ha="center", va="center", fontsize=fs, color=INK, zorder=7)


def beads(ax, x, yc, vals, ghost=False, ec=None, r=1.55, step=3.4, fs=4.4, cmap=BLUES, lim=3.0, numbers=True):
    """A vertical stack of beads, one per channel; shade is the value, number inside."""
    ys = yc + (len(vals) - 1) / 2 * step - np.arange(len(vals)) * step
    for v, y in zip(vals, ys):
        if ghost:
            ax.add_patch(Circle((x, y), r, fc="none", ec=GREY, lw=.8, ls=(0, (2, 1.5))))
            continue
        ax.add_patch(Circle((x, y), r, fc=cmap(.1 + .42 * (np.clip(v, -lim, lim) + lim) / (2 * lim)), ec=ec or "white", lw=1.2 if ec else .6, zorder=3))
        if numbers:
            ax.text(x, y, f"{v:.2f}", ha="center", va="center", fontsize=fs, color=INK, zorder=4)
    return ys


def para(ax, x, y, w, h, skew=1.6, fc=LAYER, ec=PURPLE):
    ax.add_patch(Polygon([(x, y), (x + w, y + skew), (x + w, y + h + skew), (x, y + h)], fc=fc, ec=ec, lw=1.0, zorder=3))


def gauge(ax, cx, cy, r, p):
    for i in range(90):
        ax.add_patch(Wedge((cx, cy), r, 180 * (1 - (i + 1) / 90), 180 * (1 - i / 90), width=.38 * r, fc=TURBO(.1 + .85 * i / 90), ec="none"))
    a = np.pi * (1 - p)
    ax.plot([cx, cx + .88 * r * np.cos(a)], [cy, cy + .88 * r * np.sin(a)], color=INK, lw=1.8, solid_capstyle="round")
    ax.add_patch(Circle((cx, cy), .09 * r, fc=INK))
    ax.text(cx - .8 * r, cy - 1.6, "0", fontsize=5.5, ha="center", color=MUTED), ax.text(cx + .8 * r, cy - 1.6, "1", fontsize=5.5, ha="center", color=MUTED)


def colourbar(ax, x0, x1, y, lab):
    ax.imshow(np.linspace(0, 1, 64)[None], cmap=RAINBOW, extent=(x0, x1, y, y + 1.4), aspect="auto", zorder=1)
    ax.text(x0, y - 1.7, "low", fontsize=5.4, ha="center", color=MUTED), ax.text(x1, y - 1.7, "high", fontsize=5.4, ha="center", color=MUTED)
    ax.text((x0 + x1) / 2, y + 3.0, lab, fontsize=5.8, ha="center", color=INK)


def vessel(x0, x1, yc):
    """The Fig. 2 vessel: vertices, normalised turning for the rainbow, fitted into [x0, x1]."""
    P = fit(chain(SIGN * TH * 5 * .45), x0, x1, yc)
    v = (TH - TH.min()) / np.ptp(TH)
    return P, np.r_[v[0], v, v[-1]]


def overview():
    fig, ax = canvas(46, -2)
    ax.text(50, 44, "ProfileTransformer", **CAP)
    ytop = 33
    stages = [(2, 14, "T x 2"), (26, 40, f"T x {HP['d_model']}"), (58, 72, f"T x {HP['d_model']}")]
    for k, (x0, x1, lab) in enumerate(stages):
        P, v = vessel(x0, x1, ytop)
        tube(ax, P, v if k == 0 else None, r=1.5, alpha=1 if k == 0 else .55)
        for j, p in enumerate(P[1:7]):
            if k == 0:
                node(ax, *p, r=.8, fc=TURBO(.12 + .8 * v[j + 1]))
            else:
                beads(ax, p[0], p[1], np.array([-2, 0, 2.2]) * (1 if j % 2 else -1) + j * .3, r=.75, step=1.7, numbers=False)
        ax.text((x0 + x1) / 2, ytop + 8, lab, **CAP)
        ax.text((x0 + x1) / 2, ytop - 7, ["tokens, coloured by turning", "embedded tokens", "after 2 encoder layers"][k], fontsize=5.8, ha="center", color=MUTED)
    para(ax, 18, ytop - 5, 3.2, 10, fc=LAYER), ax.text(19.6, ytop - 9, "linear", fontsize=5.8, ha="center", color=PURPLE)
    arrow(ax, (15.4, ytop), (17.6, ytop), GREY, 1.6), arrow(ax, (21.6, ytop + .8), (25, ytop + .8), GREY, 1.6)
    for x in (44, 51):
        para(ax, x, ytop - 5, 3.2, 10, fc="#cfe0f7", ec=HIGH)
    ax.text(48.5, ytop - 9, "encoder layers 1, 2", fontsize=5.8, ha="center", color=HIGH)
    arrow(ax, (41.4, ytop), (43.6, ytop), GREY, 1.6), arrow(ax, (47.4, ytop + .8), (50.6, ytop + .8), GREY, 1.6), arrow(ax, (55, ytop + .8), (57.4, ytop + .8), GREY, 1.6)
    ax.plot([74, 80, 80, 3, 3, 6], [ytop, ytop, 21.5, 21.5, 11.5, 11.5], color=GREY, lw=1.4, solid_capstyle="round")

    y2 = 11.5
    arrow(ax, (6, y2), (16.5, y2), PINK, 2.4)
    ax.text(11.3, y2 + 3, "mean over the real tokens", fontsize=5.8, ha="center", color=PINK)
    beads(ax, 20, y2, np.zeros(4), numbers=False, r=1.45, step=3.1)
    ax.text(20, y2 - 9, f"{HP['d_model']}", **CAP)
    arrow(ax, (23, y2), (30, y2), GREY, 2.0)
    ax.text(26.5, y2 + 3, "append length", fontsize=5.8, ha="center", color=LOW)
    ys = beads(ax, 33, y2, np.zeros(5), numbers=False, r=1.45, step=3.1)
    ax.add_patch(Circle((33, ys[-1]), 1.45, fc="#fde3d3", ec=LOW, lw=1.2, zorder=4))
    ax.text(33, y2 - 10, f"{HP['d_model'] + 1}", **CAP)
    arrow(ax, (36, y2), (42, y2), GREY, 1.6)
    para(ax, 43, y2 - 5, 3.2, 10), ax.text(44.6, y2 - 9.5, "linear, sigmoid", fontsize=5.8, ha="center", color=PURPLE)
    arrow(ax, (47.4, y2 + .8), (52.5, y2 + .8), GREY, 1.6)
    gauge(ax, 62, y2 - 3, 8.5, .64)
    ax.text(62, y2 - 9.5, "P(Disease)", **CAP)

    ax.add_patch(Polygon([(72, 3), (99, 3), (99, 20), (72, 20)], fc="white", ec=MUTED, lw=.8))
    for i, (kind, lab) in enumerate([("p", "linear layer"), ("b", "encoder layer: attention,\nfeed-forward, skips"), ("g", "copy or append"), ("k", "mean pooling")]):
        y = 17 - i * 3.9
        if kind == "p":
            para(ax, 74, y - 1.3, 3, 2.2, 1)
        elif kind == "b":
            para(ax, 74, y - 1.3, 3, 2.2, 1, fc="#cfe0f7", ec=HIGH)
        else:
            arrow(ax, (73.5, y), (78.5, y), GREY if kind == "g" else PINK, 2.0)
        ax.text(80.5, y, lab, fontsize=5.6, ha="left", va="center", color=INK, linespacing=1.1)
    save(fig, f"{paths.FIGURES}/transformer_1_overview")


def tokens():
    fig, ax = canvas(50, 13)
    P, v = vessel(8, 56, 41)
    tube(ax, P, v, r=2.0)
    for j in range(6):
        node(ax, *P[j + 1], str(j + 1), r=1.35)
        ax.plot([P[j + 1][0]] * 2, [P[j + 1][1] - 2.8, 33.6], color=MUTED, lw=.7, ls=":")
    ax.text(8, 47.4, "centerline respaced to chords of $\\ell$ = 5 mm", fontsize=6.5, ha="left", color=INK)
    ax.text(8, 45.5, "$\\theta_j$ = turn at vertex $j$, e.g. 0.876 rad (50.2$^\\circ$) gives $\\theta_j/\\ell$ = 0.175 rad/mm", fontsize=5.6, ha="left", color=MUTED)
    colourbar(ax, 62, 80, 45.2, "turning per mm")
    mu, sd = .15, .08
    z, s = (TH - mu) / sd, np.linspace(0, 1, 6)
    rows = [("$\\theta_j/\\ell$ (rad/mm)", TH, 31.5, "{:.2f}"), ("$z_j$", z, 28, "{:+.2f}"), ("$s_j$", s, 24.5, "{:.1f}")]
    for lab, vals, y, f in rows:
        ax.text(1.5, y, lab, fontsize=5.8, ha="left", va="center", color=INK)
        for j in range(6):
            ax.text(P[j + 1][0], y, f.format(vals[j]), fontsize=6, ha="center", va="center", color=INK)
    ax.plot([1.5, 58], [22.6, 22.6], color=MUTED, lw=.6)
    ax.text(30, 19.2, "$z_j = (\\theta_j/\\ell - \\mu)/\\sigma$ with $\\mu$ = %s, $\\sigma$ = %s over the training tokens;  $s_j$ = position along the vessel\n" % (mu, sd)
            + f"the mean of the $\\theta_j/\\ell$ row is $T_5$ = {TH.mean():.3f}, the scalar the logistic baseline gets", fontsize=5.7, ha="center", va="center", color=INK, linespacing=1.5)
    rr = np.random.default_rng(5)
    Wm, b = rr.normal(0, .7, (2, D)), rr.normal(0, .2, D)
    Emb = np.c_[z, s] @ Wm + b
    para(ax, 63, 23.5, 3.2, 10, fc=LAYER)
    ax.text(64.6, 37.5, "$\\times W + b$", fontsize=6.2, ha="center", color=PURPLE)
    arrow(ax, (59.5, 28.7), (62.6, 28.7), GREY, 1.6)
    ax.text(84, 40.5, f"each token becomes {D} channels ({HP['d_model']} in the model)", fontsize=5.8, ha="center", color=INK)
    for k in range(8):
        x = 71 + k * 3.9
        beads(ax, x, 29, Emb[k] if k < 6 else np.zeros(D), ghost=k >= 6, r=1.5, step=3.25, fs=4.2)
        ax.text(x, 20, str(k + 1) if k < 6 else "pad", fontsize=5.6, ha="center", color=MUTED)
    ax.text(84, 16.5, "dashed: padding, masked in attention", fontsize=5.4, ha="center", color=MUTED)
    save(fig, f"{paths.FIGURES}/transformer_2_tokens")


def attention(e):
    fig, ax = canvas(60, 5)
    rr = np.random.default_rng(7)
    turns = np.r_[rr.normal(0, .4, 8), 0, 0] * np.array([1, -1] * 5)
    P = fit(chain(turns), 7, 80, 47)
    v = np.abs(np.r_[turns[0], turns[:8], turns[7]])
    tube(ax, P[:10], v / v.max(), r=1.8)
    q = 4
    ax.plot(*P[9:12].T, color=GREY, lw=1.2, ls=(0, (2, 2)), zorder=1)
    pos = [P[i + 1] for i in range(8)] + [P[10], P[11]]
    for i, p in enumerate(pos):
        if i >= 8:
            node(ax, *p, "pad", fc="white", ec=GREY, ls=(0, (2, 1.5)), r=1.5, fs=4.2)
        else:
            node(ax, *p, str(i), fc="#ffd9c2" if i == q else "white", ec=LOW if i == q else INK, r=1.35)
    ks = list(range(q - W, q + W + 1))
    cx, wd = (pos[ks[0]][0] + pos[ks[-1]][0]) / 2, pos[ks[-1]][0] - pos[ks[0]][0] + 9
    ax.add_patch(Ellipse((cx, 47), wd, 15, fc=HIGH, alpha=.09, ec=HIGH, lw=.8, ls=(0, (3, 2)), zorder=0))
    ax.text(cx, 57.3, f"attention window: token {q} sees keys {ks[0]} to {ks[-1]}", fontsize=6.3, ha="center", color=HIGH)
    for k, j in enumerate(ks):
        if j == q:
            continue
        arrow(ax, (pos[j][0], pos[j][1] + 2.2), (pos[q][0], pos[q][1] + 2.2), HIGH, .6 + 15 * e["weight"][k], style="-",
              connectionstyle=f"arc3,rad={-.5 if j < q else .5}", alpha=.55, shrinkA=1, shrinkB=1)
    for lab, y in (("score $q\\cdot k_j/\\sqrt{%d}$" % D, 35), ("weight $a_j$ (softmax)", 31.8), ("value $v_j$", 24)):
        ax.text(1, y, lab, fontsize=5.7, ha="left", va="center", color=INK)
    for k, j in enumerate(ks):
        x = pos[j][0]
        ax.text(x, 35, f"{e['score'][k]:.2f}", fontsize=5.8, ha="center", va="center", color=LOW if j == q else INK)
        ax.text(x, 31.8, f"{e['weight'][k]:.2f}", fontsize=5.8, ha="center", va="center", color=LOW if j == q else INK, fontweight="bold")
        ax.plot([x, x], [pos[j][1] - 2.4, 37.2], color=MUTED, lw=.6, ls=":")
        beads(ax, x, 23, e["V"][k], r=1.5, step=3.3, fs=4.2)
    arrow(ax, (pos[ks[-1]][0] + 4.5, 23), (84.5, 23), PINK, 2.4)
    ax.text(pos[ks[-1]][0] + 8.5, 27.2, "$\\sum_j a_j v_j$", fontsize=6.6, ha="center", color=PINK)
    beads(ax, 91, 23, e["o"], ec=LOW, r=1.55, step=3.3, fs=4.2)
    ax.text(91, 14.6, "$o$, the new\nstate of token %d" % q, fontsize=5.8, ha="center", color=LOW, linespacing=1.2)
    ax.text(1, 8.5, "dashed nodes are padding. They are never attended to, and a padded query keeps only itself so its softmax is defined.\n"
            f"Band width is the weight $a_j$; they sum to {e['weight'].sum():.2f}. One head is drawn, the model has {HP['nhead']}.",
            fontsize=5.5, ha="left", va="center", color=MUTED, linespacing=1.5)
    save(fig, f"{paths.FIGURES}/transformer_3_attention")


def encoder(e):
    fig, ax = canvas(46, 4)
    cols = [("$x$", e["x"]), ("LayerNorm$(x)$", e["ln_x"]), ("$a$", e["a"]), ("$x_1 = x + a$", e["x1"]),
            ("LayerNorm$(x_1)$", e["ln_x1"]), ("$f$", e["f"]), ("$y = x_1 + f$", e["y"])]
    ops = [("LayerNorm", "p"), ("local\nattention", "p"), ("add", "+"), ("LayerNorm", "p"), (f"feed-forward\n{D} to {2 * D} to {D}, ReLU", "p"), ("add", "+")]
    xs = [6 + i * 14.6 for i in range(7)]
    ax.text(50, 44, "One encoder layer on one token, continuing from the values of Fig. 3", **CAP)
    for i, ((name, vec), x) in enumerate(zip(cols, xs)):
        beads(ax, x, 22, vec, ec=LOW if i in (0, 6) else None, r=1.6, step=3.4, fs=4.5)
        ax.text(x, 12.6, name, fontsize=6, ha="center", color=INK)
    for i, (lab, kind) in enumerate(ops):
        a, b = xs[i] + 2.6, xs[i + 1] - 2.6
        xm = (a + b) / 2
        if kind == "p":
            arrow(ax, (a, 22), (xm - 2.3, 22), GREY, 1.4), arrow(ax, (xm + 2.3, 22.8), (b, 22.8), GREY, 1.4)
            para(ax, xm - 2, 17.4, 3.4, 9.2)
            ax.text(xm, 31.2, lab, fontsize=5.6, ha="center", va="center", color=PURPLE, linespacing=1.1)
        else:
            arrow(ax, (a, 22), (xm - 1.8, 22), GREY, 1.4), arrow(ax, (xm + 1.8, 22), (b, 22), GREY, 1.4)
            ax.add_patch(Circle((xm, 22), 1.7, fc="white", ec=HIGH, lw=1.2, zorder=3))
            ax.text(xm, 22, "+", fontsize=8, ha="center", va="center", color=HIGH, zorder=4)
    for a, b, lab in ((0, 2, "skip"), (3, 5, "skip")):  # blue skips run over the layers and drop onto the sums
        xm = (xs[b] + 2.6 + xs[b + 1] - 2.6) / 2
        elbow(ax, [(xs[a] + 1, 29), (xs[a] + 1, 37), (xm, 37), (xm, 24.1)], HIGH, 1.3)
        ax.text((xs[a] + xm) / 2, 39.2, f"{lab} connection", fontsize=5.8, ha="center", color=HIGH)
    ax.text(50, 6.5, f"every token goes through this layer at once; the model stacks {HP['layers']} layers (Fig. 1)", **CAP)
    save(fig, f"{paths.FIGURES}/transformer_4_encoder")


def readout(e):
    fig, ax = canvas(40, 4)
    ax.text(50, 38.5, "From tokens to a probability", **CAP)
    xs = [6 + k * 4.4 for k in range(5)]
    for k, x in enumerate(xs):
        beads(ax, x, 26, e["Y"][k] if k < 4 else np.zeros(D), ghost=k == 4, r=1.5, step=3.25, fs=4.2)
    ax.text(xs[0] - 1.5, 34.6, "tokens leaving the last encoder layer (dashed: padding, left out)", fontsize=5.6, ha="left", color=MUTED)
    mx, yb = 36, 16.4
    for x in xs[:4]:  # a pink bracket gathers the real tokens, then one arrow into their mean
        ax.plot([x, x], [19.3, yb], color=PINK, lw=1.6, solid_capstyle="round")
    ax.plot([xs[0], mx], [yb, yb], color=PINK, lw=1.6, solid_capstyle="round")
    arrow(ax, (mx, yb), (mx, 19.2), PINK, 1.6)
    ax.text((xs[0] + mx) / 2, yb - 2.6, "mean over the real tokens", fontsize=5.8, ha="center", color=PINK)
    beads(ax, mx, 26, e["mean"], r=1.55, step=3.3, fs=4.4)
    arrow(ax, (mx + 3, 26), (47, 26), GREY, 2.0)
    ax.text(mx + 5.5, 29.8, "append\nlength", fontsize=5.8, ha="center", color=LOW, linespacing=1.15)
    vx, wx = 51, 58.5
    ys = beads(ax, vx, 26, e["vec"], r=1.55, step=3.3, fs=4.4)
    ax.add_patch(Circle((vx, ys[-1]), 1.55, fc="#fde3d3", ec=LOW, lw=1.3, zorder=3))
    ax.text(vx, ys[-1], f"{e['len']:.2f}", fontsize=4.4, ha="center", va="center", zorder=4)
    ax.text(vx, 35.4, "$x$", fontsize=7, ha="center", color=INK)
    ax.text((vx + wx) / 2, 26, "$\\cdot$", fontsize=11, ha="center", va="center")
    beads(ax, wx, 26, e["w"], r=1.55, step=3.3, fs=4.4, cmap=plt.get_cmap("Purples"))
    ax.text(wx, 35.4, "$w$", fontsize=7, ha="center", color=PURPLE)
    ax.text(66.5, 26, f"+ b\n= {e['b']:.2f}", fontsize=6.2, ha="center", va="center", color=INK, linespacing=1.3)
    ax.text(74, 26, f"z = {e['logit']:.2f}", fontsize=6.6, ha="center", va="center", color=INK)
    arrow(ax, (79, 26), (83, 26), GREY, 1.6)
    ax.text(81, 29.2, "$\\sigma$", fontsize=7, ha="center", color=PURPLE)
    gauge(ax, 91, 24, 7.3, e["p"])
    ax.text(91, 17.5, f"P(Disease) = {e['p']:.2f}", fontsize=6.2, ha="center", color=INK)
    ax.text(50, 8.5, "$x$: the four means, then the vessel length (orange);  $w$: learned weights;  "
            "$z = \\sum_i x_i w_i + b$,  $\\sigma(z) = 1/(1+e^{-z})$", fontsize=5.9, ha="center", va="center", color=INK)
    save(fig, f"{paths.FIGURES}/transformer_5_readout")


def main():
    e = example()
    overview(), tokens(), attention(e), encoder(e), readout(e)


if __name__ == "__main__":
    main()
