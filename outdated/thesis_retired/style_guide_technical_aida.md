# Style guide: writing the Technical Background (after Jiménez Ordoñez, 2026, Chapter 3)

Source: `Former_students_work/AidaJimenez_MasterThesis_s243279.pdf`, Chapter 3 "Technical
Background" (pp. 15 to 20). Counts come from a `pdftotext` extraction of that chapter only, so
word counts include equation fragments and are approximate. Quoted phrases are verbatim. For her
register across the whole thesis see `style_guide_aida.md`; for the other chapters see
`style_guide_clinical_aida.md`, `style_guide_sota_aida.md` and `style_guide_methodology_aida.md`.

Where her habits clash with the `thesis-writing` skill or with standing instructions for this
thesis, the clash is flagged in §9 and the rule there wins.

---

## 1. The chapter at a glance

| Property | Aïda Ch. 3 |
|---|---|
| Position | After Ch. 2 Clinical Background; before Ch. 4 Data and Ch. 5 Methodology |
| Length | about 1,800 words, 6 pages |
| Sections | 3, two with one subsection each (3.2.1, 3.3.1); 3.1 has none |
| Section sizes (words) | 3.1 Coordinate systems 350 · 3.2 U-Net 290 · 3.2.1 nnU-Net 445 · 3.3 FEM 130 · 3.3.1 Harmonic analysis 600 |
| Sentences | about 58; mean 32 words, median 24 |
| Citations | 25 numeric brackets from 14 sources; no author names in the text except *Ronneberger et al.* once |
| Figures | 1 (U-Net schematic, taken from a source and cited in the caption) |
| Equations | 5 numbered (3.1 to 3.5), all in 3.3.1; 2 unnumbered in 3.1 |
| Chapter-opening paragraph | none; Section 3.1 starts directly |
| First person, *this thesis*, *this work* | none |
| Forward references | none |

The chapter explains the three bodies of theory her Methodology relies on, one section each, and
nothing more. It is a reference chapter: the Methodology points back to it (*As described in
Section 3.1, ...*) and never re-teaches.

## 2. Macro-architecture

### 2.1 One section per method the Methodology uses, in the order it uses them

| Section | Used by | Funnel | Ends on |
|---|---|---|---|
| 3.1 Image Standardisation | 5.1.1 pre-processing, 5.1.4 affine fix | voxel grid → anatomical frames (LPS, RAS) → affine matrix | the hazard: wrong convention, wrong direction |
| 3.2 U-Net, 3.2.1 nnU-Net | 5.1 segmentation | architecture → self-configuring framework → tool built on it | TotalSegmentator, the tool she uses |
| 3.3 FEM, 3.3.1 Harmonic analysis | 5.5 simulations | general method → software → governing equations → coupled matrix system | the exact system ANSYS solves |

Each section narrows from a general method to the specific variant or tool her work applies. The
headings say this in two layers: the general topic, then a colon or a subsection for the variant
(*3D Medical Image Segmentation: U-Net*, then *nnU-Net*).

### 2.2 Headings

Noun phrases in Title Case naming a method or a concept: *Finite Element Method*, *Harmonic
Vibroacoustic Analysis*, *nnU-Net*. The long one (*Image Standardisation: Coordinate Systems and
Affine Transformations in Medical Imaging*) puts the purpose before the colon and the content after.

### 2.3 What is left out

No hyperparameters, no settings, no ablations, no results. Exact numbers (patch size, epochs,
trainer name) appear only in the Methodology. The background says *patch size and batch size are
derived in a data-driven manner*; the Methodology says *128 × 128 × 128 voxels with a batch size
of 7*.

## 3. Paragraph architecture

### 3.1 Section openers: a definition sentence

Every section starts by saying what the thing is, in the present tense, with its domain:

> U-Net is a convolutional neural network architecture designed for biomedical image segmentation
> tasks, where both global context and accurate spatial localization are essential.

> The Finite Element Method (FEM) is a numerical technique widely used to solve partial
> differential equations arising in structural mechanics, acoustics, and multiphysics problems.

> Three-dimensional medical images are stored as voxel grids indexed in an image coordinate
> system, commonly referred to as IJK.

> Harmonic vibroacoustic analysis is used to compute the steady-state response of a linear system
> subjected to loads that vary sinusoidally with time [42].

### 3.2 Subsection opener: the problem the variant solves

When a subsection refines its parent, it opens with the parent's limitation and then names the
variant as the answer:

> While U-Net has become a widely used baseline for biomedical image segmentation, its application
> to new datasets traditionally requires a large number of design choices ... nnU-Net was
> introduced to address this challenge by providing a fully automatic, self-configuring
> segmentation framework ...

