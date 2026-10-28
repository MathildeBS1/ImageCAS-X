"""Split the LAD, LCx and RCA of each centerline tree into proximal / mid / distal (best guess, SCCT).

    python CGPS_data/split_trunks.py [--src TREE_FOLDER] [--out CSV] a

LAD: LM bifurcation -> first diagonal (p) -> half the remaining distance to the LAD end (m) -> end (d).
LCx: LM bifurcation -> OM1 (p) -> OM2 (m) -> end (d).
RCA: ostium -> half way to the acute margin (p) -> acute margin (m) -> PDA origin (d); the acute margin
is the RCA point farthest from the ostium-to-crux chord. A missing landmark falls back to the first
side branch >= 15 mm long, and without one to a fixed fraction of the trunk.
Writes one row per tree, artery and segment: start and end in mm along the trunk, the rule used and
the visual grade at BL and FU (contains IDs, stays on the server), plus split_trunks.md next to it
with aggregates only (counts 1-4 hidden), to share.
"""

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra

import hoe10y_qc as hq
from cgps_stats import OUT_DIR, count, describe, suppress, yes

TRUNK = {
    "LAD": {"plad", "mlad", "dlad", "lad"},
    "CX": {"pcx", "mcx", "dcx", "cx"},
    "RCA": {"prca", "mrca", "drca", "rca"},
}
NAMES = {
    "LAD": ("plad", "mlad", "dlad"),
    "CX": ("pcx", "mcx", "dcx"),
    "RCA": ("prca", "mrca", "drca"),
}
BRANCH = {"LAD": r"^d\d", "CX": r"^om\d", "RCA": r"^pda$"}
MIN_BRANCH = 15.0
ARTERY_OF = {k: a.lower() for a, ks in TRUNK.items() for k in ks}


def graph(tree):
    P = np.concatenate([p for p, _ in tree])
    labels = [
        ARTERY_OF.get(l, l) for _, ls in tree for l in ls
    ]  # trunk labels collapsed to the artery
    _, node = np.unique(np.round(P, 2), axis=0, return_inverse=True)
    node = node.ravel()
    X, lab = np.zeros((node.max() + 1, 3)), [None] * (node.max() + 1)
    X[node] = P
    for i, l in enumerate(labels):
        lab[node[i]] = lab[node[i]] or l
    starts = np.cumsum([0] + [len(p) for p, _ in tree])
    E = {
        tuple(sorted(e))
        for a, b in zip(starts[:-1], starts[1:])
        for e in zip(node[a : b - 1], node[a + 1 : b])
        if e[0] != e[1]
    }
    for a, b in zip(starts[:-1], starts[1:]):  # join loose polyline ends within 1 mm
        for e in (a, b - 1):
            d = np.linalg.norm(P - P[e], axis=1)
            d[a:b] = np.inf
            if d.min() <= 1.0 and node[e] != node[d.argmin()]:
                E.add(tuple(sorted((node[e], node[d.argmin()]))))
    E = np.array(sorted(E))
    w = np.linalg.norm(X[E[:, 0]] - X[E[:, 1]], axis=1)
    G = coo_matrix(
        (np.r_[w, w], (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])),
        shape=(len(X),) * 2,
    ).tocsr()
    return X, lab, G


def trunk_path(X, lab, G, artery):
    nodes = [i for i, l in enumerate(lab) if l == artery.lower()]
    if not nodes:
        return None
    reach = np.isfinite(dijkstra(G, indices=nodes[0]))
    ends = list(np.where(reach & (np.diff(G.indptr) == 1))[0])
    ok = {"rca"} if artery == "RCA" else {"lad", "cx"}
    root = max(
        [e for e in ends if lab[e] == "lm"]
        or [e for e in ends if lab[e] in ok or lab[e] is None]
        or ends,
        key=lambda e: X[e, 2],
    )  # ostium: LM end, else the most superior trunk end (LPS +z)
    D, pred = dijkstra(G, indices=root, return_predecessors=True)
    p = [max(nodes, key=lambda i: D[i])]
    while p[-1] != root:
        p.append(pred[p[-1]])
    return p[::-1]


def branches(p, G, lab):
    """(arc length, length, label) of each side branch leaving the path."""
    on, s, out = (
        set(p),
        np.r_[0, np.cumsum([G[a, b] for a, b in zip(p[:-1], p[1:])])],
        [],
    )
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
                        seen.add(y)
                        stack.append(y)
                        length += G[x, y]
            out.append((s[k], length, max(set(labs), key=labs.count) if labs else ""))
    return out, s


