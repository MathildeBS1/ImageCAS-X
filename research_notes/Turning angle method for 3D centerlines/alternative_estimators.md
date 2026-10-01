# Alternative curvature / turning-angle estimators for noisy 3D centerlines, compared with the fixed-chord turning angle T_ℓ

Scope: estimators usable to turn a VMTK-style 3D polyline centerline (about 0.5 mm spacing, voxel-derived jitter) into one scalar per-vessel tortuosity score, compared with the thesis method T_ℓ = (1/L_c) Σ θ_j (chord respacing at ℓ, θ_j = angle between consecutive chords, L_c = n_chords × ℓ).

Local experiments referenced below were run with `exp.py` and `exp2.py` in the session scratchpad (`/tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/d8496b60-33b2-4d43-8527-4222c79b70c1/scratchpad/`), numpy/scipy 1.17.1 from the project venv. They are cited as "[local sim]". The scratchpad is ephemeral; if these numbers are to be reported, the scripts must be copied into the repo first. Set-up: curves resampled to 0.5 mm arc length; noise either white Gaussian per point (σ = 0.1 or 0.25 mm) or spatially correlated (σ = 0.25 mm, Gaussian correlation length 1 mm, closer to how real VMTK centerline jitter looks); 50 noise draws per cell; errors are relative to the analytic mean curvature.

## 1. Spline / smoothing-based approaches (smoothing spline, B-spline, Gaussian scale-space, Savitzky-Golay, VMTK Laplacian + finite differences)

### Takeaway
Every derivative-based method is a "smooth, then differentiate twice" estimator whose accuracy depends entirely on the smoothing scale. With enough smoothing (a Gaussian σ of about 3 mm, a heavily penalised smoothing spline, Savitzky-Golay with about 11 mm window) they match or slightly beat T_5mm on ranking vessels. With the smoothing that is usually used by default, they are much worse, because the second derivative amplifies noise. None is clearly better than T_ℓ for a scalar score; they mainly swap the chord length ℓ for another scale parameter (σ, λ, window, iterations) that is less interpretable.

