# Segment turning and plaque progression (Medis trees)

Aggregates only; counts 1-4 shown as <5. Outcome = higher visual grade at FU. Medis trees are mostly patients with plaque at baseline: this is progression, not new plaque in a clean cohort.

Segments: 1157 from 189 people; progressed: 374. Left out: 53 without a usable grade or occluded at BL, 332 too short for two T5 angles or without SCORE2 / follow-up.

## 1. Between people: does geometry add to SCORE2 + follow-up (+ position, BL grade)?

Base: position-stratified C 0.613, pooled AUC 0.664. Each row adds one variant.

| variant | OR per SD (95% CI, robust) | robust p | LR p | stratified C | ΔC (95% person bootstrap) | pooled AUC |
|---|---|---|---|---|---|---|
| mean T5 | 0.88 (0.76–1.01) | 0.0636 | 0.0546 | 0.614 | +0.001 (-0.009 to +0.010) | 0.664 |
| 90th pct T5 | 0.86 (0.75–0.99) | 0.0337 | 0.0294 | 0.616 | +0.003 (-0.010 to +0.014) | 0.666 |
| fraction above p75 | 0.88 (0.77–1.01) | 0.0667 | 0.0553 | 0.613 | -0.000 (-0.014 to +0.011) | 0.663 |
| mean T2.5 | 0.85 (0.74–0.99) | 0.032 | 0.0225 | 0.616 | +0.003 (-0.008 to +0.015) | 0.666 |
| mean T10 | 0.89 (0.76–1.04) | 0.154 | 0.137 | 0.611 | -0.003 (-0.011 to +0.007) | 0.664 |
| upstream 20 mm T5 | 0.98 (0.83–1.16) | 0.821 | 0.824 | 0.610 | -0.003 (-0.006 to -0.000) | 0.661 |

Stratified C = pairs of different people at the same position (the fair test); pooled AUC also rewards position. Read the robust p as the test and ΔC as an estimate. Six variants are tested: expect about one p < 0.05 in six by chance alone.

Confusion matrices (call "progresses" above the training-fold progression rate):

| model | TP | FN | FP | TN | sensitivity | specificity |
|---|---|---|---|---|---|---|
| base | 229 | 145 | 291 | 492 | 61% | 63% |
| mean T5 | 235 | 139 | 287 | 496 | 63% | 63% |
| 90th pct T5 | 233 | 141 | 288 | 495 | 62% | 63% |
| fraction above p75 | 228 | 146 | 290 | 493 | 61% | 63% |
| mean T2.5 | 232 | 142 | 285 | 498 | 62% | 64% |
| mean T10 | 230 | 144 | 283 | 500 | 61% | 64% |
| upstream 20 mm T5 | 230 | 144 | 290 | 493 | 61% | 63% |

Figures: progression_roc.png (all models), progression_confusion.png.

## 2. Within one person: does geometry pick the right segment?

**Question.** Take one person. Their segments differ in position, baseline grade and length, and in geometry. Does knowing the geometry help rank *that person's* segments, so the ones that progressed come first? SCORE2 and follow-up time are the same for all of a person's segments, so they play no role here.

**Who counts.** Only people with some but not all segments progressed can be ranked: 135 people.

**How to read the columns.**
- *within-person C*: pick one progressed and one stable segment from the same person; the share of such pairs where the model ranks the progressed one higher. 0.5 = coin flip, 1 = always right.
- *top segment progressed*: share of people whose highest-ranked segment really progressed.
- *top changed / new top progressed / old top progressed*: for how many people adding geometry moved a different segment to the top, and in how many of those the new top vs the old top had progressed. Geometry helps if 'new' is larger than 'old'.
- *p*: does geometry improve the within-person fit (likelihood-ratio test)?

