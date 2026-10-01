# Diameter / radius scalars as predictors of CAD, ischemia, plaque and outcomes (coronary CTA focus)

Research scope note: 17 tool calls; several publisher pages (JACC, RSNA, AHA, PubMed) returned 403/reCAPTCHA, so some items are abstract/snippet-level only and flagged as such. Nothing below is from memory unless placed under Gaps.

## Q1. Which diameter/radius scalars appear in the literature, with definitions, studies, outcomes and effect sizes?

### Takeaway
The scalars that recur on CCTA are: proximal and distal diameter, lumen volume, lumen volume per vessel length (V/L), lumen volume per myocardial mass (V/M, CAVi), minimum lumen area (MLA) and composites with it, percent diameter stenosis, and scaling-law exponents of area vs. length/volume. The strongest single *size-type* scalar found was V/L in the RCA (AUROC 0.88 for FFR-CT <= 0.80); V/M-type indices sit at AUROC ~0.71 to 0.78 for ischemia. No CCTA study was found that used a taper slope (d radius / d arc length) or diameter SD/CoV as a standalone predictor with a reported AUROC.

### Cited Findings

Catalogue (scalar | definition | study | outcome | performance):

- **Proximal RCA diameter, distal RCA diameter, RCA lumen volume, RCA length, V/L ratio** | V/L = RCA lumen volume / RCA length (mm^3/mm), measured ostium (#1) to crux (#3 distal end), side branches excluded | Tsugu T, Tanaka K, Belsack D et al., Eur Radiol 2023, n = 443 non-obstructive patients (60 with FFR-CT <= 0.80) | distal FFR-CT (continuous) and FFR-CT <= 0.80 | Univariable correlation with distal FFR-CT: V/L r = 0.61, lumen volume r = 0.42, distal diameter r = 0.37, proximal diameter r = 0.36, vessel length r = -0.22 (all p < 0.0001). Multivariable linear model for distal FFR-CT: calcified plaque volume beta = -0.12 (p = 0.01), V/L beta = 0.48 (p = 0.03), proximal diameter beta = 0.09 (p = 0.04). V/L for FFR-CT <= 0.80: cut-off 8.1 mm^3/mm, AUROC 0.88 (95% CI 0.84 to 0.93), sensitivity 90.0%, specificity 76.7%. Covariates considered included age, sex, BSA, blood pressure and LV mass index; results given as beta coefficients, not ORs. — [Tsugu et al. 2023, PMC10873436](https://pmc.ncbi.nlm.nih.gov/articles/PMC10873436/)
- Same paper: lumen cross-sectional area decreases distally (taper) and correlates with FFR-CT; higher nitroglycerin dose increases lumen volume and raises distal FFR-CT (i.e. the diameter scalars are acquisition-sensitive). — [search snippet of PMC10873436](https://pmc.ncbi.nlm.nih.gov/articles/PMC10873436/)
- **V/M (total epicardial lumen volume / LV myocardial mass, mm^3/g)** | patient-level | Taylor CA et al., J Cardiovasc Comput Tomogr 2017, NXT trial, 238 patients, 438 vessels with invasive FFR, nitroglycerin given | invasive FFR | Median V/M 18.57 mm^3/g split the cohort; hypothesis and reported finding: low V/M associated with lower FFR. Exact effect sizes not retrieved (PubMed blocked). — [PubMed 28789941](https://pubmed.ncbi.nlm.nih.gov/28789941), [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1934592517301697)
- **CAVi (coronary artery lumen volume index = total lumen volume / LV mass)** | Benetos G et al., Eur Radiol 2021, 60 patients / 180 vessels | 13N-ammonia PET stress MBF, MFR, ischemia | Correlation with global stress MBF R = 0.50, global MFR R = 0.39, regional stress MBF R = 0.47, regional MFR R = 0.36. AUROC 0.758 for abnormal stress MBF, 0.711 for ischemia; ROC cut-off 20.2 mm^3/g. Independently associated with abnormal stress MBF in multivariable model: OR 0.90 per unit (95% CI 0.82 to 0.998, p = 0.045). — [Benetos et al. 2021, PMC8213544](https://pmc.ncbi.nlm.nih.gov/articles/PMC8213544/)
- **Vsub/MLA^2 and vessel-specific VR/MR** | subtended myocardial mass (Vsub) over squared MLA; vessel-specific lumen volume / fractional myocardial mass | JACC Cardiovasc Imaging 2017 (Kim/Koo group, "Incremental value of subtended myocardial mass") and a later VR/MR paper | FFR <= 0.80 | Vsub/MLA^2 > 4.16 was the best single parameter, sensitivity 83.3%, specificity 67.9%. VR/MR: accuracy 87%, sensitivity 77%, specificity 92%. Patient-level V/M with cut-off in one cohort: accuracy 60%, sensitivity 45%, specificity 76%. Search-snippet level only; attribution between these papers not verified. — [JACC CI 2017](https://www.jacc.org/doi/full/10.1016/j.jcmg.2017.10.027), [PubMed 34238054 (VR/MR)](https://pubmed.ncbi.nlm.nih.gov/34238054/)
- **V/M combined with %DS and FFR-CT**: AUC 0.80 (95% CI 0.76 to 0.85) for %DS + V/M + FFR-CT vs 0.78 (0.74 to 0.83) for V/M alone. Snippet-level, originating paper in the V/M result set not pinned down. — [search results set incl. PMC11865212](https://pmc.ncbi.nlm.nih.gov/articles/PMC11865212)
- **V/M for acute coronary syndrome risk** and **V/M in TAVR** and **V/M in microvascular angina**: V/M has been extended to ACS risk stratification, TAVR outcomes and primary microvascular angina (low V/M associated with severe CAD, lower MBF, FFR <= 0.80). — [Frontiers 2025, PMC11865212](https://pmc.ncbi.nlm.nih.gov/articles/PMC11865212), [TAVR, PMC12020294](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12020294/), [microvascular angina, PubMed 28993120](https://pubmed.ncbi.nlm.nih.gov/28993120/), [JCCT 2024 severe CAD](https://www.journalofcardiovascularct.com/article/S1934-5925(24)00379-4/fulltext)
- **Scaling power-law exponents (mean lumen CSA and summed intravascular volume vs. length)** | Huo/Kassab group, Radiology 2013 "CT-based diagnosis of diffuse coronary artery disease on the basis of scaling power laws" | discriminated metabolic-syndrome patients from controls (diffuse disease) | numbers not retrieved (403). — [Radiology 2013](https://doi.org/10.1148/radiol.13122181)
- **Murray's-law deviation at bifurcations** | ratio of parent to daughter diameters vs. cube law | deviation associated with a higher degree of calcification in coronary bifurcations. Meta-analysis exists on whether coronaries obey Murray's law. — [PubMed 22261173](https://pubmed.ncbi.nlm.nih.gov/22261173/), [meta-analysis PMC11380967](https://pmc.ncbi.nlm.nih.gov/articles/PMC11380967/), [Frontiers Physiol 2022, PMC9119389](https://pmc.ncbi.nlm.nih.gov/articles/PMC9119389/)
- **Plaque diffuseness (not a diameter scalar, but length-normalised)** | sum of contiguous lesion lengths / total vessel length | each unit increase in log % plaque diffuseness gave 58% higher odds of abnormal FFR, independent of stenosis and plaque characteristics. — [PubMed 28168977](https://pubmed.ncbi.nlm.nih.gov/28168977/)
- **AI-QCT ischemia model (integrates stenosis, MLA-type and vascular morphology measures with plaque)** | Nurmohamed/CREDENCE & PACIFIC-1, JACC CI 2024 | invasive FFR ischemia | per-patient AUC 0.80 (0.75 to 0.85) vs FFR-CT 0.69 in CREDENCE (n = 305); 0.85 vs FFR-CT 0.78 in PACIFIC-1 (n = 208); vessel-level AUC 0.86 in both; positive test aHR 7.6 (1.2 to 47.0) for MACE. Per-feature contribution of the diameter terms not retrieved. — [JACC CI 2024](https://www.jacc.org/doi/10.1016/j.jcmg.2024.01.007)

### Inferences
- Among pure size scalars, length- or mass-normalised lumen volume (V/L, V/M) consistently outperforms raw diameters (Tsugu: r 0.61 for V/L vs ~0.36 for single diameters). For a per-vessel RCA regression, **mean lumen area along the centerline (= V/L)** is the closest literature-backed scalar to "mean radius": V/L = mean cross-sectional area, i.e. approximately pi * mean(r^2).
- The Tello Ayala-style fairness argument (mean absolute curvature vs full profile) maps naturally to **mean radius (or mean area = V/L)** as the size scalar, with **proximal diameter** as a secondary landmark scalar that survived multivariable adjustment in Tsugu.
- Min-radius / %stenosis-type scalars are stenosis-specific and would give the LR baseline lesion information the curvature arm lacks; if included, the comparison is no longer "global mean vs profile" symmetric.

### Gaps
- No CCTA study found reporting AUROC for **taper slope** (radius vs arc length regression) or **diameter SD / CoV / lumen irregularity index** as a standalone predictor of CAD or FFR. "Mohiaddin/Zhou taper" could not be located.
- Exact effect sizes for Taylor 2017 NXT V/M, the JACC CI 2017 Vsub/MLA^2 paper and Huo 2013 scaling laws could not be read (403 / reCAPTCHA).
- Classical MLD / MLA / %DS AUROCs vs invasive FFR (e.g. DeFACTO, NXT, DISCOVER-FLOW) were not retrieved in this pass; from memory these are typically ~0.6 to 0.7 for %DS but this is unverified.
- No sources found for WSS-outcome studies using diameter scalars on CCTA in this pass.

## Q2. Which scalars predicted FFR-CT <= 0.80 or CAD independently in multivariable models?

### Takeaway
Independent after adjustment: V/L and proximal diameter for distal RCA FFR-CT (Tsugu 2023); CAVi for abnormal PET stress MBF (Benetos 2021, OR 0.90); log plaque diffuseness for abnormal FFR. Raw distal diameter and lumen volume did not survive Tsugu's multivariable model.

### Cited Findings
- Tsugu 2023 multivariable (distal FFR-CT): calcified plaque volume beta -0.12 (p = 0.01), V/L beta 0.48 (p = 0.03), proximal diameter beta 0.09 (p = 0.04); age, sex, BSA, BP, LV mass index were candidate covariates and not all were independent. Distal diameter, lumen volume and length were not retained. — [PMC10873436](https://pmc.ncbi.nlm.nih.gov/articles/PMC10873436/)
- Benetos 2021: CAVi OR 0.90 (0.82 to 0.998, p = 0.045) for abnormal stress MBF in multivariable model. — [PMC8213544](https://pmc.ncbi.nlm.nih.gov/articles/PMC8213544/)
- Low V/M associated with lower FFR in non-obstructive CAD "independent of plaque measures". — [search result summary of V/M literature, e.g. PMC11865212](https://pmc.ncbi.nlm.nih.gov/articles/PMC11865212)
- Plaque diffuseness: +58% odds of abnormal FFR per unit log % diffuseness, independent of stenosis severity and APCs. — [PubMed 28168977](https://pubmed.ncbi.nlm.nih.gov/28168977/)
- Tello Ayala et al. 2026 (angiography, 22,334 patients, 38,691 RCA angiograms, MGH 2000 to 2021): LR covariates were age, sex, hypertension, diabetes, hypercholesterolemia, smoking + global tortuosity; **no radius/diameter scalar was included**. Transformer on local curvature + age + sex AUROC 0.67 (0.65 to 0.69) vs LR on global score 0.60 (0.58 to 0.63). — [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)

### Inferences
- Because Tello Ayala used no diameter scalar, any diameter scalar in the thesis LR is a design choice with no direct precedent in that paper; V/L (mean area) and proximal diameter are the most defensible by Tsugu's RCA-specific multivariable result, which also shares the thesis' RCA focus and CCTA modality.
- Outcome mismatch: Tsugu/Benetos predict ischemia (FFR-CT / PET), not a CAD label; ImageCAS-X's Disease column is closer to an anatomical CAD label, so effect sizes will not transfer directly.

### Gaps
- No multivariable CCTA result found for taper or diameter variability.
- No explicit OR for proximal diameter or V/L in Tsugu (linear betas only).

## Q3. Has anyone compared a scalar diameter summary against a model reading the full diameter/lumen profile?

### Takeaway
Closest evidence: Hampe et al. 2022 feed per-centerline-point lumen area (plus attenuation, calcium, bifurcation flags) to a 1D CNN + transformer and report artery-level AUC 0.78 (regression-only 0.83) for invasive FFR; ablating the lumen-area channel dropped AUC to 0.72 (p = 0.039). They did not run a scalar-summary baseline (e.g. mean area, MLA, %DS) on the same test set, so the scalar-vs-profile gap for diameter is not directly quantified. For curvature, Tello Ayala's gap is 0.07 AUROC (0.67 vs 0.60).

### Cited Findings
- Hampe N, van Velzen SGM, Planken RN, Henriques JPS, Collet C, Aben J-P, Voskuil M, Leiner T, Išgum I. Front Cardiovasc Med 2022. 569 patients, 3 hospitals; FFR in 514 arteries of 369 patients, 200 CAD-RADS 0 to 1 patients. Stage 1: 2D CNN on MPR cross-sections -> per-point lumen area, attenuation, calcium area; plus per-point bifurcation and main-branch flags. Stage 2: 1D CNN + transformer, FFR regression + classification. TestCath (76 arteries) AUC 0.78 merged, 0.83 regression alone. Removing lumen area: AUC 0.72 (p = 0.039); removing calcium or attenuation had smaller effect. No direct comparison with anatomical stenosis degree. — [Frontiers 2022](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2022.964355/full), [PubMed 36457806](https://pubmed.ncbi.nlm.nih.gov/36457806/)
- The same group argues clinical scalar indices (TAG, plaque volume, %stenosis, CDD) "limit the capability to model the complex relationship between FFR and coronary artery characteristics". This is an argument, not a measured gap. — [Frontiers 2022](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2022.964355/full)
- Related: transformer network for significant stenosis detection in CCTA (MICCAI 2021) reads the vessel as a sequence. — [arXiv 2107.03035](https://arxiv.org/abs/2107.03035)
- Tello Ayala 2026: profile (local curvature array) vs scalar (mean abs curvature): 0.67 vs 0.60 AUROC. — [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)

### Inferences
- The Hampe ablation (0.78 -> 0.72) shows the lumen-area profile carries information beyond attenuation/calcium, but says nothing about whether a scalar of that profile would suffice. A thesis LR on mean radius vs sequence model on radius profile would itself be a novel scalar-vs-profile comparison for diameter.

### Gaps
- No functional data analysis (FDA) of lumen area curves vs scalar summaries on CCTA was found in this pass.
- No IVUS profile-vs-scalar comparison was found in this pass.

## Q4. How do studies normalise diameter for body/heart size?

### Takeaway
Three approaches: (1) index to LV myocardial mass (V/M, CAVi; also subtended mass per vessel); (2) index to vessel length (V/L, i.e. mean area); (3) BSA and sex as covariates or BSA-indexed norms. Correlations of coronary size with BSA and myocardial mass are statistically significant but weak, and women have ~9% smaller arteries even after BSA indexing, so sex remains necessary.

### Cited Findings
- V/M and CAVi normalise total lumen volume by LV mass (Taylor median 18.57 mm^3/g; Benetos ROC cut-off 20.2 mm^3/g, mean LV mass 113.3 +/- 37.4 g). — [PMC8213544](https://pmc.ncbi.nlm.nih.gov/articles/PMC8213544/), [PubMed 28789941](https://pubmed.ncbi.nlm.nih.gov/28789941)
- Vessel-specific normalisation by subtended / fractional myocardial mass (VR/MR, Vsub/MLA^2). — [PubMed 34238054](https://pubmed.ncbi.nlm.nih.gov/34238054/), [JACC CI 2017](https://www.jacc.org/doi/full/10.1016/j.jcmg.2017.10.027)
- Tsugu normalises lumen volume by vessel length (V/L) and entered BSA and LV mass index as covariates. — [PMC10873436](https://pmc.ncbi.nlm.nih.gov/articles/PMC10873436/)
- In angiographically normal coronaries on MDCT, correlations between BSA or myocardial mass and coronary dimensions were significant but weak; reference values given by sex and dominance for proximal and mid segments. — [JCCT, Volume and dimensions of angiographically normal coronary arteries by MDCT](https://www.sciencedirect.com/science/article/abs/pii/S1934592517300862)
- Women have ~9% smaller epicardial diameters than men even after BSA normalisation (search summary; primary source attribution not verified). — [search result set incl. AJR 2011 and Dodge 1992](https://www.ahajournals.org/doi/pdf/10.1161/01.cir.86.1.232)
- Dodge et al. 1992 Circulation "Lumen diameter of normal human coronary arteries" (angiography) is the classical reference for segment diameters by sex, dominance and heart size; full text blocked (403). — [Circulation 1992](https://www.ahajournals.org/doi/pdf/10.1161/01.cir.86.1.232)
- Example normal CT values (Indian cohort): LM 4.08 +/- 0.44 mm, proximal LAD 3.27 +/- 0.23, proximal RCA 3.20 +/- 0.37, proximal LCx 2.97 +/- 0.37 mm. — [PubMed 28822520](https://pubmed.ncbi.nlm.nih.gov/28822520/)
- Sex-specific, BSA-normalised CTA reference values exist for chambers, aorta and PA (not coronaries). — [AJR 2011](https://www.ajronline.org/doi/10.2214/AJR.10.4990), [AJR 2012](https://www.ajronline.org/doi/10.2214/AJR.11.6945)

### Inferences
- ImageCAS-X has no BSA or LV mass readily available (to check), so the practical normalisation options are: ratio to the vessel's own proximal reference diameter (dimensionless), include sex/age as covariates (as Tello Ayala does), or compute LV mass from the CT if a myocardium segmentation exists.
- Ratio-to-proximal (e.g. distal/proximal radius, or taper slope divided by proximal radius) removes body-size scale without external covariates and is the only size-free option available from the centerline data alone.

### Gaps
- No allometric-scaling exponent for coronary diameter vs BSA was found.
- Dodge 1992 regression equations could not be read.
- ImageCAS-X covariate availability (sex, age, BSA) not checked here.
