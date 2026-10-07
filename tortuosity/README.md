# RCA tortuosity on ImageCAS-X

Mean absolute curvature $T_\ell$ of the right coronary artery (RCA), measured on the 3D
centerlines delivered with ImageCAS-X, and the low / average / high grouping at the 10th
and 90th percentiles used by Tello Ayala et al. (JACC: Advances, 2026) on 2D angiograms.

## Method

For each artery, the centerline is the geodesic path from the ostium flag (`start_points`)
to the farthest point carrying the artery's label, keeping only the artery's own points so
LM is cut off (`vessels.py`). The walk uses the whole centerline tree, because the junction
point at the LM split carries only one child's label. The path therefore always starts at
the flag, and a same-label side branch cannot replace the proximal part. It is respaced so that every step is a
straight chord of exactly $\ell$ mm. At each interior vertex the turning angle between the
arriving and leaving chord is $\theta_j = \operatorname{atan2}(|a_j \times b_j|, a_j \cdot b_j)$,
and $T_\ell = \sum_j \theta_j / (\ell \cdot \#\text{angles})$ in rad/mm (`curvature.py`). The
reported score is $T_5$; $T_2$ and $T_8$ are the chord sensitivity check.

## Files

| File | |
|---|---|
| `paths.py` | every file this code reads or writes; the only place a location is spelled out |
| `curvature.py` | chord respacing, turning angles, $T_\ell$ |
| `vessels.py` | LAD, LCX and RCA centerlines from the ImageCAS-X VTK files, ostium flag first, LM cut off |
| `check.py` | checks on synthetic curves with known answers; needs no data |
| `score.py` | one column per entry of its `FEATURES` dict, for every vessel of one split, as CSV |
| `deciles.py` | RCA groups, the two figures, and the blinded visual check |
| `figure_turning_angle.py` | the worked 3D turning-angle figure |
| `regression_model.py` | logistic regression of a yes/no scan outcome on one vessel's $T_5$ and length, with optional covariates |
| `transformer_model.py` | local-attention transformer on the same vessel's ordered turning-angle profile, against that regression on the same rows |

## Reproducing

Requires the ImageCAS-X dataset (`centerlines/`, `filelist/` and `Descriptors.xlsx`). Point
`DATA` and `RESULTS` at the top of `paths.py` at the dataset root and at a writable output
directory; nothing else holds a path. Then, from the repository root:

```bash
python -m tortuosity.check
for s in train val test; do python -m tortuosity.score --split $s; done
python -m tortuosity.deciles make          # RCA
python -m tortuosity.deciles make LAD
python -m tortuosity.deciles make LCX
python -m tortuosity.figure_turning_angle
python -m tortuosity.regression_model --vessel LAD --outcome Disease   # train, reports val
python -m tortuosity.transformer_model --vessel LAD --outcome Disease  # the same, on the profile
```

The whole cohort of 800 scans scores in under a minute on one CPU core.
`jobs/tortuosity_deciles.sh` runs the same steps on an LSF cluster.

`transformer_model.py` needs torch, which `pyproject.toml` deliberately does not declare; a CPU
wheel is enough (`uv pip install torch --index-url https://download.pytorch.org/whl/cpu`). No GPU,
but it is not a login-node job: one vessel takes about 7 minutes on one core, five seeds included,
and the login node is capped at one core. `jobs/tortuosity_models.sh` runs both arms for all three
vessels, about 25 minutes.

Outputs, under `RESULTS` unless noted:
- `tortuosity_scores/{train,val,test}_vessels.csv`
- `tortuosity_deciles/groups.csv`, the labelling sample, `key.csv`;
  for LAD and LCX the same files under `tortuosity_deciles/LAD/` and `tortuosity_deciles/LCX/`
- `figures/rca_tortuosity_deciles.pdf`, `figures/rca_tortuosity_examples.pdf` (and `lad_`, `lcx_`),
  `figures/turning_angle_3d.pdf`

`regression_model.py` takes the vessel (`LAD`, `LCX`, `RCA`; default all) and the outcome (a
yes/no descriptor column; default `Disease`), and has two kinds of model term, neither limited
in number:

- `--features` names per-vessel columns of the score CSVs, default `T_5 length_mm`. Add a
  feature by writing a function of the centerline and adding one line to `score.FEATURES`, then
  rescoring the three splits.
- `--covariates` names per-scan columns of the sheets in `paths.DESCRIPTORS`, numbers used as
  they are and text such as `Sex` split into 0/1 columns. Add a covariate by adding a column to
  a sheet, or a whole source by adding a file to that list: the files are merged on `Scan ID`,
  left to right, so the first defines the cohort of 1000 scans. The delivered sheet has no age
  or sex today.

It writes to `tortuosity_<outcome>`, suffixed with every covariate and every feature beyond the
default pair, so two models never land in the same directory. It fits on train and reports val;
`--test` adds the test split and should be run once, after the definition is fixed.

`transformer_model.py` takes the same `--vessel`, `--outcome` and `--covariates`, plus `--chord`
(mm per token, default 5) and one flag per hyperparameter. One token is the turning angle at one
interior vertex after respacing to that chord, in rad/mm and with no division by $\pi$, so the
sequence's mean is exactly $T_5$: both arms see the same measurement, one as a profile and one
collapsed to its mean. The channel is standardised on the training tokens, so the unit cannot
change the result. It fits
the logistic regression on exactly the rows the transformer saw and reports the AUC difference with
a paired bootstrap CI, which Tello Ayala et al. do not. At 560 training scans against their 38,691,
and a val split of 80 whose AUC CI is about 0.13 wide, a gap of their size (0.67 against 0.60)
cannot be resolved here: a null is unresolved, not evidence against the profile. It writes to
`tortuosity_transformer_<outcome>[_chord<l>][_<covariates>]/<vessel>_{summary.txt,predictions.csv}`
and `failed.txt`, with every hyperparameter and every deviation from the paper recorded in each
summary.

Both merges end in `.dropna`, so a half-filled covariate column or a feature that is NaN on
short vessels silently shrinks the cohort. The first line of each `<vessel>_summary.txt` prints
the training n; compare it against the default run before reading anything into a difference.

Known data faults: in case 84 only 49 of the 266 LAD-labelled points connect to the ostium, so
its LAD score (49 points, 20.6 mm) covers a fragment. In cases 619, 794 and 789 mislabelled
points sit inside the LAD and are dropped, so the path jumps a gap of a few mm. Neither is
reported in `*_failed.txt` yet.

After labelling the images listed in `labels_todo.csv` (and later `repeat_todo.csv`),
`python -m tortuosity.deciles score` (add `LAD` or `LCX` for those vessels) reports precision, recall and Cohen's kappa of the
high group against the visual labels.
