# Internal quality of the rewritten Literature Review (thesis/literature_review/literature_review.tex, 2026-10-04)

Scope and method. The chapter was read in full (lines 1 to 233, header comments included) and
checked against the 15-item rubric (`research_notes/Literature review quality assessment/standards_rubric.md`),
the earlier appraisal (`research_notes/Literature review quality assessment/chapter_appraisal.md`)
and report (`reports/Literature review quality assessment.md`), the trimmed introduction
(`thesis/introduction/01_introduction.tex`), the style guide (`thesis/style_guide_sota_aida.md`
§7, §10, §12), the paper notes in `knowledge/docs_thesis/papers/`, `find_research.md`, and the
`note` fields of `thesis/refs.bib`. All sources are local files. "LR:n" means line n of
`literature_review.tex`; "INTRO" means the introduction file. No repo file was edited.

Measurements (prose only, citations and LaTeX stripped, computed with a script): about 1,530
words, 66 sentences, mean 23.2 words, range 9 to 38, 14 sentences under 15 words, none over 45.
28 cited keys in the prose, 14 rows in the table. Earlier version: about 880 words, 13 keys,
7 rows. The rewrite therefore meets the §12 length target ("about 1,600 words") and sentence-length
rule.

---

## 1. Rubric scores (15 items, 1 to 3)

### Takeaway
The rewrite moves the chapter from 27/45 (three 1s) to about 35/45 (five 3s, ten 2s, no 1s). On the
rubric's own mapping ("mostly 2s -> 7; mostly 3s, a few 2s -> 10") it now sits at the upper edge of
the 7 band and within reach of 10. Three items (7 synthesis, 11 gap, 15 citation practice) are each
one correctable paragraph away from a 3, and the defects that hold them at 2 are factual, not
stylistic.

### Cited Findings

