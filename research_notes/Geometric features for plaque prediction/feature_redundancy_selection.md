# Redundancy, reliability and parsimonious selection of coronary geometric features for plaque prediction

Scope note: Herlev–Østerbro (CGPS) general-population CCTA cohort. Current candidate features: (1) bifurcation diameter ratio, (2) daughter-daughter bifurcation angle, (3) local turning angle along the centerline. Search budget was limited (about 18 tool calls); several primary papers were paywalled or behind captcha (PMC, nature.com), so some findings rest on abstracts or search-engine summaries and are flagged as such.

## Q1. Which geometric features explain variance in computed WSS, and how correlated are they?

### Takeaway
In the only large human CCTA-based CFD cohort found (127 left main bifurcations, Beier group, UNSW), a multivariable model of 11 shape features explained 79% of the variance in low-TAESS area, with Finet's ratio (a diameter-ratio measure) the dominant predictor, vessel diameters dominant for oscillatory shear, and curvature a secondary contributor. Bifurcation angle contributed but was not dominant. This directly supports keeping the diameter ratio, and suggests absolute lumen diameter is the most important feature missing from the current set.

### Cited Findings
- Gharleghi, Zhang, Shen, Webster, Ellis, Beier: 127 patients with suspected CAD but no significant stenosis (85 F, 42 M, median age 57), CTCA-segmented left main bifurcations, CFD (human-derived CFD evidence, not measured WSS). 11 anatomical features: mean curvature (LM, LAD, LCx), median diameter (LM, LAD, LCx), bifurcation angles A/B/C, inflow angle, Finet's ratio. — [arXiv 2401.12504](https://arxiv.org/html/2401.12504v1); published as [Sci Rep 2024](https://www.nature.com/articles/s41598-024-73490-w)
- Multiple regression R²: low TAESS 0.791; high OSI 0.633; high RRT 0.585; mean TSVI only about 0.36. — [arXiv 2401.12504](https://arxiv.org/html/2401.12504v1); [search summary of Sci Rep 2024](https://www.nature.com/articles/s41598-024-73490-w)
- Finet's ratio dominated low TAESS (p<0.001) and RRT; branch diameters dominated high OSI (all p<0.001); curvatures, angle A and BMI were secondary significant terms. The authors describe interdependent effects, e.g. a diameter-curvature interaction (women: smaller diameters but higher curvature). — [arXiv 2401.12504](https://arxiv.org/html/2401.12504v1)
- Follow-up from the same group on sex differences in LM anatomy and flow (IEEE TBME 2025). — [arXiv 2311.18489](https://arxiv.org/pdf/2311.18489); [EUR repository PDF](https://pure.eur.nl/ws/files/226833763/Sex-Specific_Variances_in_Anatomy_and_Blood_Flow_of_the_Left_Main_Coronary_Bifurcation_Implications_for_Coronary_Artery_Disease_Risk.pdf)
- Kashyap, Gharleghi, Li, McGrath-Cadell, Graham, Ellis, Webster, Beier (Sci Rep 2022): same 127-patient no-CAD CTCA cohort, CFD. Curvature-based tortuosity metrics correlated with % area TAWSS < 0.4 Pa; average absolute curvature had the highest coefficient of determination across all LM branches (p<0.001), then average squared-derivative curvature (p=0.001) and RMS curvature (p=0.002). The tortuosity index (arc/chord), the most used metric in the literature, was not significant (p=0.86). Authors recommend average absolute curvature. — [Victor Chang eprint, abstract](https://eprints.victorchang.edu.au/1198); [PMC8764056](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8764056/)
- Torsion acts on WSS mainly through helical flow: in patient-specific coronary CFD, vascular torsion was associated with helicity intensity (r=0.64, p<0.001) and adverse WSS was strongly inversely associated with helicity intensity (r=−0.91, p<0.001). — [De Nisco et al., "The atheroprotective nature of helical flow in coronary arteries", PoliTo postprint](https://iris.polito.it/retrieve/handle/11583/2726967/235290/The%20Atheroprotective%20Nature%20of%20Helical%20Flow%20in%20Coronary%20Arteries.pdf) (numbers from search summary; full text not fetched)
- Vorobtsova, Chiastra et al. (2016) on tortuosity and coronary haemodynamics: tortuosity strongly correlated with helicity intensity, and helical flow contributed to the WSS increase. — [PoliTo postprint](https://iris.polito.it/bitstream/11583/2770474/3/2016%20Vorobtsova%20Chiastra%20-%20Effects%20of%20vessel%20tortuosity%20on%20coronary%20hemodynamics%20POST-PRINT.pdf) (search summary)
- Idealised/model RCA work found flow more affected by curvature change than by torsion change (model evidence). — [search summary, Surrey thesis "Blood flow in twisted arteries"](https://openresearch.surrey.ac.uk/esploro/outputs/doctoral/Blood-flow-in-twisted-arteries/99510956902346)
- Chiastra et al. (n=10, CFD models): LAD/diagonal bifurcation angle only mildly influences haemodynamics; curvature radius drives helical flow and near-wall haemodynamics. — [Review, Diagnostics 2022, PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)
- Dynamic CT: a CFD study of bifurcation tortuosity used in vivo dynamic CT. — [PMC7574594](https://pmc.ncbi.nlm.nih.gov/articles/PMC7574594/) (not read in full)

### Inferences
- Diameter-type features (Finet's ratio, branch diameters) explained more WSS variance than bifurcation angle in the largest human CFD cohort. The current set has a ratio but no absolute size, so absolute lumen diameter (or a body-size-normalised diameter) is the most defensible addition.
- Curvature (mean absolute) beats arc/chord tortuosity for WSS. A local turning angle is a discretised curvature, so the current feature (3) is aligned with the best-supported metric, provided it is aggregated as a mean absolute value rather than a chord ratio.
- Torsion's WSS effect is mediated by helical flow, which is itself produced by both curvature and torsion; evidence that torsion adds independent variance beyond curvature in human coronaries was not found.
- Bifurcation angle shows modest, configuration-dependent effects; it is the weakest of the three current features on WSS-mechanistic grounds, though it remains a classic plaque correlate.

### Gaps
- No published correlation matrix among curvature, torsion, tortuosity, bifurcation angle, diameter ratio, diameter and taper in the same human cohort was retrieved (the Gharleghi supplementary data may contain one but was not accessed).
- Taper was not among the 11 Gharleghi features; no study quantifying taper's independent WSS contribution was found.
- Machine-learning WSS surrogates with feature attribution (e.g. Gharleghi deep-learning WSS, Rabbi) were not retrieved within budget.
- All WSS evidence is CFD on CT-derived geometry, not measured WSS; it is also confined to the left main bifurcation.

## Q2. Which features survive selection in multivariable / ML models predicting plaque?

### Takeaway
There is little direct evidence. Most multivariable plaque models are dominated by plaque and stenosis features, not geometric ones; studies using geometry alone report many significant univariate associations but only modest combined explanatory power.

### Cited Findings
- Review (Diagnostics 2022) on CCTA geometry and plaque: Tuncay et al. (n=73, CCTA) found curvature 16.7% higher in stenotic segments and 13.8% higher in stenotic arteries; tortuosity associated with stenosis only per-segment. Saltissi et al. (n=149, ICA): short left main plus wide bifurcation angle associated with proximal plaque. Friedman et al. (n=15, autopsy): LM-branch angle related to proximal atherosclerosis. Benetos et al. (n=325): low coronary artery volume index (<28 mm³/g) associated with about 4× more events. Altintas et al. (n=163): C-shaped RCAs more diseased proximally than S-shaped. — [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)
- Same review: Zhu et al. (2003): individual geometric parameters failed, but linear combinations predicted wall thickness with R² 0.17–0.44. The GEOMETRY-CTA study proposes a single "geometric risk score" but results were unavailable at the review's writing. — [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)
- Candreva et al. (CAD patients scheduled for PCI; CCTA, ICA and IVUS-VH): 23 3D geometric indexes in three groups (length-based; curvature-, torsion- and combined; vessel-path-based). 18/23 associated with at least one IVUS-VH parameter, all three groups contributed, and associations persisted after adjustment for clinical characteristics. — [search summary, Univr record](https://iris.univr.it/handle/11562/1104547); [ResearchGate entry](https://www.researchgate.net/publication/369824589_Quantitative_coronary_three-dimensional_geometry_and_its_association_with_atherosclerotic_disease_burden_and_composition)
- In ML from quantitative CCTA predicting ischaemia, percent diameter stenosis and low-density non-calcified plaque volume had highest importance; minimum lumen area and remodelling index also ranked high. These are plaque/lumen features, not centreline geometry. — [Circ Cardiovasc Imaging 2023](https://www.ahajournals.org/doi/10.1161/CIRCIMAGING.122.014369); [JACC Imaging 2020](https://www.sciencedirect.com/science/article/pii/S1936878X20308111)
- A review of data-driven plaque progression models notes ML models predicting atheroma volume change from baseline geometric features plus clinical data. — [PMC10794448](https://pmc.ncbi.nlm.nih.gov/articles/PMC10794448/) (search summary only)

### Inferences
- With 18/23 indexes "significant" in a small PCI cohort, univariate significance is a poor guide to independent value; geometric indexes are likely heavily collinear (length, path and curvature families overlap).
- For a minimal set, the existing evidence points to one size feature (diameter or lumen volume relative to myocardial mass/body size), one branching feature (diameter ratio) and one bending feature (mean absolute curvature). Bifurcation angle is the candidate to drop or keep as a secondary sensitivity feature.

### Gaps
- No study found that applies formal feature selection (LASSO, SHAP, permutation importance) to geometry-only predictors of plaque in a general-population CCTA cohort. This is a genuine literature gap and could be stated as such.
- Deep-learning shape models with reported feature importance were not found within budget.

## Q3. Reproducibility of each feature from CCTA

### Takeaway
Reproducibility evidence is thin and feature-specific. Angles measured with 3D cylinder fitting are reproducible to a few degrees; curvature and torsion depend strongly on centerline sampling resolution and smoothing, with torsion (third derivative) most fragile. No scan-rescan study of coronary curvature/torsion from CCTA was found.

### Cited Findings
- Bifurcation angle from 64-row MSCT using 3D cylinder fits to LM, LAD, LCx: phantom intra-observer difference 0.44 ± 0.54°, inter-observer difference 1.8 ± 5.8°; authors state cylinder fitting avoids planar projections and reduces inter-observer variability. — [UFU repository](https://repositorio.ufu.br/handle/123456789/18107) (search summary)
- LM bifurcation angle in dual-source CT read by two observers averaged 69.3 ± 33.3° (range 14–200°), showing large between-subject spread relative to measurement error. — [Mayo Clinic record](https://mayoclinic.elsevierpure.com/en/publications/anatomic-assessment-of-the-bifurcation-of-the-left-main-coronary-) (search summary)
- Frenet curvature κ = |p′×p″|/|p′|³ and torsion τ = (p′×p″)·p‴/|p′×p″|² need first to third derivatives of noisy centreline points; Gaussian smoothing is standard to limit noise amplification. — [ScienceDirect, ML coronary tortuosity 2026](https://www.sciencedirect.com/science/article/pii/S2772963X26002504) (search summary)
- In vascular bend landmarking (internal carotid, not coronary), centreline smoothing had minimal effect but centreline resolution changed detected bends from 3 to 33. — [PMC8626959](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8626959/) (search summary)
- Deep-learning plaque quantification was reproducible across expert-derived centrelines (ICC 0.975–1.0), indicating volumetric lumen/plaque measures are robust to centreline choice. — [Lancet Digit Health 2022](https://www.thelancet.com/journals/landig/article/PIIS2589-7500(22)00022-X/fulltext)
- Cardiac phase changes curvature and tortuosity (end-systole vs end-diastole), a source of measurement variation in retrospectively gated CCTA. — [PMC7165136](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7165136/) (not read in full)

### Inferences
- Ranking of expected reliability: diameter/area and volume (integrated over many voxels) > diameter ratio and bifurcation angle (few measurements, but robust with 3D fits) > mean curvature/turning angle (second derivative, needs fixed arc-length resampling and smoothing) > torsion (third derivative, undefined where curvature approaches zero).
- To make turning angle defensible, fix the arc-length step and smoothing scale and report a sensitivity analysis over them; this substitutes for the missing scan-rescan literature.
- Cardiac phase should be recorded and, if possible, harmonised (the CGPS acquisition phase matters).

### Gaps
- No scan-rescan or inter-software reproducibility study of coronary curvature or torsion from CCTA was found.
- Sensitivity of diameter ratio to segmentation threshold / partial volume in small daughters was not quantified in retrieved sources.

## Q4. Is torsion worth adding? Is lumen diameter the missing feature?

### Takeaway
Torsion is not worth adding to a minimal set: its effect on WSS is mediated by helical flow that curvature also produces, model evidence suggests curvature dominates, and it is the least reliable to estimate. Lumen size is the most clearly supported missing feature.

### Cited Findings
- Torsion → helicity r=0.64; helicity ↔ adverse WSS r=−0.91 (coronary CFD). — [De Nisco et al., PoliTo](https://iris.polito.it/retrieve/handle/11583/2726967/235290/The%20Atheroprotective%20Nature%20of%20Helical%20Flow%20in%20Coronary%20Arteries.pdf)
- Curvature change affected model RCA flow more than torsion change. — [Surrey thesis](https://openresearch.surrey.ac.uk/esploro/outputs/doctoral/Blood-flow-in-twisted-arteries/99510956902346)
- Branch diameters dominated OSI and were significant for RRT in 127 human LM bifurcations. — [arXiv 2401.12504](https://arxiv.org/html/2401.12504v1)
- Coronary artery volume index (lumen volume relative to myocardial mass) < 28 mm³/g associated with about 4× more events (n=325). — [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)

### Inferences
- If lumen diameter is added, normalise to body size or myocardial mass, since sex differences in diameter (and curvature) were reported and could otherwise confound plaque associations.
- In a region-level analysis, absolute diameter falls along the vessel; adding it also partially captures taper and position along the tree.

### Gaps
- No study testing torsion's incremental value over curvature for plaque (as opposed to WSS) in humans was found.

## Q5. Reverse causation: does plaque alter lumen geometry?

### Takeaway
Yes. Plaque changes lumen diameter (stenosis or, with expansive remodelling, enlargement), and therefore diameter ratio and local curvature; longitudinal studies handle this by measuring geometry or shear at baseline and predicting later change, but in a cross-sectional CCTA cohort diameter-based features are most exposed to this bias.

### Cited Findings
- PREDICTION study (n=219 ACS patients, angiography + IVUS, 3D reconstruction and CFD): low ESS at baseline independently predicted plaque progression and lumen narrowing; low-ESS regions developed excessive expansive remodelling at 6–10 months. — [PMC5508525](https://pmc.ncbi.nlm.nih.gov/articles/PMC5508525); [TCTMD](https://www.tctmd.com/news/endothelial-shear-stress-works-prediction-tool)
- Compensatory expansive remodelling preserves lumen as plaque grows; excessive expansive remodelling enlarges lumen and vessel volume and is a high-risk plaque attribute. — [PMC5508525](https://pmc.ncbi.nlm.nih.gov/articles/PMC5508525)
- The geometry/plaque review does not discuss reverse causation. — [PMC9497479](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/)
- Gharleghi et al. deliberately studied patients without significant stenosis, limiting plaque-induced geometry change. — [arXiv 2401.12504](https://arxiv.org/html/2401.12504v1)

### Inferences
- In a general-population cohort, most plaque is non-obstructive and may be remodelled outward, so lumen diameter can be biased upward or downward at plaque sites. Mitigations: measure diameter at plaque-free reference segments or vessel-level (not lesion-level), use the outer-wall/vessel diameter where available, or use proximal reference diameter for the diameter ratio.
- Curvature and bifurcation angle are largely determined by heart shape and branching and are less altered by plaque, which favours them as exposures in cross-sectional analysis; this is an inference, not a measured finding.

### Gaps
- No study quantifying how much plaque alters CCTA-derived curvature or bifurcation angle was found.
