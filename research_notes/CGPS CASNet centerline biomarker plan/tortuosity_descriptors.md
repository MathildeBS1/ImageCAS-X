# Tortuosity and geometry descriptors: consolidation of existing investigation

Synthesis of nine reports in `reports/` (and their `research_notes/` backing folders) plus
the committed code in `tortuosity/`. Nothing here is new research; every number and formula
below is traced to a specific report. Sources are cited inline as `[report file]`. The
underlying `research_notes/<Report name>/*.md` files were consulted for cross-checks but
the reports themselves are the synthesis layer and are quoted preferentially, since they
already reconcile the sub-notes.

Chronology matters: reports were written in this order and each later one revises earlier
ones. Read top to bottom for the current position, not the historical one.

1. `Merged tortuosity methods for coronaries.md` (2026-09-22, earliest)
2. `Alternative tortuosity merges for coronaries.md` (2026-09-22)
3. `Choosing a coronary tortuosity descriptor.md` (2026-09-25)
4. `Vessel specific tortuosity math and tests.md` (2026-09-25, supersedes 3 on the primary metric)
5. `Plaque prone regional geometry descriptors.md` (2026-09-26)
6. `Centerline tortuosity normal ranges.md` (2026-09-26)
7. `Two centerline tortuosity case study.md` (2026-09-26)
8. `Tortuosity protocol readiness and CT FFR.md` (2026-09-26, latest, audits 4-6)
9. `Investigation priorities across reports.md` (2026-09-26, cross-report synthesis and priority list)

**Bottom line the reports converge on:** the primary whole-vessel tortuosity descriptor is
mean absolute curvature from chord turning angles, **κ_a**, computed at a 5 mm chord on the
centerline as delivered (no extra smoothing, per the normal-ranges report) or at σ = 1 mm
extra Gaussian smoothing (per the vessel-specific report). Arc/chord (**TI = L/D − 1**) is
demoted to a secondary, literature-comparability variable because it is dominated by vessel
length and cardiac dominance, not local bending. This reverses the original recommendation
in the earliest two reports, which had ranked arc/chord first and a Grisan-style turn layer
second. **None of this is frozen or reproducible yet**: nearly every cited number comes from
scripts that live in session `/tmp` scratchpads, not from committed code, and the readiness
audit (`Investigation priorities across reports.md`) names this as the single most urgent
gap before any number can be cited in the thesis.

---

## 1. Descriptors evaluated, with exact formulas

Notation used throughout the reports: `L` = smoothed arc length of the centerline segment;
`D` = end-to-end chord (Euclidean straight-line distance between endpoints); `ℓ` = a fixed
resampling chord length in mm; `θ_j` = turning angle between consecutive unit chord
directions; `κ(s)` = curvature as a function of arc length; `σ` = the extra Gaussian
smoothing width applied on top of the delivered centerline (which itself already carries a
dataset-level σ = 0.5 mm, 5-vertex smoothing, per `Centerline tortuosity normal ranges.md`).

### 1.1 Arc/chord ratio (distance metric / tortuosity index, DM / TI)

`DM = L / D`, and `TI = DM − 1 = L/D − 1`.
Source: appears in every report; formalised in `Choosing a coronary tortuosity descriptor.md`
and `Centerline tortuosity normal ranges.md`.

A 2D/projected variant, **DM2**, is the same ratio computed after projecting the 3D
centerline onto the plane normal to a viewing direction `d = (sin α cos β, −cos α cos β,
sin β)` with `α` the LAO/RAO angle and `β` the cranial/caudal angle, using per-vessel
standard angiographic views (LAD RAO 20/CRA 30, LCx RAO 20/CAU 30, RCA LAO 30). This exists
purely to compare against angiography literature that only ever measured 2D projections
(`Centerline tortuosity normal ranges.md`).

**Identity connecting arc/chord to the tangent field** (`Vessel specific tortuosity math
and tests.md`): let `T̄` be the mean unit tangent vector along the curve and `V = 1 − |T̄|²`
the tangent variance. Then `D = L|T̄|` exactly, so

```
L/D = (1 − V)^(−1/2)        and        TI ≈ V/2   (for small V)
```

verified to 1e-5 relative error on 300 random 3D curves. This shows TI is (half) the
zeroth moment of the tangent-direction power spectrum, i.e. it is dominated by long, gentle
bends, not tight local ones.

### 1.2 Mean absolute curvature from chord turning angles (κ_a), a.k.a. the SCC density

Resample the centerline at a fixed chord length `ℓ` (mm) to get unit chord directions
`u_1, ..., u_n`. Turning angle `θ_j = arccos(u_j · u_{j+1})`. Then

```
κ_a = (Σ_j θ_j) / L         [units: mm^-1]
```

Equivalently `κ_a = K / L` where `K = Σθ_j` is total absolute turning (in radians). This is
identical to the "slope chain code (SCC) density" derived from Mateos et al. 2024's 2D chain
element `a_n = θ_n/π` (the discrete 2D SCC tortuosity is `τ = Σ|a_n|`, so `κ_a` = `π ×` that
density) and is stated to be the same family as Bullitt's sum-of-angles metric with the
torsion term dropped. Source: `Merged tortuosity methods for coronaries.md`, `Alternative
tortuosity merges for coronaries.md`, `Vessel specific tortuosity math and tests.md`.

`K = κ_a · L` (total turning in radians) is reported as a dimensionless companion, additive
under tree aggregation (a vessel's `K` is the sum of its segments' `K`).

### 1.3 RMS curvature and the concentration ratio Q

