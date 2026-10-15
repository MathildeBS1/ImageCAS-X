# Centerline-only 3D shape descriptors beyond curvature (torsion, tortuosity, helicity-related geometry) as predictors of low/oscillatory WSS and coronary plaque

Scope note: about 16 tool calls. Several primary PDFs (Vorobtsova 2016, De Nisco 2019 ABME full text, Li 2018 JIMR, PMC pages) returned 403 or bot-check pages, so for some of them only abstracts or search snippets were checked. These are flagged as such. Facts from memory that I could not verify in this session are in the Gaps sections, not in Cited Findings.

## Q1. Does torsion add predictive information beyond curvature for low WSS / plaque?

### Takeaway
Torsion is the one centerline descriptor with a mechanistic link to coronary helical flow: in swine CFD, torsion and helicity correlate at r = 0.64. In the human left-tree CFD data checked here, though, mean torsion did **not** separate stenosed from non-stenosed trees, while mean curvature did. No study found adjusts torsion for curvature against a plaque outcome, so "torsion is independent of curvature" is a hypothesis, not an established finding.

### Cited Findings
- **De Nisco et al. 2019, Ann Biomed Eng 47:425-438 (swine, n = 30 coronary arteries, CCTA+IVUS-based CFD).** Torsion was associated with helical flow features (r = 0.64, p < 0.001). Helicity intensity was strongly and inversely associated with "unfavorable WSS conditions" (r = -0.91, p < 0.001). The abstract does not say whether curvature correlated with helicity. **Animal; abstract-level only.** — [Repub abstract](https://repub.eur.nl/pub/112774); [PoliTo PDF (403 in this session)](https://iris.polito.it/retrieve/handle/11583/2726967/235290/The%20Atheroprotective%20Nature%20of%20Helical%20Flow%20in%20Coronary%20Arteries.pdf)
- **Zhang, Gharleghi, Shen, Beier 2024, R Soc Open Sci 11(9), DOI 10.1098/rsos.241267 (human, n = 39 ASOCA left coronary trees: 20 non-stenosed, 12 moderate, 7 severe; CFD).** Centerlines came from VMTK, and mean absolute curvature and mean torsion were computed along them; no centerline smoothing is described. Results:
  - **Curvature** was the only geometric descriptor that differed for whole trees, non-stenosed vs stenosed: 1.230 ± 0.090 vs 1.321 ± 0.131 (p = 0.024). It also differed for non-bifurcating segments: 0.902 ± 0.162 vs 1.001 ± 0.116 (p = 0.027). Curvature AUC was 0.711 (sensitivity 0.842, specificity 0.600).
  - **Torsion was not significant**, either for whole trees (p = 0.247) or for non-bifurcating segments (p = 0.072).
  - At bifurcations, only distal main vessel torsion differed (3.428 vs 2.771, p = 0.024). Proximal main vessel torsion (p = 0.065) and side-branch torsion (p = 0.057) did not reach significance.
  - Bifurcation angle (p = 0.742) and Finet ratio (p = 0.851) did not differ.
  - Curvature correlated with diameter (r = -0.474, p = 0.002).
  - %High-OSI separated the groups (p < 0.001; AUC 0.813). %low-TAESS did not separate non-stenosed from stenosed trees (p = 0.813), but it did separate moderate from severe (p = 0.009).
  - The fetch tool reported curvature units as "m⁻¹", which looks like a transcription error; check the paper before quoting units.
  - **Cross-sectional design**: stenosed vessels were simulated as they are, so plaque geometry contaminates the descriptors.
  - — [ar5iv preprint 2312.00257](https://ar5iv.labs.arxiv.org/html/2312.00257); [PMC11416812](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11416812/)
- **De Nisco et al. 2021, Front Bioeng Biotechnol (49 human arteries: 18 RCA, 18 LAD, 13 LCX, from 48 patients; 30 swine arteries).** Centerlines from VMTK were fitted with **free-knot regression splines** before curvature and torsion were computed from the derivatives. Mean values per main vessel were used. Curvature, torsion and tortuosity did not differ significantly between species. The page text did not include correlations between geometry and helicity/WSS. — [Frontiers full text](https://www.frontiersin.org/articles/10.3389/fbioe.2021.731924/full)
- **Vorobtsova et al. 2016 (patient-specific full coronary trees, CFD).** The abstract-level summary says more tortuous vessels had *higher* WSS, helicity intensity correlated strongly with tortuosity, and helical flow contributed directly to the WSS increase. Full text was blocked (403), so I could not check how tortuosity was defined (curvature- and torsion-based) or extract r values. — [PoliTo post-print](https://iris.polito.it/bitstream/11583/2770474/3/2016%20Vorobtsova%20Chiastra%20-%20Effects%20of%20vessel%20tortuosity%20on%20coronary%20hemodynamics%20POST-PRINT.pdf)
- **Idealized human LAD bifurcation CFD (Chiastra et al.).** Smaller curvature radius gave higher helicity intensity, and helical-flow topology was "driven mainly by the vessel curvature". **Idealized model.** — [PoliTo PDF](https://iris.polito.it/retrieve/handle/11583/2677968/158335/SSS_IdealizedCoronary_Chiastra_0119.pdf)

### Inferences
- In Zhang 2024, curvature beat torsion at the patient level. That is weak evidence that torsion carries little extra signal for plaque presence at tree level. But the study is small (n = 39), cross-sectional and averaged over whole trees. It says nothing about window-level (proximal/mid/distal) prediction of *new* plaque.
- The mechanistic chain "torsion → helicity → higher TAWSS → less wall growth" rests on swine data (De Nisco 2019/2020). If it carries over to humans, torsion would predict **lower** risk (protective direction). That makes it an interesting, hypothesis-driven fourth feature, because its expected sign is the opposite of curvature.
- Curvature also drives helicity (the idealized LAD study), so torsion and curvature should be checked for collinearity per window before both go into the same per-artery model.

### Gaps
- No study found tests torsion against plaque **after adjusting for curvature** in humans. Nor did any study use torsion to predict **new** plaque in plaque-free segments.
- I could not verify effect sizes for older human RCA/LAD geometry catalogue work from memory (e.g., Zhu/Ding/Friedman on curvature/torsion and risk), so it is not cited here.
- The De Nisco 2019 full text, which would give the per-descriptor r for torsion vs curvature with h2/h4/LNH, was not accessible.

## Q2. Is tortuosity (global or local) associated with plaque or with low WSS, and in which direction?

### Takeaway
The evidence conflicts in both directions, and the result depends on the metric:
- **CFD:** tortuosity *raises* WSS through helical flow (Vorobtsova 2016).
- **Clinical, "bend-count" definitions:** several studies report less stenosis or less calcium in tortuous segments (the "tortuosity paradox"). Others report more calcium, or no association.
- **CCTA, local curvature:** a CCTA study found curvature associated with stenosis per segment and per artery. Tortuosity was associated only per segment.

### Cited Findings
- **Li et al. 2018, J Int Med Res (CCTA).** Stenosis prevalence was significantly lower in tortuous than in non-tortuous segments, and the authors propose tortuosity as protective. N and effect sizes are not verified (403). — [DOAJ record](https://doaj.org/article/f056df4b58814c35a265c7f7b2f1c5a2)
- **Nannini et al. 2024, APL Bioengineering (automated deep-learning CCTA pipeline, trained on 281 annotated CCTAs).** Calcium volume was lower in patients with higher tortuosity scores, i.e. a negative association with calcific plaque. Tortuosity was scored by counting branches with 3 or more bends greater than 45°. This is a methods paper, so the clinical association is secondary. — [PoliMi PDF](https://re.public.polimi.it/retrieve/afba3858-b86a-41d2-8746-fca782ec8841/2024_Nannini_APLBio.pdf); [DOAJ](https://doaj.org/article/682cc7f4ef964392a6e826332d875725)
- **Li et al. 2022, BMC Surgery (n = 1,280, retrospective; tortuosity = 3 or more consecutive curvatures greater than 45°).** A review reports no significant multivariable association with calcium score, except an association with moderate CAC in women. This is second-hand via search snippet. — [DOAJ](https://doaj.org/article/fc8284499d0c4a30b7c1a465bc82d245)
- **Stable angina study, n = 83, normal or near-normal coronaries.** CAC score was *higher* in the tortuous group, and the correlation stayed significant after confounder adjustment. Snippet level only. — [SDL index record](https://sindex.sdl.edu.sa/esploro/outputs/journalArticle/The-relation-between-coronary-tortuosity-and/9930268108331)
- **2013 Polish Heart Journal.** Tortuous coronary arteries were associated with subclinical atherosclerosis (carotid IMT) even when the coronaries looked normal. — [Kardiol Pol 71(11)](https://journals.viamedica.pl/polish_heart_journal/article/view/77616)
- **CCTA geometry study (UMC Utrecht group, 2018; snippet-level).** Curvature was associated with significant stenosis per segment (p < 0.001) and per artery (p = 0.002), and was 16.7% higher in stenosed segments. Tortuosity was associated only per segment (p = 0.002). — [UMC Utrecht record](https://researchinformation.umcutrecht.nl/en/publications/non-invasive-assessment-of-coronary-artery-geometry-using-coronar/)
- **2023 LAD study (QIMS).** Tortuosity and bifurcation angle did not independently affect the vessel wall; only the two in combination did. — [QIMS](https://qims.amegroups.org/article/view/117032/html)
- **Vorobtsova 2016 (CFD, humans).** More tortuous vessels had higher physiological WSS. — [PoliTo post-print](https://iris.polito.it/bitstream/11583/2770474/3/2016%20Vorobtsova%20Chiastra%20-%20Effects%20of%20vessel%20tortuosity%20on%20coronary%20hemodynamics%20POST-PRINT.pdf)

### Inferences
- Several things could explain the "paradox":
  - Clinical tortuosity is a coarse bend count (3 or more bends greater than 45°), very different from curvature integrated along a window.
  - Tortuosity is linked to age, hypertension and female sex, which confounds the comparisons.
  - CFD suggests tortuous (helical) vessels have *higher* mean WSS, while low WSS sits at the inner bend.
- The distance-metric tortuosity index (arc length / chord length − 1) is almost a monotone function of integrated curvature over a short window. In 1-3 cm proximal/mid/distal windows it would be highly collinear with mean turning angle, so it is a poor choice for a fourth feature.
- I found no longitudinal study of tortuosity predicting new plaque.

### Gaps
- No prospective or serial CCTA/IVUS study found for tortuosity, sum-of-angles metric, or inflection-point count vs new plaque.
- No source found on **inflection points / curvature reversals** (S-shapes) vs WSS or plaque in human coronaries.

## Q3. Is helical flow intensity determined by centerline geometry, and is it atheroprotective?

### Takeaway
Helicity intensity (h2) is geometry-driven: by torsion in swine (r = 0.64) and by curvature in idealized and human models. The only longitudinal evidence is swine. There, high baseline h2 predicted *less* wall-thickness growth. Human CFD from 2025 shows h2 lowers the low-WSS area but raises the area of adversely *high* WSS, so "atheroprotective" is contested in humans.

### Cited Findings
- **De Nisco et al. 2020, Atherosclerosis, "The impact of helical flow on coronary atherosclerotic plaque development" (5 FH minipigs, 15 arteries; CCTA+IVUS at 3 months and 9.4 ± 1.9 months).**
  - TAWSS correlated with whole-volume h2 (r = 0.925, p < 0.001) and with near-wall h2 (r = 0.629, p < 0.01).
  - Mean wall thickness grew from 0.183 ± 0.108 to 0.427 ± 0.313 mm.
  - Wall-thickness growth by near-wall h2 tertile: high 0.032 ± 0.007, mid 0.037 ± 0.007, low 0.040 ± 0.007 mm/month (p < 0.05 for high vs others).
  - For comparison, by TAWSS tertile: low 0.048, mid 0.035, high 0.027 mm/month.
  - **Animal, very small n.** Geometry (torsion) was not tested directly against wall-thickness change.
  - — [Repub full text](https://repub.eur.nl/pub/125151/Repub_125151.pdf)
- **De Nisco 2019 (swine, 30 arteries).** Torsion correlated with helical-flow features (r = 0.64). Helicity intensity correlated with unfavorable WSS (r = -0.91). — [Repub](https://repub.eur.nl/pub/112774)
- **Shen, Zhang, Keramati, Almeida, Beier 2025, "High-intensity helical flow: a double-edged sword" (R Soc Open Sci, DOI 10.1098/rsos.242184; human ASOCA, n = 39 left trees).**
  - h2 correlated with higher TAESS in all segments (p < 0.05).
  - In stenosed cases, the area with low TAESS (< 0.5 Pa) shrank (p = 0.0001) and the area with high TAESS (> 4.71 Pa) grew (p < 0.05).
  - The authors conclude helical flow is not uniformly protective.
  - — [arXiv 2502.06161](https://arxiv.org/abs/2502.06161)
- **Idealized LAD.** Curvature radius governs helical-flow generation. — [Chiastra PDF](https://iris.polito.it/retrieve/handle/11583/2677968/158335/SSS_IdealizedCoronary_Chiastra_0119.pdf)

### Inferences
- For a study predicting *new* plaque in plaque-free trunks, the relevant mechanism is low-TAWSS protection. That is the side where helicity looks protective. The high-WSS downside mainly concerns existing stenoses and vulnerability.
- Torsion is therefore the most *defensible* "helicity proxy" from centerline alone. The expected direction is protective, or it acts as an interaction with curvature (curvature with torsion means helical flow; curvature without torsion means more planar secondary flow and an inner-bend low-WSS region). Treat this as a pre-specified hypothesis, not established evidence.

### Gaps
- No human longitudinal study links baseline h2, or torsion, to new plaque or wall-thickness change.
- No human study found regresses h2 on curvature and torsion jointly to show torsion's independent contribution.

## Q4. How reproducible / noisy is torsion from CCTA centerlines?

### Takeaway
I found no CCTA-specific reproducibility study of coronary torsion. Torsion needs third derivatives of the centerline. Groups that report it fit smoothing splines first (free-knot regression splines in De Nisco 2021), and the angiography/IVUS literature reports less than 2.15% error on phantoms only with Fourier or polynomial fitting. Torsion is also undefined (it diverges) where curvature is near zero.

### Cited Findings
- **De Nisco 2021.** Curvature and torsion were computed only after a free-knot regression-spline fit of the VMTK centerline, to obtain a continuous, differentiable curve. — [Frontiers](https://www.frontiersin.org/articles/10.3389/fbioe.2021.731924/full)
- **SPIE 2004 (angiography + IVUS, Iowa group).** Fourier-transform and cubic-polynomial-fit estimators of coronary curvature/torsion gave average errors below 2.15% in phantom/in-vivo validation. The Fourier method needs end extensions for open curves. Not CT. — [Iowa record](https://iro.uiowa.edu/esploro/outputs/conferenceProceeding/Curvature-and-torsion-estimation-for-coronary-artery/9984186694002771); [REDI record](https://redi.cedia.edu.ec/document/104623)
- **Zhang 2024.** Torsion was computed from raw VMTK centerlines; no smoothing is described. This may partly explain the null torsion result. — [ar5iv](https://ar5iv.labs.arxiv.org/html/2312.00257)

### Inferences
- With voxels of about 0.4-0.5 mm and stair-stepped centerlines, raw discrete torsion will be dominated by noise. A practical, defensible choice would be:
  - smoothing-spline or Savitzky-Golay fitting with a fixed physical bandwidth (a few mm);
  - reporting a **window-integrated** quantity, such as total torsion angle (∫|τ| ds) or curvature-weighted torsion (∫κ|τ| ds / ∫κ ds), instead of pointwise τ;
  - a sensitivity analysis over smoothing bandwidth.
- Curvature-weighted torsion also handles the instability of τ where κ ≈ 0.
- Phase (motion) and centerline-extraction differences across baseline/FU scans add noise. Only baseline geometry is needed for prediction, though.

### Gaps
- No inter-scan or inter-observer reproducibility data (ICC/CoV) found for coronary torsion on CCTA.
- No study found on the sensitivity of torsion to spline bandwidth in coronaries.

## Summary recommendation for the fourth feature (inference, not a cited finding)
Choose a **window-level, smoothed torsion measure**, e.g. curvature-weighted mean |torsion| or total torsion angle per proximal/mid/distal window. Reasons:
1. It is the centerline descriptor with a published mechanistic link to helical flow (swine r = 0.64). Helical flow is in turn linked to higher TAWSS and less wall growth (swine, longitudinal).
2. It is geometrically orthogonal to curvature by construction: non-planarity vs bending. Tortuosity index or sum-of-angles largely duplicate mean turning angle.
3. It gives a falsifiable directional hypothesis: protective, possibly as a modifier of the curvature effect.

Caveats to state honestly:
- Human evidence is cross-sectional and was null for tree-mean torsion (Zhang 2024, p = 0.247).
- No human longitudinal study exists.
- Noise from the third derivative must be handled by pre-specified smoothing.

Note: "Kaewchoay" and "Xie et al." from the brief were not retrieved in this session, so no claims are made about them.
