# thesis_final

Code behind the Methods chapter (`Thesis_coronary/content/methodology/`). Each feature module has pure
functions on arrays, a `tree_*` wrapper on one centerline tree (arteries from `../split_trunks.py`) and a
`--check` on synthetic shapes that needs no data.

- `curvature_feature.py`: average curvature per segment, Menger's formula with 5 mm chords
  (`segment_curvature`; sec:method-curvature, `05a_curvature.tex`).
- `bifurcation_angle.py`: left main bifurcation angle, mean over 5 to 10 mm from the bifurcation point
  (`tree_angle`; sec:method-angle, `05b_bifurcation_angle.tex`).
- `daughter_ratio.py`: daughter asymmetry ln(D_LCx / D_LAD) and Finet's ratio D_LM / (D_LAD + D_LCx), each
  diameter the median area-equivalent diameter over 5 to 10 mm from the bifurcation point (LAD, LCx) or
  over the first 2 mm from the ostium (LM)
  (`tree_ratios`; sec:method-ratio, `05c_daughter_ratio.tex`). Needs the tracer lumen contours, whose file
  format is not known yet (`tracer_rings` raises).
- `split_check.py`: checks the proximal / mid / distal split against Medis and the visual reads
  (sec:method-split, `02b_segment_split.tex`).
- `turning_feature.py`: mean turning per segment, the curvature feature before 2026-11-10; replaced by
  `curvature_feature.py`.
