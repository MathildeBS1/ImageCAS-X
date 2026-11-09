# Fact check of sec:lit-risk (03_geometry_risk.tex), prose and tab:literature

Scope: every claim about a cited study in `Thesis_coronary/content/litterature_review/03_geometry_risk.tex`
(file state 2026-11-08) and every cell of `tab:literature`. Verdicts: **supported**, **overstated**,
**wrong**, **unverifiable**. Abstracts were read for all 13 papers through the Europe PMC REST API (the
`europepmc.org/article/MED/<pmid>` links below). Full text was read for Tommasino, Won, Hageman, Zhang,
Li, Han (JAMA page) and Chen (OUP page). PubMed and part of PMC served a bot check, so Tello Ayala and
Lee 2024 were read at abstract level only. No thesis file was edited.

Summary verdicts:

| Claim (line) | Verdict |
|---|---|
| Glagov "showed that coronary arteries were larger in proportion to the amount of plaque" (59-60) | overstated (wording; the finding itself holds) |
| Li, Zhang, Han, Tommasino, Tello Ayala "conducted in patients who already had coronary disease" (63-65) | overstated (true for Han and mostly Tommasino; Li, Zhang and Tello Ayala compared patients with and without disease) |
| Won: plaque-free PARADIGM patients, CCTA repeated for clinical reasons, substantial share developed plaque (72-74) | supported (clinical indication comes from the PARADIGM design paper, not from Won) |
| Won: rapid progression associated with HbA1c at follow-up, not with conventional risk factors; no geometry (75-76) | supported, but with a power caveat (few events) |
| Chen: "shape and image texture of the LAD just before the myocardial bridge", moderately identified patients who developed plaque there (77-79) | partly wrong ("image texture"); the rest is supported |
| Lee: plaque-free segments, same registry, radiomic features; adding them to clinical risk factors better identified segments (80-82) | supported (abstract level) |
| "all three used patients scanned for a clinical reason" (84-85) | supported for Won and Lee (PARADIGM design), unverifiable for Chen |
| "random population samples avoid this selection" (87) | overstated (they reduce it; SCAPIS took part in a random invitation with incomplete participation) |
| Bergström: random population sample scanned once (89) | supported |
| Good: "have so far reported only the design of its re-examination" (90-91) | nearly supported (design plus interim risk-factor data, no plaque results) |
| Hageman: CAC "improved SCORE2 only slightly" for cardiovascular events (93-94) | supported in direction; "modestly" is the authors' word, and CAC was the largest of the modifiers |
| "mostly confined it to a single artery or bifurcation" (Kashyap, Tommasino, Chen, Tello Ayala) (99-100) | supported for the four cited; "mostly" hides Li, Zhang and Han, which measured more |
| Gap sentence (101-102) | defensible as worded; Chen 2024 is the nearest miss and should be named as such |

## Glagov 1987: is "showed" appropriate?

### Takeaway
The finding is correct: in 136 autopsy left main arteries, the area within the internal elastic lamina
grew with plaque area. "In proportion to" is stronger than the data (a moderate correlation in a
cross-section), and "enlargement" is the authors' inference from a cross-sectional sample, so "found" or
"reported" fits better than "showed".

