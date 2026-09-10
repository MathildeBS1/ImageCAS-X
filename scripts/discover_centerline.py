"""Explore the centerline graph of a case.

Files: <scan>.coronary_{left,right}_centerline.vtk. This script covers the
*structure*; the geometry it enables is in discover_tortuosity.py.

The file is a graph, not a list of vessels. All line cells index one shared
point array, so a point ID is already a graph node and two cells meeting at a
bifurcation join automatically. A cell is an edge, not an artery -- a single
cell can span two segment labels, because the label changes at the branch
point. Cell orientation is arbitrary
(`utils/precompute_centerline_samples.py:11-13`), so proximal-to-distal order
comes only from a traversal rooted at the `start_points` flag.

    uv run python scripts/discover_centerline.py images/1
    uv run python scripts/discover_centerline.py images/1 --side right

With the mask beside it, it also checks that the points land inside the lumen,
which doubles as a check that the LPS convention was applied correctly.
"""

import argparse
import os

import numpy as np

from discover_common import (case_files, orient_edges, read_centerline, resolve,
                             segment_names, segment_paths, tip_paths)


def report_structure(centerline, oriented, root, path):
    points, edges = centerline["points"], centerline["edges"]
    names = segment_names()

    print(f"\n== {os.path.basename(path)}")
    with open(path, "rb") as handle:
        encoding = handle.read(200).split(b"\n")[2].decode().strip()
    print(f"   {os.path.getsize(path) / 1e3:.1f} KB on disk, {encoding} encoding")

    print("\n-- graph")
    print(f"  {len(points)} points, {len(edges)} line cells (edges of one graph)")
    endpoints = {}
    for index, ids in enumerate(edges):
        for node in (ids[0], ids[-1]):
            endpoints.setdefault(node, []).append(index)
    junctions = sorted(node for node, cells in endpoints.items() if len(cells) > 1)
    print(f"  {len(junctions)} point IDs end more than one cell: {junctions}")
    for key, meaning in (("start", "ostium"), ("branch", "bifurcation"), ("end", "tip")):
        if centerline[key] is not None:
            ids = np.flatnonzero(centerline[key]).tolist()
            print(f"  {key + '_points':14} {len(ids):3d}  ({meaning})  ids={ids}")
    print("  those shared endpoints are exactly the branch_points -- that is what makes")
    print("  the cells one connected graph rather than independent polylines")

    if oriented is None:
        print("  !! no start_points flag: nothing here can be oriented proximal->distal")
        return
    print(f"\n  rooted traversal from ostium id {root}: "
          f"{len(oriented)}/{len(edges)} edges reached")
    spacing = [np.linalg.norm(points[ids[j + 1]] - points[ids[j]])
               for ids in oriented for j in range(len(ids) - 1)]
    print(f"  point spacing: median {np.median(spacing):.3f} mm, "
          f"range {np.min(spacing):.3f}-{np.max(spacing):.3f} mm")
    print("  that is the voxel scale, which is why any second derivative taken on")
    print("  these points without smoothing measures the grid (see discover_tortuosity.py)")

    print("\n-- edges, oriented proximal -> distal")
    for index, ids in enumerate(oriented):
        spanned = sorted({int(centerline["label"][i]) for i in ids})
        print(f"  edge {index:2d}: {len(ids):4d} pts  {ids[0]:4d} -> {ids[-1]:4d}   "
              f"{', '.join(names.get(s, str(s)) for s in spanned)}")

    print("\n-- label runs and paths")
    paths = segment_paths(centerline, oriented)
    for label_id, pieces in paths.items():
        lengths = [float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum()) for p in pieces]
        print(f"  {names.get(label_id, label_id):<8} {len(pieces)} run(s), "
              f"{sum(lengths):7.1f} mm total, longest {max(lengths):6.1f} mm")
    print(f"  {len(tip_paths(centerline, oriented, root))} ostium-to-tip paths")


def report_against_mask(centerline, mask_path, side):
    import SimpleITK as sitk

    image = sitk.ReadImage(mask_path)
    arr = sitk.GetArrayFromImage(image)
    points, labels = centerline["points"], centerline["label"]

    inside = agree = outside_grid = 0
    for point, label in zip(points, labels):
        index = image.TransformPhysicalPointToIndex([float(v) for v in point])
        if not all(0 <= index[d] < image.GetSize()[d] for d in range(3)):
            outside_grid += 1
            continue
        value = int(arr[index[2], index[1], index[0]])
        if value > 0:
            inside += 1
            agree += value == int(label)

    print(f"\n-- against the mask ({side})")
    print(f"  {inside}/{len(points)} points land on a foreground voxel "
          f"({inside / len(points) * 100:.1f}%)")
    if outside_grid:
        print(f"  {outside_grid} fall outside the grid entirely")
    print(f"  of those, {agree} carry the same label as the mask voxel "
          f"({agree / max(inside, 1) * 100:.1f}%)")
    print("  A wrong coordinate frame would score near 0% here, so this doubles as a")
    print("  check that the mask's LPS geometry was applied. The label column compares")
    print("  two independent annotations of the same point: where they disagree, the")
    print("  segment boundary was drawn in a different place on mask and centerline.")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case", nargs="+", help="case prefix, e.g. images/1")
    parser.add_argument("--side", choices=("left", "right", "both"), default="both")
    parser.add_argument("--no-mask", action="store_true",
                        help="skip the cross-check against the mask")
    args = parser.parse_args()

    sides = ("left", "right") if args.side == "both" else (args.side,)
    for raw in args.case:
        files = case_files(resolve(raw))
        for side in sides:
            path = files[side]
            if not os.path.exists(path):
                continue
            centerline = read_centerline(path)
            oriented, root = orient_edges(centerline)
            report_structure(centerline, oriented, root, path)
            if not args.no_mask and os.path.exists(files["mask"]):
                report_against_mask(centerline, files["mask"], side)


if __name__ == "__main__":
    main()
