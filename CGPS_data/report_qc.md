# Centerline quality report

Source `/data/kimbr/centerlines_hø_10Y.zip`: 744 cases found (expected 744), 744 read, **744 analysed**, 0 with read errors.

Settings: JOIN_TOL 1.0 mm, DEDUP_TOL 0.01 mm, gap > max(3.0 mm, 5.0x median spacing), numeric labels read as: **raw**.

## How the files were read

Most common parse results (arrays/columns found, which one was used as label):

- 26 files: `{"cell_arrays": [], "field_data": {"segment_names": ["1:pRCA", "5:LM", "6:pLAD", "7:mLAD", "8:dLAD", "9:D1", "11:pCx", "12:OM1", "13:LCx", "14:L-PLB", "24:unlabelled"]}, "label_array": "segment_label", "label_lookup": true, "point_arrays": ["segment_label", "branch"], "vtk_header": ["# vtk DataFile Version 5.1", "vtk output", "BINARY"], "vtk_keywords": {"DATASET": 1, "FIELD": 2, "LINES": 1, "POINT`
- 19 files: `{"cell_arrays": [], "field_data": {"segment_names": ["1:pRCA", "5:LM", "6:pLAD", "7:mLAD", "8:dLAD", "9:D1", "11:pCx", "12:OM1", "13:LCx", "14:L-PLB", "17:RI", "24:unlabelled"]}, "label_array": "segment_label", "label_lookup": true, "point_arrays": ["segment_label", "branch"], "vtk_header": ["# vtk DataFile Version 5.1", "vtk output", "BINARY"], "vtk_keywords": {"DATASET": 1, "FIELD": 2, "LINES": `
- 15 files: `{"cell_arrays": [], "field_data": {"segment_names": ["1:pRCA", "2:mRCA", "3:dRCA", "4:R-PDA", "16:R-PLB", "24:unlabelled"]}, "label_array": "segment_label", "label_lookup": true, "point_arrays": ["segment_label", "branch"], "vtk_header": ["# vtk DataFile Version 5.1", "vtk output", "BINARY"], "vtk_keywords": {"DATASET": 1, "FIELD": 2, "LINES": 1, "POINTS": 1, "POINT_DATA": 1}}`
- 12 files: `{"cell_arrays": [], "field_data": {"segment_names": ["1:pRCA", "5:LM", "6:pLAD", "7:mLAD", "8:dLAD", "9:D1", "11:pCx", "12:OM1", "13:LCx", "24:unlabelled"]}, "label_array": "segment_label", "label_lookup": true, "point_arrays": ["segment_label", "branch"], "vtk_header": ["# vtk DataFile Version 5.1", "vtk output", "BINARY"], "vtk_keywords": {"DATASET": 1, "FIELD": 2, "LINES": 1, "POINTS": 1, "POIN`
- 9 files: `{"cell_arrays": [], "field_data": {"segment_names": ["1:pRCA", "5:LM", "6:pLAD", "7:mLAD", "8:dLAD", "9:D1", "11:pCx", "12:OM1", "13:LCx", "14:L-PLB", "15:L-PDA", "24:unlabelled"]}, "label_array": "segment_label", "label_lookup": true, "point_arrays": ["segment_label", "branch"], "vtk_header": ["# vtk DataFile Version 5.1", "vtk output", "BINARY"], "vtk_keywords": {"DATASET": 1, "FIELD": 2, "LINES`
- 8 files: `{"cell_arrays": [], "field_data": {"segment_names": ["1:pRCA", "5:LM", "6:pLAD", "7:mLAD", "8:dLAD", "9:D1", "11:pCx", "12:OM1", "13:LCx", "14:L-PLB", "15:L-PDA", "17:AL", "24:unlabelled"]}, "label_array": "segment_label", "label_lookup": true, "point_arrays": ["segment_label", "branch"], "vtk_header": ["# vtk DataFile Version 5.1", "vtk output", "BINARY"], "vtk_keywords": {"DATASET": 1, "FIELD": `
- 7 files: `{"cell_arrays": [], "field_data": {"segment_names": ["1:pRCA", "24:unlabelled"]}, "label_array": "segment_label", "label_lookup": true, "point_arrays": ["segment_label", "branch"], "vtk_header": ["# vtk DataFile Version 5.1", "vtk output", "BINARY"], "vtk_keywords": {"DATASET": 1, "FIELD": 2, "LINES": 1, "POINTS": 1, "POINT_DATA": 1}}`
- 7 files: `{"cell_arrays": [], "field_data": {"segment_names": ["1:pRCA", "2:mRCA", "3:dRCA", "4:R-PDA", "5:LM", "6:pLAD", "7:mLAD", "8:dLAD", "9:D1", "11:pCx", "12:OM1", "16:R-PLB", "24:unlabelled"]}, "label_array": "segment_label", "label_lookup": true, "point_arrays": ["segment_label", "branch"], "vtk_header": ["# vtk DataFile Version 5.1", "vtk output", "BINARY"], "vtk_keywords": {"DATASET": 1, "FIELD": `

