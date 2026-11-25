"""The steps from a delivered Medis tree to the compared artery, for the Medis arteries that pass the full-artery rule
(split_trunks.full_artery) but are the shortest, beside one long reference (server only: the figure shows single
participants).

    python weekly/week12/centerline_steps_view.py [--n 4] [--artery RCA] [--rows DIR]

For the week 12 report only; copy the PNG to weekly/week12/week12_figures/.

Reuses medis_compare_arteries.csv that medis_compare.py saved in --rows. Picks the --n shortest Medis arteries
(L_medis) with medis_full true, and the longest one as a reference. The full-artery rule alone is applied here, not
the minimum length of medis_compare.reference_rows, to show what the rule lets through.

Each row, one projection for all four panels (the plane that shows the Medis tree best), drawn with the code that
medis_compare runs (split_trunks.graph, trunk_path, split, full_artery):
  1. the tree as delivered: every polyline, coloured by its segment label (this artery's proximal, mid and distal
     segments in three colours, other labels grey, unlabelled points light);
  2. the graph: the piece of the tree that holds most of this artery's labels, the other pieces faded, the joins
     the graph adds between polylines (ends within 1 mm, gaps up to BRIDGE mm) in green, the chosen start (circle)
     and the far end of the path (square);
  3. the path from start to far end, coloured by the label of each node, with the sequence of this artery's labels
     along it and the full-artery verdict;
  4. the compared artery of Medis (red, dashed) over the tracer artery (black), with both lengths.
Figure: centerline_steps_view.png in --rows. Study ids are printed to the terminal, not in the figure.
"""
import argparse
import sys
from itertools import groupby
from pathlib import Path

import numpy as np
import pandas as pd

CGPS = Path(__file__).resolve().parents[2] / "CGPS_data"
sys.path.insert(0, str(CGPS))  # the shared modules in CGPS_data/
sys.path.insert(0, str(CGPS / "thesis_final"))

NAME = {"LAD": "LAD", "CX": "LCx", "RCA": "RCA"}
PART_COL = ("tab:blue", "tab:orange", "tab:purple")  # proximal, mid, distal


def steps(tree, artery):
    """Everything the four panels draw, from the code medis_compare runs on a Medis tree."""
    from scipy.sparse.csgraph import connected_components
    from split_trunks import ARTERY_OF, NAMES, full_artery, graph, split, trunk_path

    X, lab, G = graph(tree)
    own = {v for v in NAMES[artery]} | ({"cx"} if artery == "CX" else set())
    _, comp = connected_components(G, directed=False)
    nodes = [i for i, l in enumerate(lab) if ARTERY_OF.get(l) == artery.lower()]
    main = np.bincount(comp[nodes]).argmax() if nodes else -1
    # the joins graph() added: edges between nodes that are not neighbours on one delivered polyline
    P = np.concatenate([p for p, _ in tree])
    _, node = np.unique(np.round(P, 2), axis=0, return_inverse=True)
    node = node.ravel()
    starts = np.cumsum([0] + [len(p) for p, _ in tree])
    line_edges = {tuple(sorted(e)) for a, b in zip(starts[:-1], starts[1:])
                  for e in zip(node[a:b - 1], node[a + 1:b]) if e[0] != e[1]}
    Gc = G.tocoo()
    joins = {tuple(sorted(e)) for e in zip(Gc.row, Gc.col) if e[0] != e[1]} - line_edges
    path = trunk_path(X, lab, G, artery)
    info = {}
    arts = split(X, lab, G, info)
    full = full_artery(artery, info[artery]["path_labels"]) if artery in arts else (False, "not divided")
    seq = [k for k, _ in groupby(l for l in info.get(artery, {}).get("path_labels", []) if l in own)]
    return {"tree": tree, "X": X, "lab": lab, "comp": comp, "main": main, "joins": joins, "path": path,
            "artery": arts.get(artery), "full": full, "seq": seq, "own": own, "names": NAMES[artery]}


def colour(l, names):
    return PART_COL[names.index(l)] if l in names else ("0.75" if l is not None else "0.9")


