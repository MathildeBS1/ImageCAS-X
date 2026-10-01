# Numerical robustness of bifurcation diameter descriptors: error analysis, window choice and a test protocol

Scope: parent-to-daughter ratios (r_LAD/r_LM, r_LCx/r_LM), Finet ratio F = r0/(r1+r2), daughter ratio DR = r_small/r_large, the Murray/Huo-Kassab (HK) exponent n from r0^n = r1^n + r2^n, and the area ratio AR = (r1^2 + r2^2)/r0^2 (the "junction flare" quantity already returned by `topology/angles.py:_measure`). Complements, and does not repeat, `reports/Plaque prone regional geometry descriptors.md` (EDT-vs-surface method ICC, Finet ICC 0.85/0.90, Murray unsolvable 12 to 37 %, daughter-ratio ICC 0.63 to 0.86 on 100 training scans).

Labels used throughout: **[CITED]** from a source, **[DERIVED]** worked out here analytically, **[SIM]** synthetic phantom or Monte Carlo run here, **[MEASURED]** run here on ImageCAS-X reference data. All scripts and raw outputs are in the session scratchpad `/tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/f80fe26a-7a3a-478e-9133-57e051f5b10c/scratchpad/` (`mc_propagation.py/.txt`, `phantom_radius.py/.txt`, `phantom_y.py/.txt`, `lm_profile.py/.txt`); they are not in the repo and must be moved there before any number enters the thesis. The measured window defaults are those of `topology/angles.py` (core skip `core_scale = 1.0` times the EDT radius at the junction node r_J, window `window_mm = 3.0`, median radius), so "k = 1, L = 3" below is the current code path.

## Q1. How does a radius error propagate into ratios, the Finet ratio and the exponent?

### Takeaway
Ratios and the Finet ratio have well-behaved, first-order error propagation. Multiplicative (scale) error cancels exactly, but an additive bias b does not: it shifts r1/r0 by about b(1 − q)/r0 and the Finet ratio by about b(1 − 2F)/(r1 + r2). The exponent n is ill-conditioned with a gain of n²/H, where H is the "flow-split entropy" of the daughters. It has no solution whenever a noisy daughter reaches the parent's radius, so at 0.1 to 0.25 mm radius noise its SD is 0.6 to 1.0, which is as wide as the whole 2 to 3 literature range.

