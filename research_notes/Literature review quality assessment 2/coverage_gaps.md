# Coverage gaps in the rewritten literature review (state 2026-10-04) and test of its gap sentence

Scope: `thesis/literature_review/literature_review.tex` (rewritten 2026-10-04) read against
`thesis/introduction/01_introduction.tex`. The intro's aims are an automated whole-tree CCTA pipeline
(segmentation, artery labelling, branching angles, branch radius ratios, curvature), logistic regression
versus a curvature-profile transformer, per-artery models judged against an age+sex baseline, and the CGPS
general-population cohort with a repeat CCTA about 10 years later, with new plaque as the outcome.
Compared against `research_notes/Literature review quality assessment/coverage_gaps.md` (round 1).
Method: Europe PMC REST and Crossref API queries, web search, and the local knowledge bank
(`knowledge/docs_thesis/literature.md`, `find_research.md`, `papers/`, `thesis/refs.bib`).
**[in refs.bib]** = already in the bibliography but not cited in the chapter. shen2026geometry is deliberately
uncited and is not counted as a gap. Claims are abstract-level unless marked "full text".

## Q1. Round-1 must-cites: which are now included, which are still missing, and is each omission still damaging?

### Takeaway
The rewrite closed most of round 1. Of the 16 must-cites, 12 are now cited: Han 2022, Stone 2012, Juan/Cui,
Tommasino, Bekirçavuşoğlu, Givehchi, Zhang 2024, Won 2022, Chan 2024, Bergström 2021, Groves 2009 and
Nannini 2024. The four still missing are the paywalled ones (Chen 2024, EMERALD, PROSPECT-ESS, ESC 2021/CAC).
Chen 2024 is the only omission that still damages the gap argument. The other three weaken the WSS strand and
the risk-score sentence but do not threaten novelty. The three round-1 internal fixes were all made: the
tortuosity direction conflict is now stated, Griffo is used for its result, and "several hundred" and
"systemic factors only" were removed.

