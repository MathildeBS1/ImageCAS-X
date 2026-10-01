"""One ordered centerline per named artery, read from the ImageCAS-X centerline VTK files.

Point order in the file is not walk order (consecutive points can be 80 mm apart), so each
path is rebuilt from the line cells. The points labelled with one artery form a tree, and
the artery is taken as its longest geodesic path, oriented so that it starts at the ostium.
"""
import os

import numpy as np
import vtk
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components, dijkstra
from vtk.util.numpy_support import vtk_to_numpy

# name: (segment_label, tree), with the ImageCAS-X label scheme
ARTERIES = {"LAD": (2, "left"), "LCX": (3, "left"), "RCA": (9, "right")}


def read(path):
    """Points (n, 3) in mm, segment label per point, line-cell edges (m, 2) and ostium point(s)."""
    r = vtk.vtkPolyDataReader()
    r.SetFileName(path)
    r.ReadAllScalarsOn()
    r.ReadAllFieldsOn()
    r.Update()
    p = r.GetOutput()
    pts = vtk_to_numpy(p.GetPoints().GetData()).astype(np.float64)
    data = p.GetPointData()
    label = vtk_to_numpy(data.GetArray("segment_label"))
    ostium = pts[vtk_to_numpy(data.GetArray("start_points")) > 0]
    lines, ids, edges = p.GetLines(), vtk.vtkIdList(), []
    lines.InitTraversal()
    while lines.GetNextCell(ids):
        c = [ids.GetId(i) for i in range(ids.GetNumberOfIds())]
        edges += zip(c[:-1], c[1:])
    return pts, label, np.array(edges), ostium


def longest_path(pts, edges):
    """Longest geodesic path through the largest connected component, as an ordered (n, 3) array."""
    n = len(pts)
    w = np.linalg.norm(pts[edges[:, 0]] - pts[edges[:, 1]], axis=1)
    g = coo_matrix((w, (edges[:, 0], edges[:, 1])), shape=(n, n)).tocsr()
    _, comp = connected_components(g, directed=False)
    start = np.flatnonzero(comp == np.bincount(comp).argmax())[0]
    # two Dijkstra sweeps: the farthest point from anywhere is one end, the farthest from it the other
    d = dijkstra(g, directed=False, indices=start)
    a = int(np.argmax(np.where(np.isfinite(d), d, -1)))
    d, pred = dijkstra(g, directed=False, indices=a, return_predecessors=True)
    b = int(np.argmax(np.where(np.isfinite(d), d, -1)))
    path = [b]
    while path[-1] != a:
        path.append(pred[path[-1]])
    return pts[path]


def load_vessels(case_id, data_dir=None):
    """{name: (n, 3) array in mm, ostium end first} for LAD, LCX and RCA.

    A name is absent when fewer than two edges carry its label.
    """
    data_dir = data_dir or os.environ["ImageCAS_X_data_path"]
    out = {}
    for side in ("left", "right"):
        pts, label, edges, ostium = read(f"{data_dir}/centerlines/{case_id}.coronary_{side}_centerline.vtk")
        for name, (lab, s) in ARTERIES.items():
            m = (label[edges[:, 0]] == lab) & (label[edges[:, 1]] == lab)
            if s != side or m.sum() < 2:
                continue
            P = longest_path(pts, edges[m])
            if len(ostium):
                dist = lambda x: np.linalg.norm(ostium - x, axis=1).min()
                P = P[::-1] if dist(P[-1]) < dist(P[0]) else P
            out[name] = P
    return out
