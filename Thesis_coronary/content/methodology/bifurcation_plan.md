# Bifurcation angle: evaluation, code and text

## Context

`05b_bifurcation_angle.tex` carries a note asking whether the model should use two angles
(left main to side branch, left main to distal main vessel) instead of one, and whether the inflow
angle belongs in it. The current feature is the LAD–LCx angle, taken between lines from the
bifurcation point O to the points at 5–10 mm on each artery and averaged over eleven depths.

Decided with you in this session:

1. **Angles in the model: LAD–LCx only (kept).**
   - Cui et al. 2017 (106 referred patients, 2D reformats, cross-sectional) measured all three
     angles in the same patients: only LAD–LCx was associated with stenosis; LM–LAD and LM–LCx
     were not.
   - Zhang et al. 2024 (53 stenosis-free vs 12 stenosed bifurcations): neither the bifurcation
     angle (p = 0.74) nor the inflow angle (p = 0.058) differed. Gharleghi et al. 2024 (arXiv
     preprint, not to be cited): no angle, including inflow, related to low WSS on its own.
   - So the inflow angle has no support, and all the evidence is small and cross-sectional.
   - Practical: the left main is 10.5 ± 5.3 mm long in the atlas, so LM-based angles cannot use a
     5–10 mm stretch in many people and do not exist without a left main. A second angle would
     also cost one more parameter in a block whose effective sample size is the number of people.
2. **Direction of each artery: a line fitted to its own 5–10 mm stretch (changed).**
   Tested on made-up shapes: with lines from O, a true 75° reads 65° when O sits 1 mm upstream of
   the real split and 54° at 2 mm. The fitted line stays at 75°. Its costs: 4–5 times more
   sensitive to point noise, and early bends enter more (88.6° vs 74.3° on arteries curving apart
   from 60°). It is also the closer reading of the atlas ("linear approximations of the
   centrelines", "average in the 5–10 mm depth interval").

## Changes

### 1. `CGPS_data/thesis_final/bifurcation_angle.py`

- New `artery_direction(Y, s, depths)`: the points at the eleven depths (existing
  `point_at_depth`), a least-squares line through them, unit vector pointing from the 5 mm point
  towards the 10 mm point; `None` when the artery is shorter than 10 mm.
- `lm_angle(lad, cx, depths=DEPTHS, method="fit")`: `"fit"` (default, the thesis feature) returns
  `angle_between` of the two directions; `"origin"` keeps today's mean of the from-O angles, for a
  sensitivity run only. `tree_angle` passes `method` through. Missing rules unchanged (no shared
  first point, or under 10 mm).
- `check()`: existing cases run for both methods (straight arteries at five angles, rigid motion,
  uneven spacing, short artery, no shared start). New: bifurcation point moved 0.5–3 mm upstream
  (fit must stay at 75°, from-O values printed), and both methods printed on the curving arteries.
- Docstring rewritten to the new definition, with the decision above and its sources.
- `CGPS_data/thesis_final/README.md`: the `bifurcation_angle.py` entry updated to match.
- Not touched: `progression_who_pooled.py` still takes the angle from the old Medis function; the
  CAREFUL note in the tex header stays.

### 2. Figure (one, two panels)

New `Thesis_coronary/content/methodology/figures/bifurcation_angle_figure.py`, in the style of
`curvature_figure.py` (same colours, serif, made-up shape run through the real code;
`dataviz` skill loaded first). Writes `bifurcation_angle_figure.{pdf,png}`.

- **A**: a made-up left main dividing into the LAD and LCx, the bifurcation point O, and the
  eleven points at 5–10 mm marked on each artery.
- **B**: the same points with the two fitted lines, their directions and the angle θ between
  them, with its value.

### 3. `Thesis_coronary/content/methodology/05b_bifurcation_angle.tex`

`thesis-style` skill loaded before writing. The Note line is removed. Shape as in 05a: opener
naming the feature and its source with the figure, First / Subsequently steps citing panels A and
B, one equation with a where sentence and one sentence on what the value tells, the cost of the
choice, the missing rule, the figure, then a short subsubsection on the angles not used (as
"Other Measures of Tortuosity" in 05a). About 250 words, shorter than 05a. Draft:

> The feature chosen to quantify how widely the left main divides was the angle between the LAD
> and the LCx, measured in 3D over the depths used by Medrano-Gracia et al. \cite{medranogracia2016atlas}
> (Figure A–B).
>
> First, eleven points were placed on each artery at depths from 5 to 10 mm in steps of 0.5 mm,
> where depth is the distance along the centerline from the bifurcation point O, the first
> centerline point shared by the two arteries (panel A). Starting 5 mm from O keeps the angle
> from depending on exactly where O is placed.
>
> Subsequently, a straight line was fitted to the eleven points of each artery by least squares,
> giving the directions u_LAD and u_LCx away from the bifurcation (panel B). The bifurcation angle
> was the angle between them, θ = arccos(u_LAD · u_LCx) (eq:method-angle), where u are unit
> vectors and · is the dot product. θ lies between 0 and 180 degrees, and a wider angle means the
> two arteries leave the bifurcation further apart. Although a bend within this stretch changes
> the angle, [what the stretch gains]. The angle was recorded as missing for participants whose
> LAD and LCx share no first point or whose LAD or LCx is shorter than 10 mm.
>
> **Other Angles at the Bifurcation** (`sec:method-angle-other`): the angles between the left main
> and each of the two arteries were not used, as only the LAD–LCx angle was associated with
> stenosis when all three were measured in the same patients \cite{cui2017bifurcation}. The inflow
> angle, at which the left main enters the plane of the two arteries, was not used, as it did not
> differ between stenosed and stenosis-free trees \cite{zhang2024curvature}.

Details:
- `eq:method-angle` kept; `eq:method-angle-mean` removed (grep first that nothing references it).
- The text writes arccos of the dot product; the code computes the same angle another way. Noted
  in the header, not in the text.
- Header comments updated: this decision, the sources, the simulation numbers, and CHECKs:
  Zhang's inflow result was read from the arXiv version (confirm in the published paper before
  submission); Cui is 2D, referred and cross-sectional, so "was associated", never "predicts";
  the ramus intermedius question stays open.
- Citations: all three keys already in `refs.bib`; nothing added.
- `Thesis_coronary/CLAUDE.md` (content map) is not changed now; it follows commits.

## Verification

- `python CGPS_data/thesis_final/bifurcation_angle.py --check` passes and prints the comparison.
- `python Thesis_coronary/content/methodology/figures/bifurcation_angle_figure.py`, then view the
  PNG to check labels do not overlap and the printed angle equals the code's value.
- Build `Thesis_coronary/main.tex` and confirm no undefined references or citations from 05b.
- Reread the tex against the code line by line: depths, step, missing rules, direction of the
  vectors.

No commit unless you ask.
