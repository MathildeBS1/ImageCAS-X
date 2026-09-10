"""Interactive 3D view of one ImageCAS-X case, without 3D Slicer.

Opens a VTK window with any combination of the three things a case ships with:
the multi-label mask (<scan>.coronary.nii.gz), the mesh (<scan>_surface.vtk)
and the two centerlines (<scan>_{left,right}_centerline.vtk). The mask is
contoured per coronary segment and coloured by label; the centerlines are
coloured by their segment_label array.

Uses only vtk, SimpleITK and numpy, so `uv sync` is the whole setup:

    .venv/bin/python scripts/view_case_3d.py images/1

SimpleITK reads the mask in LPS, the same frame the .vtk files are stored in,
so the contours land on the geometry once they are pushed through the image's
own index-to-physical transform.

Drag to rotate, scroll to zoom, right-drag (or shift-drag) to pan, "q" to close.
"""

import argparse
import glob
import os

import numpy as np
import SimpleITK as sitk
import vtk
from vtk.util import numpy_support

# Distinct colour per coronary segment label (1-14), reused beyond that.
SEGMENT_COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b",
    "#e377c2", "#7f7f7f", "#bcbd22", "#17becf", "#aec7e8", "#ffbb78",
    "#98df8a", "#ff9896",
]


def _rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def _color(label):
    return _rgb(SEGMENT_COLORS[(int(label) - 1) % len(SEGMENT_COLORS)])


def _index_to_physical(image):
    """4x4 voxel-index-to-LPS matrix of a SimpleITK image."""
    matrix = np.eye(4)
    direction = np.array(image.GetDirection()).reshape(3, 3)
    matrix[:3, :3] = direction @ np.diag(image.GetSpacing())
    matrix[:3, 3] = image.GetOrigin()
    return matrix


def _as_vtk_matrix(matrix):
    out = vtk.vtkMatrix4x4()
    for r in range(4):
        for c in range(4):
            out.SetElement(r, c, float(matrix[r, c]))
    return out


def label_surfaces(mask_path, smooth_iters):
    """Marching cubes per label, returned in the mask's LPS coordinates."""
    image = sitk.ReadImage(mask_path)
    arr = sitk.GetArrayFromImage(image)  # (z, y, x)
    index_to_physical = _index_to_physical(image)

    labels = np.unique(arr)
    labels = labels[labels > 0]

    out = {}
    for label in labels:
        binary = arr == label
        # Contour only the label's own bounding box (one pad voxel so the
        # surface closes), then fold the crop origin into the transform.
        spans = [np.flatnonzero(binary.any(axis=tuple(a for a in range(3) if a != ax)))
                 for ax in range(3)]
        lo = [max(int(s[0]) - 1, 0) for s in spans]
        hi = [min(int(s[-1]) + 2, n) for s, n in zip(spans, arr.shape)]
        crop = binary[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]

        # vtkImageData is x-fastest, which is exactly C order on a (z, y, x) array.
        volume = vtk.vtkImageData()
        volume.SetDimensions(crop.shape[2], crop.shape[1], crop.shape[0])
        scalars = numpy_support.numpy_to_vtk(
            np.ascontiguousarray(crop, dtype=np.uint8).ravel(), deep=True)
        volume.GetPointData().SetScalars(scalars)

        contour = vtk.vtkFlyingEdges3D()
        contour.SetInputData(volume)
        contour.SetValue(0, 0.5)
        contour.ComputeNormalsOff()  # normals are recomputed after the transform
        upstream = contour

        if smooth_iters:
            smoother = vtk.vtkWindowedSincPolyDataFilter()
            smoother.SetInputConnection(upstream.GetOutputPort())
            smoother.SetNumberOfIterations(smooth_iters)
            smoother.SetPassBand(0.05)
            smoother.NonManifoldSmoothingOn()
            smoother.NormalizeCoordinatesOn()
            upstream = smoother

        shift = np.eye(4)
        shift[:3, 3] = lo[::-1]  # lo is (z, y, x); the transform wants (x, y, z)
        transform = vtk.vtkTransform()
        transform.SetMatrix(_as_vtk_matrix(index_to_physical @ shift))
        placed = vtk.vtkTransformFilter()
        placed.SetInputConnection(upstream.GetOutputPort())
        placed.SetTransform(transform)

        normals = vtk.vtkPolyDataNormals()
        normals.SetInputConnection(placed.GetOutputPort())
        normals.SetFeatureAngle(60.0)
        normals.Update()

        mesh = normals.GetOutput()
        if mesh.GetNumberOfPoints():
            out[int(label)] = mesh
    return out


def read_polydata(path):
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(path)
    reader.ReadAllScalarsOn()
    reader.Update()
    return reader.GetOutput()


def add_actor(renderer, polydata, color=None, opacity=1.0, scalars=None, lut=None):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    if scalars is not None:
        mapper.SetScalarModeToUsePointFieldData()
        mapper.SelectColorArray(scalars)
        mapper.SetLookupTable(lut)
        mapper.SetScalarRange(lut.GetRange())
        mapper.ScalarVisibilityOn()
    else:
        mapper.ScalarVisibilityOff()
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    if color is not None:
        actor.GetProperty().SetColor(*color)
    actor.GetProperty().SetOpacity(opacity)
    renderer.AddActor(actor)
    return actor


