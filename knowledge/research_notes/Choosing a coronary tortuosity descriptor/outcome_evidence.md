# Outcome and clinical evidence for coronary tortuosity metrics

Evidence-quality tags: [FT] = full text read via fetch summary; [ABS] = abstract or search snippet only; [EDIT] = editorial. Fetch summaries were produced by a small model, so numbers should be spot-checked before thesis citation. Not covered (searched, not retrieved): Kashyap 2022 full text (paywalled redirect), Sharfo 2024 full text (403), Circulation CArTI abstract page (403; only snippets), ICONIC JAMA Cardiol numbers.

## Which metrics have been tied to outcomes, and with what effect sizes?

### Takeaway
Nearly all outcome evidence is from invasive angiography with categorical, bend-count definitions (>=3 bends of >=45 deg; Eleid score). Consistent findings: tortuosity goes with female sex, age, hypertension, and (inversely) with obstructive CAD; strong association with SCAD; ischemia without obstructive CAD. Continuous centerline metrics on CCTA have thin outcome evidence: one abstract-level MACE model (CArTI), one hypertension association (arc/chord LAD), and a null result for dynamic geometry vs CAD. Association with MACE was null in the one angiography cohort with follow-up.

### Cited Findings
- Bend-count definition, n=1010 angiography, chest pain: CT = >=3 bends (>=45 deg change of direction) in main trunk in systole and diastole; prevalence 39.1%; hypertension OR 1.533, coronary atherosclerosis OR 0.755, female OR 2.603; MACE (death, MI, revascularisation) not different over 2-4 y follow-up. [FT] — [Li 2011, PLoS One / PMC3164184](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3164184/)
- Significant coronary tortuosity (SCT: >=3 consecutive curvatures of 90-180 deg or >=2 of >=180 deg), n=737 angiography, Iran: prevalence 29.2%; more female (64.7% vs 34.1%) and older (62.9 vs 57.8 y); lower stenosis prevalence (LAD 34.5% vs 46.1%, p=0.019) and lower Gensini in all three arteries; higher TIMI frame count (LAD 15.7 vs 11.9, p<0.001), i.e. slower flow; findings held after age and sex adjustment. [FT] — [PMC6335987](https://pmc.ncbi.nlm.nih.gov/articles/PMC6335987/)
- Severe tortuosity vs non-obstructive CAD, n=131 (77 non-obstructive, 54 obstructive), same >=3 bends/>=45 deg definition: tortuous arteries in 50.6% of non-obstructive vs 14.8% of obstructive; OR 7.96 (95% CI 1.79-35.4) for tortuosity, sex OR 17.5, model AUC 0.932 (for identifying non-obstructive disease; small n, wide CIs, likely overfit). [FT] — [PMC10534717](https://pmc.ncbi.nlm.nih.gov/articles/PMC10534717/)
- Ischemia without obstructive CAD (Estrada et al., n=57 angina with non-obstructive CAD): number of bend angles in an epicardial artery in systole was the angiographic variable most associated with ischemia on stress perfusion imaging (p=0.021); ischemia in territories with tortuosity 67% vs 28% (p<0.0001, from editorial); LCx tortuosity most tied to ischemia. [ABS + EDIT] — [ABC Cardiol editorial PMC9814803](https://pmc.ncbi.nlm.nih.gov/articles/PMC9814803/); [PubMed 36541983](https://pubmed.ncbi.nlm.nih.gov/36541983/)
- Tortuosity index (arc/chord on angiogram, ImageJ, diastolic frame) vs angle method, n=160 (85 non-obstructive, 75 obstructive): TI highest in lateral ischemia for LCx tortuosity and anterior ischemia for LAD (both p<0.001); RCA no association (p=0.122); angle method only LCx-lateral (OR 4.9, p=0.046). Authors judged TI more reliable. Small, single centre. [FT] — [Diagnostics 2024, PMC10795752](https://pmc.ncbi.nlm.nih.gov/articles/PMC10795752/)
- SCAD (Eleid 2014, n=246 SCAD vs 313 controls, angiography): tortuosity 78% vs 17% (p<0.0001); score 4.41 vs 2.33; severe tortuosity (>=2 consecutive curvatures >=180 deg) HR 3.29 (95% CI 0.99-8.29, p=0.05) for recurrent SCAD; 80% of recurrences within tortuous segments. [ABS via search snippet] — [Circ Cardiovasc Interv 2014](https://www.ahajournals.org/doi/10.1161/circinterventions.114.001676) (page 403; figures from search summary of [PubMed 25138034](https://pubmed.ncbi.nlm.nih.gov/25138034/))
- SCAD follow-up (n=116, 95.7% women): Eleid score 0-3 per artery (1: >=3 curvatures 45-90; 2: 90-180; 3: >=2 of >=180); 82.8% tortuous; FMD 59.4% vs 25%; each decade of age adds 0.89 score units; 3-y recurrence 9.4%; no echo/GLS difference. [FT] — [PMC11605948](https://pmc.ncbi.nlm.nih.gov/articles/PMC11605948/)
- Continuous metric, CCTA, LAD arc/chord: CATCH-trial sub-study, n=194; tortuosity (vessel length / straight-line distance) associated with hypertension (p<0.001), female sex (p=0.01), age (p=0.045) after adjustment; not independently related to physical performance. Effect sizes not obtained. [ABS via search snippet] — [Sharfo 2024, Clin Physiol Funct Imaging](https://onlinelibrary.wiley.com/doi/abs/10.1111/cpf.12900)
- Large angiography cohort, sum of absolute turning angles / pi on RCA centerline, n=22,334 patients (38,691 RCA angiograms, MGH registry): median 0.107 (range 0.007-0.289); CAD OR 1.05 per SD, severe CAD OR 1.09 per SD, Gensini beta 0.05/SD, female beta 0.17/SD, hypertension beta 0.06/SD (p=0.002), diabetes beta -0.11/SD; local-profile transformer AUC 0.67 vs global score 0.60 for CAD. Note the positive CAD association here contrasts with the negative association in bend-count studies. [FT] — [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- CCTA MACE model: CArTI (AI-derived Coronary Artery Tortuosity Index), 992 patients, median follow-up 4.3 y, MACE via ICD/CPT codes; high- vs low-risk HR 2.69; curvature and tortuosity features among the top positive predictors. Feature definitions, CI, and adjustment set not retrieved. It is a multi-feature model, so no single-metric effect size. [ABS via snippet] — [Circulation 2025 abstract 4365988](https://www.ahajournals.org/doi/10.1161/circ.152.suppl_3.4365988)
- ICONIC (CCTA nested case-control, future ACS culprit lesions): more proximal location (median 35.1 vs 44.5 mm from ostium), bifurcation, and increased vessel tortuosity gave incremental value over stenosis and plaque features for identifying precursor culprit lesions. Tortuosity definition and effect size not retrieved. [ABS via snippet] — [ACC journal scan](https://www.acc.org/Latest-in-Cardiology/Journal-Scans/2022/02/04/18/53/Association-of-Plaque-Location); [JAMA Cardiol](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
- Narrative review notes tortuosity is associated with aging, hypertension, atherosclerosis, and that flow alteration may cause ischemia via reduced distal perfusion pressure. [ABS] — [PubMed 31211725](https://pubmed.ncbi.nlm.nih.gov/31211725/)

### Inferences
- Bend counting on angiography (>=45 deg, >=3 bends) is the metric with the most outcome literature, but it is a categorical visual definition; no single CCTA continuous metric has replicated outcome data.
- The sign of the CAD association depends on definition and cohort: negative for bend-count severe tortuosity in chest-pain angiography cohorts (OR 0.755; SCT lower Gensini); weakly positive for the turning-angle sum in a hospital registry with high CAD prevalence (OR 1.05/SD). Descriptor validation against CAD severity alone is therefore uninformative about sign.
- Most robust, definition-independent associations: female sex, age, hypertension. These are the safest targets for sanity-checking a descriptor on ImageCAS metadata or the Danish cohort.
- Strongest disease-specific phenotype: SCAD and INOCA/non-obstructive ischemia, neither obtainable from ImageCAS.

### Gaps
- No CCTA study found with continuous centerline tortuosity and FFR or CT-FFR as endpoint. Search surfaced only CT-FFR/deep-learning papers without tortuosity effect sizes.
- No coronary ectasia tortuosity study retrieved with usable numbers; one ectasia nomogram appeared in search but was not opened.
- Sharfo effect sizes, CArTI feature definitions and CI, ICONIC tortuosity effect size not obtained (403/paywall).
- Dominance association: only a mention that left dominance was a predictor in [PMC10534717](https://pmc.ncbi.nlm.nih.gov/articles/PMC10534717/) (p=0.008); no dedicated study.

## Segment, vessel, or tree scale

### Takeaway
Nearly all studies use per-vessel (per-artery) or patient-level "any artery" definitions. Segment-specific signals exist for LCx and LAD (ischemia territory match) but not RCA; no study evaluated a whole-tree descriptor for outcomes.

### Cited Findings
- Patient-level "at least one artery" (Li 2011) and per-artery analysis (Iran SCT study, LAD/LCx/RCA separately) — [PMC3164184](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3164184/); [PMC6335987](https://pmc.ncbi.nlm.nih.gov/articles/PMC6335987/)
- TI matched ischemia territory for LCx (lateral) and LAD (anterior) but not RCA; LCx tortuosity most frequent in non-obstructive group (35.1% vs 9.3%) — [PMC10795752](https://pmc.ncbi.nlm.nih.gov/articles/PMC10795752/); [PMC10534717](https://pmc.ncbi.nlm.nih.gov/articles/PMC10534717/)
- Main RCA only (to PDA), one score per vessel; left tree excluded for complexity; local turning-angle profile beat global score (AUC 0.67 vs 0.60) — [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- LAD only for arc/chord vs hypertension — [Sharfo 2024](https://onlinelibrary.wiley.com/doi/abs/10.1111/cpf.12900)
- CCTA dynamic geometry study (n=71, 137 arteries, 456 segments): curvature, arc/chord tortuosity, inflection points at artery and segment level; no relation to CAD presence, stenosis grade or plaque type. [FT] — [PMC7165136](https://pmc.ncbi.nlm.nih.gov/articles/PMC7165136/)
- Kashyap 2022: n=127 CTCA without CAD, left main bifurcation and branches, metrics tortuosity index, mean absolute curvature, RMS curvature, mean squared-derivative curvature, related to CFD wall shear stress (a surrogate, not a clinical outcome). [ABS via snippet] — [Sci Rep 2022](https://www.nature.com/articles/s41598-022-04796-w)

### Inferences
- Vessel-level (LAD, LCx, RCA separately) is the scale with prior art; RCA behaves differently and is the vessel with the most anatomical variability (dominance, PDA definition), so a per-vessel descriptor needs a well-defined endpoint for RCA.
- Local profile beat global average in the only test (0.67 vs 0.60), suggesting spatially-resolved features are worth keeping, though absolute AUC is low.

### Gaps
- No tree-level outcome study. No proximal/mid/distal segment-specific outcome comparison found.

## Normalisation

### Takeaway
Studies used dimensionless ratios (arc/chord, angle sums normalised by pi) and rarely adjusted for body size or heart size. No study tested whether normalisation changes the outcome association.

### Cited Findings
- Arc/chord is scale-free by construction — [Sharfo 2024](https://onlinelibrary.wiley.com/doi/abs/10.1111/cpf.12900); [PMC10795752](https://pmc.ncbi.nlm.nih.gov/articles/PMC10795752/)
- Turning-angle sum normalised by pi, giving 0-1 score, not by length; per-SD effect sizes reported — [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- Age and sex (both strongly tied to tortuosity) were adjusted for in the Iranian cohort and Sharfo; results held in the former — [PMC6335987](https://pmc.ncbi.nlm.nih.gov/articles/PMC6335987/)

### Inferences
- Because sex, age and hypertension all associate with tortuosity, any descriptor-outcome match in the Danish cohort must adjust for them, otherwise it may recover demographics.
- A turning-angle sum that is not divided by length scales with vessel length; whether length adds or confounds was not tested in retrieved sources.

### Gaps
- No evidence on body-surface-area, heart-volume or vessel-length normalisation and outcomes.

## Large cohorts and public data

### Takeaway
Only the MGH angiography registry (n=22,334) and CArTI (n=992 CCTA, abstract) exceed a few hundred. No retrieved study used ImageCAS.

### Cited Findings
- n=22,334 angiography — [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/); n=992 CCTA — [Circulation abstract](https://www.ahajournals.org/doi/10.1161/circ.152.suppl_3.4365988); n=1010 angiography — [PMC3164184](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3164184/); n=737 — [PMC6335987](https://pmc.ncbi.nlm.nih.gov/articles/PMC6335987/); ICONIC is a multicentre nested case-control — [ACC scan](https://www.acc.org/Latest-in-Cardiology/Journal-Scans/2022/02/04/18/53/Association-of-Plaque-Location)
- Unsupervised HMM-based tortuosity assessment on CCTA centerlines exists as a conference chapter; outcome evidence not retrieved. [ABS] — [Springer chapter](https://link.springer.com/chapter/10.1007/978-3-031-95841-0_27)

### Gaps
- No ImageCAS-based tortuosity-outcome study found (ImageCAS has no outcome labels, which limits this). Not exhaustively searched.

## Null, negative, and reproducibility results

### Takeaway
Several nulls: no MACE difference (Li 2011), no dynamic geometry vs CAD (PMC7165136), sign reversals for CAD, weak local-vs-global AUC. Reproducibility is genuinely fragile: definitions are inconsistent, readers agree only moderately, and centerline extraction in diseased vessels needs manual correction.

### Cited Findings
- No MACE difference by tortuosity over 2-4 y (n=1010) — [PMC3164184](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3164184/)
- Systolic/diastolic curvature, tortuosity, inflection change not related to CAD presence, stenosis, or plaque type; 62.3% of cases needed phase selection beyond software-optimal; semi-automatic centerline needed manual adaptation in diseased vessels (n=71) — [PMC7165136](https://pmc.ncbi.nlm.nih.gov/articles/PMC7165136/)
- Cardiologist vs algorithm on high vs non-tortuous angiograms: Cohen's kappa 0.52; 21.3% of RCA angiograms excluded for segmentation quality; RCA-only — [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- Angle-method and TI agreed for LCx and LAD but not RCA; TI preferred as angle method is visual — [PMC10795752](https://pmc.ncbi.nlm.nih.gov/articles/PMC10795752/)
- Different definitions yield opposite CAD associations (see above); the editorial calls for standardised indices and correlation with FFR/iFR — [PMC9814803](https://pmc.ncbi.nlm.nih.gov/articles/PMC9814803/)
- Intraobserver agreement for visual tortuosity in a 25-case pilot was 0.96 (kappa 0.88) [ABS, snippet]; interobserver kappa not found — [Sci Rep 2023 deep learning tortuosity detection](https://www.nature.com/articles/s41598-023-37868-6)
- Systolic vs diastolic phase alters bend count and hence classification: Estrada used systole, Li required both phases; vessel curvature was 11.1% higher in end-systole, inflection points higher (p<0.001) — [PMC7165136](https://pmc.ncbi.nlm.nih.gov/articles/PMC7165136/)

### Inferences
- The "fragile measurement" concern is supported by cardiac phase dependence, centerline-extraction dependence, and reader/algorithm kappa of ~0.5. It is not supported by a formal test-retest study of continuous CCTA curvature, which I did not find.
- Effect sizes for continuous metrics are small (OR 1.05-1.09 per SD; AUC 0.60-0.67), so expect modest signal in the Danish cohort and plan for phase and centerline noise sensitivity analyses.

### Gaps
- No formal interobserver ICC or coefficient of variation for CCTA-derived curvature or tortuosity found. Kashyap 2022 (which examined metric accuracy under computational modelling) was not read in full, so its findings on metric noise sensitivity are unverified.
