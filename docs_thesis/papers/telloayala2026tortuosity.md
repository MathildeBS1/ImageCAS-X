# telloayala2026tortuosity — A Machine Learning Driven Approach to Quantifying Coronary Artery Tortuosity

**Citation:** Tello Ayala, Supriami, Swaroop, Friedman, Unlu, Halford, Maddah, Abou-Karam,
Pomerantsev, Ellinor, Doshi-Velez, Fahed. *JACC: Advances* 2026;5(6):102829.
doi:10.1016/j.jacadv.2026.102829. PMC13308244.
**Read:** 2026-09-18 — full text (PMC HTML), methods, results, limitations, abstract. Supplemental
tables (e.g. Table 12's AUROC methodology, Table 10's classical-index correlation) referenced in
text but not opened — not accessible through this pass.
**Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/
**Verdict:** The only paper found (two search passes, several query angles) where a model operates
on the ordered per-point tortuosity profile along a centerline rather than a pre-reduced scalar —
relevant as prior art for a possible objective 8/9 representation-learning angle, but built on 2D
single-plane invasive angiography, RCA only, and with a circularity risk in its CAD label that the
authors do not address.

## What they did

Retrospective single-center study, Massachusetts General Hospital cardiac catheterization registry,
81,798 angiograms / 31,513 patients, 2000–2021. Restricted to RCA angiograms in LAO projection
(primary angle −10° to 100°), using the middle 20 frames of each loop (peak diastolic epicardial
flow). Of 49,189 eligible LAO RCA loops, excluded for no loop in LAO view (n=5,172), poor
quality/artifacts (n=1,438), inappropriate RCA length from magnification/panning (n=2,569).
**Final analysis cohort: 38,691 angiograms from 22,334 patients** (64.7±12.5 y, range 30–102, 37%
female, 83.7% White, 85.5% hypertension, 32.4% type 2 diabetes). Segmentation succeeded in 78.7%
of the 49,189 eligible loops.

Pipeline: U-Net trained on the external ARCADE dataset (1,500 labeled frames; 1,000 train / 500
held-out validation, threshold chosen to maximize Dice) segments the RCA; masks are skeletonized to
a centerline; the main branch is taken as the longest path from RCA origin to the distal PDA end;
loops are kept only if the skeleton has ≥20 discrete points with no interruption.

Tortuosity: discrete curvature at each skeleton point x_i is the turning angle between edge
x_(i-1)x_i and edge x_i,x_(i+1), absolute value, normalized by π → per-point score in [0,1]; the
global scalar is the mean of these. A "local-attention neural network transformer" instead takes
the full ordered tortuosity vector plus age and sex, trained to discriminate CAD presence in the
RCA. Compared against a logistic regression baseline using only the global scalar plus age/sex.
Architecture details (layers, heads, loss, exact train/val/test partition) are not given in the
main text; Supplemental Table 12 is cited for the AUROC methodology but was not accessible here.

CAD label: "any presence of stenosis (mild or more) in the RCA," a **qualitative call by the
interventional cardiologist performing the same angiogram** — the identical LAO frames used to
compute tortuosity, not an independent quantitative coronary angiography measurement.

## What they found

- Cardiologist concordance (300 angiograms, blinded, stratified by decile — bottom decile
  "low," top decile "high," middle 8 "average," dichotomized nontortuous vs tortuous): low-tortuosity
  precision 85.6% / recall 83.5% / F1 84.6% (n=200); high-tortuosity precision 75.3% / recall 58.0%
  / F1 65.5% (n=100); Cohen's κ = 0.52 (95% CI 0.41–0.63), moderate agreement.
- CAD discrimination: transformer (local profile + age + sex) AUROC 0.67 (95% CI 0.65–0.69) vs.
  logistic regression (global scalar + age + sex) AUROC 0.60 (95% CI 0.58–0.63). **No significance
  test (e.g. DeLong) for this comparison is reported anywhere in the accessible text** — the CIs do
  not overlap (0.65 > 0.63), but that is not the same as a stated test.
- Adjusted associations (covariates: age, sex, hypertension, T2D, hypercholesterolemia, smoking, RCA
  stenosis): female sex β=0.17 (95% CI 0.14–0.20, P<.001, higher tortuosity); hypertension β=0.06
  (0.02–0.10, P=.002); T2D β=−0.11 (−0.14 to −0.08, P<.001, lower); hypercholesterolemia β≈0.00
  (P=.900, null); smoking β=−0.02 (P=.216, null); age lost significance after adjustment (P=.121,
  vs. β=0.02/SD, P<.05 unadjusted) — authors read this as age's apparent effect being cumulative
  risk-factor exposure, not age itself. Sex×age interaction β=0.04/SD of age (0.02–0.07, P=.002),
  steeper rise in women.
- CAD: OR 1.05/SD (P<.001) for any RCA stenosis, OR 1.09/SD (P<.001) for severe CAD (mild/moderate
  not significant, P=.154/.956); Gensini score β=0.05/SD (0.04–0.07, P<.001).
- Global tortuosity range across the cohort: 0.007–0.289 (from the abstract; not broken out further
  in the body text I read).
- Correlation between this discrete-curvature score and the classical arc-length/chord-length index:
  r=0.116 (Supplemental Table 10, cited but not opened) — the two families of tortuosity formula
  barely agree.

## What the abstract does not tell you

