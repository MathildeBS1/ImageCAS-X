# Inconsistencies in the literature on five coronary geometric features and plaque/CAD (and their WSS link)

Scope: curvature/tortuosity, lumen taper, LM bifurcation angle, LM→LAD and LM→LCx diameter ratios, and the WSS
link for each. This builds on the earlier notes in `research_notes/Coronary geometry known correlates/` and
`research_notes/Taper and curvature interaction for WSS/clinical_evidence.md`. Where a number comes from those
notes, the source they used is cited.

Access legend, used after each source:
- **[FT]** full text read (in this or an earlier session).
- **[Abs]** abstract, repository record or Europe PMC record only.
- **[Sec]** secondary source only (review table or search summary). Verify before citing a number.
- **[Pre]** preprint, not peer reviewed.

Shen 2026 is excluded on the author's instruction. Note that Zhang 2024 (RSOS) has a co-author named Shen (C).
It is a 2024 paper, not the excluded one, but check with the author that it is not affected by the exclusion.

## Q1. Curvature / tortuosity: who disagrees, and why?

### Takeaway
The sign of the association depends mainly on the definition and the endpoint.

- **Inverse findings.** Visual bend counts on invasive angiography, against obstructive stenosis in referred
  chest-pain patients: Groves 2009, Li 2011, Chiha 2017, Zebic Mihic 2023. Female sex confounds all of these
  heavily (women have more tortuosity and less CAD).
- **Inverse finding on CCTA.** One automated CCTA bend score against calcium volume (Nannini 2024). Its authors'
  own data suggest confounding by position along the artery.
- **Positive or null findings.** Continuous curvature: Tuncay/Utrecht 2018 CCTA against any plaque; Tello Ayala
  2026 against angiographic stenosis; Leng/APOLLO CCTA abstract.
- **No longitudinal test.** None of these studies follows people from a plaque-free baseline. All are
  cross-sectional.
- **WSS literature.** It also points both ways. Curvature tracks low TAWSS (Kashyap 2022, weak), but tortuosity
  raises WSS via helical flow in patient-specific models (Vorobtsova 2016) and lowers OSI/RRT (Gharleghi 2024).

### Cited Findings

