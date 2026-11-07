# Agreement statistics for tracer vs Medis (method comparison against a reference that is not ground truth)

Scope note: the thesis compares in-house tracer centerlines/lumen contours with Medis (reader-analysed, plaque patients only) for per-trunk scalars (length, mean curvature T_5, taper) and per-cross-section area-equivalent radius. Clustering: many cross-sections per artery, three arteries (LAD, LCx, RCA) per person.

Verification status: Bland & Altman (2007) was read in full text (author copy, York). For the other papers, the bibliographic details were checked against indexes (PubMed, publisher, repository pages); their content was confirmed only from abstracts or secondary sources. Formulas marked **[std]** are the standard textbook forms written from my own knowledge, not quoted from a fetched full text. Check them against the original before they go into the Technical Background chapter.

## Q1. Bland-Altman limits of agreement (1986, 1999): definition, assumptions, transforms, regression LoA, plotting

### Takeaway
LoA = mean difference ± 1.96 SD of the paired differences. The 95% interval is expected to contain the difference between the methods for 95% of future pairs on similar individuals. It assumes independent pairs, a bias and SD that are constant over the measurement range, and roughly normal differences. If the spread grows with size, log-transform and report the LoA as ratios. If the bias or SD trends with size in some other way, model both against the pair mean (regression LoA, Bland & Altman 1999). Plot the difference against the mean of the two methods, not against the reference method.

