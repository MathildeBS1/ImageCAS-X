# thesis_final

Code behind the Methods chapter (`Thesis_coronary/content/methodology/`). Each feature module has pure
functions on arrays, a `tree_*` wrapper on one centerline tree (arteries from `../split_trunks.py`) and a
`--check` on synthetic shapes that needs no data.

- `curvature_feature.py`: average curvature per segment, Menger's formula with 5 mm chords
  (`segment_curvature`; sec:method-curvature, `03d_curvature.tex`).
- `bifurcation_angle.py`: left main bifurcation angle between least-squares lines through the points 5 to
  10 mm from the bifurcation point (`tree_angle`; sec:method-angle, `03a_bifurcation_angle.tex`).
- `daughter_ratio.py`: daughter asymmetry ln(D_LCx / D_LAD) (and Finet's ratio, descriptive only), each
  diameter the median area-equivalent diameter read every 0.5 mm over 5 to 10 mm from the bifurcation
  point (`tree_ratios`; sec:method-ratio, `03b_daughter_ratio.tex`). `narrower_rows` gives its model
  value: |a| on the narrower daughter's proximal row, 0 on the other. Needs the tracer lumen contours,
  which the delivered tracer files do not hold (`tracer_rings` raises).
- `split_check.py`: checks the proximal / mid / distal split against Medis and the visual reads
  (sec:method-split, `03c_segment_split.tex`).
- `tracer_probe.py`: one-off look at the tracer files (format, arrays, frame, Medis/tracer overlap);
  output in `tracer_probe.md`.
- `lumen_probe.py`: one-off look at the lumen predictions in `/data/kimbr/predictions_CGPS-10Y_folds_01234`
  (surface, npz, pkl, ostia), their frame against the Medis lumen rings, and how many participants have
  Medis lumen contours on the proximal LAD and LCx; output in `lumen_probe.md`.
- `tracer_io.py`: reads the tracer centerlines (`tracer_tree`) in the structure of the Medis trees;
  `--labels` writes `tracer_labels.md`, the table from which the code map `CODES` is filled.
- `medis_compare.py`: tracer against Medis on the features (sec:method-medis-agreement). Since 2026-11-19
  every value is computed on its own tree by the cohort's functions (`tree_features`: the curvature profile of
  `artery_curvature`, `angle_with_reason`, `daughter_ratio.tree_asymmetry` on the tree's own lumen surface), so the tracer values
  are those the plaque-free cohort gets and nothing on the tracer side comes from Medis. A pair is compared
  when both trees give a value; the tracer's missingness where Medis has a value is reported. Curvature is
  compared per artery (LAD with LAD, LCx with LCx, RCA with RCA), averaged over each tree's whole artery. Bias, limits of agreement, ICCs and bootstrap intervals. The same-vessel check (90th
  percentile of the distances between the two shared stretches, 2 mm; near O for the angle and asymmetry) is
  descriptive and a sensitivity row only. Writes `medis_compare.md` (aggregates); per-pair rows and
  Bland-Altman plots stay on the server.
- `dominance_check.py`: known-groups check of the asymmetry (2026-11-20, before the outcome is linked): the
  cohort's tracer a = ln(D_LCx / D_LAD) in the plaque-free baseline, by BL dominance. Expected: higher in left-
  than in right-dominant hearts, co-dominant between, carried by D_LCx. Writes `dominance_check.md` (aggregates).
- `cohort_tables.py`: every number of Results §Study Cohort (`results/01_cohort.tex`, 2026-11-25): the flow
  (plaque-free baseline, FU whole-scan quality flag `ct_cag_uneval`/`ct_cag_incomplete`, BL tracer files), the
  missing values with the plaque share kept / left out, Table 1 by outcome, where plaque developed and the feature
  distributions, with complete cases in both models. Runs the three feature modules on the tree split once per
  participant; feature rows saved in `--rows` for `--from-rows`. Writes `cohort_tables.md` (aggregates).
- `curvature_view.py`: for the artery pairs with the largest curvature difference and the closest agreement,
  the tracer and Medis centerlines of the compared artery drawn over each other (start and end of each) and both
  curvature profiles with their averages; reads `medis_compare_arteries.csv`. `bifurcation_view.py` and
  `asymmetry_view.py` do the same for the angle and the asymmetry.

The model script `../progression_who_pooled.py` imports the three feature modules. Removed 2026-11-18
(in git history): `turning_feature.py` (curvature before 2026-11-10) and `taper_feature.py` (taper
dropped 2026-11-16).