| # | Item | Earlier | Now | Justification and evidence |
|---|---|---|---|---|
| 1 | Scope and inclusion justified | 1 | 2 | A search statement now exists: "The studies reviewed here were identified through keyword searches on coronary geometry, wall shear stress (WSS) and coronary disease, with each record checked against Crossref and Europe PMC." (LR:31-32) and two exclusions (LR:33). No database, time window or search date is named, Crossref is a metadata check rather than a search source, and the exclusions are listed without a reason. The header itself flags this: "Search statement: CONFIRM databases and window with the user before submission." (LR:22). Rubric level 2 ("discussed the literature included and excluded"), not 3 ("justified"). |
| 2 | State of field vs what remains | 2 | 3 | Every section closes on a cited limitation and the gap paragraph separates done from undone with citations (LR:168-177). Critical judgement is visible: "Whether low WSS predicts disease prospectively is less settled." (LR:52). Held back slightly by two uncited "rarely/most" claims (see §6). |
| 3 | Situated in broader literature | 2 | 2 | Risk prediction is now present (SCORE2, LR:157-159; ORFAN inflammation, LR:160-163), which was the earlier complaint. Coronary artery calcium, the established imaging refinement of risk in asymptomatic people, is still absent (grep of the chapter and `clinical_background/` finds no CAC). The earlier report listed "ORFAN and CAC" together (report line 94); only ORFAN was added. |
| 4 | Historical development | 2 | 3 | Section 1 is a purposeful chronology from post-mortem flow visualisation (Asakura 1990, LR:42) to in-vivo CCTA (van der Giessen 2009, LR:46), prospective IVUS (Stone 2012, LR:53), simulation (2022-2025) and a 2026 graph network (LR:75). The tortuosity ladder runs from bend counts (2009, 2011) to continuous measures (2024, 2026) with "Most recently" (LR:104). The "early clinical work = 2011" error is gone. |
| 5 | Terminology | 1 | 2 | Accepted residual: tortuosity index, curvature, turning angle and bend count are still undefined anywhere (house rule plus user decision). The chapter now at least raises the ambiguity of measures: "Tortuosity shows how strongly the choice of measure can shape a finding." (LR:96) and "the tortuosity index showed no association despite being the most widely used measure" (LR:61). That is level 2 ("defined/discussed") in spirit, not 3 ("resolved ambiguities"), and the attempted resolution is wrong (item 7). |
| 6 | Key variables and phenomena | 2 | 2 | New variables are named: diameter division (LR:64-67), cardiac phase (LR:93-94), reconstruction technique (LR:88-90), remodelling (LR:139-140), label circularity (LR:137-138). Still missing: sex and hypertension as confounders of tortuosity, which Li reports ("far more common in women, OR 2.603 ... positively correlated with hypertension", refs.bib note on `li2011tortuosity`) and Tello Ayala reports (female sex beta 0.17, `papers/telloayala2026tortuosity.md`). These confounders are a plausible alternative explanation of the opposite-direction findings and are not mentioned. |
| 7 | Synthesis and own perspective | 2 | 2 (borderline 3) | Structure is now concept-centric: three sections with rotated frame sentences (LR:40-41, 86-87, 122-123), a "Collectively" sentence (LR:107-109), a cross-sectional caveat that gathers four studies (LR:139-140), a cited near miss with implication (Griffo, LR:80-81), and a cited gap paragraph. But the one new perspective, the measure-type reconciliation, is contradicted by a study it cites (see §2). Fixing that sentence would earn a 3. |
| 8 | Methods critique | 2 | 2 | Many methodological limits are now named: phantom vs patient disagreement (LR:88-90), phase dependence (LR:93-94), simulated vs measured WSS, synthetic trees (LR:62), single-vessel invasive data (LR:79), same-angiogram labels (LR:137-138). Missing: (a) Groves, Li and Tello Ayala all measured tortuosity on two-dimensional projection angiograms, not three-dimensional CCTA, which bears directly on the tortuosity conflict and on what transfers to CCTA; (b) the extraction strand is thin: Nannini (LR:112-113) receives no appraisal and artery labelling, a named pipeline stage in INTRO, has no literature at all. |
| 9 | Methods vs claims | 2 | 3 | Strongest improvement. Stone: "it predicted narrowing of the lumen, whereas the growth of plaque was predicted by the plaque already present" (LR:54-55), matching the refs.bib note ("NOT the primary endpoint"). Griffo: "Both estimates discriminated only moderately" (LR:78). Tommasino: "the reported effect sizes cannot be reproduced from their own regression table" (LR:132-133), matching `papers/tommasino2024clap.md` ("B 1.499, SE 0.206 gives a 95% CI of 2.99 to 6.70, not 3.80 to 6.70"). Tello Ayala: "the disease label was read from the same angiograms as the geometry" (LR:137-138). Han: events "within weeks" and normal-segment culprits excluded (LR:146-148), matching `papers/han2022plaque.md` ("median 29 days", "n = 21 ... excluded"). Won: "they modeled rapid progression rather than the onset of plaque" (LR:155), matching `papers/won2022paradigm.md`. |
| 10 | Practical significance | 2 | 2 | Stated once, uncritically: "Closing this gap would show whether geometry adds to systemic factors in identifying who develops plaque, using CCTA scans that are already acquired." (LR:178-179). Not critiqued: Chan's gains are modest ("absolute AUC gains are modest: +0.016 to +0.030", `papers/chan2024orfan.md`), which would calibrate what "adds" can mean. |
| 11 | Scholarly significance and gap | 2 | 2 (high) | The gap is now specific, cited clause by clause, and names its near misses (LR:169-177). Held back by: an unqualified universal absence claim not tied to the search (LR:176-177); one premise contradicted by a cited study (LR:162-163, see §4); one clause about flow studies that the thesis method does not extend (LR:171-172); and a mismatch between "adds to systemic factors" (LR:178) and the aim's age-and-sex baseline (INTRO). Artery labelling, radius ratios, the age-and-sex baseline and per-artery models are not motivated by the review. |
| 12 | Structure and rhetoric | 2 | 3 | Each section opens on an uncited frame and closes on a cited limitation, as the style guide prescribes (§12). The roadmap sentence (LR:34-35) matches the three sections. Weaknesses are repetition ("found" 14 times) and a recurring split-verb construction (§6), not structure. |
| 13 | Currency | 2 | 3 | Ten studies from 2024 to 2026: Zhang 2024, Zebić Mihić 2024, Nannini 2024, Tommasino 2024, Chan 2024, Garcha 2025, Griffo 2026, Tello Ayala 2026, Bransby 2026, Bekirçavuşoğlu 2026. The one known recent omission is Chen 2024 EHJ-CVI (myocardial bridge and new plaque), which the header lists as "Not citable yet (paywalled)" (LR:20-21) and `find_research.md` line 654 marks "BLOCKED". |
| 14 | Related work compared to own approach | 2 | 2 | Capped by the house rule against "this thesis" and forward references (style guide §10). Tello Ayala's transformer and Nannini's automated pipeline are the nearest competitors and are described, but their difference from the planned work is left implicit. The introduction does not make the comparison either. Acceptable under the rule, but an examiner will look for it. |
| 15 | Citation practice | 1 | 2 | The Bransby misattribution and the Wang join are gone (header LR:9; Bransby now reads "the authors concluded that automated methods do not yet match human performance", LR:116-117). New or remaining accuracy problems: the Zebić Mihić direction (§2), Griffo's "patients who all went on to have an infarction" applied to all data (§3), Han "came closest to a prospective design" (§3), "geometry has not been tested in this role" against Tommasino's CLAP score (§4), and three claims resting on unread full texts (Juan's adjustment, van der Giessen's "inferred", Kashyap's "weakly"; §3). |

Totals: earlier 27/45; now 35/45 (1:2, 2:3, 3:2, 4:3, 5:2, 6:2, 7:2, 8:2, 9:3, 10:2, 11:2, 12:3, 13:3, 14:2, 15:2).

### Inferences
- The mapping in the rubric is an inference, not an official DTU conversion (standards_rubric.md
  line 128). On it, the chapter is "mostly 2s" but with no 1s and five 3s, i.e. a strong 7 or weak 10.
- Items 7, 11 and 15 share the same root defect: two sentences whose wording goes beyond what the
  cited studies show (LR:107-109 and LR:162-163). Correcting those two sentences moves three items
  at once.
- Item 5 cannot reach 3 under the current house rule. Item 14 cannot reach 3 under the no-"this
  thesis" rule unless the introduction carries the comparison. Realistic ceiling with all fixes:
  about 40/45.

### Gaps
- Scores are one reader's judgement; the rubric has no inter-rater calibration.
- Whether DTU censors weight the review at all separately from the thesis is unknown
  (standards_rubric.md Q1 Gaps).

---

## 2. Synthesis vs summary: does the new structure reach level 3?

### Takeaway
Structurally yes: three concept sections, frame sentences, near misses with implications, and a
cited gap. Substantively not yet, because the tortuosity reconciliation, the chapter's main "new
perspective", attributes the opposite directions to measure type, while the cited Zebić Mihić
study found its continuous index higher in non-obstructive than obstructive disease, i.e. the same
inverse direction as the bend counts. The knowledge bank already contains the correct
reconciliation, which is by endpoint, not by measure.

### Cited Findings
- The reconciliation sentence: "Collectively, these studies reported opposite directions of
  association, with counts of discrete bends related inversely to obstructive disease and
  continuous measures related positively to disease or ischemia." (LR:107-109)
- Zebić Mihić 2024: "Tortuosity was significantly higher in non-obstructive than in obstructive CAD
  for all three arteries (p < 0.01), and the index localized: highest LCx index with lateral ischemia
  and highest LAD index with anterior ischemia" (`knowledge/docs_thesis/find_research.md` lines
  103-112). A continuous index thus related inversely to obstructive disease and positively, by
  territory, to ischemia.
