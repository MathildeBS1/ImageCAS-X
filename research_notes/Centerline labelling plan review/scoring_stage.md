# Stage 2 review: scoring extracted centerlines against delivered ImageCAS-X centerlines

Note on location: plan mode was active for this agent, so these notes are in the agent plan file instead of
`research_notes/Centerline labelling plan review/scoring_stage.md`. Copy them there unchanged.

Local evidence was measured on the login node (read-only, no jobs) with the repo's own loaders
(`bifurcation.io.load_centerline`, `bifurcation.graph.build_tree`) on the delivered test-split centerlines.

## How do CAT08, ASOCA and tree-level benchmarks score centerlines, and how do they define correspondence?

### Takeaway
CAT08 is the only coronary benchmark with a full centerline protocol: an ordered, monotone point-to-point correspondence on densely resampled curves, TP/FP/FN decided against the annotated reference radius, overlap measures (OV, OF, OT) kept separate from an accuracy measure (AI) computed only where tracking succeeded, and everything scored relative to inter-observer variability. ASOCA scores masks only (Dice, HD95). Tree-level benchmarks (EXACT'09, ATM'22) add branch-level detection (a branch counts if at least 80% of its centerline is correct) and tree length detected. The plan's Stage 2 has the ingredients of CAT08 overlap but lacks the accuracy/capability split, branch-level counting, and any observer reference.

