# Fair evaluation of flexible models (NN, GAMM, boosting) against the prespecified pooled segment cloglog GLMM

Scope: CGPS (Herlev–Østerbro) serial CCTA, about 1,000–1,200 plaque-free people at baseline, a few hundred who developed plaque, 9 trunk segments per person, segment risks pooled to a person risk 1 − ∏(1 − p_s). Prespecified: one LR test of the geometry block; ΔC and calibration are estimated, never tested; CV split by person. Background read: `thesis/methodology/03_model_size.tex` (Riley criteria, S = 0.9, anticipated C = 0.70, geometry block of 5 linear df, explicitly "a spline on every term would need more df than the model supports"), `thesis/methodology/11_cross_validation.tex` (person-level folds stratified by any-event; number of folds/repeats and nested tuning still a red `\clarify`), and `reports/Plaque risk model choice.md` (regression primary; XGBoost as secondary check for missed nonlinearity/interaction; neural curvature encoder only exploratory, with shuffled-profile control).

Search budget note: about 17 tool calls; some citations below (Riley 2020 BMJ, Harrell RMS, Vickers & Elkin 2006, DeLong 1988) are standard references whose details I know but did not re-open in this session; they are marked "(not re-checked this session)".

## 1. Sample size for flexible models, and the effective sample size with clustered segments

### Takeaway
The person, not the segment, is the unit of information for any person-level risk claim, and with a few hundred events the cohort is at or below the size where even unpenalised logistic regression stabilises; tree ensembles and neural nets need several-fold more events per candidate parameter. No accepted closed-form sample size exists for ML models; the defensible substitute is to report instability (bootstrap MAPE, instability plots) for every model compared.

