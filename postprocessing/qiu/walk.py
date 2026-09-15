"""The DPC (Distance-Probability-Cosine) walk, Qiu et al. section 3.3.2, eqs. 6-11.

From the head of a disconnected centerline the walker steps voxel by voxel toward a
candidate branch. At current point A, every neighbour A_k is scored

    D(A_k)  = -|A_k - p_m|                         eq. 6   (types 1, 2: toward endpoint p_m)
    D(A_k)  = -min_{p_t in branch} |A_k - p_t|     eq. 11  (type 3: toward the branch's side)
    PN(A_k) = min-max normalised P over the current neighbours     eq. 9
    C(A_k)  = cos(o_k, o_-1) + cos(o_k, o_-2)      eq. 8

    DPC = D + w*PN + C   if cos(o_-1, o_-2) <= 1/2,   else D + w*PN        eq. 10

where o_k is the step to A_k and o_-1, o_-2 the previous two steps. The best-scoring
neighbour is the next point. Neighbours are pre-filtered: already-stitched voxels are
excluded, and so is any step turning more than 90 degrees away from the overall
connection vector (types 1, 2) or from the history o_-1 and o_-1 + o_-2 (type 3).

Two neighbourhood levels (their "two-level neighbourhood set", side length 5): the
26-neighbourhood for short gaps, and the shell 2 <= |o| <= 3 of the 5^3 cube for long
ones, so the walker is not steered by voxels right next to it.
"""
from dataclasses import dataclass

import numpy as np

_CUBE = np.array([(i, j, k) for i in range(-2, 3) for j in range(-2, 3) for k in range(-2, 3)])
_NORM = np.linalg.norm(_CUBE, axis=1)
FIRST_LEVEL = _CUBE[(_NORM > 0) & (_NORM <= np.sqrt(3) + 1e-9)]
SECOND_LEVEL = _CUBE[(_NORM >= 2 - 1e-9) & (_NORM <= 3 + 1e-9)]


@dataclass
class WalkResult:
    path: np.ndarray       # (n, 3) voxels, path[0] is the start (the head)
    reached: bool
    reason: str


def _unit(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    return np.divide(v, n, out=np.zeros_like(v, dtype=float), where=n > 0)


def _segment_voxels(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Voxels on the straight segment a -> b, excluding a, including b. A second-level
    step jumps up to 3 voxels, and could otherwise hop straight over a thin vessel."""
    n = int(np.ceil(np.abs(b - a).max()))
    t = np.linspace(0, 1, n + 1)[1:]
    return np.unique(np.round(a[None] + t[:, None] * (b - a)[None]).astype(np.int64), axis=0)


def dpc_walk(start: np.ndarray, init_direction: np.ndarray, *, target_point: np.ndarray | None,
             target_tree, reached_label: np.ndarray, label_volume: np.ndarray,
             forbidden_label: np.ndarray, prob, blocked: set, omega: float,
             second_level: bool, max_steps: int) -> WalkResult:
    """One walk. `target_point` set -> eq. 6 toward an endpoint, with the connection-
    vector filter (types 1, 2). `target_point` None -> eq. 11 toward the nearest point
    of `target_tree` (a cKDTree over the candidate branch), with the history filter
    (type 3).

    The walk ends as soon as it enters a voxel whose label in `label_volume` is flagged
    in `reached_label`; it fails on entering one flagged in `forbidden_label` (the other
    main tree, which a join must never bridge to), on running out of admissible
    neighbours, or after `max_steps`.
    """
    offsets = SECOND_LEVEL if second_level else FIRST_LEVEL
    unit_offsets = _unit(offsets.astype(float))
    shape = np.array(label_volume.shape)

    path = [np.asarray(start, dtype=np.int64)]
    visited = {tuple(path[0])}
    o1 = o2 = _unit(np.asarray(init_direction, dtype=float))

    for _ in range(max_steps):
        a = path[-1]
        cand = a[None] + offsets
        keep = np.all((cand >= 0) & (cand < shape), axis=1)
        keep &= np.array([tuple(c) not in visited and tuple(c) not in blocked for c in cand])

        if target_point is not None:
            keep &= unit_offsets @ (target_point - a) >= 0
        else:
            keep &= (unit_offsets @ o1 >= 0) & (unit_offsets @ (o1 + o2) >= -1e-9)
        if not keep.any():
            return WalkResult(np.array(path), False, "no_admissible_neighbour")

        cand, uo = cand[keep], unit_offsets[keep]
        if target_point is not None:
            d = -np.linalg.norm(cand - target_point, axis=1)
        else:
            d = -target_tree.query(cand)[0]
        p = prob(cand)
        span = p.max() - p.min()
        pn = (p - p.min()) / span if span > 0 else np.zeros_like(p)
        score = d + omega * pn
        if float(o1 @ o2) <= 0.5:
            score = score + uo @ o1 + uo @ o2

        nxt = cand[int(np.argmax(score))]
        seg = _segment_voxels(a, nxt)
        labels = label_volume[seg[:, 0], seg[:, 1], seg[:, 2]]
        if forbidden_label[labels].any():
            return WalkResult(np.array(path + [nxt]), False, "entered_other_main_tree")
        hit = np.flatnonzero(reached_label[labels])
        if hit.size:
            path.append(seg[hit[0]])
            return WalkResult(np.array(path), True, "reached")

        o2, o1 = o1, _unit((nxt - a).astype(float))
        path.append(nxt)
        visited.add(tuple(nxt))
    return WalkResult(np.array(path), False, "max_steps")
