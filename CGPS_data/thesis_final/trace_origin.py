"""Where do the tracer points of the divided LM, LAD and LCx come from? Tells whether a wrongly labelled
bifurcation is the tracer's own labelling or a result of how tracer_io and split_trunks join the tree.

    python CGPS_data/thesis_final/trace_origin.py --id 1160 [--mm 15]

For one participant: reads the two pruned tracer files as they are (tracer_io.read_side), builds the tree
as medis_compare does (tracer_io.tracer_tree -> split_trunks.graph -> split) and prints
  1. whether graph() joined the left and the right file into one connected piece (bridging),
  2. for the LM (ostium to O) and the first --mm mm of the LAD and LCx: how many points come from the left
     and from the right file, which raw tracer codes they carry, and the largest distance to a raw point,
  3. a reading of 1 and 2.
Codes of the left file: 1 LM, 2 LAD, 3 LCx, 4-8 side branches; right file: 9 RCA, 10 PDA, 11 PLA
(tracer_io.CODES). Server only (reads the tracer files); prints the id given, no other data.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/
sys.path.insert(0, str(Path(__file__).resolve().parent))


def main():
    import tracer_io
    from scipy.sparse.csgraph import connected_components
    from scipy.spatial import cKDTree
    from split_trunks import graph, split, trunk_path

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", required=True, help="study id")
    ap.add_argument("--mm", type=float, default=15.0, help="length of the LAD and LCx to check, from O")
    ap.add_argument("--src", default=tracer_io.TRACER_DIR)
    args = ap.parse_args()

    raw = [(side, P, code) for side, f in zip(tracer_io.SIDES, tracer_io.tracer_files(args.id, args.src))
           for P, code in tracer_io.read_side(f)]
    pts = np.concatenate([P for _, P, _ in raw])
    side = np.concatenate([[s] * len(P) for s, P, _ in raw])
    code = np.concatenate([c for _, _, c in raw])
    near = cKDTree(pts)

    X, lab, G = graph(tracer_io.tracer_tree(args.id, args.src))
    _, comp = connected_components(G, directed=False)
    node_side = side[near.query(X)[1]]
    joined = [k for k in np.unique(comp) if len(set(node_side[comp == k])) > 1]
    print(f"participant {args.id}")
    print(f"1. connected pieces after graph(): {comp.max() + 1}; pieces holding points of both files: "
          f"{len(joined)} ({'left and right tree JOINED by bridging' if joined else 'left and right kept apart'})")

    arteries = split(X, lab, G)
    if "LAD" not in arteries or "CX" not in arteries:
        print("2. no LAD or no LCx after split(): " + ", ".join(sorted(arteries)))
        return
    O = arteries["LAD"][4][0]
    lad_path = X[trunk_path(X, lab, G, "LAD")]
    lm = lad_path[: int(np.argmin(np.linalg.norm(lad_path - O, axis=1))) + 1]
    parts = {"LM": lm}
    for a in ("LAD", "CX"):
        *_, Y, s = arteries[a]
        parts["LCx" if a == "CX" else a] = Y[s <= args.mm]

    print(f"2. origin of the points (LM = ostium to O; LAD and LCx = first {args.mm:g} mm from O):")
    verdict = []
    for name, Y in parts.items():
        if len(Y) == 0:
            print(f"   {name}: no points")
            continue
        d, j = near.query(Y)
        sides = {str(k): int(v) for k, v in zip(*np.unique(side[j], return_counts=True))}
        codes = {int(k): int(v) for k, v in zip(*np.unique(code[j], return_counts=True))}
        print(f"   {name}: {len(Y)} points; file {sides}; raw codes {codes}; largest distance {d.max():.2f} mm")
        expected = {"LM": 1, "LAD": 2, "LCx": 3}[name]
        if sides.get("right"):
            verdict.append(f"{name} runs through points of the RIGHT file: our joining (tracer_io merges the "
                           f"two files, split_trunks.graph bridges gaps up to 3 mm) -> our code")
        elif codes.get(expected, 0) < 0.5 * len(Y):
            verdict.append(f"{name} is mostly left-file points without code {expected}: the path runs through "
                           f"other branches -> check the tracer codes there (tracer) or the path choice (our code)")
    print("3. reading:")
    for v in verdict or ["the LM, LAD and LCx run through left-file points with their own codes (1, 2, 3). If the "
                         "plot still shows right-side vessels, the TRACER labelled them 1, 2, 3 -> tracer"]:
        print("   " + v)


if __name__ == "__main__":
    main()
