# Serial-CCTA design: does baseline coronary geometry of healthy trees predict new plaque or events about 10 years later in CGPS / Herlev-Østerbro?

Scope note. This file builds on, and does not repeat, `research_notes/Plaque prone regional geometry descriptors/longitudinal_design.md` (region correspondence, labeller accuracy, per-region mixed/GEE model, ComBat, a first power chain) and `research_notes/Centerline tortuosity normal ranges/normality_outcome_readiness.md` (determinants of tortuosity, measure requirements, sample-size table, go/no-go gates). New here: CGPS cohort facts beyond the 2023 paper, the only published 10-year serial-CCTA precedent (Amsterdam), MESA incident-CAC rates as a proxy for 10-year incidence in a plaque-free group, SCAPIS added-value numbers as the realistic ceiling for a prediction claim, a correction to the attenuation arithmetic used in the two earlier notes, a minimum-detectable-effect table by serial-subset size, and a concrete design and pre-registration list.

Evidence tags: [FT] full page body read (via fetch summary); [ABS] abstract or search snippet only; [REPO] repo file; [CALC] computed in this session; [INF] my inference. Tool budget meant most CGPS papers were reached only as abstracts or snippets; publisher pages (PubMed, ScienceDirect, Springer) returned captcha or login redirects.

## 1. What is known about CGPS / Herlev-Østerbro CCTA, and what outcomes exist

### Takeaway
CGPS is a Copenhagen population cohort (started 2003, examinations at Herlev Hospital) in which about 10,000 participants aged 40 or older opted into a research CCTA at Rigshospitalet from February 2010 on a 320-detector Toshiba/Canon Aquilion One; plaque was read per SCCT segment, and MI, revascularisation and death come from registry linkage with median follow-up now about 6 years. I found no public paper describing a CGPS repeat-CCTA substudy, so the size, interval, selection and reading protocol of the ~10-year rescan subset must come from the supervisors.