### Cited Findings
- van der Ploeg, Austin & Steyerberg (2014), "Modern modelling techniques are data hungry: a simulation study for predicting dichotomous endpoints", BMC Med Res Methodol 14:137. Compared SVM, neural nets, random forests vs logistic regression and CART. Logistic regression reached stable AUC/low optimism at roughly 20–50 events per variable (EPV); RF, SVM and NN still showed instability and high optimism above 200 EPV; conclusion that modern methods may need over 10 times the EPV of LR and should be used mainly with very large datasets — [PMC4289553](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289553). Data hungriness was defined as the minimum EPV at which c-statistic optimism < 0.01 — [Austin et al. 2024, PMC11539735](https://pmc.ncbi.nlm.nih.gov/articles/PMC11539735). (Exact numbers from abstract/secondary summary; full tables not re-read.)
- Austin, Lee & Wang (2024), "The relative data hungriness of unpenalized and penalized logistic regression and ensemble-based machine learning methods: the case of calibration", Diagn Progn Res 8:15. Monte Carlo on EFFECT AMI/HF cohorts, EPV 10–200. Penalised LR had very low calibration optimism even at low EPV; unpenalised LR optimism plateaued around 50 EPV (little change beyond ~40 EPV); bagged trees and random forests were most data hungry; boosted trees in between (more optimism than LR at small/moderate n). Authors recommend considering penalised LR — [PMC11539735](https://pmc.ncbi.nlm.nih.gov/articles/PMC11539735).
- Riley et al. (2019), Stat Med, "Minimum sample size for developing a multivariable prediction model: Part II – binary and time-to-event outcomes": criteria (i) expected shrinkage ≥ 0.9, (ii) optimism in Nagelkerke R² ≤ 0.05, (iii) overall risk within ±0.05 — [PMC6519266](https://pmc.ncbi.nlm.nih.gov/articles/PMC6519266); implemented in R `pmsampsize` (CRAN version 1.1.3, 2023-12-05) — [CRAN refman](https://cran.r-project.org/web/packages/pmsampsize/refman/pmsampsize.html). The BMJ tutorial is Riley et al., BMJ 2020;368:m441 — [Utrecht repository record](https://dspace.library.uu.nl/handle/1874/457642).
- Riley, Pate, Dhiman, Archer, Martin, Collins (2023), "Clinical prediction models and the multiverse of madness", BMC Med 21:502. GUSTO-I example: n = 40,830 (2,851 deaths, ~356 events per parameter) gave mean MAPE 0.0028 (max 0.027); n = 500 (35 deaths, ~4 events per parameter) gave mean MAPE 0.023 (max 0.14), and one person with predicted risk 0.2 ranged ~0 to 0.8 across bootstrap models, while the c-statistic stayed 0.82 (bootstrap 95% range 0.77–0.82). Instability "is not specific to AI or ML"; penalised regression can be very unstable; instability increases with tuning and data splitting; "Ultimately, all methods are limited by the available sample size for model development"; suggests MAPE below about 0.02 as a target; no separate ML sample-size rule given — [PMC10729337](https://pmc.ncbi.nlm.nih.gov/articles/PMC10729337/).
- A Fisher-information-based sample size for model *stability* (binary outcomes), software `pmstabilityss`, exists as an arXiv preprint first posted 12 July 2024 (**preprint**, peer-review status not verified) — [arXiv 2407.09293](https://arxiv.org/abs/2407.09293v2); a time-to-event companion appeared in Diagn Progn Res (Dec 2025) — [DOAJ record](https://doaj.org/article/76a4fa3eb74345bc919b2bd79e3e1d27).
- Clustered segment outcomes: Obuchowski (1997, Biometrics) extended DeLong's structural components to clustered ROC data using design-effect and effective-sample-size ideas from survey sampling, without specifying the within-cluster correlation — [clusteredROC help, Cleveland Clinic](https://www.lerner.ccf.org/quantitative-health/documents/clusteredROC_help.pdf); [metricgate summary](https://metricgate.com/calculator/obuchowski-clustered-roc).

### Inferences
- Design effect for the 9 segment outcomes per person: DE = 1 + (m − 1)·ICC with m = 9. At latent ICC 0.1 / 0.3 / 0.5, DE ≈ 1.8 / 3.4 / 5.0, so ~10,000 segments carry the information of roughly 5,600 / 2,900 / 2,000 independent segments. This matters only for segment-varying (within-person) terms. For person-level predictors (SCORE2 factors) and for the person-level risk claim, the effective n is the number of persons and the event count is the number of persons who developed plaque. (Formula is standard survey-sampling arithmetic; ICC for incident plaque is not published — estimate it from the GLMM random-intercept variance on the latent scale, σ²/(σ² + π²/6) for cloglog.)
- With, say, 300 person-events and a model of ~12–15 df (SCORE2 factors + 5 geometry terms), the GLMM sits at ~20–25 events per df — inside the zone where unpenalised LR is still somewhat optimistic per van der Ploeg/Austin. By the same simulations, RF/NN would need several thousand events to be stable. Gradient boosting and penalised GAMs are the only flexible options with a plausible chance of not being dominated by variance here.
- A neural network operating on raw curvature profiles has far more effective parameters than 300 events can support; any apparent gain must be shown to survive the multiverse/instability check, otherwise it should be reported as uninformative rather than negative.

### Gaps
- No published ICC for incident coronary plaque across segments within a person (also noted in `reports/Plaque risk model choice.md`).
- No accepted closed-form minimum sample size for NN/boosting; the `pmstabilityss` approach is for regression-type models and is partly preprint.
- I could not open Riley et al. 2024/2025 papers specifically on ML sample size beyond the stability preprint; I found no "Riley 2025 ML sample size" paper in this session.

## 2. Systematic evidence on ML vs logistic regression, overall and in cardiovascular risk

### Takeaway
When comparisons are done with low risk of bias, ML has not beaten logistic regression on discrimination; apparent ML gains concentrate in high-risk-of-bias studies and very large EHR datasets, and calibration is rarely reported. The realistic prior for this cohort is ΔC ≈ 0 for a flexible model over the GLMM.

### Cited Findings
- Christodoulou, Ma, Collins, Steyerberg, Verbakel, Van Calster (2019), "A systematic review shows no performance benefit of machine learning over logistic regression for clinical prediction models", J Clin Epidemiol 110:12–22. 71 studies, 282 LR–ML comparisons. Low risk of bias (145 comparisons): difference in logit(AUC) 0.00 (95% CI −0.18 to 0.18). High risk of bias (137): ML 0.34 (0.20–0.47) higher. Validation bias in 68% of studies; calibration not addressed in 79% — [Oxford ORA](https://ora.ox.ac.uk/objects/uuid:4167c905-5171-4fc7-b157-ff36d56a73db); [PDF](https://med.mahidol.ac.th/ceb/sites/default/files/public/pdf/Repository/1-s2.0-S0895435618310813-main.pdf).
- Liu, Krentz, Lu, Curcin (2024/2025), "Machine learning based prediction models for cardiovascular disease risk using electronic health records data: systematic review and meta-analysis", Eur Heart J Digit Health 6(1):7–22. 20–21 studies (abstract and results disagree), primary prevention, EHR. Pooled AUC: ML 0.815 (0.787–0.842), random forest 0.865, deep learning 0.847 (0.766–0.927), conventional risk scores 0.765 (0.734–0.796). 34.5% of ML models high risk of bias (mainly analysis domain); I² ≈ 99%; Egger test suggested publication bias; authors: "the real-world effectiveness of ML models remains questionable" — [PMC11750195](https://pmc.ncbi.nlm.nih.gov/articles/PMC11750195/).
- Caveat on the CVD meta-analysis: the comparator is mostly *published, unrefitted* risk scores on very large EHR datasets, not a refitted regression with the same predictors in the same data; this is the comparison Christodoulou showed inflates ML gains. (Inference from the two sources above.)

### Inferences
- The relevant comparison in the thesis is the Christodoulou low-bias type: same data, same predictors, same folds, refitted regression. The expected difference there is zero with wide uncertainty.
- The geometry block is 5 low-noise summary features plus ~6–10 SCORE2 factors; nonlinearity/interactions in such low-dimensional tabular inputs are the scenario where boosting has least to add.

### Gaps
- I found no meta-analysis specific to imaging-geometry or coronary-plaque prediction comparing ML with regression.
- I did not verify any 2022–2025 *update* of Christodoulou by the same group; a 2023 EHJ-QCC primary-prevention meta-analysis (16 studies, 3.3 million people) surfaced only as a snippet without pooled results.

## 3. Nested, person-grouped cross-validation; tuning without leakage; bootstrap vs CV; same-fold comparison

### Takeaway
Use repeated, person-grouped, event-stratified outer CV identical for all models; tune flexible models only in an inner person-grouped CV within each outer training fold; compare models on the same outer folds with person-level paired differences. Harrell's bootstrap optimism correction is the most efficient internal validation for the prespecified GLMM, but it requires re-running the whole pipeline (including tuning) in each bootstrap, which is costly for ML; repeated nested CV is the fairer common ground for the head-to-head.

### Cited Findings
- Varma & Simon (2006), "Bias in error estimation when using cross-validation for model selection", BMC Bioinformatics 7:91: using the same CV for tuning and error estimation is optimistically biased; nested CV (inner loop for selection, outer for estimation) gives a nearly unbiased estimate — [PMC1397873](https://pmc.ncbi.nlm.nih.gov/articles/PMC1397873).
- Wainer & Cawley (2021), "Nested cross-validation when selecting classifiers is overzealous for most practical applications", Expert Syst Appl 182:115222 — found only as a reference entry; content not verified — [arXiv 1811.12808 reference list context](https://arxiv.org/pdf/1811.12808).
- Steyerberg et al. (2001), "Internal validation of predictive models: efficiency of some procedures for logistic regression analysis", J Clin Epidemiol 54(8):774–781: split-sample overly pessimistic and variable; 10-fold CV low bias and variability but not suited to all measures; bootstrap best (stable, low bias) — [ResearchGate PDF](https://www.researchgate.net/profile/Ewout_Steyerberg/publication/10702563_Internal_and_external_validation_of_predictive_models_A_simulation_study_of_bias_and_precision_in_small_samples/links/54abcc8a0cf2ce2df6691007.pdf); [Erasmus repository](https://repub.eur.nl/pub/74159). Omitting predictor selection from the bootstrap underestimates optimism severely (from a related Steyerberg simulation; attribution not verified to the 2001 paper).
- Riley et al. (2023): instability "increases with data splitting into training and test sets" and depends heavily on tuning — [PMC10729337](https://pmc.ncbi.nlm.nih.gov/articles/PMC10729337/).
- `pminternal` R package implements bootstrap optimism (Harrell), .632, .632+ and CV for internal validation of arbitrary user-supplied fitting functions — [CRAN manual](https://archive.linux.duke.edu/cran/web/packages/pminternal/refman/pminternal.html).
- Collins, Dhiman, Ma, ..., Riley (2024), "Evaluation of clinical prediction models (part 1): from development to external validation", BMJ 384:e074819 — covers internal, internal-external and external validation; parts 2 (design and performance measures) and 3 (sample size for external validation) follow — [PMC10772854](https://pmc.ncbi.nlm.nih.gov/articles/PMC10772854/).

### Inferences (proposed protocol)
1. Outer loop: person-grouped, stratified by any-event, K = 5 folds × R = 10–20 repeats (fill the `\clarify` in `11_cross_validation.tex`). Generate the fold assignment once, store seeds, and reuse it for every model (GLMM, spline-GLMM, GAMM, boosting, NN).
2. Everything data-driven goes inside the training fold: standardisation, imputation, spline knot placement, recalibration coefficient of SCORE2, hyperparameter search, early stopping. Inner loop: person-grouped 5-fold CV on the outer training data only. Fix a small hyperparameter grid in advance (number written in the analysis plan) to limit the forking paths.
3. Out-of-fold predictions: for each outer fold, predict segment p_s for held-out persons and pool to person risk 1 − ∏(1 − p_s). For the GLMM, held-out persons are new clusters, so predict with random effect = 0 (or, for cloglog, integrate over the random-intercept distribution to get marginal risk; state which). Mixing conditional and marginal predictions between models would be unfair — fix this before comparison.
4. Comparison statistic: per repeat, compute pooled out-of-fold metrics on all persons (not mean of per-fold AUCs, which is unstable with ~60 events per fold); report mean over repeats. Uncertainty for Δ: CV estimates do not have a simple valid SE; use a person-level bootstrap of the whole pipeline (expensive) or report repeat-to-repeat spread plus a person-cluster bootstrap of the out-of-fold predictions as an approximate (and acknowledged anticonservative, because it ignores refitting variability) interval.
5. For the GLMM alone (primary), Harrell bootstrap optimism correction (≥ 200 bootstraps) is a valid alternative and gives the optimism-corrected calibration slope directly; report it alongside CV for transparency.

### Gaps
- No source found giving a valid closed-form CI for a CV-based ΔAUC; Bates, Hastie & Tibshirani (2023, JASA, "Cross-validation: what does it estimate and how well does it do it?") proposes nested CV for CI but I did not open it this session.
- Wainer & Cawley's conclusions not verified.

## 4. Person-level metrics, ΔC intervals, calibration, Brier, log-loss, net benefit, NRI; segment-level AUC

### Takeaway
Primary comparison metrics should be proper scoring rules (log-loss, which mirrors the GLMM likelihood, and Brier/scaled Brier) plus ΔC with a CI and calibration slope/intercept/curve; net benefit only if a decision threshold is meaningful. Do not test ΔAUC with DeLong for nested models and do not use NRI. Segment-level discrimination needs a cluster-aware AUC (Obuchowski or person-cluster bootstrap), and a within-person C is the relevant segment quantity.

### Cited Findings
- Testing AUC improvement for nested models is invalid/underpowered; the LR or Wald test of the added block is the valid test and the AUC gain should be estimated, not tested: Pepe, Kerr, Longton & Wang (2013, Stat Med) — [PMC3625503](https://pmc.ncbi.nlm.nih.gov/articles/PMC3625503); Demler, Pencina & D'Agostino (2012), "Misuse of DeLong test to compare AUCs for nested models", Stat Med 31(23):2577–87 (snippet); dissent on how harmful the misuse is in BMC Med Res Methodol 2013;13:98 — [BMC](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-98); further evidence [PMC3617074](https://pmc.ncbi.nlm.nih.gov/articles/PMC3617074). This matches the thesis rule "one LR test, ΔC estimated, never tested".
- NRI: Kerr et al. recommend against NRI with ≥ 3 categories; the category-free NRI can overstate incremental value even in independent validation data; net benefit improvement preferred — [UW working paper](https://biostats.bepress.com/uwbiostat/paper394/); Pepe et al. (Stat Biosci 2015): NRI can be positive with an uninformative marker when models fit poorly — [bepress paper393](https://biostats.bepress.com/uwbiostat/paper393); Pepe, Janes, Kerr et al. (JNCI 2014): NRI tests had false-positive rates of 63.0% in training and 18.8–34.4% in test data for null markers; NRI p-values should not be reported — [EDRN record](https://edrn.cancer.gov/data-and-resources/publications/24681599-2296-net-risk-reclassification-p-values-valid-or-misleading).
- Calibration: Van Calster et al. (2019), "Calibration: the Achilles heel of predictive analytics", BMC Med 17:230 — a poorly calibrated model can be less useful than a better-calibrated one with lower AUC; hierarchy of mean, weak (intercept, slope), moderate (curve) and strong calibration — [PMC6912996](https://pmc.ncbi.nlm.nih.gov/articles/PMC6912996). Moderate calibration guarantees non-harmful decisions in decision-curve terms (Van Calster, Nieboer, Steyerberg, SMDM 2015 abstract) — [SMDM abstract](https://smdm.confex.com/smdm/2015mo/webprogram/Paper9076.html).
- Net benefit weights false positives by the threshold odds — Van Calster & Vickers (2015, Med Decis Making), via [MSKCC record](https://synapse.mskcc.org/synapse/works/68428). Original decision curve paper: Vickers & Elkin (2006), Med Decis Making 26(6):565–574 (not re-checked this session).
- Riley et al. (2023): c-statistic can be stable while individual risks are unstable; report MAPE, prediction, classification and calibration instability plots next to C and calibration — [PMC10729337](https://pmc.ncbi.nlm.nih.gov/articles/PMC10729337/).
- Clustered AUC: Obuchowski (1997) nonparametric clustered AUC and its difference; Wu (2020) shows it is inefficient at moderate ICC and large clusters and proposes weighted versions; cluster bootstrap is an alternative — [clusteredROC help](https://www.lerner.ccf.org/quantitative-health/documents/clusteredROC_help.pdf); [IDEAS, Wu 2020](https://ideas.repec.org/a/taf/lstaxx/v49y2020i6p1446-1461.html).

### Inferences (metric set)
- Person level (primary for "who"): out-of-fold log-loss (Δ log-loss is the CV analogue of the LR statistic and is the most natural "beats" criterion for a likelihood-based primary model), Brier and scaled Brier, C with ΔC and percentile CI from person bootstrap, calibration-in-the-large, calibration slope, smoothed calibration curve (loess or restricted-cubic-spline), integrated calibration index. Net benefit only over a prespecified threshold range, and only if a clinically meaningful action exists for "will develop plaque" — likely not, so decision curves are optional/descriptive.
- Rough precision expectation (Hanley–McNeil-type arithmetic, inference): with ~300 events and ~800 non-events at C ≈ 0.70, SE(C) ≈ 0.016; ΔC between two correlated models has a smaller SE, perhaps 0.005–0.015 depending on correlation. Gains below ~0.01–0.02 will therefore be indistinguishable from zero. A pre-registered "minimal meaningful ΔC" (e.g. 0.02) and Δ log-loss margin help avoid over-reading noise.
- Segment level: report (a) overall segment AUC with person-cluster bootstrap CI (Obuchowski-type), (b) within-person C (concordance among segment pairs from the same person with discordant outcome), which removes person-level risk and isolates the "where" component, and (c) segment calibration by segment position. The pooled person risk is only as good as the segment calibration plus the independence-given-random-effect assumption; check person-level calibration separately.

### Gaps
- No source found specifically on calibration of a pooled 1 − ∏(1 − p_s) person risk from a segment GLMM (conditional vs marginal prediction for new clusters); this is an analysis-design decision to document.
- Did not retrieve the full text of BMJ "Evaluation of clinical prediction models" parts 2 and 3.

## 5. Framing the alternative model relative to the prespecified LR test; TRIPOD+AI; forking paths

### Takeaway
The flexible model cannot replace or re-run the primary hypothesis test. Frame it as a prespecified secondary (or explicitly exploratory) robustness analysis with a fixed model list, grid, metrics and decision rule written before outcomes are linked; report under TRIPOD+AI 2024 including internal validation method, tuning, calibration and instability.

### Cited Findings
- TRIPOD+AI: Collins et al., BMJ 2024;385:e078378 (16 April 2024), 27-item checklist plus 13-item abstract checklist; supersedes TRIPOD 2015 and covers both regression and ML models — [PMC11025451](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11025451/). Riley et al. (2023) anticipated TRIPOD+AI asking for instability assessment — [PMC10729337](https://pmc.ncbi.nlm.nih.gov/articles/PMC10729337/).
- Pepe et al. (2013): once the block is shown associated (LR test), testing improvement in performance is redundant; estimate the gain — [PMC3625503](https://pmc.ncbi.nlm.nih.gov/articles/PMC3625503).
- Christodoulou et al. (2019): ML advantage appeared only in high-risk-of-bias comparisons, mostly from validation issues — [ORA](https://ora.ox.ac.uk/objects/uuid:4167c905-5171-4fc7-b157-ff36d56a73db).

### Inferences (framing text)
- Primary (confirmatory): the LR test of the geometry block in the pooled cloglog GLMM. Everything else is estimation.
- Secondary (prespecified, estimation only): (a) spline-GLMM (see section 6); (b) one gradient-boosting model with the same inputs and a fixed small grid; possibly (c) a penalised GAMM. Report Δlog-loss, ΔC, calibration, instability vs the GLMM. Decision rule: "the flexible model is said to add if Δlog-loss and ΔC both favour it in > X% of repeats and the bootstrap interval excludes 0; otherwise the linear GLMM is retained." Never phrase it as a test that could overturn the primary result.
- Exploratory: the NN on curvature profiles, with shuffled-profile and summary-feature controls (as in `reports/Plaque risk model choice.md`); labelled hypothesis-generating.
- Forking paths: freeze the model list, feature set, grids, fold seeds and metrics before linking geometry to outcome (consistent with the tracer-freeze memory note); report every model run, not the best. The Who base (recalibrated vs refitted SCORE2) must be fixed first and be the same base for all compared models.

### Gaps
- No item-by-item check of TRIPOD+AI against this protocol was done in this session.
- "Garden of forking paths" (Gelman & Loken 2013/2014) not re-checked this session.

## 6. Testing whether non-linearity is needed at all (cheaper than a NN)

### Takeaway
The cheapest and most defensible check is a prespecified chunk LR test of nonlinear (restricted cubic spline) terms and/or selected interactions inside the same GLMM; a flexible model is only worth reporting if this test, or a boosting check, suggests missed structure. But the df budget in `03_model_size.tex` already says splines on all terms do not fit, so the spline test must be restricted.

### Cited Findings
- `03_model_size.tex` (thesis): df counting (spline with k knots = k − 1 df); "all geometric terms were entered linearly"; "a spline on every term would have needed [..] df, more than the model supports" — local file.
- Harrell, *Regression Modeling Strategies*, 2nd ed. (Springer 2015): recommends prespecifying restricted cubic splines by expected predictor importance and testing nonlinearity as a pooled chunk test; warns that removing nonlinear terms after a non-significant test and refitting gives anticonservative inference (not re-checked this session) — [Springer book page](https://link.springer.com/book/10.1007/978-3-319-19425-7).
- Austin et al. (2024): boosting is the least data-hungry tree ensemble but still more optimistic than LR at small/moderate EPV — [PMC11539735](https://pmc.ncbi.nlm.nih.gov/articles/PMC11539735).

### Inferences
- Concrete step: as a secondary model, add 3-knot RCS (1 extra df each) to the 5 geometry terms = 5 extra df, and do one chunk LR test (5 df) of "all nonlinearity". This uses the same likelihood, the same random effect, and costs far fewer df than any NN; with S = 0.9 it may exceed the budget, so it is a sensitivity analysis whose result is estimated (Δlog-loss, ΔC) in addition to tested.
- Keep the primary model linear regardless of the result (no data-driven switching), to keep the primary LR test valid.
- A GAMM (penalised splines with person random effect, e.g. mgcv `bam` with cloglog link) is the natural "flexible" model closest to the GLMM: smoothing penalties chosen by REML act as within-model tuning and avoid the inner CV loop.
- Boosting can act as a diagnostic for interactions: if a tuned boosting model with the same inputs does not beat the linear GLMM out-of-fold, that is evidence (not proof) that missed nonlinearity/interactions are small at this n.

### Gaps
- No source found on power of spline chunk tests at ~300 events; would need simulation.

## 7. Stability / instability plots

### Takeaway
For each compared model, run the whole pipeline in ≥ 200 bootstrap samples (persons resampled, all 9 segments together), and report prediction instability plots, MAPE, and calibration instability plots. In small samples, the GLMM is likely to have lower MAPE than any flexible model; a flexible model with comparable C but higher MAPE should not be said to "beat" it.

### Cited Findings
- Riley & Collins (2023), "Stability of clinical prediction models developed using statistical or machine learning methods", Biometrical Journal 65:2200302 (arXiv 2211.01061): instability should always be examined at development; bootstrap the full model-building procedure (e.g. 1,000 samples); prediction instability plot, MAPE, calibration, classification and decision-curve instability — [PMC10952221](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10952221/); [arXiv](https://arxiv.org/abs/2211.01061v1).
- Procedure (BMC Med 2023): predict with the original model; draw bootstrap sample of size n; rebuild with the same development process (including tuning and selection); predict for all original participants; repeat B ≥ 200; MAPE per individual; plot bootstrap vs original predictions with 2.5/97.5 percentiles; check MAPE in subgroups — [PMC10729337](https://pmc.ncbi.nlm.nih.gov/articles/PMC10729337/).
- Ensembles reduce but do not remove instability; penalised regression can be very unstable — [PMC10729337](https://pmc.ncbi.nlm.nih.gov/articles/PMC10729337/).

### Inferences
- Bootstrap must resample persons (cluster bootstrap), never segments, to respect the 9-segment clustering.
- Computational cost: bootstrap × inner-CV tuning for boosting/NN is heavy; a fixed, small grid (or fixed hyperparameters chosen in the first inner loop and then frozen, stated as a limitation) makes it feasible.
- Report MAPE for the GLMM too; if GLMM MAPE is already > 0.02, that is a finding about the cohort size, not about the model class.

### Gaps
- No published MAPE values for GLMMs with clustered outcomes; the method is described for single-level models.

## Summary of realistic expectations (inference from all sections)
- The most likely outcome is that no flexible model beats the linear pooled GLMM on out-of-fold log-loss or C by more than the noise (~0.01–0.02 in C), and that flexible models are less stable and less calibrated.
- "Beats" should require (1) better out-of-fold log-loss and C on the same repeated person-grouped folds, (2) calibration at least as good, (3) MAPE not worse, all prespecified; it should never be decided on C alone and never by a significance test of ΔC.
