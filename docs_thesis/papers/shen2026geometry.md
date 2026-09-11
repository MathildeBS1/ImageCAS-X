# shen2026geometry — The anatomy of coronary risk

**Citation:** Shen C, Zhang M, Keramati H, Zhang S, Gharleghi R, Wentzel JJ, Khan MO, Morbiducci U,
Qayyum A, Niederer SA, Samant S, Chatzizisis YS, Almeida D, Tsai T-Y, Serruys P, Beier S.
*Archives of Computational Methods in Engineering* 2026. doi:10.1007/s11831-026-10530-w.
Received 26 Sep 2025 / revised 22 Jan 2026 / accepted 15 Feb 2026. © The Author(s) 2026, open access.
Volume and article number not yet assigned.
**Read:** 2026-09-07 — **full text of the published version**, 35 pages, PDF supplied by the user and
stored beside this entry. (An earlier pass on 2026-09-07 read only the arXiv preprint
arXiv:2507.17109; that pass reached one wrong conclusion, corrected below.)
**Source:** `docs_thesis/papers/The Anatomy of Coronary Risk- …pdf`
**Verdict:** The anchor review for the state of the art — the field, by the field, naming two gaps
this thesis occupies. Cite it for framing, never for a number.

## What they did

Narrative review of coronary haemodynamics and the anatomy that drives it. Six sections plus seven
tables: imaging acquisition and reconstruction; computational analysis (solvers, rheology, wall
compliance, boundary conditions); relevance of coronary anatomy to haemodynamics and pathophysiology;
current limitations and future opportunities; conclusion.

No cohort, no meta-analysis, no pooled statistic. **311 references.** Author list is the primary
groups behind most of `literature.md` Axis 5 — Wentzel, Morbiducci, Chatzizisis, Serruys, Beier.

Reusable objects: **Table 7**, reviewed in vivo and computational studies of coronary anatomy and
flow (Focus / Data / Method / Key Findings / Study), spanning three pages; **Table 6**, computed
blood flow research by flow pattern and shape factor; **Table 1**, imaging techniques with
advantages and limitations.

## What they found

A review, so "found" means "named". Section 5 states the limitations:

**The whole-tree gap, with a sharper argument than the abstract suggests.** Most studies covered
"the main bifurcation regions or non-bifurcating vessels, and most curved segments and some regions
commonly susceptible to diseases were neglected." The reason this matters, in their words:
*"vulnerable plaques are most commonly located outside the left main region. For example, SCAD occurs
in the middle to distal vessel segments. Therefore, investigating the whole tree is essential to
understanding the effect of anatomical features on haemodynamics distributions in downstream
segments with potential risks."*

**The population gap.** *"investigations about the relationship between coronary anatomy and
haemodynamics with a large population are limited. While patient-specific geometries have
increasingly been used, the limited sample size and case selection approach may undermine the
generalisability of the analyses, which consequently restricts the clinical applications of current
findings."* They recommend **power analysis** to justify sample size, and expect future studies to
use "more extensive and diverse populations".

**Named blockers** on understanding anatomy–haemodynamics correlation: computational cost, lengthy
segmentation, multiple shape factors, wide shape variation between individuals, and *"the absence of
established thresholds for haemodynamic descriptors."*

**Statistical shape analysis** is offered as the remedy for combining multiple anatomical factors —
it *"proposes an effective and practical method to analyse complex shapes and variations, generating
representative mean shapes with variations from a group of 3D coronary models [16]"* — and
*"although its application in coronary arteries has been tested [16], such analyses have valuable
potential and are worth further exploration."*

Reference [16] is **Medrano-Gracia et al. 2017**, *A study of coronary bifurcation shape in a normal
population*, J Cardiovasc Transl Res 10:82–90 — i.e. `medranogracia2017bifurcation`, already in
`refs.bib`. Reference [274] is `medranogracia2016atlas`. The heart/aorta/bone SSM examples they cite
alongside are left ventricle, ascending aorta and bone — not coronary.

Also flagged as current directions, both absent from the preprint: **AI-QCPHA** deriving ESS from
FFR-CT for lesion-level high-risk plaque assessment (EMERALD-II trial), and **radial wall strain**,
calculated from angiography, *"a promising marker for plaque composition and stability."*

## What the abstract does not tell you

- **The whole-tree argument cuts at this thesis too.** Vulnerable plaques sit mostly *outside* the
  left main, and studies concentrating on the left main bifurcation are named as a limitation. §6
  currently makes left main bifurcation angle its best-evidenced feature. That is still defensible —
  the evidence is where it is — but the thesis should say that the left main is where the literature
  looked, not where the disease mostly is.
- **The three "gaps" are two — but the third survives in the body, not only in a footnote.**
  The preprint carried a highlights list naming three, including *"more precise and consistent
  anatomical feature definitions."* The published version drops that list. **Correction to the
  2026-09-07 reading, made 2026-09-07 on a second pass:** that reading said the definitional problem
  "survives only as a footnote to a table". It does not. Section 4 carries a full body paragraph on
  it — curvature defined as the derivative of the unit tangent or as 1/R; the tortuosity index
  "cannot capture the spatial information"; clinical practice reducing both to a bend count or a 2D
  C-/S-shape; computational studies using the index, average absolute curvature, or a single bend
  "neglecting the spatiality and continuity of this characteristic" — and it ends with a specific
  recommendation, reference [214], resolved below.
- **"Large populations" means scaling up CFD.** In context, §5's future direction is more and better
  patient-specific simulation on bigger, more diverse cohorts, justified by power analysis. The words
  **outlier**, **extreme value** and **anomaly** appear nowhere in the paper (checked).
