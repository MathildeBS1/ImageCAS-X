# CAS-Net -> CGPS (Herlev-Osterbro) inference and centerline-extraction pipeline

Scope note up front: CAS-Net is a fixed, frozen network trained only on ImageCAS-X
(`$ImageCAS_X_weights_path/cas_net.pt`, a bare `state_dict`, loaded strictly by
`BaseLumenModel.load_weights`). Nothing below retrains or fine-tunes it. Applying it to CGPS
means running the existing `inference.py` path with CGPS scans substituted for ImageCAS-X's
`volume_dir`/`volumes_resampled_dir`, and CGPS is explicitly out-of-distribution (different
scanner/protocol population) relative to the ImageCAS training cohort.

## How CAS-Net inference runs on a new scan (inference.py): tiling, TTA, resample-back, postprocess

### Takeaway
`inference.py`'s `predict()` -> `run_inference()` -> `patch_stitch_inference()` chain tiles the
0.5 mm-resampled volume into 128x160x160 patches at 50% overlap, blends overlapping logits with
an (unnormalised) Gaussian weight map, averages 4 forward passes (identity + 3 flip combinations
of the X and Y axes only, never Z), applies sigmoid, resamples the 2-channel probability map
linearly back onto the *original* scan's geometry, then runs the postprocessing pipeline
(`argmax_binarize` then `keep_components_larger_than_100_voxels`) to produce the final binary
mask written to `predictions/<scan_id>.nii.gz`. For CGPS this whole chain is unchanged: the only
thing that differs from an ImageCAS-X run is which files `cfg.data.volume_dir` /
`data.params.volumes_resampled_dir` point at, and that there is no GT mask to score against.

### Cited Findings
- Entry point and per-scan orchestration: `predict()` in `inference.py:360-538`. It builds
  `preprocessing`/`postprocessing`/`test_loader` (`inference.py:420-422`), builds the model and
  loads weights (`inference.py:424-425`, checkpoint resolved at `inference.py:398-406` to
  `<run_dir>/<method>_best.pt`, which for the delivered pretrained run is the symlink
  `cas_net_best.pt` -> `$ImageCAS_X_weights_path/cas_net.pt`), then loops scans
  (`inference.py:453`) calling `run_inference()` (`inference.py:474`).
- `run_inference()` (`inference.py:253-279`) builds the mirror-TTA combo list
  (`_mirror_axis_combos()`, `inference.py:130-135`, all 4 subsets of `_MIRROR_AXES = (2, 3)` i.e.
  tensor dims X, Y — `inference.py:127`) and dispatches to `_forward_full_volume` for CAS-Net
  (`input_type == "random_crop"`, `inference.py:141-152`), which calls
  `patch_stitch_inference()`.
- `patch_stitch_inference()` (`inference.py:70-122`): reads `patch_size` (`[128,160,160]` for
  CAS-Net, from `configs/cas_net.json:8-12` merged over `configs/pipeline.json`),
  `overlap = data.params.get("inference_overlap", 0.5)` (`inference.py:146`, value `0.5` set in
  `configs/pipeline.json:9`, i.e. 50% overlap), computes `stride = round(patch_size*(1-overlap))`
  (`inference.py:79`, so stride 64/80/80 voxels for a 128/160/160 patch at 0.5 overlap), and
  enumerates all tile starting positions via `axis_starts` (`inference.py:81-86`,
  `utils/tiling.py`). Tiles that run past the volume edge are zero-padded and cropped back
  (`inference.py:100-102`, `116-118`).
