# cui2017bifurcation — LAD-LCx bifurcation angle and significant left coronary stenosis

**Citation:** Cui Y, Zeng W, Yu J, Lu J, Hu Y, Diao N, Liang B, Han P, Shi H. *PLoS ONE*
2017;12(3):e0174352. doi:10.1371/journal.pone.0174352. PMID 28346530. PMCID PMC5367806. CC BY.
**Read:** 2026-10-04, full text (Europe PMC full-text XML). The S1/S2 data files were not opened.
**Source:** https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5367806/fullTextXML
**Verdict:** A small single-centre cross-sectional study, used as clinical evidence that a wider
LAD-LCx angle accompanies present stenosis. It says nothing about time order, and the angle varies
with cardiac phase.

## What they did

A retrospective single-centre study (Wuhan), 2010 to 2016. 119 consecutive patients with suspected
CAD who had **both CCTA and invasive angiography within three months**, i.e. patients already
referred for invasive work-up (57.5% unstable angina, 21.7% prior PCI). Left main disease and prior
CABG/stents were excluded per the criteria. 13 more were excluded (9 for missing multiphase data).
**n = 106**, mean age 59.9, 70.8% men.

Dual-source CT (Somatom Definition). Three angles (LAD-LCx, LM-LAD, LM-LCx) were measured on MPR
from centreline vectors, in systole and diastole, by two readers. Reference standard: ≥50% stenosis
on invasive angiography.

## What they found

- **LAD-LCx angle by stenosis group at diastole:**

  | Stenosis | Angle |
  |---|---|
  | <50% | 68.3° ± 18.0° |
  | 50 to 69% | 91.3° ± 29.8° |
  | 70 to 100% | 80.0° ± 19.2° |

  p = 0.001. LM-LAD and LM-LCx did not differ.
- Correlation of LAD-LCx with stenosis severity: r = 0.217 at diastole (mild).
- Multivariable logistic: LAD-LCx **per 10°**, OR 1.423 (1.140 to 1.777), p = 0.002, together with
  hyperlipidemia, diameter stenosis and lipid plaque volume.
- Cut-off ≥78°: AUC 0.719, sensitivity 66.7%, specificity 78.4%.
- Wider in non-calcified than calcified lesions (diastole 84.3° vs 74.8°, p = 0.037).
- Reproducibility of LAD-LCx at diastole: inter-observer ICC 0.963, intra-observer 0.993.

## What the abstract does not tell you

- **The relation is not monotonic.** The 50 to 69% group has a wider angle than the 70 to 100% group
  (pairwise p = 1.000), so "wider angle, worse stenosis" overstates it.
- **The angle depends on cardiac phase:** LAD-LCx was 73.6° in systole vs 78.4° in diastole, p <
  0.001, in every group. Comparisons across studies must match the phase.
- The OR is per 10°, and the multivariable model includes CCTA diameter stenosis itself.
- The population is invasive-angiography referrals with left main disease excluded, and 78 normal
  vessels were dropped from the vessel-level analysis.
- Conceded limitations: single centre, n = 106; no FFR.

## What it licenses

- Literature review §3 / table: "Cui et al. (2017) found a wider angle between the LAD and LCx in
  patients with significant left coronary stenosis on invasive angiography", described as
  cross-sectional in referred patients.
- §2 (measurement): the same bifurcation angle differs between systole and diastole. Measurement
  choices change the value.
- Table row: referred (invasive work-up), CCTA, present stenosis, n = 106.

## What it does NOT license

- That the angle precedes or predicts disease: cross-sectional.
- A dose-response: non-monotonic across stenosis grades.
- The "secondary sources' ICC" claim flagged in the old bib note: the ICC is in the paper, 0.963
  inter-observer at diastole.

## Open questions

- Which cardiac phase does the thesis pipeline's CCTA data represent? This matters for comparing
  angles to these values.
