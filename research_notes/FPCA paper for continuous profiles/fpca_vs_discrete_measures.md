# FPCA (or waveform PCA) of a continuous curve versus discrete/scalar summaries

Searched 2026-11-07 (WebSearch, Europe PMC REST API, PMC full text, Crossref). All DOIs below were verified on api.crossref.org unless marked. Citation counts: Crossref `is-referenced-by-count` (CR) and Europe PMC `citedByCount` (EPMC) on 2026-11-07.

## Which peer-reviewed papers explicitly compared FPCA / waveform PCA with discrete measures and found the curve analysis captured something the discrete measures missed?

### Takeaway
The cleanest explicit head-to-head that names FPCA is Richter et al. 2014 (J Biomech): FPCA explained 78% of jump height versus 21% for discrete points, but it is a performance outcome in healthy jumpers, not a clinical group. The cleanest clinical case is the Hatfield/Hubley-Kozey knee OA work: a PCA shape feature of the knee adduction moment (the mid-stance unloading pattern) was not captured by peak or impulse (Clin Biomech 2015) and, measured at baseline, was part of a model associated with later knee replacement (Arthritis Care Res 2015). That work uses PCA of discretised, time-normalised waveforms, not smoothed FPCA.

### Cited Findings

**Richter, O'Connor, Marshall, Moran 2014. "Comparison of discrete-point vs. dimensionality-reduction techniques for describing performance-related aspects of maximal vertical jumping." J Biomech 47(12):3012–3017. DOI 10.1016/j.jbiomech.2014.07.001 (CR 61, EPMC 41). Abstract only.**
- Design: vertical ground reaction force curves, countermovement jump propulsion phase; discrete point analysis (DPA), fPCA and analysis of characterizing phases (ACP) each fed into stepwise regression of jump height. n not in abstract (gap). — [Europe PMC abstract](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%2210.1016/j.jbiomech.2014.07.001%22&format=json&resultType=core)
- Quote: "Findings indicated that the order of effectiveness (high to low) across the examined techniques was: ACP (99%), fPCA (78%) and DPA (21%)." — same source
- Quote: "DPA was outperformed by fPCA and ACP because it can inadvertently compare unrelated features, does not analyze the whole data set and cannot examine important features that occur solely as a phase." — same source
- Caveat: ACP is the authors' own method and beat fPCA; outcome is performance in healthy athletes, not disease. — same source

**Hatfield, Stanish, Hubley-Kozey 2015. "Relationship between knee adduction moment patterns extracted using principal component analysis and discrete measures with different amplitude normalizations: Implications for knee osteoarthritis progression studies." Clin Biomech 30(10). DOI 10.1016/j.clinbiomech.2015.08.011 (CR 12). Abstract only.**
- Design: 54 knee OA patients (same cohort as the TKA-progression paper below); PCA patterns of the knee adduction moment (KAM) correlated with KAM peak and impulse; progressors to surgery vs non-progressors compared. — [Europe PMC abstract](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%2210.1016/j.clinbiomech.2015.08.011%22&format=json&resultType=core)
- Quote (background): "Knee adduction moment discrete features (peaks and impulses) are commonly reported in knee osteoarthritis gait studies, but they do not necessarily capture loading patterns." — same source
- Findings: overall-magnitude PC correlated with peak (r = 0.88–0.90) and impulse (r = 0.93); the early-vs-mid/late-stance difference PC correlated with peak only r = 0.27–0.40 "but explained minimal variance". — same source
- Quote (interpretation): "Findings suggest that the overall magnitude knee adduction moment principal pattern does not provide unique information from peak and impulse measures. However, low correlations and minimal variance explained between the pattern capturing ability to unload the joint during mid-stance and the two discrete measures, suggests that this pattern captured a unique waveform feature." — same source
- Note: this is an honest two-sided result: the first PC duplicates the scalar summary, only the shape PC adds information. Useful for a skeptical thesis.

**Park, Seeley, Francom, Reese, Hopkins 2017. "Functional vs. Traditional Analysis in Biomechanical Gait Data: An Alternative Statistical Approach." J Hum Kinet 60:39–49. DOI 10.1515/hukin-2017-0114 (CR 59). Full text open (PMC5765784).**
- Design: 19 healthy participants, experimentally induced knee pain+effusion vs control; peak-angle ANOVA vs functional ANOVA (FANOVA). Not FPCA. — [Europe PMC abstract](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE:%22Functional%20vs.%20Traditional%20Analysis%20in%20Biomechanical%20Gait%20Data%22&format=json&resultType=core)
- Quote: "The results of ANOVAs detected a condition × time interaction for the peak ankle (F1,18 = 8.56, p = 0.01) and hip joint angle (F1,18 = 5.77, p = 0.03), but did not for the knee joint angle (F1,18 = 0.36, p = 0.56). The functional data analysis, however, found several differences at initial contact (ankle and knee joint), in the mid-stance (each joint) and at toe off (ankle)." — same source

