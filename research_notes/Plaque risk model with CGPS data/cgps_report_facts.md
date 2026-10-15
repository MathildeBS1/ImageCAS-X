# CGPS aggregate statistics: facts that matter for choosing and sizing the plaque risk-prediction model

Sources (local only, nothing sent anywhere):
- R = `/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/report.md` (6,173 lines, generated 12:50; every number below is quoted exactly with its report section/heading as "R §x > heading")
- S = `/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/cgps_stats.py` (modified 15:36, i.e. **after** the report)
- C = `/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/CLAUDE.md` (variable inventory)

Privacy: counts 1-4 appear as "<5" and some cells as "hidden" (secondary suppression) in R; these are reproduced as-is and never back-calculated. Where I combine published aggregates (marked "derived"), I only add up cells that are shown in R as numbers, and give a range where a suppressed cell is involved.

**Most important caveat up front: R has no "section 0" (the chosen plaque-free LAD/CX/RCA trunk design).** `artery_design()` and the extra strata "BL segment reads present" and "BL scan year" exist in S (S lines 809-899, 1151, 1156-1158) but not in R (`grep` for "Chosen design", "BL segment reads", "scan year" in R returns 0 hits). So the exact trunk-design n/events, the trunk ICC and the read-vs-unread comparison **are not available yet**. The script has to be re-run in the secure environment. Below I give the closest proxies R does contain, with bounds.

---

## 1. Vessel-level trunk design: eligible n and events (per artery, pooled, RCA with/without LM rule, read vs unread, participant level)

### Takeaway
R contains no trunk-design output, so the exact numbers are a gap. Proxies from R §5/§7 put each trunk at roughly 300-450 (LAD), 650-850 (CX) and 600-710 (RCA) eligible arteries, all from the ~1,020 patients with BL segment reads, with a 35-45% new-plaque rate. Pooled that is about 1,800 arteries and about 700 events. Clustering is moderate (vessel-level ICC 0.27, design effect 1.46). At participant level only 264 read patients are plaque-free across the whole tree, and 124 of them (47.0%) develop plaque.

### Cited Findings
**How S defines the design (section 0, `artery_design`, S lines 809-899):**
- Trunks: LAD = plad, mlad, dlad; CX = pcx, mcx, dcx; RCA = prca, mrca, drca (`TRUNKS`, S line 95). No side branches. — [S](../../CGPS_data/cgps_stats.py)
- Eligible: all 3 trunk segments evaluable (stenosis label decoded to a number; "uneval_*" and empty → NaN → not evaluable) **and** all "none" (code 0) at BL. LAD and CX also need LM stenosis = 0. RCA is run twice: without the LM rule ("RCA") and with it ("RCA (also LM plaque-free)"). — [S](../../CGPS_data/cgps_stats.py)
- Outcome: any trunk segment ≥ minimal (code ≥1) at FU. It is set to unknown (NaN) when no plaque is seen and ≥1 trunk segment is unevaluable/missing at FU. Secondary thresholds: ≥ mild (2) and ≥ moderate (3). — [S](../../CGPS_data/cgps_stats.py)
- Additional outputs S would produce: eligibility flow, a "noise check" (trunk plaque at BL → none at FU), which segment the new plaque appeared in, a calcium cross-check (eligible but vessel CAC > 0 at BL = "plaque missed?"), a combined definition (also vessel CAC = 0), single-predictor AUCs (SCORE2-type variables, non-HDL, log(1+CAC), "segments with plaque elsewhere", FU years), FU tertile rates, pooled ICC/design effect, eligible arteries per patient, and rates by rand_group. — [S](../../CGPS_data/cgps_stats.py)
- **Consequence of the definition:** unread BL patients have empty segment fields. That makes `sb.notna().all()` False, so S **excludes all ~1,094 unread patients automatically**. Section 0, as written, is a read-subgroup-only analysis. — [S](../../CGPS_data/cgps_stats.py); [R §5 > text labels decoded (BL)](../../CGPS_data/report.md)

**Who has BL segment reads:**
- Every trunk segment's BL stenosis is "empty" in 1,094 patients (prca 1,093). Recognised + uneval = 1,022 for each segment. — [R §5 > text labels decoded (BL)](../../CGPS_data/report.md)
- Patient-level segment outcomes have n = 1,020 ("any new plaque" 777/1,020, 76.2%). "Segments with new plaque per patient" is missing for 1,096. — [R §5 > patient level](../../CGPS_data/report.md)
- At FU almost all segments are read: trunk segments "empty" <5 each. — [R §5 > text labels decoded (FU)](../../CGPS_data/report.md)

**Per-segment BL plaque-free counts (upper bounds for trunk eligibility; n = plaque-free at BL with FU plaque type known):**
- pLAD 446 → new plaque 197 (44.2%); mLAD 544 → 200 (36.8%); dLAD 822 → 186 (22.6%). — [R §5 > per segment > plad/mlad/dlad > new plaque (among plaque-free at BL)](../../CGPS_data/report.md)
- pCX 845 → 273 (32.3%); mCX 893 → 132 (14.8%); dCX 908 → 56 (6.2%). — [R §5 > per segment > pcx/mcx/dcx](../../CGPS_data/report.md)
- pRCA 723 → 210 (29.0%); mRCA 708 → 246 (34.7%); dRCA 842 → 186 (22.1%). — [R §5 > per segment > prca/mrca/drca](../../CGPS_data/report.md)
- LM 802 plaque-free → 196 (24.4%). — [R §5 > per segment > lm](../../CGPS_data/report.md)
- So the LAD trunk is capped at ≤ ~446 eligible because the pLAD is the most often diseased segment (BL plaque in pLAD: 571 plaque types recognised vs 448 "set to no plaque"). — [R §5 > text labels decoded (BL) > ct_cag_plad_plaque_type](../../CGPS_data/report.md)

