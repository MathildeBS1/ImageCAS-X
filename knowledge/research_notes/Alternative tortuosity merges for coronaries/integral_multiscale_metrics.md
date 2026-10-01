# Integral and multiscale 3D curve tortuosity descriptors as merge partners for coronary tortuosity

Scope: curvature/torsion integrals, knot-theory descriptors (writhe, average crossing number), and multiscale/frequency descriptors (Fourier/wavelet, scale-space, fractal dimension), judged against the selection criteria in `tortuosity/CLAUDE.md` and against the known weaknesses of the earlier SCC + 3D-Grisan merge (`reports/Merged tortuosity methods for coronaries.md`): Grisan = 0 on C-shapes and helices; SCC density blind to bend radius and saturating with amplitude; strong noise sensitivity at 0.5 mm spacing.

Evidence labels. **Full text** = read in full (PMC or open HTML) in this pass. **Abstract-only** = only abstract, landing page or search snippet seen. **Derivation** = my own closed-form reasoning on standard differential geometry; no source states it, and it must be checked numerically in the synthetic suite before it carries weight. Tool budget allowed about 15 retrievals, so several classic papers (Bullitt 2003 full PDF via PMC summary only, Johnson and Dougherty 2007, Choi 2009, Kalitzeos Fourier retinal work, Diedrich 2011) were not read in full.

Notation used throughout: centerline r(s), arc length s, length L, chord C = |r(L) − r(0)|, curvature κ ≥ 0, torsion τ (signed), Frenet frame (T, N, B), Darboux vector ω = τT + κB. Discrete version: polyline resampled at constant chord ℓ, unit chord directions u_n, turning angle θ_n = arccos(u_n·u_{n+1}), binormal b_n = u_n×u_{n+1}/|u_n×u_{n+1}|, torsion angle φ_n = angle between b_n and b_{n+1}.

Reference synthetic cases (from `tortuosity/CLAUDE.md` criterion 1 and the earlier report): (a) straight line; (b) one wide arc of radius R and total turn Θ vs several tight bends of radius r ≪ R with the same total turn; (c) circular helix of radius a and pitch 2πb, for which κ = a/(a²+b²), τ = b/(a²+b²) (standard result, derivation-level); (d) planar sinusoid y = A sin(2πx/λ) with varying A and λ; (e) any planar curve rotated rigidly in 3D.

---

## Q1. For each family: formula, discretisation, invariances, synthetic behaviour, vascular evidence, and whether it fixes a known weakness

