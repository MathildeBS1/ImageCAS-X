# Partitioning LV myocardium into coronary territories (LAD / LCx / RCA) from CCTA

Scope: methods for assigning LV myocardium to a supplying artery, how well they are validated, practical pitfalls, and code. Purpose: per-artery territory mass for territory-specific lumen-volume / myocardial-mass (V/M) ratios in separate LAD, CX and RCA models.

Research done 2026-10-12 with about 20 search and fetch calls. Several full texts were paywalled (ScienceDirect, BMJ Heart, Nature/npj). Where only an abstract or snippet was available, that is stated. Figures marked "(snippet)" come from search-result abstracts, not from a full-text read.

---

## 1. What partitioning methods exist, and who published them?

### Takeaway
The workhorse is **3D Euclidean nearest-vessel ("Voronoi") assignment**. Each LV voxel goes to the nearest voxel of the segmented coronary tree, and voxels are then summed per branch distal to a seed. This is established: it is commercial (Fujifilm Synapse Vincent), has been validated in swine against histology, against SPECT/MRI/invasive perfusion in small clinical series, and has a 948-patient reference-value study.
The alternatives are research-grade:
- geodesic distance on the epicardium or within the myocardium (Termeer; a Harvard pig study)
- minimum-cost-path assignment (Molloi group)
- allometric/diameter scaling, which gives a mass estimate with no spatial map
- synthetic-tree / constrained-constructive-optimisation growth (CFD community)
- the population AHA 17-segment model, optionally adjusted for dominance