`κ_r` = root-mean-square curvature at the same chord `ℓ`: `κ_r² = (1/L)·Σ_j θ_j²/ℓ` (a
second moment of turning, vs. κ_a's first moment).

```
Q = (κ_r / κ_a)² = L · Σ(θ_j²/ℓ) / (Σθ_j)²
```

Q is dimensionless, never below 1 (equal only for constant curvature), and rises without
bound as turning concentrates into fewer, sharper bends. It is built from the same two
curvature moments Kashyap 2022 used against wall-shear-stress data. Source: `Merged
tortuosity methods for coronaries.md` (proposed as co-primary with κ_a), later **dropped**
in `Alternative tortuosity merges for coronaries.md` and `Vessel specific tortuosity math and
tests.md` (see §2 and §8 below: it is non-monotone even noise-free and behaves like pure
measurement noise on real centerlines, median 1.28-1.43 vs. 1.24-1.35 on pure jittered
lines, `4/π ≈ 1.27` being the noise value).

### 1.4 Grisan's turn-segmented tortuosity density

```
τ = ((n − 1)/n) · (1/L_c) · Σ_i (L_c,si / L_χ,si − 1)
```

`L_c` = total arc length, `n` = number of "turn curves" (constant-curvature-sign segments),
`L_c,si` and `L_χ,si` = arc length and chord length of the i-th turn segment. Scores exactly
0 for a single-sign course (one C-shape or a helix), by design, because `n = 1` zeroes the
`(n-1)/n` factor. The original 2D definition uses a sign change of *planar* curvature to
split turns; a 3D space curve has no signed curvature (`κ = |r′×r″|/|r′|³` is always ≥ 0),
so the split needs a substitute "twist" detector. Source: `Merged tortuosity methods for
coronaries.md` §"Grisan's formula is dimension-free except for its twist detector", eq.
numbering (Grisan 2008 eq. 19) preserved from the original paper.

Twist-detector candidates tried, ranked by the reports:
- **Binormal flip** (original proposal): `b_j = u_j × u_{j+1}` (normalised); a twist is
  flagged where `b` reverses sign across a low-turning run. Superseded because it is a
  per-sample test in the torsion family and is noise-dominated.
- **Parallel-transport (PT) curvature-vector angle** (Bogunović-style, adopted as the
  better-evidenced 3D turn rule in `Alternative tortuosity merges for coronaries.md`): the
  curvature vector is `k1·E1 + k2·E2` in a rotation-minimising frame; a bend boundary is set
  where the PT angle between consecutive curvature peaks exceeds a threshold `α`. Evidenced
  from Kjeldsberg 2021 (carotid): CV < 5% for the PT/Bogunović detector vs. 47% for a
  torsion-extrema (Piccinelli) detector — a carotid result, not a coronary one.

`grisan3d` **is implemented in code** at `tortuosity/merged.py` (see §9), using the binormal
flip, not the later-recommended PT-angle detector, i.e. the code implements the version the
later reports say is inferior.

### 1.5 Bullitt's Sum-of-Angles Metric (SOAM) and Inflection Count Metric (ICM)

Recovered in full text in `Merged tortuosity methods for coronaries.md` /
`Alternative tortuosity merges for coronaries.md`:

```
SOAM = Σ_i √(IP_i² + TP_i²) / path length
```

`IP` = in-plane (curvature) turning angle, `TP` = out-of-plane (torsion) turning angle,
with **`TP` explicitly set to 0 at a detected inflection point**. An inflection is defined as
a local maximum of `ΔN · ΔN` above 1.0 (`N` = Frenet normal; roughly 4 at a true 180-degree
normal flip), sampled at one-voxel intervals on a spline with a Frenet frame from finite
differences.

```
ICM = (number of inflections + 1) × DM        [DM = L/D]
```

**Both are reported as unusable on the ImageCAS-X centerlines as delivered.** SOAM's torsion
term (`TP`) reads about 7.1-7.3 rad/cm on every trunk regardless of true shape, 7-10x its
in-plane part, because torsion between consecutive ~1 mm osculating planes is pure noise
(`Centerline tortuosity normal ranges.md`). On a purely planar curve SOAM reduces to the sum
of turning angles per length (i.e. to `κ_a` up to a constant), since Bullitt's own formula
zeroes the torsion term there — a correction the reports make explicitly against an earlier,
wrong claim that SOAM "adds π per inflection on planar curves."

### 1.6 3D chain-code torsion (Bribiesca-Sánchez 2024, "3D-SCC")

Read in full in `Merged tortuosity methods for coronaries.md`:

```
τ = Σ_j |α_j| + Σ_j |β_j|
```

`α_j` = signed slope-chain element in `(−1, 1)` (the 3D analogue of Mateos's `a_n`), `β_j` =
signed torsion-chain element in `[−0.5, 0.5]`. Invariant to translation, rotation and uniform
scaling. **Flagged as the least reliable quantity to extract from 0.5 mm centerlines**: the
discrete binormal `N_j = T_{j-1} × T_j` has magnitude `sin θ_j`, so on a nearly straight,
jittered polyline its direction (and hence the sign of `β`) is set by noise; a jittered
straight line scores a normalised `τ_N ≈ 0.17` from torsion alone. Validation in the source
paper itself is called out as weak (three synthetic knots, 90 sperm flagella, no expert
reference, no noise experiment, and two internal numerical errors in the published tables).

### 1.7 Mateos et al. 2024's τ3D (voxel-surface folding measure) — ruled out, not a centerline metric

`τ3D` (their eq. 8) sums, over the X, Y, Z axes, the per-slice mean absolute turning of
digitised slice-contour boundaries (each element `a_n = θ_n/π` as in §1.6, but applied to a
2D contour, not a 3D curve). **Read in full and ruled unusable on coronary lumens**: it
operates on a voxelised solid via axis-aligned slice contours, has no skeleton or 3D-curve
concept anywhere in the source, is scale- and orientation-dependent (a coronary cross-section
at 0.5 mm voxels is only 2-8 voxels wide, far below the smallest validated sphere radius of
10 voxels), and depends on how many branches a slice cuts. Only the underlying chain-coding
*discretisation principle* (constant-chord turning divided by π) survives and feeds directly
into κ_a / SCC density above. Source: `Merged tortuosity methods for coronaries.md`.

### 1.8 Inflection point count (as a standalone descriptor)

Never adopted as a primary descriptor in any report. Evidence against it: on a Frenet-Serret
robustness study cited in `Choosing a coronary tortuosity descriptor.md`, the
curvature-minimum inflection count rose by up to **439%** in coronaries as sampling
densified — i.e. it is dominated by discretisation noise, not anatomy. In the two-case study
(§4 below), inflection count and ICM both **reversed the visually obvious ranking** between
the two RCAs (`Two centerline tortuosity case study.md`). Verdict: **dropped**.

### 1.9 Bend counts / bend segmentation ("N ≥ 45°", "N ≥ 90°")

Defined operationally in `Centerline tortuosity normal ranges.md`: split the resampled
centerline into maximal runs where the local turning rate exceeds a floor (e.g. 0.02 mm^-1,
i.e. radius under 50 mm), splitting further wherever the binormal flips; a bend's angle is
its cumulative turning; report counts of bends ≥45°, ≥90°, ≥180°, and the binary "≥3 bends
≥45°" popular in the angiography literature (Li 2011). **Fragile by the reports' own
measurement**: the fraction with "≥3 bends ≥45°" swings from 0.88/0.60/0.53
(LAD/LCx/RCA) at σ=1mm/floor 0.02 to 0.37/0.19/0.07 at σ=2mm/floor 0.10 — i.e. it is almost
entirely a function of the arbitrary smoothing and floor choice, not of the vessel. It never
reproduces the angiography literature's LCx > LAD > RCA ordering at any setting tried.
Kept only as a descriptive, angiography-comparable secondary, never as a primary.

### 1.10 Bishop Curvature Spectrum (BCS): the unifying 2D/3D formalism

Introduced in `Centerline tortuosity normal ranges.md` as "the principled merge of 2D and
3D." Transport a rotation-minimising (Bishop/parallel-transport) frame `(T, M1, M2)` along
the curve (Rodrigues rotation from `T_{i-1}` to `T_i`), so that `T′ = k1 M1 + k2 M2`. Define
the **complex curvature**

```
ψ(s) = k1(s) + i·k2(s)          so that |ψ| = κ(s)
```

and its phase advances at the local torsion rate. With Gaussian pre-smoothing at `σ0`:

```
E = ∫ |ψ|² ds                         (bending energy)
kB = √(E / L)                          [mm^-1], the RMS curvature magnitude in this frame
```

Two exact decompositions of `E`:

- **Course/wiggle** (frequency split): take the orthonormal DCT of `ψ`, apply a Gaussian
  low-pass filter `|H_L(ω)|² = exp(−ω²σc²)` with `σc = √(ln 2) · λc/(2π)`, `λc = 20 mm`.
  By Parseval, `E_course + E_wiggle = E` exactly. `f_wiggle = E_wiggle / E`.
- **Planar/twist** (out-of-plane split): with a Gaussian kernel `g_W` of s.d. `W = 5 mm`,
  `E_planar = ∫ |g_W * ψ²| ds` and `E_twist = ∫ (g_W * |ψ|² − |g_W * ψ²|) ds ≥ 0`.
  `f_twist = E_twist / E` (guarded to NaN when `E = 0`).

Properties verified on phantoms: a planar curve gives real `ψ` equal to signed planar
curvature (so Grisan's constant-sign turns are exactly BCS's sign-constant intervals) and
`f_twist = 0`; a helix gives `f_twist = 1 − exp(−2τ²W²)`; rotation, mirror, reversal and
resampling leave `kB` invariant to numerical precision; the four energy parts sum to `E` to
six digits. Every classical index is shown to be a moment of the `ψ` power spectrum: RMS
curvature is moment 0, Grisan's density is approximately turn-length-weighted energy (moment
near −1), arc/chord is approximately `Σ P(ω)/ω² / 2L` (moment −2) — which is the formal
reason arc/chord is dominated by long wavelengths and length.

**Verdict on BCS** (`Centerline tortuosity normal ranges.md`, confirmed in the two-case study
and audited critically in `Tortuosity protocol readiness and CT FFR.md`): the magnitude `kB`
brings nothing new over `κ_a` (Spearman 0.85-0.97 correlated) and is *less* robust to jitter
(ICC 0.25-0.81 under 0.5 mm correlated jitter vs. κ_a's 0.71-0.87). The two *fractions*,
`f_wiggle` and `f_twist`, are the part worth keeping as **exploratory secondaries** — they
carry information beyond κ_a and length (e.g. RCA bending energy is ~75% "course" / baseline
C-shape) but their reliability under realistic (0.5 mm correlated) jitter collapses to
ICC 0.15-0.60, so the later audit explicitly downgrades an earlier "94-99% of unexplained
variance" claim for `f_twist`, since most of that "new information" is measurement noise, not
signal (`Tortuosity protocol readiness and CT FFR.md`).

### 1.11 Regional/bifurcation and radius-based descriptors

From `Plaque prone regional geometry descriptors.md`:

- **Daughter-to-daughter bifurcation angle**, using the `fitcore3` tangent definition: fit a
  line to the centerline over `[r_J, r_J + 3 mm]` from the junction (`r_J` = junction
  radius), for each daughter, then take the angle between the two fitted directions. Found
  far more stable across smoothing (78.0-80.8°) than a naive secant tangent (drifts 63-99°
  as σ varies 0-2mm), because a chord-endpoint error `σ` over chord `d` gives angular error
  `≈ √2·σ/d`.
- **Finet ratio**: `r0 / (r1 + r2)`, parent radius over sum of daughter radii, measured over
  `[r_J, r_J+3mm]` with the mask Euclidean-distance-transform (EDT) radius. Reliable at the
  left main (ICC 0.85-0.90, close to the literature's Finet ≈ 0.678, itself unverified);
  degrades at side branches and fails at the crux (ICC 0.44).
- **Daughter diameter ratio**: smaller/larger daughter radius. Size-free, ICC 0.63-0.86.
- **Curvature ratio (Dean-parameter proxy)**: `δ = κ_l5 · r`, a dimensionless local
  curvature×radius product, proposed as a low-wall-shear-stress proxy (a derivation, not a
  measured/validated quantity — flagged explicitly in `Investigation priorities across
  reports.md` as having "no traceable computation anywhere, even in scratch" and should be
  treated as **unmeasured**).
- **Murray's law exponent** and **pointwise proximal taper**: tested and **dropped**. The
  Murray exponent is unsolvable in 12-37% of bifurcations (method ICC 0.48-0.69); taper's
  pointwise error (~0.035) exceeds the normal taper signal (~0.0125) at a 10 mm baseline.
- **Frenet finite-difference curvature** (the version implemented in the pre-existing,
  non-`tortuosity/`-owned `topology/tortuosity.py`): explicitly rejected — collapses to
  ICC 0.06-0.21 under the 0.25 mm iid noise stress test, versus κ_l5's 0.70-0.91.
- **Torsion** (any 3D form): consistently rejected across every report as one derivative
  order too noisy; jitter ICC 0.24-0.41 even at 0.1 mm noise; rank order between σ=0.5 and
  2mm is uncorrelated (Spearman −0.15 to 0.01).

### 1.12 Descriptors flagged as degenerate or dropped outright (case-study evidence, §4)

Writhe (essentially zero for near-planar bending without coiling; only a genuine helix scores
non-trivially), box-counting fractal dimension (0.938 vs 0.940 for two visually very
different RCAs — degenerate for a smooth single trunk), average crossing number (plausible
but unvalidated, confounded with projection/view), SRVF elastic distance to a straight line
(restates arc/chord, adds nothing new). Source: `Two centerline tortuosity case study.md`.

---

## 2. Merging multiple tortuosity metrics into one index: conclusion is "no"

Both merge-focused reports (`Alternative tortuosity merges for coronaries.md`, earlier;
`Merged tortuosity methods for coronaries.md`, even earlier) conclude that **merging Mateos's
chain-code substrate with Grisan's turn-segmentation idea is possible only in a narrow
technical sense**, and that no single blended/weighted composite index should be adopted.

- **What actually merges cleanly:** Mateos's discretisation principle (constant chord `ℓ`,
  turning angle divided by π) supplies the substrate; Grisan's turn-segmented arc/chord-excess
  aggregation (eq. 19, §1.4) supplies the idea of splitting a curve into turns and scoring
  them locally. This yields the `grisan3d` function actually implemented in
  `tortuosity/merged.py`.
- **What does not merge:** Mateos's actual `τ3D` (a voxel-surface measure, §1.7) cannot be
  ported to a 3D centerline at all; it is discarded, and only its discretisation idea is kept.
- **The recommended non-blended pair**, settled in `Alternative tortuosity merges for
  coronaries.md`: report `κ_a` (magnitude/first moment) and `Q = (κ_r/κ_a)²`
  (concentration/second-moment ratio, §1.3) **side by side, never combined into one number**.
  This pair was chosen because it needs no extra detector or threshold beyond `ℓ`, and it
  covers three of the four known weaknesses of a Grisan-only or SCC-only approach (helix/C
  blindness, radius blindness at fixed chord, non-monotonicity in amplitude). It cannot fix
  the fourth (distinguishing an S-bend from a C-bend of equal total turning), for which a
  Grisan/PT turn layer was kept only as a rank-3 "challenger," not a primary.
- **This recommendation is itself later reversed**: `Vessel specific tortuosity math and
  tests.md` **drops Q outright**, not merely demotes it, because (a) it is non-monotone even
  in noise-free synthetic tests (reversing the one noise-free check that originally justified
  keeping it) and (b) on the 560 real training centerlines its median (1.28-1.43) is
  statistically indistinguishable from its value under pure measurement noise (`4/π ≈ 1.27`),
  and it shows **no** within-patient coherence (|Spearman ρ| ≤ 0.16 across a patient's own
  vessels), unlike κ_a (cross-vessel ρ up to 0.60).
- **Composites/weighted blends in general**: explicitly evidenced against. The comparative-
  evidence section of `Merged tortuosity methods for coronaries.md` reviews every published
  attempt to combine multiple tortuosity/curvature formulas into a single score and finds
  that **every composite that beat a single metric did so by adding non-tortuosity
  information** (caliber, bifurcation angle, CFD-derived haemodynamics, a supervised
  discriminant) — never by combining tortuosity formulas with each other. Two retinal studies
  that combined tortuosity-only metrics gained 0-5 points over the best single metric, or lost
  on one test set. Because ImageCAS-X has no outcome labels to fit combination weights, "any
  composite here has to be structural and unweighted" — and even that unweighted structural
  pair (κ_a, Q) was later abandoned for Q specifically.

**Net conclusion carried forward**: report κ_a and (secondarily) TI/arc-chord side by side.
Do not blend. The turn layer / Grisan-style bend decomposition survives only as a sensitivity
analysis behind pre-registered reliability gates, not as a co-primary.

---

## 3. Normal / reference ranges established, by vessel

**Everything below is a "development distribution" on ImageCAS-X, explicitly not a clinical
normal range.** `Centerline tortuosity normal ranges.md` states this in its verdict box:
ImageCAS-X is a single referred-population cohort (prior stroke/TIA/PAD indication, ~48.5%
plaque prevalence, no age/sex/risk-factor columns in `Descriptors.xlsx`, one cardiac phase
per scan), so "ImageCAS-X numbers are development distributions, never normal ranges." True
normal ranges require CGPS (age, sex, heart size available) and are listed as **not yet
computable** — an open item, not a completed result.

All numbers below computed on **560 training scans** (`compute_simple.py`, committed
parameters σ = 1 mm unless noted; also cross-checked at σ = 0 in the same report), reported
in `Centerline tortuosity normal ranges.md` §"ImageCAS-X reproduces published 2D values":

| Vessel | L, mm (median) | DM = L/D, median [2.5, 97.5 pct] | DM2 (standard 2D view), median (IQR) | κ_a, mm⁻¹, median [2.5, 97.5 pct] | Spearman ρ(DM, length) | Spearman ρ(κ_a, length) |
|---|---|---|---|---|---|---|
| LAD | 131.8 | 1.34 [1.12, 1.72] | 1.20 (1.14-1.29) | 0.057 [0.032, 0.104] | 0.80 | 0.20 |
| LCx | 83.7 | 1.30 [1.05, 1.70] | 1.16 (1.08-1.27) | 0.052 [0.031, 0.099] | 0.84 | 0.26 |
| RCA | 103.7 | 1.77 [1.18, 2.55] | 1.81 (1.58-2.06) | 0.045 [0.031, 0.081] | 0.69 | 0.32 |

An earlier pass in `Vessel specific tortuosity math and tests.md` (P150 sample, σ=1mm,
ℓ=5mm) gives closely consistent medians: **TI 0.32 (LAD), 0.29 (LCx), 0.77 (RCA)**, and
**κ_a 0.047-0.084 mm⁻¹ across all six named vessels** (LAD, LCx, RCA plus D1, OM1, PDA), a
narrower band than TI's factor-of-2.6 spread. That report explicitly warns: "the single
pooled 'main-vessel L/D median 1.45' [from an even earlier report] hides a factor of 2.5
between RCA and LAD, and should not be reported" — i.e. **arc/chord must never be pooled
across vessel types**, only reported per named vessel.

**RCA is dominance-dependent**, not simply "high tortuosity": median RCA TI is **0.29 in
left-dominant** vs. **0.81 in right-dominant** hearts (p = 4e-13, or p=0.00033 in the smaller
P150 dominance subsample of 8 left-/3 co-dominant cases); κ_a does **not** differ by dominance
(0.055 vs 0.046, p=0.31). This is presented as proof that whole-vessel RCA arc/chord mostly
encodes anatomy (how far the vessel must travel around the AV groove and back), not local
tortuosity.

**External validity check against angiography** (`Centerline tortuosity normal ranges.md`):
projecting the 3D centerline into a standard angiographic view (DM2) lands close to the one
per-vessel continuous angiographic study available (Zebić Mihić 2023, obstructive-CAD group):
LAD 1.18 [1.14, 1.26] vs. our 1.20; LCx 1.15 [1.10, 1.30] vs. 1.16; RCA 1.87 [1.65, 2.17]
vs. 1.81. Flagged explicitly as "an external validity check, not a calibration," because that
study did not state its projection views and used diastolic frames only. κ_a medians
(0.045-0.057 mm⁻¹) also sit close to biplane-angiography mean curvature in normal LAD/RCA
(0.050-0.066 mm⁻¹, Zhu 2008), "though the scales differ."

**LM (left main) is explicitly not assigned a tortuosity value.** Median length ~7.3-10.5 mm,
DM ≈ 1.01-1.011, κ_a undefined in 72% of cases at ℓ=5mm. Every report agrees: describe the LM
by length and bifurcation angle/Finet ratio instead, and report tortuosity as an explicit NaN
with a stated reason, never a dropped row.

**Reference-interval methodology recommended** (not yet executed): CLSI EP28-A3c nonparametric
2.5th/97.5th percentiles with 90% binomial CIs (needs ≥120 cases per partition); dominance
enters as a covariate, not a stratum (too few left-/co-dominant cases); DM should use
length- and dominance-conditional centiles via quantile regression or GAMLSS/LMS with a
Box-Cox transform; κ_a can use a log-scale parametric interval (log-skew −0.03 to 0.52).

---

## 4. Two-centerline case study: findings and practical issues

`Two centerline tortuosity case study.md` applied the descriptor set to two length-matched,
right-dominant RCAs (scan 662, 109.4 mm; scan 518, 104.4 mm), one visually a smooth single C
with a short ostial hook, the other a C carrying five visible bends winding out of plane.

**Headline result**: arc/chord differs by only 16% (1.73 vs 2.00, 44th vs 69th cohort
percentile) — nearly indistinguishable — while κ_a@5mm differs by a **factor of two** (0.035
vs 0.068 rad/mm, 10th vs 88th percentile) and matches the eye's reading. In the RAO 30
angiographic projection the arc/chord order even **reverses** (1.40 vs 1.39). Mechanistically:
518's extra 190° of turning alternates in direction and cancels in net displacement, adding
path length only to second order, while every added degree adds linearly to κ_a.

**Practical issues that came up:**

- **Ostium/take-off hook artefact.** 662 has an 88° turn in its first 6.5 mm holding 74% of
  its total bending energy (BCS `kB`). Trimming the first 5 mm drops its `kB` by 42% while
  518 barely moves. This single short segment "decided its max bend" and would remove its
  only counted bend of ≥45° if trimmed. The report concludes: **"an ostium rule (a fixed trim
  or an explicit take-off segment reported separately) must be fixed and pre-registered
  before kB, max κ, persistence or bend maxima are reported."** It is unresolved whether this
  hook is true anatomy or a centerline-extraction artefact at the aortic root; the cohort
  frequency of such hooks has not been measured.
- **Numerical instability / noise at ~1mm scale**: every measure computed at 1 mm scale or
  finer (inflection count, ICM, curvature-peak persistence counts, in-plane SOAM) **reversed**
  the visually obvious ranking of the two vessels. "Every disagreement traces to one of three
  causes: noise at the 1 mm scale ... the ostial take-off hook ... or projection." The
  measures that agreed with the eye all operated at 5 mm or coarser and in 3D.
- **Projection sensitivity**: a single 2D angiographic view (any fixed LAO/RAO/cranial/caudal
  angle) can flip the ranking (RAO 30 arc/chord) or hide bends entirely (the LAO 30 clinical
  "≥3 bends ≥45°" grade was 0 for *both* vessels, unable to separate a 10th-percentile vessel
  from an 88th-percentile one).
- **Sensitivity to smoothing choice** was checked directly for κ_a: percentiles moved only
  from 10.5 to 9.1 (662) and 88.2 to 87.9 (518) between σ=0 and σ=1mm — i.e. κ_a's *ranking*
  was stable to that change, in contrast to the energy-type and peak-count measures above.

**Recommended secondary from this case study**: `f_twist` (BCS out-of-plane energy fraction),
because it separated the two vessels sharply (0.15 vs 0.46, 0.7th vs 94.7th percentile) and
its W-free "tangent-sphere spread" analogue agreed independently. Explicitly demoted/dropped
from this case study: inflection count, ICM, writhe, box-counting dimension, fine-scale
persistence-peak counts, and SRVF distance to a line.

---

## 5. Plaque-prone regional geometry descriptors

From `Plaque prone regional geometry descriptors.md`. These are distinct from the whole-vessel
tortuosity panel: they are anchored at four fixed anatomical locations (left main bifurcation,
proximal 2-17 mm of LAD/LCx/RCA, LAD-D1 and LCx-OM1 take-offs, and the crux) rather than
computed continuously along a vessel.

**Where plaque first appears (literature grounding for site choice)**: in PARADIGM (serial
CCTA, 1,343 patients, median 3.3 years), of 334 baseline-plaque-free patients, 35% developed
new lesions, and **60% of those new lesions were in the LAD**; patients with existing plaque
developed new lesions most often in the RCA (47%). Multislice CT places >90% of left-main
plaques opposite the flow divider (carina spared). This evidence is at abstract/snippet level
only, not full text — flagged explicitly as needing a `paper-review` pass before it carries
thesis weight.

**Haemodynamic proxy chosen**: low/oscillatory wall shear stress (WSS) is the mechanism the
serial-progression literature (PREDICTION, Samady 2011) points to for plaque onset in
previously plaque-free segments — not high WSS/plaque stress, which only matters once a
lesion already exists. The strongest human geometry-to-WSS evidence (39 ASOCA CFD trees) found
**diameter was the only geometry variable to survive multiple-comparison correction**
(r=−0.85, adjusted p=0.0046); curvature/torsion correlations (~0.5-0.65) did not survive
correction, and the curvature-to-low-WSS correlation was even *negative* for the marginal
branch (r=−0.60), "consistent with curvature driving helical flow that raises WSS" rather
than lowering it. This is presented as a caution against assuming curvature straightforwardly
predicts low-WSS regions.

**Descriptor set recommended, with ImageCAS-X stability results (100 training scans)**:

- Fixed-tangent bifurcation angle (`fitcore3`, §1.11): stable (78.0-80.8° across smoothing);
  medians LM 80.8°, LAD-D1 61.4°, LCx-OM1 67.1°, crux 64.4°. ICC ≥0.97 under realistic (0.1mm)
  jitter; degrades to 0.58-0.92 under the harsher 0.25mm stress test, LM most robust.
- LM Finet ratio: 0.63 (EDT radius), method ICC 0.85, window ICC 0.90.
- Local chord curvature at 5 mm (κ_l5) in each proximal window: carries over from
  whole-vessel behaviour (ICC 0.97-0.99 realistic, 0.70-0.91 under stress).
- Local expansion ratio `E = r / median(r over ±5mm) − 1` (flags ectatic, low-WSS segments):
  proposed, untested, "at the noise edge."
- Curvature ratio `δ = κ_l5 · r` (Dean-number proxy): proposed but flagged as "borderline
  pointwise" and, per the priorities report, effectively **unmeasured** (no traceable
  computation, even in scratch).
