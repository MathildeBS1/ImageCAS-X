# Style guide: writing the State of the Art (after Jiménez Ordoñez, 2026, Section 1.1)

Source: `Former_students_work/AidaJimenez_MasterThesis_s243279.pdf`, Section 1.1 "State of the
Art" (pp. 5 to 7). Every count below was taken from a text extraction of that section only
(prose, excluding Table 1.1). Every quoted phrase is verbatim. For her register across the whole
thesis, see `style_guide_aida.md`; this file covers only the literature review.

Where her habits clash with the `thesis-writing` skill or with standing instructions for this
thesis, the clash is flagged in §10 and the rule there wins.

---

## 1. The section at a glance

| Property | Aïda §1.1 |
|---|---|
| Position | Inside Chapter 1, after the introduction prose and before "1.2 Aim of the Thesis" |
| Length | about 1,020 words of prose plus a 4-row table; 3 pages |
| Subsections | 3, each with a Title-Case noun-phrase heading |
| Paragraphs | 3 per subsection on average, 3 to 6 sentences each |
| Sentences | 42; mean 24 words, median 24.5, range 7 to 57 |
| Citations | 17 numeric brackets; 15 author-year mentions in the text |
| Numbers from studies | 4 in total (8 kHz, 1.8 mm, 169 subjects, "factor of three") |
| Figures, equations | none; one table at the very end |
| First person, "this thesis" | none; the thesis enters only as "this gap" and "a progression toward" |
| References to later sections | none |

The section is a self-contained narrative. It never points forward, and the Aim section that
follows picks up from its final gap.

## 2. Macro-architecture: three strands, one direction

Her subsections are not topics placed side by side. Each one answers the question the previous
one raises:

| Subsection | Question it answers | Ends on |
|---|---|---|
| 1.1.1 Anatomical Characterization of the Human Ear | Why does the object's geometry matter, and how much does it vary? | Generic geometry introduces error, so realistic anatomy is essential |
| 1.1.2 AI-Driven Models for Ear Segmentation | How is that geometry obtained from images? | Methods cover the wrong structures; "Bridging this gap is essential for ..." |
| 1.1.3 Three-Dimensional Finite Element Models of the Ear | What is the geometry used for downstream? | "a significant gap remains"; integration of 1.1.2 with 1.1.3 is the way forward; table |

