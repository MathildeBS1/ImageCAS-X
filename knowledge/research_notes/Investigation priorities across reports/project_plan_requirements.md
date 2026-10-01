# What the thesis plan and supervisors actually require

Scope: internal documents only. Citations are repo-relative file paths with line numbers (paths
relative to `/zhome/e2/6/224426/project/ImageCAS-X/`). `CLAUDE.thesis.md` does not exist in the
repo (checked 2026-09-26), so it was not available as a source. No Descriptors.xlsx, val or test data
was opened.

## 1. Numbered objectives, deliverables, learning objectives, research question and gap

### Takeaway
The thesis has ten objectives, identical in substance to the supervisor-issued learning objectives,
which run from clinical description (1 to 3) through state of the art (4), a segmentation framework (5),
topological characterisation methods and features (6 and 7), to cohort-scale population statistics
(8), outlier/extreme-value detection (9) and association with outcome (10). Nothing in the objectives
mentions representation learning, embeddings, graphs or phenotype clustering; those come only from
the supervisor emails and the student's own week 2 and 3 notes. The stated gap is population-scale,
tree-scale geometry described as a distribution, with its tails flagged.

### Cited Findings
- Overall goal: "develop and validate a computer-vision framework that segments the coronary artery
  tree from coronary computed tomography angiography and characterizes its topology, and to apply it
  to a large population cohort" — [thesis/project_plan.tex:6-8](thesis/project_plan.tex)
- The ten objectives, in order — [thesis/project_plan.tex:13-30](thesis/project_plan.tex):
  1. Describe heart function, focus on coronary arteries.
  2. Describe how CT records and visualises the coronaries.
  3. Describe common coronary topology and anatomical variants.
  4. Review state of the art in coronary segmentation and topological description.
  5. Implement, validate and document a state-of-the-art segmentation framework.
  6. Develop, implement, revise and validate methods for topological characterisation of coronary trees.
  7. Extract topological features "such as branching pattern, dominance, bifurcation angles and tortuosity".
  8. Apply the framework to a large cohort; population descriptions and statistics.
  9. Implement and test outlier detection and extreme-value detection of the topological features.
  10. Associate the topological features with patient outcome.
- The learning objectives (from the supervisor, "should only be taken as a rough guide") are the same
  ten items almost word for word, including "Extract topological features like branching patterns,
  dominance, angles, and tortuosity" and "Implement and test outlier detection and extreme value
  detections of topological features" — [learning_objectives.md:1-14](learning_objectives.md)
- Plan deliverables mapped to objectives: feature reliability vs ground truth on 160 ImageCAS-X test
  cases (obj. 5 to 7); repeat-scan reproducibility with per-feature measurement error and minimum
  detectable change (obj. 6); population description and normative reference ranges (obj. 8); outlier
  and extreme-value detection (obj. 9); association of baseline geometry with plaque progression at
  locations plaque-free at baseline (obj. 10); MACE risk-prediction model, baseline clinical model vs
  model adding topological features "both continuous measurements and the population-outlier flags
  ... (obj. 9, e.g. top-5% tortuosity)" (obj. 10) — [thesis/project_plan.tex:55-90](thesis/project_plan.tex)
- Gap as stated by the student's research: "no study measures tree-scale geometry across a population
  of thousands, describes its distribution, and asks which individuals fall outside it. The field's
  machine learning went to plaque radiomics instead, and its graph neural networks model patient
  similarity or segment labels rather than tree topology." — [docs_thesis/find_research.md:555-565](docs_thesis/find_research.md)
- Direction in three sentences: field is at lesion scale; tree-scale geometry is studied in cohorts one
  to two orders of magnitude smaller; "This thesis goes up-scale: measure tree topology across
  thousands, describe its distribution, and ask which individuals fall outside it" — [docs_thesis/state_of_the_art_plan.md:10-16](docs_thesis/state_of_the_art_plan.md)
- The Shen 2026 review is used to anchor three needs the aim has: a construction turning a segmented
  tree into a measurable object (whole tree, not just left main); features "a machine computes
  identically every time"; a cohort "large enough and healthy enough" — [thesis/shen2026_gaps.tex:25-72](thesis/shen2026_gaps.tex)
- Shen recommends statistical shape analysis for combining many shape factors, which the note maps
  to objective 8 — [thesis/shen2026_gaps.tex:63-70](thesis/shen2026_gaps.tex)
