# Comparing an automatic coronary centerline against a reference (Medis) centerline

Scope note: the in-house tracer is compared with reader-analysed Medis trees, and Medis is treated as a reference, not ground truth. These notes do not cover CAS-Net. Sources were checked in this session unless a line says otherwise. Schaap et al. 2009 was read in full (NIH author manuscript). Wolterink et al. 2019 was read in full (arXiv version of the Med Image Anal paper).

## 1. Standard evaluation framework (Rotterdam / CAT08) and later benchmarks

### Takeaway
The Rotterdam Coronary Artery Algorithm Evaluation Framework (Schaap et al. 2009, CAT08) is still the standard for comparing coronary centerlines. It works in four steps:
1. Resample both lines equidistantly (0.03 mm).
2. Clip the evaluated line at a disc placed at the reference ostium.
3. Find a monotone minimal-total-Euclidean-length point correspondence with Dijkstra.
4. Label points TP/FP/FN using the *local reference lumen radius* as the threshold.

From this it reports overlap (OV, OF, OT) and the accuracy of the matched part (AI). Later coronary benchmarks (Kirişli 2013, ASOCA, ImageCAS) evaluate stenosis or lumen *segmentation*, not centerlines. Centerline papers such as Wolterink 2019 still report CAT08 metrics.

### Cited findings

**Full citation.** Schaap M, Metz CT, van Walsum T, van der Giessen AG, Weustink AC, Mollet NR, Bauer C, Bogunović H, Castro C, Deng X, Dikici E, O'Donnell T, Frenay M, Friman O, Hernández Hoyos M, Kitslaar PH, Krissian K, Kühnel C, Luengo-Oroz MA, … Niessen WJ. "Standardized evaluation methodology and reference database for evaluating coronary artery centerline extraction algorithms." *Medical Image Analysis* 2009;13(5):701–714. doi:10.1016/j.media.2009.06.003. PMID 19632885. — [EUR repository](https://repub.eur.nl/pub/24468)

