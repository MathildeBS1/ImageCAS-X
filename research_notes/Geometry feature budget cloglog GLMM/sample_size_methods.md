# Sample-size / parameter-budget methods for a segment-level cloglog GLMM aggregated to person risk

Labels: **[own calc]** = numbers computed for these notes (script below), not from a source; **[inference]** = my reasoning, not a sourced claim. Project numbers (1,076 people, 452 events, ~9,700 segment rows, ~1,100 segment events) are taken from the brief; the segment-event count is a project estimate, not a count.

Own-calc script: `/private/tmp/claude-501/-Users-mathildebrinchsorensen-Desktop-ImageCAS-X/c3efb813-32ee-4e68-85e1-b6419e4abc2e/scratchpad/riley.py` (Riley criteria 1–2 solved for p at fixed n; C→R²_CS via the normal-linear-predictor approximation with the true logistic model, 10⁶ draws).

## Q1. Does Riley/pmsampsize apply to clustered data, and is there a published clustered/multilevel extension?

### Takeaway
No published extension of the Riley criteria to clustered or multilevel development data was found; pmsampsize assumes independent individuals, and a 2026 methods overview explicitly lists hierarchical data as future work. The only clustered-data sample-size evidence for prediction models is simulation (Wynants 2015: clustering had little impact; EPV mattered), which concerns patients clustered in centres, not repeated units within a person.

