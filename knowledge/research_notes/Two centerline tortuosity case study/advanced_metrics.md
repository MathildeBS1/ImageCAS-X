# Advanced tortuosity descriptors on two RCAs (scans 662 and 518)

Evidence labels. **Check**: a number produced in this pass by `tortuosity/research/case_study/advanced.py` (rerun: `source env.sh; python -m tortuosity.research.case_study.advanced`, about 13 s on one login-node core). **Derivation**: mathematics written for this note. **Cited**: from a source; web sources were seen as search summaries or landing pages, not full-text reads. Earlier repo reports are cited by path.

Population: two training-split RCAs only (label 9 of `{id}.coronary_right_centerline.vtk`), longest labelled geodesic path (`tortuosity/vessels.py`, same loader as `research/simple/compute_simple.py`), oriented ostium to distal with the file's `start_points` (`research/unified/cohort.py:start_point`). The Disease column was not opened. Percentiles are against (a) the 560 training RCAs of `simple/simple_measures.csv` (baselines; this set includes both cases) or (b) the 150 RCAs of `unified/cohort_train150.csv` (BCS outputs, `orig` rows; neither 662 nor 518 is among those 150 ids, so these percentiles are out-of-sample placements). No cohort exists for the new descriptors, so their percentile is `null`.

Outputs (`/work3/s254124/imagecasx_results/tortuosity_research/case_study/`): `advanced_metrics.json` (58 entries per case, schema as specified), `advanced_pointwise.npz` (keys `{id}_xyz, _s, _k1, _k2, _twist_local, _turns, _tangent`, plus extras `{id}_ti10` (arc/chord minus 1 of the 10 mm window centred at each point, NaN near the ends), `{id}_signed_k` (curvature signed along the local bending axis), `warp_662_to_518` and `warp_662_to_518_anat` (SRVF warping paths, columns = fraction of arc length of 662, of 518)), `srvf_warp.png`, `advanced.log`.

**Curves and smoothing.** C0 = the delivered centerline (already skeletonised and Gaussian smoothed by the dataset, σ 0.5 mm, 5-vertex window; median raw vertex spacing 0.43 mm on 662) resampled at 0.25 mm, with no extra smoothing. C0 feeds everything that uses positions or chords only: multiscale arc/chord, writhe/ACN, box counting, SRVF (whose q = T is a first derivative, but is integrated, not differentiated again). C = C0 Gaussian smoothed in arc length at σ0 = 1.25 mm (`bishop.smooth`, end padding by point reflection) and resampled at 0.25 mm. C feeds everything that needs a second derivative (ψ, κ, tangent indicatrix, turns, persistence). The extra 1.25 mm is the BCS design value: the lowest σ0 that keeps iid-noise bias on energy ≤ 5 % while retaining ≥ 70 % of a radius 3 mm bend (`research_notes/Centerline tortuosity normal ranges/unified_2d3d_method.md`, Q3). The curvature scale space smooths C0 at σ ∈ {1.25, 2, 3, 4, 6, 8, 12} mm by design. `{id}_xyz` in the npz is C (433 points for 662, 412 for 518, LPS mm). ψ's global phase (free in a Bishop frame) is fixed so that Σψ² is real positive, i.e. k1 is the globally dominant bending direction; every reported scalar is phase-invariant.

## Q1. Baselines and the Bishop curvature spectrum (BCS): what does the energy decomposition add?

### Takeaway
The two RCAs are 9th vs 86th percentile on κ_a@5 but only 66th vs 79th on BCS energy kB, and the whole difference in kB for 662 is one ostial take-off turn: removing the first 5 mm drops 662's kB from 0.086 to 0.050 mm⁻¹ while 518 barely moves (0.096 to 0.090). The shape fraction that clearly separates them is f_twist: 0.15 (0.7th percentile) vs 0.46 (94.7th); 518 bends out of its local plane, 662 bends within one.

