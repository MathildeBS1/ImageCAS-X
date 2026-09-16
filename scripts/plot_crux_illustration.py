"""Figure: what "the CRUX segment" actually is -- one real right-dominant case's RCA
splitting into R-PDA and R-PLA, with the 3 mm window scripts/bifurcation_volume.py
integrates volume over marked on the thicker ("main") branch.

Answers a question that came up discussing the +17.1% CRUX result: that number is not the
RCA getting bigger. It is a short window on one of its two daughters, right past the split.
This draws the real anatomy so the two are not confused for each other.

    uv run python scripts/plot_crux_illustration.py [case_id]

Writes figures/crux_illustration.{pdf,png}.
"""

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

from topology import angles, graph, paths

CORE_SCALE, WINDOW_MM = 1.0, 3.0
INK = "#1f2933"
TRUNK = "#7b8794"
MAIN = "#d83d29"
SIDE = "#2a78d6"
WINDOW = "#f4b942"


def _pick_case(preferred: int | None):
    desc = paths.descriptors()
    if preferred is not None:
        ids = [preferred]
    else:
        ids = paths.usable_ids()
    best = None
    for cid in ids:
        dominance = desc.loc[cid, "Dominance"] if cid in desc.index else None
        if dominance != "R":
            continue
        try:
            trees = graph.load_trees(cid)
            bs = angles.extract_trees(trees["left"], trees["right"], dominance, CORE_SCALE, WINDOW_MM)
        except Exception:
            continue
        crux = next((b for b in bs if b.named == "CRUX"), None)
        if crux is None or crux.main is None or crux.side_br is None or crux.parent is None:
            continue
        if crux.main.segment is None or crux.side_br.segment is None or crux.parent.segment is None:
            continue
        tree = trees[crux.side]
        main_seg, side_seg = tree.segments[crux.main.segment], tree.segments[crux.side_br.segment]
        main_len = tree.vessel_of(main_seg).shaft(main_seg, upstream=False)[0]
        side_len = tree.vessel_of(side_seg).shaft(side_seg, upstream=False)[0]
        score = min(len(main_len), len(side_len))  # prefer branches long enough to read clearly
        if best is None or score > best[0]:
            best = (score, cid, trees, crux)
        if preferred is not None:
            break
    if best is None:
        raise SystemExit("no right-dominant case with a measurable CRUX found")
    return best[1], best[2], best[3]


def _trunk_points(tree, parent_segment_index):
    seg = tree.segments[parent_segment_index]
    vessel = tree.vessel_of(seg)
    return vessel.points_from(vessel.segments[0])


def _best_fit_plane(points):
    centroid = points.mean(axis=0)
    _u, _s, vt = np.linalg.svd(points - centroid, full_matrices=False)
    return lambda pts: (pts - centroid) @ vt[:2].T


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case", nargs="?", type=int, default=None, help="case id; default: search for a clear example")
    args = parser.parse_args()

    case_id, trees, crux = _pick_case(args.case)
    tree = trees[crux.side]
    main_seg = tree.segments[crux.main.segment]
    side_seg = tree.segments[crux.side_br.segment]
    trunk = _trunk_points(tree, crux.parent.segment)
    main_pts, main_rad = tree.vessel_of(main_seg).shaft(main_seg, upstream=False)
    side_pts, _side_rad = tree.vessel_of(side_seg).shaft(side_seg, upstream=False)

    core = CORE_SCALE * float(main_rad[0])
    lo, hi, reason = graph.shaft_window(main_pts, core, WINDOW_MM)
    main_name = main_seg.name  # "R-PDA" or "R-PLA", whichever is thicker in this case
    side_name = side_seg.name

    project = _best_fit_plane(np.concatenate([trunk, main_pts, side_pts]))
    trunk2d, main2d, side2d = project(trunk), project(main_pts), project(side_pts)
    node2d = project(crux.position[None, :])[0]

    fig, ax = plt.subplots(figsize=(6.2, 6.2))
    ax.plot(*trunk2d.T, color=TRUNK, lw=3.0, solid_capstyle="round", label="RCA (trunk)")
    ax.plot(*main2d.T, color=MAIN, lw=2.4, solid_capstyle="round", label=f"{main_name} (thicker: “main”)")
    ax.plot(*side2d.T, color=SIDE, lw=2.0, solid_capstyle="round", label=f"{side_name} (thinner: “side”)")
    if not reason and hi - lo >= 2:
        ax.plot(*main2d[lo:hi].T, color=WINDOW, lw=6.0, alpha=0.75, solid_capstyle="butt", zorder=1,
                label=f"{WINDOW_MM:.0f} mm window: this is what “CRUX volume” measures")
    ax.plot(*node2d, "o", color=INK, ms=8, zorder=5)
    ax.annotate("crux\n(RCA splits here)", node2d, textcoords="offset points", xytext=(10, -18),
                fontsize=9, color=INK)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"case {case_id}: the CRUX measurement is a {WINDOW_MM:.0f} mm window on one\n"
                 f"branch past the split, not the RCA trunk", fontsize=10.5, color=INK)
    ax.legend(fontsize=8, loc="upper left", frameon=False)
    fig.tight_layout()

    out_dir = os.path.join(os.path.dirname(__file__), "..", "figures")
    os.makedirs(out_dir, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(out_dir, f"crux_illustration.{ext}"), dpi=300, bbox_inches="tight")
    print(f"wrote figures/crux_illustration.{{pdf,png}}  (case {case_id}, main={main_name}, side={side_name})")


if __name__ == "__main__":
    main()
