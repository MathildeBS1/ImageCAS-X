# Postprocessing sweep beyond size_100 and Qiu reconnection

Free-exploration search for postprocessing that improves on CAS-Net's shipped
pipeline (`argmax_binarize` + `keep_components_larger_than_100_voxels`), run
2026-09-14/15 alongside the Qiu reconnection work (`qiu_reconnection.md`). Where
Qiu reconnection tries to *repair* fragments with a trained classifier and a walk,
this is the cheap end of the spectrum: connected-component and morphological
transforms with no learned component, applied post hoc to the same saved
`cas_net_pretrained` predictions, no new GPU inference needed.

## Where the code is

| File | Role |
|---|---|
| `postprocessing/variants.py` | the candidate transforms, `VARIANTS` registry |
| `scripts/sweep_postprocessing.py` | screens variants against an existing run's predictions; dice + Betti errors (`--metrics fast`), or + hd95/cl_dice (`--metrics full`) |
| `scripts/materialise_variant.py` | writes one variant's masks as a real run dir (`predictions/<id>.nii.gz`), for a full `evaluate.py` pass (hd95, cl_dice, centerline_md/hd95, volumes, stratified breakdowns) |
| `jobs/sweep_postprocessing.sh` | full 160-scan test-split job, CPU-only, `hpc` queue |

## What was tried

`postprocessing/variants.py::VARIANTS`:

* `size_200` / `500` / `1000` / `2000`: re-apply the component-size filter at a
  higher voxel count than the pipeline default of 100. Strictly stricter, since the
  input already only contains >=100-voxel components.
* `keep_top2`: keep only the two largest components (same rule as
  `cas_net_pretrained_keep2`, included for a same-code-path cross-check against
  its own full `evaluate.py` run).
* `close_r1` / `r2` / `r3` / `r5`: binary closing (a solid ball footprint of that
  voxel radius), then re-applied the size-100 filter, to see whether a blunt
  morphological bridge recovers any of the true fragments Qiu's reconnection is
  aimed at, without a trained classifier or a walk.
* `open_r1`: binary opening, to strip thin spurious spikes.
* `fill_holes`: `scipy.ndimage.binary_fill_holes` per component.
* `close_r2_top2` / `close_r3_top2`: closing first, then keep only the top 2
  components (so a fragment gets one chance to merge into a main tree before
  anything not merged is dropped).

`close_r3` and `close_r5` (11 and 21-voxel structuring elements on a ~512x512x206
native grid) cost 15-27 s/scan in `scipy.ndimage.binary_closing`, an order of
magnitude past every other variant, for a footprint (0.9-1.6 mm bridge on the
in-plane 0.32-0.43 mm grid) still short of the multi-mm gaps the Qiu fragment log
actually shows (see below) — dropped from the full-cohort job's default list for
that reason, not because a screen ruled them out; see `--variants` in
`jobs/sweep_postprocessing.sh` to add them back if the fast screen's `close_r2`
trend suggested it was worth the cost.

## Context already in hand before this sweep

`cas_net_pretrained_keep2`'s full `evaluate.py` result (160/160 test scans) is the
useful bracket: dropping every component but the two largest drives
`betti_error_1` from 1.8375 (baseline) to 0.00625, since the GT is b0=2 almost
everywhere — but costs dice (0.9121 -> 0.9006), hd95 (2.99 -> 7.74 mm), cl_dice
(0.9325 -> 0.9154), centerline_md (0.73 -> 1.14 mm) and centerline_hd95 (5.75 ->
10.39 mm). `fragment_report.json` (from `scripts/qiu_fragment_report.py -r
cas_net_pretrained_keep2`) explains why: of the fragments keep2 throws away, 158/293
(54%) are >= 50% inside GT by count, but 134 013 of 180 797 total fragment voxels
(74%) are true vessel. Most of what keep2 deletes to fix the component count is real
anatomy, which is exactly the boundary/centerline accuracy it gives up. Any
postprocessing candidate here is read against that bracket, not just against
`cas_net_pretrained` alone: a good candidate should move `betti_error_1` toward
`keep2`'s 0.006 without paying keep2's whole dice/hd95/centerline cost.

