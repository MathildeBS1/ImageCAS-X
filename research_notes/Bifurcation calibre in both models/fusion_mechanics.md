# Fusion mechanics: what the network is and is not allowed to see beyond the regression

Scope: given the junction core is already masked identically in both arms (locked in
[Coronary bifurcation diameter descriptors.md](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Coronary%20bifurcation%20diameter%20descriptors.md)),
how should the bifurcation calibre scalars (Finet ratio, daughter ratio, Γ_HK deviation,
parent-to-daughter ratios) and the masked raw per-limb radius profile actually be wired into
Model 1 (logistic regression) and Model 2 (per-point/sequence network) so that a later "network
beats regression" claim is a representation result and not an information-leak artefact.

## Q1. Is there precedent for a hybrid arm that reads both a raw profile and explicit handcrafted scalars of that same profile?

### Takeaway
Yes, hybrid handcrafted-plus-learned fusion is a common, well-documented pattern in medical
imaging, almost always implemented as late fusion (concatenate a handcrafted-feature branch with a
learned-representation branch before the final classifier head). None of the found examples are
vascular-geometry-specific, and none discuss the fairness question this thesis actually has
(comparing against a *regression-only* arm that gets the scalars but not the profile), so the
precedent supports the mechanism, not the fairness argument.

### Cited findings
- A hybrid MRI brain-tumour classifier fuses handcrafted statistical features with deep (DINOv2)
  features on a ResNet-50 backbone, "integrating handcrafted features through early fusion and
  incorporating deep features via late fusion" [SNIP] ([PMC11228303](https://pmc.ncbi.nlm.nih.gov/articles/PMC11228303/)).