def segment_lut(max_label=len(SEGMENT_COLORS)):
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(max_label + 1)
    lut.SetRange(0, max_label)
    lut.SetTableValue(0, 0.55, 0.55, 0.55, 1.0)
    for label in range(1, max_label + 1):
        lut.SetTableValue(label, *_color(label), 1.0)
    lut.Build()
    return lut


def resolve(prefix):
    """Accept 'images/1', 'images/1.coronary.nii.gz' or a folder holding one case."""
    if os.path.isdir(prefix):
        hits = sorted(glob.glob(os.path.join(prefix, "*.coronary.nii.gz")))
        hits += sorted(glob.glob(os.path.join(prefix, "*_surface.vtk")))
        if not hits:
            raise SystemExit(f"no case files under {prefix}")
        prefix = hits[0]
    for suffix in (".coronary.nii.gz", ".coronary_surface.vtk", ".nii.gz", ".vtk"):
        if prefix.endswith(suffix):
            return prefix[: -len(suffix)]
    return prefix


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("case", help="path prefix of the case, e.g. images/1")
    p.add_argument("--no-mask", action="store_true", help="skip the label mask")
    p.add_argument("--no-surface", action="store_true", help="skip the mesh")
    p.add_argument("--no-centerlines", action="store_true", help="skip the centerlines")
    p.add_argument("--surface-opacity", type=float, default=0.35)
    p.add_argument("--mask-opacity", type=float, default=1.0)
    p.add_argument("--tube-radius", type=float, default=0.35,
                   help="centerline tube radius in mm; 0 draws plain lines")
    p.add_argument("--smooth", type=int, default=20,
                   help="smoothing iterations on the mask contours (0 = off)")
    p.add_argument("--screenshot", metavar="PNG",
                   help="render off-screen to this file instead of opening a window")
    args = p.parse_args()

    prefix = resolve(args.case)
    mask_path = prefix + ".coronary.nii.gz"
    surface_path = prefix + ".coronary_surface.vtk"

    renderer = vtk.vtkRenderer()
    renderer.SetBackground(1.0, 1.0, 1.0)
    lut = segment_lut()
    drew = []

    if not args.no_mask and os.path.exists(mask_path):
        for label, mesh in sorted(label_surfaces(mask_path, args.smooth).items()):
            add_actor(renderer, mesh, color=_color(label), opacity=args.mask_opacity)
        drew.append(os.path.basename(mask_path))

    if not args.no_surface and os.path.exists(surface_path):
        add_actor(renderer, read_polydata(surface_path), color=(0.78, 0.78, 0.78),
                  opacity=args.surface_opacity)
        drew.append(os.path.basename(surface_path))

    if not args.no_centerlines:
        for side in ("left", "right"):
            path = f"{prefix}.coronary_{side}_centerline.vtk"
            if not os.path.exists(path):
                continue
            line = read_polydata(path)
            if args.tube_radius > 0:
                tube = vtk.vtkTubeFilter()
                tube.SetInputData(line)
                tube.SetRadius(args.tube_radius)
                tube.SetNumberOfSides(12)
                tube.CappingOn()
                tube.Update()
                line = tube.GetOutput()
            if line.GetPointData().GetArray("segment_label"):
                add_actor(renderer, line, scalars="segment_label", lut=lut)
            else:
                add_actor(renderer, line, color=(0.0, 0.0, 0.0))
            drew.append(os.path.basename(path))

    if not drew:
        raise SystemExit(f"nothing found for prefix {prefix!r}")
    print("showing: " + ", ".join(drew))

    camera = renderer.GetActiveCamera()
    camera.SetPosition(0, -1, 0)  # anterior view, head up
    camera.SetFocalPoint(0, 0, 0)
    camera.SetViewUp(0, 0, 1)
    renderer.ResetCamera()

    window = vtk.vtkRenderWindow()
    window.AddRenderer(renderer)
    window.SetSize(1200, 900)
    window.SetWindowName(f"ImageCAS-X  {os.path.basename(prefix)}")

    if args.screenshot:
        window.SetOffScreenRendering(1)
        window.Render()
        grab = vtk.vtkWindowToImageFilter()
        grab.SetInput(window)
        grab.Update()
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(args.screenshot)
        writer.SetInputConnection(grab.GetOutputPort())
        writer.Write()
        print(f"wrote {args.screenshot}")
        return

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)
    interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    axes = vtk.vtkAxesActor()
    marker = vtk.vtkOrientationMarkerWidget()
    marker.SetOrientationMarker(axes)
    marker.SetInteractor(interactor)
    marker.SetViewport(0.0, 0.0, 0.2, 0.2)
    marker.EnabledOn()
    marker.InteractiveOff()
    window.Render()
    interactor.Start()


if __name__ == "__main__":
    main()
