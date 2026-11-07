# FPCA and functional data analysis applied to vascular centerline geometry

Scope note: the only published work I found that runs a true FPCA on vessel geometry profiles (curvature and radius as functions of arc length) with a clinical comparison is the AneuRisk work on the internal carotid artery (ICA). I found **no peer-reviewed FPCA of coronary curvature, tortuosity or diameter profiles linked to plaque**. The coronary "shape" studies I found use ordinary (multivariate) PCA on mesh or point correspondences, not FPCA on curves along the vessel. One arXiv preprint applies multivariate FPCA to coronary diameter curves. The full texts of Sangalli et al. 2009 (JASA) and Sørensen, Goldsmith and Sangalli 2013 (Stat Med) were read (author postprints); everything else is from abstracts or search snippets unless stated.

## AneuRisk project: what was done, registration, meaning of the components, link to aneurysm location

### Takeaway
On 65 ICA centerlines from 3D rotational angiography in a referral cohort, Sangalli et al. smoothed the centerlines, registered them with affine warping of arc length, ran a separate FPCA on the registered radius and curvature profiles, and used the first two scores of each in a QDA. The QDA separated patients with an aneurysm at or after the ICA terminal bifurcation from the rest, with a leave-one-out error of 21.5%. The components had clear geometric meanings (width, taper, siphon curvature), but the evidence is small, cross-sectional and exploratory.

