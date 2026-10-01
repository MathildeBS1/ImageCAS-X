# RCA tortuosity on ImageCAS-X

Mean absolute curvature $T_\ell$ of the right coronary artery (RCA), measured on the 3D
centerlines delivered with ImageCAS-X, and the low / average / high grouping at the 10th
and 90th percentiles used by Tello Ayala et al. (JACC: Advances, 2026) on 2D angiograms.

## Method

For each artery, the centerline is the longest geodesic path through the points carrying
its label, walked from the ostium (`vessels.py`). It is respaced so that every step is a
straight chord of exactly $\ell$ mm. At each interior vertex the turning angle between the
arriving and leaving chord is $\theta_j = \operatorname{atan2}(|a_j \times b_j|, a_j \cdot b_j)$,
and $T_\ell = \sum_j \theta_j / (\ell \cdot \#\text{angles})$ in rad/mm (`curvature.py`). The
reported score is $T_5$; $T_2$ and $T_8$ are the chord sensitivity check.

## Files

| File | |
|---|---|
| `curvature.py` | chord respacing, turning angles, $T_\ell$ |
| `vessels.py` | LAD, LCX and RCA centerlines from the ImageCAS-X VTK files, ostium first |
| `check.py` | checks on synthetic curves with known answers; needs no data |
| `score.py` | $T_2$, $T_5$, $T_8$ and length for every vessel of one split, as CSV |
| `deciles.py` | RCA groups, the two figures, and the blinded visual check |
| `figure_turning_angle.py` | the worked 3D turning-angle figure |

## Reproducing

Requires the ImageCAS-X dataset (`centerlines/` and `filelist/`) and two environment
variables, `ImageCAS_X_data_path` (dataset root) and `ImageCAS_X_results_path` (where
outputs go). From the repository root:

```bash
python -m tortuosity.check
for s in train val test; do python -m tortuosity.score --split $s; done
python -m tortuosity.deciles make
python -m tortuosity.figure_turning_angle
```

The whole cohort of 800 scans scores in under a minute on one CPU core.
`jobs/tortuosity_deciles.sh` runs the same steps on an LSF cluster.

Outputs:
- `$ImageCAS_X_results_path/tortuosity_scores/{train,val,test}_vessels.csv`
- `$ImageCAS_X_results_path/tortuosity_deciles/groups.csv`, the labelling sample, `key.csv`
- `figures/rca_tortuosity_deciles.pdf`, `figures/rca_tortuosity_examples.pdf`,
  `figures/turning_angle_3d.pdf`

After labelling the images listed in `labels_todo.csv` (and later `repeat_todo.csv`),
`python -m tortuosity.deciles score` reports precision, recall and Cohen's kappa of the
high group against the visual labels.
