"""Explore the lumen mesh of a case: <scan>.coronary_surface.vtk.

The mesh is not independent data. `utils/offline_generate_mesh_from_voxel.py`
produces it from the mask by marching cubes at isovalue 0.5 followed by
windowed-sinc (Taubin-style) smoothing, so everything here is a restatement of
the mask in a different representation -- explicit triangles in LPS millimetres
instead of labels on a grid. What it adds is a surface: area, a well-defined
enclosed volume, and the smoothness the voxel staircase does not have.

    uv run python scripts/discover_surface.py images/1

Reports mesh size and triangle quality, whether the surface is closed and
manifold, its connected components, area and enclosed volume, and -- when the
mask is beside it -- how far the smoothing moved the volume away from the raw
voxel count.
"""

import argparse
import os

import numpy as np
import vtk
from vtk.util import numpy_support as ns

from discover_common import case_files, read_polydata, resolve

read = read_polydata


def mass_properties(polydata):
    triangles = vtk.vtkTriangleFilter()
    triangles.SetInputData(polydata)
    triangles.Update()
    mass = vtk.vtkMassProperties()
    mass.SetInputData(triangles.GetOutput())
    mass.Update()
    return mass.GetSurfaceArea(), mass.GetVolume()


def report(path):
    mesh = read(path)
    points = ns.vtk_to_numpy(mesh.GetPoints().GetData())

    print(f"\n== {os.path.basename(path)}")
    with open(path) as handle:
        encoding = [next(handle) for _ in range(3)][2].strip()
    print(f"   {os.path.getsize(path) / 1e6:.1f} MB on disk, {encoding} encoding")
    print("   (ASCII writes ~20 characters per coordinate; BINARY would be far smaller)")

    print("\n-- size")
    print(f"  points     {mesh.GetNumberOfPoints()}")
    print(f"  polygons   {mesh.GetNumberOfPolys()}")
    sizes = {}
    for i in range(mesh.GetNumberOfCells()):
        n = mesh.GetCell(i).GetNumberOfPoints()
        sizes[n] = sizes.get(n, 0) + 1
    print(f"  cell sizes {sizes}  (3 = triangles throughout)")

    print("\n-- topology")
    edges = vtk.vtkFeatureEdges()
    edges.SetInputData(mesh)
    edges.BoundaryEdgesOn()
    edges.NonManifoldEdgesOn()
    edges.FeatureEdgesOff()
    edges.ManifoldEdgesOff()
    edges.Update()
    bad = edges.GetOutput().GetNumberOfCells()
    print(f"  boundary + non-manifold edges: {bad}")
    print("  " + ("closed and manifold -- enclosed volume is well defined"
                  if bad == 0 else
                  "NOT watertight: the enclosed volume below is not trustworthy"))

    connectivity = vtk.vtkPolyDataConnectivityFilter()
    connectivity.SetInputData(mesh)
    connectivity.SetExtractionModeToAllRegions()
    connectivity.Update()
    n_regions = connectivity.GetNumberOfExtractedRegions()
    print(f"  connected components: {n_regions}")
    if n_regions == 2:
        print("  two components is the expected anatomy: the left and right trees")
        print("  arise from separate ostia and never touch.")

    print("\n-- geometry")
    area, volume = mass_properties(mesh)
    print(f"  surface area     {area:10.1f} mm^2")
    print(f"  enclosed volume  {volume:10.1f} mm^3")
    print(f"  area / volume    {area / volume:10.3f} 1/mm   (high = thin tubes)")
    for axis, name in enumerate("xyz"):
        print(f"  {name} bounds        {points[:, axis].min():9.2f} .. "
              f"{points[:, axis].max():8.2f} mm  (LPS)")

    for i in range(n_regions):
        region = vtk.vtkPolyDataConnectivityFilter()
        region.SetInputData(mesh)
        region.SetExtractionModeToSpecifiedRegions()
        region.AddSpecifiedRegion(i)
        region.Update()
        clean = vtk.vtkCleanPolyData()
        clean.SetInputData(region.GetOutput())
        clean.Update()
        part_area, part_volume = mass_properties(clean.GetOutput())
        print(f"  component {i}: {clean.GetOutput().GetNumberOfPoints():6d} points, "
              f"{part_area:8.1f} mm^2, {part_volume:8.1f} mm^3")

    print("\n-- triangle scale")
    lengths = []
    for i in range(0, mesh.GetNumberOfCells(), max(1, mesh.GetNumberOfCells() // 4000)):
        ids = mesh.GetCell(i).GetPointIds()
        trio = points[[ids.GetId(j) for j in range(ids.GetNumberOfIds())]]
        lengths += [float(np.linalg.norm(trio[j] - trio[(j + 1) % len(trio)]))
                    for j in range(len(trio))]
    lengths = np.array(lengths)
    print(f"  edge length: median {np.median(lengths):.3f} mm, "
          f"5-95% {np.percentile(lengths, 5):.3f}-{np.percentile(lengths, 95):.3f} mm")
    print("  marching cubes puts vertices on voxel edges, so this tracks the voxel size")

    print("\n-- point arrays")
    point_data = mesh.GetPointData()
    for i in range(point_data.GetNumberOfArrays()):
        name = point_data.GetArrayName(i)
        values = ns.vtk_to_numpy(point_data.GetArray(i))
        print(f"  {name}: shape {values.shape}, dtype {values.dtype}")
        print(f"    min {np.round(values.min(axis=0), 2)}  max {np.round(values.max(axis=0), 2)}")
        if name == "voxel_coords_resampled" and values.shape[1:] == (3,):
            print("    fractional indices into the 0.5 mm isotropic resampled grid.")
            print("    Recovering a physical point from one needs the mask's origin and")
            print("    direction, not this array alone:")
            print(f"      vertex 0 physical  {np.round(points[0], 4)}")
            print(f"      vertex 0 index     {np.round(values[0], 4)}")

    mask_path = path.replace(".coronary_surface.vtk", ".coronary.nii.gz")
    if os.path.exists(mask_path):
        import SimpleITK as sitk
        image = sitk.ReadImage(mask_path)
        arr = sitk.GetArrayFromImage(image)
        voxel_volume = float((arr > 0).sum()) * float(np.prod(image.GetSpacing()))
        print("\n-- against the mask it came from")
        print(f"  mask foreground  {voxel_volume:10.1f} mm^3")
        print(f"  mesh enclosed    {volume:10.1f} mm^3")
        print(f"  difference       {volume - voxel_volume:+10.1f} mm^3 "
              f"({(volume - voxel_volume) / voxel_volume * 100:+.1f}%)")
        print("  Marching cubes at 0.5 cuts through the outer voxels rather than")
        print("  enclosing them, and the smoothing rounds off convex staircase corners,")
        print("  so the mesh is expected to enclose slightly less than the voxel count.")
        print("  Treat the two as different estimators of lumen volume, not as a check.")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("surface", nargs="+", help="case prefix or mesh path, e.g. images/1")
    for path in parser.parse_args().surface:
        report(case_files(resolve(path))["surface"])


if __name__ == "__main__":
    main()
