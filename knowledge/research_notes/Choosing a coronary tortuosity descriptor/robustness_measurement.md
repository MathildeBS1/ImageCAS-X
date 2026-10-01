# Robustness and reproducibility of tortuosity/curvature measurement on coronary CTA centerlines

Evidence-quality legend. **FT** = full text read (through WebFetch, which summarises with a small model, so numbers were not re-checked against the PDF unless marked FT-PDF). **FT-PDF** = full text converted locally with pdftotext and grepped. **ABS** = abstract or search snippet only. Not repeated here: Kjeldsberg/Kashyap/Bullitt Table 2/Bribiesca-Sanchez details and the kappa_a + Q proposal in `reports/`. Where an earlier report already cites a source (Kashyap 2022, van Zandwijk 2019, Kjeldsberg 2021) I only add numbers that were not in its headings.

Headline: I found **no coronary CTA study reporting ICC, CV or Bland-Altman for tortuosity or curvature** (scan-rescan, inter-observer or inter-extractor). Nearly all reproducibility figures below come from carotid CT, retinal fundus and cerebral MRA. Coronary evidence is limited to cardiac-phase effects, Kashyap's smoothing settings and sampling-rate work on coronary trees.

---

## 1. Which metrics are robust, which collapse under noise, smoothing or sampling choices?

### Takeaway
Length-ratio metrics (arc/chord) are the most reproducible operator-wise but discard curvature information and, on coronary data, did not correlate with wall shear stress. Derivative-based curvature metrics and anything that counts events (inflections, bends, curvature minima) are strongly sampling- and scale-dependent; torsion is worst. Arc-length-normalised curvature integrals are the most sampling-tolerant of the curvature family, but only once the centerline is sampled far more densely than voxel spacing.

