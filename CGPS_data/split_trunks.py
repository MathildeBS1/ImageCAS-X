"""Split the LAD, LCx and RCA of each centerline tree into proximal / mid / distal (best guess, SCCT).

    python CGPS_data/split_trunks.py [--src TREE_FOLDER] [--out CSV]

LAD: LM bifurcation -> first diagonal (p) -> half the remaining distance to the LAD end (m) -> end (d).
LCx: LM bifurcation -> OM1 (p) -> OM2 (m) -> end (d).
RCA: ostium -> half way to the acute margin (p) -> acute margin (m) -> PDA origin (d); the acute margin
is the RCA point farthest from the ostium-to-crux chord. A missing landmark falls back to the first
side branch >= 15 mm long, and without one to a fixed fraction of the trunk.
Writes one row per tree, artery and segment: start and end in mm along the trunk (contains IDs).
"""
import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra

import hoe10y_qc as hq
from cgps_stats import OUT_DIR

TRUNK = {"LAD": {"plad", "mlad", "dlad", "lad"}, "CX": {"pcx", "mcx", "dcx", "cx"}, "RCA": {"prca", "mrca", "drca", "rca"}}
NAMES = {"LAD": ("plad", "mlad", "dlad"), "CX": ("pcx", "mcx", "dcx"), "RCA": ("prca", "mrca", "drca")}
BRANCH = {"LAD": r"^d\d", "CX": r"^om\d", "RCA": r"^pda$"}
MIN_BRANCH = 15.0
ARTERY_OF = {k: a.lower() for a, ks in TRUNK.items() for k in ks}