- A dual-branch respiratory-audio model runs a CNN-BiLSTM-attention branch on spectral-temporal
  data in parallel with a handcrafted statistical-descriptor branch passed through a fully
  connected layer, and fuses the two branches by feature-level concatenation, explicitly motivated
  by "preserving branch-specific learning dynamics" and avoiding the handcrafted signal being
  "overshadowed by high-dimensional deep embeddings" [SNIP] ([arXiv 2512.00563](https://arxiv.org/pdf/2512.00563)).
- Across a broader multimodal-medical-imaging-fusion review, CNNs remain the dominant encoder for
  the learned branch, and late fusion (concatenation before the head) is described as the standard
  mechanism for combining a handcrafted-feature branch with a learned branch [SNIP] ([review, arXiv 2404.15022](https://arxiv.org/html/2404.15022v1)).

### Inferences
Nothing here is coronary- or bifurcation-specific, so it grounds the *mechanism* (a small MLP
branch on explicit scalars, concatenated with a pooled sequence embedding, before the final
classifier layer) without adding coronary-specific numbers to cite. This project's own precedent
reports already reached the same mechanism independently and more precisely for this exact use
case: covariates "as additional regressors in LR" and "late-fused after the pooled sequence
embedding" in the network
([fair_baseline_methodology.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Fair%20diameter%20scalars%20for%20regression/fair_baseline_methodology.md)),
and the same rule restated for bifurcation descriptors specifically in
[Coronary bifurcation diameter descriptors.md](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Coronary%20bifurcation%20diameter%20descriptors.md)'s
"Both arms must see the same windows, masks and normalisation" section. The general-medical-imaging
literature adds only that this is a common, not idiosyncratic, design choice.

### Gaps
No source discusses the specific fairness question of a hybrid-profile-plus-scalar network arm
compared against a scalar-only regression arm computed from the *same* profile. That question is
answered analytically below (Q2), not from literature, because no literature was found addressing
it directly.

## Q2. Is it unfair for the network to receive both the masked raw profile and the explicit scalar token derived from that same profile, when the regression only gets the scalar?

### Takeaway
**No, provided the scalar token given to the network is exactly the same numbers given to the
regression, and nothing is added to the network's token that is not also computed for the
regression.** The apparent asymmetry (network sees profile *and* scalars; regression sees only
scalars) is not new to the junction case; it is the same design already locked for the whole
vessel, where the network reads the full curvature/radius profile and the regression reads its
mean. Repeating that same choice at the junction scale is consistent, not an extra favour to the
network.

### Inferences [DERIVED]
The fairness rule this project has already established (Q4 of
[fair_baseline_methodology.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Fair%20diameter%20scalars%20for%20regression/fair_baseline_methodology.md))
is "same covariate vector, same encoding" for anything fused as a scalar, and separately, "the
network sees every point" as the acknowledged, accepted asymmetry that the information-matched
rungs (B2 through B4) exist to characterise, not eliminate. Two things follow directly:

1. **The scalar token itself must be identical between arms.** If the network's late-fused token
   includes Γ_HK deviation or the ramus flag, the regression's term list must include the same
   fields with the same encoding (splines for continuous terms, one-hot for categorical, per the
   Fair diameter report's own rule). Nothing invented for "the network's convenience" (for example,
   a learned embedding of the ramus flag rather than the flag itself) is allowed unless the
   regression gets an equivalent representation.
2. **Giving the network the raw masked profile *in addition to* the scalar token is not an
   information leak, because the scalar token is a deterministic function of that same profile.**
   The regression's scalar and the network's scalar are computed identically; the network's
   *additional* access to the raw profile is the same "network sees every point" asymmetry the
   whole-vessel design already accepts and already builds an information-matched rung (B3) to
   quantify. There is no new fairness problem introduced by extending an already-accepted design
   choice to a shorter window.

The one thing that *would* be unfair is the reverse: handing the network junction information that
is not also, in principle, computable from the same window for the regression. Two concrete
version of this risk are the r_J-relative window offset itself (already shared, since both arms
read the same windowed points by construction) and any auxiliary channel invented only for the
network, such as a raw voxel-intensity patch around the junction. The recommendation is therefore
to keep the network's dense channel restricted to exactly the quantities already defined
per-point in the repo (radius, and if used elsewhere, curvature), on exactly the masked domain
both arms share, plus the identical scalar token, and nothing else.

### Gaps
This is an internal consistency argument, not something independently validated by an external
study; no paper was found that states this principle explicitly for a profile-plus-summary
comparison. It follows directly from the project's own already-stated B0 to B4 ladder logic, so
the risk of it being wrong is mainly the risk that the ladder logic itself has a flaw the project
has not caught, not that this note introduces a new unexamined assumption.

## Q3. Does the junction scalar token change anything about the B0 to B4 baseline ladder already defined for the whole-vessel profile?

### Takeaway
No new rung is needed. The junction token is an addition to the existing B1 (scalar) rung's
covariate list, present at every rung from B1 upward, exactly like the whole-vessel diameter and
curvature scalars already are. The one rung that does *not* extend cleanly to the junction is B3
(FPCA / functional regression on the profile), addressed separately in
[fpca_short_window_feasibility.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Bifurcation%20calibre%20in%20both%20models/fpca_short_window_feasibility.md).

### Inferences [DERIVED]
Concretely, using the ladder already defined in
[fair_baseline_methodology.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Fair%20diameter%20scalars%20for%20regression/fair_baseline_methodology.md):
- **B0** (covariates only) is unchanged; the junction token is not a covariate in the clinical
  sense (age, sex), it is a geometric descriptor, so it belongs with the other geometric scalars
  from B1 onward, not with B0.
- **B1** (pre-specified clinical/geometric scalars) gains the junction token's fields: LM Finet
  ratio as primary, daughter ratio and Γ_HK deviation as secondaries, exactly the roles already
  assigned in the descriptor table of
  [Coronary bifurcation diameter descriptors.md](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Coronary%20bifurcation%20diameter%20descriptors.md).
- **B2** (fixed summary-stat set per channel) is where a junction-specific addition is worth
  considering: a short, pre-registered summary of the masked window's *shape*, not just its
  median, such as the window's endpoint-to-plateau ratio already measured in the diameter report's
  flare tables. This is cheap, interpretable, and does not require functional machinery.
- **B3** (FPCA / functional regression) does not extend safely to the 3 mm junction window; see the
  dedicated note.
- **B4** (generic time-series classifier features, e.g. MiniROCKET) was never proposed as
  mandatory even for the whole vessel and is lower priority here than getting B1 to B3 right at the
  junction scale for the first time.

### Gaps
None beyond what is already flagged in the whole-vessel ladder notes; this is a direct application
of an existing framework, not new territory requiring its own evidence base.