- Objective 9 has no external endorsement from Shen: "outlier, extreme value and anomaly appear nowhere
  in it ... Objective 9 gets no endorsement here" — [thesis/shen2026_gaps.tex:158-161](thesis/shen2026_gaps.tex)
- The student's own framing of the more interesting question: "whether the topology of the tree carries
  any signs of risk before disease develops" — [thesis/weekly_report_02.tex:26-33](thesis/weekly_report_02.tex)
- Three constraints the thesis addresses: "the population is selected for disease, each participant is
  imaged once, and the description is never tested against what happens afterwards" — [thesis/week2/healthy_cohort.tex:42-44](thesis/week2/healthy_cohort.tex)

### Inferences
- The formal requirement is a descriptor pipeline plus population statistics plus outlier flags plus
  an outcome model. Representation learning could serve objectives 6, 8 or 10, but no objective
  demands it; objectives 7 and 9 are explicitly about named, hand-computable features (tortuosity,
  angles, dominance) and flagging their extremes (e.g. top-5% tortuosity).
- The written research gap ("distribution ... who falls outside it") is a descriptive/statistical gap,
  not a representation gap. A recommendation that centres learned embeddings needs to show how it
  still produces a distribution and tails that can be read clinically.

### Gaps
- `thesis/concepts.tex:38-39` refers to "research question 2" (repeat-scan measurement floor) and
  "question 4" (outcome-linked subset), but no file found defines a numbered list of research
  questions. The four questions are implied only (possibly the three constraints in
  `healthy_cohort.tex:42-44` plus outcome). No single stated research question exists in the
  documents read.

## 2. Timeline and current position

### Takeaway
Week 1 began 31 August 2026; today (26 September 2026) is the end of week 4, with week 5 starting 28
September. Report submission is 22 December, oral presentation 5 January. About 12 working weeks
remain, and the plan puts all CGPS deployment and analysis (weeks 7 to 14) into that window. ImageCAS-X
Track A is roughly on plan; Track B (CGPS access) shows no evidence of having started.

### Cited Findings
- Week 1 is "31-4. September 2026" — [thesis/weekly_report_01.tex:19](thesis/weekly_report_01.tex); week 2 is 7 to 11 September — [thesis/weekly_report_02.tex:21](thesis/weekly_report_02.tex); week 3 is 14 to 18 September — [thesis/weekly_report_03.tex:21](thesis/weekly_report_03.tex); latest commits are titled "week4"/"week 4" on 21 and 23 September (git log).
- Plan schedule — [thesis/project_plan.tex:47-93](thesis/project_plan.tex):
  - Weeks 1 to 2: kick-off, clinical background, literature (obj. 1 to 4), dataset chapter.
  - Track A, weeks 3 to 4: understand the segmentation method; topology feature extraction on
    ImageCAS-X (branching, bifurcation angles, tortuosity, dominance); feature reliability vs ground truth
    on 160 test cases (obj. 5 to 7). Risk 3.
  - Week 5: topology-aware fine-tuning targeting week 3 failure modes, "if the gap is large enough to justify it". Risk 3.
  - Weeks 5 to 6: ground-truth-free inference path and per-scan connectivity QC for CGPS. Risk 2.
  - Track B, weeks 2 to 3: CGPS data access and exploration (repeat-scan intervals, outcomes, MACE). Risk 5 (highest).
  - Week 4: training in in-house labelling software; weeks 5 to 6: annotate a small CGPS subset.
  - Weeks 7 to 10: CGPS deployment, accuracy validation and domain shift, anatomical correspondence
    between repeat scans, repeat-scan reproducibility, population description and normative ranges.
  - Weeks 11 to 14: outlier/extreme-value detection; plaque progression association (risk 5); MACE
    risk model (risk 5).
  - Weeks 15 to 16: writing. 22 December submission; 5 January oral.
- `ThesisPlan.md` is an older copy with the merged block spanning weeks 7 to 14 instead of 7 to 10 — [ThesisPlan.md:30-45](ThesisPlan.md)
- The student already flagged: "It might be too ambitious, depending on how hard getting started with CGPS will be" — [thesis/weekly_report_01.tex:36-37](thesis/weekly_report_01.tex)
- Done so far (Track A): tree graph built from delivered centerlines; first features (bifurcation angle,
  angle with local branch volume, tortuosity split into L/D, curvature, torsion/non-planarity,
  inflections/SOAM); radius per centerline point from the mask distance transform; CAS-Net pipeline
  reproduced end to end (5-epoch from-scratch run, full inference/eval from delivered weights) — [thesis/weekly_report_03.tex:25-45](thesis/weekly_report_03.tex)
