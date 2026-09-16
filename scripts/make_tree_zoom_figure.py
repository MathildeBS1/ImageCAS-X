#!/usr/bin/env python
"""Figure: the whole tree in true 3D, next to a zoom on two adjacent centerline points.

The main tree figure (make_tree_figure.py) draws the centerline as a flat, coronal
(x-z) projection, which is fine for showing branching but hides genuine out-of-plane
motion -- exactly the kind of bend a 2D view would flatten away. The left panel here
redraws the same tree in true 3D (all of x, y, z, patient LPS frame, equal aspect so
no axis is stretched). The right panel zooms all the way in on two adjacent points
of one segment near a named branch, and labels every number that describes that
step: both points' full (x, y, z), the (dx, dy, dz) between them, and the resulting
3D distance -- so what one row of a Segment.points array actually is, in the
patient's own coordinates, is visible rather than asserted.

Usage:  python scripts/make_tree_zoom_figure.py [case_id] [--vessel LAD] [--to D1]
                                                 [--point-index -1]
"""

from __future__ import annotations

import argparse

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 -- registers the '3d' projection

from topology import graph, paths, viz


def _draw_tree_3d(ax, tree: graph.CoronaryTree, highlight: np.ndarray) -> None:
    for seg in tree.segments:
        p = seg.points
        ax.plot(p[:, 0], p[:, 1], p[:, 2], color=viz.color_for(seg.name), lw=1.6)
    for node in tree.nodes.values():
        if node.kind == "ostium":
            ax.scatter(*node.position, marker="s", s=45, color="black", depthshade=False)
    ax.scatter(*highlight, marker="*", s=260, color="black", edgecolor="white",
               linewidth=1.0, depthshade=False, zorder=5)
    viz.set_axes_equal(ax)
    ax.set_xlabel("LPS x (mm)", labelpad=2)
    ax.set_ylabel("LPS y (mm)", labelpad=2)
    ax.set_zlabel("LPS z (mm)", labelpad=2)
    ax.view_init(elev=18, azim=-60)
    ax.set_title("Whole tree, true 3D\n(star marks the zoomed-in points)", fontsize=9.5)


def _draw_two_points_3d(ax, p: np.ndarray, q: np.ndarray, color: str, seg_label: str) -> None:
    """Zoom to exactly two adjacent centerline points, with every number that
    describes them written on the plot: both full (x, y, z), the step (dx, dy, dz),
    and the resulting 3D distance -- nothing about the step is left off-figure."""
    d = q - p
    dist = float(np.linalg.norm(d))

    ax.plot([p[0], q[0]], [p[1], q[1]], [p[2], q[2]], "-", color=color, lw=2.2, zorder=2)
    ax.scatter(*p, s=110, color=color, edgecolor="white", linewidth=1.1, depthshade=False, zorder=3)
    ax.scatter(*q, s=110, color=color, edgecolor="white", linewidth=1.1, depthshade=False, zorder=3)

    pad = max(dist * 4.0, 1.2)
    mid = (p + q) / 2
    up = np.array([0.0, 0.0, 1.0]) * pad * 0.42

    ax.text(*(p - up), f"second-to-last point\n({p[0]:.3f}, {p[1]:.3f}, {p[2]:.3f}) mm",
            fontsize=8.5, color=color, ha="center", va="top", zorder=4)
    ax.text(*(q + up), f"last point (the bifurcation)\n({q[0]:.3f}, {q[1]:.3f}, {q[2]:.3f}) mm",
            fontsize=8.5, color=color, ha="center", va="bottom", zorder=4)
    ax.text(*(mid + 1.9 * up), f"$\\Delta$ = ({d[0]:.3f}, {d[1]:.3f}, {d[2]:.3f}) mm\n"
                                f"distance = {dist:.3f} mm", fontsize=9, fontweight="bold",
            color="black", ha="center", va="bottom", zorder=4)

    centre = mid
    for set_lim, c in zip((ax.set_xlim, ax.set_ylim, ax.set_zlim), centre):
        set_lim(c - pad, c + pad)
    ax.set_xlabel("LPS x (mm)", labelpad=12)
    ax.set_ylabel("LPS y (mm)", labelpad=12)
    ax.set_zlabel("LPS z (mm)", labelpad=12)
    ax.tick_params(labelsize=8)
    ax.view_init(elev=20, azim=-50)
    ax.set_title(f"Last two points of {seg_label},\nzoomed to true scale, every number labelled",
                 fontsize=9.5, pad=14)


def make_figure(case_id: int, vessel_name: str, branch_name: str, point_index: int = -1) -> None:
    trees = graph.load_trees(case_id)
    side = next(s for s, t in trees.items() if t.main_vessels(vessel_name))
    tree = trees[side]
    vessel = tree.main_vessels(vessel_name)[0]

    seg_in = next(s for s in vessel.segments[:-1] if branch_name in
                  {tree.segments[c].name for c in s.children if tree.segments[c].name != s.name})

    junction = seg_in.points[-1]
    p, q = seg_in.points[point_index - 1], seg_in.points[point_index]

    fig = plt.figure(figsize=(13, 6.0))
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    _draw_tree_3d(ax1, tree, junction)
    _draw_two_points_3d(ax2, p, q, viz.color_for(vessel_name),
                         f"{vessel_name} segment {seg_in.index}")
    fig.suptitle(f"case {case_id}, {side} tree: two points on {vessel_name}, "
                 f"near the {vessel_name}/{branch_name} junction", fontsize=11)
    fig.tight_layout(rect=(0, 0.02, 1, 0.94))
    out = paths.FIGURES / f"{case_id}_06_tree_zoom.png"
    fig.savefig(out, dpi=170, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out.relative_to(paths.REPO_ROOT)}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("case_id", nargs="?", type=int, default=1)
    ap.add_argument("--vessel", default="LAD")
    ap.add_argument("--to", dest="branch", default="D1")
    ap.add_argument("--point-index", type=int, default=-1,
                     help="index (into the incoming segment) of the second of the two points")
    args = ap.parse_args()
    make_figure(args.case_id, args.vessel, args.branch, args.point_index)


if __name__ == "__main__":
    main()
