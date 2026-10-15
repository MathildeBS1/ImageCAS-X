# ML / DL vs penalised regression for predicting incident or progressing coronary plaque at modest sample sizes

Context: the thesis predicts new plaque in plaque-free LAD/CX/RCA trunks from baseline geometry plus risk factors. It has about 2,100 participants (up to about 6,000 vessels) and probably a few hundred to about 1,000 events. Web access was limited: several primary full texts (van der Ploeg 2014, PARADIGM ML JAHA 2020, the 2024 curvature/haemodynamics paper) were blocked (403, login redirect or bot check). Their numbers are therefore unverified and listed under Gaps.

## 1. Systematic reviews / meta-analyses: ML vs logistic regression

### Takeaway
In clinical prediction on low-dimensional tabular data, ML shows no AUC gain over logistic regression once comparisons are at low risk of bias. The apparent ML advantage comes almost entirely from high-risk-of-bias comparisons. In cardiovascular primary prevention, the pooled ML gain over traditional risk scores is about 0.01 in C-statistic, and most of those models are at high risk of bias.

### Cited Findings
- **Christodoulou et al. 2019 (J Clin Epidemiol), 71 studies, 282 comparisons.**
  - Low-risk-of-bias comparisons (n=145): the logit(AUC) difference between LR and ML was 0.00 (95% CI −0.18 to 0.18).
  - High-risk-of-bias comparisons (n=137): logit(AUC) was 0.34 higher for ML (0.20–0.47).
  - Validation procedures were potentially biased in 68% of studies, and calibration was not addressed in 79%. — [Christodoulou 2019, JCE](https://www.sciencedirect.com/science/article/abs/pii/S0895435618310813); [Birmingham repository](https://research.birmingham.ac.uk/en/publications/a-systematic-review-shows-no-performance-benefit-of-machine-learn/)
- **Liu et al. 2023 (Eur Heart J Qual Care Clin Outcomes), 16 studies, ML vs traditional ASCVD risk scores in primary prevention.**
  - Pooled C-statistic: top-performing ML 0.773 (0.740–0.806) vs traditional scores 0.759 (0.726–0.792), a difference of about 0.014.
  - External-validation subgroup (only 2 studies): 0.797 vs 0.769.
  - 81% (55/68) of ML models were at high PROBAST risk of bias, mainly in the analysis domain. Calibration could not be pooled because it was poorly reported.
  - Caveat: the comparator is published risk scores, not a regression refitted to the same data. That favours ML. — [Liu 2023, EHJ-QCCO](https://academic.oup.com/ehjqcco/article/9/4/310/7069320)
- **Orthopaedic sports medicine SR/MA (2025/26).** It repeats the Christodoulou pattern: for 125 low-risk-of-bias comparisons the logit(AUC) difference was 0.00 (−0.18 to 0.18). The abstract is ambiguous about the sign. — [PubMed 41747825](https://pubmed.ncbi.nlm.nih.gov/41747825/)
- **Kawasaki disease IVIG-resistance review using PROBAST+AI.**
  - All included studies were at high risk of bias.
  - Pooled external-validation AUC was about 0.76 for ML vs 0.75 for LR. — [PMC13393907](https://pmc.ncbi.nlm.nih.gov/articles/PMC13393907/)

### Inferences
- The thesis predictors are structured, low-dimensional and modest in number: risk factors plus summary geometry. That is exactly the setting where these reviews find no ML gain. A realistic prior for gradient boosting or random forests over penalised logistic or Cox regression on the same predictors is a ΔAUC of about 0 to 0.02.
- Any larger gain should be treated as suspicious. Likely causes would be leakage, for example vessels from the same patient appearing in both train and test, or an unfair comparator, until proven otherwise.
- A gain on this scale cannot be detected with a few hundred events. The CI of the ΔAUC will be wider than ±0.02.

### Gaps
- No review I found stratified the ML−LR gap formally by number of events or sample size. The dependence on n is inferred from the sample-size literature in section 2.
- I did not retrieve newer cross-domain meta-analyses (2023–2026) beyond those above.

## 2. Sample-size and data requirements of ML

### Takeaway
Flexible ML needs substantially more events than regression to give stable, well-calibrated predictions. The Riley minimum sample-size criteria were built for (penalised) regression and should be treated as a lower bound for ML. ML studies routinely fall short even of that lower bound.

### Cited Findings
- **Van der Ploeg, Austin & Steyerberg 2014**, "Modern modelling techniques are data hungry: a simulation study for predicting dichotomous endpoints", BMC Med Res Methodol 14:137. It is cited as the canonical evidence that ML needs more data than LR. — [cited in statistical primer, PMC12106283](https://pmc.ncbi.nlm.nih.gov/articles/PMC12106283/)
- **Statistical primer (2025) on the Riley criteria.**
  - The criteria are "tailored for (penalized) regression approaches" but "can also be used for machine learning algorithms".
  - ML "will likely require an even larger sample size due to a larger number of predictors", plus non-linearity and interactions.
  - Recommended targets: shrinkage ≥0.9 (≤10% overfitting), and with no prior information an R² of 15% of the maximum (Nagelkerke 0.15).
  - The minimum n is the maximum across the criteria (overall risk precision, shrinkage, optimism).
  - EPV rules of thumb "should be avoided". — [PMC12106283](https://pmc.ncbi.nlm.nih.gov/articles/PMC12106283/)
- **Tsegaye et al. 2025 (J Clin Epidemiol 180), oncology ML binary-outcome models, 36 studies.**
  - Only 1 study justified its sample size.
  - The minimum required n could be computed for 17 studies, and only 5 met it.
  - The median shortfall was 302 participants with the event (range from surplus up to 2,298).
  - The authors argue ML needs more than the regression minimum, so the shortfall is understated. — [ORA Oxford record](https://ora.ox.ac.uk/objects/uuid:059fe91c-f405-4231-a634-8b26979389f0); [NDORMS](https://www.ndorms.ox.ac.uk/publication/2078785)
- **Riley et al. 2025 (Lancet Digital Health)**, "Importance of sample size on the quality and utility of AI-based prediction models for healthcare", with Collins as co-author. Found as a citation only. — [cited in search result list, PMC12106283](https://pmc.ncbi.nlm.nih.gov/articles/PMC12106283/)
- **Sequential sample-size calculations and learning curves (J Clin Epidemiol 2025).** Recommends monitoring learning curves during development to safeguard robustness. — [JCE 2025](https://www.jclinepi.com/article/S0895-4356(25)00450-0/fulltext)
- **Practical ML guide for clinicians (arXiv 2006.15069).**
  - Deep neural nets "will often require thousands of patients to converge", whereas LR "may achieve stable results with only a few hundreds".
  - It advises against ML development on cohorts with fewer than 100 positive cases. — [arXiv 2006.15069](https://arxiv.org/pdf/2006.15069)
- **Riley et al. 2021 on bootstrap variability.** Even models at the minimum sample size show substantial variability in tuning parameters and performance. — [PMC8649413](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8649413/)

### Inferences
- With roughly 300–1,000 events, a penalised regression with about 15–30 parameters, including splines for key geometry, is likely to meet the Riley criteria. pmsampsize can be run to check this for the actual event rate.
- Tree ensembles on the same predictors are feasible but will be unstable at the low end, around 300 events.
- Deep models on 1D curvature profiles, point clouds or CT images are well below typical data needs at the patient level. Thousands of patients and events are typical.
- The vessel-level n (about 6,000) does not multiply the information content. Vessels within a patient are correlated, so the effective n lies between the number of patients and the number of vessels. Events, not vessels, drive the requirement.
- A learning curve, plotting performance against training-set fraction for regression vs boosting vs DL, is a cheap and persuasive thesis figure. It shows directly whether the flexible models are still data-limited.

### Gaps
- **Exact van der Ploeg 2014 numbers could not be verified** (publisher page blocked). From memory: LR needed about 20–50 EPV for stable AUC/optimism, while RF, SVM and NN needed more than 200 EPV, and CART was also very data-hungry. Verify against the original before citing.
- No ML-specific closed-form sample-size method was found. The literature defers to the regression criteria as a minimum plus simulation or learning curves.

## 3. Cardiac-CT-specific evidence: ML for plaque progression, CAC and high-risk plaque; geometry-based plaque prediction

### Takeaway
CCTA ML studies of plaque progression and high-risk plaque exist, notably PARADIGM (n≈1,083) and SCOT-HEART ML (n=1,769). Their gains mainly come from adding quantitative baseline plaque features, not from the algorithm.

ML on clinical risk factors alone gives only modest AUCs: about 0.75 for low-attenuation plaque (LAP) burden in SCOT-HEART, which did not beat ASSIGN significantly.

I found **no peer-reviewed longitudinal study that uses CCTA-derived coronary geometry (curvature, tortuosity, bifurcation angle, shape PCA, point-cloud or graph networks) to predict where new plaque develops in plaque-free segments.** This is a genuine gap the thesis would fill. Geometric DL work so far targets wall shear stress (WSS) surrogates, not plaque outcomes.

### Cited Findings

**Plaque progression and high-risk plaque on CCTA**
- **PARADIGM ML (JAHA 2020).**
  - n=1,083 with serial CCTA.
  - Rapid plaque progression was defined as an annual increase in percent atheroma volume of at least 1.0%.
  - The ML model combined clinical, lab, and qualitative and quantitative CCTA features. Quantitative plaque features were the most important predictors. — [JAHA 2020](https://www.ahajournals.org/doi/10.1161/JAHA.119.013958); summarised in [JACC State-of-the-Art 2020](https://www.jacc.org/doi/10.1016/j.jacc.2020.06.076)
- **PARADIGM practical risk score (Eur Radiol 2023), non-ML.** Progression of non-obstructive plaque had a C-statistic of 0.732 in derivation and 0.668 in validation. This illustrates the optimism gap and the ceiling of conventional models for progression. — [Eur Radiol 2023](https://link.springer.com/article/10.1007/s00330-023-09880-x)
- **SCOT-HEART ML (Williams et al., Open Heart 2025).**
  - Design and data:
    - n=1,769: 1,416 for training and 353 held out.
    - XGBoost with grid search and 10-fold CV.
    - The outcomes are cross-sectional and prevalent: any CAD in 1,123 patients (64%), and increased LAP burden (>4%) in 907 (51%).
  - Results:
    - Any CAD: AUC 0.80 vs ASSIGN 0.75 (p=0.004).
    - LAP: AUC 0.75 vs ASSIGN 0.72 (p=0.08), so no significant gain.
  - Limitations:
    - No refitted logistic regression comparator was reported.
    - Validation was internal only.
  - The authors state it "was not possible to improve the prediction of an increased LAP burden based on clinical factors alone". — [PMC12406813](https://pmc.ncbi.nlm.nih.gov/articles/PMC12406813/)

**Other ML progression studies**
- **Pericoronary adipose tissue radiomics ML for plaque progression (2025).** n=97, retrospective, random forest and other models. This is a typical small-n radiomics study at high risk of overfitting. — [PMC11872547](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11872547/)
- **CAC progression ML (Med Biol Eng Comput 2026), West China Hospital.** n=2,579. Details were not retrieved. — [Springer 2026](https://link.springer.com/article/10.1007/s11517-026-03647-4)
- **Plasma proteomics for plaque progression.** Proteomics improved prediction of coronary plaque progression. Details were not retrieved. — [PMC11879226](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11879226/)

**Geometry and haemodynamics**
- **PREDICTION study (Stone et al., Circulation 2012).**
  - 506 ACS patients had 3-vessel IVUS plus angiographic profiling of endothelial shear stress (ESS). 329 had repeat imaging at 6–10 months.
  - Low ESS segments showed increased plaque thickness and expansive remodelling, and predicted the need for PCI at 12 months.
  - This is the main longitudinal evidence that local geometry and flow predict local plaque change. It used invasive imaging, not CCTA. — [ClinicalTrials NCT01316159](https://clinicaltrials.gov/study/NCT01316159); [TCTMD](https://www.tctmd.com/news/endothelial-shear-stress-works-prediction-tool)
- **Coronary curvature and haemodynamics (2024).** Left coronary tree models suggested that tortuosity/TSVI, curvature and oscillatory shear index (OSI) are associated with plaque onset, while low TAESS and high RRT are associated with moderate-to-severe progression. The design appears cross-sectional. — [PMC11416812](https://pmc.ncbi.nlm.nih.gov/articles/PMC11416812/)
- **Bifurcation angle (dual-source CT, n=106).** A wider LAD–LCx angle predicted significant left coronary stenosis and was related to non-calcified lesions. This is cross-sectional. — [PMC5367806](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5367806/)
- **2026 review.** CCTA plus CFD studies consistently show non-calcified and lipid-rich plaque accumulating at lateral walls and outer curvatures of bifurcations. — [Medical Sciences 2026 review](https://doi.org/10.3390/medsci14060639); [JCM 2026 bifurcation review](https://pmc.ncbi.nlm.nih.gov/articles/PMC13302630/)

**Geometric deep learning on coronary geometry**
- **GReAT (Suk, Wentzel, Wolterink et al., MICCAI/arXiv 2025).**
  - A transformer was pre-trained on 8,449 vessel point clouds, then used to classify time-averaged WSS (low/mid/high) on coronaries in a 49-patient trial.
  - It shows that geometric DL at small clinical n relies on large-scale self-supervised pre-training. — [arXiv 2508.19030](https://arxiv.org/pdf/2508.19030)
- **Other WSS surrogates.**
  - Mesh CNNs and SE(3)-equivariant mesh networks. — [arXiv 2109.04797](https://arxiv.org/pdf/2109.04797); [arXiv 2212.05023](https://arxiv.org/pdf/2212.05023)
  - A physics-informed GNN trained on 1,000 synthetic geometries derived from 40 patients. — [Sci Rep 2026](https://www.nature.com/articles/s41598-026-47410-z)
  - Point-cloud TAWSS prediction on idealised bifurcations. — [PMC11920710](https://pmc.ncbi.nlm.nih.gov/articles/PMC11920710/)
- **Patents (HeartFlow-type).** "Predicting location, onset, and/or change of coronary lesions" describes centreline curvature, torsion, bifurcation-angle and multiphase deformation features as ML inputs. No peer-reviewed performance is reported. — [US patent 9805463](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9805463)
- **Angiographic tortuosity ML.** RCA tortuosity was quantified from 38,691 invasive angiograms. No link to plaque was reported. — [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)

### Inferences
- The closest CCTA analogues (PARADIGM, SCOT-HEART) show:
  - Clinical-only models reach AUCs of about 0.70–0.75 for plaque outcomes.
  - Quantitative imaging features add more than switching from regression to boosting does.
- For the thesis, the scientific question is whether baseline geometry adds information beyond risk factors. This is best answered first with penalised regression, using ΔAUC, ΔNRI/IDI, calibration and decision curves. Algorithm choice is secondary.
- Because geometry-to-future-plaque prediction in plaque-free trunks has no CCTA precedent, a well-done regression analysis is itself novel. Flexible or deep geometry models are exploratory.
- Geometric DL (point cloud or graph) at about 2,000 patients would likely need pre-training (GReAT-style) or a strong inductive bias. It suits an exploratory role, and possibly WSS-surrogate features fed into the regression.

### Gaps
- PARADIGM ML AUC values, event count and the comparator regression could not be retrieved (403).
- I found no MESA or CONFIRM ML study on plaque or CAC progression with verifiable numbers in this search. MESA ML (Ambale-Venkatesh 2017) concerns events, not plaque progression.
- No ICONIC ML plaque-location study was retrieved.
- No peer-reviewed study was found using shape PCA/FPCA of coronary centrelines to predict plaque development.

## 4. Recommended protocol for a fair flexible-vs-regression comparison

### Takeaway
The reviews show that ML "wins" come mainly from biased comparisons: inadequate validation, uncalibrated outputs, and unequal tuning or predictors. A fair protocol therefore needs:
- identical predictors and outcome definitions;
- grouped (by participant) nested cross-validation with equal tuning effort;
- calibration and decision-curve reporting alongside AUC;
- negative controls, i.e. permuted or shuffled geometry.

### Cited Findings
- Christodoulou 2019 found bias in validation procedures in 68% of comparison studies and no calibration in 79%. These are the main sources of spurious ML advantage. — [JCE 2019](https://www.sciencedirect.com/science/article/abs/pii/S0895435618310813)
- In Liu 2023, the high risk of bias was concentrated in the analysis domain: poor discrimination and calibration reporting, and missing-data handling. — [EHJ-QCCO 2023](https://academic.oup.com/ehjqcco/article/9/4/310/7069320)
- Tuning parameters and performance estimates vary substantially across bootstrap samples near minimum sample sizes. The authors recommend quantifying this instability. — [PMC8649413](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8649413/)
- Learning curves and sequential sample-size checks are recommended during development. — [JCE 2025](https://www.jclinepi.com/article/S0895-4356(25)00450-0/fulltext)

### Inferences (protocol proposal; not individually sourced)
1. **Unit and splitting.** Model at the vessel level with participant-grouped folds (GroupKFold or stratified group k-fold by study_id). Use nested CV: an inner loop for tuning (penalty λ or spline df for regression; depth, learning rate and number of trees for XGBoost) and an outer loop for performance. Repeat it, for example 5×5 or 10×5, to get variance.
2. **Same inputs.** Feed regression and ML the same predictor set. Give the regression a fair chance to model non-linearity (restricted cubic splines) and pre-specified interactions, such as vessel × geometry. Then the comparison isolates the algorithm, not feature engineering.
3. **Outcome handling.** With about 10 years of follow-up, censoring and death, prefer:
   - penalised Cox or discrete-time logistic regression, against
   - random survival forest or gradient-boosted survival (XGBoost Cox/AFT, or DeepSurv as exploratory).
   
   If the outcome is binary at FU imaging, use penalised logistic vs XGBoost classifier.
4. **Metrics.**
   - Discrimination: AUC or C-index, with paired ΔAUC and a bootstrap CI.
   - Calibration: calibration slope and intercept, smoothed calibration curves, and the Brier score.
   - Clinical utility: decision curve analysis and net benefit.
   - Reclassification (NRI/IDI) only as secondary.
5. **Added-value test.** Compare risk factors only vs risk factors plus geometry within each model class. This is the scientific contrast, and it is more important than regression vs boosting.
6. **Negative controls.**
   - Permute the geometry features or curvature profiles across vessels or patients while keeping risk factors intact. Any "gain" should vanish.
   - Shuffle profiles within a vessel class (e.g. LAD to LAD) to check for vessel-identity leakage.
   - Run permutation tests of the ΔAUC.
7. **1D profile baselines.** Before any CNN or late-fusion network on curvature or diameter profiles, run three baselines:
   - summary statistics (mean, max, percentiles of curvature, and tortuosity) into the regression;
   - FPCA scores into the regression;
   - MiniRocket or ROCKET random-convolution features into a ridge or logistic classifier.
   
   A deep network is only worth reporting if it beats these. Late fusion means concatenating the profile embedding with the risk factors.
8. **Reporting.** Follow TRIPOD+AI and PROBAST+AI.

### Gaps
- No source was retrieved here that specifically benchmarks MiniRocket on vascular centreline profiles, or that sets out a consensus protocol for grouped-CV comparisons in multi-vessel data. Items 1, 6 and 7 are methodological best practice, not cited findings.
- TRIPOD+AI (Collins et al., BMJ 2024) was not fetched in this session. Confirm the citation.

## 5. Interpretability (SHAP) and pitfalls with correlated geometry features

### Takeaway
SHAP is useful for describing a fitted boosted model, but it is unreliable for ranking correlated features. Curvature, tortuosity, torsion, length and diameter are strongly inter-correlated. SHAP rankings among them can flip with resampling and should not be read causally. Present grouped or partial-dependence summaries and check stability across CV folds.

### Cited Findings
- SHAP "fails to differentiate between causality and correlation, often misattributing feature importance when features are highly correlated" (Causal SHAP preprint, 2025). — [arXiv 2509.00846](https://arxiv.org/pdf/2509.00846)
- **2026 healthcare XAI review.**
  - A high SHAP value may signal a proxy rather than a cause.
  - SHAP assumes independent feature contributions.
  - Attributions are not calibrated across subgroups.
  - It recommends partial dependence plots for population-level relationships. — [arXiv 2608.07522](https://arxiv.org/pdf/2608.07522)
- A 2026 preprint argues that under collinearity no feature ranking can be faithful, stable and complete at once, and that retraining with a different seed can invert the top feature. This is unreviewed. — [arXiv 2605.21492](https://arxiv.org/pdf/2605.21492)
- SHAP does not fundamentally explain what the model does internally. — [arXiv 2208.12814](https://arxiv.org/pdf/2208.12814)
- Class-dependent explanation methods, including SHAP, can leak information about the selected class (Jethani et al., AISTATS 2023). — [PMLR v206](https://proceedings.mlr.press/v206/jethani23a.html)

### Inferences
- **Feature groups.** Group geometry features into blocks and report group-level importance, for example grouped permutation importance or the summed SHAP of the block:
  - curvature block
  - tortuosity/torsion block
  - bifurcation block
  - size block
- **Stability.** Report the SHAP and permutation-importance spread across outer CV folds and bootstrap refits.
- **Main effect estimates.** Use the penalised regression with splines (odds or hazard ratios per SD, with effect plots) as the primary interpretable estimate. Use SHAP only as a secondary description of the boosted model.
- **Correlation structure.** Show a correlation heatmap of geometry features alongside any SHAP plot.

### Gaps
- No peer-reviewed study was found that quantifies SHAP instability specifically for coronary geometry features.

## Overall role recommendation (synthesis; inferential)

| Model class | Suggested role | Rationale |
|---|---|---|
| Penalised logistic/Cox (ridge/elastic net) with splines for geometry; risk factors ± geometry | **Primary** | Meets Riley sample-size criteria at a few hundred events. Low-risk-of-bias evidence shows ML gives no gain on tabular data. Interpretable added-value test. |
| Gradient boosting (XGBoost/LightGBM) / random forest on same predictors | **Secondary** (sensitivity / benchmark) | Expected ΔAUC about 0–0.02. Use to check for missed non-linearity or interactions. Needs grouped nested CV and calibration. |
| Random survival forest / boosted survival | **Secondary** if time-to-event framing is used | Same logic. Data-hungry, and calibration often poor. |
| FPCA / MiniRocket on 1D curvature/diameter profiles + regression | **Secondary / exploratory** | Cheap, strong baselines for profile information. Required before any deep profile model. |
| Late-fusion NN (profile CNN/1D transformer + risk factors) | **Exploratory** | Well below typical DL data needs. Must beat MiniRocket/FPCA and survive shuffled-profile controls. |
| Point-cloud / graph / CT-image deep models | **Exploratory only** (or as feature extractors/WSS surrogates) | The only coronary geometric-DL precedents predict WSS at n≈49 with large pre-training. No plaque-outcome precedent. |