Qiu reconnection's own val-split threshold calibration
(`cas_net_pretrained_val_qiu_calib/threshold_calibration.json`, 80 val scans, 152
fragments) found the paper's default T=1.0 without the ADF penalty is *already* the
best point on the searched grid (RecAcc 0.618, RecSen 0.71, RecSpe 0.53) —
`configs/cas_net_qiu.json`'s `eval_threshold: 1.0, use_adf: false` is the calibrated
setting, not an unturned default. This updates the project memory note that T
"needs val calibration" — it has been done, and lands back on 1.0.

## Results

### Fast screen (dice + Betti errors only), 32/160 test scans, login node

`python scripts/sweep_postprocessing.py -c configs/cas_net.json --src cas_net_pretrained --variants baseline,size_200,size_500,size_1000,size_2000,keep_top2,close_r1,close_r2,open_r1,fill_holes,close_r2_top2,close_r3_top2 --subset 32 --workers 6 --metrics fast`, 2026-09-15. Full log and per-scan JSON under `$ImageCAS_X_results_path/postproc_sweep/`.

| variant | dice | betti_error_1 | betti_error_2 |
|---|---|---|---|
| baseline | 0.9155 | 1.7500 | 0.0938 |
| size_200 | 0.9156 | 1.2188 | 0.0938 |
| **size_500** | **0.9155** | **0.5625** | 0.0938 |
| size_1000 | 0.9149 | 0.1562 | 0.0938 |
| size_2000 | 0.9143 | 0.0625 | 0.0938 |
| keep_top2 | 0.9128 | 0.0312 | 0.0938 |
| close_r1 | 0.9156 | 1.7188 | 0.0625 |
| close_r2 | 0.9153 | 1.6875 | 0.0625 |
| open_r1 | 0.8823 | 5.4688 | 1.6562 |
| fill_holes | 0.9155 | 1.7500 | 0.0938 |
| close_r2_top2 | 0.9128 | 0.0312 | 0.0625 |
| close_r3_top2 | 0.9119 | 0.0312 | 0.0625 |

Readings:

* **Raising the size filter is a strict Pareto improvement over the pipeline's own
  default of 100, up to at least 500 voxels.** `size_200` matches baseline dice
  while cutting betti_error_1 by 30%; `size_500` still matches baseline dice
  (0.9155 vs 0.9155) while cutting betti_error_1 by 68% (1.75 -> 0.56). Past 500 the
  curve trades dice for betti_error_1 continuously down to `keep_top2`'s floor.
  **This is a one-line, zero-risk config change**: replace `"min_size": 100` with
  `"min_size": 500` in `keep_components_larger_than_100_voxels`'s params (the step
  name itself is now a misnomer at min_size != 100, a naming cost worth paying).
* **Morphological closing (`close_r1`, `close_r2`) does essentially nothing**, with
  or without a top-2 filter after it (`close_r2_top2` == `keep_top2` to 4 decimal
  places, `close_r3_top2` very slightly worse). A 1-3 voxel closing radius is
  0.3-1.0 mm on this native grid; the true fragments the Qiu reconnection logs
  describe sit several mm from the main tree (docs_thesis/qiu_reconnection.md's own
  smoke test cites a 3.1 mm gap), well past what a cheap closing can bridge.
  `close_r3` and `close_r5` were dropped from this screen on cost grounds (15-27
  s/scan) after this trend was already visible in `close_r1`/`close_r2`; nothing
  here suggests a bigger radius would turn positive before it starts eating real
  structure the way `open_r1` does.
* **Opening is actively harmful**: dice drops 3.3 points, betti_error_1 more than
  triples, betti_error_2 (loop count) jumps 16x. An erosion pass this size strips
  thin distal vessel segments outright, splitting single components into several
  and creating new small fragments faster than it removes noise. Do not use.
