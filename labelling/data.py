"""Coronary trees as graphs for the segment labeller.

    python -m labelling.data --source delivered --split train      # also val, test
    python -m labelling.data --source cas_net_pretrained_t3 --split test

A tree is prepared once per case and side (``prepare``) into a list of ``Seg``s in a heart frame,
cached as ``PREPARED/<source>/<id>_<side>.pkl``; training then augments and featurises it on the
fly. ``--source delivered`` reads the delivered centerlines and their ``segment_label``; any other
source is a folder under ``bifurcation.paths.EXTRACTED`` whose points take the label of the
nearest delivered point within its GT radius (floored at 0.35 mm), else ``SPURIOUS``.

Heart frame (Hampe et al. 2024 found location the strongest feature group): origin at the LV
centroid, z along the LV long axis towards the apex (away from the LA), x towards the RV.
Chambers come from TotalSegmentator heartchambers_highres (``jobs/totalseg_heart.sh``).

Graph nodes are pieces of at most ``PIECE_MM`` of a segment, so a predicted segment that spans two
delivered labels (a missed side branch) is not forced to one label.
"""

from __future__ import annotations

import argparse
import pickle
from dataclasses import dataclass, replace

import nibabel as nib
import numpy as np
from scipy.spatial import cKDTree

from bifurcation import coords, graph, io, paths, radius, skeleton

PREPARED = paths.RESULTS / "labeller" / "prepared"
CHAMBERS = ("heart_ventricle_left", "heart_atrium_left", "heart_ventricle_right", "heart_atrium_right")
LEFT = (1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14)  # 14 "Other" never occurs on the right
RIGHT = (9, 10, 11)
CLASSES = {"left": LEFT, "right": RIGHT}
SPURIOUS = -1
PIECE_MM = 15.0
TOL_FLOOR_MM = 0.35


@dataclass
class Seg:
    pts: np.ndarray  # (n, 3) heart frame, mm
    rad: np.ndarray  # (n,) mm
    lab: np.ndarray  # (n,) segment_label, 0 remapped to 14; SPURIOUS where nothing matches
    cham: np.ndarray  # (n, 4) distance to the CHAMBERS surfaces, mm
    parent: int  # index into the tree's list, -1 for a root


def heart_frame(case_id: int):
    """``(origin, R, chamber surface trees)``; heart-frame points are ``(p - origin) @ R.T``."""
    vox = {}
    for s in CHAMBERS:
        img = nib.load(paths.totalseg_path(case_id, s))
        m = np.asarray(img.dataobj) > 0
        vox[s] = (m, img.affine)
    lv = coords.voxel_to_lps(np.argwhere(vox["heart_ventricle_left"][0]), vox["heart_ventricle_left"][1])
    c = lv.mean(0)
    z = np.linalg.svd(lv - c, full_matrices=False)[2][0]
    la = coords.voxel_to_lps(np.argwhere(vox["heart_atrium_left"][0]), vox["heart_atrium_left"][1]).mean(0)
    z = -z if np.dot(la - c, z) > 0 else z
    rv = coords.voxel_to_lps(np.argwhere(vox["heart_ventricle_right"][0]), vox["heart_ventricle_right"][1]).mean(0)
    x = (rv - c) - np.dot(rv - c, z) * z
    x /= np.linalg.norm(x)
    R = np.stack([x, np.cross(z, x), z])
    trees = [cKDTree(skeleton.surface_points(*vox[s])) for s in CHAMBERS]
    return c, R, trees


def _delivered_labels(case_id: int):
    """All delivered points of a case with their label and GT radius, for label transfer."""
    pts, lab, rad = [], [], []
    for side, cl in io.load_centerlines(case_id).items():
        r = cl.radius if cl.radius is not None else radius.compute_gt_radius(case_id)[side]
        pts.append(cl.points), lab.append(cl.segment_label), rad.append(r)
    return np.concatenate(pts), np.concatenate(lab).astype(int), np.concatenate(rad)


