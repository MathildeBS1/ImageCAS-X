# Supervisor questions

**Written:** 2026-09-09, week 2. Focused on the four gap texts: whole tree, features,
healthy cohort, segmentation.

1. **[Whole tree] Do CGPS trees get artery names at all?** The pretrained models predict a
   binary lumen, not the 14 anatomical labels, so dominance and per-artery features don't exist
   on CGPS unless something else supplies names.
   *Default: label-free tree features for CGPS; named features for ImageCAS-X only.*

2. **[Features] Which tortuosity metric do we commit to** — average absolute curvature, or a
   small panel with one declared primary?
   *Default: curvature as primary, one index reported alongside.*

3. **[Features] Is there a short-interval repeat scan anywhere in CGPS**, or do we substitute
   repeat manual labelling to measure reproducibility? CGPS repeats are years apart, which
   confounds measurement error with real change.
   *Default: repeat manual labelling for measurement error; years-apart repeats reported as
   change, not error.*

4. **[Healthy cohort] What counts as the reference "normal" population** — whole cohort,
   zero-calcium subset, or plaque-free-by-model subset?
   *Default: whole cohort as primary, zero-calcium subset as a sensitivity check.*

5. **[Segmentation] Reproduce or train?** CAS-Net runs today from the delivered pretrained
   weights. Does reproducing the published benchmark satisfy objective 5, or does the thesis
   need to train a segmentation model itself?
   *Default: reproduce from delivered weights; only train if week 3's evaluation finds a gap
   large enough to justify it (ThesisPlan.md week 5).*

6. **[Segmentation] Selected on which metric?** CAS-Net leads on DSC and Betti error, but ties
   ADE-HTL on clDice and centerline distance. Since the downstream unit of analysis is the tree,
   should the segmenter be chosen on Betti error and clDice rather than DSC?
   *Default: keep CAS-Net (already best on Betti error too), but report DSC alongside Betti
   error and clDice so a future re-selection has the numbers to act on.*
