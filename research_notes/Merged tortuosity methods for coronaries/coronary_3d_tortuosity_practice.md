# Coronary 3D tortuosity in practice: metrics, clinical relevance, and CCTA-centerline engineering constraints

Scope note: researched 2026-09-22 in ~18 tool calls. Local paper notes in `docs_thesis/papers/` were read (telloayala2026, grisan2008, mateos2024, shen2026, zhang2024 text). Several primary sources could only be reached as abstracts or search snippets; this is flagged per item. The Ciurică 2019 Hypertension review returned HTTP 403 and was NOT read beyond its bibliographic record.

## Q1. Which tortuosity metrics have been applied to coronary arteries, with what formulas and findings?

### Takeaway
Clinical coronary work is almost entirely 2D invasive angiography using visual bend-count definitions (≥3 bends of ≥45°, or two consecutive 180° turns) or the arc/chord tortuosity index (TI). The only systematic 3D comparison on CCTA (Kashyap 2022, n=127) found curvature-integral measures, not TI, relate to haemodynamics, and recommended mean absolute curvature; recent CCTA work (Ferrari/Pavia 2025, HMM) moves to local, point-wise classification. Different formula families disagree strongly (r=0.116 between a discrete-curvature mean and arc/chord in 22,334 patients).

### Cited Findings

