# Aggregating segment-level GLMM risks into a person-level risk (method background)

Scope: general method only, no CGPS results. Notation: person i, segment j = 1..J (J = 9 trunk
segments), linear predictor without the random effect η_ij = x_ij'β, person random intercept
b_i ~ N(0, σ²), conditional segment risk p_ij(b) = 1 − exp(−exp(η_ij + b)) (cloglog link).
Person outcome A_i = 1 if any segment has an event. Summed hazard S_i = Σ_j exp(η_ij).

Status labels used below: **[cited]** = stated in a source I opened or whose abstract/record I saw;
**[derivation]** = standard algebra, written out here and checkable by the reader, not quoted from a
source; **[unverified citation]** = reference I am confident of from prior knowledge but did not
re-open in this session (DOI must be checked before it goes in `refs.bib`).

Prior project documents read for context (not re-derived from scratch): `experiments/who/pooled_score2/pooling.md`,
`reports/Segment model to person risk.md`, `reports/Person risk pooling error check.md`,
`reports/Pooled who progression code issues.md` (all in `~/Desktop/Speciale/CGPS_statistics-/`).
Everything below agrees with them except where flagged.

## 1. Conditional independence, the "any event" (noisy-OR) aggregation, cloglog closure, Poisson/frailty link

### Takeaway
Under a random-intercept GLMM, segments are independent only *given* b_i, so P(A_i = 1 | b) = 1 − ∏_j(1 − p_ij(b)) (the noisy-OR form), and the marginal person risk is 1 − E_b[∏_j(1 − p_ij(b))]. With the cloglog link the product collapses to exp(−e^b S_i), so the person risk is one minus the Laplace transform of the lognormal frailty e^b evaluated at S_i: a one-dimensional integral regardless of J, with no closed form for the lognormal (closed form for gamma).

