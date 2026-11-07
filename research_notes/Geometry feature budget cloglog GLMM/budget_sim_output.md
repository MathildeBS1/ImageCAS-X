OWN CALCULATION. Aggregate inputs + synthetic data only; no individual data.

# 1. Riley criteria at person level (own calculation)

n = 1076, events = 452, phi = 0.4201; max R2_CS = 0.7435; criterion (iii) needs n >= 374 (met)
  anchor: SCORE2 recalibrated, OOF log-loss 0.6284: OOF R2_CS = 0.0986 (null log-loss 0.6803)
  anchor: refitted factors, OOF log-loss 0.6346: OOF R2_CS = 0.0874 (null log-loss 0.6803)
| C | R2_CS | P_max crit (i) S=0.9 | S_VH crit (ii) | P_max crit (ii) | binding P_max |
|---|---|---|---|---|---|
| 0.65 | 0.0675 | 8.4 | 0.645 | 42.3 | 8.4 |
| 0.7 | 0.1181 | 15.1 | 0.761 | 43.5 | 15.1 |
| 0.72 | 0.1419 | 18.5 | 0.792 | 44.1 | 18.5 |
| 0.75 | 0.1812 | 24.2 | 0.830 | 45.1 | 24.2 |
| 15% of max | 0.1115 | 14.2 | 0.750 | 43.3 | 14.2 |

n = 1041, events = 433, phi = 0.4159; max R2_CS = 0.7428; criterion (iii) needs n >= 373 (met)
  anchor: SCORE2 recalibrated, OOF log-loss 0.6284: OOF R2_CS = 0.0962 (null log-loss 0.6789)
  anchor: refitted factors, OOF log-loss 0.6346: OOF R2_CS = 0.0849 (null log-loss 0.6789)
| C | R2_CS | P_max crit (i) S=0.9 | S_VH crit (ii) | P_max crit (ii) | binding P_max |
|---|---|---|---|---|---|
| 0.65 | 0.0673 | 8.1 | 0.644 | 40.8 | 8.1 |
| 0.7 | 0.1178 | 14.6 | 0.760 | 42.0 | 14.6 |
| 0.72 | 0.1416 | 17.8 | 0.792 | 42.6 | 17.8 |
| 0.75 | 0.1808 | 23.3 | 0.830 | 43.6 | 23.3 |
| 15% of max | 0.1114 | 13.8 | 0.750 | 41.9 | 13.8 |

# 2/3. Synthetic truths (latent ICC -> observed-scale design effect) and simulation

### latent ICC 0.1, extra geometry HR 1.0 (null extras), base = SCORE2 recalibrated; 40 reps
truth: {"prev": 0.4194, "seg_events_per_1076": 659.2437, "seg_per_affected": 1.461, "rho_obs": 0.045, "deff": 1.3602, "q_seg": 0.0681, "c_true_base": 0.7012, "c_true_full": 0.7148, "seg_share": [0.21, 0.211, 0.112, 0.079, 0.055, 0.046, 0.115, 0.099, 0.073], "icc_latent": 0.1, "sigma": 0.4275, "c_mult": 1.1506, "extra_hr": 1.0}
| k geo df | total fixed df (excl. intercept) | mean OOS calibration slope (MC SE) | P(slope<0.9) | mean heuristic S_VH | OOS C | CITL | LR-test power (alpha 0.05) | mean sigma-hat | non-converged |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 12 | 1.014 (0.015) | 0.07 | 0.965 | 0.6735 | +0.015 |  | 0.565 | 0 |
| 2 | 14 | 0.989 (0.012) | 0.10 | 0.963 | 0.6820 | +0.016 | 1.00 | 0.531 | 0 |
| 4 | 16 | 0.972 (0.011) | 0.12 | 0.960 | 0.6855 | +0.018 | 1.00 | 0.513 | 0 |
| 5 | 17 | 0.970 (0.011) | 0.12 | 0.958 | 0.6883 | +0.017 | 1.00 | 0.500 | 0 |
| 6 | 18 | 0.968 (0.011) | 0.12 | 0.956 | 0.6881 | +0.018 | 1.00 | 0.500 | 0 |
| 7 | 19 | 0.959 (0.011) | 0.17 | 0.953 | 0.6875 | +0.017 | 1.00 | 0.497 | 0 |
| 8 | 20 | 0.956 (0.010) | 0.17 | 0.951 | 0.6873 | +0.017 | 1.00 | 0.497 | 0 |
| 10 | 22 | 0.948 (0.010) | 0.17 | 0.946 | 0.6866 | +0.017 | 1.00 | 0.495 | 0 |
| 12 | 24 | 0.939 (0.010) | 0.20 | 0.942 | 0.6859 | +0.017 | 1.00 | 0.493 | 0 |
first k with mean slope < 0.9: none up to 12
[elapsed 173s]