### Cited Findings
- VMTK `vmtkcenterlinegeometry` computes curvature and torsion from the Frenet frame, with the derivatives "approximated using a simple finite difference scheme along the line", and the docs state "it is very likely that such derivatives will be affected by noise"; optional Laplacian smoothing is applied first (tutorial example: 100 iterations, relaxation factor 0.1). VMTK's own "tortuosity" output is the length / endpoint-distance ratio, not a curvature integral. — [VMTK Geometric Analysis tutorial (source md)](https://github.com/vmtk/vmtk.github.com/blob/master/tutorials/GeometricAnalysis.md); [vmtkcenterlinegeometry docs](http://www.vmtk.org/vmtkscripts/vmtkcenterlinegeometry.html)
- In an ICA bend-landmarking study, Piccinelli's scalar curvature κ = |r'×r''|/|r'|³ from VMTK-style derivatives was extremely sensitive to centerline resampling length: "mean of 33 bends detected for r=0.02, in contrast to 3 bends for r=0.2", whereas Bogunović's vector-curvature (parallel transport frame) method was relatively stable; Laplacian smoothing factor had little effect (around 6 bends, recommended λ ∈ [1.2, 1.5]) and iteration count was stable for N ∈ [20, 100], with more iterations over-smoothing. — [Automated landmarking of bends in vascular structures, PMC8626959](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- Bogunović et al. detect carotid siphon bends from the trajectory of the curvature vector expressed in the parallel transport frame. — [Bogunović et al., Med Image Anal 2012](https://www.sciencedirect.com/science/article/abs/pii/S136184151200028X)
- A cerebrovascular tortuosity study reports (per search snippet; full text not retrievable, blocked by reCAPTCHA) that methods based on discrete sampling are highly sensitive to noise, "particularly in calculating second derivatives", and therefore uses unit-speed polynomial spline fitting together with an indicator of spline fit quality. — [Measuring arterial tortuosity in the cerebrovascular system using TOF MRA, PMC11703313](https://pmc.ncbi.nlm.nih.gov/articles/PMC11703313/)
- A 2026 study smooths noisy analytic space curves with cubic splines in the Frenet-Serret frame and tests statistical stability of curvature and torsion under noise by Monte Carlo (search snippet only; full text returned HTTP 403). — [Axioms 15(5):365, 2026](https://www.mdpi.com/2075-1680/15/5/365)
- [local sim] Noise-free helices: all smoothing estimators are within about 1% of truth (Gaussian σ = 3 mm: +0.2 to +1.1%; spline λ = 50: about -1.2%). Under σ = 0.25 mm correlated noise, bias grows fast as the curve straightens (true κ = 0.08 → 0.02 /mm):
  - Gaussian σ = 1 mm: +58% → +422%
  - Gaussian σ = 2 mm: +8% → +104%
  - Gaussian σ = 3 mm: +2.4% → +22%
  - Savitzky-Golay (cubic, 11 mm): +0.5% → +63%
  - smoothing spline λ = 50: +1.1% → +38%
  - VMTK-like Laplacian (100 iterations, 0.1) + FD: +17% → +196%
  - T_ℓ at ℓ = 5 mm, for comparison: -0.8% → +72%. At ℓ = 8 mm: -6.9% → +4.7%.
- [local sim] Finite differences on the raw 0.5 mm polyline without smoothing are unusable: at σ = 0.1 mm white noise the bias is +900% to +3900%.
- [local sim, implementation pitfall] `scipy.ndimage.gaussian_filter1d(..., order=2)` applied directly to absolute coordinates gave +26% bias even on noise-free helices, because the sampled derivative kernel does not sum exactly to zero and so leaks the large linear coordinate trend. Smoothing with order=0 and then taking `np.gradient` removed this bias. Any Gaussian-derivative implementation should be validated on a synthetic helix first.

### Inferences
- The known amplification of noise by the second derivative (noise variance in κ scales roughly with σ²/s⁴ for smoothing scale s) is why every smoothing method needs a scale of a few mm on 0.5 mm-jitter centerlines. That is the same scale regime as ℓ = 5 mm. Changing the estimator does not remove the need to choose a scale.
- VMTK's default pipeline (Laplacian smoothing + FD on the native spacing) is resolution-dependent: its effective scale depends on point spacing × √iterations. That makes it a poor reference for a thesis that wants a scale stated in mm.
- The spline curvature κ = |r'×r''|/|r'|³ is exact only if the spline is the true curve. The smoothing parameter (λ or s) is usually tuned by cross-validation or an assumed noise level, which is less transparent than "ℓ = 5 mm".

### Gaps
- No full-text quantitative numbers retrieved from the 2026 Axioms paper or the TOF-MRA tortuosity paper (access blocked).
- Did not locate a coronary-specific paper benchmarking spline curvature against discrete turning angles on CCTA centerlines.

## 2. Discrete estimators (turning angle over edge or dual length, Menger curvature, osculating circle, digital-geometry tangent estimators)

### Takeaway
On a polyline respaced to equal steps, the discrete estimators (turning angle / chord, turning angle / arc, Menger) differ from one another only by O((κℓ)²) terms, which are below 1% for coronary κ at ℓ = 5 mm. Their noise behaviour is set almost entirely by the step ℓ, not by which formula is used. Digital-geometry estimators (λ-MST, maximal segments, integral invariants) have multigrid-convergence proofs, but those proofs are for boundaries of digitised shapes on a grid (a staircase curve at grid step h). They do not apply to a Voronoi-derived, sub-voxel VMTK polyline, so they are not a practical upgrade here.

### Cited Findings
- Discrete curvature of a polygon has several inequivalent definitions: 2 sin(θ/2)/L, 2 tan(θ/2)/L, θ/L, and others. Each preserves a different smooth property. For example, one exactly preserves total curvature and another preserves the centre of mass under curve-shortening flow. There is no single "correct" discrete curvature. — [Vouga, Lectures in DDG 1: Plane curves](https://www.cs.utexas.edu/~evouga/uploads/4/5/6/8/45689883/notes1.pdf); [Crane, Discrete Differential Geometry course](https://brickisland.net/ddg-web/); [Discrete curvature, arXiv 2502.09353](https://arxiv.org/pdf/2502.09353)
- λ-MST tangent estimation (Lachaud, Vialard, de Vieilleville) is built from maximal digital straight segments, is proved multigrid convergent for convex shapes with C² boundary, with average convergence speed O(h^{2/3}), and runs in linear time. 3D extensions (combining 2D maximal segments, or filtered 3D maximal segments) are also multigrid convergent toward the 3D tangent. — [Fast, accurate and convergent tangent estimation on digital contours (IVC 2007)](https://www.sciencedirect.com/science/article/abs/pii/S0262885606003040); [Tangent estimation along 3D digital curves](https://www.researchgate.net/publication/261157693_Tangent_estimation_along_3D_digital_curves); [Convex shapes and convergence speed of discrete tangent estimators, arXiv 0906.3089](https://arxiv.org/pdf/0906.3089)
- Kerautret & Lachaud's Global Min-Curvature estimator selects the most probable shape consistent with tangent bounds from maximal digital straight segments. It is adapted to noise by replacing them with maximal blurred segments. — [Kerautret & Lachaud, Pattern Recognition 2009](https://www.sciencedirect.com/science/article/abs/pii/S0031320308004755)
- Coeurjolly, Lachaud and Levallois' integral-invariant estimators (ball of radius r intersected with the shape; volume or covariance of the intersection gives curvature) are proved multigrid convergent. — [Multigrid Convergent Curvature Estimator (DGCI 2013)](https://link.springer.com/chapter/10.1007/978-3-642-37067-0_34); [Robust and Convergent Curvature and Normal Estimators with Digital Integral Invariants](https://link.springer.com/chapter/10.1007/978-3-319-58002-9_9); [Multigrid convergent principal curvature estimators, CVIU 2014](https://www.sciencedirect.com/science/article/abs/pii/S1077314214001003)
- Comparative studies of 2D digital curvature estimators exist, e.g. Kerautret, Lachaud & Naegel on perfect and noisy shapes, and a 3D curvature and torsion estimator paper. Their full texts could not be retrieved here. — [Comparison of discrete curvature estimators and application to corner detection (ISVC 2008)](https://link.springer.com/chapter/10.1007/978-3-540-89639-5_68); [Curvature and Torsion Estimators for 3D Curves](https://www.researchgate.net/publication/29615553_Curvature_and_Torsion_Estimators_for_3D_Curves)
- [local sim] Estimators at step 5 mm, error vs truth (noise-free / σ = 0.25 correlated), for the κ = 0.08 and κ = 0.02 /mm helices:
  - chord-respaced turning angle T_5: -4.4 / -0.8% and -4.6 / +72%
  - arc-length-resampled turning angle / arc: -4.4 / -0.6% and -4.6 / +80%
  - Menger (circumcircle through three points 5 mm apart): -0.8 / +3.9% and -0.3 / +84%
  - The formulas are nearly identical; noise dominates.
- [local sim] Under white σ = 0.25 mm noise, arc-length resampling (which linearly interpolates the noisy polyline) was noticeably worse than chord respacing at the same ℓ: +91% vs +14% on the κ = 0.032 helix, and +191% vs +47% on κ = 0.02. Under correlated noise the gap shrank (+31% vs +26%; +80% vs +72%).

### Inferences
- For a circle, a chord of length ℓ subtends turning angle θ = 2 arcsin(κℓ/2), so θ/ℓ = κ (1 + (κℓ)²/24 + …). T_ℓ is therefore a consistent estimator of κ as ℓ → 0 on smooth curves, with relative bias about (κℓ)²/24. That is 0.4% at κ = 0.1 /mm, ℓ = 5 mm, and 4% even at a tight 5 mm radius of curvature. Menger curvature is exactly 2 sin θ / |p_{i+1} - p_{i-1}| = 1/R_circumcircle, which is exact on circles; that exactness only matters at κℓ near 1. (Derived here; Menger identity is standard trigonometry.)
- "Osculating circle fitting over a window" is Menger curvature generalised to least squares over more points. It has the same scale role as ℓ and was not simulated separately.
- Arc-length resampling vs chord respacing: on clean curves they are equivalent to O((κℓ)²). On noisy curves the chord version is more robust because it places vertices where the polyline first crosses a sphere of radius ℓ, and that position depends little on small wiggles. Arc length itself is inflated by jitter, so arc-parameter resampling moves vertices by accumulated noise length.

### Gaps
- Could not retrieve quantitative error tables from the digital-geometry comparison papers.
- No source found that applies λ-MST or integral invariants to VMTK-type (non-grid) vessel centerlines.

## 3. The role of scale (low-pass behaviour of ℓ, multi-scale reporting, choice and justification of scale)

### Takeaway
ℓ is a scale parameter, but chord respacing is a *sampling* operation, not a low-pass filter. It removes noise at scales below ℓ, but it aliases oscillations near ℓ, so T_ℓ can be non-monotone in ℓ. A Gaussian smoother does not show this aliasing. Reporting one ℓ is defensible if the thesis (a) justifies ℓ against the noise floor and the anatomical scale of interest, (b) shows a sensitivity curve over several ℓ, and (c) does not describe T_ℓ as "a low-pass filter".

### Cited Findings
- Bend counts from VMTK-style scalar curvature ranged from 3 to 33 depending on resampling length alone, showing that scale choice can dominate vessel geometry results. — [PMC8626959](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- Integral-invariant estimators make the scale explicit as a ball radius r and prove convergence when r shrinks at a specified rate with grid step h (Coeurjolly/Lachaud/Levallois). This is the digital-geometry template for a principled scale choice. — [DGCI 2013](https://link.springer.com/chapter/10.1007/978-3-642-37067-0_34); [Parameter-Free and Multigrid Convergent Digital Curvature Estimators](https://link.springer.com/chapter/10.1007/978-3-319-09955-2_14)
- [local sim] Population of 150 random smooth 100 mm curves (true mean κ 0.021 to 0.218 /mm, median 0.096), σ = 0.25 mm correlated noise:

  | estimator | Spearman ρ vs truth (clean) | ρ vs truth (noisy) | median bias (noisy) | test-retest ρ (two noise draws) |
  |---|---|---|---|---|
  | chord ℓ = 2 mm | 0.999 | 0.903 | +66% | 0.847 |
  | chord ℓ = 3 mm | 0.998 | 0.977 | +23% | 0.959 |
  | chord ℓ = 5 mm | 0.986 | 0.985 | -4.0% | 0.991 |
  | chord ℓ = 5 mm, (n-1) norm | 0.987 | 0.982 | -0.9% | 0.988 |
  | chord ℓ = 8 mm | 0.869 | 0.857 | -25% | 0.984 |
  | arc ℓ = 5 mm | 0.988 | 0.984 | -3.3% | 0.987 |
  | Menger 5 mm | 0.989 | 0.978 | -1.3% | 0.989 |
  | Gaussian σ = 2 mm | 0.990 | 0.987 | +5.5% | 0.994 |
  | Gaussian σ = 3 mm | 0.957 | 0.962 | -6.3% | 0.997 |
  | Savitzky-Golay 11 mm | 0.986 | 0.986 | -7.3% | 0.994 |
  | smoothing spline λ = 50 | 0.976 | 0.980 | +1.8% | 0.995 |
  | Laplacian 100 × 0.1 + FD | 0.996 | 0.985 | +16% | 0.987 |

  At a well-chosen scale, all methods rank vessels about equally well (ρ ≈ 0.98 to 0.99). Too small a scale loses to noise, and too large a scale (ℓ = 8, σ = 3) loses real curvature.
- [local sim, aliasing] Arc of radius 40 mm plus a 1 mm-amplitude z-wiggle of 8 mm wavelength (true mean κ 0.310 /mm; arc alone 0.025):
  - T_ℓ for ℓ = 1, 2, 3, 4, 5, 6, 8, 10 mm = 0.285, 0.264, 0.215, **0.025**, **0.100**, 0.046, 0.024, 0.026. This is non-monotone: at ℓ = 4 mm (half the wavelength) the chords "see" no wiggle, and at 5 mm part of it returns.
  - Gaussian σ = 1, 2, 3, 5 mm gives 0.251, 0.139, 0.051, 0.025, which decreases monotonically.

### Inferences
- Choosing ℓ = 5 mm is empirically near the sweet spot for 0.25 mm-scale jitter, in both bias and test-retest reliability. The thesis should justify this with its own noise estimate (e.g., curvature of repeated or perturbed centerline extractions) rather than by assertion.
- Because chord respacing aliases, T_ℓ at a single ℓ can misrank vessels whose tortuosity has a dominant spatial period close to ℓ or 2ℓ. For coronary arteries, cardiac-surface loops have wavelengths of centimetres, so this is probably rare at ℓ = 5 mm. Still, a sensitivity plot of T_ℓ against ℓ (e.g., 3 to 8 mm) per vessel is cheap insurance and answers the "why 5 mm" question.
- A cleaner "low-pass" interpretation would come from Gaussian-smoothing the centerline at σ and then taking the turning angle at fine spacing (or mean κ). This is the scale-space formulation. It is monotone in σ, so it gives a proper multi-scale curve.

### Gaps
- Did not retrieve Lindeberg scale-space papers on automatic scale selection for 1D curvature. No citable coronary paper justifying a specific chord length was found in this search.

## 4. Unsigned 3D turning angle, total curvature theory (Fenchel, Fáry-Milnor, Milnor's inscribed-polygon definition), torsion

### Takeaway
Σθ_j over an inscribed polygon is exactly Milnor's total curvature of that polygon, and it is a lower bound on the total curvature of the curve it is inscribed in. So T_ℓ is theoretically well founded as "mean absolute curvature at resolution ℓ" for a smooth true curve. However, the polygon is inscribed in the *noisy* centerline, so Σθ is bounded above by the noisy curve's total curvature, which can be large. The unsigned 3D angle is the length of the tantrix (tangent indicatrix) path, so it mixes in-plane bending and out-of-plane (torsional) turning. It does not separate curvature from torsion; torsion needs third derivatives and is much noisier.

### Cited Findings
- Sullivan: the turning angle at an interior polygon vertex is φ ∈ [0, π] between consecutive oriented edge tangents; "TC(P) is simply the sum of the turning angles at all interior vertices"; "The total curvature of P is the length of its tantrix in S^{d-1}". — [Sullivan, Curves of Finite Total Curvature, arXiv math/0606007, §2](https://arxiv.org/abs/math/0606007)
- Lemma 2.1 (Milnor): deleting a vertex never increases total curvature. Corollary 2.2: if P′ is inscribed in P then TC(P′) ≤ TC(P). Definition: TC(γ) := sup over inscribed polygons P < γ of TC(P). — [Sullivan §2](https://arxiv.org/abs/math/0606007)
- Fenchel's theorem: any closed curve in E^d has total curvature at least 2π (Theorem 2.4 in Sullivan). Fáry-Milnor: a knotted curve has total curvature > 4π. — [Sullivan](https://arxiv.org/abs/math/0606007); [Fáry-Milnor theorem](https://en.wikipedia.org/wiki/Fary-Milnor_theorem)
- VMTK's torsion depends on third derivatives, making it the most noise-sensitive of its outputs. — [VMTK Geometric Analysis](https://github.com/vmtk/vmtk.github.com/blob/master/tutorials/GeometricAnalysis.md)
- [local sim] On one noisy random curve, Σθ over chord polygons fell monotonically with ℓ: 34.4, 30.9, 22.1, 17.1, 12.6, 10.9 rad for ℓ = 0.5, 1, 2, 3, 5, 8 mm. Each chord polygon has its vertices on the input polyline, so it is inscribed and Milnor's bound applies. The polygons at different ℓ are not nested in each other, so strict monotonicity across ℓ is not guaranteed, but it held here.

### Inferences
- The accurate one-line claim is: "Σθ_j is Milnor's total curvature of a polygon inscribed at chord ℓ; dividing by nℓ gives mean absolute curvature at resolution ℓ, which converges to ∫|κ|ds / L for smooth curves as ℓ → 0." In 3D, "absolute curvature" is automatically unsigned (κ ≥ 0), so "absolute" is redundant but harmless.
- Fenchel and Fáry-Milnor apply to closed curves. For open vessel segments they give no lower bound, so they are background, not a validation.
- Torsion as a separate scalar would need much heavier smoothing. If the thesis wants to separate planar bending from out-of-plane twisting, a cheap discrete option is the dihedral angle between consecutive chord-pair planes at the same ℓ. It is still noisy when θ is small, because the plane is ill-defined for nearly collinear chords. (Inference; not simulated.)

### Gaps
- No source found that quantifies how the 3D unsigned turning angle decomposes into curvature and torsion contributions for real coronary centerlines.

## 5. Robust angle computation (atan2 vs arccos) and a length-normalisation bias in T_ℓ

### Takeaway
Use θ = atan2(|a×b|, a·b). arccos of a clipped normalised dot product loses precision below about 1e-7 rad in float64 and about 1e-3 rad in float32. That is negligible for coronary angles at ℓ = 5 mm in float64, but free to fix. A more consequential issue: dividing n-1 turning angles by n·ℓ biases T_ℓ low by 1/n = ℓ/L. That is a vessel-length-dependent bias, and it confounds comparisons between short and long vessels.

### Cited Findings
- [local sim] For true angles 1e-3, 1e-5, 1e-7, 1e-8 rad in float64, arccos gave 1.000e-3, 1.000e-5, 9.996e-8, **0** and atan2 gave exact values. In float32 at 1e-3 rad, arccos gave 9.77e-4 (-2.3%) and atan2 gave 1.000e-3.
- [local sim] Noise-free helices: T_ℓ with L_c = n·ℓ underestimated by -1.7% (ℓ = 2), -4.4% (ℓ = 5), -7.5% (ℓ = 8) on 120 mm curves regardless of κ. Normalising by (n-1)·ℓ (the length between the first and last angle vertices) reduced the ℓ = 5 bias to -0.0 to -0.3%.

### Inferences
- The -ℓ/L bias is -4% on a 120 mm RCA but about -17% on a 30 mm branch at ℓ = 5 mm. It varies systematically by vessel type, so it can create spurious between-vessel differences. The fix is to divide by (n-1)ℓ, i.e., the arc between the first and last vertex that carries an angle. The dropped final partial chord (length < ℓ) is a further small length-dependent effect worth stating.
- atan2 is also the standard recommendation for well-conditioned angles between vectors. It avoids clipping, and it handles near-π reversals better than arccos. Reversals do not occur on centerlines, but could appear if a centerline doubles back at a branch artefact.

### Gaps
- No external citation located for the atan2 vs arccos numerical-conditioning point in this session. It is supported by the local float64/float32 test only; a numerical-analysis reference (e.g., Kahan's notes on angle computation) should be added if it goes into the thesis.

## Overall recommendation-ready comparison (for the report writer)

- No alternative is clearly better than chord-respaced turning angle for a scalar per-vessel score. At matched effective scale (ℓ ≈ 5 mm ≈ Gaussian σ 2 to 3 mm ≈ SG 11 mm ≈ spline λ ≈ 50 on 0.5 mm spacing), Spearman ρ with true mean curvature is 0.96 to 0.99 for all methods, and test-retest ρ is 0.99 [local sim]. Smoothing-based methods have slightly higher test-retest ρ (0.994 to 0.997 vs 0.991), at the cost of a less interpretable scale parameter and implementation pitfalls (kernel leakage, end effects, spline λ tuning).
- Advantages of T_ℓ: the scale is stated in mm; it is grounded in Milnor/Sullivan total-curvature theory; it has no derivative estimation; and chord respacing is more robust to white jitter than arc-length resampling.
- Weaknesses of T_ℓ to fix or disclose: (1) the (n-1)/n length bias (fix with (n-1)ℓ normalisation); (2) aliasing, i.e., T_ℓ is not a low-pass filter and can be non-monotone in ℓ (report a sensitivity curve over ℓ ∈ {3, 4, 5, 6, 8} mm); (3) positive noise bias on near-straight vessels, which grows as true κ falls (+72% at κ = 0.02 /mm with 0.25 mm correlated jitter at ℓ = 5 mm) and compresses the low end of the scale; (4) use atan2.
- If a second method is wanted as a robustness check, the most defensible is Gaussian scale-space smoothing of the centerline along arc length (σ ≈ 2 to 3 mm), then mean κ or turning angle at fine spacing. It is monotone in scale, with a standard scale-space interpretation. VMTK's default Laplacian + FD pipeline is the least suitable, because its scale is resolution-dependent and it showed the largest noise bias at matched ranking performance.
