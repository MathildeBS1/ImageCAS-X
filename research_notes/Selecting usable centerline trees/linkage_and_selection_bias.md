# Linking centerline-tree selection to the CGPS CCTA reads, and handling the selection statistically

Scope: how the 744 centerline trees (`centerlines_hø_10Y.zip`, QC in `CGPS_data/report_qc.md`) should be combined with the clinical reads in `header_BL.xlsx` / `header_FU.xlsx`, so that the per-artery (LAD, CX, RCA; never pooled) cohorts of plaque-free trunks are valid for prediction of new trunk plaque at FU.

Local sources used (read in full or the relevant sections):
- [report_qc.md](../../CGPS_data/report_qc.md) (QC of the 744 trees)
- [header_BL.xlsx](../../CGPS_data/header_BL.xlsx) (213 cols), [header_FU.xlsx](../../CGPS_data/header_FU.xlsx) (277 cols), read with openpyxl
- [cgps_stats.py](../../CGPS_data/cgps_stats.py) (constants l. 40-105, `decode_segments` l. 284, `artery_design` l. 811-899)
- [report.md](../../CGPS_data/report.md) (aggregate report of 2026-10-10, which predates `artery_design`)
- [cgps_report_facts.md](../Plaque%20risk%20model%20with%20CGPS%20data/cgps_report_facts.md) (earlier research notes on the report)

---

## Q1. Which header columns enable linkage, selection and consistency checks, and what are their exact names?

### Takeaway
Linkage is only possible through `study_id`. `scandate` and `scan_age` are the only fields that can tell whether a centerline belongs to the BL or the FU scan. Per-segment evaluability (`ct_cag_<seg>_eval`) and every image-quality field except vessel-level unevaluable counts are **BL only**. Unevaluable *reasons* are **FU only**. Dominance, stent, CABG, per-segment stenosis and plaque type, and per-vessel CACS are in both files. In the BL file, `bad_quality` is useless (all False), and `_eval`, `scan_qualitative_quality`, `ct_cag_incomplete` and `PM` use undocumented codes.

### Cited Findings
**Linkage / visit identification**
- `study_id` (both). This is the only key, and it is how patients link to the CT volumes. — [CGPS_data/CLAUDE.md](../../CGPS_data/CLAUDE.md); [header_BL.xlsx](../../CGPS_data/header_BL.xlsx), [header_FU.xlsx](../../CGPS_data/header_FU.xlsx)
- `scandate`, `scan_age` (both). Comparing them with the acquisition date or age in the CT volume's DICOM or NIfTI metadata is the only header-based way to decide whether a centerline is from the BL or the FU scan. — headers
- The QC report lists case IDs up to at least 2,829 (e.g. `no_CX` list: … 2773, 2829). There are only 2,116 CGPS patients, so the case IDs in the zip are not 1…2,116 and may be `study_id` or some other key. — [report_qc.md "Red flags"](../../CGPS_data/report_qc.md)

**Per-segment reads (segments `prca mrca drca pda pla lm plad mlad dlad d1 d2 im pcx om1 mcx om2 dcx`)**
- `ct_cag_<seg>_stenosis` (both). Stored as text labels (`none/minimal/mild/moderate/severe/occlusion`, `uneval_*` = not evaluable) and decoded in `decode_segments`. — [cgps_stats.py l. 52-53, 284-312](../../CGPS_data/cgps_stats.py)
- `ct_cag_<seg>_plaque_type` (both); `_feat_spotcalc`, `_feat_napring` (both); `_feat_lap`, `_feat_posrem` (**FU only**). — headers
- `ct_cag_<seg>_eval` (**BL only**, 17 columns). FU has no per-segment eval column. At FU, evaluability is only available through `uneval_*` values in `_stenosis`. — headers
- The `_eval` codes are undocumented (e.g. plad 0: 1,953, 12: 81, 13: 73) and do not separate unread patients. — [cgps_report_facts.md §5](../Plaque%20risk%20model%20with%20CGPS%20data/cgps_report_facts.md)
- BL `_stenosis` is empty for 1,094 patients in every trunk segment, i.e. the "unread half". — [report.md, decoded text labels (BL)](../../CGPS_data/report.md)
- `ct_cag_<seg>_medis_egnet`, `ct_cag_<seg>_medis_finished` (**BL only**; Medis plaque-analysis status). Also **BL only**: `Readers_Plaque_analyses_finished` (1 for 769, missing 1,347) and `Phd_Subjektiv_finished` (1 for 753, missing 1,363). — headers; [report.md l. 5882-5894](../../CGPS_data/report.md)

