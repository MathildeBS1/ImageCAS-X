# mateos2024tortuosity3d: 3D Tortuosity computation as a shape descriptor (brain structures)

**Citation:** Mateos, Bribiesca, Guzmán-Arenas, Aguilar, Marquez-Flores. *BMC Medical Imaging*
2024;24(1):130. doi:10.1186/s12880-024-01312-6. PMID 38834987. PMCID PMC11149256.
**Read:** 2026-09-22. Full text including Tables 1 to 4 and all equations (1) to (10). Figures read
from captions only, not as images. No supplement exists.
**Source:** Europe PMC full-text XML, https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11149256/fullTextXML (CC BY).
**Verdict:** A surface-folding descriptor for voxelized solids, not a curve or vessel measure and
not an extension of Grisan 2008. It is of no use for coronary centerlines, and its one clinical
table has duplicated rows.

## What they did

**The measure.** Extends Bribiesca 2013's 2D Slope Chain Code (SCC) tortuosity to voxel objects.
In 2D, a curve is approximated by equal-length straight segments; each chain element a_n is the
normalised slope change between neighbouring segments, in (−1, 1); τ = Σ|a_n| (eq. 5). A simple
convex closed curve gives τ = 2.

The 3D version (eqs. 6 to 8) does **not** work on 3D curves. It:
1. takes a binary voxel object,
2. traces the 2D boundary contour in **every axis-aligned slice**, in X, Y and Z separately,
3. downsamples each contour by a factor of 10 (a fixed "DSF") to suppress stair-stepping,
4. fits digital straight segments (Kovalevsky's DSS algorithm) to get the chain,
5. sets τ_3D = Σ over the three directions of (sum of |slope changes| over all slices) / (number of
   slices in that direction).

A convex closed surface should then give τ_3D = 6 (2 per direction).

**Validation.** Voxelized spheres only: radius 10 to 80 voxels, "generated at different angles"
0 to 360°. Absolute error |τ_3D − 6| shown as a heat map (Fig. 4). No curves, no sinusoids, no
tortuous synthetic objects, no test that τ_3D increases with folding amplitude or frequency.

**Application 1.** One brain's pial surface smoothed by morphological closing with spheres of
radius 2, 4, 6, 8. τ_3D falls as smoothing grows. The last two are not significantly different.

**Application 2.** MIRIAD T1w MRI, 69 subjects. 9 removed after visual inspection of the images
and brain extractions, leaving 60: 37 AD and 23 controls. τ_3D per lobe (frontal, occipital,
parietal, temporal). Wilcoxon test AD vs control, then a linear regression per lobe with age and
sex as covariates. The central-sulcus result is from their earlier conference paper (Mateos 2020,
NSS/MIC), restated here.

## What they found

- **Spheres:** error "± 1" for r ∈ [10, 70] voxels. Error grows for larger spheres because the
  fixed downsampling factor stops removing stair-stepping. They state τ_3D "is extremely
  sensitive to the definition of chain elements".
- **Lobes, Wilcoxon (Table 2), 37 AD vs 23 control:** p = 0.0286 frontal, 0.031 parietal,
  0.002 occipital, 0.003 temporal. **Controls higher** in all four.
- **Lobes, adjusted for age and sex (Table 3):** p = 0.0171 frontal, 0.0013 parietal,
  0.0056 temporal. **Occipital not significant (p = 0.0648).** Effect sizes and coefficients
  not reported, only p-values.
- **Central sulcus (Table 4, from the 2020 paper):** left p = 0.021 (z = 2.32), right
  p = 0.21. Here **AD higher**, the opposite direction to the lobes.

## What the abstract does not tell you

- **It is not a vessel or curve measure.** "3D tortuosity" here means how folded a solid's
  surface is, averaged over axis-aligned slice contours. The Discussion says so outright: other
  3D methods "focus on capturing changes in 3D trajectories, whereas our approach is
  specifically designed to measure the 3D morphological variations of volumetric objects".
- **Grisan 2008 is cited once** ([15]) in a list of 2D methods. Nothing from it is used.
- **Duplicated rows in Table 1 (my check, not the authors').** 9 of 60 subjects share identical
  four-lobe values with another subject: IDs 27 (AD), 28 (Control), 29 (Control) all read
  63.4 / 35.4 / 60.4 / 36.4; 39 (Control) = 40 (AD); 43 (AD) = 44 (AD); 55 (Control) = 56 (AD).
  Four matching lobe values to one decimal place by chance is implausible. Three of the four
  groups mix AD and controls, so the group tests in Tables 2 and 3 use corrupted input. The
  paper does not mention this.
- **Opposite directions.** The abstract gives no direction. The lobes read higher in controls
  while the central sulcus read higher in AD. The paper does not reconcile the two.
- **The abstract's "p < 0.05 for ... the four brain lobes" is the unadjusted result.** After
  adjusting for age and sex, occipital is p = 0.0648.
- **No multiple-comparison correction** across 4 lobes plus 2 sulci.
- **Rotation invariance was not actually tested.** The only rotation test uses spheres, which
  look the same from every angle. Slicing along fixed X, Y, Z axes means an elongated or folded
  object can give different τ_3D after rotation. Scale invariance holds only "to some extent" for
  one downsampling factor.
- **Limitations section:** none as such. The Conclusions note only that clinical use is hard
  because brain structures are hard to access.

## What it licenses

- Objective 7, related work: "Mateos et al. (2024) extend slope-chain-code tortuosity to
  voxelized solids by summing slice-contour slope changes, a measure of surface folding rather
  than of a centerline's path."
- Objective 7, gap statement (with the citation search of 2026-09-22): the one 3D descendant of a
  2D tortuosity measure that cites Grisan 2008 does not carry the turn-based tortuosity density
  over to 3D curves. This is weak support only: it shows that *this* paper does not do it, not
  that no paper does.

## What it does NOT license

- Any claim about vessel or coronary tortuosity, or any 3D centerline method.
- τ_3D as an AD biomarker: the table has duplicated rows, directions conflict between structures,
  n = 60 from one database, no correction for multiple tests.
- "Rotation- and scale-invariant 3D tortuosity": not shown beyond spheres at one downsampling
  factor.
- Their claim to be "the first" to measure tortuosity of voxelized objects. It rests on their own
  reading of the literature, and ref [26] (Bribiesca 2021) already covers voxel surfaces.

## Open questions

- Is the Table 1 duplication a copy-paste error in the published table only, or in the data
  behind Tables 2 and 3? Unanswerable without the authors' data. It does not matter for this
  thesis unless the paper is cited for its AD result, which it should not be.
- Objective 7 still needs a 3D analogue of Grisan's turn splitting. The candidate is Bullitt
  2003's inflection definition (a flip in the normal vector's direction), not this paper.
