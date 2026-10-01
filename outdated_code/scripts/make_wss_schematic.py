"""Figure: where the shape of a vessel puts low wall shear stress.

Two schematic vessels in the plane, (a) a bend and (b) a bifurcation, with the
velocity profile drawn at a few stations and the walls marked where the shear is
low (inner wall of the bend, lateral walls of the daughter branches) and where it
is high (outer wall of the bend, the flow divider). These are the plaque sites
Asakura and Karino (1990) mapped; the profiles are drawn by hand, not simulated.

    uv run python scripts/make_wss_schematic.py

Writes figures/wss_schematic.{pdf,png}. Upload the PDF to
content/background/figures/ in Overleaf.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, Polygon

from make_tortuosity_ambiguity import INK, OUT_DIR

LUMEN = "#eef3f9"
LOW = "#e8590c"     # low / oscillating WSS: plaque-prone
HIGH = "#2a78d6"    # high WSS
PROFILE = "#52606d"
R = 1.0             # parent radius; everything else is in units of it


def frame(points):
    """Unit tangents and left normals of a polyline."""
    t = np.gradient(points, axis=0)
    t /= np.linalg.norm(t, axis=1, keepdims=True)
    return t, np.column_stack([-t[:, 1], t[:, 0]])


def arclength(points):
    return np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(points, axis=0), axis=1))])


def band(ax, wall, inward, color, width=0.13):
    """A strip lying just inside a wall, so it reads as a property of that wall."""
    inner = wall + width * inward
    ax.add_patch(Polygon(np.vstack([wall, inner[::-1]]), closed=True, fc=color, ec="none",
                         alpha=0.9, zorder=3))


def profile(ax, p, t, n, r, u, scale):
    """Velocity profile across the lumen at p: arrows along t, u(eta) with eta=+1 on the n side."""
    ax.plot(*np.array([p - 0.97 * r * n, p + 0.97 * r * n]).T, lw=0.6, color=PROFILE, zorder=4)
    eta = np.linspace(-1, 1, 60)
    tips = p + np.outer(eta * r, n) + np.outer(scale * u(eta), t)
    ax.plot(*tips.T, lw=0.8, color=PROFILE, zorder=4)
    for e in np.linspace(-0.75, 0.75, 5):
        base = p + e * r * n
        ax.add_patch(FancyArrowPatch(base, base + scale * u(np.array(e)) * t, arrowstyle="-|>",
                                     mutation_scale=5, lw=0.6, color=PROFILE, zorder=4,
                                     shrinkA=0, shrinkB=0))


def parabolic(eta):
    return 1 - eta ** 2


def skewed(k):
    """Peak pushed toward the eta = -1 wall (k > 0); normalised to a maximum of 1."""
    e = np.linspace(-1, 1, 400)
    peak = ((1 - e ** 2) * np.exp(-k * e)).max()
    return lambda eta: (1 - eta ** 2) * np.exp(-k * eta) / peak


def eddy(ax, origin, along, toward_wall, r):
    """A recirculation loop against a wall: backward along the wall, forward further in."""
    center = origin + 0.45 * r * toward_wall
    theta = np.deg2rad(np.linspace(130, 430, 80))
    loop = (center + np.outer(0.5 * r * np.cos(theta), along)
            + np.outer(0.26 * r * np.sin(theta), toward_wall))
    ax.plot(*loop[:-3].T, lw=0.9, color=LOW, zorder=5)
    ax.add_patch(FancyArrowPatch(loop[-4], loop[-1], arrowstyle="-|>", mutation_scale=6,
                                 lw=0.9, color=LOW, zorder=5, shrinkA=0, shrinkB=0))


def outline(ax, *walls):
    for w in walls:
        ax.plot(*w.T, lw=1.4, color=INK, solid_capstyle="round", zorder=6)


def label(ax, xy, text, color=INK, fontsize=7.5, **kw):
    ax.text(*xy, text, fontsize=fontsize, color=color, zorder=7, **kw)


# --------------------------------------------------------------------------------------
# (a) Bend
# --------------------------------------------------------------------------------------
def draw_bend(ax):
    rc, sweep = 2.3, np.deg2rad(115)
    straight_in = np.column_stack([np.linspace(-4.0, 0, 80), np.zeros(80)])
    phi = np.linspace(-np.pi / 2, -np.pi / 2 + sweep, 160)[1:]
    arc = np.column_stack([rc * np.cos(phi), rc + rc * np.sin(phi)])
    exit_dir = np.array([-np.sin(phi[-1]), np.cos(phi[-1])])
    straight_out = arc[-1] + np.outer(np.linspace(0, 3.6, 80)[1:], exit_dir)
    c = np.vstack([straight_in, arc, straight_out])
    t, n = frame(c)
    s = arclength(c)
    s_arc0, s_arc1 = 4.0, 4.0 + rc * sweep

    inner, outer = c + R * n, c - R * n            # the bend turns left, so left is inner
    ax.add_patch(Polygon(np.vstack([inner, outer[::-1]]), closed=True, fc=LUMEN, ec="none",
                         zorder=1))

    low = (s > s_arc0 + 0.45 * (s_arc1 - s_arc0)) & (s < s_arc1 + 1.9)
    high = (s > s_arc0 + 0.15 * (s_arc1 - s_arc0)) & (s < s_arc1 + 0.4)
    band(ax, inner[low], -n[low], LOW)
    band(ax, outer[high], n[high], HIGH)
    outline(ax, inner, outer)

    i_in = np.searchsorted(s, 1.3)
    profile(ax, c[i_in], t[i_in], n[i_in], R, parabolic, 1.25)
    i_out = np.searchsorted(s, s_arc1 + 1.05)
    profile(ax, c[i_out], t[i_out], n[i_out], R, skewed(1.8), 1.25)
    i_eddy = np.searchsorted(s, s_arc1 + 0.1)
    eddy(ax, c[i_eddy], t[i_eddy], n[i_eddy], R)

    ax.add_patch(FancyArrowPatch((-4.9, 0), (-4.15, 0), arrowstyle="-|>", mutation_scale=8,
                                 lw=1.1, color=INK))
    label(ax, (-4.95, 0.25), "flow", ha="left", va="bottom")

    i_mid = np.searchsorted(s, s_arc0 + 0.55 * (s_arc1 - s_arc0))
    label(ax, outer[i_mid] - 0.25 * n[i_mid], "outer wall\nhigh WSS", color=HIGH,
          ha="left", va="top", linespacing=1.15)
    i_lo = np.searchsorted(s, s_arc1 - 0.3)
    label(ax, inner[i_lo] + 0.3 * n[i_lo], "inner wall\nlow WSS", color=LOW,
          ha="right", va="center", linespacing=1.15)
    label(ax, outer[i_out] + np.array([0.3, 0.0]), "fast core\ncarried to\nthe outer wall",
          color=PROFILE, ha="left", va="center", fontsize=7, linespacing=1.15)
    label(ax, (-2.7, -1.25), "parabolic\nprofile", color=PROFILE, ha="center", va="top",
          fontsize=7, linespacing=1.15)
    return c


# --------------------------------------------------------------------------------------
# (b) Bifurcation
# --------------------------------------------------------------------------------------
def bezier(p0, p1, p2, n=40):
    u = np.linspace(0, 1, n)[:, None]
    return (1 - u) ** 2 * p0 + 2 * (1 - u) * u * p1 + u ** 2 * p2


def draw_bifurcation(ax):
    half = np.deg2rad(34)
    rd = R / 2 ** (1 / 3)                      # Murray's law, two equal daughters
    x0, t_end = -4.2, 5.9

    walls, daughters = {}, {}
    for sign in (+1, -1):
        d = np.array([np.cos(half), sign * np.sin(half)])
        lat = sign * np.array([-d[1], d[0]])   # points away from the flow divider
        daughters[sign] = (d, lat)
        tt = np.linspace(1.4, t_end, 100)
        # Lateral wall: the parent wall y = +-R, rounded into the daughter's lateral wall.
        start = np.array([-1.3, sign * R])
        join = 1.4 * d + rd * lat
        walls[sign] = np.vstack([
            np.column_stack([np.linspace(x0, start[0], 40), np.full(40, sign * R)]),
            bezier(start, np.array([0.0, sign * R]), join)[1:-1],
            np.outer(tt, d) + rd * lat,
        ])

    # The two inner walls cross on the axis at x = rd / sin(half); round that apex.
    apex = np.array([rd / np.sin(half), 0.0])
    d_up, d_dn = daughters[+1][0], daughters[-1][0]
    p_up, p_dn = apex + 0.45 * d_up, apex + 0.45 * d_dn
    tip = bezier(p_dn, apex - np.array([0.12, 0.0]), p_up, 30)
    run = t_end - apex @ d_up - 0.45           # so the inner walls end level with the lateral
    inner_up = p_up + np.outer(np.linspace(0, run, 100), d_up)
    inner_dn = p_dn + np.outer(np.linspace(0, run, 100), d_dn)
    divider = np.vstack([inner_dn[::-1], tip[1:-1], inner_up])

    top, bottom = walls[+1], walls[-1]
    ax.add_patch(Polygon(np.vstack([top, divider[::-1], bottom[::-1]]), closed=True,
                         fc=LUMEN, ec="none", zorder=1))

    # Low WSS on each lateral wall, from the corner to a few radii downstream.
    for sign, wall in ((+1, top), (-1, bottom)):
        seg = wall[(wall[:, 0] > -0.6) & (wall[:, 0] < 2.5)]
        _, nn = frame(seg)
        band(ax, seg, -sign * nn, LOW)
    # High WSS on the flow divider (runs upward through the apex, so left is the lumen).
    seg = np.vstack([inner_dn[:16][::-1], tip[1:-1], inner_up[:16]])
    _, nn = frame(seg)
    band(ax, seg, nn, HIGH)
    outline(ax, top, bottom, divider)

    profile(ax, np.array([-3.0, 0.0]), np.array([1.0, 0.0]), np.array([0.0, 1.0]), R,
            parabolic, 1.25)
    for sign in (+1, -1):
        d, lat = daughters[sign]
        # eta = +1 on the lateral side; the peak sits toward the divider.
        profile(ax, 3.4 * d, d, lat, rd, skewed(1.6), 1.05)
        eddy(ax, 1.25 * d, d, lat, rd)

    ax.add_patch(FancyArrowPatch((-5.1, 0), (-4.35, 0), arrowstyle="-|>", mutation_scale=8,
                                 lw=1.1, color=INK))
    label(ax, (-5.15, 0.25), "flow", ha="left", va="bottom")
    label(ax, (0.5, 1.3), "lateral wall\nlow WSS", color=LOW, ha="right", va="bottom",
          linespacing=1.15)
    label(ax, (0.5, -1.3), "lateral wall\nlow WSS", color=LOW, ha="right", va="top",
          linespacing=1.15)
    label(ax, apex + np.array([0.75, 0.0]), "flow divider\nhigh WSS", color=HIGH, ha="left",
          va="center", linespacing=1.15)


def main():
    plt.rcParams.update({"font.size": 8, "font.family": "sans-serif"})
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(6.3, 3.1),
                                     gridspec_kw={"width_ratios": [1.0, 1.08], "wspace": 0.05})
    draw_bend(ax_a)
    draw_bifurcation(ax_b)

    ax_a.set_xlim(-5.1, 5.0)
    ax_a.set_ylim(-2.1, 7.0)
    ax_b.set_xlim(-5.3, 5.6)
    ax_b.set_ylim(-4.6, 4.6)
    for ax, tag in ((ax_a, "(a) bend"), (ax_b, "(b) bifurcation")):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(tag, fontsize=9, color=INK, loc="left")

    handles = [
        Line2D([], [], color=LOW, lw=4, label="low or reversing WSS (plaque-prone)"),
        Line2D([], [], color=HIGH, lw=4, label="high WSS"),
        Line2D([], [], color=PROFILE, lw=0.9, marker=">", ms=3.5, label="velocity profile"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, fontsize=7.5,
               handlelength=1.6, columnspacing=1.6)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.1)

    os.makedirs(OUT_DIR, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT_DIR, f"wss_schematic.{ext}"), dpi=300)
    print("wrote figures/wss_schematic.{pdf,png}")


if __name__ == "__main__":
    main()
