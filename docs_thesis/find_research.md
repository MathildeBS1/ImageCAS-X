# find_research.md — geometry as a predictor of coronary artery disease

**Pass:** 2026-09-06. **Branch:** `clean_version`.
**Purpose:** source material for objective 4's state-of-the-art section — specifically the question
*does the shape of the coronary tree predict coronary artery disease, how well, and in whom?*
**Status:** 14 search queries, 22 papers selected. Metadata verified against Crossref and Europe PMC
(every DOI resolves); **claims are abstract-level, no paper read in full.** Nothing here is `[VERIFIED]` in the `refs.bib` sense until its full text is read.

**Relation to `docs_thesis/literature.md`.** That file's Axis 5 establishes the *mechanism* — shape
sets wall shear stress, shear drives the endothelial response. This file asks the empirical question
that follows: what has actually been measured, in how many patients, and against what endpoint. Where
the two overlap this file cites Axis 5 rather than repeating it. Where this pass **contradicts or
updates** `literature.md` it says so in bold; nothing there is silently overwritten.

**Conventions**, from `.claude/skills/thesis-writing/SKILL.md`:

- Every entry carries the five elements or it is cut: author and year; the data with n; what they
  did; the number; **what it licenses here**. An entry with only the first four is a summary.
- Every reported quantity carries value, dispersion, n and cohort — or an explicit note that the
  source does not report one.
- Queries that came back empty are recorded, so every "nothing exists" claim is auditable.

---

## Search record

| # | Query | Outcome |
|---|---|---|
| 1 | coronary artery geometry predictor of coronary artery disease CCTA 2026 | Orientation only. Confirms the field's centre of gravity is *plaque* radiomics, not tree geometry. |
| 2 | left main bifurcation angle coronary artery disease severity CCTA cohort 2024 2025 | Mansouri 2024; CLAP score 2024; Temov & Sun 2016; the 2026 ramus intermedius cohort. See §1.1. |
| 3 | coronary artery tortuosity association with CAD meta-analysis cohort | Groves 2009 (n = 1221); Zebić Mihić 2023b (n = 160). **Direction of the association is not what §6 implies.** See §1.2. |
| 4 | coronary dominance left dominant circulation prognosis mortality cohort study | CONFIRM registry (n = 6382, null); Khan 2016 meta-analysis (n = 255,718). **Contradicts the sole source §6 currently uses.** See §1.3. |
| 5 | ramus intermedius left main bifurcation angle atherosclerosis CCTA 1380 patients 2026 | Bekirçavuşoğlu 2026 (n = 1380); Zhang 2023 (n = 200). See §1.4. |
| 6 | coronary artery tortuosity index CCTA quantitative 2024 2025 obstructive coronary disease | Zebić Mihić 2023b; SCCT 2024 quantitative standards; CArTI (AHA 2025 abstract); an unsupervised HMM tortuosity method. See §1.2 and §4. |
| 7 | coronary artery ostial take-off angle origin angle atherosclerosis plaque CCTA association | **Effectively empty for normal anatomy.** Everything returned concerns *anomalous* origin. See §1.5. |
| 8 | machine learning coronary tree geometry predict major adverse cardiac events CCTA large cohort 2025 | Ma 2025 systematic review; Kim 2025. Everything returned is **plaque radiomics**, not tree geometry. See §2. |
| 9 | statistical shape model coronary artery anatomy population variation cohort 2024 2025 | Shen 2026 review; Sharp 2026 SSM review. **No statistical shape model of the coronary tree found** — the SSM literature is chambers and ventricles. See §4. |
| 10 | Copenhagen General Population Study coronary CT angiography plaque cohort | Fuchs 2023, **the CGPS CCTA cohort itself**, n = 9533 with adjudicated MI. See §2. |
| 11 | geometric features alone predict wall shear stress coronary ML surrogate CFD FFR-CT | Griffo 2026 (GEM-GCN, n = 748 patients) and the physics-informed line behind it. **Answers the question Axis 5 left open.** See §3. |
| 12 | graph neural network coronary artery tree topology disease prediction centerline 2025 2026 | AngioGraphCAD (nearest competitor); otherwise patient-similarity and segment-labelling graphs, not tree topology. See §4. |
| 13 | coronary bifurcation angle measurement reproducibility inter-observer variability CCTA | Givehchi 2018 phantom study; Cui 2017. **Between-technique disagreement is the size of the biological effect.** See §5.1. |
| 14 | coronary geometry changes with age remodeling reverse causation atherosclerosis | Glagov 1987; Kwon 2022 (carotid, 10-year longitudinal). See §5.2. |

---

## Stage 1 — feature by feature: the direct association

### 1.1 Bifurcation angle — four cohorts, one direction, none large