### Cited Findings
- CAT08 resamples reference and evaluated centerlines equidistantly at 0.03 mm before matching, "enabling an accurate comparison". [Schaap et al. 2009, reproduced as ch. 3 of Metz PhD thesis, sec. 3.4.3](https://repub.eur.nl/pub/23756/110629_Metz,%20Cornelis%20Thimotheus.pdf)
- CAT08 clips the evaluated centerline with a disc at the reference start point (disc radius = twice the annotated vessel radius, normal = reference tangent); everything before the first intersection is ignored, because extracted centerlines may begin in the aorta. [Metz thesis, sec. 3.4.3](https://repub.eur.nl/pub/23756/110629_Metz,%20Cornelis%20Thimotheus.pdf)
- Correspondence is the minimum total Euclidean length set of connections between the two ordered point lists, with first connection joining start points, last joining end points, and each step advancing one index on one curve (a monotone, DTW-like alignment), solved with Dijkstra. Every point on each curve is connected to at least one point on the other. [Metz thesis, sec. 3.4.3](https://repub.eur.nl/pub/23756/110629_Metz,%20Cornelis%20Thimotheus.pdf)
- A reference point is TPR if at least one connected evaluated point lies within the annotated radius, else FN. An evaluated point is TPM if at least one connected reference point lies within the radius defined at that reference point, else FP. [Metz thesis, sec. 3.4.4](https://repub.eur.nl/pub/23756/110629_Metz,%20Cornelis%20Thimotheus.pdf)
- OV = (|TPM| + |TPR|) / (|TPM| + |TPR| + |FN| + |FP|), described as similar to Dice. OF = fraction of reference points that are TP before the first FN when walking from the start, ignoring FNs in the first 5 mm (5 mm being the average annotated diameter at the start of the reference centerlines). OT = OV restricted to the clinically relevant part: segments with diameter >= 1.5 mm or proximal to such segments, operationalised as everything proximal to the most distal reference point with radius >= 0.75 mm. [Metz thesis, sec. 3.4.4](https://repub.eur.nl/pub/23756/110629_Metz,%20Cornelis%20Thimotheus.pdf)
- AI (average inside) is the mean length of connections shorter than the annotated radius at the connected reference point: "in case of a tracking failure the magnitude of the distance to the reference centerline is no longer relevant and should not be included in the accuracy measure." [Metz thesis, sec. 3.4.4](https://repub.eur.nl/pub/23756/110629_Metz,%20Cornelis%20Thimotheus.pdf)
- CAT08 converts each measure to a score: 100 = perfect, 50 = equal to inter-observer agreement, linear in between; for accuracy, per connection, 100 - 50(Am/Aio) if Am <= Aio, else 50(Aio/Am). Inter-observer variability was computed from the three observers' uncorrected centerlines. [Metz thesis, sec. 3.4.5](https://repub.eur.nl/pub/23756/110629_Metz,%20Cornelis%20Thimotheus.pdf)
- CAT08 reference: 32 CCTA scans, 4 vessels each, 3 observers, consensus by mean shift; reference centerlines averaged 138 mm (34 to 249 mm). [Metz thesis, sec. 3.4.2](https://repub.eur.nl/pub/23756/110629_Metz,%20Cornelis%20Thimotheus.pdf); [Schaap et al. 2009, Med Image Anal 13(5):701-714](https://repub.eur.nl/pub/24468)
- Wolterink et al. 2019 restate the CAT08 definitions (OT = radius >= 0.75 mm) and report OV 93.7% on the test set, AI 0.21 mm test / 0.23 mm train, versus an average inter-observer difference of 0.20 mm on the training set. [Wolterink et al. 2019, arXiv 1810.03143](https://arxiv.org/abs/1810.03143)
- Where no point-wise reference existed (UMCU, 5,448 markers), Wolterink et al. scored "hits": a marker within radius distance of an extracted centerline point, plus whether the extracted centerline reached the annotated ostium. Fully automatic ostium detection had an error of 1.8 +/- 1.0 mm over 36 scans; tree completeness was scored by an observer per clinically relevant segment (92% identified). [Wolterink et al. 2019](https://arxiv.org/abs/1810.03143)
- ASOCA (MICCAI 2020; 40 train + 20 test CCTA, 3 annotators combined by majority vote) ranks on Dice and 95% Hausdorff distance only; centerlines are released as data but are not a scored output. [ASOCA challenge site](https://asoca.grand-challenge.org/); [Gharleghi et al. data descriptor, arXiv 2211.01859](https://arxiv.org/abs/2211.01859)
- ATM'22 (airways) uses tree length detected TD (fraction of GT centerline inside the prediction) and branches detected BD = Bdet / Bref, where a branch is correct "only if more than 80% of centerline voxels extracted from the certain branch are within the ground-truth"; ranking is the mean of TD, BD, DSC and precision. [Zhang et al., ATM'22, arXiv 2303.05745](https://arxiv.org/abs/2303.05745)
- ImageCAS-X itself scores centerlines only through skeletonised masks: clDice, ASSD, HD95 (paper Statistical Measures; Table 2: CAS-Net clDice 93.3, ASSD 0.73 mm, HD95 5.75 mm; inter-observer clDice 95.4, ASSD 0.53 mm, HD95 4.58 mm). No overlap, bifurcation or branch metric is reported. [Bransby et al. 2026, arXiv 2608.30404](https://arxiv.org/abs/2608.30404) (local text: scratchpad `icx.txt` lines 242-275, 700-712)

### Inferences
- The plan's "fraction of delivered points within local radius of an extracted point, and the reverse" is exactly CAT08's TPR and TPM ingredients, but with unordered nearest-neighbour correspondence. It should also report OV (combined), an OT analogue (radius >= 0.75 mm), and an AI analogue (mean distance over TP points only). Without AI, mean distance and HD95 mix accuracy with capability: one spurious 20 mm spur moves both.
- Ordered CAT08 correspondence needs paired start and end points per vessel. That exists for delivered trees (labelled, ostium-to-end paths) but not for unnamed extracted trees before Stage 3. Practical compromise: nearest-neighbour correspondence on densely resampled curves (cheap and symmetric), plus a per root-to-leaf path OF analogue on the delivered side (walk each delivered ostium-to-terminus path, find the first point with no extracted point within radius, ignoring the first 5 mm).
- Add ATM'22-style branch-level counts (see the branch question) rather than only point fractions; a missed small branch is a small point fraction but a whole missed branch clinically.

### Gaps
- I could not open Schaap 2009 in the journal version; definitions are taken from the identical chapter in Metz's thesis. Exact CAT08 inter-observer OV/OF/OT values were not extracted.
- Kirisli et al. 2013 (stenosis framework) and the ASOCA challenge paper's full text were not read; whether ASOCA reported any centerline-derived metric in the 2022 CMIG paper is unconfirmed beyond the challenge site.

## How should branch and bifurcation detection be scored?

### Takeaway
Use one-to-one matching with an explicit tolerance, report precision, recall, F1 and the localisation error of matched pairs, and score terminal branches by the fraction of their length that is correct (ATM'22's 80% rule), not by "no delivered point within tolerance". Betti numbers are cheap but coarse; Betti matching and tree edit distance exist but add little at this stage. Local data show that the plan's "matched within 3 mm" count is ambiguous without one-to-one assignment.

### Cited Findings
- Delivered test trees (160 cases, 320 sides): 935 bifurcation-flagged vertices. Among sides with at least two bifurcations, 19.6% have a pair closer than 3 mm (44 pairs in total), and the 5th percentile of each side's closest bifurcation pair is 1.50 mm (no pair < 1 mm). Measured with `bifurcation.io.load_centerline` on `branch_points`. [repo: bifurcation/io.py](file:///zhome/e2/6/224426/project/ImageCAS-X/bifurcation/io.py)
- Delivered terminal segments (first 80 test cases, 648 terminal segments via `graph.build_tree`): length p5 10.5 mm, p10 14.0 mm, p25 24.1 mm, median 40.5 mm; 0.6% shorter than 5 mm and 4.3% shorter than 10 mm. Median tree length per side 273 mm. Per side, median 4 bifurcations / 6 ends (left) and 1 / 3 (right) in 16 train cases. [repo: bifurcation/graph.py](file:///zhome/e2/6/224426/project/ImageCAS-X/bifurcation/graph.py)
- ATM'22 branch rule: a branch is detected only if more than 80% of its centerline voxels are within the ground truth. [ATM'22, arXiv 2303.05745](https://arxiv.org/abs/2303.05745)
- TopCoW (Circle of Willis) combines mask metrics with clDice, class-average Betti-0 error, F1 for detection of specific communicating arteries, and graph-level variant classification (variant-balanced accuracy, topology match rate). [Yang et al., TopCoW, arXiv 2312.17670](https://arxiv.org/abs/2312.17670)
- Betti number error ignores where features are; the Betti matching error matches persistence barcode features spatially and is "more sensitive than the well-established Betti number error". [Stucki et al., ICML 2023](https://proceedings.mlr.press/v202/stucki23a.html)
- `utils/metrics.py` already provides volumetric Betti-0/Betti-1 errors (26-connectivity, b1 from Euler characteristic) on masks. [repo: utils/metrics.py lines 4-34](file:///zhome/e2/6/224426/project/ImageCAS-X/utils/metrics.py)
- Vessel-graph work (Vesselpose, 2026) proposes false splits and false merges as interpretable graph topology errors; the abstract-level read did not give tolerance values. [Palaniappan et al., arXiv 2605.00538](https://arxiv.org/abs/2605.00538)
- Search-snippet only (not verified in full text): Zhang et al. (CVPR 2021) count a GT centerline point as recalled if within max(r, sqrt(2)/2 voxel) of the reconstruction, and score bifurcations by the number detected within distance D plus the mean distance to the closest detected bifurcation. [Zhang et al. 2021, arXiv 2103.14268](https://arxiv.org/abs/2103.14268)
- Tree edit distance (TED) is the classical tree metric with good algorithmic properties but poor geometric properties; QED was proposed for statistics in tree space; geodesic tree-space distances were used to label airway trees with expert-level accuracy. [Feragen et al., arXiv 1207.5371](https://ar5iv.labs.arxiv.org/html/1207.5371); [hierarchical geodesic airway labelling](https://pure.eur.nl/en/publications/a-hierarchical-scheme-for-geodesic-anatomical-labeling-of-airway-/)

### Inferences
- Fault 1, bifurcation matching: "the number matched within 3 mm" double-counts when two delivered bifurcations are within 3 mm (20% of multi-bifurcation sides), and a skeleton commonly splits one trifurcation into two nearby degree-3 nodes. Use Hungarian assignment (scipy `linear_sum_assignment`) with a 3 mm gate; report TP, FP (extracted unmatched), FN (delivered unmatched), precision, recall, F1, and the matched-pair distance distribution. Optionally require that matched bifurcations also have corresponding child branches, so a spur near a real bifurcation does not count as a correct bifurcation.
- Fault 2, spurious terminal branch rule: "spurious = no delivered point within tolerance" will almost never fire, because a spur's proximal points sit next to the parent centerline. Score a terminal branch as spurious if less than ~80% (ATM'22 rule) of its length is within tolerance of the delivered tree, or equivalently by its length outside tolerance. Mirror for missed delivered branches (detected if at least 80% of its length is covered). Report branch counts and their lengths, since the delivered data say real terminal branches are almost always >= 10 mm.
- Internal (non-terminal) branch misses and breaks are not covered by the plan: a mid-vessel gap produces a dropped component (logged) but no per-branch error. Add tree length detected (TD, length-weighted recall), Betti-0 of the extracted graph per side (components), and count of root-to-leaf paths interrupted before their terminus (an OF analogue).
- Tree edit distance and Betti matching are not worth implementing for Stage 2: unlabelled TED on tens of nodes is dominated by tiny spur differences, and Stage 3 labelling gives the clinically interpretable topology comparison (per-label presence) anyway.

### Gaps
- No coronary paper was found that fixes a bifurcation tolerance by a principled rule; the 3 mm figure in the plan has no cited precedent. Full text of Zhang 2021 and Vesselpose was not read, so their tolerance values are unverified.

## Is duplicating utils/metrics.py justified, or should the plan reuse it?

### Takeaway
Do not duplicate. `compute_centerline_point_metrics` already computes the symmetric mean distance and HD95 between two centerline point sets in LPS mm with the same aggregation as the benchmark's `centerline_md`/`centerline_hd95`; Stage 2 should call it, and add only what is missing (radius-gated overlap, AI, branch and bifurcation counts). Also run the existing raw-skeleton path on the same cases to anchor Stage 2 to the paper's Table 2.

### Cited Findings
- `compute_centerline_metrics(pred_mask, ref_img, gt_pts)` (lines 146-178) skeletonises the predicted mask with `skimage.morphology.skeletonize`, converts voxel indices to LPS mm, queries KDTree both ways, returns `centerline_md` = mean of the two directed means and `centerline_hd95` = max of the two directed 95th percentiles. Raises on empty mask/skeleton/GT. [repo: utils/metrics.py](file:///zhome/e2/6/224426/project/ImageCAS-X/utils/metrics.py)
- `compute_centerline_point_metrics(pred_pts, gt_pts)` (lines 181-204) does the same on two point sets directly, documented as "directly comparable" to the mask version. It is already used by `evaluate.py` multi-class mode per segment label. [repo: utils/metrics.py](file:///zhome/e2/6/224426/project/ImageCAS-X/utils/metrics.py); [repo: evaluate.py lines 376-380](file:///zhome/e2/6/224426/project/ImageCAS-X/evaluate.py)
- `cl_dice` (lines 71-91) is the Shit et al. 2021 Tprec/Tsens harmonic mean on skeletons of masks. `compute_local_dice` (lines 215-247) computes Dice in a fixed physical-size cube at each GT centerline point. `_mm_to_voxel_indices` (207-212) maps LPS mm to voxel indices. [repo: utils/metrics.py](file:///zhome/e2/6/224426/project/ImageCAS-X/utils/metrics.py)
- `evaluate.py` multi-class mode has `_load_centerline_by_segment`, which splits a scan's left/right VTKs by `segment_label` and warns rather than silently pooling when the array is missing; per-segment centerline MD/HD95 are scored only where both sources contain the segment. [repo: evaluate.py lines 273-302, 373-380](file:///zhome/e2/6/224426/project/ImageCAS-X/evaluate.py)
- `bifurcation/radius.py:radius_at(points, mask, affine)` measures radius as the distance to the nearest background voxel centre bordering the lumen (an EDT sampled at the point), over-reading by up to half a voxel; the GT radius cache currently holds only 16 cases (32 files) in `$ImageCAS_X_results_path/centerline_radius`, none from test. [repo: bifurcation/radius.py](file:///zhome/e2/6/224426/project/ImageCAS-X/bifurcation/radius.py)
- README maps `centerline_md` to "symmetric (ASSD): mean(MD(g->p), MD(p->g)); pred skeleton vs GT centerline points", and the paper's Table 2 reports ASSD under the centerline columns. [repo: README.MD line 266](file:///zhome/e2/6/224426/project/ImageCAS-X/README.MD); [Bransby et al. 2026](https://arxiv.org/abs/2608.30404)

### Inferences
- Reuse: call `compute_centerline_point_metrics(extracted_pts, delivered_pts)` per side for MD and HD95. Reuse `radius.radius_at` on the GT mask at delivered points for the tolerance (compute it for test first with `python -m bifurcation.radius --split test`, a CPU job). Reuse the `segment_label` split idea for per-label recall. New code is then only: radius-gated TP/FP/FN and AI, Hungarian bifurcation matching, branch-level coverage, ostium distance.
- Anchor to the benchmark: run `compute_centerline_metrics` (raw skeleton, no pruning or smoothing) on the same CAS-Net test predictions. That reproduces the paper's 0.73 mm / 5.75 mm column on our cases, and the difference to the Stage 1 pipeline shows what pruning and smoothing buy.
- Discrepancy to flag: CLAUDE.md says "ASSD is not implemented ... the paper's ASSD 0.73 mm column cannot be reproduced. `centerline_md` is not the same thing". The README and Table 2 indicate the 0.73 mm ASSD is the centerline column and `centerline_md` is its implementation. The surface (lumen) ASSD is indeed absent, but the centerline ASSD appears reproducible. Worth checking with the user before relying on either statement.
- Sampling bias in reused code: KDTree nearest-vertex distances are point-count weighted. Delivered vertex spacing is median 0.45 mm (p5 0.34, p95 0.61; measured on 20 test cases). A point lying exactly on the delivered curve can read up to about half a spacing (~0.22 mm) from the nearest vertex, which is close to the plan's "mean distance <= 0.3 mm" verification target. Resample both curves to a fine equal arc-length spacing (CAT08 uses 0.03 mm; 0.05 to 0.1 mm suffices) before calling the function, or compute point-to-segment distances. Equal spacing also makes the directed means and HD95 length-weighted rather than vertex-weighted.

### Gaps
- Whether `skimage.morphology.skeletonize` in the installed version is the Lee 1994 algorithm for 3D (it is in recent scikit-image) was not checked against the installed version.

## Is a fixed 3 mm bifurcation tolerance and a local-radius tolerance sensible?

### Takeaway
A radius tolerance is the field standard (CAT08, Wolterink hits) and right for overlap, but in distal ImageCAS-X vessels it shrinks to about 0.5 mm, near the native voxel size and the vertex-spacing floor, so it needs a floor. A single 3 mm bifurcation tolerance is arbitrary: report matched fraction over a sweep (1, 2, 3, 5 mm) and the matched-pair distance distribution, and use one-to-one matching.

### Cited Findings
- ImageCAS scans: 512 x 512 x (206-275) voxels, in-plane spacing 0.29-0.43 mm, slice spacing 0.25-0.45 mm. [Bransby et al. 2026](https://arxiv.org/abs/2608.30404) (icx.txt line 99)
- Delivered centerlines were made by skeletonising the corrected mask (Lee 1994) and Gaussian smoothing (sigma 0.5 mm, 5-vertex window); start points are degree-1 vertices within 5 mm of the aorta; bifurcations are degree >= 3 vertices. [Bransby et al. 2026](https://arxiv.org/abs/2608.30404) (icx.txt lines 168-175)
- GT lumen radius at delivered centerline points (16 train cases, radius cache): p5 0.51 mm, p25 0.68, median 0.87, p75 1.11, p95 1.54 mm. [repo: bifurcation/radius.py cache](file:///zhome/e2/6/224426/project/ImageCAS-X/bifurcation/radius.py)
- `radius_at` over-reads by up to half a voxel, identically for reference and prediction. [repo: bifurcation/radius.py docstring](file:///zhome/e2/6/224426/project/ImageCAS-X/bifurcation/radius.py)
- CAT08 uses the annotated radius at the reference point as the tolerance in both directions, the 0.75 mm radius threshold for the clinically relevant part, and 5 mm (mean ostial diameter) as the grace zone for OF. [Metz thesis, sec. 3.4.4](https://repub.eur.nl/pub/23756/110629_Metz,%20Cornelis%20Thimotheus.pdf)
- Snippet-level: Zhang et al. 2021 use max(r, sqrt(2)/2 voxel) as recall tolerance. [arXiv 2103.14268](https://arxiv.org/abs/2103.14268)
- Ostium localisation reference value: automatic ostium detection error 1.8 +/- 1.0 mm. [Wolterink et al. 2019](https://arxiv.org/abs/1810.03143)

### Inferences
- Local radius: define it unambiguously as the GT-mask radius at the nearest delivered point, in both directions (CAT08 convention), never the radius measured on the predicted mask (that would reward over-segmentation). Use max(r, floor) with floor around half the native voxel diagonal (~0.3-0.4 mm), so the distal 5% of points are not scored against a tolerance smaller than the sampling error.
- Bifurcation tolerance: a skeleton junction is displaced into the parent lumen by up to roughly the parent radius (0.5 to 1.5 mm here), and smoothing over 5 vertices (~2 mm) moves it further, so 1 mm is too strict and 3 mm is plausible. But 3 mm exceeds the closest-pair spacing on 20% of multi-bifurcation sides, so it only works with one-to-one assignment. Report the curve over 1/2/3/5 mm, or a radius-scaled gate such as max(2 mm, 2 r_parent), and say which is primary.
- Ostium distance: compare to Wolterink's 1.8 mm automatic error and to the 5 mm aorta proximity rule; also report the side assignment (left/right swap) as a separate failure count, since a swapped ostium invalidates the whole side.

### Gaps
- No published coronary study was found that derives a bifurcation tolerance from voxel size or radius; this remains a judgement call to record as a deviation.

## Should scoring be stratified, and is an inter-observer reference available?

### Takeaway
Yes: stratify by side, by vessel label (recall side directly from delivered `segment_label`; precision side after Stage 3 label transfer), by radius and distance-from-ostium bins, and by Descriptors.xlsx image quality, disease and dominance, mirroring the paper. The second-annotator test centerlines are described in the paper and anticipated by the repo's `inter_observer` config, but they are not present in the local data, so no observer reference exists for Stage 2 yet.

### Cited Findings
- Paper: every test case was re-annotated by a different, randomly selected analyst, blinded, without lead-analyst review; inter-observer centerline clDice 95.4, ASSD 0.53 mm, HD95 4.58 mm. Both annotators edited the same automatically generated initial centerlines, so the authors call inter-observer agreement an upper bound. [Bransby et al. 2026](https://arxiv.org/abs/2608.30404) (icx.txt lines 188-190, 268-271, 719-722)
- The paper stratifies by disease, image quality (Likert 1-4), dominance, coronary segment, lumen attenuation, diameter and geodesic distance from the ostium (local Dice in 8 mm cubes every fifth vertex, ~2 mm). [Bransby et al. 2026](https://arxiv.org/abs/2608.30404) (icx.txt lines 250-257, 517-528)
- Repo: `configs/inter_observer.json` defines a method named `inter_observer`, and `evaluate.py` multi-class mode loads "the observers' centerlines ... beside their masks" from a run's `predictions/` directory, so upstream expects the second observer to be supplied as a run directory. [repo: configs/inter_observer.json](file:///zhome/e2/6/224426/project/ImageCAS-X/configs/inter_observer.json); [repo: evaluate.py lines 265-267, 357-361](file:///zhome/e2/6/224426/project/ImageCAS-X/evaluate.py)
- Local data: `centerlines/` holds 1600 files (800 scans x left/right, primary annotation only); `$ImageCAS_X_results_path` has no `inter_observer` directory and `$ImageCAS_X_weights_path` has none either. Data are on Zenodo record 21887809. [Bransby et al. 2026](https://arxiv.org/abs/2608.30404) (icx.txt line 196); local `ls`
- `evaluate.py` already reads `evaluation.stratify_by` and `Descriptors.xlsx` for descriptor stratification of mask metrics. [repo: evaluate.py line 537](file:///zhome/e2/6/224426/project/ImageCAS-X/evaluate.py)

### Inferences
- Without the second observer, the `gt` source (extraction on GT masks) is the only floor, but it is not independent: the delivered centerlines are the skeleton of the same masks, so `gt` error measures implementation differences (skeletoniser, resolution, smoothing) and the automatic-vs-manual pruning gap, not observer variability. Say so explicitly and do not call it an inter-observer reference.
- Ask the authors (or check the Zenodo record) for the second-annotator test masks and centerlines. If they arrive, CAT08-style scoring relative to inter-observer (100/50/0 points) becomes possible, and the paper's 0.53 mm becomes the yardstick for MD.
- Per-label recall needs no labeller: each delivered point has `segment_label`, so "fraction of LAD/LCx/RCA/D1/... points covered" is free and is the most clinically readable output. Per-label precision has to wait for Stage 3's label transfer. Also bin recall by GT radius (< 0.75 mm vs >= 0.75 mm, i.e. CAT08's OT) and by geodesic distance from the ostium.
- The "separates segmentation error from extraction error" claim in the plan is only approximate: the pruning rule is calibrated on smooth GT masks and may behave differently on bumpier predicted masks (more spurs). Report the interaction rather than subtracting `gt` from `cas_net_pretrained`.

### Gaps
- Not confirmed whether the Zenodo record contains the second-observer annotations; the paper text checked does not say they are released.

## Statistical reporting: paired comparisons and distributions

### Takeaway
Follow the paper's own rules: patient as the unit, non-parametric two-sided tests, Wilcoxon signed-rank for paired comparisons on the same scans (here `gt` vs `cas_net_pretrained`, and Stage 1 pipeline vs raw skeleton), Mann-Whitney or Kruskal-Wallis across descriptor groups, Spearman for ordinal trends. Report per-case distributions (median, IQR, worst cases) and failure counts, not only means.

### Cited Findings
- ImageCAS-X: results are mean +/- SD; all tests non-parametric, two-sided, patient as the unit; Wilcoxon signed-rank for method vs analyst on the same scans; Mann-Whitney U and Kruskal-Wallis for independent groups; Skillings-Mack for repeated-measures bins (segments, ordinal bins); Spearman rho for monotonic trends; alpha 0.05. [Bransby et al. 2026](https://arxiv.org/abs/2608.30404) (icx.txt lines 243-264)
- Table 2 SDs are large relative to means for centerline HD95 (CAS-Net 5.75 +/- 4.98 mm; inter-observer 4.58 +/- 5.75 mm), i.e. heavily skewed per-case distributions. [Bransby et al. 2026](https://arxiv.org/abs/2608.30404) (icx.txt lines 700-702)
- CAT08 reports per-dataset and per-vessel tables, and Wolterink lists per-scan OV/OF/OT/AI with image quality and calcium score, which exposes failure cases (e.g. one poor-quality scan with OF 14.7%). [Wolterink et al. 2019](https://arxiv.org/abs/1810.03143)

### Inferences
- Aggregate per patient (left and right combined, plus per side), not per point: pooled points let long left trees dominate. Report median [IQR] alongside mean +/- SD for comparability with Table 2, and a bootstrap 95% CI over patients for the headline numbers.
- Keep NaN cases (empty side, no ostium found, side swap) as counted failures in the summary JSON instead of dropping them; this matches the repo's per-case-file convention and avoids an optimistic mean.
- The plan's verification target "mean distance <= 0.3 mm" for `gt` on val should be stated after resampling, and alongside the paper's inter-observer 0.53 mm and CAS-Net 0.73 mm so the reader can place it.

### Gaps
- No source was checked on multiple-comparison correction across the many Stage 2 metrics; the paper itself reports uncorrected p < 0.05.

## Summary of concrete recommendations for Stage 2

1. Reuse `utils.metrics.compute_centerline_point_metrics` for MD/HD95 after resampling both curves to equal arc length (0.05-0.1 mm); do not reimplement.
2. Add CAT08-style radius-gated TP/FP/FN with tolerance max(r_GT at nearest delivered point, ~0.35 mm floor); report OV, OT (radius >= 0.75 mm part), an OF analogue per ostium-to-terminus path (5 mm grace), and AI (mean distance over TP only).
3. Bifurcations: Hungarian one-to-one matching, precision/recall/F1 and matched-distance distribution, swept over 1/2/3/5 mm.
4. Branches: ATM'22-style 80%-coverage rule for missed and spurious terminal branches, plus tree length detected and component count; drop the "no delivered point within tolerance" rule.
5. Ostium: distance plus a separate side-swap and not-found count.
6. Stratify recall by `segment_label`, radius bin, distance-from-ostium bin, and Descriptors.xlsx groups; per-label precision after Stage 3.
7. Anchor: also run the raw-skeleton `compute_centerline_metrics` on the same CAS-Net cases to tie to Table 2.
8. Statistics: patient unit, Wilcoxon signed-rank for paired sources, Kruskal-Wallis/Mann-Whitney for descriptor groups, median [IQR] plus failure counts.
9. Compute the GT radius cache for test (`python -m bifurcation.radius --split test`) before scoring.
10. Request the second-observer test annotations; until then do not describe the `gt` source as an observer reference.
