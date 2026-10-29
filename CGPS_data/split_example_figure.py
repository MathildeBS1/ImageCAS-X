"""Real-data version of the split-check schematic: one Medis tree, its split trunk and the Medis
contour rings on top, plus the straightened trunk with contour extents and visual grades.

    python CGPS_data/split_example_figure.py [--artery LAD] [--id STUDY_ID] [--seed 0] [--out DIR]

Without --id a tree is picked at random (seeded) among those whose artery is split from the Medis
labels and has contours of at least two trunk segments on the trunk. Runs on dtu-gpu-7 and only
draws a figure there: no coordinates are written, and the ID is printed to the terminal only, never
put in the image or its file name. The figure still shows one patient's anatomy: check with Kit
before it leaves the server.
"""
import argparse
import random
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

import centerline_qc as cq
import hoe10y_qc as hq
from cgps_stats import OUT_DIR
from split_check import COVERS, OFF_TRUNK, contour_files, contour_points, visual
from split_trunks import ARTERY_OF, NAMES, graph, split

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e4e3df"
COLORS = ("#2a78d6", "#eb6834", "#1baf7a")  # p / m / d, same order as the schematic
BURDEN = 40.0  # % plaque burden (1 - lumen / outer-wall area) from which a Medis ring is drawn as plaque


def plaque_rings(files):
    """Centre and plaque burden (%) of each lumen ring, from its nearest outer-wall ring."""
    cl = cq.read_vtk_legacy(files["centerline"].read_bytes())["points"] if "centerline" in files else None
    if not {"lumen", "outer"} <= set(files):
        return np.zeros((0, 3)), np.zeros(0)
    lum, out = ([hq.ring_geom(r) for r in hq.read_rings(files[k], cl)[0] if len(r) >= 3] for k in ("lumen", "outer"))
    if not lum or not out:
        return np.zeros((0, 3)), np.zeros(0)
    C, O = np.array([g["c"] for g in lum]), np.array([g["c"] for g in out])
    k = np.ravel(cq.nearest(C, O)[1])
    burden = np.array([100 * (1 - g["area"] / out[j]["area"]) if out[j]["area"] > 0 else np.nan
                       for g, j in zip(lum, k)])
    return C, burden


def candidate(f, artery, contours_of):
    """(tree, split result, {contour name: files}) if the tree qualifies, else None."""
    try:
        X, lab, G = graph(hq.tree_points(f))
        info = {}
        res = split(X, lab, G, info=info)
    except Exception:  # noqa: BLE001 - not a candidate
        return None
    if artery not in res or info[artery]["source"] != "medis_label":
        return None
    Y = res[artery][4]
    on = {}
    for name, files in contours_of.items():
        if ARTERY_OF.get(name, "").upper() != artery or not set(COVERS.get(name, ())) & set(NAMES[artery]):
            continue
        try:
            P = contour_points(files)
        except Exception:  # noqa: BLE001 - contour skipped
            continue
        if len(P) >= 2 and np.median(cq.nearest(P, Y)[0]) <= OFF_TRUNK:
            on[name] = files
    return ((X, lab, G), res[artery], on) if len(on) >= 2 else None


