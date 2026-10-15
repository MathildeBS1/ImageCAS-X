# Coronary lumen volume to myocardial mass ratio (V/M) from CCTA: definitions, territory versions, associations

Context: thesis predicting NEW plaque at ~10-year follow-up CCTA in baseline plaque-free LAD/CX/RCA trunks, separate models per artery; candidate feature = territory V/M (artery + branches lumen volume / mass of LV territory it supplies).

Source access notes: full text read for Ihdayhid 2022 review (Leiden open-access PDF), van Rosendael 2023 (hypertension, Leiden PDF), Liu 2021 (PMC), Ding 2025 (Frontiers), Sun 2025 (Europe PMC XML), Choi 2020 (Europe PMC XML). Taylor 2017, Kuneman 2022, Fairbairn 2020, van Diemen 2019, Grover 2017, Gaur 2017, Sellers 2018, Hamdan 2018, Holmes 2019 were read only via abstracts/search snippets or via how the Ihdayhid review summarises them.

## 1. Origin and exact computation of V/M

### Takeaway
V/M was introduced by Taylor et al. (HeartFlow and NXT investigators) in 2017 as total epicardial coronary lumen volume (mm3) divided by LV myocardial mass (g). Mass is segmented LV myocardial volume x 1.05 g/mL, and the lumen includes vessels down to about 1 mm diameter. The first-generation HeartFlow algorithm also added a synthetic microvascular tree, so its values are not comparable with later ones.