| model | within-person C | vs base | top segment progressed | top changed | new top progressed | old top progressed | p |
|---|---|---|---|---|---|---|---|
| base | 0.714 |  | 63% (85 of 135) |  |  |  |  |
| mean T5 | 0.710 | -0.004 | 63% (85 of 135) | <5 | <5 | <5 | 0.422 |
| 90th pct T5 | 0.714 | +0.000 | 62% (84 of 135) | 7 | <5 | 5 | 0.178 |
| fraction above p75 | 0.714 | +0.000 | 63% (85 of 135) | 0 | 0 | 0 | 0.982 |
| mean T2.5 | 0.709 | -0.005 | 63% (85 of 135) | 7 | 6 | 6 | 0.0828 |
| mean T10 | 0.712 | -0.002 | 62% (84 of 135) | <5 | <5 | <5 | 0.45 |
| upstream 20 mm T5 | 0.711 | -0.003 | 63% (85 of 135) | <5 | <5 | <5 | 0.539 |

**In short:** position, baseline grade and length rank the right segment first for 63% of people (within-person C 0.71). The best geometry variant (90th pct T5) gives C 0.71 (+0.00). Figure: progression_within.png.

## 3. When geometry changes a segment's risk, is it right?

**Question.** Predict each segment's risk twice, out-of-fold: with position + follow-up time only, and with mean T5 added. For most segments geometry barely changes the risk. Look at the 10% it pushed up most and the 10% it pushed down most, and check what actually happened.

**How to read it.** If geometry is right, segments it pushed *up* progress more often than the position + time model expected (observed above the grey bar), and segments it pushed *down* progress less often.

| segments | n | progressed | observed | expected, position + time | expected, + geometry |
|---|---|---|---|---|---|
| geometry raised the risk most (top 10%) | 116 | 39 | 34% | 37% | 40% |
| little change (middle 80%) | 925 | 303 | 33% | 32% | 32% |
| geometry lowered the risk most (bottom 10%) | 116 | 32 | 28% | 34% | 29% |

**In short:** where geometry raised the risk, 34% progressed (position + time expected 37%); where it lowered the risk, 28% progressed (expected 34%): geometry did not consistently move the risk in the right direction. Figure: progression_reclass.png.

## 4. Which segments swapped places in a person's ranking when geometry was added (mean T5)?

Each person's segments are ranked from highest to lowest within-person score (section 2), once without and once with mean T5. A swap is a pair of the person's segments whose order flipped. It is *correct* when the segment moved up progressed and the one moved down did not, *wrong* the other way round, and *neutral* when both progressed or both stayed stable.

Segments whose rank changed: 114 of 1144. Swapped pairs: 67. Figure: progression_swaps_T5.png.

By vessel pair:

| pair | swaps | correct | wrong | neutral |
|---|---|---|---|---|
| LCx <-> RCA | 31 | <5 | hidden | 20 |
| LAD <-> RCA | 10 | <5 | <5 | <5 |
| LCx <-> LCx | 10 | <5 | <5 | 7 |
| LAD <-> LAD | 8 | <5 | <5 | <5 |
| LAD <-> LCx | 7 | 0 | <5 | hidden |
| RCA <-> RCA | <5 | 0 | 0 | <5 |

By segment pair (most frequent 12):

| pair | swaps | correct | wrong | neutral |
|---|---|---|---|---|
| dcx <-> mcx | 9 | <5 | <5 | 6 |
| dcx <-> drca | 8 | 0 | <5 | hidden |
| pcx <-> prca | 8 | <5 | <5 | 5 |
| dlad <-> mrca | 7 | <5 | <5 | <5 |
| mrca <-> pcx | 7 | <5 | <5 | 5 |
| drca <-> mcx | 5 | <5 | 0 | <5 |
| dlad <-> mlad | <5 | 0 | <5 | <5 |
| mcx <-> plad | <5 | 0 | 0 | <5 |
| mcx <-> mrca | <5 | 0 | <5 | 0 |
| dlad <-> plad | <5 | <5 | <5 | <5 |
| dlad <-> mcx | <5 | 0 | <5 | <5 |
| mcx <-> mlad | <5 | 0 | <5 | 0 |

## 5. Segments whose risk mean T5 raised most: was geometry right to raise them?

Segments are sorted by how much adding mean T5 raised their risk (position + time vs + mean T5, out-of-fold). At each level the top k% is taken. *Progressed* = geometry was right to raise the risk; *did not progress* = geometry raised the risk of a segment that stayed stable.

