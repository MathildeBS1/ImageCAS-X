"""Per-artery selection of usable centerline trunks (LM, LAD, CX, RCA) from the Medis-derived
coronary centerlines Kit uploaded to /data/kimbr/centerlines_hø_10Y.zip (744 cases).

    python CGPS_data/centerline_selection.py                       # uses ZIP_PATH and OUT_DIR below
    python CGPS_data/centerline_selection.py --src /path/to/zip_or_folder --out ~/centerline_selection
    python CGPS_data/centerline_selection.py --limit 20             # quick trial on the first 20 cases

Run it on the secure machine, next to centerline_qc.py (whose reader it imports: same zip handling,
same VTK parser, same label names, same DEDUP_TOL / JOIN_TOL graph). Needs numpy and pandas only.

Each artery is graded on its own, because the models are fitted per artery: a case can give a
strict LAD and an excluded RCA. For every case and artery the script walks the trunk the way
tortuosity/vessels.py does on ImageCAS-X: the geodesic path from the ostium to the farthest point
carrying the most distal trunk label (dLAD, LCx, dRCA), so a same-label side twig never replaces
the trunk. These files have no ostium flag, so the ostium is the LM end point farthest from pLAD /
pCx (left) or the pRCA end point farthest from mRCA (right). Everything is then measured *on that
path*: length per segment, LM length, label order, foreign labels, unlabelled stretches, jumps,
radius (if a radius array exists). Tiers, thresholds at the top of the file:
- strict:     every trunk segment on the path (LAD pLAD+mLAD+dLAD, CX pCx+LCx, RCA pRCA+mRCA+dRCA),
              LM present and the path starting at a free end, labels in proximal->distal order,
              hardly any foreign / unlabelled length on the path, no jump, trunk long enough, and
              no fragment of the trunk's labels elsewhere, no cycle, no left/right mixing.
- acceptable: the proximal and mid segments on the path (distal may be missing or short), LM may
              be absent, looser tolerances, shorter minimum length; fragments/cycles/mixing are
              allowed (they are counted in the report).
- excluded:   anything else; the reasons are listed (several per case possible).
LM gets its own tier (it is the plaque-free gate for LAD / CX, not a model unit).

Outputs in OUT_DIR:
- secure_only/centerline_tiers.csv   one row per case x artery: tier, reasons, all path metrics.
                                     Contains case IDs: it must stay on the secure machine.
- selection_report.md                aggregate counts only (tiers per artery, reasons, overlap of
                                     usable arteries, path-length summaries). No case ID, no
                                     row-level value, counts from 1 to MIN_CELL-1 written as
                                     "<MIN_CELL", a row never keeps a single hidden cell, no min/max,
                                     quartiles only from QUARTILE_MIN values (as in cgps_stats.py).
Counts can still be combined with other tables, so have the report checked against the data
agreement before it leaves the secure environment.
"""

from __future__ import annotations

import argparse
import heapq
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import centerline_qc as qc  # noqa: E402  (reader, label names and graph settings are shared)

# ---- edit these before running (or override with --src / --out) ----
ZIP_PATH = qc.ZIP_PATH                                    # the zip, or a folder with the files
OUT_DIR = str(Path.home() / "centerline_selection")      # results folder (created if missing)
SECURE_SUBDIR = "secure_only"                             # row-level CSV goes here; never copy it out

# disclosure control (same rules as cgps_stats.py)
MIN_CELL = 5
QUARTILE_MIN = 10
GROUP_MIN = 20

# labels: Kit's codes are not SCCT numbers (14 = L-PLB, not OM2), so they are read "raw" and named
# from each file's segment_names. Codes no file names (#18-#22, #28) count as foreign side branches
# until Kit says otherwise; name them here, e.g. {22: "dCX"} would make code 22 part of the CX trunk.
LABEL_NUMBERING = "raw"
CODE_NAMES = {}
BRANCH_ARRAY = "branch"  # point array summarised (not used for grading) - ask Kit what it holds

# case level (same limits as the total_length_odd flag in centerline_qc.py)
CASE_MIN_TOTAL_MM = 50.0
CASE_MAX_TOTAL_MM = 2000.0

# trunk segments and their order from the ostium; equal rank = either name may be used
RANK = {"LAD": {"LM": 0, "pLAD": 1, "mLAD": 2, "dLAD": 3},
        "CX": {"LM": 0, "pCX": 1, "CX": 2, "mCX": 2, "dCX": 3},
        "RCA": {"pRCA": 1, "mRCA": 2, "dRCA": 3}}
