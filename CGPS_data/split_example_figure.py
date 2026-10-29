"""Is the visual-analysis plaque in a split segment with a Medis contour? Two Medis trees side by
side, one where every segment with visual plaque holds a contour and one where one does not
(the figure for medis_contour_coverage.py).

    python CGPS_data/split_example_figure.py [--artery LAD] [--seed 0]
                                             [--good STUDY_ID] [--bad STUDY_ID] [--out DIR]

Top: the split trunk in 3D (LPS mm), coloured by segment, with a grey sleeve where a Medis contour
lies and a red sleeve on a segment with visual plaque but no contour. Bottom: the straightened trunk
with each contour's extent and the BL visual grade per segment.

A segment holds a contour when a contour on the trunk has its largest overlap there (by location, as
in split_check.py). Good = at least two segments with visual plaque, all holding a contour. Poor = a
segment with visual plaque holds no contour, while another contour lies on the trunk (so Medis did
analyse this artery). Without --good / --bad the trees are picked at random (seeded) among the trunks
split from the Medis labels. Runs on dtu-gpu-7 and only draws a figure
there: no coordinates are written, and the IDs are printed to the terminal only, never put in the
image or its file name. The figure still shows two patients' anatomy: check with Kit before it
leaves the server.
"""
import argparse
import random
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

import centerline_qc as cq
import hoe10y_qc as hq
from cgps_stats import OUT_DIR
from split_check import COVERS, OFF_TRUNK, contour_files, contour_points, visual
from split_trunks import ARTERY_OF, NAMES, graph, split

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e4e3df"
COLORS = ("#2a78d6", "#eb6834", "#1baf7a")  # p / m / d, same order as the schematic
MISMATCH = "#e34948"  # segment with visual plaque but no Medis contour
pretty = lambda seg: seg.replace("lad", "LAD").replace("rca", "RCA").replace("cx", "CX")


def example(f, artery, contours_of, bl):
    """Everything to draw one tree, with kind 'good' / 'bad' / None."""
    try:
        X, lab, G = graph(hq.tree_points(f))
        info = {}
        res = split(X, lab, G, info=info)
    except Exception:  # noqa: BLE001 - not an example
        return None
    if artery not in res or info[artery]["source"] != "medis_label":
        return None
    pm, md, end, _, Y, s = res[artery]
    bounds = dict(zip(NAMES[artery], zip((0, pm, md), (pm, md, end))))
    pid = hq.id_from_name(f.name)
    grades = {seg: visual(bl, pid, seg) for seg in NAMES[artery]}
    cons = []
    for name, files in contours_of.items():
        if ARTERY_OF.get(name, "").upper() != artery or not set(COVERS.get(name, ())) & set(NAMES[artery]):
            continue
        try:
            P = contour_points(files)
        except Exception:  # noqa: BLE001 - contour skipped
            continue
        if len(P) < 2 or np.median(cq.nearest(P, Y)[0]) > OFF_TRUNK:
            continue
        lo, hi = np.percentile(s[np.ravel(cq.nearest(P, Y)[1])], [5, 95])
        overlap = {g: max(0.0, min(hi, bh) - max(lo, bl_)) for g, (bl_, bh) in bounds.items()}
        cons.append({"name": name, "extent": (lo, hi), "assigned": max(overlap, key=overlap.get)})
    plaque = [seg for seg, g in grades.items() if g == "plaque"]
    if not cons or not plaque:
        return None
    missed = [seg for seg in plaque if seg not in {c["assigned"] for c in cons}]
    kind = "bad" if missed else "good" if len(plaque) >= 2 else None
    return {"pid": pid, "kind": kind, "X": X, "G": G, "Y": Y, "s": s, "bounds": bounds, "grades": grades,
            "cons": cons, "missed": missed}


def draw_3d(ax, e, artery):
    X, G, Y, s = e["X"], e["G"], e["Y"], e["s"]
    color = dict(zip(NAMES[artery], COLORS))
    c, reach = Y.mean(0), np.ptp(Y, axis=0).max()
    rows, cols = G.nonzero()
    for i, j in zip(rows, cols):  # the rest of the tree around this trunk, faint
        if i < j and np.linalg.norm(X[i] - c) < reach:
            ax.plot(*X[[i, j]].T, color=GRID, lw=1.2)
    for con in e["cons"]:  # sleeve where a Medis contour lies
        lo, hi = con["extent"]
        m = (s >= lo) & (s <= hi)
        ax.plot(*Y[m].T, color=INK2, lw=11, alpha=0.25, solid_capstyle="round")
    for seg in e["missed"]:  # visual plaque, no contour
        lo, hi = e["bounds"][seg]
        m = (s >= lo) & (s <= hi)
        ax.plot(*Y[m].T, color=MISMATCH, lw=11, alpha=0.35, solid_capstyle="round")
    for seg, (lo, hi) in e["bounds"].items():
        m = (s >= lo) & (s <= hi)
        ax.plot(*Y[m].T, color=color[seg], lw=3.5, solid_capstyle="round")
        k = np.argmin(abs(s - (lo + hi) / 2))
        ax.text(*(Y[k] + [0, 0, 6]), pretty(seg), color=INK, fontweight="bold", fontsize=9, ha="center")
    for b in list(e["bounds"].values())[1:]:
        ax.scatter(*Y[np.argmin(abs(s - b[0]))], marker="o", s=30, c=INK, depthshade=False)
    ax.set_box_aspect(np.ptp(Y, axis=0) + 1e-6, zoom=1.35)
    ax.view_init(elev=20, azim=-60)
    ax.set_axis_off()


