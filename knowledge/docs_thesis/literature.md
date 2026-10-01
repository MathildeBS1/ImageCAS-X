# Literature search record — objective 4 and the objective-9 gap

**Passes:** 2026-09-05 (Axes 1--4), 2026-09-06 (Axis 5). **Branch:** `clean_version`.
**Status:** eleven papers selected and bibliographically verified; **none read in full yet.**

This file is a working record, not thesis prose. Its job is to make the state-of-the-art claims —
and especially the objective-9 gap claim — auditable: every citation traces to a DOI, and every
"nothing exists" claim names the queries that came back empty. The `week1` branch had a file of this
name; it is not being restored, and this is a fresh pass with its own searches.

Corresponding BibTeX keys are in `thesis/refs.bib` under `segmentation & topology state of the art`,
all marked `[BIBLIOGRAPHY VERIFIED]` — fields confirmed against Crossref, claims not yet checked
against full text. Promote to `[VERIFIED]` only after reading.

---

## Search record

Queries run this pass, and what came back.

| Query | Outcome |
|---|---|
| coronary artery tree topology graph features CTA population study 2025 | Graph-labelling methods (GNN, graph matching) and clinical variant-prevalence studies. Surfaced the Medrano-Gracia atlas. |
| computational atlas of normal coronary artery anatomy | Medrano-Gracia 2016 + 2017 companion + 2014 MICCAI construction paper; Coronary Atlas resource. |
| state of the art DL coronary artery segmentation centerline extraction review 2025 2026 | Qiu 2025 (MedIA); one-stage multitask seg+centerline; prior-knowledge/VAE centerline framework; bridging-centerline integration. |
| anomaly / outlier detection vascular tree morphology population distribution | **Nothing coronary-specific.** Generic ML tooling (isolation forest, LOF, z-score), one vessel-attribute patent, one MST-based outlier method on unrelated medical data. |
| normative coronary geometry CCTA bifurcation angle tortuosity large cohort 2023–2025 | Nannini 2024 (APL Bioeng); 2025 bifurcation scoping review; Medrano-Gracia again. No newer normative atlas found. |
| coronary semantic labeling GNN centerline tree 2025 benchmark | EAGMN, HAGMN-UQ, multi-resolution GCN labelling. All 2023–2024, all *predicting* segment labels. |
| topology-aware segmentation clDice / persistent homology / Betti loss | clDice (CVPR 2021) as the foundation; Betti-matching / TopoNet as the successor line. |
| retinal vascular topology biomarkers UK Biobank | QUARTZ tortuosity/calibre measures, fractal-dimension "vascular complexity", Reti-CVD. The methodological analogue in a different organ. |
| coronary topological features outlier / extreme value / anomaly population cohort CCTA | **Only clinical-categorical "coronary anomaly"** — anomalous origin/course/termination. See Axis 4. |
| PREDICTION study low endothelial shear stress plaque progression (2026-09-06) | Stone 2012 PREDICTION; Samady 2011; Yamamoto 2017; Bajraktari 2021 meta-analysis on *high* WSS. See Axis 5. |
| coronary bifurcation angle plaque formation scoping review (2026-09-06) | Murasato 2022 (PLOS ONE) and Shaikh 2025 (IJCI) — the two scoping reviews. See Axis 5. |
| coronary tortuosity wall shear stress mechanism (2026-09-06) | Kahe 2020 narrative review; CFD studies of tortuosity-induced low-WSS zones. See Axis 5. |

The 2026-09-06 pass covered the first of the two gaps left open above — coronary CFD/WSS from
patient-specific geometry, objective 7's hemodynamic link — and its results are Axis 5; the three
queries are the last three rows of the table.

