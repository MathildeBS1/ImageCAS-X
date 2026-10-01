# Numerics and code of the 3D turning-angle score T_l

Scope: `tortuosity/merged.py` (`chord_resample`, `_turns`, `scc_density`), how `run_merged_tests.py cohort` and `scripts/tortuosity_deciles.py` produce the thesis numbers, and the description in `thesis/week5/rca_tortuosity.tex` (lines 95 to 123). All experiments were run on the login node (CPU, float64) with scratch scripts `synth.py`, `real.py`, `dirn.py` in the session scratchpad; none of them edits the repository. "Code" below means `scc_density(P, 5) * pi`, which is exactly the thesis T_5 (checked: median of `scc_5 * pi` over the 560 training RCAs in `/work3/s254124/imagecasx_results/tortuosity_merged/train_vessels.csv` is 0.0476, 10th/90th percentiles 0.0361/0.0743, matching the thesis 0.048, 0.036, 0.074).

## 1. Does the code match the four described steps, and is the chord respacing correct?

### Takeaway
Mostly yes, and the sphere-polyline intersection is correct (it takes the first exit from the ball of radius l, never a backward or later intersection). Three real mismatches with the text: (a) the direction of respacing is arbitrary per vessel, not a chosen end; (b) the code divides by pi and the plotting script multiplies it back, while the thesis says the division is left out; (c) the normaliser counts one chord more than the angles cover, which biases every score down by (n-1)/n (about 5% at l = 5 mm) and in a length-dependent way.

### Cited Findings (code reading, file:line)
- Step 1, `chord_resample` (`tortuosity/merged.py:13-30`): from the current vertex `cur` it finds the first later input point `P[i+1+j]` with Euclidean distance >= l (`np.argmax(hit)`, line 21). The crossing lies on the segment from `a` (`cur` itself when j = 0, otherwise `P[i+j]`, which is still inside the ball) to `b = P[i+1+j]` (outside or on the sphere). It solves |a + t v - cur|^2 = l^2 (A t^2 + B t + C = 0, lines 24-26) and takes the larger root. Because `a` is inside the ball (C <= 0) and `b` is outside, exactly one root lies in [0, 1] and it is the larger one; the clip to [0, 1] (line 27) only guards rounding. Since a straight segment whose endpoints are both inside a ball stays inside it (convexity), the first input vertex outside the ball marks the first place the polyline leaves it. So the new vertex is the first exit along the curve; earlier or backward intersections cannot be chosen, and later re-entries and exits in a tight loop are ignored. No division by zero is possible: `v` is non-zero because `a` is strictly inside and `b` is on or outside the sphere.
- The loop stops when no remaining input point is >= l away (`break`, line 20), so the tail is dropped. On 120 training RCAs the dropped tail was median 2.55 mm of arc, max 4.92 mm (`real.py`).
- Steps 2-3, `_turns` (lines 33-37): chord vectors by `np.diff`, normalised, dot product clipped to [-1, 1], `np.arccos`. This is the thesis Equation (turn) applied to unit chords.
- Step 4, `scc_density` (lines 40-45): `th.sum() / (np.pi * l * (len(V) - 1))`. `len(V) - 1` is the number of chords n; there are only n - 1 angles. The docstring (line 4) and `scripts/tortuosity_deciles.py:7-10` describe the score as "over (pi * L)" and "kappa_a / pi"; `tortuosity_deciles.py:94` then plots `df.scc_5 * np.pi` "without the /pi". The thesis text (line 122-123) says the division by pi is left out. The numbers agree; the code and text do not.
- Walk direction: `vessels.longest_path` (`tortuosity/vessels.py`) returns the longest geodesic from the farther of two double-sweep Dijkstra endpoints, so which end comes first is an accident of the graph. `run_merged_tests.cohort` passes that path straight to `scc_density`. Only `tortuosity_deciles.py:rca()` reorients to ostium-first, and only for drawing. On 120 training RCAs the path started at the ostium in 61 cases (`real.py`). The thesis says "starting at one end" (line 99), which is literally true but hides that the end differs between vessels.
- Input points are cast to float64 in `vessels.read`, so all arithmetic is double precision.

