# Style guide: writing the Methodology (after Jiménez Ordoñez, 2026, Chapter 5)

Source: `Former_students_work/AidaJimenez_MasterThesis_s243279.pdf`, Chapter 5 "Methodology"
(pp. 25 to 47). Counts come from a text extraction of that chapter only; captions and tables are
excluded from word and sentence counts unless stated. Quoted phrases are verbatim. For her register
across the whole thesis see `style_guide_aida.md` (its §5 "Methodology" paragraph is the short
version of this file); for the other chapters see `style_guide_sota_aida.md` and
`style_guide_clinical_aida.md`.

Where her habits clash with the `thesis-writing` skill or with standing instructions for this
thesis, the clash is flagged in §11 and the rule there wins.

---

## 1. The chapter at a glance

| Property | Aïda Ch. 5 |
|---|---|
| Position | After Ch. 3 Technical Background and Ch. 4 Data; before Ch. 6 Results |
| Length | about 5,700 words of prose, 23 pages; the longest chapter in the thesis |
| Sections | 6 (5.1 to 5.6), one per pipeline stage, in execution order |
| Subsections | 14, plus one sub-subsection (5.5.2.1); 5.4 has none |
| Section sizes (words) | 5.1 Segmentation 1,625 · 5.2 Geometric analysis 640 · 5.3 Selection 410 · 5.4 3D models 300 · 5.5 Simulations 2,385 · 5.6 Skin 450 |
| Sentences | about 215; mean 27 words, median 23; about 30 under 15 words |
| Citations | 20 numeric brackets, nearly all for software, metrics or parameter sources |
| Figures | 17 (about 0.75 per page), the first an overview of the whole pipeline |
| Tables | 4, all parameter or feature tables |
| Equations | 4 numbered (5.1 to 5.4), about 12 unnumbered (metrics, IQR rule, selection bounds, affine diagonals, wavelength) |
| Cross-references | 17 to sections, 3 to appendices, 18 to figures, 15 to tables |
| First person | none; "this work" 5, "this thesis" 3 |

The chapter is written so that someone with the same software could redo every step. Theory lives in
Chapter 3 and is pointed back to; implementation detail that would break the flow is pushed to the
appendices. The Methodology itself holds the decisions, the settings and the reasons.

## 2. Macro-architecture: the pipeline is the table of contents

### 2.1 Chapter opening: one numbered sentence and one figure

The chapter has no roadmap paragraph. It has a single sentence that enumerates the stages and
points to the overview figure, and the sections then follow that enumeration one to one.

> The methodology followed in this work is summarized in Figure 5.1 and consists of five main
> stages: (1) AI-based segmentation of the external auditory canal and surrounding tissues,
> including data pre-processing, ground-truth generation, and model training and inference;
> (2) population-level geometric analysis of the extracted anatomies; (3) selection of
> representative subjects based on this population analysis; (4) generation of simulation-ready 3D
> anatomical models; and (5) vibroacoustic FE simulations of the selected subjects.

Caption of Figure 5.1: *Overview of the methodology pipeline followed in this work, from AI-based
segmentation and population analysis to subject selection, 3D model generation, and vibroacoustic
FE simulations.*

Note the sentence lists five stages but the chapter has six sections: 5.6 (skin) is an extension
added after the main pipeline. A reader notices; keep the enumeration and the sections in step.

### 2.2 Section order follows data flow

| Section | Input | Output handed to the next section |
|---|---|---|
| 5.1 AI-Based Segmentation | raw head CT | bone and tissue masks, landmarks |
| 5.2 Population-level Geometric Analysis | masks, landmarks | filtered cohort, features per ear |
| 5.3 Representative Patients Selection | features | four subjects |
| 5.4 3D Models Generation | masks of four subjects | `.step` volumetric geometries |
| 5.5 Harmonic Vibroacoustic Simulations | geometries | pressures, MAGBF |
| 5.6 Soft-Tissue Differentiation | geometries | extended models with skin |

Every section opens by naming the output of the previous one (§4.1). The reader never has to ask
where an input came from.

### 2.3 Headings