This is the only argument in the chapter. Everything else is description.

### 3.3 The architecture paragraph sequence

U-Net (3.2) and nnU-Net (3.2.1) each run four to six paragraphs in a fixed order:

1. **Origin**: what it is, who introduced it, when, with the citation (*Originally introduced by
   Ronneberger et al. in 2015 [34], ...*).
2. **Structure**: the parts, in data-flow order (encoder, then decoder), pointing to the figure.
3. **Key characteristic**: the one design idea that defines it (*A key characteristic of U-Net
   is the presence of skip connections ...*; *Central to nnU-Net is the concept of a dataset
   fingerprint ...*).
4. **Why it works**: the consequence of that idea (*These skip connections significantly mitigate
   the loss of spatial precision ..., making U-Net particularly effective for segmenting small or
   irregular structures*).
5. **Standing**: benchmark evidence or adoption (*Extensive benchmarking studies have shown that
   nnU-Net consistently achieves competitive or superior performance ...*).
6. **Tool**: the concrete implementation used later (*One prominent example is TotalSegmentator
   [39], an open-source framework that extends nnU-Net ...*).

### 3.4 Mechanism sentence pairs

Structure sentences are followed by a function sentence starting *This stage*, *This process*,
*By doing so*:

> The encoder, or contracting path, progressively reduces the spatial resolution of the input image
> while increasing the number of feature channels through repeated convolution and pooling
> operations. This stage enables the extraction of high-level features and captures contextual
> information over larger regions of the image [34].

### 3.5 Citation as paragraph closer

About half the paragraphs end with a bracket citing the source the whole paragraph paraphrases
(*[34]* closes four U-Net paragraphs, *[37]* closes five nnU-Net paragraphs). One source carries a
whole section. Fine for a textbook description of a single method; see §9.3.

### 3.6 Planting the hazard the Methodology later resolves

3.1 ends on what goes wrong without the theory:

> Correct interpretation of voxel directions is thus dependent on knowledge of whether the affine
> transformation maps into a RAS or LPS coordinate system. Otherwise, voxel movements may be
> associated with incorrect anatomical directions [33].

Twelve pages later, 5.1.4 cashes it: *As described in Section 3.1, this difference corresponds to
a reflection across the left–right and anterior–posterior axes, meaning that applying the original
pipeline directly ... would have produced anatomically mirrored volumes.* The background never
mentions the Methodology; it states a general consequence, and the Methodology makes the link.
This is the most useful pattern in the chapter.

## 4. How terms are introduced

| Pattern | Verbatim |
|---|---|
| Full term, abbreviation in brackets | *The Finite Element Method (FEM)*, *LPS (Left, Posterior, Superior)* |
| *commonly referred to as* | *an image coordinate system, commonly referred to as IJK*; *commonly referred to as a "U-shaped" architecture* |
| Synonym with *or* | *The encoder, or contracting path, ...*; *The decoder, or expanding path, ...* |
| *the concept of* | *Central to nnU-Net is the concept of a dataset fingerprint, which summarizes ...* |
| Symbol in a *Let* sentence | *Let P(x, t) denote the acoustic pressure field as a function of space and time.* |

No bold, no italics for new terms. Each term is defined once, at first use, and never re-glossed.

## 5. Equations

### 5.1 The derivation chain (3.3.1)

Five numbered equations build one system, each a step from the last:

1. Harmonic load in complex form (3.1), with assumptions stated first: *In harmonic analysis, all
   loads and boundary conditions are assumed to vary harmonically with time.*
2. Governing physics in words, with sources: *derived from the linearized conservation of mass and
   momentum ... [43] ... Under the assumptions of small acoustic perturbations, negligible mean
   flow, and time-harmonic excitation, these equations reduce to the Helmholtz equation ... [44].*
3. The field equation (3.2), introduced by *Let ... denote* and *Assuming ...*.
4. Discretisation in words (*Applying the standard Galerkin formulation [45] and assembling the
   element-level contributions yields a system of algebraic equations in matrix form.*), then the
   matrix system (3.3).
5. The second domain (3.4), then the coupled system (3.5), introduced by *Adding the presence of
   ...*.

The assumptions are the content. Every reduction names what was assumed to get there.

### 5.2 Symbol definitions

Two forms, both used:

- *where* sentence after short equations: *where p is the complex acoustic pressure amplitude, k
  is the acoustic wavenumber, ω is the angular frequency, and c is the speed of sound in the
  medium.*
- *where:* plus a bullet list after matrix equations, one bullet per symbol with its physical
  meaning: *[Ma] is the acoustic mass matrix, accounting for fluid inertia and compressibility.*

### 5.3 Unnumbered equations in prose (3.1)

