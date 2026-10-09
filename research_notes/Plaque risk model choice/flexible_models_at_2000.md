# Flexible models (XGBoost, late-fusion NN) vs regression at ~2000 participants x ~32,000 segments

Scope note: this file revisits the earlier conclusion (regression primary, XGBoost shallow sensitivity,
NN only as frozen pretrained encoder), which was reached at an assumed n of a few hundred. Sibling
files in this folder (`xgboost_vs_regression.md`, `late_fusion_networks.md`,
`regression_methodology.md`) already cover Grinsztajn 2022, Christodoulou 2019, Shwartz-Ziv, Riley
sample size (pmsampsize), Han 2020 (PARADIGM ML) and the EuroIntervention IVUS deep-learning model;
they are referenced but not re-derived here. Research budget was limited (about 16 tool calls); several
full texts returned 403, so some items below rest on abstracts or search-snippet summaries and are
flagged as such.

## 1. Effective sample size with clustered segment data: does segment count or participant count govern overfitting?

### Takeaway
Participant count (and participant-level events) governs both the evaluation and, largely, the
overfitting risk. Segments from the same person share risk factors, scan, reader and interval, so
32,000 segments carry far less than 32,000 independent observations; any validation must split by
participant. At ~2000 participants, regression is comfortably powered; XGBoost on ~20 summary
features moves from "clearly underpowered" to "borderline"; end-to-end deep learning remains short of
the data-hungriness thresholds reported for flexible learners.

### Cited Findings
- Saeb et al. (GigaScience 2017) argued that when there are multiple records per individual and few
  individuals, record-wise CV leaks subject identity into the test fold and overstates accuracy;
  subject-wise (leave-subject-out) CV approximates the clinical use case. The published
  "Perspectives on Saeb et al." (Little, Varoquaux, Saeb, Lonini, Jayaraman, Mohr, Kording, 2017)
  records the debate: record-wise CV is only appropriate when the deployment target is new records
  from already-seen subjects. — [Little et al., GigaScience 2017, PMC5441396](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5441396/)
- van der Ploeg, Austin, Steyerberg (BMC Med Res Methodol 2014), simulation on three clinical cohorts
  (HNSCC 1,282 subjects, 46.9% events; TBI 1,731, 22.3%; CHIP 3,181, 7.6%): a stable validated AUC
  was reached by logistic regression at about 20 to 50 events per variable (EPV), CART about 62, SVM
  and NN above 100, random forest above 200 and was "unstable even above this". Optimism < 0.01 needed
  55 to 127 EPV for LR; for SVM, NN and RF many scenarios never reached it even at > 200 EPV. Modern
  techniques needed "over 10 times as many events per variable". — [van der Ploeg et al. 2014, PMC4289553](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289553)
