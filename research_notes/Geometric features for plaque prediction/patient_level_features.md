# Patient-level (whole-tree) coronary geometric features for predicting who develops plaque or events

Scope note: about 22 search/fetch calls (October 2026). Several key full texts (JCCT, Annals of Internal Medicine, one PMC page) returned 403 or reCAPTCHA, so some findings rest on abstracts or secondary summaries; this is flagged where it applies.

## 1. Evidence per candidate whole-tree feature

### Takeaway
The best supported whole-tree feature is coronary lumen volume normalised to LV myocardial mass (V/M). Lower V/M goes with more plaque, obstructive CAD, lower FFR, and (in retrospective cohorts) more events, with incremental value over plaque metrics. Dominance has been tested prospectively and does not predict outcome. Global tortuosity is, if anything, inversely associated with CAD. Left main geometry (bifurcation angle, length, diameter) has only small cross-sectional studies and mostly speaks to where plaque sits, not to who gets it.

### Cited Findings

**Lumen volume / myocardial mass (V/M)**
- V/M = total epicardial coronary lumen volume divided by LV myocardial mass, both segmented from CCTA. It was proposed as a marker of mismatch between coronary supply and myocardial demand. [Frontiers Cardiovasc Med 2025 review](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2025.1449148/full)
- NXT trial substudy (Taylor et al., 2017): 238 patients with suspected CAD, 438 vessels with invasive FFR. Patients with low V/M had greater QCA diameter stenosis, more plaque, and lower FFR (0.80 ± 0.12 vs 0.87 ± 0.08, P < 0.0001). V/M independently predicted FFR ≤ 0.80, including in non-obstructive CAD and independent of plaque measures. Population was symptomatic patients referred for invasive angiography, so the design is cross-sectional and diagnostic, not prognostic. [PubMed 28789941](https://pubmed.ncbi.nlm.nih.gov/28789941); [Monash record](https://research.monash.edu/en/publications/effect-of-the-ratio-of-coronary-arterial-lumen-volume-to-left-ven/)
- Lower V/M has been reported with a higher incidence of obstructive CAD, greater total plaque volume, and more haemodynamically significant ischaemia. Source is the Frontiers 2025 review summarising primary studies, including a 2024 JCCT study of patients with severe CAD whose full text returned 403. [Frontiers 2025](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2025.1449148/full); [JCCT 2024](https://www.journalofcardiovascularct.com/article/S1934-5925(24)00379-4/fulltext); [EHJ 2025 abstract, V/M vs plaque volume in severe CAD](https://academic.oup.com/eurheartj/article-abstract/46/Supplement_1/ehaf784.192/8312586)
- V/M falls progressively from stable angina to unstable angina to acute MI. The authors attribute this to lower epicardial lumen volume, which may reflect plaque. This is a cross-sectional comparison. [Frontiers 2025](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2025.1449148/full); [PMC11865212, V/M for ACS risk stratification](https://pmc.ncbi.nlm.nih.gov/articles/PMC11865212)
- Outcome study in type 2 diabetes: retrospective, single centre, n = 306 (mean age 62.3, 40.9% female), median follow-up 3.8 years, composite of death, nonfatal MI, UA hospitalisation and late revascularisation. Adjusted for clinical and CCTA parameters (obstructive CAD, total plaque volume, CT-FFR), V/M had HR 0.899 per 1 mm³/g (95% CI 0.865 to 0.935). Adding V/M to clinical plus CCTA models gave NRI 0.173 (p = 0.044) and IDI 0.057 (p < 0.001). Tertile cut-points were 21.9 and 27.4 mm³/g. [PMC13151284](https://pmc.ncbi.nlm.nih.gov/articles/PMC13151284/)
- Low V/M also predicts MACE after TAVR and is lower in primary microvascular angina. Both populations are far from a general-population screening cohort. [PMC12020294, TAVR](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12020294/); [PubMed 28993120, microvascular angina](https://pubmed.ncbi.nlm.nih.gov/28993120/); [PMC12302837](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12302837/)

**Coronary calibre / lumen size relative to body size and sex**
- Body surface area and sex independently predict coronary artery size. BSA has the larger effect, but sex remains a predictor after BSA adjustment. Women have smaller proximal LAD and RCA areas on CT. [PubMed 20043337, volumetric sex differences](https://pubmed.ncbi.nlm.nih.gov/20043337/)
- In the CREDENCE and PACIFIC-1 post hoc analysis (JCCT 2026), larger lumen area went with younger age, higher BMI, lower diameter stenosis, less ischaemia and smaller plaque burden, despite larger absolute plaque volumes. Within each stenosis category, smaller lumens had more ischaemia. The design is vessel-level and the population symptomatic. [ScienceDirect S1934592526000456](https://www.sciencedirect.com/science/article/pii/S1934592526000456)
- Plaque burden metrics depend on vessel size, which depends on BSA and sex. Any lumen-size feature therefore has to be normalised (to BSA, myocardial mass, or sex) before it can mean anything at patient level. [PubMed 20043337](https://pubmed.ncbi.nlm.nih.gov/20043337/)

**Coronary dominance**
- CONFIRM, a prospective international registry: n = 6,382 (47% female, mean age 56.9), 60-month follow-up, 91% right dominant and 9% left dominant. Dominance did not predict nonfatal MI, all-cause mortality, or late revascularisation in patients with normal coronaries, non-obstructive CAD, or obstructive CAD. [Applied Radiology summary](https://appliedradiology.com/articles/the-confirm-study-results-assessment-of-coronary-dominance-by-ccta); [eScholarship full text](https://www.escholarship.org/uc/item/7fg730bm)
- Left dominance may carry different short- and long-term mortality after ACS. This is a post-event population, not a screening one. [Applied Radiology](https://appliedradiology.com/articles/the-confirm-study-results-assessment-of-coronary-dominance-by-ccta)
- In a large retrospective single-centre cohort (AHA 2023 abstract), left-dominant systems had 10.1% more of their calcium in the LAD. Dominance shifts where calcium is distributed, which is a localisation finding, not a who-gets-it finding. [Circulation 2023 abstract 14844](https://www.citedrive.com/en/discovery/abstract-14844-coronary-artery-system-dominance-influences-the-distribution-of-calcified-plaques-in-coronary-tree/)

**Global tortuosity**
- Li et al. (PLoS One 2011): 1,010 consecutive patients at angiography. Tortuosity was defined as ≥3 bends of ≥45° along the main trunk of at least one artery; prevalence 39.1%. Tortuosity was negatively associated with CAD (OR 0.755, 95% CI 0.574 to 0.994) and positively with female sex (OR 2.603) and hypertension (OR 1.533). Over 2 to 4 years there was no MACE difference (cardiac death 1.5% vs 2.2%, MI 3.6% vs 4.8%, both non-significant). [PMC3164184](https://pmc.ncbi.nlm.nih.gov/articles/PMC3164184/)
- An inverse tortuosity–atherosclerosis relation recurs elsewhere: in a pooled analysis of six stent trials [JACC Interv 2021](https://www.jacc.org/doi/10.1016/j.jcin.2020.12.027); with lower Gensini scores in chronic coronary syndrome [PubMed 39620298](https://pubmed.ncbi.nlm.nih.gov/39620298/); and with severe tortuosity in non-obstructive CAD [PMC10534717](https://pmc.ncbi.nlm.nih.gov/articles/PMC10534717). Tortuosity has also been tested against carotid IMT and risk factors as a possible early-atherosclerosis marker [PMC8012427](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8012427/).
- In an automated CCTA pipeline study, CAC volume score was lower with higher tortuosity score. [APL Bioengineering 2024 (DOAJ)](https://doaj.org/article/682cc7f4ef964392a6e826332d875725)
- A 2026 machine-learning tortuosity quantification paper exists (JACC Advances). Its outcome findings were not retrieved. [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)

**Left main geometry (bifurcation angle, length, diameter)**
- Moon et al. (QIMS 2023): retrospective, n = 133. Wider LM–LAD angle (38.3° vs 29.2°) and more tortuous proximal LAD went with >50% proximal LAD stenosis. A combined index d20×cosθ < 15.5 gave adjusted OR 11.36, sensitivity 80.8%, specificity 71.0%. The outcome is a proximal-LAD lesion, so this is localisation-flavoured even though the analysis is per patient. [PMC10644144](https://pmc.ncbi.nlm.nih.gov/articles/PMC10644144)
- Cademartiri et al. (Int J Cardiovasc Imaging 2009, 64-slice CT), n = 62. Patients with LM plaque had larger LM dimensions (bifurcation diameter 6.0 vs 4.9 mm; length 11.3 vs 10.6 mm). Of patients with a normal ostial LAD, 72% had an LM bifurcation angle < 88.5°, whereas 63% of those with LAD disease had ≥ 88.5°. Plaques sat opposite the flow divider in > 90% of cases. [Springer s10554-009-9436-3](https://link.springer.com/article/10.1007/s10554-009-9436-3); [EUR repository](https://pure.eur.nl/en/publications/assessment-of-left-main-coronary-artery-atherosclerotic-burden-us/)
- Patients with LAD plaque had LM trunks on average 2.5 mm shorter, which suggests short LM as an LAD-atherosclerosis risk factor. Among 1,500 patients, 10.7% had a short LMCA and 8.9% a long one. [Surg Radiol Anat 2023](https://link.springer.com/article/10.1007/s00276-023-03193-w); [Diagn Interv Radiol 2015](https://dirjournal.org/pdf/beb8919b-f013-4ea1-b1c8-40332e840fe1/articles/dir.2015.15108/Diagn%20Interv%20Radiol-21-454-En.pdf)
- LM trifurcation angle has been reported as a geometric risk factor for the onset of coronary calcification. This comes from a search snippet whose primary source was not verified. [PMC5367806](https://pmc.ncbi.nlm.nih.gov/articles/PMC5367806)

**Myocardial bridging**
- CCTA prevalence ranges from 10% to 30% across studies. Bridges sit in the mid-distal LAD in about 95% of cases. Plaque concentrates just proximal to the bridge and spares the tunnelled segment. [PMC4818117](https://pmc.ncbi.nlm.nih.gov/articles/PMC4818117); [Pol J Radiol](https://www.polradiol.com/The-prevalence-of-myocardial-bridging-on-multidetector-computed-tomography-and-its-relation-to-coronary-plaques,126,38839,0,1.html)
- One study found plaque proximal to a bridge in 37.8% of patients, lower than the 48.7% in matched segments of patients without bridging. The authors concluded that bridging is not a significant patient-level risk factor compared with traditional risk factors. [EUR repository 24232](https://repub.eur.nl/pub/24232); [EUR prevalence study](https://pure.eur.nl/en/publications/prevalence-of-myocardial-bridging-and-correlation-with-coronary-a/)

### Inferences
- Of the features listed, V/M is the only whole-tree geometric descriptor with outcome data and demonstrated incremental value (NRI/IDI) over plaque and CT-FFR. It is also the most obvious missing candidate for a small feature set. It needs LV myocardial segmentation in addition to the lumen tree.
- V/M is partly downstream of plaque: lumen volume shrinks as stenoses form. At a single baseline scan it is therefore partly a plaque-burden proxy, not purely a constitutional trait. For a "who develops plaque" question it should be tested in plaque-free participants at baseline, or adjusted for plaque volume.
- Tortuosity is consistently linked to female sex, hypertension and age, and inversely to CAD. Turning angle aggregated to patient level may act mainly as a sex/age/hypertension surrogate. Any analysis should adjust for these, or the feature will look protective for confounded reasons.
- Dominance can be dropped as a risk predictor (null in prospective CONFIRM), although it is cheap and useful as a stratifier for where plaque goes.
- LM length and angle and myocardial bridging bear on localisation; no evidence was found that they identify at-risk individuals.

### Gaps
- No primary CGPS (Herlev–Østerbro) or DANCAVAS publication was found that relates lumen geometry (V/M, calibre, tortuosity, bifurcation angles) to plaque or events. A geometric analysis in CGPS appears to be novel, but this rests on a limited search.
- No MESA, Miami Heart, SCOT-HEART or ICONIC analysis of whole-tree lumen geometry as a predictor was found. Miami Heart and MESA image at baseline, but searches returned nothing geometric.
- No study was found of V/M in an asymptomatic general-population cohort, or for incident plaque in people without plaque at baseline.
- Coronary origin anomalies, number of branches or tree complexity, and total vessel length were not covered by any patient-level predictive study found here.
- The Taylor 2017 NXT V/M paper and the JCCT 2024 severe-CAD V/M paper were read only through abstracts or reviews (403 on full text).

## 2. Prospective/longitudinal versus cross-sectional evidence

### Takeaway
Prospective outcome evidence exists for dominance (CONFIRM, null) and for V/M (retrospective outcome cohorts in T2DM and TAVR, positive). Everything else (tortuosity, LM length and angle, bridging, calibre) is cross-sectional or angiographic. No longitudinal study found tests a lumen-geometric feature against incident plaque in an asymptomatic or general population.

### Cited Findings
- CONFIRM dominance analysis: prospective, multicentre, n = 6,382, 5-year follow-up, null. [eScholarship](https://www.escholarship.org/uc/item/7fg730bm)
- V/M in T2DM: retrospective cohort with longitudinal follow-up (median 3.8 years), positive and incremental. [PMC13151284](https://pmc.ncbi.nlm.nih.gov/articles/PMC13151284/)
- Tortuosity (Li 2011): follow-up of 2 to 4 years with no MACE difference. [PMC3164184](https://pmc.ncbi.nlm.nih.gov/articles/PMC3164184/)
- PARADIGM, the main serial-CCTA registry, has been used for machine-learning prediction of rapid plaque progression from clinical, lab and plaque features [JAHA 2020](https://www.ahajournals.org/doi/10.1161/JAHA.119.013958) and for radiomics predicting which normal segments develop new plaque [JCCT 2024](https://www.sciencedirect.com/science/article/abs/pii/S1934592524000327). Neither is described as using whole-tree lumen geometry.
- IVUS-based ML (XGBoost) predicted segment-level atheroma volume change at 13 months from baseline geometric plus clinical features under rosuvastatin. This is segment-level, not patient-level. [Sci Rep 2024](https://www.nature.com/articles/s41598-024-51508-7)
- Anchor for the target cohort: CGPS CCTA, n = 9,533 asymptomatic adults ≥ 40 years (mean age 60.2, 57.1% women), median 3.5 years follow-up, 71 MIs. Prevalence: 54% no atherosclerosis, 36% non-obstructive, 10% obstructive. Adjusted RR for MI was 9.19 for obstructive disease and 7.65 for extensive disease (Fuchs, Kühl, Kofoed et al., Ann Intern Med 2023). [TCTMD](https://www.tctmd.com/news/mi-risk-subclinical-cad-both-extent-and-stenosis-severity-matter); [Ann Intern Med](https://www.acpjournals.org/doi/10.7326/M22-3027); [Circulation 2021 prevalence paper, PMC8448414](https://pmc.ncbi.nlm.nih.gov/articles/PMC8448414/)

### Inferences
- With only 71 MIs, CGPS has very little power for event prediction from new geometric features. Plaque presence or extent (or progression, if repeat scans exist) is the realistic endpoint.
- A CGPS analysis of lumen geometry versus plaque would be cross-sectional unless a follow-up CCTA exists. This should be stated as a limitation, along with the reverse-causation issue for V/M and lumen calibre.

### Gaps
- Whether CGPS has repeat CCTA, which would allow an incident-plaque analysis, was not determined.
- The SCOT-HEART and ICONIC literature was not reached in this search for geometric predictors.

## 3. Incremental value of whole-tree geometry over clinical risk factors (age, sex, LDL, CAC)

### Takeaway
The only quantified incremental-value result found is for V/M on top of clinical and CCTA plaque models in T2DM (NRI 0.17, IDI 0.06). No study was found that tested whole-tree geometry against age, sex, LDL and CAC in an asymptomatic population. Plaque extent and stenosis themselves carry large effect sizes in CGPS (RR 8 to 12), which leaves a high bar for geometry.

### Cited Findings
- V/M added to clinical plus CCTA models (obstructive CAD, TPV > 750 mm³, CT-FFR): NRI 0.173, IDI 0.057; no C-statistic reported. [PMC13151284](https://pmc.ncbi.nlm.nih.gov/articles/PMC13151284/)
- NXT: V/M was independent of plaque measures for FFR ≤ 0.80. [PubMed 28789941](https://pubmed.ncbi.nlm.nih.gov/28789941)
- Li 2011: tortuosity was not independently prognostic, and its associations were dominated by sex and hypertension. [PMC3164184](https://pmc.ncbi.nlm.nih.gov/articles/PMC3164184/)
- Bridging is not significant against traditional risk factors. [EUR repository](https://repub.eur.nl/pub/24232)
- In CGPS, subclinical atherosclerosis predicted MI independently of conventional risk factors. [Ann Intern Med via research.regionh.dk](https://research.regionh.dk/en/publications/subclinical-coronary-atherosclerosis-and-risk-for-myocardial-infa/)

### Inferences
- A defensible thesis analysis is: outcome = plaque presence or extent; baseline model = age, sex, BSA, LDL, BP, smoking, diabetes (CAC optional, because it is almost collinear with plaque); then add geometric features and report ΔAUC/NRI. Normalising lumen measures to BSA or myocardial mass is essential, given the sex and BSA dependence.

### Gaps
- No study found compares geometric features with CAC directly in an asymptomatic cohort.

## 4. Studies aggregating local geometry (curvature, bifurcation angle) into patient-level risk

### Takeaway
Aggregation of local geometry to patient level has been done only in small, symptomatic, cross-sectional studies. The examples are a "≥3 bends of ≥45°" tortuosity flag and the LM–LAD angle times proximal tortuosity index for proximal LAD stenosis. No validated patient-level geometric risk score from local features was found.

### Cited Findings
- Li 2011 tortuosity flag (≥3 bends ≥45°), a patient-level binary aggregation of local turning angles, was inversely associated with CAD. [PMC3164184](https://pmc.ncbi.nlm.nih.gov/articles/PMC3164184/)
- Moon 2023 d20×cosθ index: OR 11.36 for proximal LAD stenosis. [PMC10644144](https://pmc.ncbi.nlm.nih.gov/articles/PMC10644144)
- Automated CCTA tortuosity scores were computed alongside CAC and correlated negatively with CAC volume. [APL Bioengineering 2024](https://doaj.org/article/682cc7f4ef964392a6e826332d875725)
- Segment-level ML on baseline geometry predicts plaque change, but under IVUS and statin treatment. [Sci Rep 2024](https://www.nature.com/articles/s41598-024-51508-7)

### Inferences
- The user's three local features (bifurcation diameter ratio, daughter angle, turning angle) have no established patient-level aggregation in the literature, so the choice of aggregate (mean, max, count above threshold, per-vessel) is a methodological contribution that must be justified.
- If one feature is added, V/M (or lumen volume indexed to BSA) is the best-evidenced whole-tree candidate. It complements the local features because it captures calibre and supply rather than shape.

### Gaps
- No search result covered tree complexity (branch count) or total centreline length as patient-level predictors.