- The knowledge bank's own reconciliation: "They agree once the endpoint is stated precisely:
  tortuosity tracks ischemia *without* obstructive stenosis ... and tracks *inversely* with
  obstructive stenosis (Groves, p = 0.003)." (`find_research.md` lines 116-119)
- Nannini 2024, cited at LR:112 only as a pipeline, reported "a negative correlation between
  tortuosity and calcific plaque volume" with a continuous three-dimensional measure
  (`knowledge/docs_thesis/literature.md` lines 60-65). A second continuous measure with an inverse
  association, already in the chapter's reference set.
- Tello Ayala: positive association, but "OR 1.09/SD (P<.001) for severe CAD (mild/moderate not
  significant)", and its discrete-curvature score correlates with the classical arc/chord index at
  only r = 0.116 (`papers/telloayala2026tortuosity.md`).
- Other genuine synthesis moves that hold: the Stone split between lumen narrowing and plaque growth
  (LR:52-55); Griffo's "the relevant flow information is recoverable from shape, but it does not show
  whether shape identifies the individuals at risk" (LR:80-81); the cross-sectional caveat after four
  studies with Glagov (LR:139-140); "Imaging can therefore refine an individual estimate beyond
  systemic factors" (LR:162).
- Within sections, the paragraphs are still mostly one author-year sentence per study in sequence
  (e.g. LR:125-133: Juan, Bekirçavuşoğlu, Tommasino in three consecutive sentences with no linking
  claim beyond the frame at LR:124).

### Inferences
- Under the house rule ("synthesis allowed only when every element is cited"), each element of
  LR:107-109 is cited, but the generalisation "continuous measures related positively" is false for
  one of the four elements. It is therefore a synthesis that fails the rule's own test, not merely a
  bold one.
- A correct version within the rules: frame the conflict by endpoint and by projection. For example,
  "Collectively, these studies related tortuosity inversely to obstructive stenosis and positively to
  ischemia without obstructive stenosis \cite{groves...,li...,zebicmihic...}, while Tello Ayala et al.
  (2026) found it higher with any RCA disease on two-dimensional angiograms." This is fully cited and
  keeps Zebić Mihić's measure point (only the continuous index found the ischemia associations).
- The Juan/Bekirçavuşoğlu/Tommasino run would read as synthesis with one gathering sentence, e.g.
  that all three measured the left main region on CCTA in referred patients against disease on the
  same scan, which LR:124 already half-says.

### Gaps
- Zebić Mihić is abstract-level (header LR:18). Which measure produced the "higher in
  non-obstructive" result (index or bend count) is not stated in the note; the full text should be
  checked before rewriting LR:107-109.

---

## 3. Critical appraisal: does each principal study get its limitation and an implication?

### Takeaway
Most principal studies now carry a limitation; the risk section is close to exemplary. The studies
still summarised without appraisal are Asakura, Kashyap, Garcha (implicit only), Groves, Li,
Zebić Mihić, Nannini, Bekirçavuşoğlu and Chan. Four appraisal sentences overreach or rest on
unverified detail.

### Cited Findings
Per study (LR line, limitation present?, implication stated?):

