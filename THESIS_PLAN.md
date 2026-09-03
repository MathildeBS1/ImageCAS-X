# Thesis next moves — topology of coronary trees, ImageCAS-X → CGPS

## Context

Kit's reply (`response.md`) resolves most of the open questions and changes several
assumptions. What we now know:

- **The cohort is CGPS** — Copenhagen General Population Study (Herlev/Østerbro) — not a
  clinical Rigshospitalet cohort. It is **population-based**, which is materially better for
  normative modelling and for population description: "normal" can be defined from a general
  population rather than from ImageCAS's stroke/TIA/PAD-selected patients.
- **No coronary segmentation ground truth exists for CGPS yet.** Medis QAngio is planned but
  usually emits only plaque volumes, not intermediate contours; Kit and Phillip are working
  on extracting them.
- **Medis will use a different protocol and likely will not annotate all branches.** This
  matters more for you than for anyone else on the project — see Traps below.
- **The project's intended pipeline is exactly the one already recommended**: label ImageCAS
  (done) → train lumen models (done) → predict on CGPS (todo). CAS-Net slots directly into
  the third step.
- **Outer vessel wall is being labelled in ImageCAS now**, to train a wall model for CGPS.
  Plaque = wall − lumen. The repo currently has **zero** support for a second surface
  (confirmed: no code hits for wall/plaque/adventitia anywhere; `save_mask` at `utils/io.py:33`
  hard-fails on 4D input). This is Kit's workstream, not yours — but it is the mechanism by
  which plaque localisation may arrive during your thesis.
- **~2000 repeat scans exist and the number is growing.** This is the most valuable fact in
  the reply and it unlocks a validation strategy that needs no annotation at all.
- **MACE outcomes exist.** Phillip has the details; ask at tomorrow's meeting.

Thesis length: 7–9 months (45–60 ECTS). You are taking on the CGPS labelling subset.

---

## The core strategic insight: two independent validations

You now have access to two validation routes that answer *different* questions, and using
both is what will make the methods chapter strong:

| | Source | n | Answers |
|---|---|---|---|
| **Accuracy** | Your + Danina's labelled CGPS subset | ~30–40 | *Am I right?* |
| **Precision** | Repeat scans of the same patient | ~2000 | *Am I consistent?* |

**The repeat-scan route is the standout opportunity.** Adult coronary *branching topology*
is essentially invariant — you do not grow new epicardial branches. So for two scans of the
same person:

- Branch count, connectivity, Strahler order → **should be identical**. Any difference is
  measurement error, full stop.
- Bifurcation angles, tortuosity → mostly stable, but genuinely drift over years and vary
  with cardiac phase.
- Lumen diameter → genuinely changes with plaque progression.

That gives you a **per-feature reproducibility coefficient at n≈2000 with zero annotation
cost**, which is worth far more than the same statistic from 30 labelled scans. It tells you
which features are stable enough to use at all, and it yields the **minimum detectable
change** — the number you must have before claiming any feature progresses over time.

Two things to control for: stratify by **scan interval** (short interval → pure measurement
noise; long interval → noise plus real change), and record **cardiac phase**, since
tortuosity differs between systole and diastole.

---

## The scientific centrepiece: baseline geometry predicts plaque development

The repeat scans do more than validate the pipeline — they let you run the design that
cross-sectional data cannot support. This should be objective 10, in place of (or alongside)
a plain MACE association.

**Baseline geometry (t₀) → plaque change (t₀ → t₁).** Geometry is measured *before* the
plaque appears, so the temporal ordering is fixed and the reverse-causation problem —
"did geometry cause plaque, or did plaque distort geometry?" — is removed by construction.

The strongest version restricts to **locations that are plaque-free at baseline**: measure
local geometry where there is no plaque at t₀, then ask whether plaque appears there by t₁.
There was no plaque to distort the baseline geometry, so the objection cannot be raised.
And because each patient contributes many locations — some that develop plaque, some that
don't — **patient-level confounders (age, lipids, diabetes, smoking, statins) are controlled
automatically**. Each patient is their own control.

This also dissolves the statistical-power problem. Events are no longer patient-level MACE
(~25 events, supporting 2–3 predictors) but **location-level plaque onset**: ~2000 repeat
pairs × 10–20 analysable locations each is tens of thousands of observations. Locations
within a patient are correlated, so this needs mixed-effects models or clustered standard
errors rather than naive regression — but the effective power is an order of magnitude
beyond a patient-level analysis.

**The two repeat-scan uses chain together.** The reproducibility study is not a side quest;
it is the prerequisite:

1. Short-interval repeats → measurement noise → **minimum detectable change** per feature
2. Long-interval repeats → change exceeding MDC → **real progression**, not noise
3. Baseline geometry → predicts that progression

