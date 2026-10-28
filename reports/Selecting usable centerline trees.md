# Grade each artery's path, then ask Kit

The best-qualified selection of the 744 centerline trees treats each artery on its own. For LAD, LCx and RCA, find the geodesic path from an inferred ostium to the most distal trunk label, and grade that path, not the summed label lengths, as **strict**, **acceptable** or **excluded**. LM gets its own tier and serves only as the plaque-free gate for the LAD and LCx models. The QC report bounds what is possible: at most **576 LAD, 581 LCx and 553 RCA trees are strict** (567 RCA if dRCA is not required), and LM is present in **684** ([report_qc.md](../CGPS_data/report_qc.md)). The real counts will be lower, because the new path checks (order, foreign and unlabelled length on the path, jumps, minimum trunk length, fragments) have no counterpart in the QC. The script that computes them, `CGPS_data/centerline_selection.py`, is written and tested on synthetic data but has not yet run on the real data. One question comes before any threshold: **which visit the trees come from**. The file name `centerlines_hø_10Y.zip` points to the 10-year follow-up scan. If so, the trees cannot be baseline predictors, and outcome-dependent selection bias would undermine the whole design. Second, the laptop copy of `report_qc.md` lists case IDs, so it should not stay there.

## Strict and acceptable tiers come from path checks, not QC flags