**Clinical (2D angiography) definitions**
- Li et al. 2011 (PLoS One), n=1,010 consecutive angiography patients: coronary tortuosity = "≥3 bends (defined as ≥45° change in vessel direction) along main trunk of at least one artery, present both in systole and in diastole"; prevalence 39.1%. — [Li 2011, PLoS One](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0024232)
- Groves et al. 2009 (W V Med J): severe coronary tortuosity = two consecutive 180° turns by visual estimation in a major epicardial artery; retrospective 8-month WVU angiography cohort. — [PubMed 19585899](https://pubmed.ncbi.nlm.nih.gov/19585899/) (abstract level only)
- Zebić Mihić et al. 2023, n=160 (85 non-obstructive CAD, 75 obstructive): TI = "ratio between the absolute length of the coronary artery and straight-line length", measured in diastole from ostium to smallest visible branch in ImageJ (2D). Angle method = ≥3 consecutive bends ≥45° in systole and diastole. — [Zebić Mihić 2023, PMC10795752](https://pmc.ncbi.nlm.nih.gov/articles/PMC10795752/)
- Eleid et al. 2014: an angiographic "tortuosity score" (per-patient, composite) in SCAD; score 4.41±1.73 vs 2.33±1.49 in controls. The score construction was not retrieved. — [Eleid 2014, PubMed 25138034](https://pubmed.ncbi.nlm.nih.gov/25138034/)

**3D metrics on CCTA centerlines**
- Kashyap et al. 2022 (Sci Rep 12:865): 127 CTCA patients with no obstruction and calcium score 0; left main bifurcation with LM, LAD, LCx each cut 10 mm from the bifurcation point. Formulas: TI = L/C; average absolute curvature κ_a = ∫|κ|dt / L; RMS curvature = sqrt(∫κ² dt / L); average squared derivative curvature = ∫(dκ/dt)² dt / L. Against % low TAWSS (<0.4 Pa) over the full bifurcation: κ_a R²=0.112, p=0.001; ASDC R²=0.101, p=0.001; RMS R²=0.093, p=0.002; TI p=0.865 (no relation). They recommend κ_a. — [Kashyap 2022, PMC8764056](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Kashyap 2022 argue TI "does not account for actual tortuosity in 3D space": depends only on endpoint distance, and their Fig. 1 shows a vessel with more curved segments giving a lower TI. — [Kashyap 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Zhang, Gharleghi, Shen, Beier 2024 (R Soc Open Sci 11:241267), ASOCA 39 cases: used average absolute curvature per branch "as recommended in recent literature [Kashyap 2022]"; bifurcating vs non-bifurcating segments defined as 10 mm of centreline proximal/distal to a bifurcation point; branches trimmed where diameter <2 mm. Discussion states tortuosity definitions are inconsistent, TI cannot capture 3D bending, clinical studies use 2D bend counts or C/S shapes. — local text `docs_thesis/papers/zhang2024curvature.txt`; [Zhang 2024, PMC11416812](https://pmc.ncbi.nlm.nih.gov/articles/PMC11416812/)
- Shen et al. 2026 review (Arch Comput Methods Eng): curvature defined inconsistently (derivative of unit tangent vs 1/R); TI "cannot capture the spatial information"; computational studies use TI, mean absolute curvature, or a single bend, "neglecting the spatiality and continuity of this characteristic". — local note `docs_thesis/papers/shen2026geometry.md`, [doi:10.1007/s11831-026-10530-w](https://doi.org/10.1007/s11831-026-10530-w)
- Ferrari, Spairani, Magenes, Tescari, Grasso, Urtis, Arbustini (Pavia), Eur Heart J 2025 suppl. abstract ehaf784.136: 319 CCTA patients; sliding window along the 3D centerline computing curvature and local tortuosity; multivariate discrete HMM classifies each centerline point as absent/low, moderate, severe; validated on 18 LADs annotated by an independent expert: precision 0.87, recall 0.86; per-class accuracy 0.93/0.83/0.74. Window size and exact features not given in the abstract summary retrieved. — [EHJ 2025 abstract](https://academic.oup.com/eurheartj/article/46/Supplement_1/ehaf784.136/8312275). A related Springer chapter, "Unsupervised Assessment of Coronary Artery Tortuosity Through Hidden Markov Models" (doi 10.1007/978-3-031-95841-0_27), was paywalled and not read. — [Springer](https://link.springer.com/chapter/10.1007/978-3-031-95841-0_27)
- Frenet curvature κ = |p'×p''|/|p'|³ and torsion τ = (p'×p'')·p''' / |p'×p''|² are the standard definitions used in coronary patents and papers; curvature is also estimated as the inverse circumradius through three consecutive centerline points. — [US patent 9785748 (HeartFlow-type plaque-force patents)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9785748) (patent, not peer reviewed)

**2D angiography, large scale (context only)**
- Tello Ayala et al. 2026 (JACC Adv), 38,691 angiograms / 22,334 patients, RCA in LAO only: per-point turning angle / π, mean = global score (range 0.007–0.289); transformer on the ordered per-point profile + age + sex AUROC 0.67 vs 0.60 for scalar + age + sex (no formal test); discrete-curvature score vs arc/chord r=0.116. 2D projection, never acknowledged as such. — local note `docs_thesis/papers/telloayala2026tortuosity.md`, [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)

**General 3D vessel metrics (origin of DM, ICM, SOAM)**
- Bullitt et al. 2003 (IEEE TMI, cerebral MRA): Distance Metric DM = path length / chord; Inflection Count Metric ICM = (number of inflection points + 1) × DM; Sum of Angles Metric SOAM = summed angle change along the 3D curve normalised by length (details not retrieved from the snippet). ICM was reported effective at recognising abnormal tortuosity. — [Bullitt 2003, PubMed 12956271](https://pubmed.ncbi.nlm.nih.gov/12956271/)
- Grisan 2008 (IEEE TMI, 2D retinal): tortuosity density τ = ((n−1)/n)·(1/L_c)·Σ_i (L_c,si/L_χ,si − 1) over n constant-curvature-sign "turn curves"; straight stretches split between neighbours; hysteresis threshold on curvature to avoid spurious turns; cubic smoothing spline γ=0.005 on manual points. Properties required: rotation/translation invariance, composition (whole ≥ part), monotone in frequency and in amplitude. — local note `docs_thesis/papers/grisan2008tortuosity.md`

### Inferences
- The field's 3D coronary evidence base for "which metric" rests essentially on one CFD-correlation study (Kashyap 2022, R² ≈ 0.1) plus a UNSW group that adopted its recommendation. Choosing κ_a has precedent, but its selection criterion was haemodynamic, not geometric validity or reproducibility.
- The clinical ≥3 bends ≥45° rule is a 2D-angle count; a faithful 3D analogue would require a definition of "bend" and of "angle" on a space curve (e.g. tangent direction change over a turn), which none of the retrieved papers provides for CCTA.

### Gaps
- Exact SOAM formula, Eleid's score construction, and the Ferrari HMM window/features were not retrieved in full text.
- No CCTA study found that reports torsion-based tortuosity for coronaries with a clinical endpoint (torsion appears in patents and in aortic work, e.g. [Application of 3D curvature and torsion in evaluating aortic tortuosity](https://www.sciencedirect.com/science/article/abs/pii/S1007570420304494), not read).

## Q2. Clinical relevance (disease, plaque, dominance, age, sex, hypertension, SCAD)

### Takeaway
Across definitions, tortuosity is consistently higher in women and in hypertension, strongly associated with SCAD, and inversely associated with obstructive CAD (while associated with non-obstructive disease/ischaemia). Age effects are inconsistent. No retrieved study linked coronary tortuosity to dominance.

### Cited Findings
- Li 2011, n=1,010: tortuosity more frequent in women (OR 2.603), hypertension (OR 1.533, p=0.006); negatively associated with CAD (OR 0.755, p=0.045); LAD tortuosity negatively associated with LAD atherosclerosis; three-vessel disease patients less tortuous. By vessel: LCx 26.9%, LAD 21.1%, RCA 1.4%. No reproducibility reported. — [Li 2011](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0024232)
- Groves 2009: no correlation with age >65; the paper title reports severe tortuosity in relation to significant CAD (inverse association per the thesis CLAUDE.md summary). — [PubMed 19585899](https://pubmed.ncbi.nlm.nih.gov/19585899/)
- Zebić Mihić 2023: TI higher in non-obstructive than obstructive CAD for all three arteries (p<0.001 LCx, LAD; p=0.014 RCA); women higher TI in LCx and LAD; hypertension significant for RCA only; TI associated more strongly than the angle method with the territory of ischaemia. — [PMC10795752](https://pmc.ncbi.nlm.nih.gov/articles/PMC10795752/)
- Eleid 2014, SCAD n=246 (96% women) vs 313 controls: tortuosity in 78% vs 17% (p<0.0001); recurrent SCAD (n=40) occurred within tortuous segments in 80%. — [Eleid 2014](https://pubmed.ncbi.nlm.nih.gov/25138034/)
- Tello Ayala 2026, n=22,334 (2D, RCA): adjusted female β=0.17, hypertension β=0.06, T2D β=−0.11, age not significant after adjustment; OR 1.05/SD any RCA stenosis, 1.09/SD severe CAD; CAD label read from the same angiogram. — local note
- Kashyap 2022 (3D CCTA, no CAD): curvature relates to low TAWSS, the proposed mechanism linking tortuosity to atherosclerosis-prone flow. — [Kashyap 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Shen 2026 review: SCAD occurs in mid to distal segments and vulnerable plaques mostly outside the left main, so whole-tree analysis is needed. — local note
- Ciurică et al. 2019 "Arterial Tortuosity" (Hypertension 73:951–960) is the standard review covering hypertension, age, connective-tissue disease, FMD and SCAD links; not read (403). — [PubMed 30852920](https://pubmed.ncbi.nlm.nih.gov/30852920/)

### Inferences
- The direction of the disease association depends on the endpoint (obstructive: inverse; non-obstructive / ischaemia / SCAD: positive), consistently across bend-count and TI definitions, so a new measure should be validated against geometry, not by whether it reproduces a CAD association.
- Sex is the most replicated covariate; a new measure failing to show women > men on a healthy cohort would be a warning sign (though all sex evidence retrieved is 2D).

### Gaps
- No retrieved study on coronary tortuosity vs dominance.
- No 3D CCTA study with plaque (as opposed to stenosis or WSS) as endpoint was retrieved in this pass.

## Q3. Has anyone combined an inflection/turn-segmented index with 3D curvature/shape descriptors?

### Takeaway
No retrieved paper ports Grisan's turn-segmented tortuosity density to 3D curves for coronaries or other 3D vessels. The closest existing combinations are Bullitt's ICM (inflection count × arc/chord, 3D cerebral) and bend-landmarking methods for the carotid siphon that segment by curvature peaks bounded by torsion extrema (Piccinelli) or by curvature-vector rotation in a parallel transport frame (Bogunović).

### Cited Findings
- Bullitt ICM multiplies a turn count by DM in 3D; it does not integrate curvature within turns. — [Bullitt 2003](https://pubmed.ncbi.nlm.nih.gov/12956271/)
- Kjeldsberg et al. 2021 (BioMed Eng OnLine), internal carotid artery from 3D rotational angiography: compares Piccinelli's bend detection (curvature peaks bounded by torsion extrema) and Bogunović's (curvature-vector orientation change in a parallel-transport frame, angle thresholds). Piccinelli gave 6–8 bends with CV 47–58% for one bend; Bogunović consistently 4 bends, CV <5%, and robust across segmentation variants. — [Kjeldsberg 2021, PMC8626959](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- In 3D, curvature κ ≥ 0 has no sign, so Grisan's "change of curvature sign" inflection has no direct analogue; ICM and Bogunović use a change in the normal/curvature-vector direction instead. (Grisan definition: local note; 3D alternatives: Kjeldsberg 2021.)
- Mateos et al. 2024 (BMC Med Imaging) is the one 3D descendant found that cites Grisan, but it measures surface folding of voxel solids via axis-aligned slice contours, not curves. — local note `mateos2024tortuosity3d.md`
- Retinal literature still treats Grisan as the reference: in a 2019 Sci Rep comparison it was "closest to the specialists"; a 2025 PLoS One paper tests local vs global retinal indices, both 2D. — [Sci Rep 2019](https://www.nature.com/articles/s41598-019-56507-7); [PLoS One 2025](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0329379)
- Johnson & Dougherty 2007 (Med Eng Phys) proposed robust 3D tortuosity based on the minimum curvature of approximating polynomial spline fits to the vessel mid-line, designed for noisy data (abstract snippet only). — [Med Eng Phys 2007](https://www.sciencedirect.com/science/article/abs/pii/S1350453306001652)

### Inferences
- A 3D turn-segmented density is an open niche, but "no paper does it" rests on a few search passes, not a systematic review.
- The design choice that matters is the 3D "turn" definition: rotation of the principal normal beyond a threshold (Bogunović-like, stable) versus torsion extrema (Piccinelli-like, fragile). Evidence (Kjeldsberg) favours the parallel-transport / normal-rotation route.

### Gaps
- Pulmonary and 3D OCTA literature not searched in depth; possible 3D turn-based indices there were not found.

## Q4. Smoothing/resampling, spacing, cardiac phase, reproducibility on CCTA centerlines

### Takeaway
Every 3D coronary study smooths and resamples, but parameters are reported ad hoc and rarely justified by sensitivity analysis. The one explicit sensitivity study (carotid) shows centerline resampling resolution dominates bend counts (3 to 33 bends), while smoothing strength matters less. No test-retest reproducibility of 3D coronary tortuosity on CCTA was found; cardiac-phase effects are documented on angiographic 3D reconstructions.

### Cited Findings
- Kashyap 2022 pipeline: VMTK centerlines from a surface mesh, Taubin smoothing (passband 0.03, 30 iterations), centerlines resampled at 0.01 mm "to minimize errors"; ASDC (derivative of curvature) had kurtosis 63.25 in LM, while κ_a was near normal (kurtosis 2.38); surface roughness after reconstruction may affect values. — [Kashyap 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Kjeldsberg 2021: centerline resolution most influential; bend count varied 3 to 33 across resolution; smoothing factor had least impact (6–7 bends); recommended resolution 0.1 (units per their VMTK setup), smoothing λ 1.2–1.5, 60–100 iterations, with the caveat that settings may not transfer to other vascular regions. — [PMC8626959](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- A diameter-scaled approach: examine the centerline at a scale equal to the mean equivalent diameter, smoothing with a Gaussian of that width (from search snippet; primary source not confirmed). — [search snippet, source unverified](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- Grisan 2008 used a smoothing spline plus hysteresis on curvature to stop noise creating spurious turns. — local note
- Shen, Zhang, Beier 2022 (conference) studied "the effect of diameter variation when accessing patient-specific coronary tortuosity" (cited in Zhang 2024 ref 58; not read). — `zhang2024curvature.txt`
- Cardiac phase: Liao et al. 2002 (Cathet Cardiovasc Interv) analysed curvature, torsion and flexion points at end-diastole vs end-systole on 3D angiographic reconstructions, showing cyclic shape change. — [Liao 2002](https://onlinelibrary.wiley.com/doi/10.1002/ccd.10106) (abstract level). Clinical definitions require bends present in both systole and diastole (Li 2011; Zebić Mihić 2023). Zhang 2024 recommends future work consider heart motion. — `zhang2024curvature.txt`
- Reproducibility: Li 2011 and Zebić Mihić 2023 report no inter-observer coefficients; the Ferrari 2025 HMM validated on only 18 LADs; Tello Ayala 2026 cardiologist agreement κ=0.52. — sources above.

### Inferences
- At ~0.5 mm voxel spacing, the centerline point jitter is of order a voxel; curvature (second derivative) and torsion (third) amplify this. A smoothing scale tied to vessel diameter (a few mm for coronaries) and arc-length resampling finer than the smoothing scale but independent of voxel grid is the defensible default; values must be reported as a function of both.
- Resampling alone (Kashyap's 0.01 mm) does not remove noise; it only removes discretisation of the finite differences. Smoothing scale is what sets the noise floor.
- Turn/inflection counts are the most fragile quantity (Kjeldsberg: 3 to 33), so any turn-segmented index needs hysteresis or a minimum turn length/angle, as Grisan did.
- CCTA is usually reconstructed at a single mid-diastolic or end-systolic phase; phase should be recorded, and ImageCAS-type data give one phase only, so phase robustness cannot be tested there.

### Gaps
- No CCTA scan-rescan or inter-extractor ICC for 3D coronary curvature/tortuosity found.
- No study found quantifying dependence of coronary curvature on reconstruction kernel or voxel spacing.

## Q5. How should the tree be decomposed?

### Takeaway
Published 3D coronary work uses either whole named main vessels (ostium to distal end) or short fixed-length pieces around bifurcations (10 mm; Kashyap, Zhang). Clinical definitions work on the "main trunk" of each major artery. No retrieved paper uses SCCT/AHA segment-level tortuosity on CCTA.

### Cited Findings
- Kashyap 2022: LM, LAD, LCx cut 10 mm from the LM bifurcation. — [PMC8764056](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Zhang 2024: every branch per case, bifurcating vs non-bifurcating 10 mm segments, distal branches trimmed at <2 mm diameter. — `zhang2024curvature.txt`
- Li 2011: "along main trunk of at least one artery". Zebić Mihić 2023: ostium to smallest visible branch per major artery. Tello Ayala 2026: longest path from RCA origin to distal PDA. — sources above.
- Shen 2026: whole-tree analysis needed because SCAD and vulnerable plaques are mid-to-distal. — local note
- Grisan composition property (whole ≥ any part) is a constraint relevant to aggregating segments into paths. — local note

### Inferences
- Root-to-leaf paths double-count proximal segments shared between paths; bifurcation-to-bifurcation segments are short and many fall below the length needed for stable curvature. A named-vessel path (ostium to distal end of LAD, LCx, RCA) plus named-segment sub-values (proximal/mid/distal) matches the clinical unit, the thesis "keyed by anatomical label" rule, and serial comparison.
- Because density-type measures (per unit length) are length-normalised, per-segment values can be combined by length-weighted averaging, but TI (arc/chord) cannot be combined that way.
- Short segments (for example <10–15 mm) should return NaN with a reason, since a smoothing kernel of a few mm consumes much of their length.

### Gaps
- No source retrieved on SCCT 18-segment-based tortuosity or on how junction points are shared between segments in coronary tortuosity studies.
