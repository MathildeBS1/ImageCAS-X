# Statistical modelling of the taper × curvature interaction (low-WSS hypothesis) in the Who and Where models

Scope: how to put "taper and curvature together produce low wall shear stress (WSS)" into (a) the per-person logistic Who model (base = refitted SCORE2 factors) and (b) the per-segment conditional logistic Where model (strata = person, 9 trunk segments, base = position + log length + dominance × vessel), each with one prespecified likelihood-ratio (LR) test of a geometry block. All data are CGPS (Herlev–Østerbro). Sources were searched on the web. Where only bibliographic or secondary snippets were reachable, this is noted. Context from the repo: `CGPS_data/progression_turning.md` (aggregate Medis progression analysis, 1,157 segments, 189 people, 374 progressed) shows single turning terms with OR per SD around 0.85–0.89 (more turning → *less* progression), within-person LR p 0.08–0.98, and no evidence that the turning effect differs between segments (8-df test p = 0.62 / 0.68).

## 1. Options: product term, physics composite, splines/tensor smooths, stratified effects

### Takeaway
Under the parameter budget, the defensible choices are (i) a **single prespecified physics-motivated composite** (1 df, replacing or added to the two main effects) or (ii) **two linear main effects plus one product term** (3 df). Tensor-product splines (≥ 8 df) and stratified effects by segment (8 extra df per feature) are too costly and are better kept for sensitivity or descriptive analyses. No published coronary study was found that combined taper and curvature into one validated index. The composite therefore has to be justified from first principles and stated as a hypothesis.