- Topology post-processing (Qiu 2025 reconnection) was implemented and evaluated on the 160 test scans
  by 2026-09-15 — [memory: project_qiu_reconnection.md] (user auto-memory, not a thesis document)
- Week 4 was to be spent at a Microsoft hackathon; planned work: features on predicted centerlines vs
  delivered, and "Start looking into representation-learning approaches for the tortuosity features" — [thesis/weekly_report_03.tex:53-63](thesis/weekly_report_03.tex)
- CGPS: "no exact figure from the Copenhagen General Population Study appears here, or anywhere in
  thesis/, until data access" — [thesis/concepts.tex:175-176](thesis/concepts.tex); the week 1 questions still ask "What is the timeline for getting started with CGPS?" — [thesis/weekly_report_01.tex:42-48](thesis/weekly_report_01.tex)

### Inferences
- With CGPS data access apparently not yet granted at end of week 4 (plan said weeks 2 to 3), Track B
  is at least two weeks behind, and it carries the only risk-5 items. Anything that consumes weeks 5 to
  10 on ImageCAS-X-only method development competes directly with the CGPS phases that deliver
  objectives 8 to 10.
- The feature-reliability deliverable for weeks 3 to 4 (features on predicted vs delivered
  centerlines, on 160 test cases) is listed as next-week work in week 3's report, so it is likely still
  open.

### Gaps
- No document confirms whether CGPS access has been granted, or whether labelling-software training
  (week 4) happened. No week 4 report exists in `thesis/`.
- Exact week boundaries after week 4 are inferred by counting from 31 August, not stated.

## 3. What the supervisors asked for or warned against, and tensions

### Takeaway
Three people appear: Kit (dataset author and repo owner; main thesis supervisor by context), Bjørn
(LA/LAA shape-feature researcher) and Phillip (CGPS contact). Bjørn pushes a learned representation of
the tree (tokenised graph with anatomical correspondence, latent-query cross-attention, descriptors
kept as interpretable inputs and ablations). Kit originally raised representation learning, but then
explicitly told the student not to get bogged down in it, to try simpler approaches first, and to use
ImageCAS-X to develop shape descriptors and compute statistics on them, with the Herlev–Østerbro
outcome link as the main goal. That is a real tension on priority, although both agree on
interpretability, graphs with per-vertex features, and normalisation.

### Cited Findings
Identity notes: the file holds three undated emails. Emails 1 and 2 are signed "bjørn"/"Bjørn" — [from_superviser.tex:19,38](from_superviser.tex). Email 2 says "A lot of my work has been about identifying robust and clinically interpretable features for the LA+LAA" and "I had a brief talk with Kit after the meeting" — [from_superviser.tex:25-27](from_superviser.tex). Email 3 is unsigned and says "I spoke with Bjorn after the meeting" and "The reason I suggested representing learning" — [from_superviser.tex:42-44](from_superviser.tex), so it is most plausibly Kit. The repo is a fork of Kit's — [thesis/weekly_report_01.tex:31](thesis/weekly_report_01.tex); Kit is `bransby2026imagecasx`'s author by the merge "from kitbransby/main" (git log).

Bjørn, email 1 (replies to the week 3 "bounded by whatever finite set of descriptors" question, so likely the most recent):
- "more important to find a strong representation of the CAs than to craft a big set of descriptor features. Maybe establish baseline model without any 'major' feature engineering and experiment with adding more as ablation" — [from_superviser.tex:4](from_superviser.tex)
- Descriptors should give the model information not trivially extractable from the chosen representation; an interpretable feature set "saves you from black-box nature of NNs" and raises the chance the NN learns something interpretable — [from_superviser.tex:6-9](from_superviser.tex)
- Binary volumes make no sense (CAs too sparse), "Even sparse convolutions does not really sit right with me" — [from_superviser.tex:11](from_superviser.tex)
- Graph correspondence issue: vertices at the same sequence position mapping to different anatomy; need "a good CA -> graph algorithm", normalise distances "so it's purely the tree-structure remaining"; "Essentially you want to tokenize your tree" — [from_superviser.tex:12](from_superviser.tex)
- Start with node features "xyz coordinates, lumen radius, arc-length from root, depth, L/R embedding"; "variable length input - fixed length embeddings", e.g. "a fixed set of learned latent queries cross-attending to a variable-size node set" — [from_superviser.tex:14](from_superviser.tex)
- Warning: "Be careful when using transformers"; positional encodings need a lot of data ("20k+ data points for language"); consider "anatomically realistic data augmentation" — [from_superviser.tex:16](from_superviser.tex)

