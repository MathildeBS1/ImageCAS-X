"""Bifurcation geometry, conditioned on caliber: the first topological feature (objective 7).

Every splitting node gets a row (``all_bifurcations``): the daughter-daughter angle, exactly as
before, plus what that angle omits. Two same-angle bifurcations can split their flow very
differently depending on how the calibers compare -- a thick trunk sending off a much thinner
side branch deflects little itself while the side branch bends hard, whereas a genuinely
symmetric split shares the bend evenly between both daughters. So the daughter-daughter angle
alone is close to blind to exactly the caliber asymmetry it is often read as reflecting; the two
parent-relative deflections (``theta_main_deg``, ``theta_side_deg``) are where that signal
actually is. ``radius_ratio``/``area_ratio``/``finet_ratio`` give that caliber context alongside
the angles.

Each branch's direction and caliber are read off the same stretch of vessel
(``graph.outgoing_direction`` / ``graph.shaft_window``, via ``Vessel.shaft``), past a junction
core scaled by the local radius, needing the per-point radius from ``topology.radius``.

Five named bifurcations, fixed by anatomical name so a value means the same place in every case,
are flagged among the enumerated rows rather than replacing them:

    LM        LAD vs LCx, the daughters of the left main. An intermediate artery (IM), if present,
              is recorded (``im_present``) but not part of the angle.
    LAD-D1    D1 vs the LAD continuing past its origin
    LAD-D2    D2 vs the LAD continuing past its origin
    LCX-OM1   OM1 vs the LCx continuing past its origin
    CRUX      PDA vs PLA: R-PDA/R-PLA on the right tree, else L-PDA/L-PLA on the left (right
              preferred if both); cross-checked against the Dominance descriptor.

Missing ones come back as a row with NaNs and a ``reason``, never silently dropped.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field

import numpy as np

from . import graph, paths

BIFURCATION_NAMES = ("LM", "LAD-D1", "LAD-D2", "LCX-OM1", "CRUX")
TAKEOFFS = {"LAD-D1": ("D1", "LAD"), "LAD-D2": ("D2", "LAD"), "LCX-OM1": ("OM1", "LCX")}


@dataclass
class Branch:
    """One limb of a junction, oriented away from it. ``radius_mm`` is the median lumen radius
    over the same shaft window the direction is fitted on, not the (core-scale) junction radius."""

    role: str  # "parent" | "main" | "side"
    name: str | None
    segment: int | None
    direction: np.ndarray | None  # unit, away from the junction; None if not measurable
    radius_mm: float  # NaN if not measurable
    reason: str | None = None


@dataclass
class Bifurcation:
    """One splitting node's geometry for one case, or the reason it could not be measured.

    ``main``/``side_br`` are the two daughters, ordered by caliber (``main`` the thicker) so that
    ``radius_ratio`` <= 1 always; ``angle_deg`` is unordered and unchanged from the original
    definition.
    """

    side: str | None
    node: int | None
    position: np.ndarray | None
    parent: Branch | None
    main: Branch | None
    side_br: Branch | None
    named: str | None = None  # one of BIFURCATION_NAMES, or None for an unnamed enumerated row
    angle_deg: float = float("nan")  # daughter-daughter, the original definition
    theta_main_deg: float = float("nan")  # main daughter's deflection from the parent's axis
    theta_side_deg: float = float("nan")  # side daughter's deflection from the parent's axis
    out_of_plane_deg: float = float("nan")  # how far the parent axis sits from the daughters' plane
    radius_ratio: float = float("nan")  # r_side / r_main, <= 1
    area_ratio: float = float("nan")  # (r_main^2 + r_side^2) / r_parent^2, 1.0 = area-preserving
    finet_ratio: float = float("nan")  # r_parent / (r_main + r_side)
    generation: int | None = None
    dist_from_ostium_mm: float = float("nan")
    n_daughters: int = 2  # > 2 at a trifurcation; this row is one of its C(n, 2) pairs
    origin_gap_mm: float | None = None  # distance between the two daughters' start nodes
    reason: str | None = None
    extra: dict = field(default_factory=dict)


def _missing(name: str, side: str | None, reason: str, **extra) -> Bifurcation:
    return Bifurcation(side=side, node=None, position=None, parent=None, main=None, side_br=None,
                       named=name, reason=reason, extra=extra)


def _children_at(tree: graph.CoronaryTree, node: int) -> list[graph.Segment]:
    return [s for s in tree.segments if s.start_node == node]


def _branch(tree: graph.CoronaryTree, seg: graph.Segment, core_scale: float, window_mm: float,
           upstream: bool = False, role: str = "") -> Branch:
    """One limb of a junction: direction and caliber, read off the same shaft window.

    ``upstream=True`` reads ``seg`` backward from its distal (junction) end -- the direction and
    radius the parent has just before the junction, rather than a daughter's own outgoing shaft.
    """
    if seg.radii is None:
        raise ValueError("centerline has no radius: run scripts/compute_centerline_radius.py first")
    points, radii = tree.vessel_of(seg).shaft(seg, upstream=upstream)
    core = core_scale * float(radii[0])
    direction, reason = graph.outgoing_direction(points, core, window_mm)
    if reason:
        return Branch(role, seg.name, seg.index, None, float("nan"), reason)
    lo, hi, _ = graph.shaft_window(points, core, window_mm)
    return Branch(role, seg.name, seg.index, direction, float(np.median(radii[lo:hi])))


def direction(tree: graph.CoronaryTree, seg: graph.Segment, core_scale: float, window_mm: float):
    """``graph.outgoing_direction`` along ``seg``'s vessel, for callers that only need the unit
    vector (``scripts/angle_sensitivity.py``). See ``_branch`` for direction and caliber together."""
    b = _branch(tree, seg, core_scale, window_mm)
    return (np.zeros(3) if b.direction is None else b.direction), b.reason


def _anchor(tree: graph.CoronaryTree, seg_a: graph.Segment,
           seg_b: graph.Segment) -> tuple[int, graph.Segment | None]:
    """The node this pair is measured at, and the segment feeding it: the shared start node when
    the daughters agree, else the more proximal daughter's own origin (the two-junction-split
    fallback -- see ``daughter_pair``'s case 3, where the two do not literally share a node)."""
    anchor = seg_a if seg_a.start_node == seg_b.start_node else \
        min((seg_a, seg_b), key=lambda s: (s.generation, s.index))
    return anchor.start_node, None if anchor.parent is None else tree.segments[anchor.parent]


