# Is unrefitted SCORE2 an honest 'who' base?

Output of `score2_honesty.py` (full run: 20 CV repeats, 200 bootstrap replicates), run on dtu-gpu-7.

Aggregates only; small counts suppressed as in cgps_stats.py. No geometry is used. Cohort: clean baseline (SIS = 0, new SSS = 0), read at BL, FU read.

## 1. Cohort
Each row keeps the patients of the row above that also meet its condition. The analyses below use the cohort 'clean, read at BL, FU read' (image volume and quality are not required, so the numbers show the ceiling).

| step | patients |
|---|---|
| BL patients | 1801 |
| clean baseline (SIS = SSS = 0) | 1077 |
| ... read at BL (ct_cag_visual_read) | 1077 |
| ... FU segments read | 1076 |
| ... not bad image quality (bad_quality) | 1076 |

## 2. Outcome and complete cases
Outcome: any trunk segment (LAD, CX, RCA proximal/mid/distal) >= minimal at FU. Plaque only in the LM or side branches counts as no plaque.

|  | n |
|---|---|
| people with an outcome | 1076 |
| new trunk plaque | 452 |
| % | 42.0 |
| no trunk plaque, but plaque in LM / side branch (counted 0) | 31 |
| no trunk plaque, >= 1 trunk segment unevaluable | 40 |
| missing log_fu | 0 |
| missing score2_cll | 35 |
| missing age | 0 |
| missing male | 0 |
| missing smoking | 0 |
| missing sbp | 12 |
| missing tot_chol | 22 |
| missing hdl | 22 |
| missing diabetes | 0 |
| complete cases (used by every model) | 1041 |

SCORE2 risk in the complete cases: median 0.026 (as a fraction); new plaque 433/1041 (41.6%).

## 3. Discrimination and calibration
Out-of-fold values are means over 20 repeats of person-split, outcome-stratified 5-fold CV. Calibration slope 1 and intercept 0 are perfect; a slope below 1 means the predictions are too extreme (overfitting). Apparent C uses the same rows it was fitted on.

| model | parameters | apparent C | OOF C | calibration intercept | calibration slope | Brier | log-loss |
|---|---|---|---|---|---|---|---|
| follow-up only | 2 | 0.571 | 0.560 | -0.001 | 0.909 | 0.2403 | 0.6735 |
| age + sex | 4 | 0.666 | 0.660 | -0.003 | 0.949 | 0.2256 | 0.6429 |
| SCORE2 recalibrated | 3 | 0.689 | 0.687 | -0.002 | 0.972 | 0.2193 | 0.6284 |
| SCORE2 + age + sex | 5 | 0.693 | 0.687 | -0.004 | 0.949 | 0.2193 | 0.6288 |
| refitted SCORE2 factors | 9 | 0.699 | 0.686 | -0.018 | 0.866 | 0.2202 | 0.6346 |

## 4. SCORE2 slope
Slope of plaque cloglog on cloglog(SCORE2 risk). Both are log cumulative hazards, so slope 1 means SCORE2 ranks plaque hazard on the same scale as CVD hazard; below 1, SCORE2 spreads people more than their plaque risk differs.

|  | estimate | 95 % Wald interval |
|---|---|---|
| SCORE2 slope | 0.722 | 0.569 to 0.874 |

Refitted factors: hazard ratio per SD of each term (0/1 terms are standardised too, so the weights can be compared). Compare the age weight with SCORE2's, which is built for CVD.

| term | HR per SD | 95 % Wald interval |
|---|---|---|
| log_fu | 1.19 | 1.08 to 1.31 |
| age | 1.32 | 1.19 to 1.46 |
| male | 1.25 | 1.12 to 1.39 |
| smoking | 1.14 | 1.04 to 1.25 |
| sbp | 1.22 | 1.11 to 1.35 |
| tot_chol | 1.09 | 0.98 to 1.20 |
| hdl | 0.86 | 0.77 to 0.96 |
| diabetes | 1.03 | 0.94 to 1.12 |

## 5. Delta C (estimated, not tested)
Point estimate: difference of the mean OOF C in section 3. Interval: 2.5th-97.5th percentile over 200 person-bootstrap replicates with the CV redone inside each (approximate).

| comparison | delta C | 95 % bootstrap interval |
|---|---|---|
| refitted SCORE2 factors - SCORE2 recalibrated | -0.001 | -0.025 to 0.004 |
| SCORE2 + age + sex - SCORE2 recalibrated | -0.000 | -0.013 to 0.009 |
| SCORE2 recalibrated - age + sex | 0.027 | 0.008 to 0.048 |

Prespecified rule: refit - SCORE2 delta C -0.001 < 0.02, so the primary 'who' base is **SCORE2 recalibrated**. Either way, report the geometry increment over the other base as a sensitivity analysis.

## 6. Observed vs predicted by fifth of OOF risk
Predicted: mean OOF risk (averaged over the CV repeats) in each fifth; observed: events/people.

**SCORE2 recalibrated**

| fifth | mean predicted | observed |
|---|---|---|
| 1 | 0.215 | 39/209 (18.7%) |
| 2 | 0.320 | 65/208 (31.2%) |
| 3 | 0.402 | 85/208 (40.9%) |
| 4 | 0.494 | 119/208 (57.2%) |
| 5 | 0.645 | 125/208 (60.1%) |

**refitted SCORE2 factors**

| fifth | mean predicted | observed |
|---|---|---|
| 1 | 0.218 | 41/209 (19.6%) |
| 2 | 0.312 | 63/208 (30.3%) |
| 3 | 0.399 | 92/208 (44.2%) |
| 4 | 0.488 | 104/208 (50.0%) |
| 5 | 0.661 | 133/208 (63.9%) |