def draw(tree, cut, contours, grades, artery, out, burden=BURDEN):
    X, lab, G = tree
    pm, md, end, rule, Y, s = cut
    bounds = dict(zip(NAMES[artery], zip((0, pm, md), (pm, md, end))))
    color = dict(zip(NAMES[artery], COLORS))
    c = Y.mean(0)
    _, _, Vt = np.linalg.svd(Y - c, full_matrices=False)
    to2d = lambda P: (np.asarray(P) - c) @ Vt[:2].T  # best-fit plane of the trunk

    fig = plt.figure(figsize=(9, 7), facecolor=SURF)
    gs = fig.add_gridspec(2, 1, height_ratios=[1.3, 1], hspace=0.15)
    ax = fig.add_subplot(gs[0]); ax.set_facecolor(SURF)
    rows, cols = G.nonzero()
    near = np.linalg.norm(X - c, axis=1) < np.ptp(Y, axis=0).max()  # the tree around this trunk
    for i, j in zip(rows, cols):
        if i < j and near[i]:
            a, b = to2d(X[[i, j]])
            ax.plot([a[0], b[0]], [a[1], b[1]], color=GRID, lw=1.5, zorder=1)
    T = to2d(Y)
    for seg, (lo, hi) in bounds.items():
        m = (s >= lo) & (s <= hi)
        ax.plot(T[m, 0], T[m, 1], color=color[seg], lw=3.5, solid_capstyle="round", zorder=2)
        k = np.argmin(abs(s - (lo + hi) / 2))
        ax.annotate(seg.replace("lad", "LAD").replace("rca", "RCA").replace("cx", "CX"), T[k],
                    xytext=(0, 12), textcoords="offset points", ha="center", fontweight="bold", color=INK)
    for b in (pm, md):
        k = np.argmin(abs(s - b))
        ax.plot(*T[k], marker="|", ms=18, mew=1.8, color=INK, zorder=3)
    extents, plaque_at = {}, {}
    for name, files in contours.items():
        P = contour_points(files)
        extents[name] = np.percentile(s[np.ravel(cq.nearest(P, Y)[1])], [5, 95])
        C, b = plaque_rings(files)
        j = np.ravel(cq.nearest(C, Y)[1])[b >= burden] if len(C) else np.zeros(0, int)
        plaque_at[name] = s[j]
        ax.plot(T[j, 0], T[j, 1], "o", ms=7, mfc="none", mec=INK, mew=1, zorder=4)  # snapped onto the trunk
    ax.plot([], [], "o", ms=7, mfc="none", mec=INK, label=f"Medis ring with plaque burden $\\geq$ {burden:.0f} %")
    ax.legend(loc="upper right", frameon=False, fontsize=8)
    ax.set_title(f"A  Real Medis tree: {artery} split where its labels change; plaque from the Medis contours",
                 loc="left", fontsize=10, fontweight="bold", color=INK)
    ax.set_aspect("equal"); ax.axis("off")

    ax = fig.add_subplot(gs[1]); ax.set_facecolor(SURF)
    for label, yy in (("split segments", 3), ("Medis contours\n(ring centres projected)", 2),
                      ("visual analysis\n(BL grade)", 1)):
        ax.text(-0.03 * end, yy, label, ha="right", va="center", color=INK2, fontsize=8.5)
    for seg, (lo, hi) in bounds.items():
        name = seg.replace("lad", "LAD").replace("rca", "RCA").replace("cx", "CX")
        ax.add_patch(FancyBboxPatch((lo, 2.75), max(hi - lo, 0.1), 0.5, boxstyle="round,pad=0,rounding_size=0.15",
                                    fc=color[seg], ec=SURF, lw=2))
        ax.text((lo + hi) / 2, 3, name, ha="center", va="center", color="white", fontweight="bold", fontsize=8.5)
        g = grades[seg]
        gap = 0.004 * end  # surface gap between neighbouring boxes
        ax.add_patch(FancyBboxPatch((lo + gap, 0.75), max(hi - lo - 2 * gap, 0.1), 0.5, boxstyle="round,pad=0,rounding_size=0.15",
                                    fc=INK2 if g == "plaque" else SURF, ec=INK2, lw=1))
        ax.text((lo + hi) / 2, 1, g, ha="center", va="center", color="white" if g == "plaque" else INK2, fontsize=8.5)
    for k, (name, (lo, hi)) in enumerate(sorted(extents.items(), key=lambda kv: kv[1][0])):
        seg = COVERS[name][0] if name in COVERS else NAMES[artery][1]
        yy = 2 + (0.12 if k % 2 else -0.12)
        ax.plot([lo, hi], [yy, yy], color=color.get(seg, MUTED), lw=6, solid_capstyle="butt")
        ax.text((lo + hi) / 2, yy + 0.18, f"{name.replace('lad', 'LAD').replace('rca', 'RCA').replace('cx', 'CX')} contour",
                ha="center", va="bottom", color=INK, fontsize=8)
        ax.plot(plaque_at[name], np.full(len(plaque_at[name]), yy), "o", ms=5, mfc=SURF, mec=INK, mew=0.8, zorder=3)
    for b in (pm, md):
        ax.axvline(b, color=GRID, lw=1, zorder=0)
    ax.set_xlim(-0.35 * end, 1.05 * end); ax.set_ylim(0.4, 3.6)
    ax.set_xticks([0, pm, md, end]); ax.set_xticklabels([f"{v:.0f}" for v in (0, pm, md)] + [f"{end:.0f} mm"],
                                                           color=INK2, fontsize=8)
    ax.tick_params(length=0); [sp.set_visible(False) for sp in ax.spines.values()]; ax.set_yticks([])
    ax.set_title("B  Straightened trunk: where each contour falls, and the visual grade of each segment",
                 loc="left", fontsize=10, fontweight="bold", color=INK)
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=SURF)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--artery", default="LAD", choices=list(NAMES))
    ap.add_argument("--id", help="study_id of the tree to draw (default: random qualifying tree)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--burden", type=float, default=BURDEN, help="plaque burden (%%) from which a ring counts as plaque")
    ap.add_argument("--medis", default=str(Path(hq.ROOT) / hq.MEDIS_DIR))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / "split_example"))
    args = ap.parse_args()
    trees = sorted((Path(args.medis) / "Analysis_Processed" / "centerline_tree").rglob("*.vtk"))
    hq.read_label_codes((f, f) for f in trees)  # names for codes a file leaves unnamed
    contours = contour_files(args.medis)
    by_id = {}
    for (pid, name), files in contours.items():
        by_id.setdefault(pid, {})[name] = files
    if args.id:
        trees = [f for f in trees if hq.id_from_name(f.name) == hq.norm_id(args.id)]
    else:
        random.Random(args.seed).shuffle(trees)
    for f in trees:
        pid = hq.id_from_name(f.name)
        got = candidate(f, args.artery, by_id.get(pid, {}))
        if got:
            break
    else:
        raise SystemExit("no qualifying tree (artery split from Medis labels with >= 2 trunk contours)")
    bl = hq.load_sheets(hq.ROOT)["BL"]
    bl = bl.assign(id=bl["study_id"].map(hq.norm_id)).drop_duplicates("id").set_index("id")
    grades = {seg: visual(bl, pid, seg) for seg in NAMES[args.artery]}
    Path(args.out).mkdir(parents=True, exist_ok=True)
    out = Path(args.out) / f"split_example_{args.artery}_seed{args.seed}.png"
    draw(*got, grades, args.artery, out, args.burden)
    print(f"tree {pid} (keep on the server) -> {out}")


if __name__ == "__main__":
    main()
