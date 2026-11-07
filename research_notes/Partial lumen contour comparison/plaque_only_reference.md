# Validating CCTA lumen extraction on plaque-only reference segments when the target cohort is plaque-free

Scope: what the literature says about how CCTA lumen segmentation accuracy differs between diseased and non-diseased segments, how QAngio CT (Medis) lumen agrees with invasive references, and how validation studies handle a reference that only exists in diseased segments. All numbers below were read from the source unless marked "snippet only".

## Q1. Do lumen segmentation errors in CCTA differ between normal and diseased (stenotic or calcified) segments? Direction and size?

### Takeaway
The best benchmark (Kirisli 2013, Rotterdam framework) reports lumen results separately for "healthy" and "diseased" segments. The gap is small and runs in different directions for different metrics: Dice is a few points lower in diseased segments, but mean and maximum surface distance are, if anything, lower there. The authors attribute this to the smaller scale of diseased lumens, not to better accuracy. Against IVUS, CT lumen errors depend on lumen size and calcium. The literature does not clearly support either "diseased is harder" or "diseased is easier" for lumen boundaries in general. It does show that the error mechanisms differ (blooming and plaque–lumen contrast in disease; partial volume in small lumens).

### Cited Findings
- **Kirisli et al. 2013, Med Image Anal 17(8):859–876** (Rotterdam Coronary Artery Stenoses Detection and Quantification Evaluation Framework). The setup: 48 multicentre, multivendor CTA datasets, 18 for training and 30 for testing. Lumen segmentation was evaluated against the manual annotations of 3 observers, with Dice, mean surface distance (MSD) and maximum distance (MaxD) — [Kirisli PhD thesis, Erasmus MC 2013, ch. 4 (same framework)](https://repub.eur.nl/pub/40314/130614_Kirisli,%20Hortensa%20Ayla.pdf); [Repub abstract](https://repub.eur.nl/pub/41673)
- **Definition matters:** in that framework, "diseased segments are segments presenting in CTA consensus with at least one significant stenosis (≥50%). Healthy segments are segments ... with no significant stenosis (≤50%). Occluded segments were excluded." So "healthy" means *non-obstructive*, not *plaque-free*: it can contain plaque below 50%. The framework ranking weighs healthy and diseased segments separately — [Kirisli thesis, Fig. 4.6 and §4.3.6](https://repub.eur.nl/pub/40314/130614_Kirisli,%20Hortensa%20Ayla.pdf)
- **Testing-set lumen results (30 datasets), diseased vs healthy:**
  - Observer 3: Dice 79 vs 81 %, MSD 0.23 vs 0.21 mm, MaxD 3.00 vs 3.45 mm.
  - Observer 1: Dice 76 vs 77 %, MSD 0.24 vs 0.24 mm.
  - Observer 2: Dice 65 vs 72 %, MSD 0.34 vs 0.27 mm.
  - Mohr et al. (best automatic method): Dice 70 vs 73 %, MSD 0.40 vs 0.39 mm, MaxD 2.68 vs 2.75 mm.
  - Wang et al.: Dice 69 vs 69 %, MSD 0.45 vs 0.50 mm.
  - Broersen et al.: Dice 67 vs 69 %, MSD 0.50 vs 0.70 mm.
  - Shahzad et al.: Dice 58 vs 66 %.

  — [Kirisli thesis, Table 4.11](https://repub.eur.nl/pub/40314/130614_Kirisli,%20Hortensa%20Ayla.pdf)
- The authors' reading of these results: "though the Dice value obtained on healthy vessel segments is higher than the one obtained on diseased ones, the mean square distance and maximum distance obtained on healthy segments is higher than the ones obtained on diseased ones, which may be caused by the smaller scale of the diseased vessel." — [Kirisli thesis §4.5.3](https://repub.eur.nl/pub/40314/130614_Kirisli,%20Hortensa%20Ayla.pdf)
- **Failure modes in diseased segments:** on a severe mixed plaque (LAD7, dataset #08), two algorithms failed. One included the calcified part of the lesion in the lumen; the other was "attracted towards the calcium spot". Others under-segmented the soft plaque — [Kirisli thesis §4.5.3](https://repub.eur.nl/pub/40314/130614_Kirisli,%20Hortensa%20Ayla.pdf)
- **Reference uncertainty in disease:** observers disagreed on lesion extent ("One observer may indicate that a whole segment is diseased ... while another may indicate multiple smaller stenoses"). Inter-observer Dice ranged 65–79 % in diseased segments and 72–81 % in healthy segments. — [Kirisli thesis §4.6 and Table 4.11](https://repub.eur.nl/pub/40314/130614_Kirisli,%20Hortensa%20Ayla.pdf)
- **Lugauer et al. 2014 (MICCAI)**, on the same framework (testing/training):
  - Their method: Dice D 76/75 % vs H 75/77 %; MSD D 0.32/0.27 mm vs H 0.51/0.32 mm.
  - The healthy-segment MSD/MaxD were worsened by "a labeling mismatch between our applied CTL tracing and the reference" (only LM, LAD, RCA, LCX were compared).
  - They note that earlier methods "tend to focus on healthy vessels and often fail to correctly segment the lumen in diseased vessels, i.e. in the presence of calcified, non-calcified and mixed plaques".

  — [Lugauer et al. 2014 PDF](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf)
- **Freiman et al.** (arXiv 1906.09763; to my knowledge published in Med Phys, venue not verified here). On the 18 training cases and 78 segments, Dice was H 0.69 vs D 0.74 and MSD H 0.50 vs D 0.28 mm, a pattern similar to Kirisli. They state that the scanner point-spread function "may lead to an overestimation of lumen area in vessels with small lumen diameter which is known as the partial-volume effect (PVE)" — [Freiman et al., arXiv](https://arxiv.org/pdf/1906.09763)
- **Noll et al. 2013 (CT vs IVUS, calcified lesions):**
  - Sample: 60 patients, 252 calcified cross-sections, 2×64-slice CT, semi-automated SurePlaque software.
  - CT lumen area was 6.4±3.4 vs 7.0±3.7 mm² on IVUS (p<0.001). Minimum lumen diameter was 2.3 vs 2.6 mm. CT underestimated calcium arc (max arc 52° vs 83°).
  - CT missed lumen-contacting calcium in 11 %.
  - By IVUS lumen tertile, lumen area did not differ in the smallest tertile (p=0.264) but was underestimated in the 2nd and 3rd tertiles.
  - The authors attribute the low accuracy to "high variance and not to systematic error", with scatter above 70 % for lumen area in the smallest lumens.

  — [Noll et al., PMC3915947](https://pmc.ncbi.nlm.nih.gov/articles/PMC3915947)
- A related analysis found that total calcium arc ≥47° combined with mean lumen diameter ≤2.8 mm best predicted excessive lumen underestimation by CTA (snippet only; full text not read) — [PubMed 24290567](https://pubmed.ncbi.nlm.nih.gov/24290567)
- **Falcão et al. 2015 (Arq Bras Cardiol):**
  - Sample: 21 patients, 167 segments, 64-slice CT, Vitrea/SurePlaque.
  - CT tended to underestimate lumen size with wide dispersion.
  - Per-segment mean lumen area difference (CT−IVUS) was −1.1±2.3 mm² where IVUS plaque burden was <40 % (n=95), against −0.1±1.8 mm² where it was >40 % (n=72).
  - Agreement "was not substantially affected by the presence or absence of an underlying plaque". The absolute difference "tended to be larger among coronary segments without atherosclerotic plaque".
  - Limitations: small sample, CACS >600 excluded, non-independent measurements.

  — [Falcão et al. 2015, SciELO](https://scielo.br/j/abc/a/mcMsDcm8xntCkcnR7BJRmxc/?lang=en)
- **Blooming and other calcium artefacts:**
  - Calcium causes blooming, beam-hardening and photon-starvation artefacts at CCTA — [Radiology: Cardiothoracic Imaging 2025 review (snippet only)](https://pubs.rsna.org/doi/epdf/10.1148/ryct.240494)
  - In a photon-counting phantom study, blooming overestimated a 50 % stenosis as 82.7 % at 40 keV and 52.1 % at 140 keV (snippet only) — [Lübeck research portal](https://research.uni-luebeck.de/en/publications/photon-counting-detector-ct-virtual-monoenergetic-images-for-coro/)
  - The Kirisli thesis notes that stenosis degree "is generally over-estimated in CTA as compared to QCA (calcified lesions, due to blooming artifact)" — [Kirisli thesis §4.5.1](https://repub.eur.nl/pub/40314/130614_Kirisli,%20Hortensa%20Ayla.pdf)
- **The invasive reference is also imperfect in calcium.** An autopsy study found that IVUS underestimated calcified plaque cross-sectional area by 39 % (snippet only) — [em-consulte](https://em-consulte.com/article/604550/calcified-plaque-cross-sectional-area-in-human-art)

### Inferences
- Agreement measured in diseased segments is not an upper or lower bound on agreement in plaque-free segments. The published contrasts are small (a few Dice points, tenths of a mm in MSD) and change sign by metric.
- Size-dependent metrics such as Dice, and absolute distances, are confounded by lumen calibre. Diseased lumens are smaller, which lowers Dice for a fixed boundary error and lowers mm-distances for a fixed relative error. A plaque-only comparison should report scale-aware metrics, such as signed radius or area difference relative to the reference radius, or stratify by reference diameter.
- In plaque-free segments, error mechanisms specific to plaque (blooming, a soft-plaque/lumen boundary, a lesion that pulls the contour) are absent. Mechanisms that apply to all segments (partial volume in small distal lumens, noise, motion, side-branch leakage, centerline mismatch) remain. A plaque-only comparison therefore tests the tracer under the specific plaque challenges that plaque-free baselines will not present. It under-samples the generic challenges that dominate there, such as small distal calibre and branch ostia.
- "Healthy" in the Kirisli benchmark is <50 % stenosis, not plaque-free. No benchmark found here reports lumen accuracy specifically in plaque-free coronaries.

### Gaps
- No study found that reports CCTA lumen segmentation accuracy in strictly plaque-free segments against an independent reference.
- I did not read the Med Image Anal journal version of Kirisli 2013. The thesis chapter is the same framework, and its table is quoted. Later submissions on the challenge website were not checked.
- No source gave lumen diameter error as a function of vessel calibre across normal segments in vivo. Partial-volume overestimation in small lumens is asserted mechanistically (Freiman) and in phantoms, not quantified here in patients.

## Q2. Does Medis (QAngio CT) lumen agreement with IVUS/QCA differ by plaque type or stenosis?

### Takeaway
QAngio CT validation papers (Boogers 2010 against QCA, Boogers 2012 against IVUS, de Graaf 2013 against IVUS-VH) evaluated lesions in patients with coronary disease. The abstract-level data report good correlation at the minimal lumen area. I found no QAngio CT paper that reports lumen agreement stratified by plaque type or for non-diseased segments. The Medis reference itself is therefore validated mainly at lesions.

### Cited Findings
- **Boogers et al. 2012, Eur Heart J 33(8):1007–1016:**
  - QAngio CT against IVUS, fused with a 3D registration algorithm, in 51 patients, 103 arteries and 146 lesions.
  - Minimal lumen area r=0.75, lumen area stenosis r=0.79 and plaque burden r=0.70 at the MLA. Mean plaque burden r=0.64 and remodelling index r=0.56 over the lesion.
  - Read from abstract-level snippets only; full text and plaque-type subgroups not read.

  — [Repub record](https://repub.eur.nl/pub/64020); [Leiden repository](https://scholarlypublications.universiteitleiden.nl/handle/1887/120260)
- **Boogers et al. 2010, JACC Cardiovasc Imaging:** automated 64-slice CT stenosis quantification against QCA in 100 patients. Diameter stenosis r=0.83 per vessel and r=0.86 per patient. Snippet only — [Leiden repository](https://scholarlypublications.universiteitleiden.nl/handle/1887/109206)
- **de Graaf et al. 2013, Int J Cardiovasc Imaging 29:1177–1190:** QAngio CT (Research Edition 1.3.6) stenosis and plaque composition against IVUS virtual histology in 57 patients, with HU-threshold plaque categories. The lumen-area results by plaque type could not be retrieved (the PDF download failed) — [Leiden thesis chapter](https://scholarlypublications.universiteitleiden.nl/access/item%3A2919534/view)
- **QAngio scan–rescan reproducibility (RSNA 2014 abstract):**
  - Total plaque intra-observer ICC was 0.84, and total plaque indexed by length had an inter-observer ICC of 0.94.
  - Noncalcified subtypes were less reproducible (ICC 0.74–0.78).
  - No lumen-specific or normal-segment figures were given.

  — [RSNA archive](https://archive.rsna.org/2014/14017720.html)

### Inferences
- The Medis lumen contours are a reader-supervised semi-automatic reference whose own validation was at lesions. Any tracer–Medis disagreement in plaque stretches mixes tracer error with Medis error (and reader correction), especially at calcium, where QAngio also uses HU thresholds. Describe it as *agreement with a reference*, not as accuracy.
- In this thesis's data, Medis contours exist only for diseased segments, presumably because the plaque analysis was the readers' aim. Their placement is therefore tied to the lesion (start and end set around plaque). The compared stretch is likely enriched for exactly the cross-sections where CT lumen measurement is least reliable.

### Gaps
- I did not find QAngio CT lumen agreement stratified by calcified, non-calcified or mixed plaque, or by stenosis grade. The full texts of Boogers 2012 and de Graaf 2013 would need checking.
- I did not find any QAngio CT lumen validation in normal segments.

## Q3. How do validation papers handle a reference available only in diseased segments (stratification, caveats, transfer arguments)?

### Takeaway
The standard practice in the main benchmark is to stratify (diseased vs non-diseased, reported and ranked separately) rather than to transfer. I found no published argument that agreement in diseased segments transfers to normal segments. Clinical CT–IVUS papers state the limited population as a limitation, for example "relatively high risk profile ... limits extrapolation".

### Cited Findings
- The Rotterdam framework reports and ranks lumen metrics separately for diseased and healthy segments. A patient's diseased-segment ranks count only when that patient has diseased segments (weight ω_p) — [Kirisli thesis §4.3.6](https://repub.eur.nl/pub/40314/130614_Kirisli,%20Hortensa%20Ayla.pdf)
- Follow-on methods papers (Lugauer 2014, Freiman) keep this H/D split in their tables — [Lugauer 2014](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf); [Freiman, arXiv](https://arxiv.org/pdf/1906.09763)
- Falcão et al. stratify segments by IVUS plaque burden (<40 % vs >40 %). They caveat that their "relatively high risk profile" population "limits extrapolation", and that excluding CACS >600 may have inflated agreement — [Falcão et al. 2015](https://scielo.br/j/abc/a/mcMsDcm8xntCkcnR7BJRmxc/?lang=en)
- Noll et al. stratify by lumen size and calcium arc tertiles rather than pooling — [Noll et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC3915947)

### Inferences
- An honest framing for the thesis:
  - The comparison measures tracer–Medis lumen agreement over diseased stretches of baseline scans from people with plaque.
  - It supports a claim that the tracer finds the lumen boundary in the presence of plaque about as Medis does.
  - It does not directly measure accuracy in plaque-free segments of the prediction cohort, which differ in lumen size, in the absence of calcium and in where along the tree the stretch lies.
- A transfer argument can only be partial and must be stated as an assumption. In plaque-free segments the plaque-specific errors are removed, while partial volume in small lumens and branch handling remain. The published H/D contrasts are small, so a large shift in the direction of the error is not expected, but nothing measured here supports that.
- Mitigations that the literature's practice suggests:
  - stratify agreement by plaque type and stenosis grade from the BL read (`_plaque_type`, `_stenosis`) and by reference diameter;
  - report signed bias as well as absolute error;
  - report how many cross-sections are minimal or mild plaque, which come closest to the plaque-free target;
  - report the centerline-only (full-tree) Medis comparison as the part that covers non-diseased vessel, since the BL trees are not limited to diseased segments.
- Cohort shift beyond the segment level: the people with Medis contours had plaque at baseline and probably differ from the plaque-free cohort in age, calcium and image quality. That is a second reason the agreement may not transfer, separate from segment-level disease.

### Gaps
- I found no methodological paper that discusses formally transferring lumen-segmentation validation from diseased to normal segments (spectrum effects in segmentation validation). This is a recognised idea in diagnostic accuracy work, but no segmentation-specific source was located.
