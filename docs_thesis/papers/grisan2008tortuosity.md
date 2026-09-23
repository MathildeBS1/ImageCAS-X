# grisan2008tortuosity — A Novel Method for the Automatic Grading of Retinal Vessel Tortuosity

**Citation:** Grisan, Foracchia, Ruggeri. *IEEE Transactions on Medical Imaging* 2008;27(3):310–319.
doi:10.1109/TMI.2007.904657. Closed access (Unpaywall: no OA copy).
**Read:** 2026-09-22 — full text, all 10 pp., including equations (5)–(22), Figs 2–13, Tables I–II.
Equations and tables read from rendered page images, not from extracted text.
**Source:** IEEE Xplore PDF via DTU licence, saved as
`tortuosity/A_Novel_Method_for_the_Automatic_Grading_of_Retinal_Vessel_Tortuosity.pdf`.
**Verdict:** The origin and exact definition of the turn-based "tortuosity density" τ, validated
against a single retina specialist's ranking of 30 arteries and 30 veins on 2D fundus photographs;
a candidate metric for objective 7 once ported to 3D, but its reported win over plain curvature
integrals is small and untested.

## What they did

**Setting.** 2D fundus photographs, 50° field of view, digitised at 1300×1100 pixels. 60 images from
different eyes of 34 subjects, normal or with hypertensive retinopathy of varying severity. From
these, 30 arteries and 30 veins "of similar length and caliber", chosen as major vessels with
**minimal overlap or entangling** with neighbours. Centerlines were **traced manually** (points
placed by hand), deliberately not by an automatic algorithm. Funded by Nidek Technologies.

**Reference standard.** One retina specialist ordered each set (arteries, veins separately) by
increasing perceived tortuosity. Agreement measured by Spearman ρ against that ordering.

**Properties a measure should satisfy (§II).**
- Invariance to translation and rotation; to scaling only among vessels of similar caliber.
- Composition, eq. (2): a vessel is at least as tortuous as any of its parts. They reject Hart
  1999's rule that a composite lies *between* its parts, with a counterexample (Fig. 2a): three
  non-tortuous pieces joined into an obviously tortuous curve.
- Frequency modulation, eq. (3): more turn curves → higher τ at equal amplitude.
- Amplitude modulation, eq. (4): larger amplitude → higher τ at equal number of turns.

**Definitions (2D).** Curve s(l) = [x(l), y(l)], chord **L_χ** = distance between end points (6),
curve length **L_c** = arc length (7), signed curvature κ(l) (8). Note the notation: **L_c is the
arc, L_χ is the chord.**

**The method (§III-B).**
1. A *turn curve* s_i is a piece on which κ ≥ 0 throughout or κ ≤ 0 throughout, eq. (17). A
   *twist* is a change of curvature sign.
2. Straight (κ = 0) stretches make the split non-unique; each straight stretch is cut in half and
   the halves given to the neighbouring turns (Fig. 3 shows why dropping them is wrong).
3. With n turn curves, eq. (19):

   τ(s) = ((n − 1)/n) · (1/L_c) · Σ_{i=1..n} [ L_c,si / L_χ,si − 1 ]

   i.e. sum over turns of (arc/chord − 1), divided by the **whole vessel's arc length**, times
   (n − 1)/n. Units 1/length: a *density*, so vessels of different length are comparable.
   n = 1 (no twist) gives τ = 0 exactly.
4. **Preprocessing on real vessels (§IV-B).** Manual points interpolated with a cubic smoothing
   spline, regularisation parameter γ = 0.005. Small noise oscillations would create spurious
   turns, so a **hysteretic threshold on curvature** is used: the vessel is not cut at the zero
   crossing but at the midpoint between the two hysteresis-crossing points (Fig. 6).

