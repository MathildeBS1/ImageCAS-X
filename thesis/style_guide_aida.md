# Phrasing guide: writing like a DTU MSc thesis (after Jiménez Ordoñez, 2026)

Source: `Former_students_work/AidaJimenez_MasterThesis_s243279.pdf` (DTU Compute,
MSc Mathematical Modelling and Computation, July 2026, ~25 000 words of body prose).
Everything below is read off that thesis: the counts come from a text extraction of the
body (Introduction through Conclusion), the examples are quoted verbatim.

This is a guide to *register*, not to argument. Where her habits clash with the evidence
rules in the `thesis-writing` skill, the skill wins; those clashes are flagged in §8.

---

## 1. The voice in one paragraph

Formal, impersonal, calm. Long sentences (mean 27 words, median 24) built from one main
clause plus one or two participial tails. Almost no first person outside the abstract
("we propose") and preface. "This work" / "this thesis" stands in for "I" (≈30 uses).
Methods are in the past passive ("was applied", "were computed"); background, results
descriptions and discussion are in the present ("shows", "exhibits", "indicates").
Claims are softened with *may*, *suggests*, *slightly*, *approximately*, never with
"I think". Every paragraph ends by saying why the thing mattered.

## 2. Sentence architecture

### 2.1 The default sentence: main clause + participial tail

The single most frequent shape. A finite clause states the fact; a trailing *-ing* phrase
states the consequence or purpose.

> All resampling operations were performed using nearest-neighbour interpolation to
> preserve label integrity, as CT volumes are continuous-valued whereas segmentation
> masks consist of discrete labels.

> The initial cohort comprised 387 CT scans, of which eight were excluded due to
> insufficient image quality or incomplete anatomical coverage, **yielding** a final
> dataset of 379 patients.

> Padding, cropping, resampling, and origin-resetting steps were consistently applied to
> both images and masks, **ensuring** voxel-wise correspondence in the final standardized
> space.

The tail verbs, by frequency: *resulting in* (20), *ensuring* (13), *enabling* (10),
*leading to* (9), *indicating* (9), *allowing* (7), *making* , *yielding*, *reflecting*,
*providing*, *thereby* + -ing (3).

Rule of thumb: a methods sentence says **what was done**, then **why**, in one breath.
A results sentence says **what is seen**, then **what it indicates**.

### 2.2 The contrast pair inside one sentence

`X does A, while/whereas Y does B.` (*while* 39, *whereas* 12). Used constantly for
comparing two structures, datasets, configurations.

> The outer segment is primarily cartilaginous and covered by a dermal layer of
> approximately 1 mm thickness, **while** the medial segment is osseous and lined by a
> much thinner epithelial layer of approximately 0.1 mm.

> Dice measures the degree of overlap between segmentations (ranging from 0 to 1),
> **while** IoU provides a slightly more conservative estimate of agreement.

### 2.3 The "not only ... but also" and "both ... and" couplets

> This feedback **not only** degrades sound quality and limits achievable gain **but can
> also** discourage consistent device use, making its effective mitigation a critical
> challenge in hearing aid design.

### 2.4 Lists of three

Nouns and adjectives come in threes far more often than in twos or fours:

> labor-intensive, operator-dependent, and difficult to scale
> communication, environmental awareness, and social interaction
> energy transmission, damping, and device–ear coupling

Oxford comma always.

### 2.5 Front-loaded orientation phrases

Sentences often open with a short prepositional frame before the subject:

*From a biomechanical perspective, ... / From a clinical perspective, ... / From a
system perspective, ... / In the LPS system, ... / For the segmentation tasks, ... /
Regarding placement, ... / In terms of cohort characteristics, ... / Within the
mass–spring framework, ...*

These do the job a sub-heading would otherwise do and let one paragraph switch topic
without a new section.

### 2.6 Short sentences are rare and always load-bearing

Only 12 % of sentences are under 15 words. They are used for (a) one-line section
openers, (b) definitions, (c) the verdict at the end of an argument:

> This difference in boundary conditions leads to distinct behaviour.
> Evaluating a larger cohort of subjects is also necessary.
> Higher errors and variability are observed for CBJ3 compared to the other landmarks.

### 2.7 Gloss only what the argument needs, in one short clause

