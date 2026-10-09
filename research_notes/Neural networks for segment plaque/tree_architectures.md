# Neural network architectures for per-segment prediction on coronary (and analogous) trees

Scope note: the target task is node-level (per SCCT/AHA segment) prediction of future plaque in the Herlev–Østerbro CGPS cohort (~2000 participants, ~30,000-36,000 segments). Almost all published coronary tree GNNs solve anatomical labelling or FFR estimation, not plaque prediction; no published GNN for per-segment plaque progression was found (see Gaps). Results below are therefore architecture evidence by analogy. All numbers are reported with cohort size; arXiv-only items are flagged.

## 1. How have GNNs / tree models been applied to coronary trees for node/segment-level tasks?

### Takeaway
Graph and tree networks on coronary centerline trees are established for anatomical segment labelling (cohorts 71 to 511 patients, F1 roughly 0.80 to 0.96) and for FFR surrogates (trained mainly on thousands of synthetic trees, validated on ~180 real trees). They are small models (3 layers, tens to a few hundred hidden units) and operate on patient-specific trees with segments or branches as nodes. Direct application to plaque or MACE prediction at segment level is essentially absent from the literature.

### Cited Findings
Anatomical labelling (segment classification):
- TreeLab-Net (Wu et al., Int J CARS 2019): MLP encoder + bidirectional tree-structured LSTM (Bi-TreeLSTM) over the centerline tree; features are vessel spatial position and direction, normalised with a spherical coordinate transform; 436 CCTA images, 10-fold cross-validation; AUC >97% for LM, LAD, LCX, RCA and >90% for D, OM, R-PLB; beat AdaBoost, MLP and unidirectional (up-to-down, down-to-up) TreeLSTMs with fewer topological errors — [Search summary of Wu et al. 2019, doi 10.1007/s11548-018-1884-6](https://unpaywall.org/10.1007%2FS11548-018-1884-6); [CPR-GCN paper](https://arxiv.org/pdf/2003.08560)
- CPR-GCN (Yang et al., CVPR 2020, peer-reviewed): partial-residual GCN on branch-level graph (branches as nodes, parent-child edges; a bifurcation adds a new node so one anatomical branch may be several nodes), position features via spherical transform, conditioned on image features from a 3D CNN + BiLSTM run along each branch; 511 subjects, 5-fold CV; mean recall 95.8%, precision 95.4%, F1 0.955 — [CVPR open access](https://openaccess.thecvf.com/content_CVPR_2020/papers/Yang_CPR-GCN_Conditional_Partial-Residual_Graph_Convolutional_Network_in_Automated_Anatomical_Labeling_CVPR_2020_paper.pdf); [ar5iv](https://ar5iv.labs.arxiv.org/html/2003.08560)
  - Architecture: 3 GCN blocks (deeper gave no gain), 256 hidden channels; image condition branch = 3D CNN (64 channels) + 4-layer BiLSTM (hidden 128) — [ar5iv](https://ar5iv.labs.arxiv.org/html/2003.08560)
  - On the same 511-subject data TreeLab-Net reached F1 0.871 vs CPR-GCN 0.955; removing image conditions dropped CPR-GCN to F1 0.934; removing residual connections to 0.947 — [ar5iv](https://ar5iv.labs.arxiv.org/html/2003.08560)
- Hampe et al. (J Med Imaging 11(3):034001, 2024, peer-reviewed): graph attention networks for extraction + labelling; 104 CCTA scans (79 train from two hospitals, 25 test), mean 33 segments per tree (range 20-61); GAT with 3 layers, 4 heads x 8 features, dense + residual connections, dropout 0.2; multi-resolution ensemble where centerline is cut into sub-segments of 5, 10, 20, 30 points plus the undivided graph; 10 AHA-derived classes; labelling F1 0.95 on reference trees, 0.74 on automatically extracted trees — [PMC11095121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
  - Node features: location relative to the left ventricle, orientation vectors, radius statistics, appearance (tracker entropy, CNN outputs) — [PMC11095121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
  - An earlier GAT conference version reported F1 92.4% on 71 CCTA images — [search summary, EAGMN/related listing](https://arxiv.org/pdf/2305.12327); [Li et al. related-work table](https://ar5iv.labs.arxiv.org/html/2212.00386)
- Li et al. (arXiv 2212.00386, arXiv-only): 141 patients, 13 classes; compared GCN, GAT, GIN and GraphSAGE on a line-graph of segments, GraphSAGE best; 2 graph layers + FC head, Adam lr 1e-3, 500 epochs; weighted F1 0.805 (13-class) / 0.812 (11-class); rare classes (R, L-PDA, R-PDA) worst — [ar5iv](https://ar5iv.labs.arxiv.org/html/2212.00386)
- Point Transformer for coronary labelling (arXiv 2305.02533, ISBI 2023 per SPS listing): treats the segmentation as a point cloud, needs only the segmentation; 53 subjects — [arXiv](https://arxiv.org/abs/2305.02533); [ISBI listing](https://rc.signalprocessingsociety.org/conferences/isbi-2023/spsisbi23vid0245)
- CorLab-Net: point-cloud network that encodes vessel-to-heart-chamber distance fields, distance to key joint points, and local neighbour dependencies via graph convolution modules (MICCAI 2021, Springer LNCS) — [Point Transformer paper summary](https://arxiv.org/pdf/2305.02533); [Springer](https://link.springer.com/10.1007/978-3-030-87589-3_59)
- EAGMN / AGMN (invasive angiography, arXiv): label assignment by graph matching between a patient graph and template graphs, using graph attention on vertex and edge features — [EAGMN arXiv](https://arxiv.org/pdf/2305.12327); [AGMN arXiv](https://arxiv.org/pdf/2301.04733)

FFR / haemodynamics surrogates:
- TreeVes-Net: coronary representation encoder + tree-structured RNN propagating flow information along the tree; trained on 13,000 synthetic trees, tested on 180 real clinical trees; AUC 0.92 and 0.93 under two FFR criteria, better than seven ML-based FFR methods — [search summary, x-mol listing](https://www.x-mol.com/paper/5980171)
- Conditional physics-informed GNN (Xie et al., MICCAI 2023): GNN with multi-scale graph fusion and physics-residual loss plus boundary conditions as input; trained on 6,000+ synthetic geometries; validated on 183 real coronaries (143 X-ray, 40 CTA), r = 0.89 (X-ray) and 0.88 (CTA); 0.03 s per case — [MICCAI 2023 paper page](https://conferences.miccai.org/2023/papers/135-Paper0259.html)
- Mesh neural networks for SE(3)-equivariant WSS estimation directly on triangulated artery wall (Suk et al., IPMI 2023 / Comput Biol Med 2024): WSS approximation error 7.6%, NMAE 0.4%, about 100x faster than CFD — [arXiv](https://arxiv.org/abs/2212.05023v1); [UTwente record](https://research.utwente.nl/en/publications/mesh-neural-networks-for-se3-equivariant-hemodynamics-estimation-/)

Stenosis / plaque / risk:
- Coronary p-Graph (Comput Med Imaging Graph 2025): proposal-based GCN detecting and localising stenosis on CCTA trained against invasive DSA labels — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0895611125000461) (cohort size not retrieved; abstract paywalled)
- GCN predicting CT-defined CAD (CAD-RADS) from retinal fundus vascular biomarkers: an example where the graph is the retinal vessel tree and the output is patient-level coronary disease — [PMC9221688](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9221688/)

Airway analogue:
- SG-GNN / structure- and position-aware GNN for airway labelling (Xie et al., Nijmegen; arXiv 2201.04532, later peer-reviewed per GitHub/Grand Challenge release): branches as nodes, CNN branch features enriched by a GNN that aggregates neighbours (structure-aware) plus graph-position encoding (position-aware); 220 COPD airway trees; 91.18% accuracy on 18 segmental branches vs 83.83% for the CNN without graph — [arXiv](https://arxiv.org/pdf/2201.04532); [code](https://github.com/diagnijmegen/spgnn)
- Implicit point-graph networks for pulmonary tree labelling (airway, artery, vein) — [ar5iv 2309.17329](https://ar5iv.labs.arxiv.org/html/2309.17329) (arXiv; numbers not retrieved)

### Inferences
- The proven recipe for node tasks on coronary trees is: patient-specific tree graph, 2-3 message-passing layers (GCN, GAT or GraphSAGE), position + direction + radius features, optional per-segment image embedding. Tree-LSTMs were the first generation and were beaten by GCNs on the same data (0.871 vs 0.955 F1, 511 subjects).
- FFR surrogates rely on large synthetic training sets (6,000-13,000 trees) because the label is physical; plaque has no simulator, so a CGPS model must learn from ~2000 real trees only.

### Gaps
- No peer-reviewed GNN predicting future plaque or MACE per coronary segment was found. Searches for "graph neural network plaque progression CCTA segment" returned labelling, segmentation and WSS work only.
- Exact parameter counts are not reported in the papers retrieved; see Q5 for estimates.
- TreeVes-Net venue and Coronary p-Graph cohort size were not verified from full text.

## 2. Representation choices

### Takeaway
Published coronary GNNs overwhelmingly use a patient-specific graph with segments/branches as nodes (or segments as edges in a centerline-bifurcation graph, converted to a line graph). Variable topology is handled natively by message passing; robustness to missing branches has been measured explicitly in CPR-GCN. Fixed-template graphs appear mainly in graph-matching labelling approaches.

### Cited Findings
- Branch-as-node, parent-child edges; a single anatomical branch can be split into multiple nodes at each bifurcation (CPR-GCN, 511 subjects) — [ar5iv](https://ar5iv.labs.arxiv.org/html/2003.08560)
- Segment-as-edge in a bifurcation graph, converted into a line graph so segments become nodes (Li et al., 141 patients, arXiv) — [ar5iv](https://ar5iv.labs.arxiv.org/html/2212.00386)
- Hampe et al. (104 scans) builds the graph from centerline connectivity with segments defined between bifurcations, and re-discretises segments into fixed-length chunks (5-30 centerline points) at several resolutions; ensembling resolutions beat any single resolution; the method also labels disconnected sub-trees, i.e. does not require a fully connected tree — [PMC11095121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
- Point-as-node: point cloud of the segmentation (Point Transformer, 53 subjects, arXiv) and CorLab-Net — [arXiv](https://arxiv.org/abs/2305.02533); [Point Transformer pdf](https://arxiv.org/pdf/2305.02533)
- Surface-mesh vertex as node, for WSS (Suk et al.) and for lumen-mesh segmentation with GCNs (Wolterink et al., arXiv 1908.05343) — [arXiv 2212.05023](https://arxiv.org/abs/2212.05023v1); [arXiv 1908.05343](https://arxiv.org/pdf/1908.05343)
- Edge features: EAGMN embeds both vertex and edge features through graph attention — [arXiv 2305.12327](https://arxiv.org/pdf/2305.12327)
- Normalising pose/variability: spherical coordinate transform of positions (TreeLab-Net, CPR-GCN, Li et al.); location relative to the left ventricle (Hampe). Removing location features was the largest ablation drop in Hampe (labelling F1 to 0.59) — [PMC11095121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/); [ar5iv 2212.00386](https://ar5iv.labs.arxiv.org/html/2212.00386)
- Missing branches: synthetically removing main branches cost CPR-GCN about 2.6% vs 6.7% for TreeLab-Net, i.e. GCN message passing was more robust than tree-recursive LSTMs to incomplete trees (511 subjects) — [ar5iv](https://ar5iv.labs.arxiv.org/html/2003.08560)
- Class imbalance from anatomical variability: dominance-dependent classes (R-PDA, L-PDA, R) were the worst classes in Li et al. (141 patients) — [ar5iv](https://ar5iv.labs.arxiv.org/html/2212.00386)

### Inferences
- For CGPS, where plaque is graded per SCCT segment, segment-as-node is the natural choice: the label unit equals the node. A patient-specific graph built from the 18-segment template restricted to segments present (dominance-dependent PDA/PLB, absent ramus, D2/OM2) avoids imputing absent segments; an alternative is a fixed 18-node template with a "present" mask and masked loss, which permits a plain MLP or transformer over a fixed-length vector.
- Centerline-point nodes would be needed only if plaque labels were sub-segmental; with segment labels they add depth/cost without matching supervision. Point features could still be pooled into segment embeddings (e.g. a 1D CNN along the centerline per segment).
- Geometric features in this thesis (bifurcation angle, daughter ratio) are naturally edge or bifurcation attributes; they can be stored as edge features or copied to the child segment node.

### Gaps
- No paper was found that compares fixed-template vs patient-specific graphs head-to-head on the same coronary task.
- No published guidance on how SCCT segments that are present but non-evaluable should enter a GNN.

## 3. Alternatives to GNNs

### Takeaway
Sequence models along the centerline on curved/multi-planar reformations are the main established alternative for per-location plaque/stenosis tasks; point-cloud and mesh networks exist for labelling and haemodynamics; per-segment tabular models (logistic regression, boosting) are what serial-CCTA progression studies actually use.

### Cited Findings
- Recurrent CNN on MPR images (Zreik et al., IEEE TMI 2019): 3D CNN extracts features along the centerline, an RNN aggregates them, two multiclass heads detect plaque type and stenosis grade; 163 patients; accuracy 0.77 (plaque) and 0.80 (stenosis) — [arXiv 1804.04360](https://arxiv.org/pdf/1804.04360); [UMC Utrecht record](https://researchinformation.umcutrecht.nl/en/publications/a-recurrent-cnn-for-automatic-detection-and-classification-of-cor/)
- CPR-GCN uses exactly this kind of CNN + BiLSTM along each branch as a per-node image encoder feeding a GCN — combining the sequence and graph paradigms — [ar5iv](https://ar5iv.labs.arxiv.org/html/2003.08560)
- Mesh-prior plaque quantification and CAD-RADS prediction (arXiv 2310.11297) — [arXiv](https://arxiv.org/pdf/2310.11297) (details not retrieved)
- Point-cloud networks (Point Transformer, CorLab-Net) and SE(3)-equivariant mesh networks on lumen surfaces, see Q1/Q2 — [arXiv 2305.02533](https://arxiv.org/abs/2305.02533); [arXiv 2212.05023](https://arxiv.org/abs/2212.05023v1)
- Per-segment tabular radiomics: in PARADIGM, radiomic features significantly improved prediction of which normal coronary segment would develop new plaque — [ScienceDirect, J Cardiovasc Comput Tomogr 2024](https://www.sciencedirect.com/science/article/abs/pii/S1934592524000327) (abstract only, cohort numbers not retrieved)
- PARADIGM ML for rapid plaque progression in 1083 patients with serial CCTA, using nested models (clinical, + qualitative plaque, + quantitative plaque) — [PMC7335586](https://pmc.ncbi.nlm.nih.gov/articles/PMC7335586)

### Inferences
- Realistic candidate set for CGPS, ordered by complexity: (a) per-segment logistic regression / gradient boosting with segment features + SCORE2 inputs + baseline plaque; (b) per-segment MLP with neighbour features concatenated (parent, children, sibling baseline plaque and geometry), which is a hand-crafted one-hop message pass; (c) 2-3 layer GNN on the patient tree with SCORE2 inputs broadcast to every node or injected as a graph-level embedding; (d) adding a per-segment image or CPR encoder, as in CPR-GCN. Comparing (a)/(b) against (c) directly answers whether message passing helps.
- Mesh/point-cloud networks are designed for vertex-level outputs (WSS, labels); they are over-parameterised relative to ~18 labels per patient unless used as frozen feature extractors.

### Gaps
- No study found that compares sequence (CPR) models and GNNs for plaque on the same cohort.

## 4. Does message passing between neighbouring segments add value? Evidence on spatial dependence of plaque

### Takeaway
For labelling, ablations consistently show neighbourhood aggregation helps (airway accuracy 83.8% to 91.2%; coronary GAT F1 0.72 without neighbour flow vs higher with it). For plaque, epidemiological evidence shows plaque clusters and that baseline plaque raises new-plaque odds, but no study tests whether adjacent-segment plaque adds predictive value beyond patient-level plaque in a neural model.

### Cited Findings
- Hampe et al. (104 scans): removing information flow between neighbouring nodes reduced labelling F1 to 0.72 (vs full model) — [PMC11095121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
- Airway (220 COPD trees): CNN-only branch classifier 83.83% vs GNN-enriched 91.18% on 18 segmental branches — [arXiv 2201.04532](https://arxiv.org/pdf/2201.04532)
- CPR-GCN (GCN, 511 subjects) F1 0.955 vs TreeLab-Net (tree-LSTM) 0.871 vs MLP baseline lower in TreeLab-Net's own comparison (436 images) — [ar5iv](https://ar5iv.labs.arxiv.org/html/2003.08560); [CPR-GCN pdf](https://arxiv.org/pdf/2003.08560)
- PARADIGM (1,343 patients, serial CCTA, median 3.3 y): new lesions in 35% of patients without and 46.7% with baseline plaque; baseline plaque independently predicted new lesion formation (OR 1.84), as did diabetes (OR 1.38) and BMI (OR 1.04 per kg/m²); new lesions concentrated in the LAD (60%) when no baseline plaque and RCA (47%) with baseline plaque; the abstract does not report adjacency of new to existing plaque — [EHJ-CVI 2025 abstract](https://academic.oup.com/ehjcimaging/article/27/Supplement_1/jeaf367.317/8446296) (conference abstract)
- Pathology: 92% of thin-cap fibroatheromas and ruptured plaques were clustered within two adjacent 20-mm arterial segments; early lesions develop in zones adjacent to existing plaques — [Am J Med 2009 supplement (pathology review)](https://www.amjmed.com/article/S0002-9343(08)01017-6/fulltext)
- In-vivo plaque mapping (JACC Cardiovasc Imaging 2020): TCFAs clustered in proximal segments, particularly proximal LAD, whereas fibrous plaques were spread evenly along arteries — [JACC Imaging](https://www.jacc.org/doi/10.1016/j.jcmg.2020.01.013) (full text not accessible; finding from search abstract)
- Plaque distribution relative to side branches (IVUS): extent and distribution of plaque relate to major side-branch origins — [PubMed 9788034](https://pubmed.ncbi.nlm.nih.gov/9788034/) (abstract-level)
- PARADIGM per-lesion vs per-patient: a model with per-lesion CCTA measures outperformed per-patient measures for predicting a future obstructive lesion (C-statistic up to 0.895) — [search summary, PubMed 32779077](https://pubmed.ncbi.nlm.nih.gov/32779077/) (not verified against full text)

### Inferences
- Plaque is spatially clustered (proximal segments, near bifurcations, around existing plaque) and patient-level burden is a strong predictor. Much of the "neighbour" signal may therefore be captured by patient-level covariates (total baseline plaque, segment involvement score) plus segment identity. A GNN's added value must be shown against a per-segment model that already includes patient-level plaque burden and segment ID; otherwise a gain may just be patient-level information leaking through neighbours.
- Recommended ablation ladder for the thesis: per-segment model with own features; + patient-level burden; + explicit parent/child neighbour features; full GNN. This mirrors the "no information flow" ablation in Hampe et al.

### Gaps
- No published neural model quantifying the incremental value of neighbour-segment plaque for future plaque prediction.
- PARADIGM new-plaque abstract does not report segment adjacency; the radiomics new-plaque paper was paywalled.

## 5. Model size and parameter counts in small-cohort vascular GNN studies

### Takeaway
Published coronary/airway GNNs are shallow (2-3 message-passing layers) and narrow (32-256 hidden units), trained on 71-511 patients; explicit parameter counts are rarely reported. At ~2000 patients this regime is comfortably feasible; the bottleneck is the number of positive events per segment, not graph size.

### Cited Findings
- Hampe et al.: 3 GAT layers, 4 heads x 8 = 32 hidden features, dropout 0.2, 79 training scans — [PMC11095121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)
- CPR-GCN: 3 GCN blocks x 256 hidden channels plus 3D CNN (64 ch) + 4-layer BiLSTM (128) image branch; 511 subjects; more than 3 GCN blocks gave no improvement — [ar5iv](https://ar5iv.labs.arxiv.org/html/2003.08560)
- Li et al.: 2 graph layers + FC, 141 patients (arXiv) — [ar5iv](https://ar5iv.labs.arxiv.org/html/2212.00386)
- Physics-informed FFR GNN and TreeVes-Net rely on 6,000-13,000 synthetic trees to reach their accuracy, with ~180 real trees for validation — [MICCAI 2023](https://conferences.miccai.org/2023/papers/135-Paper0259.html); [x-mol](https://www.x-mol.com/paper/5980171)

### Inferences
- Rough count (own estimate, not from the papers): a 3-layer GAT with 32 hidden units and ~20 input features has on the order of 5,000-10,000 parameters; a 3 x 256 GCN on ~20 inputs is roughly 140,000 parameters excluding the image branch. With ~2000 trees and ~30,000-36,000 segment nodes, a model in the 10^3-10^5 range is reasonable; anything with a per-segment 3D image encoder would need pretraining or freezing.
- Coronary trees are tiny graphs (Hampe: mean 33 segments, 20-61), so receptive field of 2-3 hops already spans most of a main vessel; deeper GNNs would oversmooth.

### Gaps
- No parameter counts were explicitly reported in retrieved sources; values above are derived.
- No study on sample-size requirements for coronary GNNs with sparse outcome labels.