### Cited Findings
- Design: "We studied histologic sections of the left main coronary artery in 136 hearts obtained at autopsy" — [Glagov 1987, Europe PMC abstract](https://europepmc.org/article/MED/3574413)
- "The internal elastic lamina area correlated directly with the area of the lesion (r = 0.44, P less than 0.001), suggesting that coronary arteries enlarge as lesion area increases." — [Glagov 1987](https://europepmc.org/article/MED/3574413)
- The lumen area did not fall for stenosis between 0 and 40 percent, but "did diminish markedly ... for values above 40 percent (r = -0.73)". Authors' conclusion: "human coronary arteries enlarge in relation to plaque area" — [Glagov 1987](https://europepmc.org/article/MED/3574413)

### Inferences
- "Larger in proportion to" implies proportionality. The data give a moderate correlation (r = 0.44) and a regression slope of 0.88, for one artery (the left main). "Larger with more plaque" or "enlarged in relation to plaque area" (the authors' own phrase) is accurate.
- "Showed" suits a direct measurement, but the claim that arteries *enlarge* is a longitudinal process inferred from cross-sectional autopsy data. The header comment ("keep the wording to what it found") already flags this. "Found" is the safe verb.
- The second sentence ("geometry of a diseased artery may have been shaped by the plaque rather than have predisposed to it") follows from Glagov and is suitably hedged ("may").
- Suggested wording: "In an autopsy study of the left main coronary artery, Glagov et al. (1987) found that the area within the internal elastic lamina was larger in arteries with more plaque, and concluded that coronary arteries enlarge as plaque accumulates."

### Gaps
- None.

## Were Li, Zhang, Han, Tommasino and Tello Ayala all "conducted in patients who already had coronary disease"?

### Takeaway
Not for all five. All five used patients who were referred or symptomatic and measured geometry on the same
scan that showed the disease. Only Han (all cases had a culprit lesion precursor) and largely Tommasino
studied patients who mostly had disease already. Li, Zhang and Tello Ayala compared patients with and without
disease. The reverse-causality argument still holds, because geometry and disease were measured at the same
time. Only the description of the samples needs to change.

### Cited Findings
- Li 2011: "1010 consecutive patients underwent coronary angiography with complaints of chest pain"; 569 (56.3%) had CAD, defined as "≥50% luminal narrowing in at least one main coronary artery"; tortuosity was assessed in the LAD, LCx and RCA (≥3 bends of ≥45° "along main trunk of at least one artery") — [Li 2011, PLoS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0024232)
- Zhang 2024: ASOCA public dataset of "patients with suspected CAD"; 20 non-stenosed, 12 moderately and 7 severely stenosed left trees (one of 40 excluded); left main, LAD, LCx and their branches only, no RCA; no risk-factor adjustment, although sex and age differed between groups — [Zhang 2024, PMC11416812](https://pmc.ncbi.nlm.nih.gov/articles/PMC11416812/)
- Han 2022: ICONIC nested case-control; "patients with ACS and a culprit lesion precursor identified on baseline CCTA (n = 116) and propensity score-matched non-ACS controls (n = 116)"; Table 1 lists 9 controls with a "Normal" CAD read — [Han 2022, Europe PMC](https://europepmc.org/article/MED/35080587); [JAMA Cardiology full text](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
- Tommasino 2024: "Consecutive patients undergoing CCTA for suspected CAD"; severe proximal LAD stenosis in 32% (160/499) (Table 1 gives "Proximal LAD disease" in 42.1%) — [Tommasino 2024, PMC11595042](https://pmc.ncbi.nlm.nih.gov/articles/PMC11595042/)
- Tello Ayala 2026: 38,691 RCA angiograms from 22,334 patients; regression of tortuosity on age, sex, risk factors and "presence of CAD"; tortuosity associated with "presence and severity of CAD" — [Tello Ayala 2026, Europe PMC abstract](https://europepmc.org/article/MED/42312790)

### Inferences
- Patients undergoing invasive angiography (Li, Tello Ayala) or CCTA for suspected CAD (Zhang, Tommasino) are referred patients in whom disease and geometry are measured on the same scan. That is the design flaw that matters for reverse causality, and it is accurate for all five.
- Suggested wording (no numbers): "Nevertheless, most studies relating coronary geometry to disease compared diseased with disease-free arteries in patients referred for angiography, so geometry and disease were measured on the same scan [li, zhang, han, tommasino, telloayala], and their associations are susceptible to reverse causality." An alternative keeps the current frame: "were conducted in referred patients, many of whom already had coronary disease".
- Han is the only one of the five with a time order (CCTA before ACS). That time order is very short (median 29 days), and every case already had the culprit lesion on the baseline scan, so the reverse-causality point applies to Han as well.

### Gaps
- Tello Ayala: full text not opened (JACC Advances returned 403 and PMC served a bot check). The proportion with CAD and whether the angiograms were clinically indicated are unverified, although invasive angiography is always clinically indicated in practice.

## Does "mostly confined to a single artery or bifurcation" hold, and how many arteries did Li, Han and Zhang measure?

### Takeaway
It holds for the four cited studies. Kashyap measured the LM bifurcation with its LAD and LCx branches,
Tommasino the LM bifurcation angle, Chen the LAD segment proximal to a bridge, and Tello Ayala the RCA only.
The studies that measured more, Li (all three arteries, visual bend count), Han (lesions in all three
arteries) and Zhang (the whole left tree, no RCA), are not cited in that sentence, so "mostly" is carrying them.

### Cited Findings
- Kashyap 2022: "127 patients without coronary artery disease"; tortuosity measures "applied ... to the left main coronary artery bifurcation, and to its left anterior descending and left circumflex branches"; CFD gave low TAWSS (< 0.4 Pa) — [Kashyap 2022, Europe PMC](https://europepmc.org/article/MED/35039557)
- Tommasino 2024: one geometric measure, the LM bifurcation angle (LMBA > 80°) — [PMC11595042](https://pmc.ncbi.nlm.nih.gov/articles/PMC11595042/)
- Chen 2024: four models, the centreline and cross-section of the bridge (MB CL, MB CS) and of the segment just proximal to it (pMB CL, pMB CS) — [Chen 2024, Europe PMC](https://europepmc.org/article/MED/38781436)
- Tello Ayala 2026: "automated right coronary artery (RCA) tortuosity measure" — [Europe PMC](https://europepmc.org/article/MED/42312790)
- Li 2011: LAD, LCx and RCA (tortuosity found in the LCx in 26.9%, LAD 21.1%, RCA 1.4% of patients); visual bend count on invasive angiograms — [PLoS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0024232)
- Han 2022: lesions over the 18-segment SCCT model; culprit lesions 64 LAD, 19 LCx, 33 RCA. The geometry was local to each lesion (distance from the ostium, bifurcation location, tortuosity within the lesion) — [JAMA Cardiology](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
- Zhang 2024: the left tree (LM, LAD, LCx, branches such as D1, D2, M1), nine anatomical features at whole-tree, bifurcating and non-bifurcating level; no RCA — [PMC11416812](https://pmc.ncbi.nlm.nih.gov/articles/PMC11416812/)

### Inferences
- Kashyap is a CFD study of geometry against WSS in CAD-free patients. It did not relate geometry to plaque at all, so it sits awkwardly in a list of "studies that did measure geometry" in a paragraph about plaque development. It is accurate as an example of a single-bifurcation measurement.
- A more complete and still number-free version: "The studies that did measure geometry either confined it to a single artery or bifurcation [kashyap, tommasino, chen, telloayala] or measured it on scans that already showed disease [li, zhang, han]." This uses every cited element, which the chapter's synthesis rule requires.
- Typo on line 101: "litterature review" should be "literature review" (the file name keeps its spelling). The brief quotes "in this search"; the file now says "in this litterature review".

### Gaps
- None.

## Won 2022: plaque-free PARADIGM patients, plaque development, HbA1c and risk factors

### Takeaway
Supported. The 402 PARADIGM patients had no plaque at baseline (median interval 3.6 years); 35.6% developed
plaque. No baseline risk factor was associated with rapid progression; HbA1c measured at follow-up was
associated with the annual change in percent atheroma volume. Plaque development itself was not modelled,
and no geometry was measured. Two caveats: rapid progression occurred in only 4.2% (about 17 patients), so the
null result for risk factors has little power, and HbA1c at follow-up is not a baseline predictor.

### Cited Findings
- "402 patients ... without coronary plaques at baseline who underwent serial coronary CCTA were identified from the ... PARADIGM registry"; "median inter-scan period of 3.6 years (interquartile range: 2.7-5.0 years), newly developed coronary plaques and RPP were observed in 35.6% and 4.2% of the patients" — [Won 2022, Europe PMC](https://europepmc.org/article/MED/36371222)
- "The baseline traditional risk factors, i.e., advanced age (≥ 60 years), male sex, hypertension, diabetes mellitus, hyperlipidemia, obesity, and current smoking status, were not significantly associated with the risk of RPP." — [Won 2022](https://europepmc.org/article/MED/36371222)
- "the serum hemoglobin A1c level (per 1% increase) measured at follow-up CCTA was independently associated with the annual change in the PAV (β: 0.098, 95% CI 0.048-0.149)" — [Won 2022](https://europepmc.org/article/MED/36371222)
- RPP was defined as an annual increase of ≥ 1.0%/year in percent atheroma volume. Logistic regression was used for RPP; the full text gives no separate model for the occurrence of new plaque and no geometry measure. The authors call it "a retrospective case–control study" — [Won 2022, PMC9655903](https://pmc.ncbi.nlm.nih.gov/articles/PMC9655903/)
- Won does not state why patients were rescanned. The PARADIGM design paper states that patients referred for clinically indicated CCTA were enrolled if they had a second CCTA — [PARADIGM design, Lee 2016 Am Heart J (record)](https://researchexperts.utmb.edu/en/publications/rationale-and-design-of-the-progression-of-atherosclerotic-plaque/) (abstract-level search result)

### Inferences
- "a substantial share developed plaque" is accurate (about a third).
- "who had CCTA repeated for clinical reasons" is supported by the registry design, not by Won itself. It is safest to cite the design paper too, or to write "who had a repeat CCTA".
- "Rapid progression was associated with glycated haemoglobin at follow-up but not with the conventional risk factors" is accurate. Strictly, HbA1c was associated with the *annual change in PAV* (continuous); the abstract headline is about RPP. With about 17 RPP events, "not associated" means "not shown". A careful sentence: "No baseline risk factor was associated with rapid progression, although such progression was rare, whereas glycated haemoglobin measured at follow-up was."
- Table: "402 referred, 3.6 years", geometry "None", PF ✓, Pop ✗, FU ✓ are all correct. Adj "--" is defensible because plaque development was not modelled.

### Gaps
- The minimum inter-scan interval in PARADIGM (≥ 2 years per Lee 2024) is not stated in Won.

## Chen 2024 (myocardial bridge): what was measured, outcome, performance, risk factors, plaque-free level

### Takeaway
The features were mostly **geometric**, not image texture: centreline parameters (curvature, arc length)
and cross-section metrics (areas, axis lengths) of the LAD at the bridge and just proximal to it, in diastole
and systole, summarised by first-order statistics. The best model (proximal-bridge cross-section) reached
AUC 0.78, 0.75 and 0.75 (training, internal test, external). Combined with a clinical model that kept only
diabetes, it reached about 0.79 and 0.76. Patients had no plaque in the LAD (or the pre-bridge segment) at
baseline, not necessarily in the whole tree. The median interval was 3.0 years in the development set.

### Cited Findings
- "Patients with repeated CCTA scans showing LAD MB without proximal plaque in index CCTA were included from Jinling Hospital as a development set ... Patients from four other tertiary hospitals were set as external validation set. The endpoint was proximal plaque development of LAD MB in follow-up CCTA." 295 patients: development n = 192, external n = 103. "The pMB CS vascular radiomics model exhibited higher AUCs in training, internal test, and external sets (AUC = 0.78, 0.75, 0.75) than the clinical and anatomical model" — [Chen 2024, Europe PMC abstract](https://europepmc.org/article/MED/38781436)
- Full text: inclusion "no plaques located in LAD were detected at baseline CCTA"; the results narrow it to patients "without plaques in the pre-MB segment"; at least two CCTAs ≥ 3 months apart, with no clinical indication stated; median follow-up "3.0 years [IQR, 1.7–4.5 years]" in development and 2.1 years (IQR 1.4–3.1) external; plaque developed in 27.1% (52/192) and 32.0% (33/103) — [Chen 2024, OUP full text](https://academic.oup.com/ehjcimaging/article/25/10/1462/7676581)
- Features: "16 conventional quantitative cross-section metrics" and "17 centreline parameters (e.g. curvature and arc segment length of the diastolic and systolic phase", with "first-order statistics" applied — [OUP full text](https://academic.oup.com/ehjcimaging/article/25/10/1462/7676581)
- Clinical model: only diabetes survived multivariable selection (OR 3.70); "only a clinical model with diabetes was built"; no anatomical variable was significant. Clinical AUC 0.60 (development) and 0.56 (external); combined model 0.79 and 0.76 (the abstract gives 0.75 external, which conflicts with the 0.76 in Table 3) — [OUP full text](https://academic.oup.com/ehjcimaging/article/25/10/1462/7676581)

### Inferences
- "measured the shape and image texture of the LAD" is **partly wrong**. The "vascular radiomics" here are lumen and centreline geometry over the cardiac cycle. They are not grey-level texture of the image. Better: "described the shape of the LAD just before a myocardial bridge by its centreline and cross-sections over the cardiac cycle". This also matters for the gap paragraph. Chen *is* a plaque-free-baseline study of geometry, confined to one segment, which is why it is correctly listed among the single-artery geometry studies (line 100).
- "moderately identified the patients in whom plaque developed there" is supported (AUC about 0.75 to 0.78).
- Table "192 referred, bridge, 3 years": 192 is the development set only (295 with the external set). "Referred" is plausible, since these were hospital patients with repeat CCTA, but no indication is stated. Adj "?": the radiomics model was combined with a clinical model, but that clinical model held only diabetes, so "partly" (a new symbol or footnote) is more accurate than "not reported". PF ∘ (one artery or segment only) is correct.
- The external set is small (33 events), so AUC differences carry wide intervals.

### Gaps
- The final 30,000 characters of the OUP page (discussion, supplementary) were not read.

## Lee 2024 (radiomics): what was measured, outcome, performance, risk factors, plaque-free level

### Takeaway
Supported at abstract level. 9,583 plaque-free segments from 1,162 patients in a prospective multinational
serial-CCTA registry (≥ 2-year intervals; the NCT number is PARADIGM's). The outcome was plaque of total
volume ≥ 1 mm³ in the segment at follow-up (9.8% of segments). Radiomics alone matched clinical risk factors
(C about 0.70 each). Clinical risk factors plus radiomics reached C 0.772 (training) and 0.767 (test).
Plaque-free is per segment, so patients could have plaque elsewhere.

### Cited Findings
- "From a prospective multinational registry of patients with serial CCTA studies at ≥ 2-year intervals, segments without identifiable coronary plaque at baseline were selected and radiomic features were extracted. Cox models using clinical risk factors (Model 1), radiomic features (Model 2) and both ... (Model 3) ... to predict the development of a coronary plaque, defined as total PV ≥ 1 mm3" — [Lee 2024, Europe PMC abstract](https://europepmc.org/article/MED/38378314)
- "9583 normal coronary segments were identified from 1162 patients ... divided 8:2 into training and test sets. At follow-up CCTA, 9.8% of the segments developed new coronary plaque." Model 1 vs Model 2: 0.701 vs 0.699 (training), 0.696 vs 0.691 (test), "all p > 0.05". Model 3: 0.772 and 0.767 — [Lee 2024](https://europepmc.org/article/MED/38378314)
- Registry: "ClinicalTrials.gov NCT0280341" (truncated in the abstract; PARADIGM is NCT02803411, the number Won 2022 gives) — [Lee 2024](https://europepmc.org/article/MED/38378314); [Won 2022](https://europepmc.org/article/MED/36371222)

### Inferences
- "in the same registry" is supported by the NCT number.
- "features computed from the intensity pattern of the image" is the usual meaning of radiomics. The abstract does not list the feature classes, so whether shape features were included is unverifiable.
- "adding these to clinical risk factors better identified the segments" is supported. A careful reader should know that radiomics alone did no better than clinical factors. The split was 8:2 of *segments*, so a split by person is not confirmed, and if segments of one patient fell in both sets the test C may be optimistic. That is a skeptical point worth a comment in the source, but not a prose number.
- Table "1,162 referred, ≥2 years": ≥ 2 years is the minimum interval, but the table note says "Follow-up as median". Either give Lee's median (not found) or mark the cell, for example "≥2 years (minimum)". Adj ✓ and PF ∘ are correct. Lee and Won come from one registry, so they are not independent evidence.

### Gaps
- Full text not opened (PubMed bot check; JCCT not fetched). Feature classes, median interval, whether the split was by person, and the clinical covariates in Model 1 are unverified. The chapter header already records that the Lee row is abstract level.

## Population samples: Bergström 2021, Good 2026, "avoid this selection"

### Takeaway
Bergström: supported (25,182 participants without known CHD from 30,154 randomly invited, one CCTA). Good 2026
reports the design **and** interim risk-factor data for the first 5,000 re-examined, but no plaque results.
"Avoid this selection" is too strong: random invitation removes referral selection but not participation
selection.

### Cited Findings
- "We recruited 30 154 randomly invited individuals age 50 to 64 years to SCAPIS ... In total, 25 182 individuals without known coronary heart disease were included"; any atherosclerosis in 42.1%; external validity checked "using inverse probability for participation weighting and Swedish register data" — [Bergström 2021, Europe PMC](https://europepmc.org/article/MED/34543072)
- Good 2026: re-examines "approximately 15,000 participants (50% of the original SCAPIS cohort)", median 8.1 years after baseline; "Interim analyses of the first 5000 participants" report changes in hypertension, diabetes, adiposity and smoking — [Good 2026, Europe PMC](https://europepmc.org/article/MED/41558989)
- A search found no published SCAPIS re-examination results on plaque progression or incident plaque as of November 2026. The trial is registered as NCT06679777 — [search record, NCT06679777 listing](https://www.centerwatch.com/clinical-trials/listings/NCT06679777/swedish-cardiopulmonary-bioimage-study-2)

### Inferences
- Suggested wording: "Good et al. (2026) have so far reported the design of its re-examination but no plaque results." Also "random population samples reduce this selection" instead of "avoid".
- Table Bergström row: "25,182 random, one scan", Pop ✓, FU ✗, geometry "None" are correct. PF ✗ is a judgement: SCAPIS includes many plaque-free people (57.9%), but the study did not analyse them as a plaque-free baseline. A footnote could say PF means "analysed from a plaque-free baseline".
- "have not yet related geometry to later plaque" is supported only as an absence of evidence (search-based).

### Gaps
- The SCAPIS Gothenburg/Uppsala sub-studies were not searched one by one for coronary geometry.

## Hageman 2023: did CAC improve SCORE2 only slightly?

### Takeaway
Supported in direction. CAC percentile raised the C-index by 0.0198 (95% CI 0.0115 to 0.0281), the largest gain of
any modifier tested. The authors call the gains "modest". The CAC estimate comes from two cohorts (MESA, HNR)
and was not externally validated (CPRD had no CAC). The outcome was CVD events, not plaque.

### Cited Findings
- n = 409,757 from UK Biobank, ARIC, MESA, EPIC-NL and HNR; 16,166 CVD events over 10.0 years; Fine–Gray models; "Risk modifying characteristics that increased discrimination most were CAC percentile with 0.0198 [95% CI 0.0115; 0.0281]"; external validation C 0.740 vs 0.737 — [Hageman 2023, Europe PMC](https://europepmc.org/article/MED/37264679)
- Full text: CAC percentile only in HNR (n = 3,679) and MESA (n = 5,670); "CAC score was not available in the CPRD GOLD data"; authors write "led to a modest increase in discrimination" and "only modestly improved"; CAC was "clearly the most effective risk modifier"; outcome "a composite of cardiovascular mortality, non-fatal myocardial infarction, and non-fatal stroke" — [Hageman 2023, PMC10600319](https://pmc.ncbi.nlm.nih.gov/articles/PMC10600319/)

### Inferences
- "only slightly" is acceptable. "only modestly" matches the authors' word. A reader could take "only slightly" as "CAC is not useful", whereas CAC was the strongest modifier, so the point is that even the strongest imaging marker of existing disease adds little to SCORE2. Suggested wording: "Hageman et al. (2023) found that even coronary artery calcium, the strongest of the risk modifiers they examined, improved the discrimination of SCORE2 for cardiovascular events only modestly."
- The sentence ties Hageman to "beyond the established risk factors". That is fair, but Hageman concerns events. Geometry for incident plaque is a different outcome, so the inference is by analogy and should not be phrased as evidence about plaque.

### Gaps
- None.

## Is the gap sentence defensible, and table-level corrections

### Takeaway
Defensible as worded ("the geometry of the three main coronary arteries on a plaque-free baseline scan ...
plaque development at follow-up"). The nearest misses are Chen 2024 (geometry from a plaque-free LAD, one
segment, referred, about 3 years) and Lee 2024 (plaque-free segments, radiomics, referred). Neither covers all
three arteries in a plaque-free person, and neither is a population sample. A targeted search found no study
that measured multi-artery geometry on a plaque-free baseline against later plaque.

### Cited Findings
- No matching study turned up for searches of tortuosity or bifurcation angle on a plaque-free baseline CCTA against later plaque. The closest were the CLAP score (diseased baseline), a cross-sectional proximal-LAD geometry study (Moon 2023, QIMS) and the GEOMETRY-CTA protocol (12-month, about 100 patients, cross-sectional aim) — [Tommasino 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11595042/); [QIMS 2023](https://qims.amegroups.org/article/view/117032/html)
- Chen 2024 measured geometry (centreline curvature, cross-sections) from a plaque-free LAD against later plaque — [OUP](https://academic.oup.com/ehjcimaging/article/25/10/1462/7676581)
- Tommasino follow-up: "mean follow-up of 374.39 days (SD 104.28 days)"; follow-up imaging "when clinically indicated"; progression "an increase in luminal stenosis of at least 30% from baseline" plus new high-risk features; Table 3 gives LMBA > 80° for "disease progression in the proximal LAD" (HR 5.325); Methods say Cox, Table 2 is titled "Logistic regression"; MACE model covariates: diabetes, CKD, LMBA, high-risk plaque, CAC, obstructive CAD, selected at p < 0.10 — [PMC11595042](https://pmc.ncbi.nlm.nih.gov/articles/PMC11595042/)
- Han: propensity score built on age, sex, risk factors **and site-read CAD severity**; lesion-level Cox adjusted for stenosis, adverse plaque characteristics and quantitative plaque measures; median CCTA-to-ACS time 29 days (IQR 5 to 386) — [JAMA Cardiology](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)

### Inferences
Table cells, row by row:
- **Han 2022**: "116 ACS, 116 controls" ✓; "Lesion site, bends" ✓; main finding ✓ (the tortuosity counts were tiny, 5 vs 6 lesions); PF ✗ ✓; Pop ✗ ✓; FU ✗ ✓ (follow-up to ACS, no repeat scan); Adj ✓b ✓. Footnote b should read "Controls matched on risk factors and CAD severity".
- **Tommasino 2024**: "499 referred" ✓; "1 year" is a **mean**, which conflicts with the note "Follow-up as median". "LM angle" ✓. "Wide LM angle with proximal LAD progression" is supported by Table 3, but the headline association is with composite MACE (which counts proximal LAD progression as a component). Footnote a ✓ (the HR CI 3.80 to 6.70 is asymmetric around 4.47; Cox vs logistic conflict confirmed). FU ✗ is defensible (repeat imaging showed progression of existing disease, not plaque development) but could confuse, so state in the note that FU means a repeat scan from a plaque-free baseline. Adj ✓ is partial: the covariates were selected (diabetes, CKD, plaque, CAC), not the conventional risk-factor set.
- **Won 2022**: all cells ✓.
- **Chen 2024**: 192 = development set (295 in all); "3 years" ✓ (development median); geometry "LAD shape, radiomics" is fine if "radiomics" is understood as shape statistics (drop the texture reading in the prose); main finding ✓; PF ∘ ✓; FU ✓; Adj "?" should be "partly" (diabetes only).
- **Lee 2024**: 1,162 ✓; "≥2 years" is a minimum, not a median; "Radiomic texture" is plausible but unverified (abstract only); "Added to clinical risk factors" ✓; PF ∘ ✓; Adj ✓.
- **Bergström 2021**: all cells ✓; "Re-examination under way (Good 2026)" ✓.
- **Caption**: "relating coronary geometry or risk factors to later plaque" overstates Han (ACS) and Bergström (no follow-up). Suggest "Overview of the studies in this section, by sample, geometry measured and design."

Further prose points:
- Line 84 cites only Chen and Lee for "a plaque-free scan holds information about later plaque", which is right, since Won measured no imaging features. The clause "but all three used patients scanned for a clinical reason" then needs Won among its citations, because "all three" includes it.
- Line 96-98 ("either did not measure geometry [won] or described the image texture rather than the geometry [lee]") is correct, but it leaves Chen to the next sentence. Chen is the one plaque-free study that measured geometry, and saying so makes the gap sharper: "... and the one study that measured geometry from a plaque-free scan confined it to the LAD segment before a myocardial bridge [chen]".
- All suggestions keep to the chapter rules: no numbers in prose, author-year as subject, no lists, no em dashes.

### Gaps
- The search for counter-examples to the gap sentence was limited (two targeted searches plus the earlier note `research_notes/Literature review table and gaps/near_misses_longitudinal.md`). A database search with a stated strategy (the TODO in `00_chapter_intro.tex`) is still needed before the gap can be called systematic.
- The Tommasino page's final 11,500 characters and the Han page's final 30,000 characters were not read.
