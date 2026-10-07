"""Centerlines from a lumen mask, built the way ImageCAS-X built its delivered ones.

Bransby et al. 2026 (Methods, "Postprocessing"): skeletonise the mask (Lee et al. 1994), Gaussian
smooth (sigma = 0.5 mm, 5-vertex window), start points on degree-1 vertices within 5 mm of a
TotalSegmentator aorta, end points on the other degree-1 vertices, bifurcations on degree >= 3.
Spurious branches were removed by hand. This module does all of it without ground truth:

1. fill enclosed cavities, skeletonise on the native (anisotropic) grid -- 96-97 % of delivered
   end and junction points sit on native voxel centres -- and trace with ``skan``;
2. contract the sub-2-voxel junction-to-junction paths skan leaves inside junction clusters;
3. smooth each path with junction and end points fixed;
4. prune spurs by bulge size (Drees et al. 2021), never re-smoothing afterwards, which is what
   the unsmoothed degree-2 former junctions in the delivered trees show Bransby did too;
5. break cycles at the chain with the thinnest lumen;
6. place ostia from the aorta, split left from right by tree centroid, keep orphan fragments.

Every departure from the paper (automatic pruning, contraction, cycle rule, side rule, orphans,
the ostium cap) is a recorded deviation; see ``knowledge/docs_thesis/centerline_labelling.md``.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree
from skan import Skeleton
from skimage.morphology import skeletonize

from . import coords, graph, io, radius

RADIUS_FLOOR_MM = 0.1  # keeps the bulge ratio finite on single-voxel branches
ORPHAN_MIN_MM = 5.0  # ostium-less components shorter than this are dropped (and logged)
FALLBACK_MIN_MM = 20.0  # smallest component that may receive a fallback ostium
SIDE_TIE_MM = 5.0  # centroid x closer than this: decide left/right by ostium y instead


def skeleton_graph(mask: np.ndarray, affine: np.ndarray) -> tuple[np.ndarray, np.ndarray, list[np.ndarray]]:
    """Voxel indices (N, 3), LPS points (N, 3) and point-index polylines of the mask's skeleton.
    Polylines share the index of the junction they meet at."""
    idx = np.argwhere(mask)
    lo = np.maximum(idx.min(0) - 1, 0)
    hi = np.minimum(idx.max(0) + 2, mask.shape)
    skel = skeletonize(mask[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]])
    sk = Skeleton(skel)
    paths_ = [np.asarray(sk.path(i), dtype=int) for i in range(sk.n_paths)]
    used = np.unique(np.concatenate(paths_)) if paths_ else np.zeros(0, int)
    remap = np.full(len(sk.coordinates), -1)
    remap[used] = np.arange(len(used))
    ijk = np.round(sk.coordinates[used]).astype(int) + lo
    return ijk, coords.voxel_to_lps(ijk, affine), [remap[p] for p in paths_]


def _degree(n: int, lines: list[np.ndarray]) -> np.ndarray:
    deg = np.zeros(n, dtype=int)
    for line in lines:
        deg[line[0]] += 1
        deg[line[-1]] += 1
    return deg


def _arc(p: np.ndarray) -> float:
    return float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum())


def _find(parent: np.ndarray, x: int) -> int:
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def _merge_degree2(n: int, lines: list[np.ndarray], keep: set[int] = frozenset()) -> list[np.ndarray]:
    """Glue polylines through points of degree 2 (except ``keep``), so every line runs between
    junctions or ends."""
    lines = [l for l in lines if len(l) > 1]
    while True:
        deg = _degree(n, lines)
        ends = defaultdict(list)
        for k, l in enumerate(lines):
            ends[int(l[0])].append(k)
            ends[int(l[-1])].append(k)
        node = next((v for v, ks in ends.items() if deg[v] == 2 and v not in keep
                     and len(ks) == 2 and ks[0] != ks[1]), None)
        if node is None:
            return lines
        a, b = (lines[k] for k in ends[node])
        a = a if a[-1] == node else a[::-1]
        b = b if b[0] == node else b[::-1]
        lines = [l for k, l in enumerate(lines) if k not in ends[node]] + [np.concatenate([a, b[1:]])]


def contract_junctions(points: np.ndarray, lines: list[np.ndarray], max_mm: float) -> list[np.ndarray]:
    """Collapse junction-to-junction paths shorter than ``max_mm`` into one node (skan resolves a
    junction cluster into a minimum spanning tree of short paths; the delivered trees have 2 of
    575 internal segments under 1 mm)."""
    deg = _degree(len(points), lines)
    parent = np.arange(len(points))
    short = [k for k, l in enumerate(lines)
             if deg[l[0]] >= 3 and deg[l[-1]] >= 3 and _arc(points[l]) < max_mm]
    for k in short:
        a, b = _find(parent, int(lines[k][0])), _find(parent, int(lines[k][-1]))
        parent[max(a, b)] = min(a, b)
    root = np.array([_find(parent, i) for i in range(len(points))])
    out = []
    for k, l in enumerate(lines):
        if k in short:
            continue
        l = l.copy()
        l[0], l[-1] = root[l[0]], root[l[-1]]
        out.append(l)
    return out


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


def bulge(points: np.ndarray, line: np.ndarray, rad: np.ndarray) -> float:
    """Drees et al. 2021 bulge size of a terminal line running junction -> tip: the length that
    protrudes beyond the parent wall, plus the tip radius thinning ate, over the branch's own
    mean radius."""
    r = np.maximum(rad[line], RADIUS_FLOOR_MM)
    return (_arc(points[line]) - r[0] + r[-1]) / r[1:].mean() if len(line) > 2 else \
        (_arc(points[line]) - r[0] + r[-1]) / r[-1]


def prune_spurs(points: np.ndarray, lines: list[np.ndarray], rad: np.ndarray, t: float,
                protect: np.ndarray) -> tuple[list[np.ndarray], int]:
    """Remove terminal lines with bulge < ``t``, smallest first, recomputing after each removal.
    A spur is only removed while its junction keeps two other lines, so a short fork cannot erode
    into its parent. Tips flagged in ``protect`` (ostium candidates) are never removed."""
    removed = 0
    while True:
        deg = _degree(len(points), lines)
        cands = []
        for k, l in enumerate(lines):
            j, tip = (l[0], l[-1]) if deg[l[-1]] == 1 else (l[-1], l[0])
            if deg[tip] == 1 and deg[j] >= 3 and not protect[tip]:
                oriented = l if l[0] == j else l[::-1]
                cands.append((bulge(points, oriented, rad), k))
        if not cands or min(cands)[0] >= t:
            return lines, removed
        k = min(cands)[1]
        lines = _merge_degree2(len(points), [l for i, l in enumerate(lines) if i != k])
        removed += 1


def break_cycles(points: np.ndarray, lines: list[np.ndarray], rad: np.ndarray) -> tuple[list[np.ndarray], int]:
    """Maximum spanning forest by each line's thinnest radius: every cycle loses its thinnest
    chain. Self-loops always go."""
    parent = np.arange(len(points))
    order = sorted(range(len(lines)), key=lambda k: -rad[lines[k]].min())
    keep = []
    for k in order:
        a, b = _find(parent, int(lines[k][0])), _find(parent, int(lines[k][-1]))
        if a != b:
            parent[a] = b
            keep.append(k)
    dropped = len(lines) - len(keep)
    return _merge_degree2(len(points), [lines[k] for k in sorted(keep)]), dropped


def _components(n: int, lines: list[np.ndarray]) -> list[list[int]]:
    """Line indices per connected component."""
    parent = np.arange(n)
    for l in lines:
        a, b = _find(parent, int(l[0])), _find(parent, int(l[-1]))
        parent[a] = b
    groups = defaultdict(list)
    for k, l in enumerate(lines):
        groups[_find(parent, int(l[0]))].append(k)
    return list(groups.values())


def surface_points(mask: np.ndarray, affine: np.ndarray) -> np.ndarray:
    """LPS centres of the mask's boundary voxels."""
    mask = np.asarray(mask) > 0
    return coords.voxel_to_lps(np.argwhere(mask & ~ndimage.binary_erosion(mask)), affine)


