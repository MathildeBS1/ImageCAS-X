"""Overlay the tracer and Medis centerlines of the compared artery for the --n artery pairs whose average curvature
differs most (largest |T_tracer - T_medis|, either sign), and below them the pair where the two agree best, as a
reference (server only: the figure shows single participants).

    python CGPS_data/thesis_final/curvature_view.py [--n 6] [--artery LAD|CX|RCA] [--rows DIR]

Reuses medis_compare_arteries.csv that medis_compare.py saved in --rows and chooses among every artery pair with a
value in both trees, as in the curvature comparison (no same-vessel check). Both trees are read again and divided
with split_trunks.split (the tracer from its own ostia), as in medis_compare.tree_features.

Each row: left, the artery of both trees in one projection (the plane through both lines that shows them best),
tracer solid and Medis dashed, with each line's start (circle) and end (square), so a trace that stops early or
follows another vessel shows. Right, the curvature profile of each (curvature_feature.curvature_profile, CHORD mm)
along its own arc length from its own start, and its average over the whole artery (the compared value,
curvature_feature.artery_curvature over 0 to end) as a thin line over the same stretch. The row title gives the
rank, the artery, the two averages and their difference, the two artery lengths and the same-vessel check (reason
and offset; descriptive only).
Figure: curvature_view.png in --rows. The study ids are printed to the terminal with each row's numbers, not in the
figure.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/
sys.path.insert(0, str(Path(__file__).resolve().parent))
from curvature_feature import CHORD, artery_curvature, curvature_profile

NAME = {"LAD": "LAD", "CX": "LCx", "RCA": "RCA"}
STYLE = {"tracer": {"color": "k", "ls": "-"}, "Medis": {"color": "tab:red", "ls": "--"}}


def artery(tree, a, roots=None):
    """(points, arc length, end, average curvature) of artery a of one tree, the value medis_compare compares;
    None when the tree has no such artery."""
    from split_trunks import graph, split

    arts = split(*graph(tree), roots=roots)
    if a not in arts:
        return None
    _, _, end, _, Y, s = arts[a]
    return Y, s, end, artery_curvature(Y, s, (0.0, end), CHORD)[0]


def row(axl, axr, lines):
    """lines: {"tracer": artery(...), "Medis": artery(...)}."""
    pts = np.concatenate([Y[s <= end] for Y, s, end, _ in lines.values()])
    c = pts.mean(axis=0)
    axes = np.linalg.svd(pts - c)[2][:2]
    for m, (Y, s, end, T) in lines.items():
        q = (Y[s <= end] - c) @ axes.T
        axl.plot(q[:, 0], q[:, 1], lw=1.6, label=f"{m}, {end:.0f} mm", **STYLE[m])
        axl.plot(*q[0], marker="o", ms=8, color=STYLE[m]["color"], ls="none")
        axl.plot(*q[-1], marker="s", ms=8, mfc="none", mew=2, color=STYLE[m]["color"], ls="none")
        pos, kappa = curvature_profile(Y, CHORD, s)
        k = pos < end
        axr.plot(pos[k], kappa[k], lw=1.2, label=f"{m}, average {T:.3f}", **STYLE[m])
        axr.plot([0, end], [T, T], lw=0.8, color=STYLE[m]["color"])
    axl.plot([], [], marker="o", color="0.4", ls="none", label="start")
    axl.plot([], [], marker="s", mfc="none", mew=2, color="0.4", ls="none", label="end")
    axl.set_aspect("equal", adjustable="datalim")  # same scale on both axes, the panel keeps its size
    axl.set_xlabel("mm")
    axl.set_ylabel("mm")
    axl.legend(fontsize=7, loc="upper left", bbox_to_anchor=(0, -0.14), ncol=4, frameon=False)
    axr.set_xlabel("arc length from the artery's own start (mm)")
    axr.set_ylabel("curvature (1/mm)")
    axr.legend(fontsize=7, loc="upper left", bbox_to_anchor=(0, -0.14), ncol=2, frameon=False)


def figure(cases, out):
    """cases: [(row title, {"tracer": artery(...), "Medis": artery(...)}), ...], one row each."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(12, 5.6 * len(cases)), layout="constrained")
    for sub, (title, lines) in zip(np.atleast_1d(fig.subfigures(len(cases), 1, hspace=0.06)), cases):
        axl, axr = sub.subplots(1, 2, width_ratios=[1, 1.3])
        row(axl, axr, lines)
        sub.suptitle(title, fontsize=9, x=0.02, ha="left")
    path = out / "curvature_view.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def main():
    import hoe10y_qc as hq
    import tracer_io
    from cgps_stats import OUT_DIR

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=6, help="number of worst cases (largest |curvature difference|)")
    ap.add_argument("--artery", choices=("LAD", "CX", "RCA"), default=None, help="only this artery (default all)")
    ap.add_argument("--rows", default=str(Path(OUT_DIR) / "medis_compare"), help="medis_compare --rows folder")
    ap.add_argument("--src", default=tracer_io.TRACER_DIR)
    args = ap.parse_args()
    rows = Path(args.rows)
    A = pd.read_csv(rows / "medis_compare_arteries.csv", dtype={"id": str})
    if "T_tracer" not in A:
        ap.error("the CSV has no curvature columns: rerun medis_compare.py")
    if "medis_full" in A:  # only where the Medis artery is a reference, the rule of medis_compare
        from medis_compare import reference_rows
        A = reference_rows(A)[0]
    A = A.assign(diff=A["T_tracer"] - A["T_medis"]).dropna(subset=["diff"])
    if args.artery:
        A = A[A["artery"] == args.artery]
    worst = A.loc[A["diff"].abs().sort_values(ascending=False).index[:args.n]]
    picks = [(f"worst {k} of {len(A)}", r) for k, (_, r) in enumerate(worst.iterrows(), 1)]
    picks.append(("closest agreement (reference)", A.loc[A["diff"].abs().idxmin()]))

    medis = {hq.id_from_name(p.name): p for p in tracer_io.MEDIS_TREES.rglob("*.vtk")}
    hq.read_label_codes((f, f) for f in medis.values())  # as in medis_compare, so the Medis labels match
    cases = []
    for label, r in picks:
        pid, a = r["id"], r["artery"]
        lines = {"tracer": artery(tracer_io.tracer_tree(pid, args.src), a, tracer_io.tracer_ostia(pid, args.src)),
                 "Medis": artery(hq.tree_points(medis[pid]), a)}
        (_, _, lt, tt), (_, _, lm, tm) = lines["tracer"], lines["Medis"]
        off = f" ({r['offset']:.1f} mm)" if pd.notna(r.get("offset", np.nan)) else ""
        text = (f"{label}: {NAME[a]}, average curvature tracer {tt:.3f}, Medis {tm:.3f} 1/mm, difference {tt - tm:+.3f}\n"
                f"length tracer {lt:.0f} mm, Medis {lm:.0f} mm; same-vessel check: {r['reason']}{off}")
        cases.append((text, lines))
        print(f"id {pid}: {text.replace(chr(10), '; ')}")
    print(f"-> {figure(cases, rows)}")


if __name__ == "__main__":
    main()