**Comparators (12 in all).** L_c/L_χ; tc = ∫|κ|, tsc = ∫κ² and their ratios to L_c and to L_χ
(Hart 1999); DCI = (1/L_c)∫(dκ/dl)² (Patasius 2005); MAC, mean direction-angle change (14); TN,
count of angle changes ≥ π/6 (15); ICM, Bullitt's inflection count metric (16); and τ.

**Experiments.**
- Simulated: sinusoids A·sin(f·l), l ∈ [0, 6π], with (a) A = 2 and f ∈ {0, π/12, …, π/2};
  (b) f = π and A ∈ {0, …, 5}; (c) a semicircle of radius 4 cut into 1–6 arcs of alternating sign,
  same |κ| and total length (Fig. 4).
- Manual vessels: Spearman ρ with the specialist's ordering (Table I).
- Robustness: Monte Carlo, 100 repetitions, Gaussian noise added to the manual points with
  Σ = diag(0.5, 0.5) px² (99 % within 2.12 px), re-smoothed, ρ recomputed (Table II, Figs 12–13).

## What they found

**Simulated curves.** Six of twelve measures increase in all three simulated sets: τ, tc, tsc,
tsc/L_c, ICM, DCI. L_c/L_χ − 1 *falls* as turns increase (Fig. 11), MAC falls with amplitude
(Fig. 10), TN is non-monotone in frequency (Fig. 9).

**Table I, Spearman ρ with the specialist (30 arteries / 30 veins, all p < 0.0001):**

| Measure | Arteries | Veins |
|---|---|---|
| **τ** | **0.949** | **0.853** |
| tc/L_χ | 0.939 | 0.842 |
| tsc/L_χ | 0.928 | 0.804 |
| tsc | 0.925 | 0.826 |
| tc | 0.922 | 0.837 |
| MAC | 0.920 | 0.814 |
| tc/L_c | 0.919 | 0.814 |
| tsc/L_c | 0.917 | 0.773 |
| TN | 0.838 | 0.695 |
| L_c/L_χ | 0.792 | 0.656 |
| DCI | 0.787 | 0.589 |
| ICM | 0.684 | 0.575 |

**Table II, median (SD) ρ over 100 noisy repetitions:** τ 0.945 (0.006) arteries, 0.804 (0.044)
veins; tc/L_χ 0.935 (0.008), 0.779 (0.044); L_c/L_χ 0.793 (0.006), 0.659 (0.012); ICM 0.582
(0.083), 0.259 (0.108). τ has the highest median in both sets.

## What the abstract does not tell you

- **The margin is small and untested.** "Best" means 0.949 vs 0.939 (tc/L_χ) in arteries and
  0.853 vs 0.842 in veins, on n = 30 each. No test of the difference between correlated ρ values
  is reported. On these data a plain curvature integral over chord is nearly as good.
- **One rater, ranking only.** A single specialist; no inter- or intra-rater agreement, no absolute
  grades. The reference is one person's ordering.
- **Hand-picked, hand-traced vessels.** Chosen for minimal overlap; centerlines placed manually. The
  noise test adds isotropic jitter to those manual points, not the errors of a real segmentation or
  skeleton (breaks, spurs, wrong branch joins), which §VI concedes are out of scope.
- **The key parameter is not reported.** The hysteresis threshold that decides what counts as a
  turn is given only as dashed lines in Fig. 6 (roughly ±0.01 px⁻¹ by eye, not stated). γ = 0.005
  is given but its convention (it is a smoothing-spline weight) is not defined.
- **Robustness claim slightly overstated.** §V says τ's variance is smaller than all measures but
  L_c/L_χ; in veins τ's SD (0.044) ties tc/L_χ (0.044). Under noise the vein ρ drops
  0.853 → 0.804 for τ and 0.842 → 0.779 for tc/L_χ, so the two degrade by similar amounts.
