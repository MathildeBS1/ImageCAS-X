# Turning angle method for 3D centerlines: how the vascular tortuosity literature computes angles and curvature

Thesis method under review: resample the RCA centerline so consecutive points are a fixed Euclidean chord ell apart (for example 5 mm), take theta_j = arccos(u_j . u_{j+1}) between consecutive unit chord vectors (unsigned, 3D), and report T_ell = (1/L_c) sum theta_j with L_c = (number of steps) x ell, claimed to be "mean absolute curvature measured at scale ell" in rad/mm.

Evidence levels: "full text" means the primary source (or its relevant methods section, or source code) was read in this round; "abstract" means only the PubMed abstract; "project note" means the claim comes from a note in this repository that records its own full-text reading; "derivation" means arithmetic by this researcher, stated by no source.

## Q1. Bullitt et al. 2003 SOAM: exact computation, normalisation, relation to the thesis method, weaknesses

### Takeaway
SOAM is, term for term, the thesis metric plus a torsion term, computed at one-voxel spacing instead of a chosen chord ell: per-vertex in-plane angle IP_k = arccos of the dot product of consecutive unit difference vectors (identical to the thesis theta_j), a torsional angle TP_k between successive osculating-plane normals, combined as sqrt(IP_k^2 + TP_k^2), summed and divided by total polyline length, reported in rad/cm. Dropping TP_k gives exactly T_ell with ell = 1 voxel.

### Cited Findings
- Input: "a set of ordered 3D points indicating the spatial position of each vessel skeleton, regularly sampled at intervals of the length of one voxel" (full text). The skeleton comes from Aylward's intensity-ridge extraction and "is defined as a spline, which we subsequently sample at regularly spaced intervals"; no additional smoothing before angle computation is stated — [Bullitt et al. 2003, PMC2430603](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- In-plane angle: T1 = P_k - P_{k-1}, T2 = P_{k+1} - P_k, IP_k = arccos((T1/|T1|) . (T2/|T2|)), from 0 (collinear) to 180 degrees; "If the three points are collinear, the in-plane angle will thus be reported as 0" (full text) — [Bullitt 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- Torsional angle: TP_k = arccos(((T1 x T2)/|T1 x T2|) . ((T2 x T3)/|T2 x T3|)), the angle between successive osculating-plane normals; combined CP_k = sqrt(IP_k^2 + TP_k^2) (full text) — [Bullitt 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- Normalisation: SOAM = (sum_{k=1}^{n-3} CP_k) / (sum_{k=1}^{n-1} |P_k - P_{k-1}|), i.e. divided by total curve length, units radians/cm (full text) — [Bullitt 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- No explicit handling of the torsion term when T1 x T2 is near zero was found for SOAM; the only singularity handling described (skip a point if a length is < 1e-6 cm and redefine the frame) belongs to the inflection count metric (full text, via extraction tool) — [Bullitt 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- Stated limitations are about resolution, not SOAM specifically: "the resolution at which the MRA data are obtained may affect tortuosity values"; the paper also notes that tight coils "do not add greatly to total path length", a weakness of DM and ICM that SOAM was introduced to address. SOAM separated abnormal from normal vessels in all three tumour cases with high-frequency, low-amplitude coils — [Bullitt 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/); abstract summary in thesis refs.bib entry `bullitt2003tortuosity`.
- Kashyap 2022 (the only systematic coronary CTA comparison) did not include SOAM among its tested metrics; its Table 1 lists tortuosity index, average absolute curvature, RMS curvature and average squared-derivative curvature only (full text) — [Kashyap et al. 2022, PMC8764056](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)