def row(axes, st, trc, proj):
    """axes: four axes; st: steps(); trc: (points, arc length) of the tracer artery or None; proj: 3D -> 2D."""
    X, lab, names = st["X"], st["lab"], st["names"]
    a1, a2, a3, a4 = axes
    for p, ls in st["tree"]:  # 1. as delivered
        q = proj(p)
        for k in range(len(q) - 1):
            a1.plot(q[k:k + 2, 0], q[k:k + 2, 1], color=colour(ls[k], names), lw=1.4)
    for c in np.unique(st["comp"]):  # 2. graph pieces, joins, start and far end
        k = st["comp"] == c
        a2.plot(*proj(X[k]).T, ".", ms=1.5, color="0.2" if c == st["main"] else "0.85")
    for i, j in st["joins"]:
        a2.plot(*proj(X[[i, j]]).T, color="tab:green", lw=2.2)
    if st["path"]:
        a2.plot(*proj(X[st["path"][0]]), "o", ms=8, color="k")
        a2.plot(*proj(X[st["path"][-1]]), "s", ms=8, mfc="none", mew=2, color="k")
        q = proj(X[st["path"]])  # 3. the path, coloured by label
        for k in range(len(q) - 1):
            a3.plot(q[k:k + 2, 0], q[k:k + 2, 1], color=colour(lab[st["path"][k]], names), lw=2.0)
        a3.plot(*q[0], "o", ms=8, color="k")
        a3.plot(*q[-1], "s", ms=8, mfc="none", mew=2, color="k")
    a3.set_title(" > ".join(st["seq"]) + f"\nfull: {st['full'][0]} ({st['full'][1]})", fontsize=8)
    if st["artery"] is not None:  # 4. the compared arteries
        Y, s = st["artery"][4], st["artery"][5]
        a4.plot(*proj(Y).T, "--", color="tab:red", lw=1.6, label=f"Medis, {s[-1]:.0f} mm")
    if trc is not None:
        a4.plot(*proj(trc[0]).T, color="k", lw=1.4, label=f"tracer, {trc[1][-1]:.0f} mm")
    a4.legend(fontsize=7, loc="upper left", bbox_to_anchor=(0, -0.04), ncol=2, frameon=False)
    for ax, t in zip(axes, ("as delivered (label colours)", "graph: main piece, joins (green),\nstart (circle), far end (square)",
                            None, "compared artery")):
        if t:
            ax.set_title(t, fontsize=8)
        ax.set_aspect("equal", adjustable="datalim")
        ax.set_xticks([]); ax.set_yticks([])


def figure(cases, artery, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    fig = plt.figure(figsize=(14, 4.2 * len(cases)), layout="constrained")
    for sub, (title, st, trc) in zip(np.atleast_1d(fig.subfigures(len(cases), 1, hspace=0.04)), cases):
        axes = sub.subplots(1, 4)
        pts = np.concatenate([p for p, _ in st["tree"]] + ([trc[0]] if trc is not None else []))
        c = pts.mean(axis=0)
        basis = np.linalg.svd(np.concatenate([p for p, _ in st["tree"]]) - c)[2][:2]
        row(axes, st, trc, lambda Q: (np.asarray(Q) - c) @ basis.T)
        sub.suptitle(title, fontsize=9, x=0.01, ha="left")
    fig.legend([Line2D([], [], color=c, lw=2) for c in PART_COL + ("0.75", "0.9")],
               [f"proximal {NAME[artery]}", f"mid {NAME[artery]}", f"distal {NAME[artery]}", "other label", "no label"],
               loc="outside lower center", ncol=5, fontsize=8, frameon=False)
    path = out / "centerline_steps_view.png"
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def main():
    import hoe10y_qc as hq
    import tracer_io
    from cgps_stats import OUT_DIR
    from split_trunks import graph, split

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=4, help="number of the shortest full Medis arteries")
    ap.add_argument("--artery", choices=("LAD", "CX", "RCA"), default="RCA")
    ap.add_argument("--rows", default=str(Path(OUT_DIR) / "medis_compare"), help="medis_compare --rows folder")
    ap.add_argument("--src", default=tracer_io.TRACER_DIR)
    args = ap.parse_args()
    rows = Path(args.rows)
    A = pd.read_csv(rows / "medis_compare_arteries.csv", dtype={"id": str})
    if "medis_full" not in A:
        ap.error("the CSV has no medis_full column: rerun medis_compare.py")
    A = A[(A["artery"] == args.artery) & A["medis_full"].astype(bool) & A["L_medis"].notna()]
    A = A.sort_values("L_medis")
    picks = [(f"shortest {k} of {len(A)} full Medis {NAME[args.artery]}s", r) for k, (_, r) in enumerate(A.head(args.n).iterrows(), 1)]
    picks.append((f"longest full Medis {NAME[args.artery]} (reference)", A.iloc[-1]))

    medis = {hq.id_from_name(p.name): p for p in tracer_io.MEDIS_TREES.rglob("*.vtk")}
    hq.read_label_codes((f, f) for f in medis.values())  # as in medis_compare, so the Medis labels match
    cases = []
    for label, r in picks:
        pid = r["id"]
        st = steps(hq.tree_points(medis[pid]), args.artery)
        arts = split(*graph(tracer_io.tracer_tree(pid, args.src)), roots=tracer_io.tracer_ostia(pid, args.src))
        trc = (arts[args.artery][4], arts[args.artery][5]) if args.artery in arts else None
        text = f"{label}: Medis {r['L_medis']:.0f} mm, tracer {r['L_tracer']:.0f} mm"
        cases.append((text, st, trc))
        print(f"id {pid}: {text}; labels along the path: {' > '.join(st['seq'])}; full: {st['full']}")
    print(f"-> {figure(cases, args.artery, rows)}")


if __name__ == "__main__":
    main()
