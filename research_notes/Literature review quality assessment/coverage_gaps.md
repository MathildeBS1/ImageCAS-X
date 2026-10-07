# Literature review coverage gaps: coronary geometry as a risk factor for plaque/CAD

Scope assessed: `thesis/literature_review/literature_review.tex` (state 2026-10-04) against the aims in
`thesis/introduction/01_introduction.tex`. The intro says the thesis will (1) build an automated pipeline
that computes branching angles, branch radius ratios and vessel curvature, and (2) use these to predict
new plaque at a 10-year CGPS rescan, with a logistic regression and a curvature-profile transformer
judged against an age+sex baseline, fitted per artery.

The review currently cites 13 works: Asakura 1990, Chatzizisis 2007, van der Giessen 2009, Li 2011,
Kashyap 2022, Garcha 2025, Griffo 2026, Bransby 2026, Wang 2004, Tello Ayala 2026, Glagov 1987,
Sakellarios 2017, SCORE2 2021. The two gaps it claims are: (G1) studies relate geometry to simulated WSS or
to disease already present, cover one region (left main bifurcation or RCA), and the flow-in-patients
studies have "at most several hundred individuals"; (G2) no study combines consistent whole-tree geometry
with follow-up of a general population from a plaque-free state to new plaque, and risk scores use
systemic factors only.

Method: read the chapter, intro, `knowledge/docs_thesis/literature.md`, `find_research.md` and
`thesis/refs.bib` (to separate "author knows it and left it out" from "author has not found it"), then
web and Europe PMC searches on 2018 to 2026 literature. Studies marked **[in refs.bib]** are already in the
author's bibliography but not cited in this chapter. Claims are abstract-level unless noted.

## Which landmark and recent studies on coronary geometry and plaque/CAD/outcomes are missing?

### Takeaway
The biggest hole is that the three features the thesis actually computes (bifurcation angle, radius
ratio, curvature) have almost no clinical-cohort literature in the chapter: there is no clinical
bifurcation-angle study at all, curvature comes in only through Kashyap's simulation, and the single most
relevant CCTA geometry-to-outcome study, Han 2022 (ICONIC), is cited in the intro but left out of the
review. Most of the must-cite papers are already in refs.bib, so filling the gap is cheap.

### Cited Findings

