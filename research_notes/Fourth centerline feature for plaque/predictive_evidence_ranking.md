# Predictive evidence for geometric coronary features (future plaque / low WSS) — choosing a 4th centerline feature

Scope note: about 18 tool calls. Several key full texts (MDPI Diagnostics 2022 geometry review, R Soc Open Sci 2024 curvature paper) returned HTTP 403, so the findings below come from abstracts, PMC full texts, and the full text of the 2025 Shen/Beier/Wentzel/Morbiducci review (arXiv 2507.17109), which I extracted locally. I found no serial-CCTA study in which purely geometric centerline features of plaque-free segments predicted **new** plaque. The best longitudinal-type geometric evidence is lesion-level and comes from ACS outcomes, not new plaque.

## 1. Longitudinal / serial-imaging studies where baseline geometry predicted future plaque, progression or events

### Takeaway
The only robust human study in which baseline CCTA geometry predicted a future outcome is Han et al. (JAMA Cardiol 2022, ICONIC). In that study **short distance from the ostium**, **bifurcation involvement** and **tortuosity** each predicted which lesions later caused ACS, and adding them raised the AUC from 0.733 to 0.766. Curvature–plaque links in IVUS and CCTA-CFD work are mostly cross-sectional. No serial study isolated torsion, tapering or eccentricity as predictors of new plaque.