Without step 1 you cannot defend step 2, and a reviewer will ask.

**What it depends on:**

- **Plaque quantified at both timepoints.** Note the reframe: Kit calls Medis's plaque-volume
  output "not that useful for us" — true for *lumen segmentation*, but plaque volume per
  segment is precisely the **outcome variable** this design needs. Ask whether Medis output
  exists (or is planned) for both rounds, and at what granularity — per patient, per vessel,
  or per segment. Per-segment is what makes the within-patient design work.
- **Spatial correspondence between t₀ and t₁.** Two scans give two independent segmentations
  and two independent skeletons; you must match locations across them. This is real
  methodological work and a genuine contribution — but note it is *far* more tractable than
  cross-patient tree matching, because it is the same tree imaged twice, with the same
  branching pattern. Match by branch correspondence plus arc length from the ostium.
- **A long enough interval.** Plaque progression is slow; under ~2 years you may see nothing
  above the noise floor.
- **Same scanner and protocol at both timepoints**, or "progression" is partly acquisition
  drift.

---

## Start now — unblocked, and must come first regardless

You have no data locally (`ImageCAS_X_data_path` unset) and CGPS access is pending. None of
the following depends on CGPS, and all of it must happen *before* deployment anyway, because
you cannot validate a pipeline on a cohort with no ground truth.

1. **Get ImageCAS-X running.** Download volumes, labels and pretrained CAS-Net weights; set
   the two env vars; build the 0.5 mm cache; reproduce the published numbers on ~10 test
   scans (expect DSC ~91.2, clDice ~93.3). `utils/verify_dataloaders.py` renders batches
   through the real pipeline as a sanity check.
2. **Build the `topology/` package** against ImageCAS-X ground truth, which is excellent and
   already carries a labelled tree — points, line cells, `segment_label`, `start_points`,
   `end_points`, `branch_points`. Reuse rather than rewrite:
   - `_read_centerline` (`utils/precompute_centerline_samples.py:47`)
   - `_adjacency` (`:91`) — GT path only; it consumes VTK line cells
   - **`_traverse` (`:104`) — reusable verbatim for both GT and predicted trees**; takes
     `(points, adj, roots)`, returns hop depth and true arc length
   - `_radius_field` (`:153`) and `_GTGeometry` (`:167`) for local radius and mask snapping
   - `_extract_skeleton` / `_remove_small_components`
     (`models/imagecas_baseline/model.py:27`, `:33`) for the predicted path
   Direction must always come from BFS out of the roots, never from cell order — the VTK
   cells have no consistent proximal→distal orientation (`:11-13`).
3. **Phantom test suite** — synthetic trees with known angles, tortuosity and Strahler order.
   This is your unit-test suite and it needs no data at all.
4. **The GT-vs-prediction agreement study on ImageCAS-X.** Run the topology pipeline twice on
   the test set — once from GT masks, once from CAS-Net predictions — and Bland–Altman each
   feature. This defines which features survive automated segmentation, and therefore which
   are legitimate to carry into CGPS. It is the backbone of the validation chapter and it
   costs nothing extra.

Small enabling changes needed for the GT-free path (both trivially small):
- `dataloading/volume_dataset.py:20` / `base_dataset.py:_load_gt_mask` — make the GT mask
  optional at test time rather than raising. `predict()` never reads `batch["mask"]`.
- A volume-only cache builder — `utils/offline_resample_images_to_disk.py:115-117` resolves
  the mask path in the main process and aborts on the first missing file.

---

## Tomorrow's meeting — what to get

For **Phillip** (outcomes and cohort):
- Which events are recorded, how many, over what follow-up? **Event count, not patient
  count** — it determines how many features an outcome model can support.
- Are event *dates* available (survival analysis) or only binary flags?
- How many CGPS participants have CCTA at all?

On **repeat scans** — these now carry the main scientific argument, so press on the detail:
- Distribution of intervals between scans? (need ≥~2 years for plaque progression)
- Same scanner and protocol at both timepoints? If not, "change" is partly acquisition drift.
- **Why were people rescanned** — protocol/round-driven, or symptom-driven? A population
  study rescanning by protocol is clean; symptom-driven rescanning is informative selection.

On **plaque quantification** — the outcome variable for the progression design:
- Will Medis plaque volumes exist for **both** timepoints, or only the latest round?
- At what granularity — per patient, per vessel, or **per segment**? Per-segment is what
  makes the within-patient location-level analysis possible.
- Worth saying explicitly to Kit: the plaque-volume output he considers unhelpful for lumen
  segmentation is exactly what a progression analysis needs as its outcome.

