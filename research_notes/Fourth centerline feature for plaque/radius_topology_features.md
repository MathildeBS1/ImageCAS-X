# Radius/diameter- and topology-based centerline features as predictors of low WSS and coronary plaque (excluding curvature, bifurcation angle, daughter diameter ratio)

Scope note: evidence collected via WebSearch, WebFetch and Europe PMC abstracts (PubMed/PMC pages were blocked by a captcha, so several items are abstract-level only). Study design is flagged as [human CFD], [human clinical], [idealized] or [postmortem]. No source reported here studied a baseline plaque-free CCTA cohort with new plaque at follow-up as the endpoint, so every feature is an extrapolation to the thesis design.

## Q1. Which radius-based feature most consistently predicts low WSS (local lumen size/expansion, tapering, Murray deviation)?

### Takeaway
The most consistent and best-quantified geometric determinant of WSS in human coronaries is **local lumen radius itself (and therefore local expansion/narrowing relative to the expected radius)**. WSS scales strongly with 1/r; in plaque-free CCTA vessels larger segments have about 3x lower ESS than small ones, and lumen diameter outweighs curvature. At bifurcations the parallel quantity is the **area expansion ratio** (sum of daughter areas / mother area). In idealized CFD it is the main driver of the size of the low-WSS region, and it does NOT depend on the daughter-to-daughter diameter ratio. No study isolating **tapering rate** as a WSS predictor in human coronaries was found.

