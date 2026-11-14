# Statistical (non-ML) alternatives to the pooled segment-level cloglog random-intercept GLMM

Reading notes for the writer:

- **Planned model (from the three thesis .tex files).** Segment rows, cloglog link, normal random person intercept, adaptive Gauss-Hermite quadrature (30 nodes in the script). Base = segment position (pLAD reference), log segment length, dominance, log follow-up time, SCORE2 factors. Extended = base + 5 linear geometry terms. One LR test of the 5-df block. Person risk = integral over b of 1 - exp(-S_i e^b). Evaluation by person-grouped CV.
- **Discrepancy to resolve.** The assignment says "about 10-18 segments per person"; the thesis notes say "nine segments". The notes below hold for either.
- **Verification labels.** "Verified" = read in the fetched full text this session. "Abstract/snippet only" = seen only in a search snippet or abstract. Claims I know from textbooks but did not open this session are in Inferences or Gaps and marked "not verified this session".
- **Search budget.** All 7 allowed searches were used. Several primary papers could not be opened (403 or captcha); they are listed under Gaps.
- **Not repeated here.** Splines/GAMM, gamma frailty, brms mechanics, GPBoost and neural models are covered in `reports/Models to beat pooled cloglog GLMM.md`.

## 1. GEE / marginal logistic or cloglog with cluster-robust SEs versus the random-intercept GLMM

### Takeaway
GEE is a defensible sensitivity analysis for the geometry test (robust Wald instead of LR), and with hundreds of persons the sandwich variance is not the weak point. It is worse as the primary model: it gives only marginal segment risks, so the person-level "any segment" risk cannot be formed without adding a dependence model. For new-cluster prediction the published evidence shows a tie in calibration between GEE and a correctly integrated random-intercept model, not a GEE advantage.