def _dist_from_ostium(tree: graph.CoronaryTree, parent_seg: graph.Segment) -> float:
    d, s = parent_seg.length, parent_seg
    while s.parent is not None:
        s = tree.segments[s.parent]
        d += s.length
    return float(d)


def _measure(tree: graph.CoronaryTree, seg_a: graph.Segment, seg_b: graph.Segment,
            core_scale: float, window_mm: float, n_daughters: int = 2) -> Bifurcation:
    node, parent_seg = _anchor(tree, seg_a, seg_b)
    ba, bb = _branch(tree, seg_a, core_scale, window_mm), _branch(tree, seg_b, core_scale, window_mm)
    ra = ba.radius_mm if np.isfinite(ba.radius_mm) else -1.0
    rb = bb.radius_mm if np.isfinite(bb.radius_mm) else -1.0
    main, side_br = (ba, bb) if ra >= rb else (bb, ba)
    main.role, side_br.role = "main", "side"

    pa, pb = tree.nodes[seg_a.start_node].position, tree.nodes[seg_b.start_node].position
    common = dict(side=tree.side, node=node, position=tree.nodes[node].position,
                  origin_gap_mm=float(np.linalg.norm(pa - pb)), n_daughters=n_daughters,
                  generation=seg_a.generation)

    if main.reason or side_br.reason:
        reason = "; ".join(f"{b.name}: {b.reason}" for b in (main, side_br) if b.reason)
        return Bifurcation(parent=None, main=main, side_br=side_br, reason=reason, **common)

    angle = float(np.degrees(np.arccos(np.clip(np.dot(main.direction, side_br.direction), -1.0, 1.0))))
    if parent_seg is None:
        parent = Branch("parent", None, None, None, float("nan"), "no parent: this is the ostium")
        return Bifurcation(parent=parent, main=main, side_br=side_br, angle_deg=angle,
                           dist_from_ostium_mm=0.0, **common)

    parent = _branch(tree, parent_seg, core_scale, window_mm, upstream=True, role="parent")
    out = Bifurcation(parent=parent, main=main, side_br=side_br, angle_deg=angle,
                      dist_from_ostium_mm=_dist_from_ostium(tree, parent_seg), **common)
    if parent.reason:
        out.reason = f"parent: {parent.reason}"
        return out

    f = -parent.direction
    out.theta_main_deg = float(np.degrees(np.arccos(np.clip(np.dot(main.direction, f), -1.0, 1.0))))
    out.theta_side_deg = float(np.degrees(np.arccos(np.clip(np.dot(side_br.direction, f), -1.0, 1.0))))
    normal = np.cross(main.direction, side_br.direction)
    norm = np.linalg.norm(normal)
    out.out_of_plane_deg = 0.0 if norm < 1e-9 else \
        float(np.degrees(np.arcsin(np.clip(abs(np.dot(f, normal / norm)), 0.0, 1.0))))

    r0, r1, r2 = parent.radius_mm, main.radius_mm, side_br.radius_mm
    if r0 > 0 and r1 > 0 and r2 > 0:
        out.radius_ratio = r2 / r1
        out.area_ratio = (r1**2 + r2**2) / r0**2
        out.finet_ratio = r0 / (r1 + r2)
        if r1 >= r0:  # the "main" daughter is not thinner than its parent -- a caliber anomaly
            out.extra["caliber_anomaly"] = True
    return out