| top | segments | trees | progressed (right) | did not progress (wrong) |
|---|---|---|---|---|
| 5% | 58 | 45 | 17 (29%) | 41 (71%) |
| 10% | 116 | 74 | 39 (34%) | 77 (66%) |
| 15% | 174 | 97 | 63 (36%) | 111 (64%) |
| 20% | 232 | 115 | 81 (35%) | 151 (65%) |
| 25% | 290 | 124 | 92 (32%) | 198 (68%) |
| 30% | 347 | 140 | 114 (33%) | 233 (67%) |

Figure: progression_toplevels_T5.png.

**Only the top 10% (116 segments, 39 progressed):** how the two models classify them (call "progresses" above the training-fold progression rate).

| model | TP | FN | FP | TN | sensitivity | specificity |
|---|---|---|---|---|---|---|
| position + time | 34 | 5 | 45 | 32 | 87% | 42% |
| + mean T5 | 36 | <5 | 53 | 24 | 92% | 31% |

Figure: progression_top10_confusion_T5.png.

## 6. Which segments swapped places in a person's ranking when geometry was added (mean T2.5)?

Each person's segments are ranked from highest to lowest within-person score (section 2), once without and once with mean T2.5. A swap is a pair of the person's segments whose order flipped. It is *correct* when the segment moved up progressed and the one moved down did not, *wrong* the other way round, and *neutral* when both progressed or both stayed stable.

Segments whose rank changed: 243 of 1144. Swapped pairs: 149. Figure: progression_swaps_T2.5.png.

By vessel pair:

| pair | swaps | correct | wrong | neutral |
|---|---|---|---|---|
| LCx <-> RCA | 58 | 10 | 12 | 36 |
| LAD <-> LCx | 27 | <5 | hidden | 18 |
| LAD <-> RCA | 23 | hidden | <5 | hidden |
| LAD <-> LAD | 18 | <5 | <5 | 12 |
| LCx <-> LCx | 17 | <5 | <5 | 13 |
| RCA <-> RCA | 6 | 0 | <5 | hidden |

By segment pair (most frequent 12):

| pair | swaps | correct | wrong | neutral |
|---|---|---|---|---|
| pcx <-> prca | 20 | hidden | <5 | 12 |
| dcx <-> drca | 16 | 0 | 5 | 11 |
| dcx <-> mcx | 16 | <5 | <5 | 12 |
| dlad <-> mrca | 14 | hidden | <5 | 8 |
| mcx <-> plad | 11 | 0 | <5 | hidden |
| mrca <-> pcx | 11 | <5 | <5 | 7 |
| drca <-> mcx | 8 | <5 | 0 | hidden |
| dlad <-> mlad | 8 | <5 | <5 | <5 |
| mrca <-> prca | 6 | 0 | <5 | hidden |
| mlad <-> plad | 5 | 0 | 0 | 5 |
| dlad <-> plad | 5 | <5 | <5 | <5 |
| dlad <-> mcx | 5 | 0 | <5 | <5 |

## 7. Segments whose risk mean T2.5 raised most: was geometry right to raise them?

Segments are sorted by how much adding mean T2.5 raised their risk (position + time vs + mean T2.5, out-of-fold). At each level the top k% is taken. *Progressed* = geometry was right to raise the risk; *did not progress* = geometry raised the risk of a segment that stayed stable.

| top | segments | trees | progressed (right) | did not progress (wrong) |
|---|---|---|---|---|
| 5% | 58 | 47 | 22 (38%) | 36 (62%) |
| 10% | 116 | 74 | 39 (34%) | 77 (66%) |
| 15% | 174 | 102 | 63 (36%) | 111 (64%) |
| 20% | 232 | 119 | 83 (36%) | 149 (64%) |
| 25% | 290 | 133 | 97 (33%) | 193 (67%) |
| 30% | 347 | 150 | 113 (33%) | 234 (67%) |

Figure: progression_toplevels_T2.5.png.

**Only the top 10% (116 segments, 39 progressed):** how the two models classify them (call "progresses" above the training-fold progression rate).

| model | TP | FN | FP | TN | sensitivity | specificity |
|---|---|---|---|---|---|---|
| position + time | 32 | 7 | 45 | 32 | 82% | 42% |
| + mean T2.5 | 36 | <5 | 61 | 16 | 92% | 21% |

Figure: progression_top10_confusion_T2.5.png.

