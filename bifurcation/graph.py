"""Rooted vessel trees built from the dataset's centerlines.

The centerlines already encode the tree: points are unique, physical-mm, and
VTK polylines meet only at shared point indices, so degree at a point is degree
in the graph -- ``end_points``/``branch_points`` match degree 1/>=3 on all 1600
sides. Degree-2 points are mid-vessel pass-throughs, merged so one ``Segment``
spans junction to junction.

1584 of 1600 sides build as one clean rooted tree. The other 16 are real
anatomy, not corruption, and handled explicitly (see ``CoronaryTree.warnings``):
11 left sides have two ostia (absent ``LM``, LAD/LCX arise separately), 2 left
sides fragment into an orphan piece rooted at its nearest point, 3 sides
contain a cycle whose closing edge is dropped into ``chords``.

Every count above was derived by a cohort survey that is not in the repo; treat them
as recorded observations, not as invariants this module enforces.
"""

from __future__ import annotations

import json
from collections import defaultdict, deque
from dataclasses import dataclass
from functools import lru_cache

import numpy as np

from . import io, paths

OSTIUM = "ostium"
BIFURCATION = "bifurcation"
TERMINUS = "terminus"
#: Only arises on the 3 sides with a cycle: dropping the cycle-closing edge leaves a
#: node with one child, which is a junction in the raw data but not a branch point.
PASSTHROUGH = "pass-through"

#: Label 14 is a documented catch-all, and one file (case 272, left) encodes it as
#: 0. Both mean "not attributed to a named artery" -- never treat them as a vessel.
UNLABELLED = "Other"


@lru_cache(maxsize=1)
def label_names() -> dict[int, str]:
    """Canonical label -> artery name, from ``knowledge/docs_thesis/label_map.json`` (see ``paths.LABEL_MAP``)."""
    raw = json.loads(paths.LABEL_MAP.read_text())
    return {int(k): v for k, v in raw.items()}


def artery_name(label: int) -> str:
    return label_names().get(int(label), UNLABELLED)


@dataclass(frozen=True)
class Node:
    """A junction of the tree: an ostium, a bifurcation, or a vessel terminus."""

    index: int  # index into the centerline's point array
    position: np.ndarray  # (3,) LPS mm
    degree: int  # incident chains in the raw centerline, before any chord removal
    kind: str  # derived from the built tree, not from ``degree`` -- see PASSTHROUGH


@dataclass
class Segment:
    """One vessel segment: an edge of the tree, ordered proximal -> distal.

    Geometry is in mm, straight off the centerline points. ``label``/``name`` are
    the artery this segment belongs to, decided by majority vote over the interior
    points: the two endpoint points sit on shared junctions and carry the *parent*
    vessel's label, which would otherwise contaminate short segments.
    """

    index: int
    point_indices: np.ndarray
    points: np.ndarray  # (n, 3) LPS mm
    start_node: int
    end_node: int
    label: int
    name: str
    parent: int | None = None
    children: tuple[int, ...] = ()
    generation: int = 0  # 0 for the segments leaving an ostium
    radii: np.ndarray | None = None  # (n,) mm, when the centerline carries a radius

    @property
    def length(self) -> float:
        """Arc length along the centerline, mm."""
        return float(np.linalg.norm(np.diff(self.points, axis=0), axis=1).sum())

    @property
    def chord(self) -> float:
        """Straight-line distance between the segment's two nodes, mm."""
        return float(np.linalg.norm(self.points[-1] - self.points[0]))

    @property
    def tortuosity(self) -> float:
        """Distance factor: arc length / chord. 1.0 for a straight segment."""
        chord = self.chord
        return float(self.length / chord) if chord > 0 else 1.0

    @property
    def is_terminal(self) -> bool:
        return not self.children

    @property
    def is_named(self) -> bool:
        """False for the catch-all label, which is not a specific artery."""
        return self.name != UNLABELLED



def shaft_window(points: np.ndarray, core_radius_mm: float,
                 window_mm: float) -> tuple[int, int, str | None]:
    """The index range of ``points`` beyond the bifurcation core and within ``window_mm`` of arc
    past it. ``points[lo:hi]`` is the window used for both direction and caliber, so the two are
    always read off the same stretch of vessel. ``(0, 0, reason)`` when it cannot be placed.

    Points closer than ``core_radius_mm`` to the first point (the junction) are skipped: inside
    the core the skeletons of parent and daughters merge, and a direction taken from the junction
    point itself depends strongly on how far out it is read (the LM angle's cohort median moved
    from 99 to 81 degrees between 1.5 and 5 mm secants). This follows the idea of measuring
    bifurcation vectors outside the maximal inscribed sphere at the junction (VMTK).
    """
    outside = np.linalg.norm(points - points[0], axis=1) >= core_radius_mm
    if not outside.any():
        return 0, 0, "vessel ends inside the bifurcation core"
    lo = int(np.argmax(outside))
    tail = points[lo:]
    arc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(tail, axis=0), axis=1))])
    n = int(np.searchsorted(arc, window_mm, side="right"))
    if n < 3:
        return 0, 0, f"fewer than 3 points in the {window_mm:g} mm past the core"
    return lo, lo + n, None


