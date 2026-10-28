# Selecting usable centerline trees: audit of report_qc.md and a per-artery selection script

Sources used throughout. Local files are cited by absolute path:
- QC report: [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md). It was generated on the secure machine from `/data/kimbr/centerlines_hø_10Y.zip` and copied to the laptop.
- The script that generated it: [centerline_qc.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_qc.py). It was found with `grep -rl "Centerline quality report" --include='*.py'`, which matched only this file. Its `write_report()` (lines 1259-1378) emits exactly the section headings in report_qc.md.
- New script: [centerline_selection.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_selection.py). It was written for this task and verified on synthetic data (see Q3).
- Style reference: [cgps_stats.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/cgps_stats.py).
- Repository code on the ImageCAS-X data: [tortuosity/vessels.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/tortuosity/vessels.py), [tortuosity/taper.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/tortuosity/taper.py) and [bifurcation/radius.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/bifurcation/radius.py).
- Headers: [header_BL.xlsx](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/header_BL.xlsx) and [header_FU.xlsx](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/header_FU.xlsx). Their columns were read directly.
- Background: [Centerline labelling plan review.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/reports/Centerline%20labelling%20plan%20review.md). It concerns the ImageCAS-X labelling pipeline, a different dataset; only its radius findings carry over.

## Which concrete criteria and thresholds make a centerline tree usable for LM, LAD, CX, RCA trunk geometry, and how many cases pass per artery?

### Takeaway
Grade each artery separately, on the ostium-to-distal path rather than on summed label lengths. Strict means:
- every trunk segment is on the path, each at least 5 mm;
- the labels run in proximal-to-distal order;
- at most 1 mm of foreign label and at most a 2 mm unlabelled stretch lie on the path;
- there is no jump longer than 1.5 mm;
- the trunk is at least 70/40/70 mm long (LAD/CX/RCA);
- LM is at least 2 mm and the ostium is a free end;
- there is no fragment, cycle or left/right mixing.

Acceptable drops the distal segment and the LM requirement, and loosens the length minimum to 40/30/40 mm.

The QC numbers give only **upper bounds**. The path-based checks are new, so the exact counts come from running the script:

| Artery | Strict at most | Strict + acceptable at most | Excluded at least |
|---|---|---|---|
| LM | 682 | 684 | 60 |
| LAD | 576 | 678 | 66 |
| CX | 581 | 599 | 145 |
| RCA | 553 | 567 | 177 |

**There is no radius in the files**, so the taper T needs a lumen radius measured on the CT.

### Cited Findings

**(a) What report_qc.md shows, section by section**

- **Header.** 744 cases were found (744 expected), 744 read and 744 analysed, with 0 read errors. Settings: JOIN_TOL 1.0 mm, DEDUP_TOL 0.01 mm, gap > max(3.0 mm, 5.0× median spacing). Numeric labels were read as **raw**, not as SCCT codes, because codes above 18 occur (`decide_numbering` picks "scct" only if every code is ≤ 18) — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md); [centerline_qc.py L730-736](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_qc.py)
- **How the files were read.**
  - All files are legacy VTK 5.1 BINARY POLYDATA with LINES.
  - Point arrays are only `segment_label` (used as the label) and `branch`. There are no cell arrays and no radius array.
  - The field data hold a string array `segment_names` such as `"1:pRCA","5:LM",...,"24:unlabelled"`.
  - The 8 most common `segment_names` sets cover 26+19+15+12+9+8+7+7 = 103 files. The full list therefore varies a lot between files.
  - 7 files *name* only `1:pRCA` and `24:unlabelled`, and 15 name only RCA codes (1, 2, 3, 4, 16, 24).
  - Sources: [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md), "How the files were read".
- **Label codes.** Codes 1-17, 18-22, 24 and 28 occur.
  - **Named codes:** 1 pRCA, 2 mRCA, 3 dRCA, 4 R-PDA, 5 LM, 6 pLAD, 7 mLAD, 8 dLAD, 9 D1, 10 D2, 11 pCx, 12 OM1, 13 LCx, 14 L-PLB, 15 L-PDA, 16 R-PLB, 17 RI (54 files) / AL (4 files), 24 unlabelled.
  - **Codes no file names:** 18 (375 files, 15,017 pts), 19 (161; 5,948), 20 (55; 1,813), 21 (210; 11,557), 22 (238; 21,316) and 28 (184; 25,300).
  - **Files use codes they do not name.** For example, code 1 is used in 732 files but not named in 490 of them, and code 13 is used in 599 but not named in 424. Codes 14 and 15 are always named when used (0 files not naming them).
  - Code 24 (unlabelled) is in 736 files with 226,145 points.
  - Source: [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md), "Label codes".
