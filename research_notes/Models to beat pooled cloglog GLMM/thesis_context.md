# Internal thesis context: what any challenger to the pooled segment cloglog GLMM must respect

All sources are local files (repo root `/Users/mathildebrinchsorensen/Desktop/ImageCAS-X`, abbreviated `REPO`; authoritative plan `~/Desktop/Speciale/CGPS_statistics-`, abbreviated `PLAN`). No individual data exist locally; every number below is an aggregate copied from a file. Where a number is not in the files it is listed as a gap. Line numbers refer to the files as of 2026-11-02.

## 1. How the pooled "who" model is specified (and what the code actually does)

### Takeaway
The decided "who" engine is a segment-level cloglog GLMM over the 9 trunk segments with a normal person random intercept, fitted by Gauss–Hermite quadrature and pooled to person risk by integrating the shared frailty, P_i = 1 − ∫ exp(−e^b Σ_j exp(η_ij)) φ(b; 0, σ²) db, not by 1 − ∏(1 − p_s). The only implementation (`CGPS_data/progression_who_pooled.py` and its fixed successor `progression_who_pooled_t25.py`) runs on the Medis trees with a *progression* outcome, not on the plaque-free cohort with incident coronary plaque; the clean-cohort pooled model has not been coded or run.

### Cited Findings
- Decided design: "one segment-level cloglog GLMM over the 9 trunk segments (person random intercept), its segment risks pooled into one person risk ... Every who analysis, including the choice of base, is run in this pooled model, never a person-level one." — [REPO/CLAUDE.md](REPO/CLAUDE.md)
- Linear predictor / link (code docstring): segment cloglog GLMM, person random intercept b ~ N(0, s²), Gauss–Hermite quadrature with analytic gradient, pooled to person risk `P_i = 1 - int exp(-e^b sum_j exp(eta_ij)) phi(b; 0, s^2) db` — [progression_who_pooled.py:11–13](REPO/CGPS_data/progression_who_pooled.py)
- Negative marginal log-likelihood: `eta = (X @ beta)[:, None] + u[None]` with u = √2·s·x at Hermite nodes; `lij = np.where(one, np.log(-np.expm1(-mu)), -mu)` (cloglog Bernoulli), summed per person and log-sum-exp over nodes; small ridge `l2=1e-6` on β — [progression_who_pooled.py:134–150, 153](REPO/CGPS_data/progression_who_pooled.py)
- Fit: L-BFGS-B, log σ bounded to (−8, 3) i.e. s from 3e-4 to 20; default 30 nodes — [progression_who_pooled.py:68, 153–165, 455](REPO/CGPS_data/progression_who_pooled.py)
- Person risk (pooling): `S = np.add.reduceat(np.exp(X @ beta), starts_of(ids)); return 1 - (w * np.exp(-np.exp(u) * S)).sum(1)` with 40 Gauss–Hermite nodes — [progression_who_pooled.py:186–191](REPO/CGPS_data/progression_who_pooled.py)
- Segment marginal risk (for per-segment AUC only): integral over b of 1 − exp(−e^{u}·e^{η}) — [progression_who_pooled.py:179–183](REPO/CGPS_data/progression_who_pooled.py)
- Base model B2 (fixed effects), code: intercept, `log follow-up` as a free covariate (not an offset), z-scored log SCORE2 (or with `--person factors`: age, SBP, total cholesterol, HDL z-scored + male + current smoking), right dominance (right vs not), segment-position dummies (reference pLAD), `log length` (clipped at 1 mm), BL grade dummies; z constants learned on training persons — [progression_who_pooled.py:14–19, 100–121](REPO/CGPS_data/progression_who_pooled.py)
- Geometry model G02 in that code = B2 + segment mean turning angle T5 (z within segment type) + LM bifurcation angle (z) entered **only on the pLAD and pCX rows** (`X.append(a.fillna(0) * d["segment"].isin(ANGLE_SEGS))`); missing geometry set to z = 0 — [progression_who_pooled.py:18, 60, 122–129](REPO/CGPS_data/progression_who_pooled.py)
- The successor `progression_who_pooled_t25.py` adds a SCORE2-OP indicator, a `not split` indicator, BL grade merged to 4 levels, 100 nodes checked against twice as many, cold starts, paired person bootstrap (200), and has **mean T2.5 as the only geometric feature** (G03, 1 df LR test) — [progression_who_pooled_t25.py docstring lines 1–31](REPO/CGPS_data/progression_who_pooled_t25.py); [PLAN/experiments/who-progression/pooled_score2/G03_pooled_score2_t25/experiment.md](PLAN/experiments/who-progression/pooled_score2/G03_pooled_score2_t25/experiment.md)
- The run is explicitly on progression in the Medis trees: report header "The Medis trees are almost all people with plaque at baseline: this is progression, not new plaque"; segment outcome = higher grade at FU than at BL; ~90% of people expected to progress — [progression_who_pooled.py:7–9, 549–551](REPO/CGPS_data/progression_who_pooled.py); [PLAN/experiments/who-progression/setup.md](PLAN/experiments/who-progression/setup.md)
- Clean-cohort pooled baseline B2 (planned): person terms age, sex, current smoking, SBP, total cholesterol, HDL, log(follow-up), right vs non-right dominance; segment terms: one intercept per segment (9) and log(segment length); person random intercept; cloglog; result "Not run." — [PLAN/experiments/who/pooled_score2/B2_pooled_score2_linear/experiment.md](PLAN/experiments/who/pooled_score2/B2_pooled_score2_linear/experiment.md)
- The clean-cohort geometry experiment folder `who/pooled_score2/G02_pooled_score2_geommean/` exists but is empty (no experiment.md); the tree-engine G01 says "Not written yet." — [PLAN/experiments/who/](PLAN/experiments/who/)
- Plan's person-geometry definition for who: "LM angle and ratios: one value per person. Curvature and taper: the mean of within-segment-type z-scores over the measured trunk segments, with a minimum number of segments measured." — [PLAN/CLAUDE.md](PLAN/CLAUDE.md)
- Two pooling shortcuts declared wrong: (1) 1 − ∏(1 − p̄_ij) "always overestimates risk ... With 9 segments and σ² 1.2–1.8: about 0.63–0.69 instead of 0.49"; (2) b = 0 gives the median person, "about 0.45 instead of 0.49". C does not catch shortcut 2, so the person calibration plot is required — [PLAN/experiments/who/pooled_score2/pooling.md](PLAN/experiments/who/pooled_score2/pooling.md)
- A held-out person is a new cluster: the integral is the only valid out-of-fold prediction; empirical-Bayes b would leak outcomes. S_i must sum exactly the outcome-defining, FU-evaluable segments; structurally absent segments leave both S_i and the outcome; missing baseline geometry imputed, not dropped — [pooling.md](PLAN/experiments/who/pooled_score2/pooling.md)
- Technical background (thesis text): cloglog = grouped-data proportional hazards (Prentice & Gloeckler), exp(β) a hazard ratio; exposure (follow-up, length) as offset (γ = 1) or free covariate γ; random intercept = lognormal shared frailty, coefficients conditional — [REPO/thesis/technical_background/06_segment_glmm.tex](REPO/thesis/technical_background/06_segment_glmm.tex)
- Five assumptions carry the GLMM's efficiency gain: segments independent given one b_i; constant σ; normal b; S_i sums exactly the outcome segments; b independent of covariates (Mundlak) — [REPO/reports/Pooled segment GLMM background.md](REPO/reports/Pooled%20segment%20GLMM%20background.md)

