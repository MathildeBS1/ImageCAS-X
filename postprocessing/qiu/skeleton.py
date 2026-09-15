"""Prediction component -> the centerline representation Qiu et al. section 3.3 works on.

Everything here lives on the 0.5 mm isotropic grid, in integer voxel indices [x, y, z],
so Euclidean distance between indices is distance in half-millimetres.

A component is skeletonised (skimage, Lee's 3D thinning) and the 26-connected
skeleton is split into branches: maximal chains between key voxels, a key voxel being
any whose skeleton degree is not 2. Degree-1 voxels are the endpoints, which the paper
calls "opening points": the tails a disconnected vessel may be joined onto, or the
heads a disconnected vessel is joined from.
"""
from dataclasses import dataclass, field

import numpy as np
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
from skimage.morphology import skeletonize

_NEIGHBOURS = np.array([(i, j, k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)
                        if (i, j, k) != (0, 0, 0)])


@dataclass
class Endpoint:
    point: np.ndarray        # (3,) int voxel index
    direction: np.ndarray    # (3,) unit vector pointing OUT of the vessel at this tip
    radius_mm: float
    branch: np.ndarray       # the terminal branch this tip ends, ordered tip -> inward


@dataclass
class Centerline:
    """Skeleton of one or more prediction components.

    `points` / `radius_mm` are all skeleton voxels. `branches` are ordered point arrays.
    `endpoints` are the degree-1 tips with outward directions.
    """
    points: np.ndarray
    radius_mm: np.ndarray
    branches: list
    endpoints: list
    axis: np.ndarray                      # principal axis of the component voxels
    _tree: cKDTree = field(default=None, repr=False)

    @property
    def tree(self) -> cKDTree:
        if self._tree is None:
            self._tree = cKDTree(self.points)
        return self._tree

    def length_vox(self) -> float:
        return float(sum(np.linalg.norm(np.diff(b, axis=0), axis=1).sum()
                         for b in self.branches if len(b) > 1))

    def radius_at(self, point: np.ndarray) -> float:
        _, i = self.tree.query(point)
        return float(self.radius_mm[i])


def _trace_branches(pts: np.ndarray) -> tuple[list, np.ndarray, list]:
    """Split a voxel skeleton into branches. Returns (branches as index lists,
    degree per point, neighbour lists)."""
    index = {tuple(p): i for i, p in enumerate(pts)}
    nbrs = []
    for p in pts:
        nbrs.append([index[t] for t in map(tuple, p + _NEIGHBOURS) if t in index])
    deg = np.array([len(n) for n in nbrs])

    branches, seen = [], set()
    for k in np.flatnonzero(deg != 2):
        if deg[k] == 0:
            branches.append([k])
            continue
        for n in nbrs[k]:
            if (k, n) in seen:
                continue
            path, prev, cur = [k, n], k, n
            seen.update({(k, n), (n, k)})
            while deg[cur] == 2:
                nxt = nbrs[cur][0] if nbrs[cur][0] != prev else nbrs[cur][1]
                if (cur, nxt) in seen:
                    break
                seen.update({(cur, nxt), (nxt, cur)})
                path.append(nxt)
                prev, cur = cur, nxt
            branches.append(path)

    # Pure cycles have no key voxel; take each as one closed branch.
    on_branch = {i for b in branches for i in b}
    for start in range(len(pts)):
        if start in on_branch or deg[start] != 2:
            continue
        path, prev, cur = [start], None, start
        while True:
            on_branch.add(cur)
            nxt = [n for n in nbrs[cur] if n != prev and n not in on_branch]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            path.append(cur)
        branches.append(path)
    return branches, deg, nbrs


def _prune_spurs(pts: np.ndarray, min_len: int) -> np.ndarray:
    """Drop terminal branches shorter than `min_len` voxels, once. Surface bumps give
    Lee thinning short side twigs, and each would otherwise become a fake tail with a
    meaningless direction for a fragment to be joined onto."""
    if min_len <= 1 or len(pts) < 3:
        return pts
    branches, deg, _ = _trace_branches(pts)
    drop = set()
    for b in branches:
        if len(b) < 2:
            continue
        ends = deg[b[0]], deg[b[-1]]
        terminal_spur = (1 in ends) and (max(ends) >= 3)
        if terminal_spur and len(b) < min_len:
            drop.update(i for i in b if deg[i] < 3)   # keep the junction voxel
    if not drop:
        return pts
    return pts[[i for i in range(len(pts)) if i not in drop]]


def _tip_direction(branch_pts: np.ndarray, n_points: int) -> np.ndarray | None:
    """Outward unit vector at branch_pts[0] from `n_points` consecutive points (the
    paper uses three). None if the branch is too short to define one."""
    if len(branch_pts) < 2:
        return None
    far = branch_pts[min(n_points - 1, len(branch_pts) - 1)]
    v = branch_pts[0].astype(float) - far
    n = np.linalg.norm(v)
    return v / n if n > 0 else None


def build_centerline(component: np.ndarray, offset: np.ndarray, grid_mm: float,
                     spur_min_len: int = 4, direction_points: int = 3) -> Centerline:
    """Centerline of a boolean component crop whose [0,0,0] sits at global `offset`."""
    padded = np.pad(component, 1)
    skel = skeletonize(padded)[1:-1, 1:-1, 1:-1].astype(bool)
    edt = ndi.distance_transform_edt(component, sampling=grid_mm)

    vox = np.argwhere(component)
    centred = vox - vox.mean(axis=0)
    if len(vox) > 1:
        axis = np.linalg.svd(centred, full_matrices=False)[2][0]
    else:
        axis = np.array([1.0, 0.0, 0.0])

    local = np.argwhere(skel)
    if len(local) == 0:
        # Too small to thin: the component is represented by its innermost voxel.
        local = vox[[np.argmax(edt[tuple(vox.T)])]]
    local = _prune_spurs(local, spur_min_len)

    branches_idx, deg, _ = _trace_branches(local)
    radius = edt[tuple(local.T)]
    pts = local + offset

    branches, endpoints = [], []
    for b in branches_idx:
        bp = pts[b]
        branches.append(bp)
        for end, seq in ((b[0], bp), (b[-1], bp[::-1])):
            if deg[end] != 1:
                continue
            d = _tip_direction(seq, direction_points)
            if d is None:
                continue
            endpoints.append(Endpoint(point=pts[end], direction=d,
                                      radius_mm=float(radius[end]), branch=seq))
    return Centerline(points=pts, radius_mm=radius, branches=branches,
                      endpoints=endpoints, axis=axis)


def merge(parts: list, extra_points: list = (), extra_radius: list = ()) -> Centerline:
    """Union of several centerlines, plus stitched paths as extra branches.
    Endpoints are the union; the caller removes the ones a join consumed."""
    pts = [c.points for c in parts] + list(extra_points)
    rad = [c.radius_mm for c in parts] + list(extra_radius)
    branches = [b for c in parts for b in c.branches] + list(extra_points)
    endpoints = [e for c in parts for e in c.endpoints]
    axis = max(parts, key=lambda c: len(c.points)).axis
    return Centerline(points=np.concatenate(pts), radius_mm=np.concatenate(rad),
                      branches=branches, endpoints=endpoints, axis=axis)