### Cited Findings
- **Marginal calibration is a tie when the GLMM is integrated.** Pavlou et al. 2015 (verified; 100 simulated training sets of 1,000 patients in 20 centres). Median calibration slopes with the random effect set to zero were 0.948, 0.922, 0.884 and 0.788 at ICC 0.05, 0.10, 0.15 and 0.30. Integrating over the random effect gave 0.970, 0.984, 0.972 and 0.977. GEE gave 0.970, 0.983, 0.971 and 0.982. The authors call the integrated model "comparable to that of standard MLE (Ignoring clustering) and GEE". — [Pavlou et al. 2015, BMC Med Res Methodol](https://pmc.ncbi.nlm.nih.gov/articles/PMC4525751)
- **When each is preferred, per the same paper.** "GEE would be a direct approach to obtain marginal inference", but a random-effects model "would still be preferred" when the covariate-dependent MCAR assumption is doubtful or conditional predictions are wanted. A closed-form approximation is also given: beta_marginal ≈ beta_RE · c / sqrt(c²σ² + 1), c = 16√3/(15π). This is for the logit link, not cloglog, and the formula was reconstructed by the fetch tool from garbled rendering, so check it against the PDF before quoting. — [Pavlou et al. 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4525751)
- **The earlier miscalibration finding was a b = 0 artefact.** Bouwmeester et al. 2013 (verified; 20 centres, 1,000 patients, ICC 5/15/30%, also a 3% incidence scenario). At ICC 15% the random-intercept model with b = 0 had test calibration intercept 0.20 and slope 0.83, against -0.00 and 0.97 for standard logistic regression. C was 0.77 for both. The conditional (cluster-effect-using) C was 0.85, but that is not available for new clusters. — [Bouwmeester et al. 2013, BMC Med Res Methodol](https://pmc.ncbi.nlm.nih.gov/articles/PMC3658967)
- **GEE behaves like ordinary logistic regression for prediction.** Falconieri et al. 2020 (verified; simulation with 5 or 50 centres of 50 or 200 patients, ICC 5% or 20%, event rate about 0.3, 500 runs). GEE performed much like standard logistic regression. "Conditional models yielded calibrated predictions, whereas marginal models yielded miscalibrated predictions" at the centre level. The authors recommend random-intercept logistic regression and found it "robust against violations of the normality assumption". — [Falconieri et al. 2020, Biometrical Journal](https://pmc.ncbi.nlm.nih.gov/articles/PMC7383814)
- **Robustness of ML to the random-effects distribution.** McCulloch and Neuhaus report a "large degree of robustness of maximum likelihood" to misspecifying the shape of the random-effects distribution in many common situations (abstract only; the abstract does not say which quantities are robust). — [McCulloch & Neuhaus 2011, Statistical Science](https://arxiv.org/abs/1201.1980)
- **Confounding by cluster and informative cluster size.** Pavlou, Ambler and Omar 2021 study both for GEE and GLMM risk models and report that marginal predictions were mis-calibrated under those conditions (snippet only; full text returned 403/redirect). — [Pavlou et al. 2021, BMC Med Res Methodol](https://link.springer.com/article/10.1186/s12874-021-01321-x)
- **Sandwich variance needs many clusters.** The sandwich estimator "can be negatively biased with few clusters, typically ≤30" and GEE struggles for valid inference with fewer than 40 clusters (snippets only). — [arXiv 2205.05624](https://ar5iv.labs.arxiv.org/html/2205.05624); [arXiv 2511.23419](https://arxiv.org/html/2511.23419v1)
- **GEE versus random-effects models, small-sample behaviour.** Bie et al. (Stat Med 2021), as summarised in search results: GEE and marginalised multilevel models show similar small-sample bias when the correlation structure is right; random-effects models are more sensitive to correlation misspecification and can severely underestimate SEs of between-cluster associations with few clusters (snippet only; no URL to the primary paper was retrieved, so treat as unverified). — [search summary via Trials 2017 context](https://trialsjournal.biomedcentral.com/counter/pdf/10.1186/s13063-017-2248-1.pdf)
- **Rare events and separation.** With rare binary outcomes (≤10%), adjusting for several covariates can cause separation and non-convergence in logistic models (snippet only). — [arXiv 2205.05624](https://ar5iv.labs.arxiv.org/html/2205.05624)

### Inferences
- **(a) Test validity.** GEE has no likelihood, so the prespecified LR test becomes a 5-df robust Wald (or generalised score) test. With several hundred to ~2,000 persons as clusters, the ≤30-40 cluster problem does not apply. What limits the Wald test here is the number of events, not the number of clusters. GEE tests a marginal (population-averaged) hazard ratio, which is attenuated relative to the conditional one; the null hypothesis "all five coefficients zero" is the same in both, so the two tests address the same question.
- **(b) Prediction.** The thesis evaluates P(any segment has plaque). GEE estimates each segment's marginal risk and treats the correlation as a nuisance. The joint probability is not identified from the marginals. The naive 1 - ∏(1 - p_ij) assumes independence and overstates the person risk under positive within-person correlation (same point as the earlier report on plain XGBoost). A GEE therefore needs a second-stage person-level recalibration or an explicit dependence model, which is the GLMM again.
- **(c) Cost.** Same fixed-effect df; one fewer parameter (no σ²) with working independence.
- **(d) Implementation.** Easy: `geepack::geeglm(family = binomial("cloglog"), offset = ...)`, Stata `xtgee, family(binomial) link(cloglog) vce(robust)`, Python `statsmodels` GEE. QIC compares working correlation structures and mean models but is not a test, so it cannot replace the LR test (package behaviour not verified this session).
- **Best use.** Report a working-independence cloglog GEE with robust Wald test of the block as a sensitivity analysis. Agreement with the LR test shows the conclusion does not rest on the normal random intercept.
- **Verdict: worse as primary, useful as sensitivity.**

### Gaps
- No simulation was found that compares LR (GLMM) with robust Wald (GEE) type I error specifically for many small clusters (about 9-18 units) with rare events and a multi-df block. A short simulation at the thesis's own n, cluster size and event rate would be the only direct evidence.
- Hubbard et al. 2010 ("To GEE or not to GEE", Epidemiology) and Seaman, Pavlou and Copas 2014 (review of confounding by cluster and informative cluster size, Stat Med) are the standard references but were not opened this session.
- Whether the number of evaluable segments per person is informative (related to plaque risk) is an empirical question for this cohort. If it is, both GEE and GLMM marginal predictions are at risk (Pavlou 2021, snippet only).

## 2. Beta-binomial or person-level any-event / count models on aggregated features (one row per person)

### Takeaway
A person-level cloglog or logistic model of "any plaque" is the simplest valid competitor and the natural benchmark: the Riley criteria apply to it directly and its LR test is unproblematic. Its costs are that segment-specific geometry must be collapsed into person summaries (changing the hypothesis tested) and that all "where" information is lost. Beta-binomial offers nothing extra, because it cannot carry segment-level covariates.

### Cited Findings
- **Beta-binomial vs GEE.** Im 2020 reports the beta-binomial model "performed better for small sample, while GEE performed well under large sample" for clustered binary responses (abstract/snippet only). — [Im 2020, J Mod Appl Stat Methods](https://jmasm.com/index.php/jmasm/article/view/1084)
- **Beta-binomial vs random-intercept GLMM.** Harrison 2015 is reported to have found the beta-binomial model performed well even on data generated under a random-intercept GLMM (as cited in the Im 2020 snippet; the PeerJ primary returned 403, unverified). — [Harrison 2015, PeerJ](https://peerj.com/articles/1114/)
- **Both are adequate for clustered binomial data.** Ferrari and Comelli conclude that GLMMs and beta-binomial regression are both powerful for clustered binary outcomes (snippet only; behavioural-research setting). — [Ferrari & Comelli, arXiv 1605.01592](https://arxiv.org/pdf/1605.01592)
- **EPV in clustered prediction.** Wynants et al. 2015 (J Clin Epidemiol) found that the amount of clustering was not meaningfully associated with predictive performance and recommend at least 10 events per variable for clustered logistic prediction models (search summary only; primary not opened). — [UMC Utrecht record](https://researchinformation.umcutrecht.nl/en/publications/a-simulation-study-of-sample-size-demonstrated-the-importance-of-/)

### Inferences
- **What the person-level model is.** One row per person, outcome = any plaque, link cloglog with log follow-up (and optionally log total evaluable length) as offset, covariates = SCORE2 factors + person-level geometry summaries. If all covariates were person-level, the pooled GLMM's person risk 1 - E_b[exp(-S_i e^b)] and this model would target the same quantity; the GLMM only adds information through segment-level variation in covariates and outcomes.
- **(a) Test validity.** Fully valid, standard LR test on independent observations, no quadrature, no random-effect assumption. But it tests a different hypothesis: "person-summarised geometry predicts who", not "segment geometry predicts plaque in that segment". Curvature and taper are per segment, so a summary (mean, max, length-weighted mean) must be chosen in advance. Five features with one summary each keeps 5 df; more than one summary each breaks the budget. The three left-main features (angle, daughter asymmetry, Finet's ratio) are already person-level, so nothing is lost for them.
- **(b) Prediction.** No evidence found that either wins. Expected: similar discrimination for "who". The segment model can gain when the geometry effect is local (one bad segment) because averaging dilutes it; the person-level model is more robust because it makes no assumption about how segment risks combine. Persons with missing segments are handled naturally in the GLMM (S_i sums over observed segments) but need an exposure adjustment in the aggregated model.
- **(c) Cost.** Cheapest of all: no σ², no segment-position factor (saves about 8 df on nine segments), and the Riley person-level counting applies without argument.
- **(d) Implementation.** Trivial: `glm(family = binomial("cloglog"))` in R, `cloglog`/`glm` in Stata, `statsmodels` GLM in Python.
- **Beta-binomial / count of affected segments.** Uses the number of plaque segments out of n_i with person-level covariates only. It is the marginal counterpart of a random-intercept model with exchangeable segments, so it cannot include segment position, segment length or segment geometry. It answers "how many", not "any", and the thesis outcome is "any". R `glmmTMB(family = betabinomial)`, `VGAM`, `aod`; Stata `betabin` (user-written). No advantage here.
- **Verdict.** Person-level any-event model: roughly equal for "who", worse for the thesis question because it cannot say where; strongly recommended as a prespecified secondary benchmark. Beta-binomial: worse.

### Gaps
- No simulation or applied comparison was found of a segment-level (lesion-level) mixed model pooled to a person risk against a person-level model on aggregated features. This is the comparison the thesis could itself contribute.
- The choice of summary function for per-segment features has no source; it must be prespecified and justified in the thesis.

## 3. Penalised or Bayesian hierarchical versions (ridge/lasso GLMM, Firth, brms priors, shrinkage of the geometry block)

### Takeaway
The simulation evidence says penalisation improves calibration on average but is least reliable exactly at small effective sample size, and it removes the clean LR test of the geometry block. With only five prespecified linear terms inside a Riley budget, penalisation is not an improvement for the confirmatory analysis; a Bayesian fit with weakly informative priors is at best an equal-performing sensitivity analysis.

### Cited Findings
- **Penalisation is unreliable when most needed.** Riley et al. 2021 (verified; uniform shrinkage, ridge, lasso, elastic net; 500 datasets per scenario, N 100-1,000, 20 candidate predictors, 2.5-25 events per parameter). "Penalization methods are not a 'carte blanche'; they do not guarantee a reliable prediction model is developed." "They are more unreliable when needed most (i.e., when overfitting may be large)." "We recommend they are best applied with large effective sample sizes." Validation calibration slopes ranged from about 0 to 5 for some methods at the smallest sample sizes. A bootstrap shrinkage factor of 0.82 at N = 100 had a 95% range of 0.52 to 1.27. — [Riley et al. 2021, J Clin Epidemiol](https://pmc.ncbi.nlm.nih.gov/articles/PMC8026952/)
- **Same conclusion from an independent simulation.** Van Calster, van Smeden and Steyerberg (abstract verified): "the between-sample variability of calibration slopes was often increased relative to maximum likelihood"; shrinkage "improved predictions on average" but "often worked poorly in individual datasets, in particular when shrinkage was most needed"; "these methods do not solve problems associated with small sample size or low number of events per variable." "Firth's correction had only a small shrinkage effect but did so with low variability." — [Van Calster et al., arXiv 1907.11493](https://arxiv.org/abs/1907.11493) (published in Stat Methods Med Res 2020; journal version not opened)
- **Group-specific and local shrinkage.** Van de Wiel et al. 2023 (abstract verified): default single-penalty ridge/lasso can hurt calibration and coverage in low-dimensional prediction; "differential ridge penalties for covariate groups may enhance prediction accuracy" (linear regression); in the logistic setting local shrinkage gave better prediction accuracy than alternatives such as Firth's correction. — [van de Wiel et al., arXiv 2301.09890](https://arxiv.org/abs/2301.09890)
- **ML variance components are biased in sparse binary data.** A paper on REML-type estimation for binary GLMMs reports finite-sample bias of unrestricted ML in variance components, most visibly the random-intercept variance (snippet only). — [arXiv 2402.12719](https://arxiv.org/pdf/2402.12719)
- **brms supports the model.** `bernoulli("cloglog")` and new-level prediction with `sample_new_levels = "gaussian"` (as cited in the earlier local report; not re-opened). — [brms families](https://paulbuerkner.com/brms/reference/brmsfamily.html); [prepare_predictions](https://paulbuerkner.com/brms/reference/prepare_predictions.html)

### Inferences
- **(a) Test validity.** A penalised geometry block has no chi-square LR reference distribution, and lasso adds selection, which the thesis notes explicitly exclude ("No ranking, screening, stepwise or penalised selection"). A Bayesian fit replaces the test with a posterior or a LOO/ELPD comparison, which is not the prespecified frequentist test. Penalising the block therefore weakens rather than strengthens the added-value claim.
- **(b) Prediction.** Expected gain is small. The Riley budget already targets a shrinkage factor of 0.9, so little overfitting is left to remove, and the tuning parameter itself is noisy at this size (Riley 2021). The most plausible benefit of a Bayesian fit is stabilising σ² and avoiding boundary or separation problems, not better discrimination.
- **(c) Cost.** No extra nominal parameters, but one tuning parameter or prior scale that is poorly determined at small effective sample size.
- **(d) Implementation.** `glmmLasso` (R) fits L1-penalised GLMMs; to my knowledge it uses a Laplace/PQL-type approximation rather than adaptive quadrature, and its cloglog support is unverified. Firth-type correction is standard for ordinary logistic regression (`logistf`, Stata `firthlogit`) but I know of no standard Firth implementation for a cloglog GLMM with quadrature. `brms`/Stan is feasible but slow under 10 × 50 CV. Stata `bayes: mecloglog` exists to my knowledge. All four statements are from memory, not verified this session.
- **Defensible uses.** (i) A Bayesian cloglog GLMM with weakly informative priors as a sensitivity analysis on σ² and on person-level calibration. (ii) Post-estimation uniform shrinkage of the linear predictor from the person-level bootstrap, reported with its uncertainty as Riley recommends.
- **Verdict: equal at best for prediction, worse for the confirmatory test.**

### Gaps
- No simulation was found on penalised or Bayesian GLMMs for clustered binary prediction at small effective sample size; the cited evidence is for unclustered logistic and linear models.
- No evidence found on shrinking one block (geometry) while leaving the clinical block unpenalised in a GLMM.
- Software claims in the Inferences above need checking against package documentation.

## 4. Richer random-effect structures (segment-position effects, crossed effects, random slopes, vessel nesting, spatial correlation along the tree)

### Takeaway
Segment position as a fixed factor (already in the base model) is the right way to model position; nine positions are too few to treat as random and gain nothing. A vessel level, random slopes and tree-structured correlation are scientifically reasonable but poorly identified with 2-3 segments per vessel and few events per person, and most software then drops to the Laplace approximation, which is the less accurate choice for sparse binary clusters.

### Cited Findings
- **Quadrature and small clusters.** A PQL-versus-quadrature comparison notes that convergence of quadrature "is often a problem, particularly when variance parameters are close to zero or cluster sizes are small", and that variance components are often biased with both approaches (snippet only; the PMC page returned a captcha, and the paper is probably Kim, Choi and Emery 2013, which I could not confirm). — [PMC3886992](https://pmc.ncbi.nlm.nih.gov/articles/PMC3886992)
- **Ignoring a level in three-level binary data.** A comparison of mixed-effects logistic models for two nested levels of clustering reports more bias when a clustering level is ignored and nominal coverage for the full model (snippet only; probably Ten Have, Kunselman and Tran 1999, Stat Med, unconfirmed). — [catalogue record](https://opact.sdu.edu.tr/vufind/SummonRecord/FETCH-LOGICAL-c4355-eb1c556a54cc5761fa5031f2bb590dc5c0d14d14ae766bfc08d8acccf0c19fd13)
- **Clusters of size two.** For cluster size two, adaptive quadrature "prevails in terms of precision" but becomes clearly preferable only as cluster size grows (snippet only). — [Frontiers Appl Math Stat 2016](https://frontiersin.org/articles/10.3389/fams.2016.00018/pdf)
- **lme4 limitation.** In `glmer`, adaptive quadrature (nAGQ > 1) is available only for a single scalar random effect (as cited in the earlier local report; not re-opened). — [glmer documentation](https://search.r-project.org/CRAN/refmans/lme4/html/glmer.html)
- **Robustness of the simple structure.** Random-intercept logistic regression stayed reliable for prediction under non-normal random effects, a centre-by-predictor interaction and predictor-centre dependency (verified). — [Falconieri et al. 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7383814)

### Inferences
- **Segment-position fixed effects.** Already in the base model (8 df on nine segments). Making position random would save few df and requires estimating a variance from nine levels. A crossed person × position structure reduces to the same thing: fixed position effects plus the person intercept.
- **Vessel within person.** One extra variance parameter. It would capture LAD-specific versus RCA-specific susceptibility. With 2-3 segments per vessel and mostly 0-2 events per person, the vessel variance is likely to be estimated at or near zero (singular fit). It also complicates the person-risk integral (one integral per vessel inside the person integral). (a) The LR test of the fixed block stays valid if both models carry the same random structure, but in R it would rest on Laplace; Stata `mecloglog` supports multilevel adaptive quadrature to my knowledge (not verified this session). (b) No evidence that it improves person-level prediction; the person risk depends mainly on the total variance. Use as a sensitivity analysis only, with the boundary estimate reported if it occurs.
- **Random slopes (person-varying geometry effect).** Not estimable with about nine rows and at most a couple of events per person. A slope varying by segment position is a fixed interaction (5 × 8 = 40 df) or a partially pooled Bayesian term; it is outside the budget and already assigned to the secondary curvature/taper × artery analysis.
- **Spatially correlated effects along the tree (AR(1) along a vessel, CAR on the segment graph).** These need custom code or INLA/`glmmTMB` covariance structures fitted by Laplace. No source was found using them for coronary segment outcomes. For a person-level "any" risk the gain is doubtful: they reallocate correlation between neighbours without much changing the total.
- **Verdict: none is genuinely better; the vessel level is an optional sensitivity check, the rest are not feasible.**

### Gaps
- No simulation was found on identifiability of a middle-level variance with 2-3 binary units per middle-level cluster and rare events. The claim that the vessel variance will be weakly identified is reasoned, not sourced.
- No published coronary-tree application of spatial or tree-structured random effects to segment-level plaque outcomes was found.
- The two "probably" attributions above need the primary papers.

## 5. Time-to-event formulations (interval-censored shared frailty, discrete-time survival, Poisson with offset)

### Takeaway
With only two scans each segment contributes a single interval, so an interval-censored proportional-hazards frailty model collapses to the planned cloglog GLMM; survival software adds no information. The survival view is still useful because it settles an open thesis choice: log follow-up as an offset corresponds to a constant baseline hazard, a free coefficient on log follow-up to a Weibull baseline.

### Cited Findings
- **Cloglog is the grouped proportional-hazards model.** With a cloglog link the model "is of the proportional hazards form for survival times" grouped within intervals, and the approach requires intervals that are reasonably consistent across subjects (practitioner overview, snippet only). — [CTSPedia, interval-censored analysis](https://ctspedia.org/ctspedia/intervalcensoredanalysis)
- **Single-inspection designs are "case 1" interval censoring.** Huang and Wellner treat ML estimation of the proportional hazards model under case 1 interval censoring, where the event is only known to lie before or after an examination time (snippet only). — [Huang & Wellner 1997](https://sites.stat.washington.edu/jaw/JAW-papers/NR/jaw-huang-97LNS-SBS.pdf)
- **Frailty models for interval-censored data exist but need more structure.** Henschel et al. 2009 fit a Bayesian proportional-hazards model with log-normal and gamma frailties to interval-censored data and note the need to linearly approximate the cumulative hazard in their imputation step (snippet only). — [Henschel et al. 2009](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2679769/)
- **Conditional likelihood is unavailable for cloglog.** Allison states that conditional likelihood "cannot be used for" probit, complementary log-log and other non-logit models (verified in the blog post). — [Allison, Statistical Horizons](https://statisticalhorizons.com/?p=7229)
- **Gamma frailty closed form.** A gamma frailty gives a closed-form marginal survival and person risk (as cited in the earlier local report; not re-opened). — [arXiv 1403.6744](https://ar5iv.labs.arxiv.org/html/1403.6744)

### Inferences
- **Equivalence (reasoned, standard result, not verified in a primary source this session).** A segment that is plaque-free at scan 1 and inspected once at time t_i contributes P(event by t_i) = 1 - exp(-H0(t_i) exp(x'β + b)). With H0(t) = λt this is cloglog(p) = log λ + log t + x'β + b, the planned model with log follow-up as an offset. With a Weibull baseline H0(t) = λt^γ the coefficient on log t is γ, the "free term" option. A semiparametric baseline is identified only from between-person variation in follow-up length. Prentice and Gloeckler 1978 (already in the thesis bibliography as `prentice1978grouped`) is the primary reference.
- **Discrete-time survival.** Expands data to one row per interval at risk. With one interval per segment the person-period file is the current data set and the model is the same.
- **Poisson with log-exposure offset and random intercept.** Approximates the cloglog model when segment risk is low (1 - exp(-μ) ≈ μ). It misstates the variance for a binary outcome and can give fitted "risks" above one. No gain, and the cloglog version is exact under the same assumption.
- **(a)-(d).** Test validity and prediction are identical to the planned model when the baseline is parametric. Implementation is harder (R `icenReg`, `frailtypack`, `survival::survreg` with interval censoring; Stata `stintreg`, `mestreg`; software capabilities not verified this session). Nothing is gained with two scans.
- **Would matter with ≥3 scans.** More scans would give several intervals per segment and make the baseline hazard estimable.
- **Verdict: equal (the same model in different notation). Use the equivalence as justification, not as an alternative.**

### Gaps
- Prentice and Gloeckler 1978 and Allison 1982 were not readable this session (Allison PDF was a scanned image).
- Assumption worth stating in the thesis: the inspection time (follow-up length) must be non-informative for plaque risk. A search hit points to literature on informative examination times ([Open University record](https://oro.open.ac.uk/23914)), not opened.
- Segments with plaque at baseline are excluded by design (incident plaque); whether that left-truncation and the plaque-free-cohort selection affect the frailty distribution was not researched.

## 6. Conditional (fixed-effects) logistic regression using within-person contrasts only

### Takeaway
Conditional logistic regression is attractive only as a secondary "where" analysis of the segment-varying features (curvature, taper), because it removes all person-level confounding. It cannot serve the thesis's primary aim: it drops persons without events, cannot estimate person-level geometry (left-main angle, asymmetry, Finet's ratio), has no cloglog form, and yields no absolute risk. A between-within decomposition inside the planned GLMM gets most of the benefit for about two extra df.

### Cited Findings
- **Within versus mixed estimands.** Neuhaus and Kalbfleisch 1998 show that conditional likelihood estimates purely within-cluster covariate effects, whereas mixture (random-effects) models estimate a weighted average of between- and within-cluster effects, and that ignoring differing between and within effects can mislead (abstract/snippet only). — [Neuhaus & Kalbfleisch 1998, Biometrics, record](https://portal.mardi4nfdi.de/wiki/Publication:136641)
- **Consistency of conditional likelihood.** It "is known to produce consistent estimates of β even if α is correlated with X" (verified in the blog post). — [Allison, Statistical Horizons](https://statisticalhorizons.com/?p=7229)
- **Between-within method in logistic models.** Consistent only under a linearity condition (Brumback et al. 2010); Goetgeluk and Vansteelandt 2008 found biases "typically small in most practical settings"; Brumback et al. 2012 found downward bias "as high as 45%" in an extreme case with two individuals per cluster. Allison's recommendation is to add polynomial functions of the cluster means as a check (all as reported in the blog post; the primary papers were not opened). — [Allison, Statistical Horizons](https://statisticalhorizons.com/?p=7229)
- **Fixed-effects (dummy-variable) logistic regression for prediction.** Falconieri et al. recommend random-intercept or fixed-effects models over standard logistic regression and GEE for centre-specific prediction, and note that the random-intercept model can still predict for new centres using an average intercept (verified; centres had 50-200 patients each, far larger than nine segments). — [Falconieri et al. 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7383814)
- **Confounding by cluster harms marginal predictions.** Reported by Pavlou et al. 2021 (snippet only). — [Pavlou et al. 2021](https://link.springer.com/article/10.1186/s12874-021-01321-x)

### Inferences
- **(a) Test validity.** The conditional LR test is valid for within-person effects. Only persons with at least one event and at least one event-free segment contribute; with few events per person, a large share of the cohort drops out. Every person-level covariate cancels. In this design three of the five geometry features are person-level quantities placed on the pLAD/pLCx rows, so they would be identified only through that row coding, not through real within-person variation. The 5-df block test would effectively become a 2-df test of curvature and taper. It answers "where within a person", not "who".
- **(b) Prediction.** There is no intercept and no person effect, so no absolute risk and no person-level risk for a new person. It can only rank segments within a person (the within-participant C the thesis already plans to report descriptively).
- **(c) Cost.** No person-level parameters; segment-position dummies are still needed.
- **(d) Implementation.** Easy for logit (`survival::clogit`, Stata `clogit`/`xtlogit, fe`, `statsmodels` ConditionalLogit). No conditional likelihood exists for cloglog, so the hazard-ratio interpretation and the length offset logic change to odds.
- **Dummy-variable fixed effects per person.** Not viable: with about nine binary observations per person the incidental-parameters problem biases the coefficients (standard result, not verified this session).
- **Practical alternative.** Add the person mean of each segment-varying feature to the GLMM (between-within / Mundlak terms: person-mean curvature and person-mean taper, +2 df) and read the within coefficient. A clear difference between the within and between coefficients signals confounding by person. Caveat from the cited findings: small clusters are where the method's bias has been shown to be largest.
- **Verdict: worse as a prediction model, good as a prespecified secondary "where" analysis.**

### Gaps
- No evidence found on conditional logistic regression for lesion- or segment-level coronary outcomes.
- The size of between-within bias for clusters of about nine with rare events is not established by the sources read.
- How standardising features within segment type (planned in the thesis) interacts with a within-person contrast was not researched. It already removes segment-type mean differences, so the within-person contrast is between a person's segments relative to each segment type's norm.

## 7. Ranked shortlist for this thesis

### Takeaway
No statistical alternative is clearly better than the planned GLMM on all four criteria; the published evidence supports keeping it as the primary model, provided the person risk integrates over the random intercept. The valuable alternatives are cheap prespecified sensitivity analyses, not replacements.

### Cited Findings
- Correctly integrated random-intercept predictions calibrate as well as GEE for new clusters (slopes 0.97-0.98 for both across ICC 0.05-0.30). — [Pavlou et al. 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4525751)
- Random-intercept logistic regression is recommended over GEE and standard logistic regression for clustered prediction and is robust to non-normal random effects. — [Falconieri et al. 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7383814)
- Penalisation "should not be viewed as a solution to small effective samples sizes". — [Riley et al. 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8026952/)

### Inferences
Ranking is my synthesis of sections 1-6. Criteria: (a) test validity, (b) prediction for new persons, (c) parameter cost, (d) implementation.

| Rank | Formulation | (a) Test of geometry block | (b) Person-level prediction | (c) Cost | (d) Implementation | Verdict vs planned GLMM |
|---|---|---|---|---|---|---|
| 0 | Planned cloglog random-intercept GLMM, AGQ, integrated person risk | LR, valid if same rows/settings | Calibrated if b is integrated | base + 5 + σ² | `glmer` nAGQ, Stata `mecloglog` | Reference |
| 1 | Person-level cloglog/logistic on aggregated geometry | Valid and simplest, but tests a summarised hypothesis | Likely similar for "who"; no "where" | Lowest (no σ², no position factor) | Trivial | Equal for "who"; add as benchmark |
| 2 | Marginal cloglog GEE, working independence, robust Wald | Valid with this many persons; no LR | Segment marginals only; person risk needs extra dependence model | −1 (no σ²) | Easy | Worse as primary; good sensitivity test |
| 3 | Interval-censored / discrete-time frailty survival | Same as planned | Same as planned | Same | Harder | Equal (same model); use as justification |
| 4 | Bayesian GLMM with weakly informative priors | No LR test; posterior/LOO | No evidence of gain at this size | Same + prior scale | Feasible, slow in CV | Equal at best; optional sensitivity |
| 5 | Vessel-within-person nesting | Valid but Laplace in R | No evidence of gain | +1 variance, weakly identified | Moderate; Stata better | Optional sensitivity; likely singular |
| 6 | Conditional logistic / between-within terms | Valid for curvature and taper only | None (no absolute risk) | 0 / +2 | Easy | Worse for prediction; good "where" check |
| 7 | Ridge/lasso GLMM, Firth-type | Test lost or non-standard | Unreliable at small n | + tuning | Limited software | Worse |
| 8 | Beta-binomial count model | Cannot hold segment covariates | Wrong outcome ("how many") | Low | Easy | Worse |
| 9 | Random slopes, spatial/tree-correlated effects | Not estimable | — | High | Custom | Not feasible |

Suggested prespecified sensitivity set, in order of value per effort:
1. Person-level cloglog model with the same five features summarised per person (benchmark for "does the segment model earn its complexity").
2. Working-independence cloglog GEE with a robust 5-df Wald test (checks the LR result against the random-intercept assumption).
3. Between-within terms for curvature and taper (checks confounding by person).
4. Gamma frailty or Bayesian fit (checks sensitivity of person-level calibration to the frailty distribution; gamma frailty is covered in the earlier report).

### Gaps
- The ranking rests on evidence from multicentre prediction studies (20-50 clusters of 50-300 patients, event rates near 30%). No study was found for the thesis's regime: many clusters of about 9-18 units with rare events and a cluster-level "any event" target. A simulation calibrated to the cohort is the only way to turn the ranking into evidence.
- Papers that could not be opened and should be checked before citing: Pavlou et al. 2021 (CBC/ICS), Harrison 2015 (beta-binomial), Wynants et al. 2015 (EPV in clustered data), Bie et al. 2021, Neuhaus and Kalbfleisch 1998, Brumback et al. 2010/2012, Prentice and Gloeckler 1978, Allison 1982, PMC3886992.
- Textbooks named in the brief (Agresti; Fitzmaurice, Laird and Ware; Steyerberg; Gelman and Hill) were not consulted; nothing in these notes is sourced to them.
