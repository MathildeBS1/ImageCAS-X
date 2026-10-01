# Per-vessel empirical behaviour of candidate tortuosity metrics on ImageCAS-X centerlines

All numbers below were computed on the delivered reference centerlines of the **first 150 ids of `filelist/train.txt`** (train split only, test never touched), using the scratch copies of `topology/graph.py` `build_tree` and `Vessel` from the `tree-extraction` branch. Population per vessel, after a 20 mm length floor: LAD 150, LCX 150, RCA 150, D1 126 (20 short, 4 absent), OM1 104 (30 short, 16 absent), PDA 129 (18 short, 3 absent; 124 R-PDA, 5 L-PDA). Short and absent vessels are kept as NaN rows with a reason in `metrics.csv`. Dominance in these 150: 139 R, 8 L, 3 Co. The Disease column was never read.

Scratchpad root, abbreviated `$S` below: `/tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/95342cdc-997a-4936-86b1-8ef0c6bb5ebe/scratchpad/pervessel/`. The scratchpad is session-local; copy the scripts into `tortuosity/` if these numbers are to enter the thesis.

## 1. Per-vessel distributions of the candidate metrics

### Takeaway
The vessels differ most on TI, not on curvature. RCA TI (median 0.77) is more than twice LAD (0.32) and LCX (0.29), and about seven times D1 (0.10) and PDA (0.12). Mean absolute curvature kappa_a sits in a narrow band (median 0.047 to 0.084 mm^-1 at sigma 1 mm, ell 5 mm) for every vessel. It keeps its within-vessel ranking across the whole sigma and ell grid (Spearman 0.83 to 1.00), even though its absolute value falls by a factor of about 2 from ell 2 to ell 8 mm. Q stays near 1.3 in every vessel, which is the value it also takes on pure noise. The bend count is zero for 39 % to 83 % of vessels, so it has a floor.

### Cited Findings
Method and parameters (all from `compute.py`, saved in `params.json`):
- Pipeline per vessel: the `Vessel.is_main` chain (longest one if several share a name) is arc-length resampled to 0.25 mm and Gaussian smoothed at sigma in {0.5, 1, 2} mm. The ends are padded by odd reflection about each endpoint, so the endpoints stay fixed and straight ends stay straight. L is the smoothed length and D the end-to-end distance. TI = L/D - 1. Chord angle theta_i is the angle between p[i]-p[i-m] and p[i+m]-p[i], with m x 0.25 mm = ell and ell in {2, 3, 5, 8} mm. kappa_i = theta_i / ell. kappa_a = mean kappa_i and kappa_r = RMS kappa_i, both over interior points only. Q = (kappa_r/kappa_a)^2. K = kappa_a x L. Bends per 100 mm are the peaks of theta_i of 45 degrees or more, kept at least ell apart, at ell 5 and 10 mm and sigma 1 mm. Multiscale TI(ell) is the polyline length of the unsmoothed 0.25 mm resample re-sampled at arc step ell, divided by D, minus 1, for ell in {1, 2, 3, 5, 8, 12, 20} mm (source: [compute.py]($S/compute.py), [params.json]($S/params.json), [metrics.csv]($S/metrics.csv))
- Runtime was 5.7 s for 150 cases on the login node, so the full 560 train cases are feasible in the same way (source: [params.json]($S/params.json))

Default panel, sigma 1 mm and ell 5 mm: median [IQR] (5th to 95th percentile), skew. Source: section A of [analysis.txt]($S/analysis.txt), produced by [analyse.py]($S/analyse.py).