### Cited Findings
- BCS definitions (ψ = k1 + i k2 in a rotation-minimising frame; E = ∫|ψ|² ds, kB = √(E/L); course/wiggle split by DCT at half-power wavelength λc 20 mm; planar/twist split by g_W * ψ² at W 5 mm, exact and non-negative) and their verification on phantoms are in `research_notes/Centerline tortuosity normal ranges/unified_2d3d_method.md` (Q1, Q2), after [Bishop 1975](https://www.tandfonline.com/doi/abs/10.1080/00029890.1975.11993807) and [Wang et al. 2008](https://www.microsoft.com/en-us/research/publication/computation-rotation-minimizing-frames/).
- Cohort reference (150 training RCAs, σ0 1.25): kB median 0.076 [IQR 0.066, 0.092] mm⁻¹; f_wiggle@2 median 0.26; f_twist@2 median 0.25 [0.20, 0.30]; only f_twist and f_wiggle carry information beyond κ_a and length (rank R² 0.04 to 0.18) (same note, Q4).
- RCA baselines on 560 training scans: DM median 1.77, κ_a median 0.045 mm⁻¹ (`reports/Centerline tortuosity normal ranges.md`).

### Inferences
Values (check), 662 / 518, with percentile in brackets:
- Baseline arc/chord L/D (σ 1): 1.69 (42.6) / 1.96 (67.8). κ_a@5 (σ 1): 0.0336 (9.0) / 0.0647 (86.2) mm⁻¹.
- kB: 0.0857 (66.0) / 0.0956 (78.7) mm⁻¹. kB_course: 0.0648 (66.0) / 0.0756 (83.3). kB_wiggle: 0.0561 (62.7) / 0.0586 (70.7).
- f_wiggle@1.25: 0.43 (34.7) / 0.38 (13.3); @2 (pre-declared secondary): 0.30 (76.7) / 0.22 (22.7).
- f_twist@1.25: 0.15 (0.7) / 0.46 (94.7); @2 (pre-declared secondary): 0.12 (2.7) / 0.39 (92.7).
- **First 5 mm removed (sensitivity, check):** 662 kB 0.050, f_twist 0.34, f_wiggle 0.55; 518 kB 0.090, f_twist 0.47, f_wiggle 0.40. 662's pointwise energy: 74 % of E lies in the first third of the vessel, with an 88° turn over s 0 to 6.5 mm and peak κ 0.555 mm⁻¹ (radius 1.8 mm) at s 1.0 mm. The raw vertices there turn smoothly over about 4 mm, so it is in the delivered centerline, not a resampling artefact; whether it is the true ostial take-off or the extractor's entry from the aortic root cannot be decided from the centerline alone.
- **What the simple measures miss.** κ_a (mean turning, first absolute moment) scores 662 as very straight because the kink is short; kB (RMS, second moment) is dominated by it. The ratio kB / mean κ ("peakedness") makes this explicit: 1.56 for 662 vs 1.10 for 518, i.e. 662's bending is concentrated in one sharp spot, 518's is spread over the vessel (arc length with κ > 0.1 mm⁻¹, radius < 10 mm: 7.0 mm vs 33.3 mm). For the rendering: colour by |ψ| and 662 lights up only at the ostium; 518 lights up along its first 20 mm and again at s 61 to 80 mm.
- **f_twist has a spatial map.** `twist_local` = 1 − |g_W * ψ²| / (g_W * |ψ|²) per point. Energy-weighted mean: 662 0.16, 518 0.51. By thirds of arc length (energy share, energy-weighted twist): 662 (0.74, 0.05), (0.14, 0.43), (0.12, 0.50); 518 (0.44, 0.39), (0.30, 0.61), (0.26, 0.60). So 662 is non-planar only where it barely bends (runs with twist_local > 0.5 at s 13.5 to 25.5, 36 to 60 and 96.5 to 108 mm), while 518's mid and distal bends (the crux region) twist out of plane. 662's extreme-low f_twist percentile is partly the planar ostial kink dominating E; trimmed, it is 0.34, near the cohort's upper quartile at σ0 1.25 (cohort quantiles at @1.25 were not extracted for this note).

### Gaps
- No cohort percentile exists for the trimmed values, nor for any ostium-trimmed measure; whether ostial take-off kinks like 662's are common in the delivered centerlines is unmeasured and matters for every energy-type metric.

## Q2. Tangent indicatrix: how many different directions does each vessel point?

### Takeaway
518's direction of travel sweeps 512° in total against 341° for 662, covers 45 % more of the sphere of directions, and its tangents are six times less confined to a single great circle (out-of-plane variance 0.126 vs 0.019). 662 is essentially a planar C with a kink; 518 is a C that also winds out of its plane.

### Cited Findings
- The tangent indicatrix is the curve of unit tangents on S²; its length is the total curvature of the curve ([Encyclopedia of Mathematics](https://encyclopediaofmath.org/wiki/Tangent_indicatrix); [Wikipedia, Tangent indicatrix](https://en.wikipedia.org/wiki/Tangent_indicatrix)).
- Fenchel: a closed space curve has total curvature ≥ 2π, with equality only for plane convex curves ([Wikipedia, Fenchel's theorem](https://en.wikipedia.org/wiki/Fenchel%27s_theorem)). The coronaries are open, so no lower bound applies.

### Inferences
Definitions (derivation) on T = normalised ∂C/∂s, then values 662 / 518 (check):
- Indicatrix length Σ arccos(T_i·T_(i+1)) = ∫κ ds: 341.5° / 512.1°. Mean κ = this / L: 0.055 / 0.087 mm⁻¹ (the continuous analogue of κ_a, with ratio 1.6, close to κ_a's 1.9).
- Resultant |mean T| (= D/L for arc-length curves): 0.58 / 0.51.
- Smallest spherical cap containing all tangents (minimax half-angle, Nelder-Mead from 41 starts): 92.6° / 98.8°. Both exceed 90°: no hemisphere holds all directions of either RCA (each doubles back), so this does not discriminate RCAs.
- Sphere coverage (fraction of a 20 000-point Fibonacci grid within 10° of the indicatrix): 0.149 / 0.216.
- LPS octants of direction with ≥ 1 mm of arc: 5 / 6 of 8.
- Out-of-plane variance, smallest eigenvalue of ⟨T Tᵀ⟩: 0.019 / 0.126 (0 = all tangents on one great circle, i.e. a planar course; 1/3 = isotropic). Best-fit plane normals (LPS): 662 (−0.63, +0.66, +0.41), 518 (−0.60, +0.77, +0.24): both roughly the plane of the right AV groove, similar orientation, so the difference is spread about the plane, not which plane. For rendering: plot `{id}_tangent` on a sphere with that great circle; 662 hugs it, 518 leaves it.
- This is a global, W-free counterpart of f_twist, and it agrees in direction.

### Gaps
- No cohort distribution; the coverage threshold (10°) and octant rule (≥ 1 mm) are conventions chosen here, not from a source.

## Q3. Writhe and average crossing number: global 3D coiling

### Takeaway
Neither RCA coils: writhe is −0.009 and −0.006 (a three-turn helix gives ±1.48). The average crossing number differs almost threefold, 0.15 vs 0.41: in a random projection 518 overlaps itself far more often, which is what an angiographer sees as foreshortening and overlap.

### Cited Findings
- Writhe of a polygonal chain can be computed exactly segment pair by segment pair from the solid angle ([Klenin and Langowski 2000, Biopolymers 54:307](https://onlinelibrary.wiley.com/doi/10.1002/1097-0282(20001015)54:5%3C307::AID-BIP20%3E3.0.CO;2-Y)). Writhe and ACN are continuous functions of the chain coordinates for open and closed curves; ACN is the average number of unsigned crossings over all projection directions ([Sci. Rep. 2022](https://www.nature.com/articles/s41598-022-09924-0); [Panagiotou et al., arXiv 0907.3805](https://arxiv.org/pdf/0907.3805)). Open-curve writhe has endpoint subtleties treated in [Berger and Prior, "The writhe of open and closed curves"](https://empslocal.ex.ac.uk/people/staff/mab215/home_files/Writhe.pdf).

### Inferences
- Implementation (check): Klenin-Langowski segment-pair Ω on C0 at 1 mm segments, Wr = Σ_{i≠j} Ω/4π, ACN = Σ_{i≠j} |Ω|/4π, open curve, no closure. Validation: line and planar sine 0/0 exactly; right-handed helix (r 5, pitch 10 mm, 3 turns) Wr +1.48, left-handed −1.48, ACN 2.21 for both. The closed-helix approximation n(1 − sin α) would give 2.09; the open-curve end effect explains the difference (derivation, not checked further).
- 662 / 518: Wr −0.0094 / −0.0058; ACN 0.146 / 0.414.
- Interpretation: writhe measures net handedness of self-winding and is near zero for any curve that bends without coiling, so it is uninformative for RCAs (consistent with the earlier note's decision to reject writhe, `unified_2d3d_method.md` Q1). ACN is new information: it rises when distant parts of the vessel come close in direction-averaged projection, e.g. a C whose ends approach each other or a bend that folds back. It is a 3D, view-independent "projection overlap" index.

### Gaps
- ACN has no cohort reference and depends on how close distal and proximal parts come (i.e. on overall heart size), so length/heart-size confounding is untested.

## Q4. Multiscale arc/chord TI(Δ): at which scale is 518 more tortuous?

### Takeaway
518 exceeds 662 in mean TI at every scale, and the ratio grows with scale up to 20 mm (1.3× at 2 mm, 1.7× at 5, 2.6× at 10, 3.5× at 20, 2.5× at 40 mm). 518's excess tortuosity is in bends 10 to 40 mm long. At Δ ≤ 10 mm the single most tortuous window belongs to 662 (its ostial kink).

### Cited Findings
- Whole-vessel arc/chord is length- and truncation-confounded (ρ with length 0.69 on RCA; −30 % after a 20 mm distal cut) (`reports/Centerline tortuosity normal ranges.md`; `unified_2d3d_method.md` Q4).

### Inferences
Definition (derivation): TI(Δ) = mean over all start points s of Δ / |C0(s + Δ) − C0(s)| − 1, on the unsmoothed C0; also the maximum and the centre of the maximising window. Values 662 / 518 (check):

| Δ mm | mean 662 | mean 518 | max 662 (centre s) | max 518 (centre s) |
|-|-|-|-|-|
| 2 | 0.006 | 0.008 | 0.218 (1.0) | 0.053 (32.5) |
| 5 | 0.010 | 0.018 | 0.251 (2.5) | 0.056 (2.5) |
| 10 | 0.014 | 0.037 | 0.191 (5.0) | 0.087 (5.0) |
| 20 | 0.027 | 0.095 | 0.110 (10.0) | 0.185 (76.0) |
| 40 | 0.085 | 0.211 | 0.145 (70.0) | 0.350 (70.0) |
| whole (L/D − 1, C0) | 0.73 | 1.00 | | |

Both vessels' short-window maxima sit at the ostium (window starting at s = 0); 518's 20 mm maximum is the distal sweep around s 66 to 86 mm, the region of its 110° turn. Interpretation: a scale-resolved arc/chord separates "one sharp kink" (662 wins the max at Δ ≤ 10) from "sustained winding" (518 wins at every mean and at Δ ≥ 20). Mean TI(Δ) for small Δ behaves like Δ²⟨κ²⟩/24 (derivation, from the single-turn expansion in the earlier note), which is why it tracks bending energy at short scales and course shape at long scales. `{id}_ti10` gives the pointwise 10 mm map for rendering.

### Gaps
- No cohort for TI(Δ); length dependence at each Δ is unknown (expected to vanish for Δ ≪ L by construction, untested).

## Q5. Curvature scale space and peak persistence: how many bends are real?

### Takeaway
At fine scale both RCAs have 25 to 27 curvature peaks, so peak counting at σ 1.25 does not separate them (662 even has more prominent peaks: 11 vs 9 with persistence ≥ 0.05 mm⁻¹). As smoothing grows, 662 collapses to one bend by σ 4 mm while 518 keeps two inflections and two ≥ 45° turns up to σ 8 mm: 518's bends are long-lived, 662's are fine-scale ripples plus one kink.

### Cited Findings
- Mokhtarian's curvature and torsion scale-space images of space curves are built by Gaussian convolution in arc length over a continuum of scales, invariant to rotation, uniform scaling and translation ([Mokhtarian 1997, CVIU](https://www.sciencedirect.com/science/article/abs/pii/S1077314297905440); [Mokhtarian and Mackworth 1992](https://dl.acm.org/doi/10.1109/34.149591)).
- 0-dimensional persistence of a function's level-set filtration pairs each peak with the level at which it merges into a higher one; persistence diagrams are stable to small perturbations of the function ([Edelsbrunner and Morozov, Handbook ch. on persistent homology](https://www.csun.edu/~ctoth/Handbook/chap24.pdf); [Cohen-Steiner, Edelsbrunner, Harer, stability](https://math.uchicago.edu/~shmuel/AAT-readings/Data%20Analysis%20/Edelsbrunner,%20Harer,%20Stability.pdf); [peak-detection explainer](https://www.sthu.org/blog/13-perstopology-peakdetection/index.html)).

### Inferences
- CSS (check), per σ: (κ peaks > 0.02 mm⁻¹ with persistence ≥ 0.005, inflections, turns ≥ 45°).
  - 662: 1.25 (25, 26, 2); 2 (12, 2, 2); 3 (8, 2, 2); 4 (5, 0, 1); 6 (2, 0, 1); 8 (2, 0, 1); 12 (1, 0, 1).
  - 518: 1.25 (27, 10, 3); 2 (9, 5, 3); 3 (7, 2, 2); 4 (7, 2, 2); 6 (3, 2, 2); 8 (3, 1, 2); 12 (2, 0, 1).
- The persistence-0.005 filter was added after a first run counted numerical ripple in the nearly constant κ of heavily smoothed curves as peaks (27 and 55 "maxima" at σ 12); the filtered counts decrease monotonically with σ as CSS theory requires.
- 662's 26 inflections at σ 1.25 fall to 2 at σ 2: they are sign flips of near-zero curvature in straight stretches, not bends. Inflection counts at the dataset's own smoothing scale are therefore not a tortuosity signal.
- H0 persistence of κ(s) at σ0 1.25 (check): peaks with persistence ≥ 0.02 mm⁻¹: 19 / 18; ≥ 0.05: 11 / 9; total persistence 1.72 / 1.47 mm⁻¹. The persistence diagram is a fine-scale roughness descriptor and ranks these two cases opposite to κ_a; it adds a "sharpness" axis, not a tortuosity magnitude.
- For rendering: the bend lifetime (largest σ at which a ≥ 45° turn survives) is a natural colour: 518's two main turns survive to σ 8, 662's ostial kink alone survives to σ 12.

### Gaps
- Mokhtarian's space-curve CSS tracks torsion zero-crossings; torsion was not used here (noise-dominated on these centerlines, per `reports/Centerline tortuosity normal ranges.md` on SOAM). The 3D "inflection" used is the sign change of curvature along the local bending axis (Q6), not a published definition.

## Q6. Bend barcode: constant-sign turns in 3D

### Takeaway
Along the local bending axis, 518 has three turns ≥ 90° (157°, 131°, 110°) against none for 662 (largest 88°, the ostial kink). This is the clearest single visual contrast: 518 is a sequence of three large opposing sweeps; 662 is a kink followed by a gentle 67° sweep.

### Cited Findings
- Grisan's tortuosity uses turns of constant-sign curvature ([Grisan 2008](https://doi.org/10.1109/TMI.2007.904657), as recorded in `reports/Merged tortuosity methods for coronaries.md`); the earlier binormal-flip generalisation to 3D needed thresholds and failed (`unified_2d3d_method.md` Q1).

### Inferences
- Definition (derivation): local bending axis e^{iφ(s)} with φ = ½ unwrap(arg(g_W * ψ²)), W 5 mm (continuous, sign-free); signed curvature k_s = Re(ψ e^{−iφ}); turns = maximal intervals of constant sign of k_s; turn angle = ∫|ψ| ds over the interval. For a planar curve this is exactly Grisan's turn set (ψ real, φ constant). Stored as `{id}_turns` (start s, end s, angle deg) and `{id}_signed_k`.
- Turns ≥ 10° (check), [start, end, angle]: 662: [0, 6.5, 87.8], [24.0, 30.8, 18.0], [32.2, 46.0, 30.9], [51.8, 56.8, 14.0], [59.2, 79.0, 66.8], [81.2, 84.5, 10.5], [90.0, 92.5, 10.2], [94.8, 101.5, 18.8], [101.8, 108.0, 15.6]. 518: [0, 26.2, 157.2], [30.5, 36.2, 35.0], [36.5, 41.8, 26.2], [44.0, 69.0, 131.3], [69.2, 91.0, 110.4], [91.2, 94.2, 14.3], [96.5, 102.8, 17.0].
- Counts: all turns 26 / 11; ≥ 20°: 3 / 5; ≥ 45°: 2 / 3; ≥ 90°: 0 / 3. Mean length of turns ≥ 20°: 13.3 / 16.8 mm.
- Caveat: where the local axis rotates quickly (twisted regions), a single 3D bend can be split into two, as 518's [30.5, 36.2] and [36.5, 41.8] suggest.

### Gaps
- The W = 5 mm axis window is inherited from BCS, not tuned; turn boundaries in high-twist stretches depend on it.

## Q7. Elastic shape analysis (SRVF)

### Takeaway
Both RCAs are about equally far from a straight line in elastic shape space (0.80 vs 0.85 rad); SRVF distance to a line is a moment −2 (arc/chord-like) quantity and mostly restates L/D. The pairwise elastic distance is 0.46 rad after a 17° rotation and warping, down from 0.66 rad with neither; the warp is gentle and lies above the diagonal (518's features occur somewhat earlier in relative arc length, most between 20 % and 60 % of 662's length).

### Cited Findings
- In the SRV representation q = β′/√|β′| the elastic metric becomes L², reparametrisation acts by isometries, and unit-length curves live on the unit sphere of L² ([Srivastava, Klassen, Joshi, Jermyn 2011, PAMI 33(7)](https://www.semanticscholar.org/paper/Shape-Analysis-of-Elastic-Curves-in-Euclidean-Srivastava-Klassen/377415d1b8e328c7cf42cd5016dedcac09beb992)); optimal reparametrisation is found by dynamic programming ([Bruveris, "Optimal reparametrizations in the SRV framework", arXiv 1507.02728](https://arxiv.org/pdf/1507.02728)).
- SRVF distance to a line belongs to the TI (moment −2) family (`unified_2d3d_method.md` Q1).

### Inferences
- Implementation (check): C0 normalised to unit length, 200 samples, q = T scaled to unit L² norm; distance = arccos⟨q1, O (q2∘γ)√γ′⟩ with γ by DP (slopes dj/di, di, dj ≤ 6) alternating with Procrustes O ∈ SO(3), 6 iterations. Validation: self-distance and distance to a 90°-rotated copy are 0.000 after normalising q (the first run gave 0.033 because chord-sampled q had L² norm slightly below 1).
- Distance to a straight line has a closed form (derivation): orbit of a line q = e is {e√γ′}, and by Cauchy-Schwarz sup_γ ∫(q·e)√γ′ = √(∫(q·e)₊² dt), so d_elastic = arccos √(max_e ∫(T·e)₊² dt); without warping d_L2 = arccos |∫T dt| = arccos(D/L). Values: elastic 0.797 / 0.853; L2 0.954 / 1.047 rad. Line 0, planar sine 0.81, helix 1.03 in validation.
- Pairwise 662 vs 518: 0.464 (rotation 17.3° + warp), 0.511 (LPS frame, warp only), 0.664 (no rotation, no warp). Warping removes about 30 % of the raw mismatch; the rest is genuine shape difference (the out-of-plane winding and the sharp versus broad proximal turn). `srvf_warp.png` shows γ; the paths are in the npz.

### Gaps
- No cohort of pairwise distances, so 0.46 rad cannot yet be called large or small; a Karcher-mean RCA shape and each case's distance to it would give that scale (not done; out of the two-case scope).
- The DP is a small-neighbourhood grid DP of my own, not the reference `fdasrvf` implementation (not installed).

## Q8. Box-counting dimension

### Takeaway
Uninformative: 0.940 vs 0.938 with boxes 1 to 16 mm. A smooth 100 mm curve is one-dimensional at every resolvable scale, and at 8 to 16 mm the box count is limited by finite length, which pulls the slope below 1.

### Cited Findings
- None located specifically for coronary centerline fractal dimension in this pass.

### Inferences
- Check: box counts averaged over 20 random grid offsets, slope of log N against log(1/ε). Recommend dropping it for centerlines; it belongs to branching trees, not single trunks.

### Gaps
- No source was searched for vessel-tree fractal dimension; not pursued because the single-trunk result is degenerate.

## Q9. Synthesis for the rendering and for method development

### Takeaway
The two RCAs differ in three independent ways that simple measures conflate: (1) where bending sits (662 concentrated in one ostial kink, peakedness 1.56; 518 spread, 1.10), (2) planarity (f_twist 0.15 vs 0.46, tangent out-of-plane variance 0.019 vs 0.126, ACN 0.15 vs 0.41), (3) scale of the bends (518 exceeds 662 most at 10 to 40 mm windows, and its turns survive smoothing to σ 8 mm). κ_a at 5 mm happens to rank them in the "right" order, but kB nearly ties them because of the kink.

### Cited Findings
- κ_a@5 is the pre-declared primary and f_twist, f_wiggle the exploratory secondaries (`reports/Centerline tortuosity normal ranges.md`).

### Inferences
- Descriptors worth carrying forward (judgement): f_twist with its pointwise map (clear visual meaning, cohort-placed), peakedness kB/mean κ (cheap, explains κ_a vs kB disagreement), multiscale TI(Δ) mean at 10 and 20 mm (scale-resolved and length-robust by construction), the 3D bend barcode (counts ≥ 90° and the per-turn intervals), ACN (a view-independent overlap index). Not worth carrying: writhe (≈ 0 for bending without coiling), box dimension (degenerate), fine-scale peak or inflection counts (dominated by ripple), SRVF distance to a line (restates L/D).
- Method implication: an ostial take-off rule is needed before any energy-type metric (kB, persistence, max κ) is reported, since the first 5 mm alone moved 662's kB by 42 %.
- Suggested views: colour the 3D tube by |ψ| (where), by `twist_local` (which plane), by `ti10` (which scale); overlay the barcode as coloured arc intervals; tangent sphere with each case's best-fit great circle; `srvf_warp.png` for correspondence.

### Gaps
- Two cases are an illustration, not evidence. None of the new descriptors has a cohort distribution, reliability (jitter, truncation) or extractor-agreement check; those are the next steps before any of them could become a secondary.
