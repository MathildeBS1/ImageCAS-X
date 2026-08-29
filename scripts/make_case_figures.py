#!/usr/bin/env python
"""Render the four walkthrough figures for one case.

    python scripts/make_case_figures.py 7

Writes figures/<case>_0{1..4}_*.png. Headless: matplotlib Agg, no display needed.
"""

from __future__ import annotations

import argparse

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from topology import coords, io, paths, viz

DPI = 150


def fig_segmentation(seg, label_map, out):
    """Three orthogonal front-face projections of the label volume."""
    table = viz.label_rgba_table(label_map)
    cmap = ListedColormap(table)
    vol, _ = viz.crop_to_foreground(seg.labels)
    sp = seg.spacing
    # (project-along axis, title, aspect from the two remaining axes' spacing)
    views = [
        (0, "sagittal  (from the left)", sp[2] / sp[1]),
        (1, "coronal  (from the front)", sp[2] / sp[0]),
        (2, "axial  (from the feet)", sp[1] / sp[0]),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.0))
    for ax, (axis, title, aspect) in zip(axes, views):
        proj = viz.first_hit_projection(vol, axis=axis)
        ax.imshow(
            np.ma.masked_equal(proj, 0).T,
            cmap=cmap, vmin=0, vmax=len(table) - 1,
            origin="lower", interpolation="nearest", aspect=aspect,
        )
        ax.set_title(title, fontsize=10)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#cccccc")
    present = [label_map[l] for l in seg.present_labels()]
    fig.legend(handles=viz.legend_handles(present), loc="lower center",
               ncol=len(present), frameon=False, fontsize=9)
    fig.suptitle(
        f"Case {seg.case_id} — segmentation: {seg.labels.shape} voxels @ "
        f"{sp.round(3)} mm, {len(present)} labelled arteries "
        f"(cropped to the arteries; the volume is mostly air)",
        fontsize=12,
    )
    fig.tight_layout(rect=[0, 0.08, 1, 0.94])
    fig.savefig(out, dpi=DPI); plt.close(fig)
    print(f"wrote {out.name}")


def fig_surface(case_id, out, target_faces=12000):
    """The lumen surface mesh, decimated so matplotlib can render it."""
    mesh = pv.read(paths.surface_path(case_id)).triangulate()
    n = mesh.n_faces
    if n > target_faces:
        mesh = mesh.decimate(1 - target_faces / n)
    pts = np.asarray(mesh.points)
    tris = mesh.faces.reshape(-1, 4)[:, 1:]

    fig = plt.figure(figsize=(15, 5.6))
    for i, (elev, azim, name) in enumerate(
        [(20, -60, "anterior-oblique"), (20, 30, "left-lateral"), (80, -90, "superior")]
    ):
        ax = fig.add_subplot(1, 3, i + 1, projection="3d")
        ax.add_collection3d(
            Poly3DCollection(pts[tris], facecolors=viz.shade_faces(pts, tris, "#c0392b"),
                             edgecolor="none")
        )
        ax.set_xlim(pts[:, 0].min(), pts[:, 0].max())
        ax.set_ylim(pts[:, 1].min(), pts[:, 1].max())
        ax.set_zlim(pts[:, 2].min(), pts[:, 2].max())
        viz.set_axes_equal(ax)
        ax.set_box_aspect((1, 1, 1), zoom=1.45)
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(name, fontsize=10)
        ax.set_axis_off()
    fig.suptitle(
        f"Case {case_id} — lumen surface mesh ({n:,} triangles, "
        f"shown decimated to {tris.shape[0]:,})", fontsize=12,
    )
    fig.tight_layout()
    fig.savefig(out, dpi=DPI); plt.close(fig)
    print(f"wrote {out.name}")


