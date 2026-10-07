# Codebase audit of plan concurrent-percolating-steele.md (centerline extraction + GNN labeller)

Note on location: plan mode was active for this agent, so these notes are written to the one file it
may edit (this plan file) instead of
`research_notes/Centerline labelling plan review/codebase_audit.md`. Copy them there if needed.

All checks were read-only and ran on the login node with
`PYTHONPATH=. /work3/s254124/venvs/imagecasx/bin/python` from the repo root, after `source env.sh`.
Survey scripts are in the session scratchpad (`survey.py`, `s2.py` to `s5.py`). "Source" below is a
repo file:line, a data path, or the check that produced the number.

## 0. Blocking finding not in the plan: the venv's torch is CPU-only

### Takeaway
The plan's Stage 0 says to resubmit `jobs/infer_eval_cas_net.sh` to finish the 136 missing CAS-Net test
predictions. That will not work as intended. The venv holds `torch 2.14.1+cpu`, the last inference job
ran on CPU at about 30 min per case and was killed by the 12 h walltime after 24 cases. Fix torch first.

### Cited Findings
- `torch.__version__` = `2.14.1+cpu`, `torch.version.cuda` = None, `torch.backends.cuda.is_built()` = False. The dist-info is dated 2026-10-02 11:15. CLAUDE.md says the venv has torch 2.11.0+cu128, so CLAUDE.md is stale. Source: `/work3/s254124/venvs/imagecasx/lib/python3.11/site-packages/torch-2.14.1+cpu.dist-info`.
- `logs/cas_net_infer_29585272.out`: `[inference] method=cas_net device=cpu split=test`, then `TERM_RUNLIMIT: job killed after reaching LSF run time limit`. The `.err` progress bar reads `24/160 [11:58:32 ... 1790.59s/it]`. Source: `logs/cas_net_infer_29585272.{out,err}`.
- At that rate, the remaining 136 cases need about 68 h of CPU time, about six more 12 h submissions. On a GPU the job would take far less.
- `uv sync --dry-run --frozen` reports "Would uninstall ... torch==2.14.1+cpu" (plus filelock, fsspec, jinja2, markupsafe, mpmath, setuptools, sympy), because `uv.lock` has no torch entry (`grep -c 'name = "torch"' uv.lock` = 0) and `pyproject.toml:12-14` deliberately leaves torch out. Source: the dry run.

### Inferences
- If skan is added through `uv add skan` or with `pyproject.toml` followed by `uv sync`, the sync will most likely remove torch from the venv entirely, since `uv sync` is exact by default. Use `uv add --no-sync skan`, or edit pyproject and run `uv pip install skan`. Re-check with `uv sync --dry-run --frozen` first.
- The CPU torch was probably installed by an earlier sync or `uv pip` call around 2026-10-02. That is plausible but not verified.

### Gaps
- I did not determine how the CPU wheel got installed, or which CUDA wheel index to reinstall from.

## 1. bifurcation/graph.py: Segment label, _majority_label, build_tree

### Takeaway
Mostly true. `Segment.label` is an int target, and `_majority_label` exists. The function treats 14 and 0 as ordinary integers. It does not remap 0 to 14, so the 14-way head needs an explicit 0 to 14 (or ignore) mapping. `build_tree` roots each component at a flagged start point when one exists and falls back to a heuristic root when none does. It never drops a component.