### Inferences
- The thesis T_ell is SOAM with (a) TP_k set to zero and (b) sampling step ell (5 mm) instead of one voxel. The division is the same (sum of angles / polyline length). The thesis can honestly describe T_ell as "the in-plane component of Bullitt's SOAM, evaluated on a chord-respaced polyline" (derivation).
- Dropping the torsion term is defensible and arguably an improvement: TP_k is an angle between normals of nearly-degenerate planes whenever IP_k is small, so on a nearly straight noisy segment TP_k is essentially a random angle in [0, pi], which inflates SOAM on straight vessels. Bullitt gives no guard for this (derivation from the formula; no source tested it in this round).
- At one-voxel spacing, SOAM's unsigned angles accumulate voxel-staircase noise. Because every noise-induced angle is positive, the bias does not cancel; SOAM at 1 voxel is therefore expected to read high on straight vessels. The thesis's coarse ell is a direct remedy for this, trading spatial resolution for noise suppression (derivation; consistent with the Kjeldsberg resolution-sensitivity finding below).

### Gaps
- The exact published text of Bullitt's Discussion on SOAM sensitivity was only seen through an extraction tool; no quantitative noise or sampling sensitivity experiment for SOAM was found in Bullitt 2003.
- No study found that measured SOAM's test-retest reproducibility or its dependence on sampling step.

## Q2. Other 3D metrics: how angles and curvature are computed (Hart, Grisan, O'Flynn, Johnson and Dougherty, Piccinelli/VMTK, Choi, Kashyap, Ciurica, Tello)

