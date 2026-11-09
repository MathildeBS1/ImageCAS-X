# Style guide: writing the Clinical Background (after Jiménez Ordoñez, 2026, Chapter 2)

Source: `Former_students_work/AidaJimenez_MasterThesis_s243279.pdf`, Chapter 2 "Clinical
Background" (pp. 9 to 14). Counts come from a text extraction of that chapter only (prose, figure
captions and equations excluded where stated). Quoted phrases are verbatim. For her register across
the whole thesis see `style_guide_aida.md`; for the literature review see
`style_guide_sota_aida.md`. This file covers only the clinical chapter. Her Chapter 3 (Technical
Background) is in `style_guide_technical_aida.md`.

Where her habits clash with the `thesis-writing` skill or with standing instructions for this
thesis, the clash is flagged in §9 and the rule there wins.

---

## 1. The chapter at a glance

| Property | Aïda Ch. 2 |
|---|---|
| Length | about 1,600 words including captions and equations, 6 pages |
| Sections | 2, each with one or two subsections (2.1.1; 2.2.1, 2.2.2) |
| Paragraphs | 2 to 4 per section or subsection, 3 to 7 sentences each |
| Sentences | about 56; mean 29 words, median 26 |
| Citations | 16 numeric brackets; no author names in the text |
| Figures | 4, each cited before it appears, all adapted or schematic |
| Equations | 6, all in the last subsection |
| Chapter-opening paragraph | none; Section 2.1 starts directly |
| First person | none |
| Forward references | none |

The chapter is short on purpose. It teaches exactly the anatomy and the one device mechanism that
her later chapters use, and nothing else.

## 2. Macro-architecture: general to specific, ending on the thesis's object

Each section narrows from the system to the one property the thesis depends on.

| Section | Funnel | Ends on |
|---|---|---|
| 2.1 Ear Anatomy | three regions, then the outer ear and canal, then the membrane | the two-tissue canal (2.1.1), with the junction between them |
| 2.2 Hearing Aids | what a hearing aid does, then the in-the-ear form factor, then the deepest subtype, then its failure mechanism | vibroacoustic feedback and the quantity that measures it |

The last paragraph of a section states why the narrowing mattered:

> For this reason, the explicit distinction between soft tissue and bone is particularly relevant
> for vibroacoustic modelling of the ear canal.

> Consequently, ITE devices, and IIC hearing aids in particular, are highly relevant for studies
> of ear canal biomechanics, vibroacoustic feedback, and structure-borne sound transmission,
> where these factors play a central role.

The thesis is named only in a property ("relevant for ... modelling"), never in a forward pointer
to a chapter.

## 3. Paragraph architecture

### 3.1 The opening sentence names the system and its parts

> The anatomy of the human ear is a sophisticated system divided into three primary regions: the
> outer, middle, and inner ear (Figure 2.1).

> Hearing aids are small electronic medical devices designed to support individuals with hearing
> loss by improving access to sound.

One sentence of what it is, one of how it divides, and the figure is cited in the first paragraph.

### 3.2 Structure, then function, then consequence

> The TM forms the anatomical boundary between the ear canal and the middle ear. As a thin,
> conical, and multilayered membrane, it acts as both an acoustic receiver and a mechanical
> transducer, converting incident sound pressure into mechanical vibrations. These vibrations are
> subsequently transmitted through the ossicular chain, a process that is fundamental to efficient
> sound conduction toward the cochlea.

Sentence 1 locates the structure. Sentence 2 says what it does, with the participial tail
(*converting ...*) carrying the mechanism. Sentence 3 follows the energy or the blood onward to the
next structure.

### 3.3 Contrast between two parts in one sentence, then split the paragraph

> The outer segment is primarily cartilaginous and covered by a dermal layer of approximately 1 mm
> thickness, while the medial segment is osseous and lined by a much thinner epithelial layer of
> approximately 0.1 mm [8].

The next paragraph opens *In contrast, ...* for the second part. A paragraph describes one
structure.

