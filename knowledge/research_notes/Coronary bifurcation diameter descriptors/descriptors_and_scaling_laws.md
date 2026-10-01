# Coronary bifurcation diameter descriptors and scaling laws

Notation used throughout: D_p (or PMV) = proximal main vessel / parent / "mother"; D_1 (DMV) = larger daughter, usually the distal main vessel; D_2 (SB) = smaller daughter / side branch. Researcher: web research 2026-09-28, about 25 tool calls. Formulas marked "(inference)" are derived here algebraically and not quoted from a source.

## 1. The bifurcation diameter laws: formulas, derivation, and empirical fit in coronaries

### Takeaway
Four laws dominate: Murray (exponent 3), Huo-Kassab (HK, exponent 7/3), area preservation (exponent 2), and Finet's linear rule D_p = 0.678(D_1 + D_2). The best current synthesis (2024 meta-analysis, 18 studies) puts the pooled coronary flow-diameter exponent at 2.39 (95% CI 2.24-2.54), close to HK's 7/3 and clearly below Murray's 3. Which law "fits best" is metric-dependent, however: on normal CTA in the same Auckland group, one paper reports Finet best and another HK best, so no single law is settled.

### Cited Findings

**Murray's law (1926)**
- Formula: D_p^3 = D_1^3 + D_2^3, equivalently Q = k D^3. Derivation: diameters minimise total cost = viscous (Poiseuille) dissipation + metabolic cost of maintaining blood volume; consequence is constant wall shear stress throughout the tree. Assumes steady, laminar, Newtonian flow in rigid tubes. Uylings (1977) showed turbulent flow gives exponents from 2.33 to 3.0; morphometric coronary studies report exponents from 2.06 to 3.20. — [Taylor et al. 2022, Front Physiol 13:871912](https://doi.org/10.3389/fphys.2022.871912) ([open PDF](https://eprints.whiterose.ac.uk/id/eprint/185753/1/fphys-13-871912.pdf))
- Clinical legacy: the ≥6 mm² left main minimum lumen area threshold in guidelines was derived from Murray's law (de la Torre Hernández 2007/2011, as cited). — [Taylor et al. 2022](https://doi.org/10.3389/fphys.2022.871912)

**Generalised power law / junction exponent**
- D_p^x = D_1^x + D_2^x; x = 3 is Murray's optimum. x is usually solved iteratively and is biased in the presence of measurement noise. — [Witt et al. 2010, Artery Research / PMC2954284](https://pmc.ncbi.nlm.nih.gov/articles/PMC2954284/)

**Huo-Kassab (HK) law**
- D_p^(7/3) = D_1^(7/3) + D_2^(7/3); flow scales as Q ~ D^(7/3); flow split between daughters Q_1/Q_2 = (D_1/D_2)^(7/3). Generalises to trifurcations as D_p^(7/3) = D_1^(7/3) + D_2^(7/3) + D_3^(7/3) (relevant to LM trifurcation with ramus). — [Anatomy and function relation in the coronary tree, EuroIntervention](https://eurointervention.pcronline.com/article/anatomy-and-function-relation-in-the-coronary-tree-from-bifurcations-to-myocardial-flow-and-mass)
- Derivation base: Kassab's scaling laws from minimising construction (metabolic) plus operation (viscous) cost over the whole distal tree ("crown"), not a single segment. The diameter-flow exponent "is not necessarily equal to 3.0 as required by Murray's law but depends on the ratio of metabolic to viscous power dissipation." — [Kassab 2006, Am J Physiol Heart Circ Physiol 290:H894-H903](https://pubmed.ncbi.nlm.nih.gov/16143652) ([journal](https://journals.physiology.org/doi/full/10.1152/ajpheart.00579.2005))
- The EBC QCA consensus update lists Finet (2008) and the refined HK model (2012) as the reference-diameter rules; HK is described as derived from flow-diameter scaling laws plus mass conservation and "refined the Finet model". — [EBC QCA consensus update, EuroIntervention](https://eurointervention.pcronline.com/article/quantitative-angiography-methods-for-bifurcation-lesions-a-consensus-statement-update-from-the-european-bifurcation-club)
- Review claim: HK "accurately predicts all size diameters of the epicardial coronary bifurcation vessels whereas Murray's law and Finet's formula can only do so in certain size subsets"; Finet is nonetheless the most used clinically because of simplicity. — [Fundamentals of percutaneous coronary bifurcation interventions, World J Cardiol 2022 / PMC8968454](https://pmc.ncbi.nlm.nih.gov/articles/PMC8968454/)
- A secondary source states Finet's rule "violates mass conservation" (it is linear, not a power-law conservation). — [EuroIntervention review](https://eurointervention.pcronline.com/article/anatomy-and-function-relation-in-the-coronary-tree-from-bifurcations-to-myocardial-flow-and-mass)

**Finet's law (2008)**
- D_p = 0.678 (D_1 + D_2). Derived empirically from QCA of 173 bifurcations in 59 patients (mean age 46 ± 8.5) with normal angiograms, 27 with IVUS confirming normal vessels. Mean diameters: mother 3.33 ± 0.94 mm, major daughter 2.70 ± 0.77 mm, minor daughter 2.23 ± 0.68 mm. Ratio constant across scales (fractal self-similarity). Deviation of predictions: linear 0.678 rule 0.33%, Murray 5%, area conservation (exponent 2) 5.94%; Murray underestimates and flow (area) conservation overestimates D_p. — [Finet et al. 2008, EuroIntervention 3(4)](https://eurointervention.pcronline.com/article/fractal-geometry-of-arterial-coronary-bifurcations-a-quantitative-coronary-angiography-and-intravascular-ultrasound-analysis)
- Finet's rule has been shown to be a special case (linearisation) of a generalised Murray law (title-level evidence only; full text not read). — [ResearchGate: "Finet's Law as a Special Case of the Generalised Murray's Law"](https://www.researchgate.net/publication/336919153_Finet's_Law_as_a_Special_Case_of_the_Generalised_Murray's_Law)
- 2025 LM study (84 patients, 14 centres): Finet-adjusted bifurcation QCA did not improve correlation with iFR (%DS vs iFR r = -0.326 with Finet vs r = -0.402 standard Bif-QCA). — [Lunardi et al. 2025, Cardiol Res Pract / PMC12145935](https://pmc.ncbi.nlm.nih.gov/articles/PMC12145935)

**Area preservation / flow conservation (exponent 2)**
- D_p^2 = D_1^2 + D_2^2; corresponds to constant mean velocity through the tree. — [Taylor et al. 2022](https://doi.org/10.3389/fphys.2022.871912); compared in [Medrano-Gracia et al. 2017, PMC5323506](https://pmc.ncbi.nlm.nih.gov/articles/PMC5323506)

**Empirical fit: which law fits coronaries best**
- Meta-analysis (Taylor et al. 2024, AJP-Heart 327(1):H182-H190): 18 studies, 489 participants (372 humans in 9 studies; 244 animal coronary trees). Pooled exponent 2.39 (95% CI 2.24-2.54); humans 2.42 (2.17-2.67); animals 2.36 (2.17-2.55); epicardial 2.43 (2.25-2.61); transmural 2.21 (1.93-2.49). Heterogeneity I² = 99%. Diseased vs healthy: 2.29 vs 2.38, not significantly different. — [Taylor et al. 2024 / PMC11380967](https://pmc.ncbi.nlm.nih.gov/articles/PMC11380967/)
- Invasive physiology validation (Taylor et al. 2022): 27 arteries in 20 patients, angiography-derived 3D CFD vs Rayflow continuous thermodilution. The exponent best reproducing inlet flow was 2.15 (r = 0.47) and best reproducing microvascular resistance was 2.38 (r = 0.66); "not 3.0". — [Taylor et al. 2022](https://doi.org/10.3389/fphys.2022.871912)
- Normal CTA (Medrano-Gracia et al. 2017): 211 patients, zero calcium score, no stenoses, 446 bifurcations; diameters measured on luminal meshes cut by a 10 mm radius sphere centred at the bifurcation point. RMS error: HK 0.1650, area preservation 0.1685, Murray 0.1693, Finet 0.4564. Observed Finet ratio 0.6576 ± 0.083 (vs 0.678). — [Medrano-Gracia et al. 2017, "A Study of Coronary Bifurcation Shape in a Normal Population", PMC5323506](https://pmc.ncbi.nlm.nih.gov/articles/PMC5323506)
- Contradiction: the companion atlas paper (300 adults, zero CAC, no stenoses, CTA) reports bifurcations "obey the Finet diameter model and angle rule much more than HK and Murray's model". — [Medrano-Gracia et al. 2016, "A computational atlas of normal coronary artery anatomy", EuroIntervention](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy); contradicted by [Medrano-Gracia 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5323506)
- Swine casts: volume-diameter power relation exponents 2.96 (LAD), 3.00 (LCx), 2.98 (RCA), all r² = 0.999, vs theoretical 3 (this is a crown volume-stem diameter law, not the junction exponent). — [Huo & Kassab 2012, J R Soc Interface 9:190-200](https://pubmed.ncbi.nlm.nih.gov/21676970/)

### Inferences
- For a CTA pipeline, HK (7/3) and area preservation (2) are nearly indistinguishable in RMS on normal CTA (0.1650 vs 0.1685), so choosing a "best law" from CT diameters alone is not well posed; measurement protocol (distance from the bifurcation point, max inscribed sphere vs area-equivalent diameter) likely dominates law choice.
- Finet is linear, so it is well defined for every bifurcation and error behaves smoothly, which fits the earlier ImageCAS-X observation that the Finet ratio is the most reproducible (ICC 0.85-0.90 at LM). The crux failure (ICC 0.44) is consistent with the 2017 PCA finding that the RCA crux is a geometrically distinct cluster (curvature mode).
- Finet ratio and a junction exponent are algebraically linked for a given asymmetry; reporting the Finet ratio plus the daughter ratio carries the same information as the exponent without the solvability problem (inference).

### Gaps
- The original Huo & Kassab HK derivation paper (J Biomech 2012 "Which diameter and angle rule provides optimal flow patterns in a coronary bifurcation?") and Kassab 2006 full text were paywalled (403); exact derivation algebra for 7/3 not verified here.
- No CT-based study found that reports junction-exponent distributions per named junction (LM, LAD/D1, LCx/OM1, crux) in a population cohort.

## 2. Kassab tree-level scaling laws (diameter-length, length-volume, volume-flow)

### Takeaway
Kassab's laws relate a stem segment to its whole downstream crown (cumulative length L_c, volume V_c, flow Q_s, diameter D_s). They are tree descriptors rather than single-junction descriptors, and the length-volume coefficient (not exponent) was proposed as a CT index of diffuse CAD.

### Cited Findings
- Kassab 2006: all vascular trees with morphometric data (coronary, pulmonary, skeletal muscle, mesentery, omentum, conjunctiva) obey three scaling relations: crown length vs crown volume, stem diameter vs stem flow, and stem diameter vs crown length; justified by minimisation of construction plus operation cost. Reported exponents per search summary: diameter-length 3/7, volume-length about 2/7 (secondary summary, not verified from full text). — [Kassab 2006, AJP-Heart](https://pubmed.ncbi.nlm.nih.gov/16143652)
- CT application (Huo, Wischgoll, Choy, ... Bhatt, Kassab, Radiology 2013;268(3):694-701): 120 subjects (89 metabolic syndrome, 31 matched controls), dual-source CTA. Length-volume law written as V_c = K_LV · L_c^(7/9) with K_LV in cm^(-4/3); length-area law A_s = K_LA · L_c^(7/6). K_LV = 26.6 cm^(-4/3) (R² = 0.85) in metabolic syndrome vs 19.9 (R² = 0.88) in controls; threshold K_LV ≥ 23 flagged diffuse CAD in about 65% of patients and stayed below threshold in about 90% of controls. No AUC reported. Mean lumen CSA 0.039 vs 0.054 cm²; summed volume 2.71 vs 3.29 cm³. — [Huo et al. 2013 Radiology / PMC3750415](https://pmc.ncbi.nlm.nih.gov/articles/PMC3750415)
- The exponent is reported unchanged in diffuse disease; only the coefficient shifts. — [EuroIntervention review](https://eurointervention.pcronline.com/article/anatomy-and-function-relation-in-the-coronary-tree-from-bifurcations-to-myocardial-flow-and-mass)
- Companion CT paper: diffuse compensatory enlargement (positive remodelling) also detectable via scaling-law coefficients. — [Huo et al. 2013, J R Soc Interface 10:20121015 (PubMed 23365197)](https://pubmed.ncbi.nlm.nih.gov/23365197/)
- Mouse growth/ageing: length-volume exponent 3/4 constant with age, coefficient K changes with age (growth then ageing increase). — [Growth, ageing and scaling laws of coronary arterial trees, PMC4707856](https://pmc.ncbi.nlm.nih.gov/articles/PMC4707856)
- Myocardial mass link: M ∝ D^(8/3); fraction of main-artery territory supplied by a side branch = (D_SB/D_MA)^(8/3) × 100. — [EuroIntervention review](https://eurointervention.pcronline.com/article/anatomy-and-function-relation-in-the-coronary-tree-from-bifurcations-to-myocardial-flow-and-mass)

### Inferences
- Crown-level laws depend on how completely the tree is segmented (distal truncation changes L_c and V_c), so K_LV computed on automatic CTA segmentations will be resolution- and model-dependent; it needs harmonisation before transfer from ImageCAS-X to CGPS.
- The exponent notation differs between sources (3/4 in mouse paper, 7/9 in Radiology form); these are different parametrisations of the same family and should be quoted from the exact paper used.

### Gaps
- Sensitivity/specificity with confidence intervals and any outcome-linked (event) validation of K_LV were not found.

## 3. Ratio descriptors: area ratio, daughter ratio, step-down ratios, optimality ratio

### Takeaway
Simple ratios avoid the solvability problem of the junction exponent. The retinal literature's "optimality ratio" was designed precisely because the junction exponent is noise-biased and often not computable; it is a direct replacement candidate for the 12-37% unsolvable Murray exponents seen on ImageCAS-X.

### Cited Findings
- Optimality ratio: Γ = ((d_1^3 + d_2^3) / 2)^(1/3) / d_0 [written in source as (d1³+d2³)/(2d0³))^(1/3)]; optimal value for a Murray bifurcation 2^(-1/3) = 0.7937. Optimality deviation Γ_dev = |Γ - 2^(-1/3)|. Asymmetry factor α = (d_1/d_2)^2 (as extracted). At 10% measurement noise the optimality-ratio bias was under one sixth of junction-exponent bias. Healthy values 0.784-0.795; ratio rose significantly (p = 0.03) under NO-synthase inhibition (L-NMMA), i.e. it is sensitive to endothelial function. — [Witt et al. 2010, PMC2954284](https://pmc.ncbi.nlm.nih.gov/articles/PMC2954284/)
- Area ratio / branching coefficient: BC = (d_1^2 + d_2^2) / d_0^2. Knudtson's constant retinal arteriolar BC is 1.28; Patton proposed an asymmetry-dependent BC = 0.78 + 0.63·AI. — [ScienceDirect: Reliable monitoring system for AVR computation](https://www.sciencedirect.com/science/article/abs/pii/S0895611113001481)
- Finet ratio as a descriptor: D_p / (D_1 + D_2); normal CTA mean 0.6576 ± 0.083 ([Medrano-Gracia 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5323506)); Finet's QCA reference 0.678 ([Finet 2008](https://eurointervention.pcronline.com/article/fractal-geometry-of-arterial-coronary-bifurcations-a-quantitative-coronary-angiography-and-intravascular-ultrasound-analysis)).
- Step-down ratios from Finet's normal QCA means: D_1/D_p = 2.70/3.33 = 0.81, D_2/D_p = 2.23/3.33 = 0.67, D_2/D_1 = 0.83 (computed here from [Finet 2008](https://eurointervention.pcronline.com/article/fractal-geometry-of-arterial-coronary-bifurcations-a-quantitative-coronary-angiography-and-intravascular-ultrasound-analysis) means; ratio of means, not mean of ratios).
- LM normal size: CTA atlas 3.5 ± 0.8 mm diameter, 10.5 ± 5.3 mm length (300 normal adults) — [Medrano-Gracia 2016](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy); review gives 3.5-6.5 mm range, mean 4.75-5 mm (source not stated, likely angiographic/autopsy) — [PMC8968454](https://pmc.ncbi.nlm.nih.gov/articles/PMC8968454/). These disagree by >1 mm; the CT atlas value is the relevant reference for CTA.
- Sex effect on size: male scaling factor 0.999 ± 0.087 vs female 0.940 ± 0.072; hypertension, smoking, diabetes not associated with shape parameters in the normal CT cohort. — [Medrano-Gracia 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5323506)

### Inferences
- Junction exponent solvability (inference, algebra): f(x) = (d_1/d_0)^x + (d_2/d_0)^x - 1 is monotone decreasing in x when both daughters are smaller than the parent, so a unique positive root exists iff d_0 > max(d_1, d_2) and d_0 < d_1 + d_2 gives x > 1. No positive root exists when a daughter is at least as large as the parent, which is common when the parent diameter is sampled inside a stenosis, too close to the flaring core, or when the "main" daughter is actually the continuation with near-equal diameter (LM with ectatic LAD, RCA crux). This explains the 12-37% unsolvable rate and argues for the optimality ratio or Finet ratio as primary descriptors.
- Because diameters are highly correlated with body size and sex, dimensionless ratios (Finet ratio, D_2/D_1, Γ) are better candidates for cohort outcome models than absolute diameters.

### Gaps
- No reported population normal ranges of the optimality ratio for coronary arteries were found; it has only been used in retina.

## 4. Deviations from the laws and disease

### Takeaway
Evidence that law-deviation predicts disease is modest and mostly cross-sectional: an IVUS study linking high Murray ratio to calcified bifurcation plaque, CT scaling coefficients separating metabolic syndrome from controls, and retinal/cerebral analogues. No prospective outcome study of coronary bifurcation law deviation in healthy people was found.

### Cited Findings
- Schoenenberger et al. 2012 (Atherosclerosis): 253 patients, IVUS virtual histology proximal and distal to side-branch bifurcations; high Murray ratio associated with more dense calcium and less fibrous and fibro-fatty tissue; if Murray is obeyed, shear stress is constant across the bifurcation, so deviation may explain plaque-prone bifurcations. — [PubMed 22261173](https://pubmed.ncbi.nlm.nih.gov/22261173/)
- Link between deviation from Murray's law and low WSS regions in the left coronary artery (CFD study, J Theor Biol). — [ScienceDirect S0022519316300728](https://www.sciencedirect.com/science/article/abs/pii/S0022519316300728) (abstract not read in detail)
- Serial CTA study: ESS computed in models including daughter branches with Murray-based flow split predicted plaque evolution better than main-vessel-only models. — [EuroIntervention, serial CTA study (PubMed 28606882)](https://pubmed.ncbi.nlm.nih.gov/28606882/)
- Diffuse CAD by CT scaling-law coefficient K_LV ≥ 23 cm^(-4/3). — [Huo et al. 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3750415)
- Meta-analysis found no significant exponent difference between diseased and healthy coronaries (2.29 vs 2.38). — [Taylor et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11380967/)
- Retina: optimality ratio rises under NO inhibition ([Witt 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2954284/)); normotensive bifurcation exponents are closer to 3 than hypertensive ones, and bifurcation angles are more acute in hypertension and decline with age ([Stanton et al. 1995, PubMed 8903640](https://pubmed.ncbi.nlm.nih.gov/8903640/), search-snippet level).
- Cerebral: MCA junction exponent 2.9 ± 1.2 (Rossitti & Löfgren), significantly lower at distal ICA; deviation from optimal calibre at MCA bifurcations is associated with aneurysms, though in one case-control analysis only branch angles independently predicted aneurysm presence. — [PMC4185287](https://pmc.ncbi.nlm.nih.gov/articles/PMC4185287/); [BMC Neurol, PMC8830006](https://pmc.ncbi.nlm.nih.gov/articles/PMC8830006/)

### Inferences
- The disease-vs-healthy exponent null (meta-analysis) plus I² = 99% suggests junction-level law deviation is a noisy per-person marker; a crown-level coefficient or a robust ratio aggregated over several junctions is more plausible as a risk feature for a 10-year outcome model.
- Direction matters: Schoenenberger's "high Murray ratio" means a parent that is large relative to daughters (positive remodelling or daughter narrowing); a signed deviation should be kept, not only its magnitude.

### Gaps
- No prospective study linking coronary bifurcation diameter-law deviation in healthy trees to incident events was found.
- The exact definition of "Murray ratio" in Schoenenberger 2012 was not retrieved (abstract only).

## 5. Local diameter profile across the junction: POC, flaring, carina, proximal/distal ratios

### Takeaway
The bifurcation core is formally defined by the EBC as the polygon of confluence (POC) with a point of bifurcation (POB) at the centre of the largest sphere touching all three contours. Diameters must be sampled outside it, which is why segment-based reference diameters (5 mm segments) are standard. Quantitative normal data on core flaring and post-bifurcation narrowing is scarce.

### Cited Findings
- EBC definitions: POB = where centrelines meet, the mid-point of the largest circle/sphere touching all three contours; POC = central bifurcation region that behaves differently from single-vessel analysis. Six-segment model: PMV, DMV, SB, plus 5 mm segments proximal to the bifurcation and 5 mm distal in the main vessel and side branch; eleven-segment model adds 3 mm SB ostial segments. Single-vessel QCA underestimates RVD in the PMV and overestimates in DMV and SB, the reason dedicated bifurcation analysis is recommended. — [EBC QCA consensus update](https://eurointervention.pcronline.com/article/quantitative-angiography-methods-for-bifurcation-lesions-a-consensus-statement-update-from-the-european-bifurcation-club)
- Review defines POC as the area between PMV, DMV and SB bounded by lines drawn across the branch ostia; the carina is the flow divider. — [PMC8968454](https://pmc.ncbi.nlm.nih.gov/articles/PMC8968454/)
- Angles (3D QCA, Tu et al. 2012, via EBC): proximal angle A: LAD/D 151 ± 13°, LCx/OM 146 ± 18°, PDA/PL 145 ± 19°, LM 128 ± 24°; distal angle B: LAD/D 48 ± 16°, LCx/OM 57 ± 16°, PDA/PL 59 ± 17°, LM 80 ± 21°. CTA: LM angle B 89 ± 21° with ramus vs 75 ± 23° without. — [EBC consensus](https://eurointervention.pcronline.com/article/quantitative-angiography-methods-for-bifurcation-lesions-a-consensus-statement-update-from-the-european-bifurcation-club); [Medrano-Gracia 2016](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)
- CT shape PCA of 446 normal bifurcations: 3 modes explain 71% of variance; PC1 (43%) angle B, PC2 angle ratios, PC3 curvature, with the RCA crux separating on curvature. — [Medrano-Gracia 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5323506)

### Inferences
- For automatic CTA extraction, a reproducible protocol is: locate POB as the maximal inscribed sphere touching all three branches, then sample reference diameters in a window beginning beyond the POC (e.g. 1 POB-sphere radius or a fixed 2-5 mm downstream) and average over a 5 mm segment; this mirrors the EBC six-segment model and avoids the flaring core that inflates D_p or D_daughters. The 10 mm sphere cut in the CT atlas is another published convention.
- Proximal-to-distal main vessel ratio (D_PMV/D_DMV) and core flaring index (POB sphere diameter / D_PMV) are natural descriptors but I found no published normal ranges for them in CTA.

### Gaps
- No quantitative normal values for bifurcation-core flaring or post-bifurcation narrowing (e.g. SB ostial vs 5 mm distal diameter) in healthy CTA were found.
- Carina geometry descriptors (carina tip angle, carina shift) with diameter coupling were not covered by sources read.

## 6. Cross-domain analogues: retina, cerebral, airway

### Takeaway
The retinal summary calibres (CRAE/CRVE by the revised Knudtson formula) are by far the most validated diameter descriptors against outcomes, with large pooled cohorts. They are built on a fixed branching coefficient, i.e. an implicit square-law bifurcation model, which is the direct analogue of a Finet-like constant ratio.

### Cited Findings
- Knudtson revised formula (2003, Curr Eye Res 27:143): uses the 6 largest arterioles and 6 largest venules, iteratively combining largest with smallest; branching coefficients 0.88 for arterioles and 0.95 for venules (i.e. W = 0.88·(w_1² + w_2²)^(1/2) for arterioles, 0.95·(...)^(1/2) for venules). Developed on 44 normotensive, non-diabetic young adults; correlation with Parr-Hubbard 0.94-0.98; more robust to vessel count and independent of image scale. — [ScienceDirect AVR paper (coefficients)](https://www.sciencedirect.com/science/article/abs/pii/S0895611113001481); [Knudtson et al. 2003, Curr Eye Res](https://www.tandfonline.com/doi/abs/10.1076/ceyr.27.3.143.16049); [Heitmar 2015 comparison](https://onlinelibrary.wiley.com/doi/10.1097/OPX.0000000000000704)
- Constant-BC 1.28 (arterioles; 1/0.88² ≈ 1.29) vs Patton's asymmetry-dependent BC = 0.78 + 0.63·AI. — [ScienceDirect AVR paper](https://www.sciencedirect.com/science/article/abs/pii/S0895611113001481)
- Outcome validation: individual-participant meta-analysis, 10,229 people free of hypertension, diabetes, CVD; 2,599 incident hypertension; narrower CRAE OR 1.29 (1.20-1.39) per 20 µm, wider CRVE OR 1.14 (1.06-1.23) per 20 µm. — [Ding et al. 2014, J Hypertens / PMC4120649](https://pmc.ncbi.nlm.nih.gov/articles/PMC4120649)
- Retinal junction exponent and optimality ratio: see section 3 ([Witt 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2954284/)).
- Airways: Weibel symmetric model with daughter/parent ratio (homothety ratio) 2^(-1/3) ≈ 0.79, the symmetric Hess-Murray optimum; measured homothety ratios 0.80-0.85 fit micro-CT terminal bronchioles, and ratios < 0.76 associated with peripheral shift of resistance (COPD). — [Homothety ratio in healthy and COPD, Respir Physiol Neurobiol](https://www.sciencedirect.com/science/article/abs/pii/S1569904813003522); [Optimal diameter reduction ratio of acinar airways, PMC6354962](https://pmc.ncbi.nlm.nih.gov/articles/PMC6354962)
- Cerebral: MCA junction exponent 2.9 ± 1.2 (see section 4).

### Inferences
- Validation ranking by outcome evidence: CRAE/CRVE (large pooled prospective cohorts) >> retinal junction exponent/optimality ratio (small physiological and cross-sectional studies) ≈ cerebral junction exponent (case-control aneurysm) > airway homothety ratio (disease physiology, not outcomes).
- A coronary analogue of CRAE, e.g. an "equivalent LM calibre" reconstructed from LAD and LCx via a fixed coefficient, would in effect be Finet's rule; comparing observed LM vs Finet-predicted LM is a coronary counterpart to the retinal summary approach.

### Gaps
- Knudtson's original paper was not opened; coefficients are from secondary sources that agree with each other.
- No study was found transferring the optimality ratio or CRAE-style summary directly to coronary CTA.
