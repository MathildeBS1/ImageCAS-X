# Starting point this week: matching the Medis centerlines to the outcomes

The first thing I did this week was check how many of the Medis centerline trees could be linked to
the visual analysis. My earlier scripts, the trunk split and the progression analysis, ended up
with only about 200 patients. That made it look as if most of the 600 trees could not be matched to
a study ID. I wrote a short script that does only the matching: it reads the study ID from the
number in each tree's file name and looks it up in the baseline and follow-up spreadsheets. All 600
trees matched a patient in both visits, and every one of these scans was read at baseline. The
drop to about 200 must therefore happen later in the earlier scripts, when trees are split into
trunk segments and trees that cannot be split are skipped, and not in the ID matching.

The match also showed which patients the Medis trees come from. All but one of the 600 had plaque
at baseline. Of these, 541 progressed by follow-up, meaning at least one segment had a higher
stenosis grade, and 58 stayed the same or regressed. The one patient who was plaque-free at baseline
had developed plaque by follow-up. The Medis trees are therefore a reference from patients who
already have disease. They can be used to validate the geometry from the in-house tracer and to
study progression, but not to answer whether geometry predicts new plaque in the plaque-free
cohort.
