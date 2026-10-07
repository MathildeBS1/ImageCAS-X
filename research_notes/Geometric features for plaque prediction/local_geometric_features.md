# Local coronary geometric features that predict plaque location and development

Scope: human coronary arteries, CCTA-measurable lumen and centerline geometry. The user already has (1) bifurcation diameter ratio, (2) daughter-daughter bifurcation angle, (3) local turning angle along the centerline. Researched 2026-10-05.

Evidence tags used below:
- **[ABS]** abstract read in this session (Europe PMC REST API returned full abstracts).
- **[PRIOR-FT] / [PRIOR-ABS] / [PRIOR-SNIP]** taken from the repo's earlier notes, `knowledge/research_notes/Plaque prone regional geometry descriptors/*.md`, at the evidence level recorded there (full text / abstract / search snippet). These were not re-read here.
- **[SNIP]** only a search-engine summary was seen.
- Design labels: **XS** = cross-sectional association; **PROSP** = prospective / serial (baseline geometry or WSS, later plaque change or event); **CFD** = simulation only; **ANIMAL** = animal model.

Note on CGPS relevance: no source found tests baseline geometry against later plaque in a general-population or plaque-free cohort. Every prospective study below enrolled patients with established CAD or ACS, and almost all prospective evidence is for CFD-derived WSS, not for raw geometry.

## Q1. Which candidate local geometric features beyond the three have evidence, and how strong is it?

### Takeaway
The only feature with strong, repeated evidence that the three existing features do not capture is **position along the vessel (distance from the ostium / proximal location)**, with **local lumen diameter (radius) and its local expansion/taper** second, mainly as the dominant geometric determinant of WSS. **Presence of a ramus intermedius (LM trifurcation)** and the **RCA-aorta take-off angle** have newer cross-sectional CCTA support. Torsion, eccentricity, segment length, side-branch density and Murray-law residuals have weak or no direct plaque evidence. Myocardial bridging is well supported (tunnel spared, proximal segment affected) but needs a myocardium mask, not just a centerline.

### Cited Findings

