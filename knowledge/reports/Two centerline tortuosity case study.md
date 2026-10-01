# Two RCAs show why κ_a beats arc/chord

Two right-dominant training RCAs of matched length (scan 662, 109.4 mm; scan 518, 104.4 mm) differ by **16 % in arc/chord (1.73 vs 2.00, 44th vs 69th percentile) but by a factor of two in mean local bending κ_a@5 (0.035 vs 0.068 rad/mm, 10th vs 88th percentile)**, and the 3D views side with κ_a: 662 is one smooth C with a small ostial hook, 518 is a C that carries five bends of 45° or more and winds out of its own plane. Arc/chord barely moves because most of any RCA's arc/chord is the half-circle course around the AV groove, and 518's extra 190° of turning alternates in direction and cancels in where the vessel ends up. Of the advanced descriptors, the out-of-plane fraction f_twist (0.15 vs 0.46, 0.7th vs 94.7th percentile), the tangent-sphere spread, multiscale arc/chord and a 3D bend barcode add information the eye confirms; bending energy kB, maximum bend and fine-scale peak or inflection counts are hijacked by 662's 127° ostial take-off hook or by 1 mm ripple and rank the pair the wrong way or nearly tie them; writhe and box-counting dimension are degenerate. The method implications follow directly: settle an ostium rule before any energy-type metric is reported, keep κ_a@5 as primary with arc/chord only as a literature-comparable companion, carry f_twist as the candidate secondary, and drop inflection count, ICM, writhe and box-counting. Everything here rests on two vessels and one observer's reading of the renders, so it illustrates the measures' behaviour and does not validate them.