### latent ICC 0.1, extra geometry HR 1.0 (null extras), base = refitted factors (6); 40 reps
truth: {"prev": 0.4194, "seg_events_per_1076": 659.2437, "seg_per_affected": 1.461, "rho_obs": 0.045, "deff": 1.3602, "q_seg": 0.0681, "c_true_base": 0.7012, "c_true_full": 0.7148, "seg_share": [0.21, 0.211, 0.112, 0.079, 0.055, 0.046, 0.115, 0.099, 0.073], "icc_latent": 0.1, "sigma": 0.4275, "c_mult": 1.1506, "extra_hr": 1.0}
| k geo df | total fixed df (excl. intercept) | mean OOS calibration slope (MC SE) | P(slope<0.9) | mean heuristic S_VH | OOS C | CITL | LR-test power (alpha 0.05) | mean sigma-hat | non-converged |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 17 | 0.951 (0.010) | 0.30 | 0.959 | 0.6977 | -0.013 |  | 0.450 | 0 |
| 2 | 19 | 0.942 (0.009) | 0.28 | 0.958 | 0.7050 | -0.011 | 1.00 | 0.416 | 0 |
| 4 | 21 | 0.930 (0.009) | 0.30 | 0.956 | 0.7082 | -0.010 | 1.00 | 0.391 | 0 |
| 5 | 22 | 0.929 (0.009) | 0.30 | 0.954 | 0.7102 | -0.010 | 1.00 | 0.378 | 0 |
| 6 | 23 | 0.928 (0.009) | 0.30 | 0.952 | 0.7101 | -0.010 | 1.00 | 0.378 | 0 |
| 7 | 24 | 0.924 (0.008) | 0.30 | 0.950 | 0.7098 | -0.010 | 1.00 | 0.376 | 0 |
| 8 | 25 | 0.921 (0.008) | 0.30 | 0.948 | 0.7095 | -0.010 | 1.00 | 0.374 | 0 |
| 10 | 27 | 0.918 (0.008) | 0.30 | 0.944 | 0.7092 | -0.010 | 1.00 | 0.373 | 0 |
| 12 | 29 | 0.910 (0.008) | 0.40 | 0.940 | 0.7084 | -0.011 | 1.00 | 0.367 | 0 |
first k with mean slope < 0.9: none up to 12
[elapsed 383s]

### latent ICC 0.3, extra geometry HR 1.0 (null extras), base = SCORE2 recalibrated; 40 reps
truth: {"prev": 0.4201, "seg_events_per_1076": 775.3871, "seg_per_affected": 1.7154, "rho_obs": 0.1115, "deff": 1.8919, "q_seg": 0.0801, "c_true_base": 0.6973, "c_true_full": 0.709, "seg_share": [0.203, 0.203, 0.115, 0.083, 0.055, 0.048, 0.115, 0.101, 0.076], "icc_latent": 0.3, "sigma": 0.8396, "c_mult": 1.3117, "extra_hr": 1.0}
| k geo df | total fixed df (excl. intercept) | mean OOS calibration slope (MC SE) | P(slope<0.9) | mean heuristic S_VH | OOS C | CITL | LR-test power (alpha 0.05) | mean sigma-hat | non-converged |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 12 | 0.939 (0.014) | 0.35 | 0.968 | 0.6607 | +0.010 |  | 0.943 | 0 |
| 2 | 14 | 0.938 (0.013) | 0.35 | 0.966 | 0.6684 | +0.009 | 1.00 | 0.928 | 0 |
| 4 | 16 | 0.932 (0.013) | 0.40 | 0.963 | 0.6728 | +0.007 | 1.00 | 0.920 | 0 |
| 5 | 17 | 0.932 (0.013) | 0.40 | 0.961 | 0.6748 | +0.009 | 1.00 | 0.915 | 0 |
| 6 | 18 | 0.931 (0.013) | 0.40 | 0.959 | 0.6747 | +0.009 | 1.00 | 0.915 | 0 |
| 7 | 19 | 0.924 (0.013) | 0.45 | 0.956 | 0.6742 | +0.009 | 1.00 | 0.913 | 0 |
| 8 | 20 | 0.922 (0.012) | 0.47 | 0.954 | 0.6740 | +0.009 | 1.00 | 0.913 | 0 |
| 10 | 22 | 0.912 (0.012) | 0.50 | 0.950 | 0.6733 | +0.009 | 1.00 | 0.911 | 0 |
| 12 | 24 | 0.906 (0.012) | 0.55 | 0.946 | 0.6728 | +0.009 | 1.00 | 0.911 | 0 |
first k with mean slope < 0.9: none up to 12
[elapsed 557s]

