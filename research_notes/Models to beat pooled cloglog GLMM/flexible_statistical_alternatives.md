# Flexible non-NN alternatives to the pooled segment cloglog GLMM

Scope: models that keep the segment-level binary likelihood (9 trunk segments per person, person random intercept or equivalent dependence), allow non-linear and interaction effects, and still give one person risk. Builds on `reports/Pooled segment GLMM background.md` (aggregation identity, marginal vs conditional risk, b = 0 and naive-product errors, allocation information in the "who" test) and `reports/Plaque risk model choice.md` (Riley budget ~13 parameters in ~1,080 plaque-free people, XGBoost/GPBoost roles). Those points are not repeated; they are referenced.

Labels: **[unverified]** = reference recalled from background knowledge, not opened in this research; check before `refs.bib`. **[derivation]** = own algebra. Tool budget limited this to ~15 searches/fetches, so several software facts are marked unverified.

## 1. GAMMs in mgcv (cloglog, random intercept, splines, tensor products, segment-varying smooths)

### Takeaway
A GAMM is the most direct flexible extension: same likelihood, same link, same person random intercept, same aggregation identity, with penalized smooths replacing linear geometry terms. It is realistic at this sample size only with few, prespecified smooths (low k, shared smooths across segments, one tensor product at most), and its gain over linear/RCS terms is an empirical question — no source found shows GAMMs beating a GLMM for clustered binary clinical prediction.