### Cited Findings
**Bibliography**
- Sangalli LM, Secchi P, Vantini S, Veneziani A. A case study in exploratory functional data analysis: geometrical features of the internal carotid artery. *J Am Stat Assoc* 2009;104(485):37–48. doi:10.1198/jasa.2009.0002 — [author postprint](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf); [RePEc](https://econpapers.repec.org/RePEc:bes:jnlasa:v:104:i:485:y:2009:p:37-48)
- Sangalli LM, Secchi P, Vantini S, Veneziani A. Efficient estimation of three-dimensional curves and their derivatives by free-knot regression splines, applied to the analysis of inner carotid artery centrelines. *J R Stat Soc Ser C* 2009;58(3):285–306. doi:10.1111/j.1467-9876.2008.00653.x — [IDEAS/RePEc](https://ideas.repec.org/a/bla/jorssc/v58y2009i3p285-306.html)
- Sangalli LM, Secchi P, Vantini S, Vitelli V. k-mean alignment for curve clustering. *Comput Stat Data Anal* 2010;54(5):1219–1233. doi:10.1016/j.csda.2009.12.008 — [author postprint](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2010_Sangalli-Secchi-Vantini-Vitelli_CSDA_compresso.pdf)
- Sørensen H, Goldsmith J, Sangalli LM. An introduction with medical applications to functional data analysis. *Stat Med* 2013;32(30):5222–5240. doi:10.1002/sim.5989. This tutorial reuses AneuRisk65 for smoothing, alignment and FPCA. — [author postprint](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2013_Sorensen-Goldsmith-Sangalli_StatMed_compresso.pdf)
- Passerini T, Sangalli LM, Vantini S, et al. An integrated CFD-statistical investigation of parent vasculature of cerebral aneurysms. *Cardiovasc Eng Technol* 2012;3:26–40. This is the hemodynamic follow-up; I did not read it. — cited in [Sørensen et al. 2013](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2013_Sorensen-Goldsmith-Sangalli_StatMed_compresso.pdf)

**Data and cohort (JASA 2009)**
- Sixty-five patients were hospitalised at the Neuroradiology Department of Niguarda Ca' Granda Hospital, Milan, from 2002 to 2005: 33 had an aneurysm at or after the ICA terminal bifurcation, 25 had one along the ICA and 7 were "healthy". Mean age was 55.9 (SD 13.5) years. Sex, side and age were deliberately left out of the analysis, on the argument that they act on pathology only through geometry. — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- Sørensen et al. describe the 65 subjects as "suspected of being affected by cerebral aneurysms", which makes this a referral, case-dominated sample. — [Sørensen et al. 2013](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2013_Sorensen-Goldsmith-Sangalli_StatMed_compresso.pdf)
- Imaging and reconstruction:
  - Imaging was 3D rotational angiography.
  - The lumen was reconstructed with the Vascular Modeling Toolkit (VMTK), using level-set segmentation.
  - The centerline was taken as the centres of the maximal inscribed spheres, and the radius profile as the radii of those spheres.
  - Each subject had 350–1,380 points, and centerline length ranged from 27.2 to 110.1 mm.
  - Left ICAs were mirrored.

  — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)

**Domain and smoothing**
- The abscissa s is approximate arc length measured *from the terminal bifurcation back toward the heart*, with negative values. The distal bifurcation is the common anchor (s = 0), and the curves have different supports (lengths). — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- Coordinates were smoothed with Gaussian-kernel local polynomial regression: degree 4 (p + 2 for second derivatives) and bandwidth 3, chosen by a "Goldilocks" visual criterion. Curvature was computed as C(s) = ||c′ × c″|| / ||c′||³. — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- The JRSS-C companion paper proposes 3D free-knot regression splines instead. It reports that they give more accurate and efficient estimates of centerlines and derivatives, and hence curvature, than local polynomial smoothing. — [IDEAS abstract](https://ideas.repec.org/a/bla/jorssc/v58y2009i3p285-306.html)

**Registration (phase vs amplitude)**
- Registration was done on the *first derivatives* of the centerline (x′, y′, z′). Using derivatives removes the scan-volume location. — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- Phase variability is attributed to "dimensions and proportions of patients' skulls". The warping class is strictly increasing affine maps, h(s) = ms + p, chosen together with a new similarity index that is invariant to affine changes of the abscissa. — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- The template was estimated iteratively by a Procrustes-type scheme:
  - Expectation steps used loess with a span of 20%.
  - Maximisation steps were constrained to shifts of ±5 mm and stretches of ±10%.
  - The warps were normalised to have mean identity.

  — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- The same warping functions were then applied to the radius and curvature profiles, R̃ = R∘h⁻¹ and C̃ = C∘h⁻¹. Sørensen et al. note that alignment barely changed the radius profiles (little variation along the ICA) but revealed a common curvature pattern that was invisible before alignment. — [Sørensen et al. 2013](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2013_Sorensen-Goldsmith-Sangalli_StatMed_compresso.pdf)
- The warping parameters (stretch m_i, shift p_i) did not differ between the aneurysm groups (t-tests, F-tests, LDA). The authors therefore treated phase as "ancillary" and analysed amplitude only. — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- The variability of the registered derivatives was concentrated between s ≈ −50 and −20 mm. This is consistent with the known S-, Ω- and Γ-shaped ICA types, which have two, one or no siphons. — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)

**Descriptive findings after registration**
- After registration, the average radius tapers for s > −30 mm, and two curvature peaks (the siphon centres) appear at about −35 and −20 mm. — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- Aneurysm locations cluster in the terminal, tapered part, after the last curvature peak. After alignment they split into two groups either side of ≈ −13 mm, which the authors read as the average position of the dural ring (not visible on angiography). — [Sørensen et al. 2013](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2013_Sorensen-Goldsmith-Sangalli_StatMed_compresso.pdf)
- Curvature is less autocorrelated between nearby points than radius. Curvature near the last peak is also negatively correlated with curvature in the low-curvature stretch between the peaks, which the authors read as a straight stretch being followed by a marked elbow. — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)

**FPCA results**
- FPCA was run on the covariance, not the correlation, separately for radius and for curvature. Components were displayed as the mean ± one SD of the score times the eigenfunction. — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)