**Data and reference standard**
- The database has 32 CCTA datasets: 8 for training, 24 for testing. In each dataset, 4 vessels were annotated (RCA, LAD, LCX and one large side branch), giving 128 vessels. — [Schaap 2009, author manuscript](https://cdr.lib.unc.edu/downloads/cn69mc016)
- The reference standard was built as follows. — [Schaap 2009](https://cdr.lib.unc.edu/downloads/cn69mc016)
  - Three observers annotated each centerline, and the lumen radius at least every 5 mm. The radius was chosen so that the circle's area matched the lumen area.
  - The three paths were averaged with a mean-shift algorithm for open curves that weights each observer by locally estimated accuracy.
  - Observers then corrected their paths against the average using CPRs, and the consensus was recomputed.
  - Annotation took about 300 h in total.
  - Reference centerlines were on average 138 mm long (SD 41, range 34–249).
- Start and end of the reference were taken as the points where two observers' centerlines first lie within the reference radius, traversing from each end. The start is assumed to lie in the ostium. — [Schaap 2009](https://cdr.lib.unc.edu/downloads/cn69mc016)

**Correspondence (section 4.3)** — [Schaap 2009](https://cdr.lib.unc.edu/downloads/cn69mc016)
- Both centerlines are resampled equidistantly at 0.03 mm.
- The evaluated centerline is clipped with a disc at the reference start: radius = 2× the annotated vessel radius, normal = tangent of the reference at its start. Points before the first intersection with the disc are ignored. The stated reason is that "for a variety of applications the centerline can start somewhere in the aorta".
- The correspondence is the ordered set of connections C = {c0…c_{n+m−1}} that minimises the sum of Euclidean lengths of all point–point connections. Constraints:
  - c0 = [p0, q0];
  - the last connection joins the two end points;
  - each step advances exactly one index on one curve, [pa+1, qb] or [pa, qb+1].
- Every point is thus connected to at least one point on the other curve. The optimum is found with Dijkstra on a matrix of connection lengths. This is effectively a dynamic-time-warping alignment with a sum-of-distances cost.

**Point labels (section 4.4.1)** — [Schaap 2009](https://cdr.lib.unc.edu/downloads/cn69mc016)
- A reference point is TPR_ov if the distance to at least one connected evaluated point is less than the annotated radius at that reference point. Otherwise it is FN_ov.
- An evaluated point is TPM_ov if at least one connected reference point lies within that reference point's radius. Otherwise it is FP_ov.

**Metrics** — [Schaap 2009](https://cdr.lib.unc.edu/downloads/cn69mc016)
- **OV (overlap)** = (‖TPM_ov‖ + ‖TPR_ov‖) / (‖TPM_ov‖ + ‖TPR_ov‖ + ‖FN_ov‖ + ‖FP_ov‖). The paper calls it "similar to the well-known Dice coefficient". The formula image did not extract from the PDF; this is the standard form, consistent with the text and with Wolterink 2019.
- **OF (overlap until first error)** = TPR_of / (TPR_of + FN_of).
  - The first error is the first FN_ov point traversing from the start of the reference, *ignoring FN points in the first 5 mm*.
  - The 5 mm equals the average diameter annotated at the start of the references. The paper's justification is that the start "is sometimes difficult to define".
- **OT (overlap with the clinically relevant part)** is OV restricted to the clinically relevant part of the vessel.
  - That part runs from the reference start to the most distal reference point with radius ≥ 0.75 mm (diameter ≥ 1.5 mm), plus the evaluated points connected to it.
  - Segments ≥ 1.5 mm diameter, or proximal to such segments, count as clinically relevant.
- **AI (average inside)** is the mean length of all connections shorter than the annotated radius at the connected reference point. It is the accuracy "provided that the evaluated centerline is inside the vessel". The paper explicitly separates extraction *capability* (overlap) from *accuracy* (distance), and does not include tracking-failure distances in the accuracy measure.
- **Scores and ranking**
  - Each measure is converted to a score relative to inter-observer performance: 100 = perfect, 50 = equal to the observers.
  - For AI, scores are computed per connection, against the local inter-observer variability.
  - Methods are ranked by averaging ranks.

**Wolterink et al. 2019**
- **Full citation.** Wolterink JM, van Hamersvelt RW, Viergever MA, Leiner T, Išgum I. "Coronary artery centerline extraction in cardiac CT angiography using a CNN-based orientation classifier." *Medical Image Analysis* 2019;51:46–60. doi:10.1016/j.media.2018.10.005. Preprint: arXiv:1810.03143. — [arXiv](https://arxiv.org/pdf/1810.03143)
  - The DOI is from memory and was not shown on the fetched page; verify before use.
- It describes the CAT08 metrics in compact form: "A TP point lies within the radius of the closest reference point, a FP point does not lie within the radius of any reference point and a FN point is a reference centerline point for which there is no corresponding automatically extracted point". It also notes that AI is "to some extent independent of the overlap". — [Wolterink 2019](https://arxiv.org/pdf/1810.03143)
- Results:
  - CAT08 training set, leave-one-out: OV 95.7%, OF 87.1%, OT 97.1%, AI 0.23 mm. Inter-observer difference on the training set is 0.20 mm.
  - CAT08 test set (24 scans, 96 vessels): OV 93.7%, OF 81.5%, OT 97.0%, AI 0.21 mm.
  - — [Wolterink 2019](https://arxiv.org/pdf/1810.03143)
- Failure modes noted: premature termination at myocardial bridging, and continuing into an adjacent vein or artery after the true distal end. These mainly hurt OV/OF, not AI. — [Wolterink 2019](https://arxiv.org/pdf/1810.03143)
- Lower image quality lowered performance: images rated "poor" had OV 86.7% and AI 0.26 mm. — [Wolterink 2019](https://arxiv.org/pdf/1810.03143)
- Because CAT08 has only 4 vessels per patient, Wolterink added a sparse-reference evaluation. In 50 in-house scans, about 5,448 expert markers with radii were placed roughly every 10 mm. A marker counted as hit if it lay within its radius of an extracted centerline point. Tree completeness was evaluated on orCaScore data. Automatic radius vs reference radius was reported with Bland–Altman; the 95% LoA were below one voxel. — [Wolterink 2019](https://arxiv.org/pdf/1810.03143)

**Kirişli et al. 2013** is the follow-up framework from the same Rotterdam group, for stenosis detection, stenosis quantification and lumen segmentation in CTA (not centerlines).
- *Medical Image Analysis* 2013;17(8):859–876.
- doi:10.1016/j.media.2013.05.007. The DOI follows from the ScienceDirect PII S1361841513000819; the full author list and the metric details were not verified this session.
- — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1361841513000819)

**ASOCA**
- Gharleghi R, et al. "Automated segmentation of normal and diseased coronary arteries – The ASOCA challenge." *Computerized Medical Imaging and Graphics* 2022;97:102049. doi:10.1016/j.compmedimag.2022.102049. — [ASOCA citation policy](https://asoca.grand-challenge.org/CitationPolicy/)
- It is a lumen *segmentation* challenge evaluated with Dice and 95% Hausdorff distance. Data: 40 training CCTAs (20 normal, 20 with CAD) and 20 test CCTAs. — [ASOCA site](https://asoca.grand-challenge.org/)
- Data descriptor: arXiv:2211.01859, also published in *Scientific Data* 2023. — [arXiv](https://arxiv.org/pdf/2211.01859)

### Inferences
- For a tracer-vs-Medis comparison, the Schaap pipeline is the defensible default. It is the most cited coronary-specific protocol, every step is explicitly defined, and its radius-relative threshold suits vessels whose diameter varies from about 4 mm to about 1 mm.
- A small adaptation is needed. Medis supplies a lumen contour (or radius) per centerline point, so the local reference radius can come from Medis contours, or from the tracer's own lumen contour as a sensitivity check.
- Medis is not a multi-observer consensus. The framework's "score relative to inter-observer variability" therefore cannot be reproduced. Report the raw OV/OF/OT/AI only, and note that disagreement is a combined error of both methods.
- The ImageCAS and ASOCA benchmarks are about voxel segmentation (Dice/HD). They do not directly provide a centerline-comparison protocol.

### Gaps
- The OV/OT formula images did not extract from the PDF. The OV form above is standard but was rebuilt from the text, not quoted.
- Kirişli 2013 lumen-segmentation metric details were not checked this session. From memory, they are Dice, mean surface distance and maximum surface distance on the segments, compared against 3 observers.
- No ImageCAS paper was fetched. It is a segmentation dataset (Zeng A et al., *Comput Med Imaging Graph* 2023, doi:10.1016/j.compmedimag.2023.102287, from memory, verify) and is not needed for centerline evaluation.

## 2. Establishing point correspondence

### Takeaway
There are three families of options:
- nearest-point projection (closest point on the other curve);
- arc-length parameterisation (compare points at equal distance from a landmark);
- monotone optimal alignment (Schaap's minimal-sum Dijkstra correspondence, equivalent to DTW).

The monotone alignment is the published coronary standard. It keeps the ordering of points, and every point on both curves is matched.

### Cited findings
- Schaap: "All the evaluation measures are based on a point-to-point correspondence". The constraints (start–start, end–end, monotone single-index steps) "guarantee that each point of centerline I is connected to at least one point of centerline II and vice versa". — [Schaap 2009](https://cdr.lib.unc.edu/downloads/cn69mc016)
- The same correspondence was used to transfer observer radii onto the reference standard. — [Schaap 2009](https://cdr.lib.unc.edu/downloads/cn69mc016)
- Wolterink's CAT08 description uses "closest reference point" wording for TP. For the sparse marker set, the criterion is simply that a marker lies within its radius of any extracted point, i.e. a nearest-point rule. — [Wolterink 2019](https://arxiv.org/pdf/1810.03143)

### Inferences (no direct source compares the three options; this is reasoning)

| Method | How it works | Pros | Cons |
|---|---|---|---|
| Nearest point | Each point is matched to the closest point on the other curve, independently | Simple; KD-tree | Can jump to an adjacent vessel or across a loop; not one-to-one; ignores order |
| Arc-length | Points are compared at equal distance from a landmark (e.g. the ostium) | Natural for along-vessel profiles | Errors build up when one curve is longer or wigglier, e.g. a noisy tracer path is longer, so positions drift distally |
| Monotone minimal-cost (Schaap / DTW) | Ordered alignment that minimises the summed distance | Keeps order; handles different sampling and length; the standard | Needs both lines clipped to comparable start and end points (Schaap clips the start with the disc; the end is handled through the FN/FP labels) |

- Practical point: only the monotone method needs both lines to be single ordered paths. Do the comparison *per path* (ostium → distal end of one vessel, or per labelled segment), not on the whole tree.

### Gaps
- I found no paper that formally benchmarks nearest-point against DTW for coronary centerlines.

## 3. Distance metrics: mean, Hausdorff, overlap

### Takeaway
Use overlap (radius-relative hit rate) to measure whether the same vessel was traced, and mean distance over matched points (AI) to measure how accurately it was traced.

Hausdorff (or HD95) is used for surface or segmentation comparison (ASOCA). For centerlines it mostly picks up a single wrong-branch excursion or length difference, so on its own it is a poor summary of centerline accuracy.

### Cited findings
- Schaap separates the two explicitly: "Accuracy can only be evaluated when extraction succeeded; in case of a tracking failure the magnitude of the distance to the reference centerline is no longer relevant and should not be included in the accuracy measure." — [Schaap 2009](https://cdr.lib.unc.edu/downloads/cn69mc016)
- ASOCA evaluates lumen segmentation with Dice and 95% Hausdorff distance. — [ASOCA site](https://asoca.grand-challenge.org/)

### Inferences
- Recommended minimum report, per vessel or trunk:
  - OV, OF, OT (or a simple "% of the Medis path within the local radius");
  - AI in mm, as a median and IQR over patients;
  - optionally the symmetric mean distance over all matched points and HD95, as supplementary figures.
- AI and OV should be judged against voxel size. CAT08 AI values are about 0.2 mm; Wolterink's inter-observer difference is 0.20 mm.

## 4. Different ostium placement and distal reach

### Takeaway
The standard handling is:
- clip the evaluated line at a disc at the reference ostium (radius 2× the reference radius, normal = tangent);
- ignore errors in the first 5 mm for OF;
- let the distal mismatch show up as FN (reference longer) or FP (evaluated line longer);
- report OT, which restricts the comparison to the ≥ 1.5 mm diameter part.

A common-stretch analysis can be added for the geometric features.

### Cited findings
- Disc clipping, the 5 mm OF tolerance, and the OT cutoff at the most distal point with radius ≥ 0.75 mm. — [Schaap 2009](https://cdr.lib.unc.edu/downloads/cn69mc016)
- Wolterink notes that the tracker continues into adjacent vessels "after reaching the artery's most distal point". Distal overshoot is therefore a typical error that is counted as FP. — [Wolterink 2019](https://arxiv.org/pdf/1810.03143)
- In carotid tortuosity comparisons, the start and end landmarks were fixed anatomically (skull base to the carotid bifurcation or the aortic arch) so that packages measured the same stretch. — [de Vries 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6348067/)

### Inferences
- **Reasoning, not sourced.** Medis readers probably checked only the contoured (diseased) part, so distal Medis reach may be arbitrary. That makes FP beyond the Medis end unreliable as an error measure.
- **Suggestion, not sourced.** Report reference-side measures (FN, i.e. sensitivity) and accuracy on the common stretch.
- **Suggestion, not sourced.** Compare features (length, T_5) on a matched common stretch: from the ostium (disc-clipped) to the shorter of the two distal ends, mapped through the correspondence.
- **Inference.** Trunk length is directly sensitive to endpoint placement. Express its agreement as the length difference on the common stretch, and separately as the difference in distal reach.

## 5. Checking segment and artery labels

### Takeaway
Labelling papers use two kinds of metrics:
- segment-level classification metrics: per-label precision, recall and F1, with macro-averages because classes are unbalanced;
- point- or length-level label overlap along the centerline.

Cao 2017 (Medis/LKEB group, Int J Cardiovasc Imaging) is the closest precedent: SCCT/AHA segments, with results by dominance.

### Cited findings
- **Cao Q, Broersen A, de Graaf MA, Kitslaar PH, Yang G, Scholte AJ, Lelieveldt BPF, Reiber JHC, Dijkstra J.** "Automatic identification of coronary tree anatomy in coronary computed tomography angiography." *Int J Cardiovasc Imaging* 2017;33(11):1809–1819. doi:10.1007/s10554-017-1169-0. PMC5677991. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5677991/)
  - **Labels:** AHA 15-segment model plus SCCT additions (RI, OM1/OM2).
  - **Data:** 83 test cases (56 right-dominant, 27 left-dominant), labelled by two experts.
  - **Measures:**
    - presence correctness (definitely correct, semi-correct or wrong, by expert agreement);
    - point-wise *label overlap* along the centerline, i.e. same-label length divided by (TP + FP length);
    - per-patient clinical measures: whether all main-branch segments were found, LM/proximal correct, SIS-weighted and Leaman-weighted proportions.
  - **Results:**

    | Measure | RD | LD |
    |---|---|---|
    | Segments "definitely correct" | 89.2% | 83.6% |
    | Mean label overlap | 92.0% | 90.7% |

    Proximal segments and LM were correct in all patients.
  - Dominance had to be known beforehand.
- **Wu D, Wang X, Bai J, et al.** "Automated anatomical labeling of coronary arteries via bidirectional tree LSTMs." *Int J CARS* 2019;14:271–280. doi:10.1007/s11548-018-1884-6.
  - This is TreeLab-Net. The abstract reports a precision–recall AUC above 97% for LM, LAD, LCX and RCA (10-fold CV).
  - Only the abstract or secondary descriptions were seen.
  - — [Unpaywall record](https://unpaywall.org/10.1007%2FS11548-018-1884-6); [CPR-GCN discussion](https://arxiv.org/pdf/2003.08560)
- **Yang H, Zhen X, Chi Y, Zhang L, Hua X-S.** "CPR-GCN: Conditional Partial-Residual Graph Convolutional Network in Automated Anatomical Labeling of Coronary Arteries." *CVPR* 2020.
  - It reports per-segment precision, recall and F1, plus class-means because of imbalance, on 511 subjects annotated by two experts.
  - The author list is from memory; verify. The search summary flagged that the arXiv recall formula looks like a typo.
  - — [CVF open access](https://openaccess.thecvf.com/content_CVPR_2020/papers/Yang_CPR-GCN_Conditional_Partial-Residual_Graph_Convolutional_Network_in_Automated_Anatomical_Labeling_CVPR_2020_paper.pdf)
- **TopoLab** (MICCAI 2023, arXiv:2307.11959) follows "previous methods" in reporting mean recall, precision and F1 across segment categories, and adds topology metrics. It notes that TreeLab-Net and CPR-GCN use 10 and 11 categories respectively, so their numbers are not directly comparable. — [arXiv](https://arxiv.org/pdf/2307.11959)

### Inferences
- **Simplest defensible check for the thesis:**
  - after correspondence, compute the fraction of matched Medis centerline length whose tracer label equals the Medis label (Cao-style label overlap), per segment;
  - give a segment-level confusion matrix (tracer vs Medis label) for the 9 trunk segments;
  - report per-segment recall and precision, plus the boundary offset (mm along the arc) between corresponding proximal/mid/distal boundaries.
- Boundary offsets matter because prox/mid/distal splits are defined by side-branch landmarks (D1, OM1, RV branch). A shifted boundary changes the per-segment curvature and length even when the line itself is identical.
- Results should be split by dominance, as in Cao 2017.

### Gaps
- Full text of Wu 2019 was not read. Its exact matching rule (segment vs point level) is unverified.

## 6. Preprocessing: coordinates, resampling, smoothing

### Takeaway
Before comparing:
- put both centerlines in the same world frame in mm. DICOM and ITK use LPS; Slicer works internally in RAS; voxel indices must go through the image affine;
- resample both to uniform arc-length spacing (Schaap uses 0.03 mm for correspondence);
- compute curvature only after a fixed, documented smoothing or scale. Curvature is highly sensitive to resolution and smoothing; length and tortuosity index are less so.

### Cited findings
- DICOM and most medical software store data in LPS, and ITK uses LPS. 3D Slicer uses RAS internally and assumes files are LPS unless stated otherwise. RAS and LPS differ by flipping the first two axes. — [Slicer coordinate systems docs](https://slicer.readthedocs.io/en/5.6/user_guide/coordinate_systems.html)
- Mesh formats have no standardised axis directions; ITK-Snap may save meshes in RAS. — [Slicer data loading docs](https://slicer.readthedocs.io/en/5.6/user_guide/data_loading_and_saving.html)
- Schaap resamples all centerlines equidistantly at 0.03 mm "enabling an accurate comparison". — [Schaap 2009](https://cdr.lib.unc.edu/downloads/cn69mc016)
- In a sensitivity analysis of curvature/torsion-based vessel landmarking (Piccinelli and Bogunović algorithms, internal carotid), centerline *resolution* was the parameter that most strongly over- or under-segmented bends, and smoothing had the least impact. The authors also note missing documentation of the input parameters for curvature/torsion estimation. — [BioMed Eng OnLine 2021, doi:10.1186/s12938-021-00957-6](https://dx.doi.org/10.1186/s12938-021-00957-6); [MorphMan docs](https://morphman.readthedocs.io/en/stable/Miscellaneous.html)
- In a retinal cross-device study, curvature-based tortuosity had the widest ICC intervals because "curvature is not scale invariant". The distance-based tortuosity index was more stable across devices. This is a preprint. — [arXiv:2602.08580](https://arxiv.org/pdf/2602.08580)
- Wolterink's tracker samples 3D volumes at isotropic 0.5 mm patches with a radius-dependent step size, so raw tracker centerline spacing is not uniform. — [Wolterink 2019](https://arxiv.org/pdf/1810.03143)

### Inferences
- **Checklist:**
  1. Transform the tracer output (voxel indices in the NIfTI) to world mm with the volume affine.
  2. Convert to LPS to match Medis.
  3. Check visually on at least a few cases by overlaying both on the CT. A sign flip in x/y is the classic bug, and NIfTI headers usually describe RAS-like frames (inference; check against the actual header).
  4. Resample both lines by arc length: about 0.03–0.1 mm for correspondence, and a fixed spacing (e.g. 0.5 mm) for features.
  5. Apply the same smoothing or scale (the 5 mm scale of T_5) to *both* tracer and Medis lines before computing curvature. Otherwise, sampling-density differences between the two methods create curvature differences on their own.

## 7. Validating centerline-derived geometric features between methods

### Takeaway
I found no peer-reviewed head-to-head CCTA software comparison of coronary curvature or tortuosity. The closest precedent is in the carotid: de Vries 2019 compared 4 packages using ICC and Bland–Altman. Coronary bifurcation-angle reproducibility on CT has been studied with phantoms and inter-observer designs.

The established way to report feature agreement is ICC (with type stated) plus Bland–Altman bias and 95% limits of agreement, on a matched stretch.

### Cited findings
- **de Vries EE, Pourier VEC, van Laarhoven CJHCM, Vonken EJ, van Herwaarden JA, de Borst GJ.** "Comparability of semiautomatic tortuosity measurements in the carotid artery." *Neuroradiology* 2019;61(2):147–153. doi:10.1007/s00234-018-2112-3. — [PMC6348067](https://pmc.ncbi.nlm.nih.gov/articles/PMC6348067/)
  - **Design:** CTA in 12 patients; 2 observers × 2 rounds; packages 3mensio, TeraRecon, Vitrea and OsiriX.
  - **Metric:** tortuosity index = centerline length divided by straight-line distance.
  - **Agreement statistics:** ICC (two-way mixed, consistency) and Bland–Altman.
  - **Results:**
    - inter-observer ICC ranged from 0.72 (TeraRecon) to 0.99 (3mensio);
    - between-package ICC was 0.95–0.99.
  - **Limitations:** n = 12, and fixed anatomical start and end points.
- Coronary bifurcation angle on CT:
  - A cylinder-fitting method on 64-slice CT (Craiem et al. 2009) reported an inter-observer mean difference of 1.8 ± 5.8° (N = 135) and a phantom error of 0.44 ± 0.54°. — [Cardiovasc Eng 2009, doi:10.1007/s10558-009-9084-1](https://link.springer.com/article/10.1007/s10558-009-9084-1)
  - A phantom study found good correlation with true angles, but MPR and volume rendering differed by about 12° in clinical images. — [UM phantom study](https://knova.um.edu.my/research_publications_2016_2020/3460)
- Wolterink reported automatic vs reference *radius* agreement with Bland–Altman (95% LoA within about one voxel). This is a template for continuous centerline-derived quantities. — [Wolterink 2019](https://arxiv.org/pdf/1810.03143)

### Inferences
- For length, T_5 curvature, LM bifurcation angle and diameter ratios, report per feature:
  - Bland–Altman bias and 95% LoA, with proportional bias checked;
  - ICC(2,1) or ICC(A,1) for absolute agreement, with CI;
  - n and the number excluded because of failed correspondence.
- Do this on the common stretch and with identical smoothing.
- **The key interpretation (not sourced; reasoning):**
  - This validation shows the features are reproducible across methods. It does not show they are correct.
  - Because the Medis cases are almost all plaque-at-baseline patients, agreement may not transfer to the plaque-free outcome cohort.
- Bifurcation angle depends on how the branch direction vectors are defined (the distance from the bifurcation over which tangents are fitted). Fix that length and use it identically for both methods.

### Gaps
- No coronary-specific inter-software curvature or tortuosity agreement study was found in this session.
- Pflederer et al. (Invest Radiol 2006, coronary bifurcation angle by MDCT) is remembered but was not verified; check before citing.
- Medrano-Gracia et al. (coronary atlas, bifurcation angles) is remembered but was not verified; check before citing.
- Literature on curvature-scale dependence specific to coronary CCTA was not found. The evidence above is carotid, cerebral and retinal.