LEFT = ("LAD", "CX")
# segments that must lie on the path, each at least MIN_SEG_MM long (a tuple = any of these names)
REQUIRED = {"strict": {"LAD": [("pLAD",), ("mLAD",), ("dLAD",)],
                       "CX": [("pCX",), ("CX", "mCX")],
                       "RCA": [("pRCA",), ("mRCA",), ("dRCA",)]},
            "acceptable": {"LAD": [("pLAD",), ("mLAD",)],
                           "CX": [("pCX",), ("CX", "mCX")],
                           "RCA": [("pRCA",), ("mRCA",)]}}
MIN_SEG_MM = {"strict": 5.0, "acceptable": 3.0}
MIN_TRUNK_MM = {"strict": {"LAD": 70.0, "CX": 40.0, "RCA": 70.0},      # path length after LM
                "acceptable": {"LAD": 40.0, "CX": 30.0, "RCA": 40.0}}  # taper needs >= 20 mm kept
MIN_LM_MM = {"strict": 2.0, "acceptable": 0.5}
MAX_LM_MM = 35.0          # strict: a longer "LM" on the path is more likely a labelling error
FOREIGN_MM = {"strict": 1.0, "acceptable": 3.0}      # other labels on the path (a junction point is 0.5 mm)
UNLAB_RUN_MM = {"strict": 2.0, "acceptable": 5.0}    # longest unlabelled stretch on the path
UNLAB_PCT = {"strict": 5.0, "acceptable": 15.0}      # unlabelled share of the path
MAX_STEP_MM = 1.5         # an edge on the path longer than this is a jump (spacing 0.5, joins <= 1)
FRAGMENT_MM = 5.0         # strict: trunk-labelled length in another component (a broken-off piece)
REQUIRE_RADIUS = False    # True: no radius array = excluded (the QC found none; radius from CT instead)
RADIUS_RANGE = (0.3, 4.0)  # mm; plausible lumen radius on a trunk
RADIUS_VALID_FRAC = 0.9   # share of path points with a finite radius in RADIUS_RANGE
TIERS = ("strict", "acceptable", "excluded")
OTHER_SIDE = {"left": {"RCA"}, "right": {"LM", "LAD", "CX"}}  # qc.TERRITORY names


# ---------------------------------------------------------------- disclosure-safe primitives
SMALL = f"<{MIN_CELL}"
HIDDEN = "hidden"


def small(k):
    return 0 < k < MIN_CELL


def count(n):
    n = int(n)
    return SMALL if small(n) else n


def disclosive(k, n):
    """k out of n reveals too much: the rest (n - k) is small, or all of a small group."""
    return small(n - k) or (k == n and 0 < n < GROUP_MIN)


def count_of(k, n):
    k, n = int(k), int(n)
    return SMALL if small(k) else HIDDEN if disclosive(k, n) else k


def suppress(t):
    """Counts table -> displayed values (copied from cgps_stats.py): small cells become SMALL; while
    a row or column has exactly one hidden cell, its smallest other non-zero cell is hidden too."""
    t = np.asarray(t, dtype=int)
    primary = (t > 0) & (t < MIN_CELL)
    hide = primary.copy()
    lines = [np.s_[i, :] for i in range(t.shape[0])] + [np.s_[:, j] for j in range(t.shape[1])]
    changed = True
    while changed:
        changed = False
        for line in lines:
            h, v = hide[line], t[line]
            others = np.where(~h & (v > 0))[0]
            if h.sum() == 1 and len(others):
                h[others[np.argmin(v[others])]] = True
                changed = True
    out = t.astype(object)
    out[primary] = SMALL
    out[hide & ~primary] = HIDDEN
    return out


def describe(x):
    """Mean/SD from MIN_CELL values, median/quartiles from QUARTILE_MIN. Never min/max."""
    x = pd.Series(x, dtype=float).dropna()
    n = len(x)
    if n < MIN_CELL:
        return {"n": count(n)}
    q = [float(v) for v in x.quantile([0.25, 0.5, 0.75]).round(1)]
    quart = n >= QUARTILE_MIN
    return {"n": n, "mean": round(float(x.mean()), 1), "sd": round(float(x.std()), 1),
            "q1": q[0] if quart else None, "median": q[1] if quart else None, "q3": q[2] if quart else None}


# ---------------------------------------------------------------- reading (centerline_qc reader)
_polys_from_mesh = qc.polys_from_mesh