| Vessel | n | L mm | TI | kappa_a mm^-1 | kappa_r mm^-1 | Q | K rad | bends/100 mm (ell 10), % zero |
|---|---|---|---|---|---|---|---|---|
| LAD | 150 | 133 [109-146] | 0.32 [0.22-0.46] (0.14-0.63), skew 0.80 | 0.059 [0.048-0.075] (0.036-0.104), 0.75 | 0.070 | 1.41 [1.33-1.52] (1.22-1.69) | 7.8 (4.0-15.1) | 0.75, 42 % |
| LCX | 150 | 84 [65-106] | 0.29 [0.17-0.44] (0.08-0.59), 0.45 | 0.057 [0.047-0.073] (0.037-0.102), 0.94 | 0.068 | 1.34 [1.27-1.45] (1.15-1.63) | 4.8 (2.2-10.8) | 0, 51 % |
| RCA | 150 | 106 [96-117] | 0.77 [0.57-1.05] (0.28-1.46), 0.89 | 0.047 [0.040-0.062] (0.034-0.084), 0.95 | 0.054 | 1.31 [1.24-1.42] (1.15-1.64) | 5.0 (3.1-10.6) | 0.79, 48 % |
| D1 | 126 | 40 [31-57] | 0.10 [0.07-0.15] (0.03-0.27), 1.84 | 0.058 [0.044-0.075] (0.029-0.116), 1.75 | 0.067 | 1.30 [1.23-1.40] (1.12-1.65) | 2.4 (0.9-6.1) | 0, 83 % |
| OM1 | 104 | 42 [28-65] | 0.21 [0.12-0.27] (0.03-0.52), 1.74 | 0.084 [0.054-0.123] (0.034-0.171), 0.86 | 0.099 | 1.29 [1.22-1.39] (1.10-1.50) | 3.9 (0.9-10.7) | 0, 58 % |
| PDA | 129 | 44 [36-57] | 0.12 [0.08-0.20] (0.04-0.37), 1.60 | 0.070 [0.049-0.097] (0.035-0.135), 0.96 | 0.079 | 1.28 [1.21-1.37] (1.11-1.57) | 2.9 (1.2-7.2) | 0, 55 % |

- Relative spread (IQR/median) at the default point: TI 0.62 (RCA) to 1.00 (PDA); kappa_a 0.45 (RCA, LAD, LCX) to 0.83 (OM1); Q 0.13 to 0.14 in every vessel (source: [analysis.txt]($S/analysis.txt) section A)
- The bend count at ell 5 mm has zeros in 39 % (LAD) to 78 % (RCA) of vessels, and at ell 10 mm in 42 % to 83 % (source: [analysis.txt]($S/analysis.txt) section A)
- kappa_a medians depend on scale. LAD falls from 0.099 (sigma 0.5, ell 2) to 0.041 mm^-1 (sigma 2, ell 8). RCA falls from 0.077 to 0.041, and OM1 from 0.125 to 0.052 (source: [analysis.txt]($S/analysis.txt) section B)
- Rank stability of kappa_a against the default (sigma 1, ell 5): Spearman is 0.90 or higher at every grid point for LAD, LCX, RCA, OM1 and PDA. The one exception is D1, at 0.83 for sigma 0.5 and ell 2. The ell 8 mm points are the next weakest (0.90 to 0.98) (source: [analysis.txt]($S/analysis.txt) section B2)
- TI rank stability across smoothing: Spearman of TI_raw, TI at sigma 0.5 and TI at sigma 2 against TI at sigma 1 is 0.985 or higher in every vessel (source: [analysis.txt]($S/analysis.txt) section B3)
- Q grid: medians run from 1.21 to 1.47 over the whole sigma x ell grid and all vessels. Q falls as ell grows, for example LCX from 1.47 at ell 2 to 1.24 at ell 8 (source: [analysis.txt]($S/analysis.txt) section C)
- Noise floor, measured on a straight 100 mm line sampled at 0.45 mm with iid per-axis jitter of 0.05, 0.1 or 0.2 mm (20 repetitions): Q is 1.24 to 1.35 at every grid point and every jitter level. For reference, a circle has Q = 1.00 and a single-harmonic sinusoid has Q = pi^2/8 = 1.23. The kappa_a floor at sigma 1 and ell 5 is 0.0022 (jitter 0.05), 0.0049 (jitter 0.1) and 0.0154 mm^-1 (jitter 0.2). At sigma 0.5 and ell 2 it is 0.019, 0.044 and 0.128 (source: [plots_noise.py]($S/plots_noise.py), [plots_noise.txt]($S/plots_noise.txt))
- Measured jitter scale: iid jitter of 0.01, 0.02, 0.03 and 0.05 mm gives median raw step angles of 3.4, 6.8, 11.8 and 19.9 degrees. The real per-case median raw step angle is 5.8 degrees (5th to 95th percentile over the 150 cases: 4.8 to 6.9) (source: [jitter_angle.py]($S/jitter_angle.py), [jitter_angle.txt]($S/jitter_angle.txt), [crossvessel.txt]($S/crossvessel.txt))
- Multiscale TI(ell), median ratio TI(ell)/TI(1 mm) at ell 2, 3, 5, 8, 12 and 20 mm: RCA 0.99, 0.99, 0.97, 0.96, 0.93, 0.89. LAD 0.98, 0.96, 0.92, 0.87, 0.82, 0.75. LCX 0.98, 0.95, 0.91, 0.87, 0.80, 0.72. D1 0.95, 0.90, 0.79, 0.64, 0.47, 0.30. OM1 0.96, 0.91, 0.81, 0.66, 0.50, 0.35. PDA 0.94, 0.88, 0.79, 0.68, 0.52, 0.41 (source: [analysis.txt]($S/analysis.txt) section D)
- Cross-vessel differences (Kruskal-Wallis over the six vessels): TI p = 2.7e-94, kappa_a p = 4.5e-17, Q p = 6.7e-14 (source: [analysis.txt]($S/analysis.txt) section H)

