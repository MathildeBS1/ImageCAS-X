# Internal quality of the Literature Review chapter (thesis/literature_review/literature_review.tex)

Scope: the chapter read as text (lines 1 to 139, header comments included), judged against the
introduction (`thesis/introduction/01_introduction.tex`), the two style guides
(`thesis/style_guide_sota_aida.md`, `thesis/style_guide_aida.md`), the clinical background
(`thesis/clinical_background/`), the knowledge bank (`knowledge/docs_thesis/`) and the `note`
fields in `thesis/refs.bib`. All sources are local files; "LR:n" means line n of
`literature_review.tex`. `CLAUDE.thesis.md` does not exist in the repo, so it was not used.

Basic measurements (computed from the .tex, citations stripped): about 880 words of prose,
37 sentences, mean 23.7 words, range 8 to 46 words, one 7-row table, 13 cited keys. The model
section (Jimenez Ordonez 2026, Sec. 1.1) is about 1,020 words, 42 sentences, mean 24 words, three
subsections, 17 citations ([style guide §1](thesis/style_guide_sota_aida.md)). Length and sentence
rhythm therefore match the model closely; the differences are in architecture and argument, below.

---

## 1. Structure: does the chapter have a clear architecture, and is the header accurate?

### Takeaway
The chapter is a single run of eight paragraphs (mechanism, measure, simulation, segmentation,
machine learning, gap 1, gap 2 plus table). The order is defensible, but with the subsections
removed it has lost the model's object, extraction, application logic and its per-strand
synthesis, and the header comment no longer describes the text.

### Cited Findings
- The header promises an order "Asakura (+ Chatzizisis, van der Giessen) | Li, Kashyap, Zebic Mihic | Garcha (+ Griffo ...) | Tello Ayala (+ Glagov) | gap 1 ... | gap 2: Sakellarios, Zhang" (LR:3 to 5). In the text, Zebic Mihic and Zhang are never cited, and the Bransby/Wang paragraph (LR:55 to 65) is not in the header at all. — [literature_review.tex LR:3-5, 55-65](thesis/literature_review/literature_review.tex)
- The header lists `zebicmihic2024index` and `stone2012prediction` as abstract-level sources (LR:10 to 11), but neither is cited in the body. — [LR:10-11](thesis/literature_review/literature_review.tex)
- The header says "Each paragraph ends on a wrap-up of its implication" (LR:2 to 3). The gap-1 paragraph ends on a fact, not an implication: "those that related geometry to flow in patients included at most several hundred individuals" (LR:82 to 83). — [LR:78-83](thesis/literature_review/literature_review.tex)
- The model's section is "three strands, one direction": object, then how it is obtained, then what it is used for, each closed by "Collectively" or "Despite these advances" ([style guide §2, §3](thesis/style_guide_sota_aida.md)). The guide's own checklist still requires "Three subsections, Title-Case noun-phrase headings, ordered object → extraction → use" and "Each subsection ends on a gap" ([style guide §12](thesis/style_guide_sota_aida.md)). The chapter has no subsections ("sections removed by the user 2026-10-04", LR:1). — [LR:1](thesis/literature_review/literature_review.tex)
- The model's "extraction" strand (Aida's 1.1.2) maps here onto a single paragraph (Bransby, Wang; LR:55 to 65) that sits between the simulation paragraph and the machine-learning paragraph, so the sequence reads mechanism, measure, simulation, segmentation, ML, rather than object, extraction, use. — [LR:43-76](thesis/literature_review/literature_review.tex)
- Transitions between paragraphs are mostly explicit: "Geometry, by contrast, can be measured directly from routinely acquired CCTA scans" (LR:52 to 53) hands over to "Using geometry in routine risk assessment relies on automated segmentation" (LR:55 to 56). — [LR:52-56](thesis/literature_review/literature_review.tex)
- The style guide's mapping table plans strand-ending gaps sourced to Shen et al. (2026), Bransby et al. (2026) and Zhang et al. (2024) ([style guide §10 mapping](thesis/style_guide_sota_aida.md)). The header records that Shen is "deliberately NOT cited" (LR:6 to 7), and Zhang has been dropped, so the guide's plan no longer describes the chapter.

### Inferences
- The flat structure makes the chapter read as a chain of one-study paragraphs. Without headings, the reader does not know until LR:78 that paragraphs 2 to 5 were building three different limitations (measure, region, cohort design). Either restore two or three headings, or add a one-sentence roadmap after the opening paragraph naming the three strands.
- The header should be updated so it matches the text (remove Zebic Mihic, Zhang, Stone; add Bransby and Wang). An examiner never sees it, but the author and the agents working from it do, and a stale header has already produced a mismatch between the plan and the prose.
- The Bransby/Wang paragraph is the "how geometry is obtained" strand. Moving it to directly after the mechanism paragraph (object, extraction, then evidence on use) would reproduce the model's logic and let paragraphs on Li, Kashyap, Garcha and Tello run together as the "use" strand, so the gap would follow from them without interruption.

### Gaps
- Final chapter order in the thesis is unresolved: `00_chapter_intro.tex` says the mechanism link "was reviewed in Chapter~\ref{ch:literature}" (past tense, review first), while `05_hemodynamics.tex` line 116 to 117 says the evidence "is reviewed in Chapter~\ref{ch:literature}" (present, review later). Which chapter comes first could not be determined from the repo (no master .tex found in `thesis/`).

---

## 2. Synthesis versus summary

