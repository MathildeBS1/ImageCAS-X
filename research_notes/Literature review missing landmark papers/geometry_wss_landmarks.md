# Landmark papers on geometry, haemodynamics and WSS missing from the literature review

Scope: Section 1 of the review (`sec:lit-wss`, `01_geometry_wss.tex`), checked against
`refs.bib` and the Clinical Background `sec:wss` (`background/wall_shear_stress.tex`).
Citation counts are Semantic Scholar counts fetched on 2026-11-08 through the S2 Graph API
(`paper/search/match`). Google Scholar could not be queried; its counts are usually higher, often
by 1.3 to 2 times, so treat the numbers as a ranking aid, not exact values. Abstracts were read on
PubMed (efetch) unless marked otherwise. No thesis file was edited.

What Section 1 cites now: chatzizisis2007ess, asakura1990flow, vandergiessen2009bifurcation,
gijsen2019wss, kashyap2022tortuosity, zhang2024curvature, garcha2025sensitivity,
johnston2007diameter, johnston2008sshaped, johnston2009taper. `sec:wss` also cites samady2011wss,
yamamoto2017ess, peiffer2013wss, bajraktari2021highwss, davies2009shear, chiu2011disturbed,
ku1997blood, dean1927curved, qiu2000compliant, zarins1983carotid, antoniadis2015bifurcation,
nakazawa2010pathological. In `refs.bib` but not cited in any prose: stone2012prediction (only in
`00_chapter_intro.tex` comments), sakellarios2017bifurcation (cut), malek1999shear (cited in
`sec:wss` and Methods 05d).

## Which classic haemodynamic hypothesis papers are expected, and are any missing?

### Takeaway
The origin of the low-shear hypothesis (Caro et al. 1969/1971) is missing, and Section 1 calls
Asakura and Karino (1990) "early foundational work", which a reviewer who knows the field will
read as skipping two decades. Caro 1971 is the one classic I would add; Ku 1985 is the most cited
paper of the set but its point (oscillation) is already owned by `sec:wss`, and Malek 1999 is
already in the bib.

### Ranked list (all four questions)

