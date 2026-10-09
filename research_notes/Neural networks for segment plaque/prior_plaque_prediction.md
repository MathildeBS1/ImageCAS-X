# Prior ML/DL studies predicting future coronary plaque (progression, new plaque, lesion development) from CCTA

Search method: PubMed E-utilities (title/abstract queries combining ML/DL/radiomics/WSS with plaque progression / new plaque / plaque development and CCTA), plus web search. All numbers below were read from the PubMed abstract unless stated otherwise; full texts were not read (several publishers returned 403). Numbers that only appear in full texts (e.g. NRI for PARADIGM ML) are therefore not reported.

## 1. ML/DL studies predicting plaque progression or new plaque at serial CCTA

### Takeaway
Every published "prediction of future plaque from CCTA" model found uses hand-crafted features (quantitative plaque metrics, plaque or pericoronary fat radiomics) fed to Cox/logistic regression, random forest, XGBoost or gradient boosted trees. No peer-reviewed study was found that trains a deep neural network (CNN, GNN, transformer) end-to-end to predict future plaque per segment from serial CCTA. Patient-level AUCs cluster at 0.73 to 0.88 on held-out data; the one large segment-level study of incident plaque (PARADIGM radiomics, 9583 segments) reached a test C-index of 0.77. Nearly all cohorts are clinically referred, mostly Asian, with 2 to 5 year scan intervals; none is a general-population 10-year cohort.

### Cited Findings