| Study | LR | Limitation | Implication | Note |
|---|---|---|---|---|
| Asakura 1990 | 42-45 | No (n = 5 only in table) | Mechanism premise | "Early foundational work by ..." is not author-as-subject and "foundational" is praise; abstract-only source carries "demonstrated" (refs.bib: "full text not read ... note n = 5, quote it with the sample size"). |
| van der Giessen 2009 | 46-48 | Yes, "inferred from its position rather than computed" | Implicit | Full text not read (refs.bib); header says "quotes to confirm by eye" (LR:15). Unverified. |
| Chatzizisis 2007 | 49-51 | Review, none needed | Systemic vs local | Fine. |
| Stone 2012 | 53-55 | Yes, via the endpoint split | Yes | Accurate against refs.bib note. |
| Kashyap 2022 | 58-61 | No (healthy left main, simulated WSS only) | Implicit (measure choice) | "significantly but weakly" needs the R2 value checked; refs.bib says only "highest coefficient of determination". |
| Garcha 2025 | 62-67 | "synthetic" stated, not drawn out | No | The only evidence for radius ratios, and synthetic. |
| Zhang 2024 | 68-72 | Yes, small set; authors' own novelty claim | Yes | Accurate: "compared to existing work which focused mainly on the diseased branches" (refs.bib). Omits that the best discriminator was a WSS multidirectionality index, not curvature ("TSVI ... AUC = 0.876 ... average curvature ... only for the whole trees", `papers/zhang2024curvature.txt` abstract). |
| Griffo 2026 | 75-81 | Yes | Yes | Overgeneralised: "the data were single vessels ... of patients who all went on to have an infarction" (LR:79-80). The note says the MI analysis compared lesions "within the same patients, all of whom went on to have an MI", but the 748 patients pooled FAME 2 (n = 520), FIRE (n = 371) and a future-culprit series (n = 187) (`papers/griffo2026wss.md` lines 21, 54). Only the infarction analysis had that property. |
| Givehchi 2018 | 88-90 | The finding is a limitation | Yes | Contains "two" in the prose (number rule). |
| Cui 2017 | 91-94 | Yes (phase) | Yes | Accurate against `papers/cui2017bifurcation.md` ("73.6° in systole vs 78.4° in diastole"). |
| Groves 2009, Li 2011 | 97-100 | No (2D angiography, binary severe tortuosity, sex/hypertension confounding) | Via LR:107 | See §2. |
| Zebić Mihić 2024 | 101-103 | No | Via LR:107, misread | See §2. |
| Tello Ayala 2026 | 104-106, 134-138 | Yes (circular label, modest discrimination) | Yes | Omits that both models included age and sex ("transformer (local profile + age + sex) ... logistic regression (global scalar + age + sex)", note). That detail would motivate the aim's age-and-sex baseline. |
| Nannini 2024 | 112-113 | No | No | Single centre, n = 281 (refs.bib); its inverse tortuosity-calcium finding is omitted. |
| Bransby 2026 | 114-117 | Yes (authors' conclusion) | No | The implication for an automated pipeline (breaks, error propagation to geometry) is not drawn. |
| Juan 2017 | 125-126 | Yes, "did not persist after adjustment" | Covered by LR:139 | Not in refs.bib note (only n and strata) nor in `find_research.md` lines 61-63. Abstract-level (LR:18). Unverified. |
| Bekirçavuşoğlu 2026 | 127-129 | No (referred, cross-sectional) | Covered by LR:139 | A ramus intermedius is a branching-pattern variant; it is the natural citation to motivate artery labelling, and it is not used that way. |
| Tommasino 2024 | 130-133 | Yes, two | Covered by LR:139 | Accurate. "reported in a single center that" is a split verb construction. |
| Han 2022 | 142-148 | Yes, timing and exclusion | Yes | "came closest to a prospective design" (LR:142) is inaccurate: Han is "A nested case-control substudy of ICONIC" (`papers/han2022plaque.md`), and the next paragraph cites serial cohorts (Sakellarios, Won) that are more prospective. The key individual-risk limitation is also missed: the main comparison was "Culprit precursors vs non-culprit lesions in the same patients" (note), so it shows *where* within ACS patients, not *who*. |
| Sakellarios 2017 | 150-152 | Yes, small group with established disease | Implicit (daughter branch, whole-tree) | Fine. |
| Won 2022 | 153-155 | Yes, two | Yes | Accurate. "a substantial share" for 35.6% is fine under the number rule. |
| Chan 2024 | 160-163 | No (referred, modest gains, industry authorship) | Yes | `papers/chan2024orfan.md`: "absolute AUC gains are modest: +0.016 to +0.030"; authors include "directors of Caristo, which sells the device". |
| Bergström 2021 | 164-166 | Yes | Yes | Accurate. |

### Inferences
- The pattern of omissions follows the section order: section 3 is appraised throughout, section 2
  appraises measurement studies but not tortuosity or extraction studies, and section 1 appraises
  the newer computational studies but not the foundations.
- Asakura's missing limitation matters more than it looks, because the whole mechanism rests on five
  post-mortem trees read only at abstract level. "Asakura and Karino (1990) traced the flow through
  five ..." would break the number rule, but "a small set of post-mortem trees" would not.
- The Han correction strengthens the gap rather than weakening it: Han and Griffo both compared
  lesions within patients who all had an event, so neither tested between-person risk. One cited
  sentence could gather them.

### Gaps
- Juan's adjustment result, van der Giessen's "inferred", and Kashyap's "weakly" cannot be
  confirmed from local notes; each needs a full-text check (the `paper-review` skill is designed for
  this).

---

## 4. The gap: warrant, absence claim, and mapping to the aims

### Takeaway
The gap paragraph is a large improvement: every premise carries a citation and the final claim is a
narrow conjunction (whole tree, automatic, general population, new plaque on a later scan) that
survives every counterexample in the reference set. Its weak points are an unqualified universal
"No study has", a premise contradicted by Tommasino ("geometry has not been tested in this role"),
a flow clause the thesis does not extend, and four aims left unmotivated.

### Cited Findings
- Gap paragraph: LR:168-177, ending "No study has measured the geometry of the whole coronary tree
  automatically in a general population and related it to new plaque on a later scan."
- Premise check:
  - "cross-sectional or have followed referred patients whose plaque was already present
    \cite{li..., telloayala..., han...}" (LR:169-170): supported. Li (events in referred CAD
    patients), Tello Ayala (cross-sectional), Han (existing lesions, normal-segment culprits
    excluded, `papers/han2022plaque.md`). Tommasino and Sakellarios would also fit and are not cited
    here.
  - "single bifurcations, single vessels or small sets of trees \cite{kashyap..., zhang...,
    griffo...}" (LR:171-172): supported for the three cited, but Garcha (LR:62) examined 230
    synthetic whole left trees (refs.bib), which is neither single nor small. "or synthetic trees"
    would make the clause exhaustive. The clause also describes flow studies, and INTRO's aim
    computes "branching angles, branch radius ratios and vessel curvature" without simulating flow,
    which the earlier report already noted ("places the size limitation in flow studies, a branch
    the thesis does not extend", report line 347).
  - Won and Bergström clauses (LR:173-175): supported by their notes ("measured no geometry";
    "cross-sectional and reports no geometry").
- Contradicted premise in section 3: "Imaging can therefore refine an individual estimate beyond
  systemic factors, but geometry has not been tested in this role." (LR:162-163). Tommasino's CLAP
  score combined the left main bifurcation angle with clinical variables into a patient-level score
  ("CLAP score: AUC 0.91 in development, 0.85 in external validation", `papers/tommasino2024clap.md`),
  and Han reported "AUC 0.766 with AGCs vs 0.733 without" (lesion-level, `papers/han2022plaque.md`).
  Both are cited in the same section. The sentence is defensible only if narrowed, e.g. "in
  individuals without plaque" or "in the general population".
- Warrant for the absence claim:
  - The search statement names no databases, window or date (LR:31-32), and the header says it is
    unconfirmed (LR:22).
  - The Bergström note's own open question: "Has SCAPIS published repeat CCTA or any centreline
    geometry? None found in this pass; worth a check before claiming that no general-population
    cohort has geometry." (`papers/bergstrom2021scapis.md`)
  - Chen 2024 EHJ-CVI (myocardial bridge, new plaque) is unread: "Paywalled ... Needs manual access
    through DTU Findit" (`find_research.md` line 654-655). It is the study most likely to sit near
    the "geometry and new plaque on a later scan" half of the claim, though a single anatomical
    variant is not whole-tree geometry.
  - Zhang 2024 frames its cross-sectional work as "plaque onset" (title and abstract), which an
    examiner might read as a counterexample unless the review's description (stenosed vs
    stenosis-free trees on the same scan, LR:69-70) is taken as the rebuttal.
