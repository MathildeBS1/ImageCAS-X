# BL patients with plaque but no Medis centerline tree

Output of `CGPS_data/medis_missing_plaque.py`, run on dtu-gpu-7 on 2026-10-31. Trees are from
`/data/kimbr/HØ_10Y/Medis/Analysis_Processed/centerline_tree`. Aggregates only; counts 1-4 shown
as <5. Plaque at BL: `ct_cag_sis > 0` or `ct_cag_sss > 0`. Tree match: number in the tree file
name = study_id.

## Summary

- The Medis trees were expected to cover every patient with plaque at BL. They do not: of the
  **724** patients with plaque at BL, **599 (82.7 %) have a tree and 125 (17.3 %) do not**. All
  1,801 BL scans were read, so the 125 are not unread scans.
- **120 of the 125 (96.0 %) have `_medis_finished = 1`** in at least one segment, so the Medis
  plaque analysis was done for them and only the centerline tree is missing from the delivery.
  The other 5 lack a finished flag. Ask Kit whether those trees exist.
- The patients without a tree look like the patients with one. Plaque is in a trunk segment in
  94.4 % vs 96.5 %, in the pLAD in 74.4 % vs 74.1 % and in the mLAD in 61.6 % vs 60.4 %; the median
  number of plaque segments is 3 in both. They have somewhat less minimal-only plaque (27.2 % vs
  37.1 %) and more mild plaque (55.2 % vs 43.1 %) as the worst grade. Nothing here shows a selection
  by plaque location or severity behind the missing trees.
- Plaque type was not in this run. The script now reports it (per plaque segment and per patient,
  with the 120 finished patients as their own column); re-run to fill the section below.

## Patients by BL status and tree

| BL status | read | tree | no tree | total |
|---|---|---|---|---|
| plaque at BL | read | 599 | 125 | 724 |
| plaque at BL | not read | 0 | 0 | 0 |
| plaque-free at BL | read | <5 | 1,076 | 1,077 |
| plaque-free at BL | not read | 0 | 0 | 0 |
| SIS/SSS missing | | 0 | 0 | 0 |
| **all** | | **600** | **1,201** | **1,801** |

All tree IDs are in the BL sheet.

## Do the segment grades agree with SIS/SSS?

| | no tree n | % | tree n | % |
|---|---|---|---|---|
| no segment graded minimal or worse | 0 | 0.0 | 0 | 0.0 |
| some segment unevaluable / missing | 6 | 4.8 | 35 | 5.8 |

## Number of segments with plaque per patient

| | no tree n | % | tree n | % |
|---|---|---|---|---|
| 1 | 27 | 21.6 | 136 | 22.7 |
| 2 | 30 | 24.0 | 145 | 24.2 |
| 3-4 | 47 | 37.6 | 165 | 27.5 |
| 5+ | 21 | 16.8 | 153 | 25.5 |
| median (IQR) | 3 (2-4) | | 3 (2-5) | |

## Worst segment grade

| | no tree n | % | tree n | % |
|---|---|---|---|---|
| minimal | 34 | 27.2 | 222 | 37.1 |
| mild | 69 | 55.2 | 258 | 43.1 |
| moderate | 11 | 8.8 | 90 | 15.0 |
| severe | 8 | 6.4 | 19 | 3.2 |
| occlusion | <5 | 2.4 | 10 | 1.7 |

## Segments with plaque (grade minimal or worse)

Patients with plaque in each segment; % of the patients in the group. A patient counts once per
segment.

| | no tree n | % | tree n | % |
|---|---|---|---|---|
| LM | 30 | 24.0 | 162 | 27.0 |
| pLAD | 93 | 74.4 | 444 | 74.1 |
| mLAD | 77 | 61.6 | 362 | 60.4 |
| dLAD | 26 | 20.8 | 152 | 25.4 |
| D1 | 28 | 22.4 | 102 | 17.0 |
| D2 | 9 | 7.2 | 63 | 10.5 |
| IM | 5 | 4.0 | 30 | 5.0 |
| pCX | 28 | 22.4 | 123 | 20.5 |
| OM1 | 13 | 10.4 | 54 | 9.0 |
| mCX | 15 | 12.0 | 68 | 11.4 |
| OM2 | <5 | 3.2 | 19 | 3.2 |
| dCX | 5 | 4.0 | 21 | 3.5 |
| pRCA | 31 | 24.8 | 184 | 30.7 |
| mRCA | 22 | 17.6 | 128 | 21.4 |
| dRCA | 13 | 10.4 | 74 | 12.4 |
| PDA | <5 | 2.4 | 21 | 3.5 |
| PLA | <5 | 3.2 | 14 | 2.3 |
| any of the 9 trunk segments | 118 | 94.4 | 578 | 96.5 |
| only LM / side branches | 7 | 5.6 | 21 | 3.5 |
| any LAD (incl. D1, D2) | 118 | 94.4 | 552 | 92.2 |
| any CX (incl. OM1, OM2) | 40 | 32.0 | 198 | 33.1 |
| any RCA (incl. PDA, PLA) | 46 | 36.8 | 250 | 41.7 |

## Medis plaque-analysis status columns

Patients with at least one segment where the column is 1 / is filled at all.

| | no tree n | % | tree n | % |
|---|---|---|---|---|
| `_medis_egnet` = 1 in any segment | 121 | 96.8 | 599 | 100.0 |
| `_medis_egnet` filled in any segment | 125 | 100.0 | 599 | 100.0 |
| `_medis_finished` = 1 in any segment | 120 | 96.0 | 599 | 100.0 |
| `_medis_finished` filled in any segment | 121 | 96.8 | 599 | 100.0 |

## Plaque type

Not yet run. The updated script adds plaque type per plaque segment (calcified, mostly calcified,
mostly noncalcified, noncalcified, not recorded) and per patient, for the 125 without a tree, the
120 of them with Medis finished, and the 599 with a tree.
