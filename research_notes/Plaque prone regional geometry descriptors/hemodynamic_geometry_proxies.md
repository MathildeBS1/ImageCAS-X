# Hemodynamic geometry proxies: local coronary descriptors that stand in for WSS without CFD

Scope note for the report writer. This set of notes builds on the earlier tortuosity reports in `reports/` (they recommend kappa_a at a 5 mm chord with 1 mm sigma, and they already cover Kashyap 2022: kappa_a vs low TAWSS, R^2 up to 0.23 in 127 CAD-free patients; arc/chord not significant). That material is not repeated here. The research budget ran out before several primary papers could be read in full (Springer, APS and PMC fetches were blocked or rate limited), so a large share of claims below are tagged **abstract only** or **search snippet**. The tags mean:
- **[full text]**: I read the method and results sections of the paper myself.
- **[abstract only]**: taken from an abstract or publisher landing page.
- **[search snippet]**: taken from a search-engine summary of the page. It needs checking before it goes into the thesis.
- **[derivation]**: standard fluid mechanics or geometry that I worked out here. No empirical claim.

## 1. Bifurcation geometry: angles, planarity, diameter laws (Murray, Finet, Huo-Kassab)

### Takeaway
Only a few bifurcation descriptors are well defined on CCTA centerlines: angle B (DMV to SB), the inflow angle to a least-squares bifurcation plane, and the Finet ratio. They are well defined only when tangents or planes are fitted over 5 to 10 mm branch pieces, not taken at the branch point itself. Among the diameter laws, Finet's ratio (about 0.66 to 0.68) and a Huo-Kassab-type exponent (about 2.3 to 2.4) fit normal human coronaries better than Murray's 3. However, in the only whole-tree CFD comparison I could read in full (39 ASOCA trees), no bifurcation angle or Finet ratio separated stenosed from non-stenosed bifurcations. SB diameter and DMV torsion did (unadjusted p < 0.05).

