# Coronary (and other site-level) precedents: shared vs artery/position-specific predictor effects

Scope: how published segment-, vessel- or lesion-level coronary plaque models handle artery and
position, and whether predictor effects were allowed to differ by artery/position. Research budget
was limited (about 17 tool calls); several full texts (PREDICTION, EMERALD, PARADIGM per-lesion)
were paywalled, so their exact model specifications could not be checked. Items marked
"[not re-verified]" are from prior knowledge, with DOI, but their full text was not read in this session.

## 1. CCTA segment/lesion/vessel-level plaque progression and location models

### Takeaway
The large CCTA registries (PARADIGM, and as far as I could check ICONIC/EMERALD) model artery as a
**main effect or a stratifier**, and handle clustering with GEE or marginal Cox models. I found
**no** CCTA plaque-progression study that estimated artery- or position-specific slopes for a
predictor and formally tested that heterogeneity. Vessel identity itself has a large main effect
(LAD > RCA > LCx), which supports keeping position/artery dummies in the base. It does not show
that predictor slopes differ by artery.

### Cited Findings
- **PARADIGM, per vessel (Bax et al. 2022):** 1,344 patients with serial CCTA (median 3.3 y),
  multinational registry of patients referred for clinically indicated CCTA (suspected CAD). Any
  plaque progression: LCx 41.0%, RCA 52.7%, LAD 77.4% (P < 0.001). Annualised plaque volume change:
  LCx 1.8, RCA 6.4, LAD 7.3 mm³/y. Adjusted OR for prompt progression vs LCx: LAD 1.98
  (1.66–2.36), RCA 1.43 (1.22–1.70). Progression to obstructive CAD, HR vs LCx: LAD 2.45
  (1.49–4.02), RCA 1.51 (0.89–2.56). — [Bax AM et al., Eur Heart J Cardiovasc Imaging 2022;23(11):1482–1491, doi:10.1093/ehjci/jeac044](https://academic.oup.com/ehjcimaging/article/23/11/1482/6574367)
- **Model used in that paper:** logistic GEE (vessels clustered within patient) and marginal Cox
  models for multivariate failure times. Vessel was the exposure; covariates (ASCVD risk, statin,
  per-vessel baseline PAV) had **shared coefficients**. No formal vessel × covariate interaction
  tests were reported. Heterogeneity was explored only by stratification (baseline stenosis
  severity, high-risk plaque, sex, statin). The LAD/RCA vs LCx differences were not significant in
  people with obstructive CAD at baseline (a post hoc stratified finding). — [Bax et al. 2022](https://academic.oup.com/ehjcimaging/article/23/11/1482/6574367)
- **PARADIGM, per lesion (Lee et al. 2020):** 1,297 patients with only non-obstructive lesions at
  baseline (3,218 lesions); 76 lesions (2.4%, 60 patients) became obstructive over a mean of 3.8 y.
  C-statistic: clinical model 0.684; plus per-patient plaque volume and high-risk plaque 0.825;
  plus per-lesion features 0.895. The abstract does not describe how clustering or location was
  handled. — [Lee SE et al., Int J Cardiovasc Imaging 2020;36:2357–2364, doi:10.1007/s10554-020-01960-z](https://pubmed.ncbi.nlm.nih.gov/32779077/)
- **PARADIGM lesion-location grouping:** lesions were grouped as LM, proximal (pLAD/pLCx/pRCA) or
  other (AHA 17-segment model), and plaque volume, composition and progression were compared across
  the groups. This is location as the exposure, not location × predictor. — [Leiden repository record](https://scholarlypublications.universiteitleiden.nl/handle/1887/3232666) (results not retrieved)
- **PARADIGM per-vessel plaque burden (cross-sectional):** LCx had the lowest total plaque volume,
  then RCA, then LAD, even after adjusting for vessel length or volume. LCx lesions were more
  distal and more often calcified (55.3% vs RCA 39.4%, LAD 32.7%). ≥2 high-risk features: LCx 3.8%,
  RCA 10.9%, LAD 21.4%. — [Leiden repository](https://scholarlypublications.universiteitleiden.nl/access/item%3A3310064/view)
- **EMERALD (Lee JM et al. 2019):** case–control, 66 ACS culprit vs 150 non-culprit lesions.
  Culprits had lower FFRCT and higher ΔFFRCT, WSS and axial plaque stress. Lesion-level,
  symptomatic/ACS population; no artery-specific predictor effects were reported in the material I
  could access. — [Lee JM et al., JACC Cardiovasc Imaging 2019;12(6):1032–1043](https://repub.eur.nl/pub/121045)
- **MESA vessel-distribution CAC (Blaha et al. 2016):** 3,262 participants with CAC > 0, 10-y
  follow-up. The **number of calcified vessels** (1–4, LM included) improved CHD/CVD prediction
  over Agatston (HR 1.9–3.5 for four vessels vs fewer). A diffuse pattern added nothing. Regional
  information entered as person-level summaries, not as per-vessel predictor slopes. — [Blaha MJ et al., JACC Cardiovasc Imaging 2016;9(12):1407–1416](https://www.acc.org/Latest-in-Cardiology/Journal-Scans/2016/12/08/15/51/Improving-the-CAC-Score-by-Addition-of-Regional-Measures)
- **Position as weights rather than as interactions [not re-verified]:** the CT-adapted Leaman
  score applies fixed, published segment weights (by position and dominance) to plaque burden, so
  position enters as an a priori multiplier on burden, not as an estimated slope. — de Araújo
  Gonçalves P et al., Eur Heart J Cardiovasc Imaging 2013;14:1045–1055, doi:10.1093/ehjci/jet058
- **Proximal clustering of MI occlusions [not re-verified]:** acute occlusions cluster in the
  proximal third of each artery. This is a position main effect. — Wang JC et al., Circulation
  2004;110:278–284, doi:10.1161/01.CIR.0000135468.67850.F4

### Inferences
- In the CCTA field, the default is to put artery/position in as a main effect (or to report it as
  an exposure) and to estimate one shared coefficient for every other predictor. Artery-specific
  predictor slopes are not standard practice, and I found none that were prespecified.
- The large LAD/RCA/LCx main effects in PARADIGM argue for keeping segment dummies in the base. They
  are not evidence that geometry slopes differ by artery.
- All these cohorts are referral, symptomatic or ACS cohorts with plaque at baseline (PARADIGM,
  EMERALD) or CAC > 0 (the MESA subset). None is a plaque-free, population-based incident cohort.

### Gaps
- ICONIC, CONFIRM, SCOT-HEART, Dallas Heart: no segment-level model with artery × predictor terms
  was found in this session. I was unable to check whether their supplements contain any.
- Full methods of Lee 2020 (PARADIGM per-lesion) and EMERALD 2019 (clustering, location
  covariates) were not accessible.

## 2. PREDICTION and other WSS–progression studies: by artery or pooled?

### Takeaway
PREDICTION (the largest WSS study) reports **pooled** effects. The one study that analysed WSS
effects **by vessel** (Hartman et al. 2021, 41 vessels) found the low-WSS–progression relation
consistently only in the RCA (in the LAD only with vessel-specific thresholds; never in the LCx),
but it explicitly says it lacked the power to compare vessels. That is a small, post hoc,
hypothesis-generating signal of heterogeneity. Part of it reflects absolute WSS differing by
vessel, i.e. thresholds and scale, rather than true slope differences.

### Cited Findings
- **PREDICTION (Stone et al. 2012):** 506 ACS patients after PCI, three-vessel IVUS/angiography
  profiling (about 2.7 arteries per patient), arteries divided into 3-mm segments; 374 re-profiled at
  6–10 months. Large plaque burden and low ESS independently predicted lumen-area decrease. The
  combined predictor had a PPV of 41% and an NPV of 92% for progression to a PCI-treated obstruction.
  Results in the abstract are pooled over arteries. — [Stone PH et al., Circulation 2012;126:172–181, doi:10.1161/CIRCULATIONAHA.112.096438](https://pubmed.ncbi.nlm.nih.gov/22723305/)
  - The full-text statistical section (handling of clustering, any artery covariate or stratum) could
    not be accessed (publisher returned HTTP 403). The low-risk Japanese ACS population is noted in [TCTMD](https://www.tctmd.com/news/endothelial-shear-stress-works-prediction-tool).
- **Hartman et al. 2021 (Rotterdam IMPACT-type cohort):** 40 ACS patients, 41 non-culprit vessels
  (15 LAD, 10 LCx, 16 RCA), 10,205 sectors. Mixed model with WSS category and **vessel type as fixed
  effects** and the individual vessel as a random effect; GLMM for prediction.
  - Absolute WSS differed by vessel (median LAD 0.56, LCx 0.87, RCA 0.92 Pa), so absolute
    thresholds were judged inappropriate.
  - With vessel-specific tertiles, low WSS showed more progression in the LAD and RCA but not the
    LCx. With study-wide tertiles or literature thresholds, **only the RCA** showed the pattern.
  - Pooled OR for low WSS (vessel-specific tertiles) was 1.6 (1.3–2.1).
  - The authors say the number of vessels per type was too small for a detailed between-vessel
    analysis.
  — [Hartman EMJ et al., Sci Rep 2021;11:22086, doi:10.1038/s41598-021-01232-3](https://pmc.ncbi.nlm.nih.gov/articles/PMC8586146/)
- **Molony et al. 2015:** 3 patients (LAD/LM). Computed WSS–plaque change relationships varied with
  side branches and inflow assumptions, and **relative** WSS suppressed the variability. The
  authors suggest these modelling differences "may contribute to the large variability typically
  found among subjects in pooled populations". — [Molony DS et al., Biomed Eng Online 2015;14(Suppl 1):S2, doi:10.1186/1475-925X-14-S1-S2](https://pmc.ncbi.nlm.nih.gov/articles/PMC4306111/)
- Other WSS work cited in searches uses linear mixed models across plaque phenotypes (pooled over
  arteries). — [Heart 2019;105:1078](https://heart.bmj.com/content/105/14/1078)
- [not re-verified] PROSPECT ESS analysis (Stone PH et al., JACC Cardiovasc Imaging
  2018;11:462–471, doi:10.1016/j.jcmg.2017.01.031) and Kumar A et al. (high WSS and MI, JACC
  2018;72:1926–1935, doi:10.1016/j.jacc.2018.07.075): both lesion-level and pooled over arteries,
  as far as I recall. I have not confirmed whether artery was a covariate.

### Inferences
- The pattern in the WSS literature is pooled slopes, with artery either ignored or handled as a
  main effect or random effect. Where vessel-specific behaviour appeared (Hartman 2021), it came
  from a small sample, was not formally tested, and was partly a **scale/threshold** effect: the same
  absolute WSS means different things in different vessels. That points to standardising a feature
  within artery (or a relative measure) as an alternative to artery-specific slopes.
- For the thesis's curvature/taper: if feature distributions differ by artery, one shared slope on a
  raw feature implicitly assumes the same per-unit effect everywhere. Within-artery standardisation
  or centring is the lower-cost analogue of Hartman's vessel-specific tertiles.

### Gaps
- PREDICTION full-text methods (GEE vs mixed model, artery adjustment, any per-artery results) were
  not verified.

## 3. Geometry (tortuosity, bifurcation angle, diameter ratios, taper) vs plaque: per artery?

### Takeaway
Geometry–plaque studies are small, cross-sectional, mostly symptomatic or referral cohorts, and they
are **artery-specific by construction** (the LM bifurcation angle relates to left-sided disease) or
report artery-level prevalence. I found none that estimated a geometry effect separately per
artery and tested heterogeneity statistically. Results conflict across studies.

### Cited Findings
- **LAD–LCx bifurcation angle:** 106 patients with CCTA plus invasive angiography; the LAD–LCx angle
  was an independent predictor of ≥50% left coronary stenosis, OR 1.423 (per unit as reported),
  P = 0.002 (sens 66.7%, spec 78.4%). A wider angle was related to non-calcified lesions. Small,
  single-centre, symptomatic. — [PLoS ONE 2017, PMC5367806](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5367806/)
- **LM–LAD and LAD–LCx angles vs proximal LAD stenosis:** LM–LAD OR 1.094 (1.053–1.137); LAD–LCx
  OR 0.951 (0.924–0.978). The direction of the latter conflicts with the PLoS ONE study and with the
  paper's own group means, so it is possibly a coding or reporting issue. — [Cardiovasc J Afr vol 34 issue 2](https://cvja.co.za/onlinejournal/vol34/vol34_issue2/33)
- **LM trifurcation/bifurcation angle vs calcification:** about 1% greater odds of LCA
  calcification per degree. — [Pol Heart J (Kardiol Pol) 2022](https://journals.viamedica.pl/polish_heart_journal/article/view/90777)
- **Tortuosity by artery (angiography):** the prevalence of tortuosity differs by artery, and the
  cohorts disagree (LCx most often involved in an Iranian cohort; LAD in a Sydney cohort of 870).
  Definitions differ. Reviews describe the tortuosity–atherosclerosis link as conflicting. — [J Cardiovasc Thorac Res 2018;10(4):209–213](https://jcvtr.tbzmed.ac.ir/PDF/jcvtr-23381); [PMC5454180](https://pmc.ncbi.nlm.nih.gov/articles/PMC5454180)
- **Curvature/torsion vary by position within an artery:** in the LAD, curvature, torsion and
  tortuosity are generally highest distally; in the RCA they are smallest in the mid segment
  (cine-angiography, 32 LAD / 35 RCA). This implies that feature distributions differ by segment. — [CinC 2005 proceedings](https://www.cinc.org/old/Proceedings/2005/pdf/0105.pdf)
- A 2022 ESR (ECR) poster summarises CCTA associations of high angles, high calibre and high
  tortuosity with atherosclerosis, and an RCA-shape association. This is a conference poster and
  low-grade evidence. — [ECR 2022 C-10921](https://epos.myesr.org/poster/esr/ecr2022/C-10921/Findings%20and%20procedure%20details)

### Inferences
- There is no published precedent for artery × geometry slopes in an incident-plaque model. A shared
  slope with artery/position main effects is consistent with the literature, and so is restricting
  artery-specific features to their anatomical rows (e.g. the LM angle on pLAD/pLCx only).
- Because curvature and taper distributions differ systematically by segment (CinC 2005;
  tortuosity cohorts), a shared slope on the raw feature partly mixes between-segment and
  within-segment variation. Segment dummies absorb the mean differences but not scale differences.

### Gaps
- I found no CCTA study relating taper or the LM→LAD/LM→LCx diameter ratio to plaque per artery.
- No meta-analysis of bifurcation angle vs plaque was found.

## 4. Methodological precedent from other domains with positional units

### Takeaway
Periodontal research is the closest analogue: sites nested in teeth nested in persons, analysed with
multilevel models. Tooth type typically enters as a **main effect**. Random slopes have been used
for continuous baseline covariates, not for site position. I did not verify any study using
position-specific slopes for a predictor.

### Cited Findings
- **Tomasi, Leyland & Wennström 2007:** multilevel (patient/tooth/site) models of non-surgical
  periodontal treatment outcome. Smoking, site-level plaque and **tooth type** were significant
  factors (location at a molar being significant). The continuous model revealed additional
  significant interactions between covariates. A **random-slopes** model showed that the
  variability in final pocket depth increased with initial PPD (a slope on baseline PPD, not on tooth
  position). — [J Clin Periodontol 2007;34(8):682–690, doi:10.1111/j.1600-051X.2007.01111.x](https://eprints.gla.ac.uk/15848); [summary](https://searchworks.jioinstitute.edu.in/articles/asx__25736602)
- **Three-level periodontal model:** tooth type, surfaces involved and tooth mobility were the
  strongest site/tooth-level factors (main effects). — [Brazilian Oral Research](https://doaj.org/article/e1352f18f8f34b7d93b00d2d4df5e77f)
- **Gilthorpe et al.:** introduced multilevel modelling for site-in-tooth-in-subject data and
  showed that risk factors operate at more than one level. — [J Periodontal Implant Sci review](https://synapse.koreamed.org/articles/1082472)
- The general random-slope formulation (a slope varying by higher-level unit, β1j) is described in
  [J Periodontal Implant Sci 45(1)](https://synapse.koreamed.org/articles/1082472).

### Inferences
- The positional-unit literature supports the thesis's structure (position as fixed main effects,
  person random intercept, shared covariate slopes). Where heterogeneity is examined, it is either
  covariate × covariate interactions or random slopes across *persons*, not slopes by site type.
- With 9 segments, position-specific slopes would be a fixed interaction (feature × artery, 2 extra
  df per feature, or × position, 8 df). A random slope by segment with only 9 (or 3) levels is
  poorly identified.

### Gaps
- Vertebrae, retinal-sector and lung-lobe examples were not searched within the budget.

## 5. Reported magnitude of heterogeneity

### Takeaway
The only quantitative signal is (a) large **main-effect** differences between arteries in
progression (PARADIGM: LAD about 2× LCx) and (b) qualitative, untested vessel differences in the
WSS slope (Hartman 2021: a consistent effect in the RCA only, none in the LCx, n = 10–16 vessels
per type). No study reported an interaction coefficient or heterogeneity test for a geometry or
haemodynamic predictor by artery.

### Cited Findings
- PARADIGM: LAD vs LCx adjusted OR 1.98 for prompt progression; RCA vs LCx 1.43. — [Bax et al. 2022](https://academic.oup.com/ehjcimaging/article/23/11/1482/6574367)
- Hartman 2021: the share of progressing sectors was 8% LAD, 15% LCx, 11% RCA. The LCx had the
  highest progression despite the highest WSS. The low-WSS effect was significant only in the RCA
  under three of four threshold definitions. — [Hartman et al. 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8586146/)

### Inferences
- The evidence does not justify prespecifying artery-specific geometry slopes. A defensible design
  consistent with precedent is: shared slopes in the primary model (as the thesis does), with an
  artery × feature interaction as a single secondary/sensitivity test, reported as exploratory.
  Within-artery standardisation of the features is an option that addresses the scale issue
  Hartman identified.
- Power caveat: with a binary outcome over about 10 years in plaque-free people, events per artery
  will be modest. Feature × artery terms (2 df per feature) would be weakly estimated, and any
  "LAD-only" finding would be a post hoc subgroup result.

### Gaps
- No pooled or meta-analytic estimate of artery heterogeneity for any geometric predictor exists in
  what I found.