| Profile | Component | Variance explained | Interpretation |
|---|---|---|---|
| Radius | PC1 | 65.6% | Overall ICA width |
| Radius | PC2 | 13.0% (cumulative 78.6%) | Tapering |
| Curvature | PC1 | 33.4% | Curvature near the last curvature peak (how sharply the siphon bends) |
| Curvature | PC2 | 18.2% (cumulative 51.6%) | Curvature of the stretch between the two peaks; a referee noted it could also reflect a shift in peak location, i.e. residual phase |

  — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)

**Relation to aneurysm location**
- The comparison was the "Upper" group (n = 33, aneurysm at or after the terminal bifurcation) against the "Lower" group (n = 32: 25 with an ICA aneurysm and 7 healthy). — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- Upper-group patients had wider and more tapered ICAs, with less curvature between the two peaks. Their score variances were smaller for all components except curvature PC2. Welch t-test p-values were reported per component (e.g. 0.03% for one radius component), with no correction for multiplicity. — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- The QDA used the first two radius and first two curvature scores:
  - The number of components (k_R = k_C = 2) was chosen by minimising the leave-one-out error over the same data; repeated 10-fold CV was added at a referee's request.
  - The leave-one-out error was 21.54% and the apparent error 15.38%.
  - The Lower-group misclassification rate was 28.1% and the Upper-group rate 15.2%.

  — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- The authors' reading is that Upper-group patients form a tighter subpopulation nested inside the more spread-out Lower group. — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- Sørensen et al. present this as "further strong statistical evidence" for the morphology–aneurysm conjecture. — [Sørensen et al. 2013](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2013_Sorensen-Goldsmith-Sangalli_StatMed_compresso.pdf)