Noun phrases in Title Case naming the stage or the object: *Pre-processing*, *Ground-Truth
Generation*, *Bone Segmentation Model*, *Inference on Unseen Data*, *Data-quality Filtering*,
*Features Extracted*, *Outlier Removal*, *Selection Criteria*, *Material Properties*, *FE Meshing*,
*Boundary Conditions and Excitations*, *Analysis Settings*. Never a claim, never a question.

### 2.4 Section intro paragraph before the subsections

Each multi-subsection section has a short intro (1 to 4 paragraphs) that states the purpose and
lists the sub-steps in order, often with *First ... Subsequently ... Finally*:

> ANSYS Mechanical software [41] was used for the preparation and execution of the FE simulations.
> The simulation workflow consisted of several steps. First, the generated volumetric geometries
> were imported into the software and the different simulation setups were defined. Subsequently,
> the boundary conditions (BCs) and the material properties of the different tissues were assigned.
> Finally, the simulation settings were specified, and the simulations were executed on the
> computational grid.

> The overall AI-based segmentation workflow consists of an initial data preparation stage,
> followed by ground-truth generation and training of the bone segmentation model, and a final
> inference step in which both the bone model and the tissue model are applied and integrated.

The subsections then follow that order. The intro is a map of the section, not of the chapter.

## 3. Paragraph architecture: what, why, how checked

The unit is a paragraph of 2 to 5 sentences that does one operation. Its moves:

1. **What was done**, past passive, with the tool and its citation.
2. **Setting**, exact numbers and units.
3. **Why**, as a purpose clause (*to ...*), a reason clause (*as ...*, *since ...*) or a
   participial tail (*ensuring ...*).
4. **How it was checked** or what it guarantees downstream, when the step can fail.

All four in one paragraph:

> All resampling operations were performed using nearest-neighbour interpolation [52] to preserve
> label integrity, as CT volumes are continuous-valued whereas segmentation masks consist of
> discrete labels. Padding, cropping, resampling, and origin-resetting steps were consistently
> applied to both images and masks, ensuring voxel-wise correspondence in the final standardized
> space.

Check written as its own paragraph (5.1.3):

> Training and validation curves reached a stable plateau after approximately 50 epochs, indicating
> convergence of the optimization process. No substantial changes in validation performance were
> observed thereafter ... Representative learning curves from one cross-validation fold are
> provided in Appendix C, while the remaining folds exhibited very similar behaviour.

The check points to evidence (an appendix figure) rather than asserting convergence.

## 4. Opening sentences

### 4.1 Section and subsection openers chain to the previous step

The first words of most subsections place the step in time relative to the one before. This is the
glue of the chapter.

| Opener (verbatim) | Where |
|---|---|
| *This work begins with the development and application of ..., which provides the anatomical input for all subsequent analysis and simulation stages.* | 5.1 |
| *After training and evaluation, the bone segmentation model was used to ...* | 5.1.4 |
| *Geometric features ... were extracted from the segmentation outputs and anatomical landmarks obtained from the two AI-based models previously described.* | 5.2 |
| *Following segmentation inference, a data-quality filtering procedure was applied to ...* | 5.2.1 |
| *From the population-level analysis, four representative patients were selected to ...* | 5.3 |
| *Prior to selection, an outlier removal step was applied to ensure ...* | 5.3.1 |
| *Following outlier removal, the selection was restricted to ...* | 5.3.2 |
| *Once the four patients to be used in the subsequent simulations had been selected, ...* | 5.4 |
| *As an initial refinement, ...* | 5.6.1 |

Connectives used: *After*, *Following* (twice), *Prior to*, *Once ... had been*, *From*. No two
adjacent subsections share one.

### 4.2 Purpose openers

When a step is not a direct continuation, it opens with its goal in an infinitive:

> To assess the impact of including the bony structures on the simulation outcomes, an initial set
> of simulations was performed ...

> To enhance the anatomical realism of the model and improve the representation of the ear canal,
> several soft-tissue refinement strategies were explored.

> To simulate the effect of the hearing aid, a simplified model of a custom IIC device was developed.

### 4.3 Pointer openers for parameter subsections

