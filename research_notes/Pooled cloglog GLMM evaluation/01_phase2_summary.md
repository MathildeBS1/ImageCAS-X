# Phase 2: summary of research findings

Coordinator summary of the three researchers' hand-backs (2026-11-11). Detail and sources are in
glmm_weaknesses.md, statistical_alternatives.md and coronary_practice_and_guidance.md.
Total web searches: 21 (7 per strand), plus 4 Europe PMC lookups in strand 3.

## Overall answer so far
No statistical alternative was found that is clearly better than the pooled segment cloglog
random-intercept GLMM as the primary model. The model is defensible for the prespecified block
LR test of geometry, and weaker as a prediction model: nothing shows that a random-intercept
model predicts better for new persons than a model ignoring clustering. Its real role is valid
inference plus a joint model that lets segment risks be aggregated to a person risk.

## Strand 1: weaknesses of the model
- Link: at low segment risk cloglog and logit are indistinguishable in fit; cloglog is justified
  by interpretation only (hazard ratios, closure under "any segment"). The link does matter for
  the aggregated person risk.
- Offset: log length with coefficient 1 assumes hazard proportional to length; no coronary
  precedent found. A free coefficient (1 df) is the defensible default. Curvature and taper
  depend on length, so a wrong offset can leak into the tested block (inference).
- Random intercept: sigma^2 is weakly identified (informed only by persons with two or more
  positive segments). Published small-cluster simulations cover 5 to 100 clusters, not 500+
  clusters of about 9 with rare events, so the bias here is unknown. The person risk depends on
  the whole assumed frailty shape (inference).
- Test: LR test for fixed effects is asymptotic; parametric bootstrap is the stricter check.
  Laplace should not be the primary fit.
- Prediction: with b = 0 calibration is worse than a standard model (Bouwmeester 2013; Pavlou
  2015 slope 0.79 at ICC 0.30); integrated predictions are comparable to standard logistic
  (slopes 0.96 to 0.98). All evidence is logit with large clusters; nobody has validated
  integration to a joint any-event probability.
- Sample size: Riley criteria do not address clustering; count persons and person-level events.
  Three of five geometry features are person-level constants, so segment rows are
  pseudo-replicates for them (inference).
- Independence given the person: no source quantifies adjacent-segment correlation. Most exposed:
  left-main features carried on adjacent pLAD and pLCx rows (inference).

## Strand 2: statistical alternatives (ranked)
1. Person-level cloglog on aggregated geometry: equal for "who"; add as benchmark.
2. Working-independence cloglog GEE with robust Wald test: worse as primary (no joint model for
   the person risk), good sensitivity check on the LR test.
3. Interval-censored or discrete-time frailty model: with two scans it is the same model; use as
   justification. Log follow-up offset = constant baseline hazard; free coefficient = Weibull
   (standard result, not verified in a primary source).
4. Bayesian GLMM with weakly informative priors: equal at best.
5. Vessel-within-person nesting: optional sensitivity, likely singular.
6. Conditional logistic, or between-within terms in the GLMM (+2 df): worse for prediction,
   useful "where" check for confounding by person.
7. Ridge/lasso or Firth-type GLMM: worse; penalisation is least reliable at small samples and
   removes the LR test.
8. Beta-binomial count model: worse.
9. Random slopes, spatial or tree-correlated effects: not feasible.

## Strand 3: coronary practice and guidance (partial coverage)
- Practice: shear-stress IVUS studies use linear mixed models with random patient or vessel
  intercept; binary sub-unit outcomes use a GLMM (link not stated); lesion-level event studies
  use marginal Cox with robust variance (ICONIC, PROSPECT II, snippet level); CCTA cohorts use GEE
  or collapse to the patient.
- No read paper uses a cloglog link, a length offset or pooling of segment risks into a patient
  risk. Absence in a small sample, not a targeted search.
- TRIPOD-Cluster states that repeated measures within individuals are outside its scope, so it
  applies by analogy only: state how clustering was handled and which intercept predictions use.
- Lingsma 2013: of 15 OCT studies with multiple observations per patient, only 5 clearly
  accounted for clustering; recommends multilevel models.
- Verdict: random person intercept and person-level resampling are at or above common practice;
  cloglog, offset and pooled person risk are unusual and need explicit justification.

## Weak points in the evidence
- Strand 3 could not read PROSPECT (2011), published PROSPECT II, EMERALD, PREDICTION, the
  PARADIGM lesion papers, TRIPOD+AI or PROBAST (publisher blocks). Geometry-versus-plaque
  per-segment practice rests on two snippets.
- Many numbers were read through a summarising fetch tool and need checking against the PDFs.
- Several citations are snippet-only or guessed attributions (flagged in the notes).
- No simulation covers the thesis regime (many small clusters, rare events, any-event target).
- Discrepancy to resolve: my brief said 10 to 18 segments per person; the methodology notes say
  nine. Researchers used nine.

## Options for phase 3
A. Write the report now from these notes, with the gaps stated.
B. One extra research round first (allowed once): the coronary practice gaps, and/or a targeted
   search for simulations in the many-small-clusters rare-event regime.
