# Cloglog versus logit link for the pooled segment plaque model

Scope: why the segment-level GLMM uses a complementary log-log (cloglog) link instead of a logit link, and whether that was right. Local project files were read first (paths and line numbers given). Web sources were few and mostly secondary, so each one is graded. "[own computation]" marks numbers I computed here; they are not from a source.

## (A) What reasoning for cloglog does the project record?

### Takeaway
The project gives three reasons. First, cloglog is the grouped-time proportional-hazards model, so exp(β) is a hazard ratio that does not depend on interval length. Second, and this is the main technical reason, under cloglog the product of segment survival probabilities collapses to exp(−e^b·S_i). The person risk then becomes a one-dimensional integral over the random intercept, and the logit link has no such form. Third, SCORE2 has a natural home on the cloglog scale. The project's own evaluation is open that model fit cannot tell the links apart at segment level, that the reason for cloglog is interpretive, and that a logit refit is a planned sensitivity analysis. Log follow-up enters the code as a **covariate with a free coefficient, not an offset**.

### Cited Findings
- **The code (current state).** `CGPS_data/progression_who_pooled.py` l.11–14: "a segment-level cloglog GLMM with a person random intercept b ~ N(0, s^2) … pooled to person risk P_i = 1 − ∫ exp(−e^b Σ_j exp(η_ij)) φ(b; 0, s²) db". l.103 builds the design as `[np.ones(len(d)), np.log(d["years"])]` with name "log follow-up", so log follow-up is an ordinary column with an estimated coefficient. No `offset` appears in `design()`. l.118 adds log length as a covariate too, not as an offset. l.567 prints "cloglog. exp(β) is a hazard ratio for the segment". `years` is the BL-to-FU scan-date difference (`CGPS_data/progression_turning.py` l.84). Rows with years ≤ 0 are dropped (l.473). — local file
- **Caveat on the code.** Its docstring (l.7–9) says the rows are "the 9 split … segments of each **Medis tree**" and the segment outcome is a "higher grade at FU than at BL", that is, progression in the Medis (plaque-at-baseline) set. It is not yet the incident-plaque model on the plaque-free cohort. The link logic carries over, but the script as it stands is not the thesis's final who model. — local file
- **Is follow-up variable? Yes, moderately.** "Follow-up varies only by about ±12% (IQR 9.7–12.2 years)" — `~/Desktop/Speciale/CGPS_statistics-/reports/Experiment setup who and where.md` l.23. In the clean cohort, a person-level cloglog model with **follow-up alone** reaches out-of-fold C = 0.560. The refitted-factor model gives log follow-up an HR of 1.19 per SD (95% CI 1.08–1.31) — `CGPS_data/score2_honesty.md` §3–4. — local file
- **Reason 1, grouped PH.** The thesis text (`Thesis_coronary/content/technical/01_prediction_model.tex` l.272–287) states proportional hazards, "exp(β_k) is the hazard ratio", and "the hazard ratio does not depend on how long the window is \cite{prentice1978grouped}". Exposure enters as γ log E with γ free; the offset is the special case γ = 1. — local file
- **Reason 2, collapse of the person risk (the decisive one).** "Under cloglog, 1 − p_ij(b) = exp(−e^b e^{η_ij}), so the product over segments collapses to exp(−e^b S_i) … The logit link has neither property, because a product of logistic survival terms is not logistic." — `~/Desktop/Speciale/CGPS_statistics-/reports/Segment model to person risk.md` l.9. The same point is made in `experiments/who/pooled_score2/pooling.md` ("With the cloglog link, the segments collapse into one number, S_i. The integral is over one dimension only") and in `reports/Plaque risk model choice.md` l.49 ("The participant hazard is the sum of the segment hazards, so the rolled-up model is again cloglog … The logit link has no such closed form"). — local files
- **Reason 3, SCORE2 scale.** `CGPS_data/score2_honesty.md` §4: "Slope of plaque cloglog on cloglog(SCORE2 risk). Both are log cumulative hazards." The estimated slope is 0.722 (0.569–0.874). — local file
- **The project's own honest assessment.** In the thesis notes (`01_prediction_model.tex` l.95–99): "Say honestly that fit cannot tell the links apart at segment level; the reason for cloglog is interpretive (hazard ratios, segment hazards add to a person hazard). The link does matter for the person risk, which is not small." `reports/Pooled cloglog GLMM evaluation.md` l.28 rates cloglog versus logit "Low [impact] for coefficients and the test; matters for the person risk", with a "Logit refit as sensitivity" (l.81, item 6). The same report (l.13) says no coronary paper it read uses a cloglog link. — local files
- **History: the link was once the other way round.** `reports/Experiment setup who and where.md` l.3 and l.23 (an earlier report) proposed **person-level logistic regression with log follow-up as primary** and cloglog with a log(t) offset as the sensitivity analysis. The switch to cloglog as primary came with the decision to use the pooled segment model. — local file
- **Survival reading recorded.** "A free log follow-up coefficient is a Weibull grouped-PH baseline" — `reports/Person risk pooling error check.md` l.11. The thesis notes l.103–104 say the same but mark it "VERIFY in prentice1978grouped before writing". "PH cannot be tested with one follow-up scan; say so" (l.104–105). — local files
- **Risk levels in the cohort.** Of the 1,077 plaque-free people, 483 (44.8%) developed plaque anywhere. 452 of 1,076 (42.0%) developed it in one of the 9 artery segments (LAD, LCx, RCA proximal/mid/distal). In complete cases it is 433/1,041 (41.6%); median SCORE2 risk is 0.026 — `CGPS_data/score2_honesty.md` §2; `research_notes/Models to beat pooled cloglog GLMM/thesis_context.md` l.42–49. The **segment-level event rate has not been tabulated** on the 1,801-person table (`reports/Pooled cloglog GLMM evaluation.md` l.33). — local files