Subsections that are mostly a table open by pointing to it, then explain the rows:

> The extracted geometric features are summarised in Table 5.1 and can be seen in Figure 5.6.

> The material properties assigned to the different tissues, namely density, Young's modulus,
> Poisson's ratio, and loss factor, are summarized in Table 5.2.

> A schematic representation of all applied BCs is shown in Figure 5.14.

## 5. Justifying choices

The defining habit of the chapter. A setting a reader might question is followed, in the same or
the next sentence, by its reason. Six forms recur.

| Form | Verbatim example |
|---|---|
| **Purpose clause** | *... using nearest-neighbour interpolation [52] to preserve label integrity, as ...* |
| **Absence as reason** (*Since no ...*) | *Since no curated dataset exists for the bony structures of the external auditory canal, a semi-automatic workflow was developed ...* |
| **Domain consequence** (*This is particularly important for ...*) | *Training used the nnUNetTrainerNoMirroring trainer, which disables mirroring-based augmentation. This is particularly important for anatomically asymmetric structures such as the temporal bone, where left–right reflections would introduce non-physiological features.* |
| **Concede and defend** (*Although ..., ...*) | *Although this value is not physically realistic, its magnitude does not affect the results, as the MAGBF is defined as a pressure ratio and the model is linear.* |
| **Worked number** | *For the maximum simulated frequency of 10 kHz, the minimum wavelength in air is approximately 34 mm, resulting in a recommended element size below 4 mm. Accordingly, an element size of 3 × 10⁻³ m was selected for the air domain.* |
| **Sourced convention** | *These values correspond to typical bulk properties reported for acrylic-based polymers and are commonly used in engineering models when detailed material characterization is not available [63].* |

When no a-priori reason exists, she says so and states the a-posteriori check instead:

> However, unlike the acoustic domain, the propagation velocities in solid materials are not
> straightforward to define, making it difficult to directly estimate the corresponding
> wavelengths. For this reason, the mesh resolution was initially selected based on geometric
> complexity and numerical stability considerations. The adequacy of the mesh was then assessed a
> posteriori by inspecting the solution ...

Simplifications are named as such, with what they leave out:

> This layer was intended as a first-order geometric approximation rather than a detailed
> biomechanical model.

> ... although the true area and orientation of the eardrum are not explicitly represented by this
> approximation.

> ... representative values of a generic plastic material were assigned to the hearing aid as a
> simplifying assumption and kept constant across all patients.

Controls for comparability are stated with their purpose:

> To reduce external variability across patients and ensure comparability between simulations, the
> same device size and position were used for all subjects.

## 6. Problems found during the work go into the methods

5.1.4 contains a full problem-and-fix narrative instead of hiding the bug. Its seven moves, in
order:

1. **Expectation:** *The same pre-processing pipeline used during training was applied to all
   inference data to ensure consistency ...*
2. **Discovery:** *However, a fundamental affine convention discrepancy was identified between
   Dataset 1 and the high-resolution datasets.*
3. **Origin:** *The pipeline was originally developed on Dataset 1, which follows an LPS
   convention, ...* (with the matrix)
4. **Hidden assumption:** *These sign inversions were implicitly assumed by the cropping rules,
   orientation logic, and landmark-based rotations in the original pipeline.*
5. **Contrast:** *In contrast, Dataset 2 and Dataset 3 follow an RAS convention, ...* (matrix)
6. **Counterfactual consequence**, with a back-reference to theory: *As described in Section 3.1,
   this difference corresponds to a reflection across the left–right and anterior–posterior axes,
   meaning that applying the original pipeline directly ... would have produced anatomically
   mirrored volumes.*
7. **Fix and guarantee:** *To address this, the affine matrix of each input volume was inspected at
   runtime, and all spatial operations ... were reformulated in physical space ... This ensured
   that the pre-processed volumes were geometrically consistent with those seen during training,
   regardless of the underlying voxel-axis convention.*

This is the most reusable passage in the chapter. It turns a debugging episode into evidence of
care, and it tells the next student what will break.

## 7. Provenance: what was built, what was reused

She separates her own work from inherited tools in every section where both meet.

