"""Centerlines from a predicted lumen mask, in the same form as the delivered ones.

The delivered GT centerlines are a skeleton of the corrected mask, Gaussian smoothed
(sigma = 0.5 mm, 5-vertex window), with start points on degree-1 vertices near the aorta and
names matched from the hand traces (Bransby et al. 2026, Methods). This reproduces that on a
predicted mask so the result goes through the same ``graph.build_tree``:

1. skeletonize (3D, Lee et al. 1994 -- the method ImageCAS-X cites) and trace it with ``skan``;
2. convert to LPS and smooth each path with the same Gaussian, junction and end points fixed;
3. flag end and branch points by degree;
4. take the ostium and the segment labels from providers.

Only the *oracle* providers exist so far: the ostium is the predicted end point nearest the GT
start point, and each point takes the label of the nearest GT-labelled voxel. They isolate the
geometric error the extraction adds from ostium and naming error, so any result built on them
must say "oracle". Herlev-Osterbro needs real ones (an aorta mask, multi-class labels).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree
from skan import Skeleton
from skimage.morphology import skeletonize

from . import coords, graph, io, radius

RIGHT_LABELS = frozenset({9, 10, 11})  # RCA, R-PDA, R-PLA; 14 ("Other") belongs to neither
OSTIUM_MAX_MM = 10.0


def skeleton_graph(mask: np.ndarray, affine: np.ndarray) -> tuple[np.ndarray, list[np.ndarray]]:
    """(N, 3) LPS points and point-index polylines of the mask's skeleton. Polylines share the
    index of the junction they meet at, which is what ``graph.build_tree`` connects on."""
    mask = np.asarray(mask) > 0
    idx = np.argwhere(mask)
    lo = np.maximum(idx.min(0) - 1, 0)
    hi = np.minimum(idx.max(0) + 2, mask.shape)
    skel = skeletonize(mask[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]])
    sk = Skeleton(skel)
    paths_ = [np.asarray(sk.path(i), dtype=int) for i in range(sk.n_paths)]
    used = np.unique(np.concatenate(paths_)) if paths_ else np.zeros(0, int)
    remap = {int(old): new for new, old in enumerate(used)}
    points = coords.voxel_to_lps(sk.coordinates[used] + lo, affine)
    return points, [np.array([remap[int(i)] for i in p]) for p in paths_]


def smooth(points: np.ndarray, lines: list[np.ndarray], sigma_mm: float = 0.5,
           window: int = 5) -> np.ndarray:
    """Gaussian-smooth each polyline's interior points over ``window`` vertices (weights from
    arc-length distance), leaving shared junction and end points where they are."""
    out = points.copy()
    half = window // 2
    for line in lines:
        p = points[line]
        arc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))])
        for j in range(1, len(line) - 1):
            k = np.arange(max(0, j - half), min(len(line), j + half + 1))
            w = np.exp(-0.5 * ((arc[k] - arc[j]) / sigma_mm) ** 2)
            out[line[j]] = (w[:, None] * p[k]).sum(0) / w.sum()
    return out


def _degree(n: int, lines: list[np.ndarray]) -> np.ndarray:
    deg = np.zeros(n, dtype=int)
    for line in lines:
        deg[line[0]] += 1
        deg[line[-1]] += 1
    return deg


def _components(n: int, lines: list[np.ndarray]) -> np.ndarray:
    parent = np.arange(n)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for line in lines:
        a, b = find(line[0]), find(line[-1])
        parent[a] = b
    return np.array([find(i) for i in range(n)])


def oracle_labels(points: np.ndarray, gt: io.Segmentation) -> np.ndarray:
    """Label of the nearest GT-labelled voxel. Oracle: uses the GT mask."""
    ijk = np.argwhere(gt.labels > 0)
    tree = cKDTree(coords.voxel_to_lps(ijk, gt.affine))
    _, nearest = tree.query(points)
    return gt.labels[tuple(ijk[nearest].T)].astype(int)


def _subset(points, lines, keep: np.ndarray):
    """Points where ``keep`` is True and the polylines entirely within them, reindexed."""
    new = -np.ones(len(points), dtype=int)
    new[keep] = np.arange(int(keep.sum()))
    sub = [new[line] for line in lines if keep[line].all()]
    return points[keep], sub, np.flatnonzero(keep)


def centerlines_from_mask(case_id: int, mask: np.ndarray, affine: np.ndarray,
                          gt: io.Segmentation, gt_centerlines: dict[str, io.Centerline]):
    """Left and right ``io.Centerline`` from a predicted mask, with oracle ostium and labels.

    Returns ``(centerlines, notes)``; ``notes`` lists anything a reader of the result should
    know, e.g. an ostium with no predicted end point near it.
    """
    points, lines = skeleton_graph(mask, affine)
    points = smooth(points, lines)
    labels = oracle_labels(points, gt)
    comp = _components(len(points), lines)

    # Side per connected component, by majority of its side-specific labels. A component with
    # only "Other" goes to the nearer GT tree.
    side_of = {}
    gt_trees = {s: cKDTree(c.points) for s, c in gt_centerlines.items()}
    notes = []
    for c in np.unique(comp):
        lab = labels[comp == c]
        right, left = np.isin(lab, list(RIGHT_LABELS)).sum(), (~np.isin(lab, list(RIGHT_LABELS | {14}))).sum()
        if right == left == 0:
            d = {s: t.query(points[comp == c])[0].mean() for s, t in gt_trees.items()}
            side_of[c] = min(d, key=d.get)
        else:
            side_of[c] = "right" if right > left else "left"
            if min(right, left) > 0.1 * (right + left):
                notes.append(f"component of {lab.size} points has {left} left / {right} right labels")
    point_side = np.array([side_of[c] for c in comp])

    out = {}
    for side in ("left", "right"):
        pts, sub, orig = _subset(points, lines, point_side == side)
        deg = _degree(len(pts), sub)
        start = np.zeros(len(pts), dtype=int)
        ends = np.flatnonzero(deg == 1)
        gt_cl = gt_centerlines[side]
        for gt_start in gt_cl.points[np.flatnonzero(gt_cl.start_points)]:
            if len(ends) == 0:
                notes.append(f"{side}: no predicted end point to place the ostium on")
                break
            d = np.linalg.norm(pts[ends] - gt_start, axis=1)
            if d.min() > OSTIUM_MAX_MM:
                notes.append(f"{side}: nearest predicted end is {d.min():.1f} mm from the GT ostium; none set")
                continue
            start[ends[np.argmin(d)]] = 1
        lab = labels[orig]
        out[side] = io.Centerline(
            case_id=case_id, side=side, points=pts, segment_label=lab,
            segment_name=np.array([graph.artery_name(x) for x in lab]),
            branch_points=(deg >= 3).astype(int), end_points=(deg == 1).astype(int),
            start_points=start, lines=sub,
            radius=radius.radius_at(pts, mask, affine) if len(pts) else np.zeros(0),
        )
    return out, notes


def write_centerline_vtk(cl: io.Centerline, path: Path) -> None:
    """Write a centerline in the delivered file's layout, plus a ``radius`` array."""
    import vtk
    from vtk.util import numpy_support as ns

    poly = vtk.vtkPolyData()
    vpts = vtk.vtkPoints()
    vpts.SetData(ns.numpy_to_vtk(np.ascontiguousarray(cl.points, dtype=np.float64), deep=True))
    poly.SetPoints(vpts)
    cells = vtk.vtkCellArray()
    for line in cl.lines:
        pl = vtk.vtkPolyLine()
        pl.GetPointIds().SetNumberOfIds(len(line))
        for j, i in enumerate(line):
            pl.GetPointIds().SetId(j, int(i))
        cells.InsertNextCell(pl)
    poly.SetLines(cells)
    pd = poly.GetPointData()
    for name, arr in (("segment_label", cl.segment_label), ("start_points", cl.start_points),
                      ("end_points", cl.end_points), ("branch_points", cl.branch_points)):
        a = ns.numpy_to_vtk(np.asarray(arr, dtype=np.int32), deep=True)
        a.SetName(name)
        pd.AddArray(a)
    r = ns.numpy_to_vtk(np.asarray(cl.radius, dtype=np.float32), deep=True)
    r.SetName("radius")
    pd.AddArray(r)
    names = vtk.vtkStringArray()
    names.SetName("segment_name")
    for n in cl.segment_name:
        names.InsertNextValue(str(n))
    pd.AddArray(names)
    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName(str(path))
    writer.SetInputData(poly)
    writer.Write()