### Cited Findings
- `Segment` has `label: int` and `name: str`, set by majority vote over interior points. Source: `bifurcation/graph.py:63-90`, assigned at `graph.py:436-444`.
- `_majority_label(labels)` takes the interior points (`labels[1:-1]` when len > 2), then `np.argmax(np.bincount(...))`, so ties go to the smallest label. There is no special case for 0 or 14. Source: `graph.py:358-365`.
- The docstring says label 14 and the 0 in case 272 both mean "not attributed". The code expresses this only through `artery_name`: `label_names().get(label, "Other")` maps 0 to "Other" by default, because `label_map.json` has keys 1 to 14 only. `Segment.label` stays 0. Source: `graph.py:37-49`, `knowledge/docs_thesis/label_map.json`.
- `build_tree` reads roots from `centerline.start_points` (`graph.py:379`) and pins them as junctions. Components are sorted with start-point components first (`graph.py:~400`).
- A component with more than one start point is rooted at the lowest index, with the warning "component ... has N start points".
- A component with no start point is rooted at the degree-1 node nearest the already-rooted points, with the warning "has no ostium; rooted at node ...". It is kept, never dropped. Source: `graph.py:398-418`.
- `build_tree` "never raises", and cycles are dropped into `chords`. Source: `graph.py:368-370, 423-428`.
- `_build_vessels` chains segments by `name` (`graph.py:215-240`). For predicted trees where every label is 0, every segment is "Other", so `vessels` collapses into chains. This is harmless but meaningless.

### Inferences
- The plan's "components with no ostium are dropped" must happen in `extract.py` before writing. `build_tree` would otherwise silently root an orphan.
- Writing exactly one start point per kept component means `build_tree` gives one root per component, as intended.

### Gaps
- None.

## 2. Left and right label ranges; label 14; label 0

### Takeaway
Disjoint is true, but the plan's "14 'Other' is allowed on both" is factually wrong for this data. Label 14 occurs only on the left. The right side uses exactly three labels {9, 10, 11}. Label 0 occurs in one test case only.

### Cited Findings (all 800 curated cases, both sides, `survey.py`)
- Point labels in train (560): left {1,2,3,4,5,6,7,8,12,13,14}, right {9,10,11}. Val (80) and test (160) are the same, except test left also has 0.
- Label 0: only case 272, left side, 15 points, one segment of 8 mm (test split). It never occurs in train or val.
- Label 14 points: train left 5849, val left 772, test left 1701. Right: 0 in every split.
- Segments with more than one interior label: 3/7742 in train, 0/1111 in val, 2/2208 in test. So the majority target is almost always unanimous.

### Inferences
- The right side is effectively a 3-class problem (RCA, R-PDA, R-PLA) on trees with a median of 3 segments. The left side is an 11-class problem. Masking 14 onto the right head adds a class the right side never has. Allowing it is harmless, but it is not supported by the data.
- L-PDA (12) and L-PLA (13) are left-side labels. Dominance therefore shows up as label set, not side.

### Gaps
- None.

## 3. "Left ostium has larger LPS x than right ostium" rule

### Takeaway
On delivered start points the x rule holds in 556/560 train (99.3%), 80/80 val and 158/160 test. It fails by small margins of 0.7 to 6.8 mm. Two alternatives were perfect on all 800: left ostium more posterior (larger LPS y), and left-tree centroid with larger x. Two-ostium left trees exist (8 train, 2 val, 1 test), so a rule built for exactly two ostia will meet three.

### Cited Findings (`survey.py`, `s2.py`; delivered `start_points`)
- Start point counts in train: left 1 in 552 cases and 2 in 8, right always 1. Val: left 2 in 2 cases. Test: left 2 in 1 case.
- x-rule failures as (case, left x, right x) in LPS mm: train (450, 13.4, 14.5), (703, 34.4, 41.2), (600, 15.3, 16.0), (716, 6.7, 7.4); test (509, 25.2, 27.5), (935, 30.0, 31.2).
- Alternative rules, train / val / test:
  - left ostium y > right ostium y (more posterior): 560/560, 80/80, 160/160.
  - left ostium z > right (superior): 559/560, 80/80, 160/160.
  - left-tree centroid x > right-tree centroid x: 560/560, 80/80, 160/160.
  - ostium x+y: 560/560, 160/160.

### Inferences
- The plan should replace the ostium-x rule with tree-centroid x, or ostium y, or a combination. Either one is perfect on the delivered data, and centroid x is more robust to a mislocated ostium.
- For predicted masks with more than two ostium-bearing components, assign each component to a side independently (for example by its centroid x relative to the midpoint of the two largest components) rather than ranking two ostia.
- A single predicted component that contains both trees (left and right fused through a leak) gets only one ostium under "one per component, the nearest". The other side's tree is then mis-sided. This should be logged.