def outgoing_direction(points: np.ndarray, core_radius_mm: float,
                       window_mm: float = 3.0) -> tuple[np.ndarray, str | None]:
    """Unit direction a vessel leaves its first point with, measured past the bifurcation core.
    Returns ``(vector, None)``, or ``(zeros, reason)`` when it cannot be measured.

    A line is fitted (principal axis) to ``shaft_window`` and oriented away from the junction.
    Pass the points of the whole vessel onward (``Vessel.points_from``/``Vessel.shaft``), not one
    segment: the first segment after a split is often cut by a side branch within a few mm.
    """
    lo, hi, reason = shaft_window(points, core_radius_mm, window_mm)
    if reason:
        return np.zeros(3), reason
    window = points[lo:hi]
    centre = window.mean(axis=0)
    axis = np.linalg.svd(window - centre, full_matrices=False)[2][0]
    if np.dot(axis, centre - points[0]) < 0:
        axis = -axis
    return axis / np.linalg.norm(axis), None


@dataclass
class Vessel:
    """One artery: the chain of same-named segments from where that name first appears.

    A named artery is usually several segments -- the LAD is cut wherever a side branch leaves
    it. Where a segment continues into two or more children of its own name (the label scheme has
    no name for an artery's own sub-branches; 456 such junctions in the cohort), the child with
    the longest downstream run of that name continues the vessel and the others start vessels of
    their own with ``is_main=False``. That tie-break is a choice, not anatomy.
    """

    index: int
    name: str
    segments: tuple[Segment, ...]  # proximal -> distal
    parent: int | None  # index of the vessel feeding this one's origin; None at an ostium
    is_main: bool

    @property
    def first(self) -> Segment:
        return self.segments[0]

    @property
    def origin_node(self) -> int:
        return self.segments[0].start_node

    @property
    def length(self) -> float:
        return float(sum(s.length for s in self.segments))

    @property
    def points(self) -> np.ndarray:
        """All points proximal -> distal, each shared junction point once."""
        return self.points_from(self.segments[0])

    def points_from(self, segment: Segment) -> np.ndarray:
        """Points from the start of ``segment`` (one of this vessel's) to the vessel's end."""
        k = next(i for i, s in enumerate(self.segments) if s.index == segment.index)
        rest = self.segments[k:]
        return np.concatenate([rest[0].points] + [s.points[1:] for s in rest[1:]])

    def shaft(self, segment: Segment, upstream: bool = False) -> tuple[np.ndarray, np.ndarray | None]:
        """Points and radii from ``segment`` (one of this vessel's) onward to the vessel's end
        (``upstream=False``, i.e. ``points_from`` plus the matching radii), or backward to the
        vessel's start (``upstream=True``).

        ``upstream=True`` starts at ``segment``'s distal (end) node and walks toward the vessel's
        own origin: the direction and caliber a vessel arrives at its own downstream junction
        with, before that junction. Radii are ``None`` if any segment needed lacks them.
        """
        k = next(i for i, s in enumerate(self.segments) if s.index == segment.index)
        chain = self.segments[: k + 1][::-1] if upstream else self.segments[k:]
        flip = (lambda a: a[::-1]) if upstream else (lambda a: a)
        points = np.concatenate([flip(chain[0].points)] + [flip(s.points)[1:] for s in chain[1:]])
        if any(s.radii is None for s in chain):
            return points, None
        radii = np.concatenate([flip(chain[0].radii)] + [flip(s.radii)[1:] for s in chain[1:]])
        return points, radii


def _build_vessels(segments: list[Segment]) -> tuple[Vessel, ...]:
    # Segments are created in BFS order, so a child always has a higher index than its parent.
    run = [0.0] * len(segments)
    for s in reversed(segments):
        same = [run[c] for c in s.children if segments[c].name == s.name]
        run[s.index] = s.length + max(same, default=0.0)
    continues = {}
    for s in segments:
        same = [c for c in s.children if segments[c].name == s.name]
        if same:
            continues[s.index] = max(same, key=lambda c: (run[c], -c))

    vessels: list[Vessel] = []
    owner: dict[int, int] = {}
    for s in segments:
        p = s.parent
        if p is not None and continues.get(p) == s.index:
            continue
        chain = [s]
        while chain[-1].index in continues:
            chain.append(segments[continues[chain[-1].index]])
        v = Vessel(index=len(vessels), name=s.name, segments=tuple(chain),
                   parent=None if p is None else owner[p],
                   is_main=p is None or segments[p].name != s.name)
        owner.update((c.index, v.index) for c in chain)
        vessels.append(v)
    return tuple(vessels)


