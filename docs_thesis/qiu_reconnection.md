# Qiu et al. 2025 reconnection as post-processing on CAS-Net

Week 2 (`thesis/week2/segmentation_gap.tex`) committed the thesis to recovering topological
correctness *after* segmentation rather than retraining: CAS-Net reaches DSC 91.2 against the
analysts' 92.8 but a Betti error of 1.9 against their 0.4. This is the implementation of the
method that statement cites, `qiu2025topology`:

> Qiu, Shan, Wang, Dong, Wu, Yang, Hong, Shen. *A topology-preserving three-stage framework for
> fully-connected coronary artery extraction.* MedIA 103:103578 (2025). arXiv:2504.01597.

No code has been released. `github.com/YH-Qiu/CorSegRec` holds only a readme ("The code will be
available later"), checked 2026-09-14. Everything below is reimplemented from the paper text.

## 1. What the paper does, and which part is used

CorSegRec has three stages:

| Stage | What | Used here? |
|---|---|---|
| 1. Segmentation | nnU-Net trained with Dice + "NSDT soft-clDice" loss | **No.** A training loss; the thesis does not retrain. CAS-Net's delivered predictions stand in for it. |
| 2. Reconnection | skeletonise, pick join candidates, DPC walk, accept or reject, remove failures | **Yes, in full.** `postprocessing/qiu/` |
| 3. Reconstruction | INR lumen contours on 2D cross-sections along the stitched centerline, implicit extrusion surfaces | **Replaced** by a tube of interpolated radius. See deviation D1. |

Their own ablation (Table 9) credits stages 2+3 with +1.4 / +1.7 Dice and HD95 5.06 to 1.07 mm on
ASOCA / PDSCA. Their reconnection ablations (Tables 5 to 8) are scored with RecAcc, RecSen and RecSpe,
which `scripts/qiu_reconnect.py` also reports.

## 2. Where the code is

| File | Paper | Role |
|---|---|---|
| `postprocessing/qiu/skeleton.py` | 3.3 preamble | component to skeleton to branches, endpoints ("opening points"), outward tip directions from 3 consecutive points |
| `postprocessing/qiu/classifier.py` | eq. 7, 4.2 | patch features (15^3 max-pooled to 7^3, plus 7^3; Table 12) and the cascade forest P |
| `postprocessing/qiu/walk.py` | 3.3.2, eqs. 6 to 11 | the DPC walk, both neighbourhood levels, both direction filters |
| `postprocessing/qiu/reconnect.py` | 3.3.1, 3.3.3 | candidate types 1 to 3, P + ADF acceptance, removal, tube painting, GT annotation |
| `scripts/train_centerline_classifier.py` | 4.2 | trains P on the train split |
| `scripts/qiu_reconnect.py` | | applies it to a run's predictions, writes a new run dir + logs |
| `scripts/qiu_calibrate_threshold.py` | 3.3.3 | chooses the acceptance threshold on val |
| `configs/cas_net_qiu.json` | Table 12 | every parameter, in mm |
| `configs/cas_net_keep2.json` | | baseline: keep the two largest components, join nothing |
| `configs/cas_net_qiu_noremove.json` | | ablation: Qiu's joins, failures kept |
| `jobs/train_qiu_classifier.sh`, `jobs/qiu_reconnect.sh` | | LSF, CPU queue `hpc` |

It is a standalone pass over saved predictions, not a registry step in
`postprocessing/pipeline.py`: it needs the image, the 0.5 mm cache and a trained classifier, and it
runs on CPU, so bolting it onto the GPU inference job would idle the GPU. `evaluate.py` scores its
output run dir unchanged.

## 3. The algorithm, step by step

### 3.1 Grids

Predictions are saved on the scan's native grid (0.32 to 0.43 mm in-plane, 0.5 mm slices), and
Betti numbers are scored there. `reconnect.py` labels 26-connected components on the native grid,
then nearest-neighbour resamples the *label map* onto the 0.5 mm grid of `volumes_resampled/`
(`utils.io.resampled_geometry`, the same grid CAS-Net predicted on). Skeletons, walks and P all run
at 0.5 mm, so neighbourhoods are isotropic and patch sizes mean the same thing in every scan.

Only two things are written back to the native mask: fragments that are removed (by native label)
and tubes along accepted paths. Every other voxel stays bit-identical to the input prediction, so
any metric change is attributable to the repair.

### 3.2 Main trees and fragments (3.3, first paragraph)

The two largest components are the trees V_i; every other component is a disconnected fragment
CL_j. Each is skeletonised (Lee thinning) and split into branches between voxels of skeleton degree
!= 2. Terminal twigs shorter than 4 voxels are pruned once (D6). Each degree-1 voxel is a tip with
an outward direction `p0 - p2` from three consecutive points (the paper's rule).

### 3.3 Candidate selection (3.3.1)

Directions are taken along the flow: out of the tree's tail, into the fragment's head.

* **Nearest distance**: minimum distance between all points of the two centerlines.
* **Proximal angle**: between the tail's outward direction and the head's inward direction.
* **Positional cosines**: `cos(conn, u_tail) + cos(conn, u_head_in)`, conn = tail to head.

| Type | Joins | Gate (paper voxels, then mm at 0.4 mm/voxel) |
|---|---|---|
| 1 | fragment to fragment, run first "avoiding path overlap" | distance < 60 (24 mm), proximal angle < 120 deg |
| 2 | fragment head to a tree tip | distance < 80 (32 mm), proximal < 120 deg, positional sum > min(1.6, 2 cos proximal) |
| 3 | fragment to the *side* of a tree branch ("branch occurrence") | length > 10 (4 mm) needs distance < 20 (8 mm); length > 50 (20 mm) needs distance < 80 (32 mm) |

At most two candidates per fragment, nearest first. The paper performs the types
"sequentially ... on all input centerline branches", so the code runs type 1 over all fragments,
then type 2 over all waiting fragments, then type 3, and repeats types 2 and 3 for up to 3 rounds
so a fragment joined in round 1 offers its tips to the rest ("multiple rounds of filtering and
reconnection", 4.4). No (fragment, branch) pair is walked twice.

### 3.4 The DPC walk (3.3.2)

From the head, at each step every admissible neighbour A_k scores

    DPC(A_k) = D(A_k) + 5 * PN(A_k) + C(A_k)      if cos(o_-1, o_-2) <= 1/2
             = D(A_k) + 5 * PN(A_k)               otherwise

with D the negative distance to the tail point (eq. 6; type 3: to the nearest point of the branch,
eq. 11), PN = P min-max normalised over the current neighbours (eq. 9), and C the cosine of the step
with the last two steps (eq. 8). Omega = 5 is the paper's Table 5 optimum. Excluded: voxels already
on a stitched path, and steps turning more than 90 deg from the connection vector (types 1, 2) or
from `o_-1` and `o_-1 + o_-2` (type 3). Short gaps use the 26-neighbourhood; gaps above 5 mm use the
second-level shell 2 <= |o| <= 3 of a 5^3 cube (D5).

The walk ends on entering the target's mask (checked along the whole segment of a multi-voxel
step, so it cannot hop over a thin vessel), and fails on entering the *other* main tree (a join
must never fuse left and right), on running out of neighbours, or after 3x the gap in steps.

### 3.5 Accepting a join (3.3.3)

    accept  iff  mean P(path) + mean P(fragment centerline)  >=  T + p_ADF(P along path) + p_ADF(grey along path)

The grey sequence includes 5 skeleton voxels of the tree before the join and 5 of the fragment
after it. The ADF null hypothesis is a unit root, so a high p-value (non-stationary sequence) raises
the bar. The paper's T is "a predefined threshold (e.g., 1)". Rejected fragments are removed
("Any segments that fail to reconnect successfully are eliminated from the prediction mask").

### 3.6 Writing the join into the mask (stage 3 substitute)

Each accepted path is painted on the native grid as a tube, radius running linearly from the
fragment's EDT radius at the head to the tree's at the tail, floored at 0.6 mm so the tube is
26-connected on every native grid in this dataset.

## 4. Deviations from the paper (record these wherever results are reported)

| # | Deviation | Why |
|---|---|---|
| D1 | Stage 3 (INR + implicit extrusion surfaces) replaced by a linear-radius tube | stage 3 needs its own trained INR; the tube reproduces what the Betti error sees (a connection) but not lumen shape in the gap |
| D2 | Stage 1 loss not used; input is CAS-Net, not nnU-Net + NSDT soft-clDice | thesis does not retrain (week 2 statement) |
| D3 | Cascade forest rebuilt on scikit-learn (2 RF + 2 ExtraTrees per layer, OOB class vectors), not `deep-forest` | `deep-forest` has no Python 3.11 wheels. No histogram binning. 50 trees, min leaf 10, <= 3 layers, versus deep-forest's 100 trees, leaf 1, <= 20 layers, to bound model size (not yet measured) |
| D4 | Distance thresholds converted from ASOCA voxels to mm at 0.4 mm/voxel; walk on a 0.5 mm grid | paper states voxel counts at 0.3 to 0.4 mm in-plane |
| D5 | Second-level neighbourhood used when the gap exceeds 5 mm; max steps 3x the gap | paper says only "larger nearest distances" and gives no cap |
| D6 | Terminal skeleton twigs < 4 voxels pruned | Lee thinning's surface twigs would otherwise be tails with meaningless directions |
| D7 | "Opening points" = skeleton degree-1 voxels | paper mentions an 11^3 neighbourhood search without defining it |
| D8 | Type 3's "reversed" angle settings read as: branches type 2's angle test did not already take, any branch within the length-dependent distance | the paper gives one sentence |
| D9 | ADF term skipped (penalty 0) for sequences shorter than 8 | the test is undefined on a handful of points |
| D10 | P's training positives are the dataset's expert centerline VTKs rasterised at 0.5 mm, kept where inside GT lumen | paper samples "the centerline region" of its labels |
| D11 | **T is calibrated on the val split** (section 5, step 3), not fixed at 1 | T is tied to the classifier's probability scale; see the smoke test below |
| D12 | Fragments too small to survive the 0.5 mm resampling are removed with the failures | they cannot be skeletonised |

## 5. Running it

All steps are CPU except step 2. Submit from the repo root after `source env.sh`.

**Step 1: train P** (runtime not yet measured; 8 h walltime requested):

    bsub < jobs/train_qiu_classifier.sh

Check `$ImageCAS_X_results_path/qiu_centerline_classifier/report.json`: `val_auc`, and
`val_mean_p_by_region`. The mean P on true centerline voxels is what T has to be read against.

**Step 2: CAS-Net predictions for the val split** (GPU, about 40 min for 80 scans):

    mkdir -p $ImageCAS_X_results_path/cas_net_pretrained_val
    ln -s $ImageCAS_X_weights_path/cas_net.pt $ImageCAS_X_results_path/cas_net_pretrained_val/cas_net_best.pt
    bsub -env "all, RUN_DIR=cas_net_pretrained_val, SPLIT=val" < jobs/infer_eval_cas_net.sh

**Step 3: calibrate T on val.** A pass that rejects everything, so every candidate of every
fragment is walked and logged from the same state, then a replay over T in [0, 2]:

    bsub -env "all, RUN_DIR=cas_net_pretrained_val_qiu_calib, SRC_RUN=cas_net_pretrained_val, SPLIT=val, SET=eval_threshold=99" < jobs/qiu_reconnect.sh
    python scripts/qiu_calibrate_threshold.py -r cas_net_pretrained_val_qiu_calib   # login node, seconds

It prints RecAcc / RecSen / RecSpe per T, with and without ADF, and the paper's T = 1 for
reference. Put the chosen `eval_threshold` (and `use_adf`) into `configs/cas_net_qiu.json`. The
replay is exact for each fragment's own decision but ignores type-1 merges and multi-round
effects; the test run below does not.

**Step 4: the test-split comparison** (three independent jobs, minutes each):

    bsub -env "all, RUN_DIR=cas_net_pretrained_keep2, CONFIG=configs/cas_net_keep2.json" < jobs/qiu_reconnect.sh
    bsub -env "all, RUN_DIR=cas_net_pretrained_qiu" < jobs/qiu_reconnect.sh
    bsub -env "all, RUN_DIR=cas_net_pretrained_qiu_noremove, CONFIG=configs/cas_net_qiu_noremove.json" < jobs/qiu_reconnect.sh

Each writes `predictions/`, `reconnection_logs/<id>.json` (every attempt: type, distance, angles,
walk outcome, P means, ADF p-values, score, bar, and post hoc its GT fractions),
`reconnection_summary.json` and `<method>_results.json` from `evaluate.py`.

## 6. Reading the result

**The Betti-0 error rewards deletion.** In the smoke test every inspected prediction's GT has
b0 = 2, so keeping the two largest components drives b0 error to 0 whatever the fragments were.
A reconnection method only earns its place against `keep2` on what deletion cannot give: the true
vessel pieces it keeps and connects. So the table has to carry, next to Betti error, Dice, clDice
and the centerline metrics, plus RecSen (true fragments rescued) and RecSpe (false ones removed).

The three runs separate the effects:

* `keep2` minus baseline: what removal alone does.
* `qiu` minus `keep2`: what the joins add on top of removal.
* `qiu_noremove` minus baseline: what the joins do with no removal at all.

**What each fragment is.** Every log carries `fragments[].gt_fraction`, the share of the fragment
inside the 1-voxel-dilated GT lumen. The `keep2` run alone therefore answers a question worth
reporting regardless of Qiu: how much of CAS-Net's Betti error is broken vessel, and how much is
spurious structure the annotation does not contain. "Not in GT" includes real vessel beyond where
the annotators stopped, so it is "absent from the reference", not "not anatomy".

## 7. Smoke test, 2026-09-14 (mechanics only, not a result)

Login node, toy classifier (2 train scans, 10 trees; val AUC 0.93, mean P on centerline voxels
0.49), 4 test scans (85, 88, 509, 686), all other settings as in `cas_net_qiu.json`. About 25 s
per scan.

* Every walk reached its target; no walk failure of any kind.
* Only 1 of the first 9 fragments examined (scans 85, 88, 686) was >= 50% inside GT; the rest
  were spurious. If that holds cohort-wide, most of CAS-Net's b0 error is spurious components.
* Scan 88's one true fragment (1221 voxels, 3.1 mm gap): the walk ran 100% inside the GT lumen,
  i.e. found the real vessel course, but was rejected, 0.41 + 0.45 = 0.86 < T = 1.
* Scan 686's spurious fragment was accepted (0.63 + 0.55 = 1.18 >= 1.05).
* ADF p-values on 10 to 13-point P sequences reached 0.96 to 0.98, raising the bar to about 2,
  which no score can reach.

This is why D11 exists: with P on this scale, T = 1 plus ADF rejects nearly every join, and the
method collapses to `keep2`. Whether the fully trained P separates true from spurious fragments is
the first thing to read off step 1 and step 3.
