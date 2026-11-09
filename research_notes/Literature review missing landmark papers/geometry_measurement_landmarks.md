# Landmark papers on measuring coronary geometry and relating it to disease: what Section 2 of the review is missing

Scope: `Thesis_coronary/content/litterature_review/01_geometry_wss.tex`, `02_quantifying_geometry.tex`, `03_geometry_risk.tex` (prose and % headers read), `refs.bib` (keys listed), `reports/Literature review claim check.md` (read). Never suggested: CAS-Net, shen2026geometry.

Citation counts: **OpenAlex `cited_by_count`, retrieved 2026-11-08** through the OpenAlex API by DOI. Semantic Scholar rate-limited after one call (Schaap 2009: 415 on Semantic Scholar against 371 on OpenAlex). Google Scholar could not be queried. OpenAlex usually runs below Google Scholar, often by a factor of about 1.3 to 2, so read the counts as a ranking, not as Scholar figures. Findings for papers marked "abstract" come from PubMed/OpenAlex abstracts only. Papers marked "title only" had no abstract available and were not read.

## Which landmark papers are missing, ranked?

### Takeaway
The review's main gap is not a famous tortuosity or Murray paper. It is the **"geometric risk factor" line of Friedman and colleagues**: the 1983 hypothesis, the 1993 and 1997 autopsy studies relating LM bifurcation geometry to early lesions in the LAD and LCx, and Zhu 2009, which catalogued curvature, torsion and tortuosity per proximal, mid and distal segment of angiographically normal coronaries "as a potential tool for predicting risk". That line is the direct ancestor of this thesis's question and features, and none of it is in `refs.bib`. Two bibliography bugs also turned up: `schaap2009cat08` is cited in Methods but missing from `refs.bib`, and "Finet's ratio" is named in `sec:lit-wss` without `finet2008fractal` being cited.

### Cited Findings
Ranked list (rank 1 = most needed). "In bib" means the key exists in `refs.bib`; "cited" means it appears in a review `\cite`.

