# Introduce taper as a reasoned, untested hypothesis

The literature review should present lumen taper as **the one dimension of coronary shape that the other four model features leave out**: how the lumen narrows along each artery between its branches. It should then justify the feature with a short chain of verified premises and close by stating the untested step as the thesis's hypothesis. The premises are these. Blood leaves the main artery through its side branches, and an expert consensus states that this loss of flow "is typically accompanied by tapering of the lumen" ([Gijsen et al. 2019](https://academic.oup.com/eurheartj/article/40/41/3421/5576147)). In idealised simulations only tapered arteries showed a further low-WSS region in the straight proximal part ([Johnston and Johnston 2009](https://www.mssanz.org.au/modsim09/B4/johnston_bm.pdf)). In normal CCTA arteries, WSS was lowest where the lumen was widest, with a boundary-condition caveat ([Schultz et al. 2023](https://doi.org/10.1007/s10554-022-02739-0)). **No human study identified in these searches has tested taper against WSS or against plaque that developed later**, so the case is mechanistic, not empirical. The thesis has to say so plainly. Taper is preferred over the other candidates mostly **by elimination**. Torsion and the tortuosity index were null in human tests. Raw diameter carries sex and dominance. Distance from the ostium and left main length clash with the model design. Lumen volume to myocardial mass, eccentricity and radiomics have no WSS-to-incident-plaque evidence that fits a plaque-free population. Most of this elimination belongs in the Methods (`sec:method-selection`), not in §1. The current paragraph in `01_geometry_wss.tex` is close to right. It needs one consensus source for the flow-loss premise, a diameter contrast, a reverse-causation sentence, and an explicit hypothesis sentence. It also contains one unsourced clause ("where most plaque is found") that should go.

## The verified chain is short: flow loss, taper, low WSS