| Phrase | Role |
|---|---|
| *a bone segmentation model developed in this thesis and an externally developed tissue segmentation model, hereafter referred to as the tissue model* | introduces both, fixes a short name |
| *The bone segmentation model was fully developed, trained, and evaluated as part of this thesis.* | own work, stated once |
| *It was used exclusively for inference and downstream analysis.* | scope of the reused model |
| *applied without modification (see Appendix B for implementation details)* | unchanged reuse, detail to appendix |
| *based on an internal framework originally developed at Oticon* | inherited pipeline |
| *As part of this thesis, the bone segmentation framework was developed to align with the existing soft-tissue segmentation pipeline* | own adaptation of inherited code |
| *the pre-processing pipeline was extended to propagate the spatial transformations ...* | own extension, stated as a past passive |
| *the Operations team at Oticon provided a guideline document ...* then *In this work, a standardized location 3 mm beyond the first bend was selected.* | external guidance, own concrete choice |

The rule she follows: the verb says who did it. *developed in this thesis*, *extended*, *selected*
for her choices; *originally developed at*, *provided*, *applied without modification* for others'.

## 8. Numbers, settings and software

**Exact settings, with units, every time.** *0.74 mm*, *128 × 128 × 128 voxels with a batch size of
7*, *100 epochs*, *five-fold cross-validation*, *feature map widths of {32, 64, 128, 256, 320, 320}*,
*3 × 3 × 3 kernels*, *100 logarithmically spaced frequency points*, *100 Hz to 10 kHz*, *12 cores*,
*approximately 20 minutes per simulation*.

**Configuration names verbatim**, in the running text without code font: *3d_fullres*,
*nnUNetPlannerResEncL*, *nnUNetTrainerNoMirroring*, *craniofacial structures task*, *Exact Surfacing*,
*AutoSurface function with the Organic geometry setting*.

**Software cited at first use**, bracket after the name: *nnU-Net v2 framework [54]*,
*TotalSegmentator [39]*, *3D Slicer [53]*, *Geomagic Wrap [59]*, *ANSYS Mechanical software [41]*,
*eDrawings software [60]*. Later mentions are uncited, except 3D Slicer, which is re-cited each time.

**Cohort flow as counts.** *A subset of 100 volumes was selected from Dataset 1 ... split into
training and test sets using an 80/20 ratio*; *From the 758 pre-processed ear volumes initially
available in Dataset 1, 578 were retained following this filtering procedure. Similarly, Dataset 2
was reduced to 64 ears, and Dataset 3 to 68 ears.* The reader can reconstruct every *n* in Results.

**Approximately** (6 uses) only for measured or derived quantities (*approximately 13 mm*,
*approximately 50 epochs*, *approximately 343 m/s*), never for a setting she chose.

**Compute** is reported once, at the end of the simulation section.

## 9. Equations, tables and figures

### 9.1 Equations

Metrics and decision rules are defined in the Methodology, where they are used, not in the
background chapter. The chain is the same as in her clinical chapter:

1. Lead-in sentence ending on a colon or *defined as*: *Both metrics quantify the spatial overlap
   between the predicted segmentation P and the ground-truth segmentation G:*
2. Equation.
3. *where* sentence naming every symbol: *where |·| denotes the number of voxels in the
   corresponding region.*
4. One sentence on what the quantity tells you: *Dice measures the degree of overlap between
   segmentations (ranging from 0 to 1), while IoU provides a slightly more conservative estimate of
   agreement.*

Decision rules are written as equations, not prose: the IQR outlier interval
*[Q1 − 1.5 IQR, Q3 + 1.5 IQR]* and the selection bounds *µX − σX ≤ xi ≤ µX + σX*. Each is followed
by one sentence on what it achieves: *This criterion ensured that the selected subjects, while
representing relatively extreme anatomical configurations within the dataset, remained within one
standard deviation of the population mean for both variables.*

Secondary reported quantities get a definition in a clause, no equation: *Detection rate, defined
as the percentage of cases in which a landmark was successfully identified, was also reported.*

### 9.2 Tables