**Temov & Sun 2016** (*Int J Cardiovasc Imaging* 32(Suppl 1):129–137, doi:10.1007/s10554-016-0884-2,
PMID 27076223) measured the LAD–LCx angle on 2D and 3D reconstructions in **n = 196** CCTA cases
(129 male, 67 female, mean age 58 ± 10.5 years) and reported a mean of **79.40° ± 22.97°, range
35.5°–178°**. Males were 2.07-fold more likely to exceed 80° (p = 0.003) and patients with
BMI > 25 kg/m² 2.54-fold more likely (p = 0.001).
*Licenses:* this is the population §6's floating "76.4° ± 16.7°" needs attached to it — value,
dispersion, n and cohort in one place. It also warns that the angle covaries with sex and BMI, so any
angle distribution reported from our 800 cases must be stratified by sex rather than pooled.

**Juan et al. 2017** (`juan2017bifurcation`, already cited in §6), **n = 313** CCTA in three strata,
supplies the disease-severity gradient: 75.5° ± 14.7° (40 normal), 81.2° ± 20.1° (62 non-significant),
87.3° ± 18.8° (211 significant).

**Mansouri et al. 2024** (*Health Sci Rep* 7(6):e2182, doi:10.1002/hsr2.2182, PMID 38868537,
open access) analysed **n = 122** patients who had both CCTA and invasive angiography, and correlated
CCTA-derived measures against the Gensini score. Median LAD–LCx angle **58° (IQR 39°–89°)**;
correlation with Gensini **0.684, p = 0.0001** — a stronger correlation than aggregated plaque
volume (0.281), remodeling index (0.438) or calcium score (0.217). A 47.5° cut-off gave 86.7%
sensitivity and 82.1% specificity.
*Licenses:* an independent replication of the angle–severity gradient against a **continuous**
severity score rather than three strata, and the geometric measure out-performing the plaque measures
in the same patients. The cut-off itself does not transfer — one centre, n = 122 — which is the
evidence behind §6's existing decision to take the direction of the association and not a threshold.

**Tommasino et al. 2024**, the CLAP score (*J Cardiovasc Dev Dis* 11(11):338, doi:10.3390/jcdd11110338,
PMID 39590181, open access), analysed **n = 499** of 650 consecutive CCTA patients with follow-up.
Severe proximal LAD stenosis in 32% (160/499); MACE in 12.5%. A left main bifurcation angle **> 80°
was the strongest predictor of MACE, HR 4.47 (95% CI 3.80–6.70, p < 0.001)** — ahead of diabetes
(2.94), obstructive CAD (2.50) and high-risk plaque (2.30). The derived score reached AUC 0.91
(0.86–0.96) in development and 0.85 (0.79–0.91) in validation.
*Licenses:* the only **outcome** evidence for bifurcation angle found in this pass. It moves the
angle from "associated with disease severity" to "associated with events", which is the cell §6
cannot currently fill for any tree-scale feature except dominance.
*Caveat to check before quoting:* the published interval 3.80–6.70 is not centred on the point
estimate 4.47 in the way a log-scale hazard ratio normally is. Read the full text before putting that
number in the thesis.

### 1.2 Tortuosity — the association runs the opposite way from the naive reading

**Groves et al. 2009** (*W V Med J* 105(4):14–17, PMID 19585899; **no DOI**) is the largest tortuosity
cohort found: **n = 1221** consecutive coronary angiograms over eight months, severe coronary
tortuosity (SCT) defined as two consecutive 180° turns in a major epicardial artery, found in
**12.45%**. Severe tortuosity was associated with a **significantly *lower* incidence of significant
coronary artery disease (p = 0.003)**. Female sex was more common in the tortuosity group (p = 0.039);
hypertension, hyperlipidemia, smoking, family history, diabetes and age ≥ 65 were *not* predictors of
SCT.
*Licenses:* the correction §6 needs. Tortuosity is not a risk marker for obstructive disease — in the
largest cohort it is inversely associated with it. Publication venue is a state medical journal with
no DOI, so it is quoted as the largest available cohort, not as the strongest evidence.

**Zebić Mihić et al. 2023b** (*Diagnostics* 14(1):35, doi:10.3390/diagnostics14010035, PMID 38201343,
open access) — a second paper from the group behind `zebicmihic2023tortuosity`, and the more useful
one methodologically. **n = 160** patients with angina and stress-test-documented ischemia, or ACS,
all with invasive angiography. Tortuosity was measured **twice**, by a continuous tortuosity index and
by the clinical bend-angle count. Tortuosity was significantly higher in non-obstructive than in
obstructive CAD for all three arteries (p < 0.01), and the index localized: highest LCx index with
lateral ischemia and highest LAD index with anterior ischemia (both p < 0.001). **The angle method
found only one association** — LCx tortuosity with lateral ischemia, OR 4.9, p = 0.046.
*Licenses:* the strongest single argument in this pass for how objective 7 should define its
features. The same patients, the same anatomy, two measurement definitions, and the continuous index
detects territory-specific associations the discrete bend count misses almost entirely. This is the
evidence for computing a continuous tortuosity index on our centerlines rather than reproducing the
clinical "three bends over 45°" score.