def split(X, lab, G):
    paths = {a: trunk_path(X, lab, G, a) for a in TRUNK}
    if paths["LAD"] and paths["CX"]:  # LAD and LCx start at the LM bifurcation
        common = sum(1 for a, b in zip(paths["LAD"], paths["CX"]) if a == b)
        paths["LAD"], paths["CX"] = (
            paths["LAD"][common - 1 :],
            paths["CX"][common - 1 :],
        )
    out = {}
    for a, p in paths.items():
        if not p or len(p) < 3:
            continue
        br, s = branches(p, G, lab)
        L = s[-1]
        labelled = sorted(b[0] for b in br if re.match(BRANCH[a], b[2]) and b[0] > 1.0)
        marks = labelled or sorted(
            b[0] for b in br if b[1] >= MIN_BRANCH and b[0] > 1.0
        )
        rule = (
            "labelled branch"
            if labelled
            else "long branch"
            if marks
            else "fraction of length"
        )
        if a == "LAD":
            pm = marks[0] if marks else 0.25 * L
            out[a] = (pm, (pm + L) / 2, L, rule)
        elif a == "CX":
            pm = marks[0] if marks else L / 3
            out[a] = (
                pm,
                next((m for m in marks if m > pm + 1.0), (pm + L) / 2),
                L,
                rule,
            )
        else:
            crux = next((m for m in marks if m > 0.3 * L), L)
            Y = X[p]
            chord = Y[max(np.searchsorted(s, crux) - 1, 1)] - Y[0]
            dist = np.linalg.norm(np.cross(Y - Y[0], chord), axis=1)
            mid = (s > 0.2 * crux) & (s < 0.9 * crux)
            acute = s[mid][dist[mid].argmax()] if mid.any() else 2 / 3 * crux
            found = any(m > 0.3 * L for m in marks)
            out[a] = (
                acute / 2,
                acute,
                crux,
                f"acute margin; crux at {rule}"
                if found
                else "acute margin; crux at trunk end",
            )
        out[a] = (*out[a], X[p], s)  # trunk points and arc length, for per-segment features
    return out


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--src",
        default=str(Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"),
    )
    ap.add_argument("--out", default=str(Path(OUT_DIR) / "split_trunks.csv"))
    args = ap.parse_args()
    rows, failed = [], 0
    files = sorted(Path(args.src).rglob("*.vtk"))
    for f in files:
        try:
            for a, (pm, md, end, rule, *_) in split(*graph(hq.tree_points(f))).items():
                for seg, lo, hi in zip(NAMES[a], (0, pm, md), (pm, md, end)):
                    rows.append(
                        {
                            "id": hq.id_from_name(f.name) or f.stem,
                            "artery": a,
                            "segment": seg,
                            "start_mm": round(lo, 1),
                            "end_mm": round(hi, 1),
                            "rule": rule,
                        }
                    )
        except Exception:  # noqa: BLE001 - counted
            failed += 1
    df = pd.DataFrame(rows)
    sheets = hq.load_sheets(
        hq.ROOT
    )  # visual reads: patient status and each segment's grade at BL and FU
    if len(df) and "BL" in sheets:
        bl, fu = (
            s.assign(id=s["study_id"].map(hq.norm_id))
            .drop_duplicates("id")
            .set_index("id")
            for s in (sheets["BL"], sheets.get("FU", sheets["BL"].iloc[:0]))
        )
        clean = (pd.to_numeric(bl["ct_cag_sis"], errors="coerce") == 0) & (
            pd.to_numeric(bl["ct_cag_sss"], errors="coerce") == 0
        )
        df["clean_bl"] = df["id"].map(clean)
        df["read_bl"] = (
            df["id"].map(bl["ct_cag_visual_read"])
            if "ct_cag_visual_read" in bl
            else None
        )
        for tag, t in (("bl", bl), ("fu", fu)):
            df[f"grade_{tag}"] = [
                hq.grade_of(t.at[i, f"ct_cag_{s}_stenosis"])
                if i in t.index and f"ct_cag_{s}_stenosis" in t
                else "no read"
                for i, s in zip(df["id"], df["segment"])
            ]
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)
    md = Path(args.out).with_suffix(".md")
    md.write_text(summary(df, len(files), failed), encoding="utf-8")
    print(f"{len(files)} trees, {failed} failed -> {args.out} and {md}")


def table(header, rows):
    return (
        "\n".join(
            [
                "| " + " | ".join(map(str, header)) + " |",
                "|" + "---|" * len(header),
                *["| " + " | ".join(map(str, r)) + " |" for r in rows],
            ]
        )
        + "\n"
    )