### Gaps
- These rules were tested on delivered start points and delivered trees, not on predicted ostia. The aorta-distance ostium detection itself cannot be tested until aorta masks exist.

## 4. Label frequency, segments per tree, vessels split across segments, tree-consistent decode

### Takeaway
Strong class imbalance. The trees are tiny: left median 10 segments, right median 3. Named vessels routinely span several segments (LAD 553/560 cases). The "allowed transitions from train" decode would force a few test errors, because 7 test segments have parent-to-child transitions never seen in train. The plan's examples ("D only under LAD", "LM only at the root") are not strict in the data.

### Cited Findings (`survey.py`, `s2.py`, delivered trees through `graph.build_tree`)
- Segment counts by label, train. Left: LM 552, LAD 1546, LCX 1343, D1 731, D2 382, OM1 566, OM2 230, IM 179, L-PDA 37, L-PLA 53, Other 87. Right: RCA 587, R-PDA 651, R-PLA 798.
- Length by label in train (mm). Left: LM 5016, LAD 74187, LCX 49008, D1 25662, D2 12614, OM1 22631, OM2 9576, IM 5488, L-PDA 1438, L-PLA 1326, Other 2875. Right: RCA 59069, R-PDA 26465, R-PLA 30408.
- Segments per tree, train: left min/median/mean/max 4/10/10.2/21, right 1/3/3.6/9. Val and test are similar.
- Cases where a label spans more than one segment / cases with the label, train: LAD 553/560, LCX 495/560, D1 83/553, IM 38/127, R-PDA 96/518, R-PLA 136/513, RCA 25/560, LM 0/552.
- Train parent-to-child transitions: 40 distinct. Roots are LM 552, LAD 8, LCX 8 and Other 1 (left), and RCA 560 (right). The data also contains (LM to D1) 1, (LM to IM) 55, (IM to LAD) 19, (IM to LCX) 15, (Other to LAD) 2 and (R-PLA to R-PDA) 41.
- Val transitions unseen in train: 0/1111 segments.
- Test transitions unseen in train: 7/2208 segments. These are (D1 to LAD) 1, (L-PDA to L-PLA) 1, (L-PDA to L-PDA) 1, (LM to LM) 1, (right root R-PDA) 2, and (left root label 0) 1.
- `build_tree` warnings in train: 3 sides with cycle or loop warnings and 1 left side with an orphan component. Test: 1 orphan.

### Inferences
- Macro F1 over 14 labels on 160 test cases rests on about 10 to 13 test segments each for L-PDA, L-PLA and Other, and on 1 segment for label 0. Report support per class.
- A hard decode constraint costs at least 7 test segments (0.3%) by construction, plus 2 right trees whose true root is R-PDA. That is small, but the decode is not a pure win, and it should be reported as an ablation, as the plan already says.
- Because LAD, LCX and the R-PDA/R-PLA branches span several segments, "angle to parent" and the same-label continuation are strong cues. The `Vessel` chains in `_build_vessels` already encode the continuation for delivered trees.

### Gaps
- None.

## 5. radius.radius_at, io.load_centerline(root=), write_centerline_vtk round trip

### Takeaway
All true as signatures. Round trip with all-0 labels works. One unplanned prerequisite: the GT radius cache covers only 16 cases, so the "mean and proximal radius" node features are missing for nearly all delivered train trees.

