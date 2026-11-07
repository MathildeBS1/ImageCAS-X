# Clinical/imaging evidence that segment-level coronary geometry (beyond curvature, taper, LM bifurcation angle, LM daughter ratios) predicts plaque location, development or progression in humans

Scope note: 16 tool calls. Several full texts returned HTTP 403 (ScienceDirect, AHA journals), so some entries rest on abstracts or search summaries. They are marked. Earlier notes (`research_notes/Fourth centerline feature for plaque/predictive_evidence_ranking.md`, `reports/Geometric features for plaque prediction.md`, `reports/Coronary geometry known correlates.md`) already cover these: ICONIC adverse geometric characteristics (Han 2022), Wang 2004 distance from ostium, V/M ratio, Li 2011 tortuosity, Kashyap/Gharleghi CFD, and the PREDICTION PPV of 41%. They are repeated here only where needed. This file concentrates on what is new.

Overall bottom line: I found **no human study in which a purely geometric, segment-level feature, measured on a plaque-free baseline CCTA, predicted incident plaque after adjustment for anatomical position and risk factors.** The prospective geometric evidence is of three kinds. (a) It is lesion-level and event-based, in diseased or ACS patients (ICONIC, EMERALD, PROSPECT-ESS). (b) It comes from invasive serial imaging in diseased vessels (PREDICTION, Samady, Hartman). (c) It comes from serial CCTA in selected plaque-free segments using radiomics, not interpretable geometry (myocardial-bridge radiomics, PARADIGM radiomics).

## 1. Which geometric features have prospective evidence for where plaque develops (ideally in initially plaque-free segments)?

### Takeaway
Only two settings come close to "baseline plaque-free segment → later plaque" in humans. One is the segment just proximal to an LAD myocardial bridge, in a retrospective serial-CCTA study with a radiomics model. The other is a PARADIGM radiomics study of plaque-free segments. In both, the predictive gain came from texture or radiomics features, not from named geometric features, and the clinical/anatomical model alone performed poorly (external AUC 0.56). The other candidates (side-branch angle, side-branch count, LM length, eccentricity, ramus, take-off) have only cross-sectional or old autopsy/angiographic support.