def prepare(case_id: int, side: str, source: str) -> list[Seg]:
    root = None if source == "delivered" else paths.EXTRACTED / source
    cl = io.load_centerline(case_id, side, root)
    if len(cl.points) == 0:
        return []
    if source == "delivered":
        lab = np.asarray(cl.segment_label, dtype=int)
        if cl.radius is None:
            cl.radius = radius.compute_gt_radius(case_id)[side]
    else:
        g_pts, g_lab, g_rad = _delivered_labels(case_id)
        d, j = cKDTree(g_pts).query(cl.points)
        lab = np.where(d <= np.maximum(g_rad[j], TOL_FLOOR_MM), g_lab[j], SPURIOUS)
    lab = np.where(lab == 0, 14, lab)
    tree = graph.build_tree(cl)
    c, R, trees = heart_frame(case_id)
    cham = np.stack([t.query(cl.points)[0] for t in trees], axis=1)
    hf = (cl.points - c) @ R.T
    order = list(tree.walk())
    pos = {s.index: k for k, s in enumerate(order)}
    return [Seg(pts=hf[s.point_indices], rad=cl.radius[s.point_indices], lab=lab[s.point_indices],
                cham=cham[s.point_indices], parent=-1 if s.parent is None else pos[s.parent])
            for s in order]


# --- augmentation -----------------------------------------------------------------------------

def _children(segs: list[Seg]) -> list[list[int]]:
    ch = [[] for _ in segs]
    for k, s in enumerate(segs):
        if s.parent >= 0:
            ch[s.parent].append(k)
    return ch


def _reorder(segs: list[Seg], drop: set[int] = frozenset()) -> list[Seg]:
    """Pre-order, without ``drop`` and everything below it. A segment left with one child is no
    longer a junction, so the two are concatenated, as extraction would."""
    ch = [[c for c in cs if c not in drop] for cs in _children(segs)]
    out: list[Seg] = []

    def emit(k: int, parent: int) -> None:
        parts = [segs[k]]
        while len(ch[k]) == 1:
            k = ch[k][0]
            parts.append(segs[k])
        cat = lambda f: np.concatenate([getattr(parts[0], f)] + [getattr(p, f)[1:] for p in parts[1:]])
        out.append(Seg(cat("pts"), cat("rad"), cat("lab"), cat("cham"), parent))
        me = len(out) - 1
        for c in ch[k]:
            emit(c, me)

    for k, g in enumerate(segs):
        if g.parent < 0 and k not in drop:
            emit(k, -1)
    return out


def augment(segs: list[Seg], rng: np.random.Generator) -> list[Seg]:
    """Rotation +-15 deg, scale +-10 %, deletion of short terminals and of whole internal subtrees,
    and synthetic spurs, so delivered trees look like extracted ones in both directions."""
    axis = rng.normal(size=3)
    axis /= np.linalg.norm(axis)
    a = np.deg2rad(rng.uniform(-15, 15))
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    Rot = np.eye(3) + np.sin(a) * K + (1 - np.cos(a)) * K @ K
    s = rng.uniform(0.9, 1.1)
    segs = [replace(g, pts=g.pts @ Rot.T * s, rad=g.rad * s, cham=g.cham * s) for g in segs]

    ch = _children(segs)
    drop = set()
    for k, g in enumerate(segs):
        if not ch[k] and g.parent >= 0 and _length(g.pts) < 10 and rng.random() < 0.3:
            drop.add(k)
    inner = [k for k, g in enumerate(segs) if g.parent >= 0]
    if inner and rng.random() < 0.5:
        drop.add(int(rng.choice(inner)))
    segs = _reorder(segs, drop)

    for _ in range(rng.integers(0, 4)):
        long = [k for k, g in enumerate(segs) if len(g.pts) > 8]
        if not long:
            break
        k = int(rng.choice(long))
        g, i = segs[k], int(rng.integers(3, len(segs[k].pts) - 3))
        head = Seg(g.pts[:i + 1], g.rad[:i + 1], g.lab[:i + 1], g.cham[:i + 1], g.parent)
        tail = Seg(g.pts[i:], g.rad[i:], g.lab[i:], g.cham[i:], k)
        d = rng.normal(size=3)
        n = int(rng.uniform(2, 10) / 0.5)
        spur_pts = g.pts[i] + np.outer(np.arange(n + 1) * 0.5, d / np.linalg.norm(d))
        spur = Seg(spur_pts, np.full(n + 1, rng.uniform(0.3, 0.8)), np.full(n + 1, SPURIOUS),
                   np.repeat(g.cham[i:i + 1], n + 1, axis=0), k)
        tail_idx = len(segs)
        segs = [replace(x, parent=tail_idx if x.parent == k else x.parent) for x in segs]
        segs[k] = head
        segs += [tail, spur]
        segs = _reorder(segs)
    return segs


# --- features -----------------------------------------------------------------------------------

def _length(p: np.ndarray) -> float:
    return float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum())