### Inferences
- Any competitor must output a **person** risk for the "any trunk plaque" outcome and must handle that a test person's frailty is unknown (marginalise, not condition). A neural network that uses each segment's outcome in training would need an analogous pooling step (e.g. a shared person latent integrated out, or a direct person head) to produce calibrated person risk.
- Because cloglog makes person risk depend on segment hazards only through S_i = Σ exp(η_ij), the pooled GLMM already imposes an additive-on-log-hazard aggregation; a flexible model's possible gain lies in non-linear η (curvature, taper shapes), interactions, or non-additive aggregation across segments.
- The benchmark to beat in the clean cohort does not yet exist as fitted numbers; only progression-cohort code and a person-level base comparison (score2_honesty) exist.

### Gaps
- No fitted results of the pooled model on the clean cohort are in the files (B2 "Not run").
- The progression run's outputs (`progression_who_pooled*.md`) are not present locally; their results are unknown here.
- Whether log follow-up enters as an offset or a free covariate in the final model is undecided ("Still open: follow-up time enters the model as log(years)", REPO/thesis/methodology/02_population_outcome.tex:10).

## 2. Cohort numbers, segments, missingness and the parameter budget

### Takeaway
1,801 participants; 1,077 plaque-free at baseline; 483 (44.8%) developed plaque anywhere, 452 (42.0% of 1,076 with FU reads) in one of the 9 trunk segments; 1,041 complete cases with 433 events (41.6%). The segment-level event count on the new table and the Riley P_max are not yet computed; the plan's working figure is about 15–20 parameters at C = 0.70.

