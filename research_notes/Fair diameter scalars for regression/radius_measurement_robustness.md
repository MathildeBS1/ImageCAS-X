# Radius measurement along coronary centerlines and robustness of diameter scalars

Scope: how per-point lumen radius is defined and measured along CTA centerlines (VMTK MaximumInscribedSphereRadius vs cross-sectional equivalent radius vs distance transform), known artefacts (bifurcations, partial volume, calcium blooming), and which scalar summaries are stable enough to use as a fair logistic-regression baseline against a per-point sequence model on ImageCAS-X (0.5 mm isotropic; distal RCA radius ~1 to 1.5 mm = 2 to 3 voxels).

Research budget note: about 20 tool calls. Several primary full texts (Dodge 1992 Circulation, Lancet Digital Health 2022, the Reproducibility PMC paper) returned 403 or captcha, so numbers from them are taken from search-result snippets and flagged as such.

## Radius definitions: MISR vs equivalent-area radius vs distance transform

### Takeaway
VMTK's MaximumInscribedSphereRadius (MISR) is a Voronoi-based inscribed-sphere radius: by construction it is a lower bound on the local lumen size and is systematically smaller than a circle-equivalent (area-based) radius. In one direct comparison it was 0.21 to 0.24 mm smaller (median) than the circle-equivalent radius, which at a 1 to 1.5 mm distal coronary radius is a 15 to 25% relative offset. For elliptical or eccentric lumens (stenoses) the inscribed radius tracks the minor axis, whereas the equivalent-area radius tracks area.

