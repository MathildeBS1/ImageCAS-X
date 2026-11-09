# Section 2 claim check: "Summarising Curvature Along the Artery" (sec:lit-measure)

File checked: `Thesis_coronary/content/litterature_review/02_quantifying_geometry.tex` (prose as of 2026-11-08).
Full texts read for this check (2026-11-08): Tello Ayala 2026 (Europe PMC full-text XML of PMC13308244),
Li 2011 (Europe PMC full text of PMC3164184), Goldsmith 2011 NeuroImage (NCBI efetch of PMC3114268,
including Tables 1–3), Kashyap 2022 (abstract, Europe PMC), Goldsmith et al. 2011 JCGS PFR method paper
(abstract, Europe PMC). Sangalli 2009 and Grisan 2008 were checked against the earlier full-text notes in
`research_notes/FPCA technical background section/fpca_vessel_geometry_applications.md` and
`knowledge/docs_thesis/papers/grisan2008tortuosity.md` (both from full-text reads); not re-read today.

Verdict summary (sentence by sentence):

| # | Sentence (short) | Cite | Verdict |
|---|---|---|---|
| 1 | Studies above described curvature by one value per artery | (none) | Supported by sec:lit-wss (internal) |
| 2 | Condensing a continuous property is a common challenge; any summary keeps only some aspects, e.g. sharpness or number of bends | ramsay2005fda | General idea consistent with FDA; the bend example and the "biological structures" framing are not Ramsay's: partly unverifiable |
| 3 | For coronary curvature, different summaries used and none agreed | grisan, kashyap, li, tello | "Different summaries used": supported by Kashyap, Li, Tello. Grisan is retinal, not coronary: wrong as cited. "None agreed": supported only indirectly |
| 4 | Choice of summary has even decided the direction of the CAD association | (paragraph) | Overstated as a cross-study claim (Li vs Tello differ in much more than the measure); supported within Tello Ayala only |
| 5 | Li 2011: counted sharp bends on invasive angiograms of chest-pain patients; more such bends, less likely CAD | li2011 | Mostly supported; "counted ... more such bends" is overstated (binary ≥3-bend rule, not a count); borderline, adjusted, model direction reversed |
| 6 | Tello Ayala 2026: RCA with greater average turning angle more likely CAD; by tortuosity index slightly less likely | telloayala2026 | First half supported (adjusted). Second half overstated/reframed: it is a linear model of the index on stenosis, β = −0.03, P = 0.042 |
| 7 | Outside coronaries, studies avoided reduction by analysing whole profile | (none) | Fine as a bridge, but uncited |
| 8 | FPCA is a common method for quantities changing over time or along a structure | ramsay2005fda | Supported (Ramsay ch. 8); "common" better supported by ullah2013fda |
| 9 | Sangalli 2009: FPCA of ICA curvature profile; shape separated patients by aneurysm location | sangalli2009 | Overstated: classifier used radius and curvature scores together; partial separation (LOO error ~21.5%), K chosen on the same LOO error, referred sample |
| 10 | Goldsmith 2011: used FPCA on a tissue property along white-matter tracts; in most tracts whole profile separated MS from controls better than the tract average | goldsmith2011pfr | Mostly supported; "used FPCA" not stated in the NeuroImage paper (it is inside the PFR method); "most tracts" = two of three on the test set; no test of the difference |
| 11 | Tello Ayala: neural network on the whole profile identified CAD better than the average alone | telloayala2026 | Supported as reported (AUROC 0.67 vs 0.60), but no formal test; models differ in class; label from the same angiogram |
| 12 | Together: profile shape carries information a single value discards; in coronaries only one study, on invasive angiograms | sangalli, goldsmith, tello | Reasonable synthesis; the coronary half needs the caveats of #11 |

---

## Q1. Li et al. 2011: invasive angiograms, chest pain, more sharp bends less likely to have CAD? Visual? Adjusted?