On **scans**:
- Is the thin-slice reconstruction (≤0.5 mm) archived? ImageCAS-X models expect 0.25–0.45 mm
  slice spacing resampled to 0.5 mm isotropic. At ≥1 mm, distal branches vanish and your
  branch counts measure scanner resolution rather than anatomy.
- Is the reconstructed **cardiac phase** recorded per scan?

On **access**: when, and does compute happen inside the enclave or can data move?

---

## Shaping the labelling subset

Kit framed this as a learning exercise plus a validation route. Design it so it does three
jobs at once rather than one:

- **~30–40 scans.** Budget ~35 min/scan (ImageCAS-X reports 470 analyst-hours for 800 scans),
  so ~20–25 hours plus ramp-up.
- **Overlap 10–15 scans with Danina.** This gives you a **CGPS-specific inter-observer
  variability estimate** — the ceiling against which your automated features must be judged,
  mirroring exactly what the ImageCAS-X paper did. Without it you have no reference for "how
  good is good enough."
- **Include 5–10 scans that are part of a repeat pair.** Anchors the repeat-scan
  reproducibility study and lets you check whether *manual* labels are themselves
  reproducible across timepoints.
- **Stratify selection** by image quality (and dominance if known) rather than sampling at
  random or taking easy cases — otherwise you validate only where the task is easy.
- **Follow the ImageCAS-X protocol**, not the Medis one, so ImageCAS→CGPS domain shift is
  measured cleanly rather than confounded by a protocol difference.

Ask Kit to confirm the selection can be stratified and that overlap with Danina is planned
in, since both need deciding before labelling starts, not after.

---

## Milestones

Sequenced by dependency; each is cuttable from the bottom if time runs short.

| Phase | Work | Cut if short? |
|---|---|---|
| 1 | ImageCAS-X reproduced; `topology/` built; phantoms pass | No — foundation |
| 2 | GT-vs-prediction agreement on ImageCAS-X test set | No — the validation backbone |
| 3 | Labelling training + subset annotated | No — committed |
| 4 | CGPS deployment: GT-free inference + topology extraction + QC | No — the deliverable |
| 5 | Repeat-scan reproducibility study (n≈2000) → minimum detectable change | No — prerequisite for 7 |
| 6 | Population description + normative reference ranges | Trim scope, keep |
| 7 | **Baseline geometry → plaque progression** (t₀ → t₁, plaque-free locations) | No — the centrepiece |
| 8 | MACE association | Cut first; underpowered and weaker than 7 |

Phase 7 needs a **t₀↔t₁ correspondence method** built in phase 5 alongside the
reproducibility study — the same tree-matching machinery serves both.

Objectives 1–4 of your original brief (anatomy, CT, topology, state of the art) are written
alongside, grounded in this repo and the ImageCAS-X paper rather than in the abstract.

---

## Traps

- **Do not validate topology against Medis QAngio — but do use its plaque volumes.** Kit says
  it likely will not annotate all branches, so missing branches would make your pipeline look
  wrong where it is actually right, biasing branch counts, Strahler order and asymmetry. Its
  *trees* are not a topology reference. Its *plaque volumes* are the outcome variable for the
  progression analysis. Keep those two uses cleanly separate.
- **Do not wait for CGPS.** Phases 1–2 are months of work that need no access at all.
- **Do not take on the outer-wall model.** It is Kit's workstream. Keep the hook: design the
  feature table so a per-scan or per-segment plaque quantity can be joined in later if the
  wall model lands during your thesis.
- **Connectivity QC is not optional.** Betti-0 error is ~1.9 for the best method versus 0.4
  inter-observer, and the paper states vessel breaks persist in every method's output despite
  high Dice and clDice. One break splits a branch, invents an endpoint and shifts every
  Strahler number above it. Flag per scan: component count, largest-component fraction, total
  tree length, endpoint count, unconfident roots.
- **Segment naming stays out of scope** unless Medis intermediates arrive with usable branch
  names. Tree-level and unnamed-branch features work today; per-segment features and
  dominance do not.

## Verification

```bash
# foundation
python -m utils.verify_dataloaders -c configs/cas_net.json
python -m inference -c configs/cas_net.json -r <run_dir>
python -m evaluate  -c configs/cas_net.json -r <run_dir>      # expect DSC ~91.2, clDice ~93.3

# the validation backbone
python -m utils.precompute_topology -c configs/cas_net.json --split test --source gt
python -m utils.precompute_topology -c configs/cas_net.json --split test --source pred -r <run_dir>

# graph sanity, per scan: edges = nodes − roots; every vertex BFS-reached;
# summed branch lengths == total skeleton arc length

# dry-run the GT-free path on ImageCAS-X volumes with masks hidden —
# must produce byte-identical predictions to the normal path
```