### Cited Findings
- Definition (in the authors' words): "We obtain the differences between measurements by the two methods for each individual and calculate the mean and standard deviation. We then estimate the 95% limits of agreement as ... mean minus 1.96 standard deviations and mean plus 1.96 standard deviations. These limits are expected to contain the difference between measurements by the two methods for 95% of pairs of future measurements on similar individuals." — [Bland & Altman 2007, full text](https://www-users.york.ac.uk/~mb55/meas/bland2007.pdf)
- Assumption, stated explicitly: "It is an implicit assumption that the difference between the two methods is reasonably stable across the range of measurements". When this fails, transform the data (Bland & Altman 1999). — [Bland & Altman 2007](https://www-users.york.ac.uk/~mb55/meas/bland2007.pdf)
- Assumption, independence: the authors "did not state in early publications that the LoA method assumes independent observations", because the requirement applies to all statistical analyses. Treating each pair as coming from a different individual means "the interval between the limits of agreement may be too narrow." — [Bland & Altman 2007](https://www-users.york.ac.uk/~mb55/meas/bland2007.pdf)
- Check the assumption by plotting the difference against the average of the two methods. — [Bland & Altman 2007](https://www-users.york.ac.uk/~mb55/meas/bland2007.pdf). Plotting the difference against the reference ("standard") method instead is misleading, because the difference is then correlated with the x-axis by construction. — [Bland, "why plotting difference against standard method is misleading"](https://www-users.york.ac.uk/~mb55/meas/diffplot.htm)
- The 1986 Lancet paper argues that the product-moment correlation is not a measure of agreement, and it introduces the difference-versus-mean plot. — [York reproduction of Bland & Altman 1986](https://www-users.york.ac.uk/~mb55/meas/ba.htm); [Citation classic note](https://smithengineering.queensu.ca/mme/faculty/deluzio/jam/files/Citation_classic_1992.pdf)
- The 1999 paper covers differences that vary with magnitude, with two approaches. (a) Log-transform: the antilogged limits are 95% limits for the *ratio* of the methods; a worked example gives 0.80 to 1.27. (b) Regression LoA: regress the difference on the average, then regress the absolute residuals (equivalently, the SD) on the average, and build limits that vary with magnitude. The paper also covers comparing the repeatability of each method. — [Bland, "How do I estimate LoA when mean or SD of differences is not constant?"](https://www-users.york.ac.uk/~mb55/meas/glucose.htm); [citedrive record of 1999 paper](https://citedrive.com/en/discovery/measuring-agreement-in-method-comparison-studies/)
- The 1999 paper contains an error in the variance-component formula: the multiplier should divide, not multiply. Bland & Altman 2007 corrects it. — [Bland & Altman 2007, Sec. 3](https://www-users.york.ac.uk/~mb55/meas/bland2007.pdf)
- **[std]** Normality: the ±1.96 SD form assumes approximately normal differences. Bland & Altman have argued that the LoA are fairly robust to moderate non-normality. A strongly skewed or heavy-tailed distribution argues for a transform or for empirical 2.5/97.5 percentiles. I did not fetch a primary quote for this point.
- **[std]** Report confidence intervals for the bias and for each limit. In the simple case, SE(bias) = s/√n and SE(limit) ≈ √(3s²/n), as given in Bland & Altman 1986/1999. I did not fetch a primary quote for this point.

### Inferences
- Proportional bias is plausible for **length** (longer vessels give more room for disagreement at the distal end) and for **radius** (large proximal vs small distal cross-sections). Check difference-vs-mean for each quantity before choosing the plain, log or regression LoA. For radius, a log transform gives percentage-type LoA, which are easier to interpret across the proximal-to-distal range.
- Curvature T_5 is positive and right-skewed, so a log or ratio scale is likely appropriate. Taper can be near zero or negative, so a log transform is not possible for it. Use the plain or regression LoA.
- Clinical acceptability of the LoA has to be judged against a prespecified tolerance. Here a natural tolerance is the between-person SD of the feature in the target population (see Q3/Q5). LoA that are wide relative to the between-person spread mean that the tracer cannot rank people.

### Gaps
- I did not obtain the full text of the 1986 and 1999 papers. Exact equations (SE formulas, the regression-LoA formula with √(π/2) scaling of absolute residuals) should be checked in the originals.
- Bibliography (checked against index records):
  - Bland JM, Altman DG. Statistical methods for assessing agreement between two methods of clinical measurement. *Lancet* 1986;327(8476):307–310. doi:10.1016/S0140-6736(86)90837-8. The DOI string is the commonly used one, but the search results did not show it; verify it on ScienceDirect.
  - Bland JM, Altman DG. Measuring agreement in method comparison studies. *Stat Methods Med Res* 1999;8(2):135–160. doi:10.1177/096228029900800204 ([citedrive](https://citedrive.com/en/discovery/measuring-agreement-in-method-comparison-studies/)).

## Q2. Bland-Altman with repeated/clustered data (Bland & Altman 2007; mixed-model LoA) — cross-sections per artery, arteries per person

### Takeaway
With several paired observations per subject, the SD for the LoA must include both the between-subject variance of the differences ("heterogeneity", a subject × method interaction) and the within-subject variance. Pooling all pairs as if independent, or averaging to one pair per subject, both give limits that are too narrow. The general solution is a linear mixed model on the paired differences, with nested random effects (person, then artery within person) and LoA = bias ± 1.96·√(sum of variance components). Bland & Altman flag within-subject autocorrelation as unresolved, and it is directly relevant to consecutive cross-sections along a centerline.

### Cited Findings
- Model for the "true value varies" case, where pairing is retained (the case that fits paired cross-sections): "the observed difference is the sum of the mean difference (bias), a random between subjects effect (heterogeneity) and a random error within the subject. The within-subject variance is assumed constant and observations within the subject are independent. The variance for single differences ... is found by summing the between subjects and within subjects variances." — [Bland & Altman 2007, Sec. 3](https://www-users.york.ac.uk/~mb55/meas/bland2007.pdf)
- ANOVA estimator with unequal replicates m_i (n subjects): σ²_w = MS_residual, and σ²_b = (MS_subject − MS_residual) / D with D = [(Σm_i)² − Σm_i²] / [(n−1)Σm_i]. D reduces to m when replicates are equal. Total SD = √(σ²_b + σ²_w). The bias is the plain mean of all individual differences, which "automatically weights the observations correctly". — [Bland & Altman 2007, Sec. 3](https://www-users.york.ac.uk/~mb55/meas/bland2007.pdf)
- The independence of repeated differences within a subject "might be a rather strong assumption". The paper ends with "Such analyses may be further improved by the development of methods to adjust for autocorrelation." — [Bland & Altman 2007](https://www-users.york.ac.uk/~mb55/meas/bland2007.pdf)
- "True value constant" case, with no pairing: SD² = var(subject mean differences) + (1 − (1/n)Σ1/m_i)-type multiplier × (σ²_w,X + σ²_w,Y). — [Bland & Altman 2007, Sec. 4](https://www-users.york.ac.uk/~mb55/meas/bland2007.pdf)
- Averaging to one pair per subject removes only the within-subject variation and gives limits that are too narrow. Ignoring the structure has less effect when heterogeneity is small. "Incorrectly calculated limits would lead us to think that methods of measurement agreed more closely than they actually do". — [Bland & Altman 2007, Sec. 5](https://www-users.york.ac.uk/~mb55/meas/bland2007.pdf)
- An erratum letter reports an arithmetic error in the 2007 paper: W. Jones, *J Biopharm Stat* 2019;29(3):574–575, doi:10.1080/10543406.2019.1572618. — [search record](https://pubmed.ncbi.nlm.nih.gov/17613642/)
- Carstensen, Simpson & Gurrin (2008) give the statistical model behind the classical LoA, extend it to replicate measurements (exchangeable vs linked replicates), and supply code. The MethComp R package implements it. — [IDEAS/RePEc](https://ideas.repec.org/a/bpj/ijbist/v4y2008i1n16.html); [Univ. Melbourne record](https://findanexpert.unimelb.edu.au/scholarlywork/300386-statistical-models-for-assessing-agreement-in-method-comparison-studies-with-replicate-measurements)
- Parker et al. (2016) apply mixed-effects LoA with multiple sources of variability (respiratory-rate devices in COPD) and find results similar to the ANOVA approach. — [PLOS ONE 11(12):e0168321](https://ideas.repec.org/a/plo/pone00/0168321.html). The R function `SimplyAgree::loa_lme` implements mixed-model LoA. — [CRAN doc](https://search.r-project.org/CRAN/refmans/SimplyAgree/html/loa_lme.html)
- Parker et al. (2020) is a tutorial on using LoA, CCC, TDI, coverage probability and CIA for continuous repeated-measures data. — [BMC Med Res Methodol 20:154](https://bmcmedresmethodol.biomedcentral.com/counter/pdf/10.1186/s12874-020-01022-x.pdf)

### Inferences
- **Per-trunk scalars** (length, T_5, taper) give one pair per artery and three arteries per person. Either (a) report LoA per artery type (LAD, LCx, RCA separately), which gives one pair per person and the classical LoA, consistent with the per-artery convention in this project; or (b) pool the arteries with a random person intercept on the difference: d_pa = μ (+ artery fixed effect) + u_p + ε_pa, LoA = μ ± 1.96√(σ²_u + σ²_ε). Option (a) is the simplest defensible choice. Arteries differ in length and curvature, so pooling would also mix proportional-bias patterns.
- **Per-cross-section radius**: d_{p,a,s} = μ + u_p + v_{pa} + ε_{pas}, with LoA = μ ± 1.96√(σ²_u + σ²_v + σ²_ε). This is the natural nested generalisation of the Bland & Altman (2007) varying-true-value model. Fit it by REML (lme4/nlme/statsmodels). Two caveats:
  1. Consecutive cross-sections are autocorrelated. If the sampling step is smaller than the correlation length, ε is not independent. One remedy is to subsample cross-sections at a spacing comparable to the lumen diameter, or to add an AR(1) residual structure (nlme `corAR1`). Otherwise the CIs for the variance components will be too narrow, although the point LoA is not necessarily biased.
  2. Each pair is formed by matching cross-sections between two different centerlines. Mismatch in the correspondence along the vessel and in the plane orientation inflates the differences, so the LoA include registration error, not just lumen-boundary error. State the matching rule.
- Proportional bias in radius (proximal vs distal) can be handled by modelling the difference on the log scale, or by adding the pair mean as a fixed covariate (a regression-LoA analogue in the mixed model).
- Bootstrap by person (cluster bootstrap) is a simple and defensible way to get CIs for the LoA in the nested model. This matches the person-level splitting used elsewhere in the thesis.

### Gaps
- I did not obtain the full text of Carstensen et al. (2008), so its DOI and article number were not verified. The IDEAS record gives *Int J Biostat* 4(1), article 16 (2008). The DOI is likely 10.2202/1557-4679.1107; verify it.
- I found no published treatment of autocorrelated cross-sections along vessel centerlines specifically in a LoA framework.
- Bibliography: Bland JM, Altman DG. Agreement between methods of measurement with multiple observations per individual. *J Biopharm Stat* 2007;17(4):571–582. doi:10.1080/10543400701329422. PMID 17613642. — [PubMed](https://pubmed.ncbi.nlm.nih.gov/17613642/)

## Q3. ICC: which form, ICC(A,1) vs ICC(C,1), thresholds, dependence on between-subject spread, and consequences of a validation sample that differs from the target population

### Takeaway
For two fixed methods (tracer and Medis) and single measurements, the relevant forms are the two-way models with single-measurement ICCs (McGraw & Wong 1996). ICC(A,1) is absolute agreement and penalises systematic bias. ICC(C,1) is consistency and ignores additive bias. For substituting one method for the other, use ICC(A,1). For a feature used only to rank people in a model that standardises or rescales it, ICC(C,1) is arguably the relevant reliability. The Koo & Li thresholds (<0.5 poor, 0.5–0.75 moderate, 0.75–0.9 good, >0.9 excellent) are conventions. The ICC is a ratio of between-subject variance to total variance, so it is not transportable from the plaque-patient sample to the plaque-free cohort unless the between-person spread is similar in both.

### Cited Findings
- Shrout & Fleiss (1979) give guidelines for choosing among six forms of the ICC for n targets rated by k judges. The forms differ by whether judges are random or fixed and whether single or average ratings are used. — [PubMed 18839484](https://pubmed.ncbi.nlm.nih.gov/18839484/); [psych::ICC doc](https://personality-project.org/r/html/ICC.html)
- McGraw & Wong (1996) extend this to 10 forms. Model (one-way, two-way random, two-way mixed) × type (consistency C vs absolute agreement A) × unit (single, average of k). There is an erratum on p. 390. Per the psych documentation, SPSS appears to use the McGraw–Wong formula without the erratum. — [psych::ICC doc](https://personality-project.org/r/html/ICC.html); [synapsesocial record (DOI)](https://synapsesocial.com/papers/W2067724039)
- Koo & Li (2016): there are 10 forms, and choosing one requires reviewing the design. Reports should state the software, "model", "type" and "definition". — [Koo & Li search record / PMC4913118](https://pmc.ncbi.nlm.nih.gov/articles/4913118)
- Koo & Li thresholds: <0.50 poor, 0.50–0.75 moderate, 0.75–0.90 good, >0.90 excellent. — [effectsize::interpret_icc](https://www.rdocumentation.org/packages/effectsize/versions/0.7.0/topics/interpret_icc). It is commonly said that Koo & Li recommend grading on the 95% CI rather than the point estimate, but I could not confirm that from the full text; one source attributes the lower-bound rule to software convention. — [search summary](https://papers.mewayz.com/paper/oa_W2327037637)
- A two-way absolute-agreement ICC penalises a rater who scores consistently higher. The consistency form does not. — [metricgate ICC(2,1) page (Japanese)](https://metricgate.com/calculator/ja/icc-2-1-two-way-random)
- Bland & Altman (1990) argue against the ICC as the main measure of agreement between two methods. The UCL ophthalmic statistics note says reporting the ICC alongside LoA goes "against a clear steer" from Bland & Altman. — [Dore et al., Ophthalmic statistics note 14 (AAM)](https://discovery.ucl.ac.uk/id/eprint/10097012/3/Dore_Ophthalmic%20statistics%20note%2014_AAM.pdf); citation Comput Biol Med 1990;20(5):337–340, doi:10.1016/0010-4825(90)90013-f ([York refs](https://www-users.york.ac.uk/~mb55/meas/comref.htm))
- **[std]** Mean-square formulas, two-way model, n subjects, k = 2 methods. MS_R = rows (subjects), MS_C = columns (methods), MS_E = residual.
  - ICC(C,1) = (MS_R − MS_E) / (MS_R + (k−1)MS_E)
  - ICC(A,1) = (MS_R − MS_E) / (MS_R + (k−1)MS_E + (k/n)(MS_C − MS_E))
  - In variance-component terms: ICC(A,1) = σ²_s / (σ²_s + σ²_m + σ²_e) and ICC(C,1) = σ²_s / (σ²_s + σ²_e), where σ²_s is between-subject, σ²_m is method (bias) and σ²_e is residual variance.
  - In Shrout–Fleiss notation, ICC(A,1) corresponds numerically to ICC(2,1) and ICC(C,1) to ICC(3,1). I did not check these against the full text.

### Inferences
- **Dependence on spread.** The formulas show that, for a fixed error variance σ²_e, the ICC rises with the between-subject variance σ²_s. A method with identical LoA can therefore have a high ICC in a heterogeneous sample and a low ICC in a homogeneous one. This is the core argument of Bland & Altman (1990) and Müller & Büttner (1994). I could not retrieve the full text of either; see Gaps.
- **Consequence for this thesis.** Medis exists only in plaque patients. Their coronary geometry distribution may differ from the plaque-free cohort's. They are older and more often male, and may differ in vessel size and tortuosity. Plaque can also locally narrow the lumen and change contour difficulty, so the *error* variance may differ as well. A defensible approach:
  1. Report LoA as the primary agreement result. LoA are on the measurement scale and do not depend on σ²_s, given homogeneous error.
  2. Treat the ICC from the Medis sample as specific to that sample.
  3. Estimate the reliability that matters in the target population as λ_target ≈ 1 − σ²_e / Var_obs,target, where σ²_e is the tracer error variance (Q5) and Var_obs,target is the observed between-person variance of the tracer feature in the plaque-free cohort. This rests on an untestable assumption: the tracer's error variance is the same in plaque-free and plaque patients. Plaque-free vessels are arguably easier to trace, which would make it conservative, but that is a hypothesis.
- The ICC should use the same unit as the downstream model. If the risk model uses per-trunk T_5 (one value per artery per person), compute the ICC on per-trunk values. A per-cross-section radius ICC answers a different question.
- With small n (Medis subset per artery), the ICC CIs will be wide. Report them.

### Gaps
- I could not retrieve Müller R, Büttner P. A critical discussion of intraclass correlation coefficients. *Stat Med* 1994;13(23–24):2465–2476. The citation details are from memory; verify them, including the DOI 10.1002/sim.4780132310.
- I did not verify from the full text whether Koo & Li recommend grading on the CI. Treat that as unverified.
- Bibliography:
  - Shrout PE, Fleiss JL. Intraclass correlations: uses in assessing rater reliability. *Psychol Bull* 1979;86(2):420–428. doi:10.1037/0033-2909.86.2.420. — [PubMed](https://pubmed.ncbi.nlm.nih.gov/18839484/)
  - McGraw KO, Wong SP. Forming inferences about some intraclass correlation coefficients. *Psychol Methods* 1996;1(1):30–46. doi:10.1037/1082-989X.1.1.30. Erratum: *Psychol Methods* 1996;1(4):390. — [synapsesocial](https://synapsesocial.com/papers/W2067724039); [psych doc](https://personality-project.org/r/html/ICC.html)
  - Koo TK, Li MY. A guideline of selecting and reporting intraclass correlation coefficients for reliability research. *J Chiropr Med* 2016;15(2):155–163. doi:10.1016/j.jcm.2016.02.012. PMC4913118.
  - Bland JM, Altman DG. A note on the use of the intraclass correlation coefficient in the evaluation of agreement between two methods of measurement. *Comput Biol Med* 1990;20(5):337–340. doi:10.1016/0010-4825(90)90013-F.

## Q4. Lin's CCC as alternative; why Pearson correlation is inappropriate for agreement

### Takeaway
Pearson's r measures linear association. It is invariant to location and scale shifts, so two methods with a large bias or a slope ≠ 1 can have r ≈ 1. Lin's CCC measures deviation from the 45° identity line: ρ_c = r × C_b, where C_b (bias-correction factor) penalises location and scale shifts. The CCC shares the ICC's dependence on between-subject spread and is numerically close to ICC(A,1). It is a summary, not a replacement for LoA.

### Cited Findings
- The Lancet 1986 paper's central argument is that correlation is not agreement: a "high correlation does not mean that the two methods agree." — [York reproduction](https://www-users.york.ac.uk/~mb55/meas/ba.htm)
- Lin's CCC "quantifies the deviation from the 45-degree line, which is due to location and scale shifts". It is the product of Pearson's r and a bias-correction factor. Pearson's r is invariant to location and scale shifts. — [R-bloggers summary](https://www.r-bloggers.com/2020/01/concordance-correlation-coefficient/); [GenStat doc](https://genstat.kb.vsni.co.uk/knowledge-base/lconcord/)
- Lin later corrected the variance formula used for CIs: Lin LI. A note on the concordance correlation coefficient. *Biometrics* 2000;56:324–325. — [GenStat doc](https://genstat.kb.vsni.co.uk/knowledge-base/lconcord/)
- Parker et al. (2020) give CCC versions for repeated-measures data alongside LoA, TDI, CP and CIA, and find that the five methods give similar conclusions in their example. — [BMC MRM 2020;20:154](https://bmcmedresmethodol.biomedcentral.com/counter/pdf/10.1186/s12874-020-01022-x.pdf)
- **[std]** ρ_c = 2σ_xy / (σ²_x + σ²_y + (μ_x − μ_y)²). Lin used n in the moment estimates rather than n−1.

### Inferences
- Pearson r is not an agreement measure, but it is not irrelevant to this thesis's question. For *ranking*, a constant bias or a scale factor does no harm, because only the ordering and linear association matter. Squared correlation with the true value is exactly the reliability that drives attenuation (Q5). So the defensible framing is: LoA (and optionally ICC(A,1)/CCC) for *agreement*, and ICC(C,1) or a Spearman correlation as a *ranking-consistency* check. Say explicitly that the second is not agreement.
- Reporting both ICC(A,1) and CCC is redundant. Pick one.

### Gaps
- I did not retrieve the full text of Lin (1989).
- Bibliography: Lin LI-K. A concordance correlation coefficient to evaluate reproducibility. *Biometrics* 1989;45(1):255–268. doi:10.2307/2532051. PMID 2720055. The DOI is the commonly used one but was not shown in the search results; verify it on JSTOR.

## Q5. Imperfect reference: agreement vs accuracy, GRRAS, regression dilution and attenuation (ICC ↔ reliability ratio)

### Takeaway
When the reference is not ground truth, the comparison estimates *agreement* (inter-method), not *accuracy* or *validity*, and it should be reported as such. GRRAS gives a 15-item reporting checklist. For the downstream risk model, random error in a predictor attenuates its coefficient toward zero. In the single-predictor linear case the observed slope is λ times the true slope, with λ = σ²_true / (σ²_true + σ²_error), the reliability ratio, which equals an ICC. Var(tracer − Medis) = σ²_e,tracer + σ²_e,Medis if the two errors are independent. Under that assumption the disagreement variance is an upper bound on the tracer's error variance, which gives a conservative lower bound for λ. If the errors are positively correlated (both read the same image, both struggle on the same artefacts), the bound fails and the error is underestimated.

### Cited Findings
- Kottner et al. (2011) is GRRAS. Eight experts proposed 15 issues to address when reporting reliability and agreement studies. The guideline was published simultaneously in *J Clin Epidemiol* and *Int J Nurs Stud*. — [KU research profile](https://researchprofiles.ku.dk/en/publications/guidelines-for-reporting-reliability-and-agreement-studies-grras--4/); [Manchester record](https://research.manchester.ac.uk/en/publications/guidelines-for-reporting-reliability-and-agreement-studies-grras-/)
- Regression dilution: random error in the exposure X flattens the exposure–outcome slope. Error in the outcome has a different effect. — [Hutcheon et al. BMJ 2010;340:c2289](https://emj.bmj.com/lookup/ijlink/YTozOntzOjQ6InBhdGgiO3M6MTQ6Ii9sb29rdXAvaWpsaW5rIjtzOjU6InF1ZXJ5IjthOjQ6e3M6ODoibGlua1R5cGUiO3M6NDoiRlVMTCI7czoxMToiam91cm5hbENvZGUiO3M6MzoiYm1qIjtzOjU6InJlc2lkIjtzOjE3OiIzNDAvanVuMjNfMi9jMjI4OSI7czo0OiJhdG9tIjtzOjIyOiIvZW1lcm1lZC8zMy81LzMwNy5hdG9tIjt9czo4OiJmcmFnbWVudCI7czowOiIiO30=)
- The attenuation factor λ is the ratio of true-score variance to observed variance. It is also called the reliability coefficient or attenuation factor and equals the ICC. The observed coefficient is λ × the true coefficient for a single predictor. With several error-prone or correlated predictors, the bias can go in either direction. — [Rutter et al., PMC6857752](https://pmc.ncbi.nlm.nih.gov/articles/PMC6857752); [mecor paper, arXiv 2102.04791](https://arxiv.org/pdf/2102.04791)
- A large applied example: UK Biobank ICCs for 2,858 variables from repeat measures, with correction code. — [PMC10555784](https://pmc.ncbi.nlm.nih.gov/articles/PMC10555784); [Bristol record](https://research-information.bris.ac.uk/en/publications/exploring-regression-dilution-bias-using-repeat-measurements-of-2/)
- Frost & Thompson (2000) compare correction methods for one predictor. The correction factor can be estimated from repeat measurements in a subset or in a separate study. CIs for the corrected slope must account for uncertainty in the correction factor too. — [IDEAS](https://ideas.repec.org/a/bla/jorssa/v163y2000i2p173-189.html)
- Carroll, Ruppert, Stefanski & Crainiceanu (2006, 2nd ed.) is the standard text. It has sections on "Linear Regression and Attenuation" and "Attenuation in General Problems", and covers logistic regression, regression calibration and SIMEX. — [Routledge](https://www.routledge.com/Measurement-Error-in-Nonlinear-Models-A-Modern-Perspective/Carroll-Ruppert-Stefanski-Crainiceanu/p/book/9781584886334); [author page](https://carroll.stat.tamu.edu/eiv-secondedition/)

### Inferences
- **Terminology for the thesis:** say "agreement with Medis", "inter-method agreement" and "Medis reference". Avoid "accuracy", "error relative to ground truth" and "validated against ground truth". Disagreement cannot be attributed to the tracer alone.
- **Linking agreement to the risk model:**
  - Assume classical, non-differential, independent errors and errors independent between the methods. Then Var(d) = σ²_e,T + σ²_e,M, so σ²_e,T ≤ Var(d) (within-person and across-person components from the mixed-model LoA, Q2).
  - A conservative tracer reliability in the plaque-free target population is λ_T ≥ 1 − Var(d) / Var_obs,T,target.
  - For logistic regression with a modest effect, attenuation is approximately λ as well (Carroll et al. 2006, regression-calibration approximation). This is approximate; I did not verify a page reference.
- The *who* question is a prespecified LR test with ΔC. Random error in geometry lowers power and ΔC but does not create spurious association, as long as the error is non-differential (unrelated to future plaque). Differential error is conceivable here: if subclinical disease affects image quality or lumen appearance, tracer error could correlate with the outcome. Name this as a limitation.
- Error in **taper** (a slope over a short length) and **curvature** (second derivative, noise-amplifying) is likely larger relative to the between-person spread than error in length. So λ will differ across features, and features with low λ may be under-detected in the risk model.
- **Shared-error caveat:** both methods segment the same CCTA volume, so image-driven errors (motion, blooming, partial volume) affect both. Agreement then overstates accuracy. This is the main reason to write "agreement, not accuracy".

### Gaps
- I found no source that addresses transporting a reliability or attenuation estimate from one population (plaque patients) to another (plaque-free). The λ_target inference above is my own reasoning from the variance definition.
- I did not retrieve the GRRAS checklist items themselves. Get the 15 items from the paper if they are listed in the thesis.
- Bibliography:
  - Kottner J, Audigé L, Brorson S, Donner A, Gajewski BJ, Hróbjartsson A, Roberts C, Shoukri M, Streiner DL. Guidelines for Reporting Reliability and Agreement Studies (GRRAS) were proposed. *J Clin Epidemiol* 2011;64(1):96–106. doi:10.1016/j.jclinepi.2010.03.002. Also in *Int J Nurs Stud* 2011;48(6):661–671, doi:10.1016/j.ijnurstu.2011.01.016. The author list is from memory; verify it.
  - Hutcheon JA, Chiolero A, Hanley JA. Random measurement error and regression dilution bias. *BMJ* 2010;340:c2289. doi:10.1136/bmj.c2289. The user's brief said "c3223"; the correct article number is c2289.
  - Frost C, Thompson SG. Correcting for regression dilution bias: comparison of methods for a single predictor variable. *J R Stat Soc A* 2000;163(2):173–189. doi:10.1111/1467-985X.00164.
  - Carroll RJ, Ruppert D, Stefanski LA, Crainiceanu CM. *Measurement Error in Nonlinear Models: A Modern Perspective*. 2nd ed. Boca Raton: Chapman & Hall/CRC; 2006. ISBN 978-1-58488-633-4. doi:10.1201/9781420010138, from memory; verify it.

## Q6. How image segmentation / coronary centerline papers phrase "reference, not ground truth"

### Takeaway
The coronary CTA benchmarks use "reference standard" for expert or multi-observer annotations. The broader segmentation literature acknowledges inter-observer variability and a trade-off between how accurate a reference is and how realistic it is. These are the citable framings for calling Medis a "reference".

### Cited Findings
- Schaap et al. (2009), Rotterdam centerline framework: "Standardized evaluation methodology and reference database". 32 cardiac CTA datasets "with corresponding reference standard". A method creates a consensus centerline from multiple observers. 13 algorithms were evaluated. — [RUG record](https://research.rug.nl/en/publications/standardized-evaluation-methodology-and-reference-database-for-ev/); [Harvard LMI](https://lmi.bwh.harvard.edu/publications/standardized-evaluation-methodology-and-reference-database-evaluating-coronary-artery)
- Kirişli et al. (2013), Rotterdam stenosis and lumen framework: 48 multicenter, multivendor CTA datasets with reference standards from expert annotations, and algorithms from 11 groups. Automatic lumen segmentation reached precision similar to the experts. — [EUR repository](https://repub.eur.nl/pub/41673); [Sabanci](https://research.sabanciuniv.edu/22843)
- STAPLE estimates a reference segmentation and rater performance at the same time, because the true segmentation is unknown. "There is a tradeoff between the accuracy and realism of the reference standard." — [PMC1283110 (Warfield et al.)](https://pmc.ncbi.nlm.nih.gov/articles/PMC1283110); [PMC3079852](https://pmc.ncbi.nlm.nih.gov/articles/PMC3079852)

### Inferences
- Suggested phrasing: "Medis centerlines and contours, edited by a reader, served as the *reference standard*. They are not ground truth, so differences reflect error in both methods, and the results are reported as inter-method agreement." This mirrors Schaap/Kirişli usage. Unlike those benchmarks, Medis here is a single reader's clinical analysis, not a multi-observer consensus. The Medis reference is therefore probably noisier than the Rotterdam references, and probably only the contoured, diseased part was checked (per the project data notes).
- Inter-observer variability of Medis itself is unknown in this dataset. Without it, the analysis cannot separate how much of the disagreement belongs to the tracer.

### Gaps
- I did not retrieve the exact sentences from Schaap 2009 or Kirişli 2013 about observer variability, including the number of observers.
- Bibliography:
  - Schaap M, Metz CT, van Walsum T, van der Giessen AG, Weustink AC, Mollet NR, Bauer C, et al. Standardized evaluation methodology and reference database for evaluating coronary artery centerline extraction algorithms. *Med Image Anal* 2009;13(5):701–714. doi:10.1016/j.media.2009.06.003. The DOI is from memory; verify it.
  - Kirişli HA, Schaap M, Metz CT, et al. Standardized evaluation framework for evaluating coronary artery stenosis detection, stenosis quantification and lumen segmentation algorithms in computed tomography angiography. *Med Image Anal* 2013;17(8):859–876. doi:10.1016/j.media.2013.05.007.
  - Warfield SK, Zou KH, Wells WM. Simultaneous truth and performance level estimation (STAPLE): an algorithm for the validation of image segmentation. *IEEE Trans Med Imaging* 2004;23(7):903–921. doi:10.1109/TMI.2004.828354. The details are from memory; verify them.