def fig_centerline(cls, out):
    """The tree as a tree: polylines coloured by artery, topology points marked."""
    fig = plt.figure(figsize=(15, 6.4))
    names_seen = []
    for i, (elev, azim, title) in enumerate(
        [(20, -60, "anterior-oblique"), (20, 30, "left-lateral"), (80, -90, "superior")]
    ):
        ax = fig.add_subplot(1, 3, i + 1, projection="3d")
        for cl in cls.values():
            for poly in cl.lines:
                pts = cl.points[poly]
                name = str(cl.segment_name[poly[len(poly) // 2]])
                names_seen.append(name)
                ax.plot(*pts.T, color=viz.color_for(name), lw=2.0)
            for flag, marker, size, edge in [
                ("branch_points", "o", 34, "black"),
                ("end_points", "^", 26, "#444444"),
                ("start_points", "*", 150, "black"),
            ]:
                sel = np.asarray(getattr(cl, flag)) != 0
                if sel.any():
                    ax.scatter(*cl.points[sel].T, marker=marker, s=size,
                               c="white", edgecolors=edge, linewidths=1.0, depthshade=False, zorder=5)
        viz.set_axes_equal(ax)
        ax.set_box_aspect((1, 1, 1), zoom=1.45)
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(title, fontsize=10)
        ax.set_axis_off()

    from matplotlib.lines import Line2D
    topo = [
        Line2D([0], [0], marker="*", color="w", markerfacecolor="w", markeredgecolor="k",
               markersize=14, label="ostium (start)"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="w", markeredgecolor="k",
               markersize=8, label="bifurcation"),
        Line2D([0], [0], marker="^", color="w", markerfacecolor="w", markeredgecolor="#444",
               markersize=8, label="terminus"),
    ]
    fig.legend(handles=viz.legend_handles(names_seen) + topo, loc="lower center",
               ncol=9, frameon=False, fontsize=9)
    n_branch = sum(int((np.asarray(c.branch_points) != 0).sum()) for c in cls.values())
    n_end = sum(int((np.asarray(c.end_points) != 0).sum()) for c in cls.values())
    case_id = next(iter(cls.values())).case_id
    fig.suptitle(
        f"Case {case_id} — centerline tree: {len(set(names_seen))} named segments, "
        f"{n_branch} bifurcations, {n_end} termini", fontsize=12,
    )
    fig.tight_layout(rect=[0, 0.08, 1, 0.96])
    fig.savefig(out, dpi=DPI); plt.close(fig)
    print(f"wrote {out.name}")


def fig_overlay(seg, cls, case_id, out, stride=12):
    """All three representations in one frame -- the alignment proof."""
    mesh = pv.read(paths.surface_path(case_id)).triangulate()
    if mesh.n_faces > 9000:
        mesh = mesh.decimate(1 - 9000 / mesh.n_faces)
    spts = np.asarray(mesh.points)
    tris = mesh.faces.reshape(-1, 4)[:, 1:]

    fg = np.argwhere(seg.labels > 0)[::stride]
    fg_lps = coords.voxel_to_lps(fg, seg.affine)

    fig = plt.figure(figsize=(15, 6.4))
    for i, (elev, azim, title) in enumerate(
        [(20, -60, "anterior-oblique"), (20, 30, "left-lateral"), (12, -15, "close view")]
    ):
        ax = fig.add_subplot(1, 3, i + 1, projection="3d")
        ax.scatter(*fg_lps.T, s=1.2, c="#b8c4d0", alpha=0.28, depthshade=False,
                   linewidths=0, label="segmentation voxels")
        ax.add_collection3d(
            Poly3DCollection(spts[tris], facecolor="#d98880", edgecolor="none", alpha=0.28)
        )
        for cl in cls.values():
            for poly in cl.lines:
                pts = cl.points[poly]
                name = str(cl.segment_name[poly[len(poly) // 2]])
                ax.plot(*pts.T, color=viz.color_for(name), lw=2.2)
        ax.set_xlim(spts[:, 0].min(), spts[:, 0].max())
        ax.set_ylim(spts[:, 1].min(), spts[:, 1].max())
        ax.set_zlim(spts[:, 2].min(), spts[:, 2].max())
        viz.set_axes_equal(ax)
        ax.set_box_aspect((1, 1, 1), zoom=1.45)
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(title, fontsize=10)
        ax.set_axis_off()

    from matplotlib.patches import Patch
    fig.legend(
        handles=[
            Patch(facecolor="#b8c4d0", label="segmentation voxels (NIfTI, RAS → LPS)"),
            Patch(facecolor="#d98880", label="lumen surface (VTK, LPS)"),
            Patch(facecolor="#2f6fd0", label="centerlines (VTK, LPS), coloured by artery"),
        ],
        loc="lower center", ncol=3, frameon=False, fontsize=10,
    )
    fig.suptitle(
        f"Case {case_id} — the three representations overlaid; "
        "agreement here is the proof the RAS→LPS conversion is correct", fontsize=12,
    )
    fig.tight_layout(rect=[0, 0.06, 1, 0.96])
    fig.savefig(out, dpi=DPI); plt.close(fig)
    print(f"wrote {out.name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case_id", type=int, nargs="?", default=7)
    args = ap.parse_args()
    cid = args.case_id

    if not paths.has_all_files(cid):
        raise SystemExit(f"case {cid} is missing one or more files")

    d = paths.descriptors().loc[cid]
    print(f"Case {cid}: quality={d['Image Quality']}, dominance={d['Dominance']}, "
          f"disease={d['Disease']}")

    out_dir = paths.FIGURES
    out_dir.mkdir(exist_ok=True)
    label_map = viz.load_label_map()
    seg = io.load_segmentation(cid)
    cls = io.load_centerlines(cid)

    fig_segmentation(seg, label_map, out_dir / f"{cid}_01_segmentation.png")
    fig_surface(cid, out_dir / f"{cid}_02_surface.png")
    fig_centerline(cls, out_dir / f"{cid}_03_centerline.png")
    fig_overlay(seg, cls, cid, out_dir / f"{cid}_04_overlay.png")


if __name__ == "__main__":
    main()
