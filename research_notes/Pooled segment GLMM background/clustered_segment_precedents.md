# Segment-level clustered models of coronary plaque outcomes, and pitfalls of clustered binary prediction models

Scope note: about 19 searches and fetches. Several full texts (Circulation, Springer, PMC via ncbi redirect, UCL PDF) returned 403 or bot-check pages. Where only an abstract or a secondary summary was read, the finding says so. No CGPS results appear here.

## Q1. Coronary imaging precedents with segment- or lesion-level outcomes and clustering adjustment

### Takeaway
Lesion- and segment-level coronary outcome analyses are common: PARADIGM, ICONIC/CONFIRM, PREDICTION and SMARTool all work at lesion or segment level. The clustering methods I could verify are a shared-frailty Cox model plus cluster-robust (sandwich) SEs in ICONIC, and linear mixed models for continuous IVUS/CCTA progression outcomes. I found **no verified precedent** for a binary *incident* segment-plaque outcome modelled with a cloglog GLMM and person random intercept, and none that formally pooled segment predictions into a person risk by integrating over the random effect. Every precedent I could check is a referral or clinically indicated cohort, and most enrolled patients who already had plaque.

### Cited Findings
- **ICONIC lesion geometry (Han et al., JAMA Cardiol 2022;7(3):309–319, doi:10.1001/jamacardio.2021.5705).**
  - Design: a nested case-control substudy of ICONIC, inside the CONFIRM registry of 23,251 consecutive patients referred for CCTA for suspected CAD. Patients were 1:1 propensity-matched: 116 ACS patients and 116 controls, with 548 lesions.
  - Clustering: within-patient dependence in the lesion-level Cox models was handled with **shared frailty models**. Matched-set clustering in ACS-vs-control comparisons used **clustered sandwich (robust) estimators**.
  - Culprit vs non-culprit HRs: short distance from ostium 2.71 (1.73–4.24); bifurcation 2.14 (1.39–3.29); tortuosity 2.31 (1.01–5.27), P = .04.
  - The authors acknowledge selection bias from the post hoc design and note that included patients were high-risk with extensive atherosclerosis.
  - [Han et al. 2022, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8792800)
