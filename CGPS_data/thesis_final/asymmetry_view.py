"""Draw the lumen cross-sections behind the daughter asymmetry, tracer and Medis side by side, for the --n
participants whose asymmetry differs most (largest |a_tracer - a_medis|) and, below them, the one where the
two agree best (server only: the figure shows single participants).

    python CGPS_data/thesis_final/asymmetry_view.py [--n 6] [--rows DIR]

Reuses the participants CSV of medis_compare.py (--rows) and chooses among the participants whose asymmetry
was compared (asym_reason ok). Both trees and both lumen surfaces are read again and divided as in
medis_compare.py (split_trunks.split; the tracer's lumen_surface_ostium_pruned.vtk, the Medis lumen meshes of
the left tree merged), and the cross-sections are those of daughter_ratio.section, so the figure shows exactly
what was measured.

Each row has three panels. Tracer and Medis: the lumen surface near O (grey points: the mesh vertices within
ZOOM mm of O), the LM, the LAD and the LCx centerlines, O, and the cross-section loop at each of the 11 depths
(5 to 10 mm from that tree's own O) in the daughter's colour; a depth without a cross-section is a red x. Both
panels use the same projection (the plane through that participant's O and depth points that shows them best)
and the same scale; a loop perpendicular to the vessel shows as a rung across it. Third panel: the diameter
at each depth, tracer solid and Medis dashed, LAD blue and LCx orange, with each daughter's median (the D of
the asymmetry). Each row title gives a = ln(D_LCx / D_LAD) for both trees, the difference and abs(a).
Figure: asymmetry_view.png in --rows. The study ids are printed to the terminal, not in the figure.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bifurcation_view import COLOUR, ZOOM, bifurcation, draw, plane
from daughter_ratio import SECTION_DEPTHS, contour_diameter, merge, section, surface

MAX_VERTICES = 6000  # surface vertices drawn per panel (a random subset when more lie within ZOOM)


def sections(surf, b):
    """{artery: [(loop or None, p), ...] at SECTION_DEPTHS} of one tree's bifurcation b (bifurcation_view)."""
    out = {}
    for a, other in (("LAD", "CX"), ("CX", "LAD")):
        Y, s, *_ = b[a]
        out[a] = [section(*surf, Y, s, b[other][0], d)[:2] for d in SECTION_DEPTHS]
    return out


def panel(ax, name, b, surf, secs, c, axes, rng):
    O = b["O"]
    V = surf[0][np.linalg.norm(surf[0] - O, axis=1) <= ZOOM]
    if len(V) > MAX_VERTICES:
        V = V[rng.choice(len(V), MAX_VERTICES, replace=False)]
    if len(V):
        draw(ax, V, c, axes, marker=".", ms=1, color="0.6", alpha=0.25, ls="none")
    if len(b["LM"]) > 1:
        draw(ax, b["LM"], c, axes, color=COLOUR["LM"], lw=1.5, label="LM")
    for a in ("LAD", "CX"):
        Y, s, *_ = b[a]
        draw(ax, Y[s <= ZOOM], c, axes, color=COLOUR[a], lw=1.2, label="LCx" if a == "CX" else a)
        for loop, p in secs[a]:
            if loop is not None:
                draw(ax, np.r_[loop, loop[:1]], c, axes, color=COLOUR[a], lw=0.9)
            elif p is not None:
                draw(ax, [p], c, axes, marker="x", ms=6, mew=1.5, color="red", ls="none")
    draw(ax, [O], c, axes, marker="o", ms=7, color="k", ls="none", label="O")
    ax.set_title(name, fontsize=10)
    ax.set_aspect("equal")
    ax.set_xlabel("mm")
    ax.legend(fontsize=7, loc="best")


def profile(ax, secs):
    """Diameter at each depth, both trees, with each daughter's median."""
    for name, ls, mk in (("tracer", "-", "o"), ("Medis", "--", "s")):
        for a in ("LAD", "CX"):
            D = np.array([np.nan if lp is None else contour_diameter(lp) for lp, _ in secs[name][a]])
            lab = f"{name} {'LCx' if a == 'CX' else a}"
            ax.plot(SECTION_DEPTHS, D, ls=ls, marker=mk, ms=3, color=COLOUR[a], label=lab)
            if np.isfinite(D).all():
                ax.axhline(np.median(D), ls=ls, lw=0.6, color=COLOUR[a], alpha=0.6)
    ax.set_xlabel("depth from O (mm)")
    ax.set_ylabel("lumen diameter (mm)")
    ax.set_title("diameter per cut (lines: medians)", fontsize=10)
    ax.legend(fontsize=7, loc="best")


