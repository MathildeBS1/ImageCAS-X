# Style guide: the Methodology chapter (after all former students' work)

Sources: everything in `Former_students_work/`. Four finished theses carry a methods chapter; the
eleven weekly reports show how methods text looked before it reached a thesis. Counts come from a
`pdftotext` extraction of each methods chapter (captions included, so word counts are slightly
high). Quoted phrases are verbatim, typos included.

This file is the cross-student synthesis. The deep reading of one chapter is
`style_guide_methodology_aida.md`; it stays the reference for paragraph mechanics and templates.
Where any student's habit clashes with the `thesis-writing` skill, `CLAUDE.md` or the memory
rules, §8 says which rule wins.

---

## 1. The sources

| Student | Work | Methods chapter | Words | Voice | Figs / tables / eqs | What it is best at |
|---|---|---|---|---|---|---|
| Jiménez Ordoñez (Aïda) | MSc 2026, ear-canal segmentation and FE simulation | Ch. 5 *Methodology*, after Data | ~5,700 | impersonal, past passive, no *we* | 17 / 4 / 4 numbered | pipeline-ordered chapter, chained openers, problem-and-fix paragraph, provenance verbs |
| Korona and Baldachowski | MSc, coronary tree tracing on ImageCAS, tested on **CGPS** | Ch. 5 *Methods*, after a separate Ch. 4 *Dataset* | ~8,300 | *we* 59, *our* 11; mostly present tense (*we perform*, *we define*) | 16 / 1 / ~27 | every parameter has a value and a reason; rejected alternatives named; architecture reused by back-reference |
| Amalie Kirstine | BSc, CT age prediction on **CGPS** abdominal CTA | Ch. 4 *Methodology*, dataset inside it | ~6,100 | *we* 43, *our* 23; past tense | 18 / 5 / ~13 | exclusion criteria with reasons, feature table, per-feature recipe, dropped feature with reason |
| Esther Holst Øksnebjerg | BSc, kidney cortex/medulla/cyst on **CGPS** | none; theory in Ch. 3 *Technical Background and Methods*, procedure inside Ch. 6 *Experiments and Results* | ~4,400 (Ch. 5 and 6) | impersonal, present passive | 7 / 7 / 0 | numbered processing pipeline with explicit label precedence; reused model's training data stated; test-selection rule |
| Weekly reports (Korona/Baldachowski, Aïda, Esther, Radutoiu, Petersen/Ægidius, Rasmussen, Matamoros) | 11 reports | n/a | 300 to 4,800 each | first person singular, questions to supervisors | n/a | show the drafting path from diary to thesis prose (§7) |

Three of the four theses use the Herlev–Østerbro (CGPS) cohort. Korona and Baldachowski are the
closest predecessor in topic: coronary centerlines on ImageCAS, generalisation tested on 939 CGPS
scans, and a short phenotype-clustering section on left main geometry (tortuosity, radii,
bifurcation angles).

## 2. What all four agree on

These are the conventions every finished thesis follows. Treat them as fixed.

1. **An overview figure opens the methods.** Aïda's Figure 5.1, Amalie's Figure 8 (*Overview of
   the project workflow*), Korona's tree-tracing schemas (Figures 5.10, 5.11). The caption
   summarises the stages in one or two sentences.
2. **Sections follow the order the data flows.** Data → preprocessing → model(s) → assembled
   algorithm or analysis → evaluation. Nobody orders by importance.
3. **Headings are noun phrases naming the stage or object.** *Data preprocessing*, *Branch point
   detector*, *Terminating criteria*, *Feature Extraction*, *Data Split*. Never a claim or a question.
4. **Every setting is given as a number with its unit.** *41 x 41 x 41 voxels*, *τ = 1 mm*,
   *0.5 mm*, *a 15-voxel margin*, *3 iterations using a 6-connectivity structural element*,
   *learning rate 5 · 10⁻⁵*. Training hyperparameters go in a two-column table (Korona Table 5.1,
   Amalie Tables 3 and 5).
5. **Tools are named and cited at first use.** *VTK [49] function vtkDijkstraGraphGeodesicPath*,
   *vmtkcenterlines method from VMTK [50]*, *TotalSegmentator [12]*, *the XGBoost Python package
   [77]*. Function and subtask names appear verbatim (*kidney_cysts*, *tissue_4_types*).
6. **Metrics are defined as equations in the methods, with a *where* clause for every symbol.**
   Korona's OV, AI and coverage (eqs 5.24 to 5.26), Aïda's Dice and IoU, Amalie's ratios.
7. **One example figure per non-obvious step**, cited in the sentence that needs it, caption saying
   what the colours mean.