- Tree-propagated shear proxy `τ̂ = 4μQ/(πr³)` from an allometric flow-split model
  (`Q = 1.43 d^2.55`, split by `(d_sb/d_mb)^2.27`): exploratory only; carries ~3x the relative
  radius error (~50% at r=1.5mm) and is unvalidated against CFD.
- **Dropped**: torsion, Murray exponent, pointwise taper, cross-section eccentricity, Frenet
  finite-difference curvature, myocardial bridging (undetectable from centerline geometry
  alone; full-text evidence in fact shows the bridge segment itself is *spared* of plaque, and
  one study found *less* proximal/mid LAD atherosclerosis in bridge patients), parent-relative
  deflection angles.

**Elastic (SRVF) registration** is proposed as the mechanism to solve cross-patient anatomical
correspondence (Bjørn's stated concern), registering each named vessel to a per-segment Karcher
template via the square-root velocity function `q = β′/√|β′|`. Explicitly labelled as
**feasibility-only, not yet validated**: on a 30-curve prototype, nearest-neighbour
vessel-type separation improved only marginally over simple rotation-only alignment (0.93 vs
0.90), and the one vascular precedent found (65 carotids, AneuRisk65) showed only a weak,
non-significant group shape difference (permutation p=0.079).

**If one primary regional descriptor must be named**: the report picks the **LM
daughter-to-daughter bifurcation angle**, on grounds of highest stability under stress and
because it targets the LM/proximal-LAD/proximal-LCx region where first plaque concentrates —
not κ_a or any whole-vessel tortuosity measure.

---

## 6. Protocol readiness and CT-FFR

From `Tortuosity protocol readiness and CT FFR.md` (the latest, audit-style report).

### 6.1 Is the protocol ready for a clinical-style study? **No.**

The verdict is explicit: "The methods PDF is a good descriptor definition. It is not yet a
protocol for a serial-CCTA plaque paper." Four blocking problems are named:

1. **No reliability evidence at the protocol's own stated operating point.** Every quoted ICC
   in the draft protocol was actually computed with extra σ=1mm smoothing or on a different
   estimator than the one the protocol adopts ("no extra smoothing"). Reference-vs-CAS-Net
   agreement (the extractor error spectrum) has never been measured at all.
2. **No pre-registered hypothesis.** "Primary in every plaque-relevant region" is described
   as 6-9 untargeted statistical tests with no direction and no multiplicity correction.
3. **A concrete bug**: the regional κ_a code (`tortuosity/research/case_study/regional.py`)
   divides attributed turning by the *full* region length even though the first ~2.5 mm of a
   region (half a chord) never receives any attributed turning angle. This biases regional κ_a
   downward by about 2.5/|region length| — roughly 14% at the 18mm median LAD-D1 distance and
   25% at a 10mm floor — and reintroduces exactly the length-dependence κ_a was chosen to
   avoid. Fix identified: start every proximal window at 5mm (as the RCA window already does)
   or divide by `5mm × number of attributed vertices` instead of the raw window length.
4. **The protocol cannot reach the two places first plaque concentrates** (LM bifurcation,
   first 5mm of LAD/LCx) because κ_a is undefined there, and it has no stated plan for heart
   size, cardiac phase, measurement error correction, or statistical power.

Estimated fix time: "about two weeks on ImageCAS-X alone." The outcome analysis itself needs
CGPS data "that nobody on the project has seen yet."

Two further overstatement corrections flagged in this audit: the earlier "added information"
table credited `f_twist` with 94-99% of unexplained rank variance, but whole-vessel `f_twist`
has ICC only 0.15-0.32 under realistic (0.5mm correlated) jitter, so "most of that 'new
information' is noise" — the adoption rule should be *reliable* variance unexplained, not raw
variance. And a "not affected by dominance (all p≥0.2)" claim rests on only 32 left-dominant
and 15 co-dominant scans, which "cannot show absence of an effect" and should be reported as
an estimate with a confidence interval, not a null claim.

### 6.2 Twelve-item ranked punch list before freezing (verbatim structure from the report)

1. Fix the regional denominator bug (item 3 above).
2. Pick one smoothing operating point, rerun the full reliability battery there, write
   pass/fail gates into the protocol document.
3. One pre-registered primary estimand, two-sided, with a multiplicity rule and a smallest
   effect of interest.
4. Reference-vs-CAS-Net centerline agreement on the 160 test scans (ICC, Bland-Altman, wCV) —
   also gives the reliability coefficient λ needed for regression-dilution correction.
5. One proximal window scheme, chosen on reliability, mapped explicitly to SCCT segments.
6. Bifurcation family (LM/LAD-D1 daughter angle, LM Finet ratio) declared as co-primary or
   secondary, explicitly, not left ambiguous.
7. Heart-size and cardiac-phase handling as covariates (LV mass or a tree-size proxy;
   reconstructed phase and heart rate), not as ratios.
8. Rules for the ostium, ramus intermedius, missing landmarks, and the length floor.
9. Demote `f_twist` to exploratory; correct the "added information" table to reliable
   variance; report the dominance effect as an estimate with a CI, not a null.
10. Two declared reference groups (all baseline participants; a prescriptive plaque-free/
    risk-factor-free "healthy standard") with GAMLSS/LMS centile fitting — never a "healthy at
    both scans" group, which is explicitly called circular/selection-biased for this purpose.
11. A blinding record (the Disease column was in fact opened in an earlier session — recorded
    here as a documented lapse, not hidden) and a dated public pre-registration.
12. CGPS labeller validation, inter-phase reproducibility, plaque-distortion check, and κ·r
    sensitivity — deferred, needs CGPS data.

### 6.3 CT-FFR link: **No as a primary; conditional yes as a covariate.**

"CT-FFR is a stenosis index. In a plaque-free tree it reduces to a smooth decline governed by
length, radius and flow allocation, and every prognostic result for it comes from existing
lesions." Evidence for this: in normal (stenosis-free) vessels, CT-FFR falls smoothly from
~0.96-0.99 at the ostium to ~0.86-0.90 distally purely as a function of geometry; in 59
stenosis-free marathon runners the distal LAD read 0.81±0.10 with 32% at or below the clinical
0.80 "abnormal" threshold, despite no disease — i.e. CT-FFR in a healthy population is mostly
noise/geometry, not pathology. Idealized simulations show tortuosity alone (without a
stenosis) adds only 115-285 Pa (~1-2 mmHg) of extra pressure drop over several bends, and a
1D/reduced-order CT-FFR model "sees tortuosity mostly through path length" — i.e. a CT-FFR
association with tortuosity would largely just restate the length effect that κ_a was chosen
specifically to remove. The prognostic CT-FFR literature (EMERALD, EMERALD II, FAME II) all
concerns which *existing* lesion becomes a culprit within 1-3 years; none of it transfers to a
plaque-free baseline, and no study computing CT-derived haemodynamics at a plaque-free
baseline and following it >5 years for new plaque was found.

**What is recommended instead**: a minimal reduced-order haemodynamic model, not CT-FFR by
name — a steady 0D Poiseuille network per lumen tree (per-segment resistance
`8μL/(πr⁴)`, allometric inlet flow, diameter-ratio flow split at bifurcations), giving a
per-segment pressure drop, a "pseudo-FFR", and a tree-propagated WSS index
`4μQ/(πr³)` normalised to the root value, validated against steady 3D CFD on 20-40 trees.
Explicitly: "Enter the result as a pre-declared adjustment and secondary exposure, never as a
primary endpoint or as 'CT-FFR.'" Radius enters the resistance formula to the fourth power, so
"a 10% radius error gives about 40% error in segment pressure drop" — this haemodynamic layer
inherits the same reference-vs-CAS-Net radius-accuracy dependency as the tortuosity work, and
"must not delay the tortuosity freeze."

### 6.4 Power / effect size reality check

Table reproduced from the report (minimum detectable OR per SD of the descriptor, two-sided
α=0.05, 80% power, Hsieh's formula), by number of analysable plaque-free returners, baseline
plaque-free prevalence `p`, and measurement reliability `λ`:

| Analysed plaque-free returners | p=0.3, λ=1.0 | p=0.3, λ=0.7 | p=0.5, λ=1.0 | p=0.5, λ=0.7 |
|---|---|---|---|---|
| 300 | 1.45 | 1.56 | 1.41 | 1.50 |
| 500 | 1.33 | 1.41 | 1.30 | 1.37 |
| 1,000 | 1.23 | 1.28 | 1.21 | 1.25 |
| 2,000 | 1.15 | 1.19 | 1.14 | 1.17 |

The largest continuous angiographic tortuosity study found per-SD odds ratios of only
1.05-1.09 for CAD — "out of reach for any plausible rescan subset." The protocol should
therefore pre-declare a smallest effect of interest around **OR 1.3 per SD** and report
whatever minimum detectable effect the achieved sample size actually allows; a null result
then reads as "effects larger than X excluded," which is stated to be publishable, versus an
uninterpretable null without a stated detection floor.

---

## 7. Known open questions (near-verbatim from `Investigation priorities across reports.md`)

The priorities report gives an explicit, ranked ten-item list. Reproduced here close to
verbatim because the plan must acknowledge these, not silently resolve them:

1. **[Reproducibility]** Copy the `/tmp` scratch code behind every reported ImageCAS-X number
   into `tortuosity/`, commit it, and fix the import blockers (`label_map.json`,
   `IMAGECASX_OUT`, staged `topology/`). Called "the only irrecoverable loss" — the scratch
   scripts live in two session scratchpads on a login node whose `/tmp` purge policy is
   undocumented, and as of the audit date the committed code (`topology/tortuosity.py`) still
   implements the rejected Frenet finite-difference curvature, while the untracked
   `tortuosity/merged.py` at the time of that audit had no pre-smoothing and used ℓ=4mm
   (contrast: the committed `tortuosity/merged.py` reviewed in this consolidation, §9, has no
   pre-smoothing step and defaults to `L_REF=4` in its test harness — i.e. this specific gap
   may still be open).
2. **[Plan, Supervisors]** Press supervisors for Herlev-Østerbro (CGPS) access and answers on
   the serial-rescan subset, short-interval repeats, plaque-reading protocol, and branch
   naming — flagged as at least two weeks behind the project plan's own schedule.
3. **[Plan]** Rebuild the CAS-Net inference path (torch, weights, volumes were reported
   absent at audit time), predict the 160 test scans, and write a centerline extractor that
   emits labelled VTK trees from predictions — this repo currently only skeletonises for
   metrics; it does not produce a labelled tree.
4. **[Reproducibility, Plan]** Consolidate one small descriptor module under a **dated**
   pre-registration: κ_a at 5mm, fixed-tangent bifurcation angles, LM Finet, daughter ratio,
   dominance, branch counts.
5. **[Plan, Literature]** Measure reference-vs-CAS-Net-derived feature agreement (ICC,
   Bland-Altman) on the 160 test scans, and use it to fix σ, ℓ and the length floor. **Named
   as the one experiment every single report converges on and none has run.**
6. **[Plan, Supervisors]** Build a tree labeller or label-free fallback for unnamed CAS-Net and
   CGPS trees, and reuse it for repeat-scan correspondence.
7. **[Supervisors, Plan]** Compute per-vessel population distributions on ImageCAS-X with
   size, dominance and Image Quality confounds, plus a first outlier/extreme-value method
   (objective 9, currently addressed by **no** report).
8. **[Supervisors, Plan]** Run a PCA baseline on arc-length-resampled labelled segments and
   test the (Kit's) prediction that it separates on size, dominance and branch count.
9. **[Plan, Reproducibility]** Design the outcome analysis before any outcome is seen: one
   primary descriptor, a power table over effect size and reliability, then lock and open
   Disease.
10. **[Literature]** Defer SRVF templates, κ·r, persistent homology and the turn layer;
    spend literature time only on full reads of sources that will carry thesis claims.

**Five specific unresolved disagreements the reports flag as needing a single, written
decision** (verbatim structure):

- **The single primary descriptor is unresolved across reports**: the "Choosing" report names
  arc/chord TI plus κ_a as a pair; the "Vessel specific" report names κ_a alone (after finding
  TI rank-correlated 0.70-0.83 with vessel length); the "Plaque prone regional" report names
  the LM daughter angle as primary for the plaque-onset question specifically. The priorities
  report's own recommendation: pre-register **one per outcome** — κ_a for whole-vessel
  extremes (objective 9), the LM angle for new plaque (objective 10) — with a stated
  multiplicity correction, not a single universal "the" primary.
- **The length floor differs across reports** (roughly 15, 20, and 25mm across three reports,
  vs. 2-17mm windows in the regional report) — unresolved; should be set from an
  ICC-vs-remaining-length curve, not any of the currently-used round numbers.
- **Radius weighting was dropped twice** (following Hart 1999's finding that diameter-weighted
  tortuosity measures perform *worse* than unweighted ones) **and then revived** as `κ·r` in
  the regional report **without addressing that prior objection** — an internal
  inconsistency the priorities report flags explicitly, not resolves.
- **Effect-size assumptions for power differ by a factor of 3-5 in log-odds** across reports
  (OR 1.05-1.09 per SD in the Choosing report's angiography citation vs. OR 1.3 assumed in the
  regional report's power table, which is what yields "about 345 patients"). Recommended fix:
  report a sensitivity table over OR ∈ {1.05, 1.1, 1.3} and reliability λ ∈ {0.5, 0.7, 0.9},
  which "also defines when a null result is informative" — not yet done.
- **The vessel-specific report is internally inconsistent**: its headline claims κ_a "keeps
  its ranking across the whole grid" of smoothing/chord settings, but its own detailed notes
  record a minimum Spearman rank stability of **0.86 on the LCx** in one sample (P100), below
  its own pre-declared 0.90 bar. Flagged as needing resolution by the item-4 rerun, not yet
  resolved.

**Objective coverage gap, stated explicitly**: "no report addresses objective 9 (outlier and
extreme-value detection) or the MACE risk model in objective 10," and the reports' own
tortuosity-formula churn (Q co-primary → dropped; arc/chord baseline → Primary 1 → secondary;
κ_a companion → sole primary) is characterised by the priorities report itself as having
"diminishing returns" territory that the thesis should stop investing further method-research
time in, in favour of the upstream (extractor error, branch naming) and downstream (outlier
detection, CGPS outcome) gaps that no report has touched.

**Confirmation-sample warning** (recurring across reports, restated here because it affects
every number above): the P150 (first 150 `train.txt` ids) and P100
(`numpy.random.default_rng(0)` draw of 100 training ids) samples used throughout **overlap**,
so fewer than 460 of the 560 training scans remain genuinely unused for a confirmatory rerun,
and one earlier test-harness run (`run_merged_tests.py`) may have already consumed the full
560-scan training split — the audit "could not rule this out." Any future confirmatory pass
must explicitly list its unused scan set.

---

## 8. Effect of centerline smoothing degree on curvature-based tortuosity metrics

This is addressed directly and repeatedly, with closed-form derivations, and is the most
mathematically developed thread in the whole corpus. **The direction the task worried about
(over-smoothing artificially lowering curvature/tortuosity, under-smoothing amplifying
voxelisation noise) is confirmed explicitly, in both directions, with quantitative bounds.**

### 8.1 Under-smoothing / raw sampling: noise inflates turning

`Vessel specific tortuosity math and tests.md` measures that on the delivered (already
dataset-smoothed, σ=0.5mm/5-vertex) ImageCAS-X centerlines, **raw per-point turning angle is
about 3-4x the real curvature**: median raw step angle ~5.8-5.9° at ~0.45mm point spacing,
while smoothed curvature at a 5mm chord implies a much smaller true turning rate. Two
independent estimates of the residual noise disagree by more than an order of magnitude
(implied iid jitter of 0.016-0.02mm from the raw-angle statistic vs. 0.054-0.062mm from a
point-to-smoothed-curve distance), which the report resolves by concluding **most of the
apparent noise is spatially correlated error (from segmentation/skeletonisation), not
independent (white) jitter** — and correlated error is the harder problem because "at these
scales it looks like signal." A diagnostic is proposed but not yet run on real data: under
white jitter the variance of the perpendicular second difference is flat across lags 1-4; a
rise before the expected signal regime indicates correlated error.

**Closed-form noise laws** (independent/iid jitter of amplitude `σ_n`, chord `ℓ`):

```
turning angle at chord ℓ  ~ Rayleigh(scale = √6 · σ_n / ℓ)
κ_a noise floor            = √(3π) · σ_n / ℓ²
κ_r² additive bias         = 12 σ_n² / ℓ⁴           (second moment inflates faster than first)
spurious κ_a density       ≈ 3σ_n / ℓ²               (order-of-magnitude form used elsewhere)
```

Both matched Monte Carlo to the fourth decimal. At `σ_n=0.25mm`, spurious `κ_a` density is
about **0.19 rad/mm at ℓ=2mm** falling to about **0.03 rad/mm at ℓ=5mm**, against a real
coronary curvature signal near 0.08 mm⁻¹ (van Zandwijk 2019's 5mm-scale value) — i.e. at a 2mm
chord the noise floor is comparable to or larger than the signal, while at 5mm it is roughly
40% of it. **Torsion is one derivative order worse**: its standard deviation scales as
`σ_n / (κℓ³)`, and Bullitt's SOAM torsion term reads a near-constant ~2.3 rad/vertex on a
perfectly straight noisy line regardless of true noise level — the formal justification for
dropping every torsion-based descriptor.

### 8.2 Over-smoothing: length and curvature are directly deflated

Multiple independent bias terms are derived, all pointing the same direction (more smoothing
= lower apparent tortuosity):

- **Gaussian smoothing of width `w` (equivalently σ) deflates arc length** by approximately
  `(w²/2)·κ_r²` (a bias on `L`, hence on both TI and any curvature integral).
- Directly measured: Gaussian smoothing at **σ=1mm shortens arc length by a median 2.1%**, and
  at **σ=2mm by 4.2%**; L/D (arc/chord) is therefore "biased low and scale-dependent, and the
  same sigma must be used in every analysis" (`Choosing a coronary tortuosity descriptor.md`).
- **Chord discretisation** (using a polyline chord `ℓ` instead of true arc length) *also*
  deflates the measured curvature/length by approximately `κ_r²ℓ²/24` — a separate,
  smaller-order bias in the opposite mechanism from the noise-inflation above, meaning the net
  bias direction at any given `(σ, ℓ)` is a genuine trade-off, not a monotone function of
  smoothing alone.
- **Aliasing at fixed chord**: `κ_a` at `ℓ=5mm` falls by **98% on a 10mm-wavelength sinusoid**
  (because the chord lands on nearly the same phase every step) and by ~20% at 15mm
  wavelength — i.e. over-smoothing (or an over-long chord) can make a genuinely tortuous
  signal read as almost perfectly straight, a much larger effect than the length-shrinkage
  bias above.
- **"Maximise ICC" is explicitly identified as a degenerate, dangerous selection rule**:
  reliability (ICC) rises **monotonically** with both smoothing σ and chord ℓ under every
  jitter model tested, so a rule that simply picks the operating point with the highest
  reliability will always select the most aggressive smoothing available, silently trading
  away real signal for apparent stability. Quantified: at σ=2mm instead of 1mm, TI on
  8-20mm-wavelength sinusoid phantoms **loses 28-66% of its value**. The reports' explicit
  countermeasure, adopted as a design rule: **any ICC-maximising selection must be paired with
  a pre-declared bias tolerance on synthetic phantoms** (e.g. `|bias| ≤ 10%` on a fixed
  wavelength/bend-radius phantom set), which in practice caps σ at about 1mm for ℓ=3-5mm.
- The Bishop-spectrum (BCS) analysis derives a closed-form bracket for its own smoothing width
  `σ0`: "at least 1.16mm keeps iid bias under 5% of signal at the measured 0.06mm noise, and at
  most 1.27mm keeps 70% of a 90° bend of 3mm radius" — an explicit statement that the
  noise-suppression floor and the resolution ceiling are only about 0.1mm apart at the
  measured noise level, i.e. very little slack exists between under- and over-smoothing on
  these particular centerlines.
- Under the harsher, more realistic 0.5mm-correlated-over-1mm jitter stress test, **no**
  smoothing width can satisfy both constraints for the BCS shape fractions simultaneously:
  keeping bias under 20% of signal needs `σ0 ≈ 3mm`, which retains only 13% of a 3mm-radius
  bend's true signal — an explicit, quantified statement that over-smoothing and
  under-resolution genuinely trade off with no safe middle ground at that noise level.

### 8.3 The scale band the reports converge on

Four independent scale-selection arguments (a noise floor below 10% of signal, cancellation of
the two opposing length biases, an MSE-optimal smoothing width, and resolution of the tightest
physiologically plausible coronary bend, R≈3mm/90°) are stated to "all land between about 2
and 5mm" for the chord `ℓ`. This is the basis for the field's working default: **ℓ=5mm
(fallback 8mm), σ=1mm extra smoothing on top of the dataset's own σ=0.5mm** — while noting one
report (`Centerline tortuosity normal ranges.md`) argues no extra smoothing is needed at all
(σ=0) since the delivered centerlines are already smoothed, and this specific disagreement
between reports on the operating σ is one of the items the readiness audit
(`Tortuosity protocol readiness and CT FFR.md`) flags as unresolved and blocking a freeze
(§6.1, item 2 above).

### 8.4 Explicit statement that resolution, not smoothing, may be the deeper limit

`Kjeldsberg 2021` (carotid siphon, cited across reports) found bend counts ranged from 3 to 33
depending on **centerline resampling resolution alone**, while smoothing strength moved the
count only between 6 and 7 — a carotid, not coronary, result, but cited repeatedly as evidence
that resampling density, not smoothing per se, is often the dominant lever for turn-based
(not curvature-magnitude) descriptors specifically.

**Everything in this section is flagged with the same caveat the reports themselves state
repeatedly: no coronary CTA study anywhere reports an ICC, CV, or Bland-Altman figure for any
tortuosity or curvature metric under any smoothing regime.** All quantitative noise/bias
figures above come from (a) closed-form derivations verified by Monte Carlo on synthetic
curves, and (b) measurements on the reference ImageCAS-X centerlines under *synthetic*
jitter, never from a real independent segmentation-to-segmentation or extractor-to-extractor
comparison. That comparison (reference vs. CAS-Net-predicted centerlines) is item 5 of the
open-questions list in §7 and has never been run.

---

## 9. Implemented in code today vs. proposed only on paper

Checked directly against `tortuosity/merged.py`, `tortuosity/vessels.py`,
`tortuosity/run_merged_tests.py` (the only committed, non-scratch tortuosity code in the
repo, per `tortuosity/CLAUDE.md`'s scope statement that `topology/tortuosity.py` is
explicitly *not* to be edited or built on, since it implements the rejected Frenet
finite-difference curvature).

**Implemented and committed:**

- `chord_resample(P, ℓ)`: exact-chord-length resampling of a polyline by linear interpolation
  between the two bracketing points (quadratic solve for the interpolation parameter) — this
  is the substrate every curvature/turning metric in the reports depends on.
- `scc_density(P, ℓ)` = `Σθ_j / (π·ℓ·(n−1))`: this is the SCC / κ_a family up to the constant
  `π`, i.e. `κ_a = π × scc_density`. **Note the code's normalisation differs by a factor of π
  from the reports' `κ_a = Σθ_j/L` formula** (§1.2) — `scc_density` divides by `π·ℓ·(n-1) =
  π·L`, matching Mateos's original `a_n = θ_n/π` convention rather than the plain radians/mm
  convention the later reports settle on and quote all their numeric results in. Anyone
  reusing this function for a thesis number needs to multiply by π or otherwise reconcile
  the convention.
- `grisan3d(P, ℓ, kappa_floor)`: implements Grisan's eq. 19 aggregation with the
  **binormal-flip** twist detector (§1.4) — i.e. the version `Alternative tortuosity merges
  for coronaries.md` explicitly superseded in favour of a parallel-transport curvature-vector
  detector. The PT-angle detector is **not implemented in committed code**; it exists only
  as a design/derivation in the reports.
- `arc_chord(P)` = `L/D − 1`: the plain 3D TI, no vessel-specific projection variant, no
  smoothing built in (smoothing is expected to be applied to `P` before calling this).
- `vessels.py`: loads named-vessel polylines (LAD/LCx/RCA) from the VTK centerlines by
  longest-geodesic-path through same-labelled points — matches the "longest geodesic path"
  vessel definition used in most reports, but the reports also note a **second, inconsistent
  definition exists** (`topology.graph.Vessel`, which chains same-named segments and can end
  at a different point), and flag that P150/P100 samples computed under one definition are
  "not strictly comparable" to anything computed under the other — this ambiguity is
  unresolved in code.
- `run_merged_tests.py`: a synthetic/cohort/floor-effect test harness with **pre-declared
  thresholds already committed in code** (`MIN_RHO_STABLE=0.8`, `MIN_ICC=0.75`,
  `MAX_FLOOR=0.2`, `MAX_ABS_LENGTH_RHO=0.5`, `MIN_LENGTH_MM=15`, chord sweep `LS=[2,3,4,5,6,8]`,
  reference chord `L_REF=4`) — this is the one place in the repo where a pre-registration
  requirement from `tortuosity/CLAUDE.md` has actually been executed as code, though note
  `L_REF=4mm` here does not match the 5mm default the later reports settle on.

**Proposed only in reports/research_notes, not in `tortuosity/`'s committed code** (confirmed
by `find tortuosity/ -type f`, cross-checked against `Investigation priorities across
reports.md`'s own audit):

- `κ_r`, `Q = (κ_r/κ_a)²` — not implemented (and per §2, later dropped anyway).
- Bishop Curvature Spectrum (`ψ`, `kB`, `f_wiggle`, `f_twist`) — exists as
  `tortuosity/research/unified/bishop.py`, `synthetic.py`, `cohort.py`, `analyze.py`. This
  *is* committed to the repo (under `tortuosity/research/`, distinct from the `tortuosity/`
  package root), but `tortuosity/research/CLAUDE.md` and the reports both treat this as
  research/exploration code, not the frozen descriptor module.
- Regional/bifurcation descriptors (fixed-tangent angle, Finet ratio, daughter ratio, δ=κ·r,
  τ̂ shear proxy) — exist as `tortuosity/research/case_study/regional.py` and
  `regional_analysis.py` (committed, but per §6.1 item 3, `regional.py` contains the confirmed
  denominator bug and is explicitly not the frozen version).
- Simple-measures pipeline (DM, DM2, κ_a, bend counts) behind the normal-ranges report's
  numbers — exists as `tortuosity/research/simple/compute_simple.py`,
  `sensitivity_bends.py`, `summarize_simple.py` (committed).
- The case-study visualisation and "easy"/"advanced" metrics scripts — exist as
  `tortuosity/research/case_study/easy.py`, `advanced.py`, `visualise.py` (committed).
- SRVF elastic registration, Karcher templates, tree-propagated shear network solve, the PT
  turn-layer detector, and Bullitt SOAM/ICM — **confirmed not present anywhere in the
  committed tree**; these exist only as formulas/derivations in the reports and, per the
  reports' own citations, in ungrouped `/tmp` session scratchpads whose persistence is
  explicitly flagged as at risk (§7, item 1).

**Overall status**: a meaningful amount of the exploratory/research code referenced by the
reports *has* been committed under `tortuosity/research/`, contrary to the impression in the
oldest priorities-report audit that everything lived only in `/tmp`. What remains genuinely
uncommitted or unreconciled is (a) the frozen, single, pre-registered descriptor module the
`tortuosity/CLAUDE.md` protocol calls for (none of the several partially-overlapping,
differently-parameterised research scripts has been promoted to that status), (b) the
regional denominator bug fix, (c) the PT-based turn-layer detector, and (d) SRVF/shear-network
components that never left the derivation stage.