The LPS-to-RAS reflection and the voxel-to-world mapping are unnumbered, introduced by *can be
expressed as* and *such that*, and followed by a sentence reading the matrix block by block: *The
upper-left 3 × 3 block of M encodes the orientation and spacing of the image axes, while the final
column defines the spatial position of the image origin.*

## 6. Tools and software

A tool gets one paragraph at the end of its section, after the theory it implements:

> ANSYS Mechanical [41] is a commercial FEM-based simulation environment that provides extensive
> capabilities for structural dynamics, acoustics, and fluid–structure interaction analyses. It is
> widely used for the numerical simulation of coupled structural and acoustic problems involving
> complex geometries and realistic material behaviour.

> Building upon nnU-Net, several application-oriented tools have been developed for fully automated
> segmentation. One prominent example is TotalSegmentator [39], ...

Form: name, citation, *is a [kind] that provides [capability]*, then one sentence on what it is
suited for. How she used it belongs to the Methodology.

## 7. Tense, voice and vocabulary

**Tense.** Present throughout (*is*, *follows*, *encodes*, *reduce to*). Past only for history
(*was introduced*, *Originally introduced ... in 2015*). No past passive for actions, because
nothing has been done yet.

**Voice.** Mostly active with the method as subject (*The encoder ... reduces*, *nnU-Net
demonstrates*, *The framework automatically adapts*). Passive for operations inside a framework
(*Images are cropped ..., resampled ..., and normalized*).

**Connectives.** *while* 3, *whereas* 1, *Rather than* 1, *thus* 1, *therefore* 1, *By doing so*,
*As a result*, *Instead of*, *Based on*.

**Hedges and claims.** *can* 5, *typically*, *commonly* 2, *widely* 5. Claims of standing are
strong and unquantified: *strong segmentation performance*, *state-of-the-art performance*,
*de facto standard*, *significantly mitigate*. See §9.3.

## 8. Short templates

**Section opener:**
> *[Method] is a [kind of method] designed for [task], where [what the task demands] \cite{}.*

**Origin paragraph:**
> *Originally introduced by [authors] in [year] \cite{}, [method] [what it changed]. [One sentence
> on what it is used for since].*

**Structure then function:**
> *The [part], or [synonym], [what it does to the data]. This stage [what that enables] \cite{}.*

**Key characteristic:**
> *A key characteristic of [method] is [design idea]. [How it works]. [Consequence for the kind of
> structure this thesis segments or measures].*

**Subsection as the answer to its parent:**
> *While [parent] has become [status], [limitation]. [Variant] was introduced to address this by
> [mechanism] \cite{}.*

**Tool paragraph:**
> *[Tool] \cite{} is a [kind] that provides [capability]. It [what it is suited for].*

**Hazard closer:**
> *Correct [operation] therefore depends on [condition]. Otherwise, [concrete failure].*

**Equation block:**
> *Under the assumptions of [a], [b] and [c], [governing law] reduces to [name] \cite{}: [eq]
> where [symbols with meaning and unit].*

## 9. Where her chapter and this thesis part ways

These rules win over the Aïda pattern.

| Her habit | Rule for this thesis | Source of the rule |
|---|---|---|
| *Because each anatomical convention assigns ...* opens a paragraph | Never open a paragraph with *Because*. Fact first, then *so*. | memory: `feedback_no_because_opening.md` |
| Appositive glosses (*TotalSegmentator [39], an open-source framework that extends nnU-Net ...*; *ANSYS Mechanical [41] is a commercial ... environment that provides ...* is fine) | No inserted clauses after a name. Give the gloss its own sentence. | `style_guide_sota_aida.md` §10, memory: `feedback_short_replies.md` |
| One source per section (*[34]* for all of U-Net, *[37]* for all of nnU-Net) | Fine for describing what a method is. Any claim about performance or standing needs its own source, and a number with its population. | `thesis-writing` skill |
| *state-of-the-art performance*, *de facto standard*, *significantly mitigate*, *widely* 5 times | Replace with what the cited study measured, on what, with *n*, or drop the claim. | `thesis-writing` skill |
| nnU-Net described as the paper describes it (*Training follows a fixed protocol based on cross-validation*), not as used | Describe the general method from the source, but check every behaviour claim against the source. Settings from our configs go to the Methodology, not here. | `CLAUDE.md` "How to explain things" |
| Symbols redefined twice (u, p, Ma, Ca, Ka in both 3.3 and 3.5) | Define each symbol once; later equations reuse it. | proofreading |
| Typo in Eq. 3.2 (*= 0, , k = ω/c*) | Build and read the PDF of every equation. | proofreading |
| Figure 3.1 taken from a source | Allowed with credit in the caption and in `figures/external/CREDITS.md`. Prefer own figures drawn with the `academic-figures` skill when the point is our variant (CAS-Net, not the 2D U-Net). | repo convention |
| Bold terms | None. She has none here either; keep it so. | memory: `feedback_no_textbf_thesis.md` |
| Em dashes | Never. En dashes only in compounds (*encoder–decoder*, *fluid–structure*). | all guides |

