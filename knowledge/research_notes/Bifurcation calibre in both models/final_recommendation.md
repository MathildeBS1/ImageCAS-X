# The concrete junction token, junction by junction, and what remains open

Scope: synthesises the tokenization, fusion and FPCA notes in this directory into one explicit
vector definition per junction, with dimensionality, normalisation and how each arm consumes it.

## Q1. What exactly is the LM junction token?

### Takeaway
An 8-field vector, all of it already-locked scalars from
[Coronary bifurcation diameter descriptors.md](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Coronary%20bifurcation%20diameter%20descriptors.md),
none of it new engineering, plus the masked raw radius profile on each limb already available as
the per-point channel.

### Inferences [DERIVED, synthesising the diameter report's locked descriptor table with this
report's fusion and FPCA findings]

| # | Field | Type | Source | Role |
|---|---|---|---|---|
| 1 | Finet ratio F = r0/(r1+r2) | continuous, dimensionless | `topology/angles.py`-style window | Primary |
| 2 | Daughter ratio r_small/r_large | continuous, dimensionless | same window | Secondary |
| 3 | Γ_HK deviation | continuous, dimensionless | same window (needs implementing) | Secondary |
| 4 | r_LAD/r_LM | continuous, dimensionless | same window | Secondary |
| 5 | r_LCx/r_LM | continuous, dimensionless | same window | Secondary |
| 6 | Fixed-tangent angle | continuous, degrees | `topology/angles.py` (already implemented) | Nuisance covariate, per the regional report's own primary-angle framing |
| 7 | Ramus flag | binary | topology (presence of a third LM daughter) | Stratum indicator, not pooled |
| 8 | LM length | continuous, mm | topology | Covariate (10.5 ± 5.3 mm typically; must be clipped per the diameter report's ostium rule) |

Dimensionality is 8 for the LM junction specifically. LAD-D1 and LCx-OM1 drop fields 4, 5, 7 and 8
(there is only one daughter ratio to a single side branch, no ramus concept, and no "LM length"
equivalent), landing at 3 fields (Finet, daughter ratio = same value at a 2-vessel junction, Γ_HK
deviation) plus the angle and an OM1-absence flag at LCx-OM1 specifically. The crux (RCA to
PDA/PLB) keeps the same 3 to 4-field shape but every field there is explicitly flagged descriptive-
only in the diameter report (Finet method ICC 0.44), so it should enter neither arm as a modelled
predictor for now, only as a reported sensitivity item.

**Normalisation.** Every continuous field except angle, LM length and the (currently unimplemented)
Γ_HK deviation is already a ratio, so it carries no separate normalisation step beyond what its own
definition provides, consistent with the project-wide rule to prefer ratios over absolute radii.
Angle and LM length are absolute-scale quantities and should be entered exactly as the rest of the
project's continuous scalars are (standardised using training-fold statistics only, or modelled
with restricted cubic splines at 3 to 4 pre-specified knots, per
[fair_baseline_methodology.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Fair%20diameter%20scalars%20for%20regression/fair_baseline_methodology.md)).
Γ_HK deviation is already zero-centred by construction (Γ_HK − 0.743), so no further centring is
needed once it exists.

**Consumption.** The regression gets all 8 fields as additional terms (continuous ones spline-
transformed, the ramus flag as a one-hot stratum indicator per the diameter report's own
recommendation to stratify rather than pool ramus cases). The network gets the identical 8 numbers
late-fused after its pooled sequence embedding, exactly as covariates are already fused elsewhere
in this project's design. The network additionally reads the masked raw radius profile on each limb
as its existing per-point channel, unchanged from the whole-vessel design; nothing about the token
removes or replaces that channel, per
[fusion_mechanics.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Bifurcation%20calibre%20in%20both%20models/fusion_mechanics.md)'s
fairness argument. No FPCA/functional rung is added at the junction scale, per
[fpca_short_window_feasibility.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Bifurcation%20calibre%20in%20both%20models/fpca_short_window_feasibility.md).

### Gaps
Γ_HK deviation is not yet implemented anywhere in the repo; it exists only as a formula in the
diameter report. It must be built before it can appear in either arm's input, and should go through
`topology/angles.py` or a sibling module via the registry pattern this project's CLAUDE.md
prescribes, not as a one-off script.

## Q2. What is genuinely unresolved and needs a supervisor decision or a pilot run, not more literature search?

### Takeaway
Four items. None of them can be settled by reading more papers; each needs either a decision this
project's supervisors have not yet made, or a short empirical check on real ImageCAS-X data.

### Inferences
1. **Learned versus explicit junction representation is an open architecture choice, not a settled
   question.** No coronary or vascular precedent found in this pass trains a learned junction
   token the way Bjørn's Perceiver-style proposal implies; Musio et al. 2025 is the closest match
   and it is hand-computed morphometry, not a trained embedding. Whether a learned latent-query
   encoder over the raw per-limb points is worth building as an alternative or addition to the
   explicit 8-field token in Q1 is a genuine design fork, and Perceiver's own documented small-
   dataset bias risk applies directly at this cohort's scale. This should default to the explicit
   token (Q1) as the primary design, with a learned-token variant as an optional later ablation,
   not the other way round, consistent with Kit's stated priority to not get "bogged down in the
   details of representation learning for now"
   ([from_superviser.tex](file:///zhome/e2/6/224426/project/ImageCAS-X/from_superviser.tex)).
2. **The daughter-window offset (k = 1 default versus the untested k = 2 daughter-only sensitivity)
   is still open**, flagged but not resolved in the diameter report's own robustness note. This
   report's token definition inherits whichever choice is made there; it does not re-litigate it.
   It should be locked once, in the same dated commit as the rest of the pre-registration, before
   junction tokens are computed for any junction beyond the already-profiled LM.
3. **FPCA feasibility at the junction window is reasoned here, not measured.** The one-script
   eigenvalue-decay diagnostic named in
   [fpca_short_window_feasibility.md](file:///zhome/e2/6/224426/project/ImageCAS-X/research_notes/Bifurcation%20calibre%20in%20both%20models/fpca_short_window_feasibility.md)
   Q2 has not been run. This report's "skip FPCA at the junction scale" recommendation should be
   treated as a default pending that check, not a locked conclusion.
4. **Absent-limb handling is undefined.** OM1 is absent in roughly 20 of 100 sampled trees per the
   diameter report; the ramus flag by definition marks a limb that does not exist in most cases.
   Neither arm's input format for "this field does not apply to this case" (a padding value, a
   separate mask channel, a stratified model) has been decided, and the choice interacts with the
   ramus-stratification recommendation already made in the diameter report. This is a modelling
   decision the diameter report deferred and this report does not resolve either.

### Gaps
None beyond what is stated; these are genuinely open items, listed rather than resolved by design.
