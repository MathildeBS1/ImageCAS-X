# Validating a landmark rule for proximal/mid/distal segment division without ground truth

Scope: the rule splits tracer centerlines of the LAD, LCx and RCA into proximal/mid/distal using side-branch origins and fixed length fractions (medians of reader boundaries, fitted on a random half of Medis trees and tested on the other half). Medis reader labels exist only for people with plaque at baseline, not for the plaque-free target cohort. Two planned steps: (1) rule vs reader labels on Medis centerlines (share of length with the same label, boundary error in mm); (2) plaque-contour miss rate, tracer vs Medis cut at reader labels.

## Q1. Imperfect reference standard: methods and how to phrase validation when the reference is a reader's choice

### Takeaway
The standard literature says that when the reference is imperfect, you should report *agreement*, not accuracy, and add a check of clinical usefulness. The planned design compares the rule with one reader's labels and has no reader-vs-reader benchmark. That is its main weakness: without one, nobody can tell whether a rule-vs-reader disagreement of X mm is large or small.

### Cited Findings
- Reitsma et al. (2009) sort solutions for an imperfect or missing reference standard into four groups: impute or adjust for missing reference data; correct accuracy estimates for the imperfect reference; build a composite reference (a predefined rule, consensus, or a statistical model); and drop the accuracy framework in favour of "clinical test validation" when no acceptable reference exists. Reitsma JB, Rutjes AWS, Khan KS, Coomarasamy A, Bossuyt PM. J Clin Epidemiol 2009;62(8):797–806. doi:10.1016/j.jclinepi.2009.02.005 — [Birmingham repository](https://research.birmingham.ac.uk/en/publications/a-review-of-solutions-for-diagnostic-accuracy-studies-with-an-imp/)
- The longer companion review is Rutjes AWS, Reitsma JB, Coomarasamy A, Khan KS, Bossuyt PMM. "Evaluation of diagnostic tests when there is no gold standard. A review of methods." Health Technol Assess 2007;11(50). doi:10.3310/hta11500 — [NIHR](https://njl-admin.nihr.ac.uk/document/download/2001451)
- STARD 2015 is a 30-item list for reporting diagnostic accuracy studies (Bossuyt PM, Reitsma JB, et al. BMJ 2015;351:h5527. doi:10.1136/bmj.h5527). The Explanation and Elaboration is Cohen JF et al., BMJ Open 2016;6(11):e012799. doi:10.1136/bmjopen-2016-012799 — [BMJ](https://www.doi.org/10.1136/BMJ.H5527); [E&E](https://bmjopen.bmj.com/content/6/11/e012799)
- GRRAS (Guidelines for Reporting Reliability and Agreement Studies) gives 15 items for reporting interrater and intrarater agreement. Kottner J, Audigé L, Brorson S, Donner A, Gajewski BJ, Hróbjartsson A, Roberts C, Shoukri M, Streiner DL. J Clin Epidemiol 2011;64(1):96–106. doi:10.1016/j.jclinepi.2010.03.002 — [Manchester](https://research.manchester.ac.uk/en/publications/guidelines-for-reporting-reliability-and-agreement-studies-grras-/)
- Coronary precedent: Cao et al. evaluated automatic coronary segment labelling on 83 CCTA datasets (1,149 segments) against two experts. They reported the algorithm's agreement (89.2% right-dominant, 83.6% left-dominant) **next to** the two experts' agreement with each other (97.6% RD, 87.6% LD). The inter-expert figure is the ceiling. Agreement was much lower in left-dominant trees, for experts and algorithm alike. Cao Q, Broersen A, de Graaf MA, Kitslaar PH, Yang G, Scholte AJ, Lelieveldt BPF, Reiber JHC, Dijkstra J. Int J Cardiovasc Imaging 2017;33(11):1809–1819. doi:10.1007/s10554-017-1169-0 — [Springer](https://link.springer.com/article/10.1007/s10554-017-1169-0)
- A deep-learning labelling study likewise reports algorithm vs expert (96.2% label presence, 94.0% overlap) next to expert vs expert (95.0%) — [BMC Med Inform Decis Mak 2023, PMC10626726](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10626726/)
- SCCT segment boundaries are themselves ambiguous. In the ASCI-PT 2024 consensus, only 64.7% (11/17) of panellists agreed on the proximal-vs-mid LAD rule (mid-LAD once D1 > 1.5 mm), and 63.2% initially favoured the opposite reading. These are panel votes, not measured inter-reader agreement. Kim C, Park CH, ..., Yang DH. Korean J Radiol 2024;25(4):331–342. doi:10.3348/kjr.2024.0112 — [PMC10973734](https://pmc.ncbi.nlm.nih.gov/articles/PMC10973734)

### Inferences
- Wording for the thesis: "agreement with reader-assigned segment boundaries in Medis", never "accuracy" or "error against ground truth". Call the mm quantity the "boundary difference (rule − reader)", not "boundary error". Say once that a disagreement can be the reader's choice rather than a rule failure (for example, the D1-based proximal/mid LAD boundary, which experts themselves dispute).
- Best fix (a composite or benchmark reference in Reitsma's terms): have a second reader, or the student blinded to Medis labels, independently place boundaries on a random subset of Medis trees (for example 30–50 arteries per vessel). Report rule-vs-reader next to reader-vs-reader, as Cao et al. 2017 do. If the rule-vs-reader limits of agreement are close to the reader-vs-reader ones, the rule is "as good as a second reader", which is the strongest claim available without ground truth.
- If no second reading is feasible, say it as a stated limitation and do not interpret the mm numbers as error.
- Reitsma's fourth group, "clinical validation", maps onto the downstream sensitivity analysis (Q5). It is a recognised paradigm, not an ad-hoc substitute.
- Report it as STARD/GRRAS would ask for an agreement study: how the Medis trees were selected (a plaque-at-BL subset, by which readers), whether reader labels were made blind to the rule (yes by construction), how many trees were excluded (missing landmarks, anomalies, left dominance) and why, and CIs.

### Gaps
- No published inter-reader agreement for proximal/mid/distal boundary *positions in mm* on CCTA was found. The ASCI-PT figures are votes, and Cao et al. report segment-level agreement percentages.
- It is unknown whether the Medis labels were placed by one reader or several, and whether readers checked the whole tree or only the contoured part (CGPS_data/CLAUDE.md says "probably only the contoured part was checked"). If only the contoured part was checked, boundaries far from plaque may be unchecked software defaults, which would make the reference weaker than it looks.

## Q2. Fitting rule parameters: is a random half split adequate?

### Takeaway
A single random half split wastes data and gives noisy estimates. Because the rule has only a few parameters (one median fraction per boundary), overfitting is small anyway. Better: fit the medians on all trees, estimate agreement with person-level cross-validation (or a bootstrap), and give bootstrap CIs.

### Cited Findings
- Steyerberg et al. (2001): split-sample validation gave overly pessimistic estimates with large variability. The bootstrap gave stable estimates with low bias, and 10-fold cross-validation had low bias and low variability. The authors conclude that split-sample validation is inefficient and recommend the bootstrap. Steyerberg EW, Harrell FE Jr, Borsboom GJ, Eijkemans MJ, Vergouwe Y, Habbema JD. J Clin Epidemiol 2001;54(8):774–781. doi:10.1016/S0895-4356(01)00341-9 — [Erasmus repository](https://repub.eur.nl/pub/74159)
- Austin and Steyerberg (2017) found that split-sample assessment gave "too pessimistic and highly uncertain" performance estimates. Stat Methods Med Res 2017;26(2):796–808. doi:10.1177/0962280214558972 — [PMC5394463](https://pmc.ncbi.nlm.nih.gov/articles/PMC5394463)

### Inferences
- With roughly 600 Medis trees and about 2 boundaries × 3 arteries of median parameters, the optimism from fitting a median is tiny. A half split mainly halves precision. Recommended design:
  1. Final parameters: medians from **all** trees.
  2. Out-of-sample agreement: K-fold (e.g. 10-fold) by person, or leave-one-out. A median is cheap, so leave-one-out is trivial. Report the cross-validated agreement.
  3. CIs: a person-level bootstrap over the cross-validated per-artery metrics.
  4. Optionally show the gap between apparent and cross-validated agreement, to show that tuning optimism is negligible.
- If the half split stays (it is easy to explain), at least repeat it (e.g. 200 random splits) and report the spread, so the result does not depend on one draw.
- Fix the split unit to the person (one tree per person, so this is automatic, but say it). This matches the thesis rule that cross-validation is split by person.
- The fit and the evaluation must use the same length definition. A fraction fitted on Medis lengths and applied to tracer lengths transfers only if both trees end at comparable distal points (see Q4).

### Gaps
- No source specifically on validating low-parameter anatomical rules was found. The prediction-model literature is the closest analogue.

## Q3. Metrics: length-wise agreement, boundary distance (Bland–Altman), per-segment confusion

### Takeaway
Use three metrics that complement each other: (a) a length-weighted 3×3 confusion matrix per artery (proximal/mid/distal), with overall length agreement as its trace; (b) the signed boundary difference in mm per boundary, with Bland–Altman bias and 95% limits of agreement plus the share within ±5 mm and ±10 mm; (c) an outcome-relevant metric: the share of reader-labelled plaque contours that the rule places in the reader's segment. Metrics Reloaded's principle is to pick metrics that reflect the domain interest, and here the domain interest is putting geometry and plaque into the correct segment.

### Cited Findings
- Metrics Reloaded: metrics are often chosen without regard to the domain interest. The framework derives metrics from a "problem fingerprint" (domain interest, target structures, data set, output). Maier-Hein L, Reinke A, Godau P, et al. Nat Methods 2024;21(2):195–212. doi:10.1038/s41592-023-02151-z — [Warwick repository](https://wrap.warwick.ac.uk/183654)
- Bland–Altman: correlation is not agreement. Analyse the paired differences (bias, limits of agreement = mean ± 1.96 SD) against the pair mean. Bland JM, Altman DG. Lancet 1986;1(8476):307–310. doi:10.1016/S0140-6736(86)90837-8 — [authors' reprint](https://www-users.york.ac.uk/~mb55/meas/ba.htm)
- Schaap et al. (2009) set the standard for coronary centerline evaluation: overlap measures computed along the reference centerline with a correspondence between points. This is the template for "share of centerline length with matching label". Schaap M, Metz CT, van Walsum T, et al. Med Image Anal 2009;13(5):701–714. doi:10.1016/j.media.2009.06.003 — [RUG](https://research.rug.nl/en/publications/standardized-evaluation-methodology-and-reference-database-for-ev/)
- Cao et al. 2017 reported segment start/end point precision (92.0% RD, 90.7% LD) against experts, which is a boundary-based metric — [Springer](https://link.springer.com/article/10.1007/s10554-017-1169-0)
- Per-artery accuracy is lower in the LCx and its branches because of anatomical variation (review statement in the 2023 BMC paper) — [PMC10626726](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10626726/)

### Inferences
- The single "% length with the same label" is hard to interpret. It depends on artery length and is dominated by the long mid/distal stretches. The trace of a length-weighted confusion matrix gives the same number, and the off-diagonal cells show *which* boundary fails (for example proximal→mid vs mid→distal).
- The signed boundary difference is the most interpretable number for a reader ("the rule places the proximal/mid LAD boundary on average 2 mm distal to the reader, 95% LoA −12 to +16 mm"). Caveats:
  - Bland–Altman LoA assume roughly normal differences. Landmark-based boundaries probably have a mixture: near zero when the same side branch is chosen, large when a different branch is chosen. Check this with a histogram. If the distribution is heavy-tailed, report the median and IQR or the 2.5–97.5 percentiles, plus the share of boundaries with a "different landmark chosen".
  - Plot the difference against artery length or boundary position (the BA plot's x-axis) to show proportional error. Fixed fractions should err more in long or unusual arteries.
  - Report per artery and per boundary, split by dominance. Left dominance is where experts disagree most (Cao 2017).
- The plaque-contour metric (step 2) is closest to the domain interest, because in the analysis segment plaque is the outcome. Defined as "of reader-labelled plaque contour stretches, the share whose centre falls into the same segment under the rule", it is a direct estimate of outcome-location concordance. It is weighted towards proximal segments, where plaque concentrates. That is fine for its purpose, but say it.

### Gaps
- No standard metric for "segment-label agreement along a 1-D centerline" with established thresholds was found. Clinical relevance thresholds (e.g. ±5 mm) would have to be justified locally, for example against typical segment lengths or the 1.5 mm side-branch convention in SCCT/ASCI-PT.

## Q4. Transportability (spectrum): validated on plaque arteries, applied to plaque-free arteries

### Takeaway
This is a classic spectrum effect: performance estimated in one patient mix may not hold in another. Nothing can measure agreement directly in the plaque-free cohort. What can be done: (i) argue it mechanistically; (ii) test whether agreement depends on disease burden *within* Medis; (iii) compare label-free distributions (rule-derived segment lengths and fractions, landmark detection rates) between the Medis set and the clean cohort; (iv) visually audit a random sample of clean-cohort trees.

### Cited Findings
- Spectrum bias, or spectrum effect: test performance varies between subgroups and settings with different case mix. Mulherin SA, Miller WC. Ann Intern Med 2002;137(7):598–602. doi:10.7326/0003-4819-137-7-200210010-00011 — [Catalog of Bias](https://catalogofbias.org/biases/spectrum-bias/)
- The foundational paper is Ransohoff DF, Feinstein AR. N Engl J Med 1978;299(17):926–930. doi:10.1056/NEJM197810262991705 — cited via [Wikipedia: Spectrum bias](https://en.wikipedia.org/wiki/Spectrum_bias)
- Fox, Lash and Bodnar warn that transporting sensitivity and specificity estimates from external validation data to another population is a known pitfall — [PMC7750925](https://pmc.ncbi.nlm.nih.gov/articles/PMC7750925)
- Labelling studies often exclude severe proximal lesions and anomalies (Cao et al. excluded severe proximal lesions), so published accuracies come from a selected spectrum — [Springer](https://link.springer.com/article/10.1007/s10554-017-1169-0)

### Inferences
- Mechanistic argument, and its limits. Side-branch origins and fraction-of-length do not depend on plaque directly. But (a) plaque and stenosis can make the *tracer* stop early or deviate, and the plaque-free cohort has none of that. (b) Fractions depend on where the distal end is. If the tracer traces plaque-free (often younger, cleaner-image) arteries further distally than readers traced Medis trees, every fraction-based boundary moves distally. This is probably the largest transport risk and is about the tracer, not about plaque. (c) The plaque cohort is older and more often male, which may differ in artery length and dominance mix.
- Within-Medis test: stratify or regress the boundary difference on a disease-burden gradient (baseline SIS/SSS or CACS, 1 vs ≥ 2 diseased segments, plaque in the segment adjacent to the boundary vs not). If agreement does not change across the gradient, extrapolating to zero burden is more credible. It is still an extrapolation, and it should be called one.
- Label-free comparison: in the clean cohort and in Medis, compare tracer artery length, landmark detection rate (side branch found), rule-derived segment lengths, and the distance from the ostium to each boundary. Large shifts signal a transport problem without needing labels. Report only aggregates (MIN_CELL = 5).
- Visual audit: an expert, or the student blinded to outcome, rates a random sample of clean-cohort trees (e.g. n = 50) as "boundary plausible / implausible". It is crude, but it is the only direct check in the target population. Freeze the rule **before** looking at the outcome (the tracer clean cohort is pending).
- Phrase it as: "agreement was estimated in participants with plaque at baseline; it is assumed, not shown, to carry over to the plaque-free cohort; the following checks support/qualify that assumption".

### Gaps
- No study was found that measures coronary segment-labelling agreement separately in plaque-free vs diseased arteries.

## Q5. Downstream sensitivity analysis to boundary misplacement (quantitative bias analysis)

### Takeaway
Boundary misplacement causes misclassification in both exposure and outcome location. Segment geometry is computed over the rule's stretch, while follow-up plaque is assigned by the reader's segment label. Quantitative bias analysis (Lash et al. 2014) is the accepted framework. Its bias parameters should come from validation data, which is exactly what step 1 provides. Downstream sensitivity therefore *complements* the agreement check; it cannot replace it.

### Cited Findings
- Good practices for QBA: quantify the direction, magnitude and uncertainty from systematic errors, guided by a protocol. Lash TL, Fox MP, MacLehose RF, Maldonado G, McCandless LC, Greenland S. Int J Epidemiol 2014;43(6):1969–1985. doi:10.1093/ije/dyu149 — [UMN](https://experts.umn.edu/en/publications/good-practices-for-quantitative-bias-analysis/)
- Validation data can be combined with QBA to compute bias-adjusted estimates. Transporting validation parameters to a different population is a known pitfall — [Fox, Lash, Bodnar, PMC7750925](https://pmc.ncbi.nlm.nih.gov/articles/PMC7750925)
- Textbook: Fox MP, MacLehose RF, Lash TL. Applying Quantitative Bias Analysis to Epidemiologic Data, 2nd ed. Springer 2021. doi:10.1007/978-3-030-82673-4 — [Springer](https://link.springer.com/10.1007/978-3-030-82673-4)
- Misuse: bias analyses that assume only nondifferential misclassification can mislead, and good-practice adherence guards against manipulation ("Bias analysis gone bad", Lash TL, Ahern TP, Collin LJ, Fox MP, MacLehose RF. Am J Epidemiol 2021;190(8):1604–1612. doi:10.1093/aje/kwab072) — [UMN](https://experts.umn.edu/en/publications/bias-analysis-gone-bad/)
- Correction methods for outcome misclassification in *matched* or conditional designs are less developed than for unmatched logistic regression (search finding; e.g. the Sinha group's work on matched case-control misclassification) — [TAMU pdf](https://web.stat.tamu.edu/~sinha/research/kxz012.pdf)

### Inferences
- Why it matters here: the per-segment outcome (`ct_cag_<segment>_*` at FU) is defined by the reader's segment convention, but the per-segment geometry comes from the rule. Any rule-vs-reader offset puts part of a reader-"proximal" stretch into the rule's "mid", and so on. This applies to the who model too, which is also segment-level (the pooled cloglog GLMM over 9 trunk segments), not only to the where question.
- Proposed probabilistic bias analysis, prespecified:
  1. From step 1, take the empirical (cross-validated) distribution of signed boundary differences per boundary and artery.
  2. In each of B ≈ 200–500 iterations, perturb every clean-cohort boundary by a draw from that distribution (resampled, not assumed normal), recompute the segment features, refit the prespecified model, and store the LR statistic, coefficient(s), ΔC and calibration.
  3. Report the median and 2.5–97.5 percentiles of these quantities next to the main estimate.
  4. Add a simple deterministic grid as well (all boundaries shifted −10, −5, +5, +10 mm, or ± one LoA), which is easier to read.
- If conclusions are stable under realistic perturbation, the agreement level is "good enough for purpose". That is the strongest practical argument when there is no ground truth, and it fits Reitsma's "clinical validation" group.
- Limits: the perturbation draws come from the diseased Medis set (the transport issue again), so widen them (e.g. inflate SD by 1.5×) as a stress test. Within-person, nondifferential misclassification usually attenuates segment effects, but features like taper and curvature are not linear in stretch length, so do not assume the direction; simulate it.
- Freeze it before outcome data: the perturbation scheme, B, and which quantities are reported belong in the analysis plan, so the sensitivity analysis cannot be tuned after the fact (Lash 2021).

### Gaps
- No published coronary-geometry study with a boundary-perturbation QBA was found. The design above is an adaptation, not an established precedent.

## Q6. Downstream sensitivity vs direct agreement: substitute or complement?

### Takeaway
They complement each other. Direct agreement answers "does the rule reproduce the reader convention?" and supplies the bias parameters. Downstream sensitivity answers "does residual disagreement change the thesis conclusions?". Without step 1, the perturbation sizes would be arbitrary. Without the sensitivity analysis, the mm numbers have no meaning for the research question.

### Cited Findings
- QBA bias parameters should be informed by validation data where possible, and their source and uncertainty should be reported (Lash et al. 2014, doi:10.1093/ije/dyu149) — [UMN](https://experts.umn.edu/en/publications/good-practices-for-quantitative-bias-analysis/); [PMC7750925](https://pmc.ncbi.nlm.nih.gov/articles/PMC7750925)
- Reitsma et al. 2009 present "clinical validation" as an alternative paradigm for when no acceptable reference standard exists — [Birmingham](https://research.birmingham.ac.uk/en/publications/a-review-of-solutions-for-diagnostic-accuracy-studies-with-an-imp/)

### Inferences — critiques of the planned two steps and the recommended design
1. **Step 1 validates the rule on Medis centerlines, not the rule on tracer centerlines.** The thesis applies the rule to tracer trees, so add a step 1b: run the rule on the tracer centerline of the same Medis participants, map it into Medis coordinates (coordinate frame still open in 01b), and compare it with the reader labels projected by nearest point. This measures the combined tracer + rule disagreement, which is what affects the analysis. The step 1 vs 1b difference isolates the tracer's contribution, especially distal-end and landmark-detection effects on the fractions.
2. **Without a reader-vs-reader benchmark, the numbers cannot be interpreted.** Get a second independent labelling on a subset if at all possible (Q1).
3. **The half split is inefficient.** Fit on all trees, use cross-validation and bootstrap CIs by person (Q2).
4. **Step 2 is the most relevant check** (outcome-location concordance), but: plaque contours exist only for diseased segments, labels come from the same reader (not independent of step 1), and "miss rate" needs a precise definition (contour centre in the wrong segment? any overlap?). Report it per artery and segment with CIs, and compare tracer+rule with the reader's own cut, which by construction gives 100%. A more informative comparator is "Medis centerline + rule", which separates rule error from tracer error.
5. **Transport to plaque-free arteries cannot be measured directly.** Use the within-Medis burden gradient, the label-free distribution comparison and a small visual audit, and phrase it as an assumption (Q4).
6. **Add the prespecified probabilistic boundary-perturbation analysis** of the main LR test and ΔC (Q5), with perturbations drawn from the step 1b differences.
7. **Exclusions and flow:** report how many Medis trees and how many clean-cohort tracer trees the rule could not apply to (missing side branch, short trace, left dominance, anomalies), as STARD's participant-flow item asks. Silent exclusions are the usual way labelling studies inflate agreement (Cao 2017 excluded severe proximal lesions).

### Gaps
- TRIPOD+AI (Collins GS et al. BMJ 2024;385:e078378, doi:10.1136/bmj-2023-078378) covers prediction models, not preprocessing rules. Its content was not checked in this session. Cite it only for the downstream model reporting, not for the segment rule.
- Unknown: how Medis labels were produced (semi-automatic, reader-corrected?) and the coordinate frames. Both are open in `thesis/methodology/01b_medis_reference.tex` and directly limit how strong a reference Medis can be.