### Cited Findings
- **Normal-population reference values [abstract/landing page, EuroIntervention].** Medrano-Gracia et al. built an atlas from 300 adults with zero calcium score and no stenosis (Auckland; mean age about 55; 64 % female). Angles were computed from 3D centerlines at depths of 5 to 10 mm from the bifurcation point, not at a single point, and a least-squares bifurcation plane was fitted at each depth. Angles are A (PMV to SB), B (DMV to SB), C (PMV to DMV), B' (using a straight projection of the proximal vessel) and the inflow angle (PMV entering the bifurcation plane). [Medrano-Gracia, A computational atlas of normal coronary artery anatomy](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)
- In that atlas, LM angle B was 89 +/- 21 deg with an intermediate artery and 75 +/- 23 deg without one (p < 0.001). The LM averaged about 80 deg, other bifurcations about 50 deg. Males had wider angles (85 vs 74 deg, p < 0.001). The LM inflow angle was 6 deg in males vs 12 deg in females (p = 0.07). Diameters fell by about 0.25 mm per 10 mm distal to bifurcations. [same source](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy) [landing page; numbers were extracted by a summariser and should be checked against the PDF](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy/pdf)
- In the same 300 CT scans, the Finet ratio D_PMV/(D_DMV + D_SB) was 0.6576 +/- 0.083, close to Finet's published 0.678. A power-law fit gave an exponent alpha = 2.4, closest to the Huo-Kassab 7/3. [Medrano-Gracia atlas](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)
- The Huo-Kassab law is D_PMV^(7/3) = D_DMV^(7/3) + D_SB^(7/3). It is reported to predict diameters across all epicardial size ranges, whereas Murray (exponent 3) and Finet fit only subsets. [search snippet, summarising the Kassab 2016 J Biomech review and a 2021 Med Eng Phys LM paper](https://www.sciencedirect.com/science/article/abs/pii/S0021929016301270); [Scaling laws and the LM bifurcation, Med Eng Phys 2021](https://www.sciencedirect.com/science/article/abs/pii/S1350453321001016). A contrary statement appears in the same search results: a bench-testing or LM paper found coronary bifurcations "obey the Finet diameter model and angle rule much more than Huo-Kassab and Murray". [search snippet](https://www.sciencedirect.com/science/article/abs/pii/S1350453321001016). **The two claims conflict. Neither was read in full.**
- **Whole-tree CFD test [full text, preprint].** Zhang, Gharleghi, Shen and Beier used 39 ASOCA left coronary trees (CTCA, 0.3 to 0.4 mm in-plane; 20 with DS = 0 %, 12 with 0 < DS < 70 %, 7 with DS >= 70 %). They defined each bifurcation as 10 mm of centerline proximal and distal to the branch point. The inflow angle is the angle at which the PMV enters "a least-square plane fitted to all the centreline points of the DMV and SB". Angle B is between DMV and SB. FR = D_PMV/(D_DMV + D_SB). [Zhang et al. 2023, arXiv 2312.00257](https://arxiv.org/abs/2312.00257)
- In that study no bifurcation angle or FR differed between stenosed and non-stenosed bifurcations (p > 0.057). SB diameter (p = 0.041) and DMV torsion (p = 0.024) did differ. Whole-tree average curvature did too: 1.230 +/- 0.090 vs 1.321 +/- 0.131 (units printed as m^-1, which is physically implausible and probably a unit typo), p = 0.024, AUC 0.711. [Zhang et al. 2023](https://arxiv.org/abs/2312.00257)
- **Hemodynamic direction of the angle effect [search snippet from a JAHA review].** Shallower bifurcation angles are associated with higher WSS. Wider angles concentrate low WSS and OSI on the outer (lateral) walls. Chiastra et al. report counter-clockwise helical flow in the bifurcation region and SB ostia, with larger angles giving more helicity. [Advances in the Computational Assessment of Disturbed Coronary Flow and WSS, JAHA 2024/25](https://www.ahajournals.org/doi/10.1161/JAHA.124.037129)
- An LM bifurcation angle measured on CCTA has been associated with CFD-derived hemodynamic change in stenosis. [abstract only](https://pmc.ncbi.nlm.nih.gov/articles/PMC5682403/) (population not extracted)
- A CT phantom study of bifurcation-angle measurement exists. [abstract only, not read](https://www.sciencedirect.com/science/article/abs/pii/S112017971730460X)

### Inferences
- [derivation] **Rigorous angle definition from a centerline.** Take branch unit vectors as chords, not point tangents: t_PMV = (x(s_b) - x(s_b - d))/|.|, and likewise for DMV and SB at +d, with d = 5 mm (the atlas range is 5 to 10 mm). Then B = arccos(t_DMV . t_SB), and A and C follow the same pattern. The bifurcation-plane normal is n = t_DMV x t_SB / |.|, or the least-squares plane through all DMV and SB points within d. Inflow angle = arcsin(|t_PMV . n|). Out-of-plane (non-planarity) = the same quantity; in-plane angle = the angle between the projections onto the plane. All are rotation and translation invariant and dimensionless, so they meet the supervisor's "normalise distances" request without further work.
- [derivation] **Noise.** A chord over length d with endpoint error sigma has angular error about sqrt(2) sigma/d rad. With sigma about 0.25 mm (half a voxel at 0.5 mm) and d = 5 mm, that is about 4 deg. With d = 10 mm it is about 2 deg. This is well below the 21 to 23 deg between-subject SD of LM angle B, so angle B should be robust (a first-derivative quantity with a long baseline). The inflow angle (6 to 12 deg means) sits much closer to the noise floor and is likely fragile. The earlier tortuosity report found raw turning angles on 0.5 mm ImageCAS-X centerlines to be about 3x the real curvature, which is consistent with this: short baselines are what break angles.
- [derivation] **Diameter-law deviations.** A per-bifurcation residual is epsilon_k = (D_DMV^k + D_SB^k)^(1/k)/D_PMV - 1 for k in {3, 7/3}, or the fitted exponent alpha solving D_PMV^alpha = D_DMV^alpha + D_SB^alpha. Diameters must be averaged over 1 to 2 diameters away from the carina, as the atlas's 5 to 10 mm windows suggest, because radius near the flow divider is ill defined. alpha has no closed-form solution and blows up when D_SB is much smaller than D_DMV (the SB term vanishes), so the Finet ratio or epsilon_{7/3} is the safer node feature.
- The negative bifurcation result in 39 ASOCA trees is underpowered (54 bifurcations, 12 stenosed), not evidence of absence.
- ImageCAS-X centerlines carry segment labels but no radius. Diameters would have to come from the surface mesh (distance from centerline to surface) or from a distance transform of the segmentation. CGPS (binary lumen only) forces the distance-transform route, so both cohorts should use it for comparability.

### Gaps
- Could not read Finet 2008, Huo and Kassab 2012, or the Kassab 2016 scaling review in full. The exact coronary support for 7/3 vs Finet is unresolved and the sources above conflict.
- No source found that validates angle B, inflow angle or a Murray/HK residual against CFD WSS at patient level with an effect size. Only the direction is known ("wider angle, more lateral-wall low WSS"), from a review snippet.
- No reproducibility (inter-scan ICC) data for coronary bifurcation angles on CCTA were found. The phantom study was not read.
- Carina and flow-divider geometry (carina radius of curvature, polygon-of-confluence shape): no CCTA-feasible source found. At 0.5 mm voxels the carina is probably unresolvable on a binary lumen.

## 2. Curvature-flow theory: Dean, Germano, kappa*r, helicity from geometry, Womersley

### Takeaway
The dimensionless groups follow directly from a centerline plus radius: delta = kappa*r (curvature ratio), Dean De = Re*sqrt(kappa*r), Germano-type torsion ratio tau*r, and Womersley alpha = r*sqrt(omega/nu). Their physical meaning is textbook. The coronary-specific empirical evidence that they predict low or oscillatory WSS is weak and small-sample. In 39 human left trees, curvature and torsion correlated with helicity and low-TAESS area in single segments, but none of those correlations survived multiplicity correction. Diameter did survive. Helical flow intensity (h2) tracks higher TAESS, and helical flow is generated mainly by torsion and curvature.

### Cited Findings
- **Helicity vs geometry in human trees [full text, preprint].** Shen, Zhang, Keramati, Almeida and Beier studied the same 39 ASOCA left trees (20 non-stenosed, 19 stenosed). Absolute helicity intensity h2 correlated with higher TAESS in all segments (p < 0.05). In stenosed trees, high h2 reduced low-TAESS area (< 0.5 Pa, p = 0.0001) and increased adversely high TAESS (> 4.71 Pa, p < 0.05). Curvature kappa_a and torsion tau_a were computed with VMTK as length-averaged integrals. [Shen et al. 2025, arXiv 2502.06161](https://arxiv.org/abs/2502.06161)
- In the same paper's appendix, segment-level correlations in healthy trees include: Marginal diameter vs average TAESS r = -0.85 (p = 0.0001, adjusted 0.0046); Diagonal diameter vs h1 r = -0.75 (adjusted 0.036); Marginal curvature vs low-TAESS% r = -0.60 (p = 0.017, adjusted 0.69); Diagonal curvature vs h1 r = 0.57 (adjusted 0.92); LAD torsion vs RRT% r = -0.46 (adjusted 1.0); Diagonal torsion vs h1 r = 0.65 (adjusted 0.50). **Only the diameter correlations survived correction.** [Shen et al. 2025](https://arxiv.org/abs/2502.06161)
- The sign of the curvature-low-TAESS correlation in the Marginal segment was negative: more curvature went with less low-TAESS area. That is the opposite of the naive "bends are atherogenic" reading, and consistent with curvature driving helical flow that raises WSS. [Shen et al. 2025](https://arxiv.org/abs/2502.06161)
- Earlier coronary work is cited in that paper as linking severe curvature and torsion to higher helical flow intensity in idealised and patient-specific coronaries, **with sample size 3**. In swine, torsion correlated positively with helical flow intensity and high h2 with higher ESS. [Shen et al. 2025 introduction, full text](https://arxiv.org/abs/2502.06161)
- De Nisco, Morbiducci et al. (Ann Biomed Eng 2019, swine coronaries) found counter-rotating bi-helical flow attributed to vascular torsion, and high helicity intensity associated with low wall-thickness growth, i.e. atheroprotective. [abstract only, via search snippet](https://link.springer.com/article/10.1007/s10439-018-02169-x); [De Nisco 2020 Atherosclerosis, abstract only](https://www.atherosclerosis-journal.com/article/S0021-9150(20)30054-X/abstract)
- Vorobtsova, Chiastra et al. (Ann Biomed Eng 2016; idealised plus patient-specific coronaries) found that perfusion pressure drops with tortuosity, that more tortuous patient vessels had higher WSS, and that curvature and torsion induce secondary flow. [abstract only](https://link.springer.com/article/10.1007/s10439-015-1492-3)
- In a helical-tube model with time-varying geometry, WSS varied by up to 22 % when curvature changed, 3 % when torsion changed, and 26 % when both changed, so curvature dominates torsion. [J Biomech Eng 2012, search snippet only](https://asmedigitalcollection.asme.org/biomechanical/article-abstract/134/7/071005/464806/Investigation-of-the-Effects-of-Dynamic-Change-in)
- Dean-type secondary flow, which drives transverse WSS, is "particularly sensitive" to changes in local curvature produced by coronary bending, and entrance-flow development alters vortex formation in curved-artery models. [Physics of Fluids 2021, arXiv 2108.02377, search snippet](https://arxiv.org/pdf/2108.02377); [Frontiers 2022, RCA motion and pulsatility, search snippet](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2022.962687/full)
- Zhang et al. found curvature negatively correlated with diameter across segments (r = -0.474, p = 0.002): smaller arteries are more curved. [Zhang et al. 2023, full text](https://arxiv.org/abs/2312.00257)

### Inferences
- [derivation] **Definitions per node i** (smoothed centerline, radius r_i):
  - curvature ratio delta_i = kappa_i * r_i (dimensionless; Dean's small parameter)
  - Dean number De_i = Re_i * sqrt(delta_i), with Re_i = 2 r_i U_i / nu = 2 Q_i/(pi r_i nu)
  - torsion ratio (Germano's parameter) lambda_i = tau_i * r_i. The Germano number is usually Gn = tau * r / sqrt(Re) or lambda relative to delta. The exact convention varies and was not verified from a primary source.
  - Womersley alpha_i = r_i * sqrt(omega/nu). With a heart rate of about 1 Hz, nu of about 3.5e-6 m^2/s, and r from 1 to 2 mm, alpha is about 1.3 to 2.7. That is low, so flow is quasi-steady Poiseuille-like and Womersley corrections are small. This is a standard estimate; no coronary source was fetched.
- [derivation] **No new information beyond kappa and r without a flow model.** delta, lambda and alpha are products of quantities the node already has (kappa, tau, r). De needs Q_i, which on a tree without CFD must come from an allometric law (section 4), so De_i ends up as a fixed function of (kappa_i, r_i, Q-law). For a GNN these are redundant with the raw inputs unless the model is very small. Their value is interpretability and scale invariance: delta is dimensionless, so it satisfies the supervisor's normalisation request, whereas kappa in mm^-1 does not. Recommendation: replace raw kappa_a by delta = kappa_a * r as the per-node bend feature, and keep De as a secondary interpretable feature.
- [derivation] **Noise.** delta inherits curvature's second-derivative noise (the earlier report's spurious term of about 3 sigma/l^2) times r's first-order noise. At a 5 mm chord, sigma = 0.25 mm and r = 1.5 mm: spurious kappa is about 0.03 mm^-1, so spurious delta is about 0.045, against true coronary delta of roughly 0.05 to 0.2. That is borderline, so delta is usable only as a segment average, not as a pointwise value. Torsion (third derivative) is worse, and lambda should be dropped at node level. This matches the earlier reports' decision to drop torsion.
- The human evidence (39 trees, uncorrected r of about 0.5 to 0.65 for curvature and torsion, none surviving correction; diameter r = -0.85 surviving) suggests **radius is the strongest single geometric WSS proxy**, and curvature and torsion add weaker, sign-ambiguous information, through helicity.

### Gaps
- No primary source fetched for the Germano number definition in coronary use, or for a coronary study that uses Dean number as a predictor of WSS or plaque location. Search returned none.
- No coronary study found that computes "helical flow indices from geometry alone" (e.g. predicting h2 from tau_a). Only correlations with CFD-derived h1 to h4.
- The Vorobtsova 2016 and De Nisco 2019 full texts were not accessible (403 / login), so their effect sizes are missing.

## 3. Lumen shape: taper, area gradient, eccentricity, radius function, curvature-radius coupling

### Takeaway
Radius-derived shape descriptors (mean diameter, local taper dr/ds, area gradient) have the most consistent link to WSS, in both the 39-tree ASOCA data and older carotid and coronary design studies cited in the earlier reports. Eccentricity and ellipticity are measurable from a surface mesh but have no coronary validation I could find. Taper is a first derivative of a noisy radius and needs long windows.

### Cited Findings
- In 39 human left trees, the diameter correlations were the only geometry-hemodynamics associations to survive multiple-comparison correction: Marginal diameter vs average TAESS r = -0.85, Diagonal diameter vs h1 r = -0.75. [Shen et al. 2025, full text](https://arxiv.org/abs/2502.06161)
- Zhang et al. used mean maximal-inscribed-sphere diameter (MISD from VMTK) as the radius function, and found SB diameter differed between stenosed and non-stenosed bifurcations (p = 0.041). [Zhang et al. 2023, full text](https://arxiv.org/abs/2312.00257)
- The normal-atlas taper is about 0.25 mm diameter per 10 mm distal to bifurcations (300 CAD-free adults). [Medrano-Gracia atlas, landing page](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)
- In aortic flow, taper is reported to stabilise and delay the attenuation of torsion-induced helical flow. [search snippet summarising Morbiducci/De Nisco work](https://link.springer.com/article/10.1007/s10439-018-02169-x)
- The earlier reports (not repeated here) cite three designs in which lumen diameter or diameter ratio outweighed curvature for WSS: Johnston 2007 and Garcha 2025, both abstract only. See `reports/Alternative tortuosity merges for coronaries.md` line 74.

### Inferences
- [derivation] **Radius function and derived features per node:** r(s) from the distance transform of the binary lumen, sampled at centerline nodes and smoothed over a window w of at least 2r.
  - taper T = -dr/ds (dimensionless)
  - normalised area gradient G = (1/A) dA/ds = 2 (dr/ds)/r (units 1/mm; multiply by r to get a dimensionless value)
  - local expansion ratio E_i = r_i / median(r over a window of +/- 5 mm) - 1, which flags focal ectasia or narrowing (a proxy for post-stenotic low WSS or ectatic recirculation)
  - eccentricity from the surface mesh cross-section: e = 1 - r_min/r_max, from principal axes of the cross-section contour. This is possible for ImageCAS-X (surface meshes exist) and for CGPS from marching cubes on the binary lumen.
- [derivation] **Noise.** Distance-transform radius error is about +/- half a voxel (0.25 mm at 0.5 mm). Relative error at r = 1.5 mm is about 17 %. Taper over a 10 mm baseline then has error of about 0.035 (dimensionless), against a true normal taper of about 0.0125 (0.25 mm in diameter per 10 mm is 0.0125 mm/mm in radius). **Pointwise taper is below the noise floor at a 10 mm baseline.** Only segment-level taper (a linear fit of r(s) over a whole branch) is safe. Eccentricity from a 0.5 mm mask on a 3 mm lumen (6 voxels across) is dominated by voxelisation and is likely not interpretable at node level.
- "Curvature-radius coupling" is effectively delta = kappa * r (section 2). The negative kappa-diameter correlation (r = -0.47) means raw kappa partly re-encodes size. A dimensionless delta or kappa normalised within vessel removes that confound. This connects to Kit's concern that embeddings may separate on size.

### Gaps
- No coronary study found that validates cross-sectional eccentricity or ellipticity against CFD WSS.
- "Tortuosity of curvature" (variation of kappa along s, e.g. a TV-norm of kappa) had no coronary source.
- No test-retest reproducibility data for local coronary radius or taper from CCTA segmentation were found.

## 4. Reduced-order and surrogate WSS models

### Takeaway
A Poiseuille WSS estimate with an allometric flow law is a closed-form per-node proxy. With Murray's exponent it predicts uniform WSS, so any signal lives in deviation from the law. With the empirical coronary law Q = 1.43 d^2.55 it gives tau proportional to d^-0.45. Used as a per-node feature it is a monotone function of radius, unless flows are propagated down the tree through flow splits. Mesh and graph neural surrogates reach NMAE of 0.4 to 2.5 % on synthetic coronaries, but patient-level validation is thin and not needed for descriptor work.

### Cited Findings
- **Flow and diameter laws used in coronary CFD [full text].** Shen et al. prescribed the LM inflow as Q = 1.43 d^2.55 (d = mean LM diameter) and split flow at each bifurcation as Q_sb/Q_mb = (d_sb/d_mb)^2.27, "due to their strong fit to in vivo data". These are the van der Giessen-type scaling laws. [Shen et al. 2025, full text](https://arxiv.org/abs/2502.06161)
- With diameter-scaled boundary conditions in atherosclerotic human coronary bifurcations, normalised WSS maps were equivalent to those from measured flows, but absolute WSS needs caution. [Schrauwen et al., Am J Physiol Heart Circ Physiol 2016, search snippet; full text 403](https://journals.physiology.org/doi/full/10.1152/ajpheart.00896.2015); [PubMed](https://pubmed.ncbi.nlm.nih.gov/26945083/)
- Poiseuille WSS neglects lateral velocity components and wall shape. In MRI it gave about 10 % higher mean WSS than a paraboloid fit, and on synthetic cylinders it matched spectral methods. [search snippet](https://pmc.ncbi.nlm.nih.gov/articles/PMC13338701/)
- **ML surrogates.**
  - Suk, de Haan, Lippe, Brune and Wolterink: SE(3)-equivariant mesh neural network on triangular surface meshes of a large synthetic coronary dataset. Transient vector WSS, conditioned on inflow; 7.6 % approximation error, NMAE 0.4 %; up to two orders of magnitude faster than CFD. [arXiv 2212.05023, abstract only](https://arxiv.org/abs/2212.05023)
  - Mesh CNN on synthetic coronaries with and without bifurcation: NMAE <= 1.6 %, 90.5 % median approximation accuracy, under 5 s per mesh. [arXiv 2109.04797, search snippet](https://arxiv.org/abs/2109.04797)
  - Physics-informed GNN on stenotic coronaries: MAE 1.05 Pa, RMSE 5.63 Pa, R = 0.94 vs CFD, better than U-Net and MLP baselines. [Sci Rep 2026, search snippet](https://www.nature.com/articles/s41598-026-47410-z)
  - Earlier CNN on idealised coronaries: NMAE 2.5 %. [PubMed 33039809, search snippet](https://pubmed.ncbi.nlm.nih.gov/33039809/)

### Inferences
- [derivation] **Poiseuille proxy.** tau_w = 4 mu Q/(pi r^3). With Q = c r^k this gives tau_w proportional to r^(k-3).
  - Murray (k = 3): tau_w is constant. Murray's law is exactly the statement of uniform WSS, so it predicts no low-WSS sites at all.
  - HK / van der Giessen (k of about 2.33 to 2.55): tau_w proportional to r^(-0.45 to -0.67), so smaller vessels see higher WSS.
  - A per-node WSS proxy from the node's own radius is therefore a monotone transform of r. **It adds nothing a model cannot learn from r itself.**
- [derivation] **A tree-aware proxy that does add information.** Propagate Q from the root down the graph: Q_root = 1.43 d_root^2.55, then split at each bifurcation by (d_sb/d_mb)^2.27, normalising so children sum to the parent. Then compute tau_hat_i = 4 mu Q_i/(pi r_i^3) with the node's own r_i. tau_hat_i is low where the lumen is locally wider than its upstream-inherited flow warrants (ectasia, a post-stenotic segment, or a branch that is oversized relative to its parent), and high in narrowings. Normalising by the tree-root value (tau_hat_i/tau_hat_root) cancels mu and c, which gives a dimensionless, interpretable per-node feature that satisfies the supervisor's constraints.
- [derivation] **Noise.** dtau/tau = -3 dr/r. A 17 % radius error (0.25 mm at r = 1.5 mm) becomes about 50 % error in tau_hat. It must be computed on radius smoothed over at least 2 to 5 mm and reported as a segment average, and its reliability should be gated like kappa_a.
- ML WSS surrogates trained on synthetic coronaries are a CFD replacement, not an interpretable descriptor. For this thesis they could serve at most as a validation target, e.g. checking that tau_hat and delta correlate with surrogate WSS on ImageCAS-X. No pretrained public surrogate was confirmed to generalise to patient CCTA meshes.

### Gaps
- No study found that directly validates the tree-propagated Poiseuille tau_hat against CFD TAWSS in patient coronaries. That would be a natural small thesis experiment.
- Could not confirm the primary citation for Q = 1.43 d^2.55 and the 2.27 split exponent (van der Giessen 2011, J Biomech). The Shen et al. full text cites them only as their references [35].
- 1D (reduced-order network) coronary models for FFR exist, but I found no source reporting WSS accuracy from 1D models vs 3D CFD within budget.

## 5. Myocardial bridging and the LM: geometric detection from CCTA centerlines

### Takeaway
Myocardial bridging (MB) is defined by the artery's depth within myocardium and by the length of the tunnelled segment. Both need a myocardium segmentation, not just a coronary centerline. Systolic compression needs multiphase data. None of this is available in ImageCAS-X or CGPS as delivered, so MB is not detectable from the thesis data with established criteria. The LM is best handled through the bifurcation descriptors in section 1.

### Cited Findings
- In a combined CCTA and ICA study, MB depth and length were measured on CCTA and systolic compression on ICA. Compression correlated with depth but not with length. [Iran J Radiol, PMC5116748, abstract only](https://pmc.ncbi.nlm.nih.gov/articles/PMC5116748/)
- Depth > 2.0 mm and length > 25 mm are cited as high-risk anatomical features. Depth classes are superficial (> 1 to 2 mm), deep (>= 2 mm) and very deep (>= 5 mm). [search snippet, from the JACC state-of-the-art review and the CCTA/CTP paper](https://www.sciencedirect.com/science/article/pii/S0735109721071734); [PMC12470479](https://pmc.ncbi.nlm.nih.gov/articles/PMC12470479/)
- LM anatomy: in the 300-adult atlas, LM length was 10.5 +/- 5.3 mm and LM diameter about 3.5 +/- 0.8 mm, and the LM angle B depended strongly on whether an intermediate (ramus) branch was present (89 vs 75 deg). [Medrano-Gracia atlas, landing page](https://eurointervention.pcronline.com/article/a-computational-atlas-of-normal-coronary-artery-anatomy)

### Inferences
- A centerline-only MB proxy is conceivable: a mid-LAD segment with an abrupt, straightened course and a local radius dip, or a distance from the LAD centerline to the epicardial surface. However, no source validates it, and without a heart or myocardium mask it cannot measure depth. It should be listed as out of scope unless a whole-heart segmentation (e.g. TotalSegmentator-style) is added to the pipeline.
- The LM is short (about 10 mm) and trifurcates in a subset of patients. Stratify LM angle B by the presence of a ramus. Otherwise the ramus alone creates a 14 deg shift that looks like a phenotype.

### Gaps
- No paper found on automated MB detection from CCTA centerlines alone.
- No LM-specific WSS proxy beyond bifurcation angle and diameters was found within budget.

## 6. Cross-cutting: invariances, noise order, sample size

### Takeaway
Order the candidates by derivative order and baseline. Zeroth order: r, Finet or HK residual, tree-propagated tau_hat. First order over at least 5 mm: angle B, segment taper. Second order: kappa*r. Third order: torsion. Reliability falls down this list. The only human geometry-to-WSS correlation that survived correction was diameter.

### Cited Findings
- Human whole-tree evidence is limited to 39 ASOCA trees (Zhang 2023; Shen 2025, full text) and 127 CAD-free CCTA patients (Kashyap 2022, via the earlier report). Every other coronary geometry-hemodynamics study cited in Shen et al. had n = 3 or used swine. [Shen et al. 2025](https://arxiv.org/abs/2502.06161)

### Inferences
- Suggested small interpretable set per region of interest. This is my synthesis, not taken from any source.
  - **Bifurcation node:** angle B (5 mm chords), Finet ratio or HK residual epsilon_{7/3}, and the SB/DMV diameter ratio.
  - **Non-bifurcating segment node:** delta = kappa_a * r at a 5 mm chord (the dimensionless version of the earlier recommendation), and the normalised tree-propagated tau_hat.
  - **Segment level only:** linear taper.
  - Drop torsion, eccentricity and pointwise taper at node level.
- [derivation] **Invariances.** All of the above are invariant to rigid motion. Angles, delta, Finet/HK residuals and normalised tau_hat are also scale invariant. Raw r and kappa are not.
- [derivation] **Sample size.** To detect r = 0.3 at alpha = 0.05 with 80 % power needs about 85 independent units. The ASOCA studies (39 trees) could only detect r of about 0.45 or more. ImageCAS-X's 800 scans are ample for reliability and distribution work. Patient, not node, is the independent unit.

### Gaps
- No inter-scan reproducibility data for any of these local descriptors on coronary CTA were found. The CGPS serial scans (about 10 years apart) confound change with reproducibility, so a same-session reliability check (e.g. two segmentations or two reconstructions) would have to be designed.