### Cited Findings
- Riley et al. (BMJ 2020;368:m441) replace events-per-variable rules with criteria for binary outcomes: small overfitting (target shrinkage), a small gap between apparent and adjusted Nagelkerke R², and precise estimation of the overall risk. These are implemented in the R package `pmsampsize` — [Riley et al., BMJ 2020 (Utrecht repository)](https://dspace.library.uu.nl/handle/1874/457642); [pmsampsize manual](https://cran.r-universe.dev/pmsampsize/doc/manual.html)
- Of 119 binary-outcome prediction studies from 2020, only 9 justified their sample size, and 73% of those where a minimum could be computed were below it (Dhiman et al. 2023) — [BMC Med Res Methodol 2023 (DOAJ)](https://doaj.org/article/3a6129ed94174161ad89c5c14fff47aa)
- Harrell's guidance as applied in later work: at most about n/15 total degrees of freedom, with restricted cubic splines (`rcs`) used for continuous predictors. Here n means the limiting sample size; for binary outcomes Harrell uses the smaller of events and non-events — [secondary report of Harrell's rule (hbz-nrw PDF)](https://digitale-objekte.hbz-nrw.de/storage2/2019/08/10/file_25/8681209.pdf)
- RMS contains the sections "Modeling and Testing Complex Interactions" and "Spending Degrees of Freedom/Specifying Predictor Complexity". The `rms` operator `%ia%` gives *restricted interactions*: it drops the nonlinear×nonlinear product terms of a tensor spline, so the interaction is fitted with fewer df — [RMS contents (Scribd copy)](https://www.scribd.com/document/658963927/Regression-Modeling-Strategies); [r-help post by Harrell on %ia%](https://r-mailing-lists.thecoatlessprofessor.com/lists/r-devel/msg/msg-7a20f14f7069); [useR! 2016 tutorial outline: "Why and How To Pre-specify Model Complexity", interaction surfaces](https://user2016.r-project.org/tutorials/00.html)
- Steyerberg-coauthored text: the number of possible interactions grows fast (6 variables → 15 first-order interactions), so a conservative attitude to testing interactions has been proposed. In treatment-effect work, modelling interactions improved discrimination for benefit only when true interactions existed, and it was prone to overfitting (van Klaveren, Balan, Steyerberg, Kent, J Clin Epidemiol 2019) — [Steyerberg chapter (EUR repository)](https://repub.eur.nl/pub/1169/01.pdf); [van Klaveren et al. 2019 (EUR)](https://repub.eur.nl/pub/117959)
- The Dean number, the classic physics composite for curved-tube flow, is De = Re·√δ, with δ the curvature ratio (radius / radius of curvature). It is the ratio of centrifugal/inertial to viscous forces. In a human RCA, measured curvature 25 ± 9 m⁻¹ gave De of 20 ± 8, 46 ± 16 and 93 ± 33 at three flow levels, so De depends on flow (Re) as well as geometry (Krams et al. 1997) — [arXiv 2108.02377 (Dean number definition)](https://arxiv.org/pdf/2108.02377); [Krams et al. 1997 summary (synapsesocial)](https://synapsesocial.com/papers/W2006357156)
- Curvature and WSS direction are contested. In patient-specific coronary CFD, more tortuous vessels had *higher* WSS through helical flow; idealized and patient-specific models diverged, which the authors attributed to curvature imposed by the heart shape (Vorobtsova, Chiastra et al., Ann Biomed Eng 2016;44:2228–39) — [Vorobtsova et al. 2016 post-print](https://iris.polito.it/bitstream/11583/2770474/3/2016%20Vorobtsova%20Chiastra%20-%20Effects%20of%20vessel%20tortuosity%20on%20coronary%20hemodynamics%20POST-PRINT.pdf)
- In left main geometries, average absolute curvature correlated with low time-averaged WSS better than the classical tortuosity index (p = 0.86 for the latter). Another study found the opposite trend — [Accuracy of vascular tortuosity measures, PMC8764056](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8764056/)
- Pig coronaries: helicity intensity was inversely associated with unfavourable WSS (r = −0.91), and torsion dictated helical flow (r = 0.64) (De Nisco et al. 2018, summarized in search results) — [Polimi repository listing](https://re.public.polimi.it/handle/11311/1029992)
- IVUS studies: plaque thickness correlated more strongly with local curvature than with computed WSS (48 segments). The inverse WSS–plaque relation held mainly in cross-sections without luminal narrowing (Wahle et al. 2006) — [Wahle et al. abstract (Iowa)](https://user.engineering.uiowa.edu/~awahle/WahLIT/Abstracts/wahl06a-cfd.html); [Iowa repository record](https://iro.uiowa.edu/esploro/outputs/journalArticle/Plaque-development-vessel-curvature-and-wall/9984020755602771)
- Taper has been examined only in CFD work (e.g., a 2025 preprint varying taper, diameter and plaque position in LAD/LCx/RCA models; not peer-reviewed) — [preprints.org 202510.0781](https://www.preprints.org/manuscript/202510.0781/v1)
- No study was found that defined a composite index merging taper, curvature and Dean number (searched explicitly).

### Inferences
- **Product term (option 1):** 1 extra df on top of the two main effects (3 df in all). It is easy to prespecify and to test. Its weakness is the assumed shape: a linear-by-linear (bilinear) surface. If low WSS needs *both* features to be extreme (a threshold "AND" effect), a product of standardized variables captures it only roughly.
- **Composite (option 2):** the most df-efficient choice (1 df). Its power is high *if* the composite has the right functional form, and lost if it does not. Flow (Re) is not measured on CCTA, so a true Dean number is not available. A purely geometric surrogate is the curvature ratio √(κ·r) (κ = curvature, r = local lumen radius from the tracer contour); a taper-adjusted version could use the distal radius or a local radius. This is a hypothesis-driven construction with no literature precedent for coronary plaque. It should be presented as such, prespecified in writing, and kept in its own dimensionless units.
- **Physics caution (standard Poiseuille reasoning, not from a fetched source):** at fixed flow, WSS ∝ Q/r³, so a narrowing (tapering) lumen *raises* mean WSS distally. Taper alone therefore predicts *higher* WSS, while curvature redistributes WSS (low on the inner wall, high on the outer wall). The sign of the expected interaction is not obvious a priori, which favours estimating a product term over hard-coding a composite whose sign is fixed. The Medis progression results (turning OR < 1) agree with the Vorobtsova "more tortuous → higher WSS" finding and should make the thesis wary of assuming "more curvature = more risk".
- **Tensor-product splines (option 3):** a full tensor product of two 3-knot rcs terms costs 2 + 2 + 4 = 8 df. The `%ia%` restricted version costs about 2 + 2 + 3 = 7 df, and a `te()`/`ti()` smooth in mgcv uses penalized effective df. All of these exceed what a modest number of discordant events in a clean, plaque-free cohort can support, so they suit a sensitivity analysis or a descriptive figure (a predicted log-odds surface) rather than the primary test.
- **Stratified effects (option 4):** an effect of curvature per vessel or per segment costs 2–8 df per feature. The Medis progression analysis already found no heterogeneity across segments (p ≈ 0.6). For the Where question, stratifying by vessel (3 levels, 2 extra df) is the most that would be affordable.
- **Recommendation:** primary geometry block = linear (or log-transformed) curvature + taper + their product, plus the other prespecified geometry terms. Alternatively, use the composite *instead of* the product if the thesis commits to a physical hypothesis before seeing outcome data. Show the tensor surface as a secondary, descriptive figure.

### Gaps
- No full text of Harrell RMS §2.7.2 was retrieved, so the exact df guidance for interaction surfaces is from the table of contents and secondary sources.
- No coronary CCTA study using a taper × curvature product term or a validated geometric WSS surrogate in a regression model was found.
- The actual number of clean-baseline events in CGPS (and hence the Riley budget) was not computed here; it lives in `who_where_readiness.py` outputs on dtu-gpu-7.

## 2. Centring, scaling, within-person centring in clogit, and identifiability with 9 segments per person

### Takeaway
In the clogit Where model, any segment-varying variable, and the product of two such variables, is identifiable. Person-constant terms drop out. However, the **raw product taper × curvature in clogit is not a pure within-person interaction**: it mixes the within × within interaction with two cross-level terms. Prespecify within-person-centred main effects and the product of the *within-person deviations*, or state that the raw product is used and what it means. Effective information comes only from persons with at least one but not all segments with new plaque.

### Cited Findings
- Conditional likelihood methods estimate within-cluster effects of individual-level covariates but not effects of cluster-level covariates, which do not vary within clusters — [Begg & Parides 2003, Stat Med 22:2591–2602, as discussed on Statalist](https://stata.com/statalist/archive/2003-11/msg00258.html)
- Within- and between-cluster effects of a subject-level covariate can differ, and assuming they are equal can bias results. Neuhaus & Kalbfleisch (Biometrics 1998) proposed separating exposure effects into within- and between-cluster effects — [IBC 2006 abstract, Goetgeluk & Vansteelandt](https://www.jhanley.biostat.mcgill.ca/IBC2006/Abstracts/pdf/666.pdf); [Neuhaus & McCulloch summary](https://academicnewsletter.sufe.edu.cn/info/442170)
- Conditional ML removes bias when cluster random effects are correlated with a predictor. Partitioning the covariate into between- (cluster mean) and within- (deviation) components also removes it (Neuhaus & McCulloch 2006, JRSS-B) — [summary](https://academicnewsletter.sufe.edu.cn/info/442170)
- Within-subject centring (van de Pol & Wright 2009) separates within- from between-subject effects in mixed models and is distinct from grand-mean centring — [JCU repository](https://researchonline.jcu.edu.au/80096/)
- Marginal models with pair-level means can give more efficient within-pair estimates than clogit, at the cost of extra functional-form assumptions — [Victorian Centre for Biostatistics talk](https://www.vicbiostat.org.au/node/1031)
- A matching (stratum) variable cannot enter a clogit on its own but can enter as an interaction with a within-stratum-varying term. Detecting such effect modification needs large totals — [r-help thread](https://stat.ethz.ch/pipermail/r-help/2011-June/280783.html); [MetricGate clogit notes](https://metricgate.com/docs/clogit-stratified-matched/)
- The CRAN package CLRtools offers LR tests for interactions in clogit — [CLRtools vignette](https://cran.r-project.org/web/packages/CLRtools/vignettes/Conditional_Logistic_Regression.html)

### Inferences
- **Algebra of the raw product in clogit.** Write x = x̄ᵢ + x̃ᵢⱼ and z = z̄ᵢ + z̃ᵢⱼ (person mean + within-person deviation). Then x·z = x̃z̃ + x̃·z̄ᵢ + x̄ᵢ·z̃ + x̄ᵢz̄ᵢ. The last term is constant within a person and is absorbed by the stratum. The coefficient on raw x·z therefore forces one common coefficient onto (a) the pure within-person interaction x̃z̃ and (b) two cross-level modifications ("the within-person effect of taper is larger in people whose segments are on average more curved"). These are different hypotheses. Options:
  1. **Pure within (recommended for Where):** enter x̃, z̃ and x̃·z̃ (deviations from the person's mean over that person's available trunk segments). In clogit the main-effect coefficients of x̃ and x equal each other, since the person mean is absorbed. Only the product changes.
  2. **Raw product:** acceptable if stated, but its interpretation is a blend.
  3. Adding x̃·z̄ and x̄·z̃ separately costs 2 more df and is not recommended under the budget.
- **Segment-type confounding:** curvature and taper differ systematically by segment (e.g., distal vs proximal). Deviations from the person mean still carry segment-position differences, which the base model's position terms adjust for. An alternative is to centre each feature on its *segment-specific cohort mean* (and scale by the segment-specific SD) before the within-person decomposition, so "high curvature" means high *for that segment*. This matches the base model's logic and makes the product term less collinear with position. It is a prespecification choice.
- **Scaling:** standardize each feature (z-score, or after a log transform for right-skewed curvature) *before* forming the product. Report ORs per SD. Then the main-effect coefficients are effects at the mean of the other variable. Fit the scaling inside each cross-validation training fold (person-split) to avoid leakage.
- **Identifiability with 9 segments:** with 9 segments per person and 3 continuous within-varying terms (x̃, z̃, x̃z̃) plus the base, the model is identified provided segment geometries vary within persons. Precision, however, rests on *discordant* strata (persons with new plaque in 1–8 of their 9 segments); persons with 0 events, the majority in a clean cohort, contribute nothing. The effective sample size for the Where interaction is roughly the number of plaque segments in discordant persons. Check collinearity: if taper and curvature are strongly correlated within person, the product is close to a quadratic in one variable and poorly separated. Report the within-person correlation.
- **Who model:** geometry must be summarized per person (e.g., the person mean over trunk segments, or a max/percentile). The between-person interaction (person-level taper summary × person-level curvature summary) is a different estimand from the within-person one. The thesis should say that Who and Where test different interaction estimands, and that a null in one does not contradict the other.

### Gaps
- The full texts of Neuhaus & Kalbfleisch (1998) and Begg & Parides (2003) were not retrieved, so details are from citing sources. Bibliographic details: Neuhaus JM, Kalbfleisch JD. Biometrics 1998;54:638–645; Begg MD, Parides MK. Stat Med 2003;22:2591–2602.
- No paper was found that treats within × within versus cross-level product terms specifically in clogit. The decomposition above is the author's algebra, to be checked by the thesis supervisor.
- No source was found on sample size or power for interaction terms in clogit with few segments per stratum. The Riley criteria are for unconditional models.

## 3. Summarizing pointwise curvature and taper to a segment value

### Takeaway
Prespecify **one** summary per feature. Mean absolute curvature has the best literature support as a correlate of low WSS. For taper, use a signed, length-normalized radius slope (e.g., a regression slope of log radius on arc length). Max or fraction-above-threshold summaries are noisier and threshold-dependent. Trying several variants inflates type I error, as the Medis progression table already shows (six variants, "expect about one p < 0.05 by chance").

### Cited Findings
- Average absolute curvature correlated better with low TAWSS than the classic tortuosity index (p = 0.86 for the latter) and was recommended for future studies — [PMC8764056](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8764056/)
- Circumferential plaque distribution depended on *local* curvature in most vessels, and the effect increased with curvature (Wahle et al. 2004, 37 segments) — [Wahle 2004 abstract](https://user.engineering.uiowa.edu/~awahle/WahLIT/Abstracts/wahl04a-cfd.html)
- Torsion as well as curvature drives helical flow, and helical flow raises WSS — [Vorobtsova et al. 2016](https://iris.polito.it/bitstream/11583/2770474/3/2016%20Vorobtsova%20Chiastra%20-%20Effects%20of%20vessel%20tortuosity%20on%20coronary%20hemodynamics%20POST-PRINT.pdf); [De Nisco et al. via Polimi](https://re.public.polimi.it/handle/11311/1029992)
- Carotid geometric risk-factor work (Steinman group) reduced many correlated geometric variables with factor analysis and predicted relative hemodynamic risk with sensitivity/specificity up to 0.84. The incremental value of geometry over conventional risk factors for wall thickness was questionable (ARIC carotid MRI) — [Friedman/Steinman search summary; ARIC proposal](https://aric.cscc.unc.edu/aric9/system/files/aricprops/priv/MP2040.pdf); [carotid geometry thesis (CORE)](https://core.ac.uk/works/81075242)
- Repo evidence (aggregate): mean T5, 90th-percentile T5, fraction above p75, T2.5, T10 and upstream-20 mm turning gave similar ORs (0.85–0.98); the variants are highly redundant — `CGPS_data/progression_turning.md`

### Inferences
- **Curvature:** mean absolute curvature over the segment, computed at a fixed smoothing scale chosen *before* outcome data (the Medis work suggests T5 ≈ 5 mm). Log-transform if skewed.
- **Taper:** signed slope of log(radius) or of equivalent diameter against arc length (−d ln r/ds), which is dimensionally 1/length and comparable across segment lengths. Signed, because flaring segments (negative taper) and tapering segments differ physically: local flow deceleration in a widening lumen is the classic low-WSS situation. Keep the base model's log length term so that taper is not a length proxy.
- **Interaction at the right scale:** if low WSS is a *local* phenomenon (a high-curvature point in a widening stretch), a segment-level product of two means can miss it. A prespecified alternative is to compute the pointwise product κ(s)·(taper(s)) or the pointwise composite and then summarize it (mean over the segment). This is still 1 df and closer to the physics. The choice must be made before seeing outcomes.
- Avoid max and fraction-above-threshold as primary summaries. They depend on tracer noise at single points and on an arbitrary threshold.

### Gaps
- No coronary study comparing mean, max, percentile and fraction-above-threshold summaries for *taper* was found.
- How reproducible the tracer's pointwise radius is (which drives taper noise) is not established here; it belongs to the Medis validation chapter.

## 4. Fitting the interaction into the "one LR test of the geometry block" rule

### Takeaway
Put the interaction (or the composite) **inside** the prespecified geometry block, so that the single LR test has df = number of block terms, *or* keep the block main-effects-only and declare the interaction a **secondary, separately reported** LR test (block + product vs block). The first choice preserves the one-test rule. The second adds a test, which then has to be labelled exploratory. Either way, write it down before unblinding the outcome.

### Cited Findings
- Harrell recommends prespecifying model complexity (df allocated per predictor) before modelling, and testing complex interactions as pooled chunks — [useR! 2016 tutorial outline](https://user2016.r-project.org/tutorials/00.html); [RMS contents](https://www.scribd.com/document/658963927/Regression-Modeling-Strategies)
- A conservative attitude to testing interactions is recommended in prediction modelling — [Steyerberg chapter](https://repub.eur.nl/pub/1169/01.pdf)
- LR tests of each interaction against the main-effects clogit model are standard (CLRtools `check_interactions()`) — [CLRtools vignette](https://cran.r-project.org/web/packages/CLRtools/vignettes/Conditional_Logistic_Regression.html)

### Inferences
- **Option A (consistent with the decided design, recommended):** geometry block = {curvature, taper, curvature × taper, LM bifurcation angle, LM→LAD ratio, LM→LCx ratio} for Who; for Where, the segment-varying subset {curvature, taper, product} plus any segment-level ratios that vary within person. LM-level features (bifurcation angle, LM ratios) are person-constant in clogit and **drop out of the Where model** unless they are interacted with vessel (e.g., LM→LAD ratio × LAD-segment indicator). That is itself a design decision to flag. One LR test with k df. Cost: adding the product spends 1 df, which slightly lowers the power of the block test if the interaction is null.
- **Option B:** geometry block = main effects only (primary test). Interaction = a secondary LR test, reported with its estimate and CI, labelled exploratory. This changes the decided design only by adding one secondary test.
- **Option C:** replace curvature and taper with the 1-df composite in the block. This saves 1 df versus the main effects and 2 df versus Option A, but changes what "geometry" means in the primary hypothesis. Flag to the supervisor that this alters the decided block.
- ΔC and calibration for the model with the product term are estimated in the person-split CV as already planned. Interaction terms usually add little to the C-statistic even when "significant", so expect ΔC ≈ 0.
- Hierarchy: never include the product without both main effects (unless using the composite). Report the main effects as conditional effects at the mean of the other variable.

### Gaps
- No source was found that addresses "one global LR test including an interaction" specifically in a prespecified prediction or added-value framework. The advice above follows from Harrell's chunk-test principle.

## 5. Interaction on the log-odds (multiplicative) scale vs the additive scale; reporting

### Takeaway
Logistic and clogit models estimate the interaction on the multiplicative (odds-ratio) scale. Report the product-term ratio of ORs with its CI. Following Knol & VanderWeele, also report the effect of one feature at low/high levels of the other, and, for the Who model only, an additive-scale measure (RERI on predicted risks), since low WSS "acting jointly" is a biological-interaction claim that is properly judged on the additive scale. RERI cannot be obtained from the conditional Where model, which has no absolute risks.

### Cited Findings
- Knol & VanderWeele (IJE 2012) recommend reporting both multiplicative and additive interaction measures with CIs. They present the effect of each exposure within strata of the other, and they note that earlier proposals did not distinguish effect modification from interaction or give CIs for both scales — [PMC3324457](https://pmc.ncbi.nlm.nih.gov/articles/PMC3324457); [KI copy PDF](https://www.meb.ki.se/biostat/Sing2022/papers/Session1/Knol&vanderWeele_IJE_%202012_presenting_effect_modification.pdf)
- RERI, AP and the synergy index are additive measures, implemented for two binary exposures in the R package `interactionR` — [interactionR manual](https://tunsmart.r-universe.dev/interactionR/doc/manual.html)
- Interactions for spline-modelled continuous variables can be summarized with `interactionRCS` (ORs at chosen values of the modifier) — [interactionRCS](https://r-packages.io/packages/interactionRCS)

### Inferences
- **Who:** report OR per SD of taper at curvature = −1 SD, mean and +1 SD (and vice versa). Report the product-term exp(β) as a ratio of ORs. Optionally, report RERI for "high/high vs low/low" (e.g., top vs bottom tertile, predicted from the continuous model) using the absolute risks from the refitted model, which is consistent with Knol & VanderWeele.
- **Where:** only the multiplicative scale is available, since clogit conditions out the baseline odds. Report conditional ORs and a within-person risk-ranking illustration (e.g., the within-person C, as in the Medis analysis).
- A figure of the predicted log-odds surface over (curvature, taper), with the data density overlaid, is the most transparent display, whichever parametrization is tested.

### Gaps
- Knol & VanderWeele's examples are for binary exposures. Extending RERI to continuous standardized features needs chosen contrast values, and no specific source for coronary geometry was found.

## 6. Precedents: physics-informed composite predictors vs flexible interactions

### Takeaway
Arterial-geometry epidemiology has used both approaches. "Geometric risk factors" (Friedman) are motivated by hemodynamics, but in practice they were reduced to a few variables by factor analysis or entered as main effects, and their added value over conventional risk factors has been modest or questionable. Physics composites (Dean number, curvature ratio) are standard in fluid mechanics but need flow data that CCTA lacks. No coronary-plaque regression precedent for a taper–curvature composite was found.

### Cited Findings
- Friedman's "geometric risk factor" hypothesis: arterial shape sets the wall's hemodynamic environment, and geometric features that raise harmful wall stresses act as local risk factors (Johns Hopkins APL Tech Dig 1983). It was later tested against human coronary histopathology (1995) — [Friedman 1983 PDF](https://secwww.jhuapl.edu/techdigest/Content/techdigest/pdf/V04-N02/04-02-Friedman.pdf); [Springer chapter](https://link.springer.com/doi/10.1007/978-3-642-69085-3_9); [Duke record](https://scholars.duke.edu/publication/684409)
- Carotid bifurcation studies used factor analysis to condense correlated geometric variables into a few factors predicting hemodynamic risk (sensitivity/specificity up to 0.84). In ARIC, geometry predicted wall thickness, but its added value over risk factors was questionable — [ARIC proposal MP2040](https://aric.cscc.unc.edu/aric9/system/files/aricprops/priv/MP2040.pdf); [CORE record](https://core.ac.uk/works/81075242)
- The Dean number is the canonical dimensionless composite of curvature and flow. In a human RCA it spanned 20–93 depending on flow level, so it is not a pure geometry measure — [Krams 1997 summary](https://synapsesocial.com/papers/W2006357156); [arXiv 2108.02377](https://arxiv.org/pdf/2108.02377)
- Composite tortuosity indices (classic tortuosity index) performed worse than a simple curvature average at predicting low WSS. A mechanistically appealing composite is therefore not guaranteed to beat simple measures — [PMC8764056](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8764056/)
- Flexible modelling of interactions in prediction can improve discrimination when true interactions exist but overfits otherwise — [van Klaveren et al. 2019](https://repub.eur.nl/pub/117959)

### Inferences
- With limited events, a prespecified 1-df composite is the strongest choice *only if* its form is right. The literature (curvature direction contested, taper's role CFD-only, no flow data) does not pin down the form. The product term is the safer prespecified middle ground: it estimates the sign and costs 1 df.
- A pragmatic, citable framing for the thesis: "We prespecified a bilinear taper × curvature term inside the geometry block, motivated by the hemodynamic geometric-risk-factor hypothesis (Friedman). The physics composite (curvature ratio, a flow-free Dean-number surrogate) and a tensor-spline surface were evaluated as sensitivity analyses."
- Any composite must be computed from tracer lumen and centerline only, with no Medis inputs, since Medis is a reference, not ground truth.

### Gaps
- No CCTA-based coronary study using a geometric WSS surrogate as a regression predictor for incident plaque was found in this search. A targeted PubMed search (e.g., "curvature ratio" OR "geometric shear surrogate" AND CCTA) might find one.
- No source was found that compares, in biostatistics generally, physics-derived composite predictors with flexible interaction terms for power.