Bjørn, email 2:
- Understands the goal as categorising typical CA variation into classes/phenotypes, "Perhaps link classes to outcome data if time allows?" — [from_superviser.tex:25](from_superviser.tex)
- Robust, clinically interpretable features (LA+LAA: volume, elongation, sphericity); "I have nothing on curvature or tortousity (I found this in my research to be a fragile measurement for different reasons)" — [from_superviser.tex:27](from_superviser.tex)
- Discriminative-feature thinking: L/R symmetry, size difference, complexity/number of branches — [from_superviser.tex:29](from_superviser.tex)
- Graph with vertex/edge/global features, aggregate with a network, investigate latents; open questions: objective, contrastive vs autoencoder, supervised vs unsupervised — [from_superviser.tex:32-33](from_superviser.tex)

Kit (email 3, attribution inferred):
- Wants "an embedding space which separates different shapes", e.g. a high-tortuosity cluster, bifurcation-type clusters — [from_superviser.tex:42](from_superviser.tex)
- Graph with per-vertex hand-crafted descriptors "(tortuosity, angles, position relative to 4 chambers, neighbourhood)" — [from_superviser.tex:45](from_superviser.tex)
- Warning: embeddings will more likely separate on "heart size, dominance, number of branches" than on the shape descriptors of interest; normalise by volume, size, number of branches; embedding the full tree may be expensive — [from_superviser.tex:46-48](from_superviser.tex)
- "I don't want you to get bogged down in the details of representation learning for now. I think there are lots of other simpler approach to try first." — [from_superviser.tex:50](from_superviser.tex)
- "the main goal is the HØ dataset and matching the shape descriptors with outcome. For now I suggest you use ImageCAS to develop the shape descriptors, and compute some statistics on these." — [from_superviser.tex:52](from_superviser.tex)

Other supervisor-facing decisions:
- "As discussed, I will train CAS-Net from scratch"; segmentation contribution "will most likely focus on post-processing" — [thesis/weekly_report_02.tex:164-169](thesis/weekly_report_02.tex); contradicted by the week 2 gap text "This thesis does not train or fine-tune a segmentation network ... effort goes into recovering topological correctness afterward, as post-processing" — [thesis/week2/segmentation_gap.tex](thesis/week2/segmentation_gap.tex) (section "Segmentation improvements"), and by plan week 5 "Topology-aware fine-tuning" — [thesis/project_plan.tex:59-61](thesis/project_plan.tex)
- Open questions for supervisors with student defaults: CGPS trees get no artery names (default: label-free features on CGPS, named features on ImageCAS-X only); tortuosity metric (default curvature primary, one index alongside); short-interval repeat scans unlikely (default: repeat manual labelling for error); reference "normal" population (default whole cohort, zero-calcium sensitivity); reproduce vs train segmentation; select segmenter on Betti/clDice — [docs_thesis/supervisor_questions.md:6-35](docs_thesis/supervisor_questions.md). No recorded answers were found.

### Inferences
- The two supervisors converge on: graph representation with per-node features, interpretability,
  normalising away size/dominance/branch count, and caution about data size for deep models.
- They diverge on priority and on tortuosity. Bjørn: representation first, descriptors as ablation;
  tortuosity/curvature "fragile". Kit: descriptors on ImageCAS-X first, statistics, outcome on HØ as the
  main goal; representation learning deferred. Kit's instruction lines up with the formal objectives
  (7 to 10); Bjørn's does not contradict them but is not required by them.
- Both supervisors frame the target partly as "phenotypes/clusters", which is not in the formal
  objective list (the list says population statistics and outlier/extreme-value detection).
- Bjørn's transformer warning plus the n=800 ImageCAS-X size is echoed by the student's own note that
  whole-tree deep models on 800 cases "will largely rediscover PCA" — [thesis/week3/tortuosity_and_representation.tex:402-404](thesis/week3/tortuosity_and_representation.tex)

### Gaps
- Emails are undated and email 3 is unsigned; sender and ordering are inferred from content.
- No written supervisor response to the week 2/3 questions (train vs reproduce, tortuosity metric,
  correspondence by named vessel vs structure-consuming model) was found.
