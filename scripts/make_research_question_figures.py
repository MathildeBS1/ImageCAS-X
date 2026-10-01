"""Figures for thesis/week5/research_question.tex.

Four schematics, one per step of the argument that has no figure yet (the bend and
bifurcation flow picture is make_wss_schematic.py):

  rq_chain      the argument, step by step, and which steps are untested
  rq_curvature  three vessels with one tortuosity index but different curvature
  rq_angle      the LAD-LCX angle at its minimum, mean and maximum in Temov et al. 2016
  rq_design     cross-sectional versus longitudinal-from-healthy study designs

    uv run python scripts/make_research_question_figures.py

Writes figures/rq_*.{pdf,png}.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from matplotlib.patches import Arc, FancyArrowPatch, FancyBboxPatch

from make_tortuosity_ambiguity import (CHORD_MM, CMAP, INK, KAPPA_MAX_SHOWN, MUTED, OUT_DIR, TAU,
                                       build, bump, metrics, segments, solve_amplitude)
from make_wss_schematic import HIGH, LOW, LUMEN

HEALTHY = "#52606d"
BOX = "#f5f7fa"


def save(fig, name):
    os.makedirs(OUT_DIR, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT_DIR, f"{name}.{ext}"), dpi=300)
    plt.close(fig)
    print(f"wrote figures/{name}.{{pdf,png}}")


def arrow(ax, a, b, color=INK, lw=1.0, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=9, lw=lw, color=color,
                                 linestyle=ls, shrinkA=0, shrinkB=0))


# --------------------------------------------------------------------------- chain

STEPS = [
    ("Plaque forms at specific sites, not evenly along the tree", "established"),
    ("Those sites have low wall shear stress", "established"),
    ("Low shear occurs at bends and bifurcations", "established"),
    ("Geometry on a scan tracks low shear, but only some measures do", "established"),
    ("Coronary geometry differs widely between people", "established"),
    ("Does the geometry of a healthy tree predict who develops plaque?", "untested"),
]


def chain():
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    w, h, gap = 6.6, 0.62, 0.28
    for i, (text, status) in enumerate(STEPS):
        y = -i * (h + gap)
        open_q = status == "untested"
        ax.add_patch(FancyBboxPatch((0, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                    fc="white" if open_q else BOX, ec=LOW if open_q else MUTED,
                                    lw=1.4 if open_q else 0.8, ls="--" if open_q else "-"))
        ax.text(0.25, y, f"{i + 1}", ha="center", va="center", fontsize=10, weight="bold",
                color=LOW if open_q else INK)
        ax.text(0.55, y, text, ha="left", va="center", fontsize=9, color=INK)
        if i:
            arrow(ax, (w / 2, y + h / 2 + gap - 0.02), (w / 2, y + h / 2 + 0.02), color=MUTED)

    # Brackets: steps 1-4 are about sites within a tree, steps 5-6 about people.
    def bracket(i0, i1, label, color):
        top, bot = -i0 * (h + gap) + h / 2, -i1 * (h + gap) - h / 2
        x = w + 0.25
        ax.plot([x - 0.1, x, x, x - 0.1], [top, top, bot, bot], lw=1.0, color=color)
        ax.text(x + 0.15, (top + bot) / 2, label, ha="left", va="center", fontsize=8.5,
                color=color, linespacing=1.3)

    bracket(0, 3, "where in a tree\nplaque forms", INK)
    bracket(4, 5, "who develops\nplaque", LOW)

    ax.set_xlim(-0.1, w + 1.6)
    ax.set_ylim(-5 * (h + gap) - h / 2 - 0.1, h / 2 + 0.1)
    ax.axis("off")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, "rq_chain")


# ----------------------------------------------------------------------- curvature

ROWS = [
    ("one wide bend", lambda s: (np.sin(np.pi * s), 0 * s), 0.0),
    ("many small bends", lambda s: (np.sin(6 * np.pi * s), 0 * s), -12.0),
    ("one sharp bend", lambda s: (bump(0.25, 0.11)(s), 0 * s), -30.0),
]


def mean_abs_curvature(points, kappa):
    """Arc-length-weighted mean of |kappa|, the quantity Kashyap et al. call average curvature."""
    ds = np.linalg.norm(np.diff(points, axis=0), axis=1)
    k = 0.5 * (kappa[:-1] + kappa[1:])
    return (k * ds).sum() / ds.sum()


def curvature():
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    norm = Normalize(0.0, KAPPA_MAX_SHOWN)
    for label, profile, base in ROWS:
        p = build(profile, solve_amplitude(profile))
        m = metrics(p)
        xy = p[:, :2] + [0, base]
        ax.plot([0, CHORD_MM], [base, base], ls=(0, (3, 2)), lw=0.8, color=MUTED, zorder=1)
        ax.add_collection(LineCollection(segments(xy), colors=CMAP(norm(m["kappa"][:-1])),
                                         linewidths=2.4, capstyle="round", zorder=2))
        ax.plot(0, base, "o", ms=5, color=INK, zorder=3)
        ax.plot(CHORD_MM, base, "o", ms=5, mfc="white", mec=INK, mew=1.2, zorder=3)
        ax.text(CHORD_MM + 4, base + 1.0, label, ha="left", va="bottom", fontsize=8.5, color=INK)
        ax.text(CHORD_MM + 4, base - 0.3,
                f"$\\tau = {TAU:.2f}$\nmean curvature: {mean_abs_curvature(p, m['kappa']):.2f}"
                " mm$^{-1}$", ha="left", va="top", fontsize=8.5, color=INK, linespacing=1.4)

    ax.text(0, -1.5, "start", ha="center", va="top", fontsize=7, color=MUTED)
    ax.text(CHORD_MM, -1.5, "end", ha="center", va="top", fontsize=7, color=MUTED)
    ax.set_xlim(-3, CHORD_MM + 40)
    ax.set_ylim(-36, 17)
    ax.set_aspect("equal")
    ax.axis("off")

    cax = fig.add_axes([0.08, 0.13, 0.4, 0.03])
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=CMAP), cax=cax,
                      orientation="horizontal", extend="max")
    cb.set_label("local curvature $\\kappa$ (mm$^{-1}$)", fontsize=8, color=INK)
    cb.ax.tick_params(labelsize=7, colors=INK)
    cb.outline.set_visible(False)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.22)
    save(fig, "rq_curvature")


# --------------------------------------------------------------------------- angle

ANGLES = [(35.5, "narrowest"), (79.4, "mean"), (178.0, "widest")]


def vessels(ax, segs, r):
    """Straight vessel segments drawn as one lumen with a dark wall: walls first, lumens on top."""
    for lw, c, z in ((r * 2 + 1.6, INK, 1), (r * 2, LUMEN, 2)):
        for a, b in segs:
            ax.plot(*np.array([a, b]).T, lw=lw, color=c, solid_capstyle="round", zorder=z)


def angle():
    fig, axes = plt.subplots(1, 3, figsize=(6.2, 2.5))
    for ax, (theta, label) in zip(axes, ANGLES):
        o = np.array([0.0, 0.0])
        segs = [((-1.4, 0), o)]
        for sign, name in ((1, "LAD"), (-1, "LCX")):
            u = np.array([np.cos(np.radians(sign * theta / 2)), np.sin(np.radians(sign * theta / 2))])
            segs.append((o, 1.3 * u))
            ax.text(*(1.3 * u + 0.4 * u), name, ha="center", va="center", fontsize=8, color=INK)
        vessels(ax, segs, 5)
        ax.add_patch(Arc(o, 1.2, 1.2, theta1=-theta / 2, theta2=theta / 2, color=LOW, lw=1.4,
                         zorder=3))
        ax.text(0.8 if theta < 150 else 0.95, 0, f"{theta:g}\u00b0", ha="left", va="center",
                fontsize=9, color=LOW, weight="bold", zorder=4,
                bbox=dict(fc="white", ec="none", pad=0.5) if theta >= 150 else None)
        ax.text(-1.4, 0.3, "LM", ha="center", va="bottom", fontsize=8, color=INK)
        ax.set_title(label, fontsize=9, color=INK)
        ax.set_xlim(-1.7, 1.9)
        ax.set_ylim(-1.8, 1.8)
        ax.set_aspect("equal")
        ax.axis("off")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.01, wspace=0.05)
    save(fig, "rq_angle")


# -------------------------------------------------------------------------- design

def tree(ax, x, y, s=1.0, plaque=False):
    """A small coronary-tree glyph; plaque marked at its bifurcations."""
    main = [((0, 0), (0.5, 0)), ((0.5, 0), (1.0, 0.35)), ((0.5, 0), (1.0, -0.35)),
            ((0.8, 0.21), (1.1, 0.05)), ((0.8, -0.21), (1.1, -0.05))]
    for a, b in main:
        ax.plot([x + s * a[0], x + s * b[0]], [y + s * a[1], y + s * b[1]], lw=2.2,
                color=HEALTHY, solid_capstyle="round", zorder=3)
    if plaque:
        for px, py in ((0.58, 0.07), (0.58, -0.07), (0.86, 0.26)):
            ax.plot(x + s * px, y + s * py, "o", ms=4.5, color=LOW, zorder=4)


def design():
    fig, ax = plt.subplots(figsize=(6.2, 3.9))

    # (a) cross-sectional
    y = 3.6
    ax.text(0, y + 1.25, "(a) Cross-sectional: one scan, geometry and disease measured together",
            fontsize=9, color=INK, weight="bold")
    arrow(ax, (0.2, y), (9.4, y), color=MUTED)
    ax.plot([0.2, 6.6], [y, y], lw=3, color=MUTED, alpha=0.25, solid_capstyle="butt")
    ax.text(3.4, y - 0.3, "geometry and plaque develop together, unobserved", ha="center",
            va="top", fontsize=8, color=MUTED, style="italic")
    ax.plot([7.1, 7.1], [y - 0.1, y + 0.1], lw=1.2, color=INK)
    tree(ax, 6.6, y + 0.5, plaque=True)
    ax.text(7.1, y - 0.3, "scan of patients\nreferred for\nsuspected disease", ha="center",
            va="top", fontsize=8, color=INK, linespacing=1.2)
    ax.text(8.1, y + 0.5, "which came\nfirst?", ha="left", va="center", fontsize=8.5, color=LOW,
            linespacing=1.2)

    # (b) longitudinal from a healthy state
    y = 0.4
    ax.text(0, y + 1.6, "(b) Longitudinal from a healthy state: geometry measured before disease",
            fontsize=9, color=INK, weight="bold")
    arrow(ax, (0.2, y), (9.4, y), color=MUTED)
    ax.plot([1.3, 1.3], [y - 0.1, y + 0.1], lw=1.2, color=INK)
    tree(ax, 0.8, y + 0.55)
    ax.text(1.3, y - 0.3, "baseline scan,\nno disease:\nmeasure geometry", ha="center", va="top",
            fontsize=8, color=INK, linespacing=1.2)
    ax.text(4.4, y + 0.15, "follow-up (years)", ha="center", va="bottom", fontsize=8,
            color=MUTED, style="italic")
    ax.plot([7.1, 7.1], [y - 0.1, y + 0.1], lw=1.2, color=INK)
    tree(ax, 6.6, y + 1.0, s=0.8, plaque=True)
    tree(ax, 6.6, y + 0.38, s=0.8)
    ax.text(7.65, y + 1.0, "develops disease", ha="left", va="center", fontsize=8, color=LOW)
    ax.text(7.65, y + 0.38, "stays free", ha="left", va="center", fontsize=8, color=HEALTHY)
    ax.text(7.1, y - 0.3, "outcome", ha="center", va="top", fontsize=8, color=INK)
    arrow(ax, (2.6, y + 0.55), (6.3, y + 0.55), color=HIGH, lw=1.2)
    ax.text(4.4, y + 0.62, "does geometry predict this?", ha="center", va="bottom", fontsize=8.5,
            color=HIGH)


    ax.set_xlim(-0.1, 10.0)
    ax.set_ylim(-0.9, 5.0)
    ax.axis("off")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, "rq_design")


if __name__ == "__main__":
    plt.rcParams.update({"font.size": 9, "font.family": "sans-serif"})
    chain()
    curvature()
    angle()
    design()