Still not searched, and worth a later pass: repeat-scan reproducibility of imaging-derived vascular
measurements (objective 6's reliability study, Track B).

---

## Axis 1 — coronary segmentation, state of the art

The benchmark we already own is `bransby2026imagecasx`: CAS-Net at DSC 91.2, HD95 2.99 mm,
clDice 93.3, β_err 1.9, against an inter-observer ceiling of DSC 92.8. Two external papers position
it.

**Nannini et al. 2024** (`nannini2024characterization`, APL Bioengineering 8(1):016103,
doi:10.1063/5.0181281, open access as PMC10807932) is the closest published analogue to this
project's Track A, and the single most useful paper of the four. Cascaded deep learning — 2.5D
multi-view U-Net followed by 3D refinement, Dice 0.896, mean surface distance 1.027 mm — then VMTK
centerline extraction, then geometric characterization, then stratification by cardiovascular risk
factor. n = 281 CCTA from a single centre (Centro Cardiologico Monzino, Milan), 238 train / 43 test,
76% male, mean age 65.3 ± 9.6. Runtime ~5 min/patient against ~1 h of manual review.

What to take from it: three operational tortuosity definitions — a local arc-length-to-chord ratio
over 1 cm reference arcs, a direction-change tortuosity angle, and the clinical tortuosity score
(count of branches with ≥3 bends exceeding 45°, the same score `zebicmihic2023tortuosity` uses) —
and a proximal/medial/distal zoning by normalized geodesic distance from the ostium. Objective 7
needs an along-vessel parameterization; adopting theirs makes our numbers comparable to a published
cohort instead of only to themselves. Their headline finding is a negative correlation between
tortuosity and calcific plaque volume, with calcium decreasing and tortuosity increasing distally.

What it does **not** do, which is the gap this thesis occupies: no bifurcation angles, no dominance,
no graph or tree model of coronary topology, no outlier detection. Their own stated limitations are
single-scanner training data and a 43-case test set.

**Qiu et al. 2025** (`qiu2025topology`, Medical Image Analysis 103:103578, doi:10.1016/
j.media.2025.103578, preprint arXiv:2504.01597) is current state of the art on the failure mode that
matters most here: predictions that are locally accurate but **disconnected**. Three stages — a
centerline-enhanced segmentation loss; a regularized-walk reconnection of broken segments using
combined distance and direction similarity; implicit-neural reconstruction of missing vessels. Dice
88.53 (ASOCA) / 85.07 (PDSCA), HD 1.07 / 1.63 mm.

Stage 2 is the part to read closely. A disconnected prediction does not merely lower a score in this
pipeline — it yields a *wrong tree*: extra components, spurious termini, missing bifurcations, and
therefore corrupted branch counts and angles. That makes reconnection a candidate post-processing
step for the CGPS ground-truth-free inference path (`ThesisPlan.md` weeks 5–6, per-scan connectivity
quality control), where there are no labels to catch the failure. Caveat: ASOCA and PDSCA, not
ImageCAS, so the numbers are not comparable to our CAS-Net baseline and adoption needs
re-benchmarking on our 160 test cases.

Noted, not selected: a VAE-based centerline-prior framework (PMC12082760, 2025), a one-stage
multitask segmentation-plus-centerline network with hybrid conv/graph layers (MDPI J. Imaging 11(7)
:209, 2025), and bridging-centerline integration (Springer, 2026). All address the same connectivity
problem as Qiu with less coverage.

## Axis 2 — topological and geometric description of the coronary tree

**Medrano-Gracia et al. 2016** (`medranogracia2016atlas`, EuroIntervention 12(7):845–854,
doi:10.4244/EIJV12I7A139, PMID 27639736) remains the reference normative description of coronary
bifurcation geometry, and no newer atlas turned up in this pass. Computational atlas over n = 300
CCTAs selected for zero calcium score and no stenoses, enabling automatic quantification of 3D
angles, diameters and lengths across the tree. Reported: left main diameter 3.5 ± 0.8 mm, length
10.5 ± 5.3 mm; left main distal bifurcation angle 89 ± 21° with an intermediate artery versus
75 ± 23° without (p < 0.001); analogous tabulations for LAD/diagonal, LCX/OM and the right crux.

Two things to take. First, their 3D bifurcation-angle definition — objective 7 needs one that
survives the σ = 0.5 mm Gaussian smoothing baked into the delivered ImageCAS-X centerlines. Second,
the reporting shape: a population as a distribution, not a mean, which is what objective 8 wants.

The caveat must be stated wherever their numbers are used for comparison: theirs is a
**healthy-selected** cohort (zero calcium, no stenosis), whereas ImageCAS-X is 388/800 with CAD per
`Descriptors.xlsx`. Their RI-versus-no-RI angle split also intersects our `IM` label directly, giving
an external check on the intermediate-artery subgroup once `topology/graph.py` is rebuilt.

Companion, same cohort, more depth on the shape modelling: `medranogracia2017bifurcation`
(J. Cardiovasc. Transl. Res. 10(1):82–90, doi:10.1007/s12265-016-9720-2), plus the earlier MICCAI
construction paper (PMID 25485418). Public resource: the Coronary Atlas (coronaryatlas.org, UNSW
Sydney Vascular Modelling Group).

## Axis 3 — topology-aware learning

**Shit et al. 2021** (`shit2021cldice`, CVPR 2021, pp. 16555–16564,
doi:10.1109/CVPR46437.2021.01629, preprint arXiv:2003.07311) is background reading that cannot be
skipped: `bransby2026imagecasx` Table 2 reports clDice and β_err alongside DSC and HD95, and this is
the paper that defines the first and motivates the second. Soft-clDice makes the measure
differentiable via a soft morphological skeleton (iterated min/max pooling), with a proof of topology
preservation up to homotopy equivalence for binary 2D and 3D segmentations. Evaluated on five public
datasets spanning vessels, roads and neurons in 2D and 3D — general-purpose, not coronary-specific.

Its homotopy argument is also the premise of this thesis: two segmentations can share a Dice score
and carry completely different trees, so a volumetric overlap metric cannot certify a topological
feature extracted downstream.

Successor line, noted for completeness: persistent-homology losses — TopoNet first, then efficient
Betti matching (arXiv:2407.04683), which reports large gains on Betti-matching error over Dice-only
training. Heavier to compute than clDice and not yet standard for coronary work.

**How Axis 3 and Qiu divide, for week 5.** clDice changes what the network optimizes; Qiu adds
explicit repair after it. They compose rather than compete, which is why `ThesisPlan.md` week 5's
"method from the literature review chosen to address them" can reasonably draw on both, once week 3
says which failure modes actually appear in the delivered weights.

## Axis 4 — objective 9, outlier and extreme-value detection

`CLAUDE.md` records the `week1` finding — no coronary-specific paper doing outlier or extreme-value
detection on topological features — and flags it as a lead to re-verify. **This pass is consistent
with it, with one nuance that changes how the claim should be framed.**

The coronary literature does have a well-established notion of anomaly, but it is **clinical and
categorical, not statistical**: coronary artery anomalies are defined as morphological features of
origin, course or termination occurring in under 1% of an unselected population, with CCTA
prevalences reported between 0.43% and 5.79% (PMC11172169, PMC10862035). That is a taxonomy of named
variants a radiologist recognizes. It is not the same operation as treating branching, angle and
tortuosity features as a joint distribution over a population and flagging its tails.

Neither of the two population papers above does that operation. Nannini et al. stratify by risk
factor with Mann–Whitney U and χ² tests; Medrano-Gracia et al. report normative distributions but
never use them to flag an individual. The generic-tooling search returned only method literature with
no vascular domain adaptation.

**Recommended framing:** objective 9 is the unsupervised, data-driven counterpart to an existing
clinical concept, not virgin territory. This is both more defensible and more interesting than a bare
novelty claim, and it supplies a validation handle — a method that works should rediscover known
variants without being told about them: the 11 absent-left-main cases, the 41 left-dominant and 30
codominant hearts recorded in `Descriptors.xlsx`.

The nearest methodological analogues remain in a different organ. Retinal vascular topology is
measured at population scale in UK Biobank — QUARTZ-style calibre and tortuosity, fractal-dimension
"vascular complexity", segment counts — and associated with incident cardiovascular events. Worth one
paragraph in the writeup as the transfer argument, and worth reading before designing the
objective-9 method.

**Still open.** This wants a sanity check from someone who knows the field before it carries weight
in the thesis (already listed under Open questions in `CLAUDE.md`). A pass over the CFD/WSS and
statistical-shape-model literature could still turn up a coronary paper doing something equivalent
under different vocabulary — "shape outlier", "atypical morphology", "deviation from atlas".

---

## Axis 5 — why geometry drives plaque: the hemodynamic evidence

Run 2026-09-06 to close the gap the first pass left open. All seven papers below are in
`thesis/refs.bib`, marked `[VERIFIED]` for **metadata and abstract only** — Crossref plus Europe
PMC. None has been read in full. Two of them are now cited in the thesis
(`stone2012prediction`, `bajraktari2021highwss`); the rest are background for objectives 7 and 10.

### The chain, and how good the evidence for each link is

The causal chain the thesis rests on — shape sets wall shear stress, shear drives the endothelial
response, the response produces plaque — has three tiers of evidence, and they are not equally
strong.

**Localization** is old and small-n. `asakura1990flow` (Asakura & Karino, *Circ Res* 1990;66(4):1045–1066, PMID 2317887) traced flow through **five** postmortem human coronary trees and found
plaques almost exclusively on the outer wall of the daughter vessels at bifurcations — the flow
divider clean — and along the inner wall of curved segments, exactly where flow ran slow or
recirculated and wall shear was lowest. This is the single most directly useful paper for
justifying bifurcation angle and tortuosity as features, and it is now §5's primary citation. Five
trees is a real limitation and must be quoted with the number attached.

**Mechanism** is `chatzizisis2007ess` (*JACC* 2007;49(25):2379–2393, PMID 17599600), a review: the
whole tree sees the same systemic risk factors, yet lesions form where shear is low or oscillatory,
because low shear drives endothelial gene expression toward an atherogenic phenotype. Also §5.

**Prospective human evidence** is `stone2012prediction` — the PREDICTION study (Stone et al.,
*Circulation* 2012;126(2):172–181, PMID 22723305). 506 patients with ACS treated by PCI, three-vessel
angiography plus IVUS at baseline, 374 (74%) reimaged at 6–10 months, analysed in 3 mm segments.

> **State this one carefully.** Low endothelial shear stress independently predicted the
> **secondary** endpoint (decrease in lumen area) and the exploratory endpoints. It did **not**
> predict the **primary** endpoint, increase in plaque area, which was predicted by baseline plaque
> burden. The combination of predictors gave 41% positive and 92% negative predictive value. The
> headline "low shear predicts plaque progression" is routinely overstated in citing papers.

Why it matters here: it is the closest published design to `project_plan.tex` weeks 11–14 —
*association of baseline geometry with plaque progression, at locations free of plaque at baseline*.
It also bounds that plan, because the cohort is post-ACS and stented, not a general population like
CGPS.

### Can plaque composition be predicted from geometry? Partly, with heavy caveats

This question came up while writing §3 and the thesis had no evidence either way. It does now, and
the answer is qualified.

- `samady2011wss` (Samady et al., *Circulation* 2011;124(7):779–788, PMID 21788584), **n = 20**:
  low-WSS segments showed plaque progression; high-WSS segments showed necrotic-core progression
  with fibrous-tissue regression.
- `yamamoto2017ess` (Yamamoto et al., *Circ Cardiovasc Interv* 2017;10(8):e005455, PMID 28768758),
  **25 arteries from 20 patients**, serial OCT plus CFD: low ESS predicted later evolution toward the
  high-risk plaque phenotype.

Two objections to record before either is leaned on. The samples are tiny — 20 patients each. And
the relationship is partly circular: the plaque deforms the lumen from which the shear is computed,
so local shear is in part a measurement of the plaque rather than an independent predictor of it.

Both are also **lesion-scale** CFD, not tree-scale topology. Nothing here says a bifurcation angle
or a tortuosity index predicts what a plaque is made of, and §6 should not be read as claiming so.

### Shear is not monotonic

`bajraktari2021highwss` (Bajraktari, Bytyçi & Henein, *Angiology* 2021;72(8):706–714, PMID 33535802)
pools 7 IVUS studies, 615 patients, 28,276 arterial segments, median follow-up 7.71 months. High WSS
was associated with **regression** of plaque fibrous area (WMD −0.11, 95% CI −0.20 to −0.02) and
fibrofatty area (WMD −0.09, 95% CI −0.17 to −0.01) — that is, loss of the stabilizing tissue.

So low shear builds plaque and high shear destabilizes it. Shear is not one axis from safe to
dangerous, and **a topological feature designed only to flag low-shear geometry captures one half of
the mechanism.** This belongs in the thesis's limitations, and is now one paragraph in §5.

### Feature-specific mechanism

**Bifurcation angle.** `murasato2022bifurcation` (Murasato et al., *PLOS ONE* 2022;17(8):e0273157,
PMID 35976920) — scoping review. A bifurcation splits flow into the daughter vessels and produces low
wall shear on the lateral wall alongside high shear on the carinal side. That is the mechanism behind
the angle gradient `juan2017bifurcation` measures and the CFD result `wang2024lmphenotypes` reports,
and it means angle is not an arbitrary descriptor: it sets where the two shear regimes sit.
`shaikh2025bifurcation` (Shaikh et al., *Int J Cardiovasc Imaging* 2025;42(3):505–519; 575 screened,
48 included, 1946–2025) is the CCTA-specific companion, and the route into the primary literature if
§6 ever needs to stop leaning on single studies. *(Promoted here from Open leads.)*

**Tortuosity.** `kahe2020tortuosity` (Kahe et al., *Coron Artery Dis* 2020;31(2):187–192,
PMID 31211725) — narrative review. Two *separate* routes from tortuosity to harm, which is worth
keeping distinct in the writeup: reduced perfusion pressure distal to the tortuous segment, causing
ischemia without any plaque at all; and increased and oscillatory shear promoting plaque formation.
It also ties tortuosity to aging, hypertension and elastin degradation — relevant confounders for
any CGPS population model.

### What this axis does not settle

Every paper above computes shear per lesion, by CFD on one reconstructed artery, in cohorts of tens
to a few hundred. None of them derives a **tree-scale topological** feature and tests its
distribution across a population. That is exactly where objectives 7–9 sit, so Axis 5 strengthens
rather than weakens the Axis 4 framing: the mechanism linking shape to disease is well established
at lesion scale, and the population-scale topological version of it is not.

## Open leads, noted but not read

- **Graph-based coronary semantic labelling** — EAGMN (Comput. Biol. Med., 2023, PMC11073582),
  HAGMN-UQ (arXiv:2308.10320), multi-resolution GCN labelling (PMC11095121). These *predict* segment
  labels from centerline graphs. ImageCAS-X ships segment labels, so this is not currently needed —
  but it becomes directly relevant for CGPS, where predicted trees will arrive unlabelled.
- **Persistent-homology segmentation losses** — Betti matching (arXiv:2407.04683), if clDice proves
  insufficient in week 5.
