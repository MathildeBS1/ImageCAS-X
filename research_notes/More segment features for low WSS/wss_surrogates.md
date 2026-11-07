# Geometric descriptors as WSS surrogates in coronary arteries (no CFD)

Scope note: 19 tool calls. Primary full texts read: Kashyap et al. 2022 (Sci Rep, PMC), Gharleghi et al. 2025 (Sci Rep; read as arXiv v1 preprint), Zhang et al. (arXiv 2312.00257, listed as CMPB), Sarkhosh et al. 2025 (Front Physiol), van der Giessen et al. 2011 (J Biomech, abstract page), Shen et al. 2025 review (arXiv preprint 2507.17109, text extracted locally). Everything else is from search snippets and is marked as such.

A methods caveat that applies to almost every study below: none had patient-specific flow. Inflow is either scaled from inlet diameter (Q = 1.43·D^2.55, the "Doriot fit") or set to a uniform velocity, with 0 Pa or constant-pressure outlets. Any "geometry explains WSS" result therefore partly reflects how diameter entered the boundary conditions.

## Q1. ML / reduced-order WSS surrogates: which geometric inputs mattered?

### Takeaway
The coronary deep-learning surrogates I found take the raw geometry as input (point clouds, meshes, centreline plus radius) and report only overall error (NMAE about 2.5 to 10%). None reports feature importance or ablations by named descriptor (curvature, taper, diameter). So they show that geometry determines CFD WSS under fixed generic boundary conditions, but they do not say which descriptor carries the information. Most are trained mainly or entirely on synthetic geometries.