### Cited Findings
- [human CFD, n=4 RCAs from biplane angiography] WSS patterns depend on lumen diameter and curvature. There is "a strong correlation between WSS and reciprocal radius and a weaker correlation between high curvature and extremes of WSS". A low-WSS region proximal to the acute margin matches where RCA atherogenesis is preferentially found. — [Johnston & Johnston 2007, Phys Med Biol, PMID 17440250](https://doi.org/10.1088/0031-9155/52/9/013)
- [human CCTA CFD, 349 normal (plaque-free) vessels, 168 patients] ESS was evaluated per 3-mm segment. By lumen-diameter tertile: small (<2.6 mm), intermediate (2.6–3.2 mm) and large (>=3.2 mm) segments had minimal ESS of 3.8 vs 1.7 vs 1.2 Pa and maximal ESS of 6.0 vs 2.6 vs 2.0 Pa (p<0.001). ESS correlated with distance from the ostium (rho 0.22–0.62, p<0.001). By vessel, ESS was highest in the LAD > LCX > RCA (minimal ESS 2.3 vs 1.9 vs 1.6 Pa). Men had lower ESS than women even after adjusting for lumen diameter. "CCTA-based ESS values increase rapidly and become widely scattered with decreasing lumen diameter." — [Schultz et al. 2023, Int J Cardiovasc Imaging, PMID 36255544](https://doi.org/10.1007/s10554-022-02739-0)
- [human CCTA CFD, 80 patients, stenotic segments] Small lumen, proximal location, high pressure gradient and short lesion length were independent determinants of WSS. — [search-result summary of a 2016 CT-CFD study (Heart/BMJ); exact effect sizes not retrieved](https://heart.bmj.com/content/102/20/1655)
- [idealized CFD, left coronary bifurcation] "The main factor leading to large regions of low WSS is the so called expansion ratio, a relation between the cross section areas of the outflow branches and the cross section area of the main branch. Large regions of low WSS appear for high expansion ratios." The size of the low-WSS region was independent of the ratio between the outflow-branch diameters. Murray-compliant bifurcations have expansion ratios of 1–1.25, which is still not small enough to prevent low WSS. — [Doutel et al. 2016, J Theor Biol, PMID 27157126](https://doi.org/10.1016/j.jtbi.2016.04.038)
- [idealized/finite-element CFD with cast-derived geometry rules, ComboWire boundary conditions] Coronary casts obey the Huo-Kassab 7/3 diameter law better than Murray's cubic law. Murray-type Y-bifurcations decreased WSS by 10–40% and increased OSI in atherosclerosis-prone regions compared with HK-type bifurcations. — [Huo, Finet, ... Kassab 2012, J Biomech, PMID 22365499](https://doi.org/10.1016/j.jbiomech.2012.01.033)
- Murray's exponent of 3 implies constant WSS throughout the tree, which experimental measurements do not support. The exponent in human coronaries is uncertain (theory gives 2.33–3.0). — [Frontiers in Physiology 2022, Murray's law review](https://www.frontiersin.org/articles/10.3389/fphys.2022.871912/full); [EuroIntervention 2015, anatomy-function review](https://eurointervention.pcronline.com/article/anatomy-and-function-relation-in-the-coronary-tree-from-bifurcations-to-myocardial-flow-and-mass)
- Low WSS has been linked to a lumen-area step-up at the inflow of stented segments, which is the stent analogue of a local expansion. — [Expert recommendations on WSS assessment, Gijsen et al. 2019, Eur Heart J](https://academic.oup.com/eurheartj/article/40/41/3421/5576147)
- At each bifurcation, flow divides mainly according to branch diameters, and this is accompanied by tapering of the parent lumen. — [Gijsen et al. 2019, Eur Heart J](https://academic.oup.com/eurheartj/article/40/41/3421/5576147)

### Inferences
- Physically, Poiseuille-type WSS is proportional to Q/r^3. For a fixed flow Q in a trunk window, the WSS signal sits in the deviation of local radius from what the flow "expects". For a plaque-free trunk without a flow input, the defensible pure-geometry proxy is a **normalized local radius / expansion index**: for example, the local MIS radius divided by the radius predicted by a fitted taper line (or the window's mean), i.e. the residual after detrending. Or the ratio of the window-mean radius to the immediately proximal window's radius. Values >1 (local flare or ectasia) imply lower WSS.
- Raw absolute radius is strongly confounded with body size, sex (BSA and `male` are available in the CGPS BL and FU headers) and arterial position. A normalized or relative measure is better than absolute diameter.
- The bifurcation **expansion ratio** is the most WSS-relevant radius feature in the CFD literature. Because it is computed from mother and daughter areas, it is mathematically distinct from the daughter-to-daughter diameter ratio, and Doutel found low-WSS size independent of the latter. However, it needs both daughter radii, so it is a bifurcation-unit feature. It applies naturally to the proximal LAD/LCX windows (LM bifurcation) and to trunk windows only at side-branch take-offs.

### Gaps
- No human-coronary study was found that isolates **tapering rate (dr/ds)** as an independent WSS predictor. Searches for tapering returned stent and non-coronary papers only. The named authors (Zhang, Tu, Giannoglou, Malvè, Schrauwen, Rabbi, Chiastra) could not be checked for tapering-specific results within the tool budget.
- Doutel 2016 and Huo 2012 are idealized or parametric geometries, not patient-specific. No patient-specific coronary CFD was found that ranks expansion ratio against curvature and bifurcation angle.
- The full-text effect sizes for the 80-patient CT-CFD study were not retrieved.

## Q2. Evidence that deviation from Murray's law / bifurcation area ratio / flaring predicts plaque?

### Takeaway
There is one sizeable human clinical study. In an IVUS cohort of 253 patients, a high Murray ratio (mother larger than the Murray prediction, i.e. relative low shear) was independently associated with plaque *composition* (more dense calcium, less fibrous tissue) near side-branch bifurcations. It did not test plaque *presence* or incidence. The CFD support (Doutel, Huo/Kassab) is idealized.

### Cited Findings
- [human clinical, IVUS-VH, n=253] Plaque components were measured proximal and distal to a side-branch bifurcation. The Murray ratio was mother/daughter by Murray's law, and a high ratio indicates low shear stress. After adjustment for age, sex, risk factors and medication, the Murray ratio was associated with distal fibrous volume (F=4.90, p=0.028), distal fibro-fatty volume (F=4.76, p=0.030) and dense-calcium volume proximal (F=5.93, p=0.016) and distal (F=5.16, p=0.024). The authors conclude that deviation from Murray's law is associated with a high degree of calcification near bifurcations and "may explain why some patients are prone to plaque formation near vessel bifurcations." — [Schoenenberger et al. 2012, Atherosclerosis, PMID 22261173](https://doi.org/10.1016/j.atherosclerosis.2011.12.040)
- [idealized CFD] A high expansion ratio produces large low-WSS regions. Murray's law does not minimize atherosclerosis-prone low-WSS regions. — [Doutel et al. 2016](https://doi.org/10.1016/j.jtbi.2016.04.038)
- [idealized/FE] HK-type bifurcations have higher WSS and lower OSI than Murray-type. — [Huo et al. 2012](https://doi.org/10.1016/j.jbiomech.2012.01.033)
- Finet's law (mother diameter = 0.678 x sum of daughter diameters) is fractal-based and validated in human epicardial coronaries but does not conserve mass. HK and Finet are special cases of a generalized Murray law. — [EuroIntervention 2015 review](https://eurointervention.pcronline.com/article/anatomy-and-function-relation-in-the-coronary-tree-from-bifurcations-to-myocardial-flow-and-mass); [SN Computer Science 2019](https://link.springer.com/article/10.1007/s42979-019-0040-x)

### Inferences
- Murray/HK/Finet deviation and the area expansion ratio are all functions of (mother radius, daughter1 radius, daughter2 radius). With the daughter diameter ratio already in the model, adding one of these adds only one extra degree of freedom: the mother-to-daughters size relation. This information is genuinely different from the daughter ratio, but the two will be correlated, so collinearity should be checked.
- Schoenenberger's sample was a patient cohort that already had disease (IVUS), and the outcome was composition, not new-plaque occurrence. It supports plausibility but is not direct evidence for incident plaque.

### Gaps
- No CCTA study was found that relates the Murray/Finet/HK deviation or the area expansion ratio to plaque presence, or to new plaque on serial CCTA.
- No human study was found on "flaring" just distal to the bifurcation (e.g. a proximal-LAD flare) as a plaque predictor.

## Q3. Is LM length / distance to bifurcation associated with LAD (and LCX) plaque?

### Takeaway
Yes, and this is the oldest and most replicated anatomical-risk observation for the left system: a **short left main trunk** is associated with more and earlier LAD/LCX atherosclerosis. The evidence comes from postmortem (n=204), small angiographic (n=43, n=77) studies, and a small CCTA study (n=62) that did not find a length difference. All are small and cross-sectional. The feature only applies to LAD and LCX, and it is a patient-level constant, not a per-window feature.

### Cited Findings
- [postmortem, n=204] Short LM trunks were associated with earlier and faster LAD/LCX atherosclerosis and more frequent MI. In subjects over 50, the degree of branch atherosclerosis was inversely correlated with trunk length. The authors propose a congenital and possibly hereditary factor. — [Gazetopoulos et al. 1976, Br Heart J 38:1160 (PMC483149)](https://heart.bmj.com/content/38/11/1160)
- [angiographic, n=43] LM trunk length was significantly shorter in patients with coronary atherosclerosis than in those without angiographic CAD. — [Gazetopoulos et al. 1976, Br Heart J 38:180 (PMC482990)](https://doi.org/10.1136/hrt.38.2.180)
- [angiographic, n=77] Patients with LAD plaques had an LM trunk about 2.5 mm shorter than patients with intact LADs. — [Çandır et al., Balkan Med J / Trakya Univ Tip Fak Derg](https://balkanmedicaljournal.org/abstract.php?id=925) (abstract-level via search summary; p-value not retrieved)
- [CCTA 64-slice, n=62] LM length was 10.6±6.1 mm without LM plaque vs 11.3±4.0 mm with LM plaque, with no reported significant difference. LM diameters were larger with plaque (ostial 5.5±0.7 vs 6.0±1.2 mm; bifurcation 4.9±0.9 vs 6.0±1.2 mm; p<0.05), and bifurcation diameter correlated with plaque area (r=0.56). Age also differed between groups. Note that the outcome was LM plaque, not LAD plaque. — [Cademartiri et al., Assessment of LM atherosclerotic burden using 64-slice CTCA](https://pure.eur.nl/en/publications/assessment-of-left-main-coronary-artery-atherosclerotic-burden-us/)
- [CCTA, n=133, single centre] Wider LM–LAD angle (cos theta <0.8) and shorter d20 (straight-line distance across a 20-mm curved LAD segment, i.e. tortuosity) were associated with significant proximal LAD stenosis (HR 8.04 for cos theta <0.8). — [QIMS study, via search summary](https://qims.amegroups.org/article/view/117032/html) (relevant only as context, because angle and curvature are already in the model)
- LM length reference values: 9.13±3.23 mm (angiography, n=100, NE India) — [Manpoong et al. 2023, Cureus, PMID 37829965](https://doi.org/10.7759/cureus.45023); about 10.6 mm in plaque-free CCTA — [Cademartiri](https://pure.eur.nl/en/publications/assessment-of-left-main-coronary-artery-atherosclerotic-burden-us/)
- [CCTA CFD, plaque-free vessels] ESS correlates with distance from the ostium (rho 0.22–0.62). — [Schultz et al. 2023](https://doi.org/10.1007/s10554-022-02739-0)

### Inferences
- A mechanistic link between short LM and low WSS is plausible: a short trunk means the bifurcation-induced flow disturbance enters the proximal LAD/LCX with less flow development. However, no CFD study quantifying this was found.
- The Cademartiri diameter finding (larger LM with plaque) is very likely confounded by positive (Glagov) remodeling. Because baseline vessels are plaque-free in the thesis, this mitigates but does not remove the issue: the LM itself is not required to be plaque-free.
- LM length from a centerline (ostium to LAD/LCX bifurcation point) is easy to compute. It has measurement problems when the LM is very short or absent (trifurcation / separate ostia), which needs a rule (e.g. length = 0 or exclusion).
- "Distance from ostium" is already implicit in the proximal/mid/distal window design.

### Gaps
- No modern, large (>500) CCTA study of LM length vs LAD plaque, or vs incident plaque, was found.
- No CFD study quantifying WSS in the proximal LAD as a function of LM length was found.

## Q4. Is tapering rate associated with plaque or WSS?

### Takeaway
No direct human evidence was found linking coronary **tapering rate** to WSS or to plaque development, despite targeted searches. Tapering is documented as a normal anatomical property: flow loss at each side branch, captured by the Huo-Kassab and Medrano-Gracia atlas work. In physics terms, tapering partly *offsets* the WSS drop from side-branch flow loss, so a trunk segment that tapers *less* than expected (relative dilation) should have lower WSS. This makes "taper residual" or "local expansion" the mechanistically correct form of the feature, but it is an inference, not a demonstrated finding.

### Cited Findings
- The CCTA computational atlas of 300 adults with zero calcium score and no stenosis gives automated 3D diameters, lengths and angles. — [Medrano-Gracia et al. 2016, EuroIntervention, DOI 10.4244/EIJV12I7A139](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy). Vessel size and bifurcation angle differed between LM and other bifurcations and by sex. Hypertension, smoking and diabetes were not associated with shape. — [Medrano-Gracia et al. 2017, J Cardiovasc Transl Res, DOI 10.1007/s12265-016-9720-2](https://link.springer.com/article/10.1007/s12265-016-9720-2). No plaque outcome was reported.
- Coronary flow divides by diameter at each bifurcation, accompanied by parent-lumen tapering. — [Gijsen et al. 2019, Eur Heart J](https://academic.oup.com/eurheartj/article/40/41/3421/5576147)
- WSS is strongly correlated with reciprocal radius in human RCAs. — [Johnston & Johnston 2007](https://doi.org/10.1088/0031-9155/52/9/013)

### Inferences
- If tapering is chosen, compute it per window as the slope of MIS radius vs arc length (mm/mm), or normalized as (r_in − r_out)/(r_mean · L). Report it alongside the window mean radius, because taper is correlated with absolute size.
- Tapering in a trunk is largely driven by side-branch take-offs. If side branches are not units but their positions are known, tapering and branch density will be collinear.

### Gaps
- No primary study on tapering and plaque was found by Zhang, Tu, Giannoglou, Malvè, Schrauwen, Rabbi or Chiastra within the search budget. This does not prove such studies don't exist.
- Branch density (number of side branches per length) has no direct evidence on WSS or plaque. Searches returned only PCI side-branch-occlusion papers.
- Ostium height and ostial take-off angle: the only evidence is from anomalous aortic origin CFD, where a narrower take-off angle gives a more elliptical ostium and higher WSS indices ([ITU patient-specific AAOCA study](https://research.itu.edu.tr/en/publications/patient-specific-in-silico-hemodynamic-analysis-of-the-anomalous-/)). Nothing was found for normal anatomy or plaque. A centerline alone also does not give ostium height above the sinus without an aortic segmentation.

## Q5. Measurement robustness at CCTA resolution (~0.4–0.5 mm voxels) and confounding with plaque

### Takeaway
Radius-derived features are sensitive to CCTA resolution: a ±0.25 mm radius error is about 15–20% of a 1.5 mm radius. Ratios computed over longer windows (expansion index, LM length) are more robust than slopes (taper) or bifurcation-local areas. Plaque-induced remodeling confounds diameter–plaque associations in cross-sectional studies, which the plaque-free baseline mitigates.

### Cited Findings
- CCTA-based ESS "increase rapidly and become widely scattered with decreasing lumen diameter," i.e. small-radius segments are where the radius error most affects WSS. — [Schultz et al. 2023](https://doi.org/10.1007/s10554-022-02739-0)
- Larger LM diameter in plaque-bearing LMs (r=0.56 between bifurcation diameter and plaque area) is consistent with outward remodeling confounding raw diameter. — [Cademartiri et al.](https://pure.eur.nl/en/publications/assessment-of-left-main-coronary-artery-atherosclerotic-burden-us/)
- The LM is short and variable, and plaque can occupy the whole LM, which removes the reference diameter. — [ACC 2025 review on CCTA in LM disease](https://www.acc.org/Latest-in-Cardiology/Articles/2025/11/24/17/57/Role-of-CCT-Angiography-in-Left-Main-CAD)

### Inferences
- **Taper slope** is the least robust: it is a derivative of a noisy MIS radius over a short window (proximal/mid/distal windows are perhaps 15–40 mm). Fit a robust linear regression over the window and exclude about 2–3 mm around side-branch ostia, where the MIS radius jumps.
- A **local expansion index** (window-mean radius / proximal-window mean radius, or the max residual from a vessel-wide taper fit) averages over many centerline points and is more robust.
- **LM length** depends on bifurcation-point detection, which is robust to about 1 voxel (~0.5 mm) against a ~10±4–6 mm range, so the relative error is small. It applies only to LAD and CX.
- **Murray/expansion ratio** requires daughter radii just beyond the carina, where MIS radius is unreliable. Measure at about 1–2 diameters from the bifurcation point.

### Gaps
- No reproducibility (ICC) data was found specifically for MIS-radius taper or expansion indices at CCTA resolution.

## Summary ranking for the "one more feature" decision (inference, based on the evidence above)
1. **Local lumen expansion index (normalized radius / taper residual per window)**: strongest physics (WSS ~ 1/r, r^-3 at fixed flow) and strong human-CT CFD support (Johnston 2007; Schultz 2023, ~3x ESS difference across diameter tertiles in plaque-free vessels). Applies to all three arteries and all windows, is robust when averaged, and is not a function of curvature, angle or daughter ratio. Weakness: no direct plaque-outcome study.
2. **LM length (LAD/CX only)**: the only feature with direct, repeated (if old and small) human plaque evidence (Gazetopoulos n=204 postmortem, n=43; Çandır n=77). Weakness: a patient-level constant, absent for the RCA (so the RCA model would need a different feature or none), and one null CCTA study (n=62).
3. **Bifurcation area expansion ratio / Murray (HK) deviation**: best CFD-to-WSS link (Doutel) and one human IVUS composition study (n=253). Weakness: partly redundant with the daughter diameter ratio, needs daughter radii, and is a bifurcation feature that is awkward for trunk windows.
4. **Tapering rate**: intuitive, but no direct evidence was found and it is noisy at 0.5 mm voxels.
5. Branch density, ostium height, take-off angle: no usable evidence was found.