### Inferences
- The respacing algorithm itself is sound and is the standard "first exit of a sphere of radius l" chord walk. The design choice to take the first exit is the right one: taking the nearest-in-index intersection after a re-entry would skip vessel.
- In a loop whose diameter is below about l, the polyline never leaves the ball, the loop is stepped over, and its turning is invisible. The real data show this happens: the arc between consecutive chord vertices was median 1.047 l, 99th percentile 1.39 l, and at most 2.29 l (a single 5 mm chord standing in for 11.4 mm of vessel). This is a scale property, not a bug, but it means T_l is a lower bound on turning in tightly looped RCAs, which the thesis flags as frequent in the high group (ostial loops in scans 930 and 552).

### Gaps
- Not checked whether any RCA polyline contains duplicated consecutive points or backtracks (a reversal of more than 90 degrees inside one input step); the chord walk would still work but an input backtrack of more than l would create a near-180 degree turn.

## 2. arccos of a dot product vs atan2(|a x b|, a.b)

### Takeaway
arccos is ill-conditioned near 0 but the effect is irrelevant here: in float64 the per-angle difference between the two on the real RCAs is at most 4.3e-14 rad and T_5 is identical to 4 significant figures. In float32 arccos would cost about 5e-6 rad at 0.01 rad and a 5e-4 rad floor, still far below the RCA angles (median about 14 degrees per 5 mm chord). atan2 is the better habit and a one-line change, but it changes no result.

