# Methods for describing and clustering arterial tree shape, and how clusters have been validated

Scope note: about 20 search/fetch calls. Several primary full texts could not be fetched: Springer and PMC pages redirect or show a bot check, and the Project Euclid PDF came back empty. Where I could see only an abstract, I say so. Claims I could not verify from a source are listed under Gaps, not under findings.

## 1. Statistical shape models and coronary atlases from CCTA (Medrano-Gracia, Young/Cowan, Beier)

### Takeaway
The main CCTA coronary atlas work (Auckland/UNSW) used 300 and 211 plaque-free, zero-calcium patients. The shape scores mainly track **vessel size and bifurcation angle, which differ by sex**. Shape was **not associated with hypertension, smoking or diabetes**. No published clinical correlate of these modes predicts plaque. That fits the user's feature set: size (diameter ratios) and LM angle are the main axes of variation in plaque-free people.

### Cited Findings
- **Medrano-Gracia et al. 2016, EuroIntervention 12:845–854, "A computational atlas of normal coronary artery anatomy":**
  - **Cohort and acquisition:** 300 adults with calcium score 0 and no stenosis on CCTA; 64% women. Imaged at end-diastole (75% R-R). Seven meshes were excluded for poor quality, mostly small female hearts. Centreline and lumen models were made.
  - **Measures:** 3D bifurcation angles averaged over a 5–10 mm depth, inflow angle, effective diameter from lumen area every 0.5 mm, and arc length.
  - **LM:** diameter 3.5 ± 0.8 mm, length 10.5 ± 5.3 mm. LM bifurcation angle 89 ± 21° with an intermediate artery and 75 ± 23° without (p<0.001). The LM angle is about 30° wider than at other bifurcations (about 50°).
  - **Sex:** the LM bifurcation angle is wider in men (85° vs 74°, p<0.001) and still differs after adjusting for height (p=0.002).
  - **Other associations:** diameters were not related to BMI.
  - **Diameter law:** Finet ratio 0.658 ± 0.083. The fitted diameter exponent α = 2.4 is closest to Huo–Kassab, not Murray.
  - **Normalisation:** none to BSA; only regression adjustment for height and BMI.
  - **Shape analysis:** no PCA or clustering in this paper.
  - [EuroIntervention](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)
