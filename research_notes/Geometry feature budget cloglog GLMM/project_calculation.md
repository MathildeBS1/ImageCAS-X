# Geometry parameter budget of the segment-level cloglog GLMM: project calculation

Everything here is **own calculation** on aggregate project numbers and **synthetic data**. No individual CGPS data were used or requested. Script: `research_notes/Geometry feature budget cloglog GLMM/budget_sim.py` (numpy 2.x / scipy 1.18 only; own Gauss–Hermite cloglog GLMM, analytic gradient, L-BFGS-B). Full output: `budget_sim_output.md` in the same folder (40 replicates per scenario, runtime 1,166 s on 8 cores; seed 20261102). Rerun: `python3 budget_sim.py --reps 40`.

Aggregate inputs: 1,076 people with an outcome, 452 (42.0 %) developed trunk plaque; 1,041 complete cases, 433 events; OOF log-loss 0.6284 (SCORE2 recalibrated) and 0.6346 (refitted factors); OOF C 0.687 / 0.686; refitted HRs per SD — [score2_honesty.md](file:///Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/score2_honesty.md). 1,534 trunk plaque segments in 626 affected people (2.45 per person) and artery shares LAD 846 / CX 260 / RCA 428, from the **old 1,352-person table** — [plaque_location.md](file:///Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/plaque_location.md). Base design as in `design()` — [progression_who_pooled.py](file:///Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/progression_who_pooled.py).

## 1. Riley criteria at person level

### Takeaway
At an anticipated C of 0.70 the shrinkage criterion (i) allows **P_max ≈ 15** parameters (n = 1,076; 14.6 at n = 1,041), 8 at C = 0.65, 18.5 at C = 0.72, 24 at C = 0.75. Criterion (ii) never binds (≈ 42–45) and (iii) is met (needs n ≥ 374). If every fixed effect is counted (base 12 df recalibrated, 17 refitted), the five-feature geometry block fits only at C ≥ 0.72 (recalibrated) or C = 0.75 (refitted).

### Cited Findings
- Criterion (i): n = P / ((S − 1) ln(1 − R²_CS/S)), S = 0.9; (ii): S_VH = R²_CS/(R²_CS + δ·R²_CS,max), δ = 0.05; (iii): n = (1.96/0.05)² φ(1 − φ) — [Riley et al. 2020, BMJ](https://doi.org/10.1136/bmj.m441)
- C → R²_CS conversion: assume a normal linear predictor with equal variance in events and non-events, mean shift √2·Φ⁻¹(C), fit a logistic model to it and take R²_CS from the LR — [Riley, Van Calster & Collins 2021, Stat Med 40:859–864](https://research.birmingham.ac.uk/en/publications/a-note-on-estimating-the-cox-snell-rsub2sub-from-a-reported-c-sta) (doi 10.1002/sim.8806). Here it is computed by quadrature instead of the paper's large simulation.
- Own calculation, n = 1,076, φ = 0.420, max R²_CS = 0.7435 (1,041 rows in parentheses):

| anticipated C | R²_CS | P_max (i) | S_VH (ii) | P_max (ii) |
|---|---|---|---|---|
| 0.65 | 0.0675 | 8.4 (8.1) | 0.645 | 42.3 |
| 0.70 | 0.1181 | 15.1 (14.6) | 0.761 | 43.5 |
| 0.72 | 0.1419 | 18.5 (17.8) | 0.792 | 44.1 |
| 0.75 | 0.1812 | 24.2 (23.3) | 0.830 | 45.1 |
| 15 % of max R²_CS | 0.1115 | 14.2 (13.8) | 0.750 | 43.3 |

- Aggregate anchor (own calculation from the reported OOF log-loss): R²_CS = 1 − exp(−2(ℓ_null − ℓ_model)) gives **0.099** for recalibrated SCORE2 and 0.087 for the refitted factors (n = 1,076; 0.096 / 0.085 at n = 1,041). That lies between the C = 0.65 and C = 0.70 rows, consistent with the observed OOF C of 0.687 — [score2_honesty.md](file:///Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/score2_honesty.md).

### Inferences
- Since the base alone reaches about C 0.69 out of fold, a full model C of 0.70–0.72 is the plausible range. The person-level budget is then **15–18.5 df in total**, which matches the plan's "15–20 at C = 0.70".
- With the anchor available, the anticipated C can be set from the project's own base model (it uses the outcome but no geometry) instead of PARADIGM. The draft says the budget "used the number of participants and events only", which would then have to change.

### Gaps
- The quadrature conversion has not been checked against `pmsampsize` (R is not installed here). The numbers should be confirmed in pmsampsize before they are quoted.
- Riley's criteria are for independent rows. No extension to clustered or aggregated models was found, so it is unclear which parameters of a segment GLMM count toward P (see section 3).

## 2. Harrell m/15 at segment level with a design effect

### Takeaway
With about 1,107 estimated segment events, Harrell's binary limiting sample size m = min(events, non-events) = 1,107 gives **54, 39 and 23 df** at latent ICC 0.1, 0.3 and 0.55 respectively. The prior project report's 35–60 df used the ordinal formula 3nq(1 − q), which for a binary outcome gives about 2.7× more. The synthetic generator reproduces 2.45 segments per affected person only at a **latent ICC of about 0.55**, well above the 0.1–0.3 assumed so far.

### Cited Findings
- Harrell's limiting sample size: m = min(n₁, n₂) for a binary outcome, n − n⁻²Σnᵢ³ for an ordinal one; keep candidate df ≤ m/10–m/20 — [Harrell, RMS ch. 4](https://hbiostat.org/rmsc/multivar). This is quoted from memory of that table and was not re-fetched in this task. The prior project report cites the same page for 3nq(1 − q) — [Segment plaque risk model nonlinearity.md](file:///Users/mathildebrinchsorensen/Desktop/Speciale/CGPS_statistics-/reports/Segment%20plaque%20risk%20model%20nonlinearity.md).
- Segment events are **estimated, not counted**: 452 × 2.45 = 1,107 of 9,684 rows (q = 0.114), where 2.45 = 1,534 / 626 comes from the old 1,352-person table — [plaque_location.md](file:///Users/mathildebrinchsorensen/Desktop/ImageCAS-X/CGPS_data/plaque_location.md).
- Own calculation. The design effect is 1 + (9 − 1)ρ_obs, with ρ_obs the **observed-scale** within-person correlation of the segment outcomes, measured on 100,000 synthetic people (it is much smaller than the latent ICC):

| latent ICC (σ) | ρ_obs | DE | df, m = min | df, m = 3nq(1−q) | synthetic segment events per 1,076 | segments per affected |
|---|---|---|---|---|---|---|
| 0.10 (0.43) | 0.045 | 1.36 | 54 | 144 | 659 | 1.46 |
| 0.30 (0.84) | 0.111 | 1.89 | 39 | 104 | 775 | 1.72 |
| 0.55 (1.42) | 0.268 | 3.15 | **23** | 62 | 1,055 | 2.33 |

### Inferences
- At 42 % person risk, the 2.45 events per affected person pin σ near 1.4–1.5. A dry run gave 2.36 at ICC 0.55 and 2.77 at 0.65, with ≈ 1,070 and 1,260 events per 1,076 people. ICC 0.1–0.3 would give only 660–780 segment events, which contradicts the 1,107 estimate. Read together, the two aggregates point to a strongly clustered outcome. The DE is then about 3, and the segment-level Harrell budget (~23 df) is about as tight as the person-level Riley budget.
- The two budgets cover the same model. With the 12–17 base df, Harrell at ICC 0.55 leaves 6–11 geometry df.
- A DE taken from the latent ICC is the right correction for a person-level covariate. For a covariate that varies within person, clustering costs less, since part of its information comes from within-person contrasts.

### Gaps
- No published ICC exists for incident segment plaque. The 2.45 ratio comes from a different cohort (46 % affected) and is sensitive to the assumed segment shares, so the ICC ≈ 0.55 is an indirect estimate only. The real fit of the null GLMM should report σ̂.
- The p/m/d event split within arteries, the segment lengths and the log-length coefficient (0.5) are assumptions.

## 3. Simulation: person-level calibration slope of the aggregated risk as geometry df grow

### Takeaway
In no scenario did the mean out-of-sample calibration slope of the aggregated person risk fall below 0.9 by k = 12 geometry df (total 24–29 fixed df). The slope falls by only ≈ 0.003–0.006 per added geometry df. The tightest case (refitted base, ICC 0.3) reached 0.901 (MC SE 0.009) at k = 12, so it would cross 0.9 at about k ≈ 12–13. At the planned 5 df (7 with Mundlak) the slope was 0.92–0.99 in all scenarios. By this criterion the strict Riley count (section 1) is **conservative** for this design.

### Cited Findings (all own calculation, synthetic)
- Design: 1,076 people × 9 segments. Segment baseline hazards set the event shares to LAD 0.55 / CX 0.17 / RCA 0.28 (p/m/d split assumed). Log length has coefficient 0.5. Six factors with the score2_honesty HRs per SD are scaled by c so that the true base person C ≈ 0.70. A SCORE2-like proxy (age-heavy weights plus noise) is used for the recalibrated base. Log follow-up has HR 1.19. Right dominance (88 %) has no true effect. The intercept is set to 42 % person risk. A person random intercept has σ from the latent ICC.
- Geometry: 5 "planned" features with conditional HR per SD 1.20 (curvature, segment-level), 1.15 (LM angle, person-level), 1.15 (taper, segment-level), 1.10 and 1.10 (LM→LAD and LM→LCx ratios, person-level). Segment-level features have 30 % between-person variance. Person-level features correlate 0.2 with age. Features 6–12 are null (HR 1.0) or, in a sensitivity run, HR 1.10. Every person-level feature acts on all 9 rows (unlike `design()`, where the LM angle acts on pLAD/pCX only).
- Fit: own GLMM, 20 GH nodes. Person risk P = ∫[1 − exp(−e^b Σⱼ e^ηᵢⱼ)]φ(b)db with 40 nodes, evaluated on an independent synthetic validation set of 20,000 people. The slope is a logistic regression of person outcome on logit(P). 40 replicates per cell, all fits converged.

Mean OOS calibration slope (MC SE ≈ 0.009–0.015):

| scenario | base | k = 0 | 5 | 7 | 12 | P(slope < 0.9) at k = 5 / 12 | OOS C k = 0 → 5 |
|---|---|---|---|---|---|---|---|
| ICC 0.1, extras null | recalibrated | 1.014 | 0.970 | 0.959 | 0.939 | 0.12 / 0.20 | 0.674 → 0.688 |
| ICC 0.1, extras null | refitted | 0.951 | 0.929 | 0.924 | 0.910 | 0.30 / 0.40 | 0.698 → 0.710 |
| ICC 0.3, extras null | recalibrated | 0.939 | 0.932 | 0.924 | 0.906 | 0.40 / 0.55 | 0.661 → 0.675 |
| ICC 0.3, extras null | refitted | 0.936 | 0.923 | 0.917 | **0.901** | 0.38 / 0.53 | 0.688 → 0.699 |
| ICC 0.55, extras null | recalibrated | 0.976 | 0.970 | 0.960 | 0.945 | 0.23 / 0.33 | 0.667 → 0.677 |
| ICC 0.55, extras null | refitted | 0.977 | 0.964 | 0.960 | 0.947 | 0.15 / 0.17 | 0.698 → 0.705 |
| ICC 0.55, extras HR 1.1 | recalibrated | 1.007 | 0.993 | 0.991 | 0.980 | 0.07 / 0.05 | 0.678 → 0.687 |
| ICC 0.55, extras HR 1.1 | refitted | 0.987 | 0.979 | 0.976 | 0.965 | 0.12 / 0.17 | 0.700 → 0.707 |

- The mean heuristic shrinkage 1 − p/LR (LR against the intercept + σ model, segment level) was 0.94–0.97 throughout. It sits near the OOS slope at ICC 0.55, but overstates it by 0.02–0.03 for the refitted base at ICC 0.1–0.3.
- The refitted base at k = 0 is already at a slope of 0.94–0.98 (17 df). The recalibrated base's slope is not a pure overfitting measure, because the proxy is misspecified against the factor truth (a slope > 1 at ICC 0.1).
- **Even 40 % of single datasets** had a slope below 0.9 at k = 5 in the ICC 0.1–0.3 refitted-base scenarios. The mean is above 0.9, but the shrinkage of one realised model is uncertain.

### Inferences
- The 8 segment dummies and log length are identified mostly from within-person allocation over about 9,700 rows. They therefore cost far less person-level shrinkage than Riley's count assumes. Counting only person-varying base terms (log FU, SCORE2 or 6 factors, dominance: 3 / 8 df) is closer to the simulated behaviour (see table 5b).
- The five planned features add ΔC of only ≈ +0.007 to +0.014 at person level, despite segment-level HRs of 1.1–1.2. A larger σ makes this dilution stronger.
- Under these assumptions, Mundlak (+2 df) costs ≈ 0.003–0.01 in calibration slope, which is negligible.

### Gaps
- One generator family only, with 40 replicates. The predictors are independent apart from the stated correlations. There are no splines, no measurement error in geometry, and no LM-angle row restriction. A k beyond 12 was not simulated, and the crossing points are extrapolations.
- The simulation measures shrinkage under a correctly specified random-intercept model. Optimism from feature selection or coding choices is not included.

## 4. Power of the LR test of the geometry block

### Takeaway
With the "modest" segment-level effects assumed (HR 1.1–1.2 per SD on all 9 segments), the 5-df LR test had **power 1.00 in every scenario** (mean noncentrality ≈ 43–55). The df/power trade-off therefore matters only for much weaker signals. At a fixed noncentrality of 10, power falls from 0.89 (1 df) to 0.68 (5 df), 0.61 (7 df) and 0.50 (12 df).

### Cited Findings (own calculation, noncentral χ², α = 0.05)

| noncentrality λ | k = 1 | 2 | 3 | 5 | 7 | 9 | 12 |
|---|---|---|---|---|---|---|---|
| 5 | 0.61 | 0.50 | 0.44 | 0.36 | 0.31 | 0.28 | 0.25 |
| 10 | 0.89 | 0.82 | 0.76 | 0.68 | 0.61 | 0.56 | 0.50 |
| 15 | 0.97 | 0.94 | 0.92 | 0.87 | 0.82 | 0.78 | 0.72 |
| 20 | 0.99 | 0.99 | 0.98 | 0.95 | 0.93 | 0.90 | 0.87 |
| 30 | 1.00 | 1.00 | 1.00 | 1.00 | 0.99 | 0.99 | 0.98 |

- The earlier project figure (5 → 21 df: 0.56 → 0.30 at λ ≈ 7.85) has the same shape — [Segment specific geometry weights.md](file:///Users/mathildebrinchsorensen/Desktop/ImageCAS-X/reports/Segment%20specific%20geometry%20weights.md).

### Inferences
- A segment-level LR test is driven largely by within-person allocation. It can reject with near certainty while person-level ΔC is ~0.01, so power for the "who" claim should not be read from this test (consistent with the project's earlier allocation finding in the same report).
- If the true segment HRs are nearer 1.05, λ falls roughly fourfold (λ ∝ β²), into the 10–15 range where each extra df costs about 5–8 points of power.

### Gaps
- λ was not mapped to effect size beyond the two simulated truths, and power for the person-level ΔC was not simulated.

## 5. Geometry df affordable, by scenario

### Takeaway
Under the strict Riley count (all fixed effects), the 5-df block fits only if the full-model C is ≥ 0.72 (recalibrated base) or 0.75 (refitted base). Counting only person-varying base terms, 5 df fit at C ≥ 0.70 with either base, and 7 (Mundlak) at C ≥ 0.70 for the recalibrated base and C ≥ 0.72 for the refitted one. In the simulation, slope ≥ 0.9 held up to ≥ 12 geometry df in every scenario.

### Cited Findings (own calculation; n = 1,076; P_max from section 1)

5a. Strict count: base = log FU + SCORE2 (1) or factors (6; +1 diabetes) + dominance + 8 segment dummies + log length = 12 / 17 / 18 df. The random-intercept SD would add 1 more if counted.

| base | C 0.65 | C 0.70 | C 0.72 | C 0.75 |
|---|---|---|---|---|
| SCORE2 recalibrated (12) | −3.6 (no/no) | 3.1 (no/no) | 6.5 (yes/no) | 12.2 (yes/yes) |
| refitted factors (17) | −8.6 (no/no) | −1.9 (no/no) | 1.5 (no/no) | 7.2 (yes/yes) |
| refitted + diabetes (18) | −9.6 | −2.9 | 0.5 | 6.2 (yes/no) |

5b. Person-varying count: base = log FU + SCORE2/factors + dominance = 3 / 8 / 9 df. Hand arithmetic from the same P_max.

| base | C 0.65 | C 0.70 | C 0.72 | C 0.75 |
|---|---|---|---|---|
| SCORE2 recalibrated (3) | 5.4 (yes/no) | 12.1 (yes/yes) | 15.5 (yes/yes) | 21.2 (yes/yes) |
| refitted factors (8) | 0.4 (no/no) | 7.1 (yes/yes) | 10.5 (yes/yes) | 16.2 (yes/yes) |
| refitted + diabetes (9) | −0.6 (no/no) | 6.1 (yes/no) | 9.5 (yes/yes) | 15.2 (yes/yes) |

(yes/no = whether 5 geometry df without Mundlak / 7 with Mundlak fit.)

5c. Simulation, first k with mean OOS slope < 0.9: none up to 12 in all 8 scenarios. The closest was refitted ICC 0.3 at 0.901 for k = 12. Segment-level Harrell (section 2): 23–54 total df.

### Inferences
- The binding consideration is which Riley count applies. The strict count is the conservative, citable rule. The simulation suggests the true person-level cost of the within-person design terms is small. A defensible statement: "5 linear geometry df (7 with Mundlak) are within the Riley budget at C ≈ 0.70 when only person-varying parameters are counted. A simulation of the pooled model gave a mean calibration slope ≥ 0.92 at 5–7 geometry df with either base."
- The recalibrated base leaves 5 more df than the refitted base under either count. This favours it on budget grounds, in line with the ΔC = −0.001 decision in score2_honesty.md.

### Gaps
- No literature rule says how segment-level design terms count toward a person-level Riley budget. That choice is a judgement and must be stated as such.
- All conclusions depend on the synthetic design assumptions listed in section 3 and on the estimated (not counted) segment events.
