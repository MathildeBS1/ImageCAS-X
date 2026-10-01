# Longitudinal design: linking baseline regional coronary geometry to new plaque at ~10-year follow-up (CGPS serial CCTA)

Context read before searching: `from_superviser.tex` (Bjørn: tokenise the tree, learned latent queries cross-attending to a variable node set, beware positional-encoding data hunger; Kit: embeddings will separate on heart size, dominance and branch count before shape; "main goal is the HØ dataset and matching the shape descriptors with outcome"), `tortuosity/CLAUDE.md` "Analysis design (decided 2026-09-22)" (serial CCTA target; no segment vs segment comparison within a patient; adjust for age, sex, hypertension, smoking, cholesterol; hypothesis is non-obstructive disease), and `docs_thesis/supervisor_questions.md` (item 1: CGPS predictions have no artery names; item 3: ten-year repeats confound error with change).

Evidence tags used below: **[full text]** = the page body was fetched and read; **[abstract]** = only the abstract or a registry/supplement abstract was read; **[snippet]** = only a search-engine summary was seen, treat as a lead, not a citable fact. Several publisher pages (ScienceDirect, T&F, PubMed) returned 403 or captcha, so fewer items reached full text than intended.

## Correspondence: matching regions between timepoints and across patients, and labelling unnamed binary trees

### Takeaway
Serial CCTA studies overwhelmingly match at the level of the named SCCT/AHA segment (manual landmark and bifurcation matching), not by voxel or centerline registration; automated centerline registration exists but has been validated mostly on same-scan or same-scanner pairs. For CGPS the cross-patient correspondence problem is harder than the between-timepoint one, because the binary lumen has no names; learned labelling reaches F1 around 0.95 on main branches under favourable conditions but drops sharply on side branches (septals F1 0.54), so the analysis unit should be coarse and defined by things that label reliably.

