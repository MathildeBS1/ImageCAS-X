# Why lumen taper, rather than other candidate geometric features, is the added feature (and how to argue for an untested feature in a literature review)

Scope and honesty notes:
- This note extends `reports/Fourth centerline feature for plaque.md` and the three notes in `research_notes/Fourth centerline feature for plaque/`. Findings already given there (Alamir U-net attribution, Johnston 2007, Gijsen 2019, PREDICTION, Malvè 2020, De Nisco 2019/2020/2021, Vorobtsova 2016, Li 2018/2022, Nannini 2024, Cademartiri) are only referred to here, not repeated.
- **Correction to the earlier report.** It quotes "diameter and its variation ... have yet to be studied in detail" from Shen et al. 2025, arXiv 2507.17109. That source is excluded from this thesis, so the quote must be dropped from any thesis text. The gap claim has to rest on the absence of studies (see Q1 Gaps) and on primary sources.
- Preprints are flagged where they come up: Shen et al. arXiv 2502.06161 (preprint only). Gharleghi et al. arXiv 2401.12504 has since been published as Sci Rep 2025;15:254 (per the earlier note `predictive_evidence_ranking.md`; this session did not check the journal version), so cite the journal version.
- This session made about 15 tool calls. Several pages (PubMed, some publisher sites) returned only abstracts or blocked pages, and the access level is given for each source. "Snippet" means only a search-engine summary was seen; treat those claims as unverified until the PDF is read.

## Q1. For each alternative: evidence for a WSS or plaque link, measurement error on CCTA, overlap with curvature/angle/ratio, and which were null in humans

### Takeaway
None of the alternatives beats taper on all three criteria at once: a mechanistic WSS link, measurability on a plaque-free CCTA, and low overlap with curvature, the LM bifurcation angle and the LM→LAD/LCx ratios. Torsion was null in the only human test, and the tortuosity index was null against low WSS in 127 human LM bifurcations. Distance from the ostium is already absorbed by the segment intercepts. LM length exists only for the left tree. Lumen volume to myocardial mass and raw diameter are calibre measures confounded by body size and sex. Eccentricity has no human WSS-outcome evidence found. Radiomic texture of a plaque-free wall has no mechanistic WSS link. Taper's own weakness is that **no study has tested it against WSS or plaque in humans**, so its case is mechanistic and comes from elimination, not empirical.

### Cited Findings

