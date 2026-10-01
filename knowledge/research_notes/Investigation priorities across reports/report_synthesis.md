# Cross-report synthesis (R1 to R5)

Read-only repo checks 2026-09-26. No Disease column, no val/test data opened.

**Sources.** R1 = "Merged tortuosity methods for coronaries" (2026-09-22 22:34); R2 = "Alternative tortuosity merges for coronaries" (09-22 23:23); R3 = "Choosing a coronary tortuosity descriptor" (09-25 22:47); R4 = "Vessel specific tortuosity math and tests" (09-25 23:46); R5 = "Plaque prone regional geometry descriptors" (09-26 03:28). Each cites its predecessor as "the earlier report", so they form one chain. R5 shifts from vessel tortuosity to plaque-onset regional geometry.

## 1. Recommendations and how many reports back each

**All five:** extractor agreement, reference centerlines vs centerlines extracted from CAS-Net predictions on the 160 test scans, ICC plus Bland-Altman (R1 "Noise, not geometry…", R2 Step 8, R3 Step 7, R4 Conclusion first priority, R5 Priority 1). R4: this error spectrum "alone decides whether ℓ = 5 or 8 mm and σ = 1 or 2 mm". Never run; no extractor and no CAS-Net predictions exist.

**Three or four (mostly run in scratch by R4/R5):**
- Synthetic suite: R1, R2 Step 1, R3 Step 1; run by R4.
- Noise calibration, independent and correlated jitter: R2 Step 2, R3 Step 2; run by R4 with closed-form noise laws. R4's correlated-error diagnostic not run on real centerlines.
- Rank stability across ℓ and σ: R1, R2 Step 3, R3 Step 3; run by R4.
- Jitter ICC: R1, R2 Step 4, R3 Step 4; run by R4 and R5.
- Floor/ceiling fractions: R1 ("decisive experiment"), R2 Step 6, R3 Step 6.
- Confounds (length, radius, Image Quality, Dominance): R1, R2 Step 7, R3 Step 6; run by R4, R5.
- Pre-register thresholds, lock, then open Disease: R1, R2 Step 9, R3 Step 8, R4, R5 Priority 0. Never done.
- NaN rows plus length floor: all reports, floor value disagrees (section 2).
- Paper-review pass on abstract-level sources: R1, R3, R5.

**Two reports:**
- Truncation test: proposed R3 Step 5, run by R4. Key finding: whole-vessel TI ICC 0.60 on LAD after 20 mm distal cut.
- Compositionality check: R2 Step 5, R3 Step 5. Not run.
- Vessel tie-break sensitivity: R3. Not run.
- Partial Spearman for Q and turn layer given primaries: R2, R3.
- Blind expert ranking, at least 2 raters: R1, R2.
- Explicit C-shape vs S-shape decision: R1, R2.
- Heart-size proxy: R3, R5.
- Graph ablations against a tokenised baseline: R3 Step 9, R5 Priority 5.
- Mixed model: R4 (vessel fixed, patient random); R5 (logistic with Mundlak term, GEE sensitivity, power ~345 patients).

**One report only:**
- R1: fraction of vessels scoring zero on 3D Grisan (n = 1); ℓ tied to lumen radius.
- R2: read one VTK first (Step 0); keep torsion and SOAM as documented rejections.
- R3: restore topology/ files and label_map.json; σ grid {0.5,1,2} mm, ℓ grid {2,3,5,8,10} mm; power at OR 1.05 to 1.09 per SD.
- R4: RCA detrended κ_a sensitivity; LAD-to-D1 landmark segment sensitivity; split PDA by dominance; Darboux geodesic curvature as literature gap; bias cap |bias| ≤ 10 %; log or rank-inverse-normal z-scores; split criterion 6, criterion 8 post-lock; confirm on explicitly listed unused training scans.
- R5: read PARADIGM "how early" (JCCT 2023) in full; CGPS region labeller plus arc-length fallback; SRVF Karcher templates validated by D1/OM1 take-off clustering; open-end SRVF for truncated trees; τ̂ shear proxy vs CFD; H1 persistence token; ramus flag; model OM1 absence; reliability ratio λ from short-interval repeats; confirm CGPS serial subset and plaque-reading protocol with supervisors.

## 2. Contradictions, supersession, current best conclusion

- κ_a: companion (R1) → co-primary (R2) → Primary 2 (R3) → sole primary at ℓ 5 mm, σ 1 mm (R4) → kept as regional κ_l5 (R5).
- Q: co-primary (R2) → exploratory (R3) → dropped (R4, R5).
- Arc/chord TI: baseline (R1) → comparator (R2) → Primary 1 (R3) → secondary "course" variable adjusted for length and dominance (R4) → dropped as local descriptor (R5).
- Turn layer: binormal flip (R1) → parallel-transport challenger (R2) → sensitivity (R3) → bend density ICC 0.49 to 0.71 (R4).
- Torsion: dropped R3, R4, R5.
- SRVF: only R5, for correspondence/tokens, not as tortuosity index.

Reversals: κ_a vs amplitude turnover is a property of the definition (R4), not estimator failure. Q is non-monotone even noise-free (R4; median 1.28 to 1.43 near pure-noise 4/π), against R2. TI most jitter-robust but least truncation-robust (R4 vs R3). Noise: R3 "3× noise-dominated"; R4 ratio 3.6 to 4.1 but independent-jitter floor only 2 to 4 % at 5 mm; correlated error is the real risk. Pooled L/D median 1.45 (R3) should not be reported: RCA and LAD differ by 2.5×.

