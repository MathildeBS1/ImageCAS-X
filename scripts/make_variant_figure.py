#!/usr/bin/env python
"""The two connectivity variants of the left coronary system, side by side.

Dominance (scripts/make_dominance_figure.py) changes which system reaches the
crux; these two change the *connectivity* of the left tree itself, which is what a
topological descriptor has to represent rather than discard:

- absent left main: LAD and LCX arise from separate ostia, so the left tree has
  two roots instead of one;
- ramus intermedius: a third vessel leaves the left main between them.

Both variants live in the first two centimetres of the tree, which is invisible at
whole-tree scale, so the bottom row zooms on the ostial region. Every number in the
panel titles is measured from the tree the feature code uses, not typed in, so the
figure and the text cannot drift apart.

    python scripts/make_variant_figure.py
"""

from __future__ import annotations

import argparse

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from topology import graph, io, paths, viz

DPI = 150
#: Half-width of the zoom cube, mm. 15 mm covers the left main and the origins of
#: everything that leaves it in every case looked at.
ZOOM_MM = 15.0


def ostia(tree: graph.CoronaryTree) -> np.ndarray:
    """(n, 3) ostium positions, LPS mm."""
    return np.array([n.position for n in tree.nodes.values() if n.kind == graph.OSTIUM])


def draw(ax, centerline: io.Centerline, center: np.ndarray | None = None,
         elev: int = 18, azim: int = -62) -> list[str]:
    """Plot one side's centerlines; ``center`` restricts to a cube around a point."""
    names: list[str] = []
    for poly in centerline.lines:
        pts = centerline.points[poly]
        name = str(centerline.segment_name[poly[len(poly) // 2]])
        if center is not None:
            # Keep the points inside the cube, and split where the vessel leaves it,
            # so a line that re-enters does not get a chord drawn across the gap.
            inside = np.all(np.abs(pts - center) <= ZOOM_MM, axis=1)
            if not inside.any():
                continue
            runs = np.split(pts[inside], np.flatnonzero(np.diff(np.flatnonzero(inside)) > 1) + 1)
        else:
            runs = [pts]
        names.append(name)
        for run in runs:
            if len(run) > 1:
                ax.plot(*run.T, color=viz.color_for(name), lw=3.0 if center is not None else 2.2)

    sel = np.asarray(centerline.start_points) != 0
    ax.scatter(*centerline.points[sel].T, marker="*", s=210, c="white",
               edgecolors="black", linewidths=1.1, depthshade=False, zorder=5)

    if center is not None:
        for lo, hi, setter in zip(center - ZOOM_MM, center + ZOOM_MM,
                                  (ax.set_xlim3d, ax.set_ylim3d, ax.set_zlim3d)):
            setter(lo, hi)
    else:
        viz.set_axes_equal(ax)
    ax.set_box_aspect((1, 1, 1), zoom=1.85)
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    return names


def scale_bar(ax, center: np.ndarray, mm: float = 5.0) -> None:
    """A bar of known length, so the zoom row can be read as a measurement."""
    x0, y0, z0 = center - ZOOM_MM * 0.82
    ax.plot([x0, x0 + mm], [y0, y0], [z0, z0], color="black", lw=2.5, zorder=6)
    ax.text(x0 + mm / 2, y0, z0 - 1.6, f"{mm:.0f} mm", ha="center", va="top",
            fontsize=8.5, zorder=6)


def trunk_length(tree: graph.CoronaryTree) -> float:
    return sum(s.length for s in tree.segments if s.name == "LM")


def branch_children(tree: graph.CoronaryTree) -> list[str]:
    """Names leaving the most distal left main segment."""
    lm = [s for s in tree.segments if s.name == "LM"]
    if not lm:
        return []
    distal = max(lm, key=lambda s: len(tree.children_of(s)))
    return [c.name for c in tree.children_of(distal)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--typical", type=int, default=3, help="a case with a left main trunk")
    ap.add_argument("--absent", type=int, default=21, help="a case with no left main")
    ap.add_argument("--ramus", type=int, default=85, help="a case whose left main trifurcates")
    args = ap.parse_args()

    cids = [args.typical, args.absent, args.ramus]
    trees = {c: graph.load_tree(c, "left") for c in cids}
    lines = {c: io.load_centerline(c, "left") for c in cids}

    sep = np.linalg.norm(np.diff(ostia(trees[args.absent]), axis=0)[0])
    titles = [
        (args.typical, "Typical left main",
         f"one ostium; a {trunk_length(trees[args.typical]):.1f} mm trunk divides\n"
         f"into {' and '.join(branch_children(trees[args.typical]))}"),
        (args.absent, "Absent left main — 11 of 800 cases",
         f"two ostia, {sep:.1f} mm apart; LAD and LCX\narise separately"),
        (args.ramus, "Ramus intermedius — 196 of 800 cases",
         f"a {trunk_length(trees[args.ramus]):.1f} mm trunk gives off three vessels\n"
         f"at one node: {', '.join(branch_children(trees[args.ramus]))}"),
    ]

    fig = plt.figure(figsize=(13.5, 8.6))
    all_names: list[str] = []
    for i, (cid, title, blurb) in enumerate(titles):
        ax = fig.add_subplot(2, 3, i + 1, projection="3d")
        all_names += draw(ax, lines[cid])
        ax.set_title(f"{title}\ncase {cid}: {blurb}", fontsize=10, linespacing=1.45)

        center = ostia(trees[cid]).mean(axis=0)
        axz = fig.add_subplot(2, 3, i + 4, projection="3d")
        draw(axz, lines[cid], center=center)
        scale_bar(axz, center)

    fig.legend(handles=viz.legend_handles(all_names), loc="lower center",
               ncol=8, frameon=False, fontsize=9)
    fig.suptitle(
        "Connectivity variants of the left coronary system\n"
        "Top: the whole left tree. Bottom: the same case within 15 mm of the ostium, where the "
        "variant lives.  ★ marks each ostium.",
        fontsize=12,
    )
    out = paths.FIGURES / "06_left_variants.png"
    fig.tight_layout(rect=[0, 0.07, 1, 0.90])
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
