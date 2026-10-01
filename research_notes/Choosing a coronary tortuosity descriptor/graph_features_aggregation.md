# Tortuosity as a graph/tree feature for coronary trees: per-node, per-edge, per-branch, tree-level

Evidence grading used below: [FT] = full text fetched and read (via a summarising fetch tool, so paraphrase risk remains); [SNIP] = search-result snippet or abstract only; [FAIL] = fetch failed, only search metadata. The supervisor constraints (from_superviser.tex) are: interpretable hand-crafted descriptors, a baseline with little feature engineering (add descriptors as ablation), distances normalised so only tree structure remains, and consistent anatomical correspondence across patients (vertices at the same sequence position must mean the same anatomical point). Formula-level material (kappa_a, Q, SOAM, Grisan) is in the earlier reports and is not repeated.

Important scope note: I found NO paper that builds a coronary-tree GNN or tree-transformer with tortuosity as a node feature and ablates it. Everything below is assembled from adjacent fields (cerebral, retinal, airway, coronary single-vessel analysis). Treat the design conclusions as inference, not literature consensus.

## Q1. Local (per-vertex) vs per-branch vs whole-vessel vs tree-level tortuosity: what do vascular-graph ML papers use?

### Takeaway
Graph-learning datasets overwhelmingly attach tortuosity/curvature to EDGES (= branch segments between bifurcations) as pre-aggregated scalars, and keep nodes for geometry (xyz, radius, degree). Per-vertex local values appear mainly as an ordered vector fed to a sequence model (one coronary example), and whole-vessel single numbers are the clinical norm.