**Reconciling the three tortuosity papers.** They agree once the endpoint is stated precisely:
tortuosity tracks ischemia *without* obstructive stenosis (`zebicmihic2023tortuosity`, OR 7.96;
Zebić Mihić 2023b, territory-matched), and tracks *inversely* with obstructive stenosis (Groves,
p = 0.003). §6 as written quotes only the non-obstructive association and is therefore not wrong, but
it omits the inverse relationship — and a reader who takes "tortuosity is associated with disease"
forward will misread every tortuosity number this thesis reports. The inverse arm needs one sentence.

### 1.3 Dominance — the largest cohort does not reproduce the effect §6 quotes

**This is the clearest contradiction found in the pass**, and it lands on a sole-source paragraph.

**Gebhard et al. 2015**, the CONFIRM registry (*Eur Heart J Cardiovasc Imaging* 16(8):853–862,
doi:10.1093/ehjci/jeu314, PMID 25744341, open access), followed **n = 6382** CCTA patients (47%
female, mean age 56.9 ± 12.3 years) across 12 centres in 6 countries for **60 months**. Right
dominance 91% (n = 5817), left 9% (n = 565); codominant cases were excluded for low numbers. Survival
did **not** differ by dominance in any stratum: obstructive CAD HR 0.46 (0.16–1.32, p = 0.15),
non-obstructive HR 0.95 (0.41–2.21), normal arteries HR 1.04 (0.68–1.59). The one positive result was
a subgroup: left dominance **with left main disease**, HR 6.45 (1.66–25.0, p = 0.007).
*Licenses:* §6 currently states a 3.20-fold hazard for left dominance on `veltman2012dominance`
(n = 1425) alone. A CCTA cohort 4.5× larger with 2.5× the follow-up finds nothing overall. Both must
be reported, and the dominance paragraph stops being a summary of one source.

**Khan et al. 2016** (*Catheter Cardiovasc Interv* 88(2):201–208, doi:10.1002/ccd.26281,
PMID 26524998) pooled 5 studies, 8 comparisons and **255,718 participants** with acute coronary
syndrome: left dominance carried **OR 1.27 (95% CI 1.13–1.42, p < 0.0001, I² = 34%)** for mortality,
consistent across in-hospital (1.37), 30-day (1.69) and long-term (1.15) windows.
*Licenses:* the effect is real but **small — 27% relative — and conditioned on ACS**. Read beside
CONFIRM's null in stable CCTA patients, the picture is that dominance matters once an infarct has
happened, because left dominance puts more myocardium at risk, and not as a predictor of getting
there. That is a sharper claim than §6 currently makes and it is better supported.

**Our own cohort, for the comparison the skill requires.** `Descriptors.xlsx` gives 729 R / 41 L /
30 Co over the 800 usable cases (figures quoted from `CLAUDE.md`, which records them as a `week1`
result not yet re-verified on this branch — recount before printing them) — **91.1% right, 5.1% left, 3.8% codominant**. The right-dominance
share matches CONFIRM's 91% exactly; our left-dominance share is well below their 9%, because CONFIRM
excluded codominant hearts rather than counting them as a third class. Report both, and say why they
differ.

### 1.4 Ramus intermedius — the cleanest natural experiment available to us

An RI is an extra branch off the left main bifurcation. Its presence changes the bifurcation angle
without changing anything else about the patient, which makes it the closest thing in coronary
anatomy to a controlled test of whether tree-scale geometry drives plaque location.

**Bekirçavuşoğlu et al. 2026** (*Clin Radiol* 96:107299, doi:10.1016/j.crad.2026.107299,
PMID 41962318) is the newest and largest paper in this pass: **n = 1380** CCTA patients enrolled
April 2021–January 2025. RI present in **31.8% (n = 462)**. RI was the **strongest risk factor for
plaque presence in the left main, proximal LAD and proximal LCx** in both univariable and
multivariable analysis; the bifurcation angle was higher in the RI group; there was **no** association
with degree of stenosis; and mixed-type plaque was more common in the LAD of RI patients
(p = 0.020).
*Licenses:* a hypothesis this thesis can test directly. ImageCAS-X labels `IM` (label 8) in ~25% of
cases against their 31.8% — the ~25% is a `week1` figure carried in `CLAUDE.md` and not re-verified
here, so recount it before comparing, and `medranogracia2016atlas` reports the matching angle contrast
(89° ± 21° with an intermediate artery versus 75° ± 23° without, p < 0.001). Presence of RI,
bifurcation angle and plaque distribution are all things our data carries or can compute, so this is
the tree-scale feature with the shortest path from published claim to a result of our own.

**Zhang et al. 2023** (*BMC Med Imaging* 23(1):53, doi:10.1186/s12880-023-01009-2, PMID 37041479,
open access) is the contradiction to hold against it. **n = 200** (100 RI, 100 no-RI, randomly
enrolled from CCTA over nine months): proximal LAD plaque in **77% versus 53% (p < 0.05)** — but the
difference **did not survive propensity-score matching**, and multivariable analysis found RI was
**not an independent risk factor**. Their own conclusion is that RI acts indirectly, by geometry,
rather than as a risk factor in its own right.
*Licenses:* the RI effect is confounded and n-dependent — significant unmatched at n = 200, gone
after matching, back at n = 1380. State it as a geometric mediator, never as a risk factor, and treat
the disagreement as the reason our 800-case replication is worth doing.

