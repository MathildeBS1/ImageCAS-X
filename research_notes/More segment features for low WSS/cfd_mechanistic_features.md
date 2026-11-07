# Segment-level coronary geometric descriptors mechanistically linked to low / oscillatory WSS (CFD and in-vitro), beyond curvature, taper, LM bifurcation angle and LM daughter ratios

Scope note: torsion, tortuosity, helicity, Murray/HK deviation at the LM, LM length and tapering were covered in
`research_notes/Fourth centerline feature for plaque/` and the two reports (`Low WSS at bends and bifurcations.md`,
`Taper and curvature interaction for WSS.md`). They are not repeated here except where a side-branch version is new.
Search budget was limited (about 16 tool calls); several full texts were paywalled or blocked (Nature, Springer, PoliMi
PDF), so a number of findings below come from abstracts or search snippets and are marked as such.

## Q1. Which descriptors beyond curvature/taper/bifurcation angle/diameter ratios show a CFD link to low or oscillatory WSS (TAWSS, OSI, RRT, transverse WSS, topological skeleton)?

### Takeaway
The descriptor with the clearest mechanistic and CFD support is **side branches**: how many branches leave a segment and
how much flow they take. Outflow to branches lowers TAWSS in the main vessel, and the main-vessel wall opposite the
flow divider of a side-branch ostium is a low-WSS zone. Side-branch bifurcation angles (LAD–D1 etc.) have only a minor
CFD effect compared with curvature in idealised models. Cross-section eccentricity, myocardial bridging and ostial
take-off angle are weakly supported or contradictory. I found no CFD source for vessel volume / V/M, inflection
points or planarity as WSS determinants.

### Cited Findings

