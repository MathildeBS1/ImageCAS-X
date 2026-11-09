# FPCA of profiles measured along an anatomical path, related to a clinical outcome

Scope: peer-reviewed studies that applied FPCA, or regression built on FPCA, to a quantity measured along a
vessel centerline, airway, spine or white-matter tract, and related it to disease. About 14 searches and
fetches (Europe PMC REST, NCBI efetch full text, Crossref, web search). All DOIs below were checked on
Crossref (api.crossref.org/works/DOI) on 2026-11-07.

## Q1. Which peer-reviewed papers applied FPCA to a profile along a path and related it to an outcome?

### Takeaway
The best match for the thesis is Goldsmith et al. 2011 (NeuroImage). It takes FA and other DTI indices along
white-matter tracts, puts position on [0,1], and runs an FPCA-based penalized functional regression inside a
logistic model with covariates. It compares this directly with a model that uses the tract **mean**, on
held-out data. The best vascular match is Passerini et al. 2012, an AneuRisk follow-up (FPCA of ICA radius,
curvature and WSS, 52 patients). It has no comparison with a scalar summary.

### Cited Findings

**1. Goldsmith J, Crainiceanu CM, Caffo BS, Reich DS. Penalized functional regression analysis of white-matter
tract profiles in multiple sclerosis. NeuroImage 2011;57(2):431–439. DOI 10.1016/j.neuroimage.2011.04.044
(Crossref verified). Peer-reviewed; open full text PMC3114268 (author manuscript). Full text read.**
- Design: cross-sectional, case-control (115 MS cases, 42 healthy volunteers; not a population sample). Tracts:
  corpus callosum, corticospinal tract, optic radiation. Indices: FA, MD, AD, RD, MTR. Outcomes: case status
  and disability scores. Data split into training and test sets — [PMC3114268](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268)
- Path parametrisation matches the thesis: "X i ( p ) denotes the tract profile for participant i after
  subtracting the population mean μ ( p ), where p is the tract position (defined on the interval [0,1])" — [PMC3114268](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268)
- Nested models that mirror the thesis question (base, base + mean, base + profile): "Model 1 includes age,
  sex, and whole-brain MRI index; Model 2 adds the tract-specific index average; and Model 3 is the full PFR
  model". The models are logistic, e.g. "log it [ P ( Y i ) = 1 ] = γ 0 + γ 1 age i + γ 2 sex i + γ 3 brain i +
  ∫ 0 1 X i ( p ) β ( p ) d p" — [PMC3114268](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268)
- Main result (abstract): "We show that attention to spatial variation yields up to 15% (mean across all tracts
  and MRI indices: 6.4%) improvement in the ability to discriminate multiple sclerosis cases from healthy
  volunteers." — [PMC3114268](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268)
- What the profile captured that the mean missed (optic radiation, FA): "The weighting function that best
  separates the two groups using PFR ... emphasizes the contrast between the middle portion of the tract and
  its termini ... Model 2, by construction, averages these regions of the tract together." — [PMC3114268](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268)
- Discussion: "accounting for spatial variation within a tract, rather than simply considering average
  measurements, can substantially improve the statistical associations between quantitative MRI indices and
  case status" — [PMC3114268](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268)
- Caveat stated by the authors: "for the CC, the performance of Model 2 is substantially improved on the test
  set, where it in fact outperforms Model 3. This instability is a result of the small test set for the CC,
  containing 9 healthy volunteers and 24 MS cases" — [PMC3114268](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268)
- The FPCA link comes from the method paper: Goldsmith J, Bobb J, Crainiceanu CM, Caffo B, Reich D.
  Penalized functional regression. J Comput Graph Stat 2011;20(4):830–851. DOI 10.1198/jcgs.2010.10007
  (Crossref verified; PMC3285536; abstract read): "The functional predictor is projected onto a large number of
  smooth eigenvectors and the coefficient function is estimated using penalized spline regression" — [Europe PMC record](https://europepmc.org/article/PMC/PMC3285536)