def _polys_with_branch(points, lines, point_arrays, cell_arrays, source, lookup=None):
    """qc.polys_from_mesh, plus the BRANCH_ARRAY values of each polyline as Poly.branch."""
    polys, meta = _polys_from_mesh(points, lines, point_arrays, cell_arrays, source, lookup)
    kept = [np.asarray(i, int) for i in (lines or [list(range(len(points)))]) if len(i) >= 2]
    b = point_arrays.get(BRANCH_ARRAY)
    if b is not None and len(kept) == len(polys) and np.asarray(b).dtype != object:
        b = np.asarray(b, float).reshape(len(points), -1)[:, 0]
        for p, idx in zip(polys, kept):
            p.branch = b[idx]
    return polys, meta


qc.polys_from_mesh = _polys_with_branch  # parse_vtk_legacy looks it up by name at call time


def read_cases(src_path, limit=None):
    """{case: [Poly]} plus counts; label numbering and code names set as in centerline_qc.main()."""
    src = qc.Source(src_path)
    cases, _, _ = qc.group_cases(src.members)
    items = list(cases.items())[:limit] if limit else list(cases.items())
    parsed, n_err, raw = {}, 0, Counter()
    code_use = defaultdict(lambda: {"names": Counter(), "files": 0, "unnamed": 0, "points": 0})
    has_radius = Counter()
    for k, (cid, ms) in enumerate(items, 1):
        polys, bad = [], False
        for m in ms:
            if qc.ext(m) not in qc.PARSEABLE and not qc.ext(m).endswith(".gz"):
                continue
            try:
                p, meta = qc.parse_member(m, src.read(m))
                polys += p
                qc.count_codes(p, meta, code_use)
            except Exception:  # noqa: BLE001 - counted, never printed with the case ID
                bad = True
        if polys:
            parsed[cid] = polys
            raw.update(str(l) for p in polys for l in p.labels)
            has_radius["yes" if any(p.radius is not None for p in polys) else "no"] += 1
        n_err += bad or not polys
        if k % 100 == 0:
            print(f"  read {k}/{len(items)}")
    qc.LABEL_NUMBERING = LABEL_NUMBERING
    qc.decide_numbering(raw)
    for c, u in code_use.items():
        if u["names"]:
            qc._code_names[c] = u["names"].most_common(1)[0][0]
    qc._code_names.update(qc.CODE_NAMES)
    qc._code_names.update(CODE_NAMES)
    return parsed, {"cases_found": len(cases), "cases_read": len(items), "read_errors": n_err,
                    "has_radius": has_radius, "code_use": code_use}


# ---------------------------------------------------------------- graph
def build_graph(polys):
    """One graph per case, nodes and edges exactly as centerline_qc.analyse_case builds them."""
    polys, _ = qc.split_gaps(polys)
    polys = [p for p in polys if len(p.pts) >= 2 and np.isfinite(p.pts).all()]
    if not polys:
        raise ValueError("no usable polyline")
    P = np.concatenate([p.pts for p in polys])
    L = [qc.normalise_label(l) for p in polys for l in p.labels]
    R = np.concatenate([p.radius if p.radius is not None and len(p.radius) == len(p.pts)
                        else np.full(len(p.pts), np.nan) for p in polys])
    B = np.concatenate([getattr(p, "branch", None) if getattr(p, "branch", None) is not None
                        else np.full(len(p.pts), np.nan) for p in polys])
    pid = np.concatenate([np.full(len(p.pts), i) for i, p in enumerate(polys)])
    key = np.round(P / qc.DEDUP_TOL).astype(np.int64)
    _, node = np.unique(key, axis=0, return_inverse=True)
    node = node.ravel()
    n = int(node.max()) + 1
    pts = np.zeros((n, 3)); pts[node] = P
    lab = np.full(n, None, dtype=object)
    for i, l in enumerate(L):
        if lab[node[i]] is None:
            lab[node[i]] = l
    ok = np.isfinite(R)
    rsum = np.bincount(node[ok], R[ok], minlength=n); rcnt = np.bincount(node[ok], minlength=n)
    rad = np.where(rcnt > 0, rsum / np.maximum(rcnt, 1), np.nan)
    br = np.full(n, np.nan)
    for i in range(len(B) - 1, -1, -1):  # first value seen wins
        if np.isfinite(B[i]):
            br[node[i]] = B[i]

    edges, starts, n_dup = set(), np.cumsum([0] + [len(p.pts) for p in polys]), 0
    for i in range(len(polys)):
        idx = node[starts[i]:starts[i + 1]]
        n_dup += int((idx[1:] == idx[:-1]).sum())  # repeated points inside one polyline
        edges.update((min(a, b), max(a, b)) for a, b in zip(idx[:-1], idx[1:]) if a != b)
    for i in range(len(polys)):  # polyline ends within JOIN_TOL of another polyline are joined
        other = pid != i
        if not other.any():
            continue
        for e in (starts[i], starts[i + 1] - 1):
            d, j = qc.nearest(P[e][None], P[other])
            j = int(np.where(other)[0][int(np.ravel(j)[0])])
            if float(np.ravel(d)[0]) <= qc.JOIN_TOL and node[e] != node[j]:
                edges.add((min(node[e], node[j]), max(node[e], node[j])))

    adj = [[] for _ in range(n)]
    for a, b in edges:
        w = float(np.linalg.norm(pts[a] - pts[b]))
        adj[a].append((b, w)); adj[b].append((a, w))
    deg = np.array([len(x) for x in adj])
    w_node = np.array([sum(w for _, w in x) / 2 for x in adj])  # each edge split half/half
    comp = np.full(n, -1)
    for s in range(n):
        if comp[s] >= 0:
            continue
        comp[s], stack = s, [s]
        while stack:
            x = stack.pop()
            for y, _ in adj[x]:
                if comp[y] < 0:
                    comp[y] = s; stack.append(y)
    n_edges = Counter(comp[a] for a, _ in edges)
    n_nodes = Counter(comp)
    cycles = {c: n_edges.get(c, 0) - n_nodes[c] + 1 for c in n_nodes}
    branch_const = [len(set(np.asarray(getattr(p, "branch", []))[np.isfinite(getattr(p, "branch", np.zeros(0)))]))
                    <= 1 for p in polys if getattr(p, "branch", None) is not None]
    return {"n": n, "pts": pts, "lab": lab, "rad": rad, "branch": br, "adj": adj, "deg": deg,
            "w": w_node, "comp": comp, "cycles": cycles, "total_mm": float(w_node.sum()),
            "n_dup_points": n_dup, "branch_constant_per_polyline": branch_const}