### Inferences
- The raw step angle of about 5.8 degrees would be produced by only about 0.02 mm of iid per-axis jitter. At that level the kappa_a noise floor at sigma 1 and ell 5 is about 0.001 mm^-1, roughly 2 % of the vessel values (floor extrapolated linearly from the jitter runs). So kappa_a at ell 3 to 5 mm is not noise-dominated if the error is iid. Spatially correlated error was not simulated and could be larger.
- Q on real vessels (1.28 to 1.41) is barely above its value on pure noise (about 1.27, matching the 4/pi the earlier report derived) and close to a plain sinusoid. Its IQR/median is 0.13. Q therefore has almost no dynamic range at these scales.
- The multiscale profile separates two kinds of vessel. On the main vessels, and on the RCA most of all, TI comes from large-scale shape: it survives a 20 mm chord almost intact. On the side branches TI comes from bends a few mm to 10 mm across: 60 % to 70 % of it disappears at a 20 mm chord. A single TI therefore measures different things on different vessels.
- kappa_a is the metric whose value can be compared across vessels, which TI cannot, but its absolute value is only meaningful at a stated (sigma, ell).

### Gaps
- Only 150 of 560 train cases were used, following the login-node instruction; the full cohort would take about 20 s.
- The bend detector (peaks of chord angle at ell 5 or 10 mm) is one choice among several. No angiographic 45-degree definition maps cleanly onto a 3D chord scale, so the bend rates are only indicative.
- Correlated (smooth) centerline error, the realistic kind, was not simulated. The noise floor above is for iid jitter only.

## 2. Correlation with vessel length within each vessel

### Takeaway
TI is strongly length-confounded on the three main vessels (Spearman with L 0.70 to 0.83) and moderately on D1 and OM1 (0.44, 0.48), but not on PDA (0.24). K is length-confounded everywhere (0.59 to 0.78), as its definition implies. kappa_a is nearly length-free (0.04 to 0.30), and only the RCA reaches a significant but weak 0.30. Q is length-linked on the side branches (0.37 to 0.44), which counts against it.

### Cited Findings
Spearman rho with smoothed length L at sigma 1 mm (* means p < 0.01). Source: section E of [analysis.txt]($S/analysis.txt).

| Metric | LAD | LCX | RCA | D1 | OM1 | PDA |
|---|---|---|---|---|---|---|
| TI (sigma 1) | 0.78* | 0.83* | 0.70* | 0.44* | 0.48* | 0.24* |
| TI(ell 20 mm) | 0.82* | 0.87* | 0.69* | 0.63* | 0.74* | 0.35* |
| kappa_a ell 2 | 0.11 | 0.13 | 0.23* | 0.06 | 0.07 | 0.03 |
| kappa_a ell 5 | 0.17 | 0.15 | 0.30* | 0.24* | 0.14 | 0.04 |
| kappa_a ell 8 | 0.21* | 0.06 | 0.32* | 0.26* | 0.11 | -0.05 |
| Q ell 5 | 0.16 | 0.30* | 0.16 | 0.23* | 0.37* | 0.44* |
| K ell 5 | 0.59* | 0.78* | 0.67* | 0.77* | 0.73* | 0.64* |
| bends/100 mm ell 10 | 0.32* | 0.10 | 0.33* | 0.33* | 0.40* | 0.23* |
| baseline TI (sigma 10) | 0.83* | 0.89* | 0.70* | 0.77* | 0.85* | 0.51* |
| Rlen (sigma 10 baseline) | 0.23* | 0.20 | 0.31* | 0.17 | 0.12 | 0.04 |
| Rlen (spline, 25 mm knots) | 0.20 | 0.54* | 0.40* | 0.56* | 0.62* | 0.52* |
| D (chord) | 0.71* | 0.95* | 0.20 | 0.99* | 0.96* | 0.96* |

