# Recent (2010–2026) coronary simulation studies relating lumen taper or along-artery diameter change to WSS and other haemodynamic metrics

Scope and method: about 22 web searches and fetches, building on `research_notes/Why lumen taper as a feature/` and `research_notes/Taper and curvature interaction for WSS/`. Those notes already hold Johnston 2009 (MODSIM), Kandangwa 2022, Vardhan 2019, van der Giessen 2011, Gijsen 2019, Taylor 2024, Saxton, Vorobtsova 2016 and the Poiseuille/Murray arithmetic. They are only referred to here. No Shen 2026 review and no arXiv 2507.17109 are used. arXiv 2312.00257 turned up in searches; it is a preprint and is not relied on. Access level is given for each source.

**Bottom line.** Since 2010 I found **no coronary CFD study that varies taper on its own and reports WSS, OSI, RRT or TSVI in non-diseased arteries**. Johnston 2009 is still the only direct test of tapered against constant-radius coronary geometry in my searches. The post-2010 evidence is indirect. It comes in four kinds:
- a CCTA study of normal arteries in which WSS rises sharply as the lumen narrows and is linked to the artery's taper (Schultz 2023, already known; verified below);
- a machine-learning WSS surrogate in which local radius is the most important geometric input and curvature is not important (Alamir 2024);
- side-branch and flow-loss studies (Wellnhofer 2010; Vardhan 2019 and Kandangwa 2022 in earlier notes);
- taper as a nuisance factor in stent and stenosis models (diseased or treated arteries, low relevance).

## Q1. Which papers since 2010 explicitly model or quantify coronary taper and its effect on WSS or disturbed flow?

### Takeaway
Very few. In native coronary arteries, taper enters post-2010 simulation work mainly as a measured diameter decrease along the artery (Schultz 2023) or as a modelling ingredient (Kandangwa 2022, Vorobtsova 2016). The only post-2010 papers that vary taper explicitly concern stents or stenoses.

### Cited findings (ranked by relevance to the thesis use)

