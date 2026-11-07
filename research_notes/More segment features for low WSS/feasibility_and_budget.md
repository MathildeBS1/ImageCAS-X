# Feasibility and statistical budget for adding segment-level geometry features

Local context used (from project files, not the web):
- Current cohort counts: 1,077 plaque-free participants, 483 (44.8%) developed plaque in at least one segment (`thesis/results/00_cohort.tex`; counts are before the image-quality exclusion and are flagged there to be recomputed). 452/483 (93.6%) had it in a trunk (project memory, `results/00_cohort.tex`).
- Older planning reports in `~/Desktop/Speciale/CGPS_statistics-/reports/` (`Experiment setup who and where.md`, `Coronary geometry and new plaque.md`, `Segment plaque risk model nonlinearity.md`) use superseded numbers (n = 1,352, 626 or 668 person events). Their budget arguments should be re-run on 1,077 / 483 and on the final study cohort after image-quality exclusion.
- The plan's sample-size item says "about 15–20 parameters fit at an anticipated C of about 0.70 (Riley ...)" (`CGPS_statistics-/CLAUDE.md`, item 11). That figure came from the planning team's own simulated Riley shrinkage calculation, which the report says must be confirmed in pmsampsize before it is quoted.

## Q1. How much does LR-test power fall when k extra weak predictors join the geometry block?