### 3.4 Two-step relevance closure

The weight of a paragraph is carried by its last sentence, introduced by *Therefore*, *As a
result*, *For this reason* or *Consequently* (1 each in the chapter, so about one per section).
The connective is followed by a concrete property of the thesis's object, not a general remark on
importance.

> As a result of this deep insertion, IIC hearing aids interact not only with cartilaginous soft
> tissue but also with the bony portion of the ear canal.

## 4. How terms are introduced

- The abbreviation goes in brackets directly after the first full term: *tympanic membrane (TM)*,
  *sound pressure level (SPL)*, *maximum acoustic gain before feedback (MAGBF)*. After that only
  the abbreviation is used. No bold, no italics, no quotation marks.
- A definition is attached as a trailing clause: *the highest amplification that can be applied
  before sustained oscillation occurs*. A longer one gets its own sentence.
- Alternative names appear once, with *referred to as* or *commonly referred to as*:
  *The transition between these regions, referred to as the CBJ, ...*.
- Contrasts that fix a term are made with *Unlike X, where ..., Y is ...*:

> Unlike acoustic feedback, where amplified sound leaks from the ear canal and re-enters the
> microphone through an airborne path, vibroacoustic feedback is transmitted through these coupled
> pathways within the device-body system [3].

## 5. Numbers, citations, figures

**Numbers.** Always a range with a unit and a citation in the same clause. *typically measuring
between 20 and 37 mm in length, with a diameter ranging from 4.5 to 11 mm [8]*. Thicknesses carry
*approximately* (2 uses). No population is stated, because the numbers are textbook anatomy.

**Citations.** One bracket at the end of the clause it supports, up to four together where several
papers describe one mechanism (*[2, 3, 29, 30]*). Review or textbook sources dominate. Author names
never appear; those belong to the literature review.

**Figures.** 4 in 6 pages, each cited with *(Figure 2.1)* inside the first paragraph that needs it.
Captions are one to two sentences: what the figure shows, what it highlights, source.

> Figure 2.1. Overview of human ear anatomy, highlighting the outer, middle, and inner regions, as
> well as principal external ear components, associated tissue types, and the tympanic membrane.
> Adapted from [24].

Schematic curves are flagged as such: *It should be noted that both the gain and MAGBF curves are
illustrative, as their exact shape depends on the specific hearing-aid design and fitting
strategy.* The same sentence is repeated in the caption (*The curves are illustrative*).

## 6. Equations in a background chapter

Used only for the one quantity the results depend on, built up as a chain in one subsection.

1. Define it in running text: *The sound pressure level (SPL) is defined as:*
2. Equation.
3. *where* sentence naming each symbol with its unit and the reference value.
4. One sentence on what the quantity allows: *This representation enables consistent evaluation of
   pressure levels at different locations within the system.*
5. The next quantity starts from the last: *Based on this definition, the maximum acoustic gain
   before feedback (MAGBF) quantifies ...*, then *To further quantify this behaviour, the feedback
   margin (FBM) is defined as:*.
6. The curves are read in words afterwards, in the order *In general ... In contrast ...
   Beyond this region ...*.

Six equations in about two pages is her ceiling. The derivation (stability condition, then
approximation, then substitution) is written as a short run of prose sentences between equations,
each starting *The ...* or *Substituting ...*. No proofs.

## 7. Tense, voice and verbs

Present tense, active, throughout. No past passive, because nothing has been done yet. Modals are
*can* (38, far her most frequent) and *may* (2). Nothing is hedged with *seems* or *appears*.

| Job | Verbs and phrases she uses |
|---|---|
| Composition | *comprises, is divided into, is formed by, consists of* |
| Position | *extends from ... to, forms the boundary between, is located in, are positioned* |
| Function | *acts as, converts, collect and direct, is transmitted through, constrains* |
| Naming | *referred to as, defined as, commonly referred to as* |
| Scale | *typically, approximately, ranging from, between X and Y* |
| Framing | *From a biomechanical perspective, From a design perspective, From a system perspective* |

