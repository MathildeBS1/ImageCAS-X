"""Shared loaders for the discover_* scripts.

Not a command-line tool: run one of the four scripts beside it.

  discover_mask.py        the voxel label mask   (<id>.coronary.nii.gz)
  discover_surface.py     the triangle mesh      (<id>.coronary_surface.vtk)
  discover_centerline.py  the centerline graph   (<id>.coronary_{left,right}_centerline.vtk)
  discover_tortuosity.py  tortuosity of the centerlines

Everything here runs on what `uv sync` installs: numpy, scipy, vtk, SimpleITK.
"""

import ast
import glob
import os

import numpy as np
import vtk
from vtk.util import numpy_support as ns

FALLBACK_SEGMENT_NAMES = {
    1: "LM", 2: "LAD", 3: "LCx", 4: "D1", 5: "D2", 6: "OM1", 7: "OM2",
    8: "IM", 9: "RCA", 10: "R-PDA", 11: "R-PLA", 12: "L-PDA", 13: "L-PLA",
    14: "Other",
}


def segment_names():
    """SEGMENT_NAMES from evaluate.py, read without importing it (it needs torch)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "evaluate.py")
    try:
        tree = ast.parse(open(path).read())
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                    getattr(t, "id", None) == "SEGMENT_NAMES" for t in node.targets):
                return ast.literal_eval(node.value)
    except (OSError, SyntaxError, ValueError):
        pass
    return FALLBACK_SEGMENT_NAMES


def resolve(prefix):
    """Accept 'images/1', any one of the case's files, or a folder holding one."""
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


def case_files(prefix):
    return {
        "mask": prefix + ".coronary.nii.gz",
        "surface": prefix + ".coronary_surface.vtk",
        "left": prefix + ".coronary_left_centerline.vtk",
        "right": prefix + ".coronary_right_centerline.vtk",
    }


def banner(title, width=68):
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def read_polydata(path):
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(path)
    reader.ReadAllScalarsOn()
    reader.Update()
    return reader.GetOutput()


def read_centerline(path):
    """Points, the line cells, and every point-data array, as plain numpy."""
    poly = read_polydata(path)
    point_data = poly.GetPointData()

    def array(name):
        arr = point_data.GetArray(name)
        return ns.vtk_to_numpy(arr) if arr else None

    names_array = point_data.GetAbstractArray("segment_name")
    edges = []
    for i in range(poly.GetNumberOfCells()):
        ids = poly.GetCell(i).GetPointIds()
        edges.append([ids.GetId(j) for j in range(ids.GetNumberOfIds())])
    return {
        "points": ns.vtk_to_numpy(poly.GetPoints().GetData()),
        "label": array("segment_label"),
        "start": array("start_points"),
        "end": array("end_points"),
        "branch": array("branch_points"),
        "names": ({i: names_array.GetValue(i) for i in range(names_array.GetNumberOfValues())}
                  if names_array else {}),
        "edges": edges,
    }


def orient_edges(centerline):
    """Orient every edge proximal->distal by a BFS rooted at the ostium.

    Returns (oriented_edges, root_id). Cell order carries no orientation
    (`utils/precompute_centerline_samples.py:11-13`), so the point flagged in
    `start_points` is the only usable root.
    """
    flags = centerline["start"]
    root_ids = np.flatnonzero(flags) if flags is not None else []
    if len(root_ids) == 0:
        return None, None
    root = int(root_ids[0])

    incident = {}
    for index, ids in enumerate(centerline["edges"]):
        incident.setdefault(ids[0], []).append(index)
        incident.setdefault(ids[-1], []).append(index)

    oriented, seen, queue = {}, set(), [root]
    while queue:
        node = queue.pop(0)
        for index in incident.get(node, []):
            if index in seen:
                continue
            seen.add(index)
            ids = centerline["edges"][index]
            if ids[-1] == node:  # edge points the wrong way; reverse it
                ids = ids[::-1]
            oriented[index] = ids
            queue.append(ids[-1])
    return [oriented[i] for i in sorted(oriented)], root


def segment_paths(centerline, oriented):
    """One proximal->distal path per anatomical segment label.

    A cell can straddle two labels -- the label changes at a branch point -- so
    paths are cut at label changes. A label can therefore yield several
    disconnected pieces; all of them are returned.
    """
    label = centerline["label"]
    if label is None or oriented is None:
        return {}
    runs = {}
    for ids in oriented:
        current, start = int(label[ids[0]]), 0
        for position in range(1, len(ids) + 1):
            at_end = position == len(ids)
            value = None if at_end else int(label[ids[position]])
            if at_end or value != current:
                piece = ids[start:position]
                if len(piece) > 1:
                    runs.setdefault(current, []).append(piece)
                if not at_end:
                    current, start = value, position - 1
    return {label_id: [centerline["points"][np.array(p)] for p in pieces]
            for label_id, pieces in sorted(runs.items())}


def tip_paths(centerline, oriented, root):
    """Every ostium-to-tip path: the unit a whole-vessel tortuosity is defined on."""
    if oriented is None:
        return []
    children = {}
    for ids in oriented:
        children.setdefault(ids[0], []).append(ids)
    paths, stack = [], [(root, [root])]
    while stack:
        node, walked = stack.pop()
        outgoing = children.get(node, [])
        if not outgoing:
            if len(walked) > 1:
                paths.append(centerline["points"][np.array(walked)])
            continue
        for ids in outgoing:
            stack.append((ids[-1], walked + list(ids[1:])))
    return paths
