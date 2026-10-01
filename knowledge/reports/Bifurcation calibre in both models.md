# Give the network an explicit junction token, not a learned one, and skip FPCA at 3 mm

**The bifurcation calibre descriptors already locked (LM Finet ratio, daughter ratio, Γ_HK
deviation, parent-to-daughter ratios, angle, plus the ramus flag and LM length) should enter both
arms as one small, explicit, identical vector: extra terms in the regression, late-fused after the
network's pooled sequence embedding, on top of the masked raw radius profile the network already
reads on each limb.** No literature found in this pass, coronary, cerebral or retinal, trains a
*learned* junction token the way Bjørn's tokenised-tree proposal implies; the closest real
precedent, a 2025 Circle-of-Willis centerline pipeline, computes bifurcation features by exactly
the same hand-built formulas this thesis already locked (Finet, Huo-Kassab optimality, radius and
area ratios), which is independent support for the descriptor *content* but not for a learned
*architecture*. That points the default toward the explicit token, with a Perceiver-style learned
alternative as a later, optional ablation rather than the primary design, consistent with the
supervisor who wants representation learning explored and the one who wants it deferred both
getting a defensible first step. Giving the network the scalar token in addition to the raw masked
profile is not an information leak: it is the same "network sees every point, regression sees its
summary" asymmetry the whole-vessel design already accepts, repeated at junction scale, provided
the scalar token is byte-for-byte the same numbers the regression sees. The one place this report
diverges from the general profile-versus-scalar ladder already built elsewhere in this project is
functional regression: a 3 mm window at 0.5 mm spacing holds roughly six to seven points, which is
short enough that FPCA is reasoned, not measured, to support at most one or two real modes of
variation, so the information-matched rung at the junction scale should be a short fixed
summary-stat set, not FPCA, pending a one-script empirical check that has not yet been run.

## No coronary GNN paper gives a bifurcation its own node type