**A. Position along the vessel / distance from ostium (NOT captured by the three features). Evidence: strong for location, moderate for progression.**
- 208 consecutive STEMI patients (Brigham and Women's): culprit occlusions clustered in the proximal third of RCA (P=0.001), LAD (P=0.003) and LCx (P=0.001); per 10 mm increase in distance from the ostium, occlusion risk fell 13 % (RCA), 30 % (LAD), 26 % (LCx) by Poisson regression. XS, endpoint is occlusion site, not plaque onset. [ABS] [Wang et al., Circulation 2004, PMID 15249505](https://doi.org/10.1161/01.cir.0000135468.67850.f4)
- PARADIGM serial CCTA (1,343 patients, mean interscan 3.3 y): in the 334 plaque-free at baseline, 35 % developed new lesions, most often in the LAD (60 %); no geometric predictors reported. PROSP (artery level only). [PRIOR-ABS] [EHJ CVI 2026 Suppl jeaf367.317](https://academic.oup.com/ehjcimaging/article/27/Supplement_1/jeaf367.317/8446296)
- PARADIGM (1,478 patients): proximally located lesions had more low-attenuation plaque and progressed faster. PROSP. [PRIOR-SNIP] [PARADIGM review, JCCT](https://www.sciencedirect.com/science/article/abs/pii/S1934592521004640)

**B. Local lumen diameter / radius, and local expansion or taper (NOT directly captured; the diameter ratio uses diameters only at bifurcations). Evidence: moderate, indirect (via WSS).**
- In 39 human left coronary trees (ASOCA CTCA + CFD), the only geometry-hemodynamics correlations surviving multiple-comparison correction were diameter ones: Marginal diameter vs average TAESS r = -0.85 (adjusted p = 0.0046), Diagonal diameter vs helicity h1 r = -0.75 (adjusted 0.036). Curvature and torsion correlations (|r| about 0.46 to 0.65) did not survive. CFD, XS. [PRIOR-FT] [Shen et al. 2025, arXiv 2502.06161](https://arxiv.org/abs/2502.06161)
- In the same 39 trees, side-branch diameter differed between stenosed and non-stenosed bifurcations (p = 0.041), whereas no bifurcation angle or Finet ratio did (p > 0.057). XS, n small. [PRIOR-FT] [Zhang et al. 2023, arXiv 2312.00257](https://arxiv.org/abs/2312.00257)
- Curvature correlates negatively with diameter across segments (r = -0.474, p = 0.002), so raw curvature partly re-encodes vessel size. [PRIOR-FT] [Zhang et al. 2023](https://arxiv.org/abs/2312.00257)
- Normal-atlas taper is about 0.25 mm diameter per 10 mm distal to bifurcations (300 zero-calcium adults, Auckland). Reference values, not plaque evidence. [PRIOR-ABS] [Medrano-Gracia et al., EuroIntervention](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)
- Human carotid (MRI, 50 bifurcations): factor analysis of 14 geometric variables found two factors predicting 12 WSS/residence-time metrics (adjusted R^2 up to 0.54): **cross-sectional expansion at the bifurcation** and **colinearity of parent and daughter axes**; these "explain the apparent lack of an effect of branch angle on hemodynamic risk". Carotid, CFD. Relevant as a design argument that area expansion beats angle. [ABS] [Friedman group, J Biomech Eng 2010, PMID 21034157](https://doi.org/10.1115/1.4002538)
- Patient-level size proxy: coronary lumen volume to myocardial mass ratio (V/M). Low V/M in 238 NXT patients went with more plaque, greater QCA stenosis and lower FFR (0.80 vs 0.87, P < 0.0001). Global, not local; XS. [ABS] [JCCT 2017, PMID 28789941](https://doi.org/10.1016/j.jcct.2017.08.001)

**C. Bifurcation-specific features related to, but not identical to, the existing angle/ratio.**
- **Left main bifurcation angle, plaque on lateral wall.** 50 patients, 40-row MSCT: >90 % of LM-bifurcation plaques opposite the flow divider; 72 % of patients with normal ostial LAD had angle < 88.5 deg, while 63 % with any LAD disease had angle >= 88.5 deg (P = 0.018). XS. [ABS] [Int J Cardiovasc Imaging 2007, PMID 17028928](https://doi.org/10.1007/s10554-006-9144-1)
- Dual-source CT: LAD-LCx angle 94.3 +/- 16.5 deg in diseased vs 76.5 +/- 15.9 deg in normal left coronary arteries; independent predictor of significant left stenosis; wider with non-calcified plaque. XS. [PRIOR-SNIP] [PLOS One 2017](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0174352)
- **LM-LAD (take-off of LAD from LM) angle**, distinct from the LAD-LCx daughter angle: 578 symptomatic patients (Isfahan, CCTA); LM-LAD cut-off 30 deg gave sensitivity 52 % / specificity 69 % for pLAD stenosis >= 50 %; LAD-LCx cut-off 50 deg gave 70 % / 59 %. Weak discrimination. XS. [ABS] [ARYA Atheroscler 2026, PMID 41972218](https://doi.org/10.48305/arya.2025.45215.3052)
- **Ramus intermedius (trifurcation).** 1,380 CCTA patients: RI present in 31.8 %; RI was the strongest risk factor (uni- and multivariable) for plaque in LMCA, proximal LAD and proximal LCx; bifurcation angle larger with RI. XS. [ABS] [Clin Radiol 2026, PMID 41962318](https://doi.org/10.1016/j.crad.2026.107299). In the normal atlas, LM angle B was 89 vs 75 deg with vs without an intermediate branch (p < 0.001). [PRIOR-ABS] [Medrano-Gracia](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)
- **Inflow / out-of-plane (non-planarity) angle of the parent into the daughters' plane** and **axis colinearity**: defined in the atlas and in Zhang 2023 but no plaque association found. [PRIOR-FT] [Zhang et al. 2023](https://arxiv.org/abs/2312.00257)

**D. Ostial take-off angle of the RCA (NOT captured). Evidence: weak, XS, one group.**
- 250 CCTA patients: RCA-aorta angle smaller in CAD (79.1 +/- 24.9 deg) than normal (92.1 +/- 19.5 deg, p = 0.001); also smaller in smokers and correlated with BMI (r = -0.174). XS. [ABS] [J Clin Med 2023, PMID 36769698](https://doi.org/10.3390/jcm12031051)
- Pilot, 30 vs 30: RCA-aorta 87.5 vs 76.8 deg (P = 0.05); no relation to stenosis degree (P = 0.75). XS. [ABS] [QIMS 2023, PMID 36915318](https://doi.org/10.21037/qims-22-655)
- Acute take-off angle as a "high-risk feature" in anomalous origins concerns compression/ischaemia, not atherosclerosis. [ABS] [Diagnostics 2026, PMID 42587700](https://doi.org/10.3390/diagnostics16152465)

**E. Curvature / tortuosity (partly captured by turning angle). Evidence: mixed sign.**
- 39 ASOCA trees: average curvature differed between non-stenosed and stenosed trees (whole tree and non-bifurcating segments, p < 0.024, AUC > 0.711); TSVI (a multidirectional WSS metric) was the only metric differing consistently (AUC 0.876). XS + CFD. [ABS] [Royal Soc Open Sci 2024, PMID 39309260](https://doi.org/10.1098/rsos.241267)
- RCA tortuosity, ML pipeline on 38,691 angiograms (22,334 patients): higher in women (beta per SD 0.17) and with hypertension, lower with diabetes; associated with CAD (OR per SD 1.05, P < 0.001) and severe CAD (OR per SD 1.09) after adjustment. XS, whole-vessel. [ABS] [JACC Advances 2026, PMID 42312790](https://doi.org/10.1016/j.jacadv.2026.102829). This **contradicts** the smaller "severe tortuosity protects / goes with non-obstructive CAD" literature: 131 patients, OR 7.96 for non-obstructive CAD, heavily sex-confounded. [PRIOR-FT] [Zebic Mihic 2023, PMC10534717](https://pmc.ncbi.nlm.nih.gov/articles/PMC10534717/)
- Plaque localises to the inner wall of bends, where WSS is lower. [SNIP, review/patent-level statement] [USPTO 9785748 (HeartFlow)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9785748); [PRIOR-SNIP] [PMC9497479 review](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)

**F. Torsion (NOT captured by a turning-angle measure, which is in-plane curvature). Evidence: weak.**
- DMV torsion differed between stenosed and non-stenosed bifurcations (p = 0.024, unadjusted) in 39 ASOCA trees. XS. [PRIOR-FT] [Zhang et al. 2023](https://arxiv.org/abs/2312.00257)
- Torsion correlations with helicity/RRT (r = -0.46 to 0.65) did not survive multiplicity correction. [PRIOR-FT] [Shen et al. 2025](https://arxiv.org/abs/2502.06161)
- Helical-tube model: WSS changed up to 22 % with curvature change, 3 % with torsion change. CFD. [PRIOR-SNIP] [J Biomech Eng 2012](https://asmedigitalcollection.asme.org/biomechanical/article-abstract/134/7/071005/464806/Investigation-of-the-Effects-of-Dynamic-Change-in)
- Swine: torsion-driven bi-helical flow and high helicity associated with low wall-thickness growth (atheroprotective). ANIMAL. [PRIOR-SNIP] [De Nisco et al., Ann Biomed Eng 2019](https://link.springer.com/article/10.1007/s10439-018-02169-x)

**G. Myocardial bridging (NOT captured; needs myocardium). Evidence: consistent for location (tunnel spared), contested for proximal excess.**
- 36 CCTA patients with MB: no plaque in any tunnelled segment; 12 had plaque proximal to the bridge; ESS 1.2 Pa proximal, 0.95 within, 2.98 distal. [PRIOR-FT] [PMC10870693](https://pmc.ncbi.nlm.nih.gov/articles/PMC10870693/)
- Matched angiography study (76 MB vs 109 controls): MB patients had *lower* proximal LAD atherosclerotic load (30.3 vs 42.9 %, p = 0.038). [PRIOR-FT] [PMC9026775](https://pmc.ncbi.nlm.nih.gov/articles/PMC9026775/)

**H. Eccentricity / ellipticity, segment length between bifurcations, side-branch density, Murray/Finet residual.**
- Plaque eccentricity and lumen asymmetry indices exist on CCTA (231 vessels) but are used as plaque descriptors affecting FFR accuracy, not as baseline predictors. [ABS] [CAREER trial, CCI 2026, PMID 42020959](https://doi.org/10.1002/ccd.70642)
- Side branches: including side branches >1 mm in reconstructions lowered minimum TAWSS (1.09 vs 1.58 Pa) and improved prediction of IVUS progression (40 vessels, 1-year). This shows side-branch geometry modulates WSS locally, not that side-branch count predicts plaque. PROSP. [ABS] [ATVB 2026, PMID 42131920](https://doi.org/10.1161/atvbaha.126.324466)
- Finet ratio did not differ between stenosed and non-stenosed bifurcations (39 trees). [PRIOR-FT] [Zhang et al. 2023](https://arxiv.org/abs/2312.00257)

### Inferences
- Ranking of features not already in the set, by strength of plaque-location evidence: (1) arc length from ostium / proximal position; (2) local lumen radius and local expansion (area ratio vs neighbourhood); (3) LM trifurcation flag (ramus); (4) LM-LAD take-off angle and RCA-aorta angle; (5) torsion; (6) eccentricity, segment length, side-branch density, Murray residual (no direct evidence).
- Position along the vessel is the cheapest and best-supported missing feature. It partly works through flow development and the proximity of large bifurcations, but it is empirically strong on its own (13 to 30 % risk reduction per 10 mm).
- The bifurcation diameter ratio uses radius only at bifurcations; a per-node radius or local area-expansion term is what carries the strongest geometry-to-WSS signal in human CFD data.

### Gaps
- No source quantified eccentricity, segment length or side-branch density as predictors of plaque presence or onset.
- Murray/Finet/Huo-Kassab deviation vs plaque: no human study found beyond the null Finet result in 39 trees. Earlier notes flagged conflicting claims about which law fits coronaries.
- The PLOS One 2017 LM-angle numbers remain snippet-level.

## Q2. Which features are proxies for low/oscillatory WSS, and which add information beyond curvature + bifurcation angle + diameter ratio?

### Takeaway
All candidate features act through disturbed flow except distance from ostium (partly flow development, partly unexplained) and myocardial bridging (compression). In human CFD, radius and cross-sectional expansion are stronger WSS determinants than angles or curvature; torsion mostly acts through helical flow, which is atheroprotective. So the most informative addition is a radius-based term, not another angle.

### Cited Findings
- Diameter is the only geometric WSS correlate surviving multiplicity correction in 39 human trees (r = -0.85 with average TAESS). [PRIOR-FT] [Shen et al. 2025](https://arxiv.org/abs/2502.06161)
- Helical flow intensity (driven by curvature and torsion) is associated with higher TAESS and less low-TAESS area in stenosed trees (p = 0.0001). [PRIOR-FT] [Shen et al. 2025](https://arxiv.org/abs/2502.06161)
- In carotids, expansion and axis colinearity, not branch angle, predicted WSS risk metrics (R^2 up to 0.54, sensitivity/specificity up to 0.84). [ABS] [J Biomech Eng 2010, PMID 21034157](https://doi.org/10.1115/1.4002538)
- Multidirectional WSS (TSVI, transWSS) adds to TAWSS: TSVI was superior to TAWSS for predicting future MI culprits (AUC 0.77 vs 0.61; 80 culprit vs 108 non-culprit lesions, 3D-QCA). [ABS] [Candreva et al., Atherosclerosis 2022, PMID 34815069](https://doi.org/10.1016/j.atherosclerosis.2021.11.010)
- Wider bifurcation angles concentrate low WSS and OSI on lateral walls and increase helicity. [PRIOR-SNIP] [JAHA 2024 review](https://www.ahajournals.org/doi/10.1161/JAHA.124.037129)
- With a Poiseuille WSS estimate and a coronary flow law Q proportional to d^2.55, WSS scales as d^-0.45, so a node's own radius alone is monotone with WSS; information beyond radius arises only when flow is propagated from the root (local ectasia, post-stenotic widening). [PRIOR derivation] see `hemodynamic_geometry_proxies.md` section 4.

### Inferences
- Redundancy with the existing three: torsion and "curvature ratio" kappa*r add little beyond turning angle plus radius. LM-LAD take-off angle is partly a re-parameterisation of the bifurcation geometry (parent-daughter angle rather than daughter-daughter), so it adds the parent-axis information that the carotid data suggest matters (colinearity).
- Not redundant: (a) local radius and local area expansion along a segment, (b) arc length from ostium, (c) ramus/trifurcation flag, (d) MB if a myocardium mask exists.

### Gaps
- No coronary factor-analysis study analogous to the 2010 carotid one was found.
- No validation of TSVI or helicity predicted from geometry alone.

## Q3. Longitudinal evidence linking geometry or geometry-derived WSS to new plaque or progression

### Takeaway
Prospective human evidence exists for **CFD-derived low (and multidirectional) WSS** predicting plaque growth and lumen narrowing in patients with established CAD (PREDICTION, Samady, Wentzel group, PROSPECT sub-study). **No prospective study was found where raw geometry (angle, curvature, diameter ratio, torsion) is the predictor**, and none in a plaque-free general population. High WSS predicts compositional transformation and events in already stenotic lesions.

### Cited Findings
- **PREDICTION (Stone et al. 2012).** 506 ACS patients after PCI, 3-vessel IVUS + angiography CFD, 374 (74 %) re-imaged at 6 to 10 months, arteries split into 3 mm segments. Plaque area increase predicted by large baseline plaque burden; lumen area decrease independently predicted by large plaque burden and low ESS. Combined predictors: PPV 41 %, NPV 92 % for progression to a PCI-treated obstruction. PROSP, Japanese ACS cohort. [ABS] [Circulation 2012, PMID 22723305](https://doi.org/10.1161/circulationaha.112.096438)
- **Samady et al. 2011.** 20 CAD patients, VH-IVUS + CFD at baseline and 6 months, 2,249 segments. Low WSS: plaque area (P = 0.027) and necrotic core (P < 0.001) progression, vessel and lumen shrinkage (constrictive remodelling 73 % vs 30 %, P = 0.06). High WSS: necrotic core and calcium progression, fibrous regression, expansive remodelling. PROSP. [ABS] [Circulation 2011, PMID 21788584](https://doi.org/10.1161/circulationaha.111.021824)
- **PROSPECT ESS sub-study.** 697 ACS patients, 3.4 y follow-up; 145 non-culprit lesions (23 MACE). Low ESS < 1.3 Pa: 23/101 MACE vs 0/44 with ESS >= 1.3 Pa; propensity-adjusted HR 4.34 (1.89 to 10.00). PROSP, US/Europe ACS. [ABS] [Stone et al., JACC CVI 2018, PMID 28917684](https://doi.org/10.1016/j.jcmg.2017.01.031)
- **Costopoulos et al. 2019.** 40 patients, VH-IVUS at baseline and 12 months, 4,029 frames. Low WSS associated with larger plaque burden increase in progressing areas (difference 3.3 +/- 0.4 %, P < 0.001). WSS and plaque structural stress nearly independent (R^2 = 0.002). PROSP. [ABS] [Eur Heart J 2019, PMID 30907406](https://doi.org/10.1093/eurheartj/ehz132)
- **Multidirectional WSS in humans (Wentzel group, Kok et al. 2019).** 20 CAD patients, VH-IVUS at baseline and 6 months: regions with low TAWSS and low multidirectional WSS showed the greatest plaque progression (p < 0.001); multidirectional WSS mainly related to composition change. PROSP. [ABS] [EuroIntervention 2019, PMID 30860071](https://doi.org/10.4244/eij-d-18-00529)
- **Hoogendoorn et al. 2020.** 10 familial hypercholesterolaemic pigs, 3648 sectors, imaged at 3, 9, 10 to 12 months: highest progression only at low TAWSS or high multidirectional WSS. ANIMAL, PROSP. [ABS] [Cardiovasc Res 2020, PMID 31504238](https://doi.org/10.1093/cvr/cvz212)
- **Bourantas et al. 2020.** 3D-QCA ESS in 28 MACE-R vs 119 quiescent fibroatheromas over 5 years: plaque burden (HR 1.08) and max 3 mm ESS (HR 1.11) independent predictors; high ESS > 4.95 Pa plus high-risk anatomy gave 53.8 % MACE-R. PROSP (events). [ABS] [JACC CVI 2020, PMID 32417338](https://doi.org/10.1016/j.jcmg.2020.02.028)
- **Kumar et al. 2018 (FAME II).** 441 medically treated FFR <= 0.80 patients; 29 MI vs 29 matched controls: proximal-lesion WSS HR 1.234 (p = 0.002), NRI 0.69 when added to FFR. PROSP (events). [ABS] [JACC 2018, PMID 30309470](https://doi.org/10.1016/j.jacc.2018.07.075)
- **Candreva et al. 2022.** TSVI predicted future MI culprits (AUC 0.77), NRI 1.04 over stenosis + delta vFFR. Retrospective-prospective (baseline angiography median 25.9 months before MI). [ABS] [Atherosclerosis 2022, PMID 34815069](https://doi.org/10.1016/j.atherosclerosis.2021.11.010)
- **CCTA-based ESS.** 7 patients with CCTA + IVUS: plaque prevalence 49.6 % at low ESS, 34.8 % at high ESS, 20 to 24 % at intermediate ESS (U-shape). XS. [ABS] [Hetterich et al., PLoS One 2015, PMID 25635397](https://doi.org/10.1371/journal.pone.0115408). A serial CCTA WSS study of 11 patients / 7,592 sectors was found only as a search summary. [SNIP] [search result listing](https://pmc.ncbi.nlm.nih.gov/articles/PMC8749833)
- **Side branches in reconstructions** improved WSS prediction of 1-year IVUS progression (40 vessels). PROSP. [ABS] [ATVB 2026, PMID 42131920](https://doi.org/10.1161/atvbaha.126.324466)
- Review framing: shear stress improves prediction of progression only incrementally. [ABS] [Thondapu et al., Eur Heart J 2017, PMID 28158723](https://doi.org/10.1093/eurheartj/ehv689)

### Inferences
- The longitudinal chain for CGPS has to be argued in two steps: geometry determines WSS (CFD, XS), and low/multidirectional WSS predicts progression (PROSP, CAD patients). The second step has not been shown for plaque *onset* in plaque-free humans; PARADIGM's plaque-free subgroup (LAD-first) is the closest and reports no geometry.
- Effect sizes are modest (PPV 41 %, HR 1.1 to 4.3) and largely in already-diseased segments, so a geometry-only model in CGPS should expect modest discrimination.

### Gaps
- Did not retrieve the PARADIGM full texts on location, nor any PARADIGM analysis with bifurcation angle or curvature as predictor; unclear whether one exists.
- Did not find the "Kim/Taylor HeartFlow" serial new-plaque WSS study; EMERALD (culprit vs non-culprit, CCTA-CFD) remains snippet-level from earlier notes.
- Antoniadis and Chatzizisis papers were not retrieved in this session.

## Q4. Is lumen diameter/taper or torsion repeatedly reported as an independent predictor?

### Takeaway
**Diameter: partly yes, mostly as an independent determinant of WSS and as minimum lumen area in event studies, not as a predictor of plaque onset. Taper: no independent plaque evidence found. Torsion: no; isolated unadjusted signals only.**

### Cited Findings
- Small minimum lumen area was an independent predictor of non-culprit MACE in PROSPECT (with plaque burden and TCFA). This is a lesion-level, post-disease measure. [ABS] [Stone et al., JACC CVI 2018](https://doi.org/10.1016/j.jcmg.2017.01.031)
- Diameter survives correction as WSS correlate in 39 human trees; curvature and torsion do not. [PRIOR-FT] [Shen et al. 2025](https://arxiv.org/abs/2502.06161)
- Side-branch diameter (p = 0.041) and DMV torsion (p = 0.024) separated stenosed bifurcations, unadjusted, 54 bifurcations. [PRIOR-FT] [Zhang et al. 2023](https://arxiv.org/abs/2312.00257)
- Global vessel size relative to myocardium (V/M) independently linked to lower FFR and more plaque. [ABS] [JCCT 2017, PMID 28789941](https://doi.org/10.1016/j.jcct.2017.08.001)
- Curvature effect on WSS dominates torsion (22 % vs 3 %). CFD. [PRIOR-SNIP] [J Biomech Eng 2012](https://asmedigitalcollection.asme.org/biomechanical/article-abstract/134/7/071005/464806/Investigation-of-the-Effects-of-Dynamic-Change-in)

### Inferences
- If one feature is added, local radius (normalised, e.g. radius relative to the vessel's proximal reference or a local expansion ratio) has the best support and complements the bifurcation diameter ratio. Torsion is third-derivative and noisy on 0.5 mm voxel centerlines (earlier repo notes), with weak evidence, so it is a poor candidate.
- Arc length from ostium is a near-free, well-supported positional covariate; it may be better treated as a covariate than a "geometric feature".

### Gaps
- No study found that tests taper (dr/ds) as a plaque predictor in human coronaries.
- No inter-scan reproducibility data for local radius or torsion on CCTA were found.
