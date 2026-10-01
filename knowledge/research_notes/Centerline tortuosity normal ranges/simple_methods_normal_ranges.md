# Simple, literature-comparable coronary tortuosity measures and how to derive normal ranges from ImageCAS-X centerlines

Scope: which simple measures the thesis should report so its numbers can be set beside published work, what reference values exist per vessel, how 2D angiographic definitions map onto 3D centerlines, how "normal" should be quantified, and first per-vessel distributions on the ImageCAS-X training split (560 scans, centerlines only). Settled questions from the earlier repo reports are cited, not redone: [Vessel specific tortuosity math and tests](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Vessel%20specific%20tortuosity%20math%20and%20tests.md) (κ_a at chord 5 mm, σ 1 mm as primary; TI as a length- and dominance-confounded secondary; never pool vessels) and [Choosing a coronary tortuosity descriptor](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Choosing%20a%20coronary%20tortuosity%20descriptor.md).

Computation artefacts (all reproducible, training ids only, Disease column never read):
- Scripts: `/zhome/e2/6/224426/project/ImageCAS-X/tortuosity/research/simple/compute_simple.py` (measures), `summarize_simple.py` (distributions, reference limits, correlations), `sensitivity_bends.py` (bend-count sensitivity).
- Outputs: `/work3/s254124/imagecasx_results/tortuosity_research/simple/` : `simple_measures.csv` (σ 1 mm, one row per case and vessel), `simple_measures_sigma2.csv`, `summary.csv`/`summary.txt`, `summary_sigma2.*`, `sensitivity_bends.txt`.
- Run: `source env.sh; cd tortuosity/research/simple; python compute_simple.py 1.0; python compute_simple.py 2.0 _sigma2; python summarize_simple.py; python summarize_simple.py _sigma2; python sensitivity_bends.py`.

## Q1. Which simple definitions dominate the coronary literature, with exact formulas and segments

### Takeaway
Coronary papers use two families: (a) a continuous 2D arc/chord "tortuosity index" measured ostium to distal end on angiograms, and (b) visual bend-count criteria, almost always "≥3 bends with ≥45° change in direction along the main trunk" (Li 2011 style), graded by Eleid into 45 to 90°, 90 to 180° and ≥180° classes, with "≥2 consecutive 180° turns" as the severe class (Groves). Bullitt's DM, ICM and SOAM come from cerebral MRA and are rarely applied to coronaries; the newest large coronary study (JACC Advances 2026) uses mean absolute turning angle per centerline point divided by π, in one 2D view of the RCA only.

