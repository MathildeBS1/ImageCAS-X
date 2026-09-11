# griffo2026wss — Geometric deep learning-based coronary WSS estimation

**Citation:** Griffo B, Gallo D, Marlevi D, Laudato M, Mastronuzzi G, Chiastra C, Candreva A,
Collet C, De Bruyne B, Erriquez A, Campo G, Biscaglia S, Morbiducci U, Lodi Rizzini M.
*Computers in Biology and Medicine* 2026;205:111583. doi:10.1016/j.compbiomed.2026.111583.
PMID 41747562. Received 12 Dec 2025 / accepted 21 Feb 2026, CC BY.
**Read:** 2026-09-07 — **full text of the published version**, 12 pages, PDF supplied by the user and
stored beside this entry.
**Source:** `docs_thesis/papers/Geometric deep learning-based coronary wall shear stress estimation from real-world patients.pdf`
**Verdict:** Licenses the thesis's central premise — the shear field is recoverable from geometry
alone — but the prognostic half of that claim is weaker than the abstract implies and rests on a
design that is not population risk prediction.

## What they did

1078 coronary arteries (single-branch LAD, LCX, RCA segments) from 748 patients, reconstructed from
**invasive angiography (3D-QCA)**, not CCTA. Time-averaged WSS from transient CFD (CAAS Workstation
WSS) served as reference labels for a gauge-equivariant mesh graph convolutional network (GEM-GCN).

**The dataset is pooled from three clinical trials**, which is the single most important fact about
it: FAME 2 (n = 520), FIRE (n = 371), and a "future culprit" multicentre study (n = 187). Median
percentage area stenosis 58.5%. These are trial-enrolled, diseased arteries.

Two experiments: a random split with 10-fold cross-validation, and a **clinical split** holding out
only the 187 future-culprit vessels as test set. In that subset, 80 vessels carried a lesion that
later became the MI culprit and 107 carried a non-culprit lesion, with angiography 1 month to 5 years
before the event (median 25.9 months).

High-WSS surface areas were defined per vessel by the **80th percentile** of the WSS magnitude
distribution.

## What they found

**Accuracy (random split):** absolute error 0.48 [0.26–0.78] Pa, percentage error 23.6 [14.8–42.6]%,
slightly underestimating lesion- and vessel-averaged WSS. Spatial agreement on high-WSS regions
0.88 [0.81–0.92]. **Clinical split:** absolute error 0.65 [0.41–1.12] Pa, spatial agreement
0.84 [0.71–0.90]. Under 5 s per vessel.

**Normalization:** correlation between GEM-GCN and CFD lesion-averaged WSS rose from R = 0.67 to
R = 0.89 (p < 0.0001) after dividing by vessel-averaged WSS.

**MI prediction — the numbers the abstract omits.** Lesion-averaged WSS: **AUC 0.63** (95% CI
0.55–0.71, p = 0.0019) for CFD and **AUC 0.63** (0.55–0.71, p = 0.0034) for GEM-GCN, DeLong p = 0.84.
Lesion-to-vessel WSS ratio: **AUC 0.66** (0.58–0.74) for CFD and **AUC 0.68** (0.60–0.76) for
GEM-GCN, DeLong p = 0.37.

## What the abstract does not tell you

- **"Comparable MI prediction performance" means comparably moderate.** AUC 0.63–0.68. The authors
  say so themselves: *"The moderate predictive power observed in this study is primarily attributable
  to the multifactorial nature of MI. WSS represents an individual component within a complex
  pathophysiologic process."* The equivalence claim is sound; the magnitude is modest.
- **It is not population risk prediction.** The MI analysis discriminates 80 future-culprit from 107
  non-culprit lesions **within the same patients**, all of whom went on to have an MI. It answers
  "which lesion became the culprit", not "which patient has an event".
- **"Dice distance" is the Dice similarity coefficient.** Defined in §2.4 as
  DD = 2(SA_CFD ∩ SA_DL)/(SA_CFD + SA_DL), 0 ≤ DD ≤ 1. So 0.88 is good agreement, as everyone
  assumes — but the paper's own label is wrong. Quote it as spatial agreement, not as "Dice
  distance".
- **The spatial-agreement figure is for HIGH-WSS regions** (80th percentile), not low. The
  mechanism this thesis leans on in §5 is that *low* drag is where plaque begins. Griffo's strongest
  localisation result is at the opposite tail.
- **Modality gap.** Invasive angiography, not CCTA. The thesis and CGPS are CCTA.
- **Conceded limitations:** WSS-magnitude discrepancies attributed to dataset size against real-world
  geometric variability; the architecture's hyperparameters were optimised in prior work on **2000
  idealised** coronary arteries, not real ones; the model predicts cycle-averaged WSS only, not
  time-resolved.

## What it licenses

- **§4.4 (state of the art), the CFD-free premise:** the shear field is recoverable from geometry
  alone to useful accuracy, and the prognostic content survives the substitution (DeLong p = 0.84
  and 0.37). This is the sentence `05_hemodynamics.tex` previously asserted with no citation.
- **Objective 7, feature definition:** the R = 0.67 → 0.89 jump on normalising by vessel-averaged
  WSS licenses defining features as **ratios and within-tree z-scores** rather than absolute
  quantities. The relative pattern transfers; the absolute level does not.
- **The lesion-to-vessel ratio outperforming the lesion average** (0.66/0.68 vs 0.63/0.63) is a
  second, independent argument for the same normalisation choice.
- **A realistic expectation for effect size.** If shear-derived features reach AUC 0.63–0.68 for
  lesion-level MI in a selected cohort, tree-scale geometric features should not be expected to do
  better, and the thesis should not promise it.

## What it does NOT license

- **Not "geometry predicts heart attacks".** It discriminates culprit from non-culprit lesions inside
  patients who already had one, at AUC 0.63–0.68.
- **Not tree scale.** Single-branch LAD, LCX or RCA segments, one vessel at a time. No tree, no
  bifurcation topology, no whole-heart model. It licenses the premise, not the method.
- **Not a general population.** Pooled from FAME 2, FIRE and a future-culprit case series, median
  58.5% area stenosis. Transfer to CGPS — a general population cohort — is an open question, not an
  established one.
- **Not CCTA.** 3D-QCA from invasive angiography throughout.
- **Not evidence that shape predicts plaque composition.** Composition is never assessed.

## Open questions

- Does the geometry → WSS mapping hold on CCTA-derived lumens, which are lower-resolution and
  blooming-affected relative to 3D-QCA? Nothing here answers it, and it is the step the thesis needs.
- The network was hyperparameter-tuned on 2000 idealised arteries and applied to real ones. Would
  retraining on real geometry close the 23.6% percentage error, and does that matter for a
  ratio-based feature?
- If the lesion-to-vessel ratio beats the lesion average, is there a tree-scale analogue —
  a segment-to-tree normalisation — worth defining for objective 7?
