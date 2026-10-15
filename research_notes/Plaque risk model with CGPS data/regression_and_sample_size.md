# Regression framework and sample-size methodology for incident trunk plaque (CGPS, ~10-year serial CCTA, clustered vessels)

Source-status legend, used throughout:
- **[fetched]**: source located or read during this session (URL found by search or fetch).
- **[known]**: well-established reference cited from prior knowledge with its DOI. The DOI was not opened in this session, so check page and volume details before final citation.
- **[computed]**: numbers I calculated in this session (Python, numpy; script logic described below). They are not quoted from any paper.

---

## Q1. Logistic GLMM vs GEE vs cloglog with log(interval) offset vs discrete-time / interval-censored survival, for 2 time points with variable interval

### Takeaway
Each vessel is plaque-free at baseline and is checked once more at follow-up, so the data are **current-status (single-inspection, interval-censored) data**. The natural model is a **binary GLM with a complementary log-log (cloglog) link and log(interval) entered as a covariate (or as an offset)**. This model is exactly a grouped proportional-hazards model, so its coefficients are log hazard ratios. With an interval spread of only about 9.5 to 15 years (log ratio about 0.46), the results will differ little from a plain logistic model at event fractions of 30% or less. The interval term matters mainly when interval length correlates with predictors (age, scan date, randomisation group). Multi-interval discrete-time survival adds nothing here because only one inspection follows baseline.

