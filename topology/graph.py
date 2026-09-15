"""Rooted vessel trees built from the dataset's centerlines.

This is the structure every topological feature is computed on (objective 6), so
it is built exactly rather than heuristically. The dataset's centerlines make that
possible -- verified over all 1600 sides:

- Centerline points are unique and already in physical mm (LPS). No affine needed.
- The VTK polylines *are* the tree edges: they meet only at shared point indices,
  and a point shared by k polyline ends has graph degree k.
- ``end_points`` is exactly the set of degree-1 nodes and ``branch_points``
  exactly the set of degree >= 3 nodes, in every side. The flags shipped with the
  dataset and the connectivity agree perfectly.
- A few points are shared by exactly two polyline ends. Those are pass-throughs
  mid-vessel, not anatomy, and are merged away here so one ``Segment`` spans
  ostium/bifurcation to bifurcation/terminus.

1584 of 1600 sides are then a single clean rooted tree. The 16 that are not are
real and are handled explicitly rather than dropped (see ``CoronaryTree.warnings``):

- 11 left sides come apart into two components with two ostia. These are exactly
  the 11 left sides with no ``LM`` label -- the absent-left-main variant, where LAD
  and LCX arise from separate ostia. Anatomy, not corruption.
- 2 left sides (84, 272) are fragmented with a single ostium; the orphan fragment
  is rooted at its end nearest the rooted tree and flagged.
- 3 sides (8 left, 455 right, 776 left) contain a cycle. A coronary tree has none,
  so the cycle-closing edge is dropped into ``chords`` and flagged.

``scripts/survey_topology.py`` re-derives all of the above from scratch.
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
    """Canonical label -> artery name, from ``docs_thesis/label_map.json`` (see ``paths.LABEL_MAP``)."""
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

    def direction(self, span_mm: float = 3.0, *, at_end: bool = False) -> np.ndarray:
        """Unit tangent over the first (or last) ``span_mm`` of the segment.

        Bifurcation angles need the direction a vessel *leaves* its junction with,
        not the chord of the whole segment, and a single point step is too noisy at
        this sampling (~0.4 mm). Falls back to the whole segment when it is shorter
        than ``span_mm``.
        """
        pts = self.points[::-1] if at_end else self.points
        step = np.linalg.norm(np.diff(pts, axis=0), axis=1)
        take = int(np.searchsorted(np.cumsum(step), span_mm) + 1)
        vec = pts[min(take, len(pts) - 1)] - pts[0]
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else np.zeros(3)


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
    )


def load_tree(case_id: int, side: str) -> CoronaryTree:
    return build_tree(io.load_centerline(case_id, side))


def load_trees(case_id: int) -> dict[str, CoronaryTree]:
    """Both sides. They are separate trees -- the coronary circulation has two ostia."""
    return {side: load_tree(case_id, side) for side in ("left", "right")}
