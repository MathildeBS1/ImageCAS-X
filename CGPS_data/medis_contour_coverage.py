"""How much of the visual-analysis plaque has a Medis contour?

    python CGPS_data/medis_contour_coverage.py [--medis MEDIS_FOLDER] [--out MD]

Medis drew contours on segments with and without visual plaque, but mostly on plaque. This counts
the other direction: of the BL segments the visual analysis grades minimal or worse, the share that
has a Medis contour,
- by name: a BL contour named after the segment (a Medis LCx contour counts for mcx and dcx, a
  whole-LAD / whole-RCA contour for its three trunk segments). All 17 segments, in (a) the 600
  patients with a Medis tree and (b) all patients with at least one BL contour.
- by location: a contour that split_check.py puts mostly in the split trunk segment (9 trunk
  segments of the trees that split).
Each split by segment and by visual grade. Aggregates only (counts 1-4 hidden); writes
medis_contour_coverage.md.
"""
import argparse
from collections import defaultdict
from pathlib import Path

import pandas as pd

import hoe10y_qc as hq
from cgps_stats import OUT_DIR, count, count_of, pct
from split_check import COVERS, ORDER, build, contour_files
from split_trunks import table

PLAQUE = ("minimal", "mild", "moderate", "severe", "occlusion")
GRADE_GROUPS = {"minimal": ("minimal",), "mild": ("mild",), "moderate or worse": ("moderate", "severe", "occlusion")}


def plaque_segments(bl, ids, names_of):
    """One row per patient and BL segment with visual plaque, flagged by a contour of that name."""
    rows = []
    for pid in ids:
        if pid not in bl.index:
            continue
        covered = {s for n in names_of.get(pid, ()) for s in COVERS.get(n, (n,))}
        for seg in hq.SEGMENTS:
            col = f"ct_cag_{seg}_stenosis"
            g = hq.grade_of(bl.at[pid, col]) if col in bl else "missing"
            if g in PLAQUE:
                rows.append({"id": pid, "segment": seg, "grade": g, "contour": seg in covered})
    return pd.DataFrame(rows, columns=["id", "segment", "grade", "contour"])


def coverage(df, col="contour"):
    k, n = int(df[col].sum()), len(df)
    return count(n), count_of(k, n) if n else "", "" if pct(k, n) is None else pct(k, n)


def summary(df, col, segments):
    head = ["", "visual plaque segments", "with a contour", "%"]
    rows = [("all", *coverage(df, col))]
    rows += [(g, *coverage(df[df["grade"].isin(gs)], col)) for g, gs in GRADE_GROUPS.items()]
    rows += [(s, *coverage(df[df["segment"] == s], col)) for s in segments if (df["segment"] == s).any()]
    return table(head, rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--medis", default=str(Path(hq.ROOT) / hq.MEDIS_DIR))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / "medis_contour_coverage.md"))
    args = ap.parse_args()
    trees = sorted((Path(args.medis) / "Analysis_Processed" / "centerline_tree").rglob("*.vtk"))
    hq.read_label_codes((f, f) for f in trees)
    contours = contour_files(args.medis)
    bl = hq.load_sheets(hq.ROOT)["BL"]
    bl = bl.assign(id=bl["study_id"].map(hq.norm_id)).drop_duplicates("id").set_index("id")

    names_of = defaultdict(set)
    for pid, name in contours:
        names_of[pid].add(name)
    unmapped = sorted({n for ns in names_of.values() for n in ns if n not in COVERS and n not in hq.SEGMENTS})
    tree_ids = sorted({hq.id_from_name(f.name) for f in trees})
    contour_ids = sorted(names_of)

    L = ["# Visual-analysis plaque with a Medis contour (medis_contour_coverage.py)\n",
         "Aggregates only; counts 1-4 shown as <5, percentages hidden where they would reveal them. "
         "Visual plaque = BL stenosis grade minimal or worse.\n",
         f"Trees: {count(len(tree_ids))}; patients with a BL contour: {count(len(contour_ids))}; "
         f"tree patients with a BL contour: {count(len(set(tree_ids) & set(contour_ids)))}.\n"]
    if unmapped:
        L.append(f"Contour names not matched to a segment (not counted): {', '.join(unmapped)}.\n")
    for ids, title in ((tree_ids, "patients with a Medis tree"), (contour_ids, "patients with any BL contour")):
        df = plaque_segments(bl, ids, names_of)
        L += [f"## By name, {title}\n", summary(df, "contour", hq.SEGMENTS)]

    _, seg = build(trees, contours, bl)
    if len(seg):
        seg = seg[seg["visual"] == "plaque"].copy()
        seg["grade"] = [hq.grade_of(bl.at[p, f"ct_cag_{s}_stenosis"]) for p, s in zip(seg["id"], seg["segment"])]
        seg["either"] = seg["by_location"] | seg["by_name"]
        L += ["## By location, split trunk segments of the trees\n",
              "Contour by location = a Medis contour whose largest overlap is this split segment.\n",
              summary(seg, "by_location", ORDER),
              "By location or by name:\n", summary(seg, "either", ORDER)]
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(L), encoding="utf-8")
    print(f"{len(tree_ids)} trees, {len(contour_ids)} patients with contours -> {args.out}")


if __name__ == "__main__":
    main()
