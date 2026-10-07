# Stage 0/1 review: mask -> centerline extraction (plan concurrent-percolating-steele.md)

Note: plan mode was active, so these notes could not be written to the requested path
`research_notes/Centerline labelling plan review/extraction_stage.md`; copy them there.

Local evidence comes from read-only checks run with the imagecasx venv on the delivered data.
The scripts are in the session scratchpad (chk.py to chk6.py). "Train[:N]" means the first N IDs of
`paths.split_ids('train')`.

## Q1. Skeletonisation grid: anisotropic native mask vs isotropic resampling

### Takeaway
Bransby skeletonised on the native, anisotropic grid, so the plan should keep the native grid and
not resample. The delivered junction and end points sit exactly on native voxel centres. Anisotropy
here is mild (about 1.4:1), and the literature finds it has little effect on the topology.

### Cited Findings
- skimage 0.26 `skeletonize(image, *, method=None)` has no spacing argument. It uses Lee 1994 by default for 3D. — local `inspect.signature` in /work3/s254124/venvs/imagecasx; [skimage docs](https://scikit-image.org/docs/stable/api/skimage.morphology.html)
- The GT masks are anisotropic, with LAS orientation. Examples: 961 has (0.357, 0.357, 0.5) mm, 879 and 457 have (0.377, 0.377, 0.5), 718 has (0.35, 0.35, 0.5). The CAS-Net prediction for 316 is on its native grid (512x512x275, 0.369/0.5 mm). — local check chk.py
- In the delivered centerlines (train[:20]), 96.4% of end points, 97.2% of bifurcation points and 87.8% of start points lie exactly (<1e-3 voxel) on a native voxel centre. Only 1.5% of interior points do, and the median interior offset is 0.32 voxel. — local check chk2.py
- The delivered vertex step has median 0.458 mm and 5th to 95th percentile 0.345 to 0.615 mm (train[:150]). That matches 26-neighbour steps on a 0.35 to 0.5 mm grid, not a 0.5 mm isotropic grid, where steps would be at least 0.5 mm before smoothing. — chk.py
- Paper: "new centerlines were generated from the corrected masks using a skeletonisation method [28]". [28] is Lee, Kashyap and Chu 1994. — ImageCAS-X text icx.txt l.168-170, l.902
- Drees et al. make deletion depth-aware for anisotropic volumes. They resampled to anisotropy factors of 1 to 16 and found "no trend towards positive or negative impact" on topology (edge match ratio) or geometry (NetMets). — [Drees et al., arXiv 2102.03444](https://arxiv.org/abs/2102.03444)

### Inferences
- **Fault in the plan's framing (minor):** isotropic resampling would not be faithful. It changes vertex density, and with it what a "5-vertex window" means. Keep the native grid. The skeleton is in index space and is then mapped through the affine, which week3 `skeleton_graph` already does correctly.
- **Improvement: an exact-replication test.** The delivered junction and end voxels are recoverable exactly. Check what fraction of them appear in our `skeletonize(GT mask)` output. A value near 100% shows that skimage Lee reproduces their skeletoniser [28]. This is cheaper and sharper than the plan's "mean distance ≲0.3 mm" check, and it should come first.
- CAS-Net predictions arrive on that same native grid, so GT and predicted extractions are geometrically comparable.

### Gaps
- Whether Bransby used skimage's Lee implementation or another one, such as ITK BinaryThinning, is not stated. The replication test above answers it.

## Q2. Is week3 `smooth()` faithful to "σ = 0.5 mm, sliding window of 5 vertices"?

### Takeaway
Fixing junctions and ends is right; the delivered data proves Bransby did the same. Smoothing
before pruning also matches the delivered data. The kernel's exact form (distance in arc length
or in index, number of passes) is unverified.

### Cited Findings
- Paper: "Gaussian smoothing (σ = 0.5 mm) with a sliding window of 5 vertices". — icx.txt l.170-171
- Week3 `smooth` leaves polyline ends untouched and computes weights `exp(-0.5((arc_k-arc_j)/σ)^2)` over at most ±2 vertices. It reads from the unmodified `points`, which makes it a Jacobi update and order-independent. The window is truncated near ends. — `git show week3:topology/skeleton.py`
- Delivered junction and end points are on-grid (96 to 97%) while interior points are not (1.5%), so junctions and ends were held fixed during smoothing. — chk2.py
- Delivered trees contain degree-2 polyline joints, meaning a polyline split at a non-junction, on 12/80 sides (0.16 per side, train[:40]). 61.5% of these joints are on-grid. This is the signature of a junction left unsmoothed and then demoted to degree 2 when a spur was removed after smoothing. — chk4.py

### Inferences
- With a step of about 0.46 mm and σ = 0.5 mm, the weights at ±1 and ±2 vertices are about 0.65 and 0.18. So the window of 5 truncates very little and the result is close to a full Gaussian. Whether σ was applied in arc length or as index times mean step barely matters.
- The plan's order is consistent with the evidence: smooth, then prune, then re-merge degree-2 joints. A former junction stays at its on-grid, unsmoothed position, which leaves a small kink, and so does the delivered data. Re-smoothing after pruning would be a deviation; do not re-smooth if the aim is replication.
- `_degree` in week3 counts path ends, so a skan type-3 cycle path, which starts and ends on the same index, contributes degree 2. That is harmless.

### Gaps
- Number of smoothing passes and the kernel distance metric. Both are testable by fitting to the delivered interior points once Q1's replication shows the raw skeleton matches.

## Q3. Spur pruning rule and calibration

### Takeaway
The delivered trees have essentially no short terminal branches (1st percentile 7.8 mm), so
the calibration grid's upper end (5 mm, 3·r) is too low. The rule should use protrusion beyond the
parent wall normalised by radius, as in Drees's bulge size, and not raw length vs junction radius.
Calibrating on GT masks alone leaves prediction-specific spurs unvalidated.

### Cited Findings
- Delivered terminal segment lengths (train[:150], 1179 terminals): percentiles 1/5/10/25/50 are 7.8, 11.6, 16.2, 26.2 and 41.2 mm. None is shorter than 2 mm and 2 are shorter than 5 mm. — chk.py
- Delivered internal (junction-to-junction) segments: 2 of 575 are shorter than 1 mm and 14 shorter than 2 mm. 10 of 866 bifurcations have degree ≥ 4 (1.2%). — chk5.py
- Tracing protocol: "Side branches were not traced where … the diameter at the most distal point was <1 mm. Septal perforators, acute marginals and nodal arteries were not traced"; also "Where a side branch itself bifurcated, only the larger branch was traced" unless equal or >1.8 mm. — icx.txt Supplementary B (l.969-978)
- The GT mask was built from the traced centerlines: lumen predicted in cMPR volumes along each traced centerline, projected back and voxelised, then corrected slice-by-slice. — icx.txt l.155-166
- Bulge size (Drees et al.) = (length(e) − inner_length(n_b) + tip_radius(n_e)) / avgRadiusMean(e). It is defined only for leaf-to-branch-point edges, and inner length is the part of the edge inside the branching region. The authors recommend 1.5 for irregular lymphatics and say "a bulge size of 3.0 or higher can be chosen confidently" for healthy blood vessels. Pruning is iterated to a fixed point, keeps at least two edges per node ("Retain two edges"), then deletes orphans and merges degree-2 nodes. — [Drees et al., arXiv 2102.03444](https://arxiv.org/abs/2102.03444) (Sec. V-E, Alg. 1, Sec. VI-D)
- Drees et al.: pure minimum-length pruning "is problematic if vessels of different scales are present in a single dataset". — same source
- Week3 Qiu `_prune_spurs` makes a single pass, uses a fixed `min_len=4` voxels and works on raw voxels (not mm), and drops all short terminal spurs at once. — `git show week3:postprocessing/qiu/skeleton.py`

### Inferences
- **Fault: the grid is out of range.** The delivered minimum terminal length is about 8 mm. Under min_mm ≤ 5 and k ≤ 3 (k·r is about 4.5 mm for r = 1.5), almost all real terminals survive and spurs of 5 to 8 mm survive too. Extend the grid, for example min_mm up to 8 to 10 and k up to 5. Alternatively use bulge size t ∈ {1.5, 2, 3, 4, 5}.
- **Fault: the radius at the junction is the wrong normaliser.** At a bifurcation the maximal inscribed sphere, which is what `radius.radius_at` gives, is larger than either branch, so k·r_junction overstates the threshold on large parents. The skeleton branch length also includes about one parent radius inside the parent lumen. Use protrusion = length − r_parent (or inner length), compared with k times the branch's own mean radius, as in bulge size.
- **Fault: cascade erosion.** "Repeatedly delete terminal polylines shorter than …" with no guard can delete both children of a short terminal fork in the same pass, which turns the parent into a terminal that is then pruned too. Prune at most one child per junction per pass (Drees "retain two edges"), or prune the shortest first and recompute.
- **The calibration target is sound in one respect.** The GT mask contains only traced vessels (it was built from the traced centerlines), so GT-skeleton spurs come from surface bumps, bifurcation bulges and slice-wise corrections, not from untraced anatomy. The delivered tree is therefore a fair target for GT masks. The concern raised in the brief, real branches never traced and so biasing calibration, mostly does not apply to GT masks. It does apply to predictions.
- **The calibration does not transfer to predictions.** CAS-Net is trained on these masks but can still segment untraced vessels: septals, conus and acute marginals, distal branches under 1 mm, or veins. Those produce long, legitimate-looking branches that no length or radius rule should remove. Its surface noise also differs from slice-corrected GT. A setting frozen on GT will mis-prune predictions in ways the GT calibration cannot reveal. Report the pruning sensitivity on predictions as well. That needs CAS-Net val predictions, which do not currently exist: `cas_net_pretrained/predictions` holds 24 files and no `predictions_val/` dir remains on /work3. So Stage 0 must add a val inference job, or the pruning must be validated on test, which leaks.
- **Objective:** "fewest spurious + missed terminal branches" needs a defined matching tolerance and weighting. Report both counts and their trade-off curve, not a single minimum.

### Gaps
- No VMTK, Antiga or Kerautret pruning rule was retrieved in this session; only Drees (bulge size) was verified in full text. Standard vessel tools are not compared here.

## Q4. skan tracing pitfalls and `graph.build_tree` on predicted skeletons

### Takeaway
Raw skan graphs need junction-cluster collapsing, or bifurcation counts inflate relative to the
delivered data. `build_tree` breaks cycles in arbitrary BFS order. Both are fixable in a few lines.

### Cited Findings
- skan replaces clustered junction pixels by their minimum spanning tree (`_mst_junctions`), so a cluster of adjacent degree ≥ 3 voxels yields short junction-to-junction (type 2) paths. Branch types are 0 tip-tip, 1 tip-junction, 2 junction-junction, 3 cycle. Isolated cycles are traced last, and degree-0 pixels do not appear in any path. — [skan csr.py](https://github.com/jni/skan/blob/main/src/skan/csr.py)
- The delivered data has only 2/575 internal segments shorter than 1 mm and 1.2% degree ≥ 4 nodes (chk5.py). Whatever Bransby used did not leave sub-voxel junction pairs.
- `build_tree` drops "the closing edge" of a cycle as whichever chain BFS reaches second (`graph.py:431-433`), not an anatomically chosen edge. In the delivered data this occurs on 3 sides in total (1 chord in train[:150]). — bifurcation/graph.py; chk5.py
- skan is not installed in the imagecasx venv (`ModuleNotFoundError`), consistent with the plan's Stage 0. — local check

### Inferences
- **Missing step:** after tracing, contract junction-to-junction paths shorter than about 1 to 2 voxels, or shorter than the junction radius, into a single node. Without this, bifurcation counts and "matched within 3 mm" are biased, and the GNN sees fake 0.4 mm segments.
- **Cycles in predictions** arise from touching vessels (artery and vein, two branches in contact) or from cavities (plaque or low-contrast holes inside the lumen). Two improvements: fill enclosed cavities before thinning (`ndi.binary_fill_holes`; Drees cites hole filling as preprocessing in Chen et al.), and break each remaining cycle at the chain with the smallest minimum radius, not by BFS order.
- Single-voxel or tiny components produce no skan path and vanish silently. Log them with their voxel volume, in line with the "never drop silently" convention.
- Week3 `skeleton_graph` will raise on an empty mask (`idx.min` on an empty array). The driver guards against this, so it is fine.

## Q5. Ostium detection with TotalSegmentator `total` aorta, and the 5 mm rule

### Takeaway
The 5 mm rule is fragile on the `total` model. It works at 1.5 mm resolution and is reported to
leave the LVOT and aortic outflow region uncovered. Lee thinning also retracts the skeleton end by
about one vessel radius. A side that finds no ostium within 5 mm loses its whole tree under the
plan. A fallback is needed.

### Cited Findings
- The `total` task is Apache-2.0 and free. `heartchambers_highres`, which Bransby used, requires a licence ("free licenses available for non-commercial usage"). `total` runs at 1.5 mm (3 mm with `--fast`), about 2 to 3 min per scan on an RTX 3090. `--roi_subset` cuts runtime and memory. — [TotalSegmentator README](https://github.com/wasserth/TotalSegmentator)
- "the TotalSegmentator output leaves a gap between the left ventricle and the aorta. Therefore, large parts of the LVOT are missing"; TotalSegmentator "does not completely cover the aortic outflow region". — [Brosig et al., J Med Imaging 11(4):044504, 2024](https://journals.spiedigitallibrary.org/journals/journal-of-medical-imaging/volume-11/issue-04/044504/Learning-three-dimensional-aortic-root-assessment-based-on-sparse-annotations/10.1117/1.JMI.11.4.044504.full)
- Paper: start points are degree-1 vertices "lying within 5 mm of the aorta", where the aorta comes from the high-resolution heart-chambers model. — icx.txt l.171-174
- CAS-Net predictions cover the GT start points. On 24 test cases, 46 of 48 start points are inside the predicted mask (distance 0), and the other two are 1.4 and 3.0 mm away (cases 680 and 509). — chk6.py

### Inferences
- **Deviation larger than the plan states.** The paper's 5 mm was set for a sub-millimetre aorta. With a 1.5 mm model that misses part of the root, the coronary origin in the sinus can be 1 to 2 voxels (1.5 to 3 mm) further from the mask. Lee thinning also stops the skeleton end short of a blunt mask end by roughly the LM or RCA radius (about 1.5 to 2.5 mm). The error budget therefore exceeds 5 mm. Calibrate the threshold on train GT masks plus `total` aorta, by measuring the delivered start point to aorta distance, before freezing it.
- **Fault: a whole tree can be dropped.** "Components with no ostium are dropped" means that one missed threshold deletes the entire RCA or LCA. Fallback: if a side lacks an ostium, take the degree-1 vertex of the largest component nearest the aorta surface, with a looser cap, and log it.
- **False ostia:** degree-1 tips of conus or sinus-node branches, or pruning-surviving spurs near the aortic wall, can fall within 5 mm. "Nearest per component" mitigates this, but prefer the tip whose terminal branch has the largest radius, or the one nearest the root along the aorta.
- The TotalSegmentator output geometry must be matched to the mask grid, and the EDT computed with `sampling=spacing`. The aorta affine is RAS and the centerlines are LPS, so go through `coords`.

### Gaps
- No quantitative study was found of TotalSegmentator `total` aorta accuracy at the sinuses of Valsalva specifically, or of ostium localisation from it.

## Q6. Left/right rule "larger LPS x is left"

### Takeaway
The rule held on 150/150 train cases, but the minimum margin was 0.4 mm, too thin to survive
ostium-localisation error. The anterior-posterior axis separates far better: the left ostium is
14.9 to 44.1 mm more posterior. Use y, or both.

### Cited Findings
- Delivered start points, train[:150]: left x > right x in 150/150. Δx (L − R) has median 14.6 mm, 5th percentile 5.9 mm and minimum 0.4 mm. Δy (LPS, posterior +) has median 26.6 mm and range 14.9 to 44.1 mm, so the left ostium is always more posterior. — chk.py
- graph.py docstring: 11 left sides have two ostia (no LM). — bifurcation/graph.py l.9-13

### Inferences
- Anatomically, the RCA arises from the anterior (right) sinus and the LCA from the left posterior sinus, which is consistent with the data. A linear discriminant on (Δx, Δy), fitted on all 560 train cases, is more robust than x alone. For a single ostium (the other missed), compare it with the aortic root centroid along the same discriminant direction.
- With two left ostia (separate LAD and LCx), the rule must allow two components per side and not force one per side.

### Gaps
- Only 150 of the 560 train cases were checked. Rerun on all of them, as the plan already intends.

## Q7. Disconnected components

### Takeaway
Dropping components without an ostium discards real vessel: 53.9% of fragments removed from
CAS-Net test predictions overlap GT by ≥ 50%. `build_tree` can already root orphan components, so
keeping them costs almost no code.

### Cited Findings
- On the CAS-Net test split, 293 fragments removed by keep-2-largest had 53.9% with gt_fraction ≥ 0.5 (median 0.886), and 1.83 extra components per scan. — project memory `project_qiu_reconnection.md` (cas_net_pretrained_keep2 logs, 2026-09-14)
- On the 24 available test predictions, the two largest components hold under 80% of the volume in 3 cases: 676 (68%, 480 mm³ elsewhere), 909 (68%, 385 mm³) and 775 (79%, 333 mm³). — chk6.py
- `build_tree` roots a component without a start point "at its nearest point" to the rest of the tree, with a warning (2 delivered left sides do this). — bifurcation/graph.py l.384-404
- The Qiu reconnection on week3 helped overlap metrics, but its join classifier was weak (rec_acc 0.50 on test). — project memory

### Inferences
- **Improvement with almost no code:** assign each ostium-less component above a length floor to the side whose rooted tree is nearest. Write it into that side's VTK with `start_points = 0` and let `build_tree` root it. Report dropped length and orphan length separately.
- Qiu-style joins are optional. Since the join decision was close to chance, nearest-tree attachment as orphans keeps topology honest without inventing connections.
- Dropped components only "show up as missed" if scoring treats them so. Make the scoring separate "never extracted" from "extracted but orphaned".

## Q8. TotalSegmentator installation on the HPC

### Takeaway
TotalSegmentator does not pin a specific torch, so the plan's stated reason for a separate venv is
inaccurate. A separate venv is still reasonable for the nnunetv2 dependency tree. Model weights
must be redirected off /zhome.

### Cited Findings
- setup.py v2.18.0: `torch>=2.1.2`, `nnunetv2>=2.3.1`, `python_requires>=3.9`, plus about 20 other deps (SimpleITK, dicom2nifti, fury, `uharfbuzz>=0.52,<0.56.1` and others). — [TotalSegmentator setup.py](https://github.com/wasserth/TotalSegmentator/blob/master/setup.py)
- Weights default to `~/.totalsegmentator`. They can be redirected with `TOTALSEG_HOME_DIR`, and pre-downloaded with `totalseg_download_weights -t <task>`. — [TotalSegmentator docs (Algolia)](https://docsearch.algolia.com/mcp/docs/repo/wasserth/totalsegmentator); [BodyComposition README](https://github.com/fohofmann/BodyComposition)
- /zhome is at 25.9/30 GB. — CLAUDE.md

### Inferences
- Set `TOTALSEG_HOME_DIR=/work3/s254124/totalseg_home` in the job script and pre-download the weights on the login node, which has network access. Compute nodes may not.
- Runtime at about 2 to 3 min per scan (less with `--roi_subset aorta`) for 240 scans is roughly 4 to 12 GPU-hours. Split it across jobs, or skip completed cases as planned.
- Input should be `volumes/<id>.img.nii.gz`, which is the native grid, so the output aligns with the masks. Verify that the affines are equal.

## Additional faults found in the plan

- **Stage 0 omits val predictions,** which pruning validation and threshold choices need (see Q3).
- **Verification step 2 threshold** ("≲0.3 mm mean distance"): if the replication is exact, interior points should agree to about 0. Use the voxel-identity test (Q1) plus junction-count agreement, not a loose distance check.
- **Radius array** comes from `radius.radius_at`, which over-reads by up to half a voxel (documented in bifurcation/radius.py). It is fine for features, but do not use it as an unbiased pruning threshold near the 1 mm protocol cutoff.