def all_bifurcations(tree: graph.CoronaryTree, core_scale: float, window_mm: float) -> list[Bifurcation]:
    """Every splitting node in ``tree``, one row per unordered pair of daughters. A trifurcation
    (or higher) contributes one row per pair, each carrying the true ``n_daughters``."""
    out = []
    for node in tree.bifurcations():
        children = _children_at(tree, node.index)
        for seg_a, seg_b in itertools.combinations(children, 2):
            out.append(_measure(tree, seg_a, seg_b, core_scale, window_mm, n_daughters=len(children)))
    return out


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


def _lm(tree: graph.CoronaryTree, core_scale: float, window_mm: float) -> Bifurcation:
    lm = [v.index for v in tree.vessels if v.name == "LM"]
    if not lm:
        return _missing("LM", "left", "no LM bifurcation (absent left main)")
    im_present = any(v.name == "IM" and v.parent in lm for v in tree.vessels)
    pair = daughter_pair(tree, "LAD", "LCX")
    if isinstance(pair, str):
        return _missing("LM", "left", pair, im_present=im_present)
    result = _measure(tree, *pair, core_scale, window_mm)
    result.named = "LM"
    result.extra["im_present"] = im_present
    return result


def _takeoff(tree, name, core_scale, window_mm) -> Bifurcation:
    branch, trunk = TAKEOFFS[name]
    pair, note = takeoff_pair(tree, branch, trunk)
    if isinstance(pair, str):
        return _missing(name, tree.side, pair)
    result = _measure(tree, *pair, core_scale, window_mm)
    result.named = name
    if note:
        result.extra["note"] = note
    return result


def _crux(left, right, dominance, core_scale, window_mm) -> Bifurcation:
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
    result = _measure(tree, *pairs[side], core_scale, window_mm)
    result.named = "CRUX"
    result.extra.update(extra)
    return result


def extract_case(case_id: int, root=None, core_scale: float = 1.0,
                 window_mm: float = 3.0) -> list[Bifurcation]:
    """Every bifurcation for one case, the five named ones flagged via ``.named``.

    ``root`` selects predicted centerlines (see ``graph.load_trees``); ``core_scale`` multiplies
    the radius at the junction to give the core that is skipped; ``window_mm`` is the length
    the direction and caliber are read over.
    """
    trees = graph.load_trees(case_id, root)
    desc = paths.descriptors()
    dominance = desc.loc[case_id, "Dominance"] if case_id in desc.index else None
    return extract_trees(trees["left"], trees["right"],
                         dominance if isinstance(dominance, str) else None, core_scale, window_mm)


def extract_trees(left: graph.CoronaryTree, right: graph.CoronaryTree, dominance: str | None,
                  core_scale: float = 1.0, window_mm: float = 3.0) -> list[Bifurcation]:
    """``extract_case`` on trees already loaded, e.g. to measure one case several ways.

    Every splitting node in both trees (``all_bifurcations``), plus the five named bifurcations
    matched onto them by ``.named`` -- tagging the same row rather than appending a duplicate,
    except for the two-junction-split fallback (``daughter_pair`` case 3), which has no enumerated
    counterpart and is appended on its own.
    """
    rows = all_bifurcations(left, core_scale, window_mm) + all_bifurcations(right, core_scale, window_mm)
    by_key = {(r.side, r.node, frozenset((r.main.segment, r.side_br.segment))): r
              for r in rows if r.main is not None and r.side_br is not None}

    named = [_lm(left, core_scale, window_mm)]
    for name in TAKEOFFS:
        named.append(_takeoff(left, name, core_scale, window_mm))
    named.append(_crux(left, right, dominance, core_scale, window_mm))

    for result in named:
        if result.main is None or result.side_br is None:
            rows.append(result)  # missing: nothing enumerated to tag
            continue
        key = (result.side, result.node, frozenset((result.main.segment, result.side_br.segment)))
        target = by_key.get(key)
        if target is None:  # the two-junction-split fallback: no enumerated row shares this key
            rows.append(result)
        else:
            target.named = result.named
            target.extra.update(result.extra)
    return rows
