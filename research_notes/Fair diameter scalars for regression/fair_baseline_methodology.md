# Fair baseline methodology: handcrafted scalar summaries of a 1D profile vs a per-point neural sequence model

Context: per-point curvature and lumen radius profiles along coronary arteries (800 CCTA scans). Arms: sequence model on [curvature] and on [curvature, radius]; each against logistic regression (LR) on scalar summaries (mean |curvature| plus a diameter scalar). Covariates age, sex, dominance. Nested/repeated CV.

Note on sourcing: items marked "(not re-fetched this session)" are standard references cited from prior knowledge with their canonical links; the report writer should verify them before they bear thesis weight. Everything else was checked against a search result or fetched page on 2026-09-28.

## Q1. What does the methodology literature say about "strong baseline" design when claiming a deep model beats handcrafted features?

### Takeaway
The consistent message across clinical epidemiology, ML meta-science and time-series benchmarking is that apparent deep-learning advantages shrink or vanish when the comparator is tuned with equal care, validated with equal rigour, and at low risk of bias. A fair baseline is therefore one that gets the same tuning budget, the same validation protocol, the same covariates, and an information content that is not artificially crippled.

### Cited Findings
- Christodoulou E, Ma J, Collins GS, Steyerberg EW, Verbakel JY, Van Calster B. "A systematic review shows no performance benefit of machine learning over logistic regression for clinical prediction models." J Clin Epidemiol 2019;110:12–22, doi:10.1016/j.jclinepi.2019.02.004. 71 of 927 studies included (median n = 1,250, 19 predictors, 8 events per predictor). No difference in C-statistic between ML and LR in low-risk-of-bias comparisons; a difference favouring ML appeared only in high-risk-of-bias comparisons — [PubMed](https://pubmed.ncbi.nlm.nih.gov/30763612/); [J Clin Epi abstract](https://www.jclinepi.com/article/S0895-4356(18)31081-3/abstract)
- Lipton ZC, Steinhardt J. "Troubling Trends in Machine Learning Scholarship" (ICML 2018 debate track; ACM Queue 17(1), 2019). Identifies "failure to identify the sources of empirical gains" and a tendency to compare against the same weak baselines, with lineages of purported improvements overturned by simple, well-tuned baselines — [arXiv 1807.03341](https://arxiv.org/pdf/1807.03341); [ACM Queue](https://dl.acm.org/doi/10.1145/3317287.3328534)
- Grinsztajn L, Oyallon E, Varoquaux G. "Why do tree-based models still outperform deep learning on typical tabular data?" NeurIPS 2022 Datasets & Benchmarks. On 45 datasets with equal hyperparameter-search budgets, tree ensembles remained state of the art on medium-sized (~10K sample) tabular data — [paper notes / summary](https://github.com/AkihikoWatanabe/paper_notes/issues/574)
- Zvuloni E, et al. "On Merging Feature Engineering and Deep Learning for Diagnosis, Risk Prediction and Age Estimation Based on the 12-Lead ECG." IEEE Trans Biomed Eng 2023, doi:10.1109/TBME.2023.3239527. Reported that for classical 12-lead ECG diagnosis tasks deep learning did not yield a meaningful improvement over domain-knowledge feature engineering, and that for classical tasks and/or small datasets feature engineering may be the better choice — [PubMed 37022038](https://pubmed.ncbi.nlm.nih.gov/37022038/); [IEEE](https://ieeexplore.ieee.org/document/10025679/) (full text not fetched; claim from indexed abstract/summary)
- Strodthoff N, Wagner P, Schaeffter T, Samek W. "Deep Learning for ECG Analysis: Benchmarks and Insights from PTB-XL." IEEE JBHI 2021 (arXiv 2004.13701). On 21,837 ECGs, ResNet/Inception CNNs outperformed a feature-based baseline by a large margin — i.e. deep models can win when n is large and the comparator is a generic feature set — [arXiv](https://arxiv.org/abs/2004.13701); [code](https://github.com/helme/ecg_ptbxl_benchmarking)
- PTB-XL follow-up work found that combining raw signals with extracted clinical features gave only marginal gains over signal-only models, suggesting the pre-extracted features already capture much of the predictive information — [Springer chapter, "Evaluation of Raw Signal and Feature-Based Deep Learning Models for Multi-Label ECG Diagnosis on PTB-XL"](https://link.springer.com/chapter/10.1007/978-3-032-11442-6_36) (snippet-level; not fetched)
- TRIPOD+AI (Collins GS, Moons KGM, Dhiman P, Riley RD, Beam AL, Van Calster B, et al., BMJ 2024;385:e078378, published 16 April 2024) is the current reporting guideline covering both regression and ML prediction models and supersedes TRIPOD 2015; it applies the same reporting requirements (predictor handling, tuning, internal validation, performance incl. calibration) to both model classes — [PMC11025451](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11025451/)

### Inferences
- The Christodoulou result is the key citation for the thesis: a "network beats LR" claim is only credible if the LR arm is at low risk of bias, which in that review meant correct handling of continuous predictors, no data-driven selection outside validation, and reporting of calibration, not just discrimination.
- Strodthoff (n ≈ 22K) vs Zvuloni (classical tasks, smaller n) brackets the regime: with ~800 scans (and fewer events), the thesis is closer to the regime where engineered features are competitive, so a weak LR arm would visibly inflate the network's margin.
- "Strong baseline" operationally = equal effort: same outer CV folds, same seeds/repeats, same covariate set, a tuning grid for the LR penalty inside the inner loop just as the network gets inner-loop early stopping/hyperparameters.

### Gaps
- Christodoulou's detailed low-bias criteria (the four signalling items) were not re-read in full text this session.
- No source found that states a formal definition of "strong baseline" for 1D profile vs sequence-model comparisons; the rule above is a synthesis.

## Q2. Which information-matched baselines (FPCA, functional LR, summary-stat sets, binned means, splines + penalised LR) are considered the fair comparator to a sequence model on the same signal?

### Takeaway
A hierarchy exists. A single mean scalar per channel is the "clinical-convention" baseline; the information-matched comparator to a model that sees the whole profile is a functional regression on that same profile (FPCA-score logistic regression or penalised functional regression), optionally plus a small fixed summary-feature set (catch22-style) and a strong generic time-series classifier (ROCKET family). The honest design reports several rungs so the reader can see where the gain comes from.

### Cited Findings
- Functional logit regression models a binary response from a functional predictor; the standard estimator expands each curve in functional principal components and fits LR on the FPC scores, turning the functional model into a multivariate one (Escabias M, Aguilera AM, Acal C. "logitFD: an R package for functional principal component logit regression." The R Journal 2022, RJ-2022-053). Components can be chosen by explained variance or by stepwise predictive ability — [R Journal](https://rjournal.github.io/articles/RJ-2022-053/)
- Goldsmith J, Bobb J, Crainiceanu C, Caffo B, Reich D. "Penalized functional regression." J Comput Graph Stat 2011;20(4):830–851. Projects the functional predictor onto many smooth eigenvectors and estimates the coefficient function by penalised splines (mixed-model framework, so smoothing is REML-estimated rather than tuned on outcome); works for generalised (e.g. logistic) outcomes; motivated by DTI tract profiles in MS vs controls — a close analogue of per-point profiles along a vessel — [T&F](https://www.tandfonline.com/doi/abs/10.1198/jcgs.2010.10007); implemented as `refund::pfr` — [rdrr](https://rdrr.io/cran/refund/man/pfr.html)
- FPCA projection onto estimated eigenfunctions is an established route to classification features for biomedical signals (e.g. brain signals) — [arXiv 1504.02800](https://arxiv.org/pdf/1504.02800); PCA + regularised LR applied to EEG epilepsy classification — [PubMed 38424732](https://pubmed.ncbi.nlm.nih.gov/38424732)
- Lubba CH, Sethi SS, Knaute P, Schultz SR, Fulcher BD, Jones NS. "catch22: CAnonical Time-series CHaracteristics." Data Min Knowl Disc 2019;33:1821–1852. 22 minimally redundant features selected from 4,791 hctsa features via performance on 93 classification datasets (>147,000 series); covers autocorrelation, value distribution, outliers and fluctuation scaling — [Springer](https://link.springer.com/article/10.1007/s10618-019-00647-x); [arXiv 1901.10200](https://arxiv.org/abs/1901.10200); [code](https://github.com/DynamicsAndNeuralSystems/catch22)
- Middlehurst M, Schäfer P, Bagnall A. "Bake off redux: a review and experimental evaluation of recent time series classification algorithms." Data Min Knowl Disc 2024. On 112 UCR + 30 new datasets (142), MultiROCKET+Hydra and HIVE-COTE v2 were significantly best; best-in-category included FreshPRINCE (feature-based, tsfresh + rotation forest), InceptionTime (deep), rSTSF (interval) — i.e. deep learning is not dominant on generic univariate TSC — [arXiv 2304.13029](https://arxiv.org/abs/2304.13029); [DMKD](https://dl.acm.org/doi/10.1007/s10618-024-01022-1)
- Ramsay JO, Silverman BW. Functional Data Analysis, 2nd ed., Springer 2005 — canonical reference for functional linear/generalised models and FPCA — [Springer](https://link.springer.com/book/10.1007/b98888) (not re-fetched this session)
- Dempster A, Petitjean F, Webb GI. "ROCKET: exceptionally fast and accurate time series classification using random convolutional kernels." Data Min Knowl Disc 2020;34:1454–1495 — random-kernel features + ridge/logistic classifier; a linear model on fixed features that is competitive with deep TSC — [arXiv 1910.13051](https://arxiv.org/abs/1910.13051) (not re-fetched this session)

### Inferences
- Proposed baseline ladder for each channel set ([curv] and [curv, radius]):
  1. **B0 covariates only**: age, sex, dominance. Establishes what the profiles add at all.
  2. **B1 pre-specified clinical scalars**: mean |curvature| (+ one diameter scalar), plus covariates. This is the conventional comparator the thesis already plans.
  3. **B2 fixed summary set**: per channel a small pre-registered set (e.g. mean, SD, 10th/90th percentile, min, linear slope along arc length) in ridge/elastic-net LR. Tests whether distributional shape, not order, carries the signal.
  4. **B3 functional LR (information-matched)**: FPCA scores (K by fixed variance threshold, e.g. 95%, chosen inside the training fold) or `refund::pfr` on the resampled profile, plus covariates, penalised. This sees the same per-point signal as the network but with a linear, smooth functional effect.
  5. **B4 optional generic TSC**: MiniROCKET/MultiROCKET features + ridge LR, as a "no hand design, no deep learning" check.
  The network's claim is then "beats B3 (and B4)", not merely "beats B1". Beating B1 but not B3 means the gain is from reading the full profile, not from deep learning per se; that is a legitimate and interesting result, but a different claim.
- FPCA/pfr require a common domain. Profiles of varying length must be reparametrised (e.g. normalised arc length on [0,1], or fixed-length proximal segment in mm). The same reparametrisation choice must be applied to the network input or its difference stated, otherwise the arms do not see the same information.
- Binned/segment means (e.g. proximal/mid/distal thirds, or per anatomical segment) are a coarse, interpretable version of B3 and match how clinicians segment coronaries; they suit B2.

### Gaps
- No head-to-head study found comparing FPCA-LR against a sequence network specifically on vessel centerline profiles (curvature/radius); the analogy to DTI tract profiles (Goldsmith 2011) is the nearest.
- Did not locate a published consensus statement naming FPCA-LR as "the" fair comparator; the ladder is a synthesis of FDA and TSC literature.

## Q3. Feature-count matching and handling multiple candidate diameter scalars without outcome-driven selection

### Takeaway
Do not choose the diameter scalar by looking at outcome association on the full data. Either pre-register one scalar with a biological rationale, or include all candidates and let a penalty shrink them inside the training folds, with any selection repeated in every inner loop. "One scalar per channel" is a reasonable pre-specified default for B1, but information matching is better achieved by the B2/B3 rungs than by counting features.

### Cited Findings
- Varma S, Simon R. "Bias in error estimation when using cross-validation for model selection." BMC Bioinformatics 2006;7:91. Using CV to estimate error of a classifier whose parameters were tuned by CV on the same data gives a significantly optimistic estimate, shown even on null data where classes do not differ; nested CV removes this bias — [Semantic Scholar](https://www.semanticscholar.org/paper/Bias-in-error-estimation-when-using-for-model-Varma-Simon/bf75f2555e8485d536ac217068b7963de3d6fa02); [ResearchGate](https://www.researchgate.net/publication/7273753_Bias_in_Error_Estimation_When_Using_Cross-Validation_for_Model_Selection_BMC_Bioinformatics_71_91)
- Heinze G, Wallisch C, Dunkler D. "Variable selection – A review and recommendations for the practicing statistician." Biometrical Journal 2018;60:431–449, doi:10.1002/bimj.201700067. Review of selection methods and recommendations for prediction and explanatory models (the paper cautions against data-driven selection in small samples and favours background-knowledge-based pre-specification; see full text) — [Wiley](https://onlinelibrary.wiley.com/doi/full/10.1002/bimj.201700067); commentary [Le Cessie et al. 2019](https://onlinelibrary.wiley.com/doi/10.1002/bimj.201900088)
- Functional PC logit models can select components by explained variance (outcome-blind) or by stepwise predictive ability (outcome-driven) — [logitFD, R Journal 2022](https://rjournal.github.io/articles/RJ-2022-053/)
- Riley RD, Ensor J, Snell KIE, Harrell FE, Martin GP, Reitsma JB, et al. "Calculating the sample size required for developing a clinical prediction model." BMJ 2020;368:m441. Sample size depends on number of candidate predictor parameters, outcome prevalence and anticipated performance (C-statistic as proxy for R²); aims to limit overfitting via expected calibration slope (e.g. shrinkage ≥ 0.9) — [summary via PMC primer](https://pmc.ncbi.nlm.nih.gov/articles/PMC12106283/)
- Cawley GC, Talbot NLC. "On over-fitting in model selection and subsequent selection bias in performance evaluation." JMLR 2010;11:2079–2107 — over-fitting the model-selection criterion can bias performance comparisons as much as differences between algorithms — [JMLR](https://www.jmlr.org/papers/v11/cawley10a.html) (not re-fetched this session)

### Inferences
- Concrete rules for the diameter scalar(s):
  1. **Pre-register** in a dated document (git commit hash of the analysis plan) the primary diameter scalar before any outcome is inspected. A defensible default, parallel to mean |curvature|, is the **mean lumen radius along the same centerline domain** (same channel, same summary operator). This makes B1 symmetric: one mean per channel.
  2. List secondary candidates (e.g. minimum radius, radius percentile, proximal-to-distal taper slope, reference-normalised minimal diameter) as **sensitivity analyses**, all reported, not a "best of" pick.
  3. If several diameter scalars enter one model, use ridge/elastic-net with the penalty chosen in the **inner** loop; never univariate screening on the full cohort. If a selection step exists (stepwise, lasso support, FPC count chosen by predictive ability), it goes inside the inner loop (Varma & Simon 2006).
  4. Budget parameters with Riley et al.: count the candidate parameters (covariates + scalars, plus spline df if nonlinearity is modelled) against the event count; with ~800 scans and a binary CAD-type outcome, a handful of parameters is the safe range for unpenalised LR.
  5. Model continuous scalars flexibly (restricted cubic splines with 3–4 knots, pre-specified) rather than linearly or dichotomised, so the LR is not handicapped by a linearity assumption the network does not have.
- Feature-count matching: equal counts per channel is useful for B1 symmetry (curvature arm: 1 scalar; curvature+radius arm: 2 scalars) so the Δ from adding radius is comparable between LR and network. It does not equalise information with the network; that is B3's job.
- The within-arm Δ (adding radius) is the cleanest comparison: Δ_LR = AUC(B1 curv+radius) − AUC(B1 curv) vs Δ_NN = AUC(NN curv+radius) − AUC(NN curv), both on identical folds, paired.

### Gaps
- The exact Heinze et al. 2018 recommendations (e.g. EPV thresholds for selection) were not extracted from full text.
- Event count/outcome prevalence for the thesis outcome is not known here, so the Riley calculation cannot be done in these notes.

## Q4. How to include size covariates / normalisation so the NN and LR see the same confounders

### Takeaway
Give both arms the identical covariate vector (age, sex, dominance, and any body-size or reference-diameter variable) entering the same way: as additional regressors in LR and as late-fused inputs to the network head. Avoid ratio normalisation of radius (e.g. radius/BSA or radius/reference radius) as the only form of size adjustment; include the size variable as a covariate instead, and if a ratio is used, apply the identical ratio to the network's per-point radius input.

### Cited Findings
- Kronmal RA. "Spurious Correlation and the Fallacy of the Ratio Standard Revisited." J R Stat Soc A 1993;156:379–392. Using a ratio as a dependent or independent variable in multiple regression can produce incorrect or misleading inferences; recommends avoiding ratios in regression and instead including the denominator as a covariate; ratios sharing a common term can show spurious correlation even between uncorrelated components — [Wiley](https://rss.onlinelibrary.wiley.com/doi/10.2307/2983064); [OUP](https://academic.oup.com/jrsssa/article/156/3/379/7106826)
- TRIPOD+AI requires full specification of predictors and how they were handled for both regression and ML models, which in practice means the same covariate definitions across compared models must be reported — [PMC11025451](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11025451/)

### Inferences
- Rules:
  1. **Same covariate vector, same encoding**: dominance one-hot (right/left/co-dominant), sex binary, age continuous (standardised with training-fold statistics only). LR: covariates as additional terms. NN: concatenated after the sequence encoder's pooled embedding (late fusion), before the classification head. Do not feed covariates only to one arm.
  2. **Covariate-only floor (B0) for both**: report B0 and each arm's increment over B0, so the network cannot "win" merely by learning age/sex better through a nonlinear head. An additional control is to fit LR on [B0 covariates + NN's out-of-fold logit] to see whether the NN adds beyond covariates (a stacked-increment check).
  3. **Radius normalisation**: pick one convention (absolute mm, or divided by a per-vessel reference such as proximal radius) and apply it identically to the LR scalar and to the network's per-point radius channel. Per Kronmal, prefer absolute radius + size covariate over a ratio; if a ratio is scientifically required (tapering is inherently relative), state it and consider a sensitivity analysis with the absolute version.
  4. **Standardisation leakage**: z-scoring of per-point channels (network) and of scalars (LR) must use training-fold means/SDs only; same for FPCA basis estimation in B3.
  5. **Confounding by vessel length/coverage**: mean |curvature| depends on centreline length and endpoint placement; if the network sees a fixed-length or length-normalised profile, compute LR scalars over exactly the same domain.

### Gaps
- No source found that specifically addresses late fusion of clinical covariates in sequence models as a fairness requirement; the rule is inferred from the "same predictors" principle.
- Coronary-specific evidence on the best body-size normaliser for lumen radius (BSA, height, LV mass, reference segment) was out of scope and not searched.

## Q5. Evidence that FPCA or summary-statistic LR matches deep models on 1D biomedical signals

### Takeaway
Evidence is mixed and regime-dependent. With large n and complex morphology (PTB-XL ECG, ~22K records) deep CNNs clearly beat feature baselines; on classical tasks and smaller cohorts, domain features match deep models, and on generic univariate time-series benchmarks feature-based and linear-on-random-features methods are at or near the top alongside deep models. Direct FPCA-LR vs deep-network head-to-heads in biomedical 1D signals are scarce.

### Cited Findings
- Deep CNNs outperformed feature-based algorithms by a large margin on PTB-XL tasks (n = 21,837 ECGs) — [Strodthoff et al., arXiv 2004.13701](https://arxiv.org/abs/2004.13701)
- For traditional 12-lead ECG diagnosis tasks, deep learning did not yield a meaningful improvement over feature engineering; for classical tasks and/or small datasets feature engineering may be preferable — [Zvuloni et al., IEEE TBME 2023](https://pubmed.ncbi.nlm.nih.gov/37022038/)
- Combined raw-signal + clinical-feature models gave only marginal gains over signal-only on PTB-XL, suggesting features capture much of the information — [Springer 2025 chapter](https://link.springer.com/chapter/10.1007/978-3-032-11442-6_36)
- On the 142-dataset UCR benchmark, MultiROCKET+Hydra and HIVE-COTE v2 were best; the deep InceptionTime was best-in-category but not overall best; the feature-based FreshPRINCE was competitive in its category — [Middlehurst et al. 2024](https://arxiv.org/abs/2304.13029)
- LR on no-outcome-leakage clinical predictors matches ML in low-bias studies (C-statistic difference ≈ 0) — [Christodoulou et al. 2019](https://pubmed.ncbi.nlm.nih.gov/30763612/)
- PCA + regularised LR reached ~94.9% average accuracy on epilepsy EEG classification (single study, not a head-to-head with deep models in the snippet seen) — [PubMed 38424732](https://pubmed.ncbi.nlm.nih.gov/38424732)

### Inferences
- With 800 scans (and fewer positive cases, split by CV), the thesis is in the small-data regime where a well-built B2/B3 is expected to be competitive. A null or small NN advantage over B3 is a plausible, publishable outcome and should be pre-framed as such rather than treated as failure.
- Statistical comparison of arms should be paired on identical outer folds and repeats; use the corrected resampled t-test (Nadeau & Bengio 2003, Machine Learning 52:239–281, not re-fetched this session) or a bootstrap of the pooled out-of-fold predictions for ΔAUC, and report calibration (slope/intercept) for every arm, per TRIPOD+AI.

### Gaps
- No direct study found comparing FPCA/functional LR against deep sequence models on vessel geometry profiles or other anatomical 1D profiles.
- Zvuloni et al. numbers (AUCs, dataset sizes per task) were not extracted because the full text was not accessible (PubMed returned a captcha; IEEE not fetched).
- No 2025–2026 meta-analysis specifically on "deep vs feature" for 1D physiological signals was located in this session.