### Cited Findings
**Euclidean 3D Voronoi (nearest vessel), the established method**
- Kurata A, Kono A, Sakamoto T, Kido T, Mochizuki T, et al., "Quantification of the myocardial area at risk using coronary CT angiography and Voronoi algorithm-based myocardial segmentation", *Eur Radiol* 2015;25:49–57, doi:10.1007/s00330-014-3388-2. It describes Voronoi as dividing 2D/3D space "between pre-determined points or lines based on the shortest distance to those points/lines". The CTA area at risk is the sum of territories distal to a >50% stenosis, as a fraction of LV volume — [Springer](https://link.springer.com/doi/10.1007/s00330-014-3388-2); [RSNA 2014 abstract](https://archive.rsna.org/2014/14009842.html)
- Stalikas N, Mizukami T, … De Bruyne B, Collet C, "Vessel-Specific Myocardial Mass in Patients With Stable Coronary Artery Disease", *J Am Heart Assoc* 2025;14:e039013, doi:10.1161/JAHA.124.039013. Algorithm as described there:
  - The software (Synapse Vincent v5, Fujifilm) "assigns each voxel of the LV volume to the nearest voxel of an adjacent coronary artery".
  - It then "aggregates all myocardial voxels associated with the voxels of the coronary artery distal to the seed point".
  - Mass = volume × 1.05 g/cm³.
  - A seed is placed at each vessel ostium.
  - [SGUL open access PDF](https://openaccess.sgul.ac.uk/id/eprint/118057/2/stalikas-et-al-2025-vessel-specific-myocardial-mass-in-patients-with-stable-coronary-artery-disease.pdf)
- Stalikas et al. state that CCTA offers two ways to get vessel-specific mass: (1) Voronoi nearest-neighbour (citing Kurata 2015) and (2) allometric scaling "using diameter-derived regional flow as a proportion of the myocardial volume" (citing Keulards 2020) — [Stalikas 2025](https://openaccess.sgul.ac.uk/id/eprint/118057/2/stalikas-et-al-2025-vessel-specific-myocardial-mass-in-patients-with-stable-coronary-artery-disease.pdf)
- Hsieh Y-F, Lee C-K, Wang W, et al., "Coronary CT angiography-based estimation of myocardial perfusion territories for coronary artery FFR and wall shear stress simulation", *Sci Rep* 2021;11:13855, doi:10.1038/s41598-021-93237-1, PMID 34226598.
  - Each LV voxel is assigned to the nearest of LAD / LCx / RCA.
  - Territory size sets outlet flow via Q = 0.64·M^0.75.
  - Murray's law is applied because "small and trivial side branches invisible on CCTA images are neglected".
  - In 20 patients, FFR accuracy was 0.88.
  - [PMC8257574](https://pmc.ncbi.nlm.nih.gov/articles/PMC8257574/)
- A Philips patent covers assigning myocardium feeding territories by Voronoi diagram and/or Delaunay triangulation relative to a coronary tree model — [USPTO 11207043](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11207043)

**Projection to the epicardium plus geodesic Voronoi (Termeer)**
- Termeer M, et al. (TU Wien / Eindhoven), "Patient-specific coronary artery supply territory AHA diagrams" (SCMR 2009; *JCMR* 2009;11(Suppl 1):P103, doi:10.1186/1532-429X-11-S1-P103):
  - Centrelines are projected onto the epicardial surface.
  - A Voronoi diagram is computed with a **geodesic** distance on that surface.
  - Boundaries are extracted with modified marching squares.
  - Results are shown on a patient-specific bull's-eye.
  - Evaluated on 5 patients only, with no quantitative validation.
  - Reported failure case: the LAD territory was too large because the LAD was over-segmented near the apex.
  - [PMC7860735](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7860735/); [poster](https://www.cg.tuwien.ac.at/research/publications/2009/termeer-2009-scmr/termeer-2009-scmr-poster.pdf); [JCMR](https://jcmr-online.biomedcentral.com/articles/10.1186/1532-429X-11-S1-P103)
- Later book chapter: "Patient-Specific Mappings between Myocardial and Coronary Anatomy", Dagstuhl Follow-Ups (Scientific Visualization) 2010, doi:10.4230/DFU.SciViz.2010.196 — [Dagstuhl](https://drops.dagstuhl.de/entities/document/10.4230/DFU.SciViz.2010.196)

**Geodesic distance within the myocardium**
- "Estimation of Myocardial Volume at Risk from CT Angiography" (Harvard SPL / NAC) uses geodesic rather than Euclidean distance and is tested on pig-heart CTA. Snippet only; authors not retrieved — [NAC SPL](https://nac.spl.harvard.edu/publications/estimation-myocardial-volume-risk-ct-angiography)

**Proximity on micro-CT casts (Le / Molloi)**
- "Le et al." determined the territory fed by a coronary "by proximity to the coronary vessel", evaluated on micro-CT of radio-opaque porcine cast hearts. This is cited in a TU Delft thesis; the original citation was not retrieved — [TU Delft repository](https://repository.tudelft.nl/file/File_85d3c3c5-427f-4574-88e6-ba8298f6e2da?preview=1)

**Minimum-cost-path assignment (Malkasian, Hubbard, Molloi, UC Irvine)**
- "Quantification of vessel-specific coronary perfusion territories using minimum-cost path assignment and CT angiography: validation in a swine model", *J Cardiovasc Comput Tomogr* 2018, doi:10.1016/j.jcct.2018.06.006 (6 swine) — [escholarship](https://www.escholarship.org/uc/item/5zr9275p) (snippet)
- The same group in *Eur Radiol* 2020 (doi:10.1007/s00330-020-06697-w; 6 swine): the AHA 17-segment model "often fails to accurately determine left and right coronary artery perfusion territories, especially in the inferior and inferoseptal walls" — [escholarship](https://escholarship.org/uc/item/5xx455gf) (snippet)
- The method is reused as the "previously validated minimum-cost path technique" to assign LAD/LCx/RCA territories in dynamic CT perfusion. In 13 swine, per-territory reproducibility was ρ = 0.87 — [PMC11324639](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11324639/) (snippet)

**Allometric / diameter scaling (no spatial map)**
- Liu J, Li B, Ma J, et al., "Effect of the ratio of vessel-specific volume to fractional myocardial mass on fractional flow reserve", *Exp Biol Med* 2021;247(18):1630–1638, doi:10.1177/15353702211027119.
  - Vessel mass fraction comes from D = A·M^(3/4) (Choy & Kassab), not from territories.
  - VR/MR = vessel lumen volume / vessel mass fraction.
  - In 205 patients / 241 vessels: VR/MR AUC 0.89 and accuracy 87%, against whole-heart V/M AUC 0.62 and accuracy 60% for FFR < 0.80.
  - [PMC9597209](https://pmc.ncbi.nlm.nih.gov/articles/PMC9597209)
- Keulards DCJ, Fournier S, van't Veer M, et al., "Computed tomographic myocardial mass compared with invasive myocardial perfusion measurement", *Heart* 2020;106:1489–1494, doi:10.1136/heartjnl-2020-316689. Stalikas cites it as the allometric/diameter approach — [Heart](https://heart.bmj.com/content/106/19/1489)

**Taylor / HeartFlow whole-heart V/M**
- Taylor et al. 2017 defined V/M as total epicardial lumen volume / LV mass, which is patient-level and not per territory. In 238 NXT patients it independently predicted FFR ≤ 0.80 — [Galway research portal](https://research.universityofgalway.ie/en/publications/cardiac-computed-tomography-derived-coronary-artery-volume-to-myo/) (snippet)

**Synthetic vascular trees / perfusion models**
- "Personalized coronary and myocardial blood flow models incorporating CT perfusion imaging and synthetic vascular trees", *npj Imaging* 2024, doi:10.1038/s44303-024-00014-6. The search snippet says it assigns LV mesh nodes to the closest outlet by Voronoi and notes that distance-to-nearest-artery and weighted-distance variants exist. Full text was blocked — [Nature](https://www.nature.com/articles/s44303-024-00014-6)
- Background from synthetic-tree work: "image resolution limits vessel segmentation to the larger epicardial vessels", which motivates growing synthetic trees into the myocardium — [Springer BMMB 2023](https://link.springer.com/article/10.1007/s10237-023-01703-8) (snippet)

**Intramural ground truth (van Horssen, Spaan / Siebes group)**
- van Horssen P et al., "Perfusion territories subtended by penetrating coronary arteries increase in size and decrease in number toward the subendocardium", *Am J Physiol Heart* 2014. Cryomicrotome imaging of 8 canine hearts showed:
  - the subendocardium has few, large (~0.5 mL) territories, each fed by its own penetrating artery
  - the subepicardium has many small territories
  - [Amsterdam UMC](https://pure.amsterdamumc.nl/en/publications/perfusion-territories-subtended-by-penetrating-coronary-arteries-/)
- Earlier FIMH 2009 methods work from the same group: intramural vessel extraction validated against fluorescent microspheres — [UMC Utrecht](https://researchinformation.umcutrecht.nl/en/publications/extraction-of-coronary-vascular-tree-and-myocardial-perfusion-dat/)

### Inferences
- For the thesis, the defensible default is **3D Euclidean nearest-voxel assignment from the LV myocardium mask to a labelled coronary lumen (or centreline) mask, aggregated to LAD / LCx / RCA**. It is the same principle as the validated commercial implementation used by Kurata and Stalikas.
- Geodesic-in-myocardium is a reasonable sensitivity analysis. It prevents "jumping" across the LV cavity or through the septum to an artery on the other side.
- The minimum-cost-path, synthetic-tree and allometric methods are more complex and less widely replicated, so they are better cited as alternatives than adopted.
- I did not find the "Malago" paper named in the brief. The closest match is **Malkasian** (Molloi group). This may be a misremembered name.

### Gaps
- No full text was retrieved for: the Molloi 2018 JCCT paper (accuracy numbers), the Harvard geodesic paper (authors), the npj Imaging 2024 paper (authors, quantitative CT-perfusion agreement), or Keulards 2020 (exact territory algorithm).
- I could not identify a "Le Huu" paper on geodesic territories. The only "Le et al." found is the porcine micro-CT proximity method cited in the TU Delft thesis.
- I found no explicit Taylor/HeartFlow publication of a *spatial* territory-partitioning algorithm. HeartFlow's published V/M is whole-heart.

---

## 2. Validation against perfusion imaging and histology; disagreement with the AHA 17-segment model

### Takeaway
Voronoi territories agree reasonably with:
- swine histology (Ide 2017)
- SPECT (Kurata 2015: r = 0.53–0.81 depending on the SPECT score)
- MR perfusion (Fukuyama 2017: r = 0.97 for ≥70% stenoses, snippet)
- invasive thermodilution flow (Keulards 2020: ICC 0.90, which may be the allometric method)

All validation cohorts are small (n ≈ 6–35). Separately, the AHA 17-segment assignment mismatches patient-specific anatomy in most patients: 72% of patients have at least one reassigned segment, about 9% of all segments. Most errors are in the inferior/inferolateral/inferoseptal RCA–LCx border zone.

### Cited Findings
- **Ide S, Sumitsuji S, Yamaguchi O, Sakata Y**, "Cardiac computed tomography-derived myocardial mass at risk using the Voronoi-based segmentation algorithm: a histological validation study", *J Cardiovasc Comput Tomogr* 2017;11:179–182, doi:10.1016/j.jcct.2017.04.007. Stalikas 2025 cites it as showing that Voronoi mass "is substantially correlated with actual vessel-specific myocardial mass measured on ex vivo swine hearts" — [Stalikas 2025](https://openaccess.sgul.ac.uk/id/eprint/118057/2/stalikas-et-al-2025-vessel-specific-myocardial-mass-in-patients-with-stable-coronary-artery-disease.pdf); [Osaka thesis summary](https://ir.library.osaka-u.ac.jp/repo/ouka/all/81894/31569_Abstract.pdf)
- **Kurata 2015** (34 CAD patients; 128-slice CTA, Tl-201 SPECT, invasive angiography): CTA-based area at risk correlated with SPECT area at risk at r = 0.531 (SSS), 0.494 (SDS) and 0.814 (SSS/SDS), all P < 0.05 — [Springer](https://link.springer.com/doi/10.1007/s00330-014-3388-2)
- **Fukuyama, Kido, Kurata et al.**, *Open J Radiol* 2017 (30 patients): Voronoi CT territory against stress MR perfusion. A snippet reports r = 0.97 for ≥70% stenoses — [ResearchGate](https://www.researchgate.net/publication/314158293_Myocardial_Segmentation_of_Area_at_Risk_Based_on_Coronary_Computed_Tomography_Angiography_and_Voronoi_Diagram_in_Comparison_with_Magnetic_Resonance_Perfusion_Imaging) (snippet; not verified in full text)
- **Keulards 2020**, *Heart* (35 patients with near-normal arteries): CT territorial mass against invasive thermodilution perfusion distribution.
  - Mean differences: LAD 5.3 ± 6.2%, LCx −2.0 ± 7.4%, RCA −3.2 ± 3.4%.
  - ICC 0.90.
  - [Heart](https://heart.bmj.com/content/106/19/1489) (snippet)
- A 2020 study comparing Voronoi area at risk with CT perfusion found that the agreement depended on stenosis severity — [PMC8983940](https://pmc.ncbi.nlm.nih.gov/articles/PMC8983940/) (snippet)
- A pig-model study in *Informatics in Medicine Unlocked* (2020) compared direct 3D Voronoi with a variant that first projects arteries onto the myocardial surface.
  - It found the **direct (non-projection) method more accurate**.
  - It notes that Voronoi territory segmentation "has been considered controversial due to lack of validation".
  - [ScienceDirect S2352914819304253](https://www.sciencedirect.com/science/article/pii/S2352914819304253); [DOAJ](https://doaj.org/article/4899bd7b52ff437e8d5ef512d8f5e00b) (snippet)
- **AHA 17-segment model against patient anatomy.** Javadi MS, Lautamäki R, Merrill J, et al., Bengel FM, "Definition of vascular territories on myocardial perfusion images by integration with true coronary anatomy: a hybrid PET/CT analysis", *J Nucl Med* 2010;51(2):198–203, doi:10.2967/jnumed.109.067488:
  - 71 patients.
  - 72% (51/71) had at least one segment that differed from the standard assignment; 112/1,207 segments (~9%) were reassigned.
  - Of the reassigned segments: 39% were RCA→LCx, 30% LCx→LAD, 12% LAD→LCx and 11% LAD→RCA.
  - In 6 dogs, agreement against dye staining was κ = 0.80.
  - Reassignment improved separation of defect from remote territory (0.75 ± 0.13 vs 0.81 ± 0.12, P = 0.0014).
  - [JNM](https://jnm.snmjournals.org/content/51/2/198)
- In swine, the Molloi group (Eur Radiol 2020) found the AHA model "often fails", especially in the inferior and inferoseptal walls — [escholarship](https://escholarship.org/uc/item/5xx455gf) (snippet)
- Termeer et al. note that "several studies have confirmed the inaccuracy" of the population-average AHA mapping because of anatomical variation — [PMC7860735](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7860735/)

### Inferences
- The AHA 17-segment model with dominance rules is a **weak fallback** for per-artery mass. Errors concentrate in exactly the segments that decide LCx vs RCA mass. For a thesis that fits separate LCx and RCA models, AHA-based mass would add the most error in the very denominators being compared.
- Validation of Voronoi territories is mostly about *area at risk distal to a stenosis* or *whole-vessel fractions* in proximal vessels. It supports whole-artery (LAD / LCx / RCA) mass better than fine side-branch mass, which suits the thesis's trunk-level design.
- No validation exists in a screening/general-population cohort like CGPS. Stalikas notes that Voronoi is not validated after MI or in chronic total occlusion.

### Gaps
- Ide 2017 correlation coefficients were not retrieved (paywalled).
- No PET- or microsphere-based validation of *Euclidean Voronoi* in humans was found. Microsphere validation exists for Molloi's minimum-cost-path in swine.
- I found no head-to-head comparison of Euclidean vs geodesic territories against a perfusion reference in humans.

---

## 3. Practical details: vessel inclusion, truncation, dominance, ramus/LM, centrelines vs lumen, 3D vs surface, septum

### Takeaway
The reference implementation:
- uses **all branches > 1.5 mm diameter**
- seeds at each ostium
- assigns each voxel to the nearest *lumen voxel* in 3D
- defines dominance by PDA origin
- assigns the PDA/PLB territory to the LCx in left dominance

Truncation of side branches biases territories toward vessels that are segmented further. Septal perforators are a known blind spot unless they are segmented (Stalikas did segment 1,208 septals). RV myocardium is excluded, which under-states RCA supply.

### Cited Findings
- **Diameter cutoff:** "The software recognizes all side branches with a diameter > 1.5 mm" — [Stalikas 2025](https://openaccess.sgul.ac.uk/id/eprint/118057/2/stalikas-et-al-2025-vessel-specific-myocardial-mass-in-patients-with-stable-coronary-artery-disease.pdf)
- **Branches included (Stalikas):** 948 LAD, 948 LCx and 871 RCA, plus 1,888 diagonals, 1,208 septals, 1,422 OMs, 247 ramus intermedius, 850 PDA and 846 PLB — [Stalikas 2025](https://openaccess.sgul.ac.uk/id/eprint/118057/2/stalikas-et-al-2025-vessel-specific-myocardial-mass-in-patients-with-stable-coronary-artery-disease.pdf)
  - The ramus is handled as its own branch, present in 247/948 ≈ 26% of patients.
  - LM is not given a separate territory; seeds are at the LAD and LCx ostia.
- **Dominance handling:** dominance was defined by PDA origin.
  - PDA mass = all side branches in the posterior interventricular groove distal to the crux.
  - PLB mass = all side branches from the distal RCA from the crux.
  - "In cases of left coronary dominance, the mass supplied by the PDA included the most distal side branch of the dominant LCX."
  - Left dominance occurred in 11%. In left dominance, LCx mass was 47.5% [39.4–52.6] against 27.7% in right dominance, and "RCA did not subtend any part of LV mass in 77 of 103 patients with left dominance".
  - [Stalikas 2025](https://openaccess.sgul.ac.uk/id/eprint/118057/2/stalikas-et-al-2025-vessel-specific-myocardial-mass-in-patients-with-stable-coronary-artery-disease.pdf)
- **Reference fractions (n = 948):**
  - Median LV mass 141 g (IQR 118–166); women 106 g, men 150 g.
  - LAD 42.5% [37.9–48.1], LCx 28.8% (IQR printed with an error as "21.9–5.7" in the source), RCA 26.4% [20.9–31.9].
  - First septal 8.9%, first diagonal 7.9%, first OM 10.2%.
  - [Stalikas 2025](https://openaccess.sgul.ac.uk/id/eprint/118057/2/stalikas-et-al-2025-vessel-specific-myocardial-mass-in-patients-with-stable-coronary-artery-disease.pdf)
- **Septum:** septal branches together subtended a median of 10.2% [6.6–12.9] of LV mass, and 38% of first septals subtended > 10% — [Stalikas 2025](https://openaccess.sgul.ac.uk/id/eprint/118057/2/stalikas-et-al-2025-vessel-specific-myocardial-mass-in-patients-with-stable-coronary-artery-disease.pdf)
- **RV excluded:** "the software does not account for the right ventricular mass, which could lead to an underestimation of the myocardial mass subtended by the RCA" — [Stalikas 2025](https://openaccess.sgul.ac.uk/id/eprint/118057/2/stalikas-et-al-2025-vessel-specific-myocardial-mass-in-patients-with-stable-coronary-artery-disease.pdf)
- **Lumen voxels rather than centreline:** "assigns each voxel of the LV volume to the nearest voxel of an adjacent coronary artery" — [Stalikas 2025](https://openaccess.sgul.ac.uk/id/eprint/118057/2/stalikas-et-al-2025-vessel-specific-myocardial-mass-in-patients-with-stable-coronary-artery-disease.pdf)
  - Termeer used centrelines projected to the epicardium instead — [PMC7860735](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7860735/)
- **3D against surface projection:** in pigs, direct 3D Voronoi was more accurate than projecting arteries onto the surface — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2352914819304253) (snippet)
- **Truncation / unseen branches:**
  - Hsieh 2021 notes that small side branches invisible on CCTA are neglected and compensates with Murray's law for flow splitting — [PMC8257574](https://pmc.ncbi.nlm.nih.gov/articles/PMC8257574/)
  - Liu 2021 notes that excluding vessels < 1 mm may add error to allometric mass — [PMC9597209](https://pmc.ncbi.nlm.nih.gov/articles/PMC9597209)
  - Termeer reported LAD over-segmentation at the apex inflating the LAD territory — [Termeer poster](https://www.cg.tuwien.ac.at/research/publications/2009/termeer-2009-scmr/termeer-2009-scmr-poster.pdf)
- **Neighbour interaction ignored:** a 2022 CT-perfusion territory study lists as a limitation that "the impact of a neighbouring coronary vessel on a specific myocardial territory was not included" — [PMC11973961](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973961/) (snippet)

### Inferences (ad hoc recommendations for the thesis, not established)
- **Main risk: the ImageCAS-style lumen model under-segments distal vessels unevenly across LAD, LCx and RCA.** In Voronoi this moves boundary myocardium to whichever artery is segmented further. Mitigations:
  - (a) Prune all trees to a common minimum diameter, for example 1.5 mm, to match Stalikas.
  - (b) Report territory fractions alongside Stalikas reference values (LAD ~42%, LCx ~29%, RCA ~26%) as a sanity check.
  - (c) Run a sensitivity analysis at 1.0 / 1.5 / 2.0 mm cutoffs.
- **Septum:** ImageCAS-style models rarely capture septal perforators. Without them, Euclidean distance assigns the septum to whichever of LAD or PDA is closer, which is roughly anatomically right (anterior 2/3 to the LAD, inferior 1/3 to the PDA). It can, however, shortcut through the cavity. Geodesic distance restricted to the myocardium mask, for example a fast-marching method, is a cheap guard.
- **Use lumen voxels (or the lumen surface), not centrelines,** to match the validated implementation. Centrelines change distances only by about a vessel radius, so the difference is minor.
- **Labelling the tree into LAD / LCx / RCA is a prerequisite.** Voronoi gives "nearest coronary voxel", and each voxel then needs an artery label. With the thesis's per-artery outcome design, use the same LAD / LCx / RCA labels for both lumen volume (numerator) and territory (denominator).
- **Ramus intermedius:** decide a priori whether it goes to LCx, to LAD or is excluded, and apply the same rule to the lumen volume. **LM:** exclude it from both numerator and denominator, or split it. Stalikas seeds at LAD/LCx ostia.
- **Dominance:** in left-dominant patients the RCA LV territory can be near zero (77/103 in Stalikas). An RCA V/M ratio then becomes unstable or undefined. Consider excluding left-dominant patients from the RCA model, or using a minimum territory mass. The CGPS BL/FU headers include a dominance variable (`ct_cag` dominance) to cross-check the CT-derived dominance.

### Gaps
- No published quantitative study was found on how distal truncation depth changes Voronoi territory mass. This is a methodological gap that the thesis could address with its own sensitivity analysis.
- I found no published rule for the ramus or LM beyond Stalikas's branch-level treatment.

---

## 4. Sensitivity to segmentation quality; reproducibility

### Takeaway
I found **no published inter-observer or test-retest reproducibility figures specifically for Voronoi territory mass**. The available evidence covers adjacent questions: reproducibility of territory-based CT perfusion in swine (ρ = 0.87 per territory) and qualitative failure cases from over- or under-segmentation.

### Cited Findings
- Using minimum-cost-path territories, per-territory MBF reproducibility was ρ = 0.87 and whole-myocardium ρ = 0.96 in 13 swine. This measures perfusion reproducibility, not territory-mass reproducibility — [PMC11324639](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11324639/) (snippet)
- A TU Delft thesis assessed inter-observer reproducibility of coronary-seed and region annotations for a Voronoi-style approach; the results were not visible in the snippet — [TU Delft](https://repository.tudelft.nl/file/File_85d3c3c5-427f-4574-88e6-ba8298f6e2da?preview=1)
- The over-segmentation failure case: the LAD territory was too large because of apical over-segmentation — [Termeer poster](https://www.cg.tuwien.ac.at/research/publications/2009/termeer-2009-scmr/termeer-2009-scmr-poster.pdf)
- Stalikas notes Voronoi is not validated in CTO or post-MI patients; their pooled data excluded poor CCTA image quality — [Stalikas 2025](https://openaccess.sgul.ac.uk/id/eprint/118057/2/stalikas-et-al-2025-vessel-specific-myocardial-mass-in-patients-with-stable-coronary-artery-disease.pdf)

### Inferences
- The thesis should quantify sensitivity itself, for example territory mass under (i) diameter pruning thresholds, (ii) Euclidean vs geodesic distance, and (iii) a perturbed or alternative lumen segmentation. It should report the coefficient of variation or ICC of territory fractions.
- Whole-LV mass from TotalSegmentator-type models is likely more robust than the partition boundaries. The fractions depend mainly on how far each artery's tree is segmented.

### Gaps
- No inter-observer or test-retest data for Voronoi territory mass in humans.
- No study was found on how deep-learning coronary segmentation errors propagate to territory mass.

---

## 5. Open-source code and tools

### Takeaway
I found **no dedicated, maintained open-source coronary-territory partitioning tool**. The validated implementation is commercial (Fujifilm Synapse Vincent). Open toolkits (VMTK, 3D Slicer) provide the building blocks but no turnkey territory module.

### Cited Findings
- Stalikas et al. used Synapse Vincent v5 (Fujifilm) and state that "no analytic code was used beyond standard R functions" — [Stalikas 2025](https://openaccess.sgul.ac.uk/id/eprint/118057/2/stalikas-et-al-2025-vessel-specific-myocardial-mass-in-patients-with-stable-coronary-artery-disease.pdf)
- VMTK (github.com/vmtk/vmtk) is a Python-wrapped C++ toolkit for vascular segmentation, centrelines, geometry and network analysis, usable standalone or as a 3D Slicer extension. It has no territory function — [VMTK JOSS paper](https://github.com/vmtk/vmtk/blob/master/doc/joss-paper/paper.md)
- A targeted search for GitHub repositories combining coronary territories, Voronoi and VMTK returned nothing relevant — [search summary; VMTK fork](https://github.com/romangrothausmann/vmtk)

### Inferences (implementation sketch; ad hoc)
- Euclidean Voronoi is a few lines of code. Run `scipy.ndimage.distance_transform_edt(~vessel_mask, return_indices=True)` on the labelled coronary mask, read the artery label at the nearest index for each LV-myocardium voxel, then sum voxel volume × 1.05 g/cm³ per label.
- For a geodesic variant, run fast marching (for example `scikit-fmm`) or a multi-source Dijkstra restricted to myocardium ∪ vessel voxels, using one front per artery.
- Centreline extraction and branch labelling can use VMTK or skeletonisation (`skimage.morphology.skeletonize`).

### Gaps
- No public reference implementation exists to benchmark against. GitHub was not exhaustively searched (only one targeted query).
