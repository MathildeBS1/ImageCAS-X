# Training, validating and benchmarking a neural network for segment-level plaque prediction in a small clustered cohort (CGPS Herlev-Østerbro)

Scope: ~2000 patients, ~30,000 segment-level samples clustered within patients; predictors SCORE2 variables, baseline per-segment plaque, centerline tree, lumen segmentation, per-segment geometry; outcome per-segment plaque at 10-year follow-up CCTA. ImageCAS (1000 scans, no outcomes) is available for unlabelled development/pretraining.

Note on sourcing: several primary PMC pages returned captcha/403 during this session, so some numbers are taken from search-result abstracts of the primary papers rather than full text. Where that matters it is flagged.

## 1. Deep learning vs logistic regression / gradient boosting at this sample size

### Takeaway
For tabular clinical prediction at n of a few thousand, the evidence says neural networks do not beat well-specified logistic regression or tuned gradient-boosted trees on average; apparent ML gains largely vanish under low-risk-of-bias comparisons. The exceptions are tabular foundation models (TabPFN) at small n, carefully tuned/ensembled modern MLPs on large benchmarks, and settings where the NN consumes non-tabular structure (graphs, images) that the tabular baselines cannot.

### Cited Findings
- Christodoulou et al. 2019 (J Clin Epidemiol) systematic review: 71 studies (from 927), median sample size 1,250 (range 72 to 3,994,872), median 19 predictors, median 8 events per predictor. For 145 comparisons at low risk of bias, difference in logit(AUC) between LR and ML was 0.00; for 137 comparisons at high risk of bias, logit(AUC) was 0.34 (95% CI 0.20 to 0.47) higher for ML. 68% of studies had potential bias in validation procedures. Conclusion: no performance benefit of ML over LR. — [Christodoulou et al. 2019, J Clin Epidemiol (Oxford ORA record)](https://ora.ox.ac.uk/objects/uuid:4167c905-5171-4fc7-b157-ff36d56a73db); [full text PDF mirror](https://med.mahidol.ac.th/ceb/sites/default/files/public/pdf/Repository/1-s2.0-S0895435618310813-main.pdf)
- Grinsztajn, Oyallon, Varoquaux 2022 (NeurIPS Datasets & Benchmarks): 45 datasets, accounting for hyperparameter search budget; tree-based models remain state of the art on medium-sized data (~10K samples). NN weaknesses identified: not robust to uninformative features, do not preserve data orientation (rotation invariance), struggle to learn irregular functions. — [Grinsztajn et al. 2022, NeurIPS](https://neurips.cc/virtual/2022/poster/55627); [arXiv 2207.08815](https://arxiv.org/abs/2207.08815v1)
- Shwartz-Ziv & Armon (arXiv 2106.03253; ICML 2021 AutoML workshop, later Information Fusion 2022): XGBoost outperformed recent deep tabular models (TabNet, NODE, DNF-Net, 1D-CNN) including on the datasets used in those models' own papers; XGBoost needed much less tuning; an ensemble of deep models plus XGBoost beat XGBoost alone. — [Shwartz-Ziv & Armon, arXiv](https://arxiv.org/abs/2106.03253)
- McElfresh et al. 2023 (NeurIPS Datasets & Benchmarks): 19 algorithms on 176 datasets. The NN vs GBDT debate is "overemphasized": for many datasets the difference is negligible, or light GBDT tuning matters more than the model class. GBDTs handle skewed/heavy-tailed features and irregularities better. TabPFN outperformed all other algorithms on average despite being limited to training sets of ~3000. — [McElfresh et al. 2023, NeurIPS](https://neurips.cc/virtual/2023/poster/73658); [arXiv 2305.02997](https://arxiv.org/abs/2305.02997v4)
- Hollmann et al. 2025 (Nature 637:319): TabPFN (v2), a transformer pretrained on synthetic data, designed for datasets with up to ~10,000 samples; reported to outperform tuned GBDT baselines on small tabular data while requiring far less compute. — [Hollmann et al. 2025, Nature (RePEc record)](https://ideas.repec.org/a/nat/nature/v637y2025i8045d10.1038_s41586-024-08328-6.html); [University of Freiburg press release](https://uni-freiburg.de/en/new-ai-model-tabpfn-enables-faster-and-more-accurate-predictions-on-small-tabular-data-sets/). Exact win rates not retrieved (PMC full text blocked by captcha).
- TabArena (Erickson et al., preprint arXiv 2506.16791, 2025; living benchmark): with tuning plus ensembling, RealMLP (Elo 1569) and TabM (1552) ranked above LightGBM (1532), CatBoost (1489) and TabPFNv2 (1414, though normalised score 0.476 vs CatBoost 0.433). Shows that modern MLPs can match/beat GBDTs when tuned and ensembled, at large compute cost. PREPRINT. — [TabArena, arXiv](https://arxiv.org/abs/2506.16791)
- Kapoor & Narayanan 2023 (Patterns): leakage found in 17 fields affecting 294 papers; in civil-war prediction, apparent superiority of complex ML over logistic regression disappeared after leakage was corrected. — [Kapoor & Narayanan 2023, Patterns (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10499856); [project page](https://reproducible.cs.princeton.edu/)

### Inferences
- The CGPS task is not purely tabular: the NN's only defensible advantage is that it can consume the centerline graph and lumen geometry directly (GNN/point-cloud/image encoders), whereas LR/GBDT get hand-crafted per-segment features. The thesis should therefore frame the NN's added value as "does learned tree/geometry representation add discrimination over engineered features", not "NN vs LR".
- Baseline plaque at the same segment is likely to dominate prediction (strong autoregressive predictor), which shrinks the room for any complex model to add value; incremental-value testing (Section 5) is central.
- Mandatory baselines: penalised LR (with splines for continuous predictors), tuned GBDT (LightGBM/XGBoost/CatBoost) on the same engineered features, and TabPFN where n fits (TabPFN v2 limit ~10k rows, so patient-level or subsampled use, or newer versions; check). An NN that does not beat these under the same nested grouped CV is not justified.
- Christodoulou's high-vs-low risk-of-bias split is a direct warning: most reported ML gains come from flawed validation. Grouped nested CV (Section 4) is what makes the comparison credible.

### Gaps
- No benchmark found specifically for clustered (multiple-observations-per-patient) tabular clinical prediction comparing NN vs GBDT vs mixed-effects LR.
- TabPFN Nature paper's exact numbers (win rate, AUC deltas) not retrieved due to access block; TabPFN-2.5 (preprint arXiv 2511.08667) reportedly extends sample limits but was not verified.
- No study found comparing GNNs on coronary trees vs engineered-feature GBDT for plaque progression.

## 2. Sample size, events per variable, effective sample size under clustering

### Takeaway
Use Riley's criteria (pmsampsize) rather than 10 EPV; ML models need more data than regression and become unstable at small n. With ~15 segments per patient, the effective sample size is the patient count inflated by a design effect, likely between ~2,000 and ~12,000 rather than 30,000, so model complexity must be budgeted against the effective, not raw, n.

### Cited Findings
- Riley criteria for development of a binary-outcome model: target expected shrinkage factor >=0.9 (<=10% overfitting), optimism in Nagelkerke/Cox-Snell R2 <=0.05, precise estimation of overall risk (intercept). Implemented in R/Stata `pmsampsize`. Worked example: 3% event rate, 25 candidate predictors, C=0.74 requires 9,658 patients (290 events); with 15 predictors, 5,795 (174 events). The authors note ML methods "will likely require an even larger sample size". — [Martin, Riley, Ensor, Grant 2025, Eur J Cardiothorac Surg (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12106283/); original criteria in [Riley et al. 2020, BMJ 368:m441](https://www.bmj.com/content/368/bmj.m441)
- Riley & Collins 2023 (Biometrical Journal): models from small datasets show considerable instability in individual risk estimates, which manifests as miscalibration in new data; recommend examining instability at development via ~1000 bootstrap re-fits, prediction instability plots, mean absolute prediction error (MAPE), and calibration/classification/decision-curve instability plots. — [Riley & Collins 2023, Biom J (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10952221/)
- Riley et al. 2025 (Lancet Digital Health) "Importance of sample size on the quality and utility of AI-based prediction models for healthcare": argues small development sizes produce unstable, miscalibrated AI models. — [Lancet Digit Health 2025](https://www.thelancet.com/journals/landig/article/PIIS2589-7500(25)00021-4/fulltext) (full text 403; details not verified).
- Riley et al. 2024 (BMJ) "Evaluation of clinical prediction models (part 3): calculating the sample size required for an external validation study": tailor calculations to the model and setting; many validation studies are too small, giving wide CIs. — [Birmingham repository](https://research.birmingham.ac.uk/en/publications/evaluation-of-clinical-prediction-models-part-3-calculating-the-s); [PDF](https://pure-oai.bham.ac.uk/ws/files/217741108/bmj-2023-074821.full.pdf)
- Sample size via learning-type curves (preprint): combining calculations across sample sizes with Gaussian-process learning curves is more robust/efficient. PREPRINT. — [arXiv 2303.09575](https://arxiv.org/html/2303.09575v2)
- Design effect: DEFF = 1 + rho(m - 1), rho = intraclass correlation, m = average cluster size; effective sample size = n / DEFF. — [Killip, Mahfoud, Pearce 2004, Ann Fam Med](https://www.annfammed.org/content/2/3/204)

### Inferences
- Illustrative arithmetic (not from a source): 30,000 segments, m=15, rho=0.1 gives DEFF=2.4, ESS ~12,500; rho=0.3 gives DEFF=5.2, ESS ~5,800; rho near 1 for patient-level predictors (SCORE2 is constant within patient) gives ESS ~2,000. For SCORE2 coefficients the relevant n is ~2,000 patients; for segment-level geometric effects it is higher. The ICC of new plaque within patient should be estimated from the data (a null mixed-effects logistic model) and reported.
- The 10-year incident/progressed-plaque event count per segment is the critical number; per Riley, events, not rows, drive the requirement. Compute pmsampsize for the SCORE2+baseline-plaque LR baseline using an anticipated C and prevalence; treat the NN as needing substantially more.
- Learning curves (performance vs number of training patients, sampled by patient) are the practical ML analogue and should be reported for each model class.

### Gaps
- No published pmsampsize extension for clustered multilevel binary outcomes was found in this search; the design-effect adjustment is an approximation.
- Riley 2025 Lancet Digital Health specifics (numbers, recommendations) were not retrievable.

## 3. Self-supervised / transfer pretraining on unlabelled coronary data (ImageCAS)

### Takeaway
Pretraining on unlabelled data improves label efficiency in medical imaging, but graph pretraining done naively often causes negative transfer; any ImageCAS pretraining must be tested as an ablation (pretrained vs from-scratch vs engineered features) under the same CV.

### Cited Findings
- Krishnan, Rajpurkar, Topol 2022 (Nat Biomed Eng) review: self-supervised learning on unlabelled medical images, signals, EHR reduces annotation needs for expert-level performance. — [Harvard DBMI record](https://dbmi.hms.harvard.edu/publication/self-supervised-learning-medicine-healthcare)
- Hu et al. 2020 (ICLR) "Strategies for Pre-training Graph Neural Networks": naive graph-level or node-level pretraining often gives negative transfer (worse than no pretraining) on many downstream tasks; combining node-level and graph-level pretraining avoided negative transfer and gave up to 9.4% absolute ROC-AUC gains (molecular/protein benchmarks). — [Hu et al. 2020, ICLR](https://iclr.cc/virtual_2020/poster_HJlWWJSFDH.html); [arXiv 1905.12265](https://arxiv.org/abs/1905.12265v2)

### Inferences
- Feasible pretext tasks on ImageCAS without outcomes: masked node/edge attribute reconstruction on the centerline graph (radius, curvature), contrastive learning across augmented subtrees, predicting segment labels/topology, lumen-radius reconstruction. Hu et al. suggest combining local (node/segment) and global (tree) objectives.
- Domain shift: ImageCAS (Chinese hospital, mixed disease, different scanners/protocol) vs CGPS (Danish general population). Pretraining helps only if geometry distributions overlap; check distribution of engineered features across datasets before relying on it.
- With ~2000 labelled patients, frozen pretrained embeddings fed to LR/GBDT is a cheap, lower-variance alternative to full fine-tuning and should be one arm of the ablation.

### Gaps
- No study found that pretrains on coronary centerline trees or lumen meshes and transfers to plaque prediction; this would be novel. Evidence is extrapolated from molecular-graph and general medical-imaging SSL.
- No quantified evidence found on how many labelled patients are needed before pretraining stops helping in 3D vascular data.

## 4. Regularisation, ensembling, tuning under nested grouped CV; patient-level leakage

### Takeaway
All splitting must be by patient (GroupKFold), with hyperparameter tuning in an inner grouped loop and every preprocessing step fitted inside folds; non-nested tuning gives optimistic, sometimes chance-level-in-reality estimates.

### Cited Findings
- Varma & Simon 2006 (BMC Bioinformatics): CV error of a classifier tuned by the same CV is substantially biased; on independent data the "optimised" classifiers performed no better than chance in their setting; nested CV gave an estimate close to independent test-set error. — [Varma & Simon 2006 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC1397873)
- Kapoor & Narayanan 2023: taxonomy of eight leakage types (including no proper train/test separation, preprocessing on full data, duplicates/non-independence between train and test, temporal leakage); 294 affected papers across 17 fields; proposes model info sheets. — [Kapoor & Narayanan 2023, Patterns (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10499856)
- Repeated-measures data: if CV ignores participant structure, information leaks between folds and inflates performance; patient-grouped CV measures prediction on new patients, which is the clinically relevant quantity; imputation and standardisation must be fitted inside each outer fold. — [JMIR AI 2026 (peer-reviewed, details from search snippet)](https://ai.jmir.org/2026/1/e87728/PDF); [bioLeak CRAN vignette](https://archive.linux.duke.edu/cran/web/packages/bioLeak/vignettes/bioLeak-intro.html)
- Riley et al. criteria imply penalisation cannot rescue an undersized dataset; Martin et al. note penalisation/shrinkage produced unreliable models especially at small n. — [Martin et al. 2025 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12106283/)
- Shwartz-Ziv & Armon: NN+XGBoost ensembles outperform either alone; TabArena: tuning plus ensembling is what lifts MLPs to top rank. — [arXiv 2106.03253](https://arxiv.org/abs/2106.03253); [arXiv 2506.16791 (preprint)](https://arxiv.org/abs/2506.16791)

### Inferences
- Recommended regime: outer loop 5-fold GroupKFold by patient (repeated, e.g. 5x5, stratified by patient-level event status), inner GroupKFold for tuning with a fixed budget per model class (same number of trials for LR, GBDT, NN for fairness, per Grinsztajn's budget-aware protocol). Report outer-fold mean and spread.
- Leakage hazards specific to this project: (a) segments of one patient in train and test; (b) normalisation of geometric features or SCORE2 fitted on all data; (c) segment-label conventions or centerline extraction parameters tuned on the whole cohort while looking at outcomes; (d) ImageCAS pretraining is safe (no CGPS data), but any self-supervised pretraining on CGPS scans must be inside folds or on scans excluded from test folds; (e) baseline plaque read by the same readers as follow-up (measurement dependence; report, cannot fix).
- NN regularisation for small n: weight decay, dropout, early stopping on an inner grouped validation split, small architectures, and ensembling across seeds/folds (also gives uncertainty, Section 6). Consider a held-out temporal or site split if CGPS allows, as a stronger check than CV.
- Final model: retrain on all data with hyperparameters selected by inner CV; performance claimed is the outer-CV estimate (optimism-corrected), with bootstrap instability analysis per Riley & Collins.

### Gaps
- No primary source found quantifying the optimism from ignoring patient grouping specifically for segment-level coronary data.

## 5. Evaluation: discrimination, calibration, DCA, incremental value, baselines, ablations, reporting

### Takeaway
Report discrimination at both segment and patient level, calibration (calibration-in-the-large, slope, flexible curve), and net benefit by decision curve analysis; assess incremental value by delta AUC with CIs and likelihood-ratio-type tests rather than NRI; benchmark against SCORE2-only and SCORE2+baseline-plaque models; follow TRIPOD+AI and self-audit with PROBAST+AI.

### Cited Findings
- Van Calster et al. 2019 (BMC Medicine) "Calibration: the Achilles heel of predictive analytics": poorly calibrated algorithms can mislead and harm decision-making; calibration must be assessed at validation and is threatened by complexity relative to sample size. — [Van Calster et al. 2019 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6912996)
- Vickers, Van Calster, Steyerberg 2019 (Diagn Progn Res): step-by-step DCA interpretation; net benefit across threshold probabilities; read y-axis as "benefit", x-axis as "preference". — [Vickers et al. 2019 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6777022)
- NRI critiques: NRI can be biased even with independent validation data; in simulation, false-positive conclusions from NRI were 63.0% in training data and 18.8% to 34.4% in test data, vs rare for delta AUC and ~5% for the likelihood ratio test (Pepe et al.). Kerr et al. 2014 (Epidemiology): report event and non-event NRI separately; avoid NRI with three or more risk categories. — [Pepe et al. (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4615606); [Kerr et al. 2014 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3982889); [Kerr NRI PDF](https://cnsgenomics.com/data/teaching/SISG/module_10/Mod10_Session7Naomi/Resources/Kerr_NetReclassIndex.pdf)
- TRIPOD+AI (Collins et al., BMJ, 16 April 2024): 27-item checklist plus TRIPOD+AI for Abstracts; covers regression and ML; development, validation or both; supersedes TRIPOD 2015. — [Collins et al. 2024 (Oxford ORA)](https://ora.ox.ac.uk/objects/uuid:414e5fb8-5575-4b67-b94d-a0833a7cc58a/files/smp48sf448)
- PROBAST+AI (BMJ, 24 March 2025): 16 signalling questions for model development (quality and applicability) and 18 for model evaluation (risk of bias and applicability); applies to regression and AI models. — [PROBAST+AI (Oxford ORA)](https://ora.ox.ac.uk/objects/uuid:8b15c087-459b-43fa-ad03-1f66ed6ba370); [Birmingham record](https://research.birmingham.ac.uk/en/publications/probastai-an-updated-quality-risk-of-bias-and-applicability-asses/)
- Riley & Collins 2023: calibration and decision-curve instability plots across bootstrap models as part of evaluation. — [Riley & Collins 2023 (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10952221/)

### Inferences
- Model ladder (all under identical outer folds): M0 SCORE2 only (patient-level risk broadcast to segments, or with segment-type indicator); M1 SCORE2 + baseline segment plaque; M2 M1 + engineered geometry (curvature, bifurcation angle, daughter ratio, volume-to-mass) in penalised LR and GBDT; M3 NN with learned tree/lumen representation; M3b M3 with ImageCAS pretraining. Primary comparison M3 vs M2, secondary M2 vs M1 (does geometry add anything at all).
- Ablations for the NN: remove graph topology (segment-independent MLP on same features), remove lumen input, remove baseline plaque, pretraining on/off, ensemble size.
- Segment AUC is inflated by between-patient risk differences; also report patient-level AUC (any new plaque, via max or 1 - prod(1-p) aggregation) and within-patient discrimination (e.g. AUC computed within patients and averaged, or conditional C) to show whether geometry localises plaque beyond identifying high-risk persons. Patient-level CIs must use cluster (patient) bootstrap.
- Delta AUC with patient-bootstrap CIs; likelihood ratio or deviance comparison for nested regression models; NRI, if reported at all, as event/non-event components only.
- Decision threshold choice for DCA must be justified clinically (e.g. thresholds where segment-targeted follow-up imaging would change); since the clinical action is patient-level, DCA should probably be at patient level.

### Gaps
- No standard found for within-patient (conditional) discrimination metrics in segment-level coronary prediction; the specific metric choice needs justification in the thesis.
- TRIPOD+AI item list not retrieved in detail (only count of 27 items).

## 6. Uncertainty quantification

### Takeaway
Deep ensembles are the strongest simple baseline for predictive uncertainty and hold up best under dataset shift; MC dropout is cheaper but generally weaker. For a clinical prediction thesis, report both model-level uncertainty (bootstrap instability, ensemble spread) and population-level CIs on metrics.

### Cited Findings
- Lakshminarayanan, Pritzel, Blundell 2017 (NeurIPS): deep ensembles are simple, parallelisable, need little tuning, and give calibrated uncertainty as good as or better than approximate Bayesian NNs, with higher uncertainty on out-of-distribution inputs. — [Lakshminarayanan et al. 2017, NeurIPS](https://proceedings.neurips.cc/paper/2017/hash/9ef2ed4b7fd2c810847ffa5fa85bce38-Abstract.html)
- Ovadia et al. 2019 (NeurIPS): large benchmark of UQ under dataset shift; calibration degrades with shift; post-hoc calibration (temperature scaling) falls short under shift; methods that marginalise over models (deep ensembles) were surprisingly strong across tasks. — [Ovadia et al. 2019, NeurIPS](https://papers.nips.cc/paper/2019/hash/8558cb408c1d76621371888657d2eb1d-Abstract.html)
- Uncertainty of individual risk estimates from clinical prediction models (rationale, challenges, approaches) reviewed in BMJ/PMC 2025 companion literature; Riley & Collins recommend bootstrap instability plots and MAPE as the routine way to show individual-risk uncertainty. — [Uncertainty of risk estimates (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12128882/); [Riley & Collins 2023 (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10952221/)

### Inferences
- Practical: train the NN as an ensemble of 5 to 10 seeds per outer fold (also improves accuracy per Shwartz-Ziv/TabArena); report ensemble mean as the prediction and the per-segment standard deviation/entropy as uncertainty. Evaluate whether uncertainty is informative: AUC/calibration stratified by uncertainty quantile, or selective-prediction curves.
- For LR/GBDT, use bootstrap refits (Riley & Collins) so uncertainty is compared on equal terms across model classes.
- ImageCAS to CGPS is a shift; Ovadia suggests expecting calibration loss when transferring pretrained components, so recalibrate (in inner folds) and report calibration after transfer.

### Gaps
- No clinical-cohort study found that compares deep ensembles vs MC dropout specifically on small (n~2000) tabular/graph clinical data.
- The 2025 "uncertainty of risk estimates" paper's authorship and specific recommendations were not retrieved in full.
