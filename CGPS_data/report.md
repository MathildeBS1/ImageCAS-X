# CGPS outcome statistics

Aggregates only. Counts 1-4 are shown as <5. Per-column summaries are in columns_bl.csv / columns_fu.csv, value counts in stats.json.

## settings

| | |
|---|---|
| MIN_CELL | 5 |
| MAX_LEVELS | 20 |
| NO_PLAQUE | [0] |
| dayfirst | True |

## 1. Cohort and follow-up

### patients

| | |
|---|---|
| BL rows | 2116 |
| FU rows | 2116 |
| duplicate study_id in BL (dropped, first kept) | 0 |
| duplicate study_id in FU (dropped, first kept) | 0 |
| in both BL and FU (paired) | 2116 |
| BL only | 0 |
| FU only | 0 |
| BL columns | 212 |
| FU columns | 276 |

### follow-up interval (years, paired)

| | |
|---|---|
| n | 2116 |
| mean | 11 |
| sd | 1.84 |
| p5 | 9.52 |
| p25 | 9.65 |
| median | 10 |
| p75 | 12.2 |
| p95 | 15.3 |

### follow-up interval checks

| | |
|---|---|
| paired with interval | 2116 |
| interval missing/unparsed | 0 |
| interval <= 0 | 0 |
| interval < 1 year | 0 |
| interval >= 5 years | 2116 |

## 2. Outcome feasibility (events and events-per-variable)

### binary outcomes

| | n | events | pct | max predictors at 10 EPV | max predictors at 20 EPV |
|---|---|---|---|---|---|
| incident_cac (BL=0 -> FU>0) | 1261 | 478 | 37.9 | 47 | 23 |
| cac_any_increase | 2109 | 1274 | 60.4 | 83 | 41 |
| cac_progression_hokanson (dsqrt >= 2.5) | 2109 | 1053 | 49.9 | 105 | 52 |
| cac_annual_change_ge_15pct (BL>0) | 848 | 305 | 36 | 30 | 15 |
| cac_decrease (data check) | 2109 | 49 | 2.3 | 4 | 2 |
| sss_increase | 2116 | 1254 | 59.3 | 86 | 43 |
| sss_increase_ge2 | 2116 | 1022 | 48.3 | 102 | 51 |
| sis_increase | 2116 | 1220 | 57.7 | 89 | 44 |
| plaque_type_score_change | 2116 | 1369 | 64.7 | 74 | 37 |
| any segment stenosis progression | 1020 | 810 | 79.4 | 21 | 10 |
| any new plaque | 1020 | 777 | 76.2 | 24 | 12 |
| any new high-risk feature | 763 | 151 | 19.8 | 15 | 7 |
| no plaque -> plaque (SIS, among 'no plaque ->') | 1352 | 668 | 49.4 | 66 | 33 |
| plaque -> more (SIS, among 'plaque ->') | 764 | 552 | 72.3 | 21 | 10 |
| plaque -> less (SIS, among 'plaque ->') | 764 | 107 | 14 | 10 | 5 |
| incident_obstructive_cad | 876 | 285 | 32.5 | 28 | 14 |
| worst_category_worsened | 1020 | 532 | 52.2 | 48 | 24 |
| incident demo_hist_myocardial_infarction | 1028 | 6 | 0.6 | 0 | 0 |
| incident demo_hist_coronary_revasc | 1028 | 6 | 0.6 | 0 | 0 |
| incident demo_hist_stroke_tia | 891 | 31 | 3.5 | 3 | 1 |
| incident hist_angina | 2108 | 96 | 4.6 | 9 | 4 |
| incident hist_diabetes | 2071 | 61 | 2.9 | 6 | 3 |
| incident ct_cag_stent | 699 | <5 | <5 | 0 | 0 |
| incident ct_cag_cabg | 1835 | 0 | 0 | 0 | 0 |
| incident hard composite (MI/revasc/stent/CABG) | 1973 | 10 | 0.5 | 1 | 0 |

### continuous outcomes (n available)

| | |
|---|---|
| delta_cac | 2109 |
| delta_cac_per_year | 2109 |
| delta_sqrt_cac | 2109 |
| delta_log1p_cac | 2109 |
| delta_sis | 2116 |
| delta_sss | 2116 |
| delta_plaque_type_score | 2116 |
| delta_lad_sis | 2116 |
| delta_lad_sss | 2116 |
| delta_lad_plaque_type_score | 2116 |
| delta_cx_sis | 2116 |
| delta_cx_sss | 2116 |
| delta_cx_plaque_type_score | 2116 |
| delta_rca_sis | 2116 |
| delta_rca_sss | 2116 |
| delta_rca_plaque_type_score | 2116 |
| delta_sss_per_year | 2116 |
| n_segments_new_plaque | 1020 |

### BL predictors (paired patients)

| | |
|---|---|
| predictors present | 25 |
| predictors absent | none |
| complete cases on all present predictors | 0 |
| predictors with >= 20% missing | clin_bmi, hr_during_scan, hba1c, hist_smoking_years |
| complete cases on predictors with < 20% missing | 1974 |

#### missing per predictor

| | |
|---|---|
| male | 0 |
| scan_age | 0 |
| clin_bmi | 1085 |
| clin_bp_sys_mean | 26 |
| clin_bp_dia_mean | 32 |
| hr_during_scan | 1881 |
| creatinine | 39 |
| egfr | 39 |
| hba1c | 1125 |
| tot_cholesterol | 38 |
| hdl | 38 |
| ldl | 33 |
| triglyceride | 38 |
| hist_smoking_current | 0 |
| hist_smoking_former | 0 |
| hist_smoking_years | 1009 |
| hist_diabetes | 5 |
| demo_hist_family_cvd | 12 |
| demo_hist_family_hypercholesterolemia | 8 |
| med_lipid_lowering_any | 50 |
| med_antihypertensive_any | 51 |
| ct_cacs_sum | 7 |
| ct_cag_sis | 0 |
| ct_cag_sss | 0 |
| ct_cag_plaque_type_score | 0 |

## 3. Coronary calcium (CAC) progression

### total CAC

| | n | mean | sd | p5 | p25 | median | p75 | p95 |
|---|---|---|---|---|---|---|---|---|
| BL | 2109 | 68.7 | 239 | 0 | 0 | 0 | 28 | 398 |
| FU | 2116 | 190 | 463 | 0 | 0 | 15 | 153 | 1.03e+03 |

### CAC = 0

| | n | events | pct |
|---|---|---|---|
| BL | 2109 | 1261 | 59.8 |
| FU | 2116 | 805 | 38 |

### CAC BL category -> FU category

| | 0 | 1-10 | 11-100 | 101-400 | >400 |
|---|---|---|---|---|---|
| 0 | 783 | 172 | 257 | 41 | 8 |
| 1-10 | hidden | 21 | 104 | 41 | hidden |
| 11-100 | <5 | <5 | 104 | 201 | 42 |
| 101-400 | 0 | 0 | <5 | hidden | 126 |
| >400 | <5 | 0 | 0 | 0 | hidden |
| missing | <5 | <5 | <5 | <5 | 0 |

### ct_cacs_groups BL -> FU

| | 1 | 2 | 3 | missing |
|---|---|---|---|---|
| 1 | 779 | hidden | hidden | <5 |
| 2 | hidden | 480 | 211 | <5 |
| 3 | <5 | 0 | hidden | 0 |
| missing | <5 | hidden | 0 | 0 |

### change

| | n | mean | sd | p5 | p25 | median | p75 | p95 |
|---|---|---|---|---|---|---|---|---|
| delta_cac | 2109 | 122 | 295 | 0 | 0 | 12 | 113 | 603 |
| delta_cac_per_year | 2109 | 10.9 | 25.8 | 0 | 0 | 1.06 | 10.4 | 57.5 |
| delta_sqrt_cac | 2109 | 4.29 | 5.76 | 0 | 0 | 2.46 | 6.93 | 14.9 |
| delta_log1p_cac | 2109 | 1.19 | 1.46 | 0 | 0 | 0.73 | 2.03 | 4.11 |

### change among BL CAC > 0

| | n | mean | sd | p5 | p25 | median | p75 | p95 |
|---|---|---|---|---|---|---|---|---|
| delta_cac_per_year | 848 | 24.5 | 34.9 | -0.168 | 4.86 | 13.2 | 32.1 | 86.2 |
| delta_sqrt_cac | 848 | 7.62 | 6.34 | -0.422 | 3.53 | 6.77 | 10.9 | 18.2 |

### per vessel

#### lm

| | n | events | pct |
|---|---|---|---|
| BL > 0 | 2109 | 203 | 9.6 |
| FU > 0 | 2114 | 480 | 22.7 |
| increase | 2107 | 438 | 20.8 |
| new (0 -> >0) | 1904 | 315 | 16.5 |

#### lad

| | n | events | pct |
|---|---|---|---|
| BL > 0 | 2109 | 721 | 34.2 |
| FU > 0 | 2112 | 1186 | 56.2 |
| increase | 2105 | 1138 | 54.1 |
| new (0 -> >0) | 1384 | 475 | 34.3 |

#### cx

| | n | events | pct |
|---|---|---|---|
| BL > 0 | 2109 | 309 | 14.7 |
| FU > 0 | 2114 | 674 | 31.9 |
| increase | 2107 | 648 | 30.8 |
| new (0 -> >0) | 1798 | 382 | 21.2 |

#### rca

| | n | events | pct |
|---|---|---|---|
| BL > 0 | 2109 | 385 | 18.3 |
| FU > 0 | 2114 | 723 | 34.2 |
| increase | 2107 | 706 | 33.5 |
| new (0 -> >0) | 1723 | 368 | 21.4 |

## 4. Segment involvement / stenosis / plaque-type scores

### sis

#### BL

| | |
|---|---|
| n | 2116 |
| mean | 1.22 |
| sd | 2.14 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 2 |
| p95 | 6 |

#### FU

| | |
|---|---|
| n | 2116 |
| mean | 2.98 |
| sd | 3.33 |
| p5 | 0 |
| p25 | 0 |
| median | 2 |
| p75 | 5 |
| p95 | 10 |

#### delta

| | |
|---|---|
| n | 2116 |
| mean | 1.76 |
| sd | 2.48 |
| p5 | -1 |
| p25 | 0 |
| median | 1 |
| p75 | 3 |
| p95 | 7 |

#### delta value counts

| | |
|---|---|
| -5 | <5 |
| -4 | hidden |
| -3 | 10 |
| -2 | 33 |
| -1 | 56 |
| 0 | 789 |
| 1 | 337 |
| 2 | 262 |
| 3 | 200 |
| 4 | 138 |
| 5 | 87 |
| 6 | 70 |
| 7 | 47 |
| 8 | 39 |
| 9 | 14 |
| 10 | 26 |

#### increase (delta > 0)

| | |
|---|---|
| n | 2116 |
| events | 1220 |
| pct | 57.7 |

#### delta >= 2

| | |
|---|---|
| n | 2116 |
| events | 883 |
| pct | 41.7 |

#### decrease (delta < 0)

| | |
|---|---|
| n | 2116 |
| events | 107 |
| pct | 5.1 |

#### BL = 0

| | |
|---|---|
| n | 2116 |
| events | 1352 |
| pct | 63.9 |

#### FU = 0

| | |
|---|---|
| n | 2116 |
| events | 725 |
| pct | 34.3 |

### sss

#### BL

| | |
|---|---|
| n | 2116 |
| mean | 1.93 |
| sd | 3.87 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 2 |
| p95 | 10 |

#### FU

| | |
|---|---|
| n | 2116 |
| mean | 5.19 |
| sd | 6.93 |
| p5 | 0 |
| p25 | 0 |
| median | 2 |
| p75 | 8 |
| p95 | 20 |

#### delta

| | |
|---|---|
| n | 2116 |
| mean | 3.26 |
| sd | 5.14 |
| p5 | -1 |
| p25 | 0 |
| median | 1 |
| p75 | 5 |
| p95 | 14 |

#### delta value counts

| | |
|---|---|
| -5 | 15 |
| -4 | 9 |
| -3 | 11 |
| -2 | 36 |
| -1 | 49 |
| 0 | 742 |
| 1 | 232 |
| 2 | 197 |
| 3 | 147 |
| 4 | 122 |
| 5 | 71 |
| 6 | 84 |
| 7 | 61 |
| 8 | 55 |
| 9 | 43 |
| 10 | 242 |

#### increase (delta > 0)

| | |
|---|---|
| n | 2116 |
| events | 1254 |
| pct | 59.3 |

#### delta >= 2

| | |
|---|---|
| n | 2116 |
| events | 1022 |
| pct | 48.3 |

#### decrease (delta < 0)

| | |
|---|---|
| n | 2116 |
| events | 120 |
| pct | 5.7 |

#### BL = 0

| | |
|---|---|
| n | 2116 |
| events | 1352 |
| pct | 63.9 |

#### FU = 0

| | |
|---|---|
| n | 2116 |
| events | 725 |
| pct | 34.3 |

#### delta per year

| | |
|---|---|
| n | 2116 |
| mean | 0.297 |
| sd | 0.471 |
| p5 | -0.0929 |
| p25 | 0 |
| median | 0.104 |
| p75 | 0.421 |
| p95 | 1.26 |

### plaque_type_score

#### BL

| | |
|---|---|
| n | 2116 |
| mean | 2.49 |
| sd | 4.39 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 4 |
| p95 | 12 |

#### FU

| | |
|---|---|
| n | 2116 |
| mean | 4.46 |
| sd | 5.31 |
| p5 | 0 |
| p25 | 0 |
| median | 2 |
| p75 | 7 |
| p95 | 15 |

#### delta

| | |
|---|---|
| n | 2116 |
| mean | 1.98 |
| sd | 4.47 |
| p5 | -4 |
| p25 | 0 |
| median | 1 |
| p75 | 4 |
| p95 | 11 |

#### delta value counts

| | |
|---|---|
| -5 | 92 |
| -4 | 35 |
| -3 | 49 |
| -2 | 45 |
| -1 | 69 |
| 0 | 747 |
| 1 | 196 |
| 2 | 180 |
| 3 | 155 |
| 4 | 109 |
| 5 | 86 |
| 6 | 71 |
| 7 | 61 |
| 8 | 51 |
| 9 | 36 |
| 10 | 134 |

#### increase (delta > 0)

| | |
|---|---|
| n | 2116 |
| events | 1079 |
| pct | 51 |

#### delta >= 2

| | |
|---|---|
| n | 2116 |
| events | 883 |
| pct | 41.7 |

#### decrease (delta < 0)

| | |
|---|---|
| n | 2116 |
| events | 290 |
| pct | 13.7 |

#### BL = 0

| | |
|---|---|
| n | 2116 |
| events | 1352 |
| pct | 63.9 |

#### FU = 0

| | |
|---|---|
| n | 2116 |
| events | 728 |
| pct | 34.4 |

### lad_sis

#### BL

| | |
|---|---|
| n | 2116 |
| mean | 0.775 |
| sd | 1.27 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 1 |
| p95 | 4 |

#### FU

| | |
|---|---|
| n | 2116 |
| mean | 1.56 |
| sd | 1.6 |
| p5 | 0 |
| p25 | 0 |
| median | 1 |
| p75 | 3 |
| p95 | 5 |

#### delta

| | |
|---|---|
| n | 2116 |
| mean | 0.781 |
| sd | 1.27 |
| p5 | -1 |
| p25 | 0 |
| median | 0 |
| p75 | 1 |
| p95 | 3 |

#### delta value counts

| | |
|---|---|
| -4 | <5 |
| -3 | 5 |
| -2 | 29 |
| -1 | 102 |
| 0 | 977 |
| 1 | 494 |
| 2 | 300 |
| 3 | 120 |
| 4 | 66 |
| 5 | 18 |
| 6 | <5 |

#### increase (delta > 0)

| | |
|---|---|
| n | 2116 |
| events | 1002 |
| pct | 47.4 |

#### delta >= 2

| | |
|---|---|
| n | 2116 |
| events | 508 |
| pct | 24 |

#### decrease (delta < 0)

| | |
|---|---|
| n | 2116 |
| events | 137 |
| pct | 6.5 |

#### BL = 0

| | |
|---|---|
| n | 2116 |
| events | 1387 |
| pct | 65.5 |

#### FU = 0

| | |
|---|---|
| n | 2116 |
| events | 812 |
| pct | 38.4 |

### lad_sss

#### BL

| | |
|---|---|
| n | 2116 |
| mean | 1.25 |
| sd | 2.27 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 2 |
| p95 | 6 |

#### FU

| | |
|---|---|
| n | 2116 |
| mean | 2.81 |
| sd | 3.52 |
| p5 | 0 |
| p25 | 0 |
| median | 2 |
| p75 | 5 |
| p95 | 10 |

#### delta

| | |
|---|---|
| n | 2116 |
| mean | 1.57 |
| sd | 2.67 |
| p5 | -1 |
| p25 | 0 |
| median | 1 |
| p75 | 3 |
| p95 | 7 |

#### delta value counts

| | |
|---|---|
| -5 | 10 |
| -4 | 6 |
| -3 | 15 |
| -2 | 50 |
| -1 | 68 |
| 0 | 860 |
| 1 | 323 |
| 2 | 252 |
| 3 | 157 |
| 4 | 126 |
| 5 | 74 |
| 6 | 46 |
| 7 | 47 |
| 8 | 20 |
| 9 | 21 |
| 10 | 41 |

#### increase (delta > 0)

| | |
|---|---|
| n | 2116 |
| events | 1107 |
| pct | 52.3 |

#### delta >= 2

| | |
|---|---|
| n | 2116 |
| events | 784 |
| pct | 37.1 |

#### decrease (delta < 0)

| | |
|---|---|
| n | 2116 |
| events | 149 |
| pct | 7 |

#### BL = 0

| | |
|---|---|
| n | 2116 |
| events | 1387 |
| pct | 65.5 |

#### FU = 0

| | |
|---|---|
| n | 2116 |
| events | 812 |
| pct | 38.4 |

### lad_plaque_type_score

#### BL

| | |
|---|---|
| n | 2116 |
| mean | 1.62 |
| sd | 2.74 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 3 |
| p95 | 8 |

#### FU

| | |
|---|---|
| n | 2116 |
| mean | 2.34 |
| sd | 2.61 |
| p5 | 0 |
| p25 | 0 |
| median | 2 |
| p75 | 4 |
| p95 | 8 |

#### delta

| | |
|---|---|
| n | 2116 |
| mean | 0.717 |
| sd | 2.61 |
| p5 | -4 |
| p25 | 0 |
| median | 0 |
| p75 | 2 |
| p95 | 5 |

#### delta value counts

| | |
|---|---|
| -5 | 71 |
| -4 | 37 |
| -3 | 71 |
| -2 | 82 |
| -1 | 99 |
| 0 | 864 |
| 1 | 265 |
| 2 | 234 |
| 3 | 119 |
| 4 | 109 |
| 5 | 70 |
| 6 | 38 |
| 7 | 20 |
| 8 | 17 |
| 9 | 11 |
| 10 | 9 |

#### increase (delta > 0)

| | |
|---|---|
| n | 2116 |
| events | 892 |
| pct | 42.2 |

#### delta >= 2

| | |
|---|---|
| n | 2116 |
| events | 627 |
| pct | 29.6 |

#### decrease (delta < 0)

| | |
|---|---|
| n | 2116 |
| events | 360 |
| pct | 17 |

#### BL = 0

| | |
|---|---|
| n | 2116 |
| events | 1387 |
| pct | 65.5 |

#### FU = 0

| | |
|---|---|
| n | 2116 |
| events | 815 |
| pct | 38.5 |

### cx_sis

#### BL

| | |
|---|---|
| n | 2116 |
| mean | 0.198 |
| sd | 0.587 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 0 |
| p95 | 1 |

#### FU

| | |
|---|---|
| n | 2116 |
| mean | 0.617 |
| sd | 0.989 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 1 |
| p95 | 3 |

#### delta

| | |
|---|---|
| n | 2116 |
| mean | 0.42 |
| sd | 0.865 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 1 |
| p95 | 2 |

#### delta value counts

| | |
|---|---|
| -5 | <5 |
| -2 | 9 |
| -1 | 50 |
| 0 | 1430 |
| 1 | 381 |
| 2 | 170 |
| 3 | 61 |
| 4 | 13 |
| 5 | <5 |

#### increase (delta > 0)

| | |
|---|---|
| n | 2116 |
| events | 626 |
| pct | 29.6 |

#### delta >= 2

| | |
|---|---|
| n | 2116 |
| events | 245 |
| pct | 11.6 |

#### decrease (delta < 0)

| | |
|---|---|
| n | 2116 |
| events | 60 |
| pct | 2.8 |

#### BL = 0

| | |
|---|---|
| n | 2116 |
| events | 1835 |
| pct | 86.7 |

#### FU = 0

| | |
|---|---|
| n | 2116 |
| events | 1364 |
| pct | 64.5 |

### cx_sss

#### BL

| | |
|---|---|
| n | 2116 |
| mean | 0.308 |
| sd | 1.06 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 0 |
| p95 | 2 |

#### FU

| | |
|---|---|
| n | 2116 |
| mean | 1.02 |
| sd | 1.92 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 1 |
| p95 | 5 |

#### delta

| | |
|---|---|
| n | 2116 |
| mean | 0.714 |
| sd | 1.62 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 1 |
| p95 | 4 |

#### delta value counts

| | |
|---|---|
| -5 | <5 |
| -4 | 6 |
| -3 | hidden |
| -2 | 16 |
| -1 | 41 |
| 0 | 1387 |
| 1 | 260 |
| 2 | 164 |
| 3 | 92 |
| 4 | 60 |
| 5 | 29 |
| 6 | 25 |
| 7 | 15 |
| 8 | 8 |
| 10 | 6 |

#### increase (delta > 0)

| | |
|---|---|
| n | 2116 |
| events | 659 |
| pct | 31.1 |

#### delta >= 2

| | |
|---|---|
| n | 2116 |
| events | 399 |
| pct | 18.9 |

#### decrease (delta < 0)

| | |
|---|---|
| n | 2116 |
| events | 70 |
| pct | 3.3 |

#### BL = 0

| | |
|---|---|
| n | 2116 |
| events | 1835 |
| pct | 86.7 |

#### FU = 0

| | |
|---|---|
| n | 2116 |
| events | 1364 |
| pct | 64.5 |

### cx_plaque_type_score

#### BL

| | |
|---|---|
| n | 2116 |
| mean | 0.378 |
| sd | 1.17 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 0 |
| p95 | 3 |

#### FU

| | |
|---|---|
| n | 2116 |
| mean | 0.881 |
| sd | 1.53 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 1 |
| p95 | 4 |

#### delta

| | |
|---|---|
| n | 2116 |
| mean | 0.504 |
| sd | 1.48 |
| p5 | -1 |
| p25 | 0 |
| median | 0 |
| p75 | 1 |
| p95 | 3 |

#### delta value counts

| | |
|---|---|
| -5 | 10 |
| -4 | <5 |
| -3 | 28 |
| -2 | 34 |
| -1 | 50 |
| 0 | 1390 |
| 1 | 231 |
| 2 | 186 |
| 3 | 93 |
| 4 | 44 |
| 5 | 18 |
| 6 | 20 |
| 7 | 8 |
| 8 | <5 |

#### increase (delta > 0)

| | |
|---|---|
| n | 2116 |
| events | 602 |
| pct | 28.4 |

#### delta >= 2

| | |
|---|---|
| n | 2116 |
| events | 371 |
| pct | 17.5 |

#### decrease (delta < 0)

| | |
|---|---|
| n | 2116 |
| events | 124 |
| pct | 5.9 |

#### BL = 0

| | |
|---|---|
| n | 2116 |
| events | 1837 |
| pct | 86.8 |

#### FU = 0

| | |
|---|---|
| n | 2116 |
| events | 1365 |
| pct | 64.5 |

### rca_sis

#### BL

| | |
|---|---|
| n | 2116 |
| mean | 0.246 |
| sd | 0.683 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 0 |
| p95 | 2 |

#### FU

| | |
|---|---|
| n | 2116 |
| mean | 0.806 |
| sd | 1.24 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 1 |
| p95 | 4 |

#### delta

| | |
|---|---|
| n | 2116 |
| mean | 0.559 |
| sd | 1.03 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 1 |
| p95 | 3 |

#### delta value counts

| | |
|---|---|
| -3 | <5 |
| -2 | 11 |
| -1 | 36 |
| 0 | 1358 |
| 1 | 355 |
| 2 | 225 |
| 3 | 78 |
| 4 | 46 |
| 5 | hidden |

#### increase (delta > 0)

| | |
|---|---|
| n | 2116 |
| events | 709 |
| pct | 33.5 |

#### delta >= 2

| | |
|---|---|
| n | 2116 |
| events | 354 |
| pct | 16.7 |