**Inverse (more tortuosity → less CAD)**
- **Groves 2009** (W V Med J).
  - Cohort: n=1,221 angiograms, referred.
  - Definition: severe tortuosity = two consecutive 180° turns, visual.
  - Prevalence 12.45%. Severe tortuosity went with a lower incidence of significant CAD (p=0.003).
  - Cross-sectional. **[Abs]**
  - [PMID 19585899](https://pubmed.ncbi.nlm.nih.gov/19585899/)
- **Li 2011** (PLoS ONE).
  - Cohort: n=1,010 Chinese chest-pain patients, invasive angiography.
  - Definition: ≥3 bends ≥45° on a main artery, seen in systole and diastole.
  - Result: CAD OR 0.755 (0.574–0.994), with prevalence 45.1% without CAD vs 34.4% with CAD. LAD tortuosity was
    inverse to LAD atherosclerosis; the LCx and RCA showed no relation.
  - Female OR for tortuosity 2.603; hypertension OR 1.533.
  - Cross-sectional. **[FT]**
  - [DOI 10.1371/journal.pone.0024232](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0024232)
- **Chiha 2017** (IJC Heart Vasc).
  - Cohort: n=870 (589 men, 281 women), angiography for suspected CAD, Westmead.
  - Severe tortuosity in 45.2% of women vs 19.7% of men (p<0.001).
  - Women with severe tortuosity had lower Extent and Gensini scores. In men, tortuosity went only with a lower
    Extent score.
  - The conclusion is framed around sex: "Women with severe tortuosity are more likely to have normal coronary
    arteries or less severe disease than men".
  - Cross-sectional, referred. **[Abs]**
  - [DOI 10.1016/j.ijcha.2016.11.005](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE:%22Gender%20differences%20in%20the%20prevalence%20of%20coronary%20artery%20tortuosity%22)
- **Zebic Mihic 2023** (Medicina 59:1619).
  - Cohort: n=131, angina or ACS, angiography. 77 non-obstructive vs 54 obstructive.
  - Tortuous arteries 50.6% vs 14.8%.
  - Predictors of non-obstructive CAD: female sex OR 17.516, tortuosity OR 7.962, left dominance.
  - The endpoint is *non-obstructive vs obstructive*, not plaque vs no plaque. **[Abs]**
  - [DOI 10.3390/medicina59091619](https://doi.org/10.3390/medicina59091619)
- **Zebic Mihic 2024** (Diagnostics 14:35).
  - Cohort: n=160 with angina and ischaemia; compares the tortuosity index (arc/chord) with the angle method.
  - Tortuosity and the index were higher in non-obstructive than obstructive CAD for all three arteries (p<0.01).
  - Tortuosity index localised ischaemia (LCx–lateral, LAD–anterior); the angle method found only LCx–lateral
    (OR 4.9).
  - Authors' frame: tortuosity is a *mechanism of ischaemia without obstructive CAD*, not a plaque risk factor.
    **[FT, prior notes]**
  - [DOI 10.3390/diagnostics14010035](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10795752/)
- **Nannini 2024** (APL Bioeng).
  - Cohort: automated deep-learning CCTA; bend-count tortuosity score.
  - Higher tortuosity went with lower calcium volume (p<0.001).
  - Within vessels, tortuosity rose and calcium fell from proximal to distal, so position along the artery is a
    plausible confounder. **[Abs]**
  - [DOI 10.1063/5.0181281](https://re.public.polimi.it/handle/11311/1276541)
- **Estrada 2022** (Arq Bras Cardiol).
  - Tortuosity was associated with ischaemia in patients *without* CAD. The editorial calls tortuosity "a new
    phenotype for ischemia without CAD".
  - This is not a plaque endpoint. **[Sec, editorial only]**
  - [Editorial](https://abccardiol.org/en/short-editorial/coronary-tortuosity-as-a-new-phenotype-for-ischemia-without-coronary-artery-disease); [PMC9814816](https://pmc.ncbi.nlm.nih.gov/articles/PMC9814816)

**Positive or null (more curvature → more plaque or stenosis)**
- **Tuncay et al. 2018** (Utrecht, J Cardiovasc Comput Tomogr 12:257).
  - Cohort: 73 patients, CCTA, RCA.
  - Curvature was higher in segments with stenosis (+16.7%) and with plaque, at segment and artery level.
  - Tortuosity (arc/chord) was related to plaque at segment level only. The same group's ESCR 2014 poster reports
    *no* tortuosity association, so the group's own results conflict.
  - Cross-sectional. **[Abs/Sec]**
  - [ESCR poster](https://epos.myesr.org/poster/escr/escr2014/458); [Utrecht record](https://researchinformation.umcutrecht.nl/en/publications/non-invasive-assessment-of-coronary-artery-geometry-using-coronar/)
- **Tello Ayala 2026** (JACC Adv 5:102829).
  - Cohort: 22,334 patients, 38,691 RCA LAO loops; 2D invasive angiography, single-centre registry; prior PCI or
    CABG not excluded.
  - Definition: automated mean absolute turning angle/π.
  - Results (adjusted, per SD): CAD (any RCA stenosis) OR 1.05 (1.03–1.08); severe CAD OR 1.09 (1.06–1.13); mild
    and moderate CAD not significant.
  - In the same data the arc/chord index was weakly *inverse* to RCA stenosis (β −0.03, p=0.042). Arc/chord vs
    the new score: r=0.116.
  - Female β 0.17 SD; hypertension 0.06; diabetes −0.11; age null after adjustment.
  - Cross-sectional (concurrent CAD). **[FT]**
  - [DOI 10.1016/j.jacadv.2026.102829](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
  - **This is the clearest within-study proof that the definition flips the sign.**
- **Leng et al., APOLLO** (Eur Heart J suppl., likely a conference abstract).
  - Cohort: n=848, CCTA.
  - Definition: mean absolute curvature × vessel length.
  - Positive association with stenosis severity overall and per vessel (P<0.0001), adjusted for age, sex and
    hypertension. Obstructive CAD OR 1.074 (1.056–1.092); the unit is unstated.
  - Year and issue not shown. **[Abs; conference abstract]**
  - [DOI 10.1093/eurheartj/ehag785.175](https://www.citedrive.com/en/discovery/coronary-artery-tortuosity-is-independently-associated-with-stenosis-severity-obstructive-disease-and-hypertension/)
- **El Tahlawi 2016** (Atherosclerosis).
  - Cohort: n=83, CCTA, normal or near-normal coronaries.
  - Tortuosity went with a higher CAC score and with more hypertension. **[Abs, prior notes]**
  - [DOI 10.1016/j.atherosclerosis.2016.01.029](https://doi.org/10.1016/j.atherosclerosis.2016.01.029)
- **Null after adjustment.**
  - Chen 2022 (BMC Surg; n=1,280, CCTA): the calcium association was univariable only.
  - Sharfo 2024 (Danish CATCH, n=194, LAD arc/chord): no correlation with calcium.
  - **[FT / Abs, prior notes]**
  - [Chen 2022](https://link.springer.com/article/10.1186/s12893-022-01470-w); [Sharfo PMID 39210716](https://pubmed.ncbi.nlm.nih.gov/39210716/)
- **Han 2022, ICONIC** (nested case-control).
  - Tortuosity was an "adverse geometric characteristic" of future ACS culprits, but the counts were tiny (4.3% vs
    1.4%).
  - Endpoint: ACS, not plaque onset. **[Sec]**
  - [ACC Journal Scan](https://www.acc.org/Latest-in-Cardiology/Journal-Scans/2022/02/04/18/53/Association-of-Plaque-Location)

**Reviews and confounding**
- **Kahe 2020** (Coron Artery Dis 31:187–192; DOI reported as 10.1097/MCA.0000000000000769, not verified). The
  abstract:
  - associates tortuosity with ageing, hypertension and atherosclerosis;
  - proposes elastin degradation as the mechanism;
  - suggests "increased and oscillatory shear stress" in tortuous vessels *may promote* plaque;
  - calls it a mostly benign entity.
  - **[Abs]**
  - [LVHN record](https://scholarlyworks.lvhn.org/fellows-residents/101)
  - The review thus proposes the opposite mechanism to the inverse clinical studies.
- **Ciurică et al. 2019** (Hypertension, "Arterial tortuosity: novel implications for an old phenotype"). The title
  was located; the content was not read. **[title only]**
- **Eleid 2014** (Circ Cardiovasc Interv).
  - Cohort: SCAD n=246 (96% women) vs 313 controls.
  - Tortuosity 78% vs 17%.
  - Shows that tortuosity marks a non-atherosclerotic arteriopathy (FMD/SCAD), which pulls female, low-CAD
    patients into the tortuous group. **[Abs]**
  - [DOI 10.1161/CIRCINTERVENTIONS.114.001676](https://doi.org/10.1161/CIRCINTERVENTIONS.114.001676)

**WSS link (computational; the direction is also inconsistent)**
- **Kashyap 2022** (Sci Rep).
  - Data: 127 CCTA without CAD (LM, LAD, LCx).
  - Average absolute curvature had the highest R² with % area of TAWSS <0.4 Pa.
  - The arc/chord tortuosity index, the most widely used metric, showed no significant correlation (p=0.86).
  - The strength is described as modest in the thesis text; the R² values were not extracted. **[Abs]**
  - [DOI 10.1038/s41598-022-04796-w](https://doi.org/10.1038/s41598-022-04796-w)
- **Vorobtsova 2016** (Ann Biomed Eng 44:2228).
  - Design: idealised and patient-specific CFD.
  - More tortuosity → lower perfusion pressure but *higher* WSS, via helical flow.
  - The authors suggest higher WSS "could afford protection against atherosclerosis". **[Abs]**
  - [DOI 10.1007/s10439-015-1492-3](https://repub.eur.nl/pub/91183)
- **Gharleghi 2024** (arXiv 2401.12504; n=127 plaque-free CCTA).
  - Higher LAD/LCx curvature went with *less* high-OSI and high-RRT area (e.g. LCx β −0.519 for OSI).
  - Authors' wording: "potentially atheroprotective". **[Pre]**
  - [arXiv](https://arxiv.org/abs/2401.12504)
- **Zhang 2024** (R Soc Open Sci 11:241267).
  - Data: ASOCA left coronary trees; 20 non-stenosed, 12 moderate, 7 severe.
  - The topological shear variation index was the only metric that consistently separated non-stenosed from
    stenosed cases across the whole tree (p<0.002, AUC 0.876).
  - Curvature and %HighOSI separated only in some segments. The authors nonetheless propose that curvature and
    OSI drive *onset*, while low TAESS and high RRT drive *progression*.
  - Tiny, cross-sectional, stenosis-defined. **[Abs]**
  - [DOI 10.1098/rsos.241267](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11416812/)
- **Garcha & Grande Gutiérrez 2025** (Sci Rep).
  - Design: 230 *synthetic* left coronary models.
  - Tortuosity effects on adverse haemodynamics are amplified by the branch diameter ratio. Mild plaque did not
    change the structure–haemodynamics correlations. **[Abs]**
  - [DOI 10.1038/s41598-025-85781-x](https://www.arxiv.org/abs/2507.17109)

**Studies requested but not located**
- "Sun 2019" (tortuosity) and "Xie" (CCTA tortuosity and plaque) were not found. Xie, Wang & Zhou 2013 is a CFD
  study of tortuosity and flow, not plaque.
- "Estrada/Ciurică" resolved to Estrada 2022 (ischaemia, above) and Ciurică 2019 (review, title only).

### Inferences
- **The inverse/positive split is explained best by three things that coincide.**
  - Definition: visual bend counts and arc/chord vs continuous mean curvature. Tello Ayala shows both signs in the
    same 22k patients.
  - Endpoint: obstructive stenosis, non-obstructive "ischaemia" or Gensini vs any plaque or calcium.
  - Confounding: female sex (the largest correlate of tortuosity and inversely related to CAD in referred
    cohorts), SCAD/FMD, and position along the artery (distal segments are more tortuous and less calcified).
  - Age and hypertension go *with* both tortuosity and CAD, so they would bias towards a positive association, not
    an inverse one. The inverse findings are more plausibly sex, referral and definition effects.
- **Every study is cross-sectional, and almost all are referred.** In a referred cohort, tortuosity can itself
  produce symptoms (ischaemia without obstructive CAD; Zebic Mihic, Estrada). That enriches the referred group with
  tortuous, plaque-free people: a collider/referral bias toward an inverse association. A population sample such
  as CGPS avoids this mechanism.
- Most representative for a table: **Li 2011** (inverse, visual, angiography) and **Tello Ayala 2026**
  (positive with continuous curvature, inverse with arc/chord, same data). For the WSS column: **Kashyap 2022**
  (curvature ↔ low TAWSS) vs **Vorobtsova 2016** (tortuosity ↔ higher WSS).

### Gaps
- No study tests curvature on a plaque-free baseline against *incident* plaque.
- The Kashyap R² values, the full Chiha numbers and the Kahe review full text were not read.
- Groves 2009 is abstract-only.

## Q2. Lumen taper: is there clinical evidence, and does taper reflect disease rather than predict it?

### Takeaway
No clinical study was found in which lumen taper on a plaque-free vessel predicts later plaque. Taper appears in
two literatures, and both treat it as a *consequence* or *marker* of disease rather than as a cause:
- diffuse disease shrinks the lumen relative to the supplied bed (Seiler; Zhou/Kassab/Molloi; Huo/Kassab length–
  volume scaling);
- in FFR-CT and TAG, taper is a confounder that mimics a pressure or contrast gradient.

IVUS shows that lumen taper is partly caused by differential plaque accumulation. That is reverse causation for
any cross-sectional taper–plaque association.

### Cited Findings
- **Javier, Mintz et al. 1995** (Am J Cardiol; IVUS).
  - The LAD lumen tapers more (0.33 mm/10 mm) than the RCA (0.16) or LCx (0.15).
  - The mechanism varies: in some places the external elastic membrane tapers, in others plaque accumulates
    differentially.
  - **[Abs, prior notes]** [DOI 10.1016/s0002-9149(00)80072-7](https://doi.org/10.1016/s0002-9149(00)80072-7)
- **Normal angiographic tapering.** About 0.22 mm per 10 mm; reversed taper in about 10% of arteries.
  **[Sec]** [ResearchGate record](https://www.researchgate.net/publication/11090643_Normal_angiographic_tapering_of_the_coronary_arteries)
- **Seiler et al. (angiography).** Lumen area scales with summed distal branch length and myocardial mass. In CAD
  the lumen is diffusely 30–50% too small for the distal bed. **[Abs]** [Synapse record](https://synapsesocial.com/papers/W1967018012)
- **Zhou, Kassab & Molloi.**
  - 1999: diameter–length and volume–length design rules (Phys Med Biol 44:2929).
  - 2002: in-vivo validation and application to diffuse disease.
  - **Huo/Kassab, Radiology 2013:** CT length–volume scaling as a signature of a normal tree; deviation
    indicates diffuse CAD.
  - These treat altered taper or calibre as a *diagnostic marker of existing* diffuse disease.
  - Exponents not verified. **[Sec/Abs]**
  - [Wright State record](https://corescholar.libraries.wright.edu/cse/309)
- **FFR-CT.**
  - Physiological taper can push distal FFR-CT below 0.8 (false positives). A gradual decline without a focal
    lesion may instead reflect diffuse atherosclerosis.
  - In 443 RCAs, volume/length was the strongest predictor of distal FFR-CT.
  - **[Abs]** [Eur Radiol 2023](https://link.springer.com/article/10.1007/s00330-023-09972-8); [RadioGraphics FFR-CT](https://pubs.rsna.org/doi/full/10.1148/rg.210097)
- **TAG** (transluminal attenuation gradient).
  - Validation studies conflict because TAG "may be affected by changes in coronary luminal diameter". Taper is
    therefore a confounder of TAG, not an exposure.
  - **[Sec]** [Current Medical Imaging](https://www.eurekaselect.com/217199/article)
- **Ihdayhid 2021** (JCCT, ethnic differences in coronary anatomy, LV mass and FFR-CT).
  - Already in the bib. Its taper or volume findings were not read in this session. **[not opened]**
  - [DOI 10.1016/j.jcct.2020.09.004](https://doi.org/10.1016/j.jcct.2020.09.004)
- **Glagov 1987** (NEJM, 136 autopsy LMs).
  - Positive remodelling keeps the lumen until plaque reaches about 40% of the internal elastic lamina (IEL) area.
  - Early plaque therefore changes outer-wall taper more than lumen taper; later plaque narrows the lumen.
  - **[Sec]** [DOI 10.1056/NEJM198705283162204](https://doi.org/10.1056/NEJM198705283162204)
- **WSS link.** A taper raises velocity and WSS downstream in idealised CFD (see `Taper and curvature interaction
  for WSS/cfd_mechanics.md`). Garcha 2025 varied structure, including diameters, in synthetic trees. No clinical
  WSS–taper–plaque study was found. **[Abs]** [Garcha 2025](https://www.arxiv.org/abs/2507.17109)
- A large 2022 review of coronary geometry and plaque on CCTA does not discuss taper at all. **[FT, prior notes]**
  [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)

### Inferences
- **The disagreement for taper is an absence of evidence plus a direction problem.** Steeper or reversed taper in
  diseased arteries is mostly produced by plaque (focal narrowing, remodelling bulges, diffuse undersizing). Only a
  plaque-free baseline (as in CGPS) can measure taper as a predictor.
- Positive remodelling means the lumen taper of an early-plaque segment can look normal (Glagov). Lumen-based
  taper is therefore insensitive to early disease, which helps the plaque-free premise but limits interpretation.
- Representative for the table: **Javier/Mintz 1995** (IVUS taper partly from plaque) and the
  **Zhou/Kassab/Huo** scaling work (taper or calibre deviation as a marker of diffuse disease).

### Gaps
- No study of taper in diseased vs normal segments with a plaque endpoint and effect sizes was located.
- The Zhou–Kassab exponents and the Ihdayhid TAG/taper details were not verified.

## Q3. LM bifurcation angle: does a wide angle consistently associate with plaque, and which angle?

### Takeaway
Most small, referred, cross-sectional CCTA studies find a wider **angle B (LAD–LCx)** with LM or proximal left
stenosis or plaque. Typical differences are about 10–30°, and the proposed cut-offs scatter (60°, 78°, 80°).
Exceptions:
- angles A and C (LM–daughter) are reported less often and less consistently;
- a CAC study is null (Eur J Anat 2024);
- IVUS shows similar plaque at very different angles (Yakushiji);
- SYNTAX found no outcome effect.

The one "longitudinal" study (Tommasino 2024) has a diseased baseline, a 1-year follow-up and internally
inconsistent statistics. In a normal CACS-0 atlas, the angle varies strongly with sex (+10° in men) and with a
ramus (+14°). Both of these confound diseased vs normal comparisons.

### Cited Findings
- **Cui 2017** (PLoS ONE 12:e0174352).
  - Cohort: n=106 suspected CAD, dual-source CT plus ICA within 3 months; 318 angles in 126 vessels.
  - The LAD–LCx angle independently predicted significant (≥50%) left stenosis: OR 1.423, P=0.002; sensitivity
    66.7%, specificity 78.4%.
  - The angle was wider with non-calcified than calcified plaque.
  - The thesis claim that LM–daughter angles did *not* differ was **not re-verified** in this session.
  - A review attributes a 78° cut-off to Cui, and gives 68.3 ± 18.0° (<50%) vs 80.0 ± 19.2° (>70%).
  - **[Abs/Sec]** [DOAJ record](https://doaj.org/article/c8e3cc4c1f524184ae58922437f34efe); [scoping review PMC9385039](https://pmc.ncbi.nlm.nih.gov/articles/PMC9385039/)
- **Juan 2017** (Sci Rep; Chang Gung).
  - Cohort: n=313 CTA; 40 normal, 211 non-significant, 62 significant (the group labels differ between the
    abstract and the PMC text).
  - Angle B 75.5 ± 14.7° without vs 87.3 ± 18.8° with LM disease; cut-off 80°.
  - Male sex, hypertension and BMI also differed across groups: confounded.
  - **[FT/Sec, prior notes]** [DOI 10.1038/s41598-017-01679-3](https://pmc.ncbi.nlm.nih.gov/articles/PMC5431433/)
- **Temov & Sun 2016** (Int J Cardiovasc Imaging).
  - Cohort: n=196 CCTA. Angle B 79.40 ± 22.97°, range 35.5–178°.
  - Male sex RR 2.07 and BMI >25 RR 2.54 for B >80°; univariable.
  - The title is about *risk factors*, not plaque. This 2016 IJCI paper may be what was meant by
    "Rodriguez-Granillo 2016"; see Gaps.
  - **[Abs/Sec]** [DOI 10.1007/s10554-016-0884-2](https://espace.curtin.edu.au/handle/20.500.11937/4621?show=full)
- **Sun & Cao (Eur J Radiol 2011 / earlier small CT studies).**
  - 76.5 ± 15.9° (normal) vs 94.3 ± 16.5° (diseased).
  - In about 30 patients: 89.1 ± 13.1° vs 75.5 ± 19.8°.
  - 2D and volume-rendered measurement. **[Sec]** [PMC3888717](https://pmc.ncbi.nlm.nih.gov/articles/PMC3888717/); [OSTI](https://www.osti.gov/etdeweb/biblio/21584714)
- **Rodriguez-Granillo 2007** (Int J Cardiovasc Imaging 23:389).
  - Cohort: n=50, 40-row CT.
  - Plaque sat at the ostial LAD opposite the flow divider; the angle was "closely linked" to plaque in the
    bifurcation.
  - **[Sec]** [DOI 10.1007/s10554-006-9144-1](https://link.springer.com/doi/10.1007/s10554-006-9144-1)
- **Tommasino 2024, CLAP score** (J Cardiovasc Dev Dis 11:338).
  - Cohort: single-centre registry described as both observational and retrospective. 499 of 650 screened;
    320 with follow-up imaging; external validation n=200.
  - Definition: angle formed by the LM, proximal LAD and proximal LCx, measured on 2D and 3D CCTA (GE Volume
    Viewer); the cardiac phase is not stated. CCTA vs 3D-QCA mean difference −0.25°.
  - LMBA: 106.4 ± 29.4° with vs 74.7 ± 27.2° without significant (≥70%) proximal LAD stenosis.
  - LMBA >80°: MACE HR 4.47 (3.80–6.70); proximal LAD progression HR 5.325 (4.029–6.701); severe stenosis
    OR 3.234.
  - Follow-up about 374 days. Baseline plaque present.
  - Inconsistencies:
    - the MACE model is called Cox in the text but logistic in Table 2;
    - the CIs are asymmetric;
    - the stenosis denominators (160/499 vs 204/288) do not reconcile.
  - **[FT]** [DOI 10.3390/jcdd11110338](https://pmc.ncbi.nlm.nih.gov/articles/PMC11595042/)
- **Medrano-Gracia 2016 atlas** (EuroIntervention).
  - Cohort: n=300, CACS 0, no stenosis; 64% women.
  - Definition: angle B averaged over a 5–10 mm depth in a fitted bifurcation plane.
  - Overall about 80°. Men 85° vs women 74° (p<0.001, persists after height adjustment). With vs without ramus:
    89 ± 21° vs 75 ± 23°.
  - The atlas notes that earlier CT studies report larger angles and attributes the differences to methodology.
  - **[FT, prior notes]** [DOI 10.4244/EIJV12I7A139](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)
- **Gharleghi 2024** (arXiv; n=127 CCTA, no stenosis and zero calcium).
  - The Finet ratio, diameters and curvature, not explicitly the angle, independently correlated with adverse
    WSS. **[Pre]** [arXiv 2401.12504](https://arxiv.org/abs/2401.12504)
- **Null or contrary findings.**
  - Eur J Anat 2024: LAD–LCx angle not associated with CAC presence or severity; age and male sex were.
  - Yakushiji (IVUS): similar plaque distribution at about 51° and about 98° bifurcations.
  - SYNTAX (Girasis 2010): distal-angle tertiles did not predict 12-month MACCE after LM PCI.
  - **[Abs/Sec]** [Eur J Anat](https://eurjanat.com/articles/assessment-of-the-left-coronary-artery-bifurcation-angle-as-a-coronary-artery-disease-risk-factor-and-its-impact-on-coronary-artery-calcification/); [EUR repository](https://repub.eur.nl/pub/28713)
- **Angle A and C go the other way.**
  - Moon 2023 (QIMS, n=133): the LM–LAD angle in the flow convention was *larger* with ≥50% proximal LAD stenosis
    (38.3° vs 29.2°). It was predictive only combined with tortuosity.
  - CKD study: a *narrower* angle A was linked to more calcification.
  - Girasis: proximal and distal angles are inversely correlated (r = −0.75).
  - **[FT/Sec]** [PMC10644144](https://pmc.ncbi.nlm.nih.gov/articles/PMC10644144); [PLoS One 2018](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0198566)
- **Definitions.**
  - A = LM–LCx (proximal), B = LAD–LCx (distal), C = LM–LAD (main vessel); EBC and Bif-ARC.
  - A and C are reported either as obtuse angles (about 120–145°) or in the flow convention (180° minus that,
    about 35–60°). Studies mixing conventions cannot be compared directly.
  - Phase changes the angle by a mean absolute of about 6–7° per person (Handran, n=44).
  - [Bif-ARC](https://eurointervention.pcronline.com/article/definitions-and-standardized-endpoints-for-treatment-of-coronary-bifurcations); [Handran](https://www.hmpgloballearningnetwork.com/site/jic/articles/left-main-bifurcation-angle-and-changes-throughout-cardiac-cycle-quantitative-implications-left-main-bifurcation-stenting-and-stents)
- **WSS link.**
  - A wider angle → a larger low-WSS region at the lateral walls (CFD consensus).
  - Garcha 2025: the angle effect on adverse haemodynamics is *amplified or modulated* by the diameter ratio, so
    the angle alone is an incomplete proxy.
  - **[Abs]** [Garcha 2025](https://www.arxiv.org/abs/2507.17109); [PMC10512047](https://pmc.ncbi.nlm.nih.gov/articles/PMC10512047)

### Inferences
- **The positive angle B–stenosis association is fairly consistent in referred CCTA.** It is vulnerable to:
  - confounding by sex and BMI, both of which widen B and go with CAD;
  - reverse causation: LM or ostial plaque and remodelling can push the branches apart;
  - endpoint choice: stenosis ≥50% or ≥70% versus CAC (null).
- **Angles A and C are underused, and their signs depend on convention.** That is likely why studies such as Cui
  find "only B differs". A and C are geometrically coupled to B, so an apparent "A null, B positive" result can
  arise from angle-pair arithmetic.
- **The cut-offs (60°, 78°, 80°) are cohort-specific.** The normal SD is about 20–23° (range 25–180°), so a single
  threshold cannot generalise.
- Representative for the table: **Juan 2017** (or **Cui 2017**) for the cross-sectional positive B association;
  **Medrano-Gracia 2016** for normal variation and confounding by sex/ramus. Cite **Tommasino 2024** only with its
  caveats.

### Gaps
- **"Rodriguez-Granillo 2016" was not located.** The 2016 IJCI paper on LM angle and risk factors in the bib is
  Temov & Sun (DOI 10.1007/s10554-016-0884-2); Rodriguez-Granillo's located paper is from 2007. Check the
  citation.
- **"Bekircavusoglu 2026" was not found** in any search. Verify that it exists before citing it.
- **"Gharleghi 2024 left main (ASOCA/atlas)":** only arXiv 2401.12504 was located. Check whether a peer-reviewed
  version exists.
- No study tests the angle on a plaque-free baseline against incident plaque.

## Q4. LM→LAD and LM→LCx diameter ratios (Murray / Finet / Huo–Kassab): does deviation link to plaque or WSS?

### Takeaway
The "law" itself is disputed. Murray's exponent of 3 fits human epicardial coronaries poorly:
- the pooled meta-analytic exponent is 2.39 (95% CI 2.24–2.54) with I² = 99%;
- the normal CTA atlas fit is 2.4;
- Huo–Kassab's 7/3 fits all branch ratios;
- Finet's 0.678 holds only for near-symmetric bifurcations (Ds/Dl ≥ 0.75).

Clinical links between deviation and plaque are few and cross-sectional:
- IVUS: deviation goes with more calcium (Schoenenberger 2012);
- CTA: CAD trees deviate more (Chen 2020);
- Finet-based reference diameters unmask diffuse LM disease (Motreff 2010).

These cannot separate cause from effect, because diffuse plaque itself shrinks the LM. The WSS link is mainly
computational: Garcha 2025 (synthetic trees), and Gharleghi 2024, where the Finet ratio correlated with adverse
WSS [Pre]. Schrauwen 2016 uses scaling laws only to set CFD boundary conditions; it does not link ratio deviation
to plaque.

### Cited Findings
- **Taylor et al. 2024** (Am J Physiol Heart Circ Physiol).
  - Pooled flow–diameter exponent across epicardial and transmural arteries: 2.39 (2.24–2.54), I² = 99%.
  - The authors call it close to 7/3.
  - **[Abs]** [DOI 10.1152/ajpheart.00142.2024](https://pubmed.ncbi.nlm.nih.gov/38787386/)
- **Huo & Kassab 2012** (J R Soc Interface 9:190). The 7/3 law, minimum energy, mainly validated in swine casts.
  **[FT, prior notes]** [DOI 10.1098/rsif.2011.0270](https://pmc.ncbi.nlm.nih.gov/articles/PMC3223633)
- **Huo, Finet et al.** (EuroIntervention 2012).
  - HK agrees for all Ds/Dl ratios.
  - Murray and area preservation agree only for Ds/Dl ≤ 0.25.
  - Finet is "in gross error" below 0.75.
  - **[FT, prior notes]** [EuroIntervention](https://eurointervention.pcronline.com/article/optimal-diameter-of-diseased-bifurcation-segment-a-practical-rule-for-percutaneous-coronary-intervention)
- **Finet 2008** (EuroIntervention 3:490).
  - Cohort: QCA plus IVUS in angiographically normal coronaries. The sample is described inconsistently: 47 vs
    59 patients, 173 bifurcations.
  - Dm/(Dd1+Dd2) = 0.678; IVUS 0.668 ± 0.028.
  - **[FT, prior notes]** [DOI 10.4244/EIJV3I4A87](https://eurointervention.pcronline.com/article/fractal-geometry-of-arterial-coronary-bifurcations-a-quantitative-coronary-angiography-and-intravascular-ultrasound-analysis)
- **Medrano-Gracia 2016 atlas.**
  - Finet ratio 0.6576 ± 0.083; best exponent α = 2.4.
  - The LM-specific mean diameters (3.5/3.2/3.0 mm) imply LM/LAD of only about 1.09, because the LM was averaged
    along its length. This shows that the measurement definition moves the ratios more than the choice of law.
  - **[FT, prior notes]** [atlas](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)
- **Schoenenberger 2012** (Atherosclerosis 221:124; IVUS).
  - A higher Murray-deviation ratio went with more dense calcium proximal (F = 5.93, p = 0.016) and distal
    (F = 5.16, p = 0.024) to bifurcations, after adjustment for risk factors.
  - Cross-sectional, referred. **[Abs]** [DOI 10.1016/j.atherosclerosis.2011.12.040](https://www.ncbi.nlm.nih.gov/pubmed/22261173)
- **Chen 2020** (Comput Methods Biomech Biomed Eng; CTA). Bifurcations with CAD deviate further from optimal
  structure; left CAD trees deviate most. **[Abs]** [record](https://ideas.repec.org/a/taf/gcmbxx/v24y2020i7p740-752.html)
- **Motreff 2010** (EuroIntervention 5:709; n=52, QCA plus IVUS).
  - 10 of 38 angiographically normal LMs had diffuse IVUS disease.
  - Finet-based reference stenosis was 31% vs 4% by conventional QCA.
  - Ratio deviation here is a *consequence* of disease. **[FT, prior notes]** [Motreff](https://eurointervention.pcronline.com/article/diffuse-atherosclerotic-left-main-coronary-artery-disease-unmasked-by-fractal-geometric-law-applied-to-quantitative-coronary-angiography-an-angiographic-and-intravascular-ultrasound-study/pdf)
- **Schrauwen 2016** (Am J Physiol Heart Circ Physiol 310:H1304).
  - Cohort: 8 patients with mildly diseased bifurcations.
  - Diameter-based scaling laws can replace Doppler boundary conditions for *normalised* WSS, but absolute WSS
    needs caution.
  - **No plaque endpoint and no ratio-deviation analysis.** **[Abs]** [Amsterdam UMC record](https://pure.amsterdamumc.nl/en/publications/the-impact-of-scaled-boundary-conditions-on-wall-shear-stress-com/)
- **Garcha & Grande Gutiérrez 2025** (Sci Rep).
  - Design: 230 synthetic left coronary models.
  - "the diameter ratio between left coronary branches plays a substantial role in generating adverse hemodynamic
    phenotypes". It amplifies the angle, bifurcation-position and tortuosity effects.
  - Computational only; whether it discusses Murray's law was not confirmed. **[Abs]**
  - [DOI 10.1038/s41598-025-85781-x](https://www.arxiv.org/abs/2507.17109)
- **Gharleghi 2024.** In 127 plaque-free CCTA, the Finet ratio was among the features independently correlated
  with adverse WSS. **[Pre]** [arXiv 2401.12504](https://arxiv.org/abs/2401.12504)

### Inferences
- **There is no consensus on the reference law.** Its validity also depends on the branch ratio, so "deviation
  from Murray" changes meaning between studies that use exponent 3, 7/3, 2.4 or Finet's linear rule.
- **The ratio definition is a second, larger source of disagreement.** Near-carina vs length-averaged diameters,
  area-equivalent vs minimum diameter, and QCA (underestimates IVUS by 4–5.5%) all change the ratio.
- **Clinical associations run from disease to geometry** (diffuse LM undersizing, calcium). Only a plaque-free
  baseline can test ratio as a predictor.
- Representative for the table: **Taylor 2024** (which law) and **Schoenenberger 2012** (deviation ↔ calcium).
  For the WSS column: **Garcha 2025** (computational).

### Gaps
- No study relates LM→LAD or LM→LCx ratio on a plaque-free baseline to incident plaque.
- Schoenenberger's exact deviation definition and effect sizes beyond F statistics were not read.
- The Taylor 2024 full text (exponents by modality and disease) was not retrieved.

## Q5. Common methodological reasons for the inconsistency (all five features)

### Takeaway
Six recurring reasons explain most of the disagreement:
- modality: 2D invasive angiography with foreshortening and overlap vs 3D CCTA;
- manual or visual vs automated measurement;
- feature definition: bend counts vs arc/chord vs mean curvature; angle conventions; ratio sampling sites;
- whole tree vs a single artery;
- endpoint: obstructive stenosis vs any plaque vs calcium vs ACS/MACE;
- selection: referred, symptomatic cohorts, which bring sex, referral and SCAD effects.

All designs are cross-sectional or short follow-up with diseased baselines. Glagov remodelling means early plaque
alters outer-wall geometry before lumen geometry, while later plaque alters the measured lumen geometry. Both
blur cause and effect in cross-sectional data.

### Cited Findings
- **Modality and definition.**
  - Tello Ayala 2026 is 2D angiography, RCA only. The authors note that the left system has "more frequent
    overlap and foreshortening"; segmentation succeeded in 78.7% of loops; arc/chord and the new score correlate
    at only r = 0.116. **[FT]** [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
  - The scoping review on bifurcation angles: 2D QCA suffers overlap and foreshortening, while 3D QCA and CCTA are
    more reproducible. **[FT, prior notes]** [PMC9385039](https://pmc.ncbi.nlm.nih.gov/articles/PMC9385039/)
- **Endpoint.**
  - Tortuosity is inverse to *obstructive* CAD but linked to ischaemia without obstructive CAD (Zebic Mihic
    2023/2024; Estrada 2022).
  - Curvature is positive for *any* plaque at segment level (Tuncay 2018).
  - Bifurcation angle is positive for stenosis (Juan, Cui) but null for CAC (Eur J Anat 2024).
  - Sources as cited above.
- **WSS direction depends on the endpoint.** Low WSS goes with growth and progression (PREDICTION; Stone);
  high WSS and axial plaque stress go with rupture sites (EMERALD). **[Abs, prior notes]** [PubMed 22723305](https://pubmed.ncbi.nlm.nih.gov/22723305/); [PMC8475759](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8475759/)
- **Remodelling.** Glagov 1987: the lumen is preserved until about 40% plaque burden. [DOI 10.1056/NEJM198705283162204](https://doi.org/10.1056/NEJM198705283162204)
- **Referral and sex.**
  - Chiha 2017: severe tortuosity in 45.2% of women vs 19.7% of men, with less CAD.
  - Eleid 2014: tortuosity 78% in SCAD.
  - Atlas: angle B is 11° wider in men.
  - Sources as cited above.
- **Cardiac phase.** Curvature changes by up to 0.18 mm⁻¹ over the cycle on the LAD (Gross 1996, biplane); the
  angle changes by about 7° (Handran). **[Abs, prior notes]** [Duke record](https://scholars.duke.edu/publication/684552)

### Inferences
- **Row structure for a summary table.** One row per feature with: definition used, modality, cohort
  (referred/normal/population), design, endpoint, sign, and the proposed explanation. The pattern that emerges:
  every human clinical study is cross-sectional or diseased-baseline; none is a population sample; none uses a
  plaque-free baseline with incident plaque of any grade as outcome. That is the gap the CGPS design fills.
- **Suggested 1–2 representative studies per feature:**

| Feature | Study (design, cohort, n) | Definition | Endpoint | Sign | Explanation offered |
|---|---|---|---|---|---|
| Curvature/tortuosity | Li 2011 (cross-sectional, referred, 1,010, ICA) | ≥3 bends ≥45° | CAD (stenosis) | − (OR 0.755) | Women more tortuous; possible protective flow |
| | Tello Ayala 2026 (cross-sectional, referred registry, 22,334, 2D ICA, RCA) | Mean turning angle (and arc/chord) | Any RCA stenosis | + (OR 1.05/SD); arc/chord − | Definition; the authors call for prospective work |
| Taper | Javier/Mintz 1995 (IVUS, diseased) | mm per 10 mm | Mechanism of taper | Taper partly *from* plaque | Reverse causation |
| | Zhou/Kassab/Huo scaling (angiography/CT) | Diameter/volume–length laws | Diffuse disease | Deviation = disease marker | Diffuse undersizing |
| LM angle | Juan 2017 (cross-sectional, referred, 313, CCTA) | Angle B | LM/left stenosis | + (75.5 vs 87.3°) | Low WSS at lateral walls; confounded by sex/BMI |
| | Medrano-Gracia 2016 (normal CACS-0 atlas, 300) | Angle B, 5–10 mm, 3D | none (normal variation) | Men +11°, ramus +14° | Anatomical confounders |
| Diameter ratios | Taylor 2024 (meta-analysis) | Flow–diameter exponent | none | 2.39, I² = 99% | Which law applies is unsettled |
| | Schoenenberger 2012 (IVUS, referred) | Murray-deviation ratio | Dense calcium | + | Suboptimal branching → disturbed WSS (or plaque alters D) |

### Gaps
- No population-based cohort and no plaque-free-baseline longitudinal study exists for any of the five features.
  This is stated as an absence after targeted searches, not proven.
- Several requested sources could not be located or opened: Sun 2019, Xie (clinical), Rodriguez-Granillo 2016,
  Bekircavusoglu 2026, and the full texts of Kahe 2020 and Ciurică 2019. Do not cite them until they have been
  checked.
