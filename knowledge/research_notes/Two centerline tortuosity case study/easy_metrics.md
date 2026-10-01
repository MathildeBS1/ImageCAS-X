# Classical tortuosity measures on two RCAs: scan 662 (low κ_a) vs scan 518 (high κ_a)

Population and provenance for every number below. Two ImageCAS-X training scans, both right-dominant, RCA only (label 9), delivered centerline `$ImageCAS_X_data_path/centerlines/{id}.coronary_right_centerline.vtk`. Path = longest geodesic path of label 9 (`tortuosity/vessels.py`), oriented ostium to distal with the VTK `start_points` array (the start point coincides with the first path vertex in both cases, offset 0.00 mm). Resampled at 0.25 mm arc length, **no extra smoothing** (σ = 0) for the primary numbers because the delivered centerlines are already skeleton plus Gaussian σ = 0.5 mm over 5 vertices; σ = 1 mm is the sensitivity column. Percentiles are mid-rank percentiles among all **560 training RCAs** (none missing) from `simple_measures_sigma0.csv` (σ = 0) or `simple_measures.csv` (σ = 1 mm). Script: [easy.py](file:///zhome/e2/6/224426/project/ImageCAS-X/tortuosity/research/case_study/easy.py) (reuses `smooth`, `turns`, `soam_icm`, `view_dir`, `basis` from [compute_simple.py](file:///zhome/e2/6/224426/project/ImageCAS-X/tortuosity/research/simple/compute_simple.py)). Outputs: [easy_metrics.json](file:///work3/s254124/imagecasx_results/tortuosity_research/case_study/easy_metrics.json) (52 entries per case: 26 measures × σ 0 and σ 1 mm) and [easy_pointwise.npz](file:///work3/s254124/imagecasx_results/tortuosity_research/case_study/easy_pointwise.npz) (keys `{id}_xyz`, `{id}_s`, `{id}_turn5`, `{id}_bends45`, `{id}_ti10`, plus an extra `{id}_bends45_deg` with the matching bend angles). The Disease column was not read.

## Per-case values: formulas, numbers, percentiles, and why the two differ

### Takeaway
Length is matched (109.4 vs 104.4 mm) and whole-course arc/chord differs by only 16 % (1.73 vs 2.00, 44th vs 69th percentile), but local bending doubles: κ_a@5 0.035 vs 0.068 rad/mm (10th vs 88th percentile), total turning 218° vs 407°. 662 is a smooth C that turns barely more than the half-circle its AV-groove course needs; 518 carries about 190° of extra turning in five 45 to 110° bends at 2, 15, 34, 66 and 77 mm.

### Cited Findings

**Formulas used** (conventions from the earlier recipe in [Centerline tortuosity normal ranges.md](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Centerline%20tortuosity%20normal%20ranges.md); DM, ICM and SOAM originally from [Bullitt 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)):
- L = arc length of the 0.25 mm-resampled path; D = |P_end − P_start|; DM = L / D (Bullitt distance metric); TI = DM − 1.
- DM2 (view) = L/D of the path projected on the plane normal to d = (sin α cos β, −cos α cos β, sin β) in LPS; α = LAO angle (RAO negative), β = cranial. LAO 30 = α 30, β 0 (the standard RCA view in the recipe); RAO 30 = α −30, β 0.
- κ_a@5 = Σ θ_j / L, where the path is chord-resampled at exactly 5 mm Euclidean steps from the ostium, u_j are unit chord vectors, θ_j = arccos(u_j · u_{j+1}). Total turning = Σ θ_j = κ_a × L.
- SOAM in-plane = Σ IP_k / (L/10) with IP_k the turning angle between consecutive 1 mm chords (rad/cm); the torsion term is left out because it reads 7.1 to 7.3 rad/cm on every trunk (noise), per the recipe report.
- Inflections = number of Frenet-normal flips (ΔN·ΔN > 2) between consecutive 1 mm vertices whose turning exceeds 0.02 rad per mm; ICM = DM × (n_infl + 1) ([Bullitt 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)).
- Bends = maximal runs of 1 mm chord vertices turning more than 0.02 rad/mm (radius < 50 mm), split where the binormal flips; bend angle = cumulative turning over the run; position = turning-weighted mean arc length of the run's vertices ("centre"), with start and end arc lengths also given.
- Eleid-like grade per vessel: 1 = ≥3 curvatures of 45 to 90°, 2 = ≥3 of 90 to 180°, 3 = ≥2 of ≥180° ([Tweet 2024 restating Eleid, PMC11605948](https://pmc.ncbi.nlm.nih.gov/articles/PMC11605948/); original [Eleid 2014, PubMed 25138034](https://pubmed.ncbi.nlm.nih.gov/25138034/)). The 2 mm diameter qualifier is ignored (no radius used); "consecutive" is computed two ways: loose (any 3 in the class) and strict (adjacent in the bend list).
- turn5(s) (pointwise): angle between the chord from the point 5 mm (Euclidean) behind to P(s) and the chord from P(s) to the point 5 mm ahead, divided by half the arc between those two points (rad/mm); NaN within about 5 mm of either end. Its mean over the vessel reproduces κ_a (662: 0.0333 vs 0.0348; 518: 0.0707 vs 0.0680).
- ti10(s) (pointwise): 10 mm / chord between P(s − 5 mm) and P(s + 5 mm) (arc positions); NaN in the first and last 5 mm.

**Values, σ = 0 (primary). Percentile among 560 training RCAs in brackets; "n/a" where no cohort column exists.** All from [easy.py](file:///zhome/e2/6/224426/project/ImageCAS-X/tortuosity/research/case_study/easy.py) output.

| Measure | 662 | 518 | Plain-language reading of the difference |
|-|-|-|-|
| L (mm) | 109.4 [60] | 104.4 [48] | matched by design |
| D (mm) | 63.3 [73] | 52.2 [24] | 518's ends are 11 mm closer: its path folds more |
| DM = L/D | 1.730 [44] | 2.001 [69] | only 16 % apart: both are dominated by the RCA's C-shaped course |
| TI = DM − 1 | 0.730 | 1.001 | 37 % apart; subtracting the straight-line baseline widens the gap |
| DM2 LAO 30 | 1.847 [52] | 1.940 [61] | only 5 % apart in the standard angiographic view |
| DM2 RAO 30 | 1.403 [n/a] | 1.386 [n/a] | **reversed**: in RAO 30 662 reads (marginally) more tortuous |
| κ_a@5 (rad/mm) | 0.0348 [10.5] | 0.0680 [88.2] | 518 turns twice as much per mm at the 5 mm scale |
| total turning (rad) | 3.81 [24.5] | 7.10 [82.7] | |
| total turning (deg) | 218 | 407 | 662 ≈ a half-circle (180°) plus 38°; 518 ≈ 1.1 full turns |
| SOAM in-plane (rad/cm) | 1.30 [31] | 1.60 [81] | only 23 % apart: at 1 mm steps the noise floor fills both |
| inflections | 55 [84] | 36 [19] | **reversed**: counts 1 mm-scale wobble, grows with length |
| ICM | 96.9 [68] | 74.0 [36] | **reversed**, inherits the inflection count |
| bends ≥ 45° | 1 [27] | 5 [88] | 518 has five clear bends, 662 one (the ostial hook) |
| bends ≥ 90° | 1 [82] | 1 [82] | tie: 662's is the ostial hook, 518's is at 77 mm |
| max bend (deg) | 126.8 at 2.4 mm [89] | 109.4 at 77.0 mm [83] | **reversed** by 662's ostial take-off hook |
| bends ≥ 45° in LAO 30 | 1 [55] | 0 [20] | **reversed**: 518's bends are split into 20 to 43° pieces in projection |
| bends ≥ 90° in LAO 30 | 0 | 0 | tie |
| Eleid-like grade, 3D loose | 0 | 1 | 518 has four 45 to 90° bends |
| Eleid-like grade, 3D strict consecutive | 0 | 0 | 518's 45 to 90° bends are separated by smaller ones |
| Eleid-like grade, LAO 30 | 0 | 0 | neither qualifies angiographically |
| ti10 max (whole vessel) | 1.19 at 5.0 mm | 1.09 at 5.0 mm | both maxima sit in the first window, i.e. the ostial take-off |
| ti10 max beyond 10 mm | 1.035 at 69.7 mm | 1.084 at 16.7 mm | 518's worst 10 mm window is more than twice as folded (TI 0.084 vs 0.035) |
| turn5 peak position | 6.2 mm | 15.2 mm | 662 peaks at the take-off; 518 in its proximal S-bend |

**Bend lists (σ = 0, 3D; start, centre, end in mm from ostium; cumulative angle), bends ≥ 45° bold.** From the script's printed table.
- 662: **1.0 / 2.4 / 6.0, 126.8°** (ostial take-off); then only bends of 20 to 37°: 26.6 mm 22°, 62.3 mm 24°, 67.8 mm 37°, 80.7 mm 37°, 83.5 mm 23°, 88.1 mm 21°, 90.2 mm 24°, 92.3 mm 31°, 100.4 mm 20°, 104.2 mm 25°.
- 518: **1.0 / 1.8 / 3.0, 54.6°**; 5.1 mm 27°; 10.5 mm 43°; **14.0 / 15.0 / 16.0, 47.6°**; 19.3 mm 37°; 30.7 mm 28°; **32.2 / 34.0 / 37.2, 75.6°**; 41.5 mm 23°; 46.9 mm 33°; 49.9 mm 21°; 53.9 mm 33°; **61.2 / 65.7 / 69.2, 72.8°**; **70.2 / 77.0 / 82.2, 109.4°** (the only ≥ 90° bend); 85.8 mm 22°; 91.9 mm 25°; 93.6 mm 32°; 97.6 mm 21°.
- `{id}_bends45` in the npz = the bold centres: 662 [2.4]; 518 [1.8, 15.0, 34.0, 65.7, 77.0].

**Profile along the vessel, σ = 0, mean over 10 mm bins (bin start mm: mean ti10, mean turn5 rad/mm).**

| bin | 662 ti10 | 662 turn5 | 518 ti10 | 518 turn5 |
|-|-|-|-|-|
| 0 | 1.041 | 0.034 | 1.053 | 0.089 |
| 10 | 1.007 | 0.029 | 1.063 | 0.102 |
| 20 | 1.010 | 0.031 | 1.024 | 0.045 |
| 30 | 1.006 | 0.026 | 1.039 | 0.071 |
| 40 | 1.007 | 0.028 | 1.023 | 0.053 |
| 50 | 1.008 | 0.029 | 1.025 | 0.067 |
| 60 | 1.022 | 0.058 | 1.047 | 0.098 |
| 70 | 1.019 | 0.041 | 1.055 | 0.102 |
| 80 | 1.016 | 0.029 | 1.028 | 0.054 |
| 90 | 1.016 | 0.026 | 1.019 | 0.032 |
| 100 | 1.017 | 0.045 | (end) | (end) |

Median ti10 over the vessel: 662 1.011, 518 1.032; fraction of points with ti10 > 1.05: 662 1.1 %, 518 19.1 %.

**Sensitivity, σ = 1 mm** (JSON entries with suffix " (sigma 1 mm)"): DM 1.693 vs 1.957; DM2 LAO 30 1.817 vs 1.909; DM2 RAO 30 1.354 vs 1.343 (still reversed); κ_a 0.0336 [9.1] vs 0.0664 [87.9]; total turning 207° vs 389°; SOAM in-plane 0.60 vs 0.93 rad/cm; inflections 14 vs 7 (still reversed); bends ≥ 45° 1 vs 4; bends ≥ 90° 0 vs 2; max bend 75° at 2.1 mm vs **226° at 64.8 mm**; LAO 30 bends ≥ 45° 0 vs 2 (now in the "right" order); Eleid-like grades all 0. At σ = 1 mm 518's bends merge: 1 to 25 mm becomes one 160° bend, 44 to 83 mm one 226° bend.

**Length-matched context** (right-dominant RCAs with L 90 to 125 mm, n = 351, σ = 0, same csv): κ_a percentile 9.4 (662) and 91.7 (518); DM percentile 37.6 and 68.9. Cohort medians of all 560 training RCAs at σ = 0: L 105.6 mm, DM 1.80, DM2 LAO 30 1.83, κ_a 0.046 rad/mm, bends ≥ 45° 2, bends ≥ 90° 0, max bend 69°, inflections 45; 44 % of RCAs have ≥ 3 bends ≥ 45° ([simple_measures_sigma0.csv](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/simple_measures_sigma0.csv)).

**Orientation note.** κ_a depends on which end the 5 mm chord walk starts from. For 518 the unoriented cohort csv gives 0.0636 rad/mm; oriented ostium-first it is 0.0680 (7 % higher; percentile 88 either way). For 662 the csv path was already ostium-first (0.0348 in both). The coordinator's "≈ 0.064" for 518 is the unoriented value.

### Inferences
- The key visual check: 662 should look like one smooth C with a short hook at the ostium and nothing else; 518 should show an S-like wiggle in the first 20 mm (bends at 2, 15 and 19 mm), a kink at about 34 mm, and a double bend at 66 to 77 mm near the crux.
- The 127° "max bend" of 662 at 1 to 6 mm is the take-off from the aorta: the first 2 mm run anteriorly (−y) then turn rightward (−x). It is real anatomy at the ostium but lies within one 5 mm chord of the path end, so κ_a sees it only partly while the 1 mm bend detector and ti10 see it fully. At σ = 1 mm it drops to 75°. A method that trims the first 5 to 10 mm would remove 662's only ≥ 45° bend.
- Both vessels are "not tortuous" by the angiographic (LAO 30) Eleid criterion and by the strict consecutive reading, so the angiographic grade does not separate a 10th-percentile from a 90th-percentile κ_a case.

### Gaps
- The Eleid diameter qualifier (2 mm) could not be applied: no radius array was read (the recipe notes that the radius array has not been checked on a file).
- No cohort percentiles for DM2 RAO 30, Eleid grade, ti10 or bend positions: the cohort csv has no such columns and the task limited computation to the two scans.
- No expert or angiographic reading of these two vessels exists to say which bends a cardiologist would count.

## Which measures agree on which case is more tortuous, which disagree, and why

### Takeaway
518 > 662 on DM, TI, DM2 LAO 30, κ_a, total turning, SOAM in-plane, 3D bends ≥ 45°, the loose Eleid-like grade and the local ti10 profile. The ranking reverses on inflections, ICM, max bend, DM2 RAO 30 and LAO 30 bend count at σ = 0, and ties on bends ≥ 90°. Every reversal traces to one of three things: noise at the 1 mm scale, the ostial take-off hook, or projection.

### Cited Findings
- Ranking table as above; all values from [easy.py](file:///zhome/e2/6/224426/project/ImageCAS-X/tortuosity/research/case_study/easy.py).
- Across 560 training RCAs (σ = 0), Spearman ρ: DM vs κ_a 0.53, DM vs L 0.70, κ_a vs L 0.33, DM vs DM2 LAO 30 0.97, κ_a vs bends ≥ 45° 0.72, inflections vs L 0.78, inflections vs κ_a −0.01 ([simple_measures_sigma0.csv](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/simple_measures_sigma0.csv), computed here).
- The earlier recipe found bend counts are the only simple measure that moves with smoothing (Spearman 0.64 to 0.78 between σ 0 and 1 mm) and that full SOAM is noise-dominated ([Centerline tortuosity normal ranges.md](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Centerline%20tortuosity%20normal%20ranges.md)).

### Inferences
- **Why arc/chord moves 16 % while κ_a doubles.** An arc of a circle through angle Φ has DM = (Φ/2) / sin(Φ/2); a half-circle (Φ = 180°) gives DM = π/2 = 1.57 with zero local wiggle. Most of any RCA's DM is this C around the AV groove. 662 turns 218° in total, close to the half-circle, so its DM 1.73 is nearly all course. 518 turns 407°: about 190° more, but those extra bends alternate direction (S-shapes at 1 to 20 mm and 61 to 82 mm) and so largely cancel in where the vessel ends up; they add path length only as the cosine of small deviations, a second-order effect. So D shortens by 11 mm and DM rises only 0.27, while every degree of the extra turning adds linearly to κ_a.
- **Inflections and ICM reverse** because at 1 mm steps the Frenet normal flips on sub-millimetre wobble of the centerline (55 flips in 109 mm is one every 2 mm), so the count scales with length and point noise (ρ 0.78 with L, −0.01 with κ_a). 662 is 5 mm longer and its long straight stretches, having near-zero curvature, let the normal spin freely. Not a tortuosity signal at this scale.
- **SOAM in-plane barely separates them** (1.30 vs 1.60 rad/cm at σ 0) for the same reason: at 1 mm the per-step turning is about 4 times the 5 mm κ_a (1.30 rad/cm vs 0.35 rad/cm for 662), i.e. most 1 mm turning is wobble that cancels over 5 mm. With σ = 1 mm the ratio widens to 0.60 vs 0.93, closer to κ_a's ratio.
- **Max bend reverses** because it is a single-event statistic and 662's single event is the ostial take-off (127°), larger than any of 518's mid-vessel bends at σ 0. At σ 1 mm 518's bends merge into a 226° bend and the order flips back, showing max bend is set by the split/merge rule as much as by the anatomy.
- **Bends ≥ 90° tie** for two different reasons (ostial hook vs mid-vessel kink), which is why the count needs positions to be interpretable.
- **2D measures**: in LAO 30 the DM2 gap shrinks to 5 % and in RAO 30 it reverses (1.40 vs 1.39), because projection removes whatever part of 518's bending runs along the view direction; a single-view angiographic arc/chord cannot be trusted to rank these two. 2D bend counts at σ 0 reverse because in 2D every sign change of signed curvature splits a bend, so 518's bends fragment into 20 to 43° pieces; at σ 1 mm they re-form (2 vs 0).

### Gaps
- Whether the ostial hook should count at all (anatomical take-off vs RCA tortuosity) is a definition choice not settled by the literature reviewed in the earlier reports.

## What each measure is sensitive to, illustrated by these two cases

### Takeaway
Arc/chord and total turning split cleanly into "global course" and "local bends": DM mostly reports the RCA's C-shape plus length, κ_a and total turning report every bend whether or not it changes where the vessel ends up, and bend counts and max bend report discrete events whose number and size depend on smoothing and the split rule. Pointwise turn5 and ti10 localise the difference: 518's excess sits at 0 to 20 mm and 60 to 80 mm.

### Cited Findings
- κ_a at σ 1 mm moves 3.5 % (662) and 2.4 % (518) from σ 0, and its percentiles barely move (10.5 to 9.1; 88.2 to 87.9); DM moves about 2 %; bends ≥ 90° go 1 → 0 (662) and 1 → 2 (518); max bend goes 127° → 75° (662) and 109° → 226° (518); inflections go 55 → 14 and 36 → 7 ([easy.py](file:///zhome/e2/6/224426/project/ImageCAS-X/tortuosity/research/case_study/easy.py)).
- Earlier cohort result: σ 1 mm changes κ_a medians by 2 to 4 % (ρ 0.98 to 0.99) and arc/chord by about 1 % (ρ 0.999), bend counts ρ 0.64 to 0.78 ([Centerline tortuosity normal ranges.md](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Centerline%20tortuosity%20normal%20ranges.md)).
- Arc/chord is dominated by long wavelengths, length and truncation (it is approximately the moment −2 of the curvature spectrum), per the earlier report's Bishop-spectrum analysis ([Centerline tortuosity normal ranges.md](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Centerline%20tortuosity%20normal%20ranges.md)).

### Inferences
- **DM / TI / DM2**: sensitive to the global course (how far the end is from the start). Blind to bends that cancel. Adding a C-course or 5 mm of length moves it as much as adding a bend. Two vessels with the same DM can have very different local bending (here DM differs by 16 %, κ_a by 95 %). Projected DM additionally depends on view.
- **κ_a@5 / total turning**: sensitive to every turn larger than the 5 mm chord scale, additive, so S-bends count fully. Insensitive to sub-5 mm wobble (hence stable across σ) and partly blind to a bend within 5 mm of an endpoint (662's hook). Does not say where the bending is; turn5 does.
- **SOAM in-plane (1 mm)**: same idea as κ_a but at 1 mm, so it mixes in centreline noise; the contrast is compressed at σ 0.
- **Inflections / ICM**: sensitive to noise and length at 1 mm steps, not to bends; reversed here.
- **Bend counts, max bend, Eleid-like grade**: event statistics; sensitive to threshold (≥ 45°, ≥ 90°), the floor (0.02 rad/mm), the split rule at binormal flips, smoothing (bends merge at σ 1 mm) and projection. They are what a person counts by eye, which is why positions are provided, but a single event (the ostial hook) can decide them.
- **ti10 profile**: localises course folding at a 10 mm scale; both vessels are nearly straight over 10 mm almost everywhere (median TI10 0.011 vs 0.032), so it highlights where 518 bends (proximal 0 to 20 mm and 60 to 80 mm) and shows that 662's only standout is the take-off.

### Gaps
- No synthetic-curve check was run here; the monotonicity and invariance tests are criterion 1 in `tortuosity/CLAUDE.md` and belong to the method-selection stage.
- Only two vessels: nothing here estimates reliability; statements about stability rely on the earlier 560-scan sensitivity runs.
