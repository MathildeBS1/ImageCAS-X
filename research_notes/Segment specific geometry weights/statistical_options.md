# Statistical options for letting segment-level geometry effects differ across segment types

Setting: segment-level cloglog GLMM, person random intercept, 9 trunk segments (LAD/LCx/RCA × prox/mid/distal), ~1,077 people, ~452 with an event, ~1,100 segment events (estimate). One prespecified LR test of the geometry block (curvature, taper segment-level; LM angle + 2 LM diameter ratios person-level). Person-level Riley budget ~15 df. Options (a) shared β, (b) feature × artery or × position (+2 df/feature), (c) feature × segment (+8 df/feature), (d) random slopes by segment type, (e) ridge/lasso interactions, (f) Bayesian hierarchical shrinkage, (g) Mundlak within/between.

Labels: **[derivation]** = own algebra, not quoted; **[own calc]** = own noncentral-χ² computation (scipy), no data; **[on-disk]** = project report already in the repo, not an external source. Several sources below were seen only as abstracts/search snippets; this is flagged per item.

## Q1. What do prediction-model guidelines say about interactions (prespecification, df spending, heterogeneity tests)?

### Takeaway
The guidelines agree: interactions must be prespecified on subject-matter grounds, every candidate interaction df counts against the sample-size budget, they are tested jointly ("keep all or delete all"), and when included they should be penalised; data-driven interaction screening is discouraged. None of the sources gives a rule that says segment-specific slopes *should* be added; the default for prediction is the simpler additive model.