- Dominance, with only 8 L and 3 Co cases so the numbers are indicative. RCA median L is 67 mm in left-dominant against 107 mm in right-dominant hearts, and RCA median TI is 0.29 against 0.81 (Mann-Whitney R vs non-R: L p = 0.0011, TI p = 0.00033). kappa_a (0.055 vs 0.046, p = 0.31) and Rlen (0.082 vs 0.079, p = 0.54) do not differ. LCX TI is 0.50 in left-dominant and 0.28 in right-dominant hearts (source: [dominance_iq.py]($S/dominance_iq.py), [dominance_iq.txt]($S/dominance_iq.txt))
- Image Quality: |Spearman| is 0.16 or less for L, TI, kappa_a, Rlen and Q in every vessel (source: [dominance_iq.txt]($S/dominance_iq.txt))

### Inferences
- On the main vessels TI is largely a measure of how far the vessel travels around the heart. The RCA is the clearest case: its chord D is almost unrelated to L (rho 0.20), because a longer RCA curls round the crux back toward its ostium, so L/D grows with extent. The dominance split confirms this: a left-dominant RCA stops early and scores low TI.
- The spline-detrended residual picks up length dependence (0.52 to 0.62 on LCX and the branches) because a fixed 25 mm knot spacing gives short vessels only one knot. It would need knots scaled to vessel length. The Gaussian baseline does not have this problem.
- For a "normalised for length" requirement, kappa_a and the Gaussian-detrended Rlen pass on every vessel. TI passes on PDA only, and at best marginally on D1 and OM1.

### Gaps
- Length correlation may be partly real anatomy (bigger hearts, longer and more tortuous vessels). Heart size is not in Descriptors; total tree length could serve as a proxy, but was not tested here.
- With 11 non-right-dominant cases, the dominance effect is only a direction; its size is not established.

## 3. Does a heart-following baseline dominate? Detrended residual tortuosity

### Takeaway
Yes on LAD, LCX and RCA, no on the side branches. Write 1 + TI = (L/L_b)(L_b/D), with the baseline L_b from sigma 10 mm smoothing. Then the baseline factor carries 82 % to 87 % of the variance of log(1+TI) on the main vessels, but only 26 % to 34 % on D1, OM1 and PDA. The residual length excess Rlen = L/L_b - 1 is nearly length-free and patient-coherent, but it tracks kappa_a closely (rho 0.93 to 0.96), so on these data detrending mostly rediscovers kappa_a.

### Cited Findings
- Baselines (all in [compute.py]($S/compute.py)): Gaussian smoothing at sigma 10 and 15 mm with odd-reflection padding, endpoints fixed; and a cubic least-squares spline per coordinate with interior knots every 25 mm, fitted to the sigma 1 mm curve. Derived metrics: baseline TI = L_b/D - 1; Rlen = L_sigma1 / L_b - 1; kadet = kappa_a(sigma 1, ell 5) - kappa_a(baseline, ell 5); rmsdev = RMS distance between the sigma 1 mm curve and the baseline (source: [compute.py]($S/compute.py))
- Variance share of log(1+TI) carried by the baseline factor, cov(log(L_b/D), y)/var(y), for the sigma 10 / sigma 15 / spline baselines: LAD 0.82 / 0.77 / 0.89; LCX 0.83 / 0.76 / 0.87; RCA 0.87 / 0.82 / 0.94; D1 0.26 / 0.17 / 0.79; OM1 0.26 / 0.21 / 0.71; PDA 0.34 / 0.23 / 0.74 (source: [analysis.txt]($S/analysis.txt) section F2)
- Spearman(TI, baseline TI) at sigma 10: 0.93, 0.94 and 0.98 on LAD, LCX and RCA, against 0.73, 0.68 and 0.71 on D1, OM1 and PDA. Spearman(TI, Rlen) at sigma 10: 0.52, 0.52 and 0.61 on the main vessels, against 0.91, 0.84 and 0.93 on the branches (source: [analysis.txt]($S/analysis.txt) section F2)
- Baseline curvature as a share of kappa_a (median kab/ka at sigma 10): LAD 0.36, LCX 0.44, RCA 0.62, D1 0.31, OM1 0.27, PDA 0.29. The baseline kappa_a itself varies little between patients (IQR/median 0.15 to 0.26 on the main vessels) (source: [analysis.txt]($S/analysis.txt) sections F, F2)
- Rlen at sigma 10, median [IQR] and IQR/median: LAD 0.072 [0.054-0.106] 0.72; LCX 0.080 [0.058-0.114] 0.71; RCA 0.080 [0.064-0.121] 0.72; D1 0.069 [0.046-0.107] 0.88; OM1 0.116 [0.058-0.199] 1.21; PDA 0.082 [0.055-0.137] 1.00. TI IQR/median for comparison: 0.73, 0.92, 0.62, 0.86, 0.75, 1.01 (source: [analysis.txt]($S/analysis.txt) sections A, F)
- The Rlen medians are more alike across vessels (0.069 to 0.116; Kruskal-Wallis p = 1.7e-5) than the TI medians (0.10 to 0.77; p = 2.7e-94) (source: [analysis.txt]($S/analysis.txt) section H)
- Spearman(kappa_a, Rlen at sigma 10) within vessel is 0.93 to 0.96, and Spearman(kappa_a, kadet at sigma 10) is 0.94 to 0.99 (source: [analysis.txt]($S/analysis.txt) section G, F2)
- The spline baseline with 25 mm knots follows the vessel too closely: median spline Rlen is only 0.007 to 0.035, with 5th percentiles below zero on LCX, RCA, D1, OM1 and PDA (source: [analysis.txt]($S/analysis.txt) section F)

