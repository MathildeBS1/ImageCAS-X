# Quality control and selection of coronary centerline trees before geometric feature extraction (LM, LAD, LCx, RCA)

Research date: 2026-10-20. About 17 tool calls. The primary full text of Schaap et al. 2009 (CAT08) was not read; its metric definitions below come from Wolterink et al. 2019, a peer-reviewed paper that restates them in its own words.

## 1. How benchmark/evaluation frameworks measure centerline correctness, and their tolerances

### Takeaway
The de facto standard is CAT08's point-correspondence scheme. An extracted point counts as correct if it lies **within the local reference lumen radius** of the reference centerline. On that basis CAT08 reports overall overlap (OV), overlap until first error (OF), overlap restricted to the clinically relevant part (OT, radius ≥ 0.75 mm, i.e. diameter ≥ 1.5 mm) and average inside accuracy (AI, mm). Later tree-level work (Hampe 2024) keeps the radius tolerance at node level and reports F1. Segmentation challenges (ASOCA, ImageCAS) mostly score masks with Dice and HD95 rather than centerlines. ImageCAS-X (2026) adds clDice, ASSD and Betti errors.

### Cited Findings
- **CAT08 reference database**: Schaap et al., "Standardized evaluation methodology and reference database for evaluating coronary artery centerline extraction algorithms", *Medical Image Analysis* 13(5):701–714, 2009, DOI 10.1016/j.media.2009.06.003. It contains 32 CCTA datasets with consensus reference centerlines built from multiple observers, and compares 13 algorithms. — [RUG record](https://research.rug.nl/en/publications/standardized-evaluation-methodology-and-reference-database-for-ev/)
- CAT08 annotations: in each scan, three experts annotated the centerline **and radius** of four major vessels (RCA, LAD, LCx, plus a fourth side branch) in a consensus reading. The split is 8 training scans and 24 test scans. Mean voxel size is 0.32 × 0.32 × 0.4 mm³. — [Wolterink et al. 2019, Med Image Anal, DOI 10.1016/j.media.2018.10.005 / arXiv 1810.03143](https://arxiv.org/abs/1810.03143)
- Metric definitions as restated by Wolterink et al. 2019 — [arXiv 1810.03143](https://arxiv.org/abs/1810.03143):
  - "Total overlap (OV), overlap until first error (OF), and overlap of the extracted centerline with the clinically relevant part of the vessel (radius ≥ 0.75 mm, OT) are computed using TP, FP and FN detections."
  - "A TP point lies within the radius of the closest reference point, a FP point does not lie within the radius of any reference point and a FN point is a reference centerline point for which there is no corresponding automatically extracted point."
  - "AI measures the average distance between the reference and extracted centerline for automatically extracted points that are within the radius of the reference centerline", so AI is partly independent of overlap.
- Typical good performance on CAT08 (Wolterink CNN tracker): test-set OV 93.7%, OF 81.5%, AI ≈ 0.21 mm. Training leave-one-out OV is 95.7%, OF 87.1%, OT 97.1%. OV falls to 86.7% in scans rated "poor" image quality. — [arXiv 1810.03143](https://arxiv.org/abs/1810.03143)
- The OF vs OV gap is informative: OF stops counting at the first error, so it penalises early derailment (e.g. near the ostium or at a calcification). — [arXiv 1810.03143](https://arxiv.org/abs/1810.03143)
- **Tracking termination as an inbuilt QC signal**: the tracker stops when the normalised entropy of the direction posterior exceeds θH = 0.9, as a moving average. High entropy occurs at the ostium and at the distal end, and also at stepping artefacts. — [arXiv 1810.03143](https://arxiv.org/abs/1810.03143)
- **orCaScore (MICCAI 2014)** used for fully automatic tree evaluation, scored segment by segment ([arXiv 1810.03143](https://arxiv.org/abs/1810.03143)):
  - Data: 36 scans from GE and Toshiba scanners.
  - Ostium detection succeeded in 36/36 scans, with an error of 1.8 ± 1.0 mm.
  - An observer scored each of 16 clinically relevant segments (Hamdan et al. 2011) as *identified / missed / not visualised*.
  - On average 92% of visualised segments were identified. All segments were found in 16 of 36 scans, the worst scan had 10 of 15, and there were 1.17 false-negative segments per scan.
- **Hampe et al. 2024 tree-level metric** ([J Med Imaging 11(3):034001, DOI 10.1117/1.JMI.11.3.034001, PMC11095121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)):
  - Trees are resampled to 0.25 mm spacing.
  - A node is TP if it lies within the reference artery radius at that location.
  - F1 = 2TP/(2TP+FP+FN). Tree extraction F1 was 0.85 and extraction plus labelling was 0.74 (macro F1).
- **ASOCA** (Gharleghi et al., *Comput Med Imaging Graph* 2022): the first challenge on fully automatic segmentation of whole coronary trees in normal and diseased arteries. It is evaluated with Dice and 95% Hausdorff distance, not centerline overlap. Later users add clDice. — [ASOCA site](https://asoca.grand-challenge.org/); [citation policy](https://asoca.grand-challenge.org/CitationPolicy/)
- **ImageCAS** (Zeng et al. 2023), 1,000 CCTA scans with lumen masks ([arXiv 2211.01607](https://arxiv.org/html/2211.01607v2)):
  - Two radiologists label each scan independently and cross-check, and a third resolves disagreements.
  - Some secondary papers say three radiologists instead ([arXiv 2311.13100](https://arxiv.org/pdf/2311.13100)), so sources disagree.
- **ImageCAS-X** (Bransby, Øksnebjerg, Kjær, …, Kofoed, Paulsen; DTU Compute & Rigshospitalet; arXiv 2608.30404, posted 31 Aug 2026). This is directly relevant to this thesis's data. — [arXiv 2608.30404](https://arxiv.org/html/2608.30404v1)
  - **Annotations:** re-annotated lumen masks for 800 ImageCAS scans. Centerlines (VTK) carry per-vertex start, bifurcation and end flags and a per-vertex segment label. There are 14 segment classes based on the 18-segment model, including "Other" for extra D/OM branches. Each scan also has dominance, disease status and an image-quality grade.
  - **Ostium proxy:** centerline start points are vertices within 5 mm of the aorta, which is segmented with TotalSegmentator.
  - **Inter-observer test set (160 scans):** clDice 95.4, ASSD 0.53 mm, HD95 4.58 mm. **No explicit pass/fail threshold for centerline quality is stated.**
  - **Original ImageCAS labels vs the new reference:** DSC 41.8, HD95 16.15 mm, Betti error 7.0, centerline clDice 78.2. Failure examples include plaque inside the lumen, false-positive pulmonary vessels and false-positive coronary veins.
- Community add-on: a Zenodo release ("Awakening ImageCAS") provides ostium and centerline annotations for all 1,000 ImageCAS scans. Not independently verified. — [Zenodo 23243094](https://zenodo.org/records/23243094)

### Inferences
- A defensible automatic tolerance for "the centerline is in the lumen" is **distance to reference or lumen-surface centre ≤ local radius**, which is the CAT08 rule. Without a reference, the analogue is that each centerline point must lie inside the segmentation mask, and its distance to the mask boundary should be consistent with the stored radius.
- The OT convention (radius ≥ 0.75 mm, i.e. diameter ≥ 1.5 mm) is a well-established lower size limit for "clinically relevant" vessel. It also matches the van Zandwijk exclusion of segments under 1.5 mm mean diameter (Section 2).
- If the 744 trees derive from ImageCAS-X-style processing, scan-level image-quality grade and dominance may already exist and should be used directly as QC covariates.

### Gaps
- Primary Schaap 2009 text not read: exact OF/OT handling of the distal end and the score/rank normalisation are not verified here.
- **CCA-200 and ARCADE**: no results found in this session. ARCADE is an X-ray (invasive angiography) dataset per general knowledge, not verified here.
- The ASOCA paper's full metric list beyond Dice and HD95 was not verified.

## 2. QC and exclusion criteria used in coronary geometry, plaque and CFD studies

### Takeaway
Geometry studies typically exclude patients with **prior PCI/stent or CABG** and **coronary anomalies**. They exclude **arteries or segments with non-diagnostic image quality** (motion, step artefacts, metal) and **segments under 1.5 mm mean diameter**. They also drop segments where the **centerline is incorrect** after manual CPR review. Exclusion rates at artery or segment level can be very high: in one study 36% of arteries and 29% of segments were dropped. Many studies under-report how centerlines were checked.

### Cited Findings
- **van Zandwijk et al., *J Digit Imaging* 33(2):480–489, 2020** (curvature/tortuosity vs CAD, 71 patients) — [PMC7165136](https://pmc.ncbi.nlm.nih.gov/articles/PMC7165136/)
  - **Patient-level exclusion:** prior heart surgery or PCI, and coronary anomaly on CCTA.
  - **Phase selection:** if the automatic ES/ED phase was poor, a phase within ±2 phases could be chosen. **Arteries were excluded if no phase gave adequate quality.**
  - **Segment-level exclusion:** mean diameter < 1.5 mm, artefacts, **incorrect centerline**, or not visible. **An artery was excluded if any of its segments could not be assessed.**
  - **Effect:** 137/213 arteries (64.3%) and 456/639 segments (71.4%) were retained.
  - **Centerline handling:** automatic extraction (TeraRecon Aquarius iNtuition 4.4.11) followed by CPR review. Centerlines were **manually adjusted where they did not follow the lumen centre**, and segment start and end markers were placed manually.
  - **Known weakness:** the authors note extraction was often inaccurate in severely diseased arteries.
  - **Segments:** 15-segment modified AHA. RCA has proximal, mid and distal segments. The "LAD" path covers LM plus proximal, mid and distal LAD. LCx has proximal and distal segments. **Where no side branch marked a segment end, equal pre-set lengths were used.**
  - **Feature definitions:** curvature by Menger's formula sampled every 5 mm and averaged (mm⁻¹). Tortuosity = path length divided by the straight-line end-to-end distance. Inflection points counted on a rotated CPR.
  - **Related finding:** an earlier 73-patient CCTA study (same group) linked curvature to plaque at segment and artery level, and curvature was ~16.7% higher in >70% stenosed segments. — [search summary of JDI 2019 / UMC Utrecht record](https://researchinformation.umcutrecht.nl/en/publications/non-invasive-assessment-of-coronary-artery-geometry-using-coronar/) (secondary; numbers not verified in full text)
- **Moon et al., *Quant Imaging Med Surg* 13(11):7459–7466, 2023** (pLAD tortuosity and LM–LAD angle vs pLAD stenosis, 133 patients) — [PMC10644144](https://pmc.ncbi.nlm.nih.gov/articles/PMC10644144)
  - **Only exclusion:** prior CABG or PCI.
  - **Tortuosity:** computed over a **fixed 20 mm from the LAD ostium** as path length divided by chord length (d20), on TeraRecon centerlines.
  - **LM–LAD angle:** measured manually on 3D VR and axial images.
  - **Reporting gaps:** no centerline QC, minimum diameter or screening and exclusion numbers reported. This is an example of under-reporting.
- **Han, Lin et al., *JAMA Cardiology* 7(3):309–319, 2022** (vessel geometry and plaque location vs future ACS culprit) — [JAMA Cardiol](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
  - **Geometry definitions:** distance from ostium (short = < 39 mm left, < 60 mm right). Bifurcation = side-branch origin within the lesion. Tortuosity = ≥1 bend > 90° or ≥3 curves of 45–90° by a 3-point angle.
  - **Measurement and readers:** Autoplaque 2.5 for geometry and MEDIS QAngio CT 2.1.9.1 for plaque. Two level-III readers, with **repeat angle measurement in 30 random lesions giving ICC 0.91**.
  - **Exclusions:** 118 of 234 patients were excluded, including 12 culprits "not measurable due to artifact or small vessel size". Segments ≥ 2 mm were evaluated under the SCCT 18-segment model.
- **Hampe et al. 2024** (104 scans used) — [PMC11095121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
  - **Scan exclusions:** 14 scans were excluded **for imaging artefacts**: step-and-shoot 8, motion 3, metal implants 2, incomplete FOV 1.
  - **Reference centerlines:** semi-automatically tracked, overlaps removed automatically, then manually inspected and corrected. Ostia were CNN-detected and manually corrected.
- **ImageCAS-X**: 200 of 1,000 ImageCAS scans were removed *before annotation* for image quality. Reasons were motion 114, step artefacts 76, poor contrast mixing 7, static noise 1, incorrect FOV 1 and file corruption 1, i.e. 20% excluded. Side branches with distal diameter < 1 mm were not traced (labelling rule). — [arXiv 2608.30404](https://arxiv.org/html/2608.30404v1)
- **UMCU dataset quality profile (50 scans)**, for context on how common the issues are: stents 2/50, step artefacts 7/50, motion artefacts 11/50. Expert marker radii ranged 0.45–3.51 mm, median 0.81 mm. — [arXiv 1810.03143](https://arxiv.org/abs/1810.03143)
- **CCTA WSS studies:**
  - They report ESS per 3 mm segment from dedicated software — [PMC10017098](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10017098/).
  - Low WSS is linked to progression of plaque area (P = 0.027) and necrotic core (P < 0.001) — [Samady et al., Circulation 2011](https://www.ahajournals.org/doi/10.1161/circulationaha.111.021824).
  - Exclusion details for these studies were not extracted in this session.

### Inferences
- A literature-consistent selection rule set for this thesis:
  - **Patient level:** exclude prior PCI/stent or CABG. CGPS has `ct_cag_*` stent and CABG flags; check BL/FU availability in the headers.
  - **Patient level:** exclude coronary anomalies.
  - **Image quality:** exclude non-diagnostic quality. BL has `bad_quality` and `scan_qualitative_quality`.
  - **Artery level:** exclude if any trunk segment is non-evaluable. BL has `ct_cag_<segment>_eval`.
  - **Segment level:** exclude where mean radius < 0.75 mm (diameter < 1.5 mm).
  - **Centerline check:** exclude if the centerline leaves the lumen, judged by an automatic check or visual CPR review.
- The "exclude the whole artery if any segment fails" rule from van Zandwijk removes many arteries. For per-trunk models (LAD/CX/RCA separately), a softer rule is to exclude only the failing segment. The cost is that whole-vessel features then become non-comparable. Use fixed-length windows instead (e.g. the 20 mm from-ostium window in Moon et al.).
- Fixed-length or ostium-referenced windows reduce dependence on distal tracking depth, a major source of variable trunk length in automatic trees. Tortuosity and mean curvature depend on the length analysed.

### Gaps
- No HeartFlow FFR-CT, Siemens syngo, Philips or Medis-specific QC protocol details were retrieved (vendor processing is usually proprietary; HeartFlow uses analyst review per general knowledge, not verified here).
- No peer-reviewed source was found giving a numeric minimum trunk length (in mm) as an exclusion threshold.
- The CLAP score study (JCDD 2024, DOI 10.3390/jcdd11110338; LM bifurcation angle > 80° as predictor, 499/650 included) was seen only as a snippet. Its first exclusion was poor image quality. Its full exclusion list and angle method were not read. — [PMC11595042](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11595042/)
- The 2017 PLoS ONE dual-source study (LAD–LCx angle OR 1.423 for ≥50% stenosis) was seen only as a snippet; its exclusion criteria were not read. — [PMC5367806](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5367806/)

## 3. Segment labelling (SCCT/AHA), label-quality checks, dominance and proximal/mid/distal boundaries

### Takeaway
SCCT 2014 (Leipsic et al.) defines the 18-segment model with side-branch landmarks. LM runs from the ostium to the LAD/LCx bifurcation, and pLAD runs from the end of the LM to the first large septal or D1 (> 1.5 mm), whichever is more proximal. Automatic labellers (GCN/GAT/GraphSAGE) label branch-level classes reliably for the main trunks but struggle with rare, dominance-dependent classes (L-PDA, L-PLB, R-PDA vs R-PLB, ramus). Several methods do **not** subdivide trunks into proximal/mid/distal, because the landmarks are not topologically defined. Label quality is reported as (weighted or macro) F1 against expert consensus labels. Inter-rater agreement is rarely reported.

### Cited Findings
- **SCCT guideline**: Leipsic et al., "SCCT guidelines for the interpretation and reporting of coronary CT angiography", *J Cardiovasc Comput Tomogr* 8(5):342–358, 2014, DOI 10.1016/j.jcct.2014.07.003. Full text not read. — [record](https://www.cardiologicomonzino.it/en/scientific-papers/2014/10/15/scct-guidelines-for-the-interpretation-and-reporting-of-coronary-ct-an/954/)
- 2024 ASCI-PT consensus (Korean J Radiol), which builds on SCCT 2014:
  - LM is "Ostium of LM to bifurcation of LAD and LCX".
  - Proximal LAD is "End of LM to the first large septal or D1 (D1 > 1.5-mm in size) whichever is most proximal, even though proximal LAD is extremely short".
  - Source: [PMC10973734](https://pmc.ncbi.nlm.nih.gov/articles/PMC10973734) ([table T4](https://pmc.ncbi.nlm.nih.gov/articles/PMC10973734/table/T4))
- **Hampe et al. 2024** — [PMC11095121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
  - **Classes:** 10 AHA-based classes: LM, LAD, LCX, RCA, D, S, OM, AM, R-PDA, R-PLB.
  - **No proximal/mid/distal split:** subdividing the trunks "would need landmarks that don't follow from tree topology".
  - **Dominance:** left-dominant cases were scarce, so **L-PDA was merged into LCX and L-PLB into OM**.
  - **Coronary vs non-coronary:** the tracker deliberately overshoots into veins and other structures, and a GCN classifies segments as coronary or not.
  - **Failure modes:**
    - septal branches missed (F1 0.54)
    - tracking past the ostium into the aorta, which caused the LM to be discarded
    - R-PDA vs R-PLB confusion
    - **calcification gaps disconnecting LCx from LM**
    - **vein leakage into arteries**
    - gaps degrading labelling
- **Li, Armin, Denman, Ahmedt-Aristizabal (arXiv 2212.00386, Dec 2022)** — [ar5iv](https://ar5iv.labs.arxiv.org/html/2212.00386)
  - **Classes:** 13 SCCT classes. Left: LM, LAD, LCX, R (ramus), S, OM, D, L-PLB, L-PDA. Right: RCA, AM, R-PLB, R-PDA.
  - **Data and ground truth:** 141 patients. Two experts labelled each branch, then three experts voted on the final labels. No inter-rater statistic is reported.
  - **Performance:** GraphSAGE weighted F1 0.805 (13 classes). Rare classes R, L-PDA and R-PDA were poor, and the authors say experts also find them difficult.
  - **Input sensitivity:** inconsistent centerline start points reduce accuracy, which motivated standardised graph construction (origin at the first LM point).
- A GAT method on 71 CCTA scans reported F1 92.4% (venue and year not confirmed). — [SPIE profile listing](https://opticalengineering.spiedigitallibrary.org/profile/Nils.Hampe-4270570)
- **ImageCAS-X**: 14 classes on the 18-segment scheme, with an "Other" class for extra D/OM. **The lead analyst manually reviewed and corrected segment assignments.** Dominance is stored per scan. — [arXiv 2608.30404](https://arxiv.org/html/2608.30404v1)
- In van Zandwijk et al., segment boundaries were placed manually at side-branch landmarks. When no side branch was present, equal pre-set lengths were used. — [PMC7165136](https://pmc.ncbi.nlm.nih.gov/articles/PMC7165136/)

### Inferences
- **Dominance in the user's labels:** "L-PDA/L-PLB" vs "R-PDA/R-PLB" labels encode dominance. An internal consistency check is that a tree should not contain both L-PDA and R-PDA, unless it is co-dominant. Cross-check against the CGPS `ct_cag_dominance` read, available in BL/FU per the headers.
- **"LCx" label:** the user's tree labels "LCx" separately from pCx. This is likely the mid/distal Cx (SCCT segment 13 or similar), which should be confirmed. The CX trunk is then pCx + LCx up to the L-PLB/L-PDA origin.
- **Merging into trunks:** because automatic proximal/mid/distal boundaries are unreliable, merging p/m/d into one trunk per vessel (LAD = pLAD+mLAD+dLAD, RCA = pRCA+mRCA+dRCA) is consistent with Hampe 2024. Positions are then expressed as arc length from the ostium. This fits the user's "full segment = vessel" usage.
- **Label sanity checks** follow from the definitions:
  - LM must start at the aorta (within about 5 mm, per the ImageCAS-X convention).
  - LM must bifurcate into LAD and Cx (or trifurcate with RI).
  - The labels along each trunk must be ordered p → m → d.
  - No trunk label should appear in the wrong side tree.

### Gaps
- Full SCCT 2014 text with exact mid/distal LAD, mid RCA and Cx boundary definitions was not retrieved.
- No study was found that quantifies the agreement of automatic labels with CT-read segment-level findings (e.g. matching labels to `ct_cag_<segment>` columns).
- The meaning of "unnamed codes" and "unlabelled" in the user's trees could not be resolved from the literature.

## 4. Automated anomaly checks on centerline trees; tiered visual QC; inter-observer review

### Takeaway
The literature documents the failure modes to check for:
- leakage into veins, pulmonary vessels or the aorta
- gaps at heavy calcification or occlusion
- derailment near the ostium
- deviation from the lumen centre in diseased segments
- spurious extra branches
- step and motion artefacts producing jumps or entropy spikes

Most pipelines combine automatic pruning or classification with a **single expert's manual review and correction**, assessed on a held-out inter-observer subset. Formal 3-point QC grading of centerlines and explicit numeric anomaly thresholds are rarely published.

### Cited Findings
- **Failure modes in automatic trees** (Hampe 2024): vein leakage, tracking into the aorta past the ostium, calcification gaps disconnecting LCx from LM, and missed small septals. Remedy: a learned coronary-vs-non-coronary classifier plus manual correction of reference trees. — [PMC11095121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
- **ImageCAS-X manual QC workflow**: analysts trimmed automated centerlines, **removed spurious segments and added missing vessels**. Centerlines were regenerated from corrected masks by skeletonisation plus Gaussian smoothing. The lead analyst reviewed all cases for lumen errors and corrected labels. Inter-observer agreement was assessed on a 160-scan test set (clDice 95.4, ASSD 0.53 mm, HD95 4.58 mm). The original ImageCAS masks included plaque, pulmonary vessels and coronary veins, and had a Betti-number error of 7.0, a topology check. — [arXiv 2608.30404](https://arxiv.org/html/2608.30404v1)
- **Entropy-based termination** (Wolterink 2019): high direction uncertainty flags the ostium, the vessel end and stepping artefacts. These can serve as point-wise uncertainty for QC. — [arXiv 1810.03143](https://arxiv.org/abs/1810.03143)
- **Lumen deviation:** centerlines in severely diseased arteries often failed to follow the lumen and needed manual CPR-based correction. — [van Zandwijk 2020, PMC7165136](https://pmc.ncbi.nlm.nih.gov/articles/PMC7165136/)
- **Visual segment scoring** (orCaScore evaluation): each of 16 segments scored as identified / missed / not visualised. This 3-category scheme is a reusable visual QC rubric. — [arXiv 1810.03143](https://arxiv.org/abs/1810.03143)
- **Repeatability:** repeat measurement on a random subset (30 lesions, two readers, ICC 0.91 for angles) — [Han 2022 JAMA Cardiol](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006).
- **Radius plausibility:** automatic radius estimates had limits of agreement below one voxel vs reference in CAT08 and UMCU. Reference radii in UMCU ranged 0.45–3.51 mm. — [arXiv 1810.03143](https://arxiv.org/abs/1810.03143)

### Inferences
Automatic checks derived from the failure modes above. The thresholds are suggestions, not literature-validated.

1. **Topology**
   - Each side tree should be one connected component. On the left, LM is the root at the aorta (start within about 5 mm of the aorta surface) and branches to LAD and Cx. On the right, pRCA is the root.
   - No cycles. Betti-1 = 0 for a tree; ImageCAS-X uses Betti error as a metric.
2. **Ostium**
   - The first point of the LM/pRCA should be near the aortic wall.
   - Points inside the aorta mean tracking overshot (Hampe failure mode).
3. **Gaps and jumps**
   - Consecutive point spacing should be near the nominal resampling step (e.g. 0.25 mm in Hampe).
   - Steps far larger than the step size, or larger than the local radius, flag gaps or jumps. These often occur at calcification or step artefacts.
4. **Leakage into veins or other vessels**
   - Flag implausible radius jumps or monotonic distal radius increase (veins widen distally while arteries taper).
   - Flag branches leaving the expected region, or a trunk length far above the cohort distribution.
5. **Radius outliers**
   - Compare against the plausible coronary range: about 0.45–3.5 mm radius per the UMCU markers.
   - Use the OT/1.5 mm-diameter rule for the distal cut-off.
   - Also flag non-tapering trunks.
6. **Smoothness and self-intersection**
   - Spikes in discrete curvature, especially those that exceed 1/r (bending radius tighter than the lumen radius), signal jitter or a centerline leaving the lumen.
   - ImageCAS-X smoothed skeletons with a Gaussian, so the smoothing scale affects curvature features and must be fixed and reported.
7. **Label consistency**
   - Proximal-to-distal label order along each trunk.
   - Dominance consistency (Section 3).
   - Required trunks present: LM, LAD, Cx, RCA.
8. **Tiered visual QC**
   - Grade every tree, or a stratified random subset plus all automatically flagged trees, on CPR or 3D overlay with a 3-level rubric. Examples: accept / accept with segment exclusions / reject; or identified / missed / not visualised per trunk.
   - Have a second reader grade a random subset and report kappa.

### Gaps
- No peer-reviewed numeric thresholds were found for gap size, jump distance, curvature spikes or radius ratios as QC rules. These must be set empirically, e.g. from cohort percentiles, and reported as analysis choices.
- No published 3-point centerline QC grading scale for geometry studies was found. The orCaScore identified/missed/not-visualised rubric is the closest analogue.

## 5. Proportion of exclusions and selection-bias reporting

### Takeaway
Reported exclusion fractions vary widely. Because most CCTA geometry studies do not report how many centerlines failed QC, a **flow diagram** and a comparison of included vs excluded patients are needed to address selection bias.

| Study | Unit | Excluded / dropped | Retained | Main reasons |
|---|---|---|---|---|
| ImageCAS-X | scans, before annotation | 20% | 800 / 1,000 | Image quality, mainly motion and step artefacts |
| Hampe 2024 | scans | about 12% | 104 / 118 | Artefacts |
| van Zandwijk 2020 | arteries | 36% | 64.3% | Image quality, incorrect centerlines, small or non-visible segments |
| van Zandwijk 2020 | segments | 29% | 71.4% | Same as above |
| Han 2022 | patients | 50% | 116 / 234 | Mostly adjudication reasons |
| Moon 2023 | patients | not reported | 133 | Not reported |

### Cited Findings
- ImageCAS-X: 200/1,000 (20%) excluded for image quality before annotation, with reasons itemised — [arXiv 2608.30404](https://arxiv.org/html/2608.30404v1)
- Hampe 2024: 14 scans excluded for artefacts, 104 used, i.e. 14/118 ≈ 12% if 118 was the source cohort (derived) — [PMC11095121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
- van Zandwijk 2020: 35.7% of arteries and 28.6% of segments excluded (derived from 137/213 and 456/639) — [PMC7165136](https://pmc.ncbi.nlm.nih.gov/articles/PMC7165136/)
- Han 2022: 118/234 excluded with itemised reasons, including 12 for artefact or small vessel size — [JAMA Cardiol](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
- CLAP 2024: 499/650 included (23% excluded) — [PMC11595042](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11595042/)
- Moon 2023: screening and exclusion numbers not reported — [PMC10644144](https://pmc.ncbi.nlm.nih.gov/articles/PMC10644144)

### Inferences
- Exclusion for motion or step artefacts and for disease-related centerline failure, which affects severely diseased arteries, is likely **non-random with respect to the outcome**. Higher heart rate, obesity and higher calcium are associated with both poor image quality and atherosclerosis.
- For a 10-year new-plaque outcome, the cohort is restricted to plaque-free trunks at BL, which reduces disease-related centerline failure. Image-quality exclusions remain a concern.
- **Recommended reporting**, in line with the STROBE/TRIPOD style:
  - A flow diagram from all patients to those with CT, those with a tree, those passing QC per trunk (LAD/CX/RCA separately) and those with FU.
  - A table comparing included vs excluded patients on `scan_age`, `male`, BMI, heart rate, `ct_cacs_sum` and `bad_quality`.
  - Optionally inverse-probability-of-inclusion weights as a sensitivity analysis.

### Gaps
- No peer-reviewed source was retrieved that explicitly analyses selection bias from centerline QC exclusions in CCTA geometry studies.
- Typical failure rates of fully automatic trunk extraction in large population cohorts (as opposed to curated research sets) were not found.