| Table | Content | Caption habit |
|---|---|---|
| 5.1 | feature name and one-line description | *Summary of geometric features extracted from ..., including ...* |
| 5.2 | tissue parameters with units in the header | states the source per column: *taken from Brummund et al. [9], whereas the loss factors were assumed based on representative values reported in the literature [9, 61]* |
| 5.3 | per-patient device properties | says which column was computed and which assumed |
| 5.4 | element size per domain | one line |

The caption carries provenance (measured, taken from, assumed). Text then walks the rows that need
a reason; rows that need none are left to the table.

### 9.3 Figures

- One overview figure at the chapter start, then one example figure per stage (*Example of ...*,
  *Overview of ...*, *Comparison between ...*).
- Each figure is cited in the paragraph that needs it, usually in brackets at the end of a sentence:
  *... a semi-automatic workflow was developed to produce the required reference masks
  (Figure 5.3).*
- Captions are one to four sentences: what is shown, how it is laid out (*Top row ... Left column
  ...*), and a visual note when something is hidden (*The tissue structures are hidden in the
  visualization for clarity*). Selection figures explain the colour code in the caption.

## 10. Tense, voice, cross-references and vocabulary

**Tense and voice.** Past passive for every action (*was applied* / *were removed*; *was* and *were*
occur 188 times in the chapter). Present for what a tool, metric or table *is* (*nnU-Net ... automatically adapts*,
*Dice measures*, *are summarized in Table 5.2*, *is shown in Figure 5.14*). Past perfect only for
ordering (*Once the four patients ... had been selected*). No first person.

**Cross-references are allowed here**, unlike in the introduction and literature review.

| Kind | Verbatim |
|---|---|
| Back to theory | *As described in Section 3.1, this difference corresponds to ...* |
| Back within the chapter | *as described in the previous subsection*, *described in Section 5.1*, *As part of the placement sensitivity analysis described in Section 5.5.1* |
| Forward within the chapter | *as will be explained in the next subsection* (once) |
| To appendices | *The detailed procedure followed can be found in Appendix A.*, *see Appendix B for implementation details*, *are provided in Appendix C* |

**Connective counts.** *ensure* / *ensuring* / *ensured* 21, *First* as a step marker in each workflow intro,
*In addition* 7, *Additionally* 4, *Finally* 5, *Subsequently* 5, *Following* 6, *while* 12,
*whereas* 2, *However* 3, *In contrast* 2, *Therefore* 3, *Specifically* 2, *In particular* 3.

**Evaluative words** cluster on the pipeline's own outputs: *representative* 12, *consistent* /
*consistently* 8, *simplified* 8, *accurately* 4, *reliable* 4, *realistic* 3. The chapter claims
care (*consistent*, *reliable*) more often than it shows it.

## 11. Where her chapter and this thesis part ways

These rules win over the Aïda pattern.

| Her habit | Rule for this thesis | Source of the rule |
|---|---|---|
| *ensure* 21 times, often as an unverified tail (*ensuring seamless integration*) | Use *ensuring* only when the guarantee is mechanical (same transform on image and mask). When it depends on data, name the check and its result instead. | `style_guide_aida.md` §8.2, `thesis-writing` skill |
| QC criteria listed, counts per reason absent (*Cases showing incomplete anatomical coverage ..., cropping artefacts, segmentation failures, ... were removed*) | Every exclusion gets a count per reason and the case IDs go to a file. "Log which cases failed rather than dropping them silently." | `CLAUDE.md` conventions |
| One deviation justified (no mirroring); others not flagged as deviations | **Every deviation from the published training settings is recorded**, in a table: setting, published value, ours, reason. Comparisons to the benchmark's Table 2 state them. | `CLAUDE.md` conventions |
| *the default nnU-Net stopping criterion* | Check each claim about a tool's behaviour against the tool's source or docs. nnU-Net trains a fixed number of epochs; it has no stopping criterion. Our settings are in `configs/cas_net.json` merged over `configs/pipeline.json`; quote those, not memory. | `CLAUDE.md` "How to explain things" |
| Appositive gloss after a tool name (*nnU-Net v2 framework [54], a self-configuring pipeline for biomedical image segmentation that ...*) | No inserted clauses. Give the gloss its own sentence or drop it if Chapter 3 defined it. | `style_guide_sota_aida.md` §10 |
| Textbook equations for every parameter (*ρ = m / V*, Young's modulus, Poisson's ratio) | Equations only for quantities the results report or decisions depend on (Dice, clDice, HD95, Betti errors, centreline metrics, any selection rule). | `style_guide_clinical_aida.md` §9.8 |
| Unit drift: Table 5.4 header says mm, the values and text say 3 × 10⁻³ m | One unit per quantity across text, table and caption. | proofreading |
| Signpost paragraphs (*Finally, the hearing aid was added to the geometry, as will be explained in the next subsection.*) | Cut one-sentence signpost paragraphs. The next subsection heading already says it. | `style_guide_aida.md` §8.1 |
| Stage count in the opener (five) differs from the section count (six) | Keep the enumerated opener and the sections in step. | proofreading |
| Em dashes | Never. En dashes only in compounds (*left–right*, *fluid–solid*). | all guides |
| Terms introduced with bold | No `\textbf`. Abbreviation in brackets after the first full term, as she does: *boundary conditions (BCs)*. | memory: `feedback_no_textbf_thesis.md` |

