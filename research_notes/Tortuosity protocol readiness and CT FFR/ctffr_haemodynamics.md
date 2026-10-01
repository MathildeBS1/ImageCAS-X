# CT-FFR and computational haemodynamics on healthy coronary trees: descriptor value, plaque prediction, feasibility

Scope note for the report writer. This builds on `research_notes/Plaque prone regional geometry descriptors/hemodynamic_geometry_proxies.md` (Poiseuille WSS proxy, tree-propagated tau_hat, van der Giessen flow laws, ML WSS surrogates), `plaque_prone_regions.md` and `longitudinal_design.md` (PREDICTION, Samady, EMERALD, PARADIGM at snippet level). Those are not repeated except where new numbers were found. Kashyap 2022 (kappa_a vs low TAWSS, R^2 up to 0.23 in 127 CAD-free CCTA patients) is covered in the earlier `reports/` tortuosity notes and is only referenced here.

Read-status tags:
- **[full text]**: I read the relevant methods and results myself (local PDF or PMC page).
- **[full text, fetch summary]**: full text page fetched, but read through an automated extraction, so exact wording should be checked before quoting.
- **[abstract]**: abstract only (Europe PMC or publisher landing page).
- **[snippet]**: search-engine summary. Must be checked before it goes in the thesis.
- **[derivation]**: standard fluid mechanics worked out here. No empirical claim.

Access note: PubMed (reCAPTCHA), JACC, ScienceDirect and JCCT full text pages returned 403 throughout. Europe PMC's REST API and PMC worked, so abstracts came from there. None of the key JACC trials (EMERALD, EMERALD II, Kumar 2018, interscan FFRCT) could be read in full.

## 1. CT-FFR in normal / plaque-free coronaries: values, variance, determinants

### Takeaway
CT-FFR is not at ceiling in normal vessels. It declines steadily from about 0.96 to 0.99 at the ostium to about 0.86 to 0.90 distally, and the distal LAD value is widely spread: in stenosis-free marathon runners the distal LAD was 0.81 ± 0.10 and 32 % of them were at or below 0.80. So there is plenty of between-person variance. The problem is that this variance is mostly explained by lumen calibre, vessel length and lumen volume relative to myocardial mass (V/M). Those are geometric quantities the thesis can measure directly, and the distal value is also the least reproducible CT-FFR readout.