### Cited Findings
- 9,533 asymptomatic persons aged 40 or older without known ischaemic heart disease; about half had plaque, 10% obstructive disease; extent defined as "one third or more of the coronary tree"; CCTA "conducted blinded to treatment and outcomes"; median follow-up 3.5 years (range 0.1 to 8.9), 193 deaths and 71 MI; primary outcome MI, secondary death or MI; obstructive and extensive disease each about 8-fold MI risk [ABS] ([Fuchs et al., Ann Intern Med 2023;176(4)](https://www.acpjournals.org/doi/10.7326/M22-3027)). Note: one search summary says 36% had extensive plaque, the earlier repo note says 10%; the figure must be checked in the full text before it is quoted.
- A newer CGPS CCTA analysis (sex differences) reports 10,003 participants over 40 (5,710 women, 57%; 4,293 men), outcomes MI, death or MI, and clinically driven coronary revascularisation, median follow-up 6.0 years (IQR 3.9 to 9.5) [ABS] ([Eur Heart J advance article, ehag612](https://academic.oup.com/eurheartj/advance-article/doi/10.1093/eurheartj/ehag612/8759473)).
- CGPS participants are randomly selected inhabitants aged 20 to 100 of the Copenhagen area, examined at Herlev Hospital; "over 10.000" had cardiac CT at Rigshospitalet; cardiac CT was approved by the national ethics committee in 2010 [FT] ([Rigshospitalet cardiovascular CT projects page](https://rh-ct.org/projects/)).
- CCTA was added to the CGPS protocol in 2010; from February 2010 CGPS participants could opt for a research CCTA [ABS] (search summary of [Hjortkjær et al. 2019, Diab Vasc Dis Res](https://doi.org/10.1177/1479164118819961)). The opt-in wording implies a self-selected imaging subset of CGPS [INF].
- Scanner and protocol, from a reproducibility study including CGPS asymptomatic participants: 320-slice Aquilion One (Vision Edition), 320 x 0.5 mm collimation, prospective triggering, automatic phase selection with PhaseXact, median 120 kV; plaque segmented per SCCT guidelines; plaque volume intra-observer CCC 0.97 (CV 20%), inter-observer CCC 0.95 (CV 27%); reproducibility "generally decreased with worsening clinical risk profile" [FT] ([Reproducibility of quantitative CCTA in asymptomatic individuals and acute chest pain, PMC6294364](https://pmc.ncbi.nlm.nih.gov/articles/PMC6294364)).
- CGPS used two different MDCT scanners (calcium mass score calibration study) [ABS] ([Eur J Radiol](https://www.sciencedirect.com/science/article/abs/pii/S0720048X16304272)). Together with the "Vision Edition" above, this suggests at least two Aquilion One generations within the baseline period [INF].
- CGPS already published normal LV mass and chamber volumes from 320-detector CCTA [ABS] ([Fuchs et al., EHJ-CVI 2016, via ResearchGate](https://www.researchgate.net/publication/290432000_Normal_values_of_left_ventricular_mass_and_cardiac_chamber_volumes_assessed_by_320-detector_computed_tomography_angiography_in_the_Copenhagen_General_Population_Study)), and a paper on volume and dimensions of angiographically normal coronary arteries by MDCT exists [ABS] ([J Cardiovasc Comput Tomogr 2017](https://www.sciencedirect.com/science/article/abs/pii/S1934592517300862)). So LV mass (a direct heart-size covariate) is measurable from the same scans.
- Searches for a CGPS repeat or second CCTA returned no publication [search, this session].

### Inferences
- Baseline years 2010 onward plus a ~10-year interval means rescans from about 2020 onward; the earliest baseline participants are the only ones who can have a 10-year repeat, so the repeat subset over-represents early enrolees and whichever scanner generation was used first [INF].
- Clinical outcomes are available for the whole CCTA cohort (about 10,000), not only the rescan subset. The two endpoints therefore have very different denominators: new plaque only in returners, events in everyone. This is the main structural fact of the design [INF].
- Danish registry linkage (National Patient Registry for MI and revascularisation, Civil Registration and Causes of Death registries) is standard for CGPS, but the exact registries and adjudication were not confirmed from a full text here; state as "per CGPS publications" only after checking [INF].

### Gaps
- Size of the rescan subset, invitation rule (all, random, by baseline finding), response rate, interval distribution, follow-up scanner, and whether follow-up plaque was read per SCCT segment, as CAC, or quantitatively: not public.
- Which baseline participants had which scanner generation; cardiac phase policy (PhaseXact picks the quietest phase, which varies by heart rate).
- Covariate availability at the rescan (repeat blood pressure, lipids, statin start dates via prescription registry).

## 2. Outcome definitions and which fits a two-scan, 10-year design

### Takeaway
Primary imaging outcome: new plaque (any, TPV above a detection threshold or reader-positive) in baseline plaque-free units, following PARADIGM; per-patient "any new plaque" among participants plaque-free at baseline is the simplest and best-powered version, per-region new plaque is the mechanistic version. Baseline-diseased segments are excluded from the risk set (not modelled as progression) in the primary analysis. Registry events are a separate, whole-cohort secondary outcome with very low power for geometry.

### Cited Findings
- PARADIGM: risk set is SCCT segments with no plaque at baseline; new plaque is TPV at least 1 mm³ at follow-up; Cox per segment; 9,583 normal segments, 1,162 patients, interval at least 2 years [ABS, repo note] ([J Cardiovasc Comput Tomogr 2024](https://www.journalofcardiovascularct.com/article/S1934-5925(24)00032-7/abstract)).
- The only published per-protocol ~10-year serial CCTA cohort found: Amsterdam UMC, baseline 2008 to 2014 in suspected CAD; 539 invited (465 eligible in the diabetes paper), 299 rescanned, 267 to 274 analysed after excluding CABG; median interval 10.2 years (IQR 8.7 to 11.2); baseline Philips at least 64-slice at 75% R-R, follow-up Siemens SOMATOM Force at 70% R-R; AI-QCT (Cleerly) on a modified SCCT 18-segment model with vessel matching; 10.5% of vessels excluded for image quality or stents; median PAV 2.5% to 6.1%, mean progression 0.4 ± 0.5% per year; baseline non-calcified plaque the only plaque predictor; linear regression adjusted for age, sex, risk factors, statins, "kV and scanner type at follow-up" [FT] ([Increased high-risk plaque burden in type 2 diabetes: 10-year follow-up, PMC12590748](https://pmc.ncbi.nlm.nih.gov/articles/PMC12590748/); [ESC 2023 abstract, Eur Heart J 44 Suppl 2 ehad655.152](https://academic.oup.com/eurheartj/article/44/Supplement_2/ehad655.152/7392901)).
- MESA, 3,116 participants with CAC = 0 at baseline and repeat scans up to 10 years (mean age 58, 63% women): 10-year prevalence of CAC > 0 was 53%, CAC > 10 36%, CAC > 100 8%; time to conversion from a Weibull model [ABS] ([Dzaye et al., JACC CV Imaging, "Warranty period of a calcium score of zero"](https://www.jacc.org/doi/10.1016/j.jcmg.2020.06.048)).
- In SCAPIS, a stenosis of at least 50% lost independent predictive value once segment involvement and non-calcified plaque were included [FT] ([SCAPIS CCTA prediction, PMC12598578](https://pmc.ncbi.nlm.nih.gov/articles/PMC12598578/)). Extent, not stenosis, carries the risk signal in asymptomatic people.

### Inferences
- Outcome ranking for this design [INF]:
  1. Per-patient any new plaque among baseline plaque-free participants (binary). Incidence is likely high: MESA shows 53% calcium conversion from CAC = 0 over 10 years, and CCTA detects non-calcified plaque as well, so per-patient p is probably 0.4 to 0.6, which is the best case for power. Predictor: patient-level geometry (per-vessel κ_a averaged, or three vessel values).
  2. Per-region new plaque in baseline plaque-free regions (binary, clustered). Mechanistic, matches the "low WSS at bends" hypothesis, but needs the region correspondence from the earlier note and the follow-up read at region level.
  3. Continuous plaque burden change (PAV or TPV) in all participants: needs quantitative reads at both scans with comparable software; scanner change biases volumes (the Amsterdam study adjusted for follow-up kV and scanner). Secondary only.
  4. Registry events (MI, revascularisation, death) in the whole CCTA cohort: see section 5 on power; exploratory.
- Segments with baseline plaque: exclude from the new-plaque risk set (PARADIGM convention). Do not model them as "progression", because progression of existing plaque is driven by baseline plaque composition (Amsterdam: non-calcified volume was the only predictor) and would dilute the geometry question. A secondary analysis can include all segments with baseline plaque status as a covariate. At patient level, "baseline plaque-free" should mean no plaque in any segment; participants with plaque elsewhere at baseline are excluded from outcome 1 but can contribute their plaque-free regions to outcome 2 with a patient-level baseline-plaque indicator (PARADIGM found baseline plaque OR 1.84 for new lesions, per the earlier note).
- Revascularised segments or CABG between scans make the follow-up read impossible; treat as a competing event at the region or patient level and report counts (the Amsterdam study excluded 32 CABG patients).
- A detection threshold matters: follow-up scanners are more sensitive, so require a fixed minimum (for example reader-positive plaque plus at least 1 mm³, or calcium Agatston > 0 as a scanner-robust sensitivity outcome) and state it before unblinding.

### Gaps
- How CGPS rescans are read (visual SCCT, CAC only, or AI-QCT) is unknown and decides between outcomes 1 to 3.
- No CCTA analogue of the MESA conversion rate for a general population was found; the per-patient CCTA incidence is extrapolated from calcium data.

## 3. What "normal" can mean: reference group choice and conditional reference intervals

### Takeaway
"Plaque-free at both scans" is a selection on the future and must not be the only reference definition: it conditions on survival, return for rescan and outcome, so it defines a "persistently healthy survivor" standard rather than a population reference, and using it and then testing whether deviation predicts plaque is circular. Pre-declare two quantities: a descriptive population reference (all baseline participants, conditional on age, sex and body/heart size, GAMLSS or LMS centiles) and a prescriptive healthy standard (baseline plaque-free, no hypertension or diabetes, never-smoker), with the both-scans-healthy group reported only as a sensitivity or a descriptive subgroup.

### Cited Findings
- WHO growth-standard methodology reviewed about 30 centile methods and chose GAMLSS with the Box-Cox power exponential distribution, which reduced to LMS (median, coefficient of variation, skewness as smooth functions of age) [ABS] ([Borghi et al., Stat Med 2006](https://onlinelibrary.wiley.com/doi/10.1002/sim.2227)).
- Age- and size-related reference ranges (spirometry) extend LMS to condition on age and body size simultaneously [ABS] ([Cole et al., Stat Med 2009](https://onlinelibrary.wiley.com/doi/10.1002/sim.3504)).
- Sample size and composition for reference centiles have been studied explicitly [ABS] ([PMC8008444](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8008444/)); CT-derived age- and sex-specific normative curves are an established pattern (intracranial volumes from head CT) [ABS] ([NeuroImage 2025](https://www.sciencedirect.com/science/article/pii/S1053811925002757)).
- CGPS itself published "normal values" of LV mass and chamber volumes from the same CCTA cohort [ABS] ([Fuchs 2016](https://www.researchgate.net/publication/290432000_Normal_values_of_left_ventricular_mass_and_cardiac_chamber_volumes_assessed_by_320-detector_computed_tomography_angiography_in_the_Copenhagen_General_Population_Study)), a local precedent for how the group defines a normal subgroup (definition not extracted).
- Determinants that the reference must condition on (from the earlier repo note): female sex and hypertension raise tortuosity, larger heart and LV mass lower it, age mostly raises it; cardiac phase changes curvature by about 11% [REPO] (`normality_outcome_readiness.md`, section 1).
- About half of the CGPS CCTA cohort has plaque [ABS] ([Fuchs 2023](https://www.acpjournals.org/doi/10.7326/M22-3027)).

### Inferences
- Three candidate reference groups and what each licenses [INF]:
  - A. All baseline CCTA participants (about 10,000): population reference; valid for "how unusual is this tree in Copenhagen adults of this age, sex and size". Available without the rescan data and without any outcome, so it can be built before unblinding.
  - B. Baseline plaque-free and risk-factor-free (no hypertension, diabetes, current smoking, statin): prescriptive "healthy" standard, the spirometry never-smoker analogue. Uses only baseline information, so no look-ahead bias. Hypertension must not be excluded if the standard is to be used on hypertensive people, or else report hypertension-conditional centiles; since hypertension raises tortuosity, excluding it shifts the standard downward.
  - C. Plaque-free at both scans: conditions on returning (alive, willing, not revascularised) and on the outcome. Using C to define normal and then asking whether deviation from C predicts new plaque is circular (future non-cases define the centre, so cases fall in the tails by construction). Use C only descriptively ("geometry of persistently healthy trees"), or for a stability analysis of geometry change in people without disease.
- Conditional reference model: GAMLSS for each vessel's κ_a (or log κ_a) with μ and σ as smooth functions of age, plus sex, and a size term (LV mass from CT if available, else a tree-size proxy), then report z-scores. The z-score is the natural predictor for the outcome model and for the top-5% outlier flag (objective 9).
- What "normal tortuosity" cannot mean: a threshold of disease. No outcome-anchored cut-off exists (no study linking continuous CCTA tortuosity to hard outcomes, per the earlier note), so "abnormal" means "statistically unusual given age, sex and size", not "harmful".

### Gaps
- No published coronary tortuosity centiles by age and sex exist to validate against (earlier note).
- Whether GAMLSS centiles are stable at the planned n for extreme centiles (2.5%, 97.5%) in subgroups was not computed.

## 4. Analysis model, adjustment, attrition, measurement error, change in geometry, scanner change

### Takeaway
For per-patient new plaque: logistic regression (or complementary log-log with log interval offset) on baseline geometry z-score, adjusted for age, sex, hypertension, diabetes, smoking, LDL, BMI, heart size, baseline scanner/phase, interval and follow-up scanner, weighted by inverse probability of returning for the rescan. For per-region outcomes: the within-between (Mundlak) random-effects logistic model already specified in the earlier note, with GEE as sensitivity. Use baseline geometry only as the exposure; geometry change is a descriptive or secondary quantity because it is partly caused by the outcome.

### Cited Findings
- The within-between random-effects model (patient mean of the predictor plus the within-patient deviation) "offers all that fixed effects can provide and more", separating within- and between-cluster effects [ABS] ([Bell, Fairbrother and Jones, Qual Quant 2019;53:1051-74](https://link.springer.com/article/10.1007/s11135-018-0802-x); [open PDF](https://research-information.bris.ac.uk/ws/portalfiles/portal/196855552/Bell2019_Article_FixedAndRandomEffectsModelsMak.pdf)).
- Random measurement error "can introduce bias to estimates of the association between a risk factor and a disease or make a true association statistically non-significant" [ABS] ([Hutcheon, Chiolero and Hanley, BMJ 2010;340:c2289, PubMed 20573762](https://pubmed.ncbi.nlm.nih.gov/20573762/)). A method to size a repeatability substudy for correcting a single continuous exposure exists [ABS] ([Int J Epidemiol "Reflection on modern methods", PubMed 31329929](https://pubmed.ncbi.nlm.nih.gov/31329929/)). UK Biobank estimated regression dilution ratios for 2,858 variables from repeat measurements [ABS] ([IJE 2023;52(5):1545](https://academic.oup.com/ije/article/52/5/1545/7202301)).
- A published guide on IPW for attrition in cohort studies exists ([BMC Med Res Methodol 2022, 10.1186/s12874-022-01533-9](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/s12874-022-01533-9)); the full text could not be retrieved (login redirect), so its specific recommendations are not quoted here.
- 10-year serial CCTA precedent handled scanner change by adjusting for follow-up kV and scanner type, not by harmonisation [FT] ([PMC12590748](https://pmc.ncbi.nlm.nih.gov/articles/PMC12590748/)).
- CGPS plaque reproducibility falls with higher risk profile [FT] ([PMC6294364](https://pmc.ncbi.nlm.nih.gov/articles/PMC6294364)): error in the outcome read is differential by risk.
- Curvature differs by about 11% between end-systole and diastole [REPO, earlier note, van Zandwijk 2019].

### Inferences
Model specification [INF]
- Primary (patient level, baseline plaque-free participants who returned):
  `newplaque ~ z_kappa + age + sex + htn + diabetes + smoking + ldl + bmi + lv_mass + baseline_scanner + phase_or_hr + log(interval) + followup_scanner`, logistic, weights = 1/P(return). Complementary log-log with `offset(log(interval))` gives a discrete-time hazard interpretation and is preferable if intervals range from 8 to 12 years.
- Statins: statin start between scans is a mediator-like time-varying variable caused by baseline risk and possibly by incidental findings of the baseline scan. Do not adjust for it in the primary model (it would block part of the pathway from risk to plaque and could induce collider bias); adjust for baseline statin use, and add statin-between-scans as a sensitivity. A subtle CGPS point: if participants were told their baseline CCTA findings, treatment after the scan depends on baseline plaque, which is another reason to restrict to baseline plaque-free people.
- Heart size: LV mass from the CGPS CCTA (already measured in CGPS) is better than a tree proxy and should be in the model, since it both lowers tortuosity and is linked to risk.
- Per region: Mundlak model from the earlier note (`(1|patient)`, region-type fixed effects, descriptor z within region type, patient-mean descriptor). The between coefficient is the target; GEE exchangeable as sensitivity.

Attrition and competing risk
- Who returns after 10 years is selected (alive, healthy enough, still local, willing). Model P(return) in all baseline-eligible participants from baseline covariates, baseline geometry and baseline plaque, and weight returners by its inverse (stabilised, truncated at the 1st and 99th percentiles). This removes bias only if return is independent of the outcome given the weight-model covariates (missing at random); geometry must be in the weight model because it is the exposure.
- Death before rescan is a competing event, not censoring: IPW treats the dead as if they could have had a scan, estimating a controlled quantity in a population where no one dies. For plaque, report the survivor estimand explicitly; as a check, use registry MI/revascularisation/death in the non-returners to test whether geometry predicts non-return (if it does, selection is informative).
- Multiple imputation of the outcome in non-returners is not credible here (no auxiliary plaque information after baseline), so IPW plus sensitivity bounds is the honest approach.

Measurement error and a correction to the earlier notes
- The earlier `longitudinal_design.md` inflated n by 1/λ² while `normality_outcome_readiness.md` used 1/λ. They answer different questions [CALC]: under classical error with reliability λ, the slope per unit of the observed variable is λβ; expressed per SD of the observed variable, the effect is √λ times the effect per SD of the true variable. So if the target effect is stated per SD of the true descriptor, required n scales by 1/λ (not 1/λ²). The 1/λ² chain in `longitudinal_design.md` is therefore conservative by a factor 1/λ (about 1.4 at λ = 0.7). Pick one convention in the pre-registration: state effects per SD of the measured z-score (what will be reported), and use the reliability-corrected OR (regression calibration: log OR_true = log OR_obs / λ for per-unit, with bootstrap CI) as the secondary estimate.
- λ must come from same-scan or short-interval repeats (CAS-Net vs expert on ImageCAS-X test, two segmentations of the same CGPS scan, two phases if reconstructed), not from the 10-year pairs, as `supervisor_questions.md` item 3 already says.

Change in geometry between scans
- Use baseline geometry as the exposure. Follow-up geometry and change are measured at the same time as the outcome and can be consequences of plaque (plaque alters lumen centerline and segmentation), so adding change as a predictor of new plaque mixes cause and effect. Report change descriptively, and only in participants plaque-free at both scans (group C, its legitimate use): mean change per decade by vessel, compared with the measurement-error band, which is the "minimum detectable change" objective in the project plan.
- Regression to the mean: if change is modelled, adjust for baseline value, knowing that baseline adjustment with error-prone baselines induces spurious associations (Lord's paradox); treat any change analysis as exploratory.

Scanner and protocol over 10 years
- The exposure is measured only at baseline, so follow-up scanner change affects only outcome detection. Adjust for follow-up scanner/kV as the Amsterdam study did, and use a scanner-robust sensitivity outcome (for example calcium conversion).
- For baseline geometry, include baseline scanner generation and heart rate or reconstructed phase (PhaseXact varies phase with heart rate) as covariates; a ComBat-style harmonisation is a sensitivity (earlier note).

### Gaps
- No published estimate of the within-patient correlation of new-plaque status across segments in a population cohort.
- Whether CGPS participants were informed of baseline CCTA findings (which drives post-scan treatment) was not established.
- Full text of the IPW-attrition guidance not read.

## 5. Power and sample size

### Takeaway
With a per-patient outcome incidence around 0.3 to 0.5, the minimum detectable OR per SD at 80% power is about 1.4 to 1.5 for 300 returners, about 1.2 to 1.3 for 1,000, and about 1.15 to 1.2 for 2,000. Only OR 1.3 per SD or larger is realistically testable unless the rescan subset is well over 1,000; the OR 1.05 to 1.10 per SD suggested by the largest continuous tortuosity study is out of reach for any plausible serial subset. Events-based analysis in the whole cohort is worse, since MI is rare (71 MI in 3.5 years).

### Cited Findings
- Largest continuous-tortuosity study: OR 1.05 per SD for CAD, 1.09 for severe CAD [REPO, earlier note] ([Tello Ayala 2026, PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)).
- Earlier repo table: OR 1.3 at p = 0.10 needs about 1,267 (R = 1) to 1,810 (R = 0.7) participants; OR 1.05 to 1.10 needs about 9,600 to 52,000 [REPO] (`normality_outcome_readiness.md`, section 4).
- CGPS events: 71 MI and 193 deaths over median 3.5 years in 9,533 [ABS] ([Fuchs 2023](https://www.acpjournals.org/doi/10.7326/M22-3027)); median follow-up since extended to 6.0 years in 10,003 [ABS] ([EHJ ehag612](https://academic.oup.com/eurheartj/advance-article/doi/10.1093/eurheartj/ehag612/8759473)).
- MESA 10-year incident CAC 53% from CAC = 0 [ABS] ([JACC CVI](https://www.jacc.org/doi/10.1016/j.jcmg.2020.06.048)).
- Sample size for a single standardised predictor in logistic regression follows Hsieh 1998 [ABS, earlier note] ([PubMed 9699234](https://pubmed.ncbi.nlm.nih.gov/9699234/)).

### Inferences
[CALC] Minimum detectable OR per SD of the measured descriptor, two-sided α 0.05, power 0.80, Hsieh formula, inflated by 1/(1 − 0.1) for covariate R² 0.1 and by 1/λ for reliability, per-patient outcome, no weighting design effect:

| Returners analysed | p = 0.3, λ 1.0 | p = 0.3, λ 0.7 | p = 0.5, λ 1.0 | p = 0.5, λ 0.7 |
|-|-|-|-|-|
| 300 | 1.45 | 1.56 | 1.41 | 1.50 |
| 500 | 1.33 | 1.41 | 1.30 | 1.37 |
| 1,000 | 1.23 | 1.28 | 1.21 | 1.25 |
| 2,000 | 1.15 | 1.19 | 1.14 | 1.17 |

- IPW weights add a further design effect (Kish, roughly 1 + CV² of the weights, often 1.1 to 1.5) [INF].
- If the analysis is restricted to baseline plaque-free participants, roughly half the returners are lost (about 46 to 50% of CGPS has plaque at baseline), so "returners analysed" is about half of the rescan subset [INF].
- Per-region analysis adds information only to the extent that the geometry varies within patient (Mundlak within part), which is the part the design says not to interpret; for the between-patient question it has about the same power as the per-patient analysis [INF].
- Events: with about 100 to 150 MI in the whole cohort by now (extrapolated from 71 in 3.5 years, not sourced), a Cox model on one standardised predictor has power only for HR around 1.3 per SD or more [INF, Schoenfeld-type approximation, not computed exactly].
- Recommendation: declare a smallest effect of interest (OR 1.3 per SD), report the achieved minimum detectable effect, and frame a null as "effects larger than X excluded", not "no effect".

### Gaps
- Real rescan n and per-patient CCTA incidence are unknown; the table must be recomputed when they are.
- No simulation of the clustered per-region design with realistic ICC was done.

## 6. Association versus prediction

### Takeaway
The thesis should aim at an explanatory association analysis (is baseline geometry associated with new plaque, independent of known risk factors) with pre-registered estimand and adjustment set. A prediction model with added-value metrics is realistic only as a secondary, TRIPOD+AI-reported analysis, and the benchmark for "added value" is sobering: in SCAPIS (24,791 people) adding a full CCTA read to a risk score plus CAC raised the C-statistic by only 0.015.

### Cited Findings
- SCAPIS, 24,791 participants aged 50 to 64, dual-source CT, SCCT 18-segment reading, 304 coronary events over median 7.8 years: C-statistic PCE 0.728, PCE + CAC 0.764, PCE + CCTA 0.779, PCE + CAC + CCTA 0.779 (Δ 0.015 vs PCE + CAC, p = 0.004); NRI 0.133 [FT] ([SCAPIS, PMC12598578](https://pmc.ncbi.nlm.nih.gov/articles/PMC12598578/)).
- TRIPOD+AI (Collins et al., BMJ, 16 April 2024) is the current reporting guideline for regression and machine-learning prediction models [ABS] ([PMC11025451](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11025451/)).
- Minimum sample size for developing a prediction model targets precise overall risk, shrinkage of at least 0.9 and small optimism in R², not events per variable [ABS] ([Riley et al., BMJ 2020;368:m441](https://pure.manchester.ac.uk/ws/files/161373531/bmj.m441.full.pdf); [pmsampsize](https://cran.r-project.org/web/packages/pmsampsize/pmsampsize.pdf); [Riley et al. Part II, PubMed 30357870](https://pubmed.ncbi.nlm.nih.gov/30357870/)).

### Inferences
- If a direct measure of atherosclerosis (CCTA plaque) adds 0.015 in C-statistic over risk factors plus CAC, a geometric descriptor that is at most a weak WSS proxy will add less; ΔC for tortuosity is likely below 0.01 and not estimable with a few hundred returners [INF].
- Prediction for new plaque in baseline plaque-free people is a scientifically cleaner target than MACE (the comparator is risk factors alone, CAC is 0 by design), and could be framed as "does geometry improve prediction of incident plaque beyond age, sex and risk factors". Report ΔC with bootstrap CI, calibration, and a likelihood-ratio test; treat NRI as secondary since it is sensitive to categories [INF].
- The project-plan MACE model (objective 10: baseline model plus topology, plus top-5% flags) is best written as exploratory: event counts are low, and its denominators (whole cohort) differ from the plaque analysis [INF].

### Gaps
- No CCTA-geometry prediction model with reported ΔC was found (CArTI is abstract only, per earlier notes).

## 7. What to lock before seeing outcomes, and a first deliverable in about 12 weeks

### Takeaway
Lock the measurement pipeline (segmentation, extraction, labelling, descriptor, quality-control exclusions), the reference model, the estimand, outcome definitions, adjustment set, attrition model and smallest effect of interest in a dated pre-registration (OSF or a committed repo file) before any follow-up plaque or event data are linked. The realistic first deliverable, whether or not CGPS access arrives, is a registered protocol plus the ImageCAS-X measurement study; with access, add baseline geometry and population centiles on all baseline CCTA scans, which need no outcome data.

### Cited Findings
- Project plan: CGPS access in weeks 2 to 3 is rated risk 5; association with plaque progression and the MACE model are weeks 11 to 14, both risk 5; submission 22 December [REPO] (`thesis/project_plan.tex`).
- Supervisor (Kit): "the main goal is the HØ dataset and matching the shape descriptors with outcome"; develop descriptors on ImageCAS first [REPO] (`from_superviser.tex`).
- CGPS CCTA was read blinded to treatment and outcomes [ABS] ([Fuchs 2023](https://www.acpjournals.org/doi/10.7326/M22-3027)), a precedent for keeping geometry extraction blind to outcomes.
- Existing go/no-go gates for the descriptor are in `normality_outcome_readiness.md` section 4 [REPO].

### Inferences
Items to lock (pre-registration checklist) [INF]
1. Data flow: geometry is computed on baseline scans only, by someone blind to follow-up plaque and events; outcome data are joined by a separate step after the lock.
2. Pipeline version: CAS-Net weights, extractor, labeller, descriptor (κ_a at declared σ and ℓ), per-scan QC exclusion rules (connectivity, truncation, image quality) and the target vessels (LAD, LCx, RCA; LM angle only).
3. Reference definitions A (population) and B (healthy standard) with GAMLSS form and covariates; C descriptive only.
4. Primary estimand: OR per SD of baseline κ_a z-score for any new plaque over the rescan interval among baseline plaque-free returners, in the survivor population, IPW for return.
5. Outcome definition and detection threshold, handling of revascularised segments, per-region scheme for the secondary analysis.
6. Adjustment set and what is not adjusted for (statins between scans, geometry change).
7. Reliability estimate λ source and correction method; smallest effect of interest; multiplicity (one primary descriptor, others Holm).
8. Direction: two-sided, no claimed sign (earlier note shows sign inconsistency).
9. Prediction secondary: model, validation (bootstrap optimism), metrics, TRIPOD+AI.

Deliverables in about 12 weeks
- Without CGPS access: (a) the protocol above as a thesis chapter and dated OSF registration; (b) ImageCAS-X measurement study already planned (reliability of κ_a against reference centerlines and CAS-Net output on the test split, giving λ); (c) a simulation of the design (per-patient and per-region, with the λ and plausible incidence) giving the minimum detectable effect, replacing the closed-form table; (d) a label-free main-vessel identification validated on ImageCAS-X.
- With baseline CGPS images but no outcomes: run the locked pipeline on all baseline CCTA, report QC failure rate, per-vessel distributions and age/sex/LV-mass-conditional centiles (reference A and B), and domain-shift checks against ImageCAS-X. This is objective 8 and needs no outcome linkage.
- Outcome analysis (objective 10) only if the rescan subset and reads are available by about week 11; otherwise present the registered plan and power as the deliverable, which is defensible and is what the fairness of a later analysis depends on.

### Gaps
- Whether the CGPS steering group requires its own protocol approval or data-access application, and its timeline, is unknown.
- Whether OSF or an institutional registry is preferred by the supervisors is not known.
