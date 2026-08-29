# CLAUDE.md

Master's thesis: **topological characterization of coronary artery trees from cardiac CT**.
Project brief.

This repo is a fork of **ImageCAS-X** (Bransby et al. 2026), the benchmark framework published
alongside the dataset, with the thesis's topology layer merged into it (2026-08-29). Two halves:

- **Framework** (upstream): `train.py` / `inference.py` / `evaluate.py`, `configs/`, `models/`,
  `losses/`, `dataloading/`, `{pre,post}processing/`, `augmentation/`, `utils/`. Objective 5.
- **Thesis** (ours): `topology/`, `scripts/`, `docs_thesis/`, `figures/`. Objectives 6-9.

Keep them separable: `git remote add upstream git@github.com:kitbransby/ImageCAS-X.git`, and extend
the framework through its registries rather than editing its files, so upstream stays mergeable.
See Code layout below and `docs_thesis/dataset_walkthrough.md` for a narrated tour of the data.

## Thesis objectives

Written work:
1. Function of the heart, with focus on the role of the coronary arteries.
2. How CT is used to record and visualize the coronary arteries.
3. Common topology of the coronary arteries and its anatomical variants.
4. State of the art in coronary artery segmentation and topological description.

Implementation work:
5. Implement, validate and document a state-of-the-art coronary segmentation framework from CT.
6. Develop, implement, revise and validate methods for topological characterization of coronary trees.
   *(Tree construction done and validated cohort-wide — `topology.graph`, `docs_thesis/tree_construction.md`.)*
7. Extract topological features: branching patterns, dominance, angles, tortuosity.
8. Apply the framework to a large cohort; population description and statistics.
9. Outlier and extreme-value detection over the topological features.
10. Associate topological features with patient outcomes.

Objectives 6–9 are the methodological core. Objective 5 is a means to that end — prefer adopting an
established framework over inventing one. Objective 10 depends on outcome data that is not yet in hand
(see Open questions).

## Dataset: ImageCAS-X