### Cited Findings
- Gharleghi et al. 2020 (ISBI, conference paper): a U-net predicting TAWSS in the left main bifurcation reached NMAE 10.38% (SD 0.56%). It was trained on 3,429 cases, of which 127 were patient-specific and 3,302 synthetic. Figures come from a secondary citation. — [Alamir et al. 2024, Front Bioeng Biotechnol](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11345599/); reference details in the [Shen et al. 2025 review (arXiv preprint)](https://arxiv.org/pdf/2507.17109)
- Gharleghi, Sowmya & Beier 2022 (Comput Methods Programs Biomed 225:107013) extended this to transient WSS in coronary bifurcations with CNNs. I did not read the full text, so no accuracy numbers are given here. — [Shen et al. 2025 review (preprint)](https://arxiv.org/pdf/2507.17109)
- Sarkhosh et al. 2025 (Front Physiol) used **1,800 synthetic, idealised healthy LM bifurcations**. The varied parameters were LM diameter (2.18–4.18 mm), LAD and LCx diameters (1.5–3.5 mm), the LM–LAD angle (112.75–172.75°) and the LAD–LCx angle (15–130°). The input was a 4,096-node point cloud and the output TAWSS per node. Test MRE was about 11.3% (±5.5) and NAME 2.5%. Local errors reached about 20% at one LAD point, and the model underestimated LCx TAWSS near the carina. No effect of the diameters on TAWSS is quantified. LCx TAWSS rose with bifurcation angle α and plateaued above about 110°, which contradicts the prior work the paper itself cites ("wider angle → lower WSS"). — [Sarkhosh et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11920710/)
- Su et al. 2020 compared MLP, multivariate linear regression and CNN for WSS on **2,000 idealised** single-artery coronary models. Inputs were centreline coordinates plus distance and angle relative to the centreline. This comes from secondary citations only; I did not read the original. — [Suk et al. 2021, arXiv preprint](https://arxiv.org/pdf/2109.04797)
- Liu et al. (EMBC 2021, Randles group) fitted a CART regression tree on **synthetic** CFD data to predict TAWSS from lesion geometry (bifurcation angle, lesion length, severity). The tree is "interpretable", but the snippet showed no ranking of features. — [par.nsf.gov](https://par.nsf.gov/servlets/purl/10616000); [Duke](https://fds.duke.edu/db/pratt/BME/faculty/amanda.randles/publications/361777)
- Alamir et al. 2024 applied a U-net to WSS in stenosed coronaries from real patients. — [Front Bioeng Biotechnol](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11345599/)
- The Shen et al. 2025 review (arXiv preprint, Beier/Wentzel/Morbiducci/Serruys group) says angulation "showed a minor influence on haemodynamics compared to the effects of other shape factors". It reports interdependent effects of bifurcation characteristics, curvature and branch diameter. It says "diameter and its variation are important shape factors that have yet to be studied in detail". — [Shen et al. 2025 (preprint)](https://arxiv.org/pdf/2507.17109)

### Inferences
- No surrogate study gives a ranked list of named descriptors. Even so, the inputs these models need (centreline position plus local radius along the vessel) are what the tracer produces. This supports the idea that the tracer output contains the information CFD would use under generic boundary conditions. It does not show that any small set of scalar per-segment summaries keeps that information.
- Surrogate accuracy is measured against CFD that uses generic, diameter-scaled boundary conditions. It shows nothing about agreement with in-vivo WSS.

### Gaps
- I could not find Itu et al., Li et al., Ferdian et al. or Morales Ferez et al. as coronary geometry-to-WSS surrogates with feature importance. To my knowledge, WSSNet (Ferdian) works on aortic 4D-flow MRI, and Itu et al. is mainly an ML surrogate for FFR (pressure), not WSS. I did not verify either in this session.
- I found no SHAP, permutation-importance or ablation study for coronary WSS surrogates.

## Q2. Regression/correlation of WSS metrics on geometry: how much variance do curvature and taper explain, and what else adds?

### Takeaway
In the most relevant patient-specific cohort (127 plaque-free, zero-CAC CTCA patients, LM bifurcation), a single curvature metric explains only about 6–23% of the variance in % area with low TAWSS. Curvature explains none of it in the multivariable model of the same cohort, where Finet's ratio, a diameter-ratio index, dominates (univariable β = −0.84; model R² = 0.79). Diameters dominate OSI and RRT. Bifurcation angle and inflow angle add little. Taper was not tested as a separate descriptor in any study I found.

### Cited Findings
- **Kashyap et al. 2022, Sci Rep** (n = 127 symptomatic patients, no obstruction, CAC = 0, LM bifurcation with LAD and LCx): adjusted R² of each tortuosity metric against % area with TAWSS < 0.4 Pa —
  - Average absolute curvature: LM 0.196, LAD 0.232, LCx 0.061, whole bifurcation 0.112 (all p ≤ 0.013).
  - RMS curvature: LM 0.113, LAD 0.164, LCx 0.010 (n.s.), whole 0.093.
  - Average squared-derivative curvature: LM 0.086, LAD 0.160, LCx 0.007 (n.s.), whole 0.101.
  - Tortuosity index (L/C): about 0, p = 0.66–0.87.
  - The Discussion states 6–27%, but no table value reaches 27%, which is a likely internal inconsistency.
  - Diameter and bifurcation angle were not tested. Inflow was scaled with the diameter law ("q = 1.43·d^1.55" as written in the paper) and the outlets had 0 pressure.
  — [Kashyap et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- **Gharleghi et al. 2025, Sci Rep** (same 127-patient cohort; numbers read from the arXiv v1 preprint, so the published version may differ). Eleven anatomical parameters were tested: curvature, diameter of LM, LAD and LCx, angles A and B, inflow angle, and Finet's ratio. Standardised univariable β (p):
  - %lowTAESS: Finet's ratio −0.842 (<0.001). The LAD diameter (0.160, p = 0.07) and LCx diameter (0.172, p = 0.05) were borderline. All curvatures were n.s. (LM 0.094, LAD 0.006, LCx −0.112), and so were all angles.
  - %highOSI: diameters 0.69–0.74 (all <0.001) and curvatures −0.37 to −0.52 (all <0.001).
  - %highRRT: diameters 0.40–0.54, Finet −0.49 and LCx curvature −0.37 (all <0.001).
  - Step-down multiple regression R²: %lowTAESS 0.791, %highOSI 0.633, %highRRT 0.585. Finet's ratio and LM diameter were retained in all three, and angle A in several. Coefficient-to-column mapping was ambiguous in the extracted text.
  - Boundary conditions: **uniform inlet velocity**, 0 Pa at both outlets.
  — [Gharleghi et al. arXiv 2401.12504](https://arxiv.org/html/2401.12504v1); published version listed at [UNSW](https://research.unsw.edu.au/people/associate-professor-susann-beier/publications?page=0)
- The Shen et al. 2025 review summarises the above as "FR strongly correlated with low TAESS (p < 0.001)", with combined factors fitting better than single ones. — [Shen et al. 2025 (preprint)](https://arxiv.org/pdf/2507.17109)
- **Zhang et al. (arXiv 2312.00257, listed as CMPB)**: 39 ASOCA left coronary trees (20 non-stenosed, 12 moderate, 7 severe). Inflow was scaled as Q = 1.43·D^2.55 with a D^2.27 flow split.
  - Mean curvature was higher in stenosed trees (1.321 vs 1.230, p = 0.024), with AUC 0.711 (0.543–0.844).
  - %HighOSI gave AUC 0.813.
  - Curvature correlated with diameter, r = −0.474 (p = 0.002).
  - No R² and no multivariable model. Small n, and the paper has internal labelling errors. This is a cross-sectional case–control design, not incident disease.
  — [Zhang et al.](https://ar5iv.labs.arxiv.org/html/2312.00257)
- Zhang et al. 2024 (R Soc Open Sci): "When considering the entire coronary artery tree, the curvature showed more influences on haemodynamics". This is the review's summary; I did not read the paper. — [Shen et al. 2025 (preprint)](https://arxiv.org/pdf/2507.17109)
- **De Nisco et al. 2018, Ann Biomed Eng** (30 swine coronaries): unfavourable WSS was inversely associated with helicity intensity (r = −0.91), and torsion drove helical-flow features (r = 0.64). From search snippets; the full text was blocked (403). The 2020 Atherosclerosis follow-up found that high baseline helicity was associated with higher WSS magnitude and less wall-thickness growth. — [Polito repository listing](https://iris.polito.it/handle/11583/2726967)
- Earlier synthetic or small studies (from the review's table):
  - Beier et al. 2016: 9 LM models; bifurcation angle had no significant effect.
  - Shen et al. 2021 (J Biomech): 128 idealised and modified geometries; large curvature led to asymmetric secondary flow and low TAESS, larger bifurcation angle reduced low-TAESS area, and the factors were interdependent.
  - Chiastra et al. 2017 (J Biomech): bifurcation shape and hemodynamic risk.
  — [Shen et al. 2025 (preprint)](https://arxiv.org/pdf/2507.17109)
- Lesion-level work (104 patients, diseased): stenosis severity and lesion length were independent predictors of abnormal shear, while eccentricity was not. From a search snippet only. — [ScienceDirect abstract](https://www.sciencedirect.com/science/article/abs/pii/S0268003318306910)
- A 2009 geometry study found that more than 80% of coronary geometric variability falls on two factors: curvature/tortuosity and torsion. This concerns geometry, not WSS. — search snippet, [Duke Scholars](https://scholars.duke.edu/publication/710959)

### Inferences
- Curvature alone is a weak WSS proxy: about 10–20% of the variance in low-TAWSS area per branch, and less in the LCx. Diameter and diameter-ratio descriptors explain much more in the same cohort. Two biases limit this. First, the R² = 0.79 is in-sample after step-down selection from more than 11 candidates with n = 127, so it is optimistic. Second, it depends on the boundary conditions. With a uniform inlet velocity and 0 Pa outlets, the flow split, and hence daughter WSS, is set by the daughter diameters. Finet's ratio and diameter will therefore predict WSS partly by construction. This is a CFD modelling result, not an in-vivo one.
- Diameter and curvature are correlated (r ≈ −0.47 in Zhang et al.). Curvature effects that ignore diameter may partly reflect vessel size.
- A local diameter descriptor not yet in the feature set (Finet's ratio at the LM, or more generally parent-to-daughter diameter ratios) has the strongest support in the CFD-surrogate literature. The LM→LAD and LM→LCx diameter ratios already in use are close relatives of Finet's ratio, which is D_LM / (D_LAD + D_LCx).
- Torsion may matter through helical flow (De Nisco). The evidence is swine data with r for helicity, not a direct regression of WSS on torsion. Torsion from a CCTA centreline is also noisy, since it needs third derivatives.
- Bifurcation and inflow angles explain little in patient-specific data, and the synthetic studies disagree on the direction of the effect.

### Gaps
- Taper (diameter change per length) was never tested as a named predictor of WSS in any study I found. "Diameter variation" is described as understudied.
- Eccentricity and area ratio have no coronary CFD regression evidence outside stenotic lesions.
- No study regresses segment-level WSS on segment-level geometry across the full tree (RCA included) in a plaque-free cohort. The LM-bifurcation results may not carry over to mid or distal segments or to the RCA.
- I could not find out how Kashyap and Gharleghi (same cohort, same group) reconcile curvature being significant for low TAWSS in one paper and not the other. The endpoint definitions differ (TAWSS < 0.4 Pa vs a TAESS threshold, uniform vs scaled inflow).

## Q3. Lumen radius (Poiseuille, WSS ∝ Q/r³) and Murray-law flow split as proxies

### Takeaway
No study validates a diameter-only "Poiseuille WSS" against CFD in coronaries. The evidence that exists covers flow-diameter scaling. Measured coronary flow scales with diameter as Q ≈ 1.43·D^2.55, with R² = 0.87 against in-vivo data. Flow split at bifurcations follows D^2.27 rather than Murray's D³, with R² = 0.70. Using Murray's D³ instead changes average WSS by about 8% and the low-WSS area near side branches by about 13%.

### Cited Findings
- van der Giessen et al. 2011, J Biomech (6 patient-specific MSCT trees, steady flow). The empirical flow split (exponent 2.27, from Doriot et al. 2000 measurements in angiographically normal arteries) was compared with Murray's law (exponent 3).
  - Murray's law underestimates side-branch flow.
  - Average WSS between side branches was 8% higher with Murray's law (range −5% to +27%).
  - The low-WSS region near bifurcations was 13% larger with the empirical model (WSS differences −12% to +68%).
  - Small n.
  — [repub.eur.nl](https://repub.eur.nl/pub/33468)
- The Doriot-fit scaling gives R² = 0.87 for inlet flow against diameter and R² = 0.70 for the daughter flow split, compared with in-vivo measurements. — [Shen et al. 2025 review (preprint)](https://arxiv.org/pdf/2507.17109), citing van der Giessen 2011
- Conflict on the exponent: Zhang et al. use Q = 1.43·D^2.55, while Kashyap et al. write q = 1.43·d^1.55. Both cite the same source. One is probably a typo or a velocity-versus-flow difference. — [Zhang et al.](https://ar5iv.labs.arxiv.org/html/2312.00257); [Kashyap et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Gosling et al. 2020 added a taper-based (Murray-law) side-branch leakage term to a 1D coronary model. It barely changed vFFR but significantly changed the estimated flow rate and coronary flow reserve. From a snippet only. — [White Rose eprints](https://eprints.whiterose.ac.uk/158322)
- Poiseuille is used as the analytical baseline WSS (steady, Newtonian, rigid cylinder) in a coronary CFD uncertainty-quantification preprint. I found no reported correlation with 3D CFD. — [arXiv 2512.11017 (preprint)](https://arxiv.org/pdf/2512.11017)
- Murray-law-based μQFR uses side-branch diameters to apportion flow (FFR, not WSS). — [Springer](https://link.springer.com/article/10.1007/s10554-023-02974-z)

### Inferences
- Combining Poiseuille WSS = 4μQ/(πr³) with Q ∝ D^2.55 gives a mean WSS ∝ D^(−0.45), which is close to constant across vessel sizes. This is my derivation from the cited scaling and is not validated. Under the flow scaling used by all of these CFD studies, absolute lumen diameter alone therefore carries little mean-WSS information. The informative signal is local deviation from the expected diameter: a segment wider than its flow predicts (WSS ∝ Q/r³ falls steeply) or a reduced flow from side-branch loss. That points to "observed / expected diameter" or diameter-ratio features rather than raw radius.
- A per-segment flow-normalised index is a reasonable feature but has not been validated against CFD. One version estimates Q in each trunk segment from the inlet diameter minus side-branch flows (D^2.27 split), then forms τ̂ = 4μQ̂/(πr³) from the mean segment radius. Its error would follow the D^2.27 versus D³ uncertainty (about 8% mean WSS, about 13% low-WSS area). It also needs side-branch diameters, which the tracer gives only per artery, so this needs checking.
- Pulsatility, secondary flow and curvature effects are absent from Poiseuille, so it cannot capture the low and oscillatory WSS at inner bends and bifurcation lateral walls. Those are the plaque-relevant regions.

### Gaps
- I found no study that correlates a diameter-only or Poiseuille WSS estimate with 3D CFD WSS in coronary arteries.

## Q4. Simple per-segment indices validated against CFD (Murray/Finet ratio, area/expected area, reference diameter ratio)

### Takeaway
The only simple index with quantitative CFD support in a patient-specific plaque-free cohort is **Finet's ratio** at the LM bifurcation. It was the strongest single predictor of % low TAESS (β = −0.84, n = 127), but that evidence comes from one group, comes partly from a preprint, and the boundary conditions make it partly circular. No per-segment "area / expected Murray area" or "flow-normalised radius" index has been validated against CFD.

### Cited Findings
- Finet's ratio, D_parent / (D_daughter1 + D_daughter2): β = −0.842 (p < 0.001) for %lowTAESS. It was also retained in the multivariable models for OSI and RRT. — [Gharleghi et al. arXiv 2401.12504](https://arxiv.org/html/2401.12504v1)
- Huo et al. 2012 (J Biomech) asked which diameter and angle rule gives optimal bifurcation flow patterns. The review cites it for an interdependent diameter–curvature effect on haemodynamics; I did not read the paper. — [Shen et al. 2025 (preprint)](https://arxiv.org/pdf/2507.17109)
- Sun & Cao 2011 (30 CTCA patients): diseased left coronaries had a larger LM–LCx bifurcation angle (94° vs 75.5°, p = 0.02) and larger LAD and LCx diameters (p < 0.001). This is cross-sectional, with no CFD. — [Shen et al. 2025 (preprint), Table I](https://arxiv.org/pdf/2507.17109)

### Inferences
- Candidate added features, in order of supporting evidence:
  1. Finet's ratio at the LM. It is cheap, and it mostly re-expresses the LM→LAD and LM→LCx ratios already in use, so it adds little new information. A sum-based Murray deviation (D_LM³ versus D_LAD³ + D_LCx³) is a related alternative.
  2. Segment mean lumen radius, or a flow-normalised radius, as a low-WSS proxy. The physics supports it, but it is unvalidated.
  3. Torsion, via helical flow. The evidence is swine data and the measure is noisy.
  4. Taper is already included. There is no direct CFD-regression evidence for it as a WSS proxy, which is a gap rather than counter-evidence.
- Any added feature costs degrees of freedom in a pre-specified LR test. Curvature explains only about 10–20% of low-WSS-area variance, and diameter-based descriptors more, under generic boundary conditions. A WSS rationale therefore favours adding one diameter-based descriptor over adding several shape descriptors.

### Gaps
- No index has been validated against in-vivo WSS or against CFD with patient-specific flow.
- No index has been validated for RCA or non-bifurcation trunk segments.
- No study links any of these geometric WSS proxies to *incident* plaque in initially plaque-free people. The Gharleghi and Kashyap cohort is plaque-free, but its outcome is CFD-derived WSS, not follow-up plaque.
