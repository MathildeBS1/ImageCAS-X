# thesis_final

Code behind the Methods chapter (`Thesis_coronary/content/methodology/`). Each feature module has pure
functions on arrays, a `tree_*` wrapper on one centerline tree (arteries from `../split_trunks.py`) and a
`--check` on synthetic shapes that needs no data.

- `curvature_feature.py`: average curvature per segment, Menger's formula with 5 mm chords
  (`segment_curvature`; sec:method-curvature, `03a_curvature.tex`).
- `bifurcation_angle.py`: left main bifurcation angle between least-squares lines through the points 5 to
  10 mm from the bifurcation point (`tree_angle`; sec:method-angle, `03b_bifurcation_angle.tex`).
- `daughter_ratio.py`: daughter asymmetry ln(D_LCx / D_LAD) (and Finet's ratio, descriptive only), each
  diameter the median area-equivalent diameter read every 0.5 mm over 5 to 10 mm from the bifurcation
  point (`tree_ratios`; sec:method-ratio, `03c_daughter_ratio.tex`). `narrower_rows` gives its model
  value: |a| on the narrower daughter's proximal row, 0 on the other. Needs the tracer lumen contours,
  which the delivered tracer files do not hold (`tracer_rings` raises).
- `split_check.py`: checks the proximal / mid / distal split against Medis and the visual reads
  (sec:method-split, `02b_segment_split.tex`).
- `tracer_probe.py`: one-off look at the tracer files (format, arrays, frame, Medis/tracer overlap);
  output in `tracer_probe.md`.
- `lumen_probe.py`: one-off look at the lumen predictions in `/data/kimbr/predictions_CGPS-10Y_folds_01234`
  (surface, npz, pkl, ostia), their frame against the Medis lumen rings, and how many participants have
  Medis lumen contours on the proximal LAD and LCx; output in `lumen_probe.md`.
- `tracer_io.py`: reads the tracer centerlines (`tracer_tree`) in the structure of the Medis trees;
  `--labels` writes `tracer_labels.md`, the table from which the code map `CODES` is filled.
- `medis_compare.py`: tracer against Medis on the features (sec:method-medis-agreement): bias, limits
  of agreement and bootstrap intervals for curvature (per artery, over the shared stretch less 5 mm at
  each end) and the angle. Pairs are left out when the 90th percentile of the distances between the
  two shared stretches (both ways, resampled every 0.25 mm) exceeds 2 mm; angles also need the same check
  within 10 mm of O. The share left out is reported with the limits, and the distance between the two
  bifurcation points O is reported (not a cut).
  The asymmetry: plane cuts of each tree's own lumen surface at 5-10 mm from O on both daughters
  (`daughter_ratio.surface_diameters`), where the Medis lumen covers every cut. Writes `medis_compare.md` (aggregates);
  per-pair rows and Bland-Altman plots stay on the server.

The model script `../progression_who_pooled.py` imports the three feature modules. Removed 2026-11-18
(in git history): `turning_feature.py` (curvature before 2026-11-10) and `taper_feature.py` (taper
dropped 2026-11-16).