### Cited Findings
- The GLMM assumption is that responses within a cluster are independent conditional on the random effect; the correct marginal prediction for a member of a *new* cluster averages the conditional risk over the estimated random-effect distribution N(0, σ̂²) (their eq. 6). [cited] — [Pavlou, Ambler, Seaman & Omar 2015, BMC Med Res Methodol 15:59, doi:10.1186/s12874-015-0046-6](https://pmc.ncbi.nlm.nih.gov/articles/PMC4525751/)
- Skrondal & Rabe-Hesketh treat prediction of random effects (empirical Bayes) and of expected responses in multilevel GLMs, and distinguish predictions that condition on the random effects from those that integrate over them. [cited, abstract level] — [Skrondal & Rabe-Hesketh 2009, JRSS-A 172(3):659–687, doi:10.1111/j.1467-985X.2009.00587.x](https://ideas.repec.org/a/bla/jorssa/v172y2009i3p659-687.html)
- Noisy-OR in the MIL literature is exactly this form: "the posterior probability for the positive bag can be written as p(y = 1|x) = 1 − ∏[1 − σ(w'x_j)]", i.e. one minus the probability that all instances are negative. [cited] — [Siemens MIL-for-CAD patent US8131039B2](https://patents.google.com/patent/US8131039B2/en); see also [Raykar et al. ICML 2008](https://icml.cc/imls/conferences/2008/papers/587.pdf)
- Noisy-OR as a canonical-interaction model originates in Pearl, *Probabilistic Reasoning in Intelligent Systems* (Morgan Kaufmann, 1988). [unverified citation; book, no DOI checked]
- Cloglog is the grouped-time / discrete-time form of the proportional-hazards model: when data come from a continuous PH model, the cloglog of the interval event probability is linear in covariates (Prentice & Gloeckler 1978, Biometrics 34:57–67, doi:10.2307/2529588). [cited via secondary sources] — [SAS PROC LOGISTIC docs](https://support.sas.com/documentation/cdl/en/statug/63962/HTML/default/statug_logistic_sect072.htm); [SAS example](https://go.documentation.sas.com/api/docsets/statug/v_016/content/statug_logistic_examples19.htm); [DOI record](https://synapsesocial.com/papers/W1994670953)
- The lognormal Laplace transform E[exp(−s e^b)] has no closed form; Asmussen, Jensen & Rojas-Nandayapa give a closed-form approximation by a modified Laplace method in terms of the Lambert W function. [cited, abstract level] — [Asmussen, Jensen & Rojas-Nandayapa 2016, Methodol Comput Appl Probab 18(2):441–458, doi:10.1007/s11009-014-9430-7](https://arxiv.org/pdf/1803.05878)
- In shared-frailty survival models a cluster's joint survival is the frailty Laplace transform evaluated at the summed cumulative hazard; standard references are Hougaard, *Analysis of Multivariate Survival Data* (Springer 2000, doi:10.1007/978-1-4612-1304-8) [unverified citation] and Duchateau & Janssen, *The Frailty Model* (Springer 2008, doi:10.1007/978-0-387-72835-3) [DOI cited] — [Duchateau & Janssen record](https://documentserver.uhasselt.be/handle/1942/9641). Duchateau & Janssen cover parametric/semiparametric frailty, multifrailty and multilevel models, fitted by EM, penalised likelihood, Laplace integration and Bayesian methods. [cited] — same record. (The project report's udder-quarter example is in Duchateau & Janssen's book per prior project notes; I could not confirm it from the search records in this session.)

### Derivations [derivation]
1. Conditional independence given b: P(A_i = 0 | b) = ∏_j (1 − p_ij(b)). With cloglog, 1 − p_ij(b) = exp(−e^{η_ij + b}), so
   P(A_i = 0 | b) = exp(−e^b Σ_j e^{η_ij}) = exp(−e^b S_i).
   Hence P(A_i = 1 | b) = 1 − exp(−exp(log S_i + b)): **conditional on b, the person outcome is itself a cloglog model with linear predictor log S_i + b**. This is "closure" of cloglog under the any-event (noisy-OR / max) aggregation. Logit and probit are not closed: ∏(1 − expit(·)) is not 1 − expit of anything linear.
2. Marginal person risk: P_i = 1 − ∫ exp(−e^b S_i) φ(b; 0, σ²) db = 1 − L_σ(S_i), where L_σ(s) = E[exp(−sU)] is the Laplace transform of the lognormal frailty U = e^b. The integrand depends on the J segments only through the scalar S_i.
3. Poisson-process reading: if new-plaque onsets in segment j follow a Poisson process with cumulative intensity Λ_ij = U_i e^{η_ij} over the follow-up window, then P(no event in j | U) = exp(−Λ_ij), i.e. cloglog; superposition of independent Poisson processes (independent given U) is Poisson with intensity U_i S_i, so P(no event in person | U) = exp(−U_i S_i). The person count N_i | U ~ Poisson(U S_i); marginally N_i is Poisson-lognormal (Aitchison & Ho 1989, Biometrika 76:643–653, doi:10.1093/biomet/76.4.643 [unverified citation]), and P_i = 1 − P(N_i = 0). With gamma U (mean 1, variance θ) instead, P(N_i = 0) = (1 + θS_i)^{−1/θ}, the negative-binomial zero probability (closed form).
4. Caveat on the Poisson reading: segment outcomes are binary, not counts, so only the event "≥1 onset" is observed per segment. The cloglog link is what one gets if the latent process is Poisson, but the data do not test that; the binary GLMM is just a GLMM with a cloglog link.
5. Log-sum-exp: log S_i = logsumexp_j(η_ij), a smooth maximum. Person risk is dominated by the person's highest-hazard segments; a covariate that raises risk in one segment only moves log S_i by roughly that segment's share of S_i.

### Inferences
- The aggregation is exact *under the model*; it is not an approximation. All approximation enters via (a) model misspecification (conditional independence, constant σ, normality of b, link) and (b) numerical integration.
- The person-level marginal model implied by the GLMM is 1 − L_σ(S_i), which is *not* a cloglog in log S_i marginally (it is flatter), so the segment-model β are conditional (person-specific) effects, not the coefficients one would get from a marginal person-level cloglog fit.

### Gaps
- I did not open Hougaard (2000) or Duchateau & Janssen (2008) full texts in this session; chapter/page numbers for the Laplace-transform identity need to be taken from the books.
- No published source found that states the "cloglog closure under noisy-OR" in exactly these words for GLMMs; it is a direct consequence of the grouped-PH / frailty algebra and should be presented as a derivation.

## 2. Why b = 0 is wrong for the marginal risk; Gauss–Hermite; new vs existing clusters; out-of-fold prediction

### Takeaway
Plugging in b = 0 gives the risk of the *median* person (b has median 0 and risk is monotone in b), not the population-average risk; the gap is a Jensen-type effect whose sign depends on the risk level. For a held-out person (a new cluster) the correct prediction integrates over N(0, σ̂²) from the training fold, computed by Gauss–Hermite quadrature; empirical-Bayes/BLUP predictions are only for existing clusters with observed outcomes and would leak outcome information under person-split CV.

### Cited Findings
- Using only the fixed effects (random effects set to zero) to obtain marginal risks is incorrect and common in applied work; because random-intercept coefficients are larger in absolute value than marginal ones, u = 0 predictions are too spread out and their mean differs from the integrated mean. In simulation (logit, ICC = 0.30) the u = 0 approach had calibration slope 0.788 and calibration-in-the-large 0.142, while integrated predictions were well calibrated; the error is small at ICC 0.05 and the authors note ICC in hospital data rarely exceeds 0.15. [cited] — [Pavlou et al. 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4525751/)
- Recommendation: new clusters → marginal predictions integrated over the random-effect distribution; existing clusters → conditional predictions using the cluster's estimated random effect, ideally integrating over its posterior. [cited] — [Pavlou et al. 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4525751/)
- Bouwmeester et al. found that a random-intercept model discriminated better than standard logistic regression only when the cluster effect was used in prediction (c 0.69 vs 0.66), in 1,642 patients nested in 19 anaesthesiologists; Pavlou et al. 2015 note that Bouwmeester's marginal predictions set the random effects to zero. [cited, abstract level] — [Bouwmeester et al. 2013, BMC Med Res Methodol 13:19, doi:10.1186/1471-2288-13-19](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3658967/)
- Bayesian models with informative priors on random effects for new clusters have been proposed as an alternative to setting random effects to zero (Ni et al. 2018, doi:10.1186/s12874-018-0543-5). [cited via search snippet] — [search record](https://research.utwente.nl/en/publications/prediction-models-for-clustered-data-with-informative-priors-for-/)
- Empirical Bayes prediction of random effects (and its three kinds of standard errors) is treated in Skrondal & Rabe-Hesketh 2009. [cited, abstract] — [IDEAS record](https://ideas.repec.org/a/bla/jorssa/v172y2009i3p659-687.html)
- Adaptive Gauss–Hermite quadrature (Liu & Pierce 1994, Biometrika 81(3):624–629, doi:10.2307/2337136) centres and scales nodes using a Gaussian (Laplace) approximation of the integrand; it often beats Monte Carlo with 10–100 points. Jin & Andersson 2020 (Biometrika 107(3):737–744) corrected Liu & Pierce's stated error rate and concluded AGHQ is less accurate than previously thought. [cited] — [fastGHQuad manual](https://cran.r-project.org/web/packages/fastGHQuad/refman/fastGHQuad.html); [Jin & Andersson record](https://ideas.repec.org/a/oup/biomet/v107y2020i3p737-744..html)
- Coefficients from random-effects (cluster-specific) models are larger in magnitude than population-averaged (GEE/marginal) coefficients; marginal models are in the GEE tradition of Liang & Zeger 1986 (Biometrika 73:13–22). [cited for Liang & Zeger existence] — [Liang & Zeger 1986 pdf](https://www.biostat.jhsph.edu/~jleek/teaching/2011/754/reading/liangandzeger.pdf); the attenuation formula of Zeger, Liang & Albert 1988 (Biometrics 44:1049–1060, doi:10.2307/2531734) is [unverified citation].

### Derivations [derivation]
1. **Median, not mean.** P(A_i = 1 | b) is strictly increasing in b and b has median 0, so 1 − exp(−S_i) is the risk of the median person with covariates x_i. The population-average risk is P_i = 1 − E[g(b)], g(b) = exp(−S_i e^b).
2. **Jensen, sign depends on S.** g''(b) = g(b)·S e^b (S e^b − 1). At b = 0, g is concave when S < 1 and convex when S > 1. A second-order expansion E[g(b)] ≈ g(0) + (σ²/2) g''(0) gives: if S_i < 1 (i.e. b = 0 risk < 1 − e^{−1} ≈ 0.632) the b = 0 plug-in *underestimates* P_i; above 0.632 it overestimates. This is a small-σ approximation; for large σ the global shape of g matters, but the qualitative result (plug-in too extreme on both sides, compressed integrated risks) matches Pavlou's calibration slope < 1 for u = 0 predictions. The 0.632 threshold is a second-order approximation, not exact.
3. **Naive product of marginal segment risks is a different error.** 1 − ∏_j(1 − p̄_ij) with p̄_ij = 1 − E[exp(−e^b e^{η_ij})] treats segments as marginally independent. Since each 1 − p_ij(b) is decreasing in b, the terms are positively associated (Harris/Chebyshev inequality), so E[∏(1 − p_ij(b))] ≥ ∏ E[1 − p_ij(b)] and the naive product **always overestimates** P_i (equality iff σ = 0). The prior project error-check confirms this and notes that "p̄_ij" must mean *marginal* segment risks.
4. **Gauss–Hermite.** With nodes x_k and weights w_k for ∫ e^{−x²} f(x) dx, E[f(b)] = π^{−1/2} Σ_k w_k f(√2 σ x_k). The integrand exp(−S e^b) is smooth but for large σ·S the transition region in b becomes sharp, so non-adaptive GH needs more nodes as σ grows; adaptive GH, or checking against a much larger node count, guards against this. The fitting likelihood of the GLMM is a separate integral (per person, over the joint segment likelihood) and should also use adaptive quadrature rather than the Laplace approximation when clusters are small and outcomes binary (lme4 `glmer` allows nAGQ > 1 for a single scalar random effect, per prior project report).
5. **Out-of-fold prediction under person-split CV.** A held-out person is a new cluster: no outcome-based information about b_i is admissible. The only valid prediction is 1 − L_σ̂(Ŝ_i) with β̂, σ̂ and all preprocessing from the training fold. An empirical-Bayes b̂_i (BLUP/posterior mode) uses that person's own segment outcomes, which define A_i, so it is target leakage. (Conditioning on *baseline* information that is not the outcome would be legitimate but is not what EB does.)

### Inferences
- In the thesis, b = 0 vs integral should be framed as "median person vs average person", with Jensen as the reason they differ, and with the explicit statement that the size of the gap grows with σ².
- Because the integrated risk is a monotone function of S_i (for one common σ), and so is the b = 0 plug-in, the two give identical person-level C; only calibration distinguishes them. The naive product is not a function of S_i alone (depends on how hazard is spread over segments), so it can also change the ranking.

### Gaps
- No published simulation found for the *cloglog, J = 9, large-σ* setting; Pavlou's numbers are for logit models with ICC ≤ 0.30, so they show direction, not magnitude, here.
- Could not open Skrondal & Rabe-Hesketh full text in this session; specific equation numbers for "marginal expectation for a new cluster" must come from the paper.

## 3. Precedents and terminology: frailty, multilevel aggregation, MIL/noisy-OR, and two meanings of "pooling"

### Takeaway
The segment→person aggregation has direct precedents in shared-frailty survival analysis (cluster survival = Laplace transform at summed hazard), in multilevel prediction for new clusters, and in multiple-instance learning, where noisy-OR combines instance (lesion/nodule) probabilities into a bag (patient) probability. In the hierarchical-modelling literature "pooling" means something else (partial pooling = shrinkage of cluster estimates towards the population), so the thesis should call the segment→person step "aggregation" and reserve "pooling" for borrowing strength, or define the term once.

### Cited Findings
- MIL was formalised by Dietterich, Lathrop & Lozano-Pérez: instances grouped in bags, only bag labels observed; a bag is positive if at least one instance is positive. [cited] — [Dietterich et al. 1997, Artif Intell 89:31–71, doi:10.1016/S0004-3702(96)00034-3](https://sci2s.ugr.es/keel/pdf/algorithm/articulo/1997%20-%20DietterichLathropLozano-Perez%20-%20AI.pdf)
- Carbonneau et al. survey MIL problem characteristics (bag composition, data distributions, instance-label ambiguity, task) and show these strongly affect method performance across 16 MIL methods. [cited] — [Carbonneau, Cheplygina, Granger & Gagnon 2018, Pattern Recognit 77:329–353, doi:10.1016/j.patcog.2017.10.009 (DOI from one record only)](https://arxiv.org/pdf/1612.03365.pdf)
- Medical-imaging noisy-OR: Liao et al. combine the cancer probabilities of the top-5 detected lung nodules with a **leaky** noisy-OR gate into a subject-level cancer probability; the leak term covers cancer not explained by any detected nodule. [cited] — [Liao et al. 2017/2019, arXiv:1711.08324 (published IEEE TNNLS; DOI not confirmed in this session)](https://arxiv.org/pdf/1711.08324)
- Mammography: noisy-OR over lesion malignancy probabilities gives image-level scores (M&M detector). [cited, search snippet] — [arXiv:2308.06420](https://arxiv.org/pdf/2308.06420)
- Cheplygina et al. survey notes noisy-OR as one way to combine instance outputs, and that bag-level classifiers are often more robust but cannot give instance labels. [cited, search snippet] — [Cheplygina, de Bruijne & Pluim 2019, arXiv:1804.06353](https://arxiv.org/pdf/1804.06353)
- Partial pooling (Gelman & Hill radon example): complete pooling = one estimate for all clusters; no pooling = separate estimates; partial pooling = multilevel model whose group-level variance controls shrinkage (variance 0 → complete pooling, ∞ → no pooling); small clusters are pulled to the mean. In Gelman's radon cross-validation, errors were 0.84 complete, 0.86 no pooling, 0.79 multilevel. [cited via lecture/paper] — [Gelman 2004, "Multilevel (hierarchical) modeling: what it can and can't do"](https://www.stat.cmu.edu/~brian/463-663/week06/some%20nice%20papers/multi.pdf); book: Gelman & Hill, *Data Analysis Using Regression and Multilevel/Hierarchical Models*, CUP 2007 (some sources date it 2006; doi:10.1017/CBO9780511790942 [unverified citation])
- Paired-organ analogue (eyes within a person): eye-level models with a person effect give more power than person-level analysis; ignoring inter-eye correlation underestimates SEs (Glynn & Rosner 2012). [cited in prior project report, not re-opened] — [Glynn & Rosner 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3454458)

### Inferences
- Mapping: segment = instance, person = bag, "any new plaque" = standard MIL assumption. The GLMM version differs from standard noisy-OR MIL in one key way: noisy-OR MIL usually assumes instances independent given features (no b), which is exactly the naive product in §2.3 and overestimates bag risk when instances share a latent susceptibility. The random intercept is the statistical fix; the "leak" in leaky noisy-OR is a cruder fix for unexplained bag positives, not for within-bag dependence.
- In MIL the segment (instance) labels are usually unobserved; here segment labels *are* observed (per-segment reads), so this is supervised multilevel modelling, not weakly supervised MIL. The MIL literature is a precedent for the aggregation rule, not for the estimation.
- Terminology: the GLMM performs partial pooling of person effects (b_i shrinkage) during fitting, and then a separate aggregation step. Calling the aggregation "pooling" invites confusion with partial pooling and with "pooled" (= ignoring clustering) estimators. Recommend defining it once if the codebase name ("pooled engine") is kept.

### Gaps
- No textbook found that names this specific segment→person aggregation for coronary data; dental (tooth/surface→person caries) and ophthalmology are the closest clinical analogues, cited only through the prior project report.
- Multilevel regression and poststratification (aggregating unit predictions to areas) is another aggregation precedent but aggregates *means*, not "any event" probabilities; not researched further.

## 4. Pros and cons vs a direct person-level logistic model ("tree" engine)

### Takeaway
The segment GLMM uses within-person (which segment) and count (how many segments) information that the person-level "any plaque" model discards, so it can estimate geometry effects more precisely; the price is reliance on more assumptions (conditional independence given one b, constant σ across persons, correct segment-level link and covariate forms, correct handling of which segments enter S_i). Its likelihood-ratio test of the geometry block mixes "who" (between-person) and "where" (within-person allocation) information, so a rejection does not by itself show that geometry predicts who.

### Cited Findings
- Collapsing a count of affected units to "any > 0" discards information: negative-binomial count models gave CIs 61–69% as wide as logistic regression on the dichotomised outcome in simulation (36–90% on real data), with gains starting at P(count > 0) ≈ 0.3 under overdispersion. [cited in prior project report] — [Sroka & Nagaraja 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6195979/)
- Random-effects models are probably preferable when interest lies in patient-level predictor effects; but their discrimination advantage needs the cluster effect, which is unavailable for a new cluster. [cited, abstract] — [Bouwmeester et al. 2013](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3658967/)
- Pavlou notes GEE gives population-averaged effects directly, while a random-effects model is preferred when GEE's missing-data assumption is doubtful or conditional predictions are needed. [cited] — [Pavlou et al. 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4525751/)
- Between- and within-cluster covariate effects can differ, and a single coefficient on a cluster-varying covariate is a weighted mix of the two (Neuhaus & Kalbfleisch 1998, Biometrics 54:638–645, doi:10.2307/3109770). [unverified citation]

### Derivations / reasoning [derivation]
- **Where the efficiency comes from.** A person covariate x_i enters every segment's η_ij, so the GLMM sees how x_i shifts the number of affected segments, not only whether ≥1 is affected. A segment-varying covariate z_ij is also identified within person (b cancels in a within-person contrast), which the person model cannot use at all. The prior project's own Fisher-information calculation (σ = 1.5, exchangeable segments) gives ~65–70% retained information for an all-segment effect and ~6% for an effect on 3 of 10 segments; this is a project derivation, not a published result.
- **Confounding of "who" with allocation.** If geometry g_ij varies across segments, the GLMM coefficient on g is driven largely by within-person contrasts (which segment gets plaque), i.e. "where" information. Person risk depends on g only through log S_i = logsumexp_j(η_ij), whose sensitivity to g is weighted by each segment's hazard share. So the GLMM can find a strong g effect that barely moves person-level risk (ΔC ≈ 0), and the LR test of the g block can reject from allocation alone. For person-level covariates (constant across j) there is no within-person variation, and β is purely between-person, but then it is identified also from the *number* of affected segments, which is not the "any" outcome. The prior project error check reports that >90% of the information on the LM-local terms comes from within-person allocation [project derivation].
- **Assumptions the aggregation adds, and what breaks if they fail:**
  1. *Conditional independence given a single b.* If segments within the same vessel share extra dependence (vessel effect), the person-level P(any) is overestimated by a one-b model with the same total marginal segment risks (more dependence → fewer persons with ≥1 event, by the same Harris argument). Remedy: vessel-within-person random effect; still a nested 1-D integral with cloglog.
  2. *Constant σ.* If frailty variance depends on person covariates (e.g. age), person risk is mis-scaled differently across risk groups → calibration slope ≠ 1, not detectable from segment fit.
  3. *Normal b.* Shape of the frailty mostly affects tails; gamma vs lognormal can be compared on person-level calibration.
  4. *Correct segment model and correct segment set.* S_i must sum exactly the segments that define A_i; adding unevaluable or structurally absent segments inflates S_i; omitting outcome-defining segments makes the model under-predict by construction. Informative cluster size (number of evaluable segments related to risk) violates the model.
  5. *Link.* Cloglog closure is what makes S_i a sufficient summary; with a logit segment model the aggregation is still valid via a J-term product inside the integral, but loses the sufficient-statistic form.
- **Direct person-level model ("tree" engine): pros** — fits the target estimand directly; needs no conditional-independence or σ assumption; calibration in-sample is guaranteed for the intercept; robust to segment-level misspecification. **Cons** — discards count and within-person information (lower power for local geometry), must summarise segment geometry by hand (mean, max, etc.), awkward with unequal numbers of evaluable segments.
- **Bridge.** A two-stage recalibration (person logistic on cross-fitted logit P̂_i with free slope, optionally plus SCORE2) tests whether the aggregated risk is on the right scale and whether it under-uses person information; this is the standard logistic recalibration framework applied to aggregated predictions.

### Inferences
- The thesis should present the segment GLMM as more efficient *if correct*, the person model as the robust benchmark, and should not read a GLMM LR rejection as evidence for "who" without the person-level ΔC/calibration estimates.

### Gaps
- No published simulation comparing segment-GLMM aggregation vs direct person logistic for prediction of "any event" in small clusters (J ≈ 9) with large σ was found. Sroka & Nagaraja is count-vs-binary, not clustered binary-vs-person.
- Neuhaus & Kalbfleisch and Zeger–Liang–Albert DOIs not re-verified.

## 5. Evaluating person-level discrimination and calibration for aggregated predictions

### Takeaway
Once each person has one predicted P̂_i and one binary A_i, persons are independent units, so ordinary binary-outcome metrics apply: C-statistic (AUC) on P̂_i, calibration-in-the-large (intercept with logit P̂_i as offset), calibration slope (coefficient on logit P̂_i), calibration curve, Brier score, all computed out-of-fold under person-split CV. Within-cluster C (van Klaveren) is relevant to segment-level "where" discrimination, not to person-level risk.

### Cited Findings
- Calibration-in-the-large: intercept of an intercept-only logistic model with the linear predictor as offset (ideal 0); calibration slope: coefficient from regressing the outcome on the linear predictor (ideal 1; < 1 = predictions too extreme). [cited] — [Pavlou et al. 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4525751/)
- Steyerberg, *Clinical Prediction Models* (2nd ed., Springer 2019, doi:10.1007/978-3-030-16399-0) is the standard reference for these measures and for logistic recalibration. [unverified citation] Van Calster et al. 2016 calibration hierarchy (J Clin Epidemiol 74:167–176, doi:10.1016/j.jclinepi.2015.12.005) [unverified citation].
- In clustered data, concordance can be split into within-cluster and between-cluster; van Klaveren et al. recommend within-cluster C (meta-analysed cluster-specific c-indexes, random-effects meta-analysis) when the model supports decisions within clusters; in the CRASH data cluster-specific c varied (IQR 0.70–0.81). [cited] — [van Klaveren, Steyerberg, Perel & Vergouwe 2014, BMC Med Res Methodol 14:5, doi:10.1186/1471-2288-14-5](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3897966/)
- For small clusters, cluster-specific c-indexes can be too extreme; a calibrated model-based concordance (c-mbc) was less variable with lower RMSE though biased (van Klaveren, Steyerberg, Gönen et al. 2019, Diagn Progn Res, doi:10.1186/s41512-019-0055-8). [cited, search snippet] — [link](https://link.springer.com/10.1186/s41512-019-0055-8)
- Binary C, Brier and calibration are appropriate for current-status data scored at each person's own follow-up time. [cited in prior project error check] — [SAS PROC LOGISTIC doc](https://support.sas.com/documentation/cdl/en/statug/63962/HTML/default/statug_logistic_sect072.htm)

### Derivations / reasoning [derivation]
- **Which scale for the slope.** Logit P̂_i is the conventional recalibration scale. Since the GLMM conditional person model is cloglog in log S_i, one can also regress A_i on log Ŝ_i with a cloglog link; both are valid as long as the scale is stated. Calibration slope of integrated predictions should be near 1 if the model is correct; b = 0 predictions are expected to give slope < 1 (too extreme), the naive product a negative calibration intercept (overprediction).
- **C is blind to the main errors.** For a single σ, integrated risk, b = 0 risk and any monotone transform of Ŝ_i give the same person C. ΔC between engines therefore reflects only ranking differences (covariate effects), and person-level calibration is the only check on the aggregation itself. Calibration should be stratified by number of evaluable segments to detect informative cluster size.
- **Uncertainty.** Out-of-fold metrics from repeated CV vary with the split; a percentile over CV repeats is split variability, not a sampling CI. A person-level (cluster) bootstrap of the whole pipeline is needed for intervals (prior project code review found repeat percentiles ~9× narrower than a person bootstrap on mock data [project finding, simulation only]).
- **Prediction uncertainty for P̂_i** itself: propagate (β̂, log σ̂) via their sampling covariance or bootstrap persons, recomputing the integral each time.

### Inferences
- The thesis text can say: person-level performance is evaluated exactly as for any binary risk model, on out-of-fold P̂_i; the multilevel structure matters for how P̂_i is computed and for resampling (resample persons), not for the metric formulas.

### Gaps
- No source found that specifically evaluates calibration of noisy-OR/frailty-aggregated predictions; recommendations above are an application of standard prediction-model validation to aggregated scores.
- Steyerberg and Van Calster DOIs not re-opened in this session.
