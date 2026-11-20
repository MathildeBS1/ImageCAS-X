"""What is the bifurcation point O in Kit's delivered centerlines? Checks the sentence of sec:method-angle
"O is the last centerline point shared by the two arteries" against the raw tracer files.

    python CGPS_data/thesis_final/bifurcation_point_probe.py [--src TRACER_FOLDER] [--n N]

Two parts, on the left _ostium_pruned file of every BL participant with both tracer files:
  1. The raw file. Each LINES cell is one branch with a parent branch (cell data branch_id, parent). For every
     child branch: is its first point the same point as a point of its parent (within 0.01 mm), and does it
     leave from the parent's last point or from inside the parent? And the cell code of the root branch.
  2. O as the thesis code finds it (tracer_io.tracer_tree -> split_trunks.graph -> split with the tracer's own
     ostia, as medis_compare and bifurcation_angle do). Where O lies in the raw file: the last point of the
     root branch (the LM), a point repeated as the first point of the LAD and LCx branches, a point inside a
     branch, or none of these; the raw code at O; and how many LM-coded points the LAD and LCx paths carry past O.
Aggregate counts only (cgps_stats.count hides 1-4); no study_id is printed. Server only (reads the tracer files).
Output also written to bifurcation_point_probe.md next to this script (--out to change).
"""
import argparse
import io
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/
sys.path.insert(0, str(Path(__file__).resolve().parent))
import centerline_qc as cq
import tracer_io
from cgps_stats import count
from split_trunks import graph, split

SAME = 0.01  # mm: two points closer than this are the same point (graph() merges at 0.01 mm rounding)
CODE = {1: "LM", 2: "LAD", 3: "LCx"}


def left_cells(pid, src):
    """[(points, codes, branch_id, parent)] of the left pruned file, one per LINES cell."""
    v = cq.read_vtk_legacy(Path(tracer_io.tracer_files(pid, src)[0]).read_bytes())
    P, code = v["points"], np.asarray(v["point_data"]["segment_voted"]).astype(int)
    bid = np.asarray(v["cell_data"]["branch_id"]).astype(int)
    par = np.asarray(v["cell_data"]["parent"]).astype(int)
    return [(P[np.asarray(c)], code[np.asarray(c)], b, p)
            for c, b, p in zip(v["cells"].get("LINES", []), bid, par) if len(c) >= 2]


def cell_code(codes):
    return CODE.get(Counter(codes.tolist()).most_common(1)[0][0], "other")


def attachments(cells, tally):
    """Part 1: how each child branch meets its parent."""
    by_id = {b: (P, c) for P, c, b, _ in cells}
    roots = [(P, c) for P, c, _, p in cells if p == -1]
    tally["root branches per file"][len(roots)] += 1
    if roots:
        tally["code of the root branch"][cell_code(roots[0][1])] += 1
    for P, c, _, p in cells:
        if p == -1:
            continue
        if p not in by_id:
            tally["child meets parent"]["parent branch not in the file"] += 1
            continue
        Q = by_id[p][0]
        d = np.linalg.norm(Q - P[0], axis=1)
        j = int(d.argmin())
        where = "at the parent's last point" if j == len(Q) - 1 else \
            "at the parent's first point" if j == 0 else "inside the parent"
        gap = "same point" if d[j] <= SAME else "within 0.5 mm" if d[j] <= 0.5 else \
            "within 1 mm" if d[j] <= 1.0 else "more than 1 mm away"
        tally["child meets parent"][f"{gap}, {where}"] += 1
        if cell_code(by_id[p][1]) == "LM":
            tally["children of an LM-coded branch, by own code"][cell_code(c)] += 1


def locate_o(cells, pid, src, tally):
    """Part 2: where the O of split() lies in the raw left file."""
    tree = tracer_io.tracer_tree(pid, src)
    arts = split(*graph(tree), roots=tracer_io.tracer_ostia(pid, src))
    if "LAD" not in arts or "CX" not in arts:
        tally["O"]["no LAD or no LCx after split"] += 1
        return
    O = arts["LAD"][4][0]
    if np.linalg.norm(arts["CX"][4][0] - O) > SAME:
        tally["O"]["LAD and LCx do not start at the same point (no shared start)"] += 1
        return
    hits = []  # (role of O in the cell, code of the cell)
    for P, c, _, p in cells:
        for i in np.where(np.linalg.norm(P - O, axis=1) <= SAME)[0]:
            role = "first" if i == 0 else "last" if i == len(P) - 1 else "inside"
            hits.append((role, cell_code(c), p == -1, int(c[i])))
    if not hits:
        tally["O"]["not a raw point of the left file"] += 1
        return
    roles = sorted({(r, k) for r, k, _, _ in hits})
    tally["O, as (position in branch, branch code) for every branch holding it"][
        "; ".join(f"{r} of {k}" for r, k in roles)] += 1
    tally["O is the last point of the root branch"]["yes" if any(r == "last" and root for r, _, root, _ in hits)
                                                    else "no"] += 1
    tally["raw code at O"][CODE.get(hits[0][3], "other")] += 1
    near = cKDTree(np.concatenate([P for P, *_ in cells]))
    codes = np.concatenate([c for _, c, *_ in cells])
    for a, name in (("LAD", "LAD"), ("CX", "LCx")):
        d, j = near.query(arts[a][4][1:11])  # the first 5 mm past O
        lm = int(np.sum((codes[j] == 1) & (d <= SAME)))
        tally[f"LM-coded points among the first 10 {name} points past O"][
            "0" if lm == 0 else "1-3" if lm <= 3 else "4-10"] += 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=tracer_io.TRACER_DIR)
    ap.add_argument("--n", type=int, default=None, help="only the first N participants")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "bifurcation_point_probe.md"))
    args = ap.parse_args()

    ids = sorted(tracer_io.tracer_ids(args.src), key=int)[: args.n]
    tally = {k: Counter() for k in (
        "root branches per file", "code of the root branch", "child meets parent",
        "children of an LM-coded branch, by own code", "O",
        "O, as (position in branch, branch code) for every branch holding it",
        "O is the last point of the root branch", "raw code at O",
        "LM-coded points among the first 10 LAD points past O",
        "LM-coded points among the first 10 LCx points past O")}
    failed = 0
    for pid in ids:
        try:
            cells = left_cells(pid, args.src)
            attachments(cells, tally)
            locate_o(cells, pid, args.src, tally)
        except Exception:  # noqa: BLE001 - counted
            failed += 1

    out = io.StringIO()
    print("# Bifurcation point O in the tracer centerlines (bifurcation_point_probe.py)\n", file=out)
    print(f"{count(len(ids))} participants with both pruned BL files, left file; {count(failed)} could not be "
          f"read or divided. Same point = within {SAME} mm. Counts 1-4 hidden.\n", file=out)
    for title, c in tally.items():
        if not c:
            continue
        print(f"## {title}\n\n| | n |\n|---|---|", file=out)
        for k, v in c.most_common():
            print(f"| {k} | {count(v)} |", file=out)
        print(file=out)
    text = out.getvalue()
    Path(args.out).write_text(text, encoding="utf-8")
    print(text)
    print(f"written to {args.out}")


if __name__ == "__main__":
    main()