- **Label values.**
  - Code 13 "LCx" is mapped to the unsplit `CX` (29,715 + 24,242 points), so there is no mCX/dCX split.
  - Codes 14 L-PLB and 16 R-PLB both map to `PLA`, and codes 4 R-PDA and 15 L-PDA both map to `PDA`. Left and right posterior branches are therefore pooled in all QC tables.
  - `17:AL` is not recognised and becomes `?AL` (434 points). An unnamed 17 becomes IM.
  - Source: [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md), "Label values"; [centerline_qc.py ALIASES L99-124](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_qc.py)
- **Overview per case.**
  - Total length: median 685.4 mm (p5 320.2, p95 1054.2; min 36.6, max 3645.7).
  - Unlabelled: median 17.2 % (p95 45.6 %, max 100 %); 21.3 % of all length; 736 of 744 cases have some.
  - Topology: polylines median 15 (max 165); branch points median 12 (max 160); max degree 3-4.
  - Components: median 3 (range 1-6). Tiny components (< 10 mm): mean 0.4.
  - **n_gaps = 0 in every case** and **n_joins = 0 (max 1)**. Connectivity therefore comes from shared points in the file.
  - Overlap: median 16.8 mm (max 224.4).
  - Spacing: **median 0.5 mm in every case** (max spacing ≤ 0.8 mm), so the curves have been resampled.
  - Extents: about 110 × 93 × 89 mm, so the units are mm.
  - **median_radius: n = 0, so no radius array exists.**
  - Source: [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md), "Overview per case".
- **Components.** Counts are 1 component: 9 cases, 2: 339, 3: 244, 4: 118, 5: 28, 6: 6. Among complete-trunk cases with pieces < 10 mm ignored, 226 have 2 components, 114 have 3, 24 have 4 and 2 have 5 — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)
- **Segments: presence and length.** Lengths are the sum of every point with the label, so side twigs are included.

  | Segment | Cases (%) | Median mm (p5-p95, or IQR where stated) |
  |---|---|---|
  | LM | 684 (91.9 %) | 12.3 (5.7-20.9; max 48.3) |
  | pLAD | 699 | 21.7 (7.7-43.2) |
  | mLAD | 682 | 30.5; **IQR 30.0-30.9** (p5 14.6) |
  | dLAD | 600 (80.6 %) | 82.5 (18.2-128.6) |
  | pCX | 707 | 26.4 (12.5-52.6) |
  | CX (13) | 599 (80.5 %) | 37.2 (9.7-101.4) |
  | pRCA | 732 (98.4 %) | 40.0 (22.3-64.0) |
  | mRCA | 569 (76.5 %) | 38.3; IQR 34.4-43.0 |
  | dRCA | 556 (74.7 %) | 38.1; IQR 34.2-42.8 |

  - PDA has a maximum of 971.1 mm.
  - Whole arteries present: LM 684, LAD 702, CX 707, RCA 735.
  - Source: [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md), "Segments".
- **Complete main trunks** (all segments present, each joined to the previous one):

  | Trunk | Complete cases |
  |---|---|
  | LM+LAD (LM, pLAD, mLAD, dLAD) | 576 (77.4 %) |
  | LM+CX (LM, pCx, LCx) | 581 (78.1 %) |
  | RCA (pRCA, mRCA, dRCA) | 553 (74.3 %) |
  | RCA without dRCA | 567 (76.2 %) |
  | All three | 366 (49.2 %) |
  | All three, RCA without dRCA | 373 (50.1 %) |

  Source: [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md), "Complete main trunks".
- **Expected connections.** Each entry is joined cases of cases with both segments.
  - pLAD-LM 684/684 direct; pCX-LM 682/682 direct.
  - mLAD-pLAD 678/679 direct (1 missing); dLAD-mLAD 590/591 (1 missing).
  - mRCA-pRCA 566 direct + 1 via unlabelled of 567; dRCA-mRCA 555/555.
  - CX-(LM/pCX) 599/599.
  - D2: 3 missing. PDA: 9 via unlabelled, 3 missing. PLA: 6 via unlabelled.
  - Source: [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md), "Expected connections".
- **Unexpected contacts**, in number of cases:
  - Unnamed codes: #22-CX 216, #18-mLAD 193, #18-pLAD 162, #28-pCX 151, #21-dLAD 140, #19-mLAD 98, #21-mLAD 69, #19-dLAD 45, #28-CX 36, #20-dLAD 35, #22-pCX 20, #18-dLAD 20, #20-mLAD 19, #19-pLAD 14, #28-mRCA 1.
  - Named segments: **dLAD-pLAD 9** (mLAD skipped), **mLAD-pCX 3** (LAD/CX label crossing), ?AL-pLAD 3, ?AL-pCX 1, D2-IM 1, among others.
  - Source: [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)