8. **Cross-references are allowed and used.** Back to background (*As described in section 3.2*),
   back within the chapter (*as described in section 5.2.2*), to appendices.

## 3. Where they differ, and the choice for this thesis

| Question | Options seen | Choice | Why |
|---|---|---|---|
| Person and tense | Aïda: impersonal past passive. Esther: impersonal present. Korona: *we* + present (*we perform*). Amalie: *we* + past. | **Impersonal, past passive for actions; present for definitions, metrics and what a figure or table shows.** | Matches the current `methodology/06_curvature.tex` draft and the majority of the theses read as records, not plans. Korona's present tense reads like a design document. |
| Where the dataset goes | Separate chapter before methods (Korona, Esther, Aïda) or first section of methods (Amalie). | **First section of the methodology** (`01_population_outcome.tex`). | The outline already puts it there; cohort flow and exclusions belong next to the methods that cause them. |
| Where theory goes | In methods (Korona teaches vMF, Ward linkage, Thomson 1904; Amalie walks ResNet block by block and explains XGBoost gain). In background, pointed back to (Aïda). | **Background chapter; methods point back.** The one exception is a quantity this thesis defines itself (the turning angle in `06_curvature.tex`). | Methods hold decisions, settings, reasons. Teaching in methods is the main length problem in Korona and Amalie. |
| Methods and results together | Esther interleaves each experiment's method with its results. Others separate them. | **Separate.** | Interleaving made Esther's chapter hard to cite and pushed method text into *Results*. |
| Chapter roadmap paragraph | Esther: *Section 6.1 presents ..., while section 6.2 investigates ...*. Aïda: one enumerated sentence plus figure. | **Aïda's enumerated sentence.** No section-by-section roadmap. | The roadmap duplicates the headings. |
| Lists | Korona and Esther use numbered lists for procedures and criteria; Aïda uses prose. | **Numbered list only when order or identity matters** (a pipeline the text then refers to by number, a set of stopping criteria). Otherwise prose. | Korona's *Conditions 1 and 2 are straightforward* only works because the list is numbered. |

## 4. Patterns to borrow, by student

### 4.1 Korona and Baldachowski: value plus reason for every parameter

Each tuned constant is stated, then defended by what goes wrong on either side of it.

> In this project, σm = 3. Its value was chosen to send the tracer far enough so that it does not
> come back to the same point again, while minimizing the risk of sending it to other centerlines
> in the coronary tree our to the regions where coronary arteries are not present.

> The value of the chosen threshold serves as a balance between tracking for too long and missing
> parts of the coronary tree due to stopping too early.

**Asymmetric-cost reasoning.** When a rule trades two errors, they say which error is worse first:

> An important thing for consideration was that terminating the tracing too late is not as harmful
> as terminating too early. Terminating too early would result not only in a missing part of a
> centerline, but also in inability to detect potential bifurcation points on it ...

**Rejected alternative, then the choice.** Name the obvious option, its defect, then what was used:

> A popular method of distributing points on a sphere is a latitude-longitude lattice [55] ... A
> drawback of this method is that points are distributed in a highly anisotropic manner and are
> clumped together near the poles. To avoid those issues, we used a Fibonacci sphere algorithm [55].

**Reuse by back-reference.** Shared components are described once; later sections state only the
difference:

> The model architecture follows the one described in section 5.2.2 with the modified output layer,
> as in this case the model outputs only one value, the likelihood of a point being a branch point.

**Predecessor provenance.** Prior DTU theses are cited as sources and the modification is named:
*a modification of a solution used in Radutoiu's thesis [13]*; *inspired by reward function in
Ekner's thesis [52]*. Then one sentence on what the modification buys (*essentially changes the CNN
from a classification to regression type, provides more flexibility*).

**Special cases with their reason.** *For the initial tracked centerline ... we allow the tracer to
work for 10 steps before checking the terminating conditions. The reason for that is the
segmentation of the coronary tree in regions close to the aorta is of mixed quality ...*

### 4.2 Amalie Kirstine: cohort flow, feature recipes, honest exclusions

**Exclusion criterion with its purpose in the same sentence.**

> subjects with CT scans < 500 slices were excluded to ensure sufficient anatomical region coverage.

**Cohort-flow surprises go in the caption.** Table 2: *11 scans were removed after the initial
split because the subjects' ages were < 40 years. Since the exclusion happened after splitting the
data, there is a slight difference in the final number of scans in each set.*

**Feature table** with three columns: human name, name in the code, tool that produced it. The
reader can trace any feature in Results back to a mask and a function.