### Takeaway
A block LR test spends power on every added df. With the current 5-df block at 80% power, each added df needs roughly 0.7–0.8 units of extra noncentrality (about 6% of the block's whole signal) just to break even. Null or redundant additions lower power: about 80% → 74% for +2 df and → 68% for +5 df. The df cost is modest but real. A feature that is collinear with curvature or taper, or measured noisily, will not pay for its df.

### Cited Findings
- The power of an LR test of a block is 1 − F_ncχ²(critical value; df, λ), where λ is approximated by the expected LR χ². Power therefore depends on both df and λ. — [USGS model comparison power tool](https://www.mbr-pwrc.usgs.gov/software/power.html)
- Harrell's rule is to decide first how many df can be spent, then where to spend them, and then spend them (RMS §4.0). He recommends testing a whole prespecified group of predictors with a single P-value, and not removing individual insignificant effects (§4.12.1 items 8–9). — [Harrell, RMS ch. 4](https://hbiostat.org/rmsc/multivar)
- Harrell's limiting sample size for a binary outcome is m = 3nq(1−q), with candidate parameters p < m/15. The rule comes from simulations in typical low signal-to-noise settings (§4.4). — [Harrell, RMS ch. 4](https://hbiostat.org/rmsc/multivar)
- Riley et al. 2020 set three sample-size criteria: expected shrinkage of at most 10% (shrinkage ≥ 0.9), a gap between apparent and adjusted Nagelkerke R² of at most 0.05, and average risk estimated within ±0.05. They are implemented in pmsampsize, which needs an anticipated (adjusted) R² from prior work or derived from a C statistic. — [Riley et al., BMJ 2020;368:m441](https://doi.org/10.1136/bmj.m441); [pmsampsize docs](https://rdrr.io/pkg/pmsampsize/man/pmsampsize.html)
- EPV is a weak guide to out-of-sample performance. The number of predictors, the total n and the events fraction matter more. — [van Smeden et al., SMMR 2019](https://doi.org/10.1177/0962280218784726) (as cited in the project's `research_notes/Experiment setup who and where/missing_power_prespecification.md`)
- In clustered logistic prediction models, simulations showed that the degree of clustering mattered far less than EPV. — [Wynants et al. 2015](https://researchinformation.umcutrecht.nl/en/publications/a-simulation-study-of-sample-size-demonstrated-the-importance-of-/) (as cited in the project's `reports/Segment plaque risk model nonlinearity.md`)
- Penalisation is not a carte blanche. Tuning and shrinkage parameters are themselves estimated with uncertainty, and the methods are least reliable when they are most needed (small effective n, low R²). — [Riley et al., J Clin Epidemiol 2021;132:88–96](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8026952/)
- The follow-up paper recommends penalisation only in data that already meet minimum sample-size criteria, and recommends quantifying the variability of tuning. — [Riley et al., SMMR 2021](https://journals.sagepub.com/doi/reader/10.1177/09622802211046388)
- Harrell prefers fitting all prespecified candidates with shrinkage over variable selection. Stepwise selection gives biased β, SEs and P-values that are too small, and χ² statistics that lose their claimed distribution (§4.3, §4.5). Do not penalise the variable of interest (§4.12.2). — [Harrell, RMS ch. 4](https://hbiostat.org/rmsc/multivar)
- Data reduction that is masked to Y (variable clustering, PC1 summary scores, redundancy analysis) does not distort P-values or CIs and can shrink a large candidate set to a few df before the outcome is touched (§4.7). — [Harrell, RMS ch. 4](https://hbiostat.org/rmsc/multivar)
- Power falls as null noise features are added to a test (shown for a Wilcoxon-based feature test, so only an analogy here). — [arXiv 2511.20851](https://arxiv.org/pdf/2511.20851)

### Own calculation (noncentral χ², α = 0.05; illustrative and not from a source)
Python/scipy, λ fixed for the 5-df block:

| Block df | Power if added df carry **no** signal (base 80%) | Base 50% | Power if each added df carries **half** the per-df signal of the original block, independent of it (base 80%) |
|---|---|---|---|
| 5 | 0.80 | 0.50 | 0.80 |
| 6 | 0.77 | 0.47 | 0.82 |
| 7 | 0.74 | 0.44 | 0.83 |
| 8 | 0.72 | 0.42 | 0.85 |
| 10 | 0.68 | 0.38 | 0.88 |
| 15 | 0.59 | 0.31 | 0.93 |

The noncentrality needed for 80% power is 12.83 (5 df), 13.62 (6), 14.35 (7), 15.02 (8), 16.24 (10) and 18.81 (15). The "half signal" column is optimistic: it assumes new information *independent* of curvature and taper. Features correlated with them add less λ than their df cost. Measurement error lowers λ further, because the noncentrality scales roughly with the squared attenuated effect.

### Inferences
- Budget, recomputed on the current numbers: person level m ≈ 3 × 1,077 × 0.448 × 0.552 ≈ 800, so m/15 ≈ 53 df. The person-level budget is therefore not the binding constraint for a few more geometry terms. **Power of the single LR test is the binding constraint**, along with interpretability and the dilution of the primary hypothesis.
- At segment level, nominal events overstate information. The planning reports estimate a design effect of about 1.8–3.4 (ICC 0.1–0.3, 9 segments), but the ICC has not been estimated for this outcome. For the "where" conditional logistic model, only people with discordant segments (at least one segment with and one without plaque) contribute. Its information is roughly the 452 people with trunk plaque, and less if many people have plaque in all 9 trunks, which is unlikely.
- Practical rule: add a feature to the *primary* block only if (a) it is a prespecified, mechanistically distinct hypothesis, (b) its expected correlation with curvature, taper, angle and ratios is low (check this masked to Y, e.g. by Harrell varclus on the baseline features), and (c) its measurement reliability is adequate (Q2). Everything else goes into a secondary, explicitly exploratory analysis.
- Prespecification only protects the test if the block is fixed before any outcome is looked at. Project memory notes tracer output for about 1,200 plaque-free people is coming, so "freeze method before outcome" applies to the feature list too.

### Gaps
- I found no published formula or simulation for LR-test power in a cloglog GLMM or in conditional logistic regression with a multi-df block. The noncentral-χ² table above is a large-sample approximation. Simulation in the actual design (as the plan already proposes) is the proper check.
- No published anticipated R² or C for SCORE2 predicting incident subclinical plaque was found (the planning reports say the same). pmsampsize inputs remain assumptions.
- The full text of the van Smeden and Wynants papers was not re-verified in this session; they are cited through the project's earlier notes.

## Q2. How reproducible are the candidate features on CCTA, and which are too noisy?

### Takeaway
Reproducibility evidence is thin and mostly comes from semi-automated software, phantoms, carotid arteries or diseased segments. For several candidates (torsion, coronary curvature with an ICC, side-branch counts, automated V/M) I found **no** coronary-CCTA reproducibility data. Large-scale, length-integrated quantities (segment length, tortuosity index, lumen volume, LM bifurcation angle) look the most robust. Derivative-based quantities (torsion above all) and anything that depends on small side branches look the least robust. For this tracer, the Medis comparison is the only reliability evidence available, and Medis is not ground truth.

### Cited Findings
**Bifurcation angles**
- In a phantom, the interobserver mean difference for CCTA bifurcation angle was 1.8 ± 5.8° (N = 135 measurements). — [Phantom study, ResearchGate](https://researchgate.net/publication/322544209_Measurement_of_coronary_bifurcation_angle_with_coronary_CT_angiography_A_phantom_study)
- In a CT-derived projection study, interobserver bifurcation-angle differences were < 3°. — [JACC Cardiovasc Interv 2020](https://www.jacc.org/doi/10.1016/j.jcin.2020.06.042)
- A 2026 review says CCTA allows reproducible measurement of main-vessel–side-branch angle and bifurcation curvature. This is a review claim, not primary data. — [J Clin Med 2026 review](https://doi.org/10.3390/jcm15124565)
- A CCTA-SYNTAX paper notes that judging bifurcation angulation and tortuosity in 3D is harder than in 2D. — [JCCT CT-SYNTAX](https://www.sciencedirect.com/science/article/pii/S1934592523004628)

**Curvature and tortuosity**
- Tuncay et al. (73 asymptomatic PAD patients, dual-source CT, semi-automatic centerlines) report per-segment curvature with median 0.094 [0.071–0.120] and tortuosity with median 1.08 [1.04–1.12]. Curvature was 16.7% higher in stenotic segments. The abstract gives no ICC or interobserver values ("Observer Variation" appears only as a keyword). — [Tuncay et al., JCCT 2018;12(3):257–260](https://researchinformation.umcutrecht.nl/en/publications/non-invasive-assessment-of-coronary-artery-geometry-using-coronar/)
- Carotid CTA tortuosity index (12 patients, 4 software packages): interobserver ICC 0.72–0.99, intraobserver 0.85–1.0, between-package ICC 0.95–0.99. This is a larger, straighter vessel and a tiny sample. — [de Vries et al., Neuroradiology 2019](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6348067/)
- In a sensitivity analysis of centerline curvature and torsion algorithms (internal carotid), centerline *resolution* strongly changed the results, and one algorithm was vulnerable to noise and smoothness. — [BioMed Eng Online 2021](https://0-biomedical--engineering--online-biomedcentral-com.brum.beds.ac.uk/counter/pdf/10.1186/s12938-021-00957-6.pdf)
- Penalised-spline fitting of centerlines reduced curvature and torsion error compared with conventional fitting. — [Fujita Health Univ.](https://pure.fujita-hu.ac.jp/en/publications/a-penalized-spline-fitting-method-to-optimize-geometric-parameter/)
- Coronary curvature and torsion estimation methods were accurate (< 2.15% error) on phantoms and on angiography+IVUS fusion, not on CT. — [SPIE 2004](https://iro.uiowa.edu/esploro/outputs/conferenceProceeding/Curvature-and-torsion-estimation-for-coronary-artery/9984186694002771)

**Lumen area, diameter and eccentricity**
- Manual CCTA minimal lumen area: interobserver ICC 0.44–0.73 among five observers, and very weak correlation with IVUS (r 0.15–0.28). — [Search summary of a stable-angina CCTA–IVUS study (PMC4442169)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4442169)
- With semi-automated plaque software, interobserver CCC was 0.99 for MLA and 0.98 for MLD. Inter-observer relative differences were 1.2% for lumen area and 0.6% for vessel area. — [eScholarship](https://www.escholarship.org/content/qt81g7n8rg/qt81g7n8rg.pdf?t=rvzz3q); [Erasmus repub 66634](https://repub.eur.nl/pub/66634/Repub-66634.pdf) (from search summaries; full texts not checked)
- Against IVUS, a CT segmentation study reported RMS error of 16.2% for cross-sectional area and 9.5% for diameter. Another validation reported a 21% lumen-area error. — [IVUS validation of CT lumen area](https://scholarworks.indianapolis.iu.edu/items/7b610c06-b87f-434f-ac68-aa731704c17b)
- In calcified lesions, CTCA overestimated the maximum lumen diameter in the smallest tertile (mean diameter about 2.1 mm) and underestimated it in the largest. — [Termedia 2013](https://www.termedia.pl/Original-paper-Lumen-and-calcium-characteristics-within-calcified-coronary-lesions-Comparison-of-computed-tomography-coronary-angiography-intravascular-ultrasound,35,20448,0,1.html)
- A 2026 photon-counting vs energy-integrating CT study restricted its IVUS comparison to lumens ≥ 2 mm (preliminary abstract). — [ESC 365](https://esc365.escardio.org/journal/91099)
- I found no reproducibility data specifically for lumen *eccentricity or ovality* on CCTA.

**Lumen volume / myocardial mass (V/M)**
- In NXT (n = 238), low V/M went with lower FFR, independent of plaque. — Taylor et al., JCCT 2017, via [SCCT summary](https://cdn.ymaws.com/scct.org/resource/resmgr/jcct_podcast_links/Cardiac_computed_tomography-.pdf)
- V/M was weakly associated with hyperaemic MBF and FFR (n = 152). — van Diemen et al. 2019, via [Leiden repository](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- V/M is framed as a supply–demand measure, also changed by myocardial disease. — Ihdayhid et al., JCCT 2022 review, via [Galway repository](https://research.universityofgalway.ie/en/publications/cardiac-computed-tomography-derived-coronary-artery-volume-to-myo/)
- V/M needs LV myocardial segmentation, which the tracer does not provide. I found no reproducibility data for V/M.

**Myocardial bridging**
- CCTA detection rates are mostly 15–50%, with a pooled CTCA figure of about 22%, against about 42% at autopsy and about 6% at invasive angiography. — [PMC3528862](https://pmc.ncbi.nlm.nih.gov/articles/PMC3528862); [Rom J Cardiol 2024](https://reference-global.com/download/article/10.2478/rjc-2024-0016.pdf)
- Most bridges are superficial (94.3% in one CT cohort). — [Rom J Cardiol 2024](https://reference-global.com/download/article/10.2478/rjc-2024-0016.pdf)
- Dual-source CT detected 87.8% of LAD bridges found at dissection. — [PubMed 25085008](https://pubmed.ncbi.nlm.nih.gov/25085008/)
- Bridging is a myocardium-relative finding. Centerline plus lumen alone cannot detect it.

**Side branches**
- Automatic extraction methods trade sensitivity for distal parts and side branches. — [Int J Cardiovasc Imaging 2011](https://link.springer.com/doi/10.1007/s10554-011-9894-2)
- Coronary radius varies about fivefold from proximal to distal. — [DeepCenterline, arXiv 1903.10481](https://arxiv.org/pdf/1903.10481)
- I found no paper giving side-branch detection sensitivity stratified by branch diameter. Side-branch *counts* therefore depend on the tracer's detection threshold.

### Inferences (my assessment, ranked from most to least feasible with centerline + lumen contours)
1. **Segment length and distance from the ostium**: integrals along the centerline, robust to local noise but dependent on where landmarks and segment boundaries are placed (the split rule in `split_trunks.py`). Log length is already in the "where" base, and distance from the ostium is largely collinear with segment position, so as a new block term it mostly re-tests position.
2. **Tortuosity index** (arc length / chord): robust, but nearly redundant with mean curvature over a segment. Add only one of the two.
3. **Lumen area/volume (mean over the segment)**: integrating over many contours reduces noise. It is biased in small lumens (< ~2 mm), and it is strongly confounded by body size, sex and dominance (Q3). It is already partly encoded by taper and the diameter ratios.
4. **LM→LAD/LCx side-branch angles** beyond the LM bifurcation: feasible for large branches (D1, OM1) if the tracer reliably finds them. For smaller branches, detection itself is uncertain.
5. **Lumen eccentricity/ovality**: needs contours that resolve shape at sub-voxel level. At about 0.5 mm voxels in a 2–3 mm lumen, the minor/major axis spans only about 4–6 voxels, so the ratio is plausibly dominated by contour noise and reconstruction kernel. There are no CCTA reproducibility data. Not advisable as a primary term.
6. **Torsion**: a third-derivative quantity, highly sensitive to centerline sampling and smoothing. There are no coronary CCTA reproducibility data. Not advisable.
7. **Side-branch counts, V/M, myocardial bridging**: depend on detection thresholds or on myocardium segmentation that the current pipeline does not produce. Not feasible as primary terms.
- Measurement error matters for both questions. Random error attenuates the coefficients and lowers LR power. For "who", a person mean over noisy segments carries extra error. The Medis comparison (01b) can give an *indirect* agreement estimate for curvature- and lumen-type features on the LAD, LCx and RCA, and only in plaque-at-baseline people. It cannot establish reliability in the plaque-free cohort.
- Measurement heterogeneity (e.g., between scanners or protocols over the baseline period) can miscalibrate models. — [Luijken et al., Stat Med 2019](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6619392/); [Luijken et al., J Clin Epidemiol 2020](https://researchinformation.umcutrecht.nl/en/publications/changing-predictor-measurement-procedures-affected-the-performanc/)

### Gaps
- No coronary-CCTA ICC or test–retest values were found for curvature, torsion, tortuosity index, eccentricity, side-branch counts or V/M.
- No inter-scanner reproducibility for any of the geometric features was found.
- Several lumen-reproducibility figures above come from search summaries of abstracts, and the full texts were not checked.
- Whether the in-house tracer's contours resolve shape (eccentricity) at all is unknown. Any reproducibility study of the tracer itself was not available to me.

## Q3. Is lumen size in a plaque-free segment confounded by vessel size, sex, body size or dominance? How is it normalised?

### Takeaway
Yes. In CT studies of normal arteries, lumen dimensions depend on sex and dominance, and partly on body size and LV mass. Indexing to BSA removes some but not all of the sex difference. Raw lumen area would largely proxy sex, body size and dominance, and SCORE2 already contains sex. Ratio-type measures (taper, daughter/mother diameter ratios) are partly self-normalising, which is an argument for them over absolute area.

### Cited Findings
- In 201 CT subjects without atherosclerosis, lumen areas and diameters were generally smaller in women (except the proximal RCA and LM). Both sex and dominance pattern affected normal values, and reference values were given by sex and dominance. — [Am J Cardiol 2018 (em-consulte)](https://em-consulte.com/article/1208261/article/measurements-of-lumen-areas-and-diameters-of-proxi)
- In a Danish CT volumetric study, sex was not independently related to coronary artery volume. LV mass correlated strongly, independent of BSA and sex. — [KU Pure](https://test01.ku.dk/:obvius/pureproxy/3974268/en/publications/volume-and-dimensions-of-angiographically-normal-coronary-arterie)
- Unadjusted proximal LAD and RCA cross-sectional areas were smaller in women, and the difference was not significant after adjustment. The authors note that differences can persist after normalising for BSA and cardiac mass. — [Clin Cardiol 2010, PubMed 20043337](https://pubmed.ncbi.nlm.nih.gov/20043337/)
- Angiographic study: after BSA adjustment, the LM and LCx were *narrower* in men, a reversed pattern. — [Turk Gogus Kalp Damar Cerrahisi Derg](https://tgkdc.dergisi.org/abstract.php?id=3343)
- An Indian angiographic study found no sex difference after BSA indexing. — [JCDR](https://www.jcdr.net/articles/PDF/7849/18096_CE(ra1)_F(GH)_PF1(ROAK)_PFA(AK)_PF2(PAG).pdf)

### Inferences
- If lumen area is added, normalise within the model rather than by a fixed index. One way is to include BSA (or height/weight, both available in BL) plus sex as adjusters for the lumen term. Another is to use within-person relative measures (segment area / the person's LM or proximal area), which is essentially what the diameter ratios already do.
- In the "where" conditional model, person-level confounders (sex, BSA) cancel out, but dominance × vessel does not, and it is already in the base. A segment's absolute area is then strongly tied to its position, so the information left beyond position + log length is probably small.
- In the "who" pooled model, absolute lumen size would partly re-enter sex and body size, which SCORE2 covers only through sex. This makes any LR gain hard to read as "geometry".

### Gaps
- No study was found on lumen size normalisation specifically in a plaque-free population followed for incident plaque.
- The CT normal-value studies are single-centre with about 50–200 subjects, and the full-text tables were not checked.

## Q4. How to keep the primary test small while running secondary exploratory features?

### Takeaway
Keep the prespecified primary LR test on the current 5-feature block, unchanged. Put new features in a separate, prespecified *secondary* analysis that is labelled exploratory. Use estimation (effect sizes with CIs, ΔC and calibration) rather than more confirmatory tests. Reduce the secondary features masked to Y (clustering or summary scores) or fit them with penalisation, and report them without multiplicity-adjusted claims of confirmation.

### Cited Findings
- Harrell's sequence: decide the df to spend, prespecify, test the group with one global test, and stop if it is not significant (§4.0, §4.3, §4.12.1). — [Harrell, RMS ch. 4](https://hbiostat.org/rmsc/multivar)
- Harrell: data reduction masked to Y (varclus, PC1 per cluster, redundancy analysis) keeps inference valid. Use shrinkage if the heuristic shrinkage (χ² − p)/χ² is below 0.9 (§4.7, §4.7.7). — [Harrell, RMS ch. 4](https://hbiostat.org/rmsc/multivar)
- Variable selection gives a type I error of 0.39 for the first entered variable among 10 null orthogonal predictors at nominal α = 0.05 (Harrell §4.3 footnote). — [Harrell, RMS ch. 4](https://hbiostat.org/rmsc/multivar)
- Penalisation needs adequate n and reporting of the tuning variability. — [Riley et al. 2021 JCE](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8026952/); [Riley et al. 2021 SMMR](https://journals.sagepub.com/doi/reader/10.1177/09622802211046388)

### Inferences
- Concrete structure for the thesis:
  1. **Primary**: the current 5-feature block, one LR test per question, as decided.
  2. **Secondary (prespecified, exploratory)**: at most 1–3 extra features chosen *before* any outcome is seen, on mechanistic grounds and reliability (e.g., segment-mean lumen area adjusted for BSA and sex, or tortuosity index, but not both curvature and tortuosity). Report each one's coefficient with its CI, and the change in log-likelihood when it is added to the primary model. Do not make a new confirmatory claim, and if any P-values are shown, label them as such.
  3. **Sensitivity**: features with poor or unknown reliability (eccentricity, torsion, side-branch counts) only as descriptive or sensitivity analyses, if at all.
- Do not let secondary results feed back into the primary block. That would be data-driven selection after the fact, with the inference problems Harrell describes.
- State explicitly in the thesis which analyses were prespecified and when the feature list was frozen relative to unblinding the outcome.

### Gaps
- No guidance specific to GLMM or conditional logistic models was found on splitting primary and secondary feature blocks. The general prediction-modelling principles above are assumed to carry over.