## Label codes

Integer codes in the label array. Each file names only some codes in its own `segment_names`; a code a file uses without naming it gets the name other files give it (most common). Codes no file names stay `#n` - ask Kit what they are.

| code | names in segment_names (files) | used as | files using it | files not naming it | points |
|---|---|---|---|---|---|
| 1 | pRCA (242) | pRCA | 732 | 490 | 61250 |
| 2 | mRCA (93) | mRCA | 569 | 476 | 43168 |
| 3 | dRCA (92) | dRCA | 556 | 464 | 41850 |
| 4 | R-PDA (70) | PDA | 428 | 358 | 45406 |
| 5 | LM (204) | LM | 684 | 480 | 17732 |
| 6 | pLAD (210) | pLAD | 699 | 489 | 31097 |
| 7 | mLAD (194) | mLAD | 682 | 488 | 41949 |
| 8 | dLAD (187) | dLAD | 600 | 413 | 95530 |
| 9 | D1 (193) | D1 | 625 | 432 | 76454 |
| 10 | D2 (31) | D2 | 295 | 264 | 25467 |
| 11 | pCx (217) | pCX | 707 | 490 | 39678 |
| 12 | OM1 (169) | OM1 | 500 | 331 | 63897 |
| 13 | LCx (175) | CX | 599 | 424 | 53957 |
| 14 | L-PLB (102) | PLA | 102 | 0 | 8672 |
| 15 | L-PDA (32) | PDA | 32 | 0 | 1530 |
| 16 | R-PLB (78) | PLA | 511 | 433 | 60129 |
| 17 | RI (54); AL (4) | IM | 199 | 141 | 29185 |
| 18 |  | #18 | 375 | 375 | 15017 |
| 19 |  | #19 | 161 | 161 | 5948 |
| 20 |  | #20 | 55 | 55 | 1813 |
| 21 |  | #21 | 210 | 210 | 11557 |
| 22 |  | #22 | 238 | 238 | 21316 |
| 24 | unlabelled (250) | (unlabelled) | 736 | 486 | 226145 |
| 28 |  | #28 | 184 | 184 | 25300 |

## Label values

Raw labels and the segment they were mapped to (`?x` = not recognised, `#n` = number not mapped, empty = unlabelled). **Check this first** - all other numbers depend on it.