### 1.5 Ostial take-off angle — searched, and empty for normal anatomy

Query 7 returned no study relating take-off or origin angle to atherosclerosis in **normally
arising** coronary arteries. Everything found concerns *anomalous* origin — anomalous coronary artery
from the opposite sinus, where a mean take-off angle of 14.4° ± 4.5° accompanies a slit-like ostium
and an intramural course, and the geometry is read as a categorical high-risk feature.

This is `literature.md` Axis 4's finding reappearing on a different feature: coronary geometry is
handled clinically as a **taxonomy of named abnormalities**, not as a continuous distribution over a
population. Recorded here as an empty cell in the matrix rather than a feature to extract.

---

## Stage 2 — the newest and the largest cohorts

**The asymmetry this stage found is the finding.** The largest CCTA outcome cohorts in the field
measure *plaque* — its presence, its burden, its extent — in 6000 to 10,000 patients with adjudicated
events. The largest cohorts measuring *shape* are an order of magnitude smaller, and the continuous
geometric measures (angle, tortuosity) top out in the low hundreds. Nobody has measured tree geometry
at the n where the outcome cohorts live. That asymmetry is objective 8's opening.

**Fuchs et al. 2023** (*Ann Intern Med* 176(4):433–442, doi:10.7326/M22-3027, PMID 36972540) is the
**Copenhagen General Population Study CCTA cohort itself** — the dataset this project moves to under
Track B. **n = 9533** asymptomatic persons aged ≥ 40 without known ischemic heart disease, CCTA read
blinded to treatment and outcomes. 5114 (54%) had no subclinical coronary atherosclerosis, 3483 (36%)
non-obstructive and 936 (10%) obstructive disease. Over a median 3.5 years (range 0.1–8.9), 193 died
and 71 had a myocardial infarction. Adjusted relative risk for MI: obstructive **9.19 (95% CI
4.49–18.11)**, extensive **7.65 (3.53–16.57)**, obstructive-and-extensive **12.48 (5.50–28.12)**.
Stated limitation: mostly White participants.
*Licenses:* three things at once. Objective 10's endpoint **already exists and is already
adjudicated** in this cohort, with a known event count — 71 MIs in 9533 over 3.5 years, which is the
number any geometry-based analysis must be powered against. It sets the bar: a geometric feature has
to add something to "obstructive and extensive", which alone carries RR 12.5. And it shows CGPS
characterizes the coronary tree by **stenosis and extent, never by shape** — which is exactly the
room this thesis proposes to occupy.

**Ma et al. 2025** (*J Med Internet Res* 27:e68872, doi:10.2196/68872, PMID 40513092, open access;
PROSPERO CRD42024596364) systematically reviewed ML models predicting MACE from CCTA. **10 studies**,
17 models in training and 26 in testing sets. Pooled AUROC **0.7879 training / 0.7981 testing**;
logistic regression, the most common algorithm, reached 0.8229 in testing; non-LR models 0.7390;
random forests 0.8444 in training. High heterogeneity, and the authors flag the small number of
studies as a limitation.
*Licenses:* the performance figure any predictive claim in this thesis is measured against — roughly
AUC 0.80 from CCTA-derived features — and the evidence that the field's machine-learning effort on
CCTA is **radiomics of plaque**, not geometry of the tree. Every model in the review takes plaque
texture and morphology as input.

**Kim et al. 2025** (*Radiol Artif Intell* 7(3):e240459, doi:10.1148/ryai.240459, PMID 40202417),
**n = 408** emergency-department chest-pain patients across three institutions, deep-learning
classification into no / non-obstructive / obstructive CAD, 63 MACE (15.4%) at follow-up. Adding the
DL CAD-extent classification to clinical risk factors raised Harrell's C from 0.80 to 0.94
(p < 0.001), with obstructive CAD carrying HR 88.07.
*Licenses:* included as a caution rather than a result. A hazard ratio of 88 estimated on 63 events
is not a biological effect size, and quoting it uncritically is the kind of borrowed-from-the-abstract
number the writing skill bans. It is a useful example of how CCTA deep learning is currently
evaluated, and a reason this thesis should report interval width and calibration alongside any
point estimate.

## Stage 3 — does geometry alone carry the signal, without the flow simulation?

This is the question that decides how much weight objective 7's features can bear, and
`literature.md` Axis 5 left it open: the mechanism runs through wall shear stress, but computing
shear needs a CFD simulation this thesis will not run. **The answer, as of 2026, is yes — at lesion
scale, and demonstrated on a real cohort.**

