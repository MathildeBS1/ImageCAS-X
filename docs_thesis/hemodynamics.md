# Hemodynamics: turning topology into a functional endpoint

Companion to `literature.md`. Where that file surveys what exists, this one is a plan for how
hemodynamics fits *this* thesis, what is reachable with the data in hand, and what is not.

## Why this matters here

The causal chain the coronary literature runs on is:

```
geometry / topology  ->  hemodynamics (WSS)  ->  endothelial response  ->  plaque
```

Objectives 6-8 characterise the **first link only**. On its own that is a morphological
description: "these trees branch differently." Hemodynamics is what licenses the claim that the
difference *matters*. It is the reason bifurcation angle and tortuosity are considered
plaque-relevant at all, rather than incidental shape descriptors.

It also answers the thesis's weakest point. **Objective 10 has no outcome data** and may never get
any (see `CLAUDE.md`, Open questions). Wall shear stress is a *computed* endpoint: it is derived
from geometry, needs no patient follow-up, and is mechanistically upstream of the outcome we
actually care about. If outcome data never materialises, a hemodynamic endpoint is the honest
substitute — not a proxy for a missing label, but a different and defensible target.

The dataset authors intend this. `README.MD`, highlights:

> The labels support development and validation of methods for lumen segmentation, plaque and
> perivascular quantification, and **haemodynamic modelling**.

## The terms, and which are actually reachable

| Term | Definition | Reachable here? |
|---|---|---|
| **WSS** | Tangential frictional force of blood on the endothelium, Pa or dyn/cm². Low and oscillatory WSS marks where early lesions form. | **Yes** — analytically (Tier 1-2) and by CFD (Tier 3) |
| **OSI** | Oscillatory shear index, `0.5(1 - abs(int tau dt)/int abs(tau) dt)`, 0 to 0.5. How much shear *reverses* over the cardiac cycle. | Only Tier 3, and only **transient** CFD |
| **Helicity** | `H = int v . omega dV`. Rotational flow structure; generally considered protective. | Only Tier 3, 3D velocity field required |
| **FFR** | `P_distal / P_proximal` at maximal hyperemia; < 0.80 is functionally significant. | **No** — see below |
| **FFR-CT** | FFR derived computationally from CCTA by CFD. | Not without validation labels |

**FFR is not currently reachable, and this needs saying plainly.** ImageCAS ships no pressure
measurements and ImageCAS-X adds none, so there is no FFR ground truth to validate against. A
geometric resistance index (Tier 1) is *not* FFR: real FFR is dominated by nonlinear stenosis
losses and microvascular resistance under hyperemia, neither of which follows from lumen shape
alone. Worth asking the Rigshospitalet co-authors whether invasive FFR or FFR-CT exists for any
subset — that single question decides whether objective 10 has a functional endpoint.

**Note on naming:** `configs/ffr_unet.json` in this repo is *not* an FFR estimator. `models/ffr_unet.py`
is a segmentation architecture — "Feature-Fusion-and-Rectification 3D-UNet", single-channel lumen
logit — named for the group's downstream FFR application. Do not describe it as computing FFR.

## What we already have that makes this cheap

- **800 lumen surface meshes** (`surfaces/`, 3.5 GB, ASCII VTK POLYDATA). These are CFD-ready
  geometries. Having them precomputed is the single biggest reason this is tractable.
- **A validated rooted tree per side** (`topology/graph.py`), with exact connectivity, arc length,
  chord, tortuosity, generation, and `direction(span_mm)` for junction angles.
- **A local radius field, already implemented.** `utils/precompute_centerline_samples.py`
  computes `diameter_mm` as twice a Euclidean distance transform inside the GT lumen, sampled
  along the centerline, together with `dist_mm` from the ostium, `segment_name` and `hu`. This is
  exactly the radius data every formula below needs, and it does not have to be written.
  Its own caveat matters: the radius is unreliable within about one radius of a mask end — at the
  ostium (cut flat against the aorta) and at each terminus.

## Tier 0 — reframe what already exists (free, writing only)