### Cited Findings
- If the data come from a continuous-time proportional-hazards model and are observed only in grouped (interval-censored) form, the grouped-data likelihood equals a binary-response likelihood with a cloglog link, and the coefficient vector equals that of the continuous PH model (Prentice & Gloeckler framework). Source: SAS/STAT PROC LOGISTIC documentation, interval-censored example [fetched] — [SAS doc](https://support.sas.com/documentation/cdl/en/statug/63033/HTML/default/statug_logistic_sect065.htm); [SAS example code](https://support.sas.com/documentation/onlinedoc/stat/ex_code/131/logiex14.html)
- When the outcome is "at least one event during an exposure window" under a constant-rate process, p = 1 - exp(-rate x exposure), which is a cloglog model with log(exposure) as an offset. This is a vendor or blog source, so it is weak [fetched] — [MetricGate blog](https://metricgate.com/blogs/when-to-use-cloglog-link/)
- MESA modelled time to conversion from CAC = 0 to CAC > 0 with a **Weibull parametric survival model** that handled the interval-censored repeat-scan design (n = 3,116 with baseline CAC 0; 10-year prevalence of CAC > 0 was 53%) [fetched] — [Dzaye et al., JACC Cardiovasc Imaging 2021 (Houston Methodist record)](https://scholars.houstonmethodist.org/en/publications/warranty-period-of-a-calcium-score-of-zero-comprehensive-analysis-2/)
- PARADIGM analysed lesion-level progression over a variable interval (3.8 ± 1.6 y) as a binary outcome with C-statistics, apparently logistic. I could not see in the abstract whether the interval was adjusted for [fetched] — [Lee SE et al., Int J Cardiovasc Imaging 2020, PubMed 32779077](https://pubmed.ncbi.nlm.nih.gov/32779077/)

### Inferences (my derivation, [computed] or reasoned)
- **Derivation.** Under PH with cumulative baseline hazard Λ0(t), P(plaque by t | x) = 1 - exp(-Λ0(t)·e^{xβ}). Then cloglog(P) = log Λ0(t) + xβ. With a Weibull baseline, Λ0(t) = λt^k, which gives cloglog(P) = log λ + k·log(t) + xβ.
  - A **fixed offset log(t)** imposes k = 1, a constant hazard.
  - Entering **log(t) as a free covariate** estimates k. In atherosclerosis the incidence rate rises with age, so k > 1 is plausible.
  - Recommendation: fit log(interval) as a covariate, and report the offset version as a sensitivity analysis.
- **When the interval matters.** The interval ranges from about 9.5 to 15 y, so log(t) ranges over about 0.46. Under k = 1, a vessel followed for 15 y has a cumulative hazard 1.58 times that of one followed for 9.5 y. At a 20% risk this is roughly 20% vs 30% [computed: 1 - 0.8^1.58 = 0.297]. The difference is not negligible at the extremes, but it applies to few vessels if the interval distribution is concentrated near 10 y.
  - The interval matters most when it is confounded with predictors. For example, late re-scans may be in older or sicker people, or linked to the trial arm (`rand_group` is in FU).
  - For prediction, the model must be used at a **fixed horizon** (e.g. 10 y). Set t = 10 when computing predicted risks for calibration and decision curves.
- **Logistic vs cloglog.** When risks are small (< 10-15%) the two links give nearly identical predictions. At 30-50% they diverge in the tails. Choose by AIC or calibration if needed. Logistic with log(t) as a covariate is a defensible simpler alternative, but it loses the hazard-ratio interpretation.
- **GLMM vs GEE.** This choice is about clustering, not about time (see Q2). Either can use a cloglog link: `glmer(..., family = binomial("cloglog"))` or `geeglm(..., family = binomial("cloglog"))`.
- **Interval-censored Cox / Weibull (e.g. `icenReg`, `survival::survreg` with interval2) on the person or vessel.** With left bound 0 and right bound t for events, and right-censoring at t for non-events, the likelihood reduces to the same current-status likelihood. A Weibull survreg is therefore equivalent to cloglog with a log(t) covariate. It is useful as a check and maps directly onto MESA's Weibull approach.
- Discrete-time person-period expansion is pointless with one follow-up inspection, because there is only one period.

### Gaps
- I found no methods paper specifically on "cloglog + log(interval) for two-scan imaging cohorts". The derivation above is standard grouped-PH theory, but it was not quoted from a single paper. Allison's *Survival Analysis Using SAS* or Prentice & Gloeckler (Biometrics 1978) would be the canonical citation; neither was fetched.
- Whether PARADIGM or MESA incident-CAC analyses adjusted for interval in logistic models was not verified from full texts.

---

## Q2. Patient-level vs vessel-level modelling with up to 3 correlated trunks per person; calibrated participant-level risk

### Takeaway
Model at the **vessel level**, because geometry is vessel-specific and the thesis question is vessel-level. Include **artery (LAD/CX/RCA) as a fixed effect** and handle within-person correlation with either:
- **(a) a marginal model** (GEE or GLM with cluster-robust/sandwich SEs by `study_id`), which directly yields population-averaged predicted risks for a new person; or
- **(b) a random-intercept GLMM**, whose predictions must be **marginalised over the random effect** (not set to u = 0) to be calibrated for new participants.

Participant-level risk ("any new trunk plaque") is derived as 1 - Π(1 - p_vessel) only under conditional independence. Do this with the GLMM by integrating over the shared random intercept, or fit a separate participant-level model.

### Cited Findings
- TRIPOD-Cluster (BMJ, 7 Feb 2023) extends TRIPOD to prediction studies with clustered data. It adds 10 new items and updates 19 existing items, so it should be used alongside TRIPOD+AI when reporting. Note that its typical clusters are centres or studies, not vessels within a person [fetched] — [Debray et al., BMJ 2023;380:e071018 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/9903175); [E&E paper PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9903176)
- A simulation study of multilevel logistic prediction models found that at least 10 EPV is recommended for clustered data, and up to 50 EPV when variable selection is used. Clustering strength was not meaningfully associated with predictive performance [fetched, abstract only] — [Wynants et al., J Clin Epidemiol 2015](https://researchinformation.umcutrecht.nl/en/publications/a-simulation-study-of-sample-size-demonstrated-the-importance-of-/)
- PARADIGM directly compared per-lesion and per-patient models for progression to obstructive CAD:
  - 1,297 patients and 3,218 non-obstructive lesions; 76 lesions (2.4%) in 60 patients progressed.
  - C-statistics: clinical model 0.684; adding per-patient plaque measures 0.825; per-lesion model 0.895 (p < 0.001 vs per-patient).
  - This shows that sub-patient units carry extra signal [fetched] — [Lee SE et al. 2020](https://pubmed.ncbi.nlm.nih.gov/32779077/)
- Marginal vs conditional predictions from random-effects logistic models: conditional predictions with u = 0 are systematically too extreme (miscalibrated) for new clusters, and marginal predictions are needed for new clusters [known] — Pavlou M, Ambler G, Seaman S, Omar RZ. "A note on obtaining correct marginal predictions from a random intercepts model for binary outcomes." BMC Med Res Methodol 2015;15:59, https://doi.org/10.1186/s12874-015-0046-6

### Inferences
- **Structure recommended for the thesis (reasoned):**
  1. Unit = trunk that is plaque-free at baseline. Outcome = new plaque ≥ minimal at FU.
  2. Fixed effects: artery (3 levels), SCORE2 variables (or the SCORE2 linear predictor as a single term to save df), baseline plaque elsewhere (person-level), CACS (person-level, log(CACS+1); note that CACS in a plaque-free trunk is 0 by definition, so per-vessel `ct_cacs_<vessel>` is uninformative for that vessel and only other-vessel or total CACS is usable), interval term, and geometry features.
  3. **Artery-by-geometry interactions**: allow these only for the 1-3 a priori geometry features (e.g. curvature × artery), because each interaction costs 2 df. Alternatively, standardise geometry within artery (z-score per artery) to absorb artery-specific scales without interactions.
  4. Correlation: primary model GEE (exchangeable or independence working correlation) with robust SEs. Independence working correlation plus sandwich SEs gives consistent marginal coefficients and is safest for prediction. Sensitivity analysis: random-intercept GLMM, reporting σ²_u and the latent-scale ICC = σ²_u / (σ²_u + π²/3) for logit (π²/6 for cloglog).
- **Calibrated participant-level risk:** from the GLMM, P(any) = 1 - ∫ Π_j (1 - p_j(u)) φ(u; 0, σ²) du (Gauss-Hermite quadrature). From GEE there is no joint model, so either fit a person-level model (outcome = any new trunk plaque, with person-level covariates plus summaries of geometry) or use the GLMM for the joint quantity. Report calibration at both levels.
- **Validation and resampling must be clustered by participant**: bootstrap participants, not vessels, and use grouped CV folds by `study_id` (see Q4).
- **Persons contribute 1-3 vessels.** The vessels that are eligible (plaque-free) are selected non-randomly: people with more disease contribute fewer vessels. This informative cluster size can bias marginal estimates. Report the distribution of eligible vessels per person, and consider a sensitivity analysis that weights each person equally (weights 1/m_i).

### Gaps
- I found no paper that uses TRIPOD-Cluster for vessel-within-patient clustering specifically. Its applicability is an inference.
- I could not fetch the PARADIGM full text to see whether lesion clustering within patients was handled (e.g. GEE or frailty).

---

## Q3. Riley et al. (pmsampsize) criteria for binary outcomes: formulas, anticipated R²/C, application to clustered data, max-parameter table

### Takeaway
Riley's three criteria for binary outcomes are: shrinkage ≥ 0.9, optimism in Nagelkerke R² ≤ 0.05, and an intercept within ±0.05. In this design **criterion (i) always binds**. With an anticipated C of about 0.70 (realistic for traditional risk factors predicting new plaque), the design affords only about **9-14 candidate parameters per 1,000 effective vessels** at event fractions of 20-50%. About 5,000 vessels with a design effect of 1.3-1.6 (effective n about 3,100-3,850) supports roughly **30-50 parameters at a 20% event fraction**. That is enough for SCORE2 + CACS + artery + a moderate geometry set with some splines, but not for dozens of geometry features without penalisation or data reduction.

### Cited Findings
- Riley et al. BMJ 2020;368:m441 gives step-by-step sample-size calculations for prediction-model development, implemented in `pmsampsize` (R/Stata). Authors: Riley, Ensor, Snell, Harrell, Martin, Reitsma, Moons, Collins, van Smeden [fetched, record] — [Utrecht repository record](https://dspace.library.uu.nl/handle/1874/457642); DOI https://doi.org/10.1136/bmj.m441
- Binary-outcome derivations are in Riley et al., Stat Med 2019, "Minimum sample size for developing a multivariable prediction model: Part II – binary and time-to-event outcomes" [known] — https://doi.org/10.1002/sim.7992
- `pmsampsize` arguments [fetched] — [pmsampsize docs (rdrr)](https://rdrr.io/pkg/pmsampsize/man/pmsampsize.html):
  - `csrsquared` or `nagrsquared`, or `cstatistic` with `prevalence`, which approximates the Cox-Snell R² by simulation.
  - `parameters` counts all candidate parameters, including spline and dummy terms.
  - `shrinkage` defaults to 0.9.
  - The binary criteria are: shrinkage ≤ 10%; difference between apparent and adjusted Nagelkerke R² ≤ 0.05; overall risk estimated within ± 0.05.
  - "Users should be conservative" with the R² taken from previous models, and the C-statistic should ideally be optimism-adjusted.
- C → Cox-Snell R² method: assume the linear predictor is N(0,1) in non-events and N(d,1) in events, with d = √2·Φ⁻¹(C). Fit a logistic model to a large simulated sample at the target prevalence and compute R²_CS from the LR statistic [fetched] — [Riley, Van Calster, Collins, Stat Med 2021, "A note on estimating the Cox-Snell R² from a reported C statistic"](https://research.birmingham.ac.uk/en/publications/a-note-on-estimating-the-cox-snell-rsub2sub-from-a-reported-c-sta); method described in [arXiv 2509.14028 (2025)](https://arxiv.org/pdf/2509.14028), which also notes underestimation bias at high discrimination and argues that sample-size calculations should account for performance variability.
- EPV is a poor basis for sample-size planning. Out-of-sample performance depends on the number of predictors, total n, and event fraction [fetched] — [van Smeden et al., SMMR 2019;28(8):2455-74](https://researchinformation.umcutrecht.nl/en/publications/sample-size-for-binary-logistic-prediction-models-beyond-events-p/); [van Smeden et al., BMC Med Res Methodol 2016 "No rationale for 1 variable per 10 events"](https://bmcmedresmethodol.biomedcentral.com/track/pdf/10.1186/s12874-016-0267-3)
- Clustered data: about ≥ 10 EPV for multilevel logistic models, and up to 50 with variable selection [fetched] — [Wynants et al. 2015](https://researchinformation.umcutrecht.nl/en/publications/a-simulation-study-of-sample-size-demonstrated-the-importance-of-/)
- Design effect DEFF = 1 + (m̄ - 1)·ICC. Unequal cluster sizes inflate the DEFF further. These are general survey or multilevel sources, not prediction-specific [fetched, secondary] — [MetricGate design-effect doc](https://metricgate.com/docs/sample-size-mixed-model/)

### Formulas (standard Riley 2019/2020 forms, written out by me)
Notation: n = sample size, p = number of candidate parameters, φ = outcome proportion, R²_CS = anticipated Cox-Snell R², S = target shrinkage (0.9), δ = 0.05.

1. **Criterion (i), small overfitting:** n ≥ p / [ (S - 1) · ln(1 - R²_CS / S) ]. Inverted: **p_max = n · (S - 1) · ln(1 - R²_CS / S)**.
2. **Criterion (ii), small optimism in Nagelkerke R²:**
   - max(R²_CS) = 1 - exp(2·lnL_null / n) = 1 - [φ^φ (1 - φ)^(1-φ)]².
   - S_VH = R²_CS / (R²_CS + δ · max(R²_CS)).
   - Then apply the formula from (i) with S_VH in place of S.
3. **Criterion (iii), precise overall risk:** n ≥ (1.96 / 0.05)² · φ(1 - φ).
4. **Choosing R²_CS:**
   - (a) From an existing comparable model's optimism-adjusted C via the Riley 2021 simulation.
   - (b) If nothing is available, the conservative default in Riley et al. 2020 is R²_CS = 15% of max(R²_CS). This is quoted from my knowledge of the BMJ paper; the pmsampsize help page I fetched does not state it, so verify.
   - (c) For this thesis, anchor on C of about 0.65-0.70 for clinical factors alone (MESA ≥ 65 found traditional risk factors predict incident CAC poorly; PARADIGM clinical-only C = 0.684, see Q5), and on C of about 0.75 as an optimistic full-model scenario.
5. **Clustering adjustment (heuristic, not part of Riley's published criteria):** n_eff = n_vessels / DEFF, with DEFF = 1 + (m̄ - 1)·ICC_latent. Use n_eff in the formulas above. Bounds: n_eff lies between n_participants and n_vessels. If ICC → 1, every person behaves like one unit.

### Computed tables [computed, this session]
Method:
- C → R²_CS: Riley 2021 simulation, N = 200,000 per cell, numpy IRLS logistic fit. Monte-Carlo error is about ±0.003 in R², which explains the small non-monotonicity between φ = 0.4 and 0.5.
- p_max = floor(min over criteria (i) and (ii)). Criterion (i) was binding in every cell.
- Criterion (iii) is satisfied for all n ≥ 400 (requires n ≥ 138, 246, 323, 369, 384 at φ = 0.1-0.5).

**Anticipated R²_CS by event fraction**

| φ (event fraction) | max R²_CS | R²_CS @ C=0.65 | @ C=0.70 | @ C=0.75 | @ C=0.80 | 15% of max |
|---|---|---|---|---|---|---|
| 0.10 | 0.478 | 0.026 | 0.047 | 0.077 | 0.112 | 0.072 |
| 0.20 | 0.632 | 0.047 | 0.079 | 0.127 | 0.185 | 0.095 |
| 0.30 | 0.705 | 0.059 | 0.103 | 0.160 | 0.228 | 0.106 |
| 0.40 | 0.740 | 0.065 | 0.120 | 0.179 | 0.253 | 0.111 |
| 0.50 | 0.750 | 0.071 | 0.119 | 0.185 | 0.261 | 0.112 |

**Max candidate parameters, anticipated C = 0.70.** Columns are effective n: vessels after DEFF, or participants for a person-level model.

| φ | 500 | 1,000 | 1,500 | 2,000 | 3,000 | 4,000 | 5,000 | 6,000 |
|---|---|---|---|---|---|---|---|---|
| 0.10 | 2 | 5 | 8 | 10 | 16 | 21 | 26 | 32 |
| 0.20 | 4 | 9 | 13 | 18 | 27 | 36 | 46 | 55 |
| 0.30 | 6 | 12 | 18 | 24 | 36 | 48 | 60 | 72 |
| 0.40 | 7 | 14 | 21 | 28 | 43 | 57 | 71 | 86 |
| 0.50 | 7 | 14 | 21 | 28 | 42 | 56 | 70 | 84 |

**Max candidate parameters, anticipated C = 0.75**

| φ | 500 | 1,000 | 1,500 | 2,000 | 3,000 | 4,000 | 5,000 | 6,000 |
|---|---|---|---|---|---|---|---|---|
| 0.10 | 4 | 8 | 13 | 17 | 26 | 35 | 44 | 53 |
| 0.20 | 7 | 15 | 22 | 30 | 45 | 60 | 76 | 91 |
| 0.30 | 9 | 19 | 29 | 39 | 58 | 78 | 97 | 117 |
| 0.40 | 11 | 22 | 33 | 44 | 66 | 88 | 110 | 133 |
| 0.50 | 11 | 22 | 34 | 45 | 68 | 91 | 114 | 137 |

**Max candidate parameters, conservative default R²_CS = 15% of max**

| φ | 500 | 1,000 | 1,500 | 2,000 | 3,000 | 4,000 | 5,000 | 6,000 |
|---|---|---|---|---|---|---|---|---|
| 0.10 | 4 | 8 | 12 | 16 | 24 | 33 | 41 | 49 |
| 0.20 | 5 | 11 | 16 | 22 | 33 | 44 | 55 | 66 |
| 0.30 | 6 | 12 | 18 | 25 | 37 | 50 | 62 | 75 |
| 0.40 | 6 | 13 | 19 | 26 | 39 | 52 | 65 | 78 |
| 0.50 | 6 | 13 | 20 | 26 | 40 | 53 | 66 | 80 |

**Design effect** for an average of 2.5 (or 2.0) eligible vessels per person [computed]:

| ICC_latent | DEFF (m̄ = 2.5) | DEFF (m̄ = 2.0) |
|---|---|---|
| 0.1 | 1.15 | 1.10 |
| 0.2 | 1.30 | 1.20 |
| 0.3 | 1.45 | 1.30 |
| 0.4 | 1.60 | 1.40 |
| 0.5 | 1.75 | 1.50 |

**Worked example (plug in real counts):** about 5,000 eligible vessels with DEFF 1.3 / 1.45 / 1.6 gives n_eff of about 3,846 / 3,448 / 3,125 [computed].
- At φ = 0.20 and C = 0.70 (R²_CS = 0.079): p_max = 3,125 × 0.1 × (-ln(1 - 0.079/0.9)), which is about 28-35 parameters across these n_eff values.
- **Required n for a planned p** at φ = 0.20, R²_CS = 0.079 [computed]: p = 15 → n ≥ 1,633; p = 25 → n ≥ 2,721; p = 40 → n ≥ 4,354 effective vessels. Criterion (ii) needs only 448 / 746 / 1,194 in these cases.
- At φ = 0.15 and R²_CS = 0.06: p = 15 / 25 / 40 → n ≥ 2,174 / 3,624 / 5,798.
- At φ = 0.30 and R²_CS = 0.103: p = 15 / 25 / 40 → n ≥ 1,234 / 2,057 / 3,291.
- **Recipe:** `pmsampsize(type = "b", cstatistic = 0.70, parameters = P, prevalence = φ)` gives n for vessels. Multiply by DEFF. Compare with the actual count of eligible vessels. Alternatively, compare with the participant count for a person-level model.

### Inferences
- The geometry block is the swing factor. "Position-aware" features expand quickly: k features × positions × 3 arteries, plus splines. Budget the df explicitly. For example, 10 df for clinical (SCORE2 components or SCORE2 as one LP, baseline plaque, log-CACS, artery 2 df, interval 1 df) and about 15-30 df for geometry. Beyond that, use penalisation or data reduction (PCA or clustering of geometry, or one learned geometry score from a separate split; see Q4).
- **Added-value tests need less n than full model development.** A likelihood-ratio test of a pre-specified geometry block adds df but does not require re-estimating the clinical part. However, Riley criteria still apply to the full model.
- With only one cohort there is no external validation. This is a key PROBAST+AI risk-of-bias point, so state it as a limitation.

### Gaps
- No published extension of the Riley criteria to within-person clustered units was found. The DEFF approach is a heuristic I propose; it is not validated in the literature I located. A simulation-based sample size (e.g. the `samplesizedev` package or the approach in arXiv 2509.14028) would be more rigorous.
- The "15% of max R²" default was not verified against the BMJ full text in this session (BMJ returned 403).

---

## Q4. Penalisation, splines, missing predictors, internal validation, measures of added value

### Takeaway
Pre-specify a main model and fit it with ridge (or ML with a small penalty) plus restricted cubic splines (3-4 knots) for key continuous predictors. Handle missing data with multiple imputation that includes the outcome (and artery, interval and cluster ID). Validate internally with participant-level bootstrap optimism correction, or with grouped CV by `study_id`. Judge geometry's added value with:
- an LR test (nested, pre-specified block);
- ΔC with a participant-bootstrap CI;
- calibration slope and calibration plots;
- decision-curve net benefit.

Avoid category-free NRI or IDI as primary evidence.

### Cited Findings
- **NRI** can be large for poorly fitting models and is "a misleading measure of prediction improvement even with independent test data". ROC-based measures, net benefit and the Brier score cannot be inflated in this way [fetched] — [Pepe et al., Stat Biosci 2015 (EDRN listing)](https://edrn.cancer.gov/data-and-resources/publications/26504496-the-net-reclassification-index-nri-a-misleading-measure-of-prediction-improvement-even-with-independent-test-data-sets)
- NRI and IDI require well-calibrated models [fetched, summary] — Leening et al., Stat Med 2014 via [Erasmus repository](https://repub.eur.nl/pub/53045/); background on NRI extensions in [Pencina, D'Agostino, Steyerberg, Stat Med 2011 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3156371)
- Penalisation does not rescue small samples. Shrinkage-tuning parameters are estimated with large uncertainty, so penalised models can still be unreliable when n is small. Use penalisation to supplement adequate n, not to replace it [known] — Riley RD et al., J Clin Epidemiol 2021;132:88-96, https://doi.org/10.1016/j.jclinepi.2020.12.005; Van Calster B et al., SMMR 2020, "Regression shrinkage methods for clinical prediction models do not guarantee improved performance", https://doi.org/10.1177/0962280220921415
- Calibration hierarchy (mean, weak, moderate, strong) and why calibration should be reported routinely [known] — Van Calster B et al., BMC Med 2019;17:230, "Calibration: the Achilles heel of predictive analytics", https://doi.org/10.1186/s12916-019-1466-7
- Decision curve analysis and net benefit [known] — Vickers AJ, Elkin EB, Med Decis Making 2006;26:565-74, https://doi.org/10.1177/0272989X06295361
- Reporting and risk of bias [known]:
  - TRIPOD+AI (Collins et al., BMJ 2024;385:e078378, https://doi.org/10.1136/bmj-2023-078378) covers regression and ML models.
  - PROBAST+AI (Moons et al., BMJ 2025;388:e082505, https://doi.org/10.1136/bmj-2024-082505).
  - Splines, bootstrap optimism correction and multiple imputation including the outcome are standard recommendations in Steyerberg, *Clinical Prediction Models*, 2nd ed., Springer 2019, https://doi.org/10.1007/978-3-030-16399-0.
- EPV for clustered data rises to about 50 when variable selection is done, which argues against stepwise selection [fetched] — [Wynants et al. 2015](https://researchinformation.umcutrecht.nl/en/publications/a-simulation-study-of-sample-size-demonstrated-the-importance-of-/)
- SCAPIS example of an added-value report: adding CCTA total plaque volume to SCORE2 + SIS increased the C-statistic from 0.783 to 0.798, with improved reclassification. This is a secondary news source (Sept 2026), so verify against the original [fetched] — [Diagnostic Imaging](https://www.diagnosticimaging.com/view/ccta-deep-learning-research-small-plaque-volume-coronary-atherosclerosis)

### Inferences (practical protocol)
- **Penalisation:**
  - Ridge is preferred for the full model because it keeps all pre-specified terms and gives the most stable calibration.
  - Lasso or elastic net only for exploratory screening of many geometry features, and the selection must be repeated inside every bootstrap or CV fold.
  - Tune λ by grouped CV (folds by `study_id`).
  - Report the bootstrap calibration slope even for penalised models.
- **Splines:** RCS with 3 knots (2 df) for age, SBP, cholesterol, log-CACS and the 1-3 main geometry features. Count spline df in Riley's p.
- **Missingness:**
  - MICE with m ≈ % incomplete cases, including the outcome, artery, log(interval) and the person-level clinical covariates.
  - For vessel-level geometry missing from failed segmentation, impute within a long format that carries person-level variables, or use multilevel imputation (`mice` 2l methods / `jomo`).
  - Missing geometry from poor image quality is likely not missing at random. The quality variables are in the data (`bad_quality`, `scan_qualitative_quality` in BL; unevaluable reasons in FU), so include them as auxiliary variables.
  - Validate by pooling performance across imputations, applying Rubin's rules to the log-odds of C.
- **Internal validation:**
  - Harrell bootstrap optimism, B ≥ 200, resampling participants with all their vessels. Repeat every modelling step in each bootstrap (imputation where feasible, spline fitting, λ tuning, any selection).
  - Report optimism-corrected C, calibration slope, CITL, Brier score and a calibration plot (loess/flexible) at the vessel and participant level.
  - Alternative: 10-fold grouped CV repeated 5-10 times. If a geometry representation is learned (e.g. a deep feature), it must be learned within the training folds only.
- **Added value of geometry:**
  1. LR test of the pre-specified geometry block in the clinical + geometry model vs clinical alone. Use robust (Wald/score) tests if fitted by GEE, because the LR test is not valid under GEE.
  2. ΔC (optimism-corrected) with a participant-bootstrap CI. The DeLong test for nested models is known to be conservative or invalid, so do not use it.
  3. Δ calibration slope and Brier score.
  4. Decision curves at threshold ranges relevant to intensifying prevention or re-scan timing (e.g. 10-40% 10-year risk of new plaque).
  5. If NRI is reported, use pre-specified risk categories, show event and non-event components separately, and never use it alone.
- Expect a small ΔC (about 0.01-0.03). SCAPIS reports +0.015 for a strong plaque marker. A small ΔC with a significant LR test is common and should be interpreted as such.

### Gaps
- No source located that evaluates multiple imputation for vessel-clustered imaging features specifically.
- I did not fetch the TRIPOD+AI, PROBAST+AI, Steyerberg, Van Calster or Riley 2021 penalisation texts in this session. Their citations are from prior knowledge.

---

## Q5. Published models for incident plaque / CAC conversion or progression in general populations

### Takeaway
The evidence base for **predicting incident plaque in plaque-free vessels** is thin. Most work predicts:
- **incident CAC** (MESA: Weibull survival or logistic, n of about 800-3,100 with CAC = 0);
- **lesion progression in symptomatic patients** (PARADIGM: logistic, lesion level, C 0.68 → 0.90); or
- **events from baseline plaque** (CGPS, SCAPIS).

Traditional risk factors predict incident CAC only modestly. No published prospective study shows that coronary geometry predicts new plaque in a general population, which makes the thesis question novel but means priors for R² must be conservative.

### Cited Findings
- **MESA, CAC = 0 warranty period:**
  - 3,116 participants with baseline CAC 0 and repeat scans over 10 y; Weibull parametric survival model for time to CAC > 0.
  - 10-year prevalence: CAC > 0 53%, > 10 36%, > 100 8%.
  - Warranty period for CAC > 0 was 3-7 y at a 25% testing yield, by sex and race/ethnicity.
  - [fetched, abstract-level] — [Dzaye et al., JACC Cardiovasc Imaging (record)](https://scholars.houstonmethodist.org/en/publications/warranty-period-of-a-calcium-score-of-zero-comprehensive-analysis-2/)
- **MESA, ≥ 65 y:** in 815 participants with CAC = 0, traditional risk factors performed poorly for predicting incident CAC; the paper examined nontraditional markers [fetched] — [Nontraditional risk markers for incident CAC among persons ≥ 65 (PMC11198298)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11198298/). A MESA analysis also reported family history of premature CHD OR 1.55 for incident CAC (same search; the specific paper was not opened).
- **PARADIGM, lesion-level progression to obstructive CAD:**
  - 1,297 patients, 3,218 lesions, 76 events (2.4%), interval 3.8 ± 1.6 y.
  - C-statistics: clinical 0.684; + per-patient plaque 0.825; per-lesion 0.895.
  - [fetched] — [Lee SE et al., Int J Cardiovasc Imaging 2020](https://pubmed.ncbi.nlm.nih.gov/32779077/)
- **CGPS (same cohort source as the thesis):**
  - 9,533 asymptomatic people aged ≥ 40 without known IHD had CCTA. 54% had no atherosclerosis, 36% non-obstructive, 10% obstructive.
  - Median follow-up 3.5 y; 71 MIs and 193 deaths.
  - Adjusted RR for MI: obstructive 9.19, extensive 7.65; obstructive-extensive 12.48 (95% CI 5.50-28.12).
  - Some news coverage misdates the paper as 2020; it is 2023.
  - [fetched, secondary summaries] — Fuchs A et al., Ann Intern Med 2023, DOI 10.7326/M22-3027 — [Wiley knowledge hub entry](https://ascvd-lipidology.knowledgehub.wiley.com/subclinical-coronary-atherosclerosis-and-risk-for-myocardial-infarction-in-a-danish-cohort-a-prospective-observational-cohort-study/); [HCPLive](https://hcplive.com/view/subclinical-asymptomatic-atherosclerosis-linked-to-8-fold-increase-in-myocardial-infarction); [nhi.no summary](https://nhi.no/for-helsepersonell/fra-vitenskapen/subklinisk-koronar-aterosklerose-og-risiko-for-hjerteinfarkt)
- **SCAPIS:**
  - TPV added to SCORE2 + SIS: C 0.783 → 0.798; highest TPV category adjusted HR 6.36.
  - In CAC = 0, TPV > 0-32.1 mm³ gave HR 2.63 (outcome = events, not incident plaque).
  - Secondary news source, Sept 2026 [fetched] — [Diagnostic Imaging](https://www.diagnosticimaging.com/view/ccta-deep-learning-research-small-plaque-volume-coronary-atherosclerosis)
  - SCORE correlated with TPV at rho = 0.30 [fetched] — [Chalmers record](https://research.chalmers.se/en/publication/535874)
- **Geometry and plaque:**
  - A prospective protocol (GEOMETRY-CTA, about 100 patients, 12-month follow-up, geometric risk score of bifurcation angle, tortuosity and vessel volume) has no published results found.
  - Retrospective work links LAD tortuosity plus LM-LAD angle to proximal LAD stenosis (n = 133).
  - CFD on 39 left coronary trees suggests curvature and oscillatory shear matter for plaque onset in non-bifurcating segments.
  - [fetched, search summaries] — [CFD study, arXiv 2312.00257](https://ar5iv.labs.arxiv.org/html/2312.00257); [ESC365 entry](https://esc365.escardio.org/journal/47612); [QIMS retrospective article](https://qims.amegroups.org/article/view/117032/html)

### Inferences
- Model families used in this literature:
  - Weibull or interval-censored survival (MESA conversion), equivalent to the cloglog + log(t) recommendation in Q1;
  - logistic at lesion or patient level (PARADIGM);
  - Poisson or Cox for events (CGPS, SCAPIS).
  - None used formal Riley-type sample-size justification in the abstracts seen.
- For anticipated performance: clinical-only C for new or progressing plaque is about 0.65-0.70 (PARADIGM clinical 0.684; MESA ≥ 65 says risk factors are weak). This supports using C = 0.70 (or 0.65 in a pessimistic scenario) in pmsampsize, not 0.75+.
- Incidence prior: MESA's 53% 10-year conversion from CAC 0 is per person, for any CAC in the whole tree. Per-trunk incidence of any plaque (including non-calcified) in CCTA-confirmed plaque-free trunks will be lower per vessel, perhaps around 15-35% (my speculative range). The sister note's real counts should replace this.

### Gaps
- Kronmal et al. (Circulation 2007, MESA incident CAC risk factors) could not be retrieved, so its n, events and ORs are not reported here.
- No Rotterdam Study or Heinz Nixdorf Recall incident-CAC prediction model with performance metrics was retrieved in this session.
- No published model was found that predicts **incident CCTA-defined plaque (calcified or non-calcified) in plaque-free vessels** in a general population. I did not locate any serial-CCTA CGPS publication on incident plaque.
- SCAPIS figures come from a news article. The primary paper was not located.