#### decrease (delta < 0)

| | |
|---|---|
| n | 2116 |
| events | 49 |
| pct | 2.3 |

#### BL = 0

| | |
|---|---|
| n | 2116 |
| events | 1802 |
| pct | 85.2 |

#### FU = 0

| | |
|---|---|
| n | 2116 |
| events | 1304 |
| pct | 61.6 |

### rca_sss

#### BL

| | |
|---|---|
| n | 2116 |
| mean | 0.377 |
| sd | 1.24 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 0 |
| p95 | 2 |

#### FU

| | |
|---|---|
| n | 2116 |
| mean | 1.36 |
| sd | 2.44 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 2 |
| p95 | 6 |

#### delta

| | |
|---|---|
| n | 2116 |
| mean | 0.979 |
| sd | 2.04 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 1 |
| p95 | 5 |

#### delta value counts

| | |
|---|---|
| -5 | hidden |
| -4 | <5 |
| -3 | 7 |
| -2 | 12 |
| -1 | 31 |
| 0 | 1308 |
| 1 | 248 |
| 2 | 160 |
| 3 | 125 |
| 4 | 82 |
| 5 | 43 |
| 6 | 34 |
| 7 | 23 |
| 8 | 9 |
| 9 | 14 |
| 10 | 13 |

#### increase (delta > 0)

| | |
|---|---|
| n | 2116 |
| events | 751 |
| pct | 35.5 |

#### delta >= 2

| | |
|---|---|
| n | 2116 |
| events | 503 |
| pct | 23.8 |

#### decrease (delta < 0)

| | |
|---|---|
| n | 2116 |
| events | 57 |
| pct | 2.7 |

#### BL = 0

| | |
|---|---|
| n | 2116 |
| events | 1802 |
| pct | 85.2 |

#### FU = 0

| | |
|---|---|
| n | 2116 |
| events | 1304 |
| pct | 61.6 |

### rca_plaque_type_score

#### BL

| | |
|---|---|
| n | 2116 |
| mean | 0.484 |
| sd | 1.37 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 0 |
| p95 | 4 |

#### FU

| | |
|---|---|
| n | 2116 |
| mean | 1.24 |
| sd | 2.04 |
| p5 | 0 |
| p25 | 0 |
| median | 0 |
| p75 | 2 |
| p95 | 6 |

#### delta

| | |
|---|---|
| n | 2116 |
| mean | 0.757 |
| sd | 1.8 |
| p5 | -1 |
| p25 | 0 |
| median | 0 |
| p75 | 1 |
| p95 | 4 |

#### delta value counts

| | |
|---|---|
| -5 | 8 |
| -4 | 10 |
| -3 | 25 |
| -2 | 30 |
| -1 | 45 |
| 0 | 1315 |
| 1 | 209 |
| 2 | 164 |
| 3 | 121 |
| 4 | 86 |
| 5 | 43 |
| 6 | 33 |
| 7 | 12 |
| 8 | 10 |
| 9 | <5 |
| 10 | <5 |

#### increase (delta > 0)

| | |
|---|---|
| n | 2116 |
| events | 683 |
| pct | 32.3 |

#### delta >= 2

| | |
|---|---|
| n | 2116 |
| events | 474 |
| pct | 22.4 |

#### decrease (delta < 0)

| | |
|---|---|
| n | 2116 |
| events | 118 |
| pct | 5.6 |

#### BL = 0

| | |
|---|---|
| n | 2116 |
| events | 1802 |
| pct | 85.2 |

#### FU = 0

| | |
|---|---|
| n | 2116 |
| events | 1304 |
| pct | 61.6 |

## 5. Segment-level stenosis, plaque and high-risk features

### text labels decoded (BL)

#### ct_cag_lm_stenosis

| | |
|---|---|
| recognised | 1012 |
| unevaluable (uneval_*) | 10 |
| unrecognised label | 0 |
| empty | 1094 |

#### ct_cag_lm_plaque_type

| | |
|---|---|
| recognised | 207 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 805 |
| plaque, type not recorded | 0 |
| empty | 1104 |

#### ct_cag_plad_stenosis

| | |
|---|---|
| recognised | 1019 |
| unevaluable (uneval_*) | <5 |
| unrecognised label | 0 |
| empty | 1094 |

#### ct_cag_plad_plaque_type

| | |
|---|---|
| recognised | 571 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 448 |
| plaque, type not recorded | 0 |
| empty | 1097 |

#### ct_cag_mlad_stenosis

| | |
|---|---|
| recognised | 1011 |
| unevaluable (uneval_*) | 11 |
| unrecognised label | 0 |
| empty | 1094 |

#### ct_cag_mlad_plaque_type

| | |
|---|---|
| recognised | 462 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 549 |
| plaque, type not recorded | 0 |
| empty | 1105 |

#### ct_cag_dlad_stenosis

| | |
|---|---|
| recognised | 1017 |
| unevaluable (uneval_*) | 5 |
| unrecognised label | 0 |
| empty | 1094 |

#### ct_cag_dlad_plaque_type

| | |
|---|---|
| recognised | 183 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 834 |
| plaque, type not recorded | 0 |
| empty | 1099 |

#### ct_cag_d1_stenosis

| | |
|---|---|
| recognised | 1007 |
| unevaluable (uneval_*) | 15 |
| unrecognised label | 0 |
| empty | 1094 |

#### ct_cag_d1_plaque_type

| | |
|---|---|
| recognised | 141 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 866 |
| plaque, type not recorded | 0 |
| empty | 1109 |

#### ct_cag_d2_stenosis

| | |
|---|---|
| recognised | 950 |
| unevaluable (uneval_*) | 72 |
| unrecognised label | 0 |
| empty | 1094 |

#### ct_cag_d2_plaque_type

| | |
|---|---|
| recognised | 75 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 875 |
| plaque, type not recorded | 0 |
| empty | 1166 |

#### ct_cag_im_stenosis

| | |
|---|---|
| recognised | 339 |
| unevaluable (uneval_*) | 1482 |
| unrecognised label | 0 |
| empty | 295 |

#### ct_cag_im_plaque_type

| | |
|---|---|
| recognised | 38 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 301 |
| plaque, type not recorded | 0 |
| empty | 1777 |

#### ct_cag_pcx_stenosis

| | |
|---|---|
| recognised | 1012 |
| unevaluable (uneval_*) | 10 |
| unrecognised label | 0 |
| empty | 1094 |

#### ct_cag_pcx_plaque_type

| | |
|---|---|
| recognised | 156 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 855 |
| plaque, type not recorded | <5 |
| empty | 1104 |

#### ct_cag_om1_stenosis

| | |
|---|---|
| recognised | 1012 |
| unevaluable (uneval_*) | 10 |
| unrecognised label | 0 |
| empty | 1094 |

#### ct_cag_om1_plaque_type

| | |
|---|---|
| recognised | 74 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 938 |
| plaque, type not recorded | 0 |
| empty | 1104 |

#### ct_cag_mcx_stenosis

| | |
|---|---|
| recognised | 1005 |
| unevaluable (uneval_*) | 17 |
| unrecognised label | 0 |
| empty | 1094 |

#### ct_cag_mcx_plaque_type

| | |
|---|---|
| recognised | 93 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 912 |
| plaque, type not recorded | 0 |
| empty | 1111 |

#### ct_cag_om2_stenosis

| | |
|---|---|
| recognised | 920 |
| unevaluable (uneval_*) | 102 |
| unrecognised label | 0 |
| empty | 1094 |

#### ct_cag_om2_plaque_type

| | |
|---|---|
| recognised | 25 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 894 |
| plaque, type not recorded | <5 |
| empty | 1196 |

#### ct_cag_dcx_stenosis

| | |
|---|---|
| recognised | 955 |
| unevaluable (uneval_*) | 67 |
| unrecognised label | 0 |
| empty | 1094 |

#### ct_cag_dcx_plaque_type

| | |
|---|---|
| recognised | 30 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 925 |
| plaque, type not recorded | 0 |
| empty | 1161 |

#### ct_cag_prca_stenosis

| | |
|---|---|
| recognised | 977 |
| unevaluable (uneval_*) | 46 |
| unrecognised label | 0 |
| empty | 1093 |

#### ct_cag_prca_plaque_type

| | |
|---|---|
| recognised | 228 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 749 |
| plaque, type not recorded | 0 |
| empty | 1139 |

#### ct_cag_mrca_stenosis

| | |
|---|---|
| recognised | 930 |
| unevaluable (uneval_*) | 92 |
| unrecognised label | 0 |
| empty | 1094 |

#### ct_cag_mrca_plaque_type

| | |
|---|---|
| recognised | 156 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 774 |
| plaque, type not recorded | 0 |
| empty | 1186 |

#### ct_cag_drca_stenosis

| | |
|---|---|
| recognised | 963 |
| unevaluable (uneval_*) | 59 |
| unrecognised label | 0 |
| empty | 1094 |

#### ct_cag_drca_plaque_type

| | |
|---|---|
| recognised | 91 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 872 |
| plaque, type not recorded | 0 |
| empty | 1153 |

#### ct_cag_pda_stenosis

| | |
|---|---|
| recognised | 1002 |
| unevaluable (uneval_*) | 20 |
| unrecognised label | 0 |
| empty | 1094 |

#### ct_cag_pda_plaque_type

| | |
|---|---|
| recognised | 27 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 975 |
| plaque, type not recorded | 0 |
| empty | 1114 |

#### ct_cag_pla_stenosis

| | |
|---|---|
| recognised | 898 |
| unevaluable (uneval_*) | 124 |
| unrecognised label | 0 |
| empty | 1094 |

#### ct_cag_pla_plaque_type

| | |
|---|---|
| recognised | 19 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 879 |
| plaque, type not recorded | 0 |
| empty | 1218 |

### text labels decoded (FU)

#### ct_cag_lm_stenosis

| | |
|---|---|
| recognised | 2098 |
| unevaluable (uneval_*) | 15 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_lm_plaque_type

| | |
|---|---|
| recognised | 501 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 1596 |
| plaque, type not recorded | <5 |
| empty | 18 |

#### ct_cag_plad_stenosis

| | |
|---|---|
| recognised | 2087 |
| unevaluable (uneval_*) | 26 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_plad_plaque_type

| | |
|---|---|
| recognised | 1018 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 1067 |
| plaque, type not recorded | <5 |
| empty | 29 |

#### ct_cag_mlad_stenosis

| | |
|---|---|
| recognised | 2086 |
| unevaluable (uneval_*) | 27 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_mlad_plaque_type

| | |
|---|---|
| recognised | 857 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 1228 |
| plaque, type not recorded | <5 |
| empty | 30 |

#### ct_cag_dlad_stenosis

| | |
|---|---|
| recognised | 2077 |
| unevaluable (uneval_*) | 36 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_dlad_plaque_type

| | |
|---|---|
| recognised | 421 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 1655 |
| plaque, type not recorded | <5 |
| empty | 39 |

#### ct_cag_d1_stenosis

| | |
|---|---|
| recognised | 2086 |
| unevaluable (uneval_*) | 27 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_d1_plaque_type

| | |
|---|---|
| recognised | 359 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 1727 |
| plaque, type not recorded | 0 |
| empty | 30 |

#### ct_cag_d2_stenosis

| | |
|---|---|
| recognised | 2089 |
| unevaluable (uneval_*) | 24 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_d2_plaque_type

| | |
|---|---|
| recognised | 130 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 1958 |
| plaque, type not recorded | <5 |
| empty | 27 |

#### ct_cag_im_stenosis

| | |
|---|---|
| recognised | 2093 |
| unevaluable (uneval_*) | 20 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_im_plaque_type

| | |
|---|---|
| recognised | 135 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 1958 |
| plaque, type not recorded | 0 |
| empty | 23 |

#### ct_cag_pcx_stenosis

| | |
|---|---|
| recognised | 2082 |
| unevaluable (uneval_*) | 31 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_pcx_plaque_type

| | |
|---|---|
| recognised | 542 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 1539 |
| plaque, type not recorded | <5 |
| empty | 34 |

#### ct_cag_om1_stenosis

| | |
|---|---|
| recognised | 2079 |
| unevaluable (uneval_*) | 34 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_om1_plaque_type

| | |
|---|---|
| recognised | 229 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 1850 |
| plaque, type not recorded | 0 |
| empty | 37 |

#### ct_cag_mcx_stenosis

| | |
|---|---|
| recognised | 2068 |
| unevaluable (uneval_*) | 45 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_mcx_plaque_type

| | |
|---|---|
| recognised | 236 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 1832 |
| plaque, type not recorded | 0 |
| empty | 48 |

#### ct_cag_om2_stenosis

| | |
|---|---|
| recognised | 2079 |
| unevaluable (uneval_*) | 34 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_om2_plaque_type

| | |
|---|---|
| recognised | 68 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 2011 |
| plaque, type not recorded | 0 |
| empty | 37 |

#### ct_cag_dcx_stenosis

| | |
|---|---|
| recognised | 2074 |
| unevaluable (uneval_*) | 39 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_dcx_plaque_type

| | |
|---|---|
| recognised | 95 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 1979 |
| plaque, type not recorded | 0 |
| empty | 42 |

#### ct_cag_prca_stenosis

| | |
|---|---|
| recognised | 2032 |
| unevaluable (uneval_*) | 81 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_prca_plaque_type

| | |
|---|---|
| recognised | 537 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 1495 |
| plaque, type not recorded | 0 |
| empty | 84 |

#### ct_cag_mrca_stenosis

| | |
|---|---|
| recognised | 1916 |
| unevaluable (uneval_*) | 197 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_mrca_plaque_type

| | |
|---|---|
| recognised | 558 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 1358 |
| plaque, type not recorded | 0 |
| empty | 200 |

#### ct_cag_drca_stenosis

| | |
|---|---|
| recognised | 2032 |
| unevaluable (uneval_*) | 81 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_drca_plaque_type

| | |
|---|---|
| recognised | 344 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 1688 |
| plaque, type not recorded | 0 |
| empty | 84 |

#### ct_cag_pda_stenosis

| | |
|---|---|
| recognised | 2077 |
| unevaluable (uneval_*) | 36 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_pda_plaque_type

| | |
|---|---|
| recognised | 128 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 1949 |
| plaque, type not recorded | 0 |
| empty | 39 |

#### ct_cag_pla_stenosis

| | |
|---|---|
| recognised | 2077 |
| unevaluable (uneval_*) | 36 |
| unrecognised label | 0 |
| empty | <5 |

#### ct_cag_pla_plaque_type

| | |
|---|---|
| recognised | 138 |
| unrecognised label | 0 |
| set to no plaque (stenosis none) | 1939 |
| plaque, type not recorded | 0 |
| empty | 39 |

### pooled over segments (segment-level model)

| | n | events | pct |
|---|---|---|---|
| stenosis progression | 15655 | 3387 | 21.6 |
| new plaque | 13168 | 2479 | 18.8 |
| new spotty calcification | 1036 | 167 | 16.1 |
| new napkin-ring | 2551 | 61 | 2.4 |

### patient level

#### any segment stenosis progression

| | |
|---|---|
| n | 1020 |
| events | 810 |
| pct | 79.4 |

#### any new plaque

| | |
|---|---|
| n | 1020 |
| events | 777 |
| pct | 76.2 |

#### any new high-risk feature

| | |
|---|---|
| n | 763 |
| events | 151 |
| pct | 19.8 |

#### segments with new plaque per patient

| | |
|---|---|
| 0 | 243 |
| 1 | 191 |
| 2 | 150 |
| 3 | 163 |
| 4 | 92 |
| 5 | 71 |
| 6 | 48 |
| 7 | 32 |
| 8 | 16 |
| 9 | 7 |
| 10 | <5 |
| 11 | <5 |
| missing | 1096 |

#### max segment stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | 5 | missing |
|---|---|---|---|---|---|---|---|
| 0 | 134 | 71 | 36 | hidden | <5 | 0 | 0 |
| 1 | 27 | 66 | 93 | 53 | 28 | <5 | <5 |
| 2 | hidden | 50 | 104 | 91 | 91 | <5 | 0 |
| 3 | <5 | <5 | 16 | 37 | 46 | 0 | <5 |
| 4 | 0 | <5 | <5 | 14 | 10 | <5 | 0 |
| 5 | <5 | 0 | <5 | <5 | hidden | 0 | 0 |
| missing | 542 | 255 | 175 | 74 | 40 | 0 | 8 |

### per segment

#### lm

##### evaluable at BL

| | |
|---|---|
| 0 | 2004 |
| 5 | 10 |
| 12 | 38 |
| 13 | 58 |
| 14 | 6 |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 606 | 152 | 39 | <5 | <5 | <5 |
| 1 | hidden | 83 | 38 | hidden | <5 | hidden |
| 2 | hidden | 8 | 24 | 7 | <5 | 0 |
| missing | 955 | 111 | 23 | <5 | <5 | 10 |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 1004 |
| events | 248 |
| pct | 24.7 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 1004 |
| events | 43 |
| pct | 4.3 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | 9 | missing |
|---|---|---|---|---|---|---|---|
| 0 | 606 | 131 | 46 | 16 | <5 | 0 | <5 |
| 1 | 5 | 35 | 9 | <5 | 0 | 0 | <5 |
| 2 | 5 | 47 | 15 | <5 | 0 | 0 | <5 |
| 3 | 6 | 30 | 9 | <5 | 0 | 0 | <5 |
| 4 | 19 | 11 | 5 | 0 | 0 | 0 | 0 |
| missing | 955 | 92 | 33 | 12 | <5 | <5 | 10 |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 802 |
| events | 196 |
| pct | 24.4 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | 98 | 8 |
| 1 | 78 | 23 |
| missing | 1781 | 128 |

##### new spotty calcification

| | |
|---|---|
| n | 106 |
| events | 8 |
| pct | 7.5 |

##### napring BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | <5 |
| missing | hidden | <5 |

##### new napkin-ring

| | |
|---|---|
| n | 207 |
| events | <5 |
| pct | <5 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | 2116 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | 2070 |
| 1 | 46 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 1 | hidden |
| 3 | <5 |
| missing | 1912 |

#### plad

##### evaluable at BL

| | |
|---|---|
| 0 | 1953 |
| 1 | <5 |
| 12 | 81 |
| 13 | 73 |
| 14 | hidden |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 249 | 128 | 54 | 12 | <5 | <5 |
| 1 | 43 | 102 | 98 | 27 | 14 | 9 |
| 2 | hidden | 46 | 89 | 58 | 27 | <5 |
| 3 | <5 | 5 | 8 | hidden | 8 | <5 |
| 4 | 0 | 0 | <5 | <5 | <5 | 0 |
| 5 | 0 | 0 | <5 | 0 | 0 | 0 |
| missing | 758 | 190 | 94 | 32 | 10 | 13 |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 1003 |
| events | 429 |
| pct | 42.8 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 1003 |
| events | 123 |
| pct | 12.3 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | 9 | missing |
|---|---|---|---|---|---|---|---|
| 0 | 249 | 107 | 60 | 18 | hidden | 0 | <5 |
| 1 | <5 | 29 | 28 | <5 | 0 | 0 | <5 |
| 2 | <5 | 90 | 76 | 21 | <5 | 0 | 7 |
| 3 | 10 | 81 | 88 | 22 | <5 | 0 | <5 |
| 4 | 46 | 26 | 19 | hidden | <5 | <5 | 0 |
| missing | 758 | 162 | 100 | 39 | 24 | <5 | hidden |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 446 |
| events | 197 |
| pct | 44.2 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | 205 | 41 |
| 1 | 236 | 88 |
| missing | 1328 | 218 |

##### new spotty calcification

| | |
|---|---|
| n | 246 |
| events | 41 |
| pct | 16.7 |

##### napring BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | hidden |
| 1 | hidden | <5 |
| missing | hidden | hidden |

##### new napkin-ring

| | |
|---|---|
| n | 561 |
| events | 16 |
| pct | 2.9 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | 2110 |
| 1 | 6 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | 1983 |
| 1 | 133 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 0 | <5 |
| 1 | 562 |
| 2 | <5 |
| missing | 1552 |

#### mlad

##### evaluable at BL

| | |
|---|---|
| 0 | 1919 |
| 1 | 8 |
| 5 | <5 |
| 9 | <5 |
| 12 | 105 |
| 13 | 75 |
| 14 | 6 |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | 5 | missing |
|---|---|---|---|---|---|---|---|
| 0 | 344 | 97 | 62 | 31 | 10 | 0 | 5 |
| 1 | 36 | 70 | 65 | 28 | hidden | 0 | <5 |
| 2 | 13 | hidden | 57 | 45 | 35 | 0 | hidden |
| 3 | <5 | <5 | 9 | hidden | 11 | 0 | <5 |
| 4 | <5 | 0 | hidden | <5 | <5 | 0 | 0 |
| 5 | 0 | 0 | <5 | 0 | <5 | 0 | 0 |
| missing | 831 | 137 | 83 | 25 | 16 | <5 | hidden |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 993 |
| events | 396 |
| pct | 39.9 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 993 |
| events | 113 |
| pct | 11.4 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | 9 | missing |
|---|---|---|---|---|---|---|---|
| 0 | 344 | 92 | 74 | 22 | 12 | 0 | 5 |
| 1 | <5 | 13 | 17 | <5 | 0 | 0 | <5 |
| 2 | hidden | 54 | 61 | hidden | 0 | 0 | 5 |
| 3 | 10 | 74 | 58 | 17 | <5 | 0 | <5 |
| 4 | 29 | 27 | 34 | 19 | <5 | <5 | <5 |
| missing | 831 | 131 | 80 | 28 | 23 | 0 | 12 |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 544 |
| events | 200 |
| pct | 36.8 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | 172 | 36 |
| 1 | 193 | 60 |
| missing | 1469 | 186 |

##### new spotty calcification

| | |
|---|---|
| n | 208 |
| events | 36 |
| pct | 17.3 |

##### napring BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | hidden |
| 1 | <5 | 0 |
| missing | hidden | hidden |

##### new napkin-ring

| | |
|---|---|
| n | 457 |
| events | 10 |
| pct | 2.2 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | 2110 |
| 1 | 6 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | 2034 |
| 1 | 82 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 0 | <5 |
| 1 | hidden |
| missing | 1665 |

#### dlad

##### evaluable at BL

| | |
|---|---|
| 0 | 1940 |
| 1 | hidden |
| 12 | 74 |
| 13 | 87 |
| 14 | 6 |
| 17 | <5 |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 636 | 100 | 55 | 26 | 5 | 12 |
| 1 | 28 | 17 | 21 | hidden | <5 | <5 |
| 2 | 21 | hidden | 22 | 15 | hidden | <5 |
| 3 | hidden | <5 | <5 | <5 | <5 | <5 |
| 4 | <5 | 0 | <5 | 0 | 0 | 0 |
| missing | 963 | 48 | 42 | 18 | 7 | 21 |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 999 |
| events | 247 |
| pct | 24.7 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 999 |
| events | 74 |
| pct | 7.4 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | 9 | missing |
|---|---|---|---|---|---|---|---|
| 0 | 636 | 100 | 60 | 17 | 9 | 0 | 12 |
| 1 | hidden | 9 | 10 | 0 | 0 | 0 | <5 |
| 2 | hidden | 17 | 17 | 5 | <5 | 0 | <5 |
| 3 | 10 | 21 | 15 | <5 | <5 | <5 | 0 |
| 4 | 29 | 13 | 6 | <5 | 0 | 0 | <5 |
| missing | 963 | 54 | 32 | 7 | 22 | 0 | 21 |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 822 |
| events | 186 |
| pct | 22.6 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | 67 | 11 |
| 1 | 79 | 26 |
| missing | 1822 | 111 |

##### new spotty calcification

| | |
|---|---|
| n | 78 |
| events | 11 |
| pct | 14.1 |

##### napring BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | <5 |
| 1 | <5 | 0 |
| missing | hidden | hidden |

##### new napkin-ring

| | |
|---|---|
| n | 179 |
| events | <5 |
| pct | <5 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | hidden |
| 1 | <5 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | 2088 |
| 1 | 28 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 0 | <5 |
| 1 | hidden |
| missing | 1943 |

#### d1

##### evaluable at BL