- Mapping of the gap and review to INTRO's aims:

| Aim (INTRO) | Motivated in the review? | Evidence |
|---|---|---|
| Automatic whole-tree pipeline | Yes | Nannini (LR:112), Bransby (LR:114-117), Zhang's whole-tree claim (LR:71), Sakellarios daughter branch (LR:151-152), gap "whole coronary tree automatically" |
| Assign each vessel to its artery | No | No labelling literature. Bekirçavuşoğlu's ramus intermedius (LR:127-129) and Cui's LAD/LCX angle presuppose labelled branches but the link is not drawn. |
| Branching angles | Yes | Givehchi, Cui, Juan, Tommasino, Bekirçavuşoğlu |
| Branch radius ratios | Weakly | Only Garcha's synthetic diameter division (LR:63-67) |
| Vessel curvature | Yes | Kashyap, Zhang, Tello Ayala |
| Logistic regression vs transformer | Yes | Tello Ayala (LR:134-138), the best-motivated aim |
| Baseline of age and sex | No, and contradicted in wording | Gap says "adds to systemic factors" (LR:178); SCORE2 has five factors (LR:158); INTRO says "how much they improve on a baseline model of age and sex". Tello Ayala's age-and-sex covariates would motivate it but are not mentioned. |
| Per-artery models "since shear acts locally" | No | Tello Ayala is RCA-only, Garcha and Zhang left-tree-only, Bergström found plaque "most frequent in the proximal and mid LAD" (`papers/bergstrom2021scapis.md`); none of this is drawn together. |
| General population, longitudinal | Yes | Won, Bergström, gap |

### Inferences
- The absence claim is warranted as a conjunction, not as a universal. Rewording to "No study
  identified in this search has ..." costs nothing under the house rules and moves the burden onto
  the search statement, which then has to name its databases and window.
- The single highest-value fix for the gap is LR:162-163, because an examiner who has just read the
  Tommasino sentence three paragraphs earlier will see the contradiction.