**Closest existing proxy: vessel level, "plaque-free → plaque" (R §7 > level: vessel).** Vessels here include side branches: LAD = plad, mlad, dlad, d1, d2; CX = pcx, mcx, dcx, om1, om2; RCA = prca, mrca, drca, pda, pla. Only segments assessed at both visits count. There is no LM rule and no all-evaluable rule.
- LAD 139/321 (43.3%); CX 277/757 (36.6%); RCA 281/711 (39.5%); LM 196/802 (24.4%). — [R §7 > level: vessel > events / n (%) per unit](../../CGPS_data/report.md)
- Pooled over the 4 units (incl. LM): 2,591 units, 893 events (34.5%), regression 123 (8.5%), progression:regression 7.26, 599 patients with an event, **ICC within patient 0.272, design effect 1.46**, max 89 predictors at 10 EPV. — [R §7 > level: vessel > outcome summary](../../CGPS_data/report.md)
- Derived (sum of the three shown cells, LM excluded): LAD+CX+RCA = 1,789 units, 697 events (39.0%).
- A broader vessel outcome, "new plaque in a plaque-free segment" (eligible if any segment is plaque-free): LAD 539/996 (54.1%), CX 427/1,004 (42.5%), RCA 474/999 (47.4%). Pooled 1,636/3,801 (43%), ICC 0.235, design effect 1.64. — [R §7 > level: vessel](../../CGPS_data/report.md)
- Single-predictor AUCs for vessel "plaque-free → plaque": scan_age 0.611, male 0.608, ldl 0.56, hdl 0.432 (inverse, i.e. 0.568), clin_bp_sys_mean 0.616, hist_smoking_current 0.51, hist_diabetes 0.5, med_lipid_lowering_any 0.527, **ct_cacs_sum 0.697**, follow-up years 0.539. — [R §7 > level: vessel > AUC of single BL predictors](../../CGPS_data/report.md)
- Kappa between vessel "plaque-free → plaque" and vessel "incident CAC" = 0.802, and with "CAC increase" = 0.789. New plaque in clean vessels largely coincides with new calcium. — [R §7 > level: vessel > agreement (Cohen's kappa)](../../CGPS_data/report.md)

**Position level (the trunk-only analogue, but split by proximal/mid/distal, not by artery):**
- "plaque-free → plaque": proximal (LM, pLAD, pCX, pRCA) 181/362 (50.0%); mid 228/511 (44.6%); distal 262/777 (33.7%); side branches 248/736 (33.7%). Pooled ICC 0.382, design effect 1.62. — [R §7 > level: position](../../CGPS_data/report.md)
- Share of whole-tree "plaque-free → plaque" events that occur in each position: proximal 83.1%, mid 55.3%, distal 23.8%, side branches 25%. — [R §7 > level: position > % of whole-tree events](../../CGPS_data/report.md)

**Participant level:**
- Read patients plaque-free across the whole tree at BL: 264 → "plaque-free → plaque" 124 (47.0%), max 12 predictors at 10 EPV. — [R §7 > level: whole tree > outcome summary](../../CGPS_data/report.md)
- Among those 264 by FU tertile: 44/91 (48.4%), 25/60 (41.7%), 55/113 (48.7%). — [R §7 > level: whole tree > event % by follow-up interval tertile](../../CGPS_data/report.md)
- Single-predictor AUCs (whole-tree "plaque-free → plaque"): scan_age 0.634, male 0.542, ldl 0.602, hdl 0.446, SBP 0.57, smoking 0.527, diabetes 0.493, ct_cacs_sum 0.558, FU years 0.542. — [R §7 > level: whole tree > AUC](../../CGPS_data/report.md)
- Worst-category table: BL "none" row = 134 none / 71 minimal / 36 mild / hidden moderate / <5 severe at FU. — [R §8 > worst stenosis category BL -> FU](../../CGPS_data/report.md)

**Unread BL subgroup (the "missing" row of BL→FU tables; FU data only):**
- Worst category at FU for the 1,094 without BL reads: none 542, minimal 255, mild 175, moderate 74, severe 40, missing 8. — [R §8 > worst stenosis category BL -> FU, row "missing"](../../CGPS_data/report.md)
- Derived: unread with any plaque at FU = 544/1,086 (50.1%), vs 124/264 (47.0%) in read whole-tree plaque-free patients. Moderate+severe at FU in unread = 114/1,086 (10.5%). The read "none" row has a hidden moderate cell, so that share cannot be compared exactly.
- Unread segments with FU plaque, derived from the plaque-type "missing" rows: mLAD 262/1,082 (24.2%) vs 36.8% in read plaque-free mLAD; dLAD 115/1,073 (10.7%) vs 22.6%; pCX 145/1,075 (13.5%) vs 32.3%; pRCA 150/1,050 (14.3%) vs 29.0%; mRCA 183/977 (18.7%) vs 34.7%. pLAD ≈ 325-329/~1,081 (~30%) vs 44.2%. mCX ≈ 5%, dCX ≈ 2%, dRCA ≈ 7% (ranges because of hidden/<5 cells). — [R §5 > per segment > plaque type BL -> FU, row "missing"](../../CGPS_data/report.md)
- SIS BL = 0 in 1,352 patients, but CAC BL = 0 in only 1,261 (n = 2,109). Derived: at least ~84-91 SIS-0 patients have BL CAC > 0, so they had calcified plaque that the SIS did not record (this includes read and unread). — [R §4 > sis > BL = 0](../../CGPS_data/report.md); [R §3 > CAC = 0](../../CGPS_data/report.md)

### Inferences
- **The trunk design has ~1,020 patients and at most ~1,800 artery units, not 2,116 / ~6,000.** Per-artery minority-class counts from the proxies: LAD ~130-200 events, CX ~250-280, RCA ~250-280. The LM rule will shrink LAD/CX further because LM plaque is present in ~21% of read patients (207 LM plaque types recognised among ~1,012 read).
- If the unread 1,094 were really plaque-free and evaluable, the sample would roughly triple (up to ~3×1,094 more trunk units). R gives indirect support for "genuinely normal": the whole-tree FU plaque rate in unread (50.1%) is close to that of read whole-tree-normal patients (47.0%). Their per-segment rates are about half those of read plaque-free segments, which fits "read plaque-free segments sit in patients with plaque elsewhere". On the other side, the unread have 10.5% moderate+ at FU, and ≥ ~84 SIS-0 patients have CAC > 0. That is a reason to check the BL volumes before pooling.
- The RCA analysis with the LM rule vs without it can only be compared after the re-run.
- New plaque in clean vessels is mostly calcified at FU (e.g. pLAD BL-none → FU: 107 calcified, 60 mostly calcified, 18 mostly non-calcified, hidden non-calcified — [R §5 > plad > plaque type BL -> FU](../../CGPS_data/report.md)) and agrees strongly with incident CAC (κ 0.80). BL CAC is the strongest single predictor (AUC ~0.70 at vessel level), so geometry has to show added value on top of CAC and plaque elsewhere.

### Gaps
- Exact eligible n, events, LM-rule effect, ICC, eligible arteries per patient, calcium cross-check and AUCs for the trunk design: **not in R**. Re-run S (section 0) in the secure environment.
- Read-vs-unread strata ("BL segment reads present") and scan-year strata exist only in S, not in R.
- Whether the unread 1,094 are truly normal (vs never read) cannot be settled from aggregates.
- How many read patients are eligible in ≥1 trunk at participant level ("any new plaque in any eligible trunk") is not in R.

---

## 2. Event counts and events-per-variable for every binary and continuous outcome

### Takeaway
Plaque and calcium outcomes are common (35-80%), so EPV is limited by the non-event class or by n, not by rarity. Patient-level segment outcomes are restricted to n = 1,020. Hard clinical events (10/1,973) cannot be modelled.

### Cited Findings
**Binary outcomes: n, events, %, max predictors at 10 / 20 EPV** — all from [R §2 > binary outcomes](../../CGPS_data/report.md):
- incident_cac (BL=0 → FU>0): 1,261 / 478 / 37.9% / 47 / 23
- cac_any_increase: 2,109 / 1,274 / 60.4% / 83 / 41
- cac_progression_hokanson (Δ√CAC ≥ 2.5): 2,109 / 1,053 / 49.9% / 105 / 52
- cac_annual_change_ge_15pct (BL>0): 848 / 305 / 36% / 30 / 15
- cac_decrease (data check): 2,109 / 49 / 2.3% / 4 / 2
- sss_increase: 2,116 / 1,254 / 59.3% / 86 / 43
- sss_increase_ge2: 2,116 / 1,022 / 48.3% / 102 / 51
- sis_increase: 2,116 / 1,220 / 57.7% / 89 / 44
- plaque_type_score_change: 2,116 / 1,369 / 64.7% / 74 / 37
- any segment stenosis progression: 1,020 / 810 / 79.4% / 21 / 10
- any new plaque: 1,020 / 777 / 76.2% / 24 / 12
- any new high-risk feature: 763 / 151 / 19.8% / 15 / 7
- no plaque → plaque (SIS, among "no plaque →"): 1,352 / 668 / 49.4% / 66 / 33
- plaque → more (SIS): 764 / 552 / 72.3% / 21 / 10
- plaque → less (SIS): 764 / 107 / 14% / 10 / 5
- incident_obstructive_cad: 876 / 285 / 32.5% / 28 / 14
- worst_category_worsened: 1,020 / 532 / 52.2% / 48 / 24
- incident MI: 1,028 / 6 / 0.6% / 0 / 0
- incident coronary revasc: 1,028 / 6 / 0.6% / 0 / 0
- incident stroke/TIA: 891 / 31 / 3.5% / 3 / 1
- incident angina: 2,108 / 96 / 4.6% / 9 / 4
- incident diabetes: 2,071 / 61 / 2.9% / 6 / 3
- incident stent: 699 / <5 / <5 / 0 / 0
- incident CABG: 1,835 / 0 / 0 / 0 / 0
- incident hard composite (MI/revasc/stent/CABG): 1,973 / 10 / 0.5% / 1 / 0

**Continuous outcomes:** delta_cac, delta_cac_per_year, delta_sqrt_cac, delta_log1p_cac n = 2,109. All SIS/SSS/plaque_type_score deltas (total and per vessel) and delta_sss_per_year n = 2,116. n_segments_new_plaque n = 1,020. — [R §2 > continuous outcomes](../../CGPS_data/report.md)
- Δ√CAC: mean 4.29, SD 5.76, median 2.46, p75 6.93, p95 14.9. Δlog1p CAC median 0.73. ΔCAC/yr median 1.06, p95 57.5. — [R §3 > change](../../CGPS_data/report.md)
- Among BL CAC > 0 (n = 848): ΔCAC/yr median 13.2; Δ√CAC median 6.77. — [R §3 > change among BL CAC > 0](../../CGPS_data/report.md)
- ΔSIS mean 1.76 (SD 2.48), median 1, value 0 in 789, negative in 107 (5.1%), ≥2 in 883 (41.7%). — [R §4 > sis](../../CGPS_data/report.md)
- ΔSSS mean 3.26 (SD 5.14), median 1, 0 in 742, ≥10 in 242, decrease 120 (5.7%). ΔSSS/yr median 0.104, p95 1.26. — [R §4 > sss](../../CGPS_data/report.md)
- Δplaque_type_score: increase 1,079 (51%), decrease 290 (13.7%), ≤ -5 in 92. — [R §4 > plaque_type_score](../../CGPS_data/report.md)
- n_segments_new_plaque: 0 = 243, 1 = 191, 2 = 150, 3 = 163, 4 = 92, 5 = 71, 6 = 48, 7 = 32, 8 = 16, 9 = 7, 10 <5, 11 <5. — [R §5 > patient level > segments with new plaque per patient](../../CGPS_data/report.md)

**Per vessel (recorded scores, n = 2,116, unread counted as 0 at BL):**
- LAD: SIS increase 1,002 (47.4%); ΔSIS ≥2 508 (24%); SSS increase 1,107 (52.3%); BL SIS = 0 1,387 (65.5%); FU = 0 812 (38.4%); plaque-type-score decrease 360 (17%). — [R §4 > lad_sis / lad_sss / lad_plaque_type_score](../../CGPS_data/report.md)
- CX: SIS increase 626 (29.6%); ≥2 245 (11.6%); SSS increase 659 (31.1%); BL = 0 1,835 (86.7%); FU = 0 1,364 (64.5%). — [R §4 > cx_*](../../CGPS_data/report.md)
- RCA: SIS increase 709 (33.5%); ≥2 354 (16.7%); SSS increase 751 (35.5%); BL = 0 1,802 (85.2%); FU = 0 1,304 (61.6%). — [R §4 > rca_*](../../CGPS_data/report.md)
- SIS trajectories, "no plaque → plaque": whole tree 668 (31.6%); LAD 623 (29.4%); CX 502 (23.7%); RCA 533 (25.2%). "No → no": 684 / 764 / 1,333 / 1,269. — [R §6 > patient level](../../CGPS_data/report.md)

**Per-vessel CAC (n, events, %):**
- LM: BL>0 203/2,109 (9.6%); new 315/1,904 (16.5%). LAD: BL>0 721 (34.2%); new 475/1,384 (34.3%). CX: BL>0 309 (14.7%); new 382/1,798 (21.2%). RCA: BL>0 385 (18.3%); new 368/1,723 (21.4%). — [R §3 > per vessel](../../CGPS_data/report.md)
- Total CAC = 0: BL 1,261/2,109 (59.8%) → FU 805/2,116 (38%). BL 0 → FU 0 in 783. — [R §3 > CAC = 0; CAC BL category -> FU category](../../CGPS_data/report.md)
- Vessel-level pooled: incident CAC 1,540/6,809 (22.6%), ICC 0.299, design effect 1.7. CAC increase 2,930/8,426, ICC 0.383, design effect 2.15. — [R §7 > level: vessel > outcome summary](../../CGPS_data/report.md)

**Segment level (pooled):** new plaque 2,479/13,168 (18.8%), ICC 0.145, design effect 2.73. Stenosis progression 3,387/15,655 (21.6%). New spotty calcification 167/1,036 (16.1%). New napkin-ring 61/2,551 (2.4%). — [R §5 > pooled over segments; R §7 > level: segment > outcome summary](../../CGPS_data/report.md)

### Inferences
- For a trunk design with ~700 pooled events and ~1,100 non-events, raw 10 EPV allows ~69 parameters. Dividing by the design effect (1.46, vessel-level proxy) gives an effective ~48. Per artery: LAD ~13, CX/RCA ~27-28 at 10 EPV (proxy counts). Riley-type sample-size criteria were not computed in R.
- Incident CAC (478/1,261 at patient level; 1,540/6,809 vessel-level) and Hokanson CAC progression (n = 2,109) are the only image outcomes that use **all 2,116 patients without depending on BL segment reads**.
- Hard events (10) rule out clinical-outcome models.

### Gaps
- EPV for the trunk outcome itself (pending section 0).
- No per-trunk (trunk-only) continuous outcomes; the vessel scores include side branches. The recorded LAD SIS only matches the segment-derived LAD extent exactly in 79.2% (BL) / 63.7% (FU), so the recorded LAD score probably includes LM or IM. — [R §7 > derived vs recorded scores](../../CGPS_data/report.md)

---

## 3. Follow-up interval distribution: does it need an offset or time-to-event handling?

### Takeaway
Everyone has a single FU scan 9.5-15.3 years after BL (median 10, right-skewed). Event rates rise only modestly in the longest tertile and FU time alone has AUC ~0.53-0.55. Use logistic regression with FU time as a covariate, or a cloglog link with a log(time) offset, rather than time-to-event: the event time is unknown, so the outcome is interval-censored at a single visit.

### Cited Findings
- n = 2,116, mean 11, SD 1.84, p5 9.52, p25 9.65, median 10, p75 12.2, p95 15.3 years. 0 missing, 0 ≤ 0, 0 < 1 year, all 2,116 ≥ 5 years. — [R §1 > follow-up interval (years, paired); follow-up interval checks](../../CGPS_data/report.md)
- By rand_group: median 10.1 / 10 / 9.99; p75 12 / 12 / 12.5; mean 10.9 / 10.9 / 11.1. — [R §11 > rand_group > follow-up years](../../CGPS_data/report.md)
- Lipid-lowering "started" group: mean 11.3, p75 12.9. Missing-medication group: mean 9.89, p95 10.1. — [R §11 > lipid-lowering BL -> FU > follow-up years](../../CGPS_data/report.md)
- FU tertile (short / middle / long) event rates:
  - segment new plaque 17.8% / 17.0% / 21.5% — [R §7 > level: segment > event % by follow-up interval tertile](../../CGPS_data/report.md)
  - vessel "plaque-free → plaque" 33.3% / 30.7% / 38.6%; vessel incident CAC 20.8% / 19.2% / 27.6%; Hokanson 23.9% / 23.0% / 30.7% — [R §7 > level: vessel > event % by FU tertile](../../CGPS_data/report.md)
  - whole tree "plaque-free → plaque" 48.4% / 41.7% / 48.7%; incident CAC 34.0% / 35.2% / 44.1% — [R §7 > level: whole tree > event % by FU tertile](../../CGPS_data/report.md)
- AUC of FU years alone: vessel "plaque-free → plaque" 0.539; incident CAC 0.549; Hokanson 0.543; segment new plaque 0.532. — [R §7 > AUC tables](../../CGPS_data/report.md)

### Inferences
- About half the cohort has an interval of 9.5-10 years and a quarter has > 12.2 years. The spread is real but narrow relative to the 10-year horizon, and the dose-response is flat between tertiles 1 and 2. A FU-time covariate (or log-time offset with a cloglog link) is cheap and defensible. Full survival models are not identifiable with one FU scan.
- FU duration correlates with statin start (11.3 y vs 10.9 y). Adjusting for time partly also adjusts for trial-arm/clinic timing.

### Gaps
- Why some intervals are 12-15 years (rescans, scan-year cohorts) is not explained in R. The "BL scan year" stratum in S was not in this R.

---

## 4. Missingness per baseline predictor; which SCORE2 variables are complete

### Takeaway
All SCORE2 inputs are ≥ 98% complete: age, sex and smoking 0 missing, SBP 26, total cholesterol/HDL 38, diabetes 5. BMI, HbA1c, smoking-years, heart rate during scan and BL MI/revasc history are ~50-89% missing and should be excluded or treated as unavailable.

### Cited Findings
- Missing out of 2,116: male 0; scan_age 0; clin_bmi 1,085; clin_bp_sys_mean 26; clin_bp_dia_mean 32; hr_during_scan 1,881; creatinine 39; egfr 39; hba1c 1,125; tot_cholesterol 38; hdl 38; ldl 33; triglyceride 38; hist_smoking_current 0; hist_smoking_former 0; hist_smoking_years 1,009; hist_diabetes 5; demo_hist_family_cvd 12; demo_hist_family_hypercholesterolemia 8; med_lipid_lowering_any 50; med_antihypertensive_any 51; ct_cacs_sum 7; ct_cag_sis/sss/plaque_type_score 0. — [R §2 > BL predictors > missing per predictor](../../CGPS_data/report.md)
- 0 complete cases on all 25 predictors. Predictors with ≥ 20% missing: clin_bmi, hr_during_scan, hba1c, hist_smoking_years. 1,974 complete cases on the < 20%-missing set. — [R §2 > BL predictors (paired patients)](../../CGPS_data/report.md)
- BL history columns are ~51% missing: MI 50.8 / 50.6 / 53.1% by rand_group; revasc the same; stroke/TIA 50.8 / 50.5 / 53.1%; ct_cag_stent 66-68%. — [R §11 > rand_group > % missing at BL](../../CGPS_data/report.md)
- Missingness is similar across rand_groups for SCORE2 variables (SBP 1.4 / 1.3 / 0.9%; cholesterol 1.5 / 1.5 / 2.5%) and by sex. — [R §11 > % missing at BL (rand_group; male)](../../CGPS_data/report.md)
- Prevalences (BL means, paired): male 0.456, age 55.9, SBP 134, total cholesterol 5.33, HDL 1.49, LDL 3.15, current smoking 0.1, former 0.428, **diabetes 0.0189**, family CVD 0.31, lipid-lowering 0.0895, antihypertensive 0.144, CAC sum mean 68.7. — [R §13 > with FU: mean](../../CGPS_data/report.md)
- S's `DESIGN_PREDICTORS` = scan_age, male, hist_smoking_current, clin_bp_sys_mean, tot_cholesterol, hdl, hist_diabetes, med_lipid_lowering_any, med_antihypertensive_any, demo_hist_family_cvd, plus derived non-HDL, log(1+CAC), segments with plaque elsewhere and FU years. — [S lines 96-97, 816-822](../../CGPS_data/cgps_stats.py)
- Variables exist in both BL and FU unless noted (statin, DOAC etc. FU only). — [C](../../CGPS_data/CLAUDE.md)

### Inferences
- About 1,085-1,125 missing for BMI/HbA1c, close to the 1,094 unread. Together with ~51% missing BL MI history, this suggests the unread half also has a thinner BL clinical form. This cannot be confirmed without the read-status stratum. Within the read subgroup, BMI/HbA1c may be much more complete.
- Diabetes prevalence ~1.9% (~40 patients overall, mostly rand_group 2: 4.97% vs 0.55/0.54%). Inside ~1,000 read patients with clean trunks there may be only a handful of diabetics. That is a separation / unstable-coefficient risk, so consider dropping diabetes or shrinking its coefficient, or using SCORE2 as a single linear predictor.
- Multiple imputation is only needed for small fractions (≤ 2.4%) of the SCORE2 / medication variables.

### Gaps
- Missingness within the read subgroup and within eligible trunks is not reported.

---

## 5. Differences by rand_group, by baseline-read status and image quality / evaluability

### Takeaway
rand_group 2 (n = 646) is a different, higher-risk population. It is older, has more lipid-lowering (26%) and diabetes (5%), and has more progression on every outcome. All 10 hard events are in this group. Read-status strata are missing from R. BL image-quality fields are largely uninformative. FU unevaluability is highest in the RCA (mid-RCA 197 unevaluable) and will cost RCA outcomes.

### Cited Findings
**rand_group:**
- Sizes 0: 725, 1: 745, 2: 646. — [R §11 > rand_group > group sizes](../../CGPS_data/report.md)
- BL means (0 / 1 / 2): age 54.9 / 54.6 / 58.5; male 0.423 / 0.458 / 0.491; SBP 132 / 134 / 138; total cholesterol 5.28 / 5.22 / 5.53; HDL 1.54 / 1.48 / 1.44; diabetes 0.0055 / 0.0054 / 0.0497; lipid-lowering 0.0156 / 0.015 / 0.26; antihypertensive 0.0979 / 0.0955 / 0.254; CAC 45.2 / 46 / 121; SIS 0.983 / 1.02 / 1.71. — [R §11 > rand_group > BL predictor mean](../../CGPS_data/report.md)
- Outcomes (% events, 0 / 1 / 2): any new plaque 71.5 / 70.7 / 85.8; no plaque → plaque (SIS) 44.9 / 43.4 / 64; incident CAC 34.5 / 33.9 / 50.3; Hokanson 44 / 42.6 / 65; incident obstructive 27.3 / 28.4 / 41.9; incident MI 0 / 0 / 2; revasc 0 / 0 / 2; stroke/TIA 0 / 0 / 12.1; hard composite 0 / 0 / 1.7; plaque → less 17.7 / 14.7 / 10.4. — [R §11 > rand_group > binary outcomes](../../CGPS_data/report.md)
- Medians (0 / 1 / 2): ΔSSS 1 / 1 / 3; Δ√CAC 1.73 / 1 / 4.87; ΔCAC/yr 0.34 / 0.156 / 4.97. — [R §11 > rand_group > continuous outcomes](../../CGPS_data/report.md)

**Lipid-lowering change BL → FU:** never 1,371; started 510; continued 168; stopped 17; missing 50. "Started" have higher BL LDL (3.73 vs 3.03) and more new plaque (82.7% vs 70.5%), incident CAC (53.3% vs 33.3%) and incident obstructive (40.3% vs 27.5%). — [R §11 > lipid-lowering BL -> FU](../../CGPS_data/report.md); [R §10 > med_lipid_lowering_any](../../CGPS_data/report.md). FU statin 677/2,116; statin > 2 years 522. — [R §10 > FU only](../../CGPS_data/report.md)

**Sex:** women 1,151, men 965. Any new plaque 64.9% vs 85.7%; no plaque → plaque 41.5% vs 63%; plaque → less 22.1% vs 8.9%; BL CAC 30.8 vs 114. — [R §11 > male (BL)](../../CGPS_data/report.md)

**Baseline-read status:** not stratified in R (gap). Indirect facts: 1,094 empty BL segment reads; BL worst-category flags available for 1,022 (obstructive at BL 145/1,022, 14.2%); FU obstructive 516/2,106 (24.5%). — [R §5 > text labels decoded (BL); R §8 > obstructive (moderate+) at BL / at FU](../../CGPS_data/report.md)

**Image quality / evaluability, BL:**
- bad_quality False in all 2,116. scan_qualitative_quality 0: 1,539, 1: 331, missing 246. ct_cag_incomplete 0: 1,022, 16: 798, 15 <5, 17 hidden. — [R §14 > BL](../../CGPS_data/report.md)
- ct_cag_uneval 0: 498, 1: 1,348, 2: 155, 3: 58, 4: 26, … ; IM stenosis "uneval" 1,482 (IM usually coded unevaluable/absent). ct_cag_cx_uneval 1: 1,441 (probably IM counted in CX); lad_uneval 0: 2,023; rca_uneval 0: 1,911. ct_cag_eval_n median 16 (p5 14). — [R §14 > BL; R §5 > text labels decoded (BL) > ct_cag_im_stenosis](../../CGPS_data/report.md)
- BL unevaluable trunk segments among the ~1,022 read: plad <5, mlad 11, dlad 5; pcx 10, mcx 17, dcx 67; prca 46, mrca 92, drca 59; LM 10. — [R §5 > text labels decoded (BL)](../../CGPS_data/report.md)
- The `_eval` columns use unexplained codes (e.g. plad 0: 1,953, 12: 81, 13: 73) and do not separate unread patients. — [R §5 > per segment > evaluable at BL](../../CGPS_data/report.md)

**Image quality / evaluability, FU:**
- ct_cag_uneval 0: 1,866, 1: 119, 2: 56, …, 17: 7. Motion is the dominant reason (motion 0: 1,889); noise, scan field and contrast are each almost always 0; PM 0 in all. — [R §14 > FU](../../CGPS_data/report.md)
- Per vessel unevaluable ≥ 1 segment: LAD 61 (derived from 2,116 − 2,055), CX 63 (2,116 − 2,053), RCA 225 (2,116 − 1,891). — [R §14 > FU > ct_cag_*_uneval](../../CGPS_data/report.md)
- FU trunk-segment uneval: plad 26, mlad 27, dlad 36; pcx 31, mcx 45, dcx 39; prca 81, mrca 197, drca 81; LM 15. — [R §5 > text labels decoded (FU)](../../CGPS_data/report.md)
- ct_cacs_eval_all 1: 2,110, 0: 6. — [R §14 > FU](../../CGPS_data/report.md)

### Inferences
- rand_group 2 looks like a non-randomised, higher-risk stratum. Include it as a covariate or sensitivity exclusion, and/or check whether it concentrates in the read or unread half. Pooling it unadjusted inflates apparent discrimination (risk-factor and event mix differ).
- Statin initiation during FU (510, ~27% of non-users) is a post-baseline intervention linked to both risk and plaque composition (more calcified). It cannot be a baseline predictor, but it may distort "new plaque" vs "new calcium" outcomes.
- With S's rule (outcome unknown if no plaque is seen and a segment is unevaluable), RCA will lose roughly up to ~10% of eligible arteries at FU (mid-RCA 197/2,116 uneval), and LAD/CX about 2-3%. BL evaluability also removes more RCA (and dCX) candidates than LAD.

### Gaps
- No rand_group × read-status cross-tab. The meaning of rand_group 2 is not in R or C (C only lists `rand_group` as FU trial/admin).
- Decoding of `_eval`, `ct_cag_incomplete` codes 15-17 and `scan_qualitative_quality` 0/1 is not documented.

---

## 6. Red flags for modelling

### Takeaway
The main threats are: the unread half and its unresolved status; reader noise (20% of BL plaque segments read as plaque-free at FU); clustering of arteries within patients (ICC ~0.24-0.38 at sub-patient levels); very sparse diabetes and hard events; rand_group 2 heterogeneity; and a completers-only cohort with no attrition data.

### Cited Findings
- **Reader noise / regression:** segment "new plaque" regression (plaque at BL → none at FU) 504/2,487 (20.3%), progression:regression 4.92. — [R §7 > level: segment > outcome summary](../../CGPS_data/report.md). At vessel level, "plaque-free → plaque" regression is 123 (8.5%), ratio 7.26 — [R §7 > level: vessel](../../CGPS_data/report.md). pLAD BL non-calcified (type 4) → FU none: 46 — [R §5 > plad > plaque type BL -> FU](../../CGPS_data/report.md). Stenosis regression data check: pLAD 123/1,003 (12.3%), mLAD 113/993 (11.4%). — [R §5 > per segment](../../CGPS_data/report.md)
- High-risk features are mostly noise: regression 1,064 vs 185 progression events (ratio 0.17) at segment level. — [R §7 > level: segment](../../CGPS_data/report.md)
- **Clustering:** ICC within patient: segment new plaque 0.145 (design effect 2.73); position "plaque-free → plaque" 0.382 (1.62); vessel "plaque-free → plaque" 0.272 (1.46); vessel incident CAC 0.299 (1.7); vessel CAC increase 0.383 (2.15). — [R §7 > outcome summary tables](../../CGPS_data/report.md)
- **Sparse cells:** hard composite 10/1,973; incident stent <5; CABG 0; MI 6; revasc 6; diabetes prevalence 0.0189; lap at FU ≤ 6 per segment; new napkin-ring <5 in many segments. — [R §2; R §5; R §13](../../CGPS_data/report.md)
- **Data-check inconsistencies:** stroke/TIA "yes at BL, no at FU" 119. cac_decrease 49 (2.3%). — [R §9 > demo_hist_stroke_tia; R §2](../../CGPS_data/report.md)
- **Ceiling/floor:** whole-tree "new plaque in a plaque-free segment" is 79.5-95% when BL max stenosis is ≥1, so whole-tree outcomes are near-saturated in diseased patients. — [R §7 > level: whole tree > event % by BL max stenosis grade](../../CGPS_data/report.md)
- **Attrition unknowable:** BL only 0, FU only 0. Section 13 shows only "with FU" means (no comparison group). — [R §1 > patients; R §13](../../CGPS_data/report.md)
- **Score coding:** recorded LAD SIS/SSS equal the segment-derived values in only 79.2% (BL) / 63.7% (FU), while tree/CX/RCA are 89.6-97.1%. — [R §7 > derived vs recorded scores](../../CGPS_data/report.md)
- **Disclosure:** S hides "k of n" when n − k < 5 or k = n in groups < 20 (S lines 113-166). Small strata of eligible arteries (e.g. diabetics, per-rand_group by artery) will appear as "<5"/"hidden" and cannot be used for diagnostics outside the secure environment. — [S](../../CGPS_data/cgps_stats.py)
- **Calcium overlap:** κ vessel "plaque-free → plaque" vs incident CAC 0.802. BL CAC AUC ~0.70 for vessel new plaque. — [R §7 > level: vessel](../../CGPS_data/report.md)

### Inferences
- Use patient-clustered methods for pooled LAD/CX/RCA: GEE or a random-intercept logistic model for estimation, cluster-robust SEs, and patient-level (grouped) CV folds and bootstrap. Otherwise optimism and CIs will be badly underestimated.
- Reader noise in "new plaque" (≥ minimal) argues for a sensitivity outcome at ≥ mild, which S already computes, or requiring concordant new CAC (S's "combined definition"). Expect attenuated discrimination either way.
- Separation risk mainly from diabetes, and from per-artery models with LAD's ~130-200 events and 10+ candidate predictors. Penalised (ridge/Firth) logistic regression or a single SCORE2 linear predictor are prudent.

### Gaps
- Trunk-specific ICC and noise-check counts are pending section 0.

---

## 7. Which outcome definitions are most feasible statistically

### Takeaway
Feasible:
- the pooled LAD+CX+RCA trunk "new plaque ≥ minimal" outcome (≈700 events among ≈1,800 arteries in the read half; design effect ~1.5)
- vessel-level incident CAC and Hokanson CAC progression, which use all 2,116 patients
- possibly whole-tree "no plaque → plaque" by SIS (668/1,352), but only if the unread half is accepted as normal

Not feasible:
- per-artery LAD models with many predictors
- whole-tree participant-level outcomes in read-normal patients (124 events)
- high-risk features
- clinical events

### Cited Findings
- Vessel "plaque-free → plaque": 893/2,591 events, 89 predictors at 10 EPV, progression:regression 7.26 (best signal-to-noise among plaque outcomes at vessel level except "incident obstructive" 9.85 / "burden ≥2" 8.91). — [R §7 > level: vessel > outcome summary](../../CGPS_data/report.md)
- Vessel incident CAC 1,540/6,809 (154 predictors), ratio 14.8. Hokanson 2,181/8,426 (218), ratio 24.8. — [R §7 > level: vessel](../../CGPS_data/report.md)
- Whole tree "plaque-free → plaque" (read only) 124/264, 12 predictors. — [R §7 > level: whole tree](../../CGPS_data/report.md)
- SIS "no plaque → plaque" (all 2,116, unread counted as SIS 0) 668/1,352 (49.4%), 66 predictors at 10 EPV. — [R §2 > binary outcomes](../../CGPS_data/report.md)
- Incident obstructive (vessel) 512/3,857 (13.3%), but strongly driven by BL stenosis (AUC BL burden 0.783). — [R §7 > level: vessel](../../CGPS_data/report.md)
- New high-risk feature (vessel) 158/739, ratio 0.2 (noise). — [R §7 > level: vessel](../../CGPS_data/report.md)

### Inferences
- Primary: pooled trunk "new plaque ≥ minimal", clustered logistic, SCORE2 linear predictor + log(1+CAC) + plaque elsewhere + FU time ± rand_group, then geometry as added value (ΔAUC/NRI with grouped CV). Roughly 45-65 effective parameters' worth of events, which is enough for a parsimonious geometry block.
- Sensitivity analyses:
  - ≥ mild threshold
  - "new plaque and vessel CAC 0 at BL"
  - RCA with vs without the LM rule
  - excluding rand_group 2
  - adding unread patients as plaque-free (if validated), which roughly triples the units
- A secondary outcome that does not depend on BL reads is vessel-level incident CAC in vessels with CAC 0 (LAD 475/1,384, CX 382/1,798, RCA 368/1,723).

### Gaps
- Final feasibility of the trunk outcome hinges on the section-0 re-run (eligible counts with the LM rule and all-segments-evaluable rules, and the trunk ICC).