| | |
|---|---|
| 0 | 1870 |
| 1 | 10 |
| 3 | <5 |
| 5 | <5 |
| 12 | 77 |
| 13 | 71 |
| 14 | <5 |
| 17 | 79 |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | 5 | missing |
|---|---|---|---|---|---|---|---|
| 0 | 708 | 76 | 40 | 21 | 9 | 0 | 12 |
| 1 | 13 | 13 | hidden | 9 | 5 | <5 | <5 |
| 2 | 14 | 8 | 18 | 16 | hidden | 0 | <5 |
| 3 | <5 | <5 | 8 | <5 | <5 | 0 | 0 |
| 4 | <5 | <5 | 0 | <5 | <5 | 0 | 0 |
| 5 | <5 | 0 | <5 | 0 | 0 | 0 | 0 |
| missing | 985 | 47 | 33 | 24 | <5 | <5 | 16 |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 993 |
| events | 194 |
| pct | 19.5 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 993 |
| events | 56 |
| pct | 5.6 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 708 | 90 | 42 | hidden | <5 | hidden |
| 1 | <5 | hidden | hidden | 0 | 0 | 0 |
| 2 | 5 | 19 | 11 | <5 | 0 | <5 |
| 3 | hidden | hidden | 10 | <5 | 0 | 0 |
| 4 | 18 | 18 | <5 | 0 | <5 | 0 |
| missing | 985 | 68 | 25 | 8 | 7 | 16 |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 854 |
| events | 146 |
| pct | 17.1 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | 48 | 11 |
| 1 | 66 | 16 |
| missing | 1876 | 99 |

##### new spotty calcification

| | |
|---|---|
| n | 59 |
| events | 11 |
| pct | 18.6 |

##### napring BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | <5 |
| 1 | <5 | 0 |
| missing | hidden | <5 |

##### new napkin-ring

| | |
|---|---|
| n | 139 |
| events | <5 |
| pct | <5 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | 2116 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | 2099 |
| 1 | 17 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 0 | <5 |
| 1 | 121 |
| 2 | <5 |
| missing | 1992 |

#### d2

##### evaluable at BL

| | |
|---|---|
| 0 | 1851 |
| 1 | 6 |
| 3 | <5 |
| 5 | 65 |
| 12 | 50 |
| 13 | 62 |
| 14 | hidden |
| 17 | 76 |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 793 | 41 | 11 | 11 | 7 | 12 |
| 1 | 19 | <5 | <5 | <5 | <5 | 0 |
| 2 | 20 | <5 | 9 | 0 | <5 | 0 |
| 3 | hidden | 0 | <5 | 0 | <5 | 0 |
| 4 | <5 | <5 | 0 | 0 | 0 | 0 |
| missing | 1119 | 12 | 14 | <5 | <5 | 15 |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 938 |
| events | 80 |
| pct | 8.5 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 938 |
| events | 53 |
| pct | 5.7 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | 9 | missing |
|---|---|---|---|---|---|---|---|
| 0 | 793 | 46 | 11 | hidden | 6 | <5 | 12 |
| 1 | 8 | <5 | <5 | 0 | 0 | 0 | 0 |
| 2 | hidden | 9 | <5 | 0 | 0 | 0 | 0 |
| 3 | hidden | hidden | 0 | 0 | 0 | 0 | 0 |
| 4 | 25 | <5 | 0 | <5 | <5 | 0 | 0 |
| missing | 1119 | 23 | hidden | 0 | <5 | 0 | 15 |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 863 |
| events | 70 |
| pct | 8.1 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | <5 |
| 1 | hidden | hidden |
| missing | 2007 | 34 |

##### new spotty calcification

| | |
|---|---|
| n | 36 |
| events | <5 |
| pct | <5 |

##### napring BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | <5 |
| 1 | <5 | 0 |
| missing | hidden | <5 |

##### new napkin-ring

| | |
|---|---|
| n | 74 |
| events | <5 |
| pct | <5 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | 2116 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | hidden |
| 1 | <5 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 1 | hidden |
| 2 | <5 |
| missing | 2055 |

#### im

##### evaluable at BL

| | |
|---|---|
| 0 | 498 |
| 1 | <5 |
| 3 | <5 |
| 5 | 1480 |
| 12 | 29 |
| 13 | 19 |
| 14 | <5 |
| 17 | 85 |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | 5 | missing |
|---|---|---|---|---|---|---|---|
| 0 | 257 | 23 | 12 | <5 | <5 | <5 | <5 |
| 1 | <5 | <5 | <5 | <5 | <5 | 0 | 0 |
| 2 | 7 | <5 | <5 | 6 | <5 | 0 | 0 |
| 3 | <5 | <5 | 0 | <5 | 0 | 0 | <5 |
| 4 | 0 | 0 | 0 | <5 | 0 | 0 | 0 |
| missing | 1689 | 27 | 21 | 13 | 8 | 0 | 19 |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 335 |
| events | 55 |
| pct | 16.4 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 335 |
| events | 17 |
| pct | 5.1 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 257 | 24 | 10 | <5 | <5 | <5 |
| 1 | <5 | <5 | <5 | 0 | 0 | 0 |
| 2 | <5 | 8 | <5 | 0 | 0 | 0 |
| 3 | <5 | <5 | <5 | 0 | 0 | <5 |
| 4 | 6 | <5 | <5 | 0 | 0 | 0 |
| missing | 1689 | 37 | 23 | hidden | <5 | 19 |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 298 |
| events | 41 |
| pct | 13.8 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | 12 | 5 |
| 1 | 16 | 5 |
| missing | 2030 | 48 |

##### new spotty calcification

| | |
|---|---|
| n | 17 |
| events | 5 |
| pct | 29.4 |

##### napring BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | 0 |
| missing | hidden | <5 |

##### new napkin-ring

| | |
|---|---|
| n | 38 |
| events | 0 |
| pct | 0 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | 2116 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | 2107 |
| 1 | 9 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 0 | <5 |
| 1 | hidden |
| missing | 2081 |

#### pcx

##### evaluable at BL

| | |
|---|---|
| 0 | 1948 |
| 1 | 9 |
| 9 | <5 |
| 11 | <5 |
| 12 | 70 |
| 13 | 79 |
| 14 | 6 |
| 17 | <5 |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 572 | 190 | 57 | 18 | 8 | 10 |
| 1 | 21 | 43 | 25 | 8 | hidden | <5 |
| 2 | hidden | hidden | 11 | 6 | <5 | <5 |
| 3 | <5 | <5 | 5 | <5 | <5 | <5 |
| 5 | 0 | 0 | 0 | 0 | <5 | 0 |
| missing | 940 | 102 | 29 | hidden | <5 | 19 |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 997 |
| events | 321 |
| pct | 32.2 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 997 |
| events | 46 |
| pct | 4.6 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | 9 | missing |
|---|---|---|---|---|---|---|---|
| 0 | 572 | 176 | 70 | 20 | 7 | 0 | 10 |
| 1 | <5 | 17 | 12 | <5 | 0 | 0 | <5 |
| 2 | 8 | 37 | 17 | <5 | 0 | 0 | <5 |
| 3 | <5 | 21 | hidden | <5 | 0 | 0 | <5 |
| 4 | 12 | <5 | <5 | 0 | 0 | <5 | 0 |
| 9 | 0 | <5 | 0 | 0 | 0 | 0 | 0 |
| missing | 940 | 93 | 38 | 9 | 5 | 0 | 19 |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 845 |
| events | 273 |
| pct | 32.3 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | 46 | 7 |
| 1 | 73 | 31 |
| missing | 1767 | 192 |

##### new spotty calcification

| | |
|---|---|
| n | 53 |
| events | 7 |
| pct | 13.2 |

##### napring BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | <5 |
| missing | hidden | hidden |

##### new napkin-ring

| | |
|---|---|
| n | 157 |
| events | <5 |
| pct | <5 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | 2116 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | 2080 |
| 1 | 36 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 0 | <5 |
| 1 | hidden |
| missing | 1969 |

#### om1

##### evaluable at BL

| | |
|---|---|
| 0 | 1897 |
| 1 | 6 |
| 5 | <5 |
| 12 | 70 |
| 13 | 72 |
| 14 | 5 |
| 16 | <5 |
| 17 | 61 |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | 5 | missing |
|---|---|---|---|---|---|---|---|
| 0 | 786 | 81 | 25 | 20 | hidden | <5 | 18 |
| 1 | 22 | 6 | 6 | <5 | <5 | 0 | <5 |
| 2 | 11 | <5 | 5 | <5 | <5 | 0 | 0 |
| 3 | <5 | <5 | 0 | <5 | <5 | 0 | 0 |
| 5 | <5 | 0 | 0 | <5 | 0 | 0 | 0 |
| missing | 1028 | 34 | 16 | hidden | <5 | 0 | hidden |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 992 |
| events | 152 |
| pct | 15.3 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 992 |
| events | 42 |
| pct | 4.2 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 786 | 86 | 33 | hidden | hidden | 18 |
| 1 | 5 | 5 | <5 | <5 | 0 | <5 |
| 2 | 11 | 7 | 10 | 0 | 0 | 0 |
| 3 | 9 | <5 | <5 | 0 | 0 | 0 |
| 4 | 11 | <5 | <5 | <5 | 0 | 0 |
| missing | 1028 | 34 | 19 | <5 | <5 | hidden |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 920 |
| events | 134 |
| pct | 14.6 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | <5 |
| 1 | hidden | hidden |
| missing | 1975 | 67 |

##### new spotty calcification

| | |
|---|---|
| n | 32 |
| events | <5 |
| pct | <5 |

##### napring BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | 0 |
| missing | hidden | <5 |

##### new napkin-ring

| | |
|---|---|
| n | 74 |
| events | 0 |
| pct | 0 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | 2116 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | 2106 |
| 1 | 10 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 0 | <5 |
| 1 | hidden |
| missing | 2050 |

#### mcx

##### evaluable at BL

| | |
|---|---|
| 0 | 1890 |
| 1 | 9 |
| 4 | <5 |
| 5 | 7 |
| 12 | 77 |
| 13 | 80 |
| 14 | hidden |
| 17 | 47 |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 761 | 76 | 40 | 10 | 6 | 19 |
| 1 | 26 | 16 | 8 | <5 | <5 | <5 |
| 2 | 16 | <5 | hidden | <5 | <5 | <5 |
| 3 | <5 | <5 | <5 | 0 | 0 | 0 |
| 4 | <5 | 0 | 0 | <5 | 0 | 0 |
| 5 | 0 | 0 | 0 | 0 | <5 | 0 |
| missing | 1027 | 36 | 14 | hidden | <5 | 26 |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 983 |
| events | 149 |
| pct | 15.2 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 983 |
| events | 52 |
| pct | 5.3 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 761 | 79 | 37 | 9 | 7 | 19 |
| 1 | 12 | <5 | <5 | <5 | 0 | <5 |
| 2 | 14 | 13 | 6 | hidden | 0 | <5 |
| 3 | 10 | <5 | hidden | 0 | 0 | 0 |
| 4 | 8 | 0 | <5 | 0 | <5 | 0 |
| missing | 1027 | 32 | 17 | hidden | <5 | 26 |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 893 |
| events | 132 |
| pct | 14.8 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | <5 |
| 1 | hidden | hidden |
| missing | 1942 | 82 |

##### new spotty calcification

| | |
|---|---|
| n | 26 |
| events | <5 |
| pct | <5 |

##### napring BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | <5 |
| 1 | <5 | 0 |
| missing | hidden | <5 |

##### new napkin-ring

| | |
|---|---|
| n | 91 |
| events | <5 |
| pct | <5 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | hidden |
| 1 | <5 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | 2110 |
| 1 | 6 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 0 | <5 |
| 1 | hidden |
| missing | 2032 |

#### om2

##### evaluable at BL

| | |
|---|---|
| 0 | 1832 |
| 1 | 6 |
| 4 | <5 |
| 5 | 95 |
| 12 | 53 |
| 13 | 72 |
| 14 | <5 |
| 17 | 53 |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 838 | 24 | 9 | <5 | <5 | 16 |
| 1 | hidden | <5 | <5 | 0 | 0 | 0 |
| 2 | hidden | <5 | 0 | 0 | 0 | 0 |
| 4 | 0 | 0 | 0 | <5 | <5 | 0 |
| missing | 1153 | 11 | hidden | <5 | <5 | 21 |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 904 |
| events | 41 |
| pct | 4.5 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 904 |
| events | 23 |
| pct | 2.5 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 838 | 23 | 13 | <5 | <5 | 16 |
| 1 | hidden | <5 | 0 | 0 | 0 | 0 |
| 2 | hidden | <5 | 0 | 0 | 0 | 0 |
| 3 | <5 | <5 | 0 | 0 | 0 | 0 |
| 4 | <5 | 0 | 0 | 0 | 0 | 0 |
| 9 | <5 | 0 | 0 | 0 | 0 | 0 |
| missing | 1153 | 12 | 5 | <5 | <5 | 21 |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 878 |
| events | 40 |
| pct | 4.6 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | 0 |
| 1 | hidden | <5 |
| missing | hidden | hidden |

##### new spotty calcification

| | |
|---|---|
| n | 8 |
| events | 0 |
| pct | 0 |

##### napring BL -> FU

| | 0 |
|---|---|
| 0 | 26 |
| missing | 2090 |

##### new napkin-ring

| | |
|---|---|
| n | 26 |
| events | 0 |
| pct | 0 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | 2116 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | hidden |
| 1 | <5 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 1 | 22 |
| missing | 2094 |

#### dcx

##### evaluable at BL

| | |
|---|---|
| 0 | 1832 |
| 1 | 5 |
| 4 | <5 |
| 5 | 61 |
| 12 | 54 |
| 13 | 80 |
| 14 | 5 |
| 16 | <5 |
| 17 | 77 |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 852 | 35 | 14 | hidden | <5 | 17 |
| 1 | 6 | <5 | <5 | <5 | 0 | 0 |
| 2 | 9 | <5 | <5 | 0 | <5 | 0 |
| 3 | 0 | 0 | 0 | 0 | <5 | 0 |
| 4 | 0 | 0 | 0 | <5 | 0 | 0 |
| missing | 1112 | 15 | <5 | 5 | <5 | 25 |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 938 |
| events | 63 |
| pct | 6.7 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 938 |
| events | 17 |
| pct | 1.8 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 852 | 37 | 12 | hidden | <5 | 17 |
| 1 | <5 | hidden | 0 | 0 | 0 | 0 |
| 2 | 8 | 0 | <5 | <5 | 0 | 0 |
| 3 | <5 | <5 | <5 | 0 | 0 | 0 |
| 4 | <5 | 0 | 0 | <5 | 0 | 0 |
| missing | 1112 | 14 | hidden | <5 | 0 | 25 |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 908 |
| events | 56 |
| pct | 6.2 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | <5 |
| 1 | hidden | hidden |
| missing | 2043 | 44 |

##### new spotty calcification

| | |
|---|---|
| n | 7 |
| events | <5 |
| pct | <5 |

##### napring BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | <5 |
| missing | hidden | <5 |

##### new napkin-ring

| | |
|---|---|
| n | 29 |
| events | <5 |
| pct | <5 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | 2116 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | hidden |
| 1 | <5 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 0 | <5 |
| 1 | hidden |
| missing | 2092 |

#### prca

##### evaluable at BL

| | |
|---|---|
| 0 | 1848 |
| 1 | 44 |
| 5 | <5 |
| 9 | <5 |
| 12 | 157 |
| 13 | 59 |
| 14 | <5 |
| 16 | <5 |
| missing | <5 |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 513 | 137 | 46 | 21 | 6 | 26 |
| 1 | 28 | 52 | 42 | 8 | 6 | 8 |
| 2 | 7 | hidden | hidden | 9 | hidden | <5 |
| 3 | <5 | <5 | 0 | hidden | <5 | <5 |
| 4 | <5 | 0 | <5 | 0 | 0 | 0 |
| 5 | 0 | 0 | 0 | 0 | <5 | <5 |
| missing | 945 | 106 | 35 | hidden | <5 | 44 |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 937 |
| events | 282 |
| pct | 30.1 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 937 |
| events | 63 |
| pct | 6.7 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 513 | 117 | 56 | 24 | 13 | 26 |
| 1 | <5 | 20 | 9 | <5 | 0 | <5 |
| 2 | hidden | 28 | 23 | <5 | 0 | <5 |
| 3 | 14 | 30 | 26 | 8 | <5 | hidden |
| 4 | 16 | 16 | 8 | <5 | <5 | <5 |
| missing | 945 | 92 | 43 | 8 | 7 | 44 |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 723 |
| events | 210 |
| pct | 29 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | 59 | 19 |
| 1 | 106 | 44 |
| missing | 1705 | 183 |

##### new spotty calcification

| | |
|---|---|
| n | 78 |
| events | 19 |
| pct | 24.4 |

##### napring BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | <5 |
| 1 | <5 | 0 |
| missing | hidden | hidden |

##### new napkin-ring

| | |
|---|---|
| n | 227 |
| events | <5 |
| pct | <5 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | hidden |
| 1 | <5 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | 2080 |
| 1 | 36 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 0 | <5 |
| 1 | hidden |
| missing | 1908 |

#### mrca

##### evaluable at BL

| | |
|---|---|
| 0 | 1740 |
| 1 | 89 |
| 3 | <5 |
| 5 | <5 |
| 9 | <5 |
| 12 | 228 |
| 13 | 43 |
| 14 | <5 |
| 16 | <5 |
| 17 | 10 |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 462 | 144 | 60 | 30 | 12 | 66 |
| 1 | <5 | 20 | 28 | 16 | hidden | 13 |
| 2 | 5 | 7 | 20 | 14 | <5 | <5 |
| 3 | 0 | 0 | <5 | <5 | <5 | 0 |
| 4 | <5 | 0 | 0 | 0 | <5 | 0 |
| 5 | 0 | 0 | <5 | 0 | <5 | <5 |
| missing | 886 | 109 | 54 | hidden | <5 | 117 |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 847 |
| events | 318 |
| pct | 37.5 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 847 |
| events | 20 |
| pct | 2.4 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 462 | 118 | 70 | 36 | 22 | 66 |
| 1 | <5 | 9 | hidden | hidden | 0 | <5 |
| 2 | <5 | 16 | 24 | 7 | 0 | <5 |
| 3 | <5 | 16 | 21 | 12 | 0 | hidden |
| 4 | 7 | 6 | <5 | <5 | 0 | <5 |
| missing | 886 | 89 | 65 | 15 | 14 | 117 |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 708 |
| events | 246 |
| pct | 34.7 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | 26 | 10 |
| 1 | 86 | 34 |
| missing | 1760 | 200 |

##### new spotty calcification

| | |
|---|---|
| n | 36 |
| events | 10 |
| pct | 27.8 |

##### napring BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | hidden |
| 1 | <5 | 0 |
| missing | hidden | hidden |

##### new napkin-ring

| | |
|---|---|
| n | 155 |
| events | 7 |
| pct | 4.5 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | hidden |
| 1 | <5 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | 2081 |
| 1 | 35 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 1 | 131 |
| missing | 1985 |

#### drca

##### evaluable at BL

| | |
|---|---|
| 0 | 1815 |
| 1 | 47 |
| 5 | 10 |
| 9 | <5 |
| 12 | 124 |
| 13 | 81 |
| 14 | <5 |
| 16 | <5 |
| 17 | 34 |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 656 | 118 | 39 | 21 | 8 | 30 |
| 1 | <5 | 14 | 18 | 10 | 5 | <5 |
| 2 | <5 | hidden | hidden | <5 | 5 | <5 |
| 3 | 0 | 0 | <5 | 5 | <5 | 0 |
| 5 | 0 | <5 | 0 | 0 | 0 | <5 |
| missing | 1027 | 54 | 16 | hidden | <5 | 46 |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 925 |
| events | 230 |
| pct | 24.9 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 925 |
| events | 12 |
| pct | 1.3 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 656 | 95 | 58 | 19 | 14 | 30 |
| 1 | 0 | <5 | hidden | 5 | 0 | <5 |
| 2 | 0 | 11 | 15 | 5 | <5 | <5 |
| 3 | <5 | 9 | 12 | <5 | 0 | <5 |
| 4 | <5 | <5 | <5 | <5 | 0 | 0 |
| missing | 1027 | 43 | 25 | hidden | hidden | 46 |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 842 |
| events | 186 |
| pct | 22.1 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | 19 | 10 |
| 1 | 43 | 19 |
| missing | 1907 | 118 |

##### new spotty calcification

| | |
|---|---|
| n | 29 |
| events | 10 |
| pct | 34.5 |

##### napring BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | hidden |
| missing | hidden | <5 |

##### new napkin-ring

| | |
|---|---|
| n | 91 |
| events | 6 |
| pct | 6.6 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | 2116 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | 2091 |
| 1 | 25 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 0 | <5 |
| 1 | hidden |
| missing | 2036 |

#### pda

##### evaluable at BL

| | |
|---|---|
| 0 | 1932 |
| 1 | 15 |
| 5 | <5 |
| 9 | <5 |
| 12 | 53 |
| 13 | 95 |
| 14 | <5 |
| 17 | 12 |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | 5 | missing |
|---|---|---|---|---|---|---|---|
| 0 | 879 | 43 | 17 | 12 | hidden | <5 | 18 |
| 1 | hidden | <5 | <5 | <5 | <5 | 0 | 0 |
| 2 | <5 | <5 | <5 | <5 | 0 | 0 | 0 |
| 3 | 0 | <5 | 0 | <5 | 0 | 0 | 0 |
| missing | 1060 | 23 | 7 | <5 | <5 | 0 | 21 |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 984 |
| events | 88 |
| pct | 8.9 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 984 |
| events | 13 |
| pct | 1.3 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 879 | 44 | 21 | <5 | hidden | 18 |
| 1 | 7 | <5 | <5 | <5 | 0 | 0 |
| 2 | 0 | <5 | <5 | <5 | 0 | 0 |
| 3 | <5 | <5 | 0 | 0 | 0 | 0 |
| 4 | <5 | <5 | 0 | 0 | <5 | 0 |
| missing | 1060 | 21 | 8 | <5 | <5 | 21 |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 957 |
| events | 78 |
| pct | 8.2 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | <5 |
| 1 | hidden | <5 |
| missing | 2036 | 53 |

##### new spotty calcification

| | |
|---|---|
| n | 10 |
| events | <5 |
| pct | <5 |

##### napring BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | 0 |
| missing | hidden | <5 |

##### new napkin-ring

| | |
|---|---|
| n | 27 |
| events | 0 |
| pct | 0 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | 2116 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | 2109 |
| 1 | 7 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 1 | 16 |
| missing | 2100 |

#### pla

##### evaluable at BL

| | |
|---|---|
| 0 | 1849 |
| 1 | 14 |
| 5 | 108 |
| 9 | <5 |
| 12 | 49 |
| 13 | 80 |
| 14 | hidden |
| 17 | 9 |

##### stenosis BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 777 | 59 | 14 | 10 | hidden | hidden |
| 1 | <5 | <5 | <5 | <5 | 0 | <5 |
| 2 | <5 | <5 | hidden | <5 | <5 | 0 |
| missing | 1158 | 20 | 11 | <5 | <5 | 24 |

##### stenosis progression (>= 1 grade)

| | |
|---|---|
| n | 883 |
| events | 94 |
| pct | 10.6 |

##### stenosis regression (data check)

| | |
|---|---|
| n | 883 |
| events | 6 |
| pct | 0.7 |

##### plaque type BL -> FU

| | 0 | 1 | 2 | 3 | 4 | missing |
|---|---|---|---|---|---|---|
| 0 | 777 | 57 | 21 | hidden | <5 | hidden |
| 1 | <5 | <5 | <5 | 0 | 0 | 0 |
| 2 | <5 | <5 | <5 | <5 | 0 | <5 |
| 3 | 0 | <5 | <5 | 0 | 0 | 0 |
| 4 | <5 | <5 | 0 | 0 | 0 | 0 |
| missing | 1158 | 20 | 10 | <5 | <5 | 24 |

##### new plaque (among plaque-free at BL)

| | |
|---|---|
| n | 865 |
| events | 88 |
| pct | 10.2 |

##### spotcalc BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | <5 |
| 1 | hidden | <5 |
| missing | 2034 | 63 |

##### new spotty calcification

| | |
|---|---|
| n | 7 |
| events | <5 |
| pct | <5 |

##### napring BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | <5 |
| missing | hidden | <5 |

##### new napkin-ring

| | |
|---|---|
| n | 19 |
| events | <5 |
| pct | <5 |

##### lap at FU (FU only)

| | |
|---|---|
| 0 | 2116 |

##### posrem at FU (FU only)

| | |
|---|---|
| 0 | 2104 |
| 1 | 12 |

##### Medis plaque analysis finished (BL)

| | |
|---|---|
| 1 | hidden |
| 2 | <5 |
| missing | 2102 |

## 6. Plaque trajectory groups (none->none, none->plaque, plaque->same/more/less)

### patient level

#### extent: SIS (number of segments with plaque)

| | n | pct |
|---|---|---|
| no plaque -> no plaque | 684 | 32.3 |
| no plaque -> plaque | 668 | 31.6 |
| plaque -> same | 105 | 5 |
| plaque -> more | 552 | 26.1 |
| plaque -> less | 107 | 5.1 |
| missing | 0 |  |

#### burden: SSS (summed stenosis grades)