No new computation; this is intro/discussion material that makes existing features mean something:

- **Tortuosity** -> curvature drives secondary (Dean) flow; the outer wall of a bend carries low,
  disturbed shear.
- **Bifurcation angle** -> flow separates at the carina; wider angles enlarge the low-WSS zone on
  the lateral walls, which is where LM-bifurcation lesions preferentially sit.
- **Dominance and the absent-left-main variant** -> a different flow *distribution*, not just a
  different picture. The 11 absent-LM sides feed LAD and LCX from separate ostia, so the LM
  bifurcation low-WSS region simply does not exist in them.

## Tier 1 — geometric hemodynamic surrogates (cheap, all 800 cases)

**Murray's law is the keystone — but the textbook exponent is wrong for coronaries, and that
changes the feature definition.** For laminar flow in a tube,

```
tau = 4 mu Q / (pi R^3)
```

Murray's law — minimising pumping power plus the metabolic cost of blood — gives `Q ~ R^3`.
Substituting, `tau` would be **constant** throughout the tree, which is the usual textbook claim
that deviation from Murray's law is deviation from uniform WSS.

**In coronaries specifically the cubic exponent does not hold.** Taylor et al. 2024, a systematic
review and meta-analysis over 1,070 coronary trees from 372 humans and 112 animals, puts the
pooled flow-diameter exponent at **k = 2.39 (95% CI 2.24-2.54)**, closely matching Kassab's
theoretical 7/3 ~ 2.33 rather than Murray's 3.0. The consequence matters:

```
tau ~ Q / R^3 ~ R^k / R^3 = R^(k-3) = R^-0.61
```

so in a *normal* coronary tree WSS **rises toward the smaller distal vessels** rather than staying
uniform. Uniform-WSS is therefore the wrong null hypothesis. Concretely this means:

- Reference the exponent to **2.39, not 3.0**. Report per-bifurcation `k` solving
  `R_0^k = R_1^k + R_2^k`, and the deviation `|k - 2.39|`, with the CI as a tolerance band.
- Fitting `k` cohort-wide is itself a result worth reporting: an 800-tree estimate would be large
  next to the studies in that meta-analysis, and it validates the segmentation and radius
  extraction at the same time.
- Expect and model the distal WSS rise; do not treat it as an anomaly.

Alongside it, per bifurcation:

- **Area ratio** `zeta = (R_1^2 + R_2^2) / R_0^2`. Values above 1 imply deceleration and
  separation-prone flow.
- **Finet's law** `D_0 = 0.678 (D_1 + D_2)`, the coronary-specific clinical rule — a second
  reference point, and the one interventional cardiologists actually use.
- **Poiseuille resistance index** along each ostium-to-terminus path, `R ~ sum(L / r^4)`, from the
  segment lengths already in `topology/graph.py`. A crude geometric analogue of pressure loss —
  explicitly *not* FFR.
- **WSS heterogeneity index**: with `Q ~ R^2.39`, compute `tau ~ Q / R^3` per segment and report
  the spread *relative to the expected `R^-0.61` trend*. A tree whose residual spread is large has
  regions of anomalously low shear by construction.

All of this is arithmetic over data we already have. Expect minutes for the full cohort.

## Tier 2 — 1D network hemodynamics (moderate, all 800 cases)

Solve a resistance network on the rooted tree: each segment a Poiseuille resistor
`R = 8 mu L / (pi r^4)`, in series along a branch and in parallel across a bifurcation, with flow
split by Murray's law or by outlet area. It is a sparse linear solve per case — seconds — and
yields per-segment flow `Q`, pressure drop, and mean WSS.

This is a genuine hemodynamic quantity rather than a shape descriptor, at full cohort scale. It is
the right level for population statistics (objective 8) and for feeding outlier detection
(objective 9). Nektar++ ships a `PulseWaveSolver` for exactly this class of 1D arterial network if
a hand-rolled solve proves limiting.

## Tier 3 — 3D CFD on a selected subset (expensive, ~20-40 cases)

