# Extracting vessel diameter before, at and after a bifurcation (coronary and cross-domain)

Scope note: ~27 tool calls. Several primary papers (Antiga & Steinman 2004 IEEE TMI, Piccinelli 2009 IEEE TMI, Thomas 2005 Stroke, Ingebrigtsen 2004 J Neurosurg, Stanton 1995) were paywalled or blocked (403 / captcha). Their definitions below come from the VMTK docs/source code (which implement Antiga/Piccinelli) and from later open papers that quote them (Bijari et al.). Claims taken only from search snippets are marked "(snippet only)".

## Q1. QCA bifurcation algorithms (EBC, Medina segments, POC, carina) and translation to 3D CT/IVUS

### Takeaway
The European Bifurcation Club (EBC) standard is a segment model around a central "polygon of confluence" (POC): proximal main vessel (PMV), distal main vessel (DMV) and side branch (SB), with 5 mm segments beyond the treated region and a 3 mm SB ostial segment. Reference diameters in and near the POC are not interpolated but derived from fractal laws (Finet, Huo-Kassab, Murray). CT and IVUS studies translate this to fixed-mm cross-sections: 5 mm proximal to the carina, at the carina, 5 mm distal, and reference diameters taken at the healthiest point within 10 mm.

### Cited Findings
- EBC consensus: in the bifurcation six-segment model (BSM6) segments 2, 3 and 5 are the "treated segment" (PMV, DMV, SB); "Segments 1, 4, and 6 correspond to 5 mm segments beyond the treated segment." In the 11-segment model (BSM11), "Segment 8 ... reflects 3 mm ostial segments of the SB." — [EBC consensus update, EuroIntervention (Collet et al. 2017)](https://eurointervention.pcronline.com/article/quantitative-angiography-methods-for-bifurcation-lesions-a-consensus-statement-update-from-the-european-bifurcation-club); [PubMed 28067200](https://pubmed.ncbi.nlm.nih.gov/28067200/)
- Point of bifurcation (POB) in CAAS: "the mid-point of the largest possible circle touching all three contours" (i.e. a 2D maximum inscribed circle at the junction). — [EBC consensus update](https://eurointervention.pcronline.com/article/quantitative-angiography-methods-for-bifurcation-lesions-a-consensus-statement-update-from-the-european-bifurcation-club)
- The POC is the central bifurcation region "which behaves differently from a single-vessel analysis"; inside it dedicated algorithms replace single-vessel diameter calculation. — [EBC consensus update](https://eurointervention.pcronline.com/article/quantitative-angiography-methods-for-bifurcation-lesions-a-consensus-statement-update-from-the-european-bifurcation-club)
- Fractal reference laws quoted by the EBC: Finet, D_mv = 0.678 (D_dv + D_sb); Huo-Kassab, D_mv^(7/3) = D_dv^(7/3) + D_sb^(7/3). — [EBC consensus update](https://eurointervention.pcronline.com/article/quantitative-angiography-methods-for-bifurcation-lesions-a-consensus-statement-update-from-the-european-bifurcation-club)
- Single-vessel QCA is inaccurate at bifurcations because of the diameter "step-down"; dedicated software applies fractal geometry to estimate reference diameters. In the 11-segment scheme segment 7 is the POC; to define "bifurcating" cross-sections of the two daughters within the POC, "the POC area is divided into two elliptical shapes along the two centre lines based on the virtual vessel contours." — [Novel dedicated 3D QCA methodology, EuroIntervention](https://eurointervention.pcronline.com/article/a-novel-dedicated-3-dimensional-quantitative-coronary-analysis-methodology-for-bifurcation-lesions)
- CAAS 5 3D bifurcation: "The POC region in 3-D begins at the position where the 3-D centre line bifurcates and ends where the main and side branches stop coinciding with each other." The "peanut-shaped" POC is filled with Catmull-Rom interpolated virtual contours; missing contour points inside the POC are "calculated from contours outside POC by polynomial interpolation to create a virtual ellipsoid area." Diameters reported: equivalent diameter (area to circle), minimum luminal diameter = "the maximum circle that fits through the 3-D reconstruction", maximum = "the minimum circle that encloses" it. Bifurcation angle vectors have length "half the size of the equivalent luminal diameter at the start and end of the POC." — [3D QCA methodology, EuroIntervention](https://eurointervention.pcronline.com/article/a-novel-dedicated-3-dimensional-quantitative-coronary-analysis-methodology-for-bifurcation-lesions)
- CT vs IVUS "true" bifurcation study: reference vessel diameters of MB (proximal, distal) and SB taken "at the point least affected by atherosclerosis of up to 10 mm from the bifurcation's stenosis"; MB lumen/vessel areas "5 mm proximal to the carina", "at the carina level" and "5 mm distal to the carina", plus at MB MLD and "at the SB ostium". CT software Vital Vitrea Advanced 6.2; IVUS QIvus 3.0 (Medis). — [Frontiers Cardiovasc Med 2023](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2023.1292517/full)
- Fractal laws applied to angiography-derived algorithms (left main) are reported to improve reference-diameter accuracy. — [Fractal laws for bifurcation QCA, PMC12145935](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12145935/)
- CTA computational atlas of normal coronary anatomy (300 subjects): diameter "calculated every 0.5 mm from the ostium" (for LAD/LCx, from the bifurcation) by cutting the mesh with a plane normal to the centreline, area A to effective radius by A = πR²; at the bifurcation "in this region where the area is maximal within the bifurcation, an ellipse was fitted yielding two diameters" (eccentricity). Angles "defined as the average in the 5-10 mm depth interval where variation is typically small." LM ostium diameter 3.7 mm (IQR 3.2 to 4.1), LM length 10.5 ± 5.3 mm; measured Finet ratio 0.6576 ± 0.083 vs theoretical 0.678. — [Medrano-Gracia et al., EuroIntervention](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)
- Meta-analysis of Murray's law in coronaries: pooled flow-diameter exponent 2.39 (95% CI 2.24 to 2.54), close to Kassab's 7/3; humans 2.42, animals 2.36; studies used QCA, IVUS and CTA with heterogeneous measurement definitions. Finet's law was derived from IVUS of 173 epicardial bifurcations. — [Systematic review, PMC11380967](https://pmc.ncbi.nlm.nih.gov/articles/PMC11380967/)

### Inferences
- The EBC framework maps naturally onto a labelled centerline graph: PMV = parent upstream of POC, DMV and SB = daughters downstream of POC; POC = your junction sphere region. The 5 mm "beyond" segments and 3 mm SB ostial segment give citable fixed-mm windows. Your current rule, median over [r_J, r_J + 3] mm, corresponds most closely to the EBC "3 mm SB ostial segment" but starting at the POC exit rather than the centreline split.
- For healthy trees, "reference diameter" in the EBC sense (healthiest point within 10 mm) collapses to a local median/mean, so a median over a window is a defensible 3D analogue.
- The atlas' 0.5 mm-step plane-section area approach is the most direct CTA precedent for replacing EDT radius with area-equivalent radius.

### Gaps
- The exact CAAS 2D segment lengths for the BSM11 ends (beyond 5 mm / 3 mm) and QAngio CT's bifurcation definitions could not be retrieved (vendor manuals not public).
- Medina classification itself defines lesion location only (PMV, DMV, SB 0/1 codes) and has no diameter windows; not separately fetched.

## Q2. VMTK bifurcation reference system (Antiga & Steinman 2004, Piccinelli 2009) and cross-section alternatives

### Takeaway
VMTK defines the junction via tube intersection of maximum-inscribed-sphere (MIS) tubes: each centerline gets two reference points, one where it enters another centerline's tube and one "one maximum inscribed sphere upstream". The origin is the MIS-weighted barycenter of the four reference points. Measurements "before/after" are then made at distances expressed in numbers of inscribed-sphere radii (default 1) from the bifurcation, as surface cross-section area, min/max diameter and shape.

### Cited Findings
- Tube function: "Each centerline is associated to the radius of the maximum inscribed sphere" and "a tube is a function with support in 3D and values negative inside and positive outside." — [VMTK Branch Splitting tutorial](https://github.com/vmtk/vmtk.github.com/blob/master/tutorials/BranchSplitting.md) ([web](http://www.vmtk.org/tutorials/BranchSplitting.html))
- Reference points: "For each bifurcation, we identify two points on each centerline (which we termed the reference points): the first is located where the centerline intersects another centerline's tube" and "the second is located one maximum inscribed sphere upstream." — [VMTK Branch Splitting](http://www.vmtk.org/tutorials/BranchSplitting.html)
- Bifurcation group is "blanked": "The bifurcation tract group is never taken into account for splitting the surface." Surface splitting uses the zero level of (tube values of branch group) minus (tube values of the rest). Output arrays CenterlineId, TractId, GroupId, Blanking. — [VMTK Branch Splitting](http://www.vmtk.org/tutorials/BranchSplitting.html); implemented in [vmtkbranchclipper.py](https://github.com/vmtk/vmtk/blob/master/vmtkScripts/vmtkbranchclipper.py)
- Reference system: origin = "the barycenter of the four reference points weighted by the surface of the maximum inscribed sphere"; plane normal = "the normal to the polygon defined by the four reference points"; UpNormal points parent to daughters. Bifurcation vectors produce InPlane/OutOfPlane angles. Command: `vmtkbranchextractor -radiusarray@ MaximumInscribedSphereRadius --pipe vmtkbifurcationreferencesystems`. — [VMTK Geometric Analysis tutorial](https://github.com/vmtk/vmtk.github.com/blob/master/tutorials/GeometricAnalysis.md); [vmtkbifurcationreferencesystems.py](https://github.com/vmtk/vmtk/blob/master/vmtkScripts/vmtkbifurcationreferencesystems.py)
- `vmtkcenterlineoffsetattributes -referencegroupid` re-zeroes abscissas at the bifurcation origin so attributes can be compared across a population. — [VMTK Geometric Analysis](http://www.vmtk.org/tutorials/GeometricAnalysis.html)
- `vmtkbifurcationsections`: option `NumberOfDistanceSpheres` default 1, "distance from the bifurcation at which the sections have to be taken; the distance is expressed in number of inscribed spheres". Outputs: BifurcationSectionArea, BifurcationSectionMinSize ("minimum diameter"), BifurcationSectionMaxSize, BifurcationSectionShape ("ratio between minimum and maximum diameter"), BifurcationSectionClosed, BifurcationSectionOrientation (upstream/downstream), BifurcationSectionDistanceSpheres. Requires a surface and centerlines already split into branches. — [vmtkbifurcationsections.py source](https://github.com/vmtk/vmtk/blob/master/vmtkScripts/vmtkbifurcationsections.py)
- Primary references: Antiga L, Steinman DA, "Robust and objective decomposition and mapping of bifurcating vessels", IEEE TMI 23(6), 2004; Piccinelli M, Veneziani A, Steinman DA, Remuzzi A, Antiga L, "A framework for geometric analysis of vascular structures: application to cerebral aneurysms", IEEE TMI 28(8):1141-1155, 2009, doi 10.1109/TMI.2009.2021652. — [VMTK Mapping tutorial](http://www.vmtk.org/tutorials/MappingAndPatching.html); [PubMed 19447701](https://pubmed.ncbi.nlm.nih.gov/19447701/)
- Alternative CTA precedent: plane normal to centreline, polygon area, effective radius from A = πR² (every 0.5 mm) and ellipse fit where area is maximal in the bifurcation. — [Coronary atlas, EuroIntervention](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)

### Inferences
- The VMTK "one sphere" rule measures daughters at 1 MIS radius beyond the bifurcation origin; relative to the tube-intersection reference point, the second reference point is 1 MIS radius further. So VMTK distances are radius-scaled, not fixed mm. For coronary daughters (r ~ 1 to 2 mm) one sphere is ~1 to 2 mm, i.e. shorter than your 3 mm window.
- Your r_J junction sphere is conceptually the VMTK tube-intersection point on each daughter (the daughter exits the parent's tube). Adopting the VMTK convention would mean: start = where the daughter centerline leaves the parent MIS tube, measurement = 1 (or N) daughter MIS radii further.
- EDT at a centerline point equals the MIS radius on a voxel grid, which VMTK also uses for splitting; VMTK then uses surface plane-sections (area, min/max diameter) for the actual size numbers. That split, MIS for geometry and plane-section area for size, is a direct remedy for the ~0.135 mm EDT offset (half-voxel-ish bias at 0.5 mm spacing is plausible) and the junction ballooning. On a voxel mask the equivalent is marching-cubes surface then plane cut, or resampling the mask on an orthogonal plane and counting sub-voxel area.
- Equivalent diameter from area is robust to ellipticity; MIS (EDT) gives the minor radius, so on elliptical ostial sections EDT underestimates area-equivalent size while balloon regions inflate it. Report which one.

### Gaps
- Could not read Piccinelli 2009 full text (403) to confirm whether it defines explicit "two spheres" measurements; the "one sphere upstream" reference point and default NumberOfDistanceSpheres = 1 are confirmed only via VMTK docs/code.

## Q3. Cross-domain distance rules (retina, cerebral aneurysm, airway, carotid)

### Takeaway
Radius-scaled rules dominate outside coronaries: carotid uses CCA 3 radii proximal and ICA/ECA 1 sphere radius distal to the VMTK origin; automated retinal work measures daughters between about 1 and 2 vessel diameters from the branch centre and averages several profiles; airway CT averages cross-sections over the middle portion of each branch. Cerebral aneurysm work (Ingebrigtsen 2004) uses parent D1 and daughters D2/D3 with area ratio and daughter ratio.

### Cited Findings
- Retina, automated: "For each branch, the start point was at approximately one vessel diameter (15 pixels) away from the branch center. The end point was at approximately two vessel diameters away"; "Vessel width for branch 1 is calculated as the average of the three width profiles." Experts gave at least three profiles per branch. — [Xu et al., PLoS One 2012, PMC3507841](https://pmc.ncbi.nlm.nih.gov/articles/PMC3507841/)
- Retina, junction exponent x from d0^x = d1^x + d2^x (Murray x = 3); x is biased under measurement noise; optimality ratio Γ = ((d1^3 + d2^3)/(2 d0^3))^(1/3) equals 2^(-1/3) at Murray optimum irrespective of asymmetry and is more robust. Measurements via Sliding Linear Regression Filter, ~5 μm/pixel; the paper does not state the distance from the junction. — [Witt et al., Artery Research 2010, PMC2954284](https://pmc.ncbi.nlm.nih.gov/articles/PMC2954284/)
- Chapman, Witt, Hughes et al. 2002 linked abnormal retinal arteriolar bifurcation diameter relationships to peripheral vascular disease. — [Search result referencing PMC2954284](https://pmc.ncbi.nlm.nih.gov/articles/PMC2954284/)
- Cerebral aneurysm: Ingebrigtsen & Morgan, J Neurosurg 2004;101(1):108-113 measured parent D1, smaller daughter D2, larger daughter D3; DA ratio = D3/D2; OR for aneurysm 3.46 (1.02 to 11.74) for the angle parent-to-largest-branch and 48.06 (9.7 to 238.2) for the smallest branch (highest vs lowest tertile). (snippet only; abstract page blocked by captcha) — [PubMed 15255260](https://pubmed.ncbi.nlm.nih.gov/15255260)
- Carotid (Thomas et al., Stroke 2005, MRI, 25 young vs 25 older): ECA/CCA diameter ratio 0.81 ± 0.06 vs 0.75 ± 0.13; ICA/CCA 0.81 ± 0.06 vs 0.77 ± 0.12; bifurcation area ratio 1.32 ± 0.15 vs 1.19 ± 0.35; bifurcation angle 48.5 ± 6.3° vs 63.6 ± 15.4°. — [Europe PMC abstract / Stroke doi 10.1161/01.STR.0000185679.62634.0a](https://www.ahajournals.org/doi/10.1161/01.str.0000185679.62634.0a)
- Carotid (Bijari, Wasserman, Steinman): CCA reference section "three radii proximal to the bifurcation origin" (CCA3); ICA1/ECA1 "one sphere radius distal to the bifurcation origin"; Area Ratio = (A_ICA1 + A_ECA1)/A_CCA3; Flare = CCA_max (maximum bifurcation cross-sectional area)/A_CCA3; tortuosity measured from CCA3. Software AriX 1.1 (Orobix), built on VMTK. — [Bijari et al., PMC4321819](https://pmc.ncbi.nlm.nih.gov/articles/PMC4321819/)
- Airway CT: cross-sections perpendicular to the centreline, luminal areas "in the middle-third portion" automatically measured and averaged (snippet only, primary source not confirmed); VIDA Pulmonary Workstation used in never-smoker airway morphology study, which does not detail bifurcation avoidance. — [search snippet]; [PMC4335784](https://pmc.ncbi.nlm.nih.gov/articles/PMC4335784)

### Inferences
- Carotid Bijari/Thomas definitions are the cleanest transferable "before/at/after" triple: before = parent at 3 parent radii upstream of origin; after = daughters at 1 radius downstream; during = maximum section area in the bifurcation region (Flare). Healthy young carotid area ratio ~1.3 is a useful sanity comparator for coronary area ratio.
- Retinal 1 to 2 diameters and airway middle-third both express the same principle: skip roughly one diameter of junction influence, then average multiple sections.

### Gaps
- Stanton 1995 and Chapman 2002 retinal manual protocols (often described as measuring at a distance of a few vessel widths from the junction) could not be accessed; the "1.5 to 5 diameters" rule in the brief is not confirmed by any source I retrieved.
- Weibel-based airway branch diameter rules and exact carotid bulb (ICA max area) definitions from Thomas 2005 full text were not accessible.

## Q4. Distance rules: fixed mm vs radius multiples; where the daughter reaches its own diameter; nearby second branch

### Takeaway
Coronary clinical standards use fixed mm (3 mm SB ostium, 5 mm proximal/distal, reference within 10 mm, angle 5 to 10 mm depth). Engineering/VMTK and carotid work use radius multiples (1 sphere distal, 3 radii proximal). No retrieved source quantifies directly how far past the junction the daughter reaches its asymptotic diameter.

### Cited Findings
- Fixed-mm coronary rules: 5 mm segments beyond, 3 mm SB ostial (EBC) — [EBC](https://eurointervention.pcronline.com/article/quantitative-angiography-methods-for-bifurcation-lesions-a-consensus-statement-update-from-the-european-bifurcation-club); 5 mm proximal/distal to carina, reference within 10 mm — [Frontiers 2023](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2023.1292517/full); angles averaged over 5 to 10 mm depth "where variation is typically small" — [Atlas](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy).
- Radius-scaled rules: VMTK NumberOfDistanceSpheres default 1 — [vmtkbifurcationsections](https://github.com/vmtk/vmtk/blob/master/vmtkScripts/vmtkbifurcationsections.py); CCA3 / ICA1 / ECA1 — [Bijari](https://pmc.ncbi.nlm.nih.gov/articles/PMC4321819/); retina 1 to 2 diameters — [Xu 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3507841/).
- CT/IVUS rule for disease or a nearby branch: take reference at the "point least affected" within 10 mm — [Frontiers 2023](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2023.1292517/full).

### Inferences
- A defensible thesis rule: start the daughter window at the exit of the parent MIS tube (VMTK reference point 1 ≈ your r_J), skip at least one daughter radius (VMTK reference point 2), then take the median over a fixed mm window (3 mm, EBC ostial segment) or to the midpoint of the segment, truncated at the next branch's own junction sphere. Truncation plus "at least N samples" handles a nearby second branch; if the inter-branch segment is shorter than r_J + r_d + window, flag it rather than borrow from the next junction.
- Report sensitivity: fixed 3 mm vs 1 and 2 daughter radii vs 5 mm; with 0.5 mm isotropic voxels, a coronary daughter radius of ~1 mm means 1 radius ≈ 2 voxels, so radius-scaled windows are very short for small side branches and fixed mm may be more stable.
- Post-junction narrowing: the EBC practice of replacing interpolated references by fractal-law references inside the POC implies that raw diameters just past the carina are not representative; this supports skipping ≥ 1 radius.

### Gaps
- No quantitative source found on the length of the ostial transition zone in healthy coronaries (e.g. mm to reach 95% of distal diameter). Could be measured empirically in ImageCAS-X references.

## Q5. Characterising the "during" part

### Takeaway
Three established "at junction" descriptors: (1) Flare = maximum cross-section area in the bifurcation region / parent reference area (carotid, VMTK-based); (2) bifurcation area ratio = sum of daughter areas / parent area (carotid 1.32 in young adults; Ingebrigtsen in cerebral); (3) POC diameters (CAAS: equivalent diameter from area, MLD as maximum inscribed circle, elliptical split of the peanut-shaped section; atlas: ellipse fit where area is maximal). Plus the junction exponent / optimality ratio and fractal laws (Murray 3, Huo-Kassab 7/3, Finet 0.678).

### Cited Findings
- Flare and Area Ratio definitions — [Bijari, PMC4321819](https://pmc.ncbi.nlm.nih.gov/articles/PMC4321819/); area ratio values — [Thomas 2005](https://www.ahajournals.org/doi/10.1161/01.str.0000185679.62634.0a).
- POC measurement definitions — [CAAS 3D bifurcation, EuroIntervention](https://eurointervention.pcronline.com/article/a-novel-dedicated-3-dimensional-quantitative-coronary-analysis-methodology-for-bifurcation-lesions).
- Maximal-area ellipse fit at the coronary bifurcation — [Atlas](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy).
- POB = centre of largest circle touching all three contours — [EBC](https://eurointervention.pcronline.com/article/quantitative-angiography-methods-for-bifurcation-lesions-a-consensus-statement-update-from-the-european-bifurcation-club).
- Junction exponent, optimality ratio and noise bias — [Witt 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2954284/); coronary pooled exponent 2.39 — [PMC11380967](https://pmc.ncbi.nlm.nih.gov/articles/PMC11380967/).

### Inferences
- Your junction sphere radius r_J is itself the 3D analogue of the CAAS POB circle (largest inscribed sphere touching all three walls) and is a natural "during" size; r_J / r_parent is a flare-like index directly available from the EDT.
- Because the EDT balloons at junctions, a plane-section maximum area (Flare numerator) is also inflated by the junction geometry; this is intended in Flare, but should not leak into parent or daughter reference values.
- Prefer optimality ratio or Finet ratio over a fitted junction exponent for per-junction outcome modelling, given the documented noise bias of x.

### Gaps
- No coronary CT study found that reports Flare or area ratio as outcome predictors in healthy cohorts.

## Q6. Automated software and their definitions

### Takeaway
VMTK (open source) gives the most transparent, radius-scaled definitions; CAAS (Pie Medical) implements EBC POC for 2D/3D QCA; Vitrea (Canon/Vital) and QIvus (Medis) were used in CT/IVUS bifurcation comparisons with fixed-mm sections; AriX (Orobix) is VMTK-based for carotid geometry.

### Cited Findings
- VMTK scripts: vmtkcenterlines, vmtkbranchextractor, vmtkbranchclipper, vmtkbifurcationreferencesystems, vmtkbifurcationvectors, vmtkbifurcationsections, vmtkcenterlineoffsetattributes — [VMTK tutorials](http://www.vmtk.org/tutorials/GeometricAnalysis.html); [source](https://github.com/vmtk/vmtk/tree/master/vmtkScripts).
- CAAS 5 QCA-3D bifurcation: 3D reconstruction from two projections, POC definition, cross-sectional area/diameter, reference area, angle — [EuroIntervention](https://eurointervention.pcronline.com/article/a-novel-dedicated-3-dimensional-quantitative-coronary-analysis-methodology-for-bifurcation-lesions).
- Vital Vitrea Advanced 6.2 (CT), QIvus 3.0 Medis (IVUS) — [Frontiers 2023](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2023.1292517/full).
- AriX 1.1 (Orobix, VMTK-based) — [Bijari](https://pmc.ncbi.nlm.nih.gov/articles/PMC4321819/).
- VIDA Pulmonary Workstation (airways) — [PMC4335784](https://pmc.ncbi.nlm.nih.gov/articles/PMC4335784).

### Inferences
- For the thesis, reimplementing the VMTK definitions on the labelled centerline VTKs (MIS tube intersection, one-sphere offset, plane sections on a marching-cubes surface) gives citable, software-independent definitions; running VMTK itself on the ImageCAS-X surfaces is a direct validation path.

### Gaps
- QAngio CT (Medis) and Vesselucida bifurcation definitions were not found in public documentation within this search budget.