### Inferences
- The recorded justification is sound in structure. The collapse argument is the one reason that is specific to this design and cannot be matched by logit. The hazard-ratio interpretation is a bonus.
- One local text is slightly inconsistent. Several notes say "offset or free coefficient", but the code uses a free coefficient on log follow-up (and on log length). The thesis methods must say "covariate with an estimated coefficient (grouped Weibull baseline)", not "offset". Under the current code, the "invariant to interval length" claim holds only conditionally on that Weibull form (see B).
- A rough check of the constant-hazard reading [own computation, assumption-laden]: if log follow-up is roughly normal with IQR log(12.2/9.7) = 0.229, its SD is about 0.17. HR 1.19 per SD then corresponds to a coefficient of about log(1.19)/0.17 ≈ 1.0 on log time, which is what a constant hazard (offset) predicts. This is only indicative: the SD of log follow-up is not reported, the model is person-level and not the GLMM, and follow-up time may be confounded with recruitment date or age.

### Gaps
- Segment-level incident-plaque rate, and the number of people with ≥2 positive segments, in the plaque-free cohort: not computed locally.
- No local file reports a fitted logit-versus-cloglog comparison (AIC, log-likelihood, C) for any model.
- `research_notes/Pooled cloglog GLMM critical audit/` exists but is empty.

## (B1) Theory: is cloglog the grouped / interval-censored PH model, and what does that buy over logit?

### Takeaway
Yes. If plaque onset follows a continuous-time proportional-hazards model and is observed only as "by the follow-up scan or not", then P(event) = 1 − exp(−Λ0(t)·e^{xβ}). That is exactly a cloglog binary regression, and β is the PH log hazard ratio (Prentice & Gloeckler 1978). With a logit link, exp(β) is an odds ratio. Odds ratios match hazard ratios only at low risk, and an OR depends on the baseline risk and therefore on interval length. In this cohort the difference is small at segment level but real at person level.