def summary(df, n_files, failed):
    """Aggregates only (cgps_stats rules): no IDs, counts 1-4 hidden, no min/max."""
    L = [
        "# Trunk split of the Medis trees (split_trunks.py)\n",
        "Aggregates only; counts 1-4 shown as <5. Best-guess SCCT split, no ground truth exists.\n",
        f"Trees: {count(n_files)}, failed: {count(failed)}.\n",
    ]
    if not len(df):
        return "\n".join(L)
    trees = df.drop_duplicates(["id", "artery"])
    L += [
        "## Rule used\n",
        table(
            ["artery", "rule", "trees"],
            [
                (a, r, count(n))
                for (a, r), n in trees.groupby(["artery", "rule"]).size().items()
            ],
        ),
    ]
    q = lambda d, k: "" if d.get(k) is None else f"{d[k]:.1f}"
    rows = []
    for a, segs in NAMES.items():
        for sg in segs:
            d = describe(
                (df.end_mm - df.start_mm)[(df.artery == a) & (df.segment == sg)]
            )
            rows.append((sg, d["n"], q(d, "p25"), q(d, "median"), q(d, "p75")))
    L += [
        "## Segment length (mm)\n",
        table(["segment", "trees", "p25", "median", "p75"], rows),
    ]
    if "clean_bl" not in df:
        return "\n".join(L + ["_No spreadsheet found: no plaque status._\n"])
    pat = df.drop_duplicates("id").set_index("id")
    read = (
        yes(pat["read_bl"]) == 1
        if "read_bl" in pat
        else pd.Series(False, index=pat.index)
    )
    status = np.select(
        [
            pat["clean_bl"].isna(),
            (pat["clean_bl"] == True) & read,
            pat["clean_bl"] == True,
        ],  # noqa: E712
        ["not in BL sheet", "clean at BL, read", "clean at BL, not read"],
        "plaque at BL",
    )
    L += [
        "## Trees by baseline status\n",
        "Clean = BL SIS 0 and new SSS 0; read = ct_cag_visual_read.\n",
        table(
            ["status", "patients"],
            [(k, count(v)) for k, v in pd.Series(status).value_counts().items()],
        ),
    ]
    # BL -> FU change of the visual grade in each split trunk segment, then per tree
    rank = {g: i for i, g in enumerate(hq.GRADES)}
    bg, fg = df["grade_bl"].map(rank), df["grade_fu"].map(rank)
    change = pd.Series(np.select([bg.isna() | fg.isna(), fg > bg, fg < bg], ["unknown", "progressed", "regressed"], "same"),
                       index=df.index)
    cols = ["same", "progressed", "regressed", "unknown"]
    t = pd.crosstab(df["segment"], change).reindex(columns=cols, fill_value=0)
    t = t.reindex([sg for segs in NAMES.values() for sg in segs if sg in t.index])
    per = change.groupby(df["id"]).agg(lambda c: "progressed" if (c == "progressed").any() else
                                       "regressed only" if (c == "regressed").any() else
                                       "stayed the same" if (c == "same").any() else "unknown")
    t2 = pd.crosstab(pd.Series(status, index=pat.index).reindex(per.index), per)
    t2 = t2.reindex(columns=[c for c in ("stayed the same", "progressed", "regressed only", "unknown") if c in t2.columns])
    L += ["## Progression BL -> FU in the 9 split trunk segments (all trees)\n",
          "Progressed = higher visual stenosis grade at FU (none -> minimal counts); unknown = not graded or "
          "unevaluable at either visit. Unread BL scans have segments filled 'none', so read their row with care.\n",
          table(["segment", *cols], [(sg, *r) for sg, r in zip(t.index, suppress(t.to_numpy()))]),
          "Per tree (progressed = at least one segment worse; regressed only = some better, none worse):\n",
          table(["status at BL", *t2.columns, "trees"],
                [(st, *r, count(n)) for st, r, n in zip(t2.index, suppress(t2.to_numpy()), t2.sum(axis=1))]),
          f"All trees: {', '.join(f'{k} {count(v)}' for k, v in per.value_counts().items())}.\n"]
    clean = df[df["id"].isin(pat.index[status == "clean at BL, read"])]
    if len(clean):
        cat = clean["grade_fu"].map(
            lambda g: (
                "plaque"
                if g in ("minimal", "mild", "moderate", "severe", "occlusion")
                else g
                if g in ("none", "unevaluable")
                else "no FU read"
            )
        )
        cols = ["none", "plaque", "unevaluable", "no FU read"]
        t = pd.crosstab(clean["segment"], cat).reindex(columns=cols, fill_value=0)
        t = t.reindex([s for segs in NAMES.values() for s in segs if s in t.index])
        shown = suppress(t.to_numpy())
        L += [
            "## Clean-baseline trees: each split segment at follow-up\n",
            table(
                ["segment", "no plaque", "new plaque", "unevaluable", "no FU read"],
                [(sg, *r) for sg, r in zip(t.index, shown)],
            ),
        ]
        per = clean.assign(p=cat == "plaque", r=cat.isin(["none", "plaque"])).groupby(
            "id"
        )
        any_p, any_r = per["p"].any(), per["r"].any()
        L.append(
            f"Clean-baseline trees with a FU read of the split trunks: {count(any_r.sum())}; stayed clean in "
            f"every split trunk segment: {count((any_r & ~any_p).sum())}; new plaque in at least one: "
            f"{count(any_p.sum())}.\n"
        )
    return "\n".join(L)


if __name__ == "__main__":
    main()