### Cited Findings
- Kahan recommends an arctangent form over arccos because rounding can push the dot product outside [-1, 1] and near-parallel vectors lose accuracy; the stable form is theta = 2 atan2(|| |v| u - |u| v ||, || |v| u + |u| v ||) — [J. W. Walker, Computing Angle Between Vectors](https://www.jwwalker.com/pages/angle-between-vectors.html); [PyTorch issue 59194](https://github.com/pytorch/pytorch/issues/59194); [Possibly Wrong, Computing the angle between two vectors](https://possiblywrong.wordpress.com/2020/07/17/computing-the-angle-between-two-vectors/) (these secondary sources cite Kahan, "How Futile are Mindless Assessments of Roundoff in Floating-Point Computation?"; the primary PDF was not fetched).
- The arccos formulas behave poorly for nearly parallel vectors and the arctangent formulas are the most consistently accurate — [Possibly Wrong](https://possiblywrong.wordpress.com/2020/07/17/computing-the-angle-between-two-vectors/).
- Own measurement (`synth.py`, 2000 random 3D orientations per row, 5 mm steps, absolute error in rad, median / max):

| theta (rad) | float64 arccos | float64 atan2 | float32 arccos | float32 atan2 |
|---|---|---|---|---|
| 1e-2 | 9.7e-15 / 3.2e-14 | 2.4e-17 / 1.9e-16 | 5.1e-6 / 1.7e-5 | 1.1e-8 / 7.5e-8 |
| 1e-3 | 1.0e-13 / 3.4e-13 | 2.3e-17 / 1.7e-16 | 3.6e-5 / 1.5e-4 | 1.1e-8 / 7.5e-8 |
| 1e-4 | 8.5e-13 / 3.1e-12 | 2.4e-17 / 1.9e-16 | 1.0e-4 / 5.0e-4 | 1.1e-8 / 8.7e-8 |
| 1e-6 | 6.7e-11 / 2.9e-10 | 2.2e-17 / 1.9e-16 | 1.0e-6 / 4.9e-4 | 1.0e-8 / 8.1e-8 |

  The float32 arccos floor of about 5e-4 rad matches the theory: theta about sqrt(2(1 - c)), so an error of one float32 ulp in c (6e-8) gives sqrt(1.2e-7) = 3.5e-4 rad. In float64 the floor is about 1.5e-8 rad.
- On 120 real RCAs at l = 5 mm, `atan2` and the code's clipped `arccos` gave max per-angle difference 4.3e-14 rad and Spearman 1.0000 between scores (`real.py`).

### Inferences
- The clip to [-1, 1] in `_turns` is necessary and sufficient for arccos here (after normalisation |u| = 1 +- few ulp). Its side effect, that two exactly parallel chords can give 0 or about 1.5e-8 rad, is negligible against a floor of any real signal.
- If the code is ever moved to GPU/float32 or to per-point (0.47 mm) steps where angles are small, switch to atan2.

### Gaps
- Kahan's original paper not read in full; its content is taken from the three secondary sources above, which agree.

## 3. Is sum(theta) / L_c a consistent estimator of mean absolute curvature?

### Takeaway
The numerator is sound: the sum of turning angles is the discrete total curvature, and for an inscribed polygon it is at most the curve's total curvature, converging to it as the chord shrinks (Milnor, Sullivan). On a circle it is exact per unit arc. The biases come from the denominator: (a) dividing by chord length instead of arc length inflates theta/l by about l^2/(24 R^2) (under 1.1% for R >= 10 mm at l = 5); (b) dividing by n chords when only n - 1 angles exist deflates by (n-1)/n, about 5% at l = 5 mm for a median RCA and 3.5 to 7% across the cohort's range of lengths. The second bias dominates in practice and is length dependent. Menger (2 sin(theta/2)/l) is exact on circles; 2 tan(theta/2)/l overestimates. In the cohort the choice between theta and 2 sin(theta/2) changes nothing (Spearman 0.9998).

### Cited Findings
- The total curvature of a curve is the supremum of the total turning angles of all polygons inscribed in it; for a polygon it agrees with the sum of turning angles — [Sullivan, Curves of Finite Total Curvature (ResearchGate)](https://www.researchgate.net/publication/2128405_Curves_of_Finite_Total_Curvature); [Springer chapter](https://link.springer.com/chapter/10.1007/978-3-7643-8621-4_7). This is Milnor's 1950 construction; Sullivan's paper states it for space curves, so the 3D, unsigned use in the thesis is covered.
- Polygonal chains without 180 degree angles have well-defined total curvature, with curvature as point masses at the vertices — [Wikipedia, Total curvature](https://en.wikipedia.org/wiki/Total_curvature).
- Discrete curvature literature lists three standard choices at an inner vertex with turning angle theta_p: theta_p, 2 sin(theta_p/2), 2 tan(theta_p/2) — [Discrete curvature, arXiv 2502.09353](https://arxiv.org/pdf/2502.09353); the same four viewpoints (turning angle, length variation, Steiner formula, osculating circle) are the organising slide of [Crane, Discrete Curves lecture, CMU 15-458](https://brickisland.net/ddg-web/lectures/DDG-DiscreteCurves.pdf) (formulas are in images there; the mapping theta / 2 sin / 2 tan / circumcircle is taken from the arXiv source). Discrete Elastic Rods uses 2 tan(phi/2) and treats curvature as an integrated quantity spread over half of each neighbouring edge — [Bergou et al., Discrete Elastic Rods (Scribd copy)](https://www.scribd.com/document/75906093/Miklos-Bergou-Max-Wardetzky-Stephen-Robinson-Basile-Audoly-and-Eitan-Grinspun-Discrete-Elastic-Rods); [BlackHC BSc thesis summary](https://blog.blackhc.net/university-projects/bsc-thesis-discrete-elastic-rods/).
- Own derivation, circle of radius R sampled with chord l: every turning angle equals the central angle of one chord, theta = 2 arcsin(l / 2R). Hence sum(theta) over the covered arc equals arc / R exactly (numerator unbiased), theta / l = (2/l) arcsin(l/2R) = (1/R)(1 + l^2/(24 R^2) + ...), 2 sin(theta/2) / l = 1/R exactly (Menger curvature, the circumcircle of three equally spaced points), 2 tan(theta/2) / l = (1/R)(1 + l^2/(8R^2) + ...).
- Own measurement (`synth.py`, relative error vs 1/R; "code" is `scc_density*pi` on a 100 mm arc):

| R (mm) | l (mm) | theta (deg) | theta/l | 2 sin/l | 2 tan/l | code | (n-1)/n |
|---|---|---|---|---|---|---|---|
| 5 | 5 | 60.0 | +4.7% | 0 | +15.5% | -0.8% | 0.947 |
| 10 | 5 | 29.0 | +1.1% | 0 | +3.3% | -4.3% | 0.947 |
| 20 | 5 | 14.4 | +0.3% | 0 | +0.8% | -5.0% | 0.947 |
| 50 | 5 | 5.7 | +0.04% | 0 | +0.1% | -5.2% | 0.947 |
| 10 | 8 | 47.2 | +2.9% | 0 | +9.1% | -5.7% | 0.917 |
| 50 | 8 | 9.2 | +0.1% | 0 | +0.3% | -8.2% | 0.917 |

  For gentle curvature the code's error is almost entirely the (n-1)/n end effect; the chord-vs-arc overestimate only shows for R near l.
- Own measurement on 120 training RCAs, l = 5 (`real.py`), each variant against the code: dividing by (n-1) l instead of n l: median +5.0% (max +12.5%), Spearman 0.9987, Spearman with length drops from 0.361 to 0.330. Dividing by the true arc between first and last vertex: -1.4%, Spearman 0.9999. Dividing by the arc between the midpoints of the first and last chord (the arc the angles actually represent): +3.7%, Spearman 0.9987. Menger 2 sin(theta/2): -0.6%, Spearman 0.9998. Number of chords per RCA: 9 to 29, median 21.

### Inferences
- The thesis sentence "which is the mean absolute curvature measured at scale l" is defensible if read as: T_l is total turning of the l-inscribed polygon per unit length, a lower bound on the true total curvature (Milnor) divided by an underestimate of length. For gentle bends (R >> l) theta/l approximates |kappa| to better than 1%; bends shorter than l are underestimated or missed.
- The (n-1)/n factor is the one correctable, length-dependent bias: a 69 mm RCA (n about 13) is scaled by about 0.92 and a 137 mm RCA (n about 27) by about 0.96. It explains a small part of the reported Spearman 0.30 with length (in the subset, 0.361 to 0.330), not most of it. Fix: divide by (len(V) - 2) * l, i.e. the dual length of the n - 1 interior vertices (half of each neighbouring chord), which is the normalisation discrete differential geometry uses for integrated curvature.
- Arc length vs chord length in the denominator matters by about 1% on these data and is not worth a change on its own; if a change is made, the midpoint-to-midpoint arc is the principled denominator.
- The Tello-to-thesis relation: with equal chords, mean angle per step times 1/l is the same as total turning over (n-1) l. So the thesis step 4 (divide by length) is mathematically only a rescaling of a mean-angle score by 1/l, provided the n vs n-1 count is consistent.

### Gaps
- Whether van Zandwijk et al. computed pointwise curvature of a fitted spline (which would not be a lower bound and could explain their roughly twice higher 0.081 to 0.090 mm^-1) was not checked here; it is outside this note's scope but is a candidate explanation for the "not yet known" discrepancy in the thesis line 140-141.

## 4. Chord vs arc-length resampling, the dropped remainder, and direction dependence

### Takeaway
Chord vs arc-length respacing barely matters for ranking (Spearman 0.991), but the result depends on where the walk starts: reversing the direction changes an RCA's T_5 by median 3.1%, 90th percentile 10.3%, max 34%, and because the cohort walks each RCA from an arbitrary end, 3 of the 56 high and 11 of the 56 low RCAs change group when the walk is fixed to start at the ostium. Starting position inside one chord (phase) moves the score by a median 6.5% peak to peak. The low decile is the fragile one, consistent with the thesis finding that low-group membership is less stable across l.

### Cited Findings (own measurements)
- Arc-length respacing at 5 mm (`np.interp` on cumulative arc) vs the chord walk, 120 RCAs: median -0.8%, max |diff| 12.1%, Spearman 0.991 (`real.py`).
- Reversed walk vs as-run, 120 RCAs: |relative change| median 3.0%, 90th percentile 10.2%, max 24.4%, Spearman 0.974 (`real.py`).
- All 560 training RCAs (`dirn.py`): median T_5 as run 0.0476, ostium-first 0.0485, distal-first 0.0472; ostium-first minus distal-first mean +2.4% (signed), |relative difference| median 3.1%, 90th percentile 10.3%, max 33.8%. Group membership changes (each change is one vessel out and one in, so halve for "of 56"): as-run vs ostium-first 6 high-set changes and 22 low-set changes (3 and 11 of 56); ostium-first vs distal-first 8 and 30 (4 and 15 of 56).
- Start offset (first vertex moved 0, 1, 2, 3, 4 mm along the arc), 120 RCAs: per-vessel SD 2.5% of the score, peak-to-peak median 6.5%, 90th percentile 14.0%; between-vessel SD is 33% of the median (`real.py`).

### Inferences
- The direction dependence has two sources: which vertices the chord walk lands on (phase), and which end loses the dropped tail and the uncounted half-chords. The signed +2.4% for ostium-first suggests the proximal end, where ostial loops sit, is more curved, so whether the proximal half-chord is counted matters systematically.
- Fixing the walk to start at the ostium (the orientation already computed in `tortuosity_deciles.py:rca`) makes the score reproducible and anatomically defined; averaging forward and reverse, or averaging over several start offsets, would additionally reduce the phase noise (about 2.5% SD) at negligible cost. These are the two cheapest robustness gains available.
- Chord respacing has one conceptual advantage over arc-length respacing: all steps are exactly l, so theta_j are comparable, and the Menger/circumcircle interpretation holds exactly. Arc-length respacing gives unequal chords in bends. Neither changes the ranking here.
- Dropping the remainder removes up to l of vessel from one end, so for short vessels (n about 9) up to about 10% of the vessel is unscored; together with the n-1 count this penalises short vessels.

### Gaps
- Offset averaging and ostium-first were not rerun at l = 4 and 8 to see whether they also stabilise the across-l group changes reported in the thesis (lines 169-171).

## 5. The worked example

### Takeaway
It is right to the stated precision but not exact: the given point is not exactly 5 mm from (5,0,0), and 23.5/25 assumes it is.

### Cited Findings (own computation, `synth.py`)
- b = (4.70, 1.71, 0), |b| = 5.00141 mm, a.b = 23.5, cos = 23.5 / (5 * 5.00141) = 0.93974, theta = 19.993 degrees. Using the text's 23.5/25 = 0.94 gives arccos(0.94) = 19.948 degrees. The exact 20 degree point at 5 mm is (9.6985, 1.7101, 0).

### Inferences
- Both round to 20 degrees, so the example stands, but the text should write "about 0.94" or use (9.698, 1.710, 0), since step 1 promises chords of exactly l.

### Gaps
- None.

## 6. Noise sensitivity and l as a low-pass scale

### Takeaway
The thesis rule of thumb "each angle gains about 3 sigma / l radians, the score about 3 sigma / l^2, always added" is right for a straight vessel with independent 3D vertex noise (3.07 sigma / l exactly) and overstates it by about 20% at l >= 5 because chord vertices are interpolated. On a curved vessel the added bias is much smaller than 3 sigma / l^2, because |theta| of a large true angle plus small noise is nearly unbiased. So noise inflates straight vessels most and compresses the low end of the distribution.

### Cited Findings (own measurements, `synth.py`, 30 repeats each)
- Theory: for independent isotropic noise sigma per vertex, the second difference has per-component SD sqrt(6) sigma; its component perpendicular to the chord is 2D, so |perpendicular| has mean sqrt(6) sigma sqrt(pi/2) = 3.07 sigma, and theta about that over l.
- Straight 100 mm line, 0.47 mm spacing (the ImageCAS-X point spacing): measured T_l vs 3 sigma / l^2: sigma 0.1, l 5: 0.0094 vs 0.0120; sigma 0.25, l 5: 0.0234 vs 0.0300; sigma 0.5, l 5: 0.0489 vs 0.0600; sigma 0.5, l 2: 0.374 vs 0.375; sigma 0.25, l 8: 0.0087 vs 0.0117.
- Circle R = 15 mm (true 1/R = 0.0667), excess over the noise-free code value: sigma 0.25, l 5: +0.0025 (3 sigma / l^2 predicts 0.030); sigma 0.5, l 5: +0.0129 (predicts 0.060); at l = 2 the excess is close to the prediction (sigma 0.25: +0.099 vs 0.188) because noise angles there are larger than the true 7.6 degrees.

### Inferences
- The additive formula is an upper bound valid when noise angles exceed signal angles, i.e. at small l or on nearly straight segments. At l = 5 mm on a typical RCA (median true turn about 14 degrees per chord) residual noise adds little; this is why T_5 is stable and why the thesis curve of median T vs l (0.085 at 2, 0.048 at 5, 0.040 at 8) flattens: between 5 and 8 mm the remaining drop is mostly real sub-l bends being low-passed out (Milnor's inequality), not noise.
- l therefore acts as a low-pass scale in two ways at once: it suppresses noise roughly as sigma / l^2 and removes genuine bends with radius of curvature below about l/2 (loops smaller than l are skipped entirely, section 1). The two cannot be separated from T_l alone; the synthetic-plus-jitter design in `run_merged_tests.py` is the right way to show it.
- The delivered centerlines are smoothed, so their effective sigma is unknown and correlated along the vessel; the i.i.d. formula is a model, not a measurement of these data.

### Gaps
- The actual residual noise level and correlation length of the ImageCAS-X centerlines is not known; `run_merged_tests.py` injects sigma = 0.5 mm i.i.d. jitter, but no estimate of the true noise was found.
- Voxel staircase effects were not simulated separately; given 0.47 mm spacing and pre-smoothing, they fall under the sigma analysis above only if they are roughly independent between points, which staircases are not.
