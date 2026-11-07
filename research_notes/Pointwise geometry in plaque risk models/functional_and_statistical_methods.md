# Statistical (non-neural) methods for whole-curve vessel geometry predictors in a risk model

Scope note: ~20 tool calls. Several primary papers (Goldsmith 2011 full text, Reiss et al. 2017 review, Swihart et al. 2014, Gellar 2015) could only be read via abstracts, package docs or citing papers; PMC pages were blocked by a browser check. Claims marked "(not verified this session)" come from background knowledge and should be checked before they are cited in the thesis.

## 1. Functional data analysis: scalar-on-function regression, functional GLM(M)s, functional Cox; estimating and testing beta(s)

### Takeaway
The standard tool is the generalized functional linear model g(E[Y]) = alpha + Z'gamma + integral X_i(s) beta(s) ds, with beta(s) as a penalized spline (Goldsmith et al. 2011, `refund::pfr` / `lf()`), as an expansion in functional principal components (FPCR), or as a fixed low-rank basis. All of these are mixed-model or GAM fits in `mgcv`, so a binomial cloglog link and a person random intercept can in principle be added. The catch for this thesis is testing. With a penalized beta(s) the "no effect" test is a boundary or variance-component problem, and the null distribution is not a plain chi-square. One prespecified LR test with a standard reference distribution is easiest to keep if beta(s) is restricted beforehand to a small fixed, unpenalized basis or to a fixed number K of FPC scores.

