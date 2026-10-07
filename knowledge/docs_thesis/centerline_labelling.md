# Centerlines from predicted lumen, and the segment labeller

Purpose: name the arteries on trees that arrive unlabelled (Herlev–Østerbro / CGPS). The
pipeline has three stages: extract centerlines from a lumen mask the way ImageCAS-X built its
delivered ones (Bransby et al. 2026), score them against the delivered centerlines, then train a
GNN on the delivered `segment_label` to name segments.

The review that shaped this design is `reports/Centerline labelling plan review.md`, with its
notes in `research_notes/Centerline labelling plan review/`.

## Run order (the user submits every job)

| # | Job | What it gives |
|---|---|---|
| 0 | reinstall a CUDA torch in the venv (see CLAUDE.md) | GPU inference |
| 1 | `bsub -env "all, RUN_DIR=cas_net_pretrained" < jobs/infer_eval_cas_net.sh` | test predictions (24/160 exist) |
| 2 | `bsub -env "all, RUN_DIR=cas_net_pretrained, SPLIT=val" < jobs/infer_eval_cas_net.sh` | `predictions_val/` for calibration |
| 3 | `bsub < jobs/radius_cache.sh` | GT radius at every delivered point |
| 4 | one-time TotalSegmentator setup (header of `jobs/totalseg_heart.sh`), then `bsub -env "all, SPLIT=train|val|test" < jobs/totalseg_heart.sh` | aorta + chambers per case |
| 5 | `bsub -env "all, STEP=calibrate" < jobs/extract_centerlines.sh` | ostium cap, pruning grid on val |
| 6 | pick `t` at the knee of `term_spurious_mm` vs `term_missed_mm` across `cas_net_pretrained_t*/summary_val.json` | frozen `t` |
| 7 | `bsub -env "all, STEP=test, T=<t>" < jobs/extract_centerlines.sh` | test scores, GT-mask floor, Wilcoxon, sensitivity |
| 8 | `bsub -env "all, T=<t>" < jobs/train_labeller.sh` | `gnn3`, `gnn0`, evaluations |

Outputs go to `/work3/s254124/imagecasx_results/`:
- `totalseg/<id>/`
- `extracted_centerlines/<source>_t<t>[_oracle]/`, holding per-case VTK and JSON plus
  `scores_<split>.csv` and `summary_<split>.json`
- `labeller/{prepared,gnn3,gnn0}/`

## Code

- `bifurcation/skeleton.py` runs the full extraction. `bifurcation/extract.py` is its driver
  (`--fit-cap`, `--oracle-ostia`).
- `bifurcation/score_extraction.py` holds the CAT08-style measures, Hungarian bifurcation
  matching and the ATM'22 branch rule.
- `labelling/data.py` builds the heart frame, label transfer, 15 mm pieces, augmentation and
  features. `labelling/model.py` holds the SAGE-style residual GNN, tree Viterbi and transition
  counts. `labelling/train.py` and `labelling/evaluate.py` train and evaluate.

## Deviations from Bransby et al. 2026, to state with any number

- **Aorta and ostium cap.** The aorta and chambers come from TotalSegmentator
  `heartchambers_highres`, the same model the paper used; the version is in
  `totalseg/version.txt`. The ostium cap is fitted on train (99th percentile of start-point to
  aorta distance) instead of the paper's 5 mm.
- **Automatic spur pruning.** The paper removed spurs by hand. Here a bulge-size rule (Drees et
  al. 2021) is calibrated on CAS-Net val predictions.
- **Junction contraction.** Junction-to-junction paths shorter than 2 voxels are collapsed.
  Enclosed cavities are filled before thinning, and each cycle is broken at its thinnest chain.
- **Side rule.** Tree-centroid LPS x decides the side, with ostium y as tie-break when the
  centroids are within 5 mm. Both rules hold on 800/800 delivered cases.
- **Orphans and fallbacks.** Orphan components of 5 mm or more are kept on the nearest side.
  Fallback ostia go to components of 20 mm or more when fewer than two trees are rooted.
- **Radius.** Radius is the EDT on native anisotropic masks, which over-reads by up to half a
  voxel.
- **Scoring.** The primary bifurcation gate is 3 mm, with 1/2/3/5 mm reported. The tolerance is
  the GT radius floored at 0.35 mm.

## Known limits

- The `gt` arm is an implementation floor, not inter-observer agreement. The second-observer
  files are not delivered.
- On one val GT mask (case 961), the extraction matches the delivered topology exactly (same
  segment, bifurcation and terminus counts; 14 s). Delivered junction and end points sit within
  one voxel (≤ 0.61 mm) of the skeleton, not exactly on it.