### Cited Findings
- `radius_at(points_lps, mask, affine) -> np.ndarray` exists, with the signature the week3 code uses. Source: `bifurcation/radius.py:33-46`.
- `load_centerline(case_id, side, root)` reads `segment_label`, `segment_name`, `branch_points`, `end_points` and `start_points` (a KeyError if any is missing), plus `radius` if present. It uses the GT radius cache only when `root is None`. Source: `bifurcation/io.py:83-106`.
- Round trip (`s3.py`): a delivered left centerline (val case) with `segment_label` set to 0, names set to "Other" and radius set to 1 was written with week3 `write_centerline_vtk` (`git show week3:topology/skeleton.py`) to scratch and read back with `load_centerline(..., root=scratch)`. Points were equal and line count was equal (9/9). Labels came back [0], names "Other" (dtype `<U5`), radius present, 1 start point. `build_tree` gave 9 segments, the same as the original, with no warnings.
- `write_centerline_vtk` with `radius=None` did not raise. It writes a bogus `np.asarray(None)` array. Pass a real radius, as the plan does.
- Radius cache: `/work3/s254124/imagecasx_results/centerline_radius/` holds 32 files for 16 cases. `load_centerline` returns `radius=None` for every other delivered centerline (`io.py:90-95`).
- `paths.RESULTS` is hardcoded to `/work3/s254124/imagecasx_results`, which matches `$ImageCAS_X_results_path`. Source: `bifurcation/paths.py:14`, `env.sh`.
- Week3 `build_predicted_centerlines.py` calls `paths.output_dir(...)`, which does not exist in the current `bifurcation/paths.py`. The plan already adds `AORTA` and `EXTRACTED` constants instead.

### Inferences
- Add `python -m bifurcation.radius --split train` (and val, test) to Stage 0. At the docstring's ~1 s per case, that is about 15 min for 800 cases, best run as a job.

### Gaps
- None.

## 6. CAS-Net predictions

### Takeaway
24/160 test predictions exist, as the plan says, with none for train or val. They are uint8 {0,1}, `<id>.nii.gz`, at native geometry with an affine identical to the GT segmentation and volume. Fairness on test assumes the delivered weights were trained on the official train split. That is consistent with the benchmark design but not verifiable from code.

### Cited Findings
- `ls predictions | wc -l` = 24. Intersection with the filelists: train 0, val 0, test 24. Source: `/work3/s254124/imagecasx_results/cas_net_pretrained/predictions/`.
- Cases 316, 368, 423 and 448: shape (512,512,275), zooms such as (0.369, 0.369, 0.5), dtype uint8, values {0,1}, affine equal to the segmentation and the volume (atol 1e-3).
- Fragments in 8 predictions: connected components (26-connectivity) range from 2 to 6 per case. Extra components are 105 to 799 voxels, for example 316: [13073, 11736, 422, 347, 190]. Source: `s5.py`.
- `jobs/infer_eval_cas_net.sh` resumes (`inference.py:462`), but see section 0: it runs on CPU.
- Only `cas_net_pretrained` exists under the results root, not the nine `*_pretrained` dirs that CLAUDE.md describes.

### Inferences
- Several small fragments per case will become dropped no-ostium components. The plan logs their length, which is correct, but expect a non-trivial "missed" share.

### Gaps
- Which split the delivered CAS-Net weights were trained on. README and `cas_net_walkthrough.md:73` describe a 560/80/160 split, but the weights' provenance (Zenodo) was not checked.

## 7. skan, uv, dependency conflicts

### Takeaway
skan is absent and uv exists. A dry-run install adds only numba/llvmlite/toolz and does not change numpy. The real hazard is the uv sync path removing torch (section 0).

### Cited Findings
- `import skan` gives ModuleNotFoundError. `which uv` = `/zhome/e2/6/224426/.local/bin/uv`.
- `uv pip install --dry-run skan` would install llvmlite 0.50.0, numba 0.68.0, skan 0.13.1 and toolz 1.1.0. No existing package changes (numpy 2.4.6 stays).
- The venv already has vtk 9.7.0, scikit-image 0.26.0, scipy 1.17.1 and pyvista 0.49.0, which week3 `skeleton.py` and `write_centerline_vtk` need.
- TotalSegmentator is not in the imagecasx venv, and `/work3/s254124/venvs/` holds only `imagecasx`.

### Inferences
- TotalSegmentator downloads its weights on first run. If GPU compute nodes have no internet, pre-download them on the login node into the totalseg venv's weights dir. Not verified.

### Gaps
- Whether compute nodes have outbound internet.

## 8. Mask spacing and skeletonize; pruning-calibration premise