@dataclass
class CoronaryTree:
    """One side's rooted tree. Normally a single tree; a forest when anatomy says so."""

    case_id: int
    side: str
    points: np.ndarray
    nodes: dict[int, Node]
    segments: list[Segment]
    roots: tuple[int, ...]
    chords: tuple[np.ndarray, ...] = ()  # cycle-closing chains, excluded from the tree
    warnings: tuple[str, ...] = ()
    vessels: tuple[Vessel, ...] = ()

    def main_vessels(self, name: str) -> list[Vessel]:
        """Vessels of this name that start where the name first appears (not sub-branches)."""
        return [v for v in self.vessels if v.name == name and v.is_main]

    def vessel_of(self, segment: Segment) -> Vessel:
        return next(v for v in self.vessels if any(s.index == segment.index for s in v.segments))

    @property
    def is_single_tree(self) -> bool:
        return len(self.roots) == 1 and not self.chords

    @property
    def total_length(self) -> float:
        return float(sum(s.length for s in self.segments))

    def root_segments(self) -> list[Segment]:
        return [s for s in self.segments if s.parent is None]

    def children_of(self, segment: Segment) -> list[Segment]:
        return [self.segments[i] for i in segment.children]

    def by_name(self) -> dict[str, list[Segment]]:
        out: dict[str, list[Segment]] = defaultdict(list)
        for s in self.segments:
            out[s.name].append(s)
        return dict(out)

    def bifurcations(self) -> list[Node]:
        """Nodes where the tree actually splits -- always 2+ children."""
        return [n for n in self.nodes.values() if n.kind == BIFURCATION]

    def termini(self) -> list[Node]:
        return [n for n in self.nodes.values() if n.kind == TERMINUS]

    def walk(self, segment: Segment | None = None):
        """Pre-order traversal, proximal to distal. Deterministic."""
        stack = list(reversed(self.root_segments() if segment is None else [segment]))
        while stack:
            s = stack.pop()
            yield s
            stack.extend(reversed(self.children_of(s)))


def _merge_chains(
    lines: list[np.ndarray], junctions: set[int]
) -> tuple[list[np.ndarray], list[int]]:
    """Glue polylines together through degree-2 pass-through points.

    Returns the maximal chains between junctions, plus the indices of any polylines
    that touch no junction at all (a free-floating loop -- none occur in this
    dataset, but a silent drop would be worse than a reported one).
    """
    ends = defaultdict(list)
    for k, line in enumerate(lines):
        ends[int(line[0])].append(k)
        ends[int(line[-1])].append(k)

    used: set[int] = set()
    chains: list[np.ndarray] = []
    for k0, line in enumerate(lines):
        if k0 in used or not junctions & {int(line[0]), int(line[-1])}:
            continue
        used.add(k0)
        chain = list(line)
        if int(chain[0]) not in junctions:
            chain.reverse()
        while int(chain[-1]) not in junctions:
            nxt = [k for k in ends[int(chain[-1])] if k not in used]
            if not nxt:
                break
            k = min(nxt)
            used.add(k)
            piece = list(lines[k])
            if int(piece[0]) != int(chain[-1]):
                piece.reverse()
            chain.extend(piece[1:])
        chains.append(np.asarray(chain, dtype=int))
    return chains, [k for k in range(len(lines)) if k not in used]


def _components(chains: list[np.ndarray], node_ids: list[int]) -> list[list[int]]:
    parent = {n: n for n in node_ids}

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for ch in chains:
        a, b = find(int(ch[0])), find(int(ch[-1]))
        if a != b:
            parent[a] = b

    groups: dict[int, list[int]] = defaultdict(list)
    for n in node_ids:
        groups[find(n)].append(n)
    return [sorted(g) for g in groups.values()]


def _majority_label(labels: np.ndarray) -> int:
    """Most common label over the interior points; ties go to the smallest label.

    The endpoints are shared junction points carrying the parent vessel's label, so
    they are excluded whenever there is anything left to vote with.
    """
    interior = labels[1:-1] if len(labels) > 2 else labels
    return int(np.argmax(np.bincount(np.asarray(interior, dtype=int))))


