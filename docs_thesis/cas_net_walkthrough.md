# Training CAS-Net from scratch — a walkthrough

Thesis objective 5: *implement, validate and document a state-of-the-art coronary
segmentation framework from CT.*

This document has two halves. **Part 1** is how the framework works, one section per stage,
with the `file:line` to read each claim at. **Part 2** is the sequence of commands to
actually run, with what to expect from each. Read Part 1 once; work from Part 2.

Everything here was checked against the code on branch `tortuosity_focus`. Where
`ARCHITECTURE.md` and this document disagree, this one was verified more recently — the
differences are listed in [Corrections](#corrections-to-inherited-notes).

---

## 0. Orientation: three programs, one contract

```
train.py     -c configs/cas_net.json  ──>  <run_dir>/cas_net_best.pt
inference.py -c configs/cas_net.json -r <run_dir>  ──>  <run_dir>/predictions/<id>.nii.gz
evaluate.py  -c configs/cas_net.json -r <run_dir>  ──>  <run_dir>/cas_net_results.json
```

The separation is load-bearing rather than cosmetic. `evaluate.py` **never loads a model**
— it scores whatever NIfTI files sit in `predictions/`. That is how nnU-Net (a separate
training framework), TotalSegmentator (an external pretrained tool) and a second human
analyst's annotations all enter the same benchmark table on identical footing. It also
means you can re-score a run without a GPU, and that a bug in your training cannot
contaminate the scorer.

CAS-Net is the method to learn on: it is the paper's best performer (DSC 91.2) *and* its
cheapest (6.8 M parameters, 15.5 s/scan), and it is a single-stage method, so nothing is
hidden behind a cascade of five checkpoints the way the ImageCAS baseline is.

---

# Part 1 — how it works

## 1. Config: how a run is specified

`utils/config.py` is the spine. Two ideas.

**Every method config is merged over `configs/pipeline.json`.**
`BenchmarkConfig.from_json` (`utils/config.py:180-193`) loads the method JSON, finds
`pipeline.json` in the same directory, and deep-merges the method's keys on top.
`pipeline.json` is the *fairness contract* — it fixes preprocessing, the 8 augmentations,
the optimizer, the 1000-epoch schedule, postprocessing and the 11 metrics, so that every
method in the benchmark table differs only where it means to. `configs/cas_net.json` is 39
lines because everything else is inherited.

**The merge rule that will catch you out:** `_deep_merge` (`:19-28`) merges nested dicts
key by key, but **replaces lists outright**. So `cas_net.json` declaring

```json
"postprocessing": { "steps": ["argmax_binarize", "keep_components_larger_than_100_voxels"] }
```

does not append to pipeline.json's `["threshold", "keep_components_larger_than_100_voxels"]`
— it discards it. (pipeline.json's `postprocessing.params.threshold` still survives the
merge, because *that* is a dict; it just sits there inert, since no step reads it.)

A second trap: `_pick` (`:13-16`) filters each config block down to the fields its
dataclass declares and **silently drops the rest**. That is what lets a `description` key
and inline comments live in a config harmlessly — but it also means a misspelled
`"batch_sze": 12` is not an error. It is ignored, and you train at the default.

Two environment variables override the JSON *after* the merge (`:9-10`, `:135-140`):
`ImageCAS_X_data_path` → `data.data_root`, `ImageCAS_X_results_path` → `results_root`.
These are the only two paths any config needs, which is why `env.sh` sets exactly them.

Splits come from `<filelist_dir>/{train,val,test}.txt`, and every ID listed in
`exclude.txt` is dropped from all three (`_load_filelist_ids`, `:162-178`). You get
560/80/160 from the 800 usable cases.

**Effective CAS-Net config after the merge:**

| | |
|---|---|
| input | `random_crop`, patch `[128,160,160]`, `min_fg_fraction` 0.5 |
| preprocessing | `resample` (0.5 mm), `normalise_to_range` (HU [-200,1000] → [0,1]) |
| augmentation | the 8 nnU-Net defaults |
| model | `cas_net`, 2 output channels, 1 input channel, `checkpoint: null` |
| loss | `multiclass_dice` |
| training | batch 5, lr 1e-4, adam, wd 1e-8, poly LR power 0.9, **1000 epochs**, 250 train + 50 val iters/epoch, 14 workers, best-on-dice, **`amp` false**, **`cudnn_benchmark` false** |
| postprocessing | `argmax_binarize`, `keep_components_larger_than_100_voxels` |

## 2. Preprocessing, and why the step list lies

Registry: `preprocessing/pipeline.py:6-12` → `Resample`, `ResampleToShape`,
`NormaliseToRange`, `DilateMask` (`preprocessing/steps.py:6, 52, 127, 98`).

Every method wants the volume at 0.5 mm isotropic. Doing that inside `__getitem__` would
dominate training time, so it is done once, offline, by
`utils/offline_resample_images_to_disk.py`, writing `.npy` arrays to `volumes_resampled/`
and `segmentations_resampled/`. **This has already been run for all 800 cases** — see
Part 2, Step 0.

Now the subtle part. `dataloading/base_dataset.py:29` sets

```python
self.use_resampled_cache = "resample" in preprocessing.steps
```

The presence of `"resample"` in the config is what makes the loader read the *cache*, and
then `_run_preprocessing` (`:127-146`) **skips the `Resample` step at runtime** because the
cache already has it baked in. So the only preprocessing that actually executes per sample
is the HU window. `preprocessing.steps` is an honest description of what has happened to
the data by the time the model sees it — not a list of operations performed now.

The consequence for you: if you ever add a preprocessing step, decide whether it belongs in
the cache builder too. And if `volumes_resampled/` were missing, `np.load` would raise —
the cache is never built lazily.

## 3. Dataloading: the foreground quota

`input_type: "random_crop"` → `RandomCropDataset` (`dataloading/random_crop_dataset.py:13`)
via the registry at `dataloading/factory.py:22-27`. Arrays are opened `mmap_mode="r"`, so a
128 MB volume costs almost nothing until a crop touches it.

Coronary arteries occupy roughly **0.1–0.2 % of a 128×160×160 crop** (measured, below).
Under uniform sampling most crops would contain no vessel at all and the network would
learn to predict all-background. So:

`ForegroundQuotaBatchSampler` (`:115-134`) yields, per batch, a list of *booleans* rather
than indices. This is the thing that surprises everyone reading this file:

> `idx` is NOT a scan selector here — it carries a bool from `ForegroundQuotaBatchSampler`
> saying whether this batch slot must land on foreground.

`__getitem__` (`:75-112`) therefore picks a **random scan** with `random.choice`, ignoring
`idx` except as that flag. With `batch_size 5` and `min_fg_fraction 0.5`,
`ceil(5 × 0.5) = 3` slots per batch are required to contain vessel; the flags are shuffled
with a seeded RNG.

`_sample_crop_with_fg_quota` (`:55-73`) then draws a uniform origin and, if the slot
requires foreground, retries up to 20 times — cropping **only the cheap uint8 mask** on
each try, and cropping the expensive mmap-backed volume once, at the accepted origin. Crops
that run past the edge are zero-padded (`_crop_at`, `:42-53`).

Two more things this dataset does that matter:

- The mask is **binarised** (`base_dataset.py`, `_binarise_mask`). The cache stores the
  14-label segmentation, but CAS-Net is trained on vessel-vs-background. The label
  semantics matter for your topology work, not for this model.
- `_load_centerlines` (`:110`) reads both centerline VTKs for **every sample** — and then
  `_collate_fn` (`factory.py:13-20`) pops them and `_batch_targets` (`train.py`) skips
  them. For CAS-Net this is pure overhead. Leave it alone for fidelity unless the timing
  run shows the loader is your bottleneck.

Because train and val are "endless" (a fixed 250 and 50 batches per epoch drawn with
replacement), **the same scan can appear twice in one batch.** That is expected, not a bug.

## 4. Augmentation

Registry `augmentation/pipeline.py:10-19` → `augmentation/steps.py`. CAS-Net declares no
`augmentation` block, so it inherits all 8 nnU-Net defaults from pipeline.json:

| step | p | range |
|---|---|---|
| `random_flip` | 0.5 per axis | **axes [0,1] only** |
| `gaussian_noise` | 0.1 | variance 0–0.01 |
| `gaussian_blur` | 0.2 | σ 0.5–1.0 |
| `multiplicative_brightness` | 0.15 | 0.75–1.25 |
| `contrast` | 0.15 | 0.75–1.25 |
| `simulate_low_resolution` | 0.25 | zoom 0.5–1.0 |
| `gamma_invert` | 0.1 | γ 0.7–1.5 |
| `gamma` | 0.3 | γ 0.7–1.5 |

Applied **after** cropping and **only on the train split** (`random_crop_dataset.py:98-101`;
`train.py` passes `augmentation=None` for val). Note `random_flip` touches axes 0 and 1 but
never 2 — which is exactly why inference mirrors X and Y and leaves Z alone. Train-time and
test-time symmetry assumptions have to match.

## 5. The model

`models/cas_net.py`, registered as `cas_net` by the `@register_model` decorator at `:174`.
`models/registry.py:22-41` instantiates it with `config.model.params` and then loads
`config.model.checkpoint` **if it is set** — which is why a checkpoint path must never
appear in a training config.

Four blocks, following Dong et al. (MedIA 2023):

- **`ResEncoder3d`** (`:41`) — residual encoder, 16→32→64→128→256, max-pool between stages.
- **`SAFE`** (`:111`), scale-aware feature extraction, the bottleneck at 256 channels. Four
  gated dilated-conv groups at rates 1/2/3/5 give receptive fields matched to different
  vessel calibres, then a non-local attention block whose Q/K/V convolutions are
  **anisotropic** — (3,1,1), (1,3,1), (1,1,3) — so long-range context is gathered along
  each axis separately. This is the "multi-attention multi-scale" of the paper's title, and
  it is what a coronary tree needs: the LM is an order of magnitude wider than a distal
  diagonal.
- **`AGFF`** (`:80`) — attention-gated skip connections. The decoder feature gates the
  encoder feature before they are fused, so the skip carries only what the decoder is
  currently looking for.
- **`MSFA`** (`:146`) — multi-scale feature aggregation head over all four decoder levels.

```python
def forward(self, x) -> dict:
    ...
    return {"logits": self.msfa([d4, d3, d2, d1])}    # :225
```

**A single-key dict, one head, `[B, 2, X, Y, Z]`.** No deep supervision, no centerline
branch, no auxiliary outputs. The reference implementation's final `Sigmoid` is
*deliberately omitted* (`:170`): the framework contract is that models return raw logits and
all activation happens in postprocessing, so that the shared threshold path works for every
method. `MSFA.out_conv` hardcodes 2 output channels — the `classes: 2` config parameter is
accepted only to match the reference signature and is unused (`:180-181`).

## 6. The loss

`multiclass_dice` → `MulticlassSoftmaxDiceLoss` (`losses/common.py:71-91`), selected in
`losses/factory.py:12` where the comment simply reads `# CAS-Net`.

Softmax over the channel dimension, one-hot the `long` target to 2 channels, then per-class
`1 − (2·Σpt + s)/(Σpᵖ + Σtᵖ + s)` with `smooth=1.0`, `p=2`, averaged over **both classes,
background included**. Averaging in the background class is unusual for a 0.1 %-foreground
problem — background Dice is ~1.0 almost immediately and contributes little gradient — but
it is what the reference does, and matching it is the point of a benchmark.

Note there is **no topology-aware loss anywhere in this framework.** clDice exists only as
an evaluation metric. If week 5's topology-aware fine-tuning happens, that is a new loss in
`losses/`, registered in the factory — the framework has the extension point, it just has
nothing in it.

## 7. The training loop

`train.py:163`. Read it top to bottom; it is 400 lines and there is no framework magic.

1. `seed_everything()` — `SEED = 42`, hard-coded in `utils/seeding.py` and deliberately not
   configurable, with `cudnn.deterministic=True` and `benchmark=False`. Any two runs of a
   config are therefore directly comparable, including against the published numbers.
2. A timestamped run dir `<results_root>/cas_net_<YYYY-MM-DD-HH-MM-SS-ffffff>`, and `_Tee`
   (`:35`) mirrors all stdout into `<run_dir>/log.txt`.
3. Build order (`:190-199`): preprocessing → augmentation (train only) → train loader → val
   loader → model → loss → optimizer → scheduler.
4. Per batch: forward under `torch.autocast`, then **cast the logits back to fp32 before the
   loss** (`_logits_to_fp32`, `:129-144`). bf16's 8-bit mantissa is too coarse for a Dice
   sum over ~10⁶ voxels. There is no `GradScaler`, because bf16 has fp32's exponent range
   and cannot underflow the way fp16 would. **For CAS-Net `amp` is false, so this is all
   fp32 anyway** — the machinery matters only if you turn amp on.
5. Validate with a pseudo-Dice that **skips GT patches with no foreground** (`_dice_score`,
   `:294`) — otherwise an empty patch scores a meaningless 0 or 1 and swamps the average.
6. Save `cas_net_best.pt` when val Dice improves (`_is_better`, `:92`; NaN never replaces
   the best). Redraw `training_curves.png` every epoch.

**An "epoch" here is a fixed number of iterations, not a pass over the data** — 250 train,
50 val (`utils/config.py:81-84`). This is what makes the schedule comparable across methods
whose datasets have wildly different lengths: a crop dataset is effectively infinite, a
volume dataset has 560 items. So the full schedule is **1000 × 250 = 250 000 training
iterations**, and the poly LR decays over `total_iters = epochs` (`:84-88`).

### `--resume` — ours, not upstream

Upstream `train.py` saved only a bare `state_dict`, so a run killed by the walltime
restarted from zero. Since 250 000 fp32 iterations cannot fit one job, this fork adds:

- `<method>_last.pt`, written **every epoch**: model + optimizer + scheduler + epoch +
  curve history, via a temp file and `os.replace`, so a kill mid-write leaves the previous
  state intact rather than a truncated file.
- `--resume RUN_DIR`, which continues in the original folder and **appends** to `log.txt`
  instead of truncating it, so one run stays one log across many submitted jobs.
- `<method>_best.pt` deliberately stays a **bare `state_dict`**, because `inference.py` and
  `BaseLumenModel.load_weights` (`models/base_model.py:15-17`) do a strict
  `load_state_dict` and would break on a wrapped dict.

This is a deliberate modification to an upstream file. Keep it small so the fork stays
mergeable against `git@github.com:kitbransby/ImageCAS-X.git`.

## 8. Inference

`inference.py`. The stable contract is one function —
`run_inference(model, volume, cfg, device, scan_id)` (`:253`): full preprocessed volume in,
full-volume logits on CPU out.

`build_eval_dataloader` (`factory.py:108-129`) always yields **whole volumes at batch size
1**, whatever the training `input_type`. A model trained on crops must still be scored on
whole scans, so the tiling happens inside inference rather than in the loader.

For CAS-Net that means `patch_stitch_inference` (`:70-122`):

- tile the volume with **50 % overlap** (`stride = round(128 × 0.5)` etc.)
- run tiles in batches of 6
- blend with a **Gaussian weight map**, `sigma_scale = 0.125` (nnU-Net's value), so tile
  seams do not show as ridges in the probability field
- accumulate `logits × w`, divide by the summed weights

Wrapped around that, **mirror test-time augmentation** over X and Y only (`_MIRROR_AXES =
(2,3)`, `:28`) — 4 forward passes over the whole tiling, averaged. Z is excluded because
training only ever flipped axes 0 and 1. This is where most of your inference time goes.

Then per scan (`predict()`, `:360`):

1. `torch.sigmoid(logits)` (`:500`) — **before** resampling, so the continuous probability
   field survives the change of resolution rather than a hard-edged binary mask being
   interpolated.
2. resample the probabilities back to the **original scan geometry**, per channel, linearly
   (`:294`), using the original CT's header — not the GT mask's.
3. run the postprocessing pipeline
4. write `<run_dir>/predictions/<scan_id>.nii.gz`

`model.checkpoint` is `null` in `cas_net.json`, so `:398-406` defaults it to
`<run_dir>/cas_net_best.pt` — exactly what `train.py:255` wrote. That is the whole reason
the pretrained weights were staged as run dirs: no config edit is needed to score them.

Predictions for non-test splits go to `predictions_<split>/`, so a cascade's earlier stage
can never overwrite the test set. **Inference resumes by default**: scans already on disk
are skipped unless `--overwrite`.

`--save-probs` carries an explicit warning that it is *not* meaningful for CAS-Net, whose
two channels are not "lumen" and "not lumen" in the way a single-channel sigmoid would be.

## 9. Postprocessing and evaluation

Registry `postprocessing/pipeline.py:6-13`. CAS-Net runs two steps, in order:

- **`argmax_binarize`** (`steps.py:46`, commented `# CAS-Net`) — not `threshold`. CAS-Net's
  two channels are independent and do not sum to 1, so cutting either at 0.5 is not the
  same as taking the larger. This is precisely the override that made
  `postprocessing.steps` replace pipeline.json's list.
- **`keep_components_larger_than_100_voxels`** (`:23`) — size-based, deliberately *not*
  largest-component. The left and right coronary trees are two separate components; a
  largest-component filter would delete one of them.

`evaluate.py` never builds a model (`:8-9`). Per scan, in a worker process, it loads the
prediction (which carries the original volume's header), resamples the **GT onto the
prediction's grid** with nearest-neighbour, and computes metrics — so every distance is in
true millimetres and every volume in true millilitres. Each worker rebuilds its own
`BenchmarkConfig` from the path (`:126-128`) so the config never has to be picklable.

The 11 metrics for CAS-Net: `dice`, `hd95`, `cl_dice`, `centerline_md`, `centerline_hd95`,
`volume_{pred,gt,mad,bias}_ml`, `betti_error_1`, `betti_error_2`. Plus `local_dice` where
`centerline_samples/<id>.npz` exists.

Output is `<run_dir>/cas_net_results.json` with `per_scan`, `summary`, `coverage`
(including `missing_prediction_ids` — check this), `summary_by_group` stratified by Image
Quality / Dominance / Disease, and `summary_by_point_group`; plus `point_metrics.csv`.

**ASSD is not implemented.** `utils/metrics.py` has no symmetric surface distance, so the
paper's ASSD 0.73 mm column cannot be reproduced by this code. `centerline_md` — mean
predicted-skeleton-to-GT-centerline distance — is *not* the same quantity and must not be
reported as if it were.

---

# Part 2 — running it

All commands assume `source env.sh` first and the repo root as working directory.
**Never run training or inference on the login node**; it has no GPU.

## Step 0 — confirm the state of the data

The expensive precompute has already been done. Confirm rather than assume:

```bash
source env.sh
ls $ImageCAS_X_data_path/volumes_resampled | wc -l        # expect 800
ls $ImageCAS_X_data_path/segmentations_resampled | wc -l  # expect 800
du -sh $ImageCAS_X_data_path/volumes_resampled            # expect ~102G
wc -l $ImageCAS_X_data_path/filelist/*.txt                # 560 / 80 / 160 / 200
```

If those hold, **there is no resampling job to run.** If `volumes_resampled/` were ever
lost, rebuild it with
`python -m utils.offline_resample_images_to_disk -c configs/cas_net.json --workers 8`
as a CPU job on the `hpc` queue — budget 100–150 GB and several hours.

`centerline_samples/` holds 160 `.npz`, the test split only. That is correct and
sufficient: only `evaluate.py` reads them.

## Step 1 — see the real pipeline, on the login node

```bash
python -m utils.verify_dataloaders -c configs/cas_net.json \
    --n-batches 1 --num-workers 2 \
    --out-dir /dtu/blackhole/0a/224426/imagecasx_derived/dataloader_check
```

CPU only, about a minute. Keep `--num-workers` small — the login node is shared, and the
config's 14 would be antisocial. Send `--out-dir` to blackhole; the default writes into the
repo, and `/zhome` is at 25.9/30 GB.

Real output from this repo:

```
[train batch 0] 117: vol shape=(128, 160, 160) min=0.0000 max=0.8605 mean=0.2880 | mask fg_frac=0.00202
[train batch 0] 4:   vol shape=(128, 160, 160) min=0.0000 max=0.9892 mean=0.2424 | mask fg_frac=0.00103
[train batch 0] 587: vol shape=(128, 160, 160) min=0.0000 max=1.0000 mean=0.4019 | mask fg_frac=0.00187
[train batch 0] 50:  vol shape=(128, 160, 160) min=0.0123 max=1.0000 mean=0.1744 | mask fg_frac=0.00098
[train batch 0] 681: vol shape=(128, 160, 160) min=0.0000 max=0.9305 mean=0.2365 | mask fg_frac=0.00145
```

What to check, and what it teaches:

- **shape is exactly (128,160,160)** — the crop is doing what the config says.
- **min/max inside [0,1]** — the HU window ran. A max of 1.0000 means that crop contained
  something at or above 1000 HU: contrast-filled lumen, calcium, or metal.
- **`fg_frac` around 0.001–0.002** — vessels are **0.1–0.2 %** of a crop. This single number
  justifies the whole foreground-quota design, and explains why validation uses a
  pseudo-Dice that skips empty patches.
- **all five slots have foreground here**, though only three were *required* to. At
  128×160×160 the crop is large enough that a uniform draw often catches a vessel anyway;
  the quota matters much more for the small-patch methods.
- **a scan id may repeat within a batch** (e.g. `961` twice in the val batch) — train and
  val sample with replacement, by design.

The PNGs show the middle slice with the mask boundary overlaid. Expect recognisable
cardiac CT with tiny bright vessel cross-sections. Some crops will show noise or a bright
band — that is either the augmentation pipeline or genuine metal artifact, and both are
supposed to be there. If a crop looks like static, or the mask overlay sits nowhere near a
bright vessel, stop and investigate before spending GPU time.

## Step 2 — rehearse inference and evaluation on the delivered weights

Do this **before** training. It takes hours instead of weeks, it teaches stages 8 and 9,
and it produces the reference numbers your own run will be judged against. If it fails, the
problem is your environment — and you have found that out before burning a week of queue.

```bash
bsub -env "all, RUN_DIR=cas_net_pretrained" < jobs/infer_eval_cas_net.sh
```

`cas_net_pretrained/cas_net_best.pt` is already staged as a symlink to the delivered
weights, and `model.checkpoint: null` makes `inference.py` find it with no config change.

160 test scans, each tiled at 50 % overlap and run 4× for mirror TTA. Expect a few hours.

Then check `$ImageCAS_X_results_path/cas_net_pretrained/cas_net_results.json`:

```bash
python -c "
import json,sys
r=json.load(open(sys.argv[1]))
print(r['coverage'])
for k,v in sorted(r['summary'].items()): print(f'{k:24s} {v}')
" $ImageCAS_X_results_path/cas_net_pretrained/cas_net_results.json
```

Against the paper's Table 2 (160 test cases):

| metric | published |
|---|---|
| DSC | 91.2 |
| clDice | 93.3 |
| HD95 | 2.99 mm |
| cl-HD95 | 5.75 mm |
| Betti-1 error | 1.9 |
| *(ASSD 0.73 mm)* | *not computable here — no ASSD metric exists* |

`coverage.n_missing_predictions` must be **0 of 160**. For context: inter-observer agreement
is DSC 92.8 and the original ImageCAS labels score 41.8 against these labels — so 91.2 is
close to, but significantly below, the human ceiling, and no automated method in the paper
reaches it.

## Step 3 — the timing run

Never guess the schedule. Measure it.

```bash
bsub -q gpuh100 -W 4:00 -env "all, CONFIG=configs/cas_net_smoke.json" \
     < jobs/train_cas_net.sh
```

`configs/cas_net_smoke.json` is identical to `cas_net.json` except `epochs: 5` and
`method_name: "cas_net_smoke"`. The distinct method name keeps its run dir and its
checkpoints separate, so a 5-epoch model can never be mistaken for a trained one.

Command-line `bsub` options override the `#BSUB` lines in the script, which is how this
lands on the shorter, far less contended `gpuh100` queue instead of `gpua100`.

Read out of `logs/cas_net_<jobid>.out` and `<run_dir>/log.txt`:

- **the `nvidia-smi` block at the top** — confirm you got an 80 GB card.
- **`time=` on each epoch line.** Divide by 300 (250 train + 50 val iterations) for a rough
  per-iteration cost. Ignore epoch 1; it pays for cuDNN warm-up and cold page cache.
- **whether it OOMs at all.** Batch 5 at 128×160×160 in fp32 is the single riskiest thing
  about this configuration.
- **whether `dice=` moves.** In 5 epochs it will be low, but it should not be identically
  zero or NaN.

The epoch line looks like:

```
Epoch 3/5  train=0.5123  val=0.4980  dice=0.2114  lr=9.46e-05  time=8m 12s
```

## Step 4 — size the real run

```
wall clock ≈ epochs × 300 iterations × (your measured s/iter)
```

For the full published schedule, `epochs = 1000`. At 2 s/iter that is ~167 hours; at
1 s/iter, ~83 hours. Either way it exceeds the **72 h ceiling on `gpua100`** (and the 24 h
ceiling everywhere else), so plan on chained jobs: `ceil(total_hours / 70)` submissions,
leaving margin for the tail epoch.

If that is more queue time than the project can afford, shorten the schedule rather than
quietly changing other things. **Record whatever you choose.** The benchmark's fairness
claim rests on matched settings, and any comparison to Table 2 must state the deviation.

Two speedups worth considering, in order of safety:

- **`"cudnn_benchmark": true`** — free, and sound here because every batch has the same
  fixed 128×160×160 shape. `utils/config.py:89-92` notes that with `cudnn.deterministic`
  still on, autotuning picks within the deterministic set. Low risk.
- **`"amp": true`** — a larger win in both time and memory, but it makes the run
  numerically non-identical to the published fp32 one. `train.py` already casts logits back
  to fp32 before the loss, so the Dice sum stays accurate. Higher risk to comparability.

Put either in a **new** config, never by editing `configs/cas_net.json` in place, so the
published settings remain on disk exactly as shipped.

## Step 5 — train

```bash
bsub < jobs/train_cas_net.sh
```

Note the run dir it prints (`[train] run_dir=...`). Then queue each continuation *before*
the current job ends, so you do not lose your place in the queue:

```bash
bsub -w "ended(<jobid>)" -env "all, RUN_DIR=cas_net_2026-09-09-…" < jobs/train_cas_net.sh
```

Verifying a resume actually resumed — look for this in the appended `log.txt`:

```
[train] resumed at epoch 118/1000  best dice=0.8241
```

If instead you see `Epoch 1/1000`, the resume did not take: either `RUN_DIR` was not passed
through (`-env "all, RUN_DIR=..."`, and the `all,` matters), or `<run_dir>/cas_net_last.pt`
is missing. Stop and fix it rather than letting a second run start from zero in the same
folder.

Because `_last.pt` is written by temp-file-and-rename, a job killed mid-write leaves the
*previous* epoch's state intact. You lose at most one epoch, never the run.

Watch progress with `<run_dir>/training_curves.png`, redrawn every epoch: train and val
loss, val Dice on a twin axis, LR below.

## Step 6 — predict, score, compare

```bash
bsub -env "all, RUN_DIR=cas_net_2026-09-09-…" < jobs/infer_eval_cas_net.sh
```

If you resumed training further and re-run inference into the same run dir, pass
`OVERWRITE=1` — inference skips scans already present, so stale predictions would otherwise
survive silently.

Then compare your `cas_net_results.json` against `cas_net_pretrained`'s. Same 160 test
scans, same `SEED = 42`, same metrics, same postprocessing. Fill this in:

| | pretrained | from scratch | Δ |
|---|---|---|---|
| DSC | | | |
| clDice | | | |
| HD95 (mm) | | | |
| cl-HD95 (mm) | | | |
| Betti-1 error | | | |
| epochs trained | 1000 (published) | | |
| deviations | none | | |

A gap is not automatically a bug. Attribute it: a shortened schedule, `amp`/`cudnn_benchmark`
changes, or a different card are all legitimate causes — but they have to be named, and this
is the table the thesis reports.

---

## Troubleshooting

| Symptom | Cause |
|---|---|
| `FileNotFoundError` on a `.npy` in `volumes_resampled/` | the cache is never built lazily; run the offline resample script |
| CUDA OOM early in epoch 1 | not an 80 GB card. `-R "select[gpu80gb]"` is in the job script for this reason; check `nvidia-smi` in the log |
| `Checkpoint not found` from `inference.py` | `-r` must name the timestamped run folder, not the config |
| Resumed job restarts at epoch 1 | `RUN_DIR` not passed (`-env "all, RUN_DIR=..."`) or `<method>_last.pt` absent |
| `Cannot resume: … does not exist` | the run predates `--resume`, or `-c` names a different method than that run dir |
| Val dice is NaN every epoch | every sampled val patch was empty; check `min_fg_fraction` and the mask cache |
| A config change had no effect | `_pick` silently drops unknown keys — check the spelling against the dataclass in `utils/config.py:31-122` |
| A whole preprocessing/postprocessing list vanished | lists replace rather than merge; re-declare the full list |
| Second training run scores suspiciously well from epoch 1 | a checkpoint path was left in the method config, turning it into a fine-tune |

## Corrections to inherited notes

Verified against the code on this branch; the earlier `CLAUDE.md` was wrong on all three:

- **`utils/config.py` does not expand `${VAR}`** in checkpoint paths. There is no string
  interpolation anywhere in the config loader. Paths resolve via `data_root`/`results_root`
  and the `-r` run dir. `env.sh` still exports `ImageCAS_X_weights_path`, but no config
  reads it.
- **ASSD is not implemented**, so the published ASSD column cannot be reproduced.
- `ARCHITECTURE.md` predates the `--resume` change and describes `train.py` as taking `-c`
  only; that section is now out of date.

## Still not runnable, and why

Not needed for CAS-Net, but worth knowing before you reach for another method:

- **ImageCAS 3-stage baseline** — only four of its five checkpoints were delivered; there is
  no Stage-1 coarse model. Also needs `volumes_resampled_128/`, which does not exist here.
- **`imagecas_stage3_patch_*.json`** — `centers_dir` is empty and must be generated first.
- **ADE-HTL** — additionally needs TotalSegmentator `heartchambers_highres` masks.
- **nnU-Net** — has no model in this framework's registry by design; it runs under its own
  CLI and drops predictions into `<run_dir>/predictions/` for `evaluate.py` to score.
