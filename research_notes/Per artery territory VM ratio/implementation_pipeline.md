# Implementation pipeline: per-artery coronary lumen volume (V) and LV myocardial mass (M) from CCTA with open tools

Scope: ~1,000-2,000 contrast CCTA scans (CGPS, baseline and ~10-year follow-up), in-house deep-learning lumen model trained on ImageCAS, goal of per-artery V (LAD+diagonals, CX+OMs, RCA+PDA/PLA) and territory M. Data must stay local. Research done 2026-10-12. "Cited Findings" = established/reported facts with sources; "Inferences" = suggestions for this thesis.

## 1. LV myocardium segmentation from CCTA and the mass convention

### Takeaway
TotalSegmentator's `heartchambers_highres` gives LV myocardium (plus LV/RV/LA/RA, aorta, pulmonary artery) out of the box and runs locally, but it is a licensed task (free non-commercial licence key needed), and I found no peer-reviewed validation of its myocardial mass against MRI or manual CCTA contours. Mass = myocardial volume x 1.05 g/mL is the near-universal convention in the V/M literature. CT LV mass agrees with MRI on average (near-zero bias), but limits of agreement are about +/-28 g, so expect noise.

### Cited Findings
**TotalSegmentator**
- `heartchambers_highres` classes: myocardium, atrium_left, ventricle_left, atrium_right, ventricle_right, aorta, pulmonary_artery. It is described as "trained on sub-millimeter resolution" — [TotalSegmentator GitHub README](https://github.com/wasserth/TotalSegmentator)
- Licence: listed under "Available with a license"; "free licenses available for non-commercial usage", set with `totalseg_set_license -l aca_...`; commercial use requires contacting the author. The `coronary_arteries` task (single class `coronary_arteries`, no LAD/CX/RCA split) is also licensed. The default `total` task (Apache-2.0) has only a single `heart` class — [TotalSegmentator GitHub README](https://github.com/wasserth/TotalSegmentator)
- In v2 the heart-chamber classes were moved out of `total` into `heartchambers_highres`. Heart-chamber label errors were corrected. The public TotalSegmentator dataset **removed** the heart-chamber classes, so you cannot retrain or inspect them from the public data — [TotalSegmentator v2 improvements](https://github.com/wasserth/TotalSegmentator/blob/master/resources/improvements_in_v2.md)
- Original paper: overall mean Dice 0.943 across all structures (not heart-specific) — [Wasserthal et al., TotalSegmentator, arXiv 2208.05868 / Radiology: AI 2023](https://arxiv.org/pdf/2208.05868)
- Independent check: a 2025 preprint using TotalSegmentator's heart-chamber model as a pseudo-label generator for **preclinical** (animal) 4D cardiac CT reported Dice > 0.90 against manual ground truth for most structures. The aorta and pulmonary artery were weaker — [arXiv 2505.09564](https://arxiv.org/html/2505.09564v1). This is animal data, so it does not transfer directly to human CCTA mass accuracy.
- TotalSegmentator chamber/myocardium outputs have been used in large outcome studies (e.g. chest CT mortality prediction), but those papers are not manual-vs-model validations — [Nature Communications 2024](https://www.nature.com/articles/s41467-024-46977-3); [JACC Advances 2024](https://www.jacc.org/doi/10.1016/j.jacadv.2024.101300)
- A DTU/Rigshospitalet group (Hansen, Kofoed, Paulsen et al.) generated whole-heart labels for ImageCAS with TotalSegmentator in a public dataset. It also flags common data flaws, including step artefacts and structures extending beyond the field of view — [Hansen et al., STACOM 2025, arXiv 2510.06090](https://arxiv.org/abs/2510.06090). The same work notes that TotalSegmentator's LAA outputs are "blocky" because of 1.5 mm resolution. That concerns the standard (non-highres) model — [arXiv 2510.06090 PDF](https://arxiv.org/pdf/2510.06090)

**Other open models / benchmarks**
- MM-WHS challenge (60 CT + 60 MRI, 12 groups): mean whole-heart Dice 0.872 +/- 0.087 for CT across methods, best team 0.908. Deep-learning methods averaged 0.875 and multi-atlas 0.859. Myocardium was among the harder substructures — [Zhuang et al., Med Image Anal 2019, arXiv 1902.07880](https://arxiv.org/pdf/1902.07880)
- A U-Net trained on CCTA (166 patients) reached median Dice 0.920 (IQR 0.811-0.944) for the LV myocardium against manual annotation — [Univ. Milan repository](https://air.unimi.it/handle/2434/955568)
- A deep-learning model on non-contrast chest CT against cardiac MRI gave ICC 0.91 for LV mass (0.85 LVEDV, 0.84 LVESV). It failed in 1/53 patients — [Diagnostics 2024, PMC11675647](https://pmc.ncbi.nlm.nih.gov/articles/PMC11675647)

**CT vs MRI mass accuracy**
- Meta-analysis (53 studies, 1,814 patients): CT minus MRI LV mass mean difference 0.13 g, limits of agreement -28.2 to +28.4 g. The authors call the limits "moderately wide" — [Kaniewska et al., Eur Radiol 2017 meta-analysis (springermedicine record)](https://www.springermedicine.com/noninvasive-evaluation-of-global-and-regional-left-ventricular-f/20864202)
- A 2013 CT-vs-CMR study (40 subjects) found CT systematically underestimated LV mass without noise reduction (-10.3 +/- 10.1 g). With strong noise reduction the bias was -0.5 +/- 8.3 g (r = 0.97). So image noise and reconstruction shift mass — reported in search results, record likely [Weill Cornell VIVO pubid 23522745](https://vivo.weill.cornell.edu/display/pubid23522745) (attribution not verified against full text)

**Convention: density, phase, papillary muscles**
- M = segmented LV myocardial volume x assumed density 1.05 g/cc. This is the standard in the V/M literature (HeartFlow-based and others) — [Ihdayhid et al., JCCT 2022;16:198-206 (review)](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view); also used by [Ding et al., Front Cardiovasc Med 2025;12:1449148](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2025.1449148/full)
- Ding et al. segmented from the 75% R-R phase (prospective gating) — [Front Cardiovasc Med 2025](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2025.1449148/full)
- On MRI, including vs excluding papillary muscles and trabeculations changes LV mass significantly. The effect is larger in hypertrophy (Fabry). Clinical practice is inconsistent — [JCMR, PMC4335368](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4335368/)
- CGPS reference values for CT LV mass exist: 569 healthy CGPS participants, 320-detector CCTA, semi-automated software. 97.5th-percentile LVM index was 80 g/m^2 (men) and 65 g/m^2 (women), and men had larger absolute and indexed mass — [Fuchs et al., Eur Heart J Cardiovasc Imaging 2016;17(9):1009-1017](https://research.regionh.dk/da/publications/normal-values-of-left-ventricular-mass-and-cardiac-chamber-volume/)

### Inferences
- Practical choice: TotalSegmentator `heartchambers_highres` (obtain the free academic licence, run offline with `--device gpu` or CPU). Data never leaves the machine, and the licence key is only checked locally. Confirm in the licence text that university thesis use counts as "non-commercial".
- Apply M = V_myo x 1.05 g/mL. Report whether papillary muscles and trabeculae are included. TotalSegmentator labels are blood-pool vs wall, so papillary muscles are probably split between the two. Inspect a sample to decide, and state it as a limitation.
- Mass is phase-dependent mainly through segmentation (wall thickening, papillary muscles merging with the wall in systole), not true mass change. Use the same phase as the reconstruction used for the lumen, usually mid-diastole 70-80% or best-diastolic. Record the phase from DICOM; CGPS headers do not contain it.
- Validate locally. Hand-correct LV myocardium in ~20-30 scans (stratified by BL/FU scanner), and compare TotalSegmentator mass with Fuchs 2016 CGPS reference ranges (same cohort and scanner family, so ideal plausibility anchors).
- Fallback if the licence is a problem: train nnU-Net on public whole-heart labels (MM-WHS CT, or TotalSegmentator-derived labels on ImageCAS from Hansen et al.).

### Gaps
- No peer-reviewed validation of TotalSegmentator `heartchambers_highres` LV myocardium Dice or mass vs MRI/manual on human CCTA was found. Its training-data composition (contrast vs non-contrast, phase mix) is not documented in the README.
- Per-structure CT myocardium Dice for MM-WHS was not retrieved (see Tables 4-5 of arXiv 1902.07880).
- No CT-specific study found quantifying the diastole-vs-systole mass difference or papillary-muscle inclusion effect for CCTA.

## 2. Coronary lumen volume: method dependence, cutoffs, acquisition factors, branch labelling

### Takeaway
Lumen volume depends strongly on the method and on how far distally the tree is tracked (published V/M values range ~18-43 mm^3/g largely for this reason). The literature convention is to include vessels down to about 1 mm diameter. Nitroglycerin has a large effect on V (up to ~70% between groups), and kernel/blooming affects lumen boundaries. Automated LAD/CX/RCA labelling of centerlines is mature for main branches (87-100% accuracy) but weaker for LCx side branches.

### Cited Findings
**Method and distal cutoff**
- V/M lumen volume is "dependent on the image analysis methods used to segment the coronary arteries and the extent of the tree that is resolved". First-generation HeartFlow V/M added a synthetic microvascular tree and gave higher values. The refined method uses only epicardial lumen in vessels > ~1 mm — [Ihdayhid et al., JCCT 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view), citing [Taylor et al., JCCT 2017;11:429-436](https://pubmed.ncbi.nlm.nih.gov/28789941)
- Ding et al. set a 1 mm threshold manually at the distal end of each vessel on straightened MPR, and included branches > 1 mm — [Front Cardiovasc Med 2025](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2025.1449148/full)
- In Syngo.via-based workflows, the operator adjusts an HU threshold (50-665 HU) before lumen volume is computed, which adds reader dependence — [Frontiers 2025 via search summary](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2025.1449148/full)
- Reported values differ between pipelines: Taylor 2017 (NXT) median V/M 18.57 mm^3/g; ADVANCE (n=3,110) mean V 3,003 mm^3 (range 493-7,891), M 122 g, V/M 25.2 mm^3/g (range 5.6-62.5); Ding 2025 controls 43.3 +/- 11.5 mm^3/g; a TAVR study cutoff of 33.31 mm^3/g — [Ihdayhid 2022 review](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view); [Ding 2025](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2025.1449148/full); [TAVR study, PMC12020294](https://pmc.ncbi.nlm.nih.gov/articles/PMC12020294)

**Nitroglycerin, heart rate, image quality**
- In 200 healthy Copenhagen volunteers (320-slice CT, CAC 0, normal high-quality CCTA), mean coronary volume was 4.33 mL with nitroglycerin vs 2.55 mL without. LV mass correlated strongly with coronary volume after adjusting for BSA and sex, and sex was not independently associated. The LAD share of volume rose from right- to left-dominant systems — [Sørensen, Kühl, Fuchs et al., JCCT 2017;11:295-301](https://test01.ku.dk/:obvius/pureproxy/3974268/en/publications/volume-and-dimensions-of-angiographically-normal-coronary-arterie)
- Repeat CCTA in 35 patients (0.4 mg vs 0.8 mg NTG, scans 3.9 +/- 1.6 y apart): coronary volume 2,639 +/- 753 vs 2,845 +/- 827 mm^3 (p = 0.009), while V/M did not change significantly (p = 0.20) — [Holmes et al., Eur Radiol 2019;29:6829-6836 (Cambridge repository)](https://www.repository.cam.ac.uk/handle/1810/298240)
- The review states that routine nitroglycerin and heart-rate control improve lumen-volume quantification, and that spatial resolution "prohibits the complete visualization of the coronary vasculature" — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- Ding et al. list as limitations spatial resolution, motion artefacts, poor opacification for small vessels, and an unclear effect of contrast "turbidity" on volume — [Ding 2025](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2025.1449148/full)

**Reconstruction kernel / blooming**
- The convolution kernel is described as the most important factor in blooming. In phantoms, calcified area varied systematically from sharp to soft kernels (normalised area 0.93 -> 1.07). Sharper kernels reduce blooming but increase noise — summarised from [SPIE virtual imaging trial](https://medicalimaging.spiedigitallibrary.org/conference-proceedings-of-spie/12304/1230415/A-virtual-imaging-trial-framework-to-study-cardiac-CT-blooming/10.1117/12.2646407.full) and [stent phantom study, PMC3904014](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3904014/)

**Branch labelling and datasets**
- ImageCAS: 1,000 CCTA from a Siemens 128-slice dual-source scanner, labelled by two radiologists plus consensus — [Zeng et al., arXiv 2211.01607](https://arxiv.org/pdf/2211.01607)
- ImageCAS-X (Bransby, ..., Kofoed, Paulsen; arXiv 31 Aug 2026, under review): 800 ImageCAS scans with voxel-wise lumen and **coronary segment** labels, centerlines and meshes. Methods are benchmarked against inter-observer variability, stratified by image quality, dominance, segment, vessel diameter and attenuation. Licence CC BY 4.0 — [arXiv 2608.30404](https://arxiv.org/abs/2608.30404)
- Improved ImageCAS coronary labels plus TotalSegmentator whole-heart labels — [Hansen et al., arXiv 2510.06090](https://arxiv.org/abs/2510.06090)
- Automated labelling: a 3D U-Net (myocardium) combined with distance-transform centerline labelling (157 patients) needed expert modification or removal of 5.4% of 2,180 segments, with 96.2% label-presence accuracy — [BMC Med Inform Decis Mak 2023, PMC10626726](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10626726/). Accuracy across methods is typically 87-100% for RCA, LAD and LM, and lower for LCx and side branches — same source. Graph/point methods include CPR-GCN ([arXiv 2003.08560](https://arxiv.org/pdf/2003.08560)), topology-constrained labelling ([arXiv 2307.11959](https://arxiv.org/pdf/2307.11959)) and hierarchical PointNet++ ([A*STAR](https://oar.a-star.edu.sg/communities-collections/articles/21017)).

### Inferences
- Pipeline suggestion:
  1. Lumen mask from the in-house model.
  2. Centerlines (VMTK `vmtkcenterlines`, or skeletonisation with `skimage.morphology.skeletonize` plus a graph via `skan`) with a per-point radius from the maximal inscribed sphere or distance transform.
  3. Label branches. Train a labeller on ImageCAS-X segment labels, or use rules: identify LM/RCA ostia from aortic connectivity, then LAD vs CX by direction relative to the LV long axis/interventricular groove. Assign side branches to their parent trunk (LAD+D+ramus by convention, CX+OM, RCA+PDA/PLA, with PDA/PLA following dominance).
  4. Prune all points with radius < 0.5 mm (diameter < 1 mm) and compute V per tree as the voxel volume, or better, as the mesh volume of the pruned lumen.
- Report V at two cutoffs (1.0 and 1.5-2.0 mm diameter) as a sensitivity analysis. A 2 mm cutoff is far less sensitive to scanner resolution, noise and NTG, which matters across a 10-year scanner gap.
- Ramus intermedius: decide a rule (e.g. assign to LAD or to a separate category) and state it.
- CGPS headers record nitroglycerin (`scandata_nitro`), kV, mA and contrast volume **only at FU**. Heart rate (`preparation_heartrate`, `hr_during_scan`) and BSA are in both. Scanner model, kernel, slice thickness and phase are not in the headers and must come from DICOM tags. Use these as adjustment or QC covariates; BL nitro must be assumed from protocol.
- Because the outcome design uses plaque-free trunks, V is less contaminated by stenosis, but diffuse remodelling and calcium blooming still bias lumen boundaries.

### Gaps
- No phantom study found that directly measures coronary **lumen volume** bias vs reference across kernels and voxel sizes. Evidence is indirect (stent and calcium blooming).
- No study found of lumen volume change attributable to scanner generation over a ~10-year gap.
- No quantitative comparison found of V at 1 mm vs 2 mm cutoffs.

## 3. Reproducibility of lumen volume and V/M

### Takeaway
Published reproducibility evidence for V/M is thin: one single-centre study reported intra-/inter-observer ICC 0.78/0.76, and repeat-scan data come only from the NTG study (V changed, V/M did not). The thesis should estimate its own scan-level reproducibility.

### Cited Findings
- V/M intra-observer ICC 0.78 and inter-observer ICC 0.76 (20% of patients re-measured after one month by two radiologists; semi-manual AW workstation) — [Ding et al., Front Cardiovasc Med 2025](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2025.1449148/full)
- Repeat scans years apart with different NTG doses: V +7.8% (p = 0.009), V/M unchanged (p = 0.20) — [Holmes et al., Eur Radiol 2019](https://www.repository.cam.ac.uk/handle/1810/298240)
- Related CT measures: automated plaque volume interscan r = 0.90-0.96 — [Schuhbaeck et al. (cris.fau.de)](https://cris.fau.de/publications/111546424). An interscan CT plaque-volume reproducibility study from Odense — [Iraqi et al., JCCT 2024, doi:10.1016/j.jcct.2024.09.009](https://findresearcher.sdu.dk/ws/files/276924136/Open_Access_Version.pdf)
- ImageCAS-X benchmarks lumen segmentation against inter-observer variability, giving a reference for annotation-level agreement — [arXiv 2608.30404](https://arxiv.org/abs/2608.30404)

### Inferences
- Internal reproducibility options:
  - (a) Run the pipeline on multiple phases or reconstructions of the same exam if the DICOM series include them (closest to interscan).
  - (b) Compute test-retest agreement on ImageCAS-X scans where two annotators exist.
  - (c) Perturbation tests: resampling, ±1 voxel erosion/dilation, cutoff shifts.
- Report ICC, within-subject CV and Bland-Altman for per-artery V, territory M and V/M.

### Gaps
- No interscan (same-day repeat) reproducibility study of lumen volume or V/M was found. No per-artery or territory V/M reproducibility data were found.

## 4. Quality-control checks

### Takeaway
Use automated plausibility checks (FOV truncation, mass vs sex/BSA against CGPS norms, V vs M, territory fractions vs dominance), with visual review of flagged cases. The CGPS headers provide reader-graded image quality and unevaluable-segment information to exclude or stratify on.

### Cited Findings
- CGPS normal LV mass index (97.5th percentile 80/65 g/m^2 men/women), with sex- and age-specific values — [Fuchs et al., EHJ-CVI 2016](https://research.regionh.dk/da/publications/normal-values-of-left-ventricular-mass-and-cardiac-chamber-volume/)
- Expected magnitudes: ADVANCE M 55-357 g (mean 122), V 493-7,891 mm^3; women V 2,548 vs men 3,226 mm^3 and M 99.5 vs 133.2 g; V/M higher in women (26.2 vs 24.8) — [Ihdayhid 2022 citing Fairbairn et al., JACC CVI 2020;13:2576-2587](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- Coronary volume share by dominance: the LAD share rises from right- to left-dominant systems, and the RCA and CX shares move in opposite directions — [Sørensen et al., JCCT 2017](https://test01.ku.dk/:obvius/pureproxy/3974268/en/publications/volume-and-dimensions-of-angiographically-normal-coronary-arterie)
- ImageCAS-derived public data contain step artefacts and structures beyond the FOV — [Hansen et al. 2025](https://arxiv.org/abs/2510.06090)
- Territory M: Voronoi (nearest-centerline) assignment of myocardium to coronary territories correlated with SPECT area-at-risk (r = 0.814) — [Kurata et al., Eur Radiol 2015](https://link.springer.com/doi/10.1007/s00330-014-3388-2). CT-derived fractional mass agreed with invasively measured relative perfusion territories — [Keulards et al., Heart 2020;106:1489-1494](https://heart.bmj.com/content/106/19/1489). Histological and cadaver validation — [Ide et al., JCCT 2017;11:179-182](https://link.springer.com/article/10.1007/s12928-015-0370-0). Vessel-specific myocardial mass reference values (n = 948) exist in JAHA 2024/25 (per search result; not opened).

### Inferences
Suggested automated QC flags:
- **FOV truncation**: LV myocardium or blood-pool mask touching the first or last axial slice or the in-plane FOV edge (apex often truncated at caudal end, base/LA at cranial end) → flag/exclude M. CGPS FU has `ct_cag_uneval_scanfield` (+ per vessel).
- **Mass plausibility**: LVMi outside sex-specific CGPS 1st-99th range, or |z| > 3 vs a regression on sex, age and BSA (`male`, `scan_age`, `clin_bsa`). Check the LV blood-pool volume range as well.
- **Lumen plausibility**: V per artery outside the cohort 1-99th percentile. V vs M residual outliers. Disconnected components. LM/RCA ostium not connected to the aorta. Trunk length too short (missed distal vessel).
- **Territory vs dominance**: RCA territory fraction should be larger in right-dominant (`ct_cag_dominance`) and LCX larger in left-dominant. Treat disagreements as labelling errors.
- **Image quality**: exclude or stratify by `bad_quality`, `scan_qualitative_quality`, `ct_cag_*_uneval` and motion/noise reasons (FU). Exclude `ct_cag_stent`/`ct_cag_cabg`.
- **BL-FU consistency**: within-person V change implausibly large (e.g. > 40%) in plaque-free trunks → check NTG, phase and kernel.
- Visual review of a random 5% plus all flagged cases, with a dashboard of overlays.

### Gaps
- No published consensus QC checklist for automated V/M was found.
- The JAHA vessel-specific mass reference paper and the Ide cadaver numbers were not opened.

## 5. Statistical handling: indexing, transforms, measurement error

### Takeaway
V scales roughly linearly with M (exponent ~1 in swine), so a simple ratio V/M is defensible. A safer modelling choice is log V with log M (and sex/BSA) as separate covariates, which lets the data choose the exponent. Measurement error and heterogeneity between BL and FU scanners can bias coefficients and harm calibration in small prediction models.

### Cited Findings
- Coronary flow in FFRCT is derived from allometric scaling, flow ∝ M^(3/4). Women's higher resting flow per gram is consistent with this scaling — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- Swine CT study: exponents 3/4 for length–mass and length–volume, and 1.0 for **volume–mass** — [Int J Cardiovasc Imaging 2008, doi:10.1007/s10554-008-9303-7](https://link.springer.com/article/10.1007/s10554-008-9303-7) (likely Choy & Kassab group; authorship not confirmed from the abstract page). Human data (638 arteries, 43 patients) confirm power-law V–M relations — [SKKU 2020](https://scholarworks.bwise.kr/skku/handle/2021.sw.skku/25537); foundational paper [Choy & Kassab, J Appl Physiol 2008;104:1281-1286](https://pubs.rsna.org/doi/10.1148/radiol.13122181) (cited in this Radiology paper)
- Sex was not independently associated with coronary volume once BSA and LV mass were accounted for — [Sørensen et al., JCCT 2017](https://test01.ku.dk/:obvius/pureproxy/3974268/en/publications/volume-and-dimensions-of-angiographically-normal-coronary-arterie)
- When predictors are measured differently across settings (e.g. scanner or protocol), calibration and discrimination degrade, sometimes to clinical uselessness — [Luijken et al., Stat Med 2019;38:3444-3459, doi:10.1002/sim.8183](https://researchinformation.umcutrecht.nl/en/publications/impact-of-predictor-measurement-heterogeneity-across-settings-on-/). Real examples showed calibration slopes of 0.50-1.67 — [Luijken et al., J Clin Epidemiol 2020](https://researchexchange.ocrahope.org/papers/j-jclinepi-2019-11-001)

### Inferences
- Primary predictor: log(V_artery) adjusted for log(M_territory) (or log M_total), sex and BSA; a ratio constrains the exponent to 1. Report V/M as a secondary, interpretable index. V/M^(3/4) is an option motivated by flow scaling, but the swine data suggest V ∝ M^1, so test the fitted exponent rather than assume it.
- Log-transform V, M and V/M (right-skewed, multiplicative errors). Check with residual plots.
- Measurement error in V (ICC ~0.76-0.78 reported for manual V/M) attenuates coefficients by roughly the reliability ratio and wastes the effective sample size, which matters given Riley sample-size limits. Consider regression calibration using the internal reproducibility estimate, or at least a sensitivity analysis.
- The BL→FU scanner change does not affect a baseline-only predictor model directly, but it does matter if FU-derived V/M or change scores are used. Then adjust for scan year/scanner, or restrict to change-insensitive cutoffs (≥ 2 mm).
- Per the project's per-artery-only rule: fit separate LAD, CX and RCA models, each with its own territory M.

### Gaps
- No study found comparing V/M vs V/M^(2/3) vs V/M^(3/4) indexing for prediction performance.
- No published estimate of measurement-error impact specifically for V/M in prediction models.