**2. Passerini T, Sangalli LM, Vantini S, Piccinelli M, Bacigaluppi S, Antiga L, Boccardi E, Secchi P,
Veneziani A. An integrated statistical investigation of internal carotid arteries of patients affected by
cerebral aneurysms. Cardiovasc Eng Technol 2012;3(1):26–40. DOI 10.1007/s13239-011-0079-x (Crossref verified;
online 2011-12-28). Peer-reviewed. I read the open MOX Report 19/2011 preprint version, not the journal PDF.**
- Data: AneuRisk, 65 patients scanned 2002–2006 by 3D rotational angiography at Niguarda Hospital, Milan,
  reduced to 52. Referral population (aneurysm work-up), cross-sectional — [MOX Report 19/2011](https://www.mate.polimi.it/biblioteca/add/qmox/19-2011.pdf)
- Method: "these quantities are regarded as stochastic functions of an axial coordinate defined along the
  vessel. To extract patterns from such a complex aggregate of information we resorted to ... Functional
  Principal Component Analysis (FPCA)." FPC scores were then used in multivariate analysis and discriminant
  analysis — [MOX Report 19/2011](https://www.mate.polimi.it/biblioteca/add/qmox/19-2011.pdf)
- Outcome groups: aneurysm location (Upper = at or after the ICA terminal bifurcation; Lower = along the ICA,
  or no aneurysm), split further by rupture status into UR/UN/LR/LN/No — [MOX Report 19/2011](https://www.mate.polimi.it/biblioteca/add/qmox/19-2011.pdf)
- Results: "Significant differences occur among the five groups of subjects, in particular emphasized by the
  first principal component of the Radius and the Curvature and the second principal component of the axial
  derivative of WSS". The paper also notes that "the component along this mode measures the average radius of
  the ICA". **In other words, the first radius FPC is essentially the mean.** The paper does not compare the
  scores with a scalar summary — [MOX Report 19/2011](https://www.mate.polimi.it/biblioteca/add/qmox/19-2011.pdf)
- Shape clusters versus location: no-aneurysm patients were 0% Ω-shaped and 100% S-shaped, against 70%/30% for
  aneurysms at or after the bifurcation. The sample is small (n = 52) — [MOX Report 19/2011](https://www.mate.polimi.it/biblioteca/add/qmox/19-2011.pdf); [BOA Unimib record](https://boa.unimib.it/handle/10281/27403)

**3. Supporting references (methods or data; abstracts read only)**
- Goldsmith J, Crainiceanu CM, Caffo B, Reich D. Longitudinal penalized functional regression for cognitive
  outcomes on neuronal tract measurements. J R Stat Soc C 2012;61(3):453–469. DOI 10.1111/j.1467-9876.2011.01031.x
  (Crossref verified; PMC3366511). A GLMM with functional predictors: tract profiles measured at repeated
  visits in MS patients, related to a cognitive score. This is structurally close to the thesis's GLMM with
  profile terms — [Europe PMC](https://europepmc.org/article/PMC/PMC3366511)
- Greven S, Crainiceanu C, Caffo B, Reich D. Longitudinal functional principal component analysis. Electron J
  Stat 2010;4:1022–1054. DOI 10.1214/10-EJS575 (Crossref verified; PMC3131008). Longitudinal FPCA of DTI tract
  profiles in MS patients and controls. Descriptive; no outcome model — [Europe PMC](https://europepmc.org/article/PMC/PMC3131008)
- Pomann G-M, Staicu A-M, Ghosh S. A two-sample distribution-free test for functional data with application
  to a DTI study of MS. J R Stat Soc C 2016;65(3):395–414. DOI 10.1111/rssc.12130 (Crossref verified;
  PMC4812165). A group test on tract profiles; not read beyond the title and record — [Crossref](https://api.crossref.org/works/10.1111/rssc.12130)
- Sangalli LM, Secchi P, Vantini S. AneuRisk65: a dataset of three-dimensional cerebral vascular geometries.
  Electron J Stat 2014;8:1879–1890. DOI 10.1214/14-EJS938 (Crossref verified). The data source behind Sangalli
  2009 and Passerini 2012 — [Crossref](https://api.crossref.org/works/10.1214/14-EJS938)
- Sangalli et al. 2009 JASA 104:37–48, DOI 10.1198/jasa.2009.0002 (Crossref verified; already cited in the
  thesis) — [Crossref](https://api.crossref.org/works/10.1198/jasa.2009.0002)
- The refund R package ships the Goldsmith DTI data (FA profiles of the corpus callosum, with PASAT as the
  outcome) — [refund DTI docs](https://rdrr.io/cran/refund/man/DTI.html)

**4. Checked and not recommended**
- "Prescreening and treatment of aortic dissection through an analysis of infinite-dimension data", BioData
  Min 2021, DOI 10.1186/s13040-021-00249-8 (348 dissection cases, 171 controls). The paper calls itself FDA,
  but the morphology part reduces slope curves of 2D centerlines to four scalar statistics. It is not FPCA, and
  the "predissected" centerline is restored from images taken after the dissection — [PMC8015064](https://pmc.ncbi.nlm.nih.gov/articles/PMC8015064)
- **Preprint (arXiv 2411.18398, "Derivative Estimation of Multivariate Functional Data")**: FPCA of coronary
  diameter and QFR curves and of their derivatives. Not peer-reviewed as far as I found (no journal reference in
  the arXiv record); diameter rather than curvature; no plaque outcome — [arXiv](https://arxiv.org/pdf/2411.18398)
- **Preprint (arXiv 2108.13147, merge trees)**: reuses the Sangalli 2009 pipeline (FPCA of AneuRisk curvature
  and radius → QDA). Methods only — [arXiv](https://arxiv.org/pdf/2108.13147)
- Spine: the closest finds were multivariate PCA of articulated or Procrustes spine shape models (Boisvert et
  al., ELCVIA 2008), not FPCA of a curvature profile — [ELCVIA](https://elcvia.cvc.uab.cat/article/view/v7-n4-boisvert-cheriet-pennec-et-al)

### Inferences
- For the thesis claim "FPCA is used on a continuous profile that is hard to summarise in one number, and the
  profile can carry information the mean misses", Goldsmith 2011 NeuroImage is the strongest single citation.
  It is peer-reviewed, its full text is open, it parametrises position on [0,1], it fits logistic models with
  base covariates and compares profile against mean on a held-out test set. Pair it with Sangalli 2009 or
  Passerini 2012 as the vascular-geometry example.
- Cite Goldsmith with care. It is case-control MS against controls (a strong disease contrast), the gain is
  "up to 15%" with a mean of 6.4%, and in one tract the mean-only model did better on the test set. The method
  is FPCA-based penalized regression with a smooth β(p), not FPC scores entered as covariates.
- Passerini 2012 shows FPC scores of ICA curvature and radius differ by aneurysm location. Its first radius FPC
  is essentially the mean radius, which supports the thesis point that FPC1 often reproduces the scalar summary
  and later FPCs carry the shape.

### Gaps
- I did not extract the AUC values from Goldsmith 2011 Table 2. The tables did not come through in the
  full-text extraction.
- I did not read the journal version of Passerini 2012, only the MOX preprint. Exact p-values for the FPC
  scores are not recorded here.

## Q2. Any prospective or longitudinal designs (geometry measured before disease)?

### Takeaway
I found none. Every vascular FPCA study found is cross-sectional, in referral patients with disease already
present. Goldsmith 2012 JRSS-C and Greven 2010 are longitudinal, but in patients who already have MS, so the
profiles are not measured before disease.

### Cited Findings
- Passerini 2012 and Sangalli 2009: cross-sectional, AneuRisk referral angiography with the aneurysm already
  present — [MOX Report 19/2011](https://www.mate.polimi.it/biblioteca/add/qmox/19-2011.pdf)
- Goldsmith 2012 JRSS-C: "the scalar outcome and the functional exposure are measured longitudinally", in MS
  patients — [Europe PMC](https://europepmc.org/article/PMC/PMC3366511)
- The aortic dissection FDA study imaged patients after the dissection — [PMC8015064](https://pmc.ncbi.nlm.nih.gov/articles/PMC8015064)

### Inferences
- A prospective, population-based FPCA of vessel geometry against incident disease appears to be new. The
  thesis can say so, hedged ("we found no").

### Gaps
- No systematic search was done (no Scopus or Web of Science; statistics journals are poorly indexed in Europe
  PMC). A prospective FPCA study in retinal-imaging cohorts (e.g. UK Biobank) may exist without being found.

## Q3. Is there any coronary FPCA of curvature linked to plaque?

### Takeaway
I found none. The searches turned up curvature–plaque studies with scalar or local curvature, and one coronary
FPCA preprint on diameter and QFR. Nothing applies FPCA to coronary curvature with a plaque outcome.

### Cited Findings
- The coronary FPCA preprint covers diameter and QFR derivatives only, with no plaque outcome — [arXiv 2411.18398](https://arxiv.org/pdf/2411.18398)
- An older study of circumferential plaque against local curvature used Fourier or polynomial curvature
  estimates, not FPCA — [ResearchGate record](https://www.researchgate.net/publication/221624156_Quantitative_Analysis_of_Circumferential_Plaque_Distribution_in_Human_Coronary_Arteries_in_Relation_to_Local_Vessel_Curvature)

### Inferences
- The thesis may state that, to our knowledge, FPCA of coronary curvature profiles has not been related to
  plaque. It should be worded as "we found no", not "none exists".

### Gaps
- Retinal, airway and spinal-curvature FPCA linked to outcomes: nothing found in this search. This is a search
  limitation, not evidence of absence.

## Q4. Ranking for the thesis use

### Takeaway
1. Goldsmith et al. 2011 NeuroImage, DOI 10.1016/j.neuroimage.2011.04.044. Best fit and strongest: compares
   profile against mean head to head, uses [0,1] position, base covariates and a test set; n = 157,
   case-control, cross-sectional. Cite it together with the JCGS method paper, DOI 10.1198/jcgs.2010.10007.
2. Passerini et al. 2012 CVET, DOI 10.1007/s13239-011-0079-x. Vascular curvature and radius FPCA, scores
   against aneurysm location and rupture; n = 52 referral patients; no comparison with a scalar.
3. Sangalli et al. 2009 JASA (already cited) and the AneuRisk65 dataset paper, DOI 10.1214/14-EJS938.
4. Goldsmith 2012 JRSS-C, DOI 10.1111/j.1467-9876.2011.01031.x: a GLMM with functional predictors, a
   method-level parallel to the thesis GLMM.
5. Greven 2010 EJS, DOI 10.1214/10-EJS575: methods and descriptive only.

### Cited Findings
- See Q1 for the sources of each ranked item — [PMC3114268](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268); [MOX Report 19/2011](https://www.mate.polimi.it/biblioteca/add/qmox/19-2011.pdf)

### Inferences
- Recommended pair: Goldsmith 2011 (profile beats mean, with outcome and validation) plus Passerini 2012 or
  Sangalli 2009 (vessel curvature and radius FPCA).

### Gaps
- None beyond those listed above.