def _unit(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


@dataclass
class Graph:
    x: np.ndarray  # (P, F) piece features
    parent: np.ndarray  # (P,) piece index, -1 for roots
    y: np.ndarray  # (P,) class index within the side's CLASSES, -1 = no target
    lab: list[np.ndarray]  # per piece, point labels (segment_label ids, or SPURIOUS)
    w: list[np.ndarray]  # per piece, point weights: mm of centerline each point stands for
    side: str


def featurize(segs: list[Seg], side: str) -> Graph:
    ch = _children(segs)
    n_sub = np.ones(len(segs))
    len_sub = np.array([_length(g.pts) for g in segs])
    for k in reversed(range(len(segs))):  # pre-order reversed: children before parents
        for c in ch[k]:
            n_sub[k] += n_sub[c]
            len_sub[k] += len_sub[c]
    depth, geo0 = np.zeros(len(segs)), np.zeros(len(segs))
    ostium = {}
    root_of = np.zeros(len(segs), dtype=int)
    for k, g in enumerate(segs):
        if g.parent >= 0:
            depth[k] = depth[g.parent] + 1
            geo0[k] = geo0[g.parent] + _length(segs[g.parent].pts)
            root_of[k] = root_of[g.parent]
        else:
            root_of[k] = k
            ostium[k] = g.pts[0]

    x, parent, y, labs, ws, last_piece, end_dir = [], [], [], [], [], {}, {}
    cls = {l: i for i, l in enumerate(CLASSES[side])}
    for k, g in enumerate(segs):
        arc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(g.pts, axis=0), axis=1))])
        n_pieces = max(int(np.ceil(arc[-1] / PIECE_MM)), 1)
        cuts = np.unique(np.searchsorted(arc, np.linspace(0, arc[-1], n_pieces + 1)))
        cuts[0], cuts[-1] = 0, len(g.pts) - 1
        for q, (a, b) in enumerate(zip(cuts[:-1], cuts[1:])):
            if b <= a:
                continue
            p, r = g.pts[a:b + 1], g.rad[a:b + 1]
            par = (last_piece[g.parent] if g.parent >= 0 else -1) if q == 0 else len(x) - 1
            d_in = _unit(p[min(3, len(p) - 1)] - p[0])
            cos_par = float(np.dot(d_in, end_dir[par])) if par >= 0 else 1.0
            seg_len = np.linalg.norm(np.diff(p, axis=0), axis=1)
            w = np.zeros(len(p))
            w[:-1] += seg_len / 2
            w[1:] += seg_len / 2
            chord = np.linalg.norm(p[-1] - p[0])
            x.append(np.concatenate([
                [_length(p), chord, _length(p) / chord if chord > 0 else 1.0, r.mean(), r[0]],
                p[0], p[-1], p.mean(0), _unit(p[-1] - p[0]), p.mean(0) - ostium[root_of[k]],
                g.cham[a:b + 1].mean(0),
                [depth[k], n_sub[k], len_sub[k], len(ch[k]), cos_par, geo0[k] + arc[a],
                 q / n_pieces, float(not ch[k]), float(g.parent < 0)],
            ]))
            end_dir[len(x) - 1] = _unit(p[-1] - p[max(len(p) - 4, 0)])
            parent.append(par)
            l = g.lab[a:b + 1]
            inner = l[1:-1] if len(l) > 2 else l
            inner = inner[inner != SPURIOUS]
            y.append(cls.get(int(np.bincount(inner).argmax()), -1) if len(inner) else -1)
            labs.append(l), ws.append(w)
        last_piece[k] = len(x) - 1
    return Graph(np.asarray(x, dtype=np.float32), np.asarray(parent), np.asarray(y), labs, ws, side)


def load(source: str, split: str) -> list[tuple[int, str, list[Seg]]]:
    out = []
    for case in paths.split_ids(split):
        for side in ("left", "right"):
            f = PREPARED / source / f"{case}_{side}.pkl"
            if f.exists():
                out.append((case, side, pickle.loads(f.read_bytes())))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="delivered", help="'delivered' or a folder under EXTRACTED")
    ap.add_argument("--split", default="train", choices=["train", "val", "test"])
    args = ap.parse_args()
    out = PREPARED / args.source
    out.mkdir(parents=True, exist_ok=True)
    failed = []
    for case in paths.split_ids(args.split):
        for side in ("left", "right"):
            try:
                (out / f"{case}_{side}.pkl").write_bytes(pickle.dumps(prepare(case, side, args.source)))
            except Exception as exc:  # logged per case, never dropped silently
                failed.append(f"{case}\t{side}\t{type(exc).__name__}: {exc}")
    (out / f"failed_{args.split}.txt").write_text("".join(f + "\n" for f in failed))
    print(f"{args.source} {args.split}: {len(failed)} failed -> {out}")


if __name__ == "__main__":
    main()
