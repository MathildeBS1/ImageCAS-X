# Section 1 claim check: Coronary Geometry and Wall Shear Stress (`sec:lit-wss`, `01_geometry_wss.tex`)

Checked 2026-11-08 against the prose of lines 134-188. Full texts read: Kashyap 2022 (PMC8764056), Garcha and Grande Gutierrez 2025 (PMC11770140), Zhang 2024 (local full text `knowledge/docs_thesis/papers/zhang2024curvature.txt`), Johnston and Johnston 2009 (MODSIM PDF). Abstract level: Asakura and Karino 1990, Johnston and Johnston 2007, Johnston and Johnston 2008, Chatzizisis 2007, van der Giessen 2009 (publisher abstract page). Gijsen 2019: PMC page blocked by a captcha today; the quote is taken from the earlier full-text read stored in the project's evidence-phrasing skill. Bibliographic data checked against Crossref.

## Q1. Does each study's population, method and endpoint match how the thesis describes it?

### Takeaway
Most sentences are supported. Five need wording changes: van der Giessen "the same pattern" (only bifurcations were studied, and WSS was assumed, not computed), Kashyap "best predicted" (it is a correlation, in symptomatic referred patients with zero calcium, not a general CAD-free population), Garcha "artificial trees" (variants of one patient model), Johnston 2007 "depended" (a correlation in four arteries), and the Johnston 2009 inference "complementary rather than redundant information", which goes beyond what an idealised model with two geometries can show.

### Cited Findings