### Takeaway
The chapter mostly summarises, one study (sometimes one study plus one supporting citation) per
paragraph. There are two genuine synthesis moves (the measure-dependence sentence and the Glagov
caveat), but the one real conflict in the evidence, the inverse tortuosity–CAD association in Li
et al. (2011) against the positive one in Tello Ayala et al. (2026), is never noticed or reconciled.

### Cited Findings
- Paragraph pattern: Asakura + 2 supporting (LR:17 to 27); Li + Kashyap (LR:29 to 41); Garcha + Griffo (LR:43 to 53); Bransby + Wang (LR:55 to 65); Tello Ayala + Glagov (LR:67 to 76); Sakellarios alone in gap 2 (LR:85 to 98). Each paragraph is built around one principal study. — [LR:17-98](thesis/literature_review/literature_review.tex)
- The only "Collectively" sentence: "Collectively, these findings highlight that whether an association is found can depend on the choice of measure as much as on the anatomy." (LR:40 to 41). It gathers only two studies, and Li et al. (2011) used a single measure (a bend count), so Li cannot show measure dependence; only Kashyap does. — [LR:33-41](thesis/literature_review/literature_review.tex); Li used "three or more bends of at least 45 degrees" ([refs.bib li2011tortuosity note](thesis/refs.bib))
- Moreover Kashyap's "association" is with simulated WSS, not with disease: "compared each against simulated WSS" (LR:36 to 37). The synthesis sentence slides from an association with WSS to "whether an association is found" in general. — [LR:35-41](thesis/literature_review/literature_review.tex); Kashyap correlated metrics "against the percentage of vessel area below 0.4 Pa time-averaged wall shear stress" ([refs.bib kashyap2022tortuosity note](thesis/refs.bib))
- Unreconciled conflict: Li "found tortuosity to be inversely associated with CAD" (LR:33 to 34); Tello Ayala's turning-angle work identified CAD (LR:72 to 73), and the bib note records "Per SD of tortuosity, adjusted OR for CAD 1.05 (1.03-1.08)", a positive association. The chapter never sets these against each other. — [LR:33-34, 69-74](thesis/literature_review/literature_review.tex); [refs.bib telloayala2026tortuosity note](thesis/refs.bib)
- The knowledge bank already flags this as a cherry-picking risk: "`groves2009tortuosity` (n = 1221) finds the **inverse** with obstructive disease. Not wrong as written, but incomplete in a way that reads as cherry-picked." — [state_of_the_art_plan.md, "Two corrections"](knowledge/docs_thesis/state_of_the_art_plan.md)
- The Li bib note also records that "major adverse events over 2-4 years did NOT differ between CAD patients with and without tortuosity", i.e. a geometry measure with an outcome follow-up and a null result, which the chapter omits even though gap 2 is about the absence of follow-up. — [refs.bib li2011tortuosity note](thesis/refs.bib)
- A real synthesis move: "Because the data were cross-sectional, they cannot show whether the geometry preceded the disease, as an artery remodels while plaque grows \cite{glagov1987remodeling}." (LR:75 to 76). This brings a second study to bear on the first's design. — [LR:75-76](thesis/literature_review/literature_review.tex)
- A second partial synthesis: Bransby's per-branch accuracy is joined to Wang's occlusion location: "Automated segmentation is therefore most reliable in the arteries that matter most for assessing plaque risk" (LR:64 to 65). — [LR:57-65](thesis/literature_review/literature_review.tex)
- The model itself allows "criticism of a single study's method beyond one concessive clause" to be absent ([style guide §9](thesis/style_guide_sota_aida.md)), so its pattern is also mostly summary. The author's rule "No conclusions of our own ... Collectively may only gather findings already cited" ([style guide §10](thesis/style_guide_sota_aida.md)) further limits synthesis.

### Inferences
- The chapter would gain most from one paragraph that compares the clinical geometry–disease studies directly: Li (inverse, bend count, 2D angiography, referred), Tello Ayala (positive and weak, turning angle, 2D angiography, referred, RCA), and any bifurcation-angle study. The comparison itself (different measures, opposite signs, same referred populations) is the evidence for the "consistent measurement" gap and is more persuasive than the current single synthesis sentence. Reconciling is possible within the "no conclusions of our own" rule by citing a source that names the inconsistency (the introduction already cites `shen2026geometry` for exactly this, see §6).
- The "Collectively" sentence should either be moved after Tello Ayala, so it can gather Li, Kashyap and Tello, or be reworded to claim only what Kashyap showed (curvature tracks low WSS, the tortuosity index does not).

### Gaps
- Whether Li et al. adjusted for sex and hypertension when reporting the inverse association could not be checked from the local notes (the note gives sex and hypertension associations separately); this matters for how the conflict should be framed.

---

## 3. Critical appraisal of each cited study

### Takeaway
Appraisal is thin and uneven. Design is usually stated in words (post-mortem, simulation,
cross-sectional, longitudinal), cohort type sometimes, and limitations almost never. Only Tello
Ayala (cross-sectional) and Sakellarios (existing plaque) receive a sentence of critique. The
bib notes hold the critical detail, but almost none of it reached the prose.

### Cited Findings (study by study)