### Cited Findings
- 1,801 participants, all read at BL; 724 (40.2%) with plaque/stenosis at BL excluded; 1,077 (59.8%) plaque-free, all with graded FU; image-quality exclusion "[..]" not yet fixed — [REPO/thesis/results/00_cohort.tex](REPO/thesis/results/00_cohort.tex)
- 483/1,077 (44.8%) developed plaque in ≥1 segment; 452 (93.6% of them) in a trunk segment; 31 (6.4%) only in LM or a side branch (counted as no outcome) — [00_cohort.tex](REPO/thesis/results/00_cohort.tex)
- Per artery among the 1,077: LAD 390 (36.2%), RCA 185 (17.2%), LCx 127 (11.8%) participants — [00_cohort.tex](REPO/thesis/results/00_cohort.tex)
- Severity among the 452: 261 (57.7%) at most minimal, 140 (31.0%) mild, 37 (8.2%) moderate, 14 (3.1%) severe/occlusion — [00_cohort.tex](REPO/thesis/results/00_cohort.tex)
- score2_honesty cohort: 1,077 clean → 1,076 with FU segments read; 452 events (42.0%); 40 people with no trunk plaque but ≥1 unevaluable trunk segment; missing SCORE2 35, SBP 12, total cholesterol 22, HDL 22; complete cases 1,041 with 433 events (41.6%); median SCORE2 risk 0.026 — [REPO/CGPS_data/score2_honesty.md §1–2](REPO/CGPS_data/score2_honesty.md)
- The 9 trunk segments: proximal, mid and distal LAD, LCx and RCA; LM and side branches excluded — [REPO/thesis/methodology/02b_segment_split.tex:17–30](REPO/thesis/methodology/02b_segment_split.tex)
- Segment boundaries are placed at landmarks (side branches), else at a fixed fraction of the artery length; checked by a miss rate of Medis contours vs the visual grade — [02b_segment_split.tex:32–51](REPO/thesis/methodology/02b_segment_split.tex)
- Old-table numbers (not to be quoted until recomputed): 1,352 clean, 668 (49.4%) developed plaque, 626 with trunk plaque, 2,055 incident plaque segments, 61% of trunk plaque segments minimal — [PLAN/CLAUDE.md](PLAN/CLAUDE.md)
- Riley criteria chosen (S ≥ 0.9, optimism in Nagelkerke R² ≤ 0.05, overall risk ±0.05), P_max = n(S−1)ln(1 − R²_CS/S), anticipated C 0.70 (sensitivity 0.65, 0.75), all numbers "[..]"; geometric block = 5 df; base in the table currently "refitted SCORE2 factors [..]" — [REPO/thesis/methodology/03_model_size.tex:24–72](REPO/thesis/methodology/03_model_size.tex)
- "All geometric terms were entered linearly. A spline on every term would have needed [..] degrees of freedom, more than the model supports." — [03_model_size.tex:48–49](REPO/thesis/methodology/03_model_size.tex)
- Plan: "about 15–20 parameters fit at an anticipated C of about 0.70 (Riley criteria). Splines on every term (26–31 df) do not fit. Confirm in pmsampsize" — [PLAN/CLAUDE.md open decision 11](PLAN/CLAUDE.md)
- `who_where_readiness.py` still uses 10/20 events-per-parameter rules (line 51) and must be switched to Riley — [03_model_size.tex:7–8](REPO/thesis/methodology/03_model_size.tex); [REPO/CGPS_data/who_where_readiness.py:51](REPO/CGPS_data/who_where_readiness.py)
- Structural absence: PDA/PLA in non-right-dominant hearts filled "none" although they may not exist; structurally absent rows leave; dominance in both files — [PLAN/CLAUDE.md](PLAN/CLAUDE.md)
- Missing geometry rule (open): MI with the outcome for the test, z = 0 for CV prediction, complete cases as sensitivity — [PLAN/CLAUDE.md open decision 9](PLAN/CLAUDE.md)
- Tracer geometry for ~1,200 plaque-free people "soon"; method to be frozen before outcome linkage — [user memory index, MEMORY.md "Tracer clean cohort coming"]; freeze rules in [PLAN/CLAUDE.md open decision 12](PLAN/CLAUDE.md)