| Rank | Paper (full citation, DOI) | S2 cites | What it showed (one line) | In refs.bib? | Where it belongs | Judgment |
|---|---|---|---|---|---|---|
| 1 | Stone PH, Saito S, Takahashi S, et al. Prediction of progression of coronary artery disease and clinical outcomes using vascular profiling of endothelial shear stress and arterial plaque characteristics: the PREDICTION Study. Circulation 2012;126:172-181. doi:10.1161/CIRCULATIONAHA.112.096438 | 607 | 506 ACS patients, 374 re-imaged at 6-10 months: low ESS independently predicted lumen narrowing, but the primary end point (plaque area increase) was predicted by plaque burden only | Yes, `stone2012prediction`, not cited in prose | Lit review (`sec:lit-risk`, one sentence) or `sec:wss` | Must add (already in bib) |
| 2 | Caro CG, Fitz-Gerald JM, Schroter RC. Atheroma and arterial wall shear. Observation, correlation and proposal of a shear dependent mass transfer mechanism for atherogenesis. Proc R Soc Lond B 1971;177:109-159. doi:10.1098/rspb.1971.0019 | 1,473 | Early atheroma in human arteries lies at sites of low wall shear; origin of the low-shear hypothesis | No | Lit review, opening of `sec:lit-wss` (or `sec:wss`) | Must add, or drop "early foundational" from the Asakura sentence |
| 3 | Lee SW, Antiga L, Spence JD, Steinman DA. Geometry of the carotid bifurcation predicts its exposure to disturbed flow. Stroke 2008;39:2341-2347. doi:10.1161/STROKEAHA.107.510644 | 380 | CFD in 50 carotid bifurcations of 25 young adults: proximal area ratio and bifurcation tortuosity predicted disturbed-flow area, bifurcation angle did not; concludes geometry can stand in for CFD in large imaging studies | No (bijari2014flare from the same group is in the bib) | Lit review `sec:lit-wss` | Must add (best single source for the thesis premise "geometry as a surrogate for disturbed flow") |
| 4 | Friedman MH, Brinkman AM, Qin JJ, Seed WA. Relation between coronary artery geometry and the distribution of early sudanophilic lesions. Atherosclerosis 1993;98:193-199. doi:10.1016/0021-9150(93)90128-H | 81 | 15 autopsy hearts: a smaller LM branch angle went with relatively more early lesions in the proximal LAD and LCx ("geometric risk factor") | No | Lit review `sec:lit-wss`, next to Cui/Juan on the LM angle | Nice to have (only direct pathology evidence on one of the five features; small n; direction opposite to the CCTA studies) |
| 5 | Friedman MH, Deters OJ, Mark FF, Bargeron CB, Hutchins GM. Arterial geometry affects hemodynamics. A potential risk factor for atherosclerosis. Atherosclerosis 1983;46:225-231. doi:10.1016/0021-9150(83)90113-2 | 271 | Coins the "geometric risk factor" hypothesis: individual differences in arterial geometry change local haemodynamics (aortic bifurcation casts) | No | Lit review opening | Nice to have (cite Friedman 1993 or Lee 2008 instead under one source per concept) |
| 6 | Ku DN, Giddens DP, Zarins CK, Glagov S. Pulsatile flow and atherosclerosis in the human carotid bifurcation. Positive correlation between plaque location and low oscillating shear stress. Arteriosclerosis 1985;5:293-302. doi:10.1161/01.ATV.5.3.293 | 2,883 | Pulsatile carotid model vs cadaver intimal thickness: plaque thickest where mean WSS is low and oscillating (r = 0.82-0.95, 20 sites) | No (ku1997blood review and zarins1983carotid are) | Clinical background only | Nice to have (most cited paper in the field, but zarins1983carotid and chatzizisis2007ess hold its points) |
| 7 | Chiastra C, Gallo D, Tasso P, et al. Healthy and diseased coronary bifurcation geometries influence near-wall and intravascular flow: a computational exploration of the hemodynamic risk. J Biomech 2017;58:79-88. doi:10.1016/j.jbiomech.2017.04.016 | 74 | Idealised LAD-diagonal models: bifurcation angle had a minor effect on near-wall haemodynamics, curvature radius a moderate one | No | Lit review `sec:lit-wss` | Nice to have (isolated angle effect; simulation only; full text not read) |
| 8 | Zhu H, Ding Z, Piana RN, Gehrig TR, Friedman MH. Cataloguing the geometry of the human coronary arteries: a potential tool for predicting risk of coronary artery disease. Int J Cardiol 2009;135:43-52. doi:10.1016/j.ijcard.2008.03.087 | 66 | Curvature, torsion and tortuosity per segment in 67 angiographically normal LADs and RCAs (52 patients) as a first step to geometric risk factors | No | Lit review `sec:lit-measure` or Methods | Nice to have |
| 9 | Morbiducci U, Kok AM, Kwak BR, Stone PH, Steinman DA, Wentzel JJ. Atherosclerosis at arterial bifurcations: evidence for the role of haemodynamics and geometry. Thromb Haemost 2016;115:484-492. doi:10.1160/TH15-07-0597 | 238 | Review linking bifurcation geometry, disturbed flow and plaque across vascular beds | No | Either | Nice to have (one review could replace several primary studies; antoniadis2015bifurcation already holds bifurcation flow in `sec:wss`) |
| 10 | Stone PH, Maehara A, Coskun AU, et al. Role of low endothelial shear stress and plaque characteristics in the prediction of nonculprit major adverse cardiac events: the PROSPECT study. JACC Cardiovasc Imaging 2018;11:462-471. doi:10.1016/j.jcmg.2017.01.031 | 169 | Nested in PROSPECT (ACS), 145 lesions in 97 patients: low ESS (<1.3 Pa) predicted non-culprit MACE, HR 4.34 | No | `sec:lit-risk` only | Nice to have (PREDICTION holds the concept) |
| 11 | Malek AM, Alper SL, Izumo S. Hemodynamic shear stress and its role in atherosclerosis. JAMA 1999;282:2035-2042. doi:10.1001/jama.282.21.2035 | 3,813 | Most cited review of the shear hypothesis | Yes, `malek1999shear` (cited in `sec:wss`, Methods 05d) | Clinical background | Not needed in the review (already present) |
| 12 | Caro CG, Fitz-Gerald JM, Schroter RC. Arterial wall shear and distribution of early atheroma in man. Nature 1969;223:1159-1160. doi:10.1038/2231159a0 | 676 | Short letter version of Caro 1971 | No | - | Not needed if Caro 1971 is cited |
| 13 | Glagov S, Zarins CK, Giddens DP, Ku DN. Hemodynamics and atherosclerosis. Insights and perspectives gained from studies of human arteries. Arch Pathol Lab Med 1988;112:1018-1031. PMID 3052352 (no DOI) | 1,154 | Review: plaque at bifurcations, branchings and curvatures where shear is low and flow non-unidirectional | No | Background | Not needed (Malek, Chatzizisis hold it) |
| 14 | Fry DL. Acute vascular endothelial changes associated with increased blood velocity gradients. Circ Res 1968;22:165-197. doi:10.1161/01.RES.22.2.165 | 1,349 | Canine aorta: high shear damages endothelium; the competing high-shear hypothesis that Caro answered | No | - | Not needed |
| 15 | Samady H, Eshtehardi P, McDaniel MC, et al. Coronary artery wall shear stress is associated with progression and transformation of atherosclerotic plaque and arterial remodeling in patients with coronary artery disease. Circulation 2011;124:779-788. doi:10.1161/CIRCULATIONAHA.111.021824 | 829 | 20 patients, 6-month IVUS: low WSS with plaque progression and constrictive remodelling | Yes, `samady2011wss` (in `sec:wss`) | Background | Not needed in the review |
| 16 | Stone PH, Coskun AU, Kinlay S, et al. Effect of endothelial shear stress on the progression of coronary artery disease, vascular remodeling, and in-stent restenosis in humans: in vivo 6-month follow-up study. Circulation 2003;108:438-444. doi:10.1161/01.CIR.0000080882.35274.AD | 467 | First serial human ESS study, 12 arteries in 8 patients: low ESS regions developed plaque and outward remodelling | No | - | Not needed (n = 8; superseded by PREDICTION) |
| 17 | Stone PH, Coskun AU, Kinlay S, et al. Regions of low endothelial shear stress are the sites where coronary plaque progresses and vascular remodelling occurs in humans: an in vivo serial study. Eur Heart J 2007;28:705-710. doi:10.1093/eurheartj/ehl575 | 199 | 13 patients, 47 subsegments: plaque progressed in 33.3% of low-ESS vs 7.9% of higher-ESS subsegments | No | - | Not needed (n = 13; superseded) |
| 18 | Gibson CM, Diaz L, Kandarpa K, et al. Relation of vessel wall shear stress to atherosclerosis progression in human coronary arteries. Arterioscler Thromb 1993;13:310-315. doi:10.1161/01.ATV.13.2.310 | 310 | 20 segments, angiography 3 years apart, assumed flow 8 ml/s: low shear correlated with faster progression | No | - | Not needed (historical first; small, assumed flow) |
| 19 | Krams R, Wentzel JJ, Oomen JA, et al. Evaluation of endothelial shear stress and 3D geometry as factors determining the development of atherosclerosis and remodeling in human coronary arteries in vivo (ANGUS + CFD). ATVB 1997;17:2061-2065. doi:10.1161/01.ATV.17.10.2061 | 299 | One human RCA: thicker wall at the inner curve, where shear was lower | No | - | Not needed (n = 1, cross-sectional) |
| 20 | Kumar A, Thompson EW, Lefieux A, et al. High coronary shear stress in patients with coronary artery disease predicts myocardial infarction. JACC 2018;72:1926-1935. doi:10.1016/j.jacc.2018.07.075 | 173 | FAME II, 29 MI vs 29 matched controls: high WSS in the proximal lesion segment predicted MI beyond FFR | No | - | Not needed (high WSS in stenotic lesions; `bajraktari2021highwss` holds it) |
| 21 | Lee JM, Choi G, Koo BK, et al. Identification of high-risk plaques destined to cause acute coronary syndrome using CCTA and computational fluid dynamics (EMERALD). JACC Cardiovasc Imaging 2019;12:1032-1043. doi:10.1016/j.jcmg.2018.01.023 | 304 | 72 ACS patients with prior CCTA: CT-derived WSS and other haemodynamics added to plaque features for culprit lesions (C 0.747 to 0.789) | No | - | Not needed (diseased, culprit-lesion, CT-FFR software; outside a plaque-free design) |
| 22 | Cheng C, Tempel D, van Haperen R, et al. Atherosclerotic lesion size and vulnerability are determined by patterns of fluid shear stress. Circulation 2006;113:2744-2753. doi:10.1161/CIRCULATIONAHA.105.590018 | 1,035 | Mouse carotid cuff: low and oscillatory shear regions grew lesions of different phenotype; the main causal experiment | No | Background only | Not needed (mechanism; header of 01_geometry_wss.tex already lists Cheng as "not used") |
| 23 | Myers JG, Moore JA, Ojha M, Johnston KW, Ethier CR. Factors influencing blood flow patterns in the human right coronary artery. Ann Biomed Eng 2001;29:109-120. doi:10.1114/1.1349703 | 260 | One patient-specific RCA: geometric factors (curvature) dominate RCA haemodynamics over inflow conditions | No | - | Not needed (Kashyap and Johnston hold curvature) |
| 24 | Soulis JV, Farmakis TM, Giannoglou GD, Louridas GE. Wall shear stress in normal left coronary artery tree. J Biomech 2006;39:742-749. doi:10.1016/j.jbiomech.2004.12.026 | 166 | Steady CFD of one normal LCA: low WSS on the lateral walls of the LM bifurcation | No | - | Not needed (one geometry, steady flow) |
| 25 | Beier S, Ormiston J, Webster M, et al. Impact of bifurcation angle and other anatomical characteristics on blood flow: a computational study of non-stented and stented coronary arteries. J Biomech 2016;49:1570-1582. doi:10.1016/j.jbiomech.2016.03.038 | 72 | Angle changed alone in left main models (40-80 deg): minor effect on low-WSS and OSI area; diameter and tortuosity mattered more | No | - | Not needed if Chiastra (or Garcha) holds the angle; pick one |
| 26 | Wellnhofer E, Osman J, Kertzscher U, et al. Flow simulation studies in coronary arteries: impact of side-branches. Atherosclerosis 2010;213:475-481. doi:10.1016/j.atherosclerosis.2010.09.007 | 91 | Leaving out side branches distorts simulated WSS | No | - | Not needed (CFD methods; the thesis runs no CFD) |
| 27 | Wang JC, Normand SL, Mauri L, Kuntz RE. Coronary artery spatial distribution of acute myocardial infarction occlusions. Circulation 2004;110:278-284. doi:10.1161/01.CIR.0000135468.67850.F4 | 376 | 208 STEMI patients: occlusions cluster in the proximal third of the arteries | No | Discussion (segment intercepts), not Section 1 | Not needed in Section 1 |