- Labelling and per-artery modelling could be motivated with citations already in the reference set
  (Bekirçavuşoğlu, Tello Ayala RCA-only, Bergström proximal LAD) in one or two sentences; radius
  ratios need at least one clinical study beyond Garcha (the earlier report's must-cite list, report
  line 357).

### Gaps
- Whether SCAPIS or another general-population cohort has published centreline geometry or repeat
  CCTA was not checked (the Bergström note flags this).
- Chen 2024, Lee 2019 EMERALD and Stone 2018 PROSPECT ESS remain unread (header LR:20-21); their
  bearing on the absence claim is unknown.

---

## 5. Is the search statement adequate for rubric item 1?

### Takeaway
It lifts item 1 from 1 to 2. It is not adequate for 3: no named databases, no time window, no search
date, no stated inclusion criteria, and exclusions without reasons. The header admits it is
provisional.

### Cited Findings
- Statement: LR:31-33, quoted in §1.
- Header: "Search statement: CONFIRM databases and window with the user before submission." (LR:22)
- Rubric item 1 asks that the review "states what is covered, sources/time window, and what is
  excluded and why"; the BME objective asks to "plan, perform and document a structured and focused
  literature search" (standards_rubric.md lines 17, 130).
- SDU: longer sections "require more systematic documentation of search method, databases and terms"
  (standards_rubric.md line 74).

### Inferences
- A level-3 version needs about two more clauses: named databases (e.g. PubMed and Europe PMC, if that
  is what was used), a date window and search date, an inclusion criterion (geometry measured in human
  coronary arteries and related to WSS or disease), and one reason per exclusion (anomalous origins
  are a different mechanism; radiomics without geometry does not measure shape). Numbers in a search
  window (years) may conflict with the no-numbers rule; the author has to decide whether years count.
- "checked against Crossref and Europe PMC" describes bibliographic verification, which is good
  practice but is not a search source; as written it may read to an examiner as the search itself.

### Gaps
- The actual databases and window used could not be determined from local files.

---

## 6. Writing: flow, sentence length, repetition, uncited claims, banned phrasing, consistency

### Takeaway
Sentence-level quality is good and the house rules are almost entirely respected (no em dashes, no
two-comma insertions found, author-year subjects except one). The remaining issues are verb
repetition, a split-verb workaround for the comma rule, two uncited "most/rarely" generalisations,
one number word, and three inconsistencies with the introduction and style guide.

### Cited Findings
- Length: about 1,530 words, mean 23.2 words, max 38, none over 45 (script count). §12 target
  "about 1,600 words", "mean about 24 words, few under 15, none over 45". 14 of 66 sentences are
  under 15 words, which is more than "few".
- Verb and connective counts (grep, case-insensitive, whole words): found 14, reported 5, also 5,
  showed 3, whereas 3, later 3, although 3, demonstrated 2, despite 2, because 2. §12: "each
  connective from §5 used at most twice"; "whereas", "later", "although" exceed it, and "found"
  carries 14 study sentences.
- Split-verb construction (prepositional phrase between verb and that-clause), apparently a
  workaround for the no-inserted-clause rule: "Bekirçavuşoğlu et al. (2026) found in patients
  referred for CCTA that a ramus intermedius ..." (LR:127-128); "Tommasino et al. (2024) reported in
  a single center that ..." (LR:130); "Chan et al. (2024) showed in patients referred for CCTA that
  ..." (LR:160). Three in two pages reads as a tic.
- Author-as-subject exception: "Early foundational work by Asakura and Karino (1990) ... traced"
  (LR:42), also a praise adjective.
- Uncited field claims:
  - "these differences have been studied as a possible marker of who develops coronary plaque"
    (LR:29-30); Temov supports only the variation.
  - "Most clinical studies have instead compared geometry with disease seen on the same scan."
    (LR:124); a "most" claim without citation (rubric item 12 "no sweeping generalisations").
  - "Serial CCTA has followed plaque over longer periods, but rarely from a plaque-free start."
    (LR:149); "rarely" uncited.
  - "Because flow simulation is costly" (LR:74); low-risk, likely stated by Griffo.
  - "but geometry has not been tested in this role" (LR:163); uncited and contradicted (§4).
- Number in prose: "two standard reconstruction techniques" (LR:89). Minor, but the rule is stated
  without exception.
- Repeated model phrasing: "Despite these advances" (LR:168) is the model's 1.1.2 opener verbatim
  (style guide §7), now following a paragraph that ends on a limitation, which the earlier report
  also flagged ("near-verbatim from the model and follows a paragraph that ended on a limitation",
  report line 394).
- Odd frame: "Using vessel shape as a marker of plaque" (LR:40) means "a marker of who develops
  plaque"; as written it reads as localisation, against the individual-risk focus.
- Consistency with INTRO:
  - INTRO still cites the source the review deliberately excludes: "inconsistent definitions of
    geometry have produced conflicting findings \cite{han2022plaque,shen2026geometry}" (INTRO,
    limitations paragraph). The LR header says "shen2026geometry deliberately NOT cited (user)"
    (LR:10). If the exclusion is meant thesis-wide, INTRO breaks it; if review-only, the reader sees
    it in chapter 1 and not in chapter 2, which looks selective.
  - INTRO's limitation sentence ("Most studies relating geometry to plaque measured it in referred
    patients whose plaque was already present") and LR:169-170 are near-identical. The duplication is
    smaller than before but still present.
  - "adds to systemic factors" (LR:178) vs INTRO's "baseline model of age and sex".
  - INTRO typo outside the review: "scanned as second time".