### Cited Findings
- Harrell RMS ch. 4 (§4.12.1 item 2): the modelling strategy is to "specify relevant candidate predictors and possible interactions" in advance, and "Don't use Y to decide which X's to include." — [Harrell, RMS ch. 4](https://hbiostat.org/rmsc/multivar)
- Harrell §4.4: the limiting-sample-size rule p < m/15 counts in p "*all* variables screened for association with response, including interactions." — [Harrell, RMS ch. 4](https://hbiostat.org/rmsc/multivar)
- Harrell §4.12.1 item 10: "Check additivity assumptions by testing pre-specified interaction terms. Use a global test and either keep all or delete all interactions." — [Harrell, RMS ch. 4](https://hbiostat.org/rmsc/multivar)
- Harrell §4.12.2 item 2 (effect estimation): "Careful consideration of interactions; inclusion forces estimates to be conditional and raises variances." Item 5: "Don't penalize terms for variable of interest." — [Harrell, RMS ch. 4](https://hbiostat.org/rmsc/multivar)
- Harrell §4.5 cites Spiegelhalter (1986): better prediction usually comes from fitting all candidate variables with shrinkage rather than selection; penalised MLE is listed as the tool. — [Harrell, RMS ch. 4](https://hbiostat.org/rmsc/multivar)
- Harrell §4.7.7 worked example: restricting an interaction to be linear (e.g. "3+1+1 d.f." for a spline × sex) is the standard way to cap df of an interaction with a flexible term. — [Harrell, RMS ch. 4](https://hbiostat.org/rmsc/multivar)
- Riley et al. 2020 sample-size criteria (BMJ 368:m441, doi:10.1136/bmj.m441): target expected shrinkage ≥ 0.9, optimism in Nagelkerke R² ≤ 0.05, precise overall risk; the `parameters` input is "the number of candidate predictor parameters", which "may be larger than the number of candidate predictors". Interactions are not mentioned explicitly in the manual text found, but they are candidate parameters in the same sense. — [pmsampsize manual (CRAN)](https://cran.r-project.org/web/packages/pmsampsize/refman/pmsampsize.html)
- A Steyerberg-group thesis chapter: "If 6 variables are entered in the model, already 15 first order interaction terms are possible. Therefore, a conservative attitude towards testing of interaction terms has been proposed." (seen as search snippet) — [Erasmus repository](https://repub.eur.nl/pub/1169/01.pdf)
- van Klaveren, Balan, Steyerberg & Kent 2019 (J Clin Epidemiol 114:72–83, doi:10.1016/j.jclinepi.2019.05.029): models with all treatment × covariate interactions overestimated heterogeneity and were overfit "even with doubled sample sizes"; penalised regression reduced miscalibration considerably; a constant-effect model was best when there were no true interactions, penalised effect models best when there were. Recommendation: include only plausible interactions and fit them with penalisation. (abstract/highlights only) — [PMC7497896](https://pmc.ncbi.nlm.nih.gov/articles/PMC7497896)
- Kontopantelis, Sperrin, Mamas & Buchan 2018 (J Clin Epidemiol 93:79–83): heterogeneity should be investigated with interaction terms within one model rather than separate subgroup models. (abstract only) — [PubMed 28943379](https://pubmed.ncbi.nlm.nih.gov/28943379/); [Liverpool record](https://livrepository.liverpool.ac.uk/id/eprint/3149481)
- Brookes et al. 2004 (J Clin Epidemiol 57:229–236): formal interaction tests beat subgroup-specific tests; subgroup analyses should be restricted to those proposed before data collection. — [Bristol record](https://research-information.bris.ac.uk/en/publications/subgroup-analyses-in-randomized-trials-risks-of-subgroup-specific/); [Glasgow eprints](https://eprints.gla.ac.uk/87531)
- BMJ Statistics Note (Altman & Matthews 1996, "Interaction 1: heterogeneity of effects"): exploring many subgroups "is almost certain to throw up some spurious significant interactions." (snippet) — [BMJ 313:486](https://www.bmj.com/content/313/7055/486)
- On-disk project report already recommends grouped segment classes, not all levels, for geometry interactions, and a linear-by-group interaction (`%ia%`-style, 2 df per feature for 3 groups) as the cheapest heterogeneity check; full RCS4 × 10-level interaction "would not fit". — [on-disk] `~/Desktop/Speciale/CGPS_statistics-/reports/Segment plaque risk model nonlinearity.md`

### Inferences
- Applying Harrell's "global test, keep all or delete all" to this thesis: a heterogeneity test, if done, should be one prespecified joint LR test of all geometry × segment-group terms, reported as a finding and *not* used to choose the model that carries the confirmatory test (same logic as Harrell's rule against testing linearity and then re-testing association) [derivation].
- The confirmatory LR test and the predictive model can be separated: the confirmatory test uses the prespecified (shared-β) block; a heterogeneity model, if any, is a secondary/estimation analysis. This mirrors the "risk model vs effect model" split of van Klaveren et al. [derivation].
- Budget arithmetic [derivation]: shared β uses 5 geometry df. Option (b) for curvature and taper by artery adds 4 → 9; by artery and position (structured, Q4) adds 8 → 13; option (c) adds 16 → 21. Against a person-level budget of ~15 with ~11 df already used by SCORE2 + log follow-up + LM terms (per the brief: 7 + 1 + 3), only (a) fits the person-level budget cleanly; (b) is borderline. The segment-level budget is larger (on-disk report estimates 35–60 df for ≥mild), so the binding constraint depends on which level one argues the Riley criterion applies to — curvature/taper slopes by segment type are identified mainly from within-person allocation, so the segment-level budget is arguably the relevant one for them, but the person-level budget for any person-risk claim.

### Gaps
- Steyerberg's *Clinical Prediction Models* (2nd ed. 2019) text on interactions was not opened; no direct quote available.
- No source found that addresses interaction df spending in a *clustered* prediction model (Riley criteria have no clustered extension; TRIPOD-Cluster was not opened for this).
- TRIPOD/TRIPOD+AI items on interactions were not checked.

## Q2. Power: truly common effect spread over k df vs a 1-df test; power when effects truly differ

### Takeaway
Spreading a truly common effect over more df costs substantial power (own calc: 80% at 1 df falls to ~65% at 3 df and ~45% at 9 df for the same noncentrality); but if the effect is concentrated in some segment types or differs in sign, the shared 1-df test loses the projection and the multi-df test can win. Tests of the heterogeneity itself (the interaction) are much weaker than main-effect tests (4×–16× sample size heuristics).

### Cited Findings
- Gelman: "You need 16 times the sample size to estimate an interaction than to estimate a main effect" under his setup (interaction half the size of the main effect *and* SE of interaction twice the main-effect SE → effect/SE ratio 4× smaller → 4² = 16). If subgroup effects are 0.3 and 0.9 rather than 0.45 and 0.75, the factor is ~4. — [Gelman 2018](https://statmodeling.stat.columbia.edu/2018/03/15/need16/); [Gelman 2023 explanation](https://statmodeling.stat.columbia.edu/2023/11/09/you-need-16-times-the-sample-size-to-estimate-an-interaction-than-to-estimate-a-main-effect-explained/)
- Brookes et al. 2004: interaction tests reached the power of the overall comparison only when the interaction was at least twice the overall effect; power dropped considerably for smaller (more realistic) interactions. (abstract-level) — [Glasgow eprints](https://eprints.gla.ac.uk/87531); [NCCHTA brief](https://www.inahta.org/upload/Briefs_3/02-96%20NCCHTA%20-%20Subgroup%20Analyses%20in%20RCT.pdf)
- Harrell: a 2-df spline test is nearly optimal even when the truth is linear, and the right practice is to keep prespecified flexibility rather than test-then-simplify (as summarised in the on-disk report citing RMS ch. 2). — [Harrell, RMS ch. 2](https://hbiostat.org/rmsc/genreg)

### Inferences
- Formula [derivation]: with local information I_j for the slope in segment type j (approximately independent), and true slopes β_j, the noncentrality of the 1-df shared-slope LR test ≈ (Σ_j I_j β_j)² / Σ_j I_j; the k-df test of all β_j = 0 has noncentrality ≈ Σ_j I_j β_j². By Cauchy–Schwarz the k-df NCP is always ≥ the 1-df NCP; the ratio is the squared cosine between β and the constant vector (information-weighted). The k-df test pays for this with a larger critical value.
- Common effect, same NCP λ, power at α = 0.05 [own calc]:

  | λ | 1 df | 2 df | 3 df | 5 df | 9 df |
  |---|---|---|---|---|---|
  | 5.0 | 0.61 | 0.50 | 0.44 | 0.36 | 0.28 |
  | 7.85 | 0.80 | 0.71 | 0.65 | 0.56 | 0.45 |
  | 10.5 | 0.90 | 0.84 | 0.78 | 0.70 | 0.59 |

- Applied to the geometry block [own calc]: if the 5-df shared block has NCP 7.85 (power 0.56) and the added artery interactions carry no signal, a 9-df block with the same NCP has power 0.45; at NCP 10.5, 0.70 → 0.59.
- Effect present in only one of three equally informative artery groups, Iβ² = 10.5 [own calc]: shared 1-df NCP = 3.5 → power 0.47; 3-df artery-specific test NCP = 10.5 → power 0.78. With opposite-sign effects (e.g. curvature protective in one artery, harmful in another, which the on-disk nonlinearity report notes is mechanistically possible), the shared NCP can approach 0 while the k-df test retains power [derivation].
- Hence the choice is a bet on the prior shape of heterogeneity; it must be made before seeing outcomes. Given that the published geometry–plaque evidence gives no segment-specific effect sizes (on-disk reports), a shared slope is the default bet; artery-grouped (3-level) is the only heterogeneity coding with a mechanistic rationale cheap enough to consider [derivation].

### Gaps
- No simulation literature was found specifically on power of shared vs segment-specific slopes in clustered binary/cloglog models; the numbers above are generic noncentral-χ² approximations, assuming independent per-type information and ignoring correlation from the random intercept.
- Brookes et al.'s exact sample-size inflation factor was not retrieved (the commonly quoted "4×" was not confirmed in the sources seen).

## Q3. Random slopes over a grouping factor with 9 (or 3) levels: is the variance estimable?

### Takeaway
With 9 levels a random-slope variance is weakly identified; with 3 it is essentially not identified by likelihood alone and will often give singular (zero) fits. Rules of thumb range from ≥5–6 to ≥10 levels. Bayesian fitting with a weakly informative half-t/half-Cauchy prior on the slope SD makes it estimable but prior-sensitive. Segment type as fixed effect plus a random slope by type is valid in form, but with 9 types this is better viewed as shrinkage (option f) than as variance estimation.

### Cited Findings
- Bolker GLMM FAQ: "there must be a reasonable number of random-effects levels (e.g. blocks) – more than 5 or 6 at a minimum"; Onkelinx: "in case n_s < 10 it is safer to use the variable as a fixed effect", >20 levels for experiments, cautious validation for 10–20; with few levels "in the worst case it will lead to various numerical difficulties such as lack of convergence, zero variance estimates". — [Bolker, GLMM FAQ](https://bbolker.github.io/mixedmodels-misc/glmmFAQ.html)
- Oberpriller, Leite & Pichler 2022 (Ecol Evol 12:e9062): simulations with 2–8 levels; for random-intercept models the fixed-vs-random choice did not affect type I error or power of the population slope; when an effect differs among groups, a random slope + intercept model, "switching to a fixed-effect model only in case of a singular fit, avoids overconfidence"; they suggest starting with the mixed model regardless of number of levels. — [PMC9309037](https://pmc.ncbi.nlm.nih.gov/articles/PMC9309037); [bioRxiv](https://www.biorxiv.org/content/10.1101/2021.05.03.442487.full.pdf)
- Snijders & Bosker suggest not using multilevel models with fewer than ~10 clusters (as quoted in Austin 2010). — [PMC2949382](https://pmc.ncbi.nlm.nih.gov/articles/PMC2949382)
- McNeish & Stapleton 2016 ("Modeling clustered data with very few clusters", Multivariate Behav Res 51:495–518; and Educ Psychol Rev 28:295–314) — reviewed small-cluster methods; a secondary source says some methods worked with as few as four clusters. Full text not seen. — [ASU profile](https://isearch.asu.edu/profile/3146016); [UMD dissertation record](https://drum.lib.umd.edu/items/8358c2b6-8f5b-43b5-8ac7-c1908e166de4/full)
- Gelman 2006 (Bayesian Analysis 1:515–533) proposes half-t / half-Cauchy priors for hierarchical SDs (density non-zero at 0, unlike inverse-gamma); Polson & Scott 2012 argue half-Cauchy as default for top-level scale parameters. — [Gelman 2006, Project Euclid](https://projecteuclid.org/euclid.ba/1354024466); [Polson & Scott, arXiv 1104.4937](https://arxiv.org/pdf/1104.4937)
- A blog source claims that with fewer than ~5 groups the prior dominates the group-level SD (unverified rule of thumb, not peer-reviewed). — [MetricGate blog](https://metricgate.com/blogs/setting-variance-priors-hierarchical-model/)

### Inferences
- [derivation] A random slope by segment type, `(0 + curv | segtype)`, has its variance identified from 9 (or 3) slope "observations"; even with perfect per-type estimates, a variance from 9 values has ~8 df (relative SE of the SD ≈ 1/√16 ≈ 25% only in the ideal Gaussian case), and from 3 values ~2 df. With noisy per-type slopes, the ML variance is often 0 (singular fit), which collapses to option (a) automatically — that is not a failure but it means option (d) by ML is data-adaptively choosing between (a) and (c), i.e. a hidden model selection.
- [derivation] Random slopes do not change the df of the confirmatory fixed-effect test (the mean slope keeps 1 df) but add a variance parameter, and the LR test of the mean slope in the presence of an estimated slope variance has a less settled reference distribution in small-level settings. A boundary LR test of the slope variance itself is χ²₀:χ²₁ mixture (Self & Liang, cited in on-disk background report).
- [derivation] Crossed structure: in this model the person random intercept and segment-type slopes are crossed (segment type is not nested in person). In lme4/glmmTMB this means two random-effect terms and Laplace approximation (adaptive GHQ in `glmer` needs a single scalar random effect, per on-disk report), so the integration rule of the confirmatory model would change.
- Segment type as fixed intercepts plus random slope by type is the standard "fixed for intercepts, random for slopes" form and is legitimate; the problem is solely the number of levels.

### Gaps
- No source found specifically on random-slope variance estimability with ~9 levels in binary GLMMs with large per-level information (here each segment type has ~1,000 people), which differs from the usual few-clusters-few-units setting; Oberpriller et al. is the closest (Gaussian/binomial ecology simulations, 2–8 levels).
- McNeish & Stapleton full text not read.

## Q4. Penalised interactions, hierarchical shrinkage, and structured (artery + position) interactions

### Takeaway
Shrinking segment-specific slopes toward a common slope (Dixon–Simon exchangeable interactions; Bayesian hierarchical subgroup models; ridge on interaction terms only) is the recommended way to *estimate* heterogeneity in prediction, but it does not give a clean prespecified LR test with known df. A structured artery + position decomposition (2 + 2 df instead of 8) is a natural low-rank parameterisation; it is an own derivation here, no source found for it in this context.

### Cited Findings
- Dixon & Simon 1991 (Biometrics 47:871–881): Bayesian subset analysis with treatment × covariate interactions assumed exchangeable, which shrinks interaction posteriors toward zero; most meaningful when subsets have no a priori ranking; applicable to proportional-hazards estimates; implemented in R `DSBayes` and `beanz`. (abstract/package docs) — [beanz docs](https://search.r-project.org/CRAN/refmans/beanz/html/beanz-package.html); [DSBayes](https://packages.oit.ncsu.edu/cran/web/packages/DSBayes/refman/DSBayes.html)
- Jones, Ohlssen, Neuenschwander, Racine & Branson 2011 (Clin Trials 8:129–143, doi:10.1177/1740774510396933): reviews Bayesian hierarchical models for subgroup effects, proposing shrinkage estimation as an alternative to hypothesis testing in exploratory subgroup analysis. A 2024 paper notes these models only shrink across disjoint (non-overlapping) subgroups. (abstract) — [PubMed via QxMD](https://read.qxmd.com/read/21282293/bayesian-models-for-subgroup-analysis-in-clinical-trials); [arXiv 2407.11729](https://arxiv.org/html/2407.11729v1)
- EMA-presented work (Bornkamp et al.) on Bayesian shrinkage for routine estimation of subgroup effects. — [EMA presentation](https://www.ema.europa.eu/en/documents/presentation/presentation-bayesian-shrinkage-methods-routine-estimation-subgroup-treatment-effects-bbornkamp-novartis-nbest-dbratton-gsk-mjelizarow-ucb-nmuhlemann-cytel-jmcmurray-university-glasgow_en.pdf)
- van Klaveren et al. 2019: penalised effect models were optimal when true interactions existed; unpenalised interaction models overestimated heterogeneity. — [PMC7497896](https://pmc.ncbi.nlm.nih.gov/articles/PMC7497896)
- Harrell: "Don't penalize terms for variable of interest" in effect estimation; penalisation is primarily for prediction. — [Harrell, RMS ch. 4](https://hbiostat.org/rmsc/multivar)

### Inferences
- [derivation] Structured interaction: β_j = β + α_artery(j) + γ_position(j) with sum-to-zero constraints gives 1 + 2 + 2 df per feature instead of 1 + 8, assuming no artery × position interaction in the slope. Testing the 4 heterogeneity df jointly is the "additive heterogeneity" test. This is the same idea as additive main effects in a two-way table applied to slopes.
- [derivation] Partial-pooling equivalence: a random slope by segment type (option d) fitted by REML/Bayes, a ridge penalty on deviations β_j − β̄ (option e), and a normal hierarchical prior (option f) are the same model family; ridge with a fixed λ = 1/τ² is option (d) with τ fixed instead of estimated. Lasso/fused lasso instead push deviations exactly to zero (selection), which re-introduces data-driven model choice.
- [derivation] For the confirmatory test, a sensible prespecified design is: confirmatory LR test on the shared-β block (unpenalised, as Harrell advises for the variable of interest); a secondary analysis estimating artery-specific slopes with shrinkage (hierarchical prior with half-normal/half-Cauchy SD, or the 2-df artery deviation with ridge), reported as estimates with intervals, not as a test.
- [derivation] Penalised or Bayesian models complicate the "one LR test" plan: penalised likelihood has no standard χ² reference (effective df instead of df), and Bayesian fits give posterior quantities, not an LR p-value.

### Gaps
- No source found applying structured (row + column) slope decompositions to anatomical segment grids, or any coronary paper with segment-specific geometry coefficients.
- Jones et al. 2011 and Dixon & Simon 1991 full texts not opened; specifics on how many subgroups are needed for the shrinkage variance are not confirmed.

## Q5. Does per-type standardisation change the meaning of a shared coefficient?

### Takeaway
Yes [derivation, no source found]: with z_ij = (x_ij − m_j)/s_j and one shared β, the raw-unit log-HR in segment type j is β/s_j, so a shared z-coefficient already imposes type-specific raw-unit effects proportional to 1/s_j (and removes between-type mean differences from the slope). This is itself a structural assumption, "equal effect per within-type SD", and should be stated as such.

### Cited Findings
- The on-disk nonlinearity report recommends standardising by segment type before the Mundlak split so that the person mean does not encode which segments a person has (e.g. mid RCA naturally more curved). — [on-disk] `~/Desktop/Speciale/CGPS_statistics-/reports/Segment plaque risk model nonlinearity.md`
- The on-disk background report found (own sim) that a Wald test of β_W = β_B comparing coefficients on different scales falsely rejected in 27.5% vs 5% — scale choice changes the meaning of equality tests. — [on-disk] `reports/Pooled segment GLMM background.md`

### Inferences
- [derivation] Shared β on z-scores ⇔ raw slopes β_j = β/s_j. Shared β on raw x ⇔ equal raw-unit slopes across types. These are two different 1-df hypotheses; the alternative parameterisations differ only in which direction the 1-df test points, and neither is "no heterogeneity" in the other's scale. Under H0 (all β_j = 0) both tests are valid; they differ in power depending on whether the truth is closer to "equal per SD" or "equal per unit".
- [derivation] Mean-centring by type (subtracting m_j) also removes between-type differences in average curvature from the slope; those are absorbed by the segment-type intercepts anyway, so this changes nothing when type intercepts are in the model, but the scaling by s_j does.
- [derivation] If s_j differs a lot across types (e.g. distal segments much more variable in curvature), the z-scaling up-weights types with small SD in raw units. A check: report the raw-unit implied slopes β/s_j alongside.
- [derivation] Per-type z-scaling must use training-fold m_j, s_j only under person-split CV.

### Gaps
- No literature found that discusses "standardise within subgroup then fit a common slope" as an implicit interaction; this is presented as own derivation.

## Q6. Cloglog/PH framing: is "same HR across segment types" analogous to proportional hazards across strata, and how is it checked?

### Takeaway
Yes, in the sense that matters: segment-type intercepts are like stratum-specific baseline hazards (stratified Cox), and a shared slope is the stratified-Cox assumption that covariate effects are identical across strata; the standard check is an LR (or Wald) test of covariate × stratum interaction terms. This is different from the usual time-PH check (Schoenfeld residuals), which is not available with one follow-up scan.

### Cited Findings
- In a stratified Cox model, stratification gives each stratum its own baseline hazard but forces covariate effects to be identical; whether coefficients vary across strata is tested with an LR test comparing interaction and no-interaction models. — [MWSUG 2019 paper](https://mwsug.org/proceedings/2019/RF/MWSUG-2019-RF-100.pdf); [Breheny lecture notes, Iowa](https://myweb.uiowa.edu/pbreheny/7210/f19/notes/11-19.pdf); [R-help thread on strata × covariate tests](https://stat.ethz.ch/pipermail/r-help/2005-October/080242.html)
- Grouped-data PH (Prentice & Gloeckler 1978) gives the cloglog link, β as log HR (summarised in on-disk background report with sources). — [SAS PROC LOGISTIC](https://support.sas.com/documentation/cdl/en/statug/63962/HTML/default/statug_logistic_sect072.htm)
- Therneau & Grambsch (2000, p. 142) recommend PH tests per stratum when Schoenfeld variance differs across strata (secondary source; book not opened). — summarised in search results; book not verified.

### Inferences
- [derivation] With one follow-up scan (current-status data), the time-PH assumption cannot be checked from Schoenfeld residuals; only the "across strata" homogeneity (covariate × segment type) is checkable, and it is exactly option (b)/(c) as a test. So the interaction test is the cloglog analogue of checking that a covariate's HR does not differ by stratum.
- [derivation] A non-significant interaction test is not evidence of homogeneity given the low power (Q2); report estimates with intervals.
- [derivation] Note the subtle difference: in the GLMM the segment intercepts are fixed effects (like stratum baselines) but the person random intercept is the frailty — so the analogue is a stratified shared-frailty model.

### Gaps
- Therneau & Grambsch text on strata-by-covariate interaction not directly verified.

## Q7. How does aggregation to person risk dilute segment-specific effects (relevance to "who")?

### Takeaway
Person risk depends on segments only through S_i = Σ_j exp(η_ij); a covariate acting in one segment type moves log S_i only by that type's hazard share, so segment-specific effects are diluted at person level, and much of the segment-model information comes from within-person allocation ("where"). Segment-specific slopes therefore mainly add "where" information and are unlikely to improve person-level prediction ("who") much.

### Cited Findings
- On-disk derivation: P_i = 1 − E_b[exp(−e^b S_i)]; a segment HR of 1.3 on a hazard share w = 0.3 multiplies the conditional person hazard by (1 − w) + 1.3w ≈ 1.09. — [on-disk] `reports/Pooled segment GLMM background.md`
- On-disk own calculation: for a feature coded on 2 of 9 segments, 6.2% of the segment model's information comes from the count of positive segments and 93.8% from allocation given the count; a person-level "any" model has 0.042 of the segment model's information for an effect on 2 of 9 segments vs 0.672 for an all-segment effect. — [on-disk] `reports/Pooled segment GLMM background.md`
- On-disk own sim: a segment-level LR test can reject on allocation while the person-level null is true (12/12 vs 1/12 replicates, direction only). — [on-disk] same file

### Inferences
- [derivation] Segment-specific slopes concentrate geometry's effect on fewer segments, which (by the on-disk calculation) shifts information even further to allocation. Options (b)/(c)/(d)/(f) therefore make the pooled-model LR test *more* likely to reject on "where" information, which conflicts with a who-only thesis framing. A shared slope across all segments is the coding closest to a "who" effect.
- [derivation] For "who", what matters is the person-level summary Σ_j w_ij·HR_ij; heterogeneity in β_j that averages out across a person's segments has nearly no person-level effect. So even if segment-type heterogeneity is real, it may be irrelevant to person-level ΔC.
- [derivation] Mundlak (g) is the relevant complement here: the between-person component β_B of curvature/taper is the "who" part; segment-type heterogeneity in β_W is "where". Option (g) answers a different question (confounding by person) than (b)–(f) (heterogeneity across types) and can be combined, at +1 df per feature.

### Gaps
- No external source on dilution of unit-specific effects under any-event aggregation; all numbers are project derivations/simulations on made-up parameters and should be rechecked on the fitted base model.

## Summary table of options (own synthesis, based on the findings above)

| Option | Extra df (curv + taper) | Confirmatory LR test | Power if truth common | Power if truth heterogeneous | Identifiability | Interpretability | Prespecification fit |
|---|---|---|---|---|---|---|---|
| (a) shared β (z within type) | 0 | clean, 2 df | best | loses projection; ~0 if signs differ | fine | one HR per SD (implies β/s_j raw) | standard |
| (b) × artery or × position | +4 | clean, 9 df block | lower (e.g. 0.56 → 0.45) | better if concentrated | ok (≥100s events per artery, est.) | 3 HRs/feature | fine if mechanism given |
| (b') artery + position additive | +8 | clean, 13 df | lower still | captures additive patterns | ok | 5 parameters/feature | own construct, no precedent found |
| (c) × 9 segments | +16 | clean but 21 df, exceeds person budget | much lower | best only if strongly heterogeneous | weak cells (~100 events/segment type, est.) | 9 HRs/feature, noisy | discouraged by guidelines |
| (d) random slope by type | +1 variance each | mean slope 1 df; reference distribution less clear; crossed RE breaks adaptive GHQ | ≈ (a) when variance → 0 | adaptive | poor with 9 levels, very poor with 3; singular fits likely | mean HR + SD | ML variance estimate is hidden model selection |
| (e) ridge/lasso on interactions | effective df < nominal | no standard LR χ² | ≈ (a) at strong penalty | moderate | stable | shrunk HRs | penalty choice must be prespecified (or CV, data-driven) |
| (f) Bayesian hierarchical | prior-dependent | posterior, not LR | ≈ (a) | adaptive | estimable with weakly informative prior; prior-sensitive with 3 groups | shrunk type HRs + τ | prior must be prespecified |
| (g) Mundlak within/between | +1 each | clean | n/a (different question) | separates who/where | between part noisy (2–9 segments) | β_W "where", β_B "who" | already discussed on-disk |

Recommendation pattern consistent with the sources (inference, not a sourced verdict): keep (a) for the single confirmatory LR test; prespecify one secondary joint test of feature × artery (3 groups, +4 df) reported as a finding, not a model-selection gate; if segment-specific estimates are wanted, estimate them with shrinkage (f or e) and report them as estimates. Do not use (c) or ML random slopes (d) for confirmatory purposes.
