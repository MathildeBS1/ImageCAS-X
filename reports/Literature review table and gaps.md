# Rebuild the review around a gap-map table

The Literature Review should be cut and refocused rather than extended. In a test compile of `Thesis_coronary/` it runs to **four physical pages**: three full pages of prose (about 1,260 words) and a four-row table that floats onto a page of its own. It also covers only two of the thesis's five features in any depth (curvature and the LM bifurcation angle). Lumen taper and the LM→LAD and LM→LCx diameter ratios get no clinical evidence at all, and the review never asks what "beyond SCORE2" can realistically mean. The fix has four parts. First, cut the material that no longer serves the fixed question: Griffo 2026, Sakellarios 2017, the Bransby segmentation paragraph and the filler openers. Second, give each feature one sentence of evidence that names its inconsistency. Third, add the two near misses an examiner is likely to name, Chen 2024 and Lee 2024. Fourth, replace the descriptive table with a **nine-row table that adds four narrow design columns** (plaque-free baseline, random population, follow-up to incident plaque, adjustment). The gap then shows as columns that are never ticked together, and the caption no longer has to state it. A prototype of that table, compiled in the thesis class, takes about **65% of one page**. That leaves room for roughly **1,000 words of prose** inside a three-page limit. The evidence base under all of this is thin: every geometry–plaque study in humans is cross-sectional or starts from a diseased baseline, most are in referred patients, and several key sources were read only as abstracts. One of them (Tommasino 2024) has statistics that do not reproduce. The text must therefore report what each study found and say nothing beyond that.

## Four pages, two of five features, and a gap stated only in the caption

The chapter files (`00_chapter_intro.tex` to `03_geometry_risk.tex`) were compiled alone with the thesis preamble. The prose fills chapter pages 1 to 3 (399, 449 and 433 words) and the table lands on page 4. At the thesis's 130 mm text width, a full page holds about 450 words, so a three-page chapter including a table has room for about 1,000 words of prose. The table's own size decides the rest.

Measured against the fixed question, the content has drifted. Section 1 ends on Griffo 2026, a graph network that estimates WSS. Its closing synthesis says shape "carries enough of the flow information to replace its simulation", which overstates what it cites: Kashyap found the curvature–low-WSS relation "significant although weak", and Griffo identified culprits only "moderately". The thesis never estimates WSS, so Griffo no longer earns its 80 words. Section 2 opens with a motivation sentence ("Using coronary geometry as a marker relies on…"), which the no-filler rule forbids. It closes with the Bransby benchmark, which is an arXiv preprint (`refs.bib`: arXiv:2608.30404). It is also misworded: "The best method came close … but ultimately concluded". The geometry now comes from the in-house tracer, so that paragraph argues for something the thesis no longer does.