| raw_label | mapped_to | n_points |
|---|---|---|
| 24 |  | 128875 |
| 24:unlabelled |  | 97270 |
| 8 | dLAD | 66883 |
| 9 | D1 | 55125 |
| 16 | PLA | 54599 |
| 12 | OM1 | 40886 |
| 1 | pRCA | 38509 |
| 4 | PDA | 37315 |
| 2 | mRCA | 36691 |
| 3 | dRCA | 35645 |
| 7 | mLAD | 30427 |
| 13 | CX | 29715 |
| 8:dLAD | dLAD | 28647 |
| 11 | pCX | 27281 |
| 28 | #28 | 25300 |
| 13:LCx | CX | 24242 |
| 12:OM1 | OM1 | 23011 |
| 10 | D2 | 22958 |
| 1:pRCA | pRCA | 22741 |
| 17 | IM | 21527 |
| 9:D1 | D1 | 21329 |
| 22 | #22 | 21316 |
| 6 | pLAD | 20882 |
| 18 | #18 | 15017 |
| 5 | LM | 12636 |
| 11:pCx | pCX | 12397 |
| 21 | #21 | 11557 |
| 7:mLAD | mLAD | 11522 |
| 6:pLAD | pLAD | 10215 |
| 14:L-PLB | PLA | 8672 |
| 4:R-PDA | PDA | 8091 |
| 17:RI | IM | 7224 |
| 2:mRCA | mRCA | 6477 |
| 3:dRCA | dRCA | 6205 |
| 19 | #19 | 5948 |
| 16:R-PLB | PLA | 5530 |
| 5:LM | LM | 5096 |
| 10:D2 | D2 | 2509 |
| 20 | #20 | 1813 |
| 15:L-PDA | PDA | 1530 |
| 17:AL | ?AL | 434 |

## Overview per case

| metric | n | mean | min | p5 | q1 | median | q3 | p95 | max |
|---|---|---|---|---|---|---|---|---|---|
| total_mm | 744.0 | 690.2 | 36.6 | 320.2 | 521.9 | 685.4 | 849.5 | 1054.2 | 3645.7 |
| unlabelled_mm | 744.0 | 146.8 | 0.0 | 12.4 | 63.1 | 119.6 | 192.3 | 337.7 | 2446.5 |
| unlabelled_pct | 744.0 | 20.3 | 0.0 | 3.4 | 10.9 | 17.2 | 24.8 | 45.6 | 100.0 |
| n_polylines | 744.0 | 16.0 | 3.0 | 7.0 | 11.0 | 15.0 | 19.0 | 27.0 | 165.0 |
| n_points | 744.0 | 1403.3 | 77.0 | 648.6 | 1059.0 | 1391.0 | 1726.5 | 2144.3 | 7531.0 |
| n_branch_points | 744.0 | 13.1 | 0.0 | 4.0 | 8.0 | 12.0 | 16.0 | 23.0 | 160.0 |
| n_end_points | 744.0 | 18.7 | 4.0 | 9.0 | 14.0 | 18.0 | 22.0 | 30.0 | 168.0 |
| max_degree | 744.0 | 3.1 | 2.0 | 3.0 | 3.0 | 3.0 | 3.0 | 4.0 | 4.0 |
| n_components | 744.0 | 2.8 | 1.0 | 2.0 | 2.0 | 3.0 | 3.0 | 4.0 | 6.0 |
| n_tiny_components | 744.0 | 0.4 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 2.0 | 3.0 |
| n_gaps | 744.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| n_joins | 744.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| overlap_mm | 744.0 | 18.0 | 0.0 | 5.8 | 11.8 | 16.8 | 22.4 | 31.3 | 224.4 |
| median_spacing_mm | 744.0 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 |
| max_spacing_mm | 744.0 | 0.7 | 0.5 | 0.6 | 0.6 | 0.7 | 0.7 | 0.8 | 0.8 |
| extent_x | 744.0 | 109.5 | 25.7 | 82.2 | 102.1 | 111.5 | 119.8 | 130.7 | 186.6 |
| extent_y | 744.0 | 93.1 | 29.5 | 67.7 | 84.9 | 94.4 | 103.0 | 113.5 | 125.9 |
| extent_z | 744.0 | 88.9 | 20.6 | 66.0 | 83.0 | 89.8 | 96.7 | 107.5 | 133.0 |
| median_radius | 0.0 |  |  |  |  |  |  |  |  |