def dijkstra(adj, sources, n):
    dist, pred = np.full(n, np.inf), np.full(n, -1)
    heap = [(0.0, s) for s in sources]
    for s in sources:
        dist[s] = 0.0
    heapq.heapify(heap)
    while heap:
        d, x = heapq.heappop(heap)
        if d > dist[x]:
            continue
        for y, w in adj[x]:
            if d + w < dist[y]:
                dist[y], pred[y] = d + w, x
                heapq.heappush(heap, (d + w, y))
    return dist, pred


def side_of(label):
    return qc.TERRITORY.get(label, label)


# ---------------------------------------------------------------- one trunk
def trunk(G, artery):
    """Path metrics of one trunk: ostium -> farthest point with the most distal trunk label."""
    rank, lab, deg, n = RANK[artery], G["lab"], G["deg"], G["n"]
    first = min((s for s in rank if rank[s] == 1))
    m = {"artery_present": any(l in rank and l != "LM" for l in lab)}
    first_nodes = np.where(lab == first)[0]
    if not len(first_nodes):
        return {**m, "path_found": False}
    c = Counter(G["comp"][first_nodes]).most_common(1)[0][0]
    in_c = G["comp"] == c
    first_nodes = first_nodes[in_c[first_nodes]]
    lm_nodes = np.where(in_c & (lab == "LM"))[0] if artery in LEFT else np.zeros(0, int)
    nxt = np.where(in_c & np.isin(lab, [s for s in rank if rank[s] == 2]))[0]
    orientation_known = True
    if len(lm_nodes):  # left: LM end point farthest from the first trunk segment
        d, _ = dijkstra(G["adj"], list(first_nodes), n)
        cand = [x for x in lm_nodes if deg[x] == 1] or list(lm_nodes)
    else:  # no LM (left) or RCA: end point of the first segment farthest from the next segment
        cand = [x for x in first_nodes if deg[x] == 1] or list(first_nodes)
        if len(nxt):
            d, _ = dijkstra(G["adj"], list(nxt), n)
        else:
            d, orientation_known = np.zeros(n), False
    ostium = int(max(cand, key=lambda x: d[x]))
    dist, pred = dijkstra(G["adj"], [ostium], n)
    trunk_nodes = [x for x in np.where(in_c & np.isfinite(dist))[0] if lab[x] in rank and lab[x] != "LM"]
    top = max(rank[lab[x]] for x in trunk_nodes)
    target = max((x for x in trunk_nodes if rank[lab[x]] == top), key=lambda x: dist[x])
    path = [int(target)]
    while path[-1] != ostium:
        path.append(int(pred[path[-1]]))
    path = path[::-1]

    P = G["pts"][path]
    el = np.linalg.norm(np.diff(P, axis=0), axis=1)
    w = np.zeros(len(path)); w[:-1] += el / 2; w[1:] += el / 2
    pl = [lab[x] for x in path]
    seg = defaultdict(float)
    for l, wi in zip(pl, w):
        seg[l] += wi
    foreign = sum(wi for l, wi in zip(pl, w) if l is not None and l not in rank)
    unl = seg.get(None, 0.0)

    def longest_run(test):
        best = cur = 0.0
        for l, wi in zip(pl, w):
            cur = cur + wi if test(l) else 0.0
            best = max(best, cur)
        return best

    ranks = [rank[l] for l in pl if l in rank]
    k0 = next((k for k, l in enumerate(pl) if l in rank and rank[l] >= 1), len(pl) - 1)
    labels_c = Counter()
    for x in np.where(in_c)[0]:
        labels_c[side_of(lab[x])] += 1
    own = [s for s in rank if s != "LM"]
    tot_own = sum(G["w"][(lab == s)].sum() for s in own)
    in_c_own = sum(G["w"][(lab == s) & in_c].sum() for s in own)
    on_path_own = sum(seg.get(s, 0.0) for s in own)
    r = G["rad"][path]
    lo, hi = RADIUS_RANGE
    m.update({
        "path_found": True, "orientation_known": orientation_known,
        "ostium_is_end": bool(deg[ostium] == 1), "lm_in_component": bool(len(lm_nodes)),
        "path_mm": round(float(el.sum()), 2), "trunk_mm": round(float(el[k0:].sum()), 2),
        "lm_mm": round(seg.get("LM", 0.0), 2),
        **{f"{s}_mm": round(seg.get(s, 0.0), 2) for s in own},
        "foreign_mm": round(foreign, 2), "foreign_run_mm": round(longest_run(lambda l: l is not None and l not in rank), 2),
        "unlabelled_mm": round(unl, 2), "unlabelled_run_mm": round(longest_run(lambda l: l is None), 2),
        "unlabelled_pct": round(100 * unl / el.sum(), 2) if el.sum() else np.nan,
        "monotone": bool(all(a <= b for a, b in zip(ranks[:-1], ranks[1:]))),
        "n_order_breaks": int(sum(a > b for a, b in zip(ranks[:-1], ranks[1:]))),
        "max_step_mm": round(float(el.max()), 3) if len(el) else 0.0,
        "fragment_mm": round(float(tot_own - in_c_own), 2),
        "offpath_same_label_mm": round(float(in_c_own - on_path_own), 2),
        "cycles_in_component": int(G["cycles"][c]),
        "left_right_mixed": bool(any(labels_c[s] for s in OTHER_SIDE["left" if artery in LEFT else "right"])),
        "radius_present": bool(np.isfinite(r).any()),
        "radius_valid_frac": round(float(np.mean(np.isfinite(r) & (r >= lo) & (r <= hi))), 3),
        "radius_median": round(float(np.nanmedian(r)), 3) if np.isfinite(r).any() else np.nan,
        "n_branch_ids_on_path": int(len(np.unique(G["branch"][path][np.isfinite(G["branch"][path])]))),
        "ostium_node": ostium, "path_nodes": path,
    })
    return m