The QC flags are poor selectors. Only **45 of 744 trees carry no red flag**. Most flags reflect side-branch features that do not touch a trunk: `unknown_labels` (546 cases), `>2_components` (396) and `unlabelled>20%` (287) ([report_qc.md](../CGPS_data/report_qc.md)). The unnamed codes touch trunks the way side branches do (#18 at pLAD/mLAD, #21 at dLAD, #28 at pCx). Among the 366 trees complete in all three trunks, 226 have exactly two components once pieces under 10 mm are ignored, which is the normal left plus right pair. Excluding on these flags would discard good trunks. The flags that matter are the ones the QC never computes. Its "joined" test checks contact, not proximal-to-distal order. It does not locate the ostium, separate the trunk's own label from same-label twigs, measure foreign or unlabelled length on the trunk, or detect cycles ([centerline_qc.py](../CGPS_data/centerline_qc.py)).

The selection script therefore walks the trunk the way the ImageCAS-X code does ([tortuosity/vessels.py](../tortuosity/vessels.py)). It takes the geodesic path from the ostium to the farthest node with the most distal trunk label (dLAD, LCx, dRCA), so a same-label side twig cannot stand in for the trunk. The files carry no ostium flag. On the left, the ostium is the LM end point farthest from pLAD (for LAD) or pCx (for LCx). Without an LM, and on the right, it is the end of the first segment farthest from the next one. If the next segment is missing, the direction is unknown and the trunk is excluded. Every metric is then measured on that path. The thresholds come from the report's own distributions. Point spacing is **0.5 mm in every case**, with **0 gaps** and at most one join, so a 1.5 mm edge is a safe jump test. The segment 5th percentiles (pLAD 7.7 mm, pCx 12.5 mm, LCx 9.7 mm, pRCA 22.3 mm) mean a 5 mm per-segment minimum removes only broken tails ([report_qc.md](../CGPS_data/report_qc.md)). The acceptable-tier trunk minimum of 30-40 mm protects the planned taper fit. `tortuosity/taper.py` drops the first 3 mm and the zones near junctions, and returns NaN with less than 20 mm of usable arc ([taper.py](../tortuosity/taper.py)).

| Criterion (on the ostium-to-distal path) | Strict | Acceptable |
|---|---|---|
| Required segments | LAD p/m/d; LCx pCx + LCx(13); RCA p/m/d | LAD p/m; LCx pCx + LCx(13); RCA p/m |
| Minimum length per required segment | 5 mm | 3 mm |
| LM on the path (LAD, LCx) | 2-35 mm, ostium a free end | may be absent |
| Label order proximal to distal | required | required |
| Foreign label on the path | ≤ 1 mm | ≤ 3 mm |
| Longest unlabelled stretch / share | ≤ 2 mm / ≤ 5 % | ≤ 5 mm / ≤ 15 % |
| Largest step | ≤ 1.5 mm | ≤ 1.5 mm |
| Trunk length after LM (LAD / LCx / RCA) | 70 / 40 / 70 mm | 40 / 30 / 40 mm |
| Trunk-label fragment elsewhere, cycle, left/right mixing | none (fragment ≤ 5 mm) | allowed, counted |
| Case total length | 50-2000 mm | 50-2000 mm |

The literature offers no numeric centerline-QC standard to borrow. CAT08 judges correctness by whether a point lies within the reference lumen radius, and reports overlap and overlap until first error ([Wolterink et al. 2019](https://arxiv.org/abs/1810.03143)). That needs a reference tree or a radius, and this export has neither. Published geometry studies exclude prior PCI or CABG, non-diagnostic image quality, segments under 1.5 mm diameter and "incorrect centerline" on visual review. Those exclusions can be large: van Zandwijk et al. kept only **64.3 % of arteries** after excluding any artery with one unassessable segment ([van Zandwijk et al. 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7165136/)). The tier thresholds above are therefore analysis choices fitted to this cohort. They should be fixed before outcomes are looked at, and reported as such.

Three findings shape what the geometry can mean. First, **no radius array exists**: `median_radius` has n = 0, and the only point arrays are `segment_label` and `branch` ([report_qc.md](../CGPS_data/report_qc.md)). The taper feature therefore needs a lumen radius measured on the CT, as `bifurcation/radius.py` does for ImageCAS-X ([radius.py](../bifurcation/radius.py)). Second, the mLAD length is almost constant (IQR **30.0-30.9 mm**), and the three RCA thirds are each about 38-40 mm ([report_qc.md](../CGPS_data/report_qc.md)). The proximal, mid and distal boundaries were set by a length rule, not by anatomy. That supports the existing vessel-level outcome and calls for position windows defined by arc-length fraction. Hampe et al. likewise refused to split trunks into p/m/d, because those landmarks "don't follow from tree topology" ([Hampe et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)). Third, LM is absent in **60 trees (8.1 %)**. True separate LAD and LCx ostia occur in only **0.16-0.77 %** of CT cohorts ([jcpres cohort](https://jcpres.com/article/2816); [Vojnosanit Pregl 2018](https://aseestant.ceon.rs/index.php/vsp/article/view/VSP160205201I)). Most missing LMs are therefore labelling or segmentation misses. That is why the acceptable tier tolerates them, while LM plaque status still comes from the reader column `ct_cag_lm_stenosis`.

| Artery | Strict, at most | Strict + acceptable, at most | Excluded, at least |
|---|---|---|---|
| LM (gate) | 682 | 684 | 60 |
| LAD | 576 | 678 | 66 |
| LCx | 581 | 599 | 145 |
| RCA | 553 | 567 | 177 |

These are upper bounds from the QC tables ([report_qc.md](../CGPS_data/report_qc.md)). LCx is likely to drop most below its bound. Its LCx label is short (5th percentile 9.7 mm), so the 40 mm strict minimum will bite. Unnamed code #22 also touches the LCx label in **216 trees**. If #22 is actually the distal circumflex, every one of those paths stops early.

## The visit question outranks every threshold

The selection only matters if the trees can serve as baseline predictors. The QC script's docstring calls the data the "baseline cohort", but the zip is named `10Y` ([centerline_qc.py](../CGPS_data/centerline_qc.py)), and CGPS follow-up has a median of about 10 years. If the trees come from the FU scan, the problems are not fixable by adjustment. Geometry measured after the plaque has formed is not a baseline predictor. Centerline failure could also be *caused* by the new plaque (calcium blooming, tracking stopping at a stenosis), which makes exclusion outcome-dependent. Under outcome-dependent missingness, complete-case analysis is biased ([van Buuren, FIMD §2.7](https://stefvanbuuren.name/fimd/sec-when.html)) and missing-indicator methods do harm ([Sisk et al.](https://arxiv.org/pdf/2206.12295)). If the trees are BL, failure happens before the outcome and can only relate to it through shared causes. Image quality falls with heart rate and BMI ([Dewey et al. 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC3294286)) and with CAC > 400 and female sex ([Chao et al. 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804794)). These are measured, so complete-case analysis is approximately valid for the conditional model.

The questions below are ordered by how much of the design each answer can overturn. The user should take questions 1-4 to the data manager and questions 5-11 to Kit, who made the trees. Kit's answers become constants in the script.

| # | Question | Who | Why it matters / what changes |
|---|---|---|---|
| 1 | **Are the 744 trees from the BL or the FU CCTA? What do "10Y" and "hø" mean?** Check by matching each tree's source-volume date to BL vs FU `scandate`, reported only as "matches BL / FU / neither". | data manager, Kit | FU trees invalidate the baseline-predictor design; BL extraction would then be mandatory. |
| 2 | Is the case ID (file stem) the `study_id`? IDs go above 2,116, the number of CGPS patients. | data manager | Without a key, no tree can be linked to reads or outcomes. |
| 3 | How were the 744 chosen (random, scan year, image-quality prescreen, or the Medis sub-study: `Readers_Plaque_analyses_finished` = 769, `Phd_Subjektiv_finished` = 753)? Were scans attempted and dropped? | data manager, Kit | Defines the first selection stage of the flow diagram, and whether the trees overlap the BL-read half (~1,020 patients). |
| 4 | Do all 744 have BL segment reads, or do some fall in the ~1,094 with empty BL reads? | data manager | Expected per-artery cohorts range from about 87 to 181 (LAD), 208 to 431 (LCx) and 186 to 385 (RCA), depending on the answer. |
| 5 | What are codes 18, 19, 20, 21, 22 and 28? Above all, is **22 the distal LCx** or OM2? | Kit | Sets `CODE_NAMES`; can move up to 216 LCx trunks between tiers. |
| 6 | Does code 13 "LCx" always cover the reader's `mcx` + `dcx`? Are the p/m/d boundaries rule-based? | Kit | Confirms the LCx trunk definition and the arc-length windows. |
| 7 | What does the `branch` point array hold? Does it identify ostium-to-tip paths? | Kit | Could replace the inferred ostium (`BRANCH_ARRAY`). |
| 8 | Can a radius or lumen contour be exported from Medis? What coordinate frame are the points in, and do they align with the CT affine? | Kit | Decides whether taper uses an exported radius (`REQUIRE_RADIUS`) or one sampled from the CT. |
| 9 | Why do per-file `segment_names` lists omit codes the file uses? Why is the numbering non-SCCT (14 = L-PLB, 15 = L-PDA)? Is 17 "AL" the same as "RI"? | Kit | Confirms `LABEL_NUMBERING = "raw"` is right. |
| 10 | Is a missing LM (60 trees) separate ostia or a miss? Why do about 163 trees have pRCA without mRCA, with pRCA up to 119 mm? What explains the 36.6 mm and 3,645.7 mm totals and the 971 mm "PDA"? | Kit | Sets LM handling and whether a whole-RCA-as-pRCA case should be relabelled rather than excluded. |
| 11 | Were the trees made on the same reconstruction and phase the readers used, with one correction protocol? | Kit | Decides whether tier can be cross-checked against reader evaluability. |
| 12 | Codebooks for `ct_cag_<seg>_eval`, `scan_qualitative_quality`, `ct_cag_incomplete`, `ct_cag_dominance` and BL `PM`. | data manager | Needed for the read-side filters and the dominance check. |

The cohort ranges in question 4 multiply the observed rates with the filters assumed independent. They are rough figures, not data ([linkage notes](../research_notes/Selecting%20usable%20centerline%20trees/linkage_and_selection_bias.md); [cgps_report_facts.md](../research_notes/Plaque%20risk%20model%20with%20CGPS%20data/cgps_report_facts.md)). LAD is the binding artery in every scenario: at the low end, only about 35-40 events support it.

## Running the selection script on the secure machine

The script imports `centerline_qc.py` for the zip reader, VTK parser, label naming and graph tolerances. Place it in the same folder as that file on the secure machine (both are in `CGPS_data/`). It needs only numpy and pandas; scipy is optional. Default input is `/data/kimbr/centerlines_hø_10Y.zip`, default output `~/centerline_selection` ([centerline_selection.py](../CGPS_data/centerline_selection.py)).

```bash
# 1. quick trial on the first 20 cases (checks that the real binary VTK files parse)
python CGPS_data/centerline_selection.py --limit 20 --out ~/centerline_selection_trial

# 2. full run with the defaults (ZIP_PATH and OUT_DIR at the top of the script)
python CGPS_data/centerline_selection.py

# 3. explicit source and output, e.g. after Kit re-exports
python CGPS_data/centerline_selection.py --src /data/kimbr/centerlines_hø_10Y.zip --out ~/centerline_selection
```

The run writes two files with opposite privacy status. **`~/centerline_selection/secure_only/centerline_tiers.csv`** has one row per case and artery (LM, LAD, LCx, RCA). It holds the tier, `why_not_strict`, `why_excluded` and every path metric: segment lengths on the path, `trunk_mm`, `lm_mm`, foreign and unlabelled length and runs, `monotone`, `max_step_mm`, fragments, cycles, left/right mixing, radius presence and `branch` IDs on the path. It contains case IDs and **must never leave the secure machine**. **`~/centerline_selection/selection_report.md`** is aggregate only. It contains the settings, a tier table per artery, reason counts, usable-artery patterns per case, LAD and LCx tier by LM tier, on-path length summaries by artery and tier, and the radius, duplicate and `branch` checks. It lists no case IDs, and read errors are counted, not listed. Counts from 1 to 4 print as "<5", a row never keeps a single hidden cell, means need 5 values and quartiles 10, and min/max are never shown. These rules are copied from `cgps_stats.py` (`MIN_CELL = 5`, `QUARTILE_MIN = 10`, `GROUP_MIN = 20`) ([cgps_stats.py](../CGPS_data/cgps_stats.py)). Even so, it should be checked against the data agreement before it leaves the secure environment, because counts can be combined with other tables.

The research step generated legacy VTK 4.2 and 5.1 test zips of 6 and 60 cases that mimic Kit's files. The script produced the expected tiers on them: a full tree was strict everywhere, a tree with no LM, dLAD or dRCA was acceptable for LAD, LCx and RCA with LM excluded, an out-of-order LAD was excluded, and a pRCA-only tree was excluded. A search for case-ID strings in the generated report found none ([audit notes](../research_notes/Selecting%20usable%20centerline%20trees/qc_report_audit_and_script.md)). Two parts are untested on real data. The binary 5.1 parsing is inherited unchanged from the QC script, which read all 744 files without error. The ostium inference has never been checked against a ground-truth start point. That is why the 20-case trial comes first.

All constants sit at the top of the script. The table below pairs each one with the question that settles it.

| Constant (default) | Adjust when |
|---|---|
| `ZIP_PATH`, `OUT_DIR` | A new export arrives (question 1: BL trees extracted). |
| `CODE_NAMES = {}` | Kit names the unnamed codes; `{22: "dCX"}` makes 22 part of the LCx trunk (question 5). |
| `LABEL_NUMBERING = "raw"` | Only if Kit confirms a true SCCT scheme (question 9); "raw" is correct for the current files. |
| `RANK`, `REQUIRED` | Code 13 turns out not to be the whole LCx, or Kit splits mCX/dCX (question 6). For **left-dominant** RCAs, consider dropping dRCA from `REQUIRED["strict"]["RCA"]` once `ct_cag_dominance` is decoded (question 12). |
| `BRANCH_ARRAY = "branch"` | Kit says `branch` marks ostium-to-tip paths; the ostium rule could then use it (question 7). |
| `REQUIRE_RADIUS = False`, `RADIUS_RANGE (0.3, 4.0)`, `RADIUS_VALID_FRAC 0.9` | A Medis radius export exists (question 8). Otherwise leave as is and measure radius on the CT. |
| `MIN_LM_MM {2, 0.5}`, `MAX_LM_MM 35` | Kit explains the missing and long LMs (question 10). |
| `MIN_TRUNK_MM` (70/40/70 strict; 40/30/40 acceptable) | After the first aggregate run, if LCx strict collapses because of #22. Fix it before linking outcomes. |
| `MIN_SEG_MM`, `FOREIGN_MM`, `UNLAB_RUN_MM`, `UNLAB_PCT`, `MAX_STEP_MM 1.5`, `FRAGMENT_MM 5` | Only for documented reasons, and only before outcomes are seen. |
| `CASE_MIN_TOTAL_MM 50`, `CASE_MAX_TOTAL_MM 2000` | Kit explains the length outliers (question 10). |
| `MIN_CELL 5`, `QUARTILE_MIN 10`, `GROUP_MIN 20` | Only if the data agreement demands stricter disclosure control; never loosen. |

The script stops at centerline tiers. The next step is still to be written, and it also runs only on the secure machine. Once question 2 confirms the key, join `centerline_tiers.csv` to the BL and FU tables by `study_id` inside `cgps_stats.py`'s `artery_design`. Then report, per artery, aggregate cross-tabs of tier against BL trunk `_stenosis` evaluability and `_eval`, `ct_cag_{lad,cx,rca}_uneval`, `ct_cag_dominance` against the PDA/PLB codes present, `ct_cag_lm_stenosis` against a missing LM, and vessel CACS in "plaque-free" trunks. The eligible set for artery *a* is then the intersection of: tree from the BL scan, artery tier usable, BL trunk read and evaluable (plus LM for LAD and LCx), trunk plaque-free with no stent, CABG or revascularisation, and FU outcome known.

## Exclusion is testable because the outcome comes from the reads

The design has one strength against selection bias. The outcome is read by a reader, independent of the centerline, so the new-plaque rate among eligible arteries *excluded* for centerline reasons can be observed. Per artery, compare included and excluded arteries on age, sex, BMI, heart rate, log CAC and scan year, using standardised mean differences. Then fit a logistic selection model and report its c-statistic. Finally, test whether exclusion is associated with the outcome after adjustment. A clearly non-null association contradicts the outcome-independent assumption that justifies complete-case analysis. The primary analysis should then be complete-case on the strict tier, with sensitivity analyses on the acceptable tier and with stabilised, truncated inverse-probability weights. Metten et al. found IPW no less biased than complete-case analysis and less efficient, and recommend a narrow selection model ([Metten et al. 2022](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8848672/)). Each artery needs its own flow diagram (2,116 → 744 trees → BL match → BL reads → tier → evaluable → plaque-free → FU known → events), with small-cell suppression, as TRIPOD+AI items 20a and 21 require ([TRIPOD+AI](https://pmc.ncbi.nlm.nih.gov/articles/PMC11019967/)).

## The laptop copy of report_qc.md holds case IDs

`CGPS_data/report_qc.md` lists **up to 40 case IDs per red flag** ([report_qc.md](../CGPS_data/report_qc.md)). The QC script's own docstring says the report and CSVs "contain case IDs ... keep them on the DTU machine" ([centerline_qc.py](../CGPS_data/centerline_qc.py)). The laptop copy is untracked but not git-ignored (`git check-ignore` returns nothing), so a routine `git add .` would commit it. If those IDs are `study_id`s, the copy breaks the user's rule that only aggregates leave the secure environment. The user should delete the laptop copy, or replace it with a version regenerated on the secure machine without the ID lists. They should add `CGPS_data/report_qc.md` (and `**/secure_only/`) to `.gitignore`, and check with the data agreement whether a report is needed. Two research notes behind this report also quote a few of those IDs (`qc_report_audit_and_script.md` in its privacy finding, `linkage_and_selection_bias.md` in its Q1 linkage finding). They should be redacted the same way. This report quotes none.

## Conclusion

The data side is cleaner than the 45 flag-free trees suggest. Connectivity is intact, LM to pLAD and LM to pCx joins are 100 % direct, and no left/right contact occurs, so the losses will come from short or mislabelled distal trunks, above all the LCx. The open questions are mostly about meaning, not geometry. One unnamed code (#22) can decide a quarter of the LCx cohort. The missing radius forces taper onto the CT. And a single date comparison decides whether the 744 trees belong in a baseline-prediction thesis at all. Running the selection script before Kit answers is still worthwhile, because its aggregate report shows how much each answer is worth. The tiers should then be frozen before any outcome is linked, so the per-artery selection stays a pre-specified design choice rather than a tuned one.