**Per-feature recipe:** source mask → restriction → formula → figure. The restriction is written as a
set equation, which makes it checkable:

> Sfeature = Sfeature,original ∩ SL1-L4 mask

**Normalising for acquisition differences, with the bias named first.** *The CT scans varied in the
number of slices and anatomical coverage ... This variation can introduce bias in some extracted
volume- or ratio based features ... To reduce this bias, volume and ratio features were computed
within a standardized anatomical region.* The coronary analogue is any feature that scales with
how much of the tree the segmentation reached.

**A feature dropped, with the reason.** *upon investigating some subjects, we found that some scans
did not include the entire liver ... which is why it was excluded as an input feature.* Features
considered and not used are part of the method.

**Problem and fix for a reused tool.** TotalSegmentator fat leaking outside the body led to a body
mask; the Korfiatis model mixing left and right led to a merge-and-split postprocessing step, each
with a before/after figure.

### 4.3 Esther Holst Øksnebjerg: explicit pipelines and stated limits

**Numbered pipeline whose steps each name input, operation, output**, ending in a precedence rule
that resolves overlaps:

> In cases where a voxel is labelled as both cyst and cortex/medulla, the cyst label takes
> precedence. The resulting final segmentation mask contains four mutually exclusive classes ...

**What a reused model was trained on.** *the model was trained and validated on 1238 and 306
contrast enhanced pre-donation CT scans ... The subjects were healthy individuals evaluated as
potential kidney donors*, with a table of that population. For any pretrained model applied to
Herlev–Østerbro, state the population it saw.

**Decision rule for statistical tests.** *If the data for a variable could be considered normally
distributed, based on the result from the Shapiro–Wilk test, within both groups, Welch's t-test was
performed ... Otherwise, the Mann–Whitney U-test was performed.*

**Design limits stated plainly.** *By design, all samples were included in the cross-validation
setup, and no independent test set was held out.*

**When no ground truth exists, say how the output was checked instead.** *Since there are no manual
segmentations available ... a quantitative evaluation of the framework cannot be made on this
dataset. Instead, the predictions are inspected visually.*

### 4.4 Aïda Jiménez Ordoñez

Covered in full in `style_guide_methodology_aida.md`. The four things only she does well: the
enumerated opener sentence (§2.1 there), chained subsection openers (*Following ...*, *Prior to
...*, *Once ... had been*; §4.1), the seven-move problem-and-fix paragraph (§6), and provenance
verbs that say who did the work (*developed in this thesis* versus *applied without
modification*; §7).

## 5. Anti-patterns seen across the theses

| Pattern | Example | Instead |
|---|---|---|
| Teaching in the methods | Korona's history of the Thomson problem; Amalie's block-by-block ResNet-18 and XGBoost gain | Background chapter, one back-reference |
| Promotional adjectives on tools | *state-of-the-art AI-based tools*, *robust and widely used*, *a perfect candidate* | Say what the tool does and why it fits this data |
| *ensure* as a free guarantee | *This ensured that all included CT scans were suitable for model training* | Name the check and its count |
| Vague exclusions | *Most of images, having various quality issues ..., were excluded* (Korona, 1000 → 762) | Count per reason, case IDs in a file |
| *accurate enough* without a number | *the results were accurate enough for the goal of branch spawning* | State the tolerance, or say it was not measured |
| Exploratory results in methods | Amalie's mean age 60.4, age histograms in 4.1.1 | Cohort table in methods; distributions in Results |
| Tense drift | Korona: *we perform*, *has been processed*, *was used*, *we decided* in one section | One rule (§3) |
| Methods placed in Results | Esther 6.1 and 6.4 | Separate chapters |
| Unit or symbol drift | Aïda's mm/m table; Korona's *ω* in the equation, *w* in the text | One unit and one symbol per quantity |

## 6. What carries straight over to Herlev–Østerbro

Concrete things from the predecessors that this methodology needs to state, because the CGPS
theses either did them well or left them open:

- **Cohort definition and flow** (Amalie, Esther): who was invited, age bound, CT protocol, which
  subset this thesis received, then every exclusion with a count. `01_population_outcome.tex`.
- **What the delivered labels are** (Korona): *segmentations of left coronary trees automatically
  extracted with nnU-Net model [47], corrected manually by one expert*. State who produced every
  label used, automatic or manual, and how many readers.
- **The pretrained models' training populations** (Esther): CAS-Net or TotalSegmentator were not
  trained on Herlev–Østerbro; say what they were trained on.
- **Centerline extraction recipe** (Korona 5.1): seed from aorta overlap, endpoints from geodesic
  maxima, VMTK centerlines with inscribed-sphere radius, and the known failure (*overestimated
  spheres* at stenoses). `03_centerline_tree.tex`.