def grade(m, artery, tier, case_ok):
    """Reasons why the trunk is not of this tier (empty list = it is)."""
    if not case_ok:
        return ["case_total_length_odd"]
    if not m["artery_present"]:
        return ["artery_absent"]
    if not m["path_found"]:
        return [f"no_{min(s for s in RANK[artery] if RANK[artery][s] == 1)}"]
    why = []
    for group in REQUIRED[tier][artery]:
        if max(m.get(f"{s}_mm", 0.0) for s in group) < MIN_SEG_MM[tier]:
            why.append(f"{group[0]}_missing_or_short")
    if not m["orientation_known"]:
        why.append("orientation_unknown")
    if artery in LEFT:
        if tier == "strict":
            if m["lm_mm"] < MIN_LM_MM["strict"]:
                why.append("no_LM_on_path")
            elif m["lm_mm"] > MAX_LM_MM:
                why.append("LM_too_long")
        elif 0 < m["lm_mm"] < MIN_LM_MM["acceptable"]:
            why.append("LM_fragment")
    if tier == "strict" and not m["ostium_is_end"]:
        why.append("ostium_not_end_point")
    if not m["monotone"]:
        why.append("labels_not_in_order")
    if m["foreign_mm"] > FOREIGN_MM[tier]:
        why.append("foreign_label_on_path")
    if m["unlabelled_run_mm"] > UNLAB_RUN_MM[tier]:
        why.append("unlabelled_stretch_on_path")
    if m["unlabelled_pct"] > UNLAB_PCT[tier]:
        why.append("unlabelled_share_on_path")
    if m["max_step_mm"] > MAX_STEP_MM:
        why.append("jump_on_path")
    if m["trunk_mm"] < MIN_TRUNK_MM[tier][artery]:
        why.append("trunk_too_short")
    if m["radius_present"] and m["radius_valid_frac"] < RADIUS_VALID_FRAC:
        why.append("radius_implausible")
    if REQUIRE_RADIUS and not m["radius_present"]:
        why.append("radius_absent")
    if tier == "strict":
        if m["fragment_mm"] > FRAGMENT_MM:
            why.append("trunk_label_fragment_elsewhere")
        if m["cycles_in_component"] > 0:
            why.append("cycle_in_tree")
        if m["left_right_mixed"]:
            why.append("left_right_mixed")
    return why