- **Red flags.** 45 of 744 cases have no flag.

  | Flag | Cases |
  |---|---|
  | unknown_labels | 546 |
  | >2_components | 396 |
  | unlabelled>20% | 287 |
  | no_LM | 60 |
  | no_LAD | 42 |
  | no_CX | 37 |
  | no_RCA | 9 |
  | disconnected_segment | 8 |
  | segment<2mm | 3 |
  | total_length_odd | 2 |

  These flags never fired: left_and_right_in_one_tree, left_right_labels_joined, impossible_contact, gaps_in_polyline and overlapping_polylines. **The section also lists up to 40 case IDs per flag** — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)

**(b) What centerline_qc.py does, and its thresholds**

- **Constants:** EXPECTED_CASES = 744, DEDUP_TOL = 0.01 mm, JOIN_TOL = 1.0 mm, GAP_FACTOR = 5, GAP_MIN = 3 mm, OVERLAP_TOL = 0.5 mm, SHORT_SEGMENT = 2 mm, LABEL_NUMBERING "auto", CODE_NAMES = {}, COMPLETE_RCA_NEEDS_DRCA = True — [centerline_qc.py L62-77](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_qc.py)
- **Reading.**
  - `Source` reads the zip in place, including nested zips.
  - `group_cases` makes one case per file (`<id>_centerline.vtk`) and skips the `.log`.
  - `parse_vtk_legacy` is its own reader for ASCII or binary VTK 4.x/5.1 (OFFSETS/CONNECTIVITY, FIELD string arrays).
  - `lookup_from_field` turns `segment_names` into a code-to-"code:name" map.
  - `coded_array` picks the integer array of which at least 80 % of values are codes in the lookup (`segment_label`).
  - The `branch` array is read but not used.
  - Source: [centerline_qc.py L145-499](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_qc.py)
- **Label naming.**
  - `count_codes` tallies, per file, which codes are used and whether that file names them.
  - `main` gives every code the most common name across files (`_code_names`). Unnamed codes stay `#n`.
  - `normalise_label` maps names to SCCT-style names through `ALIASES`; "lcx" maps to the unsplit "CX".
  - Source: [centerline_qc.py L695-737, 1186-1190, 1235-1256](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_qc.py)
- **Graph construction** (`analyse_case`).
  - Points within DEDUP_TOL become one node; consecutive points in a polyline form edges.
  - A polyline end is joined to the nearest point of another polyline within JOIN_TOL.
  - Lengths are summed over unique edges, each split half and half between its two end labels.
  - Components are found with union-find; "tiny" means under 10 mm.
  - Label contacts are counted as direct edges or as "via unlabelled" (both labels touch the same unlabelled stretch).
  - Overlap is polyline length (beyond 2 mm from its ends) within OVERLAP_TOL of another polyline, or on shared nodes.
  - `split_gaps` only *counts* jumps for explicit (VTK) connectivity.
  - Source: [centerline_qc.py L753-932](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_qc.py)
- **Flags** (`flags_for`):
  - no_LM / no_LAD / no_CX / no_RCA: no length with that label.
  - unlabelled > 20 %; components > 2.
  - left_and_right_in_one_tree: 1 component holding both RCA and LAD/LM.
  - impossible_contact: LAD/LM/CX touching RCA.
  - disconnected_segment: any `conn_* == "missing"`.
  - Segment length between 0 and 2 mm.
  - gaps; unknown labels (`?`/`#`).
  - total_mm < 50 or > 2000.
  - overlap > 20 % of total.

  Source: [centerline_qc.py L935-953](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_qc.py)