What to keep without change: one section per method the Methodology uses, in its order (§2.1);
general method → variant → tool (§2.1); the definition opener (§3.1); the subsection-as-answer
opener (§3.2); the architecture sequence (§3.3); the hazard closer (§3.6); the derivation chain
with assumptions named (§5.1); no settings, no results (§2.3); no chapter roadmap and no forward
references.

## 10. Mapping onto this thesis

### 10.1 Background or Methodology

Background says what a method is and why it works: general, present tense, cited to its source,
no numbers chosen in this thesis, no cohort. Methodology says what was done with it: which variant,
which settings, on which data, why, and how it was checked, in the past passive.

- Per sentence: *would it be true if this thesis had never been written?* Yes means background.
- Per section: a Methodology section must point back to it (*As described in Section ...*). If
  none does, cut it.

### 10.2 Chapter structure

The skeleton is in `thesis/technical_background/` (headings, labels, one `%` line per planned
paragraph, no prose).

| File | Section (subsection) | Pointed back to by (`methodology.tex`) | Ends on |
|---|---|---|---|
| `01_image_geometry.tex` | CT Image Geometry and Resampling | Lumen Segmentation | hazard: thin vessels thinned or broken by resampling |
| `02_segmentation_networks.tex` | 3D Segmentation: U-Net (CAS-Net) | Lumen Segmentation | tool: TotalSegmentator |
| `03_centerline_extraction.tex` | Centerline Extraction and the Coronary Tree (Graph Neural Networks) | Centerline Extraction, Artery Labeling | hazard: a break in the lumen is a break in the tree; tool: Hampe et al. 2024 |
| `04_curvature.tex` | Curvature of a Centerline | Geometric Features, Reliability | smoothing, stated as fact |
| `05_risk_models.tex` | Risk Prediction Models (Functional Principal Component Analysis) | Statistical Analysis | the 1D CNN as the alternative with too many weights |

Five sections and three subsections against her three and two; about 35 planned paragraphs
against her 24, target about 2,500 words. Every subsection goes one step deeper into its section,
as hers do. Convolution and training are assumed, as in hers; the soft Dice loss goes to the
Methodology. Two hazard closers only (`01`, `03`).

Left out: Medis (a commercial product that delivered reference labels; Data chapter and
Methodology), transformers (none in the Methodology), CFD/FEM (no flow simulation), WSS and
bifurcation scaling laws (Clinical Background), segmentation and prediction metrics
(Methodology), Tello Ayala et al. 2026 (a study, so literature review).

Equations belong here only when they form a chain the Methodology then uses (§5.1): curvature in
`04`, logistic regression and the ridge penalty in `05`, the message-passing update in `03`.

### 10.3 Material already written that belongs here

`thesis/pipeline/02_model_architecture.tex` (about 1,270 words) explains U-Net and the CAS-Net
attention modules. Under her split, that explanation moves to `02_segmentation_networks.tex`; the
Methodology keeps only CAS-Net's configuration and settings. Strip its `\textbf`, the inserted
gloss after *U-Net*, and the code references (*function names refer to `models/cas_net.py`*) when
moving it.

## 11. Checklist before calling the chapter done

- [ ] Every section is pointed back to by a Methodology stage; no section is there for completeness.
- [ ] Sections in the order the Methodology uses them; each narrows from general method to the variant or tool used.
- [ ] Each section opens with a definition sentence; each subsection opens with the limitation it addresses.
- [ ] Architecture sections follow origin, structure, key characteristic, why it works, standing, tool.
- [ ] Where the Methodology depends on getting something right, the section closes on what goes wrong otherwise.
- [ ] No settings, hyperparameters, results or code names; those live in the Methodology.
- [ ] Equations only as a chain the later chapters use; assumptions named at each reduction; each symbol defined once.
- [ ] Performance or standing claims carry a source and a number with its population, or are cut.
- [ ] Present tense; past only for history; no first person; no forward references; no chapter roadmap.
- [ ] No paragraph opens with *Because*; no appositive glosses; no em dashes; no `\textbf`.
- [ ] External figures credited in the caption and in `figures/external/CREDITS.md`.
- [ ] `hunspell -l -t -d en_US -p wordlist.txt` returns only names; build with zero undefined citations.
