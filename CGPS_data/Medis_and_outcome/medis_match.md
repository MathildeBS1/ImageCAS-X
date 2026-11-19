# Medis centerline trees matched to the visual reads

Output of `CGPS_data/medis_match.py`, run on dtu-gpu-7 on 2026-10-29. Trees are from
`/data/kimbr/HØ_10Y/Medis/Analysis_Processed/centerline_tree`.

Aggregates only; counts 1-4 shown as <5. Match: number in the tree file name = study_id.

| | n |
|---|---|
| tree files | 600 |
| files without a number in the name | 0 |
| distinct IDs | 600 |
| IDs with more than one tree | 0 |
| **IDs matched to the BL sheet** | **600** |
| IDs not in the BL sheet | 0 |
| matched IDs also in the FU sheet | 600 |

Outcome groups of the matched patients, split by `ct_cag_visual_read` (unread BL segments are filled with 'none', so unread scans look plaque-free).

| BL status | outcome | read | not read | total |
|---|---|---|---|---|
| plaque at BL | progressed | 541 | 0 | 541 |
| plaque at BL | stayed / regressed | 58 | 0 | 58 |
| plaque-free at BL | new plaque at FU | <5 | 0 | <5 |
| **plaque at BL** | all | | | **599** |
| **plaque-free at BL** | all | | | **<5** |

Definitions:
- Plaque-free at BL: `ct_cag_sis == 0` and `ct_cag_sss == 0` (new SSS). New plaque at FU: FU SIS or
  SSS > 0, any grade including minimal.
- Plaque at BL: progressed means at least one segment has a higher stenosis grade at FU than at BL;
  stayed / regressed means no segment got worse.

## Notes

- All 600 trees match a `study_id` in both the BL and FU sheets. This settles the earlier question
  of whether ~400 trees failed to match: none did.
- All matched scans were read at BL.
- The Medis trees are effectively a diseased-patient reference. Almost every one comes from a patient
  with plaque at BL, so the trees cannot be used for the clean-baseline "who"/"where" outcome. They
  can be used to validate the tracer's geometry, and to study progression in patients who already
  have plaque.
- There are no "never plaque" or "no FU values" rows: no matched patient falls into either group.

## Where the 541 progressed patients progressed

All 2,476 segments (of the 17) with a higher grade at FU than at BL in these patients, split by
segment: the 9 trunk segments one by one, the LM and side branches together. A patient who worsened
in several segments counts once per segment. Figure: `progression_pie.png` (made by
`progression_pie.py`).

| segment | worsened segments | % of all worsened segments |
|---|---|---|
| pLAD | 268 | 10.8 |
| mLAD | 283 | 11.4 |
| dLAD | 174 | 7.0 |
| pCX | 234 | 9.5 |
| mCX | 116 | 4.7 |
| dCX | 51 | 2.1 |
| pRCA | 204 | 8.2 |
| mRCA | 233 | 9.4 |
| dRCA | 184 | 7.4 |
| LM and side branches | 729 | 29.4 |
| total | 2,476 | 100.0 |

The 9 trunk segments hold 1,747 of the 2,476 worsened segments (70.6 %). By artery: LAD trunk
29.3 %, CX trunk 16.2 %, RCA trunk 25.0 %.

## BL plaque patients without a tree (2026-10-31)

The trees do not cover every patient with plaque at BL: 599 of the 724 (82.7 %) have one and 125
do not, although 120 of those 125 have `_medis_finished = 1`. Their plaque location, number of
plaque segments and worst grade match those of the patients with a tree. Details in
`medis_missing_plaque.md`.