- **Complete trunks.** `TRUNKS` = LAD [LM, pLAD, mLAD, dLAD], CX [LM, pCX, CX], RCA [pRCA, mRCA, dRCA], RCA_no_dRCA [pRCA, mRCA]. Complete means every segment has length > 0 and every non-first segment's `conn_` is direct or via unlabelled. Note that `conn_CX` accepts LM *or* pCX as the parent — [centerline_qc.py L128-135, L1034-1052](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_qc.py)
- **Embedded SCCT map.** The script's SCCT dict assigns 13 mCX, 14 OM2, 15 PDA, 16 PLA, 17 IM, 18 PLA, consistent with the SCCT 18-segment model. That model has 15 L-PDA, 16 R-PLB, 17 ramus intermedius and 18 L-PLB — [centerline_qc.py L96-98](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_qc.py); [World J Radiol figure reproducing the SCCT scheme](https://pmc.ncbi.nlm.nih.gov/articles/PMC4919754/figure/F3)
- **What the QC never checks:**
  - path order: "joined" is a contact test, not ordering;
  - where the ostium is (the CGPS files have no ostium flag, unlike ImageCAS-X's `start_points`);
  - how much of a label lies on the trunk versus on same-label twigs;
  - foreign or unlabelled length *on* the trunk;
  - cycles.

  Sources: [centerline_qc.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_qc.py); [tortuosity/vessels.py docstring](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/tortuosity/vessels.py)

**(c) Proposed per-artery rule.** All thresholds are top-level constants in [centerline_selection.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_selection.py).

- **Path definition.**
  - The trunk is the geodesic path from the ostium to the farthest node carrying the most distal trunk label. This is the method of [tortuosity/vessels.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/tortuosity/vessels.py), so a same-label twig cannot replace the trunk.
  - The ostium has to be inferred, because these files have no `start_points` flag:
    - left, with LM present: the LM end point (degree 1) farthest from pLAD (for LAD) or pCx (for CX);
    - left without LM, and RCA: the end point of the first segment farthest from the next segment (mLAD / LCx / mRCA).
  - If there is no next segment, the direction is unknown and the trunk is excluded.
- **Segment sets.**
  - LAD = LM → pLAD → mLAD → dLAD.
  - CX = LM → pCx(11) → LCx(13, "CX"). mCX/dCX are accepted at the same rank if a later export splits them.
  - RCA = pRCA → mRCA → dRCA.
  - PDA/PLB, D1/D2, OM1, IM and the unnamed codes #18-#28 are all "foreign" on a trunk path.
- **Strict** (every condition must hold):
  - the required segments are on the path, each at least `MIN_SEG_MM["strict"] = 5 mm` (LAD p/m/d; CX pCx + LCx; RCA p/m/d);
  - left trunks have LM on the path between `MIN_LM_MM = 2 mm` and `MAX_LM_MM = 35 mm`, and the ostium is a free end;
  - label ranks along the path never decrease (monotone);
  - foreign label on the path is at most 1 mm (a junction node is 0.5 mm);
  - the longest unlabelled stretch is at most 2 mm, and the unlabelled share at most 5 %;
  - no path edge is longer than `MAX_STEP_MM = 1.5 mm` (the spacing is 0.5 mm and joins are ≤ 1 mm);
  - the trunk length after LM is at least 70 / 40 / 70 mm (LAD / CX / RCA);
  - the trunk's own labels have no more than 5 mm in another component (fragments);
  - the component has no cycle and no labels from the other side (left/right mixing);
  - if a radius array exists, at least 90 % of path points lie in 0.3-4.0 mm;
  - the case total is between 50 and 2000 mm (the QC's units check).
- **Acceptable:**
  - only the proximal and mid segments are required (dLAD or dRCA may be missing or short); CX still needs pCx + LCx;
  - segments must be at least 3 mm;
  - LM may be absent;
  - foreign label at most 3 mm; unlabelled stretch at most 5 mm and share at most 15 %;
  - trunk at least 40 / 30 / 40 mm;
  - monotone order, no jump, known orientation and the case-level length check still apply;
  - fragments, cycles and mixing are allowed but counted.
- **Excluded:** anything else, with every failed criterion listed.
- **LM tier:**
  - strict: LM present, in one piece, a free-end ostium shared by the LAD and CX paths, 2-35 mm on the path, no mixing;
  - acceptable: LM present on at least one left path, at least 0.5 mm;
  - excluded: LM absent.
- **Where the thresholds come from:**
  - 0.5 mm spacing, n_gaps = 0 and n_joins ≤ 1 make 1.5 mm a safe jump test — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)
  - Segment p5 values are 7.7 mm (pLAD), 14.6 (mLAD), 18.2 (dLAD), 12.5 (pCX), 9.7 (CX) and 22.3 (pRCA). A 5 mm per-segment minimum therefore removes only the broken tail, about the 3 cases with segments under 2 mm — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)
  - The acceptable trunk minimum of at least 30 mm protects the taper fit. [tortuosity/taper.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/tortuosity/taper.py) drops the first 3 mm and the zones near junctions, and returns NaN when fewer than 20 mm of arc or fewer than 60 % of samples remain.
  - MAX_LM_MM = 35 sits well above the QC LM p95 of 20.9 mm (max 48.3) — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)
- **Treating a missing LM as acceptable rather than real separate ostia is a judgement.** CT cohorts report an absent LM with separate LAD/LCx ostia in 0.16 % (5 of 3,181) to 0.77 % (12 of 1,562) of patients. This data has no LM in 60 of 744 cases (8.1 %), so most of those are probably segmentation or labelling misses — [jcpres single-centre cohort](https://jcpres.com/article/2816); [Vojnosanit Pregl 2018](https://aseestant.ceon.rs/index.php/vsp/article/view/VSP160205201I); [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)

**Counts per tier per artery derivable from the report** (upper bounds; the exact numbers need the script):

- **LM:**
  - present in 684 cases;
  - both LM→pLAD (684/684) and LM→pCX (682/682) are joined in the cases with those segments;
  - strict is at most 682 and usable at most 684; excluded is at least 60 (no_LM) — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)