### Inferences
- With ~433–452 person events and 15–20 df total, a parametric base of ~9–13 df (6 SCORE2 factors or 1 log-SCORE2 + follow-up + dominance + 8 segment dummies + log length) leaves roughly 5 df for geometry; this is the constraint any flexible model faces, because the person (not the segment) is the unit of information for "who".
- The segment rows (~9 × 1,041 ≈ 9,400 if all graded) add information mainly about within-person allocation, not about who.

### Gaps
- Number of incident plaque segments in the trunk on the 1,801 table: not in the files.
- Segment-level unevaluable/ungraded counts at FU per segment and number of structurally absent segments: not in the files.
- Riley P_max, image-quality exclusions, final study-cohort n, follow-up time distribution: all "[..]".
- Intraclass correlation / σ̂ on the clean cohort: not estimated.

## 3. Geometry features: segment-level vs person-level; SCORE2 base options

### Takeaway
Five prespecified terms, each 1 df, linear: curvature and taper (per trunk segment) and three left-main bifurcation terms (LM bifurcation angle, LM→LAD and LM→LCx diameter ratios), which are person-level values. The base is open between recalibrated published SCORE2 and the refitted SCORE2 factors; the person-level score2_honesty run favoured recalibrated SCORE2 but is explicitly not the decision.

### Cited Findings
- Table: curvature and taper "each trunk segment, primary"; LM angle, LM→LAD ratio, LM→LCx ratio "left main bifurcation, primary"; secondary: other bifurcations, lumen volume/myocardial mass, curvature × calibre (Dean-type), local expansion, upstream turning, pointwise profiles — [REPO/thesis/methodology/04_feature_selection.tex:43–54](REPO/thesis/methodology/04_feature_selection.tex)
- Selection criteria include "a cost of one degree of freedom, with a coefficient read as the odds ratio per standard deviation"; no univariable screening, no stepwise/penalised selection for the test — [04_feature_selection.tex:62–73](REPO/thesis/methodology/04_feature_selection.tex)
- The two ratios share the LM diameter in the denominator and are correlated; log-scale coding (scaling-law deviation + LAD/LCx asymmetry) is an open question — [04_feature_selection.tex:75–77](REPO/thesis/methodology/04_feature_selection.tex)
- How LM terms enter the pooled model: in the progression code only on pLAD/pCX rows; the plan flags that "LM terms coded only on the proximal rows turn the 'who' test mostly into a 'where' test: about 94% of its information is allocation. Either split them into a main effect plus a proximal contrast, or rename the test." — [PLAN/CLAUDE.md open decision 5](PLAN/CLAUDE.md); derivation 6.2% count vs 93.8% allocation, and simulation 12/12 vs 1/12 rejections — [REPO/reports/Pooled segment GLMM background.md](REPO/reports/Pooled%20segment%20GLMM%20background.md)
- Curvature/taper z-scored within segment type; "The z-score within segment type is an assumption (one OR per within-type SD), not a de-confounding step." — [PLAN/CLAUDE.md open decision 6](PLAN/CLAUDE.md)
- Measurement: unsigned turning angle has a positive noise floor (≈ √6·σ/ℓ²) depending on image quality, thus on BMI and heart rate; resample 0.5 mm, smooth w ≈ 2–3 mm (curvature), ≥ 5 mm (taper); per-scan noise covariate; taper as robust slope of log radius vs arc length, masking side branches — [PLAN/CLAUDE.md "Measurement notes"](PLAN/CLAUDE.md)
- Absent LM / ramus / trifurcation rule undecided; an absent-LM indicator would cost 1 df — [03_model_size.tex:75](REPO/thesis/methodology/03_model_size.tex); [PLAN/CLAUDE.md open decision 5](PLAN/CLAUDE.md)
- Base options: B1/B2 refitted SCORE2 factors; B3 published SCORE2 frozen with a free slope — [PLAN/CLAUDE.md "Who"](PLAN/CLAUDE.md). "Open: Who base: recalibrated SCORE2 ... or the refitted SCORE2 factors. To be compared in the pooled model. The person-level score2_honesty.py run is not the decision." — [REPO/CLAUDE.md](REPO/CLAUDE.md)
- score2_honesty (person-level cloglog, 5-fold × 20 repeats, 200 bootstraps): OOF C follow-up only 0.560; age + sex 0.660; SCORE2 recalibrated 0.687 (cal. slope 0.972, Brier 0.2193, log loss 0.6284); refitted factors (9 params) 0.686 (apparent 0.699, cal. slope 0.866, log loss 0.6346). ΔC refit − recalibrated −0.001 (−0.025 to 0.004) — [REPO/CGPS_data/score2_honesty.md §3, §5](REPO/CGPS_data/score2_honesty.md)
- SCORE2 slope on cloglog scale 0.722 (0.569–0.874); HR per SD: age 1.32, male 1.25, SBP 1.22, log follow-up 1.19, smoking 1.14, total cholesterol 1.09 (0.98–1.20), HDL 0.86, diabetes 1.03 (0.94–1.12) — [score2_honesty.md §4](REPO/CGPS_data/score2_honesty.md)
- Calibration by fifth (SCORE2 recalibrated): top fifth predicted 0.645 vs observed 60.1%; fourth 0.494 vs 57.2% — [score2_honesty.md §6](REPO/CGPS_data/score2_honesty.md)
- Robustness rung: add diabetes, BMI and height; "If the increment collapses there, geometry was measuring body size." Statins at baseline only — [PLAN/CLAUDE.md](PLAN/CLAUDE.md)