- Riley and Collins (BMC Med 2023), GUSTO-I (40,830 participants, 2,851 deaths, 7 predictors, C 0.8):
  mean absolute prediction error (MAPE, bootstrap instability of individual risks) was 0.0027 for
  unpenalised LR at n = 40,830 and 0.03 at n = 300 (21 deaths). At the pmsampsize minimum of 752
  participants (53 events): LASSO with 7 predictors MAPE 0.019; LASSO with 27 candidates 0.029 (vs
  0.038 forcing all in); random forest with default hyperparameters 0.047; random forest restricted
  to depth 3 0.019. Even at n = 752, individuals with estimated risk 0.4 had 95% bootstrap ranges of
  roughly 0.2 to 0.6. Data-driven tuning of RF hyperparameters added instability compared with
  prespecified settings. — [Riley & Collins, Stability of clinical prediction models, BMC Med 2023, PMC10952221](https://pmc.ncbi.nlm.nih.gov/articles/PMC10952221/)
- Riley and Collins also frame this as a "multiverse of madness": small development data produce many
  plausible models with very different individual predictions; instability plots from bootstrapping
  are recommended to expose it. — [Riley & Collins, BMJ 2023, PMC10729337](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10729337/)

### Inferences
- Participant-level arithmetic (illustrative; the true event rate in Herlev–Østerbro is unknown here):
  with 2000 participants and a participant-level "any new/progressing plaque" rate of 20 to 40%,
  there are about 400 to 800 events. With 15 to 25 candidate parameters, that is about 16 to 53 EPV:
  inside the van der Ploeg "LR stable" band, but 4 to 10 times below the > 200 EPV at which RF (the
  closest analogue to XGBoost in that study) stabilised. The earlier "few hundred" scenario sat at
  1 to 10 EPV, so the move to 2000 is a real change for regression (now robust, splines and a few
  interactions affordable) and a partial change for trees (shallow boosting becomes defensible as a
  co-primary sensitivity, not a replacement).
- Segment-level arithmetic: the design effect for clustered binary data is about 1 + (m - 1) x ICC.
  With m about 16 segments and a plausible within-person ICC of 0.2 to 0.4 for plaque development
  (not sourced; must be estimated from the data), the design effect is about 4 to 7, so 32,000
  segments behave like roughly 4,500 to 8,000 independent segments for estimating segment-level
  (within-person) geometry effects. For participant-level covariates (age, LDL, smoking) the
  information is bounded by the 2000 participants regardless of segment count. A flexible learner
  fitted on segments will therefore overfit person-level patterns as if it had 16 times more data
  than it does unless grouping is respected in tuning (early stopping, hyperparameter search) as well
  as in evaluation.
- Grouped (participant-level) K-fold CV, with tuning nested inside, is required for every model,
  including regression; segment-level splitting would let a learner memorise person-level risk via
  any person-identifying feature combination and inflate AUC. Paired deltas (model with vs without
  geometry) computed on the same participant folds remain the right attribution unit.

### Gaps
- No source found giving the within-participant ICC for incident/progressing plaque across coronary
  segments in serial CCTA; the design-effect numbers above are assumption-based.
- Riley & Collins examples were not checked for an XGBoost-specific MAPE at n in the low thousands;
  only RF was reported in the retrieved portion. The full text (beyond 100k characters) was not read.
- Did not retrieve a quantitative study of how much segment-wise vs participant-wise CV inflates AUC
  specifically for clustered medical-imaging tabular data.

## 2. Mixed-effects machine learning (GPBoost, MERF, LMMNN) vs plain XGBoost and GLMM

### Takeaway
Mixed-effects ML methods exist and are mature enough to run (GPBoost has R and Python packages
with binary likelihoods), but evidence that they beat a GLMM or a plain booster with good
participant-level features on clinical clustered binary outcomes is thin and largely from their own
authors' simulations. At m = 16 segments per person, a participant random intercept is estimable,
so GPBoost is the natural "flexible GLMM" sensitivity if a tree model is fitted at segment level.

### Cited Findings
- Sigrist (JMLR 2022, vol. 23, paper 232, pp. 1 to 46), "Gaussian Process Boosting": combines tree
  boosting for the fixed-effects function with Gaussian-process and grouped random effects, relaxing
  both the linearity of the mean function in mixed models and the independence assumption of
  boosting; also presented as a solution for high-cardinality categorical variables. The abstract
  reports "increased prediction accuracy compared to existing approaches on multiple simulated and
  real-world data sets" (no numbers in the abstract). — [Sigrist, JMLR 2022](https://www.jmlr.org/papers/v23/20-322.html); [arXiv 2004.02653](https://arxiv.org/pdf/2004.02653)
- GPBoost is implemented as R/Python package `gpboost` (CRAN). The author's tutorial reports GPBoost
  being much faster than lme4 for GLMMs (> 100 times in some simulated cases). This is a blog, not
  peer-reviewed. — [CRAN gpboost manual](https://archive.linux.duke.edu/cran/web/packages/gpboost/refman/gpboost.html); [Sigrist, Towards Data Science](https://towardsdatascience.com/generalized-linear-mixed-effects-models-in-r-and-python-with-gpboost-89297622820c/)
- Simchoni and Rosset, "Integrating Random Effects in Deep Neural Networks" (JMLR 2023, vol. 24,
  paper 156, pp. 1 to 57): LMMNN uses the Gaussian negative log-likelihood of a mixed model as the
  DNN loss and reports better prediction than natural competitors on simulated and real clustered,
  spatial and longitudinal data. Earlier version at NeurIPS 2021. Primarily continuous outcomes in the
  main development. — [Simchoni & Rosset, JMLR 2023](https://www.jmlr.org/papers/v24/22-0501.html); [NeurIPS 2021 paper](https://papers.nips.cc/paper_files/paper/2021/file/d35b05a832e2bb91f110d54e34e2da79-Paper.pdf)
- A simulation in Türkiye Klinikleri J Biostat compared LME, MERF and GPBoost by RMSE; for a
  nonlinear function GPBoost beat MERF and LME in RMSE and time (search-snippet level; continuous
  outcome; low-tier journal). — [Türkiye Klinikleri J Biostat](https://turkiyeklinikleri.com/article/en-evaluation-of-traditional-machine-learning-and-mixed-effect-machine-learning-model-performances-by-simulation-study-101345.html)
- For clustered binary outcomes specifically, Speiser's BiMM tree / BiMM forest (tree + GLMM hybrid)
  showed similar or superior accuracy to CART, RF and GLMMs in simulation. — [Speiser, Univ. Iowa seminar summary](https://www.public-health.uiowa.edu/seminar/jaime-lynn-speiser); a 2025 extension, Generalized Tree-Informed Mixed Model Regression — [arXiv 2503.02266](https://arxiv.org/pdf/2503.02266)

### Inferences
- Random effects in these methods mostly improve prediction for new observations from seen
  clusters. For the thesis, every test participant is a new cluster, so the random effect contributes
  zero at prediction and the benefit is mainly in estimating the fixed function without letting
  heavy-event participants dominate (a weighting/efficiency effect), plus honest standard errors.
  Expect modest gains over plain XGBoost with grouped tuning.
- For the participant-level primary question, the segment-level model is not needed at all: one can
  model at participant level (aggregated geometry summaries) where no random effect is required.
  Mixed-effects ML is relevant only to a secondary per-segment analysis (where does it happen, given
  who), which the memory note says is mechanism-only.
- Practical ranking for the per-segment secondary analysis: GLMM (cloglog with participant random
  intercept and log-interval offset) primary; GPBoost with the same random intercept as the flexible
  sensitivity; MERF and LMMNN not worth the extra engineering.

### Gaps
- No peer-reviewed head-to-head of GPBoost vs GLMM vs plain XGBoost on a clinical clustered binary
  outcome with ~2000 clusters was found.
- Did not verify whether GPBoost supports a cloglog link with offset (it supports binary likelihoods
  including probit/logit; cloglog support not checked).

## 3. Benchmarks at n ~ 2000 to 30,000: trees vs NNs vs foundation models vs LR

### Takeaway
At a few thousand rows of ~20 tabular features, the ML benchmark literature says the choice between
GBDT and NN usually matters less than tuning, GBDTs win on irregular features, and TabPFN v2 is
top-tier below ~10,000 rows. None of these benchmarks compares against a well-specified clinical
regression; clinical comparisons with low risk of bias show no discrimination gain of ML over LR.

### Cited Findings
- McElfresh et al. (NeurIPS 2023 Datasets & Benchmarks, "When Do Neural Nets Outperform Boosted Trees
  on Tabular Data?"): 19 algorithms, 176 datasets, > 538,000 models; dataset sizes 32 to 1,025,009
  rows, about half with < 2,300 training rows. For about one third of datasets, light hyperparameter
  tuning of a GBDT gave a larger improvement than choosing GBDT vs NN. GBDTs win on "irregular"
  datasets (skewed, heavy-tailed features). TabPFN had the best average performance on small
  datasets (<= 1,250 rows) and, even subsampling to 3,000 rows, ranked near CatBoost overall (average
  rank 5.89 vs 5.50) while training about two orders of magnitude faster. XGBoost was top on the seven
  largest datasets. — [McElfresh et al. 2023, arXiv 2305.02997](https://arxiv.org/html/2305.02997v4); [NeurIPS 2023 oral](https://neurips.cc/virtual/2023/oral/73658)
- Grinsztajn, Oyallon, Varoquaux (NeurIPS 2022): trees beat deep nets on 45 datasets of ~10,000
  samples, but the benchmark excluded datasets < 3,000 rows and those where linear models were nearly
  as good. — [arXiv 2207.08815](https://arxiv.org/abs/2207.08815) (numbers as recorded in sibling note `xgboost_vs_regression.md`)
- Hollmann et al., "Accurate predictions on small data with a tabular foundation model" (Nature 2025,
  doi 10.1038/s41586-024-08328-6), TabPFN v2: pretrained on synthetic data, targeted at datasets with
  up to 10,000 samples; reported to outperform tuned GBDT ensembles in that regime. — [Univ. Freiburg release](https://uni-freiburg.de/en/new-ai-model-tabpfn-enables-faster-and-more-accurate-predictions-on-small-tabular-data-sets/); [PMC11711098](https://pmc.ncbi.nlm.nih.gov/articles/PMC11711098/)
- Christodoulou et al. (J Clin Epidemiol 2019): 282 LR-vs-ML comparisons in 71 clinical studies
  (median n 1,250, median 19 predictors, median 8 EPV); for low risk-of-bias comparisons the logit(AUC)
  difference was 0.00 (95% CI -0.18 to 0.18); 79% did not assess calibration. — [ORA record](https://ora.ox.ac.uk/objects/uuid:4167c905-5171-4fc7-b157-ff36d56a73db)

### Inferences
- Herlev–Østerbro at 2000 participants with ~20 participant-level features is in exactly the regime
  where TabPFN v2 is claimed strongest and where GBDT vs NN differences are small. Of the flexible
  tabular options, TabPFN v2 (no tuning, in-context) is arguably the most stable sensitivity model
  now, but it is a black box, does not natively handle a time offset/cloglog structure or clustering,
  and calibration in clinical data needs checking.
- Risk factors (age, LDL, BP) are "regular" features; geometry features (curvature, angles, ratios)
  can be skewed/heavy-tailed, which is where GBDTs gain. Log/rank transforms plus splines in the
  regression remove much of that advantage.
- Net: at 2000, the expected discrimination gain of XGBoost over a spline/interaction-aware penalised
  regression is near zero; it becomes a credible co-primary sensitivity, not the primary model.

### Gaps
- TabPFN v2 full text not fetched; exact sample-size and feature limits (reported as up to 10,000
  samples and 500 features) and the clinical-calibration performance are from secondary summaries.
- No clinical LR-vs-ML comparison at n 2000 to 5000 with low risk of bias and calibration reporting
  was retrieved beyond Christodoulou's pooled estimate.

## 4. Precedents: ML/DL on per-segment or per-lesion CCTA features predicting plaque progression or events

### Takeaway
Precedents are mostly PARADIGM (n about 1,000 to 2,250, serial CCTA, 2 or more years apart), using
boosted ML at participant level or regression at lesion level. Gains reported for ML are from
internal validation, often without calibration, and the strongest per-lesion result came from a
plain regression-type model. Deep learning on serial imaging exists mainly in IVUS and in small
radiomics series.

### Cited Findings
- Han et al. (JAHA 2020), PARADIGM: 1,083 patients with serial CCTA; rapid plaque progression
  defined as annual increase in percent atheroma volume >= 1.0%; nested ML models (clinical;
  + qualitative plaque; + quantitative plaque); quantitative plaque features were most important.
  AUC values not retrieved in this session (full text 403). — [DOAJ record, JAHA 2020](https://doaj.org/article/636830fb82c14cdaaff903a3ea5e9d51); [Emory OA](https://open.library.emory.edu/concern/publications/bb2318c5-d880-476f-8c71-8fc18b8021f5)
- PARADIGM per-lesion vs per-patient (search-snippet level): registry of 2,252 serial-CCTA patients
  (>= 2 year interval); 1,297 with only non-obstructive lesions; 3,218 non-obstructive baseline
  lesions; at 3.8 +/- 1.6 years, 76 lesions (2.4%, in 60 patients) became obstructive (> 50%). Adding
  per-patient plaque volume and high-risk features gave C 0.825; per-lesion features gave C 0.895
  (p < 0.001). — [Per lesion versus per patient analysis, UCP portal](https://ciencia.ucp.pt/en/publications/per-lesion-versus-per-patient-analysis-of-coronary-artery-disease/)
- Pericoronary adipose tissue radiomics (2025): 97 patients, 127 plaques (40 progressive); random
  forest AUC 0.971 training vs 0.821 validation, an example of the optimism typical at tiny n. —
  [PMC11872547](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11872547/)
- IVUS deep learning (EuroIntervention): biLSTM + 2 dense layers forecasting change in percent
  atheroma volume; test accuracy 0.84, MCC 0.68, F1 0.84 with external validation. —
  [EuroIntervention](https://eurointervention.pcronline.com/article/derivation-and-external-validation-of-a-deep-learning-model-to-predict-changes-in-coronary-plaque-burden)
- Automated plaque quantification (PlaqueSegNet, Radiology 2025/2026): 2,013 patients from 17
  hospitals (1,409 train / 604 validation), ICC > 0.90 vs readers and IVUS across four external sets;
  this is measurement, not prediction of progression. — [Radiology](https://pubs.rsna.org/doi/abs/10.1148/radiol.251967); [Diagnostic Imaging news, Apr 2026](https://www.diagnosticimaging.com/view/quantifying-coronary-plaque-ccta-fully-automated-ai-model-)

### Inferences
- The PARADIGM per-lesion example has 76 lesion events in 60 patients out of 3,218 lesions: event
  counts in clustered per-lesion data are tiny relative to the record count, which is the same trap
  the thesis faces at segment level.
- No precedent was found that uses coronary centerline geometry (curvature profiles, bifurcation
  angles) with ML for incident plaque in an asymptomatic population cohort; the thesis would be
  first-of-kind rather than following a template, which argues for interpretable primary analysis.

### Gaps
- ICONIC and CREDENCE ML analyses, and endothelial shear stress + ML progression models, were not
  retrieved within the tool budget; their sample sizes and ML-vs-regression gains remain open.
- Han 2020 AUCs and calibration not verified in this session (sibling note may hold them).

## 5. Late fusion of a curvature-sequence encoder with tabular risk factors at this size

### Takeaway
At 2000 participants (a few hundred to ~800 participant events), training a sequence encoder end to
end on the outcome is more affordable than at a few hundred, but still below the EPV range where
neural nets stabilise, and the encoder would compete with only a modest incremental signal. The
earlier two-stage design (outcome-free pretrained encoder on ImageCAS, or a cross-fitted
out-of-fold profile score, compared against MiniRocket + ridge) remains the right plan; the
change is that a lightly fine-tuned encoder becomes a reasonable exploratory arm.

### Cited Findings
- Neural nets needed > 100 EPV for stable AUC and often never reached optimism < 0.01 at > 200 EPV in
  clinical simulations. — [van der Ploeg et al. 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289553)
- Data-driven hyperparameter tuning increases individual-risk instability compared with prespecified
  settings (shown for random forest). — [Riley & Collins 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10952221/)
- MiniRocket / ROCKET and self-supervised pretraining evidence, plus the "late fusion = logistic
  regression with one learned covariate" argument, are documented in the sibling note
  `late_fusion_networks.md` (not re-fetched here).

### Inferences
- Parameter budget: a 1D CNN over a resampled curvature profile has thousands of weights; with
  ~400 to 800 participant events (or ~1,600 segment events with a design effect of 4 to 7), end-to-end
  training is still far into the data-hungry zone. Pretraining on ImageCAS (1000 geometries, no
  outcome) then freezing, or fine-tuning only the last layer with strong weight decay, keeps the
  outcome-trained parameter count near that of a spline.
- At 2000 the cross-fitted design becomes cleaner: with 5 or 10 participant-grouped folds, each
  out-of-fold curvature score is learned from 1,600 to 1,800 participants, so a K-fold cross-fitted
  profile score entering a regression as one covariate is now practical. Attribution: refit the
  fused model without the curvature family on identical participant folds and report the paired
  delta in log-likelihood/Brier/AUC with participant-bootstrap CIs.
- MiniRocket + ridge (no outcome-trained features, ~10,000 random kernels, ridge on top) must be the
  baseline any learned encoder beats; if it does not, the encoder adds nothing.

### Gaps
- No published study found that fuses a centerline curvature sequence with risk factors for plaque
  outcomes, so there is no empirical estimate of the curvature signal's incremental AUC.

## 6. Interpretability for an association question: SHAP, correlated features, ML-to-inform-regression

### Takeaway
A two-step approach (XGBoost + SHAP interaction screen, then prespecify only confirmed nonlinear
terms or interactions in the regression, tested on held-out participants) is supported in
epidemiology, but SHAP-based interaction detection only reliably catches moderate-to-large
interactions, and SHAP values are not effect estimates when features are correlated (geometry
families are highly correlated). Use it as hypothesis generation, with the regression as the
estimand.

### Cited Findings
- Interaction analysis with XGBoost + SHAP vs logistic regression, simulation informed by Swedish
  population cohorts (n = 47,770): sensitivity for detecting interaction discrepancies was 28%
  (small), 83% (moderate) and 100% (large); SHAP had similar ability to LR to identify interaction
  direction. — [Interaction Analysis Based on Shapley Values and XGBoost, PMC9340268](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9340268/)
- RuleSHAP (2025) combines Bayesian sparse regression with tree-derived rules and Shapley values to
  detect nonlinear and interaction effects with uncertainty quantification, demonstrated on
  epidemiological cohort data (age, sex, ethnicity, BMI, glucose). Preprint. —
  [arXiv 2505.00571](https://arxiv.org/pdf/2505.00571)

### Inferences
- The Swedish simulation had 47,770 participants; at 2000 participants the power to detect small
  interactions via SHAP will be well below the 28% reported there, so a null SHAP screen is not
  evidence of no interaction.
- With correlated geometry features (curvature summaries along the same artery, lumen volume vs
  myocardial mass), interventional SHAP splits credit arbitrarily; group-level SHAP (sum per feature
  family) or drop-family refits are more defensible than per-feature attributions.
- Workflow that survives reviewers: split participants into discovery and confirmation halves (or
  cross-fit); screen with XGBoost/SHAP or tree-based rules on discovery; encode at most 2 to 4
  candidate terms (spline knots, product terms) in the penalised regression; test them on the
  confirmation half via a likelihood-ratio or paired-delta comparison.

### Gaps
- Not retrieved: methodological work on SHAP with correlated features (e.g. Aas et al. 2021) and
  group-SHAP; cited from general knowledge only, so omitted as findings.

## Overall bottom line for the report writer (inference)
- At ~2000 participants: regression (penalised logistic/cloglog with log-interval offset, splines on
  continuous risk factors) stays primary; it is now well powered, so the nested "does geometry add"
  test is robust and a few prespecified nonlinear terms/interactions are affordable.
- XGBoost (shallow, prespecified or lightly tuned within participant-grouped nested CV, depth 2 to 3)
  upgrades from minor sensitivity to a credible co-primary sensitivity and an interaction screen;
  GPBoost if fitted at segment level. TabPFN v2 is a cheap additional tabular benchmark in this n range.
- NN late fusion: still exploratory; pretrained/frozen or cross-fitted encoder, benchmarked against
  MiniRocket + ridge; full end-to-end training on the outcome is still under-resourced by EPV standards.
- Everything evaluated with participant-grouped CV, calibration reported, instability plots
  (Riley & Collins) for each model.