Others checked and judged not needed for Section 1 (counts from S2): Chatzizisis 2008 Circulation
pig study (402, doi:10.1161/CIRCULATIONAHA.107.695254); Wentzel 2012 Cardiovasc Res review (357,
doi:10.1093/cvr/cvs217); Brown 2016 Nat Rev Cardiol review (258, doi:10.1038/nrcardio.2015.203);
Hahn and Schwartz 2009 Nat Rev Mol Cell Biol (1,241, doi:10.1038/nrm2596, mechanotransduction);
Hoogendoorn 2020 Cardiovasc Res, 10 FH pigs, multidirectional WSS (116, doi:10.1093/cvr/cvz212);
Corban 2014 Atherosclerosis (134); Koskinas 2009 review (131); Thomas 2005 Stroke, young vs old
carotid geometry (249, doi:10.1161/01.STR.0000185679.62634.0a); Vorobtsova 2016 (65), Malvè 2014
(68), Prosi 2004 (152); Sun and Cao 2011 Eur J Radiol LM angle on CCTA (83,
doi:10.1016/j.ejrad.2011.04.015).

### Cited Findings
- Caro 1971 (Proc R Soc B) has about 1,473 S2 citations and the 1969 Nature letter about 676; both
  predate Asakura 1990 by two decades — [S2 / PubMed 4396262](https://pubmed.ncbi.nlm.nih.gov/4396262/), [PubMed 5810692](https://pubmed.ncbi.nlm.nih.gov/5810692/)
- Caro's low-shear proposal answered Fry's 1968 high-shear endothelial-damage hypothesis (S2 about
  1,349 citations) — [Fry 1968, Circ Res](https://doi.org/10.1161/01.RES.22.2.165)
- Ku 1985: in a pulsatile carotid model compared with cadaver plaques, intimal thickness correlated
  with the reciprocal of mean WSS (r = 0.82) and with an oscillation index (r = 0.82); authors
  conclude oscillation "may enhance atherogenesis"; about 2,883 S2 citations, the most cited paper
  in this set apart from Malek — [PubMed 3994585](https://pubmed.ncbi.nlm.nih.gov/3994585/)
- Glagov 1988 (review, about 1,154 S2 citations, no DOI): plaque at "bifurcations, branchings, and
  curvatures" where "flow velocity and shear stress are reduced and flow departs from a laminar,
  unidirectional pattern" — [PubMed 3052352](https://pubmed.ncbi.nlm.nih.gov/3052352/)
- Malek 1999 JAMA has about 3,813 S2 citations and is already `malek1999shear` — [JAMA](https://doi.org/10.1001/jama.282.21.2035)
- Friedman 1983 introduced the "geometric risk factor" idea (title: "Arterial geometry affects
  hemodynamics. A potential risk factor for atherosclerosis"); PubMed has no abstract — [PubMed 6838702](https://pubmed.ncbi.nlm.nih.gov/6838702/)

### Inferences
- The phrase "Early foundational work by Asakura and Karino (1990)" is the most visible gap: either
  cite Caro 1971 before Asakura (one clause: the hypothesis that atheroma localises at low wall
  shear was first proposed from human autopsy arteries) or call Asakura "autopsy work" instead of
  "early foundational". Under the one-source rule Caro adds the origin of the hypothesis, which
  chatzizisis2007ess (a 2007 review) does not hold.
- Ku 1985 is the paper most reviewers know by name, but `sec:wss` already cites zarins1983carotid
  for the low-WSS/plaque correlation and chatzizisis2007ess for oscillation; adding Ku would
  duplicate both. If the author wants one carotid classic in `sec:wss`, Ku 1985 is a stronger choice
  than Zarins 1983 (it adds pulsatile flow and oscillation), but that is a swap, not an addition.
- Malek, Glagov 1988 and Fry are background-level and not needed in the review.

### Gaps
- Google Scholar counts could not be retrieved (no API access); S2 counts only.
- Caro 1971 full text was not read; the one-line summary is from the title and the well-known
  content of the paper, not from a fetched abstract (PubMed has none). Read it before citing.
- Friedman 1983 abstract not available on PubMed; the summary relies on the title.

## Which prospective in-vivo WSS studies belong in a review about geometry predicting plaque?

### Takeaway
One sentence citing PREDICTION (`stone2012prediction`, already in the bib) is the expected
addition; the smaller Stone 2003/2007 and Gibson 1993 studies are superseded, and Samady 2011 is
already in `sec:wss`. None of these studies starts from a plaque-free artery, which is itself
worth one clause in `sec:lit-risk` because it sharpens the thesis gap. Be careful with the PREDICTION
wording: low ESS did not predict its primary end point.

### Cited Findings
- PREDICTION: 506 ACS patients after PCI, three-vessel IVUS profiling, 374 (74%) re-imaged at 6-10
  months; "Increase in plaque area (primary end point) was predicted by baseline large plaque
  burden; decrease in lumen area (secondary end point) was independently predicted by baseline
  large plaque burden and low endothelial shear stress"; about 607 S2 citations — [PubMed 22723305](https://pubmed.ncbi.nlm.nih.gov/22723305/)
- Stone 2003: "the first experience in humans relating ESS to subsequent outcomes", 12 arteries in
  8 patients, 6-month follow-up — [PubMed 12860915](https://pubmed.ncbi.nlm.nih.gov/12860915/)
- Stone 2007: 13 patients, 47 subsegments; plaque progressed in 33.3% of low-ESS vs 7.9% of
  higher-ESS subsegments (P = 0.009) — [PubMed 17347172](https://pubmed.ncbi.nlm.nih.gov/17347172/)
- Gibson 1993: 20 arterial segments, angiography 3.0 years apart, flow assumed 8 ml/s; low shear
  correlated with progression in 15 of 20 segments — [PubMed 8427866](https://pubmed.ncbi.nlm.nih.gov/8427866/)
- PROSPECT ESS (Stone 2018): 145 non-culprit lesions in 97 ACS patients; no lesion without low ESS
  led to non-culprit MACE; propensity-adjusted HR 4.34 (1.89-10.00) — [PubMed 28917684](https://pubmed.ncbi.nlm.nih.gov/28917684/)
- Kumar 2018: FAME II, 29 MI vs 29 matched controls; higher WSS in the proximal lesion segment
  predicted MI (HR 1.234, C 0.65) — [PubMed 30309470](https://pubmed.ncbi.nlm.nih.gov/30309470/)
- EMERALD (Lee 2019): 72 ACS patients with CCTA 1 month to 2 years before ACS; adding haemodynamic
  features raised C from 0.747 to 0.789 for culprit lesions — [PubMed 29550316](https://pubmed.ncbi.nlm.nih.gov/29550316/)
- The earlier claim check already recommended PREDICTION and PROSPECT ESS for one sentence in
  `sec:lit-risk` rather than `sec:lit-wss` — local file `reports/Literature review claim check.md`

### Inferences
- PREDICTION is the expected citation: largest, prospective, coronary, in-vivo, and already in
  the bib. Suggested framing for `sec:lit-risk`: the prospective evidence that low WSS precedes
  progression comes from patients who already had disease after ACS (PREDICTION), which is the
  reverse-causality gap the section already argues. Do not write that low ESS predicted plaque
  growth in general: it predicted lumen narrowing; plaque area growth was predicted by plaque burden.
- PROSPECT ESS is the second-best choice if an event outcome is wanted, but it is a nested
  case-control of 97 patients and its outcome is MACE, not plaque; under the one-source rule it
  adds nothing PREDICTION does not hold for this thesis.
- Kumar 2018 and EMERALD concern high WSS or culprit lesions in stenotic disease; they belong
  nowhere in a plaque-free design and `bajraktari2021highwss` already holds high WSS.
- All of these studies compute WSS; none relates geometry alone to later plaque. They support the
  WSS link in the premise, not the thesis claim itself.

### Gaps
- No prospective human study was found that computed WSS in plaque-free coronary arteries and
  followed them to plaque onset; this matches the review's stated gap but was not searched
  systematically here.

## Which landmark geometry-WSS computational studies on curvature, bifurcation angle, diameter ratio and taper are missing?

### Takeaway
The most cited and most on-point missing paper is Lee, Antiga, Spence and Steinman (2008, Stroke):
it tests the thesis premise directly (geometry predicts disturbed-flow exposure between
individuals, so imaging studies can use geometry instead of CFD), and its finding that area
ratio mattered but angle did not parallels the thesis's diameter-ratio and angle features. It is
carotid, so it must be labelled as another vascular bed. The coronary computational studies
(Chiastra 2017, Beier 2016, Soulis 2006, Myers 2001, Wellnhofer 2010) are simulation-only, mostly
idealised or single-geometry and modestly cited (65-260); at most one of Chiastra or Beier is
worth adding, for an isolated angle effect. Nothing more widely cited on coronary taper was found.

### Cited Findings
- Lee 2008: CFD in 50 carotid bifurcations from MRI of 25 young adults; disturbed flow related to
  proximal area ratio (beta about 0.5) and bifurcation tortuosity (beta about -0.4), "but not
  bifurcation angle, planarity, or distal area ratio"; concludes geometric features are "robust
  surrogate markers" so large imaging studies can proceed "without the need for time-consuming and
  expensive flow imaging or CFD studies"; about 380 S2 citations — [PubMed 18556585](https://pubmed.ncbi.nlm.nih.gov/18556585/)
- Friedman 1993: 15 autopsy hearts; relative proximal sudanophilia in LAD and LCx "correlated
  negatively with LM branch angle, suggesting that a small LM branch angle may be a 'geometric risk
  factor'"; stronger for the LCx — [PubMed 7681291](https://pubmed.ncbi.nlm.nih.gov/7681291/)
- Chiastra 2017: idealised LAD-diagonal models with varied angle and curvature; "bifurcation angle
  has a minor" effect on near-wall haemodynamics while "cardiac curvature radius moderately affects
  near-wall hemodynamics" (stated for stenosed cases) — [PubMed 28457603](https://pubmed.ncbi.nlm.nih.gov/28457603/)
- Beier 2016: nine bifurcations with angles changed alone (40-80 deg); the angle "had a minor
  impact" on low-WSS and OSI area, and diameter and tortuosity "appear to have stronger effects" — [PubMed 27062590](https://pubmed.ncbi.nlm.nih.gov/27062590/)
- Morbiducci 2016 (review, about 238 S2 citations) frames bifurcation geometry as a determinant of
  disturbed flow and plaque across beds — [PubMed 26740210](https://pubmed.ncbi.nlm.nih.gov/26740210/)
- Zhu 2009 (Friedman group): 32 LADs and 35 RCAs from 52 patients with angiographically normal
  arteries; curvature, torsion and tortuosity differ by segment; >80% of geometric variability in
  two factors (curvature/tortuosity and torsion) — [PubMed 18597872](https://pubmed.ncbi.nlm.nih.gov/18597872/)
- Myers 2001: in a patient-specific RCA, geometry (curvature) dominated RCA haemodynamics — [PubMed 11284665](https://pubmed.ncbi.nlm.nih.gov/11284665/)
- Wellnhofer 2010: "Side-branches must not be neglected in numerical flow simulation" — [PubMed 20934704](https://pubmed.ncbi.nlm.nih.gov/20934704/)
- Thomas 2005: young carotid bifurcations vary less in angle and diameter ratios than older ones
  (e.g. bifurcation angle 48.5 +/- 6.3 vs 63.6 +/- 15.4 deg) — [PubMed 16224089](https://pubmed.ncbi.nlm.nih.gov/16224089/)
- Clinical CCTA on the LM angle: Sun and Cao 2011 report "a direct correlation between left
  bifurcation angle and ... formation of plaques" (small sample) — [PubMed 21543178](https://pubmed.ncbi.nlm.nih.gov/21543178/)

### Inferences
- Lee 2008 holds a concept no current source holds: that geometry can replace the flow simulation
  as a marker of disturbed flow across individuals, which is why the thesis can use geometry
  without CFD. Kashyap holds the coronary curvature version only. Adding Lee 2008 would also put
  the diameter-ratio and angle results side by side with Garcha (simulation) in a real-geometry
  sample. Skeptical notes: carotid, 25 young adults, CFD only, no plaque outcome.
- Friedman 1993 is small (15 hearts) and low-cited, but it is the only pathology study on the LM
  angle, and its direction (small angle, more proximal lesions) is opposite to the CCTA studies
  (Sun 2011, Tommasino 2024 wide angle). That conflict could be worth one sentence in the review or
  the Discussion; under the one-source rule it adds "pathology direction for the LM angle", which
  Cui and Juan do not hold.
- Chiastra 2017 and Beier 2016 say the same thing (angle effect minor, curvature/diameter larger);
  pick one at most. Garcha already shows the angle effect depends on branch widths, so adding either
  is only nice to have, and only after a full-text read.
- On taper, no paper more widely cited than the Johnston series was found in this search; the
  header of `01_geometry_wss.tex` already records a broad taper search (Javier 1995, Zubaid 2002,
  Huo 2013, Kandangwa 2022 and others).
- Gijsen 2019 (about 289 S2 citations) is already cited and is the right consensus source.

### Gaps
- Rabbi/Soulis bifurcation-angle CFD papers beyond Soulis 2006 were not looked up; they are
  likely low-cited, simulation-only studies.
- Full texts of Lee 2008, Chiastra 2017 and Friedman 1993 were not read; summaries are from
  abstracts only.
- A Semantic Scholar lookup for "Hemodynamic disturbances due to the presence of the left main
  bifurcation" and an LM-bifurcation flow-divider pathology paper failed (rate limit / no match).

## Is the van der Giessen / Asakura evidence base missing a more widely cited source?

### Takeaway
Asakura and Karino (1990, about 815 S2 citations) is already the right, widely cited autopsy
source for coronary plaque at bends and bifurcations. Van der Giessen 2009 (EuroIntervention,
about 78 S2 citations) is modestly cited; Nakazawa 2010 (JACC, about 277), already in the bib and
in `sec:wss`, is the more cited source for lateral-wall plaque at bifurcations, but it is pathology
of autopsy hearts, not imaging of living patients, so it does not replace van der Giessen's point.
No change is needed beyond adding Caro 1971 as the origin of the hypothesis.

### Cited Findings
- Asakura and Karino 1990, Circ Res: about 815 S2 citations — [doi:10.1161/01.RES.66.4.1045](https://doi.org/10.1161/01.RES.66.4.1045)
- Van der Giessen 2009, EuroIntervention: about 78 S2 citations — [PubMed 19378688](https://pubmed.ncbi.nlm.nih.gov/19378688/)
- Nakazawa 2010, JACC: about 277 S2 citations; already `nakazawa2010pathological` — [doi:10.1016/j.jacc.2010.01.021](https://doi.org/10.1016/j.jacc.2010.01.021)
- Older autopsy studies on coronary plaque location: Fox 1982 (young coronary arteries, about 111
  S2 citations, doi:10.1016/0021-9150(82)90198-8) and Svindland 1983 (LM bifurcation, about 87;
  early sudanophilic lesions start in the proximal branches and spread distally) — [PubMed 6193799](https://pubmed.ncbi.nlm.nih.gov/6193799/); Montenegro and Eggen 1968 (about 188, no DOI found)

### Inferences
- The one-source rule is satisfied as is: Asakura holds autopsy localisation, van der Giessen holds
  the in-vivo CT version, Nakazawa holds flow-divider sparing in `sec:wss`. Svindland 1983 would add
  only "lesions start proximally at the LM bifurcation", which may interest the Discussion of the
  segment intercepts, not Section 1.
- Side finding in `refs.bib`: `rampidis2022geometry` (Diagnostics 2022, vol 12(9)) carries
  doi = 10.1161/01.CIR.85.6.1987, which is a Circulation 1992 DOI and cannot belong to a 2022
  Diagnostics review. Check and correct it (not edited here).

### Gaps
- No systematic citation-count comparison of in-vivo bifurcation imaging studies was run beyond
  van der Giessen and Nakazawa.