Her sentences keep subject, verb and object together and put extra information in the
tail (§2.1) or in a sentence of its own. She glosses only the one key term of the
introduction (*vibroacoustic feedback ..., which occurs when ...*), in a single trailing
clause. Do not interrupt the main clause with an appositive or a parenthetical gloss, and
leave other definitions to the background chapter.

> Avoid: Instead, it collects where the wall shear stress (WSS), the drag of the flowing
> blood on the vessel wall, is low or oscillates over the cardiac cycle.
>
> Prefer: Instead, it collects where the wall shear stress (WSS) is low or oscillates
> over the cardiac cycle. WSS is the drag of the flowing blood on the vessel wall.

An abbreviation in brackets directly after its term is the only interruption allowed.
A definition gets its own short sentence (§2.6), placed after the sentence that first
needs the term.

## 3. Paragraph architecture

Paragraphs are 3 to 6 sentences and almost always follow this order:

1. **Topic sentence** stating the claim or the step.
2. **Elaboration** with specifics: numbers, citation, method name.
3. **Consequence** with a tail verb or *therefore / as a result*.
4. *(often)* **Significance sentence** opening with *This*, *These*, *Overall*,
   *Collectively*: "This highlights the importance of ..."

Worked example (Introduction, §1.1.1):

> [1] Large-scale geometric studies have further revealed substantial inter-individual
> variability in ear canal anatomy. [2] Voss et al. (2020) analysed silicone moulds from
> 169 subjects, demonstrating that cross-sectional areas are generally larger than
> previously assumed and tend to increase with age. [2] Advancing this further,
> high-resolution CT-based investigations by Balouch et al. (2023) quantified variability
> at specific anatomical landmarks, reporting that dimensions can vary by up to a factor
> of three between individuals. [2] Most recently, Voss et al. (2025) provided a
> comprehensive lifespan analysis using CT imaging. [3] Their findings indicate that ...

Then the *next* paragraph is the synthesis:

> **Collectively**, these findings highlight that ear canal geometry is highly
> individualized ... **Therefore**, realistic anatomical representation is essential ...

### 3.1 Linking paragraphs

The first words of a paragraph almost always point backwards. Openers seen most often:

| Function | Openers (counts in body) |
|---|---|
| Add | *In addition* (16), *Additionally* (3), *Furthermore* (6), *Moreover* (3) |
| Narrow | *In particular* (14), *Specifically* (4) |
| Contrast | *However,* (12), *In contrast* (12), *Despite these advances/limitations* (9) |
| Consequence | *As a result* (7), *therefore* (14, mostly mid-sentence), *Consequently* |
| Sequence | *First, ... Second, ...*, *Subsequently*, *Finally,* (12) |
| Wrap-up | *Overall,* (13), *Collectively,*, *Together,* |
| Anaphora | *This* (76 sentence-initial), *These* (32) |
| Chronology (lit. review) | *Early foundational work by ...*, *Subsequent research has further ...*, *More ... have since emerged*, *Most recently, ...* |

"This"/"These" + noun is her glue: *This feedback ..., This step ensured ..., These
findings highlight ..., These sign inversions were implicitly assumed ...*. She almost
never leaves *This* bare without a noun after it.

## 4. Filler, hedge and intensifier vocabulary

These are the words that make the text sound like her. Use them at roughly her rate,
not more.

**Hedges (softening a claim)**
*may* (21), *can* (18), *slightly* (12), *approximately* (17), *relatively* (6),
*likely*, *suggests/suggesting*, *tend to*, *generally*, *marginally*, *somewhat*,
*broadly consistent*, *to some extent*.

> This behaviour is **likely** associated with differences in contour definition ...
> ... which **may** contribute to the **slightly** lower mean values ...

**Intensifiers / evaluative adjectives**
*consistent* (41), *realistic* (19), *critical* (15), *robust* (11), *essential* (9),
*significant(ly)*, *substantial*, *comprehensive*, *high-fidelity*, *key*,
*fundamental*, *strongly*, *particularly* (20).

**Signposting verbs for results**
*highlight* (23), *demonstrate* (17), *indicate* (9+), *suggest*, *reflect*, *confirm*,
*underline*, *show*.
The ladder of strength she uses: *suggests* < *indicates* < *shows* < *demonstrates*.
She reserves *demonstrates* for things with numbers behind them.

