"""How many scans are left in the clean-baseline cohort (BL ct_cag_sis == 0 and ct_cag_sss == 0).

    python CGPS_data/clean_baseline_count.py [--bl BL_FILE] [--fu FU_FILE]

Uses BL_PATH / FU_PATH from cgps_stats.py unless overridden. Prints aggregate counts only (small
counts suppressed as in cgps_stats.py); nothing is written to disk.

About half of the BL patients have no segment reads but SIS/SSS recorded as 0, so the cohort is
also split by whether any BL segment stenosis was read.
"""
from __future__ import annotations

import argparse

from cgps_stats import BL_PATH, FU_PATH, SEGMENTS, count, load, num


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bl", default=BL_PATH)
    ap.add_argument("--fu", default=FU_PATH)
    args = ap.parse_args()

    bl = load(args.bl)
    sis, sss = num(bl["ct_cag_sis"]), num(bl["ct_cag_sss"])
    seg_cols = [f"ct_cag_{s}_stenosis" for s in SEGMENTS if f"ct_cag_{s}_stenosis" in bl]
    read = bl[seg_cols].notna().any(axis=1)

    clean = (sis == 0) & (sss == 0)
    rows = [
        ("BL patients", len(bl)),
        ("SIS and SSS both recorded", (sis.notna() & sss.notna()).sum()),
        ("clean baseline (SIS == 0 and SSS == 0)", clean.sum()),
        ("  with BL segment reads", (clean & read).sum()),
        ("  without BL segment reads (0 may mean 'not read')", (clean & ~read).sum()),
        ("SIS == 0 but SSS != 0 (inconsistent)", ((sis == 0) & sss.notna() & (sss != 0)).sum()),
        ("SSS == 0 but SIS != 0 (inconsistent)", ((sss == 0) & sis.notna() & (sis != 0)).sum()),
    ]

    if args.fu and args.fu != "/path/to/followup.xlsx":
        fu_ids = set(load(args.fu)["study_id"].dropna())
        in_fu = bl["study_id"].isin(fu_ids)
        rows += [
            ("clean baseline with a FU scan", (clean & in_fu).sum()),
            ("  with BL segment reads and a FU scan", (clean & read & in_fu).sum()),
        ]

    width = max(len(name) for name, _ in rows)
    for name, n in rows:
        print(f"{name:<{width}}  {count(n)}")


if __name__ == "__main__":
    main()
