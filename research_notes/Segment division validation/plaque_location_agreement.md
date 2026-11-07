# Plaque-location agreement as a check on segment division (CCTA)

Scope: precedents and benchmarks for checking that plaque found by a reader falls in the same coronary
segment under an alternative/automated segment division; reader reproducibility of segment-level plaque
assignment. Search budget ~18 tool calls; several full texts (PMC, Nature, JACC) were blocked, so many
numbers below are from abstracts/search snippets and are marked as such. DOIs marked "(from memory,
verify)" were not confirmed by a fetched page.

Overall finding up front: **I found no published study that does exactly the planned check** (reader
plaque contours placed on an automatically divided centerline, segment "miss" counted, with a reader-cut
reference centerline as baseline). The nearest precedents are (a) automated SCCT/AHA segment-labelling
papers evaluated against expert labels, (b) landmark-based co-registration in serial CCTA (PARADIGM) and
CT-vs-IVUS work, and (c) segment-level reader agreement studies. None reports a "proportion of lesions
assigned to the same segment by two readers/methods" directly; segment-level kappas measure agreement on
plaque presence per segment, which conflates detection and location.

## Q1. Inter-/intra-reader agreement for segment-level plaque assignment in CCTA

### Takeaway
Segment-level reader agreement for plaque *presence* is typically kappa ~0.7–0.9 in small studies
(20–150 patients), lower for non-calcified plaque and much lower for plaque composition/high-risk features.
No study found isolates disagreement about *which segment* a plaque belongs to; boundary ambiguity (e.g.
D1 as the proximal/mid LAD border) is acknowledged in lexicon material but not quantified.