**Stock phrases (each appears several times)**
- *plays a key/crucial role in*
- *highlights the importance of*
- *is particularly relevant for*
- *in the context of*
- *a key characteristic of X is*
- *from a ... perspective*
- *as shown in Figure X / as illustrated in Figure X / (Figure X)*
- *as described in Section X*
- *Despite these limitations, ...*
- *Several limitations should be acknowledged.*
- *Future work should focus on ...*
- *The main findings and their implications are discussed in the following sections.*

**Words she does not use:** *delve, leverage, utilize* (once, appendix), *novel* (once,
about nnU-Net), *groundbreaking, cutting-edge, paradigm*. No rhetorical questions. No
exclamation marks. No "we" in body chapters.

## 5. Depth of explanation, chapter by chapter

The depth is uneven on purpose. She explains what the reader needs to follow *her*
results and stops there.

### Introduction (8 paragraphs; her SotA is 3 subsections inside it)
About 2.5 pages, 8 paragraphs, one statistic, about 10 citations, no individual studies
and no per-study numbers (those are one sentence each in the State of the Art).
**Deviation for this thesis:** the literature is its own chapter, "Literature Review"
(`literature_review/literature_review.tex`, `\label{ch:literature}`), not a 1.1: three
sections and a closing table, written to `style_guide_sota_aida.md`. The Introduction
keeps her funnel and still names no individual studies; it ends on the aim.
Funnel: societal problem (1.5 billion people) → device → specific failure (vibroacoustic
feedback) → why simulation → why current geometry capture fails (*two key
limitations. First ... Second ...*) → why AI → remaining challenges → *This work aims to
...* with a two-stage outline. Every paragraph is one step down the funnel, and its last
sentence sets up the next paragraph's first.

State of the Art (in our thesis: one *section* of the SotA chapter per strand, same
rules): one subsection per strand, each **chronological** (Early ... →
Subsequent ... → More recently ... → Most recently ...), each study gets **one sentence
of what they did + one clause of what it showed**, each subsection closes with a **gap
sentence**: *Despite these advances, the majority of studies remain focused on ...*
followed by *Bridging this gap is essential for ...*. Ends with a summary table.

### Clinical and Technical Background (textbook depth)
Definitions first, then mechanism, then relevance to the thesis:

> The transition between these regions, referred to as the CBJ, represents a critical
> anatomical and mechanical boundary. Differences in stiffness, damping, and tissue
> composition across the CBJ ... strongly influence the propagation ... **For this
> reason**, the explicit distinction between soft tissue and bone is particularly
> relevant for vibroacoustic modelling of the ear canal.

Equations are introduced in running text (*The sound pressure level (SPL) is defined
as:*), followed by *where ...* defining each symbol, followed by one sentence on what the
quantity is used for. Architecture sections (U-Net, nnU-Net) are ~4 paragraphs each:
origin + citation, structure, key characteristic, why it works. No ablations, no
hyperparameter tables in background.

### Data (short, factual)
One paragraph per dataset: source → acquisition → size and exclusions with exact
counts → a sentence on strengths, a sentence on weaknesses (*however*), and **what it was
therefore used for**. Exclusions always carry a reason.

### Methodology (deepest chapter; reproducibility depth)
Opens with an enumerated overview: *consists of five main stages: (1) ...; (2) ...*.
Each subsection: **what** (tool, version, setting) → **why** (one clause) → **how
checked**. Exact numbers everywhere (patch 128×128×128, batch 7, 100 epochs, 0.74 mm).
Software is named with citation (*using 3D Slicer [53]*). Choices that a reader might
question get a justification sentence:

> Training used the nnUNetTrainerNoMirroring trainer, which disables mirroring-based
> augmentation. This is particularly important for anatomically asymmetric structures
> such as the temporal bone, where left–right reflections would introduce
> non-physiological features.

Assumptions are stated and immediately defended:

> Although this value is not physically realistic, its magnitude does not affect the
> results, as the MAGBF is defined as a pressure ratio and the model is linear.

Problems found during the work are written into methods, not hidden:
*However, a fundamental affine convention discrepancy was identified between ...*
followed by the cause and the fix.

### Results (describe, then interpret lightly)
Pattern per figure/table: *Figure X compares/shows ...* → describe the global trend →
*However, clear differences are observed in ...* → numbers → one interpretation sentence
(*This shift is consistent with ...*) → *Overall, ...* summary. Heavy interpretation is
deferred to Discussion, but she does give the mechanism (mass–spring analogy) inside
Results when the figure is unreadable without it.

