"""Read the in-house tracer centerlines (sec:method-tracer) into the tree structure of the Medis trees.

    python CGPS_data/thesis_final/tracer_io.py --labels [--src TRACER_FOLDER] [--n N]   # label map table

    from tracer_io import tracer_tree
    tracer_tree(pid)  # [(points in LPS mm, label per point), ...], as hoe10y_qc.tree_points

Files (tracer_probe.md, 2026-11-18): /data/kimbr/centerlines_for_mathilde/BL_<id>.coronary_{left,right}_
centerline[_ostium_pruned].vtk, legacy VTK 5.1, one LINES cell per branch, step 0.5 mm. The points are in
the LPS mm frame of the Medis trees (bounds agree within about 1 mm), so no mapping is applied. The
_ostium_pruned files are read: the stub the tracer grows into the aorta before the ostium is cut off.
Each point carries an integer code (point data segment_voted). The files hold no lumen (no radius, ring or
contour array), so the daughter asymmetry cannot be computed from them (daughter_ratio.tracer_rings).

The codes are not the SCCT numbers (the right tree carries 9, 10 and 11). CODES maps them, per side, to the
split_trunks names. It was filled on 2026-11-18 from tracer_labels.md (--labels: for each code, the label of
the nearest Medis tree point within 2 mm, over the 600 Medis participants); confirm it with Kit.
  left   1 lm (79% of points nearest Medis LM), 2 lad (87% p/m/dLAD), 3 cx (69% cx/pCx), 4 d1 (76%),
         5 d2 (43%; d1 24%), 6 om1 (44%), 7 om2 (om1 52%: a second obtuse marginal), 8 im (75%)
  right  9 rca (88% p/m/dRCA), 10 pda (72%), 11 pla (81%)
Not mapped (None, unlabelled side branches): left 11 (30 points), 12 (cx 42%, pla 16%, pda 12%; about
40 participants, distal LCx or its posterior branches), 13 (unlabelled 46%), 14 (Medis code 21 51%, d2 13%);
in fewer than five right trees 2 (dlad), 3 and 13. They count as side branches for the landmark rule only by
their length. Codes are mapped per side, so a stray LAD code in a right tree does not become an LAD.
"""
import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/
import centerline_qc as cq
import hoe10y_qc as hq
from cgps_stats import count

TRACER_DIR = "/data/kimbr/centerlines_for_mathilde"
MEDIS_TREES = Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"
PATTERN = "BL_{pid}.coronary_{side}_centerline_ostium_pruned.vtk"
SIDES = ("left", "right")
NEAR = 2.0  # mm: a tracer point takes the label of the nearest Medis point only this close

# Tracer code -> split_trunks name per side (None = not used); from tracer_labels.md, 2026-11-18.
CODES = {
    "left": {1: "lm", 2: "lad", 3: "cx", 4: "d1", 5: "d2", 6: "om1", 7: "om2", 8: "im"},
    "right": {9: "rca", 10: "pda", 11: "pla"},
}


def read_side(path):
    """[(points (n, 3), codes (n,)), ...], one entry per LINES cell (branch) of one tracer file."""
    v = cq.read_vtk_legacy(Path(path).read_bytes())
    P, code = v["points"], np.asarray(v["point_data"]["segment_voted"]).astype(int)
    return [(P[np.asarray(c)], code[np.asarray(c)]) for c in v["cells"].get("LINES", []) if len(c) >= 2]


def tracer_files(pid, src=TRACER_DIR):
    return [Path(src) / PATTERN.format(pid=pid, side=s) for s in SIDES]


def tracer_ids(src=TRACER_DIR):
    """Study ids with both pruned BL files."""
    have = [{hq.id_from_name(p.name.split(".", 1)[0]) for p in Path(src).glob(PATTERN.format(pid="*", side=s))}
            for s in SIDES]
    return have[0] & have[1]


def tracer_tree(pid, src=TRACER_DIR):
    """Both pruned files of one participant in the structure of hoe10y_qc.tree_points."""
    return [(P, [CODES[side].get(int(c)) for c in code])
            for side, f in zip(SIDES, tracer_files(pid, src)) for P, code in read_side(f)]


def label_table(src=TRACER_DIR, medis=MEDIS_TREES, n=None):
    """Per side and tracer code: participants, points, the share of points with a Medis point within NEAR
    mm, and the shares of the nearest Medis labels among those."""
    trees = {hq.id_from_name(p.name): p for p in Path(medis).rglob("*.vtk")}
    hq.read_label_codes((f, f) for f in trees.values())  # names for Medis codes a file leaves unnamed
    ids = sorted(tracer_ids(src) & set(trees), key=int)[:n]
    people, points, near, lab = Counter(), Counter(), Counter(), defaultdict(Counter)
    failed = 0
    for pid in ids:
        try:
            medis = hq.tree_points(trees[pid])
            M = np.concatenate([p for p, _ in medis])
            ml = np.array([l or "unlabelled" for _, ls in medis for l in ls], dtype=object)
            seen = set()
            for side, f in zip(SIDES, tracer_files(pid, src)):
                for P, code in read_side(f):
                    d, j = cq.nearest(P, M)
                    for c, dist, k in zip(code, np.ravel(d), np.ravel(j)):
                        key = (side, int(c))
                        seen.add(key)
                        points[key] += 1
                        if dist <= NEAR:
                            near[key] += 1
                            lab[key][ml[k]] += 1
            for key in seen:
                people[key] += 1
        except Exception:  # noqa: BLE001 - counted
            failed += 1
    L = ["# Tracer label codes against the nearest Medis label (tracer_io.py --labels)\n",
         (f"{count(len(ids))} participants with a Medis tree and both pruned tracer files; "
          f"{count(failed)} could not be read. A tracer point takes the label of the nearest Medis tree point "
          f"if it lies within {NEAR:g} mm. Shares of points; counts of participants 1-4 hidden.\n"),
         "| side | code | participants | points | within 2 mm | nearest Medis labels (share of those within 2 mm) |",
         "|---|---|---|---|---|---|"]
    for side, c in sorted(people, key=lambda k: (k[0], k[1])):
        key = (side, c)
        tot = sum(lab[key].values())
        top = ", ".join(f"{l} {100 * v / tot:.0f}%" for l, v in lab[key].most_common(5)) if tot else "-"
        L.append(f"| {side} | {c} | {count(people[key])} | {points[key]} | "
                 f"{100 * near[key] / points[key]:.0f}% | {top} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--labels", action="store_true", help="write the code table tracer_labels.md")
    ap.add_argument("--src", default=TRACER_DIR)
    ap.add_argument("--n", type=int, default=None, help="only the first N participants")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "tracer_labels.md"))
    args = ap.parse_args()
    if not args.labels:
        ap.print_help()
        return
    text = label_table(args.src, n=args.n)
    Path(args.out).write_text(text, encoding="utf-8")
    print(text)
    print(f"written to {args.out}")


if __name__ == "__main__":
    main()