**A. Side branches: number, flow extraction, ostium location (strongest new candidate)**
- Bourantas group (Ramasamy et al., **bioRxiv preprint 2023, not peer-reviewed in this version**; n = 19 IVUS vessels with
  13-month follow-up plus 13 OCT vessels; all had at least one side branch >1 mm): adding side branches to the 3D model
  lowered mean TAWSS from 1.698 to 0.821 Pa (IVUS models) and from 1.325 to 0.682 Pa (OCT models), p<0.001, and changed
  multidirectional WSS. In native segments, WSS from the model with side branches predicted progression better (AUC 0.712 vs
  0.554 without side branches) — [bioRxiv 10.1101/2023.04.05.535789](https://www.biorxiv.org/content/10.1101/2023.04.05.535789.full.pdf)
- The same preprint gives the mechanism: blood diverted into side branches reduces main-vessel flow, so WSS is lower in models
  with side branches — [bioRxiv 10.1101/2023.04.05.535789](https://www.biorxiv.org/content/10.1101/2023.04.05.535789.full.pdf)
- Li et al. (Stone/Coskun group; PMC4983229; human, invasive imaging): leaving side branches out greatly reduces the ability to
  detect regions with pathologic ESS, but ESS calculated without them keeps good negative predictive value over the major
  arteries. Search summary only; the full text was blocked, so n and sensitivity numbers were not checked — [PMC4983229](https://pmc.ncbi.nlm.nih.gov/articles/PMC4983229/)
- Search summary (source not fully checked): a side branch changes the main-branch SS distribution only within about 3 mm of
  the ostium — [PMC4983229 / ResearchGate "Impact of side-branches"](https://www.researchgate.net/publication/47383902_Flow_simulation_studies_in_coronary_arteries-Impact_of_side-branches)
- How side-branch outflow is split matters. In six patient-specific coronary trees, Murray's-law outflow gave an average WSS
  8% higher than an empirical flow model (range −5% to +27%), and Murray's law underestimates side-branch flow (J Biomech 2011;
  via search summary) — [ScienceDirect S0021929011000789](https://www.sciencedirect.com/science/article/pii/S0021929011000789)
- Molony and colleagues (IVUS-based CFD): WSS was low on the wall opposite the flow divider in models with side branches. In
  models without side branches this was not always so (via search summary) — [Springer, Biomed Eng Online 14 S1 S2](https://link.springer.com/article/10.1186/1475-925X-14-S1-S2)
- Grayscale IVUS (no CFD): in complex bifurcation lesions, plaque at the side-branch ostium sits mainly opposite the flow
  divider, in regions expected to have low WSS (search snippet) — [Springer Medicine, vessel remodeling and plaque distribution in side branch](https://www.springermedicine.com/vessel-remodeling-and-plaque-distribution-in-side-branch-of-comp/21554956)

**B. Side-branch bifurcation angle (LAD–D1, LCx–OM, RCA branches)**
- Chiastra, Migliavacca et al., J Biomech 2017 (**idealised**, population-based LAD/D1 models, with and without stenosis):
  cardiac curvature influences near-wall and intravascular haemodynamics, while the bifurcation angle has only a minor
  effect. A smaller radius of curvature gave more low-WSS exposure and, with stenosis, less oscillatory WSS exposure
  (abstract via search; PDF blocked, so the % surface-area numbers were not retrieved) — [PoliMi record 11311/1029992](https://re.public.polimi.it/handle/11311/1029992)
- Gallo et al. (PoliTo, ESBIT; **idealised**, diseased bifurcations): the distal bifurcation angle affects low and oscillatory
  WSS (RRT > 4 Pa⁻¹ surface fraction), but only moderately in the stenosed case — [PoliTo ESBIT PDF](https://iris.polito.it/retrieve/handle/11583/2676235/156275/ESBITAthematic_GALLO.pdf)
- A review table (JCM 2022) notes that lesion-specific (patient) models did not show the significant WSS–bifurcation-angle
  correlation that idealised models report — [PMC9457427 table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC9457427/table/jcm-11-05143-t002)
- Sci Rep 2025 (reverse flow in side branches by bifurcation angle; full text redirected to login, content unverified):
  the title links side-branch reverse flow to bifurcation angle and plaque formation — [Nature Sci Rep s41598-025-89427-w](https://www.nature.com/articles/s41598-025-89427-w)
- Persian-language CFD study of the left coronary tree (single model, low quality): flags the LAD after D3 as high risk using
  WSS ≤1.5 Pa and OSI ≥0.3 thresholds — [Magiran 1616880](https://magiran.com/paper/1616880/?lang=en)

**C. Lumen cross-section eccentricity / ovality**
- Biplane angiography, three human RCAs (Biomed Eng Online 2006): circular cross-sections with about 0.8 mm axial
  resolution gave sufficiently accurate WSS compared with elliptic cross-sections. Mean elliptical eccentricity (ratio of the
  radii) was about 1.13 across about 3,000 cross-sections; irregular lumina were uncommon and mostly at severely diseased
  sites — [PMC1513234](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1513234/); [Biomed Eng Online 5:39](https://link.springer.com/article/10.1186/1475-925X-5-39)
- Cerebral venous sinus CFD (not coronary): cross-sectional area influenced haemodynamics more than triangularity or
  circularity (via search summary) — [iieta.org](https://iieta.org/download/file/fid/48054)
- Non-peer-reviewed arXiv 2026 preprint (area-matched elliptic throats, minor/major 0.8/0.6/0.4) studied FFR and pressure
  drop; I did not retrieve WSS results — [arXiv 2609.19290](https://arxiv.org/pdf/2609.19290)
- The Eur Heart J expert consensus links low WSS to greater plaque eccentricity. Here eccentricity is an outcome of
  low WSS, not a lumen-shape predictor of it — [Gijsen et al. 2019](https://academic.oup.com/eurheartj/article/40/41/3421/5576147)
- The coronary-aneurysm CFD study where eccentricity drove adverse shear and near-wall vortices concerns aneurysms, not
  normal segments — [Phys Fluids 38:031904](https://pubs.aip.org/aip/pof/article/38/3/031904/3382252/How-cross-sectional-eccentricity-modulates)

**D. Myocardial bridging**
- Moving-boundary CFD (Macquarie; 92 MB patients vs 20 controls; abstract via search): proximal LAD WSS was lower with MB;
  plaque burden correlated with proximal WSS (r = −0.51) and peak residence time (r = 0.60) — [Macquarie record](https://researchers.mq.edu.au/en/publications/abnormal-shear-stress-and-residence-time-are-associated-with-prox/)
- Same group, 10 vs 10 with endothelial dysfunction: proximal LAD WSS 0.32 ± 0.14 Pa with MB vs 0.71 ± 0.38 Pa without,
  p = 0.01 (abstract via search) — [Macquarie record](https://researchers.mq.edu.au/en/publications/myocardial-bridging-and-endothelial-dysfunction-computational-flu/)
- **Contradicting:** Giannopoulos et al., Angiology 2024 (36 LAD MBs, CCTA, steady diastolic CFD, bridge compression
  **not** modelled): ESS 5 mm proximal vs first 5 mm inside MB 0.94 vs 1.06 Pa (p = .56); proximal vs within 1.2 vs 0.95 Pa
  (p = .17); within vs distal 0.95 vs 2.98 Pa (p < .0001). Plaque proximal to MB in 12/36 (33%), none within. ESS did not
  differ between arteries with and without plaque (p = .81) — [PMC10870693](https://pmc.ncbi.nlm.nih.gov/articles/PMC10870693/)

**E. Ostial take-off angle**
- The only take-off-angle CFD/FSI work found concerns an **anomalous** RCA from the left sinus (symptoms linked to a smaller
  angle, 27.8° vs 31.9°, p = 0.017; ischaemia, not WSS or plaque) — [PMC8047363](https://pmc.ncbi.nlm.nih.gov/articles/PMC8047363)
- MRI plus CFD: velocity profiles are skewed at the coronary ostia, with near-wall flow reversal on the myocardial side of the
  RCA and the epicardial side of the left artery (ISMRM 2006 abstract) — [ISMRM 2006 01917](https://cds.ismrm.org/protected/06MProceedings/PDFfiles/01917.pdf)

**F. WSS topological skeleton / TSVI (new outcome metric, not a geometric descriptor)**
- Mazzi et al., Ann Biomed Eng 2021 (human coronaries, IVUS follow-up): TSVI, the variability of WSS contraction and expansion
  over the cardiac cycle, and low WSS were both associated with wall-thickness increase (abstract via search; n and effect
  sizes not retrieved) — [Springer 10.1007/s10439-021-02829-5](https://link.springer.com/article/10.1007/s10439-021-02829-5)
- Method paper and review: skeleton = fixed points (WSS vanishes) linked by contraction and expansion manifolds; computed from
  WSS divergence — [Mazzi et al. 2021 review, Mathematics](https://www.researchgate.net/publication/350414597_Wall_Shear_Stress_Topological_Skeleton_Analysis_in_Cardiovascular_Flows_Methods_and_Applications); code: [GitHub TSVI](https://github.com/PoliToBIOMed-Lab-Cardiovascular-Biomech/TSVI)
- No source found that maps a centerline/lumen geometric descriptor onto TSVI or skeleton features in native coronaries.
  The only coronary skeleton geometry study found is stented (three arteries) — [iris.polito.it 2955945](https://iris.polito.it/retrieve/handle/11583/2955945/566397)

### Inferences
- **Side-branch flow loss** is the mechanistically cleanest new segment feature. In Poiseuille terms WSS ∝ Q/r³, so a segment
  that loses flow to branches without narrowing to match has lower WSS. Computable from the tracer if branch ostia and their
  diameters are available. A proxy is the count of branches >1–1.5 mm per segment, or the sum of branch d^(7/3 to 3) relative
  to the parent. Two caveats. First, the existing note `Taper and curvature interaction for WSS.md` already treats raw taper as
  the part of WSS not explained by branch flow loss, so branch flow loss and taper overlap by design; a "taper–branch
  mismatch" (taper minus the taper that branch outflow would justify) would be the non-redundant form. Second, the in-house
  tracer labels only the trunk artery (LAD/LCx/RCA); whether it gives side-branch ostia and diameters is unknown to me.
- **Side-branch bifurcation angle** (LAD–D1, LCx–OM) is unlikely to add much: idealised CFD shows a minor effect relative to
  curvature, and patient-specific work does not confirm it. The same conclusion as for the LM angle in earlier notes.
- **Eccentricity/ovality** in plaque-free segments is close to circular (mean radius ratio about 1.13) and its WSS effect
  appears small next to area. On a CCTA lumen contour it would mostly measure segmentation noise and partial-volume effects.
  Low priority.
- **Myocardial bridging** is a categorical, LAD-mid-only feature, contradictory in CFD (moving-boundary models positive,
  static CCTA model null) and not reliably detectable from a lumen contour (bridging needs the myocardium). It is also not in
  the BL/FU headers as a variable as far as these notes go. Low priority.
- **Ostial take-off angle**: no evidence in normal anatomy. Not recommended.

### Gaps
- No CFD source found linking **inflection points / curvature sign changes**, **planarity**, **segment length**,
  **distance from ostium**, **vessel/lumen volume-to-myocardial-mass (V/M)** or **ramus (LM trifurcation)** to low or
  oscillatory WSS. V/M is studied for FFR and ischaemia (not WSS) to my knowledge, but I did not verify this with a source.
- Effect-size numbers for Chiastra 2017 (LAD–D1 angle vs curvature, % area of low TAWSS/high OSI) were not retrieved (PDF 403).
- Li et al. (PMC4983229) sensitivity/NPV numbers not retrieved (captcha).
- Whether the Ramasamy et al. preprint was later published in a peer-reviewed journal was not checked.
- The 2010 study of 30 patient-specific RCAs (plaque virtually removed; TAWSS finds most plaques, OSI/RRT fewest false
  positives) appeared in a search summary without a checkable URL, so it is not cited.

## Q2. Which have consistent mechanistic support vs single-study or contradictory findings?

### Takeaway
Consistent: side-branch outflow lowers main-vessel WSS, and the wall opposite the side-branch flow divider is a low-WSS
site (several CFD groups, IVUS co-location). Contradictory: myocardial bridging (moving-boundary vs static CCTA CFD) and
side-branch bifurcation angle (idealised vs patient-specific). Weak or absent: eccentricity, ostial take-off angle, V/M,
inflection points, planarity.

### Cited Findings
- Side-branch outflow: preprint (Ramasamy 2023), Stone/Coskun group (PMC4983229), Molony (Biomed Eng Online) and the outflow
  boundary-condition study (J Biomech 2011) agree in direction — see Q1 A for links:
  [bioRxiv](https://www.biorxiv.org/content/10.1101/2023.04.05.535789.full.pdf), [PMC4983229](https://pmc.ncbi.nlm.nih.gov/articles/PMC4983229/),
  [Biomed Eng Online 14 S1 S2](https://link.springer.com/article/10.1186/1475-925X-14-S1-S2), [J Biomech 2011](https://www.sciencedirect.com/science/article/pii/S0021929011000789)
- Bifurcation angle: idealised models report a minor/moderate effect ([PoliMi](https://re.public.polimi.it/handle/11311/1029992),
  [PoliTo ESBIT](https://iris.polito.it/retrieve/handle/11583/2676235/156275/ESBITAthematic_GALLO.pdf)); patient-specific models show no significant correlation
  ([PMC9457427 table](https://pmc.ncbi.nlm.nih.gov/articles/PMC9457427/table/jcm-11-05143-t002))
- Myocardial bridge: positive in moving-boundary CFD ([Macquarie](https://researchers.mq.edu.au/en/publications/abnormal-shear-stress-and-residence-time-are-associated-with-prox/)),
  null in static CCTA CFD ([PMC10870693](https://pmc.ncbi.nlm.nih.gov/articles/PMC10870693/))
- Eccentricity: one small coronary study (three RCAs) finds circular approximation adequate ([PMC1513234](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1513234/))

### Inferences
- The difference between moving-boundary and static models suggests the MB effect, if real, comes from systolic compression,
  which a single-phase CCTA lumen cannot capture.
- The side-branch evidence is mostly from diseased, invasively imaged vessels (IVUS/OCT, often stented), not plaque-free CCTA.
  Transfer to the CGPS plaque-free cohort is an assumption.

### Gaps
- No head-to-head study ranks these descriptors against one another in the same patient-specific coronary dataset.

## Q3. How much of WSS variance do they add beyond curvature and taper?

### Takeaway
I found no study reporting incremental WSS variance (R² or similar) from any of these descriptors beyond curvature and taper.
The only quantitative "added value" figure found is the side-branch preprint: modelling branches roughly halved mean TAWSS and
raised progression AUC from 0.554 to 0.712. This concerns model completeness, not a scalar segment feature, and comes from
n = 19 vessels in an unreviewed preprint.

### Cited Findings
- TAWSS 1.698 → 0.821 Pa (IVUS) and 1.325 → 0.682 Pa (OCT) with side branches; AUC 0.712 vs 0.554 for progression —
  [bioRxiv 10.1101/2023.04.05.535789](https://www.biorxiv.org/content/10.1101/2023.04.05.535789.full.pdf)
- First-order WSS scales with the inverse cube of the mean lumen radius (WSS ∝ R⁻³), which makes lumen size, and with it flow
  per unit area, the dominant geometric driver (search summary of a CFD sensitivity paper) — [Sci Rep 2025, s41598-025-85781-x](https://www.nature.com/articles/s41598-025-85781-x)
- A search for a variance decomposition of WSS by geometric descriptors found none; the earlier note
  `predictive_evidence_ranking.md` §2 covers the surrogate/ML geometry-to-WSS studies.

### Inferences
- Given WSS ∝ Q/r³, any feature that changes Q per segment (branch outflow) or r (taper, local area) should matter more than
  shape features of the cross-section. That favours branch flow loss, or a taper–branch mismatch, over eccentricity, take-off
  angle or side-branch angle. This is reasoning, not a measured result.

### Gaps
- No R² / partial-R² values for any descriptor beyond curvature and taper found. Answering this would need the user's own CFD
  on a subset, or a surrogate-model feature-importance study (none located for these specific features).
