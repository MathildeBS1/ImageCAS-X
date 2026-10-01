# Junction tokenization: what the vascular graph-learning literature actually builds

Scope: whether any published vascular (coronary, cerebral, retinal) graph or sequence model treats a
bifurcation as a distinct node/token type with its own feature vector, separate from ordinary
centerline-point or vessel-segment nodes, and what that vector contains. Grounds Bjørn's request
("tokenize your tree", node features "xyz coordinates, lumen radius, arc-length from root, depth,
L/R embedding", "a fixed set of learned latent queries cross-attending to a variable-size node set",
[from_superviser.tex](file:///zhome/e2/6/224426/project/ImageCAS-X/from_superviser.tex)) in what
actually exists, rather than in what sounds plausible.

Labels: **[FT]** methods section read via WebFetch and quoted/paraphrased directly, **[SNIP]** search-
result summary only, no full text read, **[ABS]** abstract-level claim.

## Q1. Do coronary-artery GNN labeling papers give bifurcations their own node type and feature set?

### Takeaway
**No. Every coronary-artery graph-labeling paper found treats the bifurcation as a topological
event that starts a new segment, not as a node with its own, differently-composed feature vector.**
Nodes are either individual centerline points or whole segments, and every node in the graph gets
the same feature schema regardless of whether it sits at a branch or mid-vessel.

### Cited findings
- A coronary CTA extraction-and-labeling GNN builds the graph with "each point in the centerline
  ... a node in the graph", so all points, including bifurcation points, are the same node type.
  Its actual unit of classification is the *segment* (sequence of points between bifurcations), and
  every segment gets an identical feature schema: location (Cartesian coordinates at start, end and
  each quartile relative to the LV myocardium centre), orientation (direction vectors), geometry
  (mean and SD of vessel radius over the segment) and appearance (tracker-uncertainty and seed-CNN
  entropy). Trained on 79 scans (46 + 33 from two hospitals), tested on 25. Architecture: three
  GAT layers, dense input connections, four attention heads of eight encodings each [FT] ([PMC11095121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)).
- A second coronary-labeling paper using geometric deep learning also makes *segments* the nodes
  ("whenever branches bifurcate, we treat the resultant segment as a new node"), so a bifurcation is
  represented only implicitly, as the boundary between two segment-nodes, never as its own node.
  Features are start/end/midpoint coordinates and directional vectors, re-parametrised onto an
  S²×S² manifold to handle angular periodicity. No radius or diameter feature is used at all [FT] ([arXiv 2212.00386](https://arxiv.org/html/2212.00386v1)).
- AGMN (graph-matching network for angiographic semantic labeling) could not be read in full text
  this session; the fetched PDF did not extract cleanly and no methods passage on node-feature
  construction could be recovered. Left as a gap rather than guessed at [gap, not usable] ([arXiv 2301.04733](https://arxiv.org/pdf/2301.04733)).
- An intracranial-artery labeling GNN (a related cerebrovascular precedent) and its hierarchical-
  refinement follow-up were located but not read in full text this session; their existence is
  noted as further evidence that node-per-point or node-per-segment graphs, not node-per-bifurcation
  graphs, are the field's default for artery labeling [SNIP] ([arXiv 2007.14472](https://arxiv.org/pdf/2007.14472); [PMC10869117](https://pmc.ncbi.nlm.nih.gov/articles/PMC10869117)).

### Inferences
The labeling literature's graphs are built to answer "which named vessel is this point/segment on",
a different question from this thesis's "what does this junction's geometry predict". Neither
found paper needed a junction-specific feature bundle for its own task, so their silence on the
question is not itself evidence against building one; it just means **no coronary-labeling paper
supplies a template to copy**.

### Gaps
AGMN's methods were not recoverable. No paper was found that reports an ablation of "bifurcation
node with dedicated features" versus "no special bifurcation handling" for a coronary labeling or
prediction task, so the value of a distinct junction token is not literature-tested even indirectly
in this sub-area.

## Q2. Does any vascular graph pipeline compute a distinct bifurcation-level feature bundle?

### Takeaway
**Yes, one does, and it is close kin to this thesis's own locked descriptor set.** Musio et al.
2025's Circle-of-Willis centerline-graph pipeline, already trusted elsewhere in this project's
report chain for its segment-level radius reliability numbers, explicitly computes bifurcation
features *separately* from segment features, and the bifurcation feature list is built from the
same Finet and Huo-Kassab formulas this thesis has already locked.

### Cited findings
- "The centerline graph is subdivided based on the anatomical segments and bifurcations of the CoW,
  and a comprehensive set of morphometric features is computed for each segment and bifurcation
  separately." For major bifurcations (basilar artery, ICA), the feature bundle is three bifurcation
  angles, individual parent-to-child radius ratios, a radius sum ratio, an area sum ratio, and a
  bifurcation exponent; minor bifurcations get only the three angles. The paper states the radius-
  and area-based metrics explicitly "include individual ratios between the radii of the parent and
  child vessels, the radius and area sum ratios, as well as the bifurcation exponent" [FT, methods
  text fetched and quoted directly] ([arXiv 2510.13720](https://arxiv.org/html/2510.13720v1)).
- The paper names its formulas explicitly: the Finet relation r_p = 0.678·(r_c1 + r_c2), described
  as "the empirical Finet formula for vascular bifurcations", and the Huo-Kassab optimality relation
  r_p^(7/3) = r_c1^(7/3) + r_c2^(7/3), from "the minimum energy hypothesis" [FT] ([arXiv 2510.13720](https://arxiv.org/html/2510.13720v1)).
- Its windowing differs from this repo's r_J-relative convention: daughter directions are taken from
  points "located 1 mm away from the bifurcation... to obtain more stable directions", and daughter
  radii are sampled "at the maximum distance from the bifurcation point to the start of each child
  vessel", i.e. a **fixed 1 mm offset**, not a radius-scaled offset like this repo's `1·r_J` [FT] ([arXiv 2510.13720](https://arxiv.org/html/2510.13720v1)).

### Inferences
**This is the closest real precedent for a "junction token", and it validates content, not
architecture.** Every scalar in this thesis's already-locked bifurcation descriptor set (Finet
ratio, daughter ratio, Γ_HK-style optimality deviation, parent-to-daughter ratios, angle) has a
direct counterpart in a 2025 published pipeline on a different vessel bed. That is independent
convergent support for the descriptor *list*, from a source that was not consulted when the list
was locked in [Coronary bifurcation diameter descriptors.md](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Coronary%20bifurcation%20diameter%20descriptors.md).
It is not, however, evidence for a *learned* junction token: Musio's bundle is hand-computed
morphometry, fed presumably into downstream statistics rather than into a trained embedding layer.
The one design difference worth flagging is the window: a fixed 1 mm offset is a different
convention from this repo's `1·r_J`, and given the diameter report's own finding that the LCx flare
does not clear by 1 mm in a majority of ImageCAS-X cases (flare end median 2.5 mm, IQR up to 5 mm),
copying Musio's fixed-mm offset would likely reintroduce the same flare contamination the diameter
report worked to avoid. The r_J-relative window should be kept, not replaced.

### Gaps
Whether Musio's bifurcation feature bundle is ever fed to a downstream classifier (versus reported
only descriptively) was not established; the fetched text covered feature *construction*, not its
consumption. No accuracy or reliability number for the bifurcation-level features specifically (as
opposed to the segment-level radius reliability already cited elsewhere in this project) was
retrieved.

## Q3. Does the retinal-junction literature classify junctions using calibre-type features, and are those features ever fused into an outcome model?

### Takeaway
Retinal vascular-junction papers do use geometric junction features, angle and diameter
relationships among them, but for a different task: classifying a detected point as a bifurcation
versus a crossing, not predicting a clinical outcome. None of the found papers fuse junction
features into a downstream disease-prediction model the way this thesis intends.

### Cited findings
- Deep-learning junction detectors (an RCNN-based proposal network followed by a refinement and a
  classification network) locate and classify retinal junctions as bifurcation or crossover; a
  separate GCN-based approach uses "topological, geometric, and color features of vessels" for the
  same classification task [SNIP] ([ScienceDirect S016926071930940X](https://www.sciencedirect.com/science/article/abs/pii/S016926071930940X); [ScienceDirect S0957417425005494](https://www.sciencedirect.com/science/article/abs/pii/S0957417425005494)).
- Earlier, non-deep-learning work on the same problem extracted "geometric properties like angles
  and diameter relationships" as junction feature vectors for classification [SNIP] ([ResearchGate 261465030](https://www.researchgate.net/publication/261465030_Detection_and_Classification_of_Bifurcation_and_Branch_Points_on_Retinal_Vascular_Network)).
- This project has already separately sourced the retinal *optimality-ratio* literature (Witt et al.
  2010, cited in [Coronary bifurcation diameter descriptors.md](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Coronary%20bifurcation%20diameter%20descriptors.md))
  for the Γ descriptor itself, which is a distinct strand from this junction-detection literature.

### Inferences
The retinal-junction detection strand answers "is this point a bifurcation", which this thesis does
not need (ImageCAS-X and CAS-Net both deliver junction locations already, via centerline topology).
Its relevance here is narrower than it first looks: it confirms that angle and diameter-ratio
features are the standard, literature-recognised content of a junction descriptor, which again
supports the descriptor *content* already locked, but supplies no precedent for *fusing* those
features into a prediction network downstream, which is squarely this report's open question.

### Gaps
No retinal or coronary study was found that fuses junction-level calibre features into a downstream
outcome-prediction network (as opposed to a junction-type classifier or a purely descriptive
morphometric report). This is a genuine literature gap, not an oversight in the search.

## Q4. Whole-tree tokenization for generation (VesselGPT) and what it does and does not answer

### Takeaway
VesselGPT tokenizes a whole vessel tree as a sequence for autoregressive *generation*, not
classification or outcome prediction, and its token content (coordinates, spline coefficients,
control points via a learned VQ-VAE codebook) does not distinguish a junction token from a
segment token. It is a weak analogy to Bjørn's ask: it shows a working example of "tokenize the
tree" in vascular geometry, but for a different task and without the junction/segment distinction
Bjørn's proposal implies.

### Cited findings
- Vessel trees are modelled "as sequences of nodes, using Vector-Quantized Variational Autoencoders
  (VQ-VAE) to learn discrete vocabularies of tokenized node embeddings", with a transformer trained
  for "vessel tree generation through autoregressive next-node prediction". Trees are serialised by
  preorder traversal into "ordered vectors of node attributes including coordinates, spline
  coefficients, and control points" [SNIP, search summary only, full PDF too large to fetch in this
  session] ([arXiv 2505.13318](https://arxiv.org/pdf/2505.13318)).

### Inferences
VesselGPT is evidence that tree tokenization is a live technique in vascular geometry, which is
useful context for taking Bjørn's proposal seriously as engineering, not just as intuition. It
supplies no evidence either way on whether a junction-specific token content or fusion strategy
helps a downstream *prediction* task, since generation and prediction have different success
criteria.

### Gaps
The full paper was not read; whether it treats bifurcation nodes any differently from segment nodes
internally (even if the search summary did not surface it) was not confirmed by full-text reading.

## Q5. Bjørn's "learned latent queries cross-attending to a variable-size node set" grounded in architecture

### Takeaway
This is a real, named architecture pattern (Perceiver / Perceiver IO, and Set Transformer's
Induced Set Attention Block), not a novel proposal specific to this thesis. It exists precisely to
turn a variable-size, permutation-invariant input set into a fixed-length embedding via a small
number of learned query vectors that cross-attend to the input. The one documented caution that
applies directly to this cohort size is that the learned latent array itself can overfit small
datasets.

### Cited findings
- Perceiver and Perceiver IO use "asymmetric cross-attention from a small latent array to
  high-dimensional inputs, decoupling compute from input length"; the latent array performs
  self-attention among itself and only cross-attends to the (arbitrarily large, arbitrarily
  structured) input for a bounded number of cross-attention steps. Set Transformer's Induced Set
  Attention Block (ISAB) applies a similar learned-inducing-point bottleneck to set-structured
  data [SNIP, search-summary level, not independently verified against the original papers in this
  session] ([Hugging Face Perceiver docs](https://huggingface.co/docs/transformers/model_doc/perceiver); [Hugging Face Perceiver IO blog](https://huggingface.co/blog/perceiver)).
- On small datasets, "the learnable latent array is too biased to the training data" when the
  dataset is not large enough [SNIP].

### Inferences
Bjørn's proposal has a name and a working implementation family; it is not speculative
architecture. But the small-dataset caution is exactly the risk this project's own methodology
notes already flag for any network arm at n ≈ 800 with a modest event count (see
[fair_baseline_methodology.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Fair%20diameter%20scalars%20for%20regression/fair_baseline_methodology.md)'s
citation of Christodoulou et al. 2019 and the EPV arithmetic in
[Scalar tortuosity metrics for CAD models.md](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Scalar%20tortuosity%20metrics%20for%20CAD%20models.md)).
A Perceiver-style learned junction/tree token is a legitimate later experiment, not a default: it
should be compared against the explicit scalar token this report recommends as the default,
exactly as the project's B0 to B4 baseline ladder already prescribes for the whole-vessel profile.

### Gaps
No source was fetched in full for the Perceiver/Set Transformer architectural claims; they are
standard enough in the general ML literature that this is treated as background knowledge
confirmed by search rather than a claim needing full-text verification, but that distinction should
be kept honest if this note is cited for anything load-bearing.