### latent ICC 0.3, extra geometry HR 1.0 (null extras), base = refitted factors (6); 40 reps
truth: {"prev": 0.4201, "seg_events_per_1076": 775.3871, "seg_per_affected": 1.7154, "rho_obs": 0.1115, "deff": 1.8919, "q_seg": 0.0801, "c_true_base": 0.6973, "c_true_full": 0.709, "seg_share": [0.203, 0.203, 0.115, 0.083, 0.055, 0.048, 0.115, 0.101, 0.076], "icc_latent": 0.3, "sigma": 0.8396, "c_mult": 1.3117, "extra_hr": 1.0}
| k geo df | total fixed df (excl. intercept) | mean OOS calibration slope (MC SE) | P(slope<0.9) | mean heuristic S_VH | OOS C | CITL | LR-test power (alpha 0.05) | mean sigma-hat | non-converged |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 17 | 0.936 (0.010) | 0.42 | 0.961 | 0.6877 | +0.007 |  | 0.870 | 0 |
| 2 | 19 | 0.928 (0.010) | 0.30 | 0.959 | 0.6945 | +0.007 | 1.00 | 0.852 | 0 |
| 4 | 21 | 0.923 (0.010) | 0.38 | 0.957 | 0.6977 | +0.007 | 1.00 | 0.843 | 0 |
| 5 | 22 | 0.923 (0.009) | 0.38 | 0.955 | 0.6994 | +0.007 | 1.00 | 0.837 | 0 |
| 6 | 23 | 0.921 (0.009) | 0.38 | 0.953 | 0.6992 | +0.007 | 1.00 | 0.837 | 0 |
| 7 | 24 | 0.917 (0.010) | 0.42 | 0.951 | 0.6989 | +0.007 | 1.00 | 0.836 | 0 |
| 8 | 25 | 0.916 (0.010) | 0.40 | 0.949 | 0.6988 | +0.008 | 1.00 | 0.836 | 0 |
| 10 | 27 | 0.909 (0.009) | 0.47 | 0.945 | 0.6982 | +0.008 | 1.00 | 0.835 | 0 |
| 12 | 29 | 0.901 (0.009) | 0.53 | 0.941 | 0.6976 | +0.008 | 1.00 | 0.833 | 0 |
first k with mean slope < 0.9: none up to 12
[elapsed 730s]

### latent ICC 0.55, extra geometry HR 1.0 (null extras), base = SCORE2 recalibrated; 40 reps
truth: {"prev": 0.4206, "seg_events_per_1076": 1055.0503, "seg_per_affected": 2.3315, "rho_obs": 0.2685, "deff": 3.1478, "q_seg": 0.1089, "c_true_base": 0.6964, "c_true_full": 0.7032, "seg_share": [0.186, 0.185, 0.114, 0.088, 0.064, 0.055, 0.118, 0.107, 0.082], "icc_latent": 0.55, "sigma": 1.4179, "c_mult": 1.6873, "extra_hr": 1.0}
| k geo df | total fixed df (excl. intercept) | mean OOS calibration slope (MC SE) | P(slope<0.9) | mean heuristic S_VH | OOS C | CITL | LR-test power (alpha 0.05) | mean sigma-hat | non-converged |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 12 | 0.976 (0.014) | 0.23 | 0.972 | 0.6674 | -0.006 |  | 1.484 | 0 |
| 2 | 14 | 0.981 (0.014) | 0.20 | 0.969 | 0.6733 | -0.002 | 1.00 | 1.478 | 0 |
| 4 | 16 | 0.975 (0.014) | 0.17 | 0.966 | 0.6757 | +0.000 | 1.00 | 1.477 | 0 |
| 5 | 17 | 0.970 (0.014) | 0.23 | 0.964 | 0.6766 | -0.000 | 1.00 | 1.474 | 0 |
| 6 | 18 | 0.969 (0.014) | 0.23 | 0.962 | 0.6766 | -0.000 | 1.00 | 1.473 | 0 |
| 7 | 19 | 0.960 (0.013) | 0.23 | 0.960 | 0.6760 | -0.000 | 1.00 | 1.472 | 0 |
| 8 | 20 | 0.958 (0.013) | 0.23 | 0.958 | 0.6759 | -0.000 | 1.00 | 1.472 | 0 |
| 10 | 22 | 0.951 (0.013) | 0.28 | 0.954 | 0.6755 | -0.000 | 1.00 | 1.471 | 0 |
| 12 | 24 | 0.945 (0.013) | 0.33 | 0.950 | 0.6750 | -0.000 | 1.00 | 1.470 | 0 |
first k with mean slope < 0.9: none up to 12
[elapsed 840s]