| # | Paper (full citation) | DOI | OpenAlex cites | One-line finding | In refs.bib? | Judgment | What it adds that no cited source holds |
|---|---|---|---|---|---|---|---|
| 1 | Friedman MH, Brinkman AM, Qin JJ, Seed WA. Relation between coronary artery geometry and the distribution of early sudanophilic lesions. *Atherosclerosis* 1993;98(2):193–199 | 10.1016/0021-9150(93)90128-H | 80 | In 15 autopsy hearts, LM branch angle (from a 3-D centerline reconstruction) correlated negatively with the relative proximal involvement of the LAD and LCx: "a small LM branch angle may be a 'geometric risk factor' for proximal atherosclerotic disease" (abstract) | No | **Must add** (Section 1 or 3) | The only source found that relates the LM bifurcation angle to *early* (sudanophilic, pre-stenotic) lesions, and it isolates the local geometric effect from systemic risk factors through a normalised index. It names the concept "geometric risk factor". Caveat: n = 15, autopsy, and its direction (small angle worse) is opposite to Tommasino's wide-angle finding, which is itself worth a sentence |
| 2 | Zhu H, Ding Z, Piana RN, Gehrig TR, Friedman MH. Cataloguing the geometry of the human coronary arteries: a potential tool for predicting risk of coronary artery disease. *Int J Cardiol* 2009;135(1):43–52 | 10.1016/j.ijcard.2008.03.087 | 54 | Biplane angiograms of 52 patients with angiographically normal LAD (32) and RCA (35): curvature, torsion and tortuosity per proximal/mid/distal segment; LAD highest distally, RCA lowest mid-segment, LAD torsion > RCA; >80% of the geometric variability expressed by two factors (abstract) | No | **Must add** (Section 2) | The only coronary source found that measures curvature per proximal/mid/distal segment in *normal* arteries, which is the thesis's unit of analysis. Its factor result (two factors explain >80%) is the one coronary example of reducing a multivariate curvature description, which fits `sec:lit-measure`. Caveats: referred angiography patients, 2-D biplane reconstruction, no outcome |
| 3 | Friedman MH, Deters OJ, Mark FF, Bargeron CB, Hutchins GM. Arterial geometry affects hemodynamics: a potential risk factor for atherosclerosis. *Atherosclerosis* 1983;46(2):225–231 | 10.1016/0021-9150(83)90113-2 | 264 | Origin of the "geometric risk factor" hypothesis, that individual differences in arterial geometry change local haemodynamics and so individual susceptibility (title only; no abstract on PubMed/OpenAlex) | No | Nice to have (one of #1 or #3, not both, unless the hypothesis gets its own sentence) | Gives the hypothesis its original source. Not read: I believe it studied casts of the human aortic bifurcation, not coronaries, but I could not verify this. Read before citing |
| 4 | Ding Z, Biggs T, Seed WA, Friedman MH. Influence of the geometry of the left main coronary artery bifurcation on the distribution of sudanophilia in the daughter vessels. *Arterioscler Thromb Vasc Biol* 1997;17(7):1356–1360 | 10.1161/01.ATV.17.7.1356 | 47 | In 17 vascular casts, LAD proximal involvement correlated best with an interaction of LM bifurcation planarity and the LCx–LAD angle (P = .013); geometric features act jointly (PubMed abstract) | No | Nice to have (only if #1 is not used) | An early-lesion counterpart to Garcha 2025's finding that the features do not act independently. Caveat: n = 17. OpenAlex attaches a wrong abstract (rabbit aorta) to this DOI, so use PubMed (PMID 9261267) |
| 5 | Morbiducci U, Kok AM, Kwak BR, Stone PH, Steinman DA, Wentzel JJ. Atherosclerosis at arterial bifurcations: evidence for the role of haemodynamics and geometry. *Thromb Haemost* 2016;115(3):484–492 | 10.1160/TH15-07-0597 | 267 | Review: plaque co-localises with disturbed flow at geometrically predisposed sites; geometric attributes are the "easier-to-measure" surrogates of shear stress (abstract) | No | Nice to have (Section 1) | A review-level statement that geometry is a surrogate for WSS at both carotid and coronary bifurcations, which is the thesis's premise. `chatzizisis2007ess` holds the low-WSS → plaque link but not the "geometry as surrogate marker" step. Cite it only if that sentence needs a source beyond the CFD studies |
| 6 | Lee SW, Antiga L, Spence JD, Steinman DA. Geometry of the carotid bifurcation predicts its exposure to disturbed flow. *Stroke* 2008;39(8):2341–2347 | 10.1161/STROKEAHA.107.510644 | 365 | CFD of 50 carotid bifurcations of 25 young adults: disturbed-flow area related to proximal area ratio and bifurcation tortuosity, not to bifurcation angle or planarity; interindividual variation exceeded reconstruction uncertainty (abstract) | No (but `bijari2014flare`, the same group's follow-up, is in bib and uncited) | Nice to have / not needed | The canonical test of the "geometric risk" assumptions, i.e. that disturbed flow varies widely between people and follows lumen geometry. Carotid, not coronary, and Kashyap 2022 already makes the coronary version of the point. Bijari 2014 (82 cites; carotid geometry predicts early wall thickening) is the carotid analogue of the thesis question and is already in `refs.bib`. If one carotid paper is used, Bijari 2014 is the better fit (outcome = early wall thickening), but its sample (believed to be MESA participants) was not verified here |
| 7 | Murray CD. The physiological principle of minimum work: I. The vascular system and the cost of blood volume. *PNAS* 1926;12(3):207–214 | 10.1073/pnas.12.3.207 | 2,119 | Minimum-work optimum: flow ∝ r³, so parent r³ = sum of daughter r³ (classic) | No (only `taylor2024murray`, `schoenenberger2012murray`, `huo2012scaling`, `finet2008fractal`) | **Must add in Methods 05c** if the text names "Murray's law"; not needed in the review | The original statement of the law that the LM→LAD/LCx diameter ratios are judged against. Taylor 2024 (a meta-analysis) reports the coronary exponent but is not the eponymous source |
| 8 | Finet G, Gilard M, Perrenot B, et al. Fractal geometry of arterial coronary bifurcations: a quantitative coronary angiography and intravascular ultrasound analysis. *EuroIntervention* 2008;3(4):490–498 | 10.4244/EIJV3I4A87 | 219 | Coronary bifurcation diameters follow D_parent = 0.678 (D_d1 + D_d2) (well known; not re-read here) | **Yes**, not cited in review | **Must cite where "Finet's ratio" is named** (`01_geometry_wss.tex`, Zhang sentence), or drop the eponym | The prose names "Finet's ratio" with no Finet citation. This is a citation bug rather than a missing landmark |
| 9 | Hutchins GM, Bulkley BH, Miner MM, Boitnott JK. Correlation of age and heart weight with tortuosity and caliber of normal human coronary arteries. *Am Heart J* 1977;94(2):196–202 | 10.1016/S0002-8703(77)80280-9 | 102 | Autopsy: coronary tortuosity and calibre in normal arteries increase with age and heart weight (title only; no abstract online) | No | Nice to have (Section 3 or Methods 06) | The earliest source that coronary tortuosity tracks age, a SCORE2 factor. That supports testing geometry *beyond* SCORE2 and the "variance explained by known risk factors" check (`sec:method-validity-split`). Not read |
| 10 | Ciurică S, Lopez-Sublet M, Loeys BL, et al. Arterial tortuosity. *Hypertension* 2019;73(5):951–960 | 10.1161/HYPERTENSIONAHA.118.11647 | 206 | Review of arterial tortuosity across beds (genetic, hypertensive, ageing, SCAD/FMD links) (no abstract online; content not verified) | No | Nice to have (one tortuosity review at most) | A review stating outright that tortuosity has no agreed definition, which Kashyap only implies (the claim check flagged this). Must be read in full first |
| 11 | Kahe F, Sharfaei S, Pitliya A, et al. Coronary artery tortuosity: a narrative review. *Coron Artery Dis* 2020;31(2):187–192 (online 2019) | 10.1097/MCA.0000000000000769 | 48 | Coronary tortuosity is common and linked to ageing, hypertension and atherosclerosis; possible ischaemia, altered shear; "generally benign" (abstract) | No | Alternative to #10 (coronary-specific, less cited) | Same role as Ciurică. The abstract does not state the "no agreed definition" point |
| 12 | Pflederer T, Ludwig J, Ropers D, Daniel WG, Achenbach S. Measurement of coronary artery bifurcation angles by multidetector computed tomography. *Invest Radiol* 2006;41(10):793–798 | 10.1097/01.rli.0000239318.88270.9f | 87 | Phantom and patient study of CT bifurcation-angle accuracy and interobserver variability against invasive angiography, plus the normal distribution of four main bifurcation angles (abstract) | No | Nice to have (Methods 06, not the review) | The standard source that the LM angle can be measured on CT, with accuracy and reader variability. Caveat: 16-slice CT, 15 patients for variability |
| 13 | Medrano-Gracia P, Ormiston J, Webster M, et al. A computational atlas of normal coronary artery anatomy. *EuroIntervention* 2016;12(7):845–854 | 10.4244/EIJV12I7A139 | 89 | Statistical atlas of LM bifurcation shape in CCTA of people without CAD (known; not re-read) | **Yes**, dropped for space | Nice to have | The normal-population reference for LM bifurcation angles and diameters on CCTA. `medranogracia2017bifurcation` (33 cites; no clear shape–risk-factor relation in calcium-zero patients) is the one-sentence option the claim check proposed |
| 14 | Kassab GS. Scaling laws of vascular trees: of form and function. *Am J Physiol Heart Circ Physiol* 2006;290(2):H894–H903 | 10.1152/ajpheart.00579.2005 | 225 | Review of diameter, length and flow scaling in vascular trees (known; not re-read) | No (`huo2012scaling` is in bib) | Not needed | `huo2012scaling` already holds the 7/3 exponent, so the one-source rule argues against this |
| 15 | Schaap M, Metz CT, van Walsum T, et al. Standardized evaluation methodology and reference database for evaluating coronary artery centerline extraction algorithms. *Med Image Anal* 2009;13(5):701–714 | 10.1016/j.media.2009.06.003 | 371 (Semantic Scholar 415) | CAT08: the reference standard and overlap/accuracy metrics for coronary centerline extraction on CCTA | **No (bug)**: `\cite{schaap2009cat08}` in `methodology/01b_medis_reference.tex` line 31 has no `refs.bib` entry | **Fix the bib**; not needed in the review | Already the cited method source for clipping at the first and last contour. It must be in `refs.bib` or LaTeX will print "?" |
| 16 | Leipsic J, Abbara S, Achenbach S, et al. SCCT guidelines for the interpretation and reporting of coronary CT angiography. *J Cardiovasc Comput Tomogr* 2014;8(5):342–358 | 10.1016/j.jcct.2014.07.003 | 1,100 | Reporting standard incl. the coronary segment model and stenosis grading (known) | No (`abbara2016scct`, the acquisition guideline, is in bib) | Not needed in the review; possibly Data `sec:data-plaque-location` | The source for the segment model and grade categories the CGPS reads use, *if* the CGPS reads follow it (unverified; ask Kit). Belongs in Data, not the review |
| 17 | Kirişli HA, Schaap M, Metz CT, et al. Standardized evaluation framework for evaluating coronary artery stenosis detection, stenosis quantification and lumen segmentation algorithms in computed tomography angiography. *Med Image Anal* 2013;17(8):859–876 | 10.1016/j.media.2013.05.007 | 209 | Rotterdam stenosis/lumen-segmentation benchmark | No | Not needed | The tracer is not the author's work and the Medis comparison already has Schaap |
| 18 | Passerini T, Sangalli LM, Vantini S, et al. An integrated statistical investigation of internal carotid arteries of patients affected by cerebral aneurysms. *Cardiovasc Eng Technol* 2012;3(1):26–40 | 10.1007/s13239-011-0079-x | 37 | AneuRisk follow-up: FDA of carotid radius and curvature combined with CFD (title only) | No | Not needed | Same cohort and point as `sangalli2009aneurisk` |
| 19 | Eleid MF, Guddeti RR, Tweet MS, et al. Coronary artery tortuosity in spontaneous coronary artery dissection. *Circ Cardiovasc Interv* 2014;7(5):656–662 | 10.1161/CIRCINTERVENTIONS.114.001676 | 324 | 246 SCAD vs 313 controls: tortuosity 78% vs 17%; severe tortuosity HR 3.29 (0.99–8.29) for recurrence (abstract) | No | Not needed | The most cited *coronary-specific* tortuosity paper, but about SCAD, a non-atherosclerotic disease, in a referral case-control sample. Off-topic for plaque |
| 20 | Han HC. Twisted blood vessels: symptoms, etiology and biomechanical mechanisms. *J Vasc Res* 2012;49(3):185–197 | 10.1159/000335123 | 499 | Review: tortuosity linked with ageing, atherosclerosis, hypertension, genetic defects and diabetes; proposes mechanical instability as cause (abstract) | No | Not needed (or the alternative to #10) | The most cited general tortuosity review, but not coronary and not about measurement |
| 21 | Zegers ES, Meursing BT, Zegers EB, Oude Ophuis AJ. Coronary tortuosity: a long and winding road. *Neth Heart J* 2007;15(5):191–195 | 10.1007/BF03085979 | 106 | Three case reports of angina with tortuosity and no stenosis, plus a hypothesis of pressure loss → ischaemia (abstract) | No | Not needed | A case series. It is widely cited but adds nothing on measurement or plaque |
| 22 | Turgut O, Yilmaz A, Yalta K, et al. Tortuosity of coronary arteries: an indicator for impaired left ventricular relaxation? *Int J Cardiovasc Imaging* 2007;23(6):671–677 | 10.1007/s10554-006-9186-4 | 70 | Visual tortuosity linked to diastolic dysfunction (title only) | No | Not needed | Often cited for the visual "≥3 bends ≥45°" type of definition that Li 2011 used. Not verified as its origin |
| 23 | Estrada APD, Lopes RO, Villacorta H. Coronary tortuosity and its role in myocardial ischemia in patients with no coronary obstructions. *Int J Cardiovasc Sci* 2017;30(2):163–170 | 10.5935/2359-4802.20170014 | 12 | Narrative review of tortuosity and ischaemia without obstruction (abstract) | No | Not needed | Low impact, regional journal, narrative |

Supporting abstracts and records:
- Friedman 1993 abstract (LM angle vs relative proximal involvement, 15 hearts, "geometric risk factor") — [PubMed 7681291](https://pubmed.ncbi.nlm.nih.gov/7681291/)
- Zhu 2009 abstract (52 patients, per-segment curvature/torsion/tortuosity, two factors >80%) — [PubMed 18597872](https://pubmed.ncbi.nlm.nih.gov/18597872/)
- Ding 1997 abstract (17 casts, planarity × LCx–LAD angle interaction, P = .013) — [PubMed 9261267](https://pubmed.ncbi.nlm.nih.gov/9261267/)
- Friedman 1983 record (no abstract) — [PubMed 6838702](https://pubmed.ncbi.nlm.nih.gov/6838702/)
- Morbiducci 2016 abstract ("easier-to-measure" geometric surrogates) — [OpenAlex/DOI](https://doi.org/10.1160/th15-07-0597)
- Lee 2008 abstract — [DOI](https://doi.org/10.1161/STROKEAHA.107.510644)
- Hutchins 1977 record (no abstract) — [PubMed 141878](https://pubmed.ncbi.nlm.nih.gov/141878/)
- Ciurică 2019 record (no abstract) — [PubMed 30852920](https://pubmed.ncbi.nlm.nih.gov/30852920/)
- Kahe abstract — [DOI](https://doi.org/10.1097/MCA.0000000000000769)
- Eleid 2014 abstract — [DOI](https://doi.org/10.1161/CIRCINTERVENTIONS.114.001676)
- Pflederer 2006 abstract — [PubMed 17035869](https://pubmed.ncbi.nlm.nih.gov/17035869/)
- Citation counts — [OpenAlex API](https://api.openalex.org/works/doi:10.1073/pnas.12.3.207) (same endpoint used for every DOI above)

### Inferences
- The thesis's own framing is close to the Friedman "geometric risk factor" programme: geometry as a person-level, measurable predisposition, measured per segment, independent of systemic risk factors. A reviewer from biomechanics would likely notice its absence more than the absence of any tortuosity review. A reviewer from clinical cardiology would more likely expect a tortuosity review (Ciurică or Kahe) and SCCT.
- Friedman 1993 also gives the review a useful tension: a *small* LM angle with early proximal lesions (autopsy) against Tommasino's *wide* angle with progression (referred, 1 year). This parallels the direction disagreement that `sec:lit-measure` already shows for curvature.
- The two bibliography problems (Schaap missing from `refs.bib`; "Finet's ratio" uncited) are cheaper and more certain fixes than any addition.

### Gaps
- Google Scholar counts could not be retrieved; Semantic Scholar rate-limited. All counts are OpenAlex.
- Friedman 1983, Hutchins 1977, Ciurică 2019, Turgut 2007 and Passerini 2012 had no abstract available; their one-line findings are from titles or general knowledge and must be read before use.
- Finet 2008, Medrano-Gracia 2016, Kassab 2006, Murray 1926 and Leipsic 2014 findings are stated from well-known content, not re-read in this session.

## Coronary tortuosity definitions and clinical associations: which source is the standard?

### Takeaway
No single coronary tortuosity paper is the agreed standard. By citations, the most cited coronary-specific paper is Eleid 2014 (SCAD, 324), and the most cited general reviews are Han 2012 (499) and Ciurică 2019 (206). For plaque, none of them adds a measurement the review lacks. The one review-level addition worth making is a single tortuosity review that states the lack of an agreed definition (Ciurică preferred, Kahe as the coronary alternative), after full-text reading. Groves 2009 (cut) is a small regional-journal visual study and should stay cut.

### Cited Findings
- Eleid 2014: 246 SCAD vs 313 controls; tortuosity 78% vs 17%; recurrent SCAD in tortuous segments in 80% — [Circ Cardiovasc Interv](https://doi.org/10.1161/CIRCINTERVENTIONS.114.001676)
- Kahe 2020: tortuosity "commonly associated with aging, hypertension, atherosclerosis"; "generally ... a benign entity" — [Coron Artery Dis](https://doi.org/10.1097/MCA.0000000000000769)
- Han 2012: clinical links of tortuosity with ageing, atherosclerosis, hypertension, genetic defects, diabetes; "mechanisms ... poorly understood" — [J Vasc Res](https://doi.org/10.1159/000335123)
- Zegers 2007 is three case reports and a hypothesis — [PubMed 17612682](https://pubmed.ncbi.nlm.nih.gov/17612682/)
- Estrada 2017 is a narrative review — [Int J Cardiovasc Sci](https://doi.org/10.5935/2359-4802.20170014)
- `groves2009tortuosity` is in `refs.bib` (W V Med J, no DOI), cut from the review; OpenAlex did not index it — [refs.bib, local]
- Zebić Mihić 2024 (`zebicmihic2024index`, in bib) compares the tortuosity index with angle-count methods; 5 OpenAlex cites — [Diagnostics](https://doi.org/10.3390/diagnostics14010035)
- Hutchins 1977: tortuosity and calibre vs age and heart weight in normal coronaries — [PubMed 141878](https://pubmed.ncbi.nlm.nih.gov/141878/)

### Inferences
- For the review's "no summary has been agreed" sentence, the claim check already found that Grisan is retinal and Kashyap only implies the point. A tortuosity review is the clean single source, but only after its text is confirmed.
- Hutchins 1977 is more useful to the thesis than any tortuosity review. Age dependence of tortuosity is the reason geometry must be tested *beyond* SCORE2 (whose main factor is age). It also bears on the planned check of how much feature variance the known risk factors explain.
- Most clinical tortuosity definitions are visual counts of bends on invasive angiograms (Li 2011, Groves, Eleid's score). None is a continuous 3-D curvature measure, so none competes with Kashyap/Zhang as the source for average curvature.

### Gaps
- Could not confirm which paper first set the "≥3 bends ≥45°" definition (Turgut 2007 vs Zegers 2007 vs Li 2011).
- Ciurică 2019 full text not obtained; whether it states "no agreed definition" is unverified.

## Bifurcation angle and diameter scaling laws: which are expected?

### Takeaway
Expected in a thesis that uses LM→LAD/LCx diameter ratios: **Murray 1926** (2,119 cites) as the eponymous law, cited where Methods 05c names it, and **Finet 2008** cited wherever "Finet's ratio" is named (it is named in `sec:lit-wss` without a citation). Huo and Kassab 2012 is already in bib for 7/3. For the LM angle, Friedman 1993 is the missing early-lesion evidence. Pflederer 2006 is the standard CT measurement source, and Medrano-Gracia 2016 (in bib) the normal CCTA atlas. No "Rodriguez-Granillo 2016" LM-angle paper was found, which matches the existing CAREFUL note in `00_chapter_intro.tex`.

### Cited Findings
- Murray 1926 — 2,119 OpenAlex citations — [PNAS](https://doi.org/10.1073/pnas.12.3.207)
- Finet 2008 — 219 citations; already `finet2008fractal` — [EuroIntervention](https://doi.org/10.4244/EIJV3I4A87)
- Huo & Kassab 2012 — 153 citations; already `huo2012scaling` — [J R Soc Interface](https://doi.org/10.1098/rsif.2011.0270)
- Kassab 2006 scaling review — 225 citations — [Am J Physiol](https://doi.org/10.1152/ajpheart.00579.2005)
- Zhou, Kassab, Molloi 1999, generalisation of Murray's law for the coronary tree — 199 citations — [Phys Med Biol](https://doi.org/10.1088/0031-9155/44/12/306)
- Taylor 2024 meta-analysis of Murray's law in coronaries — 22 citations; in bib — [Am J Physiol](https://doi.org/10.1152/ajpheart.00142.2024)
- Schoenenberger 2012, deviation from Murray's law and calcification — 26 citations; in bib — [Atherosclerosis](https://doi.org/10.1016/j.atherosclerosis.2011.12.040)
- Friedman 1993 (n = 15) and Ding 1997 (n = 17): LM angle / planarity vs early proximal LAD/LCx lesions — [PubMed 7681291](https://pubmed.ncbi.nlm.nih.gov/7681291/); [PubMed 9261267](https://pubmed.ncbi.nlm.nih.gov/9261267/)
- Pflederer 2006: CT angle accuracy (phantom 25–90°), interobserver variability vs invasive angiography in 15 patients, normal angle distribution — [PubMed 17035869](https://pubmed.ncbi.nlm.nih.gov/17035869/)
- Temov 2016 — 34 citations; in bib, cited in the Introduction — [Int J Cardiovasc Imaging](https://doi.org/10.1007/s10554-016-0884-2)
- Medrano-Gracia 2016 atlas — 89; 2017 shape study — 33; both in bib — [EuroIntervention](https://doi.org/10.4244/EIJV12I7A139); [J Cardiovasc Transl Res](https://doi.org/10.1007/s12265-016-9720-2)
- Juan 2017 — 32; Cui 2017 — 44 (both in bib) — [Sci Rep](https://doi.org/10.1038/s41598-017-01679-3); [PLoS ONE](https://doi.org/10.1371/journal.pone.0174352)
- Sun & Cao 2011, CT LM bifurcation angle vs plaque — 78 citations; not in bib — [Eur J Radiol](https://doi.org/10.1016/j.ejrad.2011.04.015)
- OpenAlex search for "left main bifurcation angle plaque Rodriguez-Granillo" returned no such 2016 paper — [OpenAlex search](https://api.openalex.org/works?search=left%20main%20bifurcation%20angle%20plaque%20Rodriguez-Granillo)

### Inferences
- The scaling sources belong in Methods 05c (which the content map says owns Murray, 2.39 and 7/3), not in the review. The review only needs Finet cited where the eponym appears.
- Friedman 1993 and Tommasino 2024 point in opposite directions for the LM angle (small angle → early proximal lesions vs wide angle → progression). Together with the Medrano-Gracia normal atlas, they show that the angle's expected sign is not settled. That is a direct argument for a two-sided test of the geometry block.
- Pflederer 2006 fits `sec:method-validity` (measurement properties) better than the review.

### Gaps
- No source found that tests LM→LAD/LCx diameter ratios (as opposed to Murray deviation or Finet) against later plaque.
- The Sun & Cao 2011 finding was not read beyond the title.

## Centerline extraction and measurement standards on CCTA: do any belong in the review?

### Takeaway
No. Schaap 2009 (CAT08), Kirişli 2013 and Lesage 2009 are standards for building or evaluating extraction algorithms. The tracer is cited as someone else's tool, and the review's chapter rules leave measure definitions to Methods. The SCCT reporting guideline (Leipsic 2014, about 1,100 cites) may belong in the Data chapter if the CGPS reads follow its segment model. **Action item:** `schaap2009cat08` is cited in `methodology/01b_medis_reference.tex` but has no entry in `refs.bib`.

### Cited Findings
- Schaap 2009 — 371 (OpenAlex), 415 (Semantic Scholar) — [Med Image Anal](https://doi.org/10.1016/j.media.2009.06.003)
- Kirişli 2013 — 209 — [Med Image Anal](https://doi.org/10.1016/j.media.2013.05.007)
- Lesage 2009 lumen-segmentation review — 951 — [Med Image Anal](https://doi.org/10.1016/j.media.2009.07.011)
- Leipsic 2014 SCCT interpretation/reporting guideline — 1,100 — [J Cardiovasc Comput Tomogr](https://doi.org/10.1016/j.jcct.2014.07.003)
- CAD-RADS 2.0 (Cury 2022) — 449 — [J Cardiovasc Comput Tomogr](https://doi.org/10.1016/j.jcct.2022.07.002)
- `grep schaap` over `Thesis_coronary/refs.bib` returns nothing; the `\cite{schaap2009cat08}` is at `content/methodology/01b_medis_reference.tex:31` — [local files]

### Inferences
- `bransby2026imagecasx` was already cut from the review. Adding extraction benchmarks would reintroduce a strand the author removed on purpose.
- Leipsic 2014 would source the per-segment grading in `sec:data-plaque-location`. Check with Kit whether the CGPS 17-segment reads follow SCCT/AHA before citing.

### Gaps
- Not verified which segment model the CGPS reads use.

## Functional data analysis of vessel geometry: is there a coronary example?

### Takeaway
No peer-reviewed FPCA of coronary curvature profiles was found, which confirms the earlier search noted in the `02_quantifying_geometry.tex` header. A PubMed query (`functional data analysis[tiab] AND coronary[tiab] AND (centerline OR curvature OR geometry)`) returned zero records. The nearest coronary analogue is **Zhu 2009**, a factor analysis of per-segment curvature, torsion and tortuosity in which two factors explained more than 80% of variability. It is multivariate reduction of scalar summaries, not FPCA of a profile. Sangalli 2009 (113 cites, JASA) remains the vascular FPCA precedent. Passerini 2012 and AneuRisk65 (2014) are the same cohort and should not be added.

### Cited Findings
- PubMed query above returned no IDs (run 2026-11-08) — [PubMed E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=functional%20data%20analysis%5Btiab%5D%20AND%20coronary%5Btiab%5D%20AND%20(centerline%20OR%20curvature%20OR%20geometry))
- Sangalli 2009 JASA — 113 citations; in bib — [JASA](https://doi.org/10.1198/jasa.2009.0002)
- Sangalli, Secchi, Vantini, Veneziani 2009, free-knot regression splines for 3-D centerlines and their derivatives (curvature estimation) — 69 citations — [J R Stat Soc C](https://doi.org/10.1111/j.1467-9876.2008.00653.x)
- Passerini 2012 — 37; AneuRisk65 dataset paper 2014 — 32 — [Cardiovasc Eng Technol](https://doi.org/10.1007/s13239-011-0079-x); [Electron J Stat](https://doi.org/10.1214/14-ejs938)
- Zhu 2009: >80% of coronary geometric variability in two factors — [PubMed 18597872](https://pubmed.ncbi.nlm.nih.gov/18597872/)
- Claim check: only coronary FPCA-type work found was an arXiv preprint (2411.18398, diameter curves), not suitable — [local report](file:///Users/mathildebrinchsorensen/Desktop/ImageCAS-X/reports/Literature%20review%20claim%20check.md)

### Inferences
- The review's closing claim that profile shape has been shown in coronaries in only one study (Tello Ayala, angiograms) holds after this search.
- The Sangalli 2009 JRSS-C spline paper is not a review addition. It could support Methods 05a if the text has to justify how curvature is estimated from a noisy centerline (smoothing before differentiation), which is an open question for the tracer.
- Zhu 2009 can serve `sec:lit-measure` twice without breaking the one-source rule: as the per-segment normal-geometry catalogue, and as the only coronary example of reducing curvature descriptors jointly.

### Gaps
- Scopus, Web of Science and Google Scholar were not searched, so a coronary FPCA paper in a conference or engineering venue cannot be ruled out.
- arXiv 2411.18398 was not re-checked for a peer-reviewed version.
