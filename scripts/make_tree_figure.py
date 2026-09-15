#!/usr/bin/env python
"""Figure: the centerline as anatomy, and the same centerline as a rooted tree.

The point of the figure is that the second panel is *derived*, not drawn by hand:
the dendrogram is exactly what ``topology.graph`` hands to the feature code, with
distance from the ostium (mm) as the vertical axis, so segment lengths, branching
order and generation depth can all be read off it.

Usage:  python scripts/make_tree_figure.py [7 21 ...]
"""

from __future__ import annotations

import argparse

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from topology import angles, graph, paths, viz


def layout(tree: graph.CoronaryTree) -> tuple[dict[int, float], dict[int, float]]:
    """Dendrogram coordinates: x spreads the leaves out, y is mm from the ostium."""
    x: dict[int, float] = {}
    leaf = 0.0
    for seg in tree.walk():  # pre-order keeps sibling subtrees from crossing
        if seg.is_terminal:
            x[seg.index] = leaf
            leaf += 1.0
    for seg in reversed(tree.segments):  # children always have a higher index
        if seg.children:
            x[seg.index] = float(np.mean([x[c] for c in seg.children]))

    y0: dict[int, float] = {}
    for seg in tree.walk():
        y0[seg.index] = 0.0 if seg.parent is None else y0[seg.parent] + tree.segments[seg.parent].length
    return x, y0


def draw_dendrogram(ax, tree: graph.CoronaryTree) -> None:
    x, y0 = layout(tree)
    for seg in tree.segments:
        c = viz.color_for(seg.name)
        y1 = y0[seg.index] + seg.length
        ax.plot([x[seg.index]] * 2, [y0[seg.index], y1], color=c, lw=2.6, solid_capstyle="round")
        if seg.parent is not None:  # elbow across to the parent's stem
            ax.plot([x[seg.parent], x[seg.index]], [y0[seg.index]] * 2, color=c, lw=1.4, alpha=0.8)
        if seg.children:
            ax.plot([x[seg.index]], [y1], "o", color=c, ms=4.5, mec="white", mew=0.8, zorder=3)
        else:
            ax.text(x[seg.index], y1 + 3, seg.name, ha="center", va="top", fontsize=6.5,
                    color=c, rotation=90, clip_on=False)
    for r in tree.roots:
        ax.plot([x[s.index] for s in tree.segments if s.start_node == r][:1], [0], "s",
                color="black", ms=5, zorder=4)

    ax.set_ylabel("distance from ostium (mm)")
    ax.set_xticks([])
    for spine in ("top", "right", "bottom"):
        ax.spines[spine].set_visible(False)
    ax.margins(x=0.08, y=0.12)


def draw_anatomy(ax, trees: dict[str, graph.CoronaryTree], case_id: int) -> None:
    """Coronal view: LPS x (patient left) against z (superior).

    Also marks the 5 target bifurcations from ``topology.angles`` with their
    measured angle, so a wrong-vector bug shows up on the figure directly rather
    than only as a CSV number.
    """
    for tree in trees.values():
        for seg in tree.segments:
            p = seg.points
            ax.plot(p[:, 0], p[:, 2], color=viz.color_for(seg.name), lw=1.8, solid_capstyle="round")
        for node in tree.nodes.values():
            style = {"ostium": ("s", 7, "black"), "bifurcation": ("o", 4, "#333333"),
                     "pass-through": ("o", 3, "#999999"), "terminus": (".", 3.5, "#666666")}[node.kind]
            ax.plot(node.position[0], node.position[2], style[0], ms=style[1],
                    color=style[2], mec="white", mew=0.6, zorder=3)

    for bif_name, result in angles.extract_case(case_id).items():
        if result.position is None:
            continue
        x, z = result.position[0], result.position[2]
        ax.plot(x, z, "*", ms=11, color="#d62728", mec="white", mew=0.6, zorder=4)
        ax.annotate(f"{bif_name}\n{result.angle_deg:.0f}°", (x, z), xytext=(5, 5),
                    textcoords="offset points", fontsize=6.5, color="#d62728", zorder=4)

    ax.set_aspect("equal")
    ax.invert_xaxis()  # +x is patient-left, so flip for a face-on view
    ax.set_xlabel("LPS x (mm)")
    ax.set_ylabel("LPS z (mm)")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def make_figure(case_id: int) -> None:
    trees = graph.load_trees(case_id)
    fig = plt.figure(figsize=(13, 6.4))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.5, 1, 1], wspace=0.28,
                          left=0.06, right=0.98, top=0.86, bottom=0.11)

    draw_anatomy(fig.add_subplot(gs[0, 0]), trees, case_id)
    # One depth scale for both sides, so the two trees are directly comparable.
    depth = max(max((y + s.length for s, y in zip(t.segments, layout(t)[1].values())), default=1)
                for t in trees.values())
    dendro_axes = []
    for col, side in ((1, "left"), (2, "right")):
        tree = trees[side]
        ax = fig.add_subplot(gs[0, col])
        dendro_axes.append(ax)
        draw_dendrogram(ax, tree)
        ax.set_ylim(depth * 1.12, -depth * 0.04)
        note = "" if tree.is_single_tree else f"  ({len(tree.roots)} ostia)" if len(tree.roots) > 1 else "  (cycle)"
        ax.set_title(f"{side} tree{note}\n{len(tree.segments)} segments, "
                     f"{len(tree.bifurcations())} bifurcations, {tree.total_length:.0f} mm",
                     fontsize=9)

    names = {s.name for t in trees.values() for s in t.segments}
    dendro_axes[1].set_ylabel("")
    fig.legend(handles=viz.legend_handles(names), loc="lower center", ncol=len(names),
               frameon=False, fontsize=8, bbox_to_anchor=(0.5, 0.0))
    warn = [w for t in trees.values() for w in t.warnings]
    fig.suptitle(f"case {case_id} — centerline and derived rooted tree"
                 + (f"\n{'; '.join(warn)}" if warn else ""), fontsize=11)
    out = paths.FIGURES / f"{case_id}_05_tree.png"
    fig.savefig(out, dpi=170, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out.relative_to(paths.REPO_ROOT)}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cases", nargs="*", type=int, default=[7, 21])
    for cid in ap.parse_args().cases:
        make_figure(cid)


if __name__ == "__main__":
    main()