### Inferences
- On the main vessels, whole-vessel TI is mostly baseline: 80 % to 90 % of its variance is the course the vessel takes over the heart, not local tortuosity. The claim in "Choosing a coronary tortuosity descriptor.md" that vessel-level TI is the anchor should be read with this in mind. On LAD, LCX and RCA it measures course and extent, and those depend on heart geometry and dominance.
- On the side branches TI is mostly residual, and there it agrees with kappa_a (rho 0.79 to 0.85). TI and kappa_a therefore mean roughly the same thing on branches and different things on main vessels.
- Detrending is useful as a way of understanding TI but adds little as a new metric: Rlen at sigma 10 mm is almost a monotone transform of kappa_a at ell 5 mm (rho 0.93 to 0.96). If a residual metric is wanted, kappa_a already serves. The exception is the RCA, where 62 % of kappa_a is baseline curvature from the AV-groove C-shape, so kadet or Rlen would remove heart shape that kappa_a keeps.
- A Gaussian baseline is preferable to a fixed-knot spline: the spline's knot spacing interacts with vessel length and produces negative residual lengths.

### Gaps
- The baseline scale (10 or 15 mm) is arbitrary, and the shares move by 5 to 10 points between the two. No anatomical criterion was found to fix it.
- The baseline was not tested against a heart-surface reference such as the epicardial surface or the AV groove. It is only a low-pass version of the same centerline.

## 4. Rank correlation between metrics within each vessel: which carry distinct information

### Takeaway
There are essentially three independent axes. (a) The kappa_a family: kappa_a at every ell, kappa_r, Rlen, kadet and the bend rate (rho 0.55 to 0.99 with each other). (b) Large-scale TI: TI(ell 20 mm) and the baseline TI. (c) Q, which correlates with nothing (|rho| 0.40 or less), including across vessels in the same patient. TI links (a) and (b) differently by vessel: on LAD and LCX it is mainly (b) (rho with kappa_a 0.40 to 0.41); on the RCA it is almost purely (b) (rho with TI(20 mm) 0.99); on the branches it is mainly (a) (rho with kappa_a 0.79 to 0.85).

### Cited Findings
Spearman within vessel. Source: section G of [analysis.txt]($S/analysis.txt).

| Pair | LAD | LCX | RCA | D1 | OM1 | PDA |
|---|---|---|---|---|---|---|
| TI vs kappa_a (ell 5) | 0.40 | 0.41 | 0.52 | 0.85 | 0.79 | 0.84 |
| TI vs TI(ell 20) | 0.95 | 0.95 | 0.99 | 0.76 | 0.68 | 0.79 |
| kappa_a ell 5 vs ell 2 | 0.97 | 0.96 | 0.95 | 0.91 | 0.96 | 0.95 |
| kappa_a vs Rlen (sigma 10) | 0.96 | 0.93 | 0.95 | 0.92 | 0.95 | 0.95 |
| kappa_a vs bends/100 mm (ell 10) | 0.82 | 0.72 | 0.80 | 0.55 | 0.62 | 0.59 |
| kappa_a vs K | 0.88 | 0.71 | 0.87 | 0.78 | 0.74 | 0.77 |
| TI vs K | 0.68 | 0.81 | 0.73 | 0.83 | 0.84 | 0.80 |
| Q vs kappa_a | 0.32 | 0.26 | 0.07 | -0.12 | -0.18 | -0.05 |
| Q vs TI | 0.10 | 0.28 | 0.19 | 0.08 | 0.04 | 0.12 |

