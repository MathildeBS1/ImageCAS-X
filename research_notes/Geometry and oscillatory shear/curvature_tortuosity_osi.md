# Coronary curvature, tortuosity and torsion vs oscillatory / multidirectional WSS (OSI, RRT, transWSS, TSVI)

Notes compiled 2026-11-07. "FT" = details read from full text; "ABS" = abstract or record summary only; "SNIP" = search snippet only (weakest). All CFD studies below assume rigid walls unless stated otherwise. None measured WSS in vivo; all are model outputs. No CAS-Net or Shen 2026 (arXiv) material is used.

## Q1. Which studies quantitatively relate coronary curvature/tortuosity/torsion to OSI (or RRT, transWSS, TSVI)? Direction and size?

### Takeaway
Only a handful of coronary studies report a quantitative curvature-vs-oscillatory-metric relation, and the strongest one (Gharleghi et al. 2025, 127 CAD-free CCTA left main bifurcations, pulsatile) finds curvature **negatively** associated with high-OSI and high-RRT area but **positively** associated with TSVI (standardised β about −0.37 to −0.52 for OSI, +0.25 to +0.38 for TSVI). Kashyap 2022 reports no OSI/RRT at all, and Zhang 2024 reports group differences (stenosed vs non-stenosed) in curvature, %HighOSI and TSVI side by side, not a curvature-OSI correlation.

### Cited Findings