1. **Schultz et al. 2023, Int J Cardiovasc Imaging 39(2):441–450, DOI 10.1007/s10554-022-02739-0** (already known; verified, full text via PMC). Patient-specific CCTA-based CFD of **normal (plaque-free) coronary arteries**: 349 vessels (93 LAD, 127 LCx, 129 RCA) from 168 patients, analysed in 5,223 segments of 3 mm. The taper measure is indirect: lumen diameter per 3-mm segment along the artery, with no explicit slope. Quotes:
   - "ESS values increase rapidly and become widely scattered with decreasing lumen diameter."
   - "the LAD and LCx taper more rapidly in diameter while the RCA remains fairly constant until very distally in the vessel". The authors use this to explain why WSS varied less along the RCA.
   - The proximal-to-distal rise in ESS was clearest in the LAD (ρ = 0.47 for minimal and 0.62 for maximal ESS, p < 0.001) and weaker in the other arteries (ρ 0.22–0.34).
   - Limitation: missing side branches probably make distal flow, and hence distal ESS, too high. — [PMC9870961](https://pmc.ncbi.nlm.nih.gov/articles/PMC9870961/)

2. **Alamir et al. 2024, Front Bioeng Biotechnol 12:1360330, DOI 10.3389/fbioe.2024.1360330** (open access, full text read to 100k of 110k characters). Authors: Alamir SH, Tufaro V, Trilli M, Kitslaar P, Mathur A, Baumbach A, Jacob J, Bourantas CV, Torii R. Patient-specific design: 50 **stenosed** coronary vessels reconstructed with 3D QCA (invasive angiography, not CCTA), plus 550 synthetic variants made by flipping inlet and outlet and varying inlet velocity. The model is a U-net WSS surrogate with 17 engineered input features; feature importance was computed with integrated gradients over 10 test patients. The taper measure is local radius as an input map, plus an inlet-to-outlet radius ratio used only as a check. Quotes:
   - "Our findings indicate that the radius and inlet velocity are the most important features"
   - "Our results indeed indicate that velocity carries significant importance, following the vessel radius."
   - "Curvature as Menger curvature is not shown as significant"
   - Taper itself: "we examined the ratio of inlet and outlet radii, which is 0.86 0.12 and suggesting the tapering is not substantial." This ratio was used to justify flipping inlet and outlet. It was not a feature.
   - Caveats: the arteries are diseased, the importance ranking is that of a neural surrogate and not a physical sensitivity analysis, and the data come from one group. — [Frontiers full text](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2024.1360330/full)

3. **Wellnhofer et al. 2010, Atherosclerosis 213:475–481, "Flow simulation studies in coronary arteries — impact of side-branches"** (DOI not verified; abstract via secondary listing only). Steady and transient CFD in 3D-reconstructed RCA trees, comparing the same tree with and without side branches. Local WSS differed by up to 12.0 Pa, with a fall in volume flow of up to 78.7% along the main vessel. The authors conclude that side branches should not be left out. **No explicit taper statement was confirmed.** It is relevant because flow loss is what taper has to match. — [Springer chapter citing it](https://link.springer.com/chapter/10.1007%2F978-1-4939-0745-8_4)

4. **Kandangwa et al. 2022, Front Bioeng Biotechnol, DOI 10.3389/fbioe.2022.962687** (earlier notes; full text). A single-subject RCA model with the taper switched off: removing taper moved the highest TAWSS and transWSS proximally, and OSI changed less. It is the only post-2010 coronary paper found that switches taper on and off in a native artery, but with n = 1 and MRI-based. — [Frontiers](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2022.962687/full)

5. **Stent and stenosis models in tapered vessels** (diseased or treated arteries; low relevance):
   - Mechanical and hydrodynamic effects of stent expansion in tapered coronary vessels, Biomech Model Mechanobiol 2022, DOI 10.1007/s10237-022-01605-1. Search snippet: "the wall shear stress distribution of conical stent expansion is more uniform compared with equal diameter expansion". Full text not read. — [PMC9626435](https://pmc.ncbi.nlm.nih.gov/articles/PMC9626435/)
   - Parametric CFD of standardised 50% coronary stenoses, Math Comput Appl 2026, 31(6):251 (MDPI). Idealised, morphometric linear taper. Snippet: "In the more strongly tapered LAD and LCX geometries, flow acceleration and wall-shear loading were distributed over a longer progressively narrowing segment". The abstract snippet comparing tapered with non-tapered peak WSS is garbled. Full text 403. — [MDPI](https://www.mdpi.com/2297-8747/31/6/251)

### Inferences
- The post-2010 literature supports two statements: WSS in normal CCTA arteries is governed mainly by local lumen size, and the taper of the LAD and LCx produces a proximal-to-distal rise in WSS (Schultz). It does not support a statement that taper itself, as a slope, has been tested as a WSS determinant in a patient cohort.
- The thesis measures the slope of log radius per segment. The closest published analogue is the segment-wise diameter–WSS relation in Schultz 2023. No study computes WSS against a log-radius slope.

### Gaps
- No post-2010 idealised coronary CFD found that crosses tapered, uniform and divergent geometry with curvature (consistent with the earlier notes).
- Full text not accessed: Wellnhofer 2010 (taper statement), the 2022 stent paper, MDPI 2026, and Vorobtsova 2016 (403 in the earlier notes).
- The murine study (Serafini et al. 2025, Comput Biol Med 187:109793, DOI 10.1016/j.compbiomed.2025.109793; healthy mice, micro-CT, CFD) relates geometry to haemodynamics, but its full text was 403. Whether diameter or taper was a descriptor is unknown. It is not human, so low priority — [Polito record](https://iris.polito.it/handle/11583/2999350)
- De Nisco et al. 2021 (Front Bioeng Biotechnol, DOI 10.3389/fbioe.2021.731924; 49 human non-culprit arteries from IVUS and CCTA, 30 swine) compared "anatomical features". The abstract does not say whether taper or diameter was among them — [Frontiers](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2021.731924/full)

## Q2. Is taper or diameter change a stronger or weaker determinant of WSS than curvature? Null results?

### Takeaway
The only post-2010 coronary evidence that ranks the two directly is Alamir 2024. There, local radius was the leading geometric input for a WSS surrogate and Menger curvature was "not shown as significant", in stenosed QCA arteries. Schultz 2023 supports diameter as the dominant correlate of WSS in normal CCTA arteries but did not rank curvature quantitatively. These are diameter results, not taper-slope results.

### Cited findings
- Radius dominant, curvature not significant (integrated gradients, 50 patients, 3D QCA) — [Alamir 2024](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2024.1360330/full)
- In normal CCTA arteries, ESS "increase rapidly and become widely scattered with decreasing lumen diameter". The authors add: "It is known, that ESS depends not only on the lumen diameter, but also on the specific 3D geometry of the vessel" — [Schultz 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9870961/)
- Null result on the curvature side, in an animal model: in healthy murine and swine coronary models, a Polito group summary (via search snippet) states that "none of the geometric features were found to be correlated with the index" (helicity). The authors suggest that geometry's role "may be masked by the complex geometric features of the coronary tree". Snippet only — [Serafini et al. 2025 record](https://iris.polito.it/handle/11583/2999350)
- Idealised bifurcations: smaller curvature radius gave higher helicity and more low-WSS exposure (Chiastra et al. 2017, J Biomech, healthy and diseased bifurcation geometries; abstract via search). Taper was not varied — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0021929017302166)

### Inferences
- The two ways of ranking agree with Johnston & Johnston 2007 (reciprocal radius stronger than curvature). The newer evidence is either diseased (Alamir) or univariate (Schultz). A defensible wording is "local lumen size dominates WSS, and curvature acts as a secondary, location-specific modifier". "Taper beats curvature" is not a defensible wording.
- When curvature is not important in a WSS surrogate, that partly reflects the fact that WSS averaged over a cross-section or a map hides the circumferential inner-wall and outer-wall effects (see the earlier note on length scales).

### Gaps
- No post-2010 study found that reports partial R² or a head-to-head comparison of taper slope against curvature for WSS in non-diseased human coronaries.

## Q3. Do recent authors (including Johnston follow-ups) extend the taper work to patient geometries?

### Takeaway
I found no 2010–2015 Johnston & Johnston follow-up on taper in RCAs. Their repository work found in searches (four angiography-reconstructed RCAs, non-Newtonian and waveform studies) predates 2010. In patient geometries, the extension comes from other groups: Schultz 2023 (CCTA, normal arteries, diameter), Kandangwa 2022 (one RCA, taper switched off) and Wellnhofer 2010 (flow loss through side branches).

### Cited findings
- Griffith repository records for Johnston et al. list the tapered S-shaped models (MODSIM 2009) and the four-RCA study. Neither is dated 2010 or later in the search results — [Griffith, tapered S-shaped models](https://research-repository.griffith.edu.au/items/070a2050-b50a-5c8f-817e-0ddfefee734a); [Griffith, four RCAs](https://research-repository.griffith.edu.au/items/7702e510-ce09-510b-ac29-4187a7595860)
- The four-RCA study reports: "Large differences are found in the wall shear stress magnitude (WSS) distributions in the four arteries", with low WSS proximal to the acute margin (search snippet). This is pre-2010 context — same source.

### Inferences
- A literature review can honestly say that the taper result from idealised models has not been replicated as a slope-based analysis in patient-specific CCTA cohorts. Its closest patient-level counterpart is the diameter–WSS relation in normal CCTA arteries.

### Gaps
- Google Scholar was not queried directly, so a Johnston journal paper from 2010 or later could have been missed. The Griffith item page returned 403.

## Ranking by relevance to the thesis use
1. Schultz 2023 (normal CCTA arteries, diameter and artery-specific taper vs ESS): high.
2. Alamir 2024 (radius dominant, curvature not significant; diseased, QCA): medium-high, for the taper-vs-curvature argument.
3. Kandangwa 2022 (taper switched off in an RCA, n = 1): medium.
4. Wellnhofer 2010 and Vardhan 2019 (flow loss through side branches, which is what taper must match): medium, mechanistic.
5. Stent and stenosis taper papers (2022, MDPI 2026): low; diseased or treated arteries.

## Candidate review sentences (author–year as subject, no numbers, no lists)
- "In computational models of plaque-free coronary arteries reconstructed from CCTA, \citet{schultz2023} found that wall shear stress rose steeply as the lumen narrowed, and attributed the more uniform shear along the RCA to its nearly constant diameter compared with the tapering LAD and LCx."
- "\citet{alamir2024} trained a neural network to predict wall shear stress from coronary geometry and found the local vessel radius to be its most important geometric input, whereas centerline curvature contributed little, in line with the earlier observation of \citet{johnston2007} that wall shear stress follows the reciprocal radius more closely than curvature."
- "Whether the narrowing along an artery matters beyond lumen size has been examined in only a few simulations: removing taper from a single RCA model shifted the highest shear proximally \citep{kandangwa2022}, and leaving out side branches, whose flow loss taper normally matches, changed wall shear stress substantially \citep{wellnhofer2010}."

Use with care: Alamir 2024 used stenosed vessels from invasive angiography, and Wellnhofer 2010 was verified only from its abstract. The third sentence should not claim that the side-branch study tested taper.
