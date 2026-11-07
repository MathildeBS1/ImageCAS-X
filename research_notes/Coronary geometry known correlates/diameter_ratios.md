# LM→LAD and LM→LCx diameter ratios: scaling laws, normal values, correlates

Scope: expected values and validation checks for LM/LAD and LM/LCx diameter ratios taken from in-house tracer lumen contours in CGPS CCTA (about 1,200 plaque-free and about 600 plaque scans).

## 1. Bifurcation scaling laws (Murray, Finet, Huo–Kassab): empirical fit in human LM bifurcations

### Takeaway
In human coronary bifurcations the effective diameter exponent is below Murray's 3 and close to Huo–Kassab's 7/3 (pooled about 2.4). Finet's linear 0.678 is a good approximation only for near-symmetric bifurcations (Ds/Dl ≥ 0.75), which is the typical LAD/LCx case. Scatter for a single bifurcation is large: the Finet ratio has an SD of about 0.08 in normal CTA, which is about ±12%. In diseased LM bifurcations no law predicts the LM diameter better than about ±0.8–1 mm.

### Cited Findings
- **Finet et al. 2008 (EuroIntervention 3:490–498), QCA plus IVUS.** The sample is described inconsistently in the paper. The abstract says 47 patients, 27 of them with IVUS. The methods/results text says 59 of 87 enrolled patients under 55 years (35 F / 24 M, age 46 ± 8.5) with angiographically normal coronaries, scanned before valve surgery, giving 173 bifurcations (about 2.9 per patient). Mean QCA diameters: mother 3.33 ± 0.94 mm, major daughter 2.70 ± 0.77, minor daughter 2.23 ± 0.68. Reported R = Dm/(Dd1+Dd2) = 0.678 (no SD given for the whole set). In the IVUS subgroup R(IVUS) = 0.668 ± 0.028, with angiography not significantly different. Mean deviation from measured: 0.33% for the linear law versus 5% for Murray. QCA underestimates IVUS diameters by −4.4% (LM), −4.3% (LAD) and −5.5% (LCx). The text has internal inconsistencies: 3.39/(2.708+2.236) works out to 0.686, not 0.678, and the "overestimate" direction of Murray differs between text and figure. — [Finet 2008](https://eurointervention.pcronline.com/article/fractal-geometry-of-arterial-coronary-bifurcations-a-quantitative-coronary-angiography-and-intravascular-ultrasound-analysis)
- **Huo–Kassab (HK) law.** D_m^(7/3) = D_d1^(7/3) + D_d2^(7/3), derived from a minimum-energy hypothesis. They report the 7/3 flow–diameter exponent (2009 Biophys J) and validate it mainly in swine casts. The intraspecific scaling paper is J R Soc Interface 9(66):190–200 (online 2011, issue 2012, DOI 10.1098/rsif.2011.0270). — [Huo & Kassab, PMC3223633](https://pmc.ncbi.nlm.nih.gov/articles/PMC3223633); [Kassab & Finet review, EuroIntervention](https://eurointervention.pcronline.com/article/structure-function-relation-in-the-coronary-artery-tree-from-fluid-dynamics-to-arterial-bifurcations/pdf)
- **Huo, Finet et al. 2011–2012, "Optimal diameter of diseased bifurcation segment" (EuroIntervention, DOI 10.4244/EIJV7I11A206).** Tested on Finet's human QCA/IVUS data and on swine casts (mother ≥ 0.5 mm). HK agrees for all bifurcation types and was within ±4% in the swine data. Murray and area preservation (AP) agree only for Ds/Dl ≤ 0.25. Finet agrees only for Ds/Dl ≥ 0.75 (≥ 0.65 in swine) and is "in gross error" below 0.75. The implied Dm/(Dl+Ds) coefficient for Ds/Dl ≥ 0.75: HK 0.676 ± 0.001, Murray 0.634 ± 0.002, AP 0.710 ± 0.001, Finet 0.678. As Ds/Dl → 1: HK 0.673, Murray 0.63, AP 0.707. As Ds/Dl → 0, all coefficients → 1. — [Huo et al., EuroIntervention](https://eurointervention.pcronline.com/article/optimal-diameter-of-diseased-bifurcation-segment-a-practical-rule-for-percutaneous-coronary-intervention)
- **Normal CTA atlas, Medrano-Gracia et al. 2016 (EuroIntervention 12:845–854).** n = 300 (64% F, age 55.3 ± 9.1, 85% European, Auckland), CAC = 0, no stenosis, 64-slice CT at 75% R-R with nitroglycerine. Area-equivalent diameter every 0.5 mm normal to the centerline. Across bifurcations the Finet ratio was 0.6576 ± 0.083. The least-squares fit of D_p^α = D_d^α + D_sb^α was best at α = 2.4, "closest to the Huo–Kassab model". — [Medrano-Gracia 2016](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)
- **Systematic review and meta-analysis of Murray's law in coronaries (Am J Physiol Heart Circ Physiol 2024, PMID 38787386).** Pooled flow–diameter exponent across epicardial and transmural arteries: 2.39 (95% CI 2.24–2.54), I² = 99%. The authors say this is very close to Kassab's 7/3. — [Search summary of PubMed 38787386](https://pubmed.ncbi.nlm.nih.gov/38787386/); [author repository PDF (not retrieved; access blocked)](https://shura.shu.ac.uk/34534/1/Saxton-SystematicReviewAndMetaanalysis(VoR).pdf)
- **Diseased LM bifurcations, ABC Cardiol 2025.** QCA plus IVUS in 13 patients with mean LM plaque burden 43%. Predicting LM diameter from LAD + LCx, bias / precision (mm) against QCA: Murray 0.06 / 0.95, Finet −0.35 / 0.96, HK −0.03 / 0.95. Against IVUS: Murray −0.49 / 0.84, Finet −0.91 / 0.82, HK −0.64 / 0.84. IVUS was 11.4% larger than QCA. The authors call the study exploratory. — [Estimating LM bifurcation geometry, ABC Cardiol](https://new.scielo.br/j/abc/a/x4td9RRjsfcNcF9kcHtjf9n/?lang=en)
- **Other LM QCA work.** Measured LM 3.75 ± 0.85 mm versus Finet-predicted 3.89 ± 0.80 mm. Finet-QCA did not improve LM reference-diameter estimation over conventional bifurcation QCA. — [Lunardi 2025, Cardiol Res Pract](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12145935/)
- **Theory.** Finet's and HK's rules have been shown to be special cases of a generalised Murray law, with a CT 3D left coronary dataset used in support. — [Finet's Law as a special case of the generalised Murray's law](https://open.icm.edu.pl/handle/123456789/21895)

### Inferences
- **Laws for typical LAD/LCx diameters.** For LAD ≈ 3.2 mm and LCx ≈ 3.0 mm (atlas means), the laws predict LM ≈ 3.91 mm (Murray, α = 3), ≈ 4.18 mm (HK, α = 7/3) and ≈ 4.20 mm (Finet). That gives an expected LM/LAD ≈ 1.22–1.31 and LM/LCx ≈ 1.30–1.40. These are my own arithmetic from the published formulas.
- **The atlas LM table does not follow the laws.** In the same normal CTA atlas, the LM-specific mean diameters (3.5 / 3.2 / 3.0 mm) give a ratio of means of only 1.09 (LM/LAD) and 1.17 (LM/LCx). The implied exponent at the LM level is very high (my calculation: about 6). The LM diameter there is apparently an average along the whole LM trunk, while daughter values are averages along each branch, which differs from the near-carina reference diameters the laws assume. Measurement definition can therefore move LM/daughter ratios by more than the difference between laws. The tracer's ratio should be compared with values that were measured the same way.
- **What to expect for a correct extraction.** On plaque-free CTA, the per-bifurcation exponent should centre at about 2–3 (pooled 2.4), with wide per-case scatter. A median exponent far outside 2–3 under a near-carina sampling protocol would suggest a systematic bias in the LM or daughter diameters.

### Gaps
- No full-text CCTA study was found that fits Murray, HK and Finet specifically at the LM bifurcation in a plaque-free general population, with the scatter reported. The Medrano-Gracia 2017 (J Cardiovasc Transl Res, 211 cases with CAC 0 and no intermediate artery) shape-model paper reportedly compares laws, but was paywalled and not verified.
- Per-bifurcation SD of the fitted exponent was not found. Only the Finet-ratio SD (0.083) is available.
- The meta-analysis full text (diameter-only exponents by modality and disease) could not be retrieved.

## 2. Normal LM, proximal LAD and proximal LCx diameters and their ratios

### Takeaway
Normal CTA lumen (area-equivalent) diameters are about 3.5 mm (LM), 3.2 mm (LAD) and 3.0 mm (LCx), about 15–20% smaller in women. Invasive QCA gives larger values (Dodge: LM 4.5, proximal LAD 3.7 mm). LAD is typically about 5–10% larger than LCx. LM/LAD is about 1.1–1.2 and LM/LCx about 1.15–1.3, depending on modality and on where the diameters are measured.

### Cited Findings
- **Dodge et al. 1992 (Circulation 86:232).** 83 angiograms with smooth lumen borders, selected from 9,160 (70 normal, 7 with dilated cardiomyopathy, 6 with LVH from aortic stenosis). 96 points in 32 segments. LM 4.5 ± 0.5 mm, proximal LAD 3.7 ± 0.4 mm, distal LAD 1.9 ± 0.4 mm. Women's diameters were 9% smaller (p < 0.001), still significant after BSA normalisation (p < 0.01). Diameters were not affected by age or tortuosity. LAD diameter was not affected by dominance, but RCA and LCx were. Diameters were larger in LVH (about +17%) and in dilated cardiomyopathy (about +12%). — [Dodge 1992 abstract](https://www.ahajournals.org/doi/10.1161/01.cir.86.1.232)
- **Dodge 1992, LCx by dominance.** A search-engine summary of the same paper gives proximal LCx as 3.4–4.2 mm depending on dominance (significant). This was not verified against the full text. — [Dodge 1992](https://www.ahajournals.org/doi/pdf/10.1161/01.cir.86.1.232)
- **Medrano-Gracia 2016 normal CTA atlas, LM-bifurcation table** (n = 217 without intermediate artery; area-equivalent diameter; values are mean ± SD [Q1–Q3]):
  - All: LM 3.5 ± 0.8 [3.2–4.1], LAD 3.2 ± 0.7 [2.8–3.6], LCx 3.0 ± 0.7 [2.5–3.5].
  - Males (n = 66): LM 4.1 ± 0.6, LAD 3.7 ± 0.6, LCx 3.6 ± 0.6.
  - Females (n = 151): LM 3.3 ± 0.7, LAD 3.0 ± 0.6, LCx 2.8 ± 0.7.
  - With intermediate artery (n = 74): males (n = 38) LAD 3.6, LCx 3.2; females (n = 36) LM 3.0, LAD 2.7, LCx 2.6.
  - Confluence (flare) region: Dmax 5.2 ± 1.2, Dmin 3.6 ± 0.8, eccentricity 1.4 ± 0.3.
  - LM length 10.2 ± 5.6 mm (10.5 ± 5.3 overall).
  - LAD tapers about 0.25 mm per 10 mm beyond bifurcations.
  - The LM IQR of 3.2–4.1 mm agrees with QCA (3.1–4.2) but differs from post-mortem measurements (4.9 ± 0.8).

  — [Medrano-Gracia 2016](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)
- **BSA-indexed values in an Indian cohort.** LM 2.34, proximal LAD 1.87 and proximal LCx 1.70 mm/m², with no sex difference after BSA indexing. The modality was not verified. — [Coronary artery dimensions in normal Indians](https://www.sciencedirect.com/science/article/pii/S0019483216302668)
- **MDCT of angiographically normal arteries.** Women had smaller lumen diameters in all segments except the proximal RCA and the LM. — [MDCT normal coronary volume/dimensions](https://www.sciencedirect.com/science/article/abs/pii/S1934592517300862)

### Inferences
- **Ratios from published means** (ratio of means, not the mean of per-person ratios; my arithmetic):
  - Atlas CTA: LM/LAD 1.09, LM/LCx 1.17, LAD/LCx 1.07. Males 1.11 / 1.14 / 1.03; females 1.10 / 1.18 / 1.07.
  - Dodge QCA: LM/proximal LAD 1.22.
  - Finet's generic mother/major daughter is 1.23, mother/minor daughter is 1.49, and major/minor is 1.21. These are not LM-specific.
- **Expected CGPS range.** The atlas population (CAC 0, no stenosis, mean age 55) is close to the CGPS plaque-free baseline, so its CTA numbers are the most relevant benchmark. Expect LAD/LCx median of about 1.05–1.10 with an LCx > LAD share that is not small (overlapping SDs of 0.7 mm). Expect LM/LAD around 1.1–1.25, depending on how far from the carina the diameters are sampled.

### Gaps
- No large CCTA cohort was found that reports per-person LM/LAD and LM/LCx ratio distributions (mean, SD, percentiles). Only diameter means are available, so the SD of the ratios is unknown.
- No Scandinavian or Danish normal coronary diameter reference was found.

## 3. Correlates of the ratios, mapped to CGPS variable availability

### Takeaway
Absolute diameters scale with sex and body size; ratios should largely cancel these. The correlate most likely to shift the LM/LCx and LAD/LCx ratios is dominance, with a larger LCx in left dominance. An intermediate artery (ramus) changes the angle but, in the atlas, not the LM diameter. LVH enlarges diameters. Age and tortuosity had no effect on diameter in Dodge.

### Cited Findings
- **Dominance.** LCx (and RCA) diameter depends on dominance; LAD does not. — [Dodge 1992](https://www.ahajournals.org/doi/10.1161/01.cir.86.1.232). A 16-slice CTA study of 104 normal adults found proximal LCx differed in left-dominant hearts versus balanced and right-dominant (no difference between those two). The direction was not visible in the snippet. — [HKU CTA study](https://hub.hku.hk/handle/10722/92210). Left dominance is about 8–10% in CT and angiography cohorts. — [Coronary dominance on CCTA](https://pmc.ncbi.nlm.nih.gov/articles/PMC13363422/)
- **Sex.** In CTA, males have larger LM, LAD and LCx (for example LM 4.1 vs 3.3 mm). — [Medrano-Gracia 2016](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy). Women's diameters are 9% smaller even after BSA normalisation. — [Dodge 1992](https://www.ahajournals.org/doi/10.1161/01.cir.86.1.232). In the atlas, sex ratios of LM:LAD:LCx were similar in both sexes (my arithmetic, Section 2).
- **Body size.** In the CTA atlas, diameters were not significantly related to body size (BMI/height regression). — [Medrano-Gracia 2016](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy). BSA indexing removed the sex difference in an Indian cohort. — [Indian cohort](https://www.sciencedirect.com/science/article/pii/S0019483216302668)
- **Age.** No effect on lumen diameter. — [Dodge 1992](https://www.ahajournals.org/doi/10.1161/01.cir.86.1.232)
- **Intermediate artery (trifurcation).**
  - LM bifurcation angle B is 89 ± 21° with an intermediate artery and 75 ± 23° without (p < 0.001), but LM diameter does not differ.
  - With an intermediate artery, LAD and LCx are slightly smaller (for example females 2.7 / 2.6 vs 3.0 / 2.8 mm), consistent with flow splitting three ways.
  - About 74 of 300 normal CTA patients (about 25%) had an intermediate artery.

  — [Medrano-Gracia 2016](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)
- **LV mass/LVH.** Diameters about 17% larger in LVH from aortic stenosis (n = 6), and about 12% larger in dilated cardiomyopathy (n = 7). — [Dodge 1992](https://www.ahajournals.org/doi/10.1161/01.cir.86.1.232)
- **Hypertension and diabetes.** No primary source was found on their effect on LM/LAD or LM/LCx ratios in plaque-free arteries.

### Correlates mapped to CGPS availability

| Correlate | Expected effect on ratios | Available in CGPS? |
|---|---|---|
| Dominance | Left dominance: larger LCx, so LM/LCx down and LAD/LCx down | Yes (`ct_cag` dominance, BL and FU) |
| Sex | Absolute diameters smaller in women; ratios about unchanged | Yes (`male`) |
| Body size | Weak or absent effect on CTA diameters; ratios about unchanged | Yes (height, weight, BMI, BSA) |
| Age | No effect on diameter (Dodge) | Yes (`scan_age`) |
| Intermediate artery | Smaller LAD and LCx relative to LM, wider angle | Not a tabular variable. The `im` segment read columns (`ct_cag_im_*`) indicate whether it was assessed. It can also be derived from centerlines and CT. |
| LV mass/LVH | Larger diameters | Not in the tables. Could be derived from the CT volumes (LV myocardium segmentation). |
| Hypertension | Unknown | Antihypertensive medication and BP at BL; derived hypertension at FU only |
| Diabetes | Unknown | Yes (`diabetes`, HbA1c) |
| Lipids, eGFR, smoking, SCORE2 | Unknown | Yes |
| Nitro | Vasodilation enlarges diameters, possibly unequally | FU only (`nitro` scan parameter). BL nitro use is not in the headers. |
| Image quality | Affects measurement noise | Yes (BL `scan_qualitative_quality`, `bad_quality`) |

### Inferences
- **Stratifying validation checks.** Dominance is the one strong, physiologically expected correlate of LCx-based ratios that is available. A check that LM/LCx and LAD/LCx are lower in left-dominant scans is a direction-of-effect check (small n: about 8–10% of 1,801 is roughly 150).
- **Sex and body size as checks on the ratios.** A strong sex or BSA effect on the ratios, as opposed to on absolute diameters, would be unexpected and could signal a resolution-dependent bias. Small vessels lose more relative diameter to partial-volume blur.

### Gaps
- No study was found that quantifies dominance-stratified LM/LCx ratios on CTA.
- No study was found on hypertension, diabetes or smoking effects on bifurcation ratios in normal arteries.
- The association of BL nitro administration with ratios cannot be assessed: BL nitro is not available.

## 4. Distortion by plaque and remodelling, sampling location, and contour method

### Takeaway
Plaque distorts the ratios in both directions:
- Positive (Glagov) remodelling preserves or enlarges the lumen up to about 40% plaque burden.
- Diffuse LM disease shrinks the LM lumen uniformly by about 1.2 mm, invisible without a reference.
- Calcification is associated with deviation from Murray's law.

Ratios are therefore valid as "normal geometry" only in plaque-free trees. Diameters must be sampled outside the bifurcation flare, where the confluence area is up to about 1.4× eccentric and Dmax is about 5.2 mm. Area-equivalent and minimum diameters differ systematically.

### Cited Findings
- **Glagov remodelling.** Glagov et al. 1987 (NEJM 316:1371), 136 autopsy LM sections: arteries enlarge in relation to plaque area, and lumen narrowing may be delayed until plaque occupies about 40% of the IEL area. — [Glagov 1987](https://insight.jci.org/references/scholar/6633/B1). Later IVUS work shows both compensatory enlargement and paradoxical shrinkage. — [PMC1728600](https://pmc.ncbi.nlm.nih.gov/articles/PMC1728600)
- **Diffuse LM disease, Motreff et al. 2010 (EuroIntervention 5:709).** 52 patients with QCA and IVUS. Of 38 angiographically normal LMs, 10 had diffuse disease on IVUS (plaque burden > 40% along the whole LM). Conventional QCA stenosis was 4%, versus 31% when the reference LM diameter came from Finet's law applied to LAD + LCx. Diffuse atheroma made LM diameter underestimated by about 1.2 mm on average. — [Motreff 2010](https://eurointervention.pcronline.com/article/diffuse-atherosclerotic-left-main-coronary-artery-disease-unmasked-by-fractal-geometric-law-applied-to-quantitative-coronary-angiography-an-angiographic-and-intravascular-ultrasound-study/pdf)
- **Murray deviation and calcification, Schoenenberger et al. 2012 (Atherosclerosis 221:124, IVUS).** A higher Murray ratio (deviation) was associated with more dense calcium proximal (F = 5.93, p = 0.016) and distal (F = 5.16, p = 0.024) to bifurcations, after adjustment for risk factors. — [PubMed 22261173](https://www.ncbi.nlm.nih.gov/pubmed/22261173); [unibe repository](https://boris.unibe.ch/7539)
- **CTA, Chen et al. 2020 (Comput Methods Biomech Biomed Eng).** Bifurcations with CAD deviate further from optimal (Murray-type) structure; left CAD trees deviated most and non-CAD right trees least. — [Chen 2020](https://ideas.repec.org/a/taf/gcmbxx/v24y2020i7p740-752.html)
- **Sampling location.** The normal CTA atlas shows:
  - Area-equivalent diameter briefly increases in the confluence polygon, which they fit with an ellipse: Dmax 5.2 vs Dmin 3.6 mm, eccentricity 1.4.
  - LAD diameter fluctuates at bifurcations and then stabilises, with about 0.25 mm per 10 mm taper.
  - Angles were averaged over 5–10 mm from the bifurcation point for robustness.

  — [Medrano-Gracia 2016](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)

  Finet used IVUS lumen areas over the first 5 mm after the bifurcation for the daughters, and QCA reference segments adjacent to the bifurcation without neighbouring side branches. — [Finet 2008](https://eurointervention.pcronline.com/article/fractal-geometry-of-arterial-coronary-bifurcations-a-quantitative-coronary-angiography-and-intravascular-ultrasound-analysis)
- **Modality and contour method.**
  - QCA underestimates IVUS by about 4–5.5% in the LM, LAD and LCx. — [Finet 2008](https://eurointervention.pcronline.com/article/fractal-geometry-of-arterial-coronary-bifurcations-a-quantitative-coronary-angiography-and-intravascular-ultrasound-analysis)
  - IVUS is 11.4% larger than QCA in a diseased LM. — [ABC Cardiol 2025](https://new.scielo.br/j/abc/a/x4td9RRjsfcNcF9kcHtjf9n/?lang=en)
  - CTA LM IQR (3.2–4.1 mm) matches QCA, but post-mortem measurements are 4.9 mm. — [Medrano-Gracia 2016](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)

### Inferences
- **Effect of plaque on ratios.** Plaque in the LM (diffuse narrowing) lowers LM/LAD and LM/LCx. Plaque in a proximal daughter with positive remodelling may preserve or even raise the daughter's lumen. The plaque group (about 600 CGPS scans) should therefore show wider scatter and a shift in the ratios. That makes it a useful contrast, not a validation set for "normal" ratios.
- **Elliptical lumen.** With an eccentric lumen (eccentricity about 1.4 at the confluence), the minimum diameter is about 15–30% below the area-equivalent diameter near the carina. Ratios mixing the two, or sampling inside the flare, will be biased. Sampling about 3–5 mm (LM: midshaft or just proximal to the flare) and 5–10 mm into each daughter, with area-equivalent diameters, is consistent with the atlas and Finet protocols.
- **Partial volume.** Partial-volume blur on CT inflates small-lumen diameters proportionally more. LCx (the smaller daughter) and female or small vessels would show ratios biased towards 1.

### Gaps
- No study was found that quantifies how LM/daughter ratios change with distance from the carina on CTA (only the diameter-vs-depth curves in the atlas figures).
- No direct CTA comparison was found of area-equivalent versus minimum-diameter-based scaling exponents.

## 5. Which relations are robust enough to validate a diameter-extraction method?

### Takeaway
Robust checks on plaque-free scans:
- the fitted exponent should centre near 2.3–2.5;
- the Finet ratio should be about 0.66 ± 0.08;
- LM > LAD ≥ LCx on average, with LAD/LCx about 1.05–1.10;
- absolute area-equivalent diameters should match the CTA atlas (LM about 3.5, LAD about 3.2, LCx about 3.0 mm), with men about 20% larger;
- ratios should be roughly sex-invariant.

Directional checks: left dominance gives a larger LCx, and an intermediate artery gives smaller daughters. Agreement with Medis diameters on the same scans is the only direct check. Laws alone cannot validate individual measurements, given ±0.8–1 mm per-case scatter.

### Cited Findings
- Pooled exponent 2.39 (CI 2.24–2.54) but I² = 99%, which shows large heterogeneity across studies and methods. — [PubMed 38787386](https://pubmed.ncbi.nlm.nih.gov/38787386/)
- Normal CTA: exponent fit 2.4, Finet ratio 0.6576 ± 0.083. — [Medrano-Gracia 2016](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)
- Per-case prediction of LM diameter from LAD + LCx has precision of about 0.8–0.96 mm for all three laws. — [ABC Cardiol 2025](https://new.scielo.br/j/abc/a/x4td9RRjsfcNcF9kcHtjf9n/?lang=en)
- HK is accurate across all Ds/Dl. Finet is valid only at Ds/Dl ≥ 0.75. — [Huo et al., EuroIntervention](https://eurointervention.pcronline.com/article/optimal-diameter-of-diseased-bifurcation-segment-a-practical-rule-for-percutaneous-coronary-intervention)

### Inferences
- **Cohort-level checks, by robustness:**
  1. The sex difference in absolute diameter: well replicated (QCA and CTA).
  2. The distribution of the exponent or Finet ratio on plaque-free LM bifurcations: centre about 2.4 / about 0.66; reject if the median exponent is below 2 or above 3.5 under a near-carina protocol.
  3. Absolute diameters within atlas IQRs.
  4. The LCx dominance effect: direction only.
  5. Plaque-group ratios more dispersed than plaque-free ratios.
- **What is not a validation target.** Per-person agreement with any law: expected residuals of about ±12% (Finet SD 0.083 on 0.66) are as large as plausible extraction errors. Medis contours exist only for diseased segments, and Medis trees exist only for the 600 plaque scans. Direct diameter validation against Medis is therefore confined to diseased anatomy, where remodelling complicates agreement.
- **Choosing the law for ratios near 1.** For LAD/LCx ratios near 1 (Ds/Dl ≥ 0.75, the common LM case), Finet, HK and Murray coefficients differ only by 0.634–0.678. Distinguishing the laws needs very precise diameters. Validation should use HK (exponent 7/3) as the expected value, not attempt to discriminate between laws.

### Gaps
- No published LM-specific CTA scatter of per-bifurcation exponents was found to set formal acceptance limits.
- No reproducibility data (interobserver or scan–rescan) for CTA LM/LAD/LCx diameter ratios were found.