### Takeaway
The field splits into two families. (1) Angle-sum metrics on a polyline (Bullitt SOAM, Grisan's MAC and TN, Tello, Bribiesca's slope chain code), which differ mainly in spacing and normaliser. (2) Pointwise curvature kappa(s) integrated along a smoothed, finely resampled curve (Hart's tc/tsc, Kashyap's average absolute curvature, VMTK, O'Flynn, Johnson and Dougherty, Choi). The thesis metric is a member of family 1 that is a consistent discretisation of family 2's average absolute curvature kappa_a.

### Cited Findings
- Hart et al. 1999 define curvature-integral tortuosity: tc = integral of |kappa| dl and tsc = integral of kappa^2 dl over the vessel, with ratios to chord or length proposed to remove length dependence (full text of Grisan's review of Hart, Eq. 9) — [Grisan et al. 2008, IEEE TMI, local PDF p. 312](https://doi.org/10.1109/TMI.2007.904657); refs.bib note: Hart's metric is squared curvature normalised by path length — [Hart 1999](https://doi.org/10.1016/S1386-5056(98)00163-4)
- Grisan's review also defines the Mean Angle Change metric: theta(i) = arccos(v_{i+n} . v_{i-n}) with direction vectors from sample i to i+n and i-n, and MAC = (1/(N - 2n)) sum theta(i), "where n is a fixed, user-defined parameter, which provides a regularization of the estimated direction". This is an angle sum divided by the number of points, not by length, with a user-chosen stride n as the scale parameter (full text, Eqs. 11 to 14) — [Grisan 2008, p. 312 to 313](https://doi.org/10.1109/TMI.2007.904657)
- Grisan also describes an absolute direction-angle count TN = number of centre points with theta(i) >= pi/6 (Eq. 15), and Bullitt's ICM = (n_ic + 1) L_chi / L_c (Eq. 16) (full text) — [Grisan 2008, p. 313](https://doi.org/10.1109/TMI.2007.904657)
- Grisan's own tau = ((n-1)/n)(1/L_c) sum (L_c,si / L_chi,si - 1) "has a dimension of 1/length and thus may be interpreted as a tortuosity density" (full text, Eq. 19) — [Grisan 2008, p. 313](https://doi.org/10.1109/TMI.2007.904657)
- Kashyap et al. 2022 (coronary CTA, n = 127 without CAD): average absolute curvature kappa_a = (integral_{t1}^{t2} |kappa(t)| dt) / L and RMS curvature = integral of kappa^2 / L, attributed to Hart; total (unnormalised) curvature integrals were excluded "since these metrics are not scale invariant and dependent on the arc length of the vessels". Centerlines computed and smoothed in VMTK from a Taubin-smoothed surface (passband 0.03, 30 iterations), each branch cut at 10 mm from the bifurcation, and "resampled with equal spacing of 0.01 mm to minimize errors that would be introduced based on discretization" (full text) — [Kashyap 2022, PMC8764056](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- VMTK (vtkvmtkCenterlineGeometry, the implementation behind Piccinelli et al. 2009): optional Laplacian line smoothing before geometry (defaults: 100 iterations, smoothing factor 0.01); first derivative xp = (p_{j+1} - p_{j-1}) / (|e0| + |e1|); second derivative xpp = ((p_{j+1}-p_j)/|e1| - (p_j - p_{j-1})/|e0|) / ((|e0|+|e1|)/2), i.e. the difference of consecutive unit edge vectors divided by the mean edge length; curvature = |xp x xpp| / |xp|^3; torsion from a further finite difference; VMTK's "Tortuosity" output is L / chord - 1 (source code) — [VMTK source, vtkvmtkCenterlineGeometry.cxx](https://github.com/vmtk/vmtk/blob/master/vtkVmtk/ComputationalGeometry/vtkvmtkCenterlineGeometry.cxx)
- Piccinelli et al. 2009 present the VMTK centerline-based framework, "founded upon solid computational geometry criteria, which confer robustness of the analysis with respect to the high variability of in vivo vascular geometry" (abstract only) — [Piccinelli et al. 2009, PubMed 19447701](https://pubmed.ncbi.nlm.nih.gov/19447701/)
- O'Flynn et al. 2007 computed 3D curvature from MRA centerlines of three subjects and report it per length: renal arteries "mean average values of 0.114 +/- 0.015 and 0.070 +/- 0.019 mm(-1)" (abstract only; smoothing and sampling not visible) — [O'Flynn et al. 2007, PubMed 17431787](https://pubmed.ncbi.nlm.nih.gov/17431787/)
- Johnson and Dougherty 2007 fit approximating polynomial splines and use unit-speed 3D curvature of the smoothest path; "The use of approximating polynomial spline-fitting obviates the need for arbitrary filtering of mid-line data which is necessary with other tortuosity indices"; two of three metrics "scale invariant, additive, and ... independent of the resolution of the imaging system"; RMS curvature of the smoothest path best for high-frequency coiling (abstract only) — [Johnson and Dougherty 2007, PubMed 16996773](https://pubmed.ncbi.nlm.nih.gov/16996773/)
- Choi, Cheng, Wilson and Taylor 2009 (Stanford, includes coronary arteries): lumen centroids via 2D threshold plus level set, and "an optimal Fourier smoothing technique was developed to eliminate spurious irregularities of the centerline connecting the centroids" before computing curvature change and axial twist (abstract only) — [Choi et al. 2009, PubMed 19002584](https://pubmed.ncbi.nlm.nih.gov/19002584/)
- Ciurica et al. 2019 review: arterial tortuosity lacks "a standardized, universally accepted method", with tortuosity index / distance metric the most common (search-snippet level only) — [Ciurica et al. 2019, Hypertension](https://www.ahajournals.org/doi/10.1161/HYPERTENSIONAHA.118.11647)
- Tello Ayala et al. 2026 (2D angiographic RCA, 38,691 images): per skeleton point, the turning angle between edges x_{i-1}x_i and x_i x_{i+1}, "absolute value, normalized by pi", global score = mean over points; point spacing is one skeleton pixel (project note of full-text reading) — [docs_thesis/papers/telloayala2026tortuosity.md; PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/). This conflicts with the brief's statement that Tello's equation uses signed angles: the project's full-text note records absolute values. The thesis should check Tello's equation before citing either reading.
- Tello's discrete-curvature score correlated only r = 0.116 with arc/chord in 22,334 patients (project note; Supplemental Table 10 not opened) — [project note](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)

### Inferences
- The thesis sits exactly between the two families: it has family 1's mechanics (arccos of chord dot products, like Bullitt, Grisan MAC, Tello) and family 2's normalisation and units (per mm, like Hart, Kashyap, O'Flynn, Bullitt). The closest single published relatives are (i) Bullitt's SOAM without torsion and (ii) Bribiesca's slope chain code, which also uses constant-length chords (Q4) (derivation).
- VMTK's finite-difference curvature is itself a turning-angle estimator. With uniform spacing ell, xp = (u0 + u1)/2 with norm cos(theta/2), and xpp = (u1 - u0)/ell with norm 2 sin(theta/2)/ell, orthogonal to xp, so kappa_VMTK = 2 sin(theta/2) / (ell cos^2(theta/2)). Relative to theta/ell this is 1.002 at theta = 0.1 rad, 1.019 at 0.3 rad, 1.054 at 0.5 rad and 1.245 at 1 rad (derivation, numerically checked). So on the same polyline, the thesis per-vertex theta/ell and VMTK's curvature agree within about 2 % for turning angles up to about 17 degrees; they diverge only at sharp turns, where VMTK reads higher.
- What the "best" curvature studies do that the thesis does not: they separate denoising (Laplacian smoothing, Fourier smoothing, spline approximation, surface Taubin smoothing) from discretisation (very fine resampling, 0.01 mm in Kashyap) and then estimate pointwise curvature. The thesis instead lets one parameter, ell, act as both denoiser and discretiser. Neither approach is validated as superior for coronary CTA; the explicit-smoothing approach has more precedent, the chord approach has one honest scale parameter and no hidden smoother settings (derivation).

### Gaps
- Piccinelli 2009 full text, O'Flynn 2007 and Choi 2009 methods, and Johnson and Dougherty's spline details were not accessible (Springer and ScienceDirect blocked); only abstracts and VMTK source were read.
- Kim/Han-type coronary bend definitions (count of bends > 45 degrees) and Ciurica's full definitions were not re-researched in this round; earlier project reports ("Choosing a coronary tortuosity descriptor.md", "Scalar tortuosity metrics for CAD models.md") already cover bend-count definitions.
- No source compared an angle-sum metric against a smoothed-spline kappa_a on the same coronary centerlines.

## Q3. How papers handle discretisation scale and noise in voxel-derived centerlines

### Takeaway
Most papers either sample at the native resolution (Bullitt, one voxel; Tello, one pixel) and accept noise, or smooth explicitly and then resample finely (Kashyap 0.01 mm after VMTK smoothing; VMTK defaults 100 Laplacian iterations; Choi Fourier smoothing; Johnson and Dougherty splines). Grisan's MAC uses a stride n as a regulariser, which is the closest published analogue to the thesis's ell. Evidence that resolution dominates turn-based metrics is strong.

### Cited Findings
- Bullitt: one-voxel sampling on a spline-defined skeleton, no explicit additional smoothing; acknowledges resolution may affect values (full text) — [Bullitt 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- Grisan's MAC stride n "provides a regularization of the estimated direction" (full text) — [Grisan 2008, p. 313](https://doi.org/10.1109/TMI.2007.904657)
- Kashyap: VMTK smoothing then 0.01 mm resampling "to minimize errors that would be introduced based on discretization" (full text) — [Kashyap 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- VMTK defaults: 100 smoothing iterations, factor 0.01, Laplacian (source code) — [VMTK source](https://github.com/vmtk/vmtk/blob/master/vtkVmtk/ComputationalGeometry/vtkvmtkCenterlineGeometry.cxx)
- Johnson and Dougherty: spline approximation instead of "arbitrary filtering", designed "to explicitly handle the challenge of noisy data" (abstract) — [PubMed 16996773](https://pubmed.ncbi.nlm.nih.gov/16996773/)
- Choi et al.: "optimal Fourier smoothing" of centroid centerlines (abstract) — [PubMed 19002584](https://pubmed.ncbi.nlm.nih.gov/19002584/)
- Carotid sensitivity study: the bend count ranged from 3 to 33 depending on centerline resolution, while smoothing strength moved it only between 6 and 7 (project report citing full text) — [Kjeldsberg et al. 2021, PMC8626959](https://pmc.ncbi.nlm.nih.gov/articles/PMC8626959/) via reports/Merged tortuosity methods for coronaries.md
- In discrete differential geometry the turning angle at a vertex is the integrated curvature over the vertex's dual cell, and pointwise discrete curvature is k_i = 2 psi_i / (|e_{i-1/2}| + |e_{i+1/2}|); alternative formulas 4 sin(psi/2)/(...) and 2 tan(psi/2)-based ones exist, and they do not share all smooth properties (the sine version violates the discrete turning-number theorem) (full text of lecture notes) — [Vouga, Lectures in Discrete Differential Geometry 1, pp. 6 to 9](https://www.cs.utexas.edu/~evouga/uploads/4/5/6/8/45689883/notes1.pdf); the 2 tan(phi/2) variant is used in discrete elastic rods — [Bergou et al. 2008, refs.bib](https://doi.org/10.1145/1360612.1360662)

### Inferences
- Noise bias of unsigned angles scales like sigma/ell per vertex and sigma/ell^2 per mm (earlier project derivation: spurious density about 3 sigma / ell^2). With an assumed sigma of 0.25 mm and ell = 5 mm this is 3 x 0.25 / 25 = 0.03 rad/mm, which is not negligible relative to typical coronary kappa_a values of order 0.05 to 0.1 mm^-1 (O'Flynn's renal 0.07 to 0.11 mm^-1 gives the order of magnitude for arteries). The thesis should quantify this floor on straight synthetic lines with realistic jitter (derivation; typical coronary kappa_a range not sourced here).
- The coarse chord also low-pass filters true geometry: curvature features with wavelength shorter than about 2 ell are aliased or lost. At ell = 5 mm, bends tighter than roughly a 5 to 10 mm length are undersampled. The metric is therefore "mean absolute curvature of the curve smoothed at scale ell", not of the curve itself (derivation).
- Because every family is scale-dependent, the best practice supported by this literature is to report the scale explicitly and show a sweep (Richardson-style or rank stability across ell), which the project's tortuosity/CLAUDE.md already requires.

### Gaps
- No coronary CTA paper reporting a sensitivity sweep of an angle-sum metric across sampling step was found.
- Centerline jitter magnitude for ImageCAS reference centerlines has not been sourced; the sigma used above is an assumption.

## Q4. Does anyone use chord (Euclidean) respacing rather than arc-length resampling?

### Takeaway
Yes: Bribiesca's Slope Chain Code (SCC) family does exactly this, placing constant-length straight segments whose endpoints touch the curve and taking the angle between contiguous segments. This is the one established tortuosity lineage that matches the thesis discretisation; Mateos et al. 2024 and a 2025 retinal SCC paper belong to it. Vascular curvature papers (VMTK, Kashyap, Bullitt) resample along arc length or at voxel spacing instead.

### Cited Findings
- "The SCC of a curve is obtained by placing straight-line segments of constant length around the curve (the endpoints of the straight-line segments always touching the curve), and calculating the slope changes between contiguous straight-line segments scaled to a continuous range from -1 to 1"; the representation is invariant to translation and rotation, optionally scaling, and "does not use a grid" (search-snippet level, via the Mateos 2024 PMC record and ResearchGate listings) — [Mateos et al. 2024, PMC11149256](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11149256/); [Bribiesca, A chain code for representing 3D curves](https://www.researchgate.net/publication/223490302_A_chain_code_for_representing_3D_curves)
- SCC tortuosity is tau = sum |a_n| with a_n = theta_n / pi (Mateos Eq. 5; the project's full-text note), i.e. total absolute turning divided by pi, not normalised by length (project report citing full text) — [Mateos 2024](https://doi.org/10.1186/s12880-024-01312-6) via reports/Merged tortuosity methods for coronaries.md
- A 2025 paper titled "Slope Chain Code-based scale-independent tortuosity measurement on retinal vessels" exists (Experimental Eye Research, S0014483525000570); its method details were blocked (title only) — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0014483525000570)
- The ESCC variant uses variable segment lengths for scale invariance (snippet level) — [Bribiesca ESCC, ResearchGate](https://www.researchgate.net/publication/331896259_A_Chain_Code_for_Representing_High_Definition_Contour_Shapes)
- Milnor's total curvature of a polygon is the sum of its exterior (turning) angles, and the total curvature of a curve is the supremum over all inscribed polygons (secondary summary) — [Wikipedia: Total curvature](https://en.wikipedia.org/wiki/Total_curvature); [Sullivan, Curves of Finite Total Curvature](https://link.springer.com/chapter/10.1007/978-3-7643-8621-4_7)

### Inferences
- Chord respacing yields a polygon inscribed in the centerline (vertices on the curve), which is exactly the object in Milnor's definition. Consequence: for a noise-free smooth curve, the thesis numerator sum theta_j can never exceed the true total curvature integral of |kappa|, and the denominator N ell never exceeds the arc length. This is a principled justification for chord respacing that no vascular paper states: it makes T_ell a well-defined inscribed-polygon estimator converging to kappa_a as ell -> 0 on smooth curves (derivation).
- Chord versus arc-length respacing differ only when the curve bends appreciably within one step; with ell = 5 mm and coronary radii of curvature typically larger than ell, the chord and arc length of one step differ by roughly ell^3 kappa^2 / 24, a sub-percent effect (derivation; typical coronary kappa not sourced here). The choice is therefore mainly one of cleanliness (equal chords make every theta_j comparable and every step exactly ell), not of accuracy.
- A practical justification the thesis can give: chord respacing produces equal edge lengths, which is the condition under which the discrete-curvature formula k_i = 2 theta_i / (|e_{i-1/2}| + |e_{i+1/2}|) reduces to theta_i / ell (Vouga), so T_ell is exactly the mean of a standard discrete curvature (derivation from Vouga's Eq. 1).

### Gaps
- No vascular (non-SCC) paper was found that explicitly justifies chord over arc-length respacing.
- The 2025 retinal SCC paper's choice of segment length and normalisation could not be read.

## Q5. Normalisation: per length vs per point vs by pi; units reported

### Takeaway
Dividing total turning by length is the majority convention in 3D vascular work (Bullitt rad/cm; Hart and Kashyap 1/L; Grisan 1/length; O'Flynn mm^-1). Dividing by the number of points (Grisan's MAC, Tello) or by pi (SCC, Tello) is the retinal and chain-code convention. At fixed spacing ell, the per-point mean equals the per-length value times ell (up to an end correction), so the choices are equivalent only when spacing is fixed and reported.

### Cited Findings
- Bullitt SOAM: divided by total length, radians/cm (full text) — [Bullitt 2003](https://pmc.ncbi.nlm.nih.gov/articles/PMC2430603/)
- Kashyap: kappa_a divided by L; unnormalised totals excluded as not scale-invariant (full text) — [Kashyap 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- Grisan tau: dimension 1/length, a "tortuosity density"; MAC divided by N - 2n points (full text) — [Grisan 2008](https://doi.org/10.1109/TMI.2007.904657)
- O'Flynn: curvature in mm^-1 (abstract) — [PubMed 17431787](https://pubmed.ncbi.nlm.nih.gov/17431787/)
- Tello: mean per point of |angle|/pi, dimensionless, spacing = one pixel (project note) — [PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)
- SCC: sum |theta|/pi, not normalised by length (project report) — [Mateos 2024](https://doi.org/10.1186/s12880-024-01312-6)
- Bergou et al.: discrete bending energy sums over vertices divided by the mean edge length (refs.bib note) — [Bergou 2008](https://doi.org/10.1145/1360612.1360662)

### Inferences
- The thesis L_c = N steps x ell but the sum has N - 1 interior angles, so T_ell = ((N-1)/N) x mean(theta_j / ell). For a 100 mm RCA at ell = 5 mm (N = 20) this is a 5 % downward bias versus the mean discrete curvature; for 25 mm segments (N = 5) it is 20 %. It is length-dependent, which matters for the thesis's criterion of low correlation with vessel length. Either divide by (N - 1) ell, or state the definition as total turning per polyline length (which is what Bullitt does: SOAM also sums n-3 angles over n-1 edges) (derivation).
- Dividing by pi (Tello, SCC) is a pure rescale when angles are unsigned; it changes units, not rankings. Tello's per-point mean at pixel spacing is not comparable across images with different magnification, which the thesis fixes by using mm and a fixed ell (derivation).
- Units: rad/mm is correct for T_ell and matches Bullitt (rad/cm) and O'Flynn/Kashyap-style mm^-1 (radians being dimensionless). Values at different ell are not directly comparable, so ell must accompany every number (derivation).

### Gaps
- No source found that reports reference ranges of kappa_a or SOAM for normal coronaries at a stated sampling scale.

## Q6. Is turning angle per length recognised as a curvature estimator?

### Takeaway
Yes. In discrete differential geometry the turning angle at a polygon vertex is the standard "integrated curvature", total turning equals Milnor total curvature, and theta_i / (mean adjacent edge length) is the standard pointwise discrete curvature. The thesis claim "mean absolute curvature measured at scale ell, rad/mm" is therefore mathematically sound, with two qualifiers: it is the curvature of the ell-inscribed polygon (a smoothed curve), and the (N-1)/N end factor.

### Cited Findings
- "One relationship from smooth differential geometry is the equivalence of integrated curvature and turning angle"; discrete curvature k_i = 2 psi_i / (|e_{i-1/2}| + |e_{i+1/2}|) derived from the winding-number theorem and, independently, from area inflation by circle sectors; alternatives with sin and tan exist and none satisfies every smooth property (full text) — [Vouga, DDG notes 1](https://www.cs.utexas.edu/~evouga/uploads/4/5/6/8/45689883/notes1.pdf)
- Total curvature of a polygon = sum of turning angles (Milnor), and curve total curvature = supremum over inscribed polygons (secondary) — [Wikipedia: Total curvature](https://en.wikipedia.org/wiki/Total_curvature)
- In vascular work, average absolute curvature is (1/L) integral |kappa| ds and was the best coronary metric against low wall shear stress in Kashyap (full text; R^2 values in the project's earlier reports) — [Kashyap 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8764056/)
- VMTK's finite-difference curvature on a polyline is built from the difference of consecutive unit edge vectors divided by mean edge length (source code), i.e. a turning-angle based estimator — [VMTK source](https://github.com/vmtk/vmtk/blob/master/vtkVmtk/ComputationalGeometry/vtkvmtkCenterlineGeometry.cxx)

### Inferences
- T_ell = discrete average absolute curvature kappa_a (Hart, Kashyap) of the ell-inscribed polygon, which is also SOAM's in-plane part (Bullitt) and, times ell/pi, SCC tortuosity per segment (Bribiesca/Mateos). The thesis can cite all three lineages as the same quantity at different scales and normalisers (derivation).
- For theta up to about 0.3 rad (17 degrees) per 5 mm step, theta/ell agrees with VMTK's curvature within 2 %, and with the sine and tan variants within 1 %, so the choice among discrete curvature formulas is immaterial except at sharp bends (derivation, numerically checked: 2 sin(t/2)/t = 0.996 and 2 tan(t/2)/t = 1.008 at t = 0.3).
- What the thesis should not claim: that T_ell estimates the curvature of the true vessel independently of ell. Upward noise bias (small ell) and downward inscribed-polygon bias (large ell) move it in opposite directions, and ell selects the balance. "At scale ell" in the claim is essential.

### Gaps
- No vascular paper found that explicitly names the angle-sum-per-length metric a "curvature estimator" and validates it against analytic curves; SOAM's paper calls it a tortuosity metric, not a curvature estimate.
