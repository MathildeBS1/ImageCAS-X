# schultz2023ess — CCTA-based endothelial shear stress in normal coronary arteries

**Citation:** Schultz J, van den Hoogen IJ, Kuneman JH, de Graaf MA, Kamperidis V, Broersen A,
Jukema JW, Sakellarios A, Nikopoulos S, Tsarapatsani K, Naka K, Michalis L, Fotiadis DI,
Maaniitty T, Saraste A, Bax JJ, Knuuti J. *The International Journal of Cardiovascular Imaging*
2023;39(2):441–450. doi:10.1007/s10554-022-02739-0. PMID 36255544, PMC9870961. CC BY.
**Read:** 2026-09-07 — **full text of the published version**, 10 pages, PDF supplied by the user and
stored beside this entry.
**Source:** `docs_thesis/papers/Coronary computed tomography angiography-based endothelial wall shear stress in normal coronary arteries.pdf`
**Verdict:** A template for how objective 8 should be reported, and a list of the exclusions that
make such a study possible — but its headline gradient is substantially an artefact of its own
boundary conditions, so it is a form to copy rather than a result to build on.

## What they did

Consecutive patients referred for clinically-indicated CCTA for suspected CAD, Turku University
Hospital, 2007–2011. 172 patients screened; arteries **without atherosclerosis identified by visual
inspection** in multiple views. 357 normal vessels found, 8 dropped (7 failed ESS analysis, 1
ambiguous), leaving **349 vessels from 168 patients** (mean age 59 ± 9, 39% men) and **5223 3-mm
segments**. By vessel: 93 LAD, 127 LCx, 129 RCA. Median analysed vessel length 42 mm (IQR 33–54).

64-row PET-CT, in-plane resolution **~0.4 mm**, slice thickness **0.625 mm**, 512 × 512, imaged in
diastole with rate control and nitrate. That resolution is close to ImageCAS-X's (0.318–0.43 mm
in-plane, 0.5 mm slices), so its feasibility limits are likely to transfer.

**Four exclusions define the study, and all four matter here:**
- The **left main was excluded** from the simulations. LAD and LCx were reconstructed *after* the
  bifurcation and treated as independent vessels.
- **Side branches were not analysed.**
- **Boundary conditions were not patient-specific**: a fixed 100 mmHg inlet pressure and a uniform
  1 ml/s outlet velocity for *every* vessel, because CCTA supplies no velocity data.
- Steady-state, Newtonian, rigid-wall CFD.

ESS computed on 0.5 mm cross-sections, pooled into 3-mm segments, averaged over 90° arcs; minimal
and maximal ESS are the min and max of those arc averages around the circumference.

## What they found

ESS highest in LAD, then LCx, then RCA — minimal 2.3 / 1.9 / 1.6 Pa and maximal 3.7 / 3.0 / 2.5 Pa
(both p < 0.001), still significant pairwise after adjusting for lumen diameter.

By sex: men lower than women, **minimal ESS 1.7 vs 1.9 Pa (p < 0.001), maximal 2.7 vs 2.9 Pa
(p = 0.044)**, surviving adjustment for lumen diameter. Median lumen diameter was larger in men,
3.1 vs 2.8 mm.

By lumen-diameter tertile: small (< 2.6 mm) 3.8 Pa (IQR 2.4–6.6) minimal and 6.0 Pa (3.8–10.1)
maximal, against 1.7 / 2.6 for intermediate and 1.2 / 2.0 for large (p < 0.001). Correlation between
ESS and distance from the ostium ρ = 0.22–0.62.

## What the abstract does not tell you

- **The diameter gradient is partly the authors' own artefact, and they say so.** From Limitations:
  *"The lack of side branches indicates that the simulated flow in the distal parts of the vessels is
  higher than in reality, and this can result in unrealistically high ESS values as seen in our
  study."* The headline "ESS is highest in small segments" is therefore not a clean biological
  finding — with no side branches to carry flow away, the model pushes the whole inlet flow through
  the narrowing distal vessel.
- **Flow was not patient-specific.** With Q fixed at 1 ml/s for every vessel and τ ∝ Q/R³, the
  reported ESS is close to a monotone restatement of lumen radius. The sex and vessel differences
  survive adjustment for diameter, but the diameter gradient itself is largely built in.
- **No invasive comparison.** They concede: *"Our study does not provide direct comparison of CCTA
  based ESS values with those obtained using invasive methods."* This is **not** a validation of
  CCTA-derived shear; `eslami2021ccta` and `ding2023ccta` are.
- **The sex effect is small.** 1.7 vs 1.9 Pa, and p = 0.044 for maximal ESS. On 5223 segments,
  significance is cheap.
- **Segment-level statistics on clustered data.** 5223 segments come from 349 vessels in 168
  patients; the ANCOVA is on segments, with no clustering adjustment evident in the text I read.
- **"Absence of atherosclerosis" was a visual call**, not a calcium score of zero or any quantitative
  criterion.
- **The distal feasibility failure is real and separate from the artefact above:** *"the ESS analysis
  process was not feasible in all vessels, which was especially the case in distal segments likely
  due to limited resolution of CCTA and motion artefacts."*

## What it licenses

- **Objective 8, as a form to copy.** A normative distribution over a disease-free cohort, reported
  per fixed-length segment, stratified by vessel, by sex and by calibre, with feasibility reported as
  analysed vessel length. That is the shape of the population description this thesis owes, and it is
  the closest published precedent found in either search pass.
- **Stratify by sex.** Two unrelated quantities now show a sex difference in coronary geometry —
  this and `temov2016bifurcation` — so pooling the sexes is not defensible.
- **Report feasibility, not just results.** Their median analysed length of 42 mm and their 8
  excluded vessels are reported honestly; our per-case failures should be too
  (`CLAUDE.md`: log which cases failed rather than dropping them silently).
- **The resolution limit is real at our own voxel size.** Their 0.4 mm / 0.625 mm is close to
  ImageCAS-X, and distal analysis failed for resolution and motion. Any distal feature we define
  inherits that.
- **Whole-tree gap, third independent confirmation.** They excluded the left main and treated LAD and
  LCx as unrelated vessels. Even a study explicitly about normal coronary anatomy does not analyse a
  tree.

## What it does NOT license

- **Not a validation that CCTA-derived shear is accurate** — they explicitly did not compare against
  invasive imaging.
- **Not "shear rises toward the distal vessels"** as a biological claim. In this study that is
  produced by omitting side branches.
- **Not a normative reference range anyone should compare our numbers against**, because the
  boundary conditions are non-physiological and uniform across patients.
- **Not a sex effect of any magnitude worth acting on clinically** — 0.2 Pa. It licenses
  stratification, not interpretation.
- **Not a tree-scale result.**

## Open questions

- Their exclusions are exactly our inclusions: we have the left main, the side branches and the
  segment labels. Does a tree-scale descriptive study become straightforwardly novel simply because
  the CFD studies cannot afford to keep the branches?
- They report ESS per 3-mm segment with min/max over 90° arcs. Is a fixed-length segmentation the
  right along-vessel parameterisation for our topological features, or does
  `nannini2024characterization`'s normalised geodesic-distance zoning fit better?
- Their reference [32] is cited as showing that omitting side branches costs little predictive
  accuracy. Worth chasing before we assert that side branches matter for feature extraction.
