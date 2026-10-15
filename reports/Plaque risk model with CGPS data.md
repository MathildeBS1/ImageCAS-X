# Real CGPS data shrink the model budget

**The real CGPS aggregates keep penalisable regression as the primary model, but they cut the parameter budget, so the model must be smaller than the earlier report planned.** The primary model is a vessel-level binary regression with a complementary log-log (cloglog) link, fitted to baseline plaque-free LAD, CX and RCA trunks. Log follow-up time enters as a free covariate, and standard errors and resampling are clustered by participant. Its first job is to test whether a prespecified geometry block of about 6 degrees of freedom adds to SCORE2 risk factors, plaque elsewhere and calcium. Gradient boosting stays as a prespecified benchmark on identical inputs, and any neural or geometry-fusion model is reduced to one cross-fitted score inside that regression.

Three facts drive the change:

- **Baseline segment reads exist for only about 1,020 of the 2,116 paired participants.** As currently coded, the trunk design draws only on that read half.
- **The interval is a decade, not 3 to 5 years.** It runs from 9.5 to 15.3 years (median 10).
- **New plaque is common and clustered.** In the closest vessel-level proxy, about 39% of clean vessels develop plaque, with a within-patient intraclass correlation (ICC) of 0.27.

Together these give roughly 1,800 eligible arteries and 700 events at most. That is an effective sample of about 1,200 arteries, which supports about **12 to 27 candidate parameters** under the Riley criteria (central estimate 16 at an anticipated C of 0.70). The earlier plan assumed 25 parameters at participant level and about 30,000 segments.

The choice is not final. The exact trunk-design counts ("section 0" of `cgps_stats.py`) are missing from `report.md`. So is the read/unread stratification. Whether the 1,094 unread participants were genuinely normal could double or triple the sample, and it has to be settled in the secure environment first.

## The real cohort overturns five planning assumptions

The earlier recommendation was built on literature-based guesses. Every guess that mattered for model choice now has a measured counterpart, and most moved in an unfavourable direction for sample size.

All 2,116 participants have exactly one follow-up scan. The interval has a **median of 10 years, mean 11, p5 9.52 and p95 15.3**, with nobody under 5 years ([report.md §1](../CGPS_data/report.md)). The earlier report assumed a 3 to 5 year interval and borrowed PARADIGM's 35.6% incidence over 3.6 years ([Won et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9655903/)). The real rates are higher:

- **47.0% (124/264)** of read participants who were plaque-free across the whole tree developed plaque ([report.md §7, whole tree](../CGPS_data/report.md)).
- **39.0% (697/1,789)** of LAD, CX and RCA vessels that were plaque-free at baseline did so. This is derived from the three per-vessel cells, with side branches included and without the left main (LM) rule ([report.md §7, vessel](../CGPS_data/report.md)).

The bigger surprise is coverage. Every trunk segment's baseline stenosis field is empty in **1,094 participants**, and patient-level segment outcomes exist for n = 1,020 ([report.md §5](../CGPS_data/report.md)). The trunk-eligibility rule in `artery_design()` requires every trunk segment to be decoded as evaluable. It therefore silently excludes the whole unread half ([cgps_stats.py, artery_design](../CGPS_data/cgps_stats.py)).

| Quantity | Earlier assumption | Real CGPS aggregate | Consequence |
|---|---|---|---|
| Interval | 3 to 5 years | median 10, p5 9.52, p95 15.3 y | Fixed 10-year prediction horizon; log-time covariate instead of a forced offset |
| Analysable participants | about 2,000 | 2,116 paired, but about 1,020 with baseline segment reads | Trunk design is a read-subgroup analysis until the unread half is resolved |
| Plaque-free at baseline | about 54% (about 1,080 participants) | 264 read participants plaque-free across the whole tree | Participant-level "plaque-free" model is infeasible (about 2 to 3 parameters) |
| New plaque in clean units | 25 to 35% | 47.0% whole tree; 39.0% vessel proxy | Outcome is common and close to balanced |
| Analysis unit | about 30,000 segments | at most about 1,800 trunks (user-chosen design) | Budget is set by trunks, not segments |
| Within-patient ICC | 0.1 to 0.4, unknown | 0.272 vessel (design effect 1.46); 0.145 segment; 0.382 position | Effective n about 1,200 arteries |
| Hard clinical events | not considered | 10/1,973 | No clinical-outcome model is possible |

