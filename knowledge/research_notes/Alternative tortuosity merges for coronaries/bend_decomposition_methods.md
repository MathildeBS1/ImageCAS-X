# 3D bend decomposition methods for vessel centerlines (replacement for the Grisan-style twist detector)

Evidence levels. **Full text** = read in full or in the relevant section during this pass (Bullitt 2003 via PMC2430603; Kjeldsberg 2021 via PMC8626959; Sangalli 2009 JRSS-C preprint PDF; Thomas 2005 PDF; morphMan and VMTK source code). **Abstract-only** = abstract or search snippet only (Bogunović 2012, Piccinelli 2009, O'Flynn 2007, Vorobtsova 2016, Ferrari 2025, Kashyap 2022 abstract here, but read in full by the earlier pass). **Derivation** = reasoning by this researcher, not stated by any source.

Correction to the brief: O'Flynn et al. 2007 is not a carotid paper. It characterises aortic, renal and iliac branches from MRA in 3 subjects (see Q1 findings). Thomas et al. 2005 is the carotid-bifurcation paper.

## Q1. Which bend detector is most stable to noise and resolution, and has code?

### Takeaway
Bogunović's detector (angle between curvature vectors at consecutive curvature maxima, expressed in a parallel-transport frame) is the only 3D bend detector with a head-to-head stability comparison, and it beat Piccinelli's torsion-extrema detector clearly (superior bend CV < 5 % vs 47 %). Both are implemented in open code (morphMan, GPL-3.0, on top of VMTK), but the morphMan Bogunović implementation is hard-wired to the four-bend carotid siphon, so for coronaries only its core (parallel-transport curvature-vector angle) is reusable. A derivation below explains why it is more stable: it works at second-derivative order, whereas torsion extrema need third derivatives.

### Cited Findings

**Bullitt et al. 2003, IEEE TMI 22(9):1163-1171 (full text, PMC author manuscript), §II-D**
- Input: ordered 3D skeleton points "regularly sampled at intervals of the length of one voxel". The authors chose one-voxel sampling because sub-voxel sampling adds noise, and justify it with Koenderink: a chord shorter than half the radius of curvature misestimates arc length by at most 1 % (§II-B, Discussion). — [Bullitt 2003, PMC2430603](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- **DM** = path length / chord (dimensionless, §II-D-1). — [Bullitt 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- **ICM, 3D inflection definition (§II-D-2):** "an inflection point [is] a locus that exhibits a minimum of total curvature ... the Normal and Binormal axes of the Frenet frame change orientation by close to 180°". Frenet frame is geometric: V ≈ P_{k+1} − P_{k−1}; A ≈ T2 − T1; N = normalise((V × A) × V). If |A| < 10⁻⁶ cm the point is skipped and the frame is redefined at the next point. On a synthetic sine wave, ΔN·ΔN ≈ 4.0 at inflections, 10⁻² to 10⁻⁸ elsewhere, and ≈ 0.01 at the extrema. **Detection rule: local maxima of ΔN·ΔN with ΔN·ΔN > 1.0.** ICM = (n_inflections + 1) × DM, so "both a straight line and a coil are ... reported as having inflection counts of 1". — [Bullitt 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- **SOAM (§II-D-3), exact formula.** T1 = P_k − P_{k−1}, T2 = P_{k+1} − P_k, T3 = P_{k+2} − P_{k+1}. In-plane angle IP_k = arccos(T̂1·T̂2). Torsional angle TP_k = arccos of the dot product of the unit normals (T1×T2)/|T1×T2| and (T2×T3)/|T2×T3|. Both lie in [0, π]. When the frame crosses an inflection, TP_k is set to 0 instead of 180°. CP_k = √(IP_k² + TP_k²); **SOAM = Σ_{k=1}^{n−3} CP_k / Σ_{k=1}^{n−1} |P_k − P_{k−1}|**, in rad/cm. — [Bullitt 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- **Bullitt Table 2 (synthetic)**, freq / amp / length (cm) / DM / ICM / SOAM:
  - Sine waves at equal length: 3 / 10 / 13.9 / 1.6 / 9.7 / 0.9; 10 / 3 / 13.9 / 1.6 / 32.3 / 3.1; 20 / 1.5 / 13.9 / 1.6 / 64.7 / 6.2.
  - Coils at equal length: 3 / 6.3 / 1.5 / 1.5 / 1.3; 10 / 1.9 / 1.5 / 1.5 / 4.5; 20 / 0.94 / 1.5 / 1.5 / 9.2. **ICM = DM for every coil.**
  - Amplitude series, sine: amplitude 10 → 20 → 40 gives SOAM 0.9 → 0.7 → 0.4. Coil: amplitude 6.3 → 20 → 40 gives SOAM 1.3 → 0.6 → 0.3. **SOAM falls as amplitude rises at fixed frequency.**

  — [Bullitt 2003, Table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- Bullitt's stated failure modes: DM "may assign the same tortuosity value to a large, gentle 'C' curve as to a much more tortuous vessel"; "As coils do not contain inflection points, the ICM does no better than the DM when analyzing coils". — [Bullitt 2003 §II-D](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)

**Piccinelli et al. 2009, IEEE TMI 28(8) (abstract-only; method as restated by Kjeldsberg 2021 and as coded in morphMan)**
- Framework of Voronoi-diagram / minimal-cost-path centerlines with curvature, torsion and tortuosity, released in VMTK. — [PubMed 19447701](https://pubmed.ncbi.nlm.nih.gov/19447701/)
- Bend definition: "a bend for each curvature peak enclosed by a proximal and a distal torsion peak". Kjeldsberg Eq. 3: κ = ‖r′×r″‖/‖r′‖³. Eq. 4: τ = r‴·(r′×r″)/‖r′×r″‖². — [Kjeldsberg 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- morphMan's Piccinelli code smooths torsion with a Gaussian of σ = 25 samples (VMTK route) or 10 samples (spline route), then takes local maxima of |torsion|. It drops curvature maxima within the first or last 10 points. Of any two curvature (or torsion) maxima closer than **70 samples**, it keeps only the larger. These are sample-count parameters, so their physical scale changes with the resampling step. — [morphMan automated_landmarking_piccinelli.py](https://github.com/KVSlab/morphMan/blob/master/src/morphman/automated_landmarking/automated_landmarking_piccinelli.py)

**Bogunović et al. 2012, Med Image Anal 16(4) (abstract-only; method from Kjeldsberg and morphMan)**
- Carotid siphon "modeled as a sequence of four bends". "Bends are detected from the trajectory of the curvature vector expressed in the parallel transport frame of the curve." Geometry then characterised by local and global geometric features and by LDDMCM shape distances. 96 3DRA images. ICA identification succeeded at 99 % in cross-validation. For all but one landmark, either the bias was non-significant or the variability was within 50 % of inter-observer variability. **LDDMCM classified siphon shape classes better than the geometric features did.** — [Europe PMC abstract, doi 10.1016/j.media.2012.01.006](https://doi.org/10.1016/j.media.2012.01.006)
- Kjeldsberg Eq. 6: T′(t) = k₁(t)E₁(t) + k₂(t)E₂(t), with E₁, E₂ the parallel-transport normals. Bends are found from the rotation angle α between curvature-vector projections. Thresholds proximal→distal: **α = 45°, 60°, 45°, 110°**. — [Kjeldsberg 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- Per-bend features (secondary description): for each of the four bends, the curvature, the vessel diameter and the angles between adjacent bends. — [Kjeldsberg 2021 search-snippet summary](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8626959/)
- **Exact algorithm in morphMan (code read):**
  1. Optionally resample the centerline.
  2. Compute VMTK curvature, then Gaussian-filter it with σ = 2 samples.
  3. Take local maxima and minima of curvature. A max/min pair is pruned if the two are within 5 samples and |Δκ| < 0.01.
  4. Express the curvature vector in the (k₁, k₂) basis. E₁ is VMTK's ParallelTransportNormals, Gram-Schmidt-orthogonalised against the Frenet tangent, and E₂ completes the frame. k₁ and k₂ come from κ·N_Frenet = k₁E₁ + k₂E₂.
  5. At each consecutive pair of curvature maxima, compute θ_i = arccos(k̂_i · k̂_{i+1}) (in degrees) between the normalised (k₁, k₂) vectors.
  6. Search outward from the maximum coronal coordinate, where the siphon apex is anatomically expected. At the first θ_i above the bend-specific tolerance (45, 60, 45, 110°), place the interface at the last curvature minimum between those two maxima.

  — [morphMan automated_landmarking_bogunovic.py](https://github.com/KVSlab/morphMan/blob/master/src/morphman/automated_landmarking/automated_landmarking_bogunovic.py); [centerline_operations.get_k1k2_basis](https://github.com/KVSlab/morphMan/blob/master/src/morphman/common/centerline_operations.py)

**Kjeldsberg et al. 2021, BioMed Eng OnLine (full text via PMC; section-level detail partially retrieved)**
- Data: 10 ICA models for sensitivity and comparison; 8 segmentations of one case for robustness; 5 Aneurisk models checked by Bogunović, who judged "10 out of 12" models well landmarked (snippet). — [Kjeldsberg 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- **Piccinelli sensitivity:** resampling step r = 0.02 gave a mean of **33 bends**; r = 0.2 gave **3 bends**. Smoothing λ ∈ [1.2, 1.5] gave 6-7 bends. Iterations N ∈ [20, 100] gave consistent results. — [Kjeldsberg 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- **Bogunović sensitivity:** lowest CV at r = 0.1; λ = 1.1 gave a mean landmarked length of about 60 mm with minimum CV; N ≤ 100 gave low deviation, lowest at N = 20. — [Kjeldsberg 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- **Robustness across 8 segmentations:** Piccinelli superior bend CV = 47 %, posterior and inferior < 20 %. Bogunović superior bend CV < 5 %, low overall. Recommended settings r = 0.1, λ = 1.2, N = 100. Code: GPL-3.0 at github.com/KVSlab/morphMan (Python, on VMTK). — [Kjeldsberg 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- Discrepancy: the earlier pass recorded "Piccinelli CV 47-58 %" and "4 bends with Bogunović". This pass retrieved 47 % for the superior bend and < 20 % for the others. The 58 % figure could not be re-located, so treat 47-58 % as unconfirmed. The "3 to 33 bends" range belongs to **Piccinelli's** detector, not to bend detection in general. — [Kjeldsberg 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)

**VMTK vmtkcenterlinegeometry / vmtkcenterlineattributes (source read)**
- Optional smoothing is iterative Laplacian relaxation: p_j += λ·(½(p_{j−1} + p_{j+1}) − p_j), with default λ (SmoothingFactor) = 0.01 and 100 iterations. λ > 1 in Kjeldsberg means over-relaxation. — [vtkvmtkCenterlineSmoothing.cxx](https://github.com/vmtk/vmtk/blob/master/vtkVmtk/ComputationalGeometry/vtkvmtkCenterlineSmoothing.cxx); [vtkvmtkCenterlineGeometry.cxx](https://github.com/vmtk/vmtk/blob/master/vtkVmtk/ComputationalGeometry/vtkvmtkCenterlineGeometry.cxx)
- Curvature uses 3-point non-uniform finite differences, κ = |x′ × x″| / |x′|³. The length-weighted mean curvature is also returned. **Tortuosity is defined per line as L/D − 1.** Frenet T, N, B are output per point. — [vtkvmtkCenterlineGeometry.cxx](https://github.com/vmtk/vmtk/blob/master/vtkVmtk/ComputationalGeometry/vtkvmtkCenterlineGeometry.cxx)
- Parallel-transport normals (discrete rotation-minimising frame): start from an arbitrary normal perpendicular to the first tangent. At each point, rotate the previous normal by the angle between consecutive unit tangents about the axis t₀ × t₁, re-project it orthogonal to t₁ and normalise. — [vtkvmtkCenterlineAttributesFilter.cxx](https://github.com/vmtk/vmtk/blob/master/vtkVmtk/ComputationalGeometry/vtkvmtkCenterlineAttributesFilter.cxx)

**Sangalli, Secchi, Vantini, Veneziani 2009, JRSS-C 58(3):285-306 (full text preprint)**
- 3D free-knot regression splines. The three coordinates share one knot vector, knots are chosen by a Stein-unbiased-risk selector pSSE = RSS + C·σ̂²·(m + n_k) (eq. 3), and knot search uses a modified Zhou-Shen algorithm. The 65 AneuRisk ICAs used order m = 5 and C = 4; order 5 gives a continuous third derivative, and so a continuous torsion. The authors argue this is more accurate and efficient than local polynomial smoothing (§4-5). — [Sangalli 2009 PDF](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JRSSC_compresso.pdf)
- **Bend delimiter:** "points of approximately zero curvature ... can be taken as delimiters of artery bends or siphons". They use curvature local minima with **κ < 0.0145 mm⁻¹**, i.e. radius of curvature > 68.966 mm, the mean centerline length. Rationale: for an arc of length l on a circle of radius R, chord/arc = (2R/l)·sin(l/2R) (formula partly garbled in the text extraction; this is the standard form), which "is greater than 0.95 when R > l", so near a curvature minimum the curve is treated as locally straight if R exceeds the population mean length (§5). Curvature estimates are "stable with respect to variations of C over a reasonable span", compared at C = 3, 4, 5 (Fig. 8). — [Sangalli 2009 PDF](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JRSSC_compresso.pdf)
- The paper motivates curvature through the Dean number D = (2ρU₀R/µ)^{1/2}·(R/R_curv)^{1/2}, where R is the lumen radius and R_curv the radius of curvature (§2). — [Sangalli 2009 PDF](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JRSSC_compresso.pdf)

**O'Flynn et al. 2007, Ann Biomed Eng 35:1368-1381 (abstract-only)**
- 3D branching parameters and tortuosity from MRA centerlines of **3 subjects**, for the aorta, renal and iliac arteries (not the carotid). Renal mean average curvature was 0.114 ± 0.015 mm⁻¹ (left) and 0.070 ± 0.019 mm⁻¹ (right). No bend detector is described in the abstract. — [PubMed 17431787](https://pubmed.ncbi.nlm.nih.gov/17431787/)

**Thomas et al. 2005, Stroke 36:2450-2456 (full text PDF)**
- Carotid bifurcation MRI, 25 young (24 ± 4 y) vs 25 older (63 ± 10 y) subjects. Tortuosity = **L/D − 1** from origin to branch end; there is no bend decomposition. ICA tortuosity 0.025 ± 0.013 (young) vs 0.086 ± 0.105 (older). Young vessels showed less inter-individual variation. — [Thomas 2005 PDF](https://uwo.scholaris.ca/bitstreams/e9c3d588-e9bb-4ca6-9df3-fb0e81a0e8dc/download)

### Inferences
- **Why Bogunović is stable (derivation, standard frame theory of Bishop 1975; not stated by Kjeldsberg).** In a parallel-transport frame T′ = k₁E₁ + k₂E₂. Here κ = |(k₁, k₂)|, and the polar angle φ of (k₁, k₂) satisfies φ′ = τ wherever κ > 0. So the angle between curvature vectors at two curvature peaks equals ∫τ ds between them, plus a jump of π if κ passes through zero, as at a planar inflection. Bogunović therefore measures *integrated* torsion between peaks, from quantities that need only first and second derivatives (tangent and T′). Piccinelli locates *pointwise* extrema of torsion, a third-derivative quantity. That is one derivative order more noise amplification, plus an extremum search on a noisy signal. This fits the 47 % vs < 5 % CV and the 3 to 33 bend-count swing.
- **Bogunović is the correct generalisation of Grisan's twist.** For a planar curve, (k₁, k₂) moves along a fixed line through the origin, and a sign change of signed curvature is a 180° flip of the curvature vector. That is Grisan's twist exactly, and Bullitt's ΔN·ΔN ≈ 4 event. For a space curve, the PT angle changes continuously, and a threshold α on it gives a graded 3D twist. Bullitt's Frenet-normal flip (> 1.0 on ΔN·ΔN, i.e. |ΔN| > 1, about 60° or more of normal rotation between adjacent samples) is a per-sample test. It is sensitive to sampling step and blind to slow rotation such as a helix. The PT angle accumulated over a whole bend is not.
- Transferable coronary detector (derivation). The morphMan code is ICA-specific: it has four fixed bends, seeds from the coronal coordinate, and uses per-bend tolerances. What transfers:
  1. Resample to a fixed mm step and smooth at a stated scale.
  2. Compute (k₁, k₂) with VMTK-style PT normals.
  3. Take curvature peaks above κ_high.
  4. Merge adjacent peaks unless the PT angle between their curvature vectors exceeds α.
  5. Place boundaries at the lowest-κ point between retained peaks, optionally requiring κ < κ_low there, which is a hysteresis analogue of Grisan and Sangalli.

  Every threshold should be in mm or degrees, never in samples. Sample-count constants (70, 25, 5) are the likely source of Piccinelli's resolution sensitivity.
- Sangalli's rule, a curvature minimum below 1/(mean length), is scale-aware by design. The coronary analogue would be κ < 1/L̄ over the vessel population, with L̄ of order 50-150 mm. That threshold (about 0.007-0.02 mm⁻¹) is at or below the likely noise floor of CCTA curvature (compare van Zandwijk's 0.08 mm⁻¹ at 5 mm in the earlier report). So a pure κ-minimum rule will rarely fire on real coronaries unless smoothing is heavy.

### Gaps
- Bogunović 2012 full text (the exact PT bend algorithm in the paper, its per-bend feature list and formulas, the siphon classes) was not retrievable (ScienceDirect 403). The per-bend feature list comes from a secondary description.
- Piccinelli 2009 full text was not read, so its own smoothing, spline and torsion-peak thresholds are not verified. Only morphMan's re-implementation was seen.
- The units of Kjeldsberg's resampling step r (presumably mm) and the exact table and figure numbers were not confirmed in this pass.
- No study compares 3D bend detectors on coronary centerlines. All stability evidence is from the ICA (3DRA, sub-mm, about 60 mm segments).

## Q2. How can bend-level features be aggregated so the score is radius-aware and does not score helices or C-shapes as 0?

### Takeaway
The zero for helices and C-shapes comes from two separable pieces of Grisan's index: a twist detector that never fires on constant-sign or helical courses, and the (n−1)/n factor that zeroes any single-turn vessel. Replace the detector with a PT-angle split, which cuts a helix into bends every α/τ of arc length, and drop (n−1)/n. Then weight each bend by a dimensionless sharpness such as lumen radius over bend radius (the Dean-number ratio). The published aggregations are sum-of-angles per length (SOAM, κ_a), count × arc/chord (ICM), angiographic counts of bends above an angle, and a per-point HMM class. None is radius-aware. The radius-aware variants below are derivations, not published methods.

### Cited Findings
- **ICM and SOAM behaviour on coils and C-shapes:** ICM gives inflection count 1 for a coil, so ICM = DM (Table 2: 1.5 for all three coils). SOAM ranks coils correctly by frequency (1.3 → 4.5 → 9.2) but *decreases* with amplitude at fixed frequency (1.3 → 0.6 → 0.3). — [Bullitt 2003, Table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- Bullitt's SOAM keeps a torsional angle term TP_k, so helical rotation adds to the score even without inflection. At inflections TP_k is zeroed "because it is confusing to include points with torsional angles of 180° when analyzing a planar curve". — [Bullitt 2003 §II-D-3](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- Bogunović's bend-level features: per-bend curvature, diameter, and angle between adjacent bends. Whole-shape LDDMCM beat these features for shape-class separation. — [Kjeldsberg 2021 description](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/); [Bogunović 2012 abstract](https://doi.org/10.1016/j.media.2012.01.006)
- Dean number D ∝ (R/R_curv)^{1/2}: the flow effect of a bend depends on lumen radius relative to bend radius, not on curvature alone. — [Sangalli 2009 §2](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JRSSC_compresso.pdf)
- **Angiographic bend definitions (2D, projection-dependent):**
  - Most common: ≥ 3 consecutive bends of ≥ 45° change in direction along the main trunk of LAD, LCx or RCA, present in both systole and diastole.
  - Zegers: ≥ 2 segments with ≥ 3 curvatures ≤ 120° in diastole.
  - Eleid: ≥ 2 consecutive curvatures ≥ 180° in a vessel ≥ 2 mm, end-diastole.
  - Estrada: ≥ 3 consecutive bends of < 90° in vessels > 2 mm, diastole.

  — [Zebić Mihić 2023, PMC10795752](https://pmc.ncbi.nlm.nih.gov/articles/PMC10795752/) (search-snippet level this pass; the earlier pass read the full text)
- **Per-point labelling:** Ferrari and Spairani (AIME 2025 chapter; EHJ 2025 abstract), 319 CCTA patients. Features are curvature and **Lempel-Ziv complexity** computed over overlapping sliding windows on the 3D centerline, encoded by a custom algorithm. A multivariate discrete HMM labels each point absent/low, moderate or severe. On 18 LADs: precision 0.87, recall 0.86, per-class accuracy 0.93/0.83/0.74. Window size is not given. — [Springer chapter page](https://link.springer.com/chapter/10.1007/978-3-031-95841-0_27) (abstract-only); [EHJ 2025 abstract](https://academic.oup.com/eurheartj/article/46/Supplement_1/ehaf784.136/8312275) (abstract-only)
- A threshold-free curvature integral has coronary precedent: average absolute curvature correlated best with low TAWSS in 127 CAD-free CCTA patients, and the tortuosity index did not (p = 0.86). — [Kashyap 2022, PMC8764056](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)

### Inferences
All of the following are derivations.

- **Where the zeros come from.**
  - *Planar C-shape:* the curvature vector keeps one direction (φ constant), so no split occurs; n = 1, and (n−1)/n = 0.
  - *Helix* (κ, τ constant): no curvature peaks and no Frenet flip, so n = 1 → 0. In PT coordinates, however, φ grows linearly (φ′ = τ). Splitting whenever the accumulated PT angle since the last boundary exceeds α gives bends of length α/τ, so a helix yields n ≈ τL/α bends. A tight helix scores high, a loose one low. That is what is wanted.
  - *C-shape, again:* even with that split, a C-shape stays one bend. The (n−1)/n factor therefore has to go, or C-shapes are zero by construction. Whether a C-shape *should* score above zero is the thesis decision flagged in the earlier report. With (n−1)/n removed, it scores its own arc/chord excess: 0.571 for a 180° arc (πR / 2R − 1) and about θ²/24 for small θ.
- **Bend-level features** (for bend b with arc length L_b and chord C_b):
  - Turning θ_b = ∫_b κ ds. This equals the angle between end tangents only for planar bends and is at least that angle otherwise.
  - Bend radius R_b = L_b / θ_b, or 1/κ_peak.
  - Lumen-normalised sharpness δ_b = r_b / R_b, with r_b the mean inscribed-sphere radius of the bend (Dean ratio).
  - Excess e_b = L_b / C_b − 1.
  - Twist within the bend, ∫_b τ ds (equal to the PT angle change).
  - Inter-bend angle, the PT angle between adjacent bend peaks (Bogunović's "angle between adjacent bends").
  - Inter-bend distance, from peak to peak in mm.
  - Bend density, n / L per 100 mm.
- **Aggregations and their properties.**
  1. **Σθ_b / L.** Identical to κ_a / SOAM without torsion if the bends tile the vessel, so the decomposition adds nothing. It is useful only as the baseline.
  2. **Σ e_b / L** (Grisan's numerator without (n−1)/n). Non-zero for C-shapes and split helices. Still grows roughly as θ²/24 per bend, so it rewards few sharp bends over many shallow ones.
  3. **Radius-aware Σ θ_b·√δ_b / L or Σ θ_b·δ_b / L.** Dimensionless per unit length. A tight bend in a large vessel counts more than the same angle in a small one. This matches the Dean-number argument, but it has **no validation in any source found**. It needs a per-point radius, and the ImageCAS-X VTK radius array has not yet been checked (`tortuosity/CLAUDE.md`).
  4. **Count of bends with θ_b ≥ 45° per 100 mm.** The 3D analogue of the angiographic "≥ 3 consecutive bends > 45°". It is a count, which `tortuosity/CLAUDE.md` rejects as the primary measure (Zebić Mihić 2023b). Report it only for comparability with the angiographic literature. Angle conventions differ: "≥ 45° change in direction" means interior angle ≤ 135°, Zegers' ≤ 120° interior means ≥ 60° turning, and Estrada's < 90° interior means > 90° turning. 3D θ_b removes the projection foreshortening that biases the 2D angles.
  5. **max_b θ_b·√δ_b** (worst bend). Captures a single sharp kink that a mean dilutes, but it is a max statistic, so it is noisy.
  6. **Σ θ_b² / L.** Penalises concentration of turning. Its ratio to (Σθ_b)² / L is a "sharpness concentration" that separates one wide arc from several tight bends at equal total turning.
- Criterion 1 in `tortuosity/CLAUDE.md` (monotone in amplitude): Bullitt's own Table 2 shows the sum-of-angles family fails it when amplitude rises at fixed frequency and path length grows (SOAM 0.9 → 0.4). Options 2 and 3, per-bend excess and radius-weighted turning, are the candidates that can rise with amplitude. This must be checked on the synthetic suite, not assumed.
- The PT-angle split threshold α is the one new parameter. The ICA thresholds (45-110°) are anatomy-tuned and do not transfer. α should be chosen by rank stability (criterion 2), e.g. a sweep of 45, 90 and 135°.

### Gaps
- No published method found that aggregates bend-level features with a lumen-radius weighting, or that splits helices by PT angle. Both are proposals.
- Ferrari 2025's window size, feature encoding and HMM state structure were not accessible (paywall). It is unknown whether a per-point label can be summarised into a continuous per-vessel index.
- No source was found on the noise behaviour of a per-bend r/R ratio. Radius and curvature errors would multiply.

## Q3. Is there evidence linking bend-level features to clinical or haemodynamic outcomes in coronaries?

### Takeaway
Weak and indirect. Coronary evidence links *vessel-level* curvature integrals or counts to haemodynamics and plaque. No study found tests *per-bend* features (angle, radius, r/R) against a coronary outcome. The strongest per-bend outcome evidence is in the carotid siphon, from 2D angiographic angles, and even there whole-shape descriptors beat bend features for classification.

### Cited Findings
- Kashyap 2022: in 127 CAD-free CCTA patients, average absolute curvature had the highest R² against the % of vessel area with TAWSS < 0.4 Pa (p < 0.001), followed by squared-derivative curvature (p = 0.001) and RMS curvature (p = 0.002). The tortuosity index was not significant (p = 0.86). — [Kashyap 2022, PMC8764056](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Vorobtsova 2016 (idealised and patient-specific CFD): perfusion pressure falls with tortuosity, but more tortuous patient vessels had *higher* WSS, driven by helical flow. There was "a strong correlation between tortuosity and helicity intensity", and "an accurate representation of coronary tortuosity must account for all relevant geometric aspects, including curvature imposed by the heart shape". — [Europe PMC abstract, doi 10.1007/s10439-015-1492-3](https://doi.org/10.1007/s10439-015-1492-3) (abstract-only)
- Carotid siphon, 2D DSA, 692 aneurysm patients: an anterior-knee angle > 15.40° was associated with rupture (P = .005), post-siphon location (P = .034) and size (P = .015). This is a 2D bend-angle feature, not Bogunović's 3D method. — [Waihrich 2017 AJNR, PMC7963716](https://pmc.ncbi.nlm.nih.gov/articles/PMC7963716/) (abstract-only)
- Bogunović 2012: LDDMCM whole-shape similarity classified siphon shape classes better than the bend-based geometric features. — [Bogunović 2012 abstract](https://doi.org/10.1016/j.media.2012.01.006)
- Sangalli and co-workers report a "strong relationship between vessel geometry and aneurysm location" from curvature and radius profiles in AneuRisk65, with "interesting results" on aneurysm position within bends (not quantified in the 2009 paper). — [Sangalli 2009 §2, §5](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JRSSC_compresso.pdf)
- Thomas 2005: in the older group, no demographic effect on carotid geometry survived Bonferroni (P < 0.0056). There was a "near-significant" effect of total plaque area on ICA:CCA ratio. — [Thomas 2005 PDF](https://uwo.scholaris.ca/bitstreams/e9c3d588-e9bb-4ca6-9df3-fb0e81a0e8dc/download)
- Search snippet only: plaques are said to concentrate near side branches and "at the lesser curvature of bends where blood flow speeds are relatively low". Its primary source was not identified. — [ScienceDirect snippet, IJC 2015](https://www.sciencedirect.com/science/article/abs/pii/S0167527315306434) (unverified)

### Inferences
- For the thesis, the haemodynamic rationale for bend-level features is the Dean-number argument (r/R, Sangalli) plus Vorobtsova's helicity finding. Helicity arises from torsion and out-of-plane bends. That is a reason not to zero helices, and to keep a torsion or PT-angle component as Bullitt's SOAM does (derivation).
- Kashyap's result means any bend-level index must beat plain κ_a on the pre-registered criteria before it is preferred. Per-bend decomposition adds value only if it separates shapes that κ_a confuses: one wide arc against several tight bends at equal total turning, and radius-relative sharpness (derivation).

### Gaps
- No coronary study found that tests per-bend angle, bend radius, r/R or inter-bend distance against plaque, WSS or events. The searches were limited (about 3 queries on this point), so this is "not found", not "does not exist".
- The Vorobtsova full text (idealised bend parametrisation: number of bends, bend angle, curvature radius) was not retrievable (the post-print link returned HTML), so its bend-level CFD numbers are missing.
- No comparison was found between cardiac-phase effects on bend-level features and the known phase effect on inflection counts (van Zandwijk 2019, earlier report).
