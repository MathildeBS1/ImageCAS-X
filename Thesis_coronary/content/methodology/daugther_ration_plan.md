# Daughter ratio: definition, code, and Methods 05c

## Context

`05c_daughter_ratio.tex` is notes only and `CGPS_data/thesis_final/` has no ratio code. The planned
features were the LM→LAD and LM→LCx diameter ratios. Evaluation:

- Both planned ratios divide by the left main diameter, the least reliable of the three (LM length
  10.5 ± 5.3 mm in Medrano-Gracia 2016, so the stretch clear of the ostium and of the widened
  confluence is short or absent). Its error enters both features and correlates them, and both go
  missing together.
- The review supports the width difference between the LAD and the LCx (Garcha 2025) and discusses
  Finet's ratio (Zhang 2024, null). Neither study used LM→daughter ratios.

Decided with the user (2026-11-11):

1. Two features, still 2 parameters: **daughter asymmetry** `ln(D_LCx / D_LAD)` (no LM diameter
   needed, available whenever the angle is) and **Finet's ratio** `D_LM / (D_LAD + D_LCx)` (carries
   the LM uncertainty alone).
2. Angle and ratios keep **their own linear terms** in the tested block (5 parameters). **Angle ×
   asymmetry** is one prespecified secondary term, estimated, outside the LR test. Reason: one
   simulation study on synthetic trees, and a product needs its main effects.

## 1. Code: `CGPS_data/thesis_final/daughter_ratio.py` (new)

Mirror `bifurcation_angle.py` (docstring, constants, pure functions, `tree_*` wrapper, `--check`).

- `DEPTHS = (5.0, 10.0)` mm from the bifurcation point O, the interval of `bifurcation_angle.DEPTHS`,
  so angle and diameters describe the same stretch, beyond the confluence.
- `contour_diameter(ring)`: area-equivalent diameter `2 sqrt(A / pi)`, A the area of the lumen
  contour polygon in 3D (half the norm of the summed cross products about the centroid). Same
  definition as Medrano-Gracia 2016 ("effective radius", A = πR²).
- `reference_diameter(s, D, lo, hi)`: median of D over the centerline points with arc length in
  [lo, hi]; nan when the vessel does not reach `hi` (daughters) or has fewer than 2 points there.
  Median, so one cross-section widened by a side-branch origin does not move it.
- LM: same 5 to 10 mm, measured upstream from O; nan when the LM is shorter than 10 mm.
  (Setting to revisit outcome-blind once the tracer LM lengths are known; report coverage.)
- `lm_ratios(lad, cx, lm)` → `{"asymmetry": ln(D_cx / D_lad), "finet": D_lm / (D_lad + D_cx)}`;
  asymmetry is returned even when the LM is nan.
- `tree_ratios(tree)`: LAD and LCx from `split_trunks.split(*graph(tree))` (arc length 0 at O, as in
  `tree_angle`); LM points = the shared start of `split_trunks.trunk_path(X, lab, G, "LAD")` and
  `"CX"`, reversed so arc length runs upstream from O. Contours per point: the tracer file format is
  unknown (`split_check.tracer_tree` raises `NotImplementedError` for the same reason), so the
  contour loader does the same with a clear message; all functions above take arrays and are
  testable now.
- `check()`: circular and elliptical rings (known area), rigid motion, tubes with known diameters
  → exact asymmetry and Finet (0.678 for the Finet mean values 3.39 / (2.708 + 2.236)), one widened
  cross-section in the window leaves the median unchanged, short LM → Finet nan but asymmetry kept,
  short daughter → both nan, uneven point spacing.
- `README.md` in `thesis_final/`: add the entry, in the form of the other two.

## 2. Figure: `Thesis_coronary/content/methodology/figures/daughter_ratio_figure.py` (new)

One figure, made-up bifurcation run through the real code (pattern of `curvature_figure.py`), PDF + PNG.
Panel A: LM, LAD and LCx with O, the 5 to 10 mm stretch shaded on each vessel, and one lumen contour
with its equal-area circle and `D = 2 sqrt(A/π)`. Panel B: the three diameters drawn as bars or
circles to scale with the two formulas and their numbers. Label `fig:method-ratio`.

## 3. Text: `Thesis_coronary/content/methodology/05c_daughter_ratio.tex`

Read `Thesis_coronary/CLAUDE.md` (done) and load the `thesis-style` skill first. Length and detail
as the main part of 05a (about 350 words, two equations, the figure), prose only, no lists, no
"trunk", British spelling, reason before method, no sentence opening with "Because". Heading
"Diameter Ratios", label `sec:method-ratio` kept. Order, each sentence handing over to the next:

1. Opener: how the diameter divides at the left main bifurcation was described by two ratios
   (figure). No rationale (owned by `sec:method-features` and `sec:lit-wss`).
2. First, the diameter of a cross-section: area-equivalent diameter from the tracer's lumen contour
   (`eq:method-diameter`), following Medrano-Gracia et al. (already cited in 05b).
3. Subsequently, one diameter per vessel: the median over 5 to 10 mm from the bifurcation point O
   of `sec:method-angle`, with its reason (clear of the widened confluence; same stretch as the
   angle) and its cost (short left main → no value).
4. Finally, the two features: asymmetry (`eq:method-asymmetry`), 0 for equal daughters, sign reading;
   Finet's ratio (`eq:method-finet`, \cite{finet2008fractal}), 0.678 as the value Finet reported,
   lower = daughters wide for their parent. One sentence on why the left main enters one feature only.
5. Missing rule; pointer to `sec:method-models` for the secondary angle × asymmetry term (one clause).

Not in the text: Murray 3, 2.39, 7/3 (no longer needed; note in the header that the fact-ownership
line in the map lapses), the rejected LM→daughter ratios (counterfactual rule; kept in the header
comments with the reasons above), implementation detail (cross products, interpolation).
Header comments: date, decision, sources, and CHECKs: Garcha full text not read this session (Nature
redirect; abstract: "diameter ratio between left coronary branches ... can amplify the effect of
... bifurcation angle"), so its exact ratio definition and direction are unverified; tracer contour
format; LM window; `progression_who_pooled.py` has no ratios yet, so model and text disagree until it
calls `tree_ratios`.

## 4. Keep the rest in line (small edits)

- `05_features.tex`: sentence 4 and the table row → "daughter asymmetry and Finet's ratio"; header note.
- `03_prediction_model.tex` and `04_model_size.tex` (notes only): five features renamed; angle ×
  asymmetry as prespecified secondary term outside the LR test; Finet's ratio no longer "set aside".
- `05b_bifurcation_angle.tex`: nothing in the prose; header note that 05c reuses O and the depths.
- Root `CLAUDE.md` (objective paragraph and Geometry line) and memory `segment-cloglog-who-model`:
  new feature names and the secondary term. Tell the user that
  `~/Desktop/Speciale/CGPS_statistics-/CLAUDE.md` (authoritative plan) needs the same change; edit it
  only if they say so.
- `Thesis_coronary/CLAUDE.md` (content map): only when committed, per the project rule.

## Verification

- `python CGPS_data/thesis_final/daughter_ratio.py --check` passes; `bifurcation_angle.py --check`
  still passes.
- `python Thesis_coronary/content/methodology/figures/daughter_ratio_figure.py` writes the PDF/PNG;
  view the PNG.
- `latexmk` on `Thesis_coronary/main.tex`: no undefined references (`sec:method-ratio`,
  `fig:method-ratio`, `finet2008fractal`).
- Reread 05c against the code line by line (windows, median, missing rules, formulas) and grep the
  new text for "trunk", list environments and "Because".
