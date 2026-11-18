"""Draw the LM bifurcation of the tracer and of Medis side by side, for the participants whose tracer angle is
the widest compared with Medis (server only: the figures show single participants).

    python CGPS_data/thesis_final/bifurcation_view.py [--n 1] [--rows DIR]

Reuses the per-pair CSVs that medis_compare.py saved in --rows (medis_compare_participants.csv and
medis_compare_arteries.csv), so nothing is recomputed for the other participants. Ranks the participants
by theta_tracer - theta_medis (largest first) and, for the first --n, reads both trees again and divides
them with split_trunks.split. Left panel the tracer, right panel Medis, each with: the bifurcation point O,
the LAD and LCx up to ZOOM mm from O, the LM and side branches near O in grey (so a trifurcation or a
misplaced O shows), the points 5 to 10 mm along each daughter (bifurcation_angle.DEPTHS), the fitted line
through them (artery_direction) and the angle between the two lines as an arc.
Both panels use the same projection (the plane through all zoom points that shows them best) and the same
scale, so they can be compared directly; the angle printed in each panel is the 3D angle. The title gives
the alignment check of the LAD and LCx from medis_compare (reason and median offset).
Figures: bifurcation_view_rank<k>.png in --rows. The study id is printed to the terminal, not in the figure.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bifurcation_angle import DEPTHS, artery_direction, lm_angle, point_at_depth

COLOUR = {"LAD": "tab:blue", "CX": "tab:orange"}
ZOOM = 15.0  # mm from O shown in each panel
ARC = 4.0  # mm: radius of the angle arc


def plane(points):
    """Centre and the first two principal axes of the points: the projection used for both panels."""
    c = points.mean(axis=0)
    return c, np.linalg.svd(points - c)[2][:2]


def draw(ax, P, c, axes, **kw):
    q = (np.asarray(P) - c) @ axes.T
    ax.plot(q[:, 0], q[:, 1], **kw)


def bifurcation(arteries):
    """O, and per daughter (Y, s, depth points, fitted direction); None when the LAD or LCx is missing."""
    if "LAD" not in arteries or "CX" not in arteries:
        return None
    out = {}
    for a in ("LAD", "CX"):
        *_, Y, s = arteries[a]
        pts = [point_at_depth(Y, s, d) for d in DEPTHS]
        out[a] = (Y, s, np.array([p for p in pts if p is not None]), artery_direction(Y, s))
    return arteries["LAD"][4][0], out


def figure(row, art_rows, trees, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from split_trunks import graph, split

    split_out = {m: split(*graph(t)) for m, t in trees.items()}
    bif = {m: bifurcation(a) for m, a in split_out.items()}
    zoom = np.concatenate([np.r_[[O], *[d[2] for d in daughters.values()]]
                           for O, daughters in (b for b in bif.values() if b)])
    c, axes = plane(zoom)

    fig, panels = plt.subplots(1, 2, figsize=(11, 5.5), sharex=True, sharey=True)
    for ax, m in zip(panels, ("tracer", "Medis")):
        if not bif[m]:
            ax.set_title(f"{m}: no LAD and LCx")
            continue
        O, daughters = bif[m]
        for P, _ in trees[m]:
            near = np.linalg.norm(P - O, axis=1) <= ZOOM
            if near.sum() > 1:
                draw(ax, P[near], c, axes, color="0.75", lw=1)
        for a, (Y, s, pts, u) in daughters.items():
            name = "LCx" if a == "CX" else a
            draw(ax, Y[s <= ZOOM], c, axes, color=COLOUR[a], lw=1.6, label=name)
            if len(pts):
                draw(ax, pts, c, axes, marker="o", ms=4, color=COLOUR[a], ls="none")
            if u is not None:
                draw(ax, [O, O + 12 * u], c, axes, color=COLOUR[a], lw=3, alpha=0.4)
        draw(ax, [O], c, axes, marker="o", ms=9, color="k", ls="none", label="O")
        ul, uc = daughters["LAD"][3], daughters["CX"][3]
        theta = lm_angle(split_out[m]["LAD"][4:], split_out[m]["CX"][4:])
        if ul is not None and uc is not None:
            w = np.linspace(0, 1, 50)[:, None]
            arc = ul * (1 - w) + uc * w
            draw(ax, O + ARC * arc / np.linalg.norm(arc, axis=1, keepdims=True), c, axes, color="k", lw=1)
        ax.set_title(f"{m}: angle {theta:.0f} deg")
        ax.set_aspect("equal")
        ax.set_xlabel("mm")
        ax.legend(fontsize=8, loc="best")
    panels[0].set_ylabel("mm")

    check = "; ".join(f"{'LCx' if r.artery == 'CX' else r.artery}: {r.reason}"
                      + (f" ({r.offset:.1f} mm)" if pd.notna(getattr(r, "offset", np.nan)) else "")
                      for r in art_rows.itertuples())
    fig.suptitle(f"rank {row.rank} of the widest tracer angles: difference {row.diff:+.0f} deg "
                 f"(tracer - Medis)\nalignment check: {check}", fontsize=9)
    fig.tight_layout()
    path = out / f"bifurcation_view_rank{row.rank}.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def main():
    import hoe10y_qc as hq
    import tracer_io
    from cgps_stats import OUT_DIR

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=1, help="how many of the widest tracer angles to plot")
    ap.add_argument("--rows", default=str(Path(OUT_DIR) / "medis_compare"), help="medis_compare --rows folder")
    ap.add_argument("--src", default=tracer_io.TRACER_DIR)
    args = ap.parse_args()
    rows = Path(args.rows)
    P = pd.read_csv(rows / "medis_compare_participants.csv", dtype={"id": str})
    A = pd.read_csv(rows / "medis_compare_arteries.csv", dtype={"id": str})
    P["diff"] = P["theta_tracer"] - P["theta_medis"]
    top = P.dropna(subset=["diff"]).sort_values("diff", ascending=False).head(args.n)
    top["rank"] = range(1, len(top) + 1)

    medis = {hq.id_from_name(p.name): p for p in tracer_io.MEDIS_TREES.rglob("*.vtk")}
    hq.read_label_codes((f, f) for f in medis.values())  # as in medis_compare, so the Medis labels match
    for row in top.itertuples():
        trees = {"tracer": tracer_io.tracer_tree(row.id, args.src), "Medis": hq.tree_points(medis[row.id])}
        path = figure(row, A[(A["id"] == row.id) & A["artery"].isin(["LAD", "CX"])], trees, rows)
        print(f"rank {row.rank}: id {row.id}, difference {row.diff:+.1f} deg -> {path}")


if __name__ == "__main__":
    main()