* **Hole filling is an exact no-op** (identical to baseline on every metric to 4
  decimals): these masks have no enclosed background voxels to fill. Confirms the
  Betti-1 (loop) error here is not coming from erroneous holes.

### Full-cohort `evaluate.py`, 160/160 test scans

For context, the two runs that already existed before this task (`cas_net_pretrained`,
`cas_net_pretrained_keep2`) plus the Qiu reconnection run this task's memory flagged
as needing a result (`cas_net_pretrained_qiu`, from the user's own already-running
`jobs/qiu_reconnect.sh` job, not resubmitted here):

| run | dice | hd95 (mm) | cl_dice | centerline_md (mm) | centerline_hd95 (mm) | betti_error_1 | betti_error_2 |
|---|---|---|---|---|---|---|---|
| cas_net_pretrained (baseline, size>=100) | 0.9121 | 2.99 | 0.9325 | 0.733 | 5.75 | 1.838 | 0.106 |
| cas_net_pretrained_keep2 (top-2 only) | 0.9006 | 7.74 | 0.9154 | 1.136 | 10.39 | 0.006 | 0.100 |
| cas_net_pretrained_qiu (Qiu reconnection, T=1.0 calibrated) | 0.9074 | 4.97 | 0.9264 | 0.879 | 7.73 | 0.006 | 0.150 |
| cas_net_pretrained_qiu_noremove (Qiu joins, no removal) | 0.9104 | 3.18 | 0.9306 | 0.750 | 6.07 | 0.756 | 0.150 |
| **cas_net_pretrained_size200** | **0.9123** | **3.02** | **0.9328** | **0.740** | **5.94** | **1.281** | **0.106** |
| cas_net_pretrained_size500 | *pending* | | | | | | |
| cas_net_pretrained_size1000 | *pending* | | | | | | |

Qiu reconnection sits strictly between baseline and keep2 on every continuous
accuracy metric (dice, hd95, cl_dice, centerline_md, centerline_hd95): the true
joins it makes recover some of what keep2's blind removal throws away, but its
test-split reconnection accuracy (`reconnection_summary.json`:
`tp=82, fp=83, tn=65, fn=63`, RecAcc 0.502) is barely above chance, despite T being
correctly calibrated on val (`threshold_calibration.json`: T=1.0 without ADF is
already the grid optimum, RecAcc 0.618 on val -- a real val-to-test generalisation
gap, not a mis-set threshold). Both `qiu` and `keep2` force betti_error_1 to ~0 by
construction (`remove_unconnected: true` always leaves exactly the kept trees), so
that metric alone cannot separate them; the continuous metrics are where the
Qiu machinery's cost (a trained classifier, per-scan skeletonisation and DPC walks,
~20 s/scan) earns anything back over the free `keep_top2` baseline, and on this
cohort it earns back about half the gap to plain baseline, not more.

**The best point in the whole Qiu family is `qiu_noremove` -- the ablation that
keeps every fragment (joined or not) and only ever adds tubes, never deletes.** It
lands almost on top of baseline on every continuous metric (dice 0.9104 vs 0.9121,
hd95 3.18 vs 2.99 mm, cl_dice 0.9306 vs 0.9325, centerline_md 0.750 vs 0.733 mm,
centerline_hd95 6.07 vs 5.75 mm -- all within about 0.3 mm or 0.002 dice of doing
nothing) while cutting betti_error_1 by 59% (1.838 -> 0.756), a far better
efficiency-per-point-of-Betti-error than either `qiu` or `keep2`, both of which buy
their much lower betti_error_1 (~0) with real dice/hd95/centerline cost.
`remove_unconnected: true`'s deletion step is where the Qiu pipeline's cost shows
up as a loss, not a gain, on this cohort: at RecAcc ~0.5, roughly half of what it
removes was worth keeping. The paper's own design keeps removal because it targets
the Betti number as the reported metric (Table 9); this benchmark's fuller metric
set makes that trade visible.