**Asakura and Karino (1990)**
- Prose: "traced the flow through a small number of human coronary trees after death. Their work demonstrated that plaque formed almost exclusively on the outer walls..." (LR:19 to 22). — [LR:19-22](thesis/literature_review/literature_review.tex)
- Bib: "five postmortem human coronary trees ... note n = 5, quote it with the sample size"; "full text not read". — [refs.bib asakura1990flow note](thesis/refs.bib)
- Appraisal: "demonstrated" (top of the guide's strength ladder below "established", [style guide §6.3](thesis/style_guide_sota_aida.md)) for five post-mortem trees, with no WSS measured in the trees. The author's own bib note asks for the sample size alongside the claim; the no-numbers rule turns it into "a small number", which is the right signal but weak.

**Chatzizisis et al. (2007) and van der Giessen et al. (2009)**
- Prose: "Subsequent research has consistently located plaque at these sites in living patients and identified low wall shear stress (WSS) as the underlying cause" (LR:23 to 25). — [LR:23-25](thesis/literature_review/literature_review.tex)
- Bib: Chatzizisis is a "Review, not primary work", full text not read. Van der Giessen: "65 CT cross-sections near coronary bifurcations; plaque in 72% of low-WSS outer-wall quarters vs 31% of flow-divider quarters ... Patient n not given in the abstract", full text not read. — [refs.bib notes](thesis/refs.bib)
- Appraisal: "consistently" and "the underlying cause" are causal and universal claims resting on one narrative review and one cross-sectional CT study with plaque also present in a third of flow-divider quarters. Neither study's design is stated.

**Li et al. (2011)**
- Prose: "applied such a count to consecutive patients undergoing angiography and found tortuosity to be inversely associated with CAD" (LR:33 to 34). Table: "Cross-sectional bend count" (LR:115). — [LR:33-34, 115](thesis/literature_review/literature_review.tex)
- Bib: n = 1010; tortuosity "far more common in women", "positively correlated with hypertension"; 2 to 4 year MACE follow-up, null. — [refs.bib li2011tortuosity note](thesis/refs.bib)
- Appraisal: the inverse finding, the opposite of what the chapter's premise predicts, is reported with no comment on the referred population, 2D projection, sex/hypertension confounding or the follow-up. "Cross-sectional" in the table is incomplete given the follow-up arm. "Early clinical work" (LR:32) for a 2011 study is questionable when `groves2009tortuosity` (2009) is in the knowledge bank.

**Kashyap et al. (2022)**
- Prose: "applied every previously used tortuosity measure to the left main bifurcation of individuals without CAD and compared each against simulated WSS. Curvature-based measures were clearly related to low WSS, whereas the tortuosity index showed no association despite being the most widely used measure." (LR:35 to 39). — [LR:35-39](thesis/literature_review/literature_review.tex)
- Bib: CTCA, n = 127 patients without CAD, average absolute curvature had the highest coefficient of determination, tortuosity index p = 0.86. — [refs.bib kashyap2022tortuosity note](thesis/refs.bib)
- Appraisal: the best-described study in the chapter (region, population, comparator). Missing: the outcome is a simulated surrogate, not disease, and the population is patients referred for CTCA without CAD rather than a general population. "clearly" is an evaluative word in a study sentence, which the guide restricts to frames and gaps ([style guide §9](thesis/style_guide_sota_aida.md)).

**Garcha and Grande Gutierrez (2025)**
- Prose: "simulated blood flow in computer-generated models of the left coronary tree ... the area of low WSS followed the division of diameter and formed in the narrower branch, with an uneven division strengthening the effects of angle and bending." (LR:45 to 49). — [LR:45-49](thesis/literature_review/literature_review.tex)
- Bib: "230 synthetic left-coronary CFD models ... Synthetic geometries, not patients." — [refs.bib garcha2025sensitivity note](thesis/refs.bib)
- Appraisal: "computer-generated" signals the design. Not stated: synthetic geometries may not span real anatomical variation, and the outcome is again simulated WSS, not plaque. The sentence at LR:45 to 47 is 46 words, the longest in the chapter and above the guide's 45-word ceiling ([style guide §12](thesis/style_guide_sota_aida.md)).

**Griffo et al. (2026)**
- Prose: cited only for "Such flow simulations remain limited by their high computational cost and the specialized expertise they require, which restricts their use across large populations" (LR:50 to 51). — [LR:50-51](thesis/literature_review/literature_review.tex)
- Bib: Griffo's own contribution is a network that "estimates WSS from geometry alone in < 5 s per vessel" in 748 patients, with moderate MI discrimination (AUC 0.63 to 0.68) among patients who all had an MI. — [refs.bib griffo2026wss note](thesis/refs.bib); [papers/griffo2026wss.md](knowledge/docs_thesis/papers/griffo2026wss.md)
- Appraisal: the chapter cites Griffo for a limitation that Griffo's own work addresses. An examiner who knows the paper will see that geometry-to-WSS at scale already exists. This is precisely the "near miss" the model recommends naming and then distinguishing ([style guide §7](thesis/style_guide_sota_aida.md)): single vessels, invasive angiography, all patients with MI.

**Bransby et al. (2026)**
- Prose: "benchmarked several deep learning methods on a large public CCTA dataset against the agreement between expert annotators. Their work demonstrated that the best methods approached human agreement, with the most accurate segmentations in the main branches of the tree." (LR:57 to 60). — [LR:57-60](thesis/literature_review/literature_review.tex)
- Knowledge bank: the best method is "close to, but significantly below, the human ceiling, and no automated method in the paper reaches it". The style guide planned to end this strand on "automated methods do not yet match human agreement, with breaks in every method". — [cas_net_walkthrough.md line 449-452](knowledge/docs_thesis/cas_net_walkthrough.md); [style guide §10 mapping](thesis/style_guide_sota_aida.md)
- Appraisal: "approached human agreement" is the favourable half of that finding; the limitation (significantly below, connectivity breaks) and the fact that it is an arXiv preprint (refs.bib `journal = {arXiv preprint}`) are dropped. The author list includes DTU group members (Paulsen, Jimenez), so it is the home group's preprint; examiners will expect its limits to be stated. Generalisation from the benchmark dataset to the CGPS scans the thesis uses is not addressed.

**Wang et al. (2004)**
- Prose: "these branches carry the greatest clinical consequence, mapping the occlusions behind acute myocardial infarction to the proximal third of each main coronary artery" (LR:61 to 63). — [LR:61-63](thesis/literature_review/literature_review.tex)
- Bib: "208 consecutive STEMI patients, one centre ... CAREFUL: this is the location of culprit OCCLUSIONS in STEMI, not of all plaque"; abstract only. — [refs.bib wang2004occlusions note](thesis/refs.bib)
- Appraisal: "proximal third" of the arteries (Wang) is matched to "main branches" (Bransby); these are not the same unit, so "therefore most reliable in the arteries that matter most" (LR:64) is a loose join. Wang is also a localisation ("where") study, which the author's own rule confines to mechanism.

**Tello Ayala et al. (2026)**
- Prose: "measured the turning angle along the right coronary artery in a large archive of invasive angiograms from patients referred for suspected heart disease. A transformer reading the full turning-angle profile identified CAD more accurately than a logistic regression on the mean angle, suggesting that the full shape of a vessel carries information that a single summary value does not." (LR:69 to 74). — [LR:69-74](thesis/literature_review/literature_review.tex)
- Full-text note: AUROC 0.67 vs 0.60, "No significance test" for that gap; "CAD label is a qualitative call by the same cardiologist on the same LAO frames used for tortuosity -- circularity risk the authors do not address"; "2D single-plane projection"; segmentation succeeded in "only 78.7% of eligible loops". — [refs.bib telloayala2026tortuosity note](thesis/refs.bib); [papers/telloayala2026tortuosity.md](knowledge/docs_thesis/papers/telloayala2026tortuosity.md)
- Appraisal: the chapter's best-appraised study (population, region, design, reverse causation). Still missing the limitations most relevant to this thesis, whose transformer is modelled on it: modest discrimination, no test of the difference, a 2D projection, and the label circularity. "suggesting that the full shape of a vessel carries information" is a reasonable hedge, but with AUROC 0.67 and no significance test it carries more than the result supports.

**Glagov et al. (1987)**
- Prose: "as an artery remodels while plaque grows" (LR:76). Bib: 136 autopsy hearts; "lumen area is preserved until the lesion occupies 40%". — [LR:76](thesis/literature_review/literature_review.tex); [refs.bib glagov1987remodeling note](thesis/refs.bib)
- Appraisal: Glagov measured cross-sectional area in the left main, not centreline shape. Its finding (lumen preserved early) could even be read as geometry staying stable while early plaque grows. The knowledge bank holds a closer source for geometry drift: Kwon et al. 2022, carotid bifurcation angle increasing over about ten years in 177 subjects ([find_research.md line 486-494](knowledge/docs_thesis/find_research.md)).

**Sakellarios et al. (2017)**
- Prose: "followed coronary bifurcations in a small group of patients with repeated CCTA over several years, reporting that WSS predicted the growth of existing plaque most accurately when the daughter branch was included. Yet the outcome was the progression of plaque that was already present, not its onset." (LR:88 to 91). — [LR:88-91](thesis/literature_review/literature_review.tex)
- Bib: "17 bifurcations in 15 patients (PROSPECT MSCT), baseline and 3-year serial CCTA ... Very small n"; abstract only. — [refs.bib sakellarios2017bifurcation note](thesis/refs.bib)
- Appraisal: design and the key limitation (progression, not onset) are stated well. What is not stated: the predictor is simulated WSS, not geometry; PROSPECT is an acute coronary syndrome population; and the comparison is between two modelling choices, not a test of whether geometry predicts anything.

**SCORE2 (2021)**
- Prose: "current risk scores combine systemic risk factors only \cite{score2_2021}" (LR:94 to 95). Bib: "Full text not opened." — [refs.bib score2_2021 note](thesis/refs.bib)
- Appraisal: acceptable for a well-known fact. Note that the thesis baseline is "age and sex" ([01_introduction.tex line 58-59](thesis/introduction/01_introduction.tex)), not SCORE2, so the review sets up a comparison the aims do not run.

### Do the "no numbers" and "no concept explanations" rules weaken appraisal?
- The no-numbers rule replaces cohort sizes with "a small number" (LR:20), "a large archive" (LR:70), "a small group" (LR:89) and "at most several hundred individuals" (LR:83). The last is a quantitative claim the reader cannot check in the prose; it can only be checked from the table, and the table does not list all studies it summarises. — [LR:20, 70, 83, 89](thesis/literature_review/literature_review.tex)
- The model uses "4 in total" numbers including "169 subjects" ([style guide §1](thesis/style_guide_sota_aida.md)), so it is less strict than the author's rule; the guide notes the rule is the user's own ("neither former thesis reports numbers in its review", [style guide §10](thesis/style_guide_sota_aida.md)).
- The table carries the cohort column but no imaging modality, population type (referred, no CAD, ACS, general) or outcome column (WSS, present CAD, progression, onset). The model's guidance is that "the middle columns are the comparison axes that make her gap visible" ([style guide §8](thesis/style_guide_sota_aida.md)). The caption has to state the gap in words instead: "None followed a plaque-free coronary tree over time." (LR:134 to 135). — [LR:110-137](thesis/literature_review/literature_review.tex)
- The no-concept rule leaves "tortuosity index", "curvature-based measures", "turning angle" and "daughter branch" undefined in the review, and a grep of `thesis/clinical_background/*.tex` finds no definition of tortuosity, curvature or turning angle (only a comment in the `05_hemodynamics.tex` header). So the reader cannot see why curvature and the tortuosity index differ, which is the crux of the Kashyap result. — grep result, [05_hemodynamics.tex line 5](thesis/clinical_background/05_hemodynamics.tex)

### Inferences
- The rules themselves are coherent and match a deliberate house style; the weakness is that nothing replaces the information they remove. Two low-cost fixes keep both rules intact: (a) add Population, Modality and Outcome columns to the table (cohort sizes stay in the table, design limits become visible at a glance); (b) give each principal study one concessive clause naming its main limitation, which the model allows ("While effective for ..., these workflows required ...", [style guide §9](thesis/style_guide_sota_aida.md)).
- Qualitative size words can still be calibrated without numbers: "five" is a number, but "a handful of post-mortem trees" or "a single-centre series" is not, and design words (single-centre, referred, synthetic, two-dimensional) carry most of the appraisal weight anyway.
- The definitions of the geometric measures need a home. If the clinical background is meant to hold all concepts, it currently lacks the geometry measures entirely; they belong either there or in the methods chapter with a forward pointer, which the review's no-forward-reference rule would then forbid. That tension should be resolved explicitly.

### Gaps
- Bransby's per-branch accuracy claim ("most accurate segmentations in the main branches") was not traced to a specific table in the local notes; the knowledge bank gives whole-image DSC only.

---

## 4. Are the two gaps convincingly derived, and do they map to the thesis aims?

### Takeaway
The gaps point in the right direction (referred, cross-sectional, single region; no plaque-free
follow-up), and gap 2 maps cleanly onto the aim. But both gaps are stated as the author's own
inference without a source, against the guide's own rule; gap 1's cohort-size clause is narrowed
to flow studies, which the thesis does not do; and gap 2's absence claim rests on one cited study
and a non-sequitur "therefore".

### Cited Findings
- Gap 1: "Studies to date have related coronary geometry either to WSS in computer models or to disease that was already present at the time of imaging. Most of them examined a single region of the tree, such as the left main bifurcation or the right coronary artery, and those that related geometry to flow in patients included at most several hundred individuals." (LR:79 to 83). — [LR:78-83](thesis/literature_review/literature_review.tex)
- "either ... or" is contradicted by the next paragraph, where Sakellarios relates geometry-informed WSS to later progression (LR:88 to 90), and by Li's outcome follow-up (bib). Kashyap used patient CCTA geometries, not "computer models" in the sense of Garcha's synthetic trees. — [LR:88-90](thesis/literature_review/literature_review.tex); [refs.bib notes](thesis/refs.bib)
- "Most of them examined a single region" is supported in the text by two studies (Kashyap left main, Tello RCA); Li and Garcha do not fit it cleanly. The header says the region and cohort-size points "are rebuilt from the primary studies reviewed here (Kashyap left main, Tello RCA, Griffo/Sakellarios cohorts)" because Shen is not cited (LR:6 to 7). — [LR:6-7](thesis/literature_review/literature_review.tex)
- The cohort-size clause is restricted to studies relating "geometry to flow in patients", because the large cohorts in the review (Li, Tello Ayala, 22,334 patients in the table) relate geometry to disease. The aim does not compute flow: "computes branching angles, branch radius ratios and vessel curvature ... these features are used to predict which individuals develop new plaque" ([01_introduction.tex line 53-56](thesis/introduction/01_introduction.tex)). So the size limitation is located in a branch of the literature the thesis does not extend.
- The style guide's rule: "No conclusions of our own. Every synthesis or gap sentence must restate what a cited study demonstrated or stated" and the checklist item "Each subsection ends on a gap that a cited source stated, not one we inferred." ([style guide §10, §12](thesis/style_guide_sota_aida.md)). LR:78 to 83 and LR:92 to 93 carry no citation.
- Gap 2: "The few longitudinal studies available have followed patients who already had coronary disease." (LR:87) is supported by one citation (Sakellarios). "No study has therefore combined consistent measurement of the coronary tree with follow-up of a general population from a plaque-free state to the formation of new plaque." (LR:92 to 93). — [LR:87-93](thesis/literature_review/literature_review.tex)
- The knowledge bank holds further longitudinal studies that would make "the few" evidenced: Stone et al. 2012 PREDICTION (506 post-ACS patients, 374 re-imaged; cut 2026-10-04 per LR:5), Samady et al. 2011 (n = 20), Yamamoto et al. 2017 (20 patients, serial OCT), and Han et al. 2022 (ICONIC), which the introduction itself cites for the same point. — [refs.bib stone2012prediction note](thesis/refs.bib); [find_research.md lines ~476-490](knowledge/docs_thesis/find_research.md); [01_introduction.tex line 38-40](thesis/introduction/01_introduction.tex)
- The bridging sentence: "Bridging this gap is essential, as current risk scores combine systemic risk factors only \cite{score2_2021}, although these factors reach the whole coronary tree while plaque forms where its geometry lowers WSS \cite{chatzizisis2007ess}." (LR:94 to 96). The "although" clause is a localisation argument (where plaque forms within a tree) used to justify an individual-risk claim (who develops plaque). — [LR:94-96](thesis/literature_review/literature_review.tex)
- The introduction itself acknowledges that localisation may not translate into individual risk: "the localization of plaque within a tree does not translate into a difference in risk between individuals" is named as a possible result ([01_introduction.tex line 67-69](thesis/introduction/01_introduction.tex)). The user's rule is that the thread is "who develops plaque (individual risk), never where plaque forms. Localization studies appear only as mechanism." ([style guide §10](thesis/style_guide_sota_aida.md)).
- "The integration of these two elements represents a progression toward testing ..." (LR:97 to 98): the referent of "these two elements" is unclear (consistent measurement and follow-up? geometry and systemic factors?). The model's equivalent names both strands explicitly ("The integration of AI-based segmentation with such high-fidelity FE modelling", [style guide §2](thesis/style_guide_sota_aida.md)). — [LR:97-98](thesis/literature_review/literature_review.tex)

### Mapping to the aims (01_introduction.tex lines 47-62)
| Aim element | Where the review motivates it | Status |
|---|---|---|
| General population, not referred patients | Gap 2 "follow-up of a general population" (LR:93); Tello "patients referred" (LR:71) | Covered |
| Longitudinal, new plaque at second scan | Gap 2, Sakellarios (LR:85 to 91) | Covered, thinly (one study) |
| Automatic segmentation | Bransby (LR:55 to 65) | Covered, limitations omitted |
| Assign each vessel to its coronary artery | Nothing | Not motivated |
| Branching angles | Garcha only, synthetic (LR:45 to 49) | No clinical angle–disease study reviewed |
| Branch radius ratios | Garcha diameter division (LR:47 to 49) | Synthetic only |
| Curvature | Kashyap (LR:35 to 39) | Covered (WSS outcome only) |
| Logistic regression vs transformer on curvature profile | Tello Ayala (LR:72 to 74) | Directly motivated |
| Baseline of age and sex | SCORE2 (LR:94 to 95) | Mismatch: review sets up SCORE2, aim uses age and sex |
| Fitted per artery "since shear acts locally" | Region gap (LR:81 to 82), Wang (LR:61 to 63) | Partially |

### Inferences
- Gap 1 should be reframed onto what the thesis does: large geometry–disease cohorts exist but are referred and cross-sectional (Li, Tello Ayala), and the studies with mechanistic grounding are small (Kashyap, Sakellarios). That keeps the three dimensions in the header (measure, region, cohort) and drops the narrowing to flow studies.
- Gap 2's absence claim needs support of the kind an examiner can accept: either cite a review that states it (the introduction already uses `shen2026geometry`; `zhang2024curvature` states its own novelty against prior work, per its bib note), or describe how the literature was searched. Citing the additional longitudinal studies (Stone, Han, Samady, Yamamoto), all in diseased or referred patients, would turn "the few" from one study into a pattern, and remove the non-sequitur "therefore".
- The "although" sentence can be repaired by moving the individual-level premise to the front: geometry varies between people (Temov 2016, already cited in the introduction), so some trees carry more low-WSS area than others. That is the individual-risk argument; the within-tree localisation is only its mechanism.
- Bifurcation angle is one of the three features in the aim, yet no clinical bifurcation-angle study is reviewed although several sit in the knowledge bank (e.g. the 106-patient CCTA angle study and left main angle >80 degrees with MACE in `find_research.md` lines ~78 and ~455). An examiner will ask why angles are measured if the review shows evidence only from synthetic trees.
- Artery labelling is a named pipeline stage with no literature at all; one sentence or a short near-miss would suffice.

### Gaps
- Whether any study has actually followed a plaque-free general population with serial CCTA and related geometry to new plaque could not be verified here (no web search was in scope); the knowledge bank's two research passes found none, and found Kwon 2022 (carotid) as "the only longitudinal vascular-geometry study" ([find_research.md line 486](knowledge/docs_thesis/find_research.md)). The gap claim is plausible but its support is the author's search, which the chapter does not describe.

---

## 5. Overreach relative to abstract-level sources

### Takeaway
The strongest causal and universal wording in the chapter sits on exactly the sources the header
lists as abstract-only (Chatzizisis, van der Giessen, Sakellarios, Li), and on Asakura, whose
full text is also unread per its bib note.

### Cited Findings
- Abstract-level sources per header: "chatzizisis2007ess (full text pending), vandergiessen2009bifurcation, stone2012prediction, sakellarios2017bifurcation, zebicmihic2024index, li2011tortuosity" (LR:10 to 11). Asakura's bib note also says "full text not read"; Wang's says "full text not read"; SCORE2's "Full text not opened". — [LR:10-11](thesis/literature_review/literature_review.tex); [refs.bib](thesis/refs.bib)
- "Subsequent research has consistently located plaque at these sites in living patients and identified low wall shear stress (WSS) as the underlying cause" (LR:23 to 25) rests on Chatzizisis (review, abstract) and van der Giessen (abstract, patient n unknown). "consistently" and "the underlying cause" are the two strongest claims in the chapter. — [LR:23-25](thesis/literature_review/literature_review.tex)
- "These findings established that the sites at risk are geometrically distinctive" (LR:26): "established" is the top of the guide's strength ladder, reserved "for a finding that later work built on" ([style guide §6.3](thesis/style_guide_sota_aida.md)); here it rests on n = 5 plus two abstract-level sources.
- "Their work demonstrated that plaque formed almost exclusively on the outer walls" (LR:21 to 22): the "almost exclusively" wording is from the abstract (per bib note), and is acceptable, but "demonstrated" for five specimens is strong.
- Sakellarios: "reporting that WSS predicted the growth of existing plaque most accurately when the daughter branch was included" (LR:90 to 91) is faithful to the abstract (bib: p = 0.007, 0.0006, 0.025 for model comparison). "over several years" for a 3-year follow-up is fine. No overreach, but the gap-2 absence claim rests on this single abstract-level source.
- Li: abstract-level, yet the bib note contains more (sex, hypertension, follow-up) than the prose uses; under-use rather than overreach.
- Gap 1's "computer models" and "at most several hundred" depend on Griffo (full text) and Kashyap (bibliography verified, open access), so they are not abstract-level problems.

### Inferences
- Soften LR:23 to 25 (e.g. "has repeatedly associated ... with low WSS" rather than "consistently ... the underlying cause"), or read van der Giessen and Chatzizisis in full before leaving the causal wording. The `paper-review` skill exists for this.
- Replace "established" at LR:26 with "indicated" or "suggested" unless the sentence is re-anchored on a stronger body of work.
- Before submission, the gap-2 support should not rest on an unread abstract alone.

### Gaps
- None beyond those listed; all abstract-level judgements are based on the bib notes, which record what the abstracts say.

---

## 6. Coherence with the introduction and the clinical background (division of labour)

### Takeaway
The three chapters overlap on the same handful of citations (Asakura, Chatzizisis, Glagov, SCORE2,
Tello Ayala), and the introduction already states the review's gaps, citing a source the review
deliberately excludes. The review therefore re-derives conclusions the reader has already been
given, under a different citation policy.

### Cited Findings
- The introduction already says: "Most studies relating geometry to plaque were conducted in patients referred for suspected CAD ... few of these studies followed the patients over time \cite{han2022plaque,telloayala2026tortuosity}. Since an artery remodels as plaque grows ... \cite{glagov1987remodeling}. In addition, there is no standard way to quantify coronary geometry, and inconsistent definitions have produced conflicting findings ... \cite{shen2026geometry}." ([01_introduction.tex lines 36-45](thesis/introduction/01_introduction.tex)). The review repeats each point (LR:29 to 41, 75 to 76, 79 to 93) without Han or Shen. — [LR header 6-7](thesis/literature_review/literature_review.tex)
- The introduction's "Current risk assessment, however, considers only the former ... \cite{score2_2021}" ([01_introduction.tex line 32-34](thesis/introduction/01_introduction.tex)) is repeated at LR:94 to 95. The phrase "CCTA scans that are already acquired" appears in both ([01_introduction.tex line 66](thesis/introduction/01_introduction.tex); LR:98).
- Asakura appears in the introduction (line 26), in `05_hemodynamics.tex` with a figure and n = 5 stated in prose ("Tracing the flow through five human coronary trees after death", line 82 to 83), and again as the review's opening (LR:19 to 22). The clinical background therefore uses a number the review's rule forbids for the same study. — [05_hemodynamics.tex lines 81-85](thesis/clinical_background/05_hemodynamics.tex)
- `05_hemodynamics.tex` closes: "The evidence that these features track WSS in measured trees, and that they relate to disease, is reviewed in Chapter~\ref{ch:literature}." (line 116 to 117). The review delivers one study for each half (Kashyap; Li and Tello Ayala). — [05_hemodynamics.tex lines 116-117](thesis/clinical_background/05_hemodynamics.tex)
- `05_hemodynamics.tex` header comment points to "state_of_the_art/03_geometry_wss_plaque.tex and 04_cohort_limitations.tex" (lines 19 to 21), a directory that no longer exists in `thesis/`. — [05_hemodynamics.tex lines 19-21](thesis/clinical_background/05_hemodynamics.tex)

### Inferences
- Decide which chapter owns the gap statement. Following the model, where the Aim "picks up from its final gap" ([style guide §1](thesis/style_guide_sota_aida.md)), the review should own the evidence and the introduction should only name the problem. Currently the introduction gives the evidence and the review restates it.
- Make the Shen policy consistent: cite it in both or neither. If it is excluded from the review because its points are "rebuilt from the primary studies", the rebuild must actually carry them (§4 shows it does not yet for "region" and "cohort size").
- Remove the Asakura duplication: the clinical background already has the flow mechanism and figure, so the review could open on the clinical question directly (geometry and disease in patients) and cite Asakura in one clause as the mechanistic starting point.

### Gaps
- None.

---

## 7. Writing quality: flow, signposting, wrap-ups, repetition, clarity

### Takeaway
Sentence-level prose is clean, the rhythm matches the model, and the house rules (author-year
subjects, no em dashes, no inserted clauses) are followed. Weaknesses are a repeated frame, some
repetition of "large populations", a self-confirming opening claim in paragraph 2, two vague
referents, and a generic gap opener borrowed verbatim from the model.

### Cited Findings
- Repeated frame: "Using coronary geometry as such a marker relies on a consistent quantification of vessel shape." (LR:29) and "Using geometry in routine risk assessment relies on automated segmentation" (LR:55). The guide asks to "rotate the verb" across frames ([style guide §11](thesis/style_guide_sota_aida.md)). — [LR:29, 55](thesis/literature_review/literature_review.tex)
- Self-confirming paragraph: it opens "However, the chosen measure can determine whether such a relationship is detected" (LR:30, uncited) and closes "whether an association is found can depend on the choice of measure as much as on the anatomy" (LR:40 to 41). The evidence in between does not add to what the opener asserted. — [LR:30, 40-41](thesis/literature_review/literature_review.tex)
- "large populations" / "at scale": "restricts their use across large populations" (LR:51), "a feasible stand-in for WSS at scale" (LR:53), "can supply their geometry across large populations" (LR:65). — [LR:51, 53, 65](thesis/literature_review/literature_review.tex)
- Reporting verb repetition: "Their work demonstrated" (LR:21, LR:59), "Their simulations demonstrated" (LR:48). — [LR:21, 48, 59](thesis/literature_review/literature_review.tex)
- Generic gap opener: "Despite these advancements, a significant gap remains in the current literature." (LR:78) is near-verbatim from the model ("a significant gap remains in current state-of-the-art modelling", [style guide §7](thesis/style_guide_sota_aida.md)) and follows a paragraph that ended on a limitation (Glagov), so "advancements" is not earned. — [LR:78](thesis/literature_review/literature_review.tex)
- Vague referents: "Most of them" (LR:81) after "Studies to date"; "these two elements" (LR:97). — [LR:81, 97](thesis/literature_review/literature_review.tex)
- Uncited field claim as opener: "The geometry of the coronary arteries has been studied for several decades, beginning with the question of where plaque forms." (LR:17 to 18). The guide: "If it states a fact about the field ... cite it." ([style guide §10](thesis/style_guide_sota_aida.md)). It also opens the chapter on "where plaque forms", which the research-focus rule assigns to mechanism only.
- Long sentences: LR:45 to 47 (46 words, above the guide's 45-word ceiling), LR:72 to 74, LR:81 to 83 and LR:88 to 91 (36 words each). Mean 23.7 against the model's 24. — computed from the .tex
- Evaluative words in study sentences: "clearly related" (LR:38). The guide says evaluative words go "mostly in frames and gaps rather than in study sentences" ([style guide §9](thesis/style_guide_sota_aida.md)).
- The table pointer "An overview of the state of the art regarding coronary geometry, wall shear stress and disease is summarized in Table~\ref{tab:literature}" (LR:99 to 100) is the model's sentence; "An overview ... is summarized" is slightly redundant.
- The table mixes strands (Asakura mechanism, Bransby segmentation) and puts Sakellarios last, out of chronological order but in text order, which the guide permits ("Row order: The order in which the studies appear in the text", [style guide §8](thesis/style_guide_sota_aida.md)). The model's table holds only the final strand's studies. Griffo, Wang, Glagov, Chatzizisis and van der Giessen are cited in prose but not tabled, which is fine, but then "at most several hundred individuals" (LR:83) cannot be checked from the table.
- Rules checked and followed: no em dashes in the chapter body; author-year as subject with `\cite` after the year in every study sentence; no inserted clauses between commas found.

### Inferences
- Rotate the second frame (e.g. a "The measurement of ... relies on ..." or "enables" form), cut "However, the chosen measure can determine ..." to a neutral frame, and let the evidence lead to the measure-dependence point.
- Replace "Despite these advancements" with a gap opener that names the strands just reviewed, and fix the two referents.
- Split LR:45 to 47 into what was varied and what was found.

### Gaps
- No spell-check or build was run (read-only task).

---

## 8. Length and depth compared with the model

### Takeaway
Length is matched (about 880 vs 1,020 words; 13 vs 17 citations), but depth per strand is
smaller: the model gives each strand three to six studies with a field-level topic sentence,
the chapter gives each "strand" one or two studies. With one study per claim, several claims fall
foul of the thesis-writing rule that no section rests on one source.

### Cited Findings
- Model: "Paragraphs: 3 per subsection on average, 3 to 6 sentences each"; six studies in 1.1.1, six in 1.1.2, five or more in 1.1.3 ([style guide §1, §3](thesis/style_guide_sota_aida.md)).
- Chapter: measure strand = Li + Kashyap; simulation = Garcha (+ Griffo for cost); segmentation = Bransby (+ Wang); ML = Tello Ayala; longitudinal = Sakellarios. — [LR:29-91](thesis/literature_review/literature_review.tex)
- The model uses field-level topic sentences ("Large-scale geometric studies have further revealed ...") to group studies ([style guide §5](thesis/style_guide_sota_aida.md)); the chapter has them in a few places ("Computational studies have also explored ...", LR:43; "Machine learning has also been used ...", LR:67) but each introduces a single study.
- The `thesis-writing` skill description requires "no section rest[ing] on one source"; gap 2's longitudinal evidence, the ML strand and the simulation strand each rest on one study (skill listing in the session system prompt).
- The knowledge bank holds unused material that fits the existing strands without new search: Groves 2009 and Zebic Mihic 2024 (measure strand), bifurcation-angle studies (find_research.md §5.1 and line ~78), Zhang 2024 whole-tree curvature (simulation strand, already read first-hand per its bib note), Stone 2012, Samady 2011, Yamamoto 2017, Han 2022 (longitudinal strand), Kwon 2022 (geometry drift). — [find_research.md](knowledge/docs_thesis/find_research.md); [refs.bib notes](thesis/refs.bib); [state_of_the_art_plan.md](knowledge/docs_thesis/state_of_the_art_plan.md)

### Inferences
- The chapter can grow by about 200 to 300 words and stay within the model's 3-page budget. The highest-value additions, in order: (1) one clinical bifurcation-angle study and Groves 2009 in the measure strand, reconciling the conflicting tortuosity signs; (2) Stone 2012 and Han 2022 in gap 2 so "the few longitudinal studies" is plural; (3) Griffo as a named near miss rather than a cost citation; (4) Zhang 2024 as the whole-tree counterpoint to the "single region" claim.
- Depth can also be added without new studies, by giving each principal study one limitation clause (§3) and adding Population, Modality and Outcome columns to the table.

### Gaps
- The model PDF itself (`Former_students_work/AidaJimenez_MasterThesis_s243279.pdf`) was not opened; comparisons rely on the author's style-guide extraction of it.