What to keep without change: the enumerated opener, the chaining openers (§4.1), the
what-why-check paragraph (§3), the six justification forms (§5), the problem-and-fix narrative (§6),
the provenance verbs (§7), exact settings and cohort flow (§8), and appendices for long procedures.

## 12. Mapping onto this thesis

### 12.1 Stages

Her five stages map onto ours as follows. Only the first is drafted; the rest are listed so the
opener can enumerate them once they exist.

| Her stage | Ours | Files |
|---|---|---|
| 5.1 AI-based segmentation (data prep, ground truth, model, inference) | CAS-Net trained from scratch on ImageCAS-X: data and splits, preprocessing, model, training, inference and postprocessing, evaluation | `thesis/pipeline/*.tex`; `knowledge/docs_thesis/cas_net_walkthrough.md` |
| 5.2 Population-level geometric analysis | centreline extraction and labelling, then tortuosity and bifurcation features | `bifurcation/`, `tortuosity/` |
| 5.3 Representative subject selection | (if any) case selection for figures or for the risk model | n/a |
| 5.4 to 5.6 | no counterpart | n/a |

### 12.2 Her provenance split, applied to ours

| Ours | Phrase to use |
|---|---|
| ImageCAS-X framework, configs, `CASNet3D`, losses, inference, metrics | reused: *was used without modification*, *the benchmark's training configuration* |
| `train.py --resume` and `<method>_last.pt` | own extension: *the training script was extended to resume from ...*, with the reason (walltime caps on the GPU queues) |
| Training from scratch, the comparison to the delivered weights | own work: *trained in this thesis* |
| Delivered pretrained weights | external: *provided with the benchmark*, *hereafter referred to as the pretrained model* |
| 0.5 mm resampled cache | reused or own, depending on who ran `utils/offline_resample_images_to_disk`; state it |

### 12.3 Candidates for a §6-style problem-and-fix paragraph

Write these up the way she wrote the affine discrepancy, if they affect a number:

- the venv's torch switched to a CPU wheel (`2.14.1+cpu`, 2026-10-05), so GPU jobs would have run on
  CPU without error;
- a checkpoint path left in a method config silently turns a fresh run into a fine-tune;
- `"resample"` in `preprocessing.steps` selects the cache and is then skipped at runtime.

### 12.4 Candidates for the deviations table

