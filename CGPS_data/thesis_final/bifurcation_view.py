"""Draw the LM bifurcation of the tracer and of Medis side by side for two participants: the one whose tracer
angle is the widest compared with Medis, and the one where the two angles agree best (server only: the
figure shows single participants).

    python CGPS_data/thesis_final/bifurcation_view.py [--all] [--rows DIR]

Reuses the per-pair CSVs that medis_compare.py saved in --rows (medis_compare_participants.csv and
medis_compare_arteries.csv), so nothing is recomputed for the other participants. Only participants whose
LAD and LCx both passed the alignment check are chosen (column aligned), as in the angle comparison;
--all chooses among every participant. Row 1: the largest theta_tracer - theta_medis. Row 2: the smallest
|theta_tracer - theta_medis|. Both trees are read again and divided with split_trunks.split.

Each row has the tracer left and Medis right, with: the LM from the ostium to the bifurcation point O
(green), O, the LAD and LCx up to ZOOM mm from O, the side branches near O in grey (so a trifurcation or a
misplaced O shows), the points 5 to 10 mm along each daughter (bifurcation_angle.DEPTHS), the fitted line
through them (artery_direction) and the angle between the two lines as an arc. The two panels of a row use
the same projection (the plane through that participant's zoom points that shows them best) and the same
scale; the angle printed in each panel is the 3D angle. Each row title gives the difference and the
alignment check of the LAD and LCx (reason and median offset).
Figure: bifurcation_view.png in --rows. The study ids are printed to the terminal, not in the figure.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bifurcation_angle import DEPTHS, artery_direction, lm_angle, point_at_depth

COLOUR = {"LM": "tab:green", "LAD": "tab:blue", "CX": "tab:orange"}
ZOOM = 15.0  # mm from O shown in each panel
ARC = 4.0  # mm: radius of the angle arc


def plane(points):
    """Centre and the first two principal axes of the points: the projection of one row."""
    c = points.mean(axis=0)
    return c, np.linalg.svd(points - c)[2][:2]


def draw(ax, P, c, axes, **kw):
    q = (np.asarray(P) - c) @ axes.T
    ax.plot(q[:, 0], q[:, 1], **kw)


def bifurcation(tree):
    """{"O", "LM", "LAD", "CX", "theta"} of one tree; LAD and LCx as (Y, s, depth points, fitted direction).
    None when the LAD or LCx is missing."""
    from split_trunks import graph, shared_prefix, split, trunk_path

    X, lab, G = graph(tree)
    arteries = split(X, lab, G)
    if "LAD" not in arteries or "CX" not in arteries:
        return None
    pl, pc = trunk_path(X, lab, G, "LAD"), trunk_path(X, lab, G, "CX")
    out = {"O": arteries["LAD"][4][0], "LM": X[pl[:shared_prefix(pl, pc)]],
           "theta": lm_angle(arteries["LAD"][4:], arteries["CX"][4:])}
    for a in ("LAD", "CX"):
        *_, Y, s = arteries[a]
        pts = [point_at_depth(Y, s, d) for d in DEPTHS]
        out[a] = (Y, s, np.array([p for p in pts if p is not None]), artery_direction(Y, s))
    return out


def panel(ax, m, b, tree, c, axes):
    if b is None:
        ax.set_title(f"{m}: no LAD and LCx")
        return
    O = b["O"]
    for P, _ in tree:
        near = np.linalg.norm(P - O, axis=1) <= ZOOM
        if near.sum() > 1:
            draw(ax, P[near], c, axes, color="0.75", lw=1)
    if len(b["LM"]) > 1:
        draw(ax, b["LM"], c, axes, color=COLOUR["LM"], lw=1.8, label="LM")
    for a in ("LAD", "CX"):
        Y, s, pts, u = b[a]
        draw(ax, Y[s <= ZOOM], c, axes, color=COLOUR[a], lw=1.6, label="LCx" if a == "CX" else a)
        if len(pts):
            draw(ax, pts, c, axes, marker="o", ms=4, color=COLOUR[a], ls="none")
        if u is not None:
            draw(ax, [O, O + 12 * u], c, axes, color=COLOUR[a], lw=3, alpha=0.4)
    draw(ax, [O], c, axes, marker="o", ms=9, color="k", ls="none", label="O")
    ul, uc = b["LAD"][3], b["CX"][3]
    if ul is not None and uc is not None:
        w = np.linspace(0, 1, 50)[:, None]
        arc = ul * (1 - w) + uc * w
        draw(ax, O + ARC * arc / np.linalg.norm(arc, axis=1, keepdims=True), c, axes, color="k", lw=1)
    ax.set_title(f"{m}: angle {b['theta']:.0f} deg", fontsize=10)
    ax.set_aspect("equal")
    ax.legend(fontsize=7, loc="best")


def figure(cases, out):
    """cases: [(row title, trees {"tracer": tree, "Medis": tree}, alignment text), ...], one row each."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, grid = plt.subplots(len(cases), 2, figsize=(11, 5.2 * len(cases)), squeeze=False)
    for row, (title, trees, check) in zip(grid, cases):
        bif = {m: bifurcation(t) for m, t in trees.items()}
        zoom = np.concatenate([np.r_[[b["O"]], b["LAD"][2], b["CX"][2]] for b in bif.values() if b])
        c, axes = plane(zoom)
        for ax, m in zip(row, ("tracer", "Medis")):
            panel(ax, m, bif[m], trees[m], c, axes)
            ax.set_xlabel("mm")
        row[0].set_ylabel("mm")
        lim = [(min(a.get_xlim()[0] for a in row), max(a.get_xlim()[1] for a in row)),
               (min(a.get_ylim()[0] for a in row), max(a.get_ylim()[1] for a in row))]
        for ax in row:
            ax.set_xlim(lim[0])
            ax.set_ylim(lim[1])
        row[0].annotate(f"{title}\nalignment check: {check}", xy=(0, 1.12), xycoords="axes fraction",
                        fontsize=9, va="bottom")
    fig.tight_layout()
    path = out / "bifurcation_view.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def alignment(A, pid):
    rows = A[(A["id"] == pid) & A["artery"].isin(["LAD", "CX"])]
    return "; ".join(f"{'LCx' if r.artery == 'CX' else r.artery}: {r.reason}"
                     + (f" ({r.offset:.1f} mm)" if pd.notna(getattr(r, "offset", np.nan)) else "")
                     for r in rows.itertuples())