### latent ICC 0.55, extra geometry HR 1.0 (null extras), base = refitted factors (6); 40 reps
truth: {"prev": 0.4206, "seg_events_per_1076": 1055.0503, "seg_per_affected": 2.3315, "rho_obs": 0.2685, "deff": 3.1478, "q_seg": 0.1089, "c_true_base": 0.6964, "c_true_full": 0.7032, "seg_share": [0.186, 0.185, 0.114, 0.088, 0.064, 0.055, 0.118, 0.107, 0.082], "icc_latent": 0.55, "sigma": 1.4179, "c_mult": 1.6873, "extra_hr": 1.0}
| k geo df | total fixed df (excl. intercept) | mean OOS calibration slope (MC SE) | P(slope<0.9) | mean heuristic S_VH | OOS C | CITL | LR-test power (alpha 0.05) | mean sigma-hat | non-converged |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 17 | 0.977 (0.011) | 0.15 | 0.965 | 0.6981 | -0.001 |  | 1.397 | 0 |
| 2 | 19 | 0.975 (0.011) | 0.15 | 0.963 | 0.7025 | +0.000 | 1.00 | 1.392 | 0 |
| 4 | 21 | 0.970 (0.010) | 0.15 | 0.961 | 0.7045 | +0.003 | 1.00 | 1.388 | 0 |
| 5 | 22 | 0.964 (0.010) | 0.15 | 0.959 | 0.7050 | +0.002 | 1.00 | 1.384 | 0 |
| 6 | 23 | 0.963 (0.010) | 0.15 | 0.957 | 0.7049 | +0.002 | 1.00 | 1.384 | 0 |
| 7 | 24 | 0.960 (0.010) | 0.15 | 0.956 | 0.7046 | +0.002 | 1.00 | 1.382 | 0 |
| 8 | 25 | 0.959 (0.010) | 0.15 | 0.954 | 0.7045 | +0.002 | 1.00 | 1.382 | 0 |
| 10 | 27 | 0.953 (0.010) | 0.17 | 0.950 | 0.7039 | +0.002 | 1.00 | 1.380 | 0 |
| 12 | 29 | 0.947 (0.010) | 0.17 | 0.947 | 0.7033 | +0.002 | 1.00 | 1.379 | 0 |
first k with mean slope < 0.9: none up to 12
[elapsed 938s]

### latent ICC 0.55, extra geometry HR 1.1 (all features carry signal), base = SCORE2 recalibrated; 40 reps
truth: {"prev": 0.4208, "seg_events_per_1076": 1067.9623, "seg_per_affected": 2.3588, "rho_obs": 0.2777, "deff": 3.2212, "q_seg": 0.1103, "c_true_base": 0.7028, "c_true_full": 0.7159, "seg_share": [0.186, 0.186, 0.116, 0.088, 0.064, 0.056, 0.117, 0.106, 0.082], "icc_latent": 0.55, "sigma": 1.4179, "c_mult": 1.6638, "extra_hr": 1.1}
| k geo df | total fixed df (excl. intercept) | mean OOS calibration slope (MC SE) | P(slope<0.9) | mean heuristic S_VH | OOS C | CITL | LR-test power (alpha 0.05) | mean sigma-hat | non-converged |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 12 | 1.007 (0.012) | 0.05 | 0.972 | 0.6777 | -0.031 |  | 1.497 | 0 |
| 2 | 14 | 1.003 (0.011) | 0.05 | 0.969 | 0.6826 | -0.030 | 1.00 | 1.493 | 0 |
| 4 | 16 | 0.994 (0.011) | 0.05 | 0.967 | 0.6850 | -0.031 | 1.00 | 1.490 | 0 |
| 5 | 17 | 0.993 (0.011) | 0.07 | 0.965 | 0.6867 | -0.030 | 1.00 | 1.485 | 0 |
| 6 | 18 | 0.993 (0.011) | 0.07 | 0.963 | 0.6872 | -0.030 | 1.00 | 1.485 | 0 |
| 7 | 19 | 0.991 (0.011) | 0.05 | 0.961 | 0.6887 | -0.029 | 1.00 | 1.479 | 0 |
| 8 | 20 | 0.990 (0.011) | 0.05 | 0.960 | 0.6891 | -0.029 | 1.00 | 1.480 | 0 |
| 10 | 22 | 0.985 (0.010) | 0.07 | 0.957 | 0.6905 | -0.028 | 1.00 | 1.478 | 0 |
| 12 | 24 | 0.980 (0.010) | 0.05 | 0.954 | 0.6923 | -0.029 | 1.00 | 1.473 | 0 |
first k with mean slope < 0.9: none up to 12
[elapsed 1060s]