### Inferences
- The base already reaches OOF C ≈ 0.69 with 3 parameters; the plan's expected geometry increment is ΔC 0.00–0.02 (ΔAUC ≈ 0.005 at OR 1.2/SD, [PLAN/CLAUDE.md](PLAN/CLAUDE.md)). Any challenger's gain must be judged against that tiny, noisy target; bootstrap intervals on ΔC of ±0.02 (score2_honesty §5) are of the same order as the expected effect.
- The refitted 9-parameter base already shows optimism (cal. slope 0.866) at this n, a warning sign for any more flexible learner.

### Gaps
- No pooled-model comparison of the two bases exists yet.
- Tracer-based taper and LM diameter ratios are not yet computed (the progression code lacks them because Medis contours cover only diseased segments, [who-progression G02 experiment.md](PLAN/experiments/who-progression/pooled_score2/G02_pooled_score2_geommean/experiment.md)).

## 4. What is prespecified, and what "beat" must mean

### Takeaway
Inference is one prespecified likelihood-ratio test of the geometry block (5 df, linear) in the pooled model; ΔC, ΔBrier, Δlog loss and calibration are estimated with paired person-level intervals and never tested; CV is 10 person folds × 50 repeats stratified on the person outcome, with every learned quantity fitted in the training fold. A challenger can therefore only "beat" the GLMM as an estimated, paired, out-of-fold improvement in person-level log loss/Brier/C with acceptable calibration, on the same folds and outcome, as a secondary/exploratory analysis; it cannot replace the confirmatory test.

