# Does the information-matched functional rung (FPCA) extend to a 3 mm bifurcation window?

Scope: the project's own precedent
([fair_baseline_methodology.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Fair%20diameter%20scalars%20for%20regression/fair_baseline_methodology.md)
Q2) proposed functional logistic regression on FPCA scores (citing logitFD and Goldsmith et al.
2011's penalised functional regression, itself built on DTI tract profiles) as the information-
matched comparator between a scalar-mean regression and a per-point network, for the *whole-vessel*
profile. This note asks whether the same machinery is sound at the much shorter, junction-specific
window the diameter report defined: `[1·r_J, 1·r_J + 3 mm]` per limb.

## Q1. How many points does the junction window actually contain?

### Takeaway
**About 6 to 7 points per limb, at the resolution the repo actually trains and infers on.**

### Inferences [DERIVED from repo facts already established in CLAUDE.md and the diameter report]
`volumes_resampled/` and `segmentations_resampled/` are the 0.5 mm isotropic cache CAS-Net trains
and infers on (per this project's CLAUDE.md). A 3 mm window at 0.5 mm centerline-point spacing is
therefore roughly 6 to 7 centerline points, before whatever smoothing or resampling the radius
profile itself receives. The reference (native-resolution) masks used for `lm_profile.py` in the
diameter report have finer in-plane spacing (0.32 to 0.40 mm), so the reference-side window is
marginally denser, at most 8 to 9 points, but the CAS-Net-derived Herlev-Østerbro pipeline the
thesis actually targets will run at 0.5 mm. This is the resolution that matters for a design
decision meant to generalise to CGPS.

### Gaps
This is arithmetic on the repo's own stated resolution, not a fetched literature number, and it
has not been checked against what `topology/angles.py`'s actual window extraction returns as a
point count on a real case; that would be a one-line diagnostic, not yet run.

## Q2. Does the sparse-FPCA literature (irregular, few-points-per-subject data) say anything usable here?

### Takeaway
**Not directly transferable, and it would be a citation-shopping mistake to use it as if it were.**
The sparse-FPCA literature (Yao, Müller and Wang-style PACE methods, James's sparse principal
component models) addresses a different axis of sparsity: each *subject* is observed at only a few,
often *irregularly spaced*, time points, and information is pooled *across subjects* to estimate a
shared covariance surface. The junction window is the opposite regime: every subject (all ~800
scans) is observed at a short but *regular*, *densely and identically sampled* 3 mm domain (0.5 mm
spacing, same nominal window definition for everyone). This is "densely observed on a short
domain", not "sparsely observed on a long domain", and the estimation problems are not the same
problem even though both involve "few points".

### Cited findings
- "Curves are often measured at an irregular and sparse set of time points which can differ widely
  across individuals... In sparse settings, each curve is observed at only a few time points, making
  it difficult to directly compute the covariance function." The standard fix (PACE, conditional
  expectation) exists specifically for that cross-subject pooling problem [SNIP] ([search summary
  covering James et al. and PACE-family methods](https://hastie.su.domains/Papers/fpc.pdf)).
- "In standard principal component analysis it is often possible to estimate well the first few
  eigenvectors even if the fitted covariance matrix is unstable. However, in functional principal
  component analysis this is generally not the case" [SNIP], underscoring that FPCA eigenvector
  estimation is more fragile than ordinary PCA even in the favourable, densely-observed regime this
  project is actually in, let alone the sparse one.

### Inferences [DERIVED]
Because the junction case is densely, regularly and identically sampled across ~800 subjects, the
relevant risk is not "can a covariance surface be estimated from sparse per-subject sampling" (it
can, trivially, since every subject has the same ~6 to 7-point grid); it is **"how many genuinely
distinguishable modes of variation can 6 to 7 points support before the higher components are just
fitting noise"**. A smooth basis of 3 to 4 knots, the number already named as standard practice
elsewhere in this project's own spline recommendations (restricted cubic splines, 3 to 4 knots, for
continuous scalars), already consumes half or more of the window's degrees of freedom. In practice
this likely limits the junction window to one or two stable functional components: something close
to the window's overall level (which the median scalar already captures) and something close to a
linear trend or decay rate along the window (which is close to, and may be redundant with, the
flare-decay quantities the diameter report already measured directly, e.g. "flare end" and the
plateau-normalised profile table).

### Gaps
This is a reasoned inference from repo facts and general FPCA behaviour, not a literature-sourced
number, and it has not been checked empirically. It should be, before anyone commits engineering
time to a junction-level FPCA/pfr implementation: the concrete test is to fit FPCA on the real
ImageCAS-X window data (the 36-case LM profiles already extracted for the diameter report, or a
larger re-pull) and look at the eigenvalue decay: if the second eigenvalue explains only a few
percent of variance beyond the first, that confirms the window supports effectively one functional
mode, and a scalar summary is not leaving useful signal on the table. **This diagnostic has not
been run.** It is a short script (fit FPCA on the existing `lm_profile.py`-style window matrix,
report the eigenvalue spectrum), not yet written, and should live in the repo, not a scratchpad,
if it is written, since it is a one-time design check rather than a per-scan artefact.

## Q3. What does this imply for the B3 rung at the junction scale?

### Takeaway
**Skip a dedicated FPCA/functional-regression rung at the junction window. Use a short, fixed,
pre-registered summary-stat set instead (the B2 rung), and reserve genuine functional regression
for the whole-vessel profile, where the point count (tens to low hundreds along a full coronary
segment) is the regime Goldsmith et al. 2011's DTI-tract-profile precedent and the logitFD package
were actually built for.**

### Inferences [DERIVED]
This is not a claim that functional methods never apply to short windows in principle; it is a
claim that the specific 3 mm, ~6-point ImageCAS-X/CGPS junction window is below the point count
where the information-matched functional rung is likely to add anything beyond what a 2 to 3 number
summary (window median, endpoint-to-plateau ratio, a coarse slope) already gives, and that
implementing it anyway risks manufacturing spurious components that then need their own
overfitting safeguards for no evidenced benefit. The project's own EPV-style caution against adding
parameters without an evidence bar
([Scalar tortuosity metrics for CAD models.md](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Scalar%20tortuosity%20metrics%20for%20CAD%20models.md))
applies here directly: an FPCA rung that supports at most one or two real components is not buying
enough information-matching to be worth its own parameter and validation cost, when the network's
"sees every point" asymmetry is already fully captured by handing it the raw masked profile
directly (Q3 of [fusion_mechanics.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Bifurcation%20calibre%20in%20both%20models/fusion_mechanics.md)).

### Gaps
The eigenvalue-decay diagnostic in Q2 would let this be stated as measured rather than reasoned.
Until it is run, this recommendation should be treated as a design default open to revision, not a
locked decision, and should not be cited elsewhere in the thesis as settled.