**Look at the figure first.** The static comparison is below; the interactive version, with linked orthographic cameras (LAO 30, AP, RAO 30), a shared curvature colour scale and a curvature strip that places a cursor on the 3D curve, is at [rca_tortuosity_comparison.html](file:///work3/s254124/imagecasx_results/tortuosity_research/case_study/rca_tortuosity_comparison.html).

![Scans 662 (left) and 518 (right), RCA centerlines in LAO 30 at the same mm scale, coloured by curvature |ψ| (0 to 0.20 mm⁻¹), with bends of 45° or more marked, the ostium to distal chord dashed, and the numbers panel with cohort percentiles](/work3/s254124/imagecasx_results/tortuosity_research/case_study/rca_tortuosity_comparison.png)

## Both vessels trace the same C, and only local bending tells them apart

Both curves are the delivered centerline (label 9), longest geodesic path, oriented ostium to distal, resampled at 0.25 mm with no smoothing beyond the dataset's own σ 0.5 mm; percentiles for simple measures are mid-rank among all **560 training RCAs** ([easy.py](file:///zhome/e2/6/224426/project/ImageCAS-X/tortuosity/research/case_study/easy.py)). The whole-vessel measures say the two are similar: arc/chord 1.73 vs 2.00, and in the standard LAO 30 projection only **1.85 vs 1.94 (5 % apart)**. In RAO 30 the order even reverses (1.40 vs 1.39). A circular arc through angle Φ has arc/chord (Φ/2)/sin(Φ/2), so a pure half-circle already scores π/2 = 1.57 with zero wiggle. 662 turns **218°** in total, barely more than that half-circle, so its arc/chord is almost all course. 518 turns **407°**, but its extra bends form S-shapes at 1 to 20 mm and 61 to 82 mm that cancel in net direction and add path length only to second order, while every degree adds linearly to κ_a ([easy.py](file:///zhome/e2/6/224426/project/ImageCAS-X/tortuosity/research/case_study/easy.py)). Among the 560 RCAs, arc/chord correlates with length at Spearman 0.70 and with κ_a only at 0.53, which is the cohort version of the same effect.

The event counts that a reader would make by eye agree with κ_a: **one bend of 45° or more in 662 (the ostial hook at 2.4 mm) against five in 518 (at 1.8, 15, 34, 66 and 77 mm)**. Pointwise curvature localises 518's excess to 0 to 20 mm and 60 to 80 mm, and 19 % of 518's points sit in 10 mm windows with arc/chord above 1.05 against 1 % for 662. Yet the angiographic Eleid-like grade in LAO 30 is 0 for both, because projection fragments 518's bends into 20 to 43° pieces, so the clinical 2D grade cannot separate a 10th-percentile vessel from an 88th-percentile one ([Eleid 2014](https://pubmed.ncbi.nlm.nih.gov/25138034/); criteria restated in [Tweet 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11605948/)).

## The advanced lens adds planarity and scale, but the ostial hook poisons energy

The advanced descriptors were computed on the centerline smoothed at σ0 1.25 mm, the Bishop curvature spectrum design value, with percentiles placed against **150 training RCAs** that include neither case ([advanced.py](file:///zhome/e2/6/224426/project/ImageCAS-X/tortuosity/research/case_study/advanced.py)). The complex curvature ψ = k1 + i k2 lives in a rotation-minimising frame ([Bishop 1975](https://www.tandfonline.com/doi/abs/10.1080/00029890.1975.11993807); [Wang et al. 2008](https://www.microsoft.com/en-us/research/publication/computation-rotation-minimizing-frames/)). Its RMS magnitude kB nearly ties the pair (**0.086 vs 0.096 mm⁻¹, 66th vs 79th**) because 662 has an 88° turn in its first 6.5 mm with peak curvature 0.56 mm⁻¹ (radius 1.8 mm), holding **74 % of its bending energy in the first third**. Trimming the first 5 mm drops 662's kB by 42 % to 0.050 while 518 barely moves (0.090). κ_a, a first moment over 5 mm chords, sees the short hook only partly; kB, a second moment, is dominated by it. Their ratio (peakedness 1.56 vs 1.10) is a cheap flag for exactly this situation.

Planarity is where the advanced lens pays off. **f_twist, the out-of-plane share of bending energy, is 0.15 vs 0.46 (0.7th vs 94.7th percentile)**, and the W-free tangent-sphere version agrees: the smallest eigenvalue of the tangent covariance is 0.019 vs 0.126 (0 means all directions lie on one great circle), and 518's tangents cover 22 % of the sphere of directions against 15 %. Both best-fit planes are the right AV groove, so the difference is spread about the plane, not which plane. Scale is the third axis: mean windowed arc/chord TI(Δ) favours 518 at every window, with the ratio rising from **1.3× at 2 mm to 3.5× at 20 mm**, and in curvature scale space 518 keeps two turns of 45° or more up to σ 8 mm while 662 collapses to its single hook by σ 4 mm. The 3D bend barcode (constant-sign turns along the local bending axis, a 3D generalisation of [Grisan 2008](https://doi.org/10.1109/TMI.2007.904657)) reads **three turns of 90° or more in 518 (157°, 131°, 110°) against none in 662**.

The remaining descriptors do not earn a place. Writhe is essentially zero for both (−0.009, −0.006; a three-turn helix gives ±1.48), because bending without coiling has no net handedness ([Klenin and Langowski 2000](https://onlinelibrary.wiley.com/doi/10.1002/1097-0282(20001015)54:5%3C307::AID-BIP20%3E3.0.CO;2-Y)). Average crossing number differs 0.15 vs 0.41 and plausibly tracks projection overlap ([Panagiotou et al.](https://arxiv.org/pdf/0907.3805)), but no view shows a self-crossing and heart-size confounding is untested. Box-counting dimension is 0.940 vs 0.938, degenerate for a smooth single trunk. SRVF elastic distance to a straight line (0.80 vs 0.85 rad) is an arc/chord-type quantity and restates it ([Srivastava et al. 2011](https://www.semanticscholar.org/paper/Shape-Analysis-of-Elastic-Curves-in-Euclidean-Srivastava-Klassen/377415d1b8e328c7cf42cd5016dedcac09beb992)); the pairwise elastic distance of 0.46 rad has no cohort scale yet.

## Side by side: which numbers the eye confirms

Percentiles in brackets: simple measures against 560 training RCAs (σ 0), BCS measures against 150 training RCAs (out-of-sample placement); "none" means no cohort distribution exists. The eye column is the rendering author's reading of the LAO 30 figure plus same-scale AP, RAO 30, lateral and superior renders ([visualise.py](file:///zhome/e2/6/224426/project/ImageCAS-X/tortuosity/research/case_study/visualise.py)), not a blind or expert rating.

| Measure | 662 | 518 | Eye agrees? |
|-|-|-|-|
| **Easy** | | | |
| Arc length L (mm) | 109.4 [60] | 104.4 [48] | matched by design |
| Arc/chord L/D, 3D | 1.73 [44] | 2.00 [69] | partly: both look like a similar C; gap far smaller than the visual difference |
| Arc/chord, LAO 30 projection | 1.85 [52] | 1.94 [61] | partly, as above |
| Arc/chord, RAO 30 projection | 1.40 | 1.39 | no: reverses the order |
| κ_a@5 (rad/mm) | 0.035 [10.5] | 0.068 [88.2] | **yes** |
| Total turning (deg) | 218 [24.5] | 407 [82.7] | **yes** |
| SOAM in-plane, 1 mm (rad/cm) | 1.30 [31] | 1.60 [81] | yes in order, contrast compressed by 1 mm noise |
| Bends ≥ 45° (3D) | 1 [27] | 5 [88] | **yes** |
| Bends ≥ 90° (3D) | 1 [82] | 1 [82] | no: tie of an ostial hook and a mid-vessel kink |
| Max bend (deg, position) | 127 at 2.4 mm [89] | 109 at 77 mm [83] | no: set by 662's hook, hidden in LAO 30 |
| Inflections, 1 mm | 55 [84] | 36 [19] | no: reversed, counts wobble and length |
| ICM (Bullitt) | 96.9 [68] | 74.0 [36] | no: reversed, inherits inflections |
| Eleid-like grade, LAO 30 | 0 | 0 | no: neither graded, though 518 is clearly bendier |
| **Advanced** | | | |
| kB, bending energy RMS (mm⁻¹) | 0.086 [66] | 0.096 [79] | no: near tie driven by the ostial hook |
| kB, first 5 mm trimmed | 0.050 | 0.090 | yes |
| Peakedness kB / mean κ | 1.56 | 1.10 | yes: one sharp spot vs spread bending |
| f_twist@1.25 | 0.15 [0.7] | 0.46 [94.7] | **yes**, once the view is rotated |
| f_wiggle@2 | 0.30 [77] | 0.22 [23] | unclear: not checkable by eye |
| Tangent out-of-plane variance | 0.019 | 0.126 | **yes** (lateral view: 662 flat, 518 an S) |
| Mean TI(Δ = 20 mm) | 0.027 | 0.095 | yes: 518's bends are 10 to 40 mm long |
| Barcode turns ≥ 90° | 0 | 3 | **yes** |
| Turns ≥ 45° surviving σ 8 mm | 1 | 2 | yes |
| Curvature peaks, persistence ≥ 0.05 | 11 | 9 | no: reversed, fine-scale ripple |
| ACN, average crossing number | 0.15 | 0.41 | plausible, not checkable in any single view |
| Writhe | −0.009 | −0.006 | n/a: both zero, nothing to see |
| SRVF distance to a line (rad) | 0.80 | 0.85 | partly: restates arc/chord |
| Box-counting dimension | 0.940 | 0.938 | n/a: degenerate |

Every disagreement traces to one of three causes: **noise at the 1 mm scale** (inflections, ICM, persistence peaks, compressed SOAM), **the ostial take-off hook** (max bend, bends ≥ 90°, kB), or **projection** (RAO 30 arc/chord, LAO 30 bend counts and Eleid grade). The measures that agree with the eye all operate at 5 mm or coarser and in 3D.

## Conclusion

The case study changes the ordering of the method's open questions. The ostium is not a detail to settle later: one short take-off hook, whose status as true anatomy or as the extractor's entry from the aortic root cannot be decided from the centerline alone, moved 662's kB by 42 %, decided its max bend, and would remove its only bend of 45° or more if the first 5 to 10 mm were trimmed. So an **ostium rule (a fixed trim or an explicit take-off segment reported separately) must be fixed and pre-registered before kB, max κ, persistence or bend maxima are reported**, and the cohort frequency of such hooks in the delivered centerlines needs measuring first. The pair also sharpens why **κ_a@5 stays primary and arc/chord stays a companion**: arc/chord mostly measures the RCA's obligatory C plus length and is only literature-comparable, while κ_a tracks the bending the eye counts and was stable to smoothing (percentiles 10.5 to 9.1 and 88.2 to 87.9 between σ 0 and 1 mm).

Beyond magnitude, the pair shows that tortuosity has at least two further visible axes, **planarity and bend scale**, which κ_a does not capture. f_twist is the natural **candidate secondary**, backed by its W-free tangent-sphere twin and a spatial map, with multiscale TI(Δ) at 10 to 20 mm and the 3D barcode count of turns of 90° or more as exploratory descriptors. **Drop inflection count, ICM, writhe, box-counting dimension, fine-scale peak counts and SRVF distance to a line**, and never quote a single-view 2D arc/chord or Eleid grade as a ranking. None of these conclusions carries population weight: no new descriptor has a cohort distribution, a jitter or truncation reliability check, or agreement against CAS-Net-extracted centerlines, and the blind expert ranking (Kendall τ) remains the proper test of "agrees with the eye".