**Kashyap et al. 2022, Sci Rep (FT)**
- Did NOT compute OSI, RRT or any oscillatory/multidirectional metric; the only shear output is TAWSS, summarised as % area < 0.4 Pa — [Kashyap 2022, PMC8764056](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Flow was pulsatile (initial steady solution, then 4 transient cycles, 4th analysed), rigid walls (justified by a cited <2% TAWSS change with FSI), Carreau–Yasuda blood, parabolic inlet with flow scaled q = 1.43 d^1.55, 0 Pa outlets, laminar, Re < 120 — [Kashyap 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- n = 127 patients with coronary symptoms, no obstruction, zero calcium score — [Kashyap 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Adjusted R² (p) vs low-TAWSS area, Table 4: average absolute curvature LM 0.196 (<0.001), LAD 0.232 (<0.001), LCx 0.061 (0.013), whole bifurcation 0.112 (0.001); tortuosity index LM −0.011 (0.66), LAD 0.026 (0.099), LCx 0.007 (0.28), whole −0.018 (0.865). RMS curvature and squared-derivative curvature intermediate, non-significant in LCx — [Kashyap 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- These are univariable relations; no adjustment for diameter or other anatomy reported in what was read — [Kashyap 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)

**Gharleghi et al. 2025, Sci Rep, "Assessing left main bifurcation anatomy and haemodynamics as a potential surrogate for disease risk in suspected CAD without stenosis" (FT)**
- n = 127 patients with suspected CAD, no stenosis or calcification in the epicardial coronaries (Intra Care, Auckland; GE 64-slice CTCA); 66.9% female, median age 57 — [Gharleghi 2025, PMC11697190](https://pmc.ncbi.nlm.nih.gov/articles/PMC11697190/)
- Transient (pulsatile, generic waveform scaled by LM diameter), rigid walls, no cardiac motion, Carreau–Yasuda, plug inlet, zero-pressure outlets, 4 cycles with 4th analysed; analysis within 10 mm of the LM bifurcation — [Gharleghi 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11697190/)
- "Tortuosity" here = mean centreline curvature (tortuosity index not used). Metrics: lowTAESS (<0.5 Pa), highOSI (>0.1), highRRT (>4.17 Pa⁻¹), mean TSVI; no transWSS or helicity — [Gharleghi 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11697190/)
- Curvature vs highOSI area: standardised β LM −0.367, LAD −0.484, LCx −0.519 (all p < 0.001), i.e. more curved branches had LESS high-OSI area — [Gharleghi 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11697190/)
- Curvature vs highRRT: LAD β −0.269 (adj. p 0.018), LCx −0.368 (p < 0.001), LM −0.157 (adj. p 0.552, n.s.) — [Gharleghi 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11697190/)
- Curvature vs mean TSVI: LM β +0.249 (adj. p 0.043), LAD +0.376 (p < 0.001), LCx +0.333 (adj. p 0.001), i.e. more curved = more multidirectional (TSVI) — [Gharleghi 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11697190/)
- Curvature vs lowTAESS: no significant association (all adj. p = 1) in this analysis; Finet's ratio was the strongest lowTAESS predictor (β −0.842) — [Gharleghi 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11697190/)
- Diameters were strongly associated with highOSI (β ≈ +0.69 to +0.74) and TSVI (β ≈ −0.51 to −0.58); females had smaller diameters and higher curvature, so curvature and diameter are confounded — [Gharleghi 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11697190/)
- Multivariable: backward stepwise linear regression (AIC), LAD/LCx diameters dropped a priori for collinearity; R² lowTAESS 0.791, highOSI 0.633, highRRT 0.585, meanTSVI 0.360; curvature terms retained in several models, but per-predictor coefficients in Table 3 could not be read reliably from the web text — [Gharleghi 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11697190/)
- An earlier arXiv preprint by the same group on sex differences at the LM bifurcation exists (later IEEE TBME 2025) — [arXiv 2311.18489](https://arxiv.org/pdf/2311.18489); [Europe PMC record, Gharleghi IEEE TBME 2025](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=(coronary)%20AND%20(curvature%20OR%20tortuosity%20OR%20torsion)%20AND%20(%22oscillatory%20shear%22%20OR%20%22transverse%20WSS%22%20OR%20%22relative%20residence%20time%22%20OR%20TSVI%20OR%20%22multidirectional%22)&format=json&pageSize=60&resultType=lite)

**Zhang et al. 2024, R Soc Open Sci, "A new understanding of coronary curvature and haemodynamic impact on the course of plaque onset and progression" (FT)**
- n = 39 left coronary trees from the public ASOCA dataset (20 non-stenosed, 12 moderate, 7 severe); one case excluded — [Zhang 2024, PMC11416812](https://pmc.ncbi.nlm.nih.gov/articles/PMC11416812/)
- Pulsatile (4 cycles, 4th analysed, dt 0.005 s), rigid walls, Carreau–Yasuda, generic waveform scaled by inlet diameter, diameter-based flow splits, end-diastolic geometry only — [Zhang 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11416812/)
- Metrics: TAESS, OSI, RRT = 1/[(1−2·OSI)·TAESS], TSVI (after Mazzi et al.); %HighOSI thresholds 0.1 and 0.2 — [Zhang 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11416812/)
- **No curvature–OSI, curvature–TSVI or curvature–RRT correlation coefficients are reported.** The only reported correlation is curvature vs diameter (r = −0.474, p = 0.002). The curvature–haemodynamics link is made qualitatively via group comparisons — [Zhang 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11416812/)
- Fig. 3 = side-by-side group comparisons (non-stenosed vs stenosed) of average curvature, %HighOSI@0.1 and TSVI for whole trees (20 vs 19), non-bifurcating (57 vs 14) and bifurcating segments (53 vs 12). Fig. 4 = ROC curves for the same three variables — [Zhang 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11416812/)
- Group results: curvature differs whole-tree (1.321 ± 0.131 vs 1.230 ± 0.090, p = 0.024) and non-bifurcating (p = 0.027), not at bifurcations; %HighOSI@0.1 higher in stenosed whole-tree and non-bifurcating (p < 0.001), not at bifurcations; TSVI 186 ± 40 vs 137 ± 25 whole-tree (p < 0.001), also higher at bifurcating and non-bifurcating segments — [Zhang 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11416812/)
- ROC (stenosed vs non-stenosed): TSVI AUC 0.876, %HighOSI@0.1 AUC 0.813 (cut-off 0.006, i.e. 0.6% of area), curvature AUC 0.711 — [Zhang 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11416812/)
- Moderate vs severe: only %LowTAESS@0.5 Pa (p = 0.009) and %HighRRT@2.5 Pa⁻¹ (p = 0.012) differed; %HighOSI (p = 0.665), TSVI (p = 0.114) and curvature did not — [Zhang 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11416812/)
- No multivariable adjustment; sex (60% female non-stenosed vs 14–17% stenosed) and age differed between groups — [Zhang 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11416812/)
- The arXiv preprint version (Dec 2023) reported curvature as the only anatomical feature differing between groups and also cautioned that OSI values were very small — [arXiv 2312.00257](https://arxiv.org/pdf/2312.00257)

**Shen et al. 2025, R Soc Open Sci, "High-intensity helical flow: a double-edged sword in coronary artery haemodynamics" (FT, first ~100k characters)**
- Same ASOCA 39 left coronary trees (20/19), pulsatile, rigid, Carreau–Yasuda, generic scaled inflow — [Shen 2025, Europe PMC PMC12324882](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12324882/fullTextXML)
- Geometry–oscillatory relations: LAD torsion vs RRT% (non-stenosed) ρ = −0.46, p = 0.049, Holm-adjusted p = 1.0; marginal-branch diameter vs RRT% ρ ≈ 0.61–0.62, adjusted p > 0.6. No curvature/torsion–OSI correlations survived correction; no TSVI results in the part read — [Shen 2025](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12324882/fullTextXML)
- Note: this is a different paper from the "Shen 2026 arXiv geometry paper" the user asked to exclude.

**Pinho et al. 2019 (two papers, ABS)**
- Left coronary, 8 patients, FSI (compliant walls): higher LM and LCx curvature and some tortuosity measures associated with less favourable haemodynamic descriptors; abstract does not state whether OSI was among them — [Pinho 2019 MBEC, DOI 10.1007/s11517-018-1904-2](https://doi.org/10.1007/s11517-018-1904-2)
- RCA, 10 healthy CT subjects, compliant model: lower tortuosity associated with more atherosclerosis-prone haemodynamics; OSI not mentioned in abstract — [Pinho 2019 CVET, DOI 10.1007/s13239-019-00403-8](https://doi.org/10.1007/s13239-019-00403-8)

**Other CFD of coronary geometry without OSI**
- Malvè et al. 2015: 8 CT LM bifurcations, **steady** CFD (so OSI cannot be computed); LM-to-LAD tortuosity index linked to low WSS in proximal LAD — [Malvè 2015, DOI 10.1007/s10439-014-1056-y](https://doi.org/10.1007/s10439-014-1056-y) (ABS)
- Johnston & Johnston 2007: 4 angiography-reconstructed RCAs, single time point (no OSI); WSS correlated strongly with reciprocal radius and only weakly with curvature; high WSS on the inside of bends — [Johnston & Johnston 2007, PubMed 17440250](https://pubmed.ncbi.nlm.nih.gov/17440250/) (ABS). The user's "Johnston & Johnston 2009" could not be identified; the 2007 PMB paper is the curvature one found.
- Ashrafee et al. 2024: Taguchi design-of-experiments on 18 LCA models derived from 2 patients; bifurcation angle or LM diameter dominant depending on metric; curvature-OSI specifics not in abstract — [Ashrafee 2024, DOI 10.1088/2057-1976/ad2f59](https://doi.org/10.1088/2057-1976/ad2f59) (ABS)

### Inferences
- The only coronary dataset that gives a direct, quantitative, partly adjusted curvature–OSI/RRT/TSVI relation is Gharleghi 2025. It appears to be the same 127-patient Auckland CAD-free cohort as Kashyap 2022 (same n, same group, same CFD pipeline), so the two are not independent evidence. This is inferred, not stated in what was read.
- Direction depends on the metric: in that cohort, curvature goes with less high-OSI/high-RRT area but more TSVI. Treating "oscillatory" and "multidirectional" as one family would hide this.
- Zhang 2024 cannot be cited as showing curvature correlates with OSI; it shows that stenosed trees have both higher curvature and higher %HighOSI/TSVI, in a 39-tree cross-sectional sample confounded by sex and age, with stenosis possibly altering both.

### Gaps
- In Zhang 2024, the ordering of the curvature means (1.321 vs 1.230) by group could not be confirmed from the extracted text; the abstract/title framing says stenosed trees were more curved. The unit "m⁻¹" in the extraction is implausible for coronaries (probably mm⁻¹ or a scaled unit); check the PDF.
- Gharleghi 2025 Table 3 (multivariable coefficients) could not be read; whether curvature survives adjustment for diameter/Finet's ratio for each metric is unconfirmed.
- Pinho 2019 full texts not read; unknown whether OSI was analysed.
- Van der Giessen et al. 2011 (J Biomech 44:1089–1095, boundary conditions in patient-specific coronary trees) was located only as a reference; its OSI/curvature content was not found. Xie/Liu idealised studies could not be identified with certainty.

## Q2. Is the evidence consistent, or is OSI small in coronaries regardless of curvature?

### Takeaway
Repeatedly, coronary CFD finds OSI very small, with high-OSI (>0.1) area typically only a few percent of the wall; authors themselves (Myers 2001, Zhang 2024, Gharleghi 2025) warn that OSI/RRT differences should be interpreted with caution. Evidence on curvature is therefore thin and not consistent in direction across metrics.

### Cited Findings
- Myers et al. 2001 (realistic rigid RCA cast-based model, steady and pulsatile): local 3D curvature strongly shaped velocity and WSS; "The oscillatory shear index was very small and was attributed to flow reversal in the waveform, rather than separation." — [Myers 2001, DOI 10.1114/1.1349703](https://doi.org/10.1114/1.1349703) (ABS)
- Gharleghi 2025: highOSI@0.1 covered 3.08 ± 2.36% of the bifurcation wall (max 12.1%); highRRT 4.84 ± 3.06%; versus lowTAESS 25.6%. Authors: OSI and RRT results "should be interpreted with caution" — [Gharleghi 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11697190/)
- Zhang 2024: OSI values generally very small (<0.4) and luminal area with adverse OSI <15%; authors urge caution; ROC cut-off for %HighOSI was 0.006 — [Zhang 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11416812/)
- Dynamic motion matters more for OSI than for TAWSS: in an MRI-derived moving RCA, TAWSS was little affected by motion while oscillatory WSS metrics were more affected — [Kandangwa 2022, Front Bioeng Biotechnol](https://www.frontiersin.org/articles/10.3389/fbioe.2022.962687); earlier Torii et al. 2010 found cardiac motion (with cyclic radius and curvature change) significantly affected instantaneous WSS and OSI — [Torii 2010, Ann Biomed Eng](https://link.springer.com/doi/10.1007/s10439-010-0008-4) (SNIP). Rigid, end-diastolic CCTA models (Kashyap, Gharleghi, Zhang, Shen) therefore likely misestimate OSI the most.
- Kandangwa et al. 2025: in moving RCA geometries, RRT accounted for about half of the anatomical variation in fatty-streak prevalence, attributed to low plus multidirectional WSS — [Kandangwa 2025, Ann Biomed Eng, PMC11782302](https://pmc.ncbi.nlm.nih.gov/articles/PMC11782302/) (ABS via Europe PMC record). This links RRT to lesion location, not to curvature directly.
- Idealised curved/dynamic tubes: time-varying curvature with oscillatory pressure gradient roughly doubled OSI in an analytic/numerical curved-tube model; a helical tube with dynamic curvature/torsion showed OSI changes up to 24% with curvature change, a larger effect than torsion — [search summary incl. PubMed 24763627](https://pubmed.ncbi.nlm.nih.gov/24763627/) (SNIP; authors/details not verified). A 2022 arXiv preprint (180° curved tube) found WSS metrics, including OSI, sensitive to inlet flow development — [arXiv 2209.08440](https://arxiv.org/pdf/2209.08440) (preprint, SNIP).
- Vorobtsova et al. 2016: idealised curved vessels with zero torsion vs 23 patient-based tortuous arteries; patient-specific tortuosity correlated strongly with helicity intensity, which raised WSS; conclusion opposite to the zero-torsion idealised case (more tortuous = lower atherosclerosis risk). OSI is not mentioned in the abstract — [Vorobtsova 2016, Ann Biomed Eng 44:2228](https://doi.org/10.1007/s10439-015-1492-3) (ABS)

### Inferences
- Because high-OSI area is a few percent and sensitive to waveform, inlet development, wall motion and thresholds, a curvature–OSI association in rigid CCTA-based CFD is fragile evidence; curvature–TAWSS and curvature–TSVI relations are better supported than curvature–OSI.
- Idealised zero-torsion models and patient-specific models can reach opposite conclusions (Vorobtsova 2016), so idealised curved-tube OSI results should not be transferred to real coronaries.

### Gaps
- No study found that relates baseline curvature-driven OSI to incident plaque in a plaque-free population over time; all coronary human evidence above is cross-sectional or model-only.
- No CCTA study found reporting transverse WSS (transWSS) vs curvature in human coronaries.

## Q3. Torsion and helical flow: does torsion/helicity reduce or raise OSI?

### Takeaway
In swine coronaries, torsion drives helical flow and helicity intensity is strongly and inversely associated with exposure to adverse (low/oscillatory) WSS, suggesting torsion is protective through helicity; but direct torsion–OSI correlations in human CCTA trees do not survive multiple-comparison correction, and one group argues high-intensity helicity is "double-edged".

### Cited Findings
- De Nisco et al. 2019: 30 swine coronary arteries (reconstructed in vivo, with measured flow per the group's standard pipeline); counter-rotating bi-helical structures; helicity intensity inversely associated with unfavourable WSS (r = −0.91, p < 0.001); vascular torsion dictates helical flow features (r = 0.64, p < 0.001) — [De Nisco 2019, Ann Biomed Eng 47:425](https://iris.polito.it/handle/11583/2726967) (ABS/SNIP; full text 403). Which WSS metric(s) make up "unfavourable WSS" (low TAWSS vs high OSI vs RRT) was not confirmed.
- De Nisco 2021: swine and human coronary CFD models gave similar WSS metrics, helical flow and anatomy, supporting transfer of the swine helicity findings — [De Nisco 2021, Front Bioeng Biotechnol](https://doi.org/10.3389/fbioe.2021.731924) (ABS)
- Vorobtsova 2016: tortuosity (with torsion from heart shape) correlated with helicity intensity, which increased WSS; authors stress modelling torsion — [Vorobtsova 2016](https://doi.org/10.1007/s10439-015-1492-3) (ABS)
- Shen 2025 (39 ASOCA trees, rigid): helicity intensity h2 correlated with higher TAESS; in stenosed trees with both less low-TAESS and more high-TAESS area; no helicity–OSI correlations reported; torsion–RRT (LAD) ρ = −0.46 unadjusted, not significant after Holm correction — [Shen 2025](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12324882/fullTextXML)
- Idealised dynamic helical tube: changing curvature affected OSI more (up to 24%) than changing torsion — [PubMed 24763627](https://pubmed.ncbi.nlm.nih.gov/24763627/) (SNIP)

### Inferences
- Direction, where measured, is that torsion → more helicity → less low/oscillatory WSS; the evidence base is mainly one swine cohort (n = 30) plus non-significant human trends.
- For a CCTA tracer-based thesis, torsion is noisier to estimate than curvature (third derivative of the centreline), so the weak human torsion results may partly reflect measurement noise (inference, not tested in these sources).

### Gaps
- De Nisco 2019 full text not accessible (403); exact metric definitions and per-artery correlations not verified.
- No human CCTA study found that reports torsion vs OSI with an adjusted analysis.
- Other vascular beds (carotid, aorta) were not searched in depth; not needed for the coronary question.