### Cited Findings
- **Han D et al., JAMA Cardiology 2022;7(3):309–319 (ICONIC substudy of CONFIRM).** Nested case-control with baseline CCTA (≥64-detector, Autoplaque 2.5). 116 ACS patients, 116 propensity-matched controls, 548 lesions (116 culprit precursors, 432 nonculprit). Median CCTA-to-ACS time was 29 days. — [JAMA Cardiol](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
  - Feature definitions: "short distance from ostium" = below the median (<39 mm LCA, <60 mm RCA); bifurcation = side-branch origin within the lesion; tortuosity = one bend >90° or three curves of 45–90° within the lesion. — [JAMA Cardiol](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
  - Culprit vs nonculprit: median distance from ostium 35.1 vs 44.5 mm (P<.001); bifurcation 73.3% vs 38.9%; tortuosity 4.3% vs 1.4% (P=.046). — [JAMA Cardiol](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
  - Multivariable Cox HRs vs nonculprit lesions: short distance HR 2.71 (1.73–4.24); bifurcation HR 2.14 (1.39–3.29); tortuosity HR 2.31 (1.01–5.27); 1 adverse geometric characteristic (AGC) HR 2.90 (1.38–6.08); ≥2 AGCs HR 6.84 (3.33–14.04). — [JAMA Cardiol](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
  - Vs matched controls: short distance HR 1.55 (1.02–2.33); bifurcation HR 2.63 (1.77–3.92). Tortuosity was not reported as significant in this comparison. — [JAMA Cardiol](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
  - AUC: stenosis + adverse plaque characteristics 0.712; + quantitative plaque 0.733; + AGCs 0.766 (bootstrap optimism-corrected). None of the 40 lesions without adverse plaque characteristics or AGCs became culprits. — [JAMA Cardiol](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
  - Caveats stated: post hoc analysis; tortuosity was rare (<5%) and probably underpowered; WSS not assessed; population had extensive atherosclerosis. — [JAMA Cardiol](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
- **Serial-CCTA review (36 studies).** Baseline quantitative plaque features predicted progression and MACE better than qualitative ones. Geometry was not a focus. — [PubMed 34997285](https://pubmed.ncbi.nlm.nih.gov/34997285/)
- **KJR review of quantitative CCTA.** In a serial CCTA cohort of 1,478 patients, proximal lesions showed more lipid-rich plaque and faster progression. This supports position (distance from ostium) as a progression factor. — [KJR 10.3348/kjr.2023.1311](https://kjronline.org/DOIx.php?id=10.3348%2Fkjr.2023.1311)
- **PROSPECT (IVUS).** Predictors were plaque-level, led by plaque burden ≥70% (adjusted HR 5.3). Later analyses added **proximal location** and **large vessel size**. Vessel curvature was not a predictor in PROSPECT. — search summary of [Yonsei repository / PROSPECT literature](https://ir.ymlib.yonsei.ac.kr/handle/22282913/188325?mode=full). This is secondary; verify against the primary PROSPECT papers.
- **Candreva A et al., J Cardiovasc Transl Res 2024;17(4):893–900.** An automated 3D measure of luminal narrowing (Minimum Lumen Ratio, the abruptness of proximal narrowing) was a strong indicator of future MI. This applies to already-narrowed segments, not plaque-free ones. — cited in [Shen et al. review, arXiv 2507.17109](https://arxiv.org/abs/2507.17109)
- **Wahle A et al., Med Image Anal 2006 (IVUS + angiography fusion, 48 segments, cross-sectional).** Plaque was thicker on the inner curve, and circumferential plaque thickness correlated more strongly with **local curvature** than with CFD WSS. — [Wahle 2006 PDF](https://user.engineering.uiowa.edu/~awahle/WahLIT/Papers/wahl06a-cfd.pdf)
- **Zhang M, Gharleghi R, Shen C, Beier S, R Soc Open Sci 2024;11:241267.** 3D models derived from ASOCA (CTCA, 39 left coronary trees per the review's Table I). Of BA, torsion, inflow angle, diameter, curvature and Finet's ratio, **curvature was the only geometric parameter that differed between stenosed and non-stenosed arteries**. The authors propose curvature + OSI as plaque-onset markers. Cross-sectional CFD. — [R Soc Open Sci](https://royalsocietypublishing.org/rsos/article/11/9/241267/92655/A-new-understanding-of-coronary-curvature-and); [arXiv preprint 2312.00257](https://arxiv.org/pdf/2312.00257); table entry in [Shen et al. 2025 review](https://arxiv.org/abs/2507.17109)
- **Angiographic tortuosity cohorts (cross-sectional, invasive coronary angiography).** Li et al. 2011 (n=1010): severe CAD was located in vessels with *low* tortuosity (p=0.045); tortuosity correlated negatively with atherosclerosis and had no correlation with MACE. Chiha et al. 2017 (n=870): women with severe tortuosity were more likely to have normal coronaries (p=0.03). — Table I of [Shen et al. 2025 review](https://arxiv.org/abs/2507.17109)
- **Serial IVUS ML on geometry.** A data-driven study trained a model on baseline IVUS geometric descriptors to predict change in percent atheroma volume. Which descriptors were used (and whether curvature or torsion were among them) was not visible. — [PMC10794448](https://pmc.ncbi.nlm.nih.gov/articles/PMC10794448/)

### Inferences
- Of the purely geometric features, **position along the vessel (distance from ostium)** has the strongest prospective human evidence (HR about 1.5–2.7), followed by bifurcation proximity. The thesis already encodes position through its proximal/mid/distal windows. If distance from ostium is fitted as a continuous covariate, it would largely duplicate the window indicator rather than add new shape information.
- Tortuosity as an outcome predictor is inconsistent: a positive HR in Han 2022 (rare, wide CI), but negative or null associations in the angiographic cohorts of Li 2011 and Chiha 2017.
- The evidence for curvature comes from cross-sectional studies, yet it is the most consistently reported shape factor. It is a reasonable anchor feature.

### Gaps
- No serial CCTA study was found that predicts **new plaque in plaque-free segments** from centerline geometry (curvature, torsion, tapering, eccentricity). Thondapu, Kashyap, Shi, Bulant and Antoniadis serial studies use CFD WSS, not geometry-only predictors, as far as the searches showed. Their full texts were not retrieved.
- The full text of the MDPI Diagnostics 2022 review (geometry vs plaque burden on CCTA) was blocked (403).

## 2. Geometry-to-WSS surrogate / correlation studies: which geometric inputs explain low WSS?

### Takeaway
In surrogate and correlation studies, **vessel radius/diameter (calibre and its variation)** and **curvature** are the dominant geometric determinants of WSS. Finet's ratio (diameter-ratio family) matters at the left main bifurcation. Bifurcation angle has a minor, interdependent effect. Torsion has almost no supporting evidence.

### Cited Findings
- **Alamir et al. (PMC11345599), U-net WSS surrogate.** 50 real stenosed coronaries (40 train, 10 test) + 550 synthetic. Integrated-gradients feature importance over 17 inputs: **"radius and inlet velocity are the most important features."** Menger curvature was not highlighted as significant in the Discussion but was kept in the top-6 subset (velocity, radius, θ, curvature, tangential-y, normal-z). The subset gave MAE 2.28 Pa (NMAE 6.84%) vs full set MAE 2.01 Pa (6.03%). The paper contradicts itself on the importance of the curvature-vector components. — [PMC11345599](https://pmc.ncbi.nlm.nih.gov/articles/PMC11345599/)
- **Gharleghi R et al., Sci Rep 2025;15:254 (arXiv 2401.12504).** 127 CTCA left main bifurcations without significant stenosis; 11 anatomical features vs adverse haemodynamics. **Finet's ratio** correlated with low TAESS (p<0.001) and independently with RRT (p<0.01). **Vessel diameters** correlated with high OSI (p<0.001) and independently with RRT. **Curvature** correlated with high OSI (p<0.001), and daughter-branch curvature independently with RRT. Bifurcation and inflow angle were not reported as significant. Combined features matched haemodynamics better than single ones, and the curvature effect depends on local calibre. — [arXiv 2401.12504](https://arxiv.org/abs/2401.12504v1); [Shen et al. 2025 review](https://arxiv.org/abs/2507.17109)
- **Gharleghi et al., ISBI 2020 DL surrogate.** TAWSS in 127 LM bifurcations from radii, bifurcation angles and curvature; CV MAE 0.0407 Pa. This is secondary reporting, and no per-feature importance was found. — [ResearchGate](https://www.researchgate.net/publication/341582470_Deep_Learning_for_Time_Averaged_Wall_Shear_Stress_Prediction_in_Left_Main_Coronary_Bifurcations)
- **Kashyap et al. 2022 (127 CTCA LM bifurcations).** Comparing tortuosity index, absolute curvature, squared curvature and squared-derivative curvature, **average absolute curvature had the strongest correlation with low TAESS** and was recommended over the tortuosity index. — Table I and text of [Shen et al. 2025 review](https://arxiv.org/abs/2507.17109)
- **Malvè et al. 2020 (PMC7574594; 8 patients, CT, steady CFD).** Only **LM–LAD tortuosity** correlated with low-WSS amplitude in the proximal LAD (R²=0.719, p=0.008). Branch angles, area ratios, radius and radius of curvature did not correlate. LM–LCx tortuosity was weaker (R²=0.421, p=0.082). The sample is very small. — [PMC7574594](https://pmc.ncbi.nlm.nih.gov/articles/PMC7574594/)
- **Zhu/cataloguing study 2009 (LAD and RCA).** Curvature, torsion and tortuosity vary by segment; the LAD has higher torsion than the RCA; in the LAD all three are highest distally. Descriptive only, with no outcome. — [PMC2759354](https://pmc.ncbi.nlm.nih.gov/articles/PMC2759354/)
- **PI-GNN WSS surrogate (Sci Rep 2026).** Inputs include curvature, local angle and stenosis eccentricity, semi-axes and offset (1000 synthetic stenoses from 40 CT geometries). No feature ranking was retrieved. — [Nature Sci Rep](https://www.nature.com/articles/s41598-026-47410-z)

### Inferences
- If low WSS is the mechanistic target, the geometric surrogate evidence ranks roughly: **local calibre / diameter variation (radius, tapering, Finet-type ratios) ≈ curvature > tortuosity index > bifurcation angle > torsion**.
- Radius dominates surrogate importance partly because WSS scales roughly with Q/r³. In a geometry-only model without flow, the *relative* change in radius along the window (tapering/expansion) is likely more informative than absolute radius, which partly encodes body size and dominance.

### Gaps
- No surrogate study was found that ranks **torsion**, **tapering**, or **cross-sectional ellipticity** explicitly against curvature in plaque-free vessels.

## 3. Reviews ranking geometric risk factors

### Takeaway
The most recent comprehensive review (Shen, Gharleghi, Wentzel, Morbiducci, Chatzizisis, Serruys, Beier et al., arXiv 2507.17109, 2025) concludes that bifurcation angle has minor isolated influence, curvature is a "crucial factor for disease onset", and diameter / Finet's ratio are important but understudied. It treats tortuosity findings as contradictory because of inconsistent definitions.

### Cited Findings
- "The magnitude of the angulations between branches showed a minor influence on haemodynamics compared to the effects of other shape factors". The effect of bifurcation angle "is interdependent to other geometrical features and has minimal effects when isolated" (citing Beier et al. and Chiastra et al. 2017). — [Shen et al. 2025](https://arxiv.org/abs/2507.17109)
- "Among all investigated features, curvature was a crucial factor for the disease onset". "When considering the entire coronary artery tree, the curvature showed more influences on haemodynamics". — [Shen et al. 2025](https://arxiv.org/abs/2507.17109)
- "Diameter and its variation are important shape factors that have yet to be studied in detail". FR "strongly correlated with low TAESS (p<0.001)". There is an "interdependent effect between diameter and curvature". — [Shen et al. 2025](https://arxiv.org/abs/2507.17109)
- Tortuosity/curvature: "contradictory or inconclusive findings"; "the definition of tortuosity and curvature overlaps in some literature". Mean absolute curvature is recommended. — [Shen et al. 2025](https://arxiv.org/abs/2507.17109)
- Consensus mechanism: chronically low, oscillatory WSS at outer bifurcation walls and inner walls of bends is the strongest local risk factor. — [Curr Atheroscler Rep 2022](https://link.springer.com/article/10.1007/s11883-022-00993-0)

### Inferences
- The review literature supports curvature and bifurcation features as a starting set, but flags **diameter variation** as the main under-exploited geometric factor. That points to a calibre-change feature (tapering) as the complement.

### Gaps
- The review gives no quantitative ranking (importances, ORs) across features. Its conclusions are narrative syntheses of mostly cross-sectional CFD work.

## 4. Practical: which candidate is least redundant with curvature, bifurcation angle and diameter ratio, and is best supported?

### Takeaway
**Recommendation: a per-window lumen tapering / calibre-change feature** (e.g., normalised radius gradient dr/ds ÷ r̄, or the ratio of distal to proximal window radius, which captures tapering vs expansion). It has the strongest surrogate support (radius is the top geometric importance in WSS ML; diameters correlate with OSI/RRT), it is flagged by reviews as under-studied, and it is mathematically independent of centerline curvature and angles. In plaque-free trunks it is not confounded by stenosis. Runner-up: distance from ostium / side-branch proximity. It has the best prospective outcome evidence (HR 2.71), but the proximal/mid/distal window design already largely captures it. Tortuosity and torsion are weak choices: tortuosity is redundant with curvature, and torsion has essentially no outcome or surrogate evidence.

### Cited Findings (supporting the ranking)
- Radius was the most important geometric WSS input (integrated gradients). — [PMC11345599](https://pmc.ncbi.nlm.nih.gov/articles/PMC11345599/)
- Diameters correlated with high OSI (p<0.001) and RRT independently of the other features. Curvature effect depends on calibre. — [arXiv 2401.12504](https://arxiv.org/abs/2401.12504v1); [Shen et al. 2025](https://arxiv.org/abs/2507.17109)
- Tortuosity index is outperformed by mean absolute curvature as a correlate of low TAESS, so it is largely redundant with mean curvature / turning angle. — [Shen et al. 2025 (Kashyap 2022)](https://arxiv.org/abs/2507.17109)
- Torsion was included in Zhang 2024 but did not differ between stenosed and non-stenosed arteries (only curvature did). — [R Soc Open Sci 2024](https://royalsocietypublishing.org/rsos/article/11/9/241267/92655/A-new-understanding-of-coronary-curvature-and)
- Distance from ostium: HR 2.71 (lesion level, ACS) and HR 1.55 vs matched controls. — [JAMA Cardiol 2022](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
- Proximal lesions progress faster on serial CCTA (n=1,478). — [KJR](https://kjronline.org/DOIx.php?id=10.3348%2Fkjr.2023.1311)
- Bifurcation angle has minimal isolated effect. — [Shen et al. 2025](https://arxiv.org/abs/2507.17109)

### Inferences (redundancy assessment; my reasoning, not directly measured in a paper)
| Candidate | Redundancy with curvature / BA / diameter ratio | Evidence strength | Verdict |
|---|---|---|---|
| Tapering / lumen expansion (radius gradient) | Low vs curvature and BA. Moderate vs daughter diameter ratio only at the bifurcation itself; along trunk windows it is distinct | Surrogate (radius top), CFD correlation (diameters → OSI/RRT), review flagged | **Best 4th feature** |
| Distance from ostium / bifurcation | Collinear with the window index (prox/mid/distal) | Best prospective outcome evidence (HR 1.5–2.7) | Use as a stratifier or offset if windows are pooled; otherwise already captured |
| Tortuosity index | High vs mean turning angle / curvature | Contradictory outcome data; weaker WSS correlate than mean curvature | Avoid |
| Torsion | Low redundancy, but noisy to estimate from CCTA (third derivative of the centerline) | No outcome or surrogate support found | Avoid with few events |
| Murray / Finet deviation | High vs daughter diameter ratio | Finet strongly tied to low TAESS (LM bifurcation) | Redundant with existing feature |
| Take-off / inflow angle | Moderate vs BA | Not significant in Gharleghi 2025 | Low priority |
| Cross-sectional eccentricity / ellipticity | Low | Evidence is mainly for stenotic lesions (post-stenotic flow), not plaque-free lumen; sensitive to CCTA resolution | Low priority for plaque-free trunks |
- With few events, a 4th feature should be robust to CCTA segmentation noise. Radius gradient over a 1–3 cm window is more stable than torsion or ellipticity.
- Caveat: absolute radius correlates with sex and body size, and in the RCA with dominance. Use normalised tapering, not raw radius. CGPS has `male` and BSA, and `ct_cag` dominance appears to be present per the data notes, if adjustment is needed.

### Gaps
- No head-to-head study measured the correlation (redundancy) between tapering and curvature in coronary centerlines. The redundancy table above is reasoned, not cited.
- No study was found that tests tapering as a predictor of **new** plaque in serial CCTA. This would be a novel contribution, not a replication.