Units: total lengths of ~200-800 mm and extents of ~50-150 mm mean mm; much smaller values suggest cm, much larger voxels.

Unlabelled length over all cases: 109218 of 513515 mm (**21.3 %**); cases with any unlabelled length: 736 of 744.

Connected components (separate pieces) per case - expect 2: left and right tree. In complete-trunk cases the LAD/CX trunks are one piece and the RCA trunk another, so extra pieces are side branches or fragments:

| components | all cases | complete trunks | complete trunks, pieces < 10 mm ignored |
|---|---|---|---|
| 1 | 9 | 0 | 0 |
| 2 | 339 | 155 | 226 |
| 3 | 244 | 130 | 114 |
| 4 | 118 | 64 | 24 |
| 5 | 28 | 12 | 2 |
| 6 | 6 | 5 | 0 |

## Segments: presence and length (mm)

| segment | cases | % cases | mean | min | p5 | q1 | median | q3 | p95 | max |
|---|---|---|---|---|---|---|---|---|---|---|
| LM | 684 | 91.9 | 12.8 | 0.5 | 5.7 | 9.7 | 12.3 | 15.8 | 20.9 | 48.3 |
| pLAD | 699 | 94.0 | 22.5 | 3.5 | 7.7 | 14.8 | 21.7 | 27.5 | 43.2 | 82.1 |
| mLAD | 682 | 91.7 | 30.9 | 3.9 | 14.6 | 30.0 | 30.5 | 30.9 | 48.0 | 57.4 |
| dLAD | 600 | 80.6 | 79.4 | 1.1 | 18.2 | 54.5 | 82.5 | 106.8 | 128.6 | 202.8 |
| D1 | 625 | 84.0 | 59.7 | 4.7 | 10.6 | 30.9 | 52.6 | 79.4 | 137.9 | 282.0 |
| D2 | 295 | 39.7 | 42.0 | 4.4 | 8.1 | 19.7 | 34.1 | 56.6 | 102.5 | 174.1 |
| IM | 195 | 26.2 | 72.0 | 3.6 | 7.9 | 30.9 | 57.9 | 108.8 | 163.9 | 290.4 |
| pCX | 707 | 95.0 | 27.7 | 3.7 | 12.5 | 16.0 | 26.4 | 34.6 | 52.6 | 84.4 |
| CX | 599 | 80.5 | 44.9 | 2.2 | 9.7 | 26.9 | 37.2 | 60.3 | 101.4 | 137.4 |
| OM1 | 500 | 67.2 | 62.7 | 4.2 | 9.4 | 29.7 | 52.2 | 83.5 | 146.8 | 256.2 |
| pRCA | 732 | 98.4 | 41.8 | 4.7 | 22.3 | 35.8 | 40.0 | 46.1 | 64.0 | 119.3 |
| mRCA | 569 | 76.5 | 38.1 | 4.2 | 26.7 | 34.4 | 38.3 | 43.0 | 49.0 | 66.5 |
| dRCA | 556 | 74.7 | 37.8 | 3.2 | 17.9 | 34.2 | 38.1 | 42.8 | 49.0 | 90.8 |
| PDA | 460 | 61.8 | 50.0 | 4.5 | 14.3 | 29.5 | 44.8 | 61.1 | 92.1 | 971.1 |
| PLA | 613 | 82.4 | 55.1 | 3.6 | 11.5 | 24.3 | 45.8 | 75.5 | 130.3 | 374.5 |
| #18 | 375 | 50.4 | 19.0 | 3.0 | 5.2 | 8.6 | 13.6 | 22.6 | 47.0 | 260.5 |
| #19 | 161 | 21.6 | 17.4 | 2.5 | 4.9 | 7.4 | 10.7 | 20.0 | 51.0 | 164.4 |
| #20 | 55 | 7.4 | 15.5 | 3.2 | 5.0 | 6.4 | 11.0 | 16.6 | 42.5 | 78.8 |
| #21 | 210 | 28.2 | 26.7 | 4.2 | 6.5 | 11.8 | 21.3 | 35.8 | 65.9 | 110.8 |
| #22 | 238 | 32.0 | 43.9 | 3.1 | 6.6 | 17.1 | 34.9 | 62.3 | 107.9 | 187.6 |
| #28 | 184 | 24.7 | 67.2 | 2.7 | 5.8 | 16.8 | 48.3 | 101.4 | 180.6 | 309.8 |
| ?AL | 4 | 0.5 | 52.7 | 20.6 | 20.9 | 22.2 | 45.7 | 76.2 | 94.3 | 98.8 |

