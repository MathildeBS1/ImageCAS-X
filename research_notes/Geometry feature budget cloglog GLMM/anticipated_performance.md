# Anticipated model performance (C / Cox–Snell R²) for the sample-size calculation: incident coronary plaque in people plaque-free at baseline

Setting: CGPS Herlev–Østerbro, ~1,076 plaque-free at baseline CCTA, 452 (42%) developed plaque in a trunk segment at the ~10-year CCTA. Note that the analysis model is a segment-level cloglog GLMM. The Riley criteria below are for a person-level binary model, so they are only an approximation for the pooled model.

## Q1. C-statistics of risk factors or risk scores for incident CAC or incident CCTA plaque in people without disease at baseline

### Takeaway
The only direct incident-outcome C I could verify is from MESA. Traditional risk factors predicting CAC 0 → CAC > 0 over ~2.5 years in low-Framingham-risk people gave an **apparent** C of 0.688. I found **no** published C for risk factors or scores predicting incident *CCTA plaque* (any grade) in initially plaque-free people, and no SCORE2 C for any incident subclinical outcome. Incident-outcome evidence therefore points to C ≈ 0.65–0.72 for a risk-factor base model.

### Cited Findings
- **Okwuosa et al., MESA (JACC Cardiovasc Imaging 2012;5(2):144–153, doi:10.1016/j.jcmg.2011.11.008).**
  - Sample: participants with Framingham Risk Score < 10% and repeat CAC (n = 2,620). Of the 1,830 with CAC = 0 at baseline, 214 (11.7%) developed CAC > 0 over a mean of 2.5 years.
  - Base model: age, sex, race/ethnicity, SBP, DBP, antihypertensive treatment, total and HDL cholesterol, smoking, BMI, physical activity, family history.
  - "The base model ... discriminated incident CAC better than increased CAC (c-statistic = 0.688 versus 0.645)." For overall CAC progression the base C was 0.711, and novel markers raised it only to 0.7158–0.7164.
  - Age was the main driver of model fit. All C values are apparent: no cross-validation or external validation is described.
  - Source: [PMC3310187](https://pmc.ncbi.nlm.nih.gov/articles/PMC3310187)
- **Kronmal et al., MESA (Circulation 2007;115:2722–30, doi:10.1161/CIRCULATIONAHA.106.674143).** Predictors of incident CAC over ~2.4 years were age, male sex, white race, hypertension, BMI, diabetes and family history. The summary I read reported no C. — [Blaha et al. Glob Heart 2016 review, PMC5117817](https://pmc.ncbi.nlm.nih.gov/articles/PMC5117817)
- **DeFilippis et al., MESA (JACC 2011;58:2076–83, doi:10.1016/j.jacc.2011.08.022).** Each 5% higher absolute Framingham Risk Score was associated with 40% higher risk of incident CAC. No C was reported in the summary. — [PMC5117817](https://pmc.ncbi.nlm.nih.gov/articles/PMC5117817)
- **Shea et al., MESA (Circ Cardiovasc Imaging 2021;14:e011981, doi:10.1161/CIRCIMAGING.120.011981).**
  - Among 3,286 people with CAC = 0, the transition rate to CAC > 0 was about 7 per 100 person-years.
  - No C or AUC is reported for incident CAC.
  - Source: [PMC7987729](https://pmc.ncbi.nlm.nih.gov/articles/PMC7987729)
- **An Asian cohort starting from CAC = 0** reportedly found that the Framingham Risk Score had the best discrimination for CAC progression (AUC 0.660). I saw only a search snippet, not the primary paper, so this is unverified and needs checking before citing. — search result only, see Gaps.
- **PESA 6-year progression** (3D vascular ultrasound, not CCTA). 32.7% progressed, 17.5% of them with incident disease. Determinants were found by stepwise logistic regression, but I found no reported AUC. — [ACC/PESA summaries](https://www.acc.org/latest-in-cardiology/articles/2017/11/13/15/51/established-and-new-risk-scores-both-accurately-predict-subclinical-atherosclerosis)

### Inferences
- The MESA incident-CAC C of 0.688 is the closest analogue, but it differs from CGPS in four ways:
  - The outcome is CAC, not CCTA plaque that includes non-calcified minimal plaque.
  - Follow-up is 2.5 years, not ~10.
  - Incidence is 11.7%, not 42%.
  - It is apparent and restricted to low-risk people, which narrows the range of risk factors and lowers C.
- Its direction of bias is therefore mixed. The low-risk restriction and short follow-up push C down. The apparent (unvalidated) estimate pushes it up.
- A 10-year horizon with a wide age range is likely to make age dominate, as it did in MESA. A risk-factor model's C for incident plaque at 10 years plausibly lies in the 0.65–0.72 range. This is an inference, not a measured value.

### Gaps
- No verified C for SCORE2, the Pooled Cohort Equations or SCORE predicting incident CCTA plaque or incident CAC in a general-population cohort. I found none for DANCAVAS, the CGPS imaging cohorts, SCAPIS follow-up, MiHEART or PESA.
- No age-only C for incident CAC or plaque was found.
- The Dzaye/Budoff "CAC = 0 warranty period" papers model time to conversion with Weibull models. They report no C in the material I accessed.
- I did not verify the PARADIGM clinical-model C of 0.68 that the draft cites. It comes from a referral (symptomatic or suspected CAD) cohort with plaque progression as the outcome, which is a different population and outcome from incident plaque in plaque-free people.

## Q2. Cross-sectional C of risk factors for any plaque or CAC in asymptomatic cohorts (upper and lower reference)

### Takeaway
Cross-sectional discrimination of risk factors for *prevalent* disease is higher: about 0.75–0.79 for CAC > 0 in MESA (cross-validated) and about 0.69 for multi-territory plaque and 0.78 for CAC ≥ 1 in PESA. Prevalent disease reflects the whole lifetime exposure and the full age range, so these figures are best read as an **upper reference** for a 10-year incident outcome in people who were all plaque-free at baseline.

### Cited Findings
- **Pletcher et al., MESA baseline (Circulation 2013;128(10), doi:10.1161/CIRCULATIONAHA.113.002598).**
  - Design: cross-sectional, 6,757 participants, of whom 50% had CAC > 0.
  - Cross-validated C for prevalent CAC > 0:
    - Framingham Risk Score alone: 0.752
    - Age + sex alone: 0.767
    - All conventional risk factors + race: 0.789
  - Age and sex alone carry almost all of the discrimination.
  - Source: [PMC3840900](https://pmc.ncbi.nlm.nih.gov/articles/PMC3840900)
- **PESA (Fernández-Alvira et al., JACC 2017), 3,983 asymptomatic middle-aged Spanish workers, cross-sectional.**
  - Plaque presence (multi-territory ultrasound + CAC): Fuster-BEWAT C 0.692 and ideal cardiovascular health C 0.694.
  - CACS ≥ 1: C 0.780 and 0.782.
  - Source: [ACC summary](https://www.acc.org/latest-in-cardiology/articles/2017/11/13/15/51/established-and-new-risk-scores-both-accurately-predict-subclinical-atherosclerosis)
- **SCAPIS (25,182 people aged 50–64).**
  - 42.1% had CCTA atherosclerosis and 5.5% of those with CAC = 0 had plaque.
  - A questionnaire model for *widespread* atherosclerosis had an AUC of about 0.8, and clinical measurements added little.
  - These figures come from press and conference coverage, not the primary paper, so they need verifying.
  - Source: [the-hospitalist coverage](https://community.the-hospitalist.org/content/scapis-simple-questionnaire-can-identify-silent-atherosclerosis)
- **SCAPIS Linköping (Strömberg et al., Scand J Prim Health Care 2025;43(2):455–462, doi:10.1080/02813432.2025.2456948).**
  - Cross-sectional, n = 3,087.
  - CACS > 0 prevalence rose from 26.1% in the low–moderate SCORE2 group to 52.8% in the high group and 60% in the very-high group.
  - Only odds ratios are reported, **no AUC**.
  - Source: [PMC12090275](https://pmc.ncbi.nlm.nih.gov/articles/PMC12090275/)
- **Miami Heart Study (Nasir et al. 2021, n = 2,359).**
  - 49% had CCTA plaque, and 16% of those with CAC = 0 had plaque.
  - Plaque prevalence rose with PCE risk, from 13.5% to 50% in the CAC = 0 strata.
  - **No C-statistic** was reported in what I could access.
  - Source: [Houston Methodist record](https://scholars.houstonmethodist.org/en/publications/coronary-atherosclerosis-in-an-asymptomatic-us-population-miami-h/)
- **Playford et al., Am Heart J Plus 2024 (doi:10.1016/j.ahjo.2024.100493).** Self-referred or clinician-referred asymptomatic CCTA (n = 828). Agreement between the Australian Framingham-based score and plaque was poor (kappa 0.10–0.15). No AUC was reported. — [PMC11698937](https://pmc.ncbi.nlm.nih.gov/articles/PMC11698937/)

### Inferences
- The cross-sectional C (0.69–0.79) exceeds the only incident-outcome C (0.688), which is consistent with prevalent disease being easier to discriminate.
- CGPS restricts to plaque-free people at baseline. This removes the people the risk factors identify most easily, so C should be below the cross-sectional values. An anticipated C of 0.75 or more for the *base* model would be optimistic.
- Risk-factor discrimination for CCTA plaque that includes minimal or non-calcified lesions is plausibly lower than for CAC. The PESA figures show this pattern: 0.69 for plaque against 0.78 for CAC.

### Gaps
- I did not obtain the primary SCAPIS AUC paper or any SCAPIS SCORE2 AUC for prevalent CCTA plaque.
- No Miami Heart C was found.

## Q3. C, R² or ΔC for coronary geometry (tortuosity, bifurcation angle, diameters) predicting plaque

### Takeaway
I found **no** study reporting C or ΔC for baseline geometry predicting *incident* plaque in plaque-free people. The studies that exist are cross-sectional (geometry against stenosis on the same scan) or come from referral progression cohorts. There is no defensible external number for the geometry increment, so the anticipated C should be set from the base model plus a modest assumed ΔC.

### Cited Findings
- **CLAP score (J Cardiovasc Dev Dis 2024).**
  - LAD progression model including the LM bifurcation angle, with AUC 0.91 in development and 0.85 in validation.
  - Population: **referral/clinical** patients with LAD disease. The outcome was progression (≥ 30% stenosis increase or new high-risk features).
  - Not transferable to incident plaque in plaque-free people, and the AUCs are likely inflated by a selected referral population.
  - Source: [PMC11595042](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11595042/)
- **Cui et al. (PLoS ONE 2017).** The LAD–LCx bifurcation angle was an independent predictor of significant left coronary stenosis on the *same* CCTA (cross-sectional). — [DOAJ record](https://doaj.org/article/c8e3cc4c1f524184ae58922437f34efe)
- **Moon et al. (QIMS 2023).** A combined tortuosity × LM–LAD angle descriptor (d20·cosθ) was associated with proximal LAD stenosis. The study is retrospective and cross-sectional, and the results are reported as hazard or odds ratios, not AUC. — [QIMS](https://qims.amegroups.org/article/view/117032/html)

### Inferences
- Any anticipated ΔC from geometry is a guess. Novel markers for incident CAC in MESA added about +0.005 to C. This is not about geometry, but it shows how small increments over a risk-factor base usually are. — [PMC3310187](https://pmc.ncbi.nlm.nih.gov/articles/PMC3310187)
- A ΔC of +0.01 to +0.03 is a plausible, conservative planning assumption. Riley's criteria are driven by the full-model R², so this moves P_max only modestly. For example, going from C 0.68 to 0.70 moves P_max from ~12 to ~15.

### Gaps
- No incident-outcome geometry study with discrimination metrics was found, in general-population or referral cohorts.

## Q4. Riley, Van Calster & Collins 2021: converting C to Cox–Snell R², and the 15%-of-max rule

### Takeaway
The citation is verified: Riley RD, Van Calster B, Collins GS. *A note on estimating the Cox-Snell R² from a reported C statistic (AUROC) to inform sample size calculations for developing a prediction model with a binary outcome.* Stat Med 2021;40(4):859–864, doi:10.1002/sim.8806. The default when R² is unknown comes from Riley et al. 2019 Part II (Stat Med 2019;38(7):1276–1296, doi:10.1002/sim.7992): assume a Nagelkerke R² of 0.15, that is R²_CS = 0.15 × max(R²_CS).

At 42% prevalence:
- max R²_CS = 0.744.
- 15% of the maximum gives R²_CS = 0.112, which corresponds to C ≈ 0.69–0.70 and P_max ≈ 14 at n = 1,076 (criterion 1, S = 0.9).

### Cited Findings
- **Riley et al. 2021 (doi:10.1002/sim.8806).** Riley and colleagues show how to derive the anticipated R²_CS from a reported C for binary-outcome models, with R and Stata code and a small simulation. They suggest taking the anticipated value from closely related published models. — [Birmingham repository](https://research.birmingham.ac.uk/en/publications/a-note-on-estimating-the-cox-snell-rsub2sub-from-a-reported-c-sta)
- **Software.** The `pmsampsize` R package implements the conversion: its C-statistic option is used "in conjunction with the expected prevalence to approximate the Cox-Snell R-squared using the approach of Riley et al." Its documentation also advises entering the adjusted R² of a previous model, not the apparent R². — [pmsampsize manual](https://cran.r-universe.dev/pmsampsize/doc/manual.html)
- **Riley et al. 2019 Part II (doi:10.1002/sim.7992):**
  - "we suggest that sample sizes be derived assuming the value of R²_CS,adj corresponds to an R²_Nagelkerke of 0.15." A higher value, such as 0.5, may suit predictors that are direct or mechanistic measures of the outcome.
  - max(R²_CS) = 1 − exp(2·lnL_null/n), with lnL_null = E·ln(E/n) + (n−E)·ln(1−E/n).
  - Source: [PMC6519266](https://pmc.ncbi.nlm.nih.gov/articles/PMC6519266)
- **My computation.** Method: equal-variance binormal linear predictor with exact logistic likelihood, N = 10⁶ simulated, prevalence 452/1,076 = 0.42. n = 1,076, S = 0.9.
  - Criterion 1 (shrinkage ≥ 0.9) gives P_max = n·(S−1)·ln(1 − R²/S).
  - Criterion 2 (optimism in R²_Nagelkerke ≤ 0.05) does not bind (P ≈ 41–47).
  - The results reproduce the draft's 8 / 15 / 24.

| C | R²_CS | fraction of max R² | P_max (criterion 1) |
|---|---|---|---|
| 0.60 | 0.031 | 0.04 | 3.7 |
| 0.65 | 0.068 | 0.09 | 8.4 |
| 0.68 | 0.096 | 0.13 | 12.2 |
| 0.70 | 0.118 | 0.16 | 15.1 |
| 0.72 | 0.141 | 0.19 | 18.4 |
| 0.75 | 0.182 | 0.25 | 24.3 |
| 0.78 | 0.226 | 0.30 | 31.0 |
| 0.80 | 0.255 | 0.34 | 35.9 |
| 15% of max (R² 0.112) | 0.112 | 0.15 | 14.2 |

### Inferences
- At 42% prevalence, Riley's generic default (15% of max) lands almost exactly on C ≈ 0.70. It agrees with the incident-CAC literature (0.69–0.71, apparent) and sits below the cross-sectional values (0.75–0.79).
- C ≈ 0.68–0.70 (R²_CS ≈ 0.10–0.12, P_max ≈ 12–15) is the best-supported planning range. C = 0.65 (P_max ≈ 8) is a conservative sensitivity bound. C = 0.75 is not supported by any incident-outcome source.
- The Riley formula assumes one independent binary outcome per person. The pooled segment cloglog GLMM, with 9 segments per person and a random intercept, does not map onto it exactly. The person count and person-level events are the conservative unit, and the thesis text should state this as an approximation.
- Because the binormal conversion is model-based, the exact R² depends slightly on how the conversion is done. Running `pmsampsize` with `cstatistic=` gives values in the same range.

### Gaps
- I could not fetch Riley et al. BMJ 2020 ("Calculating the sample size required for developing a clinical prediction model", BMJ 2020;368:m441, doi:10.1136/bmj.m441) because of a 403 error. I have not verified its wording on the 15% default or on the use of existing models.
- I did not read the exact simulation details of the 2021 note. My table uses an analytic binormal equivalent, not their code.

## Q5. Can the project's own cross-validated base-model C (SCORE2 only, no geometry) be used as the anticipated C?

### Takeaway
Partly. Riley et al. say an existing model's *adjusted* (optimism-corrected) R² can inform the calculation and serves as a **lower bound** for a new model that adds predictors. A cross-validated base-model C from the same data is optimism-corrected and directly relevant to the population and outcome. The weakness is that it is computed on the same outcome data the sample size is meant to plan for. It must be reported as such (post hoc, data-informed), and the literature-based range should be shown alongside it.

### Cited Findings
- **Riley et al. 2019 Part II:**
  - Prior models can supply the anticipated R²_CS,adj.
  - Apparent values are "upwardly biased (optimistic)", so the adjusted value should be used, with S_VH = 1 + (p/n)·ln(1 − R²_app)/R²_app.
  - External-validation R² needs no adjustment.
  - An existing model's adjusted R² can serve as a lower bound for a new model that adds predictors.
  - Source: [PMC6519266](https://pmc.ncbi.nlm.nih.gov/articles/PMC6519266)
- **pmsampsize documentation.** Use the adjusted R² of a previous model, not the apparent one. — [pmsampsize manual](https://cran.r-universe.dev/pmsampsize/doc/manual.html)

### Inferences
- A cross-validated, person-split base-model C (SCORE2 + log follow-up) in the pooled model is the closest thing to an "existing model's adjusted R²" for this exact outcome. By Riley's logic it is a legitimate *lower bound* for the full (base + geometry) model.
- **Caveats.** These are my reasoning, not quoted from Riley:
  1. Riley's framework is meant to be used *before* data collection or analysis. Using the same cohort's outcome makes the budget data-dependent and should be stated openly. It should be fixed before geometry is ever fitted against the outcome. This fits the project rule to freeze the method before seeing the outcome.
  2. The internal estimate has sampling uncertainty (n = 1,076, 452 events, so roughly ±0.03 for C). Report its interval and show P_max across that interval.
  3. The pooled-model C is a person-level C from aggregated segment risks. Its conversion to R²_CS through the Riley formula is an approximation.
- **Recommended framing:**
  - The primary anticipated C is about 0.70 (R²_CS ≈ 0.12, P_max ≈ 15), supported by three things:
    - (a) Riley's 15%-of-max default, which gives C ≈ 0.70 at 42% prevalence;
    - (b) MESA incident-CAC risk-factor C 0.688–0.711 (apparent);
    - (c) cross-sectional C 0.75–0.79 as an upper reference.
  - The internal cross-validated base C is reported as a check, or used as a data-informed lower bound.
  - C = 0.65 is a conservative sensitivity bound.
  - PARADIGM (referral, progression in patients with existing plaque) should be replaced or demoted to a secondary mention, because its population and outcome do not match.

### Gaps
- I found no Riley et al. statement that addresses using a *same-cohort* internal estimate to set the sample-size input. The caveats above are reasoning, not citations.
