# tommasino2024clap — CLAP score: left main bifurcation angle and LAD outcomes

**Citation:** Tommasino A, Dell'Aquila F, Redivo M, Pittorino L, Mattaroccia G, Tempestini F, Santucci
S, Casenghi M, Giovannelli F, Rigattieri S, Berni A, Barbato E. *Journal of Cardiovascular
Development and Disease* 2024;11(11):338. doi:10.3390/jcdd11110338. PMID 39590181. PMCID
PMC11595042. Open access.
**Read:** 2026-10-04, full text on PMC. Supplementary tables and figures (S1 to S5) were not read.
**Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC11595042/
**Verdict:** The only angle-to-outcome study in the bib, but its statistical reporting is internally
inconsistent and its "MACE" is mostly clinician-driven revascularisation and progression. Cite it at
most as one single-centre report, never for its effect sizes.

## What they did

A single-centre registry (Rome), March 2021 to March 2023. 650 consecutive patients **referred for
CCTA for suspected CAD**. Excluded: 66 with poor image quality or prior CABG, and 85 with a ramus
intermedius. **n = 499**: 78.3% men, hypertension 73.1%, proximal LAD disease 42.1%, prior LAD PCI
22.0%.

LMBA was measured by two operators on 128-slice CCTA (GE Volume Viewer, 2D/3D), and by 3D-QCA in the
288 patients who had invasive angiography.

Follow-up was one year (mean 374 days). The MACE composite: cardiovascular death, MI, PCI, TLR, and
"progression" in the proximal LAD. Progression was assessed by imaging done "when clinically
indicated or in cases where baseline CCTA or ICA had identified a plaque with high-risk features".
The CLAP score was developed and then externally validated on 200 patients from another hospital.

## What they found

- **Primary endpoint (a):** LMBA agreed between CCTA and 3D-QCA (mean difference −0.25°). AUC for
  significant proximal LAD stenosis: 0.84 (CCTA) and 0.86 (3D-QCA). Optimal cut-off 80° (sensitivity
  0.93, specificity 0.70).
- **Cross-sectional angle:** LMBA 106.4° ± 29.4° with significant LAD stenosis vs 74.7° ± 27.2°
  without.
- **Primary endpoint (b), MACE:**
  - 12.47% overall: progression 42 (8.4%), TLR 12 (2.4%), MI elsewhere 5 (1%), CV death 3 (0.6%);
  - LMBA >80°: 19.8% vs 7.4%;
  - reported "HR" for LMBA >80°: 4.47 (95% CI 3.80 to 6.70).
- **CLAP score:** AUC 0.91 in development, 0.85 in external validation.

## What the abstract does not tell you

- **The interval is wrong, and so are other numbers in Table 2.** From the table's own B and SE:
  - **LMBA:** B 1.499, SE 0.206 gives a 95% CI of **2.99 to 6.70**, not 3.80 to 6.70.
  - **CKD:** B 0.537, SE 0.422 gives Wald 1.62, **p ≈ 0.20**, CI 0.75 to 3.91, which crosses 1.
    The paper reports p = 0.041 and CI 1.31 to 6.72.
  - **Diabetes:** Wald 14.7 gives p ≈ 0.0001, not the reported 0.031.
  The table is labelled logistic regression (odds ratios), while the text calls the same numbers Cox
  hazard ratios.
- **"MACE" is soft and clinician-dependent.** Hard events were 8 of 499 (5 MI, 3 deaths). The rest is
  PCI/TLR and "progression", ascertained by imaging that was triggered partly by baseline findings.
  Wide angles go with baseline LAD stenosis, so wide-angle patients are more likely to be re-imaged
  and treated. This is an incorporation/verification bias that the paper does not address.
- The population is diseased: 42% had proximal LAD disease and 22% prior LAD PCI. The 80° cut-off
  was derived for present stenosis, then reused for outcomes in the same data.
- No limitations paragraph addressing these issues was found. The authors concede only that hard
  outcomes need larger studies.

## What it licenses

- At most, in literature review §3: "Tommasino et al. (2024) reported in a single centre that a wide
  left main bifurcation angle accompanied proximal LAD disease and its progression within a year in
  referred patients". Pair it with a design caveat, and do not quote its effect size.
- As a methods point: CCTA and invasive 3D-QCA give similar left-main bifurcation angles (mean
  difference −0.25°) in this cohort.

## What it does NOT license

- "Bifurcation angle predicts MACE, HR 4.47": the interval is inconsistent with its own SE, and the
  endpoint is soft and biased.
- Plaque onset or general-population risk: a diseased, referred cohort.
- Any of its CIs or p-values, without recomputation.

## Open questions

- Table S1 and Figure S3 (event counts by angle group, CLAP validation) are in the unread supplement.
- Is there an erratum? None found on the PMC page as of 2026-10-04.