### Takeaway
Native masks are anisotropic, about 0.32 to 0.40 mm in-plane by 0.5 mm slice, with LAS axcodes. More importantly, the plan's calibration premise looks wrong. Lee skeletons of the GT masks have no excess terminals: they have slightly fewer degree-1 voxels than the delivered centerlines have terminals. Calibrating spur pruning on GT masks will therefore select near-zero pruning, which will not transfer to CAS-Net masks, where spurs and fragments do appear.

### Cited Findings
- 10 train segmentations: spacing in-plane 0.318 to 0.395 mm, z 0.5 mm, axcodes ('L','A','S'). Some have 206 or 239 slices. Source: survey of `segmentations/*.coronary.nii.gz`.
- `skimage.morphology.skeletonize` (3D, Lee) on a cropped GT mask takes about 0.4 s per case. It is purely voxel-topological and ignores spacing.
- 11 val GT masks (`s3.py`, `s4.py`). The mask always has 2 components (26-connectivity), and so does the skeleton. Skeleton degree-1 voxels compared with delivered terminals (end + start points, both sides): 10/12, 8/10, 9/10, 11/11, 14/14, 13/14, 9/11, 10/12, 11/12, 11/13, 9/11. The skeleton is never above the delivered count.
- 8 CAS-Net test predictions (`s5.py`), same comparison: 19/13, 13/13, 13/11, 13/11, 10/12, 21/15, 10/11, 14/12. The excess comes largely from the extra fragments.

### Inferences
- The GT masks seem to have been curated so that their skeleton is clean, which is consistent with Bransby's manual spur removal. The "fewest spurious + missed" objective on GT masks is dominated by missed terminals, which pruning cannot fix.
- Calibrate pruning on predicted masks against delivered centerlines instead. That needs val predictions, and none exist; the inference config would need `--split val`. Alternatively, report pruning as a sensitivity analysis on the test predictions.
- Degree-1 voxel counts are a rough proxy, since voxel clusters at tips and junctions blur them. The direction of the result was consistent across all 11 GT cases, though.
- Anisotropy: the skeleton topology is fine. Spur lengths are measured in mm after `voxel_to_lps`, so the threshold is unaffected. The isotropic 0.5 mm cache (`segmentations_resampled/`) is an option, but it would then differ from how the delivered centerlines were made, which is not documented.

### Gaps
- Why the GT skeleton has fewer terminals: whether short terminal branches are lost to Lee thinning, or delivered start points sit beyond the mask. This was not resolved with a skan trace, because skan is not installed.

## 9. Naming clash: labelling package, train.py

### Takeaway
There is no clash.

### Cited Findings
- No `labelling/` directory or `labelling.py` module exists in the repo. `find -iname "*label*"` finds only `label_map.json` and the research_notes dir.
- `pyproject.toml:32`: `py-modules = ["train", "inference", "evaluate"]`. `python -m labelling.train` resolves the dotted name, so the root `train.py` does not shadow it.
- `pyproject.toml:34-43` packages.find includes only the framework packages. `bifurcation` and `labelling` are importable only with the repo root on `sys.path`, that is, `python -m` from the repo, as the existing jobs do via `source env.sh` in the repo. Running a script by path from elsewhere fails, as observed: ModuleNotFoundError for `bifurcation`.

### Gaps
- None.

## 10. CLAUDE.md convention check

### Takeaway
The plan is broadly compliant. There are four points of friction.

### Cited Findings and Inferences
- Outputs on /work3: compliant (`paths.RESULTS`).
- Per-case outputs and failure logs: compliant (per-case JSON, `failed.json`).
- Reproducibility: the TotalSegmentator separate venv is outside `pyproject`/`uv.lock`. Record the TotalSegmentator version and weights version in the per-case JSON or job log so the aorta masks stay reproducible.
- Minimal code: `_majority_label` is a private helper. Reusing it across packages is fine, but the 0 to 14 remap must be explicit in one place.
- Registries: `labelling/` is outside the framework, so the registry rule does not apply. No upstream file is edited. Compliant.
- Deviations: add to the deviation list (a) the side rule actually used, (b) the pruning calibration source, and (c) the radius measurement on native anisotropic masks.
- Stage 0's dependency step must not run `uv sync` (section 0).

### Gaps
- None.