`amp` false (fp32, needs an 80 GB card); `cudnn_benchmark` if switched on; queue and GPU model
(`gpua100`, not the paper's hardware); resumed runs across walltime caps; ASSD not implemented, so
the paper's ASSD column is not reproduced.

## 13. Audit of `thesis/pipeline/` against this guide

| File | Words | Matches | Departs |
|---|---|---|---|
| `00_chapter_intro.tex` | 539 (mostly TikZ) | overview figure first, as her Figure 5.1 | heading *Understanding the Pipeline*; *This chapter walks through* signpost; no enumerated stage sentence; typos *preforming*, *Kit study*; 3 `\textbf` |
| `01_data_preparation.tex` | 571 | stage order | 6 `\textbf`; check for cohort flow counts (1000 → 800 → 560/80/160) |
| `02_model_architecture.tex` | 1,266 | | longest file; architecture explanation belongs in Technical Background, Methodology keeps settings; 6 `\textbf` |
| `03_training.tex` | 352 | settings given with numbers ($10^{-4}$, 1000 epochs) | teaches backprop and Adam (*Training adjusts the network's weights ...*); her methods never teach, they point back to Chapter 3; mid-sentence glosses; `--` as a dash; 5 `\textbf`; no deviations table |
| `04_inference.tex` | 377 | | 3 `\textbf`; check that tiling overlap, Gaussian blending, mirror axes and the 100-voxel component rule appear as exact settings |
| `05_evaluation_metrics.tex` | 475 | metrics defined in methods, as she does | 8 `\textbf`; must say ASSD is absent and why |

The current chapter is written as a tutorial. Hers is written as a record. The main revision is
moving explanation to the background chapter and replacing it with settings, reasons and checks.

This table is read-only. No `.tex` was edited.

## 14. Templates

**Chapter opener:**
> *The methodology followed in this work is summarized in Figure~\ref{} and consists of [n] main
> stages: (1) [stage, with its sub-steps]; (2) [stage]; ...; and ([n]) [stage].*

**Section intro:**
> *[Stage] was performed to [purpose]. The workflow consisted of [n] steps. First, [step].
> Subsequently, [step]. Finally, [step].*

**Chained subsection opener:**
> *Following [previous step], [this step] was applied to [input] to [purpose].*

**Step paragraph (what, setting, why, check):**
> *[Step] was performed using [tool] \cite{}, with [setting and unit]. [Setting] was chosen
> [to / as / since] [reason]. [Check] confirmed [result, with n] (Appendix~\ref{}).*

**Reuse versus own work:**
> *[Component] was used without modification \cite{}. [Other component] was extended in this
> thesis to [what], as [reason].*

**Deviation:**
> *[Setting] was set to [ours] instead of the published [theirs] \cite{}, as [reason]. All deviations
> are listed in Table~\ref{tab:deviations}.*

**Concede and defend:**
> *Although [simplification], [why it does not affect the reported quantity].*

**Problem and fix:**
> *However, [discrepancy] was identified between [A] and [B]. [A] [convention / assumption], which
> [component] implicitly assumed. In contrast, [B] [differs]. Without correction, [concrete
> consequence]. To address this, [fix]. [How the fix was verified].*

**Metric definition:**
> *[Metric] quantifies [property] between the prediction $P$ and the reference $G$: [equation]
> where [symbols]. [One sentence on what a high or low value means].*

## 15. Checklist before calling the chapter done

- [ ] One enumerated opener sentence plus an overview figure; the number of stages matches the sections.
- [ ] Sections in execution order; each opens by naming the previous step's output or its own purpose.
- [ ] Every paragraph says what was done, with which tool (cited at first use), with which setting.
- [ ] Every non-default setting has a reason in the same or next sentence.
- [ ] Every deviation from the published settings is in the deviations table.
- [ ] Every exclusion has a count per reason; the cohort flow reconstructs every *n* in Results.
- [ ] Own work and reused work are separated by the verb (*developed in this thesis* versus *used without modification*).
- [ ] At least one problem-and-fix paragraph where a bug would have changed a number.
- [ ] Metrics and decision rules defined as equations with a *where* sentence; no textbook equations.
- [ ] No teaching: theory is pointed back to (*As described in Section ...*), long procedures go to an appendix.
- [ ] Past passive for actions, present for definitions and table/figure pointers, no first person.
- [ ] *ensuring* only for mechanical guarantees; no *seamless*, *accurately represents* without a check.
- [ ] One unit per quantity across text, tables and captions.
- [ ] No em dashes, no `\textbf`, no inserted clauses, no one-sentence signpost paragraphs.
- [ ] `hunspell -l -t -d en_US -p wordlist.txt` returns only names; build with zero undefined citations.