Whole arteries present (any of their segments):

- LM: 684 of 744 (91.9 %)
- LAD: 702 of 744 (94.4 %)
- CX: 707 of 744 (95.0 %)
- RCA: 735 of 744 (98.8 %)

## Complete main trunks (not dominance-dependent)

A trunk is complete when all its segments are present and each is joined to the one before it (directly or through unlabelled points). PDA/PLB are left out as they depend on dominance; dRCA can be small in left-dominant hearts, so RCA is also shown without it.

| trunk | complete cases | % of cases |
|---|---|---|
| LM + LAD (LM, pLAD, mLAD, dLAD) | 576 | 77.4 |
| LM + CX (LM, pCx, LCx) | 581 | 78.1 |
| RCA (pRCA, mRCA, dRCA) | 553 | 74.3 |
| RCA without dRCA (pRCA, mRCA) | 567 | 76.2 |
| All three (LAD, CX, RCA incl. dRCA) | 366 | 49.2 |
| All three, RCA without dRCA | 373 | 50.1 |

**Complete trunks** (all three, incl. dRCA; set by COMPLETE_RCA_NEEDS_DRCA): 366 of 744. Case IDs: `complete_trunks.txt`; per trunk: `complete_LAD.txt`, `complete_CX.txt`, `complete_RCA.txt`, `complete_RCA_no_dRCA.txt`. Figures: `figures/all/` (all centerlines) and `figures/complete_trunks/`.

## Expected connections

Among cases that have both the segment and one of its parents: `direct` = an edge joins them, `via_unlabelled` = joined through unlabelled points, `missing` = not joined (a gap > 1.0 mm or the segment hangs elsewhere).

| segment | parent(s) | cases | direct | via_unlabelled | missing |
|---|---|---|---|---|---|
| pLAD | LM | 684 | 684 | 0 | 0 |
| pCX | LM | 682 | 682 | 0 | 0 |
| mLAD | pLAD | 679 | 678 | 0 | 1 |
| dLAD | mLAD | 591 | 590 | 0 | 1 |
| mRCA | pRCA | 567 | 566 | 1 | 0 |
| dRCA | mRCA | 555 | 555 | 0 | 0 |
| CX | LM/pCX | 599 | 599 | 0 | 0 |
| D1 | LAD/dLAD/mLAD/pLAD | 625 | 625 | 0 | 0 |
| D2 | LAD/dLAD/mLAD/pLAD | 295 | 292 | 0 | 3 |
| IM | CX/LAD/LM/pCX/pLAD | 195 | 195 | 0 | 0 |
| OM1 | CX/dCX/mCX/pCX | 500 | 500 | 0 | 0 |
| PDA | CX/RCA/dCX/dRCA/mCX/mRCA/pCX/pRCA | 460 | 448 | 9 | 3 |
| PLA | CX/PDA/RCA/dCX/dRCA/mCX/mRCA/pCX/pRCA | 612 | 606 | 6 | 0 |

Unexpected segment contacts (pairs not in the expected list; number of cases):