- **Two conceded blind spots.** (i) A vessel with constant curvature sign scores **0 whatever its
  shape**: a shallow C and a deep U are indistinguishable (§VI: "rarely seen in retinal vessels").
  (ii) τ is a density, so it scales with vessel size; §III-B calls it magnification-invariant in
  physical units, §VI concedes it is scale-dependent between vessels of different size.
- **Retina-specific premise.** The non-tortuous reference is a circular arc, not a straight line,
  because the retina is near-hemispherical. That is what makes the n = 1 → 0 rule sensible there.
- **Amplitude saturates.** In Fig. 10, τ rises from about 0.5 to 0.75 over A = 1–5 and flattens
  above A ≈ 3, so it discriminates poorly between large amplitudes.
- **Printing issues.** Eq. (16) prints ICM as (n_ic + 1)·L_χ/L_c (chord over arc), the inverse of
  the arc/chord that ICM is built on; Fig. 9's caption says "number of twists" for a frequency axis;
  ref [9] (Bullitt 2003) is given as *Med. Image Anal.* but is IEEE TMI 22(9).
- **2D only.** Signed curvature (8) is a planar concept. The paper notes that Bullitt's twist
  (Frenet normal flipping by π) is "equivalent to a change in sign of the curvature for planar
  curves", which is the natural route to 3D, but does not attempt it.

## What it licenses

- `thesis/week3/tortuosity_and_representation.tex:253`: the formula
  τ = ((n−1)/n)(1/L)Σ(L_i/C_i − 1) as written there is **correct** (L = arc, C = chord), and the
  description "cuts at its n−1 inflections into n pieces" matches eqs. (17)–(19).
- "Grisan et al. proposed a turn-based tortuosity density, splitting a vessel where curvature changes
  sign and summing each turn's arc/chord excess, normalised by vessel length."
- "On 30 arteries and 30 veins ranked by one retina specialist, it correlated with the ranking at
  ρ = 0.949 and 0.853, marginally ahead of integrated curvature over chord (0.939, 0.842)."
- "Arc/chord alone ranked poorly (ρ = 0.792, 0.656), and falls as turns are added to a curve of
  fixed length" — support for rejecting L/D as the primary measure (objective 7).
- The four desired properties (rotation/translation invariance, composition, frequency and
  amplitude monotonicity) as a source for selection criterion 1 in `tortuosity/CLAUDE.md`.
- The Monte Carlo design (jitter centerline points, recompute rank agreement) as precedent for
  selection criterion 3.

## What it does NOT license

- **"τ is the best tortuosity measure."** It was best by ~0.01 in ρ, on 60 hand-traced 2D retinal
  vessels, against one rater, with no significance test between measures.
- **Anything about coronary arteries, 3D, or disease.** Retina, 2D photographs, hypertensive
  retinopathy only. No outcome, no plaque.
- **Robustness to segmentation.** Only point jitter on manual tracings was tested.
- **Using τ with its n = 1 → 0 rule unchanged on coronaries.** The zero-for-one-bend rule rests on the
  retina's arc-shaped reference; a coronary segment with one large bend would score 0 (a floor
  effect under selection criterion 5).

## Open questions

- **3D port.** Replace "curvature sign change" with Bullitt's Frenet-normal flip (N_i·N_{i+1} < 0)
  or minima of |κ|; the hysteresis then needs a 3D analogue (e.g. ignore flips where |κ| stays
  below a threshold, or turns shorter than a minimum length). Both thresholds must go through
  selection criteria 2 and 3, since the paper gives no value to transfer.
- **The n = 1 case.** Should a single-bend coronary segment really score 0? Possibly report τ
  alongside a curvature integral (tc/L_χ), which was nearly as good here and has no such floor.
- **Scale.** τ has units 1/mm; coronary vessel length and heart size vary, so criterion 6 (no
  correlation with length) is a real test for it.
- Whether a follow-up paper by the same group (ref [18]-style automatic tracing, or later retinal
  benchmarks such as PubMed 40773512) tested τ on automatic centerlines.
