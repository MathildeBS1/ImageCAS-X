# Neural network design for segment-level plaque prediction with patient-level covariates (CGPS Herlev–Østerbro, ~2000 patients / ~30,000 segments)

Scope note: ~17 tool calls were used. Several design points rest on well-known methods literature that I could not re-fetch in full within budget; those are placed under Inferences or Gaps rather than presented as cited findings. Preprints are flagged [PREPRINT].

## Q1. Fusion strategies for patient-level tabular (SCORE2) plus segment-level features

### Takeaway
At this data size the inputs are all low-dimensional tabular features, so the published evidence argues for a simple, strongly regularised model (early concatenation of broadcast patient features with segment features, or a small hierarchical/shared-encoder MLP), benchmarked against logistic regression and gradient-boosted trees. FiLM/DAFT-style conditioning was designed for fusing tabular data into high-dimensional image feature maps and offers little that a concatenation-plus-interaction MLP cannot already express when the "segment branch" is itself ~5 to 10 numbers.

### Cited Findings
- DAFT (Pölsterl, Wolf, Wachinger, MICCAI 2021) conditions a 3D CNN on tabular clinical data by predicting per-channel scale and shift for convolutional feature maps; reported balanced accuracy 0.622 for Alzheimer diagnosis and c-index 0.748 for time-to-dementia — [arXiv 2107.05990](https://arxiv.org/abs/2107.05990)
- DAFT was reported as more effective than FiLM because it learns a wider, more dynamic range of scale/shift parameters; FiLM was "overall less effective" in that comparison — [DAFT paper PDF](https://arxiv.org/pdf/2107.05990)
- On medium-sized tabular data (~10K samples) tree-based models (XGBoost, random forests) remain state of the art over deep learning across 45 benchmark datasets; NNs struggle with uninformative features, rotation-invariant inductive bias and irregular target functions — [Grinsztajn, Oyallon, Varoquaux, NeurIPS 2022](https://arxiv.org/abs/2207.08815v1)
- Systematic review of 71 clinical prediction studies (median n = 1,250, median 19 predictors): no performance benefit of ML (incl. ANNs) over logistic regression; 68% of studies had potential bias in validation — [Christodoulou et al., J Clin Epidemiol 2019;110:12-22](https://ora.ox.ac.uk/objects/uuid:4167c905-5171-4fc7-b157-ff36d56a73db)
- PARADIGM (serial CCTA, 1297 patients, 3218 non-obstructive lesions, 3.8 y interval, 76 lesions (2.4%) progressed to obstructive) found per-lesion plaque volume and high-risk plaque features improved C-statistic from 0.825 (per-patient features) to 0.895 (per-lesion features), p < 0.001 — direct precedent that lesion/segment-level features add value beyond patient-level aggregates for serial CCTA outcomes — [PubMed 32779077](https://pubmed.ncbi.nlm.nih.gov/32779077/)

### Inferences
- Recommended baseline architecture ("early fusion, shared head"): for segment j of patient i, input x_ij = [SCORE2 vars of i (broadcast), segment-type one-hot or learned embedding (LM, pLAD, mLAD, ...), baseline plaque of j, geometry of j], into a 2 to 3 layer MLP with dropout/weight decay, output logit. This is equivalent to a nonlinear GLM with all patient-segment interactions available.
- Hierarchical variant worth one ablation: a patient encoder f(SCORE2) -> h_i and a segment encoder g(segment features) -> s_ij, combined by concatenation or by FiLM (h_i producing scale/shift on s_ij). FiLM here is just a structured multiplicative interaction; with ~7 patient variables it is unlikely to beat concatenation and adds parameters. Report it as an ablation, not a main design.
- Tree-level context: if the coronary tree is represented as a graph (segments as nodes, parent-child edges), a small GNN or attention pooling over neighbouring segments can let a segment "see" plaque in adjacent segments (plaque in proximal LAD predicts mid-LAD). A cheaper equivalent is to hand-craft neighbour features (plaque in parent segment, patient-level plaque count/burden excluding j). Given the tree is small (16 to 18 nodes), the hand-crafted route is likely competitive; this is an inference, not a cited result.
- Attention pooling is relevant only if a patient-level outcome is also predicted (multi-task); for segment-level outcomes it is not needed.
- With ~2000 patients the effective sample size for patient-level effects is ~2000, not ~30,000; the patient branch should therefore be small and heavily regularised.
- Mandatory comparators: (a) logistic GLMM / GEE with the same inputs, (b) gradient-boosted trees with patient-grouped CV. A neural net that does not beat these is still a valid thesis result.

### Gaps
- I found no published study that fuses SCORE2-type risk factors with per-segment CCTA geometry in a neural network for incident plaque; the design is therefore not directly benchmarked in literature.
- I did not retrieve a head-to-head comparison of concatenation vs FiLM for purely tabular multi-level data (DAFT compares them for image + tabular only).
- Perez et al. FiLM (AAAI 2018) original was not fetched within budget.

## Q2. Handling clustering of segments within patients

### Takeaway
Two separate issues: (1) training: the model can include patient random effects (LMMNN, MeNets, ARMED) or simply rely on patient-level covariates plus regularisation; (2) evaluation: splits must be by patient (grouped/block CV), and uncertainty in metrics should come from a patient-level (cluster) bootstrap. (2) is non-negotiable; (1) is optional and mostly helps when the cluster effect is strong and partly unexplained by covariates.

### Cited Findings
- Standard DNNs implicitly assume independent responses; LMMNN (Simchoni & Rosset, JMLR 2023, 24) treats correlation sources (clusters, spatial, temporal) as random effects and trains by minimising the Gaussian NLL with SGD; it improved predictive performance over competitors in simulations and real data — [JMLR v24 22-0501](https://www.jmlr.org/papers/v24/22-0501.html); [arXiv 2206.03314](https://arxiv.org/abs/2206.03314)
- LMMNN cites MeNets (Xiong et al., 2019) and DeepGLMM (Tran et al., 2020) as related mixed-effects NN approaches — [arXiv 2206.03314](https://arxiv.org/pdf/2206.03314)
- LMMNN is focused on regression; classification is described as more of a proof of concept, because the exact NLL for a GLMM with non-Gaussian outcomes involves intractable integrals — [arXiv 2206.03314 / GitHub discussion](https://github.com/gsimchoni/lmmnn/issues/14)
- A follow-up uses Monte Carlo methods to enable mixed-effects NNs for diverse (non-Gaussian) clustered outcomes [PREPRINT] — [arXiv 2407.01115](https://arxiv.org/pdf/2407.01115)
- ARMED (Nguyen, Treacher, Montillo, 2023) adds to an existing NN: (1) an adversarial classifier forcing the fixed-effects network to learn cluster-invariant features, (2) a random-effects subnetwork for cluster-specific effects, (3) a method to apply random effects to clusters unseen in training; it better separated confounded from true associations in simulation and was applied to dementia prognosis — [PMC10644386](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10644386/)
- Ignoring hierarchical structure in cross-validation "results in serious underestimation of predictive error"; block CV (split by group) is nearly universally more appropriate when the goal is prediction to new data — [Roberts et al., Ecography 2017;40:913-929](https://www.biometrie.uni-freiburg.de/mitarbeiter/dormann/roberts-et-al-2017-ecography.pdf)
- TRIPOD-Cluster (Debray et al., BMJ 2023;380:e071018) is the reporting checklist for prediction models developed or validated on clustered data; TRIPOD+AI (BMJ 2024;385:e078378) covers regression and ML models generally — [EQUATOR TRIPOD](https://www.equator-network.org/reporting-guidelines/tripod/); [Debray 2023 PDF](https://research.birmingham.ac.uk/files/187291565/DebrayT2023Transparent.pdf)

### Inferences
- Key practical point for CGPS: at prediction time for a new participant there is no follow-up data from that participant, so a random intercept b_i cannot be estimated for the target patient. In LMMNN/ARMED terms the new patient is an "unseen cluster" and the prediction reverts to the fixed-effects part (b_i = 0, or ARMED's unseen-cluster approximation). Random effects therefore mainly (a) improve fixed-effect estimation by soaking up within-patient correlation and (b) give a variance component (ICC) to report. Do not use a free patient-ID embedding as an input: it cannot generalise to new patients and will leak under any non-grouped split.
- The "patient susceptibility" that a random intercept would capture can be partly encoded deterministically from baseline data available at prediction time: number of plaqued segments at baseline, total baseline plaque burden, CAC score (if available). Including these as patient-level inputs is a legitimate, prediction-time-available alternative to random effects.
- Conditional vs marginal: a GLMM/random-effects model yields patient-conditional probabilities; a model with no random effect (or GEE) yields population-averaged probabilities. Calibration should be assessed on the scale the model targets; for a prediction tool on new patients, the marginal (b_i integrated out) probability is the relevant one.
- Evaluation recipe: patient-grouped K-fold (e.g. 5x5 repeated, stratified by patient-level outcome count), all preprocessing/imputation fitted within folds; report segment-level AUC, Brier, calibration slope/intercept with 95% CIs from a patient-level bootstrap (resample patients, keep all their segments). Also report patient-level metrics (any new plaque per patient) derived by aggregating segment probabilities (1 - prod(1 - p_ij) is only valid under conditional independence; note this).
- Report the ICC from a logistic GLMM fitted alongside; it quantifies how much the clustering matters and justifies (or not) a mixed-effects NN.

### Gaps
- MeNets (Xiong et al. 2019) and DeepGLMM (Tran et al. 2020) original papers were not fetched; details only known via the LMMNN citation.
- No source found on cluster-bootstrap CIs specifically for AUC in segment-nested data; this is standard practice but uncited here.
- No paper found comparing mixed-effects NNs with plain NNs for binary clustered outcomes at n ~ 2000 clusters.

## Q3. Treating baseline plaque: input vs outcome split; multi-task; ordinal; change score vs ANCOVA

### Takeaway
Condition on baseline (ANCOVA logic): predict follow-up status with baseline status as an input, not "change" as the target. Because "incident plaque in a plaque-free segment" and "progression of an existing plaque" are biologically and statistically different questions with very different base rates, either fit them as two heads (multi-task) or as two separate analyses, and make the incident-plaque analysis the primary one for testing geometry.

### Cited Findings
- Vickers (BMC Med Res Methodol 2001) compared post-score analysis, change from baseline, percentage change and ANCOVA with baseline as covariate: ANCOVA had the highest power; change score is acceptable only when baseline-follow-up correlation is high; percentage change had the lowest power and is not recommended — [BMC 1471-2288-1-6](https://bmcmedresmethodol.biomedcentral.com/track/pdf/10.1186/1471-2288-1-6); [PMC34605](https://pmc.ncbi.nlm.nih.gov/articles/PMC34605)
- Vickers & Altman (BMJ 2001;323:1123) "Analysing controlled trials with baseline and follow up measurements" makes the same ANCOVA recommendation — [BMJ 323/7321/1123](https://www.bmj.com/content/323/7321/1123)
- PARADIGM restricted its analysis to non-obstructive lesions at baseline and defined the outcome as progression to >50% stenosis, i.e. it split by baseline status rather than modelling change across all lesions; event rate was 2.4% of lesions — [PubMed 32779077](https://pubmed.ncbi.nlm.nih.gov/32779077/)
- CORAL (Cao, Mirjalili, Raschka, Pattern Recognition Letters 2020) gives rank-consistent ordinal outputs for any NN by K-1 binary tasks with shared weights and ordered biases, avoiding inconsistencies of independent binary classifiers — [arXiv 1901.07884](https://arxiv.org/abs/1901.07884v5)

### Inferences
- Note the ANCOVA evidence comes from randomised trials (estimation of a treatment effect). The transferable lesson for prediction is: model Y_followup | Y_baseline, X, which automatically handles regression to the mean and lets the effect of baseline be nonlinear. A "change" target (delta burden) forces a coefficient of 1 on baseline and mixes measurement error into the outcome.
- Proposed outcome structure per segment:
  - Head A (primary, geometry question): P(any plaque at FU | no plaque at baseline). Trained only on baseline-plaque-free segments. This is where geometry (curvature, bifurcation angle, diameter ratio) is most mechanistically interpretable and least confounded by existing disease.
  - Head B (secondary): progression in baseline-plaqued segments, e.g. ordinal category change (stable / increase / composition change) via CORAL, or follow-up burden regressed on baseline burden (ANCOVA-style with baseline as input).
  - Optional Head C: plaque type at FU (calcified / non-calcified / mixed) as multinomial, conditional on presence.
  Shared trunk with separate heads is reasonable multi-task design; masking losses for inapplicable segments keeps each head's denominator correct.
- A single-head model over all segments with baseline plaque as an input is acceptable as a sensitivity analysis but its AUC will be dominated by "plaque stays plaque", which inflates apparent performance and hides the geometry signal. Always report Head A separately.
- Ordinal coding of plaque (none < calcified-only < mixed < non-calcified) is not clearly a monotone order of severity; ordinal losses should only be used for burden categories (e.g. stenosis grade, volume tertiles), not composition.
- Plaque regression (plaque at baseline, none at FU) will occur partly due to reader/measurement variability; it should be counted and reported, not silently merged.

### Gaps
- Did not find serial-CCTA studies that explicitly compare change-score vs conditional modelling for plaque volume; the ANCOVA argument is imported from trial methodology.
- No source retrieved on multi-task learning benefits at this sample size in clinical tabular data.

## Q4. Class imbalance and loss choice

### Takeaway
Use plain (unweighted) binary cross-entropy, a proper scoring rule, and accept the low event rate. Resampling, class weights and focal loss distort predicted probabilities; if used for discrimination they must be followed by recalibration, which TRIPOD-style reporting will require anyway.

### Cited Findings
- van den Goorbergh et al. (JAMIA 2022) compared no correction, random undersampling, oversampling and SMOTE for (ridge) logistic regression: outcome imbalance is not a problem in itself, corrections "dramatically deteriorated" calibration (overestimation of risk) with no consistent discrimination gain, and recalibration could not always repair it; recommendation was no correction — [PMC9382395](https://pmc.ncbi.nlm.nih.gov/articles/PMC9382395)
- A 2026 evaluation across diverse real-world clinical prediction tasks found class-imbalance corrections gave no generalisable discrimination improvement and degraded Brier score and calibration intercept/slope [PREPRINT] — [arXiv 2603.00208](https://arxiv.org/pdf/2603.00208)
- Focal loss is not a strictly proper loss, so outputs are not consistent estimates of the class posterior; a closed-form transformation has been proposed to recover calibrated risks from focal-loss-trained GBDTs — [Penn State record](https://pure.psu.edu/en/publications/estimating-calibrated-risks-using-focal-loss-and-gradient-boosted/); [arXiv 2404.19494](https://arxiv.org/html/2404.19494v1)
- PARADIGM's lesion-level event rate was 2.4% (obstructive progression), showing the scale of imbalance to expect for hard segment-level outcomes on serial CCTA — [PubMed 32779077](https://pubmed.ncbi.nlm.nih.gov/32779077/)

### Inferences
- For CGPS Head A, with e.g. ~30,000 segments of which a majority are plaque-free at baseline and a 10-year incident rate of perhaps a few to ~10% per segment (unknown; to be measured), there will be on the order of hundreds to low thousands of events. That is enough for BCE without reweighting; the problem is effective sample size (events and patients), not imbalance per se.
- If focal loss or weighting is tried for comparison, apply post-hoc recalibration (Platt/logistic or isotonic) fitted on out-of-fold predictions within the grouped CV, and report calibration before and after.
- Report: AUC (segment and patient level), Brier score, calibration slope and intercept, calibration plot, and decision-curve net benefit if a clinical threshold is discussed.

### Gaps
- No study found on focal loss specifically for nested segment-level medical outcomes.
- Expected 10-year per-segment incident plaque rate in a general-population cohort was not searched here (belongs to the clinical background research thread).

## Q5. Missing / non-evaluable segments, absent anatomy, censoring (death, revascularisation, loss to follow-up)

### Takeaway
Distinguish three kinds of "missing": (1) structurally absent segments (anatomy, e.g. no ramus, left-dominant PDA), which are not missing data and should simply not exist as rows; (2) non-evaluable segments (artefact, stent), which are missing outcomes/inputs; (3) participants who did not get a follow-up scan, often informatively (death, revascularisation, illness). (3) is the main validity threat, and the estimand must be stated explicitly, e.g. "plaque at 10 years among those alive and un-revascularised".

### Cited Findings
- Kurland & Heagerty (2005) characterised targets of inference for longitudinal data truncated by death via factorisations of the joint distribution of survival and response, motivating the "partly conditional" (among survivors) mean model — [as summarised in PMC2812934](https://pmc.ncbi.nlm.nih.gov/articles/PMC2812934)
- Li & Su (2017/2018, JRSS-C) proposed joint modelling of the longitudinal outcome with semi-competing dropout and death, targeting the outcome profile "given being alive", since extrapolating beyond death is often inappropriate — [PMC5741179](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5741179/)
- TRIPOD-Cluster and TRIPOD+AI require reporting of how missing data and loss to follow-up were handled — [EQUATOR TRIPOD](https://www.equator-network.org/reporting-guidelines/tripod/)

### Inferences
- Estimand: the natural one for a two-scan cohort is the partly conditional estimand (plaque at FU among those who survive and are scanned without intervening revascularisation of that territory). State that predictions do not apply to people who die or are revascularised, and quantify this group.
- Informative dropout check: compare baseline SCORE2, plaque burden and geometry between participants with and without a FU scan; fit a model for P(has FU scan | baseline) and use inverse-probability-of-censoring weights in the loss (weighted BCE) as a sensitivity analysis. IPCW is compatible with any NN loss.
- Revascularisation/stent between scans: the treated segment's outcome is unobservable (stent artefact) and the indication is itself "plaque progressed". Options: (a) treat revascularised segments as events (composite "new plaque or revascularised"), (b) exclude them (biased toward lower risk), (c) both as sensitivity analyses. (a) is closest to a competing-event composite strategy.
- Death between scans is a competing event; with only two time points and no event times for plaque, a full competing-risk survival model is not identifiable for the plaque outcome. Reporting the numbers and the partly-conditional estimand is the realistic option.
- Non-evaluable segments at FU: mask them out of the loss (do not impute outcomes). Non-evaluable inputs at baseline: impute within folds (e.g. multiple imputation or simple imputation with missingness indicator) and report counts. Segment-type embedding or one-hot ensures absent segments do not need placeholders.
- Segment-level outcome missingness may correlate with disease (calcium blooming, stents), so report outcome availability by baseline plaque status.

### Gaps
- No source retrieved on IPCW in neural network training for clinical prediction specifically; this is an inference from standard survival methodology.
- Medis/CGPS-specific rates of non-evaluable segments not available here.

## Q6. Interpretability and showing that geometry adds value beyond SCORE2 + baseline plaque

### Takeaway
The primary evidence for "geometry adds value" should be a nested-model comparison (with vs without geometry, same architecture, same grouped CV folds), reported as a likelihood/log-loss difference with patient-bootstrap CI plus change in calibration and AUC, not NRI. SHAP or integrated gradients are secondary descriptive tools, and must account for correlated features.

### Cited Findings
- Pepe, Kerr, Longton & Wang (Stat Med 2013): the null of "no improvement" in AUC, NRI, IDI is equivalent to "the new marker is not a risk factor given the old ones"; tests based on NRI/IDI can have inflated false-positive rates; recommend likelihood-ratio testing of the new variables and estimation (not testing) of performance improvement — [PMC3625503](https://pmc.ncbi.nlm.nih.gov/articles/PMC3625503); [biostats.bepress paper379](https://biostats.bepress.com/uwbiostat/paper379)
- Kernel SHAP assumes feature independence; with correlated features it evaluates unrealistic data points and "the explanations may be very misleading"; Aas, Jullum & Løland (Artificial Intelligence 2021;298) give conditional-distribution approximations that are more accurate under dependence — [arXiv 1903.10464](https://arxiv.org/abs/1903.10464v3)
- PARADIGM's evidence for lesion-level value was a C-statistic comparison of nested models (0.825 -> 0.895, p < 0.001) — [PubMed 32779077](https://pubmed.ncbi.nlm.nih.gov/32779077/)

### Inferences
- Concrete protocol: Model 0 = SCORE2 + segment type; Model 1 = Model 0 + baseline plaque (segment and patient-level burden); Model 2 = Model 1 + geometry. Fit each as (i) logistic GLMM and (ii) the NN, on identical patient-grouped folds. Report out-of-fold log-loss, Brier, AUC, calibration, and their differences with patient-bootstrap CIs. For the GLMM, the LRT on geometry terms is the formal test (Pepe/Kerr logic).
- Geometry features are correlated with each other and with anatomy (segment type determines typical curvature and bifurcation angles), so (a) always include segment type in the base model, else geometry gets credit for anatomy; (b) use grouped/conditional SHAP or permutation importance of the whole geometry block rather than per-feature marginal SHAP.
- Integrated gradients are equivalent in spirit to SHAP for differentiable models with a baseline; the choice of baseline (e.g. mean segment of the same type) matters and should be stated.
- Attention weights (if a GNN/attention over the tree is used) are not faithful explanations by default; use them descriptively only.
- Dependence plots of SHAP for curvature or bifurcation angle, stratified by segment type, give the mechanistic picture (e.g. risk vs angle near bifurcations); a GAM/GLMM with splines gives the same plot with CIs and is a good cross-check.

### Gaps
- The Jain & Wallace "attention is not explanation" (NAACL 2019) and Sundararajan integrated gradients (ICML 2017) papers were not fetched within budget.
- Riley et al. sample-size criteria for prediction models (BMJ 2020) were not retrieved; would be useful to justify the number of candidate parameters for ~2000 patients.
- No published SHAP analysis of coronary geometry for incident plaque was found.