### Cited Findings
- "One prespecified LR test of the geometry block per question; ΔC and calibration are estimated, never tested." "Cross-validation is split by person." — [REPO/CLAUDE.md](REPO/CLAUDE.md)
- CV: 10 folds stratified on person outcome, 50 repeats with recorded seeds; same fold files for every experiment; z constants, knots, imputation, σ̂² fitted in training fold. "ΔAUC tests are invalid for nested models. No NRI/IDI p-values, no Hosmer–Lemeshow." — [PLAN/CLAUDE.md "Decided"](PLAN/CLAUDE.md)
- Who metrics "All per person, never per segment: C, Brier, calibration slope and intercept. ... C alone can hide a wrongly pooled person risk." Same folds for both engines → paired differences — [PLAN/experiments/who/setup.md](PLAN/experiments/who/setup.md)
- Code implements: LR on full-data fits, `lr = 2 * (fits["G02"]["ll"] - fits["B2"]["ll"])`, df = number of added columns; CV metrics C, Brier, log loss, calibration slope/intercept, paired Δ "an estimate, not a test" — [progression_who_pooled.py:30–36, 496–501](REPO/CGPS_data/progression_who_pooled.py)
- Who-progression variant: "Δ log loss is the primary comparison. Also scaled Brier." CIs by paired person bootstrap with the CV rerun — [PLAN/experiments/who-progression/setup.md](PLAN/experiments/who-progression/setup.md)
- Thesis CV text: k-fold, folds per participant, stratified by incident plaque in any of the nine segments; number of folds/repeats and nested tuning still "\clarify" — [REPO/thesis/methodology/11_cross_validation.tex](REPO/thesis/methodology/11_cross_validation.tex)
- Expected result stated in advance: "Who will probably give a small or null increment: ΔC 0.00–0.02". "A significant LR test with ΔC near zero is a coherent result" — [PLAN/CLAUDE.md](PLAN/CLAUDE.md)
- Flexible terms (splines, curvature × taper, splined LM) are exploratory only (where G02–G04); "The planned transformer is demoted: it must beat the FPCA/functional models on the same folds." — [PLAN/CLAUDE.md](PLAN/CLAUDE.md)
- Earlier NN report: a network fed the same per-segment table "will, at best, tie" regression; its only defensible advantage is structural (tree topology, ordered profile); proposed ablation ladder on identical folds (regression → XGBoost/TabPFN → per-segment MLP → hand-crafted neighbours → GNN → pretrained profile encoder → shuffled controls); attribution by refitting, not SHAP — [REPO/reports/Neural networks for segment plaque.md](REPO/reports/Neural%20networks%20for%20segment%20plaque.md). Note: that report assumed ~2,000 participants, ~15 segments/person and baseline plaque as predictor; outdated for the plaque-free 9-segment design.
- Earlier model-choice report: regression primary, XGBoost a prespecified secondary; LR stable at ~20–50 EPV, random forests needed >200 (van der Ploeg); ML vs LR logit(AUC) difference 0.00 (−0.18 to 0.18) at low risk of bias (Christodoulou) — [REPO/reports/Plaque risk model choice.md](REPO/reports/Plaque%20risk%20model%20choice.md)
- Freeze before outcome linkage: git hash, hashed feature table, smoothing scale, OSF time-stamp — [PLAN/CLAUDE.md open decision 12](PLAN/CLAUDE.md)

### Inferences
- "Beat" should mean: same 1,041-ish complete-case persons (or same imputation), same person outcome (any trunk plaque, minimal included), same base covariates, same 10×50 folds, all tuning nested inside training folds, person-level out-of-fold risk; better paired Δlog loss/ΔBrier (primary) and ΔC with person-bootstrap intervals, calibration slope near 1. Equally, the challenger must be compared against the GLMM *with geometry* (G model), not only against the base, to isolate the value of non-linearity.
- A segment-trained flexible model compared on segment AUC would be invalid here: segment AUC mixes who and where and is not the who metric.
- Given the anticipated ΔC 0.00–0.02 and ~450 events, any flexible model's gain over the linear GLMM is likely within CV noise; a pre-registered secondary status is the only defensible framing.

### Gaps
- Tuning protocol (nested CV) for any flexible model is not specified anywhere.
- Multiplicity rule across who/where (open decision 8) is unresolved, though the where question has been dropped from the .tex for now.

## 5. Clinical background: biological reasons for non-linear or interaction effects

### Takeaway
The thesis's clinical background (v2) argues that low/oscillatory WSS marks plaque-prone sites, located on the inner wall of bends and the lateral walls of bifurcations, growing with bend tightness and flow rate. It does not itself claim U-shapes or interactions; the project reports argue that curvature alone has a mechanistic case for non-monotonicity, taper for saturation, LM angle and ratios for monotone (possibly convex, one-sided) effects, and that curvature and taper superpose (additive on log-WSS), so their product is a secondary test only.

