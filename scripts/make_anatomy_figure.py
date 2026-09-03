#!/usr/bin/env python
"""Annotated axial CT slice for the clinical background chapter.

An axial slice through the aortic root with the delivered coronary segmentation overlaid, so
the anatomy section shows the reader the real modality rather than a schematic.

The coronary ostium marker is **derived from the data, not placed by eye**: the centerline's
``start_points`` flag gives the ostium in LPS millimetres, and ``coords.lps_to_voxel`` puts it
on the image grid. Everything else on the figure -- the chamber labels -- is placed by hand
after looking at the rendered slice, because nothing in this dataset segments the chambers.

Usage:  python scripts/make_anatomy_figure.py [--case 7] [--slice-offset 0]

matplotlib/Agg only: the login node has no DISPLAY and the repo does not render with VTK.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np

from topology import coords, io, paths, viz

# Structures annotated on case 7's ostium slice, as (label, row, col) in the rotated display
# grid, read off the rendered image.
#
# Only the aortic root is labelled. This slice sits at the level of the coronary ostia, which
# is *not* a four-chamber level: the ventricles are not both sectioned here, and nothing in
# this dataset segments the chambers, so labelling them would be guesswork. Naming only what
# the image unambiguously shows is the honest version of this figure.
CASE7_STRUCTURES = [
    ("ascending aorta", 241, 164),
]

WINDOW = (-100, 700)  # HU display window: wide enough for contrast, soft tissue and fat


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", type=int, default=7)
    ap.add_argument("--slice-offset", type=int, default=0,
                    help="axial slices away from the ostium slice; use to hunt a better level")
    ap.add_argument("--no-labels", action="store_true",
                    help="render without chamber labels, for deciding where they go")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    cid = args.case
    vol_path = paths.volume_path(cid)
    if not vol_path.exists():
        raise SystemExit(f"no CT volume for case {cid}: {vol_path}")

    img = nib.load(str(vol_path))
    seg = io.load_segmentation(cid)

    # Ostium, straight from the ground truth.
    cl = io.load_centerline(cid, "left")
    ostium_lps = cl.points[cl.start_points.astype(bool)]
    ostium_ijk = coords.lps_to_voxel(ostium_lps, img.affine)[0]
    k = int(ostium_ijk[2]) + args.slice_offset

    ct = np.asarray(img.dataobj[:, :, k], dtype=np.float32)
    labels = seg.labels[:, :, k]

    # Radiological convention: anterior at the top. np.rot90 maps a voxel (i, j) of an
    # (M, N) array to display column i and display row N-1-j, so capture N before rotating.
    n_cols = ct.shape[1]
    ct = np.rot90(ct)
    labels = np.rot90(labels)
    oi = int(ostium_ijk[0])
    oj = n_cols - 1 - int(ostium_ijk[1])

    fig, ax = plt.subplots(figsize=(7.2, 7.2))
    lo, hi = WINDOW
    ax.imshow(np.clip(ct, lo, hi), cmap="gray", vmin=lo, vmax=hi, interpolation="bilinear")

    # Coronary segmentation overlay, in the shared artery colours.
    label_map = viz.load_label_map()
    table = viz.label_rgba_table(label_map, alpha=0.95)
    rgba = table[np.clip(labels, 0, len(table) - 1)]
    rgba[labels == 0, 3] = 0.0
    ax.imshow(rgba, interpolation="nearest")

    ax.annotate(
        "left coronary ostium", xy=(oi, oj), xytext=(oi + 70, oj + 55),
        color="#ffd400", fontsize=10, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#ffd400", lw=1.6),
    )

    if not args.no_labels and cid == 7:
        for name, row, col in CASE7_STRUCTURES:
            ax.text(col, row, name, color="white", fontsize=11, fontweight="bold",
                    ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.22", fc="black", ec="none", alpha=0.5))

    # Legend for the arteries actually present on this slice, in the shared colours.
    present = [label_map[l] for l in np.unique(labels) if l in label_map]
    if present:
        ax.legend(handles=viz.legend_handles(present), loc="lower left", frameon=True,
                  facecolor="black", edgecolor="none", labelcolor="white", fontsize=10)

    ax.set_axis_off()
    fig.tight_layout(pad=0.2)

    out = args.out or str(paths.REPO_ROOT / "figures" / "anatomy_ct.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="black")
    plt.close(fig)
    print(f"case {cid}  slice k={k}  ostium voxel={ostium_ijk.tolist()}  "
          f"HU={int(img.dataobj[tuple(ostium_ijk)])}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