### Takeaway
Population and direction are correct: 1,010 consecutive Chinese patients who had elective invasive coronary
angiography for chest pain, with tortuosity less common in patients with CAD (adjusted OR 0.755, P = 0.045,
borderline). But Li did not analyse a bend *count*. Tortuosity was a yes/no label (≥3 bends of ≥45° in the main
part of at least one artery, seen in both systole and diastole). The paper does not say how the bends were
judged (no quantitative coronary angiography is described, so it was most likely read by eye). CAD meant ≥50%
stenosis, and the regression had tortuosity as its outcome and CAD as one of its predictors.

### Cited Findings
- Population: "A total of 1010 consecutive patients underwent coronary angiography due to chest pain and similar symptoms were included in the present study (544 male, mean age: 64±11 years)"; "All patients underwent elective coronary angiography according to the Judkins technique using a Philip FD-10 X-ray system." — [Li et al. 2011, PLoS ONE, PMC3164184](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0024232)
- Definition: "CT was identified by ≥3 bends (defined as ≥45° change in vessel direction) along main trunk of at least one artery, present both in systole and in diastole [4]". The LAD was assessed in RAO cranial, the LCX in LAO caudal and the RCA in RAO views. — [Li et al. 2011](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0024232)
- How the bends were assessed (visually or by software) is not stated. No QCA software, reader count or blinding is described. — [Li et al. 2011](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0024232) (absence noted from the full text)
- CAD definition: "CAD was verified as ≥50% luminal narrowing in at least one main coronary artery." — [Li et al. 2011](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0024232)
- Unadjusted: CAD in 49.6% of tortuosity-positive vs 60.7% of tortuosity-negative patients (P = 0.001). The abstract puts it the other way round: tortuosity in 45.1% of non-CAD vs 34.4% of CAD patients (P = 0.001). — [Li et al. 2011](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0024232)
- Adjusted: Table 2, "Multivariate logistic regression analysis of selected variables for coronary tortuosity": female OR 2.603, hypertension OR 1.533, diabetes OR 0.702, hyperlipidemia OR 0.657, CAD B −0.48, OR 0.755 (95% CI 0.574–0.994), P = 0.045. The outcome is tortuosity; the covariates shown are sex, hypertension, diabetes, hyperlipidemia and CAD. Age and smoking are not shown, and the text gives no rule for selecting the variables. — [Li et al. 2011](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0024232)
- Reporting inconsistency: Table 3 (LAD tortuosity vs LAD ≥50% stenosis) prints the *same* OR 0.755 (0.574–0.994) but with B −0.192, SE 0.210 and χ² 97.095, P < 0.001. In Table 2, B −0.48 does not equal ln(0.755) = −0.28 either. So the printed CAD estimate is internally inconsistent. — [Li et al. 2011](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0024232)
- No association for the LCX or RCA: "There were no significant difference between LCX(RCA) tortuosity and LCX(RCA) artherosclerosis." — [Li et al. 2011](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0024232)
- Many of the CAD patients had already been revascularised (Table 4: previous PCI 62.8% vs 65.3% by tortuosity group). — [Li et al. 2011](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0024232)
- MACE over 2–4 years did not differ by tortuosity; the authors cite the small sample and short follow-up. — [Li et al. 2011](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0024232)

### Inferences
- "counted sharp bends ... patients with more such bends" is the weak point. A suggested rewrite: "Li et al. (2011) classed
  an artery as tortuous when it had at least three sharp bends on invasive angiograms of patients with chest pain,
  and patients with such arteries were less likely to have CAD". This is still true and no longer implies a dose-response with bend count.
- The adjusted result is borderline (upper CI 0.994), and its printed numbers are inconsistent. The thesis does not need
  to say this in the prose (the chapter forbids numbers), but it should not lean on Li alone for the direction.
- "CAD" in Li is obstructive (≥50%) disease, unlike the thesis outcome (any plaque). This matters if the closing synthesis or the
  Methods later compare directions.

### Gaps
- Whether the bend reading was visual, blinded or done by one or more readers: not reported.
- The full covariate set of the multivariable model: not reported beyond "selected variables".