### latent ICC 0.55, extra geometry HR 1.1 (all features carry signal), base = refitted factors (6); 40 reps
truth: {"prev": 0.4208, "seg_events_per_1076": 1067.9623, "seg_per_affected": 2.3588, "rho_obs": 0.2777, "deff": 3.2212, "q_seg": 0.1103, "c_true_base": 0.7028, "c_true_full": 0.7159, "seg_share": [0.186, 0.186, 0.116, 0.088, 0.064, 0.056, 0.117, 0.106, 0.082], "icc_latent": 0.55, "sigma": 1.4179, "c_mult": 1.6638, "extra_hr": 1.1}
| k geo df | total fixed df (excl. intercept) | mean OOS calibration slope (MC SE) | P(slope<0.9) | mean heuristic S_VH | OOS C | CITL | LR-test power (alpha 0.05) | mean sigma-hat | non-converged |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 17 | 0.987 (0.014) | 0.15 | 0.965 | 0.6996 | -0.030 |  | 1.424 | 0 |
| 2 | 19 | 0.989 (0.014) | 0.10 | 0.963 | 0.7037 | -0.027 | 1.00 | 1.422 | 0 |
| 4 | 21 | 0.982 (0.013) | 0.12 | 0.960 | 0.7056 | -0.026 | 1.00 | 1.420 | 0 |
| 5 | 22 | 0.979 (0.013) | 0.12 | 0.959 | 0.7066 | -0.025 | 1.00 | 1.416 | 0 |
| 6 | 23 | 0.978 (0.013) | 0.12 | 0.957 | 0.7071 | -0.025 | 1.00 | 1.418 | 0 |
| 7 | 24 | 0.976 (0.013) | 0.12 | 0.956 | 0.7081 | -0.025 | 1.00 | 1.412 | 0 |
| 8 | 25 | 0.975 (0.013) | 0.12 | 0.955 | 0.7085 | -0.025 | 1.00 | 1.413 | 0 |
| 10 | 27 | 0.969 (0.013) | 0.17 | 0.952 | 0.7095 | -0.024 | 1.00 | 1.408 | 0 |
| 12 | 29 | 0.965 (0.013) | 0.17 | 0.949 | 0.7110 | -0.024 | 1.00 | 1.404 | 0 |
first k with mean slope < 0.9: none up to 12
[elapsed 1166s]

# 2. Harrell m/15 at segment level with design effect (own calculation)
Segment events ESTIMATED: 452 x 2.45 = 1,107 (2.45 from the OLD 1,352-person table); rows 1,076 x 9 = 9,684.
| latent ICC | observed-scale rho (synthetic) | design effect | m definition | m | df = m/(DE*15) | synthetic seg events per 1,076 | synthetic seg per affected |
|---|---|---|---|---|---|---|---|
| 0.1 | 0.045 | 1.36 | min(events, non-events) | 1107 | 54 | 659 | 1.46 |
| 0.1 | 0.045 | 1.36 | 3nq(1-q) [ordinal formula] | 2942 | 144 | 659 | 1.46 |
| 0.3 | 0.111 | 1.89 | min(events, non-events) | 1107 | 39 | 775 | 1.72 |
| 0.3 | 0.111 | 1.89 | 3nq(1-q) [ordinal formula] | 2942 | 104 | 775 | 1.72 |
| 0.55 | 0.268 | 3.15 | min(events, non-events) | 1107 | 23 | 1055 | 2.33 |
| 0.55 | 0.268 | 3.15 | 3nq(1-q) [ordinal formula] | 2942 | 62 | 1055 | 2.33 |