def draw_straight(ax, e, artery):
    bounds, s = e["bounds"], e["s"]
    end = s[-1] if len(s) else 1
    color = dict(zip(NAMES[artery], COLORS))
    gap = 0.004 * end  # surface gap between neighbouring boxes
    for label, yy in (("split\nsegments", 3), ("Medis\ncontours", 2), ("visual\nanalysis", 1)):
        ax.text(-0.03 * end, yy, label, ha="right", va="center", color=INK2, fontsize=8)
    for seg, (lo, hi) in bounds.items():
        ax.add_patch(FancyBboxPatch((lo + gap, 2.75), max(hi - lo - 2 * gap, 0.1), 0.5,
                                    boxstyle="round,pad=0,rounding_size=0.15", fc=color[seg], ec="none"))
        ax.text((lo + hi) / 2, 3, pretty(seg), ha="center", va="center", color="white", fontweight="bold", fontsize=8)
        g, missed = e["grades"][seg], seg in e["missed"]
        ax.add_patch(FancyBboxPatch((lo + gap, 0.75), max(hi - lo - 2 * gap, 0.1), 0.5,
                                    boxstyle="round,pad=0,rounding_size=0.15",
                                    fc=MISMATCH if missed else INK2 if g == "plaque" else SURF,
                                    ec=MISMATCH if missed else INK2, lw=1))
        ax.text((lo + hi) / 2, 1, "plaque,\nno contour" if missed else g, ha="center", va="center",
                color="white" if g == "plaque" else INK2, fontsize=7.5 if missed else 8)
    for k, con in enumerate(sorted(e["cons"], key=lambda c: c["extent"][0])):
        lo, hi = con["extent"]
        seg = COVERS[con["name"]][0]
        yy = 2 + (0.13 if k % 2 else -0.13)
        ax.plot([lo, hi], [yy, yy], color=color.get(seg, MUTED), lw=6, solid_capstyle="butt")
        ax.text((lo + hi) / 2, yy + 0.17, pretty(con["name"]), ha="center", va="bottom", color=INK, fontsize=7.5)
    for lo, _ in list(bounds.values())[1:]:
        ax.axvline(lo, color=GRID, lw=1, zorder=0)
    cuts = [0] + [lo for lo, _ in list(bounds.values())[1:]] + [end]
    ax.set_xticks(cuts); ax.set_xticklabels([f"{v:.0f}" for v in cuts[:-1]] + [f"{end:.0f} mm"], color=INK2, fontsize=7.5)
    ax.set_xlim(-0.3 * end, 1.03 * end); ax.set_ylim(0.4, 3.6)
    ax.tick_params(length=0); [sp.set_visible(False) for sp in ax.spines.values()]; ax.set_yticks([])


def figure(good, bad, artery, out):
    fig = plt.figure(figsize=(12, 8), facecolor=SURF)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.2, 1], hspace=0.0, wspace=0.08)
    titles = {"good": "Good overlap: every segment with visual plaque\nholds a Medis contour",
              "bad": "Poor overlap: a segment with visual plaque\nholds no Medis contour"}
    for col, (kind, e) in enumerate((("good", good), ("bad", bad))):
        ax = fig.add_subplot(gs[0, col], projection="3d"); ax.set_facecolor(SURF)
        draw_3d(ax, e, artery)
        ax.set_title(f"{'AB'[col]}  {titles[kind]}", loc="left", fontsize=10, fontweight="bold", color=INK)
        ax = fig.add_subplot(gs[1, col]); ax.set_facecolor(SURF)
        draw_straight(ax, e, artery)
    handles = [Line2D([], [], color=INK2, lw=8, alpha=0.25, label="Medis contour"),
               Line2D([], [], color=MISMATCH, lw=8, alpha=0.35, label="visual plaque, no Medis contour"),
               Line2D([], [], ls="", marker="o", ms=5, color=INK, label="split boundary (Medis label change)")]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, fontsize=8.5, bbox_to_anchor=(0.5, 0.0))
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=SURF)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--artery", default="LAD", choices=list(NAMES))
    ap.add_argument("--good", help="study_id of the good example (default: random)")
    ap.add_argument("--bad", help="study_id of the poor example (default: random)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--medis", default=str(Path(hq.ROOT) / hq.MEDIS_DIR))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / "split_example"))
    args = ap.parse_args()
    trees = sorted((Path(args.medis) / "Analysis_Processed" / "centerline_tree").rglob("*.vtk"))
    hq.read_label_codes((f, f) for f in trees)  # names for codes a file leaves unnamed
    by_id = {}
    for (pid, name), files in contour_files(args.medis).items():
        by_id.setdefault(pid, {})[name] = files
    bl = hq.load_sheets(hq.ROOT)["BL"]
    bl = bl.assign(id=bl["study_id"].map(hq.norm_id)).drop_duplicates("id").set_index("id")
    random.Random(args.seed).shuffle(trees)
    wanted = {k: hq.norm_id(v) for k, v in (("good", args.good), ("bad", args.bad)) if v}
    found = {}
    for f in trees:
        pid = hq.id_from_name(f.name)
        kinds = [k for k in ("good", "bad") if k not in found and wanted.get(k) in (None, pid)]
        if not kinds:
            continue
        e = example(f, args.artery, by_id.get(pid, {}), bl)
        if e and e["kind"] in kinds:
            found[e["kind"]] = e
        if len(found) == 2:
            break
    missing = {"good", "bad"} - set(found)
    if missing:
        raise SystemExit(f"no {' / '.join(sorted(missing))} example found for {args.artery}")
    Path(args.out).mkdir(parents=True, exist_ok=True)
    out = Path(args.out) / f"split_example_{args.artery}_seed{args.seed}.png"
    figure(found["good"], found["bad"], args.artery, out)
    print(f"good: tree {found['good']['pid']}, poor: tree {found['bad']['pid']} (keep on the server) -> {out}")


if __name__ == "__main__":
    main()