- Phillip's role (CGPS access, repeat-scan cohort) is known only from reports, not from his own words.

## 4. Data: final analysis cohort, outcome, current availability, and the role of ImageCAS-X

### Takeaway
ImageCAS-X (800 usable clinically referred CCTA scans, 560/80/160 split, with segment-labelled
centerlines) is the development and validation set: pipeline building, segmentation verification,
feature reliability. The real analysis is on CGPS / Herlev–Østerbro, a general-population cohort with
repeat scans about ten years apart and adjudicated outcomes: normative ranges, outliers, plaque
progression at baseline-plaque-free locations, and MACE prediction. CGPS data is not yet in hand, its
subset structure is unknown, and it will have no delivered centerlines or artery names.

### Cited Findings
- ImageCAS-X "licenses building the pipeline, verifying the segmentation against annotations, and
  measuring the reproducibility of each feature. It cannot license a normative description of healthy
  coronary topology"; clinically referred, CAD in roughly half of the 800 — [thesis/concepts.tex:184-194](thesis/concepts.tex)
- Split: train 560, val 80, test 160, exclude 200 of 1000 — [CLAUDE.md, "State of the data"](CLAUDE.md)
- CGPS: participants not selected for disease, re-scanned over time, adjudicated outcomes; RQ2 needs the
  repeat-scan subset, RQ4 the outcome-linked subset, and "Whether those two subsets overlap, and by how
  much, is unknown" — [thesis/concepts.tex:196-203](thesis/concepts.tex)
- Phillip: some participants scanned twice about ten years apart; some healthy at first scan developed
  CAD by the second, others unchanged — [thesis/weekly_report_02.tex:34-38](thesis/weekly_report_02.tex)
- Outcome cohort cited as Fuchs, CGPS CCTA, n = 9533 with adjudicated MI — [docs_thesis/state_of_the_art_plan.md:42-43](docs_thesis/state_of_the_art_plan.md) (abstract-level literature, not project data)
- Outcomes in the plan: plaque progression "at locations free of plaque at baseline" and MACE — [thesis/project_plan.tex:84-90](thesis/project_plan.tex)
- Kit: "the main goal is the HØ dataset and matching the shape descriptors with outcome" — [from_superviser.tex:52](from_superviser.tex)
- HØ has "no delivered centerlines and no segment names"; plan is to extract centerlines from the 160
  test predictions and measure feature drift vs corrected masks as a baseline error estimate; HØ will be
  out of distribution for CAS-Net — [thesis/weekly_report_03.tex:47-51](thesis/weekly_report_03.tex)
- CGPS labelling protocol will differ and "probably will not annotate all branches"; protocol difference
  is a confounder — [thesis/concepts.tex:246-249](thesis/concepts.tex)
- Disease reshapes lumen geometry (Glagov), hence a reference distribution must come from people free
  of disease; "This is the entire reason the work is split across two cohorts" — [thesis/concepts.tex:211-218](thesis/concepts.tex)
- Name "Herlev–Østerbro" is settled for CGPS — [memory: project_herlev_osterbro_naming.md]
- The student's framing of the HØ question: "is there a latent representation of tortuosity that can predict future plaque occurrence" — [thesis/weekly_report_03.tex:97-100](thesis/weekly_report_03.tex)

### Inferences
- Anything developed on ImageCAS-X must transfer to predicted masks without names or delivered
  centerlines. Methods that depend on the 14 anatomical labels or on the delivered smoothed centerlines
  (including per-named-vessel correspondence for tokenisation) serve ImageCAS-X only unless a labelling
  step is added.
- Any learned representation trained on ImageCAS-X is trained on a referred, roughly half-diseased
  population and then applied to a healthy population through a different segmentation path, which
  compounds domain shift.
- Diseased vs healthy on ImageCAS-X (Disease column) is only a stand-in endpoint and is cross-sectional,
  so it is contaminated by remodelling per concepts.tex B.

### Gaps
- CGPS size of repeat-scan and outcome subsets, scan intervals, outcome coding, covariates, and
  annotation budget: all unknown pending access.

## 5. Representation / learning vs hand-crafted descriptors in the plan

### Takeaway
The formal plan and objectives are entirely descriptor-based (branching, dominance, bifurcation angle,
tortuosity; reliability, reproducibility, normative ranges, outlier flags, risk model with continuous
features plus outlier flags). Representation learning enters only through supervisors' emails and the
student's own week 2/3 notes, where it is framed as a checked complement (PCA baseline, probes against
hand-crafted measures), not as a replacement. Anatomical correspondence appears in the plan, but for
repeat scans of the same participant, not across patients.