- **LAD:**
  - strict is at most 576 (complete LM+LAD);
  - strict + acceptable is at most 678 (pLAD and mLAD both present and joined, LM not required);
  - excluded is at least 66, including 42 no_LAD;
  - the 9 cases with a dLAD-pLAD contact and the 1 with a missing mLAD-pLAD join will drop out of the usable tiers — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)
- **CX:** strict at most 581; usable at most 599 (CX present and joined); excluded at least 145 — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)
- **RCA:** strict at most 553; usable at most 567 (pRCA + mRCA joined); excluded at least 177 — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)
- **All three:** strict at most 366 (all three complete including dRCA) — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)

### Inferences

**Where the real counts will fall below the bounds**
- The strict counts will be lower than the bounds. The extra path checks (trunk length, foreign or unlabelled length on the path, fragments, cycles, LM length, free-end ostium) have no counterpart in the QC.
- The largest drops are likely for CX:
  - the LCx (13) p5 is 9.7 mm and the pCX median is only 26.4 mm, so the 40 mm strict minimum will bite;
  - #22 touches CX in 216 cases. If #22 is actually the distal circumflex, the CX path stops early.

**Flags that should not exclude a trunk**
- `unknown_labels` (546) and `>2_components` (396) should not exclude an artery.
  - The unnamed codes contact trunks the way side branches do (#18 at pLAD/mLAD, #21 at dLAD, #28 at pCX).
  - With pieces under 10 mm ignored, 226 of 366 complete cases have exactly 2 components.
  - Per-artery path grading only penalises these when they sit *on* the trunk path or carry the trunk's own labels.
- `unlabelled>20%` (287) is mostly side-branch length. It only matters if the unlabelled length lies on the trunk path; the QC found only 1 trunk join via unlabelled points (mRCA-pRCA).

**What the label distributions and topology suggest**
- The tight mLAD length (IQR 30.0-30.9 mm) and the near-equal pRCA/mRCA/dRCA lengths (about 38-40 mm each) suggest that proximal/mid/distal boundaries are set by a length rule in Medis or Kit's labelling, not by anatomy. Position-aware windows should therefore be defined by arc-length fraction along the path, using segment labels only to fix the trunk ends. This fits the thesis choice of a vessel-level outcome.
- In this export, 9 cases with 1 component is the same count as 9 no_RCA cases, and left_and_right_in_one_tree never fired. The single-component cases are therefore probably one-sided trees, not merged left/right trees.

**Two QC outputs that look wrong as written**
- Code 14 = L-PLB and code 15 = L-PDA conflict with SCCT's 14 = OM2 and 18 = L-PLB. Reading these files as SCCT numbers would have been wrong, so "raw" was the right numbering. The unnamed 18 is also not SCCT L-PLB here, since it contacts LAD segments (#18-mLAD 193, #18-pLAD 162).
- Code 17 named "AL" in 4 files becomes `?AL`, while 17 named "RI" becomes IM. AL (anterolateral) is often used as a synonym for the ramus. Neither matters for trunks; both are foreign on the trunk path.

### Gaps
- Exact tier counts per artery cannot be derived from the report. The path-based metrics did not exist when it was run, so they require running `centerline_selection.py` on the secure machine.
- No lower bound on strict counts can be given. The 45 flag-free cases are not a lower bound, because the flags do not test lengths along the path.
- The thresholds (5 mm segments; 70/40/70 and 40/30/40 mm trunks) are justified by the report distributions and the taper code's 20 mm requirement. They are not taken from published centerline-QC standards; I found no such standard.

## What does the report reveal that is ambiguous or suspicious (red flags) and needs answers before selection is final?

### Takeaway
The labels and topology are clean: 0 gaps, 0 impossible contacts, and the LM→pLAD/pCx joins are 100 % direct. The open questions are about meaning:
- six unnamed codes, one of which (#22) may be distal CX;
- non-SCCT numbering (14/15);
- `segment_names` lists that omit codes the file uses;
- no radius array;
- an unused `branch` array;
- 8 % missing LM;
- unknown identity of the 744 cases (which study_ids, BL or FU, and what "10Y" means).

The report also contains case IDs and sits untracked in the repository.

### Cited Findings
- **No radius.** `median_radius` has n = 0, and the only point arrays are `segment_label` and `branch`. The trunk taper T (Theil-Sen slope of ln r against arc length) needs a lumen radius. In this repository that radius comes from lumen-mask cross-sections ([tortuosity/taper.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/tortuosity/taper.py)) or a distance transform ([bifurcation/radius.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/bifurcation/radius.py)). The latter says neither delivered nor predicted ImageCAS-X centerlines carry a radius either — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)
- **Unnamed codes** #18-#22 and #28 have the contact patterns below. Unnamed code 23 and codes 25-27 do not occur — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)

  | Code | Contacts (cases) | Median length (mm) |
  |---|---|---|
  | #18 | mLAD 193, pLAD 162, dLAD 20 | 13.6 |
  | #19 | mLAD 98, dLAD 45, pLAD 14 | 10.7 |
  | #20 | dLAD 35, mLAD 19 | 11.0 |
  | #21 | dLAD 140, mLAD 69 | 21.3 |
  | #22 | CX 216, pCX 20 | 34.9 |
  | #28 | pCX 151, CX 36, mRCA 1 | 48.3 |

- **`segment_names` is incomplete per file.** Many files use codes without naming them: code 2 is unnamed in 476 of 569 files, and code 10 (D2) is named in only 31 of the 295 files that use it. The "7 files with only pRCA" are files that *name* only pRCA. Whether they contain only pRCA is not shown; no_RCA is 9 and no_LM is 60 — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)
- **Dominance-like codes.** L-PLB (14) is in 102 files and L-PDA (15) in 32. R-PLB (16) is used in 511 and R-PDA (4) in 428. The QC pools them as PLA/PDA. Both BL and FU headers contain `ct_cag_dominance` for a cross-check — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md); [header_BL.xlsx / header_FU.xlsx](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/header_BL.xlsx), read directly
- **pRCA without mRCA.** pRCA is present in 732 cases but mRCA in only 569: about 163 RCAs carry pRCA without mRCA. pRCA also reaches 119.3 mm at the maximum (p95 64) — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)
- **Outlier cases.**
  - total_mm max 3645.7, with n_polylines up to 165 and branch points up to 160;
  - a PDA reaching 971.1 mm;
  - total_mm min 36.6 mm;
  - total_length_odd flags 2 cases.

  Source: [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)