### Cited Findings
- VesselGraph (whole-brain mouse vessel graphs) puts geometric descriptors on edges: volume, length, curvature, surface-distance-based values; nodes are kept mainly to preserve curvature via their positions; edge statistics include percentiles, averages and totals of edge length, average curvature and tortuosity per edge. Evidence [SNIP] (search summary of the paper; the PDF itself could not be parsed) — [VesselGraph, ResearchGate](https://www.researchgate.net/publication/354235479_Whole_Brain_Vessel_Graphs_A_Dataset_and_Benchmark_for_Graph_Learning_and_Neuroscience_VesselGraph), code at https://github.com/jocpae/VesselGraph
- A retinal heterogeneous-graph model makes each inter-bifurcation vessel segment one NODE, with features volume, length, curvature and surface-distance values; z-score normalisation of node features; interpretability attribution links predictions to tortuosity and segment volume. Evidence [FT] — [arXiv 2502.16697](https://arxiv.org/html/2502.16697)
- Circle of Willis pipelines produce a labeled centerline graph attributed with radius, length, curvature, tortuosity per edge, plus node coordinates; the TopCoW-derived CoW centerline-graph paper reports radius, segment length and bifurcation ratios, and its fetched text did not state that curvature/tortuosity are stored. Evidence [SNIP] for the graph attributes — [TopCoW search summary, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10793481/), [Circle of Willis Centerline Graphs, arXiv abstract page](https://arxiv.org/abs/2510.13720) [FT of abstract page only]
- CaravelMetrics (cerebrovascular graph tool) computes instantaneous curvature kappa(t)=|x' x x''|/|x'|^3 on interpolated centerlines per edge, plus geodesic length, bifurcation counts (degree-3 nodes), loops, fractal features; features are computed for the whole graph or per one of 30 arterial territories of an atlas (a form of anatomical correspondence). Evidence [FT] — [arXiv 2512.03869 (html)](https://arxiv.org/html/2512.03869)
- Coronary: a local-attention transformer takes the ordered vector of per-point local tortuosity along an artery (RCA) as input, plus age and sex, letting the model learn which segments drive CAD discrimination. Local tortuosity there is the turning angle at x_i between edges x_{i-1}x_i and x_ix_{i+1}, divided by pi (range 0 to 1); vessel level = mean absolute turning angle; patient level = selecting the loop where the RCA is longest. No radius normalisation. Evidence [FT] — [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- Airway trees: GNN labeling uses node geometry (location, local radius, orientation) and branch features (orientation, mean radius, angle to parent); airway phenotyping (RadAr) computes tortuosity per branch as arc/chord, curvature/torsion/direction along branch pathways with first-order statistics per branch. Evidence [SNIP] for GNN labeling — [SPGNN, arXiv 2201.04532](https://arxiv.org/pdf/2201.04532), [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1361841524002111); [FT] for RadAr — [PMC13419480](https://pmc.ncbi.nlm.nih.gov/articles/PMC13419480/)
- Coronary geometry alignment work stores curvature/tortuosity as cumulative quantities along centerlines and organises features by bifurcation generation in a 2D array (diagonal = outlets, off-diagonal = bifurcations), with the left-main bifurcation as origin and its tangent on the x axis. Evidence [FT] — [PMC12233030](https://pmc.ncbi.nlm.nih.gov/articles/PMC12233030/)
- Recent vessel-tree tokenisers (VesselGPT, VesselTok, VeTTA) tokenise nodes/points of the centerline for reconstruction/generation; the summaries I saw do not specify hand-crafted tortuosity features, they learn geometry. Evidence [SNIP] — [VesselGPT](https://arxiv.org/pdf/2505.13318), [VesselTok](https://arxiv.org/pdf/2603.18797), [Vector Representations of Vessel Trees](https://arxiv.org/html/2506.11163)

### Inferences
- Best-supported layout: per-BRANCH (edge or branch-node) tortuosity scalars, computed on the resampled, smoothed branch polyline, are the norm; per-vertex values are optional and only justified if the model is sequence-based over a branch.
- If tokens are branches (branch-level tokenisation with anatomical segment index), tortuosity as a branch token feature matches the retinal and VesselGraph practice most directly. If tokens are centerline points, a per-vertex turning angle/pi vector is the only coronary precedent, but it inherits the noise and sampling sensitivity (Q2/Q5).
- Correspondence: the coronary/CaravelMetrics precedents index by generation or by atlas territory; the supervisor's correspondence concern is best met by attaching features to anatomically named branches (LM, prox/mid/dist LAD, etc.) rather than to sequence position.

### Gaps
- No coronary GNN/transformer paper with a tortuosity ablation found. VesselGraph and Vesselformer full texts were not readable (binary PDF), so which edge features actually help in their benchmarks is unverified.
- No graph paper found that attaches tortuosity to nodes as a windowed local feature and reports its effect.

## Q2. Scale-aware or scale-free features: normalising by radius, length, heart size

### Takeaway
Arc/chord and turning-angle-per-length are already scale-free in length units; curvature (1/mm) is not. Explicit curvature-times-radius (or window sized in local radii) has a defensible geometric basis (curvature ratio a/R in haemodynamics; radius-proportional smoothing in spline tortuosity work) but I found it used as an ML feature nowhere.

### Cited Findings
- Tortuosity is often made dimensionless via ratios such as path length over radius of curvature (L/R) and path length over wavelength (L/lambda, sinuosity); a mathematical-modelling paper argues normal tortuosity is similar across orders of magnitude of vessel size (coronary, cerebral, retinal, splenic) and follows a minimum integral-square-curvature model. Evidence [FT] — [Vascular tortuosity: a mathematical modeling perspective, PMC10717352](https://pmc.ncbi.nlm.nih.gov/articles/PMC10717352/)
- Spline-based 3D tortuosity: metrics from approximating polynomial splines fitted to "data balls" along the midline give values largely independent of image resolution, and a data-ball radius of one quarter of the local vessel radius is reported as validated. Evidence [SNIP] (PubMed page blocked; snippet from search) — [PubMed 17419088](https://pubmed.ncbi.nlm.nih.gov/17419088/)
- A tortuosity method on cortical vessels smooths the centerline with a Gaussian kernel whose scale equals the average equivalent diameter. Evidence [SNIP] (403 on fetch) — [ScienceDirect S0026286213001994](https://www.sciencedirect.com/science/article/abs/pii/S0026286213001994)
- Frenet-Serret work claims that curvature/torsion measured at sub-voxel sampling with centerline accuracy tied to vessel radius allows comparison across modality, resolution and size. Evidence [SNIP] (PDF unreadable) — [arXiv 1911.12316](https://arxiv.org/pdf/1911.12316)
- Among indices tested for 3D scale invariance and monotonic response to amplitude/frequency, the standard deviation of curvature is reported to satisfy them best. Evidence [SNIP] — attributed in the search summary to a 3D-vessel tortuosity index study; primary source not identified, treat as unverified.
- Coronary CTA study of 127 patients: the length-normalised mean absolute curvature (kappa_a) explained 6 to 27 percent of TAWSS variance, while the arc/chord tortuosity index explained none (p=0.86); centerlines were resampled at 0.01 mm. Evidence [FT] — [PMC8764056](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- The coronary local-tortuosity transformer normalises angles by pi only, not by radius or length. Evidence [FT] — [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- Airway phenotyping (RadAr) uses z-score standardisation across patients after feature selection and mentions no explicit body-size normalisation beyond ratios such as surface-area-to-volume. Evidence [FT] — [PMC13419480](https://pmc.ncbi.nlm.nih.gov/articles/PMC13419480/)
- Retinal graph model: z-score normalisation of node features. Evidence [FT] — [arXiv 2502.16697](https://arxiv.org/html/2502.16697)
- Coronary alignment framework normalises curvilinear length by total segment length. Evidence [FT] — [PMC12233030](https://pmc.ncbi.nlm.nih.gov/articles/PMC12233030/)
- Brain artery tree persistent-homology analysis avoids alignment/registration and radius measurements entirely; age correlation stays significant (rho=0.52) after controlling for total artery length, i.e. size can be regressed out post hoc. Evidence [FT] — [ar5iv 1411.6652](https://ar5iv.arxiv.org/html/1411.6652)

### Inferences
- Scale-free options in increasing strictness: (1) arc/chord or turning-angle-sum divided by length (dimensionless by construction, but sample-spacing dependent); (2) kappa*L per branch (total turning angle, radians); (3) kappa*r_local, or window length = c * local radius, which also removes dependence on vessel calibre and is the only variant that separates "bend sharp relative to lumen" from "small vessel". Only (1) and (2) have direct ML precedent; (3) has geometric support from the spline and Gaussian-scale papers and the a/R haemodynamic ratio, but no ML use found.
- Heart-size leak: no reviewed paper normalises by heart size for tortuosity. Since arc/chord and angles are already unit-free, tortuosity is naturally size-robust; the leak comes from lengths, xyz and arc-from-root, which the supervisor already wants normalised (for instance by branch length, tree total length, or LM-to-crux reference).

### Gaps
- No source found using curvature*radius as a feature, nor arc/chord in a fixed window in units of local radius. That combination should be presented as our proposal, not as literature practice.
- The exact scale-invariance study behind the "SD of curvature" claim was not identified.

## Q3. Aggregating local values to segment and tree descriptors

### Takeaway
Reviewed studies overwhelmingly use the mean (of absolute curvature or turning angle) per vessel or branch, sometimes with several first-order statistics, and then either per-anatomical-segment values or eight-plus statistics per feature at tree level. Distribution-aware summaries (percentile, max, RMS) appear as alternatives, with evidence that mean absolute curvature is best behaved.

### Cited Findings
- Mean absolute curvature (kappa_a) had the highest R^2 with low wall shear stress, was closest to normally distributed, and was recommended over the tortuosity index; RMS curvature and squared-derivative curvature were intermediate. Evidence [FT] — [PMC8764056](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- RadAr computes first-order statistics along each branch, then aggregates each branch feature with eight summary statistics, separately for the whole tree (excluding trachea and main bronchi) and each of six lobes, giving 462 features per patient. Evidence [FT] — [PMC13419480](https://pmc.ncbi.nlm.nih.gov/articles/PMC13419480/) (which eight statistics is not stated in what I read)
- VesselGraph edge statistics include percentiles, averages and totals of edge tortuosity/curvature/length. Evidence [SNIP] — [ResearchGate](https://www.researchgate.net/publication/354235479_Whole_Brain_Vessel_Graphs_A_Dataset_and_Benchmark_for_Graph_Learning_and_Neuroscience_VesselGraph)
- Bullitt SOAM sums angles over consecutive point triplets divided by path length (a length-normalised aggregate, high for coils/high-frequency low-amplitude waves), ICM counts curve minima; used to separate tumour-related vasculature. Evidence [SNIP] — [PubMed 12956271](https://pubmed.ncbi.nlm.nih.gov/12956271/?dopt=Abstract)
- Left main artery phenotyping: tortuosity 1 - D/L for the LM segment only, plus bifurcation angles, ostial angle, diameters, arc length; Ward hierarchical clustering gave four clusters (short stem/thin branches; large bifurcation angle; angled ostium with curved stem/thick branches; angled ostium with straight stem), n=60 total. Evidence [FT] — [PMC10804578](https://pmc.ncbi.nlm.nih.gov/articles/PMC10804578/) (normalisation only described as "normalizing for outliers")
- Coronary transformer study: vessel level = mean absolute turning angle; the patient level takes one vessel, not a pooled statistic. Evidence [FT] — [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- Coronary alignment framework organises features by bifurcation generation and per outlet/bifurcation so cohorts can be compared generation by generation. Evidence [FT] — [PMC12233030](https://pmc.ncbi.nlm.nih.gov/articles/PMC12233030/)
- Brain artery trees: instead of geometric aggregates, the 100 largest 0-dimensional (bends) and 1-dimensional (loops) persistence values form fixed-length vectors; correlations with age were rho=0.53 (0-dim) and rho=0.61 (1-dim), and with sex p=0.032 for 1-dim. Evidence [FT] — [ar5iv 1411.6652](https://ar5iv.arxiv.org/html/1411.6652), journal version [Ann. Appl. Stat.](https://projecteuclid.org/journals/annals-of-applied-statistics/volume-10/issue-1/Persistent-homology-analysis-of-brain-artery-trees/10.1214/15-AOAS886.full)

### Inferences
- A defensible default: per branch store (mean |kappa| or total turning per length, arc/chord), optionally a high percentile as peak bend; per tree, use length-weighted means (weights by branch length so short spurious branches do not dominate) and per-named-segment values (LM, proximal/mid/distal LAD, LCx, RCA) so that missing branches are explicit missing values rather than shifting indices.
- Because length-weighted means hide localised kinks, a small histogram or 2 to 3 percentiles per tree is the natural ablation, consistent with the supervisor's "baseline first, add features as ablation".
- Sequence-model alternative: feed the ordered per-vertex vector along a resampled-to-fixed-count branch, as in the coronary transformer, which avoids choosing an aggregate but needs many more parameters and data.

### Gaps
- Which eight statistics RadAr uses was not confirmed. No reviewed study compares mean vs percentile vs max aggregation head-to-head for coronary trees.
- No length-weighted vs unweighted comparison found.

## Q4. Studies that cluster or phenotype vascular/coronary tree shape and which descriptors they used

### Takeaway
Coronary phenotyping studies are small and mostly restricted to the left main, using simple arc/chord tortuosity plus angles and diameters with Ward clustering; tree-wide shape work uses topology-only methods (persistent homology) or alignment plus curvature, and airway phenotyping is the most mature model of tree-level feature aggregation.

### Cited Findings
- LM morphological phenotypes via hierarchical clustering (see Q3): [PMC10804578](https://pmc.ncbi.nlm.nih.gov/articles/PMC10804578/) [FT]
- Left coronary tree anatomy and haemodynamics work on plaque formation exists (arXiv 2312.00257); its descriptors were not read. Evidence [SNIP] — [arXiv 2312.00257](https://arxiv.org/pdf/2312.00257)
- Coronary tree alignment via left-main bifurcation, nine features; no clustering reported. Evidence [FT] — [PMC12233030](https://pmc.ncbi.nlm.nih.gov/articles/PMC12233030/)
- Brain artery persistent homology (Bendich et al.) as above. Evidence [FT] — [ar5iv 1411.6652](https://ar5iv.arxiv.org/html/1411.6652). It was followed by persistent-homology work on pulmonary arterial trees per the search summary (not opened). Evidence [SNIP] — [Semantic Scholar entry](https://www.semanticscholar.org/paper/Persistent-Homology-Analysis-of-Brain-Artery-Trees.-Bendich-Marron/869263162d6dde4a56c8688ebbffa41a47fe3b6e)
- Airway: five morphological categories (luminal dimensions, branch length, tapering, tortuosity, global tree descriptors); global tortuosity, branching-angle heterogeneity and curvature were found significant for disease. Evidence [SNIP] for the category list, [FT] for RadAr method — [PMC13419480](https://pmc.ncbi.nlm.nih.gov/articles/PMC13419480/)
- Retinal shape-graph classification (reducing shape-graph complexity) and ring-based retinal features exist as interpretable classifiers; not read beyond titles. Evidence [SNIP] — [arXiv 2409.09168](https://arxiv.org/pdf/2409.09168), [arXiv 2608.24723](https://arxiv.org/pdf/2608.24723)

### Inferences
- The supervisor's warning that embeddings will first separate on heart size, dominance and branch count is consistent with the brain-tree result that total length carries much of the signal; regressing out or normalising length (as done for age correlations) is an established control.
- Statistical shape models of the full coronary tree with tortuosity descriptors were not found; the gap is real, not just a search miss, though coverage was limited.

### Gaps
- No tree-edit-distance study of coronary trees retrieved. No coronary statistical shape model using curvature/tortuosity retrieved. Persistent-homology coronary work not found.

## Q5. Evidence on window/chord size relative to vessel radius for meaningful 3D tortuosity

### Takeaway
The only radius-relative rules found are: spline data-balls at one quarter of local vessel radius, Gaussian smoothing at a scale equal to mean vessel diameter, and fixed physical windows (4 mm) in intracranial work. None was validated on coronaries at 0.5 mm resolution.

### Cited Findings
- Data-ball radius of 1/4 local vessel radius validated for spline-based 3D tortuosity metrics that are largely resolution independent. Evidence [SNIP] — [PubMed 17419088](https://pubmed.ncbi.nlm.nih.gov/17419088/)
- Gaussian smoothing scale s = average equivalent diameter used before measuring cortical vessel tortuosity. Evidence [SNIP] — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0026286213001994)
- A fixed 4 mm window curvature (angle between entry and exit tangent divided by 4 mm, maximum over the centerline) is used for intracranial aneurysm centerlines. Evidence [SNIP] — [PMC12971357](https://pmc.ncbi.nlm.nih.gov/articles/PMC12971357/)
- Coronary study used 0.01 mm resampling to limit discretisation error; discrete three-point turning angles (PMC13308244) have no stated spacing or smoothing rule. Evidence [FT] — [PMC8764056](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/), [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- Supervisor-side caveat: curvature/tortuosity was found fragile in his LA/LAA work. Evidence [FT] — from_superviser.tex in this repo.

### Inferences
- A radius-proportional window (chord length of roughly 1 to 4 local radii, or Gaussian sigma of order local diameter) is the best-supported principle; the numeric constant should be chosen empirically via the validation ladder in the earlier reports, with stability of branch-level values to centerline noise as the criterion.
- At 0.5 mm voxel resolution, distal coronary radii (about 1 mm) make a quarter-radius window (0.25 mm) sub-voxel; windows must be clamped to a physical minimum tied to centerline noise, which conflicts with a pure radius-relative rule. This is an inference from geometry, not from a source.

### Gaps
- No primary full text confirming the quarter-radius rule (PubMed blocked). No study relating chord size to radius for coronary CT specifically.

## Design conclusion for the thesis (inference from the above)
1. Baseline node/token features: xyz (normalised), radius (normalised), arc from root (normalised by branch or tree length), depth, L/R. No tortuosity in baseline, matching the supervisor.
2. First ablation: one branch-level scalar pair per branch (arc/chord and mean absolute curvature times local radius, or total turning per unit length), computed on smoothed, resampled polylines with radius-relative smoothing, attached to the branch token or edge; tree-level: length-weighted mean plus per-named-segment values.
3. Second ablation: per-vertex turning angle/pi as an ordered vector per branch (the only coronary ML precedent), and distribution summaries (percentiles/histogram) at tree level.
4. Report all normalisation choices as deviations; note the literature offers no head-to-head evidence for any of these.
