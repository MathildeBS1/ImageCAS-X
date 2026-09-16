"""Figure: the shaft window scripts/bifurcation_volume.py integrates over, drawn on real
bifurcation geometry. Colors mark the three zones graph.shaft_window carves out of each
daughter: the excluded core near the junction, the 3 mm window the frustum volume is summed
over, and the rest of the vessel beyond it. The incoming parent vessel is drawn for context
only, not colored by zone, since volume is never read from it.

One healthy and one diseased example is drawn for each of the three named bifurcations whose
local main-daughter volume actually separates diseased from healthy after Benjamini-Hochberg
correction (bifurcation_volume.tex: CRUX, LCX-OM1, LAD-D1). LM and LAD-D2 are left out because
they did not survive correction there. Each example is the real case in the cohort closest to
its own group's median main-daughter volume at that bifurcation, the matching rule
scripts/plot_volume_example.py already uses for CRUX alone.

    uv run python scripts/plot_bifurcation_window.py

Writes figures/bifurcation_window.{pdf,png}.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from topology import angles, graph, paths

CORE_SCALE, WINDOW_MM = 1.0, 3.0
CONTEXT_MM = 8.0  # how far past the window (or before the junction, for the parent) to draw

# healthy/diseased median main-daughter volume, mm^3, from bifurcation_volume.tex's table.
TARGETS = {
    "CRUX": {"no": 6.74, "yes": 7.78},
    "LCX-OM1": {"no": 7.59, "yes": 8.45},
    "LAD-D1": {"no": 10.80, "yes": 10.02},
}

COLORS = {"core": "#b0b7bf", "window": "#2a78d6", "beyond": "#cfd8e3", "parent": "#7b8794"}


def _walk(tree, seg, upstream, max_mm):
    points, radii = tree.vessel_of(seg).shaft(seg, upstream=upstream)
    arc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(points, axis=0), axis=1))])
    n = min(int(np.searchsorted(arc, max_mm, side="right")) + 1, len(points))
    return points[:n], radii[:n]


def _find_bifurcation(case_id, named):
    desc = paths.descriptors()
    dominance = desc.loc[case_id, "Dominance"] if case_id in desc.index else None
    dominance = dominance if isinstance(dominance, str) else None
    trees = graph.load_trees(case_id)
    bs = angles.extract_trees(trees["left"], trees["right"], dominance, CORE_SCALE, WINDOW_MM)
    b = next(b for b in bs if b.named == named)
    return trees[b.side], b


def _main_daughter_volume(tree, b):
    seg = tree.segments[b.main.segment]
    points, radii = tree.vessel_of(seg).shaft(seg, upstream=False)
    core = CORE_SCALE * float(radii[0])
    lo, hi, reason = graph.shaft_window(points, core, WINDOW_MM)
    if reason or hi - lo < 2:
        return None
    pts, rad = points[lo:hi], radii[lo:hi]
    ds = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    r0, r1 = rad[:-1], rad[1:]
    return float(np.sum((np.pi / 3.0) * ds * (r0**2 + r0 * r1 + r1**2)))


def _pick_examples(named, ids, desc):
    """{'no': case_id, 'yes': case_id} closest to TARGETS[named] for that disease group."""
    volumes = {"no": [], "yes": []}
    for cid in ids:
        disease = desc.loc[cid, "Disease"] if cid in desc.index else None
        if disease not in ("no", "yes"):
            continue
        dominance = desc.loc[cid, "Dominance"] if cid in desc.index else None
        dominance = dominance if isinstance(dominance, str) else None
        try:
            trees = graph.load_trees(cid)
            bs = angles.extract_trees(trees["left"], trees["right"], dominance, CORE_SCALE, WINDOW_MM)
        except Exception:
            continue
        b = next((x for x in bs if x.named == named and x.main is not None
                  and x.main.segment is not None), None)
        if b is None:
            continue
        volume = _main_daughter_volume(trees[b.side], b)
        if volume is not None:
            volumes[disease].append((cid, volume))
    return {disease: min(vals, key=lambda cv: abs(cv[1] - TARGETS[named][disease]))[0]
            for disease, vals in volumes.items()}


def _segment_colors(n_segments, lo, hi):
    """One color per point-to-point segment: core (before the window), window (what the frustum
    sum uses, pts[lo:hi]), beyond (after it)."""
    colors = []
    for i in range(n_segments):
        if i < lo:
            colors.append(COLORS["core"])
        elif i <= hi - 2:
            colors.append(COLORS["window"])
        else:
            colors.append(COLORS["beyond"])
    return colors


def _add_branch(ax, points, radii, lo, hi, label):
    segs = np.stack([points[:-1], points[1:]], axis=1)
    colors = _segment_colors(len(segs), lo, hi)
    widths = 4.0 * (radii[:-1] + radii[1:])  # scale with local caliber
    lc = Line3DCollection(segs, colors=colors, linewidths=widths, capstyle="round")
    ax.add_collection3d(lc)
    if label and hi > lo:
        mid = points[(lo + hi) // 2]
        ax.text(*mid, f"  {label}", fontsize=6.5, color=COLORS["window"])


def _draw(ax, case_id, named):
    tree, b = _find_bifurcation(case_id, named)

    context_parts = []
    if b.parent.segment is not None:
        ppoints, pradii = _walk(tree, tree.segments[b.parent.segment], upstream=True, max_mm=CONTEXT_MM)
        segs = np.stack([ppoints[:-1], ppoints[1:]], axis=1)
        widths = 4.0 * (pradii[:-1] + pradii[1:])
        ax.add_collection3d(Line3DCollection(segs, colors=COLORS["parent"], linewidths=widths))
        context_parts.append(ppoints)

    for branch, label in ((b.main, "main"), (b.side_br, "side")):
        points, radii = _walk(tree, tree.segments[branch.segment], upstream=False,
                               max_mm=CONTEXT_MM + WINDOW_MM)
        core = CORE_SCALE * float(radii[0])
        lo, hi, reason = graph.shaft_window(points, core, WINDOW_MM)
        _add_branch(ax, points, radii, lo, hi, label if not reason else None)
        context_parts.append(points[:30])

    ax.scatter(*b.position, color="black", s=25, zorder=5)

    all_pts = np.concatenate(context_parts)
    center = all_pts.mean(axis=0)
    span = np.abs(all_pts - center).max() * 1.15
    ax.set_xlim(center[0] - span, center[0] + span)
    ax.set_ylim(center[1] - span, center[1] + span)
    ax.set_zlim(center[2] - span, center[2] + span)
    ax.set_xticklabels([]); ax.set_yticklabels([]); ax.set_zticklabels([])


def main():
    ids = paths.usable_ids()
    desc = paths.descriptors()

    fig = plt.figure(figsize=(7.5, 10.5))
    labels = {"no": "healthy", "yes": "diseased"}
    for row, named in enumerate(TARGETS):
        examples = _pick_examples(named, ids, desc)
        for col, disease in enumerate(("no", "yes")):
            ax = fig.add_subplot(3, 2, row * 2 + col + 1, projection="3d")
            case_id = examples[disease]
            _draw(ax, case_id, named)
            ax.set_title(f"{named}, {labels[disease]} (case {case_id})", fontsize=9)

    handles = [
        plt.Line2D([0], [0], color=COLORS["parent"], lw=3, label="parent vessel (context)"),
        plt.Line2D([0], [0], color=COLORS["core"], lw=3,
                   label="core, excluded (within 1 daughter radius of the junction)"),
        plt.Line2D([0], [0], color=COLORS["window"], lw=3,
                   label="window, integrated (3 mm past the core)"),
        plt.Line2D([0], [0], color=COLORS["beyond"], lw=3, label="beyond the window (context only)"),
    ]
    fig.legend(handles=handles, fontsize=8, loc="lower center", ncol=2, bbox_to_anchor=(0.5, 0.0))
    fig.suptitle("The three bifurcations whose local main-daughter volume separates\n"
                 "diseased from healthy after FDR correction, one real example each",
                 fontsize=10.5)
    fig.tight_layout(rect=[0, 0.06, 1, 0.95])

    out_dir = os.path.join(os.path.dirname(__file__), "..", "figures")
    os.makedirs(out_dir, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(out_dir, f"bifurcation_window.{ext}"), dpi=300, bbox_inches="tight")
    print("wrote figures/bifurcation_window.{pdf,png}")


if __name__ == "__main__":
    main()
