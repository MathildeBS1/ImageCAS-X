# FPC scores of a continuous curve as predictors in clinical outcome models

Scope: peer-reviewed clinical or epidemiological studies where a curve is reduced by FPCA to scores, and the scores are entered into a logistic, Cox or similar model for a binary or time-to-event outcome. Ideally the paper also compares the scores with a scalar summary. DOIs were checked against api.crossref.org on 2026-11-07. The access level is given for each paper.

## Which peer-reviewed papers follow FPCA -> scores -> clinical outcome model?

### Takeaway
The design is well established in accelerometry/mortality cohorts. The two clearest large prospective examples are UK Biobank (Stein et al. 2023, n = 84,877, 2,850 deaths) and MrOS (Zeitzer et al. 2018, n = 2,976). Both run FPCA on a 24-hour activity profile and enter the scores into multivariable Cox models. In cardiovascular epidemiology the clearest example is Shi et al. 2020 (Statistics in Medicine), which uses Framingham Offspring cholesterol trajectories, FPC scores and landmark Cox models for CHD.

### Cited findings

**1. Stein MJ, Baurecht H, Sedlmeier AM, ... Viallon V, Weber A. "Association between circadian physical activity patterns and mortality in the UK Biobank." Int J Behav Nutr Phys Act 2023;20:102. DOI 10.1186/s12966-023-01508-z (Crossref verified, published 2023-09-01). Peer-reviewed; open access; full text read via PMC.**
- Design: prospective cohort. Wrist accelerometry was recorded in 2013–2015. The pattern sample had 96,351 people and the mortality sample 84,877, with 2,850 deaths over a median follow-up of 6.9 years — [PMC10472628](https://pmc.ncbi.nlm.nih.gov/articles/PMC10472628)
- Curve: the hourly ENMO profile averaged across days, a 24-point curve per person. ENMO was first regressed on age, sex, BMI and study centre, and the standardised residuals were analysed. FPCA was done with PACE (R `fdapace`). Four components explained 95.8% of variance, and fPC1 (65.5%) is overall daytime activity — [PMC10472628](https://pmc.ncbi.nlm.nih.gov/articles/PMC10472628)
- Model: Cox model with age as the time scale, stratified by sex and centre. It adjusted for diabetes, CVD, smoking, alcohol, socioeconomic status, education, sedentary behaviour and diet. Scores entered with restricted cubic splines — [PMC10472628](https://pmc.ncbi.nlm.nih.gov/articles/PMC10472628)
- Results:
  - fPC1 = −2: HR 1.69 (95% CI 1.57–1.81).
  - fPC1 = +2: HR 0.91 (0.84–0.99), non-linear.
  - fPC2: HR 0.98 (0.94–1.03).
  - fPC3: HR 0.88 per unit (0.83–0.93).
  - fPC4: HR 1.16 per unit (1.08–1.25).
  - Quote (abstract): "A fPC1 score of + 2 (high overall PA) was inversely associated with mortality (Hazard ratio, HR = 0.91; 95% CI: 0.84-0.99), whereas a score of -2 (low overall PA) was associated with higher mortality (1.69; 95% CI: 1.57-1.81; p for non-linearity < 0.001)."
  - Source: [PMC10472628](https://pmc.ncbi.nlm.nih.gov/articles/PMC10472628); [Springer](https://link.springer.com/10.1186/s12966-023-01508-z)
- No C-index is reported, and there is no head-to-head comparison with a total-volume scalar model. The authors note: "Correlations between fPCs and accelerometer-derived PA variables were rather weak." Their own conclusion plays down the shape components: "it is less important during which daytime hours one is active" — [PMC10472628](https://pmc.ncbi.nlm.nih.gov/articles/PMC10472628)
- Limitations the authors state: possible reverse causation (excluding deaths in the first 2 years did not change the results), confounding by occupation, and differential misclassification — [PMC10472628](https://pmc.ncbi.nlm.nih.gov/articles/PMC10472628)
- A medRxiv preprint version exists (10.1101/2022.12.05.22283101). Cite the peer-reviewed IJBNPA version — [medRxiv](https://www.medrxiv.org/content/10.1101/2022.12.05.22283101v1.full)

**2. Zeitzer JM, et al. (MrOS Study Group). "Daily Patterns of Accelerometer Activity Predict Changes in Sleep, Cognition, and Mortality in Older Men." J Gerontol A Biol Sci Med Sci 2018;73(5):682–687. DOI 10.1093/gerona/glw250 (Crossref verified, online 2017-02-03). Peer-reviewed; abstract only read, via Europe PMC.**
- Design: the prospective MrOS cohort of 2,976 older men. FPCA was applied to 4–7 days of activity patterns, with 6.5–8 years of mortality follow-up — [PubMed 28158467 / Europe PMC](https://pubmed.ncbi.nlm.nih.gov/28158467/)
- Results, quoted from the abstract:
  - "low daytime activity at baseline was associated with ... a 1.6-fold higher rate of all-cause mortality (hazard ratio = 1.64 [1.34-2.00])"
  - "Having a late afternoon peak in activity was associated with a 1.4-fold higher rate of all-cause mortality (hazard ratio = 1.46 [1.21-1.77])"
  - "Those having a longer duration of their daytime activity with a bimodal activity pattern also had over a 1.4-fold higher rate of cardiovascular-related mortality (hazard ratio = 1.42 [1.02-1.98])"
  - Conclusion: "Patterns of daily activity may be useful as predictive biomarkers."
  - Source: [Oxford Academic](https://academic.oup.com/biomedgerontology/article/73/5/682/2967602)
- Not verified (full text not read): the number of deaths, the covariate set, and whether the shape-component HRs are mutually adjusted with the amplitude (FPC1) score.

**3. Shi B, Wei P, Huang X. "Functional principal component based landmark analysis for the effects of longitudinal cholesterol profiles on the risk of coronary heart disease." Stat Med 2021;40(3):650–667. DOI 10.1002/sim.8794 (Crossref verified, online 2020-11-05). Peer-reviewed; full text read via PMC.**
- Design: Framingham Offspring. n = 1,669 unrelated people aged 25–75, with 110 CHD events (6.59%). Total cholesterol was measured at 7 visits — [PMC9580044](https://pmc.ncbi.nlm.nih.gov/articles/PMC9580044)
- Method: FPCA by PACE. Three FPCs explained 99% of the variation (72.0%, 17.5% and 10.0%). Scores entered landmark Cox models stacked into a "super model". Covariates were only sex and smoking — [PMC9580044](https://pmc.ncbi.nlm.nih.gov/articles/PMC9580044)
- Comparator: a landmark model using the last observed total cholesterol (LVCF). This is a single-value summary, not the mean. FPCA model AUC at a 5-year horizon (landmarks at 35, 50, 65 and 75 years) was 0.691, 0.691, 0.690 and 0.690. LVCF AUC was 0.591, 0.588, 0.589 and 0.592. The authors write that the FPCA model "has a better ability to distinguish between high-risk and low-risk subjects." In simulations, Brier scores were on average about tenfold lower — [PMC9580044](https://pmc.ncbi.nlm.nih.gov/articles/PMC9580044)
- Interpretation of the components: "subjects with positive values for the first FPC score during early ages 40 to 55 would have lower CHD risks." FPC3 coefficients stayed near zero — [PMC9580044](https://pmc.ncbi.nlm.nih.gov/articles/PMC9580044)
- Caveats:
  - This is a methods paper with a demonstration application. No numeric HRs are given (only coefficient plots).
  - The AUCs appear apparent (in-sample). I did not see cross-validation in what I read.
  - The comparator is weak (last value only, not mean or slope).

**4. Ratcliffe SJ, Heller GZ, Leader LR. "Functional data analysis with application to periodically stimulated foetal heart rate data. II: Functional logistic regression." Stat Med 2002;21(8):1115–1127. DOI 10.1002/sim.1068 (Crossref verified). Peer-reviewed; abstract only.**
- Design: functional logistic regression of the fetal heart rate curve (basis expansion), with optional scalar covariates, for the risk category of the birth outcome. The abstract reports that the tracings "could predict 94.1 per cent of the high risk pregnancies". Without the stimulus, "the heart rates were no more predictive than chance" — [Macquarie](https://researchers.mq.edu.au/en/publications/functional-data-analysis-with-application-to-periodically-stimula-2/); [scispace](https://scispace.com/papers/functional-data-analysis-with-application-to-periodically-2kdf8br0vs)
- Caveat: this is a basis-expansion functional GLM, not strictly FPC scores. The sample is small and from a clinical series. The result is apparent accuracy.

**5. Geometry analogue (not an outcome model): Sangalli LM, Secchi P, Vantini S, Veneziani A. "A Case Study in Exploratory Functional Data Analysis: Geometrical Features of the Internal Carotid Artery." JASA 2009;104(485):37–48. DOI 10.1198/jasa.2009.0002 (Crossref verified). Peer-reviewed; full text read from the authors' posted PDF, which may differ slightly from the typeset version.**
- Design: the AneuRisk project, with 65 hospital patients from 3D angiography:
  - 33 with an aneurysm at or after the ICA terminal bifurcation (Upper group);
  - 25 with an aneurysm along the ICA;
  - 7 healthy.
  - The last two are pooled as the Lower group (n = 32).
  - Source: [author PDF](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- Method: registration of centerlines, then FPCA of the radius and curvature profiles along the artery, then quadratic discriminant analysis on the first 2 radius and first 2 curvature FPC scores — [author PDF](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- Result: "According to L1ER, if kR = kC = 2 are used, 21.54% of the new patients would be misclassified". Leave-one-out misclassification was 28.12% in the Lower group and 15.15% in the Upper group. Upper-group patients "have significantly wider, more tapered and less curved ICA's" — [author PDF](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- Caveat: this is a cross-sectional referral series. The outcome is aneurysm location, not incident disease. The model is QDA, not a GLM.

**Weaker fits found (not recommended as the main citation):**
- Xu SY, et al. "Modeling Temporal Variation in Physical Activity Using Functional Principal Components Analysis." Stat Biosci 2019;11:403–421. DOI 10.1007/s12561-019-09237-3 (Crossref verified). The sample is 578 overweight women, and the outcome is cross-sectional (quality-of-life type), not a clinical event. The full-text PDF was skimmed — [PDF](https://d-nb.info/1185234462/34)
- Gestational weight FPCA (PLoS One 2017) found that trajectory covariates gave R² and MSE identical to a simple linear regression. This is a useful negative example — [PLoS One](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0186761)

**Preprints (flagged, not for recommendation):**
- Generalized multilevel FPCA of NHANES 2011–2014 active/inactive patterns: Cox model on fPC scores, n = 4,445, first eigenfunction HR 0.66 (arXiv 2311.14054). This is a preprint — [arXiv](https://arxiv.org/html/2311.14054)
- Comparison of Gaussian FPCA, Poisson FPCA and NARFD scores for 5-year mortality in NHANES 2005–2006 using logistic regression, random forest and AdaBoost (arXiv 2105.14649). Its peer-reviewed status was not checked — [arXiv](https://arxiv.org/html/2105.14649)

### Inferences
- The FPCA -> scores -> Cox pattern is used routinely in large prospective cohorts (accelerometry), so it is a recognised design, not an ad hoc one. This supports describing the thesis approach as standard practice.
- In both accelerometry cohorts, FPC1 is overall volume and dominates. Shape components (fPC3/fPC4 in UK Biobank, the late-afternoon peak in MrOS) carry additional, smaller associations. This parallels the thesis setup: a level-type FPC1, close to mean curvature, plus shape scores.

### Gaps
- MrOS: deaths, covariates, and whether the shape HRs are adjusted for amplitude are not verified (abstract only).
- Ratcliffe 2002: the full text was not read, so the model details and validation are unverified.

## Which show that FPC scores add beyond the mean/scalar summary or beyond standard risk factors?

### Takeaway
I found no peer-reviewed clinical cohort study that reports a formal discrimination gain (ΔC/ΔAUC) of FPC scores over the scalar mean of the same curve, on top of a base risk model. The nearest evidence is partial:
- Shi et al. 2020 shows an AUC gain over a single-value summary (0.69 vs 0.59), but only sex and smoking were in the model.
- UK Biobank and MrOS show that non-volume shape components carry independent hazard ratios beside standard covariates, without reporting a C-index.

### Cited findings
- Shi et al. 2020: FPC-score landmark model AUC ≈ 0.69 vs ≈ 0.59 for the last-value model, Framingham, 110 CHD events — [PMC9580044](https://pmc.ncbi.nlm.nih.gov/articles/PMC9580044)
- Stein et al. 2023: fPC3 (HR 0.88) and fPC4 (HR 1.16 per unit) were associated with mortality after multivariable adjustment. fPCs correlate only "rather weakly" with scalar PA variables. No C-index and no total-volume comparison model were reported, and none of the sensitivity analyses compared fPCs with total volume — [PMC10472628](https://pmc.ncbi.nlm.nih.gov/articles/PMC10472628)
- Zeitzer et al. 2018: a late-afternoon activity peak gave HR 1.46 (1.21–1.77) for all-cause mortality, separately from the low-daytime-activity (amplitude) component, which gave HR 1.64 — [Europe PMC/PubMed abstract](https://pubmed.ncbi.nlm.nih.gov/28158467/)
- Scalar accelerometry summaries alone are strong predictors. In NHANES (n = 2,978 aged > 50, 297 deaths), total activity count was the best single predictor of 5-year mortality (AUC 0.771), ahead of age (0.758). That paper (Smirnova et al., J Gerontol A 2020) used scalar summaries, not FPCA. So a scalar summary can already capture much of the signal — [PMC7494021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7494021/)
- The gestational weight FPCA study found no gain over simple regression (identical R² and MSE) — [PLoS One](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0186761)

### Inferences
- The claim the literature supports is: "FPC scores entered beside standard covariates in a Cox/GLM are an established way to use a whole curve, and shape components can carry associations separate from the level component". The claim "FPC scores have been shown to improve discrimination over the scalar mean" is not supported by what I found. Avoid it, or phrase it as untested.
- This fits the thesis treating the FPC analysis as descriptive and secondary.

### Gaps
- I found no study with ΔC of FPC scores vs the mean of the same curve beside a clinical base score (e.g. SCORE2, PCE). The searches covered accelerometry, cholesterol trajectories, pregnancy BP, childhood growth and generic terms.
- CGM, ECG/pulse waveforms, eGFR trajectories and the CD4 work (Yao, Müller, Wang 2005, a methods paper) were not searched in depth because of the time budget.
- The NHANES-specific FPCA mortality papers by Leroux, Crainiceanu and colleagues were not located as peer-reviewed full texts in this pass. The Stat Biosci paper found turned out to be Xu et al. (a different design).

## Ranking: top 3 by fit (curve -> scores -> binary/time-to-event outcome beside a base risk model) and strength

### Takeaway
1. **Stein et al. 2023, IJBNPA (UK Biobank).** This is the best overall fit and strength: large and prospective, FPCA by PACE, a few scores in a multivariable Cox model beside standard risk factors, full text open. Weakness: no comparison with a scalar summary, and only a mid-tier journal.
2. **Zeitzer et al. 2018, J Gerontol A (MrOS).** Prospective, n = 2,976, FPCA scores in Cox models, with a shape component (not only volume) linked to mortality. Weakness: abstract-level verification only.
3. **Shi, Wei & Huang 2020/2021, Stat Med (Framingham CHD).** This is the only one with an explicit discrimination comparison against a simpler summary (AUC 0.69 vs 0.59), and it has a cardiovascular outcome. Weaknesses:
   - It is a methods paper.
   - It has 110 events and a minimal covariate set.
   - The comparator is the last value, not the mean.
   - The AUC is probably apparent.

As a domain analogue, not an outcome-model citation, **Sangalli et al. 2009 JASA** is the closest geometric precedent: FPCA of artery curvature and radius profiles, with scores used for classification. It is cross-sectional, with 65 referral patients.

### Cited findings
- See the sources above: [PMC10472628](https://pmc.ncbi.nlm.nih.gov/articles/PMC10472628), [PubMed 28158467](https://pubmed.ncbi.nlm.nih.gov/28158467/), [PMC9580044](https://pmc.ncbi.nlm.nih.gov/articles/PMC9580044), [Sangalli author PDF](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)

### Inferences
- A defensible thesis sentence would be: "Entering a few FPC scores of a profile beside standard covariates in a survival or binary-outcome model is an established design in large cohorts (Stein et al. 2023; Zeitzer et al. 2018), and FPC scores have been used for discrimination from arterial curvature and radius profiles (Sangalli et al. 2009)." It should not claim proven added discrimination over the mean.

### Gaps
- No top-journal (e.g. JAMA, Circulation, Lancet) clinical application with this exact design and a scalar-summary comparison was found.