Unresolved: length floor (R2 ~15, R3 25, R4 20 mm; R5 uses 2 to 17 mm windows with 5 mm chord). Radius weighting: R2/R3 drop it (Hart 1999); R5 revives κ·r without addressing Hart. Single pre-registered primary: R3 TI, R4 κ_a, R5 LM daughter angle; not reconciled.

R4 internal inconsistency: headline says κ_a keeps ranking across whole grid; notes give P100 min ρ 0.86 on LCx, below the 0.9 bar.

Best-evidenced: R4 for tortuosity (κ_a primary), still exploratory by its own statement. R5 complements rather than supersedes.

## 3. Tested on ImageCAS-X vs argued

- R1: literature and derivation only.
- R2: noise-free numpy synthetic checks only.
- R3: 20 test-split cases (40 sides, 61 vessels). Point spacing 0.45 mm, no radius array, step angle 5.9°; trees built for 1,584/1,600 sides; 26/255 segments < 10 mm; LM median 10.1 mm. Conflicts with reserving test for extractor agreement.
- Between R3 and R4: tortuosity/run_merged_tests.py on all 560 training scans, 0.5 mm independent jitter at ℓ 4 mm. SCC density ICC 0.74/0.64/0.50 (LAD/LCx/RCA), 3D Grisan 0.83/0.80/0.82. Output /work3/s254124/imagecasx_results/tortuosity_merged/.
- R4: P150 (first 150 training ids), P100 (rng(0)). TI vs length ρ 0.70 to 0.83. RCA TI by dominance 0.29 vs 0.81 on only 8 left + 3 co-dominant. 20 mm distal cut: ICC TI 0.60/0.81/0.83, κ_a 0.95/0.88/0.93. Correlated 0.5 mm error over 1 mm: κ_a ICC 0.87/0.76/0.71, fails 0.90 gate. Image Quality |ρ| ≤ 0.16.
- R5: 100 training scans (rng(0)+rng(1)), 30 curves SRVF prototype. LCx-OM1 present 80/100. Six tangent rules differ median 18.7° (LM), 27.2° (LAD-D1). κ_l5 ICC 0.97 to 0.99; torsion 0.24 to 0.41. LM Finet 0.63. SRVF 1-NN vessel-type separation 0.90 → 0.93 only. 95/100 right-dominant.

Samples overlap; no confirmation set listed. Every ICC is sensitivity of a single reference centerline to synthetic perturbation; none uses real extractor error, cardiac phase or scanner variation. No expert ranking; validity untested.

## 4. Blockers and reproducibility debts (checked 2026-09-26)

Still blocking: docs_thesis/label_map.json missing (recover via `git show 5742f47:docs_thesis/label_map.json`). topology/paths.py:42 OUTPUT_ROOT defaults to /dtu/blackhole; env.sh does not set IMAGECASX_OUT. segmentations_resampled/, volumes*, imagecas_orig_labels, centerline_samples absent; CLAUDE.md "State of the data" stale.

Cleared: topology/ core files staged; `import topology.graph` works.

Debts: R4/R5 numbers come only from /tmp scratch scripts (95342cdc…/scratchpad/{pervessel,repro,math}, 389c400f…/scratchpad/{regional,treemath}). tortuosity/merged.py, vessels.py, run_merged_tests.py untracked, implement R1's superseded method. No threshold committed with a date. tortuosity/CLAUDE.md still lists radius array as unchecked. Junction sharing unresolved. Nothing exists for CAS-Net centerline extractor, predictions, or CGPS region labeller.

Order: (1) restore label_map.json; (2) set IMAGECASX_OUT to /work3; (3) rebuild segmentations_resampled or record native-spacing EDT radius as method, fix CLAUDE.md; (4) commit tortuosity/ and topology/; (5) commit dated thresholds and bias cap before rerun; (6) port /tmp scripts (most time-critical); (7) list unused training ids for confirmation (< 460 remain); (8) rerun, then build extractor and CAS-Net inference for extractor agreement.

## 5. Marked unverified, abstract-only, or gap

Shared gap (R2, R3, R4): no coronary CTA ICC, CV or Bland-Altman exists for any tortuosity metric; framed as thesis contribution.
- R1: Bribiesca-Sánchez 2024 and Bullitt 2003 threshold (resolved by R2); Bribiesca 2013; Johnson and Dougherty 2007; Gabrielides and Sapidis 2020; retinal SCC; Ferrari HMM. "No 3D Grisan port" rests on ~3 searches.
- R2: many abstract-only (aorta ICC, De Nisco, Selvarasu, Moon, Vorobtsova, Barb); PLOS One 2025 labels conflict; no coronary FFR, no 3D merged-composite gain, no coronary ICC.
- R3: outcome evidence abstract-level (Sharfo, CArTI, ICONIC); robustness figures cross-organ; supervisor "fragile" claim untested on coronary CTA.
- R4: entirely exploratory; correlated-error diagnostic not run; dominance on n = 11; baseline scale arbitrary; no Darboux literature; Liao 2002 abstract only.
- R5: PARADIGM, Stone, Samady, Wang, Medrano-Gracia, Finet, Murray sources, van der Giessen, SRVF theory, Frost and Thompson, Fuchs all abstract/snippet/prior-knowledge level; Shen 2025 and Zhang 2023 preprints; no coronary SRVF study; power assumptions ρ = 0.1 and OR 1.3 assumed; CGPS protocol not public; OM1 absence not image-checked; no window sweep; ramus not stratified.