def graph(tree):
    P = np.concatenate([p for p, _ in tree])
    labels = [ARTERY_OF.get(l, l) for _, ls in tree for l in ls]  # trunk labels collapsed to the artery
    _, node = np.unique(np.round(P, 2), axis=0, return_inverse=True)
    node = node.ravel()
    X, lab = np.zeros((node.max() + 1, 3)), [None] * (node.max() + 1)
    X[node] = P
    for i, l in enumerate(labels):
        lab[node[i]] = lab[node[i]] or l
    starts = np.cumsum([0] + [len(p) for p, _ in tree])
    E = {tuple(sorted(e)) for a, b in zip(starts[:-1], starts[1:]) for e in zip(node[a:b - 1], node[a + 1:b]) if e[0] != e[1]}
    for a, b in zip(starts[:-1], starts[1:]):  # join loose polyline ends within 1 mm
        for e in (a, b - 1):
            d = np.linalg.norm(P - P[e], axis=1)
            d[a:b] = np.inf
            if d.min() <= 1.0 and node[e] != node[d.argmin()]:
                E.add(tuple(sorted((node[e], node[d.argmin()]))))
    E = np.array(sorted(E))
    w = np.linalg.norm(X[E[:, 0]] - X[E[:, 1]], axis=1)
    G = coo_matrix((np.r_[w, w], (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(len(X),) * 2).tocsr()
    return X, lab, G


def trunk_path(X, lab, G, artery):
    nodes = [i for i, l in enumerate(lab) if l == artery.lower()]
    if not nodes:
        return None
    reach = np.isfinite(dijkstra(G, indices=nodes[0]))
    ends = list(np.where(reach & (np.diff(G.indptr) == 1))[0])
    ok = {"rca"} if artery == "RCA" else {"lad", "cx"}
    root = max([e for e in ends if lab[e] == "lm"] or [e for e in ends if lab[e] in ok or lab[e] is None] or ends,
               key=lambda e: X[e, 2])  # ostium: LM end, else the most superior trunk end (LPS +z)
    D, pred = dijkstra(G, indices=root, return_predecessors=True)
    p = [max(nodes, key=lambda i: D[i])]
    while p[-1] != root:
        p.append(pred[p[-1]])
    return p[::-1]


def branches(p, G, lab):
    """(arc length, length, label) of each side branch leaving the path."""
    on, s, out = set(p), np.r_[0, np.cumsum([G[a, b] for a, b in zip(p[:-1], p[1:])])], []
    for k, v in enumerate(p):
        for u in G[v].indices:
            if u in on:
                continue
            seen, stack, length, labs = {v, u}, [u], G[v, u], []
            while stack:
                x = stack.pop()
                labs += [lab[x]] if lab[x] else []
                for y in G[x].indices:
                    if y not in seen and y not in on:
                        seen.add(y); stack.append(y); length += G[x, y]
            out.append((s[k], length, max(set(labs), key=labs.count) if labs else ""))
    return out, s


def split(X, lab, G):
    paths = {a: trunk_path(X, lab, G, a) for a in TRUNK}
    if paths["LAD"] and paths["CX"]:  # LAD and LCx start at the LM bifurcation
        common = sum(1 for a, b in zip(paths["LAD"], paths["CX"]) if a == b)
        paths["LAD"], paths["CX"] = paths["LAD"][common - 1:], paths["CX"][common - 1:]
    out = {}
    for a, p in paths.items():
        if not p or len(p) < 3:
            continue
        br, s = branches(p, G, lab)
        L = s[-1]
        marks = [b[0] for b in br if re.match(BRANCH[a], b[2])] or [b[0] for b in br if b[1] >= MIN_BRANCH]
        marks = sorted(m for m in marks if m > 1.0)
        if a == "LAD":
            pm = marks[0] if marks else 0.25 * L
            out[a] = (pm, (pm + L) / 2, L)
        elif a == "CX":
            pm = marks[0] if marks else L / 3
            out[a] = (pm, next((m for m in marks if m > pm + 1.0), (pm + L) / 2), L)
        else:
            crux = next((m for m in marks if m > 0.3 * L), L)
            Y = X[p]
            chord = Y[max(np.searchsorted(s, crux) - 1, 1)] - Y[0]
            dist = np.linalg.norm(np.cross(Y - Y[0], chord), axis=1)
            mid = (s > 0.2 * crux) & (s < 0.9 * crux)
            acute = s[mid][dist[mid].argmax()] if mid.any() else 2 / 3 * crux
            out[a] = (acute / 2, acute, crux)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / "split_trunks.csv"))
    args = ap.parse_args()
    rows, failed = [], 0
    files = sorted(Path(args.src).rglob("*.vtk"))
    for f in files:
        try:
            for a, (pm, md, end) in split(*graph(hq.tree_points(f))).items():
                for seg, lo, hi in zip(NAMES[a], (0, pm, md), (pm, md, end)):
                    rows.append({"id": hq.id_from_name(f.name) or f.stem, "artery": a, "segment": seg,
                                 "start_mm": round(lo, 1), "end_mm": round(hi, 1)})
        except Exception:  # noqa: BLE001 - counted
            failed += 1
    df = pd.DataFrame(rows)
    sheets = hq.load_sheets(hq.ROOT)  # visual reads: patient status and each segment's grade at BL and FU
    if len(df) and "BL" in sheets:
        bl, fu = (s.assign(id=s["study_id"].map(hq.norm_id)).drop_duplicates("id").set_index("id")
                  for s in (sheets["BL"], sheets.get("FU", sheets["BL"].iloc[:0])))
        clean = (pd.to_numeric(bl["ct_cag_sis"], errors="coerce") == 0) & (pd.to_numeric(bl["ct_cag_sss"], errors="coerce") == 0)
        df["clean_bl"] = df["id"].map(clean)
        df["read_bl"] = df["id"].map(bl["ct_cag_visual_read"]) if "ct_cag_visual_read" in bl else None
        for tag, t in (("bl", bl), ("fu", fu)):
            df[f"grade_{tag}"] = [hq.grade_of(t.at[i, f"ct_cag_{s}_stenosis"]) if i in t.index and f"ct_cag_{s}_stenosis" in t
                                  else "no read" for i, s in zip(df["id"], df["segment"])]
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)
    print(f"{len(files)} trees, {failed} failed -> {args.out}")


if __name__ == "__main__":
    main()
