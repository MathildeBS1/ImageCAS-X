"""One ordered centerline path per named artery, straight from the VTK files.

Point order in the file is not walk order (consecutive points can be 80 mm apart), so the
paths are rebuilt from the line cells. Points labelled with an artery form a connected
tree; the artery is taken as its longest geodesic path.
"""
import os

import numpy as np
import vtk
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components, dijkstra
from vtk.util.numpy_support import vtk_to_numpy

ARTERIES = {"LAD": (2, "left"), "LCX": (3, "left"), "RCA": (9, "right")}


def _polydata(path):
    r = vtk.vtkPolyDataReader()
    r.SetFileName(path)
    r.ReadAllScalarsOn()
    r.ReadAllFieldsOn()
    r.Update()
    return r.GetOutput()


def read(path):
    p = _polydata(path)
    pts = vtk_to_numpy(p.GetPoints().GetData()).astype(np.float64)
    label = vtk_to_numpy(p.GetPointData().GetArray("segment_label"))
    lines, ids = p.GetLines(), vtk.vtkIdList()
    lines.InitTraversal()
    edges = []
    while lines.GetNextCell(ids):
        c = [ids.GetId(i) for i in range(ids.GetNumberOfIds())]
        edges += zip(c[:-1], c[1:])
    return pts, label, np.array(edges)


def longest_path(pts, edges):
    """Longest geodesic path (mm) through the graph, as an ordered (n, 3) array."""
    n = len(pts)
    w = np.linalg.norm(pts[edges[:, 0]] - pts[edges[:, 1]], axis=1)
    g = coo_matrix((w, (edges[:, 0], edges[:, 1])), shape=(n, n)).tocsr()
    k, comp = connected_components(g, directed=False)
    keep = np.flatnonzero(comp == np.bincount(comp).argmax())
    d = dijkstra(g, directed=False, indices=keep[0])
    a = int(np.argmax(np.where(np.isfinite(d), d, -1)))
    d, pred = dijkstra(g, directed=False, indices=a, return_predecessors=True)
    b = int(np.argmax(np.where(np.isfinite(d), d, -1)))
    path = [b]
    while path[-1] != a:
        path.append(pred[path[-1]])
    return pts[path]


def start_point(case, side, data_dir=None):
    """The ostium point(s) of one tree, flagged by the file's start_points array."""
    data_dir = data_dir or os.environ["ImageCAS_X_data_path"]
    p = _polydata(f"{data_dir}/centerlines/{case}.coronary_{side}_centerline.vtk")
    pts = vtk_to_numpy(p.GetPoints().GetData()).astype(np.float64)
    return pts[vtk_to_numpy(p.GetPointData().GetArray("start_points")) > 0]


def load_vessels(case_id, data_dir=None):
    """{name: (n, 3) LPS mm} for LAD, LCX, RCA, ostium end first; a name is absent when it cannot be built."""
    data_dir = data_dir or os.environ["ImageCAS_X_data_path"]
    out = {}
    for side in ("left", "right"):
        pts, label, edges = read(f"{data_dir}/centerlines/{case_id}.coronary_{side}_centerline.vtk")
        ost = start_point(case_id, side, data_dir)
        for name, (lab, s) in ARTERIES.items():
            if s != side:
                continue
            m = (label[edges[:, 0]] == lab) & (label[edges[:, 1]] == lab)
            if m.sum() >= 2:
                P = longest_path(pts, edges[m])
                d = lambda x: np.linalg.norm(ost - x, axis=1).min()
                out[name] = P[::-1] if len(ost) and d(P[-1]) < d(P[0]) else P
    return out