### Cited Findings
- **Profiles in normal vessels [abstract / snippet].** In vessels with 0 % or < 25 % stenosis, FFRCT falls continuously from ostium to distal vessel: LAD 0.96 ± 0.024 to 0.86 ± 0.054, RCA 0.99 ± 0.006 to 0.90 ± 0.037 (both P < 0.001). There is an extra significant drop across the distal LAD but not the distal RCA. Population is patients with CAD referred for CCTA, not a healthy cohort; n not retrieved (JACC abstract page 403). [JACC 2018 abstract, "Profiles of FFRCT in patients with CAD"](https://www.jacc.org/doi/10.1016/S0735-1097(18)32115-6)
- A practice guide gives the ostium to distal difference in normal vessels (0 % or < 25 % stenosis) as 0.08 to 0.13, and recommends reading FFRCT 1 to 2 cm distal to a lesion rather than at the vessel end, because distal values ≤ 0.80 are common without any stenosis. [snippet] [RadioGraphics 2022, CT FFR practical guide](https://pubs.rsna.org/doi/full/10.1148/rg.210097); [AJR, FFRCT current status](https://www.ajronline.org/doi/10.2214/AJR.20.23332)
- **Asymptomatic, stenosis-free cohort [full text, fetch summary].** 98 asymptomatic male marathon runners, 53 ± 7 years; 59 without coronary stenosis analysed with an on-site ML CT-FFR prototype (Siemens cFFR 3.2, syngo.via Frontier). Distal FFRCT: LAD 0.81 ± 0.10 (19/59 = 32 % ≤ 0.80), LCx 0.89 ± 0.07 (8 %), RCA 0.89 ± 0.07 (7 %). 22 of 59 (37 %) had at least one abnormal distal value. Distal vessel diameter differed significantly for LAD and RCA but "isolated vessel diameter is one important but not the only factor influencing FFRCT". Authors attribute the steady distal decline to physiological tapering. Caveat: athletes have large LV mass, which pushes allometric hyperaemic flow up. [PMC8589749](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589749/)
- **V/M ratio as determinant [abstract].** 238 NXT-trial patients, 438 vessels. Low epicardial lumen volume to LV myocardial mass ratio (median split, 18.57 mm^3/g) gave lower invasive FFR overall (0.80 ± 0.12 vs 0.87 ± 0.08, P < 0.0001), including in non-obstructive CAD, and V/M independently predicted FFR ≤ 0.80. The search snippet adds that in QCA stenosis ≤ 50 %, low vs high V/M gave FFR 0.81 ± 0.12 vs 0.88 ± 0.07. [Taylor et al., JCCT 2017, PubMed 28789941](https://pubmed.ncbi.nlm.nih.gov/28789941); follow-up on V/M with myocardial blood flow [PubMed 31302027, snippet](https://pubmed.ncbi.nlm.nih.gov/31302027/)
- The review "The Anatomy of Coronary Risk" states that FFRCT loses accuracy in moderate lesions and with heavy calcification, and that QFR may not apply in severe tortuosity. It separates FFRCT/QFR (stenosis severity, PCI guidance) from anatomy-flow studies (mechanism). [full text] Shen et al., local PDF `docs_thesis/papers/The Anatomy of Coronary Risk ... .pdf`, sections 3 and 5.

### Inferences
- [derivation] In a stenosis-free vessel, hyperaemic pressure loss is dominated by viscous (Poiseuille) loss, dP = 8 mu L Q / (pi r^4), summed along the path. Hyperaemic Q in every CT-FFR package is set from myocardial mass (allometric scaling) and split by downstream lumen size. Distal CT-FFR in a healthy tree is therefore close to a closed-form function of path length, path radius (fourth power) and V/M. It encodes geometry the thesis can compute directly, with the inflow assumption layered on top.
- The spread in normal vessels (distal LAD SD 0.05 to 0.10) is large enough to be a descriptor, but it would mostly be a nonlinear summary of "long, thin LAD relative to heart size". That is a legitimate descriptor of diffuse narrowing / lumen-mass mismatch, not of tortuosity.
- The LAD is the vessel where normal FFRCT is lowest and most variable, and the one where tortuosity is usually measured. Any tortuosity vs CT-FFR association in the LAD needs adjustment for LAD length and mean radius, or it is confounded by construction.

### Gaps
- No normative FFRCT distribution from a general-population, plaque-free cohort (age and sex stratified) was found. The runner cohort (male athletes) and CAD-referral cohorts are the closest.
- Could not read the profiles paper in full (n, vessel count, software).
- No study found that decomposes normal-vessel FFRCT variance into length, radius, V/M and curvature in one model.

## 2. Does baseline CT-FFR, delta-FFR or WSS predict future plaque onset, progression or events?

### Takeaway
Every prognostic haemodynamic study found starts from existing disease: lesions in ACS or stable CAD patients, followed for months to 3 to 5 years. In those settings, low ESS predicts lumen loss and progression, and high WSS, delta-FFRCT and axial plaque stress predict which existing lesion becomes an ACS culprit. Effect sizes are moderate (AUC about 0.63 to 0.78 for WSS alone), and the prognostic horizon is short: EMERALD II's discrimination fell significantly after 2 years. I found no study that computes CT-derived haemodynamics on a plaque-free baseline and follows it for new plaque over about 10 years. The closest are invasive serial studies showing low WSS drives growth in plaque-free wall regions over 12 months.

### Cited Findings
**Low ESS and progression (existing disease)**
- **PREDICTION (Stone 2012) [abstract].** 506 ACS patients after PCI; three-vessel angiography plus IVUS ESS profiling; serial imaging in 374 at 6 to 10 months. The primary end point (increase in plaque area) was predicted by large baseline plaque burden only. Low ESS independently predicted decrease in lumen area (secondary end point), and together with plaque burden predicted increased plaque burden and lesions needing PCI. The combined predictors had PPV 41 % and NPV 92 %. [Circulation 2012;126:172-81, via Europe PMC](https://pubmed.ncbi.nlm.nih.gov/22723305/)
- Earlier notes already hold Samady 2011 (20 CAD patients, 6 months) and the PROSPECT low-ESS substudy at snippet level. [plaque_prone_regions.md]
- **CCTA-CFD serial study [full text, fetch summary].** 22 patients, 34 lesions, paired CCTA about 2 years apart (median 22 months). Transient OpenFOAM CFD, Murray's law flow split, values normalised to a proximal stenosis-free reference segment. Adjusted predictors of progression: normalised minimum TAWSS OR 0.38 (95 % CI 0.25 to 0.57), normalised maximum helicity OR 1.44 (1.07 to 1.93); AUC 0.78. Regression predicted by gradient oscillatory number and vorticity (AUC 0.83). Lesions, not plaque-free segments; very small n. [J Cardiovasc Transl Res 2025, PMC12858539](https://pmc.ncbi.nlm.nih.gov/articles/PMC12858539/)

**High WSS / delta-FFR and events (existing lesions)**
- **Kumar 2018, FAME II substudy [snippet].** 441 stable CAD patients with FFR ≤ 0.80 on medical therapy; 34 (8 %) had MI within 3 years. 29 vessel-related MI cases vs 29 propensity-matched controls, angiography-based 3D reconstruction. Proximal-lesion WSS > 4.71 Pa had a higher rate of vessel-related MI. [JACC 2018;72:1926-35](https://www.jacc.org/doi/10.1016/j.jacc.2018.07.075)
- **EMERALD (Lee 2019) [abstract].** 72 ACS patients with prior CCTA; 66 culprit vs 150 non-culprit lesions. Culprits had higher diameter stenosis (55.5 ± 15.4 % vs 43.1 ± 15.0 %). Adding haemodynamics (FFRCT, delta-FFRCT, WSS, axial plaque stress) improved discrimination and reclassification over stenosis alone. Lesions with both adverse plaque and adverse haemodynamic characteristics: HR 11.75 (2.85 to 48.51) vs neither. Thresholds from earlier notes: delta-FFRCT ≥ 0.06, WSS ≥ 154.7 dyn/cm^2, APS ≥ 1606.6 dyn/cm^2. [JACC CVI 2019, PubMed 29550316](https://pubmed.ncbi.nlm.nih.gov/29550316/)
- **EMERALD II [snippet].** 351 patients with CCTA who had ACS 1 month to 3 years later. Delta-FFRCT ≥ 0.10 had the highest specificity (88.3 %) for culprit lesions; plaque burden ≥ 70 % had the highest sensitivity (90.6 %). An explainable ML model ranked delta-FFRCT as the most important feature. The AI-QCPHA model also included WSS and myocardial blood flow. [JACC CVI 2024, AI-QCPHA](https://www.jacc.org/doi/10.1016/j.jcmg.2024.03.015); [SOLACI summary](https://solaci.org/en/2025/12/18/emerald-ii-non-invasive-coronary-anatomy-and-physiology-ccta-in-acs-prediction/)
- **EMERALD II time frame [snippet].** Prognostic value was concentrated within 2 years. The AUC of the combined four characteristics was 0.851 for test-to-event < 1 year vs 0.741 at 2 to 3 years (P = 0.006). [JACC CVI 2025](https://www.jacc.org/doi/10.1016/j.jcmg.2025.02.003); [ACC journal scan](https://www.acc.org/latest-in-cardiology/journal-scans/2025/04/23/13/28/emerald-ii)
- **Global delta-CT-FFR in non-obstructive disease [full text, fetch summary].** 1215 diabetic patients (60.1 ± 10.3 y), CT-FFR > 0.75 in all vessels, deep-learning CT-FFR (DEEPVESSEL FFR). Global gradient = sum of delta-CT-FFR over all vessels > 2 mm; mean 0.19 ± 0.25 (0.17 ± 0.22 without MACE vs 0.37 ± 0.36 with MACE). Median follow-up 57.3 months; 137 MACE (11.3 %, mostly unstable angina). Gradient ≥ 0.20: HR 2.88 (1.76 to 4.70). "Non-obstructive" includes plaque, so this is not a plaque-free baseline. [PMC10373274](https://pmc.ncbi.nlm.nih.gov/articles/PMC10373274/)
- **Griffo 2026 [full text, via local paper review].** In 187 future-culprit vs non-culprit lesions (all patients later had MI), lesion WSS AUC 0.63 and lesion-to-vessel WSS ratio AUC 0.66 to 0.68, whether from CFD or a GNN surrogate. [docs_thesis/papers/griffo2026wss.md]

**Closest to plaque-free baselines**
- Low WSS was associated with more plaque progression than mid or high WSS "even in the regions classified as a plaque-free wall", with low WSS and lipid acting synergistically. WSS came from IVUS lumen fused with a CT centreline and invasive flow boundary conditions, in patients with existing coronary disease. [snippet] [Cardiovasc Res 2023, NIRS/OCT study, PMC10153640](https://pmc.ncbi.nlm.nih.gov/articles/PMC10153640/)
- Tziotziou et al. 2023: 34 coronary arteries imaged at baseline and 12 months. Higher mechanical wall stress was associated with more vessel wall growth in healthy segments. In diseased regions low MWS plus high WSS gave the largest lipid-rich necrotic core increase. [abstract] [Atherosclerosis 2023;387, PMID 38029610](https://www.sciencedirect.com/science/article/pii/S002191502305308X)
- PARADIGM does define new plaque in baseline plaque-free SCCT segments (9583 segments, 1162 patients, ≥ 2 years), but the published predictor work there is radiomics and clinical factors, not CFD. [longitudinal_design.md, snippet]

### Inferences
- The event evidence (EMERALD, EMERALD II, Kumar, Griffo) is about **which existing lesion ruptures in the next 1 to 3 years**. Its mechanism is high WSS and axial plaque stress at the upstream shoulder of a stenosis. In a plaque-free tree there is no lesion shoulder, so these metrics are not defined and the results do not transfer.
- The mechanistic evidence relevant to plaque onset (low ESS and oscillatory flow at curvature inner walls and bifurcation outer walls) comes from invasive, short-follow-up studies in diseased patients. It supports low WSS as a local risk factor, but nothing tests it as a 10-year predictor from CCTA in healthy people.
- EMERALD II's loss of discrimination after 2 years suggests haemodynamic snapshots have a short horizon for events. A 10-year CGPS interval would be weaker still for events, though plaque onset (a slower process) could plausibly behave differently. This is untested.
- A CGPS analysis of baseline haemodynamics vs 10-year new plaque would be novel, which is both its value and its risk: there is no effect size to power against.

### Gaps
- No study found with CT-derived CT-FFR, delta-FFR or WSS at a plaque-free baseline and follow-up of more than about 5 years for new plaque.
- PREDICTION, EMERALD and Kumar 2018 were read at abstract or snippet level only; full ORs by ESS category were not retrieved.
- Could not confirm whether any PARADIGM substudy used FFRCT or CFD for plaque-free segments. One search hit ("Role of quantitative plaque analysis and FFRCT to assess plaque progression", J Thorac Imaging) was not read.

## 3. Tortuosity and haemodynamics without stenosis: does it change CT-FFR, and is CFD redundant with geometry?

### Takeaway
Tortuosity does raise pressure loss and helicity in simulations, but in the absence of stenosis the effect is small, a few mmHg at resting flow in idealised 2D models. Clinically it matters only in extreme tortuosity, and there it is mainly a wire artefact of invasive FFR. The robust human finding is that curvature explains a modest share of low-WSS variance (R^2 up to 0.23 in 127 CAD-free patients, Kashyap 2022). So WSS is partly, not fully, predictable from curvature. CT-FFR in a healthy tree is close to redundant with length and radius, while local WSS / OSI / helicity carry some information geometry scalars do not.

### Cited Findings
- **Li 2012, idealised simulation [full text, fetch summary].** 2D idealised models, tortuosity angle 30 to 120 degrees, 0 to 5 bends; single inlet velocity 0.156 m/s (LAD resting peak), plus a pulsatile run. Steady pressure drop at 30 degrees rose with bend count: 115 Pa (1 bend), 205 Pa (3), 285 Pa (5), i.e. about 0.9 to 2.1 mmHg. At 120 degrees with 5 bends it was 139 Pa. No hyperaemic simulation. The summary also reports "about 15 mmHg in severe cases"; I could not locate that in the extracted table, so treat it as unverified. [PMC3419180](https://pmc.ncbi.nlm.nih.gov/articles/PMC3419180/)
- **Extreme tortuosity case [full text, fetch summary].** One patient with ≥ 2 consecutive 180-degree turns in the LAD: invasive FFR 0.37 vs CT-FFR 0.62, with post-PCI FFR only 0.67. Authors conclude extreme tortuosity lowers invasive FFR/iFR (wire straightening creates pseudo-stenoses) and recommend CT-FFR instead. n = 1. [PMC9189850](https://pmc.ncbi.nlm.nih.gov/articles/PMC9189850/)
- **Review synthesis [full text].** "In computational studies, tortuous vessels cause larger helicity [Vorobtsova 2016], and higher pressure drops [ref 255]". Some studies found high helicity from curvature protects against low TAESS; others found the opposite in idealised and patient-specific non-bifurcating geometries (Xie 2014). The review attributes the contradictions partly to inconsistent curvature metrics and recommends mean absolute curvature (Kashyap) as the most robust. Its study table records "helicity is correlated with the pressure drop; an increase in tortuosity may reduce perfusion" and "tortuosity could have protective effects". [Shen et al., "The Anatomy of Coronary Risk", local PDF, section 4 and table]
- Kashyap 2022, 127 CAD-free CCTA patients: mean absolute curvature vs low TAWSS R^2 up to 0.23; arc/chord tortuosity index not significant. [earlier tortuosity reports in `reports/`, not re-read here]
- Schultz 2023 (168 patients, 349 visually normal vessels, fixed 1 ml/s inflow, no side branches): ESS gradients largely reflect lumen diameter, and the authors concede the no-side-branch set-up inflates distal ESS. [full text, via `docs_thesis/papers/schultz2023ess.md`]
- Tortuosity is related to coronary microvascular findings in some non-obstructive cohorts but not to vasomotor dysfunction in another (228 patients). [snippet] [PMC8792852](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8792852/); [Li et al. 2020, coronary flow reserve in tortuosity](https://doi.org/10.1177/0300060520955060)

### Inferences
- [derivation] Curvature adds secondary-flow losses on top of Poiseuille loss. For coronary Dean numbers (Re about 100 to 300 at hyperaemia, r/R_c about 0.05 to 0.2) the classic curved-pipe friction correlations give roughly a 10 to 30 % increase over the straight-pipe loss for the curved segment only. Extra path length from tortuosity enters linearly through L. Both are small relative to the r^-4 radius dependence. Tortuosity should therefore move distal CT-FFR by at most a few hundredths in a healthy vessel. This order of magnitude matches Li 2012.
- A standard 1D/0D CT-FFR model sees tortuosity only through path length (and sometimes a curvature loss term). A 1D CT-FFR correlation with tortuosity would mostly be the length effect. That makes 1D CT-FFR close to redundant with (length, radius profile, V/M).
- WSS / OSI / helicity from 3D CFD are the haemodynamic quantities that are not reducible to one geometric scalar. Their extra information is local (inner-wall low WSS at bends, bifurcation flanks), so they belong to a regional analysis, not a per-vessel scalar.

### Gaps
- No clinical study found that tests tortuosity vs FFRCT or delta-FFRCT in stenosis-free vessels, adjusted for length and radius.
- Vorobtsova 2016 and Xie 2014 were not re-read here; their numbers come only via the review.
- The Dean-flow loss factor above is a textbook estimate, not taken from a coronary-specific source.

## 4. Feasibility: inputs, tools, compute, validation and reproducibility

### Takeaway
A defensible reduced-order model is feasible for thousands of trees; full 3D transient CFD is not, within 12 weeks. The binding inputs are a lumen radius profile along the tree (from segmentation, not centerlines alone) and a flow assumption (myocardial mass, or an allometric law on the tree itself). Open tools exist (SimVascular's automated 0D/1D, Blanco-type 1D models, OpenFOAM), and 1D FFR agrees with 3D to within 0.00 ± 0.03. Commercial CT-FFR (HeartFlow, Siemens cFFR prototype, DEEPVESSEL) is not usable per case at scale for this thesis. Interscan reproducibility of FFRCT is good for delta-FFRCT and worst for distal FFRCT, and depends on image quality.

### Cited Findings
- **1D vs 3D (Blanco et al.) [abstract].** 20 patients, 29 trees (9 CCTA, 20 IVUS). 1D models with lumped pressure-loss terms at stenoses and bifurcations, same boundary conditions as 3D. FFR_1D vs FFR_3D: mean difference 0.00 ± 0.03; at 0.80 cut-off AUC 0.97, accuracy 0.98. "Inexpensive FFR_1D simulations can be reliably used as a surrogate of demanding FFR_3D". [Sci Rep 2018;8:17275, arXiv 1805.11472](https://arxiv.org/abs/1805.11472)
- **Automated 0D/1D in SimVascular [abstract].** 72 public models across anatomies; 0D and 1D flow/pressure errors typically 1 to 10 % vs 3D. 0D needs about a third of 1D runtime; 3D needs hours to days on a cluster. All open-source in SimVascular. Coronary inclusion not confirmed from the abstract. [Pfaller et al., arXiv 2111.04878](https://arxiv.org/abs/2111.04878)
- **Steady vs pulsatile 3D [abstract].** 133 CT-reconstructed coronaries with invasive FFR: steady and pulsatile FFRCT correlated r = 0.988; vs invasive FFR r = 0.797; steady CFD about 30-fold cheaper. [arXiv 2408.16496](https://arxiv.org/abs/2408.16496)
- **ML CT-FFR (Itu 2016, Siemens) [snippet].** 12,000 synthetic trees with reduced-order CFD labels; deep network trained on 10,000. On 127 lesions from 87 patients: r = 0.9994 vs the physics model, 2.4 s per case. Proprietary. [PubMed 27079692](https://pubmed.ncbi.nlm.nih.gov/27079692)
- **Boundary conditions.** Van der Giessen-type laws (Q = 1.43 d^2.55 at the inlet, split (d_sb/d_mb)^2.27) are used by Shen et al.; diameter-scaled BCs reproduce normalised but not absolute WSS (Schrauwen 2016). [earlier notes, hemodynamic_geometry_proxies.md section 4] CT-FFR packages scale hyperaemic flow to myocardial mass, which is why V/M matters (see question 1).
- **WSS surrogates.** Griffo 2026 GEM-GCN: 0.48 Pa median absolute error, < 5 s per vessel, but trained on 3D-QCA of diseased single vessels, not CCTA trees. [griffo2026wss.md]; synthetic-coronary mesh surrogates in the earlier notes.
- **Interscan reproducibility [snippet].** 102 patients with known CAD scanned twice within 1 hour, identical protocol; 82 evaluable in both (79 % male, 64 ± 9 y). No difference in median FFRCT; r = 0.82 to 0.92. Agreement highest for delta-FFRCT and lowest for distal-vessel FFRCT; narrower limits of agreement with the best image quality. [JCCT 2024/25, interscan FFRCT](https://www.journalofcardiovascularct.com/article/S1934-5925(24)00523-9/fulltext); [JACC CVI 2025, test-retest](https://www.jacc.org/doi/10.1016/j.jcmg.2025.02.009)
- A search snippet reports a coefficient of variation of 3.4 % (95 % CI 1.4 to 4.6 %) for repeated FFRCT analyses, similar to repeated invasive FFR. The source paper could not be pinned down. [snippet] [ResearchGate, "Good FFRCT test-retest reproducibility"](https://www.researchgate.net/publication/391964428_Good_FFRCT_Test-Retest_Reproducibility)
- Inter-rater variability of ML CT-FFR in patients without obstructive CAD (pre-TAVR) depended on image quality, calcification and measurement location. [snippet] [PMC11395889](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11395889/)
- The review lists open and commercial solvers (OpenFOAM, SimVascular, CRIMSON, CAAS) and says FFR needs only a steady hyperaemic simulation, whereas TAESS / OSI need several transient cycles. [full text] Anatomy of Coronary Risk, section 3.1.

### Inferences
- [derivation] **Compute budget.** A steady Poiseuille network on a tree of about 20 to 50 segments is a sparse linear solve: milliseconds to seconds per tree on a CPU, so all CGPS and ImageCAS-X trees are trivial. 1D pulsatile models are minutes per tree. Steady 3D CFD on a meshed whole tree is roughly 0.5 to several CPU-hours; transient 3D for OSI is 30-fold more (per arXiv 2408.16496). That is feasible only for a small validation subset (about 20 to 40 trees), not the cohort.
- **Input readiness in this project.** The ImageCAS-X references and CAS-Net outputs are lumen masks, so a radius profile along the centerline is obtainable. Myocardial mass is not segmented anywhere in the current pipeline. Adding an LV segmentation (e.g. a TotalSegmentator-type model) is extra work. The allometric tree-root law avoids it, at the cost of ignoring lumen-mass mismatch (V/M), which is exactly the strongest known determinant of healthy CT-FFR.
- **Resolution sensitivity.** Poiseuille loss scales with r^-4, so a 10 % radius error gives about 40 % error in the segment pressure drop, and small distal vessels at 0.5 mm voxels dominate the error. Distal FFRCT being the least reproducible readout is consistent with this. Delta-based and normalised quantities are more robust.
- **Validation needs.** Without invasive FFR or 4D flow in CGPS, validation can only be internal: 1D vs steady 3D on a subset (OpenFOAM or SimVascular), and test-retest via two segmentations of the same scan (reference vs CAS-Net on ImageCAS-X).
- **Licensing.** HeartFlow is a commercial, per-case, cloud service; Siemens cFFR is a research prototype under agreement; DEEPVESSEL is commercial. None fit a master's thesis on thousands of scans without a partnership.

### Gaps
- openBF, CRIMSON and HeMoLab availability, licence and coronary validation were not checked in this pass.
- No open-source CT-FFR pipeline validated against invasive FFR on CCTA was confirmed.
- No per-case runtime for 3D steady coronary CFD from a primary source was found; the numbers above are estimates.
- No reproducibility data for CT-derived WSS on repeat CCTA were found.

## 5. Is CT-FFR the wrong tool for plaque-free baselines, and what is a minimal defensible haemodynamic descriptor in 12 weeks?

### Takeaway
Yes. CT-FFR is a stenosis-physiology index. In a plaque-free tree it reduces to a smooth decline set by length, radius and flow allocation, and its prognostic evidence is all lesion-level in existing disease. Low WSS / ESS (plus OSI, helicity) is the mechanistically relevant quantity for plaque onset, but it needs 3D CFD, which cannot scale in the time left. The minimal defensible option is a steady reduced-order network model on the lumen tree: per-segment pressure drop / delta-FFR and a tree-propagated Poiseuille WSS index, both normalised. Validate them against steady 3D CFD on a small subset, and treat them as covariates next to tortuosity rather than as a new primary endpoint.

### Cited Findings
- The review separates FFRCT/QFR (stenosis severity, PCI guidance) from anatomy-haemodynamics research (mechanism of CAD), and notes steady hyperaemic simulation suffices for FFR while TAESS/OSI need transient simulation. [full text] Anatomy of Coronary Risk, sections 3.1 and 5.
- The adverse haemodynamic features that predict ACS (delta-FFRCT, high WSS, axial plaque stress) are all measured across existing lesions. [Lee 2019 abstract](https://pubmed.ncbi.nlm.nih.gov/29550316/); [EMERALD II](https://www.jacc.org/doi/10.1016/j.jcmg.2024.03.015)
- Low ESS predicts lumen loss and progression (PREDICTION) and low WSS predicts growth even in plaque-free wall regions (Cardiovasc Res 2023), supporting WSS as the onset-relevant quantity. [PREDICTION abstract](https://pubmed.ncbi.nlm.nih.gov/22723305/); [PMC10153640, snippet](https://pmc.ncbi.nlm.nih.gov/articles/PMC10153640/)
- Normalising WSS to a reference (vessel mean or proximal healthy segment) improved agreement and prediction in two studies: Griffo (R 0.67 to 0.89 after normalisation; ratio AUC higher than raw) and the 22-patient serial CCTA study. [griffo2026wss.md]; [PMC12858539](https://pmc.ncbi.nlm.nih.gov/articles/PMC12858539/)
- Delta-FFRCT is the most reproducible FFRCT readout across repeat scans. [snippet] [JCCT interscan study](https://www.journalofcardiovascularct.com/article/S1934-5925(24)00523-9/fulltext)

### Inferences
Proposed minimal package (my synthesis, not from any one source):
1. **Steady 0D/1D Poiseuille network** on each lumen tree: inlet flow from the allometric root law (Q = 1.43 d^2.55), splits by (d_sb/d_mb)^2.27, per-segment resistance 8 mu L / (pi r^4) with r smoothed over 2 to 5 mm. Output per segment: pressure drop, a pseudo-FFR at each node (P/P_aortic), and delta-FFR over named or graph-defined segments. Cost: seconds for the whole cohort. Implemented from scratch in NumPy, or via SimVascular's ROM for cross-checking.
2. **Tree-propagated WSS index** tau_hat = 4 mu Q_i / (pi r_i^3), normalised to the root, as already derived in `hemodynamic_geometry_proxies.md`. This is the WSS-side counterpart and captures "lumen wider than its inherited flow warrants".
3. **Validation subset** of 20 to 40 ImageCAS-X trees: steady 3D CFD (OpenFOAM or SimVascular) with the same BCs, reporting agreement for pressure drop and segment-mean WSS, and the correlation of 3D inner-bend low-WSS area with kappa_a. This directly tests how much of 3D WSS the tortuosity descriptor and tau_hat already explain.
4. **Reproducibility**: reference vs CAS-Net segmentation on the ImageCAS-X test split (ICC of distal pseudo-FFR, delta-FFR, tau_hat), since no interscan data exist.
5. **Framing**: report these as physically motivated covariates that tell whether a tortuosity association survives adjustment for flow-resistance geometry, not as CT-FFR equivalents. Do not call the output "CT-FFR" or claim ischaemia relevance.

Also:
- If LV mass can be segmented cheaply, V/M is the single most evidence-backed haemodynamic-geometric scalar for healthy trees and needs no simulation at all.
- Transient 3D (OSI, helicity, TAWSS) at cohort scale is out of scope for 12 weeks. A pretrained WSS surrogate would need retraining on CCTA trees, and none was confirmed to generalise.

### Gaps
- No precedent for a reduced-order haemodynamic descriptor used as a predictor of new plaque in a population cohort, so its expected effect size is unknown.
- It is unknown how much of 3D-CFD low-WSS area in healthy trees is explained by tau_hat plus kappa_a together; that is the proposed validation experiment.
- Whether CGPS has LV segmentations or mass measurements available was not checked.