**Griffo et al. 2026** (*Comput Biol Med* 205:111583, doi:10.1016/j.compbiomed.2026.111583,
PMID 41747562) reconstructed **1078 coronary arteries from 748 patients** from invasive angiography,
computed time-averaged wall shear stress by transient CFD as reference labels, and trained a
gauge-equivariant mesh graph convolutional network (GEM-GCN) to estimate WSS **from the geometry
alone**. Output in **< 5 s per vessel**. Lesion- and vessel-averaged WSS was slightly underestimated:
absolute error 0.48 Pa [IQR 0.26–0.78], percentage error 23.6% [14.8–42.6]; spatial agreement on
high-WSS regions Dice 0.88 [0.81–0.92], and 0.84 [0.71–0.90] under a clinical rather than random
split. After normalization by vessel-averaged WSS the correlation with CFD lesion-averaged WSS rose
from **R = 0.67 to R = 0.89 (p < 0.0001)**. Critically, **lesion-averaged WSS and the
lesion-to-vessel WSS ratio predicted myocardial infarction equally well whether computed by CFD or by
the network**.
*Licenses:* the strongest single justification in this pass for extracting geometric features at all.
The shear field is recoverable from shape, so a geometric feature is not a crude proxy for
hemodynamics — it carries most of the information, and the prognostic content survives the
substitution. Two limits must travel with the claim: it is **lesion-scale, single-vessel**, not
tree-scale, so it licenses the premise and not the method; and the jump from R = 0.67 to R = 0.89 on
normalization says the **relative** shear pattern transfers while the absolute level does not. That
is a concrete design instruction for objective 7 — define features as ratios and within-tree z-scores
rather than absolute quantities.

Supporting work in the same line, noted and not fetched: physics-informed graph neural networks for
real-time WSS in stenotic coronaries (*Sci Rep* 2026, doi:10.1038/s41598-026-47410-z); TAWSS
prediction across morphological variants of bifurcations (PMC11920710); and Gharleghi, Samarasinghe,
Sowmya & Beier's ISBI 2020 paper (doi:10.1109/ISBI45749.2020.9098715) as the earliest of the line.

## Stage 4 — learned shape: where the state of the art actually sits

**Shen et al. 2026**, *The Anatomy of Coronary Risk: How Arterial Geometry Shapes Coronary Artery
Disease Through Blood Flow Haemodynamics* (*Arch Comput Methods Eng*,
doi:10.1007/s11831-026-10530-w) is the review this thesis has been missing. Author list includes
Wentzel, Morbiducci, Chatzizisis, Serruys and Beier — the groups behind most of Axis 5 — and it
carries **311 references**. It reviews the hemodynamic effect of coronary anatomy, imaging and
computational analysis methods, then names the persisting gaps, closing on the need to understand CAD
mechanism "in individuals representative of large populations".
*Licenses:* two things. It is the review that can relieve `rampidis2022geometry` of carrying §5 and
§6 alone — the writing skill flags both sections as single-source, and this is a 2026 review of the
same causal argument by the primary groups. And its stated future direction, mechanism in individuals
representative of large populations, **is objective 8 stated by the field**, which is the citation
that makes the thesis's framing not merely our own opinion. Not read; 311 references also make it
the best route into the primary literature for the rest of the chapter.

**Sun et al. 2026**, AngioGraphCAD (*Med Image Anal* 112:104079, doi:10.1016/j.media.2026.104079;
preprint doi:10.21203/rs.3.rs-4344029/v1) is the **nearest competitor found in this pass**. A graph
neural network over lesion geometry features, with masked attention fusing multiple stenoses,
predicting future cardiovascular events at both lesion and patient level from invasive coronary
angiography; evaluated on two cohorts at lesion level and one at patient level, reported as
outperforming clinical measures. Their own claim: *"the first study that highlights the importance of
geometry information in advancing future events prediction from invasive coronary angiography."*
*Licenses:* §4 must cite this or its novelty claim is not credible. The differences that keep
objectives 7–10 distinct, stated plainly: invasive angiography rather than CCTA; the geometry of
**stenoses** rather than of the tree; supervised event prediction rather than population description
or unsupervised outlier detection. It strengthens the premise this thesis rests on — geometry carries
prognostic information — while occupying a different problem.

**Sharp, Betts & Banerjee 2026** (*J R Soc Interface* 23(235):20250785, doi:10.1098/rsif.2025.0785,
PMID 41759183) is a narrative review of statistical shape modeling across cardiovascular disease:
landmark methods through point distribution models, PCA for dimensionality reduction, and
**compactness, generalization and specificity** as the standard evaluation metrics for a population
shape model.
*Licenses:* the method reference if objective 9 takes the shape-model route, and the vocabulary for
arguing that a population model is adequate. Note what it does *not* contain: the review spans
cardiovascular disease and the coronary **tree** is not among its subjects — the SSM literature is
chambers and ventricles. Consistent with `literature.md` Axis 4.

**Yaseliani et al. 2025** (*J Biomed Inform* 167:104846, doi:10.1016/j.jbi.2025.104846,
PMID 40360137) is recorded to prevent a category error. It predicts long-term CAD mortality with a
5-layer GCN reaching 93.02% recall and 89.42% NPV — but its graph has **patients as nodes**, linked
by propensity-matched causal features. No artery is modelled.
*Licenses:* "graph neural network for coronary artery disease" in this literature usually means a
patient-similarity graph or a segment-labelling graph (`literature.md` Open leads: EAGMN, HAGMN-UQ),
not a model of the tree's topology. §4 should make that distinction explicitly, because it is most of
the apparent competition.