Words missing from the chapter: *crucial, comprehensive, robust, novel*. The evaluative adjectives
that fill her Results chapter (*consistent, realistic*) are absent. A background chapter in her
hands is descriptive.

## 8. Short templates

Structure paragraph:
> *[System] is divided into [n parts]: [a], [b], and [c] (Figure X). [a] comprises [parts], which
> [function] [cite]. [b] forms the boundary between [x] and [y]. As [adjectives], it acts as
> [role], [-ing consequence].*

Contrast paragraph:
> *From a [x] perspective, [object] can be divided into two [adj] distinct regions: [A] and [B].
> [A] is [property] and [B] is [property], while [number, unit] [cite]. The transition between
> them, referred to as [ABBR], represents [role]. For this reason, [distinction] is particularly
> relevant for [what the thesis does].*

Equation block:
> *[Quantity] is defined as: [eq] where [symbol] denotes [meaning, unit]. This [enables ...].*

## 9. Where her chapter and this thesis part ways

These rules win over the Aïda pattern.

1. **No bold for terms.** The standing rule is to define terms in plain text. `00_chapter_intro.tex`
   ends with "set in bold there", and `01_heart_anatomy.tex` (16 `\textbf`), `04_ccta.tex` (5) and
   `05_hemodynamics.tex` (3) still use it, plus `\emph` in `01` (12) and `03` (several). Ask before
   stripping.
2. **No mid-sentence glosses.** Her pattern is a trailing clause or a following sentence (§4). Our
   `03_cad.tex` has several appositives: *the lumen, the open channel the blood flows through*, and
   *the endothelium, the layer of cells lining the artery*. Move each to a sentence of its own.
3. **Chapter opening.** She has none. Ours has a roadmap and a "No cardiology background is
   assumed" line (`00_chapter_intro.tex`). Decision for the author whether to keep; the
   roadmap breaks her "never point forward" habit.
4. **Evidence per medical claim.** Her citations are mostly textbook-level and her numbers carry no
   population. Ours need one source per claim and the cohort behind any prevalence, mortality or
   accuracy figure (the `thesis-writing` skill). Keep her number style (range, unit, source) and
   add the *n* where a study produced it.
5. **Relevance sentences must name a consequence.** Hers do (*particularly relevant for
   vibroacoustic modelling of the ear canal*). Never close on "this highlights the importance of
   ...".
6. **Mechanism lives in the clinical chapter, studies in the literature review.** She has no
   separate lit-review overlap, we do. `05_hemodynamics.tex` closed with study evidence until the
   2026-10-04 move; do not let it drift back.
7. **Em dashes.** None, as in the other guides. Her en dashes are in compounds only.
8. **Equations.** We need few. A clinical chapter equation is justified only for a quantity the
   results use (wall shear stress, perhaps FFR as a pressure ratio). Follow §6 if so.

## 10. Audit of the current chapter against this guide

| File | Words | Matches | Departs |
|---|---|---|---|
| `00_chapter_intro.tex` | 235 | clear order of sections | roadmap and "bold terms" line (§9.1, §9.3) |
| `01_heart_anatomy.tex` | 1,012 | funnel from circulation to tree to dominance; 20 cites | 16 `\textbf` and 12 `\emph`; longest chapter piece, about 3 times her anatomy section |
| `02_variants.tex` | 313 | short, one section | 2 cites only, no subsections; check one source per claim |
| `03_cad.tex` | 601 | disease told in the order cause, mechanism, consequence | appositive glosses; narrative asides ("All of this happens quietly") that are outside her register |
| `04_ccta.tex` | 424 | acquisition, then resolution, narrowing to what CT can resolve | 5 `\textbf`; 6 cites for a technical section |
| `05_hemodynamics.tex` | 1,258 | ends on topology as the thesis's object (her §2 pattern) | 3 `\textbf`; longest, about the length of her whole chapter |

This table is read-only. No `.tex` was edited.