**Sentence 1 (Chatzizisis 2007): "vessel shape influences the level of WSS, and plaque tends to develop where WSS is low". Verdict: supported (review level).**
- Chatzizisis et al. 2007 is a JACC review. It states that plaques form where endothelial shear stress is low and oscillatory, and that low shear stress changes endothelial gene expression in ways that favour early plaque formation. — [Europe PMC record, DOI 10.1016/j.jacc.2007.02.059](https://doi.org/10.1016/j.jacc.2007.02.059)
- Caveat: it is a narrative review that draws mainly on animal and cross-sectional human data. It is fine as the premise, but it is not human evidence on plaque onset.

**Sentence 2 (Asakura and Karino 1990): "on autopsied hearts found plaque concentrated at bifurcations and bends". Verdict: supported, but incomplete.**
- Flow was visualised in five postmortem human coronary artery trees. Plaques and wall thickenings sat mainly on the outer walls of branches at bifurcations and on the inner walls of curves. These sites had slow or disturbed, recirculating flow and low wall shear stress, and the authors conclude that low flow velocity and low shear stress are the main haemodynamic factors in where lesions form. — [Europe PMC abstract via DOI 10.1161/01.RES.66.4.1045](https://doi.org/10.1161/01.RES.66.4.1045)
- The thesis sentence leaves out the flow-visualisation link to low WSS, which is the whole reason this paper belongs in a WSS section. It also leaves out the specific walls (outer wall of the branch, inner wall of the bend) and the very small sample. Under the chapter's no-numbers rule, "a few" can stand in for the count.

**Sentence 3 (van der Giessen 2009): "found the same pattern on the CT scans of living patients and located the plaque on the outer walls of the bifurcations". Verdict: partly overstated.**
- Design: 28 retrospectively studied symptomatic patients, 64-slice CT, 65 cross-sections near the left main and LAD-D1 bifurcations. Each cross-section was divided into four parts ranked by *expected* WSS. — [EuroIntervention abstract](https://eurointervention.pcronline.com/article/plaque-and-shear-stress-distribution-in-human-coronary-bifurcations-a-multislice-computed-tomography-study)
- Results: "Of all parts I [outer wall, lowest WSS], 72% contained plaque. This was 62%, 38% and 31% in parts II, III and IV", and "Plaque was never found exclusively in the flow divider part IV." Conclusion: "plaque is mostly present in low WSS regions." — [same](https://eurointervention.pcronline.com/article/plaque-and-shear-stress-distribution-in-human-coronary-bifurcations-a-multislice-computed-tomography-study)
- WSS was not computed. Each part's WSS level was assigned from the bifurcation geometry. — [same](https://eurointervention.pcronline.com/article/plaque-and-shear-stress-distribution-in-human-coronary-bifurcations-a-multislice-computed-tomography-study)
- Problem: the study looked only at bifurcations, so "the same pattern" (bifurcations *and* bends) is broader than what was studied. Plaque was "mostly" on the outer wall, but the flow divider was also involved in about a third of cross-sections. The patients were symptomatic and most cross-sections already had plaque (88%).

**Sentence 4 (Gijsen 2019): "WSS cannot be measured directly in the coronary arteries of patients". Verdict: supported.**
- Gijsen et al. 2019, p. 3422: "Since wall shear stress in coronary arteries cannot be measured directly, we need to compute ..." (from the earlier full-text read in `.claude/skills/evidence-phrasing/SKILL.md`). Bibliographic data confirmed. — [Crossref DOI 10.1093/eurheartj/ehz551](https://doi.org/10.1093/eurheartj/ehz551)

**Sentence 5 (bridge): "Studies have therefore simulated the blood flow through arteries reconstructed from scans to see which features of the geometry lead to low WSS". Verdict: fits Kashyap, but only loosely fits Zhang and Garcha.**
- Zhang used low-WSS area as an outcome next to stenosis, not as the endpoint for geometry (see below). Garcha's models are variants of one repository patient model whose parameters were changed by sampling, not arteries reconstructed from each patient's scan. — [Garcha PMC11770140](https://pmc.ncbi.nlm.nih.gov/articles/PMC11770140/); [Zhang 2024](https://doi.org/10.1098/rsos.241267)

**Sentences 6-7 (Kashyap 2022). Verdict: endpoint and results supported; population and the word "predicted" need wording changes.**
- Population: 127 patients referred for CTCA with symptoms of CAD who "showed no obstruction and had a zero-calcium score". The abstract calls them patients "without coronary artery disease". — [Kashyap PMC8764056](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Site and endpoint: the left main bifurcation with its LAD and LCx branches. The outcome is the share of the vessel area with TAWSS below 0.4 Pa. — [same](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Measures: tortuosity index, average absolute curvature, RMS curvature, average squared-derivative curvature. — [same](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Results (adjusted R², whole bifurcation): average absolute curvature 0.112 (p = 0.001), RMS curvature 0.093 (p = 0.002), squared-derivative curvature 0.101 (p = 0.001), tortuosity index -0.018 (p = 0.865). For the LAD alone, average curvature reached 0.232. — [same, Table 4](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- The authors call the tortuosity index "the most commonly used tortuosity metric" and recommend average absolute curvature. — [same](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Limitations the authors state: a constant-pressure outlet (no patient-specific data), rigid walls, the diameter profile not considered (it "may interact with tortuosity"), and only the left main bifurcation. — [same](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Assessment: "strongest correlation ... weak but significant" is supported. "Tortuosity index was not related ... although it is the most widely used" is supported. "Best predicted" is not: the analysis is a cross-sectional correlation between a measure and simulated WSS, with no prediction. "Individuals without CAD" is the authors' own wording, but they are symptomatic referred patients with zero calcium and no obstruction, not a population sample. The two other curvature-based measures were also significant, so the separation is between the tortuosity index and every curvature measure, not between average curvature and all the others (the header note already says this).

**Sentences 8-9 (Zhang 2024). Verdict: the anatomical result is supported; the description needs scoping.**
- Data: ASOCA, 40 cases with one excluded; "Of the 39 left main coronary trees studied, 20 had no significant stenosis, 12 were moderately stenosed and 7 had severe stenoses." Non-stenosed means %DS = 0. — [Zhang full text (local), RSOS](https://doi.org/10.1098/rsos.241267)
- Nine anatomical features. For bifurcating segments these include the inflow angle, the bifurcation angle and Finet's ratio, defined as the "ratio of the mean PMV diameter to that of the mean DMV and SB diameters". — [same](https://doi.org/10.1098/rsos.241267)
- Key quote: "Absolute average curvature was the only anatomical parameter significantly higher in the stenosed whole trees (... p = 0.024) and non-bifurcating segments (... p = 0.027), but not in the bifurcating segments (p > 0.057)." — [same](https://doi.org/10.1098/rsos.241267)
- TSVI, a flow index, beat curvature (AUC 0.876 vs 0.711). %LowTAESS did **not** separate non-stenosed from stenosed trees; it separated only moderate from severe (p = 0.009). — [same, abstract](https://doi.org/10.1098/rsos.241267)
- "Coronary curvature negatively correlated with diameter (r = -0.474 and p = 0.002), suggesting that smaller arteries tend to be more curved." — [same](https://doi.org/10.1098/rsos.241267)
- The authors state their limits: the "sample size is still relatively small due to its retrospective and single-centre nature", and there were no patient-specific boundary conditions. The population is "patients with suspected CAD". — [same](https://doi.org/10.1098/rsos.241267)
- Assessment: "only average curvature was significantly higher in stenosed trees" is supported, but only at the whole-tree level and in segments between bifurcations, not at the bifurcations themselves. The angle and Finet's ratio entered the comparison only for bifurcating segments, where *no* anatomical feature was significant. "Related the geometry to disease" is correct. The design is cross-sectional, so the curvature difference may partly follow from disease or from vessel size, and Zhang did not find low WSS to be the link.

**Sentences 10-14 (Garcha and Grande Gutierrez 2025). Verdict: mostly supported; "artificial trees", "one feature at a time" and "the more ... the larger" need softening.**
- Generation: "230 synthetic left coronary artery models", all derived from one baseline patient model: "The LCA structure was derived from model 0066_H_CORO_H in the Vascular Modeling Repository." Parameters were sampled within ±2 SD of angiographic data. — [Garcha PMC11770140](https://pmc.ncbi.nlm.nih.gov/articles/PMC11770140/)
- Varied: bifurcation position and angle, LAD and LCx diameters (sex-specific), tortuosity (Eleid 0-2 score) and mild plaque, first in phases and then in combination. — [same](https://pmc.ncbi.nlm.nih.gov/articles/PMC11770140/)
- Endpoint: area with TAWSS below 0.5 Pa, normalised, "in a spherical region at each bifurcation". — [same](https://pmc.ncbi.nlm.nih.gov/articles/PMC11770140/)
- Diameter ratio: "the diameter ratio between left coronary branches plays a substantial role in generating adverse hemodynamic phenotypes". ALWSS "demonstrated a strong quadratic fit with diameter ratio", with its lowest value near the neutral ratio (about 0.94). Skewed ratios produced low WSS "in the smaller-of-the-two branches". — [same](https://pmc.ncbi.nlm.nih.gov/articles/PMC11770140/)
- Interaction: the ratio "can amplify the effect of other geometric features such as bifurcation position and angle, and vessel tortuosity", and "skewed LAD/LCX diameter ratios strengthen the correlations". The *direction* of the angle effect reverses with dominance (R = -0.73 LAD-dominant vs R = 0.86 LCx-dominant). — [same](https://pmc.ncbi.nlm.nih.gov/articles/PMC11770140/)
- Neutral ratio: angle and position had non-significant or weak effects on bifurcation ALWSS, and "ALWSS at the LAD/LCx bifurcation did not correlate with LAD and LCx tortuosity". — [same](https://pmc.ncbi.nlm.nih.gov/articles/PMC11770140/)
- The paper is internally inconsistent about which ratio (0.65 or 1.40) counts as LAD- or LCx-dominant: the Methods and the Results label them differently. Do not write a direction (LAD wider vs LCx wider) without checking the figures. — [same](https://pmc.ncbi.nlm.nih.gov/articles/PMC11770140/)
- Limits the authors state: rigid walls; a laminar, parabolic inlet with an LM shorter than the entrance length; microvascular dysfunction not modelled; "we cannot definitively confirm how well our findings would translate to a clinical population". — [same](https://pmc.ncbi.nlm.nih.gov/articles/PMC11770140/)
- Assessment: "Artificial left coronary trees" should be "variants of one left coronary model" (they are not independent synthetic trees). "Change one feature at a time" is true of the early phases only. "The more the two branches differed in width, the larger the area of low WSS" fits the quadratic fit within the sampled range, but only a few ratio levels were tested, so "unequal widths gave a larger low-WSS area" is safer. "Strengthened the effect of the angle and of the bending" is the authors' own claim. "Strengthened" hides the fact that the angle effect changed *sign*; "changed the size and even the direction of the angle effect" is closer to the paper.

**Sentence 15 (taper less studied). Verdict: unverifiable as stated, but plausible and modestly worded.** No source was checked. The searches recorded in the header notes found far fewer taper studies than curvature or bifurcation studies. Keep it, since it claims only "less attention".

**Sentences 16-17 (Johnston and Johnston 2007). Verdict: supported in substance; the verb is too causal.**
- Four human RCAs reconstructed from biplane angiograms, power-law viscosity. WSS varied widely between arteries, so results from one artery do not generalise. The study reports a "strong correlation between WSS and reciprocal radius and a weaker correlation between high curvature and extremes of WSS". — [Europe PMC abstract, DOI 10.1088/0031-9155/52/9/013](https://doi.org/10.1088/0031-9155/52/9/013)
- "Depended more on the width" reads as causal. "Correlated more closely with the width of the lumen than with the curvature" matches the abstract.

**Sentences 19-20 (Johnston 2008 and 2009 models). Verdict: supported.**
- 2008 (ANZIAM J. 49, C341-C358; first author P. R. Johnston): S-shaped in-plane and out-of-plane models with uniform diameter, which have "two regions of consistently low WSS" in in-plane arteries. — [ANZIAM J page](https://journal.austms.org.au/ojs/index.php/ANZIAMJ/article/view/330); uniform diameter confirmed in the 2009 paper: "We have previously considered flow in in-plane and out-of-plane S-shaped models with uniform diameter (Johnston and Johnston, 2008)" — [MODSIM09 PDF](https://www.mssanz.org.au/modsim09/B4/johnston_bm.pdf)
- 2009 design: "two different rigid, circular cross-section, S-shaped arteries", "evenly tapering ... with an outlet radius of 78% of the inlet radius" (2 mm to 1.56 mm over 16 cm), Newtonian, uniform inlet velocity profile, 3 cm straight inlet. — [MODSIM09 PDF](https://www.mssanz.org.au/modsim09/B4/johnston_bm.pdf)
- Findings: "'low' WSS on the inside of the bend" in every artery. The "tapered arteries ... also show a region of consistently low WSS in the proximal region ... Such points are not observed in constant radius artery models", and that region is "due, in part, to the overall taper in the artery and not only to the local curvature variation". — [same](https://www.mssanz.org.au/modsim09/B4/johnston_bm.pdf)

**Sentence 21: "Taper and curvature therefore lowered WSS at different sites, indicating that they carry complementary rather than redundant information". Verdict: overstated.**
- The paper shows a separate low-WSS *site* in two idealised geometries with one taper level. "Complementary rather than redundant information" is a statistical claim about features across people, which this design cannot test. It is the thesis's inference (the header comment already flags it). Further caveats the prose leaves out: only one taper (78%) was simulated, and with a uniform inlet profile on a short straight inlet the proximal pattern may partly reflect inlet conditions (my reading of the method, not stated by the authors).

**Sentence 22: "The models were idealised and rigid, so this separation has not been shown in real coronary arteries". Verdict: reasonable, but slightly too absolute.** Johnston 2009 itself draws on earlier realistic RCAs (Johnston et al. 2006) that show proximal regions of consistently low WSS, and argues that taper partly explains them. "Was not tested in real coronary arteries" is more accurate than "has not been shown". — [MODSIM09 PDF, Discussion](https://www.mssanz.org.au/modsim09/B4/johnston_bm.pdf)

### Inferences
- The section's weakest descriptive points are van der Giessen ("same pattern") and the Johnston 2009 inference. The rest are scoping issues (population, verbs) that can be fixed without adding numbers.
- Kashyap is the only cited study whose arteries were free of stenosis and calcium. Zhang and van der Giessen are symptomatic or suspected-CAD patients. Garcha is simulation only.

### Gaps
- The Asakura and Johnston 2007 full texts were not read (paywalled). Verdicts rest on abstracts.
- The Gijsen 2019 quote was not re-fetched today (PMC captcha). It relies on the project's earlier full-text read.
- Zhang's angle and Finet p-values are in the supplementary appendix, which was not checked. The main text says only that curvature was the "only anatomical parameter" significant at the whole-tree level and in non-bifurcating segments, and that none was significant at bifurcations.

## Q2. Is the closing "Collectively ..." synthesis supported by every study it cites?

### Takeaway
No. Average curvature (Kashyap) and the diameter ratio (Garcha) are supported. Taper rests on one idealised conference model. The bifurcation angle is not supported as a feature "most closely tied" to low WSS: Garcha found weak or non-significant angle effects at a neutral ratio and a sign change with dominance, and Zhang found no anatomical feature, angle included, that differed at bifurcations. Zhang also related curvature to stenosis, not to low WSS. "Most closely tied" implies a head-to-head ranking that no cited study made.

### Cited Findings
- Curvature: supported by Kashyap (weak, adjusted R² about 0.1 for the whole bifurcation). — [PMC8764056](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Curvature in Zhang is tied to stenosis. Low-WSS area did not separate stenosed from non-stenosed trees ("Coronary trees with moderate or severe stenoses differed only in %LowTAESS"). — [Zhang 2024](https://doi.org/10.1098/rsos.241267)
- Garcha: tortuosity did not correlate with bifurcation ALWSS at a neutral diameter ratio; it did in LAD-dominant models. This partly tempers the curvature claim (different measure, Eleid score). — [PMC11770140](https://pmc.ncbi.nlm.nih.gov/articles/PMC11770140/)
- Angle: weak or non-significant at the neutral ratio, and the sign reverses with dominance in Garcha. — [PMC11770140](https://pmc.ncbi.nlm.nih.gov/articles/PMC11770140/). In the idealised LAD-D1 models of Chiastra et al. 2017, the bifurcation angle had little effect on local haemodynamics, while curvature radius had a moderate effect. — [Chiastra 2017 summary, Erasmus repository](https://repub.eur.nl/pub/99510) (abstract-level, via search snippet; not read in full)
- Taper: one idealised MODSIM paper (two geometries, one taper level). — [MODSIM09 PDF](https://www.mssanz.org.au/modsim09/B4/johnston_bm.pdf)
- Diameter ratio: supported by Garcha. In Zhang, Finet's ratio did not differ between stenosed and stenosis-free bifurcating segments (no anatomical feature did). — [Zhang 2024](https://doi.org/10.1098/rsos.241267)

### Inferences
- A synthesis that every cited study supports: "Collectively, these simulation studies relate average curvature, unequal branch widths and lumen taper to low WSS, and suggest that the bifurcation angle acts mainly through the branch widths. The relations were weak in patient arteries and were found in simulations or in single scans, so whether these features precede plaque has not been tested." This keeps the angle (the thesis models it) with an honest status, drops "most closely tied", and ends on the gap without anticipating `sec:lit-risk` in detail.
- If the angle must stay in the list, cite only Garcha for it and write "the bifurcation angle, whose effect depended on the branch widths".
- Remove `zhang2024curvature` from the closing citation, or rephrase so Zhang supports curvature and *stenosis*, not low WSS.

### Gaps
- No study was found that compared curvature, taper, diameter ratio and angle head to head for low WSS in the same arteries. A ranking claim therefore has no source.

## Q3. Are the cite keys pointing to the correct papers?

### Takeaway
All ten keys point to the right papers, and Crossref confirms author, year, journal, volume, pages and DOI for every entry with a DOI. Two small fixes: `zhang2024curvature` lacks `number = {9}`, and `garcha2025sensitivity` could spell out the first name (Arnav).

### Cited Findings
- `kashyap2022tortuosity`: Sci Rep 12(1):865, 2022, DOI 10.1038/s41598-022-04796-w. Matches. — [Crossref](https://api.crossref.org/works/10.1038/s41598-022-04796-w)
- `garcha2025sensitivity`: Sci Rep 15(1):3325, published 2025-01-27, DOI 10.1038/s41598-025-85781-x; also PMC11770140. Matches. The header CHECK note (DOI linked to an arXiv preprint) is resolved: the DOI is the Scientific Reports paper. — [Crossref](https://api.crossref.org/works/10.1038/s41598-025-85781-x); [PMC11770140](https://pmc.ncbi.nlm.nih.gov/articles/PMC11770140/)
- `vandergiessen2009bifurcation`: EuroIntervention 4(5):654-661, 2009, DOI 10.4244/EIJV4I5A109. Matches. — [Crossref](https://api.crossref.org/works/10.4244/EIJV4I5A109)
- `johnston2008sshaped`: ANZIAM J 49, C341-C358, first author P. R. Johnston, DOI 10.21914/anziamj.v49i0.330. Matches; the page range is confirmed by the 2009 reference list. — [Crossref](https://api.crossref.org/works/10.21914/anziamj.v49i0.330); [MODSIM09 PDF refs](https://www.mssanz.org.au/modsim09/B4/johnston_bm.pdf)
- `gijsen2019wss`: Eur Heart J 40(41):3421-3433, DOI 10.1093/eurheartj/ehz551. Matches. — [Crossref](https://api.crossref.org/works/10.1093/eurheartj/ehz551)
- `zhang2024curvature`: RSOS 11(9):241267, DOI 10.1098/rsos.241267. Issue 9 is missing in the bib. — [Crossref](https://api.crossref.org/works/10.1098/rsos.241267)
- `asakura1990flow`, `johnston2007diameter`, `chatzizisis2007ess`: authors, journal, volume, pages and DOI match Europe PMC records. — [DOI 10.1161/01.RES.66.4.1045](https://doi.org/10.1161/01.RES.66.4.1045); [DOI 10.1088/0031-9155/52/9/013](https://doi.org/10.1088/0031-9155/52/9/013); [DOI 10.1016/j.jacc.2007.02.059](https://doi.org/10.1016/j.jacc.2007.02.059)
- `johnston2009taper`: MODSIM09, Cairns, pp. 671-677. Confirmed from the PDF (first page 671, references end on 677). — [MODSIM09 PDF](https://www.mssanz.org.au/modsim09/B4/johnston_bm.pdf)

### Inferences
- `johnston2009taper` and `johnston2008sshaped` are conference proceedings, not peer-reviewed journal articles in the usual sense (ANZIAM J. publishes conference proceedings as its C series). The taper argument therefore rests on proceedings papers. The text could say "conference studies" or "simplified models" so the reader can weigh this.

### Gaps
- None.

## Q4. Proposed wording improvements, caveats, order, and missing or weak studies

### Takeaway
The fixes are small and respect the chapter rules (author-year as subject, no numbers, no lists, no em dashes). The most important are rewriting the closing synthesis, softening the van der Giessen and Johnston 2009 inferences, and scoping Kashyap's population and verb. The chronological order is thematic, not strict, which is defensible. Chiastra et al. 2017 is a strong candidate addition, because it bears directly on whether the angle belongs in the synthesis.

### Cited Findings (supporting the proposals)
- See the quotes under Q1 and Q2 for each wording change below.

### Inferences: concrete wording proposals (drafts; check against the thesis-style skill)
- Asakura: "Early foundational work by Asakura and Karino (1990) \cite{asakura1990flow} visualised the flow in a few coronary trees from autopsy and found plaque on the outer walls of branches at bifurcations and on the inner walls of bends, where the flow was slow and WSS low."
- van der Giessen: "Van der Giessen et al.\ (2009) \cite{vandergiessen2009bifurcation} later found plaque near bifurcations on the CT scans of symptomatic patients mostly on the outer wall, where WSS is expected to be low, although WSS was not computed."
- Kashyap: "... simulated the flow through the left main bifurcation of patients referred with symptoms but without coronary calcium or narrowing, and tested which measure of tortuosity was most closely related to how much of the wall had low WSS." Then: "Average curvature showed the strongest relation, which was weak but significant, while the tortuosity index, the most widely used measure, was not related to low WSS."
- Zhang: "... comparing stenosis-free with stenosed trees of patients with suspected CAD. ... but only average curvature was significantly higher in stenosed trees, and only over the whole tree and between bifurcations, not at them." Optional caveat: "The comparison was made on a single scan, so the higher curvature may also accompany disease rather than precede it."
- Garcha: "... generated a large set of variants of one left coronary model, first changing one feature at a time and then several together." "Unequal widths of the two branches gave a larger area of low WSS at the bifurcation." "A difference in width also changed the size and even the direction of the effects of the angle and of the bending, so the features did not act independently of one another."
- Johnston 2007: "... they found that WSS was more closely related to the width of the lumen than to the curvature."
- Johnston 2009: "Taper and curvature therefore lowered WSS at different sites in these models, suggesting that taper may add information that curvature does not carry." Limit: "The models were idealised and rigid, so this separation was not tested in real coronary arteries."
- Closing: see the draft under Q2.

### Inferences: chronological order
- The current order is Chatzizisis 2007 (premise), Asakura 1990, van der Giessen 2009, Gijsen 2019, Kashyap 2022, Zhang 2024, Garcha 2025, then Johnston 2007-2009. The taper paragraph steps back in time. This is a defensible thematic choice, since taper is introduced as a less studied feature. No reordering is needed, but the taper paragraph's opener could carry the time shift, e.g. "Whereas ... have been studied repeatedly, an earlier series of simulations by Johnston and Johnston ...".

### Inferences: missing or weak studies
- Weak: `johnston2009taper` and `johnston2008sshaped` (proceedings, idealised, two geometries, one taper level); `johnston2007diameter` (four arteries); Zhang (39 trees, suspected CAD, Welch t-tests across many metrics, with no multiple-testing correction mentioned in the extracted text); van der Giessen (28 symptomatic patients, WSS assumed). Each is acceptable if its limit is stated in words, as the section partly does already.
- Candidate addition: Chiastra et al. 2017, J Biomech 58:79-88, DOI 10.1016/j.jbiomech.2017.04.016. Idealised LAD-D1 bifurcations, healthy and stenosed. The bifurcation angle had little effect on local haemodynamics; a smaller curvature radius increased low-WSS exposure in stenosed models. It is cited by Zhang 2024 (its ref. 27) and directly tempers the angle claim. — [Erasmus repository](https://repub.eur.nl/pub/99510) (only the abstract summary was seen; read the full text before citing)
- Not needed here: prospective human low-WSS evidence (e.g. Stone et al. 2012 PREDICTION, cited in Zhang as ref. 10) concerns progression in diseased arteries and belongs in the Clinical `sec:wss` or `sec:lit-risk`, not in this geometry-to-WSS section.

### Gaps
- Beier et al. 2016 (J Biomech, bifurcation angle and anatomical features in non-stented and stented coronaries) and Malvè et al. 2015 (Ann Biomed Eng, tortuosity of the coronary bifurcation; Zhang ref. 56) may also be relevant to the angle and curvature claims. They were not checked in this pass.
- The "less attention to taper" claim has no direct source. It relies on the searches recorded in the file header.