The order runs from **the object**, through **the means of measuring it**, to **its application**.
The final gap merges the last two strands ("The integration of AI-based segmentation with such
high-fidelity FE modelling ..."), which is exactly what the Aim then proposes.

**Headings** are noun phrases in Title Case naming the strand, never a claim:
*Anatomical Characterization of the Human Ear*, *AI-Driven Models for Ear Segmentation*,
*Three-Dimensional Finite Element Models of the Ear*.

## 3. Paragraph architecture inside a subsection

Every subsection follows the same three-move pattern.

**Move 1. Frame (1 sentence).** A general claim stating what the strand is needed for. It is
uncited and written in the present tense.

**Move 2. Chronology (1 to 2 paragraphs).** Studies in time order, each introduced by a
chronological or additive connective, usually one or two sentences per study.

**Move 3. Synthesis and gap (1 paragraph).** It opens with *Collectively* or *Despite these
advances/advancements*, states what the strand still lacks, and ends on why closing that gap
matters.

The three subsections, sentence by sentence:

**1.1.1 (frame, then six studies, then synthesis)**
1. Frame: *Accurate prediction of vibroacoustic behaviour in the ear fundamentally depends on a realistic geometric representation of the ear canal.*
2. *Early foundational work by Stinson (1989) [11] demonstrated that ...*
3. *This finding established that ...*
4. *Subsequent research has further refined the clinical and anatomical understanding of ...* (a topic sentence for the paragraph)
5. *Nielsen and Darkner (2011) [8] identified that ...* then *Crucially, they highlighted the necessity of ...*
6. *Complementing this, Abdala and Keefe (2012) [12] examined ...* then *Their work demonstrated that ...*
7. *Large-scale geometric studies have further revealed substantial inter-individual variability in ...* (topic sentence)
8. *Voss et al. (2020) [6] analysed ..., demonstrating that ...*
9. *Advancing this further, ... investigations by Balouch et al. (2023) [10] quantified ..., reporting that ...*
10. *Most recently, Voss et al. (2025) [7] provided a comprehensive ... analysis ...* then *Their findings indicate that ...*
11. Synthesis: *Collectively, these findings highlight that ...* then *In computational vibroacoustic modelling, assuming a generic geometry introduces systematic errors.* then *Therefore, realistic anatomical representation is essential to ensure ...*

**1.1.2 (frame, early methods, deep learning, gap)**
1. Frame: *The generation of anatomically realistic computational models relies on precise segmentation of medical imaging data.*
2. *Early approaches often used semi-automated geometric modelling.* then *For example, Poznyakovskiy et al. (2011) [13] proposed ...* then *While effective for ..., these workflows required substantial user intervention and were difficult to scale ...*
3. *Recent advances in deep learning have enabled fully automated segmentation pipelines, improving both efficiency and reproducibility.*
4. *Hussain et al. (2021) [14] introduced ..., achieving ...* then *Similarly, Neves et al. (2021) [15] demonstrated that ...*
5. *MRI-based segmentation has also benefited from neural network architectures.* then *Vaidyanathan et al. (2021) [16] applied ...* then *Stebani et al. (2023) [17] extended this approach to ..., demonstrating ...*
6. Gap: *Despite these advances, the majority of studies remain focused on ..., and few provide ...* then a near miss: *... methods ..., such as ... Dritsas et al. (2024) [1], have enabled ...* then *However, these approaches are not directly applicable to ...* then *Bridging this gap is essential for producing ...*

**1.1.3 (frame, studies, review, gap, table)**
1. Frame: *Three-dimensional finite element (FE) modelling enables explicit representation of ..., overcoming the constraints of simplified approaches.*
2. *Brummund et al. (2014) [9] reconstructed ... and modelled ...* then *Their simulations demonstrated how ...*
3. *More anatomically comprehensive FE frameworks have since emerged.* then *Elghanaoui et al. (2025) [18] developed ...* then *Validation against experimental benchmarks showed ..., underscoring the value of ...*
4. *Additional studies have established methodological foundations for ...* then *Chen and Lee et al. [19, 20] developed ...* then *Subsequent work by Wang et al. [21, 22] explored ..., illustrating how ...* then *A comprehensive review by Cheng et al. (2022) [23] highlighted the role of ...*
5. Gap: *Despite these advancements, a significant gap remains in current state-of-the-art modelling.* then *Existing frameworks often lack ...* then *Establishing such a model is essential, as ...* then *The integration of [strand 2] with [strand 3] represents a progression toward ...*
6. Table pointer: *An overview of the state of the art regarding ... is summarized in Table 1.1.*

## 4. Opening sentences

Each subsection opens with a frame sentence that names what the field **depends on**, **relies on**
or **enables**. All three openers carry no citation and use the present tense.

| Template | Her sentence |
|---|---|
| *Accurate [task] of [object] fundamentally depends on [requirement].* | Accurate prediction of vibroacoustic behaviour in the ear fundamentally depends on a realistic geometric representation of the ear canal. |
| *The [product] relies on precise [method] of [data].* | The generation of anatomically realistic computational models relies on precise segmentation of medical imaging data. |
| *[Method] enables explicit representation of [X], overcoming the constraints of simplified approaches.* | Three-dimensional finite element (FE) modelling enables explicit representation of ear anatomy, tissue mechanics, and acoustic–structure interaction, overcoming the constraints of simplified approaches. |

The requirement named in the first opener (realistic geometry) is the thread the next two
subsections pick up (obtaining it, then using it).

## 5. The chronological ladder

Studies are ordered by year inside each strand, and the connective signals where on the timeline
the study sits. These are her connectives, in the order she uses them:

| Position | Connective (verbatim) |
|---|---|
| First study | *Early foundational work by A (year) [n] ...* / *Early approaches often used ...* |
| Next study, same line | *Subsequent research has further refined ...* / *Subsequent work by A [n] explored ...* |
| Parallel study | *Complementing this, A (year) [n] ...* / *Similarly, A (year) [n] ...* |
| Larger or deeper study | *Large-scale ... studies have further revealed ...* / *Advancing this further, ...* |
| Method extension | *A (year) [n] extended this approach to ...* |
| Shift in the field | *Recent advances in deep learning have enabled ...* / *More ... frameworks have since emerged.* / *X has also benefited from ...* |
| Supporting body of work | *Additional studies have established methodological foundations for ...* |
| Review | *A comprehensive review by A (year) [n] highlighted ...* |
| Latest study | *Most recently, A (year) [n] provided ...* |

Rules she follows:
- **Field-level topic sentences** (*Large-scale geometric studies have further revealed ...*,
  *MRI-based segmentation has also benefited from ...*) announce a group of studies before naming
  them, so the reader knows why the next two citations belong together.
- **Never two connectives of the same kind in a row.** *Subsequent* is followed by *Complementing*,
  then *Large-scale ... further*, *Advancing this further*, and *Most recently*.
- **Each connective is used once or twice in the whole section:** *Subsequent* 2, *Early* 3,
  *Complementing* 1, *Similarly* 1, *Most recently* 1, *Collectively* 1, *Despite* 2,
  *However* 1, *Therefore* 1.

## 6. The study sentence

### 6.1 Formula

> **[Author] et al. ([year]) [n] + [action verb, past] + [what they did], + [participle] + [what it showed].**

> Voss et al. (2020) [6] analysed silicone moulds from 169 subjects, **demonstrating** that
> cross-sectional areas are generally larger than previously assumed and tend to increase with age.

> Hussain et al. (2021) [14] introduced AutoCasNet for micro-CT segmentation of inner ear
> structures, **achieving** high accuracy while significantly reducing processing time.

When the finding needs room, she uses two sentences: the first says what they did, and the second
opens on an anaphor, *This finding ...*, *Their work ...*, *Their findings ...* or
*Their simulations ...*, followed by *demonstrated / indicate / established*.

> Abdala and Keefe (2012) [12] examined the developmental trajectory of canal geometry from
> infancy through adolescence. **Their work demonstrated that** the maturation of the canal's
> central axis and entrance morphology significantly alters audiological measurements over time.

### 6.2 Citation placement

- Author and year appear in the text, with the numeric bracket **immediately after the year**:
  *Stinson (1989) [11]*, not at the end of the sentence.
- Two authors are named in full (*Nielsen and Darkner (2011)*); three or more become *et al.*
- Groups of papers by one team are cited once, without a year: *Chen and Lee et al. [19, 20]*,
  *Wang et al. [21, 22]*.
- Each study is cited once, in its first sentence. The follow-up sentence (*Their work ...*) is
  not cited again.
- Frame, synthesis and gap sentences carry **no citation**.

### 6.3 Verbs

The action verb says what the study did; the reporting verb says what it showed.

| Role | Verbs (count in §1.1) |
|---|---|
| What they did | analysed 1, examined 1, identified 1, quantified 1, proposed 2, introduced 1, applied 1, developed 2, reconstructed 1, explored 1, extended 1, provided 1 |
| What it showed | demonstrated 4 (+ demonstrating 2), highlighted 2 (+ highlight 1, highlighting 1), established 2, revealed 1, refined 1, showed 1, indicate 1 |
| Participial tail | demonstrating, achieving, reporting, highlighting, illustrating, underscoring, employing |

Strength ladder: *indicate* < *showed* < *demonstrated* < *established*. She keeps
*established* for a finding that later work built on (*This finding established that simplified
geometries cannot ...*).

## 7. Synthesis and gap rhetoric

Each subsection ends by turning from what was found to what is missing. The three gaps escalate.

| Subsection | Gap pattern | Verbatim |
|---|---|---|
| 1.1.1 | Synthesis, consequence, requirement | *Collectively, these findings highlight that ...* / *In computational vibroacoustic modelling, assuming a generic geometry introduces systematic errors.* / *Therefore, realistic anatomical representation is essential to ensure ...* |
| 1.1.2 | Coverage gap, near miss, bridge | *Despite these advances, the majority of studies remain focused on ..., and few provide ...* / *However, these approaches are not directly applicable to ...* / *Bridging this gap is essential for producing ...* |
| 1.1.3 | Explicit gap, what is lacking, why, way forward | *Despite these advancements, a significant gap remains in current state-of-the-art modelling.* / *Existing frameworks often lack ...* / *Establishing such a model is essential, as ...* / *The integration of ... represents a progression toward ...* |

Note the variation: *advances* in 1.1.2 and *advancements* in 1.1.3, so the two *Despite*
sentences do not read as repeats.

The **near miss** in 1.1.2 is worth copying. She names the closest existing method (Dritsas et
al. 2024), credits it, then says in one *However* sentence why it does not answer the question.

## 8. The closing table

| Element | Her choice |
|---|---|
| Position | After the last paragraph of 1.1.3, introduced by *An overview of the state of the art regarding ... is summarized in Table 1.1.* |
| Scope | Only the studies of the final strand (4 rows), not the whole section |
| Columns | Author & Year / Tissues Included / Segmentation Approach / Main Findings |
| Row order | The order in which the studies appear in the text |
| Findings cell | One clause, present tense, no citation: *Occlusion increases low-frequency pressure via wall impedance.* |
| Caption | *Overview of state-of-the-art [X], highlighting [column 2], [column 3], and main conclusions.* |

The middle columns are the comparison axes that make her gap visible: tissues (none includes
all) and segmentation approach (all manual or semi-manual).

## 9. Register and vocabulary

**Tense.** Past for what a study did and found (*identified*, *demonstrated*). Present perfect for
trends in the field (*have enabled*, *have since emerged*, *has also benefited*). Present for
frames, synthesis and gaps (*depends on*, *remain focused*, *is essential*).

**Evaluative words (count in about 1,020 words):** essential 3, substantial 3, comprehensive 3,
realistic 3, high 3, significantly 2, necessity 2, consistent 2, accurate 2 (+ accurately 2),
crucially 1, robust 1, strong 1, effective 1, high-fidelity 1. She uses evaluative words
sparingly, about one per hundred words, and mostly in frames and gaps rather than in study
sentences.

**Anaphora as glue:** *this* 7, *these* 5, *their* 3, always followed by a noun (*This finding*,
*these workflows*, *these approaches*, *Their simulations*).

**Absent:** first person, "this thesis", rhetorical questions, section references, figure
references, numbers compared across studies, criticism of a single study's method beyond one
concessive clause (*While effective for inner ear structures, these workflows required ...*).

## 10. Adapting it to this thesis: where her habits must change

| Her habit | Rule for this thesis | Source of the rule |
|---|---|---|
| Synthesis and gap sentences are her own inference (*In computational vibroacoustic modelling, assuming a generic geometry introduces systematic errors.*) | **No conclusions of our own.** Every synthesis or gap sentence must restate what a cited study demonstrated or stated, for example a review's own stated limitation or an author's own future work. *Collectively* may only gather findings already cited. | User instruction, 2026-10-04 |
| Few numbers; qualitative findings (*high accuracy*, *expert-level performance*, *strong agreement*) | **No numbers in the prose.** State findings qualitatively (*curvature explained the most variance*, *the transformer predicted CAD better*). Cohort sizes may appear in the table only. | User instruction, 2026-10-04 (neither former thesis reports numbers in its review) |
| Frame sentences uncited | Keep the frame uncited only if it is definitional. If it states a fact about the field (e.g. what risk scores include), cite it. | `thesis-writing` skill, sourcing |
| Research question implicit | The thread is **who develops plaque** (individual risk), never where plaque forms. Localization studies appear only as mechanism. | Memory: `project_research_focus_risk.md` |
| Glosses in the main clause are rare | Same: no mid-sentence glosses. A definition gets its own sentence, or follows directly after the abbreviation. | `style_guide_aida.md` §2.7 |
| Occasional inserted clause between two commas | **No inserted clauses.** Nothing is set off between two commas inside the main clause: no *, how its vessels bend and branch,*, no *, by Li et al. (2011),*, no *, however,*. Make the author the subject (*Li et al. (2011) conducted one of the first ...*), move the connective to the front (*However, the same two techniques ...*), or give the extra information its own sentence. | User instruction, 2026-10-04 |
| *Crucially*, *essential*, *significant gap* | Allowed at her rate (once or twice per section), never as praise for a study. | User request to match her phrasing; skill bans praise adjectives |
| No forward references | Same: no `\ref` to later sections, no mention of our own results or methods. | User instruction, 2026-10-04 |
| Em dashes | Never. She uses en dashes only inside compounds (*device–tissue*). | `style_guide_aida.md` §8 |

### Mapping her three strands onto ours

| Her strand | Ours | Ends on (sourced) |
|---|---|---|
| Why the object's geometry matters | Coronary Geometry as a Risk Factor: risk scores are systemic only; WSS mechanism; geometry sets low-WSS exposure; geometry varies between people | Shen et al. (2026): large-population studies are limited; the whole tree is rarely studied |
| How the geometry is obtained | AI-Based Extraction of the Coronary Tree: minimum cost path, CAT08, CNN tracking, U-Net/nnU-Net, ImageCAS, ImageCAS-X | Bransby et al. (2026): automated methods do not yet match human agreement, with breaks in every method |
| What the geometry is used for | Coronary Geometry as a Predictor of Disease: angle and tortuosity versus CAD; machine-learning prediction | Shen et al. (2026) on population size and selection; Zhang et al. (2024) on missing healthy follow-up; then the table |

## 11. Templates

**Frame (one per subsection, rotate the verb):**
> *Accurate [prediction / measurement] of [X] [fundamentally] depends on [Y].*
> *The [measurement / generation] of [X] relies on [precise / automatic] [Y].*
> *[Method] enables [explicit / automatic] [Z], overcoming [stated limitation of earlier work].*

**One study, one sentence:**
> *[A] et al. ([year]) \cite{} [did X] in [n] [cohort], demonstrating that [finding].*

**One study, two sentences:**
> *[A] et al. ([year]) \cite{} [did X] in [n] [cohort].*
> *Their [work / findings / simulations] [demonstrated / indicate] that [finding].*

**Field shift:**
> *Recent advances in [field] have enabled [capability], improving both [A] and [B].*

**Sourced synthesis (this thesis's version of *Collectively*):**
> *Collectively, these studies [showed / reported] that [restatement of cited findings only].*

**Sourced gap:**
> *Despite these advances, [Author] et al. ([year]) \cite{} [noted / identified / reported] that [their stated limitation].*
> *[Author] et al. ([year]) \cite{} [added / likewise named] [second stated limitation].*

**Table pointer (last sentence of the section):**
> *An overview of [the studies relating X to Y] is given in Table~\ref{tab:literature}.*

## 12. Checklist before calling the section done

- [ ] Three subsections, Title-Case noun-phrase headings, ordered object → extraction → use.
- [ ] Each subsection opens with an uncited (or definitional) frame sentence: *depends on / relies on / enables*.
- [ ] Studies chronological within each strand; each connective from §5 used at most twice.
- [ ] Every study sentence: author and year as the subject, `\cite` right after the year, the cohort described in words.
- [ ] Each subsection ends on a gap that a cited source stated, not one we inferred.
- [ ] No `\ref` to later sections, no "this thesis", no own results.
- [ ] One table at the end, columns chosen to make the gap visible, rows in text order, one-clause findings.
- [ ] Prose about 1,600 words plus the table (cap raised from about 1,200 to about 1,600 words by the user, 2026-10-04, to make room for appraisal and synthesis).
- [ ] Synthesis is allowed when every element of it is cited (a *Collectively* sentence that compares cited findings is fine; an uncited inference is not).
- [ ] Sentence length near hers: mean about 24 words, few under 15, none over 45.
- [ ] No em dashes, no `\textbf`, no praise adjectives; *essential* and *Crucially* at most twice.
- [ ] No inserted clauses between two commas inside a sentence; no numbers in the prose.
- [ ] `hunspell -l -t -d en_US -p wordlist.txt` returns only names; build with zero undefined citations.