- **Narrative review, no search protocol** — no PRISMA, no inclusion criteria, no screening counts.
  "The field has not done X" cannot be sourced to it.
- One sentence in §5 is garbled by copy-editing: automated segmentation "has enabled … large-scale
  segmentation … **Therefore**, the sample sizes … were relatively small." The intended sense is
  plainly the opposite; do not quote that sentence.

## Corrections to the earlier preprint-based pass

- **311 references is CORRECT.** The preprint's highest citation number is 295; the published version
  runs to reference 311 (Schneiders et al. 2015, the final entry). The correction made in `refs.bib`
  and `find_research.md` on the preprint reading was **wrong and has been reverted**.
- **Reference [16] is resolved**: `medranogracia2017bifurcation`, not the 2016 atlas.
- The `find_research.md` query-9 correction **stands**, in a narrower form: statistical shape analysis
  has been applied to coronary **bifurcation shape**, not to whole coronary trees, and Shen calls
  further exploration worthwhile.

## What it licenses

- **§4 opening, framing:** the field names whole-tree analysis and large-scale population study as
  its own persisting gaps, so the thesis's direction is the field's stated direction.
- **§4 and §5 single-source repair:** a 2026 review of the same causal argument by the primary
  groups, relieving `rampidis2022geometry` (`find_research.md` repair 5).
- **Objective 7, tortuosity definition:** the field concedes tortuosity and curvature definitions
  overlap and that inconsistent measurement plausibly explains contradictory findings — licensing one
  explicit, justified definition. Corroborates `find_research.md` §1.2 independently.
- **Objective 7, beyond the left main:** their SCAD/distal-vessel argument licenses extracting
  features across the whole tree rather than at the left main alone.
- **Objective 8, sample size:** licenses a power justification for the cohort rather than "all 800
  because they exist".
- **Table 7** as the reading route into §4.3's primary literature.

## What it does NOT license

- **Not evidence.** No cohort, no pooled estimate, no number quotable with a population behind it.
- **Not an endorsement of objective 9.** It never mentions outlier or extreme-value detection, and
  its population framing is about larger CFD studies, not about treating features as a distribution
  and flagging its tails.
- **Not proof that coronary shape models are absent** — it says the opposite, citing
  Medrano-Gracia 2017.
- **Not a systematic review.**

## Open questions

- ~~Table 7 spans three pages of studies.~~ **Mined 2026-09-07 — see "What Table 7 yielded" below.**
- Radial wall strain is offered as a marker of plaque composition from angiography alone. Does it
  bear on the composition-from-geometry question raised in §3, or is it a wall-mechanics measurement
  that geometry cannot reach?
- "The absence of established thresholds for haemodynamic descriptors" — does that argue for or
  against objective 9's distribution-based, threshold-free framing? Probably for, but the thesis
  should make that argument explicitly rather than assume it.


## What Table 7 yielded (mined 2026-09-07)

All second-hand — the primary papers behind Table 7 have not been read. Two entries were followed to
their own records and verified against Europe PMC; both are now in `refs.bib`.

**The scale ceiling, in the field's own summary table.** Largest whole-tree geometry-and-flow study:
**39** patient-specific left coronary trees (Zhang 2023, ref [228]). Largest single-bifurcation CFD:
**127** left main bifurcations (Gharleghi 2023/2024, Kashyap 2022). Only in vivo tortuosity scoring
reaches ~1000 patients, and it counts bends on an angiogram. This is the scale gap quantified from
the review itself.

**Bifurcation angle: the CFD literature is split, and the thesis currently says it is not.**
Clinical entries agree — Temov (n = 196), Cui (n = 106), Sun and Cao (n = 30, diseased left
coronaries 94° ± 19.7° vs 75.5° ± 19.8°, p = 0.02). Computational entries do not: Beier 2016 found
**no significant effect** of angle on adverse haemodynamics; Chiastra 2017 found a **minor impact**;
Shen 2021 found a **larger angle reduced** low-shear area. Others point the expected way.
**Action required:** `thesis/state_of_the_art/05_predicts_disease.tex` line ~77 asserts "an
anatomical gradient, an outcome association and a hemodynamic mechanism pointing the same way",
resting on `wang2024lmphenotypes` alone. That overstates a split literature.

**Tortuosity: the sign depends on the level of analysis.** Patient/artery level negative or null —
Li 2011 (n = 1010, OR 0.755, 95% CI 0.574–0.994, p = 0.045, and MACE no different over 2–4 years),
Chiha 2017 (n = 870). Segment level positive — Tuncay 2018 (n = 73, 30% higher tortuosity in
plaque-bearing segments, *no significant correlation at artery level*). Several CFD entries offer
helical flow as an atheroprotective mechanism. Refines `find_research.md` §1.2, which had the
inverse association but not the level-of-analysis explanation.

**Sex is a systematic modifier.** Males 2.07× more likely to exceed 80° (Temov); tortuosity far more
common in women (Li, OR 2.603); women with severe tortuosity more often normal (Chiha); and low
shear sits on the *inner* wall of curvature in females, *outer* in males (Gharleghi 2023) — a
difference in location, not amount.

**Reference [214] resolved:** Kashyap et al. 2022, *Sci Rep* 12:865, doi:10.1038/s41598-022-04796-w
— now `kashyap2022tortuosity`. CTCA from 127 patients **without** CAD; average absolute curvature
correlated best with low TAWSS across all left main branches (p < 0.001), while **the tortuosity
index showed no significant correlation at all (p = 0.86)**. This is the source for objective 7's
choice of measure.

**New in `refs.bib` from this pass:** `kashyap2022tortuosity`, `li2011tortuosity`.