Within-patient agreement across vessels (Spearman over cases, pairwise complete). Source: [crossvessel.py]($S/crossvessel.py), [crossvessel.txt]($S/crossvessel.txt).
- kappa_a: LAD vs LCX 0.38, LAD vs RCA 0.51, LAD vs D1 0.56, LAD vs OM1 0.60, LAD vs PDA 0.43, D1 vs OM1 0.56, RCA vs PDA 0.15
- Rlen (sigma 10): LAD vs LCX 0.53, LAD vs RCA 0.51, LAD vs OM1 0.56
- TI: LAD vs LCX 0.39, LAD vs RCA 0.33, LCX vs RCA 0.05, RCA vs PDA 0.06
- Q: all pairs between -0.13 and 0.16
- L: all pairs between -0.22 and 0.26
- Per-case median raw step angle vs kappa_a (ell 5): LAD 0.42, LCX 0.25, RCA 0.59, D1 0.21, OM1 0.20, PDA 0.14. The value at ell 8 is nearly the same as at ell 2 (for example RCA 0.57 vs 0.60) (source: [crossvessel.txt]($S/crossvessel.txt))

### Inferences
- kappa_a acts partly as a patient-level trait: it is coherent across the patient's arteries (rho up to 0.60) even though vessel lengths are not (rho 0.26 or less). That fits the Groves-style view of tortuosity as a systemic phenotype (not verified here). It also fits a scan-level factor such as motion or reconstruction. The raw step angle correlates with kappa_a about equally at ell 2 and ell 8, which suggests real shape rather than point noise, but the data cannot separate the two.
- Q behaves like measurement noise: no link to kappa_a or TI, and no coherence within a patient. Together with the noise-floor result in section 1, this argues against keeping Q even as a secondary metric at these scales.
- K adds nothing beyond kappa_a and L, since K = kappa_a x L by construction. Its TI and length correlations come from L.
- The bend rate is a coarse, floored version of kappa_a (rho 0.55 to 0.82) and adds no distinct information.

### Gaps
- None of these correlations is a validity result. Without an expert ranking (criterion 7 in `tortuosity/CLAUDE.md`), redundancy can be measured but correctness cannot.
- The Groves reference for tortuosity as a patient trait is from the tortuosity CLAUDE.md criteria list and was not re-read here.

## 5. Extreme cases per vessel and whether they look plausible

### Takeaway
The extremes look plausible, and they show what each metric measures. The lowest TI and lowest kappa_a RCA (case 266) is a short (52 mm) straight RCA that never reaches the crux. The highest-TI RCA (241, TI 2.53) is a full C-loop whose end returns near the ostium. The highest-TI LAD (715, 0.94) wraps round the apex. The highest-kappa_a vessels have multiple tight local bends. A few patients (786, 371, 715, 241) score high on kappa_a in nearly every vessel. One OM1 (786) shows a sharp step-like kink that could be a centerline artefact.

### Cited Findings
Plots in `$S/extremes_<vessel>.png`: lowest and highest TI, lowest and highest kappa_a, each with the raw points, the sigma 1 mm curve, the sigma 10 mm baseline and the chord (source: [plots_noise.py]($S/plots_noise.py). Case ids, value and L (mm) come from section I of [analysis.txt]($S/analysis.txt).)

| Vessel | TI lowest | TI highest | kappa_a lowest | kappa_a highest |
|---|---|---|---|---|
| LAD | 547 (0.10, 106), 570, 8 | 628 (0.72, 171), 715 (0.89, 172), 571 (0.94, 153) | 705, 818, 266 (0.032) | 970 (0.117, 92), 715 (0.117), 371 (0.124, 150) |
| LCX | 323 (0.045, 50), 599, 452 | 143, 786, 4 (0.75, 127) | 327, 774, 563 (0.031 to 0.035) | 371, 786, 870 (0.128, 37) |
| RCA | 266 (0.04, 52), 971 (0.07, 67), 570 | 4 (1.88), 814 (1.96), 241 (2.53, 132) | 266, 384, 563 (0.029 to 0.031) | 469, 640, 970 (0.100, 131) |
| D1 | 971, 266, 747 (0.014 to 0.018) | 643, 786, 371 (0.53, 26) | 266, 384, 971 (0.021 to 0.023) | 135, 360, 786 (0.219, 28) |
| OM1 | 705 (0.019, 33), 174, 779 | 293, 786, 940 (0.99, 42) | 388, 779, 705 (0.025 to 0.027) | 970, 940, 786 (0.257, 33) |
| PDA | 336, 236, 762 (0.013 to 0.027) | 940, 157, 971 (0.61, 41) | 236, 336, 154 (0.026 to 0.030) | 360, 971, 940 (0.180, 52) |

