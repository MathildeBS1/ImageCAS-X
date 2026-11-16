# Change log of Thesis_coronary/content/technical/01_mixed_model.tex

Moved out of the header comment of the .tex on 2026-11-16, unchanged. It records every dated edit,
the citation audits and what was cut or moved, up to the review fixes of 2026-11-16 (listed at the end).

```
Technical Background, section 1: the cloglog GLMM and recalibration of a published score.
2026-11-14 (user: "use the best of score2_loglog_explainer.pdf and cloglog_vs_logit.md to write the
  best possible section; limit to 3 pages; additional information in the appendix, like an example of
  how SCORE2 recalibrates itself, as we recalibrate"). Written fresh (user's choice); the committed
  version (bde293e) was only used for cite keys, page locations and labels.
Sources: research_notes/Cloglog versus logit link choice/cloglog_vs_logit.md and
  score2_loglog_explainer.tex (study note). General method only, present tense; no cohort numbers,
  settings or software (Methodology 03).
Citations by location, as checked in the committed version: dobson2002glm Sections 3.4, 7.2 (GLM,
  link), 7.3 (cloglog), 9.2 Eq. 9.3 (offset), 10.2 Eq. 10.4 (hazard, 1 - p = exp(-Lambda)), 10.2.2
  Eqs. 10.7-10.9 (proportional hazards, hazard ratio), 10.2.3 Eqs. 10.12-10.13 (constant or rising
  hazard), 11.1 (clustered outcomes); prentice1978grouped pp. 58-59 Eqs. 2-5 (grouped PH gives
  cloglog), p. 66 (window independence).
score2_2021: SCORE2 Updated Supplementary Material (project root, .docx, read 2026-11-14): Box 1
  (Fine and Gray models), Box 6 (recalibration by intercept and slope), Supplementary Methods
  Table 4 (1 - S0^exp(LP); calibrated risk = 1 - exp(-exp(scale1 + scale2 ln(-ln(1 - risk))))).
Uncited reasoning (algebra): "-log of a product is a sum"; Lambda close to p for rare events; the
  2^gamma reading of the slope; "recalibration keeps the relative weights" closer.
CITATION WANTED: a general recalibration source for eq:tech-recal and calibration in the large
  (e.g. Janssen et al. 2008 J Clin Epidemiol; Steyerberg 2019 Clinical Prediction Models); none in
  refs.bib. The text currently cites only SCORE2's own use of the method.
CHECK (code, for Methodology): CGPS_data/progression_who_pooled.py l.111-112 enters SCORE2 as
  standardised log(SCORE2), not as cloglog(SCORE2) as in eq:tech-recal; score2_honesty.py l.134 uses
  cloglog. The Methodology must describe what the final thesis_final/ code does. The section does not
  decide the open base choice (recalibrated SCORE2 vs refitted factors).
Fine and Gray subdistribution-hazard caveat moved to app:score2-recal (page limit).
2026-11-14 (user): opener "A risk model gives" -> "A prediction model estimates ..., referred to as the risk"; "prediction model" is the TRIPOD term (collins2015tripod, not in refs.bib, no cite needed for the definition), "risk" now defined here.
2026-11-14 (user: "too straight into the GLM"): bridge sentence added (weights, sum, turned into a risk; uncited, as in TRIPOD's "combine multiple predictors by assigning relative weights"); GLM sentence now names the weighted sum.
2026-11-14 (user: "use aida styleguide"): opener rebuilt on Aida's definition opener (style_guide_technical_aida.md 3.1, 8): GLM defined first (kind + task), then its use as a prediction model (risk defined), then structure (weights -> linear predictor). Bridge sentence and the separate prediction-model definition removed.
2026-11-14 (user: "find the best opening, draw on papers and books and the other theses"): opener checked
  against Dobson Section 3.4 (GLM = unifying framework, Nelder and Wedderburn 1972, three parts:
  exponential-family response, linear component x^T beta, monotone link) and Section 7.2 (a linear model
  for a probability "has the disadvantage that ... the fitted values ... may be less than zero or greater
  than one"); Aida Ch. 3 and Esther's bachelor project 3.2 for the definition-first opener (no earlier
  student thesis covers GLMs). Fixed: "designed for outcomes that do not follow a normal distribution"
  (inaccurate, a GLM includes the normal case) -> "extends linear regression to outcomes that need not";
  Bernoulli outcome and p_i introduced before use; beta_0 defined; the reason for the link now cites 7.2.
  Dobson's three parts appear as three consecutive sentences, not as a list.
2026-11-14 (user: "minimise repetition, maximise flow"): "does not follow" (user edit) back to "need not" (grammar; a GLM includes the normal case); Bernoulli and risk merged into one sentence chained by "Such an outcome" -> "this risk"; "event" 4 -> 2 and "probability" 4 -> 1; the two link sentences merged, reason first ("As the linear predictor can take any value"), cites 3.4 and 7.2 together.
2026-11-14 (user: "warmer, need not is not warm"): "that need not follow a normal distribution" -> "that are not normally distributed"; still accurate, as linear regression already covers the normal case and the extension is to the others.
2026-11-14 (user: "dont open with such"): "Such an outcome follows ..." -> "Whether unit i has the event then follows a Bernoulli distribution with probability p_i, referred to as its risk." (picks up "whether an event occurs" from the first sentence).
2026-11-14 (user: "use the best of this to make the best first section, make sure it is general"): opener
  rebuilt from the earlier version (linear regression -> GLM keeps the weighted sum, other distribution;
  Bernoulli for an event in a window) and the study note (risk between 0 and 1, linear predictor any value,
  the link translates "and back again"). Kept from the last version: risk defined, prediction-model use,
  beta_0 as intercept, closer. General only: no SCORE2 or plaque. The observation window is back (the
  cloglog subsection relies on it); "$p_i$ is a probability, but" (sentence opening with a symbol) dropped.
2026-11-14 (user: "sound a bit more academic"): link sentences reworded ("bounded"/"unbounded"; "mapped onto
  the scale ... and mapped back by its inverse", reason first); closer -> "determines the scale on which the
  covariates act additively, and hence the interpretation of the coefficients". Content unchanged.
2026-11-14 (user: "humanise"): link sentence from passive ("the risk is mapped ... by g ... and mapped back by its
  inverse") to active, with g and its inverse as the subjects.
2026-11-14 (user: "make better"): "can be any value" -> "can take any real value"; link sentence now opens
  with "The two are connected by", picking up the two quantities of the sentence before; trailing space removed.
2026-11-14 (user: "easier to understand"): closer -> "The covariates add up on the scale of the link, so the
  choice of link decides what each coefficient means." (stray "th" removed).
2026-11-14 (user: "that was worse"): closer reverted to the academic version (without the stray "th").
2026-11-14 (user: no "thus", "act", "hence"; "warmer, try a rewrite"): closer -> "Choosing a link therefore means
  choosing the scale on which the effects of the covariates add up, and with it what the coefficients describe."
2026-11-14 (user wording): closer -> "The link therefore decides how the coefficients should be understood."
2026-11-14 (user: "use more filler words"): hazard sentence de-compressed: appositive gloss ("the hazard, the rate
  of ...") -> "referred to as the hazard, and it describes, at each moment of the window, how quickly the event
  occurs among the units that have not yet had it" ("rate" no longer repeated).
2026-11-14 (user: "use score2_loglog_explainer.pdf to make a better cloglog subsection, in the style of the section
  before"): rebuilt on the explainer's build-up: the link reached from the risk in three steps ("First, ...
  Subsequently, ... Finally, ..."): risk -> probability of staying event-free -> minus log = cumulative hazard
  (product -> sum) -> second log under PH (product -> sum). Up/down direction kept in one sentence (log twice
  up, exp twice down). Opener names the cloglog link first, as the GLM paragraph names the GLM. Exposure
  paragraph split into shorter sentences. Claims, citations and labels unchanged. Copy before: scratchpad
  01_prediction_model_before_cloglog_rewrite.tex.
2026-11-14 (user: no generic words like "suited", thesis language): cloglog opener -> "arises for an event that can
  occur at any time during the observation window but is recorded only at its end" (grouped-PH wording, Prentice).
2026-11-14 (user: "rewrite the section with the best from this [earlier version]; read the other students'
  technical chapters"): 4.1.1 rebuilt in the earlier version's direct order (hazard -> cumulative hazard ->
  1 - p = exp(-Lambda) -> PH assumed -> inserted -> link), in the register of Aida 3.3.1 ("is used when",
  "assuming", "Under this assumption", "yields") and Esther 3.4 (definition, then formula); Korona and Amalie
  have no technical chapter. Kept from the explainer version: product-over-the-window -> sum sentence, inverse
  link, log twice / exp twice, odds-ratio pointer. Dropped: "three steps" scaffold; "close to p_i when rare"
  (in Appendix B). Copy before: scratchpad 01_prediction_model_before_cloglog_v3.tex.
2026-11-14 (user: "more concise"): hazard / product / minus-log sentences (3) -> 2: hazard defined, then "Summed over
  the window ... 1 - p_i = exp(-Lambda_i)"; the product-to-sum intuition left to Appendix B (0.99^10 example), pointed to.
2026-11-14 (user: "make it more clear that this is one way"): hazard sentence -> "One way to derive a link is to model how the
  risk builds up over the window, through the rate ... referred to as the hazard" (other assumptions give other links).
2026-11-14 (user: "don't these overlap"): opener and "One way" sentence merged into one ("When an event can occur ...,
  one way to derive a link is ..."); the name "complementary log-log (cloglog)" now defined where the derivation yields it.
2026-11-14 (user: "more concise, don't overexplain"): opener -> "For an event that is only observed at the end of the window,
  one way to derive a link is through the rate ... among units still event-free, referred to as the hazard".
2026-11-14 (user: same concise pass): PH sentences -> "Under proportional hazards, each covariate multiplies the hazard by
  the same factor throughout the window, so that Lambda_i = exp(eta_i)." + "Inserting this into 1 - p_i = exp(-Lambda_i) gives ...".
2026-11-14 (user: "mark the assumption clearer and the flow from the former sentences"): PH as an explicit assumption,
  reason first ("To connect the covariates to the hazard, it is assumed that ..., referred to as proportional hazards");
  "The cumulative hazard is then ..."; "inserting it into the probability of no event"; paragraph break removed (one derivation).
2026-11-14 (user): "reached from the risk by taking the logarithm twice" cut (the equation shows it; the model is fitted
  downward, not by transforming outcomes); kept: log cumulative hazard scale and exp twice for a prediction.
2026-11-14 (user): hazard-ratio sentence shortened to the definition; window-length independence and the odds-ratio
  comparison cut here (argument for cloglog over logit, kept in Appendix B with prentice1978grouped p. 66).
2026-11-14 (user): "one-unit increase" -> "an increase of one" (avoids clash with unit i); added that a hazard ratio
  refers to one step on the covariate's scale (year, mm, SD) and is read with that scale; Results must state the
  unit of every hazard ratio (per SD, per mm).
2026-11-14 (user): exposure paragraph tightened from 4 to 3 sentences (offset merged as the special case gamma = 1);
  content and citations unchanged.
2026-11-14 (user): "fixing gamma at 1 gives the special case" -> "when gamma is fixed at 1 instead of estimated, the term is
  referred to as an offset".
2026-11-14 (user: "more concise and to the point"): exposure sentence split in two: term and consequence; offset definition.
2026-11-14 (user): offset sentence opens with "When" (two "With" openers in a row); gamma < 1 (falling hazard) added
  (algebra of Lambda proportional to t^gamma; Dobson 10.2.3 covers the Weibull form).
2026-11-14 (user): window-length reading of gamma (constant / rising / falling hazard) removed here, as exposure is not
  only time; moved as a ready sentence to the notes of methodology/03_prediction_model.tex (log follow-up term).
2026-11-14 (user: "move it all to methodology"): subsection "Recalibrating a Published Score" (sec:tech-recalibration,
  eq:tech-recal) moved to methodology/03_prediction_model.tex as sec:method-recalibration / eq:method-recal, slope
  renamed gamma -> delta (gamma is the exposure coefficient here). The CITATION WANTED and code CHECK above now apply there.
2026-11-14 (user: "make why we are now talking about a random intercept clearer, and why and what GLMMs are used for"):
  subsection renamed "Clustered Outcomes and the Random Intercept"; opens with the GLM's independence assumption
  (Dobson 3.4, "a set of independent random variables"), why it fails for clusters, the GLMM as the answer
  (Dobson 11.1), what "mixed" means (fixed beta + random cluster effects; uncited, standard), and its two uses:
  valid standard errors and a joint model that gives the cluster risk (points to sec:tech-aggregation).
2026-11-14 (user: "go straight into it"; whole section re-read first): 4.1.2 opener cut from five sentences to four:
  GLM independence and why clusters break it in one sentence; GLMM + meaning of "mixed" in one; joint description ->
  cluster risk moved up from between sigma^2 and the frailty; notation list folded into the "where" sentence
  (x_ijk dropped, unused later; Lambda_ij kept, used in H_i).
2026-11-14 (user: "more concise, fit the phrasing and detail of the former two, warm while academic"): 4.1.2
  tightened: first sentence split; "accounts for this by adding ..., in its simplest form an intercept"; "mixed"
  explained after the equation; frailty, conditional beta and sigma^2 estimation as their own short paragraph;
  "often summarised by the median hazard ratio"; nested sentence ends on "although". Claims, cites, labels kept.
  Copy before: scratchpad 01_prediction_model_before_412_tighten.tex.
2026-11-14 (user: "make the fitting and testing section more concise"): quadrature sentences merged; "is compared with
  chi^2_q" dropped (the display shows it); "of the chi^2_1 test" dropped. Claims, cites and labels unchanged.
2026-11-14 (user: "explain better"): cluster-risk sentence now says why the GLMM gives it (it models how the events of
  units in a cluster depend on each other; separate unit risks cannot give it). Dangling "Describing ..." opener removed.
2026-11-14 (user: "make the sentences less ai"): frailty paragraph rewritten: stacked trailing clauses split into short
  sentences; MHR as what it summarises; conditional beta with an example; sigma^2 estimation as cause, then consequence.
  Claims and cites unchanged.
2026-11-14 (user: "more concise, only what the thesis needs"): frailty paragraph 6 -> 4 sentences. Kept: shared frailty
  (e^{b_i} in sec:tech-aggregation), median hazard ratio (planned for reporting sigma^2), conditional beta (reading of the
  geometry hazard ratios), poor estimation of sigma^2 (nine segments, few events). Cut: "Given b_i the units are
  independent" (stated where it is used, sec:tech-aggregation) and the two-units example.
2026-11-14 (user: "best of both worlds"): frailty paragraph keeps the 4-sentence cut but restores "by the same factor",
  "how much the frailty differs between clusters" and the two-units example; "larger than its effect averaged" (wrong for
  beta < 0; ambiguous "which") -> "averaged over clusters a covariate has a weaker effect than beta_k suggests".
Moved to the appendix: cloglog vs logit, the rate reading with a worked example, OR vs HR, and
  "rates add, odds do not" (app:link); SCORE2's recalibration as a worked example (app:score2-recal).
Left to the Discussion: proportional hazards cannot be tested with one follow-up scan; the links are
  indistinguishable by fit at low event rates; a logit refit as sensitivity analysis.
Labels referenced elsewhere, all kept: sec:tech-model, sec:tech-segment-glmm, sec:tech-recalibration,
  sec:tech-nested, sec:tech-glmm-likelihood, sec:tech-aggregation, eq:tech-lp, eq:tech-link,
  eq:tech-cloglog, eq:tech-glmm, eq:tech-lr, eq:tech-agg-conditional, eq:tech-agg-marginal.
  New: eq:tech-recal.
2026-11-15 (user: "explained to be easier understood and move the more technical math into appendix"):
  sec:tech-segment-glmm rewritten in plain steps. Moved to app:link-derivation: 1 - p = exp(-Lambda), the
  proportional-hazards step Lambda_i = Lambda_0 exp(sum beta x), and the link form log{-log(1-p)} = eta
  (eq:tech-cloglog now shows only the inverse). Added a worked hazard-ratio example (1.5 per SD, made up)
  and the doubling reading of the offset (algebra, uncited beyond Dobson 9.2).
2026-11-15 (user: "rewrite 01 in the technical with prognostic association framing, call the file something else,
  keep the most technical part in appendix, limit repetition, look to former students, warmer human tone"):
  file renamed 01_prediction_model.tex -> 01_mixed_model.tex; section title "Generalized" -> "Generalised" (as the
  text spells it). Copy before: scratchpad 01_prediction_model_before_association_rewrite.tex.
  FRAMING (root CLAUDE.md, 2026-11-15): the section is now told around the hazard ratio and the test of a block,
  not around a prediction model. "Used as a prediction model, the GLM estimates this risk" -> "The GLM relates
  this risk to the covariates". The words "prognostic factor" are not used (term open with the supervisor).
  NEW subsection content, sec:tech-glmm-likelihood, now "Adjusted Association and the Test of a Block": what
  "adjusted" means (dobson2002glm Section 9.2: "provided all the other explanatory variables remain the same";
  stated there for the rate ratio of Poisson regression), association is not cause (see CITATION WANTED), the
  95% interval exp(beta +- 1.96 SE) (dobson2002glm Section 9.2 Eq. 9.4, Wald, stated for Poisson regression), and
  the LR test, now cited to dobson2002glm Section 5.7 (difference of deviances of nested models, 2[l1 - l0] ~
  chi2(p - q), "provided that certain independence conditions hold"). All three read in the PDF 2026-11-15.
  MOVED to the new appendix content/appendix/mixed_model_details.tex (app:glmm), text unchanged apart from joins:
  Gauss-Hermite quadrature and Laplace (app:glmm-fitting); poor estimation of sigma^2, the nested random effect
  (label sec:tech-nested moved with it) and the halved p-value (app:glmm-variance); the marginal cluster risk
  (eq:tech-agg-marginal moved with its label), the b = 0 risk and its dependence on sigma^2 and normality
  (app:glmm-risk).
  CUT as repetition: "While events are rare, the cumulative hazard is close to the risk ..." (in
  app:link-derivation); "sigma^2 = 0 returns the GLM"; "the cluster risk keeps the cloglog form, a property the
  logit link lacks" (in app:link-logit).
  ADDED, uncited (plain reading of a definition or of an equation): a hazard ratio of 1 means no difference;
  why the model is called mixed; what the frailty stands for; the reading of the LR test ("if the block adds
  nothing ..."); "one test covers the whole block"; the hazard ratio and the risk answer different questions;
  "or the order of the clusters by risk" (reasoning; the earlier text said only "may barely change the cluster
  risk").
  REWORDED: "averaged over clusters a covariate has a weaker effect than beta_k suggests" -> "the same
  comparison gives a hazard ratio closer to 1" (no "effect"; pavlou2015marginal kept).
  New label: sec:tech-random-intercept (the subsection had none). Subsection sec:tech-aggregation retitled
  "From Association to Risk"; sec:tech-segment-glmm retitled "... and the Hazard Ratio".
  CITATION WANTED: a source for "an adjusted association does not show that changing the covariate would change
  the hazard unless every common cause is among the covariates" (e.g. a prognostic-factor or epidemiology
  reference; none in refs.bib). Uncited reasoning until then.
  CHECK: Methodology 03 must say which interval the final script reports (Wald, as here, or profile).
2026-11-16 (user: "they are not always too small, they can also be too large"): clustering sentence -> SEs too small
  for between-cluster covariates, can be too large for within-cluster ones; cite moved 11.1 -> 11.6 (Dobson 11.6:
  GEE SEs "larger for the intercepts and smaller for the slopes"; 11.1's own example says "over-estimated").
2026-11-16 (user: "apply them, use the example wording"): Dobson states no general between/within rule, so the SE
  sentence now cites it as an example (11.6, Table 11.7: group intercept SE 8.17 pooled vs 9.97 random effects;
  slope SE 1.62 vs 0.66). Correlation sentence cites 11.1; GLMM cite -> 11.1 and 11.5, Eq. 11.11 (shared random
  intercept, Normal responses only).
2026-11-16 (user: "is that wording correct in technical background"): "as in the stroke example of \textcite" ->
  \cite[e.g.][...]: the reader never meets the stroke example, and the chapter states general methods.
2026-11-16 (user: "write this in more of a technical background kind of way"): frailty paragraph -> three paragraphs
  with equations. New labels eq:tech-frailty (Lambda_ij(b_i) = e^{b_i} Lambda_ij) and eq:tech-mhr
  (MHR = exp{sqrt(2 sigma^2) Phi^{-1}(0.75)}, Austin 2017, full text read). Claims otherwise unchanged.
  CHECK: pavlou2015marginal covers marginal predictions in random-intercept LOGISTIC models only; it may not state
  that the marginal HAZARD ratio is closer to 1. Verify, or replace with a frailty source (e.g. duchateau2008frailty,
  not yet opened). The marginal model is also no longer proportional hazards, so "a hazard ratio" there is an average.
2026-11-16 (user: "make it more concise ... easy understanding on the first read ... only the most essential
  equation"): frailty part back to one paragraph of six sentences. eq:tech-frailty dropped (follows from eq:tech-glmm);
  eq:tech-mhr and "MHR of 1 = no difference, same scale as the HRs" moved to app:glmm-variance; MHR kept here as
  words. The CHECK on pavlou2015marginal above still stands.
2026-11-16 (user: "more understandable on the first read ... cut what is not needed ... write only what is done"):
  frailty paragraph rewritten to five sentences: frailty read as "above 1 = more prone", MHR read through an example
  (MHR of 2), conditional HR last. Cut: "The individual b_i are not estimated, only their variance sigma^2" (says what
  is not done; sigma^2 already defined after eq:tech-glmm); "Averaged over clusters ... closer to 1"
  (pavlou2015marginal is logistic only, so the CHECK above is resolved by the cut; conditional vs averaged HRs go to
  the Discussion per Methods 03 notes); the second random effect in the appendix pointer (still in app:glmm-variance).
2026-11-16 (user: "can and should these subsections be made into one ... only describe what is done ... concise,
  look to Aida's technical section"): sec:tech-glmm-likelihood and sec:tech-aggregation merged into one subsection,
  "Adjusted Association, the Test of a Block and the Cluster Risk" (Aida Ch. 3 has at most one subsection per
  section). sec:tech-aggregation kept as an anchor label on the cluster-risk paragraph; equations, citations and
  appendix pointers unchanged.
  CUT: "Whether changing the covariate would change the hazard is a different question ..." (says what the model
  does not do; uncited, so the CITATION WANTED above is resolved by the cut; the causal caveat is owed to the
  Discussion). "This is an association." folded into the sentence before. "One test covers the whole block ..."
  -> "in one step". "A hazard ratio and a risk answer different questions." and the sentence after it (bridge;
  the dilution sentence carries the point). "or the order of the clusters by risk" (uncited reasoning; owed to
  Methods 03 / Discussion if needed).
  REWORDED: "holds only if ..., and otherwise the test rejects too often" -> "relies on the random effects
  capturing the dependence within clusters" (the condition, not the failure).
2026-11-16 (user: "can it just be the fitted model"; "cut the interval sentence"): subsection retitled "The Fitted
  Model". CUT: the two 95% confidence interval sentences (exp{beta +- 1.96 SE}, dobson2002glm Section 9.2 Eq. 9.4;
  "the range of hazard ratios the data are compatible with"), as first-course statistics. Methodology 03 must now
  name the interval itself (Wald or profile, see the CHECK above). The "adjusted" sentences now run straight into
  the test, as one paragraph.
2026-11-16 (user: "match the tone in Aida's section for all sentences in The Fitted Model"): every sentence reworded
  in the register of Aida Ch. 3 (style_guide_technical_aida.md 3.4, 4, 5.1, 5.2, 3.6): "referred to as", "is assessed
  with", "denote", "Under the null hypothesis", "Let ... denote", "Assuming ...", "reduces to", "yields", hazard
  closer with "As a result". Claims, citations, equations and labels unchanged. Two precisions: "hazards" ->
  "cumulative hazards" (Lambda_ij is the cumulative hazard), and conditional independence given b_i is now stated
  as an assumption of the model.
2026-11-16 (user: "replace block with set and apply the citation fixes"; Dobson PDF re-read, Sections 5.7, 9.2,
  10.2.2, 11.7): "block" -> "set" in this subsection (Dobson never says "block"; 5.7 speaks of nested models M0 and
  M1, 2.4 of "a set of explanatory variables").
  CITATIONS: adjusted comparison 9.2 -> 10.2.2 Eq. 10.7 (hazard ratio e^{beta_k} "provided that sum_{i != k}
  x_i beta_i is constant"; 9.2 states it for the rate ratio of Poisson regression). "referred to as adjusted" is now
  its own uncited sentence: the term is not Dobson's in either passage. LR test 5.7 -> 5.7 and 11.7 (5.7: D =
  2[l(b1) - l(b0)] ~ chi2(p - q) "provided that certain independence conditions hold", independent outcomes; 11.7:
  "For multilevel data, nested models can be compared using likelihood ratio statistics").
  CAREFUL: Dobson's q is the number of parameters of the simpler model (df = p - q); here q is the number of added
  covariates.
  CHECK: "block" is still used in the \todonote of Methodology 03 and in the root CLAUDE.md ("geometry block").
2026-11-16 (user: "fix citation issues across the full text"): CITATION AUDIT of every \cite in this file.
  Opened: dobson2002glm (PDF in the repo root; Sections 3.4, 5.7, 7.2, 7.3, 9.2, 10.2-10.2.3, 11.1, 11.5-11.7);
  austin2017mhr (full text on PubMed Central, PMC5299617, read through a web fetch, Section 2.2).
  NOT opened: prentice1978grouped, duchateau2008frailty (no PDF in the repository).
  HOLDS, unchanged: GLM (3.4: exponential-family response, linear component); link (3.4: "monotone, differentiable
  function called the link function"; 7.2: fitted values of a linear model "may be less than zero or greater than
  one"); hazard (10.2); cumulative hazard and S = exp[-H] (10.2, Eq. 10.4 and the line above it); GLM independence
  (3.4: "a set of independent random variables"); correlated outcomes (11.1: "persistent characteristics", "shared
  socio-economic and environmental conditions"; "unmeasured" is my word); MHR (Austin 2.2); LR test (5.7, 11.7).
  FIXED:
  - cloglog: 7.3 gives the name and pi = 1 - exp[-exp(.)] from an extreme value tolerance distribution in a
    dose-response model, not from hazards. Cite moved from the risk equation to the sentence naming the link; the
    equation keeps prentice1978grouped alone.
  - proportional hazards: 10.2.2 -> 10.2.2, Eq. 10.8 (the definition). Dobson never says that the cloglog link
    assumes proportional hazards; that step rests on prentice1978grouped. "Lambda_i = exp(eta_i)" follows from
    log H1 = log H0 + sum x beta (10.2.2, line before Eq. 10.9), with log H0 as the intercept; uncited.
  - hazard ratio: Eqs. 10.7-10.9 -> Eq. 10.7 (e^{beta_k}, "provided that sum_{i != k} x_i beta_i is constant";
    "a one-unit change in a continuous explanatory variable").
  - offset: cite moved from "Doubling the exposure ..." (algebra) to "the term is called an offset". SETTING: 9.2
    defines the offset log n_i, and calls n_i the exposure, for Poisson regression with a log link on the mean, not
    for a cloglog model. gamma log E_i with gamma estimated is not in Dobson (uncited).
  - random intercept: 11.1 and 11.5, Eq. 11.11 -> 11.5. Eq. 11.11 is a Normal model (Y = mu + a_j + e_jk); the
    generalised form g(mu) = X beta + Z u with "binomial for y|u and Normal for u" is unnumbered in the same section,
    which also has "a mixed model with both fixed and random effects". 11.1 does not introduce random effects.
  - frailty: duchateau2008frailty (never opened) -> austin2017mhr Section 2.2: "the term e^{alpha_j} is referred to
    as a frailty term", "The frailty terms have a multiplicative effect on the hazard function". "shared frailty" ->
    "frailty" (Austin does not say "shared"). SETTING: Austin's model is a Cox model with log-normal frailty, not a
    cloglog GLMM.
  - adjusted comparison in sec:tech-glmm-likelihood: second cite of 10.2.2, Eq. 10.7 removed; the hazard-ratio
    sentence in sec:tech-segment-glmm already carries it for the same point.
  CAREFUL (kept): standard errors too small between clusters, too large within, \cite[e.g.][11.6, Table 11.7]. The
    table shows it as one example (difference in intercept: s.e. 8.166 pooled vs 9.966 random effects; slope: 1.143
    vs 0.463). Dobson states no general rule, and 11.1 says the standard deviation of a between-area difference
    "will be over-estimated" under independence, the opposite direction.
  CITATION WANTED: a multilevel text that states the between/within rule for standard errors in general.
  CHECK: prentice1978grouped pp. 58-59, Eqs. 2-5 (the cloglog risk from grouped proportional hazards) was read by an
    earlier session from pasted text and could not be re-opened; PDF requested from the user (papers/).
```

## 2026-11-16, review fixes

The section was reviewed against Aida's Chapter 3 and edited. The list of changes is in the header
comment of `01_mixed_model.tex` (entry 2026-11-16). The version before the edit is this log's last state;
a copy of the full file is in the session scratchpad as `01_mixed_model_before_review_fixes.tex`.