- Style guide internal inconsistency: §12 says "Prose about 1,600 words plus the table (cap raised
  from 1,000 to 1,200 words by the user, 2026-10-04 ...)". The parenthetical contradicts the target.
- Table: rows follow text order and the Population/Modality/Outcome columns make the gap visible, as
  the earlier report recommended (report line 390). But the four tortuosity studies that carry the
  section 2 argument are only half present (Li and Tello Ayala in, Groves and Zebić Mihić out), and
  Tommasino, the only patient-level angle-to-outcome study, is absent. The caption's "grouped as in
  the text by mechanism, measurement and risk" is accurate.

### Inferences
- The "found" count is the main source of the residual summary feel; rotating to "reported",
  "observed", "related ... to", or folding two studies into one sentence would cut it by half
  without breaking the author-as-subject rule.
- The split-verb tic can be removed inside the rules by moving the population to the subject:
  "In patients referred for CCTA, Bekirçavuşoğlu et al. (2026) ..." would begin with a phrase and a
  comma, which is allowed (only material between two commas is banned).

### Gaps
- No spell check or LaTeX build was run (§12 asks for hunspell and zero undefined citations); not
  verified here.

---

## 7. Earlier weaknesses: fixed, remaining, and newly introduced

### Takeaway
All of the earlier "examiner can verify in minutes" errors are fixed, both earlier gaps have been
rebuilt with citations, and most of the must-cite additions are in. What remains is mainly
coverage (CAC, labelling, radius ratios, Chen 2024) and definitions. The rewrite introduced four
new problems, all of them claims that outrun a cited study.

### Cited Findings
Fixed (earlier source, now):
- Bransby misattribution and the Wang "therefore" join (report line 339): fixed; Wang removed (LR:9),
  Bransby now quotes the authors' conclusion (LR:116-117).
- Uncited gaps contradicted by Han and Griffo (report line 347): fixed; Han is discussed with its
  limits (LR:142-148), Griffo's design is stated (LR:78-81), the gap is cited (LR:169-175), and the
  "at most several hundred" clause is gone.
- "Li vs Tello Ayala contradiction is not noticed" (report line 17): noticed and addressed
  (LR:96-109), though the resolution is wrong (see New).
- Flat chain of one-study paragraphs, no subsections (appraisal §1): fixed; three sections with
  frames and closing limitations.
- Limitations almost never stated (appraisal §3): largely fixed (§3 table above).
- Overreach on abstract-level sources ("underlying cause", "established", "clearly"; report line
  91-92): fixed; Chatzizisis now "implicated" (LR:49), Kashyap "significantly but weakly" (LR:60).
- Missing Stone 2012, PARADIGM, ORFAN, SCAPIS, Han, Zhang, Groves, Givehchi, Nannini, angle studies
  (report line 94): all added.
- No search statement or roadmap (report line 95): both added (LR:31-35).
- Table without comparison axes (report line 390): fixed with Population/Modality/Outcome columns.
- 46-word sentence, "these two elements" referent, duplicated "Their work demonstrated", "large
  populations" repetition (report line 394): fixed.
- Individual-risk breaches (opening, Wang paragraph, risk sentence; report line 390): fixed; the
  opening now names "who develops coronary plaque" (LR:29-30) and Griffo's limit is framed around
  individuals (LR:81).

Remaining:
- Terminology undefined (accepted residual).
- CAC absent (report line 13 and 94).
- Artery labelling and radius ratios without literature (report line 357).
- Chen 2024, EMERALD and PROSPECT ESS unread (report line 94; header LR:20-21).
- Sex and hypertension confounding of tortuosity (report line 16).
- Search statement without databases and window (report line 11; header LR:22).
- Introduction overlap and the INTRO citation of shen2026geometry (appraisal §6).
- "Despite these advances" model phrasing (report line 394).
- Flow-study clause in the gap that the thesis does not extend (report line 347).
- Alignment of the significance sentence with the age-and-sex baseline (report line 93, item 4).

New problems introduced by the rewrite:
1. The measure-type reconciliation (LR:107-109) contradicts Zebić Mihić and Nannini (§2).
2. "geometry has not been tested in this role" (LR:162-163) contradicts Tommasino's CLAP score (§4).
3. "Han et al. (2022) came closest to a prospective design" (LR:142) mischaracterises a nested
   case-control study and sits awkwardly before two serial cohorts (§3).
4. Griffo's design sentence over-extends the infarction subset to all data (LR:79-80) (§3).
5. Minor: "found" repetition from the longer text, the split-verb construction, "two" in the prose,
   the "Early foundational work by" opener, and unverified appraisal details (Juan, van der Giessen,
   Kashyap) now carrying weight that abstracts may not support.

