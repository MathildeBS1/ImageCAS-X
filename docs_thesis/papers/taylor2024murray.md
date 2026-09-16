# taylor2024murray — Systematic review and meta-analysis of Murray's law in the coronary circulation

**Citation:** Taylor DJ, Saxton H, Halliday I, Newman T, Hose DR, Kassab GS, Gunn JP, Morris PD.
*American Journal of Physiology: Heart and Circulatory Physiology* 2024;327(1):H182–H190.
doi:10.1152/ajpheart.00142.2024. PMID 38787386.
**Read:** 2026-09-16 — full text via PMC (PMC11380967), including abstract, methods, results,
discussion and limitations.
**Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC11380967/
**Verdict:** Murray's cubic law does not hold empirically for coronary arteries. The pooled
flow-diameter exponent is 2.39, not 3.0. Any bifurcation feature that compares a measured quantity
against a Murray-law "optimum" must use this exponent (or state why it uses 3 instead), not the
textbook cube law.

## What they did

Systematic review and random-effects meta-analysis of every study quantifying an optimum
flow-diameter exponent for mammalian coronary arteries (Cochrane, PubMed Medline, Scopus, Embase,
searched 20 March 2023). From 4,772 screened articles, 18 studies (22 unique datasets) were pooled.

Data covered 1,070 unique coronary trees: 372 humans (826 bifurcations/arteries, across nine human
studies) and 112 animals (244 trees: 53 pigs, 44 rats, 11 mice, 4 dogs, across nine animal studies).
Imaging/measurement modality varied by study: IVUS, quantitative coronary angiography, CT
angiography, and postmortem morphometric casts. Most human studies (6 of 9) used healthy vessels
imaged during clinically indicated evaluation; one study mixed 42 healthy and 68 diseased
participants. Risk of bias assessed with the NIH quality tool, funnel plots and Egger regression.

## What they found

**Primary (only) outcome: the pooled flow-diameter exponent** across epicardial and transmural
arteries combined = **2.39 (95% CI 2.24–2.54, I² = 99%)**. This sits close to the theoretical 2.33
(7/3) derived by Kassab and colleagues from a non-cubic cost model, and far from Murray's original
cubic exponent of 3.0.

Subgroups (all still pooled with the same large heterogeneity):
- By species: humans 2.42 (2.17–2.67); animals 2.36 (2.17–2.55).
- By vessel type: epicardial 2.43 (2.25–2.61); transmural 2.21 (1.93–2.49).
- By disease status: cardiovascular disease 2.29 (2.10–2.49); healthy 2.38 (2.19–2.56).
- Sensitivity analysis down-weighting studies contributing multiple exponents from the same
  dataset: unchanged at 2.39 (2.19–2.56).

All subgroup confidence intervals overlap substantially; the paper does not claim any of these
splits is statistically distinguishable from another.

**Stated clinical implication:** using 2.39 instead of 3.0 shifts the left main minimum lumen area
threshold used in PCI decisions from the guideline 6 mm² to roughly 7.1 mm², and implies wall shear
stress is not size-invariant but scales as WSS ∝ D⁻⁰·⁷⁵.

## What the abstract does not tell you

- **The I² = 99% figure is not hidden** — it is in the abstract verbatim, so this is not a case of
  a headline number outrunning a buried caveat.
- **Two studies were near-outliers and treated cautiously.** Exponents of 1.32 and 1.18 appear in
  the pooled dataset but the authors flag them as reflecting "unexplained blood acceleration" rather
  than a true low exponent — a data-quality caveat that only appears in the limitations section, not
  the abstract.
- **The authors' own uncertainty about clinical utility is discussion-only.** The paper states
  outright that "the clinical utility of defining variations in the flow-diameter exponent for
  patient groups and vessel sizes is uncertain" — this directly qualifies the MLA-threshold
  implication the abstract otherwise states plainly.
- **This is a mixed human+animal, mixed-modality pool**, not a homogeneous CCTA-derived human
  result. 112 of 1,070 trees are animal (pig/rat/mouse/dog), and the four imaging/measurement
  techniques pooled (IVUS, QCA, CTA, postmortem cast) are not equivalent measurements of the same
  quantity, which is very likely why I² is 99%. The abstract states the number but not this
  composition.

## What it licenses

- **The core methodological point for objective 7:** if a bifurcation feature compares a measured
  radius/angle relationship to a theoretical Murray-law optimum, the reference exponent should be
  **2.39** (or the Kassab 7/3 = 2.33 it agrees with), not Murray's textbook 3.0. Citing "Murray's
  law" without this correction overstates how well-established the cube law is for coronary vessels
  specifically.
- **A citable number for the flow-diameter relationship already used qualitatively** in
  `05_hemodynamics.tex:96-97` and `week2/hemodynamics.tex:92-93` ("how much of the flow each branch
  carries is set largely by its diameter, as described by Murray's law"). Neither sentence commits to
  a specific exponent, so neither needs correction, but if either is extended into a numeric formula,
  it must use 2.39, not 3.
- **A citable, quantified statement that WSS is not diameter-invariant** (WSS ∝ D⁻⁰·⁷⁵ under the
  revised exponent), useful if `05_hemodynamics.tex`'s WSS equation discussion is extended.

## What it does NOT license

- **No angle result at all.** This paper is entirely about the flow-diameter (Murray) exponent; it
  never measures or discusses bifurcation angle. Zamir's angle-from-radius formula
  (cos θ = (r₀⁴+r₁⁴−r₂⁴)/(2r₀²r₁²)) is derived under the cubic cost model specifically; substituting
  2.39 for the exponent inside that same formula is not something this paper validates; the formula
  itself would need re-derivation under whatever cost model produces exponent 2.39. That re-derivation
  is not in this paper and was not found here.
- **Not a precise, low-variance number.** I² = 99% across species and modalities means the 2.39
  point estimate is a central tendency over very heterogeneous measurements, not a tight physiological
  constant. Any thesis use of it should carry the CI and the heterogeneity caveat, not just the point
  value.
- **Not evidence the exponent differs meaningfully by disease status or vessel size.** The subgroup
  CIs overlap; the paper does not claim disease or location changes the exponent, only that data were
  "limited" for that question.
- **Not a single coherent human-CCTA cohort.** 372 humans across nine studies and three imaging
  modalities, not a fresh, uniformly-acquired sample. Do not describe this as "measured on n = 372
  patients" without the modality and study-pooling caveat.

## Open questions

- Is there a published generalization of Zamir's angle formula for an arbitrary flow-diameter
  exponent (rather than the cubic-specific derivation)? Not addressed here; would need its own
  search before building an angle-vs-radius "optimality deviation" feature on anything but the raw
  radii and a citation to this exponent.
- Would a single-modality, single-segmentation-method sample (e.g. this thesis's own 800 CCTA-derived
  cases) show less than I² = 99% heterogeneity, i.e. is most of that heterogeneity a modality artifact
  rather than genuine physiological variability? This paper doesn't decide it, but the thesis's own
  data could serve as one more homogeneous data point if this angle is pursued.