Noted, not fetched: CORA, generalizable CAD assessment from CCTA by pathology-centric representation
learning (arXiv:2603.24847); a structure-aware dual-graph risk prediction network for coronary
stenosis (*Biomed Signal Process Control*, 2026).

---

## Stage 5 — the adversarial pass: what would break the argument

### 5.1 The measurement error is the same size as the biological effect

**Givehchi et al. 2018** (*Phys Med* 45:198–204, doi:10.1016/j.ejmp.2017.09.137, PMID 29373248)
fabricated **nine phantoms** with known bifurcation angles from 55.3° to 134.5°, imaged them by CCTA,
and measured the LAD–LCx angle by multiplanar reformation (MPR) and by volume rendering (VRT). Mean
absolute error against the true angle: **MPR 2.4° ± 2.2°, VRT 3.8° ± 2.9°**. Applied to **50 clinical
CCTA cases**, the two techniques disagreed **with each other by 12.0° ± 10.6°**.
*Licenses:* **the most important number in this pass.** Juan et al.'s disease gradient spans
75.5° → 87.3°, about 12°, from normal arteries to significant stenosis. Two accepted measurement
techniques applied to the same real patients disagree by that same 12°. The published angle–disease
association is therefore only as real as the measurement protocol behind it, and any angle this
thesis reports must come from a single, automatic, deterministic definition computed on the
centerline — not from a manual reformation. It is also the argument for objective 6's reliability
study existing at all: without a measurement-error figure of our own, none of our angle numbers can
be interpreted.

**Cui et al. 2017** (*PLoS ONE* 12(3):e0174352, doi:10.1371/journal.pone.0174352, PMID 28346530,
open access) is a third independent replication of the angle–stenosis association and adds a
phenotype result. **n = 106** patients with both CCTA and invasive angiography within three months,
318 bifurcation angles and 126 vessels. The LAD–LCx angle was significantly larger where stenosis was
≥ 50%, and significantly **wider in the non-calcified than the calcified plaque group**; it was an
independent predictor of significant left coronary stenosis, **OR 1.423 (p = 0.002)**, with ROC
sensitivity 66.7%, specificity 78.4%, PPV 85.2%, NPV 55.8%.
*Licenses:* it fills the tree-geometry × plaque-phenotype cell nothing else in the pass fills, and it
gives the angle's honest discrimination — 67% sensitive, 78% specific on its own. That supports
treating bifurcation angle as a **population descriptor**, which is objective 8, and not as a
diagnostic test.
*To verify in full text:* the inter-observer ICC of 0.963 (0.946–0.975) and intra-observer 0.993
(0.989–0.995) attributed to this study in search results do **not** appear in its abstract. Confirm
before quoting.

### 5.2 Reverse causation — the geometry is not fixed while the disease develops

**Glagov et al. 1987** (*N Engl J Med* 316(22):1371–1375, doi:10.1056/NEJM198705283162204,
PMID 3574413) examined histologic sections of the left main coronary artery in **136 hearts at
autopsy**. The internal elastic lamina area correlated with lesion area (**r = 0.44, p < 0.001**) —
arteries enlarge as plaque grows. Lumen area did **not** decrease while the lesion occupied up to
**40%** of the internal elastic lamina area, then fell sharply above it (**r = −0.73, p < 0.001**).
*Licenses:* the primary source for the caveat that governs this whole thesis. Every ImageCAS-X
centerline and surface is derived from a **lumen** segmentation, and the lumen has already been
reshaped by the disease we would predict from it. Glagov makes it quantitative: below 40% lesion area
the lumen is preserved, so early disease is nearly invisible to lumen geometry, while advanced
disease deforms it — so a cross-sectional geometry–disease association is partly the disease writing
its own predictor.
**This also repairs `literature.md`.** Axis 5 states the circularity for lesion-scale WSS — "the
plaque deforms the lumen from which the shear is computed" — with no citation. Glagov 1987 is that
citation.

**Kwon et al. 2022** (*Sci Rep* 12(1):4932, doi:10.1038/s41598-022-09062-7, PMID 35322148,
open access) is the only longitudinal vascular-geometry study found. **n = 177** subjects with
contrast-enhanced carotid MRA at baseline and again after a mean **130.2 ± 8.1 months**; mean age at
follow-up 70.7 ± 10.6 years, 40.1% male. Bilateral **bifurcation angle**, common carotid diameters
and common carotid areas all increased significantly over the decade (**p < 0.001**); maximum
diameter and internal carotid area did not change.
*Licenses:* transfers as a warning, not a result — carotid, not coronary. Bifurcation angle **drifts
upward with age**, so a cross-sectional finding that wide angles accompany disease is partly a
finding that both accompany age. Every angle analysis in this thesis must adjust for age. It is also
the published precedent for objective 6's repeat-scan study: CGPS's repeat scans make the coronary
version of exactly this measurement possible, and no one has reported it.

### 5.3 The measurement standard to check our definitions against

