"""One ordered centerline per named artery, read from the ImageCAS-X centerline VTK files.

Point order in the file is not walk order (consecutive points can be 80 mm apart), so each
path is rebuilt from the line cells. Each artery is the geodesic path from the ostium flag
(start_points) to the farthest point carrying its label, keeping only its own labelled points
(so LM is cut off).

How points are joined: every point has an id and an xyz. Each line cell is a list of ids in walk
order; neighbours in a cell become an edge (line 48). Cells meeting at a bifurcation share that
point's id, which is what joins them. All edges of the file go into one sparse graph weighted by
length in mm (line 56), a tree, so the route from the ostium to any point is unique.

The path always starts at the ostium flag, so a same-label side branch can never replace the
proximal part. Example (case 100, LAD, junction at point 416): the farthest LAD point from the
ostium is the distal tip (104 mm past the junction), not the 5.5 mm twig, so the twig is dropped.
A twig longer than the distal arm would win the end, but the proximal arm would still be on the path.
The whole tree is used, not only the artery's label, because the junction point at the LM split
carries one child's label, so the other child connects to LM only through it.
"""
import numpy as np
import vtk
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components, dijkstra
from vtk.util.numpy_support import vtk_to_numpy

from . import paths

# name: (segment_label, tree), with the ImageCAS-X label scheme
ARTERIES = {"LAD": (2, "left"), "LCX": (3, "left"), "RCA": (9, "right")}


def read(path):
    """Points (n, 3) in mm, segment label per point, line-cell edges (m, 2) and ostium point ids."""
    r = vtk.vtkPolyDataReader()
    r.SetFileName(path)
    r.ReadAllScalarsOn()  # load segment_label (the SCALARS block)
    r.ReadAllFieldsOn()  # load the FIELD block: segment_name and start/branch/end flags
    r.Update()
    p = r.GetOutput()
    pts = vtk_to_numpy(p.GetPoints().GetData()).astype(np.float64)  # xyz in mm; row i = point id i, arbitrary order
    data = p.GetPointData()
    label = vtk_to_numpy(data.GetArray("segment_label"))  # 1 LM 2 LAD 3 LCX 4 D1 5 D2 6 OM1 7 OM2 | 9 RCA 10 R-PDA 11 R-PLA
    start = np.flatnonzero(vtk_to_numpy(data.GetArray("start_points")))  # ostium ids: on LM, or on LAD and LCX when there is no LM
    lines, ids, edges = p.GetLines(), vtk.vtkIdList(), []  # LINES section: cells = CONNECTIVITY sliced by OFFSETS
    lines.InitTraversal()  # cursor at cell 0
    while lines.GetNextCell(ids):  # fills ids with the next cell: one unbranched polyline, junction to junction/end
        c = [ids.GetId(i) for i in range(ids.GetNumberOfIds())]  # e.g. [241, 130, 43, ..., 763], in walk order
        edges += zip(c[:-1], c[1:])  # neighbours -> edges (241,130), (130,43); cells join via shared junction ids
    return pts, label, np.array(edges), start


def longest_path(pts, edges, a, targets):
    """Geodesic path from point id a to the farthest of the point ids targets, as ids with a first; None if none reachable."""
    n = len(pts)
    w = np.linalg.norm(pts[edges[:, 0]] - pts[edges[:, 1]], axis=1)  # edge length in mm, so distance = arc length
    g = coo_matrix((w, (edges[:, 0], edges[:, 1])), shape=(n, n)).tocsr()  # g[i, j] = length of edge i-j
    d, pred = dijkstra(g, directed=False, indices=a, return_predecessors=True)  # directed=False: each edge walkable both ways
    targets = targets[np.isfinite(d[targets])]  # inf = not connected to the ostium
    if not len(targets):
        return None
    path = [targets[np.argmax(d[targets])]]  # farthest target from the ostium
    while path[-1] != a:  # walk predecessors back to the ostium
        path.append(pred[path[-1]])
    return path[::-1]


def load_vessels(case_id):
    """{name: (n, 3) array in mm, ostium end first} for LAD, LCX and RCA.

    A name is absent when it has no ostium flag or no labelled point connected to it.
    """
    out = {}
    for side in ("left", "right"):
        pts, label, edges, start = read(paths.CENTERLINE.format(case=case_id, side=side))
        for name, (lab, s) in ARTERIES.items():
            a = start[np.isin(label[start], (1, lab))]  # this artery's ostium flag: on LM or on the artery itself
            if s != side or not len(a):
                continue
            path = longest_path(pts, edges, a[0], np.flatnonzero(label == lab))  # ostium -> farthest point with this label
            if path is not None:
                out[name] = pts[[i for i in path if label[i] == lab]]  # keep only the artery's own points: LM is cut off
    return out
