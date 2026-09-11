"""Explore the voxel mask of a case: <scan>.coronary.nii.gz.

The mask is the primary artefact -- the annotation the surface and the
centerlines are both derived from. It is a dense label map: one small integer
per voxel, 0 for background and 1-14 for the coronary segment that voxel lies
in. Nothing in the file names those labels; the names come from the centerline
VTKs and from the scheme in README.MD.

    uv run python scripts/discover_mask.py images/1

Reports grid geometry and the index-to-physical transform, the label set with
per-segment voxel counts and volumes, each segment's physical extent, and a
connected-component count per segment (a segment in several pieces is either a
genuine gap in the annotation or a break the extraction introduced).
"""

import argparse
import os

import numpy as np
import SimpleITK as sitk
from scipy import ndimage

from discover_common import case_files, resolve, segment_names


def report(path):
    image = sitk.ReadImage(path)
    arr = sitk.GetArrayFromImage(image)          # (z, y, x)
    spacing = np.array(image.GetSpacing())        # (x, y, z)
    voxel_mm3 = float(np.prod(spacing))
    names = segment_names()

    print(f"\n== {os.path.basename(path)}")
    print(f"   {os.path.getsize(path) / 1e3:.1f} KB on disk, "
          f"{arr.nbytes / 1e6:.1f} MB uncompressed")

    print("\n-- grid")
    print(f"  size (x,y,z)   {image.GetSize()}")
    print(f"  array (z,y,x)  {arr.shape}   <- SimpleITK reverses the axes")
    print(f"  spacing        {tuple(float(v) for v in spacing)} mm")
    print(f"  voxel volume   {voxel_mm3:.6f} mm^3")
    print(f"  dtype          {image.GetPixelIDTypeAsString()}")
    print(f"  extent         {tuple(round(float(s) * n, 1) for s, n in zip(spacing, image.GetSize()))} mm")

    print("\n-- index -> physical (LPS)")
    direction = np.array(image.GetDirection()).reshape(3, 3)
    matrix = np.eye(4)
    matrix[:3, :3] = direction @ np.diag(spacing)
    matrix[:3, 3] = image.GetOrigin()
    for row in matrix:
        print("   " + "  ".join(f"{v:10.5f}" for v in row))
    print("  SimpleITK reports LPS. The NIfTI header itself stores RAS, so a reader")
    print("  that hands back RAS (nibabel does) needs diag(-1,-1,1) applied before")
    print("  anything here will line up with the .vtk files.")

    labels = sorted(int(v) for v in np.unique(arr) if v > 0)
    foreground = int((arr > 0).sum())
    print("\n-- occupancy")
    print(f"  foreground {foreground} of {arr.size} voxels = "
          f"{foreground / arr.size * 100:.3f}%  ({foreground * voxel_mm3:.1f} mm^3)")
    print("  the file is mostly zeros, which is why it gzips to a fraction of its size")

    print("\n-- segments")
    print(f"  {'label':>5}  {'name':<8} {'voxels':>8} {'mm^3':>9} {'share':>7} "
          f"{'parts':>6} {'extent (mm)':>22}")
    structure = np.ones((3, 3, 3), dtype=bool)   # 26-connectivity
    for label in labels:
        binary = arr == label
        n = int(binary.sum())
        _, parts = ndimage.label(binary, structure=structure)
        where = [np.flatnonzero(binary.any(axis=tuple(a for a in range(3) if a != ax)))
                 for ax in range(3)]
        # axis order is (z, y, x); report extent as (x, y, z) to match spacing
        extent = [(w[-1] - w[0] + 1) * s for w, s in zip(where[::-1], spacing)]
        print(f"  {label:>5}  {names.get(label, '?'):<8} {n:>8} {n * voxel_mm3:>9.1f} "
              f"{n / foreground * 100:>6.1f}% {parts:>6}"
              f"   {extent[0]:6.1f} x{extent[1]:6.1f} x{extent[2]:6.1f}")

    absent = sorted(set(names) - set(labels))
    if absent:
        print(f"\n  absent: {', '.join(f'{i} ({names[i]})' for i in absent)}")
        print("  Absence is anatomy or annotation scope, not a defect. Labels 10/11 are")
        print("  the right-sided PDA/PLA and 12/13 the left-sided ones, so which pair")
        print("  is present encodes coronary dominance.")

    multi = [(label, names.get(label, '?')) for label in labels
             if ndimage.label(arr == label, structure=structure)[1] > 1]
    if multi:
        print(f"\n  in more than one piece: "
              f"{', '.join(f'{n} ({i})' for i, n in multi)}")
        print("  worth a look -- a segment in several pieces is a gap in the lumen")
        print("  annotation, and any centerline through it will be broken too.")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mask", nargs="+", help="case prefix or mask path, e.g. images/1")
    for path in parser.parse_args().mask:
        report(case_files(resolve(path))["mask"])


if __name__ == "__main__":
    main()