| | n | pct |
|---|---|---|
| no plaque -> no plaque | 684 | 32.3 |
| no plaque -> plaque | 668 | 31.6 |
| plaque -> same | 58 | 2.7 |
| plaque -> more | 586 | 27.7 |
| plaque -> less | 120 | 5.7 |
| missing | 0 |  |

#### LAD extent: lad SIS

| | n | pct |
|---|---|---|
| no plaque -> no plaque | 764 | 36.1 |
| no plaque -> plaque | 623 | 29.4 |
| plaque -> same | 213 | 10.1 |
| plaque -> more | 379 | 17.9 |
| plaque -> less | 137 | 6.5 |
| missing | 0 |  |

#### CX extent: cx SIS

| | n | pct |
|---|---|---|
| no plaque -> no plaque | 1333 | 63 |
| no plaque -> plaque | 502 | 23.7 |
| plaque -> same | 97 | 4.6 |
| plaque -> more | 124 | 5.9 |
| plaque -> less | 60 | 2.8 |
| missing | 0 |  |

#### RCA extent: rca SIS

| | n | pct |
|---|---|---|
| no plaque -> no plaque | 1269 | 60 |
| no plaque -> plaque | 533 | 25.2 |
| plaque -> same | 89 | 4.2 |
| plaque -> more | 176 | 8.3 |
| plaque -> less | 49 | 2.3 |
| missing | 0 |  |

#### extent: segments with plaque, counted from segment plaque types

| | n | pct |
|---|---|---|
| no plaque -> no plaque | 134 | 13.1 |
| no plaque -> plaque | 124 | 12.2 |
| plaque -> same | 105 | 10.3 |
| plaque -> more | 552 | 54.1 |
| plaque -> less | 105 | 10.3 |
| missing | 1096 |  |

### BL predictor mean by SIS trajectory group

| | no plaque -> no plaque | no plaque -> plaque | plaque -> same | plaque -> more | plaque -> less |
|---|---|---|---|---|---|
| male | 0.268 | 0.467 | 0.476 | 0.685 | 0.393 |
| scan_age | 52.3 | 55.9 | 58.3 | 59.5 | 58.6 |
| clin_bmi | 25 | 26.4 | 25.7 | 26.5 | 25.3 |
| clin_bp_sys_mean | 128 | 136 | 136 | 140 | 135 |
| clin_bp_dia_mean | 78.4 | 81.9 | 81.9 | 83.2 | 80.3 |
| hr_during_scan | 55 | 53.4 | 52.3 | 51.8 |  |
| creatinine | 75.6 | 77.8 | 78.5 | 80.5 | 78.2 |
| egfr | 89.1 | 89 | 86.7 | 88.6 | 85.5 |
| hba1c | 34.8 | 36.3 | 36.6 | 36.1 | 35.1 |
| tot_cholesterol | 5.13 | 5.41 | 5.46 | 5.46 | 5.33 |
| hdl | 1.57 | 1.44 | 1.54 | 1.43 | 1.52 |
| ldl | 2.96 | 3.22 | 3.23 | 3.28 | 3.12 |
| triglyceride | 1.41 | 1.74 | 1.61 | 1.77 | 1.61 |
| hist_smoking_current | 0.0716 | 0.117 | 0.0952 | 0.12 | 0.0841 |
| hist_smoking_former | 0.371 | 0.413 | 0.486 | 0.495 | 0.477 |
| hist_smoking_years | 18.6 | 23.4 | 22.6 | 24.7 | 24.9 |
| hist_diabetes | 0.0088 | 0.03 | 0.0288 | 0.0182 | 0.0093 |
| demo_hist_family_cvd | 0.275 | 0.329 | 0.269 | 0.336 | 0.327 |
| demo_hist_family_hypercholesterolemia | 0.505 | 0.515 | 0.587 | 0.443 | 0.551 |
| med_lipid_lowering_any | 0.0464 | 0.0862 | 0.12 | 0.146 | 0.068 |
| med_antihypertensive_any | 0.0778 | 0.162 | 0.19 | 0.195 | 0.155 |
| ct_cacs_sum | 0.286 | 37.1 | 178 | 147 | 188 |
| ct_cag_sis | 0 | 0 | 3.43 | 3.26 | 3.93 |
| ct_cag_sss | 0 | 0 | 5.52 | 5.14 | 6.27 |
| ct_cag_plaque_type_score | 0 | 0 | 7.26 | 6.49 | 8.57 |

### segment level (more/less = stenosis grade change)

#### pooled over segments

| | n | pct |
|---|---|---|
| no plaque -> no plaque | 10689 | 68.3 |
| no plaque -> plaque | 2479 | 15.8 |
| plaque -> same | 806 | 5.1 |
| plaque -> more | 908 | 5.8 |
| plaque -> less | 773 | 4.9 |
| missing | 20317 |  |

#### per segment (n)

| | no plaque -> no plaque | no plaque -> plaque | plaque -> same | plaque -> more | plaque -> less | missing |
|---|---|---|---|---|---|---|
| lm | 606 | 196 | 107 | 52 | 43 | 1112 |
| plad | 249 | 197 | 202 | 232 | 123 | 1113 |
| mlad | 344 | 200 | 140 | 196 | 113 | 1123 |
| dlad | 636 | 186 | 42 | 61 | 74 | 1117 |
| d1 | 708 | 146 | 35 | 48 | 56 | 1123 |
| d2 | 793 | 70 | 12 | 10 | 53 | 1178 |
| im | 257 | 41 | 6 | 14 | 17 | 1781 |
| pcx | 572 | 273 | 58 | 48 | 46 | 1119 |
| om1 | 786 | 134 | 12 | 18 | 42 | 1124 |
| mcx | 761 | 132 | 21 | 17 | 52 | 1133 |
| om2 | 838 | 40 | <5 | <5 | 23 | 1212 |
| dcx | 852 | 56 | 6 | 7 | 17 | 1178 |
| prca | 513 | 210 | 79 | 72 | 63 | 1179 |
| mrca | 462 | 246 | 47 | 72 | 20 | 1269 |
| drca | 656 | 186 | 27 | 44 | 12 | 1191 |
| pda | 879 | 78 | <5 | 10 | 13 | 1132 |
| pla | 777 | 88 | 6 | 6 | 6 | 1233 |

## 7. Outcome definitions by anatomical level (segment, position, vessel, whole tree)

### how to read

| | |
|---|---|
| levels | segment -> position (proximal/mid/distal/side branch) -> vessel -> whole tree; each unit counts only segments assessed at both visits |
| regression | the opposite change (plaque or stenosis decreasing); mostly reader variability, so a high progression:regression ratio means more signal than noise |
| ICC / design effect | how much events cluster within patients at sub-patient levels; inflates the variance, so the effective sample is n units / design effect |
| EPV | max predictors at 10 events per variable, ignoring clustering |
| OBSTRUCTIVE_GRADE | 3 |

### level: segment

#### units (segments in each)

| | |
|---|---|
| lm | lm |
| plad | plad |
| mlad | mlad |
| dlad | dlad |
| d1 | d1 |
| d2 | d2 |
| im | im |
| pcx | pcx |
| om1 | om1 |
| mcx | mcx |
| om2 | om2 |
| dcx | dcx |
| prca | prca |
| mrca | mrca |
| drca | drca |
| pda | pda |
| pla | pla |

#### outcome summary (all units pooled)

| | n units | events | pct | regression events | regression pct | progression : regression | patients with event | ICC within patient | design effect | max predictors at 10 EPV |
|---|---|---|---|---|---|---|---|---|---|---|
| new plaque in a plaque-free segment | 13168 | 2479 | 18.8 | 504 | 20.3 | 4.92 | 777 | 0.145 | 2.73 | 247 |
| plaque-free -> plaque | 13168 | 2479 | 18.8 | 504 | 20.3 | 4.92 | 777 | 0.145 | 2.73 | 247 |
| extent increase (+1 segment with plaque) | 15655 | 2479 | 15.8 | 504 | 3.2 | 4.92 | 777 | 0.0947 | 2.36 | 247 |
| burden increase (sum of stenosis grades) | 15655 | 3387 | 21.6 | 773 | 4.9 | 4.38 | 810 | 0.143 | 3.06 | 338 |
| burden increase >= 2 | 15655 | 1263 | 8.1 | 239 | 1.5 | 5.28 | 518 | 0.112 | 2.61 | 126 |
| max stenosis +1 grade | 15655 | 3387 | 21.6 | 773 | 4.9 | 4.38 | 810 | 0.143 | 3.06 | 338 |
| incident obstructive | 15432 | 860 | 5.6 | 109 | 48.9 | 7.89 | 382 | 0.12 | 2.69 | 86 |
| new high-risk feature | 1001 | 185 | 18.5 | 1064 | 71.8 | 0.17 | 142 | 0.301 | 1.28 | 18 |
| any plaque progression | 15655 | 3387 | 21.6 | 773 | 4.9 | 4.38 | 810 | 0.143 | 3.06 | 338 |

#### events / n (%) per unit

| | new plaque in a plaque-free segment | plaque-free -> plaque | extent increase (+1 segment with plaque) | burden increase (sum of stenosis grades) | burden increase >= 2 | max stenosis +1 grade | incident obstructive | new high-risk feature | any plaque progression |
|---|---|---|---|---|---|---|---|---|---|
| lm | 196/802 (24.4%) | 196/802 (24.4%) | 196/1004 (19.5%) | 248/1004 (24.7%) | 51/1004 (5.1%) | 248/1004 (24.7%) | 19/1004 (1.9%) | 9/104 (8.7%) | 248/1004 (24.7%) |
| plad | 197/446 (44.2%) | 197/446 (44.2%) | 197/1003 (19.6%) | 429/1003 (42.8%) | 137/1003 (13.7%) | 429/1003 (42.8%) | 141/965 (14.6%) | 48/236 (20.3%) | 429/1003 (42.8%) |
| mlad | 200/544 (36.8%) | 200/544 (36.8%) | 200/993 (20.1%) | 396/993 (39.9%) | 178/993 (17.9%) | 396/993 (39.9%) | 161/944 (17.1%) | 38/201 (18.9%) | 396/993 (39.9%) |
| dlad | 186/822 (22.6%) | 186/822 (22.6%) | 186/999 (18.6%) | 247/999 (24.7%) | 107/999 (10.7%) | 247/999 (24.7%) | 67/978 (6.9%) | 14/75 (18.7%) | 247/999 (24.7%) |
| d1 | 146/854 (17.1%) | 146/854 (17.1%) | 146/993 (14.7%) | 194/993 (19.5%) | 92/993 (9.3%) | 194/993 (19.5%) | 68/965 (7.0%) | 10/57 (17.5%) | 194/993 (19.5%) |
| d2 | 70/863 (8.1%) | 70/863 (8.1%) | 70/938 (7.5%) | 80/938 (8.5%) | 35/938 (3.7%) | 80/938 (8.5%) | 24/927 (2.6%) | <5/36 | 80/938 (8.5%) |
| im | 41/298 (13.8%) | 41/298 (13.8%) | 41/335 (12.2%) | 55/335 (16.4%) | 22/335 (6.6%) | 55/335 (16.4%) | 16/329 (4.9%) | 5/17 (29.4%) | 55/335 (16.4%) |
| pcx | 273/845 (32.3%) | 273/845 (32.3%) | 273/997 (27.4%) | 321/997 (32.2%) | 98/997 (9.8%) | 321/997 (32.2%) | 47/982 (4.8%) | 8/52 (15.4%) | 321/997 (32.2%) |
| om1 | 134/920 (14.6%) | 134/920 (14.6%) | 134/992 (13.5%) | 152/992 (15.3%) | 61/992 (6.1%) | 152/992 (15.3%) | 39/985 (4.0%) | <5/32 | 152/992 (15.3%) |
| mcx | 132/893 (14.8%) | 132/893 (14.8%) | 132/983 (13.4%) | 149/983 (15.2%) | 62/983 (6.3%) | 149/983 (15.2%) | 25/977 (2.6%) | <5/25 | 149/983 (15.2%) |
| om2 | 40/878 (4.6%) | 40/878 (4.6%) | 40/904 (4.4%) | 41/904 (4.5%) | 16/904 (1.8%) | 41/904 (4.5%) | 7/902 (0.8%) | 0/8 (0.0%) | 41/904 (4.5%) |
| dcx | 56/908 (6.2%) | 56/908 (6.2%) | 56/938 (6.0%) | 63/938 (6.7%) | 24/938 (2.6%) | 63/938 (6.7%) | 10/936 (1.1%) | <5/7 | 63/938 (6.7%) |
| prca | 210/723 (29.0%) | 210/723 (29.0%) | 210/937 (22.4%) | 282/937 (30.1%) | 93/937 (9.9%) | 282/937 (30.1%) | 56/924 (6.1%) | 20/75 (26.7%) | 282/937 (30.1%) |
| mrca | 246/708 (34.7%) | 246/708 (34.7%) | 246/847 (29.0%) | 318/847 (37.5%) | 129/847 (15.2%) | 318/847 (37.5%) | 83/833 (10.0%) | 12/33 (36.4%) | 318/847 (37.5%) |
| drca | 186/842 (22.1%) | 186/842 (22.1%) | 186/925 (20.1%) | 230/925 (24.9%) | 88/925 (9.5%) | 230/925 (24.9%) | 53/916 (5.8%) | 11/27 (40.7%) | 230/925 (24.9%) |
| pda | 78/957 (8.2%) | 78/957 (8.2%) | 78/984 (7.9%) | 88/984 (8.9%) | 39/984 (4.0%) | 88/984 (8.9%) | 25/982 (2.5%) | <5/10 | 88/984 (8.9%) |
| pla | 88/865 (10.2%) | 88/865 (10.2%) | 88/883 (10.0%) | 94/883 (10.6%) | 31/883 (3.5%) | 94/883 (10.6%) | 19/883 (2.2%) | <5/6 | 94/883 (10.6%) |

#### agreement between outcomes (Cohen's kappa)

| | new plaque in a plaque-free segment | plaque-free -> plaque | extent increase (+1 segment with plaque) | burden increase (sum of stenosis grades) | burden increase >= 2 | max stenosis +1 grade | incident obstructive | new high-risk feature | any plaque progression |
|---|---|---|---|---|---|---|---|---|---|
| new plaque in a plaque-free segment | 1 | 1 | 1 | 1 | 0.504 | 1 | 0.217 |  | 1 |
| plaque-free -> plaque | 1 | 1 | 1 | 1 | 0.504 | 1 | 0.217 |  | 1 |
| extent increase (+1 segment with plaque) | 1 | 1 | 1 | 0.811 | 0.452 | 0.811 | 0.145 | 0 | 0.811 |
| burden increase (sum of stenosis grades) | 1 | 1 | 0.811 | 1 | 0.482 | 1 | 0.351 | 0.0747 | 1 |
| burden increase >= 2 | 0.504 | 0.504 | 0.452 | 0.482 | 1 | 0.482 | 0.604 | 0.0679 | 0.482 |
| max stenosis +1 grade | 1 | 1 | 0.811 | 1 | 0.482 | 1 | 0.351 | 0.0747 | 1 |
| incident obstructive | 0.217 | 0.217 | 0.145 | 0.351 | 0.604 | 0.351 | 1 | 0.0698 | 0.351 |
| new high-risk feature |  |  | 0 | 0.0747 | 0.0679 | 0.0747 | 0.0698 | 1 | 0.0747 |
| any plaque progression | 1 | 1 | 0.811 | 1 | 0.482 | 1 | 0.351 | 0.0747 | 1 |

#### event % by BL max stenosis grade (ceiling/floor)

| | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| new plaque in a plaque-free segment | 2479/13168 (18.8%) | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| plaque-free -> plaque | 2479/13168 (18.8%) | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| extent increase (+1 segment with plaque) | 2479/13168 (18.8%) | 0/1325 (0.0%) | 0/939 (0.0%) | 0/171 (0.0%) | 0/38 (0.0%) | 0/14 (0.0%) |
| burden increase (sum of stenosis grades) | 2479/13168 (18.8%) | 577/1325 (43.5%) | 294/939 (31.3%) | 37/171 (21.6%) | 0/38 (0.0%) | 0/14 (0.0%) |
| burden increase >= 2 | 955/13168 (7.3%) | 205/1325 (15.5%) | 103/939 (11.0%) | 0/171 (0.0%) | 0/38 (0.0%) | 0/14 (0.0%) |
| max stenosis +1 grade | 2479/13168 (18.8%) | 577/1325 (43.5%) | 294/939 (31.3%) | 37/171 (21.6%) | 0/38 (0.0%) | 0/14 (0.0%) |
| incident obstructive | 361/13168 (2.7%) | 205/1325 (15.5%) | 294/939 (31.3%) | 0/0 | 0/0 | 0/0 |
| new high-risk feature | 0/0 | 93/481 (19.3%) | 78/432 (18.1%) | 12/70 (17.1%) | <5/13 | 0/5 (0.0%) |
| any plaque progression | 2479/13168 (18.8%) | 577/1325 (43.5%) | 294/939 (31.3%) | 37/171 (21.6%) | 0/38 (0.0%) | 0/14 (0.0%) |

#### event % by BL plaque

| | no plaque at BL | plaque at BL |
|---|---|---|
| new plaque in a plaque-free segment | 2479/13168 (18.8%) | 0/0 |
| plaque-free -> plaque | 2479/13168 (18.8%) | 0/0 |
| extent increase (+1 segment with plaque) | 2479/13168 (18.8%) | 0/2487 (0.0%) |
| burden increase (sum of stenosis grades) | 2479/13168 (18.8%) | 908/2487 (36.5%) |
| burden increase >= 2 | 955/13168 (7.3%) | 308/2487 (12.4%) |
| max stenosis +1 grade | 2479/13168 (18.8%) | 908/2487 (36.5%) |
| incident obstructive | 361/13168 (2.7%) | 499/2264 (22.0%) |
| new high-risk feature | 0/0 | 185/1001 (18.5%) |
| any plaque progression | 2479/13168 (18.8%) | 908/2487 (36.5%) |

#### event % by follow-up interval tertile (should rise with time)

| | 1 short | 2 middle | 3 long |
|---|---|---|---|
| new plaque in a plaque-free segment | 835/4695 (17.8%) | 659/3882 (17.0%) | 985/4591 (21.5%) |
| plaque-free -> plaque | 835/4695 (17.8%) | 659/3882 (17.0%) | 985/4591 (21.5%) |
| extent increase (+1 segment with plaque) | 835/5645 (14.8%) | 659/4742 (13.9%) | 985/5268 (18.7%) |
| burden increase (sum of stenosis grades) | 1182/5645 (20.9%) | 962/4742 (20.3%) | 1243/5268 (23.6%) |
| burden increase >= 2 | 439/5645 (7.8%) | 355/4742 (7.5%) | 469/5268 (8.9%) |
| max stenosis +1 grade | 1182/5645 (20.9%) | 962/4742 (20.3%) | 1243/5268 (23.6%) |
| incident obstructive | 291/5573 (5.2%) | 265/4661 (5.7%) | 304/5198 (5.8%) |
| new high-risk feature | 66/375 (17.6%) | 72/375 (19.2%) | 47/251 (18.7%) |
| any plaque progression | 1182/5645 (20.9%) | 962/4742 (20.3%) | 1243/5268 (23.6%) |

#### AUC of single BL predictors (0.5 = no signal)

| | BL extent | BL burden | BL max stenosis | scan_age | male | ldl | hdl | clin_bp_sys_mean | hist_smoking_current | hist_diabetes | med_lipid_lowering_any | ct_cacs_sum | follow-up years |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new plaque in a plaque-free segment | 0.5 | 0.5 | 0.5 | 0.592 | 0.604 | 0.541 | 0.448 | 0.595 | 0.506 | 0.499 | 0.525 | 0.68 | 0.532 |
| plaque-free -> plaque | 0.5 | 0.5 | 0.5 | 0.592 | 0.604 | 0.541 | 0.448 | 0.595 | 0.506 | 0.499 | 0.525 | 0.68 | 0.532 |
| extent increase (+1 segment with plaque) | 0.406 | 0.406 | 0.406 | 0.565 | 0.585 | 0.539 | 0.454 | 0.573 | 0.506 | 0.499 | 0.517 | 0.621 | 0.539 |
| burden increase (sum of stenosis grades) | 0.57 | 0.567 | 0.567 | 0.595 | 0.593 | 0.536 | 0.455 | 0.587 | 0.505 | 0.498 | 0.525 | 0.683 | 0.523 |
| burden increase >= 2 | 0.546 | 0.543 | 0.543 | 0.594 | 0.598 | 0.539 | 0.455 | 0.592 | 0.502 | 0.499 | 0.517 | 0.695 | 0.528 |
| max stenosis +1 grade | 0.57 | 0.567 | 0.567 | 0.595 | 0.593 | 0.536 | 0.455 | 0.587 | 0.505 | 0.498 | 0.525 | 0.683 | 0.523 |
| incident obstructive | 0.73 | 0.737 | 0.737 | 0.623 | 0.596 | 0.537 | 0.46 | 0.605 | 0.5 | 0.498 | 0.519 | 0.761 | 0.519 |
| new high-risk feature | 0.5 | 0.483 | 0.483 | 0.487 | 0.559 | 0.493 | 0.464 | 0.493 | 0.512 | 0.492 | 0.513 | 0.492 | 0.52 |
| any plaque progression | 0.57 | 0.567 | 0.567 | 0.595 | 0.593 | 0.536 | 0.455 | 0.587 | 0.505 | 0.498 | 0.525 | 0.683 | 0.523 |

#### continuous change (zero-inflation, skew)

| | n | mean | sd | p5 | p25 | median | p75 | p95 | pct zero | pct negative |
|---|---|---|---|---|---|---|---|---|---|---|
| change in extent | 15655 | 0.126 | 0.418 | 0 | 0 | 0 | 0 | 1 | 80.9 | 3.2 |
| change in burden | 15655 | 0.263 | 0.83 | 0 | 0 | 0 | 0 | 2 | 73.4 | 4.9 |
| change in max stenosis | 15655 | 0.263 | 0.83 | 0 | 0 | 0 | 0 | 2 | 73.4 | 4.9 |

#### trajectory groups (pooled)

##### extent

| | n | pct |
|---|---|---|
| no plaque -> no plaque | 10689 | 68.3 |
| no plaque -> plaque | 2479 | 15.8 |
| plaque -> same | 1983 | 12.7 |
| plaque -> more | 0 | 0 |
| plaque -> less | 504 | 3.2 |
| missing | 0 |  |

##### burden (presence from extent)

| | n | pct |
|---|---|---|
| no plaque -> no plaque | 10689 | 68.3 |
| no plaque -> plaque | 2479 | 15.8 |
| plaque -> same | 806 | 5.1 |
| plaque -> more | 908 | 5.8 |
| plaque -> less | 773 | 4.9 |
| missing | 0 |  |

#### % of whole-tree events that occur in this unit

| | new plaque in a plaque-free segment | plaque-free -> plaque | extent increase (+1 segment with plaque) | burden increase (sum of stenosis grades) | burden increase >= 2 | max stenosis +1 grade | incident obstructive | new high-risk feature | any plaque progression |
|---|---|---|---|---|---|---|---|---|---|
| lm | 33.3 | 24.6 | 27.9 | 33.5 | 8.1 | 34.5 | 4.3 | 33.3 | 31.1 |
| plad | 67.7 | 60.8 | 27.2 | 57.5 | 20.7 | 64.6 | 38.8 | 68.6 | 53.8 |
| mlad | 55.6 | 42.5 | 28 | 54.2 | 29 | 60.3 | 46 | 55.9 | 49.9 |
| dlad | 31.2 | 19.3 | 26.3 | 33.6 | 17.8 | 34.4 | 19.6 | 56 | 31.3 |
| d1 | 23.1 | 13.6 | 20.5 | 26.6 | 14.7 | 27.4 | 18.5 | 47.6 | 24.6 |
| d2 | 10.9 | 6.7 | 10.6 | 11.6 | 5.6 | 11.5 | 7.3 | <5 | 10.8 |
| im | 17.9 | <5 | 17.5 | 22.4 | 9.8 | 25.4 | 12.1 | hidden | 20.2 |
| pcx | 43.6 | 24 | 38.6 | 42.9 | 16 | 40.6 | 10.5 | 53.3 | 40.5 |
| om1 | 19.3 | 8.3 | 19 | 21 | 9.9 | 19.7 | 8.3 | <5 | 19.3 |
| mcx | 19.7 | 8.6 | 19.6 | 20.9 | 10.3 | 19.2 | 5.4 | <5 | 19 |
| om2 | 6 | 0 | 6.2 | 6.3 | 3 | 6.3 | 2.4 | hidden | 5.7 |
| dcx | 8.1 | <5 | 8.4 | 8.7 | 4.1 | 8.3 | 2.6 | <5 | 8.3 |
| prca | 39.8 | 18.8 | 32.1 | 41 | 16.2 | 39.9 | 15.1 | 66.7 | 37.6 |
| mrca | 46.5 | 28.7 | 40.6 | 49.7 | 24 | 51.8 | 25.6 | hidden | 46.6 |
| drca | 29.2 | 5.6 | 28.3 | 32.8 | 15.5 | 34.4 | 12.6 | hidden | 31 |
| pda | 10.7 | <5 | 11.2 | 12 | 6.4 | 12.4 | 6.3 | <5 | 11.3 |
| pla | 13.3 | <5 | 14.8 | 14.8 | 5.7 | 13.2 | 5.3 | <5 | 13.5 |

