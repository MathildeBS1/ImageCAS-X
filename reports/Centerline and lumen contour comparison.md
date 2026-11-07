# Validate the tracer at the feature level

The best comparison is a **two-layer design that ends at the features the risk model uses**. The first layer is a per-path, Schaap-style centerline comparison. It uses a monotone point correspondence, overlap labels relative to the local radius, and OV/OF/OT plus AI ([Schaap 2009](https://cdr.lib.unc.edu/downloads/cn69mc016)). It establishes that both methods traced the same vessel, defines the common stretch, and gives the pairing that everything downstream needs. The second layer is a cross-section comparison of lumen area (equivalent radius) on Medis contours paired through that correspondence. The **primary endpoint** is agreement on the per-artery features themselves: curvature, taper, the LM bifurcation angle, and the LM→LAD and LM→LCx ratios. It is reported as Bland–Altman bias and 95% limits of agreement, with ICC(A,1) secondary. This design is defensible for three reasons. Every step has a published coronary precedent. The comparison sits in one CT volume and one LPS frame, so no registration is needed. And the thesis needs to know whether the tracer can **rank people** on geometry, not whether it reproduces a single reader's contours. Three facts limit what the validation can claim. Medis is a single-reader clinical reference, not a multi-observer consensus. Its contours exist only in diseased segments. And nearly all Medis patients had plaque at baseline. The results are therefore inter-method agreement in a shifted domain. They carry over to the plaque-free cohort only through an explicit, assumption-laden reliability argument. Leave out the inter-observer scoring, 3D surface meshing, Hausdorff as a headline number, Lin's CCC next to ICC, Pearson r, and any correction for measurement error.

## Schaap's correspondence is the backbone, with three adaptations

The Rotterdam framework (CAT08) is still the coronary centerline standard. Later coronary benchmarks evaluate stenosis or lumen segmentation instead: Kirişli 2013 ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1361841513000819)) and ASOCA, which uses Dice and HD95 ([ASOCA](https://asoca.grand-challenge.org/)). Recent centerline methods still report CAT08 metrics ([Wolterink 2019](https://arxiv.org/pdf/1810.03143)).

**How the correspondence works.** Schaap resamples both lines at **0.03 mm**. The evaluated line is clipped at a disc placed at the reference start, with radius twice the reference radius and normal equal to the reference tangent. The correspondence is the ordered set of point–point connections with minimal total Euclidean length. It runs from start to start and end to end, and each step advances one index on one curve. Dijkstra finds the optimum, so in effect it is dynamic time warping with a sum-of-distances cost. Every point on each curve is connected to at least one point on the other ([Schaap 2009](https://cdr.lib.unc.edu/downloads/cn69mc016)).

**Point labels and metrics.**
- A reference point is a true positive if a connected evaluated point lies within the **local reference radius**; otherwise it is a false negative. Evaluated points are labelled the same way: within a connected reference point's radius is a true positive, otherwise a false positive.
- **OV** is the Dice-like overlap of all labelled points.
- **OF** is overlap until the first error, ignoring errors in the first 5 mm.
- **OT** restricts overlap to the part of the vessel with diameter ≥ 1.5 mm.
- **AI** is the mean connection length over connections inside the radius.
- Schaap separates *capability* (overlap) from *accuracy* (distance). In his words, "in case of a tracking failure the magnitude of the distance to the reference centerline is no longer relevant" ([Schaap 2009](https://cdr.lib.unc.edu/downloads/cn69mc016)).

**Benchmark values.** On the CAT08 test set, a strong CNN tracker reached OV 93.7%, OF 81.5%, OT 97.0% and AI 0.21 mm. The inter-observer difference was about 0.20 mm. The typical failures were stopping early at myocardial bridges and continuing distally into adjacent vessels ([Wolterink 2019](https://arxiv.org/pdf/1810.03143)).

**Why the monotone correspondence and not the alternatives.** No paper benchmarks the alternatives against each other, so this is reasoning, not evidence.
- Nearest-point matching ignores order and can jump to a neighbouring vessel.
- Matching by arc length from the ostium drifts distally whenever one line is longer or noisier.
- The monotone correspondence keeps order, tolerates different sampling, and is the published coronary convention.

It requires single ordered paths. Run it **per path**, from the ostium to the distal end of the LAD, LCx and RCA trunks, not on the whole tree.

**Three adaptations are necessary.**

*No inter-observer scoring.* Medis has one reader, so Schaap's scores relative to inter-observer variability (100 = perfect, 50 = observer level) cannot be reproduced. Report raw OV/OT/AI only. Interpret any disagreement as the combined error of both methods ([Schaap 2009](https://cdr.lib.unc.edu/downloads/cn69mc016)).

*A fallback for the radius threshold.* Schaap's threshold is the annotated radius at each reference point. Medis contours exist only in diseased segments, so many trunk points will have no Medis radius.
- Where a Medis contour exists, use its equivalent radius.
- Elsewhere, use the tracer's own per-step radius as the fallback.
- Keep a fixed threshold (for example 1.5 mm) as a sensitivity check.

The fallback is my design choice, not a published rule. State it.

*Distal endpoints.* Medis readers probably checked only the contoured, diseased part of each tree (project data notes). So distal Medis reach may be arbitrary, and false positives beyond the Medis end are not trustworthy errors.
- Report reference-side recall (the share of the Medis path that the tracer covered) and OT.
- Report accuracy (AI) on the **common stretch**: from the disc-clipped ostium to the shorter of the two distal ends, mapped through the correspondence.
- Treat difference in distal reach as a separate descriptive number, not as error.

This is reasoning, not sourced. It follows the carotid practice of fixing start and end landmarks so that every package measures the same stretch ([de Vries 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6348067/)). Report OF only if space allows: its 5 mm ostial tolerance exists because the start "is sometimes difficult to define" ([Schaap 2009](https://cdr.lib.unc.edu/downloads/cn69mc016)).

**Hausdorff and HD95 stay supplementary.** On a centerline they mostly record a single wrong-branch excursion or a length difference ([ASOCA](https://asoca.grand-challenge.org/) uses them for surfaces, not paths).

## Frames, resampling and labels must be fixed before any metric

**Frames.** Most comparison bugs happen before the comparison starts. DICOM and ITK use LPS. 3D Slicer works in RAS internally and assumes files are LPS. The two differ by a sign flip of the first two axes ([Slicer docs](https://slicer.readthedocs.io/en/5.6/user_guide/coordinate_systems.html)). Mesh formats have no standard axis convention ([Slicer data docs](https://slicer.readthedocs.io/en/5.6/user_guide/data_loading_and_saving.html)). So the steps are:
1. Map the tracer's voxel indices to world mm with the NIfTI affine.
2. Convert explicitly to LPS to match Medis.
3. Overlay both lines on the CT for a handful of cases.
4. Use a gross gate before any metric, for example a median centerline distance below about 1 mm. This threshold is a design choice.

**Resampling and smoothing.** Resample both lines by arc length: about 0.03–0.1 mm for the correspondence, following Schaap's 0.03 mm, and a fixed coarser spacing for the features. Apply the **same smoothing scale to both methods** before computing curvature. Raw tracker spacing is not uniform; Wolterink's step size depends on the radius ([Wolterink 2019](https://arxiv.org/pdf/1810.03143)). In curvature and torsion landmarking of the internal carotid, centerline resolution was the parameter that most strongly over- or under-segmented bends ([BioMed Eng OnLine 2021](https://dx.doi.org/10.1186/s12938-021-00957-6)). A cross-device retinal preprint found that curvature-based tortuosity had the widest ICC intervals, because "curvature is not scale invariant" ([arXiv:2602.08580](https://arxiv.org/pdf/2602.08580), preprint). No coronary-specific study of scale dependence was found, so this evidence is carotid, cerebral and retinal by analogy. Fix the bifurcation angle the same way: use one tangent-fitting distance from the branch point, identical for both methods.

**Label checking.** Segment labels matter as much as the line itself. The proximal/mid/distal boundaries are set by side-branch landmarks, so a shifted boundary changes per-segment length and curvature even when the two lines coincide (reasoning). Lugauer's lumen evaluation shows the cost of a labelling mismatch between centerline and reference. In 7 datasets it produced "a large error bias", worst for surface distances in healthy vessels ([Lugauer 2014](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf)).

The closest precedent for the label check comes from the Medis/LKEB group itself (Cao 2017). It labelled AHA/SCCT segments and reported **label overlap along the centerline**: same-label length divided by matched length. Mean label overlap was 92.0% in right-dominant and 90.7% in left-dominant cases, and results were split by dominance ([Cao 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5677991/)). Labelling papers with unbalanced classes use per-label precision, recall and F1 with macro averages ([CPR-GCN](https://openaccess.thecvf.com/content_CVPR_2020/papers/Yang_CPR-GCN_Conditional_Partial-Residual_Graph_Convolutional_Network_in_Automated_Anatomical_Labeling_CVPR_2020_paper.pdf); [TopoLab](https://arxiv.org/pdf/2307.11959)). For the lean version, report three things:
- Cao-style label overlap per trunk segment;
- a 9 × 9 confusion matrix of tracer against Medis labels;
- the offset along the arc between corresponding segment boundaries.

Split all three by dominance.

## Lumen agreement belongs on paired cross-sections

**Why cross-sections rather than surfaces.** Medis supplies discrete cross-sectional contours, the tracer predicts one contour per step, and the downstream features are per-section radii. A cross-section comparison therefore fits the data. Meshing both into surfaces would add interpolation choices and mix in disagreement about the centerline and the branch labels. Lugauer found surface distances more sensitive to labelling mismatch than Dice ([Lugauer 2014](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf)). The Rotterdam lumen reference was itself drawn as cross-sectional contours on one shared set of centerlines ([Lugauer 2014](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf)).

**Pairing contours.** CT–IVUS work needs landmark registration across modalities ([Boogers 2012](https://pubmed.ncbi.nlm.nih.gov/22285583/); [Radunović 2023](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2023.1292517/full)). Here both methods segment the same volume, so the only problem is that the two centerlines differ. The recipe below is mostly geometric reasoning, not a published protocol.
1. Map each Medis contour (centroid plus plane) through the centerline correspondence to its tracer step.
2. Gate each pair on centroid distance (for example below about 1 mm or one lumen radius).
3. Gate each pair on the angle between the plane normals (for example below 15–20°). An oblique cut inflates area by roughly 1/cos θ. Alternatively, reslice the tracer lumen on the Medis plane.
4. Clean each contour: close it, give it a consistent orientation, and remove duplicate points.
5. Compute the area with the shoelace formula in plane coordinates, and r_eq = √(A/π).

No source prescribes these thresholds. Prespecify them, and report how many pairs each gate rejects.

**Which metrics.** The primary per-section metric is **r_eq (or area) agreement**. Report Dice and mean contour distance per section as secondary shape descriptors only. These benchmarks show what disagreement to expect:

| Comparison (Rotterdam test set) | Dice diseased / healthy | Mean surface distance |
|---|---|---|
| Each expert vs the others | 65–79% / 72–81% | 0.21–0.34 mm |
| Best automatic method | 76% / 75% | 0.32 / 0.51 mm |

Source: [Lugauer 2014, Table 1](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf).

The table shows that two human readers disagree substantially on CT lumen borders, so a gap between the tracer and Medis is not, on its own, a sign that the tracer fails. Older QAngio CT validations against IVUS lead with Pearson r (for example MLA r = 0.75) ([Boogers 2012](https://pubmed.ncbi.nlm.nih.gov/22285583/)). That is association, not agreement.

**Where bias matters for taper and ratios.** A constant bias in r_eq cancels in taper (a slope) and largely cancels in the diameter ratios. A proportional or position-dependent bias does not. So regress the Bland–Altman difference on the pair mean and on arc position; that check is more informative than Dice (reasoning).

**Plaque and bifurcations need their own strata.** Rotterdam reports healthy and diseased segments separately, and expert disagreement was larger in diseased segments ([Lugauer 2014](https://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2014/Lugauer14-PLS.pdf)). Bifurcation work anchors at the carina, uses a ±5 mm window, and excludes heavy calcification because calcium blooming hides the lumen border ([Radunović 2023](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2023.1292517/full)). No standard exclusion distance exists, so the 3–5 mm zone is borrowed, not validated. Prespecify three things:
- an exclusion zone around the LM carina and the side-branch ostia;
- LM→LAD and LM→LCx radii at a fixed offset beyond that zone, identical for both methods;
- strata of cross-sections: no plaque (Medis lumen ≈ outer wall), plaque, and near a bifurcation.

The **no-plaque stratum** comes closest to the plaque-free outcome cohort.

**Expect a smaller n for the ratios.** Contours exist only in diseased segments, so a ratio can be validated only where Medis contoured both the LM and the proximal daughter. Report that n explicitly.

## Clustered statistics must respect persons, and the LoA must lead

**Bland–Altman definition.** The 95% limits of agreement (LoA) are the mean paired difference ± 1.96 SD. They are "expected to contain the difference between measurements by the two methods for 95% of pairs of future measurements on similar individuals" ([Bland & Altman 2007](https://www-users.york.ac.uk/~mb55/meas/bland2007.pdf)). The method assumes:
- a bias and spread that are stable across the range;
- independent pairs;
- roughly normal differences.

Plot the difference against the mean of the two methods, never against the reference. Plotting against the reference correlates the difference with the x-axis by construction ([Bland, diffplot](https://www-users.york.ac.uk/~mb55/meas/diffplot.htm)). If the spread grows with size, log-transform the data; the antilogged limits are then limits for the *ratio* of the methods. If the bias or SD trends with size in some other way, use regression LoA ([Bland, glucose example](https://www-users.york.ac.uk/~mb55/meas/glucose.htm)).

**Choosing the scale per feature** (reasoning):
- **radius**: log scale, which gives percentage limits from the proximal to the distal trunk;
- **curvature**: log scale, since it is positive and right-skewed;
- **taper**: plain or regression LoA, since it can be zero or negative.

**Repeated measures.** Cross-sections are nested in arteries, and arteries are nested in persons. If you pool all pairs, or average to one pair per person, the limits come out too narrow. That would "lead us to think that methods of measurement agreed more closely than they actually do" ([Bland & Altman 2007](https://www-users.york.ac.uk/~mb55/meas/bland2007.pdf)).
- Bland & Altman's varying-true-value model sums the between-subject and within-subject variance components ([Bland & Altman 2007](https://www-users.york.ac.uk/~mb55/meas/bland2007.pdf)).
- The general form is a mixed model on the differences, available as `SimplyAgree::loa_lme` ([CRAN](https://search.r-project.org/CRAN/refmans/SimplyAgree/html/loa_lme.html); [Parker 2016](https://ideas.repec.org/a/plo/pone00/0168321.html)).
- For cross-sections, fit d = μ + u_person + v_artery + ε, with LoA = μ ± 1.96√(σ²_u + σ²_v + σ²_ε).
- Bland & Altman leave autocorrelation explicitly unresolved ([Bland & Altman 2007](https://www-users.york.ac.uk/~mb55/meas/bland2007.pdf)), and consecutive cross-sections are autocorrelated. Subsample at roughly one lumen diameter, and get CIs by a **person-level cluster bootstrap**, which matches the thesis's person-split logic (reasoning).
- For the per-artery features there is one pair per artery, so classical LoA **per artery type** is the simplest defensible choice. It also respects the project's per-artery convention.

**ICC as a secondary.** Bland & Altman argue against the ICC as the primary measure of agreement ([Dore et al.](https://discovery.ucl.ac.uk/id/eprint/10097012/3/Dore_Ophthalmic%20statistics%20note%2014_AAM.pdf)). Report it as a secondary, and state its form: model, type and unit ([Koo & Li 2016](https://pmc.ncbi.nlm.nih.gov/articles/4913118)). The two relevant forms are two-way single-measure ICCs ([psych::ICC](https://personality-project.org/r/html/ICC.html)):
- **ICC(A,1)**, absolute agreement, which penalises a systematic offset;
- **ICC(C,1)**, consistency, which ignores an additive offset.

Use ICC(A,1) as the agreement summary. Add ICC(C,1) only if you want to frame the result as ranking consistency, and say that it is not agreement. CCC is close to ICC(A,1), so reporting both is redundant ([GenStat](https://genstat.kb.vsni.co.uk/knowledge-base/lconcord/)). Pearson r is invariant to location and scale shifts, so it cannot show agreement ([Bland & Altman 1986, York copy](https://www-users.york.ac.uk/~mb55/meas/ba.htm)).

**Lean reporting set:**

| Layer | Report | Leave out |
|---|---|---|
| Centerline | OV, OT, reference-side recall; AI on the common stretch (median, IQR by person); reach difference | Inter-observer scores, HD as headline, FP beyond the Medis end as error |
| Labels | Label overlap per segment, 9 × 9 confusion matrix, boundary offset, by dominance | Topology metrics, macro-F1 tables |
| Contour | r_eq LoA (log scale, mixed model), stratified; Dice and mean contour distance secondary | 3D surface metrics, MLA and stenosis, MAXSD |
| Features (primary) | Per-artery LoA and ICC(A,1) with CI for curvature, taper, LM angle, LM→LAD and LM→LCx ratios; n and exclusions | CCC, Pearson r, Koo–Li labels as verdicts |

## Transfer to the plaque-free cohort needs an explicit reliability argument

**Use the right words.** Medis is a reader-edited reference, so the result is **inter-method agreement**, not accuracy. Benchmark papers call expert annotation a "reference standard" ([Schaap 2009](https://research.rug.nl/en/publications/standardized-evaluation-methodology-and-reference-database-for-ev/)). STAPLE starts from the premise that the true segmentation is unknown and notes "a tradeoff between the accuracy and realism of the reference standard" ([Warfield 2004](https://pmc.ncbi.nlm.nih.gov/articles/PMC1283110)). GRRAS gives a 15-item reporting checklist for agreement studies ([Kottner 2011](https://researchprofiles.ku.dk/en/publications/guidelines-for-reporting-reliability-and-agreement-studies-grras--4/)).

**Why the ICC does not transfer.** The ICC is a ratio of between-subject variance to total variance. It therefore depends on how spread out the sample is, and an ICC from plaque patients does not carry over to a plaque-free cohort with different spread (formula reasoning, consistent with [Bland & Altman 1990](https://www-users.york.ac.uk/~mb55/meas/comref.htm)). The LoA are on the measurement scale and do not depend on that spread, provided the error is homogeneous. This is the main reason to make **LoA the primary result**.

**Link to the risk model.** Random error in a predictor attenuates its coefficient by the reliability ratio λ = σ²_true / σ²_observed ([Hutcheon 2010](https://emj.bmj.com/lookup/ijlink/YTozOntzOjQ6InBhdGgiO3M6MTQ6Ii9sb29rdXAvaWpsaW5rIjtzOjU6InF1ZXJ5IjthOjQ6e3M6ODoibGlua1R5cGUiO3M6NDoiRlVMTCI7czoxMToiam91cm5hbENvZGUiO3M6MzoiYm1qIjtzOjU6InJlc2lkIjtzOjE3OiIzNDAvanVuMjNfMi9jMjI4OSI7czo0OiJhdG9tIjtzOjIyOiIvZW1lcm1lZC8zMy81LzMwNy5hdG9tIjt9czo4OiJmcmFnbWVudCI7czowOiIiO30=); [Rutter, PMC6857752](https://pmc.ncbi.nlm.nih.gov/articles/PMC6857752)). In logistic regression this holds approximately ([Carroll 2006](https://www.routledge.com/Measurement-Error-in-Nonlinear-Models-A-Modern-Perspective/Carroll-Ruppert-Stefanski-Crainiceanu/p/book/9781584886334)). The bound below is my own reasoning, with no source for transporting it between populations:
1. Assume the tracer and Medis errors are independent. Then Var(d) = σ²_e,T + σ²_e,M, so σ²_e,T ≤ Var(d).
2. Combine this with the observed spread of the tracer feature in the ~1,200 plaque-free people: λ_T ≥ 1 − Var(d) / Var_obs,target.
3. The bound holds only if the tracer's error variance is the same in plaque-free and plaque patients.

The bound breaks in one specific way. Both methods read the same volume, so motion, blooming and partial volume affect both, and those shared errors make agreement overstate accuracy. Assumption 1 then fails, and so does the bound.

**What the attenuation does to the *who* test.** Random, non-differential error lowers power and ΔC but does not create associations. Error that depends on subclinical disease could do so. Name this as a limitation.

**Expect λ to differ by feature.** Curvature amplifies noise, and taper is a slope over a short length. Both are therefore likely to have lower λ than length (reasoning).

**Do not call the validation conservative.** Plaque-free trunks are probably easier to trace, so errors measured in diseased Medis segments may be an upper bound. But this is a hypothesis: the reader's contours in plaque are also less certain. Write it as a limitation, not as a guarantee.

## Conclusion

The validation's real job is narrow. It must show that tracer geometry varies between people more than it disagrees with Medis. Contour fidelity is secondary to that. This reframing has three consequences:
- The Schaap correspondence matters mainly as the mechanism that defines the common stretch and pairs the cross-sections. As a scoreboard it matters less.
- The decisive tables are per-artery feature LoA, set against the between-person SD of each feature in the plaque-free cohort. If a feature's LoA are wide relative to that SD, the tracer cannot rank people on it, whatever OV it scores.
- The cheapest addition with the highest value is the **no-plaque stratum** of Medis cross-sections. It is the only part of the reference that resembles the target cohort.

Several things could not be verified from the notes, and they mark where the evidence is thin:
- No published study compares an automatic tracer's contours with Medis contours in the same CT.
- No coronary inter-software study of curvature agreement was found.
- No source covers moving a reliability estimate from one population to another.

The thesis should say all three plainly rather than borrow certainty from the CAT08 benchmark.

## Reference list (BibTeX-ready)

Verification flags: **[V]** means the bibliographic record was checked in the notes against an index or repository page. **[DOI?]** means the DOI or another detail is from memory and must be checked before use. **[abs]** means the content was confirmed only from the abstract or secondary sources.

```bibtex
@article{schaap2009standardized,
  author  = {Schaap, Michiel and Metz, Coert T. and van Walsum, Theo and van der Giessen, Alina G. and Weustink, Annick C. and Mollet, Nico R. and Bauer, Christian and Bogunovi{\'c}, Hrvoje and Castro, Carlos and Deng, Xiang and Dikici, Engin and O'Donnell, Thomas and Frenay, Michel and Friman, Ola and Hern{\'a}ndez Hoyos, Marcela and Kitslaar, Pieter H. and Krissian, Karl and K{\"u}hnel, Caroline and Luengo-Oroz, Miguel A. and others and Niessen, Wiro J.},
  title   = {Standardized evaluation methodology and reference database for evaluating coronary artery centerline extraction algorithms},
  journal = {Medical Image Analysis}, year = {2009}, volume = {13}, number = {5}, pages = {701--714},
  doi     = {10.1016/j.media.2009.06.003}
}
% [V] full text read (author manuscript); the middle authors are truncated in the notes, so complete the list.
% The OV formula was reconstructed from the text, as the formula image did not extract. Quote it carefully.

@article{wolterink2019coronary,
  author  = {Wolterink, Jelmer M. and van Hamersvelt, Robbert W. and Viergever, Max A. and Leiner, Tim and I{\v{s}}gum, Ivana},
  title   = {Coronary artery centerline extraction in cardiac {CT} angiography using a {CNN}-based orientation classifier},
  journal = {Medical Image Analysis}, year = {2019}, volume = {51}, pages = {46--60},
  doi     = {10.1016/j.media.2018.10.005}, eprint = {1810.03143}, archivePrefix = {arXiv}
}
% Full text read (arXiv). [DOI?] the DOI was not shown on the fetched page.

@article{kirisli2013standardized,
  author  = {Kiri{\c{s}}li, H. A. and Schaap, M. and Metz, C. T. and Dharampal, A. S. and Meijboom, W. B. and others},
  title   = {Standardized evaluation framework for evaluating coronary artery stenosis detection, stenosis quantification and lumen segmentation algorithms in computed tomography angiography},
  journal = {Medical Image Analysis}, year = {2013}, volume = {17}, number = {8}, pages = {859--876},
  doi     = {10.1016/j.media.2013.05.007}
}
% [abs] full text not read; DOI inferred from the PII. The full author list and the metric definitions are unverified.

@inproceedings{lugauer2014precise,
  author    = {Lugauer, Felix and Zheng, Yefeng and Hornegger, Joachim and Kelm, B. Michael},
  title     = {Precise lumen segmentation in coronary computed tomography angiography},
  booktitle = {Medical Computer Vision: Algorithms for Big Data (MCV, MICCAI workshop)},
  series    = {Lecture Notes in Computer Science}, publisher = {Springer}, year = {2014},
  doi       = {10.1007/978-3-319-13972-2_13}
}
% Full text read (PDF). [DOI?] check the volume number and pages. This is a workshop paper.

@article{cao2017automatic,
  author  = {Cao, Qing and Broersen, Alexander and de Graaf, Michiel A. and Kitslaar, Pieter H. and Yang, Guanyu and Scholte, Arthur J. and Lelieveldt, Boudewijn P. F. and Reiber, Johan H. C. and Dijkstra, Jouke},
  title   = {Automatic identification of coronary tree anatomy in coronary computed tomography angiography},
  journal = {The International Journal of Cardiovascular Imaging}, year = {2017}, volume = {33}, number = {11}, pages = {1809--1819},
  doi     = {10.1007/s10554-017-1169-0}
}
% [V] PMC5677991.

@inproceedings{yang2020cprgcn,
  author    = {Yang, Han and Zhen, Xingjian and Chi, Ying and Zhang, Lei and Hua, Xian-Sheng},
  title     = {{CPR-GCN}: Conditional Partial-Residual Graph Convolutional Network in Automated Anatomical Labeling of Coronary Arteries},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)}, year = {2020}
}
% [DOI?] the author list is from memory; verify it. Optional citation.

@article{devries2019comparability,
  author  = {de Vries, Eline E. and Pourier, Vanessa E. C. and van Laarhoven, Constant J. H. C. M. and Vonken, Evert-Jan and van Herwaarden, Joost A. and de Borst, Gert J.},
  title   = {Comparability of semiautomatic tortuosity measurements in the carotid artery},
  journal = {Neuroradiology}, year = {2019}, volume = {61}, number = {2}, pages = {147--153},
  doi     = {10.1007/s00234-018-2112-3}
}
% [V] PMC6348067. Note the small sample (n = 12).

@article{radunovic2023bifurcation,
  author  = {Radunovi{\'c}, A. and Vidakovi{\'c}, R. and Tim{\v{c}}i{\'c}, S. and others},
  title   = {Multislice computerized tomography coronary angiography can be a comparable tool to intravascular ultrasound in evaluating ``true'' coronary artery bifurcations},
  journal = {Frontiers in Cardiovascular Medicine}, year = {2023}, volume = {10}, pages = {1292517},
  doi     = {10.3389/fcvm.2023.1292517}
}
% Full text read. Its abstract and tables are internally inconsistent, so cite it only for the carina +/- 5 mm and calcium-exclusion conventions.

@article{boogers2012automated,
  author  = {Boogers, Mark J. and Broersen, Alexander and van Velzen, Joella E. and de Graaf, Fleur R. and El-Naggar, Heba M. and Kitslaar, Pieter H. and Dijkstra, Jouke and Delgado, Victoria and Boersma, Eric and de Roos, Albert and Schuijf, Joanne D. and Schalij, Martin J. and Reiber, Johan H. C. and Bax, Jeroen J. and Jukema, J. Wouter},
  title   = {Automated quantification of coronary plaque with computed tomography: comparison with intravascular ultrasound using a dedicated registration algorithm for fusion-based quantification},
  journal = {European Heart Journal}, year = {2012}, volume = {33}, number = {8}, pages = {1007--1016},
  doi     = {10.1093/eurheartj/ehr465}
}
% [V][abs] PMID 22285583.

@article{bland1986statistical,
  author  = {Bland, J. Martin and Altman, Douglas G.},
  title   = {Statistical methods for assessing agreement between two methods of clinical measurement},
  journal = {The Lancet}, year = {1986}, volume = {327}, number = {8476}, pages = {307--310},
  doi     = {10.1016/S0140-6736(86)90837-8}
}
% [DOI?] the DOI is the commonly used string but was not retrieved.

@article{bland1999measuring,
  author  = {Bland, J. Martin and Altman, Douglas G.},
  title   = {Measuring agreement in method comparison studies},
  journal = {Statistical Methods in Medical Research}, year = {1999}, volume = {8}, number = {2}, pages = {135--160},
  doi     = {10.1177/096228029900800204}
}
% [V] record only. Its variance-component formula has an error, corrected in Bland & Altman 2007.

@article{bland2007agreement,
  author  = {Bland, J. Martin and Altman, Douglas G.},
  title   = {Agreement between methods of measurement with multiple observations per individual},
  journal = {Journal of Biopharmaceutical Statistics}, year = {2007}, volume = {17}, number = {4}, pages = {571--582},
  doi     = {10.1080/10543400701329422}
}
% [V] full text read; PMID 17613642. An arithmetic erratum is noted in Jones 2019, J Biopharm Stat 29(3):574-575.

@article{bland1990note,
  author  = {Bland, J. Martin and Altman, Douglas G.},
  title   = {A note on the use of the intraclass correlation coefficient in the evaluation of agreement between two methods of measurement},
  journal = {Computers in Biology and Medicine}, year = {1990}, volume = {20}, number = {5}, pages = {337--340},
  doi     = {10.1016/0010-4825(90)90013-F}
}
% [abs] the argument was seen only through secondary sources.

@article{mcgraw1996forming,
  author  = {McGraw, Kenneth O. and Wong, S. P.},
  title   = {Forming inferences about some intraclass correlation coefficients},
  journal = {Psychological Methods}, year = {1996}, volume = {1}, number = {1}, pages = {30--46},
  doi     = {10.1037/1082-989X.1.1.30}
}
% [V] record only. Erratum: Psychol Methods 1996;1(4):390. The ICC(A,1) and ICC(C,1) formulas are textbook forms; check them against the paper.

@article{shrout1979intraclass,
  author  = {Shrout, Patrick E. and Fleiss, Joseph L.},
  title   = {Intraclass correlations: uses in assessing rater reliability},
  journal = {Psychological Bulletin}, year = {1979}, volume = {86}, number = {2}, pages = {420--428},
  doi     = {10.1037/0033-2909.86.2.420}
}
% [V] PubMed 18839484. The ICC(2,1)/(3,1) <-> ICC(A,1)/(C,1) correspondence is unverified.

@article{koo2016guideline,
  author  = {Koo, Terry K. and Li, Mae Y.},
  title   = {A guideline of selecting and reporting intraclass correlation coefficients for reliability research},
  journal = {Journal of Chiropractic Medicine}, year = {2016}, volume = {15}, number = {2}, pages = {155--163},
  doi     = {10.1016/j.jcm.2016.02.012}
}
% [V] PMC4913118. Unverified: whether they recommend grading on the 95% CI.

@article{lin1989concordance,
  author  = {Lin, Lawrence I-Kuei},
  title   = {A concordance correlation coefficient to evaluate reproducibility},
  journal = {Biometrics}, year = {1989}, volume = {45}, number = {1}, pages = {255--268},
  doi     = {10.2307/2532051}
}
% [DOI?] Cite it only if you explain why CCC was not used.

@article{parker2016application,
  author  = {Parker, Richard A. and Weir, Christopher J. and Rubio, Noah and Rabinovich, Roberto and Pinnock, Hilary and Hanley, Janet and McCloughan, Lucy and Drost, Ellen M. and Mantoani, Leandro C. and MacNee, William and McKinstry, Brian},
  title   = {Application of mixed effects limits of agreement in the presence of multiple sources of variability: exemplar from the comparison of several devices to measure respiratory rate in {COPD} patients},
  journal = {PLoS ONE}, year = {2016}, volume = {11}, number = {12}, pages = {e0168321},
  doi     = {10.1371/journal.pone.0168321}
}
% [DOI?] the author list and title are from memory; only the journal, volume and article number were in the notes.

@article{kottner2011grras,
  author  = {Kottner, Jan and Audig{\'e}, Laurent and Brorson, Stig and Donner, Allan and Gajewski, Byron J. and Hr{\'o}bjartsson, Asbj{\o}rn and Roberts, Chris and Shoukri, Mohamed and Streiner, David L.},
  title   = {Guidelines for Reporting Reliability and Agreement Studies ({GRRAS}) were proposed},
  journal = {Journal of Clinical Epidemiology}, year = {2011}, volume = {64}, number = {1}, pages = {96--106},
  doi     = {10.1016/j.jclinepi.2010.03.002}
}
% [V] record only. [DOI?] the author list is from memory.

@article{hutcheon2010random,
  author  = {Hutcheon, Jennifer A. and Chiolero, Arnaud and Hanley, James A.},
  title   = {Random measurement error and regression dilution bias},
  journal = {BMJ}, year = {2010}, volume = {340}, pages = {c2289},
  doi     = {10.1136/bmj.c2289}
}
% [V] the article number is c2289, not c3223.

@book{carroll2006measurement,
  author    = {Carroll, Raymond J. and Ruppert, David and Stefanski, Leonard A. and Crainiceanu, Ciprian M.},
  title     = {Measurement Error in Nonlinear Models: A Modern Perspective},
  edition   = {2}, publisher = {Chapman \& Hall/CRC}, address = {Boca Raton}, year = {2006},
  isbn      = {978-1-58488-633-4}, doi = {10.1201/9781420010138}
}
% [DOI?] No page reference was verified for the logistic attenuation approximation.

@article{warfield2004staple,
  author  = {Warfield, Simon K. and Zou, Kelly H. and Wells, William M.},
  title   = {Simultaneous truth and performance level estimation ({STAPLE}): an algorithm for the validation of image segmentation},
  journal = {IEEE Transactions on Medical Imaging}, year = {2004}, volume = {23}, number = {7}, pages = {903--921},
  doi     = {10.1109/TMI.2004.828354}
}
% [DOI?] the details are from memory. Optional citation, used only for the "reference, not ground truth" framing.
```

Do not cite these until checked: Pflederer 2006 and Medrano-Gracia (bifurcation angles), Papadopoulou (QAngio CT), Park 2015 (DOI not retrieved), de Graaf 2013 (DOI not retrieved), Müller & Büttner 1994, Carstensen 2008 (DOI likely 10.2202/1557-4679.1107), and the ImageCAS and ASOCA papers. ASOCA and ImageCAS evaluate segmentation, not centerlines, and the methodology does not need them.