### Cited Findings
- Murray's law has exponent 3. The pooled coronary flow-diameter exponent across 18 studies (1,070 trees) is 2.39 (95 % CI 2.24 to 2.54) with I² = 99 %. The authors attribute the heterogeneity partly to the relatively low resolution of several imaging techniques, and the pooled value agrees closely with Huo and Kassab's 7/3 [CITED] — [Taylor et al. 2024, Am J Physiol Heart Circ Physiol 327:H182](https://pmc.ncbi.nlm.nih.gov/articles/PMC11380967/)
- Reported coronary exponents range from 2.06 to 3.20. A CFD study found 2.15 best matched inlet flow and 2.38 best matched microvascular resistance, and noted that angiographic resolution was limited to 0.1 mm [CITED, abstract/summary] — ["Revisiting Murray's law in human epicardial coronary arteries", Front Physiol 2022;13:871912](https://pmc.ncbi.nlm.nih.gov/articles/PMC9119389/)
- Finet et al. 2008 (173 bifurcations, 59 patients, QCA with an IVUS subset of 27) found Dm = 0.678 (Dd1 + Dd2) at all bifurcation levels. R(angio) = 0.670 ± 0.031 and R(IVUS) = 0.668 ± 0.028 (NS). Mean diameters were mother 3.33 ± 0.94, major daughter 2.70 ± 0.77 and minor 2.23 ± 0.68 mm. The deviation from the linear law was 0.33 %, against 5 % for Murray and 5.94 % for flow conservation [CITED] — [Finet et al. 2008, EuroIntervention 3(4)](https://eurointervention.pcronline.com/article/fractal-geometry-of-arterial-coronary-bifurcations-a-quantitative-coronary-angiography-and-intravascular-ultrasound-analysis). *Note:* the quoted SD of 0.03 is far smaller than the ImageCAS-X between-subject SD of 0.094 (Q5) and the ~0.05 per 0.1 mm noise derived below, so it cannot be a per-bifurcation SD on CT-scale data. It is best read as an angiography/IVUS figure under different conditions.
- The European Bifurcation Club QCA consensus uses Finet's Dmv = 0.678·(Ddv + Dsv) and the HK law Dmv^(7/3) = Ddv^(7/3) + Dsv^(7/3) to derive reference diameters [CITED] — [EBC QCA consensus update, EuroIntervention](https://eurointervention.pcronline.com/article/quantitative-angiography-methods-for-bifurcation-lesions-a-consensus-statement-update-from-the-european-bifurcation-club)

### Inferences
**Derivations [DERIVED]** (the measured radius is r̂_i = r_i + b + ε_i, with b a shared additive bias and ε_i iid with SD σ):
1. *Scale invariance.* All five descriptors are homogeneous of degree 0 in (r0, r1, r2), so a common multiplicative error r̂ = c·r cancels exactly. The exponent equation is also scale-invariant, since a common factor c^n cancels. An additive bias is not a scale error, so it does **not** cancel.
2. *Ratio q = r1/r0.* Under additive bias, dq/db = (1 − q)/r0, which vanishes only when q = 1. Under noise, SD(q)/q ≈ σ·√(1/r1² + 1/r0²). For q = 0.8 and r0 = 2 mm this is +0.010 per +0.1 mm bias, and SD 0.064 per 0.1 mm noise (MC agrees: 0.064).
3. *Finet F = r0/(r1+r2).* Bias gives dF/db = (1 − 2F)/(r1 + r2), which is negative for any F > 0.5, so a positive (EDT-like) bias lowers F. Noise gives SD(F)/F ≈ σ·√(1/r0² + 2/(r1+r2)²). At LM-like radii (2.0, 1.6, 1.4) this is −0.011 per +0.1 mm bias and SD 0.046 per 0.1 mm noise. At distal radii (1.0, 0.85, 0.55) it is −0.031 per 0.1 mm bias and SD 0.10 per 0.1 mm noise. Error scales with 1/r, so the distal-branch Finet is about 2 to 3 times noisier than the LM value.
4. *Area ratio AR.* Its relative error is about twice that of a radius ratio. The bias slope is 2(r1+r2)/r0² − 2AR/r0, which is +0.037 per 0.1 mm at the LM and +0.075 at distal radii. SD is 0.16 per 0.1 mm noise at the LM.
5. *Exponent n.* Write p_i = (r_i/r0)^n, so that p1 + p2 = 1, and let H = −(p1 ln p1 + p2 ln p2) be the Shannon entropy of the "flow split" (≤ ln 2 = 0.693). Implicit differentiation of g = r1^n + r2^n − r0^n gives
   **dn = (n²/H)·(p1·d ln r1 + p2·d ln r2 − d ln r0).**
   So n is scale-invariant (the bracket vanishes for a common d ln r), but the gain is n²/H. H → 0 when one daughter carries almost the whole split (p1 → 1, i.e. r1 → r0), which is typical for a main-branch continuation beside a small side branch, and the gain then diverges. At that point the problem also stops having a solution: a positive n exists only if max(r1, r2) < r0, and n ≥ 1 exactly when F ≤ 1. Noise that pushes r̂1 ≥ r̂0 makes n undefined, and that is where the 12 to 37 % "unsolvable" of the earlier report comes from. First-order SD: SD(n) ≈ (n²/H)·σ·√((p1/r1)² + (p2/r2)² + 1/r0²).

**Monte Carlo [SIM]** (`mc_propagation.txt`, 20,000 draws for ratios and 4,000 for n):

| Configuration (r0, r1, r2 mm) | n_true | n²/H | SD(n) per 0.1 mm (1st-order) | σ = 0.1: unsolvable / P(n ∈ [2, 3.2]) | σ = 0.25: unsolvable / P(n ∈ [2, 3.2]) | Finet bias at b = +0.25 |
|---|---|---|---|---|---|---|
| LM-like (2.0, 1.6, 1.4) | 2.44 | 8.7 | 0.60 | 0.2 % / 64 % | 15 % / 27 % | −0.024 |
| LM equal (2.0, 1.55, 1.55) | 2.72 | 10.7 | 0.72 | 0.1 % / 62 % | 18 % / 28 % | −0.020 |
| Side branch (1.5, 1.35, 0.8) | 2.39 | 10.8 | 1.00 | 15 % / 39 % | 35 % / 15 % | −0.037 |
| Distal (1.0, 0.85, 0.55) | 2.09 | 7.2 | 1.02 | 14 % / 28 % | 37 % / 10 % | −0.056 |

- Even with *no* noise, a bias of b = +0.25 mm moves n from 2.44 to 2.79 at the LM and from 2.09 to 2.74 at distal radii. A realistic EDT bias therefore turns an HK-like 7/3 into something Murray-like, and the "which law holds" question cannot be answered from EDT radii without a bias model.
- Noise also biases n **downward** through selection. Among solvable draws the median n falls from 2.39 to 1.73 at the side branch when σ = 0.25, because draws with r̂1 near r̂0 are either dropped or give very large n. The noisy estimator is biased, not just imprecise.
- The Finet ratio and r1/r0 remain unbiased to ≤ 0.01 under pure noise at σ ≤ 0.1 (nonlinearity bias is ≤ 0.02 at σ = 0.25). Their SD is the limiting factor.
- In what follows, σ is the error of the *window-level* radius (after the 3 mm median), not of the per-point EDT. Per-point errors along a window are spatially correlated (a segmentation boundary is offset over millimetres), so the median does not reduce σ by √n_points. This is why the test protocol (Q4) must estimate σ at window level.

### Gaps
- No published source was found that gives an analytic error propagation for the Murray/HK exponent. The n²/H result above is derived here and should be checked, e.g. by a symbolic check in the test suite (Q4).
- The Huo and Kassab 2012 derivation of the 7/3 exponent and its stated measurement sensitivity were not retrieved. The earlier report also lists it as unread.

## Q2. EDT vs surface-distance vs cross-sectional-area radius: bias at 1 to 3 mm

### Takeaway
The repo's EDT radius (distance to the nearest background voxel centre, `topology/radius.py`) is an *inscribed-sphere* estimator. On an ideal binary cylinder it over-reads by only +0.01 to +0.05 mm, far less than the half voxel its docstring allows. Its real biases are radius-dependent. PSF blur makes it under-read small vessels (−0.03 mm at 3 mm radius to −0.17 mm at 0.75 mm, for σ_PSF = 0.5 mm). Ellipticity makes it read the minor semi-axis, which is −9 to −11 % against the area-equivalent radius at b/a = 0.8. A radius-dependent bias is exactly the kind that does not cancel in ratios. Area-equivalent radius is unbiased under ellipticity and least affected by digitisation, but it needs cross-sections that are well defined, which they are not in the bifurcation core.

### Cited Findings
- Typical CT FWHM of the point-spread function is 0.5 to 0.7 mm in-plane and 0.7 to 1.0 mm along z. Structures smaller than the FWHM are severely distorted [CITED, search-result snippet attributed to an AJR artifacts review; the full text returned HTTP 403 and was not verified] — [AJR, Artifacts in ECG-synchronized MDCT coronary angiography](https://ajronline.org/doi/10.2214/AJR.07.2138)
- Blooming, beam hardening and partial volume impair lumen assessment especially below 2 mm diameter. A CT-number-calibration method beat FWHM-based diameter estimation for 0.8 to 2.5 mm phantom stenoses, and maximum intraluminal voxel value falls with diameter below a PSF-determined cutoff [CITED, abstract] — [Chen et al. 2019, Med Phys](https://pubmed.ncbi.nlm.nih.gov/31603567/)
- On dual-source CT against IVUS, luminal area was underestimated at one window setting (mean (SD) difference −2.1 (1.6) mm²). The least-biased setting (155 %/65 % of mean luminal intensity) gave 0.2 (1.73) mm² [CITED, abstract] — [Coronary vessel and luminal area with DSCT vs IVUS, J Comput Assist Tomogr 2011](https://pubmed.ncbi.nlm.nih.gov/21245696)
- The Lesage et al. review organises lumen segmentation by models, features and extraction schemes. Radius accuracy therefore inherits the segmentation's own boundary model [CITED] — [Lesage et al. 2009, Med Image Anal 13(6):819](https://www.sciencedirect.com/science/article/abs/pii/S136184150900067X)
- Frangi et al. validated model-based vessel diameter quantitation on a carotid bifurcation phantom with known ground truth. This is the precedent for phantom-with-truth radius validation [CITED, abstract; numerical accuracy not retrieved] — [Frangi et al. 1999, IEEE TMI 18(10)](https://ieeexplore.ieee.org/iel5/42/17611/00811279.pdf)
- The medial axis is the locus of centres of maximal inscribed spheres, and VMTK's bifurcation reference system parameterises branches by the local maximal-inscribed-sphere radius [CITED] — [Antiga and Steinman 2004, IEEE TMI 23(6):704](https://link.springer.com/article/10.1007/s11517-008-0420-1) (cited via a secondary paper; original not fetched)

### Inferences
**Phantom 1 [SIM]** (`phantom_radius.txt`): straight cylinders of radius R at 0.5 mm isotropic voxels, 12 random orientations and sub-voxel offsets each, estimators averaged over 11 axis points. Bias in mm (mean ± SD across orientations):

| Mask model | R | EDT (repo rule) | Staircase-surface min distance | Area-equivalent √(A/π) |
|---|---|---|---|---|
| Binary, centre-inside | 0.75 | +0.046 ± 0.009 | −0.150 | +0.002 |
| | 1.0 | +0.039 ± 0.009 | −0.158 | +0.001 |
| | 2.0 | +0.024 ± 0.007 | −0.196 | +0.002 |
| | 3.0 | +0.011 ± 0.002 | −0.212 | −0.006 |
| PV + PSF σ = 0.3 mm (FWHM 0.7), threshold 0.5 | 0.75 | −0.014 ± 0.017 | −0.209 | −0.062 |
| | 1.0 to 3.0 | −0.003 to −0.010 | −0.21 to −0.23 | −0.021 to −0.040 |
| PV + PSF σ = 0.5 mm (FWHM 1.2) | 0.75 | −0.168 ± 0.026 | −0.359 | −0.247 |
| | 1.0 | −0.108 ± 0.017 | −0.322 | −0.161 |
| | 1.5 | −0.068 ± 0.010 | −0.273 | −0.090 |
| | 2.0 | −0.047 ± 0.007 | −0.261 | −0.071 |
| | 3.0 | −0.030 ± 0.003 | −0.253 | −0.044 |
| Elliptic b/a = 0.8 (area-matched), binary | 1.0 / 2.0 / 3.0 | −0.006 / −0.143 / −0.267 | −0.20 / −0.34 / −0.47 | ≈ 0 |

- **The half-voxel figure is a worst case, not typical.** The EDT on an ideal binary mask over-reads by 0.01 to 0.05 mm (2 to 10 % of a voxel) and shrinks with R. The larger EDT-minus-surface gap (+0.135 mm) that the earlier report found against the delivered surface mesh is therefore mostly the surface estimator reading *low*, not the EDT reading high. Any minimum distance to a rough or staircase surface is an extreme-value statistic and is biased low (−0.15 to −0.21 mm for the unsmoothed staircase here).
- **Blur creates a radius-dependent bias.** At σ_PSF = 0.5 mm the EDT bias runs from −0.03 mm at 3 mm radius to −0.17 mm at 0.75 mm, i.e. −1 % to −22 %. Because small daughters lose proportionally more, ratio descriptors are biased: in the Y phantom (Q3, σ = 0.5) the Finet ratio reads +0.023 high at (2.0, 1.7, 1.0) and +0.046 high at (1.5, 1.3, 0.8), and r2/r0 reads 13 % low. At σ_PSF = 0.3 mm the same ratios are within 0.005 of truth. The PSF and threshold behaviour of the *segmentation* (GT annotation or CAS-Net) therefore decides whether ratios are trustworthy at distal branches.
- **Ellipticity.** EDT returns roughly the minor semi-axis, so against the area-equivalent radius it reads −√(b/a)-type low: −0.14 mm at R = 2 and −0.27 mm at R = 3 for b/a = 0.8. This bias is *multiplicative*. It cancels in ratios only if parent and daughter share the same ellipticity, and near the carina they do not, because the daughter origins are oval. That argues for using an area-based radius at least as a sensitivity analysis.
- **Additive bias does not fully cancel** [DERIVED]. From Q1, a common b = +0.05 mm (EDT on a sharp mask) shifts the LM Finet by −0.006, which is negligible. A realistic *differential* bias (−0.03 mm on a 2 mm LM against −0.11 mm on a 1 mm daughter, at σ_PSF = 0.5) shifts it by several hundredths, which is comparable to the SDC in Q4.
- **Converting the cited CT-vs-IVUS spread to radius** [DERIVED]: an area SD of 1.73 mm² at a lumen area of about 7 mm² (r ≈ 1.5 mm) corresponds to δr = δA/(2πr) ≈ 0.18 mm. This supports 0.1 to 0.25 mm as the realistic radius-noise range to test.

### Gaps
- The in-plane PSF of the ImageCAS source scans and the blur implicit in the GT annotations are unknown. The σ_PSF = 0.3 and 0.5 mm settings bracket the cited FWHM range but are not measured.
- The area-equivalent radius was not computed on real data: it needs cross-sectional planes along the centerline, which the repo lacks. The prior report's surface-distance comparison used the smoothed delivered mesh, not the staircase proxy used here.
- Frangi 1999's numerical diameter accuracy was not retrieved (PubMed returned a CAPTCHA).

## Q3. Window choice and how far the junction flare reaches

### Takeaway
The default window (skip the core k = 1·r_J, median over L = 3 mm) is close to optimal in both phantom and real data. Starting at the junction (k = 0) is badly biased: it lowers the LM Finet by −0.04 to −0.07 and raises daughter/parent ratios by 0.02 to 0.11. Beyond k ≈ 1.5 or L = 5 mm, taper and side-branch take-offs start changing the value. On 36 ImageCAS-X test cases the EDT excess over the downstream plateau falls below 5 % after a median of 1.5 mm (about 1.25·r_J) on the LAD and 2.5 mm (about 2.25·r_J) on the LCx, with a long tail to 6.5 to 7 mm. Most of the apparent "flare" is inscribed-sphere geometry at a Y junction rather than true luminal widening.

### Cited Findings
- EBC QCA segment model (BSM6/BSM11): 5 mm segments beyond the treated segments and 3 mm ostial SB segments, with the point of bifurcation defined as the centre of the largest circle touching all three contours. The consensus does not give fixed mm offsets for the reference segments relative to that point [CITED] — [EBC QCA consensus update](https://eurointervention.pcronline.com/article/quantitative-angiography-methods-for-bifurcation-lesions-a-consensus-statement-update-from-the-european-bifurcation-club)
- Finet measured reference diameters in the "artery segment adjacent to the bifurcation … with no other neighbouring bifurcation" [CITED] — [Finet et al. 2008](https://eurointervention.pcronline.com/article/fractal-geometry-of-arterial-coronary-bifurcations-a-quantitative-coronary-angiography-and-intravascular-ultrasound-analysis)
- VMTK/Antiga-Steinman measures bifurcation quantities outside the maximal inscribed sphere at the junction, which is the basis for the repo's k·r_J core skip [CITED via secondary] — [Antiga and Steinman 2004, IEEE TMI 23(6):704](https://link.springer.com/article/10.1007/s11517-008-0420-1)

### Inferences
**Phantom 2 [SIM]** (`phantom_y.txt`): a Y built as the union of three capsules at 0.5 mm voxels with PV and PSF, random rotation, 4 repeats. A pure union has *no* anatomical flare, so any EDT excess here is geometric.
- At the junction the EDT is ≈ r0 (r_J/r0 = 0.93 to 0.99). Along a daughter axis the inscribed sphere keeps touching the parent's far wall, so r(0)/r_daughter is 1.24 for a 1.6 mm daughter and 1.53 for a 1.3 mm one from geometry alone. The excess (> 0.05 mm) ends at 0.9 to 2.0 mm, i.e. 0.46 to 1.2·r_J. It lasts longer for the smaller daughter and for narrower angles (50° vs 80°).
- Window bias at σ_PSF = 0.3 mm (truth Finet 0.690, r1/r0 0.800, r2/r0 0.650):

| start k·r_J | L = 2 mm | L = 3 mm | L = 5 mm |
|---|---|---|---|
| 0 | F 0.625, r2/r0 0.751 | F 0.673, r2/r0 0.678 | F 0.688, r2/r0 0.652 |
| 0.5 | F 0.684 | F 0.688 | F 0.689 |
| 1.0 | F 0.689 | F 0.690 | F 0.691 |
| ≥ 1.5 | F 0.691 to 0.693 | F 0.691 to 0.693 | F 0.691 |

  With k ≥ 1, every case tested (4 geometries, angles 50 to 80°, r2/r0 0.50 to 0.65) is within 0.005 of the true Finet at σ_PSF = 0.3. At k = 0 and L = 2 the error is −0.065 to −0.093. A longer window partly rescues k = 0 by diluting the flare, but in real vessels it then picks up taper.

**Real data [MEASURED]**, `lm_profile.txt`: 40 test-split ids tried and N = 36 with a single-node LM→LAD/LCx junction. Three had no parent or a split junction, and one had 2 LAD vessels. GT mask at native resolution (in-plane 0.32 to 0.40 mm, z 0.5 mm), delivered left centerline, EDT exactly as `topology/radius.py`. Profiles are normalised per case by the median radius 5 to 10 mm (arc) from the junction.
- r_J (EDT at the junction node) has median 1.51 mm (IQR 1.39 to 1.69). r_J is quantised because the node sits on a voxel lattice, e.g. several cases give exactly 1.50 and one gives 0.50 mm (case 909, which looks like a node placed near the wall).
- r/plateau by arc distance, median [IQR] (n = 36 LAD and LCx, n = 25 LM with ≥ 5 mm of LM):

| arc from junction | 0 mm | 0.5 | 1.0 | 1.5 | 2.0 | 3.0 | 4.0 | 5.0 |
|---|---|---|---|---|---|---|---|---|
| LAD | 1.23 [1.09, 1.38] | 1.18 | 1.12 | 1.07 | 1.01 | 1.03 | 1.02 | 1.00 |
| LCx | 1.43 [1.22, 1.80] | 1.39 | 1.26 | 1.21 | 1.15 | 1.11 | 1.07 | 1.02 |
| LM (upstream) | 1.10 [0.88, 1.27] | 1.10 | 1.07 | 1.09 | 1.10 | 1.03 | 1.01 | 1.04 |

- **Flare end** (first 0.5 mm bin with r/plateau ≤ 1.05), median (IQR, max): LAD 1.5 mm (0.9 to 3.0, 6.5), LCx 2.5 mm (1.4 to 5.0, 7.0), LM 1.0 mm (0 to 4.0, 6.0). With a 10 % threshold: LAD 1.0, LCx 2.0 and LM 0.5 mm. In r_J units the cohort-median profile drops below 1.05 at about 1.25·r_J on the LAD and 2.25·r_J on the LCx.
- The size of the LAD excess at the origin (1.23) matches the pure-geometry phantom (1.24 for a daughter of 0.8·r0). The LCx excess (1.43) and its decay (≈ 2.25·r_J against 0.5 to 1.2·r_J in the phantom) are longer than geometry alone predicts. Plausible reasons are genuine ostial funnelling of the LCx, an early OM or ramus take-off inside the first 5 mm, and a plateau depressed by taper. These cannot be separated with EDT alone.
- **Window sensitivity on real data**: median |Δ| against the default (k = 1, L = 3) and cohort median, for the LM Finet:

| k \ L | 2 mm | 3 mm | 5 mm |
|---|---|---|---|
| 0 | 0.541 (\|Δ\| 0.076) | 0.573 (0.049) | 0.598 (0.028) |
| 0.5 | 0.593 (0.042) | 0.604 (0.019) | 0.600 (0.011) |
| 1.0 | 0.629 (0.016) | **0.615** (ref) | 0.605 (0.020) |
| 1.5 | 0.598 (0.009) | 0.604 (0.016) | 0.610 (0.030) |
| 2.0 | 0.600 (0.021) | 0.595 (0.023) | 0.607 (0.037) |

  The same table for r_LAD/r_LM gives 0.953 at (0, 2) against 0.884 at (1, 3), and for r_LCx/r_LM 0.882 against 0.774. The daughter-to-parent ratios are the most window-sensitive descriptors (|Δ| up to 0.10 to 0.12 at k = 0), and the Finet ratio the least. From k = 0.5 to 2 and L = 2 to 5 the Finet ratio stays within about 0.02 to 0.04 of the default. That is below its between-subject SD (0.094, Q5) but comparable to the SDC.
- The LM Finet from GT EDT radii is 0.615 at the default window (N = 36). The earlier report found 0.63 on 100 training scans, and Finet's angiographic value is 0.678. The Q1/Q2 bias analysis predicts EDT-based Finet reads *low* whenever EDT over-reads (b > 0). The gap to 0.678 also contains the difference between CT and angiographic lumen definitions, so it should not be read as anatomy.
- 10 of 36 cases (28 %) have a daughter window radius ≥ the LM window radius at the default window. This is exactly the condition that makes the exponent unsolvable (Q1), and it matches the earlier report's 12 to 37 %.

### Gaps
- The 5 to 10 mm plateau is itself contaminated by taper and by D1/OM/ramus take-offs, and the LM plateau reaches toward the ostium (LM length 2.8 to 22.7 mm in these cases). A per-case plateau from a fitted taper model would be cleaner.
- Only the LM junction was profiled. LAD-D1, LCx-OM1 and the crux, where radii are 1 to 2 mm, were not.
- N = 36 is from the first 40 ids of `test.txt`, not a random sample stratified by image quality or dominance.

## Q4. Test protocol: synthetic phantoms, reference vs CAS-Net agreement, minimum detectable difference

### Takeaway
Use a three-tier protocol with pre-registered pass thresholds. (1) Unit tests of the error algebra and a Y-phantom suite with known radii, blur, ellipticity, rotation and resampling. (2) Reference-vs-CAS-Net agreement on the 160 test scans, reporting ICC(2,1) absolute agreement with CI, Bland-Altman bias and limits with a proportional-bias check, and window-level σ. (3) Translation into SEM, the smallest detectable change and attenuation of effect sizes, judged against the between-subject SD. With the default window, the LM Finet's SDC is about 0.08 to 0.10, roughly one between-subject SD, so it only supports group-level inference.

### Cited Findings
- There are ten ICC forms. Studies must report model, type and definition. Interpretation bands are < 0.5 poor, 0.5 to 0.75 moderate, 0.75 to 0.9 good and > 0.9 excellent, judged on the 95 % CI rather than the point estimate [CITED] — [Koo and Li 2016, J Chiropr Med](https://pmc.ncbi.nlm.nih.gov/articles/PMC4913118/)
- Agreement between two measurement methods should be assessed by the mean difference and limits of agreement plotted against the mean, not by correlation [CITED] — [Bland and Altman 1986, Lancet](https://www-users.york.ac.uk/~mb55/meas/ba.pdf)
- The main distinction among ICC equations is whether systematic error enters the denominator: ICC(2,1)/(2,k) include it and ICC(3,1)/(3,k) exclude it. The SEM derived from the ICC gives the minimal difference needed to be confident that a true individual change occurred [CITED, abstract] — [Weir 2005, J Strength Cond Res 19(1):231](https://pubmed.ncbi.nlm.nih.gov/15705040/)

### Inferences
**Tier 1: synthetic tests [DERIVED protocol; the phantom code exists in scratch and runs in about 1 minute on one CPU]**
1. *Algebra tests* (exact, no image): scale invariance (r → c·r leaves all five descriptors unchanged to 1e-12); the additive-bias slopes dq/db = (1−q)/r0 and dF/db = (1−2F)/(r1+r2) against finite differences; the exponent gain dn = (n²/H)(Σp_i d ln r_i − d ln r0) against a finite difference; n undefined iff max(r1, r2) ≥ r0.
2. *Cylinder suite*: R ∈ {0.75, 1, 1.25, 1.5, 2, 2.5, 3} mm at 0.5 mm isotropic, ≥ 12 random orientations and sub-voxel offsets. Masks: binary, PV plus Gaussian PSF σ ∈ {0, 0.3, 0.5} mm thresholded at 0.5, ellipticity b/a ∈ {1, 0.8}. Pass criterion for the EDT on a binary mask: |bias| ≤ 0.05 mm (observed 0.011 to 0.046). Record, rather than fail, the blur and ellipticity biases (Q2 table) as the known error model.
3. *Y-phantom suite*: (r0, r1, r2) spanning LM-like (2.0, 1.6, 1.3), unequal (2.0, 1.7, 1.0) and side-branch/distal (1.5, 1.3, 0.8) and (1.0, 0.8, 0.5); angles 50°, 80° and 110°; random rotation. Add perturbations: (a) resampling native → 0.5 mm with linear interpolation of the PV image before thresholding, the path ImageCAS-X's `volumes_resampled` takes; (b) centerline jitter of 0.1 and 0.25 mm iid; (c) a filleted junction (union smoothed by a morphological closing of radius 0.5 to 1 mm) to create a real flare. Pass criterion: at the default window, |F̂ − F| ≤ 0.01 and |q̂ − q| ≤ 0.02 at σ_PSF ≤ 0.3. Report the σ_PSF = 0.5 failures as the small-vessel limit.
4. *Window-scan test*: over k ∈ {0, 0.5, 1, 1.5, 2} and L ∈ {2, 3, 5} mm, the chosen window must lie on a plateau of the bias curve, i.e. |F̂(k ± 0.5) − F̂(k)| ≤ 0.01 in phantoms. It does for k = 1 and L = 3 (Q3).
5. *Exponent test*: at σ = 0.1 mm the MC must reproduce SD(n) ≈ 0.6 at LM radii and ≈ 1.0 at side-branch radii, and an unsolvable rate of ≈ 15 % for r1/r0 = 0.9. That documents why n is reported as descriptive only.

**Tier 2: reference vs CAS-Net on the 160 test scans [protocol; not runnable now]**
- CAS-Net predictions do not exist yet (`$ImageCAS_X_results_path/cas_net_pretrained` holds only the weight symlink). Run `jobs/infer_eval_cas_net.sh` first. The predicted mask then needs a centerline and labels. The simplest correspondence-safe design is to *evaluate the predicted mask's EDT on the GT centerline points*, which isolates segmentation error from centerline and labelling error. Then repeat with extracted predicted centerlines to get total error.
- Per descriptor and site (LM first): ICC(2,1) absolute agreement with 95 % CI (Koo and Li reporting), Bland-Altman bias and 95 % limits of agreement, regression of difference on mean to detect proportional (radius-dependent) bias, and window-level σ̂ = SD(r̂_pred − r̂_GT)/√2 per limb. The √2 assumes equal error in both, so also report the raw SD. Stratify by the `Descriptors.xlsx` image quality.
- Detection rate: the fraction of cases where the LM junction is found in both (36 of 40 on GT alone), and the caliber-anomaly rate in each.

**Tier 3: minimum detectable difference [DERIVED, using MEASURED between-subject SD and the earlier report's ICCs]**
- SEM = SD_between·√(1 − ICC). SDC (individual level) = 1.96·√2·SEM (Weir-type minimal difference). Attenuation: an observed correlation is ρ_true·√ICC, and the sample size for a fixed power scales by 1/ICC.
- LM Finet: SD_between = 0.094 (N = 36, default window). At ICC 0.85 (method) SEM = 0.036 and SDC = 0.101. At ICC 0.90 (window) SEM = 0.030 and SDC = 0.082. **The SDC is about 0.9 to 1.1 between-subject SDs**, so individual-level classification is not supported. A group-level difference of 0.3 SD (0.03) is detectable with an inflation of about 1.1 to 1.2 in N.
- Daughter ratio: SD_between = 0.105. At ICC 0.63 SDC = 0.177 (1.7 SD) and N inflates 1.6-fold; at ICC 0.86 SDC = 0.109.
- r_LAD/r_LM and r_LCx/r_LM: SD_between = 0.155 and 0.180. Their window |Δ| of 0.10 to 0.12 at k = 0 is two-thirds of an SD, so fixing the window is not optional.
- **Upper bound on real window-level noise [DERIVED + MEASURED]**: at the cohort-median radii (1.49, 1.21, 1.12 mm) the Finet noise gain is 0.058 per 0.1 mm. Because the observed total SD of 0.094 must exceed the noise SD, σ_window ≤ 0.094/0.58 ≈ 0.16 mm for GT-derived EDT radii. Tier 2 should find CAS-Net-vs-GT σ̂ below this, or CAS-Net noise would dominate the between-subject signal.

### Gaps
- No published reliability study of CT-derived Finet or daughter ratios was found to benchmark against. The only ICCs available are this project's own (earlier report).
- Scan-rescan reliability (the quantity the CGPS ten-year analysis actually needs) cannot be measured on ImageCAS-X, which has one scan per patient. Tier 2 gives the method component only.

## Q5. Radius profile across the LM bifurcation on ImageCAS-X reference cases

### Takeaway
On N = 36 test-split reference cases [MEASURED], the EDT radius along the daughters starts 23 % (LAD) and 43 % (LCx) above the downstream plateau. It settles within 5 % by a median of 1.5 mm (LAD) and 2.5 mm (LCx), about 1.25·r_J and 2.25·r_J, with IQR upper ends of 3.0 and 5.0 mm. On the LM side the excess is small (median 1.10 at the node) and irregular. The default k = 1, L = 3 window therefore clears the median LAD flare but not the LCx flare in about half of cases.

### Cited Findings
- No external source reports a CT-derived radius profile across the LM bifurcation in r_J units. The only comparable external convention is the EBC's use of 5 mm reference and 3 mm ostial segments — [EBC QCA consensus](https://eurointervention.pcronline.com/article/quantitative-angiography-methods-for-bifurcation-lesions-a-consensus-statement-update-from-the-european-bifurcation-club)

### Inferences
- Values are those in the Q3 tables (`lm_profile.txt`). Additional descriptor medians at the default window (N = 36): r_LM 1.485 mm, r_LAD 1.214 mm, r_LCx 1.121 mm, r_LAD/r_LM 0.884, r_LCx/r_LM 0.774, Finet 0.615 and DR 0.884. Between-subject SDs are 0.155, 0.180, 0.094 and 0.105 respectively.
- Because the LCx flare commonly extends past 1·r_J (≈ 1.5 mm), the default window [1·r_J, 1·r_J + 3 mm] averages some of it into r_LCx. This biases r_LCx/r_LM up and the Finet ratio down in a subset of cases. A defensible, pre-registered alternative is a later start, e.g. k = 2 (about 3 mm). Only the uniform version (k = 2 for all three limbs) was measured here: the Finet ratio moves by 0.023 and r_LCx/r_LM by 0.036 (median |Δ|, L = 3). A daughter-only k = 2 with parent k = 1 is untested. The choice should be fixed before any CGPS outcome is seen and reported as a sensitivity analysis.
- These numbers come from 36 cases, one reader's GT masks and one estimator (EDT on the delivered centerline). They describe the measurement, not coronary anatomy.

### Gaps
- The same profile on CAS-Net predictions (to see whether the network smooths the carina and changes the flare length) awaits Tier 2.
- The area-equivalent radius profile, which would separate true luminal flaring from inscribed-sphere geometry, was not computed.