**Nieman et al. 2024**, the SCCT expert consensus on quantitative CCTA (*J Cardiovasc Comput Tomogr*
18(5):429–443, doi:10.1016/j.jcct.2024.05.232, PMID 38849237, open access), defines standards for
performing and reporting quantitative coronary measures on cardiac CT.
*Licenses:* the document objective 7's feature definitions should be checked against, so our numbers
are comparable to the clinical literature and not only to themselves. Note that it is framed around
**plaque and stenosis** quantification; whether it defines any tree-geometry measure at all is a
full-text question, and if it does not, that absence is itself citable evidence for the gap.

### 5.4 What the adversarial pass did *not* find

No null result or failed replication was found for the **bifurcation angle** association — five
cohorts, one direction. The vulnerabilities there are measurement (§5.1) and confounding by age, sex
and BMI (Temov & Sun; Kwon), not contradiction. For **tortuosity** and **dominance** the
contradictions are in §1.2 and §1.3 and are substantial. **Not found, and still open:** the source
for §6's claim that "curvature has been reported as higher in atherosclerotic than in
non-atherosclerotic segments" — this pass did not locate its origin, so the claim remains
unsupported by anything but `rampidis2022geometry`.

---

## Stage 6 — synthesis

### The evidence matrix, filled

Cells give the studies found in this pass, with n. **Empty means no study was found**, and the
queries behind each are in the search record.

| | CAD present / extent | Plaque phenotype | Progression | Ischemia | Events / mortality |
|---|---|---|---|---|---|
| **Tree scale** — bifurcation angle, dominance, branch presence | Temov 196; Cui 106; Mansouri 122; Juan 313; Zhang 200; Bekirçavuşoğlu 1380 | Cui 106 (wide angle ↔ non-calcified); Bekirçavuşoğlu 1380 (RI ↔ mixed plaque) | *(empty)* | *(empty)* | Tommasino 499 (LMBA > 80°, HR 4.47); dominance: Veltman 1425, Gebhard 6382 (null), Khan 255,718 (OR 1.27) |
| **Vessel scale** — tortuosity, curvature, taper | Groves 1221 (**inverse**); Zebić Mihić 131 and 160 | *(empty)* | *(empty)* | Zebić Mihić 160 (territory-matched) | *(conference abstract only: CArTI)* |
| **Lesion scale** — lumen and plaque shape, radiomics | Ma 2025 review, 10 studies | the bulk of the field | Stone 2012 (Axis 5) | Griffo 748 (WSS from shape) | Griffo 748 (MI); Sun 2026 (events); Kim 408; Ma 2025 (AUC ≈ 0.80) |

Three things fall out of the table:

1. **The field's mass is in the bottom row.** Lesion-scale plaque shape is where the cohorts, the
   machine learning and the outcome evidence are. Tree-scale geometry is studied in cohorts one to
   two orders of magnitude smaller, against softer endpoints.
2. **Two tree-scale cells are simply empty** — progression and ischemia. Nobody has asked whether
   baseline tree geometry predicts who progresses, which is what `ThesisPlan.md` weeks 11–14 propose.
3. **No cell in the table contains a population-distribution study.** Every entry is a group
   comparison or a supervised predictor. Treating tree geometry as a distribution and flagging its
   tails — objective 9 — remains unoccupied, and this pass, run on entirely different queries from
   `literature.md`'s, **independently reproduces its Axis 4 conclusion.**

### The features, ranked by the evidence behind them

| Rank | Feature | Evidence | What it licenses |
|---|---|---|---|
| 1 | **Bifurcation angle** | 5 independent CCTA cohorts (n = 106–499), consistent direction, one MACE study, one phantom accuracy study | Extract it. Define it automatically on the centerline — §5.1 makes a manual definition indefensible. Report by sex and adjust for age. |
| 2 | **Dominance** | Largest evidence base in the pass, but conditional: OR 1.27 in ACS (n = 255,718), null in stable CCTA (n = 6382), HR 6.45 with left main disease | Keep §6's decision to stratify by it rather than report it alone — now supported by three sources, not one. Ground truth is in `Descriptors.xlsx`. |
| 3 | **Tortuosity** | Direction depends on endpoint (inverse with obstructive, positive with non-obstructive) and on measurement definition | Extract as a **continuous index**, not the clinical bend count (Zebić Mihić 2023b). Report against non-obstructive disease specifically. |
| 4 | **Branch presence (ramus intermedius)** | n = 1380 supports, n = 200 propensity-matched does not | The cleanest natural experiment our data supports: `IM` is label 8, and the angle contrast is published. State as a geometric mediator, never a risk factor. |
| 5 | **Ostial take-off angle** | None for normally arising arteries (§1.5) | Do not claim it. Record the empty cell. |
| 6 | **Branch count / branching pattern** | None found, in this pass or in `literature.md` | Confirms §6's closing sentence. This is the descriptive-only territory objective 8 occupies. |

### The gap, stated for §4