**Provenance RESOLVED (2026-08-29):** this is the dataset of Bransby et al. 2026, *"ImageCAS-X: A
dataset and benchmark for validating coronary vessel segmentation and centerline extraction in
computed tomography angiography"* — DTU Compute + Rigshospitalet, i.e. our own lab. Dataset and
pretrained weights: [Zenodo 21887809](https://zenodo.org/records/21887809); site:
<https://kitbransby.github.io/ImageCAS-X/>. Cite the BibTeX in `README.MD`. It layers voxel labels,
centerlines, surfaces and `Descriptors.xlsx` onto the public **ImageCAS** cohort (Zeng et al.,
[arXiv:2211.01607](https://arxiv.org/abs/2211.01607)), which supplies the CT volumes.

Two roots, and the distinction matters:

- `/dtu/blackhole/0a/224426/ImageCAS-X_dataset` (3.6 GB) — the **read-only** delivered dataset.
- `/dtu/blackhole/0a/224426/imagecasx_data` — the **composed root** everything actually reads:
  symlinks to the four dataset directories and `Descriptors.xlsx`, plus `volumes/` and the caches
  the framework writes (`volumes_resampled/`, `segmentations_resampled/`, `centerline_samples/`).
  This is what `$ImageCAS_X_data_path` points at. The indirection exists because the framework
  writes its caches *inside* `data_root`, which would otherwise violate the read-only rule.

All facts below were verified by inspection on 2026-08-28.

```
centerlines/     1600 .vtk   binary  POLYDATA  — <id>.coronary_{left,right}_centerline.vtk (2 per case)
                 point arrays: segment_label (int, same ids as the segmentation), segment_name (str),
                 start_points / branch_points / end_points (0/1 flags = ostia, bifurcations, termini)
segmentations/    800 .nii.gz        uint8     — <id>.coronary.nii.gz
surfaces/         800 .vtk   ASCII   POLYDATA  — <id>.coronary_surface.vtk (3.5 GB, the bulk of the data)
filelist/           4 .txt                     — train.txt (560) val.txt (80) test.txt (160) exclude.txt (200)
Descriptors.xlsx    1000 rows, 1 sheet ("master") — columns: Scan ID, Image Quality, Dominance, Disease
```

Cases are keyed by a bare integer id (e.g. `100`), consistent across all four directories. The split
files contain one id per line and partition the 800 cases 560/80/160. `exclude.txt` holds a further 200
ids — ImageCAS ships 1000 cases, so this dataset is the 800 that survived exclusion. **Check `exclude.txt`
before assuming an id is available**; do not silently skip missing files.

### Descriptors.xlsx (verified 2026-08-28)

One sheet, `master`, 1000 rows (all of ImageCAS, including excluded cases), one row per `Scan ID`:

- `Image Quality` — integer 0–4. **`0` exactly identifies the 200 ids in `exclude.txt`** (confirmed by
  set equality); 1–4 for the 800 usable cases (4: 436, 3: 167, 2: 142, 1: 55).
- `Dominance` — `R` (729), `L` (41), `Co` (30) = codominant; `NaN` for the 200 excluded rows. **This is
  the ground truth for objective 7's dominance feature — read it from here, don't infer it from
  segmentation labels.**
- `Disease` — `yes` (388) / `no` (412) for the 800 usable cases; `NaN` for excluded. Presence/absence of
  CAD, useful as a grouping variable for population statistics (objective 8) and possibly a proxy
  outcome (objective 10) if no richer outcome data materializes.

Read with `pandas.read_excel` (needs `openpyxl` installed; plain `pandas` alone raises on `.xlsx`).

### Segmentation labels — RESOLVED (2026-08-28)

Segmentations are **multi-label, not binary**. Labels 1–14, verified against the centerlines across 36
cases with 100% agreement (`scripts/derive_label_map.py`, canonical copy in `docs_thesis/label_map.json`):

| 1 `LM` | 2 `LAD` | 3 `LCX` | 4 `D1` | 5 `D2` | 6 `OM1` | 7 `OM2` |
|---|---|---|---|---|---|---|
| 8 `IM` | 9 `RCA` | 10 `R-PDA` | 11 `R-PLA` | 12 `L-PDA` | 13 `L-PLA` | 14 `Other` |

Labels 1–8 are the left system, 9–11 the right, 12–13 the posterior vessels of left-dominant hearts.
Left and right centerline files use disjoint label ranges. **Label 14 is a catch-all** — treat it as
unlabelled, not as a specific artery.

Which labels a case has is real anatomy, not annotation noise: `R-PDA`/`R-PLA` never appear in
left-dominant hearts and `L-PDA`/`L-PLA` never in right-dominant ones, because the posterior vessels
arise from the dominant artery. This means the `Dominance` column and the label set are two independent
records of the same fact and can be cross-validated. `IM` (ramus intermedius) appears in ~25% of cases,
matching its textbook prevalence. See `docs_thesis/dataset_walkthrough.md`.

### Centerline topology — RESOLVED (2026-08-29)

The centerlines carry **exact** connectivity: polylines meet only by sharing a point index, so the
tree is built without any proximity threshold (`topology/graph.py`). `end_points` is exactly the
degree-1 set and `branch_points` exactly the degree-≥3 set in **1600/1600 sides**, which makes the
dataset's flags an independent check on the graph rather than a restatement of it. All 1600 sides pass
every validation check in `scripts/survey_topology.py`; 1584 are one clean rooted tree.

**Centerline points are already in physical mm (LPS)** — no affine, unlike anything touching the
volumes. Two traps, both handled in `graph.py`: junction points carry the *parent* vessel's label (so
segment labels are a majority vote over interior points), and after a cycle-closing edge is dropped a
degree-3 point is no longer a branch point (so node kind comes from the built tree, not raw degree).

**11 left sides have two ostia, and they are exactly the 11 left sides with no `LM` label** — set
equality. This is the **absent left main** variant (LAD and LCX from separate ostia), 1.4% of cases:
anatomy, not corruption. Never assume one ostium per side. The remaining oddities are named and
flagged, not dropped: cases 84 and 272 are genuinely fragmented, and cases 8 (L), 455 (R), 776 (L)
contain a cycle. See `docs_thesis/tree_construction.md`.

### Geometry

- Volumes are 512×512×Z, Z varies per case (206–275 in the sample).
- In-plane spacing varies per case (0.318–0.43 mm sampled); slice thickness is 0.5 mm.
- **Anisotropic and non-uniform across cases.** Any metric with physical units — tortuosity, branch
  angle, length, radius — must use the affine from the NIfTI header. Never compute in voxel space and
  never assume a shared spacing across cases.
- **Coordinate frames differ and the mismatch is silent.** NIfTI affines are RAS; the VTK centerlines
  and surfaces are LPS (`LPS = diag(-1,-1,1) · RAS`). Because coronary trees are roughly symmetric, a
  mirrored overlay still looks like a plausible heart — you will not notice by eye. Always convert via
  `topology/coords.py`. Verified correct: 100% of centerline points land on a labelled voxel and
  100% agree with that voxel's label.

### The CT images — RESOLVED and on disk (2026-08-29)

The delivered dataset carries only labels and derived geometry. The CT volumes are the base
ImageCAS cohort from [Kaggle](https://www.kaggle.com/datasets/xiaoweixumedicalai/imagecas)
(CC BY-NC 4.0 — cite ImageCAS alongside ImageCAS-X), downloaded 2026-08-29 by
`jobs/download_imagecas.sh`: 83 GB of archives, 86 GB extracted, 1000 `<id>.img.nii.gz` plus 1000
`<id>.label.nii.gz`, all present and linked into the composed root.

**Not plain zips.** Five split multi-volume archives, whose final segment was uploaded as
`.change2zip` because Kaggle refuses a second `.zip`, and Kaggle then wraps each single-file
download in *another* zip. Info-ZIP `unzip` cannot read split archives at all; `7za` can, after the
rename. Both layers are handled in the job — re-read it before changing anything there.

**`<id>.label.nii.gz` is the original ImageCAS binary label, NOT our ground truth.** It is linked to
`imagecas_orig_labels/`, deliberately out of the way. It is what the benchmark's "ImageCAS (labels)"
row scores (DSC 41.8 against the ImageCAS-X labels), and is useful for nothing else here.

Verified on arrival: all 800 usable cases have volume + segmentation + both centerlines + surface;
volume and segmentation headers agree exactly (size, spacing, origin, direction) over a 25-case
sample; and centerline points sample a **median 336 HU** in the CT — contrast-filled lumen, which
confirms the LPS/RAS conversion in `coords.py` against the *images*, not just the segmentations.

## Environment (DTU HPC)

- Login node has no GPU. System `python` is 3.9.25 with numpy/scipy/torch 2.8.0+cu128/networkx/matplotlib.
  **Missing everything imaging: nibabel, SimpleITK, vtk, pyvista, monai, scikit-image, scikit-learn,
  nnU-Net.** No conda on PATH.
- **`source env.sh` before anything.** It sets `ImageCAS_X_data_path` / `ImageCAS_X_results_path`
  (the only two paths any config reads) and points uv at blackhole. It is gitignored — machine-local.
- Env is **uv**-managed, Python 3.11, torch 2.11.0+cu128. **The venv lives at
  `/dtu/blackhole/0a/224426/venvs/imagecasx`, not in the repo** — it is 7.3 GB and `/zhome` is at
  26/30 GB quota. `env.sh` exports `UV_PROJECT_ENVIRONMENT` *and* `VIRTUAL_ENV`: `uv venv`/`sync`/
  `run` read the former, but `uv pip` reads only the latter, and fails with "No virtual environment
  found" without it. The uv cache is redirected to blackhole too.
- Home quota is the binding constraint. `~/.cache` holds ~19 GB (uv 8.3, clip 7.0, huggingface 3.6)
  left over from earlier projects — reclaimable if space runs short.
- Scheduler is **LSF** (`bsub`). GPU queues: `gpua100`, `gpuv100`, `gpua40`, `gpul40s`, `gpua10`.
  Queues are heavily contended (thousands pending) — assume long waits and write jobs to checkpoint.
- Storage: **do not write outputs to home** (quota 26/30 GB). Write to
  `/dtu/blackhole/0a/224426/` (2.8 TB free). Note blackhole is scratch: treat it as deletable, keep
  code and small results in git. The 0.5 mm resample cache alone is ~100–150 GB.
- Never run training, full-cohort feature extraction, or anything long on the login node — `bsub` it.

## Conventions

- Data is read-only input. Never modify anything under `ImageCAS-X_dataset/`; write derived artifacts
  to a separate output tree on blackhole.
- 800 cases is small enough that per-case failures matter. Prefer per-case output files over one large
  aggregate, so a crash mid-cohort does not lose completed work, and log which cases failed rather than
  dropping them silently.
- Feature extraction must be deterministic and re-runnable; record the code version alongside outputs
  so population statistics can be traced to the code that produced them.
- Respect the provided train/val/test split for anything learned. Population statistics (objective 8)
  are descriptive and may use all 800, but say which set was used.
- This is thesis work: results feed a written document. When a number is produced, keep the code path
  that produced it reproducible — no one-off shell edits that vanish.

## Open questions

- ~~Source of the CT images~~ — RESOLVED: base ImageCAS on Kaggle (see above). Still to *ask*:
  does the lab already hold the volumes and the pretrained weights internally, so we can skip the
  download entirely?
- Source of patient outcome data for objective 10 — `Disease` (yes/no) in `Descriptors.xlsx` is the only
  outcome-like field currently available and is coarse. Richer outcome data likely requires a separate
  cohort or a supervisor-provided linkage. Worth resolving early, since it may redirect which cohort the
  framework is ultimately run on.
- ~~Provenance of "ImageCAS-X"~~ — RESOLVED 2026-08-29 by getting access to this repo: Bransby et
  al. 2026, our own lab. The guess in the literature survey ("likely a local extension") was right.
  Full literature survey: see `docs_thesis/literature.md`.
- **CAS-Net is in `configs/` but absent from the benchmark table** on the project site. Is it in the
  paper? It matters because it is the method we picked to build on.

Resolved (2026-08-29): the centerline graph model, its validation over all 1600 sides, and the
absent-left-main variant (above); the dataset's provenance and the source of the CT images, both
settled by gaining access to the ImageCAS-X repo.

Resolved (2026-08-28): exclusion is by `Image Quality == 0` in `Descriptors.xlsx`, exactly matching
`exclude.txt`; dominance ground truth is the `Dominance` column, and it agrees with the label set;
the label→artery mapping is established (above); the RAS/LPS frame difference is handled in `coords.py`.

## The framework half (objective 5)

Three entry points, all `python -m`, all driven by one JSON config, all needing `source env.sh`:

```
python -m train     -c configs/<method>.json [--resume RUN_DIR]
python -m inference -c configs/<method>.json -r <run_dir> [--split test] [--save-probs]
python -m evaluate  -c configs/<method>.json -r <run_dir> [-j 8]
```

- **Configs layer.** `configs/pipeline.json` fixes everything that must be identical across methods
  for a fair comparison (paths, 0.5 mm resample, HU window −200..1000, the 8 nnU-Net augmentations,
  adam + poly LR, 1000 epochs × 250 iters, postprocessing, metrics, stratification). A method config
  declares only what is method-specific. They are deep-merged; unknown keys are silently dropped.
- **`inference.py` is the only script that loads a model.** `evaluate.py` scores whatever sits in
  `<run_dir>/predictions/`, so external methods (nnU-Net, TotalSegmentator) just drop files in.
- **Extend through registries** — `models/registry.py`, `losses/factory.py`,
  `{pre,post}processing/pipeline.py`, `augmentation/pipeline.py`. Adding a class and registering it
  needs no core edits, which is what keeps the upstream merge clean.
- **The metrics we care about already exist**: `cl_dice`, `betti_error_1/2`, `centerline_md` (ASSD),
  `centerline_hd95`, plus per-segment / per-diameter / per-HU local Dice.
- **Seed is hard-coded** `SEED = 42` in `utils/seeding.py`, deliberately not configurable, so any two
  runs of a config are directly comparable — including against the published numbers.
- **`--resume` is ours, not upstream.** Upstream saved only a bare `state_dict`, so a run killed by
  the 24 h walltime restarted from zero. `train.py` now also writes `<method>_last.pt` every epoch
  (model + optimizer + scheduler + epoch + curves, via a temp file and rename so a mid-write kill
  cannot corrupt it). `<method>_best.pt` deliberately stays a bare state_dict — `inference.py` and
  `BaseLumenModel.load_weights` expect exactly that. Chain jobs with
  `bsub -w "ended(<jobid>)" -env "all, RUN_DIR=<run_dir>" < jobs/train_cas_net.sh`.
- Two configs are **unrunnable as shipped**: `imagecas_stage3_patch_*.json` have `centers_dir: ""`
  and `imagecas_inference.json` has all five checkpoint fields `null`. ADE-HTL additionally needs
  TotalSegmentator `heartchambers_highres` masks. Skip all of these unless actually needed.

`jobs/` holds the LSF scripts: `download_imagecas.sh`, `resample_cache.sh`,
`centerline_samples.sh`, `train_cas_net.sh`.

## Code layout

`topology/` — `paths` (dataset locations, splits, descriptors, **output tree + `code_version()`**),
`io` (loaders returning `Segmentation`/`Centerline`/`Surface`), `coords` (**frame conversions — always
use these**), `graph` (**rooted `CoronaryTree` from a centerline — the structure all topological
features are computed on**), `viz` (shared artery colours, headless matplotlib helpers).
`scripts/` — `derive_label_map.py`, `survey_topology.py`, `make_case_figures.py`,
`make_dominance_figure.py`, `make_tree_figure.py`.
`docs_thesis/dataset_walkthrough.md` — narrated tour of the data; `docs_thesis/tree_construction.md` — the graph
model and its cohort-wide validation; `docs_thesis/hemodynamics.md` — how WSS/CFD turn the topology
into a functional endpoint, and the resolution limit that bounds it; `figures/` — their output.
Derived artifacts go to `paths.OUTPUT_ROOT` (`/dtu/blackhole/0a/224426/imagecasx_derived`, override
with `IMAGECASX_OUT`) — never to `/zhome`, never into the dataset.

PyVista is used **only as a VTK file parser**, never as a renderer: the login node has no `DISPLAY`
and off-screen VTK needs OSMesa/xvfb that may not be present. All rendering is matplotlib/Agg.
Hand-rolling a binary-VTK parser was tried and silently produced garbage — use `pv.read`.

## Research gap identified (2026-08-28)

Literature search (`literature.md`) found **no coronary-specific paper doing outlier / extreme-value
detection on topological features** (objective 9). Vascular feature extraction and disease-status
classification are both well covered, but treating a population's branching/tortuosity/angle features
as a distribution and flagging population-level outliers is not represented in what was found. Nearest
analogues are in a different organ (RETA retinal vascular tree benchmark) or use generic, un-adapted
tooling (scikit-learn Isolation Forest / LOF). This is a plausible novel-contribution angle for the
thesis — worth confirming it's a real gap (not a search artifact) before leaning on it in the writeup.
