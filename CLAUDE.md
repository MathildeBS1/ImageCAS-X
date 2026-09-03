# CLAUDE.md

Master's thesis: **topological characterization of coronary artery trees from cardiac CT**.
Project brief.

This repo is a fork of **ImageCAS-X** (Bransby et al. 2026), the benchmark framework published
alongside the dataset, with the thesis's topology layer merged into it (2026-08-29). Two halves:

- **Framework** (upstream): `train.py` / `inference.py` / `evaluate.py`, `configs/`, `models/`,
  `losses/`, `dataloading/`, `{pre,post}processing/`, `augmentation/`, `utils/`. Objective 5.
- **Thesis** (ours): `topology/`, `scripts/`, `docs_thesis/`, `figures/`, `thesis/`,
  `.claude/skills/`. Objectives 6-9.

Keep them separable: `git remote add upstream git@github.com:kitbransby/ImageCAS-X.git`, and extend
the framework through its registries rather than editing its files, so upstream stays mergeable.
Two upstream files are deliberately modified, both noted under The framework half: `train.py`
(`--resume`) and `utils/config.py` (`${VAR}` expansion in checkpoint paths).
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

This is the dataset of Bransby et al. 2026, *"ImageCAS-X: A
dataset and benchmark for validating coronary vessel segmentation and centerline extraction in
computed tomography angiography"* — DTU Compute + Rigshospitalet, i.e. our own lab. Dataset and
pretrained weights: [Zenodo 21887809](https://zenodo.org/records/21887809); site:
<https://kitbransby.github.io/ImageCAS-X/>. Cite the BibTeX in `README.MD`. It layers voxel labels,
centerlines, surfaces and `Descriptors.xlsx` onto the public **ImageCAS** cohort (Zeng et al.,
[arXiv:2211.01607](https://arxiv.org/abs/2211.01607)), which supplies the CT volumes.

Two roots, and the distinction matters:

- `/dtu/blackhole/0a/224426/ImageCAS-X_dataset` (3.6 GB) — the **read-only** delivered dataset.
  All four directories resolve and the counts below hold. The directories are group-writable
  (`drwxrwx---`), so read-only is a convention here, not a permission — do not rely on the
  filesystem to stop you. If the dataset is ever re-copied, re-run `scripts/survey_topology.py`:
  it rebuilds all 1600 sides in ~5 s and is the cheapest check that nothing changed.
- `/dtu/blackhole/0a/224426/imagecasx_data` — the **composed root** everything actually reads:
  symlinks to the four dataset directories and `Descriptors.xlsx`, plus `volumes/` and the caches
  the framework writes (`volumes_resampled/`, `segmentations_resampled/`, `centerline_samples/`).
  This is what `$ImageCAS_X_data_path` points at. The indirection exists because the framework
  writes its caches *inside* `data_root`, which would otherwise violate the read-only rule.


```
centerlines/     1600 .vtk   binary  POLYDATA  — <id>.coronary_{left,right}_centerline.vtk (2 per case)
                 point arrays: segment_label (int, same ids as the segmentation), segment_name (str),
                 start_points / branch_points / end_points (0/1 flags = ostia, bifurcations, termini)
segmentations/    800 .nii.gz        uint8     — <id>.coronary.nii.gz
surfaces/         800 .vtk   ASCII   POLYDATA  — <id>.coronary_surface.vtk (3.5 GB, the bulk of the data)
filelist/           4 .txt                     — train.txt (560) val.txt (80) test.txt (160) exclude.txt (200)
Descriptors.xlsx    1000 rows, 1 sheet ("master") — columns: Scan ID, Image Quality, Dominance, Disease
```

The automated tracer that initialized these centerlines is reference [26] of the paper:
Baldachowski & Korona's DTU thesis, `Former_students_work/Korona_Baldachowski_Master_Thesis.pdf`.
Two of the paper's co-authors (Jiménez, Øksnebjerg) also have work in that directory — the former
students are upstream of this dataset, not parallel to it.

Cases are keyed by a bare integer id (e.g. `100`), consistent across all four directories. The split
files contain one id per line and partition the 800 cases 560/80/160. `exclude.txt` holds a further 200
ids — ImageCAS ships 1000 cases, so this dataset is the 800 that survived exclusion. **Check `exclude.txt`
before assuming an id is available**; do not silently skip missing files.

### Descriptors.xlsx

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

### Segmentation labels

Segmentations are **multi-label, not binary**. Labels 1–14, verified against the centerlines across 36
cases with 100% agreement (`scripts/derive_label_map.py`, canonical copy in `docs_thesis/label_map.json`):

| 1 `LM` | 2 `LAD` | 3 `LCX` | 4 `D1` | 5 `D2` | 6 `OM1` | 7 `OM2` |
|---|---|---|---|---|---|---|
| 8 `IM` | 9 `RCA` | 10 `R-PDA` | 11 `R-PLA` | 12 `L-PDA` | 13 `L-PLA` | 14 `Other` |

Labels 1–8 are the left system, 9–11 the right, 12–13 the posterior vessels of left-dominant hearts.
Left and right centerline files use disjoint label ranges. **Label 14 is a catch-all** — treat it as
unlabelled, not as a specific artery.

**The right side is annotated more coarsely than the left**, and the paper documents why
(Supplementary B) — it is a deliberate protocol, not an oversight. Only `RCA`, `R-PDA` and `R-PLA`
exist for the right side, and label 14 `Other` never appears there (all 88 occurrences are left).
The protocol rules, which bound every branch-level feature:

- **Not traced at all: septal perforators, acute marginals and nodal arteries.** Note septal
  perforators are *left*-sided, so this is not purely a right-side restriction.
- A side branch was not traced where its connection to the parent was unclear, where it could not
  be clearly delineated, or where its **distal diameter was < 1 mm**.
- `Other` (14) is D3/D4/OM3/OM4, but only when at least as large as the first or second branch, or
  **> 1.8 mm** at the proximal end.
- Where a side branch itself bifurcated, only the larger was traced — unless the two were equal or
  the smaller exceeded 1.8 mm. Same rule for multiple PDAs or PLAs.
- Where a *main* vessel bifurcated, main-versus-side was decided **by course, not by size**: the
  branch continuing along the atrioventricular groove is the LCX even when the OM is larger, and
  the branch along the anterior interventricular groove is the LAD.

So a branch count measures the protocol as much as the anatomy, on both sides, and any
left-versus-right comparison must say so.

Which labels a case has is real anatomy, not annotation noise: `R-PDA`/`R-PLA` never appear in
left-dominant hearts and `L-PDA`/`L-PLA` never in right-dominant ones, because the posterior vessels
arise from the dominant artery. This means the `Dominance` column and the label set are two independent
records of the same fact and can be cross-validated. `IM` (ramus intermedius) appears in ~25% of cases,
matching its textbook prevalence. See `docs_thesis/dataset_walkthrough.md`.

### Centerline topology

The centerlines carry **exact** connectivity: polylines meet only by sharing a point index, so the
tree is built without any proximity threshold (`topology/graph.py`). `end_points` is exactly the
degree-1 set and `branch_points` exactly the degree-≥3 set in **1600/1600 sides**. That agreement is
**not independent evidence**: the paper defines the flags by degree (`end_points` = degree 1,
`branch_points` = degree ≥ 3, `start_points` = degree-1 within 5 mm of the aorta), so matching them
confirms our loader reproduces their connectivity and nothing more. All 1600 sides pass every
validation check in `scripts/survey_topology.py`; 1584 are one clean rooted tree.

**Provenance of the centerlines** (Kit_paper.pdf, Methods): the delivered centerlines are *not* the
hand-traced ones. Analysts traced centerlines in CoronaryExplorer from an automated method and
manually refined them (200 h), those drove cMPR lumen annotation, the lumen mask was U-Net predicted
then manually corrected slice by slice (270 h) — and then **new centerlines were regenerated from
the corrected masks by skeletonization + Gaussian smoothing (σ = 0.5 mm, 5-vertex window)** because
the traced ones did not run through the centre of the corrected lumen. Segment names were carried
over by nearest-match to the traced centerlines and reviewed by the lead analyst; voxel labels were
propagated from the centerline by nearest point. So the human effort sits in the **masks** and the
**segment names**, not in the centerline geometry, and the σ = 0.5 mm smoothing is baked into any
tortuosity computed from the delivered points. See `docs_thesis/tree_construction.md`.

**Centerline points are already in physical mm (LPS)** — no affine, unlike anything touching the
volumes. Two traps, both handled in `graph.py`: junction points carry the *parent* vessel's label (so
segment labels are a majority vote over interior points), and after a cycle-closing edge is dropped a
degree-3 point is no longer a branch point (so node kind comes from the built tree, not raw degree).

**13 left sides have two ostia; 11 of them are the 11 sides with no `LM` label.** Those 11 are the
**absent left main** variant (LAD and LCX from separate ostia), 1.4% of cases: anatomy, not
corruption. Never assume one ostium per side. The other two, 84 and 272, are genuinely fragmented —
a component with no ostium, rooted arbitrarily — so two-ostia and no-LM are **not** the same set, and
`survey_topology.py` prints exactly that (`identical (absent left main, not a data defect): False`).
Cases 8 (L), 455 (R) and 776 (L) contain a cycle. See `docs_thesis/tree_construction.md`.

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

### The CT images

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

## Pretrained weights

`/dtu/blackhole/0a/224426/pretrained_weights` (370 MB + 1.2 GB nnU-Net), pointed at by
`$ImageCAS_X_weights_path` in `env.sh`. These are the weights behind the published benchmark table,
so they let objective 5 be *reproduced* rather than retrained — no GPU queue, no 24 h walltimes.

Single-file weights for CAS-Net, FFR-UNet, Swin UNETR, the two ADE-HTL stages and four of the five
ImageCAS baseline stages, plus nnU-Net in its own 5-fold layout.

All are **bare `state_dict`s**, which is what `BaseLumenModel.load_weights` expects. Every one was
loaded into the model its config builds with `strict=True` and matched exactly — no missing and no
unexpected keys — by `scripts/stage_pretrained_weights.py`.

**How to use them.** `inference.py` defaults `model.checkpoint` to `<run_dir>/<method>_best.pt`, so
the weights are staged as run dirs under `$ImageCAS_X_results_path` and need no config change:

```bash
source env.sh
python scripts/stage_pretrained_weights.py      # re-runnable; verifies before linking
python -m inference -c configs/cas_net.json -r cas_net_pretrained --split test
python -m evaluate  -c configs/cas_net.json -r cas_net_pretrained
```

Nine methods are staged this way. Two exceptions:

- **The ImageCAS 3-stage baseline** loads five checkpoints by name rather than one, so it is wired
  directly in `configs/imagecas_inference.json` — an inference-only config that trains nothing.
  Only four of its five stages were delivered, so it cannot run; that config's own comment explains
  why the dilated weights must not be substituted for the missing Stage 1.
- **nnU-Net** is in its own native 5-fold layout and has no model registered in this framework. It
  runs under its own CLI and drops predictions into `<run_dir>/predictions/` for `evaluate.py`.

## Environment (DTU HPC)

- Login node has no GPU. System `python` is 3.9.25 and is missing everything imaging (nibabel,
  SimpleITK, vtk, pyvista, scikit-image) — use the venv, never the system interpreter. No conda on
  PATH. Note the framework imports neither monai nor nnU-Net; only torch, SimpleITK, scipy, numpy,
  matplotlib and tqdm.
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

- **Outcome data for objective 10.** `Disease` (yes/no) in `Descriptors.xlsx` is the only
  outcome-like field available, and it is coarse. Richer data needs a separate cohort or a
  supervisor-provided linkage. This is the highest-risk dependency in the project — it may redirect
  which cohort the framework is ultimately run on.
- **The Rigshospitalet cohort.** The project is expected to move to a Rigshospitalet dataset whose
  ground truth is unknown. The precedent is CGPS, which the previous group used: 939 scans carrying
  left-tree segmentations only — no centerlines, no artery labels, no right tree, and limited access
  to the images. If the new cohort looks like that, dominance is uncomputable and centerlines must be
  derived first. Ask early; it changes the plan.
- **No Stage-1 coarse checkpoint** was delivered for the ImageCAS 3-stage baseline (four of five
  stages arrived), so that one method cannot be reproduced from the published weights. Ask the
  dataset authors whether the file exists.
- **Is the objective-9 research gap real?** See Research gap below — worth confirming with someone
  who knows the field before leaning on it in the writeup.

## The framework half (objective 5)

**What objective 5 is reproducing** (Kit_paper.pdf, Table 2, on the 160 test cases):

| | DSC | HD95 mm | β_err | clDice | ASSD mm | cl-HD95 mm |
|---|---|---|---|---|---|---|
| **CAS-Net** (best) | 91.2 | 2.99 | 1.9 | 93.3 | 0.73 | 5.75 |
| **Inter-observer** (ceiling) | 92.8 | 2.46 | 0.4 | 95.4 | 0.53 | 4.58 |
| ImageCAS original labels | 41.8 | 16.15 | 7.0 | 78.2 | 2.23 | 18.89 |

**CAS-Net is in the paper and is the best method** — this answers the old open question. It is also
the cheapest to run (6.8 M params, 15.5 s per scan), which is why it is the one to build on. **No
automated method reaches inter-observer agreement**: every CAS-Net-vs-analyst difference is
significant (p < 0.001 on DSC, clDice and ASSD). The paper's own caveat is that both annotators
edited the *same* automatically generated centerlines and initialized from the same 3D U-Net, so
the DSC inter-observer figure is an **upper bound** on agreement rather than a neutral reference.
Analysts averaged 35 minutes per scan; every model is under 2 minutes.

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
- **Checkpoint paths expand `${VAR}`** — ours, not upstream. `utils/config.py` runs the six
  `model.*checkpoint` fields through `os.path.expandvars`, so a config can name
  `${ImageCAS_X_weights_path}/...` instead of committing a machine-local absolute path. Nothing else
  in the config is expanded, and an unset variable is left verbatim so the "Checkpoint not found"
  error shows what failed to expand.
- **Never put a pretrained path in a method config.** `train.py` builds its model through the same
  `build_model(cfg)` as `inference.py`, and that loads `model.checkpoint` whenever it is set — so a
  checkpoint left in `configs/cas_net.json` silently turns every later "fresh" run into a fine-tune,
  and the logs look normal. Use the staged run dirs instead (see Pretrained weights).
- Still **unrunnable as shipped**: `imagecas_stage3_patch_*.json` have `centers_dir: ""`, and
  `imagecas_inference.json` is now wired for four of its five stages but still lacks Stage 1. ADE-HTL
  additionally needs TotalSegmentator `heartchambers_highres` masks. Skip these unless actually needed.

`jobs/` holds the LSF scripts: `download_imagecas.sh`, `resample_cache.sh`,
`centerline_samples.sh`, `train_cas_net.sh`.

## Code layout

`topology/` — `paths` (dataset locations, splits, descriptors, **output tree + `code_version()`**),
`io` (loaders returning `Segmentation`/`Centerline`/`Surface`), `coords` (**frame conversions — always
use these**), `graph` (**rooted `CoronaryTree` from a centerline — the structure all topological
features are computed on**), `viz` (shared artery colours, headless matplotlib helpers).
`scripts/` — `derive_label_map.py`, `survey_topology.py` (validates the trees),
`cohort_numbers.py` (**describes them: every cohort number quoted in the thesis, printed and
written as JSON with `code_version()`** — the chapter cites it, so re-run it before submitting),
`stage_pretrained_weights.py`, `make_case_figures.py`, `make_dominance_figure.py`,
`make_tree_figure.py`, `make_anatomy_figure.py`, `make_variant_figure.py`,
`fetch_external_figures.py`.
Borrowed figures live in `figures/external/` and are fetched by `fetch_external_figures.py`,
which pulls the file, its licence and its author from the same Wikimedia Commons API response
and writes `figures/external/CREDITS.md`. **Never type an attribution by hand** — re-run the
script, and copy the credit line it generates into the caption.
`thesis/` — **thesis prose, to paste into the thesis document.** Plain LaTeX fragments with no
build system and no `\documentclass`. `clinical_background/` holds one file per section, numbered
in reading order, so a section can be worked on without touching the rest; `01_heart_anatomy.tex`
needs `graphicx`. `weekly_report_01.tex` needs nothing. `refs.bib` is shared and works with both
bibtex and biblatex; every entry is marked `[VERIFIED]`, `[BOOK]` or `[PARTIAL]`.
`thesis/wordlist.txt` is the hunspell personal dictionary (`hunspell -l -t -d en_US -p
wordlist.txt *.tex` is empty today) — domain and LaTeX words only, no prose, since a misspelling
added there is one the check can never catch again.
`.claude/skills/thesis-writing/SKILL.md` — how to write for the thesis, calibrated against two
documents in `Former_students_work/` (Korona & Baldachowski's thesis for chapters, Aida's weekly
report 1 for weekly reports) and the specific defects verified in each.
`docs_thesis/dataset_walkthrough.md` — narrated tour of the data; `docs_thesis/tree_construction.md` — the graph
model and its cohort-wide validation; `docs_thesis/hemodynamics.md` — how WSS/CFD turn the topology
into a functional endpoint, and the resolution limit that bounds it; `figures/` — their output.
Derived artifacts go to `paths.OUTPUT_ROOT` (`/dtu/blackhole/0a/224426/imagecasx_derived`, override
with `IMAGECASX_OUT`) — never to `/zhome`, never into the dataset.

PyVista is used **only as a VTK file parser**, never as a renderer: the login node has no `DISPLAY`
and off-screen VTK needs OSMesa/xvfb that may not be present. All rendering is matplotlib/Agg.
Hand-rolling a binary-VTK parser was tried and silently produced garbage — use `pv.read`.

## Research gap

Literature search (`docs_thesis/literature.md`) found **no coronary-specific paper doing outlier or
extreme-value detection on topological features** (objective 9). Vascular feature extraction and
disease-status classification are both well covered; treating a population's branching, tortuosity
and angle features as a distribution and flagging population-level outliers is not. The nearest
analogues are in a different organ (the RETA retinal benchmark) or use generic tooling without
domain adaptation. A plausible novel-contribution angle — see Open questions before leaning on it.