### Takeaway
Among integral descriptors, **bending energy per length ∫κ²ds / L (Kashyap's RMS curvature squared)** and the dimensionless **bend-concentration ratio L·∫κ²ds / (∫κds)²** are the only ones that are radius-aware and do not saturate with sinusoid amplitude, so they directly fix the SCC weaknesses; **Bullitt's SOAM total angle Σ√(IP²+TP²)/L** is the only one with published synthetic evidence that it scores helices (coils) where inflection-based indices fail. Writhe and average crossing number are exactly zero on every planar curve, so they can only be out-of-plane add-ons. Frequency-domain descriptors (band power of deviation from a smooth baseline, curvature spectrum) are the natural way to make scale explicit, but have essentially no 3D coronary validation.

### Cited Findings

**A. Curvature and torsion integrals**

- Kashyap et al. 2022 (full text, 127 CTCA patients without obstructive CAD, zero calcium score, left main bifurcation + LAD + LCx) defined: tortuosity index = arc/chord; average absolute curvature κ_a = ∫κ(t)dt / L; RMS curvature κ_r = √(∫κ²(t)dt / L); average squared-derivative curvature κ_d = ∫(dκ/dt)²dt / L. — [Kashyap 2022, Sci Rep 12:865](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Kashyap 2022 discretisation: VMTK centerlines from surface meshes, Taubin smoothing (passband 0.03, 30 iterations), resampled at 0.01 mm spacing. — [Kashyap 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Kashyap 2022 results versus low TAWSS (R²): κ_a LMCA 0.196, LAD 0.232, LCx 0.061, whole bifurcation 0.112 (p < 0.001); κ_r 0.113 / 0.164 / 0.010 / 0.093 (p = 0.002); κ_d 0.086 / 0.160 / 0.007 / 0.101 (p = 0.001); arc/chord −0.011 / 0.026 / 0.007 / −0.018 (not significant, p = 0.86). Curvature metrics "accounted for 6–27% of TAWSS variance". The endpoint is haemodynamic, not reproducibility or expert ranking. — [Kashyap 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Bullitt et al. 2003 (IEEE TMI, intracerebral MRA; read via PMC summary) define the Sum of Angles Metric: in-plane angle IP_k between consecutive tangent vectors, torsional angle TP_k between successive osculating-plane normals, total angle CP_k = √(IP_k² + TP_k²), SOAM = Σ CP_k / path length (rad/cm). Skeleton represented as a spline and "regularly sampled at intervals of the length of one voxel"; Frenet frame from velocity and acceleration. — [Bullitt 2003 (PMC2430603)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- Bullitt 2003 synthetic tests at constant path length: sine waves of increasing frequency gave DM (arc/chord) 1.6 at all frequencies (fail), ICM 9.7 → 32.3 → 64.7, SOAM 0.9 → 3.1 → 6.2. Coils (helices) of increasing frequency gave DM 1.5 constant, ICM 1.5 constant ("no inflection points in coils"), SOAM 1.3 → 4.5 → 9.2. — [Bullitt 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- Bullitt 2003 clinical: SOAM was most effective for Type III tight coils in malignant tumours (21.5 to 21.9 vs normal 12.5 to 16.8); ICM, not SOAM, detected AVM nidi (Type II); DM and ICM detected meandering basilar artery (Type I; DM 1.5 vs normal 1.1 ± 0.1). Sample sizes are small (three cases per abnormal type per the summary). — [Bullitt 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- Search-snippet description of SOAM: "effective for calculating tortuosity in curves that do not have an inflection point" and "a high response in curves with high frequencies or of the sinusoidal type" (abstract-only / snippet). — [ResearchGate figure page](https://www.researchgate.net/figure/The-diagram-sum-of-angle-metric-SOAM-given-in-rad-m-versus-vessel-segment-length-L_fig6_230808481)
- Curvature κ = |r′×r″|/|r′|³ and torsion τ = r‴·(r′×r″)/|r′×r″|² are the definitions used (the fetched summary printed r″ in the numerator, which is a transcription error: the standard formula uses r‴). Torsion is described as measuring "how sharply the curve is twisting out of the osculating circle"; parallel-transport frame gives curvature vector k₁E₁ + k₂E₂. — [Kjeldsberg 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- Thoracic aorta morphometry (48 cases, 16 per group) computed κ and τ at 200 equally spaced points with Frenet–Serret formulas after a fifth-order B-spline regression with 20 control points and second/third-derivative regularisation, but used plane-fit displacement integrals rather than integrated κ/τ as the summary. Out-of-plane (anteroposterior) displacement differed between groups (P = .010). — [Aorta morphometry, JTCVS Open 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11704593/)
- Aortic torsion literature exists that projects the centerline onto its mean plane of curvature to create "torsion-free" geometries and compares WSS; curvature–torsion graphs have been used to relate "inverted torsion" to aneurysm position (search snippets only, abstract-only). — [JTCVS Open 2024 search snippet](https://www.jtcvsopen.org/article/S2666-2736(24)00264-X/fulltext); [Springer chapter, FSI thoracic aorta](https://link.springer.com/chapter/10.1007/978-3-319-40827-9_29)
- Choi et al. 2009 (Ann Biomed Eng) developed methods for quantifying 3D deformation (length, curvature, twist) of arteries from cardiac-gated CT, motivated by stent design; coronaries "experience mechanical deformations of twisting, bending, and stretching due to their tethering to the epicardial surface" (abstract-only). — [Choi 2009, Ann Biomed Eng](https://link.springer.com/article/10.1007/s10439-008-9590-0); [PubMed 24835123](https://pubmed.ncbi.nlm.nih.gov/24835123/)

**B. Knot-theory descriptors**

- Writhe of a curve "describes its geometrical self-entanglement" and equals the average over all viewing directions of signed crossings N₊ − N₋; the average crossing number is the unsigned analogue (general reference, not vascular). — [Wikipedia: Writhe](https://en.wikipedia.org/wiki/Writhe)
- Algorithms for computing writhe of discretised curves exist in the polymer/knot literature (not vascular). — [arXiv math/0406148, Computing the writhe of a knot](https://arxiv.org/pdf/math/0406148)
- I found **no vascular (coronary, cerebral, retinal) paper using writhe or average crossing number as a tortuosity index**; the targeted search returned only polymer, solar-corona and generic tortuosity pages. — [search result set incl. Kashyap 2022 and physics preprints](https://arxiv.org/pdf/1004.3918)

**C. Multiscale / frequency-domain descriptors**

- "Improved characterisation of aortic tortuosity" (Med Eng Phys 2011, 33(6)) introduced the FFT of the vessel's curvature signal as a tortuosity measure, tested on computer-simulated vessels, a phantom and clinical data, arguing "a single value is insufficient to describe vessel tortuosity" and that the curvature spectrum "provides a compact and graphic representation"; also two MATLAB centreline extraction algorithms (abstract-only). — [PubMed 21317017](https://pubmed.ncbi.nlm.nih.gov/21317017/); [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1350453311000129)
- "Application of 3D curvature and torsion in evaluating aortic tortuosity" (Commun Nonlinear Sci Numer Simul 2020) exists but was not retrieved (title only). — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1007570420304494)
- A 2025 retinal peripapillary method defines point-to-point (local, tangent-differential), point-to-line (relative) tortuosity, and a "tortuosity spectrum"; a related retinal pipeline integrates PSD power within a target spatial-period band normalised by the number of valid samples (2D, snippet-level, abstract-only). — [PMC12574746](https://pmc.ncbi.nlm.nih.gov/articles/PMC12574746/)
- "Multiscale analysis of tortuosity in retinal images using wavelets and fractal methods" (Charles Sturt; 2D retinal) claims direct application to segmented vessels "without suffering from poorly chosen sampling rates" (abstract-only). — [CSU research output](https://researchoutput.csu.edu.au/en/publications/multiscale-analysis-of-tortuosity-in-retinal-images-using-wavelet/)
- Helmberger et al. 2014 (PLOS One, full text, 24 patients, 18 PH / 6 non-PH): 3D box-counting fractal dimension on connected lung-vessel **centerlines of the whole tree**, box sizes 1 to 100 pixels, FD = slope of log–log fit; mean FD 2.35 ± 0.06 (range 2.21 to 2.44); no correlation with mPAP (ρ = −0.30, p = 0.15) or PVR (ρ = −0.34, p = 0.10). The simple arc/chord distance metric did correlate with mPAP (ρ = 0.60, p = 0.002; AUC 0.84). Repeatability was not tested. — [Helmberger 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC3909124/)

### Inferences

Per-family formulas, discretisation, invariances and synthetic behaviour (all behaviour statements below are **derivations** unless tagged with a source above):

1. **Total absolute curvature K = ∫κ ds; discrete Σθ_n.** Mean form K/L = κ_a (Kashyap). Invariant to rotation, translation; K is scale invariant (dimensionless), K/L has units 1/mm. Line: 0. Arc of angle Θ: K = Θ for any radius, so **one 180° arc of radius 20 mm and one 180° hairpin of radius 2 mm give the same K** (radius-blind; this is the same weakness as SCC, which is literally the discrete K/π). K/L separates them only through L. Helix: K/L = κ = a/(a²+b²) > 0 (sees helices). Sinusoid: per half period 2·arctan(2πA/λ) → saturates at π as A grows (same as SCC). Rotated planar curve: unchanged. So κ_a does not fix any known SCC weakness; it *is* the SCC core.

2. **Bending energy E = ∫κ² ds; RMS κ_r = √(E/L) (Kashyap).** Discrete: Σ(θ_n/ℓ)²·ℓ = Σθ_n²/ℓ. Invariant to rigid motion; E scales as 1/length, E·L is dimensionless and scale invariant. Line: 0. Arc of angle Θ, radius R: E = Θ/R, so **tight bends score higher than a wide arc of equal turning, in proportion to 1/radius (radius-aware)**. Helix: E/L = κ². Sinusoid: for small A, E per wavelength ≈ A²(2π/λ)⁴·λ/2, and for large A the crest radius shrinks roughly as λ²/(4π²A) so E keeps rising; **no amplitude saturation**, monotone in A and in frequency. Rotated planar curve: unchanged. This fixes the two SCC weaknesses (radius blindness, amplitude saturation) and the helix/C-shape blindness of Grisan, but is worse for noise (see Q2).

3. **Bend-concentration ratio Q = L·E / K² = (mean κ²)/(mean κ)².** By Cauchy–Schwarz Q ≥ 1, with equality iff κ is constant along the curve. Dimensionless and scale invariant; undefined on a line (K = 0, return NaN or define 0). Single arc: Q = 1. Helix: Q = 1. Several tight bends joined by straights: Q = L/(sum of bend arc lengths) > 1, so it rises as bending concentrates into few short, tight bends. This is a threshold-free, radius-aware quantity that **separates "one gentle big curve" from "few tight bends" without any turn segmentation**, and it is related to Kashyap's κ_d (curvature variability). It does not by itself grow with amplitude, so it must be paired with a magnitude term (K/L or E/L).

4. **Total torsion ∫|τ| ds; SOAM torsion part ΣTP_k.** Zero on every planar curve (including planar sinusoids and arcs): useless as a stand-alone tortuosity index, only an out-of-plane descriptor. Helix: ∫|τ| ds = L·b/(a²+b²). Ill-conditioned where κ → 0 because the binormal is undefined: the formula divides by |r′×r″|², so a planar sinusoid produces torsion spikes at each inflection that are pure noise. For a 3D inflection (binormal flip of π) the discrete TP_k jumps by ≈ π, so ΣTP_k partially counts Grisan-type twists.

5. **Total angle / Darboux magnitude ∫|ω| ds = ∫√(κ²+τ²) ds; Bullitt's discrete Σ√(IP²+TP²).** |ω| is the total angular speed of the Frenet frame. Rigid-motion invariant. Line: 0 (but TP is undefined on a line; implementation must zero it where IP is below a floor). Helix: L/√(a²+b²), strictly larger than K; Bullitt confirms SOAM rises with coil frequency where DM and ICM are flat. Planar curves: reduces to K except for TP ≈ π jumps at each inflection, which add π per inflection, so **SOAM mixes a curvature integral with an inflection count**. That makes it an implicit merge of SCC-type and Grisan-type information, but in an uncontrolled way: the π-per-inflection term is noise-driven when curvature is small. Still radius-blind for single arcs (same as K).

6. **Curvature-weighted arc/chord** (e.g., Grisan's per-turn arc/chord excess or ∫κ ds / C). Arc/chord of an arc of angle Θ is (Θ/2)/sin(Θ/2), independent of radius; the per-turn excess grows ≈ Θ²/24 (earlier report). Arc/chord fails the frequency test (Bullitt: DM constant 1.6 across sine frequencies) and is uncorrelated with haemodynamics (Kashyap p = 0.86) and so is a weak partner. Helmberger's arc/chord did correlate with mPAP in lung trees, so it is not useless as a biomarker, but its failure modes on synthetic curves are documented.

7. **Writhe Wr = (1/4π)∫∫ (r₁−r₂)·(dr₁×dr₂)/|r₁−r₂|³; average crossing number ACN = same with absolute value of the integrand.** Discrete: Klenin–Langowski or Levitt double sums over segment pairs, O(N²). Rigid-motion and scale invariant, dimensionless; writhe flips sign under reflection. For any **planar** curve the triple product is zero, so Wr = ACN = 0 on arcs, sinusoids and any rotated planar curve. For open curves writhe is not an integer and depends on how ends are treated. Helix: grows roughly with the number of turns and with the pitch angle. Hence writhe/ACN are blind to all in-plane tortuosity and only quantify 3D self-wrapping, which for a coronary running on a convex epicardial surface is expected to be small; they also carry an undesired dependence on how much of the heart the vessel wraps around (global shape, not local tortuosity). Not a fix for any weakness except, marginally, the helix blind spot. No vascular precedent was found.

8. **Fourier band power of deviation from a baseline.** Construct a baseline (chord line, or heavily smoothed centerline at scale σ_B), compute the deviation vector d(s) ⟂ baseline, take its two perpendicular components as a complex signal d₁ + i d₂ (rotation invariant after taking power), and report P(f) or band-integrated power per length. Line: 0. Wide arc vs tight bends: energy lands at low vs high spatial frequency, so **the spectrum separates them by construction and is radius/wavelength-aware**. Sinusoid: spectral line at 1/λ with power ∝ A² (monotone in A, no saturation; frequency read off the peak). Helix: d is a vector of constant length rotating once per pitch, so a single one-sided spectral line of power ∝ a² at 1/pitch (non-zero, and the sign of frequency gives handedness). Rotated planar curve: invariant if the power of both components is summed. White noise contributes a flat floor that can be excluded by band-limiting, which is the principled way to handle the 0.5 mm jitter. The curvature-spectrum variant (FFT of κ(s), Med Eng Phys 2011) inherits curvature's noise but is baseline-free. Weakness: output is a curve, not a scalar; collapsing to one number requires a pre-registered band, and short segments (< ~15 mm) give very few frequency bins.

9. **Scale-space tortuosity curves.** Compute any scalar (K/L, E/L, arc/chord, Grisan τ) after Gaussian smoothing of r(s) at σ ∈ {σ₁…σ_m}, giving a tortuosity-vs-scale curve. Small-σ end is noise-dominated; large-σ end drops to 0. The *area* under or *slope* of this curve is a multiscale scalar; it directly answers criterion 2 (stability over smoothing) by reporting, rather than hiding, the dependence. No 3D vascular paper doing exactly this was retrieved.

10. **Fractal dimension of a single centerline.** A smooth curve has box-counting dimension 1 at scales below its smallest bend radius; D > 1 appears only over a limited range of scales. A 50 mm coronary segment sampled at 0.5 mm spans at most two decades of box sizes, too few for a stable slope, and jitter inflates D at fine scales. Helmberger's FD (2.35) is a whole-tree space-filling measure and did not correlate with haemodynamics while arc/chord did. **Not recommended** for per-segment coronary tortuosity.

Which fix which known weakness of the earlier merge:
- C-shape / helix scored 0 by Grisan: fixed by K/L, E/L, SOAM total angle, Fourier band power (all non-zero on C and helix). Not fixed by writhe on C (zero, planar), partly by writhe on helix.
- SCC radius blindness: fixed by E/L, Q, Fourier/scale-space. Not by K, SOAM.
- SCC amplitude saturation: fixed by E/L and Fourier band power (∝ A²). Not by K, SOAM.
- Noise sensitivity: made worse by E, κ_d, torsion, SOAM torsion term; addressed structurally only by band-limited Fourier power or explicit scale-space reporting.

### Gaps
- The Bullitt 2003 full paper was read only via a PMC-derived summary; the exact spline smoothing and the sample sizes per clinical group should be checked with `paper-review` before SOAM results carry weight.
- Kashyap 2022 has no synthetic or noise test; no source here compares κ_a vs κ_r on helices or on arcs of different radius.
- Med Eng Phys 2011 curvature-spectrum paper and the CNSNS 2020 3D curvature–torsion aortic paper were abstract-only or title-only; their formulas, band choice and results are unknown.
- No source applying writhe or ACN to any vessel was found; the conclusion "no precedent" rests on one search.
- No 3D coronary paper using Fourier/wavelet deviation spectra or scale-space tortuosity curves was found.
- All synthetic-behaviour statements in Inferences are derivations and must be verified numerically.

---

## Q2. Which descriptors separate "one gentle big curve" from "many tight bends", which are radius-aware, and which are robust to centerline noise (reproducibility evidence)?

### Takeaway
Radius-aware separation comes from quantities that weight curvature super-linearly (bending energy, RMS curvature, Q ratio) or from frequency content (Fourier band power); linear curvature integrals (K, SCC, SOAM) and arc/chord are radius-blind per bend. Noise robustness runs the other way: each extra derivative or power of κ amplifies jitter, and the only direct reproducibility evidence in 3D vessels (Kjeldsberg 2021, carotid siphon) shows resampling step dominates everything, with torsion-based detection least stable.

### Cited Findings
- Kjeldsberg et al. 2021 (full text; carotid siphon): with Piccinelli's torsion-extrema bend detector, resampling parameter r from 0.02 to 0.2 changed the number of bends from 33 to 3; r < 0.1 was "considerably noisy, creating an undesired amount of short bends", recommended r = 0.1. Smoothing factor λ changed bend count only 7 to 8 (left) or 5 (right). — [Kjeldsberg 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- Kjeldsberg 2021: Piccinelli's torsion-based method had CV = 47 % for the first bend across segmentations and was described as "vulnerable to model smoothness and noise"; Bogunović's parallel-transport curvature-vector method had CV < 5 % for the superior bend but uses ICA-specific angle thresholds (45°, 60°, 45°, 110°). — [Kjeldsberg 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- Kashyap 2022 used very heavy preprocessing for curvature (Taubin smoothing plus 0.01 mm resampling) and did not report any reproducibility or jitter analysis. — [Kashyap 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Bullitt 2003 sampled at one-voxel intervals on a spline-fitted skeleton; no noise experiment in the retrieved summary. — [Bullitt 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- Helmberger 2014 explicitly did not test repeatability (radiation dose). — [Helmberger 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC3909124/)
- The earlier report derived a spurious turning-density bias of ≈ 3σ/ℓ² for Σθ/L under independent jitter σ (≈ 0.19 rad/mm at ℓ = 2 mm, 0.03 rad/mm at ℓ = 5 mm with σ = 0.25 mm), against a real signal near 0.08 mm⁻¹ (van Zandwijk 5 mm Menger curvature). — [earlier report citing van Zandwijk 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7165136/)

### Inferences
- **Separation ranking (derivation):** Fourier band power and scale-space curves > Q ratio ≈ E/L (radius-aware) > Grisan τ (separates via n, but 0 on single bends) > K/L, SCC, SOAM (separate only through length/total turning) > arc/chord (fails frequency) > writhe/ACN/total torsion (blind to planar shape).
- **Noise extension of the earlier derivation to bending energy (derivation, upper bound for independent jitter):** turning-angle noise has E[θ²] ≈ 12σ²/ℓ² (two perpendicular components, each second-difference variance 6σ²), so spurious E/L ≈ 12σ²/ℓ⁴. With σ = 0.25 mm: ≈ 0.047 mm⁻² at ℓ = 2 mm and ≈ 0.0012 mm⁻² at ℓ = 5 mm, against a real κ² near 0.0064 mm⁻² (κ ≈ 0.08 mm⁻¹). So bending energy is roughly 7× noise-dominated at ℓ = 2 mm but ≈ 20 % biased at ℓ = 5 mm; its ℓ-dependence (ℓ⁻⁴) is much steeper than K's (ℓ⁻²). Bending energy is only usable with ℓ or smoothing σ of several mm, which in turn caps the smallest resolvable bend radius near ℓ.
- **Torsion (derivation):** the binormal angle noise scales like (noise angle)/(signal angle), so where real θ is small, TP is essentially random in [0, π]. SOAM's torsion term and total torsion are therefore the least robust quantities here, consistent with Kjeldsberg's 47 % CV for the torsion-based bend detector.
- **Robust options:** (i) band-limited Fourier power, because jitter is spread over all frequencies and a band stopping at wavelength ≈ 4 to 5 mm excludes most of it; (ii) reporting tortuosity-vs-scale curves so the stability criterion is built in; (iii) using Q, which is a ratio and partly cancels multiplicative scale bias, although additive jitter bias in E does not cancel.
- The literature has **no ICC or test–retest data** for κ_a, κ_r, SOAM, writhe or spectral indices on coronary centerlines; criterion 3 (jitter ICC) and criterion 4 (reference vs CAS-Net centerline ICC) must be measured in-house.

### Gaps
- No coronary reproducibility study (inter-observer, inter-extractor, jitter) for any integral or spectral tortuosity metric was found in this pass.
- Real centerline error is spatially correlated; the σ/ℓ scalings above are upper bounds and need the in-house jitter test with correlated noise.
- The unit of Kjeldsberg's resampling parameter r (mm or relative) was not confirmed from the summary.

---

## Q3. Which natural pairings with a turn-count or Grisan-type index cover each other's blind spots?

### Takeaway
The strongest pairing is **Grisan-type turn structure + a radius-aware magnitude (bending energy per length or band-limited Fourier power)**, optionally with the Q ratio as a threshold-free stand-in for turn structure. SOAM already fuses curvature with a π-per-inflection term, but in an uncontrolled, noise-driven way; writhe is only worth adding as a separate out-of-plane descriptor.

### Cited Findings
- Bullitt's own three metrics were complementary: ICM (arc/chord × inflection count) detected AVM nidi and meandering vessels, SOAM detected tight coils where ICM failed, and DM failed frequency. No single metric covered all three abnormality types. — [Bullitt 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- Kashyap 2022 found curvature-based metrics outperforming arc/chord against haemodynamics in coronaries, with κ_a best, κ_r and κ_d close behind. — [Kashyap 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- The Med Eng Phys 2011 curvature-spectrum work argues a single scalar is insufficient to describe tortuosity (abstract-only). — [PubMed 21317017](https://pubmed.ncbi.nlm.nih.gov/21317017/)
- Bogunović-type parallel-transport curvature-vector rotation gave the most stable 3D bend segmentation (CV < 5 %) on carotid siphons, suggesting it as the twist detector if a Grisan-type split is used. — [Kjeldsberg 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)

### Inferences (derivations)
Candidate pairings, each with what it covers:

| Pairing | Grisan / turn index covers | Partner covers | Remaining blind spot |
|---|---|---|---|
| 3D Grisan τ + **E/L** (bending energy per length) | many-vs-one bend structure (per-turn arc/chord excess ≈ Θ²/24 still rises with turn angle) | C-shapes, helices, radius, amplitude without saturation | E is noise-heavy (ℓ⁻⁴); needs ℓ ≥ ~4 to 5 mm |
| 3D Grisan τ + **band-limited Fourier power** of deviation from smoothed baseline | discrete turn structure | radius/wavelength, amplitude (∝ A²), helices, explicit noise band | band and baseline scale must be pre-registered; short segments few bins |
| **K/L (SCC density) + Q ratio** (no turn segmentation at all) | K/L: magnitude of turning, sees C and helix | Q: concentration of bending into few tight bends (= 1 for arc and helix, > 1 for localised bends); radius-aware | Q ignores amplitude (needs K/L); Q undefined on line; E bias from jitter enters Q |
| Per-turn **bending energy inside Grisan's aggregator** (replace L_c/L_χ − 1 by E_turn·L_turn or ∫κ² over the turn) | segmentation into turns | radius-awareness per turn | still 0 when n = 1 because of (n−1)/n; drop that factor or add a C/helix term |
| SOAM (total angle) as a single merged index | implicit π per 3D inflection | curvature + torsion, helix-sensitive (Bullitt) | radius-blind; torsion term noise-dominated at small θ; not recommended over an explicit pair |
| Any of the above + **writhe/ACN** as a separate channel | nothing new in plane | 3D self-wrapping (helix) | zero on all planar shapes; global not local; no vascular precedent |

- Recommended shortlist for the thesis synthetic suite, in order: (1) E/L at pre-registered ℓ plus K/L, reported with a scale sweep; (2) Q = L·E/K² as a threshold-free "one wide vs many tight" index to test against Grisan τ directly, since both aim at the same property but Q has no twist detector, no floor at n = 1, and gives 1 (not 0) on C-shapes and helices; (3) band-limited Fourier deviation power as the multiscale check. Fractal dimension and writhe are not worth implementing as primary candidates.
- The C-shape definitional question from the earlier report reappears: Q scores a C-shape and a helix as minimally "concentrated" (Q = 1) but E/L and K/L score them as curved. Reporting a magnitude plus a concentration channel lets the thesis keep both readings rather than choosing one implicitly.

### Gaps
- None of these pairings has been tested on coronaries in the literature; all are new designs.
- The Q ratio is my derivation; I found no vascular source that uses (mean κ²)/(mean κ)² explicitly, although it is closely related to curvature-variability measures such as Kashyap's κ_d.
- No expert-ranking agreement data (criterion 7) exist for bending energy, Q or spectral indices in any 3D vascular bed found here.