### Cited Findings
- Distance factor / arc-chord: coronary "tortuosity index" = "the ratio between the absolute length of the coronary artery and straight-line length", measured in diastole from the ostium to the smallest visible branch, with ImageJ ([Zebić Mihić 2023, PMC10795752](https://pmc.ncbi.nlm.nih.gov/articles/PMC10795752/)).
- Bullitt 2003 (cerebral MRA): Distance Metric DM = path length / chord; Inflection Count Metric ICM = (number of inflection points + 1) × DM; Sum of Angles Metric SOAM: in-plane angle IP_k between consecutive tangent vectors, torsional angle TP_k between successive osculating-plane normals, CP_k = √(IP_k² + TP_k²), SOAM = Σ CP_k / path length (rad/cm). 3D inflection = locus of minimum total curvature where the Frenet normal and binormal flip by close to 180°, detected as large local maxima of ΔN·ΔN ([Bullitt 2003, PMC2430603](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/); definitions as recovered in the repo note [math_foundations.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Vessel%20specific%20tortuosity%20math%20and%20tests/math_foundations.md)).
- Li 2011 bend-count criterion: tortuosity = "≥3 bends (defined as ≥45° change in vessel direction) along main trunk of at least one artery, present both in systole and in diastole"; 1,010 consecutive angiography patients ([Li 2011, PLOS One](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0024232)). The same definition (≥3 consecutive bends of ≥45°, systole and diastole) is used by the non-obstructive CAD studies ([Zebić Mihić 2023, PMC10795752](https://pmc.ncbi.nlm.nih.gov/articles/PMC10795752/); [PMC10534717](https://pmc.ncbi.nlm.nih.gov/articles/PMC10534717/)).
- Eleid (Mayo SCAD) score, restated in a later Mayo paper: TCA = "three or more abrupt turns of >45 degrees in at least one major epicardial coronary artery at end-diastole"; per vessel (LAD, LCx, RCA, left PDA) 0 = none; 1 = ≥3 consecutive curvatures of 45 to 90°, or of 90 to 180° in vessels <2 mm; 2 = ≥3 consecutive curvatures of 90 to 180° in vessels ≥2 mm; 3 = ≥2 consecutive curvatures ≥180° in vessels ≥2 mm; summed over vessels ([PMC11605948](https://pmc.ncbi.nlm.nih.gov/articles/PMC11605948/); original [Eleid 2014, PubMed 25138034](https://pubmed.ncbi.nlm.nih.gov/25138034/)).
- Zegers 2007: tortuosity = two or more segments with ≥3 curvatures ≤120° (interior angle) during diastole ([Zegers 2007, PubMed 17612682](https://pubmed.ncbi.nlm.nih.gov/17612682/), abstract-level via search snippet).
- Groves 2009: severe coronary tortuosity = two consecutive 180° turns by visual estimation in a major epicardial artery ([Groves 2009, PubMed 19585899](https://pubmed.ncbi.nlm.nih.gov/19585899/)).
- Angle conventions differ between papers: "≥45° change in direction" means interior angle ≤135°, Zegers' ≤120° interior means ≥60° turning ([repo note, comparative evidence](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Alternative%20tortuosity%20merges%20for%20coronaries/comparative_evidence.md)).
- Other angiographic indices: a Tortuosity Severity Index grading significant tortuosity as mild/moderate with >4 curvatures in total or any severe/extreme curvature ([PMC6303525](https://pmc.ncbi.nlm.nih.gov/articles/PMC6303525/)).
- JACC Advances 2026 (Tello Ayala et al.): discrete curvature θ_i = turning angle between consecutive skeleton edges x_{i−1}x_i and x_ix_{i+1}; score = mean |θ_i| / π over the branch-pruned RCA skeleton in an LAO view (primary angle −10° to 100°), 38,691 angiograms from 22,334 patients; described as the Bribiesca slope-chain approach ([local PDF](file:///zhome/e2/6/224426/project/ImageCAS-X/A%20Machine%20Learning%20Driven%20Approach%20to%20Quantifying%20Coronary%20Artery%20Tortuosity%20_%20JACC_%20Advances.pdf); [doi 10.1016/j.jacadv.2026.102829](https://www.jacc.org/doi/10.1016/j.jacadv.2026.102829)). The same paper notes that TI, SOAM and ICM give reproducible scalars but rely on global quantities.

### Inferences
- For comparability the thesis should report, per vessel: (1) DM = L/D over the whole labelled vessel (ostium to label end); (2) a bend count at 45° and 90° plus the derived binary "≥3 bends ≥45°" and an Eleid-like grade; (3) a curvature-per-length measure. For (3) the earlier report's κ_a (sum of turning at chord 5 mm / L) is the SOAM in-plane term at a stated scale; Bullitt's full SOAM with the torsion term should not be reported (see Q5 results). The JACC score is a mean turning angle per pixel-step on a 2D skeleton and is scale dependent (it is not scale invariant in practice, because θ_i depends on the pixel step); it is not directly reproducible from a 3D centerline.
- "Segment" is almost always the whole main trunk from ostium to the distal visible end, not the AHA 17-segment model. None of the retrieved papers report per-AHA-segment tortuosity values.

### Gaps
- Exact Eleid 2014 wording from the original article was not retrieved; the definition above comes from a 2024 Mayo restatement.
- Zegers 2007 full text not read; the "two or more segments" qualifier is from a search snippet.
- Bullitt's numerical ΔN·ΔN threshold was not recovered (earlier repo notes flag the same gap).

## Q2. Published normative or reference values per vessel (CTA and angiography)

### Takeaway
No published source gives CTA-based normal ranges of arc/chord, SOAM or curvature per coronary vessel in a healthy population. The only per-vessel continuous values are 2D angiographic TI medians from 160 patients (RCA about 1.9 to 2.0, LAD and LCx about 1.2 to 1.3); per-vessel bend-criterion prevalences (LCx > LAD >> RCA) come from symptomatic angiography cohorts; the largest continuous distribution (JACC 2026) covers the RCA in one 2D view only. Women have more tortuosity in every study that reports sex; age effects are weaker and partly explained by risk factors.

### Cited Findings
- 2D angiographic TI (L/D), median (IQR), non-obstructive vs obstructive CAD, 160 patients (89 men, mean age 61 to 62): LCx 1.30 (1.13 to 1.47) vs 1.15 (1.10 to 1.30); LAD 1.26 (1.18 to 1.45) vs 1.18 (1.14 to 1.26); RCA 2.00 (1.79 to 2.27) vs 1.87 (1.65 to 2.17) ([Zebić Mihić 2023, PMC10795752](https://pmc.ncbi.nlm.nih.gov/articles/PMC10795752/)). The same study's bend criterion was met by LCx 40 % vs 14.7 %, LAD 32.9 % vs 10.7 %, RCA 9.4 % vs 0 %.
- Li 2011, 1,010 angiography patients: coronary tortuosity in 39.1 %; per vessel LCx 26.9 %, LAD 21.1 %, RCA 1.4 %, LAD and LCx both 9.9 %; more common in women (OR 2.603, p < 0.001) and with hypertension (OR 1.533, p = 0.006); negatively associated with CAD (OR 0.755) ([Li 2011](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0024232)).
- Non-obstructive CAD group of 131 angiography patients: LCx 35.1 %, LAD 27.3 %, RCA 11.7 % tortuous; higher prevalence in women noted ([PMC10534717](https://pmc.ncbi.nlm.nih.gov/articles/PMC10534717/)).
- Eleid 2014: tortuosity in 78 % of SCAD patients vs 17 % of 313 controls without SCAD or CAD; tortuosity score 4.41 ± 1.73 vs 2.33 ± 1.49 ([Eleid 2014 via search summary of PubMed 25138034](https://pubmed.ncbi.nlm.nih.gov/25138034/)). In a later SCAD cohort, each decade of age was associated with about 0.89 units higher score ([PMC11605948](https://pmc.ncbi.nlm.nih.gov/articles/PMC11605948/)).
- JACC Advances 2026, RCA in LAO: mean age 64.7 ± 12.5, 37 % female; score range 0.007 to 0.289; median 0.107; stated IQR 0.029 to 0.190; skewness 0.744, kurtosis 3.879; 99th percentile 0.199; 90th percentile 0.152 overall (0.158 women, 0.148 men; 0.151 to 0.153 across race), about 27° mean angulation; women higher (β per SD 0.17, 95 % CI 0.14 to 0.20); age β 0.02 per SD in an age-and-sex model, attenuated to 0.01 (p = 0.121) after risk-factor adjustment; higher with hypertension, lower with diabetes ([local PDF](file:///zhome/e2/6/224426/project/ImageCAS-X/A%20Machine%20Learning%20Driven%20Approach%20to%20Quantifying%20Coronary%20Artery%20Tortuosity%20_%20JACC_%20Advances.pdf)). Internal inconsistency: an upper quartile of 0.190 cannot sit above a 90th percentile of 0.152, so either the IQR or the percentiles are misreported.
- Groves 2009: severe tortuosity more frequent in women and hypertensive patients, negatively associated with CAD ([PubMed 19585899](https://pubmed.ncbi.nlm.nih.gov/19585899/)).
- Precedent for age-stratified CTA normal values in another vessel: descending thoracic aorta TI = centerline length / straight length in 200 patients without vascular disease, 1.05 (SD 0.024) under 65 vs 1.14 (0.078) at 65 or older, p < 0.001; no sex difference (p = 0.626); age the only independent predictor in linear regression ([PMC6478292](https://pmc.ncbi.nlm.nih.gov/articles/PMC6478292/)).
- 3D curvature in normal coronaries from biplane angiography: end-diastolic mean curvature 0.050 to 0.066 mm⁻¹ in normal LAD and RCA ([Zhu 2008, PMC2759354](https://pmc.ncbi.nlm.nih.gov/articles/PMC2759354/), as cited in the earlier repo report).

### Inferences
- The literature populations are symptomatic angiography cohorts, not healthy volunteers; "normal" in these papers means "without SCAD" or "obstructive vs non-obstructive". The obstructive-CAD group of Zebić Mihić is the closest published comparator for an unselected CCTA cohort like ImageCAS.
- Any per-vessel reference derived from ImageCAS-X is therefore the first CTA-based per-vessel distribution of these simple measures that we could find, but it is a population reference distribution of CAD-suspected patients, not a healthy normal range.

### Gaps
- No CTA study reporting per-vessel normal L/D, SOAM or curvature in healthy subjects was found in the searches run here (three targeted queries).
- Age and sex are not available in ImageCAS-X (only Image Quality, Dominance, Disease in Descriptors.xlsx), so the female-sex effect that every study reports cannot be adjusted for; this is a structural limit of any ImageCAS-X normal range.
- Turgut 2010 and other hypertension studies were not re-read here.

## Q3. Mapping 2D angiographic definitions onto a 3D centerline

### Takeaway
There are two principled mappings. The first is to simulate the angiographic view: project the 3D centerline onto the image plane of a standard C-arm angulation (defined from the LPS patient frame) and compute the 2D measure there. On ImageCAS-X this reproduces the published 2D TI medians closely. The second is view-independent: average the 2D measure over all anterior views, or take the least-foreshortened view. Bend counts do not map well; they depend strongly on the smoothing scale and curvature floor, and 3D counts exceed 2D counts because out-of-plane bends are lost in projection.

### Cited Findings
- Standard projections: LCA in 30° RAO with cranial and caudal tilt, 45° caudal LAO, 60° cranial LAO, 90° left lateral; RCA in 45° cranial LAO and 30° RAO; LAO shows the ostial and proximal RCA ([search summary of EuroIntervention / BJC trainee guides](https://eurointervention.pcronline.com/article/tools-and-techniques-angiographic-views); [BJC 2016](https://bjcardio.co.uk/2016/08/optimal-angiographic-views-for-invasive-coronary-angiography-a-guide-for-trainees/)). An optimised view set comprised LAO cranial, AP-RAO caudal, RAO caudal and AP-RAO cranial for the left system, and LAO cranial, RAO, AP-RAO cranial for the right ([PMC3487091](https://pmc.ncbi.nlm.nih.gov/articles/PMC3487091/)).
- JACC 2026 used LAO views with primary angle −10° to 100° for the RCA ([local PDF](file:///zhome/e2/6/224426/project/ImageCAS-X/A%20Machine%20Learning%20Driven%20Approach%20to%20Quantifying%20Coronary%20Artery%20Tortuosity%20_%20JACC_%20Advances.pdf)).
- ImageCAS-X centerline coordinates are in an LPS-like frame (+x patient left, +y posterior, +z superior): in all 552 training scans with LM, LAD and RCA labels, the left tree lies at larger x than the RCA and the LAD's lower end lies below the LM (sanity check `frame_ok`, 0 failures) ([summary.txt](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/summary.txt)). Detector direction used: d = (sin α cos β, −cos α cos β, sin β), α = LAO primary angle (RAO negative), β = cranial secondary angle (caudal negative) ([compute_simple.py](file:///zhome/e2/6/224426/project/ImageCAS-X/tortuosity/research/simple/compute_simple.py)).
- Own result, σ 1 mm, 560 training scans, views LAD RAO 20° / CRA 30°, LCx RAO 20° / CAU 30°, RCA LAO 30°: projected 2D DM median (IQR) LAD 1.20 (1.14 to 1.29), LCx 1.16 (1.08 to 1.27), RCA 1.81 (1.58 to 2.06). Published obstructive-CAD values are LAD 1.18 (1.14 to 1.26), LCx 1.15 (1.10 to 1.30), RCA 1.87 (1.65 to 2.17) ([summary.txt](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/summary.txt); [Zebić Mihić 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10795752/)).
- Own result: 2D DM in the standard view ranks vessels almost identically to 3D DM (Spearman ρ 0.92 LAD, 0.90 LCx, 0.97 RCA); DM averaged over 256 random anterior views, ρ 0.95 to 0.97. The view average is higher than 3D DM (LAD 1.49 vs 1.34, LCx 1.48 vs 1.30, RCA 2.05 vs 1.77) because oblique views foreshorten the chord more than the arc. The least-foreshortened view gives DM slightly below 3D (LAD 1.25, LCx 1.22, RCA 1.74). Median foreshortening in the standard view (projected / 3D length): LAD 0.89, LCx 0.87, RCA 0.94 ([summary.txt](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/summary.txt)).
- Own result: bend counts agree less between 2D and 3D (ρ 0.71 LAD, 0.68 LCx, 0.53 RCA). Fraction of vessels with ≥3 bends ≥45° at σ 1 mm and curvature floor 0.02 mm⁻¹: 3D LAD 0.88, LCx 0.60, RCA 0.53; 2D standard view LAD 0.68, LCx 0.38, RCA 0.19 ([summary.txt](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/summary.txt)).

### Inferences
- The recommended literature-comparable 2D number is "projected DM in a declared standard view", computed from the 3D centerline, reported next to 3D DM. It is cheap (256-view projection included, the whole pass took 61 s) and its agreement with the published medians is a useful external validity check. The residual differences in segment definition (labelled vessel end vs "smallest visible branch", single CT phase vs diastolic frame) must be stated.
- A C-arm view is patient-specific in practice (operators pick the view that opens the vessel). The least-foreshortened view is a reproducible stand-in for that operator choice; the fixed standard view is closer to how the JACC pipeline filtered loops. Report the fixed standard view as primary and the view-averaged value as a view-independent sensitivity figure.
- The "≥3 bends ≥45°" criterion cannot be ported as a single number: see Q5 sensitivity. Angiographers count abrupt, visually salient turns; a centerline algorithm also counts the long, gentle, heart-following curvature unless a curvature floor excludes it.

### Gaps
- No published paper was found that projects CTA centerlines onto angiographic views to calibrate tortuosity against angiography; the mapping above is our own.
- The view angles used by Zebić Mihić for the TI measurement were not stated in the retrieved text.
- ImageCAS gives one cardiac phase (typically diastolic reconstruction); the angiographic criteria require bends in both systole and diastole, which cannot be checked.

## Q4. How "normal" should be quantified

### Takeaway
Use CLSI EP28-A3c style nonparametric 2.5th and 97.5th percentiles with 90 % confidence intervals on each limit, per vessel, as the headline reference interval (n = 560 per vessel satisfies the 120 per partition minimum). Because the measures depend on covariates that cannot be partitioned with ≥120 cases (left dominance n = 32, codominance n = 15), express covariate dependence with quantile regression or GAMLSS/LMS (Box-Cox, median and CV smooth in log vessel length and dominance), and define "outlier" relative to a declared upper centile (97.5th for reference limits, 95th for a "top 5 %" flag), not by an absolute cut-off. Label the result a reference distribution in a CAD-suspected CCTA population.

### Cited Findings
- CLSI EP28-A3c: 120 reference individuals per partition for the nonparametric method, which estimates the 2.5th and 97.5th percentiles with a 90 % CI on each limit; parametric methods require Gaussian or transformable data; robust biweight for about 20 to 120 subjects; Harrell-Davis for moderate samples; bootstrap for CIs; screen outliers with Tukey box plots and check normality with Shapiro-Wilk or Anderson-Darling; partitioning multiplies the requirement (two partitions need about 240) ([analyse-it EP28 guide](https://analyse-it.com/learn/choosing-a-reference-interval-method); [CLSI EP28](https://clsi.org/shop/standards/ep28/)).
- At n = 120 the 3rd and 118th order statistics are the nonparametric 2.5th and 97.5th percentiles; CIs by the binomial rank method ([MetricGate EP28 nonparametric](https://metricgate.com/docs/reference-range-clsi-nonparametric/)).
- LMS method (Cole and Green 1992): after a Box-Cox power transformation the measurement is normal at each covariate value; skewness L, median M and CV S are smooth curves, giving covariate-adjusted z-scores and centiles; GAMLSS generalises it (BCCG distribution) and extends references to depend on body size as well as age ([Indian Pediatrics LMS/BCPE review](https://link.springer.com/article/10.1007/s13312-014-0310-6); [Cole 2009, Stat Med, age- and size-related reference ranges](https://onlinelibrary.wiley.com/doi/10.1002/sim.3504)). LMS underlies WHO, CDC and UK90 growth charts ([same search summary](https://link.springer.com/article/10.1007/s13312-014-0310-6)).
- Precedent in cardiac geometry: JACC 2026 defined low / average / high tortuosity as bottom decile / middle 8 deciles / top decile of its cohort and reported sex-specific 90th percentiles ([local PDF](file:///zhome/e2/6/224426/project/ImageCAS-X/A%20Machine%20Learning%20Driven%20Approach%20to%20Quantifying%20Coronary%20Artery%20Tortuosity%20_%20JACC_%20Advances.pdf)).
- Own result, distribution shape: skew of DM−1 is 1.33 (LAD), 0.45 (LCx), 0.58 (RCA); log(DM−1) is −0.33, −0.72, −1.49. κ_a skew 0.65, 1.03, 1.23; log κ_a −0.03, 0.29, 0.52 ([summary.txt](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/summary.txt)). The RCA left tail of log(DM−1) is the short left-dominant RCAs.
- Own result, covariates: Image Quality is not associated with any measure (|ρ| ≤ 0.07). Dominance moves DM strongly: RCA DM median 1.30 in left-dominant (n = 32) vs 1.79 in right-dominant (n = 513), p = 4e-13; LCx DM 1.48 vs 1.27, p = 1e-9; LAD 1.47 vs 1.33, p = 3e-6. κ_a differs little (RCA p = 0.20, LAD p = 0.59, LCx 0.044 vs 0.052, p = 0.035) ([summary.txt](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/summary.txt)). This reproduces the P150 dominance finding of the earlier report on the full training split.

### Inferences
- Recommended protocol: (1) fix scripts, smoothing σ, chord ℓ, views and floors before looking at confirmation data (they are fixed now in `compute_simple.py`); (2) per vessel, nonparametric 2.5th / 97.5th percentiles with binomial 90 % CIs on all 560 training scans; (3) for DM (strongly length- and dominance-dependent) report centiles conditional on log L and dominance by quantile regression (τ = 0.025, 0.5, 0.975) or GAMLSS BCCG/BCPE with smooth terms in log L and a dominance factor; (4) for κ_a, log-transform and a parametric interval is defensible (log skew ≤ 0.52), with the nonparametric interval as check; (5) verify on the validation split with the EP28 transfer procedure (about 20 per partition, binomial test of how many fall outside) only after the thresholds are frozen, and keep test scans untouched; (6) call "outlier" a value above the 97.5th centile of the covariate-conditional distribution, and "top 5 %" above the conditional 95th.
- Partitioning by dominance fails EP28 (32 and 15 cases < 120), so dominance must be a covariate, not a partition. "Heart size" from the tree could be total left-plus-right tree length or the ostium-to-apex distance; it was not computed here.
- Length conditioning is a choice with consequences: part of long-vessel DM is real anatomy (the apical wrap, dominance), so conditional centiles answer "tortuous for its length", not "tortuous".

### Gaps
- The Harris-Boyd partition criterion and the exact EP28 wording were not retrieved (the standard is paywalled; information is from vendor summaries).
- Cole's sample-size guidance for GAMLSS centiles ([PMC8008444](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8008444/)) was identified but not read, so no number is given for how many cases a covariate-conditional 2.5th centile needs.
- Quantile regression / GAMLSS fits were not run in this pass; only the marginal intervals and covariate associations were computed.

## Q5. First per-vessel distributions on ImageCAS-X training centerlines

### Takeaway
On all 560 training scans, per vessel at σ 1 mm: 3D DM medians are LAD 1.34, LCx 1.30, RCA 1.77, LM 1.01; κ_a (chord 5 mm) medians are 0.057, 0.052, 0.045 mm⁻¹; DM correlates with length (ρ 0.69 to 0.84) while κ_a and in-plane SOAM barely do (ρ 0.09 to 0.32). Bullitt's full SOAM (with torsion) and ICM are noise-dominated and should not be reported. Bend counts are usable only with the floor and smoothing stated, because the "≥3 bends ≥45°" prevalence moves from 0.88 to 0.37 on the LAD across reasonable settings. Runtime: 61 s for the full pass (median 0.107 s per scan), CPU only.

### Cited Findings
Method (all from [compute_simple.py](file:///zhome/e2/6/224426/project/ImageCAS-X/tortuosity/research/simple/compute_simple.py)): vessel = longest geodesic path of the label (LM 1, LAD 2, LCx 3, RCA 9) via `tortuosity/vessels.py`; arc-length resample 0.25 mm; Gaussian smooth σ = 1 mm (σ = 2 mm sensitivity). L = smoothed arc length, D = end-to-end chord, DM = L/D. κ_a = Σ chord turning angles at chord 5 mm / L. SOAM (Bullitt) at 1 mm steps in rad/cm; soam_ip = in-plane part only. Inflections = Frenet normal rotating >90° (ΔN·ΔN > 2) between vertices turning more than 0.02 rad per 1 mm; ICM = DM × (n_infl + 1). Bends = maximal runs of 1 mm chord vertices turning more than floor × 1 mm (floor 0.02 mm⁻¹, i.e. radius of curvature < 50 mm), split at binormal flips; bend angle = cumulative turning over the run. Eleid-like grade from bend counts, ignoring the "consecutive" and diameter qualifiers.

Per-vessel results, σ 1 mm, n = 560 per trunk (LM present in 552; κ_a on LM only when ≥10 mm, n = 153) ([summary.txt](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/summary.txt), [summary.csv](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/summary.csv)):

| Vessel | Measure | Median | IQR | 2.5th [90 % CI] | 97.5th [90 % CI] | ρ with L |
|-|-|-|-|-|-|-|
| LM | L (mm) | 7.3 | 4.8 to 10.5 | 1.9 | 17.9 | |
| LM | DM | 1.011 | 1.006 to 1.024 | 1.001 | 1.085 [1.08, 1.12] | 0.41 |
| LAD | L (mm) | 131.8 | 111.1 to 145.2 | 81.0 | 169.6 | |
| LAD | DM | 1.341 | 1.225 to 1.456 | 1.123 [1.11, 1.13] | 1.716 [1.68, 1.77] | 0.80 |
| LAD | κ_a, ℓ 5 mm (mm⁻¹) | 0.057 | 0.046 to 0.071 | 0.032 [0.031, 0.034] | 0.104 [0.099, 0.108] | 0.20 |
| LAD | soam_ip (rad/cm) | 0.96 | 0.82 to 1.16 | 0.64 | 1.59 [1.53, 1.67] | 0.09 |
| LAD | bends ≥45° | 5 | 3 to 6 | 1 | 9 [9, 10] | 0.42 |
| LAD | bends ≥90° | 2 | 1 to 3 | 0 | 6 [5, 6] | 0.32 |
| LAD | 2D DM, RAO20/CRA30 | 1.201 | 1.143 to 1.288 | 1.076 | 1.527 [1.49, 1.59] | 0.71 |
| LCx | L (mm) | 83.7 | 60.1 to 107.1 | 36.1 | 138.1 | |
| LCx | DM | 1.295 | 1.165 to 1.457 | 1.054 [1.04, 1.06] | 1.697 [1.68, 1.74] | 0.84 |
| LCx | κ_a, ℓ 5 mm (mm⁻¹) | 0.052 | 0.041 to 0.066 | 0.031 [0.029, 0.031] | 0.099 [0.096, 0.106] | 0.26 |
| LCx | soam_ip (rad/cm) | 0.92 | 0.78 to 1.13 | 0.61 | 1.57 [1.53, 1.69] | 0.17 |
| LCx | bends ≥45° | 3 | 2 to 5 | 0 | 8 [8, 9] | 0.64 |
| LCx | bends ≥90° | 1 | 0 to 2 | 0 | 5 [4, 6] | 0.43 |
| LCx | 2D DM, RAO20/CAU30 | 1.157 | 1.080 to 1.270 | 1.023 | 1.471 [1.46, 1.54] | 0.69 |
| RCA | L (mm) | 103.7 | 92.1 to 116.2 | 58.5 | 140.0 | |
| RCA | DM | 1.770 | 1.550 to 2.027 | 1.175 [1.09, 1.22] | 2.549 [2.47, 2.77] | 0.69 |
| RCA | κ_a, ℓ 5 mm (mm⁻¹) | 0.045 | 0.038 to 0.056 | 0.031 [0.029, 0.031] | 0.081 [0.079, 0.086] | 0.32 |
| RCA | soam_ip (rad/cm) | 0.72 | 0.63 to 0.83 | 0.52 | 1.16 [1.12, 1.22] | 0.20 |
| RCA | bends ≥45° | 3 | 2 to 4 | 1 | 6 [5, 6] | 0.41 |
| RCA | bends ≥90° | 1 | 0 to 2 | 0 | 3 [3, 4] | 0.42 |
| RCA | 2D DM, LAO30 | 1.806 | 1.575 to 2.064 | 1.159 | 2.620 [2.55, 2.71] | 0.67 |

- Consistency with earlier repo work: RCA TI = DM − 1 median 0.77 matches the P150 value 0.77 of the earlier report, and κ_a trunk medians 0.045 to 0.057 mm⁻¹ fall inside its 0.047 to 0.084 band ([earlier report](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Vessel%20specific%20tortuosity%20math%20and%20tests.md)). κ_a medians also sit in the range of normal biplane end-diastolic mean curvature 0.050 to 0.066 mm⁻¹ ([Zhu 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2759354/)), although the scales differ.
- Bullitt SOAM including torsion: medians 7.1 to 7.3 rad/cm on every trunk, about 7 to 10 times soam_ip, with ρ with L of −0.09 to 0.02; torsion angles between consecutive osculating planes at 1 mm steps dominate it ([summary.txt](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/summary.txt)). This matches the earlier finding that SOAM reads about 2.3 rad per vertex on a straight noisy line ([earlier report, math t5](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Vessel%20specific%20tortuosity%20math%20and%20tests.md)).
- Inflections and ICM: median inflection counts 15 (LAD), 10 (LCx), 12 (RCA); ICM medians 21.2, 14.7, 23.6, ρ with L 0.65 to 0.83 ([summary.txt](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/summary.txt)).
- soam_ip and κ_a rank vessels alike (ρ 0.87 to 0.93); κ_a vs DM only ρ 0.41 to 0.53; κ_a vs bends ≥45° ρ 0.64 to 0.68 ([summary.txt](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/summary.txt)).
- Smoothing sensitivity, σ 2 mm vs 1 mm: DM medians 1.31 / 1.28 / 1.75 vs 1.34 / 1.30 / 1.77 (LAD / LCx / RCA); κ_a 0.051 / 0.046 / 0.043 vs 0.057 / 0.052 / 0.045; soam_ip drops about 30 % (LAD 0.68 vs 0.96) because it is measured at 1 mm steps ([summary_sigma2.txt](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/summary_sigma2.txt)).
- Bend-criterion prevalence ("≥3 bends ≥45°"), fraction of vessels ([sensitivity_bends.txt](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/sensitivity_bends.txt)):

| Setting | LAD 3D | LAD 2D | LCx 3D | LCx 2D | RCA 3D | RCA 2D |
|-|-|-|-|-|-|-|
| σ 1, floor 0.02 mm⁻¹ | 0.88 | 0.68 | 0.60 | 0.38 | 0.53 | 0.19 |
| σ 1, floor 0.05 | 0.76 | 0.63 | 0.47 | 0.33 | 0.34 | 0.12 |
| σ 1, floor 0.10 | 0.54 | 0.52 | 0.33 | 0.28 | 0.10 | 0.05 |
| σ 2, floor 0.02 | 0.77 | 0.59 | 0.40 | 0.29 | 0.33 | 0.22 |
| σ 2, floor 0.10 | 0.37 | 0.42 | 0.19 | 0.16 | 0.07 | 0.04 |

- Largest single bend (cumulative turning without inflection) has median 161° on the LAD, 108° on the LCx and 104° on the RCA; ≥2 bends ≥180° in 14.1 % of LADs vs 3.7 % LCx and 1.8 % RCA at σ 1 mm ([summary.txt](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/summary.txt)). The LAD value reflects the curvature around the anterior wall and apex, which the earlier report linked to the apical wrap-around variant.
- Eleid-like grade distribution (0/1/2/3), σ 1 mm: LAD 0.29 / 0.42 / 0.15 / 0.14; LCx 0.58 / 0.30 / 0.08 / 0.04; RCA 0.72 / 0.21 / 0.05 / 0.02. Patient-level "any trunk with ≥3 bends ≥45°": 0.95 in 3D, 0.80 in 2D ([summary.txt](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/summary.txt)).
- Runtime: `compute_simple.py` 61.0 s for 560 scans (0.107 s per scan median), including reading both VTKs, four vessels, all 3D measures and 256-view projections; `sensitivity_bends.py` 82 s ([summary.txt](file:///work3/s254124/imagecasx_results/tortuosity_research/simple/summary.txt)).

### Inferences
- Report set for literature comparison: 3D DM and 2D DM in a declared standard view per vessel (comparable to Zebić Mihić TI), κ_a at ℓ 5 mm as the primary curvature-per-length (comparable in spirit to SOAM in-plane and to JACC's mean turning angle, but not numerically), bends ≥45° and ≥90° counts and the binary "≥3 bends ≥45°" with floor and σ declared. Do not report Bullitt's full SOAM or ICM from these centerlines.
- Published bend-criterion prevalences (LAD 21 %, LCx 27 %, RCA 1.4 % in Li 2011) are reached only with a tight-bend floor (about 0.1 mm⁻¹, radius < 10 mm) and σ 2 mm, and even then the LAD exceeds the LCx, the reverse of the angiographic order. The likely reason is that a 3D centerline records the LAD's long curvature over the anterior wall and apex as large bends, which a grader looking at one projection does not count as "abrupt turns". A calibrated floor would need expert-graded cases, which ImageCAS-X does not provide. Until then, bend counts should be presented as a scale-dependent descriptive measure, not as a replication of the angiographic prevalence.
- LM tortuosity is not meaningful (median length 7.3 mm, DM 1.011, κ_a undefined in 72 % of cases), consistent with the earlier report's recommendation to report LM geometry by bifurcation angle rather than tortuosity.
- The DM reference intervals above are marginal. Because DM correlates with L at ρ 0.69 to 0.84 and differs by dominance, the thesis should publish length- and dominance-conditional centiles for DM, and marginal intervals for κ_a (whose length correlation is weak).

### Gaps
- Age and sex covariates do not exist in ImageCAS-X, so the sex effect documented in every clinical study (Li 2011, JACC 2026, Groves 2009) cannot be modelled.
- The Disease column was deliberately not read, so the training distribution mixes patients with and without CAD; whether a "disease-free" subset would shift the intervals is untested here.
- Quantile regression / GAMLSS conditional centiles, a heart-size proxy from total tree length, and validation-split verification were not run in this pass.
- The bend algorithm counts cumulative turning between inflections; an alternative "net direction change within a fixed arc window" definition was not tested.
