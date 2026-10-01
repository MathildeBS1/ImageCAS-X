# Repo readiness: what the five reports recommend vs what ImageCAS-X can deliver now

Audit date 2026-09-26, branch `tree-extraction_essential` at HEAD `d306d36`, login node `hpclogin1`. All checks were read-only (ls, git, quick imports, reading CSV headers of scratch outputs). No Disease column, no val/test data were opened. "Source" links point at local files; `file://` paths under `/tmp/...` are session scratchpads on the login node's local disk.

## Q1. For each major recommendation: committed code, scratch-only code, or nothing?

### Takeaway
Almost every number the reports rely on comes from scratch code under `/tmp` on one login node. The committed code (`topology/`, `tortuosity/`) covers tree building, the fitcore3-style bifurcation angle, the Finet and radius ratios, and an older Frenet-style tortuosity panel. It does not cover the recommended 5 mm chord κ_a with the reflected-end smoothing, κ·r, sliding-window TI(Δ), SRVF registration, the node-graph or tokeniser, or the ICC/reliability protocol. κ·r in particular has no traceable computation anywhere, even in scratch.

### Cited Findings
Status per recommendation (C = committed at HEAD, S = staged or untracked in working tree, T = `/tmp` scratch only, N = nothing found):

- **Tree construction with anatomical labels (prerequisite for everything regional).** C: `topology/graph.py` (`build_tree`, `Vessel`, `shaft_window`, `outgoing_direction`, 494 lines) was cherry-picked in commit 3ae9667. It depends on `topology/io.py` and `paths.py`, which are only *staged* (`A` in git status), not committed. It also needs `docs_thesis/label_map.json`, which is absent. — [git status / `git ls-tree -r HEAD`](file:///zhome/e2/6/224426/project/ImageCAS-X/topology/graph.py); [commit 3ae9667 message: "without its supporting io/paths/coords/viz modules"](file:///zhome/e2/6/224426/project/ImageCAS-X/topology/graph.py)
- **5 mm chord curvature κ_a (σ = 1 mm, step 0.25 mm), the primary descriptor in the "Vessel specific" report.**
  - T: the implementation behind the reported numbers is `repro/metrics.py`, with reflected-end padding and constant-chord resampling, and `pervessel/compute.py`, which writes columns `ka_s{σ}_l{ℓ}`, `kr_*`, `Q_*` and `K_*` for σ ∈ {0.5, 1, 2} and ℓ ∈ {2, 3, 5, 8}. — [repro/metrics.py](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/95342cdc-997a-4936-86b1-8ef0c6bb5ebe/scratchpad/repro/metrics.py); [pervessel/params.json](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/95342cdc-997a-4936-86b1-8ef0c6bb5ebe/scratchpad/pervessel/params.json)
  - S: `tortuosity/merged.py::scc_density` is the same estimator family (Σθ/(πℓ·n) on a chord-resampled chain). It is untracked and has no Gaussian pre-smoothing. — [tortuosity/merged.py](file:///zhome/e2/6/224426/project/ImageCAS-X/tortuosity/merged.py)
  - C: `topology/tortuosity.py` computes Frenet finite-difference curvature (`curvature_mean/rms/max`), torsion, SOAM, inflections, bends > 45° and plane measures with σ = 1 mm and step 0.25 mm. That is the family the regional report *drops* ("Frenet finite-difference curvature ... too unstable to carry"). — [topology/tortuosity.py lines 30-95](file:///zhome/e2/6/224426/project/ImageCAS-X/topology/tortuosity.py); [Plaque prone report, "The recommended set"](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Plaque%20prone%20regional%20geometry%20descriptors.md)
  - Regional κ_l5 and κ_l3 in 2 to 17 mm proximal windows: T only (`regional/extract.py::kappa_chord`). — [regional/extract.py](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/389c400f-e05f-4871-b8aa-6345347e6d71/scratchpad/regional/extract.py)
- **κ·r (δ, Dean curvature ratio), Ablation 1 in the regional report.** N. The feature list actually written by `regional/extract.py` is: abs_tau_med, angle, area_ratio, daughter_ratio, finet, interostial, kappa_diff, kappa_l3, kappa_l5, len_*, murray_dev3, murray_k, present, r0, rA, rB, r_start, taper_rel, taper_slope, tau_signed_mean, thetaA, thetaB, tree_len, turning_rad. No product feature is among them. A grep for δ, delta, "curvature ratio" and k*r in `extract.py`, `analyse.py` and `analysis.txt` returned nothing. The report's status "δ borderline pointwise, use window average" therefore has no traceable computation. The quantity is defined only in the literature note. — [regional out/*.csv feature column](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/389c400f-e05f-4871-b8aa-6345347e6d71/scratchpad/regional/out/113.csv); [hemodynamic_geometry_proxies.md line 41, 56](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Plaque%20prone%20regional%20geometry%20descriptors/hemodynamic_geometry_proxies.md)
- **Bifurcation angles with a fixed tangent rule (fitcore3, σ = 1 mm).**
  - C: `topology/angles.py` fits over [r_J, r_J + 3] mm (`core_scale = 1.0`, `window_mm = 3.0`), which is the fitcore3 definition. It also names the LM, LAD-D1, LAD-D2, LCX-OM1 and CRUX bifurcations and returns NaN rows with a reason when a bifurcation is missing.
  - It needs a per-point radius. That radius comes either from a `radius` array in the VTK (absent in the delivered files, per `io.load_centerline`'s fallback) or from `paths.radius_cache_path` under `OUTPUT_ROOT`. The cache is written by `scripts/compute_centerline_radius.py`, which exists only on the `tree-extraction` and `week3` branches.
  - The σ = 1 mm pre-smoothing and the other five tangent rules (sec2/3/5, fit0-3, fit3-8) used for the "19 to 27° within a case" claim are T only.
  - Sources: [topology/angles.py lines 1-30, 314-358](file:///zhome/e2/6/224426/project/ImageCAS-X/topology/angles.py); [topology/io.py load_centerline](file:///zhome/e2/6/224426/project/ImageCAS-X/topology/io.py); [regional/extract.py TANGENTS](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/389c400f-e05f-4871-b8aa-6345347e6d71/scratchpad/regional/extract.py)
- **Finet ratio and daughter radius ratio.**
  - C (formula): `angles.py` carries `radius_ratio`, `area_ratio` and `finet_ratio` fields.
  - T (the reported definition "median over [r_J, r_J + 3] mm" and the ICCs of 0.85 to 0.90 at the LM and 0.44 at the crux): `regional/extract.py` lines ~305-308.
  - Radius used two ways, both T: `r_edt` from the native NIfTI via `topology.radius.radius_at`, and `r_surf` from the surface mesh (`regional/radius_two_ways.py`, 100 cases cached in `radius/*.npz`).
  - Sources: [angles.py docstring](file:///zhome/e2/6/224426/project/ImageCAS-X/topology/angles.py); [radius_two_ways.py](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/389c400f-e05f-4871-b8aa-6345347e6d71/scratchpad/regional/radius_two_ways.py)
- **SRVF elastic registration and Karcher template.** T only: `treemath/proto.py`, on 30 curves (10 each of LAD, LCX and RCA), M = 100 samples. Its output reports:
  - 110 ms per pair;
  - "DP steps rejected (warp did not lower L2): 636/1308", meaning the dynamic-programming warp was rejected in about half the steps;
  - elastic 1-NN accuracy 0.93 against 0.90 for rotation-only;
  - distance under correlated 0.5 mm error 0.163, which is 0.38 of the inter-subject median;
  - an "extrinsic" 5-iteration Karcher-style mean for the LAD only.
  - No per-segment templates, no null curve for absent branches, no D1/OM1 take-off validation, and no partial or open-end matching. There is no SRVF code in the repo (grep for srvf, karcher and elastic in *.py found none).
  - Sources: [treemath/out_M100.txt](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/389c400f-e05f-4871-b8aa-6345347e6d71/scratchpad/treemath/out_M100.txt); [treemath/proto.py](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/389c400f-e05f-4871-b8aa-6345347e6d71/scratchpad/treemath/proto.py)
- **Node graph with anatomical correspondence (tokenised tree, latent-query model, tangent-PCA baseline).** N. `graph.py` gives labelled `Segment`/`Vessel` objects, which are the raw material. No code resamples them into nodes (1 mm or SRVF-matched), builds a heart-anchored frame (LCA ostium → RCA ostium), assigns depth or generation features, or exports a graph dataset. There is also no model code outside the segmentation framework. — [topology/graph.py function list](file:///zhome/e2/6/224426/project/ImageCAS-X/topology/graph.py); [Plaque prone report node-feature table](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Plaque%20prone%20regional%20geometry%20descriptors.md)
- **Sliding-window arc/chord TI(Δ).** T only: `repro/ext.py` ("mean over windows of arc length Delta of (Delta/chord) − 1, Delta in {2, 5, 10, 20} mm, windows stepped by 0.25 mm"). `pervessel/compute.py` has a *different* multiscale TI (`TIms_l{ℓ}`, chord-resampled whole-vessel TI), so the two names must not be conflated. The committed `topology/tortuosity.py` has 20 mm sliding windows for SOAM and κ_rms maxima, not for arc/chord. — [repro/ext.py](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/95342cdc-997a-4936-86b1-8ef0c6bb5ebe/scratchpad/repro/ext.py); [pervessel/compute.py line 77-78](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/95342cdc-997a-4936-86b1-8ef0c6bb5ebe/scratchpad/pervessel/compute.py)
- **Pre-registered reliability protocol (ICC(2,1) within vessel, perturbation chain, bias cap, dated thresholds).**
  - T: `regional/analyse.py` has an ICC(2,1) with 1000 case-bootstrap resamples (rng 0); `repro/analyze_icc.py` and `repro/icc.csv` also exist.
  - S: `tortuosity/run_merged_tests.py` has thresholds written in code ("fixed here, before any cohort number was seen": `MIN_RHO_STABLE = 0.8`, `MIN_ICC = 0.75`, `MAX_FLOOR = 0.2`, `MAX_ABS_LENGTH_RHO = 0.5`), but for the *merged* method (scc/grisan3d at ℓ_ref = 4 mm), not for κ_a at 5 mm. It is untracked, so it carries no commit date.
  - Its output exists on work3: `tortuosity_merged/train_vessels.csv` (1680 rows ≈ 560 × 3) and a 60-row pilot. `train_failed.txt` is empty.
  - Sources: [regional/analyse.py](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/389c400f-e05f-4871-b8aa-6345347e6d71/scratchpad/regional/analyse.py); [tortuosity/run_merged_tests.py](file:///zhome/e2/6/224426/project/ImageCAS-X/tortuosity/run_merged_tests.py); [/work3/s254124/imagecasx_results/tortuosity_merged/](file:///work3/s254124/imagecasx_results/tortuosity_merged/train_vessels.csv)
- **Synthetic suite.**
  - T: `repro/synthetic.py` and `synth_ext.py`, plus `math/t1..t6`.
  - S: `run_merged_tests.py synthetic` (line, sinusoid, alternating arcs) for the merged method only.
  - Sources: [repro/synthetic.py](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/95342cdc-997a-4936-86b1-8ef0c6bb5ebe/scratchpad/repro/synthetic.py); [math/](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/95342cdc-997a-4936-86b1-8ef0c6bb5ebe/scratchpad/math/t1_geometry.py)
- **Extractor agreement on the 160 test scans (reference vs CAS-Net-derived centerlines).** N. The only skeleton code is `skimage.morphology.skeletonize` inside `utils/metrics.py`, used for clDice/centerline metrics. It does not produce a labelled VTK tree. `io.centerline_file(root=...)` is ready to read predicted centerlines once they exist in the same naming. — [utils/metrics.py lines 73-84](file:///zhome/e2/6/224426/project/ImageCAS-X/utils/metrics.py); [topology/io.py centerline_file](file:///zhome/e2/6/224426/project/ImageCAS-X/topology/io.py)
- **Region labeller for unlabelled (CAS-Net / CGPS) trees and the label-free arc-length fallback.** N. — [repo grep for cgps/herlev in *.py/*.sh/*.json: no hits](file:///zhome/e2/6/224426/project/ImageCAS-X/)
- **Inventory of what still exists in the two cited scratchpads** (both present on `hpclogin1` `/tmp`, local disk `/dev/sda7`):
  - 95342cdc (61 MB): `math/` t1 to t6 plus `common.py`; `pervessel/` (compute, analyse, crossvessel, dominance_iq, jitter_angle, plots_noise, `metrics.csv` 1.3 MB, `params.json`); `repro/` (metrics, synthetic, real, ext, extract, extra, check, analyze and analyze_icc, with outputs `real_{LAD,LCX,RCA}.csv` ~13 MB each, `ext_*.csv`, `icc.csv`, `vessels.npz`, `calib.npz`); `repo/` (a private copy of topology `io/paths/coords/graph/radius` plus `label_map.json`); `probe.py` and `probe2.py`.
  - 389c400f (44 MB): `regional/` (common, extract, analyse, radius_two_ways, `label_map.json`, `out/` 100 per-case CSVs plus a log, `radius/` 101 files, `analysis.txt`, `err.txt` of 392 lines that are Pandas4 FutureWarnings at the head); `treemath/` (`proto.py`, `out_M100.txt`, `out_tmd.txt`).
  - Sources: [95342cdc scratchpad](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/95342cdc-997a-4936-86b1-8ef0c6bb5ebe/scratchpad/); [389c400f scratchpad](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/389c400f-e05f-4871-b8aa-6345347e6d71/scratchpad/)
- **Other scratchpads with older, possibly relevant geometry code**, not cited by the five reports:
  - `ca2bf90b/` (2026-09-16): `kappa_noise_floor.py`, `planarity_*`, `quality_confound.py` and **`disease_compare.py`**.
  - `58b7d004/` (2026-09-22): `automated_landmarking_{bogunovic,piccinelli,tools}.py`.
  - The `tree-extraction` branch has `scripts/tortuosity_disease.py`.
  - These Disease-touching scripts matter for the pre-registration claim: they show that Disease was looked at in some earlier session, even though the five reports did not open it.
  - Sources: [ca2bf90b scratchpad](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/ca2bf90b-8580-4afb-aece-9fc6dc61bc95/scratchpad/disease_compare.py); [58b7d004 scratchpad](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/58b7d004-89a3-4909-88a0-d90c95ee1ed5/scratchpad/automated_landmarking_tools.py)

### Inferences
- The two tortuosity code lines in the repo disagree with the reports' final recommendation. `topology/tortuosity.py` is Frenet-based, which the reports reject. `tortuosity/merged.py` is the chord family, but it has no smoothing and uses ℓ_ref = 4 mm, not the recommended σ = 1 and ℓ = 5. The recommended κ_a pipeline exists only in `repro/metrics.py` and `pervessel/compute.py`.
- `run_merged_tests.py` produced a full-train-split CSV for the merged method. The later reports demoted Grisan-3D and dropped Q, so that 560-scan result is a sunk cost apart from its `scc_*` and `arc_chord` columns. It also consumed all 560 training scans, which bears on the "unused confirmation scans" problem.
- κ·r should be treated as unmeasured. The regional report's status column overstates what was run.
- The SRVF prototype's roughly 50 % DP-step rejection rate suggests the warp optimiser is fragile. The 1-NN gain of 0.93 against 0.90 is within what 30 curves can resolve. SRVF is a feasibility sketch, not evidence.

### Gaps
- I did not rerun any scratch script, so I cannot confirm they still reproduce their text outputs with the current staged `topology/` modules. Some scratch scripts import `topology` from the repo via `sys.path` and monkey-patch `paths.LABEL_MAP` and `OUTPUT_ROOT`.
- I did not check which training IDs `run_merged_tests.py cohort` actually used. The row count suggests all 560, but this is unverified.
- Whether `/tmp` on `hpclogin1` is purged on reboot or by age is not documented anywhere I checked. The scratchpads are visible only from this login node.

## Q2. Which environment and reproducibility blockers exist right now?

### Takeaway
All five blockers named in the task are confirmed. The audit also found three larger ones:
- The CAS-Net path is unrunnable on this machine: no torch in the venv, no pretrained weights, no volumes or resampled caches.
- The repo is not installed in the venv.
- CLAUDE.md's description of the data tree is stale for `/work3`.

The descriptor work on reference centerlines is unblocked by three small edits. Everything that needs CAS-Net predictions (reliability step 1, extractor agreement, CGPS) is blocked until the segmentation environment is rebuilt.

### Cited Findings
- **`docs_thesis/label_map.json` is missing**, and `topology.graph.load_trees(1)` fails with `FileNotFoundError: .../docs_thesis/label_map.json`. The file is recoverable byte-identically from `git show 5742f47:docs_thesis/label_map.json` or `tree-extraction:docs_thesis/label_map.json` (14 labels: 1 LM, 2 LAD, 3 LCX, 4 D1, 5 D2, 6 OM1, 7 OM2, 8 IM, 9 RCA, 10 R-PDA, 11 R-PLA, 12 L-PDA, 13 L-PLA, 14 Other). — [topology/paths.py LABEL_MAP](file:///zhome/e2/6/224426/project/ImageCAS-X/topology/paths.py); [commit a556062 added it; absent at HEAD](file:///zhome/e2/6/224426/project/ImageCAS-X/docs_thesis/)
- **Blackhole fallbacks in `topology/paths.py`:**
  - `DATA_ROOT` falls back to `/dtu/blackhole/0a/224426/imagecasx_data`. This is harmless when env.sh is sourced.
  - `OUTPUT_ROOT` defaults to `/dtu/blackhole/0a/224426/imagecasx_derived` unless `IMAGECASX_OUT` is set. env.sh does *not* set `IMAGECASX_OUT`, and `/dtu/blackhole/0a/224426` does not exist on this machine. `output_dir()` would therefore fail at `mkdir`, and the radius cache is never found, so `angles.py` gets no radius.
  - Sources: [topology/paths.py lines 18-50](file:///zhome/e2/6/224426/project/ImageCAS-X/topology/paths.py); [env.sh](file:///zhome/e2/6/224426/project/ImageCAS-X/env.sh)
- **The radius producer is missing on this branch.** `paths.radius_cache_path` and `io.load_centerline` point at `scripts/compute_centerline_radius.py`, which exists only on the `tree-extraction` and `week3` branches. Its companions (`extract_bifurcation_angles.py`, `tortuosity_sensitivity.py`, `angle_sensitivity.py`, `derive_label_map.py`) are also there, and `topology/tortuosity.py`'s docstring references `tortuosity_sensitivity.py`. — [`git ls-tree -r tree-extraction scripts/`](file:///zhome/e2/6/224426/project/ImageCAS-X/scripts/)
- **The data tree differs from CLAUDE.md.** `$ImageCAS_X_data_path = /work3/s254124/ImageCAS-X_dataset` is a plain 3.7 GB directory containing only:
  - `centerlines/` (1600 VTK = 800 × left/right);
  - `segmentations/` (800 `.coronary.nii.gz` plus a stray uncompressed `1.coronary.nii`, 72 MB, case 1 is in train);
  - `surfaces/` (800);
  - `filelist/` (560/80/160/200);
  - `Descriptors.xlsx` and a `.DS_Store`.
  - There are **no symlinks** and no `volumes/`, `volumes_resampled/`, `segmentations_resampled/`, `imagecas_orig_labels/` or `centerline_samples/`. CLAUDE.md lists all of these as present, with sizes.
  - Sources: [ls of $ImageCAS_X_data_path](file:///work3/s254124/ImageCAS-X_dataset/); [CLAUDE.md "State of the data"](file:///zhome/e2/6/224426/project/ImageCAS-X/CLAUDE.md)
- **No weights, no trained runs.** `$ImageCAS_X_weights_path = /work3/s254124/pretrained_weights` does not exist. `$ImageCAS_X_results_path` contains only `tortuosity_merged/` and `tortuosity_merged_pilot/`, not the nine `*_pretrained` dirs CLAUDE.md describes. — [ls /work3/s254124](file:///work3/s254124/)
- **The venv lacks torch.** `import torch, monai` fails with `ModuleNotFoundError: No module named 'torch'` in `/work3/s254124/venvs/imagecasx`. vtk 9.7.0 and pyvista 0.49.0 are present. CLAUDE.md states torch 2.11.0+cu128. — [venv check](file:///work3/s254124/venvs/imagecasx/)
- **The repo is not installed in the venv.** From `/tmp`, both `import topology` and `import models` fail. site-packages holds only `_virtualenv.pth`, with no `__editable__` finder or `imagecas_x` dist-info. Scripts therefore work only when run from the repo root or with `sys.path` hacks, which is how the scratch scripts do it. — [site-packages listing](file:///work3/s254124/venvs/imagecasx/lib/python3.11/site-packages/)
- **`topology` is not in `[tool.setuptools.packages.find]`.** The include list is augmentation, dataloading, losses, models, postprocessing, preprocessing and utils, so an editable install would still miss `topology*` (and `tortuosity*`). — [pyproject.toml lines 34-43](file:///zhome/e2/6/224426/project/ImageCAS-X/pyproject.toml)
- **Uncommitted files:**
  - `topology/{__init__,io,paths,coords}.py` are staged but not committed. HEAD has only graph, angles, radius and tortuosity, so HEAD itself cannot import `topology.graph`.
  - `tortuosity/{vessels,merged,run_merged_tests}.py`, three of the five reports, their research_notes and `from_superviser.tex` are untracked.
  - `pyproject.toml` (adds pyvista and pandas) and `env.sh` (blackhole → work3) are modified.
  - `tortuosity/CLAUDE.md` is gitignored by the `CLAUDE.md` pattern, so the selection criteria it defines are not version-controlled.
  - Sources: [git status](file:///zhome/e2/6/224426/project/ImageCAS-X/); [.gitignore line 3](file:///zhome/e2/6/224426/project/ImageCAS-X/.gitignore)
- **`env.sh` is tracked in git**, contrary to CLAUDE.md ("Gitignored, machine-local"). Its diff swaps every blackhole path for work3, so committing it will break the other machine. — [git diff env.sh](file:///zhome/e2/6/224426/project/ImageCAS-X/env.sh)
- **`tortuosity/CLAUDE.md` forbids importing `topology/tortuosity.py`**, which it treats as "prior art". `tortuosity/vessels.py` reimplements vessel extraction by longest geodesic path over label-2/3/9 edges. That is a second, different definition of "the LAD" from `topology.graph.Vessel`, which chains same-named segments. — [tortuosity/CLAUDE.md](file:///zhome/e2/6/224426/project/ImageCAS-X/tortuosity/CLAUDE.md); [tortuosity/vessels.py](file:///zhome/e2/6/224426/project/ImageCAS-X/tortuosity/vessels.py)

### Inferences
- The regional report says the absence of `segmentations_resampled/` forced native NIfTI radii. More precisely, *every* derived cache is absent: the whole CLAUDE.md data description was written for the blackhole machine. For topology work this matters little. `topology.radius` reads native NIfTI through `io.load_segmentation`, and native spacing (in-plane ~0.35 mm, z 0.5 mm) is arguably the better choice for radius. It should simply be declared as the method.
- The two vessel definitions (`tortuosity/vessels.py` longest geodesic vs `graph.Vessel` label chaining) can yield different LAD endpoints, and therefore different TI and κ_a. The scratch P150 and P100 runs used different loaders, so they are not strictly comparable until this is resolved.
- Because torch, the weights and the volumes are all missing, the reports' top priority 1 cannot start without first redoing the environment and data staging. That work is Kaggle download plus Zenodo weights plus `pip install torch`, several GPU-hours and 100+ GB. Priority 1 is the reference-vs-CAS-Net extractor spectrum, which decides σ and ℓ. The reports list it as step 1 but do not cost it.

### Gaps
- It is unclear whether the blackhole machine still exists with the caches, weights and `*_pretrained` runs. If it does, copying may be cheaper than regenerating.
- I did not check whether `uv sync` would install torch from `pyproject.toml`, or whether torch is an optional or extra dependency.

## Q3. What does the project need that the reports did not address, or addressed only briefly?

### Takeaway
The reports are descriptor-centric. The supervisor email and the project plan put the weight on four other things:
- representation and tokenisation with anatomical correspondence;
- phenotyping, meaning clustering or embedding into "typical variation" classes;
- a working ImageCAS-X → CGPS inference and labelling path with domain-shift and QC;
- repeat-scan correspondence and reproducibility.

The plan also has two objectives the reports never touch: outlier and extreme-value detection (obj. 9) and MACE risk prediction (obj. 10). None of these has any code.

### Cited Findings
- Bjørn's requests:
  - "More important to find a strong representation of the CAs than to craft a big set of descriptor features."
  - Graphs have "a correspondence issue ... vertices at the same position in the sequence corresponding to widely different anatomical points", so "you need to cook a good CA -> graph algorithm", normalise distances, and "tokenize your tree".
  - Suggested node features: xyz, lumen radius, arc length from root, depth, L/R embedding.
  - Architecture: "variable length input - fixed length embeddings" with learned latent queries cross-attending.
  - Warnings about transformer positional encodings needing lots of data; suggests "anatomically realistic data augmentation".
  - Source: [from_superviser.tex](file:///zhome/e2/6/224426/project/ImageCAS-X/from_superviser.tex)
- Kit's framing:
  - "categorize typical variation in the CA into some classes/phenotypes".
  - Embeddings "will separate on ... heart size, dominance, number of branches"; normalising "may help".
  - "Main goal is the HØ dataset and matching the shape descriptors with outcome"; "use ImageCAS to develop the shape descriptors, and compute some statistics".
  - Also tells Mathilde not to "get bogged down in the details of representation learning for now".
  - Source: [from_superviser.tex](file:///zhome/e2/6/224426/project/ImageCAS-X/from_superviser.tex)
- The project plan, weeks 7 to 10 and 11 to 14, includes:
  - "ImageCAS-X to CGPS domain shift";
  - "Method for anatomical correspondence between repeat scans of the same participant" (risk 4);
  - "Repeat-scan reproducibility study: per-feature measurement error and minimum detectable change";
  - "normative reference ranges";
  - "Outlier and extreme-value detection" (obj. 9);
  - a "Risk-prediction model for major adverse cardiac events" with a clinical baseline plus topology features and outlier flags (obj. 10);
  - weeks 5 to 6 "ground-truth-free inference path, and per-scan connectivity quality control".
  - Source: [thesis/project_plan.tex](file:///zhome/e2/6/224426/project/ImageCAS-X/thesis/project_plan.tex)
- How much the reports cover each of these:
  - **Correspondence and tokenisation.** One section of the regional report: labelled SRVF per named segment → M matched tokens. It also says "If a latent-query network does not beat tangent PCA of a labelled elastic tree ... the network is not earning its keep". The "Choosing" report mentions a "tokenised tree baseline" only as the host for ablations. No report specifies a *tree-level* tokeniser: how tokens from different segments are ordered or pooled, how absent branches (OM1 missing in 20/100, D1 absent in 3/100) and the ramus are handled, or how "Other" labels are treated. — [Plaque prone report, "Elastic registration" and "recommended set"](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Plaque%20prone%20regional%20geometry%20descriptors.md); [regional_feasibility.md line 23](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Plaque%20prone%20regional%20geometry%20descriptors/regional_feasibility.md)
  - **Anatomically realistic augmentation.** One sentence: SRSF phase and amplitude generative models are "a published route". [SNIP-level Tucker 2013] — [Plaque prone report](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Plaque%20prone%20regional%20geometry%20descriptors.md)
  - **Phenotyping or clustering.** Not addressed in any of the five reports; checked by reading their section headings and conclusions. The nearest is the "Vessel specific" report's inference that κ_a is coherent within patients (cross-vessel ρ up to 0.60), "fits tortuosity as a patient-level phenotype", or a scan-level factor. — [Vessel specific report, "Curvature survives"](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Vessel%20specific%20tortuosity%20math%20and%20tests.md)
  - **Sample size and power for CGPS.** One paragraph in the regional report. It gives ≈345 patients at OR 1.3/SD, 20 % incidence, 10 regions, ρ = 0.1, λ = 0.7, and says to use λ from short-interval repeats. The "Choosing" report cites OR 1.05 to 1.09 per SD for "power expectations". These two effect-size assumptions differ by a factor of about 3 to 5 in log-OR, and no report reconciles them. — [Plaque prone report](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Plaque%20prone%20regional%20geometry%20descriptors.md); [Choosing report step 9](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Choosing%20a%20coronary%20tortuosity%20descriptor.md)
  - **Domain shift (diseased ImageCAS → asymptomatic CGPS).** Only in passing:
    - scanner as a covariate, with ComBat as a sensitivity analysis;
    - "confirm with supervisors" for the serial subset size, scanners and reading protocol;
    - the labeller should be "trained on ImageCAS-X's 800 labelled trees with position-only inputs that match CGPS".
    - Not addressed: that ImageCAS reference distributions come from a *symptomatic, CAD-enriched* population, so "normative" z-scores built on it would be biased for a healthy cohort. Also not addressed: that CAS-Net was trained on ImageCAS lumens, with a CGPS segmentation-accuracy gap measured only on a to-be-annotated subset.
    - Sources: [Plaque prone report](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Plaque%20prone%20regional%20geometry%20descriptors.md); [project_plan.tex Track B](file:///zhome/e2/6/224426/project/ImageCAS-X/thesis/project_plan.tex)
  - **Short-interval repeats.** The supervisor-questions file already lists this as open. Its default is "repeat manual labelling for measurement error; years-apart repeats reported as ...". — [docs_thesis/supervisor_questions.md item 3](file:///zhome/e2/6/224426/project/ImageCAS-X/docs_thesis/supervisor_questions.md)
- **Dominance imbalance.** 95 of the 100 regional-sample scans are right-dominant (3 co-dominant, 2 left). That means ~5 % non-right cases, a small stratum for per-dominance reference ranges or any phenotype split on dominance. — [regional_feasibility.md line 26](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Plaque%20prone%20regional%20geometry%20descriptors/regional_feasibility.md)
- **Existing code that serves CGPS preparation.**
  - `postprocessing/qiu/` exists, but only a `__pycache__` is present in the working tree. That is the stage-2 reconnection work noted in memory.
  - `io.centerline_file(root=...)` accepts predicted centerlines.
  - No CGPS paths, loaders or QC scripts exist.
  - Sources: [postprocessing/qiu/](file:///zhome/e2/6/224426/project/ImageCAS-X/postprocessing/qiu/); [topology/io.py](file:///zhome/e2/6/224426/project/ImageCAS-X/topology/io.py)

### Inferences
- The thesis-critical missing algorithm is a **CA → token-sequence map that works on unlabelled trees.** On ImageCAS-X the labels make correspondence nearly free, since per-segment arc-length resampling already gives correspondence up to warping. Every downstream use (CGPS, repeat-scan correspondence, CAS-Net trees) needs either a labeller or a label-free alternative. The reports rank the labeller as priority 2 but treat it as a classification problem. The supervisor frames it as a representation problem. One piece of work, "label the tree, then tokenise per named segment with SRVF or arc-length matching", serves the descriptor ablations, the phenotyping embedding and the repeat-scan correspondence (plan item, risk 4). It should be scoped as the central method contribution, not as preprocessing.
- Phenotyping needs a representation before it needs a model. The cheapest defensible baseline is the one the regional report already names: tangent PCA or k-means over labelled per-segment resampled curves plus radius, with size and dominance regressed out or stratified. Kit predicts that embeddings will separate on heart size, dominance and branch count, so the first phenotyping experiment should *test* that prediction by correlating PCs with tree length, dominance and branch count. Treat it as a result, not a nuisance.
- The augmentation that Bjørn wants can come cheaply from the same machinery. Sampling from per-segment PCA (or SRVF tangent-space PCA) modes gives anatomically plausible trees. No report scopes it, and it is only needed if a learned model is attempted.
- The power arithmetic depends on an unverified OR assumption and on λ, which cannot be measured until CAS-Net predictions exist. The honest thesis position is a sensitivity table over OR ∈ {1.05, 1.1, 1.3} and λ ∈ {0.5, 0.7, 0.9}. That table is also the answer to "is a null informative".
- The domain-shift question has a measurable ImageCAS-internal proxy. `Descriptors.xlsx` Image Quality strata are allowed, and so is dominance. Disease strata are allowed *after* locking. Comparing descriptor distributions across them indicates how much reference ranges move with population, before CGPS is seen.

### Gaps
- The CGPS serial-subset size, the scanners, the availability of short-interval repeats, and the plaque-reading protocol are all unknown. The regional report and `supervisor_questions.md` both leave them open.
- No source found for how many ImageCAS scans have a ramus/IM or other variants across the full train split. The label map includes IM (8) and "Other" (14), but prevalence was only reported for the 100-scan sample.
- Objectives 9 and 10 (extreme-value detection, MACE model) have no design in any report. I found nothing in the repo either.

## Q4. What is the smallest ordered set of steps that turns the reports' conclusions into reproducible thesis results?

### Takeaway
There are six blocks, and the first three are small. Steps 0 to 2 below use only reference centerlines and native masks. They can produce thesis-grade, reproducible descriptor numbers on the training split without CAS-Net. Step 3, rebuilding the CAS-Net environment, is the long pole: it gates every reliability claim and all CGPS work, so it should start in parallel now.

### Cited Findings (the facts each step rests on)
- The scratch code to port is enumerated in Q1. The fixes are enumerated in Q2. The reports' own orders are the regional report's priorities 0 to 7 and the "Choosing" report's steps 0 to 9. Both put "fix environment, move scratch into repo, commit dated definitions" first. — [Plaque prone report priorities](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Plaque%20prone%20regional%20geometry%20descriptors.md); [Choosing report "Experiments in order"](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Choosing%20a%20coronary%20tortuosity%20descriptor.md)
- The "Vessel specific" report requires that selection thresholds and the bias cap be committed "with a date, before the rerun", and that confirmation use "training scans outside both samples". P150 is the first 150 of `train.txt`. P100 and the regional 100 are `default_rng(0)` draws, and they overlap. — [Vessel specific report conclusion](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Vessel%20specific%20tortuosity%20math%20and%20tests.md); [regional/common.py cases()](file:///tmp/claude-324426/-zhome-e2-6-224426-project-ImageCAS-X/389c400f-e05f-4871-b8aa-6345347e6d71/scratchpad/regional/common.py)

### Inferences (proposed order)
0. **Make the repo importable and committed (≈1 hour, login node).**
   - Restore `docs_thesis/label_map.json` from 5742f47.
   - Export `IMAGECASX_OUT=/work3/s254124/imagecasx_derived` in env.sh, or change the default.
   - Commit the staged `topology/{__init__,io,paths,coords}.py`.
   - Add `topology*` and `tortuosity*` to `packages.find` and `pip install -e .` into the venv.
   - Bring `scripts/compute_centerline_radius.py` over from `tree-extraction`.
   - Decide whether env.sh stays tracked. It is currently tracked, with a blackhole → work3 diff.
   - Update CLAUDE.md's data section to what actually exists.
   - Delete or explain the stray `segmentations/1.coronary.nii`. It is outside the read-only rule only if this tree is the user's own copy.
1. **Rescue the scratch code before `/tmp` is lost (login node, copy only).**
   - Copy `95342cdc/.../{math,pervessel,repro}/*.py` plus `params.json`, and `389c400f/.../{regional,treemath}/*.py`, into `tortuosity/` (or `tortuosity/scratch_import/`) unchanged, with a commit noting their provenance.
   - Copy the text outputs (`analysis.txt`, `ext_analysis.txt`, `out_M100.txt`) next to them, so the report numbers stay traceable.
   - The ~40 MB of CSVs can go to `/work3`.
   - Do this first among the code steps, because it is the only irrecoverable item.
2. **Consolidate one descriptor module and pre-register (small code, CPU bsub).**
   - Pick one vessel definition: `graph.Vessel` (label chaining) or `vessels.longest_path`, and record the choice.
   - Implement κ_a (σ = 1, ℓ = 5, 0.25 mm step, reflected-end padding), TI, TI(Δ) and κ·r as a window average in one module.
   - Reuse `angles.py` fitcore3 plus Finet and daughter ratio with the EDT radius on native NIfTI, declared as the method.
   - Write the thresholds and the |bias| ≤ 10 % cap into a committed, dated file (e.g. `tortuosity/PREREG.md`, or code constants plus the commit date).
   - List the confirmation IDs explicitly: training IDs not in P150 ∪ P100 ∪ regional-100 ∪ whatever `run_merged_tests` used.
   - Rerun the synthetic suite and the jitter, truncation and ICC chain as a user-submitted CPU job writing per-case files to `/work3`. Result: reproducible versions of the reports' numbers, or corrections.
3. **Rebuild the segmentation environment (long pole, start in parallel).**
   - Install torch and monai into the venv.
   - Restage the pretrained weights (Zenodo 21887809) and the ImageCAS volumes (`jobs/download_imagecas.sh`).
   - Regenerate the 0.5 mm caches, or copy them if the blackhole machine is reachable.
   - Run `cas_net_pretrained` inference on the 160 test scans.
   - Add a centerline extractor for predictions that writes VTK in the delivered naming, so `graph.load_trees(root=...)` works. It is not in the repo.
   - This unlocks regional priority 1 (extractor error spectrum → fix σ and ℓ) and the λ estimate.
4. **Correspondence and tokenisation baseline on ImageCAS-X training (the supervisor's core ask).**
   - Per named segment: arc-length resampling to M nodes with features (heart-frame xyz normalised by inter-ostial distance, r, s and s/L, depth, L/R), plus explicit absent-branch tokens.
   - SRVF warping as the step-2 variant, validated by D1 and OM1 take-off spread in template coordinates.
   - Tangent-PCA or PCA embedding as the phenotyping baseline, with a check that the top PCs correlate with size, dominance and branch count (Kit's prediction).
   - Descriptor ablations enter here.
5. **Labeller or label-free fallback for unlabelled trees.** Train on ImageCAS-X labels with position-only inputs, evaluate on the CAS-Net-derived test trees from step 3, and then on the CGPS annotated subset. This is shared with the repeat-scan correspondence item in the plan.
6. **Lock, then open Disease and CGPS.**
   - Build reference distributions on training plus the confirmation set, with Image Quality and dominance strata.
   - Build the power and sensitivity table over OR and λ.
   - Pre-register the primary: LM angle, or κ_a, per the reports. The reports disagree on this; decide once.
   - Then run the CGPS pipeline and the obj. 9 and 10 analyses.

Only steps 0 to 2 are needed for descriptor numbers to enter the thesis. Step 3 gates every reliability claim that matters for CGPS. Steps 4 and 5 are the supervisor-facing contribution that the reports under-weight.

### Gaps
- The reports disagree on the single primary descriptor. "Plaque prone" names the LM daughter angle. "Vessel specific" names κ_a, and "Choosing" names TI plus κ_a. No report reconciles them, so the decision belongs to the student and supervisors before step 6.
- The GPU time for step 3 was not estimated. CLAUDE.md's walkthrough covers training from scratch, but inference-only with the delivered weights needs just the weights, the volumes and torch.