- Gaussian blending: `_gaussian_kernel()` (`inference.py:58-67`) builds an *unnormalised*
  per-axis Gaussian with `sigma = patch_size * sigma_scale` (nnU-Net's convention),
  `sigma_scale` from `data.params.inference_gaussian_sigma_scale`, value `0.125`
  (`configs/pipeline.json:10`). `weighting` defaults to `"gaussian"`
  (`data.params.inference_weighting`, also `"gaussian"` in `configs/pipeline.json:9`). Weighted
  logits are accumulated per voxel and divided by the accumulated weight at the end
  (`inference.py:118-121`) — this is why the kernel need not be pre-normalised.
- Mirror TTA: `_mirror_tta()` (`inference.py:230-250`) flips the volume over each of the 4 axis
  combos in `_mirror_axis_combos()`, forwards each, flips the resulting logits back, and averages
  (`accum / len(combos)`, `inference.py:249-250`). Z is never flipped — the module docstring
  states this matches the training-time `random_flip` augmentation axes
  (`configs/pipeline.json`'s `augmentation.params.random_flip.axes: [0, 1]`, i.e. X and Y only)
  and that a craniocaudal flip "is not anatomically valid" (`inference.py:26-28`). For CGPS this
  matters unchanged: whatever the scan's acquisition orientation, only X/Y mirroring is applied.
- Activation: `prob = torch.sigmoid(logits).numpy()` (`inference.py:500`), applied *before* any
  resampling so the continuous probability survives the resolution change rather than an
  already-binarised mask (comment at `inference.py:497-498`). CAS-Net has 2 independent sigmoid
  channels (`output_type: "mask_2ch_sigmoid"`, `configs/cas_net.json:5`) that do not sum to 1.
- Resample back to original geometry: `_resample_probs_to_original_space()`
  (`inference.py:294-312`) resamples per-channel probabilities with `sitk.sitkLinear` onto
  `ref_img`'s grid, where `ref_img` is the *original* CT volume's sitk header
  (`_load_reference_volume()`, `inference.py:282-291`, read straight from
  `cfg.data.volume_dir`/`volume_suffix`, i.e. the native, non-0.5mm file — for CGPS this is
  whatever native-resolution CGPS CT file is pointed at by that config field). This is done so
  binarisation happens "at full original resolution rather than on an already-thresholded mask,
  which would alias fine vessel boundaries" (`inference.py:296-297`).
- Postprocessing: `sample = postprocessing(sample); pred_orig = sample["mask"]`
  (`inference.py:530-531`), then `bio.save_mask(pred_orig, ref_img, pred_paths[i])`
  (`inference.py:533`). The postprocessing pipeline for CAS-Net (`configs/cas_net.json:32-38`,
  which *replaces* `pipeline.json`'s `["threshold", "keep_components_larger_than_100_voxels"]`
  list wholesale — CLAUDE.md's "lists replace, not merge" gotcha) is exactly:
  1. `ArgmaxBinarize` (`postprocessing/steps.py:46-55`): `np.argmax(pred, axis=0)` over the
     2-channel probability map — correct for CAS-Net specifically because the two channels are
     independent sigmoids, not a single softmax that sums to 1 (docstring at
     `postprocessing/steps.py:47-49`; this is *not* the `Threshold` step, which would be wrong
     here — `postprocessing/steps.py:6-20`).
  2. `KeepComponentsLargerThan100Voxels` (`postprocessing/steps.py:23-43`): 26-connected
     `scipy.ndimage.label`, keeps every component with >= `min_size` voxels (default 100,
     `postprocessing/steps.py:32`); this is size-based rather than keep-top-N specifically so
     that both a left and a right coronary tree survive as separate components
     (`postprocessing/steps.py:25-26`).
  - Step registry and config-driven assembly: `postprocessing/pipeline.py:6-34`.
- The `-r/--results-dir` CLI convention and the resume/overwrite/`--save-probs`/`--split`/
  `--computational_analysis` flags are documented in `inference.py:590-621`. For a CGPS run, the
  config's `data.*_dir` fields would point at CGPS volume files and a fresh/no-GT-required
  `--split` (evaluate.py, not inference.py, is what needs GT, per its own docstring at
  `inference.py:11-12`: "evaluate.py never loads a model, so externally-produced predictions can
  be dropped into predictions/ and scored without running this" — implying inference-only
  cohorts like CGPS are a supported mode of use as long as evaluate.py is simply not run, or run
  with metrics that need no GT).
- Model loading is strict: `BaseLumenModel.load_weights` (referenced in CLAUDE.md, confirmed by
  the checkpoint-must-stay-bare-state_dict gotcha) does a strict `load_state_dict`, so the
  frozen ImageCAS-X-trained weights are loaded byte-for-byte with no CGPS-specific parameters.

### Inferences
- Running CAS-Net on CGPS requires no code change to `inference.py` itself: only the method
  config's `data` block (volume directory/suffix, and whichever `preprocessing.steps`/cache dirs
  apply) needs to point at CGPS data, and the checkpoint must remain the delivered
  `cas_net_best.pt`/`cas_net.pt`, never a path to a CGPS-finetuned file (per CLAUDE.md's
  "never put a checkpoint path in `configs/cas_net.json`" gotcha, which exists specifically to
  prevent an accidental fine-tune when reusing this same code path for training).
- Because postprocessing keeps *every* component >= 100 voxels rather than exactly two, an OOD
  scan with more noise-driven false-positive fragments than ImageCAS-X scans could retain more
  spurious small trees than on the training distribution; this is the same axis `keep2`/Qiu
  reconnection was built to address (see the dedicated section below).

### Gaps
- No CGPS-specific inference config exists in the repo yet; the exact `data.volume_dir`/
  `volume_suffix`/resampled-cache paths CGPS would use are not yet decided anywhere I found.

## The two distinct "0.5" concepts: voxel-spacing resampling vs. centerline-coordinate smoothing

### Takeaway
"0.5 mm" appears in this repo in two structurally unrelated places that happen to share a
number: (1) `Resample`'s `target_spacing=0.5` resamples the *volume/mask voxel grid* to 0.5 mm
isotropic spacing before/for the CNN, executed offline once and cached; (2) a Gaussian smoothing
of *centerline point coordinates* along arc length with `sigma_mm=0.5` over a 5-vertex window,
applied when building a tree-ready centerline from a skeletonized mask, to match how the
delivered GT centerlines were themselves produced. These are unrelated pipeline stages
operating on different objects (dense voxel grid vs. sparse 1D curve) and there is no code path
in which one determines or substitutes for the other.

### Cited Findings
- Voxel-grid resampling: `preprocessing/steps.py`'s `Resample` class (`preprocessing/steps.py:6-49`)
  resamples the sitk volume to `target_spacing` mm isotropic with `sitkLinear` interpolation for
  the image and `sitkNearestNeighbor` for the mask (`preprocessing/steps.py:29,43`).
  `configs/pipeline.json` sets `preprocessing.params.resample.target_spacing = 0.5`. This is run
  offline, once, by `utils/offline_resample_images_to_disk.py` (`utils/offline_resample_images_to_disk.py:1-13,
  44-65`) to build the `volumes_resampled/`/`segmentations_resampled/` `.npy` caches (already
  built for the 800 curated ImageCAS-X scans, per CLAUDE.md's dataset section).
- `base_dataset.py:_load_volume`/`_load_gt_mask` (`dataloading/base_dataset.py:68-95`) read
  straight from that cache via `np.load(..., mmap_mode="r")` whenever `"resample"` is present in
  `config.preprocessing.steps` (`dataloading/base_dataset.py:29`), and `_run_preprocessing`
  (`dataloading/base_dataset.py:127-146`) explicitly *skips* the `Resample` step class at
  runtime in that mode (`skip_types += (Resample,)`, `dataloading/base_dataset.py:135`) — the
  resample is baked into the cache, not repeated per sample. This is a description of a
  preprocessing decision on the *volume the network sees*; it has nothing to do with any curve.
- Centerline-coordinate smoothing: `topology/skeleton.py`'s module docstring states explicitly
  that "the delivered GT centerlines are a skeleton of the corrected mask, Gaussian smoothed
  (sigma = 0.5 mm, 5-vertex window)... (Bransby et al. 2026, Methods)" and that the module's job
  is to "reproduce that on a predicted mask." The `smooth()` function
  (`topology/skeleton.py:53-64`, exact signature `smooth(points, lines, sigma_mm: float = 0.5,
  window: int = 5)`) Gaussian-smooths each polyline's *interior* points over a window of vertices
  local to arc-length distance (`w = np.exp(-0.5 * ((arc[k] - arc[j]) / sigma_mm) ** 2)`,
  `topology/skeleton.py:62`), explicitly leaving shared junction and end points unmoved
  (`half = window // 2`, loop only over `range(1, len(line) - 1)`, `topology/skeleton.py:59-63`).
  This is a smoothing of a small set of 3D point *coordinates* along a already-extracted 1D
  curve — a completely different array, operation, and purpose from the volumetric resample
  above, and the coincidence that both use "0.5" is not derived from a shared constant anywhere
  in the code (they are independent literals in two different files: `configs/pipeline.json`'s
  `target_spacing` and `topology/skeleton.py`'s `sigma_mm` default).
- Important caveat on where this smoothing code currently lives: `topology/skeleton.py` is
  **not present on the current checked-out branch** (`tree-extraction_essential`). It exists on
  the `week3` branch (confirmed via `git show week3:topology/skeleton.py`, full contents read).
  The commit that removed it from the current branch, `4aab47a` ("Trim to tree-building +
  angle/tortuosity feature extraction"), states explicitly in its message that it dropped "The
  predicted-mask centerline pipeline that feeds Herlev-Osterbro prep (topology/skeleton.py,
  scripts/build_predicted_centerlines.py, scripts/validate_extraction.py) — still an open problem
  per thesis/week3/coronary_tree_graph.tex, not part of this objective." So as of the currently
  committed `tree-extraction_essential` branch, there is no committed mask -> centerline
  extraction path for CGPS; it must be recovered from `week3` (or reimplemented) before it can be
  run on CGPS predictions.
- Separately, `topology/tortuosity.py` (current branch, present) has its *own* Gaussian smoothing
  stage, with different defaults, applied later in the pipeline for tortuosity feature
  computation, not centerline construction: `RESAMPLE_MM = 0.25`, `DEFAULT_SIGMA_MM = 1.0`
  (`topology/tortuosity.py:30-31`), used via `gaussian_filter1d(curve, sigma_mm / step_mm, axis=0,
  mode="nearest")` (`topology/tortuosity.py:128,153`) on an arc-length-*resampled* (not the raw
  skeletonized) point set. This is a third, distinct smoothing operation: it resamples to a
  uniform 0.25 mm arc-length grid first (`_resample()`, `topology/tortuosity.py:100-110`) then
  applies `scipy.ndimage.gaussian_filter1d` with `sigma_mm=1.0` (not 0.5) as a preprocessing step
  before computing curvature/torsion/SOAM etc. It should not be confused with either the CNN
  voxel-resample or the skeleton-smoothing step above; if "0.5 smoothing" in a CGPS planning
  context means this stage, note the actual current default here is `sigma_mm=1.0`, not 0.5 —
  0.5 mm is only the *resample step size* used inside `_resample()`... no: re-checking,
  `RESAMPLE_MM = 0.25` is the resample step, not 0.5. **0.5 mm smoothing as a concrete, currently
  code-verified parameter matches only `topology/skeleton.py`'s `smooth(sigma_mm=0.5, window=5)`,
  not `topology/tortuosity.py`'s stage (sigma 1.0 mm, resample 0.25 mm).**

### Inferences
- If "0.5 mm smoothing like in this repo" is meant in a CGPS write-up, the precise, code-grounded
  referent is `topology/skeleton.py:smooth()`'s Gaussian arc-length smoothing with
  `sigma_mm=0.5`, `window=5` vertices, applied to skeleton point coordinates after
  skeletonization and before the mask -> centerline result is fed into `graph.build_tree`. It is
  categorically not the CAS-Net input's 0.5 mm voxel-grid resample.
- Because `topology/skeleton.py` currently exists only on the `week3` branch, any CGPS plan that
  cites "the existing 0.5mm smoothing" needs to first pull that file back (e.g.
  `git show week3:topology/skeleton.py > topology/skeleton.py` plus its `postprocessing/qiu/skeleton.py`
  counterpart if reconnection is also wanted) rather than assuming it is already active on
  whichever branch CGPS work happens on.

### Gaps
- No document in `docs_thesis/` or elsewhere states a chosen sigma/window for CGPS specifically;
  the 0.5 mm/5-vertex values are inherited unmodified from matching the *ImageCAS-X GT delivery's*
  own construction (Bransby et al. 2026 Methods), not derived for or validated on CGPS geometry.

## Centerline extraction from a binary mask: skeletonization algorithm and tree building

### Takeaway
Two separate, non-overlapping code paths exist for "mask -> centerline": (1) `topology/graph.py`
on the current branch builds a *rooted tree* structure from an **already-existing** centerline
point/polyline set (VTK file, either the delivered GT or a predicted centerline dropped into a
directory with the same naming) — it does no skeletonization itself; (2) `topology/skeleton.py`
(week3 branch only) is the actual mask -> skeleton -> centerline-points step, using
`skimage.morphology.skeletonize` (Lee et al. 1994, 3D thinning) traced with the `skan` package,
followed by the 0.5mm/5-vertex Gaussian smoothing described above, then handed to
`topology/graph.py:build_tree` for the rooted-tree structure. A third, independent skeletonizer
(`postprocessing/qiu/skeleton.py`, also week3-only) exists purely to support Qiu-style stage-2
fragment reconnection and is not used for the final centerline product.

### Cited Findings
- `topology/graph.py:build_tree()` (`topology/graph.py:367-484`, current branch) takes an
  `io.Centerline` object (i.e. already-loaded VTK points + polylines + per-point
  start/end/branch flags) and: computes point degree from polyline endpoints
  (`topology/graph.py:373-376`), identifies junctions as points with degree != 2 or flagged as a
  start point (`topology/graph.py:380`), merges polylines through degree-2 pass-through points
  into maximal junction-to-junction chains via `_merge_chains()`
  (`topology/graph.py:300-334`), finds connected components and picks a root per component
  (preferring an existing start/ostium point, else the point nearest the rest of the tree,
  `topology/graph.py:393-415`), then does a BFS from each root orienting every chain
  proximal -> distal into `Segment`s (`topology/graph.py:417-449`), dropping any edge that would
  close a cycle into `chords` (`topology/graph.py:430-432,450-451`). It does **not** read a mask
  or run any skeletonization — its input is always a point cloud with pre-existing topology
  markers, from `io.load_centerline()` (`topology/io.py:101-125`, reads a VTK file via `pyvista`,
  taking `branch_points`/`end_points`/`start_points`/`segment_label` arrays straight off the
  file's own point-data arrays).
- `topology/io.py:load_centerline(case_id, side, root=None)` (`topology/io.py:101-125`) explicitly
  supports `root` pointing at "a directory of files in the same naming" as the GT delivery for
  predicted centerlines (`topology/io.py:94-98`, `centerline_file()`), meaning
  `topology/graph.py`'s tree builder is designed to be reused on a predicted centerline **once
  one has been produced and written to VTK in the same layout** — but producing that VTK file
  from a mask is exactly the step `topology/skeleton.py` performs, and that file is not on the
  current branch.
- `topology/skeleton.py` (week3 branch; full contents read via `git show week3:topology/skeleton.py`):
  - `skeleton_graph(mask, affine)` (lines ~30-42): crops the mask to its bounding box + 1-voxel
    margin, runs `skimage.morphology.skeletonize(mask_crop)` (binary 3D thinning; the module
    docstring calls this "Lee et al. 1994 — the method ImageCAS-X cites"), wraps the boolean
    skeleton in `skan.Skeleton`, and calls `sk.path(i)` for each of `sk.n_paths` to get ordered
    point-index polylines; converts voxel indices to LPS mm via `coords.voxel_to_lps`.
  - `smooth(points, lines, sigma_mm=0.5, window=5)`: the arc-length Gaussian smoothing described
    above.
  - `_degree()`/`_components()`: same style of degree/union-find helpers as `topology/graph.py`,
    used here just to find connected pieces of the raw skeleton before assigning a left/right
    side.
  - `oracle_labels(points, gt)`: assigns each skeleton point the label of the *nearest GT-labelled
    voxel* — explicitly called "oracle" because it uses the GT mask's per-segment labels, which
    would not exist for a real deployment (CGPS) case. The docstring states plainly: "Herlev-
    Osterbro needs real [providers] (an aorta mask, multi-class labels)" — i.e. this labelling
    approach as written is not directly usable on CGPS without a real, non-oracle label source.
  - `centerlines_from_mask(case_id, mask, affine, gt, gt_centerlines)`: the top-level function —
    builds the raw skeleton graph, smooths it, labels points (currently oracle-only), splits into
    left/right by majority label per connected component (falling back to nearest-GT-tree
    distance for all-"Other" components), and for each side finds start/ostium points by matching
    predicted degree-1 endpoints to GT ostium locations within `OSTIUM_MAX_MM = 10.0` mm — this
    ostium-matching is also GT-dependent ("oracle ostium... the predicted end point nearest the
    GT start point").
  - Output is wrapped into an `io.Centerline` object per side and can be written to VTK via
    `write_centerline_vtk()`, in the same file layout the delivered GT uses, so it round-trips
    into `topology/graph.py:build_tree()` unchanged.
- Separate, Qiu-specific skeletonizer: `postprocessing/qiu/skeleton.py` (week3 branch; full
  contents read) operates directly on 0.5mm-grid integer voxel indices (not LPS mm), also via
  `skimage.morphology.skeletonize` ("Lee's 3D thinning"), but its purpose is narrower: split a
  *prediction component* into branches (`_trace_branches()`) to find degree-1 "opening points"
  (candidate tips for stage-2 reconnection joins) with an outward tip direction
  (`_tip_direction()`) and a spur-pruning step (`_prune_spurs()`, drops short terminal branches
  under `min_len` voxels that Lee thinning creates as surface-bump artefacts). This module feeds
  `postprocessing/qiu/reconnect.py`'s fragment-joining logic, not the final analysis centerline;
  it has no Gaussian coordinate smoothing at all (only spur pruning).
- `utils/metrics.py` has a third, evaluation-only skeletonization: `compute_centerline_metrics()`
  (`utils/metrics.py:146-178`) and `cl_dice()` (`utils/metrics.py:71-91`) call
  `skimage.morphology.skeletonize(pred)` directly on the binary prediction mask (no smoothing,
  no tree-building, no left/right split) purely to get voxel-level skeleton points for computing
  `centerline_md`/`centerline_hd95`/`cl_dice` against the GT centerline — a metrics-only skeleton,
  disconnected from the tree/vessel-feature pipeline entirely.

### Inferences
- For a CGPS deployment pipeline (mask -> usable centerline tree with named vessels, e.g. for
  tortuosity/angle feature extraction downstream), the code that actually does this
  (`topology/skeleton.py`) needs its "oracle" providers (labelling, ostium-matching) replaced
  with real, non-GT-dependent providers before it is usable on CGPS, exactly as its own docstring
  flags ("Herlev-Osterbro needs real ones"). This is explicitly an open problem, not solved code.
- The three skeletonizers in this repo (`topology/skeleton.py`, `postprocessing/qiu/skeleton.py`,
  `utils/metrics.py`'s inline use) are independent implementations for three different purposes
  (final centerline construction, reconnection candidate-finding, evaluation-only distance
  metrics) and should not be conflated; none of them currently need each other.

### Gaps
- No non-oracle ostium/labelling provider exists in the repo for CGPS (no aorta mask, no
  multi-class vessel labelling model) — `topology/skeleton.py`'s own docstring names this as the
  missing piece, and no code addressing it was found anywhere in git history across the branches
  checked (`main`, `tree-extraction`, `week1`-`week3`, `clean_version`, `thesis-setup`,
  `tortuosity_focus`, `tree-extraction_essential`).
- `scripts/build_predicted_centerlines.py` and `scripts/validate_extraction.py`, named in commit
  `4aab47a`'s message as the driver/validation scripts around `topology/skeleton.py`, were not
  read in full for this note (out of the explicit scope given — mask-extraction algorithm and
  smoothing were the ask); their presence confirms a script-level entry point existed on `week3`
  but their exact CLI/behaviour is unverified here.

## Qiu et al. stage-2 reconnection / "keep2" post-processing: implementation status and calibration

### Takeaway
A full Qiu-et-al.-2025-style stage-2 reconnection implementation (candidate joins, a learned
DTW-walk-based "trust" classifier P, threshold-based accept/reject, ADF stationarity penalty) was
built and evaluated on the full ImageCAS-X test split on 2026-09-14/15, with a "keep2" (delete-
all-fragments-except-the-two-largest) baseline for comparison — but **this code has since been
deliberately removed from the current branch** (`tree-extraction_essential`) as out of scope for
the tree-building/angle-feature objective that branch was trimmed to. It survives only on the
`week3` branch (and its ancestors). Calibration was done, and it found the classifier's
discrimination weak (test rec_acc ~0.50) even though the join-then-reject mechanism still
improved topology (Betti-0) more cheaply on Dice than plain deletion.

### Cited Findings
- Source location (week3 branch, confirmed via `git ls-tree -r week3` and `git show`):
  `postprocessing/qiu/__init__.py`, `classifier.py`, `reconnect.py`, `skeleton.py`, `walk.py`,
  documented in `docs_thesis/qiu_reconnection.md` (215 lines, deviations D1-D12 from the paper,
  per the removal commit's diffstat) and driven by `jobs/qiu_reconnect.sh` /
  `jobs/train_qiu_classifier.sh` / `jobs/sweep_postprocessing.sh`, with configs
  `configs/cas_net_qiu.json`, `configs/cas_net_qiu_noremove.json`, `configs/cas_net_keep2.json`
  (all week3-only; removed by commit `4aab47a` on the current branch, per that commit's diffstat
  which lists all of the above as deletions).
- Current-branch reality, verified directly: `postprocessing/qiu/` on disk today
  (`tree-extraction_essential`) contains **only compiled `.pyc` files** under `__pycache__/`
  (`classifier.cpython-311.pyc`, `__init__.cpython-311.pyc`, `reconnect.cpython-311.pyc`,
  `skeleton.cpython-311.pyc`, `walk.cpython-311.pyc`) and zero `.py` source files — i.e. it was
  run recently enough on this machine to leave bytecode, but the source is gone from the working
  tree and from every commit reachable on this branch. `git log --all --oneline -- postprocessing/qiu`
  shows it existed as of commits `2d88dff` ("changes") and was removed by `4aab47a` ("Trim to
  tree-building + angle/tortuosity feature extraction").
- `postprocessing/qiu/reconnect.py` (read in full from `week3` via `git show week3:...`):
  `ReconnectParams` dataclass (`reconnect.py`, lines ~33-58) with `mode: "qiu" | "keep_largest"`,
  `n_main_components=2` ("the two largest connected components" — this is the literal "keep2"
  concept, available as a mode inside the same params object rather than a separate script),
  `grid_mm=0.5` (operates on the same 0.5mm cache grid CAS-Net predicts on), distance/angle
  thresholds for three join-candidate types (`type1_max_dist_mm=24.0`, `type2_max_dist_mm=32.0`,
  `type3_short/long_*`), a DTW-style walk (`omega=5.0`, `walk.py`), and stage-3 evaluation
  parameters `eval_threshold: float = 1.0` ("paper: 'a predefined threshold (e.g., 1)'") and
  `use_adf: bool = True` (Augmented Dickey-Fuller stationarity test on the walked path,
  `adf_pvalue()` in `reconnect.py` calling `statsmodels.tsa.stattools.adfuller`). The module
  docstring states units were converted from the paper's voxel units at "a nominal 0.4 mm/voxel"
  since the paper's own dataset (ASOCA/PDSCA) has in-plane spacing 0.3-0.4mm, an explicit,
  documented deviation.
- Calibration numbers (from project memory `project_qiu_reconnection.md`, dated 2026-09-14/15,
  which states these were computed on this machine but is 12 days old and unverifiable against
  current code since the source is gone — treat as historical record, not re-derivable right
  now):
  - A real centerline-probability classifier P was trained (`qiu_classifier_29395891`): val AUC
    0.977, mean P = 0.74 on true centerline vs 0.11 off-centerline vs 0.006 outside the mask.
  - T (i.e. `eval_threshold`) was calibrated on the **val** split only (80 scans, 152 fragments,
    79/152 = 52% true vessel by GT overlap — matching the test-split rate of 53.9% closely). Best
    setting over a grid: **`eval_threshold=1.0, use_adf=false`** — RecAcc 0.618, RecSen 0.711,
    RecSpe 0.526 — beating both the paper's literal "T=1 + ADF" (RecAcc 0.533) and every
    ADF-enabled setting tried (best 0.572 at threshold 0.75). I.e. disabling ADF outperformed the
    paper's own configuration in this reimplementation.
  - Full test-split comparison (160 scans, jobs `29405686` qiu / `29405709` qiu_noremove, scored
    with `scripts/compare_runs.py`, also week3-only) against `cas_net_pretrained_keep2` and raw
    `cas_net_pretrained`: at T=1.0 on 293 test fragments (base delete-all-fragments accuracy
    0.461), `qiu`'s reconnect/reject decision itself scored rec_acc **0.502**, rec_sen 0.566,
    rec_spe 0.439 — "barely above the base rate despite val AUC 0.977" (memory's own wording).
  - Paired deltas vs. raw baseline (better/worse relative to `cas_net_pretrained`):
    `betti_error_1`: keep2 -1.831 (best, ties qiu at -1.831), qiu_noremove -1.081;
    `dice`: keep2 -0.012, qiu -0.005, qiu_noremove -0.002;
    `cl_dice`: keep2 -0.017, qiu -0.006, qiu_noremove -0.002;
    `centerline_hd95`: keep2 +4.64, qiu +1.98, qiu_noremove +0.33;
    `local_dice`: keep2 -0.040, qiu -0.011, qiu_noremove **+0.002 (only method that improved it)**.
  - Cohort fragment breakdown (computed from `cas_net_pretrained_keep2`'s
    `reconnection_logs/*.json`, 160 test scans, 293 removed fragments): 53.9% have GT overlap
    fraction >= 0.5 (median 0.886 among those), only 44.7% are fully spurious (GT fraction == 0).
    Mean extra components per scan beyond the main two trees: 1.83.
  - Memory's own conclusion: "reconnect-then-reject dominates plain deletion on the
    accuracy/topology trade-off, but the improvement is coming mostly from 'reattach real
    fragments' rather than from P/T correctly discriminating real vs spurious (rec_acc ~0.50 says
    that discrimination is weak)." I.e. the mechanism helps despite, not because of, accurate
    per-fragment classification.

### Inferences
- Because this code is currently absent from the branch this research was run on, any CGPS plan
  that wants to reuse Qiu-style reconnection needs an explicit recovery step first: e.g.
  `git show week3:postprocessing/qiu/<file>.py > postprocessing/qiu/<file>.py` for each of
  `__init__.py`, `classifier.py`, `reconnect.py`, `skeleton.py`, `walk.py`, plus
  `docs_thesis/qiu_reconnection.md` for the deviation log, before it can be run at all.
- The T=1.0/no-ADF calibration was done on ImageCAS-X's own val split, never on any CGPS data
  (CGPS has no GT to calibrate against in the first place, since it has no manual segmentation).
  Carrying that calibration to CGPS predictions is an extrapolation across an OOD gap on top of
  an already-weak classifier (rec_acc ~0.50 on ImageCAS-X's own test split); there is no
  calibration number for CGPS anywhere, and none can be produced by the same method (val-split
  RecAcc-maximisation) without GT.

### Gaps
- No CGPS-specific reconnection run, calibration, or even a plan for how T would be chosen
  without GT was found anywhere in the repo, docs_thesis/, or memory.
- The exact contents of `docs_thesis/qiu_reconnection.md` (D1-D12 deviation list) were not read
  in full for this note (it too is week3-only and not on the current branch); only its existence
  and the memory summary above were confirmed. A CGPS plan that leans on Qiu deviations should
  pull that file from `week3` and read it directly rather than relying on this summary.

## Quality-control mechanisms usable on CGPS predictions without ground truth

### Takeaway
Every metric in `evaluate.py`/`utils/metrics.py` that appears in `configs/pipeline.json`'s
`evaluation.metrics` list needs a GT mask or GT centerline and is therefore unusable as-is on
CGPS. What remains usable without GT are: (1) the two committed, GT-free postprocessing filters
that already run inside `inference.py` itself (component-count/size filtering), (2) qualitative
visual inspection via `utils/display_in_slicer.py`'s "segments" mode (loads a mask + centerlines
with no GT dependency), and (3) `inference.py --computational_analysis`'s parameter-count/timing/
memory report (a sanity check that the model ran as expected, not a correctness check). The
"oracle" QC signals inside `topology/skeleton.py` (ostium-match distance, left/right label purity
per component) are GT-dependent and therefore not usable on CGPS in their current form.

### Cited Findings
- `KeepComponentsLargerThan100Voxels` (`postprocessing/steps.py:23-43`) already runs on every
  CAS-Net prediction, GT or not, as part of the postprocessing chain in `inference.py:530`. Its
  component count and per-component size, before filtering, is available as a free-standing
  sanity signal: an OOD scan producing many more sub-100-voxel components than typical
  ImageCAS-X scans would be a visible red flag even without any GT to score against (this would
  need a small script change to *log* pre-filter component counts, which does not exist yet —
  currently the step only filters, it does not report the counts it dropped).
- `utils/display_in_slicer.py`'s `"segments"` mode (`utils/display_in_slicer.py:102-131`,
  invoked from `main()` at `utils/display_in_slicer.py:309-318`) loads only a mask + left/right
  centerline VTKs with **no GT/prediction comparison and no Dice computation** — this is directly
  usable for eyeballing a CGPS prediction's mask and (once a predicted centerline VTK exists, per
  the gap above) its centerline tree in 3D, exactly as it is used for ImageCAS-X scans. Its
  `"compare"` mode (`utils/display_in_slicer.py:267-306`), by contrast, is built around a GT
  entry (`GT_LABEL`, always loaded first at `utils/display_in_slicer.py:280`) and per-method Dice
  read from `<run>_results.json` (`run_dice()`, `utils/display_in_slicer.py:248-264`) — not
  usable for CGPS without either fabricating a GT-shaped comparator or modifying the script to
  drop the GT/Dice assumptions.
- `inference.py --computational_analysis` (`inference.py:432-438,611-618`) times a fixed 1
  warm-up + 10 measured scans and reports parameter count, per-scan inference time, and peak GPU
  memory to `computational_cost.json` (`_report_computational_cost()`,
  `inference.py:541-587`) — a run-health check (did it crash, does it use plausible memory/time)
  rather than an output-quality check, but free to run on any cohort including CGPS since it
  needs no GT.
- `evaluate.py`'s Betti-number/Dice/HD95/cl_dice/centerline_md/volume-difference metrics
  (`configs/pipeline.json`'s `evaluation.metrics` list, `utils/metrics.py`'s `METRIC_REGISTRY`)
  all take a `gt` mask or `gt_centerline_pts` argument as a hard requirement (every function
  signature in `utils/metrics.py` takes `(pred, gt, ...)` and several raise `ValueError` if `gt`
  is empty, e.g. `hausdorff_95` at `utils/metrics.py:56-57`, `cl_dice` at
  `utils/metrics.py:80-81`) — none of these run on CGPS without a GT mask/centerline, which CGPS
  by definition does not have.
- `topology/skeleton.py`'s `centerlines_from_mask()` (week3-only) already produces `notes`
  (a list of strings) flagging exactly the kind of QC signal that *would* generalize to CGPS if
  the function's oracle dependencies were replaced: e.g. "`{side}: no predicted end point to
  place the ostium on`" and "`{side}: nearest predicted end is {d:.1f} mm from the GT ostium;
  none set`" and "component of {n} points has {left} left / {right} right labels" (mixed-label
  components) — but as written these compare against a GT ostium/GT labels, so they are not
  directly usable on CGPS until non-oracle providers replace the GT-based ones.
- `evaluate.py:310` references "skeletons and Betti numbers are intrinsic" in the context of a
  box-crop discussion (not fully read in depth here, out of the given scope, but confirms Betti
  numbers are computed on the prediction mask alone in principle — `_betti_numbers()` in
  `utils/metrics.py:4-17` indeed takes a single mask, not a GT-pred pair, at the primitive level).
  However the metric functions exposed and used, `betti_error_1`/`betti_error_2`
  (`utils/metrics.py:20-34`), are *errors* — `abs(betti(pred) - betti(gt))` — so they still need
  GT as currently wired into `evaluate.py`. The underlying `_betti_numbers(mask)` primitive
  itself, called on the CGPS prediction alone, would still be a usable GT-free QC number (raw b0
  = connected-component count, b1 = loop count) — it is just not currently exposed as a
  standalone metric outside the paired-error framing.

### Inferences
- The cheapest immediately-usable QC on CGPS without any code change: run `_betti_numbers()`
  (or equivalently `scipy.ndimage.label` + `skimage.measure.euler_number`, exactly as
  `utils/metrics.py:4-17` does) on each CGPS prediction mask alone and flag scans with
  unusually many components (should ideally be 2, one per coronary tree, matching what
  `keep_components_larger_than_100_voxels` is designed to leave behind) or a nonzero b1 (a loop,
  anatomically implausible for a coronary tree and a sign of a segmentation artefact).
- A practical CGPS QC pass with existing tooling: for a sample of CGPS scans, load the CAS-Net
  prediction mask (and, once produced, its centerline) in `utils/display_in_slicer.py`'s
  `"segments"` mode (with `MASK_DIR` pointed at the prediction directory rather than the GT
  `segmentations/` dir, and `CENTERLINES_DIR` at wherever a predicted centerline VTK would be
  written) for visual review — this needs only a config-value change in that script, not new
  code.

### Gaps
- No automated, scripted QC report (beyond the two ad hoc primitives above) exists in the repo
  for a no-GT cohort; everything in `evaluate.py` assumes GT is available.
- Whether/how `topology/skeleton.py`'s oracle providers would be replaced with real ones for
  CGPS (a real aorta/ostium detector, a real per-voxel vessel-name classifier) is, per that
  module's own docstring, an explicitly open problem with no committed solution anywhere in the
  branches checked.

## docs_thesis/cas_net_walkthrough.md and CLAUDE.thesis.md: additional pipeline/OOD detail

### Takeaway
`docs_thesis/cas_net_walkthrough.md` (607 lines, read via targeted greps and the surrounding
context for the tiling/postprocessing/resample sections) documents exactly the same pipeline
parameters found directly in the code above (50% overlap, Gaussian sigma_scale 0.125,
argmax_binarize + keep_components_larger_than_100_voxels, 0.5mm resample cache, mirror TTA over
X/Y only) with no discrepancy found. It contains no CGPS/Herlev-Osterbro/OOD-specific section.
`CLAUDE.thesis.md` does not exist on disk in this project (`ls` returned "No such file or
directory" at the project root), despite being referenced in `CLAUDE.md` as the file holding
CGPS/Herlev-Osterbro dataset context — it is gitignored and evidently not present on this
machine/checkout, so none of that context could be read for this note.

### Cited Findings
- `docs_thesis/cas_net_walkthrough.md:79-85` table: `input: random_crop, patch [128,160,160],
  min_fg_fraction 0.5`; `preprocessing: resample (0.5 mm), normalise_to_range (HU [-200,1000] ->
  [0,1])`; `postprocessing: argmax_binarize, keep_components_larger_than_100_voxels` — matches
  `configs/cas_net.json`/`configs/pipeline.json` exactly.
- `docs_thesis/cas_net_walkthrough.md:281-296`: "tile the volume with 50% overlap (`stride =
  round(128 x 0.5)` etc.)"; "blend with a Gaussian weight map, `sigma_scale = 0.125` (nnU-Net's
  value)"; "mirror test-time augmentation over X and Y only"; "resample the probabilities back to
  the original scan geometry, per channel, linearly" — all consistent with the direct code
  reading above.
- `docs_thesis/cas_net_walkthrough.md:316-325` explains the `argmax_binarize`-not-`threshold`
  choice and the `keep_components_larger_than_100_voxels` size-based rationale in the same terms
  as the code comments.
- Grep for `CGPS|Herlev|OOD|out-of-distribution|external` in the walkthrough returns exactly one
  hit, at line 26, which is about TotalSegmentator (an external *tool*, not the CGPS dataset) —
  i.e. no CGPS-specific content exists in this document.
- `ls -la CLAUDE.thesis.md` at the project root returned "No such file or directory" (exit code
  2). Per `CLAUDE.md`'s own text, this file is "gitignored, machine-local" and holds "dataset
  anatomy, label scheme, centerline topology, the topology/ rebuild, CGPS, the research gap" —
  none of that could be consulted for this note since the file is absent from this checkout.

### Inferences
- Everything this note reports about the CAS-Net inference/postprocessing pipeline is corroborated
  by two independent sources (the code itself and the walkthrough doc), which is unusual to be
  able to state cleanly and should be reasonably trustworthy as a description of current behaviour.
- Any CGPS-specific dataset/label/topology context that might otherwise have been in
  `CLAUDE.thesis.md` is not recoverable from this checkout; if that file exists elsewhere (a
  different machine, or restorable from a private note), it should be consulted directly rather
  than assuming this note's silence on CGPS dataset specifics means no such context exists.

### Gaps
- Content of `CLAUDE.thesis.md` is entirely unknown from this environment.
- Whether `docs_thesis/qiu_reconnection.md`'s D1-D12 deviation list contains any statement
  relevant to OOD/CGPS applicability of the reconnection classifier was not checked, since that
  file is also absent from the current checkout (week3-only, per the section above).