The mechanistic case rests on three sources, and each has a different strength. **Gijsen et al. 2019** is the anchor. The full text was partly read, and it is a peer-reviewed *Eur Heart J* consensus. It states that side-branch outflow "leads to a reduction of blood flow in the main vessel, which is typically accompanied by tapering of the lumen". It also says that flow divides between main vessel and side branch "mainly depending on their diameters", and that regulation by shear "plays a continuous role in the development, growth, remodelling, and maintenance of the vascular system" ([Gijsen et al. 2019](https://academic.oup.com/eurheartj/article/40/41/3421/5576147)). The same consensus lists the low-WSS sites as inner bends, ostia and lateral bifurcation walls. **It does not list taper**, so no expert review names taper as a plaque determinant. This is not yet in `refs.bib`.

**Johnston and Johnston 2009** is the only study found that compares tapered with uniform coronary-like geometry and reports WSS. It is a conference paper with rigid, idealised S-shaped models. The global WSS minimum moved to the straight proximal inlet in the tapered models, which the authors attribute "in part, to the overall taper in the artery and not only to the local curvature variation" ([Johnston and Johnston 2009](https://www.mssanz.org.au/modsim09/B4/johnston_bm.pdf)). The paper does not say that the proximal inlet is "where most plaque is found". The current sentence adds that clause without a source and should drop it.

**Schultz et al. 2023** found the lowest WSS where the lumen was widest in 349 visually normal vessels from referred patients. It imposed the same outflow on every vessel and left out the side branches, which the authors say exaggerates distal WSS. Part of the diameter gradient is therefore built into the model ([Schultz et al. 2023](https://doi.org/10.1007/s10554-022-02739-0)). The caveat already in the prose must stay.

The remaining step is an inference: an artery whose lumen narrows less than its flow falls is wide for the flow it carries and therefore has low WSS. It follows from Poiseuille scaling and mass conservation. **No paper was found that states it in those words**, and no paper links the mismatch to plaque. It may appear in §1 only in words, as the thesis's hypothesis. The formula and its arithmetic stay in Methods 05d, and the scaling exponents stay in 05c. The secondary support (side-branch sensitivity in [Vardhan et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6586809), low WSS in Kawasaki aneurysms, shear homeostasis in dog and monkey shunts) is either indirect or not verified to DOI level. It is not needed in a review paragraph.

## Calibre and reverse causation explain why the form and the baseline matter

Two further points make the case specific to this design. First, **raw diameter is a poor substitute for taper**. In normal angiograms, women's diameters were smaller than men's even after normalisation for body surface area, and dominance changed RCA and LCx calibre ([Dodge et al. 1992](https://doi.org/10.1161/01.CIR.86.1.232), abstract only; already in `refs.bib` as `dodge1992diameter`). Raw diameter therefore carries sex and dominance as well as shape. Schultz found men's WSS lower than women's even after adjustment for diameter. That a log-radius slope cancels any multiplicative size factor is a mathematical property that belongs in Methods 05d. The review needs only the contrast: taper describes how the lumen changes along the artery, not how large it is. One source partly conflicts with Dodge: the CT atlas found LM diameter differed by sex but was not related to BMI-based size ([Medrano-Gracia et al. 2016](https://doi.org/10.4244/EIJV12I7A139)). So the review should say that diameter differs by sex and dominance, not how much of the difference is body size.

Second, **in diseased arteries calibre is partly an effect of plaque**. Lumen area followed the summed distal branch length and myocardial mass, and in coronary artery disease the lumen was "diffusely 30–50% too small for distal myocardial bed size" ([Seiler, Kirkeeide and Gould 1992](https://doi.org/10.1161/01.cir.85.6.1987), abstract only, not yet in `refs.bib`). Javier et al. 1995 reports that IVUS lumen taper partly reflects differential plaque accumulation. Only its abstract was seen, through an index page, and the earlier notes misattributed its numbers to an angiographic "normal tapering" paper ([Javier et al. 1995](https://doi.org/10.1016/s0002-9149(00)80072-7)). It should stay out until the full text is read. Volume-to-mass studies show the same thing in referred, cross-sectional cohorts: low lumen volume relative to myocardial mass goes with more plaque and lower FFR ([Taylor et al. 2017](https://doi.org/10.1016/j.jcct.2017.08.001)). Together these sources make the plaque-free baseline the reason taper fits this thesis better than it fits the cross-sectional studies behind it. By Glagov remodelling, early wall thickening can leave the lumen almost intact ([Glagov et al. 1987](https://doi.org/10.1056/nejm198705283162204)). That argument is already owned by `sec:lit-risk` and should not be repeated in §1.

The same reverse-causation reading means **the sign is not fixed**. The WSS hypothesis predicts that weaker taper goes with more plaque. Diffuse disease below CT detection could steepen or flatten taper before any plaque is graded. Zubaid et al. 2002 even proposed that a departure from expected taper could mark "diseased segments that are not angiographically stenotic". That is a tiny QCA study with no outcome; only the abstract was read, it has no DOI and its PMID is 12368932 ([Europe PMC](https://europepmc.org/article/MED/12368932)). The review should state the WSS direction as the hypothesis and leave the sign question to Methods 05d, which already lists two-sided versus signed testing as open.

## Every alternative fails a test that taper passes

Taper's advantage is that it satisfies three conditions at once. It has a mechanistic WSS link, it can be measured on a plaque-free CCTA, and it overlaps little with curvature, the LM angle and the LM→LAD/LCx ratios. No alternative satisfies all three, though taper's own human evidence is also absent.

| Candidate | Why not chosen | Strength of that reason | Where the argument belongs |
|---|---|---|---|
| Torsion | Did not separate stenosed from stenosis-free trees in the only human test ([Zhang et al. 2024](https://doi.org/10.1098/rsos.241267)); positive only in swine ([De Nisco et al. 2019](https://repub.eur.nl/pub/112774), abstract); a third derivative of a voxel centerline | Moderate; whether the null survives smoothing is unknown | §1 Zhang sentence, only if torsion's p-value is confirmed in the journal version |
| Helicity | A flow quantity that needs CFD velocity fields, not a geometric feature | Strong | Methods |
| Tortuosity index | Not related to low WSS in LM bifurcations without CAD (p = 0.86) ([Kashyap et al. 2022](https://doi.org/10.1038/s41598-022-04796-w)); overlaps with curvature | Strong | Already in §1 |
| Raw diameter | Carries sex and dominance ([Dodge et al. 1992](https://doi.org/10.1161/01.CIR.86.1.232)) | Moderate (abstract only) | §1 taper paragraph |
| Left main length | Exists for the LAD and LCx only, not the RCA; one value per person | Strong (design) | Methods |
| Distance from the ostium | Strong for STEMI occlusion sites in a referral cohort ([Wang et al. 2004](https://doi.org/10.1161/01.CIR.0000135468.67850.F4), abstract), but carried by the segment intercepts | Strong (design) | Methods |
| Eccentricity | No coronary CFD study isolating it was found; noisy at CCTA resolution | Weak (absence of evidence) | Leave out |
| Lumen volume to myocardial mass | Needs LV mass; person-level; evidence on ischaemia and FFR in referred cohorts, none on plaque development ([Taylor et al. 2017](https://doi.org/10.1016/j.jcct.2017.08.001)) | Moderate | Leave out of §1 |
| Radiomics | No mechanistic WSS link for a plaque-free wall; many parameters | Moderate | `sec:lit-risk` if anywhere |

The pattern suggests a division of labour. §1 should make only the **positive** case for taper and the diameter contrast, because a review section about geometry and WSS is the natural home for both. The design-based eliminations (left main length, distance from the ostium, helicity, radiomics) are arguments about the model and should live in Methods `sec:method-selection`, which already points back to §1 for the null features. Rehearsing all of them in the review would read as an afterthought justification.

A good model for the paragraph's structure is the perivascular fat attenuation papers. They move from a known driver to a missing measurement, then to a mechanism that makes it visible, and then state the gap as the result of a search: "we identified no cohort studies investigating the prognostic value of perivascular fat attenuation phenotyping" ([Oikonomou et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6137540/)). The model's "Because" opening should not be copied. The same moves apply to taper. The known driver is low WSS (already opened in §1 with `chatzizisis2007ess`). The missing measurement is narrowing along the artery. The mechanism is flow loss with taper. The gap is that no study identified in this search related taper to plaque that developed later.

## (a) Recommended structure of the taper paragraph

The paragraph should keep its place after the Garcha, Cui, Juan and Schoenenberger block and before the "Collectively" synthesis, in six moves of one or two sentences each. The first is a **transition and gloss**: Garcha studied the division of diameter at a bifurcation, while the lumen also narrows between branches, referred to as lumen taper. The second is the **premise** (Gijsen 2019): flow leaves through side branches, and this loss of flow is typically accompanied by taper. The third is **simulation evidence** (Johnston and Johnston 2009, then Schultz 2023 with its caveat): taper adds a low-WSS region, and the widest lumen has the lowest WSS. The fourth is **why this form** (Dodge 1992): diameter carries sex and dominance, so the change along the artery, not the size, is the feature. The fifth is **why before plaque** (Seiler 1992): in diseased arteries calibre may follow the disease. The sixth is the **gap and hypothesis**: no study identified in this search related taper to plaque that developed later, and the step from narrowing to low WSS to plaque is the thesis's hypothesis.

The "Collectively" closing paragraph can stay as written. It already says taper adds "a further region of low WSS in the proximal part of the artery" and cites only Johnston.

## (b) Draft LaTeX prose (9 sentences)

```latex
Garcha and Grande Guti\'errez examined how the diameter divides at a bifurcation, but the lumen
also narrows along each artery between its branches, referred to as lumen taper.
Gijsen et al.\ (2019) \cite{gijsen2019wss} stated in an expert consensus that blood leaves the
main artery through its side branches and that this loss of flow is typically accompanied by
tapering of the lumen.
Johnston and Johnston (2009) \cite{johnston2009taper} simulated the flow through idealised
S-shaped coronary arteries with and without taper.
In both, WSS was low on the inner wall of each bend, but only the tapered arteries had a further
region of consistently low WSS in the straight proximal part, which the authors attributed partly
to the overall taper and not only to the curvature.
Schultz et al.\ (2023) \cite{schultz2023ess} simulated the flow in normal arteries on CCTA and
found the lowest WSS where the lumen was widest, although the same flow was imposed on every
artery without its side branches, which the authors note exaggerates this gradient.
Dodge et al.\ (1992) \cite{dodge1992diameter} found the diameter of normal arteries to differ
between women and men even after normalisation for body surface area, and to differ with
dominance, so the diameter itself reflects sex and dominance as well as the shape of the artery.
In arteries with coronary disease, Seiler et al.\ (1992) \cite{seiler1992structure} found the
lumen diffusely too small for the myocardium it supplied, so in such arteries the calibre may
follow the disease rather than precede it.
No study identified in this search related taper to plaque that developed later.
That an artery whose lumen narrows less than its flow falls has low WSS, and therefore develops
plaque, is a hypothesis of this thesis and not an established finding.
```

Suggested header comment for the file:
`% Taper paragraph 2026-11-07: Gijsen 2019 full text partly read (quote "typically accompanied by tapering of the lumen"); Johnston 2009 conference paper, idealised rigid models; Schultz 2023 full text, fixed outflow caveat; Dodge 1992 and Seiler 1992 abstract only. "where most plaque is found" removed (not in Johnston). Javier 1995, Zubaid 2002 not used (abstract only, unverified).`

Three cite keys already exist in `Thesis_coronary/refs.bib`: `johnston2009taper`, `schultz2023ess` and `dodge1992diameter`. Two new entries are needed:

```bibtex
@article{gijsen2019wss,
  title   = {Expert recommendations on the assessment of wall shear stress in human coronary
             arteries: existing methodologies, technical considerations, and clinical applications},
  author  = {Gijsen, Frank and Katagiri, Yuki and Barlis, Peter and others},
  journal = {European Heart Journal},
  volume  = {40},
  number  = {41},
  pages   = {3421--3433},
  year    = {2019},
  doi     = {10.1093/eurheartj/ehz551}
}

@article{seiler1992structure,
  title   = {Basic structure-function relations of the epicardial coronary vascular tree. Basis
             of quantitative coronary arteriography for diffuse coronary artery disease},
  author  = {Seiler, Christian and Kirkeeide, Richard L. and Gould, K. Lance},
  journal = {Circulation},
  volume  = {85},
  number  = {6},
  pages   = {1987--2003},
  year    = {1992},
  doi     = {10.1161/01.CIR.85.6.1987}
}
```

Check the Gijsen author list and the exact Seiler title against the publisher pages before committing. The notes verified the DOI, journal, volume and pages, but not every author.

Two ownership points need a decision before committing. First, the content map assigns "the research gap" to the end of `sec:lit-risk` only. The gap sentence above is narrow (taper only) and phrased as the brief requires, but it should be reconciled with the map or moved there. Second, Seiler duplicates in spirit the remodelling argument of `sec:lit-risk`. If space is tight, it is the first sentence to cut, and the reverse-causation point then rests on `sec:lit-risk` alone.

## (c) What must stay out of the taper text

**Inferences that must not appear as findings.** The first is that an artery narrowing less than its flow loss has low WSS: no paper states it, so it is allowed only as the hypothesis sentence. Others are that taper predicts plaque, that the thesis is "the first" test, any expected sign, and the claim that a log-radius slope cancels body size and sex (a Methods property, and in the data an expectation to check). The "flow-matched taper residual" and the taper × curvature superposition argument are the researchers' own arithmetic. So is the claim that divergent segments compound with curvature. The phrase "where most plaque is found" in the current Johnston sentence has no source.

**Unverified or Methods-owned numbers.** The Poiseuille relation and its arithmetic belong in 05d. Murray's exponent of 3, Kassab's 7/3 and the pooled 2.39 belong in 05c. The normal taper of about 0.25 mm per 10 mm (Medrano-Gracia 2016) belongs in 05d. These must not appear in the review: the "0.22 mm per 10 mm, about 10% reversed" figures, which come from Javier 1995 on diseased arteries, not normal ones; the per-artery LAD 0.33, RCA 0.16 and LCx 0.15 mm per 10 mm values, which were never verified; Zubaid's T1 percentages; and every percentage from the Dodge and Seiler abstracts, since the chapter rule bans numbers in prose. The existing Zhang sentence's "nine geometric features" also breaks that rule.

**Excluded or weak sources.** `shen2026geometry` and its preprint arXiv 2507.17109 must never appear, including the "diameter and its variation ... have yet to be studied in detail" quote used in an earlier report. Also leave out these preprints and unchecked versions: Shen et al., arXiv 2502.06161, and Gharleghi et al., arXiv 2401.12504. The journal version of Gharleghi (*Sci Rep* 2025) has not been checked. Javier 1995 and Zubaid 2002 are abstract only and unverified. Kamiya and Togawa 1980, Zarins 1987 and Cheng 2007 were seen only through secondary pages, with DOIs unverified. Other weak sources are search-snippet-only (the MDPI 2026 parametric stenosis, the Baghdad tube model, the Soulis companions) or not peer reviewed (an APS conference abstract and a USPTO patent). Some are off-target for this paragraph: the Kawasaki aneurysm and ectasia CFD, the V/M and TAG studies (referral cohorts, attenuation rather than geometry), and Nadeem 2020 (airway, not coronary). CAS-Net must not be mentioned, the word "trunk" must not be used, and nothing may refer forward to Methods.

## Conclusion

The review does not need to show that taper predicts plaque. It needs to show that taper is the missing dimension of a shape description that WSS physics says should matter, and that the literature has measured it only in diseased or simulated arteries. Stated that way, the absence of human evidence becomes the paragraph's niche rather than a weakness to hide. The plaque-free CGPS baseline is what turns a reverse-causation problem in earlier work into a testable question. The honest cost is that taper enters the geometry block on a mechanistic argument and on the elimination of alternatives, with no prior effect size. A null result for taper would therefore be informative rather than surprising.

The practical consequence is a split of the argument. The review carries the positive mechanism, the diameter contrast and the gap. Methods `sec:method-selection` carries the design-based eliminations (left main length, distance from the ostium, helicity). Methods 05d carries the formula, the normal taper size and the sign question. Keeping each argument in its owner section is also what keeps the taper paragraph to nine sentences.