## 8. Is geometry better at predicting some segments than others?

One model per turning scale gives every segment its own turning effect (turning x segment), adjusted for SCORE2, follow-up time, position and BL grade as in section 1. T5 and T2.5 are per-segment values: the turning angles inside that segment's own stretch of the trunk, averaged.

- *OR per SD*: odds of progressing per SD more turning than usual for that segment.
- *AUC within segment*: comparing people at that segment only; base vs + turning (out-of-fold), with the change and a bootstrap interval.
- *Different between segments?*: one test of whether the turning effect varies across the 9 segments (8 df). Read single segments with care: 18 estimates means some will look strong by chance.

mean T5: different between segments? p = 0.619
mean T2.5: different between segments? p = 0.675

| segment | events / segments | scale | OR per SD (95% CI) | p | AUC base | AUC + turning | ΔAUC (95% bootstrap) |
|---|---|---|---|---|---|---|---|
| plad | 54 / 132 | mean T5 | 0.78 (0.54–1.15) | 0.215 | 0.661 | 0.669 | +0.007 (-0.030 to +0.043) |
| plad | 54 / 132 | mean T2.5 | 0.81 (0.56–1.19) | 0.293 | 0.661 | 0.657 | -0.004 (-0.043 to +0.035) |
| mlad | 73 / 148 | mean T5 | 0.88 (0.60–1.28) | 0.499 | 0.588 | 0.592 | +0.004 (-0.017 to +0.023) |
| mlad | 73 / 148 | mean T2.5 | 0.90 (0.60–1.34) | 0.608 | 0.588 | 0.596 | +0.007 (-0.007 to +0.023) |
| dlad | 41 / 140 | mean T5 | 1.12 (0.78–1.63) | 0.537 | 0.677 | 0.672 | -0.005 (-0.028 to +0.021) |
| dlad | 41 / 140 | mean T2.5 | 1.08 (0.75–1.57) | 0.672 | 0.677 | 0.672 | -0.005 (-0.024 to +0.012) |
| pcx | 56 / 141 | mean T5 | 0.85 (0.62–1.17) | 0.315 | 0.646 | 0.620 | -0.025 (-0.061 to +0.002) |
| pcx | 56 / 141 | mean T2.5 | 0.71 (0.52–0.98) | 0.038 | 0.646 | 0.656 | +0.011 (-0.036 to +0.055) |
| mcx | 25 / 112 | mean T5 | 0.63 (0.39–1.01) | 0.056 | 0.486 | 0.526 | +0.040 (-0.048 to +0.131) |
| mcx | 25 / 112 | mean T2.5 | 0.66 (0.43–1.01) | 0.0558 | 0.486 | 0.529 | +0.043 (-0.032 to +0.118) |
| dcx | 21 / 105 | mean T5 | 0.97 (0.65–1.46) | 0.886 | 0.578 | 0.559 | -0.019 (-0.049 to +0.007) |
| dcx | 21 / 105 | mean T2.5 | 0.99 (0.64–1.53) | 0.972 | 0.578 | 0.553 | -0.025 (-0.059 to +0.001) |
| prca | 35 / 100 | mean T5 | 1.17 (0.77–1.78) | 0.463 | 0.645 | 0.629 | -0.016 (-0.062 to +0.024) |
| prca | 35 / 100 | mean T2.5 | 1.09 (0.70–1.69) | 0.704 | 0.645 | 0.628 | -0.017 (-0.043 to +0.008) |
| mrca | 34 / 108 | mean T5 | 0.84 (0.55–1.27) | 0.4 | 0.641 | 0.621 | -0.020 (-0.060 to +0.023) |
| mrca | 34 / 108 | mean T2.5 | 0.71 (0.47–1.06) | 0.0904 | 0.641 | 0.639 | -0.003 (-0.066 to +0.070) |
| drca | 35 / 171 | mean T5 | 0.71 (0.44–1.14) | 0.159 | 0.554 | 0.561 | +0.007 (-0.066 to +0.057) |
| drca | 35 / 171 | mean T2.5 | 0.80 (0.50–1.30) | 0.374 | 0.554 | 0.558 | +0.004 (-0.041 to +0.050) |

Figure: progression_per_segment.png.
