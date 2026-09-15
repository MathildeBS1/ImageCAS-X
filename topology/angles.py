"""Bifurcation angle: the first topological feature (objective 7).

The angle between two daughter branches' outgoing directions at a bifurcation, each measured
past the bifurcation core with ``Segment.outgoing_direction`` (so it needs the per-point radius
from ``topology.radius``). Built on ``graph.Vessel``: a named bifurcation is where one vessel
leaves another, so no search over nodes is needed.

Five named bifurcations, fixed by anatomical name so a value means the same place in every case:

    LM        LAD vs LCx, the daughters of the left main. An intermediate artery (IM), if present,
              is recorded (``im_present``) but not part of the angle.
    LAD-D1    D1 vs the LAD continuing past its origin
    LAD-D2    D2 vs the LAD continuing past its origin
    LCX-OM1   OM1 vs the LCx continuing past its origin
    CRUX      PDA vs PLA: R-PDA/R-PLA on the right tree, else L-PDA/L-PLA on the left (right
              preferred if both); cross-checked against the Dominance descriptor.

Missing ones come back as NaN with a ``reason``, never silently dropped.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from . import graph, paths

BIFURCATION_NAMES = ("LM", "LAD-D1", "LAD-D2", "LCX-OM1", "CRUX")
TAKEOFFS = {"LAD-D1": ("D1", "LAD"), "LAD-D2": ("D2", "LAD"), "LCX-OM1": ("OM1", "LCX")}


@dataclass
class BifurcationResult:
    """One bifurcation's angle for one case, or the reason it could not be measured."""

    name: str
    angle_deg: float  # NaN when not measurable
    side: str | None = None
    position: np.ndarray | None = None  # (3,) LPS mm, for plotting; None if not measured
    reason: str | None = None  # set exactly when angle_deg is NaN
    origin_gap_mm: float | None = None  # distance between the two daughters' start nodes
    segments: tuple[int, int] | None = None  # the two segment indices the angle was measured on
    extra: dict = field(default_factory=dict)


def _missing(name: str, side: str | None, reason: str, **extra) -> BifurcationResult:
    return BifurcationResult(name, float("nan"), side=side, reason=reason, extra=extra)


def _children_at(tree: graph.CoronaryTree, node: int) -> list[graph.Segment]:
    return [s for s in tree.segments if s.start_node == node]


def direction(tree: graph.CoronaryTree, seg: graph.Segment, core_scale: float, window_mm: float):
    """``graph.outgoing_direction`` along ``seg``'s vessel from ``seg`` onward, skipping a core of
    ``core_scale`` x the radius at ``seg``'s start node."""
    if seg.radii is None:
        raise ValueError("centerline has no radius: run scripts/compute_centerline_radius.py "
                         "(GT) or build it with topology.skeleton (prediction)")
    points = tree.vessel_of(seg).points_from(seg)
    return graph.outgoing_direction(points, core_scale * float(seg.radii[0]), window_mm)


def _measure(name: str, tree: graph.CoronaryTree, seg_a: graph.Segment, seg_b: graph.Segment,
             core_scale: float, window_mm: float, **extra) -> BifurcationResult:
    va, ra = direction(tree, seg_a, core_scale, window_mm)
    vb, rb = direction(tree, seg_b, core_scale, window_mm)
    pa, pb = tree.nodes[seg_a.start_node].position, tree.nodes[seg_b.start_node].position
    common = dict(side=tree.side, origin_gap_mm=float(np.linalg.norm(pa - pb)),
                  segments=(seg_a.index, seg_b.index), extra=extra)
    if ra or rb:
        reason = "; ".join(f"{s.name}: {r}" for s, r in ((seg_a, ra), (seg_b, rb)) if r)
        return BifurcationResult(name, float("nan"), reason=reason, **common)
    angle = float(np.degrees(np.arccos(np.clip(np.dot(va, vb), -1.0, 1.0))))
    return BifurcationResult(name, angle, position=(pa + pb) / 2, **common)


def daughter_pair(tree: graph.CoronaryTree, name_a: str, name_b: str):
    """The first segments of the ``name_a`` and ``name_b`` daughters of one split, or a reason.

    1. Main vessels of the two names that start at the same node: the shallowest such pair.
    2. Else a segment of one name that sits beside the other vessel's origin. This is the case
       where a vessel kept its name through a split that also produced the other daughter.
    3. Else the unique main vessel of each name, at different origins. A three-way split stored
       as two junctions a fraction of a mm apart; ``origin_gap_mm`` records how far.
    """
    va, vb = tree.main_vessels(name_a), tree.main_vessels(name_b)
    if not va or not vb:
        return f"no {name_a if not va else name_b} in the tree"

    shared = [(a.first, b.first) for a in va for b in vb if a.origin_node == b.origin_node]
    if not shared:
        found = {(s.index, b.first.index): (s, b.first)
                 for b in vb for s in _children_at(tree, b.origin_node) if s.name == name_a}
        found.update({(a.first.index, s.index): (a.first, s)
                      for a in va for s in _children_at(tree, a.origin_node) if s.name == name_b})
        shared = list(found.values())
    if shared:
        gen = min(a.generation for a, _ in shared)
        best = [p for p in shared if p[0].generation == gen]
        if len(best) > 1:
            return f"{len(best)} {name_a}/{name_b} pairs at generation {gen}"
        return best[0]
    if len(va) == 1 and len(vb) == 1:
        # Only a split if both hang off the same tree: a fragment rooted by graph.py's fallback
        # has no ancestor in common with the rest (case 84's LAD sat 22 mm from the LCx).
        if not _ancestors(tree, va[0]) & _ancestors(tree, vb[0]):
            return f"{name_a} and {name_b} are in disconnected parts of the tree"
        return va[0].first, vb[0].first
    return f"{len(va)} {name_a} and {len(vb)} {name_b} vessels with no shared origin"