Full 3D CFD on 800 cases is a thesis of its own. Bounded instead by using it as *validation*:

1. Tiers 1-2 give hemodynamic features for all 800.
2. Objective 9's outlier detection flags the topological and hemodynamic extremes.
3. Run 3D CFD **on the flagged cases plus a matched typical control group**.

This tests the thesis's central claim rather than assuming it: *do topological outliers actually
have adverse hemodynamics?* That turns objective 9 from "we found unusual trees" into "we found
trees whose geometry implies disturbed flow, confirmed by simulation" — which is a mechanistic
result, and a far stronger contribution.

Steady-state simulation gives time-averaged WSS. **OSI and helicity require transient, pulsatile
simulation** with an inflow waveform — several times the cost, and worth reserving for a handful
of illustrative cases rather than the whole subset.

Practical notes:
- The surfaces come from marching cubes on voxel labels
  (`utils/offline_generate_mesh_from_voxel.py`, isovalue 0.5, windowed-sinc smoothing). They still
  need CFD-grade preparation: inlet/outlet capping, remeshing, boundary-layer inflation.
- **Boundary conditions are the weak point.** There is no patient-specific flow data, so inlet
  flow and outlet resistances must come from literature-typical values or allometric scaling.
  State this as a limitation up front; it bounds every quantitative claim.

## The resolution limit — state this before quoting any WSS number

`tau ~ 1/R^3`, so relative radius error is **amplified threefold**:

```
d(tau)/tau = 3 dR/R
```

Volumes are 512x512xZ at 0.32-0.43 mm in-plane and 0.5 mm slice thickness. A radius error of one
half-voxel (~0.2 mm) gives:

| Vessel | Radius | Radius error | WSS error |
|---|---|---|---|
| LM / proximal LAD | ~2.0 mm | 10% | ~30% |
| Mid LAD / LCX | ~1.2 mm | 17% | ~50% |
| Distal / D2, OM2 | ~0.5 mm | 40% | >100%, meaningless |

**So restrict quantitative WSS claims to proximal and mid segments** (LM, proximal-to-mid LAD,
LCX, RCA) where radius is at least ~1.5 mm — roughly labels 1, 2, 3, 9. Distal branches can still
carry *topological* features, but not WSS numbers. This is a scoping rule worth writing into the
methods rather than discovering at review.

## Tooling available on the DTU cluster

`module avail` shows: **gmsh** (meshing), **nektar** (Nektar++: 1D `PulseWaveSolver` and 3D
`IncNavierStokesSolver`, built for arterial flow), **petsc** (sparse solvers), **paraviewbatch**
(headless post-processing), plus licensed **ansys** (Fluent) and **comsol**. No OpenFOAM module.
Nektar++ plus gmsh is the natural open-source path; Fluent is the conventional choice in the
clinical CFD literature if licence seats allow.

## Recommended sequence

1. **Tier 0 + Tier 1 now** — they need no CT images, so they are unblocked while the download
   runs, and Murray-law deviation is a strong objective-7 feature in its own right.
2. **Tier 2 next**, feeding objectives 8 and 9.
3. **Test against the one real endpoint we have**: `Disease` (yes/no, 388/412 over the 800 usable
   cases) in `Descriptors.xlsx`. Do topologically or hemodynamically extreme trees show higher
   disease prevalence? Coarse, but it is a genuine clinical variable and n = 800.
4. **Tier 3 last**, scoped by what objective 9 flags.

## To confirm with the supervisor

- Does any subset have **invasive FFR or FFR-CT**? This decides whether objective 10 has a
  functional endpoint or whether WSS becomes the endpoint.
- Is CFD in scope for this thesis, or does it belong to a collaborator? Tier 3 is a real
  commitment and is the natural place for a joint effort.
- **Citation check:** WSS/Murray/CFD references are currently *absent* from `literature.md`.
  Friedman et al. 1993 (shear and intimal thickening) and Wang et al. 2024 (LM morphological
  phenotypes and hemodynamics) were suggested in discussion but are not in this repo's
  bibliography and have not been verified here. Obtain and read them before citing.
