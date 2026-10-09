# Regression methodology for testing whether coronary geometry adds to risk factors for new plaque

Scope: CGPS (Herlev–Østerbro) serial CCTA, plaque-free at baseline, binary new plaque per artery domain (LM, LAD, LCx, RCA), risk factors plus geometry scalars plus functional PCA scores of curvature. Notes compiled 2026-10-07. Sources marked "secondary" were found only through aggregator or tutorial pages in this session and should be checked against the original before being cited in the thesis.

## 1. Explanation vs prediction framing, and how to show incremental value

### Takeaway
The question "does geometry add information beyond risk factors" is answered most powerfully and most simply by a likelihood-ratio (or Wald) test of the geometry coefficients in a regression that already contains the risk factors; delta AUC is a badly underpowered test of the same null, NRI is unreliable, and calibration plus decision curves are descriptive add-ons that matter only if a usable prediction tool is claimed.

### Cited Findings
- Shmueli (Statistical Science 25(3):289–310, 2010, doi 10.1214/10-STS330) argues that explanatory and predictive modelling are conflated in many disciplines, that high explanatory power does not imply high predictive power, and that the goal changes practical choices at every step of the modelling process ([Project Euclid](https://projecteuclid.org/euclid.ss/1294167961); [author PDF](https://www.stat.berkeley.edu/%7Ealdous/157/Papers/shmueli.pdf)).
- Pepe, Kerr, Longton and Wang ("Testing for improvement in prediction model performance", Stat Med 2013) show that null hypotheses of no improvement in ROC AUC, IDI, change in risk distribution and some reclassification measures are all equivalent to the null that the new predictor's coefficient is zero in the risk model, so a separate test of improvement is redundant once the predictor is shown to be a risk factor ([EDRN abstract page](https://edrn.nci.nih.gov/data-and-resources/publications/23296397-2080-testing-for-improvement-in-prediction-model-performance/); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3617074)).
- Vickers, Cronin and Begg ("One statistical test is sufficient for assessing new predictive markers", BMC Med Res Methodol 2011;11:13): the area (delta AUC) test had much lower power than the likelihood ratio and Wald tests and was extremely conservative, with test size below 0.006 in all configurations studied; they conclude that significance of a new predictor given existing ones is best assessed within the regression model ([PMC3042425](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3042425/); [Springer](https://link.springer.com/article/10.1186/1471-2288-11-13)).
- Pepe, Fan, Feng, Gerds, Hilden ("The Net Reclassification Index (NRI): a misleading measure of prediction improvement even with independent test data sets", Stat Biosci 2015): NRI computed on a large test set from a training-set model is likely positive even when the new marker carries no information, because poorly fitting models inflate it; ROC-, net-benefit- and Brier-based measures do not have this defect ([EDRN](https://edrn.cancer.gov/data-and-resources/publications/26504496-the-net-reclassification-index-nri-a-misleading-measure-of-prediction-improvement-even-with-independent-test-data-sets); [PMC4615606](https://pmc.ncbi.nlm.nih.gov/articles/PMC4615606)).
- Kerr et al. (Epidemiology 2014) recommend that if NRI is used its event and non-event components are always reported separately (as summarised in [EDRN/search summary](https://edrn.nci.nih.gov/data-and-resources/publications/26504496-the-net-reclassification-index-nri-a-misleading-measure-of-prediction-improvement-even-with-independent-test-data-sets); original not fetched).
- Vickers, Van Calster, Steyerberg ("Net benefit approaches to the evaluation of prediction models, molecular markers, and diagnostic tests", BMJ 2016;352:i6): net benefit puts benefits and harms on one scale via a threshold-probability exchange rate, and a decision curve plots it across thresholds to judge whether using a model or marker does more good than harm ([Duke Scholars](https://scholars.duke.edu/publication/952669); [MSKCC record](https://synapse.mskcc.org/synapse/works/90307)).
- Steyerberg, Vickers et al. also reviewed incremental-value methods ("Assessing the incremental value of diagnostic and prognostic markers: a review and illustration") ([Erasmus](https://pure.eur.nl/en/publications/assessing-the-incremental-value-of-diagnostic-and-prognostic-mark/); content not fetched).

### Inferences
- The thesis question is primarily explanatory/associational in Shmueli's sense ("is geometry associated with new plaque after adjustment"), with a secondary predictive question ("does it improve predictions"). The nested-model LRT plan (Model 0 vs Model 1 vs Model 2) is the correct primary inferential test and should be framed as such; the LRT should be done on unpenalised (or Firth) maximum-likelihood fits, since LRTs on ridge-penalised fits do not have the usual chi-square reference distribution.
- Report delta AUC (optimism-corrected) and calibration as descriptive effect sizes, not as hypothesis tests. Skip NRI or, if a reviewer insists, report category-free components separately. Decision curves are only meaningful if a clinical action threshold exists; for an asymptomatic population with no defined action on "new plaque risk" they may be presented as exploratory.
- A clean way to phrase it: "inference by LRT on the full sample; predictive performance (AUC, calibration slope, Brier) by bootstrap optimism correction".

### Gaps
- Did not fetch full texts of Pepe 2013 or Kerr 2014 to quote exact simulation numbers beyond the abstracts above.

## 2. Sample size, EPV, and penalisation

### Takeaway
Use Riley et al. (BMJ 2020) criteria via `pmsampsize` to state the maximum number of candidate parameters the expected number of events supports; EPV=10 has no firm basis. Ridge/lasso/Firth reduce average overfitting but do not rescue a too-small sample, because the tuning parameter itself is estimated with large uncertainty exactly when shrinkage is most needed.

### Cited Findings
- Riley, Ensor, Snell et al. ("Calculating the sample size required for developing a clinical prediction model", BMJ 2020;368:m441, published 18 March 2020) give a stepwise calculation conditional on outcome prevalence, number of candidate predictor parameters and anticipated Cox-Snell R²; for binary outcomes effective sample size is about min(events, non-events) ([Utrecht repository](https://dspace.library.uu.nl/handle/1874/457642); [pmsampsize docs](https://archive.linux.duke.edu/cran/web/packages/pmsampsize/refman/pmsampsize.html)).
- The binary-outcome criteria (Riley et al., Stat Med 2019, Part II, and BMJ 2020): (i) expected global shrinkage factor ≥0.9 (predictor effects shrink ≤10%), (ii) absolute difference ≤0.05 between apparent and adjusted Nagelkerke R², (iii) overall risk estimated within ±0.05; the anticipated Cox-Snell R² must be prespecified, ideally from previous studies ([pmsampsize manual](https://erised.las.iastate.edu/CRAN/web/packages/pmsampsize/pmsampsize.pdf); [Keele repository](https://keele-repository.worktribe.com/OutputFile/461007); [PMC10439652](https://pmc.ncbi.nlm.nih.gov/articles/PMC10439652)). The BMJ paper also discusses a fourth criterion on mean absolute prediction error and a default of assuming Cox-Snell R² equal to 15% of its maximum when no prior R² exists; I could not fetch the BMJ full text (403) to confirm the exact wording, so verify before citing.
- The 10-EPV rule of thumb is widely used ([pmsampsize docs summary of Riley 2020](https://archive.linux.duke.edu/cran/web/packages/pmsampsize/refman/pmsampsize.html)), but van Smeden et al. ("No rationale for 1 variable per 10 events criterion for binary logistic regression analysis", BMC Med Res Methodol 2016;16:163) found by simulation that evidence for EPV rules is weak and that small-sample problems depend also on total sample size and other factors; they compared ML and Firth's correction ([PMC5122171](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5122171/)).
- Van Calster, van Smeden, De Cock, Steyerberg ("Regression shrinkage methods for clinical prediction models do not guarantee improved performance: simulation study", Stat Methods Med Res 2020) compared ML with uniform shrinkage, ridge, lasso, adaptive lasso and Firth: shrinkage improved calibration slopes on average but increased between-sample variability of the slope, often worked poorly in individual datasets especially when most needed, and "do[es] not solve problems associated with small sample size or low number of events per variable" ([arXiv 1907.11493](https://arxiv.org/abs/1907.11493); [KU Leuven PDF](https://lirias.kuleuven.be/bitstream/123456789/655306/2/Regression%20shrinkage%20for%20clinical%20prediction%20models%202nd%20REVISION%20SUBMITTED%20TO%20SMMR.pdf)).
- Riley, Snell, Martin et al. ("Penalization and shrinkage methods produced unreliable clinical prediction models especially when sample size was small", J Clin Epidemiol 2021) examined uniform shrinkage, ridge, lasso and elastic net: tuning parameters are estimated with large uncertainty, most problematic with small effective sample size and low Cox-Snell R², leading to considerable miscalibration; penalisation is "not a carte blanche" and is best applied with sample sizes meeting the Riley criteria ([Birmingham PDF](https://research.birmingham.ac.uk/files/187644934/1_s2.0_S0895435620312099_main.pdf); [ORA Oxford](https://ora.ox.ac.uk/objects/uuid:9de839aa-8a9d-4234-9ed3-c45e4d05ee13)).
- Pavlou et al. (Biometrical Journal 2024) propose modified cross-validation and bootstrap tuning of penalised regression to reduce this instability ([UCL PDF](https://discovery.ucl.ac.uk/10194305/1/Pavlou_Biometrical%20J%20-%202024%20-%20Pavlou%20-%20Penalized%20Regression%20Methods%20With%20Modified%20Cross%E2%80%90Validation%20and%20Bootstrap%20Tuning%20Produce%20%281%29.pdf); content not fetched).

### Inferences
- Parameter budget is the binding constraint. Rough count: age, sex, dominance, smoking, LDL, SBP, diabetes, BMI/statin, interval ≈ 9–11 df; geometry scalars ≈ 4–6 df (more if splined or per-domain); curvature PCs 3–5 per artery. With, say, 50 events per domain, Riley criterion (i) will typically allow only around 5–10 parameters at plausible R², so Model 2 per domain is almost certainly over budget. Run `pmsampsize` with the expected prevalence and a conservative R² before fixing the model, and report it (TRIPOD+AI requires a sample size justification).
- Options when events are few: (a) pool domains into one participant-domain model with domain as a factor and common geometry slopes (more events per parameter, clustering handled as in section 4); (b) data reduction blinded to outcome (e.g. fewer PCs, a single summary per geometry feature, Harrell-style redundancy analysis); (c) Firth for the LRT/inference fits to remove small-sample bias and separation; (d) ridge only for the predictive-performance arm, with the caveat from Van Calster 2020 and Riley 2021 stated explicitly and the tuning instability shown (e.g. distribution of bootstrap lambdas).
- Do not choose lasso for the primary analysis: variable selection is unstable at this size and undermines the "geometry block adds information" test.

### Gaps
- Exact text of the BMJ 2020 fourth criterion and the 15%-of-max-R² default could not be verified (BMJ 403, PMC captcha).
- No published anticipated R² exists for "new plaque in plaque-free baseline CCTA"; an R² from CAC-incidence studies would have to be converted.

## 3. Nonlinearity: restricted cubic splines

### Takeaway
Harrell's RMS approach is to prespecify restricted cubic splines (3–5 knots at fixed quantiles) for continuous predictors where nonlinearity is plausible and the df budget allows, rather than to test linearity and then decide; each k-knot spline costs k−1 df.

### Cited Findings
- Restricted cubic splines with k knots spend k−1 df; default knot placement at quantiles (5th, 27.5th, 50th, 72.5th, 95th for 5 knots); Harrell's RMS suggests about 3 knots for very small n, 4–5 for moderate, 5 for n ≥ 200, and 5 or fewer is usually sufficient (secondary summaries: [MetricGate](https://metricgate.com/blogs/restricted-cubic-splines-regression/); [Frontiers in Epidemiology 2023 tutorial](https://www.frontiersin.org/journals/epidemiology/articles/10.3389/fepid.2023.1283705/full); [Statalist archive](https://stata.com/statalist/archive/2004-11/msg00441.html)). Verify against RMS 2nd ed. (Springer 2015), ch. 2.4, before citing.

### Inferences
- Given the df budget in section 2, splines should be reserved for age (known nonlinear) and possibly LDL, with 3 knots; geometry features can enter linearly in the primary model, with 3-knot splines as a sensitivity analysis or allocated by Harrell's "spend df where the predictive potential is highest" rule decided before looking at outcome associations.
- Never categorise continuous geometry (e.g. "angle > 80°") in the primary analysis; it wastes information.

### Gaps
- Did not access RMS directly in this session; knot-number table is from secondary sources.

## 4. Correlated outcomes across the four artery domains

### Takeaway
Options are (a) four separate per-domain logistic models, (b) a pooled participant-domain logistic model with cluster-robust (GEE/sandwich) inference, giving population-averaged effects, (c) a random-intercept logistic model, giving participant-specific effects, all with participant-level (cluster) bootstrap for validation. Methodological work on clustered prediction models shows calibration depends on whether the model and the validation measure match the clustered structure.

### Cited Findings
- Random-effects models and GEE are the two common approaches for clustered data, giving cluster-specific (conditional) and population-averaged (marginal) inference respectively (Bouwmeester et al., BMC Med Res Methodol 2013;13:19, [PDF](https://bmcmedresmethodol.biomedcentral.com/track/pdf/10.1186/1471-2288-13-19); Wynants et al., [PMC4525751](https://pmc.ncbi.nlm.nih.gov/articles/PMC4525751)).
- With high ICC (≥15%), calibration was adequate only when the performance measure matched the development method: standard measures for standard models, cluster-adapted measures for random-intercept models; calibration slopes deviate from 1 not only from overfitting but also from the model choice (standard vs mixed), prediction type (marginal, conditional, average random effect) and validation level ([search summary of Bouwmeester 2013 / Wynants 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4525751); [VU record](https://research.vu.nl/en/publications/prediction-models-for-clustered-data-comparison-of-a-random-inter/)).
- Random-intercept logistic calibration was better than standard logistic even under violated random-effect assumptions, and with ICC 20% cluster-specific predictions performed best (Wynants et al. [PMC7383814](https://pmc.ncbi.nlm.nih.gov/articles/PMC7383814); these studies concern patients clustered in centres, not outcomes clustered within patients).
- PARADIGM found per-lesion CCTA measures predicted development of obstructive lesions better than per-patient summaries, supporting sub-patient (segment/lesion-level) modelling in serial CCTA ([PARADIGM search result](https://pmc.ncbi.nlm.nih.gov/articles/PMC8385056)).

### Inferences
- Geometry is naturally domain-level (LAD curvature predicts LAD plaque), while risk factors are participant-level. A pooled participant-domain long-format model (outcome per domain, domain as factor, domain-specific geometry, participant risk factors) matches this and quadruples event counts relative to per-domain models, easing section 2's constraint.
- For the "geometry adds to risk factors" question, a marginal (GEE / logistic with cluster-robust SEs) model is the natural target: population-averaged odds ratios, easy LRT analogue (use a robust Wald or score test, since GEE has no likelihood) and straightforward bootstrap by participant. A random-intercept model is the alternative if the LRT is wanted directly; note that conditional ORs are larger in magnitude than marginal ORs and the predictions are not comparable to Model 0 calibration without care.
- Resampling must be at participant level (cluster bootstrap) in every validation step, including CV folds for ridge tuning; this is already in the plan and is correct.
- Per-domain separate models remain useful as secondary, descriptive analyses; LM is likely too event-poor to model alone.

### Gaps
- No found methodology paper specifically on prediction with multiple binary outcomes nested within the same individual (as opposed to individuals within centres); ICC for new plaque across domains within a person is unknown.

## 5. Varying follow-up interval: logistic vs cloglog vs interval-censored survival

### Takeaway
"New plaque between two scans" is interval-censored: onset is known only to lie between baseline and follow-up. A binary GLM with complementary log-log link and offset log(interval) is exactly the grouped-data proportional hazards model and handles unequal intervals in a principled way; logistic with interval as a covariate is an acceptable approximation when risk is low.

### Cited Findings
- Grouped/interval-censored survival data, where only the interval containing the event is known, can be analysed with the discrete proportional hazards model of Prentice and Gloeckler (1978) and Allison (1982), which is equivalent to a binary response model with complementary log-log link (SAS PROC LOGISTIC documentation, [SAS example](https://go.documentation.sas.com/api/docsets/statug/v_016/content/statug_logistic_examples19.htm); [SAS code](https://support.sas.com/documentation/onlinedoc/stat/ex_code/121/logiex14.html)).
- Interval censoring arises e.g. when time to onset is known only to lie between two health examinations ([Wellner/Huang lecture notes, U. Washington](https://sites.stat.washington.edu/jaw/JAW-papers/NR/jaw-huang-97LNS-SBS.pdf)).
- MESA incident-CAC analyses (e.g. family history and incident CAC, mean time between scans 3.1 ± 1.3 years, OR 1.55 for premature family history) used regression adjusted for demographics and risk factors ([MESA family history paper, PMC4491495](https://pmc.ncbi.nlm.nih.gov/articles/PMC4491495)); Kronmal et al. (Circulation 2007) studied risk factors for CAC progression in MESA ([search record](https://scholars.houstonmethodist.org/en/publications/cardiovascular-events-with-absent-or-minimal-coronary-calcificati/)). I could not open these papers to confirm whether incident CAC was modelled with relative-risk regression with an interval term.

### Inferences
- With one follow-up scan per person, cloglog with offset log(Δt) assumes a constant hazard over the interval and gives hazard ratios; if intervals vary modestly (e.g. 3–6 years) and event risk is low, logistic with log(Δt) or Δt as covariate gives nearly identical inference. A reasonable primary choice: cloglog with offset (a defensible "rate" interpretation); sensitivity: logistic with interval covariate. Full interval-censored survival (e.g. `icenReg`, Turnbull) adds nothing with a single follow-up visit per person.
- If interval is an offset, check proportionality by also fitting log(Δt) as a free covariate; a coefficient near 1 supports the offset.
- Risk factors measured at baseline only: say so, and note that statin initiation between scans is a time-varying confounder of plaque incidence.

### Gaps
- Could not find a CCTA plaque-incidence paper that explicitly used cloglog; the MESA modelling choice remains unverified in this session.

## 6. Functional predictors (curvature profiles via FPCA)

### Takeaway
Entering the first few FPCA scores of a curve into a GLM is the standard functional generalised linear model approach, and there is direct vascular precedent: the AneuRisk project used FPCA of internal carotid curvature and radius profiles to discriminate aneurysm location, and Gervini used a logistic model on curvature profiles with warping.

### Cited Findings
- Sangalli, Secchi, Vantini, Veneziani (JASA 2009, AneuRisk): explored relations between internal carotid artery geometry, expressed by radius profile and centerline curvature, and aneurysm location; used iterative curve registration to remove phase variability, FPCA for dimension reduction, and quadratic discriminant analysis on FPC scores to discriminate patients with aneurysms in different districts ([JASA PDF](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf); [JASA](https://informahealthcare.com/doi/abs/10.1198/jasa.2009.0002)).
- Gervini (EJS 2014, "Analysis of AneuRisk65 data: warped logistic discrimination") modelled curvature profiles with likelihood-based warping inside a logistic regression for upper vs lower aneurysms; including warping functions significantly lowered misclassification ([arXiv 1310.2236](https://arxiv.org/pdf/1310.2236)); the EJS 2014 AneuRisk65 special section and rejoinder contain several competing functional analyses ([Project Euclid](https://projecteuclid.org/euclid.ejs/1414588181); [rejoinder](https://re.public.polimi.it/retrieve/e0c31c08-fc9c-4599-e053-1705fe0aef77/2014_Sangalli-Secchi-Vantini_EJS_AneuRisk65_rejoinder.pdf)).

### Inferences
- FPC scores enter the logistic model as ordinary continuous predictors, so Model 2's LRT with df = number of retained PCs is valid. The number of PCs should be fixed before outcome analysis (e.g. 80–90% variance, or 2–3 PCs), not tuned on outcome, otherwise the LRT is anticonservative.
- FPCA should be fitted inside each bootstrap resample (or at least acknowledged as an unsupervised step outside); since it does not use the outcome, fitting it once on all participants introduces little optimism, which is the usual practice.
- The AneuRisk work shows that registration (alignment of arc length, e.g. to bifurcations) materially changes results; coronary profiles should be parametrised on anatomical landmarks (ostium, first major branch) before FPCA.
- AneuRisk n was 65, so it is precedent for the method, not for sample size.

### Gaps
- Found no published study using FPCA of coronary curvature in a regression for plaque outcomes; this appears to be a genuine gap (a novelty point for the thesis).
- Did not search penalised functional logistic regression (e.g. `refund::pfr`) literature in this session.

## 7. Precedent in CCTA / CAC incidence and progression cohorts

### Takeaway
Population CCTA cohorts use logistic regression for cross-sectional plaque presence and Cox models for events; serial-CCTA registries (PARADIGM) use multivariable logistic models and risk scores for progression; MESA uses regression for incident CAC with adjustment for time between scans. None found used geometry beyond plaque/lumen measures.

### Cited Findings
- SCAPIS: population-based cohort of 30,154 adults aged 50–64 from six Swedish cities (2013–2018) with CCTA; associations between risk factors and coronary atherosclerosis were evaluated with logistic regression and incident events with Cox models (JACC Cardiovasc Imaging 2026, Lp(a) paper) ([JACC](https://www.jacc.org/doi/10.1016/j.jcmg.2026.05.020)).
- In SCAPIS, adding total plaque volume to risk scores improved discrimination and reclassification for events, with adjusted HR up to 6.36 in the highest category, and HR 2.63–5.26 for TPV >0 among CAC=0 (as reported in the same search result; original paper not fetched, verify which SCAPIS paper these numbers come from) ([JACC](https://www.jacc.org/doi/10.1016/j.jcmg.2026.05.020)).
- CGPS: Fuchs et al., "Subclinical coronary atherosclerosis and risk for myocardial infarction in a Danish cohort: a prospective observational cohort study", Ann Intern Med 2023 (doi 10.7326/M22-3027) found CCTA-detected atherosclerosis associated with about eight-fold MI risk ([AuntMinnie Europe news](https://www.auntminnieeurope.com/clinical-news/article/15657736/subclinical-atherosclerosis-increases-heart-attack-risk-8-fold); [Wiley knowledge hub](https://ascvd-lipidology.knowledgehub.wiley.com/subclinical-coronary-atherosclerosis-and-risk-for-myocardial-infarction-in-a-danish-cohort-a-prospective-observational-cohort-study/)). Modelling details not retrieved.
- PARADIGM: multinational registry of 2,252 patients with clinically indicated serial CCTA ≥2 years apart at 13 sites in 7 countries (2003–2015); multivariable analyses of progression; a practical CCTA-based progression risk score for non-obstructive plaque (Eur Radiol 2023); per-lesion measures outperformed per-patient measures for predicting new obstructive lesions ([Eur Radiol 2023](https://link.springer.com/article/10.1007/s00330-023-09880-x); [PMC8385056](https://pmc.ncbi.nlm.nih.gov/articles/PMC8385056); [Radiology 2021](https://pubs.rsna.org/doi/abs/10.1148/radiol.2021202630)).
- MESA: incident CAC modelled with regression adjusted for demographics and risk factors; family history of premature CHD OR 1.55 for incident CAC, mean scan interval 3.1 ± 1.3 years ([PMC4491495](https://pmc.ncbi.nlm.nih.gov/articles/PMC4491495)); Kronmal et al. Circulation 2007 is the core MESA risk-factor/CAC-progression paper ([record](https://scholars.houstonmethodist.org/en/publications/cardiovascular-events-with-absent-or-minimal-coronary-calcificati/)).

### Inferences
- The proposed analysis (multivariable logistic or cloglog with risk-factor adjustment and scan interval) is consistent with how the field models incident disease between two imaging exams. The novel elements are the per-domain outcome and geometry predictors, which justify the clustered-data handling and the explicit sample size reasoning.
- PARADIGM is clinically referred, not asymptomatic; its effect sizes should not be used as the anticipated R² for CGPS without caveat.

### Gaps
- Could not confirm the exact model (relative-risk regression vs logistic) used in Kronmal 2007 or how MESA handled unequal intervals.
- No CGPS serial-CCTA paper on incident plaque was found; whether CGPS has published rescan results is unknown from this search.
- No CONFIRM-specific modelling details were retrieved (CONFIRM is mostly single-scan with events follow-up).

## Overall recommendation (synthesis of the above)

### Takeaway
Logistic (or cloglog) regression is the right primary analysis. Recommended structure: (1) prespecified pooled participant-domain model with domain factor, participant risk factors, scan interval (offset under cloglog), and domain-level geometry; (2) inference on geometry by LRT (Firth-ML or mixed model) or robust Wald (GEE) comparing nested blocks; (3) predictive performance by participant-level bootstrap optimism correction reporting AUC, calibration slope/intercept and Brier for Model 0 vs 1 vs 2; (4) ridge only as a secondary predictive model with acknowledged tuning instability; (5) `pmsampsize` justification and TRIPOD+AI reporting.

### Cited Findings
- LRT over delta AUC ([Vickers 2011](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3042425/)); NRI caution ([Pepe 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4615606)); penalisation caveats ([Van Calster 2020](https://arxiv.org/abs/1907.11493); [Riley 2021](https://research.birmingham.ac.uk/files/187644934/1_s2.0_S0895435620312099_main.pdf)); sample size ([Riley 2020 via pmsampsize](https://archive.linux.duke.edu/cran/web/packages/pmsampsize/refman/pmsampsize.html)); cloglog for grouped survival ([SAS](https://go.documentation.sas.com/api/docsets/statug/v_016/content/statug_logistic_examples19.htm)); clustered prediction ([Bouwmeester 2013](https://bmcmedresmethodol.biomedcentral.com/track/pdf/10.1186/1471-2288-13-19)).

### Inferences
- The current plan's main weak point is the parameter budget per domain; pooling domains and fixing PC count/knots in advance are the two largest levers.
- Running ridge and then an LRT on the ridge fit would be incoherent; keep inferential and predictive arms separate.

### Gaps
- TRIPOD+AI (Collins et al., BMJ 2024) and TRIPOD-Cluster were not fetched in this session; checklist items should be read from the original.
