"""Match the Medis centerline trees to the visual reads and count the outcome groups.

    python CGPS_data/medis_match.py [--src TREE_FOLDER] [--out MD]

The number in a tree's file name is the study_id. Matched patients are split by baseline status:
- plaque-free at BL (ct_cag_sis == 0 and ct_cag_sss == 0): new plaque at FU (any grade, SIS or SSS > 0)
  or never plaque;
- plaque at BL: progressed (any segment a higher grade at FU than at BL) or stayed / regressed.
Patients without FU values are counted separately. Aggregates only (counts 1-4 shown as <5).
"""

import argparse
from collections import Counter
from pathlib import Path

import pandas as pd

import hoe10y_qc as hq
from cgps_stats import OUT_DIR, SEGMENTS, count, num, yes

RANK = {g: i for i, g in enumerate(hq.GRADES)}


def progressed(b, f):
    """Any segment read at both visits with a higher grade at FU."""
    for s in SEGMENTS:
        c = f"ct_cag_{s}_stenosis"
        if c in b and c in f:
            gb, gf = hq.grade_of(b[c]), hq.grade_of(f[c])
            if gb in RANK and gf in RANK and RANK[gf] > RANK[gb]:
                return True
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / "medis_match.md"))
    args = ap.parse_args()

    files = sorted(Path(args.src).rglob("*.vtk"))
    per_id = Counter(hq.id_from_name(f.name) for f in files)
    no_id = per_id.pop(None, 0)

    sheets = hq.load_sheets(hq.ROOT)
    bl, fu = (sheets[v].assign(id=sheets[v][hq.ID_COL].map(hq.norm_id)).drop_duplicates("id").set_index("id")
              for v in ("BL", "FU"))
    matched = [i for i in per_id if i in bl.index]

    groups = Counter()
    for i in matched:
        b = bl.loc[i]
        read = "read" if yes(pd.Series([b.get("ct_cag_visual_read")])).iloc[0] == 1 else "not read"
        sis_b, sss_b = num(pd.Series([b["ct_cag_sis"], b["ct_cag_sss"]]))
        f = fu.loc[i] if i in fu.index else None
        sis_f, sss_f = num(pd.Series([f["ct_cag_sis"], f["ct_cag_sss"]])) if f is not None else (None, None)
        if pd.isna(sis_b) or pd.isna(sss_b):
            g = ("BL status unknown", "")
        elif sis_b == 0 and sss_b == 0:
            if f is None or pd.isna(sis_f) or pd.isna(sss_f):
                g = ("plaque-free at BL", "no FU values")
            else:
                g = ("plaque-free at BL", "new plaque at FU" if sis_f > 0 or sss_f > 0 else "never plaque")
        else:
            if f is None:
                g = ("plaque at BL", "no FU values")
            else:
                g = ("plaque at BL", "progressed" if progressed(b, f) else "stayed / regressed")
        groups[(*g, read)] += 1

    rep = ["# Medis centerline trees matched to the visual reads", "",
           "Aggregates only; counts 1-4 shown as <5. Match: number in the tree file name = study_id.", "",
           "| | n |", "|---|---|",
           f"| tree files | {count(len(files))} |",
           f"| files without a number in the name | {count(no_id)} |",
           f"| distinct IDs | {count(len(per_id))} |",
           f"| IDs with more than one tree | {count(sum(n > 1 for n in per_id.values()))} |",
           f"| **IDs matched to the BL sheet** | **{count(len(matched))}** |",
           f"| IDs not in the BL sheet | {count(len(per_id) - len(matched))} |",
           f"| matched IDs also in the FU sheet | {count(sum(i in fu.index for i in matched))} |", "",
           "Outcome groups of the matched patients, split by `ct_cag_visual_read` (unread BL segments are "
           "filled with 'none', so unread scans look plaque-free).", "",
           "| BL status | outcome | read | not read | total |", "|---|---|---|---|---|"]
    for bs, oc in sorted({k[:2] for k in groups}):
        r, nr = groups[(bs, oc, "read")], groups[(bs, oc, "not read")]
        rep.append(f"| {bs} | {oc} | {count(r)} | {count(nr)} | {count(r + nr)} |")
    for bs in sorted({k[0] for k in groups}):
        rep.append(f"| **{bs}** | all | | | **{count(sum(n for k, n in groups.items() if k[0] == bs))}** |")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(rep) + "\n", encoding="utf-8")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