### level: position

#### units (segments in each)

| | |
|---|---|
| proximal (LM, pLAD, pCX, pRCA) | lm, plad, pcx, prca |
| mid | mlad, mcx, mrca |
| distal | dlad, dcx, drca |
| side branches | d1, d2, om1, om2, im, pda, pla |

#### outcome summary (all units pooled)

| | n units | events | pct | regression events | regression pct | progression : regression | patients with event | ICC within patient | design effect | max predictors at 10 EPV |
|---|---|---|---|---|---|---|---|---|---|---|
| new plaque in a plaque-free segment | 3972 | 1761 | 44.3 | 456 | 27.2 | 3.86 | 777 | 0.281 | 1.81 | 176 |
| plaque-free -> plaque | 2386 | 919 | 38.5 | 186 | 11.1 | 4.94 | 585 | 0.382 | 1.62 | 91 |
| extent increase (+1 segment with plaque) | 4062 | 1622 | 39.9 | 296 | 7.3 | 5.48 | 750 | 0.25 | 1.74 | 162 |
| burden increase (sum of stenosis grades) | 4062 | 1879 | 46.3 | 384 | 9.5 | 4.89 | 789 | 0.295 | 1.88 | 187 |
| burden increase >= 2 | 4062 | 1195 | 29.4 | 143 | 3.5 | 8.36 | 597 | 0.298 | 1.89 | 119 |
| max stenosis +1 grade | 4062 | 1666 | 41 | 387 | 9.5 | 4.3 | 761 | 0.261 | 1.78 | 166 |
| incident obstructive | 3867 | 642 | 16.6 | 68 | 34.9 | 9.44 | 366 | 0.342 | 1.96 | 64 |
| new high-risk feature | 837 | 173 | 20.7 | 857 | 75.2 | 0.2 | 142 | 0.263 | 1.16 | 17 |
| any plaque progression | 4062 | 2070 | 51 | 614 | 15.1 | 3.37 | 809 | 0.335 | 2 | 199 |

#### events / n (%) per unit

| | new plaque in a plaque-free segment | plaque-free -> plaque | extent increase (+1 segment with plaque) | burden increase (sum of stenosis grades) | burden increase >= 2 | max stenosis +1 grade | incident obstructive | new high-risk feature | any plaque progression |
|---|---|---|---|---|---|---|---|---|---|
| proximal (LM, pLAD, pCX, pRCA) | 579/986 (58.7%) | 181/362 (50.0%) | 539/1019 (52.9%) | 605/1019 (59.4%) | 409/1019 (40.1%) | 477/1019 (46.8%) | 188/963 (19.5%) | 75/355 (21.1%) | 670/1019 (65.8%) |
| mid | 443/959 (46.2%) | 228/511 (44.6%) | 415/1010 (41.1%) | 520/1010 (51.5%) | 330/1010 (32.7%) | 478/1010 (47.3%) | 208/949 (21.9%) | 49/239 (20.5%) | 569/1010 (56.3%) |
| distal | 348/1010 (34.5%) | 262/777 (33.7%) | 327/1016 (32.2%) | 381/1016 (37.5%) | 212/1016 (20.9%) | 362/1016 (35.6%) | 108/988 (10.9%) | 26/105 (24.8%) | 406/1016 (40.0%) |
| side branches | 391/1017 (38.4%) | 248/736 (33.7%) | 341/1017 (33.5%) | 373/1017 (36.7%) | 244/1017 (24.0%) | 349/1017 (34.3%) | 138/967 (14.3%) | 23/138 (16.7%) | 425/1017 (41.8%) |

#### agreement between outcomes (Cohen's kappa)

| | new plaque in a plaque-free segment | plaque-free -> plaque | extent increase (+1 segment with plaque) | burden increase (sum of stenosis grades) | burden increase >= 2 | max stenosis +1 grade | incident obstructive | new high-risk feature | any plaque progression |
|---|---|---|---|---|---|---|---|---|---|
| new plaque in a plaque-free segment | 1 | 1 | 0.928 | 0.799 | 0.589 | 0.678 | 0.239 | 0.0292 | 0.87 |
| plaque-free -> plaque | 1 | 1 | 1 | 1 | 0.641 | 1 | 0.219 |  | 1 |
| extent increase (+1 segment with plaque) | 0.928 | 1 | 1 | 0.809 | 0.626 | 0.686 | 0.231 | 0.108 | 0.78 |
| burden increase (sum of stenosis grades) | 0.799 | 1 | 0.809 | 1 | 0.652 | 0.859 | 0.353 | 0.0802 | 0.906 |
| burden increase >= 2 | 0.589 | 0.641 | 0.626 | 0.652 | 1 | 0.641 | 0.531 | 0.104 | 0.573 |
| max stenosis +1 grade | 0.678 | 1 | 0.686 | 0.859 | 0.641 | 1 | 0.432 | 0.0581 | 0.802 |
| incident obstructive | 0.239 | 0.219 | 0.231 | 0.353 | 0.531 | 0.432 | 1 | 0.079 | 0.33 |
| new high-risk feature | 0.0292 |  | 0.108 | 0.0802 | 0.104 | 0.0581 | 0.079 | 1 | 0.0301 |
| any plaque progression | 0.87 | 1 | 0.78 | 0.906 | 0.573 | 0.802 | 0.33 | 0.0301 | 1 |

#### event % by BL max stenosis grade (ceiling/floor)

| | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| new plaque in a plaque-free segment | 919/2386 (38.5%) | 375/746 (50.3%) | 368/674 (54.6%) | 75/124 (60.5%) | 20/33 (60.6%) | <5/9 |
| plaque-free -> plaque | 919/2386 (38.5%) | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| extent increase (+1 segment with plaque) | 919/2386 (38.5%) | 307/761 (40.3%) | 317/720 (44.0%) | 60/145 (41.4%) | 15/37 (40.5%) | <5/13 |
| burden increase (sum of stenosis grades) | 919/2386 (38.5%) | 473/761 (62.2%) | 398/720 (55.3%) | 73/145 (50.3%) | 13/37 (35.1%) | <5/13 |
| burden increase >= 2 | 544/2386 (22.8%) | 320/761 (42.0%) | 280/720 (38.9%) | 44/145 (30.3%) | 7/37 (18.9%) | 0/13 (0.0%) |
| max stenosis +1 grade | 919/2386 (38.5%) | 401/761 (52.7%) | 303/720 (42.1%) | 42/145 (29.0%) | <5/37 | 0/13 (0.0%) |
| incident obstructive | 171/2386 (7.2%) | 168/761 (22.1%) | 303/720 (42.1%) | 0/0 | 0/0 | 0/0 |
| new high-risk feature | 0/0 | 68/325 (20.9%) | 83/398 (20.9%) | 17/84 (20.2%) | 5/21 (23.8%) | 0/9 (0.0%) |
| any plaque progression | 919/2386 (38.5%) | 529/761 (69.5%) | 493/720 (68.5%) | 101/145 (69.7%) | 23/37 (62.2%) | 5/13 (38.5%) |

#### event % by BL plaque

| | no plaque at BL | plaque at BL |
|---|---|---|
| new plaque in a plaque-free segment | 919/2386 (38.5%) | 842/1586 (53.1%) |
| plaque-free -> plaque | 919/2386 (38.5%) | 0/0 |
| extent increase (+1 segment with plaque) | 919/2386 (38.5%) | 703/1676 (41.9%) |
| burden increase (sum of stenosis grades) | 919/2386 (38.5%) | 960/1676 (57.3%) |
| burden increase >= 2 | 544/2386 (22.8%) | 651/1676 (38.8%) |
| max stenosis +1 grade | 919/2386 (38.5%) | 747/1676 (44.6%) |
| incident obstructive | 171/2386 (7.2%) | 471/1481 (31.8%) |
| new high-risk feature | 0/0 | 173/837 (20.7%) |
| any plaque progression | 919/2386 (38.5%) | 1151/1676 (68.7%) |

#### event % by follow-up interval tertile (should rise with time)

| | 1 short | 2 middle | 3 long |
|---|---|---|---|
| new plaque in a plaque-free segment | 607/1442 (42.1%) | 500/1191 (42.0%) | 654/1339 (48.8%) |
| plaque-free -> plaque | 311/843 (36.9%) | 227/656 (34.6%) | 381/887 (43.0%) |
| extent increase (+1 segment with plaque) | 554/1475 (37.6%) | 450/1227 (36.7%) | 618/1360 (45.4%) |
| burden increase (sum of stenosis grades) | 668/1475 (45.3%) | 541/1227 (44.1%) | 670/1360 (49.3%) |
| burden increase >= 2 | 434/1475 (29.4%) | 328/1227 (26.7%) | 433/1360 (31.8%) |
| max stenosis +1 grade | 603/1475 (40.9%) | 466/1227 (38.0%) | 597/1360 (43.9%) |
| incident obstructive | 224/1409 (15.9%) | 199/1157 (17.2%) | 219/1301 (16.8%) |
| new high-risk feature | 63/310 (20.3%) | 70/309 (22.7%) | 40/218 (18.3%) |
| any plaque progression | 734/1475 (49.8%) | 614/1227 (50.0%) | 722/1360 (53.1%) |

#### AUC of single BL predictors (0.5 = no signal)

| | BL extent | BL burden | BL max stenosis | scan_age | male | ldl | hdl | clin_bp_sys_mean | hist_smoking_current | hist_diabetes | med_lipid_lowering_any | ct_cacs_sum | follow-up years |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new plaque in a plaque-free segment | 0.575 | 0.577 | 0.576 | 0.594 | 0.616 | 0.55 | 0.445 | 0.6 | 0.506 | 0.498 | 0.526 | 0.691 | 0.537 |
| plaque-free -> plaque | 0.5 | 0.5 | 0.5 | 0.604 | 0.63 | 0.565 | 0.438 | 0.606 | 0.502 | 0.498 | 0.515 | 0.706 | 0.538 |
| extent increase (+1 segment with plaque) | 0.512 | 0.515 | 0.519 | 0.576 | 0.602 | 0.553 | 0.446 | 0.58 | 0.51 | 0.499 | 0.518 | 0.651 | 0.545 |
| burden increase (sum of stenosis grades) | 0.593 | 0.586 | 0.582 | 0.602 | 0.614 | 0.548 | 0.45 | 0.598 | 0.502 | 0.499 | 0.522 | 0.703 | 0.526 |
| burden increase >= 2 | 0.601 | 0.593 | 0.585 | 0.614 | 0.606 | 0.541 | 0.442 | 0.599 | 0.506 | 0.502 | 0.526 | 0.7 | 0.522 |
| max stenosis +1 grade | 0.538 | 0.525 | 0.514 | 0.596 | 0.59 | 0.546 | 0.46 | 0.585 | 0.5 | 0.5 | 0.514 | 0.668 | 0.524 |
| incident obstructive | 0.734 | 0.745 | 0.737 | 0.641 | 0.605 | 0.542 | 0.454 | 0.611 | 0.498 | 0.501 | 0.522 | 0.784 | 0.516 |
| new high-risk feature | 0.553 | 0.533 | 0.493 | 0.506 | 0.554 | 0.48 | 0.466 | 0.515 | 0.518 | 0.49 | 0.51 | 0.502 | 0.498 |
| any plaque progression | 0.655 | 0.65 | 0.644 | 0.62 | 0.626 | 0.542 | 0.445 | 0.612 | 0.501 | 0.497 | 0.531 | 0.738 | 0.521 |

#### continuous change (zero-inflation, skew)

| | n | mean | sd | p5 | p25 | median | p75 | p95 | pct zero | pct negative |
|---|---|---|---|---|---|---|---|---|---|---|
| change in extent | 4062 | 0.486 | 0.921 | -1 | 0 | 0 | 1 | 2 | 52.8 | 7.3 |
| change in burden | 4062 | 1.01 | 1.92 | -1 | 0 | 0 | 2 | 5 | 44.3 | 9.5 |
| change in max stenosis | 4062 | 0.524 | 1.11 | -1 | 0 | 0 | 1 | 3 | 49.5 | 9.5 |

#### trajectory groups (pooled)

##### extent

| | n | pct |
|---|---|---|
| no plaque -> no plaque | 1467 | 36.1 |
| no plaque -> plaque | 919 | 22.6 |
| plaque -> same | 677 | 16.7 |
| plaque -> more | 703 | 17.3 |
| plaque -> less | 296 | 7.3 |
| missing | 0 |  |

##### burden (presence from extent)

| | n | pct |
|---|---|---|
| no plaque -> no plaque | 1467 | 36.1 |
| no plaque -> plaque | 919 | 22.6 |
| plaque -> same | 332 | 8.2 |
| plaque -> more | 960 | 23.6 |
| plaque -> less | 384 | 9.5 |
| missing | 0 |  |

#### % of whole-tree events that occur in this unit

| | new plaque in a plaque-free segment | plaque-free -> plaque | extent increase (+1 segment with plaque) | burden increase (sum of stenosis grades) | burden increase >= 2 | max stenosis +1 grade | incident obstructive | new high-risk feature | any plaque progression |
|---|---|---|---|---|---|---|---|---|---|
| proximal (LM, pLAD, pCX, pRCA) | 77.3 | 83.1 | 75.6 | 80.9 | 63.8 | 74.1 | 52.1 | 72.8 | 83 |
| mid | 60.9 | 55.3 | 58.5 | 70.8 | 52.8 | 72.4 | 61.4 | 62 | 70.7 |
| distal | 45.3 | 23.8 | 46.1 | 51 | 34.4 | 49.5 | 29.5 | 68.4 | 50.5 |
| side branches | 50.4 | 25 | 48.7 | 50.9 | 39.1 | 51.5 | 39.9 | 48.9 | 52.8 |

### level: vessel

#### units (segments in each)

| | |
|---|---|
| LM | lm |
| LAD | plad, mlad, dlad, d1, d2 |
| CX | pcx, mcx, dcx, om1, om2 |
| RCA | prca, mrca, drca, pda, pla |

#### outcome summary (all units pooled)

| | n units | events | pct | regression events | regression pct | progression : regression | patients with event | ICC within patient | design effect | max predictors at 10 EPV |
|---|---|---|---|---|---|---|---|---|---|---|
| new plaque in a plaque-free segment | 3801 | 1636 | 43 | 416 | 28.8 | 3.93 | 777 | 0.235 | 1.64 | 163 |
| plaque-free -> plaque | 2591 | 893 | 34.5 | 123 | 8.5 | 7.26 | 599 | 0.272 | 1.46 | 89 |
| extent increase (+1 segment with plaque) | 4033 | 1485 | 36.8 | 240 | 6 | 6.19 | 737 | 0.187 | 1.55 | 148 |
| burden increase (sum of stenosis grades) | 4033 | 1754 | 43.5 | 282 | 7 | 6.22 | 783 | 0.242 | 1.72 | 175 |
| burden increase >= 2 | 4033 | 1060 | 26.3 | 119 | 3 | 8.91 | 576 | 0.213 | 1.63 | 106 |
| max stenosis +1 grade | 4033 | 1567 | 38.9 | 277 | 6.9 | 5.66 | 751 | 0.232 | 1.68 | 156 |
| incident obstructive | 3857 | 512 | 13.3 | 52 | 29.5 | 9.85 | 348 | 0.186 | 1.52 | 51 |
| new high-risk feature | 739 | 158 | 21.4 | 777 | 75.9 | 0.2 | 140 | 0.238 | 1.11 | 15 |
| any plaque progression | 4033 | 1903 | 47.2 | 527 | 13.1 | 3.61 | 810 | 0.245 | 1.72 | 190 |
| CAC increase | 8426 | 2930 | 34.8 | 218 | 2.6 | 13.4 | 1291 | 0.383 | 2.15 | 293 |
| CAC progression (Hokanson) | 8426 | 2181 | 25.9 | 88 | 1 | 24.8 | 1085 | 0.331 | 1.99 | 218 |
| incident CAC | 6809 | 1540 | 22.6 | 104 | 6.4 | 14.8 | 1020 | 0.299 | 1.7 | 154 |

#### events / n (%) per unit

| | new plaque in a plaque-free segment | plaque-free -> plaque | extent increase (+1 segment with plaque) | burden increase (sum of stenosis grades) | burden increase >= 2 | max stenosis +1 grade | incident obstructive | new high-risk feature | any plaque progression | CAC increase | CAC progression (Hokanson) | incident CAC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LM | 196/802 (24.4%) | 196/802 (24.4%) | 196/1004 (19.5%) | 248/1004 (24.7%) | 51/1004 (5.1%) | 248/1004 (24.7%) | 19/1004 (1.9%) | 9/104 (8.7%) | 248/1004 (24.7%) | 438/2107 (20.8%) | 308/2107 (14.6%) | 315/1904 (16.5%) |
| LAD | 539/996 (54.1%) | 139/321 (43.3%) | 455/1015 (44.8%) | 594/1015 (58.5%) | 409/1015 (40.3%) | 496/1015 (48.9%) | 241/896 (26.9%) | 94/405 (23.2%) | 682/1015 (67.2%) | 1138/2105 (54.1%) | 848/2105 (40.3%) | 475/1384 (34.3%) |
| CX | 427/1004 (42.5%) | 277/757 (36.6%) | 378/1011 (37.4%) | 416/1011 (41.1%) | 248/1011 (24.5%) | 379/1011 (37.5%) | 98/983 (10.0%) | 12/101 (11.9%) | 457/1011 (45.2%) | 648/2107 (30.8%) | 461/2107 (21.9%) | 382/1798 (21.2%) |
| RCA | 474/999 (47.4%) | 281/711 (39.5%) | 456/1003 (45.5%) | 496/1003 (49.5%) | 352/1003 (35.1%) | 444/1003 (44.3%) | 154/974 (15.8%) | 43/129 (33.3%) | 516/1003 (51.4%) | 706/2107 (33.5%) | 564/2107 (26.8%) | 368/1723 (21.4%) |

#### agreement between outcomes (Cohen's kappa)

| | new plaque in a plaque-free segment | plaque-free -> plaque | extent increase (+1 segment with plaque) | burden increase (sum of stenosis grades) | burden increase >= 2 | max stenosis +1 grade | incident obstructive | new high-risk feature | any plaque progression | CAC increase | CAC progression (Hokanson) | incident CAC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new plaque in a plaque-free segment | 1 | 1 | 0.918 | 0.846 | 0.565 | 0.733 | 0.221 | 0.025 | 0.895 | 0.663 | 0.542 | 0.763 |
| plaque-free -> plaque | 1 | 1 | 1 | 1 | 0.582 | 1 | 0.18 |  | 1 | 0.789 | 0.615 | 0.802 |
| extent increase (+1 segment with plaque) | 0.918 | 1 | 1 | 0.826 | 0.593 | 0.71 | 0.208 | 0.108 | 0.79 | 0.54 | 0.466 | 0.689 |
| burden increase (sum of stenosis grades) | 0.846 | 1 | 0.826 | 1 | 0.633 | 0.862 | 0.308 | 0.0483 | 0.926 | 0.655 | 0.561 | 0.728 |
| burden increase >= 2 | 0.565 | 0.582 | 0.593 | 0.633 | 1 | 0.607 | 0.525 | 0.109 | 0.571 | 0.442 | 0.483 | 0.465 |
| max stenosis +1 grade | 0.733 | 1 | 0.71 | 0.862 | 0.607 | 1 | 0.38 | 0.0988 | 0.831 | 0.567 | 0.488 | 0.709 |
| incident obstructive | 0.221 | 0.18 | 0.208 | 0.308 | 0.525 | 0.38 | 1 | 0.0637 | 0.304 | 0.251 | 0.311 | 0.164 |
| new high-risk feature | 0.025 |  | 0.108 | 0.0483 | 0.109 | 0.0988 | 0.0637 | 1 | 0.0536 | 0.0828 | 0.0897 | 0.185 |
| any plaque progression | 0.895 | 1 | 0.79 | 0.926 | 0.571 | 0.831 | 0.304 | 0.0536 | 1 | 0.714 | 0.592 | 0.749 |
| CAC increase | 0.663 | 0.789 | 0.54 | 0.655 | 0.442 | 0.567 | 0.251 | 0.0828 | 0.714 | 1 | 0.792 | 1 |
| CAC progression (Hokanson) | 0.542 | 0.615 | 0.466 | 0.561 | 0.483 | 0.488 | 0.311 | 0.0897 | 0.592 | 0.792 | 1 | 0.794 |
| incident CAC | 0.763 | 0.802 | 0.689 | 0.728 | 0.465 | 0.709 | 0.164 | 0.185 | 0.749 | 1 | 0.794 | 1 |

#### event % by BL max stenosis grade (ceiling/floor)

| | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| new plaque in a plaque-free segment | 893/2591 (34.5%) | 345/566 (61.0%) | 302/480 (62.9%) | 79/127 (62.2%) | 15/25 (60.0%) | <5/12 |
| plaque-free -> plaque | 893/2591 (34.5%) | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| extent increase (+1 segment with plaque) | 893/2591 (34.5%) | 284/725 (39.2%) | 233/541 (43.1%) | 62/134 (46.3%) | 11/30 (36.7%) | <5/12 |
| burden increase (sum of stenosis grades) | 893/2591 (34.5%) | 445/725 (61.4%) | 325/541 (60.1%) | 76/134 (56.7%) | 13/30 (43.3%) | <5/12 |
| burden increase >= 2 | 460/2591 (17.8%) | 297/725 (41.0%) | 240/541 (44.4%) | 57/134 (42.5%) | 5/30 (16.7%) | <5/12 |
| max stenosis +1 grade | 893/2591 (34.5%) | 388/725 (53.5%) | 241/541 (44.5%) | 45/134 (33.6%) | 0/30 (0.0%) | 0/12 (0.0%) |
| incident obstructive | 128/2591 (4.9%) | 143/725 (19.7%) | 241/541 (44.5%) | 0/0 | 0/0 | 0/0 |
| new high-risk feature | 0/0 | 60/294 (20.4%) | 69/330 (20.9%) | 23/84 (27.4%) | 5/22 (22.7%) | <5/9 |
| any plaque progression | 893/2591 (34.5%) | 484/725 (66.8%) | 401/541 (74.1%) | 104/134 (77.6%) | 18/30 (60.0%) | <5/12 |
| CAC increase | 809/2586 (31.3%) | 579/724 (80.0%) | 477/541 (88.2%) | 127/133 (95.5%) | hidden/30 | hidden/12 |
| CAC progression (Hokanson) | 576/2586 (22.3%) | 451/724 (62.3%) | 388/541 (71.7%) | 108/133 (81.2%) | 25/30 (83.3%) | hidden/12 |
| incident CAC | 646/2363 (27.3%) | 151/241 (62.7%) | 58/85 (68.2%) | hidden/16 | <5/5 | <5/<5 |

#### event % by BL plaque

| | no plaque at BL | plaque at BL |
|---|---|---|
| new plaque in a plaque-free segment | 893/2591 (34.5%) | 743/1210 (61.4%) |
| plaque-free -> plaque | 893/2591 (34.5%) | 0/0 |
| extent increase (+1 segment with plaque) | 893/2591 (34.5%) | 592/1442 (41.1%) |
| burden increase (sum of stenosis grades) | 893/2591 (34.5%) | 861/1442 (59.7%) |
| burden increase >= 2 | 460/2591 (17.8%) | 600/1442 (41.6%) |
| max stenosis +1 grade | 893/2591 (34.5%) | 674/1442 (46.7%) |
| incident obstructive | 128/2591 (4.9%) | 384/1266 (30.3%) |
| new high-risk feature | 0/0 | 158/739 (21.4%) |
| any plaque progression | 893/2591 (34.5%) | 1010/1442 (70.0%) |
| CAC increase | 809/2586 (31.3%) | 1223/1440 (84.9%) |
| CAC progression (Hokanson) | 576/2586 (22.3%) | 980/1440 (68.1%) |
| incident CAC | 646/2363 (27.3%) | 228/349 (65.3%) |

#### event % by follow-up interval tertile (should rise with time)