### Cited Findings
- Prentice & Gloeckler (1978), "Regression Analysis of Grouped Survival Data with Application to Breast Cancer Data", *Biometrics* 34(1):57–67, doi 10.2307/2529588. It proposes a grouped-data version of Cox's PH model — [scilit record](https://scilit.com/publications/994d0738ce096f9417692845dca7b7f0) (record only; full text not read).
- SAS documentation: the grouped-data model is "equivalent to the binary response model with complementary log-log link function". It is "a discrete analog of the continuous proportional hazards model (Prentice and Gloeckler 1978; Allison 1982)", with λ_ij = 1 − exp(−exp(α_j + β′x_i)). The β vector "is identical to that of the continuous-time proportional hazards model" — [SAS PROC LOGISTIC example](https://go.documentation.sas.com/api/docsets/statug/v_023/content/statug_logistic_examples19.htm) (reliable software documentation).
- Rodríguez (Princeton GLM notes): the cloglog model "can be obtained by grouping time in the continuous-time proportional-hazards model". It "do[es] not need to assume that the hazard is constant in each interval", and its results "should be more robust to the choice of categories". Cloglog "would seem more appropriate" when time is continuous but observed grouped. Logit is "used much more often", largely because of software — [Rodríguez, c7s6](https://grodri.github.io/glms/notes/c7s6) (reliable lecture notes).
- Current-status data: log-log link ↔ proportional hazards, logit ↔ proportional odds — [Jewell & van der Laan review, UC Berkeley WP 113](https://biostats.bepress.com/ucbbiostat/paper113) (abstract only read; the PH/cloglog statement comes from secondary search snippets citing it, so verify).
- Interval-censored caveat: the cloglog grouped approach "requires that the intervals are somewhat consistent across subjects" — [CTSPedia](https://ctspedia.org/ctspedia/intervalcensoredanalysis) (practitioner wiki, weak).
- OR versus RR/HR: odds ratios approximate risk ratios when the outcome is rare and can diverge substantially when it is common — VanderWeele 2020, *Biometrics* 76(3):746–752 — [IDEAS record](https://ideas.repec.org/a/bla/biomet/v76y2020i3p746-752.html) (record only). Dichotomised time-to-event methods differ importantly when follow-up and censoring vary — [Salika/Fisher et al. 2022, BMC Med Res Methodol](https://discovery.ucl.ac.uk/10145997/1/Fisher_s12874-022-01541-9.pdf) (not opened this session; cited locally in the setup report).
- Within the Aranda-Ordaz family, the cloglog effect measure is claimed always to approximate the risk ratio better than the OR — [Tsubota & Beppu 2025, arXiv 2506.00889](https://arxiv.org/abs/2506.00889v1). **Preprint, not peer-reviewed.**
- Size of the OR–HR gap at this cohort's risk levels [own computation, assuming PH holds]:
  - Baseline risk 2%: HR 1.5 gives OR 1.51.
  - Baseline risk 6%: OR 1.52.
  - Baseline risk 15%: OR 1.56.
  - Baseline risk 42% (the person level): OR 1.75.
  - Interval dependence: same HR 1.5, constant hazard, 42% risk at 11 years. The implied OR is 1.71 at 9.7 years and 1.78 at 12.2 years, so it drifts by about 4% across the IQR of follow-up.

### Inferences
- **At segment level the choice barely matters for β.** If the segment risk is the person risk spread over 9 segments, it is likely below about 10–15%. There an OR and an HR differ by under ~5% for moderate effects. The local notes are right that segment-level fit will not discriminate the links. (The segment rate is still untabulated.)
- **At person level the links differ.** At 42% the two scales differ by roughly 15% for an HR of 1.5. That matters for (i) what the pooled person risk is and (ii) how calibration of the person risk behaves. It does not matter much for the person-level C.
- **Interval-length invariance is a modest practical gain here.** Follow-up spans only ±12%, so an OR would drift little. The stronger practical gain is that cloglog makes "risk at a fixed 10-year horizon" a clean extrapolation through the time term, and that SCORE2 is itself a 10-year risk with a log-cumulative-hazard structure (local §A).
- **The "invariant" claim needs a qualifier given the code.** With log t as a free covariate (coefficient κ), Λ0(t) ∝ t^κ, a grouped Weibull baseline. The HR is then constant over t only if PH holds and that time form is right. With a single scan per person, the data cannot separate "non-PH" from "wrong baseline shape" (see B3). "Weibull" is my derivation (standard: log Λ0(t) = log λ + κ log t), not verified in Prentice & Gloeckler.

### Gaps
- Prentice & Gloeckler 1978, Allison 1982, Singer & Willett 2003, Tutz & Schmid 2016 and Finkelstein 1986 were not opened (paywalled or books). Statements attributed to them rest on SAS/Rodríguez documentation and well-known results.
- No source found that directly quantifies OR drift with interval length; the numbers above are my own.

## (B2) Does the HR interpretation survive in the GLMM, and does the pooling fit cloglog naturally?

### Takeaway
Partly. Conditional on the person intercept b_i, exp(β) is a conditional (within-person, frailty-adjusted) hazard ratio. e^{b_i} is a lognormal shared frailty multiplying all nine segment hazards. Averaged over b, the marginal segment model is no longer exactly PH with the same β: marginal effects are attenuated, as in any frailty model. The pooling 1 − E_b[exp(−e^b S_i)] is exactly the shared-frailty survival function evaluated at the summed cumulative hazard, and it exists in closed one-dimensional form only because of cloglog. Note that the naive 1 − ∏(1 − p̄_s) on marginal risks is **not** what the code does, and it would be wrong.

### Cited Findings
- Discrete-time PH model with a random effect for unobserved heterogeneity: Scheike & Jensen 1997, "A Discrete Survival Model with Random Effects: An Application to Time to Pregnancy", *Biometrics*, doi 10.2307/2533117 — [MaRDI record](https://portal.mardi4nfdi.de/wiki/Item:Q4351029) (record only). Later work describes it as a PH model with random effects for grouped data on the cloglog scale (search snippet only).
- The project's derivation: "Write each segment's conditional survival as exp(−Z_i H_ij(t)). Then P(no event in any segment by t) = L_Z(Σ_j H_ij(t)) … A cloglog binary GLMM with an offset or covariate for log follow-up time *is* that grouped-time proportional-hazards frailty model". Closest analogue: Duchateau & Janssen's udder-quarter infection data — `~/Desktop/Speciale/CGPS_statistics-/research_notes/Segment model to person risk/aggregation_methods.md` l.90; [Goethals et al. 2009](https://research.itg.be/en/publications/modeling-interval-censored-clustered-cow-udder-quarter-infection-/). — local + record
- Shortcuts, as quantified locally: the independence product on marginal risks gives about 0.63–0.69 instead of 0.49, and b = 0 gives about 0.45 instead of 0.49 (old-table prevalence, σ² 1.2–1.8) — `experiments/who/pooled_score2/pooling.md`. The code integrates correctly (`progression_who_pooled.py` l.11–13). — local
- Conditional versus marginal: conditional coefficients exceed marginal ones in magnitude. The closed-form attenuation β_m ≈ β_c/√(c²σ²+1) is a **logit** result and does not transfer to cloglog — [Pavlou et al. 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4525751/); the project plan also flags "the G01-vs-G02 attenuation formula does not apply to cloglog" (`CGPS_statistics-/CLAUDE.md`, open item 10). — local + PMC
- Median hazard ratio for a lognormal frailty: exp(0.954σ) — [Austin, Wagner & Merlo 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5299617/) (as relayed in `reports/Person risk pooling error check.md` l.11).
- With gamma frailty the person risk is closed-form, 1 − (1 + θS_i)^{−1/θ}. A gamma-frailty refit is a listed sensitivity analysis — `reports/Segment model to person risk.md` l.21; thesis notes l.150–152. — local

### Inferences
- The thesis wording "exp(β) is the hazard ratio … compares two units of the same cluster" (`01_prediction_model.tex` l.284, l.296) is correct for the conditional model. It should not be read as a population-average HR. For person-level geometry terms (LM angle, ratios), "within-person" is not meaningful. There β is the conditional HR given the frailty, which is between-person information adjusted for frailty. Local notes already say β mixes between- and within-person information (root `CLAUDE.md`).
- With logit there is no shortcut: P(no segment event | b) = ∏ 1/(1+e^{η+b}) does not collapse. The integral is still one-dimensional over b, but it is computed per person over all segment terms. So logit is computationally feasible. The real loss is the interpretability: no "summed hazard", and no person-level model of the same family. Earlier local wording ("the logit link has no such closed form") is correct, but it should not be read as "logit pooling is impossible".

### Gaps
- No source opened that derives the marginal (b-integrated) segment hazard ratio for a lognormal frailty. A gamma frailty gives the familiar convergence of marginal HRs toward 1 over time; I state this from memory, unverified.

## (B3) Is PH plausible and testable; does the link change C or the LR test; empirical link comparisons?

### Takeaway
PH cannot be tested with one follow-up scan per person. With a single observation time, the time effect, the baseline-hazard shape and any covariate×time interaction are confounded except through variation in follow-up length, and that variation is narrow (IQR 9.7–12.2 y). Link choice almost never changes discrimination or the significance of a block test materially when risks are not extreme: under link violation, MLE slopes are roughly proportional to the true ones (Li & Duan 1989). A logit refit and a profile over the Aranda-Ordaz link family are cheap, informative checks.

### Cited Findings
- "PH cannot be tested with one follow-up scan; say so" — `01_prediction_model.tex` l.104–105 (local notes).
- Li & Duan (1989), "Regression Analysis Under Link Violation", *Ann. Statist.* 17(3):1009–1052: under elliptically symmetric regressors, MLEs under a wrong link are consistent up to a scalar factor — [Project Euclid](https://projecteuclid.org/journals/annals-of-statistics/volume-17/issue-3/Regression-Analysis-Under-Link-Violation/10.1214/aos/1176347254.short) (abstract plus secondary descriptions).
- Czado & Santner (1992), *J. Stat. Plan. Inference* 33:213–231: a wrong link (especially wrong skewness) can bias coefficient estimates and inflate MSE; assuming logit when it is wrong increases bias — secondary description via search ([Springer s10260-020-00529-3](https://link.springer.com/10.1007/s10260-020-00529-3)); original not read.
- Aranda-Ordaz (1981, *Biometrika* 68:357–363) asymmetric family nests logit and cloglog; its shape parameter can be profiled, e.g. R `gcloglog` — [gcloglog manual](https://cran.r-universe.dev/gcloglog/doc/manual.html); [glmx plinks](https://rdrr.io/cran/glmx/man/plinks.html). No standard named "goodness-of-link" test of logit versus cloglog was found. Vendor heuristics ([MetricGate](https://metricgate.com/docs/aranda-ordaz-asymmetric-link/)) are weak sources.
- Cloglog has a fixed asymmetry (negative skewness), which is why flexible families exist — search snippet of a link-misspecification review (weak).

### Inferences
- **The LR test of the geometry block is essentially link-robust.** It is a test of β_geometry = 0. Under both links the null model is identical in form, and Li–Duan proportionality implies the same direction and roughly the same signal-to-noise. The p-value should change little. Report the logit LR as a sensitivity check.
- **C is link-robust.** The person risk is monotone in S_i under cloglog, and the analogous logit-pooled risk ranks people almost identically when the linear predictors are close up to scale. Calibration can differ, especially at 42% person risk and through the σ² estimate (σ² sits on a different latent scale: π²/6 for cloglog versus π²/3 for logit).
- **The parts that carry PH-type assumptions** are the time term (κ on log t), the length term, and the constancy of β over the ~10-year window. All of them are untestable or weakly testable here. A κ near 1 is consistent with a constant hazard but does not prove PH.
- **Is the asymmetry plausible?** Plaque onset as a "first event of a process accumulating over time and arterial length" is the textbook motivation for cloglog: the inverse link is P(at least one event of a Poisson process). That gives it substantive plausibility beyond convenience.
- **Log link / Poisson with offset is not a good alternative.** It can predict probabilities above 1 at 42% person risk. A Poisson model of a binary segment outcome is a rare-event approximation of cloglog, accurate only at low segment risk. The earlier local report already rules it out (`Experiment setup who and where.md` l.23).

### Gaps
- No empirical study was found that compares cloglog and logit GLMMs for clustered binary imaging outcomes on C or calibration.
- No published coronary/CCTA paper using cloglog was found, by either this search or the local evaluation (absence evidence, weak).

## (B4) Verdict, caveats, methods sentence, sensitivity analysis

### Takeaway
Cloglog was defensible and, for this design, the better choice. The reason is structural, not empirical: it is the grouped/interval-censored PH model; it makes segment hazards add into a person hazard, so the person risk is a one-dimensional frailty Laplace transform; and it puts SCORE2 and follow-up on their natural log-cumulative-hazard scale. Data will not show it fits better than logit at segment level. A logit refit should be a prespecified sensitivity analysis, and it is already listed as item 6 in the local plan.

### Cited Findings
- The project already lists the "logit-link refit; fixed-offset version of length" as sensitivity analysis 6 — `reports/Pooled cloglog GLMM evaluation.md` l.81; thesis notes l.152. — local
- Examiner checklist item "why cloglog and not logit, with the honest answer that fit cannot distinguish them at segment level and the reason is interpretive" — `reports/Pooled cloglog GLMM evaluation.md` l.89. — local
- Grouped-PH equivalence — [SAS](https://go.documentation.sas.com/api/docsets/statug/v_023/content/statug_logistic_examples19.htm); [Rodríguez](https://grodri.github.io/glms/notes/c7s6).

### Inferences
- **Caveats the thesis should state:**
  - exp(β) is a conditional hazard ratio given the person frailty, not population-averaged.
  - PH over the window and the time form (free coefficient on log follow-up, i.e. a grouped Weibull baseline, not an offset) are assumptions that one follow-up scan per person cannot test.
  - At segment level, cloglog and logit give nearly the same coefficients. The links differ mainly in the person risk, where the event proportion is about 42%.
  - Hazard ratios here must not be compared numerically with odds ratios from the literature.
  - "Hazard ratio independent of window length" holds under PH. In this cohort the window varies only about ±12%.
- **One methods sentence (suggestion; the code has a free log follow-up coefficient):** "The segment outcomes were modelled with a complementary log-log link, which is the form a proportional-hazards model takes when an event is known only to have occurred between two scans \cite{prentice1978grouped}; its coefficients are hazard ratios, and the segment hazards of one person add to a person hazard, so that the segment risks combine into one person risk." (Check against thesis-style rules before use: no "Because" opening, no list.)
- **Sensitivity analysis worth doing, in order:**
  - Refit B2 and G02 with a logit link on the same folds. Report the LR statistic, ΔC and person calibration. Expect near-identical LR and C. Any calibration difference shows how much the person risk leans on the link.
  - Report κ (the log follow-up coefficient) with its CI against 1, as the constant-hazard check.
  - Optionally, profile the Aranda-Ordaz shape parameter in a person-level model as a descriptive link check. This is not a test that decides anything.
  - Do not add a log-link/Poisson model.
- **Wording fix needed:** some local notes and the earlier report say "log(time) as offset". The code estimates the coefficient. Keep the thesis text in line with the code (root `CLAUDE.md`: methods must describe exactly what the code does).

### Gaps
- Whether the final plaque-free incident-plaque script keeps log follow-up as a free covariate is unknown. The only pooled script read (`progression_who_pooled.py`) is the Medis progression version.
- The size of the person-risk difference between links in this cohort is unknown until the logit refit is run on dtu-gpu-7.
