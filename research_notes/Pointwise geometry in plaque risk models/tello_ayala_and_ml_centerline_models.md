# Tello Ayala et al. (JACC: Advances 2026) and ML models on point-wise coronary centerline geometry

Access note: The full text was read through PubMed Central (PMC13308244), using a summarising fetch tool. The ScienceDirect page returned HTTP 403. The Supplemental Methods (mmc1.docx), which hold the transformer details, could not be accessed. Everything below about architecture details beyond the main text is therefore a gap. Bibliographic metadata were checked against Crossref and Europe PMC.

## 1. What exactly does Tello Ayala et al. do?

### Takeaway
The study uses **2D invasive coronary angiography, not CCTA**. It covers the **RCA only** in a single-centre catheterisation registry (MGH, 22,334 patients). Its main product is an unsupervised, hand-defined tortuosity score: the mean absolute discrete turning angle along a skeletonised U-Net segmentation. A secondary supervised local-attention transformer takes the ordered vector of local tortuosity, plus age and sex, and classifies **concurrent** angiographic RCA CAD (any stenosis, mild or worse). It reaches AUROC 0.67, against 0.60 for logistic regression on mean tortuosity, age and sex. The study predicts no incident plaque, events or ischaemia.

### Cited Findings
- **Bibliographic details.** Authors: Tello Ayala JR, Supriami K, Swaroop S, Friedman SF, Unlu O, Halford J, Maddah M, Abou-Karam R, Pomerantsev E, Ellinor PT, Doshi-Velez F, Fahed AC. JACC: Advances 5(6 Pt 2):102829, June 2026, PMID 42312790, PMCID PMC13308244, CC BY-NC-ND 4.0, 63 references. — [Crossref](https://api.crossref.org/works/10.1016/j.jacadv.2026.102829); [Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22Tello%20Ayala%22%20AND%20tortuosity&format=json&resultType=core)
- **Stated motivation.** "Prior studies enrolled fewer than 1,000 subjects and relied on heuristic metrics." Objective: to develop and validate an automated ML-based measure of RCA tortuosity and to relate it to sex, age, CAD and risk factors. — [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- **Cohort.**
  - The source is the MGH cardiac catheterisation registry, 2000–2021: 81,798 angiograms from 31,513 patients.
  - Analysed: 38,691 RCA LAO loops from 22,334 patients.
  - Exclusions: 5,172 with no LAO RCA loop, 1,438 for poor quality or artefacts, 2,569 for inappropriate RCA length.
  - Patients with prior PCI (28.9%) or CABG (15.5%) were **not** excluded.
  - Patient-level analyses used one loop per patient, the one with the longest visible RCA.
  - Source: [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- **Input and pipeline.**
  - A U-Net was trained on the external ARCADE dataset (1,000 training and 500 validation images). Its threshold was chosen to maximise Dice.
  - The middle 20 frames of each loop were segmented, and the frame with the longest visible artery was chosen.
  - The mask was skeletonised to a centerline, and the main branch was selected automatically ("no manual intervention").
  - Source: [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- **Tortuosity metric.**
  - Discrete curvature is the turning angle between consecutive skeleton edges at each point.
  - The score averages the absolute angles and divides by π, giving a value between 0 and 1. It is described as invariant to translation, rotation and scale.
  - Observed range: 0.007–0.289.
  - **No smoothing, spline fitting or resampling of skeleton points is described in the main text.**
  - A classical arc/chord index was also computed. Its correlation with the new score was weak (Pearson r = 0.116).
  - Source: [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- **Model types.**
  - U-Net segmentation: supervised on the ARCADE masks.
  - Global tortuosity score: deterministic and label-free (not learned).
  - Local-attention transformer: operates "on the ordered vector of local tortuosity along the artery". It was trained "to predict CAD given age, sex, and the local tortuosity vector".
  - Input length, resampling, padding, hyperparameters, data split, and whether splits were by patient are **not given in the main text** (Supplement only).
  - Source: [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- **Label.**
  - "CAD was defined as any presence of stenosis (mild or more) in the RCA". It was read by the interventional cardiologist from the **same** angiogram.
  - A sensitivity analysis used stenosis anywhere in the tree.
  - Risk factors came from ICD codes, laboratory values and medications.
  - Source: [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- **Validation of the score against experts.**
  - 300 angiograms were stratified into low (n = 200) and high (n = 100) tortuosity and compared with a blinded interventional cardiologist's tortuous/non-tortuous call.
  - Low bucket: precision 85.6%, recall 83.5%, F1 84.6%. High bucket: precision 75.3%, recall 58.0%, F1 65.5%.
  - Cohen's κ = 0.52 (95% CI 0.41–0.63), "moderate".
  - Source: [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- **Associations, adjusted per SD of tortuosity.**
  - CAD: OR 1.05 (95% CI 1.03–1.08). Severe CAD: OR 1.09 (1.06–1.13). Mild and moderate CAD: not significant. Gensini score: β = 0.05 (0.04–0.07).
  - Female sex: β = 0.17. Hypertension: β = 0.06. Diabetes: β = −0.11.
  - Age was not significant after adjustment (P = 0.121). Hypercholesterolaemia and smoking were not significant.
  - Source: [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- **Discrimination.** Transformer (local tortuosity vector + age + sex): AUROC 0.67 (95% CI 0.65–0.69). Logistic regression (mean tortuosity + age + sex): AUROC 0.60 (0.58–0.63). Neither model included hypertension, diabetes, lipids or smoking. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- **Stated limitations.**
  - RCA only: "may not fully capture the more complex branching of the left coronary system". The left system has "more frequent overlap and foreshortening".
  - "the retrospective design can introduce selection bias and variability in imaging protocols".
  - Segmentation succeeded in only 78.7% of eligible loops. "real-world angiograms were not acquired with tortuosity measurement in mind".
  - Prospective validation is needed.
  - Source: [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- **Plaque and events.** Plaque appears only as a mechanistic speculation (shear stress), and was not measured. CT is mentioned only for prior studies. No events or prognosis were analysed, and the authors call for prospective outcome studies. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- **Internal inconsistencies in the article.**
  - The abstract attributes 85.6% precision to the high-tortuosity class, but the results give it for the low bucket.
  - The sample is given as 38,681 in one paragraph and 38,691 elsewhere.
  - Figure 2 says 23,334 patients rather than 22,334.
  - Source: [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- **Funding and disclosures.** NIH R01MH123804 (Doshi-Velez, Tello Ayala), NHLBI, AHA, EU and Fondation Leducq. Fahed is a cofounder of Goodpath and Avigena. No code or data availability statement was found in the main text. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)

### Inferences
- **What it shows versus what it claims.**
  - It shows a scalable, automated **descriptive** 2D tortuosity score with only moderate expert agreement (κ 0.52, high-tortuosity recall 58%).
  - It shows a tiny **cross-sectional** association with prevalent stenosis: OR 1.05 per SD.
  - "Machine learning driven" mainly refers to the segmentation. The score itself is a hand-crafted mean turning angle.
- **The AUROC gain is weak evidence for point-wise modelling.**
  - The 0.67 versus 0.60 comparison is cross-sectional and lacks risk-factor adjustment.
  - It comes from a referral (catheterisation) population with prevalent disease.
  - The CAD label comes from the same image, so stenosis can itself distort the 2D skeleton and its local turning angles (reverse causation or measurement artefact).
  - The split strategy is unverified.
  - A transformer that sees the position of curvature along the RCA may partly learn where stenoses tend to be read, rather than a geometric risk.
- **Noise handling.**
  - Turning angles on a raw pixel skeleton without smoothing are sensitive to pixel discretisation and step length.
  - The weak correlation with the arc/chord index (r = 0.116) suggests that the score is partly measuring high-frequency skeleton jitter. This is my inference, not the authors'.
  - This is a caution, not a template, for curvature from a 3D tracer.
- **Suitability as a template for the CGPS thesis.** It is poor:
  - The data differ: 2D projection angiography versus 3D CCTA.
  - The outcome differs: prevalent stenosis versus plaque incident over 10 years in a plaque-free cohort.
  - The scale differs by about 20 times: 22k patients versus about 1,000–1,200 people with about 450 events.
  - It used no prespecified hypothesis test and no adjustment for SCORE2 risk factors.
  - Its usable lesson is narrow: a global summary loses positional information, and an ordered local profile can carry more signal. Even that is shown only cross-sectionally and weakly.

### Gaps
- The transformer architecture, input length and resampling, train/validation/test split, whether splitting was by patient, and calibration could not be verified (Supplement mmc1.docx was not accessible).
- Whether any smoothing is applied in the Supplement is unknown.
- No code release was found.

## 2. Other ML models that use point-wise or sequential coronary centerline geometry

### Takeaway
Point-wise and sequence models on coronary centerlines exist mainly for **(a) cross-sectional detection** of plaque and stenosis from image intensities along the centerline (MPR-based recurrent CNNs, slice-level transformers), and **(b) FFR or haemodynamics surrogates** (GNNs, PointNet++, transformers on the tree), usually trained on CFD-simulated labels. I found **no published model that uses point-wise geometry profiles (curvature, torsion, radius/taper) on a baseline scan to predict incident plaque, plaque progression or events**. The longitudinal plaque-progression ML studies I found use segment- or patient-level summary features.

### Cited Findings
- **Zreik et al., IEEE TMI 2019;38(7):1588–1598.**
  - The model is a recurrent CNN. A 3D CNN extracts features from cubes along centerline-based MPR images, and an RNN aggregates them along the artery to classify plaque type (none, non-calcified, mixed, calcified) and stenosis (none, <50%, >50%).
  - Data: 163 patients (98 training, 65 test).
  - The MIDL 2018 version (131 patients) reported accuracies of 0.77 for plaque and 0.80 for stenosis.
  - The input is image intensity along the centerline, not a geometry profile, and the task is detection of **existing** plaque.
  - Source: [arXiv 1804.04360](https://arxiv.org/pdf/1804.04360)
- **QuantiPlaque.** A transformer on straightened vessels (3D patches) predicts the presence of plaque per slice. This is again cross-sectional detection from images. Details were only seen in a search snippet. — [PMC13173773](https://pmc.ncbi.nlm.nih.gov/articles/PMC13173773/)
- **FFR and haemodynamics on the centerline or tree (detail from search snippets; not opened):**
  - Conditional physics-informed GNN over the arterial topology (MICCAI 2023). Reported correlation with measured FFR: r = 0.89 on X-ray, r = 0.88 on CT. — [MICCAI 2023](https://conferences.miccai.org/2023/papers/135-Paper0259.html)
  - CenterlinePointNet++: surface point cloud plus centerline graph, estimating pressure drop and vFFR. — [MICCAI 2023](https://conferences.miccai.org/2023/papers/109-Paper0692.html)
  - Bi-VesTreeFormer: a transformer on centerlines split at bifurcations, predicting FFR per centerline point. — [ScienceDirect 2025](https://www.sciencedirect.com/science/article/abs/pii/S0895611125000734)
  - CorNet: point cloud to velocity and pressure fields. — [ScienceDirect 2025](https://www.sciencedirect.com/science/article/abs/pii/S0952197625014629)
  - Targets are physiology or CFD, not plaque or outcomes, and sample sizes and event counts were not verified.
- **Sakellarios, Tsompou, Kigka et al., Applied Sciences 2021.**
  - Population: 187 patients (480 vessels) with stable CAD, CCTA at baseline and after 6.2 ± 1.4 years.
  - Model: a multi-parametric ML model (risk factors, lipids, 3D imaging parameters, computed ESS and LDL accumulation) predicting site-specific progression, defined by changes in lumen area, plaque area and burden.
  - Reported accuracy: 88%.
  - The population already had CAD, the sample is small, and the features are local or segment summaries rather than learned sequence models.
  - Source: [DOAJ record](https://doaj.org/article/887844a1d32343c9bfc0ce0debfb3cc8)
- **Han et al., JAHA 2020;9(5):e013958, PARADIGM registry.**
  - The ML model predicts rapid plaque progression (annual increase in percent atheroma volume ≥1.0%). 224 patients (21%) had rapid progression.
  - Best model (clinical + qualitative + quantitative plaque features): AUC 0.83, versus 0.60 for the ASCVD score.
  - Quantitative atherosclerosis features were the most important predictors.
  - The inputs are patient-level summaries, and the cohort was a serial-CCTA registry, largely with plaque at baseline.
  - Source: [PMC7335586](https://pmc.ncbi.nlm.nih.gov/articles/PMC7335586)
- **Nannini et al., APL Bioengineering 2024.**
  - Two-stage U-Net segmentation of CCTA, trained on 281 annotated scans, Dice 0.896.
  - Tortuosity is scored as the count of branches with three or more bends of more than 45°. Tortuosity rises from proximal to distal, and calcium shows the opposite pattern.
  - The statistical analyses used manual segmentations only.
  - This is a descriptive, cross-sectional study with no prediction of outcomes.
  - Source: [PMC10807932](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10807932/)
- **Cobo et al., Sci Rep 2023.**
  - A CNN classifies tortuous versus non-tortuous from 658 invasive angiographies: accuracy (87 ± 6)%, AUC 0.96 ± 0.03.
  - The target is expert tortuosity, not an outcome.
  - Source: [PMC10333289](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10333289/)
- **Patents.** Several patents ("Systems and methods for predicting location, onset, and/or change of coronary lesions") describe ML on longitudinal geometry and haemodynamics. They are method claims with no validated results. — [USPTO 9805463](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9805463)

### Inferences
- The closest designs to "point-wise geometry → future plaque" are serial ESS/CFD studies (Sakellarios et al.; PREDICTION-type IVUS work, not searched here). These summarise local haemodynamics per segment or region rather than feeding raw profiles to a deep network, and they use small diseased cohorts.
- Sequence and graph architectures are well developed for FFR. Their training labels are dense (per point and simulated), which is very different from about 450 binary person-level events.

### Gaps
- For the FFR GNN, PointNet and transformer papers, sample sizes and whether they beat simple 1D or reduced-order baselines were not checked in full text. Only search snippets were seen.
- I did not search IVUS-based ESS progression ML studies (PREDICTION, PROSPECT-ESS) in depth.
- No study on incident plaque in a plaque-free baseline cohort with point-wise geometry input was found. Searches returned none, but this does not prove that none exists.

## 3. Evidence that point-wise geometry beats summarised geometry for plaque prediction

### Takeaway
The evidence is very thin. The only direct head-to-head I found is Tello Ayala et al.: an ordered local-tortuosity transformer reached AUROC 0.67 versus 0.60 for logistic regression on mean tortuosity, age and sex. That comparison is for **prevalent** stenosis on 2D angiograms in about 22k referral patients, without risk-factor adjustment, and with an unverified split. I found no evidence for incident plaque or events, and none at a sample size like the thesis's (about 450 events).

### Cited Findings
- AUROC 0.67 (0.65–0.69) for the transformer on the local tortuosity vector + age + sex, versus 0.60 (0.58–0.63) for logistic regression on mean tortuosity + age + sex. The label is prevalent RCA stenosis read from the same angiogram. — [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- In the same paper, the adjusted association of the global score with CAD was OR 1.05 per SD. Global tortuosity therefore adds very little cross-sectionally. — [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)

### Inferences
- **Suitability of a point-wise deep model for the thesis.** It is not suitable as the primary analysis:
  - With about 1,000–1,200 people and about 450 events, a transformer, 1D CNN or GNN on curvature and taper profiles has far more parameters than events. Overfitting and unstable cross-validated ΔC would follow.
  - There is no single prespecified LR test of a geometry block for a neural network. That conflicts with the decided design: one LR test, ΔC and calibration estimated rather than tested, and the pooled cloglog GLMM over 9 segments.
  - Tello Ayala needed about 22k patients to get a modest AUROC gain on an easier, concurrent label.
- **A defensible middle ground** that stays within a cloglog GLMM likelihood-ratio framework (my suggestion, not tested in the literature found): represent each segment's curvature and taper profile with a few prespecified functionals instead of only a mean. Candidates are max, an upper quantile, the proportion of arc length above a threshold, and the location of peak curvature relative to the segment start. These would form a slightly larger but still prespecified geometry block, or a sensitivity analysis.
  - Smoothing should be fixed before the outcome is seen, given the noise sensitivity of raw discrete turning angles that the Tello Ayala design illustrates.
- **Profile models as exploration only.** A deep profile model, if wanted, belongs in exploratory or secondary analysis, with person-split CV and clear labelling as hypothesis-generating.

### Gaps
- I found no study comparing point-wise geometry with summary geometry for **incident** plaque or events, on any imaging modality.
- I did not verify whether any FFR GNN paper reports a fair comparison against summary-feature or reduced-order baselines.
