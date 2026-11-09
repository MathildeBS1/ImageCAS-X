# Designing the literature summary (evidence) table: state of the art, gap and inconsistencies

Scope note (2026-11-07). The sources below were opened in full unless marked "[not opened]". PMC served a captcha for part of the session, so two PMC articles were read through the Europe PMC full-text XML service, which serves the same text. Only one real thesis table could be read and checked (Xing 2019, Erasmus). Searches of TU Delft, DiVA, DTU Orbit, Imperial Spiral and Aarhus Pure gave no thesis with an extractable state-of-the-art table on coronary geometry, so the "3–6 thesis examples" target is **not met**. One published review in the same field (Rampidis et al. 2022) is used as the closest example. The current table and the studies already in the chapter come from `Thesis_coronary/content/litterature_review/03_geometry_risk.tex` (four rows: Zhang 2024, Li 2011, Tello Ayala 2026, Han 2022; the text also discusses Sakellarios 2017, Tommasino 2024, Won 2022 (PARADIGM) and Bergström 2021 (SCAPIS)).

## 1. How do real theses and reviews in the field structure their state-of-the-art tables?

### Takeaway
The examples that could be checked use one row per study (or per model/parameter) and 4–5 descriptive columns: what was studied, the setting/population, the measure, and a short finding. None has explicit gap or design-feature columns. That is the weakness of the current thesis table too: the gap sits only in the caption and text.