def _ancestors(tree: graph.CoronaryTree, vessel: graph.Vessel) -> set[int]:
    out, p = set(), vessel.parent
    while p is not None:
        out.add(p)
        p = tree.vessels[p].parent
    return out


def takeoff_pair(tree: graph.CoronaryTree, branch: str, trunk: str):
    """``branch``'s first segment and the ``trunk`` vessel continuing past its origin, or a
    reason. If the trunk ends there, the one other daughter is used and noted."""
    cands = [v for v in tree.main_vessels(branch)
             if v.parent is not None and tree.vessels[v.parent].name == trunk]
    if not cands:
        return f"no {branch} arising from the {trunk}", None
    note = None
    if len(cands) > 1:
        if len({v.origin_node for v in cands}) > 1:
            return f"{len(cands)} {branch} vessels arising from the {trunk}", None
        # The branch splits right at its own origin: keep the longer half, as graph.Vessel does.
        cands.sort(key=lambda v: -v.length)
        note = f"{len(cands)} {branch} branches share one origin; longest used"
    v = cands[0]
    parent_segs = {s.index for s in tree.vessels[v.parent].segments}
    others = [s for s in _children_at(tree, v.origin_node) if s.index != v.first.index]
    cont = [s for s in others if s.index in parent_segs]
    if cont:
        return (v.first, cont[0]), note
    if len(others) == 1:
        return (v.first, others[0]), f"{trunk} ends here; used {others[0].name!r}"
    return f"ambiguous siblings at the {branch} origin: {sorted(s.name for s in others)}", None


def _lm(tree: graph.CoronaryTree, core_scale: float, window_mm: float) -> BifurcationResult:
    lm = [v.index for v in tree.vessels if v.name == "LM"]
    if not lm:
        return _missing("LM", "left", "no LM bifurcation (absent left main)")
    im_present = any(v.name == "IM" and v.parent in lm for v in tree.vessels)
    pair = daughter_pair(tree, "LAD", "LCX")
    if isinstance(pair, str):
        return _missing("LM", "left", pair, im_present=im_present)
    return _measure("LM", tree, *pair, core_scale, window_mm, im_present=im_present)


def _takeoff(tree, name, core_scale, window_mm) -> BifurcationResult:
    branch, trunk = TAKEOFFS[name]
    pair, note = takeoff_pair(tree, branch, trunk)
    if isinstance(pair, str):
        return _missing(name, tree.side, pair)
    result = _measure(name, tree, *pair, core_scale, window_mm)
    if note:
        result.extra["note"] = note
    return result


def _crux(left, right, dominance, core_scale, window_mm) -> BifurcationResult:
    pairs = {"right": daughter_pair(right, "R-PDA", "R-PLA"),
             "left": daughter_pair(left, "L-PDA", "L-PLA")}
    found = [s for s in ("right", "left") if not isinstance(pairs[s], str)]
    if not found:
        return _missing("CRUX", None, f"right: {pairs['right']}; left: {pairs['left']}",
                        dominance_descriptor=dominance)
    side = found[0]
    extra = {"dominance_descriptor": dominance}
    if len(found) == 2:
        extra["note"] = "both right and left crux present; right used"
    if {"R": "right", "L": "left"}.get(dominance, side) != side:
        extra["dominance_mismatch"] = True
    tree = right if side == "right" else left
    return _measure("CRUX", tree, *pairs[side], core_scale, window_mm, **extra)


def extract_case(case_id: int, root=None, core_scale: float = 1.0,
                 window_mm: float = 3.0) -> dict[str, BifurcationResult]:
    """All five angles for one case, keyed by ``BIFURCATION_NAMES``.

    ``root`` selects predicted centerlines (see ``graph.load_trees``); ``core_scale`` multiplies
    the radius at the junction to give the core that is skipped; ``window_mm`` is the length
    the direction line is fitted over.
    """
    trees = graph.load_trees(case_id, root)
    desc = paths.descriptors()
    dominance = desc.loc[case_id, "Dominance"] if case_id in desc.index else None
    return extract_trees(trees["left"], trees["right"],
                         dominance if isinstance(dominance, str) else None, core_scale, window_mm)


def extract_trees(left: graph.CoronaryTree, right: graph.CoronaryTree, dominance: str | None,
                  core_scale: float = 1.0, window_mm: float = 3.0) -> dict[str, BifurcationResult]:
    """``extract_case`` on trees already loaded, e.g. to measure one case several ways."""
    out = {"LM": _lm(left, core_scale, window_mm)}
    for name in TAKEOFFS:
        out[name] = _takeoff(left, name, core_scale, window_mm)
    out["CRUX"] = _crux(left, right, dominance, core_scale, window_mm)
    return out