Two coronary-artery graph-labeling papers were read in full text for this report. Neither treats a
bifurcation as a distinct node type with its own feature schema. One makes every centerline point a
node and classifies whole segments using location, orientation and mean/SD radius features applied
identically regardless of whether a point sits at a branch ([PMC11095121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/)).
The other makes segments the nodes outright, so a bifurcation exists only implicitly as a segment
boundary, and uses no radius feature at all, only positional and directional geometry re-expressed
on a spherical manifold ([arXiv 2212.00386](https://arxiv.org/html/2212.00386v1)). A third paper,
AGMN, could not be read in full text this session and is left as a genuine gap rather than guessed
at ([arXiv 2301.04733](https://arxiv.org/pdf/2301.04733)). **The coronary-labeling literature
answers a different question (which named vessel is this) and supplies no template for a junction-
specific feature bundle**, because its own task never needed one. Full detail in
[junction_tokenization_literature.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Bifurcation%20calibre%20in%20both%20models/junction_tokenization_literature.md)
Q1.

## One real precedent exists, and it validates the descriptor list, not an architecture

A 2025 Circle-of-Willis centerline-graph pipeline, already cited elsewhere in this project's report
chain for its segment-level radius reliability figures, does compute a distinct bifurcation-level
feature bundle, separately from segment features: three bifurcation angles, individual parent-to-
child radius ratios, a radius sum ratio, an area sum ratio and a bifurcation exponent for major
bifurcations. Its methods text names the exact same formulas this thesis has already locked, "the
empirical Finet formula for vascular bifurcations" (r_p = 0.678·(r_c1 + r_c2)) and the Huo-Kassab
minimum-energy relation (r_p^(7/3) = r_c1^(7/3) + r_c2^(7/3)) ([arXiv 2510.13720](https://arxiv.org/html/2510.13720v1)).
**That every scalar in this thesis's locked bifurcation descriptor set has a direct 2025 counterpart
on a different vessel bed, arrived at independently, is real convergent support for the descriptor
content.** It is not evidence for a learned junction embedding: the bundle is hand-computed
morphometry, not a trained token. Its windowing convention also differs in a way worth flagging
rather than copying, a fixed 1 mm offset from the bifurcation rather than this repo's radius-scaled
`1·r_J`; given the diameter report's own finding that the LCx flare commonly extends past 1·r_J
(median flare end 2.5 mm, IQR up to 5.0 mm), a fixed 1 mm offset would likely reintroduce the flare
contamination the r_J-relative window was built to avoid, so the repo's existing convention should
be kept. Full detail in
[junction_tokenization_literature.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Bifurcation%20calibre%20in%20both%20models/junction_tokenization_literature.md)
Q2, with the retinal junction-classification literature (Q3, angle and diameter-ratio features used
for junction-*type* detection, never fused into an outcome model) and VesselGPT's whole-tree VQ-VAE
tokenization for *generation* (Q4, a weak analogy since it neither targets prediction nor
distinguishes junction from segment tokens) rounding out what does and does not transfer.

## The fusion rule already locked for the whole vessel extends cleanly; FPCA does not

This project's own precedent reports already settled how a scalar and a profile of the same
underlying signal must be shared between arms: "same covariate vector, same encoding... extra terms
in the regression, late-fused after the pooled sequence embedding" in the network
([fair_baseline_methodology.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Fair%20diameter%20scalars%20for%20regression/fair_baseline_methodology.md)).
Applying that rule at the junction scale is not a new fairness question with its own literature to
find; it is the same rule applied to a shorter domain. **The apparent asymmetry, the network reading
both the masked raw profile and the identical scalar token while the regression reads only the
scalar, is not an extra favour to the network: the scalar is a deterministic function of the same
profile the network already reads, so nothing is added that the network could not in principle
derive itself, and nothing is withheld from the regression that changes what it is allowed to see.**
The one genuine boundary is that nothing invented purely for the network's convenience, a learned
embedding of the ramus flag rather than the flag itself, for instance, is permitted unless the
regression gets an equivalent representation. General medical-imaging fusion literature (hybrid
handcrafted-plus-deep branches in an MRI tumour classifier and a respiratory-audio model, both using
late-fusion concatenation before the classifier head) confirms this mechanism is standard practice,
though neither is vascular-specific and neither addresses this project's specific fairness question
directly. Full detail, including how the junction token slots into the existing B0 to B4 baseline
ladder, is in
[fusion_mechanics.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Bifurcation%20calibre%20in%20both%20models/fusion_mechanics.md).

Functional logistic regression on FPCA scores, the information-matched rung already proposed for
the whole-vessel profile (citing logitFD and Goldsmith et al. 2011's DTI-tract-profile precedent),
does not extend safely to the junction window. **At 0.5 mm spacing, a 3 mm window holds roughly six
to seven points, and the sparse-FPCA literature that might seem to apply (pooling across subjects
observed at few, irregular time points) is solving a different problem: this project's junction
windows are densely and identically sampled across all ~800 subjects, so the binding constraint is
not cross-subject pooling but how many distinguishable modes of variation six to seven points can
support before higher components are fitting noise, which is likely one or two at most.** The
recommended substitute is a short, pre-registered summary-stat set (the window median already used,
plus an endpoint-to-plateau ratio, since the diameter report already measured exactly this quantity
in its flare tables), not full functional machinery. This is a reasoned default, not a measured one:
the concrete check, an eigenvalue-decay diagnostic on the real 36-case LM window data already
extracted for the diameter report, has not been run and should be, before this recommendation is
treated as locked. Full detail in
[fpca_short_window_feasibility.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Bifurcation%20calibre%20in%20both%20models/fpca_short_window_feasibility.md).

## The token, concretely

At the LM junction the token is 8 fields: Finet ratio (primary), daughter ratio, Γ_HK deviation,
r_LAD/r_LM, r_LCx/r_LM, the fixed-tangent angle, a ramus flag and LM length. LAD-D1 and LCx-OM1 drop
the parent-to-daughter pair and the ramus/length fields (there is only one daughter ratio and no
"LM length" equivalent there), landing at 3 continuous fields plus angle, and LCx-OM1 additionally
needs an OM1-absence flag. The crux keeps the same shape but every field there stays descriptive-
only, per the diameter report's own ICC 0.44 caveat, and should not enter either arm as a modelled
predictor yet. Every ratio field needs no further normalisation beyond its own definition; angle and
LM length are the only absolute-scale fields and get standardised or spline-modelled like the
project's other continuous scalars. **Γ_HK deviation is not yet implemented anywhere in the repo**;
it exists only as a formula in the diameter report and must be built, through the registry pattern
this project's CLAUDE.md prescribes, before it can enter either arm. Full field-by-field detail,
including exact dimensionality per junction, is in
[final_recommendation.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Bifurcation%20calibre%20in%20both%20models/final_recommendation.md).

## Conclusion

The question this report was asked to resolve, "junction tokens or late-fused junction features",
turns out to have a definite mechanical answer once broken apart: the token is the descriptor set
already locked, fused the same way covariates are already fused, on top of the profile channel that
was never going away. What the literature genuinely could not settle is whether that explicit token
should eventually be replaced or supplemented by a learned one; no coronary or vascular precedent
trains a junction embedding the way Bjørn's proposal describes, so that choice remains a design
fork for a later ablation, not a question this pass of research could close. Four items stay open
and need either a supervisor decision or a short pilot rather than more reading: the learned-versus-
explicit token fork itself, the still-untested k = 2 daughter-window sensitivity from the diameter
report, the FPCA eigenvalue-decay check that would turn this report's "skip it" from a reasoned
default into a measured one, and how either arm should represent a limb that does not exist in a
given tree (OM1 absence, no ramus). None of these four block writing the descriptor extraction code
itself; they block only the parts of the design that assume a learned architecture or a functional
representation neither of which is the recommended starting point here.
