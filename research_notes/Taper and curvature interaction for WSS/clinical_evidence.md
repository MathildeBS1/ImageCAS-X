# Clinical and imaging evidence: coronary taper, curvature/tortuosity and plaque location, formation and progression

Scope: human coronary studies (CCTA, IVUS, angiography, autopsy). Animal and pure-CFD work is flagged separately. For each study the notes say whether it is cross-sectional (association) or longitudinal (prediction). Reported numbers come from abstracts and secondary summaries reached by search; where the full text was not read, the notes say so.

## 1. Does geometry (or geometry-derived WSS) predict future plaque location or progression?

### Takeaway
The longitudinal evidence that local haemodynamics predicts where plaque grows comes mainly from invasive IVUS + angiography CFD studies of *already diseased* arteries, followed for 6–12 months: Stone 2003 and 2007, PREDICTION 2012, and Samady/McDaniel 2011. In these studies low ESS/WSS predicts plaque growth and lumen loss, independently of and in addition to baseline plaque burden. CCTA-based studies show that geometry and CT-derived WSS mark future ACS culprits (ICONIC/Han 2022, EMERALD). No study found tests raw geometry (curvature, taper) as a predictor of *new* plaque in plaque-free segments. The closest is a PARADIGM radiomics study of 9,583 normal segments.