The read half also looks plaque-enriched. Only 264 of about 1,020 read participants (about 26%) were plaque-free across the whole tree. In the full CGPS CCTA cohort, 54% had no atherosclerosis ([Fuchs et al. 2023, via Wiley summary](https://ascvd-lipidology.knowledgehub.wiley.com/subclinical-coronary-atherosclerosis-and-risk-for-myocardial-infarction-in-a-danish-cohort-a-prospective-observational-cohort-study/)).

My reading, which is an inference and not a reported fact, is that baseline reads were done preferentially on scans with disease. If so, most eligible trunks sit in people who already have plaque elsewhere. "Plaque elsewhere" will then be strongly informative within this sample, and the fitted model will transport poorly to the people a primary-prevention model targets. This needs checking.

Two other facts reshape what "new plaque" means after a decade. First, new plaque in clean vessels agrees closely with new calcium: Cohen's kappa against vessel incident calcium (CAC) is **0.802**. Second, baseline total CAC is the strongest single predictor of vessel new plaque, with an **AUC of 0.697**, against 0.61 for age, 0.61 for sex and 0.62 for systolic pressure ([report.md §7, vessel](../CGPS_data/report.md)). In practice the outcome is mostly "a clean trunk calcifies within ten years". Geometry therefore has to show value on top of a strong calcium signal, not on top of weak risk factors.

## Seven hundred events afford sixteen parameters, not twenty-five

The Riley criteria for a binary outcome require:

- expected shrinkage of at least 0.9;
- optimism in Nagelkerke R² of at most 0.05;
- precise estimation of the overall risk.

They are implemented in `pmsampsize` ([pmsampsize manual](https://rdrr.io/pkg/pmsampsize/man/pmsampsize.html); [Riley et al., BMJ 2020](https://doi.org/10.1136/bmj.m441)). There is no published extension to vessels clustered within people. The pragmatic heuristic is to divide the number of vessels by the design effect, so the effective n lies between the number of participants and the number of vessels. The design-effect formula is the standard survey one ([MetricGate design-effect doc](https://metricgate.com/docs/sample-size-mixed-model/)), and its use here is an assumption to state in the thesis.

I computed Cox-Snell R² from an anticipated C-statistic using the Riley-Van Calster-Collins simulation method ([Riley, Van Calster, Collins 2021](https://research.birmingham.ac.uk/en/publications/a-note-on-estimating-the-cox-snell-rsub2sub-from-a-reported-c-sta)). I then inverted criterion (i), which bound in every scenario, for the real proxies. These are my calculations, not outputs of `report.md`.

| Scenario | Units, event fraction, design effect | Effective n | Max parameters at C = 0.65 / 0.70 / 0.75 |
|---|---|---|---|
| Central: read half, vessel proxy from §7 | 1,789; 0.39; 1.46 | 1,225 | **9 / 16 / 27** |
| Pessimistic: LM rule and evaluability shrink LAD and CX | 1,400; 0.35; 1.50 | 933 | 6 / 12 / 19 |
| Per-artery model, LAD | about 350; 0.40 | 350 | 2 / 4 / 7 |
| Per-artery model, CX or RCA | about 650 to 750; 0.35 to 0.38 | 650 to 750 | 4 to 5 / 8 to 9 / 14 to 15 |
| Participant level, whole-tree plaque-free | 264; 0.47 | 264 | 2 / 3 / 6 |
| Unread half accepted as plaque-free (speculative) | about 4,700; about 0.25; 1.6 | about 2,940 | 17 / 31 / 51 |

The conservative default of 15% of the maximum Cox-Snell R² gives 16 parameters in the central scenario and 12 in the pessimistic one. That agrees with the C = 0.70 column.

Which column applies? The clinical-only C for plaque outcomes in the literature is about 0.68 to 0.70. Examples are PARADIGM's clinical model at 0.684 ([Lee et al. 2020](https://pubmed.ncbi.nlm.nih.gov/32779077/)) and the PARADIGM risk score falling from 0.732 to 0.668 on validation ([Eur Radiol 2023](https://link.springer.com/article/10.1007/s00330-023-09880-x)). Here, though, calcium alone reaches 0.70 at vessel level and artery identity adds signal. A full-model C of 0.72 to 0.75 is therefore plausible. **I would plan for about 18 to 20 candidate parameters and verify this against `pmsampsize` once the section-0 event fraction is known.**

The earlier figure of 25 parameters was a participant-level calculation over all 2,000 participants. The real trunk design is smaller in effective size and must pay for artery and position terms out of the same budget. Per-artery models are ruled out (LAD affords about 4 parameters). A participant-level "plaque-free person" model is ruled out too. Any geometry representation with more than a handful of free parameters must be learned outside the outcome model, or shrunk.

Accepting the unread half as genuinely plaque-free would roughly double the budget. There is indirect support for it. The unread participants' whole-tree plaque rate at follow-up (50.1%, derived) resembles that of read whole-tree-normal participants (47.0%). But at least about 84 to 91 participants with a segment involvement score (SIS) of 0 have baseline CAC above 0 ([report.md §3–4](../CGPS_data/report.md)). This is the **single largest lever on model choice**, and it can only be resolved from the baseline volumes or the data manager.

## A cloglog trunk model with a six-degree geometry block

Each trunk is clean at baseline and inspected once, after about a decade. That makes these current-status (interval-censored) data. Under proportional hazards, the grouped-time likelihood is a binary model with a cloglog link, and its coefficients are log hazard ratios ([SAS PROC LOGISTIC documentation](https://support.sas.com/documentation/cdl/en/statug/63033/HTML/default/statug_logistic_sect065.htm)). Entering log(interval) as a free covariate is equivalent to a Weibull baseline hazard. That is the same model family MESA used for conversion from CAC = 0 over 10 years ([Dzaye et al., JACC CV Imaging 2021](https://scholars.houstonmethodist.org/en/publications/warranty-period-of-a-calcium-score-of-zero-comprehensive-analysis-2/)).

The earlier report fixed log(interval) as an offset. The real data argue against forcing a constant hazard. Event rates by follow-up tertile are flat to non-monotone (vessel proxy **33.3%, 30.7%, 38.6%**), and follow-up years alone have an AUC of only **0.539** ([report.md §7](../CGPS_data/report.md)). Follow-up length also tracks statin initiation (mean 11.3 years in starters). **Fit log(years) as a free covariate, keep the offset as a sensitivity analysis, and compute all predicted risks at a fixed 10-year horizon.** Logistic regression with the same terms is a second sensitivity analysis. At event fractions near 40% the two links diverge only in the tails.

### Clustering and the earlier mixed-model choice

The earlier report preferred a random-intercept GLMM because segment hazards summed neatly to a participant risk. That argument loses force in a trunk design with one to three units per person, for three reasons:

- the thesis estimand is now vessel-level risk;
- the random-intercept variance is identified only from people with two or more eligible trunks;
- conditional predictions with the random effect set to zero are miscalibrated for new patients, so they must be marginalised anyway ([Pavlou et al. 2015](https://doi.org/10.1186/s12874-015-0046-6)).

**The primary fit should therefore be marginal.** That means maximum likelihood under independence with participant-clustered sandwich standard errors, plus participant-level bootstrap and cross-validation. The random-intercept GLMM becomes the sensitivity analysis that reports the latent-scale ICC. Eligible trunks are selected non-randomly, because people with more disease contribute fewer clean trunks. So also report a fit that weights each participant equally (weights 1/mᵢ).

### Model specification and budget

| Block | Terms | df |
|---|---|---|
| Design | artery (LAD, CX, RCA); log(follow-up years) | 3 |
| SCORE2 risk factors | age (restricted cubic spline, 3 knots); male; current smoking; systolic BP; total cholesterol; HDL | 7 |
| Imaging baseline | log(1 + total CAC); number of segments with plaque elsewhere | 2 |
| Population stratum | rand_group 2 indicator | 1 |
| **Model 0 total** | | **13** |
| Geometry block (illustrative; fix on ImageCAS-X before outcomes are opened) | mean trunk curvature; 2 mean-removed FPCA position scores; tortuosity; ostial take-off or bifurcation angle; proximal lumen size | **6** |
| **Model 1 total** | | **19** |

Several choices in the table need justifying.

**Diabetes is left out of the primary model.** It is not a SCORE2 input, and its prevalence is 1.89% ([report.md §13](../CGPS_data/report.md)), which is concentrated in rand_group 2 (4.97%). Within about 1,000 read participants with clean trunks it would invite separation, so it belongs in a sensitivity analysis.

**rand_group 2 gets its own term.** This group is older and has 26% lipid-lowering use and 50.3% incident CAC, against about 34% in groups 0 and 1. All 10 hard events occurred in it ([report.md §11](../CGPS_data/report.md)). It is a different population, so it needs a term (or exclusion in a sensitivity analysis), not silent pooling.

**Baseline lipid-lowering is left out.** It enters only in sensitivity analyses. Statin initiation during follow-up (510 participants) is post-baseline and must never be adjusted for in the prediction model.

**The SCORE2 inputs are complete enough.** All are at least 98% complete: age, sex and smoking have 0 missing, systolic BP 26, and cholesterol and HDL 38 each. Single-digit-percentage multiple imputation that includes the outcome, artery, log-time and cluster ID is sufficient. BMI, HbA1c, smoking-years and heart rate during the scan are 50 to 89% missing and are excluded ([report.md §2](../CGPS_data/report.md)).

**Total CAC is the calcium term, not per-vessel CAC.** Per-vessel CAC of the eligible trunk should be zero, so it is uninformative. A positive value flags a possible missed plaque, which is what the section-0 "calcium check" counts.

**Geometry slopes are shared across arteries.** Each feature is standardised within artery instead of interacted with it, because one artery-by-feature interaction costs 2 df. FPCA scores are computed on the mean-removed profile so that the position block is nested in the mean-curvature term.

The position-aware design fits this framework without segment-level outcomes. The user chose trunk outcomes because automated geometry cannot reproduce reader proximal/mid/distal boundaries. Position therefore enters through the geometry features, either as windowed curvature or FPCA scores, not through the outcome.

## Boosting benchmarks the regression; networks compete only as one score

Low-risk-of-bias comparisons find no AUC advantage for machine learning over logistic regression: the logit(AUC) difference is **0.00 (95% CI −0.18 to 0.18)** across 145 comparisons. The apparent ML gains come from high-risk-of-bias studies ([Christodoulou et al. 2019](https://www.sciencedirect.com/science/article/abs/pii/S0895435618310813)). In cardiovascular primary prevention, the pooled ML gain over traditional scores is about 0.014 in C, and 81% of the ML models were at high risk of bias ([Liu et al. 2023](https://academic.oup.com/ehjqcco/article/9/4/310/7069320)).

Flexible learners are also data-hungry. Logistic regression stabilised at about **20 to 50 events per variable**, while random forests needed more than 200 ([van der Ploeg et al. 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289553)). Penalised logistic regression needs fewer data than ensembles to calibrate ([Austin, Lee and Wang](https://pmc.ncbi.nlm.nih.gov/articles/PMC11539735)). The closest CCTA plaque precedent is SCOT-HEART, with n = 1,769, where XGBoost did not significantly beat the ASSIGN score for low-attenuation plaque (AUC 0.75 vs 0.72, p = 0.08) ([Williams et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12406813/)).

With about 700 events, an effective n of about 1,200 and 19 parameters, the regression sits at roughly 37 events per parameter. That is inside its stable band. Any tree ensemble on the same inputs is well below the range where ensembles stabilised.

**XGBoost therefore drops from "prespecified secondary with a substantive role" to "prespecified benchmark".** Its specification is:

- shallow trees (depth 2 to 3) with strong shrinkage;
- exactly the Model 0 and Model 1 inputs;
- tuning by nested cross-validation grouped by participant;
- reporting of calibration and instability.

Its single question is whether the spline regression missed a strong non-linearity or interaction. The realistic prior for that gain is about 0 to 0.02 in AUC. That is smaller than the confidence interval this sample can produce, so a null result is the expected and reportable outcome. SHAP output is descriptive only, because SHAP misattributes credit among correlated features ([arXiv 2509.00846](https://arxiv.org/pdf/2509.00846)), and curvature, tortuosity and size are strongly inter-correlated. Group-level importance by refit is the defensible alternative.

The neural arm loses most of the affordability the earlier report granted it. That report counted 700 to 1,000 participant events plus 500 to 1,500 segment events for an outcome-trained encoder. The real trunk design has at most about 700 correlated vessel events, and networks needed more than 100 events per variable in simulation ([van der Ploeg et al. 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289553)). The only coronary geometric deep-learning precedents predict wall shear stress, not plaque, and they relied on pretraining on 8,449 vessel point clouds to work at n = 49 ([GReAT, arXiv 2508.19030](https://arxiv.org/pdf/2508.19030)).

The viable configuration is therefore an **outcome-free, self-supervised encoder**. It is pretrained on ImageCAS-X and on all CGPS baseline trees, then frozen, and it emits one cross-fitted, out-of-fold score per trunk that enters Model 1 as a single degree of freedom. Pretraining can include the 1,094 unread participants, because it needs no reads.

That score must beat two controls. One is a cross-fitted MiniRocket-plus-ridge score; MiniRocket matched leading classifiers on 109 UCR datasets at far lower cost ([Dempster et al. 2021](https://arxiv.org/pdf/2012.08791)). The other is a shuffled-order profile. Fine-tuning beyond the last layer, point-cloud or graph networks trained end to end, and CT-image models are exploratory at most.

| Model | Role at the real sample size | What it answers |
|---|---|---|
| Cloglog trunk regression, Model 0 → Model 1 (unpenalised for inference; ridge for prediction) | **Primary** | Does a prespecified geometry block add to SCORE2, plaque elsewhere and calcium? |
| Random-intercept GLMM; logistic link; log-time offset; 1/mᵢ weights | Sensitivity | Robustness to the clustering, link and time assumptions |
| Shallow XGBoost (optionally TabPFN) on identical inputs | Prespecified benchmark | Did the regression miss non-linearity or interaction? |
| FPCA / MiniRocket score inside the regression | Secondary | Does the position profile carry information beyond the summaries? |
| Frozen self-supervised encoder score (cross-fitted, 1 df) | Exploratory | Does a learned profile beat MiniRocket and the shuffled control? |
| Per-artery models; participant-level plaque-free model; clinical events | Not feasible | About 2 to 7 parameters available, or only 10 events |

### Validation and added-value protocol

Every resampling step is grouped by `study_id`. Internal validation uses a Harrell bootstrap with at least 200 participant resamples, repeating imputation, spline fitting and penalty tuning inside each resample. Five-by-ten repeated grouped cross-validation is an alternative. Report the following at the 10-year horizon, at vessel level and, from the GLMM, as participant-level "any eligible trunk" risk:

- optimism-corrected C;
- calibration slope and calibration-in-the-large;
- Brier score;
- a flexible calibration curve;
- prediction-instability plots ([Riley and Collins 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10952221/)).

The added-value test of geometry is a cluster-robust Wald test of the 6-df block, on unpenalised fits. A likelihood-ratio test from the GLMM is a sensitivity analysis. A GEE-type fit has no likelihood, and a likelihood-ratio statistic from a ridge fit has no chi-square reference. ΔC (bootstrap confidence interval, no DeLong test), Δlog-likelihood, ΔBrier and decision curves are effect sizes.

ΔAUC is a much weaker test than likelihood-based tests ([Vickers, Cronin and Begg 2011](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3042425/)). NRI can be positive for uninformative markers, so it is at most secondary, with prespecified categories ([Pepe et al. 2015](https://edrn.cancer.gov/data-and-resources/publications/26504496-the-net-reclassification-index-nri-a-misleading-measure-of-prediction-improvement-even-with-independent-test-data-sets)). A within-artery permutation of the geometry features is the negative control. The realistic expectation is a ΔC of about 0.01 to 0.02. For comparison, SCAPIS reports +0.015 for total plaque volume on top of SCORE2 and SIS, but that figure comes from a secondary news source and must be verified ([Diagnostic Imaging](https://www.diagnosticimaging.com/view/ccta-deep-learning-research-small-plaque-volume-coronary-atherosclerosis)). Report following TRIPOD+AI and TRIPOD-Cluster ([Debray et al. 2023](https://pmc.ncbi.nlm.nih.gov/articles/9903175)), and state that there is no external validation.

The prespecified sensitivity set is:

- the outcome at ≥ mild instead of ≥ minimal. Reader noise is real: 20.3% of baseline plaque segments read as plaque-free at follow-up ([report.md §7, segment](../CGPS_data/report.md));
- the "combined" definition requiring vessel CAC = 0 at baseline;
- RCA with and without the LM rule;
- excluding rand_group 2;
- adding diabetes and baseline lipid-lowering.

There is also a secondary outcome that does not depend on baseline reads: vessel incident CAC in vessels with zero calcium. It uses all 2,116 participants and gives LAD 475/1,384, CX 382/1,798 and RCA 368/1,723 ([report.md §3](../CGPS_data/report.md)). It is the one analysis that can use the full cohort today, but it does not guarantee a plaque-free trunk.

## What the secure environment must produce before the choice is final

`report.md` was generated before section 0 and the new strata were added to `cgps_stats.py`. Searches of the report for the design and strata return nothing ([cgps_stats.py](../CGPS_data/cgps_stats.py)). Each item below changes a number in the specification above. All outputs should keep the existing small-cell suppression.

| Re-run or addition | Why it matters for the model choice |
|---|---|
| Section 0 (`artery_design`) as written: eligibility flow per artery, eligible n, events at ≥ minimal, ≥ mild and ≥ moderate | Replaces the 1,789 / 697 proxy; sets the event fraction and the Riley budget |
| LM-rule effect, and RCA with and without the LM rule | LM plaque in about 21% of read participants may shrink LAD and CX below the pessimistic scenario |
| Pooled ICC, design effect, patients contributing, eligible arteries per patient | Effective n; whether the 1/mᵢ weighting matters |
| Noise check, where the new plaque appeared, calcium check (eligible trunks with vessel CAC > 0) | Outcome reliability; choice of position windows; possible missed plaque |
| Single-predictor AUCs and follow-up tertile rates in the trunk design | Anticipated C for `pmsampsize`; log-time versus offset |
| "BL segment reads present" and "BL scan year" strata (already in the script) | Tests whether the read half is plaque-enriched, and whether follow-up length reflects scan-year cohorts |
| New: rand_group × read-status cross-tab; predictor missingness, diabetes count and baseline lipid-lowering among eligible trunks | Covariate set, separation risk and imputation needs within the analysed sample |
| New: geometry-pipeline success rate per eligible trunk, by artery and image quality | Missing-geometry mechanism (likely not at random; mid-RCA is unevaluable at follow-up in 197 participants) |
| `pmsampsize` with the real event fraction and anticipated C of 0.70 and 0.75, divided by the design effect | Confirms or cuts the 19-df specification |
| Resolution of the 1,094 unread participants (baseline volumes or data manager), then section 0 re-run with them included if they were genuinely normal | Could raise the budget to about 30 to 50 parameters and restore primary-prevention generalisability |

## Conclusion

The real data move the binding constraint from the choice of learner to who is in the denominator. A decade of follow-up makes new plaque common enough that events are not scarce. Instead, the analysable sample is set by which baseline scans were read, and the read half appears to be enriched for people who already have plaque. Two consequences follow. A null geometry effect in the read-only analysis would say little about plaque-free individuals in a screening population. And the most valuable next step for the thesis is a phone call to the data manager about the unread scans, not a more sophisticated model.

The outcome is in practice "a clean trunk calcifies within ten years", and calcium is the strongest competitor. Geometry is therefore most likely to be informative about which trunk calcifies, the "where" question, rather than who does. The pooled artery term and the within-artery standardised geometry are where that signal would show first. A modest, well-calibrated regression that shows a significant 6-df geometry block with a ΔC of about 0.01 to 0.02 would be a novel and defensible result. A boosted or neural model that claims much more on this sample should be treated as evidence of leakage until proven otherwise.