### Cited Findings
- "Plaque forms and grows preferentially where the WSS is low or oscillatory"; high WSS harmful only to existing narrowing plaque — [REPO/thesis/clinical_background_v2/03_wall_shear_stress.tex:57–58](REPO/thesis/clinical_background_v2/03_wall_shear_stress.tex)
- In a bend the fastest blood is carried to the outer wall; low WSS on the inner wall; inner-wall mean WSS about half the outer in a coronary bend model, oscillating more; disturbed flow "grows stronger the tighter the bend and the higher the flow rate" — [03_wall_shear_stress.tex:66–69](REPO/thesis/clinical_background_v2/03_wall_shear_stress.tex)
- At a bifurcation, high WSS on the flow divider, disturbed flow along lateral walls; extent "depends mainly on the share of the parent flow that enters the side branch"; flow divider largely spared — [03_wall_shear_stress.tex:71–75](REPO/thesis/clinical_background_v2/03_wall_shear_stress.tex)
- Dominance changes artery size (proximal RCA 3.9 vs 2.8 mm; LCx 3.4 vs 4.2 mm in right vs left dominance), so statistics are stratified by dominance — [REPO/thesis/clinical_background_v2/01_heart_anatomy.tex](REPO/thesis/clinical_background_v2/01_heart_anatomy.tex)
- WSS is local, motivating per-segment features — [02b_segment_split.tex:28–29](REPO/thesis/methodology/02b_segment_split.tex); [05_features.tex:16](REPO/thesis/methodology/05_features.tex)
- Non-linearity report: no human study has tested the shape of any of the four geometry–plaque relations; published thresholds (LM angle 78–80°) are Youden cut-offs from small samples; curvature has opposing pathways (low inner-wall shear vs protective helical flow) → two-sided spline; taper → saturation; angle/ratios monotone, ratio effect one-sided (low-shear when summed daughter area is high); PROSPECT low-shear pattern step-like; "most likely empirical result is that splines and linear terms give almost the same predictions"; RCS4 × 10-level segment interaction costs 27 df per feature and does not fit — [PLAN/reports/Segment plaque risk model nonlinearity.md](PLAN/reports/Segment%20plaque%20risk%20model%20nonlinearity.md)
- Taper × curvature: idealized simulations show superposition — curvature places low WSS (inner wall), taper scales its level (Q/r³); in a tapered model the global WSS minimum moved from a bend to the straight proximal inlet (Johnston et al. 2009); recommend two linear main effects, product as prespecified secondary test; "No human study has ever fitted a taper × curvature term against plaque" — [REPO/reports/Taper and curvature interaction for WSS.md](REPO/reports/Taper%20and%20curvature%20interaction%20for%20WSS.md)
- Secondary candidates with interaction flavour: curvature × calibre (Dean-type), upstream turning (with downstream as negative control), pointwise profiles — [04_feature_selection.tex:51–54](REPO/thesis/methodology/04_feature_selection.tex)
- Segment-specific geometry effects: plan notes person × position confounding (age × proximal, sex × proximal) — [PLAN/CLAUDE.md open decision 4](PLAN/CLAUDE.md); a report exists on segment-specific weights ([REPO/reports/Segment specific geometry weights.md](REPO/reports/Segment%20specific%20geometry%20weights.md), not read in detail here)

### Inferences
- Plausible flexible-model targets: (a) non-monotone or saturating curvature/taper curves; (b) curvature × flow proxy (calibre, dominance, upstream position), the Dean-type idea; (c) LM-angle effects specific to pLAD/pLCx; (d) dominance-dependent effects in RCA/LCx. All are exploratory per the plan, and the measurement noise floor in curvature will flatten real curvature shapes.
- None of these is supported by human outcome data; the reasoning is mechanistic (CFD, idealized models), so a flexible model's prior expected gain is small.

### Gaps
- The clinical background v2 does not discuss taper, diameter ratios or interactions directly (only bends and bifurcations); the daughter-ratio scaling law sits in methodology/08_daughter_ratio.tex (Huo–Kassab deviation Δ_HK).

## 6. Text–code mismatches noticed

### Takeaway
Several inconsistencies exist between the thesis text, the plan and the only pooled-model code; none of the methods text on the who model is yet backed by code in `CGPS_data/thesis_final/` (which holds only `split_check.py`).