---

## Q2. Tello Ayala et al. 2026: RCA, greater average turning angle more likely CAD, tortuosity index slightly less likely; neural network on the whole profile better than the average? Peer-reviewed? Population?

### Takeaway
The paper is a peer-reviewed original research article in JACC: Advances (received 13 Nov 2025, revised
18 Mar 2026, accepted 21 Apr 2026; PMC flags it as not a preprint). The mean-turning-angle result is
correct and adjusted (OR 1.05 per SD). The "tortuosity index slightly less likely" half is a reframing. The paper
reports that in a *linear model with the arc/chord index as outcome*, RCA stenosis had a weak inverse coefficient
(β = −0.03, P = 0.042), in a supplementary table. The neural-network result is reported as AUROC 0.67 vs 0.60,
with no formal test of the difference, between models of different classes, on a CAD label read from the same angiogram.
The population is a single-centre cardiac catheterisation registry, so these are patients referred for invasive
angiography, including some who had already been revascularised.

### Cited Findings
- Journal and dates: JACC: Advances 2026;5(6):102829, "Original Research"; history dates 13-11-2025 (received), 18-03-2026 (revised), 21-04-2026 (accepted), published 17-06-2026; PMC metadata "pmc-prop-preprint no". No medRxiv or arXiv version was found in this check. — [Tello Ayala et al. 2026, PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/); [DOI](https://doi.org/10.1016/j.jacadv.2026.102829)
- Population: "This study was conducted using data from the Massachusetts General Hospital cardiac catheterization registry. This registry includes 81,798 coronary angiograms performed between 2000 and 2021 on 31,513 patients"; analysis on "38,691 right coronary angiography loops from 22,334 patients using the left anterior oblique (LAO) view." — [Tello Ayala et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- Prior revascularisation was not excluded: "We did not exclude patients with prior coronary revascularization 28.9% (n = 6,459) had a history of percutaneous coronary intervention and 15.5% (n = 3,455) had a history of coronary artery bypass grafting." — [Tello Ayala et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- CAD label: "The presence of CAD was obtained from the findings associated with the angiogram from which we computed the tortuosity. CAD was defined as any presence of stenosis (mild or more) in the RCA (primary analysis) ... as determined by the interventional cardiologist performing the coronary angiography." — [Tello Ayala et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- Measure: the per-point turning angle along the 2D skeleton, absolute value normalised by π, with the global score as the mean (per the earlier full-text note). "Average turning angle" is a fair plain-language name. — [Tello Ayala et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- Mean-turning-angle result, adjusted: "In a multivariable logistic regression adjusting for age, sex, hypertension, type 2 diabetes mellitus (T2DM), hypercholesterolemia, and smoking, this corresponded to an OR of 1.05 (95% CI: [1.03-1.08] P < 0.001)". — [Tello Ayala et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- Tortuosity-index result: "Using the classical tortuosity index (arc length/chord length), only age and RCA stenosis remained significant, and RCA stenosis showed a weak inverse association (β = −0.03; 95% CI: −0.06 to 0.00; P = 0.042) (Supplemental Table 10, Supplemental Figure 8)." This comes from the linear models "with tortuosity as the dependent variable" adjusted for age, sex, hypertension, T2DM, hypercholesterolemia, smoking and RCA stenosis. — [Tello Ayala et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- Agreement of the two measures: "modest agreement with the classical arc length/chord length index (Pearson r = 0.116; P < 0.001; Jaccard = 0.103 for top-decile overlap ...)". — [Tello Ayala et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- Profile vs mean: "a transformer neural network model having as inputs the full array of local tortuosity along with age and sex achieved an area under the receiver-operating characteristic curve of 0.67 (95% CI: 0.65-0.69), outperforming a logistic regression model based on mean tortuosity, age, and sex (... 0.60; 95% CI: 0.58-0.63." No DeLong or other test is reported in the main text. The Discussion nevertheless calls it "a modest but significant gain in CAD discrimination". — [Tello Ayala et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- Training data: "Tortuosity from all eligible loops was used for training the transformer model, whereas patient-level analyses used one loop per individual". The train/test partition is described only in the supplement. — [Tello Ayala et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- The authors contrast their result with earlier studies: "contrasting with smaller studies that relied on heuristic measurements of tortuosity and reported inverse or unclear associations. 18, 19". — [Tello Ayala et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- Limitations as stated: RCA only; "the retrospective design can introduce selection bias"; segmentation succeeded in 78.7% of eligible loops. — [Tello Ayala et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)

### Inferences
- Sentence 6, second half: "by the tortuosity index the same arteries were slightly less likely to [have CAD]" reverses the model.
  The paper shows that arteries with stenosis had a slightly *lower* index. The sign is equivalent in spirit, but a reader will take
  it as a CAD-outcome model. Suggested: "while arteries with stenosis had a slightly lower tortuosity index". The index result is
  also only just significant and sits in a supplement, so "slightly" is right. Do not strengthen it.
- Sentence 11 is accurate as reported. It needs its caveats, ideally in a short sentence: the difference was not tested, the
  network also differed from the comparison model in kind, and the CAD label was read from the same angiogram. The section comment
  already says "NO test of the difference"; the prose does not say so. The closing sentence only says "one study, on invasive
  angiograms".
- Population wording: "patients referred for invasive coronary angiography" is accurate (catheterisation registry). Also, part of the
  sample had already had stents or bypass, which matters for a plaque-free-baseline thesis.

### Gaps
- Supplemental Tables 10 and 12 (index regression; AUROC methodology and data split) were not opened. Whether the test patients were
  kept apart from the training loops of the same patient is unverified.

---

## Q3. Sangalli et al. 2009 (AneuRisk): FPCA on internal carotid curvature separated patients by aneurysm location?

### Takeaway
Partly. FPCA was run separately on the registered radius and curvature profiles of 65 ICAs from a neuroradiology
referral sample. The classifier that "separated" the groups (QDA) used the first two radius *and* the first two curvature
scores together. The groups were "Upper" (aneurysm at or after the terminal bifurcation, n = 33) vs "Lower" (ICA aneurysm
or none, n = 32, including 7 without aneurysm). Leave-one-out error was 21.5%, with the number of components chosen by that
same error. "The shape of the [curvature] profile separated patients by where their aneurysm lay" therefore overstates it on
two counts: radius shape was part of the separation, and the separation was partial.

### Cited Findings
- 65 patients from Niguarda Ca' Granda Hospital, Milan (2002–2005): 33 with an aneurysm at or after the ICA terminal bifurcation, 25 along the ICA, 7 "healthy"; 3D rotational angiography. — [Sangalli et al. 2009 JASA, author postprint](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf) (via earlier full-text note)
- Subjects were "suspected of being affected by cerebral aneurysms". — [Sørensen, Goldsmith, Sangalli 2013, Stat Med](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2013_Sorensen-Goldsmith-Sangalli_StatMed_compresso.pdf)
- Separate FPCA on the registered radius and curvature profiles; QDA on the first two radius plus the first two curvature scores; K chosen by minimising leave-one-out error on the same data; leave-one-out error 21.54%, apparent error 15.38%. — [Sangalli et al. 2009](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf) (via earlier full-text note)
- Upper-group ICAs were wider and more tapered, with less curvature between the two siphon peaks. — [Sangalli et al. 2009](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)

### Inferences
- Suggested rewrite: "Sangalli et al. (2009) applied FPCA to the radius and curvature profiles of the internal carotid artery,
  and the shapes of the two profiles together partly separated patients by where their aneurysm lay." This keeps it free of numbers
  and accurate. "Exploratory" is the authors' own word (in the title) and is worth keeping in mind.

### Gaps
- Not re-read today; relies on the 2026-11 full-text note.

---

## Q4. Goldsmith et al. 2011 (NeuroImage): does "used FPCA ... in most tracts the whole profile separated MS from controls better than the tract average" hold?

### Takeaway
Mostly. 115 MS cases and 42 healthy volunteers, cross-sectional, three tracts (corpus callosum, corticospinal tract,
optic radiation) and three MRI indices for case status (FA, MD, MTR). Model 3 (penalized functional regression on the
whole profile) beat Model 2 (tract average) in all three indices of the corticospinal tract and the optic radiation on the
test set, and in all three corpus-callosum indices it did worse. So "most tracts" means two of three. No test of the AUC
difference is reported. The NeuroImage paper itself never names FPCA: its method description says "PFR uses a large spline
basis for β(p)". FPCA enters only through the PFR method paper, which projects the predictor "onto a large number of smooth
eigenvectors". "Used FPCA" is therefore defensible but indirect.

### Cited Findings
- "a cross-sectional MRI and functional study of 115 multiple-sclerosis cases and 42 healthy volunteers ... using training and testing sets to validate the results. We show that attention to spatial variation yields up to 15% (mean across all tracts and MRI indices: 6.4%) improvement in the ability to discriminate multiple sclerosis cases from healthy volunteers." — [Goldsmith et al. 2011 NeuroImage, PMC3114268](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268/)
- Models: "Model 1 includes age, sex, and whole-brain MRI index; Model 2 adds the tract-specific index average; and Model 3 is the full PFR model". — [Goldsmith et al. 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268/)
- Table 2 (AUC, training LOO; test in parentheses), Model 2 → Model 3:
  - corticospinal tract: FA .73(.67)→.80(.70); MD .78(.74)→.80(.76); MTR .71(.65)→.73(.72)
  - corpus callosum: FA .68(.80)→.78(.73); MD .73(.86)→.80(.78); MTR .65(.77)→.72(.71)
  - optic radiation: FA .74(.67)→.79(.77); MD .78(.74)→.81(.80); MTR .71(.65)→.69(.69)
  - On training (LOO), Model 3 is better in 8 of 9; on the test set, in 6 of 9 (worse in all corpus-callosum indices).
  — [Goldsmith et al. 2011, Table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268/)
- "Note that for the CC, the performance of Model 2 is substantially improved on the test set, where it in fact outperforms Model 3. This instability is a result of the small test set for the CC, containing 9 healthy volunteers and 24 MS cases". — [Goldsmith et al. 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268/)
- Smoothing was tuned on the outcome: "We choose the level of smoothness to maximize the area under the leave-one-out, cross-validated ROC curve". The training-set AUCs of Model 3 are therefore optimistic. — [Goldsmith et al. 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268/)
- Method text: "PFR uses a large spline basis for β(p) and explicitly induces smoothness via standard mixed-effects models and cross-validation." FPCA is mentioned only as Greven et al.'s related work. — [Goldsmith et al. 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268/)
- PFR method paper: "The functional predictor is projected onto a large number of smooth eigenvectors and the coefficient function is estimated using penalized spline regression". — [Goldsmith, Bobb, Crainiceanu, Caffo, Reich 2011, J Comput Graph Stat, PMC3285536](https://doi.org/10.1198/jcgs.2010.10007)
- Mean-centring for case status uses the healthy-volunteer mean profile. — [Goldsmith et al. 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268/)

### Inferences
- Suggested rewrite: "Subsequently, Goldsmith et al. (2011) related a tissue property measured along white-matter tracts of the brain
  to multiple sclerosis with a functional regression built on FPCA, and in two of the three tracts the whole profile separated
  patients from healthy volunteers better than the tract average." "Two of the three" is a number. If the chapter rule forbids it,
  keep "in most tracts" but add "with a functional regression built on FPCA" instead of "used FPCA".
- The contrast is a strong case-control one (established MS vs volunteers), so this shows that the method can work, not that it
  predicts incident disease. The closing sentence's "carry information on disease" is fine.

### Gaps
- Exact appendix of the NeuroImage paper (the PFR details) was not in the PMC text.

---

## Q5. Is "different summaries have been used and none has been agreed" supported by the four cited papers?

### Takeaway
Half. "Different summaries have been used" is supported by Kashyap (explicitly), Li (bend rule) and Tello Ayala
(mean turning angle vs arc/chord, r = 0.116). Grisan 2008 is about **retinal** vessels on 2D fundus photographs, so it does
not support a claim "for curvature in coronary arteries". "None has been agreed" is supported only by implication:
Kashyap blames the "ambiguous findings in the literature" on the use of different metrics and *recommends* one, which shows
there was no standard. None of the four states outright that there is no consensus. Reviews say this more directly.

### Cited Findings
- Kashyap 2022: "Several previous studies considered different tortuosity metrics when exploring its impact of on the wall shear stress (WSS), which has likely contributed to the ambiguous findings in the literature"; "The tortuosity index, the most widely used measure in literature, showed no significant correlation to low TAWSS (p = 0.86). We thus recommend the use of average-absolute-curvature as a tortuosity measure for future studies." — [Kashyap et al. 2022, Sci Rep, PMC8764056](https://doi.org/10.1038/s41598-022-04796-w)
- Tello Ayala 2026: earlier metrics (Tortuosity Index, Sum-of-Angles, Inflection-Count Metric) "provide reproducible scalar values, yet their reliance on global quantities ... leads to oversight of local morphological cues"; agreement with arc/chord r = 0.116. — [Tello Ayala et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- Grisan 2008: retinal tortuosity; arc/chord − 1 *falls* as turns are added at equal |curvature| and length (Fig. 11), and different measures respond differently to bend number and amplitude; the reference was one specialist's ranking of 30 arteries and 30 veins. — [Grisan et al. 2008, IEEE TMI](https://doi.org/10.1109/TMI.2007.904657) (via earlier full-text note)
- Kahe et al. 2020 narrative review of coronary artery tortuosity (Coronary Artery Disease, DOI 10.1097/MCA.0000000000000769) covers the definitions and clinical meaning of coronary tortuosity and calls it "a benign entity" in general. Only the abstract was read. — [Kahe et al. 2020](https://doi.org/10.1097/MCA.0000000000000769)
- Ciurică et al. 2019, "Arterial Tortuosity: Novel Implications for an Old Phenotype", Hypertension 73:951–960 (review). The abstract was not available in this check. — [PubMed 30852920](https://pubmed.ncbi.nlm.nih.gov/30852920/)
- A 2025 systematic review (Int J Morphol) reportedly states that there is no consensus on the definition, classification or measurement of arterial tortuosity. This is from a search snippet only, not read. — [Int J Morphol 2025 PDF](https://intjmorphol.com/wp-content/uploads/2025/11/Art_43_435_2025.pdf)

### Inferences
- Move grisan2008tortuosity to sentence 2 (the general point that a summary keeps only some aspects of the profile; Grisan shows
  arc/chord and bend-based measures react differently to bend number and amplitude). Or drop it, since the comment already notes
  it is otherwise uncited.
- For "none has been agreed", Kashyap is the best coronary support already in refs.bib. If a direct statement is wanted, read and
  cite Ciurică 2019 or Kahe 2020 after a full-text check. Do not cite the Int J Morphol review without reading it (small journal).
- A safer wording that the four (three) cites fully support: "For curvature in coronary arteries, studies have used different
  summaries, and these summaries agree poorly with each other."

### Gaps
- Ciurică 2019 and Kahe 2020 full texts were not read; whether they state "no consensus" explicitly is unverified.

---

## Q6. Other claims and section-level improvements

### Takeaway
The second paragraph's headline ("the choice of curvature summary has even decided the direction of the association")
is the main overstatement. Across studies, Li and Tello Ayala differ in country, era, vessels, CAD definition (≥50% vs any
stenosis) and measure, so the measure cannot be singled out. Within Tello Ayala the two measures gave opposite signs on the
same arteries, which supports a softer claim. Ramsay 2005 supports the FPCA sentence, but not the bend-sharpness example
or the "biological structures" framing.

### Cited Findings
- Li CAD = "≥50% luminal narrowing in at least one main coronary artery"; Tello Ayala CAD = "any presence of stenosis (mild or more) in the RCA". — [Li 2011](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0024232); [Tello Ayala 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- Tello Ayala itself attributes the difference from earlier inverse findings to "smaller studies that relied on heuristic measurements of tortuosity", i.e. to the measure *and* to the sample size. — [Tello Ayala 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- PFR and FPCA as general tools: the PFR method paper describes the eigenvector projection; Ramsay and Silverman ch. 8 covers functional PCA. — [Goldsmith et al. 2011 JCGS](https://doi.org/10.1198/jcgs.2010.10007); [Ramsay & Silverman 2005](https://doi.org/10.1007/b98888)

### Inferences (concrete improvements; the prose is not edited)
- **Sentence 2 (ramsay2005fda):** Ramsay does not discuss bend sharpness vs bend count. Either cite Grisan 2008 for the bend example
  (it shows exactly that arc/chord and turn counts respond differently to bend number and amplitude, in retinal vessels) and Ramsay only
  for the general principle, or drop "common challenge in the analysis of biological structures" (unsupported framing).
- **Sentence 3:** remove grisan2008tortuosity from the coronary claim (retinal). Consider "studies have used different summaries,
  which agree poorly" (supported by Kashyap and Tello Ayala) instead of "none has been agreed". Cite order chronologically:
  li2011, kashyap2022, telloayala2026.
- **Sentence 4:** soften to "In clinical studies of the coronary arteries, the direction of the association with CAD has differed
  between summaries", or "even in the same arteries, two summaries have pointed in opposite directions" (Tello Ayala). Avoid "decided",
  which implies causation from a two-study contrast.
- **Sentence 5 (Li):** replace "counted sharp bends ... patients with more such bends" with the binary rule ("classed an artery as
  tortuous when it had at least three sharp bends"). Optionally add that the association was weak. "CAD" in Li is obstructive disease.
- **Sentence 6 (Tello Ayala):** "while arteries with stenosis had a slightly lower tortuosity index" instead of "slightly less likely to".
  Add "patients referred for invasive angiography" if the population is not stated in the table.
- **Sentence 9 (Sangalli):** "radius and curvature profiles ... together partly separated". It is cross-sectional and from referred patients.
- **Sentence 10 (Goldsmith):** "with a functional regression built on FPCA" instead of "used FPCA"; "in most tracts" is acceptable (two of three).
- **Sentence 11 (Tello Ayala profile):** add one short caveat sentence: the difference was not tested, and the CAD label came from
  the same angiograms. This is already flagged in the file's comments but missing in the prose.
- **Sentence 8:** "common" is best supported by ullah2013fda (FPCA in 51 of 84 applied FDA studies, already verified per the
  comments); re-add that cite beside ramsay2005fda.
- **Chronology:** paragraph 2 (2011 → 2026) and paragraph 3 (2009 → 2011 → 2026) are already in order.
- **Style:** the tortuosity index is still undefined in the review (OPEN in the file). If a definition is not allowed here, "the
  ratio of arc length to chord length" in parentheses on first use would be a minimal fix. No lists or em dashes found in the prose.
- **Missing studies (worth considering):** Kahe 2020 (coronary tortuosity review) or Ciurică 2019 (arterial tortuosity review) as a
  direct source for the lack of an agreed definition; Passerini et al. 2012 (Cardiovasc Eng Technol, AneuRisk CFD + FPCA follow-up)
  as a second vascular FPCA example; Groves 2009 is already in sec:lit-wss/table. No peer-reviewed FPCA of coronary curvature
  profiles was found in this or earlier searches. The one coronary FPCA-type work found earlier is an arXiv preprint (2411.18398,
  diameter curves), not suitable for the review.

### Gaps
- Whether a coronary study has compared several curvature summaries against plaque or CAD *in the same cohort* (beyond Tello Ayala,
  and Kashyap against WSS rather than disease) was not searched exhaustively here.