### Cited Findings
- **Xing R. (2019), PhD thesis, Erasmus University Rotterdam, "Wall Shear Stress and Atherosclerotic Plaque Progression"**, Chapter 2 (a review), Table 1 "Animal models of different surgically manipulated flow velocities" (runs over two pages). Exact columns: *Model flow manipulation | Flow velocity and shear stress profiles | Reported vessel pathology | Animal species | Remarks*. Rows are grouped by type of model (AV-fistula, vascular graft, ligation with sub-rows complete/partial, aortic constriction, perivascular device), not by year. Cells are bullet fragments with superscript reference numbers; the "Remarks" column carries the limitation or special feature of each model (e.g. "No surgery induced vessel damage at site of plaque development") — [Xing 2019 thesis PDF](https://repub.eur.nl/pub/117214/Thesis_XING_Final_All.pdf) (text extracted locally from the PDF).
- **Rampidis et al. (2022), Diagnostics 12(9):2178**, a review of coronary geometry and plaque in the CCTA era. Table 1, "Relationship between main geometric features proposed in the literature and atherosclerosis", has the columns *Parameter | Outcome | Modality | Number of Patients [n]* and 12 rows, ordered as the text discusses them (LM length … RCA shape, CAVi index), not grouped by design. Findings are short direction phrases ("Shorter in CAD patients", "Negative correlation", "Positive correlation"). Some rows give no direction, and significance is rarely stated. One footnote lists the abbreviations — [Rampidis 2022, Europe PMC full text](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9497479/fullTextXML)
- Weaknesses in that table, seen when it is checked against its own text: the "Number of Patients" column holds non-patient units (15 autopsy hearts; CFD models). Tortuosity in Tuncay et al. is tabulated as a general positive association although the text says it held "only at the per-segment level". The conflict over the LM angle is only in the text ("Contrary to this study, Saltissi et al. found no significant difference in the left main angle"), so the table hides it — [Rampidis 2022](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9497479/fullTextXML)
- The same review names the measurement inconsistency outright: "questions still remain regarding the optimal parameter with which to quantify coronary arterial geometry", and "which modality should be used (ICA vs. CCTA), whether dynamic or static measurements should be made" — [Rampidis 2022](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9497479/fullTextXML)
- Example of an opposite direction in the field: Khosravani-Rudpishi et al. (2018, 737 patients) found significant coronary tortuosity *negatively* correlated with CAD and noted that "some studies declare a positive correlation … although some others are in the opposition" — [J Cardiovasc Thorac Res 2018, PMC6335987](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6335987/) (search snippet only; [not opened in full])

### Inferences
- Both checked tables are *descriptive* tables. A reader can see what was done but not what is missing, because no column measures each study against the thesis question. The Rampidis table shows how a free-text "finding" column hides inconsistency: rows read alike although the text reports conflicts. Its "Number of Patients" column shows how mixed units creep in when the column is not defined.
- The Xing "Remarks" column is a compact model for a per-row limitation without a full risk-of-bias column.

### Gaps
- No DTU, KU, Aarhus, Karolinska, TU Delft, ETH or Imperial MSc/PhD thesis with a coronary geometry/CCTA state-of-the-art table could be retrieved. The TU Delft repository refused connections, DiVA/Orbit search results did not surface relevant theses, and Erasmus theses beyond Xing (e.g. Tziotziou 2025, "Coronary and Carotid Atherosclerosis: Morphometrics and Biomechanics", [EUR event page](https://www.eur.nl/en/events/phd-defence-aikaterini-tziotziou-2025-08-26)) were not opened. Column sets of further thesis tables are therefore **not reported**; nothing has been invented.

## 2. What do reporting and appraisal frameworks prescribe for evidence tables?

### Takeaway
None of the frameworks prescribes a fixed layout. They say what the columns must capture (PICO/PECO elements; for prediction studies, the CHARMS domains). They also say that tables beat prose, that rows should be ordered the way the synthesis is argued, and that the direction of effect is a legitimate summary when estimates are not comparable.

### Cited Findings
- **PRISMA 2020, item 17**: "Cite each included study and present its characteristics." Item 18: "Present assessments of risk of bias for each included study." Item 19 asks for per-study results, "ideally using structured tables or plots". Item 20a: "For each synthesis, briefly summarise the characteristics and risk of bias among contributing studies." No table format is given — [Page et al. 2021, PRISMA 2020 statement, PMC8005924](https://pmc.ncbi.nlm.nih.gov/articles/PMC8005924/)
- **Cochrane Handbook ch. 9 (summarising study characteristics)**: "Tabulating study characteristics is generally preferable to lengthy description in the text" (9.3.5). "Tabulating study characteristics can help to explore and compare PICO elements across studies" (9.3.2). Data "can be ordered in many different ways (e.g. by comparison or by specific PICO elements)", and the best order depends on the table's purpose (9.3.2). Reordering "by comparison, outcome and time frame" shows which studies inform which question (9.3.3). Characteristics should be coded into pre-specified categories (9.3.1, Table 9.3.a). Tabulation "can also help to improve the transparency of decisions made around grouping of studies" (9.3.5). Authors must check that the review's "direction of effect and statistical significance" match the primary studies (9.4) — [Cochrane Handbook ch. 9](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-09)
- **SWiM (Campbell et al. 2020, BMJ 368:l6890)**, nine items: grouping studies for synthesis; standardised metric and transformation; synthesis methods; criteria to prioritise results; investigation of heterogeneity; certainty of evidence; data presentation methods; reporting results; limitations of the synthesis. Item 7: "Study findings presented in tables or graphs should be ordered in the same way as the syntheses are reported". It names "vote counting based on direction of effect" as an acceptable synthesis method and "effect direction plots" as a display. Item 9 asks authors to report the limitations of the synthesis, including "the standardised metric(s) used" — [SWiM, Europe PMC full text PMC7190266](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7190266/fullTextXML)
- **CHARMS (Moons et al. 2014, PLoS Med 11:e1001744)**, 11 extraction domains for prediction-model studies: source of data (design; cohort designs recommended for prognosis; "a non-nested case-control design is inappropriate for developing a prediction model"); participants (recruitment, setting, eligibility); outcome (definition, blinding); candidate predictors (definition, measurement, "available at the intended time of use", handling of continuous predictors); sample size (events, EPV); missing data; model development; model performance ("Calibration and discrimination should always be recorded"); model evaluation (apparent / optimism-corrected / external); results; interpretation. No table layout is prescribed — [CHARMS, PLoS Med](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1001744)
- **Evidence gap maps (Snilstveit et al.)**: a matrix of interventions (rows) by outcomes (columns), with cells showing the amount and quality of evidence, so that empty cells are the gaps — [Snilstveit et al. 2013, World Bank WP 6725](https://documents1.worldbank.org/curated/en/212651468163487838/pdf/WPS6725.pdf) (search summary; the full PDF was [not opened]). The often cited journal version, Snilstveit et al. 2016, J Clin Epidemiol 79:120–129, was [not opened].
- **Garrard Matrix Method**: a grid with documents as rows and abstraction topics as columns; the first columns are author/title/journal, year and purpose, and the remaining columns are chosen for the review's purpose — [Goldman & Schmalz 2004, Health Promot Pract, describing Garrard](https://fenix.iseg.ulisboa.pt/downloadFile/563083097459317/Goldman_Schmalz_2004.pdf) (search summary; Garrard's book itself was [not opened]; [catalogue record](https://libcat.mcphs.edu/Record/p818097/TOC))
- **University writing-centre synthesis matrices**: sources go in rows and themes in columns. Common content columns are methodology, key findings and gaps. One guide advises starting with a citation column plus three or four theme columns, and warns that too many columns turns the matrix into clerical work. A matrix is meant to move the writer from summary to synthesis — [UNC Writing Center](https://writingcenter.unc.edu/2022/03/synthesis-matrix); [SUNY Poly](https://sunypoly.edu/sites/default/files/Using%20a%20Synthesis%20Matrix.pdf); [Stanford](https://teachingwriting.stanford.edu/synthesis-matrix) (aggregated through search results; not each opened in full)
- **PROBAST** (Wolff et al. 2019, Ann Intern Med; domains: participants, predictors, outcome, analysis) and **PECO/PICOTS** were [not opened] in this session. They are named here only as the natural sources for an "exposure = geometry, timing = before disease" framing.

### Inferences
- The thesis question is an exposure (PECO) question with a prediction purpose. The columns that carry the gap map onto CHARMS domains: *source of data* (design), *participants* (setting: referred vs random population), *predictors available at the intended time of use* (geometry before plaque), *outcome* (incident plaque vs prevalent CAD vs events), and *model development/evaluation* (adjustment for risk factors; incremental value).
- The evidence-gap-map idea fits a review table as a set of design-feature columns with check/cross cells. The empty "column of crosses" is the gap, seen at a glance.
- SWiM item 7 and Cochrane 9.3.2–9.3.3 support ordering rows by the strand/design the text argues through, not chronologically.

### Gaps
- No framework gives a number of rows or columns for a printed table; the limits in section 4 are inferences.

## 3. How to encode the gap and the inconsistencies

### Takeaway
Encode the gap as a few narrow yes/no design-feature columns defined by the thesis question. Encode inconsistency with a "measure as defined" column and a separate direction column (+ / − / 0). Keep the free-text finding short and attached to the measure.

### Cited Findings
- Coding characteristics into pre-specified categories makes studies comparable and grouping transparent — [Cochrane ch. 9.3.1, 9.3.5](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-09)
- Direction of effect is a valid comparative summary when metrics differ ("vote counting based on direction of effect"; "effect direction plots"), but the metric used must be stated as a limitation — [SWiM items 3, 7, 9](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7190266/fullTextXML)
- Free-text "outcome" cells with no direction can hide conflicts that the text reports (LM angle, Friedman vs Saltissi; tortuosity only per segment) — [Rampidis 2022](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9497479/fullTextXML)
- CHARMS asks whether predictors were "available at the intended time of use". Geometry measured after plaque fails this for a "before plaque" prediction question — [CHARMS](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1001744)
- The thesis chapter already contains one direction conflict: Li 2011 (bend count on invasive angiograms, 1,010 patients) reports tortuosity *inversely* associated with CAD, while Tello Ayala 2026 (RCA turning-angle profile on CCTA, 22,334 referred patients) reports tortuosity *higher* with CAD (from `03_geometry_risk.tex`).

### Inferences
- The four gap features follow straight from the thesis question and the chapter text. **Plaque-free at geometry measurement** (all ✗ except Won 2022, which measured no geometry). **Random population sample** (only Bergström 2021/SCAPIS, scanned once). **Follow-up to incident plaque** (Won 2022). **Adjusted for risk factors.** A fifth, **automated whole-tree measurement**, is in the text's gap sentence and can be folded into the measure column ("automated, whole tree" vs "manual, RCA only") instead of taking another column.
- Rows that show the gap but measure no geometry (Won 2022, Bergström 2021) are worth including. They make the gap visible from the other side: the cohorts with the right design have no geometry. A geometry cell of "—" (none measured) is informative.
- Direction column: use +, −, 0 (null) and "n/a" for studies with no association test. Define in the footnote what + means (higher value of the geometric measure ↔ more disease). Where the measure is a *profile* (Tello Ayala) or a classifier (Zhang 2024), write "discriminates" and not a sign, so that no direction is invented. A "this thesis" final row (all ✓, measure listed, direction "?") is a common device, but it must read as design, not as a finding.
- To avoid overclaiming in finding cells, give the association as the study's own measure and outcome ("bend count inversely associated with angiographic CAD"), not as a mechanism ("tortuosity protects"). State the outcome level (stenosis, prevalent CAD, progression, ACS) and do not merge them into "disease". Flag cross-sectional designs in the design column so that "predicts" never appears for a cross-sectional association. The project memory "skeptical thesis claims" and Rampidis's mixed-unit "n" column point the same way.

### Gaps
- I found no published coronary-geometry review with explicit design-feature tick columns, so the check/cross layout is adapted from evidence-gap-map logic, not copied from a domain example.

## 4. Size, orientation, ordering, footnotes and how the text refers to the table

### Takeaway
For a 3-page review with one table, aim for 6–8 rows and 4 text columns plus 3–4 narrow symbol columns. That fits portrait with `tabularx` at `\footnotesize`. Order the rows by strand/design toward the thesis design, with the conflicting rows adjacent. Let the text state the pattern the table shows and never re-list the cells.

### Cited Findings
- Writing-centre guidance: a citation column plus three or four theme columns; more columns become clerical work — [synthesis matrix guides via search: UNC](https://writingcenter.unc.edu/2022/03/synthesis-matrix), [Stanford](https://teachingwriting.stanford.edu/synthesis-matrix)
- Order the rows as the synthesis is reported — [SWiM item 7](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7190266/fullTextXML); order by the PICO element or comparison that serves the purpose — [Cochrane 9.3.2–9.3.3](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-09)
- Tables are for scanning patterns and preferred over long description — [Cochrane 9.3.5](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-09)
- Domain example: 12 rows × 4 columns plus one abbreviation footnote fits one journal page — [Rampidis 2022](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9497479/fullTextXML); the Xing thesis table with 5 columns of bullet cells needed two pages — [Xing 2019](https://repub.eur.nl/pub/117214/Thesis_XING_Final_All.pdf)

### Inferences
- Portrait is better in a 3-page review: a landscape page breaks the reading flow and eats a full page. With `\footnotesize`, four `X` columns and four ✓/✗ columns about 0.5 cm wide fit a DTU A4 text width. Keep each text cell to 1–2 lines. Use landscape only if the page budget allows a full page and the rows exceed ~8.
- Group rows under bold strand sub-headers (or `\midrule` separators) that follow the section's argument: (a) cross-sectional geometry ↔ prevalent disease, (b) follow-up of existing disease or events, (c) plaque-free or population cohorts without geometry, (d) this thesis. Inside (a), put Li 2011 and Tello Ayala 2026 next to each other so that the opposite directions sit side by side. Order chronologically only within a strand.
- Put in the footnote all abbreviations, the definition of +/−/0, the definition of each ✓ column (e.g. "Plaque-free: geometry measured on a scan without plaque"), and "n = persons" (state the unit when it differs, e.g. "39 trees").
- Let the text name the pattern and the exception, not the cells. For example: "Table~\ref{tab:literature} shows that the studies with geometry measured it after disease was present, while the two cohorts with the design to answer the question measured no geometry." The direction conflict gets one sentence with both citations. The current caption carries the gap claim; move it into the text, because the columns now show it.
- Two wording points in the current table, against the project rules: the caption uses "new plaque" (the rules require "incident coronary plaque", or "developed plaque" for people), and "highlighting the cohort…" is a filler lead-in.

### Gaps
- No source gives a hard row limit for a page; the 6–8 figure is a layout estimate for A4 at `\footnotesize`.

## 5. Recommended column set and row-selection logic for this thesis

### Takeaway
Use a combined descriptive + gap-map table: four short text columns (study, population & design, geometry as measured, outcome & direction) and four narrow ✓/✗ design columns that spell out the thesis question. Use 7–8 rows grouped by strand, with the conflicting tortuosity studies adjacent and a final "This thesis" row.

### Cited Findings
- The columns take their content from the CHARMS domains: source of data/design, participants/setting, predictor definition and timing, outcome, adjustment/model — [CHARMS](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1001744)
- Gap visibility comes from the evidence-gap-map logic (empty cells = gaps) — [Snilstveit et al. 2013](https://documents1.worldbank.org/curated/en/212651468163487838/pdf/WPS6725.pdf)
- The direction column and its stated metric limitation follow SWiM items 3, 7 and 9 — [SWiM](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7190266/fullTextXML)
- Row ordering by the synthesis, not by year — [SWiM item 7](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7190266/fullTextXML); [Cochrane 9.3.2](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-09)

### Inferences

**Recommended columns (portrait, `tabularx`, `\footnotesize`, booktabs):**

| # | Column | What goes in it (fill rule) |
|---|---|---|
| 1 | Study | First author (year) + citation. Nothing else. |
| 2 | Population & design | n with its unit (persons unless stated); setting coded as *referred*, *consecutive invasive angiography*, *case–control in registry*, *random population*; design coded as *cross-sectional*, *longitudinal (interval)*. |
| 3 | Geometry as measured | Measure as the study defines it + modality + scope/method, e.g. "bend count, invasive angiography, main arteries, manual"; "turning-angle profile, CCTA, RCA, automated"; "—" if none measured. |
| 4 | Outcome and direction | Outcome level (stenosis / prevalent CAD / progression / ACS / incident plaque) and timing, then the sign: "Prevalent CAD; −". Use "discr." for classifier/profile results and "n/a" when there is no geometry test. |
| 5 | PF | ✓ if geometry (or the baseline scan) was taken when no plaque was present. |
| 6 | Pop | ✓ if the sample is random from the general population. |
| 7 | FU | ✓ if followed to incident coronary plaque on a repeat scan (✗ for events within weeks, or progression of existing disease). |
| 8 | Adj | ✓ if the geometry association was adjusted for conventional risk factors. |

If only seven columns are allowed, merge 5–8 into one "Design (PF/Pop/FU/Adj)" column with four symbols, e.g. "✗ ✗ ✗ ✓", and define the order in the header. The four separate columns read better, because a vertical column of ✗ is the gap seen at a glance.

**Footnote:** abbreviations; "+ higher value of the measure with more disease, − with less, 0 no association, discr. discriminates without a single direction"; definitions of PF/Pop/FU/Adj; "n = persons unless stated".

**Row-selection logic (7–8 rows, grouped):**
- *Strand A: geometry vs prevalent disease (cross-sectional).* Zhang 2024 (whole-tree curvature, 39 trees; discr.), Li 2011 (bend count, 1,010; −), Tello Ayala 2026 (RCA turning-angle profile, 22,334 referred; +, profile discr.). Li and Tello Ayala adjacent: same construct, opposite direction, different measure and modality. That is the inconsistency, shown in columns 3–4.
- *Strand B: geometry with follow-up, but of existing disease or events.* Han 2022 (ACS within weeks; FU ✗), Tommasino 2024 (LM bifurcation angle → proximal LAD progression at 1 year in referred patients; the only bifurcation-angle row) and/or Sakellarios 2017 (bifurcation WSS → lumen reduction). Keep one of the last two if space is short; Tommasino is closer to the thesis's LM-angle feature.
- *Strand C: the right design without geometry.* Won 2022/PARADIGM (plaque-free referred, repeat CCTA; PF ✓, FU ✓, geometry "—"), Bergström 2021/SCAPIS (random population, single scan; Pop ✓, FU ✗, geometry "—").
- *Final row: This thesis* (CGPS Herlev–Østerbro, random population, plaque-free baseline, ~10-year repeat CCTA, curvature/taper/LM angle/diameter ratios from the in-house tracer, adjusted for SCORE2 factors; all ✓; direction "—"). It closes the gap visibly. Present it as design only.
- *Inclusion rule, stated once in the text:* a study is a row if it either measured coronary geometry against coronary disease or has a design element the thesis needs (plaque-free baseline, random population, repeat scan). Pure CFD/WSS studies stay in the text of the earlier sections, since they test mechanism, not association in people.

**Cell-filling consistency checks:** check every direction sign against the paper's own wording (Cochrane 9.4). Use the outcome level the paper used. Write "predicts" only for longitudinal designs. Give the population unit explicitly. Copy the measure's name from the paper, not a harmonised name, because the different definitions are themselves part of the inconsistency the table should show.

### Gaps
- The ✓/✗ entries for Sakellarios 2017 and Tommasino 2024 (risk-factor adjustment in particular) and the exact sign for Zhang 2024 and Han 2022 must be checked against the full texts; they are not filled here, so that no values are invented. The chapter notes (`00_chapter_intro.tex`) say the full texts of Zhang, Li, Tello Ayala, Han, Won, Bergström, Tommasino and Cui were read, so the check can be done from those.