def centerlines_from_mask(case_id: int, mask: np.ndarray, affine: np.ndarray,
                          aorta_pts: np.ndarray, t: float, cap_mm: float):
    """Left and right ``io.Centerline`` from a binary lumen mask, with no ground truth.

    ``aorta_pts`` are LPS points the ostia must lie within ``cap_mm`` of: the aorta surface, or,
    for an oracle check, the delivered start points. Returns ``(centerlines, notes)``; ``notes``
    is a dict for the per-case JSON.
    """
    mask = ndimage.binary_fill_holes(np.asarray(mask) > 0)
    ijk, points, lines = skeleton_graph(mask, affine)
    spacing = np.linalg.norm(affine[:3, :3], axis=0)
    lines = contract_junctions(points, lines, 2 * spacing.max())
    lines = _merge_degree2(len(points), lines)
    rad = radius.radius_at(points, mask, affine)
    points = smooth(points, lines)

    d_aorta = cKDTree(aorta_pts).query(points)[0]
    deg = _degree(len(points), lines)
    candidate = (deg == 1) & (d_aorta <= cap_mm)
    lines, n_pruned = prune_spurs(points, lines, rad, t, candidate)
    lines, n_cycles = break_cycles(points, lines, rad)
    deg = _degree(len(points), lines)

    notes = {"n_pruned": n_pruned, "n_cycles_broken": n_cycles, "fallback_ostia": 0,
             "fused_components": 0, "orphan_mm": 0.0, "dropped_mm": 0.0, "side_rule": "centroid_x"}
    comps = _components(len(points), lines)
    comp_pts = [np.unique(np.concatenate([lines[k] for k in c])) for c in comps]
    comp_len = [sum(_arc(points[lines[k]]) for k in c) for c in comps]

    # One ostium per component: the degree-1 vertex nearest the aorta within the cap.
    ostium = {}
    for c, pts in enumerate(comp_pts):
        cand = pts[(deg[pts] == 1) & (d_aorta[pts] <= cap_mm)]
        if len(cand):
            ostium[c] = int(cand[np.argmin(d_aorta[cand])])
            if np.ptp(points[cand], axis=0).max() > 20.0:
                notes["fused_components"] += 1  # ostium candidates far apart: L and R joined
    # Fewer than two trees rooted: give the largest remaining components their tip nearest the aorta.
    for c in sorted(range(len(comps)), key=lambda c: -comp_len[c]):
        if len(ostium) >= 2 or comp_len[c] < FALLBACK_MIN_MM:
            break
        if c not in ostium:
            tips = comp_pts[c][deg[comp_pts[c]] == 1]
            if len(tips):
                ostium[c] = int(tips[np.argmin(d_aorta[tips])])
                notes["fallback_ostia"] += 1

    # Side: the rooted tree with the smallest centroid x (patient right) is right, the rest left.
    side_of = {}
    rooted = sorted(ostium, key=lambda c: points[comp_pts[c]].mean(0)[0])
    if len(rooted) == 2:
        a, b = rooted
        if abs(points[comp_pts[a]].mean(0)[0] - points[comp_pts[b]].mean(0)[0]) < SIDE_TIE_MM:
            rooted = sorted(rooted, key=lambda c: points[ostium[c]][1])  # left is more posterior
            notes["side_rule"] = "ostium_y"
    for i, c in enumerate(rooted):
        side_of[c] = "right" if i == 0 else "left"

    # Orphans join the nearest rooted side, rooted later by graph.build_tree; slivers are dropped.
    if side_of:
        side_tree = {s: cKDTree(points[np.concatenate([comp_pts[c] for c in side_of if side_of[c] == s])])
                     for s in set(side_of.values())}
    for c in range(len(comps)):
        if c in side_of:
            continue
        if comp_len[c] < ORPHAN_MIN_MM or not side_of:
            notes["dropped_mm"] += comp_len[c]
            continue
        d = {s: tr.query(points[comp_pts[c]])[0].min() for s, tr in side_tree.items()}
        side_of[c] = min(d, key=d.get)
        notes["orphan_mm"] += comp_len[c]

    out = {}
    for side in ("left", "right"):
        ks = [k for c, s in side_of.items() if s == side for k in comps[c]]
        used = np.unique(np.concatenate([lines[k] for k in ks])) if ks else np.zeros(0, int)
        new = -np.ones(len(points), dtype=int)
        new[used] = np.arange(len(used))
        sub = [new[lines[k]] for k in ks]
        d = _degree(len(used), sub)
        start = np.zeros(len(used), dtype=int)
        for c, s in side_of.items():
            if s == side and c in ostium:
                start[new[ostium[c]]] = 1
        out[side] = io.Centerline(
            case_id=case_id, side=side, points=points[used],
            segment_label=np.zeros(len(used), dtype=int),
            segment_name=np.array([graph.artery_name(0)] * len(used)),
            branch_points=(d >= 3).astype(int), end_points=((d == 1) & (start == 0)).astype(int),
            start_points=start, lines=sub, radius=rad[used],
        )
        notes[f"{side}_ostia"] = int(start.sum())
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