- **Medrano-Gracia et al. 2017, J Cardiovasc Transl Res 10:82–90, "A study of coronary bifurcation shape in a normal population"** (PMC5323506):
  - **Cohort:** 211 patients with zero calcium, no stenosis and no intermediate artery. Statistical shape models (PCA) of **446 major bifurcations**.
  - **Shape differences:** LM bifurcations differed from the others in size and bifurcation angle, and RCA crux bifurcations in inlet and curvature angles. Size and bifurcation angle differed by sex.
  - **Risk factors:** hypertension, smoking and diabetes had no clear association with shape.
  - **Diameter law:** Huo–Kassab fit best.
  - **Caveat:** abstract only; I could not get the per-mode variance or the number of modes. [Springer](https://link.springer.com/article/10.1007/s12265-016-9720-2); [Europe PMC record](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1007/s12265-016-9720-2&resultType=core&format=json)
- **MICCAI 2014 conference version** (Medrano-Gracia et al., LNCS chapter) — [Springer](https://link.springer.com/chapter/10.1007/978-3-319-10470-6_64). Details not retrieved.
- **The UNSW group (Beier) and later work:** the group describes its project as "the largest coronary artery population vessel shape and flow database to date", aimed at ML risk stratification. Companion work: Beier et al. 2016, J Biomech 49:1570–1582, on bifurcation angle and haemodynamics. [UNSW Coronary Atlas](https://www.unsw.edu.au/research/svmg/research/coronary-atlas)
- **Zhang, Gharleghi, Shen, Beier 2023 (arXiv preprint, not peer reviewed):**
  - **Data:** 39 public left coronary trees (ASOCA): 20 non-stenosed, 12 moderate, 7 severe.
  - **Curvature:** average curvature differed between non-stenosed and stenosed trees (p=0.024), and in non-bifurcating segments (p=0.027).
  - **Interpretation:** the authors suggest curvature matters for plaque *onset* and low TAESS/RRT for progression. This is cross-sectional, tiny and not a shape model. [arXiv 2312.00257](https://arxiv.org/abs/2312.00257)
- **PCA shape model of diseased LADs** (Politecnico di Torino thesis plus a conference abstract; grey literature): 233 LADs from 3D QCA, not CCTA. 14 modes explained 90% of the variance and 22 explained 95%. The abstract reports 19 modes for 95%. That count differs from the thesis, perhaps because it is a different cohort or version. [PoliTo thesis](https://webthesis.biblio.polito.it/34856)
- **Review of cardiovascular SSM** (Sharp, Betts, Banerjee): PCA is the most common SSM method. [ORA Oxford](https://ora.ox.ac.uk/objects/uuid:e5654160-0e60-457d-9bc2-1ddcd149f304)

### Inferences
- **Who these cohorts were:** both atlas cohorts are plaque-free or zero-CAC, which matches the user's ~1,200 clean baselines. Neither has follow-up, so no prior work tests whether atlas shape modes predict *incident* plaque. The user's who/where design would be new evidence, not a replication.
- **What the modes mostly hold:** the PCA modes mostly hold size, LM angle, and RCA inlet/curvature. The user's four scalar features already cover diameter ratios, LM angle and curvature. A full PCA shape model would mostly re-express these plus size, which is largely nuisance tied to sex and body size.
- **Measurement conventions:** the angle definitions differ between atlases: in-plane vs 3D, and averaged over a 5–10 mm depth. To compare with Medrano-Gracia, the user's LM angle definition should state its depth interval and cardiac phase.
- **Feasibility:** all of this needs only centerlines and lumen area per step, no CFD.

### Gaps
- Per-mode variance and loadings, and the size of the sex effect per mode, for Medrano-Gracia 2017. The full text was not retrieved; Springer/PMC were blocked.
- I found no large CCTA statistical shape model of the *whole* coronary tree (as opposed to bifurcations) with longitudinal plaque outcomes.
- The 2025 IEEE paper by Gharleghi/Beier on sex-specific LM bifurcation variation was seen in a listing but not checked. [dblp](https://dblp.dagstuhl.de/pid/251/2682.html)

## 2. Functional data analysis and elastic shape analysis of centerlines

### Takeaway
The AneuRisk project (Sangalli, Secchi, Vantini, Veneziani) is the reference for treating centerline **radius and curvature profiles as functions**:
1. register them (alignment),
2. reduce with fPCA,
3. then classify or cluster.

It used **65 patients**, and the geometry of the distal 3 cm told aneurysm-location groups apart. SRVF/elastic methods exist for curves and trees, but I found no coronary-tree application. All of these methods work on centerline plus radius data.

### Cited Findings
- **Sangalli et al. 2009, JASA 104(485):37–48, "A case study in exploratory functional data analysis: geometrical features of the internal carotid artery":**
  - **Data:** 65 AneuRisk patients. The ICA radius and centerline curvature profiles were registered, then reduced with fPCA, then classified with QDA on the PC scores.
  - **Result:** the last 3 cm of the ICA differ in geometry for patients with an aneurysm at or after the terminal bifurcation. That group has *lower* variability in radius and curvature.
  - [PDF](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf); [MOX](https://mox.polimi.it/reports-and-books/publication-results/?id=150)
- **Centerline estimation:** a companion paper, Sangalli et al. 2009, JRSS-C, covers efficient estimation of 3D centerlines and curvature. [PDF](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JRSSC_compresso.pdf)
- **k-mean alignment:**
  - **Method:** Sangalli, Secchi, Vantini, Vitelli 2010, Comput Stat Data Anal 54. It jointly aligns curves (separating phase from amplitude variation) and clusters them into k groups, separating within-cluster from between-cluster amplitude variation.
  - **AneuRisk65 application:** EJS 2014, 8:1891–1904.
  - [MOX report](https://www.mate.polimi.it/biblioteca/add/qmox/45-2013.pdf); [EJS](https://projecteuclid.org/journals/electronic-journal-of-statistics/volume-8/issue-2/Analysis-of-AneuRisk65-data-k-mean-alignment/10.1214/14-EJS938A.pdf); [MOX AneuRisk page](https://mox.polimi.it/research-areas/statistics/research/high-dimensional-complex-data-functional-spatial-and-object-data/aneurisk)
- **AneuRisk65 as a benchmark:**
  - It became a benchmark for functional data analysis. In the 2014 EJS special issue, groups compared methods, including elastic/SRVF carotid shape analysis treating curves via 3D coordinates, radii and curvature. They differed in the warping allowed (shift only, linear, or flexible).
  - A later classifier on the radius curves (33 upper vs 32 lower/healthy) had **32.3% misclassification**. The geometric signal is real but modest.
  - [EJS rejoinder](https://re.public.polimi.it/retrieve/e0c31c08-fc9c-4599-e053-1705fe0aef77/2014_Sangalli-Secchi-Vantini_EJS_AneuRisk65_rejoinder.pdf); [Project Euclid](https://projecteuclid.org/euclid.ejs/1414588180); [arXiv 1708.08257](https://arxiv.org/pdf/1708.08257)
- **Elastic shape analysis of trees:** an extended SRVF for tree-like 3D objects puts each branch in an L² metric that captures bending and stretching. It was shown on neurons and botanical trees, not coronaries. [arXiv 2110.08693](https://arxiv.org/pdf/2110.08693)
- **SRVF on cerebral arteries:** a 2026 IEEE Access paper builds an SRVF Riemannian representation of cerebral artery centerlines, with tangent PCA for the main deformation modes. It is cerebral, but the method transfers. [DOAJ](https://doaj.org/article/bd17c041d7454a988bb033a5cb2868e2)

### Inferences
- **Fit to the user's data:** the user's tracer gives per-step lumen contours, so **radius(s) and curvature(s) profiles per trunk segment** are directly available. The Sangalli pipeline (register → fPCA → scores) is feasible without CFD and gives richer per-segment descriptors than one mean curvature or taper.
- **Registration landmarks:** anatomical landmarks (LM bifurcation, D1/OM origins) give natural landmark registration, which is simpler than elastic warping.
- **How much it adds:** the AneuRisk effect sizes were modest (about 32% error), even with n=65 and a strong anatomical hypothesis. Richer functional descriptors are not guaranteed to add much discrimination.
- **Using it in the prespecified test:** if fPCA scores are used, they must be fixed *before* the LR test. Fit the fPCA within each CV fold, or on the plaque-free baseline only with a prespecified number of components, so the one-test design holds.

### Gaps
- The concrete k-mean alignment result on AneuRisk65 (number of clusters, their anatomy, link to aneurysm location) could not be confirmed: the EJS PDF came back empty. From memory, the two clusters matched "S-shaped" vs "Omega-shaped" siphons. **This is unverified; do not cite it without checking.**
- I found no coronary application of fPCA or SRVF to CCTA centerlines with clinical outcomes.

## 3. Graph and tree descriptors, and coronary geometry phenotyping/clustering studies

### Takeaway
Tree-level topology descriptors exist: branch counts and lengths, and persistent homology (shown for brain arteries, which relates to age and sex). Coronary geometry clustering is **sparse and small**. The one direct study (left main phenotypes) has **n=76**, four clusters and only CFD-based "validation". I found no coronary deep-learning-embedding phenotyping study with clinical validation.

### Cited Findings
- **Persistent homology of brain artery trees** (Bendich, Marron, Miller, Pieloch, Skwerer 2016, Ann Appl Stat 10(1):198–218):
  - **Representation:** artery trees are turned into persistence diagrams. In the authors' words, the features capture how arteries **bend** through space rather than total length.
  - **Age:** the features correlate with age. That correlation stays significant after controlling for earlier summaries such as total length.
  - **Sex:** sex effects are stronger than in the only earlier study to find any.
  - **Cohort:** ages 18–72. The sample size was not in the snippets; the dataset is the UNC MRA brain artery set.
  - [arXiv 1411.6652](https://arxiv.org/pdf/1411.6652); [DOI 10.1214/15-AOAS886](https://dx.doi.org/10.1214/15-aoas886)
- **LM morphological phenotypes (BioMed Eng OnLine, Jan 2024):**
  - **Data and features:** 76 patients' LM arteries from CTA. Centerline geometry: stem length, bifurcation angle, ostium angulation, branch thickness.
  - **Clustering:** unsupervised, giving **four phenotypes**.
  - **Validation:** only CFD differences between phenotypes. The authors *suggest* the method may flag higher-risk people, but there was no outcome validation.
  - **Caveat:** the full text was not retrieved (bot check), so I could not confirm how k was chosen or whether stability was tested.
  - [PMC10804578](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10804578/); [BMC](https://biomedical-engineering-online.biomedcentral.com/articles/10.1186/s12938-024-01205-3)
- **Patient-level clustering in CAD** (Pezel et al. 2021, Front Cardiovasc Med): hierarchical clustering on clinical + CCTA + stress CMR data found 3 phenogroups. It clusters patients on mixed data, not vessel geometry. [Frontiers](https://www.frontiersin.org/articles/10.3389/fcvm.2021.760120)
- **Tortuosity:** cross-sectional studies link coronary tortuosity with CAD and calcium. One CT study found a significant tortuosity–calcium correlation after adjustment. These are small and retrospective. [PMC3164184](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3164184/)

### Inferences
- **Tree-level descriptors to consider:**
  - *Easy to get from the tracer:* dominance (already in the tabular data), number of side branches per trunk (D1/D2, OM1/OM2, presence of an intermediate artery), and trunk lengths. These are cheap descriptors that could serve as adjustment or descriptive variables.
  - *Tied to the LM angle:* the 89° vs 75° difference with or without an intermediate artery is large. Whether an intermediate artery is present (ramus, `im` segment in the headers) should be modelled alongside the LM angle.
  - *Persistent homology:* feasible from centerlines alone, but hard to interpret, and coronary validation is lacking.
- **Prior evidence:** no study clusters coronary geometry in more than about 100 people with clinical or outcome validation. A clustering result in CGPS (~1,800) would be among the largest, but the prior evidence that discrete coronary "types" exist is weak.

### Gaps
- I found no deep-learning embedding (graph neural network, autoencoder) of coronary trees used for patient phenotyping with clinical validation; the search was limited.
- The sample size of the Bendich dataset, and the cluster-selection details of the 2024 LM study, are unconfirmed.

## 4. Deciding whether clusters exist, and the danger of clustering continuous anatomy

### Takeaway
Coronary geometry varies continuously; nothing found suggests natural discrete types. Clustering will *always* return k groups, so cluster existence must be tested. Two checks:
- **Bootstrap stability** (Hennig: Jaccard ≥ 0.75 stable, ≤ 0.5 dissolved).
- Comparing against a **unimodal or continuous null**.

The diabetes-subtype debate (Dennis et al. 2019) shows clusters from continuous traits often predict *worse* than the continuous traits they were built from. That argues for keeping the user's continuous geometry block in the prespecified LR test, and treating any clustering as descriptive.

### Cited Findings
- **Hennig clusterwise bootstrap stability** (`fpc::clusterboot`):
  - **Thresholds:** a mean Jaccard ≥ 0.75 means a stable, valid cluster; ≥ 0.85 highly stable. 0.6–0.75 means a pattern with doubtful membership; < 0.6 should not be trusted. The default dissolution cutoff is ≤ 0.5, with theoretical support in Hennig (2008).
  - **Limit:** stability alone does not prove validity. Inflexible methods can give stable but invalid clusters (Hennig 2007).
  - [CRAN refman](https://search.r-project.org/CRAN/refmans/fpc/html/clusterboot.html); [rdocumentation](https://www.rdocumentation.org/packages/fpc/versions/2.2-13/topics/clusterboot)
  - A secondary source attributes a > 0.80 threshold to Hennig 2007, which conflicts with the fpc documentation's 0.75. [RSC supplement](https://www.rsc.org/suppdata/d1/mo/d1mo00150g/d1mo00150g2.pdf)
- **Clusters vs continuous features** (Dennis, Shields, Henley, Jones, Hattersley 2019, Lancet Diabetes Endocrinol 7(6):442–451):
  - **Design:** the Ahlqvist 5-cluster scheme was applied to ADOPT (n=4,351) and validated in RECORD (n=4,447).
  - **Results:** clusters did differ in progression and treatment response. However, **simple continuous clinical features beat the clusters** for choosing therapy, and baseline eGFR predicted CKD better than cluster membership.
  - **Authors' conclusion:** use specific phenotypic measures to predict specific outcomes rather than assigning subgroups. The cluster authors replied in published correspondence.
  - [Exeter ORE](https://ore.exeter.ac.uk/repository/handle/10871/36310); [PracticeUpdate](https://www.practiceupdate.com/content/disease-progression-and-treatment-response-in-data-driven-subgroups-of-type-2-diabetes-compared-with-models-based-on-simple-clinical-features/83208); [reply](https://ore.exeter.ac.uk/repository/handle/10871/40316?show=full)
- **AneuRisk precedent:** a well-defined anatomical grouping on ICA geometry was still only classified with about 32% error. [arXiv 1708.08257](https://arxiv.org/pdf/1708.08257)

### Inferences
Suggested protocol, built from standard methods. Sources were not fetched in this session for the gap statistic or GMM BIC; see Gaps.
1. **Standardise and adjust** the features for size, sex and phase first (section 5), so clusters do not just rediscover sex or body size. Medrano-Gracia showed size and LM angle differ by sex.
2. **Compare models:** fit a Gaussian mixture with k=1…K and compare BIC. If k=1 wins, report "no clusters". Also compute the gap statistic against a uniform or PCA-aligned reference, and the silhouette.
3. **Check stability:** run `clusterboot` with B ≥ 100. Report the Jaccard per cluster, and accept a cluster only at ≥ 0.75.
4. **Fit a continuous null:** fit a single multivariate Gaussian (or Gaussian copula) to the features, simulate datasets of the same size, and re-run the clustering. If the simulated data give the same silhouette or stability, the clusters are only a partition of a continuum.
5. **External or known-groups validation:** do the clusters differ in variables *not* used to build them (dominance, presence of the intermediate artery, sex, age, SCORE2)? Then, prespecified and descriptive only, check new plaque rate by cluster.
6. **Compare with the continuous model:** compare the cluster's ΔC with the continuous geometry block's ΔC in the same person-split CV. The Dennis result predicts that the continuous block will do at least as well.
7. **Fit with the thesis design:** this keeps the one prespecified LR test per question untouched. Clustering becomes a secondary, descriptive analysis.

### Gaps
- Primary sources were not retrieved for Tibshirani, Walther & Hastie 2001 (gap statistic), Fraley & Raftery (mclust BIC), or Rousseeuw 1987 (silhouette). These are standard references but **unverified in this session**.
- I found no coronary-specific paper that formally tested whether geometry clusters exist against a continuous null.

## 5. Normalising geometry for body/heart size and cardiac phase before clustering

### Takeaway
- **Size:** coronary diameter scales with body size (BSA) and sex. Some sex difference may remain after BSA indexing; the evidence is mixed. **Ratios** (LM→LAD, LM→LCx), angles and curvature are largely size-free, but absolute taper (mm/mm) and curvature (1/mm) are not.
- **Phase:** geometry changes over the cardiac cycle, and tortuosity is more pronounced in systole. The phase of each scan should be recorded and held fixed, or adjusted for. The atlas work used 75% R-R (end-diastole).

### Cited Findings
- **Dodge et al. 1992, Circulation 86:232–246:** normal coronary lumen diameter depends on age, sex, anatomic variation and LV hypertrophy or dilation. Women's arteries are narrower even after BSA normalisation, as cited by later work. [Swiss Med Wkly citing Dodge](https://smw.ch/index.php/smw/article/download/112/109/212)
- **Angiography, LM lumen:** BSA and sex are both independent predictors of coronary size, and body size has the greater influence. [PMC2268658](https://pmc.ncbi.nlm.nih.gov/articles/PMC2268658)
- **Contrary angiographic study:** in Indian and Caucasian patients, indexing to BSA removed the male–female diameter difference. This study is small and not CT-based. [PMC5560873](https://pmc.ncbi.nlm.nih.gov/articles/PMC5560873)
- **CT volumetric study** (50 women, 44 men, no CAD): coronary dimensions were compared adjusting for BSA and LV mass. Size explains some, but not all, of the sex differences. [PubMed 20043337](https://pubmed.ncbi.nlm.nih.gov/20043337/)
- **Medrano-Gracia 2016:**
  - **Angle after height adjustment:** the LM bifurcation angle sex difference survives height adjustment (p=0.002).
  - **BMI:** diameters were not related to BMI.
  - **Phase:** all scans were at 75% R-R. The authors note angles change through the cycle.
  - **Exclusions:** small female hearts were over-represented among exclusions.
  - [EuroIntervention](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)
- **Dynamic CT:** coronary geometry (curvature, tortuosity) changes through the cycle, but the *amount* of change was not related to CAD. [J Digit Imaging 2019](https://link.springer.com/article/10.1007/s10278-019-00300-5)
- **Tortuosity definitions:** these often require bends present in both systole and diastole. The LAD looks more tortuous in systole, and tortuosity may be less visible in large hearts. [PLoS ONE/DOAJ](https://doaj.org/article/ba12249b690141f5b7c63924570efa4b); [RSNA](https://pubs.rsna.org/doi/abs/10.1148/73.5.785); [PMC3164184](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3164184/)

### Inferences
Practical rules that follow from these findings:
1. **Use dimensionless features where possible:**
   - diameter ratios (already planned);
   - taper as relative change per unit length, or Δ log diameter per normalised length;
   - curvature × local diameter, or curvature times segment length;
   - tortuosity index (arc length / chord).

   Keep log segment length as a covariate, as the where model already does.
2. **Adjust for body size and sex where absolute measures stay:** where absolute measures (mm) remain, adjust for BSA (available in both BL and FU) and `male`, or residualise on them before clustering. Otherwise clusters will reproduce sex and body size.
3. **Cardiac phase:** if the reconstruction phase per scan is not in the headers, it is **not available**. The listed headers cover heart rate during preparation and scan, but `hr_during_scan` has only 268 BL values. In that case:
   - use heart rate in preparation as a proxy covariate;
   - run a sensitivity analysis on curvature-based features, since they are the most phase-sensitive.
4. **Intermediate artery and dominance:** state these, or stratify on them, before interpreting LM angle clusters. Intermediate-artery presence alone shifts the angle by about 14°.

### Gaps
- No CCTA study found that quantifies how much curvature or taper change between 70–80% R-R reconstructions vs systolic ones in a way usable as a correction factor.
- Whether the CGPS NIfTI headers or DICOM metadata store the reconstruction phase is not known from the tabular headers.
- No source found on normalising coronary geometry for heart size (LV mass or volume) specifically before clustering.