| | 1 short | 2 middle | 3 long |
|---|---|---|---|
| new plaque in a plaque-free segment | 567/1379 (41.1%) | 452/1129 (40.0%) | 617/1293 (47.7%) |
| plaque-free -> plaque | 308/926 (33.3%) | 224/729 (30.7%) | 361/936 (38.6%) |
| extent increase (+1 segment with plaque) | 511/1460 (35.0%) | 398/1221 (32.6%) | 576/1352 (42.6%) |
| burden increase (sum of stenosis grades) | 623/1460 (42.7%) | 506/1221 (41.4%) | 625/1352 (46.2%) |
| burden increase >= 2 | 362/1460 (24.8%) | 309/1221 (25.3%) | 389/1352 (28.8%) |
| max stenosis +1 grade | 564/1460 (38.6%) | 446/1221 (36.5%) | 557/1352 (41.2%) |
| incident obstructive | 180/1400 (12.9%) | 154/1158 (13.3%) | 178/1299 (13.7%) |
| new high-risk feature | 57/269 (21.2%) | 59/273 (21.6%) | 42/197 (21.3%) |
| any plaque progression | 677/1460 (46.4%) | 550/1221 (45.0%) | 676/1352 (50.0%) |
| CAC increase | 967/2824 (34.2%) | 895/2800 (32.0%) | 1068/2802 (38.1%) |
| CAC progression (Hokanson) | 676/2824 (23.9%) | 644/2800 (23.0%) | 861/2802 (30.7%) |
| incident CAC | 458/2199 (20.8%) | 434/2261 (19.2%) | 648/2349 (27.6%) |

#### AUC of single BL predictors (0.5 = no signal)

| | BL extent | BL burden | BL max stenosis | scan_age | male | ldl | hdl | clin_bp_sys_mean | hist_smoking_current | hist_diabetes | med_lipid_lowering_any | ct_cacs_sum | follow-up years |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new plaque in a plaque-free segment | 0.613 | 0.615 | 0.619 | 0.606 | 0.606 | 0.548 | 0.45 | 0.603 | 0.513 | 0.498 | 0.533 | 0.701 | 0.535 |
| plaque-free -> plaque | 0.5 | 0.5 | 0.5 | 0.611 | 0.608 | 0.56 | 0.432 | 0.616 | 0.51 | 0.5 | 0.527 | 0.697 | 0.539 |
| extent increase (+1 segment with plaque) | 0.526 | 0.53 | 0.535 | 0.578 | 0.593 | 0.55 | 0.453 | 0.579 | 0.513 | 0.498 | 0.522 | 0.648 | 0.545 |
| burden increase (sum of stenosis grades) | 0.622 | 0.619 | 0.615 | 0.608 | 0.599 | 0.552 | 0.451 | 0.598 | 0.509 | 0.499 | 0.529 | 0.702 | 0.523 |
| burden increase >= 2 | 0.651 | 0.648 | 0.641 | 0.598 | 0.609 | 0.54 | 0.449 | 0.598 | 0.504 | 0.499 | 0.527 | 0.697 | 0.531 |
| max stenosis +1 grade | 0.569 | 0.559 | 0.548 | 0.603 | 0.586 | 0.546 | 0.456 | 0.588 | 0.505 | 0.5 | 0.527 | 0.676 | 0.524 |
| incident obstructive | 0.775 | 0.783 | 0.772 | 0.63 | 0.596 | 0.534 | 0.449 | 0.606 | 0.505 | 0.501 | 0.522 | 0.763 | 0.516 |
| new high-risk feature | 0.584 | 0.566 | 0.519 | 0.504 | 0.562 | 0.497 | 0.459 | 0.495 | 0.509 | 0.49 | 0.503 | 0.492 | 0.508 |
| any plaque progression | 0.675 | 0.674 | 0.668 | 0.62 | 0.604 | 0.55 | 0.452 | 0.604 | 0.51 | 0.499 | 0.535 | 0.726 | 0.522 |
| CAC increase | 0.756 | 0.757 | 0.754 | 0.674 | 0.625 | 0.567 | 0.436 | 0.635 | 0.519 | 0.511 | 0.541 | 0.788 | 0.521 |
| CAC progression (Hokanson) | 0.734 | 0.735 | 0.731 | 0.662 | 0.624 | 0.554 | 0.437 | 0.631 | 0.516 | 0.511 | 0.539 | 0.781 | 0.543 |
| incident CAC | 0.598 | 0.599 | 0.598 | 0.621 | 0.609 | 0.575 | 0.444 | 0.622 | 0.524 | 0.509 | 0.522 | 0.669 | 0.549 |

#### continuous change (zero-inflation, skew)

| | n | mean | sd | p5 | p25 | median | p75 | p95 | pct zero | pct negative |
|---|---|---|---|---|---|---|---|---|---|---|
| change in extent | 4033 | 0.482 | 0.951 | -1 | 0 | 0 | 1 | 2 | 57.2 | 6 |
| change in burden | 4033 | 1 | 2.02 | -1 | 0 | 0 | 2 | 5 | 49.5 | 7 |
| change in max stenosis | 4033 | 0.498 | 0.992 | -1 | 0 | 0 | 1 | 2 | 54.3 | 6.9 |
| change in sqrt CAC | 8426 | 1.81 | 3.65 | 0 | 0 | 0 | 2.83 | 9.22 | 62.6 | 2.6 |

#### trajectory groups (pooled)

##### extent

| | n | pct |
|---|---|---|
| no plaque -> no plaque | 1698 | 42.1 |
| no plaque -> plaque | 893 | 22.1 |
| plaque -> same | 610 | 15.1 |
| plaque -> more | 592 | 14.7 |
| plaque -> less | 240 | 6 |
| missing | 0 |  |

##### burden (presence from extent)

| | n | pct |
|---|---|---|
| no plaque -> no plaque | 1698 | 42.1 |
| no plaque -> plaque | 893 | 22.1 |
| plaque -> same | 299 | 7.4 |
| plaque -> more | 861 | 21.3 |
| plaque -> less | 282 | 7 |
| missing | 0 |  |

#### % of whole-tree events that occur in this unit

| | new plaque in a plaque-free segment | plaque-free -> plaque | extent increase (+1 segment with plaque) | burden increase (sum of stenosis grades) | burden increase >= 2 | max stenosis +1 grade | incident obstructive | new high-risk feature | any plaque progression | CAC increase | CAC progression (Hokanson) | incident CAC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LM | 33.3 | 24.6 | 27.9 | 33.5 | 8.1 | 34.5 | 4.3 | 33.3 | 31.1 | 34.2 | 28.4 | 19.7 |
| LAD | 71.1 | 82.9 | 64.6 | 81.4 | 65.5 | 87.4 | 81.1 | 81 | 84.7 | 88.4 | 79.4 | 81 |
| CX | 55.6 | 30.3 | 54.7 | 56.1 | 40.1 | 51.1 | 24.6 | 40 | 56.9 | 50.5 | 42.5 | 28 |
| RCA | 62 | 37 | 64.2 | 66.4 | 57.2 | 62.2 | 41.9 | 82.7 | 64.9 | 55.2 | 52.5 | 29.9 |

### level: whole tree

#### units (segments in each)

| | |
|---|---|
| whole tree | lm, plad, mlad, dlad, d1, d2, im, pcx, om1, mcx, om2, dcx, prca, mrca, drca, pda, pla |

#### outcome summary (all units pooled)

| | n units | events | pct | regression events | regression pct | progression : regression | patients with event | ICC within patient | design effect | max predictors at 10 EPV |
|---|---|---|---|---|---|---|---|---|---|---|
| new plaque in a plaque-free segment | 1020 | 777 | 76.2 | 353 | 46.7 | 2.2 | 777 |  |  | 24 |
| plaque-free -> plaque | 264 | 124 | 47 | 36 | 4.8 | 3.44 | 124 |  |  | 12 |
| extent increase (+1 segment with plaque) | 1020 | 676 | 66.3 | 90 | 8.8 | 7.51 | 676 |  |  | 34 |
| burden increase (sum of stenosis grades) | 1020 | 707 | 69.3 | 107 | 10.5 | 6.61 | 707 |  |  | 31 |
| burden increase >= 2 | 1020 | 604 | 59.2 | 57 | 5.6 | 10.6 | 604 |  |  | 41 |
| max stenosis +1 grade | 1020 | 528 | 51.8 | 131 | 12.8 | 4.03 | 528 |  |  | 49 |
| incident obstructive | 881 | 282 | 32 | 26 | 18.7 | 10.8 | 282 |  |  | 28 |
| new high-risk feature | 515 | 142 | 27.6 | 518 | 82.1 | 0.27 | 142 |  |  | 14 |
| any plaque progression | 1020 | 807 | 79.1 | 398 | 39 | 2.03 | 807 |  |  | 21 |
| CAC increase | 2109 | 1274 | 60.4 | 49 | 2.3 | 26 | 1274 |  |  | 83 |
| CAC progression (Hokanson) | 2109 | 1053 | 49.9 | 10 | 0.5 | 105 | 1053 |  |  | 105 |
| incident CAC | 1261 | 478 | 37.9 | 20 | 2.4 | 23.9 | 478 |  |  | 47 |

#### agreement between outcomes (Cohen's kappa)

| | new plaque in a plaque-free segment | plaque-free -> plaque | extent increase (+1 segment with plaque) | burden increase (sum of stenosis grades) | burden increase >= 2 | max stenosis +1 grade | incident obstructive | new high-risk feature | any plaque progression | CAC increase | CAC progression (Hokanson) | incident CAC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new plaque in a plaque-free segment | 1 | 1 | 0.761 | 0.7 | 0.577 | 0.399 | 0.231 | 0.0528 | 0.915 | 0.716 | 0.556 | 0.798 |
| plaque-free -> plaque | 1 | 1 | 1 | 1 | 0.737 | 1 | 0.127 |  | 1 | 0.808 | 0.556 | 0.826 |
| extent increase (+1 segment with plaque) | 0.761 | 1 | 1 | 0.773 | 0.696 | 0.457 | 0.272 | 0.0898 | 0.683 | 0.532 | 0.46 | 0.717 |
| burden increase (sum of stenosis grades) | 0.7 | 1 | 0.773 | 1 | 0.783 | 0.597 | 0.342 | 0.049 | 0.747 | 0.584 | 0.513 | 0.723 |
| burden increase >= 2 | 0.577 | 0.737 | 0.696 | 0.783 | 1 | 0.566 | 0.462 | 0.0628 | 0.554 | 0.469 | 0.515 | 0.559 |
| max stenosis +1 grade | 0.399 | 1 | 0.457 | 0.597 | 0.566 | 1 | 0.561 | 0.0422 | 0.442 | 0.328 | 0.292 | 0.635 |
| incident obstructive | 0.231 | 0.127 | 0.272 | 0.342 | 0.462 | 0.561 | 1 | 0.0501 | 0.251 | 0.246 | 0.328 | 0.142 |
| new high-risk feature | 0.0528 |  | 0.0898 | 0.049 | 0.0628 | 0.0422 | 0.0501 | 1 | 0.0338 | 0.039 | 0.0509 | 0.166 |
| any plaque progression | 0.915 | 1 | 0.683 | 0.747 | 0.554 | 0.442 | 0.251 | 0.0338 | 1 | 0.779 | 0.593 | 0.816 |
| CAC increase | 0.716 | 0.808 | 0.532 | 0.584 | 0.469 | 0.328 | 0.246 | 0.039 | 0.779 | 1 | 0.79 | 1 |
| CAC progression (Hokanson) | 0.556 | 0.556 | 0.46 | 0.513 | 0.515 | 0.292 | 0.328 | 0.0509 | 0.593 | 0.79 | 1 | 0.771 |
| incident CAC | 0.798 | 0.826 | 0.717 | 0.723 | 0.559 | 0.635 | 0.142 | 0.166 | 0.816 | 1 | 0.771 | 1 |

#### event % by BL max stenosis grade (ceiling/floor)

| | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| new plaque in a plaque-free segment | 124/264 (47.0%) | 213/268 (79.5%) | 311/349 (89.1%) | 95/100 (95.0%) | hidden/28 | hidden/11 |
| plaque-free -> plaque | 124/264 (47.0%) | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| extent increase (+1 segment with plaque) | 124/264 (47.0%) | 180/268 (67.2%) | 267/349 (76.5%) | 81/100 (81.0%) | 18/28 (64.3%) | 6/11 (54.5%) |
| burden increase (sum of stenosis grades) | 124/264 (47.0%) | 208/268 (77.6%) | 270/349 (77.4%) | 82/100 (82.0%) | 18/28 (64.3%) | 5/11 (45.5%) |
| burden increase >= 2 | 90/264 (34.1%) | 175/268 (65.3%) | 243/349 (69.6%) | 74/100 (74.0%) | 17/28 (60.7%) | 5/11 (45.5%) |
| max stenosis +1 grade | 124/264 (47.0%) | 173/268 (64.6%) | 185/349 (53.0%) | 45/100 (45.0%) | <5/28 | 0/11 (0.0%) |
| incident obstructive | 15/264 (5.7%) | 82/268 (30.6%) | 185/349 (53.0%) | 0/0 | 0/0 | 0/0 |
| new high-risk feature | 0/0 | 29/137 (21.2%) | 77/265 (29.1%) | 25/78 (32.1%) | 8/26 (30.8%) | <5/9 |
| any plaque progression | 124/264 (47.0%) | 227/268 (84.7%) | 324/349 (92.8%) | hidden/100 | hidden/28 | hidden/11 |
| CAC increase | 105/264 (39.8%) | 232/268 (86.6%) | 331/349 (94.8%) | hidden/99 | hidden/28 | hidden/11 |
| CAC progression (Hokanson) | 73/264 (27.7%) | 192/268 (71.6%) | 296/349 (84.8%) | hidden/99 | hidden/28 | hidden/11 |
| incident CAC | 86/238 (36.1%) | 29/56 (51.8%) | 28/37 (75.7%) | <5/<5 | <5/<5 | <5/<5 |

#### event % by BL plaque

| | no plaque at BL | plaque at BL |
|---|---|---|
| new plaque in a plaque-free segment | 124/264 (47.0%) | 653/756 (86.4%) |
| plaque-free -> plaque | 124/264 (47.0%) | 0/0 |
| extent increase (+1 segment with plaque) | 124/264 (47.0%) | 552/756 (73.0%) |
| burden increase (sum of stenosis grades) | 124/264 (47.0%) | 583/756 (77.1%) |
| burden increase >= 2 | 90/264 (34.1%) | 514/756 (68.0%) |
| max stenosis +1 grade | 124/264 (47.0%) | 404/756 (53.4%) |
| incident obstructive | 15/264 (5.7%) | 267/617 (43.3%) |
| new high-risk feature | 0/0 | 142/515 (27.6%) |
| any plaque progression | 124/264 (47.0%) | 683/756 (90.3%) |
| CAC increase | 105/264 (39.8%) | 698/755 (92.5%) |
| CAC progression (Hokanson) | 73/264 (27.7%) | 619/755 (82.0%) |
| incident CAC | 86/238 (36.1%) | 63/101 (62.4%) |

#### event % by follow-up interval tertile (should rise with time)

| | 1 short | 2 middle | 3 long |
|---|---|---|---|
| new plaque in a plaque-free segment | 285/370 (77.0%) | 227/309 (73.5%) | 265/341 (77.7%) |
| plaque-free -> plaque | 44/91 (48.4%) | 25/60 (41.7%) | 55/113 (48.7%) |
| extent increase (+1 segment with plaque) | 244/370 (65.9%) | 189/309 (61.2%) | 243/341 (71.3%) |
| burden increase (sum of stenosis grades) | 263/370 (71.1%) | 198/309 (64.1%) | 246/341 (72.1%) |
| burden increase >= 2 | 215/370 (58.1%) | 174/309 (56.3%) | 215/341 (63.0%) |
| max stenosis +1 grade | 203/370 (54.9%) | 144/309 (46.6%) | 181/341 (53.1%) |
| incident obstructive | 100/323 (31.0%) | 78/258 (30.2%) | 104/300 (34.7%) |
| new high-risk feature | 53/190 (27.9%) | 54/184 (29.3%) | 35/141 (24.8%) |
| any plaque progression | 300/370 (81.1%) | 235/309 (76.1%) | 272/341 (79.8%) |
| CAC increase | 422/707 (59.7%) | 406/701 (57.9%) | 446/701 (63.6%) |
| CAC progression (Hokanson) | 325/707 (46.0%) | 325/701 (46.4%) | 403/701 (57.5%) |
| incident CAC | 134/394 (34.0%) | 151/429 (35.2%) | 193/438 (44.1%) |

#### AUC of single BL predictors (0.5 = no signal)

| | BL extent | BL burden | BL max stenosis | scan_age | male | ldl | hdl | clin_bp_sys_mean | hist_smoking_current | hist_diabetes | med_lipid_lowering_any | ct_cacs_sum | follow-up years |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new plaque in a plaque-free segment | 0.766 | 0.77 | 0.749 | 0.66 | 0.642 | 0.568 | 0.434 | 0.631 | 0.52 | 0.498 | 0.551 | 0.787 | 0.511 |
| plaque-free -> plaque | 0.5 | 0.5 | 0.5 | 0.634 | 0.542 | 0.602 | 0.446 | 0.57 | 0.527 | 0.493 | 0.522 | 0.558 | 0.542 |
| extent increase (+1 segment with plaque) | 0.621 | 0.632 | 0.635 | 0.604 | 0.626 | 0.551 | 0.437 | 0.604 | 0.52 | 0.498 | 0.533 | 0.687 | 0.533 |
| burden increase (sum of stenosis grades) | 0.664 | 0.655 | 0.629 | 0.63 | 0.624 | 0.579 | 0.444 | 0.594 | 0.517 | 0.499 | 0.527 | 0.72 | 0.514 |
| burden increase >= 2 | 0.675 | 0.67 | 0.643 | 0.635 | 0.643 | 0.583 | 0.438 | 0.618 | 0.507 | 0.503 | 0.532 | 0.737 | 0.533 |
| max stenosis +1 grade | 0.557 | 0.528 | 0.46 | 0.595 | 0.56 | 0.539 | 0.467 | 0.561 | 0.497 | 0.501 | 0.522 | 0.61 | 0.513 |
| incident obstructive | 0.784 | 0.793 | 0.743 | 0.65 | 0.629 | 0.549 | 0.441 | 0.625 | 0.505 | 0.506 | 0.527 | 0.812 | 0.532 |
| new high-risk feature | 0.608 | 0.597 | 0.55 | 0.528 | 0.556 | 0.485 | 0.46 | 0.516 | 0.518 | 0.488 | 0.501 | 0.528 | 0.492 |
| any plaque progression | 0.817 | 0.817 | 0.787 | 0.695 | 0.656 | 0.569 | 0.432 | 0.649 | 0.514 | 0.502 | 0.555 | 0.836 | 0.495 |
| CAC increase | 0.856 | 0.86 | 0.841 | 0.692 | 0.638 | 0.594 | 0.445 | 0.643 | 0.524 | 0.51 | 0.533 | 0.789 | 0.521 |
| CAC progression (Hokanson) | 0.82 | 0.823 | 0.796 | 0.678 | 0.64 | 0.586 | 0.441 | 0.644 | 0.521 | 0.51 | 0.53 | 0.782 | 0.555 |
| incident CAC | 0.616 | 0.622 | 0.622 | 0.604 | 0.593 | 0.61 | 0.448 | 0.608 | 0.535 | 0.504 | 0.507 | 0.5 | 0.551 |

#### continuous change (zero-inflation, skew)

| | n | mean | sd | p5 | p25 | median | p75 | p95 | pct zero | pct negative |
|---|---|---|---|---|---|---|---|---|---|---|
| change in extent | 1020 | 1.94 | 2.41 | -1 | 0 | 1 | 3 | 7 | 24.9 | 8.8 |
| change in burden | 1020 | 4.03 | 5.41 | -2 | 0 | 3 | 7 | 14 | 20.2 | 10.5 |
| change in max stenosis | 1020 | 0.637 | 1.13 | -1 | 0 | 1 | 1 | 2 | 35.4 | 12.8 |
| change in sqrt CAC | 2109 | 4.29 | 5.76 | 0 | 0 | 2.46 | 6.93 | 14.9 | 37.3 | 2.3 |

#### trajectory groups (pooled)

##### extent

| | n | pct |
|---|---|---|
| no plaque -> no plaque | 140 | 13.7 |
| no plaque -> plaque | 124 | 12.2 |
| plaque -> same | 114 | 11.2 |
| plaque -> more | 552 | 54.1 |
| plaque -> less | 90 | 8.8 |
| missing | 0 |  |

##### burden (presence from extent)

| | n | pct |
|---|---|---|
| no plaque -> no plaque | 140 | 13.7 |
| no plaque -> plaque | 124 | 12.2 |
| plaque -> same | 66 | 6.5 |
| plaque -> more | 583 | 57.2 |
| plaque -> less | 107 | 10.5 |
| missing | 0 |  |

### derived vs recorded scores (coding check)

| | n | Spearman rho | pct exactly equal |
|---|---|---|---|
| tree extent vs ct_cag_sis (BL) | 1020 | 0.988 | 95.1 |
| tree extent vs ct_cag_sis (FU) | 1020 | 0.993 | 91.8 |
| tree burden vs ct_cag_sss (BL) | 1020 | 0.989 | 95.1 |
| tree burden vs ct_cag_sss (FU) | 1020 | 0.995 | 91.8 |
| lad extent vs ct_cag_lad_sis (BL) | 1015 | 0.951 | 79.2 |
| lad extent vs ct_cag_lad_sis (FU) | 1015 | 0.955 | 63.7 |
| lad burden vs ct_cag_lad_sss (BL) | 1015 | 0.967 | 79.2 |
| lad burden vs ct_cag_lad_sss (FU) | 1015 | 0.98 | 63.7 |
| cx extent vs ct_cag_cx_sis (BL) | 1011 | 0.951 | 95.8 |
| cx extent vs ct_cag_cx_sis (FU) | 1011 | 0.962 | 89.6 |
| cx burden vs ct_cag_cx_sss (BL) | 1011 | 0.941 | 95.8 |
| cx burden vs ct_cag_cx_sss (FU) | 1011 | 0.955 | 89.6 |
| rca extent vs ct_cag_rca_sis (BL) | 1003 | 0.962 | 97.1 |
| rca extent vs ct_cag_rca_sis (FU) | 1003 | 0.981 | 96.5 |
| rca burden vs ct_cag_rca_sss (BL) | 1003 | 0.96 | 97.1 |
| rca burden vs ct_cag_rca_sss (FU) | 1003 | 0.983 | 96.5 |

## 8. Patient-level stenosis category

### worst stenosis category BL -> FU (highest flag set)

| | none | minimal | mild | moderate | severe | occlusion | missing |
|---|---|---|---|---|---|---|---|
| none | 134 | 71 | 36 | hidden | <5 | 0 | 0 |
| minimal | 27 | 66 | 93 | 53 | 28 | <5 | <5 |
| mild | hidden | 50 | 104 | 91 | 91 | <5 | 0 |
| moderate | <5 | <5 | 16 | 37 | 46 | 0 | <5 |
| severe | 0 | <5 | <5 | 14 | 10 | <5 | 0 |
| occlusion | <5 | 0 | <5 | <5 | hidden | 0 | 0 |
| missing | 542 | 255 | 175 | 74 | 40 | 0 | 8 |

### obstructive (moderate+) at BL

| | |
|---|---|
| n | 1022 |
| events | 145 |
| pct | 14.2 |

### obstructive at FU

| | |
|---|---|
| n | 2106 |
| events | 516 |
| pct | 24.5 |

### incident obstructive CAD

| | |
|---|---|
| n | 876 |
| events | 285 |
| pct | 32.5 |

### worst category worsened

| | |
|---|---|
| n | 1020 |
| events | 532 |
| pct | 52.2 |

## 9. Clinical events between the scans

### demo_hist_myocardial_infarction

| | |
|---|---|
| yes at BL, no at FU (data check) | 0 |

#### BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | 1022 | 6 |
| missing | 1079 | 9 |

#### incident (no at BL, yes at FU)

| | |
|---|---|
| n | 1028 |
| events | 6 |
| pct | 0.6 |

### demo_hist_coronary_revasc

| | |
|---|---|
| yes at BL, no at FU (data check) | 0 |

#### BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | 1022 | 6 |
| missing | 1078 | 10 |

#### incident (no at BL, yes at FU)

| | |
|---|---|
| n | 1028 |
| events | 6 |
| pct | 0.6 |

### demo_hist_stroke_tia

| | |
|---|---|
| yes at BL, no at FU (data check) | 119 |

#### BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | 860 | 31 |
| 1 | 119 | 19 |
| missing | 1035 | 52 |

#### incident (no at BL, yes at FU)

| | |
|---|---|
| n | 891 |
| events | 31 |
| pct | 3.5 |

