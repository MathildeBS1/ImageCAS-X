"""How many scans are left in the clean-baseline cohort (BL ct_cag_sis == 0 and ct_cag_sss == 0).

    python CGPS_data/clean_baseline_count.py [--bl BL_FILE] [--fu FU_FILE] [--out FILE]

Uses BL_PATH / FU_PATH from cgps_stats.py (Kit's BL_anonymised.xlsx / FU_anonymised.xlsx) unless
overridden. Aggregate counts only (small counts suppressed as in cgps_stats.py), printed and written
as a markdown table to OUT_FILE (copy it to CGPS_data/clean_baseline.md, like report.md and
plaque_location.md).

SSS is the current ct_cag_sss of the new spreadsheets (not ct_cag_sss_old); the old one is only
compared. In the new BL file unread segments are filled with "none" (ct_cag_na_to_none_n), so a
scan counts as read from ct_cag_visual_read; read_at_bl() falls back to "any segment stenosis
recorded" for the old tables without that column. The cohort is split by it.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from cgps_stats import BL_PATH, FU_PATH, OUT_DIR, SEGMENTS, count, load, num, yes

OUT_FILE = str(Path(OUT_DIR) / "clean_baseline.md")


def read_at_bl(bl):
    """True where a reader visually read the BL scan."""
    if "ct_cag_visual_read" in bl:
        return yes(bl["ct_cag_visual_read"]) == 1
    seg_cols = [f"ct_cag_{s}_stenosis" for s in SEGMENTS if f"ct_cag_{s}_stenosis" in bl]
    return bl[seg_cols].notna().any(axis=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bl", default=BL_PATH)
    ap.add_argument("--fu", default=FU_PATH)
    ap.add_argument("--out", default=OUT_FILE, help="markdown file for the counts")
    args = ap.parse_args()

    bl = load(args.bl)
    sis, sss = num(bl["ct_cag_sis"]), num(bl["ct_cag_sss"])
    read = read_at_bl(bl)

    clean = (sis == 0) & (sss == 0)
    rows = [
        ("BL patients", len(bl)),
        ("BL scan visually read" + ("" if "ct_cag_visual_read" in bl else " (any segment read)"), read.sum()),
        ("SIS and SSS both recorded", (sis.notna() & sss.notna()).sum()),
        ("clean baseline (SIS == 0 and SSS == 0)", clean.sum()),
        ("  read at BL", (clean & read).sum()),
        ("  not read at BL (0 may mean 'not read')", (clean & ~read).sum()),
        ("SIS == 0 but SSS != 0 (inconsistent)", ((sis == 0) & sss.notna() & (sss != 0)).sum()),
        ("SSS == 0 but SIS != 0 (inconsistent)", ((sss == 0) & sis.notna() & (sis != 0)).sum()),
    ]
    if "ct_cag_na_to_none_n" in bl:
        filled = num(bl["ct_cag_na_to_none_n"]) > 0
        rows += [("clean, read, with segments filled NA -> none", (clean & read & filled).sum())]
    if "ct_cag_sss_old" in bl:
        sss_old = num(bl["ct_cag_sss_old"])
        clean_old = (sis == 0) & (sss_old == 0)
        rows += [
            ("clean with ct_cag_sss_old instead", clean_old.sum()),
            ("  clean with new SSS only", (clean & ~clean_old).sum()),
            ("  clean with old SSS only", (clean_old & ~clean).sum()),
        ]

    if args.fu:
        fu_ids = set(load(args.fu)["study_id"].dropna())
        in_fu = bl["study_id"].isin(fu_ids)
        rows += [
            ("clean baseline with a FU scan", (clean & in_fu).sum()),
            ("  read at BL and a FU scan", (clean & read & in_fu).sum()),
        ]

    lines = ["# Clean-baseline cohort (BL ct_cag_sis == 0 and ct_cag_sss == 0)", "",
             "Aggregates only; small counts suppressed as in cgps_stats.py. SSS is the new ct_cag_sss; "
             "read at BL = ct_cag_visual_read.", "", "|  | patients |", "|---|---|"]
    lines += [f"| {name.strip() if not name.startswith('  ') else '&nbsp;&nbsp;' + name.strip()} | {count(n)} |"
              for name, n in rows]
    text = "\n".join(lines) + "\n"
    print(text)
    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