### Cited Findings
- `CGPS_data/thesis_final/` contains only `README.md` and `split_check.py`; no pooled-model script is finalised — [REPO/CGPS_data/thesis_final/README.md](REPO/CGPS_data/thesis_final/README.md)
- Code vs design: `progression_who_pooled.py` uses Medis trees, progression outcome and BL grade covariate, curvature (mean T5) + LM angle only, no taper or LM ratios; the decided who model uses plaque-free cohort, incident coronary plaque, 5 geometry terms — [progression_who_pooled.py:7–18](REPO/CGPS_data/progression_who_pooled.py) vs [04_feature_selection.tex:70](REPO/thesis/methodology/04_feature_selection.tex)
- Segment-level vs person-mean geometry: plan says curvature/taper enter who as person means of within-type z; code enters them per segment row — [PLAN/CLAUDE.md](PLAN/CLAUDE.md) vs [progression_who_pooled.py:122–125](REPO/CGPS_data/progression_who_pooled.py); thesis 05_features.tex says segment values enter the one model over nine segments — [05_features.tex:16–18](REPO/thesis/methodology/05_features.tex)
- Feature count: 05_features.tex says "Four geometric features" (curvature, bifurcation angle "for each bifurcation", daughter ratio Δ_HK "for each bifurcation", lumen volume/myocardial mass) and omits taper; 04_feature_selection.tex says five primary terms (curvature, taper, LM angle, two LM ratios) with V/M secondary — [05_features.tex:8–35](REPO/thesis/methodology/05_features.tex) vs [04_feature_selection.tex:43–70](REPO/thesis/methodology/04_feature_selection.tex). 08_daughter_ratio.tex defines a single Δ_HK deviation, not two LM→LAD / LM→LCx ratios — [08_daughter_ratio.tex](REPO/thesis/methodology/08_daughter_ratio.tex)
- Coefficient reading: 04_feature_selection.tex criterion 5 says "odds ratio per standard deviation", but the cloglog model gives hazard ratios — [04_feature_selection.tex:68](REPO/thesis/methodology/04_feature_selection.tex) vs [06_segment_glmm.tex](REPO/thesis/technical_background/06_segment_glmm.tex)
- Base in budget table: 03_model_size.tex lists "Base terms: refitted SCORE2 factors", while the base is formally open and score2_honesty's rule picked "SCORE2 recalibrated" — [03_model_size.tex:65](REPO/thesis/methodology/03_model_size.tex); [REPO/CLAUDE.md](REPO/CLAUDE.md); [score2_honesty.md §5](REPO/CGPS_data/score2_honesty.md)
- Cohort definition: 02_population_outcome.tex defines plaque-free by SIS = 0 only; project rule is SIS = 0 and SSS = 0 — [02_population_outcome.tex:17](REPO/thesis/methodology/02_population_outcome.tex) vs [REPO/CGPS_data/CLAUDE.md](REPO/CGPS_data/CLAUDE.md)
- 03_model_size.tex says the budget for the "binary outcome" uses participants and events, consistent with person-level Riley, but the model is a segment-level GLMM; how segment rows count is not stated — [03_model_size.tex](REPO/thesis/methodology/03_model_size.tex)
- CV settings differ by script: plan 10 folds × 50 repeats; score2_honesty 5 folds × 20 repeats; who-progression t25 10 folds × 20 repeats; thesis text unspecified — [PLAN/CLAUDE.md](PLAN/CLAUDE.md); [score2_honesty.md §3](REPO/CGPS_data/score2_honesty.md); [PLAN/experiments/who-progression/setup.md](PLAN/experiments/who-progression/setup.md); [11_cross_validation.tex](REPO/thesis/methodology/11_cross_validation.tex)
- 02_population_outcome.tex mentions a sensitivity analysis restricted to mild or worse; the methodology chapter intro mentions a section `02_models` "NOT WRITTEN" — [02_population_outcome.tex:20](REPO/thesis/methodology/02_population_outcome.tex); [00_chapter_intro.tex:7](REPO/thesis/methodology/00_chapter_intro.tex)
- Known code issues with the first pooled script are documented in `PLAN/reports/Pooled who progression code issues.md` (not read here); the t25 script replaces it — [who-progression/setup.md](PLAN/experiments/who-progression/setup.md)

### Inferences
- Before any challenger is compared, the benchmark itself needs a clean-cohort implementation with the 5-term block, a decided coding of LM terms (main effect + proximal contrast), a decided base, and the offset/covariate choice for follow-up.

### Gaps
- Contents of `PLAN/reports/Pooled who progression code issues.md` and `reports/Segment specific geometry weights.md` were not reviewed in detail.