- **The CAD label and the tortuosity measure come from the same image, read by the same person at
  the same time.** The abstract states the OR and moves on; nowhere in the accessible text do the
  authors flag that a cardiologist's qualitative stenosis call on an angiogram could be influenced
  by, or correlated with, the vessel's visible curvature on that same angiogram — the paper does not
  concede this as a limitation. This is the single largest gap between what the headline OR implies
  ("tortuosity predicts CAD") and what the design can actually support.
- **This is a 2D projection measurement, not a 3D one, and the paper never says so.** Tortuosity is
  computed on the centerline of a single-plane fluoroscopic projection (LAO view). Foreshortening,
  out-of-plane vessel course, and view-angle dependence are known confounds for any 2D angiographic
  shape measurement and are not discussed anywhere in the accessible text — not in methods, not in
  limitations. A vessel with real 3D tortuosity can appear foreshortened-straight in one projection
  and a vessel with a simple 3D curve can appear tortuous if it runs partly along the viewing axis.
- **Segmentation succeeded in only 78.7%** of eligible loops (38,691 / 49,189); the authors attribute
  failures to "suboptimal frame rate or limited orthogonal views" but do not test whether failed
  segmentations were disproportionately the more tortuous or more complex cases — if so, the analyzed
  cohort's tortuosity distribution is right-truncated relative to the true population, which matters
  specifically for any outlier/tail analysis built on top of a measure like this.
- **AUROC 0.67 vs 0.60 has no stated significance test.** The confidence intervals do not overlap,
  which is suggestive, but the paper does not report a DeLong test or equivalent, so "the local model
  is better" is asserted from CI non-overlap, not demonstrated with a paired test on the same
  patients.
- **Limitations section, as stated:** RCA-only ("may not fully capture the more complex branching of
  the left coronary system"), retrospective design ("can introduce selection bias and variability in
  imaging protocols"), no duration/time-on-treatment data for risk factors, prospective validation
  and left-system extension left to future work. Left system explicitly deferred because of "more
  complex bifurcations and more frequent overlap and foreshortening" — i.e. the authors know
  foreshortening is a problem for the *left* system, but do not connect this to the *RCA* measurements
  they did report.
- No code or data release stated anywhere in the accessible text.

## What it licenses

- Citable as the only found instance of a model operating on the **ordered per-point tortuosity
  profile** rather than a scalar summary, and getting a real (if modest, non-formally-tested) AUROC
  gain from it (0.67 vs 0.60) — usable as a one-sentence existence proof that keeping per-position
  structure carries some signal a global mean discards, motivating (not validating) a
  representation-learning approach to tortuosity for objective 8/9.
- Citable for the caution already in `literature.md`/`state_of_the_art_plan.md` that different
  hand-crafted tortuosity formulas disagree: their discrete-curvature score correlates only r=0.116
  with the classical arc-length/chord-length index, in the largest tortuosity cohort found to date
  (n=22,334 patients). Strengthens the existing "state formulas as formula-specific, not as
  tortuosity itself" framing.
- The population-scale correlates (sex, hypertension, diabetes, CAD presence/severity, Gensini score,
  all at n>20,000 with adjustment) are citable as the largest single tortuosity-covariate association
  study found, useful as an external prior for what a CGPS tortuosity-vs-comorbidity check should
  roughly look like in direction and rough magnitude, RCA-only.

## What it does NOT license

- Does **not** validate a representation-learning approach for the 3D, CTA-derived centerlines this
  thesis actually has (`centerlines/` VTK, ImageCAS-X). This paper's centerline is a 2D single-plane
  projection curve; the geometry, the noise sources (foreshortening, cardiac motion within the
  20-frame window), and the failure mode (78.7% segmentation success, unknown tortuosity-dependent
  bias) are different in kind from a volumetric skeleton. Citing this as "ML on centerlines for
  tortuosity works" without stating the 2D/3D distinction would overreach.
- Does **not** establish tortuosity as an independent predictor of CAD free of measurement
  circularity — the CAD label and the tortuosity measure share a source image and a rater, and the
  paper does not rule out or even discuss this.
- Does **not** generalize past the RCA (authors' own limitation) — no left main, LAD, or LCx result,
  and the left system is explicitly deferred because of geometry the authors expect to be harder,
  which likely also holds for objective 7/8's full-tree geometry work here.
- Does **not** give a reproducible architecture: no code/data release, and the transformer's own
  design (layers, heads, loss, exact split) is not in the accessible main text, only referenced to a
  supplemental table not opened in this pass.

## Open questions

- Supplemental Table 12 (AUROC methodology) and Table 10 (classical-index correlation) were cited
  but not opened — if this paper is leaned on more heavily later, those should be pulled to confirm
  the train/test partition and the r=0.116 number's exact computation.
- Whether the 78.7% segmentation success rate is tortuosity-dependent is not tested by the authors
  and is not answerable from this paper alone; worth keeping in mind if a similar CGPS pipeline
  reports a segmentation/reconnection success rate below 100% on the tortuosity tail specifically
  (relates to [[project_qiu_reconnection]] — same shape of concern, fragments/failures not being a
  random sample of the true distribution).
- No attempt in this paper to learn an embedding of the tortuosity sequence itself (e.g. an
  autoencoder or contrastive objective over the curvature vector) — the transformer still consumes a
  hand-crafted per-point angle, it just doesn't collapse it to one number first. The gap identified in
  the 2026-09-18 web search session (no paper learns a tortuosity *representation* end-to-end from
  centerline geometry) stands after reading this paper in full.