### Cited Findings
- 64-slice CT, 20 patients, two readers, 262 segments: segment-level plaque detection weighted kappa 0.88
  (95% CI 0.76–0.95); plaque type only moderate (unweighted kappa 0.45). Very small sample. — Intra- and
  interobserver variability in detection and assessment of calcified and noncalcified coronary artery
  plaques using 64-slice CT, Int J Cardiovasc Imaging 2008, DOI 10.1007/s10554-008-9299-z
  ([Springer](https://link.springer.com/article/10.1007/s10554-008-9299-z);
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/18587663))
- Dual-source CT, 150 patients, low-dose vs retrospective protocols: interobserver agreement for plaque
  detection was significantly higher for calcified than non-calcified plaque; high-pitch protocol segment
  agreement 664/748 segments (88.8%). — Eur Radiol 2012, DOI 10.1007/s00330-012-2389-2
  ([PubMed](https://pubmed.ncbi.nlm.nih.gov/22661076/))
- Danish study (Copenhagen, includes CGPS-related authors Nordestgaard, Kofoed): de Knegt MC, Linde JJ,
  Fuchs A, Nordestgaard BG, Køber LV, Hove JD, Kofoed KF. Reproducibility of coronary atherosclerotic plaque
  characteristics in populations with low, intermediate, and high prevalence of CAD by MDCT: a guide to
  reliable visual coronary plaque assessments. Int J Cardiovasc Imaging 2016;32(10):1555–66,
  DOI 10.1007/s10554-016-0932-y. 150 patients (50 asymptomatic, 50 symptomatic non-ACS, 50 ACS), 4 readers,
  320-slice CT, all segments. Presence-of-CAD kappa 0.73, rising to 0.81 after accounting for heart rate,
  BMI, **plaque location** and stenosis >/<50%. The abstract does not state whether these are segment-level.
  — [PubMed](https://pubmed.ncbi.nlm.nih.gov/27378095)
- ROMICAT-II substudy (30 patients, 3 readers, acute chest pain): kappa 0.77 for coronary plaque presence,
  0.69 for high-risk plaque. — Puchner SB et al., JACC 2014, DOI 10.1016/j.jacc.2014.05.039
  ([JACC](https://www.jacc.org/doi/10.1016/j.jacc.2014.05.039))
- Plaque detection vs a three-reader consensus: kappa 0.582–0.802 across readers; the most experienced
  reader was less variable and more accurate (2010 study, snippet only). —
  [Erasmus repository](https://pure.eur.nl/en/publications/reproducibility-accuracy-and-predictors-of-accuracy-for-the-detec/)
- CT vs IVUS, 1,002 co-registered cross-sections: interobserver kappa for plaque detection on CT 0.48
  (non-calcified), 0.42 (mixed), 1.00 (calcified) (snippet only; source in same search result set). —
  [Leiden repository](https://scholarlypublications.universiteitleiden.nl/access/item%3A3729155/view)
- CAD-RADS (patient-level category, not segment): 50 cases, 8 readers (4 expert, 4 early career), ICC 0.958
  for categories; modifier V (high-risk plaque) kappa 0.40. — Maroules CD et al., J Cardiovasc Comput Tomogr
  2018 ([PubMed 29217341](https://pubmed.ncbi.nlm.nih.gov/29217341); DOI 10.1016/j.jcct.2017.11.014 from
  memory, verify)
- CAD-RADS in stable chest pain: category kappas 0.76 (CAD-RADS 2) to 1.0 (CAD-RADS 0); CAD-RADS 1 kappa 0.92.
  — [ResearchGate record](https://www.researchgate.net/publication/326203154_Inter-observer_agreement_of_the_Coronary_Artery_Disease_Reporting_and_Data_System_CAD-RADS_TM_in_patients_with_stable_chest_pain)
- High-risk plaque features have modest interobserver agreement even among experts (kappa 0.15–0.69). —
  [Insights Imaging 2022, DOI 10.1186/s13244-022-01286-5](https://insightsimaging.springeropen.com/articles/10.1186/s13244-022-01286-5)
- CLARIFY interobserver substudy (232 patients, level-3 experts vs AI-QCT): significant interobserver
  variability among expert readers for plaque composition; weighted kappa for percent calcified plaque
  ~0.23–0.34. — [PubMed 35986973](https://pubmed.ncbi.nlm.nih.gov/35986973/)
- Segment boundary ambiguity: in the CAD-RADS lexicon material, the first diagonal sometimes serves as the
  proximal/mid LAD boundary, so a lesion near D1 could reasonably be assigned to either. —
  [ECR 2018 poster C-2139](https://epos.myesr.org/poster/esr/ecr2018/C-2139/findings%20and%20procedure%20details)
- Segment-level CT-coronary-reading reproducibility for SIS specifically, or SCOT-HEART/CONFIRM/PROMISE
  segment-level kappas: not found in searches (see Gaps).

### Inferences
- A segment-level kappa of ~0.8 for plaque presence implies two expert readers disagree on a nontrivial
  share of plaque-positive segments (agreement in 88.8% of *all* segments in the 2012 study includes many
  plaque-free segments). Part of this disagreement is detection, part is location; the literature does not
  separate them. The thesis's "Medis-cut-at-reader-labels" baseline is therefore the right design: it
  absorbs reader/Medis inconsistency so the excess can be attributed to the division.
- Most of these numbers come from symptomatic/referral cohorts with higher plaque burden and larger plaque;
  minimal plaque in a general-population cohort like CGPS is likely harder to detect and locate, so
  agreement there would be expected to be lower, not higher (inference, not shown).
- The de Knegt 2016 paper is the closest local precedent (same Copenhagen group, 320-slice CT, includes an
  asymptomatic stratum) and names plaque location as a determinant of reader agreement.

### Gaps
- No study found that reports reader agreement on *segment assignment* of a given lesion (e.g. "% of
  lesions placed in the same SCCT segment by two readers"), nor adjacent-segment disagreement rates.
- SCOT-HEART, CONFIRM, PROMISE core-lab segment-level reproducibility figures were not retrieved; they may
  exist in supplements. I cannot give numbers.
- Segment-level kappa in de Knegt 2016 not confirmed (full text not accessed).
- SIS interobserver reproducibility not found.

## Q2. Automated vs reader reads at segment level; handling of lesions near/spanning boundaries

### Takeaway
Commercial AI plaque tools (Cleerly CLARIFY, HeartFlow) report agreement per patient and per vessel, not per
lesion-in-segment; no tolerance-zone or adjacent-segment-credit rule was found in their published
validations. Automated segment *labelling* papers (often by the Leiden/LKEB group that built Medis QAngio
CT) evaluate labels against experts at segment or point level and show clear accuracy drops when the
centerline is automatic and for distal/side-branch segments; expert-vs-expert labelling itself is
imperfect, especially in left-dominant trees.

### Cited Findings
- CLARIFY (Choi AD et al., J Cardiovasc Comput Tomogr 2021;15(6):470–476, DOI 10.1016/j.jcct.2021.05.004):
  232 patients; AI-QCT vs consensus of level-3 readers; per-vessel and per-patient comparison; agreement
  within one CAD-RADS category in 228/232 patients (98.3%) and 923/924 vessels (99.9%); Bland–Altman mean
  difference in maximal stenosis −0.8% per vessel. Per-segment lesion matching not reported in the abstract.
  Industry-funded/industry-authored. — [PubMed 34127407](https://pubmed.ncbi.nlm.nih.gov/34127407/)
- A single-centre AI-QCT vs reader study (Medscape summary) notes segment involvement and stenosis scores
  were not available; comparison was per vessel. —
  [Medscape](https://www.medscape.com/viewarticle/ai-outperforms-human-readers-coronary-ct-angiography-2025a10001gn)
- Deep-learning plaque segmentation papers report per-patient or per-vessel detection (e.g. vessel-level
  sensitivity 94.7%, specificity 84.9%; small non-calcified plaque hardest, false positives from motion/step
  artefacts), not per-segment lesion matching. — [PMC12931776](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12931776/);
  PlaqueViT external test of only 28 patients, per-patient sensitivity 0.88, specificity 0.76 —
  [PMC12226657](https://pmc.ncbi.nlm.nih.gov/articles/PMC12226657/)
- Automated SCCT labelling (BMC Med Inform Decis Mak 2023, DOI 10.1186/s12911-023-02332-y): 16 segments
  identified per case from the centerline, reviewed by experts against SCCT standards; accuracy 94.0% vs
  86.5% for a comparison method; authors note centerline extraction quality strongly affects labelling. —
  [Springer](https://link.springer.com/article/10.1186/s12911-023-02332-y)
- Cao Q, Broersen A, ... Reiber JHC, Dijkstra J (Leiden/LKEB, the Medis QAngio CT group), "Automatic
  identification of coronary tree anatomy in CCTA", Int J Cardiovasc Imaging 2017: automated labels agreed
  with experts on 89.2% of segments in right-dominant and 83.6% in left-dominant trees; **expert-vs-expert
  agreement was 97.6% (RD) and 87.6% (LD)**. (Snippet; DOI 10.1007/s10554-017-1169-0 from memory, verify.) —
  [PMC5677991](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5677991/)
- Yang G et al. (same group), automatic coronary tree labelling: 95% (right) / 93% (left) correct on
  hand-annotated centerlines, falling to 87% / 86% on automatically extracted centerlines; most errors from
  false-positive branches receiving location-dependent labels. —
  [ResearchGate](https://www.researchgate.net/publication/254019616_Automatic_coronary_artery_tree_labeling_in_coronary_computed_tomographic_angiography_datasets)
- Review-style summary: 87–100% labelling accuracy for RCA, LAD, LM; weaker for smaller branches. —
  [BMC 2023 (PMC10626726)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10626726/)
- Graph-based labelling: weighted F1 0.805 over 13 classes, 141 scans (ISBI 2023, QUT) —
  [QUT eprints](https://eprints.qut.edu.au/243806/1/146798438.pdf); graph attention network F1 92.4% on 71
  scans, combined extraction+labelling F1 ~0.74 (van Velzen/Hampe/Wolterink et al.) —
  [UvA DARE](https://www.dare.uva.nl/id/16ff5208-5d6a-4fc0-a489-12bcb03170b6); CPR-GCN, CVPR 2020 —
  [CVF](https://openaccess.thecvf.com/content_CVPR_2020/papers/Yang_CPR-GCN_Conditional_Partial-Residual_Graph_Convolutional_Network_in_Automated_Anatomical_Labeling_CVPR_2020_paper.pdf)

### Inferences
- The Cao 2017 expert-vs-expert figures (97.6% RD, 87.6% LD) are the most directly usable benchmark for
  "how often should two segment divisions agree": even experts disagree on ~2–12% of segment labels, more in
  left-dominant anatomy. An excess miss rate of the tracer division over the Medis baseline within a few
  percentage points would be within expert-level label disagreement (inference).
- Labelling accuracy falls ~7–8 points when centerlines are automatic rather than manual (Yang). This
  supports the thesis's design of comparing tracer vs Medis centerline under the same plaque contours, since
  centerline quality and division rule both contribute.
- None of the AI-plaque validations offers a boundary tolerance or adjacent-segment credit rule to copy; the
  thesis would need to define its own (e.g. report miss rate with and without a ±N mm tolerance at each
  boundary, or count contours that straddle a boundary as hits for either segment). This is a design choice
  without a direct precedent found.
- Segment-labelling papers evaluate labels (which segment a centerline point belongs to), not plaque
  location; the thesis's plaque-located check evaluates the division only where it matters for the outcome,
  which is a reasonable and arguably more outcome-relevant variant, but it is sampled only where plaque is
  (plaque-at-baseline participants, a different population from the plaque-free cohort).

### Gaps
- No published segment-level lesion matching of AI tools (Cleerly, HeartFlow, Elucid) vs readers was found;
  CLARIFY full text was not accessed to check for per-segment tables.
- Per-segment (proximal/mid/distal) labelling accuracy breakdowns were not retrieved from full texts.
- No precedent found for counting a segment "missed" when a graded segment does not contain the reader's
  contour.

## Q3. CCTA vs invasive angiography/IVUS: how segments/lesions were co-registered

### Takeaway
CT–IVUS/ICA comparisons co-register by anatomical landmarks: ostium, side-branch origins, calcifications,
and distance from the ostium; analyses are then restricted to the stretch between the most proximal and
most distal shared landmark. Bifurcation work uses fixed windows (e.g. 5 mm around the carina). Segment-level
CT-vs-ICA accuracy studies simply apply the same segment model in both modalities; mis-assignment to an
adjacent segment is not quantified.

### Cited Findings
- INVICTUS (Cleerly AI-QCT vs IVUS, 108 vessels / 85 patients, Eur Radiol 2026, DOI
  10.1007/s00330-026-12412-y): an IVUS core lab mapped landmarks (ostium, side branches, calcifications,
  stenoses) on the IVUS pullback and angiogram, then matched them on CCTA; the distance between the most
  proximal and most distal co-registered landmarks defined the analysis segment, irrespective of plaque
  burden. Whole-segment correlations: EEM volume r = 0.899, lumen r = 0.943, plaque volume r = 0.833. —
  [Springer](https://link.springer.com/article/10.1007/s00330-026-12412-y)
- VH-IVUS vs CT high-risk plaque (J Cardiovasc Comput Tomogr 2017): plaque locations co-registered by
  triangulation using reference measurements from coronary ostia and side branches. —
  [JCCT](https://www.journalofcardiovascularct.com/article/S1934-5925(17)30197-1/fulltext)
- Standardized CT plaque quantification vs IVUS (head-to-head): plaque limits matched using the distance
  from the aorto-coronary ostium, target lesions, side branches or calcifications. —
  [PMC6824266](https://pmc.ncbi.nlm.nih.gov/articles/PMC6824266/)
- 3D CT reconstruction vs IVUS registered at side branches: volume mismatch increased with distance from the
  registration landmark (snippet truncated). —
  [ResearchGate](https://www.researchgate.net/publication/291385105_Three-dimensional_reconstruction_of_coronary_arteries_and_plaque_morphology_using_CT_angiography_-_comparison_and_registration_with_IVUS)
- 3D angiography–IVUS co-registration using a side branch as common landmark: mean mismatch −0.07 ± 0.51 mm
  at 44 bifurcations (abstract, small sample). — [JACC abstract](https://www.jacc.org/doi/10.1016/S0735-1097(14)61793-9)
- CT-PRECISION: bifurcation analysis within 5 mm proximal/distal of the carina for the main vessel and 5 mm
  from the side-branch ostium. — [PMC7806530](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7806530/)
- Fusion CT–IVUS (Medis/LKEB-associated authors, 2012): 3D registration of a full IVUS run to the CT volume
  using anatomical landmarks; QCT vs IVUS MLA r = 0.75 (n = 146). Product name not confirmed in snippet. —
  [Leiden repository](https://scholarlypublications.universiteitleiden.nl/handle/1887/120260)
- Segment-level CT vs ICA accuracy studies apply the same segment model to both modalities, classify each
  segment by its worst lesion; e.g. 128-slice CT segment-based sensitivity 87%, specificity 97%. —
  [PubMed 19099978](https://pubmed.ncbi.nlm.nih.gov/19099978); 64-slice study —
  [JACC 2005, DOI 10.1016/j.jacc.2005.05.056](https://www.jacc.org/doi/10.1016/j.jacc.2005.05.056)

### Inferences
- Side-branch origins are the standard anchors for matching location across modalities, and registration
  error grows with distance from the anchor. This supports the thesis rule (side-branch origins where
  available) and predicts that the fixed-fraction boundaries (where no branch exists) will be the least
  reliable, so the miss rate should be reported separately for landmark-based vs fraction-based boundaries.
- Restricting analysis to the stretch between shared landmarks (INVICTUS) parallels the thesis's cutting of
  the tracer centerline at the first/last Medis contour.

### Gaps
- No CT-vs-ICA study found that reports how often a lesion was assigned to an adjacent segment across
  modalities; segment misregistration is acknowledged as a limitation in this literature but not quantified
  in what I retrieved.

## Q4. Serial CCTA: matching segments between baseline and follow-up

### Takeaway
PARADIGM (the main serial-CCTA registry) matched baseline and follow-up segments and lesions using fiduciary
landmarks: branch points/side branches and distance from the ostium, on a modified 17-segment AHA model
(segments ≥2 mm). Lehman 2009 used co-registration over the proximal 40 mm in 1-mm cross-sections. These are
precedents for landmark-anchored segment matching, not for validating a segment division.

### Cited Findings
- PARADIGM cluster analysis (Sci Rep 2021, DOI 10.1038/s41598-021-96616-w): modified 17-segment AHA model,
  segments ≥2 mm diameter scored; baseline and follow-up segments paired using branch points as landmarks;
  2,252 patients with serial CCTA ≥2 years apart, 13 sites, 7 countries, 2003–2015. Note: a clinically
  referred, symptomatic/suspected-CAD registry, not a population cohort. —
  [Nature](https://www.nature.com/articles/s41598-021-96616-w); [PMC8385056](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8385056/)
- PARADIGM statin paper: Lee SE et al. Effects of statins on coronary atherosclerotic plaques: the PARADIGM
  study. JACC Cardiovasc Imaging 2018, DOI 10.1016/j.jcmg.2018.04.015 — segments and lesions co-registered
  using ostial distance and branch vessels as landmarks (Online Figures 4–5). —
  [JACC](https://www.jacc.org/doi/10.1016/j.jcmg.2018.04.015)
- PARADIGM high-risk plaque progression: JACC Cardiovasc Imaging 2020, DOI 10.1016/j.jcmg.2019.09.011 —
  lesions co-registered by fiduciary landmarks incl. distance from ostium and branch vessels. —
  [JACC](https://www.jacc.org/doi/10.1016/j.jcmg.2019.09.011)
- PARADIGM sex differences: JACC Cardiovasc Imaging 2020, DOI 10.1016/j.jcmg.2020.06.034 — same
  fiduciary-landmark co-registration between CTA-1 and CTA-2. — [JACC](https://www.jacc.org/doi/10.1016/j.jcmg.2020.06.034)
- PARADIGM per-artery variation (Eur Heart J Cardiovasc Imaging 2022;23(11):1482): side branches as
  landmarks. — [OUP](https://academic.oup.com/ehjcimaging/article/23/11/1482/6574367)
- Lehman SJ et al., Assessment of coronary plaque progression in CCTA using a semiquantitative score, JACC
  Cardiovasc Imaging 2009 (PMID 19909929; DOI 10.1016/j.jcmg.2009.07.007 from memory, verify): 69 ACS
  patients, 64-slice CT at baseline and 2 years; datasets co-registered and plaque scored in 1-mm
  cross-sections of the proximal 40 mm of each major artery; semiquantitative score vs volume progression
  r = 0.75. Small, older technology. —
  [Flinders record](https://researchnow.flinders.edu.au/en/publications/assessment-of-coronary-plaque-progression-in-coronary-ct-angiogra/)
- Serial CCTA progression may be underestimated by CAD-RADS category change (motivating segment-level
  scoring). — [PMC9584618](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9584618/)

### Inferences
- PARADIGM's practice (a reader matching segments at baseline and follow-up by side-branch landmarks) is
  exactly what the CGPS reader is assumed to have done for per-segment outcome grading. The thesis division
  uses the same anchors, which is the best available argument that tracer segments approximate reader
  segments; the planned Medis-contour check is the way to quantify it.
- No serial-CCTA paper found reports the reproducibility of the *segment matching* itself (i.e. whether two
  readers pair the same lesion to the same segment at both time points).

### Gaps
- PARADIGM reproducibility figures (inter/intraobserver for plaque volume, segment matching) not retrieved
  (full texts blocked). The PARADIGM design paper
  ([eScholarship PDF](https://escholarship.org/content/qt2tv6w9pf/qt2tv6w9pf_noSplash_8f25cfec44c3ea98de7b7845fde4f408.pdf?t=oikoee))
  likely contains them; not read.
- No population-based serial CCTA study (like CGPS) was found describing segment matching.

## Cross-cutting benchmarks for the planned check (summary for the writer)
- Expert vs expert segment labelling: 97.6% (right-dominant) / 87.6% (left-dominant) agreement (Cao 2017,
  Leiden/LKEB, small sample, not verified in full text).
- Automated vs expert labelling: ~84–94%, with ~7–8 point drop on automatic vs manual centerlines.
- Segment-level plaque presence between readers: kappa ~0.73–0.88; non-calcified plaque lower.
- Registration error grows with distance from side-branch landmarks; fixed-fraction boundaries likely the
  weakest point.
- No published precedent for the exact "reader contour in graded segment" miss-rate design; the Medis
  reader-cut baseline is the thesis's own control and is methodologically appropriate given the absence of
  ground truth. Caveat: Medis contours exist only for diseased segments in plaque-at-baseline participants
  (outside the plaque-free cohort), and those plaques are larger/more visible than incident minimal plaque.