def grade_lm(G, lad, cx, case_ok):
    """LM tier from the LAD and CX paths: present, one piece, free ostium, shared by both paths."""
    lab = G["lab"]
    lm = np.where(lab == "LM")[0]
    m = {"lm_present": bool(len(lm)), "lm_mm": max(lad.get("lm_mm", 0.0), cx.get("lm_mm", 0.0)),
         "lm_total_mm": round(float(G["w"][lm].sum()), 2) if len(lm) else 0.0}
    pieces = set()
    if len(lm):  # LM pieces: components of the graph restricted to LM nodes
        lm_set, seen = set(lm.tolist()), set()
        for s in lm:
            if s in seen:
                continue
            pieces.add(s); stack = [s]; seen.add(s)
            while stack:
                x = stack.pop()
                for y, _ in G["adj"][x]:
                    if y in lm_set and y not in seen:
                        seen.add(y); stack.append(y)
    on_lad, on_cx = lad.get("lm_mm", 0.0) > 0, cx.get("lm_mm", 0.0) > 0
    same_ostium = on_lad and on_cx and lad.get("ostium_node") == cx.get("ostium_node")
    m.update({"lm_pieces": len(pieces), "lm_on_lad_path": on_lad, "lm_on_cx_path": on_cx,
              "lm_shared_ostium": bool(same_ostium),
              "ostium_is_end": bool(lad.get("ostium_is_end") if on_lad else cx.get("ostium_is_end", False))})
    reasons = {"strict": [], "acceptable": []}
    if not case_ok:
        reasons = {t: ["case_total_length_odd"] for t in reasons}
    elif not len(lm):
        reasons = {t: ["LM_absent"] for t in reasons}
    else:
        r = reasons["strict"]
        if len(pieces) > 1: r.append("LM_in_pieces")
        if not same_ostium: r.append("LM_not_shared_by_LAD_and_CX")
        if not m["ostium_is_end"]: r.append("ostium_not_end_point")
        if m["lm_mm"] < MIN_LM_MM["strict"]: r.append("LM_short")
        if m["lm_mm"] > MAX_LM_MM: r.append("LM_too_long")
        if (lad.get("left_right_mixed") if on_lad else cx.get("left_right_mixed")): r.append("left_right_mixed")
        if not (on_lad or on_cx): reasons["acceptable"].append("LM_not_on_any_path")
        elif m["lm_mm"] < MIN_LM_MM["acceptable"]: reasons["acceptable"].append("LM_short")
    return m, reasons


def tier_of(reasons):
    return "strict" if not reasons["strict"] else "acceptable" if not reasons["acceptable"] else "excluded"


