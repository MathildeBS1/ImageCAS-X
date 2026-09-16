"""Figure: two real CRUX main-daughter branches, one healthy and one diseased, chosen close
to each group's median local branch volume from bifurcation_volume.tex's Table 1 (healthy
6.74 mm^3, diseased 7.78 mm^3, n_h=400, n_d=371). Draws each branch as a lumen radius profile,
radius(s) mirrored above and below the centerline, over the same shaft window
scripts/bifurcation_volume.py integrates the frustum volume over -- so the shaded area is a
direct 2D read of the printed volume difference, not a separate rendering choice.

    uv run python scripts/plot_volume_example.py

Writes figures/volume_example.{pdf,png}.
"""

import os

import matplotlib.pyplot as plt
import numpy as np

from topology import angles, graph, paths

CORE_SCALE, WINDOW_MM = 1.0, 3.0
TARGET = {"no": 6.74, "yes": 7.78}


def _crux_branches():
    desc = paths.descriptors()
    out = []
    for cid in paths.usable_ids():
        disease = desc.loc[cid, "Disease"] if cid in desc.index else None
        if disease not in ("yes", "no"):
            continue
        dominance = desc.loc[cid, "Dominance"] if cid in desc.index else None
        dominance = dominance if isinstance(dominance, str) else None
        try:
            trees = graph.load_trees(cid)
            bs = angles.extract_trees(trees["left"], trees["right"], dominance, CORE_SCALE, WINDOW_MM)
        except Exception:
            continue
        for b in bs:
            if b.named != "CRUX" or b.main is None or b.main.segment is None:
                continue
            tree = trees[b.side]
            points, radii = tree.vessel_of(tree.segments[b.main.segment]).shaft(
                tree.segments[b.main.segment], upstream=False)
            if radii is None:
                continue
            core = CORE_SCALE * float(radii[0])
            lo, hi, reason = graph.shaft_window(points, core, WINDOW_MM)
            if reason or hi - lo < 2:
                continue
            pts, rad = points[lo:hi], radii[lo:hi]
            ds = np.linalg.norm(np.diff(pts, axis=0), axis=1)
            r0, r1 = rad[:-1], rad[1:]
            volume = float(np.sum((np.pi / 3.0) * ds * (r0**2 + r0 * r1 + r1**2)))
            arc = np.concatenate([[0.0], np.cumsum(ds)])
            out.append({"case_id": cid, "disease": disease, "volume": volume, "arc": arc, "radius": rad})
    return out


def main():
    branches = _crux_branches()
    example = {}
    for disease, target in TARGET.items():
        pool = [b for b in branches if b["disease"] == disease]
        example[disease] = min(pool, key=lambda b: abs(b["volume"] - target))

    rmax = max(b["radius"].max() for b in example.values())
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.1), sharey=True)
    labels = {"no": "healthy", "yes": "diseased"}
    colors = {"no": "#2a78d6", "yes": "#d83d29"}
    for ax, disease in zip(axes, ("no", "yes")):
        b = example[disease]
        ax.fill_between(b["arc"], -b["radius"], b["radius"], color=colors[disease], alpha=0.35)
        ax.plot(b["arc"], b["radius"], color=colors[disease], lw=1.5)
        ax.plot(b["arc"], -b["radius"], color=colors[disease], lw=1.5)
        ax.axhline(0, color="#7b8794", lw=0.6, zorder=0)
        ax.set_title(f"{labels[disease]}, case {b['case_id']}\nvolume = {b['volume']:.2f} mm$^3$",
                     fontsize=9.5)
        ax.set_xlabel("arc length past bifurcation core (mm)", fontsize=8.5)
        ax.set_ylim(-1.15 * rmax, 1.15 * rmax)
    axes[0].set_ylabel("lumen radius (mm)", fontsize=8.5)
    fig.suptitle("CRUX main daughter, two cases matched to each group's median volume:\n"
                 "shaded area is the frustum volume the disease-vs-healthy test compares",
                 fontsize=9.5)
    fig.tight_layout()

    out_dir = os.path.join(os.path.dirname(__file__), "..", "figures")
    os.makedirs(out_dir, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(out_dir, f"volume_example.{ext}"), dpi=300, bbox_inches="tight")
    print(f"wrote figures/volume_example.{{pdf,png}}")
    for disease in ("no", "yes"):
        b = example[disease]
        print(f"  {labels[disease]}: case {b['case_id']}, volume={b['volume']:.3f} mm^3 "
              f"(target {TARGET[disease]})")


if __name__ == "__main__":
    main()