### Discussion (one subsection per Results block)
Order inside each subsection: restate main finding → explain discrepancies (*This
behaviour is likely associated with ...*) → compare to literature → *Several limitations
should be acknowledged.* → *Despite these limitations, ...* → strength/contribution.
Followed by a "Relevance and Potential Applications" section written from *a clinical
perspective* and *a design perspective*.

### Conclusion (one page)
One paragraph per contribution, each opening with the component as subject (*The
developed segmentation pipeline demonstrates ...*, *The population-level analysis
provides ...*), then *A key finding of this work is ...*, then *Future work should focus
on ...*, then *In conclusion, this work establishes ...*.

## 6. Tense and voice

| Where | Tense / voice | Example |
|---|---|---|
| Background facts | present, active | *U-Net follows a symmetric encoder–decoder structure* |
| Prior studies | past, active | *Voss et al. (2020) analysed silicone moulds from 169 subjects* |
| Their findings | present or past | *Their findings indicate that ...* |
| Own methods | past, passive | *Outliers were identified using the IQR criterion* |
| Own results (describing figures) | present, passive or intransitive | *Higher errors are observed for CBJ3*; *the curve exhibits a minimum* |
| Discussion | present + modal | *These differences may arise from ...* |
| Future work | *should* | *Future work should focus on ...* |

Passive is the norm in methods. In results she prefers
*is observed*, *exhibits*, *shows*, *remains*.

## 7. Small mechanics

- Abbreviations defined at first use in each chapter, then always used: *cartilaginous–
  bony junction (CBJ)*.
- Figure references either inline (*as shown in Figure 5.9a*) or parenthetical at the end
  of a clause (*(Figure 1.1)*). Every figure is introduced before it appears.
- Citations as numeric brackets after the clause they support, author + year named in
  text only in the State of the Art.
- Numbers always with units and approximate markers (*approximately 1.8 mm medial to*,
  *∼51–54 mm²*). Ranges reported as *between X and Y* or *ranging from X to Y*.
- British spellings mostly (*modelling, behaviour, centre, analysed*) with some
  American slips (*characterization, optimized*). Pick one and stay consistent.

## 8. What not to copy

Her register is a good target; a few habits would fail the `thesis-writing` skill:

1. **Signpost openers with no content.** *This section evaluates the influence of tissue
   characterization ...*, *This section presents the performance of ...*. Cut them; start
   with the finding.
2. **Unsourced significance sentences.** *This highlights the importance of accurate
   anatomical modelling* closes many paragraphs without new evidence. Keep the shape,
   but make the closing sentence carry a specific consequence for a later chapter.
3. **Adjective inflation.** *consistent* 41 times, *realistic* 19, *critical* 15. Each
   repetition weakens the next. Allow each a few times per chapter.
4. **Unquantified hedges in results.** *slightly higher*, *marginally lower* without the
   number next to them. She sometimes gives the number, sometimes not; always give it.
5. **Population missing from claims.** *Dice values above 0.93* is fine; *robust
   performance* needs "on the 20 test volumes". Her Discussion also generalises from
   four simulated subjects before adding the caveat; put the n first.
6. **Doubled words and extraction slips** (*induced induced*, *landmark landmarks*): proof
   read.
7. Inserted clauses and mid-sentence glosses: see §2.7. Move them to a following
   sentence or a tail.
8. Em dashes: she uses en dashes only in compounds (*device–tissue*). Keep it that way;
   never as a parenthetical dash.

## 9. Quick templates

Methods step:
> *[Step] was performed using [tool] [cite], [setting]. [One-clause reason], ensuring
> [consequence].*

Results paragraph:
> *Figure X compares [A] and [B]. Both exhibit [shared trend]. However, [difference] is
> observed [where], with [A] showing [value] compared to [value] for [B]. This [shift /
> difference] is consistent with [mechanism]. Overall, [one-line takeaway].*

Literature strand:
> *Early work by [Author] ([year]) [did X], showing [Y]. Subsequent studies [extended
> this to Z] [cites]. More recently, [Author] ([year]) [did W]. Despite these advances,
> [gap]. Addressing this gap is essential for [this thesis's aim].*

Limitation block:
> *Several limitations should be acknowledged. [Limitation 1]. In addition, [limitation
> 2], which may [effect]. Despite these limitations, [what still holds and why].*