**MUST-CITE: CCTA geometry and future events (the closest prior work to the thesis aim)**
- Han D, et al. Association of plaque location and vessel geometry determined by CCTA with future ACS-causing culprit lesions. *JAMA Cardiol* 2022;7(3):309-319. doi:10.1001/jamacardio.2021.5705. ICONIC nested case-control: 548 lesions in 116 patients with incident ACS after CCTA. Culprit precursors were closer to the ostium (median 35.1 vs 44.5 mm), more often at bifurcations (73.3% vs 38.9%) and more often in tortuous segments (4.3% vs 1.4%), all P<.05. **[in refs.bib; cited in intro, not in review]**. Why it matters: it is the only large CCTA study linking baseline vessel geometry to *future* events, it is a counterexample to "geometry was only related to disease already present", and it bears directly on the gap claim. — [Houston Methodist record](https://scholars.houstonmethodist.org/en/publications/association-of-plaque-location-and-vessel-geometry-determined-by-/); [PMC8792800](https://pmc.ncbi.nlm.nih.gov/articles/PMC8792800)
- Tommasino A, et al. CLAP score. *J Cardiovasc Dev Dis* 2024;11(11):338. doi:10.3390/jcdd11110338, PMID 39590181. n=499 CCTA patients with follow-up; left main bifurcation angle >80° was the strongest MACE predictor (reported HR 4.47; the CI 3.80-6.70 looks odd and needs checking in the full text). **[in refs.bib]**. Why: the only outcome study for bifurcation angle. — [PMC11595042](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11595042/); interval caveat from `find_research.md` §1.1

**MUST-CITE: bifurcation angle vs CAD (the thesis computes branching angles, but the review has no clinical angle study)**
- Juan YH, et al. 2017, n=313 CCTA: LM bifurcation angle 75.5° (normal), 81.2° (non-significant), 87.3° (significant stenosis). **[in refs.bib]** — per `find_research.md` §1.1 (abstract-level)
- Cui Y, et al. *PLoS ONE* 2017;12(3):e0174352. doi:10.1371/journal.pone.0174352, PMID 28346530. n=106 CCTA+ICA; LAD-LCx angle was an independent predictor of significant left stenosis (OR 1.423) and wider in non-calcified plaque. **[in refs.bib]** — [PMC5367806](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5367806/)
- Bekirçavuşoğlu et al. *Clin Radiol* 2026;96:107299. doi:10.1016/j.crad.2026.107299, PMID 41962318. n=1380 CCTA; ramus intermedius (which widens the LM angle) was the strongest risk factor for plaque in LM/proximal LAD/LCx. **[in refs.bib]**. Why: the largest tree-scale geometry cohort, and it shows that branching *topology* affects plaque. — per `find_research.md` §1.4
- Givehchi S, et al. *Phys Med* 2018;45:198-204. doi:10.1016/j.ejmp.2017.09.137, PMID 29373248. Two standard CCTA angle-measurement techniques disagreed by 12.0° ± 10.6° in 50 patients, which is the same size as the normal-to-stenosis gradient in Juan 2017. **[in refs.bib]**. Why: this strengthens the review's "measure determines the finding" paragraph far more than Li/Kashyap alone, and it justifies an automated definition. — per `find_research.md` §5.1
- Nice-to-have (newer, same direction): Temov & Sun 2016 (n=196, angle varies 35.5°-178°, depends on sex and BMI) **[in refs.bib, cited in intro comment]**; Mansouri 2024 *Health Sci Rep* 7:e2182 (n=122, angle vs Gensini r=0.684) **[in refs.bib]**; Moradi M, et al. *ARYA Atheroscler* 2026;22:41-47, doi:10.48305/arya.2025.45215.3052, PMID 41972218 (n=578 CCTA, wider LAD-LCX and LM-LAD angles go with greater pLAD stenosis) **[not in refs.bib]**; Zhang 2023 RI propensity-matched null (n=200) **[in refs.bib]**. — [Europe PMC 41972218](https://europepmc.org/article/MED/41972218)

**MUST-CITE: curvature (the transformer input), which the review supports only with Kashyap's simulation**
- Zhang M, Gharleghi R, Shen C, Beier S. A new understanding of coronary curvature and haemodynamic impact on the course of plaque onset and progression. *R Soc Open Sci* 2024;11:241267. doi:10.1098/rsos.241267, PMID 39309260. 39 ASOCA left trees (20 non-stenosed, 19 stenosed), analysed as whole tree, bifurcating and non-bifurcating segments. **[in refs.bib, read in full; listed in the chapter's own planning comment as part of gap 2 but dropped from the text]**. Why: it is the whole-tree curvature-to-WSS study and the direct precedent for "geometry at plaque *onset*". Its cohort (n=39) supports the cohort-size claim in G1. Do not count `shen2025helical` as a second cohort; it uses the same 39 trees. — [Europe PMC](https://europepmc.org/article/MED/39309260)
- Iwami T, et al. *Am J Cardiol* 1998;82:381-384. doi:10.1016/s0002-9149(98)00340-3, PMID 9708671. IVUS: plaque forms on the inner arc of curved LAD segments, and greater curvature goes with more inner-wall plaque. Why: in vivo human evidence for the Asakura inner-bend claim. **[not in refs.bib]** — [Europe PMC 9708671](https://europepmc.org/article/MED/9708671)
- Wahle A, et al. *Med Image Anal* 2006;10:615-631. doi:10.1016/j.media.2006.03.002, PMID 16644262. Angio+IVUS fusion: circumferential plaque distribution depends on local curvature in most vessels; plaque-WSS correlation in 48 segments. Nice-to-have. **[not in refs.bib]** — [Europe PMC 16644262](https://europepmc.org/article/MED/16644262)
- van Zandwijk JK, et al. *J Digit Imaging* 2020;33:480-489. doi:10.1007/s10278-019-00300-5. n=71 CCTA; curvature changes across the cardiac cycle (0.090 vs 0.081 mm⁻¹). Why: reconstruction phase is a measurement confounder for any CCTA curvature feature. **[in refs.bib]** — per refs.bib note

**SHOULD-CITE: dominance (relevant if fitting per artery or stratifying)**
- Gebhard C, et al. CONFIRM. *Eur Heart J Cardiovasc Imaging* 2015;16(8):853-862. doi:10.1093/ehjci/jeu314. n=6382 CCTA, 60-month follow-up; dominance did not predict survival overall. Khan 2016 meta-analysis (255,718 ACS patients): left dominance OR 1.27 for mortality. Veltman 2012: HR 3.20 (n=1425). **[all in refs.bib]**. Why: CONFIRM is the largest CCTA "anatomy and outcome" cohort, and dominance decides how per-artery models are defined. — per `find_research.md` §1.3

**SHOULD-CITE: radius ratios / Murray's law (the thesis computes branch radius ratios)**
- The review's only radius-ratio source is Garcha 2025 (synthetic). Schoenenberger 2012, Finet 2008, Huo 2012 and Taylor 2024 (Murray exponent) are **[in refs.bib]**. `find_research.md` ("Not searched") records that no study relating deviation from Murray's law to clinical plaque was searched for; I did not find one either. Why: one sentence is enough to say the radius-ratio feature rests on scaling laws plus simulation, with no clinical cohort behind it.

**Nice-to-have: other geometry features**
- Myocardial bridging: Chen YC, et al. *Eur Heart J Cardiovasc Imaging* 2024;25:1462-1471. doi:10.1093/ehjci/jeae135, PMID 38781436. n=295 patients with LAD myocardial bridge and **no proximal plaque at index CCTA**, repeated CCTA; a vascular radiomics model (centreline and cross-section) predicted new proximal plaque, external AUC 0.75. See also the gap discussion below. **[not in refs.bib]** — [Europe PMC 38781436](https://europepmc.org/article/MED/38781436)
- Left main dimensions: Cademartiri et al. (64-slice CT, n=62): larger LM diameters with LM plaque. Small and old; mention only if LM length is a feature. — [EUR repository](https://repub.eur.nl/pub/24227)

### Inferences
- An examiner reading the intro (angles, radius ratios, curvature) and then the review will look for the clinical evidence on each feature. Right now angles have only a simulation (Garcha), curvature only a simulation (Kashyap), and radius ratios only a simulation (Garcha). Adding Juan/Cui/Bekirçavuşoğlu/Tommasino, Zhang 2024 + Iwami, and one Murray sentence closes this with papers the author mostly already holds.
- Han 2022 is the most damaging omission. It is in refs.bib, cited in the intro, and it is CCTA, outcome-based and geometric. Leaving it out of the review makes the "geometry only vs present disease" framing look selective.

### Gaps
- I did not find a published CCTA study relating deviation from Murray's law or daughter radius ratio to clinical plaque in patients. That absence is consistent with `find_research.md`, but neither search was exhaustive.
- CArTI (AHA 2025 abstract, AI coronary tortuosity index vs 5-year MACE, doi:10.1161/circ.152.suppl_3.4365988): I found no full paper as of 2026-10-04.
- Özyaşar et al. 2024 (*Turk Kardiyol Dern Ars* 52:553-560, n=388, tortuosity vs Gensini): the direction of the association could not be confirmed from the abstract snippet.

## Is there literature on wall shear stress / hemodynamics vs geometry-only predictors that the review should engage?

### Takeaway
Yes. The review treats WSS mechanistically (Asakura, Chatzizisis, van der Giessen) and then jumps to "geometry is a feasible stand-in for WSS at scale" with only Griffo for support. It omits the prospective WSS-outcome studies (PREDICTION, PROSPECT), the CCTA-based WSS-outcome studies (EMERALD, SMARTool), the finding that high WSS also carries risk, and the expert consensus. These matter because the thesis's argument is "geometry → low WSS → plaque", and the strength of the WSS → plaque link in humans is the premise.

### Cited Findings
- **MUST** Stone PH, et al. PREDICTION. *Circulation* 2012;126(2):172-181. PMID 22723305. 506 ACS patients, 374 reimaged at 6-10 months. Low ESS predicted lumen loss but **not** the primary endpoint (plaque area increase). **[in refs.bib; cut from this chapter on 2026-10-04]**. Why: it is the largest prospective human WSS → progression study and the closest design to the thesis. Its partly negative primary result has to be acknowledged rather than avoided. — per `literature.md` Axis 5
- **MUST** Stone PH, et al. PROSPECT ESS substudy. *JACC Cardiovasc Imaging* 2018;11:462-471. doi:10.1016/j.jcmg.2017.01.031, PMID 28917684. 145 lesions in 97 ACS patients; low ESS added prognostic value beyond plaque burden, MLA and TCFA. 3-year non-culprit MACE was 52.1% (high anatomic risk + low ESS) vs 0.0% (physiological/high ESS). **[not in refs.bib]** — [Europe PMC 28917684](https://europepmc.org/article/MED/28917684)
- **MUST** Lee JM, et al. EMERALD. *JACC Cardiovasc Imaging* 2019;12:1032-1043. doi:10.1016/j.jcmg.2018.01.023, PMID 29550316. 72 ACS patients with CCTA 1 month to 2 years before the event; 66 culprit vs 150 non-culprit lesions. CCTA-derived WSS, axial plaque stress and ΔFFRCT improved identification of future culprit lesions. **[not in refs.bib]**. Why: it is CCTA-based, so it supports the review's claim that CCTA can deliver flow-relevant information. — [Europe PMC 29550316](https://europepmc.org/article/MED/29550316); [EMERALD-related PMC8475759](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8475759/)
- **SHOULD** Kumar A, et al. *J Am Coll Cardiol* 2018;72:1926-1935. doi:10.1016/j.jacc.2018.07.075, PMID 30309470. FAME II medically treated arm (441 patients, 34 MIs): **high** proximal WSS (>4.71 Pa) predicted MI. Together with Bajraktari 2021 (meta of 615 patients, high WSS → regression of fibrous tissue) **[in refs.bib]**, this shows that WSS risk is not monotonic. A geometry proxy tuned only to low WSS captures half of the mechanism. — [Europe PMC 30309470](https://europepmc.org/article/MED/30309470); [ACC press release](https://www.acc.org/about-acc/press-releases/2019/03/17/09/24/two-william-w-parmley-young-author-achievement-awardees-selected)
- **SHOULD** Sakellarios A, et al. SMARTool. *Appl Sci* 2021;11(5):1976. 187 patients / 480 vessels with stable CAD, CCTA at baseline and after 6.2 ± 1.4 years. ESS predicted progression univariately but was **not independent** once LDL concentration entered the model; LDL, plaque burden and plaque area were independent. **[not in refs.bib]**. Why: it is the largest serial-CCTA WSS study (187 patients, which the review's "at most several hundred" covers), and it contradicts Sakellarios 2017 at 12x the sample. — [MDPI](https://www.mdpi.com/2076-3417/11/5/1976); [DOAJ](https://doaj.org/article/887844a1d32343c9bfc0ce0debfb3cc8)
- **Nice** Sakellarios A, et al. *Eur Heart J Cardiovasc Imaging* 2017;18:11-18. doi:10.1093/ehjci/jew035, PMID 26985077. 32 post-ACS patients, serial CCTA at 3 years; LDL transport and ESS predicted progression. A second Sakellarios 2017 paper, distinct from the cited EuroIntervention one (15 patients, 17 bifurcations). — [Europe PMC 26985077](https://europepmc.org/article/MED/26985077); cited paper confirmed at [EuroIntervention](https://eurointervention.pcronline.com/article/the-effect-of-coronary-bifurcation-and-haemodynamics-in-prediction-of-atherosclerotic-plaque-development-a-serial-computed-tomographic-coronary-angiographic-study) (doi:10.4244/EIJ-D-16-00929; 15 patients, 335 segments, 3-year follow-up, outcome = progression at existing bifurcation disease)
- **SHOULD** Gijsen F, et al. Expert recommendations on the assessment of WSS in human coronary arteries. *Eur Heart J* 2019;40:3421-3433. doi:10.1093/eurheartj/ehz551, PMID 31566246. Why: the standard methodological reference whenever WSS is invoked. **[not in refs.bib]** — [Europe PMC 31566246](https://europepmc.org/article/MED/31566246)
- **SHOULD** Eslami P, et al. *Ann Biomed Eng* 2021;49(4):1151-1168. doi:10.1007/s10439-020-02631-9. In 14 patients, CCTA-derived vs invasive WSS correlated at r=0.86 to 0.95, but categorical concordance was only 64% in the held-out patients. **[in refs.bib]**. Why: the review's line "geometry can be measured directly from routine CCTA" is stronger if it also states how well CCTA reproduces WSS. — [PMC8360211](https://pmc.ncbi.nlm.nih.gov/articles/PMC8360211)
- Griffo 2026 (cited, but only for simulation cost): 1078 arteries / 748 patients, GEM-GCN estimates WSS from geometry alone, and its WSS predicts MI as well as CFD-derived WSS does (AUC 0.63-0.68, within-patient culprit vs non-culprit). Why: this is the strongest published evidence that geometry alone carries the WSS signal, which is the review's central bridge. The review uses it only for "CFD is expensive". — per `knowledge/docs_thesis/papers/griffo2026wss.md`

### Inferences
- The review's Garcha → "geometry as a stand-in for WSS" paragraph would be much stronger if it cited Griffo for its actual result (geometry-only WSS keeps its prognostic value), and EMERALD for CCTA-derived WSS predicting ACS.
- The honest version of the WSS-to-plaque link is "consistent but modest, and partly negative on primary endpoints (PREDICTION, SMARTool)". Saying so pre-empts the obvious examiner question of why geometry would work if WSS itself predicts only modestly.

### Gaps
- I did not verify the full text of SMARTool (Appl Sci 2021). The numbers above are from the indexed abstract. The first author is reported as Sakellarios; confirm the author list before citing.

## Are the claimed gaps already addressed by recent papers?

### Takeaway
G2's core claim (no geometry study following a *general-population, plaque-free* cohort to *new* plaque) still holds as of October 2026 as far as I could find. But several statements around it are overstated or contradicted by papers already in refs.bib: plaque-free-at-baseline serial-CCTA cohorts exist (PARADIGM, the myocardial bridge study); CCTA geometry has been related to *future* events (ICONIC); a geometry-to-WSS study with 748 patients sits inside the review; and "risk scores combine systemic factors only" ignores CAC and CCTA-based risk tools that guidelines and large cohorts already use.

### Cited Findings

**G1: "related geometry either to WSS in computer models or to disease already present"**
- Contradicted by Han 2022 ICONIC (geometry at baseline CCTA vs later ACS culprit, n=116 patients / 548 lesions), Tommasino 2024 (LM angle vs later MACE, n=499) and Sun 2026 AngioGraphCAD (*Med Image Anal* 112:104079, doi:10.1016/j.media.2026.104079; lesion geometry GNN predicting future events from ICA) **[in refs.bib]**. Rephrase as "to disease already present or to events in patients with established disease". — [Houston Methodist record](https://scholars.houstonmethodist.org/en/publications/association-of-plaque-location-and-vessel-geometry-determined-by-/); `find_research.md` Stage 4

**G1: "at most several hundred individuals" (geometry and flow in patients)**
- Griffo 2026, which the review itself cites, used 748 patients / 1078 arteries. Kumar 2018 used 441 FAME II patients (WSS, not geometry), and SMARTool 187. Either restrict the claim to CCTA with whole-tree geometry (where Kashyap n=127 and Zhang n=39 are the ceiling) or change "several hundred" to "under a thousand". — [Europe PMC 30309470](https://europepmc.org/article/MED/30309470); `griffo2026wss.md`

**G1: "single region"**
- This still holds for the WSS literature: Kashyap (LM), Tello Ayala (RCA), Schultz 2023 (excludes LM and side branches). Zhang 2024 is a partial exception (whole *left* tree, n=39) and should be cited as such. Nannini 2024 and Medrano-Gracia 2016 compute whole-tree descriptors but without outcomes.

**G2: "the few longitudinal studies available have followed patients who already had coronary disease"**
- Partly contradicted. Won KB, et al. (PARADIGM). *Cardiovasc Diabetol* 2022;21:239. doi:10.1186/s12933-022-01656-9, PMID 36371222. **402 patients with no plaque at baseline**, serial CCTA, median 3.6 years: 35.6% developed new plaque. Baseline traditional risk factors (age, sex, hypertension, diabetes, lipids, obesity, smoking) did **not** predict rapid progression; follow-up HbA1c did. No geometry was measured. **[not in refs.bib]**. Why: it is the closest published design to the CGPS longitudinal subset (referred, not general population), it gives the base rate of new plaque, and its null for systemic risk factors strengthens the review's motivation. — [Europe PMC 36371222](https://europepmc.org/article/MED/36371222); [PMC9655903](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9655903/)
- Chen YC, et al. *EHJ-CVI* 2024 (above): 295 patients plaque-free proximal to an LAD myocardial bridge, followed with repeat CCTA to new plaque. A centreline/cross-section vascular radiomics model reached AUC 0.75 externally and beat the anatomical model. Why: this is the nearest existing instance of "CCTA shape features at a plaque-free site predict later plaque formation", though local (one site), referred patients, and radiomics rather than interpretable geometry. **This is the paper most likely to be raised against the G2 novelty claim.** — [Europe PMC 38781436](https://europepmc.org/article/MED/38781436)

**G2: "No study has therefore combined consistent measurement of the coronary tree with follow-up of a general population from a plaque-free state to the formation of new plaque"**
- I found nothing that contradicts this. General-population CCTA cohorts are cross-sectional or outcome-based on plaque/stenosis, not geometry: SCAPIS (Bergström G, et al. *Circulation* 2021;144:916-929, doi:10.1161/circulationaha.121.055340, PMID 34543072; 25,000+ individuals aged 50-64, atherosclerosis in 42.1%, 5.5% even with CAC=0) **[not in refs.bib]** and CGPS (Fuchs 2023, n=9533) **[in refs.bib, cited in intro]**. The review should cite SCAPIS alongside CGPS as the other general-population CCTA resource and say neither has published geometry. — [Europe PMC 34543072](https://europepmc.org/article/MED/34543072); [TCTMD](https://www.tctmd.com/news/scapis-cta-finds-silent-cad-42-middle-aged-adults)

**G2: "current risk scores combine systemic risk factors only"**
- Overstated. The 2021 ESC prevention guideline (Visseren FLJ, et al. *Eur J Prev Cardiol* 2022;29:5-115, doi:10.1093/eurjpc/zwab154, PMID 34558602) uses SCORE2 but lists CAC scoring as a risk modifier. **[not in refs.bib]** — [Europe PMC 34558602](https://europepmc.org/article/MED/34558602)
- CAC already adds individual-level imaging information beyond risk factors: Detrano R, et al. (MESA). *N Engl J Med* 2008;358:1336-1345, doi:10.1056/nejmoa072100; Polonsky TS, et al. *JAMA* 2010;303:1610-1616, doi:10.1001/jama.2010.461 (CAC improves risk classification). **[not in refs.bib]** — [Europe PMC 18367736](https://europepmc.org/article/MED/18367736); [Europe PMC 20424251](https://europepmc.org/article/MED/20424251)
- CCTA-derived non-plaque biomarkers already add to risk scores: Oikonomou EK, et al. CRISP-CT. *Lancet* 2018;392:929-939, doi:10.1016/s0140-6736(18)31114-0 (pericoronary fat attenuation index predicts cardiac mortality); Chan K, et al. ORFAN. *Lancet* 2024;403:2606-2618, doi:10.1016/s0140-6736(24)00596-8 (40,091 CCTA patients, median 2.7 years; FAI score adds to QRISK3 + CAD-RADS 2.0 and predicts events even with no CT-detected CAD). **[not in refs.bib]**. Why: ORFAN is the direct precedent for "a CCTA-derived, non-plaque marker that refines individual risk", which is exactly the role the thesis proposes for geometry. An examiner in cardiac CT will expect it. — [Europe PMC 30170852](https://europepmc.org/article/MED/30170852); [Europe PMC 38823406](https://europepmc.org/article/MED/38823406); [TCTMD](https://www.tctmd.com/news/ai-assisted-look-coronary-inflammation-ct-refines-cv-risk-assessment)
- Ma 2025 (*J Med Internet Res* 27:e68872; 10 studies, pooled testing AUROC ≈0.80 for ML MACE prediction from CCTA, almost all plaque radiomics) **[in refs.bib]** gives the benchmark any geometry model is compared against. — `find_research.md` Stage 2

**Automated / deep-learning geometry extraction (the review cites only Bransby)**
- Nannini G, et al. *APL Bioeng* 2024;8:016103. doi:10.1063/5.0181281, PMID 38269204. Fully automated two-stage U-Net segmentation (281 annotated CCTAs) with automatic centreline tortuosity scoring and CAC. Tortuosity rose from proximal to distal while calcium fell, giving a negative tortuosity-calcified plaque relation. **[in refs.bib]**. Why: the direct precedent for an automated CCTA geometry pipeline linked to plaque. — [PMC10807932](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10807932/)
- Medrano-Gracia P, et al. A computational atlas of normal coronary artery anatomy. *EuroIntervention* 2016;12(7):845-854. doi:10.4244/EIJV12I7A139. 300 CCTA adults, automatic 3D angles, diameters and lengths. **[in refs.bib]**. Why: the normative reference population for automated tree geometry. — [EuroIntervention](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)
- Zeng 2023 ImageCAS and Dong 2023 CAS-Net **[both in refs.bib]**: the dataset and model behind Bransby's benchmark. One clause would show where the pipeline comes from.

### Inferences
- A defensible G2, given the evidence: "No study has measured whole-tree geometry automatically in a *general-population* CCTA cohort and related it to *new* plaque at a repeat scan. The closest designs are plaque-free referred cohorts without geometry (PARADIGM), a single-site radiomics study (myocardial bridge), and baseline-geometry-to-event studies in referred patients (ICONIC, CLAP)."
- The risk-score sentence should change from "systemic risk factors only" to "systemic risk factors, refined in imaged patients by CAC, plaque and inflammation markers (CAC, ORFAN), but not by geometry".

### Gaps
- I could not determine whether SCAPIS or CGPS have published any geometry (angle, tortuosity) analyses. Searches returned none, but conference abstracts were not covered.
- I did not search Chinese multicentre CCTA AI cohorts (e.g., a 16,300-patient AI plaque study surfaced in one search) for geometry outputs. They appear to be plaque-focused.

## Are there contradicting findings (e.g., tortuosity protective vs harmful) that the review should reconcile?

### Takeaway
Yes, and the contradiction is inside the review's own citations. Li 2011 reports tortuosity *inversely* associated with CAD (OR 0.755), while Tello Ayala 2026 reports a *positive* association (adjusted OR 1.05 per SD for CAD, 1.09 for severe CAD). The text presents both without noting that they point in opposite directions. Add Groves 2009 (inverse), Zebić Mihić 2023/2024 (positive for non-obstructive disease and ischemia), Li M 2022 (null on multivariable) and ICONIC (tortuous segments over-represented among future culprits), and the picture is mixed in ways that depend on endpoint and measure. The bifurcation-angle literature is directionally consistent; dominance is conditional.

### Cited Findings
- Inverse: Li Y, et al. *PLoS ONE* 2011;6(8):e24232 (n=1010 angiography; OR 0.755, 95% CI 0.574-0.994; no difference in MACE at 2-4 years) **[cited]**; Groves 2009 *W V Med J* 105(4):14-17, PMID 19585899 (n=1221; severe tortuosity in 12.45%, lower significant CAD, p=0.003) **[in refs.bib]**. — [PMC3164184](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3164184/); refs.bib notes
- Positive: Tello Ayala 2026 *JACC Adv* 5:102829 (22,334 patients; adjusted OR 1.05 [1.03-1.08] per SD for CAD) **[cited, but the positive direction is not stated in the review]**; Han 2022 ICONIC (tortuous segments 4.3% of culprit precursors vs 1.4% of non-culprit lesions) **[in refs.bib]**. — refs.bib note (full text read); [Houston Methodist record](https://scholars.houstonmethodist.org/en/publications/association-of-plaque-location-and-vessel-geometry-determined-by-/)
- Endpoint-dependent: Zebić Mihić 2023 (tortuosity with non-obstructive CAD, OR 7.96) and 2023b/2024 (n=160; a continuous index localizes ischemia while the bend count finds almost nothing) **[both in refs.bib]**. — `find_research.md` §1.2
- Null after adjustment: Li M, et al. Correlation analysis of coronary artery tortuosity and calcification score. *BMC Surg* 2022;22:66. doi:10.1186/s12893-022-01470-w, PMID 35197040. n=1280; tortuosity in 35%, more common in women and with hypertension, age and BMI. No association with CAC or stenosis on multivariable analysis (moderate CAC OR 1.49 only univariably). **[not in refs.bib]** — [Europe PMC 35197040](https://europepmc.org/article/MED/35197040)
- Negative with calcified plaque, by segment: Nannini 2024 (tortuosity distal, calcium proximal). — [PMC10807932](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10807932/)
- Measure dependence: Kashyap 2022 **[cited]**: average absolute curvature tracks low WSS while the tortuosity index does not (p=0.86).
- Confounding: tortuosity rises with age, female sex and hypertension (Li 2011 OR 2.603 for women; Li M 2022; Kahe 2020 review **[in refs.bib]**). Bifurcation angle rises with age (carotid analogue: Kwon 2022, n=177, 10-year MRA **[in refs.bib]**) and varies with sex and BMI (Temov 2016). Why: this supports the thesis's age+sex baseline and should be stated as the reason for it.
- Dominance: CONFIRM null (n=6382) vs Veltman HR 3.20 vs Khan meta OR 1.27 in ACS **[all in refs.bib]**. — `find_research.md` §1.3
- Ramus intermedius: positive at n=1380 (Bekirçavuşoğlu 2026) vs not independent after propensity matching at n=200 (Zhang 2023) **[both in refs.bib]**.
- WSS direction: low WSS → plaque growth (Chatzizisis, PREDICTION secondary endpoint) vs high WSS → MI and fibrous regression (Kumar 2018; Bajraktari 2021). — [Europe PMC 30309470](https://europepmc.org/article/MED/30309470)

### Inferences
- One reconciling sentence is supported by the cited evidence: studies using discrete 2D bend counts in referred angiography populations (Li 2011, Groves) find an inverse link with *obstructive* CAD, while continuous or 3D measures (Tello Ayala, Zebić Mihić index, Kashyap curvature) find positive or territory-specific links. Women and hypertension are over-represented in tortuous vessels, which confounds both. This also justifies the thesis using continuous curvature with an age+sex baseline.
- Glagov remodeling (cited) also cuts against the inverse finding: advanced plaque can straighten or stiffen lumens, so a cross-sectional inverse association is not evidence of protection.

### Gaps
- No meta-analysis of coronary tortuosity vs CAD was found. Kahe 2020 is a narrative review.
- Whether ICONIC's tortuosity difference survives adjustment could not be confirmed from the abstract (the counts are small: 5 vs 6 lesions).

---

### Note on shen2026geometry (deliberately uncited; not counted as a gap)
Shen et al. 2026 (*Arch Comput Methods Eng*, doi:10.1007/s11831-026-10530-w; authors include Wentzel, Morbiducci, Chatzizisis, Serruys, Beier) names essentially the same two gaps as the review's G1: anatomy-haemodynamics studies "with a large population are limited", and most cover only the main bifurcation, so "investigating the whole tree is essential". It also notes that inconsistent tortuosity/curvature definitions likely cause contradictory findings, which is the review's measurement paragraph. An examiner from the Beier/Wentzel orbit will recognise the framing. Rebuilding it from primary studies is legitimate, but G1 should not be presented as the thesis's own discovery, and if challenged, the author should be ready to say Shen reached it independently. Shen has no search protocol, so it cannot license "no study has done X" claims anyway. (Source: `knowledge/docs_thesis/papers/shen2026geometry.md`, read in full.)

### Priority summary
- **Must-cite (mostly already in refs.bib):** Han 2022 ICONIC; Stone 2012 PREDICTION; Juan 2017 or Cui 2017 plus Tommasino 2024 (angles, with outcomes); Bekirçavuşoğlu 2026; Givehchi 2018; Zhang 2024 curvature; Won 2022 PARADIGM plaque-free cohort; Chen 2024 myocardial bridge new plaque; Lee 2019 EMERALD; Stone 2018 PROSPECT; Chan 2024 ORFAN (plus CAC: Detrano 2008 or the ESC 2021 guideline); SCAPIS 2021; Groves 2009 or Li M 2022 (to settle the tortuosity direction); Nannini 2024.
- **Should-cite:** Gebhard 2015 CONFIRM (dominance); Kumar 2018 (high WSS); SMARTool 2021; Gijsen 2019 consensus; Eslami 2021; Medrano-Gracia 2016; Iwami 1998; one Murray's-law source; Zebić Mihić 2023/2024; Oikonomou 2018 CRISP-CT.
- **Nice-to-have:** Moradi 2026; Mansouri 2024; Temov 2016; Wahle 2006; van Zandwijk 2020; Kwon 2022; Sun 2026 AngioGraphCAD; Ma 2025; Sakellarios 2017 EHJCI (n=32); Zhang 2023 RI.
- **Internal fixes:** state that Li 2011 (inverse) and Tello Ayala 2026 (positive) disagree; use Griffo for its geometry-only WSS result, not only for cost; correct "at most several hundred"; soften "systemic risk factors only".