### Cited Findings
- pmsampsize binary criteria: (i) expected shrinkage ≤ 10% (S ≥ 0.9), (ii) absolute difference ≤ 0.05 between apparent and adjusted Nagelkerke R², (iii) average risk estimated within ±0.05. Input `parameters` = "the number of candidate predictor parameters for potential inclusion in the new prediction model", which "may be larger than the number of candidate predictors". No mention of clustering. — [pmsampsize reference manual, CRAN](https://cran.r-project.org/web/packages/pmsampsize/refman/pmsampsize.html)
- Source papers: Riley RD et al. Minimum sample size for developing a multivariable prediction model: Part II – binary and time-to-event outcomes. Stat Med 2019;38:1276–1296, doi:10.1002/sim.7992; Riley RD et al. Calculating the sample size required for developing a clinical prediction model. BMJ 2020;368:m441, doi:10.1136/bmj.m441. The BMJ paper states that "the amount of model overfitting is dictated by the total number of predictor parameters considered, not just those included in the final model equation" and that required size depends on events per candidate parameter, total participants and outcome proportion. — [Utrecht repository record of BMJ 2020](https://dspace.library.uu.nl/handle/1874/457642); [ResearchGate record of Part II](https://www.researchgate.net/publication/328539604_Minimum_sample_size_for_developing_a_multivariable_prediction_model_PART_II_-_binary_and_time-to-event_outcomes) (full texts not fetched: 403)
- The closest formal extension found is to multinomial outcomes, not clustering: Pate A, Riley RD, Collins GS, van Smeden M, Van Calster B, Ensor J, Martin GP. Stat Methods Med Res 2023, doi:10.1177/09622802231151220. — [PMC10012398](https://pmc.ncbi.nlm.nih.gov/articles/PMC10012398/)
- Shamsutdinova D, Zimmer F, …, Carr E. "Sample Size Calculations for Developing Clinical Prediction Models: Overview and pmsims R package", arXiv:2602.23507 (Feb 2026, preprint): closed-form approaches rely on distributional assumptions limiting generalisability "especially for complex settings such as multilevel data"; "Future work should extend these methods to hierarchical and multimodal data." — [arXiv 2602.23507](https://arxiv.org/abs/2602.23507)
- Wynants L, Bouwmeester W, Moons KGM, Moerbeek M, Timmerman D, Van Huffel S, Van Calster B, Vergouwe Y. A simulation study of sample size demonstrated the importance of the number of events per variable to develop prediction models in clustered data. J Clin Epidemiol 2015;68(12):1406–1414, doi:10.1016/j.jclinepi.2015.02.002. Varied ICC 0/5/20%, EPV 5/10/20/50, backward selection. Clustering was not meaningfully associated with predictive performance; at ICC 20% median calibration slope ≈ 0.71 (EPV 5), ≈ 0.85 (EPV 10), ≈ 0.96 (EPV 50). Recommends EPV ≥ 10, up to 50 with variable selection. — [EUR repository](https://repub.eur.nl/pub/91572); [Utrecht record](https://utrecht-main-test.atmire.com/items/47a03d88-caec-41f4-a83b-f04c8ad70046)
- Wynants, Van Huffel, Van Calster review (Diagn Progn Res/BMC 2015) "extend[s] the EPV guidelines to multicenter studies, acknowledging the clustered nature of the data"; residual ICC quantifies inter-centre variability. Details not in abstract. — [PMC4582405](https://pmc.ncbi.nlm.nih.gov/articles/PMC4582405/)
- Falconieri N, Van Calster B, Timmerman D, Wynants L (Biom J 2020, doi:10.1002/bimj.201900075): in multicentre simulations random-intercept logistic regression gave better centre-specific calibration; small samples gave overfitting. — [OCRA research exchange record](https://researchexchange.ocrahope.org/papers/bimj-201900075) (abstract-level only)
- Moineddin R, Matheson FI, Glazier RH. A simulation study of sample size for multilevel logistic regression models. BMC Med Res Methodol 2007;7:34, doi:10.1186/1471-2288-7-34. Groups of 5/30/50, 30/50/100 groups, ICC 0.04/0.17/0.38. Fixed effects close to unbiased with 100 groups of 50; variance components more biased than fixed effects and their SEs underestimated; with groups of size 5 bias was severe (variance estimates sometimes > 100% biased). Recommends ≥ 50 groups of ≥ 50. Note: this is about parameter estimation including random slopes, not prediction. — [PMC1955447](https://pmc.ncbi.nlm.nih.gov/articles/PMC1955447/)

### Inferences
- [own calc] Reproducing the thesis's person-level Riley number: n = 1,076, φ = 0.42, max R²_CS = 0.744. Criterion 1 (S = 0.9) binds: P_max ≈ **8.4 at C = 0.65, 15.2 at C = 0.70, 24.2 at C = 0.75** (R²_CS ≈ 0.068 / 0.119 / 0.181). Criterion 2 is not binding (≈ 42–45). Criterion 3: 95% CI half-width of the risk = 0.029 < 0.05, met. So the thesis's "P_max ≈ 15 at C = 0.70" is reproduced, but it is very sensitive to the anticipated C: ±0.05 in C moves the budget from ~8 to ~24. The C used must be the anticipated *optimism-adjusted* C of the full model (pmsampsize manual), i.e. base + geometry, which for SCORE2 in a plaque-free cohort is itself uncertain.
- [own calc] A naive segment-level Riley count (n = 9,700, φ = 0.113, C = 0.70–0.75 at segment level) gives P_max ≈ 59–94. This treats segments as independent and is not a valid budget; it is only an upper bound for parameters identified mainly from segment-level variation (see Q2).
- [own calc] Harrell's rule (below) gives a much looser person-level number: m = 3nq(1−q) = 3·1,076·0.42·0.58 ≈ 786, p < m/15 ≈ 52. Riley at C = 0.70 is ~3.5× stricter because it uses the expected R² (low signal → more shrinkage). The thesis should state which criterion it uses and why; Riley is the current standard (TRIPOD-era guidance) and is the more conservative.
- [inference] Wynants 2015 and Falconieri 2020 concern patients clustered in centres (few large clusters, cluster = nuisance). The thesis structure is the inverse: many small clusters (1,076 persons × 9 segments) and the prediction target is the *cluster* (person). Their "clustering hardly matters" result should not be transferred.
- [inference] Moineddin's "group size 5 is bad" concerns variance and random-slope estimation with ≤ 100 groups. With 1,076 groups the random-intercept variance should be reasonably estimated, but it is identified only from within-person co-occurrence of segment events.

### Gaps
- No paper found that derives Riley-type criteria (shrinkage, optimism, intercept precision) for a GLMM, for clustered binary outcomes, or for unit-level models aggregated to cluster-level predictions.
- Full texts of Riley 2019 Part II and BMJ 2020 could not be fetched (403); the exact R²_CS-from-C approximation (Riley et al. 2022, Diagn Progn Res "A note on estimating the Cox-Snell R² from a reported C statistic") was reimplemented, not checked against pmsampsize output.

## Q2. How should person-level vs segment-level (within-person) parameters be counted?

### Takeaway
No formal "level-specific parameter budget" for prediction models was found. Survey/multilevel theory gives a design effect for a regression coefficient that depends on both the covariate's and the outcome's intraclass correlation (≈ 1 + (m−1)ρxρy), so a within-person-varying covariate draws information from segment events, discounted by clustering, whereas a person-constant covariate (ρx = 1) is limited by person-level information. This supports a two-budget reading, but it is an inference, not published guidance.

### Cited Findings
- Kish design effect for means with equal clusters: 1 + (m−1)ρ; effective n = n/DEFF. — [PracTools vignette, CRAN](https://cran.r-project.org/web/packages/PracTools/vignettes/Design-effects.html); [MetricGate](https://metricgate.com/docs/multilevel-logistic-sample-size/)
- For a regression coefficient (Scott & Holt 1982, JASA 77:848–854), the design factor is approximately 1 + (m−1)ρxρy, with ρx the within-cluster correlation of the covariate and ρy the residual correlation of the outcome; var_c(β̂) = var_I(β̂)·DF. Simulated design effects (1.69, 1.61, 1.91) were close to the approximation (1.72, 1.72, 2.01). Secondary source (seminar slides); original not fetched. — [McMaster seminar slides](https://math.mcmaster.ca/canty/seminars/0102/april3sem.pdf); [Wikipedia: Design effect](https://en.wikipedia.org/wiki/Design_effect) (notes that the DEFF for a regression coefficient differs from that for a mean)
- Harrell: effective sample size for a binary response m = 3nq(1−q) (≈ 3·min(events, non-events) when unbalanced); p < m/15; p counts "all variables screened for association with response, including interactions"; the rule ignores the sample size needed for the intercept. RMS ch. 4 does not discuss clustered data. — [Harrell, RMS ch. 4, §4.4](https://hbiostat.org/rmsc/multivar)
- Prior project analysis (not external): an effect on 2 of 9 segments carries 0.042 of the segment-model information in a person-level "any plaque" model vs 0.672 for an all-segment effect; 93.8% of the segment model's information on a 2-segment feature comes from allocation. — [on-disk, `reports/Pooled segment GLMM background.md`, cited in `reports/Segment specific geometry weights.md`]

### Inferences
- [inference] Person-constant covariates (SCORE2 or its factors, log follow-up, dominance, LM angle, LM→LAD and LM→LCx ratios): ρx = 1, so DF ≈ 1 + (m−1)ρy, the full cluster penalty. Their information is essentially person-level; they should be counted against the person-level budget (~15 at C = 0.70). Note the LM features entered only on pLAD/pLCx (or LAD/LCx) rows vary within person (0 on other rows), but the *value* is still a single person-level number, so person-level counting is appropriate.
- [inference] Segment-varying covariates with a shared slope (curvature, taper z-scored within segment type): if their between-segment-within-person correlation ρx is low, DF ≈ 1 and information comes from all ~1,100 segment events. In the conditional GLMM (random intercept), the slope is identified from both within-person contrasts (which segments get plaque) and between-person differences (who has more plaque). Only the between-person part answers "who". A Mundlak split (person mean vs within-person deviation) would make this explicit at +1 df per feature.
- [inference] Segment dummies (8 df): if every person contributes all 9 segments, Σ_j exp(α_j + x_iβ) = exp(x_iβ)·Σ_j exp(α_j) for person-level x, so the dummies collapse into one person-level intercept in the aggregated risk. They are identified purely from where events occur (segment-level allocation) and cost segment-level, not person-level, information. Log length behaves similarly (mostly within-person). With missing/unevaluable segments or segment-varying covariates the cancellation is only approximate.
- [inference] Practical rule for the thesis: report two counts. (a) Person-level df = person-constant base terms + person-level geometry + the between-person part of segment-varying geometry (conservatively count each shared-slope segment feature as 1 df here too). Compare with Riley person-level P_max (8–24 by C). (b) Segment-level df = all fixed effects incl. dummies and log length; compare with a clustering-discounted segment budget, e.g. Riley/Harrell on n_eff = n_seg/(1+(m−1)ρ) with m = 9. With latent-scale ICC ρ = σ²/(σ² + π²/6) for cloglog (π²/6 ≈ 1.645) — e.g. σ² = 1 → ρ ≈ 0.38, DEFF ≈ 4.0, n_eff ≈ 2,400 rows; σ² = 0.5 → ρ ≈ 0.23, DEFF ≈ 2.8. These numbers are illustrative only; the latent-scale ICC formula is standard for logit (π²/3) and its cloglog analogue (π²/6) is an inference, and Kish's DEFF is the conservative, person-constant-covariate case.
- [inference] The current 5-df geometry block (2 segment-varying + 3 person-level) plus a recalibrated SCORE2 base (≈ 2 person-level df incl. log follow-up, + dominance 1) ≈ 8 person-level df: inside the C = 0.70 budget. With refitted SCORE2 factors (≈ 6–7 df) the person-level count is ≈ 12–13, inside at C = 0.70 but over at C = 0.65.

### Gaps
- No source found that gives a formal level-specific budget for multilevel *prediction* models, or a design-effect adjustment to Riley's criteria.
- The Scott–Holt formula is for linear regression / survey estimation with a working-independence estimator; its applicability to a conditional cloglog GLMM was not verified. The original 1982 paper was not fetched.
- The actual ρy (random-intercept variance) and ρx (within-person correlation of curvature/taper) are unknown before fitting; they can be estimated from geometry alone (ρx) without outcome data.

## Q3. Do non-selected candidate parameters, segment dummies and the random-effect variance count?

### Takeaway
Candidate parameters count whether or not they are kept (Riley, Harrell, Wynants: variable selection raises the need). Nothing found addresses segment dummies or random-effect variances explicitly; by the derivation in Q2, dummies cost segment-level rather than person-level information, and the single variance parameter is plausibly one person-level df.

### Cited Findings
- pmsampsize: `parameters` = candidate predictor parameters "for potential inclusion"; may exceed number of predictors (nonlinear terms, categories). — [pmsampsize manual](https://cran.r-project.org/web/packages/pmsampsize/refman/pmsampsize.html)
- Riley BMJ 2020: overfitting "is dictated by the total number of predictor parameters considered, not just those included in the final model equation". — [BMJ 2020 record](https://dspace.library.uu.nl/handle/1874/457642)
- Harrell: p = candidate parameters in a stepwise analysis; "includes all variables screened for association with response, including interactions"; univariable screening "in no way reduces multiple comparison problems". — [RMS ch. 4](https://hbiostat.org/rmsc/multivar)
- Wynants 2015: with backward selection, up to 50 EPV may be needed; selection gave up to 118% relative bias in predictor effects at EPV 5. — [EUR repository](https://repub.eur.nl/pub/91572)

### Inferences
- [inference] Both SCORE2 bases count if the base is chosen by comparing them in the outcome data (the open "recalibrated vs refitted" decision): the comparison is a selection step, so the conservative count is the larger base (≈ 6–7 df) even if the 1-df recalibrated base is kept. Choosing the base on non-outcome grounds (or by prespecified rule) avoids this.
- [inference] Any secondary blocks (e.g. the +4 df curvature/taper × artery heterogeneity test in the segment-weights report) do not count against the primary model's budget if they are never used to choose the primary model, but they do need their own budget if they are reported as predictive models.
- [inference] The random-intercept variance enters the person risk through E_b[·] and is identified from the over-dispersion of per-person segment-event counts, a person-level quantity. Counting it as 1 person-level df is conservative and cheap; Riley does not count the intercept and no source covers variance components.

### Gaps
- No source on counting fixed effects for cluster-level "position" indicators or variance components in prediction sample size.

## Q4. Is the 42% event fraction handled correctly, and does the cloglog link change anything?

### Takeaway
Riley handles any event fraction through max R²_CS and the intercept-precision criterion; at φ = 0.42 the effective sample size is near its maximum, and criterion 1 (shrinkage) binds. The cloglog link is not covered by the papers, but the shrinkage criterion rests on a likelihood-ratio heuristic that is link-agnostic; the C→R² conversion assumes a logistic model.

### Cited Findings
- van Smeden M, Moons KGM, de Groot JAH, Collins GS, Altman DG, Eijkemans MJC, Reitsma JB. Sample size for binary logistic prediction models: beyond events per variable criteria. Stat Methods Med Res 2019;28(8):2455–2474, doi:10.1177/0962280218784726: out-of-sample performance is better approximated by number of predictors, total sample size and events fraction than by EPV. — [Utrecht record](https://researchinformation.umcutrecht.nl/en/publications/sample-size-for-binary-logistic-prediction-models-beyond-events-p/); [full text PDF](https://dspace.library.uu.nl/bitstream/1874/387109/1/vansmeden.pdf) (not fetched)
- Harrell's effective n for binary outcomes 3nq(1−q) is maximised (0.75n) at q = 0.5. — [RMS ch. 4](https://hbiostat.org/rmsc/multivar)
- Pavlou 2024: calibration worsens as prevalence increases at high C; at C = 0.85 the needed EPV was 19.4 at prevalence 0.5 vs 10.2 from the Riley formula, and 8 vs 5.3 at prevalence 0.1. Prevalences tested: 10%, 30%, 50%. — [PMC11234534](https://pmc.ncbi.nlm.nih.gov/articles/PMC11234534/)

### Inferences
- [own calc] At φ = 0.42, EPV language is misleading: the limiting class is events (452) vs non-events (624) — 452/15 ≈ 30 EPP at Riley's P_max of 15. Riley's number is driven by the low anticipated R²_CS, not by the event count.
- [inference] With 42% events in 10 years, the cloglog and logit links differ more than in rare-event settings (they converge only for small risks). The heuristic shrinkage factor (van Houwelingen/le Cessie: S ≈ 1 − p/LR χ²) holds for any GLM fitted by ML, so criterion 1 transfers to cloglog if expressed in LR χ² / R²_CS terms; the C-to-R² mapping (logistic, normal LP) is an approximation for a cloglog model. Pavlou's finding that the CS formula is adequate for C < 0.8 supports using it here (anticipated C ≈ 0.65–0.75).
- [inference] For the pooled model the relevant prevalence is the person-level 42%, but the model is fitted to segment rows with ~11% events; the person-level aggregated risk is a nonlinear function of segment predictions, so the Riley criteria apply only loosely to it.

### Gaps
- No source on sample size for cloglog or discrete-time hazard prediction models specifically; pmsampsize's survival option (Cox/R²) is an alternative framing not evaluated here.

## Q5. Simulation-based sample-size approaches and how to implement them for a GLMM

### Takeaway
Pavlou et al. 2024 (samplesizedev) shows the Riley shrinkage formula is adequate for C < 0.8 but that the realised calibration slope is highly variable, especially with < 10 predictors; their simulation targets expected CS = 0.9. No packaged tool supports GLMMs or aggregated person risk, so a bespoke simulation of the actual model is the only route that answers the question directly.

### Cited Findings
- Pavlou M, Ambler G, Qu C, Seaman SR, White IR. An evaluation of sample size requirements for developing risk prediction models with binary outcomes. BMC Med Res Methodol 2024;24:146, doi:10.1186/s12874-024-02268-5. Both the CS formula (Riley criterion 1) and the MAPE formula perform adequately for C < 0.8 at any prevalence; for C = 0.85/0.90 n must rise by ≥ 50%/100% to meet the target CS. Target expected CS 0.9; MAPE ≤ 0.05. With the formula-based n, P(CS < 0.8) ranges ~0.1 (low strength) to 0.6 (high); with simulation-based n it is ~0.12. Variability is much higher with < 10 predictors ("care should be taken when the number of predictor variables is small"). Assumes normal independent predictors, ML logistic regression; no clustered data. — [PMC11234534](https://pmc.ncbi.nlm.nih.gov/articles/PMC11234534/)
- Pavlou M et al. 2021: sample size for external validation of binary-outcome models (C, CS, calibration-in-the-large), R package `sampsizeval`. — [PMC8529102](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8529102/)
- pmsims (2026 preprint): model-agnostic, simulation + Gaussian-process learning curves + assurance (probability of reaching target); hierarchical data listed as future work. — [arXiv 2602.23507](https://arxiv.org/abs/2602.23507)

### Inferences
- [inference] A GLMM-specific simulation for the thesis, using only non-outcome information plus assumed effect sizes:
  1. Take the real covariate matrix (person-level SCORE2/factors, dominance, LM features; segment-level curvature, taper, length, segment type, z-scored per type) — no outcomes needed, so it can be done before the outcome is seen.
  2. Fix a data-generating cloglog GLMM: segment baseline hazards α_j calibrated to plausible segment event shares (from aggregate published/plausible proportions), σ² of the random intercept chosen so that person prevalence ≈ 0.42 and the per-person count over-dispersion is plausible (grid σ² ∈ {0.25, 0.5, 1}), SCORE2 effect giving base C ≈ 0.65–0.70, geometry effects at a few anticipated HR/SD (incl. null).
  3. For each of R ≈ 500 replicates draw outcomes, fit the exact analysis model (same Gauss–Hermite code as `progression_who_pooled.py`), and evaluate the aggregated person risk on a large independent simulated population: calibration slope of logit/cloglog(P_i), calibration-in-the-large, ΔC, and the LR-test power for the geometry block.
  4. Report mean CS and P(CS < 0.8 or < 0.9) for each candidate model size (e.g. 5-df vs 9-df geometry; recalibrated vs refitted base). Pass criterion: E[CS] ≥ 0.9 (Riley/Pavlou target) and, following Pavlou/pmsims, a high probability of CS ≥ 0.8.
  This uses the real n and cluster structure and directly answers whether the parameter count is supportable; it also yields the power numbers. Computational cost ≈ R × (#scenarios) GLMM fits.
- [inference] Riley's criterion 3 analogue at person level (precision of the mean aggregated risk) is easy to check analytically and is clearly met (half-width 0.029).

### Gaps
- No published simulation of sample size for GLMM-based or cluster-aggregated prediction models was found.
- samplesizedev's internal algorithm (Supplementary Material 1) was not read.

## Q6. Can penalisation (ridge) support more parameters?

### Takeaway
No: Riley et al. 2021 and companion work say shrinkage/penalisation is not a remedy for small effective samples; it is least reliable exactly when overfitting is large, and should be applied on top of an adequate sample size.

### Cited Findings
- Riley RD, Snell KIE, Martin GP, Whittle R, Archer L, Sperrin M, Collins GS. Penalization and shrinkage methods produced unreliable clinical prediction models especially when sample size was small. J Clin Epidemiol 2021;132:88–96, doi:10.1016/j.jclinepi.2020.12.005. Simulation: N = 100–1,000, 50% events, 20 predictors (5 true), 500 datasets; ridge, lasso, elastic net (5-fold CV), heuristic and bootstrap uniform shrinkage. Tuning parameters more uncertain at small n; at smallest n, calibration slopes ranged roughly 0 to 5; at large n ~0.8–1.2. Applied example: bootstrap shrinkage S = 0.94 (0.77–1.18) at n = 262 vs 0.78 (0.43–1.21) at n = 50. Quotes: "Penalization methods are not a 'carte blanche'; they do not guarantee a reliable prediction model is developed." "They are more unreliable when needed most (i.e., when overfitting may be large)." "We recommend they are best applied with large effective sample sizes", identified by formal sample-size calculations targeting S ≥ 0.9. — [PMC8026952](https://pmc.ncbi.nlm.nih.gov/articles/PMC8026952/)
- Follow-up (Martin GP, Riley RD, Collins GS, Sperrin M. Stat Methods Med Res 2021;30(12):2545–2561, doi:10.1177/09622802211046388): variability in tuning parameters and predictive performance should be examined; penalisation used alongside minimum sample size, not instead. — [SAGE](https://journals.sagepub.com/doi/reader/10.1177/09622802211046388) (summarised from search snippet; not fetched)
- Harrell recommends data reduction "or use penalized estimation" but does not tie penalisation to a higher p:m ratio; advises against penalising the variable of interest when estimating its effect. — [RMS ch. 4](https://hbiostat.org/rmsc/multivar)

### Inferences
- [inference] For this thesis the primary analysis is an LR test of a prespecified block, which requires unpenalised ML; ridge would break the χ² reference. Ridge is therefore only relevant for descriptive/secondary estimates (e.g. shrunken per-segment slopes) and cannot be used to justify a larger confirmatory block.
- [inference] Uniform post-hoc shrinkage of the fitted geometry block (bootstrap S) is still worth reporting as an overfitting diagnostic; Riley 2021's own applied example shows its CI is wide at moderate n.

### Gaps
- No study of penalised GLMMs (e.g. glmmLasso, ridge on fixed effects in GLMMs) in prediction sample-size terms was found.
