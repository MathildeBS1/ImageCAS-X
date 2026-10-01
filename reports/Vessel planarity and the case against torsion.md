# Vessels sit within 2% of a plane; torsion still reports 0.5 mm-1

Named coronary vessels are close to planar curves. Run on the 160-case test split
through the delivered ground-truth centerlines (`topology.tortuosity.extract_case`,
default 1 mm Gaussian smoothing), the third principal axis of a vessel's own shape,
`non_planarity`, carries well under 1.1% of that vessel's total spread in every one
of the four named vessels, and the RMS perpendicular distance from each vessel's own
best-fit plane, `plane_d_rms_norm`, is only 0.5-2.3% of the vessel's own arc length:

| vessel | n | out-of-plane variance (median) | RMS distance from own plane (median, % of length) | tangent angle off plane (median) | torsion, mean \|τ\| (mm⁻¹) |
|---|---|---|---|---|---|
| LM  | 159 | 0.01% | 0.52% | 3.0°  | 0.551 |
| LAD | 160 | 0.72% | 2.10% | 16.0° | 0.505 |
| LCX | 160 | 0.65% | 2.11% | 14.0° | 0.517 |
| RCA | 158 | 0.30% | 1.26% | 9.2°  | 0.566 |

LM is nearly a straight line lying in a single plane; LAD and LCX are the most
twisted, and even they deviate from their own best-fit plane by only about 2% of
their own length. Yet on the same centerlines, with the same code, torsion averages
0.50-0.57 mm⁻¹ everywhere, vessel to vessel, with no relationship to how planar the
vessel actually is. A torsion of ~0.53 mm⁻¹, if it were a real, sign-consistent
rotation, would rotate the curve's osculating plane a full turn (2π) roughly every
12 mm (`2π / 0.53 ≈ 11.9 mm`). Nothing in the planarity numbers above supports a
vessel corkscrewing once every 12 mm; the LAD's own shape says under 1% of its
variance leaves a single plane over its *entire* length, not once every centimetre.
The two readouts, geometry says flat, torsion says twisting, cannot both be
describing the same curve.

## Why they disagree: torsion is a third derivative, planarity is not

`topology/tortuosity.py`'s own docstring states the reason directly: "the distance
metric needs none, SOAM and the inflection count need one, curvature needs two,
torsion needs three. Each extra derivative amplifies whatever position noise sits in
the centerline." Concretely:

- `non_planarity` and `plane_d_rms_mm` come from a PCA of the raw point positions,
  zero derivatives. They are close to a direct readout of where the centerline
  actually sits.
- `plane_angle_mean_deg` uses the unit tangent, one derivative (a finite difference
  between adjacent points).
- Torsion is `τ = (d1 x d2)·d3 / |d1 x d2|²`, built from first, second *and* third
  derivatives of position (`np.gradient` applied three times in `measure()`). Each
  differentiation is a discrete difference divided by a small step, and each one
  multiplies whatever sub-voxel jitter sits in the centerline by roughly `1/step_mm`.
  By the third derivative, position noise that is invisible in the raw points has
  been amplified enough to dominate the signal, which is why `torsion_mean_abs` is
  masked to only the points where curvature is at least 10% of that vessel's own
  peak (`TORSION_KAPPA_FRACTION`) and still comes out order-0.5 mm⁻¹ on curves that
  are, by every zero- and one-derivative measure, nearly flat.

This is not specific to this pipeline. Chartrand's foundational result on
differentiating noisy data is explicit that "denoising the data before or after
differentiating does not generally give satisfactory results... the real secret is
to regularize the differentiation itself"
([Chartrand 2007](https://jasoncantarella.com/downloads/chartrand-2007-numerical.pdf)),
and a paper applying the same Frenet-Serret framework to noisy 3D curves treats
curvature and torsion jointly as a penalized-spline fitting problem for exactly this
reason ([arXiv:2203.02398](https://arxiv.org/html/2203.02398)). The vascular-specific
evidence is a direct analogue: a carotid bend-detection study found the number of
detected bends swings from 3 to 33 purely as a function of centerline resolution and
smoothing choice, with the raw coordinate noise held fixed
([PMC8626959](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)); torsion, needing
one more derivative than curvature, should be at least as resolution-sensitive.

A further tell is in the *sign*, not just the magnitude: `torsion_mean_abs` is a mean
of `|τ|`, and it stays around 0.5 mm⁻¹ even though the planarity numbers above rule
out a large, consistent net rotation. A real helical course would accumulate a
consistent-sign torsion over some run of the vessel; a mean-absolute value this large
next to a non-planarity this small is the signature of a torsion trace that flips
sign rapidly from point to point, i.e. numerical noise scattering around zero rather
than a coherent 3D twist.

## Where this fits the locked decision

This does not change a decision, it gives the existing one a number on this
project's own cohort. Torsion was already excluded from both Model 1 (as a scalar
covariate) and Model 2 (as a profile channel) on noise-instability and
zero-outcome-evidence grounds
([Scalar tortuosity metrics for CAD models.md](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Scalar%20tortuosity%20metrics%20for%20CAD%20models.md)),
and a subsequent pass concluded a magnitude-threshold denoising fix cannot rescue it,
because the error is systematic and pipeline-tied rather than the kind of noise a
threshold suppresses
([Torsion threshold to filter noise.md](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Torsion%20threshold%20to%20filter%20noise.md)).
The planarity comparison here is consistent with both: on a cohort where the true
geometric signal torsion is supposed to measure is, by construction, small (these
vessels are close to planar), the estimator still reports a magnitude around
0.5 mm⁻¹ uniformly across all four named vessels regardless of how planar each one
actually is. That flatness of the estimator's output, when the true underlying
signal should vary the way `non_planarity` does, is itself evidence the estimator is
reporting its own noise floor rather than anatomy.

---
Reproducibility: `scripts/check_vessel_planarity.py`, test split (`filelist/test.txt`,
160 cases), delivered ground-truth centerlines, `topology.tortuosity.extract_case`
defaults (`sigma_mm=1.0`, `step_mm=0.25`). Run with `source env.sh && python
scripts/check_vessel_planarity.py`.