### Cited Findings
- PARADIGM defines outcome per SCCT segment: segments with no identifiable plaque at baseline are selected, and new plaque is total plaque volume at least 1 mm³ in that segment at follow-up. 9583 normal segments from 1162 patients (60.3 ± 9.2 y, 55.7% male), serial clinically indicated CCTA at intervals of at least 2 years; Cox models per segment with clinical factors, radiomics, and both. [abstract/snippet] [Prediction of the development of new coronary atherosclerotic plaques with radiomics, J Cardiovasc Comput Tomogr 2024](https://www.journalofcardiovascularct.com/article/S1934-5925(24)00032-7/abstract); [PARADIGM design paper](https://pubmed.ncbi.nlm.nih.gov/27914502/)
- The traditional serial-CCTA approach uses "anatomical landmarks to match baseline and follow-up scans"; a newer in-house tool (Cao et al.) automatically co-registers 3D lumen and vessel-wall surface models to compute local plaque thickness differences. Its validation used two phase reconstructions of the same acquisition (50 patients, 300 vessels, 320-row scanners, identical reconstruction settings), so the "true" difference is zero; this validates noise floor, not cross-scanner or ten-year registration. [full text] [Automatic quantification of local plaque thickness differences, serial CCTA, PMC10899547](https://pmc.ncbi.nlm.nih.gov/articles/PMC10899547/)
- Fully automatic nonlinear volume co-registration of serial CCTA pairs (global displacement plus local volume-preserving deformation, histogram matching of intensities first) was proposed in 2010. [snippet] [Woo et al., Med Phys 2010](https://pubmed.ncbi.nlm.nih.gov/20229898/)
- Centerline-based serial analysis steps along the centerline in 1 mm increments to obtain cross-sections, and centerline co-registration enables point-to-point matching. [snippet] [Assessment of coronary plaque progression using a semi-quantitative score, PMC2796339](https://pmc.ncbi.nlm.nih.gov/articles/PMC2796339/)
- CPR-GCN (conditional partial-residual GCN): 511 CCTA subjects, inputs are centerline position features plus image features along the branch; five-fold CV mean recall 95.8%, precision 95.4%, F1 0.955. [abstract] [CPR-GCN, arXiv 2003.08560](https://arxiv.org/abs/2003.08560). Image conditioning adds about 2 points of F1 over a position-only variant, and GCNs are more robust to synthetic gaps than the TreeLab-Net tree-LSTM. [snippet] same source.
- TreeLab-Net (tree-structured LSTM on centerline position features only): AUC above 97% for LM, LAD, LCX, RCA and above 90% for D, OM, R-PLB. [snippet] [DL labelling review, PMC10626726](https://pmc.ncbi.nlm.nih.gov/articles/PMC10626726/)
- GAT ensemble on a CNN-tracked centerline graph, 104 CCTA scans (Aalst and Amsterdam, age 47 to 85), 10 AHA classes: F1 RCA 0.90, LAD 0.86, AM 0.84, LCX 0.74, OM 0.74, D 0.73, septal 0.54; labels disconnected sub-trees; beats a prior Wolterink method (F1 0.85 vs 0.75); data not public. [full text] [Graph neural networks for extraction and labeling of the coronary tree, PMC11095121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
- Other label-only-from-geometry approaches exist (point transformer, geometric deep learning on centerlines). [snippet] [Point Transformer for coronary artery labeling, arXiv 2305.02533](https://arxiv.org/pdf/2305.02533); [Automated coronary arteries labeling via geometric deep learning, arXiv 2212.00386](https://arxiv.org/pdf/2212.00386); [TTN topological transformer, PMC10706468](https://pmc.ncbi.nlm.nih.gov/articles/PMC10706468/)

### Inferences
- Two separate correspondence problems. (a) Within patient, baseline to follow-up: because the outcome is "new plaque in region r" and the predictor is measured at baseline only, what matters is that region r is the same anatomy at both times. Named segments, or arc length from the ostium along a named main vessel, suffice; fine voxel registration is not needed and would be undermined by scanner change. (b) Across patients: the design in `tortuosity/CLAUDE.md` (compare across patients, never segment vs segment within a patient) requires that region r means the same thing in every patient. This is the binding constraint for CGPS.
- ImageCAS-X is the natural training set for a labeller that works on CAS-Net binary lumens, since it has 800 labelled trees with the same kind of input (binary lumen, centerlines). A position-only model (TreeLab-Net style, or a GNN on the `topology/` centerline graph) matches the CGPS input; CPR-GCN's image conditioning would need the CGPS image, which is available, but adds domain-shift risk across scanners.
- Given the per-class F1 above, commit a priori to a coarse region scheme that labels reliably: LM, proximal/mid/distal LAD, proximal/distal LCX, proximal/mid/distal RCA (by arc-length fractions of the labelled main path), and treat side branches (D, OM, septal) as pooled "side-branch" regions or exclude them. Report labeller accuracy on a held-out ImageCAS-X split and on a small manually labelled CGPS subset (for example 30 trees) so misclassification rate is known.
- A label-free fallback that needs no learned labeller: split at the ostia (left vs right tree), take the main path by largest radius or longest arc, express position as normalised arc length from the ostium, and bin into thirds. This is "arc-length alignment from ostium" and is sufficient for a GAM along the vessel (next section).
- Between-timepoint matching of the plaque outcome: if follow-up plaque is read per SCCT segment by a CGPS reader, the geometry regions must be mapped onto the same segment scheme. Otherwise map follow-up plaque onto baseline arc length by anchoring at the ostium and the first major bifurcation(s), then linear arc-length interpolation between anchors (a landmark-piecewise-linear registration; inference, no cited validation found).

### Gaps
- No published validation found of automated centerline registration across different scanner generations over about 10 years.
- No labeller accuracy reported on segmentation-model-derived (rather than expert-traced) trees from a population cohort; this must be measured in-thesis.
- How CGPS readers scored plaque (per SCCT segment, CAC only, or quantitative plaque volume) at each visit is not established from public sources; must be confirmed with the supervisors.

## Statistics: region-level outcomes nested in vessels nested in patients

### Takeaway
The clean primary model is a mixed-effects (or GEE) logistic model for "new plaque yes/no" per baseline-plaque-free region, with random patient intercept (optionally vessel nested in patient), region type as a fixed effect, and the descriptor entered as a within-region-type standardised value; PARADIGM used per-segment Cox, which only makes sense with scan-interval variation or multiple scans. Arc-length GAMs are the natural spatial extension.

### Cited Findings
- PARADIGM new-plaque analysis at patient level: 1343 patients with suspected CAD, median interval 3.3 y (IQR 2.6 to 4.8), new lesions in 35.0% without and 46.7% with baseline plaque; baseline plaque OR 1.84 (1.38 to 2.46), diabetes and higher BMI also predictors; new obstructive lesions rare (0.9% vs 0.7%). Logistic regression adjusted for covariates and CT interval. [abstract] [PARADIGM new plaque formation, EHJ-CI 2025 supplement](https://academic.oup.com/ehjcimaging/article/27/Supplement_1/jeaf367.317/8446296)
- PARADIGM radiomics study used Cox models at segment level for new plaque (TPV ≥ 1 mm³). [abstract/snippet] [J Cardiovasc Comput Tomogr 2024](https://www.journalofcardiovascularct.com/article/S1934-5925(24)00032-7/abstract)
- GEE has been used in CCTA segment-level analyses to account for within-patient clustering. [snippet] [PARADIGM cluster analysis, Sci Rep 2021](https://www.nature.com/articles/s41598-021-96616-w); [Predictors of inaccurate stenosis assessment, JACC CV Imaging 2013](https://www.jacc.org/doi/10.1016/j.jcmg.2013.02.011)
- PREDICTION (serial IVUS, Japan, Stone et al., Circulation 2012;126:172-81): local endothelial shear stress and plaque characteristics predicting progression, analysed along short arterial subsegments. [snippet; full text not retrieved] [PubMed 22723305](https://pubmed.ncbi.nlm.nih.gov/22723305/)
- A CFD serial-CCTA study reported normalised minimum WSS (OR 0.38) and maximum helicity (OR 1.44) as predictors of progression. [snippet, small preliminary study] [J Cardiovasc Transl Res 2025](https://link.springer.com/article/10.1007/s12265-025-10735-7)

### Inferences
- Unit and risk set: regions plaque-free at baseline (as PARADIGM), outcome new plaque at follow-up. Secondary: plaque volume or segment-involvement change as a continuous or zero-inflated outcome (two-part or Tweedie model) if quantitative plaque is available.
- Primary model, in R `lme4`/`glmmTMB` notation: `newplaque ~ z_desc + region_type + age + sex + htn + smoking + ldl + statin_between + interval + scanner_pair + (1 | patient)`, with `(1 | patient/vessel)` as sensitivity. Standardise the descriptor within region type using ImageCAS-X or CGPS-baseline reference distributions, so "per SD" is comparable across regions and a region-type × descriptor interaction tests whether the effect differs by location. This respects the "no within-patient segment vs segment" rule because the descriptor contrast is between patients at the same region type; the patient random intercept absorbs patient-level propensity.
- Separate within- and between-patient effects (Mundlak / within-between decomposition): add the patient mean of the descriptor as a covariate. The between-patient coefficient is the cross-patient question in `tortuosity/CLAUDE.md`; the within coefficient is what that rule says not to interpret.
- GEE vs mixed: GEE (exchangeable working correlation, robust SE) gives population-averaged ORs and is robust to misspecified correlation; mixed-effects gives subject-specific ORs, larger in magnitude when between-patient variance is large. Report GEE as primary if the goal is an epidemiological OR, mixed as sensitivity; with only about 8 to 15 regions per patient both are feasible.
- Time-to-event: with only two scans there is no event time, only interval-censored status. Cox on segments (as PARADIGM) is defensible only with varied intervals; with a near-constant ~10-year gap, logistic with interval as covariate (or complementary log-log with log(interval) offset, which is the discrete-time interval-censored hazard) is more honest. Frailty Cox and joint longitudinal-survival models need more than two imaging visits or a clinical event endpoint (MI, death from registry linkage); the latter is the natural second outcome in CGPS.
- Spatial models along arc length: a binomial GAM (`mgcv`) with `s(arc_norm, by = vessel)` for baseline location risk plus the local descriptor, and `s(patient, bs = "re")`. If descriptors are computed as curves along the centerline (curvature profile), functional logistic regression (scalar-on-function) is the principled alternative to hand-binned regions, at the cost of interpretability. Spatial autocorrelation between adjacent regions of the same vessel is handled by the vessel random effect or an AR(1) along arc length.
- Multiple testing: declare one primary descriptor and one primary outcome (as already decided for tortuosity); treat the remaining descriptors as secondary with Holm or FDR control, and treat region-type interactions as exploratory.
- Power (Hsieh-type formula for a standard-normal covariate in logistic regression, n = (z_{1-α/2} + z_{1-β})² / (p(1−p) β²), my calculation, not from a source): OR 1.3 per SD (β = 0.262), α 0.05, power 80%, new-plaque region prevalence p = 0.20 gives about 710 independent regions; p = 0.10 gives about 1270. Multiply by the design effect 1 + (m − 1)ρ for a patient-level-clustered predictor (m = 10 regions, ρ = 0.1 gives 1.9), by about 1/(1 − R²) for correlation with covariates (R² = 0.2 gives 1.25), and by about 1/λ² for measurement error (next section). Worked chain for p = 0.2: 710 × 1.9 × 1.25 × 2.04 (λ = 0.7) ≈ 3,450 regions, about 345 patients with 10 regions each. Bonferroni over 5 descriptors multiplies by about 1.7.

### Gaps
- Could not retrieve PARADIGM full-text statistical details (random effects vs GEE for segment clustering) or PREDICTION's subsegment analysis model because of 403/captcha.
- No published serial-CCTA study found that relates baseline curvature or tortuosity (as opposed to WSS/plaque features) to new plaque per segment.
- No real estimate of the within-patient intraclass correlation of new-plaque outcomes across segments found; the ρ = 0.1 above is an assumption to replace with CGPS or PARADIGM values.

## Covariates, confounders, and scanner change over ten years

### Takeaway
Adjust for the prespecified risk factors, statin exposure between scans, interval, and heart size and dominance; treat the baseline scanner and reconstruction as a batch variable. ComBat-family harmonisation is well established for imaging features but assumes scanner is not confounded with biology; since the predictor is measured only at baseline, the key harmonisation is across baseline scanners, while follow-up scanner change mainly affects outcome ascertainment.

### Cited Findings
- CGPS CCTA: 9533 asymptomatic persons aged 40 or older without known IHD; 46% had some CAD, 10% obstructive (≥50%), 10% extensive (plaque in at least a third of segments); extensive non-obstructive disease adjusted RR 2.70 for death or MI. Extent defined by segment count. [abstract] [Fuchs et al., Ann Intern Med 2023](https://www.acpjournals.org/doi/10.7326/M22-3027)
- CGPS already used two different MDCT scanners and compared a calibrated calcium mass score across them. [snippet] [Eur J Radiol, CGPS calibrated mass score](https://www.sciencedirect.com/science/article/abs/pii/S0720048X16304272)
- ComBat estimates additive and multiplicative batch effects by empirical Bayes and has harmonised CT, MRI and PET radiomic features; limitations: assumes normal errors, fails with multimodal feature distributions or unknown/multiple imaging parameters; generalised variants address these. [full text of abstract page] [Generalized ComBat, Sci Rep 2022](https://www.nature.com/articles/s41598-022-08412-9)
- Reconstruction-kernel normalisation and ComBat improve reproducibility of handcrafted CT features across kernels. [snippet] [PMC9030848](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9030848/)
- Longitudinal ComBat (ADNI, 663 participants) models scanner effects inside a mixed model; more powerful for longitudinal change and better type I error than including scanner as a covariate on unharmonised data. [abstract] [Beer et al., NeuroImage 2020](https://www.sciencedirect.com/science/article/pii/S1053811920306157)
- Traveling-subject validation shows ComBat does not remove all scanner effects. [abstract] [Validation of cross-sectional and longitudinal ComBat, travelling subjects](https://www.sciencedirect.com/science/article/pii/S2666956022000605)

### Inferences
- Confounders: age, sex, hypertension, smoking, LDL or total cholesterol, diabetes, BMI (PARADIGM found diabetes and BMI predictive), statin use between scans (it changes plaque trajectory and is likely prescribed because of baseline risk), scan interval. Heart size (for example LV mass or a tree-length surrogate) and dominance matter mainly because both drive raw geometry (Kit's point); normalising descriptors by vessel length or radius and adjusting for dominance-derived region availability avoids size confounding. Dominance itself is only available on CGPS if the labeller provides it.
- Harmonisation plan: (1) prefer scale-free descriptors (curvature normalised by radius, tortuosity indices) that are less resolution sensitive; (2) quantify resolution sensitivity directly on ImageCAS-X by downsampling/reblurring volumes to the older scanner's in-plane and slice spacing, re-segmenting and re-measuring (a digital phantom; inference, no cited precedent); (3) include baseline scanner/kernel as a covariate, with ComBat (preserving age, sex, outcome) as sensitivity; (4) never harmonise with the outcome as a protected covariate omitted, or ComBat removes real signal if scanner is confounded with calendar time and risk.
- Outcome ascertainment differs by scanner generation: newer follow-up scanners detect smaller plaques, inflating "new plaque" rates at follow-up. This biases the incidence level but not the between-patient contrast if all patients switched scanner together; if follow-up scanner varies, include it as a covariate.
- Cardiac phase and heart rate at baseline alter curvature; record and adjust (already flagged in `tortuosity/CLAUDE.md`).

### Gaps
- Public details of which scanners and kernels CGPS used at each visit, and whether any participants had both scanners at one visit (which would allow direct calibration), were not found.
- No published ComBat application to coronary centerline geometric descriptors found.

## Measurement error: regression dilution, ICC, and required sample size

### Takeaway
Classical error in the baseline descriptor attenuates the log-OR by approximately the reliability ratio λ (the ICC from repeat measurement), which inflates required sample size by about 1/λ²; λ must come from short-interval repeats (repeat segmentation or repeat manual labelling on the same scan, or same-day phases), not the ten-year pairs.

### Cited Findings
- Frost and Thompson (2000) compare six methods (regression-based and correlation-based) to estimate the regression dilution ratio from repeat measurements in a subset or a separate study, then correct the fitted slope. [abstract] [Frost and Thompson, JRSS-A 2000;163:173-189](https://rss.onlinelibrary.wiley.com/doi/10.1111/1467-985X.00164)
- The slope is biased by the reliability ratio, the variance of the usual (true) values divided by the variance of the observed values. [snippet] [Regression dilution bias: tools for correction and sample size, Ups J Med Sci 2012](https://www.tandfonline.com/doi/full/10.3109/03009734.2012.668143)
- Same-scan phase-to-phase plaque-thickness co-registration is used to establish a zero-change noise floor. [full text] [PMC10899547](https://pmc.ncbi.nlm.nih.gov/articles/PMC10899547/)

### Inferences
- For logistic regression with rare-ish outcome and normal classical error, observed log-OR ≈ λ × true log-OR (regression calibration approximation). With λ = 0.7, true OR 1.3 per SD appears as about 1.20; with λ = 0.5, about 1.14. Required n scales by about 1/λ²: 2.0 at λ = 0.7, 4.0 at λ = 0.5. Regional descriptors on short segments (tortuosity on 20 mm) are likely to have lower ICC than whole-vessel ones, so region length is a reliability versus locality trade-off that should be chosen with the ICC in hand.
- Sources of λ available without a short-interval CGPS rescan: (a) CAS-Net vs expert label on ImageCAS-X test split (segmentation error component); (b) two segmentations (for example CAS-Net and a second model, or two TTA settings) on the same CGPS scan; (c) two cardiac phases of the same CGPS acquisition if reconstructed. The ten-year pairs give an upper bound on combined error plus change only (`supervisor_questions.md` item 3).
- Correct via regression calibration using the λ estimate (and bootstrap the CI), and report both naive and corrected ORs.
- Differential error: if baseline image quality differs by risk (obesity, heart rate), error is not classical; adjust for Image Quality or BMI and check that descriptor ICC does not vary by those.

### Gaps
- No published ICC for regional curvature/tortuosity from automated segmentations was retrieved here (earlier reports in `reports/` cover whole-vessel tortuosity reproducibility; not repeated).
- The exact logistic attenuation factor under non-rare outcomes is not closed form; a simulation on the planned design would give a better number than the approximation.

## Precedents: serial natural-history studies and population cohorts with repeat CCTA

### Takeaway
PARADIGM is the main serial-CCTA precedent and defines new plaque per SCCT segment as TPV ≥ 1 mm³ in baseline plaque-free segments over ≥2 years (median 3.3). EMERALD is a case-control culprit-lesion study, not serial. PREDICTION is serial IVUS over months in patients with ACS. No population-based cohort with ~10-year repeat CCTA was found in the literature, which makes CGPS repeat scanning novel and also means there is no direct design template.

### Cited Findings
- PARADIGM: prospective multinational registry of 2252 consecutive patients with clinically indicated serial CCTA. [abstract/snippet] [J Cardiovasc Comput Tomogr 2024](https://www.journalofcardiovascularct.com/article/S1934-5925(24)00032-7/abstract); [design paper](https://pubmed.ncbi.nlm.nih.gov/27914502/). New-plaque segment definition and results as in section 1 and 2.
- PARADIGM review: "Where, why and how fast" summarises location and rate of progression findings. [snippet] [J Cardiovasc Comput Tomogr 2021 review](https://www.journalofcardiovascularct.com/article/S1934-5925(21)00464-0/abstract)
- PARADIGM practical CCTA risk score for progression of non-obstructive plaque. [snippet] [Eur Radiol 2023](https://link.springer.com/article/10.1007/s00330-023-09880-x)
- EMERALD: 66 culprit vs 150 non-culprit lesions (case-control, CCTA preceding ACS); adverse plaque characteristics plus hemodynamics (FFRCT ≤ 0.80, ΔFFRCT ≥ 0.06, WSS ≥ 154.7 dyn/cm², axial plaque stress ≥ 1606.6 dyn/cm²) had incremental value. Lesions already existed at baseline, so EMERALD addresses plaque destined to rupture, not new plaque. [abstract] [Lee et al., JACC CV Imaging 2019, PubMed 29550316](https://pubmed.ncbi.nlm.nih.gov/29550316/)
- EMERALD II extends this to prognostic time frames. [snippet] [JACC CV Imaging 2025](https://www.jacc.org/doi/10.1016/j.jcmg.2025.02.003)
- PREDICTION (Stone 2012): serial IVUS with ESS profiling in ACS patients. [snippet] [Circulation 2012, PubMed 22723305](https://pubmed.ncbi.nlm.nih.gov/22723305/)
- CGPS: 9533 asymptomatic participants with CCTA at baseline; outcome linkage to MI and death. [abstract] [Fuchs et al., Ann Intern Med 2023](https://www.acpjournals.org/doi/10.7326/M22-3027)

### Inferences
- The thesis can adopt the PARADIGM segment-level definition (baseline plaque-free segment, new plaque at follow-up) directly, which makes results comparable; its population (symptomatic, clinically indicated, 3 y) differs from CGPS (asymptomatic general population, ~10 y), and that difference should be stated.
- PARADIGM's patient-level new-lesion rate of 35% in 3.3 y for patients without baseline plaque suggests region-level incidence over ten years in an older general population may be high enough (p of 0.1 to 0.2 per region) to make the power calculation above realistic, but that is extrapolation.
- Geometry-to-plaque precedents are hemodynamic (WSS, helicity) rather than purely geometric; curvature and tortuosity act through WSS, so a geometric descriptor result should be framed as a WSS proxy unless CFD is run.

### Gaps
- SCOT-HEART and MESA: no repeat-CCTA natural-history component found in this search (MESA's repeats are CAC scans, from memory, unverified here).
- Size of the CGPS repeat-scan subset, interval distribution, and plaque reading protocol at follow-up: unknown from public sources.

## Graph/tokenised tree with learned latent queries in a small-data longitudinal setting

### Takeaway
With a few hundred patients and a binary region outcome, a learned set-encoder should be an ablation over a pre-registered per-region feature model, not the primary analysis. Its most defensible role is pretraining the representation on ImageCAS-X (800 trees, self-supervised or label-prediction) and on all CGPS baseline trees (thousands, unlabelled), then freezing it and feeding per-region pooled embeddings into the same mixed model.

### Cited Findings
- Supervisor proposal: tokenise the tree with node features (xyz, radius, arc length from root, depth, L/R), fixed learned latent queries cross-attending to a variable node set; caution that transformer positional encodings need large data; consider anatomically realistic augmentation. Kit: embeddings will likely separate on heart size, dominance and branch count; normalise; start simpler. [full text] `from_superviser.tex` (local)
- GNNs on coronary centerline graphs already achieve high branch labelling accuracy from position features on hundreds of scans, showing the graph representation is learnable at this data scale for a well-posed supervised task. [abstract/full text] [CPR-GCN](https://arxiv.org/abs/2003.08560); [PMC11095121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)

### Inferences
- The correspondence problem Bjørn raises is the same problem as section 1. Solving it with the labeller (region type per node, plus normalised arc length within region) gives each token an anatomical identity, which replaces generic positional encodings with anatomical ones and reduces the data requirement he warns about.
- Primary (interpretable): per-region handcrafted descriptors → mixed/GEE logistic. Ablation 1: same model plus learned region embedding (region-pooled latent, reduced by PCA to a few components) to test incremental value with a likelihood-ratio test or ΔAUC under patient-grouped cross-validation. Ablation 2: learned model alone. Report whether the learned embedding correlates with the handcrafted descriptor and with heart size/dominance (Kit's concern), which is the interpretability check.
- Keep outcome labels out of representation training (train on ImageCAS-X and unlabelled CGPS baselines only), otherwise the few hundred longitudinal patients are used twice and inference becomes optimistic; any supervised fine-tuning on the longitudinal outcome needs nested, patient-grouped cross-validation.
- Latent queries give a patient-level (whole-tree) vector; for a region-level outcome, pool attention outputs per region or read out node embeddings, otherwise the model answers a patient-level question the design says is out of scope.

### Gaps
- No published use of set/graph transformers with learned latent queries (Perceiver-style) on coronary trees for outcome prediction was searched for or found in this pass.
- No evidence on how many trees are needed for a coronary-tree self-supervised encoder to yield stable embeddings.
