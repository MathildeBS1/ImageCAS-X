# Literature review — coronary artery segmentation & topological characterization

Compiled 2026-08-28 via web search. Organized by thesis objective (see `CLAUDE.md`). Not exhaustive —
a starting set to read from and expand as the thesis progresses.

## Research gap (thesis positioning)

**No paper found does outlier / extreme-value detection on coronary artery topological features**
(objective 9). This looks like a genuine gap rather than a search miss — general vascular-tree feature
extraction and disease-status classification are both well covered (see below), but treating a
population's branching/tortuosity/angle features as a distribution and flagging population-level
outliers or extreme cases is not represented in the coronary literature turned up here. The nearest
analogues are in a different organ (retinal trees, RETA benchmark) or use generic tooling
(scikit-learn Isolation Forest / LOF) without domain-specific adaptation. Worth confirming this is a
real gap (not just an artifact of search terms) before leaning on it, but if it holds, it is a
legitimate novel-contribution angle for the thesis rather than just plumbing.

## Dataset provenance

"ImageCAS-X" does not appear as a published dataset name in any of the searches below — only the base
**ImageCAS** dataset (Zeng et al., 1000 CTA cases, Guangdong Provincial People's Hospital,
[arXiv:2211.01607](https://arxiv.org/abs/2211.01607)) is documented. Case count (1000), volume
dimensions, and split structure in `/dtu/blackhole/0a/224426/ImageCAS-X_dataset` match ImageCAS exactly,
but the centerlines, surfaces, and `Descriptors.xlsx` (Dominance, Disease, Image Quality) are not part
of the public ImageCAS release. **Open: confirm with supervisor where the "X" extension and the
descriptor labels originated**, so the dataset can be cited correctly in the thesis.

## Segmentation (objective 5)

- [ImageCAS: A Large-Scale Dataset and Benchmark for Coronary Artery Segmentation based on CTA](https://arxiv.org/abs/2211.01607)
  — source dataset paper; establishes the nnU-Net/3D U-Net baselines to compare against.
- [SFD-Mamba2Net: Structure-Guided Frequency-Enhanced Dual-Stream Mamba2 Network](https://arxiv.org/pdf/2509.08934)
  and [Multi-View Deformable Convolution Meets Visual Mamba](https://arxiv.org/pdf/2603.21829)
  — current (2025–2026) architecture frontier; state-space/Mamba models displacing pure transformers.
- [Anatomy Guided Coronary Artery Segmentation from CCTA Using Spatial Frequency Joint Modeling](https://arxiv.org/pdf/2512.12539)
  and [Prior-knowledge-based deep learning segmentation framework](https://pmc.ncbi.nlm.nih.gov/articles/PMC12082760/)
  — anatomical-prior-informed approaches; relevant since the dataset already carries per-branch labels
  usable as priors.
- [Fast and automatic coronary artery segmentation using nnU-Net](https://link.springer.com/article/10.1007/s10554-025-03408-8)
  — plain nnU-Net as a strong, reproducible baseline; sensible first framework given objective 5 is a
  means to the topology work, not the end in itself.

## Centerline extraction & anatomical labeling

- [Coronary Artery Centerline Extraction Using a CNN-Based Orientation Classifier](https://arxiv.org/pdf/1810.03143)
  — foundational CNN centerline-tracing method, still widely used as a component.
- [Graph neural networks for automatic extraction and labeling of the coronary artery tree](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
  — GNN-based, directly relevant to objective 6 (topology as graph learning).
- [Automated Coronary Arteries Labeling via Geometric Deep Learning](https://arxiv.org/pdf/2212.00386)
  and [Multi-graph Graph Matching for Coronary Artery Semantic Labeling](https://arxiv.org/pdf/2402.15894)
  — labeling segments to AHA/SYNTAX nomenclature via graph matching; useful if segment identity (not
  just topology) is needed for feature extraction.
- [Deep learning-based automated algorithm for labeling coronary arteries in CTA](https://pmc.ncbi.nlm.nih.gov/articles/PMC10626726/)
  — CTA-specific (rather than invasive angiography), closer to this dataset's modality.

## Topological / geometric feature extraction (objectives 6–7)

- [Same Branches, Different Trees: A Bifurcation Connectedness Metric for Coronary Artery Segmentation and FFR-CT Decision Agreement](https://arxiv.org/html/2607.28327v1)
  — very recent (2026), directly quantifies topological differences between coronary trees; closest
  methodological neighbor found for objective 6.
- [Topological Data Analysis in the Assessment of Coronary Atherosclerosis: A Comprehensive Narrative Review](https://pmc.ncbi.nlm.nih.gov/articles/PMC12190947/)
  — reviews persistent homology and Mapper applied to coronary structure; notes open problems (no
  standardized protocol, small datasets, interpretability) the thesis could position against.
- [Extraction of morphometry and branching angles of the porcine coronary arterial tree from CT images](https://pubmed.ncbi.nlm.nih.gov/19749169/)
  — classic reference method for branching-angle extraction from CT, still cited as baseline.
- [Accuracy of vascular tortuosity measures using computational modelling](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8764056/)
  — compares tortuosity metrics for numerical robustness; relevant given the dataset's anisotropic,
  case-varying voxel spacing (see `CLAUDE.md`).
- [Assessment of Dynamic Change of Coronary Artery Geometry and Its Relationship to CAD](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7165136/)
  — links geometric/tortuosity features to disease status; methodologically close to what could be done
  with the `Disease` column in `Descriptors.xlsx`.
- [Real-Time Coronary Artery Dominance Classification from Angiographic Images](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12110073/)
  — dominance classification SOTA (87–93% accuracy); less directly relevant since dominance ground
  truth is already provided, but useful for framing against classification difficulty in the literature.

## Outlier / extreme-value detection on morphological features (objective 9)

No coronary-specific paper found — see "Research gap" above. Nearest analogues:
- [The RETA Benchmark for Retinal Vascular Tree Analysis](https://arxiv.org/pdf/2111.11658)
  — same problem shape (vascular tree feature statistics) in a different organ; check their
  feature/statistics methodology for transferable ideas.
- [scikit-learn Novelty and Outlier Detection](https://scikit-learn.org/stable/modules/outlier_detection.html)
  (Isolation Forest, Local Outlier Factor) — standard toolkit referenced as the go-to generic approach.

## Associating features with outcomes (objective 10)

- [A fully automated deep learning approach for coronary artery segmentation and comprehensive characterization](https://pubs.aip.org/aip/apb/article/8/1/016103/3061557)
  — end-to-end pipeline from segmentation through anatomical characterization to risk indicators;
  closest single paper to the full objectives 5→10 chain.
- [CT Angiographic and Plaque Predictors of Functionally Significant Coronary Disease and Outcome Using Machine Learning](https://www.jacc.org/doi/10.1016/j.jcmg.2020.08.025)
  — ML models on per-segment CCTA features predicting adverse events; a template for structuring the
  outcome-association analysis.
- [Short-term and long-term outcome prediction for CAD patients using ML and multi-center data](https://www.medrxiv.org/content/10.1101/2025.05.26.25328366.full.pdf)
  — recent (2025) multi-center outcome prediction; useful for standard outcome variables/endpoints,
  given this dataset itself lacks outcome data (see `CLAUDE.md` open questions).

## Hemodynamics and geometry-plaque association (added 2026-08-29)

Verified by search; none of these were in the original survey. See `hemodynamics.md` for how they
fit the plan.

**Closest prior work — read these first.**
- [Han et al., *Association of Plaque Location and Vessel Geometry ... With Future ACS-Causing
  Culprit Lesions*, JAMA Cardiology 2022](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)
  — ICONIC nested case-control. Three adverse geometric characteristics carry **incremental
  prognostic value over stenosis severity and plaque characteristics**: more proximal location,
  location at a bifurcation, increased tortuosity. This is the strongest published geometry ->
  hard-outcome link and it validates the thesis premise. Compute these three.
- [Wang et al., *Left main coronary artery morphological phenotypes and its hemodynamic
  properties*, BioMed Eng OnLine 2024](https://biomedical-engineering-online.biomedcentral.com/articles/10.1186/s12938-024-01205-3)
  — n=76 LMs, centerline geometry -> unsupervised clustering -> 4 phenotypes -> CFD for TAWSS per
  phenotype. Cluster 2 (large bifurcation angle) showed low TAWSS near the LAD branch point.
  **This is nearly our method at small scale on one bifurcation.** Not a blocker — it is a
  template, and our differentiators are 800 vs 76 cases, whole tree vs LM only, and
  outlier/extreme-value framing rather than clustering. Must be cited and positioned against.

**Morphometric scaling.**
- [Taylor et al., *Systematic review and meta-analysis of Murray's law in the coronary arterial
  circulation*, AJP Heart Circ Physiol 2024](https://journals.physiology.org/doi/abs/10.1152/ajpheart.00142.2024)
  — pooled flow-diameter exponent **2.39 (95% CI 2.24-2.54)** over 1,070 trees, matching Kassab's
  7/3 rather than Murray's 3. Corrects the reference value for any Murray-deviation feature.
- [van der Waal et al., *Revisiting Murray's law in human epicardial coronary arteries*, Front
  Physiol 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9119389/)

**Geometry and plaque burden.**
- [*Relationship between Coronary Arterial Geometry and Atherosclerotic Plaque Burden*, review,
  2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9497479/) — the survey to read for objective 7's
  justification. Cites Friedman 1983/1993/1997 (the origin of "geometric risk factors" and the LM
  branch-angle correlation), Chatzizisis 2007 (ESS mechanism), Morbiducci 2016. Reports normal LM
  bifurcation angle **76.4 +/- 16.7 deg**, and curvature **16.7% higher** in stenotic segments.
- [Coronary artery volume index (CAVi): a novel CCTA-derived predictor of cardiovascular
  events, Int J Cardiovasc Imaging 2020](https://link.springer.com/article/10.1007/s10554-019-01750-2)
  — lumen volume / myocardial mass. **CAVi < 27.9 mm3/g: MACE 17.2% vs 4.5% over 5.4 y.**
  Near-free for us: `evaluate.py` already computes `volume_gt_ml`, and the repo already wires in
  TotalSegmentator heart masks for ADE-HTL. Best available bridge to an outcome-like endpoint.
- [Bifurcation angle and hemodynamics by CCTA-derived CFD, 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5682403/)
  — WSS changes with wider angulation (>80 deg) in stenotic models. Note the literature is
  **inconsistent on the direction** of the bifurcation-angle association; report ours, do not
  assume a sign.

**Coronary dominance reference values.**
- [*Clinical Significance of Coronary Arterial Dominance*, JAHA 2024](https://www.ahajournals.org/doi/10.1161/JAHA.123.032851)
  — right 70-89%, left 8-12%, codominant 2.5-17.5%. The wide codominance range reflects
  inconsistent *definitions*, which matters for us (see `hemodynamics.md`).