- Visual reading of the PNGs I opened (RCA, LAD, OM1). RCA 266 is a short straight run with sigma 1 mm curve, baseline and chord almost on top of each other. RCA 241 is a large loop that the sigma 10 baseline follows closely (Rlen 0.25). RCA 970 has a small loop near the proximal end on top of the C-shape (kappa_a 0.100). LAD 715 has an apical hook at the distal end, which drives its high TI. LAD 371 has repeated small bends along its whole length. OM1 940 has a loop (TI 0.99). OM1 786 has an abrupt Z-shaped kink at mid-length (kappa_a 0.257) (source: [extremes_RCA.png]($S/extremes_RCA.png), [extremes_LAD.png]($S/extremes_LAD.png), [extremes_OM1.png]($S/extremes_OM1.png))
- Recurring cases, with per-case median raw step angle (cohort 5th to 95th percentile 4.8 to 6.9 degrees). Case 786: 5.84 degrees, kappa_a LAD 0.111, LCX 0.119, D1 0.219, OM1 0.257. Case 371: 6.59 degrees, LAD 0.124, LCX 0.116, OM1 0.154. Case 715: 7.22 degrees (above the cohort 95th percentile), LAD 0.117, LCX 0.105. Case 266: 5.13 degrees, low in every vessel (LAD 0.032, RCA 0.029, D1 0.021) (source: [plots_noise.txt]($S/plots_noise.txt))

### Inferences
- The RCA TI extremes are really extremes of RCA extent and path: a non-reaching RCA (266 and 971, 52 and 67 mm) against a looping one. Neither is "tortuosity" in the angiographic sense. This is the dominance and baseline effect from sections 2 and 3, seen directly.
- Case 715's raw step angle is above the cohort 95th percentile, so its high kappa_a may partly reflect a noisier centerline. Case 786 is not unusually noisy by that measure but shows a kink, so it should be checked against the segmentation before being taken as real. Only a visual check of the lumen can separate the two.

### Gaps
- I inspected only the RCA, LAD and OM1 PNGs; `extremes_LCX.png`, `extremes_D1.png` and `extremes_PDA.png` were written but not viewed.
- Nothing was checked against the CT image or segmentation, so plausibility here means geometric plausibility of the centerline only.

## 6. Where the data agrees and disagrees with "Choosing a coronary tortuosity descriptor.md" (TI + kappa_a)

### Takeaway
The data backs kappa_a as a length-normalised, scale-rank-stable, patient-coherent measure, confirms that Q sits at its noise value and that the bend count floors, and confirms that TI is the most smoothing-robust metric. It disagrees with making TI the primary at whole-vessel scale for LAD, LCX and RCA. There TI is 70 % to 83 % rank-correlated with length and 82 % to 87 % baseline-driven, and on the RCA it mostly encodes dominance. The earlier report also misstated the direction of branch-level TI range. One metric definition can serve all vessels only if it is kappa_a at a fixed (sigma, ell). TI needs either per-vessel reference distributions or a detrended form.