# 4. Power of the k-df LR test at a FIXED noncentrality (same total signal spread over k df)
| noncentrality | k=1 | k=2 | k=3 | k=5 | k=7 | k=9 | k=12 |
|---|---|---|---|---|---|---|---|
| 5.0 | 0.61 | 0.50 | 0.44 | 0.36 | 0.31 | 0.28 | 0.25 |
| 10.0 | 0.89 | 0.82 | 0.76 | 0.68 | 0.61 | 0.56 | 0.50 |
| 15.0 | 0.97 | 0.94 | 0.92 | 0.87 | 0.82 | 0.78 | 0.72 |
| 20.0 | 0.99 | 0.99 | 0.98 | 0.95 | 0.93 | 0.90 | 0.87 |
| 30.0 | 1.00 | 1.00 | 1.00 | 1.00 | 0.99 | 0.99 | 0.98 |
| 42.9 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 44.5 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 49.9 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 51.3 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 54.1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 55.4 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

# 5. Geometry df affordable (Riley binding P_max minus base df; n = 1,076)
Base df (excl. intercept): log FU 1 + SCORE2 1 | factors 6(+1) + dominance 1 + 8 segment dummies + log length 1. The random-intercept SD would add 1 more if counted.
| base | C | P_max (binding) | base df | geometry df left | 5 (no Mundlak) fits? | 7 (Mundlak) fits? |
|---|---|---|---|---|---|---|
| SCORE2 recalibrated | 0.65 | 8.4 | 12 | -3.6 | no | no |
| SCORE2 recalibrated | 0.7 | 15.1 | 12 | 3.1 | no | no |
| SCORE2 recalibrated | 0.72 | 18.5 | 12 | 6.5 | yes | no |
| SCORE2 recalibrated | 0.75 | 24.2 | 12 | 12.2 | yes | yes |
| SCORE2 recalibrated | 15% of max | 14.2 | 12 | 2.2 | no | no |
| refitted factors (6) | 0.65 | 8.4 | 17 | -8.6 | no | no |
| refitted factors (6) | 0.7 | 15.1 | 17 | -1.9 | no | no |
| refitted factors (6) | 0.72 | 18.5 | 17 | 1.5 | no | no |
| refitted factors (6) | 0.75 | 24.2 | 17 | 7.2 | yes | yes |
| refitted factors (6) | 15% of max | 14.2 | 17 | -2.8 | no | no |
| refitted factors + diabetes | 0.65 | 8.4 | 18 | -9.6 | no | no |
| refitted factors + diabetes | 0.7 | 15.1 | 18 | -2.9 | no | no |
| refitted factors + diabetes | 0.72 | 18.5 | 18 | 0.5 | no | no |
| refitted factors + diabetes | 0.75 | 24.2 | 18 | 6.2 | yes | no |
| refitted factors + diabetes | 15% of max | 14.2 | 18 | -3.8 | no | no |

Simulation (person-level OOS calibration slope of aggregated risk), first k with mean slope < 0.9:
  ICC 0.1, extra HR 1.0, base recal: >12; slope at k=5: 0.970, k=7: 0.959, k=12: 0.939
  ICC 0.1, extra HR 1.0, base refit: >12; slope at k=5: 0.929, k=7: 0.924, k=12: 0.910
  ICC 0.3, extra HR 1.0, base recal: >12; slope at k=5: 0.932, k=7: 0.924, k=12: 0.906
  ICC 0.3, extra HR 1.0, base refit: >12; slope at k=5: 0.923, k=7: 0.917, k=12: 0.901
  ICC 0.55, extra HR 1.0, base recal: >12; slope at k=5: 0.970, k=7: 0.960, k=12: 0.945
  ICC 0.55, extra HR 1.0, base refit: >12; slope at k=5: 0.964, k=7: 0.960, k=12: 0.947
  ICC 0.55, extra HR 1.1, base recal: >12; slope at k=5: 0.993, k=7: 0.991, k=12: 0.980
  ICC 0.55, extra HR 1.1, base refit: >12; slope at k=5: 0.979, k=7: 0.976, k=12: 0.965

Total runtime 1166s