**k-mean alignment (CSDA 2010)**
- This paper proposes joint clustering and alignment, so that amplitude clusters are not confused with phase clusters. The CSDA postprint illustrates it with simulations and the Berkeley growth data. I did not find the AneuRisk application in that paper; it appears in other Sangalli/Vantini papers that I did not verify. — [Sangalli et al. 2010 CSDA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2010_Sangalli-Secchi-Vantini-Vitelli_CSDA_compresso.pdf)
- A later elastic (square-root velocity) analysis of AneuRisk65 reportedly recovered the Ω-, Γ- and S-shaped clusters by hierarchical clustering. This source is a secondary page and I did not verify it. — [Lacuna page](https://lacuna.tiptreesystems.com/work/analysis-of-aneurisk65-data-elastic-shape-registration)

**Non-FDA corroboration that ICA curvature relates to aneurysm**
- Lauric A et al. found higher mean intracranial ICA curvature in ICAs with sidewall aneurysms, adjusted for age, hypertension, hypercholesterolaemia and smoking. This is a retrospective study with scalar curvature, not FPCA. — [J NeuroIntervent Surg 2014;6(10):733](https://jnis.bmj.com/content/6/10/733)

### Inferences
- The AneuRisk pipeline is a direct methodological template for curvature and radius profiles on a coronary trunk: smooth, take arc length from an anatomical landmark, register, run FPCA separately per profile, then feed a few scores to a model. It also shows the key design choice: the warp class (affine here) defines what counts as "phase", and the authors justified ignoring phase only *after* checking it was unrelated to the outcome.
- The clinical evidence is weak by modern standards:
  - n = 65 in a referral sample.
  - The design is cross-sectional, with the outcome (aneurysm location) present at imaging.
  - Group sizes were 33 versus 32.
  - Many univariate tests had no multiplicity correction.
  - Model size was chosen by the same leave-one-out error that is reported, so the 21.5% is mildly optimistic.
  - There is no external validation.

  It should be cited as an illustrative, hypothesis-generating example, not as evidence that geometry predicts disease.
- The interpretation of curvature PC2 is ambiguous (amplitude versus residual phase). This is a concrete example of why FPCA components should be described with caution after an imperfect registration.

### Gaps
- I could not verify the number of components retained or the CV details in the JRSS-C paper. The abstract only reports the method comparison.
- I did not verify which paper contains the AneuRisk application of k-mean alignment (possibly Sangalli, Secchi, Vantini, Vitelli 2010 in *Communications in Applied and Industrial Mathematics*, or Vantini's later work).
- I did not read the follow-up hemodynamic paper (Passerini et al. 2012).

## FPCA/FDA and shape PCA on coronary geometry; carotid and aortic analogues

### Takeaway
I found no peer-reviewed FPCA of coronary curvature, tortuosity or taper profiles. The coronary "shape" literature uses multivariate PCA on point-corresponded surface meshes: bifurcation atlases in normal anatomy (Medrano-Gracia 2017) and LAD shape linked to later MI in a small angiographic cohort (Griffo 2025). Carotid and aortic work uses scalar geometry or mesh PCA, mostly in small referral or patient cohorts.

### Cited Findings
**Coronary**
- **Medrano-Gracia P, Ormiston J, Webster M, et al.** A study of coronary bifurcation shape in a normal population. *J Cardiovasc Transl Res* 2017;10(1):82–90. doi:10.1007/s12265-016-9720-2. — [PMC5323506](https://pmc.ncbi.nlm.nih.gov/articles/PMC5323506)
  - Cohort: retrospective CTCA database, 211 patients selected for zero calcium score and no stenosis, giving 446 bifurcations (LM, D1, OM1, crux).
  - Shape representation: lumen meshes cut by a 10 mm sphere around each bifurcation. A CAD template was registered by rigid then non-rigid coherent point drift (no landmarks) to 3,057 corresponding points.
  - PCA: ordinary PCA with isotropic size removed. The first three modes explain 71% (PC1 ≈ 43%). PC1 was interpreted as bifurcation angle B, PC2 as the ratio of angles A and C, and PC3 as curvature.
  - Associations: modes differed by bifurcation type, and scale and PC1 by sex. There were no significant associations with hypertension, smoking or diabetes (ANOVA, α = 0.01).
  - Design: cross-sectional, no outcomes.
- **Griffo B, Lodi Rizzini M, Candreva A, Collet C, Mizukami T, Chiastra C, Gallo D, Morbiducci U, Aldieri A.** Exploring the association between coronary vascular anatomical features and future myocardial infarction through statistical shape modelling. *J Biomech* 2025;189:112829. doi:10.1016/j.jbiomech.2025.112829. — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0021929025003410); [IRIS PoliTo record](https://iris.polito.it/handle/11583/3001212)
  - Data: 69 LAD models from 3D quantitative coronary angiography, i.e. invasive, so a referral population. Future-culprit cases were compared with non-culprit controls, and the outcome was MI at about 5 years.
  - Methods: PCA followed by LDA on the PCA scores, with a second analysis after the main lesion was virtually removed. Both discriminations were reported as p < 0.0001, and adding main-lesion severity improved discrimination.
  - What I could not see: the paywalled full text, so the exact case/control numbers, the validation scheme and any AUC are unknown.
  - Design: this is mesh/shape PCA, not FPCA of curvature profiles, and it is case–control on diseased vessels.
- **Zhu Y, Golovkine S, Bargary N, Simpkin AJ.** Derivative estimation of multivariate functional data. arXiv:2411.18398 (2024). **Preprint; peer review not confirmed.** — [arXiv](https://arxiv.org/abs/2411.18398)
  - Methods: multivariate FPCA of the *derivatives* of coronary diameter and QFR curves from angiograms.
  - Results: a search snippet says a component moves the location of the narrowest diameter and of the fastest QFR drop, and that 139 patients were included; neither was verified on the abstract page.
  - No plaque outcome.

**Carotid**
- **Bijari PB, Wasserman BA, Steinman DA** (Stroke 2014). Carotid bifurcation geometry (flare, proximal curvature) was an "independent, albeit weak, predictor" of early ICA bulb wall thickening, but only once geometric assumptions and the effect of disease on geometry were addressed. This is scalar geometry, not FPCA. — [search snippet; ARIC proposal](https://aric.cscc.unc.edu/aric9/system/files/aricprops/priv/MP2040.pdf); [Bijari thesis](https://core.ac.uk/works/81075242)
- A 2020 3D CMR study (n = 121 high-risk patients) found that carotid tortuosity (β = 0.764) and ICA/CCA diameter ratio (β = −0.302) independently predicted wall thickness. The design is cross-sectional. — [PMC7488078](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7488078/)

**Aortic (multivariate PCA / statistical shape models, small cohorts)**
- An HLHS reconstructed-arch atlas (n = 35): 10 PCA modes explain 90%, and 4 of 5 poor-outcome patients deviated from the atlas above the median. — [CORE](https://core.ac.uk/outputs/49478731/)
- Ascending thoracic aortic aneurysm (ATAA) statistical shape analysis: modes were correlated with simulated wall shear stress and strain, not clinical outcomes. — [J Pers Med 2020, doi:10.3390/jpm10020028](https://doi.org/10.3390/jpm10020028)
- Aortic dissection (n = 31 ATAA): a PLS-DA shape mode was associated with dissection. — [PMC11262626](https://pmc.ncbi.nlm.nih.gov/articles/PMC11262626/)
- Fetal arch, suspected coarctation (n = 112): centerline-based statistical shape model modes separated false-positive from confirmed coarctation. — [PMC10299929](https://pmc.ncbi.nlm.nih.gov/articles/PMC10299929)

### Inferences
- For a coronary thesis, the honest framing is: FPCA of curvature and radius profiles has a clear vascular precedent (AneuRisk, ICA), while coronary shape analyses so far use mesh PCA in normal anatomy or small invasive referral cohorts. A prospective FPCA of plaque-free coronary curvature profiles against incident plaque appears to be unstudied, as far as these searches show. This is an absence of evidence from limited searching, not proof that no such work exists.
- Medrano-Gracia is the closest cohort analogue to a plaque-free baseline (zero CAC, no stenosis), but it has no follow-up. Its curvature mode is a mesh-level mode within 10 mm of the bifurcation, not a profile along the trunk.
- The Griffo result should not be presented as geometry predicting incident disease. The vessels were already diseased, the outcome was MI rather than plaque, the sample was small, and the validation is unclear.

### Gaps
- My searches did not turn up FPCA of coronary curvature or tortuosity profiles, SRV/elastic analysis of coronary centerlines, or FPCA of coronary taper. More specific database searches (e.g. Scopus "functional principal" AND coronary AND centerline) might still find conference papers.
- Not verified:
  - The full text of Griffo 2025 (403 on fetch).
  - The full text of the Bijari Stroke 2014 paper (exact volume, pages and DOI not retrieved).
  - Thomas et al. 2005 (Stroke), on young-adult carotid geometry.
  - Any coronary statistical-shape atlas beyond bifurcations (e.g. other Medrano-Gracia/Young atlas papers).

## Domain handling (arc length vs normalised length, landmarks) and phase vs amplitude

### Takeaway
AneuRisk anchors arc length at a distal landmark (the terminal bifurcation, s = 0), keeps the raw length differences, and absorbs size and position differences with an affine warp of arc length estimated on the centerline derivatives. It reports phase separately and shows it is unrelated to the outcome. The mesh-PCA coronary atlases avoid the issue by using point correspondence inside a fixed sphere.

### Cited Findings
- AneuRisk domain: the abscissa runs from the terminal bifurcation toward the heart, the curves have different supports (27–110 mm) and the template is estimated on the union of supports. The authors used loess partly because "very few curves are defined at high distance from the terminal bifurcation". — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- Warp class: affine, h(s) = ms + p. The authors stress that "the couple ρ and W jointly defines what is meant by phase variability". — [Sangalli et al. 2009 JASA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)
- Sørensen et al. describe landmark versus continuous alignment in general terms, and say that unaddressed misalignment "acts as a confounding factor". — [Sørensen et al. 2013](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2013_Sorensen-Goldsmith-Sangalli_StatMed_compresso.pdf)
- The k-mean alignment paper shows that clustering without alignment can create spurious clusters that are really phase clusters. — [Sangalli et al. 2010 CSDA](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2010_Sangalli-Secchi-Vantini-Vitelli_CSDA_compresso.pdf)
- In the Medrano-Gracia bifurcation study, correspondence came from coherent point drift to a template, with no landmarks. Isotropic scale was kept as a separate size index. Registration error was a median of 0.27 mm and a maximum of 1.36 mm, worst at deformed ostia. — [PMC5323506](https://pmc.ncbi.nlm.nih.gov/articles/PMC5323506)

### Inferences
- For coronary trunk segments with landmark ends (ostium or bifurcations), a normalised-length domain amounts to a fixed affine warp anchored at both landmarks. The AneuRisk approach instead estimates the warp from the data and anchors only one end. Either way, the thesis text should say which variation is being treated as phase, and whether the warp (or segment length) is kept as a covariate. AneuRisk kept it and tested it.
- Normalising to segment length removes absolute position information, such as "curvature 10 mm from the ostium". AneuRisk kept millimetres from a landmark, which is what allowed its dural-ring interpretation.

### Gaps
- I found no coronary study comparing arc-length and normalised-length domains for FPCA.

## Evidence linking geometry components to plaque or outcomes, and its strength

### Takeaway
No study I found links FPCA components of coronary geometry to plaque. The component–outcome links that exist are as follows:
- AneuRisk: aneurysm location, n = 65, referral, cross-sectional.
- Griffo: future MI, n = 69 invasive-angiography LADs, case–control, mesh PCA.
- Medrano-Gracia: risk factors only (null), n = 211 normal CTCA, cross-sectional.
- Several aortic and carotid studies: n of about 30–120, mostly cross-sectional patient cohorts.

All of these are small and hypothesis-generating.

### Cited Findings
| Study | Geometry representation | Design and sample | Outcome / association |
|---|---|---|---|
| AneuRisk ([JASA 2009](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)) | FPCA of ICA radius and curvature profiles | 65 subjects, referral, cross-sectional | QDA leave-one-out error 21.5% for aneurysm location; no external validation |
| Medrano-Gracia 2017 ([PMC5323506](https://pmc.ncbi.nlm.nih.gov/articles/PMC5323506)) | Mesh PCA of coronary bifurcations | 211 patients selected as normal on CTCA | No association with hypertension, smoking or diabetes; type and sex differences only |
| Griffo 2025 ([J Biomech](https://www.sciencedirect.com/science/article/pii/S0021929025003410)) | PCA + LDA of LAD shape | 69 LADs from QCA, culprit vs non-culprit | Discrimination p < 0.0001; details unverified |
| Bijari et al. 2014 ([thesis record](https://core.ac.uk/works/81075242)) | Scalar carotid geometry | Patient cohorts | Geometry an "independent, albeit weak" predictor of wall thickening |
| Lauric et al. 2014 ([JNIS](https://jnis.bmj.com/content/6/10/733)) | Scalar ICA curvature | Retrospective | Higher curvature with sidewall aneurysm (adjusted) |
| Zhu et al. 2024 ([arXiv](https://arxiv.org/abs/2411.18398), **preprint**) | Multivariate FPCA of coronary diameter/QFR derivatives | Angiography | Methods paper; no plaque outcome |

### Inferences
- When citing these as grounding for FPCA, the thesis should say that FPCA has been used to *describe* and *discriminate* vessel geometry in small, mostly referral, cross-sectional samples. It should not say that FPCA geometry components are established predictors of atherosclerosis.
- A prospective, population-based, plaque-free-baseline design would differ from all of the above on every axis (population, design, outcome). That difference should be stated as a contrast, not as a claim that earlier work validates the approach.

### Gaps
- I did not find a prospective study of FPCA-derived vessel geometry against incident atherosclerosis in any vascular bed.
- Griffo 2025 performance metrics and validation scheme are unverified.