Patient-level progression (existing plaque)
- Han et al. 2020, JAHA, PARADIGM registry: 1083 patients with serial clinically indicated CCTA; outcome rapid plaque progression (RPP) = annual increase in percent atheroma volume (PAV) >= 1.0%, occurring in 224 (21%). Three ML models (clinical; + qualitative plaque; + quantitative plaque) compared with ASCVD risk score, Duke CAD score, and logistic regression. AUC: ML model 3 0.83 (0.78 to 0.89) vs ASCVD 0.60, Duke CAD 0.74, ML clinical-only 0.62, ML + qualitative 0.73; statistical (logistic) model 0.81, not significantly different from ML (P = 0.128). Quantitative CT plaque features ranked highest. Patient level. — [Han 2020, PubMed 32089046](https://pubmed.ncbi.nlm.nih.gov/32089046/)
- Su et al. 2026 (online 2025), Can J Cardiol: 664 adults with subclinical non-obstructive CAD from a community screening program (China), serial CCTA, median follow-up 56 months. Seven algorithms compared after LASSO selection; final 8-feature random forest AUC 0.875 (0.827 to 0.920). SHAP drivers: fibrofatty plaque volume and coronary artery calcium category. Patient level; screening population closest in design to CGPS found. — [Su 2026, PubMed 41349607](https://pubmed.ncbi.nlm.nih.gov/41349607/)
- Feng et al. 2023, Eur Radiol: 400 patients with >= 2 CCTAs (2009 to 2020), 7:3 split. AUC (validation): conventional plaque parameters 0.654, plaque radiomics 0.729, combined 0.758. FAI and non-calcified plaque burden independent predictors. — [Feng 2023, PubMed 37460800](https://pubmed.ncbi.nlm.nih.gov/37460800/)
- Chen R et al. 2024, J Thorac Imaging: 500 patients with serial CCTA >= 2 years apart; progression = annual plaque-burden change above cohort median. Test AUC: PCAT radiomics 0.736 vs quantitative plaque characteristics 0.594 (P = 0.007). — [Chen R 2024, PubMed 38704662](https://pubmed.ncbi.nlm.nih.gov/38704662/)
- Li Y et al. 2024, Insights Imaging: 1233 patients, two centres, random forest; RPP prediction. PCAT radiomics AUC 0.85 train, 0.84 internal, 0.81 external validation, significantly higher than clinical and plaque-characteristic models; adding clinical or plaque features to radiomics did not improve AUC significantly. — [Li 2024, PubMed 38900243](https://pubmed.ncbi.nlm.nih.gov/38900243/)
- Ma et al. 2026, Acta Diabetol: 114 T2DM patients with 1 to 49% stenosis, 1 to 5 year follow-up; "progression" mixes events (MI, revascularisation) with stenosis >= 50% on follow-up CCTA. Logistic nomogram (HbA1c, LAD-FAI, plaque length) AUC 0.833. Small, outcome definition not purely imaging. — [Ma 2026, PubMed 42541542](https://pubmed.ncbi.nlm.nih.gov/42541542/)

Lesion-level progression
- Chen Q et al. 2023, Circ Cardiovasc Imaging: 214 patients, 2 hospitals (development 137 patients / 164 lesions; validation 77 / 101 lesions). RPP defined per lesion as annual plaque-burden increase >= 1.0%. XGBoost plaque radiomics signature AUC 0.81 vs 0.69 for conventional morphology in validation (P = 0.04); OR 2.35 after adjustment. Lesion level. — [Chen Q 2023, PubMed 37725670](https://pubmed.ncbi.nlm.nih.gov/37725670/)
- Pan et al. 2025, Eur J Radiol Open: 97 patients, 127 plaques (40 progressive). PCAT radiomics random forest AUC 0.971 train / 0.821 validation. Very small; the large train-validation gap indicates overfitting. Lesion level. — [Pan 2025, PubMed 40034660](https://pubmed.ncbi.nlm.nih.gov/40034660/)
- Lee SE et al. 2020, Int J Cardiovasc Imaging, PARADIGM: 1297 patients with only non-obstructive lesions, 3218 lesions, inter-scan interval 3.8 +/- 1.6 years; 76 lesions (2.4%) became obstructive (> 50% stenosis). C-statistic: clinical risk factors 0.684; + per-patient plaque volume and high-risk plaque 0.825; + per-lesion plaque volume and high-risk plaque 0.895 (per-lesion superior, P < 0.001). Statistical (not ML) model, but key evidence that lesion-level features outperform patient-level burden. — [Lee 2020, PubMed 32779077](https://pubmed.ncbi.nlm.nih.gov/32779077/)
- Zhang H et al. 2026, Diagnostics: 542 NSTE-ACS patients; PCAT radiomics of non-culprit lesions; serial CCTA sub-cohort n = 60 where baseline radiomics score associated with annual non-calcified plaque volume progression (standardised beta 0.477). Main endpoint was MACE (AUC 0.793 combined vs 0.703 clinical). — [Zhang H 2026, PubMed 42122042](https://pubmed.ncbi.nlm.nih.gov/42122042/)

Kinetic plaque features (uses the follow-up scan, so not baseline prediction)
- Wang Y et al. 2022, EHJ-CVI: 101 ACS cases with prior serial CCTA plus 101 matched controls. Baseline lesion features did not differ; changes between scans (stenosis, remodelling index, necrotic core, CT-FFR, calcium ratio) did. XGBoost on top-5 kinetic features AUC 0.918 for ACS. Outcome is events, not plaque. — [Wang 2022, PubMed 34151931](https://pubmed.ncbi.nlm.nih.gov/34151931/)

Other cohorts named in the brief
- Kolossváry et al. 2021, Radiology: 300 participants (HIV / cocaine cohort, Baltimore) with CAD on CCTA, mean 4.0 years between scans, 1276 radiomic features per plaque; risk factors (cocaine, HIV, ASCVD risk) associated with distinct, non-overlapping changes in radiomic features. Descriptive, not a predictive model. — [Kolossváry 2021, PubMed 33591887](https://pubmed.ncbi.nlm.nih.gov/33591887/)
- Kolossváry et al. 2022, Eur Radiol: 69 people with HIV, CCTA at 0, 6, 12 months; latent radiomic network framework for temporal plaque morphology change. Proof of principle, no prediction AUC. — [Kolossváry 2022, PubMed 35648210](https://pubmed.ncbi.nlm.nih.gov/35648210/)
- NATURE-CT 2026, JCCT: 205 low-risk outpatients (CAC <= 100, no lipid-lowering therapy), median 4.9 years between scans, AI-QCT (Cleerly). Non-calcified plaque rose from median 27.5 to 53.5 mm3; only 3% met the PARADIGM RPP threshold. Natural history, no prediction model; relevant base rates for a low-risk population. — [Aldana-Bitar 2026, PubMed 42167968](https://pubmed.ncbi.nlm.nih.gov/42167968/)
- SMARTool (EU H2020): about 263 patients with CCTA at two time points ~5 years apart, plus clinical, molecular and omics data; platform description. — [Sakellarios 2018, PubMed 30441365](https://pubmed.ncbi.nlm.nih.gov/30441365/)

### Inferences
- The thesis would be, as far as these searches show, the first segment-level neural-network model of future plaque on serial CCTA, and the first in a general-population cohort with a ~10-year interval. Claim this carefully ("no study found") since full texts and non-PubMed venues (MICCAI, arXiv) were not exhaustively checked.
- Han 2020 shows a well-tuned logistic model matched ML (0.81 vs 0.83). A logistic or Cox model on the same per-segment features is therefore a mandatory baseline, not just SCORE2.
- Single-centre radiomics studies with train AUC >= 0.95 and much lower validation AUC (Pan 2025; Zhang R 2025 below) should be quoted with caution; multi-centre / external-validation studies (Li 2024, Chen Q 2023, Lee 2024) are better anchors.

### Gaps
- No ICONIC, CAPIRE, Miami Heart Study or SCAPIS paper reporting an ML model of serial plaque change was found; SCAPIS ML work found was segmentation only ([Alvén 2025, PlaqueViT](https://pubmed.ncbi.nlm.nih.gov/39909898/)). Miami Heart and SCAPIS have single baseline CCTA in what was found.
- No "Weber et al." ML progression study was identified.
- Dey/Lin deep-learning plaque quantification work predicts MI (events), not plaque progression; not retrieved in detail here.
- No deep-learning (CNN/GNN) model predicting future plaque from serial CCTA in a peer-reviewed journal was found. A 3D CNN for clinical outcome from CCTA exists ([JIIM 2025](https://link.springer.com/article/10.1007/s10278-025-01667-4)) but predicts events.

## 2. Geometric / hemodynamic features (WSS, curvature, bifurcation, FFR-CT) with ML for lesion development

### Takeaway
Hemodynamic CCTA studies of plaque progression are small (12 to 37 patients, tens of vessels or lesions) and mostly use regression, with one gradient-boosted-trees model (AUC 0.76). Low WSS and high LDL concentration predict segment-level plaque-burden increase; side branches must be included for WSS to predict well. Myocardial-bridge studies are the only CCTA "geometry + ML predicts new plaque" studies with external validation. Large lesion-level hemodynamic studies (EMERALD) predict ACS events, not plaque development.

### Cited Findings
- Sakellarios et al. 2017, EHJ-CVI (PROSPECT-MSCT data): 32 ACS patients, CCTA after PCI and at 3 years, 58 vessels. Outcome: plaque-burden increase > 2 SD of intra-observer variability. High LDL concentration (OR 2.16), plaque burden (OR 1.40), plaque area (OR 3.46) independent; ESS predictive only univariately. Accuracy 65.1% (LDL model) vs 62.5% (ESS model). — [Sakellarios 2017, PubMed 26985077](https://pubmed.ncbi.nlm.nih.gov/26985077/)
- Sakellarios et al. 2020, IEEE EMBC (same 32 patients / 58 arteries): gradient boosted trees on CFD + LDL transport features. Plaque-area increase by 20%: accuracy 0.73, sensitivity 0.67, specificity 0.86, AUC 0.76; lumen-area decrease AUC 0.59. Reported to outperform logistic regression. Conference paper. — [Sakellarios 2020, PubMed 33018578](https://pubmed.ncbi.nlm.nih.gov/33018578/)
- Sakellarios et al. 2017, EuroIntervention: 17 bifurcations in 15 patients (PROSPECT-MSCT), 3-year CCTA follow-up. Low ESS predicted lumen reduction (p = 0.007), plaque-burden increase (p = 0.0006), necrotic core change (p = 0.025); including daughter branches with Murray's-law flow split gave better prediction than main-vessel-only models. — [Sakellarios 2017b, PubMed 28606882](https://pubmed.ncbi.nlm.nih.gov/28606882/)
- Bourantas et al. 2016, JACC CVI research letter: PROSPECT-MSCT, non-invasive prediction of atherosclerotic progression (abstract not available; details not verified). — [Bourantas 2016, PubMed 26363836](https://pubmed.ncbi.nlm.nih.gov/26363836/)
- Ramasamy et al. 2026, ATVB (IVUS/OCT-based, not CCTA): 40 vessels; complete reconstruction with side branches gave C-statistic 0.725 vs 0.651 for single-vessel reconstruction for progression (lumen area reduction + plaque-burden increase). — [Ramasamy 2026, PubMed 42131920](https://pubmed.ncbi.nlm.nih.gov/42131920/)
- Liu et al. 2017, Comput Assist Surg: 12 ACS patients, RCA CCTA at baseline and 12 months, 365 segments of 3 mm. Plaque-burden increase predicted by small minimal lumen area and low WSS; von Mises stress predicted remodelling. — [Liu 2017, PubMed 29032716](https://pubmed.ncbi.nlm.nih.gov/29032716/)
- Lv et al. 2026, J Cardiovasc Transl Res: 22 patients, 34 lesions, mean 2-year interval; normalised minimum WSS (OR 0.38) and maximum helicity (OR 1.44) predicted progression (diameter stenosis +5%); AUC 0.78 progression, 0.83 regression. — [Lv 2026, PubMed 41483452](https://pubmed.ncbi.nlm.nih.gov/41483452/)
- De Nisco et al. 2024, ATVB: 37 ACS patients with CCTA + NIRS-IVUS + OCT at baseline and 1 year; high topological shear variation index and low TAWSS associated with higher PAV progression, largest (>= 5.9%) where lipid-rich plaque coincided. — [De Nisco 2024, PubMed 38328935](https://pubmed.ncbi.nlm.nih.gov/38328935/)
- Chen YC et al. 2024, EHJ-CVI: 295 patients with LAD myocardial bridge and no proximal plaque at index CCTA (development 192, external 103 from four hospitals). Vascular radiomics of proximal cross-sections predicted new proximal plaque: AUC 0.78 / 0.75 / 0.75 (train / internal / external); added to clinical + anatomical model, external AUC rose 0.56 to 0.75, NRI 0.76, IDI 0.17. Incident-plaque, location-specific. — [Chen YC 2024, PubMed 38781436](https://pubmed.ncbi.nlm.nih.gov/38781436/)
- Chen Y et al. 2024 (Chinese): 104 matched LAD-MB patients, median 3 years; CFD "mechanomics" random forest predicted proximal plaque formation, validation AUC 0.86, HR 10.58. — [Chen Y 2024, PubMed 39990838](https://pubmed.ncbi.nlm.nih.gov/39990838/)
- Li SY et al. 2025 (Chinese): 253 LAD-MB patients without baseline LAD-MB plaque (+75 external), median 3.2 years; decision-tree ML combining FAI, MB anatomy, risk factors beat logistic regression in external validation (NRI 0.359, IDI 0.108). — [Li SY 2025, PubMed 40374349](https://pubmed.ncbi.nlm.nih.gov/40374349/)
- Tommasino et al. 2024, J Cardiovasc Dev Dis: 499 patients; left-main bifurcation angle > 80 degrees HR 4.47 for MACE; "CLAP" score AUC 0.85 validation. Cross-sectional stenosis + MACE, not serial plaque. — [Tommasino 2024, PubMed 39590181](https://pubmed.ncbi.nlm.nih.gov/39590181/)
- EMERALD: 72 ACS patients, 216 lesions on pre-event CCTA; adverse hemodynamic characteristics (FFR-CT, delta FFR-CT, WSS, axial plaque stress) added discrimination of culprit lesions. EMERALD II lesion-level AUC 0.851 for ACS within 2 years vs 0.741 beyond 2 years. Outcome is ACS culprit, not plaque development. — [TCTMD summary](https://www.tctmd.com/news/ai-assessment-plaque-hemodynamics-may-id-lesion-specific-acs-risk); [Mount Sinai record, prognostic time frame](https://scholars.mssm.edu/en/publications/prognostic-time-frame-of-plaque-and-hemodynamic-characteristics-a/)

### Inferences
- Bifurcation and side-branch geometry matter for hemodynamic predictors (Sakellarios 2017b, Ramasamy 2026), which supports using the full centerline tree rather than isolated vessels as model input.
- The MB studies show that geometry-local features can predict incident plaque at a specific location with external AUC about 0.75; a reasonable expectation for a segment-level geometry model.
- No study combined curvature, bifurcation angle, daughter diameter ratio and lumen volume-to-myocardial mass in an ML model of future plaque; this is open.

### Gaps
- Stone PREDICTION and PROSPECT ESS work are IVUS-based; not retrieved here. Kumar et al. high-WSS-and-MI work is invasive/events; not retrieved.
- No CCTA-only study with > 100 patients modelling WSS -> plaque progression was found.

## 3. Incremental value beyond clinical risk scores and baseline plaque burden

### Takeaway
Clinical risk scores alone are weak for predicting future plaque (AUC/C 0.60 to 0.70). Adding baseline plaque quantification or radiomics typically adds 0.07 to 0.23 AUC. Whether ML adds over a regression on the same features is unproven (Han 2020: 0.83 vs 0.81, NS).

### Cited Findings
- PARADIGM RPP: ASCVD score 0.60 -> ML with quantitative plaque 0.83; logistic on same features 0.81 (NS). — [Han 2020](https://pubmed.ncbi.nlm.nih.gov/32089046/)
- PARADIGM new plaque per segment: clinical 0.696 vs radiomics 0.691 (no difference) vs combined 0.767 (test, P < 0.0001). — [Lee 2024, PubMed 38378314](https://pubmed.ncbi.nlm.nih.gov/38378314/)
- PARADIGM obstructive lesion: clinical 0.684 -> + per-patient plaque 0.825 -> + per-lesion plaque 0.895. — [Lee 2020](https://pubmed.ncbi.nlm.nih.gov/32779077/)
- LAD-MB new plaque: clinical + anatomical 0.56 -> + vascular radiomics 0.75 (external), NRI 0.76, IDI 0.17. — [Chen YC 2024](https://pubmed.ncbi.nlm.nih.gov/38781436/)
- Radiomics vs plaque metrics: 0.729 vs 0.654 (Feng 2023), 0.736 vs 0.594 (Chen R 2024), 0.81 vs 0.69 (Chen Q 2023); adding plaque/clinical to PCAT radiomics gave no significant gain (Li 2024). — [Feng 2023](https://pubmed.ncbi.nlm.nih.gov/37460800/); [Chen R 2024](https://pubmed.ncbi.nlm.nih.gov/38704662/); [Chen Q 2023](https://pubmed.ncbi.nlm.nih.gov/37725670/); [Li 2024](https://pubmed.ncbi.nlm.nih.gov/38900243/)

### Inferences
- The thesis comparison ladder is supported by precedent: SCORE2 inputs -> + baseline segment plaque -> + geometry -> neural network, with a regression on identical features as the fair ML baseline.
- Most incremental-value reports use DeLong only; NRI/IDI is reported only in MB studies. Reporting NRI/IDI and calibration would be above the norm.

### Gaps
- NRI/IDI for Han 2020 and Lee 2024 (if any) are in full texts not accessed.
- No study benchmarked against SCORE2 specifically; ASCVD PCE and Duke CAD score are the reported comparators.

## 4. Incident plaque in plaque-free segments vs progression of existing plaque

### Takeaway
Three study lines target incident plaque: PARADIGM segment-level radiomics (largest, segment level), CCTA-negative patients (patient level), and LAD myocardial bridges (location level). Segment-level incident plaque is rare (9.8% of normal segments over >= 2 years), so class imbalance is substantial even before a 10-year horizon.

### Cited Findings
- Lee SE et al. 2024, JCCT, PARADIGM: 9583 plaque-free segments from 1162 patients (age 60.3, 55.7% male), serial CCTA >= 2 years; new plaque = total plaque volume >= 1 mm3 in the segment at follow-up; 9.8% developed plaque. Segment-level Cox models, 8:2 split. Test C-index: clinical 0.696, radiomics 0.691, clinical + radiomics 0.767. This is the closest precedent to the thesis outcome. — [Lee 2024, PubMed 38378314](https://pubmed.ncbi.nlm.nih.gov/38378314/)
- Tantawy et al. 2026 (EHJ-CVI abstract supplement), PARADIGM: 1343 patients, 334 (24.9%) without baseline plaque, follow-up median 3.3 years; new lesions most often in LAD (60%) and RCA (47%); predictors baseline plaque presence (OR 1.84), diabetes (OR 1.38), BMI (OR 1.04/kg/m2). Abstract only, no ML. — [Tantawy 2026](https://academic.oup.com/ehjcimaging/article/27/Supplement_1/jeaf367.317/8446296)
- Zhang R et al. 2025, Int J Cardiol: 947 patients with normal baseline CCTA, two CCTAs; PCAT radiomics (279 features) + clinical model AUC 0.99 train, 0.93 validation; patient level. Implausibly high training AUC; interval and definition details not in abstract. — [Zhang R 2025, PubMed 40812623](https://pubmed.ncbi.nlm.nih.gov/40812623/)
- LAD myocardial-bridge incident plaque: Chen YC 2024 (n = 295, external AUC 0.75), Li SY 2025 (n = 253 + 75 external), Chen Y 2024 (n = 104, validation AUC 0.86). — [Chen YC 2024](https://pubmed.ncbi.nlm.nih.gov/38781436/); [Li SY 2025](https://pubmed.ncbi.nlm.nih.gov/40374349/); [Chen Y 2024](https://pubmed.ncbi.nlm.nih.gov/39990838/)

### Inferences
- Lee 2024 sets a concrete baseline target: segment-level incident-plaque C-index about 0.70 for clinical factors and about 0.77 with image features, at 2 to 5 years in a referred population. The thesis should report incident (plaque-free baseline segments) and progression (plaque-present segments) as separate tasks, as the literature does.
- The finding that patient-level baseline plaque presence predicts new lesions (Tantawy) suggests including other segments' baseline plaque (a tree-level or graph context) as input to each segment's prediction.

### Gaps
- No incident-plaque study with an interval near 10 years or in a general population was found.
- Lee 2024's handling of within-patient clustering (segments nested in patients) is not stated in the abstract.

## 5. Reported pitfalls: interscan variability, scanner change, reader variability, regression to the mean

### Takeaway
Short-interval repeat-scan studies report good interscan reproducibility for total and non-calcified plaque volume, but these use the same scanner over days to months. Over 10 years scanner, reconstruction and software changes are unavoidable; the evidence on cross-protocol effects is limited (one tube-voltage study) and radiomic features are known to be reconstruction-sensitive. No serial CCTA ML study addressing regression to the mean was found.

### Cited Findings
- Schuhbaeck et al. 2014, Eur Radiol: 20 patients scanned twice within 100 days on dual-source CT; automated software; interscan r = 0.92 (total), 0.90 (non-calcified), 0.96 (calcified plaque volume). — [Schuhbaeck 2014, PubMed 24962824](https://pubmed.ncbi.nlm.nih.gov/24962824/)
- Meah et al. 2021, JCCT: 20 patients with advanced CAD, repeat CCTA 2 weeks apart, 149 segments; no significant interscan differences; calcified and low-attenuation plaque had relatively wide limits of agreement (-236.6 to 174 mm3; -15.8 to 10.5 mm3). — [Meah 2021, PubMed 33423941](https://pubmed.ncbi.nlm.nih.gov/33423941/)
- Lee SE et al. 2019, JCCT: repeat CCTA within 90 days; 95 patients same kVp, 24 patients different kVp; no significant per-segment or per-lesion plaque volume differences in either group. Small different-kVp group. — [Lee 2019, PubMed 30342980](https://pubmed.ncbi.nlm.nih.gov/30342980/)
- Kolossváry et al. 2019, JCCT: image reconstruction algorithms affect volumetric and radiomic plaque parameters (title-level; abstract not read). — [Kolossváry 2019, PubMed 30447949](https://pubmed.ncbi.nlm.nih.gov/30447949/)
- Kolossváry et al. 2021, JCCT: vessel-wall segmentation choice affects volumetric and radiomic parameters (title-level). — [Kolossváry 2021b, PubMed 32868246](https://pubmed.ncbi.nlm.nih.gov/32868246/)
- Sakellarios et al. 2021, Diagnostics: 20 patients, 6-year interscan interval; imaging/reconstruction error propagated minimally to shear stress but substantially to some plaque-growth-model variables. — [Sakellarios 2021, PubMed 34943545](https://pubmed.ncbi.nlm.nih.gov/34943545/)
- Sakellarios 2017 defined progression as change > 2 SD of intra-observer variability, an explicit measurement-error threshold. — [Sakellarios 2017, PubMed 26985077](https://pubmed.ncbi.nlm.nih.gov/26985077/)
- Lee 2024 used plaque volume >= 1 mm3 as the incident-plaque threshold, below many reported limits of agreement for small plaque. — [Lee 2024](https://pubmed.ncbi.nlm.nih.gov/38378314/); [Meah 2021](https://pubmed.ncbi.nlm.nih.gov/33423941/)
- Cho et al. 2022 case report (13 years, 5 CCTAs, Cleerly AI-QCT): small plaques that readers might call artefacts reappeared at the same locations on each scan. — [Cho 2022, PubMed 36435762](https://pubmed.ncbi.nlm.nih.gov/36435762/)

### Inferences
- For CGPS, the outcome should be defined with a threshold tied to measured reproducibility (as Sakellarios did) or validated on a repeat-scan subset, and scanner/protocol at each time point should be a recorded covariate or stratification factor.
- Per-segment visual plaque labels (presence/absence) are less exposed to volume measurement error than percent atheroma volume, but more exposed to reader variability; inter-reader agreement on segment plaque presence in CGPS should be reported.
- Image-intensity features (radiomics, CNN on raw HU) are more scanner-sensitive than lumen geometry, which favours the thesis's geometry inputs for a 10-year cross-scanner design.

### Gaps
- No source found quantifying regression to the mean in serial CCTA plaque progression or how ML studies handle it.
- No study found on cross-scanner (different vendor/generation) reproducibility over long intervals; Lee 2019 covers only kVp differences over < 90 days.
- No serial CCTA study found reporting inter-reader kappa for segment-level plaque presence at both time points.