### Cited Findings
- Plan feature list: "branching, bifurcation angles, tortuosity and dominance" — [thesis/project_plan.tex:56-58](thesis/project_plan.tex); risk model features: "continuous measurements and the population-outlier flags ... e.g. top-5% tortuosity" — [thesis/project_plan.tex:86-90](thesis/project_plan.tex)
- The only correspondence item in the plan: "Method for anatomical correspondence between repeat scans of the same participant" (weeks 7 to 10, risk 4) — [thesis/project_plan.tex:77-78](thesis/project_plan.tex)
- Week 2 plan: two routes, hand-crafted descriptors (curvature as a profile, bends and angles read against
  vessel thickness) and learned representations (autoencoder), with PCA as baseline ("If an
  autoencoder cannot beat PCA, the network adds nothing") and t-SNE for looking only — [thesis/weekly_report_02.tex:186-222](thesis/weekly_report_02.tex)
- Scope narrowed to LM, LAD, LCX for a start — [thesis/weekly_report_02.tex:149-151](thesis/weekly_report_02.tex); [thesis/week2/major_vessel.tex](thesis/week2/major_vessel.tex)
- Week 3 note: units of analysis (10 to 30 mm windows give tens of thousands of samples; per vessel
  about 800; whole tree 800); suggested path PCA/fPCA per vessel, then self-supervised window encoder with
  measurement-nuisance augmentations, probes against the hand-crafted panel, and "Only then a tree-level
  GNN or recursive VAE" — [thesis/week3/tortuosity_and_representation.tex:402-515](thesis/week3/tortuosity_and_representation.tex)
- Week 3 note pitfall: "The network learns the pipeline, not the anatomy" (predicted-mask centerlines on
  CGPS, tracer shortcuts, image quality) — [thesis/week3/tortuosity_and_representation.tex:497-502](thesis/week3/tortuosity_and_representation.tex)
- Tortuosity choice: average absolute curvature as primary, justified by Kashyap 2022 (tortuosity index
  p = 0.86 vs low WSS) — [thesis/shen2026_gaps.tex:136-149](thesis/shen2026_gaps.tex); curvature and torsion need 2nd/3rd derivatives and "may be far less reliable ... but they may also carry more signal" — [thesis/weekly_report_03.tex:40-41](thesis/weekly_report_03.tex)
- Level of analysis matters for tortuosity (segment vs patient level reverse sign); sex is a systematic
  modifier, so every distribution is stratified by sex — [thesis/shen2026_gaps.tex:107-130](thesis/shen2026_gaps.tex)
- Confounders for descriptors: branch count is a protocol measurement; right side annotated more coarsely;
  image quality confounds branch counts; delivered centerlines are smoothed (sigma 0.5 mm) — [thesis/concepts.tex:238-273](thesis/concepts.tex)
- Student's stated motivation for representation learning: descriptors bound what can be found, and
  the question of how to identify which geometric property drives a latent-outcome association — [thesis/weekly_report_03.tex:79-95](thesis/weekly_report_03.tex)

### Inferences
- Serves the plan: robust, reproducible descriptors (curvature-based tortuosity, bifurcation angle with
  diameters, branch/dominance measures that survive the ground-truth-free path), their measurement
  error, population distributions, and outlier flags. A representation-learning component serves the
  plan best if it is a bounded add-on to objective 10 (does it add predictive value beyond descriptors),
  evaluated against PCA and linear probes, as both Kit's caution and the student's own suggested path imply.
- Drift risk: building a tokenised-tree transformer with cross-patient correspondence on 800 ImageCAS-X
  cases before CGPS access, since (a) no objective requires it, (b) Kit asked to defer it, (c) Bjørn
  himself warns about data size, and (d) the plan's correspondence work is between repeat scans, which
  is a different and required problem.
- Bjørn's "tortuosity is fragile" remark aligns with the student's derivative-noise concern and with the
  reproducibility deliverable (obj. 6); it argues for investing in measurement-floor work on tortuosity,
  not for dropping it, since tortuosity is named in objective 7 and in the risk-model example.

### Gaps
- No document states whether representation learning would count toward the objectives or be judged
  as extra. No supervisor has ruled on the student's per-named-vessel vs structure-consuming
  correspondence question.