Section 3 has two errors that matter. It writes "new plaque" twice, plus once in the caption. It also says Won et al. related plaque progression "to age, sex, hypertension, diabetes, hyperlipidemia, obesity, smoking and HbA1c". In fact the conventional factors were *not* significantly associated with rapid progression; only HbA1c *measured at follow-up* was ([Won 2022, PubMed 36371222](https://pubmed.ncbi.nlm.nih.gov/36371222/)). Won's development of plaque (35.6% over a median 3.6 years) was reported descriptively, not modelled. The gap sentence opens with "Despite these advancements, a significant gap remains", another filler. It also frames the gap as "automated measurement of the whole coronary tree", which is not what the thesis now tests: it tests five named features of three arteries and the LM.

The table is the weakest part. Its four rows (Zhang, Li, Tello Ayala, Han) are all cross-sectional or events-within-weeks, and nothing in its columns marks what is missing. Published examples share this weakness. The one thesis table that could be checked uses five descriptive columns with no gap or design columns: Xing's Erasmus PhD thesis on WSS and plaque progression has *Model | Flow and shear profile | Vessel pathology | Species | Remarks* ([Xing 2019](https://repub.eur.nl/pub/117214/Thesis_XING_Final_All.pdf)). The closest review in the field has four columns, *Parameter | Outcome | Modality | Number of patients*. Its finding cells are direction phrases that hide the conflicts its own text reports, such as the LM angle disagreement and tortuosity holding "only at the per-segment level" ([Rampidis 2022](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9497479/fullTextXML)). The search aimed for three to six thesis tables to compare. **Only one was found**: the DTU, DiVA, TU Delft, Aarhus and Imperial repositories gave nothing extractable. The design below therefore rests mainly on the reporting frameworks, not on thesis precedent.

## Each feature's sign depends on definition, endpoint and referral

The review should name the inconsistency feature by feature in one sentence each. These are the facts it can safely use.

**Curvature and tortuosity.** The sign flips with the definition. Li 2011 counted bends of 45° or more on invasive angiograms and found tortuosity inversely associated with CAD (OR 0.755, 0.574–0.994). In the same data, female sex had an OR of 2.603 for tortuosity ([Li 2011](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0024232)). Tello Ayala 2026 is the strongest evidence that definition alone flips the sign. In **22,334 referred patients**, an automated mean turning angle of the RCA was *positively* associated with stenosis (OR 1.05 per SD), while the classic arc/chord index was weakly *inverse* (β −0.03). The two measures correlated at only r = 0.116 ([Tello Ayala 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)). Tello Ayala used 2D invasive angiography, not CCTA. One of the research notes (`table_design.md`) wrongly says CCTA. The CAD label also came from the same angiogram, read by the same operator.

Referral is a plausible driver of the inverse results. Tortuosity is framed as a mechanism of ischaemia *without* obstructive disease ([Zebic Mihic 2024](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10795752/)), so chest-pain referral can enrich cohorts for tortuous arteries without plaque. That is an inference, and the text must present it as one. The WSS literature points both ways as well. Average curvature was the measure most related to low TAWSS, while arc/chord was unrelated (p = 0.86) ([Kashyap 2022](https://doi.org/10.1038/s41598-022-04796-w)). Patient-specific CFD found that tortuosity *raises* WSS through helical flow ([Vorobtsova 2016](https://repub.eur.nl/pub/91183), abstract only).

**LM bifurcation angle.** In referred CCTA cohorts, a wider LAD–LCx angle accompanies left stenosis. Cui 2017 found it independently predictive (per 10°, OR 1.423, 1.140–1.777) in 106 patients, while the two LM–daughter angles did not differ. The angle also differed between systole and diastole (73.6° vs 78.4°), and the relation was not monotonic across stenosis grades (`knowledge/docs_thesis/papers/cui2017bifurcation.md`; [Cui 2017](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0174352)). Juan 2017 found the angle wider with stenosis in univariable analysis but **not after adjustment (P = 0.064)** ([Juan 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5431433/)). In 300 normal arteries with zero calcium, the angle was wider in men (85° vs 74°) and with a ramus (89° vs 75°). Sex therefore confounds diseased-vs-normal comparisons ([Medrano-Gracia 2016](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)).

**Diameter ratios.** The reference law itself is unsettled. A meta-analysis pooled the flow–diameter exponent at 2.39 (2.24–2.54), with I² = 99%, rather than Murray's 3 ([Taylor 2024](https://pubmed.ncbi.nlm.nih.gov/38787386/), abstract only). Deviation from Murray's law went with more dense calcium at bifurcations on IVUS, after adjustment for risk factors, cross-sectionally ([Schoenenberger 2012](https://www.ncbi.nlm.nih.gov/pubmed/22261173), abstract only). In synthetic trees, an unequal LAD/LCx diameter division amplified the angle and bending effects on adverse haemodynamics ([Garcha 2025](https://doi.org/10.1038/s41598-025-85781-x)).

**Taper.** No clinical study was found in which lumen taper on a plaque-free vessel predicts later plaque. On IVUS, taper partly *results from* differential plaque accumulation ([Javier 1995](https://doi.org/10.1016/s0002-9149(00)80072-7), abstract only). Positive remodelling preserves the lumen until plaque reaches about 40% of the IEL area ([Glagov 1987](https://doi.org/10.1056/NEJM198705283162204)). Both are reasons why taper can be read as a predictor only on a plaque-free scan.

Across the features, the disagreement comes from six sources: modality (2D projection vs 3D), visual vs automated measurement, the feature's definition, single artery vs tree, the endpoint (stenosis, any plaque, calcium, ACS) and referral. All the human studies are cross-sectional or start from a diseased baseline.

## The nearest studies are referred, short and radiomic

The gap holds, but two near misses must now be named, or an examiner will name them. **Chen 2024** measured centreline metrics, including curvature, and cross-section radiomics in a plaque-free LAD proximal to a myocardial bridge. The sample was 192 referred patients plus 103 external, with plaque developing in 27.1% over a median of 3.0 years. The radiomic models discriminated moderately (external AUC 0.75). The paper itself is inconsistent: the combined external AUC is 0.76 in the Results and 0.75 in the abstract ([Chen 2024](https://academic.oup.com/ehjcimaging/article/25/10/1462/7680519), full text). **Lee 2024** followed 9,583 plaque-free *segments* in 1,162 PARADIGM patients, with scans at least two years apart. Radiomic texture added to clinical risk factors raised the C-index to 0.767 in the test set, against about 0.70 for clinical factors alone ([Lee 2024, PubMed 38378314](https://pubmed.ncbi.nlm.nih.gov/38378314/), abstract only). These patients could have plaque elsewhere, and whether the split was by person cannot be checked from the abstract.

Neither study uses a population sample, a prespecified interpretable geometry block or a ten-year interval. The stricter gap therefore holds: **no study found has related named geometric features measured in plaque-free persons to later plaque, in any cohort type**. Other studies fall further away. Han 2022 is a nested case-control study with a median of 29 days from scan to ACS ([Han 2022](https://jamanetwork.com/journals/jamacardiology/fullarticle/2788006)). Tommasino 2024 followed a diseased cohort for one year, with re-imaging triggered by clinicians ([PMC11595042](https://pmc.ncbi.nlm.nih.gov/articles/PMC11595042/)). CArTI is a conference abstract with a MACE endpoint ([AHA 2025](https://www.ahajournals.org/doi/10.1161/circ.152.suppl_3.4365988)). The one real competitor is still to come: the SCAPIS re-examination has rescanned about 15,000 randomly sampled participants a median of 8.1 years after baseline, but has published only its design ([Good 2026, PubMed 41558989](https://pubmed.ncbi.nlm.nih.gov/41558989/)). No CGPS publication on serial CCTA or geometry was found ([PubMed search](https://pubmed.ncbi.nlm.nih.gov/?term=%22Copenhagen+General+Population+Study%22+coronary+computed+tomography+angiography&sort=date&size=50)). Both should be re-checked before submission.

The review is also silent on "beyond SCORE2", which the question requires. One sentence would calibrate it. Across five pooled cohorts with event endpoints, even the strongest imaging marker, the CAC percentile, raised SCORE2's C by only about 0.02 ([Hageman 2023, PubMed 37264679](https://pubmed.ncbi.nlm.nih.gov/37264679/)). No study was found that adds any imaging marker to SCORE2 to predict *incident plaque*. The testing logic (test the coefficient block once; estimate ΔC and calibration without testing them) comes from Pepe 2013 and Pepe 2014 ([PubMed 23296397](https://pubmed.ncbi.nlm.nih.gov/23296397/); [PubMed 24681599](https://pubmed.ncbi.nlm.nih.gov/24681599/)). That belongs in the Methodology, not the review.

## A gap-map table: four text columns and four design ticks

No framework prescribes a layout, but together they say what the columns must carry and how the rows should run. PRISMA 2020 asks for each study's characteristics and results "ideally using structured tables" ([PRISMA 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8005924/)). The Cochrane Handbook prefers tables to long description, asks for characteristics coded into pre-specified categories, and says to order rows by the comparison the review argues ([Cochrane ch. 9](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-09)). SWiM accepts "vote counting based on direction of effect" and asks that tables follow the order of the synthesis ([SWiM](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7190266/fullTextXML)). CHARMS supplies the domains that carry this gap. Its most decisive item asks whether predictors were "available at the intended time of use", and geometry measured after plaque fails it ([CHARMS](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1001744)). Evidence-gap maps make empty cells the gaps ([Snilstveit 2013](https://documents1.worldbank.org/curated/en/212651468163487838/pdf/WPS6725.pdf)). Writing-centre synthesis matrices warn that more than a citation column plus three or four theme columns turns into clerical work ([UNC](https://writingcenter.unc.edu/2022/03/synthesis-matrix)).

The design follows from these. It has four short text columns (Study, Sample, Geometry, Outcome with direction) and four ✓/✗ columns taken from the question (PF, Pop, FU, Adj). Rows are grouped by strand, separated by `\midrule`, and ordered as the text argues, with Li and Tello Ayala adjacent so that their opposite signs sit side by side. The research notes propose a final "This thesis" row. **Drop it**: the house rules forbid comparing the review with the thesis's own work and forbid forward references. The gap should show from the other side instead: the rows with geometry never tick PF and FU together, and the rows that do tick them measured no geometry or no named geometry. Each measure keeps its own published name, because the differences in definition are part of what the table shows.

## Revision plan

### (a) Studies to keep, add or cut, per section (prose target in brackets)

| Section | Keep | Add | Cut | Reason |
|---|---|---|---|---|
| §1 Geometry and WSS (≈280 words) | Asakura 1990; van der Giessen 2009; Kashyap 2022; Zhang 2024; Garcha 2025 | Optional: Vorobtsova 2016, one clause (tortuosity raises WSS), only after reading the full text | Griffo 2026; the "replace its simulation" synthesis | The thesis does not estimate WSS. Garcha is the only study joining the angle, bending and diameter ratio. The new closing synthesis should claim only that shape determines where WSS is low, with the strength qualified as Kashyap reports it |
| §2 Quantifying geometry (≈330 words) | Cui 2017 (add its systole/diastole difference); Li 2011; Tello Ayala 2026 (add its own inverse arc/chord result and the shared-image label) | Juan 2017 (clause: not significant after adjustment); Medrano-Gracia 2016 (sex and ramus widen the angle); Taylor 2024 and Schoenenberger 2012 (one sentence on diameter ratios); one taper sentence (Javier 1995 after verification, or a cited absence) | Opener filler sentence; Groves 2009 (abstract only, duplicates Li); the Bransby paragraph; "this must be extended" | Every feature the model uses needs one cited sentence naming its inconsistency. The sex confounding links directly to the SCORE2 base |
| §3 Geometry and risk (≈390 words) | Glagov 1987 premise; Han 2022; Tommasino 2024 (rephrase caveat); Won 2022 (correct it); Bergström 2021 | Chen 2024 and Lee 2024 (one sentence each); Good 2026 (one clause: re-examination reported design only); Hageman 2023 (one sentence: imaging adds little to SCORE2 even for events) | Sakellarios 2017 (tiny, existing disease, its "best" not a formal test); "Despite these advancements"; "new plaque" ×2 | The near misses make the gap claim defensible. Hageman places "beyond SCORE2" in context without numbers in the prose |
| §0 chapter file | heading | update the header comment (cited keys, abstract-only list, owed sources) | outdated Bekircavusoglu, Givehchi and transformer notes | Keeps the content map in `Thesis_coronary/CLAUDE.md` true at commit |

Each replacement sentence must keep the house rules: author and year as subject with `\cite` after the year, no numbers, no lists, "LCx" (the three "LCX" in §1 and §2 should change; note that `background/heart_anatomy.tex` also uses LCX), and outcome wording such as "a substantial share developed plaque". Three corrections are load-bearing. The first is for Won, for example: *Won et al.\ (2022) \cite{won2022paradigm} rescanned registry patients without plaque on a first CCTA, reported that a substantial share developed plaque, and found rapid progression associated only with HbA1c measured at follow-up, without measuring geometry.* The second is for Tommasino: *their confidence intervals and p-values do not reproduce from their own regression table* (not "intervals cannot be reproduced", and not "effect sizes", since the point estimate does reproduce). The third is the gap: *No study identified in this search measured coronary geometry on a plaque-free scan in a random sample of the population and followed it to incident coronary plaque.* The search-statement TODO (databases, window, date, inclusion criterion) is still owed, and its dates need an explicit exception to the no-numbers rule or a footnote.

### (b) Final table design and filled cells

The columns are Study | Sample | Geometry | Outcome (with direction) | PF | Pop | FU | Adj, in `tabularx`, `\footnotesize`, booktabs, portrait. The prototype below compiles in the thesis class without overfull boxes and takes about 65% of a page.

```latex
\begin{table}[h]
  \centering
  \footnotesize
  \setlength{\tabcolsep}{2.5pt}
  \newcommand{\y}{\checkmark}\newcommand{\n}{$\times$}\newcommand{\p}{$\circ$}
  \begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{0.15\linewidth}%
      >{\raggedright\arraybackslash}X >{\raggedright\arraybackslash}X >{\raggedright\arraybackslash}X%
      *{4}{>{\centering\arraybackslash}p{0.045\linewidth}}@{}}
    \toprule
    Study & Sample & Geometry & Outcome & PF & Pop & FU & Adj \\
    \midrule
    Li (2011) \cite{li2011tortuosity} & 1,010 chest pain, ICA & Bend count, visual & CAD $-$ & \n & \n & \n & \y \\
    Tello Ayala (2026) \cite{telloayala2026tortuosity} & 22,334 referred, ICA & RCA turning angle; arc/chord & Stenosis $+$; $-$ & \n & \n & \n & \y \\
    Cui (2017) \cite{cui2017bifurcation} & 106 referred, CCTA & Three LM angles, manual & Stenosis $+$ LAD--LCx, $0$ LM & \n & \n & \n & \y \\
    \midrule
    Han (2022) \cite{han2022plaque} & 116 ACS, 116 controls & Lesion site and bends & ACS within weeks $+$ & \n & \n & \n & \y\textsuperscript{b} \\
    Tommasino (2024) \cite{tommasino2024clap} & 499 referred, one year & LM angle, manual & LAD progression $+$\textsuperscript{a} & \n & \n & \n & \y \\
    \midrule
    Chen (2024) & 192 referred with LAD bridge, 3 years & Centreline radiomics & Incident plaque, discr. & \p & \n & \y & ? \\
    Lee (2024) & 1,162 referred (9,583 segments), $\geq$2 years & Radiomic texture & Incident plaque, discr. & \p & \n & \y & \y \\
    Won (2022) \cite{won2022paradigm} & 402 referred, plaque-free, 3.6 years & None & Rapid progression & \y & \n & \y & -- \\
    Bergstr\"om (2021) \cite{bergstrom2021scapis} & 25,182 random sample, one scan & None & Prevalent plaque & \n & \y & \n & -- \\
    \bottomrule
  \end{tabularx}
  \caption{Studies relating coronary geometry to coronary disease, and cohorts with the design to
    do so. PF: geometry measured, or baseline scanned, without plaque ($\circ$ in one segment or
    artery only). Pop: random sample of the general population. FU: repeat scan to incident
    coronary plaque. Adj: adjusted for conventional risk factors. $+$/$-$/$0$: larger value with
    more, less or no difference in disease; discr.: classifier without one direction. Sample:
    persons unless stated. \textsuperscript{a}Confidence intervals and p-values do not reproduce
    from the reported coefficients. \textsuperscript{b}Controls matched on risk factors; geometry
    adjusted for plaque features. ACS: acute coronary syndrome; ICA: invasive coronary
    angiography; LAD: left anterior descending; LCx: left circumflex; LM: left main; RCA: right
    coronary artery.}
  \label{tab:literature}
\end{table}
```

Before the table goes in, check each cell against its source, as Cochrane 9.4 asks for direction and significance. Chen 2024 and Lee 2024 need new `refs.bib` entries (doi 10.1093/ehjci/jeae135; doi 10.1016/j.jcct.2024.02.003), as do Good 2026, Hageman 2023 and Javier 1995 if they are used.

| Row | Verified cells | Unverified or flagged cells |
|---|---|---|
| Li 2011 | Sample, geometry, sign (full text) | **Adj ✓ unverified**: confirm that OR 0.755 comes from the multivariable model |
| Tello Ayala 2026 | All, including adjustment set (age, sex, hypertension, T2D, hypercholesterolaemia, smoking) | None. The caption could add that the label comes from the same angiogram |
| Cui 2017 | All (local full-text note). The multivariable model includes diameter stenosis and lipid plaque volume | "0 LM" is a group comparison, not the multivariable model |
| Han 2022 | Sample, timing, sign | **Adj ✓ is by matching plus plaque adjustment**, hence footnote b. Check that this coding is acceptable |
| Tommasino 2024 | Sample, angle definition, one-year interval | Direction stands, but statistics are irreproducible (footnote a). **Adj ✓ inferred** from "multivariable" |
| Chen 2024 | Sample, interval, outcome, PF ◦ (full text) | **Adj "?"**: radiomics-model covariates not stated |
| Lee 2024 | Plaque-free segments, 1,162 patients, ≥2 years (abstract) | **Whole row abstract-level**. Some C-index values are from a search snippet; person-level split unverified |
| Won 2022 | All (local full-text note) | None |
| Bergström 2021 | All (local full-text note) | None |
| Schoenenberger 2012 (held back) | Direction and adjustment (abstract) | **n unknown**, abstract only. Add as a tenth row only if the full text is read and the page budget allows |

Zhang 2024 leaves the table (39 trees, CFD, stenosis-defined) but stays in §1.

### (c) Evidence caveats

| Caveat | Sources affected | What to do |
|---|---|---|
| Abstract-only | Asakura 1990, Glagov 1987, Groves 2009, Schoenenberger 2012, Taylor 2024, Javier 1995, Vorobtsova 2016, Lee 2024, Hageman 2023, Good 2026 (design paper); Kashyap R² values not extracted | Cite direction only, no mechanism claims; read the full text before adding numbers to the table |
| Preprints and conference abstracts | Bransby 2026 (arXiv), Gharleghi 2024 (arXiv), CArTI (AHA abstract), Leng/APOLLO (EHJ abstract) | Do not use as table rows. Cutting Bransby removes the only preprint from the prose |
| Tommasino inconsistencies | From Table 2's B 1.499 and SE 0.206, the 95% CI is 2.99–6.71, not the reported 3.80–6.70. CKD p ≈ 0.20 (reported 0.041) and diabetes p ≈ 0.0001 (reported 0.031). Table labelled logistic Exp(B) while the text says Cox HR. Denominators 160/499 vs 204/288 do not reconcile. Re-imaging was "when clinically indicated", a verification bias. 85 patients with a ramus were excluded. The 80° cut-off was derived on the same data ([PMC11595042](https://pmc.ncbi.nlm.nih.gov/articles/PMC11595042/)) | Report the direction only, with footnote a. Never quote the HR |
| Rodriguez-Granillo 2016 | Not located. The 2016 IJCI LM-angle paper in the bib is Temov & Sun (doi 10.1007/s10554-016-0884-2); Rodriguez-Granillo's located paper is from 2007 (IJCI 23:389, n = 50) | Do not cite "Rodriguez-Granillo 2016". Use temov2016bifurcation or the 2007 paper |
| Bekircavusoglu 2026 | Today's search did not find it, but `thesis/refs.bib` records it as checked (Clin Radiol 96:107299, doi 10.1016/j.crad.2026.107299, PMID 41962318, abstract only). Zhang 2023 found the ramus association did not survive propensity matching ([PMC10091592](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10091592/)) | Leave it out. The ramus is not a model feature, and the citation conflict is unresolved |
| Author overlap with the excluded review | Zhang 2024 and Gharleghi 2024 share authors with shen2026geometry (Zhang M, Gharleghi R, Shen C, Beier S). Some notes link Garcha 2025's DOI to arXiv 2507.17109, which is shen2026geometry's preprint | Confirm with the author that Zhang 2024 may stay. Check every Garcha claim against the Sci Rep paper itself |
| Errors inside the notes | `table_design.md` calls Tello Ayala CCTA (it is 2D angiography). Juan 2017 group labels differ between the abstract and PMC. Chen 2024 gives AUC 0.76 vs 0.75 | Copy cells from the papers, not the notes |
| Strength of the absence claim | Searches were budget-limited. MESA, Miami Heart, DISCHARGE and Rotterdam were not searched one by one, and CGPS conference abstracts were not searched | Keep "identified in this search". Re-check SCAPIS re-examination and CGPS output before submission |
| Population vs referred rates | PARADIGM's 35.6% developing plaque comes from referred patients | Never present it as a population rate |

## Conclusion

The review does not need more literature. Its existing literature needs to sit in a structure where the absence is visible. Most of the gain comes from columns, not prose. Once PF, Pop and FU are columns, the gap no longer has to be asserted: the rows with geometry never combine a plaque-free baseline with follow-up, and the rows with that design measured no named geometry. The prose can then spend its roughly 1,000 words on what a table cannot show: why the signs flip (definition, endpoint, sex and referral), and why each of the five features can be read as a predictor only on a plaque-free scan.

The new framing also exposes a risk. The gap is "no study identified in this search", and the two closest competitors are moving. SCAPIS has rescanned a random population and will publish, and a CGPS paper on progression from risk factors alone is plausible. A short, dated search statement and a final re-check before submission protect the claim better than any rewording.