### Cited Findings
- VMTK computes centerlines from the Voronoi diagram of the surface, and each centerline point carries the radius of the maximally inscribed sphere (MISR); this array is the basis for VMTK's branch splitting and bifurcation analysis. Framework paper: Piccinelli M, Veneziani A, Steinman DA, Remuzzi A, Antiga L, "A framework for geometric analysis of vascular structures: application to cerebral aneurysms", IEEE TMI 2009;28(8):1141-55 — [VMTK tutorials / search summary](http://www.vmtk.org/tutorials/GeometricAnalysis.html); [VMTK Branch Splitting](http://www.vmtk.org/tutorials/BranchSplitting.html); [Improved prediction of disturbed flow via geometric variables (PMC3371282)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3371282)
- In the VMTK bifurcation reference system, the bifurcation origin is "the barycenter of the four reference points weighted by the surface of the maximum inscribed sphere defined on the reference points. The reason of the weighting is that small branches have less impact on the position of the bifurcation origin." — [VMTK GeometricAnalysis tutorial (GitHub source)](https://github.com/vmtk/vmtk.github.com/blob/master/tutorials/GeometricAnalysis.md)
- Musio et al. (2025, TopCoW Circle-of-Willis centerline graphs, 200 patients, MRA+CTA) computed three radii per centerline edge: Voreen's average radius, a circle-equivalent (CE) radius from cross-sectional area, and an MIS radius "defined as the 10th percentile of distances from the centerline to the vessel surface". "The median of the pairwise differences between Voreen and CE radius estimates is very near zero... The MIS radii are consistently smaller, with median differences of 0.21–0.24 mm, reflecting their more conservative definition." They adopted CE radius for all morphometrics. — [Musio et al., arXiv 2510.13720, Suppl. B.1](https://arxiv.org/abs/2510.13720)
- The same paper reports segment radius, length and bifurcation ratios as robust between reference and predicted centerline graphs: median relative error below 5% and Pearson r above 0.95; curvature had the highest error and lowest correlation. The tiny, globular Acom segment was excluded because of much higher error. — [Musio et al., arXiv 2510.13720](https://arxiv.org/abs/2510.13720)
- A single scalar radius per centerline point can represent an axis-offset eccentric stenosis with locally circular cross-sections but "cannot directly encode circumferentially varying D-shaped, irregular, or multilobed sections." — [Search summary citing arXiv 2609.19290](https://arxiv.org/pdf/2609.19290)
- CT-vs-IVUS validation (Chen/Kassab group, PLoS One 2014, 64-slice CCTA, 5 patients, 11 arteries, 1314 matched pairs) computed diameter "from an inscribed circle fitted in the CSA" rather than assuming circularity, to capture non-circular stenoses. — [IVUS validation of CT lumen area, PMC3906085](https://pmc.ncbi.nlm.nih.gov/articles/PMC3906085/)
- Quantitative CCTA study (160 patients, 210 segments with FFR): diameter calipers on oval lumens from eccentric plaque give "arbitrary diameter caliper anchor point placement" and higher interobserver variability; area-based measures were more reproducible and more predictive (see robustness section). — [Quantitative CCTA: absolute lumen sizing, PMC5052288](https://pmc.ncbi.nlm.nih.gov/articles/PMC5052288/)

### Inferences
- For an ellipse with semi-axes a > b, the inscribed radius is about b, while the equivalent-area radius is sqrt(ab). So MISR/CE ratio = sqrt(b/a); a 2:1 ellipse gives MISR about 29% below CE. Stenoses with eccentric plaque therefore look more severe in MISR than in area terms. This is geometry, not a cited result.
- An Euclidean distance transform sampled at the centerline voxel equals the inscribed radius quantised to the voxel grid (plus up to half a voxel boundary uncertainty). At 0.5 mm voxels and 1 to 1.5 mm radii, that is a +-0.25 mm quantisation, i.e. up to about 20% relative noise distally. MISR computed from a smoothed marching-cubes surface is sub-voxel but inherits the surface's smoothing bias.
- Because ImageCAS-X centerlines ship with MISR, and the systematic MISR offset is roughly constant in mm, ratio features (e.g. distal/proximal) partially cancel it, whereas absolute distal radii carry it fully.

### Gaps
- I did not obtain a coronary-specific (rather than cerebral) head-to-head of MISR vs equivalent-area radius vs IVUS. The Musio numbers are from Circle of Willis vessels (radius ~1 to 1.5 mm, similar scale).
- Piccinelli 2009 full text was not fetched; no exact statement on MISR bias in stenoses from it.

## Bifurcation handling

### Takeaway
At a branch point the inscribed sphere expands into the junction, so MISR is inflated there. VMTK handles this by branch splitting: each centerline is divided into groups, and the bifurcation region is defined by spheres (reference points one MISR / one sphere downstream), so the "blanked" bifurcation tract can be dropped. Published pipelines either blank the bifurcation group or exclude a fixed region around branch points.

### Cited Findings
- VMTK's `vmtkbranchextractor` splits centerlines into branches and bifurcation groups (GroupIds; bifurcations flagged, identified by group id), and the surface can then be split into branches "using the fact that each centerline is associated with maximum inscribed sphere radii". — [VMTK Branch Splitting tutorial](http://www.vmtk.org/tutorials/BranchSplitting.html); [VMTK GeometricAnalysis](https://github.com/vmtk/vmtk.github.com/blob/master/tutorials/GeometricAnalysis.md)
- Bifurcation reference points are taken one per tract at the bifurcation, and the origin is MISR-weighted. — [VMTK GeometricAnalysis](https://github.com/vmtk/vmtk.github.com/blob/master/tutorials/GeometricAnalysis.md)
- Carotid geometry work parameterised each branch "using an objective distance metric based on the local MISR" (i.e. distances from the bifurcation expressed in MISR units, following Antiga and Steinman 2004). — [Bijari/Steinman-group PMC3371282](https://pmc.ncbi.nlm.nih.gov/articles/PMC3371282)
- TopCoW centerline morphometrics exclude edges "between bifurcation points and the boundaries of child vessels" from segment radius statistics. — [Musio et al. 2025](https://arxiv.org/abs/2510.13720)
- The CT-vs-IVUS CSA pipeline "can only process a straight vessel without bifurcation", requiring manual removal of side branches. — [PMC3906085](https://pmc.ncbi.nlm.nih.gov/articles/PMC3906085/)

### Inferences
- A pragmatic rule consistent with VMTK practice: mask centerline points within about 1 to 2 MISR (or a fixed ~1 to 2 mm) of each branch point before computing summaries, and use robust statistics (median rather than mean) so residual spikes do not dominate. Whether ImageCAS-X VTK centerlines carry VMTK's Blanking/GroupIds arrays should be checked in the files; if not, branch points can be found from the topology graph.
- For the neural sequence model, the same bifurcation spikes are present in the input; to keep the comparison fair, either both models see masked profiles or neither does.

### Gaps
- No coronary paper found that states an exact "exclude N mm around bifurcations" rule for radius profiles; the value above is inferred.

## Resolution, partial volume and calcium blooming

### Takeaway
CTA lumen size in 2 to 4 mm coronaries has roughly 8 to 10% diameter error vs IVUS in favourable conditions, but in stenoses CT underestimates minimal lumen diameter by about 21% on average, and calcium blooming inflates stenosis severity by several to 30+ percentage points in 3 mm phantom lumens. Partial volume matters most exactly where the ImageCAS-X distal RCA sits (2 to 3 voxels across the radius).

### Cited Findings
- 64-slice CCTA vs IVUS (5 patients, 11 arteries, 1314 matched pairs): diameter RMSE 9.5% (normalised to mean), mean percent error 7.9%, fit y = 0.97x + 0.057; CSA RMSE 16.2%, mean percent error LAD 11.2%, LCx 8.3%, RCA 7.9%, fit y = 0.95x + 0.23. — [PMC3906085 (PLoS One 2014)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3906085/)
- Meta-analysis of CCTA vs intravascular imaging (Fischer/Voros et al., JACC Imaging 2011): on a segmental basis CT underestimated minimum luminal diameter by 21% and overestimated diameter stenosis by 39%; minimal luminal area was overestimated by 27% while area stenosis was underestimated by only 5%. — [JACC Cardiovasc Imaging 2011, 10.1016/j.jcmg.2011.03.006](https://www.jacc.org/doi/10.1016/j.jcmg.2011.03.006) (numbers from search snippet; full text not fetched)
- Partial volume: full-width-half-maximum style radius estimation is biased where the lumen is small relative to the point-spread function; explicitly modelling partial volume in automatic coronary lumen segmentation (MICCAI 2012 challenge data) improved maximal surface distance error by about 39% and raised the AUC of CT-FFR for FFR <= 0.8 from 0.69 to 0.79 (N = 76, DeLong p = 0.012). — [Freiman et al., arXiv 1906.09763](https://arxiv.org/pdf/1906.09763)
- Calcium blooming, 3 mm lumen phantom (4.5 mm vessel), energy-integrating CT vs photon-counting CT measured stenosis: one-sided 50% -> 56.9% (EID) / 54.8% (PCD); one-sided 25% -> 33.1% / 25.1%; ring 50% -> 82.5% / 66.9%; ring 75% -> 100% (read as occluded) / 90.8%. — [PMC9171751](https://pmc.ncbi.nlm.nih.gov/articles/PMC9171751/)
- Blooming is predominantly a partial-volume effect and may cause overestimation of stenosis in heavily calcified lesions; phantom work on 2, 3 and 5 mm vessels with calcified plaque exists. — [Wang et al., Cardiovasc Diagn Ther, PMC13554304](https://pmc.ncbi.nlm.nih.gov/articles/PMC13554304); [PMC11362394](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11362394/)
- Conventional SCCT stenosis grading is limited to segments with diameter >= 1.5 mm. — [SCCT guidelines search summary](https://www.journalofcardiovascularct.com/article/S1934-5925(09)00070-7/fulltext)

### Inferences
- ImageCAS scans are older-generation energy-integrating CT, so blooming-driven local radius dips at calcified plaque are expected in the reference labels too; a CAS-Net prediction and the reference will differ most at exactly those points. Minimum-type scalars absorb this noise; median-type scalars dilute it.
- The 1.5 mm diameter floor used clinically (0.75 mm radius) is close to the ImageCAS-X distal RCA range; points below it are near the resolution limit and are candidates for truncation rather than measurement.

### Gaps
- No study found quantifying CTA radius bias specifically for 1 to 1.5 mm radii at 0.5 mm isotropic resampling (as opposed to native ~0.35 to 0.5 mm in-plane, 0.5 to 0.75 mm slice).

## Robustness and reproducibility of candidate scalars

### Takeaway
Across studies, area-based and aggregate (averaged or volumetric) lumen measures are more reproducible than minimum-type or ratio-to-reference measures. Percent stenosis depends on a reference diameter definition (nearest normal proximal segment, two-sided average, or a fitted taper), and that choice is a major source of variance. For a regression baseline, median radius over a fixed proximal window is the most defensible; minimum and percent-stenosis-vs-taper are the least robust.

### Cited Findings
- Quantitative CCTA with FFR (160 patients, 210 segments): reference = "the closest normal proximal cross-sectional vessel area and diameter", or the closest distal one if the lesion is ostial. Inter-method/observer correlation was highest for MLA (r = 0.63), then MLD (r = 0.56), %diameter stenosis (r = 0.49), %area stenosis (r = 0.40). AUC for FFR < 0.8: MLA 0.97, MLD 0.92, %area stenosis 0.89, %diameter stenosis 0.87. — [PMC5052288](https://pmc.ncbi.nlm.nih.gov/articles/PMC5052288/)
- Deep-learning plaque/stenosis quantification (Lin et al., Lancet Digital Health 2022, international multicentre): quantitative diameter stenosis agreement between two expert readers ICC 0.915 to 0.973; DL reproducibility ICC 0.975 to 1; DL vs IVUS minimal luminal area ICC 0.904. — [Lancet Digit Health 2022](https://www.thelancet.com/journals/landig/article/PIIS2589-7500(22)00022-X/fulltext) (numbers from search snippet; page returned 403)
- In a quantitative CCTA reproducibility study, intra- and inter-observer concordance for minimal lumen diameter was CCC 0.92 and 0.86. — [PMC6294364 / PubMed 30550593](https://pubmed.ncbi.nlm.nih.gov/30550593/) (snippet; full text behind captcha)
- Fusion-based quantification defines percent diameter stenosis by dividing the narrowest lumen diameter by the average of two normal reference cross-sections (proximal and distal), with a reference line estimating normal tapering. — [PubMed 23417447](https://pubmed.ncbi.nlm.nih.gov/23417447/?dopt=Abstract) (snippet)
- In TopCoW, segment-level radius (averaged over the segment) from predicted graphs matched reference with median relative error < 5%, r > 0.95, whereas curvature (a pointwise, derivative-based feature) was least reliable. — [Musio et al. 2025](https://arxiv.org/abs/2510.13720)

### Inferences
- Ranking for robustness to segmentation noise, distal truncation and missing branches (inferred from the above plus sampling statistics):
  1. Median radius over a fixed proximal window (e.g. first 10 to 20 mm after the ostium, bifurcations masked): unaffected by distal truncation, insensitive to single-point spikes; most robust.
  2. Mean radius over the same window: similar, but bifurcation and blooming spikes leak in.
  3. Whole-vessel mean/median: biased by distal truncation, because a shorter segmented vessel drops the thinnest points and raises the mean. CAS-Net vs reference truncation differences directly become radius differences.
  4. Taper slope (linear fit of r vs arc length): depends on both endpoints, so truncation changes it; robust-regression (Theil-Sen/Huber) helps.
  5. Minimum radius and percent stenosis vs fitted taper: single-point statistics that inherit blooming, partial volume and bifurcation artefacts; the published r = 0.49 to 0.56 for MLD/%DS inter-method correlation versus r = 0.63 for MLA shows this.
- For fairness: the per-point sequence model can in principle learn to ignore artefacts, while a scalar cannot, so a naive whole-vessel mean handicaps the logistic regression. Computing the scalar from the same masked, truncated-to-common-length profile the sequence model sees is the fairest pairing.
- If a minimum-type scalar is wanted, a low percentile (e.g. 5th or 10th) of radius over a window is a middle ground, analogous to Musio's 10th-percentile MIS definition.

### Gaps
- No study found reporting ICC of taper slope, or of mean-vs-median radius, specifically comparing algorithmic vs reference segmentations in coronaries.
- No quantitative study found on how distal truncation of segmented coronaries changes vessel-mean radius; this could be measured directly on ImageCAS-X by truncating reference centerlines to CAS-Net predicted length.

## Arc-length windows: fixed mm vs normalised length; SCCT segments

### Takeaway
Clinical segment definitions (SCCT 18-segment, derived from AHA) are anatomical, not metric: they are tied to landmarks (acute margin, PDA origin, branch origins), so their lengths vary per patient. Fixed-mm windows from the ostium are landmark-free and truncation-robust; normalised-length windows are sensitive to where the segmented vessel ends.

### Cited Findings
- RCA per SCCT/AHA: proximal = ostium to one half the distance to the acute margin; mid = end of proximal to acute margin; distal = acute margin to origin of the PDA. The proximal/mid boundary is often marked by a large acute marginal branch. — [SYNTAX/segment definitions summary (ResearchGate figure)](https://www.researchgate.net/figure/Definition-of-the-coronary-tree-segments-1-RCA-proximal-From-the-ostium-to-one-half_fig1_323968281); [Radiology Assistant CAD-RADS 2.0](https://radiologyassistant.nl/cardiovascular/cad-rads/coronary-artery-disease-reporting-and-data-system)
- The SCCT 18-segment model differs from the 1975 AHA scheme by adding ramus intermedius (segment 17) and left posterolateral branch (segment 18); all segments are to be analysed with it. — [2014 SCCT reporting guidelines](https://www.researchgate.net/publication/271225902_2014_SCCT_guidelines_for_the_interpretation_and_reporting_of_coronary_CT_angiography_A_report_of_the_Society_of_Cardiovascular_Computed_Tomography_Guidelines_Committee)
- When anatomical landmarks are absent, TopCoW defined sub-segments by fixed lengths equal to the population median lengths (A1, P1, C7: e.g. 15.57 mm for the first). — [Musio et al. 2025, Suppl. B.2](https://arxiv.org/abs/2510.13720)

### Inferences
- A fixed proximal window (e.g. 0 to 20 mm from ostium, or population-median proximal RCA length) mirrors the TopCoW fallback and is independent of distal truncation. Normalised arc length (0 to 1) moves every point whenever the distal end moves, so it is not recommended for a scalar that must match between reference and CAS-Net centerlines.
- ImageCAS-X centerlines do not carry the acute margin landmark, so SCCT proximal/mid/distal cannot be reproduced exactly without labelling; fixed-mm is the practical proxy.

### Gaps
- No published population median proximal-RCA length in mm was retrieved.

## Normalising for heart size

### Takeaway
Coronary diameter scales weakly with myocardial mass (exponent about 0.22) and with body size (roughly sqrt(BSA)); women have ~9% smaller coronaries even after BSA normalisation. Ratio features (e.g. distal/proximal radius, or radius relative to the vessel's own proximal reference) are an internal normalisation that needs no BSA, which ImageCAS-X likely lacks.

### Cited Findings
- Dodge et al. (Circulation 1992) normal angiographic diameters: left main 4.5 +- 0.5 mm, proximal LAD 3.7 +- 0.4 mm, distal LAD 1.9 +- 0.4 mm; women had 9% smaller epicardial diameter (p < 0.001) even after BSA normalisation. — [Dodge et al., Circulation 1992;86:232](https://www.ahajournals.org/doi/pdf/10.1161/01.cir.86.1.232) (snippet; PDF returned 403)
- Allometric scaling on CCTA (Choi et al., Physiol Rep 2020; 43 patients, 638 arteries, branches >= 1.0 mm): exponents vs artery-specific myocardial mass: diameter 0.224 +- 0.082, length 0.795 +- 0.140, volume 1.080 +- 0.229. Authors propose that expected vessel size can be defined from perfused myocardial mass. — [PMC7387886](https://pmc.ncbi.nlm.nih.gov/articles/PMC7387886/)
- Across cardiovascular structures, BSA is a stronger determinant of size than age, height or weight alone, with vascular and valve diameters relating linearly to sqrt(BSA). — [Sluysmans and Colan, J Appl Physiol 2005](https://journals.physiology.org/doi/pdf/10.1152/japplphysiol.01144.2004) (snippet)

### Inferences
- With diameter ~ M^0.22, a 50% difference in myocardial mass gives only ~9% difference in diameter, comparable to CT measurement error (~8 to 10%). Heart-size normalisation is thus second-order relative to artefact handling, but sex should be included as a covariate if available.
- Ratio features (distal-window median / proximal-window median) cancel both body size and a constant MISR offset, which is attractive for fairness with the sequence model.

### Gaps
- ImageCAS-X metadata (Descriptors.xlsx) lists image quality, dominance and disease; whether sex/BSA are available was not checked here.
- Dodge 1992 regression coefficients against BSA/LV mass could not be retrieved (403).
