"""Which patients with plaque at BL (visual read) have no Medis centerline tree, and where is their plaque?

    python CGPS_data/medis_missing_plaque.py [--src TREE_FOLDER] [--out MD]

The Medis trees should cover every patient who is not plaque-free at BL. This script counts the BL
patients with plaque (ct_cag_sis > 0 or ct_cag_sss > 0) without a tree, split by ct_cag_visual_read,
and for them reports the number of plaque segments, the worst grade, the segments with plaque
(grade minimal or worse) and the Medis plaque-analysis status columns, next to the same numbers for
the patients with a tree. The no-tree patients whose Medis analysis is marked finished get their own
column, with the plaque type of their plaque segments. Aggregates only (counts 1-4 shown as <5).
"""

import argparse
from pathlib import Path

import pandas as pd

import hoe10y_qc as hq
from cgps_stats import OUT_DIR, SEGMENTS, count, num, yes

RANK = {g: i for i, g in enumerate(hq.GRADES)}
TYPES = tuple(hq.PLAQUE_CODES)
TYPE_OF_CODE = {str(v): k for k, v in hq.PLAQUE_CODES.items()}
TRUNKS = ("plad", "mlad", "dlad", "pcx", "mcx", "dcx", "prca", "mrca", "drca")


def pc(k, n):
    return f"{100 * k / n:.1f}" if n else ""


