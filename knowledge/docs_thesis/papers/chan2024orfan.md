# chan2024orfan — ORFAN: CCTA coronary inflammation (FAI Score) and events

**Citation:** Chan K, Wahome E, Tsiachristas A, Antonopoulos AS, Patel P, Lyasheva M, Kingham L, West
H, Oikonomou EK, Volpe L, Mavrogiannis MC, Nicol E, Mittal T, Halborg T, Kotronias R, Adlam D, Modi B,
Rodrigues J, Screaton N, Kardos A, Greenwood JP, Sabharwal N, De Maria GL, Munir S, McAlindon E, Sohan
Y, Tomlins P, Siddique M, Kelion A, Shirodaria C, Pugliese F, Petersen SE, Blankstein R, Desai M,
Gersh BJ, Achenbach S, Libby P, Neubauer S, Channon KM, Deanfield J, Antoniades C; ORFAN Consortium.
*Lancet* 2024;403(10444):2606-2618. doi:10.1016/S0140-6736(24)00596-8. PMID 38823406. PMCID
PMC11664027 (author manuscript).
**Read:** 2026-10-04, full text of the author manuscript on PMC. The supplementary appendix
(methods detail, supplementary tables and figures) was not read.
**Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC11664027/
**Verdict:** The precedent for a non-plaque CCTA marker adding to a clinical risk score, and the
counterexample to "risk estimates use systemic factors only". It is a referred chest-pain cohort, the
marker is inflammation rather than geometry, and the tool is commercial with author conflicts.

## What they did

- **Cohort A:** 40,091 consecutive patients with clinically indicated CCTA in 8 UK hospitals,
  2011 to 2021. MACE (MI, new heart failure, cardiac death) via national data linkage, median 2.7
  years (IQR 1.4 to 5.3). Used for risk profile and event rates.
- **Cohort B (nested):** 3,393 consecutive patients from Royal Brompton and Harefield, 2010 to
  2015, followed for a median of 7.7 years (IQR 6.4 to 9.1). Congenital heart disease and transplant
  referrals were excluded. Used to test the FAI Score and to externally validate AI-Risk.
- **The marker:** the FAI Score (perivascular fat attenuation per artery: RCA, LAD, LCx) and AI-Risk
  (FAI Score plus plaque burden plus clinical factors), both computed with the CaRi-Heart v2.0
  device (Caristo Diagnostics). CAD-RADS 2.0 was read in a core lab.
- **Comparator:** QRISK3, compared on time-dependent c-statistic, continuous NRI and IDI over a
  10-year horizon.

## What they found

- **Cohort A:** 32,533 patients (81.1%) had no obstructive CAD. They accounted for 66.3% of MACE
  (2,857 events) and 63.7% of cardiac deaths (1,118).
- **Cohort B, FAI Score:**
  - FAI Score in every artery predicted cardiac mortality and MACE, independently of risk factors and
    CAD-RADS (Table 3, HRs per SD).
  - With all three arteries in the top versus bottom quartile: cardiac mortality HR 29.8 (95% CI
    13.9 to 63.0), MACE HR 12.6 (8.5 to 18.6).
- **Cohort B, incremental value for cardiac mortality (10-year AUC):**

  | Model | All patients | No obstructive CAD | Obstructive CAD |
  |---|---|---|---|
  | QRISK3 | 0.831 | 0.786 | 0.747 |
  | + CAD-RADS 2.0 | 0.838 (p = 0.36, not significant) | | |
  | + CAD-RADS 2.0 + AI-Risk | 0.854 (p = 7.7×10⁻⁷) | 0.816 (p = 0.0017) | 0.773 |

- **Cohort B, MACE:** QRISK3 0.784, rising to 0.805 with CAD-RADS 2.0 + AI-Risk.
- **Reclassification against QRISK3:** NRI 0.38 (0.23 to 0.45) for cardiac mortality and 0.27
  (0.091 to 0.32) for MACE.

## What the abstract does not tell you

- **"Even in those without any visible plaque"** (Discussion) rests on a subgroup that pooled no and
  minimal atheroma: CAD-RADS 0 and 1 combined, per Table 3's footnote. The HRs in that subgroup are
  adjusted for medications only, not for risk factors.
- **Stenosis grading added nothing to QRISK3** (CAD-RADS p = 0.36 for mortality, p = 0.38 for MACE).
  The added value comes from AI-Risk, which itself contains plaque burden plus FAI Score. The gain from
  FAI alone over QRISK3 + CAD-RADS is not isolated in the main text.
- **Population:** referred, clinically indicated CCTA for chest pain, not the general population. The
  "represents the UK population" claim concerns ethnic mix.
- **Conflicts:** three authors (Neubauer, Channon, Antoniades) are founders, shareholders and
  directors of Caristo, which sells the device. Antoniades holds the licensed patents, and three
  authors are Caristo employees.
- **Conceded limitations:** QRISK3 was trained on the same NHS data (an advantage to the baseline);
  treatment after obstructive findings distorts risk; no hs-CRP to compare with.
- The absolute AUC gains are modest: +0.016 to +0.030.

## What it licenses

- Literature review §3: "Chan et al. (2024) showed in patients referred for CCTA that a measure of
  coronary inflammation added to a clinical risk score, also in patients without obstructive
  disease."
- A gap sentence: imaging already refines systemic risk estimates (inflammation; calcium via the ESC
  guideline), but geometry has not been tested in this role.
- Table row: referred, CCTA, cardiac events, inflammation marker, n = 40,091 (validation 3,393).

## What it does NOT license

- "In people without plaque": that subgroup is CAD-RADS 0 and 1 combined, with medication-only
  adjustment.
- "General population": a referred chest-pain cohort.
- That a CCTA marker improves on stenosis grading alone: CAD-RADS added nothing. The improvement is
  from AI-Risk as a package.
- An independent validation: a manufacturer-affiliated study.

## Open questions

- Does any FAI or ORFAN analysis report geometry? Not in this paper.
- The supplement holds the per-vessel FAI performance (Supplementary Table 11). Read it if the thesis
  quotes FAI's own AUC.
