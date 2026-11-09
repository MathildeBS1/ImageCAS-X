# Near misses: baseline coronary geometry and later plaque development (longitudinal / serial CCTA)

Search date 2026-11-07. Tool budget limited (about 25 calls). PubMed pages often returned a cookie wall, so several abstracts were read through Europe PMC or publisher pages. "Opened" means I read the full text or abstract myself. "Not opened" means the facts come from a search snippet or secondary citation and must be checked before they go into the thesis table. Shen 2026 (coronary geometry) was not searched for or used, per instruction.

## Q1. Verification of the named near misses (literature table rows)

### Takeaway
The two closest studies are Lee 2024 (PARADIGM radiomics: plaque-free *segments* in a referred serial CCTA registry, outcome new plaque, but radiomic texture features, not named geometry) and Chen 2024 (centreline curvature/cross-section radiomics proximal to an LAD myocardial bridge, plaque-free LAD at baseline, referred Chinese patients, ~2–3 y follow-up). Neither is a random population sample, neither measures named whole-tree geometry (bifurcation angle, diameter ratios, taper) as prespecified predictors, and neither reaches a 10-year interval. The gap claim holds in its current form.

### Cited Findings

**Chen et al. 2024, Eur Heart J Cardiovasc Imaging 25(10):1462–1471, doi 10.1093/ehjci/jeae135 (full text opened)** — [OUP](https://academic.oup.com/ehjcimaging/article/25/10/1462/7680519)
- Title: "Coronary CTA-based vascular radiomics predicts atherosclerosis development proximal to LAD myocardial bridging."
- Cohort: 192 consecutive patients at Jinling Hospital (2007–2021) with LAD myocardial bridge and at least two CCTAs at least 3 months apart (training 154, internal test 38); external set 103 patients from four other Chinese centres. Hospital CCTA patients, i.e. referred/clinical, not population-based; 88 came from an earlier CT-FFR study.
- Baseline plaque status: no plaque in the LAD at baseline.
- Geometry: in the 30 mm segment proximal to the bridge (pMB) and in the bridge itself, 17 centreline metrics (including curvature and arc length) and 16 cross-sectional metrics (axis lengths, areas) in systole and diastole, expanded to 496 cross-sectional and 531 centreline radiomic features per segment; Boruta selection, top 15, random forest.
- Outcome: any plaque 20–30 mm proximal to the bridge entrance, any stenosis or type. 52/192 (27.1%) development, 33/103 (32.0%) external.
- Follow-up: median 3.0 y (IQR 1.7–4.5) development, 2.1 y (1.4–3.1) external.
- Adjustment: clinical logistic model (only diabetes independent, OR 3.70, 95% CI 1.67–8.21). Covariates in the radiomics models not clearly stated.
- Effect: pMB cross-sectional model AUC 0.75 (external, 0.64–0.86); pMB centreline model OR 2.69 (1.43–5.06); clinical model external AUC 0.56; combined external AUC 0.76 in Results vs 0.75 in abstract (internal inconsistency).
- Limitations (authors): retrospective, small, short follow-up, incomplete risk-factor data, tested only in bridge patients.

**Lee SE et al. 2024, J Cardiovasc Comput Tomogr 18(3):274–280, doi 10.1016/j.jcct.2024.02.003, PMID 38378314 (abstract only)** — [Europe PMC record](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1111/joim.70068%20OR%20DOI:10.1016/j.jcct.2024.02.003&resultType=core&format=json); [PubMed](https://pubmed.ncbi.nlm.nih.gov/38378314/)
- Title: "Prediction of the development of new coronary atherosclerotic plaques with radiomics." PARADIGM registry (multinational, clinically referred serial CCTA, scans at least 2 years apart).
- 9,583 plaque-free baseline segments from 1,162 patients (mean age 60.3 ± 9.2, 55.7% male); 8:2 train/test split; 9.8% of segments developed new plaque (new plaque defined as total plaque volume ≥ 1 mm³ at follow-up, per search snippet).
- Features: radiomic features of the plaque-free segments (texture/intensity), not named geometric features.
- Cox models: clinical risk factors C-index ~0.70 (0.701 train / 0.696 test per snippet); radiomics alone 0.699 / 0.691 (snippet); combined 0.772 train / 0.767 test (abstract).
- Patients are not plaque-free as persons: segments were plaque-free, but the person could have plaque elsewhere (PARADIGM is mostly patients with disease). Abstract-level only; split by person not verifiable from abstract.

**CArTI, AHA Scientific Sessions 2025, Circulation 152(Suppl 3), Abstract 4365988, doi 10.1161/circ.152.suppl_3.4365988 (not opened, 403; search snippet only; conference abstract)** — [AHA](https://www.ahajournals.org/doi/10.1161/circ.152.suppl_3.4365988)
- Title: "AI-informed Coronary Artery Tortuosity Index (CArTI) from Cardiac CT Angiography Predicts 5-Year Cardiovascular Risk." Deep-learning coronary segmentation, a structural complexity/tortuosity index of the tree; holdout C-index 0.648 for 5-year MACE.
- Cohort size, population type, baseline plaque status and adjustment not available from what I could read. Outcome is MACE, not plaque development. Not peer reviewed.

**Good et al. 2026, J Intern Med 299(4):467–480, doi 10.1111/joim.70068, PMID 41558989 (abstract via Europe PMC)** — [Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1111/joim.70068%20OR%20DOI:10.1016/j.jcct.2024.02.003&resultType=core&format=json)
- Design paper of the SCAPIS re-examination: about 15,000 participants (50% of the original random population cohort) re-examined at six Swedish university hospitals, median 8.1 years after baseline, aged 55–75 at follow-up, including repeat imaging. First 5,000: 50% women, median age 65.5.
- No outcome results on plaque development and no geometry. Important as a future competitor: once SCAPIS re-examination CCTA results appear, they will be a random-population serial CCTA cohort with ~8-year interval.
- Related: a photon-counting CCTA protocol paper for the re-examination (1,147 re-exam vs 29,554 baseline scans; ~30% of baseline stenosis cases downgraded to < 50%) — [PubMed 42127646](https://pubmed.ncbi.nlm.nih.gov/42127646/) (snippet only). Relevant as a warning: scanner change between visits (energy-integrating to photon-counting) can change plaque detection, an artefact that also applies to any 10-year serial design with a scanner change.

**ICONIC geometry substudy: Han D et al. 2022, JAMA Cardiol 7(3):309–319, doi 10.1001/jamacardio.2021.5705 (full text opened)** — [JAMA Cardiology](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
- Nested case-control within CONFIRM (23,251 referred patients with suspected CAD): 116 ACS cases and 116 propensity-matched controls (of 234 pairs, 118 excluded); 548 lesions.
- Plaque present at baseline (all analyses are lesion-level, culprit precursor vs nonculprit).
- Geometry (lesion-level, reader-defined): short distance from ostium (< 39 mm LCA, < 60 mm RCA), bifurcation within lesion, tortuosity (one bend > 90° or three curves of 45–90°).
- Outcome: future ACS culprit; median time CCTA to ACS 29 days (IQR 5–386).
- Adjusted for stenosis, adverse plaque characteristics and quantitative plaque. HR: short ostial distance 2.71 (1.73–4.24), bifurcation 2.14 (1.39–3.29), tortuosity 2.31 (1.01–5.27); ≥ 2 adverse geometric characteristics 6.84 (3.33–14.04). AUC 0.733 to 0.766.
- Limitations: post hoc, half of pairs excluded, tortuosity < 5%, very short interval (many ACS within a month: closer to diagnosis than prediction).
- Note: this is the "Han 2022" already cited in the review.

**EMERALD: Lee JM et al. 2019, JACC Cardiovasc Imaging 12(6):1032–1043, doi 10.1016/j.jcmg.2018.01.023 (not opened; search snippet)** — [search record](https://scholars.mssm.edu/en/publications/prognostic-time-frame-of-plaque-and-hemodynamic-characteristics-a/)
- Case-control of patients with ACS who had CCTA 1 month to 2 years before the event; 66 culprit and 150 nonculprit lesions. CFD-derived FFR-CT, ΔFFR-CT, WSS and axial plaque stress; culprits had higher WSS and axial plaque stress; best model c-index 0.789.
- Plaque present at baseline; outcome ACS; referred. EMERALD II (JACC CVI 2025;18(7):784–795, 351 patients) found plaque/hemodynamic features most relevant within 2 years (snippet only).

**PREDICTION: Stone PH et al. 2012, Circulation 126:172–181 (not opened; secondary citation)** — [TCTMD](https://www.tctmd.com/news/endothelial-shear-stress-works-prediction-tool); [Bourantas 2020 citing it](https://boris.unibe.ch/144322/8/Bourantas%20JACCCardiovascImaging%202020_AAM.pdf)
- 506 Japanese ACS patients, invasive 3-vessel IVUS-based vascular profiling with ESS at baseline and repeat at 6–10 months (interval from memory, unverified); low ESS independently predicted progressive lumen narrowing and plaque growth. Invasive, plaque-laden ACS patients.

**PROSPECT ESS: Stone PH et al. 2018, JACC Cardiovasc Imaging (not opened; snippet)** — [Mount Sinai record](https://scholars.mssm.edu/en/publications/role-of-low-endothelial-shear-stress-and-plaque-characteristics-i-2/)
- Post hoc in PROSPECT (697 ACS patients, 3-vessel IVUS): 145 lesions in 97 patients (23 non-culprit MACE lesions, 122 controls). Low ESS: propensity-adjusted HR 4.34 (1.89–10.00) for non-culprit MACE. Invasive, existing lesions.

**Samady et al. 2011, Circulation 124:779–788 (not opened in this session)** — no source retrieved; from memory: ~20 patients with nonobstructive CAD, IVUS-VH and ESS at baseline and 6 months, low-ESS segments showed constrictive remodelling and plaque progression. Treat as unverified.

**Tommasino et al. 2024, J Cardiovasc Dev Dis 11(11):338, doi 10.3390/jcdd11110338 (full text opened; "CLAP score")** — [PMC11595042](https://pmc.ncbi.nlm.nih.gov/articles/PMC11595042/)
- Single-centre (Sant'Andrea, Rome) observational registry of consecutive symptomatic patients referred for CCTA; 499 analysed (of 650), external validation 200.
- Plaque present at baseline in many (severe proximal LAD stenosis 32%).
- LM bifurcation angle (LM–pLAD–pLCx) measured manually by two readers in 2D/3D; cut-off 80°; agreement with 3D-QCA bias −0.25°.
- Mean follow-up 374 ± 104 days; proximal LAD progression in 42 (8.4%), defined as ≥ 30% increase in stenosis or new high-risk features; follow-up imaging only when clinically indicated (verification bias).
- LMBA > 80°: HR 4.47 (3.80–6.70) for MACE, HR 5.33 (4.03–6.70) for proximal LAD progression; OR 3.23 for stenosis.
- Quality problems found in the full text: table labelled logistic but reports HRs, a Wald statistic inconsistent with its p value, implausibly narrow CI for LMBA. Treat effect sizes skeptically.

### Inferences
- The only serial-CCTA studies with plaque-free baselines and an incident-plaque outcome that use image features are Lee 2024 (segments, radiomics) and Chen 2024 (bridge-proximal LAD, centreline/cross-section radiomics). Both are referred hospital cohorts with 2–3 year intervals, and both use high-dimensional feature sets rather than a prespecified, interpretable geometry block tested beyond risk factors.
- All ESS/WSS studies (PREDICTION, PROSPECT, Samady, EMERALD, Sakellarios) start from existing plaque, in ACS or referred patients, and most measure geometry-derived haemodynamics with the plaque already shaping the lumen (remodelling artefact: lumen geometry is partly a consequence, not a cause).
- Han 2022 and Tommasino 2024 measure geometry with disease present and have very short intervals; their outcomes are events or clinically triggered re-imaging.

### Gaps
- CArTI abstract full text (cohort size, population, plaque status, adjustment) could not be opened (HTTP 403).
- Lee 2024: full text not opened; whether the train/test split was by person, and whether segments from persons with plaque elsewhere were included, is unverified.
- Samady 2011, Sakellarios 2017, PREDICTION interval: not opened this session.

## Q2. Geometry measured on CCTA in people without plaque, related to later plaque; serial CCTA incident-plaque studies in plaque-free or CAC = 0 people

### Takeaway
I found no study (2015–Nov 2026) in which curvature, tortuosity, bifurcation angle, diameter ratios, taper or myocardial-mass/lumen-volume ratio were measured on CCTA in plaque-free *persons* and related to later plaque development. Serial CCTA work in plaque-free people (PARADIGM, NATURE-CT-type data) looks at risk factors only. Random population serial CCTA (SCAPIS re-examination) exists only as a design paper so far.

### Cited Findings
- Searches combining tortuosity / vessel geometry / bifurcation angle with incident or new plaque on serial CCTA returned no matching study; the closest results were ICONIC (Han 2022) and lesion-level/cross-sectional work — [search results incl. JAMA Cardiol](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006).
- SCCT guidance states that evidence is insufficient to recommend serial CCTA plaque progression imaging clinically — [SCCT quantitative standards, JCCT 2024](https://www.journalofcardiovascularct.com/article/S1934-5925(24)00341-1/fulltext) (snippet only).
- PARADIGM serial CCTA (1,005 patients): higher ASCVD risk associated with faster progression — [JAMA Netw Open](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2768616) (snippet; risk factors only, referred, mostly with plaque).
- CAC = 0 serial data: a secondary summary reports NATURE-CT non-calcified plaque volume rising from median 27.5 to 53.5 mm³ over 5 years in CAC = 0 people — [Empirical Health blog](https://www.empirical.health/blog/nature-ct-coronary-plaque-progression/). Secondary, non-academic source; not verified against the original paper; do not cite.
- A US military cohort (NCT02636062) was designed to measure the rate of index plaque development after CAC = 0; status unclear, last update 2018 — [ClinicalTrials.gov](https://clinicaltrials.gov/study/NCT02636062).
- MESA, Miami Heart, DISCHARGE, Rotterdam, CONFIRM: no geometry-to-incident-plaque study surfaced in my searches (searched indirectly through the combined queries above; not exhaustively per cohort).

### Inferences
- The gap claim ("no study combined automated whole-tree geometry measurement with follow-up to incident plaque in a random population") still holds. A stricter version can also be defended: no study has related *named* geometric features measured in *plaque-free persons* to later plaque at any interval, in any cohort type. The nearest exceptions are segment-level (Lee 2024) or a single bridged segment (Chen 2024), both referred.
- Won 2022 (PARADIGM plaque-free) and Lee 2024 come from the same registry; Lee 2024 is effectively the image-feature extension of Won 2022 and should sit next to it in the table.

### Gaps
- Per-cohort searches of MESA (no CCTA serial imaging is expected), Miami Heart (baseline only so far, to my knowledge), DISCHARGE (outcome trial), Rotterdam and Chinese/Korean general-population cohorts were not run individually because of the tool budget. Absence of evidence here is from combined queries only.
- Won 2022 and Bergström 2021 numbers were not re-verified in this session.

## Q3. CGPS / Herlev–Østerbro publications on serial CCTA or coronary geometry

### Takeaway
No CGPS publication found that reports serial CCTA plaque development or coronary geometry. The published CGPS CCTA work is baseline (single-scan) prevalence and event-outcome studies.

### Cited Findings
- PubMed search "Copenhagen General Population Study" + coronary CT angiography (sorted by date) returned 19 records (2013–2026); none is about serial/repeat CCTA, plaque progression, incident plaque or coronary geometry; topics are MI risk (Fuchs 2023 Ann Intern Med; Larsen 2026 Eur Heart J, sex and MI risk), HIV, liver transplant, pre-eclampsia, aortic dimensions, LV mass, myocardial perfusion, calcium scoring, plaque morphology (de Knegt 2019, 2024) — [PubMed search](https://pubmed.ncbi.nlm.nih.gov/?term=%22Copenhagen+General+Population+Study%22+coronary+computed+tomography+angiography&sort=date&size=50).
- Fuchs et al. 2023 Ann Intern Med (doi 10.7326/M22-3027): 9,533 asymptomatic adults ≥ 40 y, CCTA from 2010, MI/death 2.7% (260/9,533) over 3.5 years; single-scan outcome study — [ACP](https://www.acpjournals.org/doi/10.7326/M22-3027) (snippet).
- No 2025–2026 CGPS paper by Fuchs, Kühl, Kofoed, Køber or Nordestgaard on serial CCTA was found by web search — [search](https://doi.org/10.7326/m23-0533) (closest hit: "Contemporary Natural History of Coronary Artery Disease" correspondence, not serial CCTA).

### Inferences
- Nothing published answers the thesis question. Because the 10-year follow-up scans are recent, a CGPS group paper on plaque progression (risk factors) could appear soon; check again before submission.

### Gaps
- Conference abstracts (ESC 2026, SCCT 2026) by the CGPS group were not searched.

## Q4. Left main bifurcation angle and later plaque

### Takeaway
Bifurcation-angle studies are cross-sectional except Tommasino 2024, which is short-term (about 1 year), referred, with plaque present, clinically triggered re-imaging and internal statistical inconsistencies. None relates angle measured in plaque-free people to later plaque.

### Cited Findings
- Tommasino 2024: see Q1 (LMBA > 80°, HR 5.33 for proximal LAD progression at ~1 y) — [PMC11595042](https://pmc.ncbi.nlm.nih.gov/articles/PMC11595042/).
- Dual-source CT study (PLoS One 2017): LAD–LCx bifurcation angle independent predictor of significant left coronary stenosis (OR 1.423, p = 0.002); cross-sectional; authors only *suggest* a role in earlier plaque development — [PLoS One](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0174352) (snippet).
- Temov & Sun 2016 (Int J Cardiovasc Imaging, doi 10.1007/s10554-016-0884-2): LM bifurcation angle vs CAD risk factors, cross-sectional — [Springer](https://link.springer.com/article/10.1007/s10554-016-0884-2) (title only).
- Ramus intermedius study: RI associated with wider LAD–LCx angle and LM bifurcation atherosclerosis; cross-sectional — [PMC10091592](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10091592/) (snippet).
- 2025 scoping review on CCTA in bifurcation disease: large LM bifurcation angles indicate obstructive disease (cross-sectional framing) — [Int J Cardiovasc Imaging 2025](https://link.springer.com/article/10.1007/s10554-025-03524-5) (snippet).

### Inferences
- Wider angles with plaque present may partly be an effect of disease (remodelling and plaque bulk change the measured branch directions), so cross-sectional angle–plaque associations cannot be read as prediction. The thesis's plaque-free baseline removes that reverse-causation path.

### Gaps
- Juan 2017, Rodriguez-Granillo, Sun/Cui and Gharleghi 2024 were not opened this session; based on what I know they are cross-sectional (angle vs stenosis/plaque, or angle normal values/atlas) with no follow-up, but this needs confirming.