### Cited Findings
**Invasive serial studies (longitudinal, diseased arteries)**
- Stone et al. 2003 (Circulation 108:438–444; PMID 12860915). IVUS, biplane angiography and flow were used to make 3D reconstructions of 12 arteries in 8 patients (6 native, 6 stented), followed for 6 months. In native arteries, regions with low baseline ESS showed more plaque thickening with outward remodelling, so the lumen radius did not change. Regions with physiological ESS changed little. — [Wahle/Uiowa abstract page](https://user.engineering.uiowa.edu/~awahle/WahLIT/Abstracts/ston03b-cfd.html); [Uiowa repository](https://iro.uiowa.edu/esploro/outputs/journalArticle/Effect-of-Endothelial-Shear-Stress-on/9984047643502771)
- Stone et al. 2007 (Eur Heart J), 13 patients. Plaque progressed in subsegments with low ESS, with either constrictive or expansive remodelling. Low-ESS subsegments progressed more often: 33.3% vs 7.9% for moderate or higher ESS (P = 0.009, adjusted for clustering of lesions within patients). — [Wahle/Uiowa abstract](https://user.engineering.uiowa.edu/~awahle/WahLIT/Abstracts/ston07-cfd.html)
- PREDICTION (Stone et al., Circulation 2012;126:172–181; DOI 10.1161/CIRCULATIONAHA.112.096438):
  - Design: 506 ACS patients after PCI had 3-vessel IVUS/angiographic profiling (mean 2.7 arteries per patient), divided into 3-mm segments. 374 (74%) were re-imaged at 6–10 months.
  - Primary endpoint (increase in plaque area): predicted by large baseline plaque burden.
  - Lumen-area decrease: independently predicted by large plaque burden **and** low ESS.
  - The combined predictors gave PPV 41% and NPV 92% for progression of an obstruction requiring PCI.
  - Authors' conclusion: plaque burden and low ESS give "independent and additive prediction".
  - The ORs and segment counts were not in the abstract. — [PubMed 22723305](https://pubmed.ncbi.nlm.nih.gov/22723305/); [ClinicalTrials.gov NCT01316159](https://clinicaltrials.gov/study/NCT01316159); [TCTMD](https://www.tctmd.com/news/endothelial-shear-stress-works-prediction-tool)
- McDaniel/Samady et al. 2011 (Circulation 124:779–788), patients with CAD on atorvastatin:
  - Imaging: IVUS-VH and Doppler-derived WSS at baseline and 6 months.
  - Low-WSS segments had more plaque and necrotic core progression, and constrictive remodelling.
  - High-WSS segments had necrotic core and calcium progression, fibrous regression and excessive expansive remodelling, a shift toward a vulnerable phenotype. — [Houston Methodist Scholars](https://scholars.houstonmethodist.org/en/publications/coronary-artery-wall-shear-stress-is-associated-with-progression-/); [AHA journal page](https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.111.021824)
- Combined plaque structural stress (PSS) and WSS have been studied for progression, regression and composition change. This is a later extension of the same idea. — [PMC6503452](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6503452/)
- Multidirectional WSS (VH-IVUS, 20 patients) was mainly associated with *composition* change rather than plaque size. — [EuroIntervention PDF](https://eurointervention.pcronline.com/article/the-influence-of-multidirectional-shear-stress-on-plaque-progression-and-composition-changes-in-human-coronary-arteries/pdf)
- Method sensitivity:
  - Low-WSS sectors progressed more than mid- and high-WSS sectors for every definition of "low" tested.
  - Absolute WSS varies so much between individuals that absolute thresholds were not appropriate.
  - Patient flow rate and the exclusion of side branches change the observed WSS–progression associations substantially.
  - Sources: [Sci Rep 2021 / PMC8586146](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8586146/); [PMC4306111](https://pmc.ncbi.nlm.nih.gov/articles/PMC4306111/)
- A meta-analysis of serial studies with baseline CFD WSS found that low WSS was associated with lumen-area reduction, plaque-burden increase and necrotic-core increase. — [Int J Cardiol 2024 meta-analysis](https://www.sciencedirect.com/science/article/abs/pii/S0167527324006818)

**CCTA-based studies (longitudinal, mostly diseased or culprit outcomes)**
- Han D et al., JAMA Cardiol 2022;7:309–319 (ICONIC nested case-control):
  - Population: 116 patients with ACS whose culprit-lesion precursor was visible on baseline CCTA, against 116 propensity-matched non-ACS controls.
  - Adverse geometric characteristics (AGCs): distance from the ostium, bifurcation location and tortuosity. Tortuosity was defined as 1 bend >90° or 3 curves of 45–90°.
  - Precursors sat closer to the ostium (median 35.1 vs 44.5 mm) and more often at a bifurcation (73.3% vs 38.9%). Tortuosity was rare in both groups (4.3% vs 1.4%; all P < .05).
  - HR 2.90 for 1 AGC and 6.84 for ≥2 AGCs.
  - Adding AGCs to stenosis and plaque features raised the AUC from 0.733 to 0.766.
  - The authors say AGCs add prognostic information beyond plaque assessment. — [ACC Journal Scan](https://www.acc.org/Latest-in-Cardiology/Journal-Scans/2022/02/04/18/53/Association-of-Plaque-Location); [JAMA Cardiol](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
- EMERALD (Lee JM, Choi G, Koo BK et al., JACC Cardiovasc Imaging 2019;12:1032–1043):
  - Data: CCTA taken before ACS. 66 culprit vs 150 non-culprit lesions in 72 patients; another write-up gives 75 culprits among 226 lesions.
  - Culprits had higher ΔFFRCT, WSS and axial plaque stress (APS), all p < 0.01.
  - Means: WSS 221.8 vs 145.5 dyn/cm² (p < 0.001); APS 2585.9 vs 1734.7 dyn/cm² (p = 0.006).
  - Note: here *high* WSS marks the rupture site, not low WSS marking the growth site. — [Frontiers/PMC8475759](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8475759/); [Healio](https://cm.healio.com/news/cardiology/20160603/emerald-ffrct-accurately-predicts-which-plaques-cause-acs); [EMERALD II registration](https://clinicaltrials.gov/study/NCT03591328)
- A preliminary CCTA-CFD serial study (n = 22) found:
  - Progression: normalised minimum WSS (OR 0.38, p < 0.001) and maximum helicity (OR 1.44, p = 0.016).
  - Regression: average vorticity and gradient oscillatory number. — [PMC12858539](https://pmc.ncbi.nlm.nih.gov/articles/PMC12858539/)
- PARADIGM radiomics (Lee et al., J Cardiovasc Comput Tomogr 2024;18:274–280; PMID 38378314):
  - Data: 9,583 segments that were **normal at baseline**, from 1,162 patients. 9.8% developed new plaque on follow-up CCTA.
  - C-index: about 0.70 for the clinical-only model and about 0.70 for the radiomics-only model.
  - Clinical plus radiomics gave a C-index of 0.772 (training) and 0.767 (test), a significant improvement.
  - This is texture, not geometry, but it is the closest design analogue to the "where" question. — [Yonsei repository](https://ir.ymlib.yonsei.ac.kr/handle/22282913/200058); [JCCT abstract](https://www.journalofcardiovascularct.com/article/S1934-5925(24)00032-7/abstract)
- Patient-level outcome: low coronary artery volume index (CAVi <28 mm³/g, on CCTA) was associated with about 4× more cardiovascular events over 4.6 years in 325 patients, regardless of stenosis (Benetos 2020, Int J Cardiovasc Imaging). — [Review PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)

### Inferences
- In the invasive serial studies the baseline is diseased, the follow-up short (6–12 months) and patients largely post-ACS or post-PCI. Moving their effect sizes to a plaque-free baseline with a 10-year horizon is an extrapolation.
- WSS is a *derived* quantity: it combines geometry (diameter, curvature, taper, branching) with flow. Raw geometric descriptors such as curvature or taper are expected to carry a weaker, diluted version of the WSS signal.
- The direction depends on the endpoint. Low WSS goes with growth and new plaque. High WSS and APS go with the rupture site (EMERALD, and Samady's high-WSS vulnerable phenotype). For an outcome of new plaque of any grade, "low WSS" geometry is the relevant hypothesis.

### Gaps
- No human study found that uses baseline curvature or taper (rather than WSS) to predict *new* plaque in plaque-free segments on serial CCTA.
- The full-text ORs for PREDICTION and the AUCs for the PARADIGM radiomics paper were not retrieved.

## 2. Evidence on coronary taper (tapering ratio, abnormal/reversed tapering) and plaque

### Takeaway
Taper is mostly described as a normal physiological property, or treated as a confounder of FFR-CT. Direct human evidence linking a taper metric to plaque presence or progression is thin. Older IVUS and angiographic work shows that lumen taper in diseased arteries partly reflects *differential plaque accumulation*, which is a reverse-causation problem. Diffuse disease shrinks the lumen relative to the supplied myocardium. No CCTA study was found in which taper predicts future plaque.

### Cited Findings
- Angiographic lumen tapering averages about 0.22 mm per 10 mm of arterial length and is almost always present. Reversed tapering occurs in about 10% of arteries. — [ResearchGate: "Normal angiographic tapering of the coronary arteries"](https://www.researchgate.net/publication/11090643_Normal_angiographic_tapering_of_the_coronary_arteries)
- IVUS (Am J Cardiol) findings on lumen tapering:
  - The LAD tapers more steeply (0.33 mm/10 mm) than the RCA (0.16) or LCx (0.15); p = 0.0061 for LAD vs RCA.
  - The mechanism varies with lesion location: tapering of the external elastic membrane in some places, differential plaque accumulation in others. — [DOI 10.1016/s0002-9149(00)80072-7](https://doi.org/10.1016/s0002-9149(00)80072-7)
- Seiler et al. (angiography): lumen area scales with the summed distal branch length and the supplied myocardial mass. In CAD patients the lumen is diffusely 30–50% too small for the distal bed. Diffuse disease therefore changes calibre and taper along the whole vessel, not only at focal lesions. — [Synapse record of the abstract](https://synapsesocial.com/papers/W1967018012)
- In FFR-CT, physiological tapering can push distal FFR-CT below 0.8 and cause false positives. A gradual distal decline without a focal lesion may instead indicate diffuse atherosclerosis. In 443 RCAs, the volume/length ratio was the strongest predictor of distal FFR-CT (cut-off 8.1 mm³/mm), and the authors suggest tapering contributes. — [Eur Radiol 2023, RCA morphology](https://link.springer.com/article/10.1007/s00330-023-09972-8); [RSNA RadioGraphics FFR-CT guide](https://pubs.rsna.org/doi/full/10.1148/rg.210097)
- A large 2022 review of coronary geometry vs plaque on CCTA (PMC9497479) does **not** discuss taper at all. This marks taper as an under-studied descriptor. — [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)
- Proxies for calibre and volume:
  - CAVi (lumen volume over myocardial mass) is prognostic (Benetos 2020, above).
  - CAVi is independently associated with abnormal stress myocardial blood flow on PET, adding to stenosis severity (Benetos 2021, Eur Radiol, n = 60). — [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)

### Inferences
- On a plaque-free baseline, measured lumen taper mostly reflects outer-vessel taper and the branching and myocardial-mass pattern. That makes it a cleaner exposure than in diseased cohorts. Residual subclinical (CT-invisible) wall thickening could still bias it.
- Vessel differences in taper (LAD steeper) mean taper is confounded with vessel and position. Per-segment models need position or vessel in the base model, as in the clogit design.

### Gaps
- No human CCTA or IVUS study was found that defines a "tapering ratio" and relates it, alone or with curvature, to future plaque. Older angiographic papers on "abnormal tapering" in CAD may exist, but none was retrieved and verified in this search.
- No study was found that reports positive vs negative (reversed) taper as a plaque risk factor with effect sizes.

## 3. Curvature and tortuosity vs plaque: inner curvature, and more or less atherosclerosis?

### Takeaway
Curvature is fairly consistently associated with plaque presence (cross-sectional CCTA) and with circumferential plaque thickness on the inner bend (IVUS fusion). Global tortuosity is inconsistent: from no association, to a segment-level association, to an *inverse* association with calcium. Studies that combine curvature and torsion (and their cyclic change) explain more wall-thickness variance than single parameters.

### Cited Findings
- Tuncay et al. 2018 (J Cardiovasc Comput Tomogr 12:257–260), 73 patients, end-diastolic CCTA, RCA:
  - Curvature was higher in segments with stenosis and with plaque, at segment and artery level. Curvature was 16.7% higher in stenotic segments and 13.8% in stenotic arteries.
  - Calcified and mixed-plaque segments were more curved than plaque-free segments.
  - At artery level, curvature was associated with plaque but not with significant stenosis.
  - Cross-sectional. — [ESCR 2014 poster](https://epos.myesr.org/poster/escr/escr2014/458); [review PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)
  - **Conflict on tortuosity within the same group:** the ESCR abstract reports *no* association of tortuosity with plaque or stenosis, while the published review says tortuosity was associated with plaque at segment level only. — [ESCR poster](https://epos.myesr.org/poster/escr/escr2014/458) vs [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)
- Nannini et al. 2024 (APL Bioengineering), automated CCTA:
  - Patients with higher tortuosity had *lower* calcium volume (p < 0.001).
  - Within vessels, tortuosity rose from proximal to distal while calcium fell. Position may therefore confound the inverse association. — [Polimi repository](https://re.public.polimi.it/handle/11311/1276541); [DOAJ](https://doaj.org/article/682cc7f4ef964392a6e826332d875725)
- Han 2022 (ICONIC): tortuous lesions were more frequent among future ACS culprits (4.3% vs 1.4%), but the counts were very small. — [ACC Journal Scan](https://www.acc.org/Latest-in-Cardiology/Journal-Scans/2022/02/04/18/53/Association-of-Plaque-Location)
- Moon et al. 2023 (Quant Imaging Med Surg 13:7459–7466), 133 patients, cross-sectional CTA:
  - Measures: proximal LAD tortuosity (d20 = chord over the first 20 mm) and the LM–LAD angle (29.2° vs 38.3° for <50% vs ≥50% stenosis, P < 0.001).
  - d20 alone was not significant (P = 0.104), with AUC 0.634.
  - The product d20×cosθ <15.5 was a multivariable predictor of severe proximal LAD stenosis: OR 11.36 (3.9–39.5), AUC 0.767, adjusted for hypertension and pack-years. — [PMC10644144](https://pmc.ncbi.nlm.nih.gov/articles/PMC10644144)
- Inner curvature on IVUS fused with biplane angiography (Wahle, Sonka et al.):
  - 12 patients: combinations of inner curvature with above-average plaque outweighed the opposite combinations in most vessels.
  - 37 segments from 31 patients: the hypothesis held in most vessels (p < 0.001), and the effect grew with curvature.
  - 48 segments: circumferential plaque thickness correlated more strongly with local curvature than with WSS.
  - A 2004 paper found no direct relationship in *complex* geometries.
  - Sources: [Wahle 2003 abstract](https://user.engineering.uiowa.edu/~awahle/WahLIT/Abstracts/wahl03b-cfd.html); [Wahle 2006 abstract](https://user.engineering.uiowa.edu/~awahle/WahLIT/Abstracts/wahl06a-cfd.html); [Wahle 2004 abstract](https://user.engineering.uiowa.edu/~awahle/WahLIT/Abstracts/wahl04a-cfd.html); [Uiowa repository](https://iro.uiowa.edu/esploro/outputs/journalArticle/Plaque-development-vessel-curvature-and-wall/9984020755602771)
- Zhu & Friedman 2003 (ATVB 23:2260–2265), RCA, biplane cine-angiography with IVUS:
  - Time-averaged curvature and torsion, and their cyclic excursion, correlated with maximum wall thickness and asymmetry when combined (R² 0.17–0.44).
  - Single parameters did not correlate.
  - This is the clearest human evidence that *combinations* of geometric descriptors matter. — [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)
- Friedman et al. 1996 (Atherosclerosis), lesion-free autopsy hearts: branch angle and local curvature correlated with intimal thickness *before overt disease*. This is relevant to a plaque-free baseline. — [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)
- Katranas 2013 (Int J Cardiol), CCTA with CFD: curvature was higher in systole and in atherosclerotic segments, and ESS was lower there. — [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)
- Cardiac-cycle effects:
  - van Zandwijk 2020 (J Digit Imaging): curvature was higher at end-systole than at end-diastole.
  - The change in geometry over the cycle was not associated with stenosis degree or plaque type.
  - Phase choice therefore affects curvature values. — [PMC7165136](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7165136/)
- IVUS-based fluid–structure interaction model (10 patients):
  - At peak pressure and curvature, wall thickness correlated positively with flow shear stress in 9 of 10 patients and negatively with plaque wall stress in 9 of 10.
  - The correlations were weaker at minimum curvature.
  - Cross-sectional, in established plaque. — [PMC3977946](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3977946/)
- Older bifurcation and left-main geometry studies:
  - Saltissi 1979: a short LM with a wide bifurcation angle was associated with proximal disease.
  - Friedman 1993: relative proximal involvement correlated negatively with LM branch angle.
  - Svindland 1983: plaque sits on the outer (lateral) walls at the left bifurcation and spares the flow divider.
  - Source: [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)
- Tortuosity has no standard definition. Studies use a length/chord index, bend-angle counts (Han), or a chord over a fixed length (Moon). — [Case report PMC10335608](https://pmc.ncbi.nlm.nih.gov/articles/PMC10335608/); [PMC10644144](https://pmc.ncbi.nlm.nih.gov/articles/PMC10644144)

**Model-only (non-clinical) evidence, kept separate:**
- Pinho 2019 (CFD, n = 8–10): high calibre, wide angles and tortuosity gave a plaque-prone LAD flow profile; higher curvature in some configurations gave a "resistant" profile.
- Malvè 2015 (dynamic CT-CFD): LM/LAD tortuosity was associated with low WSS in the proximal LAD.
- Chiastra 2017: the effect of curvature on flow is magnified in stenotic vessels.
- Sources: [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/); [arXiv 2312.00257, left-coronary anatomy vs haemodynamics](https://arxiv.org/pdf/2312.00257)

**Animal:** experimental (porcine) work from Stone's group on the natural history of coronary atherosclerosis and low ESS supports the low-ESS → plaque-initiation mechanism. The details were not retrieved here. — [MIT DSpace record](https://dspace.mit.edu/entities/publication/456c02b2-89b9-434b-bd4f-3a2a5c142f5d)

### Inferences
- Local curvature (a segment-level maximum or mean) is the better-supported descriptor. Global tortuosity indices may mix in age and hypertension effects (both cause tortuosity) and distal position (more tortuous, less calcified), which could explain the inverse findings.
- Inner-curvature localisation is a *within-segment* (circumferential) effect. Per-segment curvature can only proxy it, so the expected per-segment effect sizes are modest.

### Gaps
- No OCT study of the inner-curvature effect was found.
- No longitudinal CCTA study relating baseline curvature to new plaque was found.

## 4. Taper and curvature together: interaction or effect modification

### Takeaway
No human clinical study was found that tests taper and curvature together in one model, includes a taper × curvature interaction term, or reports that one modifies the other's effect on plaque. Combination evidence is limited to three sources. Zhu & Friedman 2003 found curvature with torsion jointly explained wall thickness while single parameters did not. Moon 2023 found a product of tortuosity and LM–LAD angle stronger than either alone. Han 2022 found that counting multiple adverse geometric features gave a graded HR.

### Cited Findings
- Curvature with torsion (and their cyclic excursion) jointly correlated with wall thickness (R² 0.17–0.44); single parameters did not. — [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)
- d20 × cosθ (tortuosity × angle) predicted stenosis (AUC 0.767) better than either component (0.634 and 0.743). This is an empirical product term, not a fitted interaction. — [PMC10644144](https://pmc.ncbi.nlm.nih.gov/articles/PMC10644144)
- ≥2 AGCs gave HR 6.84 vs 2.90 for 1 AGC. This is additive counting, not an interaction test. — [ACC Journal Scan](https://www.acc.org/Latest-in-Cardiology/Journal-Scans/2022/02/04/18/53/Association-of-Plaque-Location)
- Two further combination findings:
  - Saltissi 1979: short LM plus a wide bifurcation angle was associated with proximal disease more strongly than short LM alone, a joint geometric effect.
  - Chiastra 2017 (model): the curvature effect on flow is magnified in stenotic vessels.
  - Source: [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)
- In PREDICTION, low ESS and large plaque burden were "independent and additive" predictors. Geometry and flow and wall status combine, but no interaction was reported. — [PubMed 22723305](https://pubmed.ncbi.nlm.nih.gov/22723305/)
- A search for "taper + curvature + plaque" in IVUS/CFD returned no human study that models taper explicitly. — [PMC3977946](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3977946/) (closest: curvature-phase × stress)

### Inferences
- Testing a taper × curvature interaction would be novel in the clinical literature. With no prior effect sizes, any interaction should be prespecified as exploratory and not folded into the primary LR test, because power for interactions is low.
- Physically, taper accelerates flow and raises WSS, while curvature creates low WSS on the inner wall. Effect modification is therefore plausible: a curved segment that tapers weakly may be most low-WSS-prone. This is mechanistic reasoning, not evidence.

### Gaps
- No human study with a taper × curvature term was found. No retrieved study reported stratified curvature effects by taper level.

## 5. Added value beyond position or clinical risk factors, and reverse causation

### Takeaway
Few studies quantify geometry's added value:
- Beyond plaque features: Han 2022 (AUC 0.733 → 0.766).
- Beyond hypertension and smoking: Moon 2023 (OR 11.4).
- Clinical model plus radiomics in normal segments (C-index 0.70 → 0.77), which shows segment-level CT information can add to clinical factors for new plaque.

No study was found that tests geometry beyond *anatomical position* (proximal vs distal segment). Reverse causation is rarely addressed explicitly. Lumen taper in diseased arteries partly reflects plaque, and position confounds both tortuosity and calcium.

### Cited Findings
- Han 2022: geometric features added discrimination over stenosis and plaque features (AUC 0.733 → 0.766). Distance from the ostium, a position variable, was itself one of the "geometric" features. — [ACC Journal Scan](https://www.acc.org/Latest-in-Cardiology/Journal-Scans/2022/02/04/18/53/Association-of-Plaque-Location)
- PARADIGM radiomics: clinical only ~0.70, clinical plus radiomics 0.767 (test set), for new plaque in baseline-normal segments. — [Yonsei repository](https://ir.ymlib.yonsei.ac.kr/handle/22282913/200058)
- Moon 2023: the geometric product stayed significant with hypertension (OR 4.54) and pack-years (OR 1.04) in the model. Cut-offs were derived and tested in the same cohort (overfitting). — [PMC10644144](https://pmc.ncbi.nlm.nih.gov/articles/PMC10644144)
- Friedman 1993 used a *relative* proximal-involvement index to remove systemic risk-factor effects from geometry–plaque associations, an early within-person design. — [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)
- Reverse causation:
  - IVUS shows lumen tapering partly reflects differential plaque accumulation. — [DOI 10.1016/s0002-9149(00)80072-7](https://doi.org/10.1016/s0002-9149(00)80072-7)
  - Diffuse CAD makes lumens 30–50% too small for the bed. — [Synapse/Seiler](https://synapsesocial.com/papers/W1967018012)
  - Low-ESS regions undergo outward remodelling with preserved lumen, so plaque can grow without changing lumen geometry, and later change it. — [Stone 2003 abstract](https://user.engineering.uiowa.edu/~awahle/WahLIT/Abstracts/ston03b-cfd.html)
- Position confounding: tortuosity rises and calcium falls from proximal to distal. — [Polimi/Nannini 2024](https://re.public.polimi.it/handle/11311/1276541)
- Lesion-free autopsy hearts showed curvature and branch-angle associations with intimal thickening *before* plaque. This supports geometry → wall change and not only the reverse. — [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)

### Inferences
- A plaque-free baseline (SIS = SSS = 0) removes most of the reverse-causation problem for lumen geometry. Subclinical, CT-invisible wall thickening and positive remodelling can still alter diameter and taper. Using an outer-wall or lumen measure in plaque-free segments, and the earliest scan, is the best available control.
- Since position strongly determines both geometry (taper, tortuosity) and plaque (proximal predilection), a conditional within-person model with position in the base is the right test. The literature offers no precedent effect size for geometry beyond position.

### Gaps
- No study was found that adjusts geometry–plaque associations for segment position and reports the incremental effect.
- No study was found that tests geometry beyond SCORE2 or other clinical risk scores for person-level new plaque.
- Follow-up in the geometry/WSS literature is 6 months to about 5 years. No 10-year serial geometry study was found.