def build_tree(centerline: io.Centerline) -> CoronaryTree:
    """Build the rooted tree for one side. Never raises on the odd sides -- it
    records what it had to do in ``warnings`` so the cohort run can report them."""
    pts = centerline.points
    n_points = len(pts)

    degree = np.zeros(n_points, dtype=int)
    for line in centerline.lines:
        degree[int(line[0])] += 1
        degree[int(line[-1])] += 1

    starts = [int(i) for i in np.flatnonzero(centerline.start_points)]
    # Degree != 2 is a real junction; ostia are pinned so one can never be merged over.
    junctions = {int(i) for i in np.flatnonzero(degree != 0) if degree[i] != 2} | set(starts)
    chains, loose = _merge_chains(centerline.lines, junctions)

    warnings: list[str] = []
    if loose:
        warnings.append(f"{len(loose)} polyline(s) form a closed loop touching no junction; dropped")

    node_ids = sorted({int(c[0]) for c in chains} | {int(c[-1]) for c in chains})
    adjacency: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for k, ch in enumerate(chains):
        adjacency[int(ch[0])].append((k, int(ch[-1])))
        adjacency[int(ch[-1])].append((k, int(ch[0])))

    # --- choose a root per component -------------------------------------------------
    comps = _components(chains, node_ids)
    comps.sort(key=lambda c: (not set(c) & set(starts), -len(c), c[0]))
    roots: list[int] = []
    rooted_pts: list[np.ndarray] = []
    for comp in comps:
        own = sorted(set(comp) & set(starts))
        if own:
            root = own[0]
            if len(own) > 1:
                warnings.append(f"component at node {root} has {len(own)} start points")
        else:
            # A detached fragment. Its proximal end is the one nearest the rest of
            # the tree, which is the best stand-in for an ostium we can justify.
            candidates = [n for n in comp if degree[n] == 1] or comp
            if rooted_pts:
                ref = np.asarray(rooted_pts)
                root = min(candidates, key=lambda n: float(np.min(np.linalg.norm(ref - pts[n], axis=1))))
            else:
                root = candidates[0]
            warnings.append(f"component of {len(comp)} nodes has no ostium; rooted at node {root}")
        roots.append(root)
        rooted_pts.extend(pts[n] for n in comp)

    # --- orient every chain away from its root ---------------------------------------
    segments: list[Segment] = []
    chord_chains: list[np.ndarray] = []
    used: set[int] = set()
    seen: set[int] = set(roots)
    for root in roots:
        queue = deque([(root, None)])
        while queue:
            node, parent_seg = queue.popleft()
            for k, other in sorted(adjacency[node]):
                if k in used:
                    continue
                used.add(k)
                if other in seen:  # closes a cycle: a coronary tree has none
                    chord_chains.append(chains[k])
                    continue
                seen.add(other)
                idx = chains[k] if int(chains[k][0]) == node else chains[k][::-1]
                label = _majority_label(centerline.segment_label[idx])
                seg = Segment(
                    index=len(segments),
                    point_indices=idx,
                    points=pts[idx],
                    start_node=node,
                    end_node=other,
                    label=label,
                    name=artery_name(label),
                    parent=parent_seg,
                    generation=0 if parent_seg is None else segments[parent_seg].generation + 1,
                    radii=None if centerline.radius is None else centerline.radius[idx],
                )
                segments.append(seg)
                queue.append((other, seg.index))
    if chord_chains:
        warnings.append(f"{len(chord_chains)} cycle-closing edge(s) dropped to make a tree")

    for seg in segments:
        if seg.parent is not None:
            p = segments[seg.parent]
            p.children = (*p.children, seg.index)

    # Kind comes from the tree that was actually built: a node whose extra edge was
    # dropped as a chord is no longer a branch point, whatever its raw degree says.
    n_children: dict[int, int] = defaultdict(int)
    for seg in segments:
        n_children[seg.start_node] += 1
    root_set = set(roots)

    def kind_of(n: int) -> str:
        if n in root_set:
            return OSTIUM
        return {0: TERMINUS, 1: PASSTHROUGH}.get(n_children[n], BIFURCATION)

    nodes = {
        n: Node(index=n, position=pts[n], degree=int(degree[n]), kind=kind_of(n))
        for n in node_ids
    }
    return CoronaryTree(
        case_id=centerline.case_id,
        side=centerline.side,
        points=pts,
        nodes=nodes,
        segments=segments,
        roots=tuple(roots),
        chords=tuple(chord_chains),
        warnings=tuple(warnings),
        vessels=_build_vessels(segments),
    )


def load_tree(case_id: int, side: str, root=None) -> CoronaryTree:
    """``root=None`` is the delivered GT; otherwise a directory of centerlines in its naming."""
    return build_tree(io.load_centerline(case_id, side, root))


def load_trees(case_id: int, root=None) -> dict[str, CoronaryTree]:
    """Both sides. They are separate trees -- the coronary circulation has two ostia."""
    return {side: load_tree(case_id, side, root) for side in ("left", "right")}