**Torsion (and helicity, which is a flow quantity and not geometry)**
- Human CFD on 39 ASOCA left trees (20 non-stenosed): mean curvature was the only geometric parameter that differed between stenosed and non-stenosed trees; mean torsion did not. Torsion came from raw VMTK centerlines with no smoothing described. Open access. DOI 10.1098/rsos.241267 — [Zhang et al. 2024, R Soc Open Sci](https://doi.org/10.1098/rsos.241267) (details from the earlier note `torsion_tortuosity_helicity.md`; not re-read this session).
- Torsion correlated with helical-flow intensity (r = 0.64) in **swine**, and helicity was inversely related to adverse WSS (r = −0.91). Abstract only. DOI 10.1007/s10439-018-02169-x — [De Nisco et al. 2019, Ann Biomed Eng (abstract, EUR repository)](https://repub.eur.nl/pub/112774).
- Helicity indices need CFD velocity fields, so they are not a geometric feature the tracer can provide (see `torsion_tortuosity_helicity.md`, Q3).

**Tortuosity index (path length / chord length)**
- In 127 CTCA LM bifurcations **without CAD**, the tortuosity index "showed no significant correlation with low TAWSS (p = 0.86)", whereas curvature-based measures did; average absolute curvature had the highest R² and is recommended. Open access. DOI 10.1038/s41598-022-04796-w — [Kashyap et al. 2022, Sci Rep (DOAJ record)](https://doaj.org/article/3670df7ece6f492a85e2ecc0fe144fb7); [Nature PDF](https://www.nature.com/articles/s41598-022-04796-w.pdf). Exact R² values were not retrieved this session.
- Clinical "tortuosity paradox": angiographic and CCTA bend-count tortuosity associates with *less* stenosis/calcium in several cohorts and with more in others (sources in `torsion_tortuosity_helicity.md`, Q2).

**Raw lumen diameter / vessel size**
- Normal angiograms (83 selected from 9,160): women's epicardial diameters were 9% smaller than men's (p < 0.001) "even after normalization for body surface area" (p < 0.01). RCA proximal diameter varied with dominance (3.9 ± 0.6 vs 2.8 ± 0.5 mm), LAD diameter did not. Diameter rose with LV hypertrophy (+17%) and dilated cardiomyopathy (+12%) in men, and was unaffected by age or tortuosity. Abstract only (search snippet). DOI 10.1161/01.CIR.86.1.232 — [Dodge et al. 1992, Circulation](https://doi.org/10.1161/01.CIR.86.1.232) (abstract text seen through [indexing sites](https://scilit.com/publications/4ea6396b1cf44612b116c2fb6b49d4e5)).
- In plaque-free vessels on CCTA, segments under 2.6 mm had more than three times the minimal ESS of segments over 3.2 mm, and men had lower ESS than women after adjustment for diameter. Paywalled (from the earlier report). DOI 10.1007/s10554-022-02739-0 — [Schultz et al. 2023, Int J Cardiovasc Imaging](https://doi.org/10.1007/s10554-022-02739-0).
- In the zero-calcium CT atlas, LM diameter differed by sex (ANOVA p < 0.001), but diameters were "not significantly related to BMI-based size". Open access. DOI 10.4244/EIJV12I7A139 — [Medrano-Gracia et al. 2016, EuroIntervention](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy). This conflicts in part with Dodge (BSA-normalised sex gap), so how much of the sex gap is body size is not settled.

**Left main length**
- Applies only to the LAD and LCx, not to the RCA (structural argument, `radius_topology_features.md` Q3). It also sits next to the LM angle and ratios in the same bifurcation, so overlap is likely (inference).

**Distance from the ostium**
- In 208 STEMI patients, occlusions clustered in the proximal third of the RCA, LAD and LCx; risk fell 13% (RCA), 30% (LAD) and 26% (LCx) per 10 mm from the ostium. Abstract only. DOI 10.1161/01.CIR.0000135468.67850.F4 — [Wang et al. 2004, Circulation](https://hcp.hms.harvard.edu/publication/coronary-artery-spatial-distribution-acute-myocardial-infarction-occlusions). Note that the outcome is acute occlusion in a referral STEMI cohort, not incident plaque in a population sample.
- In the pooled 9-segment GLMM, segment intercepts (proximal/mid/distal × artery) already carry position, so distance from the ostium adds little beyond them (inference about the model design).

**Eccentricity / ovality of the lumen**
- No study was found in this session that isolates lumen eccentricity as a WSS determinant in patient-specific coronary CFD; the search returned only methods papers. — [search summary; e.g. PMC8360211 CTA-vs-IVUS LAD CFD](https://pmc.ncbi.nlm.nih.gov/articles/PMC8360211).
- The CT atlas computed eccentricity only at bifurcations, from an ellipse fitted to the maximal-area cross-section. — [Medrano-Gracia 2016](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy).

**Lumen volume to myocardial mass (V/M)**
- V/M is the ratio of total epicardial lumen volume to LV mass; lower V/M was reported along SAP → UA → AMI in a single-centre retrospective study. Open access. DOI 10.3389/fcvm.2025.1449148 — [Frontiers Cardiovasc Med 2025](https://frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2025.1449148/full).
- A lumen-volume index has been used as a marker of diffuse, flow-limiting atherosclerosis against PET. Open access. — [Coronary artery lumen volume index vs 13N-ammonia PET (PMC8213544)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8213544/).
- No study was found that tests V/M as a predictor of plaque *development* on serial CCTA (search summary). V/M also needs an LV mass segmentation the tracer does not provide.

**Local expansion / Murray deviation**
- Covered in `radius_topology_features.md` (Q1–Q2); the Murray-type quantity overlaps with the LM→LAD/LCx ratios already in the model.

**Radiomic texture**
- I found no study linking radiomic texture of a *plaque-free* coronary wall or lumen to WSS. Radiomics on CCTA has been developed for characterising existing plaque and pericoronary fat (gap; not sourced this session).

### Inferences
- Comparison grid (my synthesis of the findings above and the earlier notes):

| Feature | WSS/plaque link in humans | CCTA measurement risk | Overlap with curvature/angle/ratios | Fits a 9-segment, both-tree model |
|---|---|---|---|---|
| Torsion | Null (Zhang 2024); swine positive | High (third derivative) | Low in theory | Yes |
| Tortuosity index | Null vs low TAWSS (Kashyap 2022) | Low | High (curvature) | Yes |
| Raw diameter | Strong for WSS (Schultz 2023) | Moderate (partial volume) | Moderate (ratios) | Yes, but confounded by sex/body size/dominance |
| LM length | Old direct plaque studies (earlier note) | Low | Moderate (LM angle) | No (no RCA) |
| Distance from ostium | Strong for STEMI location (Wang 2004) | Low | Absorbed by segment intercepts | Redundant |
| Eccentricity | None found | High at 0.4–0.5 mm | Unknown | Yes |
| V/M | Ischaemia/ACS, not plaque development | Needs LV mass | Calibre-type | Person level only |
| Radiomics | None for plaque-free wall | High, scanner-dependent | Unknown | Too many parameters |
| **Relative taper** | **Mechanistic only (Poiseuille + flow loss at branches); untested** | **Moderate (slope over many points)** | **Low; partial with LM ratios proximally** | **Yes** |

- The case for taper is therefore partly by elimination. The thesis should say so plainly rather than claim taper is "proven".

### Gaps
- No primary human study of taper rate against WSS or plaque was found (this session or earlier ones). That cannot prove none exists.
- Kashyap 2022 full R² values, and Dodge 1992 full text (segment tables, BSA analysis), were not read.
- Whether the Zhang 2024 torsion null survives centerline smoothing is unknown.

## Q2. Why a scale-free shape measure (relative taper, log-radius slope) rather than absolute diameter

### Takeaway
Absolute diameter mixes shape with body size, sex, dominance and LV mass. A log-radius slope is unchanged when the whole artery is scaled, so person-level size effects cancel. That isolates the "does the lumen narrow as fast as its flow falls" signal, while SCORE2 already carries sex.

### Cited Findings
- Sex gap persists after BSA normalisation (−9%); dominance changes RCA calibre; LV hypertrophy and dilated cardiomyopathy enlarge arteries. — [Dodge 1992](https://doi.org/10.1161/01.CIR.86.1.232) (abstract only).
- LM diameter differs by sex in a zero-calcium CT population. — [Medrano-Gracia 2016](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy).
- Men had lower ESS than women even after adjustment for diameter. — [Schultz 2023](https://doi.org/10.1007/s10554-022-02739-0) (paywalled; from earlier report).
- Normal arteries taper: the CT atlas reports LAD diameters that "decrease distally in an approximately linear fashion" and, beyond bifurcations, "a smooth reduction of approximately 0.25 mm per 10 mm of length". — [Medrano-Gracia 2016](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy).
- Bifurcation diameters in zero-calcium CT best fit the Huo–Kassab scaling model; sex but not hypertension, smoking or diabetes associated with shape. DOI 10.1007/s12265-016-9720-2 — [Medrano-Gracia et al. 2017, J Cardiovasc Transl Res](https://link.springer.com/10.1007/s12265-016-9720-2) (abstract/snippet level).
- An angiographic study defined tapering indices T1/T2 as percent diameter reduction along a segment and proposed that an expected taper could flag "diseased segments that are not angiographically stenotic"; tapering of up to 14% and 21% in the proximal and distal LAD and 9% in the dominant RCA. — [PubMed 12368932, "Normal angiographic tapering of the coronary arteries"](https://pubmed.ncbi.nlm.nih.gov/12368932/) (**snippet only**: the PubMed page was blocked, so authors, journal and exact numbers are unverified).

### Inferences
- A pure scaling argument: if r(s) = k·f(s), then d ln r / ds = f′/f, independent of k. Body-size and sex effects that act as a multiplicative factor on the whole tree therefore cancel. Effects that change shape (e.g. dominance shifting flow between the RCA and the LCx) do not cancel, so dominance stays a reason to look at taper by artery.
- The angiographic "taper flags non-stenotic disease" idea (PubMed 12368932, unverified) supports the reverse-causation concern already raised in the earlier report: steep taper may be early diffuse disease rather than a low-WSS shape. This argues for a two-sided test.
- Absolute ESS falls with diameter at roughly r⁻³ for a fixed flow, but flow itself scales with vessel size (Huo–Kassab), so absolute diameter is a poor proxy for WSS across people. Within-artery change is what is informative (inference from Poiseuille scaling and the Medrano-Gracia 2017 fit).

### Gaps
- No study was found comparing relative and absolute diameter measures as plaque predictors.
- The Dodge BSA result conflicts with Medrano-Gracia's "not related to BMI-based size"; BMI is not BSA, and neither claim was checked in full text.

## Q3. Is taper measurable on CCTA with adequate reproducibility at ~0.4–0.5 mm voxels?

### Takeaway
Diameter profiles along the centerline are routine in CCTA pipelines: the CT atlas samples every 0.5 mm, and TAG uses a slope along the artery. But **no published scan-rescan or interobserver reproducibility of a geometric taper slope was found**. The expected signal is small (about 0.25 mm per 10 mm, i.e. about half a voxel per 10 mm), so the slope must be fitted over many cross-sections, and reproducibility has to be shown in the thesis's own data.

### Cited Findings
- The atlas computes an effective diameter (from the cross-sectional area, A = πR²) every 0.5 mm along the centerline of a semi-automatic lumen mesh. It reports no ICC or limits of agreement, and calls the method "fully automatic" in the Discussion but "semi-automatic" in the Methods. — [Medrano-Gracia 2016](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy).
- In the atlas, "limitations in resolution" made about 3% of cases unsuitable, mostly smaller female hearts. — same source.
- TAG (the slope of intraluminal attenuation along the artery, an *attenuation* taper, not a geometric one): automated measurement narrowed inter- and intra-observer limits of agreement by 25% and 36% vs manual, in 60 arteries from 20 patients. Open access (abstract seen via snippet). — [Chatzizisis et al. 2014 (PMC4104747)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4104747); manual TAG interobserver r = 0.954 in 28 patients (snippet). — [Accuracy and reproducibility of automated TAG (CiNii record)](https://cir.nii.ac.jp/crid/1361981470147940352).
- Scan-rescan reproducibility of automated lumen/wall segmentation for *plaque volume* is high (ICC ≥ 0.96, 30 people, rescans a median of 6 days apart) — [Eur Radiol 2026, s00330-026-12598-1](https://link.springer.com/article/10.1007/s00330-026-12598-1) (snippet). It drops between vendors (vessel ICC 0.967 same vendor vs 0.766 different vendor) — [Radiology 2016, 10.1148/radiol.2016161670](https://pubs.rsna.org/doi/abs/10.1148/radiol.2016161670) (paywalled, abstract). These are volumes, not slopes.
- When the lumen is smaller than the reconstruction blur, segmentation tends to *overestimate* the diameter (patent text "Vessel lumen sub-resolution segmentation", [USPTO 10580141](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10580141); a patent, not peer reviewed).

### Inferences
- If small distal lumens are overestimated, measured taper is biased *flatter* distally. This bias shrinks the effect towards "less taper" and could mimic the hypothesised low-WSS state. A per-segment standardisation (as planned) handles the mean shift, not differences between people in image quality. Image quality (`scan_qualitative_quality`, BL) is a sensible sensitivity covariate.
- Over a 30 mm segment the expected diameter change (~0.75 mm) is about 1.5–2 voxels, but a robust slope over ~60 samples at 0.5 mm reduces random error far below that of two endpoint diameters. This is an argument for a regression slope over an endpoint ratio.
- The CGPS design gives a unique reproducibility check: baseline vs follow-up taper in segments that stay plaque-free (already proposed in the earlier report). It mixes scanner and protocol change with ten years of ageing, so it is a conservative (lower-bound) reliability estimate.

### Gaps
- No ICC for a geometric taper/log-radius slope on CCTA was found. No FFR-CT pipeline paper reporting taper as a named feature was found within the budget.
- TAG reproducibility is for attenuation, not geometry; it shows only that slopes along CCTA centerlines can be reproducible.

## Q4. How good papers introduce an untested but mechanistically motivated predictor

### Takeaway
Strong introductions follow Swales's "Create a Research Space" moves: establish what is known, show what is missing (the niche), then occupy it. The best imaging example is the perivascular fat attenuation index (FAI). Its authors go from a known driver (inflammation) to a missing measurement (no imaging of it), then to a mechanism that makes it visible (inflammation changes adjacent fat), a measure built from that mechanism, and a stated gap ("no cohort studies"). Taper maps cleanly onto the same structure.

### Cited Findings
- **CARS model.** Move 1 establishes the territory, Move 2 establishes a niche (counter-claiming, indicating a gap, question-raising, or continuing a tradition), and Move 3 occupies it. A guide warns that saying "nobody has tried this" is not enough on its own; writers should show what earlier work has not said. — [UMass Writing Center](https://www.umass.edu/writing-center/resources/creating-research-space); [CGU CARS handout (PDF)](https://my.cgu.edu/writing-rhetoric/wp-content/uploads/sites/9/2020/08/CARS-Model.pdf); [Lund AWELU, structure of introductions](https://www.awelu.lu.se/writing/writing-stage/structuring-the-text/structure-of-introductions). Canonical source: Swales J. *Genre Analysis*, Cambridge UP 1990 (not read this session).
- **Example 1, mechanism → measure (Antonopoulos et al. 2017, Sci Transl Med, DOI 10.1126/scitranslmed.aal2658, abstract open).** "Because vascular inflammation is not detectable with commonly used imaging modalities, we hypothesized that phenotypic changes in perivascular adipose tissue (PVAT) induced by vascular inflammation could be quantified using a new computerized..." They then show the mechanism ("inflamed human vessels release cytokines that prevent lipid accumulation in PVAT-derived preadipocytes") before introducing FAI. — [Oxford record](https://www.cardioscience.ox.ac.uk/bhf-centre-of-research-excellence/our-team/charalambos-antoniades/publication_modal/698028). (The quote starts with "Because"; Mathilde's style rule forbids that opening, so borrow the structure, not the wording.)
- **Example 2, gap stated as absence of cohort evidence (Oikonomou et al. 2018, Lancet, CRISP-CT, DOI 10.1016/S0140-6736(18)31114-0, open on PMC).** The introduction moves from what CCTA does ("focuses predominantly on identification of anatomically significant coronary artery stenosis"), to where events arise ("most acute coronary syndromes are caused by unstable but non-obstructive atherosclerotic plaques"), to the missing measurement ("no method is readily available to allow early detection of vascular inflammation in coronary arteries"). The "Research in context" panel states the gap from a search: "we identified no cohort studies investigating the prognostic value of perivascular fat attenuation phenotyping." — [PMC6137540](https://pmc.ncbi.nlm.nih.gov/articles/PMC6137540/).
- **Example 3, "why this measure, not the common one" (Kashyap et al. 2022, Sci Rep, open).** The tortuosity index is presented as the most widely used measure, then shown to have no correlation with low TAWSS (p = 0.86), and average absolute curvature is recommended instead. This is a counter-claim (CARS Move 2a) used to justify the choice of measure. — [DOAJ](https://doaj.org/article/3670df7ece6f492a85e2ecc0fe144fb7). The thesis already uses this for curvature, and the same pattern applies to taper vs raw diameter.
- **Example 4, a location effect turned into a testable predictor (Wang et al. 2004, Circulation).** The authors turn an observed spatial pattern into predictable "hot spots" within the proximal third, and propose it to guide vulnerable-plaque detection. — [Harvard HMS record](https://hcp.hms.harvard.edu/publication/coronary-artery-spatial-distribution-acute-myocardial-infarction-occlusions) (abstract).

### Inferences
- Structure for the taper paragraph (prose, no lists, per thesis rules; my proposal):
  1. Established link: low WSS localises plaque, and in human CT-based flow studies lumen calibre is the strongest geometric determinant of WSS (Schultz 2023; Johnston 2007; Alamir surrogate study).
  2. Missing dimension: curvature, the LM bifurcation angle and the LM→LAD/LCx ratios describe bending and branching, but not how the lumen changes calibre along the artery.
  3. Mechanism: flow falls at each side branch, and the parent lumen normally tapers with it (Gijsen 2019; Medrano-Gracia 2016: ~0.25 mm per 10 mm). An artery that tapers less than its flow loss is relatively wide and, by Poiseuille scaling, has lower WSS. This step is an inference and must be written as a hypothesis.
  4. Why this measure: raw diameter carries sex, body size and dominance (Dodge 1992; Schultz 2023); a log-radius slope does not change when the artery is scaled. Torsion was null in humans and is noisy; the tortuosity index was null against low WSS (Zhang 2024; Kashyap 2022); distance from the ostium is held in the segment intercepts.
  5. Gap: no study was found that tested taper against WSS or incident coronary plaque in humans. State it as the result of a search ("we found no study ...") in the style of the CRISP-CT panel, not as "has never been studied".
- An example sentence in Mathilde's register (no list, no "Because" opening, "developed plaque"): "Curvature, the bifurcation angle and the diameter ratios describe how the artery bends and branches, but none of them describes how its lumen narrows between branches. Flow falls at every side branch, and in plaque-free arteries the lumen narrows by about 0.25 mm per 10 mm \cite{medranogracia2016}; an artery that narrows less than its flow falls is relatively wide for the flow it carries, which by Poiseuille scaling lowers its wall shear stress. Taper was therefore added as the rate of change of log lumen radius along the artery, which, unlike the diameter itself, does not change with body size or sex \cite{dodge1992}. We found no study that has tested taper against wall shear stress or incident coronary plaque."
- Skeptical framing: present the sign as open (WSS hypothesis predicts less taper → more plaque; diffuse sub-threshold disease predicts the opposite), which keeps the prespecified LR test two-sided.

### Gaps
- No MSc/PhD thesis was found in this session that justifies an untested geometric predictor. The examples are journal papers.
- Verbatim long passages could not be extracted (the tool limits quotes); the short quotes above are exact.
- Swales 1990 and Swales & Feak were not read directly; only university writing-centre summaries were.