### Cited Findings
**Myocardial bridging (MB): segment proximal to the bridge**
- Chen YC et al., Eur Heart J Cardiovasc Imaging 2024;25(10):1462–1471. Multicentre **retrospective** serial-CCTA study of patients with LAD MB and **no proximal plaque at index CCTA**. n = 295: 192 development (Jinling Hospital, 8:2 train/test) and 103 external validation (4 hospitals). The outcome was plaque developing proximal to the MB on follow-up CCTA. The follow-up interval was not given in the abstract. — [PubMed 38781436](https://pubmed.ncbi.nlm.nih.gov/38781436)
  - Radiomics model of the proximal MB cross-section: AUC 0.78 (train), 0.75 (internal test), 0.75 (external). The **clinical + anatomical model: AUC 0.56 externally**. Adding radiomics raised the AUC to 0.75 (P = 0.002; NRI 0.76, IDI 0.17). The abstract does not name the individual anatomical predictors (bridge length or depth). — [PubMed 38781436](https://pubmed.ncbi.nlm.nih.gov/38781436)
- A companion "mechanomics" study is also retrospective: two CCTAs >3 months apart, machine learning. Patients with high mechanomics scores more often developed proximal plaque. — [PMC11839342](https://pmc.ncbi.nlm.nih.gov/articles/PMC11839342/)
- In a long-term follow-up study, 93.8% of plaques in segments shared with a bridge sat **proximal** to the bridge, and annualised MACE did not differ meaningfully between bridge and no-bridge groups. — [Sci Rep 2025](https://www.nature.com/articles/s41598-025-13939-8)
- MB closer to the LAD ostium was associated with abnormal pericoronary fat attenuation. This is cross-sectional, and the hemodynamic link is the authors' speculation. — [Sci Rep 2024](https://www.nature.com/articles/s41598-024-55005-9)
- An ATVB paper titled "Myocardial Bridge and the Progression of Atherosclerotic Plaque in the Proximal Segment" exists, but its full text returned 403, so its design and effects are not verified here. — [ATVB 10.1161/ATVBAHA.118.311065](https://www.ahajournals.org/doi/10.1161/ATVBAHA.118.311065)
- A 2025 scoping review concludes that AI/radiomics MB models show moderate-to-high accuracy for proximal plaque but need prospective validation. — [PMC12470274](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12470274/)

**Plaque-free segments in serial CCTA (PARADIGM)**
- A radiomics study (J Cardiovasc Comput Tomogr 2024) selected **segments without plaque at baseline**. It compared Cox models with clinical risk factors, radiomic features and both. About 9.8% of segments developed new plaque (TPV ≥ 1 mm³ at follow-up), and adding radiomics improved prediction. The full text (403) was not read, so C-statistics, n and the inclusion of geometric covariates are unverified. — [JCCT S1934592524000327](https://www.sciencedirect.com/science/article/abs/pii/S1934592524000327)
- PARADIGM sub-analysis (EHJ-CVI 2026 supplement, **conference abstract**). n = 1,343 analysed of 2,252 people with suspected CAD (a referral population); 334 (24.9%) had no baseline plaque. Median interscan interval was 3.3 y (≥ 2 y). New lesions appeared in **35% without baseline plaque** vs 46.7% with it. Where there was no baseline plaque, new lesions were most often in the **LAD (60%)**; with baseline plaque, in the RCA (47%). Adjusted predictors of new lesions: baseline plaque OR 1.84 (1.38–2.46), diabetes OR 1.38 (1.03–1.85), BMI OR 1.04/kg·m⁻² (1.01–1.08). **No geometric predictors were reported.** — [EHJ-CVI abstract](https://academic.oup.com/ehjcimaging/article/27/Supplement_1/jeaf367.317/8446296)
- PARADIGM case-control (n = 402, no baseline plaque, retrospective): HbA1c was independently associated with rapid progression. No geometric predictors. — [PMC9655903](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9655903/)

**Side-branch take-off angle and side branches**
- The evidence here is almost entirely about **PCI side-branch occlusion** (CT bifurcation score, RESOLVE, CT-PRECISION), not plaque development. The SCCT consensus notes that no dedicated CCTA bifurcation software exists. — [PMC10351068](https://pmc.ncbi.nlm.nih.gov/articles/PMC10351068); [PMC7806530](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7806530/); [J Clin Med 2026 review](https://doi.org/10.3390/jcm15124565)
- A trial registration (NCT04185493) states that larger side-branch take-off angles "have been associated with increased plaque burden". This is a background claim in a registry entry, not a result. — [ClinicalTrials.gov NCT04185493](https://clinicaltrials.gov/study/NCT04185493)
- A small cross-sectional study (Hasanuddin Univ.) related bifurcation and take-off angle to stenosis degree and calcium score. Only the title was seen. — [Unhas](https://discover.unhas.ac.id/publications/the-relationship-between-coronary-artery-bifurcation-angle-and-take-off-angle-or)
- ICONIC (from the earlier note): **bifurcation involvement** (a side-branch origin within the lesion) gave HR 2.14 for ACS culprit vs nonculprit and HR 2.63 vs matched controls. This was a lesion-level, post hoc nested case-control study in patients with established plaque. — [JAMA Cardiol 2022](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)

**Left main length**
- Old studies: angiography (n = 43, 1976) found a shorter LM in patients with CAD. Autopsy (n = 204, 1976) found LAD/LCx atherosclerosis inversely related to LM length in people over 50. — [Heart 1976;38:180](https://heart.bmj.com/content/38/2/180); [Heart 1976;38:1160](https://heart.bmj.com/content/38/11/1160)
- 64-slice CT (n = 62, cross-sectional): LM length 10.6 ± 6.1 mm without LM plaque vs 11.3 ± 4.0 mm with it, so there was no short-LM effect. A larger LM **diameter** was associated with LM plaque, which is plausibly remodelling (reverse causation). — [Cademartiri, EUR repository](https://pure.eur.nl/en/publications/assessment-of-left-main-coronary-artery-atherosclerotic-burden-us/)

### Inferences
- The MB result is the closest analogue to the thesis "where" design (plaque-free segment at baseline, serial CCTA), but it shows that **explicit anatomical features did not discriminate (AUC 0.56)**. Only texture-like features did. This tempers expectations for adding more geometric features.
- The PARADIGM result that LAD dominates new plaque in plaque-free people supports keeping vessel/position in the "where" base. Geometry has to beat that.
- LM length has contradictory, small and old evidence. It is not a strong candidate.

### Gaps
- I found no prospective human study testing LAD–D1 or LCx–OM take-off angles, side-branch count/density, ramus/trifurcation, ostial take-off angle or lumen eccentricity as predictors of **incident** plaque.
- Follow-up interval, MB length/depth effects and adjusted ORs from Chen 2024 and the ATVB 2018 paper were not accessible.

## 2. Are there studies where geometry predicted *who* develops CAD (person level) beyond risk factors?

### Takeaway
None found with interpretable geometry in an asymptomatic or plaque-free population. The PARADIGM plaque-free predictors of new plaque are clinical (diabetes, BMI, HbA1c). Person-level geometry evidence is cross-sectional (V/M, tortuosity; see the earlier reports) or is about ischemia/FFR, not incident plaque.

### Cited Findings
- PARADIGM: adjusted predictors of new lesions were baseline plaque, diabetes and BMI. No geometry was tested. — [EHJ-CVI abstract](https://academic.oup.com/ehjcimaging/article/27/Supplement_1/jeaf367.317/8446296)
- ML studies on CCTA predict CAD presence, FFR or MACE. Among them, lumen-geometry features such as minimum lumen area and remodelling index gave AUC 0.797 for low FFR. These are plaque-dependent features, so they do not apply to plaque-free baselines. — [JACC CV Imaging 2020](https://www.sciencedirect.com/science/article/pii/S1936878X20308111); [ML-MACE systematic review, PMC12205263](https://pmc.ncbi.nlm.nih.gov/articles/PMC12205263/)
- V/M ratio: I found no serial-CCTA study linking baseline V/M to plaque progression or new plaque. Its evidence remains cross-sectional (see `reports/Geometric features for plaque prediction.md`). — [Leiden thesis on V/M](https://scholarlypublications.universiteitleiden.nl/access/item%3A3640299/download)
- Serial CCTA shows that plaque growth comes mostly with **outward remodelling**: +1 mm³ plaque → +0.71 mm³ vessel and −0.29 mm³ lumen. Lumen size therefore changes little early on, and a baseline lumen measure in diseased cohorts partly encodes existing plaque. — van den Hoogen et al., EHJ-CVI 2022;23(10):1336–1344, via [search summary of Leiden repository](https://scholarlypublications.universiteitleiden.nl/access/item%3A4290013/view) (secondary; verify)

### Inferences
- A person-level geometry → incident CAD result in CGPS would be novel. Absence of prior evidence is not evidence of absence, but the prior should be a small effect.

### Gaps
- No study found that tested geometry against SCORE2, PCE or another risk score for incident plaque.

## 3. Does adding many geometry features improve prediction, or do effects disappear after adjustment for position / vessel size?

### Takeaway
Mixed and indirect. In diseased-lesion studies, hemodynamic and geometric indices are strongly intercorrelated but add jointly over plaque features (EMERALD, ICONIC, PROSPECT). Absolute WSS thresholds work at population level but fail per patient (Hartman 2021). In the one plaque-free-segment study with an explicit anatomical model (MB), anatomy alone was near chance. No study explicitly showed geometric effects surviving adjustment for distance from ostium **and** vessel size in plaque-free segments.

### Cited Findings
- EMERALD (Lee JM, JACC CV Imaging 2019;12:1032–43). **Case-control**, 72 ACS patients, 216 lesions (66 culprit, 150 nonculprit) on pre-ACS CCTA. Culprits had lower FFR-CT and higher ΔFFR-CT, WSS and axial plaque stress (all p < 0.01). Cut-offs: WSS ≥ 154.7 dyn/cm², APS ≥ 1,606.6 dyn/cm². — [summary/record](https://scholars.duke.edu/individual/pub1307933/pub1307933.rdf); [EMERALD II registry](https://clinicaltrials.gov/study/NCT03591328)
- EMERALD substudy (Yang, Front Cardiovasc Med 2021): local hemodynamic indices were **significantly intercorrelated**, yet each added similar independent value for ACS over high-risk plaque and FFR-CT. Adding many correlated geometry/hemodynamic features therefore gives overlapping, not cumulative, information. — [Front Cardiovasc Med 2021](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2021.713835/pdf)
- ICONIC: adverse geometric characteristics (short distance from ostium, bifurcation, tortuosity) raised the AUC from 0.733 to 0.766 over plaque features. ≥2 AGCs gave HR 6.84. Tortuosity was rare (<5%) and underpowered. — [JAMA Cardiol 2022](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
- PROSPECT-ESS (Stone, JACC CV Imaging 2018): in nonculprit lesions of ACS patients, low ESS gave a propensity-adjusted **HR 4.34 (1.89–10.00)** for nonculprit MACE (22.8% vs 0%) at 3.4 y, beyond plaque burden, MLA and morphology. — [Mount Sinai record](https://scholars.mssm.edu/en/publications/role-of-low-endothelial-shear-stress-and-plaque-characteristics-i-2/)
- Bourantas, JACC CV Imaging 2020 (PROSPECT + IBIS-4, n = 697 ACS, **3D-QCA-derived ESS**): plaque burden HR 1.08 and maximum 3-mm ESS HR 1.11 were independent predictors of lesion-level MACE-R at 5 y. Angiography-based geometry plus a flow model added prognostic information. — [UCL Discovery PDF](https://discovery-pp.ucl.ac.uk/10116727/1/Bourantas_et_al_Shear_stress_estimated_by_QCA.pdf); [Galway record](https://research.universityofgalway.ie/en/publications/shear-stress-estimated-by-quantitative-coronary-angiography-predi/)
- Hartman et al., Sci Rep 2021 (IVUS + CT reconstructions, 10,205 sectors of 45° × 1.5 mm, calcified regions excluded). Low-WSS sectors progressed more under every low-WSS definition at population level. With measured flow, however, absolute WSS ranged so widely between patients that **absolute thresholds were inappropriate per patient**. This argues for within-person (conditional) comparisons, as in the thesis "where" design. — [Sci Rep 2021 (DOAJ)](https://doaj.org/article/868ad3401d0641db9538bbafb6bb82d8); [PMC8586146](https://pmc.ncbi.nlm.nih.gov/articles/PMC8586146)
- Hoogendoorn et al., Cardiovasc Res 2020: almost all WSS metrics had similar predictive values for plaque development (47–50%) and advanced fibrous-cap atheroma development (59–61%). Multidirectional WSS was linked to advanced plaque. — [PoliTo cvz212.pdf](https://iris.polito.it/bitstream/11583/2819197/3/cvz212.pdf)
- An Atherosclerosis 2023 paper, "Mechanical wall stress and wall shear stress are associated with atherosclerosis development in non-calcified coronary segments", is directly relevant: it is about early-stage segments. Its full text returned 403 and the authors were not confirmed, so n and effects are unverified. — [Atherosclerosis S002191502305308X](https://www.sciencedirect.com/science/article/pii/S002191502305308X)
- A preliminary CCTA-CFD study found that normalised minimum WSS (OR 0.38, p < 0.001) and maximum helicity (OR 1.44, p = 0.016) predicted progression. It is small and preliminary. — [J Cardiovasc Transl Res 2025, PMC12858539](https://pmc.ncbi.nlm.nih.gov/articles/PMC12858539/)
- Hartman 2021 also reports that the low-WSS definition matters (absolute vs vessel-relative tertiles). — [Sci Rep 2021](https://www.nature.com/articles/s41598-021-01232-3)

### Inferences
- High intercorrelation (EMERALD) plus few events implies that adding many geometric features mostly adds variance. A single prespecified geometry block (as the thesis does) is the defensible approach.
- Distance from ostium and vessel size drive much of the "where" signal (ICONIC, Wang 2004, PROSPECT). The thesis base (position + log length + dominance × vessel) already absorbs much of what most geometric features would capture.

### Gaps
- No study found reported geometry effects with and without adjustment for distance from ostium / vessel calibre in plaque-free segments.

## 4. CCTA studies using CT-derived WSS or geometry to predict plaque progression or new plaque (EMERALD, ICONIC, PARADIGM, SCOT-HEART, Danish cohorts)

### Takeaway
EMERALD and ICONIC are **retrospective case-control ACS studies on diseased lesions**, not progression or new-plaque studies. PARADIGM has serial CCTA with plaque-free segments but reports clinical and radiomic predictors, not CFD/geometry. I found no SCOT-HEART or Danish (DANCAVAS, CGPS/Copenhagen) study using geometry or WSS to predict new plaque. Invasive serial-imaging WSS studies (PREDICTION, Samady) are all in diseased, symptomatic patients.

### Cited Findings
- EMERALD and ICONIC: see section 3. Both use ACS outcomes, not plaque development. — [EMERALD record](https://scholars.duke.edu/individual/pub1307933/pub1307933.rdf); [JAMA Cardiol 2022](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
- PARADIGM new-plaque and radiomics studies: see section 1. — [EHJ-CVI abstract](https://academic.oup.com/ehjcimaging/article/27/Supplement_1/jeaf367.317/8446296); [JCCT 2024](https://www.sciencedirect.com/science/article/abs/pii/S1934592524000327)
- PREDICTION (Stone, Circulation 2012; 3D-IVUS in ACS patients, serial 6–10 months): low ESS + large plaque burden predicted progression requiring PCI, with PPV ~41% (as cited in the earlier report). — [Circulation 2012](https://doi.org/10.1161/circulationaha.112.096438)
- Samady et al., Circulation 2011: low-WSS segments developed more plaque and necrotic-core progression and constrictive remodelling than intermediate-WSS segments. This was a small serial VH-IVUS study in patients with CAD. The exact n was not verified in this session. — [Houston Methodist record](https://scholars.houstonmethodist.org/en/publications/coronary-artery-wall-shear-stress-is-associated-with-progression-/)
- A JACC state-of-the-art review states that CCTA-derived features (including WSS) "can be leveraged to predict plaque evolution". This is a review claim, not new data. — [JACC 2020 review](https://www.jacc.org/doi/10.1016/j.jacc.2020.06.076)
- A serial-CCTA review of 36 studies: baseline quantitative plaque metrics predicted progression better than qualitative ones; geometry was not a focus. — [PMC8923615](https://pmc.ncbi.nlm.nih.gov/articles/PMC8923615/)

### Inferences
- Every CT-WSS / geometry predictive study found is either ACS case-control (EMERALD, ICONIC) or invasive serial imaging in diseased vessels (PREDICTION, Samady, Hartman, PROSPECT). Applying their effect sizes to plaque-free asymptomatic CGPS segments is extrapolation. Plaque in those studies also alters lumen geometry and WSS (reverse causation), which a plaque-free baseline avoids.
- Feature table (my synthesis for the report writer):

| Feature | Best human evidence | Design / population | Beyond position & risk factors? | Plaque-free baseline? |
|---|---|---|---|---|
| Distance from ostium / proximal location | ICONIC HR 2.71 (culprit vs nonculprit); Wang 2004 | Case-control ACS; STEMI angiography | Lesion-level multivariable; not vs risk factors | No |
| Bifurcation involvement (side-branch origin in segment) | ICONIC HR 2.14 / 2.63 | Case-control ACS | Partly | No |
| Tortuosity | ICONIC HR 2.31 (rare, wide CI) | Case-control ACS | Partly | No |
| Myocardial bridge (segment proximal to MB) | Chen 2024 radiomics AUC 0.75 ext.; anatomy model 0.56 | Retrospective serial CCTA, multicentre | Radiomics yes; anatomy no | **Yes** |
| CT/QCA-derived low or high WSS, APS | EMERALD; Bourantas 2020 HR 1.11; PROSPECT-ESS HR 4.34 | Case-control / post hoc of ACS trials | Beyond plaque features | No |
| Radiomics of plaque-free segments | PARADIGM JCCT 2024 (improved over clinical) | Retrospective serial CCTA, referral | Beyond clinical risk factors | **Yes** |
| Side-branch take-off angle (LAD–D1, LCx–OM) | Only PCI side-branch-occlusion studies | Cross-sectional | No | No |
| LM length | 1976 angiography/autopsy (short LM → CAD); CT n = 62 null | Cross-sectional | No | No |
| Lumen eccentricity, side-branch count, ramus, ostial take-off | None found | — | — | — |
| V/M, indexed lumen volume | Cross-sectional only (earlier report) | Referral | No | No |

### Gaps
- No SCOT-HEART, DANCAVAS or CGPS geometry/WSS-to-new-plaque study found. If one exists it would be key; a targeted search of Danish cohort output is advised.
- The Atherosclerosis 2023 non-calcified-segment WSS paper and the ATVB 2018 MB progression paper should be read in full (both 403 here).
- PREDICTION and Samady numbers were not re-verified in this session. The PPV ~41% comes from the earlier report.