- #22-CX: 216
- #18-mLAD: 193
- #18-pLAD: 162
- #28-pCX: 151
- #21-dLAD: 140
- #19-mLAD: 98
- #21-mLAD: 69
- #19-dLAD: 45
- #28-CX: 36
- #20-dLAD: 35
- #22-pCX: 20
- #18-dLAD: 20
- #20-mLAD: 19
- #19-pLAD: 14
- dLAD-pLAD: 9
- ?AL-pLAD: 3
- mLAD-pCX: 3
- #21-D2: 2
- #21-pLAD: 1
- #18-IM: 1
- D2-IM: 1
- #28-mRCA: 1
- #20-pLAD: 1
- #22-IM: 1
- #28-OM1: 1
- ?AL-pCX: 1

## Red flags

Cases without any flag: 45 of 744.

| flag | cases |
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
| total_length_odd(units?) | 2 |

- **unknown_labels** (546): 12, 13, 14, 16, 17, 21, 22, 24, 29, 31, 34, 36, 41, 42, 44, 55, 60, 65, 67, 68, 71, 78, 88, 96, 98, 109, 111, 112, 114, 115, 126, 131, 132, 141, 146, 147, 149, 154, 161, 162 ...
- **>2_components** (396): 11, 13, 22, 24, 28, 29, 34, 47, 49, 55, 60, 65, 67, 68, 69, 71, 78, 80, 86, 88, 92, 96, 98, 109, 111, 112, 114, 126, 131, 135, 141, 146, 147, 161, 185, 188, 189, 190, 196, 212 ...
- **unlabelled>20%** (287): 11, 12, 13, 22, 34, 36, 41, 47, 49, 68, 69, 78, 80, 81, 88, 92, 96, 98, 107, 109, 115, 120, 126, 131, 134, 135, 137, 177, 189, 196, 217, 218, 227, 245, 255, 266, 290, 300, 311, 313 ...
- **no_LM** (60): 47, 49, 92, 126, 134, 137, 189, 227, 255, 270, 313, 333, 338, 406, 434, 479, 539, 587, 594, 629, 655, 701, 756, 769, 784, 786, 940, 1039, 1052, 1132, 1138, 1191, 1290, 1360, 1364, 1383, 1405, 1423, 1439, 1716 ...
- **no_LAD** (42): 47, 49, 92, 134, 137, 189, 227, 255, 313, 333, 338, 479, 539, 587, 594, 629, 655, 701, 756, 769, 940, 1132, 1138, 1191, 1290, 1360, 1383, 1439, 1716, 1853, 1859, 1975, 1994, 2071, 2132, 2272, 2296, 2437, 2553, 2556 ...
- **no_CX** (37): 47, 49, 92, 134, 189, 227, 313, 333, 338, 406, 479, 539, 587, 594, 701, 756, 769, 786, 1132, 1138, 1191, 1290, 1383, 1788, 1859, 1975, 2071, 2132, 2263, 2269, 2272, 2296, 2437, 2532, 2553, 2773, 2829
- **no_RCA** (9): 137, 718, 727, 786, 1191, 1351, 1383, 2246, 2532
- **disconnected_segment** (8): 12, 362, 442, 672, 1609, 1964, 1980, 2173
- **segment<2mm** (3): 28, 444, 1874
- **total_length_odd(units?)** (2): 1360, 1716

Flag meanings: `no_LM/LAD/CX/RCA` = artery missing (a missing LM can be real - separate ostia - but check); `unlabelled>20%`; `>2_components` = fragments; `left_and_right_in_one_tree` = left and right trees joined (should be separate); `impossible_contact` = e.g. LAD touching RCA; `disconnected_segment` = an expected connection is missing; `segment<2mm`; `gaps_in_polyline` = jump inside one polyline; `unknown_labels` = labels not mapped (see label table); `overlapping_polylines` = > 20 % of length runs on top of another polyline.

Figures in `figures/all/` and `figures/complete_trunks/`: `segment_lengths.png`, `segment_presence.png`, `unlabelled_pct.png`, `branch_points.png`, `total_length.png`, `components.png`.
