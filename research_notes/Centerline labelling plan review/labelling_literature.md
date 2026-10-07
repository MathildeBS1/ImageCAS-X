# Automatic anatomical labelling of coronary centerline trees: literature vs Stage 3 of the plan

Note: plan mode was active, so these notes are written here instead of
`research_notes/Centerline labelling plan review/labelling_literature.md`. Copy them there unchanged.

## Q1. What the published methods do and report

### Takeaway
The three leads in literature.md split into two kinds. EAGMN and HAGMN-UQ are 2D invasive angiography (ICA) methods with 5 labels and template graph matching, so they are a poor template for a CCTA labeller. The multi-resolution GCN paper (Hampe et al. 2024) is CCTA and is the closest published analogue to Stage 3. On CCTA, segment-graph methods report mean F1 of about 0.86 to 0.96 on clean or manually corrected trees. The one fully automatic pipeline drops to 0.74.

### Cited Findings
**Correction to the plan's reading list**
- EAGMN (Comput. Biol. Med. 2023) uses 2D ICA from LAO/RAO views, not CCTA. The dataset is 263 ICA images (79 templates plus 184 for 5-fold CV). Labels are LMA, LAD, LCX, D and OM only. Nodes are artery segments with 121 hand-crafted texture, position and topology features. It labels by association-graph matching to template ICAs with majority voting. Weighted accuracy is 0.8653 and per-label F1 is LMA 0.99, LAD 0.88, LCX 0.86, D 0.82, OM 0.80. Reported baselines: CPR-GCN 0.458, BiTreeLSTM 0.749, SVM 0.665 — [EAGMN, PMC11073582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11073582/)
- HAGMN-UQ (arXiv:2308.10320) is also ICA. It uses 718 angiograms from two sites, the same 5 labels and the same 121 hand-crafted features. Accuracy is 93.45%, against AGMN 86.39%, EAGMN 87.67% and NGM 90.39%. Testing matches the case to template graphs, and uncertainty cuts the templates compared from about 17.7 to 1.1 — [HAGMN-UQ](https://arxiv.org/html/2308.10320)

**CCTA segment-graph methods**
- Hampe et al., "Graph neural networks for automatic extraction and labeling of the coronary artery tree in CT angiography", J Med Imaging 2024 (this is PMC11095121). Data: 104 CCTA scans from 2 hospitals, 79 train and 25 test, with 10 AHA classes (LM, LAD, LCX, RCA, D, S, OM, AM, R-PDA, R-PLB). Nodes are segments between bifurcations or endpoints. The model is an ensemble of 3-layer GATs with 4 heads plus dense and residual connections. Features are location relative to the LV myocardium centre, orientation, radius mean and std, and appearance (tracker-CNN entropy and seed-CNN outputs). Labelling F1 is 0.74 on automatically extracted trees and 0.91 to 0.95 on manual reference trees. Per class on automatic trees: RCA 0.90, LAD 0.86, AM 0.84, LCX 0.74, OM 0.74, D 0.73, LM 0.70, R-PDA 0.69, R-PLB 0.69, S 0.54 — [Hampe 2024, PMC11095121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
- CPR-GCN (Yang et al., CVPR 2020) uses 511 subjects (6760 segments, 13.2 segments per tree on average) and 11 classes (RCA, R-PDA, R-PLB, AM, LM, LAD, LCX, RI, D, OM, S). Nodes are segments split at every bifurcation, "so main branches (e.g., RCA, LAD) might be represented by multiple nodes". Centerlines come from an automatic segmentation. In 5-fold CV mean F1 is 0.955. On the same data the conventional template method of Cao scores 0.857 and TreeLab-Net 0.871. Per-class F1 for CPR-GCN: RCA 0.990, LM 0.989, LAD 0.988, AM 0.987, LCX 0.976, S 0.964, R-PDA 0.938, R-PLB 0.945, OM 0.914, D 0.909, RI 0.909 — [CPR-GCN](https://arxiv.org/pdf/2003.08560)
- TreeLab-Net (Wu et al., IJCARS 2019) combines an MLP encoder with a bidirectional Tree-LSTM. Features are positions and directions under a spherical coordinate transform, on 436 subjects. Its mean F1 is 0.871 as reproduced by CPR-GCN. It cannot handle a parent with more than 2 children, and a missing branch shifts its layer indices — [CPR-GCN](https://arxiv.org/pdf/2003.08560); [TreeLab-Net, ResearchGate](https://www.researchgate.net/publication/329226443_Automated_anatomical_labeling_of_coronary_arteries_via_bidirectional_tree_LSTMs)
- TopoLab (Zhang et al., MICCAI 2023) has 14 classes. Segment features combine a Transformer over centerline points (intra-segment) with GCN interaction between segments, plus image features trilinearly sampled from a 3D ResUNet encoder. An anatomy-aware connection classifier labels pairs of connected segments. Centerlines come from 3D thinning of the segmentation annotations. Results: orCaScore (72 scans, public annotations released by the authors) F1 87.23% vs CPR-GCN 82.72% and TreeLab-Net 83.12%; in-house (800/200/200) F1 92.19% vs CPR-GCN 90.84%. Ablations: without the Transformer, F1 falls by 7.94 points; without the GCN, by 1.57 points — [TopoLab, arXiv:2307.11959](https://arxiv.org/html/2307.11959v1)
- LWT-ARTERY-LABEL (Zhang, Gharleghi, Beier et al., EMBC 2025) uses a plain MLP on 14 inputs: length, mean curvature, and start/mid/end Cartesian coordinates from VMTK centerlines. The MLP has 18,438 parameters and is trained with focal loss, followed by seven sequential rule-based topology steps. It covers 13 classes, including D1 to D3 and OM1 to OM3. Data are the Coronary Atlas (380), GeoCAD (70) and orCaScore (72, external). On orCaScore it reports F1 93.26% vs TopoLab 87.23%, and claims to beat TreeLab-Net, CPR-GCN, CorLab-Net and TaG-Net. Coordinates are normalised to the scan's RAS frame and origin, not to a cardiac centre, and the authors list this as a limitation — [LWT-ARTERY-LABEL, arXiv:2508.06874](https://arxiv.org/html/2508.06874v1)
- Li et al. (ISBI 2023) use 141 patients, 13 classes (including L-PDA and L-PLB) and 22.9 segments per patient. Under 5-fold CV the weighted F1 is GCN 0.622, GAT 0.642, GIN 0.657 and GraphSAGE 0.805 — [Li et al., ar5iv 2212.00386](https://ar5iv.labs.arxiv.org/html/2212.00386)
- TTN (Zhang et al., IEEE JTEHM 2024) is a Transformer that treats branch labelling as sequence labelling. It uses a topological position encoding and a "segment-depth loss" against main-vs-side-branch imbalance, on 325 CCTA scans (numbers only in the abstract seen) — [TTN, Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=PMCID:PMC10706468&resultType=core&format=json)
- Point Transformer (Wang, Ma, Li, ISBI 2023) converts the segmentation to a point cloud, classifies the points and maps them to centerline labels. It uses 53 CCTA subjects; the abstract gives no numbers — [arXiv:2305.02533](https://arxiv.org/abs/2305.02533)

**Classical and atlas methods**
- Cao et al. (Int J Cardiovasc Imaging 2017, not IJCARS) start with point-set registration of a 3D model. There are separate right-dominant and left-dominant models, and dominance must be known beforehand. RCA, LAD and LCX are found as the centerlines nearest the aligned model's main branches; the LAD/LCX overlap is LM. A cost-minimising iterative matching then labels the side branches. Logic rules: RI if the branch leaves within 0.5 cm of the LAD-LCX bifurcation, OM if it leaves more than 2 cm along LCX, and branches under 1 cm or above 120 degrees are removed. On 83 scans (1149 segments) segment accuracy is 89.2% for RD and 83.6% for LD, against expert agreement of 97.6% (RD) and 87.6% (LD). Most disagreements are on D and OM: 55.2% in RD and 78.6% in LD — [Cao 2017, PMC5677991](https://pmc.ncbi.nlm.nih.gov/articles/PMC5677991/); [Cao PhD thesis, Leiden 2020](https://scholarlypublications.universiteitleiden.nl/access/item%3A2914681/view)
- Gülsün et al. (MICCAI 2014, Siemens) match the case to a standard model tree via geodesics. Chamber positions set the coordinate frame. Labelling takes about 3 min. They report 87.0% (left tree) and 86.0% (right tree) overlap on automatically detected centerlines, and did not handle LD cases or cases with RI. These figures are as reported by Cao, since the primary text was not accessible — [Cao thesis, Ch. 2 discussion](https://scholarlypublications.universiteitleiden.nl/access/item%3A2914681/view)
- Akinyemi et al. (EUSIPCO 2009) train a multivariate Gaussian classifier on geometric features of pre-segmented centerlines and report 84% accuracy. The accuracy figure comes from a search snippet; the full text was not read — [EUSIPCO 2009](https://new.eurasip.org/Proceedings/Eusipco/Eusipco2009/contents/papers/1569187117.pdf)
- Ren et al. (BMC Med Inform Decis Mak 2023) use a 3D U-Net, skeletonisation and rules, identifying LCX by its distances to the LA and LV. On 157 patients, all right-dominant, segment presence accuracy is 96.2% and overlap 94.0% — [Ren 2023, PMC10626726](https://pmc.ncbi.nlm.nih.gov/articles/PMC10626726/)

### Inferences
- The plan says to read EAGMN in full "before fixing the feature list and architecture". That is the wrong anchor: it is 2D, 5-label and template-matching. Hampe 2024 (CCTA, GAT, 10 classes, ablations, automatic vs manual trees) and TopoLab (14 classes, constraint-aware classifier) should replace it as the primary reads. CPR-GCN is a good third.
- The 14-label scheme matches TopoLab's class count, so TopoLab's 87 to 92% F1 is the closest scale reference. Hampe's 0.74 on automatic trees is the realistic reference for the "predicted test trees" arm.

### Gaps
- Primary full texts for TreeLab-Net, Gülsün 2014, Akinyemi 2009, TTN, CorLab-Net and TaG-Net were not read, so their numbers are secondary or abstract-level.
- No published method was found that trains on ImageCAS or ImageCAS-X labels, and no 2026 CCTA labelling paper turned up.

## Q2. Do image features help, and by how much?

### Takeaway
Yes, but the gain is modest: about 2 to 3 F1 points. Location is by far the most important feature group.

### Cited Findings
- CPR-GCN: dropping the image conditions (3D CNN plus BiLSTM over cubes along the segment) lowers mean F1 from 0.955 to 0.934. The biggest losses are OM (0.914 to 0.822) and D (0.909 to 0.859). LM, LAD and RCA barely change — [CPR-GCN Table 5](https://arxiv.org/pdf/2003.08560)
- Hampe 2024 ablation on automatic trees: full model F1 0.74. Without location 0.59, without orientation 0.71, without geometry 0.72, without appearance 0.71 — [Hampe 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
- TopoLab samples image features from a ResUNet encoder, but the excerpt seen reports no image-off ablation — [TopoLab](https://arxiv.org/html/2307.11959v1)
- LWT-ARTERY-LABEL uses no image features and still reports the best orCaScore F1 (93.26%) — [LWT](https://arxiv.org/html/2508.06874v1)

### Inferences
- A geometry-only first version is defensible. Image features are a later improvement aimed at D/OM, not a prerequisite.
- What matters most is the location frame, which is covered in Q5.

### Gaps
- No study isolates image features specifically for the D-vs-LAD continuation decision.

## Q3. Main-vessel continuation, spurious/missing branches, dominance

### Takeaway
The published GNNs mostly handle continuation implicitly: per-segment classes plus message passing. Robustness to missing or spurious branches is tested by synthetic deletion. Dominance is the weakest point everywhere: rule and atlas methods need it decided first, and inter-expert agreement on L-PDA is itself poor.

### Cited Findings
- **Continuation.** In CPR-GCN and Hampe every junction-to-junction segment is a node, so LAD spans several nodes that all carry "LAD" — [CPR-GCN Fig. 4](https://arxiv.org/pdf/2003.08560); [Hampe 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/). Cao identifies the main branches first, by registering to a model, and labels side branches only after that — [Cao 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5677991/). EAGMN makes continuation explicit with incremental labels along flow (LCX1, LCX2) — [EAGMN](https://pmc.ncbi.nlm.nih.gov/articles/PMC11073582/)
- **Missing and spurious branches.** CPR-GCN deleted 20% of LM/RCA branches, which touched 1123 of 6760 segments. Mean F1 fell 0.955 to 0.929 for CPR-GCN and 0.871 to 0.802 for TreeLab-Net — [CPR-GCN Table 4](https://arxiv.org/pdf/2003.08560). EAGMN stays above 0.81 accuracy with 20% of branches removed — [EAGMN](https://pmc.ncbi.nlm.nih.gov/articles/PMC11073582/). Hampe found that label ambiguity from leakage, where a coarse segment mixes artery and vein, is reduced by multi-resolution graphs; the ensemble also mitigates missed bifurcations — [Hampe 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
- **Weakest classes.** On automatic trees Hampe's weakest classes are R-PDA and R-PLB (0.69). The authors suggest "relative features or rule-based post-processing" for these but did not implement it — [Hampe 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
- **Dominance.** Cao needs separate RD and LD models and the dominance type in advance; RD is about 86% of patients. Inter-observer overlap variability on L-PDA in LD cases is 10%, and expert agreement on LD trees is only 87.6% — [Cao 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5677991/); [Cao thesis](https://scholarlypublications.universiteitleiden.nl/access/item%3A2914681/view). Ren et al. sidestep dominance by including only right-dominant patients — [Ren 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10626726/). Gülsün excluded LD cases — [Cao thesis](https://scholarlypublications.universiteitleiden.nl/access/item%3A2914681/view)
- **Class imbalance** is named as the main remaining problem by CPR-GCN — [CPR-GCN Discussion](https://arxiv.org/pdf/2003.08560). TTN adds a segment-depth loss for it — [TTN](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=PMCID:PMC10706468&resultType=core&format=json) — and LWT uses focal loss — [LWT](https://arxiv.org/html/2508.06874v1)

### Inferences
- With about 10 to 14% left-dominant cases in 560 trees, L-PDA and L-PLA will have very few training segments. Expect their F1 to be unstable, and report it with counts. Two further options: a separate tree-level dominance prediction, scored on its own, and/or a class-weighted or focal loss. The plan currently has neither.
- The plan's augmentation removes only short terminal segments. CPR-GCN's evidence argues for also deleting whole internal subtrees, and for adding synthetic spurs, since predicted trees will have extra branches too.

### Gaps
- The ImageCAS-X dominance prevalence in the train split was not checked here. It is a repo query, not a literature one.

## Q4. Is junction-to-junction segment the right node unit?

### Takeaway
It is the standard unit (CPR-GCN, Hampe, TopoLab, Li). But Hampe shows that splitting long segments into sub-segments at several resolutions, then averaging the probabilities back onto the points, helps on automatic trees. That is exactly the case where a missed side branch makes one segment span two GT labels.

### Cited Findings
- Hampe's "multi-resolution graph ensembling" combines an undivided graph with graphs whose segments are capped at 5, 10, 20 and 30 centerline points. Predictions are projected back to the fine graph by averaging probabilities. It was motivated by label ambiguity when one coarse segment mixes classes — [Hampe 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
- Hampe scores at node level on automatic trees: a node is a TP if its nearest reference node lies within the local artery radius — [Hampe 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/). Cao and Ren use a per-label overlap measure along the centerline — [Cao 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5677991/); [Ren 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10626726/)
- Point-level alternatives exist: the Point Transformer classifies points and maps them to centerlines — [arXiv:2305.02533](https://arxiv.org/abs/2305.02533). TopoLab aggregates points inside each segment with a Transformer, and removing that step cost 7.94 F1 points — [TopoLab](https://arxiv.org/html/2307.11959v1)

### Inferences
- The plan has two related weaknesses. First, the training target is the segment-majority label. Second, the predicted-tree evaluation takes a segment-majority after a 3 mm nearest-point transfer. Together they hide the "segment spans two labels" error that predicted trees will produce.
- A low-cost fix inside the plan's design has two parts:
  - Also build a graph that splits segments longer than a fixed length, for example 10 to 20 mm, and average the probabilities back onto the points (Hampe).
  - Report length-weighted point accuracy as primary. The plan already lists it.
- Use the local radius rather than a fixed 3 mm as the match tolerance, to match Hampe's definition.

### Gaps
- No paper directly compares segment-level and point-level training on the same data.

## Q5. Ostium-relative coordinates plus rotation augmentation vs a heart-centred frame

### Takeaway
Location is the dominant feature, and the strongest CCTA systems anchor it to the heart, not to the vessel. Hampe uses the LV myocardium centre, Gülsün uses chamber positions, and Ren uses LA/LV distances. An ostium-only frame keeps translation information but leaves cardiac orientation to the scanner frame plus ±15° jitter.

### Cited Findings
- Hampe's location is Cartesian coordinates relative to the LV myocardium centre, z-scored on the training set, with no rotation augmentation described. Removing location drops F1 from 0.74 to 0.59, the largest ablation effect — [Hampe 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
- Gülsün used the positions of the four chambers to set the coordinate frame — [Cao thesis](https://scholarlypublications.universiteitleiden.nl/access/item%3A2914681/view)
- Ren identifies LCX from the distances of candidate centerline points to the LA and LV — [Ren 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10626726/)
- CPR-GCN and TreeLab-Net use per-branch spherical coordinates (S² manifold) to normalise orientation variance — [CPR-GCN §3.1](https://arxiv.org/pdf/2003.08560). Li et al. take their origin at the first point of the left tree's first centerline — [Li ISBI 2023](https://ar5iv.labs.arxiv.org/html/2212.00386)
- LWT uses the scanner RAS frame and origin, and lists this as a limitation when scans include non-cardiac regions — [LWT](https://arxiv.org/html/2508.06874v1)
- Cao normalises scale and uses rigid point-set registration to a model — [Cao 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5677991/)

### Inferences
- The plan already runs TotalSegmentator. Adding chamber or LV masks gives three useful extras:
  - an LV-centred origin;
  - an LV long-axis frame;
  - per-segment distances to the LV, LA, RV and septum.
  These would help exactly the hard decisions: LAD vs D (interventricular groove), LCX/OM (AV groove vs LV free wall) and PDA (posterior groove, crux). The cost is one more `--roi_subset` or `heartchambers_highres` run, and that is the task the plan currently lists as a deviation it avoided.
- Keep ostium-relative features as well. They are cheap, and the side split depends on them.
- ±15° rotation is reasonable as a robustness jitter but does not replace a canonical frame.

### Gaps
- No study ablates an ostium frame against a heart frame on the same data.

## Q6. Small data (560 trees): will a GNN beat simple baselines? Keep a baseline?

### Takeaway
The evidence is mixed and argues for keeping a non-graph reference. On orCaScore a 18k-parameter MLP plus rules beats every GNN reported. Hampe's node-only ("self-connections") model is 2 F1 points behind the full GNN. A tuned template method is within 1.4 points of TreeLab-Net. 560 trees is larger than every CCTA set above except CPR-GCN (511) and TopoLab in-house (1200).

### Cited Findings
- Hampe ablation: self-connections only (no neighbourhood) gives F1 0.72, against 0.74 for the full model — [Hampe 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
- LWT MLP plus rules gives orCaScore F1 93.26%, against TopoLab 87.23% (and CPR-GCN 82.72%, TreeLab-Net 83.12% as reported by TopoLab) — [LWT](https://arxiv.org/html/2508.06874v1); [TopoLab](https://arxiv.org/html/2307.11959v1)
- On CPR-GCN's 511 subjects, Cao's conventional method scores mean F1 0.857 and TreeLab-Net 0.871; CPR-GCN reaches 0.955 — [CPR-GCN Table 3](https://arxiv.org/pdf/2003.08560)
- Architecture sensitivity: on 141 patients GAT gives F1 0.642 and GraphSAGE 0.805 — [Li ISBI 2023](https://ar5iv.labs.arxiv.org/html/2212.00386). CPR-GCN got no gain from 3 to 4 GCN layers, which it links to tree depth mostly under 4. It also found residual connections necessary: without them F1 is 0.947 vs 0.955 — [CPR-GCN](https://arxiv.org/pdf/2003.08560)
- Human reference: Cao's expert agreement is 97.6% (RD) and 87.6% (LD) — [Cao 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5677991/)

### Inferences
- Faults in "4 GAT-style layers, GNN only":
  - GAT's attention-weighted neighbour mean can wash out the node's own features. Li's 0.64 vs 0.81 suggests a GraphSAGE-style update (separate self and neighbour weights, concatenated) or an explicit residual is safer.
  - 4 layers is at or past the depth where CPR-GCN saw no gain.
- A zero-layer ablation (the same head on node features only, i.e. an MLP) costs no new code path, and it answers whether message passing helps. I suggest reporting it even though the user ruled out a GBM. Without it, the plan cannot claim the graph matters.

### Gaps
- No published learning curve shows how labelling F1 scales with the number of training trees on CCTA.

## Q7. Constrained decoding

### Takeaway
Unconstrained segment classifiers often produce anatomically invalid trees: CPR-GCN violates topology in 39 to 54% of cases. TopoLab's connection classifier more than halves that. The plan's greedy top-down decode is a weaker form of the same idea; exact max-product (Viterbi) over the tree is the natural upgrade.

### Cited Findings
- TopoLab measures a "violation rate" (cases with anatomically invalid label connections): orCaScore 22.29% vs 53.91% for CPR-GCN, and in-house 9.40% vs 38.70%. It labels each segment by taking the most confident connection-pair prediction covering it, with pair classes restricted to the valid parent-child templates (for example LM→LAD) — [TopoLab](https://arxiv.org/html/2307.11959v1)
- LWT applies seven sequential rule-based steps after the MLP. These include left/right separation and RI validated by a 3 mm distance from the LM end — [LWT](https://arxiv.org/html/2508.06874v1)
- Cao uses cost-minimising iterative matching to the model and then logic rules: RI under 0.5 cm, OM over 2 cm along LCX, D/OM ordering and proximal/mid/distal splits — [Cao 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5677991/)
- HAGMN-UQ and EAGMN use graph matching to templates plus anatomical structural loss and confidence — [HAGMN-UQ](https://arxiv.org/html/2308.10320); [EAGMN](https://pmc.ncbi.nlm.nih.gov/articles/PMC11073582/)
- CPR-GCN claims that having no hard-coded rules makes it more robust when main branches are missing: one wrong LM does not propagate — [CPR-GCN Discussion](https://arxiv.org/pdf/2003.08560)

### Inferences
- Greedy top-down decoding commits early. A wrong LM or LAD at depth 1 forces every descendant into an allowed-but-wrong label, the propagation risk CPR-GCN warns about. Max-product dynamic programming over the rooted tree, with unary GNN log-probabilities plus a transition table, is exact and no more code. Two further options:
  - soft transition penalties learned from train-split counts, so that rare valid variants (for example L-PDA under LCX) are not banned;
  - an "at most one child continues the parent vessel" constraint, which needs a state per (node, does-a-child-continue) pair and is still small.
- Report a violation rate, as TopoLab does, for both the raw and decoded outputs.
- Ordinal labels (D1/D2, OM1/OM2) depend on take-off order along the parent. The plan's fractional take-off position feature helps. A post-decode re-ordering rule (rename D labels by take-off order along LAD) is what Cao and LWT effectively do.

### Gaps
- No CCTA paper was found that uses tree-CRF or Viterbi decoding explicitly with reported numbers, so this recommendation rests on reasoning, not on an ablation.