- **Feature definitions as equations with a figure** (Korona 5.9, Amalie 4.3.1): one schematic
  figure of where each feature is measured, like Korona's Figure 5.16. `05_features.tex` onward.
- **Features considered and not used** (Amalie's liver volume). Already a subsection in
  `methodology_long_draft.tex`.
- **Coverage normalisation** (Amalie's L1 to L4 window): any per-artery feature that depends on how
  far distally the segmentation reaches needs a fixed reference length or region, stated as such.

## 7. From weekly report to thesis

The reports show that methods text is drafted weekly and lifted into the thesis. Korona and
Baldachowski's Weekly Report 10 §1.2.1 is their thesis §5.1 almost word for word (*Each image and
the corresponding segmentation has ben processed so that it can serve as an input ...*). Draft
weekly methods in thesis register and the lift is free.

What changes on the way, shown by Esther's Weekly Report 5 against her thesis §6.1:

| Weekly report | Thesis |
|---|---|
| *I had some trouble running their code, since they used some old versions of python and tensorflow* | dropped |
| *I tried running the model on a couple of the whole-body CT scans ... but the predictions were very bad, so I decided to crop the images around the kidneys* | *The full-body scan is cropped to the kidney region.* |
| *I added a margin of 15 voxels in each dimension* | *This bounding box is then expanded by a 15-voxel margin in every direction* |
| *NB: I'm not 100% sure which are left and right.* | resolved before writing; left/right split by TotalSegmentator masks |

Aïda's Weekly Report 2 tried TotalSegmentator, then thresholding, then a mix. In the thesis the
dead ends shrink to one sentence of reason: *Since no curated dataset exists for the bony
structures ..., a semi-automatic workflow was developed*.

Rules for the conversion:

1. First person singular, hedges (*I think*, *not 100% sure*) and questions to supervisors go.
2. Dead ends survive only as the reason for the final choice, unless the comparison is a result.
3. Uncertainties are resolved or become a stated limitation; never carried over as *NB*.
4. Placeholders like Petersen and Ægidius's *train/val/test?-set* are fixed before the lift.
5. Qualitative figures state how cases were chosen, as Radutoiu's caption does: *The first two
   represent the best cases, the next two average cases, and the last is the worst case*, with the
   scan IDs.

## 8. Rules that win over any student

| Student habit | Rule | Source |
|---|---|---|
| *we* / *our* (Korona, Amalie) | Impersonal past passive | §3; current draft |
| Em dashes, `--` as a dash | Never; en dash only in compounds (*cortex–medulla*) | memory `feedback_no_em_dashes.md` |
| Bold term definitions | No `\textbf` | memory `feedback_no_textbf_thesis.md` |
| Paragraphs opening *Because* (Amalie 4.3.1: *Because CT images consist of voxels with known spatial dimensions ...*) | Fact first, then *so* | memory `feedback_no_because_opening.md` |
| Appositive glosses after tool names | Own sentence or drop | `style_guide_sota_aida.md` §10 |
| Exclusions without counts | Count per reason; failed case IDs logged to a file | `CLAUDE.md` conventions |
| Deviations from a published setup mentioned in passing | Deviations table: setting, published, ours, reason | `CLAUDE.md` conventions |
| Claims about a tool's behaviour from memory | Check against source or docs | `CLAUDE.md` |
| Numbers without population | Every *n* reconstructible from the cohort flow | `thesis-writing` skill |

## 9. Checklist

- [ ] Overview figure and one enumerated opener sentence; stage count matches section count.
- [ ] Population first: source, inclusion, protocol, exclusions with counts per reason.
- [ ] Sections in data-flow order; each opens from the previous output or its own purpose.
- [ ] Every tool cited at first use; every reused model's training population stated.
- [ ] Every parameter has value, unit and reason; trade-off parameters say which error is worse.
- [ ] Obvious alternatives named and rejected in one or two sentences where a reader would ask.
- [ ] Shared components described once, later sections give only the difference.
- [ ] Features: equation, *where* clause, schematic figure, and a list of features considered and dropped.
- [ ] Coverage or acquisition bias in any feature named and normalised.
- [ ] Problems found during the work written as problem and fix where they affect a number.
- [ ] No theory taught; back-references to the background chapter.
- [ ] Qualitative figures state how the shown cases were selected, with IDs.
- [ ] Impersonal past passive; present only for definitions and pointers.
- [ ] No em dashes, no `\textbf`, no *Because* openings, no promotional adjectives, no unchecked *ensure*.