def plaque_type(raw):
    """Visual plaque-type cell -> one of TYPES, or 'not recorded'."""
    t = hq.label_text(pd.Series([raw])).iloc[0]
    t = TYPE_OF_CODE.get(t.removesuffix(".0"), t)
    return t if t in TYPES else "not recorded"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / "medis_missing_plaque.md"))
    args = ap.parse_args()

    tree_ids = {hq.id_from_name(f.name) for f in Path(args.src).rglob("*.vtk")} - {None}
    bl = hq.load_sheets(hq.ROOT)["BL"]
    bl = bl.assign(id=bl[hq.ID_COL].map(hq.norm_id)).drop_duplicates("id").set_index("id")

    read = yes(bl["ct_cag_visual_read"]) == 1
    sis, sss = num(bl["ct_cag_sis"]), num(bl["ct_cag_sss"])
    plaque = (sis > 0) | (sss > 0)
    tree = bl.index.isin(tree_ids)
    # per-segment grade rank; unevaluable / missing -> NaN
    grade = pd.DataFrame({s: bl[f"ct_cag_{s}_stenosis"].map(hq.grade_of).map(RANK) for s in SEGMENTS
                          if f"ct_cag_{s}_stenosis" in bl})
    seg_plaque = grade >= RANK["minimal"]

    rep = ["# BL patients with plaque but no Medis centerline tree", "",
           "Aggregates only; counts 1-4 shown as <5. Plaque at BL: `ct_cag_sis > 0` or `ct_cag_sss > 0`. "
           "Tree match: number in the tree file name = study_id.", "",
           "| BL status | read | tree | no tree | total |", "|---|---|---|---|---|"]
    for name, m in [("plaque at BL", plaque), ("plaque-free at BL", ~plaque & sis.notna() & sss.notna()),
                    ("SIS/SSS missing", sis.isna() | sss.isna())]:
        for r, rm in [("read", read), ("not read", ~read)]:
            k = m & rm
            rep.append(f"| {name} | {r} | {count((k & tree).sum())} | {count((k & ~tree).sum())} | {count(k.sum())} |")
    rep.append(f"| **all** | | **{count(tree.sum())}** | **{count((~tree).sum())}** | **{count(len(bl))}** |")
    rep.append(f"\nTree IDs not in the BL sheet: {count(len(tree_ids - set(bl.index)))}.")

    finished = pd.concat([num(bl[c]) == 1 for c in bl if c.endswith("_medis_finished")], axis=1).any(axis=1)
    groups = {"plaque, no tree": plaque & ~tree, "no tree, Medis finished": plaque & ~tree & finished,
              "plaque, tree": plaque & tree}
    n = {g: int(m.sum()) for g, m in groups.items()}
    hdr = "| | " + " | ".join(f"{g} n | %" for g in groups) + " |"
    sep = "|---|" + "---|---|" * len(groups)

    def row(label, ks):
        return f"| {label} | " + " | ".join(f"{count(k)} | {pc(k, n[g])}" for g, k in zip(groups, ks)) + " |"

    # agreement of SIS/SSS with the segment grades
    rep += ["", "## Do the segment grades agree with SIS/SSS?", "", hdr, sep,
            row("no segment graded minimal or worse", [int((~seg_plaque[m].any(axis=1)).sum()) for m in groups.values()]),
            row("some segment unevaluable / missing", [int(grade[m].isna().any(axis=1).sum()) for m in groups.values()])]

    nseg = {g: seg_plaque[m].sum(axis=1) for g, m in groups.items()}
    rep += ["", "## Number of segments with plaque per patient", "", hdr, sep]
    for label, lo, hi in [("0", 0, 0), ("1", 1, 1), ("2", 2, 2), ("3-4", 3, 4), ("5+", 5, 99)]:
        rep.append(row(label, [int(nseg[g].between(lo, hi).sum()) for g in groups]))
    rep.append("| median (IQR) | " + " | ".join(
        f"{nseg[g].median():.0f} ({nseg[g].quantile(.25):.0f}-{nseg[g].quantile(.75):.0f}) | " if n[g] >= 10 else " | "
        for g in groups) + " |")

    worst = {g: grade[m].max(axis=1) for g, m in groups.items()}
    rep += ["", "## Worst segment grade", "", hdr, sep]
    for gname in hq.GRADES:
        rep.append(row(gname, [int((worst[g] == RANK[gname]).sum()) for g in groups]))

    rep += ["", "## Segments with plaque (grade minimal or worse)", "",
            "Patients with plaque in each segment; % of the patients in the group. A patient counts once "
            "per segment.", "", hdr, sep]
    for s in grade.columns:
        rep.append(row(s, [int(seg_plaque.loc[m, s].sum()) for m in groups.values()]))
    rep.append(row("any of the 9 trunk segments", [int(seg_plaque.loc[m, list(TRUNKS)].any(axis=1).sum())
                                                   for m in groups.values()]))
    rep.append(row("only LM / side branches", [int((seg_plaque.loc[m].any(axis=1)
                                                    & ~seg_plaque.loc[m, list(TRUNKS)].any(axis=1)).sum())
                                               for m in groups.values()]))
    for v, segs in [("LAD (incl. D1, D2)", ("plad", "mlad", "dlad", "d1", "d2")),
                    ("CX (incl. OM1, OM2)", ("pcx", "mcx", "dcx", "om1", "om2")),
                    ("RCA (incl. PDA, PLA)", ("prca", "mrca", "drca", "pda", "pla"))]:
        rep.append(row(f"any {v}", [int(seg_plaque.loc[m, list(segs)].any(axis=1).sum()) for m in groups.values()]))

    # plaque type of the plaque segments (BL _plaque_type exists only for segments with plaque)
    ptype = pd.DataFrame({s: bl[f"ct_cag_{s}_plaque_type"].map(plaque_type) for s in grade.columns
                          if f"ct_cag_{s}_plaque_type" in bl}).where(seg_plaque)
    tot = {g: int(ptype[m].notna().sum().sum()) for g, m in groups.items()}
    rep += ["", "## Plaque type of the plaque segments", "",
            "Per plaque segment; % of the plaque segments in the group (" + ", ".join(
                f"{g}: {count(tot[g])}" for g in groups) + ").", "",
            "| | " + " | ".join(f"{g} segments | %" for g in groups) + " |", sep]
    for t in TYPES + ("not recorded",):
        ks = [int((ptype[m] == t).sum().sum()) for m in groups.values()]
        rep.append(f"| {t} | " + " | ".join(f"{count(k)} | {pc(k, tot[g])}" for g, k in zip(groups, ks)) + " |")
    nonc = ptype.isin(("mostly_noncalcified", "noncalcified"))
    rep += ["", "Per patient; % of the patients in the group.", "", hdr, sep,
            row("all plaque segments (mostly) calcified", [int((ptype[m].isin(("calcified", "mostly_calcified"))
                                                                 | ptype[m].isna()).all(axis=1).sum()
                                                                - (ptype[m].isna().all(axis=1)).sum())
                                                            for m in groups.values()]),
            row("any (mostly) noncalcified segment", [int(nonc[m].any(axis=1).sum()) for m in groups.values()]),
            row("any segment with no type recorded", [int((ptype[m] == "not recorded").any(axis=1).sum())
                                                      for m in groups.values()])]

    # Medis plaque-analysis status (BL only, filled only for segments with plaque)
    rep += ["", "## Medis plaque-analysis status columns", "",
            "Patients with at least one segment where the column is 1 / is filled at all.", "", hdr, sep]
    for suf in ("medis_egnet", "medis_finished"):
        cols = [f"ct_cag_{s}_{suf}" for s in SEGMENTS if f"ct_cag_{s}_{suf}" in bl]
        vals = bl[cols].apply(num)
        rep.append(row(f"`_{suf}` = 1 in any segment", [int((vals[m] == 1).any(axis=1).sum()) for m in groups.values()]))
        rep.append(row(f"`_{suf}` filled in any segment", [int(vals[m].notna().any(axis=1).sum()) for m in groups.values()]))

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(rep) + "\n", encoding="utf-8")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