# ---------------------------------------------------------------- report
def md_table(df):
    df = df.fillna("")
    cols = [str(c) for c in df.columns]
    rows = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    rows += ["| " + " | ".join(str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join(rows)


def settings():
    names = ("LABEL_NUMBERING", "CODE_NAMES", "CASE_MIN_TOTAL_MM", "CASE_MAX_TOTAL_MM", "REQUIRED", "MIN_SEG_MM",
             "MIN_TRUNK_MM", "MIN_LM_MM", "MAX_LM_MM", "FOREIGN_MM", "UNLAB_RUN_MM", "UNLAB_PCT", "MAX_STEP_MM",
             "FRAGMENT_MM", "REQUIRE_RADIUS", "RADIUS_RANGE", "RADIUS_VALID_FRAC", "MIN_CELL", "QUARTILE_MIN")
    g = globals()
    return {k: g[k] for k in names} | {"DEDUP_TOL (qc)": qc.DEDUP_TOL, "JOIN_TOL (qc)": qc.JOIN_TOL}


def write_report(out, info, df, extra):
    n = df["case"].nunique()
    arteries = ["LM", "LAD", "CX", "RCA"]
    R = ["# Centerline selection per artery (aggregate only)", "",
         f"Cases found: {count(info['cases_found'])}; read: {count(info['cases_read'])}; "
         f"**analysed: {count(n)}**; read errors: {count(info['read_errors'])}; "
         f"analysis errors: {count(extra['analysis_errors'])}.", "",
         "No case ID or row-level value is in this file. Counts from 1 to "
         f"{MIN_CELL - 1} are shown as `{SMALL}`; `{HIDDEN}` = hidden so that a small count cannot be "
         "worked out from a row total. Reasons overlap (a case can fail several).", "",
         "Settings:", "", *[f"- `{k}` = `{json.dumps(v, default=str)}`" for k, v in settings().items()], ""]

    R += ["## Tier per artery", ""]
    t = np.array([[int((df.loc[df.artery == a, "tier"] == tr).sum()) for tr in TIERS] for a in arteries])
    shown = suppress(t)
    tab = pd.DataFrame(shown, columns=TIERS)
    tab.insert(0, "artery", arteries)
    tab["usable (strict + acceptable)"] = [count_of(t[i, 0] + t[i, 1], n) for i in range(len(arteries))]
    R += [md_table(tab), ""]

    R += ["## Why trunks are not strict / are excluded", "",
          "`not strict` counts every case below strict (acceptable or excluded) that fails the strict "
          "criterion; `excluded` counts the excluded cases that fail the acceptable criterion.", ""]
    for a in arteries:
        sub = df[df.artery == a]
        ns = Counter(x for s in sub.loc[sub.tier != "strict", "why_not_strict"] for x in s.split(";") if x)
        ex = Counter(x for s in sub.loc[sub.tier == "excluded", "why_excluded"] for x in s.split(";") if x)
        keys = sorted(set(ns) | set(ex), key=lambda k: -(ns[k] + ex[k]))
        R += [f"### {a}", ""]
        R += [md_table(pd.DataFrame([{"reason": k, "not strict": count(ns[k]), "excluded": count(ex[k])}
                                     for k in keys])) if keys else "none", ""]

    R += ["## Usable arteries per case (LAD, CX, RCA)", "",
          "Usable = strict or acceptable. Separate models per artery, so this is for information only.", ""]
    piv = df[df.artery.isin(["LAD", "CX", "RCA"])].pivot(index="case", columns="artery", values="tier")
    usable = piv.isin(["strict", "acceptable"])
    pat = usable.apply(lambda r: "+".join(a for a in ("LAD", "CX", "RCA") if r.get(a, False)) or "none", axis=1)
    order = ["LAD+CX+RCA", "LAD+CX", "LAD+RCA", "CX+RCA", "LAD", "CX", "RCA", "none"]
    vc = pat.value_counts()
    shown = suppress([[int(vc.get(k, 0))] for k in order])
    R += [md_table(pd.DataFrame({"usable arteries": order, "cases": shown[:, 0]})), ""]
    strict_all = int((piv == "strict").all(axis=1).sum())
    R += [f"All three strict: {count_of(strict_all, n)} of {count(n)}.", ""]

    R += ["## LAD and CX by LM tier", "",
          "LM must be plaque-free for LAD / CX eligibility (a reader variable, ct_cag_lm_*); this shows how "
          "often the LM centerline itself is usable alongside the trunk.", ""]
    lm = df[df.artery == "LM"].set_index("case")["tier"]
    for a in LEFT:
        tr = df[df.artery == a].set_index("case")["tier"]
        ct = pd.crosstab(lm.reindex(tr.index), tr).reindex(index=list(TIERS), columns=list(TIERS)).fillna(0)
        shown = suppress(ct.to_numpy())
        tab = pd.DataFrame(shown, columns=[f"{a} {c}" for c in TIERS])
        tab.insert(0, "LM tier", list(TIERS))
        R += [f"### {a}", "", md_table(tab), ""]

    R += ["## Path lengths (mm) by artery and tier", "",
          "Measured on the ostium-to-distal path, not summed over every point with the label "
          "(that is what report_qc.md shows). Mean/SD from 5 values, quartiles from 10; no min/max.", ""]
    rows = []
    for a in ("LAD", "CX", "RCA"):
        cols = ["trunk_mm", "lm_mm"] + [f"{s}_mm" for s in RANK[a] if s != "LM"] + \
               ["unlabelled_mm", "foreign_mm", "offpath_same_label_mm", "fragment_mm"]
        for tr in TIERS:
            sub = df[(df.artery == a) & (df.tier == tr) & df["path_found"].fillna(False).astype(bool)]
            for ccol in cols:
                if ccol in sub and (a in LEFT or ccol != "lm_mm"):
                    rows.append({"artery": a, "tier": tr, "measure": ccol, **describe(sub[ccol])})
    R += [md_table(pd.DataFrame(rows)), ""]

    R += ["## Radius, duplicates and the `branch` array", ""]
    hr = info["has_radius"]
    R += [f"- Cases with a radius array: {count(hr.get('yes', 0))} of {count(sum(hr.values()))} "
          "(report_qc.md found none; trunk taper then needs a radius from the CT lumen, e.g. "
          "tortuosity/taper.py cross-sections).",
          f"- Cases with repeated consecutive points inside a polyline: {count(extra['dup_cases'])}.",
          f"- Polylines whose `{BRANCH_ARRAY}` value is constant along the polyline: "
          f"{count(extra['branch_const'])} of {count(extra['branch_polys'])} polylines carrying it "
          f"(if all, `{BRANCH_ARRAY}` is a polyline / path ID - confirm with Kit)."]
    for a in ("LAD", "CX", "RCA"):
        sub = df[(df.artery == a) & df["path_found"].fillna(False).astype(bool)]
        d = describe(sub["n_branch_ids_on_path"]) if "n_branch_ids_on_path" in sub else {"n": 0}
        R.append(f"- distinct `{BRANCH_ARRAY}` values on the {a} path: "
                 + ", ".join(f"{k} {v}" for k, v in d.items() if v is not None))
    R += ["", "## Label codes used (files, not cases)", ""]
    cu = info["code_use"]
    R += [md_table(pd.DataFrame([{"code": c, "name used": qc.normalise_label(c) or "(unlabelled)",
                                  "files using it": count(u["files"])} for c, u in sorted(cu.items())])), ""]
    (out / "selection_report.md").write_text("\n".join(R), encoding="utf-8")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--src", default=ZIP_PATH, help="zip file or folder with the centerlines (default ZIP_PATH)")
    ap.add_argument("--out", default=OUT_DIR, help="output folder (default OUT_DIR)")
    ap.add_argument("--limit", type=int, default=None, help="only analyse the first N cases")
    args = ap.parse_args()
    if not Path(args.src).expanduser().exists():
        raise SystemExit(f"source not found: {args.src} (set ZIP_PATH at the top of {Path(__file__).name})")
    out = Path(args.out).expanduser()
    (out / SECURE_SUBDIR).mkdir(parents=True, exist_ok=True)

    parsed, info = read_cases(args.src, args.limit)
    print(f"{info['cases_read']} cases read, {len(parsed)} with centerlines")
    rows, extra = [], {"analysis_errors": 0, "dup_cases": 0, "branch_const": 0, "branch_polys": 0}
    for k, (cid, polys) in enumerate(parsed.items(), 1):
        try:
            G = build_graph(polys)
            case_ok = CASE_MIN_TOTAL_MM <= G["total_mm"] <= CASE_MAX_TOTAL_MM
            res = {a: trunk(G, a) for a in ("LAD", "CX", "RCA")}
        except Exception:  # noqa: BLE001 - counted only, the case ID is not printed
            extra["analysis_errors"] += 1
            continue
        extra["dup_cases"] += G["n_dup_points"] > 0
        extra["branch_const"] += sum(G["branch_constant_per_polyline"])
        extra["branch_polys"] += len(G["branch_constant_per_polyline"])
        for a, m in res.items():
            why = {t: grade(m, a, t, case_ok) for t in ("strict", "acceptable")}
            rows.append({"case": cid, "artery": a, "tier": tier_of(why), "why_not_strict": ";".join(why["strict"]),
                         "why_excluded": ";".join(why["acceptable"]), "case_total_mm": round(G["total_mm"], 1),
                         **{kk: v for kk, v in m.items() if kk not in ("path_nodes", "ostium_node")}})
        m, why = grade_lm(G, res["LAD"], res["CX"], case_ok)
        rows.append({"case": cid, "artery": "LM", "tier": tier_of(why), "why_not_strict": ";".join(why["strict"]),
                     "why_excluded": ";".join(why["acceptable"]), "case_total_mm": round(G["total_mm"], 1), **m})
        if k % 100 == 0:
            print(f"  graded {k}/{len(parsed)}")
    df = pd.DataFrame(rows)
    if df.empty:
        raise SystemExit("no case could be analysed - run centerline_qc.py --inspect first")
    secure = out / SECURE_SUBDIR / "centerline_tiers.csv"
    df.to_csv(secure, index=False)
    write_report(out, info, df, extra)
    print(f"wrote {secure} (case IDs - keep on this machine) and {out / 'selection_report.md'} (aggregate)")


if __name__ == "__main__":
    sys.exit(main())
