# Gradient-boosted trees (XGBoost etc.) vs penalized logistic regression for new-plaque risk in Herlev–Østerbro

Thesis setting assumed throughout: plaque-free at baseline, binary new plaque at follow-up per artery domain (LM, LAD, LCx, RCA); ~5-10 risk factors + ~5-15 geometric features (so ~10-25 candidate predictors, more with splines/dummies); n a few hundred to ~1000; events tens to low hundreds per domain. Implied events per candidate predictor (EPP/EPV) is roughly 1-10, i.e. at or below the range where even regression needs penalization.

## 1. Empirical head-to-head evidence: does ML beat LR on clinical tabular data?

### Takeaway
In clinical prediction with modest numbers of predictors, methodologically sound comparisons find no discrimination gain for ML over logistic regression; apparent gains concentrate in studies with high risk of bias. The tabular-ML benchmarks that crown XGBoost compare trees against deep learning, not against well-specified LR, and are run on data sets far larger than this cohort.

### Cited Findings
- Christodoulou et al. 2019 (J Clin Epidemiol 110:12-22): systematic review, 71 studies, 282 LR-vs-ML comparisons; median n 1,250, median 19 predictors, median 8 events per predictor. Low risk of bias comparisons (n=145): difference in logit(AUC) between LR and ML 0.00 (95% CI -0.18 to 0.18). High risk of bias comparisons (n=137): logit(AUC) 0.34 (0.20 to 0.47) higher for ML. Calibration not addressed in 56/71 (79%) studies; 68% had potential bias in validation procedures. [ORA record](https://ora.ox.ac.uk/objects/uuid:4167c905-5171-4fc7-b157-ff36d56a73db); [search summary of abstract](https://pesquisa.bvsalud.org/ses/resource/es/mdl-30763612)
- Most common ML methods in that review were classification trees, random forests, ANNs and SVMs (boosting was a minority), so the review is not a boosting-specific test. [BVS/Medline record](https://pesquisa.bvsalud.org/ses/resource/es/mdl-30763612)
- Grinsztajn, Oyallon & Varoquaux, NeurIPS 2022 (Datasets & Benchmarks): 45 tabular data sets; tree-based models (XGBoost, random forests) remain state of the art over deep learning on "medium-sized data (~10K samples)". [arXiv 2207.08815](https://arxiv.org/abs/2207.08815)
- Grinsztajn inclusion criteria explicitly removed data sets with < 3,000 samples or < 4 features, and truncated training sets to 10,000; they also removed "too easy" data sets (where a simple/linear model was nearly as good). [ar5iv full text](https://ar5iv.labs.arxiv.org/html/2207.08815)
- Shwartz-Ziv & Armon (arXiv 2021; Information Fusion 2022): XGBoost outperformed recent tabular deep models across data sets, including those the deep models were proposed on, and needed less tuning; best results often from an XGBoost + deep ensemble. [arXiv 2106.03253](https://arxiv.org/abs/2106.03253)
- Liu et al. 2024 meta-analysis (ML for CVD risk on EHR data): pooled AUC 0.865 for random forest and 0.847 for deep learning vs conventional risk scores, but heterogeneity I² > 99% and possible publication bias; comparator was existing risk scores, not refit regressions on the same data. [PMC11750195](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11750195/)

### Inferences
- The Grinsztajn/Shwartz-Ziv results are not evidence for XGBoost over LR in a cohort of a few hundred to ~1000: they excluded data sets under 3,000 samples and screened out data sets where linear models do well, and they benchmark trees against neural nets.
- Many published "ML wins" (including the 2024 CVD meta-analysis) compare a newly fitted ML model against an old fixed score; that conflates new data/new predictors with the algorithm. A fair test requires LR refit on the same predictors and same data.

### Gaps
- I did not find a 2023-2026 systematic review restricted to boosting-vs-penalized-LR at small n with low risk of bias; the Christodoulou 2019 result remains the reference point.
- Shwartz-Ziv & Armon journal version details (Information Fusion volume) not verified here; arXiv version cited.

## 2. Sample size, overfitting, calibration and instability at small n

### Takeaway
Tree ensembles are measurably more "data hungry" than LR, and especially more than penalized LR, for both discrimination stability and calibration. At the EPV this cohort will have (single digits per candidate predictor per domain), boosting would be in the regime where simulations show substantial optimism and miscalibration, and individual risk predictions would be unstable.

### Cited Findings
- van der Ploeg, Austin & Steyerberg 2014 (BMC Med Res Methodol 14:137): simulations based on three clinical cohorts (n 1,282 / 1,731 / 3,181; outcome rates 46.9%, 22.3%, 7.6%). RF, SVM and NN showed instability and high optimism even with >200 events per variable; modern methods "may need over 10 times as many events per variable" as LR to reach a stable AUC and small optimism. [PMC4289553](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289553)
- Austin, Lee & Wang 2024 (Diagn Progn Res 8:15), "The relative data hungriness of unpenalized and penalized logistic regression and ensemble-based machine learning methods: the case of calibration": Monte Carlo in AMI and heart-failure cohorts, EPV 10 to 200, six methods including stochastic gradient boosting. Ridge/lasso "displayed very low optimism even when the number of EPV was very low"; unpenalized LR plateaued around EPV ≥ 50; boosted trees showed moderate optimism (better than RF/bagging); RF and bagging most data hungry. Conclusion: penalized LR "substantially less data hungry" for calibration. [PMC11539735](https://pmc.ncbi.nlm.nih.gov/articles/PMC11539735)
- Austin et al. (same research line): LR on average had optimal calibration slopes; RF often produced predicted probabilities of 0 or 1 so a calibration slope could not be fitted. [PMC11539735](https://pmc.ncbi.nlm.nih.gov/articles/PMC11539735)
- Riley & Collins 2023 (Biometrical Journal, doi 10.1002/bimj.202200302), "Stability of clinical prediction models developed using statistical or machine learning methods": instability of estimated risks is often considerable at small n and manifests as miscalibration in new data. GUSTO-I case studies: mean absolute prediction error (MAPE) 0.0027 at n = 40,830 (2,851 events) vs 0.03 at n = 300 (21 events) for unpenalized LR. At n = 752 (53 events): 27 predictors LASSO MAPE 0.029 vs all-in 0.038; 7 predictors LASSO 0.019; random forest default 0.047, depth-limited (3) 0.019, Platt-recalibrated RF 0.045. [PMC10952221](https://pmc.ncbi.nlm.nih.gov/articles/PMC10952221/)
- Riley & Collins recommend: bootstrap the full model-building procedure (≥200, e.g. 1000 replicates); report prediction instability plots, MAPE, calibration and decision-curve instability plots; avoid default hyperparameters; make stability checks routine. [PMC10952221](https://pmc.ncbi.nlm.nih.gov/articles/PMC10952221/); [arXiv 2211.01061](https://arxiv.org/abs/2211.01061v1)
- The Riley & Collins n = 752 / 53-event scenario is the closest published analogue to a Herlev–Østerbro artery-domain model; there, an unconstrained tree ensemble was ~2.5x more unstable than LASSO and recalibration did not fix it. [PMC10952221](https://pmc.ncbi.nlm.nih.gov/articles/PMC10952221/)

### Inferences
- With tens to low hundreds of events per domain and 10-25 candidate predictors, EPV is ~1-10. Austin 2024 and van der Ploeg 2014 place boosting well outside its stable regime there, while ridge/lasso remain usable. Per-domain XGBoost on LM (presumably the rarest domain) is likely infeasible.
- Boosting needs hyperparameter tuning (depth, learning rate, n_trees, subsampling) by nested CV; with ~50 events, the tuning itself adds variance that the Riley/Collins bootstrap would expose.
- A pooled participant-level or vessel-level model (with domain as a covariate and clustering handled) raises the event count and is a stronger option than any per-domain ML model.

### Gaps
- Austin 2024 tested stochastic gradient boosting (gbm), not XGBoost/LightGBM/CatBoost specifically; no simulation found that isolates XGBoost with modern regularization at EPV < 10.
- Formal ML-specific sample size criteria (beyond Riley et al. pmsampsize criteria for regression) were not retrieved in this pass.

## 3. Interpretability for an association question ("does geometry add information?")

### Takeaway
XGBoost cannot directly give an incremental-value test for a feature family. SHAP and gain importance describe the fitted model, are unreliable with correlated features, and are not causal. The defensible ML version of the question is the same as for LR: fit with and without the geometric family under identical resampling and compare out-of-sample performance (ΔAUC, Δlog-loss/Brier, calibration, decision curves), with bootstrap uncertainty. Penalized LR does this more cheaply and also gives interpretable coefficients.

### Cited Findings
- Hooker, Mentch & Zhou 2021 (Statistics and Computing), "Unrestricted permutation forces extrapolation: variable importance requires at least one more model, or there is no free variable importance": permute-and-predict importance creates points far from the data, so the model extrapolates and the importance is unreliable; they argue importance needs refitting ("at least one more model") rather than permuting. [arXiv 1905.03151](https://arxiv.org/abs/1905.03151)
- SHAP can fail to recover ground-truth attributions when predictors are correlated, and makes correlations learned by the model transparent while disregarding causal structure, which can misattribute importance (evaluation of XAI on clinical prediction models). [arXiv 2306.11985](https://arxiv.org/pdf/2306.11985)
- Different models trained on the same clinical data can select different groups of correlated features, giving discrepant explanations. [arXiv 2311.16654](https://arxiv.org/pdf/2311.16654)
- Riley & Collins 2023 recommend instability checks for anything derived from the model, including at individual level; feature-level stability follows the same bootstrap logic. [PMC10952221](https://pmc.ncbi.nlm.nih.gov/articles/PMC10952221/)

### Inferences
- Geometric features are likely correlated with each other (curvature summaries, vessel length, dominance, lumen volume/mass) and with risk factors (age, sex, body size), which is exactly the setting where SHAP/permutation importance is least trustworthy.
- "Does family X add information" maps onto Hooker et al.'s refit recommendation (drop-the-family refit, i.e. leave-one-covariate-out), which works for any learner. It is a prediction question, not a causal one, in both LR and XGBoost.
- With LR the answer comes with a likelihood-ratio test of the geometry block, coefficient estimates with CIs, and a clinically readable model; XGBoost gives only the out-of-sample comparison, with more variance at this n.

### Gaps
- No peer-reviewed study found that compares SHAP-based and refit-based incremental-value conclusions on a small clinical cohort.

## 4. When boosting helps: nonlinearity and interactions vs splines in LR

### Takeaway
Boosting's advantage is automatic discovery of irregular nonlinearities and high-order interactions, which pays off with large n and many features. With ~20 predictors and few events, restricted cubic splines for continuous predictors plus a few prespecified interactions (e.g. geometry x age, x sex, x domain) capture plausible nonlinearity with far fewer effective parameters.

### Cited Findings
- Grinsztajn et al. attribute trees' advantage partly to their ability to learn irregular functions and their robustness to uninformative features, and evaluated on ≥3,000-sample data sets after removing data sets where simple models were nearly as good. [ar5iv full text](https://ar5iv.labs.arxiv.org/html/2207.08815)
- In clinical comparisons with low risk of bias (median 19 predictors, 8 events per predictor) the added flexibility produced no AUC gain over LR. [ORA record](https://ora.ox.ac.uk/objects/uuid:4167c905-5171-4fc7-b157-ff36d56a73db)
- Riley & Collins: a depth-3 random forest matched LASSO stability (MAPE 0.019 each) while default deep trees were unstable (0.047), showing that constraining trees towards low-order interactions is what makes them viable at small n. [PMC10952221](https://pmc.ncbi.nlm.nih.gov/articles/PMC10952221/)

### Inferences
- A shallow XGBoost (max_depth 1-2, strong shrinkage) is close to an additive/low-order-interaction model, i.e. to what spline-LR already represents; so a sensitivity XGBoost mainly serves as a check that LR has not missed a strong nonlinearity/interaction. If shallow XGBoost does not beat spline-LR out of sample, that is itself reportable evidence.

### Gaps
- No source found quantifying how often splines + selected interactions close the gap to boosting on small clinical data; the inference above is reasoning, not a cited result.

## 5. Precedent in cardiology / CCTA

### Takeaway
The CCTA ML papers that report gains (CONFIRM, MESA) had thousands to tens of thousands of patients, hundreds of variables, and often compared ML against fixed clinical scores rather than refit regressions on the same inputs. Where ML was compared within a modest cohort for a plaque endpoint (SCOT-HEART, n 1,769), boosting did not improve prediction of high-risk plaque burden beyond a risk score.

### Cited Findings
- Motwani et al. 2017 (Eur Heart J 38:500-507), CONFIRM: n = 10,030 suspected CAD, 745 deaths over 5 years; ML combining clinical + CCTA variables AUC 0.79 vs Framingham Risk Score 0.61, segment stenosis score 0.64, segment involvement score 0.64, Duke index 0.62. Comparators were existing scores, not a refit LR on the same variables. [Houston Methodist record](https://scholars.houstonmethodist.org/en/publications/machine-learning-for-prediction-of-all-cause-mortality-in-patient/)
- Al'Aref et al. 2020 (Eur Heart J 41:359-367), CONFIRM: XGBoost, 13,054 patients, 2,380 (18.2%) obstructive CAD; 80/20 split with 10-fold CV. AUC: ML + CACS 0.881, ML alone 0.773, CAD consortium clinical score 0.734, CACS alone 0.866, updated Diamond-Forrester 0.682. Note ML + CACS improved on CACS alone by only 0.015. [Yonsei repository](https://ir.ymlib.yonsei.ac.kr/handle/22282913/175325); [PMC7849944](https://pmc.ncbi.nlm.nih.gov/articles/PMC7849944)
- Ambale-Venkatesh et al. 2017 (Circ Res), MESA: random survival forests, 6,814 participants, 12-year follow-up, 735 candidate variables; imaging, ECG and biomarkers dominated the top-20 predictors over traditional risk factors; compared against standard risk scores. [IFCC summary](https://oslm.ifcc.org/publication/cardiovascular-event-prediction-by-machine-learning-the-multi-ethnic-study-of-atherosclerosis); [PMC5640485](https://pmc.ncbi.nlm.nih.gov/articles/PMC5640485)
- SCOT-HEART ML (n = 1,769): XGBoost with 10-fold CV and grid search predicted any CAD on CCTA with AUC 0.80 vs 0.75 for the 10-year CV risk score alone; for increased low-attenuation plaque burden, XGBoost performed similarly to the risk score and did not improve prediction from clinical factors. [PMC12406813](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12406813/)

### Inferences
- None of these precedents is a plaque-free, incident-plaque, per-artery design; all are 2-50x larger than Herlev–Østerbro's expected n, and the gains reported are mostly against fixed scores. They do not license XGBoost as primary analysis here.
- The SCOT-HEART null for plaque burden at n ~1,800 is the closest precedent and is a caution: boosting on clinical variables did not add for a plaque endpoint.

### Gaps
- MESA exact C-statistics for RSF vs refit Cox were not retrieved (PMC page blocked).
- No SCAPIS ML paper on incident/prevalent CCTA plaque with XGBoost was found in this pass; searches returned SCOT-HEART and CONFIRM instead.
- No published study found using XGBoost for incident plaque in initially plaque-free CCTA participants.

## 6. Reporting standards: TRIPOD+AI and PROBAST+AI

### Takeaway
Both current standards are method-agnostic: whatever learner is used, the thesis must report sample size justification, handling of missing data, hyperparameter tuning, internal validation of the whole pipeline, calibration, and (per Riley & Collins) stability. Using XGBoost adds reporting burden without relaxing any regression requirement.

### Cited Findings
- TRIPOD+AI (Collins et al., BMJ, 18 April 2024): 27-item checklist plus abstract checklist, harmonized for regression or ML models; supersedes TRIPOD 2015, which "should no longer be used". [PMC11025451](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11025451/)
- PROBAST+AI (Moons et al., BMJ, 24 March 2025, doi 10.1136/bmj-2024-082505): 16 signalling questions for model development (quality/applicability) and 18 for evaluation (risk of bias/applicability), across four domains (participants and data sources, predictors, outcome, analysis); applies irrespective of regression or AI technique and may replace PROBAST 2019. [Birmingham record](https://research.birmingham.ac.uk/en/publications/probastai-an-updated-quality-risk-of-bias-and-applicability-asses/); [ORA](https://ora.ox.ac.uk/objects/uuid:8b15c087-459b-43fa-ad03-1f66ed6ba370)
- Christodoulou 2019: high-risk-of-bias validation was the main source of apparent ML superiority, and 79% of studies did not address calibration, the main things these tools now check. [ORA record](https://ora.ox.ac.uk/objects/uuid:4167c905-5171-4fc7-b157-ff36d56a73db)

### Inferences
- Recommendation for the thesis: penalized LR (ridge or LASSO, splines for continuous predictors, few prespecified interactions; ideally one pooled model with domain terms rather than four small ones) as primary; incremental value of geometry tested by nested-model comparison (likelihood ratio + bootstrap-optimism-corrected ΔAUC/Δlog-loss/calibration). XGBoost, if used, as a secondary sensitivity analysis only: shallow trees, strong regularization, nested CV, same drop-the-geometry-family refit comparison, calibration reported, Riley-Collins bootstrap instability shown; interpret SHAP only descriptively. Do not use it at all per domain if a domain has fewer than roughly 50-100 events.

### Gaps
- Exact TRIPOD+AI item numbers for hyperparameter tuning and fairness were not extracted here.
