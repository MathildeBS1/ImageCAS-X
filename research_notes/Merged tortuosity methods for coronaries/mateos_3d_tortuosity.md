# Mateos et al. 2024, "3D Tortuosity computation as a shape descriptor": method in depth and fit to coronary centerlines

Paper: Mateos M-J, Bribiesca E, Guzmán-Arenas A, Aguilar W, Marquez-Flores JA. "3D Tortuosity computation as a shape descriptor and its application to brain structure analysis." BMC Medical Imaging 2024;24:130. doi:10.1186/s12880-024-01312-6. Received 14 Feb 2023, accepted 27 May 2024. CC BY 4.0. Read in full from the local PDF (12 pages, `tortuosity/ 3D Tortuosity computation as a shape descriptor.pdf`; note the filename starts with a space) with pdftotext, plus page images of pp. 3 to 6 for equations and Figs. 2 to 4. Page numbers below are the journal's "Page n of 12".

Source links used throughout: [PDF / DOI](https://doi.org/10.1186/s12880-024-01312-6), [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11149256/).

## What exactly is the tortuosity definition?

### Takeaway
τ3D is not a curve measure. It is the 2D Slope Chain Code (SCC) tortuosity of Bribiesca 2013 (sum of normalised absolute turning angles along a polygonal contour), applied to the boundary contour in every axis-aligned slice of a binary voxel object, summed per slice, averaged over slices in each of X, Y, Z, and added over the three directions (Eq. 8). For a single 2D curve the SCC value is total absolute turning divided by π.

### Cited Findings
- Continuous background (p. 3, Eqs. 1 and 2): average curvature of arc EF is K_av = α / EF, where α is the angle of contingency (angle between tangents at E and F); curvature at E is K_E = lim_{F→E} K_av = lim_{EF→0} α/EF. — [Mateos 2024, p. 3](https://doi.org/10.1186/s12880-024-01312-6)
- Discrete curvature (p. 4, Eq. 3): assume EF is "constant and straight, as in the notation of the SCC"; set EF = 1, so K_E = α. The discrete curvature at a vertex is "the angle of contingency α, or the slope change between contiguous straight-line segments at that point". It is normalised to the range (−1, 1); "Extreme values of 1 or −1 are not taken into consideration for practical purposes." — [Mateos 2024, p. 4](https://doi.org/10.1186/s12880-024-01312-6)
- Fig. 2b (p. 3) shows the normalisation graphically: 0 = no turn, ±0.5 = 90° turn, ±1 = 180° reversal, i.e. a_n = (signed turning angle)/180°. The sign encodes turn direction (left/right) in the slice plane. — [Mateos 2024, Fig. 2b, p. 3](https://doi.org/10.1186/s12880-024-01312-6)
- Chain (Eq. 4, p. 4): A = a_1 a_2 … a_n, where a_n is "the slope change between contiguous straight-line segments of the curve in that element position", range −1 to 1. — [Mateos 2024, Eq. 4](https://doi.org/10.1186/s12880-024-01312-6)
- 2D tortuosity (Eq. 5, p. 4): τ = Σ_{n=1}^{N} |a_n|, N = total number of chain elements (citing Bribiesca 2013, ref [16]). — [Mateos 2024, Eq. 5](https://doi.org/10.1186/s12880-024-01312-6)
- Per-slice chains (Eq. 6, p. 5), verbatim structure: X_i = x_{1i} x_{2i} … x_{N_i i}, "contour(s) in slice i, direction X", i = 1..S_X; likewise Y_j = y_{1j} … y_{M_j j}, j = 1..S_Y; Z_k = z_{1k} … z_{L_k k}, k = 1..S_Z. S_X, S_Y, S_Z are "the number of slices in each direction". — [Mateos 2024, Eq. 6](https://doi.org/10.1186/s12880-024-01312-6)
- Eq. 7 (p. 5) only states the correspondence Σ_{n=1}^{N_i}|a_n| → Σ_{n=1}^{N_i}|x_{ni}|, Σ_{m=1}^{M_j}|y_{mj}|, Σ_{l=1}^{L_k}|z_{lk}|. — [Mateos 2024, Eq. 7](https://doi.org/10.1186/s12880-024-01312-6)
- Eq. 8 (p. 5), the definition:
  τ3D = [Σ_{i=1}^{S_X} Σ_{n=1}^{N_i} |x_{ni}|] / S_X + [Σ_{j=1}^{S_Y} Σ_{m=1}^{M_j} |y_{mj}|] / S_Y + [Σ_{k=1}^{S_Z} Σ_{l=1}^{L_k} |z_{lk}|] / S_Z.
  The Conclusions restate it as "the normalized sum of all the slope chain elements for each filtered contour in every slice, and in the X, Y, and Z directions" (p. 11). — [Mateos 2024, Eq. 8, p. 5 and p. 11](https://doi.org/10.1186/s12880-024-01312-6)
- Reference values (p. 5): per Bribiesca, τ for any simple convex closed curve = 2; "extending it to surfaces the value of τ3D for convex closed surfaces is always 6". — [Mateos 2024, p. 5](https://doi.org/10.1186/s12880-024-01312-6)
- The paper frames the arc/chord ratio (Lotmar) as inadequate because two curves with equal arc and chord can differ in turns (Fig. 1, p. 2). — [Mateos 2024, p. 2, Fig. 1](https://doi.org/10.1186/s12880-024-01312-6)
- Parent 2D method (secondary description, not read in full): the SCC places straight-line segments of constant length along the curve with endpoints on the curve and takes slope changes scaled to (−1, 1); Bribiesca 2013 also defines min/max tortuosity and a normalised tortuosity. — [ResearchGate abstract of Bribiesca 2013, Pattern Recognit 46:716–724](https://www.researchgate.net/publication/256822731_A_measure_of_tortuosity_based_on_chain_coding)

### Inferences
- Since a_n = θ_n/π with θ_n the exterior (turning) angle, Eq. 5 is τ = (1/π) Σ|θ_n|: the discrete total absolute curvature of the polygon divided by π. This is why a convex closed curve gives exactly 2 (total turning 2π), independent of its size, and a straight open line gives 0. It is the same quantity as the numerator of Bullitt 2003's sum-of-angles metric, but without dividing by length and in planar form.
- For τ3D = 6 on a sphere, S_X must count only slices that intersect the object; if empty slices of the volume were counted, the sphere value would depend on the field of view. The paper does not state this explicitly (my reading of Eqs. 6 and 8 against the value 6).
- Each slice term is the sum over all contour components ("contour(s)") in that slice, so a slice that cuts the object into k disjoint convex blobs contributes ≈ 2k. τ3D therefore mixes two things: concavity of each slice contour and number of connected cross-sections per slice. Holes (inner contours) would add further contributions; the paper does not say whether inner contours are traced.
- The measure is signed per element but only |a_n| enters, so inflection structure (sign changes) is discarded, unlike Grisan 2008 or Bullitt's inflection count.

### Gaps
- Bribiesca 2013 was not read in full here; the exact constant-segment-length placement and its "normalized tortuosity" formula are known only from the abstract.
- Whether inner (hole) contours are traced, and whether S_X counts only non-empty slices, is not stated in the paper.

## Does it operate on a volume, a skeleton, or a curve? How does it handle branching?

### Takeaway
Input is a binary voxelized solid. The 1D objects actually measured are 2D boundary contours of axis-aligned slices. There is no skeleton, no 3D curve, and no concept of branching; the Discussion explicitly separates it from methods that capture "changes in 3D trajectories".

### Cited Findings
- Pipeline (p. 4): (1) obtain the voxelized object; (2) "Track contours for every slice i, j, k, for each corresponding direction X, Y, Z"; (3) filter stair-stepping: downsample contours, then apply a Digital Straight Segment (DSS) algorithm; (4) compute τ3D. — [Mateos 2024, p. 4](https://doi.org/10.1186/s12880-024-01312-6)
- Contour tracking: trace the complete border in each slice "to obtain a sequence of boundary points without vertex repetition", citing two tracing algorithms (refs [34] Seo 2016, [35] Ren 2002) without saying which was used. — [Mateos 2024, p. 4](https://doi.org/10.1186/s12880-024-01312-6)
- Discussion (p. 10): other 3D methods "focus on capturing changes in 3D trajectories, whereas our approach is specifically designed to measure the 3D morphological variations of volumetric objects. Consequently, our method cannot be compared with these other methods". — [Mateos 2024, p. 10](https://doi.org/10.1186/s12880-024-01312-6)
- Claimed advantage: "the SCC is generated directly from the voxels, reducing sources of uncertainty and improving computation speed", "can be applied to any voxelized object" (p. 10), "without requiring interpolation" (p. 3). — [Mateos 2024, pp. 3, 10](https://doi.org/10.1186/s12880-024-01312-6)
- The 2025 follow-up by the same first author (ADNI, 1354 participants, Desikan–Killiany regions from FreeSurfer) uses the same Eq. 8 unchanged on "cortical contours extracted in three orthogonal orientations (axial, coronal, sagittal)", "carried out independently in three directions (X,Y,Z) for every cortical region". — [Mateos, Lah, Qiu 2025, NeuroImage: Clinical](https://pmc.ncbi.nlm.nih.gov/articles/PMC12508885/)

### Inferences
- Applied to a coronary lumen mask, τ3D would measure lumen cross-section outline complexity plus the number of times each axis-aligned slice cuts the tree. A vessel running along an axis gives near-circular contours (≈2 each); a vessel curving through the slice planes, and every bifurcation, adds extra components (≈2 each). The number is thus driven by vessel orientation relative to the scanner axes and by branch count, not by centerline path shape.

### Gaps
- No branching or tree handling exists in the paper; nothing to report.

## What parameters or smoothing does it require, and how sensitive is it to noise and sampling?

### Takeaway
Two filtering choices: contour downsampling by a fixed factor of 10 (DSF) and Kovalevsky's DSS polygonal approximation, which together define the straight segments and hence the chain. The authors call τ3D "extremely sensitive to the definition of chain elements" and show error growing at large radii because DSF is fixed. No noise experiment exists.

### Cited Findings
- Stair-stepping (p. 5, Fig. 3): an axis-aligned voxel line gives a straight contour, a 45° line gives a staircase whose every step is a spurious slope change. — [Mateos 2024, p. 5, Fig. 3](https://doi.org/10.1186/s12880-024-01312-6)
- Downsampling (p. 5): "decreasing the sampling frequency of the tracked contours by a factor of ten. The choice of downsampling factor (DSF) is influenced by the size of the analyzed objects and is used to balance the reduction of the artifact with the preservation of relevant details". — [Mateos 2024, p. 5](https://doi.org/10.1186/s12880-024-01312-6)
- DSS (p. 5): after downsampling, "a DSS-algorithm is applied to select the vertices that define different straight segments"; the Kovalevsky method [37] is used, "based on calculating the narrowest strip defined by the nearest support below and above". — [Mateos 2024, p. 5](https://doi.org/10.1186/s12880-024-01312-6)
- Sensitivity statement (p. 6): "the computation of τ3D is extremely sensitive to the definition of chain elements; thus, the filtering process is essential to achieve an accurate estimation." — [Mateos 2024, p. 6](https://doi.org/10.1186/s12880-024-01312-6)
- Scale-dependent failure (p. 6): with constant DSF, "the downsampling process becomes insufficient in filtering out stair-stepping artifacts for larger spheres radii", increasing error. — [Mateos 2024, p. 6](https://doi.org/10.1186/s12880-024-01312-6)
- Smoothing experiment (pp. 6–7, Eq. 10, Fig. 5): morphological closing (I ⊕ B) ⊖ B of a brain pial surface with spherical B of radius 2, 4, 6, 8; τ3D decreases with B; "The last two volumes exhibit no statistically significant difference". — [Mateos 2024, pp. 6–7](https://doi.org/10.1186/s12880-024-01312-6)
- Image quality: "Given the sensitivity of τ3D to both image quality and segmentation accuracy, a visual inspection was conducted", removing 9 of 69 MIRIAD subjects (pp. 7–8). — [Mateos 2024, pp. 7–8](https://doi.org/10.1186/s12880-024-01312-6)

### Inferences
- Note the DSS approximation produces segments of unequal length, which departs from the SCC's constant-length segments (Eq. 3 sets EF = 1). The effective segment length, and so the measured total turning, then depends on local geometry and voxel orientation. This is the likely reason for the stated sensitivity.
- A downsampling factor of 10 boundary points presupposes contours of at least tens of points. A coronary cross-section at 0.5 mm voxels (radius 1 to 2 mm = 2 to 4 voxels, perimeter roughly 12 to 25 boundary points) would be reduced to 1 to 3 vertices, below the smallest validated sphere (radius 10 voxels).
- The DSF is a smoothing scale in voxel units, not in mm; results across scanners with different voxel size would not be comparable without rescaling it.

### Gaps
- No noise-injection, resampling, or segmentation-perturbation experiment; the only robustness evidence is the sphere error map and the closing experiment.
- Which contour-tracing algorithm and what connectivity (4 vs 8) were used is not stated.
- No code release found (paper has no code availability statement; the 2025 follow-up also mentions none per [PMC12508885](https://pmc.ncbi.nlm.nih.gov/articles/PMC12508885/)).

## What properties (scale invariance, rotation invariance, additivity, monotonicity) are claimed or shown?

### Takeaway
Claimed: translation, rotation, scale invariance inherited from 2D SCC, and scale invariance of τ3D "to some extent" at DSF = 10. Shown: only |τ3D − 6| on voxelized spheres (radius 10 to 80 voxels, "different angles"), plus a decrease under morphological smoothing on one brain. Rotation invariance of τ3D itself, additivity and monotonicity in folding amplitude/frequency are not tested.

### Cited Findings
- Introduction (p. 2): SCC "is independent of translation, rotation, and scaling" (said of 2D SCC). — [Mateos 2024, p. 2](https://doi.org/10.1186/s12880-024-01312-6)
- Validation (pp. 5–6, Eq. 9): voxelized spheres "generated at different angles and with different radii"; absolute error Δx = |x_i − x|, x = 6. Fig. 4 heat map: angle 0–360°, radius 10 to 80 voxels; "the tortuosity can be computed with an error of ± 1 for objects with r ∈ [10, 70] voxels"; results "suggest that the proposed method for computing tortuosity is, to some extent, invariant under scaling for a downsampling factor of 10". — [Mateos 2024, pp. 5–6, Fig. 4](https://doi.org/10.1186/s12880-024-01312-6)
- From the Fig. 4 image (my reading): radius rows are 10, 15, 20, 30, 40, 50, 70, 80 (no 60); colour bar tops out near 1.3; errors at r = 10 to 40 are mostly ≈0.2 to 0.4, rows 70 and 80 approach 1 to 1.3. An error of 1 on a reference value of 6 is about 17 %. — [Mateos 2024, Fig. 4, p. 6](https://doi.org/10.1186/s12880-024-01312-6)
- Conclusions (p. 11): "This validation establishes the accuracy and scale invariance of τ3D." — [Mateos 2024, p. 11](https://doi.org/10.1186/s12880-024-01312-6)
- Clinical use (pp. 7–10, Tables 1–4): MIRIAD, 60 subjects (37 AD, 23 controls); Wilcoxon per lobe p = 0.0286 frontal, 0.031 parietal, 0.002 occipital, 0.003 temporal, controls higher; after age/sex regression (Table 3) occipital p = 0.0648; left central sulcus p = 0.021 (z = 2.32) with AD higher, right p = 0.21 (Table 4). — [Mateos 2024, pp. 8–9](https://doi.org/10.1186/s12880-024-01312-6)
- Limitations: no limitations section; Conclusions only note that clinical validation is hard because brain structures are hard to access (p. 11). Future work: other databases and longitudinal studies (p. 11). The 2025 follow-up lists parcellation dependence and no scanner test-retest evaluation as limitations. — [Mateos 2024, p. 11](https://doi.org/10.1186/s12880-024-01312-6); [Mateos 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12508885/)

### Inferences
- The sphere test cannot probe rotation invariance: a sphere looks identical from every direction. Because contours are taken in fixed X, Y, Z slices, rotating an elongated or folded object changes how many components and concavities each slice sees, so τ3D is generally not rotation invariant. For a single tubular vessel this is the dominant effect.
- Scale invariance is only approximate and only within one DSF; with a fixed DSF, small objects are over-smoothed and large ones under-filtered (the paper's own Fig. 4 trend).
- Monotonicity was shown only in the weak sense that heavier smoothing lowers τ3D on one brain.

### Gaps
- No evidence on additivity, monotonicity with amplitude/frequency, or agreement with perceived tortuosity.

## Checks against the existing note `docs_thesis/papers/mateos2024tortuosity3d.md`

### Takeaway
The existing note is accurate on the method, the validation, the numbers and the Table 1 duplicates (all re-verified). It misses several internal inconsistencies of the paper and, more importantly for coronaries, the curve-based 3D SCC follow-up (Bribiesca-Sánchez et al. 2024), so its "of no use for coronary centerlines" verdict is right for τ3D but too broad for the SCC family.

### Cited Findings
- Confirmed: DSF = 10, Kovalevsky DSS, Eq. 8, value 6 for convex surfaces, sphere radii 10–80, error ±1 for r ∈ [10, 70], closing radii 2/4/6/8, 69 → 60 subjects, Table 2–4 p-values, Discussion quote on "3D trajectories". — [Mateos 2024](https://doi.org/10.1186/s12880-024-01312-6)
- Confirmed by recomputation from Table 1 text: identical four-lobe rows for IDs 27 (AD) / 28 (Control) / 29 (Control); 39 (Control) / 40 (AD); 43 (AD) / 44 (AD); 55 (Control) / 56 (AD). — [Mateos 2024, Table 1, pp. 8–9](https://doi.org/10.1186/s12880-024-01312-6)
- New: the text's per-lobe medians swap parietal and occipital. Text (p. 9) gives parietal M = 33 (AD) / 35 (control) and occipital M = 59 / 62, but Table 1's occipital column ranges ≈26–42 and parietal ≈45–73. My recomputed medians from Table 1: occipital 33.3 (AD) / 34.7 (control), parietal 59.1 / 62.4. Table 2 also orders columns Frontal, Parietal, Occipital, Temporal while Tables 1 and 3 use Frontal, Occipital, Parietal, Temporal, so which lobe carries which p-value in Table 2 is uncertain. — [Mateos 2024, pp. 8–9](https://doi.org/10.1186/s12880-024-01312-6)
- New: Fig. 5 caption says closing is "(Eq. 5)" (it is Eq. 10) and speaks of "five structuring elements" while the text lists four radii (2, 4, 6, 8); probably the original plus four. — [Mateos 2024, pp. 6–7](https://doi.org/10.1186/s12880-024-01312-6)
- New: p. 3 states the average curvature α/EF "is equivalent to the geodesic distance between the points of the arc EF", which is dimensionally wrong (curvature is angle per length). — [Mateos 2024, p. 3](https://doi.org/10.1186/s12880-024-01312-6)
- New: the existing note says figures were read from captions only; Figs. 2–4 are now read as images (see Fig. 2b normalisation and Fig. 4 radius rows above).
- New and important: the SCC group published a separate 3D *curve* extension. Bribiesca-Sánchez A. et al., "A three-dimensional extension of the slope chain code: analyzing the tortuosity of the flagellar beat of human sperm", Pattern Analysis and Applications, published online 28 June 2024 (received 1 Dec 2023). It encodes polygonal 3D curves with parallel slope and torsion chains, claims invariance to translation, rotation and uniform scaling, and robustness to mirroring and starting point. — [Springer landing page](https://link.springer.com/article/10.1007/s10044-024-01286-9); [ResearchGate](https://www.researchgate.net/publication/381803010_A_three-dimensional_extension_of_the_slope_chain_code_analyzing_the_tortuosity_of_the_flagellar_beat_of_human_sperm)
- Per search-engine summaries of that paper (secondary, full text paywalled / 403 here): slope changes are scaled to [0, 1], torsion to [0, 0.5], and 3D-SCC tortuosity is the sum of absolute slope changes and torsions. Treat as unverified. — [Springer landing page (via search snippet)](https://link.springer.com/article/10.1007/s10044-024-01286-9)
- The 3D-SpermFlagella dataset paper (Scientific Data 2026) cites that work but does not restate its definitions; its released code is the flagellum tracer, not the tortuosity code. — [PMC13039792](https://pmc.ncbi.nlm.nih.gov/articles/PMC13039792/)
- A 2025 retinal paper applies SCC with a "scale-independent" tortuosity to retinal vessels (Experimental Eye Research, S0014483525000570); full text not retrievable (403). — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0014483525000570)

### Inferences
- For the thesis gap statement, "the SCC line has no 3D curve tortuosity" would be false; Bribiesca-Sánchez 2024 is the relevant 3D curve descendant and should be read (paper-review) before objective 7 cites the SCC family.

### Gaps
- Bribiesca-Sánchez 2024 and the 2025 retinal SCC paper were not accessible in full; their exact formulas, segment-length rule and validation are unverified.

## What would it take to run it on a coronary centerline tree (0.5 mm isotropic CCTA, noisy, bifurcations)?

### Takeaway
τ3D as published cannot be used: it needs a large binary solid, is axis-dependent, and measures slice-contour folding, not a vessel path. What transfers is the SCC core applied directly to each 3D centerline polyline: resample at a constant chord length ℓ, take turning angles θ_n, and sum θ_n/π (optionally plus a torsion chain as in Bribiesca-Sánchez 2024). That is a total-absolute-curvature measure whose smoothing scale is ℓ, and it needs per-segment handling of branches and an explicit length normalisation choice.

### Cited Findings
- The SCC's defining assumptions are constant, straight segments (EF = 1, Eq. 3) and chain elements = normalised slope change (Eqs. 4–5). — [Mateos 2024, pp. 3–4](https://doi.org/10.1186/s12880-024-01312-6)
- The authors themselves say trajectory-based 3D tortuosity is a different problem that their method does not address (p. 10). — [Mateos 2024, p. 10](https://doi.org/10.1186/s12880-024-01312-6)
- Only validated at object scales ≥ 10 voxels radius with DSF = 10 (p. 6). — [Mateos 2024, p. 6](https://doi.org/10.1186/s12880-024-01312-6)
- Project context: centerlines are LPS-mm polylines per scan (left tree LM/LAD/LCX, right RCA) with per-point `segment_label`; radius array and junction sharing not yet checked; measurement rules demand per-vessel and per-segment length-normalised output, sweeps over smoothing and resampling, and synthetic-curve checks (zero on a line, monotone in amplitude and frequency, rotation invariant, separates one wide arc from several tight bends). — `tortuosity/CLAUDE.md` (local file)

### Inferences
- **Do not voxelize the lumen and run Eq. 8.** Coronary cross-sections are 2 to 8 voxels across at 0.5 mm, far below the validated range; the result would depend on heart orientation in the scanner and branch count.
- **Minimal SCC-for-centerlines (reconstructed, not from the paper):** for each branch polyline P(s), (1) resample with vertices on the curve at constant chord length ℓ (mm), (2) unit segment directions u_n, (3) θ_n = arccos(u_n · u_{n+1}) ∈ [0, π), (4) a_n = θ_n/π, (5) τ_SCC = Σ a_n. Optionally add a torsion chain (dihedral angle between consecutive osculating planes, scaled to [0, 0.5] per the 3D-SCC summary). This is rotation and translation invariant by construction, which τ3D is not.
- **ℓ is the whole smoothing story.** Because Σθ converges to (1/π)∫κ ds only as ℓ → 0 for a smooth curve, and point jitter of σ on vertices spaced ℓ adds turning of order σ/ℓ radians per vertex, τ_SCC diverges as ℓ approaches the noise scale. With ~0.5 mm jitter, ℓ must be several mm, and the CLAUDE.md rule (report values across ℓ and resampling) applies directly. A radius-proportional ℓ (e.g. a multiple of the local lumen radius) is one way to get anatomical scale invariance; that is a design choice, not something in the paper.
- **Length normalisation is a real choice.** SCC τ is a total (additive over concatenated pieces, plus the junction angle), so it grows with the number of bends and with vessel length. Per-length output (τ/L, which is essentially Bullitt 2003's sum-of-angles metric in normalised units) or per-segment totals must be chosen explicitly. The paper's "scale invariance" means invariance to uniform scaling of the whole shape at a proportionally scaled ℓ, which is not what fixed-ℓ (mm) resampling on vessels of different length gives.
- **Behaviour against the synthetic criteria (analytic, to be verified in code):** straight line → 0; a single 180° bend gives τ = 1 whatever its radius, so one wide arc and one tight hairpin score the same, while several tight bends score more; for a sinusoid y = A sin(2πx/λ), total turning per half period is 2·arctan(2πA/λ), so τ rises with frequency but saturates in amplitude (each half period is capped at π). That saturation is a candidate failure of "monotone in amplitude" at large A/λ.
- **Branching.** SCC is defined per curve; a tree must be split into segments (by `segment_label`) or root-to-leaf paths. Decide whether the turning angle at a bifurcation is counted (it belongs to the tree's geometry, not to either vessel's path) and exclude it by default so per-segment values sum consistently. Junction points shared between branches (not yet checked in the VTK files) must be handled before resampling.
- **Plaque artefact.** Local centerline deviation at stenoses adds turning like any other noise; ℓ larger than typical lesion length suppresses it but also removes real tight bends. This interacts with the "must not read high because of plaque" rule and should be tested with the jitter/ICC criterion.
- **Radii** are not used by SCC at all; they enter only if ℓ is tied to radius or if a lumen-aware measure is wanted.
- Net: Mateos 2024 contributes nothing implementable for coronaries beyond pointing to the SCC definition; the actually relevant sources are Bribiesca 2013 (2D SCC tortuosity) and Bribiesca-Sánchez 2024 (3D SCC with torsion).

### Gaps
- Exact 3D-SCC torsion definition and scaling, and whether Bribiesca-Sánchez 2024 validate against noise or sampling, need the full text (not accessible here).
- No published application of SCC-type tortuosity to coronary centerlines was found in these searches (absence in a limited search, not proof of absence).
- Whether Bribiesca's earlier chain codes for 3D tree objects handle branching in a way reusable here was not checked.