**Vessel/patient-level evaluability and quality**
- Both files: `ct_cag_uneval`, `ct_cag_incomplete`, `ct_cag_lad_uneval`, `ct_cag_cx_uneval`, `ct_cag_rca_uneval`. — headers
- BL `ct_cag_cx_uneval` = 1 in 1,441 patients, which is probably the IM being counted in CX (IM stenosis is `uneval` in 1,482). The CX vessel count is therefore not usable as-is. — [cgps_report_facts.md §5](../Plaque%20risk%20model%20with%20CGPS%20data/cgps_report_facts.md)
- **BL only**: `scan_qualitative_quality` (0: 1,539, 1: 331, missing 246; coding undocumented), `Image_Quality_reason_1`, `Image_Quality_reason_2` (free text; the script lists them in `FREE_TEXT` and never outputs them), `bad_quality` (False in all 2,116, so uninformative), `ct_cag_eval_n` (median 16, p5 14), `PM` (0: 1,149, missing 967; meaning not documented, possibly pacemaker). — headers; [cgps_stats.py l. 62, 92-93](../../CGPS_data/cgps_stats.py); [cgps_report_facts.md §5](../Plaque%20risk%20model%20with%20CGPS%20data/cgps_report_facts.md); [report.md l. 5875-5880](../../CGPS_data/report.md)
- **FU only**: patient-level reasons `ct_cag_uneval_motion`, `ct_cag_uneval_noise`, `ct_cag_uneval_scanfield`, `ct_cag_uneval_contrastdefect`, `ct_cag_uneval_pm`, `ct_cag_uneval_other`. Per vessel: `ct_cag_{lad,cx,rca}_uneval_contrast`, `_uneval_scanfield`, `_uneval_pm`, `_uneval_noise`. Note there is **no per-vessel motion reason**, although motion is the dominant FU reason. — headers; [cgps_report_facts.md §5](../Plaque%20risk%20model%20with%20CGPS%20data/cgps_report_facts.md)
- FU unevaluability is highest in the RCA: mid-RCA `uneval` 197; vessel-level uneval ≥ 1 segment: LAD 61, CX 63, RCA 225. — [cgps_report_facts.md §5](../Plaque%20risk%20model%20with%20CGPS%20data/cgps_report_facts.md)
- **FU only** scan/technical fields (none exist at BL): `scandata_kv`, `scandata_ma`, `scandata_contrast_volume`, `scandata_nitro`, `scandata_dlp_heart_angio`, `scandata_dlp_heart_calciumscore`, `ct_angio_heart_done`, `ct_noncontrast_heart_done`, `preparation_betablocker`, `preparation_systolic_bp`, `preparation_diastolic_bp`. — header_FU
- Both files: `preparation_heartrate`, `hr_during_scan`, `clin_bmi`, `clin_weight`, `clin_height`, `clin_bsa`. These are the patient factors that drive image quality (see Q4). — headers

**Anatomy / devices**
- `ct_cag_dominance` (both; codes undocumented). — headers
- `ct_cag_stent`, `ct_cag_cabg` (both); `demo_hist_coronary_revasc`, `demo_hist_myocardial_infarction` (both); `demo_hist_cag`, `demo_hist_icd_pm` (**FU only**). Incident stent < 5 and incident CABG 0 over follow-up. — headers; [report.md l. 81-82, 5065-5100](../../CGPS_data/report.md)

**Calcium**
- `ct_cacs_lm`, `ct_cacs_lad`, `ct_cacs_cx`, `ct_cacs_rca`, `ct_cacs_sum`, `ct_cacs_groups` (both); `ct_cacs_other`, `ct_cacs_{lm,lad,cx,rca}_eval`, `ct_cacs_eval_all` (**FU only**; eval_all 1 in 2,110, 0 in 6). — headers; [cgps_report_facts.md §5](../Plaque%20risk%20model%20with%20CGPS%20data/cgps_report_facts.md)

**Not available in either header** (do not plan on them): scanner model or vendor, BL kV/mA/contrast/nitro, gating mode, reconstruction kernel, slice thickness, cardiac phase, per-segment image-quality grades, reader identity or inter-reader agreement, heart rhythm at BL (`demo_hist_afib` is FU only), and a documented dominance code. — headers (absence checked against full column lists)