**Deluzio & Astephen 2007. "Biomechanical features of gait waveform data associated with knee osteoarthritis: an application of principal component analysis." Gait Posture 25(1):86–93. DOI 10.1016/j.gaitpost.2006.01.007 (CR 369, EPMC 262). Abstract only.**
- Design: 50 end-stage knee OA vs 63 age-matched controls; PCA of knee flexion angle, flexion moment and adduction moment waveforms, then hypothesis tests and discriminant analysis. — [Europe PMC abstract](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%2210.1016/j.gaitpost.2006.01.007%22&format=json&resultType=core)
- Quote: "The two groups were separated with a misclassification rate (estimated by cross-validation) of 8%. The discriminatory features of the gait waveforms were, in order of their discriminatory ability: the amplitude of the flexion moment, the range of motion of the flexion angle, the magnitude of the flexion moment during early stance, and the magnitude of the adduction moment during stance." — same source
- The abstract does not compare with discrete measures; it is the most cited waveform-PCA clinical paper, not a head-to-head. A 2005 Clin Biomech paper by Astephen & Deluzio combined nine waveform and eight discrete measures (<6% misclassification) per a search summary only, not verified. — [search snippet, ISC listing](https://manuscript.isc.ac/Inventory/10/488874.htm)

**Landry, McKean, Hubley-Kozey, Stanish, Deluzio 2007. "Knee biomechanics of moderate OA patients measured during gait at a self-selected and fast walking speed." J Biomech 40(8). DOI 10.1016/j.jbiomech.2006.08.010 (CR 202). Abstract only.**
- 41 moderate OA vs 43 controls, waveform PCA. Quote: "Differences in the magnitude and shape of the knee joint moment waveforms were found between the two groups. The OA group had larger adduction moment magnitudes during stance and this higher magnitude was sustained for a longer portion of the gait cycle." No explicit discrete comparison in the abstract. — [Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE:%22Knee%20biomechanics%20of%20moderate%20OA%20patients%22&format=json&resultType=core)

**Yoshida, Commandeur, Hundza, Klimstra 2022. "Detecting differences in gait initiation between older adult fallers and non-fallers through multivariate functional principal component analysis." J Biomech 144:111342. DOI 10.1016/j.jbiomech.2022.111342 (CR 15). Abstract only.**
- True (multivariate) FPCA, 56 community-dwelling older adults, fallers vs non-fallers (cross-sectional). Abstract frames FPCA as possibly highlighting "group differences not detectable using discrete comparisons alone" and concludes mFPCA "supports and enhances previous findings"; no head-to-head numbers in the abstract. — [Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%2210.1016/j.jbiomech.2022.111342%22&format=json&resultType=core)

**Other leads (not verified in depth)**
- Aragón-Basanta et al. 2025 Sci Rep, "Functional data analysis of ground reaction forces combined with clinical measures for early knee osteoarthritis detection", DOI 10.1038/s41598-025-24411-y (CR 3, open access PMC12627083). Not read. — [Europe PMC listing](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22functional%20principal%20component%22%20AND%20(discrete%20OR%20%22peak%20values%22)%20AND%20(gait%20OR%20clinical)&format=json&pageSize=25&resultType=lite)
- Brandon et al. 2013 J Electromyogr Kinesiol, DOI 10.1016/j.jelekin.2013.09.010: methods on interpreting PCs (single component reconstruction), not a comparison. — [Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE:%22Interpreting%20principal%20components%20in%20biomechanics%22&format=json&resultType=core)
- Ullah & Finch 2013 BMC Med Res Methodol 13:43, DOI 10.1186/1471-2288-13-43 (CR 263) verified, the review already cited in the thesis sentence.

### Inferences
- In this literature the "FPCA beats discrete" claim is mostly asserted in introductions; explicit head-to-heads with numbers are few (Richter 2014; Hatfield Clin Biomech 2015; Park 2017 with FANOVA).
- The Hatfield Clin Biomech result fits the coronary argument well: a magnitude PC is redundant with the scalar summary (as mean curvature would be), and the extra information sits in shape PCs. That is also the honest framing (FPCA does not automatically add information).

### Gaps
- Full texts of Richter 2014, Hatfield Clin Biomech 2015 and Deluzio 2007 were not accessed; sample size of Richter 2014 unknown.
- Donoghue et al. 2008 MSSE DOI could not be verified (guessed DOI 10.1249/MSS.0b013e31815ef91c not found on Crossref).
- Warmenhoven, Harrison et al. 2014 "comparison of discrete and functional analyses" not located in this search.
- No peer-reviewed FPCA vs discrete comparison for spinal curvature, voice, pupil, heart rate or growth curves was found within the search budget; the only vascular-geometry FPCA hits remain AneuRisk/Sangalli-type work.

## Which are prospective (curve measured before outcome)?

### Takeaway
Hatfield, Stanish & Hubley-Kozey 2015 (Arthritis Care Res) is the one prospective-type study found: baseline gait waveform PCA in moderate knee OA, followed 4–8 years for total knee arthroplasty. It is exploratory, small (n = 54) and uses waveform PCA, and the discrete peak/impulse comparison is in the companion Clin Biomech paper, not this one.

### Cited Findings
- Hatfield GL, Stanish WD, Hubley-Kozey CL. "Three-Dimensional Biomechanical Gait Characteristics at Baseline Are Associated With Progression to Total Knee Arthroplasty." Arthritis Care Res 2015;67(7):1004–1014. DOI 10.1002/acr.22564 (CR 84). Full text open, PMC4654242. — [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC4654242/)
- Design: baseline gait 2003–2008 in 80 moderate medial knee OA patients; 54 analysed; 26 had TKA (mean 4 ± 3 y after baseline), 28 did not (mean 8 ± 2 y to follow-up radiograph). PCA of time-normalised ensemble-averaged waveforms (PCA built on n = 149 incl. 64 controls). — [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC4654242/)
- Quote (abstract): "Baseline demographic, symptomatic, and radiographic variables were similar, but 7 gait variables differed (P < 0.05) between groups." — same source
- Quote (abstract): "A multivariate model including overall knee adduction moment magnitude, knee flexion/extension moment difference, and stance–dorsiflexion moment had a 74% correct classification rate, with no overtraining based on cross-validation. A 1-unit increase in model score increased by 6-fold the odds of progression to TKA." Results text gives OR 5.7; sensitivity 84.6%, specificity 71.4%. — same source
- Quote (conclusion): "novel findings include altered sagittal plane moment patterns indicative of reduced ability to unload the joint during midstance ... adding baseline demographic and clinical factors did not improve the model." — same source
- This paper does not itself test discrete peak KAM or impulse against the PCs. — same source
- Cohort numbers vary across sources (thesis 54/26; conference abstract 50/25). — [Dalhousie repository](https://dalspace.library.dal.ca/items/0e88d059-60f6-4970-8845-d49cdfc51fd5/full)

### Inferences
- Combined with the companion Clin Biomech 2015 paper (same 54 patients), one can say: a PCA shape feature not captured by peak or impulse was, at baseline, part of a model associated with later knee replacement. The two papers should be cited together if that claim is made, and "associated with", not "predicted", is the safe verb (exploratory, small, cross-validated only internally).

### Gaps
- No prospective study with true smoothed FPCA versus discrete measures and a clinical outcome was found.

## Ranking for a one-sentence citation in the coronary-geometry review

### Takeaway
1) Hatfield et al. 2015 Clin Biomech + Arthritis Care Res pair (clinical, baseline curve, later outcome, explicit discrete comparison; but waveform PCA, small). 2) Richter et al. 2014 J Biomech (explicit three-way head-to-head naming fPCA; non-clinical). 3) Deluzio & Astephen 2007 Gait Posture (most cited clinical waveform PCA, 50 vs 63, 8% CV misclassification; no discrete comparison in abstract). Park et al. 2017 is a good head-to-head but uses FANOVA, not FPCA.

### Cited Findings
- Hatfield pair: [Arthritis Care Res, PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC4654242/); [Clin Biomech abstract](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%2210.1016/j.clinbiomech.2015.08.011%22&format=json&resultType=core)
- Richter 2014: [abstract](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%2210.1016/j.jbiomech.2014.07.001%22&format=json&resultType=core)
- Deluzio 2007: [abstract](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%2210.1016/j.gaitpost.2006.01.007%22&format=json&resultType=core)

### Inferences
- Suggested sentence (to adapt to thesis style): "In knee osteoarthritis, principal component analysis of the knee adduction moment curve isolated a mid-stance unloading pattern that peak and impulse did not capture (Hatfield et al. 2015a), and this pattern, measured at baseline, was part of a model associated with later knee replacement (Hatfield et al. 2015b)." If one paper only: Hatfield 2015 Arthritis Care Res.
- Wording must say PCA of waveforms (the basic form of FPCA, per Warmenhoven 2021), not FPCA.

### Gaps
- Full text of the Clin Biomech paper not read; the claim rests on its abstract.
