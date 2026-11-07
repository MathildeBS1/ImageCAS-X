# Comparing automatic cross-sectional lumen contours with Medis (QAngio CT) reference contours

Scope note: about 15 tool calls. Several primary full texts (Kirişli 2013 Medical Image Analysis, Boogers 2012 Eur Heart J, Park 2015 Eur Radiol) were not readable in full: the Kirişli PDF host returned 503 and the journals are paywalled. Where details of those papers come only from abstracts or from a secondary paper (Lugauer et al. 2014, which describes the Rotterdam lumen evaluation), this is stated. Anything marked "Inference" is my reasoning, not a sourced finding.

Key bibliographic details (for BibTeX):
- Kirişli HA, Schaap M, Metz CT, Dharampal AS, Meijboom WB, et al. Standardized evaluation framework for evaluating coronary artery stenosis detection, stenosis quantification and lumen segmentation algorithms in computed tomography angiography. *Medical Image Analysis* 2013;17(8):859–876. doi:10.1016/j.media.2013.05.007 — [ITU record](https://research.itu.edu.tr/en/publications/standardized-evaluation-framework-for-evaluating-coronary-artery-/)
- Lugauer F, Zheng Y, Hornegger J, Kelm BM. Precise lumen segmentation in coronary computed tomography angiography. MICCAI 2014 workshop on Medical Computer Vision (MCV), LNCS, Springer. doi:10.1007/978-3-319-13972-2_13 (workshop paper, peer-reviewed but not a journal) — [PDF](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf)
- Boogers MJ, Broersen A, van Velzen JE, de Graaf FR, El-Naggar HM, Kitslaar PH, Dijkstra J, Delgado V, Boersma E, de Roos A, Schuijf JD, Schalij MJ, Reiber JHC, Bax JJ, Jukema JW. Automated quantification of coronary plaque with computed tomography: comparison with intravascular ultrasound using a dedicated registration algorithm for fusion-based quantification. *European Heart Journal* 2012;33(8):1007–1016. doi:10.1093/eurheartj/ehr465. PMID 22285583 — [PubMed](https://pubmed.ncbi.nlm.nih.gov/22285583/). Note: this is *Eur Heart J*, not JACC Cardiovasc Imaging as the brief suggested.
- de Graaf MA, Broersen A, Kitslaar PH, Roos CJ, Dijkstra J, Lelieveldt BPF, Jukema JW, Schalij MJ, Delgado V, Bax JJ, Reiber JHC, Scholte AJ. Automatic quantification and characterization of coronary atherosclerosis with computed tomography coronary angiography: cross-correlation with intravascular ultrasound virtual histology. *International Journal of Cardiovascular Imaging* 2013;29(5):1177–1190 (published online 30 June 2013). Note: *Int J Cardiovasc Imaging*, not *Eur Heart J Cardiovasc Imaging* — [Leiden thesis record](https://scholarlypublications.universiteitleiden.nl/access/item%3A2919534/view). Author list and issue number are from memory; check the DOI before BibTeX (I did not retrieve it).
- Park HB, Lee BK, Shin S, et al. Clinical feasibility of 3D automated coronary atherosclerotic plaque quantification algorithm on coronary computed tomography angiography: comparison with intravascular ultrasound. *European Radiology* 2015;25(10):3073–3083 (QAngio CT; 150 segments, 142 patients; expert vs non-expert vs fully automatic) — [Yonsei record](https://ir.ymlib.yonsei.ac.kr/handle/22282913/141694). DOI not retrieved.
- Radunović A, Vidaković R, Timčić S, et al. Multislice computerized tomography coronary angiography can be a comparable tool to intravascular ultrasound in evaluating "true" coronary artery bifurcations. *Frontiers in Cardiovascular Medicine* 2023;10:1292517. doi:10.3389/fcvm.2023.1292517 — [Frontiers](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2023.1292517/full)
- Maier-Hein L, Reinke A, Godau P, et al. Metrics reloaded: recommendations for image analysis validation. *Nature Methods* 2024;21(2):195–212. doi:10.1038/s41592-023-02151-z. PMID 38347141 — [Warwick record](https://wrap.warwick.ac.uk/183654)
- Taha AA, Hanbury A. Metrics for evaluating 3D medical image segmentation: analysis, selection, and tool. *BMC Medical Imaging* 2015;15:29. doi:10.1186/s12880-015-0068-x — [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4533825/)
- Bland JM, Altman DG. Statistical methods for assessing agreement between two methods of clinical measurement. *Lancet* 1986;327(8476):307–310. doi:10.1016/S0140-6736(86)90837-8. Cited as the origin of Bland–Altman in [this search summary](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12064138/). Volume, pages and DOI are standard but from memory, not retrieved here.

---

## 1. How are cross-sections paired between two methods whose centerlines differ?

### Takeaway
Three approaches appear in the literature. In the Rotterdam lumen challenge (Kirişli 2013), all observers drew contours on cross-sections of a shared set of reference centerlines. CT–IVUS validation (Boogers 2012 and later core labs) uses landmark-based registration: ostium, side branches and calcium spots act as control points, with linear arc-length interpolation between them. The pragmatic version for Medis vs tracer is to resample one method's lumen on the other's planes, or to match by normalised arc length between shared landmarks such as the ostium and the bifurcation carinas. Either way, whether a point is really "the same location" is an error source, and it must be reported.

### Cited Findings
- In the Rotterdam framework, "the expert contours ... were annotated from the same set of centerlines" and still "vary considerably". Three medical experts annotated, and the framework computes each measure against each expert separately and averages them — [Lugauer et al. 2014](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf)
- Lugauer et al. used their own automatic centerlines. "A labeling mismatch between our applied CTL [centerline] tracing and the reference causes a large error bias" in 7 datasets. It "deteriorates the MSD and MAXSD error measures in particular for the healthy vessels". Only the main vessels (LM, LAD, RCA, LCX) were compared — [Lugauer et al. 2014](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf)
- The Rotterdam framework has 48 multicentre, multivendor CTA datasets and evaluated 11 research groups. Its conclusion: "Automatic lumen segmentation is possible with a precision similar to that obtained by experts" — [Kirişli 2013 abstract, ITU record](https://research.itu.edu.tr/en/publications/standardized-evaluation-framework-for-evaluating-coronary-artery-/)
- Boogers 2012 (Leiden QCT software, which preceded or became QAngio CT) fused "a complete IVUS run with a CT angiography volume using true anatomical markers". The study had 51 patients, 103 arteries and 146 lesions — [PubMed](https://pubmed.ncbi.nlm.nih.gov/22285583/). Per a secondary summary of the full text, the markers were side branches, calcified spots and overlapping veins — [ResearchGate entry via search](https://www.researchgate.net/publication/221785162_Automated_quantification_of_coronary_plaque_with_computed_tomography_comparison_with_intravascular_ultrasound_using_a_dedicated_registration_algorithm_for_fusion-based_quantification) (not verified in full text).
- A core-lab CT–IVUS study coregistered "using the proximal and distal end and each side branch". It refined alignment of the lumen and area profiles with software (ImFusion), and "the position of intermediate IVUS frames is linearly sampled on the corresponding CCTA lumen centerline" — [RSNA Radiology: Cardiothoracic Imaging, ryct.230312 (via search snippet)](https://pubs.rsna.org/doi/10.1148/ryct.230312). Not fetched in full; check authors and year before citing.
- In the INVICTUS AI-QCT vs IVUS work, the minimal lumen area (MLA) sites were "independently determined and not actively co-registered". Landmarks (ostium, side branches, calcifications) were mapped by the core lab — [Eur Radiol 2026, s00330-026-12412-y (via search snippet)](https://link.springer.com/article/10.1007/s00330-026-12412-y). Not fetched; the date suggests it is very recent.
- In a bifurcation study, the carina was the anchor: points 5 mm proximal and distal were placed on IVUS and transferred to CTCA using the IVUS-measured distances. The authors call this semiautomated co-registration and say it "can lead to a certain bias" — [Radunović et al. 2023](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2023.1292517/full)

### Inferences
- For Medis vs tracer, both lumens come from the *same CT volume and the same world frame* (LPS mm), so no cross-modality registration is needed. The only problem is that the centerlines differ. Option A follows the Rotterdam principle of a shared centerline: take each Medis contour plane (its centroid plus the plane normal from the Medis centerline tangent), intersect the tracer's lumen with that plane, and compare in the plane. Option B: match each Medis contour to the tracer step nearest in 3D, or nearest by arc length from a shared landmark (the ostium, or the LM bifurcation carina), and reject pairs whose centroids are farther apart than a threshold, e.g. about 1 mm or one lumen radius. I found no source for a specific threshold.
- The tracer predicts a contour per step in its own plane. Comparing two contours from *differently oriented* planes biases area: an oblique cut inflates area by roughly 1/cos(theta). Report the angle between the two plane normals per pair, and either exclude pairs above a cut-off (e.g. 15–20°) or reslice one method onto the other's plane. This is geometry, not a cited finding.
- Arc-length matching from the ostium accumulates the length difference between the two centerlines along the vessel. Piecewise normalisation between landmarks (the ostium, then each bifurcation) follows CT–IVUS practice and limits that drift.
- Lugauer's "labeling mismatch" finding shows directly that a different centerline or branch labelling can dominate surface-distance metrics. Report how many pairs were rejected by the matching step.

### Gaps
- The exact way Kirişli 2013 builds the 3D reference surface from the cross-sectional contours, and its evaluation region, could not be verified: the PDF host was unavailable and coronary.bigr.nl has a broken TLS certificate.
- I found no published study that compares an in-house tracer's contours with Medis QAngio CT *contours* in the same CT. All the QAngio CT validations found compare with IVUS.
- Papadopoulou et al. (QAngio CT / IVUS) was not found in these searches. Do not cite it without checking.

---

## 2. Which contour metrics are standard, and which suit a radius/taper downstream feature?

### Takeaway
Segmentation challenges report overlap (Dice) and boundary distances (mean surface distance and maximum surface distance or Hausdorff), split into healthy and diseased segments. Clinical QAngio CT validations report lumen area, MLA, % area stenosis and plaque burden, using correlation (and sometimes Bland–Altman) against IVUS. The downstream features here are r = sqrt(A/pi), its slope along the trunk (taper), and the LM→LAD and LM→LCx ratios, so the primary metric should be **lumen area or equivalent radius agreement per matched cross-section**: Bland–Altman bias and limits of agreement, plus ICC. Report Dice and mean contour distance per section as secondary shape metrics. Better still, compare the *derived feature itself* (taper slope and ratio per trunk) between methods.

### Cited Findings
- Rotterdam lumen metrics: DICE (volumetric overlap), MSD (mean surface distance) and MAXSD (maximum surface distance), reported separately for diseased (D) and healthy (H) segments — [Lugauer et al. 2014, Table 1](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf)
- Agreement between experts on lumen contours is modest. The test-set Dice of each expert against the others was Expert3 79% (D) / 81% (H), Expert1 76/77, Expert2 65/72. MSD was 0.21–0.34 mm and MAXSD 2.8–3.5 mm. The best automatic method had Dice 76/75, MSD 0.32/0.51 mm and MAXSD 2.47/3.67 mm — [Lugauer et al. 2014, Table 1](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf)
- Another Rotterdam participant reported Dice 68% (healthy) and 65% (diseased) — [search summary of Shahzad et al. 2013, repub.eur.nl](https://repub.eur.nl/pub/17397) (not fetched).
- Boogers 2012 (QCT vs IVUS) reported only correlations in the abstract: MLA r = 0.75, lumen area stenosis r = 0.79, plaque burden at MLA r = 0.70, mean plaque burden r = 0.64, remodelling index r = 0.56 — [PubMed](https://pubmed.ncbi.nlm.nih.gov/22285583/)
- In the bifurcation study, mean CTCA − IVUS lumen area was −0.61 ± 3.63 mm² (proximal main branch), −1.58 ± 2.07 (carina), −1.72 ± 2.81 (distal) and −2.22 ± 0.95 (MLD). The abstract and the table disagree on values and signs, which suggests the paper has reporting errors — [Radunović et al. 2023](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2023.1292517/full)
- Taha & Hanbury analyse 20 segmentation metrics and give guidelines for choosing a subset to suit the data and task. They also note that the literature defines metrics inconsistently — [Taha & Hanbury 2015](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4533825/)
- Metrics Reloaded is a framework for choosing validation metrics through a "problem fingerprint", covering semantic segmentation among other tasks — [Maier-Hein et al. 2024](https://wrap.warwick.ac.uk/183654)

### Inferences
- Correlation (r) measures association, not agreement. The Boogers-style r values would not show a systematic offset in r. Taper and ratios are differences and ratios of radii, so a *constant* bias in r cancels in taper (a slope) and mostly cancels in ratios. A *proportional* bias, or one that depends on location, does not cancel. Bland–Altman with the bias regressed on the mean (and on arc position) is therefore the informative analysis.
- Dice for small 2D objects (lumen r of about 1–2.5 mm) is very sensitive to sub-voxel boundary shifts. A 0.2 mm shift on a 1.5 mm radius gives Dice of about 0.87. The expert-level Dice of 65–80% is a useful benchmark for "as good as a second reader". This is my own arithmetic; Metrics Reloaded warns about overlap metrics on small structures, but I did not verify that passage.
- Hausdorff or MAXSD is dominated by single outlier points (e.g. side-branch leakage). Use the 95th percentile, or report it only as a secondary measure.
- The recommended hierarchy for this thesis: (1) per-section area or r_eq agreement (Bland–Altman bias and 95% LoA in mm and %, ICC(2,1) or ICC(3,1) absolute agreement); (2) per-trunk feature agreement (taper slope, LM→LAD and LM→LCx ratios) with Bland–Altman and ICC; (3) per-section Dice and mean contour distance as shape descriptors. Minimal lumen diameter matters for stenosis but not for this plaque-free taper question.

### Gaps
- I did not retrieve Kirişli's own definitions, e.g. whether MSD is computed on surfaces or on cross-sections.
- I did not find a QAngio CT paper with Bland–Altman limits for per-section lumen area against IVUS in the full text. Park 2015 and Boogers 2012 likely contain them, but I could not verify this.

---

## 3. Surface-based (3D) or cross-section-based comparison?

### Takeaway
The Rotterdam challenge reports "volumetric" Dice and surface distances, but its reference was drawn as cross-sectional contours on given centerlines. Medis supplies discrete cross-sectional contours, and the tracer produces one contour per step. So a cross-section-based comparison fits the data and the downstream feature, which is a per-section area. A 3D surface comparison would need meshing both sets of contours, which adds interpolation choices and mixes in centerline and branch-labelling disagreement.

### Cited Findings
- Rotterdam: expert annotations were cross-sectional contours made "from the same set of centerlines". The metrics include "volumetric overlap (DICE)" and surface distances — [Lugauer et al. 2014](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf)
- Surface-distance metrics were hurt by a mismatch in centerline labelling, more than Dice was, especially in healthy segments — [Lugauer et al. 2014](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf)
- Earlier Rotterdam-group lumen work reported Dice 0.85 and average symmetric surface distance 0.22 mm (28 arteries, 12 patients) — [search summary, Schaap et al. 2009](https://repub.eur.nl/pub/17381) (not fetched).

### Inferences
- Cross-section-based comparison isolates contour error *given* a location. Centerline agreement should be reported separately, e.g. the distance between tracer and Medis centerlines. A separate note covers the centerline comparison.
- A 3D comparison is only needed if the tracer's output is used as a mesh (e.g. CFD). It is not needed for taper and ratios.

### Gaps
- No source found that compares 2D vs 3D evaluation of coronary lumen head-to-head.

---

## 4. Plaque vs non-plaque sections, bifurcations, calcium blooming

### Takeaway
Standard practice reports healthy and diseased segments separately (Rotterdam). Bifurcation regions are either excluded or analysed as their own class with landmark anchors (carina ± 5 mm). Heavily calcified lesions are often excluded in CT–IVUS work, because calcium blooming hides the lumen border. Every Medis contour here comes from a *diseased* segment, while the thesis cohort is plaque-free. The validation is therefore a harder, shifted domain: errors measured there are probably an upper bound for plaque-free trunks, though this is not proven. Within the Medis segments, the plaque-free cross-sections can be separated from the plaque cross-sections using the lumen versus outer-wall contours (wall thickness near zero).

### Cited Findings
- Rotterdam metrics are split into healthy (H) and diseased (D). Prior methods "tend to focus on healthy vessels and often fail to correctly segment the lumen in diseased regions" — [Lugauer et al. 2014](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf)
- Disagreement between experts was larger in diseased segments: Expert2 Dice 65% (D) vs 72% (H) — [Lugauer et al. 2014](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf)
- Bifurcation study: the carina was defined as the last frame showing the full circumference of both the main and side branch before confluence. The "polygon of confluence" was the carina ± 5 mm. Lumen-area disagreement varied by position (SD of 2.1–3.6 mm² near the bifurcation) — [Radunović et al. 2023](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2023.1292517/full)
- The same study excluded circumferential calcification > 180° and/or ≥ 5 mm length, and type III/IV calcified lesions. Calcium density on CTCA "approaches the density of contrast fluid" and can impede border detection — [Radunović et al. 2023](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2023.1292517/full)
- Lugauer's method explicitly excludes calcium, "in the presence of calcified and non-calcified plaque". The SPIE 2014 paper title is "Improving accuracy in coronary lumen segmentation via explicit calcium exclusion..." (doi:10.1117/12.2043238) — [search summary](https://cris.fau.de/publications/122598124)

### Inferences
- Prespecify an exclusion zone around side-branch ostia and the LM bifurcation, e.g. within one or two parent-vessel diameters, or a fixed 3–5 mm, of a carina. At an ostium the cross-sectional plane cuts both branches, and the two methods may close the contour differently. The 5 mm figure is borrowed from the bifurcation-study convention, not a validated standard. The LM→LAD and LM→LCx ratios need radii *near* the bifurcation, so define them at a fixed offset beyond the exclusion zone, the same offset for both methods.
- Stratify the agreement by section type: (a) no plaque (lumen ≈ outer wall in Medis), (b) non-calcified plaque, (c) calcified plaque (e.g. high-HU voxels inside the outer wall), (d) near a bifurcation. Report Bland–Altman per stratum. Expect (a) to be the most relevant to the plaque-free thesis cohort.
- Be careful with the claim that "the validation is harder, therefore conservative". Diseased segments may also be scanned or read differently, and the reader's contours in plaque are themselves less certain. State it as a limitation, not a guarantee.

### Gaps
- No source found that quantifies the effect of blooming on QAngio CT lumen contours specifically.
- No source found for a standard exclusion distance around a bifurcation in CT contour validation.

---

## 5. Practical steps (frames, resampling, normals, outliers)

### Takeaway
The workflow is not standardised in the literature. Below is a defensible recipe assembled from the sources above and standard geometry. Mostly inferences; flag as such.

### Cited Findings
- Rotterdam-style lumen methods work in centerline-orthogonal cross-sections. Lugauer used a slice distance of 0.3 mm and 64 radial rays per cross-section — [Lugauer et al. 2014](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf)
- Taha & Hanbury stress that metric definitions vary across papers and should be stated explicitly, ideally computed with a standard tool — [Taha & Hanbury 2015](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4533825/)

### Inferences (recipe)
1. **Frames.** Medis is in LPS mm (project data notes). NIfTI or ITK-based tracers often store RAS (nibabel) or LPS (ITK/SimpleITK). Convert explicitly: RAS = diag(−1, −1, 1) · LPS. Use the NIfTI affine (qform/sform) for voxel→world. Check by overlaying both centerlines on the CT and confirming the median centerline distance is below about 1 mm before any contour metrics.
2. **Contour clean-up.** Close each polygon, make the orientation consistent (counter-clockwise in the plane), remove duplicate points, and reject self-intersecting contours.
3. **Plane and normal.** Medis: fit the plane by PCA or SVD of the contour points (normal = smallest singular vector), and check it against the Medis centerline tangent. Tracer: use the step direction. Record the angle between the normals for each pair.
4. **Pairing.** Use the arc-length-from-ostium match, or the nearest centroid in 3D, then gate: centroid distance below a threshold and normal angle below a threshold. Alternatively, reslice the tracer's lumen on the Medis plane.
5. **Resampling.** Resample both contours to a fixed number of points equally spaced in arc length (e.g. 64–128). Compute the area by the shoelace formula in the 2D plane coordinates, r_eq = sqrt(A/pi), the polygon-overlap Dice (e.g. with shapely), the mean symmetric contour distance, and the 95th percentile contour distance.
6. **Exclusions (prespecified).** Exclude sections within X mm of a side-branch ostium or carina, Medis contours flagged incomplete, and degenerate contours. Report counts for each reason.
7. **Outliers.** Do not delete them silently. Report the full Bland–Altman plot, plus a sensitivity analysis without pairs failing the gate. Use log-scale or % differences if the spread grows with size.
8. **Clustering.** Sections are nested in segments, which are nested in persons. Bland–Altman limits from pooled sections understate the uncertainty. Use repeated-measures Bland–Altman (Bland & Altman 2007 for multiple observations per subject; not retrieved here) or summarise per segment first.
9. **Primary endpoint.** Agreement of per-trunk taper and of the LM→LAD and LM→LCx ratios between tracer and Medis, computed on the same arc-length window.

### Gaps
- No source found that prescribes a specific number of contour points or gating thresholds. These are design choices to prespecify.

---

## 6. Reporting agreement or reproducibility of area and diameter

### Takeaway
Use Bland–Altman (bias, 95% LoA) for agreement and ICC (state the form: two-way, absolute agreement, single measure) for reliability. Do not rely on Pearson r alone, though older QAngio CT validations lead with it. Report the stratified results (healthy vs diseased, near vs away from a bifurcation).

### Cited Findings
- Boogers 2012 reports Pearson r only, in the abstract — [PubMed](https://pubmed.ncbi.nlm.nih.gov/22285583/)
- Bland–Altman (Bland & Altman 1986, Lancet) is the standard method for agreement between two clinical measurement methods. One applied study defines LoA as mean ± 1.96 SD — [PMC12064138](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12064138/)
- The bifurcation study reports per-location mean ± SD differences in lumen area against IVUS. Its abstract and table are inconsistent: an example of a reporting failure to avoid — [Radunović et al. 2023](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2023.1292517/full)
- Park 2015 compared expert, non-expert and fully automatic QAngio CT analyses against IVUS (150 segments, 142 patients) and called the automatic performance "excellent". The specific agreement numbers were not retrieved — [Yonsei record](https://ir.ymlib.yonsei.ac.kr/handle/22282913/141694)
- The inter-expert Rotterdam numbers (Dice 65–81%, MSD 0.21–0.34 mm) give a reference for how much two human readers disagree on CT lumen contours — [Lugauer et al. 2014](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf)

### Inferences
- Medis contours are a reader-edited *reference*, not ground truth. The framing should be "agreement with a reference" (Bland–Altman, ICC), not "accuracy". If no repeated Medis reads exist, the reference's own variability cannot be estimated from these data. Cite the Rotterdam inter-expert disagreement as context for the size to expect.
- Suggested reporting: per-section r_eq difference (tracer − Medis) with bias and LoA in mm and %, ICC(A,1), and the same for taper and ratios at trunk level. Stratify by plaque status of the section and by distance to a bifurcation. Also report the number of pairs and the exclusions.
- For the ICC form, cite Koo & Li 2016 (J Chiropr Med 15:155–163, doi:10.1016/j.jcm.2016.02.012). It was not retrieved in this session; verify it before citing.

### Gaps
- I did not retrieve a study comparing lumen area between two CT software packages (e.g. QAngio CT vs another vendor) on the same scans. That would be the closest analogue to tracer vs Medis. A targeted search on "inter-software" or "inter-vendor" CT plaque quantification agreement is recommended.
- I could not verify the Bland–Altman 2007 (repeated measures) and Koo & Li 2016 details in this session.