**Label correspondence between centerline codes and read columns**
- Centerline codes (as used in QC): 1 pRCA, 2 mRCA, 3 dRCA, 4 R-PDA, 5 LM, 6 pLAD, 7 mLAD, 8 dLAD, 9 D1, 10 D2, 11 pCx, 12 OM1, 13 LCx, 14 L-PLB, 15 L-PDA, 16 R-PLB, 17 RI (also "AL" in 4 files), 24 unlabelled. Codes 18, 19, 20, 21, 22 and 28 are unnamed in every file and occur in 375, 161, 55, 210, 238 and 184 cases. — [report_qc.md "Label codes"](../../CGPS_data/report_qc.md)
- The reads have `mcx`, `dcx` and `om2`, but the centerlines have a single code 13 "LCx" and no named OM2. The reads have a single `pda` and `pla` column, while the centerlines separate R-PDA/L-PDA and R-PLB/L-PLB. — headers vs [report_qc.md](../../CGPS_data/report_qc.md)
- The ImageCAS-X annotation protocol (same group, Bransby et al.) deliberately does **not** split LAD/LCx/RCA into proximal/mid/distal, "because they depend on side branch positions which are highly variable". It also adds an "Other" category for D3/OM3-type branches. — [Bransby et al., ImageCAS-X, arXiv 2608.30404](https://arxiv.org/pdf/2608.30404)
- mLAD length in the 744 trees is almost constant (q1 30.0, median 30.5, q3 30.9 mm). — [report_qc.md "Segments"](../../CGPS_data/report_qc.md)

### Inferences
- The almost-constant mLAD length suggests the pLAD/mLAD/dLAD (and probably pRCA/mRCA/dRCA) boundaries in the centerline files come from a length or algorithm rule, not the reader's landmark-based boundaries. This supports the existing decision to define eligibility and outcome at trunk level ([thesis design memory](../../CGPS_data/cgps_stats.py), `TRUNKS`) and not to match segments one-to-one.
- The CX trunk is defined in reads as `pcx+mcx+dcx`, but in centerlines as pCx (11) + LCx (13). Position windows for CX must therefore be defined geometrically (e.g. arc-length thirds), not by read boundaries.
- Codes 18-22 and 28 have to be resolved with the annotator (Kit) before a trunk is declared "complete". Several of them touch mLAD/dLAD/CX/pCX (e.g. #22-CX 216 cases, #18-mLAD 193, #28-pCX 151; [report_qc.md](../../CGPS_data/report_qc.md)), so they are probably side branches (D3, OM2/OM3, septals?). If any of them is a trunk continuation (e.g. a distal CX code), trunk completeness changes.

### Gaps
- No codebook was found for `_eval`, `scan_qualitative_quality`, `ct_cag_incomplete` (codes 0/15/16/17), `ct_cag_dominance` or `PM`. The data manager must supply it.
- I could not verify the official SCCT 2014 18-segment numbering online (the guideline table was not retrievable). It is unconfirmed whether the centerline numbering (14 = L-PLB, 15 = L-PDA, 17 = RI) follows SCCT or a local scheme.

---

## Q2. Consistency checks between centerline trees and reads

### Takeaway
Run a set of aggregate cross-tabulations of centerline-derived flags × read fields on the secure machine. Covering dominance, segment presence vs evaluability, devices, calcium in "plaque-free" trunks and the visit date shows (a) whether the trees and reads describe the same scan and anatomy, and (b) whether centerline failure is concentrated in difficult (and higher-risk) anatomy.

### Cited Findings
- Dominance definitions used by the annotating group: right = PDA and PLA from the RCA; left = PDA from the LCx; co-dominant = PDA/PLA from both, or R-PDA without R-PLA. Their prevalence among 800 scans was 91.1% right, 5.1% left, 3.8% co-dominant. — [Bransby et al., ImageCAS-X](https://arxiv.org/pdf/2608.30404)
- A 6,382-patient CCTA cohort found 91% right and 9% left dominance. — [search summary of dominance/prognosis cohort (Mount Sinai scholars record)](https://scholars.mssm.edu/en/publications/coronary-dominance-and-prognosis-in-patients-undergoing-coronary--2/) (secondary snippet; full text not checked)
- In the 744 trees: L-PDA (15) is present in 32 cases (4.3%), L-PLB (14) in 102 (13.7%), R-PDA (4) in 428 (57.5%), R-PLB (16) in 511 (68.7%), dRCA in 556 (74.7%) and RCA in 735 (98.8%). — [report_qc.md "Label codes", "Segments"](../../CGPS_data/report_qc.md)
- No LM in 60 cases, no LAD in 42, no CX in 37; complete trunks: LM+LAD 576, LM+CX 581, RCA 553 (567 without dRCA), all three 366. — [report_qc.md](../../CGPS_data/report_qc.md)
- The script treats a trunk as evaluable only if all three trunk segments have a decoded stenosis at BL (`sb.notna().all`), with `uneval_*` decoded to NaN. The outcome is unknown if no plaque is seen at FU and any trunk segment is unevaluable. — [cgps_stats.py l. 811-850](../../CGPS_data/cgps_stats.py)
- The script already includes a check for "eligible but vessel calcium > 0 at BL (plaque missed?)". — [cgps_stats.py `artery_design`, calcium block](../../CGPS_data/cgps_stats.py)

### Inferences (proposed checks; all as aggregate counts with `MIN_CELL = 5` suppression via the script's `count`/`count_of`/`crosstab`)
1. **Visit match (do this first).** Compare the scan date (or age) from the centerline's source volume with BL and FU `scandate`/`scan_age`. Report only "matches BL / matches FU / neither", without dates.
2. **Dominance vs labels.** Cross-tab `ct_cag_dominance` (the visit that matches the trees) × {L-PDA present, L-PLB present, R-PDA present, R-PLB present, dRCA present}. Expected: right-dominant → R-PDA and no L-PDA; left-dominant → L-PDA and short or absent dRCA/R-PDA. The tree-level L-PDA share (4.3%) is in the expected range (5-9%). The L-PLB share (13.7%) is higher than left plus co-dominance (≈9%), which points to labelling or co-dominance differences. R-PDA at only 57.5% suggests many right-dominant trees are truncated distally. Use dominance to decide whether dRCA is required for "RCA complete" (tier 553 vs 567).
3. **Reader-evaluable but no centerline label (per trunk segment).** For each trunk segment, cross-tab BL `ct_cag_<seg>_stenosis` evaluable (decoded, non-NaN) and `_eval` × centerline segment present and connected. Report four cells per segment:
   - evaluable ∩ missing centerline = pipeline failure. This is the cell to test for informativeness in Q4.
   - unevaluable ∩ centerline present = geometry from a segment the reader could not assess. Exclude it, or keep it only in the lenient tier.
4. **LM.** `ct_cag_lm_stenosis` read vs LM centerline absent (60 cases). A real separate-ostia anatomy has no LM in the read either. A read LM with no LM label means centerline failure. LAD/CX trunk geometry then has no defined origin, so those cases are excluded from the LAD/CX models.
5. **Devices / revascularisation.** BL `ct_cag_stent`, `ct_cag_cabg`, `demo_hist_coronary_revasc`, `demo_hist_myocardial_infarction`: exclude the patient (not primary prevention, and stent or graft geometry is not native). Most of these patients would fail "plaque-free" anyway, but a stent in another vessel or CABG would not be caught by the trunk rule. Also check whether `PM` (BL) or `demo_hist_icd_pm` (FU) is associated with RCA centerline failure (lead artefacts in the RCA region). This is my hypothesis, not a sourced fact.
6. **Calcium in "plaque-free" trunks.** Eligible artery × vessel CACS (`ct_cacs_lad`, `ct_cacs_cx`, `ct_cacs_rca`, and `ct_cacs_lm` for LAD/CX) > 0. This is already in `artery_design`. Report it separately for centerline-included and centerline-excluded arteries.
7. **Unread half.** Cross-tab "BL reads present" (any `ct_cag_<trunk seg>_stenosis` non-empty) × "in the 744". Also cross-tab with `Readers_Plaque_analyses_finished` and `Phd_Subjektiv_finished`. Their counts (769 and 753) are close to 744, which suggests the trees may come from one of these sub-studies (see Q5).
8. **Plausibility.** Total length or extent outliers (`total_length_odd` 2 cases, max total 3,645 mm, n_polylines up to 165) vs `clin_height`/`clin_bsa`. These are units or duplication errors, not anatomy, so exclude them.

### Gaps
- No published study was found that validates centerline-label presence against reader segment evaluability. These checks are design proposals, not established methods.

---

## Q3. Per-artery eligibility as an intersection, and expected cohort/event shrinkage

### Takeaway
For artery *a* ∈ {LAD, CX, RCA}, eligibility = **V** (centerline from the BL scan) ∩ **C_a** (centerline trunk usable) ∩ **R_a** (BL trunk read and evaluable, plus LM for LAD/CX) ∩ **P_a** (trunk plaque-free, plus LM plaque-free for LAD/CX, no stent/CABG/revasc) ∩ **O_a** (FU outcome known). The 744 trees are at most about 35% of the 2,116 patients, and only the read half can satisfy R_a. Expected per-artery cohorts therefore run from about 80 (LAD, if the 744 are a random draw) to about 430 (CX, if the 744 all have reads), with roughly 35-160 events. LAD is the binding artery.

### Cited Findings
- Trunk-complete trees: LAD 576/744 (77.4%), CX 581 (78.1%), RCA 553 (74.3%) or 567 (76.2%) without dRCA. The completeness rule requires all segments present and connected; PDA/PLB are excluded. — [report_qc.md "Complete main trunks"](../../CGPS_data/report_qc.md)
- Only 45/744 trees have no red flag. `unknown_labels` 546, `>2_components` 396, `unlabelled>20%` 287. — [report_qc.md "Red flags"](../../CGPS_data/report_qc.md)
- BL reads exist for about 1,020-1,022 of 2,116 patients (≈48%). — [cgps_report_facts.md](../Plaque%20risk%20model%20with%20CGPS%20data/cgps_report_facts.md); [CGPS data caveats memory, from report.md](../../CGPS_data/report.md)
- Vessel-level proxies among read patients (vessel units include side branches, so trunk-only eligibility is likely higher): LAD 139 events/321 eligible (43.3%), CX 277/757 (36.6%), RCA 281/711 (39.5%). The LM rule will shrink LAD/CX further (LM plaque in about 21% of read patients). — [cgps_report_facts.md §1](../Plaque%20risk%20model%20with%20CGPS%20data/cgps_report_facts.md)
- Riley et al. criteria for a binary-outcome model: expected shrinkage ≥ 0.9 (≤ 10% overfitting), apparent-vs-adjusted Nagelkerke R² difference ≤ 0.05, and outcome risk estimated within ±0.05. Implemented in `pmsampsize`. — [Riley et al. BMJ 2020;368:m441 / pmsampsize manual](https://cran.r-universe.dev/pmsampsize/doc/manual.pdf)
- BL trunk-segment unevaluable among read patients: plad < 5, mlad 11, dlad 5; pcx 10, mcx 17, dcx 67; prca 46, mrca 92, drca 59; LM 10. At FU: plad 26, mlad 27, dlad 36; pcx 31, mcx 45, dcx 39; prca 81, mrca 197, drca 81. — [cgps_report_facts.md §5](../Plaque%20risk%20model%20with%20CGPS%20data/cgps_report_facts.md)

### Inferences
**Operational definitions (two tiers, fixed before looking at outcomes):**
- *C_a strict*: all trunk segments present and connected (as in `complete_LAD/CX/RCA.txt`); LM present for LAD/CX; dRCA required unless the read dominance is left; no unresolved unknown code inside the trunk path; trunk not split across components; no `disconnected_segment` or `segment<2mm` on the trunk; total length plausible.
- *C_a lenient*: trunk present to at least a fixed arc length (e.g. through the mid third), with unknown side-branch codes allowed and fragments elsewhere ignored ("pieces < 10 mm ignored" column in the QC report).
- *R_a*: patient in the BL-read half; every trunk segment (and `lm` for LAD/CX) has a decoded stenosis (not `uneval_*`) and an evaluable `_eval` code, once decoded.
- *P_a*: as in `artery_design`; additionally BL `ct_cag_stent`, `ct_cag_cabg`, `demo_hist_coronary_revasc` = 0. Optional sensitivity: vessel CACS = 0 as well (the "combined definition" already in the script).
- *O_a*: as in `artery_design` (FU plaque seen, or all trunk segments evaluable at FU).

**Rough shrinkage arithmetic (my calculation; assumes independence between the filters, which is unlikely):**
| scenario | LAD eligible (events at 43%) | CX (37%) | RCA (40%) |
|---|---|---|---|
| 744 random from 2,116 (≈48% read) | 744×0.48×0.774×0.315 ≈ 87 (≈38) | 744×0.48×0.781×0.742 ≈ 208 (≈76) | 744×0.48×0.743×0.697 ≈ 186 (≈73) |
| 744 all from the read half | ≈ 181 (≈78) | ≈ 431 (≈158) | ≈ 385 (≈152) |

These figures are before the LM rule for CX, the strict-tier extras and FU outcome loss (≈ 2-3% LAD/CX, up to ≈ 10% RCA). With a minority class of about 35-80 for LAD, a Riley-type budget of about 4-10 parameters leaves room for a SCORE2 linear predictor, log(1+CAC), FU time and only 1-3 geometry terms. The per-artery model must be planned for the LAD lower bound.
- If the trees are FU scans (see Q5), V fails for all 744 and none of this applies to the "baseline geometry" design.

### Gaps
- Exact per-artery eligible n and events for the trunk design are not in `report.md`. `artery_design` must be re-run, and extended with the centerline filter, in the secure environment.
- The correlation between centerline completeness and read/plaque status is unknown. The table above treats them as independent.

---

## Q4. Selection bias: is excluding poor centerlines informative, how to check it, and how to analyse it

### Takeaway
Centerline failure plausibly follows image quality, which depends on heart rate, BMI, calcium and sex. Calcium and age are also plaque-risk factors, so exclusion is likely *covariate-dependent*. Complete-case analysis then stays approximately valid for the conditional prediction model, as long as those covariates are in the model and failure does not depend on the outcome itself. Conditions where it would not stay valid: centerlines from FU scans, or failure caused by plaque. The outcome is read independently of the centerline, so the event rate among excluded-but-eligible arteries is observable. That gives a direct, aggregate-only test. Primary analysis: complete case (strict tier). Sensitivity analyses: lenient tier, IPW for selection, and possibly MI. Report one flow diagram per artery (TRIPOD+AI 20a/20b/21, STROBE 13).

### Cited Findings
**Image quality depends on patient factors that overlap with plaque risk**
- CORE-64 (291 patients, 64-slice): poorer patient-level image quality was associated with higher BMI (OR 0.89, p < 0.001), higher heart rate (OR 0.90, p < 0.001) and breathing artefact (OR 4.97). Calcium score (p = 0.77), age (p = 0.10) and sex were not associated with image quality, but calcium and age reduced diagnostic accuracy at vessel level. — [Dewey, Vavere et al., AJR 2010;194:93-102](https://pmc.ncbi.nlm.nih.gov/articles/PMC3294286)
- 256-slice study (451 patients): worse quality with heart rate (β 0.0035/bpm, p < 0.001), CAC > 400 (β 0.21, the strongest predictor), CAC 100-400 (β 0.043), and female sex (male β −0.045). Age was significant only univariably; BMI was not significant. Nondiagnostic segments were 0.3%, 12 of the 21 from heavy calcification and 9 from motion. — [Chao et al., Acta Cardiol Sin 2013;29:444-450](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804794)
- A large scoring-system cohort lists BMI categories, heart rate and calcium categories as predictors of uninterpretable segments. Findings on BMI conflict across studies. — [search summary: Circulation scoring-system report](https://cardiovascularbusiness.com/topics/cardiac-imaging/circ-scoring-system-predicts-ccta-image-quality) (secondary; not read in full)
- The annotating group excluded 200 of 1,000 ImageCAS scans as non-diagnostic (motion 114, step artefacts 76, contrast 7, …) before centerline labelling. — [Bransby et al., ImageCAS-X](https://arxiv.org/pdf/2608.30404)
- In CGPS, BL `bad_quality` is all False, and `scan_qualitative_quality` is 1 for 331 and missing for 246. FU unevaluability is mostly motion and concentrated in the RCA. — [cgps_report_facts.md §5](../Plaque%20risk%20model%20with%20CGPS%20data/cgps_report_facts.md)

**Missing-data theory relevant to complete-case vs imputation**
- If missingness does not depend on the outcome (given the covariates), complete-case regression coefficients are unbiased, whether the missing data are in predictors or outcome. MI has an advantage mainly when auxiliary predictors of the outcome exist outside the analysis model. — [van Buuren, FIMD §2.7](https://stefvanbuuren.name/fimd/sec-when.html)
- Complete-case analysis can be unbiased under "outcome-independent MNAR", while MI is generally biased there, and the assumption can be checked with data. — [Sjölander seminar abstract, Uppsala 2025](https://www.uu.se/en/department/statistics/events/archive/2025-03-19-seminar-2025-03-19-arvid-sjolander) (abstract only)
- For prediction, how missing data are handled should match the deployment policy. If complete data are required at deployment, use MI at development including the outcome. Missing-indicator methods can harm when missingness depends on the outcome. — [Sisk et al. simulation, arXiv 2206.12295](https://arxiv.org/pdf/2206.12295); [compatibility study, arXiv 2504.06799](https://arxiv.org/abs/2504.06799v2); title-level source: Sperrin et al., "Missing data should be handled differently for prediction than for description or causal explanation", J Clin Epidemiol 2020 (doi 10.1016/j.jclinepi.2020.03.028; full text not read)
- IPW removes complete-case bias when the selection model is correct; MI is usually more efficient; weight stabilisation and truncation are standard. — [Seaman & White, Stat Methods Med Res 2013 (review)](https://www.citedrive.com/en/discovery/review-of-inverse-probability-weighting-for-dealing-with-missing-data/)
- In a simulation of cohort attrition, IPW gave about the same bias as complete-case analysis and was less efficient in every scenario. The authors recommend a narrow response model. — [Metten et al., BMC Med Res Methodol 2022](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8848672/)

**Reporting**
- TRIPOD+AI (Collins et al., BMJ 2024;385:e078378): item 6b eligibility; 7 data pre-processing and quality checking (and whether these were similar across sociodemographic groups); 11 how missing data were handled, with reasons for omitting data; 5a data sources and representativeness; 20a flow of participants with and without the outcome (a diagram may help); 20b characteristics and amount of missing data; 21 number of participants and events in each analysis; 14 fairness; 23a subgroup performance. — [TRIPOD+AI, PMC11019967](https://pmc.ncbi.nlm.nih.gov/articles/PMC11019967/)
- STROBE item 13: (a) numbers at each stage (potentially eligible, examined, confirmed eligible, included, followed up, analysed), (b) reasons for non-participation at each stage, (c) consider a flow diagram. The E&E notes that losses unrelated to health mainly cost precision, while health-related losses bias. — [STROBE educational expansion, item 13](https://bookdown.org/melissaksharp/STROBE_eduexpansion/results-participants-13.html) (secondary; original Vandenbroucke 2007 E&E not read)

### Inferences
**Why exclusion is probably informative, and in which direction**
- Centerline failure (missing segments, fragments, unlabelled share) is plausibly driven by motion (heart rate), noise (BMI) and blooming or step artefacts. The cited studies link these to image quality. Calcium and age are plaque-risk predictors, so the included set will likely be lower-risk, and arteries with "hidden" plaque (CACS > 0 but read as none) may be under-represented. The direction is not certain: BMI was null in one study and calcium null in another.
- The plaque-free restriction (P_a) already removes most high-calcium arteries, which shrinks the room for calcium-driven selection within the eligible set.
- **Decisive point: the timing of the scan.** If the trees are from BL scans, failure happens before the outcome. It can only relate to the outcome through shared causes (calcium, age, HR, BMI), which are measured and can be adjusted for, so complete-case analysis is approximately valid for the conditional model ("outcome-independent" missingness). If the trees are from FU scans, failure can be caused by the new plaque itself (calcified plaque blooming, stenosis-induced tracking stops), so selection depends on the outcome and complete-case analysis is biased. Geometry measured after plaque has formed is also not a baseline predictor (reverse causation).

**Checks (aggregate only, `MIN_CELL = 5`, no row-level output, no free-text values)**
1. Per artery, among arteries meeting R_a ∩ P_a: compare centerline-included vs excluded on `scan_age`, `male`, `clin_bmi`, `hr_during_scan`, `preparation_heartrate`, `clin_bp_sys_mean`, `tot_cholesterol`, `hdl`, `hist_smoking_current`, `hist_diabetes`, `med_lipid_lowering_any`, log(1+`ct_cacs_sum`), vessel CACS, "plaque elsewhere", `scan_qualitative_quality`, `ct_cag_eval_n`, `ct_cag_dominance`, BL scan year (from `scandate`, reported as year bands), `rand_group` (FU). Use standardised mean differences (the script has `smd`) and counts with suppression.
2. **Outcome-dependence test.** Event rate of new trunk plaque in included vs excluded arteries, plus the odds ratio of exclusion on the outcome adjusted for the covariates above. This works because outcomes come from the reads, not the centerlines. A clearly non-null adjusted association contradicts the outcome-independent assumption.
3. A selection model (logistic regression of "centerline usable" on the covariates). Report only coefficients/ORs with CIs and its c-statistic. A c-statistic near 0.5 means selection close to random.
4. Explicitly repeat checks 1-3 for the read vs unread half and for "in the 744" vs "not in the 744" (the second selection stage).

**Analysis strategy**
- *Primary*: complete-case analysis on the strict tier, with the selection drivers (age, sex, HR/BMI, log CAC) among the candidate predictors or adjusted for, which they mostly already are.
- *Sensitivity 1*: lenient tier. Compare coefficients and apparent and optimism-corrected performance.
- *Sensitivity 2*: IPW using a narrow, stabilised and truncated selection model (per Metten et al.). Report the change in coefficients and calibration-in-the-large.
- *Sensitivity 3 (optional)*: MI of geometry for centerline-excluded but otherwise eligible arteries. Use the outcome in the imputation model (deployment requires geometry, so per Sisk et al. that is appropriate). Caveat: clinical variables probably predict geometry poorly, so MI adds variance rather than information. It is also invalid if missingness is MNAR in the geometry itself (e.g. tortuous vessels failing more often). I would not make it primary.
- Do **not** use missing-indicator approaches (risk under outcome-dependent missingness; Sisk et al.).
- *Intended-use statement* (TRIPOD+AI 3b/5a): the model applies to arteries whose CCTA permits a complete automated or semi-automated trunk centerline. Report the excluded fraction as a limit on applicability.

**Flow diagram (one per artery, never pooled)**
2,116 CGPS → in centerline set (744) → tree matches BL scan date → BL segment reads present → [artery] centerline usable (strict; lenient in brackets) → trunk (and LM) reader-evaluable → trunk (and LM) plaque-free, no stent/CABG/revasc → FU outcome known → analysed, events / non-events. Give the reason counts at each step (TRIPOD+AI 20a/21; STROBE 13b). Apply small-cell suppression to the published diagram too.

### Gaps
- No study was found that quantifies informative exclusion from *automated centerline or geometry failure* in a longitudinal CCTA plaque cohort. Evidence is indirect (image-quality predictors).
- No source was found that directly compares complete-case vs MI vs IPW for *imaging-derived* predictors in prediction models.
- The full texts of Sperrin 2020 and the Vandenbroucke 2007 STROBE E&E were not read; the statements above rest on titles and secondary summaries.

---

## Q5. Unresolved data questions that block the final selection

### Takeaway
The single blocking question is which visit the 744 trees come from. "10Y" in `centerlines_hø_10Y` suggests the 10-year follow-up (CGPS FU median ≈ 10 y), which would make them unusable as baseline predictors. Next in importance are how the 744 were sampled and whether they coincide with the BL-read sub-study.

### Cited Findings
- File name `centerlines_hø_10Y.zip`, 744 cases. — [report_qc.md](../../CGPS_data/report_qc.md)
- CGPS FU median ≈ 10 y (9.5-15). — CGPS data caveats memory (from [report.md](../../CGPS_data/report.md))
- `Readers_Plaque_analyses_finished` = 1 for 769 patients and `Phd_Subjektiv_finished` = 1 for 753 (BL only); BL reads exist for about 1,020. — [report.md l. 5882-5894](../../CGPS_data/report.md); [cgps_report_facts.md](../Plaque%20risk%20model%20with%20CGPS%20data/cgps_report_facts.md)
- Case IDs in the QC lists go up to at least 2,829 (more than 2,116 patients). — [report_qc.md](../../CGPS_data/report_qc.md)

### Inferences — questions for the user to resolve (with the data manager / Kit)
1. **Visit:** Are the 744 trees from BL or FU CCTA? Does "10Y" mean 10-year follow-up? Does "hø" mean anything (a person's initials? "højre"?) Verify by matching volume acquisition dates to `scandate` (aggregate agreement only).
2. **ID mapping:** Are the case IDs in the zip equal to `study_id`? If not, where is the key (IDs > 2,116 exist)?
3. **Sampling:** How were the 744 chosen? Random, consecutive, by scan year, by image quality (pre-screened like ImageCAS-X's 20% exclusion?), or as the Medis/reader sub-study (`Readers_Plaque_analyses_finished` 769, `Phd_Subjektiv_finished` 753)? Were any scans attempted and dropped before the zip was made? Those count as exclusions in the flow diagram.
4. **BL reads:** Do all 744 have BL segment reads (the read half), or do some fall in the 1,094 with empty BL reads? Is SIS/SSS = 0 in the unread half "normal" or "not read"?
5. **Same scan/reconstruction:** Were the trees made from the same reconstruction or phase the readers used? Was the same segmentation pipeline (CoronaryExplorer, the same automated tracker) and the same manual-correction protocol used for all 744? Is there a list of manually corrected vs uncorrected cases?
6. **Label scheme:** What are codes 18, 19, 20, 21, 22 and 28 (and "AL" in code 17)? Are pLAD/mLAD/dLAD and pRCA/mRCA/dRCA boundaries anatomical or rule-based (mLAD ≈ 30.5 mm almost constant)? Is code 13 "LCx" the whole CX beyond pCx (i.e. reader `mcx`+`dcx`)?
7. **Codebooks:** Meaning of `ct_cag_<seg>_eval` codes (0/12/13…), `scan_qualitative_quality` (0/1), `ct_cag_incomplete` (15/16/17), `ct_cag_dominance` codes, BL `PM`, and whether BL `bad_quality` was ever filled in.
8. **Readers:** Are BL and FU read by the same reader(s)/core lab, blinded to each other? (Reader noise: about 20% of BL plaque segments are read plaque-free at FU; [cgps_report_facts.md](../Plaque%20risk%20model%20with%20CGPS%20data/cgps_report_facts.md).) Reader identity is not in the headers.
9. **More trees:** Can BL centerlines be extracted for the remaining read patients (≈1,020 minus the overlap), and/or FU centerlines (for a geometry-change sensitivity analysis or a centerline-vs-read agreement check)? If the 744 are FU, BL extraction becomes mandatory.
10. **Devices:** Are `ct_cag_stent`/`ct_cag_cabg` at BL really largely missing (strata table in report.md around l. 5443 shows values ≈66-68 and 12-16; check whether those are % missing), and how should missing be interpreted (= no device?)?
11. **rand_group:** Is `rand_group` 2 over- or under-represented in the 744? It is a higher-risk, possibly non-randomised stratum ([cgps_report_facts.md §5](../Plaque%20risk%20model%20with%20CGPS%20data/cgps_report_facts.md)).
12. **Tier rules:** Agree the strict and lenient centerline-usable rules, and the unlabelled-percentage and fragment thresholds, *before* looking at outcome associations (pre-specification).

### Gaps
- The meaning of "hø" and "10Y" could not be established from any repository file. It is an inference from the CGPS follow-up length only.
