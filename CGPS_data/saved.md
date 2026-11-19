# Curvature scores per segment model: parameter budget

Output of `segment_k_budget.py`, dtu-gpu-7, 4 November 2026 (aggregates only).

Plaque-free at BL with a FU row: 1077 (read at BL: 1077). An event is plaque (minimal or worse) in that segment at FU; n counts the segments graded at FU. Base: 1 df. K_max = largest P by Riley criteria (i) and (ii) minus the base df, at three anticipated C of the segment model; events/10 and /15 minus the base df for comparison. No image-quality exclusion yet. The outcome-blind shape count (turning_profile_shapes.md) caps K from the other side: K = min(shapes that pass, K_max).

| segment | n graded | events | % events | events/10 | events/15 | K_max C=0.65 | K_max C=0.70 | K_max C=0.75 | mean risk ±0.05 |
|---|---|---|---|---|---|---|---|---|---|
| plad | 1075 | 275 | 25.6 | 26 | 17 | 5 | 10 | 18 | met |
| mlad | 1076 | 201 | 18.7 | 19 | 12 | 4 | 8 | 14 | met |
| dlad | 1073 | 90 | 8.4 | 8 | 5 | 1 | 3 | 7 | met |
| pcx | 1076 | 99 | 9.2 | 8 | 5 | 1 | 4 | 7 | met |
| mcx | 1073 | 40 | 3.7 | 3 | 1 | 0 | 1 | 2 | met |
| dcx | 1074 | 12 | 1.1 | 0 | -1 | 0 | 0 | 0 | met |
| prca | 1060 | 88 | 8.3 | 7 | 4 | 1 | 3 | 6 | met |
| mrca | 1020 | 123 | 12.1 | 11 | 7 | 2 | 5 | 9 | met |
| drca | 1063 | 42 | 4.0 | 3 | 1 | 0 | 1 | 2 | met |

The −1 for dcx under events/15 means the base alone already exceeds that rule; the script now shows 0.

## What it means

- K_max is the number of curvature scores, each with its own weight, that a single-segment model can
  carry on top of the 1-df base. C = 0.70 is the primary column and C = 0.65 the conservative one.
- The final K per segment is the smaller of K_max and the number of shapes that pass the
  outcome-blind checks (bootstrap, Horn, cross-validation), fixed before geometry meets the outcome.
- Three groups:
  - pLAD, mLAD (8–10 at C = 0.70; 4–5 at 0.65): room for every stable shape.
  - mRCA, pLCx, dLAD, pRCA (3–5; 1–2 at 0.65): about 2 shapes.
  - mLCx, dRCA (1; 0 at 0.65): at most φ1. dLCx (12 events): no model; describe only.
- Being within budget limits overfitting but does not give precision. A 95% CI for an OR per SD is
  roughly ×/÷ 1.17 with 275 events and ×/÷ 1.33 with 40 events (approximation), so an OR of
  about 1.2 is only resolvable in pLAD and mLAD.
- The anticipated C of a single-segment model is unknown; the person-level SCORE2 base gave an
  out-of-fold C of 0.687.
- mRCA has 1,020 graded of 1,077: about 57 FU segments were not graded (unevaluable).
- Counts are on the 1,077 before the image-quality exclusion; rerun once the study cohort is fixed.