- **Topology anomalies.** dLAD touches pLAD (skipping mLAD) in 9 cases, mLAD touches pCX in 3, and 8 cases have a disconnected segment — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)
- **Overlap.** Median 16.8 mm per case, max 224.4 mm, while n_joins is about 0. Polylines share stretches (likely common proximal parts or shared junction nodes), but the 20 % flag never fired — [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md)
- **Which cohort.** The QC docstring calls the data "Herlev-Østerbro / CGPS baseline cohort, 744 cases", while the file name says `10Y` — [centerline_qc.py L1-2](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_qc.py). The project memory records 2,116 BL+FU patients, of whom only about 1,020 have BL segment reads (memory note cgps-data-caveats, from the user's earlier cgps_stats aggregate reports).
- **Privacy.**
  - report_qc.md lists up to 40 case IDs per red flag (for example "47, 49, 92, ...", values up to 2,829).
  - The QC script's own docstring says "The report and CSVs contain case IDs (file / folder names); keep them on the DTU machine".
  - `git status` shows `CGPS_data/report_qc.md` as untracked and not git-ignored (`git check-ignore` returns nothing).
  - Sources: [report_qc.md](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report_qc.md); [centerline_qc.py L27](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_qc.py)
- **Image-quality and evaluability columns that exist:**
  - **BL:** `scan_qualitative_quality`, `bad_quality`, `Image_Quality_reason_1/2` (free text), `ct_cag_eval_n`, `ct_cag_incomplete`, `ct_cag_uneval`, `ct_cag_lad_uneval`, `ct_cag_cx_uneval`, `ct_cag_rca_uneval`, per-segment `ct_cag_<seg>_eval`, and BL-only `ct_cag_<seg>_medis_egnet` / `ct_cag_<seg>_medis_finished`.
  - **FU:** `ct_cag_uneval_motion/noise/scanfield/contrastdefect/pm/other`, per vessel `ct_cag_{lad,cx,rca}_uneval_{contrast,scanfield,pm,noise}`, per-segment `_eval`, `ct_cacs_*_eval` and `scandata_kv`.

  Source: [header_BL.xlsx](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/header_BL.xlsx) and [header_FU.xlsx](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/header_FU.xlsx), read directly.

### Inferences

**Possible meaning of the unnamed codes**
- #18-#21 behave like extra LAD side branches (diagonals beyond D2, or septals).
- #22 behaves like OM2 or a distal CX continuation.
- #28 behaves like an early CX branch (OM, or a ramus-like branch).
- If #22 is actually dCX, the CX trunk is cut short in up to 216 cases. Setting `CODE_NAMES = {22: "dCX"}` in the selection script would include it.

**What the per-file `segment_names` lists might record**
- The lists vary from file to file, and codes 14/15 are always named when used.
- This could mean `segment_names` records which segments were edited or finished in Medis rather than which exist. That would link to the BL-only `ct_cag_<seg>_medis_finished` / `_medis_egnet` columns. This is a hypothesis to put to Kit.

**Privacy**
- The case IDs in report_qc.md may be study_ids. If so, the laptop copy breaks the user's "only aggregates leave" rule.
- The file should not be committed. It should be deleted from the laptop, or regenerated without ID lists, after checking with the data agreement.

### Gaps (open questions for Kit, or for the user's data manager)

**Identity of the 744 cases**
1. Which visit are the centerlines from (BL or FU)? What does "10Y" in `centerlines_hø_10Y.zip` mean (the 10-year follow-up scan, or the 10-year cohort)? The QC docstring says baseline.
2. Is the case ID (file stem) the `study_id`? If not, where is the key?
3. Which 744 of the about 2,116 patients are included, and why? For example, a Herlev-Østerbro site subset, the read BL half (about 1,020), or a random sample.

**How the centerlines were made**
4. Did they come from the Medis automatic segmentation, or were they manually corrected? Is this per segment (relating to `ct_cag_<seg>_medis_finished` / `_medis_egnet`)? Were the reader's CCTA segment grades made on the same Medis tree?
5. What coordinate system are the points in (scanner/patient LPS or RAS, or a Medis internal frame)? Do they align with the CT volume's affine, so that radius can be sampled from the CT?

**Codes and arrays in the files**
6. What do codes 18, 19, 20, 21, 22 and 28 mean? In particular, is 22 OM2 or the distal LCx?
7. Why does each file's `segment_names` list only some of the codes it uses?
8. Why is the numbering non-SCCT? 14 = L-PLB and 15 = L-PDA here, whereas SCCT has 14 = OM2, 15 = L-PDA and 18 = L-PLB. Does 13 "LCx" always cover both mid and distal CX?
9. Code 17 is named "RI" in some files and "AL" in others: is it the same branch?
10. What does the `branch` point array hold (polyline ID, path ID from the ostium, Medis branch index)? Does it identify separate ostium-to-tip paths, and could it replace the inferred ostium?
11. Is a radius, lumen contour or diameter available in Medis (for example a QAngio/Medis lumen export)? Can it be exported? Otherwise radius must come from CT segmentation.
12. Code 24 is "unlabelled", covering about 226k points and 21 % of length: is it vessel the labeller could not assign, or junction filler?

**How dominance and specific cases are encoded**
13. Is dominance encoded by which PDA/PLB codes appear? Does that agree with `ct_cag_dominance` (in both BL and FU)?
14. Why do about 163 cases have pRCA without mRCA, with pRCA up to 119 mm? Is the whole RCA labelled pRCA in those?
15. Is a missing LM (60 cases, 8 %) a true separate-ostia anatomy or a segmentation miss? The literature prevalence is 0.16-0.77 %.
16. What explains the two total-length outliers (36.6 mm and 3,645.7 mm) and the 971 mm "PDA"?

**Matching to the reader data**
17. How should trunk centerlines be matched to reader reads? The plan is to cross-tabulate tier against `ct_cag_<seg>_eval` (both visits), `ct_cag_{lad,cx,rca}_uneval`, BL `bad_quality` / `scan_qualitative_quality` / `ct_cag_eval_n`, and the FU `ct_cag_uneval_*` reasons. `Image_Quality_reason_1/2` is free text and must not be tabulated. These columns exist in the headers; no "centerline quality" variable exists in either header.

## What should the runnable selection script output?

### Takeaway
[centerline_selection.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_selection.py) imports `centerline_qc` for the zip reader, VTK parser, label naming and graph tolerances. It grades LM, LAD, CX and RCA per case into strict, acceptable or excluded, with reasons, and writes two files:
- `secure_only/centerline_tiers.csv`: row-level with case IDs; it stays on the secure machine;
- `selection_report.md`: aggregate only, with small cells suppressed. It is the only file meant to leave.

It ran end to end on synthetic Kit-style VTK zips of 6 and 60 cases and gave the expected tiers.

### Cited Findings

**Usage**

```
python CGPS_data/centerline_selection.py [--src ZIP_OR_DIR] [--out DIR] [--limit N]
```

The defaults are `ZIP_PATH = qc.ZIP_PATH` (`/data/kimbr/centerlines_hø_10Y.zip`) and `OUT_DIR = ~/centerline_selection`. It needs only numpy and pandas, like the QC script. scipy is optional and is used through `qc.nearest` — [centerline_selection.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_selection.py)

**How it reuses the QC script**
- It uses `qc.Source`, `qc.group_cases`, `qc.parse_member`, `qc.count_codes`, `qc.decide_numbering`, `qc._code_names`, `qc.normalise_label`, `qc.split_gaps`, `qc.nearest`, `qc.TERRITORY`, `qc.DEDUP_TOL` and `qc.JOIN_TOL`.
- It wraps `qc.polys_from_mesh` to keep the `branch` array per polyline, which the QC drops.
- `build_graph` copies the node, edge and join logic of `analyse_case`, but keeps node labels, adjacency, components, cycles, radius and branch.
- `LABEL_NUMBERING = "raw"` and `CODE_NAMES = {}` (Kit's answers go here).
- Source: [centerline_selection.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_selection.py)

**Per-artery metrics** (columns of the secure CSV)
- tier, why_not_strict, why_excluded, case_total_mm;
- artery_present, path_found, orientation_known, ostium_is_end, lm_in_component;
- path_mm, trunk_mm, lm_mm, `<segment>_mm` on the path;
- foreign_mm, foreign_run_mm, unlabelled_mm, unlabelled_run_mm, unlabelled_pct;
- monotone, n_order_breaks, max_step_mm;
- fragment_mm, offpath_same_label_mm, cycles_in_component, left_right_mixed;
- radius_present, radius_valid_frac, radius_median;
- n_branch_ids_on_path.

LM rows instead carry lm_present, lm_mm, lm_total_mm, lm_pieces, lm_on_lad_path, lm_on_cx_path, lm_shared_ostium and ostium_is_end — [centerline_selection.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_selection.py)

**Aggregate report sections**
1. Settings: every threshold.
2. Tier per artery (LM, LAD, CX, RCA × strict, acceptable, excluded, usable), with primary and secondary suppression.
3. Reasons per artery, as "not strict" and "excluded" counts.
4. Usable-artery patterns per case (LAD+CX+RCA, ..., none).
5. Cross-tables of LAD and CX tier by LM tier.
6. On-path length summaries by artery and tier: mean/SD from 5 values, quartiles from 10, never min/max.
7. Radius presence, duplicate points, and whether `branch` is constant per polyline.
8. Label codes by number of files.

It never prints a case ID: read and analysis errors are counted, not listed — [centerline_selection.py](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/centerline_selection.py)

**Disclosure control.** `small`, `count`, `disclosive`, `count_of` and `suppress` are copied from cgps_stats.py with MIN_CELL = 5, QUARTILE_MIN = 10 and GROUP_MIN = 20 — [cgps_stats.py L46-49, L109-166](/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/cgps_stats.py)

**Verification on synthetic data**
- The generator is `/private/tmp/claude-501/-Users-mathildebrinchsorensen-Desktop-ImageCAS-X/0e34615c-f6d3-4d97-a78c-7ddbaa9d53fb/scratchpad/gen/make_synth.py`.
- It writes legacy VTK 4.2 and 5.1 (OFFSETS/CONNECTIVITY) ASCII files with `segment_label`, `branch` and `segment_names`, at 0.5 mm spacing, plus a `.log` decoy. Some cases have a `MaximumInscribedSphereRadius` array.
- The 6-case zip gave the expected grades:

  | Synthetic case | Expected grade |
  |---|---|
  | All segments present | strict for every artery |
  | No LM, no dLAD, no dRCA | LAD, CX and RCA acceptable; LM excluded |
  | mLAD→pLAD→unlabelled→dLAD order | LAD excluded (`labels_not_in_order`, `unlabelled_stretch_on_path`) |
  | pRCA only | RCA excluded (`mRCA_missing_or_short`, `orientation_unknown`, `trunk_too_short`) |
  | Left side absent | LAD/CX `artery_absent` |
  | Short LCx | CX acceptable (`trunk_too_short` for strict) |

- The radius array was detected, with a valid fraction of 1.0.
- The 60-case run showed unsuppressed counts and quartiles. A grep for case-ID strings in that report found 0 hits.
- Outputs: `/private/tmp/claude-501/-Users-mathildebrinchsorensen-Desktop-ImageCAS-X/0e34615c-f6d3-4d97-a78c-7ddbaa9d53fb/scratchpad/sel_out/` and `/private/tmp/claude-501/-Users-mathildebrinchsorensen-Desktop-ImageCAS-X/0e34615c-f6d3-4d97-a78c-7ddbaa9d53fb/scratchpad/sel60/`.

### Inferences
- **Next step after the first run:**
  - set `CODE_NAMES` once Kit answers (for example, if 22 = dCX);
  - rerun;
  - join `secure_only/centerline_tiers.csv` to the BL/FU tables on the secure machine by `study_id`, if the case ID is the study_id;
  - cross-tabulate tier against `ct_cag_<seg>_eval`, `ct_cag_*_uneval` and `bad_quality` using cgps_stats-style suppression.

  The geometry cohort per artery is then the intersection of: centerline tier usable, trunk plaque-free and evaluable (reader), and LM plaque-free (reader, for LAD/CX).
- **Threshold choices:**
  - Raising `REQUIRE_RADIUS` makes no sense for this export; the radius must be measured on the CT.
  - The strict LM requirement only concerns the LM centerline. LM plaque status comes from `ct_cag_lm_stenosis` (BL and FU) regardless of the centerline.

### Gaps
- The script has not been run on the real data, which is not on this laptop.
- Real-data edge cases may need small fixes: binary 5.1 parsing is inherited unchanged from the QC script, which already read all 744 files.
- Ostium inference without a start flag is untested against ground truth. Kit's answer on the `branch` array (question 10) may allow a better ostium rule.