### Cited Findings
- Report claim: TI is the vessel-scale anchor for LAD, LCx and RCA ([report](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Choosing%20a%20coronary%20tortuosity%20descriptor.md)). Data: TI vs L rho 0.78, 0.83, 0.70; baseline variance share 0.82, 0.83, 0.87; RCA TI 0.29 in left-dominant vs 0.81 in right-dominant (p = 0.00033, 11 non-R cases) (source: [analysis.txt]($S/analysis.txt), [dominance_iq.txt]($S/dominance_iq.txt)). **Disagrees.**
- Report claim: TI is the most reproducible metric. Data: TI across sigma 0 to 2 mm has rank rho 0.985 or higher in every vessel, higher than kappa_a across its grid (0.83 or higher) (source: [analysis.txt]($S/analysis.txt) B2, B3). **Agrees** for smoothing robustness. Jitter ICC and extractor agreement were not tested.
- Report claim: branch-scale TI has almost no dynamic range (segment arc/chord about 1.10). Data at named-vessel level (not junction-to-junction segment): D1, OM1 and PDA TI medians 0.10, 0.21, 0.12, with IQR/median 0.86, 0.75 and 1.01, higher than the main vessels' 0.62 to 0.92 (source: [analysis.txt]($S/analysis.txt) A). **Partly disagrees.** Absolute TI is small on branches, but its relative spread is larger than on main vessels and it tracks kappa_a (rho 0.79 to 0.85). Junction-to-junction segments were not measured here.
- Report claim: kappa_a is length-normalised. Data: rho with L between 0.04 and 0.30 at ell 5 mm; only the RCA (0.30) reaches p < 0.01 among the main vessels, plus D1 at 0.24 (source: [analysis.txt]($S/analysis.txt) E). **Agrees**, with a weak residual on RCA and D1.
- Report claim: provisional default ell 5 mm and sigma 1 mm. Data: kappa_a ranking is stable across the grid (rho 0.90 or higher except D1 at sigma 0.5, ell 2), but absolute values change by a factor of about 2. With about 0.02 mm iid-equivalent jitter the floor at ell 5 mm is about 2 % of vessel values (source: [analysis.txt]($S/analysis.txt) B, B2; [plots_noise.txt]($S/plots_noise.txt); [jitter_angle.txt]($S/jitter_angle.txt)). **Agrees**, and ell 3 mm would also pass the iid noise test. The report's claim that raw turning is about three times the real curvature is consistent: a raw 5.8 degrees per 0.45 mm is about 0.22 rad/mm, against kappa_a 0.047 to 0.084 at ell 5. But the jitter test suggests this gap is mostly real sub-5 mm curvature plus small (about 0.02 mm) point noise, not noise alone. That is an inference.
- Report claim: Q tends to about 4/pi on pure noise, so keep it only as exploratory. Data: Q on jittered lines 1.24 to 1.35 (4/pi = 1.27); on real vessels median 1.28 to 1.41, IQR/median 0.13; no within-patient cross-vessel coherence (|rho| 0.16 or less); length-linked on branches (0.37 to 0.44) (source: [plots_noise.txt]($S/plots_noise.txt), [analysis.txt]($S/analysis.txt), [crossvessel.txt]($S/crossvessel.txt)). **Agrees, and more strongly**: the data supports dropping Q, not only demoting it.
- Report claim: bend counts have a floor effect. Data: 39 % to 83 % zeros (source: [analysis.txt]($S/analysis.txt) A). **Agrees.**
- Report claim: store K per branch as a dimensionless companion. Data: K vs L rho 0.59 to 0.78 in every vessel (source: [analysis.txt]($S/analysis.txt) E). **Caution**: K is length-confounded by construction and must always be paired with length.
- Report claim (earlier probe on 20 test cases): pooled main-vessel raw L/D median 1.45. Data on 150 train cases, per vessel: raw TI median 0.34 (LAD), 0.31 (LCX), 0.79 (RCA) (source: [analysis.txt]($S/analysis.txt) A). That pooled figure hides a factor of 2.5 between RCA and LAD, so pooled TI statistics across vessel types should not be reported.

### Inferences
- **One metric for all vessels?** Only kappa_a (sigma 1 mm, ell 3 to 5 mm) behaves consistently across vessel types: similar medians (0.047 to 0.084 mm^-1), weak length dependence, stable ranking, patient coherence. It suits all vessels with the same definition and scale. TI does not: it measures course and extent on LAD, LCX and RCA, and local bending on D1, OM1 and PDA. Using it for all vessels would need per-vessel z-scoring and length adjustment, or the detrended Rlen, which in practice converges on kappa_a.
- **Vessel-specific scale?** The data do not argue for per-vessel ell. The ranking at ell 2 to 8 mm is stable in every vessel. The multiscale TI profile shows the branches' excess length sits at 2 to 12 mm and the main vessels' at 20 mm or more. That supports reporting one small-scale metric (kappa_a) plus, if wanted, a large-scale course metric (TI or baseline TI) as a separate, explicitly length- and dominance-adjusted variable, rather than per-vessel methods.
- The RCA is the one vessel where kappa_a carries a large baseline component (62 % of kappa_a at sigma 10). If the RCA is to be compared with the others, kadet or Rlen may be preferable there, but this is a design choice the data do not settle.
- For the Danish outcome analysis, vessel-level TI on the RCA would largely be a dominance and heart-geometry variable. The earlier report's recommendation to "name TI at vessel level" if only one metric is allowed should flip to kappa_a on this evidence, which is the reversal condition that report itself anticipated.

### Gaps
- No jitter ICC, truncation test or extractor-agreement test was run (report steps 4, 5 and 7), so reproducibility, the report's binding criterion, is still untested for either metric.
- The length and dominance confounding of TI could be removed by regression. Whether residualised TI then carries information beyond kappa_a was not tested.
- Results come from 150 train cases. The 11 non-right-dominant cases are too few for any claim beyond direction.
