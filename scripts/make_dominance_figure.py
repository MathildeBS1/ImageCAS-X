#!/usr/bin/env python
"""Right- vs left-dominant hearts, side by side.

Dominance is the single most important topological variant in the coronary tree:
whichever artery reaches the crux and gives off the posterior descending branch is
"dominant". The dataset encodes this twice over -- as a Dominance column in
Descriptors.xlsx, and implicitly in which segment labels exist -- and the two agree.

    python scripts/make_dominance_figure.py
"""

from __future__ import annotations

import argparse

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from topology import io, paths, viz

DPI = 150


def draw(ax, cls, elev=18, azim=-62):
    names = []
    for cl in cls.values():
        for poly in cl.lines:
            pts = cl.points[poly]
            name = str(cl.segment_name[poly[len(poly) // 2]])
            names.append(name)
            ax.plot(*pts.T, color=viz.color_for(name), lw=2.2)
        sel = np.asarray(cl.start_points) != 0
        if sel.any():
            ax.scatter(*cl.points[sel].T, marker="*", s=170, c="white",
                       edgecolors="black", linewidths=1.0, depthshade=False, zorder=5)
    viz.set_axes_equal(ax)
    ax.set_box_aspect((1, 1, 1), zoom=1.9)
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--right", type=int, default=7, help="a right-dominant case")
    ap.add_argument("--left", type=int, default=45, help="a left-dominant case")
    args = ap.parse_args()

    desc = paths.descriptors()
    fig = plt.figure(figsize=(13, 5.6))
    all_names = []
    panels = [
        (args.right, "Right-dominant", "RCA reaches the crux and supplies\nR-PDA + R-PLA"),
        (args.left, "Left-dominant", "RCA is short; the circumflex supplies\nL-PDA + L-PLA instead"),
    ]
    for i, (cid, title, blurb) in enumerate(panels):
        ax = fig.add_subplot(1, 2, i + 1, projection="3d")
        cls = io.load_centerlines(cid)
        all_names += draw(ax, cls)
        segs = sorted({str(n) for cl in cls.values() for n in cl.segment_name})
        ax.set_title(
            f"{title} — case {cid}  (Dominance = {desc.loc[cid, 'Dominance']})\n{blurb}\n"
            f"segments: {', '.join(segs)}",
            fontsize=10, linespacing=1.5,
        )

    fig.legend(handles=viz.legend_handles(all_names), loc="lower center",
               ncol=8, frameon=False, fontsize=9)
    fig.suptitle(
        "Coronary dominance, the dataset's central topological variant\n"
        "★ marks each ostium. Same colour scheme; only the posterior supply differs.",
        fontsize=12,
    )
    out = paths.FIGURES / "05_dominance_comparison.png"
    fig.tight_layout(rect=[0, 0.10, 1, 0.87])
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"wrote {out.name}")


if __name__ == "__main__":
    main()