### hist_angina

| | |
|---|---|
| yes at BL, no at FU (data check) | 0 |

#### BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | hidden |
| missing | hidden | <5 |

#### incident (no at BL, yes at FU)

| | |
|---|---|
| n | 2108 |
| events | 96 |
| pct | 4.6 |

### hist_diabetes

| | |
|---|---|
| yes at BL, no at FU (data check) | <5 |

#### BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | hidden |
| 1 | <5 | hidden |
| missing | hidden | 0 |

#### incident (no at BL, yes at FU)

| | |
|---|---|
| n | 2071 |
| events | 61 |
| pct | 2.9 |

### ct_cag_stent

| | |
|---|---|
| yes at BL, no at FU (data check) | <5 |

#### BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | hidden | <5 |
| 1 | <5 | <5 |
| missing | hidden | <5 |

#### incident (no at BL, yes at FU)

| | |
|---|---|
| n | 699 |
| events | <5 |
| pct | <5 |

### ct_cag_cabg

| | |
|---|---|
| yes at BL, no at FU (data check) | <5 |

#### BL -> FU

| | 0 | 1 |
|---|---|---|
| 0 | 1835 | 0 |
| 1 | <5 | <5 |
| missing | hidden | 0 |

#### incident (no at BL, yes at FU)

| | |
|---|---|
| n | 1835 |
| events | 0 |
| pct | 0 |

### incident hard composite (MI/revasc/stent/CABG)

| | |
|---|---|
| n | 1973 |
| events | 10 |
| pct | 0.5 |

### FU-only history (cannot separate new from pre-existing)

#### demo_hist_afib

| | |
|---|---|
| 0 | 2074 |
| 1 | 42 |

#### demo_hist_heart_failure

| | |
|---|---|
| 0 | 2107 |
| 1 | 9 |

#### demo_hist_icd_pm

| | |
|---|---|
| 0 | hidden |
| 1 | <5 |

#### demo_hist_pad

| | |
|---|---|
| 0 | 2104 |
| 1 | 12 |

#### demo_hist_dm

| | |
|---|---|
| 0 | 2022 |
| 1 | 94 |

#### demo_hist_cag

| | |
|---|---|
| 0 | 2035 |
| 1 | 81 |

#### demo_hist_rheumatoid_arthritis

| | |
|---|---|
| 0 | 2083 |
| 1 | 33 |

#### demo_hist_systemic_lupus_erythematosus

| | |
|---|---|
| 0 | hidden |
| 1 | <5 |

#### demo_hypertension_deriv

| | |
|---|---|
| 0 | 196 |
| 1 | 1920 |

#### demo_hypercholesterolemia_deriv

| | |
|---|---|
| 0 | 582 |
| 1 | 1534 |

#### demo_smoker_status

| | |
|---|---|
| (text values, not listed) | 2116 |

### adverse events (trial, FU)

#### ae_serious

| | |
|---|---|
| 0 | <5 |
| 1 | hidden |
| missing | 2102 |

#### ae_grade

| | |
|---|---|
| 1 | <5 |
| 2 | <5 |
| 3 | 6 |
| missing | 2106 |

#### ae_criteria

| | |
|---|---|
| 1 | <5 |
| 3 | hidden |
| missing | 2104 |

#### ae_intervention_related

| | |
|---|---|
| 3 | <5 |
| 4 | hidden |
| missing | 2106 |

#### ae_outcome_status

| | |
|---|---|
| 1 | 6 |
| 3 | <5 |
| 5 | <5 |
| missing | 2106 |

## 10. Medication BL -> FU

### med_lipid_lowering_any

| | 0 | 1 |
|---|---|---|
| 0 | 1371 | 510 |
| 1 | 17 | 168 |
| missing | 34 | 16 |

### med_antihypertensive_any

| | 0 | 1 |
|---|---|---|
| 0 | 1270 | 497 |
| 1 | 18 | 280 |
| missing | 35 | 16 |

### med_diuretic

| | 0 | 1 |
|---|---|---|
| 0 | 1837 | 168 |
| 1 | hidden | hidden |
| missing | hidden | <5 |

### med_asa

| | 0 | 1 |
|---|---|---|
| 0 | 1911 | 62 |
| 1 | hidden | hidden |
| missing | hidden | <5 |

### med_insulin

| | 0 | 1 |
|---|---|---|
| 0 | 2050 | 5 |
| 1 | <5 | hidden |
| missing | hidden | <5 |

### med_anticoagulant_any

| | 0 | 1 |
|---|---|---|
| 0 | 968 | 45 |
| 1 | 12 | 13 |
| missing | 1016 | 62 |

### med_diabetes_other

| | 0 | 1 |
|---|---|---|
| 0 | 1862 | 180 |
| 1 | <5 | hidden |
| missing | hidden | <5 |

### med_arthritis

| | 0 | 1 |
|---|---|---|
| 0 | hidden | hidden |
| 1 | hidden | <5 |
| missing | hidden | 0 |

### FU only

#### med_statin

| | |
|---|---|
| 0 | 1439 |
| 1 | 677 |

#### med_statin_duration_above_2_years

| | |
|---|---|
| 0 | 1594 |
| 1 | 522 |

#### preparation_betablocker

| | |
|---|---|
| 0 | 1368 |
| 50 | 22 |
| 75 | 20 |
| 100 | 697 |
| missing | 9 |

#### med_platelet_agg_inhibitors

| | |
|---|---|
| 0 | 2040 |
| 1 | hidden |
| missing | <5 |

#### med_doac_noac

| | |
|---|---|
| 0 | 2008 |
| 1 | 108 |

#### med_warfarin

| | |
|---|---|
| 0 | 2107 |
| 1 | 9 |

#### med_metformin

| | |
|---|---|
| 0 | 2037 |
| 1 | 79 |

## 11. Outcomes by randomisation group, lipid-lowering change and sex

### rand_group (FU)

#### group sizes

| | |
|---|---|
| 0 | 725 |
| 1 | 745 |
| 2 | 646 |

#### follow-up years

| | n | mean | sd | p5 | p25 | median | p75 | p95 |
|---|---|---|---|---|---|---|---|---|
| 0 | 725 | 10.9 | 1.8 | 9.53 | 9.67 | 10.1 | 12 | 15.2 |
| 1 | 745 | 10.9 | 1.8 | 9.52 | 9.65 | 10 | 12 | 15.3 |
| 2 | 646 | 11.1 | 1.93 | 9.51 | 9.65 | 9.99 | 12.5 | 15.3 |

#### BL predictor mean

| | 0 | 1 | 2 |
|---|---|---|---|
| male | 0.423 | 0.458 | 0.491 |
| scan_age | 54.9 | 54.6 | 58.5 |
| clin_bmi | 25.5 | 25.5 | 26.8 |
| clin_bp_sys_mean | 132 | 134 | 138 |
| clin_bp_dia_mean | 79.7 | 81.1 | 82.4 |
| hr_during_scan | 53.2 | 53.2 | 53.2 |
| creatinine | 77.5 | 77.5 | 78.6 |
| egfr | 89 | 89.7 | 87.1 |
| hba1c | 35 | 35.1 | 37.1 |
| tot_cholesterol | 5.28 | 5.22 | 5.53 |
| hdl | 1.54 | 1.48 | 1.44 |
| ldl | 3.1 | 3.06 | 3.3 |
| triglyceride | 1.48 | 1.57 | 1.87 |
| hist_smoking_current | 0.0952 | 0.0966 | 0.11 |
| hist_smoking_former | 0.388 | 0.421 | 0.48 |
| hist_smoking_years | 22 | 21.6 | 24 |
| hist_diabetes | 0.0055 | 0.0054 | 0.0497 |
| demo_hist_family_cvd | 0.301 | 0.284 | 0.35 |
| demo_hist_family_hypercholesterolemia | 0.481 | 0.497 | 0.52 |
| med_lipid_lowering_any | 0.0156 | 0.015 | 0.26 |
| med_antihypertensive_any | 0.0979 | 0.0955 | 0.254 |
| ct_cacs_sum | 45.2 | 46 | 121 |
| ct_cag_sis | 0.983 | 1.02 | 1.71 |
| ct_cag_sss | 1.5 | 1.6 | 2.79 |
| ct_cag_plaque_type_score | 2.05 | 2.14 | 3.37 |

#### % missing at BL (were variables collected in every group?)

| | 0 | 1 | 2 |
|---|---|---|---|
| male | 0 | 0 | 0 |
| scan_age | 0 | 0 | 0 |
| clin_bmi | 50.8 | 50.5 | 52.8 |
| clin_bp_sys_mean | 1.4 | 1.3 | 0.9 |
| clin_bp_dia_mean | 1.7 | 1.5 | 1.4 |
| hr_during_scan | 89.5 | 89.5 | 87.5 |
| creatinine | 1.5 | 1.5 | 2.6 |
| egfr | 1.5 | 1.5 | 2.6 |
| hba1c | 54.2 | 53.2 | 52 |
| tot_cholesterol | 1.5 | 1.5 | 2.5 |
| hdl | 1.5 | 1.5 | 2.5 |
| ldl | 1.4 | 1.3 | 2 |
| triglyceride | 1.5 | 1.5 | 2.5 |
| hist_smoking_current | 0 | 0 | 0 |
| hist_smoking_former | 0 | 0 | 0 |
| hist_smoking_years | 52.1 | 48.5 | 41.8 |
| hist_diabetes | <5 | <5 | <5 |
| demo_hist_family_cvd | <5 | <5 | 1.1 |
| demo_hist_family_hypercholesterolemia | <5 | <5 | 0.9 |
| med_lipid_lowering_any | 2.8 | 1.6 | 2.8 |
| med_antihypertensive_any | 2.8 | 1.6 | 2.9 |
| ct_cacs_sum | <5 | <5 | <5 |
| ct_cag_sis | 0 | 0 | 0 |
| ct_cag_sss | 0 | 0 | 0 |
| ct_cag_plaque_type_score | 0 | 0 | 0 |
| demo_hist_myocardial_infarction | 50.8 | 50.6 | 53.1 |
| demo_hist_coronary_revasc | 50.8 | 50.6 | 53.1 |
| demo_hist_stroke_tia | 50.8 | 50.5 | 53.1 |
| hist_angina | <5 | <5 | <5 |
| ct_cag_stent | 66.2 | 66.7 | 67.6 |
| ct_cag_cabg | 11.7 | 12.1 | 16.1 |
| ct_cag_none | 0 | 0 | 0 |
| ct_cag_minimal | 0 | 0 | 0 |
| ct_cag_mild | 0 | 0 | 0 |
| ct_cag_moderate | 0 | 0 | 0 |
| ct_cag_severe | 0 | 0 | 0 |
| ct_cag_occlusion | 0 | 0 | 0 |

#### binary outcomes (% events)

| | 0 | 1 | 2 |
|---|---|---|---|
| incident_cac (BL=0 -> FU>0) | 34.5 | 33.9 | 50.3 |
| cac_any_increase | 55 | 53.2 | 74.8 |
| cac_progression_hokanson (dsqrt >= 2.5) | 44 | 42.6 | 65 |
| cac_annual_change_ge_15pct (BL>0) | 43 | 30.5 | 34.9 |
| cac_decrease (data check) | 1.7 | 2.6 | 2.8 |
| sss_increase | 53.2 | 54.5 | 71.5 |
| sss_increase_ge2 | 41.2 | 44.2 | 61 |
| sis_increase | 52 | 52.2 | 70.3 |
| plaque_type_score_change | 59.6 | 59.1 | 76.9 |
| any segment stenosis progression | 75.2 | 73.3 | 89.2 |
| any new plaque | 71.5 | 70.7 | 85.8 |
| any new high-risk feature | 19.5 | 21.2 | 18.8 |
| no plaque -> plaque (SIS, among 'no plaque ->') | 44.9 | 43.4 | 64 |
| plaque -> more (SIS, among 'plaque ->') | 67.1 | 70.2 | 78.1 |
| plaque -> less (SIS, among 'plaque ->') | 17.7 | 14.7 | 10.4 |
| incident_obstructive_cad | 27.3 | 28.4 | 41.9 |
| worst_category_worsened | 48.5 | 47.8 | 59.8 |
| incident demo_hist_myocardial_infarction | 0 | 0 | 2 |
| incident demo_hist_coronary_revasc | 0 | 0 | 2 |
| incident demo_hist_stroke_tia | 0 | 0 | 12.1 |
| incident hist_angina | 4.7 | 3.5 | 5.6 |
| incident hist_diabetes | 1.3 | 2.2 | 5.9 |
| incident ct_cag_stent | 0 | 0 | <5 |
| incident ct_cag_cabg | 0 | 0 | 0 |
| incident hard composite (MI/revasc/stent/CABG) | 0 | 0 | 1.7 |

#### continuous outcomes (median)

| | 0 | 1 | 2 |
|---|---|---|---|
| delta_sss | 1 | 1 | 3 |
| delta_sis | 1 | 1 | 2 |
| delta_sss_per_year | 0.086 | 0.0996 | 0.248 |
| delta_sqrt_cac | 1.73 | 1 | 4.87 |
| delta_cac_per_year | 0.34 | 0.156 | 4.97 |
| n_segments_new_plaque | 2 | 2 | 3 |

### lipid-lowering BL -> FU

#### group sizes

| | |
|---|---|
| continued | 168 |
| never | 1371 |
| started | 510 |
| stopped | 17 |
| missing | 50 |

#### follow-up years

| | n | mean | sd | p5 | p25 | median | p75 | p95 |
|---|---|---|---|---|---|---|---|---|
| continued | 168 | 10.9 | 1.81 | 9.51 | 9.61 | 9.91 | 12.1 | 15.2 |
| never | 1371 | 10.9 | 1.78 | 9.52 | 9.65 | 10 | 11.9 | 15.2 |
| started | 510 | 11.3 | 2.01 | 9.52 | 9.66 | 10.1 | 12.9 | 15.3 |
| stopped | 17 | 11.3 | 1.89 |  | 9.74 | 10.2 | 13 |  |
| missing | 50 | 9.89 | 0.638 | 9.64 | 9.69 | 9.72 | 9.85 | 10.1 |

#### BL predictor mean

| | continued | never | started | stopped | missing |
|---|---|---|---|---|---|
| male | 0.536 | 0.438 | 0.48 | 0.294 | 0.48 |
| scan_age | 61.8 | 54.6 | 57.1 | 61.6 | 57.2 |
| clin_bmi | 28.5 | 25.6 | 26.1 | 24.5 |  |
| clin_bp_sys_mean | 140 | 132 | 138 | 138 | 132 |
| clin_bp_dia_mean | 82.1 | 80.1 | 83.2 | 81.7 | 79.7 |
| hr_during_scan | 54.3 | 53.5 | 52.5 |  |  |
| creatinine | 77.1 | 77.2 | 79.7 | 74.3 | 78.7 |
| egfr | 88 | 89.7 | 86.4 | 85.7 | 87.2 |
| hba1c | 38 | 35 | 36.7 | 35.7 | 35.3 |
| tot_cholesterol | 4.73 | 5.19 | 5.97 | 4.44 | 5.02 |
| hdl | 1.5 | 1.51 | 1.44 | 1.7 | 1.26 |
| ldl | 2.48 | 3.03 | 3.73 | 2.17 | 3.09 |
| triglyceride | 1.87 | 1.51 | 1.91 | 1.27 | 1.48 |
| hist_smoking_current | 0.0893 | 0.0926 | 0.123 | 0.235 | 0.06 |
| hist_smoking_former | 0.446 | 0.399 | 0.508 | 0.235 | 0.4 |
| hist_smoking_years | 24.2 | 21.4 | 24.2 | 26.6 | 24 |
| hist_diabetes | 0.113 | 0.0022 | 0.0276 | 0.176 | 0.02 |
| demo_hist_family_cvd | 0.443 | 0.276 | 0.36 | 0.312 | 0.32 |
| demo_hist_family_hypercholesterolemia | 0.569 | 0.485 | 0.509 | 0.375 | 0.56 |
| med_lipid_lowering_any | 1 | 0 | 0 | 1 |  |
| med_antihypertensive_any | 0.473 | 0.0897 | 0.18 | 0.188 |  |
| ct_cacs_sum | 248 | 39.4 | 81 | 46.1 | 157 |
| ct_cag_sis | 2.46 | 0.945 | 1.5 | 1.06 | 1.7 |
| ct_cag_sss | 3.93 | 1.43 | 2.56 | 1.65 | 2.6 |
| ct_cag_plaque_type_score | 4.81 | 1.99 | 2.96 | 1.88 | 3.54 |

#### % missing at BL (were variables collected in every group?)

| | continued | never | started | stopped | missing |
|---|---|---|---|---|---|
| male | 0 | 0 | 0 | 0 | 0 |
| scan_age | 0 | 0 | 0 | 0 | 0 |
| clin_bmi | 57.1 | 51.4 | 45.5 | 35.3 | hidden |
| clin_bp_sys_mean | <5 | 1.3 | 1 | 0 | <5 |
| clin_bp_dia_mean | <5 | 1.7 | 1 | 0 | <5 |
| hr_during_scan | 89.3 | 89.8 | 85.5 | hidden | 100 |
| creatinine | 3 | 1.5 | 2 | 0 | <5 |
| egfr | 3 | 1.5 | 2 | 0 | <5 |
| hba1c | 48.2 | 53.3 | 57.6 | 64.7 | 16 |
| tot_cholesterol | 3 | 1.5 | 1.8 | 0 | <5 |
| hdl | 3 | 1.5 | 1.8 | 0 | <5 |
| ldl | 3 | 1.4 | 1.2 | 0 | <5 |
| triglyceride | 3 | 1.5 | 1.8 | 0 | <5 |
| hist_smoking_current | 0 | 0 | 0 | 0 | 0 |
| hist_smoking_former | 0 | 0 | 0 | 0 | 0 |
| hist_smoking_years | 47.6 | 51.1 | 37.5 | 52.9 | 56 |
| hist_diabetes | 0 | <5 | <5 | 0 | 0 |
| demo_hist_family_cvd | <5 | 0.4 | <5 | <5 | 0 |
| demo_hist_family_hypercholesterolemia | <5 | <5 | <5 | <5 | 0 |
| med_lipid_lowering_any | 0 | 0 | 0 | 0 | 100 |
| med_antihypertensive_any | <5 | 0 | 0 | <5 | hidden |
| ct_cacs_sum | <5 | <5 | <5 | <5 | 0 |
| ct_cag_sis | 0 | 0 | 0 | 0 | 0 |
| ct_cag_sss | 0 | 0 | 0 | 0 | 0 |
| ct_cag_plaque_type_score | 0 | 0 | 0 | 0 | 0 |
| demo_hist_myocardial_infarction | 57.1 | 51.5 | 45.9 | 35.3 | hidden |
| demo_hist_coronary_revasc | 57.1 | 51.5 | 45.9 | 35.3 | hidden |
| demo_hist_stroke_tia | 57.1 | 51.4 | 45.9 | 35.3 | hidden |
| hist_angina | 0 | 0.4 | <5 | 0 | 0 |
| ct_cag_stent | 67.9 | 67.5 | 69.6 | 70.6 | 16 |
| ct_cag_cabg | 18.5 | 13 | 12.7 | <5 | <5 |
| ct_cag_none | 0 | 0 | 0 | 0 | 0 |
| ct_cag_minimal | 0 | 0 | 0 | 0 | 0 |
| ct_cag_mild | 0 | 0 | 0 | 0 | 0 |
| ct_cag_moderate | 0 | 0 | 0 | 0 | 0 |
| ct_cag_severe | 0 | 0 | 0 | 0 | 0 |
| ct_cag_occlusion | 0 | 0 | 0 | 0 | 0 |

#### binary outcomes (% events)

| | continued | missing | never | started | stopped |
|---|---|---|---|---|---|
| incident_cac (BL=0 -> FU>0) | 51 | 28 | 33.3 | 53.3 | <5 |
| cac_any_increase | 81.4 | 56 | 53.3 | 73.6 | 43.8 |
| cac_progression_hokanson (dsqrt >= 2.5) | 70.1 | 46 | 42.9 | 63.2 | 31.2 |
| cac_annual_change_ge_15pct (BL>0) | 26.7 | 32 | 37.1 | 38.5 | <5 |
| cac_decrease (data check) | 3.6 | <5 | 2 | 2.2 | 0 |
| sss_increase | 77.4 | 54 | 53.2 | 70.6 | 47.1 |
| sss_increase_ge2 | 68.5 | 38 | 41.9 | 60.2 | 35.3 |
| sis_increase | 75.6 | 50 | 51.7 | 68.8 | 47.1 |
| plaque_type_score_change | 83.3 | 62 | 58.6 | 75.9 | 47.1 |
| any segment stenosis progression | hidden | 75.8 | 73.9 | 85.6 | <5 |
| any new plaque | 93.1 | 72.7 | 70.5 | 82.7 | <5 |
| any new high-risk feature | 20.4 | <5 | 21.6 | 16.9 | <5 |
| no plaque -> plaque (SIS, among 'no plaque ->') | 70.7 | 30.4 | 43.7 | 64.5 | <5 |
| plaque -> more (SIS, among 'plaque ->') | 79.6 | 66.7 | 69.5 | 74.8 | <5 |
| plaque -> less (SIS, among 'plaque ->') | 7.5 | <5 | 16 | 13.1 | hidden |
| incident_obstructive_cad | 43.8 | 34.5 | 27.5 | 40.3 | <5 |
| worst_category_worsened | 61.8 | 45.5 | 48.7 | 56.8 | <5 |
| incident demo_hist_myocardial_infarction | 0 | hidden | 0 | 2.2 | 0 |
| incident demo_hist_coronary_revasc | 0 | hidden | 0 | 2.2 | 0 |
| incident demo_hist_stroke_tia | 0 | hidden | 0.9 | 10.9 | 0 |
| incident hist_angina | 4.2 | <5 | 4 | 6.3 | <5 |
| incident hist_diabetes | 7.4 | <5 | 1.4 | 6.1 | 0 |
| incident ct_cag_stent | 0 | 0 | 0 | <5 | 0 |
| incident ct_cag_cabg | 0 | 0 | 0 | 0 | 0 |
| incident hard composite (MI/revasc/stent/CABG) | 0 | 0 | 0 | 2.1 | 0 |

#### continuous outcomes (median)

| | continued | missing | never | started | stopped |
|---|---|---|---|---|---|
| delta_sss | 4 | 1 | 1 | 2 | 0 |
| delta_sis | 2.5 | 0.5 | 1 | 2 | 0 |
| delta_sss_per_year | 0.4 | 0.102 | 0.0871 | 0.209 | 0 |
| delta_sqrt_cac | 6.6 | 1.87 | 1 | 4.47 | 0 |
| delta_cac_per_year | 11.3 | 0.362 | 0.207 | 3.55 | 0 |
| n_segments_new_plaque | 3 | 2 | 2 | 3 | <5 |

### male (BL)

#### group sizes

| | |
|---|---|
| 0 | 1151 |
| 1 | 965 |

#### follow-up years

| | n | mean | sd | p5 | p25 | median | p75 | p95 |
|---|---|---|---|---|---|---|---|---|
| 0 | 1151 | 11 | 1.83 | 9.51 | 9.65 | 10 | 12.1 | 15.3 |
| 1 | 965 | 11 | 1.85 | 9.53 | 9.65 | 10 | 12.3 | 15.2 |

#### BL predictor mean

| | 0 | 1 |
|---|---|---|
| male | 0 | 1 |
| scan_age | 55.7 | 56.2 |
| clin_bmi | 25.3 | 26.6 |
| clin_bp_sys_mean | 131 | 138 |
| clin_bp_dia_mean | 79.2 | 83.1 |
| hr_during_scan | 53.3 | 53 |
| creatinine | 72.8 | 83.9 |
| egfr | 84.9 | 93.2 |
| hba1c | 35.4 | 36.1 |
| tot_cholesterol | 5.35 | 5.31 |
| hdl | 1.65 | 1.29 |
| ldl | 3.09 | 3.22 |
| triglyceride | 1.39 | 1.92 |
| hist_smoking_current | 0.108 | 0.0912 |
| hist_smoking_former | 0.434 | 0.42 |
| hist_smoking_years | 21.7 | 23.5 |
| hist_diabetes | 0.0148 | 0.0239 |
| demo_hist_family_cvd | 0.348 | 0.265 |
| demo_hist_family_hypercholesterolemia | 0.555 | 0.431 |
| med_lipid_lowering_any | 0.08 | 0.101 |
| med_antihypertensive_any | 0.144 | 0.145 |
| ct_cacs_sum | 30.8 | 114 |
| ct_cag_sis | 0.718 | 1.82 |
| ct_cag_sss | 1.08 | 2.94 |
| ct_cag_plaque_type_score | 1.48 | 3.68 |