def figure(cases, out):
    """cases: [(row title, {"tracer": (bifurcation, surface), "Medis": (...)}), ...], one row each."""
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib.figure import Figure

    rng = np.random.default_rng(0)
    fig = Figure(figsize=(16, 5.6 * len(cases)))
    grid = fig.subplots(len(cases), 3, squeeze=False)
    for row, (title, trees) in zip(grid, cases):
        secs = {m: sections(surf, b) for m, (b, surf) in trees.items()}
        pts = [p for m in secs for a in secs[m] for _, p in secs[m][a] if p is not None]
        c, axes = plane(np.r_[[b["O"] for b, _ in trees.values()], pts])
        for ax, m in zip(row[:2], ("tracer", "Medis")):
            panel(ax, m, *trees[m], secs[m], c, axes, rng)
        row[0].set_ylabel("mm")
        lim = [(min(a.get_xlim()[0] for a in row[:2]), max(a.get_xlim()[1] for a in row[:2])),
               (min(a.get_ylim()[0] for a in row[:2]), max(a.get_ylim()[1] for a in row[:2]))]
        for ax in row[:2]:
            ax.set_xlim(lim[0])
            ax.set_ylim(lim[1])
        profile(row[2], secs)
        row[0].annotate(title, xy=(0, 1.1), xycoords="axes fraction", fontsize=9, va="bottom")
    fig.tight_layout()
    path = out / "asymmetry_view.png"
    fig.savefig(path, dpi=130)
    return path


def main():
    import hoe10y_qc as hq
    import tracer_io
    from cgps_stats import OUT_DIR
    from medis_compare import medis_lumen_files

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=6, help="number of worst cases (largest |asymmetry difference|)")
    ap.add_argument("--rows", default=str(Path(OUT_DIR) / "medis_compare"), help="medis_compare --rows folder")
    ap.add_argument("--src", default=tracer_io.TRACER_DIR)
    ap.add_argument("--lumen", default=tracer_io.LUMEN_DIR)
    ap.add_argument("--medis", default=None, help="Medis contour folder (default <ROOT>/<MEDIS_DIR>)")
    args = ap.parse_args()
    rows = Path(args.rows)
    P = pd.read_csv(rows / "medis_compare_participants.csv", dtype={"id": str})
    if "asym_reason" not in P:
        ap.error("the CSV has no asymmetry columns: rerun medis_compare.py")
    P = P[P["asym_reason"] == "ok"]
    P = P.assign(diff=P["asym_tracer"] - P["asym_medis"])
    worst = P.loc[P["diff"].abs().sort_values(ascending=False).index[:args.n]]
    picks = [(f"worst {k} of {len(P)}", r) for k, (_, r) in enumerate(worst.iterrows(), 1)]
    picks.append(("closest agreement (reference)", P.loc[P["diff"].abs().idxmin()]))

    medis = {hq.id_from_name(p.name): p for p in tracer_io.MEDIS_TREES.rglob("*.vtk")}
    hq.read_label_codes((f, f) for f in medis.values())  # as in medis_compare, so the Medis labels match
    lumen = medis_lumen_files(args.medis)
    cases = []
    for label, r in picks:
        pid = r["id"]
        trees = {"tracer": (bifurcation(tracer_io.tracer_tree(pid, args.src), tracer_io.tracer_ostia(pid, args.src)),
                            surface(tracer_io.tracer_lumen(pid, args.lumen))),
                 "Medis": (bifurcation(hq.tree_points(medis[pid])), merge([surface(f) for f in lumen[pid]]))}
        text = (f"{label}: a tracer {r['asym_tracer']:+.2f}, Medis {r['asym_medis']:+.2f}, difference {r['diff']:+.2f}; "
                f"abs(a) {abs(r['asym_tracer']):.2f} / {abs(r['asym_medis']):.2f}\n"
                f"D LAD {r['D_LAD_tracer']:.2f} / {r['D_LAD_medis']:.2f} mm, "
                f"D LCx {r['D_CX_tracer']:.2f} / {r['D_CX_medis']:.2f} mm (tracer / Medis)")
        cases.append((text, trees))
        print(f"id {pid}: {text.replace(chr(10), '; ')}")
    print(f"-> {figure(cases, rows)}")


if __name__ == "__main__":
    main()