### Cited Findings
- **Origin.** Taylor CA, Gaur S, Leipsic J, et al. "Effect of the ratio of coronary arterial lumen volume to left ventricle myocardial mass derived from coronary CT angiography on fractional flow reserve." J Cardiovasc Comput Tomogr 2017;11(6):429–436. PMID 28789941. NXT trial substudy: 238 patients, 438 vessels, all with CCTA, QCA and invasive FFR. — [PubMed](https://pubmed.ncbi.nlm.nih.gov/28789941); [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1934592517301697)
- **Lumen volume (V).**
  - Centrelines and lumen boundaries of the epicardial arteries are traced (deep learning in HeartFlow's pipeline) down to about 1 mm diameter. V is the volume inside the segmented lumen surface.
  - The refined (current) method uses only CT-derived epicardial lumen from vessels >1 mm.
  - Semi-automated segmentation in standard CT software is also feasible.
  - — [Ihdayhid et al., JCCT 2022;16(3):198–206, doi:10.1016/j.jcct.2021.10.007](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **First- vs second-generation algorithm.**
  - The first-generation algorithm "derived the coronary luminal volume as a combination of the segmented epicardial vasculature in addition to the volume of a synthetic tree simulating the microvasculature" and therefore reported higher V/M. This is why Gaur 2017 reports medians of 53–65 mm3/g.
  - The review says the NXT analysis by Taylor 2017 also used "first-generation V/M algorithms", yet its median is 18.57 mm3/g. The review does not resolve this apparent inconsistency.
  - — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Myocardial mass (M).** M = segmented LV myocardial volume x 1.05 g/mL (assumed constant tissue density). Only the LV is used; the RV free wall is excluded. — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view); same 1.05 g/mL in [van Rosendael et al., Am J Cardiol 2023;199:100–109, doi:10.1016/j.amjcard.2023.04.025](https://scholarlypublications.universiteitleiden.nl/access/item%3A3759937/download)
- **ADVANCE registry protocol.**
  - Total luminal volume = "summation of all the segmented coronary arteries".
  - Computed centrally by HeartFlow core lab.
  - Sublingual nitrates given to all patients; metoprolol if heart rate >60 bpm.
  - V/M was not available for all patients because the software was still being developed during the study period.
  - — [van Rosendael 2023](https://scholarlypublications.universiteitleiden.nl/access/item%3A3759937/download)
- **Non-HeartFlow implementation** (Ding et al., Front Cardiovasc Med 2025;12:1449148):
  - Whole tree segmented at the 75% R-R phase, with a manual 1 mm distal threshold and branches >1 mm included. GE AW 4.7 software, density 1.05 g/mL.
  - No nitroglycerin given.
  - Intra-/inter-observer ICC 0.78 / 0.76.
  - — [Frontiers](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2025.1449148/full)
- **Another implementation** (Sun et al. 2025): automatic segmentation on GE "PHIgo" research platform, density 1.05 g/mL, best phase "usually late diastole", no nitroglycerin. — [Sun et al., BMC Cardiovasc Disord 2025;25:552, doi:10.1186/s12872-025-04978-0, PMID 40722136](https://pmc.ncbi.nlm.nih.gov/articles/PMC12302837/)
- **Nitroglycerin effect.** Holmes KR, Fonte TA, Weir-McCall J, et al., Eur Radiol 2019;29:6829–6836. 35 patients scanned twice, after 0.4 mg and after 0.8 mg sublingual nitroglycerin. The higher dose increased coronary luminal volume but did not change FFRCT. The V/M result itself was not retrievable. — [Cambridge repository](https://www.repository.cam.ac.uk/handle/1810/298240); citation from [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Rationale.**
  - FFRCT already uses allometric scaling: resting coronary flow ∝ LV mass^3/4.
  - V/M is framed as "an integrated measure of resting myocardial blood supply and demand".
  - Low V/M is hypothesised to mean larger resting pressure gradients, lower FFR and lower hyperaemic perfusion.
  - — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Invasive precursors:**
  - Lewis & Gotsman, Br Heart J 1973: coronary artery area rose linearly with LV mass.
  - Seiler, Kirkeeide & Gould, Circulation 1992: lumen area relative to regional myocardial mass was 30–50% lower in CAD than in normal angiograms.
  - — as summarised in [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)

### Inferences
- The cardiac phase is not standardised in the HeartFlow papers I could access. Independent groups use the best diastolic phase (75% R-R or late diastole). For a thesis, use one fixed phase per scan and report it.
- Absolute V/M depends on the algorithm and on the distal cutoff. Values from different pipelines (first- vs second-generation HeartFlow, GE AW, PHIgo, ImageCAS-style segmentations) should not be compared on an absolute scale. Within-cohort ranking is what matters.
- Nitroglycerin is a source of within-patient variation in V. Note whether CGPS baseline and follow-up scans used nitro. The FFR-CT CLAUDE notes say FFR-CT has a nitro variable; the BL nitro variable needs checking against the header files.

### Gaps
- I could not access Taylor 2017's full text, so I cannot confirm its exact phase, its exact diameter cutoff, or its precise "first-generation" lumen definition.
- I found no published formal test–retest (scan–rescan) reproducibility study of HeartFlow V/M. The only agreement statistic found is the ICC of 0.76–0.78 from Ding 2025.

## 2. Per-vessel / territory-specific V/M studies

### Takeaway
Territory V/M is still rare and not standardised. As of 2022, HeartFlow and Nørgaard/Leipsic described V/M as limited to a per-patient measure and listed regional V/M as future work. Only a handful of small studies compute a vessel-specific ratio. They use three different ways to get territory mass: allometric diameter-based fractional mass, the fixed AHA 17-segment assignment, and Voronoi tessellation. None is longitudinal.

### Cited Findings
- **2022 status: per-patient only.**
  - The 2022 review states: "The reporting of V/M remains limited to being a per-patient measure of total coronary luminal volume and total LV myocardial mass… the global measure of V/M is limited in identifying the regional heterogeneity of 'vascular health'."
  - Regional V/M "has been limited by the lack of validated CT techniques to quantify fractional myocardial mass in relation to patient-specific coronary anatomy". The review shows "breakdown of myocardial mass and V/M per territory" as a future direction (its Fig. 5).
  - — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Validation of CT fractional mass against invasive perfusion.** Keulards D, Fournier S, van 't Veer M, et al. "Computed tomographic myocardial mass compared to invasive myocardial perfusion measurement." Heart 2020;106:1489–1494. Invasively measured perfusion in all three territories agreed highly with CT-derived fractional mass. — cited in [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Other territory-mass methods cited:**
  - Voronoi-based mass at risk with histological validation: Ide S et al., JCCT 2017;11:179–182.
  - Intracoronary physiology: Murai T et al., Circ Cardiovasc Interv 2019;12:e007322.
  - — cited in [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Liu et al. 2021 — "VR/MR", vessel-specific volume over allometric fractional mass.** Liu J, Li B, Ma J, Wang X, Zhang L, Mao B, Liu Y. "Effect of the ratio of vessel-specific volume to fractional myocardial mass on fractional flow reserve." Exp Biol Med 2021;247(18):1630–1638. doi:10.1177/15353702211027119.
  - Cohort: 205 patients, 241 stenosed vessels (LAD 160, LCX 41, RCA 40).
  - Vessel lumen volume from CTA, including segments ≥1 mm.
  - Fractional mass not segmented. It was estimated from vessel diameter by allometric scaling (D = A·M^3/4 form, citing Choy & Kassab 2008).
  - Results: VR/MR AUC 0.89 vs global V/M AUC 0.62 for FFR ≤0.80. Cut-offs 12.98 vs 23.55 mm3/g; accuracy 87% vs 60%.
  - Weaknesses: retrospective design; the reported CI for the AUC is internally inconsistent; the authors admit the allometric mass estimate may be inaccurate and that plaque distorts the volume–mass relation.
  - — [PMC9597209](https://pmc.ncbi.nlm.nih.gov/articles/PMC9597209)
- **Sun et al. 2025 — vessel-specific V/M with AHA 17-segment territories.** Sun L, Yu Y, Li X, Tong G, Gao B, Liu H, Wang Z. BMC Cardiovasc Disord 2025;25:552.
  - V_LAD, V_LCX and V_RCA came from the segmented tree, using GE PHIgo software.
  - Territory mass used fixed AHA segments: LAD = 1, 2, 7, 8, 13, 14, 17; LCX = 5, 6, 11, 12, 16; RCA = 3, 4, 9, 10, 15.
  - "Some outliers, especially in some right dominant cases, were excluded."
  - Results: 23 primary microvascular angina (PMVA) patients vs 25 matched controls. Vessel-specific V/M was significantly lower for LAD and LCX but not for RCA. Vessel-specific CT-FFR did not differ. Patient-level V/M AUC was 0.753.
  - The lower V/M was driven by higher myocardial mass, not lower volume, which contrasts with Grover 2017.
  - — [PMC12302837](https://pmc.ncbi.nlm.nih.gov/articles/PMC12302837/)
- **Choi et al. 2020 — per-artery cumulative lumen volume vs Voronoi territory mass (scaling, not a V/M biomarker study).** Choi JH, Kim E, Kim HY, Lee SH, Kim SM. "Allometric scaling patterns among the human coronary artery tree, myocardial mass, and coronary artery flow." Physiol Rep 2020;8(14):e14514. doi:10.14814/phy2.14514. PMID 32725793.
  - Data: 43 patients without obstructive lesions, 638 arteries/segments (LAD 233, LCX 209, RCA 196).
  - For each segment: cumulative downstream tree volume V, length L and proximal diameter D, plus Voronoi-tessellated subtended LV mass M (Fujifilm Synapse Vincent).
  - Mean per-segment values: V 437 ± 501 mm3, M 23.0 ± 21.9 g. Per patient: total V 2410 ± 941 mm3, LV mass 129 ± 45 g, which implies a whole-heart V/M of about 19 mm3/g.
  - Fitted exponents:

    | Relation | Fitted exponent (OLS) | Theoretical (Kassab) |
    |---|---|---|
    | V–M | 1.03–1.08 | 1 |
    | L–M | 0.75–0.80 | 3/4 |
    | D–M | about 0.22 | 3/8 |
    | V–D | about 3.4–3.5 | — |

  - D–M is about 43% below theory, which the authors attribute to truncation of the tree to epicardial vessels.
  - Exponents differed significantly between LAD, LCX and RCA. "RCA showed smaller arterial length, arterial volume, and diameter given the same size of myocardium."
  - — [PMC7387886](https://pmc.ncbi.nlm.nih.gov/articles/PMC7387886/)
- **Subtended-mass approach without a volume ratio.** JACC Cardiovasc Imaging study (doi:10.1016/j.jcmg.2017.10.027): "Incremental Value of Subtended Myocardial Mass for Identifying FFR-Verified Ischemia Using Quantitative CT Angiography". It used 3D Voronoi to assign the territories of the three arteries and the mass subtended by each stenosis.
  - V_ratio (subtended % of LV) >30% discriminated FFR-ischaemia with sensitivity 71.4% and specificity 55.6%.
  - V_sub/MLA² >4.16 improved accuracy.
  - — [JACC CVI](https://www.jacc.org/doi/full/10.1016/j.jcmg.2017.10.027) (author list not verified)
- **Kim HY et al. 2016, JACC Cardiovasc Interv:** mass subtended by an artery related to the physiological severity of a stenosis. — cited by [Liu 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC9597209)
- **Post-PCI subanalysis.** International prospective PCI study (120 patients, 123 vessels) with Voronoi-based territory mass from CCTA. Post-PCI RFR and FFR were associated with subtended myocardial mass and with the coronary volume-to-mass ratio. — search-snippet only; primary citation not verified (surfaced alongside [PMC9597209](https://pmc.ncbi.nlm.nih.gov/articles/PMC9597209))
- **Grover et al. 2017 — closest to a per-system split.** Microvascular angina (MVA) vs controls: lower V/M was driven mainly by lower *left* coronary lumen volume (1117 ± 80 vs 1750 ± 98 mm3). Volume was split by left vs right system, but mass was not split by territory. — [Ihdayhid 2022 Table 1](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view); [PubMed 28993120](https://pubmed.ncbi.nlm.nih.gov/28993120/)
- **Sellers et al. 2018 (HCM):** greater coronary volume in HCM, with "equal contribution from the right and left coronary systems". — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Swine validation of territory assignment.** An automated vessel-specific minimum-cost-path method matched reference territory mass closely (slope 0.99, R² 1.00). The AHA 17-segment model underestimated it (M_AHA = 0.81·M_REF + 5.03 g). — search summary only (source surfaced in [PMC9597209](https://pmc.ncbi.nlm.nih.gov/articles/PMC9597209) search; primary citation not verified)

### Inferences
- The thesis feature (artery-plus-branches lumen volume divided by the mass of that artery's own territory) corresponds most closely to Sun 2025 (AHA territories) and Choi 2020 (Voronoi territories). Liu 2021 is a weaker variant because its mass is not segmented but derived from diameter, which makes the ratio partly circular.
- **Use Voronoi / nearest-centreline territories rather than AHA 17-segment.**
  - AHA segments are a fixed population template. They ignore dominance, which Sun 2025 had to exclude as outliers, and they underestimate territory mass in animal validation.
  - Voronoi follows patient-specific anatomy (Ide 2017 histological validation; Keulards 2020 perfusion agreement).
  - Caveat: with Voronoi, a large artery claims more myocardium, so V and M are coupled by construction. Expect V–M exponents of about 1 (Choi 2020), not independent variation.
- RCA has systematically lower lumen volume per gram of territory (Choi 2020). This supports the user's decision to fit separate per-artery models rather than pooling. Territory V/M must not be compared across arteries on an absolute scale.
- With separate per-artery models, LV territory mass should be defined consistently. RCA territory mass from the LV excludes the RV free wall, which the RCA also supplies, so RCA V/M from LV-only mass is biased upward. Choi 2020 and Sun 2025 both used LV mass only.

### Gaps
- I found no study that computed territory V/M at baseline and related it to future plaque in that territory.
- I found no reproducibility data specifically for territory V/M.
- I found no HeartFlow peer-reviewed publication (through 2026) that reports a validated per-territory V/M product. The 2022 review shows it only as a future direction. A targeted PubMed check for 2023–2026 HeartFlow regional V/M abstracts is recommended.
- I could not verify primary citations for the post-PCI Voronoi V/M subanalysis or for the swine minimum-cost-path study.

## 3. What V/M is associated with (cross-sectional and outcome evidence)

### Takeaway
Low global V/M is consistently associated, cross-sectionally, with:
- lower invasive FFR and FFRCT, independent of stenosis and plaque;
- more plaque and more stenosis;
- diabetes;
- microvascular angina, HCM, STEMI/ACS.

Women have higher V/M than men. Hypertension is not associated once adjusted. Correlations with PET flow are weak. Outcome data are limited to small or short-term studies. No longitudinal study links baseline V/M to future plaque development or progression.

### Cited Findings
**FFR / ischaemia**
- **Taylor 2017 (NXT).**
  - Below vs above the median V/M (18.57 mm3/g): FFR 0.80 ± 0.12 vs 0.87 ± 0.08 (p<0.0001); QCA diameter stenosis 38% vs 31%; total plaque volume 593 vs 392 mm3.
  - In vessels with ≤50% stenosis: FFR 0.81 vs 0.88.
  - V/M independently predicted FFR ≤0.80, independent of sex, BMI, stenosis and plaque.
  - Pearson r(FFR, V/M) = 0.33.
  - — [PubMed 28789941](https://pubmed.ncbi.nlm.nih.gov/28789941); [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **van Diemen et al. 2019 (PACIFIC; 152 patients, 431 vessels).** van Diemen PA, Schumacher SP, Bom MJ, et al. J Cardiovasc Comput Tomogr 2019;13(4):179–187.
  - Median V/M 20.71 mm3/g.
  - Low vs high V/M: abnormal vessel hyperaemic MBF 34% vs 19%; FFR ≤0.80 20% vs 9%.
  - No difference in mean hyperaemic MBF (3.27 vs 3.51 mL/min/g) or CFR (3.20 vs 3.22).
  - Weak correlations with vessel MBF (R = 0.148) and global MBF (R = 0.179).
  - The authors suggested regional V/M might correlate better.
  - — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view); [VU repository](https://research.vu.nl/en/publications/18a7c105-98ae-4af1-b047-16464acc47d8)
- **Liu 2021:** global V/M performed poorly for vessel-level ischaemia (AUC 0.62, r ≈ 0.06–0.14); vessel-specific VR/MR performed better (AUC 0.89). — [PMC9597209](https://pmc.ncbi.nlm.nih.gov/articles/PMC9597209)

**Sex and age**
- **Fairbairn et al. 2020 (ADVANCE, n=4737).** Fairbairn TA, Dobson R, Hurwitz-Koweek L, et al. "Sex differences in coronary computed tomography angiography-derived fractional flow reserve: lessons from ADVANCE." JACC Cardiovasc Imaging 2020;13:2576–2587. doi:10.1016/j.jcmg.2020.07.008.

  | Measure | Women | Men |
  |---|---|---|
  | Lumen volume (mm3) | 2548 ± 768 | 3226 ± 977 |
  | LV mass (g) | 100 ± 23 | 133 ± 30 |
  | V/M (mm3/g) | 26.2 ± 7.6 | 24.8 ± 7.2 |

  - Women's higher V/M is driven by lower LV mass.
  - Female sex, stenosis severity, multivessel disease and FFRCT were independently associated with V/M.
  - Higher V/M was independently associated with lower 90-day revascularisation.
  - — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view); [Beaumont repository](https://scholarlyworks.beaumont.org/cardiology_articles/164)
- No primary study I accessed reports a direct V/M–age association.

**Diabetes**
- **Kuneman et al. 2022 (ADVANCE, n=3053, 21.9% diabetic).** Kuneman JH, et al. "Coronary volume to left ventricular mass ratio in patients with diabetes mellitus." J Cardiovasc Comput Tomogr 2022;16(4):319–326.
  - Diabetic vs non-diabetic: lumen volume 2850 ± 940 vs 3040 ± 970 mm3 (p<0.0001); LV mass similar (about 122 g, p=0.70); V/M 23.9 ± 6.8 vs 25.7 ± 7.5 mm3/g (p<0.0001).
  - The difference held in both obstructive and non-obstructive CAD.
  - — [UTU repository](https://www.utupub.fi/items/c4e6dfcc-c0fc-4e72-98e3-8db64613550f/full); [Monzino](https://www.cardiologicomonzino.it/en/scientific-papers/2022/02/25/coronary-volume-to-left-ventricular-mass-ratio-in-patients-with-diabet/2662/)

**Hypertension / LVH**
- **van Rosendael et al. 2023 (ADVANCE, n=2378, 56% hypertensive; diabetics excluded).**
  - Hypertensive vs normotensive: LV mass 122.7 vs 120.0 g; lumen volume 3105 vs 2966 mm3; V/M 26.0 vs 25.3 mm3/g.
  - After ANCOVA adjustment (age, BMI, hyperlipidaemia, sex, number of obstructive vessels, maximum stenosis), V/M did not differ (difference 0.48 mm3/g, p=0.116). Volume and mass were both still higher.
  - Conclusion: coronary volume scales up with LV mass in hypertension.
  - — [van Rosendael 2023](https://scholarlypublications.universiteitleiden.nl/access/item%3A3759937/download)
- **Hamdan et al. 2018 (HCM n=55 vs secondary LVH from hypertension/aortic stenosis n=176).** Hamdan A, et al. JACC Cardiovasc Imaging 2018;11:1926–1928. In secondary LVH, V/M fell in proportion to rising LV mass. In HCM it was disproportionately low for any given mass. — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Sellers et al. 2018 (37 HCM vs 37 controls).** Sellers SL, et al. JCCT 2018;12:467–471.
  - HCM: higher mass (176 vs 119 g) and higher volume (4112 vs 3290 mm3), but lower V/M (23.8 vs 26.5 mm3/g) and lower nadir FFRCT.
  - Lowest V/M in septal HCM.
  - — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)

**Microvascular angina**
- **Grover et al. 2017.** Grover R, Leipsic JA, Mooney J, et al. JCCT 2017;11:423–428. V/M 25.6 ± 5.9 in MVA vs 30.0 ± 6.5 mm3/g in controls, driven by lower lumen volume. — [PubMed 28993120](https://pubmed.ncbi.nlm.nih.gov/28993120/); [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Sun 2025:** lower V/M in Chinese PMVA, driven by higher mass. — [PMC12302837](https://pmc.ncbi.nlm.nih.gov/articles/PMC12302837/)

**Ethnicity**
- **Ihdayhid et al. 2020 (JCCT; 100 Caucasian, 100 South Asian, 100 East Asian):** V/M 29.3 (East Asian) vs 25.3 (Caucasian) vs 25.3 mm3/g (South Asian). — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)

**Plaque burden and stenosis**
- Low V/M goes with more plaque volume and more stenosis (Taylor 2017).
- In ADVANCE, stenosis severity and multivessel disease were independently associated with V/M (Fairbairn 2020).
- — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)

**Calcium score**
- I found no primary study that reports a V/M–CAC association.

**Acute coronary syndromes and events**
- **Gaur et al. 2017 (first-generation algorithm).** Gaur S, Taylor CA, Jensen JM, et al. JACC Cardiovasc Imaging 2017;10:424–433.
  - Post-STEMI median V/M 53 vs 65 mm3/g in stable CAD (p=0.009).
  - Lowest (40 mm3/g) in 8 patients who needed unplanned PCI within 12 months.
  - — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Ding et al. 2025 (n=450).** Ding E, Chen L, Wei X, You D, Pan C. Front Cardiovasc Med 2025;12:1449148.

  | Group | V/M (mm3/g) |
  |---|---|
  | Controls | 43.3 ± 11.5 |
  | Stable angina | 31.0 ± 9.9 |
  | Unstable angina | 24.3 |
  | AMI | 17.8 |

  - AUC for ACS: 0.78, vs 0.74 for FFRCT.
  - V/M independently associated with high GRACE score (OR 0.153).
  - CCTA was performed 0.5–6 months *before* the ACS event.
  - — [Frontiers](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2025.1449148/full)
- **Li W et al. 2025 (TAVR).** BMC Cardiovasc Disord 2025;25:311. PMID 40269687. Low V/M (median cut-off 33.31 mm3/g) was associated with MACE after transcatheter aortic valve replacement, driven by higher LV mass. — reference list of [Sun 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12302837/); [BMC PDF](https://biomedcentral-bmccardiovascdisord.publicaciones.saludcastillayleon.es/counter/pdf/10.1186/s12872-025-04705-9.pdf)

**Longitudinal plaque development or progression**
- None found. Searches for serial-CCTA studies relating baseline V/M (global or territorial) to new plaque or plaque progression returned no such study. The 2022 review's future-directions section does not mention plaque progression. It asks only whether V/M is modifiable and whether improving it improves outcomes. — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Related serial-CCTA remodelling evidence.** Multicentre study of 1245 patients and 5721 segments: per 1 mm3 of added plaque, vessel volume rose by about 0.71 mm3 and lumen volume fell by about 0.29 mm3, i.e. plaque growth partly reduces lumen. — search summary; [Leiden repository](https://scholarlypublications.universiteitleiden.nl/access/item%3A3638655/view) (primary citation details not verified)

### Inferences
- **No longitudinal V/M–plaque link exists.** Using baseline territory V/M to predict *new* plaque in a plaque-free trunk is, as far as I found, a novel hypothesis. It should be framed as exploratory, not as replicating established evidence.
- **Plausible mechanisms (speculative):**
  - Low V/M implies higher flow per lumen cross-section, so higher wall shear stress under allometric flow ∝ M^3/4. That would predict *less* atherogenic low-WSS, which argues against low V/M → new plaque.
  - Alternatively, low V/M may mark diabetes, microvascular or endothelial dysfunction, or a small "constitutional" vessel calibre, which could predict *more* plaque.
  - The sign of the effect is therefore not predictable a priori. A two-sided test is appropriate.
- **Confounding.** V/M differs by sex (via LV mass), diabetes (via volume), HCM and LVH (via mass). Models should include sex, diabetes and LV mass or BMI/BSA as covariates, or use V and M as separate terms, or both. All are available or derivable in CGPS: `male`, diabetes history and medication, HbA1c, BMI, BSA; LV mass from the CT volume.
- **Reverse causality.** Restricting to baseline plaque-free trunks reduces the problem that existing plaque lowers lumen volume. Plaque in the *branches* included in the territory volume would still reduce V. Consider excluding, or adjusting for, baseline plaque elsewhere in the territory (per-segment `ct_cag_<segment>_plaque_type` / `_stenosis` at BL).

### Gaps
- No V/M–CAC association study found.
- No direct V/M–age study found.
- No study of V/M under statins or other medication.
- No large prospective hard-outcome (MACE) study of global V/M in stable patients beyond the 90-day revascularisation endpoint in ADVANCE.

## 4. Typical values, normal ranges, reproducibility

### Takeaway
With the current HeartFlow method, global V/M in symptomatic CAD cohorts is about 25 mm3/g (median 24.8, range 5.6–62.5). First-generation values (50–65 mm3/g) and some non-HeartFlow pipelines (43 mm3/g in Chinese controls) are much higher, so absolute values are method-specific. No population-based "normal range" exists.

### Cited Findings
- **ADVANCE (n=3110), current algorithm:**

  | Measure | Mean | Median | Range |
  |---|---|---|---|
  | Lumen volume (mm3) | 3003 | 2873 | 493–7891 |
  | LV mass (g) | 122 | 118 | 55–357 |
  | V/M (mm3/g) | 25.2 | 24.8 | 5.6–62.5 |

  — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Medians in other cohorts:**
  - NXT: 18.57 mm3/g ([PubMed 28789941](https://pubmed.ncbi.nlm.nih.gov/28789941)).
  - PACIFIC: 20.71 mm3/g ([VU](https://research.vu.nl/en/publications/18a7c105-98ae-4af1-b047-16464acc47d8)).
  - Chinese stenosed-vessel cohort: 25.86 mm3/g ([PMC9597209](https://pmc.ncbi.nlm.nih.gov/articles/PMC9597209)).
- **Non-HeartFlow controls with normal angiograms:** 43.3 ± 11.5 mm3/g (GE AW, no nitro). — [Ding 2025](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2025.1449148/full)
- **First-generation algorithm (epicardial plus synthetic microvascular tree):** medians 53–65 mm3/g. — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Territory level (derived from Choi 2020's per-segment means):** cumulative V 437 mm3 and Voronoi M 23 g, roughly 19 mm3/g. These are not per-trunk values; they are averaged across all segment origins. — [PMC7387886](https://pmc.ncbi.nlm.nih.gov/articles/PMC7387886/)
- **Liu 2021 vessel-specific VR/MR:** median 16.35, mean 14.72 mm3/g; ischaemia cut-off 12.98. — [PMC9597209](https://pmc.ncbi.nlm.nih.gov/articles/PMC9597209)
- **Reproducibility:** intra-observer ICC 0.78, inter-observer ICC 0.76 (Ding 2025). — [Frontiers](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2025.1449148/full)

### Inferences
- An ICC of about 0.76–0.78 is only moderate. Measurement error in V/M will dilute effect estimates (regression dilution). The thesis should report its own segmentation reproducibility, for example on a re-segmented subset.

### Gaps
- No healthy population-based reference values (e.g., asymptomatic general population such as CGPS) were found.
- No published scan–rescan reproducibility.
- No age- or sex-specific normal curves.

## 5. Limitations and criticisms

### Takeaway
V/M depends on how the coronary tree is segmented and truncated, on vasodilator state (nitroglycerin), and on LV mass, so in practice it is partly an LV-mass index. It correlates only weakly with perfusion. Existing plaque lowers lumen volume (reverse causality). Global V/M hides regional heterogeneity. Nearly all evidence is retrospective, cross-sectional and industry-linked.

### Cited Findings
- **Segmentation and truncation dependence.**
  - Lumen volume "is dependent on the image analysis methods used to segment the coronary arteries and the extent of the tree that is resolved".
  - Spatial resolution "prohibits the complete visualization of the coronary vasculature".
  - — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
  - Small-vessel detection is limited by resolution and motion. — [Ding 2025](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2025.1449148/full)
  - Truncated trees bias scaling exponents. — [Choi 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7387886/)
- **Algorithm generations are not comparable** (synthetic microvasculature vs none). — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Vasodilator state.** Higher nitroglycerin dose increases lumen volume. — [Holmes 2019](https://www.repository.cam.ac.uk/handle/1810/298240)
  - Endothelial or microvascular function affects epicardial vasodilation and hence V. — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **LV mass confounding.**
  - Sex differences in V/M are driven by LV mass ([Fairbairn 2020 via Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)).
  - Secondary LVH lowers V/M in proportion to mass (Hamdan 2018).
  - Hypertension shows no adjusted difference because volume scales up with mass ([van Rosendael 2023](https://scholarlypublications.universiteitleiden.nl/access/item%3A3759937/download)).
- **Weak link to perfusion:** R ≈ 0.15–0.18 with PET MBF. — [van Diemen 2019 via Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Reverse causality from plaque.**
  - Low-V/M patients have more plaque and stenosis (Taylor 2017).
  - Plaque growth reduces lumen volume (about 0.29 mm3 of lumen lost per 1 mm3 of plaque in serial CCTA) — [Leiden](https://scholarlypublications.universiteitleiden.nl/access/item%3A3638655/view).
  - Liu 2021 states that plaque may distort the volume–mass relationship — [PMC9597209](https://pmc.ncbi.nlm.nih.gov/articles/PMC9597209).
- **Global measure misses regional disease.** — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Territory-assignment error.**
  - AHA templates underestimate territory mass in swine.
  - Dominance-related outliers had to be excluded with AHA territories. — [Sun 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12302837/)
- **Study design.**
  - Studies are predominantly retrospective, observational case–control. — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
  - Many key papers have HeartFlow employees or HeartFlow-funded authors. Taylor and Updegrove are HeartFlow employees; Leipsic holds HeartFlow stock options. — [Ihdayhid 2022 competing interests](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)

### Inferences
- In the thesis population, the main threat to interpretation is that territory V/M partly encodes LV territory mass (body size, sex, BP) and partly encodes vessel calibre. Reporting V, M and V/M separately is advisable, as is an allometric alternative such as residuals of log V on log M within each artery.
- Partial-volume effects and the threshold of the ImageCAS-trained segmentation will set the effective distal cutoff. Fix a diameter cutoff (e.g., ≥1 mm, as in HeartFlow and Ding 2025) to standardise across scans.

### Gaps
- No formal methodological critique paper of V/M (e.g., a letter or editorial challenging it) was found.

## 6. Allometric scaling laws underpinning V/M

### Takeaway
V/M rests on Kassab-group scaling theory:
- coronary tree volume scales approximately linearly with perfused myocardial mass (V ∝ M^1);
- flow scales as M^3/4;
- diameter scales as M^3/8.

So V/M should be roughly constant in healthy vessels. Human CCTA data support V–M ≈ 1 for epicardial trees but show weaker-than-theory D–M scaling and artery-specific differences.

### Cited Findings
- **Theoretical exponents** (Choy & Kassab 2008; Huo & Kassab 2009), as listed by Choi 2020:

  | Relation | Exponent |
  |---|---|
  | L–M | 3/4 |
  | V–M | 1 |
  | D–M | 3/8 |
  | V–L | 9/7 |
  | D–L | 3/7 |
  | V–D | 3 |
  | Q–M | 3/4 |
  | Q–D | 7/3 |

  — [PMC7387886](https://pmc.ncbi.nlm.nih.gov/articles/PMC7387886/)
- **Primary sources:**
  - Choy JS, Kassab GS. "Scaling of myocardial mass to flow and morphometry of coronary arteries." J Appl Physiol 2008;104:1281–1286. Cited as the foundational reference (ref. 1) in [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view).
  - Huo Y, Kassab GS. Vascular volume scaling law (2009): cumulative volume relates to cumulative length and diameter; validated in pig coronary trees and other organs. — [PMC2716468](https://pmc.ncbi.nlm.nih.gov/articles/PMC2716468)
- **Mass–diameter relation:** myocardial mass ∝ vessel area^4/3, i.e. ∝ D^8/3 (equivalently D ∝ M^3/8). — [Kassab & Finet, EuroIntervention 2015, doi:10.4244/EIJV11SVA3](https://eurointervention.pcronline.com/article/anatomy-and-function-relation-in-the-coronary-tree-from-bifurcations-to-myocardial-flow-and-mass)
- **Clinical use of length–volume scaling** to detect diffuse CAD on CT: Huo et al., Radiology 2013. — [Wright State repository](https://corescholar.libraries.wright.edu/cse/309)
- **FFRCT's flow model:** resting flow ∝ LV mass^3/4. — [Ihdayhid 2022](https://scholarlypublications.universiteitleiden.nl/access/item%3A3567756/view)
- **Human CCTA validation (Choi 2020):**
  - Unadjusted OLS exponents: V–M 1.031, L–M 0.750, D–M 0.215, V–D 3.387.
  - D–M and D–L were well below theory; the authors attribute this to truncation at epicardial vessels.
  - Exponents differed between LAD, LCX and RCA; the RCA is smaller for the same mass.
  - — [PMC7387886](https://pmc.ncbi.nlm.nih.gov/articles/PMC7387886/)
- **Liu 2021** used D = A·M^3/4 to estimate fractional mass from diameter. This form differs from the 3/8 diameter exponent above. — [PMC9597209](https://pmc.ncbi.nlm.nih.gov/articles/PMC9597209)
- **Murray's law** (flow ∝ D^3 at bifurcations; minimum-work principle) underlies these exponents. Specific primary-source details were not retrieved in this search and come from background knowledge (Murray CD, Proc Natl Acad Sci USA 1926;12:207–214). Kassab & Finet 2015 discusses bifurcation laws in the coronary tree. — [EuroIntervention](https://eurointervention.pcronline.com/article/anatomy-and-function-relation-in-the-coronary-tree-from-bifurcations-to-myocardial-flow-and-mass)

### Inferences
- Because V ∝ M^≈1, a simple ratio V/M is a reasonable size normalisation for epicardial trees. With artery-specific exponents slightly different from 1, a log-log residual (log V − b·log M, with b estimated per artery) is a more principled "relative lumen deficit" feature. It fits the per-artery modelling strategy.
- Liu 2021's use of a 3/4 diameter exponent conflicts with Kassab's D ∝ M^3/8. This is a further reason not to estimate territory mass from diameter, and instead to segment it with Voronoi.

### Gaps
- I did not retrieve the Huo & Kassab 2009 full text or Murray 1926 directly. Their exact exponents are taken from Choi 2020's summary and from background knowledge.