#### % missing at BL (were variables collected in every group?)

| | 0 | 1 |
|---|---|---|
| male | 0 | 0 |
| scan_age | 0 | 0 |
| clin_bmi | 52.9 | 49.3 |
| clin_bp_sys_mean | 1.7 | 0.7 |
| clin_bp_dia_mean | 1.9 | 1 |
| hr_during_scan | 89.1 | 88.7 |
| creatinine | 1.9 | 1.8 |
| egfr | 1.9 | 1.8 |
| hba1c | 52 | 54.6 |
| tot_cholesterol | 1.8 | 1.8 |
| hdl | 1.8 | 1.8 |
| ldl | 1.6 | 1.6 |
| triglyceride | 1.8 | 1.8 |
| hist_smoking_current | 0 | 0 |
| hist_smoking_former | 0 | 0 |
| hist_smoking_years | 46.2 | 49.4 |
| hist_diabetes | <5 | <5 |
| demo_hist_family_cvd | 0.5 | 0.6 |
| demo_hist_family_hypercholesterolemia | <5 | <5 |
| med_lipid_lowering_any | 2.3 | 2.5 |
| med_antihypertensive_any | 2.3 | 2.6 |
| ct_cacs_sum | 0.5 | <5 |
| ct_cag_sis | 0 | 0 |
| ct_cag_sss | 0 | 0 |
| ct_cag_plaque_type_score | 0 | 0 |
| demo_hist_myocardial_infarction | 53.1 | 49.4 |
| demo_hist_coronary_revasc | 53.1 | 49.4 |
| demo_hist_stroke_tia | 53 | 49.4 |
| hist_angina | <5 | <5 |
| ct_cag_stent | 67.1 | 66.5 |
| ct_cag_cabg | 15.9 | 9.9 |
| ct_cag_none | 0 | 0 |
| ct_cag_minimal | 0 | 0 |
| ct_cag_mild | 0 | 0 |
| ct_cag_moderate | 0 | 0 |
| ct_cag_severe | 0 | 0 |
| ct_cag_occlusion | 0 | 0 |

#### binary outcomes (% events)

| | 0 | 1 |
|---|---|---|
| incident_cac (BL=0 -> FU>0) | 31.2 | 50.3 |
| cac_any_increase | 48.2 | 74.9 |
| cac_progression_hokanson (dsqrt >= 2.5) | 37 | 65.2 |
| cac_annual_change_ge_15pct (BL>0) | 37.9 | 34.7 |
| cac_decrease (data check) | 2.4 | 2.2 |
| sss_increase | 47.6 | 73.2 |
| sss_increase_ge2 | 35.4 | 63.7 |
| sis_increase | 46 | 71.5 |
| plaque_type_score_change | 53.9 | 77.6 |
| any segment stenosis progression | 68.1 | 89 |
| any new plaque | 64.9 | 85.7 |
| any new high-risk feature | 14.6 | 23 |
| no plaque -> plaque (SIS, among 'no plaque ->') | 41.5 | 63 |
| plaque -> more (SIS, among 'plaque ->') | 59.2 | 80.4 |
| plaque -> less (SIS, among 'plaque ->') | 22.1 | 8.9 |
| incident_obstructive_cad | 20.9 | 43.7 |
| worst_category_worsened | 45.6 | 57.7 |
| incident demo_hist_myocardial_infarction | <5 | 1 |
| incident demo_hist_coronary_revasc | <5 | 1 |
| incident demo_hist_stroke_tia | 2.1 | 5 |
| incident hist_angina | 5.7 | 3.2 |
| incident hist_diabetes | 2.1 | 3.9 |
| incident ct_cag_stent | <5 | 0 |
| incident ct_cag_cabg | 0 | 0 |
| incident hard composite (MI/revasc/stent/CABG) | <5 | 0.8 |

#### continuous outcomes (median)

| | 0 | 1 |
|---|---|---|
| delta_sss | 0 | 3 |
| delta_sis | 0 | 2 |
| delta_sss_per_year | 0 | 0.298 |
| delta_sqrt_cac | 0 | 4.79 |
| delta_cac_per_year | 0 | 4.53 |
| n_segments_new_plaque | 1 | 3 |

## 12. Baseline predictor vs outcome associations

### Spearman rho, BL predictor vs continuous outcome

| | male | scan_age | clin_bmi | clin_bp_sys_mean | clin_bp_dia_mean | hr_during_scan | creatinine | egfr | hba1c | tot_cholesterol | hdl | ldl | triglyceride | hist_smoking_current | hist_smoking_former | hist_smoking_years | hist_diabetes | demo_hist_family_cvd | demo_hist_family_hypercholesterolemia | med_lipid_lowering_any | med_antihypertensive_any | ct_cacs_sum | ct_cag_sis | ct_cag_sss | ct_cag_plaque_type_score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| delta_sss | 0.304 | 0.274 | 0.197 | 0.251 | 0.19 | -0.0945 | 0.136 | 0.0393 | 0.231 | 0.111 | -0.165 | 0.137 | 0.21 | 0.0549 | 0.0564 | 0.187 | 0.0886 | 0.049 | -0.052 | 0.13 | 0.161 | 0.491 | 0.278 | 0.274 | 0.261 |
| delta_sis | 0.298 | 0.234 | 0.221 | 0.241 | 0.197 | -0.085 | 0.143 | 0.0436 | 0.211 | 0.118 | -0.17 | 0.144 | 0.214 | 0.0655 | 0.0458 | 0.169 | 0.0781 | 0.0573 | -0.0545 | 0.119 | 0.152 | 0.411 | 0.169 | 0.176 | 0.154 |
| delta_sss_per_year | 0.305 | 0.28 | 0.2 | 0.25 | 0.19 | -0.0899 | 0.141 | 0.0332 | 0.234 | 0.0992 | -0.173 | 0.127 | 0.212 | 0.0527 | 0.0562 | 0.193 | 0.0897 | 0.0458 | -0.0431 | 0.131 | 0.165 | 0.496 | 0.285 | 0.28 | 0.268 |
| delta_sqrt_cac | 0.294 | 0.335 | 0.184 | 0.281 | 0.234 | -0.0873 | 0.15 | -0.008 | 0.232 | 0.133 | -0.106 | 0.14 | 0.159 | 0.0783 | 0.0796 | 0.2 | 0.105 | 0.0609 | -0.0495 | 0.139 | 0.165 | 0.597 | 0.545 | 0.547 | 0.535 |
| delta_cac_per_year | 0.311 | 0.387 | 0.188 | 0.29 | 0.233 | -0.0867 | 0.168 | -0.0324 | 0.246 | 0.124 | -0.111 | 0.13 | 0.162 | 0.0679 | 0.09 | 0.222 | 0.103 | 0.0514 | -0.0462 | 0.164 | 0.186 | 0.732 | 0.649 | 0.651 | 0.636 |
| n_segments_new_plaque | 0.333 | 0.238 | 0.218 | 0.251 | 0.192 | -0.0547 | 0.159 | 0.0591 | 0.148 | 0.1 | -0.146 | 0.119 | 0.2 | 0.0417 | 0.0565 | 0.144 | -0.0177 | 0.0654 | -0.112 | 0.132 | 0.149 | 0.452 | 0.359 | 0.372 | 0.315 |

### standardised mean difference of BL predictor, events vs non-events

| | male | scan_age | clin_bmi | clin_bp_sys_mean | clin_bp_dia_mean | hr_during_scan | creatinine | egfr | hba1c | tot_cholesterol | hdl | ldl | triglyceride | hist_smoking_current | hist_smoking_former | hist_smoking_years | hist_diabetes | demo_hist_family_cvd | demo_hist_family_hypercholesterolemia | med_lipid_lowering_any | med_antihypertensive_any | ct_cacs_sum | ct_cag_sis | ct_cag_sss | ct_cag_plaque_type_score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| incident_cac (BL=0 -> FU>0) | 0.391 | 0.343 | 0.218 | 0.38 | 0.316 | -0.161 | 0.169 | 0.0466 | 0.266 | 0.362 | -0.159 | 0.363 | 0.278 | 0.228 | 0.0999 | 0.389 | 0.081 | 0.126 | 0.0133 | 0.0676 | 0.155 |  | 0.278 | 0.24 | 0.26 |
| cac_any_increase | 0.583 | 0.688 | 0.256 | 0.512 | 0.404 | -0.242 | 0.293 | -0.0475 | 0.42 | 0.308 | -0.181 | 0.315 | 0.295 | 0.164 | 0.188 | 0.464 | 0.16 | 0.109 | -0.0596 | 0.241 | 0.296 | 0.453 | 0.998 | 0.877 | 0.96 |
| cac_progression_hokanson (dsqrt >= 2.5) | 0.586 | 0.637 | 0.261 | 0.506 | 0.419 | -0.199 | 0.288 | -0.0361 | 0.398 | 0.261 | -0.201 | 0.276 | 0.282 | 0.141 | 0.127 | 0.353 | 0.158 | 0.111 | -0.127 | 0.209 | 0.245 | 0.475 | 0.977 | 0.87 | 0.943 |
| cac_annual_change_ge_15pct (BL>0) | -0.067 | -0.384 | -0.0348 | 0.0061 | 0.151 | 0.101 | -0.0649 | 0.181 | 0.0288 | -0.0249 | 0.0363 | -0.0326 | -0.0258 | 0.0269 | -0.0768 | -0.0286 | 0.0787 | 0.0749 | -0.0265 | -0.163 | -0.0796 | -0.707 | -0.607 | -0.638 | -0.486 |
| cac_decrease (data check) | -0.0585 | 0.137 | 0.197 | 0.157 | -0.253 |  | -0.363 | 0.203 | -0.331 | -0.0293 | -0.171 | -0.0306 | 0.123 | 0.0083 | 0.21 | 0.0444 | -0.194 | 0.0824 | 0.107 | 0.144 | 0.0941 | 0.23 | -0.118 | -0.158 | -0.118 |
| sss_increase | 0.549 | 0.536 | 0.292 | 0.445 | 0.356 | -0.224 | 0.228 | 0.0423 | 0.389 | 0.245 | -0.263 | 0.281 | 0.293 | 0.149 | 0.118 | 0.395 | 0.125 | 0.0952 | -0.0637 | 0.204 | 0.26 | 0.256 | 0.432 | 0.338 | 0.388 |
| sss_increase_ge2 | 0.589 | 0.517 | 0.364 | 0.488 | 0.352 | -0.146 | 0.243 | 0.06 | 0.436 | 0.251 | -0.284 | 0.279 | 0.339 | 0.0542 | 0.0799 | 0.338 | 0.148 | 0.0809 | -0.0876 | 0.212 | 0.263 | 0.332 | 0.493 | 0.407 | 0.445 |
| sis_increase | 0.54 | 0.473 | 0.329 | 0.446 | 0.374 | -0.172 | 0.249 | 0.0378 | 0.309 | 0.229 | -0.261 | 0.265 | 0.281 | 0.143 | 0.107 | 0.33 | 0.102 | 0.113 | -0.0749 | 0.2 | 0.224 | 0.184 | 0.285 | 0.242 | 0.243 |
| plaque_type_score_change | 0.542 | 0.619 | 0.292 | 0.48 | 0.395 | -0.228 | 0.278 | -0.0403 | 0.332 | 0.239 | -0.236 | 0.265 | 0.296 | 0.148 | 0.137 | 0.45 | 0.0985 | 0.0946 | -0.0251 | 0.221 | 0.273 | 0.428 | 0.791 | 0.67 | 0.79 |
| any segment stenosis progression | 0.671 | 0.717 | 0.35 | 0.56 | 0.4 | -0.0849 | 0.209 | 0.0734 | 0.367 | 0.248 | -0.252 | 0.258 | 0.372 | 0.0866 | 0.251 | 0.377 | 0.034 | 0.157 | -0.19 | 0.428 | 0.301 | 0.415 | 1.22 | 1.02 | 1.09 |
| any new plaque | 0.595 | 0.56 | 0.334 | 0.468 | 0.346 | -0.0537 | 0.205 | 0.0719 | 0.129 | 0.231 | -0.224 | 0.242 | 0.306 | 0.129 | 0.159 | 0.399 | -0.0277 | 0.157 | -0.171 | 0.379 | 0.27 | 0.312 | 0.86 | 0.716 | 0.789 |
| any new high-risk feature | 0.265 | 0.132 | 0.168 | 0.122 | 0.0617 | -0.0156 | 0.141 | 0.0411 | 0.11 | -0.0877 | -0.172 | -0.0334 | 0.0883 | 0.0305 | -0.0003 | -0.0129 | -0.217 | -0.112 | -0.267 | 0.0123 | -0.129 | 0.197 | 0.577 | 0.505 | 0.691 |
| no plaque -> plaque (SIS, among 'no plaque ->') | 0.423 | 0.477 | 0.322 | 0.435 | 0.373 | -0.133 | 0.195 | -0.0052 | 0.376 | 0.266 | -0.276 | 0.297 | 0.333 | 0.155 | 0.0857 | 0.418 | 0.154 | 0.119 | 0.0198 | 0.16 | 0.261 | 0.229 |  |  |  |
| plaque -> more (SIS, among 'plaque ->') | 0.521 | 0.132 | 0.29 | 0.278 | 0.239 | 0.114 | 0.205 | 0.206 | 0.0903 | 0.0706 | -0.204 | 0.118 | 0.129 | 0.0978 | 0.0268 | 0.0773 | -0.0055 | 0.0811 | -0.252 | 0.162 | 0.0576 | -0.104 | -0.169 | -0.147 | -0.283 |
| plaque -> less (SIS, among 'plaque ->') | -0.535 | -0.0864 | -0.336 | -0.272 | -0.297 |  | -0.188 | -0.232 | -0.322 | -0.131 | 0.14 | -0.172 | -0.101 | -0.105 | -0.033 | 0.0394 | -0.0879 | 0.0031 | 0.171 | -0.243 | -0.102 | 0.0974 | 0.249 | 0.196 | 0.38 |
| incident_obstructive_cad | 0.54 | 0.51 | 0.193 | 0.407 | 0.284 | -0.206 | 0.213 | 0.0218 | 0.482 | 0.183 | -0.234 | 0.196 | 0.269 | 0.0456 | 0.109 | 0.206 | 0.0815 | 0.0732 | -0.123 | 0.169 | 0.234 | 0.685 | 1.04 | 1.04 | 0.914 |
| worst_category_worsened | 0.242 | 0.299 | 0.0913 | 0.23 | 0.141 | -0.0186 | 0.066 | 0.0263 | 0.225 | 0.127 | -0.138 | 0.147 | 0.11 | -0.0253 | 0.118 | 0.116 | 0.0488 | 0.0632 | -0.118 | 0.138 | 0.117 | 0.0731 | 0.14 | -0.0216 | 0.0622 |
| incident demo_hist_myocardial_infarction | 0.791 | 0.0629 | -0.0644 | 0.0398 | 0.528 |  | 0.492 | 0.0131 |  | 0.341 | -0.293 | 0.447 | 0.294 | 0.208 | 0.433 | 0.455 | 0.496 | 0.0705 | 0.194 | -0.421 | 0.506 | -0.191 | -0.0725 | -0.176 | 0.0091 |
| incident demo_hist_coronary_revasc | 0.791 | 0.112 | 0.0737 | 0.423 | 0.713 |  | 0.0635 | 0.622 |  | -0.272 | -0.706 | -0.0879 | 0.321 | 0.208 | 0.433 | 0.0723 | 0.496 | 0.0705 | -0.52 | -0.421 | 0.506 | -0.0877 | 1.1 | 1.04 | 1.17 |
| incident demo_hist_stroke_tia | 0.431 | 0.432 | 0.227 | 0.429 | 0.217 | 0.215 | 0.293 | -0.134 |  | 0.204 | -0.158 | 0.313 | 0.0526 | 0.0287 | 0.208 | 0.126 | -0.195 | 0.196 | 0.0203 | -0.412 | -0.192 | 0.324 | 0.202 | 0.281 | 0.176 |
| incident hist_angina | -0.287 | 0.222 | 0.109 | -0.0644 | 0.0382 | -0.0725 | -0.0224 | -0.288 | 0.177 | 0.0359 | -0.153 | 0.0526 | 0.143 | 0.205 | 0.0631 | 0.356 | 0.143 | 0.126 | 0.0932 | -0.0177 | 0.102 | -0.125 | -0.0514 | -0.0115 | -0.0336 |
| incident hist_diabetes | 0.32 | 0.113 | 0.995 | 0.577 | 0.551 | 1.03 | 0.0373 | 0.229 | 1.86 | -0.0106 | -0.909 | 0.103 | 0.615 | 0.0458 | 0.0705 | 0.208 |  | 0.182 | -0.0828 | 0.317 | 0.379 | 0.147 | 0.0873 | 0.119 | 0.0775 |
| incident ct_cag_stent |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| incident ct_cag_cabg |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| incident hard composite (MI/revasc/stent/CABG) | 0.487 | -0.0535 | -0.137 | 0.23 | 0.663 |  | 0.101 | 0.293 |  | 0.174 | -0.3 | 0.329 | 0.1 | 0.271 | 0.34 | 0.0744 | 0.35 | -0.017 | -0.189 | -0.435 | 0.167 | -0.223 | 0.666 | 0.719 | 0.74 |

## 13. Loss to follow-up: BL characteristics with vs without FU

| | with FU: mean | without FU: mean | SMD |
|---|---|---|---|
| male | 0.456 |  |  |
| scan_age | 55.9 |  |  |
| clin_bmi | 25.9 |  |  |
| clin_bp_sys_mean | 134 |  |  |
| clin_bp_dia_mean | 81 |  |  |
| hr_during_scan | 53.2 |  |  |
| creatinine | 77.8 |  |  |
| egfr | 88.7 |  |  |
| hba1c | 35.7 |  |  |
| tot_cholesterol | 5.33 |  |  |
| hdl | 1.49 |  |  |
| ldl | 3.15 |  |  |
| triglyceride | 1.63 |  |  |
| hist_smoking_current | 0.1 |  |  |
| hist_smoking_former | 0.428 |  |  |
| hist_smoking_years | 22.5 |  |  |
| hist_diabetes | 0.0189 |  |  |
| demo_hist_family_cvd | 0.31 |  |  |
| demo_hist_family_hypercholesterolemia | 0.499 |  |  |
| med_lipid_lowering_any | 0.0895 |  |  |
| med_antihypertensive_any | 0.144 |  |  |
| ct_cacs_sum | 68.7 |  |  |
| ct_cag_sis | 1.22 |  |  |
| ct_cag_sss | 1.93 |  |  |
| ct_cag_plaque_type_score | 2.49 |  |  |

## 14. Image quality and evaluability (paired patients)

### BL

#### bad_quality

| | |
|---|---|
| False | 2116 |

#### scan_qualitative_quality

| | |
|---|---|
| 0 | 1539 |
| 1 | 331 |
| missing | 246 |

#### ct_cag_incomplete

| | |
|---|---|
| 0 | 1022 |
| 15 | <5 |
| 16 | 798 |
| 17 | hidden |

#### ct_cag_uneval

| | |
|---|---|
| 0 | 498 |
| 1 | 1348 |
| 2 | 155 |
| 3 | 58 |
| 4 | 26 |
| 5 | 11 |
| 6 | 8 |
| 7 | 5 |
| 8 | <5 |
| 9 | <5 |
| 10 | <5 |
| 11 | <5 |
| 12 | <5 |

#### PM

| | |
|---|---|
| 0 | 1149 |
| missing | 967 |

#### Phd_Subjektiv_finished

| | |
|---|---|
| 1 | 753 |
| missing | 1363 |

#### Readers_Plaque_analyses_finished

| | |
|---|---|
| 1 | 769 |
| missing | 1347 |

#### ct_cag_lad_uneval

| | |
|---|---|
| 0 | 2023 |
| 1 | 77 |
| 2 | 11 |
| 3 | <5 |
| 4 | <5 |

#### ct_cag_cx_uneval

| | |
|---|---|
| 0 | 578 |
| 1 | 1441 |
| 2 | 59 |
| 3 | 27 |
| 4 | hidden |
| 6 | <5 |

#### ct_cag_rca_uneval

| | |
|---|---|
| 0 | 1911 |
| 1 | 137 |
| 2 | 28 |
| 3 | 21 |
| 4 | 10 |
| 5 | 9 |

#### ct_cag_eval_n (evaluable segments)

| | |
|---|---|
| n | 2116 |
| mean | 16 |
| sd | 1.04 |
| p5 | 14 |
| p25 | 16 |
| median | 16 |
| p75 | 16 |
| p95 | 17 |

### FU

#### ct_cag_incomplete

| | |
|---|---|
| 0 | hidden |
| 17 | <5 |

#### ct_cag_uneval

| | |
|---|---|
| 0 | 1866 |
| 1 | 119 |
| 2 | 56 |
| 3 | 17 |
| 4 | 9 |
| 5 | 12 |
| 6 | <5 |
| 7 | <5 |
| 8 | 5 |
| 9 | <5 |
| 10 | <5 |
| 11 | <5 |
| 12 | <5 |
| 13 | <5 |
| 14 | <5 |
| 15 | <5 |
| 17 | 7 |

#### ct_cag_uneval_motion

| | |
|---|---|
| 0 | 1889 |
| 1 | 111 |
| 2 | 56 |
| 3 | 15 |
| 4 | 8 |
| 5 | 12 |
| 6 | <5 |
| 7 | <5 |
| 8 | <5 |
| 9 | <5 |
| 10 | <5 |
| 11 | <5 |
| 12 | <5 |
| 13 | <5 |
| 14 | <5 |
| 15 | <5 |
| 17 | <5 |

#### ct_cag_uneval_noise

| | |
|---|---|
| 0 | 2107 |
| 1 | <5 |
| 2 | <5 |
| 3 | <5 |
| 4 | <5 |
| 6 | <5 |

#### ct_cag_uneval_scanfield

| | |
|---|---|
| 0 | 2104 |
| 1 | <5 |
| 3 | <5 |
| 4 | <5 |
| 6 | <5 |
| 8 | <5 |
| 14 | <5 |
| 17 | <5 |

#### ct_cag_uneval_contrastdefect

| | |
|---|---|
| 0 | 2109 |
| 1 | <5 |
| 8 | <5 |
| 9 | <5 |
| 17 | <5 |

#### ct_cag_uneval_pm

| | |
|---|---|
| 0 | 2116 |

#### ct_cag_uneval_other

| | |
|---|---|
| 0 | 2116 |

#### ct_cacs_eval_all

| | |
|---|---|
| 0 | 6 |
| 1 | 2110 |

#### ct_angio_heart_done

| | |
|---|---|
| 1 | 2116 |

#### ct_noncontrast_heart_done

| | |
|---|---|
| 1 | 2116 |

#### ct_cag_lad_uneval

| | |
|---|---|
| 0 | 2055 |
| 1 | 28 |
| 2 | 13 |
| 3 | <5 |
| 4 | hidden |
| 5 | 6 |
| 6 | 8 |

#### ct_cag_lad_uneval_contrast

| | |
|---|---|
| 0 | 2109 |
| 1 | 7 |

#### ct_cag_lad_uneval_scanfield

| | |
|---|---|
| 0 | 2108 |
| 1 | 8 |

#### ct_cag_lad_uneval_pm

| | |
|---|---|
| 0 | 2116 |

#### ct_cag_lad_uneval_noise

| | |
|---|---|
| 0 | hidden |
| 1 | <5 |

#### ct_cag_cx_uneval

| | |
|---|---|
| 0 | 2053 |
| 1 | 16 |
| 2 | 13 |
| 3 | 7 |
| 4 | 6 |
| 5 | 10 |
| 6 | 11 |

#### ct_cag_cx_uneval_contrast

| | |
|---|---|
| 0 | 2110 |
| 1 | 6 |

#### ct_cag_cx_uneval_scanfield

| | |
|---|---|
| 0 | 2110 |
| 1 | 6 |

#### ct_cag_cx_uneval_pm

| | |
|---|---|
| 0 | 2116 |

#### ct_cag_cx_uneval_noise

| | |
|---|---|
| 0 | hidden |
| 1 | <5 |

#### ct_cag_rca_uneval

| | |
|---|---|
| 0 | 1891 |
| 1 | 115 |
| 2 | 63 |
| 3 | 18 |
| 4 | 9 |
| 5 | 20 |

#### ct_cag_rca_uneval_contrast

| | |
|---|---|
| 0 | 2110 |
| 1 | 6 |

#### ct_cag_rca_uneval_scanfield

| | |
|---|---|
| 0 | 2109 |
| 1 | 7 |

#### ct_cag_rca_uneval_pm

| | |
|---|---|
| 0 | 2116 |

#### ct_cag_rca_uneval_noise

| | |
|---|---|
| 0 | 2110 |
| 1 | 6 |