### Cited Findings
- In mgcv a term `s(id, bs="re")` appends the dummy matrix to the model; "The coefficients associated with the model matrix component are assumed i.i.d. normal, with unknown variance (to be estimated)", which "is equivalent to an identity penalty matrix (i.e. a ridge penalty)" — so a person random intercept is just one more penalized smooth — [mgcv smooth.construct.re docs](https://stat.ethz.ch/R-manual/R-devel/library/mgcv/html/smooth.construct.re.smooth.spec.html)
- The same page warns that such random effects "do not exploit the sparse structure of many random effects, and may therefore be relatively inefficient for models with large numbers of random effects", and points to `gamm`/`gamm4` as alternatives — [mgcv docs](https://stat.ethz.ch/R-manual/R-devel/library/mgcv/html/smooth.construct.re.smooth.spec.html)
- `binomial(link = "cloglog")` is a standard R GLM family and is accepted by `gam`/`bam` (standard R behaviour; [unverified] beyond general mgcv knowledge — mgcv accepts any `glm` family).
- Specification sketch (own, not from a source):
  `bam(y ~ seg + log_len + dom:vessel + SCORE2 terms + s(curv, k=5) + s(taper, k=5) + ti(curv, taper, k=c(4,4)) + s(lm_angle, k=4) + s(id, bs="re"), family=binomial("cloglog"), method="fREML", discrete=TRUE)`.
  Segment-varying effects: `s(curv, by=seg_ordered)` on an ordered factor gives a reference smooth plus 8 difference smooths; or `s(curv, seg, bs="fs")` (factor-smooth with one shared penalty) to borrow strength across segments. Both are mgcv constructs [unverified details: Wood 2017, *Generalized Additive Models: An Introduction with R*, 2nd ed., CRC].
- `gamm` fits non-Gaussian responses by PQL, which is known to be biased for binary outcomes with small clusters (Breslow & Clayton 1993, JASA 88:9–25 [unverified]); `gamm4` uses lme4's Laplace instead [unverified]. `gam/bam` with `bs="re"` use a Laplace-approximate REML/ML (Wood 2011, JRSS-B 73:3–36 [unverified]).
- Penalized smooth terms make the LR test of a "geometry block" non-standard: mgcv's `anova.gam`/`summary` p-values for smooths are approximate (Wood 2013, Biometrika 100:221–228 [unverified]). This conflicts with the decided prespecified LR test, so a GAMM can serve the predictive arm, not the test.
- No method among those compared was uniformly best: in Austin, Harrell & Steyerberg's simulations across six data-generating processes, "(un)penalized logistic regression and boosted trees tended to outperform the others", and classical methods "perform well in low-dimensional settings with large data sets" — [Austin, Harrell & Steyerberg 2021, Stat Methods Med Res 30(6):1465–1483](https://pmc.ncbi.nlm.nih.gov/articles/PMC8188999) (search-result summary; full text not opened).

### Inferences
- Parameter cost: a `k=5` cubic regression spline costs up to 4 df per feature but REML typically shrinks it to an edf of 1–3; an `ti(curv,taper)` adds up to 9 basis coefficients, edf usually 1–4. With 3 segment-level and 3 person-level geometry features as smooths plus one tensor, total edf could plausibly be 8–20 against a ~13-parameter Riley budget (from the earlier report). Segment-specific smooths (`by=seg`, 9 × 4 df) are out of budget; `bs="fs"` or no segment variation is the realistic option [derivation].
- Because the link and random intercept are unchanged, person risk is computed exactly as in the background report (1 − ∫exp(−e^b S_i)φ db) using the GAMM's fitted η; prediction for new persons must exclude the `s(id)` term (`exclude="s(id)"` in `predict.gam`) and then integrate over N(0, σ̂²), where σ̂² is read off `gam.vcomp` [derivation; mgcv argument names unverified].
- Simplest defensible use: a sensitivity/predictive model where geometry enters by REML-penalized smooths, compared to the linear GLMM on person-split out-of-fold log-likelihood, Brier and calibration.

### Gaps
- No published comparison of GAMM vs GLMM for clustered binary *prediction* was retrieved.
- Whether `bam(discrete=TRUE)` with a cloglog family and `bs="re"` gives estimates of σ² as accurate as adaptive quadrature (glmer nAGQ>1) was not checked; Laplace bias for binary data with small clusters is discussed in the background report.

## 2. Tree boosting / forests with random effects (GPBoost, MERF/MERT, GMERF, glmertree, REEMtree, BiMM forest)

### Takeaway
None of these offers a cloglog likelihood out of the box as far as could be verified: GPBoost supports only `bernoulli_logit` and `bernoulli_probit` for binary data. The binary-capable tree-mixed methods (GPBoost, BiMM forest, GMERF, MEml, glmertree) have mostly author-run simulation evidence of matching or slightly beating GLMMs; the only large benchmark (Sigrist 2023 preprint) is on continuous outcomes with ≥28k rows, irrelevant to ~1,100 persons with a few hundred events.

### Cited Findings
- GPBoost binary likelihoods: `bernoulli_logit` (aliases `binary`, `binary_logit`) and `bernoulli_probit`; `cloglog` is not listed. Grouped random effects via `group_data`, random coefficients via `group_rand_coef_data`, Gaussian processes via `gp_coords` — [GPBoost main parameters](https://gpboost.readthedocs.io/en/latest/Main_parameters.html)
- GPBoost methodology: Sigrist, F. (2022) "Gaussian Process Boosting", JMLR 23:1–46, models the predictor function as a boosted tree ensemble with Gaussian process / grouped random effects, estimating covariance parameters jointly; abstract claims higher accuracy than existing approaches — [JMLR](https://www.jmlr.org/papers/v23/20-322.html)
- Non-Gaussian extension: Sigrist, F. (2023) "Latent Gaussian Model Boosting", IEEE TPAMI, DOI 10.1109/TPAMI.2022.3168152 (arXiv 2105.08966) — [arXiv](https://arxiv.org/abs/2105.08966v5); binary results in that paper not checked.
- Sigrist (2023, **arXiv preprint 2307.02071**) compared linear mixed models, LightGBM, CatBoost, NN with embeddings/random effects and GPBoost on 8 datasets of ~28k–125k rows, **all continuous outcomes, no binary datasets**; GPBoost averaged 7.02% from the best result vs 47.6% for linear mixed models and beat the LMM on 7/8 datasets; MERF was excluded as too slow — [arXiv 2307.02071](https://arxiv.org/html/2307.02071v1)
- BiMM forest alternates a random forest with a GLMM taking the forest's predicted probabilities and a cluster random effect; simulations showed "similar or superior prediction accuracy compared to standard random forest, GLMMs and its tree counterpart (BiMM tree)" for clustered binary outcomes — Speiser et al. (2019) Chemometr Intell Lab Syst 185:122–134 — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0169743918304362); [ResearchGate](https://www.researchgate.net/publication/330328418_BiMM_forest_A_random_forest_method_for_modeling_clustered_and_longitudinal_binary_outcomes). Feature-selection follow-up: [Speiser et al. 2021, J Biomed Inform](https://pmc.ncbi.nlm.nih.gov/articles/PMC8131242/)
- Generalized mixed-effects random forest (GMERF, Pellagatti, Masci, Ieva, Paganoni; MOX report 36/2020) for binary outcomes; its simulation uses 10 groups × 40 observations and reports "prediction performances comparable to models like GLM and GLMM" — [MOX report](https://www.mate.polimi.it/biblioteca/add/qmox/36-2020.pdf) (technical report; later journal version [unverified]). Earlier generalized mixed-effects regression trees: [Statist Probab Lett](https://www.sciencedirect.com/science/article/abs/pii/S0167715217300895)
- MEml (Ngufor et al. 2019, J Biomed Inform 89:56–67) combines GLMM random effects with non-linear ML; it was "competitive with traditional GLMM" and substantially beat ML without random effects for longitudinal HbA1c change — [Mayo record](https://mayoclinic.elsevierpure.com/en/publications/mixed-effect-machine-learning-a-framework-for-predicting-longitud)
- MERF/MERT (Hajjem, Bellavance & Larocque 2011 J Stat Comput Simul; 2014 J Stat Comput Simul 84:1313–1328) and REEMtree (Sela & Simonoff 2012, Mach Learn 86:169–207) are Gaussian-response methods; the Python `merf` package is Gaussian only [all unverified].
- glmertree (Fokkema, Smits, Zeileis, Hothorn & Kelderman 2018, Behav Res Methods 50:2016–2034 [unverified]) grows a model-based tree on fixed effects with a `glmer` random effect; since it calls `glmer`, any `binomial(link=...)` including cloglog should be accepted [unverified — docs page returned 404].
- Boosted trees in Austin et al. 2021 were among the top performers alongside logistic regression in large-N, small-p cardiovascular simulations — [PMC8188999](https://pmc.ncbi.nlm.nih.gov/articles/PMC8188999)

### Inferences
- GPBoost with `bernoulli_probit` or `bernoulli_logit` and `group_data = person` is the strongest candidate in this family. The loss of cloglog costs the hazard interpretation and the Laplace-transform closure, but not the person risk: P_i = 1 − ∫Π_s[1 − F(f(x_is) + b)]φ(b; 0, σ̂²) db is still a 1-D integral computable by Gauss–Hermite on the boosted f [derivation]. At low segment risk logit, probit and cloglog nearly coincide (background report), so the link mismatch matters mainly for high-risk persons.
- GPBoost uses a Laplace approximation for non-Gaussian likelihoods (docs mention Laplace throughout), with the binary small-cluster σ² bias discussed in the background report; with 9 segments per person and rare events σ̂² may be biased [inference].
- glmertree is the only tree-mixed method likely to keep cloglog exactly, but a single tree partitions on fixed effects; it is an interaction-discovery tool more than a better predictor.
- Tuning (learning rate, depth, number of rounds) must be nested and grouped by person; with a few hundred person events, depth 1–2 boosting is a sensible ceiling (consistent with the earlier report's shallow-XGBoost recommendation).
- Tree methods give no LR test of the geometry block; they belong in the predictive comparison only.

### Gaps
- No direct simulation of GPBoost (binary) vs a correctly specified GLMM at n ≈ 1,000 clusters × 9 units with ~5–10% unit prevalence was found.
- GPBoost's handling of prediction for unseen groups on the response scale (whether `predict` integrates over the random effect for marginal probabilities) was not checked; it would in any case give marginal *segment* probabilities, not the person "any" probability, so the 1-D integral must be coded by hand.

## 3. Bayesian alternatives (BART with random effects, horseshoe cloglog, GP classification, random slopes)

### Takeaway
brms/Stan supports the exact current model with cloglog, plus regularized horseshoe or other shrinkage priors, splines (`s()` via mgcv bases) and segment-specific random slopes; this is the most faithful flexible Bayesian option. BART variants with random effects exist (mxBART, stan4bart) but binary BART uses a probit link, and evidence of gains over a GLMM at this size is limited to author simulations.

### Cited Findings
- brms bernoulli/binomial families "support `logit`, `probit`, `probit_approx`, `cloglog`, `cauchit`, `identity`, and `log`" — [brms brmsfamily](https://paulbuerkner.com/brms/reference/brmsfamily.html). Correct new-person prediction uses new levels with `sample_new_levels = "gaussian"` — [brms prepare_predictions](https://paulbuerkner.com/brms/reference/prepare_predictions.html) (from background report).
- stan4bart fits "semiparametric linear and multilevel models" combining non-parametric BART components with parametric components sampled by Stan, with lme4 formula syntax; current CRAN version 0.0-13; the CRAN page does not state the binary link — [CRAN stan4bart](https://cran.r-project.org/web/packages/stan4bart/index.html). Associated paper: Dorie, Perrett, Hill & Goodrich (2022) Entropy 24:1782 [unverified].
- mxBART: Spanbauer, C. & Sparapani, R. (2021) "Nonparametric machine learning for precision medicine with longitudinal clinical trials and Bayesian Additive Regression Trees with mixed models", Stat Med 40(11):2665–2691 — [citation via search result](https://arxiv.org/pdf/2210.01872); BART software: Sparapani, Spanbauer & McCulloch (2021) J Stat Softw 97(1):1–66 — [BART vignette](https://mirror.linux.duke.edu/pub/cran/web/packages/BART/vignettes/the-BART-R-package.pdf)
- Binary BART (Chipman, George & McCulloch 2010, Ann Appl Stat 4:266–298, doi 10.1214/09-AOAS285 — DOI confirmed on [CRAN stan4bart](https://cran.r-project.org/web/packages/stan4bart/index.html)) uses a probit data-augmentation (Albert–Chib) link [unverified for each package].
- Regularized horseshoe: Piironen & Vehtari (2017), Electron J Stat 11:5018–5051 [unverified]; available in brms as `horseshoe()` [unverified].
- rsBART / random-intercept BART (Tan, Flannagan & Elliott 2018?) [unverified; not found in this research].
- GP classification with grouped effects: GPBoost supports GPs (`gp_coords`) together with grouped random effects for binary likelihoods — [GPBoost docs](https://gpboost.readthedocs.io/en/latest/Main_parameters.html).

### Inferences
- A brms model `y ~ seg + ... + s(curv, k=5) + t2(curv, taper) + (1 + curv || id)` with `family = bernoulli("cloglog")` and horseshoe on the geometry block reproduces the current model exactly when the smooths shrink to linear, so it is nested by construction [derivation]. On ~10k segment rows and ~1,100 persons, Stan sampling is feasible but slow (hours, not days) [inference].
- A person-varying slope `(curv | id)` is weakly identified: each person has at most 9 segments and usually 0–2 events, so the slope variance will be dominated by the prior [inference]. Segment-specific slopes (geometry × segment interaction as fixed or as `(curv | seg)` with 9 levels) are more realistic and directly ask whether geometry acts differently by position — the 9-level random slope effectively is partial pooling of 9 interaction terms.
- Bayesian models give a posterior for person risk that integrates over b and over parameters, which handles the marginal/conditional issue naturally, but the prespecified LR test must still come from the frequentist GLMM.
- Expect gains over a linear GLMM only if true geometry effects are non-linear; with horseshoe the model mostly protects against overfitting rather than discovering structure [inference].

### Gaps
- No head-to-head of mxBART/stan4bart vs GLMM for clustered *binary* prediction was found.
- Whether stan4bart supports binary (probit) outcomes was not confirmed from the CRAN page.

## 4. Multivariate / joint models for the 9 correlated segment outcomes

### Takeaway
The random-intercept cloglog GLMM is already a shared-frailty model; the meaningful extensions are (a) a different frailty law (gamma: closed-form person risk), (b) an extra vessel-within-person frailty, or (c) a multivariate probit with a structured 9 × 9 correlation. Each adds 1–36 dependence parameters and changes person-level calibration far more than segment-level fit; unstructured correlation is unrealistic with a few hundred events.

### Cited Findings
- A frailty model is a random-intercept mixed model with a cloglog conditional link, and gamma frailty is popular "mainly for inference simplicity due to conjugacy between Gamma distribution and the complementary-log-log link" — [arXiv 1403.6744](https://ar5iv.labs.arxiv.org/html/1403.6744) (from background report).
- Gamma frailty with mean 1 and variance θ gives P_i = 1 − (1 + θS_i)^(−1/θ) [derivation, background report]; shared-frailty joint survival is the frailty Laplace transform at the summed cumulative hazard (Duchateau & Janssen 2008, *The Frailty Model*, Springer, doi 10.1007/978-0-387-72835-3) — [record](https://documentserver.uhasselt.be/handle/1942/9641)
- Multiplying separately modelled outcome risks "is only valid if the outcomes are conditionally independent given the covariates" — [Martin et al. 2021](https://arxiv.org/abs/2001.07624)
- Interval-censored clustered udder quarters with shared gamma frailty is the closest worked analogue — [Goethals et al. 2009](https://research.itg.be/en/publications/modeling-interval-censored-clustered-cow-udder-quarter-infection-/)
- Multivariate probit (Ashford & Sowden 1970; Chib & Greenberg 1998, Biometrika 85:347–361) [unverified]; R `mvProbit`, `MCMCpack`/`bayesm`-type samplers [unverified].
- Penalized discrete-time survival with heterogeneity (random effects): Groll & Tutz (2017), Lifetime Data Anal, DOI 10.1007/s10985-016-9359-y — cited on [CRAN glmmLasso](https://cloud.r-project.org/web/packages/glmmLasso/index.html); this is the closest published "penalized cloglog frailty" framework.

### Inferences
- Gamma frailty: same parameter count as now; closed-form person risk; marginal segment risk 1 − (1 + θe^η)^(−1/θ) is again explicit. Fitting a binary GLMM with gamma random intercept needs custom likelihood (the integral is closed form: L_i = Σ over subsets via inclusion–exclusion, or use the identity P(all 0) = (1+θS_i)^(−1/θ) only for the all-zero pattern) — for persons with ≥1 positive segment the likelihood requires inclusion–exclusion over positive segments, which is cheap when positives are 1–3 [derivation]. Comparing gamma vs lognormal on person-level calibration is the cheapest dependence sensitivity.
- Nested frailty (person + vessel-within-person): 1 extra variance; person risk becomes a nested 1-D integral (still cheap under cloglog). Identifiability is weak with 2–4 segments per vessel and rare events (earlier report).
- Multivariate probit: unstructured R has 36 correlations; a one-factor structure (each segment loading on one person factor) has 9 loadings, a vessel-block structure 3–6 parameters. Person risk = 1 − Φ_9(−η; R), computable by `mvtnorm::pmvnorm`. A one-factor probit with equal loadings is the probit random-intercept GLMM [derivation]. It gains nothing on "who" unless dependence differs by vessel.
- Copula models for 9 binaries are poorly identified (binary margins make copula parameters weakly identified) [inference, no source retrieved].

### Gaps
- No coronary or general clinical study comparing person-level calibration of lognormal vs gamma vs multivariate-probit dependence for "any of K units" outcomes was found.

## 5. Penalized GLMM and splines/fractional polynomials inside the existing GLMM

### Takeaway
The cheapest non-linearity is a 3-knot restricted cubic spline (1 extra df per feature) or a first-degree fractional polynomial inside the existing cloglog GLMM; the models stay nested, so the prespecified LR test survives with the df counted honestly. glmmLasso and ridge are predictive tools only and should not replace the unpenalized test model.

### Cited Findings
- glmmLasso: Groll & Tutz (2014) "Variable selection for generalized linear mixed models by L1-penalized estimation", Stat Comput 24(2):137–154, DOI 10.1007/s11222-012-9359-z; gradient ascent algorithm with a final unpenalized re-estimation on the selected variables; package v1.6.4 (2026-01-27) — [CRAN glmmLasso](https://cloud.r-project.org/web/packages/glmmLasso/index.html). Whether it accepts a cloglog link was not verified.
- Earlier project report already rules out lasso for the inferential model and reserves ridge for prediction, citing Van Calster et al. 2020 on variable calibration slopes after shrinkage — `reports/Plaque risk model choice.md`.
- In `lme4::glmer`, adaptive GH (nAGQ>1) is available for a single scalar random effect, i.e. this model — [glmer docs](https://search.r-project.org/CRAN/refmans/lme4/html/glmer.html) (from background report); so `rms::rcs()` or `splines::ns()` terms can be added with no change to estimation.
- Fractional polynomials: Royston & Altman (1994) JRSS-C 43:429–467; MFP: Royston & Sauerbrei (2008) Wiley [unverified].

### Inferences
- Concrete plan: linear GLMM (primary, test) → same GLMM with `rcs(x, 3)` on curvature, taper and LM angle (+3 df) and one product term curvature × taper (+1 df) → LR comparison of these as a prespecified secondary, or out-of-fold person log-likelihood. Total extra df 4, inside budget [derivation].
- An interaction curvature × taper as a single product term is the minimal test of the WSS-motivated interaction; a tensor spline is the GAMM upgrade.
- Ridge on a GLMM: `glmmTMB` does not provide a penalty directly; options are brms with normal priors (Bayesian ridge), mgcv `paraPen`, or `glmmLasso` with lasso [unverified for exact syntax].

### Gaps
- No evidence found specific to clustered binary data on RCS vs FP vs penalized splines for prediction.

## 6. Pooling 1 − ∏(1 − p_s) and marginal vs conditional risk across the alternatives

### Takeaway
Already resolved for the GLMM in the background report (integrate over b; b = 0 gives the median person; naive product of marginal segment risks overestimates and can re-rank). The new point here is how each alternative inherits this: every random-effect model (GAMM, GPBoost, BART-mixed, brms) needs the same 1-D integral coded by hand; models without a random effect (plain XGBoost/forest on segment rows) produce marginal segment risks whose naive product is biased upward and must be recalibrated at person level.

### Cited Findings
- Marginal predictions "are often obtained, incorrectly, using only estimates of the fixed effects"; b = 0 predictions gave calibration slope 0.788 at ICC 0.30 vs ~0.98 integrated — [Pavlou et al. 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4525751/) (from background report).
- No package returns P(any segment) directly; GLMMadaptive "marginal" predictions are marginal *segment* risks — [GLMMadaptive vignette](https://drizopoulos.github.io/GLMMadaptive/articles/Methods_MixMod.html) (from background report).
- GPBoost random effects for grouped data — [GPBoost docs](https://gpboost.readthedocs.io/en/latest/Main_parameters.html).

### Inferences
- For a non-cloglog link F (logit/probit in GPBoost, BART), P_i = 1 − ∫Π_s[1 − F(η_is + b)]φ(b)db; the product stays inside the integral and the S_i sufficient statistic is lost, but cost is still trivial (9 terms × ~40 nodes) [derivation].
- For probit with normal b, marginal segment risk is closed form Φ(η/√(1+σ²)), but the "any" probability is still an orthant probability of a 9-dim equicorrelated normal (ρ = σ²/(1+σ²)) — computable by 1-D integration or `pmvnorm` [derivation].
- For tree ensembles trained on segment rows without a random effect: a person-level recalibration (logistic/cloglog of observed A_i on log Σ_s(−log(1 − p̂_s)) in training folds) is the simplest fix; it restores calibration but not ranking errors from the naive product [derivation].
- Because C is blind to aggregation errors (background report), any comparison of alternatives must report person-level calibration slope and intercept, not only ΔC.

### Gaps
- No published study comparing the person-level calibration of aggregated segment predictions across GLMM, GPBoost and BART was found.

## 7. Summary table: candidates for this cohort

| Model | Software | Keeps cloglog? | Extra params vs linear GLMM | LR test possible? | Interpretability | Realism at ~1,100 persons, few hundred events | Evidence it beats a GLMM |
|---|---|---|---|---|---|---|---|
| GLMM + 3-knot RCS + 1 product term | lme4 `glmer` (nAGQ>1), GLMMadaptive | Yes | ~4 df | Yes (nested) | High (HR curves) | High | None specific; standard practice |
| GAMM (penalized splines, `ti`, `bs="fs"`) | mgcv `gam/bam`, gamm4 | Yes | edf ~4–15 | Approximate only | High (smooth plots) | Moderate if smooths shared across segments | None retrieved for clustered binary prediction |
| Bayesian cloglog GLMM + horseshoe/splines/segment slopes | brms/Stan | Yes | many, shrunk | No (use LOO/elpd) | High | Moderate (compute time) | None retrieved |
| Gamma or nested frailty | custom likelihood; frailty texts | Yes | 0–1 | Yes | High | High (gamma), weak (nested) | Sensitivity only |
| Multivariate probit (factor/block R) | mvProbit, Stan | No (probit) | 3–36 | Yes vs probit RI | Moderate | Low for unstructured R | None |
| GPBoost (trees + person RE) | gpboost R/Python | No (logit/probit) | tuned ensemble | No | Low (SHAP) | Moderate with depth 1–2, nested grouped tuning | Large continuous benchmarks only (preprint) |
| BiMM forest / GMERF / MEml | R code from authors | Via GLMM step: possibly | ensemble | No | Low | Moderate | Author simulations: "similar or superior" |
| glmertree | glmertree | Probably (via glmer) | tree splits | No | High (tree) | Moderate | None retrieved |
| mxBART / stan4bart | BART, stan4bart | No (probit) | ensemble | No | Low–moderate | Moderate | Author simulations only |
| GP classification + RE | GPBoost, Stan | No | GP hyperparams | No | Low | Moderate in low dimension | None retrieved |

### Overall inferences
- Given ~13 affordable parameters and a few hundred person events, the realistic "beat the GLMM" ladder is: linear GLMM → RCS/product-term GLMM (nested, testable) → GAMM with shared smooths → GPBoost (logit, shallow) as the flexible ML check. Bayesian brms is the best single tool if non-linearity and segment-varying slopes are to be explored with honest uncertainty.
- Since most person-level "who" information is diluted by the log-sum-exp aggregation (background report), flexible segment-level functions are unlikely to change person-level C much; any gain is more likely to show in "where" (within-person) discrimination. A flexible model that wins on segment-row log-likelihood but not on person-level out-of-fold log-likelihood/calibration has not beaten the GLMM for the "who" question [inference].
- Skepticism: every positive claim for GPBoost, BiMM forest, GMERF, MEml, mxBART comes from the method developers' own simulations or (for GPBoost's broad benchmark) a preprint on large continuous datasets. Independent evidence (Austin et al. 2021; Christodoulou et al. 2019 via earlier report) points to little or no gain of flexible learners over well-specified regression in low-dimensional clinical data.

### Gaps (overall)
- Not opened in this research and to verify before citing: Wood 2017 book; Wood 2011/2013; Breslow & Clayton 1993; Fokkema et al. 2018; Hajjem et al. 2011/2014; Sela & Simonoff 2012; Dorie et al. 2022; Piironen & Vehtari 2017; Chib & Greenberg 1998; Royston & Altman 1994; GMERF journal version; full text of Austin et al. 2021 and Sigrist 2022/2023 binary results.
- No cardiovascular imaging application of GAMM, GPBoost, BART-mixed or multivariate probit to segment-level plaque outcomes was searched for systematically (tool budget); none surfaced incidentally.