- **PARADIGM per-lesion vs per-patient (Lee SE et al., Int J Cardiovasc Imaging 2020;36(12):2357–2364, doi:10.1007/s10554-020-01960-z).**
  - Cohort: drawn from a multinational registry of 2,252 patients with serial CCTA ≥2 years apart. 1,297 patients with only non-obstructive lesions were included: 3,218 lesions, follow-up 3.8 ± 1.6 y.
  - Outcome: 76 lesions (2.4%) in 60 patients became obstructive.
  - C-statistics: clinical model 0.684; + per-patient plaque 0.825; + per-lesion plaque 0.895 (p < 0.001).
  - The abstract does not state how lesions clustered within patients were handled. The trial ID is given inconsistently (NCT02803411 vs NCT0280341).
  - Caution: a lesion-level C-statistic pools lesions across patients, so part of the "per-lesion superiority" may be between-patient discrimination counted at lesion level.
  - [PubMed 32779077](https://pubmed.ncbi.nlm.nih.gov/32779077/)
- **PARADIGM progression methods.** Whole-heart atherosclerosis was characterised per segment, with baseline and follow-up CCTA co-registered, then **summed to patient level**. This is aggregation of measurements, not of model predictions. PARADIGM is a registry of clinically indicated serial CCTA, i.e. referral. [PARADIGM record, Weill Cornell VIVO](https://vivo.weill.cornell.edu/display/pubid33451974)
- **PARADIGM statin, lesion level (Park/Conte et al. 2023).** 613 patients, 1,432 lesions; a 37% reduction in annual PAV in mild lesions with ≥2 high-risk features. The clustering method was not visible in the snippet. [search record, Univ. Milan AIR](https://air.unimi.it/handle/2434/977448)
- **PREDICTION (Stone et al., Circulation 2012;126:172–181, doi:10.1161/CIRCULATIONAHA.112.096438).**
  - Design: IVUS-based vascular profiling of endothelial shear stress (ESS) at baseline and 6–10 months in 374 post-PCI ACS patients (Japan). Low baseline ESS and baseline plaque burden independently predicted plaque enlargement and lumen narrowing.
  - I could not retrieve the methods (403), so the clustering model and link are **unverified**.
  - [ClinicalTrials.gov NCT01316159](https://clinicaltrials.gov/study/NCT01316159); [PMC5508525 (cites the 2012 paper)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5508525); [TCTMD summary](https://www.tctmd.com/news/endothelial-shear-stress-works-prediction-tool)
- **Later PREDICTION analysis.** Linear mixed-effects models estimated the ESS effect on progression across plaque phenotypes; low ESS was associated with progression in all phenotypes. This is a continuous outcome. [PMC10939719](https://pmc.ncbi.nlm.nih.gov/articles/PMC10939719/)
- **Conflicting analysis of related ESS data.** Plaque area predicted change in plaque area (p < 0.001), but flow shear stress did not (p = 0.32). [Heart 2019;105:1078](https://heart.bmj.com/content/105/14/1078)
- **PREDICTION-derived FSI modelling study.** It used **GLMMs** over combinations of biomechanical risk factors to predict wall-thickness and plaque-area increase. It is small and preliminary, and the outcome is not clinical. [PMC5783767](https://pmc.ncbi.nlm.nih.gov/articles/PMC5783767)
- **Stone et al. 2007, subsegment ESS study.** Subsegments with low ESS progressed more often than those with moderate/higher ESS (33.3% vs 7.9%). This is an early subsegment-level design with subsegments nested in arteries and patients. [Wahle lab abstract](https://user.engineering.uiowa.edu/~awahle/WahLIT/Abstracts/ston07-cfd.html)
- **Serial CCTA burden study (PMC9584618).** Explicitly used **linear mixed models** for repeated observations at non-standardised intervals. [PMC9584618](https://pmc.ncbi.nlm.nih.gov/articles/PMC9584618)
- **SMARTool (Smit et al., Circ Cardiovasc Imaging 2020).** A per-plaque serial CCTA analysis, interscan ~6.2 y. The snippet does not show how repeated plaques per patient were handled. [Houston Methodist record](https://scholars.houstonmethodist.org/en/publications/effect-of-statin-treatment-on-coronary-plaque-progression-a-seria/)

### Inferences
- The cardiology precedent for "segment rows, person cluster" is real, but it is mostly survival with frailty or robust SEs (ICONIC) or continuous mixed models (PREDICTION/IVUS). A segment-level binary GLMM with a cloglog link and an offset appears to be a methodological choice rather than an established convention in this field. The thesis should present it as justified by the discrete-time/interval-censoring argument, not by precedent.
- None of the verified precedents studies plaque-free baselines. All are referral or indicated-imaging cohorts with prevalent disease (CONFIRM/ICONIC, PARADIGM, PREDICTION post-ACS). Effect sizes should not be transferred to a general-population cohort.
- The PARADIGM per-lesion C (0.895) is a pooled lesion-level C. It is not comparable with a person-level C or a within-person C.

### Gaps
- I could not verify the PREDICTION 2012 clustering model or link, nor the clustering handling in PROSPECT (Stone, NEJM 2011), SCOT-HEART, CONFIRM lesion analyses or the PARADIGM lesion papers (all paywalled or not retrieved). In particular, I could not confirm whether any used a GEE or GLMM with a logit or cloglog link.
- I found no study that pooled segment-level predicted risks to a person-level risk, i.e. P(any segment) = 1 − ∏(1 − p_s) integrated over b. This looks like a genuine gap, but absence of evidence from ~19 searches is weak evidence.
- I found no coronary study that used segment length as an exposure offset (see Q5).

## Q2. What goes wrong when clustering is ignored; GLMM vs GEE vs cluster-robust SEs for binary outcomes

### Takeaway
Ignoring within-person correlation treats ~9 segment rows as independent. This understates SEs for person-level covariates, so tests are anti-conservative. Cluster-robust SEs and GEE fix inference for **marginal** (population-averaged) effects. A GLMM estimates **conditional** (person-specific) effects, which for logit or cloglog are larger in magnitude than the marginal ones, and gives correct marginal risks only when predictions are integrated over the random effect. The sources I could retrieve this session cover the prediction-side consequences well. The classic inference literature is listed under Gaps as unverified.

### Cited Findings
- **Calibration from setting b = 0.** Taking marginal risks from a random-intercept logistic model with b = 0 gives miscalibrated population-level predictions, and the miscalibration grows with clustering. At ICC 0.30 the calibration slope was 0.788 with b = 0, against 0.977 when integrating over the random-effect distribution. The paper also notes that Skrondal and colleagues had earlier flagged this as a common applied error. [Pavlou, Ambler, Seaman, Omar, BMC Med Res Methodol 2015;15:59, doi:10.1186/s12874-015-0046-6](https://pmc.ncbi.nlm.nih.gov/articles/PMC4525751); [Table 1](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/s12874-015-0046-6/tables/1)
- **Confounding by cluster and informative cluster size.** GEE and GLMM can give inaccurate predictions under confounding by cluster (CBC) or informative cluster size (ICS), which motivates cluster-mean (Mundlak-type) terms. I read only the search summary; the PDF returned 403. [Pavlou et al., BMC Med Res Methodol 2021, s12874-021-01321-x](https://discovery-pp.ucl.ac.uk/10131097/1/s12874-021-01321-x.pdf); review: Seaman, Pavlou, Copas, Stat Med 2014 (via the same search, [UCL listing](https://www.ucl.ac.uk/statistics/dr-menelaos-pavlou))
- **Bias in multilevel logistic estimates.** In simulation, multilevel logistic fixed effects were unbiased with ~100 clusters of ≥50, while variance components remained slightly biased. Rare outcomes and higher ICC worsened accuracy. [Moineddin, Matheson, Glazier, BMC Med Res Methodol 2007;7:34, doi:10.1186/1471-2288-7-34](https://pmc.ncbi.nlm.nih.gov/articles/PMC1955447/)

### Inferences
- For this design (few segments per person, many persons) the problem is the reverse of the multicentre setting. Cluster size is ~9, not ~50, and there are about a thousand clusters. Person-level geometry and SCORE2 terms are cluster-constant, so naive segment-row SEs for them would be the most anti-conservative, because the design effect applies fully to cluster-level covariates.
- Informative cluster size is relevant. The number of usable trunk segments per person (dominance, structurally absent PDA/PLA, ungradable segments) may correlate with risk.

### Gaps (classic references not fetched this session, cited from background knowledge; verify DOIs before citing)
- Liang & Zeger 1986, *Biometrika* 73:13–22, doi:10.1093/biomet/73.1.13 (GEE); Zeger, Liang & Albert 1988, *Biometrics* 44:1049, doi:10.2307/2531734 (conditional vs marginal coefficients, the attenuation factor ≈ (1 + 0.346σ²)^−½ for logit).
- Neuhaus, Kalbfleisch & Hauck 1991, *Int Stat Rev* 59:25, doi:10.2307/1403444.
- Hubbard et al. 2010, "To GEE or not to GEE", *Epidemiology* 21:467, doi:10.1097/EDE.0b013e3181caeb90.
- I did not find, and therefore cannot cite, the attenuation formula for the **cloglog** link. For cloglog with normal b there is no closed form, so integration is numerical.

## Q3. Guidance on developing and validating clustered prediction models

### Takeaway
The multicentre prediction literature (Bouwmeester 2013; Pavlou 2015; Wynants 2018; Falconieri 2020) agrees on three points:
1. Model the clustering.
2. Pick the prediction type (conditional, average-random-effect, or marginal/integrated) to match the level at which predictions will be used.
3. Validate at the level the research question targets.

For new clusters, i.e. new people, marginal predictions must be obtained by integrating over b, not by setting b = 0. **Correction to the brief:** "Pavlou et al. 2015 BMJ" is a few-events/penalisation paper (BMJ 351:h3868). The clustered-prediction Pavlou 2015 paper is in *BMC Med Res Methodol*.

### Cited Findings
- **Bouwmeester et al. 2013.**
  - Citation: BMC Med Res Methodol 13:19, doi:10.1186/1471-2288-13-19.
  - Data: 1,642 surgical patients in 19 anaesthesiologist clusters, plus simulations.
  - Discrimination: random-intercept models discriminated better only when cluster effects were used for prediction (C 0.69 vs 0.66).
  - Calibration and recommendation: random-intercept models were well calibrated within clusters, and the authors favour them when patient-level predictor effects are of interest.
  - [PMC3658967](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3658967/)
  - Critique: Pavlou et al. 2015 showed that Bouwmeester's marginal predictions set b = 0 and were therefore miscalibrated. [PMC4525751](https://pmc.ncbi.nlm.nih.gov/articles/PMC4525751)
- **Pavlou BMJ 2015 is not about clustering.** Pavlou, Ambler, Seaman, Guttman, Elliott, Omar, "How to develop a more accurate risk prediction model when there are few events", BMJ 2015;351:h3868 is about few events and penalisation. It is relevant to Q4, not Q3. [UCL staff page](https://www.ucl.ac.uk/mathematical-physical-sciences/statistics/people/academic-and-lecturing-staff/dr-menelaos-pavlou)
- **Wynants et al. 2018.**
  - Citation: Wynants, Vergouwe, Van Huffel, Timmerman, Van Calster, *Stat Methods Med Res* 27(6):1723–1736, doi:10.1177/0962280216668555.
  - Framework: evaluation at the cluster level and the population level, for population-averaged, cluster-specific and average-random-effect predictions.
  - Calibration: slopes can depart from 1 because of model type, prediction type and validation level, not only overfitting.
  - Heavy clustering: at ICC 20%, cluster-specific predictions performed best at both levels.
  - Recommendation: "models should reflect the data structure, while the level of model validation should reflect the research question."
  - [EUR RePub](https://repub.eur.nl/pub/106551)
- **Wynants et al. multicentre overview.** Clustering should be handled during analysis, e.g. with mixed-effects models and centre-level variables. Only mixed-effects regression can give a model calibrated simultaneously at the centre and the population level. [Arch Public Health 2015;73(S1):O3](https://archpublichealth.biomedcentral.com/articles/10.1186/2049-3258-73-S1-O3); a related review, "Prediction models in multicenter studies: methodological aspects and current state of the art", is at [PMC4582405](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4582405/) (bot-check blocked the full text, so the authors and journal are not verified).
- **Falconieri et al. 2020.**
  - Citation: Falconieri, Van Calster, Timmerman, Wynants, *Biometrical Journal* 62(4):932–944.
  - Findings: with adequate sample size, conditional models gave calibrated predictions and marginal models miscalibrated ones. Small samples caused overfitting. Miscalibration of standard logistic regression worsened with stronger clustering. The authors recommend random-intercept logistic regression for centre-specific prediction.
  - Note: this is a simulation study, not a review.
  - [Maastricht CRIS](https://cris.maastrichtuniversity.nl/en/publications/developing-risk-models-for-multicenter-data-using-standard-logist/)

### Inferences
- Mapping to the thesis: "centre" corresponds to "person", and new test-fold people are new clusters with unknown b.
  - For the **who** question (person risk in a new person), the right prediction is the **marginal, integrated** one, P(any plaque) = ∫[1 − ∏_s(1 − p_s(b))] φ(b) db. Setting b = 0 would be Bouwmeester's error, made worse by the product over segments.
  - For the **where** question, within-person ranking does not depend on b in a random-intercept model, so within-person C is invariant to how b is handled.
- Cross-validation split by person is the cluster-level analogue of leave-centre-out validation, which this literature uses to evaluate prediction in new clusters. No source I retrieved states this explicitly for segment data.
- In the Wynants framework, a "population-level" C pools across clusters and mixes within- and between-cluster discrimination. That supports reporting within-person C and person-level C separately, not a pooled segment-row C.

### Gaps
- I did not retrieve a source that explicitly prescribes grouped (by-cluster) K-fold CV for clustered prediction models. It is standard practice, but I have no citation from this session.
- I did not retrieve guidance on calibration slope or intercept for integrated marginal predictions from a **cloglog** GLMM specifically. All retrieved work is logit.

## Q4. Sample size and events per parameter for multilevel prediction models

### Takeaway
The Riley et al. criteria (implemented in `pmsampsize`) are single-level: shrinkage ≤ 10%, an optimism gap in Nagelkerke R² ≤ 0.05, and the average risk estimated within ±0.05. I found **no published extension of the Riley criteria to clustered or multilevel prediction models**. Multilevel sample-size evidence comes from parameter-estimation simulations such as Moineddin 2007, not from prediction-performance criteria.

### Cited Findings
- **`pmsampsize` criteria.** For binary and survival outcomes: expected shrinkage ≤ 10%, a gap between apparent and adjusted Nagelkerke R² of about 0.05, and the average outcome risk within ±0.05. These come from Riley et al. (2018 onward). [pmsampsize manual](https://cran.r-universe.dev/pmsampsize/doc/manual.html); [CRAN](https://www.stats.bris.ac.uk/R/web/packages/pmsampsize/index.html)
- **Moineddin et al. 2007 (multilevel logistic simulation).** Fixed effects were unbiased with 100 groups × ≥50 per group, and variance components were slightly biased. Rare events need larger samples. This concerns estimation, not prediction. [PMC1955447](https://pmc.ncbi.nlm.nih.gov/articles/PMC1955447/)
- **Design effect.** DEFF = 1 + (m − 1)ρ and N_eff = N/DEFF for equal cluster sizes. The source is vendor documentation, so it is low authority and listed only as a formula reference. [MetricGate](https://metricgate.com/docs/multilevel-logistic-sample-size/)
- **Penalisation in small samples.** Penalisation can improve prediction accuracy when there are few events (Pavlou et al., BMJ 2015;351:h3868). This session confirms only the title and topic. [UCL page](https://www.ucl.ac.uk/statistics/dr-menelaos-pavlou)

### Inferences
- A defensible approach is to apply the Riley criteria at the **person** level for who-question parameters, i.e. person-constant terms such as SCORE2 factors and LM features, using persons and person events. Segment-level events are not independent and overstate the information for those terms.
- Segment-varying within-person terms (curvature or taper deviations) gain information from segment events, but only from informative people, and the design effect depends on the ICC. This is a reasoned argument, not something I found in a published criterion.

### Gaps (unverified references from background knowledge; verify before citing)
- Riley et al. 2019, *Stat Med* 38:1276–1296, doi:10.1002/sim.7992 (binary/time-to-event criteria); Riley et al. 2020, *BMJ* 368:m441, doi:10.1136/bmj.m441.
- Riley et al. also published sample-size work for *external validation* (Stat Med 2021 and onward), but I did not confirm a multilevel version.
- Whether any 2023–2026 paper extends the Riley criteria to random-effects prediction models: not found.

## Q5. Exposure adjustment for segment length in lesion- or segment-level models

### Takeaway
I found **no coronary imaging study that used segment length as an offset or exposure term** in a segment-level plaque model. ICONIC used distance from the ostium as a *predictor*, not as exposure. The justification for log(length) has to come from the cloglog/Poisson-process argument: if lesions arise as a Poisson process along the vessel with rate λ, then P(≥1) = 1 − exp(−λ·L·t), so cloglog P = log λ + log L + log t. On that basis log L enters as an offset (coefficient fixed at 1) or as a free covariate tested against 1.

### Cited Findings
- **ICONIC.** Distance from the ostium (HR 2.71 for short distance) and bifurcation location were modelled as lesion characteristics, not as exposure. [Han et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8792800)
- **Thesis's own planning report.** It states that log(length) enters as a free covariate tested against 1 in the cloglog GLMM. This is the thesis's own decision, not external evidence. Source: local file `~/Desktop/Speciale/CGPS_statistics-/reports/Segment plaque risk model nonlinearity.md`.

### Inferences
- Length is not a pure exposure. Proximal segments are both longer and haemodynamically different, and in the AHA/SCCT scheme segment boundaries are defined by landmarks. A free coefficient on log L is therefore the safer default; an offset should be treated as a hypothesis.
- Measurement error in tracer-derived length adds attenuation if length enters as a covariate.

### Gaps
- I found no published precedent, in coronary or other vascular imaging, for a length offset in lesion-incidence models. Analogues from other fields (e.g. polyp counts per colon segment, or road-segment accident models with log length offsets) were not searched.