### Inferences
- The earlier report's conclusion ("The chapter's problem is not effort or style but evidence
  management", report line 408) still applies, in a smaller form: the knowledge bank already contains
  the facts that correct each new problem (`find_research.md` lines 116-119; `papers/tommasino2024clap.md`;
  `papers/han2022plaque.md`; `papers/griffo2026wss.md`).

### Gaps
- None beyond those listed under §3 and §4.

---

## 8. Concrete remaining fixes, prioritised, compatible with the house rules

### Takeaway
Six sentence-level corrections (about 150 words changed) remove every new error and lift items 7,
11 and 15. Three short additions close the aim-motivation holes. The search statement and the
unread full texts are the pre-submission tasks.

### Cited Findings (each fix is tied to the evidence above)
Priority 1, factual (an examiner can check each one):
1. Rewrite LR:107-109 by endpoint rather than measure type, citing Groves, Li, Zebić Mihić and Tello
   Ayala; keep Zebić Mihić's point that only the continuous index found the ischemia associations;
   optionally add Nannini's inverse calcium finding. Verify Zebić Mihić's full text first (§2 Gaps).
2. Narrow LR:163 to "but geometry has not been tested in this role in individuals without plaque"
   (or "in the general population"), since Tommasino's CLAP score combined the angle with clinical
   variables (§4).
3. LR:142: replace "came closest to a prospective design" with a description that fits a nested
   case-control study, and add that culprits were compared with other lesions in the same patients,
   so the design addresses where rather than who (`papers/han2022plaque.md`).
4. LR:79-80: restrict "patients who all went on to have an infarction" to the infarction analysis
   (`papers/griffo2026wss.md`).
5. LR:176-177: "No study identified in this search has ..."; add "or synthetic trees" to LR:171-172,
   or drop the flow clause, since the thesis does not simulate flow.
6. LR:178: align "adds to systemic factors" with the aim (age and sex), or add Tello Ayala's age and
   sex covariates (LR:134) so that the baseline is motivated.

Priority 2, aim motivation (one or two sentences each, all from held citations):
7. Labelling: one sentence noting that the ramus intermedius result (Bekirçavuşoğlu) and the LAD/LCX
   angle (Cui, Juan) presuppose that branches are assigned to named arteries; if a labelling study is
   to be cited it has to be read first (none is in the reference set).
8. Per-artery models: gather Tello Ayala (RCA only), Garcha and Zhang (left tree only) and Bergström
   (proximal LAD predilection) in one cited sentence.
9. Radius ratios: one clinical study beyond Garcha, from the earlier must-cite list (report line 357).
10. CAC: one sentence beside Chan on calcium scoring as the established imaging refinement of risk,
    once a source is read.

Priority 3, appraisal completeness:
11. One limitation clause each for Kashyap (healthy left main, simulated WSS), Nannini (single
    centre), Chan (referred, modest gains), and Groves/Li (two-dimensional angiograms, sex and
    hypertension confounding), using design words, not numbers.
12. Asakura: "a small set of post-mortem trees" in place of "Early foundational work by", restoring
    author-as-subject and removing the praise adjective.
13. Confirm by full text: Juan "did not persist after adjustment", van der Giessen "inferred ...
    rather than computed", Kashyap "weakly" (paper-review skill).

Priority 4, writing:
14. Cut "found" from 14 to about 7; keep "whereas", "later", "although" to two each (§12).
15. Replace the three split-verb sentences by a fronted population phrase ("In patients referred for
    CCTA, ...").
16. Cite or soften LR:124 ("Most clinical studies") and LR:149 ("rarely"), e.g. by restating them
    as properties of the cited studies.
17. Replace "Despite these advances" (LR:168) with a gap opener that follows from a limitation, e.g.
    "Taken together, ...".
18. Remove "two" at LR:89 ("the standard reconstruction techniques").
19. Reframe LR:40 as "a marker of who develops plaque".

Priority 5, cross-chapter and pre-submission:
20. Decide whether shen2026geometry is excluded thesis-wide; if so, replace it in INTRO with
    Zebić Mihić or Kashyap for the "inconsistent definitions" claim.
21. Complete the search statement (databases, window, search date, inclusion criterion, one reason
    per exclusion) and remove the CONFIRM note from the header (LR:22).
22. Read Chen 2024, and check SCAPIS for geometry or repeat CCTA, before the absence claim is final.
23. Add Groves, Zebić Mihić and Tommasino rows to the table so the tortuosity conflict and the only
    patient-level angle-outcome study are visible; fix the §12 parenthetical in the style guide.

### Inferences
- Fixes 1 to 6 together would plausibly raise items 7, 11 and 15 to 3, giving about 38/45; fixes 7
  to 13 would add item 8 and item 6, giving about 40/45, the realistic ceiling under the current
  house rules (items 5 and 14 capped by rule).
- None of the fixes requires numbers in the prose, concept definitions, inserted clauses, em dashes
  or citing shen2026geometry. Fix 21 may require years in the search window; that is the one place
  the no-numbers rule may need an explicit exception.

### Gaps
- The word cost of Priority 2 and 3 additions (estimated 150 to 250 words) would push the prose to
  about 1,700 to 1,800 words, above the §12 target of about 1,600; the author would need to accept
  that or trim elsewhere (e.g. the Givehchi/Cui paragraph).