The mechanism from shape to plaque is settled at lesion scale, and as of 2026 the shear field is
recoverable from geometry alone with prognostic content intact (Griffo). Individual tree-scale
features — bifurcation angle, dominance, tortuosity, branch presence — each have a small evidence
base pointing in a consistent direction. The outcome cohorts that could test them at scale exist and
are already published, including the one this project moves to (Fuchs, n = 9533). What does not exist
is the join: **no study measures tree-scale geometry across a population of thousands, describes its
distribution, and asks which individuals fall outside it.** The field's machine learning went to
plaque radiomics instead, and its graph neural networks model patient similarity or segment labels
rather than tree topology.

### Read in full, in this order

1. **Griffo 2026** — licenses the whole feature-extraction premise; check whether the normalization
   result generalizes beyond single vessels.
2. **Shen 2026** — the anchor review for §4, and 311 references into the primary literature.
3. **Sun 2026 (AngioGraphCAD)** — the nearest competitor; the novelty claim must be written against it.
4. **Bekirçavuşoğlu 2026** — the hypothesis most directly testable on our 800 cases.
5. **Tommasino 2024** — the only tree-scale outcome study; verify the HR 4.47 interval (§1.1).
6. **Gebhard 2015** — the null that §6's dominance paragraph has to answer.
7. **Zebić Mihić 2023b** — decides how objective 7 defines tortuosity.
8. **Givehchi 2018** — sets the measurement-error floor for objective 6.

### Repairs this pass licenses in the thesis (no `.tex` edited here)

1. **§6 dominance** — add `gebhard2015dominance` (null, n = 6382) and `khan2016dominance`
   (OR 1.27, n = 255,718). Restate as a conditional effect. This alone removes the sole-source
   dependence flagged by the writing skill.
2. **§6 tortuosity** — add the inverse association with obstructive disease (`groves2009tortuosity`)
   and the measurement-definition result (`zebicmihic2024index`).
3. **§6 bifurcation angle** — attach a population to the floating "76.4° ± 16.7°", or replace it with
   Temov & Sun's 79.40° ± 22.97° over n = 196, which carries its cohort.
4. **§6, new sentence** — the 12.0° ± 10.6° between-technique disagreement (`givehchi2018phantom`)
   against a 12° biological gradient.
5. **§5 and §6 single-source** — `shen2026geometry` is a 2026 review of the same causal argument by
   the primary groups, and citing it lowers `rampidis2022geometry`'s share below the one-third bar.
6. **§5 or §3** — `glagov1987remodeling` for the reverse-causation caveat; it also supplies the
   missing citation in `literature.md` Axis 5.
7. **Still open** — the origin of §6's curvature claim was not found (§5.4).

### Cross-references to `literature.md`

- **Updates Axis 5:** Griffo 2026 answers the question Axis 5 left open — geometry alone suffices to
  recover the shear field, with MI-prediction performance preserved.
- **Supplies a missing citation to Axis 5:** Glagov 1987 for the plaque-deforms-the-lumen circularity.
- **Independently confirms Axis 4:** reached from different queries, no population-distribution or
  outlier study of coronary tree geometry was found.
- **No contradiction found** between this pass and `literature.md` on any point.

---

## Added to `thesis/refs.bib`

One dated section, `% ==== geometry as a predictor of CAD`, 22 entries, all
`[BIBLIOGRAPHY VERIFIED]`. Every DOI was checked to resolve at Crossref;
`groves2009tortuosity` has none issued.

`temov2016bifurcation` · `mansouri2024bifurcation` · `tommasino2024clap` ·
`groves2009tortuosity` · `zebicmihic2024index` · `gebhard2015dominance` · `khan2016dominance` ·
`bekircavusoglu2026ramus` · `zhang2023ramus` · `fuchs2023cgps` · `griffo2026wss` ·
`shen2026geometry` · `sun2026angiographcad` · `sharp2026ssm` · `givehchi2018phantom` ·
`cui2017bifurcation` · `glagov1987remodeling` · `kwon2022carotid` · `nieman2024scct` ·
`ma2025mlmace` · `kim2025dlmace` · `yaseliani2025gnn`

Nothing under `thesis/` was edited in this pass. The repairs these entries enable are listed in
Stage 6.

## Not searched, for a later pass

- **Repeat-scan reproducibility of imaging-derived vascular measurements** — still open from
  `literature.md`. Kwon 2022 is the nearest thing found here and it is carotid MRA over ten years,
  not repeat CCTA. Objective 6's reliability study needs its own pass.
- **Coronary vessel taper and Murray-law deviation as predictors** — `taylor2024murray` gives the
  exponent, but no study relating deviation from it to disease was searched for.
- **Sex differences in coronary geometry** — three papers in this pass report a sex effect
  (Temov & Sun, Groves, Kwon) and none of them is about sex. Worth a dedicated query.
- **CArTI** (AI-informed Coronary Artery Tortuosity Index predicting 5-year MACE) is an AHA 2025
  conference abstract, doi:10.1161/circ.152.suppl_3.4365988; the publisher returned HTTP 403 and its
  numbers were not retrieved. It is the only vessel-scale-to-events entry in the matrix and should be
  chased if a full paper appears.