### Cited Findings
**Now included (round-1 must-cites)**
- Han 2022 ICONIC: now a full paragraph, correctly qualified (events median 29 days after CCTA, culprits in
  normal segments excluded). Full text in `knowledge/docs_thesis/papers/han2022plaque.md`. — [PMC8792800](https://pmc.ncbi.nlm.nih.gov/articles/PMC8792800)
- Stone 2012 PREDICTION: cited, with the negative primary endpoint stated (WSS predicted lumen narrowing, not plaque growth). — chapter text
- Juan 2017, Cui 2017, Tommasino 2024, Bekirçavuşoğlu 2026, Givehchi 2018: all cited. Tommasino is cited with the caveat that its effect sizes cannot be reproduced (full text: `papers/tommasino2024clap.md`). — chapter text
- Zhang 2024 (whole left tree, n=39), Won 2022 PARADIGM (402 plaque-free referred patients), Chan 2024 ORFAN, Bergström 2021 SCAPIS: all cited. — chapter text
- Tortuosity direction: Groves 2009, Li 2011, Zebić Mihić 2024 and Tello Ayala 2026 are now reconciled by "discrete counts inverse, continuous measures positive". — chapter text
- Nannini 2024 and Bransby 2026: cited for automated extraction. — chapter text

**Still missing: the four paywalled must-cites**
- **Chen YC, Zheng J, Zhou F, ... Teng Z, Zhang LJ. Coronary CTA-based vascular radiomics predicts atherosclerosis development proximal to LAD myocardial bridging. *Eur Heart J Cardiovasc Imaging* 2024;25(10):1462-1471. doi:10.1093/ehjci/jeae135, PMID 38781436.** Europe PMC lists it as "subscription required", with no OA copy. Still damaging: it is the nearest published instance of CCTA shape-derived features at a plaque-free site predicting new plaque on a repeat CCTA (details in Q2). — [Europe PMC 38781436](https://europepmc.org/article/MED/38781436)
- **Lee JM, et al. EMERALD. *JACC Cardiovasc Imaging* 2019;12:1032-1043. doi:10.1016/j.jcmg.2018.01.023, PMID 29550316.** CCTA-derived WSS and axial plaque stress improved identification of future ACS culprits (72 patients). Moderately damaging: the WSS strand has no CCTA-based WSS-outcome study, only IVUS (Stone 2012) and invasive angiography (Griffo). It is not a novelty threat. — [Europe PMC 29550316](https://europepmc.org/article/MED/29550316) (round-1 summary; not re-read)
- **Stone PH, et al. PROSPECT ESS substudy. *JACC Cardiovasc Imaging* 2018;11:462-471. doi:10.1016/j.jcmg.2017.01.031, PMID 28917684.** Low ESS added prognostic value beyond plaque burden, MLA and TCFA. Mildly damaging: the chapter currently gives only the partly negative PREDICTION result, so the WSS-outcome link looks weaker than the literature supports. — [Europe PMC 28917684](https://europepmc.org/article/MED/28917684)
- **Visseren FLJ, et al. 2021 ESC Guidelines on CVD prevention. *Eur Heart J* 2021;42:3227-3337 (also *Eur J Prev Cardiol* 2022;29:5-115, doi:10.1093/eurjpc/zwab154, PMID 34558602).** CAC is listed as a risk modifier. Now low damage: the rewrite no longer says "systemic factors only" and uses ORFAN to show imaging refines risk. One CAC citation would still be expected by a cardiac-CT examiner, since CAC is the guideline-endorsed imaging refiner and ORFAN is not. A CAC alternative that is not paywalled: Detrano 2008 MESA, *NEJM* 358:1336-1345, doi:10.1056/nejmoa072100. — [Europe PMC 34558602](https://europepmc.org/article/MED/34558602)

**Round-1 should-cites still absent (optional)**
- Kumar 2018 (high WSS predicts MI, doi:10.1016/j.jacc.2018.07.075); SMARTool 2021 (ESS not independent of LDL, 187 patients); Gijsen 2019 WSS consensus (doi:10.1093/eurheartj/ehz551); Eslami 2021 **[in refs.bib]**; Medrano-Gracia 2016 atlas **[in refs.bib]**; Iwami 1998; Li M 2022 (tortuosity null after adjustment); Oikonomou 2018 CRISP-CT; van Zandwijk 2019/2020 curvature over the cardiac cycle **[in refs.bib as vanzandwijk2019curvature]**. — round-1 notes, Q2 and Q4

### Inferences
- What remains missing is concentrated in the WSS-outcome evidence (EMERALD, PROSPECT-ESS, Kumar). One
  sentence after Stone 2012 would close it: "CCTA- and IVUS-derived WSS has since added to plaque
  features in identifying future culprits (EMERALD, PROSPECT-ESS)".
- Medrano-Gracia 2016 (300 CCTA adults, automatic 3D angles, diameters and lengths) is **[in refs.bib]** and
  fits the "automated extraction" paragraph at no cost. It is also the only normative whole-tree geometry
  cohort.
- van Zandwijk is **[in refs.bib]** and would extend Cui's cardiac-phase point from angles to curvature,
  which is the transformer's input. This is cheap and relevant.

### Gaps
- EMERALD, PROSPECT-ESS and ESC 2021 full texts were not retrieved in this pass. The publisher pages block
  automated access, so their numbers rest on round-1 abstract notes.

## Q2. Chen 2024 (EHJ-CVI): what can be established, and how does it differ from the thesis?

### Takeaway
The Europe PMC abstract and a 2025 scoping review establish the design. It is a retrospective, multicentre
(five Chinese tertiary hospitals), referred-patient cohort of 295 people with an LAD myocardial bridge and no
plaque proximal to it at index CCTA, followed to a repeat CCTA. The endpoint was new proximal plaque. A
"proximal MB cross-section" vascular radiomics model reached an external AUC of 0.75 and raised the
clinical+anatomical model from 0.56 to 0.75. It differs from the thesis in population (referred, MB carriers),
spatial scope (one segment), features (radiomics, not interpretable geometry) and the absence of a
general-population or whole-tree analysis. So it does not break the gap sentence. It is, however, the
strongest precedent that CCTA vessel features at a plaque-free site predict new plaque, and an examiner may
raise it.

### Cited Findings
- Design: patients with repeated CCTA showing LAD MB **without proximal plaque on index CCTA**. The development set came from Jinling Hospital (192 patients, split 8:2 into train/internal test) and the external validation set from four other tertiary hospitals (103 patients). Endpoint: proximal plaque development at follow-up CCTA. — [Europe PMC abstract, PMID 38781436](https://europepmc.org/article/MED/38781436)
- Four vascular radiomics models were built: MB centreline, proximal-MB centreline, MB cross-section and proximal-MB cross-section (pMB CS). pMB CS AUC was 0.78/0.75/0.75 (train/internal/external), above the clinical and anatomical model (all P<0.05). Adding pMB CS raised the external AUC from 0.56 to 0.75 (P=0.002), with NRI 0.76 (0.37-1.14) and IDI 0.17 (0.07-0.26). — [Europe PMC 38781436](https://europepmc.org/article/MED/38781436)
- Stated rationale: "cardiac cycle morphological changes can accelerate plaque growth proximal to MB". This is a local haemodynamic mechanism, the same family as the thesis's low-WSS argument. — [Europe PMC 38781436](https://europepmc.org/article/MED/38781436)
- Secondary description: Abu Suleiman A, Russo F, Della Valle L, et al. *J Cardiovasc Dev Dis* 2025;12(9):350, doi:10.3390/jcdd12090350 (scoping review of AI in MB) describes it as a retrospective cohort/validation study (n=295, mean age 55±10, 66% male), with plaque-free status defined at baseline CCTA. The review does not report follow-up interval or segmentation method. It lists Zhou 2019 (*JACC CVI*; CT-FFR and ΔCT-FFR as the strongest ML predictors of plaque proximal to MB) as the earlier work. — [PMC12470274](https://pmc.ncbi.nlm.nih.gov/articles/PMC12470274/)
- A related follow-up study (open access) is Feng D, Shang R, Hu L, et al. *Quant Imaging Med Surg* 2025, doi:10.21037/qims-2024-2752, PMID 41209226, PMC12591738. It included 135 LAD-MB patients with ≥2 CCTAs (2014-2023), 90 of whom formed plaque proximal to the MB. After clinical adjustment, MB length (P=0.043) and perivascular FAI (P=0.001) were independent predictors (combined AUC 0.755). ΔCT-FFR was correlated (P=0.039). — [Europe PMC 41209226](https://europepmc.org/article/MED/41209226)

**Difference from the thesis**

| | Chen 2024 | Thesis |
|---|---|---|
| Population | Referred patients with an LAD myocardial bridge, Chinese hospitals | CGPS general population |
| Spatial scope | One segment proximal to the MB | Whole tree, per artery |
| Features | Vascular radiomics (centreline and cross-section) | Interpretable geometry (angles, radius ratios, curvature profile) |
| Extraction | Not established (abstract silent) | Fully automated pipeline |
| Outcome | New plaque at one site | New plaque per artery and per individual |
| Baseline comparator | Clinical + anatomical model (AUC 0.56) | Age+sex |

### Inferences
- Chen 2024 counts against a looser gap claim ("no study has related baseline CCTA vessel features to new
  plaque") but not against the chapter's sentence, which is anchored on "whole coronary tree", "automatically"
  and "general population". It should be cited next to Won 2022 as the plaque-free serial-CCTA design that
  *did* use vessel features, so the reader sees the gap was checked rather than assumed.
- "Vascular radiomics" from the Teng group (the senior author is a mechanomics/biomechanics researcher)
  probably includes centreline shape descriptors, but this cannot be confirmed without the full text. Do not
  call it "geometry" in the thesis until it has been read.

### Gaps
- Not established: follow-up interval, whether segmentation and feature extraction were automated, and
  whether the centreline features include curvature or tortuosity. The full text is needed via DTU Findit.
  No ResearchGate or author-manuscript copy surfaced in searches.

## Q3. Is there any 2024-2026 study that breaks the gap sentence?

### Takeaway
No. As of 2026-10-04 I found no study that measured whole-tree coronary geometry automatically in a
general-population cohort and related it to new plaque on a later scan. Three findings tighten the
surroundings, though. (a) CArTI (AHA 2025 abstract) extracted 227 automated tortuosity, curvature and torsion
features from CCTA segmentations and predicted 5-year MACE. This directly contradicts the chapter's sentence
"geometry has not been tested in this role". (b) Lee 2024 (JCCT, PARADIGM) predicted new plaque in 9583
plaque-free segments from baseline CCTA radiomics. (c) SCAPIS has started a repeat-CT re-examination of about
15,000 general-population participants after a median of 8.1 years. This is a competing cohort that could
close the gap soon; no geometry analysis has been published from it.

### Cited Findings
**Closest threats (not breaking, but must be cited)**
- **Lebowitz, Modanwal, Dhamdhere, Mutha, De Cecco, van Assen, Madabhushi. Abstract 4365988: AI-informed Coronary Artery Tortuosity Index (CArTI) from Cardiac CT Angiography Predicts 5-Year Cardiovascular Risk. *Circulation* 2025;152(Suppl 3). doi:10.1161/circ.152.suppl_3.4365988.** Coronary arteries were segmented with a 3D U-Net in CCTAs of 992 patients (median follow-up 4.3 years, MACE from ICD/CPT codes). From each segmentation, 227 structural features (tortuosity, curvature, torsion) were extracted and the top 8 went into a Cox model. Holdout C-index was 0.648, and the high-risk group had HR 2.69 (1.07-6.78). Curvature and tortuosity features were positively associated with MACE. The abstract does not state the population, but code-derived MACE suggests a clinical, not general-population, cohort. No new-plaque outcome, and no full paper found. — [Crossref record](https://api.crossref.org/works/10.1161/circ.152.suppl_3.4365988)
- **Lee SE, Hong Y, Hong J, et al. (Chang HJ senior; PARADIGM investigators). Prediction of the development of new coronary atherosclerotic plaques with radiomics. *J Cardiovasc Comput Tomogr* 2024. doi:10.1016/j.jcct.2024.02.003, PMID 38378314.** The study used 9583 segments without plaque at baseline from 1162 patients in a multinational serial-CCTA registry (interval ≥2 years). 9.8% of segments developed new plaque (≥1 mm³). Clinical risk factors alone gave C 0.696 and radiomics alone 0.691 in test. Combined, they gave 0.767. Referred patients, radiomics rather than geometry, segment-level. Not in refs.bib. — [Europe PMC 38378314](https://europepmc.org/article/MED/38378314)
- **Good E, Bergström G, Blomberg A, et al. The SCAPIS re-examination: rationale, design, methods, and management of incidental findings. *J Intern Med* 2026. doi:10.1111/joim.70068, PMID 41558989.** About 15,000 participants (50% of SCAPIS) are being re-examined at six university hospitals, aged 55-75, a median of 8.1 years after baseline. Baseline imaging, including "extensive computer tomography imaging", is replicated. One stated aim is to "quantify and explain the development of atherosclerosis". This is the only other general-population serial-CT cohort found. Interim data (first 5000) are on risk factors only. — [Europe PMC 41558989](https://europepmc.org/article/MED/41558989)

**Serial-CCTA new-plaque studies without geometry (strengthen "nobody used geometry")**
- Zhao W, Li N, Jiang B, et al. *Clin Radiol* 2025, doi:10.1016/j.crad.2025.107018, PMID 40768936. 160+60 risk-factor patients with normal initial CCTA and ≥2 CCTAs within 5 years; 60/160 formed new plaque. FAI predicted new plaque (AUC 0.723) and added to risk factors (0.817 vs 0.749). — [Europe PMC 40768936](https://europepmc.org/article/MED/40768936)
- The Amsterdam 10-year serial-CCTA cohort is the closest interval match to CGPS: 299 patients with suspected CAD, median interscan 10.2 years, AI-QCT plaque analysis. Its papers relate plaque progression to Lp(a) (Nurmohamed NS, et al. *JAMA Cardiol* 2024, doi:10.1001/jamacardio.2024.1874, PMID 39018040), polygenic risk (Nurmohamed NS, et al. *JACC CVI* 2024, doi:10.1016/j.jcmg.2024.06.015, PMID 39152960), diabetes (Gaillard EL, et al. *Cardiovasc Diabetol* 2025, doi:10.1186/s12933-025-02977-1, PMID 41194148) and proteomics (Kraaijenhof JM, et al. *EHJ-CVI* 2025, doi:10.1093/ehjci/jeae313). No geometry was measured, and the patients were referred. — [Europe PMC 39018040](https://europepmc.org/article/MED/39018040); [Europe PMC 39152960](https://europepmc.org/article/MED/39152960)
- A PARADIGM sub-analysis (EHJ-CVI 2026 supplement abstract jeaf367.317) of 2252 serial-CCTA patients found new lesions in over a third of patients without baseline plaque. No geometry. — [OUP abstract](https://academic.oup.com/ehjcimaging/article/27/Supplement_1/jeaf367.317/8446296)

**General-population geometry: none found**
- Europe PMC queries combining coronary tortuosity, curvature, bifurcation angle or geometry with SCAPIS, UK Biobank, MESA, CGPS, Rotterdam, Heinz Nixdorf, BioImage or "general population" (2020-2026) returned no coronary-geometry study. Hits were retinal (RetiMap, UK Biobank) and carotid. SCAPIS outputs found are on plaque, risk factors, immune phenotypes and the aorta. UK Biobank, Heinz Nixdorf Recall and MESA do not have contrast CCTA in their core protocols (MESA and Heinz Nixdorf Recall use non-contrast CAC CT), so they cannot supply lumen geometry. — Europe PMC searches run 2026-10-04 (no single URL); see the SCAPIS hit list via [Europe PMC](https://europepmc.org/search?query=SCAPIS%20coronary%20geometry)
- Methods-only tortuosity work on clinical CCTA cohorts: an HMM-based unsupervised tortuosity method (Springer LNCS 2025 chapter, and ESC 2025 abstract ehaf784.136, 319 clinical patients). Neither has an outcome. — [Springer](https://link.springer.com/chapter/10.1007/978-3-031-95841-0_27); [EHJ supplement](https://academic.oup.com/eurheartj/article/46/Supplement_1/ehaf784.136/8312275)

### Inferences
- **The gap sentence holds as written.** Every near-miss fails at least two of its four qualifiers:
  - CArTI: automated, tree-wide but not general population, MACE not new plaque.
  - Lee 2024 and Won 2022: new plaque, but referred patients and no geometry.
  - Chen 2024 and Feng 2025: new plaque, but one segment, referred patients and radiomics.
  - SCAPIS: general population and serial, but no geometry published.
- **One adjacent sentence no longer holds.** "Imaging can therefore refine an individual estimate beyond
  systemic factors, but geometry has not been tested in this role" is contradicted by CArTI. Tommasino 2024
  (LM angle to MACE, already cited) also contradicts it weakly. Suggested repair: "geometry has been tested
  in this role only in referred patients and against clinical events (Tommasino; CArTI)".
- **The closing summary sentence also needs one more citation.** "Plaque-free cohorts with repeat CCTA have
  come from clinical registries without geometry \cite{won2022paradigm}" should add Lee 2024, which used the
  same registry at segment level with imaging features, and Chen 2024. Otherwise an examiner can name a
  plaque-free serial study with imaging predictors that the chapter appears not to know.
- **SCAPIS re-examination should be named.** Citing it as "a second general-population serial-CT cohort
  now under way" makes the thesis look aware rather than lucky, and supports the transferability argument.
- A safer wording, if desired: "No study has measured the geometry of the whole coronary tree automatically
  in a general population and related it to new plaque on a later scan; the closest designs used radiomics
  at a single site in referred patients \cite{chen2024}, segment radiomics in a clinical registry
  \cite{lee2024}, or automated tortuosity against clinical events \cite{carti2025}."

### Gaps
- CArTI: the cohort source (likely Emory, given De Cecco and van Assen) and whether participants were
  plaque-free are not in the abstract, and no full paper was found as of 2026-10-04.
- MICCAI/ISBI 2024-2025 proceedings were not searched exhaustively. Searches surfaced only methods papers
  (labelling, segmentation, tortuosity scoring), none with a population or new-plaque outcome.
- The SCAPIS re-examination paper says "extensive CT imaging" but the abstract does not confirm that
  contrast CCTA was repeated. Check the full text before writing "repeat CCTA".
- Lee 2024: whether the radiomic feature set included shape features (for example, PyRadiomics shape class
  on the segment mask) is not stated in the abstract.

## Q4. Literature motivating aims the review does not cover (labelling, radius ratio/Murray, dominance): expected in the review or acceptable elsewhere?

### Takeaway
- **Labelling** is a named pipeline step in the intro but absent from the review. One sentence citing one or
  two automated CCTA labelling methods belongs in the "Quantifying Coronary Geometry" strand. The detailed
  survey can go to the methods chapter.
- **Radius ratio/Murray** is the clearest uncovered aim. Only Garcha (synthetic) touches it. One sentence
  stating that the evidence is scaling-law physiology plus simulation, with no clinical cohort, is expected,
  because the absence is itself part of the gap.
- **Dominance (CONFIRM null vs Khan meta)** is acceptable in clinical background or methods, because the thesis
  stratifies by artery rather than testing dominance as a predictor. A cross-reference is enough.

### Cited Findings
**Automated coronary artery labelling (CCTA and ICA)**
- Wu D, Wang X, Bai J, et al. Automated anatomical labeling of coronary arteries via bidirectional tree LSTMs (TreeLab-Net). *Int J Comput Assist Radiol Surg* 2019;14:271-280. doi:10.1007/s11548-018-1884-6. The first deep tree-structured CCTA labeller. Not in refs.bib. — [Crossref](https://doi.org/10.1007/s11548-018-1884-6)
- Hampe N, van Velzen SGM, Wolterink JM, et al. Graph neural networks for automatic extraction and labeling of the coronary artery tree in CT angiography. *J Med Imaging* 2024;11(3):034001. doi:10.1117/1.jmi.11.3.034001, PMID 38756439. **[in refs.bib as hampe2024gnn]**. Why: joint extraction and labelling on CCTA, so it is the best single citation for the pipeline step. — [Europe PMC 38756439](https://europepmc.org/article/MED/38756439)
- Zhang Y, Luo G, Wang W, et al. TTN: Topological Transformer Network for automated coronary artery branch labeling in cardiac CT angiography. *IEEE J Transl Eng Health Med* 2024. doi:10.1109/jtehm.2023.3329031, PMID 38074924. — [Europe PMC 38074924](https://europepmc.org/article/MED/38074924)
- Brandt V, Fischer A, Schoepf UJ, et al. Deep learning-based automated labeling of coronary segments for structured reporting of CCTA in accordance with SCCT guidelines. *J Thorac Imaging* 2024. doi:10.1097/rti.0000000000000753, PMID 37889562. Clinical (SCCT-segment) labelling. — [Europe PMC 37889562](https://europepmc.org/article/MED/37889562)
- Zhao C, Xu Z, Hung GU, Zhou W. EAGMN. *Comput Biol Med* 2023;166:107469. doi:10.1016/j.compbiomed.2023.107469 **[in refs.bib]**; Zhao C, Esposito M, Xu Z, Zhou W. HAGMN-UQ. *Med Image Anal* 2025. doi:10.1016/j.media.2024.103374, PMID 39413456. Both are on **invasive angiograms**, not CCTA, so they are less apt than Hampe/TTN for a CCTA pipeline. — [Europe PMC 39413456](https://europepmc.org/article/MED/39413456)
- Ren P, et al. A deep learning-based automated algorithm for labeling coronary arteries in CTA images. *BMC Med Inform Decis Mak* 2023. doi:10.1186/s12911-023-02332-y, PMID 37932709. — [Europe PMC 37932709](https://europepmc.org/article/MED/37932709)

**Radius ratios / Murray's law**
- Taylor DJ, Saxton H, Halliday I, et al. Systematic review and meta-analysis of Murray's law in the coronary arterial circulation. *Am J Physiol Heart Circ Physiol* 2024. doi:10.1152/ajpheart.00142.2024, PMID 38787386. **[in refs.bib as taylor2024murray]**. Why: the definitive reference for the expected exponent, against which "deviation" is defined. — [Europe PMC 38787386](https://europepmc.org/article/MED/38787386)
- Shumal M, Saghafian M, Shirani E, et al. Association of Murray's law with atherosclerosis risk: numerical validation of a general scaling law of arterial tree. *Comput Biol Med* 2025. doi:10.1016/j.compbiomed.2025.109741, PMID 39874813. A simulation linking departure from Murray scaling to atherogenic haemodynamics. Not in refs.bib. Nice-to-have: it pairs with Garcha as a second simulation source. — [Europe PMC 39874813](https://europepmc.org/article/MED/39874813)
- Finet 2008, Huo 2012, Schoenenberger 2012 **[all in refs.bib]**: scaling-law and diameter-ratio physiology. — `thesis/refs.bib`
- No clinical study relating Murray deviation or daughter radius ratio to plaque incidence or progression was found (Europe PMC query: coronary AND Murray/Finet/scaling law AND plaque/atherosclerosis AND bifurcation, 2010-2026, 357 hits, all PCI/QCA/physiology). This is consistent with round 1 and with `find_research.md` "Not searched". — Europe PMC search 2026-10-04

**Dominance (per-artery models)**
- Gebhard C, et al. CONFIRM. *EHJ-CVI* 2015;16(8):853-862. doi:10.1093/ehjci/jeu314 (n=6382, no survival difference by dominance) **[in refs.bib]**; Khan 2016 meta (OR 1.27 for mortality after ACS) **[in refs.bib]**; Veltman 2012 **[in refs.bib]**; Wu 2024 JAHA review **[in refs.bib]**. Full detail in `find_research.md` §1.3. — `knowledge/docs_thesis/find_research.md`

### Inferences
- An examiner reading the intro aims list will check that each named feature has prior work in the review.
  Angles have it (Cui, Juan, Tommasino, Givehchi). Curvature has it (Kashyap, Zhang, Tello Ayala, Nannini).
  Labelling has none, and radius ratios have only one synthetic study. Two sentences would close both:
  - "Automated labelling of the extracted tree into named arteries has been developed on CCTA with graph
    and tree networks \cite{wu2019treelab,hampe2024gnn}."
  - "Branch radius ratios rest on scaling laws \cite{taylor2024murray} and simulation \cite{garcha2025sensitivity};
    no clinical study has related them to plaque."
  The second sentence also strengthens the gap.
- Dominance is not a thesis feature, so leaving it out of the review is defensible. It should appear where
  per-artery modelling is justified (methods), because left-dominant trees change what "the RCA model" means.

### Gaps
- I did not find a CCTA labelling benchmark on a population (non-referred) cohort. All labelling methods
  were trained and tested on clinical scans, which is a transfer risk for CGPS worth one line in methods.

## Q5. Papers already held locally that should be used

### Takeaway
Several useful sources are already in `refs.bib` and cost nothing to add: Hampe 2024 (labelling), Taylor 2024
(Murray), Medrano-Gracia 2016 (normative automated tree geometry), van Zandwijk (curvature changes over the
cardiac cycle), Eslami 2021 (CCTA vs invasive WSS), Kwon 2022 and Li 2011 (age and sex confounding of
geometry, which justifies the age+sex baseline), and the dominance set. New items not held, in priority order:
Chen 2024, Lee 2024 JCCT, CArTI 2025, SCAPIS re-examination 2026, EMERALD, PROSPECT-ESS, ESC 2021 or Detrano
2008, Wu 2019 TreeLab-Net.

### Cited Findings
- In refs.bib, not cited in the chapter: `hampe2024gnn`, `taylor2024murray`, `finet2008fractal`, `huo2012scaling`, `schoenenberger2012murray`, `medranogracia2016atlas`, `medranogracia2017bifurcation`, `vanzandwijk2019curvature`, `eslami2021ccta`, `kwon2022carotid`, `gebhard2015dominance`, `khan2016dominance`, `veltman2012dominance`, `wu2024dominance`, `zhao2023eagmn`, `mansouri2024bifurcation`, `zebicmihic2023tortuosity`, `sun2026angiographcad`, `zeng2023imagecas`, `dong2023casnet`, `fuchs2023cgps`. — `thesis/refs.bib` grep 2026-10-04
- Not in refs.bib: Chen 2024, Lee 2024 JCCT, CArTI 2025, Good 2026 SCAPIS re-exam, Lee 2019 EMERALD, Stone 2018 PROSPECT-ESS, Visseren 2021 ESC, Detrano 2008, Wu 2019 TreeLab-Net, TTN 2024, Shumal 2025, Feng 2025, Zhao 2025, Kumar 2018, Gijsen 2019, Iwami 1998. — `thesis/refs.bib` grep 2026-10-04
- `literature.md` already flags EAGMN, HAGMN-UQ and multi-resolution GCN as "relevant for CGPS, where predicted trees arrive unlabelled". `find_research.md` lists CArTI as "chase if a full paper appears" and marks Chen, EMERALD and PROSPECT as blocked. — `knowledge/docs_thesis/literature.md` l.272-275; `find_research.md` l.633-660

### Inferences
- Citing `fuchs2023cgps` once in the gap paragraph, as the cohort that can close the gap, would tie the
  review to the thesis design. It is currently cited only in the intro.
- **Priority list**
  - **Must-cite:**
    - Chen 2024: the plaque-free, new-plaque, vessel-feature precedent.
    - Lee 2024 JCCT: new plaque from baseline CCTA features in 9583 normal segments.
    - CArTI 2025: automated CCTA tortuosity/curvature to MACE; contradicts "geometry has not been tested in this role".
    - SCAPIS re-examination 2026: the competing general-population serial cohort.
    - Hampe 2024 or Wu 2019: covers the labelling aim.
    - Taylor 2024: covers the radius-ratio aim and shows no clinical cohort exists.
  - **Should-cite:**
    - EMERALD and PROSPECT-ESS: WSS-outcome evidence on CCTA and IVUS.
    - ESC 2021 or Detrano 2008: CAC as the guideline imaging refiner.
    - Medrano-Gracia 2016: normative automated tree geometry.
    - van Zandwijk: curvature over the cardiac phase.
    - Amsterdam 10-year serial CCTA (Nurmohamed 2024): interval analogue of CGPS, no geometry.
  - **Nice-to-have:**
    - Feng 2025 and Zhao 2025 (FAI and new plaque).
    - Shumal 2025 (Murray simulation).
    - TTN 2024 and Brandt 2024 (labelling).
    - Kumar 2018, Gijsen 2019, Eslami 2021.
    - The dominance set, which belongs in methods.

### Gaps
- Not verified whether `vanzandwijk2019curvature` in refs.bib is the J Digit Imaging 2020 paper that round 1
  cited (the key says 2019, which is possibly the online-first year).