### Cited Findings
- Goldsmith, Bobb, Crainiceanu, Caffo and Reich, "Penalized Functional Regression", J. Comput. Graph. Stat. 20(4):830–851 (2011). The functional predictor is projected onto a large number of smooth eigenvectors, and beta(s) is estimated by penalized spline regression. The smoothing level is set by REML or cross-validation in an associated mixed model, and the method runs in standard mixed-effects software. It covers generalized (non-Gaussian) outcomes, predictors measured with or without error, sparse or dense sampling, multiple functional predictors and multilevel structure. The application uses DTI tract profiles in MS. — [Search summary of abstract / core.ac.uk copy](https://core.ac.uk/download/61318164.pdf); [refund pfr docs](https://rdocumentation.org/packages/refund/versions/0.1-5/topics/pfr)
- `refund::pfr()` wraps mgcv `gam`/`bam`/`gamm`/`gamm4` for "a scalar (but not necessarily continuous) response". Its special terms are `lf()` (linear functional), `af()` (additive functional), `lf.vd()` (variable domain), `fpc()` (FPC-based), `peer()` and `re()` (random effects, e.g. `re(ID)` for a subject random intercept). The default smoothing method is REML. The family is passed through to `gam`. — [refund pfr docs (rdrr.io)](https://rdrr.io/cran/refund/man/pfr.html)
- mgcv natively supports scalar-on-function terms through its "summation convention". A matrix covariate with a `by=` weight matrix enters the linear predictor as rowSums(F*L), "an approximation to the integral required for performing scalar-on-function regression", e.g. `gam(y ~ s(X, by=L, k=20))`. The term is not automatically centred unless rowSums(L) is constant. — [mgcv linear.functional.terms](https://rdrr.io/pkg/mgcv/man/linear.functional.terms.html)
- Generalized multilevel functional regression (Crainiceanu, Staicu and Di, JASA 104(488):1550–1561, 2009) allows exponential-family outcomes (e.g. hypertension as a binary outcome) with multilevel functional exposures (sleep EEG, Sleep Heart Health Study). It compares a two-stage frequentist approach with a joint Bayesian one. — [PMC2897156 record / search summary](https://pmc.ncbi.nlm.nih.gov/articles/PMC2897156); [JHU working paper](https://biostats.bepress.com/jhubiostat/paper173)
- Functional Cox: Gellar, Colantuoni, Needham and Crainiceanu, "Cox regression models with functional covariates for survival data", Statistical Modelling 15(3):256–278 (2015). It combines penalized signal regression with mixed-effects proportional hazards methods for a baseline densely sampled functional exposure. Chen et al. (2011) is cited as the first functional Cox model. — [Statistical Modelling abstract](https://statmod.org/smij/Vol15/Iss3/Gellar/Abstract.html); [extended functional Cox, arXiv 2511.04852 (preprint)](https://arxiv.org/pdf/2511.04852)
- Testing beta(s) = 0: Swihart, Goldsmith and Crainiceanu (Technometrics, "Restricted likelihood ratio tests for functional effects in the functional linear model") write pfr in mixed-model form and test no effect as zero variance components. `refund::rlrt.pfr` documentation: use the RLRT for the *constancy* test, and the ordinary LRT (method = "ML") for the *inclusion* (no-effect) test. — [Swihart publication list](https://biostat.jhsph.edu/~bswihart/Publications/index.html); [rlrt.pfr docs](https://rdrr.io/cran/refund/man/rlrt.pfr.html)
- McLean, Hooker and Ruppert (arXiv 1310.5811, later published) point out that an RLRT is inappropriate for the no-effect test because the fixed effects differ between the hypotheses. They use the exact LRT null distribution of Crainiceanu and Ruppert (2004) instead. They test linearity within a functional GAM. — [arXiv 1310.5811](https://arxiv.org/pdf/1310.5811)
- A comparison of tests (Tekbudak, Alfaro Córdoba, Maity and Staicu; arXiv 1710.05729) used n = 50/100/500 and 5,000 replications for size and 1,000 for power. For nullity, the McLean et al. LRT and the Kong–Staicu–Maity F-test on FPC scores (KSM) performed similarly at n = 500. At moderate n there was no uniform winner, and the authors recommend KSM. The García-Portugués bootstrap test was least powerful. For linearity, the McLean et al. RLRT was best, and the FPCA-based Horváth–Reeder test had inflated type I error at small or moderate n. — [ar5iv 1710.05729](https://ar5iv.arxiv.org/html/1710.05729)
- Reviews: Morris, "Functional Regression", Annu. Rev. Stat. Appl. 2:321–359 (2015) (arXiv 1406.4068) covers basis representations and scalar-on-function, function-on-scalar and function-on-function regression. Reiss, Goldsmith, Shang and Ogden, "Methods for scalar-on-function regression", Int. Stat. Rev. 85(2):228–249 (2017) reviews linear, nonlinear and nonparametric models and their software. — [Morris arXiv](https://arxiv.org/pdf/1406.4068); [Reiss et al. RePEc](https://econpapers.repec.org/RePEc:bla:istatr:v:85:y:2017:i:2:p:228-249)

### Inferences
- **Fitting in the thesis model.** The segment-level cloglog GLMM could take a functional term per segment in mgcv: `gam(y ~ base + segment + s(S, by=K) + s(id, bs="re"), family=binomial(link="cloglog"))`, with S the matrix of normalised arc-length positions and K the curvature matrix times the quadrature weights. The cloglog link and the `bs="re"` random intercept are standard mgcv features (not verified this session for the combination with linear functional terms). A single beta(s) shared by all 9 segments costs roughly the basis dimension. A beta(s) per segment or per artery multiplies that by 9 or 3.
- **Parameter cost.** A penalized beta(s) uses an effective df chosen by REML. It is typically between 1 and k−1, where k is about 10–20 basis functions. It is estimated, not prespecified, so "the geometry block" no longer has a fixed df. FPCR with K prespecified scores costs exactly K parameters per functional predictor (and per artery if beta varies by artery). An unpenalized B-spline beta(s) with 3–5 basis functions costs exactly 3–5.
- **Keeping one prespecified LR test with a standard reference distribution (chi-square with fixed df).** Fix the number of FPC scores K, or the number of unpenalized basis functions, before the outcome is examined, for example from the share of curve variance explained in an outcome-blind step. Then test the whole geometry block with an LR test on K × (number of curves) df. If a penalized beta(s) is kept, the LR null is a mixture or nonstandard and needs the Crainiceanu–Ruppert exact or simulated distribution or a parametric bootstrap. In a GLMM with a random intercept that is computationally heavy (Crainiceanu–Ruppert is derived for linear mixed models).
- With FPCR, the leading PCs capture the dominant *variation* in curvature, not necessarily the variation that predicts plaque. If the risk-relevant feature is a low-variance direction, a small K misses it. The KSM results above show that a fixed small number of FPC scores still gives a well-sized test.

### Gaps
- No source found showing a scalar-on-function term inside a cloglog GLMM with a random intercept and an LR test. The construction is plausible in mgcv/gamm4 but unverified.
- Full texts of Goldsmith 2011, Reiss et al. 2017 and Swihart et al. could not be read. Details of their simulation results (effective df ranges, power) are not reported here.
- Reiss and Ogden 2007 (JASA, FPCR and functional PLS) was not retrieved this session.

## 2. Curves of different lengths: registration, normalised arc length, landmarks

### Takeaway
There are three approaches: (a) map each vessel or segment to normalised arc length [0,1], which assumes that relative position is what matters; (b) keep absolute arc length from a landmark such as the ostium or a bifurcation, and let beta depend on the domain length (variable-domain regression, `lf.vd`); (c) register curves by warping, as in the AneuRisk carotid work. In the thesis model, the segment split itself already acts as landmark registration. A normalised arc length within each segment is the simplest outcome-blind choice.

### Cited Findings
- Variable-domain functional regression (Gellar, Colantuoni, Needham and Crainiceanu, JASA 109(508):1425–1439, 2014) lets each subject's functional predictor have its own domain width T_i. The coefficient is beta(t, T_i), which changes smoothly with T_i. In refund, `lf.vd()` fits the average of X_i(t)·beta(t, T_i) over [0, T_i] with bivariate thin-plate splines. The transform options are "standardized", "linear", "quadratic", "lagged" and "noInteraction". The example is binary: `pfr(death ~ lf.vd(SOFA) + age + los, family="binomial")`. — [lf.vd docs](https://rdrr.io/cran/refund/man/lf.vd.html); [IDEAS record](https://ideas.repec.org/a/taf/jnlasa/v109y2014i508p1425-1439.html)
- AneuRisk (Sangalli, Secchi, Vantini and Veneziani, JASA 2009) studied the internal carotid artery in 65 patients. The centerlines had 350–1,380 points and lengths of 27.2–110.1 mm. Arc length was measured from the terminal bifurcation (a landmark) back toward the heart, and left carotids were mirrored. The curves were registered by iterative affine warping (shift ≤ ±5 mm, plus dilation), maximising a similarity index on first derivatives. Registration separates amplitude from phase variability, and mean similarity rose from 0.80 to 0.93. FPCA of the registered radius and curvature profiles followed. QDA on FPC scores separated aneurysm location groups, with a leave-one-out error of about 21.5%. — [Sangalli et al. 2009 PDF](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)

### Inferences
- In the 9-trunk-segment model, a segment boundary defined by anatomy (e.g. side branches) is a landmark. Normalising arc length within each segment is landmark registration with linear warping in between. Warping registration on top of that would remove phase variability that may itself carry risk information, for example where along the segment the bend lies. It also adds an estimation step that must be frozen before the outcome is examined.
- Normalisation discards segment length. If length matters, it should enter as a separate scalar covariate. Alternatively, use absolute arc length from the segment start, truncated to a common length; that drops data from long segments.
- `lf.vd` is the principled option when domain length truly varies and the effect may depend on it, but it costs a bivariate surface. With about 1,000 people, that is likely too expensive.

### Gaps
- No coronary-specific registration study was found.

## 3. Scalar summaries that use every point and resist noise

### Takeaway
No source was found that directly compares the reliability of the mean, max, quantiles, excursion length or bend counts of vessel curvature. Clinical vessel studies use total or integrated absolute curvature and tortuosity indices. Statistical reasoning favours smoothed-curve quantiles (e.g. the 75th or 90th percentile) and length above a threshold over the raw max. Any such summary should be computed on the smoothed curve at a scale fixed in advance.

### Cited Findings
- In Loeys–Dietz syndrome, a JAHA 2024 carotid study recommends a curvature-based measure, *total absolute curvature*, for early detection or monitoring of disease progression. — [DOAJ record, JAHA 2024](https://doaj.org/article/81f1f393851444b8870a8859b4bfbc75)
- Tuncay et al. (2018; 73 people, CCTA, semi-automatic centerlines) found curvature 16.7% higher in segments with significant stenosis and 13.8% higher in such arteries. Curvature was related to plaque per segment and per artery (p < 0.001). The tortuosity index (centerline length / end-to-end distance) was related to plaque only per segment. The analysis is cross-sectional and the sample small. — [Record](https://katalog.lib.cas.cz/KNAV/EdsRecord/cmedm,29486988)
- AneuRisk found ICAs in the aneurysm-at/after-bifurcation group to be "significantly wider, more tapered and less curved" in the last 3 cm. That is the kind of shape difference a single mean could hide. — [Sangalli et al. 2009](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)

### Inferences
- **Noise biases curvature upward.** Curvature is |r''|-based, so it is ≥ 0, and residual noise always adds to it. The max of a noisy curve is driven by the largest noise spike: it grows with the number of points (vessel length) and is the least reliable summary. The mean of unsmoothed curvature, and integrated absolute curvature even more so, also carries a noise floor proportional to length. Integrated curvature mixes "how curved" with "how long".
- More robust candidates on the *smoothed* curve:
  - an upper quantile (e.g. the 75th or 90th percentile);
  - the length or fraction of the segment with curvature above a threshold fixed a priori (e.g. from the clean-cohort distribution or a hemodynamic radius-of-curvature argument);
  - the number of bends exceeding the threshold, with a minimum separation in mm.
  The threshold-based ones need the threshold frozen outcome-blind.
- **Multiscale summaries.** Curvature at 2–3 smoothing scales (e.g. 2, 5 and 10 mm windows) separates local kinks from global bends. Each scale is an added parameter and the scales are highly correlated, so pick one primary scale before the outcome and treat the others as sensitivity analyses.
- A low-K FPCA score set is itself a "summary that uses every point". The first FPC of curvature is often close to a weighted mean, and later FPCs capture where the curvature lies.

### Gaps
- No primary study was found that compares test–retest or inter-method reliability (ICC) of mean vs max vs quantile vs excursion curvature for coronary centerlines. This is a real gap. The thesis's Medis comparison could supply such agreement data for each candidate summary, outside the plaque-free cohort.

## 4. Smoothing noisy curvature from discrete centerlines; choosing the scale without the outcome

### Takeaway
Curvature needs second derivatives, so smoothing is mandatory. The established statistical approach is local polynomial or spline regression of each coordinate on arc length, with degree ≥ p+2. The bandwidth is chosen by goodness-of-fit versus roughness, or by agreement with a reference, never by outcome association. AneuRisk used a Gaussian-kernel local polynomial of degree 4 with bandwidth 3 (on an approximate mm arc-length axis). Results were insensitive to bandwidths near 3; 0.1 overfitted noise and 6 flattened peaks.

### Cited Findings
- Sangalli et al. 2009 used Gaussian-kernel local polynomial regression of x(s), y(s) and z(s). The degree was 4, by the rule p + 2 where p = 2 is the highest derivative needed. The bandwidth of 3 was chosen by a "Goldilocks approach", balancing average squared error against a roughness measure (the integral of squared second derivatives). They report that "variations of the bandwidth in a reasonable neighborhood of 3 do not appreciably affect the subsequent analyses". A free-knot regression spline alternative is in Sangalli et al. (2007). — [Sangalli et al. 2009](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- A vessel-morphology preprint (arXiv 2607.14195, not peer-reviewed) notes that centerline extraction leaves coordinate noise. It applies a Gaussian filter (sigma = 1) before computing invariants, and argues that fixed-window finite differences amplify noise, especially third derivatives (torsion). It does not test the sensitivity to sigma. — [arXiv 2607.14195 (preprint)](https://arxiv.org/pdf/2607.14195)
- Goldsmith et al. 2011 handle error in the functional predictor by projecting it onto smooth eigenvectors (FPCA smoothing) before estimating beta(s). In the testing comparison, the KSM FPC-score F-test was the only nullity test described as suitable for sparse, error-contaminated predictors; the penalized-spline LRT assumes dense, error-free curves. — [core.ac.uk Goldsmith](https://core.ac.uk/download/61318164.pdf); [ar5iv 1710.05729](https://ar5iv.arxiv.org/html/1710.05729)

### Inferences
- **Outcome-blind scale choice options.**
  - (i) Generalized cross-validation or REML smoothing of each centerline's coordinates. This is per curve, data-driven and outcome-free.
  - (ii) A fixed window in mm justified physically, e.g. a few lumen diameters (proximal coronary diameter about 3–4 mm), so that sub-diameter wiggles from tracer jitter are not counted as bends.
  - (iii) Choose the scale that maximises tracer–Medis agreement of the curvature summary. It is outcome-free, but it lies outside the plaque-free cohort and Medis is a reference, not ground truth.
  - (iv) A roughness-versus-fit plot as in AneuRisk.
  Freeze the choice before the outcome is linked, in line with the plan to freeze the method before the outcome.
- Smooth the curve in 3D (coordinates on arc length), not the curvature signal after the fact. Frenet-frame curvature from raw points with finite differences is noise-dominated. Torsion is worse and probably should not be used.
- **Measurement error in X attenuates beta toward zero**, both for scalar summaries and for functional terms. Pre-smoothing reduces the variance part, but bias from tracer path errors (e.g. corner-cutting) is not removed. A reliability estimate (e.g. from the Medis comparison) would allow a regression-calibration sensitivity analysis.

### Gaps
- No coronary-CT study found that reports how curvature statistics change with the smoothing window, or recommends a window in mm.

## 5. Applications of functional regression to vessel geometry or similar medical curves

### Takeaway
The AneuRisk project (carotid siphon, 65 patients) is the main precedent for functional analysis of vessel radius and curvature profiles: registration, FPCA, then classification of aneurysm location. It is small and cross-sectional, and its outcome is not prospective. The same group related curvature to wall shear stress with function-on-function regression. No functional regression of coronary curvature profiles on incident plaque was found.

### Cited Findings
- AneuRisk / Sangalli et al. 2009 JASA: 65 patients (33 with an aneurysm at or after the ICA terminal bifurcation, 25 with an aneurysm along the ICA, 7 healthy). Registered radius and curvature profiles were analysed by FPCA, then QDA on FPC scores, with a leave-one-out misclassification of about 21.5%. — [Sangalli et al. 2009](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- The same group studied the relationship between ICA curvature and wall shear stress using function-on-function regression (MOX reports). — [MOX report 24/2007](https://www.mate.polimi.it/biblioteca/add/qmox/24-2007.pdf); [MOX publication list](https://mox.polimi.it/reports-and-books/publication-results/?id=149)
- Penalized functional regression's original application was DTI tract profiles (fractional anisotropy along a white-matter tract) predicting MS outcomes. This is an anatomical "profile along a path", analogous to curvature along a vessel. — [Goldsmith et al. 2011](https://core.ac.uk/download/61318164.pdf)
- Carotid tortuosity on CT angiography independently predicted 90-day functional outcome after anterior-circulation stroke (scalar tortuosity, not functional). — [search summary; primary not retrieved](https://mail.ijrr.com/article-1-6807-en.pdf)
- Coronary lesion-prediction patents describe Frenet curvature along centerlines and smoothed area-vs-arc-length profiles. They describe intended methods and report no validated performance. — [US patent 11663715](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11663715)

### Inferences
- The precedents support the *technique* (smoothing, registration, FPCA of vessel profiles). They do not show that functional predictors beat scalar summaries for clinical outcomes in vessels. The thesis should not claim that.

### Gaps
- No prospective study was found that uses a functional curvature or radius profile to predict incident atherosclerosis (coronary, carotid or aortic). No retinal-vessel functional regression study was retrieved within budget.

## 6. Sample size and power: functional predictor vs scalar summaries (~1,000 people, ~450 events)

### Takeaway
No source gives power for functional predictors with a binary outcome at this sample size. Simulation evidence shows well-sized tests at n = 500 for continuous outcomes. The general principle holds: power depends on how well the chosen summary or basis aligns with the true beta(s). With about 450 events and 9 correlated segments per person, the effective information is closer to 450 events than to 9 × 1,000 segment-observations. A few prespecified FPC scores or quantiles per curve type is affordable. A per-segment or per-artery beta(s) is not.

### Cited Findings
- Tekbudak et al. used n = 50, 100 and 500 (continuous response). Nullity tests had good size and power at n = 500, and FPCA-based tests degraded with sparse or few points. — [ar5iv 1710.05729](https://ar5iv.arxiv.org/html/1710.05729)
- A 2026 arXiv preprint ("PCA score regression: the art of losing power", arXiv 2605.24118, not peer-reviewed) argues for function-on-scalar regression (the reverse direction) that regressing PC scores is a misspecified model with power loss. The loss depends on how the PCs correlate with the true effect, and uncorrected multiplicity inflates alpha (about 0.06–0.08). It is relevant only by analogy. — [arXiv 2605.24118 (preprint)](https://arxiv.org/pdf/2605.24118)

### Inferences
- **Rough budget.** Using the common 10–20 events-per-parameter heuristic (not verified this session for GLMMs), about 450 events support roughly 20–45 parameters in total, including the SCORE2 base and 8 segment intercepts. Each scheme then costs:
  - 2 curves (curvature, taper) × 1 shared beta(s) × K = 3 FPC scores: 6 df;
  - the same with beta varying by artery (3): 18 df;
  - a per-segment beta(s) (9 segments): 54 df, which is too many.
- **The scalar-summary block is the efficient choice if beta(s) is roughly flat.** If the risk is driven by a localised feature (e.g. one sharp proximal bend), the mean dilutes it, and an upper quantile, excursion length or a low-K FPC set captures more of it. A defensible design: prespecify the primary geometry block as summaries or FPC scores (fixed df, one LR test), and fit the penalized functional beta(s) as a descriptive or secondary analysis with no test.
- The segment GLMM already gives within-artery spatial resolution (9 segments), a coarse step-function beta(s). A functional term inside each segment adds resolution only at the sub-segment scale (millimetres to centimetres). That is also the scale where tracer noise is largest.

### Gaps
- No simulation found of scalar-on-function power with a binary or cloglog outcome, clustered data and about 450 events. A thesis-specific simulation (generate beta(s) shapes, compare the mean vs quantile vs K-FPC vs pfr LR power) would be needed for any quantitative power claim.