def main():
    import hoe10y_qc as hq
    import tracer_io
    from cgps_stats import OUT_DIR

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true", help="choose among all participants, not only aligned ones")
    ap.add_argument("--rows", default=str(Path(OUT_DIR) / "medis_compare"), help="medis_compare --rows folder")
    ap.add_argument("--src", default=tracer_io.TRACER_DIR)
    args = ap.parse_args()
    rows = Path(args.rows)
    P = pd.read_csv(rows / "medis_compare_participants.csv", dtype={"id": str})
    A = pd.read_csv(rows / "medis_compare_arteries.csv", dtype={"id": str})
    if not args.all:
        if "aligned" not in P:
            ap.error("the CSV has no column aligned: rerun medis_compare.py, or use --all")
        P = P[P["aligned"]]
    P = P.assign(diff=P["theta_tracer"] - P["theta_medis"]).dropna(subset=["diff"])
    wide = P.loc[P["diff"].idxmax()]
    close = P.loc[P["diff"].abs().idxmin()]

    medis = {hq.id_from_name(p.name): p for p in tracer_io.MEDIS_TREES.rglob("*.vtk")}
    hq.read_label_codes((f, f) for f in medis.values())  # as in medis_compare, so the Medis labels match
    cases = []
    for label, r in (("largest difference, tracer wider", wide), ("close agreement", close)):
        trees = {"tracer": tracer_io.tracer_tree(r["id"], args.src), "Medis": hq.tree_points(medis[r["id"]])}
        cases.append((f"{label}: tracer - Medis = {r['diff']:+.0f} deg", trees, alignment(A, r["id"])))
        print(f"{label}: id {r['id']}, difference {r['diff']:+.1f} deg")
    print(f"-> {figure(cases, rows)}")


if __name__ == "__main__":
    main()