### Cited Findings
- On 9,000 vessels including coronary trees, measurements made at voxel-level sampling "generally underestimate common tortuosity metrics"; for all metrics except inflection counts, changes were **<5 % between 10x and 100x** the original sampling (originals 1-10 points/mm); the authors conclude 10-100 points/mm are needed for vessels of radius 0.1-10 mm. On a Salkowski phantom the measured total curvature, torsion and combined values were below analytic truth at native sampling and matched only at 10x-100x. (FT-PDF) — [Bullitt-group Frenet-Serret paper, arXiv 1911.12316](https://arxiv.org/abs/1911.12316) (published IEEE TMI 2021, [doi](https://doi.org/10.1109/tmi.2020.3025467)); full PDF in `tool-results`, text grepped.
- In the same paper, torsion-only metrics showed "considerably more variation" than curvature-only metrics as sampling rose, because torsion needs 2nd and 3rd derivatives. Arc-length-normalised versions (TC/L, TT/L, TCCT/L, SOA) were "more robust to errors associated with oversampling" (phantom, 100x overshoot smaller). (FT-PDF) — [arXiv 1911.12316](https://arxiv.org/pdf/1911.12316)
- Same paper, inflection counts: the curvature-minimum count IC_kappa rose by **as much as 439 % (coronary arteries) and 1027 % (abdominal/iliac/renal)** with denser sampling; the normal-vector-jump count IC_N fell with sampling because its threshold is not tied to step size. Authors say both definitions need redefining. (FT-PDF) — [arXiv 1911.12316](https://arxiv.org/pdf/1911.12316)
- Same paper: SOA and average combined curvature+torsion converge to a near one-to-one relationship at high sampling, i.e. many published metrics are redundant. (FT-PDF) — [arXiv 1911.12316](https://arxiv.org/pdf/1911.12316)
- Coronary left-main bifurcation, 127 patients without CAD, VMTK centerline, Taubin smoothing (passband 0.03, 30 iterations), resampled at 0.01 mm: arc/chord tortuosity index had **no relationship with low TAWSS (R2 -0.018, p=0.86)**, average absolute curvature R2 0.112 (p<0.001). The tortuosity index distribution was heavy-tailed (kurtosis 9.46, skewness 2.71) vs curvature (1.49, 1.02). (FT) — [Kashyap et al. 2022, Sci Rep 12:865](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/) (region is a 10 mm piece; earlier reports have the per-region table).
- Curvature-based indices are noise- and sampling-sensitive; angle-based ones unstable at low resolution; "overly small windows increased noise sensitivity in curvature-based indices, whereas larger windows attenuated diagnostically relevant features". (ABS, search-engine synthesis, not a verified quote of one paper) — [search result summary, PMC12786152 etc.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12786152/)
- Retinal, 2D: tortuosity indices differ in response to image scaling: tau_Hart varies inversely with the square of the scaling factor and tau_Grisan inversely with the factor; no index preserved its relative ordering after magnification. Resolving-power changes moved tau_Grisan by up to **70.2 %** (FOV >30 degrees), tau_Wang 38.5 %, tau_a-s 36.5 %, tau_Hart 30.6 %. tau_Hart was the most resilient (SRCC 0.832 veins, 0.924 arteries). (FT) — [Standardizing image acquisition... retinal tortuosity, PMC12265663](https://pmc.ncbi.nlm.nih.gov/articles/PMC12265663/)
- Retinal, cross-software: ICC between different software packages for retinal parameters was 0.159-0.410 (poor), attributed partly to differing tortuosity definitions and numerical ranges; same-method inter-observer ICC 0.92 for peripapillary tortuosity. (ABS, search snippets) — [SIVA vs VAMPIRE, PMC5868859](https://pmc.ncbi.nlm.nih.gov/articles/PMC5868859/); [peripapillary method, PMC12574746](https://pmc.ncbi.nlm.nih.gov/articles/PMC12574746/)
- A 2D angiography discrete-curvature score (turning angle / pi) showed only Pearson r=0.116 with arc/chord, and Cohen kappa 0.52 against experts, i.e. metric families disagree strongly. (FT) — [ML coronary tortuosity, PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)

### Inferences
- The Frenet-Serret result is the strongest new challenge to the proposed pair (kappa_a, Q): kappa_r and Q depend on second-moment curvature, which is the quantity that inflates under noise. Whether the chord-angle (discrete turning-angle over chord ell) implementation in the earlier report escapes this is untested; its noise floor and ell sweep must be measured on ImageCAS.
- 0.5 mm isotropic data is ~2 points/mm, well below the 10 points/mm "sufficient" rate; derivative curvature from raw 0.5 mm points will be biased low. Spline-interpolate and resample first (and report the resampling step), or use chord angles at ell of several voxels.
- Inflection/bend counts should be treated as the most fragile family, consistent with Kjeldsberg (below). Recommending bends per 100 mm is defensible only for comparison with angiographic scoring.

### Gaps
- No noise-injection or jitter experiment on real coronary CTA centerlines with kappa_r or Q was found.
- Gu/Hart 2007 spline-curvature paper ([PubMed 17419088](https://pubmed.ncbi.nlm.nih.gov/17419088/)) was not retrievable (captcha); the claim that spline-fitted metrics are "largely independent of resolution" is from a search snippet only (ABS).
- The exact figures for Frenet Table S4/Fig. 6 per metric were not extracted.

---

## 2. Recommended and validated smoothing scales, chord lengths, spline settings

### Takeaway
The only quantitative, validated parameter recommendations are for carotid siphon bends (Kjeldsberg) and coronary left-main curvature (Kashyap's Taubin settings, not validated for robustness). Chord length is not systematically validated for coronaries anywhere I found.

### Cited Findings
- Kjeldsberg, ICA, two bend detectors (parameters in the units of the morphMan model, resampling length r, Laplacian factor lambda, iterations N): Piccinelli bend count fell from mean 33 (r=0.02) to 3 (r=0.2), with r=0.1 giving 6-7 bends; lambda 1.2-1.5 and N 20-100 gave stable counts (7 to 6 bends over N 50-250). Bogunovic: lowest CV at r=0.1, lambda near 1.1 (mean bend length ~60 mm), N=20 (similar at 60-100), failure to detect bends at lambda>2.0, deviation rises for N>100. Conclusion in the abstract-level summary: **smoothing had least effect, resolution most**. (FT) — [Kjeldsberg 2021, PMC8626959](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- Sampling rule of thumb from the Frenet paper: reconstruction error falls below the vessel radius at ~10 points/mm; sufficient rate scales with radius (10-100 points/mm for radius >~1 mm; higher for radius <1 mm), and oversampling above ~100x can overfit noise (Salkowski total metrics overshoot). (FT-PDF) — [arXiv 1911.12316](https://arxiv.org/pdf/1911.12316)
- Kashyap's settings (Taubin passband 0.03, 30 iterations, 0.01 mm resample) are what produced the only significant coronary kappa_a result; no sensitivity analysis on those settings is reported in the summary I obtained. (FT) — [Kashyap 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Coronary dynamic geometry study used Menger curvature "at every 5 mm" (a chord-like scale) on CTA centerlines, and found ES/ED differences detectable at that scale (see section 4). (FT) — [van Zandwijk 2019, PMC7165136](https://pmc.ncbi.nlm.nih.gov/articles/PMC7165136/)
- Hart-style and Grisan-style retinal indices depend on the segmentation/centerline method: all indices did better on matched-filter than Gabor-filter centerlines despite similar centerline correctness scores (0.71-0.77). (FT) — [PMC12265663](https://pmc.ncbi.nlm.nih.gov/articles/PMC12265663/)

### Inferences
- A defensible protocol: spline-fit or Taubin/Laplacian smooth lightly (Kjeldsberg: smoothing is the low-impact knob), resample to <=0.1-0.25 mm, then compute chord-based quantities at a pre-registered ell and report an ell sweep (e.g. 2, 3, 5, 10 mm). The ell values are my design choice; Menger at 5 mm (van Zandwijk) is the only coronary precedent.
- Because Kjeldsberg found resolution, not smoothing, drives bend counts, any bend-based metric must fix the resampling step and state it.
- Tension with earlier reports: the ell of 3 to 5 mm proposal is broadly consistent with the 5 mm precedent, but the Frenet paper suggests kappa_r-based Q computed from derivative curvature (rather than chord angles) would need much finer sampling and would be noise-limited. If Q is implemented with chord angles it is not the metric the Frenet paper tested.

### Gaps
- No coronary paper systematically varies chord length or spline smoothing and reports metric stability.
- Kjeldsberg parameters are in model-specific units (r, lambda, N) for carotid siphon; no mm-based translation to coronaries.

---

## 3. Does the centerline extractor change results?

### Takeaway
No coronary comparison of extractors on tortuosity output exists in what I found. Extractor accuracy studies exist (CAT08) but quantify position error, not derived curvature. The mechanism of failure is known: skeletonisation is noise-sensitive, minimal-path can shortcut, VMTK spheres fail in highly tortuous or narrow lumens.

### Cited Findings
- CAT08 evaluation of 13 coronary centerline algorithms on 32 CTA scans uses overlap and mean distance (e.g. best automatic method overlap 93.7 %, accuracy 0.30 mm); it does not report curvature or tortuosity. (ABS) — [CAT08, PubMed 19632885](https://pubmed.ncbi.nlm.nih.gov/19632885/)
- Skeletonisation/thinning is sensitive to mask noise and spurious branches; minimal-path methods are cost-sensitive, can make shortcuts, and favour shorter paths (biasing length and hence arc/chord downward); VMTK inscribed-sphere approach struggles with high tortuosity, rapid branching and narrow lumen. (ABS, background statements in search snippets, not primary comparisons) — [DeepCenterline arXiv 1903.10481](https://arxiv.org/pdf/1903.10481); [VMTK-related, arXiv 2309.08779](https://arxiv.org/html/2309.08779v2)
- Carotid CT, four commercial packages (each with its own semi-automatic centerline): pairwise inter-software agreement on tortuosity index **ICC 0.95-0.99** in 12 highly tortuous ECAA patients; median TI 1.42 (IQR 1.29-1.65, skull base to bifurcation). Arc/chord is therefore robust to the extractor **for large, macroscopic tortuosity**. (FT) — [Comparability of semiautomatic tortuosity measurements in the carotid artery, PMC6348067](https://pmc.ncbi.nlm.nih.gov/articles/PMC6348067/)
- Kjeldsberg segmentation variability (proxy for extractor and segmentation differences): Piccinelli superior-bend CV 47 %, "not robust enough to overcome real-world inter-laboratory differences"; Bogunovic CV <5 % for superior bend. (FT) — [PMC8626959](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- Retinal centerline extractor changed absolute index performance (matched vs Gabor filter) although centerline correctness was similar. (FT) — [PMC12265663](https://pmc.ncbi.nlm.nih.gov/articles/PMC12265663/)

### Inferences
- The carotid ICC 0.95-0.99 was obtained in a tortuosity range (TI ~1.3-1.4) far above normal coronary segment values (~1.10 per segment, see section 4). ICC scales with between-subject variance; coronary arc/chord on a healthy cohort has a much narrower range and its ICC would probably be lower. This is an inference, not a measured value.
- ImageCAS-X centerlines derive from labelled masks; the effective "extractor" difference between ImageCAS and the Danish cohort will be mask differences, which Kjeldsberg shows dominate.

### Gaps
- No coronary paper compares VMTK vs minimal-path vs model-based centerlines on tortuosity/curvature. Stated as absent, not confirmed absent from all literature.

---

## 4. Cardiac phase, stents/plaque, segmentation errors (truncated distal ends)

### Takeaway
Cardiac phase is a measurable, systematic effect on curvature (about +9 to +11 % end-systole vs end-diastole) and on inflection counts, but small on arc/chord at the artery level (+2.3 %, not significant). Stent and plaque effects on tortuosity metrics specifically were not found in the literature. Truncation effect is unquantified but follows from the definitions.

### Cited Findings
- 71 patients, 137 arteries, 456 segments, retrospective-gated CTA, ES vs ED: mean curvature (Menger, every 5 mm) **0.090 vs 0.081 mm^-1 at artery level (+11.1 %, p=0.002)**, 0.085 vs 0.078 at segment level (+8.9 %, p<0.001). Tortuosity (arc/chord) 1.36 vs 1.33 at artery level (+2.3 %, p=0.09, not significant) and **1.12 vs 1.10 at segment level (+1.8 %, p=0.005)**. Inflection points higher in ES at both levels (p<0.001). No relationship between stenosis degree or plaque type and the dynamic change. (FT) — [van Zandwijk et al. 2019, PMC7165136](https://pmc.ncbi.nlm.nih.gov/articles/PMC7165136/)
- Only 64.3 % of 213 arteries and 71.4 % of 639 segments could be included in that study, i.e. a third of vessels failed inclusion (reasons not extracted). (FT) — same source.
- Clinical angiographic tortuosity is defined as >=3 bends of >=45 degrees in a main branch, "present both in systole and diastole" in the SCAD/angiography literature; intra-observer angiographic agreement for tortuosity: 0.92 with kappa 0.78 in one SCAD study (2D angiography, categorical). (ABS, search snippets) — [Circ Cardiovasc Interv SCAD](https://www.ahajournals.org/doi/full/10.1161/CIRCINTERVENTIONS.114.001676)
- Segmentation performance is lower in plaque-bearing than plaque-free CTA, and image quality has only a small positive correlation with segmentation performance; blooming from stents depends on strut/size/material. Effects on derived tortuosity were not quantified. (ABS, search snippets) — [Image quality in coronary CTA, PMC5605061](https://pmc.ncbi.nlm.nih.gov/articles/PMC5605061/); [stent CTA, AJR](https://ajronline.org/doi/10.2214/AJR.23.29506)
- Retinal analog for image/segmentation failure: in papilledema, 3 of 30 eyes unmeasurable; one outlier from a different optic-disc centre changed ATI agreement, and the authors say rater variability dominates over physiology and acquisition. (FT) — [PMC8727308](https://pmc.ncbi.nlm.nih.gov/articles/PMC8727308/)

### Inferences
- Arc/chord per segment is more phase-stable than curvature-moment metrics (0.63 vs 0.51 inflections per segment is a 24 % relative difference [the earlier report cites those numbers]; curvature +9 to 11 %; arc/chord +2 %). So the proposed (kappa_a, Q) pair, being curvature moments, is expected to carry a ~10 % phase shift; ImageCAS cannot test this (single phase per scan) but the Danish cohort may.
- Truncated distal ends (from segmentation failure) reduce L and chord together; arc/chord is fairly length-invariant only if the missing tail resembles the rest, while Q (grows with straight padding per the earlier report) and any total/bend-count metric are length-dependent. Distal truncation therefore biases count-per-vessel and total metrics most and density metrics least. This is derivation, not measured.
- Plaque-induced local deflection: no measurement found; treat the earlier report's risk statement as unverified in both directions.

### Gaps
- No study quantifies stent or calcified-plaque effect on centerline-derived tortuosity or curvature in CTA.
- No study of distal truncation effects on tortuosity.
- van Zandwijk's exclusion reasons and Bland-Altman/repeatability were not retrieved.

---

## 5. Minimum length / segment definition for a reliable number

### Takeaway
There is no validated minimum length for coronaries. Indirect evidence: (i) Kashyap's only significant results used 10 mm pieces but with arc/chord failing there; (ii) tortuosity per segment is ~1.10 with small dynamic range, so short segments have low signal-to-noise; (iii) sampling error scales with radius and inflates for short vessels.

### Cited Findings
- Frenet paper: for short vessels, native-rate sampling produced "exceedingly high values of curvature" that decreased then increased with sampling; authors argue the sampling rate should be set by vessel radius, and that arc-length normalisation controls covariation between vessel length, sampling and tortuosity. (FT-PDF) — [arXiv 1911.12316](https://arxiv.org/pdf/1911.12316)
- Carotid: reproducibility was high (ICC 0.72-0.99 inter-observer across packages) for a **long** skull-base-to-bifurcation/arch span, i.e. tens of mm to cm scale, in a highly tortuous cohort. (FT) — [PMC6348067](https://pmc.ncbi.nlm.nih.gov/articles/PMC6348067/)
- Kjeldsberg mean siphon bend length ~60 mm for Bogunovic at stable settings; Piccinelli bends vs the rest are unstable at small r. (FT) — [PMC8626959](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/)
- Segment-level arc/chord median values in coronaries: 1.10 (ED) to 1.12 (ES); artery level 1.33 to 1.36. (FT) — [PMC7165136](https://pmc.ncbi.nlm.nih.gov/articles/PMC7165136/)

### Inferences (design proposals, not evidence-backed thresholds)
- Use a minimum of roughly 5 to 10 chord lengths per measured vessel (so ~15 to 50 mm at ell 3 to 5 mm, consistent with the earlier report's 15 mm floor but arguably too low for stability of second-moment metrics), pre-register it, and report NaN otherwise.
- Prefer named-vessel or fixed-anatomical-landmark segments (proximal 30-40 mm of LAD/LCx/RCA measured from the ostium or bifurcation) over "whatever the segmentation returns", so distal truncation does not change the denominator.
- Empirically fix the floor on ImageCAS: compute the metric on nested truncations (e.g. 20, 30, 40, 60 mm) and on 0.25-1 mm jitter, and pick the length where between-scan ICC of the metric stabilises.

### Gaps
- No source states a minimum coronary length for reliable tortuosity.
- No coronary ICC/CV for any tortuosity metric on CTA (repeat scans, inter-observer, inter-scanner). Cerebral MRA scan-rescan (7 healthy subjects, inter-session CoV for TI, BL, ICM) exists but figures were not retrieved ([medRxiv 2024, 403 blocked; snippet only](https://www.medrxiv.org/content/10.1101/2024.12.23.24319570v1.full)).
- Retinal: intra-rater/inter-image ICC for arterial tortuosity index 0.90/0.95 (n=17) and venous 0.80/0.73 (n=27), authors stress rater variability as dominant (FT, [PMC8727308](https://pmc.ncbi.nlm.nih.gov/articles/PMC8727308/)); this is 2D and semi-manual, so transferability to automated CTA is low.

---

## Where this contradicts or qualifies the earlier reports

1. **Q and kappa_r sensitivity.** The earlier proposal ranks (kappa_a, Q) first with a noise floor to be measured. Frenet-Serret evidence (FT-PDF) says derivative-based curvature at voxel-level sampling is biased low and second-derivative-driven metrics are the noisiest. This does not disprove the proposal but means the ell sweep and jitter experiment are not optional, and Q should be implemented on chord angles after resampling, not on finite-difference curvature of 0.5 mm points.
2. **Cardiac phase.** The earlier report singles out the turn/inflection layer as the component most exposed to phase. New numbers show curvature moments also shift ~9-11 % between phases, so kappa_a and Q are exposed too, while arc/chord shifted only 1.8-2.3 %. The relative phase-robustness ranking is arc/chord > curvature > inflection count.
3. **Arc/chord as a "comparator" only.** Kashyap's zero TAWSS relationship for arc/chord in the left-main is a haemodynamic-relevance finding, not a reproducibility one. On reproducibility alone (carotid ICC 0.95-0.99), arc/chord is the best-supported metric. The two criteria should not be conflated when ranking.
4. **Bend counts.** Consistent with the earlier reading of Kjeldsberg (evidence against torsion-extrema detection), the Frenet paper independently shows curvature-minimum inflection counts changing by up to 439 % in coronaries with sampling. This strengthens, not contradicts, the demotion of bend counts, but also implicates the curvature-minima count and not only torsion-extrema.
5. **Extrapolating carotid ICC to coronary.** The 0.95-0.99 figures came from a cohort with TI ~1.3-1.4; do not quote them as coronary reproducibility.

## Source quality summary
- FT: Kjeldsberg 2021, carotid comparability (PMC6348067), van Zandwijk 2019, Kashyap 2022, retinal papilledema variability, retinal standardisation (PMC12265663), coronary ML angiography (PMC13308244).
- FT-PDF: Frenet-Serret arXiv 1911.12316 (fetched PDF, grepped locally).
- ABS/snippet only: Bullitt 2003, Gu/Hart 2007, CAT08, SCAD angiography, SIVA vs VAMPIRE, stent/image-quality items, medRxiv cerebral TOF (403), extractor-mechanism statements.
- Not retrieved: Grisan, Kalitzeos, Diedrich, Hart 1999 primary reliability figures (only search snippets on classification rates and expert variability).
