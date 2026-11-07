# Thesis vocabulary, style and FPCA code for a Technical Background FPCA section

All sources are local repo files (read-only). Paths are relative to
`/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/`; `file:line` gives the line.

## 1. Vocabulary, notation, labels and section structure

### Takeaway
The thesis writes in American spelling ("centerline", "normalized", "summarized", "millimeters", "labeled"). It calls curvature "turning-angle curvature" or "mean turning" in rad/mm, with $\theta_j$, $\kappa_j$, $\ell$, $T_\ell$, $s$ and $\mathbf{c}(s)$ already defined. The FPCA section already has a placeholder, `\subsection{Functional Principal Component Analysis}` with `\label{sec:tech-fpca}`, inside the parked `05_risk_models.tex`. Its four-paragraph plan is stale: it describes logistic models and a 1D CNN, and the thesis now uses a cloglog GLMM.

### Cited Findings

**Where the section sits and its placeholder**
- The placeholder is `\subsection{Functional Principal Component Analysis}` `\label{sec:tech-fpca}` under `\section{Risk Prediction Models}` `\label{sec:tech-risk-models}`. The file is marked "PARKED: pointed back to by nothing" and "STALE: the FPCA subsection served the old curvature profile ... so FPCA may no longer be used" — [technical_background/05_risk_models.tex:1-5, 17-27](thesis/technical_background/05_risk_models.tex)
- The planned paragraphs are:
  - P1, the opener: "a curvature profile has one value per position, too many to enter a logistic model directly; FPCA summarises it".
  - P2: the mean function plus orthogonal component functions, giving K scores.
  - P3: the scores keep where along the artery the bend lies.
  - P4: a 1D CNN as the alternative, with too many weights.

  Source: [05_risk_models.tex:28-33](thesis/technical_background/05_risk_models.tex). P1 and P4 refer to a logistic model and a CNN that are no longer in the plan.
- "CITE WANTED: functional data analysis, Ramsay and Silverman." — [05_risk_models.tex:12](thesis/technical_background/05_risk_models.tex)
- Chapter order, from the chapter intro comments: image geometry, segmentation network, centerline extraction, curvature, risk models (parked), segment-level cloglog GLMM. The map from Methodology files to background sections has no FPCA entry. — [technical_background/00_chapter_intro.tex:6-20](thesis/technical_background/00_chapter_intro.tex)
- Chapter rule: "a sentence that would be true if this thesis had never been written is background; what was done, with which settings, on which data, is Methodology. Every section is pointed back to by a Methodology section ... if none does, cut it." Also: "Present tense ... No settings, no cohort, no results." — [00_chapter_intro.tex:3-5, 22](thesis/technical_background/00_chapter_intro.tex)

**Notation already defined (the FPCA section must reuse it and avoid clashes)**
- Centerline: "a space curve c(s) parametrised by arc length"; curvature $\kappa(s) = \lVert c''(s)\rVert$ is planned for the background (P1/P2 comments only). The written prose defines curvature as "the inverse of the radius of the circle that best fits the curve there". "the curvature profile is the curve of curvature against distance from the origin of the vessel, preserving where along the vessel a bend is located." — [technical_background/04_curvature.tex:14-24](thesis/technical_background/04_curvature.tex)
- Figure `\label{fig:curvature}` (rq_curvature.pdf) shows three synthetic centerlines with the same tortuosity index and different mean curvature. The caption uses "Color" (American). — [04_curvature.tex:29-37](thesis/technical_background/04_curvature.tex)
- Methodology symbols:
  - $\mathbf{v}_j$: vertices respaced at a chord of $\ell = 5$ mm.
  - $\theta_j$: turning angle, given by the atan2 form (`\label{eq:method-turn}`).
  - $\mathbf{a}_j$, $\mathbf{b}_j$: the arriving and leaving chords; $n$ the number of interior vertices.
  - $\kappa_j = \theta_j/\ell$: the "curvature profile", "turning per millimeter ... in rad/mm, ordered from the ostium outward" (`\label{eq:method-profile}`).
  - $T_\ell = \frac{1}{n_s\ell}\sum_{j\in s}\theta_j$: mean curvature of segment $s$ (`\label{eq:method-tl}`).

  Note that $s$ is used both for arc length (04_curvature) and as the segment index in $T_\ell$. — [methodology/06_curvature.tex:9-42](thesis/methodology/06_curvature.tex)
- Taper uses "arc length $s$, measured from the start of the trunk", $r(s)$ and $A(s)$. — [methodology/09_taper.tex:25-31](thesis/methodology/09_taper.tex)
- GLMM notation that the FPCA scores would feed into. The FPCA section must not reuse these symbols with other meanings:
  - $y_{ij}$ with person $i = 1,\dots,N$ and segment $j = 1,\dots,n_i$; $\mathbf{x}_{ij}$, $\eta_{ij}$, $\boldsymbol\beta$, $b_i \sim N(0,\sigma^2)$, $p_{ij}$.
  - Labels: `eq:tech-cloglog`, `eq:tech-glmm`, `eq:tech-mhr`, `eq:tech-lr`, `eq:tech-agg-conditional`, `eq:tech-agg-marginal`.
  - Sections: `sec:tech-segment-glmm`, `sec:tech-cloglog`, `sec:tech-glmm`, `sec:tech-glmm-likelihood`, `sec:tech-aggregation`.

  The clashes: $j$ is already the segment index here and the vertex index in 06_curvature, so a grid index needs another letter. $b_i$ is the random intercept, and $\boldsymbol\beta$ the coefficients. — [technical_background/06_segment_glmm_short.tex:13-103](thesis/technical_background/06_segment_glmm_short.tex)
- The week-10 FPCA notes use $M_{ij}$ for the people × grid matrix, $m_j$ for the mean, $D_{ij}$ for deviations, $\varphi_{kj}$ for patterns, $c_{ik}$ for scores, $\lambda_k$ for eigenvalues, $S_{jj'}$ for the covariance, $z = c/\mathrm{SD}$ for the standardised score, and grid points $u_j = (j-0.5)/50$. These are working notes, not thesis text. $S$ clashes with $S_i$ in eq:tech-agg-conditional. — [week10/fpca_explained.tex:42-214](thesis/week10/fpca_explained.tex)

**Cross-reference targets**
- `sec:tech-curvature` (κ(s), profile, noise), `fig:curvature`, `sec:method-curvature`, `eq:method-profile`, `eq:method-tl` and `eq:method-turn` — [label list from grep over thesis/](thesis/)
- `sec:method-split` (nine segments: proximal, mid, distal of LAD, LCx, RCA), `fig:method-segments`, `tab:method-segments`, `sec:app-split`, `sec:method-selection`, `sec:method-size` and `sec:method-size-who` (Riley criteria) — [methodology/02b_segment_split.tex:25-42](thesis/methodology/02b_segment_split.tex); [methodology/03_model_size.tex:12-22](thesis/methodology/03_model_size.tex)
- Labels that do not exist: no `sec:method-fpca`, and no methodology text describes FPCA. The only FPCA mention outside the stale long draft is "pointwise profiles" kept "for secondary analyses, reported apart from the test of the geometry block" — [methodology/04_feature_selection.tex:44](thesis/methodology/04_feature_selection.tex)

**Glossary (exact terms in use)**
- Anatomy and segments:
  - "left anterior descending (LAD)", "left circumflex (LCx)", "right coronary artery (RCA)", "left main (LM)" — [02b_segment_split.tex:17,20](thesis/methodology/02b_segment_split.tex)
  - "a proximal, a mid and a distal segment, giving nine segments per participant" — [02b_segment_split.tex:30](thesis/methodology/02b_segment_split.tex)
  - Results table uses "pLAD, mLAD, dLAD" — [results/00_cohort.tex:35](thesis/results/00_cohort.tex)
  - "trunk segments", "nine trunk segments", "the trunks", "each trunk" — [05_features.tex:11,17](thesis/methodology/05_features.tex); [02b_segment_split.tex:40](thesis/methodology/02b_segment_split.tex). Running text uses "proximal LAD" seldom; "pLAD" appears in results only.
- Curvature:
  - "Turning-angle curvature" is the feature name in tab:method-features — [05_features.tex:28](thesis/methodology/05_features.tex)
  - "mean turning angle per millimeter at a chord of 5 mm" — [10b_feature_validity.tex:75](thesis/methodology/10b_feature_validity.tex)
  - "curvature profile", "mean curvature", "turning per millimeter", "rad/mm", "chord" — [06_curvature.tex:27-40](thesis/methodology/06_curvature.tex)
  - "Upstream turning" — [04_feature_selection.tex:44](thesis/methodology/04_feature_selection.tex)
- Positions: "distance along an artery ... counted from the ostium" — [05_features.tex:13](thesis/methodology/05_features.tex). "ordered from the ostium outward" — [06_curvature.tex:9,33](thesis/methodology/06_curvature.tex)
- Data and cohort:
  - "in-house tracer", "Herlev--{\O}sterbro cohort", "baseline CCTA volumes" — [01a_inhouse_tracer.tex:10](thesis/methodology/01a_inhouse_tracer.tex)
  - "participants", which is the standard word for people in the thesis — [02_population_outcome.tex:17](thesis/methodology/02_population_outcome.tex)
  - "plaque-free baseline cohort" — [00_chapter_intro.tex:22](thesis/methodology/00_chapter_intro.tex)
  - "clean-baseline cohort" — [11_cross_validation.tex:5](thesis/methodology/11_cross_validation.tex); [04_feature_selection.tex](thesis/methodology/04_feature_selection.tex)
- Outcome: "The primary outcome was incident coronary plaque" — [02_population_outcome.tex:19](thesis/methodology/02_population_outcome.tex). "A participant who developed plaque only in the LM ..." — [02b_segment_split.tex:22](thesis/methodology/02b_segment_split.tex)
- Lumen: "lumen contours", "lumen mask", "cross-sections" — [09_taper.tex:27-34](thesis/methodology/09_taper.tex); [05_features.tex:14](thesis/methodology/05_features.tex)

**Spelling and style mechanics**
- American spelling dominates the chapter text: "summarized", "Color", "normalized", "millimeters", "labeled", "parametrized" — [04_curvature.tex:26,34](thesis/technical_background/04_curvature.tex); [06_curvature.tex:24,33](thesis/methodology/06_curvature.tex); [05_features.tex:22](thesis/methodology/05_features.tex)
- There are British slips: "idealised" — [09_taper.tex:18](thesis/methodology/09_taper.tex); "penalised" — [04_feature_selection.tex](thesis/methodology/04_feature_selection.tex). The comments and code use "normalised".
- The style guide asks to pick one spelling: "British spellings mostly ... with some American slips ... Pick one and stay consistent" (about Aida's thesis) — [style_guide_aida.md:314-315](thesis/style_guide_aida.md)
- `wordlist.txt` (326 entries) contains "centerline(s)", "PCA", "voxel" and "covariate". It lacks "FPCA", "eigenfunction", "eigenvalue" and "Karhunen". — [wordlist.txt](thesis/wordlist.txt)
- The bibliography is biblatex numeric, `sorting=none`, with `\cite{key}`. Author names appear in the text only as "Tello Ayala et al.\ \cite{...}". Citations go at the end of a sentence. — [week5/features_and_wss.tex:8-9](thesis/week5/features_and_wss.tex); [06_curvature.tex:14,44](thesis/methodology/06_curvature.tex)
- Section shape: the existing written background section (06_segment_glmm_short) runs about 100 lines. It opens with a definition sentence, has subsections in Title Case with `\label{sec:tech-...}`, uses numbered equations with `\label{eq:tech-...}` followed by a "where" sentence, and puts one sentence per source line. — [06_segment_glmm_short.tex:13-103](thesis/technical_background/06_segment_glmm_short.tex)

### Inferences
- If FPCA is kept as a subsection of `sec:tech-risk-models`, that parent section is itself parked and unwritten. A writer may need to attach FPCA to `sec:tech-curvature` (04_curvature.tex) instead, as a subsection on summarising the curvature profile, or make it a section of its own. A Methodology section must point back to it, and none does yet.
- Notation proposal that avoids the clashes:
  - functions: $x_i(t)$ on $t\in[0,1]$ (normalized position), mean $\mu(t)$, eigenfunctions $\phi_k(t)$, eigenvalues $\lambda_k$, scores $\xi_{ik}$
  - grid: points $t_g$, $g = 1,\dots,G$
  - avoid $j$, $s$ (arc length vs segment), $S$, $b$, $\beta$, $\kappa_j$ reused as a function, and $c$ (the centerline $\mathbf{c}(s)$).

  This is my suggestion, not existing thesis text.

### Gaps
- No main thesis file (`main.tex`) or preamble was found, so neither `\usepackage` settings nor whether `\eqref` vs `Eq.~\eqref` is standard could be confirmed. 06_segment_glmm_short uses both `model~\eqref{}` and `Eq.~\eqref{}`.

## 2. Style rules that apply

### Takeaway
A Technical Background section opens with a definition sentence in the present tense. A subsection opens with the limitation of its parent and names the method as the answer. Equations form a chain, with the assumptions named and each symbol defined once in a "where" sentence. The section carries no settings, cohort, results or code names, and uses no first person, no forward references, no `\textbf`, no em dashes and no sentence starting with "Because".

### Cited Findings
- Section opener: "Every section starts by saying what the thing is, in the present tense, with its domain". Subsection opener: "opens with the parent's limitation and then names the variant as the answer" — [style_guide_technical_aida.md:62-87](thesis/style_guide_technical_aida.md)
- Background vs Methodology: "No hyperparameters, no settings, no ablations, no results." — [style_guide_technical_aida.md §2.3](thesis/style_guide_technical_aida.md). The grid size (50), the 5 mm chord, the K rules and pLAD/mLAD therefore belong in the Methodology.
- Introducing terms: "Full term, abbreviation in brackets"; "*commonly referred to as*"; symbols in a "Let ... denote" sentence. "No bold, no italics for new terms. Each term is defined once" — [style_guide_technical_aida.md §4](thesis/style_guide_technical_aida.md)
- Equations: a derivation chain where "Every reduction names what was assumed to get there"; symbols are defined in a "where" sentence; unnumbered equations are introduced with "can be expressed as" — [style_guide_technical_aida.md §5](thesis/style_guide_technical_aida.md)
- Checklist:
  - "Present tense; past only for history; no first person; no forward references; no chapter roadmap"
  - "No paragraph opens with *Because*; no appositive glosses; no em dashes; no `\textbf`"
  - "Performance or standing claims carry a source and a number with its population, or are cut"
  - "`hunspell -l -t -d en_US -p wordlist.txt`" (en_US dictionary, which confirms American spelling)

  — [style_guide_technical_aida.md §11](thesis/style_guide_technical_aida.md)
- "Two hazard closers only (`01`, `03`)". Curvature ends on smoothing "stated as fact" — [style_guide_technical_aida.md §10.2](thesis/style_guide_technical_aida.md); [04_curvature.tex:10](thesis/technical_background/04_curvature.tex)
- Project rules:
  - Methods text must match `CGPS_data/thesis_final/` exactly; "Do not describe planned or recommended analyses as done".
  - Never mention CAS-Net; all text is about CGPS (Herlev–Østerbro).
  - Outcome wording: "incident coronary plaque" for the outcome and "developed plaque" for people, never "new plaque" or "first ever".

  — [CLAUDE.md](CLAUDE.md)
- User rules from memory: reason first, then how; fold properties into the main sentence; no "Because" opener; no filler or lead-in sentences; be skeptical and never overstate evidence. FPCA "only pLAD/mLAD" — [memory: curvature-fpca-plad-mlad-only.md](~/.claude/projects/-Users-mathildebrinchsorensen-Desktop-ImageCAS-X/memory/curvature-fpca-plad-mlad-only.md)

### Inferences
- Under these rules the FPCA background should state:
  - the functional setting
  - the Karhunen–Loève expansion, with mean, covariance operator, eigenfunctions, eigenvalues and scores
  - the discretized version on a common grid, which is PCA of the centred matrix computed by SVD
  - fraction of variance explained
  - FPCA is unsupervised: components rank variance, not association with an outcome. This is a natural fact-closer and matches the week-10 sentence "FPCA finds the ways people differ most, not the ways that matter for plaque" — [fpca_explained.tex:188](thesis/week10/fpca_explained.tex)
  - possibly a note that amplitude vs phase variation needs registration (Sangalli et al.), stated as general fact.

  The grid of 50, the 5 mm chord, the Horn/bootstrap/CV rules for K and pLAD/mLAD stay in the Methodology.

### Gaps
- `style_guide_methodology.md`, `style_guide_methodology_aida.md`, `style_guide_clinical_aida.md` and `style_guide_sota_aida.md` were not read in full; only the technical guide and the spelling line of style_guide_aida.md were.

## 3. What the code does with FPCA (and mismatches)

### Takeaway
`CGPS_data/turning_profile_shapes.py` runs an outcome-blind, exploratory FPCA:
- Input: the sliding-window turning profile (sliding T5, rad/mm) of each segment, interpolated linearly onto 50 midpoints of normalised position.
- Method: column-centred, then PCA by `numpy.linalg.svd` with equal grid weights. There is no smoothing, no registration and no standardisation inside the FPCA.
- Scope: all 9 segments and 3 full trunks, by default on Medis trees (plaque at baseline). The tracer loader is not written.
- K: counted by six rules.

No outcome model with FPCA scores is coded, and nothing FPCA-related is in `CGPS_data/thesis_final/`. The decision that FPCA is descriptive only in pLAD and mLAD, with mean turning in the main model, is in memory and in the week-10 notes, not in thesis text or code. Several mismatches between text and code follow below.

### Cited Findings

**Curve analysed**
- "The turning profile is the sliding-window T5 (tortuosity.curvature.profile_thesis): the turning angle over a 5 mm chord before and after every centerline point, in rad/mm, computed on the whole trunk and then cut at the split_trunks boundaries." — [CGPS_data/turning_profile_shapes.py:6-8](CGPS_data/turning_profile_shapes.py)
- `profile_thesis(P, l, s=None, smooth=0.0)`: for each point $P_i$, it finds $B_i$ and $F_i$, the points on the polyline exactly $l$ mm away in a straight line before and after. It returns arc length $s_i$ and atan2(|a×c|, a·c)/l with a = P_i − B_i and c = F_i − P_i. "centred on each point instead of on vertices laid from P[0]". Smoothing is "Off by default: the tracer centerlines are expected to arrive smoothed already" — [tortuosity/curvature.py:70-92](tortuosity/curvature.py); `_at_chord` [tortuosity/curvature.py:48-60](tortuosity/curvature.py)
- Profiles are computed on the trunk path from `split_trunks.split`. Arc length for the LAD and LCx starts at the LM bifurcation, and for the RCA at the ostium: "Node path from the ostium (LM bifurcation for LAD/CX after split())". The figure axis label reads "mm along the trunk (RCA: ostium; LAD, LCx: LM bifurcation)" — [CGPS_data/split_trunks.py:11-14,103](CGPS_data/split_trunks.py); [turning_profile_shapes.py:208](CGPS_data/turning_profile_shapes.py)

**Resampling, normalization, grid**
- `on_grid` keeps profile points with lo ≤ pos < hi and requires at least `MIN_PTS = 5`. It maps position to (p − p[0])/(p[−1] − p[0]), that is 0 at the first and 1 at the last profile point of the segment, not at the segment boundaries. It evaluates at `g = (arange(n_grid)+0.5)/n_grid` by `np.interp` (linear). — [turning_profile_shapes.py:59,90-97](CGPS_data/turning_profile_shapes.py)
- `--grid` defaults to 50. — [turning_profile_shapes.py:307](CGPS_data/turning_profile_shapes.py)
- Inclusion:
  - a segment needs length hi − lo ≥ 2·chord (10 mm)
  - a full trunk needs end ≥ 4·chord (20 mm)
  - a matrix is analysed only if it has ≥ `QUARTILE_MIN` = 10 people

  — [turning_profile_shapes.py:106-110,324](CGPS_data/turning_profile_shapes.py); [CGPS_data/cgps_stats.py:47](CGPS_data/cgps_stats.py)
- Length normalization therefore removes segment length; the lengths are kept only for reporting (median length). There is no registration or warping. — [turning_profile_shapes.py:110,294](CGPS_data/turning_profile_shapes.py)

**Eigen-decomposition**
- `pca(M)`: `mean = M.mean(0)` and `np.linalg.svd(M - mean, full_matrices=False)`. The sign is fixed so that each component sums to ≥ 0. The variance shares are `S**2/(S**2).sum()`. The components are the rows of `Vt`, with unit Euclidean norm on the grid. — [turning_profile_shapes.py:114-118](CGPS_data/turning_profile_shapes.py)
- Scores: `(M - mean) @ Vt[:3].T`. Their SD is stored for the ±2 SD figures. The scores are not standardised or exported. — [turning_profile_shapes.py:173-175](CGPS_data/turning_profile_shapes.py)
- There are no quadrature weights: grid points are equally weighted, so eigenvectors are orthonormal in ℝ^50, not in L²[0,1]. The scale differs from functional eigenfunctions by a factor √50 (my inference from the code; the shares of variance are unaffected).

**Number of components (K)**
- The code has six rules (`var80`, `var90`, `horn`, `shift`, `boot`, `cv`), "with no cap from a parameter budget":
  - Horn: permute people at each grid position, 95th percentile.
  - shift: a circular shift of each person's deviation, a stricter null.
  - boot: bootstrap of people, with median |cosine| to the best-matching resampled component ≥ 0.9.
  - cv: 5-fold person split, predicting one contiguous fifth of the grid from the other four.

  `KMAX = 15`, `--perm 200`, `--boot 200`, `--seed 0`. — [turning_profile_shapes.py:12-24,57-60,126-175,305-309](CGPS_data/turning_profile_shapes.py)
- The written sources disagree on the rule for the final K:
  - "$K$: the patterns that pass Horn and the bootstrap, capped by the budget below." — [week10/fpca_explained.tex:234](thesis/week10/fpca_explained.tex)
  - "The smallest of the three is used" (Horn, bootstrap, CV) — [week10/fpca_from_plots.tex](thesis/week10/fpca_from_plots.tex)
  - "K = min(shapes that pass, K_max)", "(bootstrap, Horn, cross-validation)" — [CGPS_data/saved.md:5,25-26](CGPS_data/saved.md)
  - The code itself reports all six and picks none.
- Budget: `segment_k_budget.py` uses Riley criteria per single-segment model with base df = 1 (recalibrated SCORE2). Its output: pLAD has 275 events (K_max 5/10/18 at C = 0.65/0.70/0.75) and mLAD 201 (4/8/14). The other segments get ≤ 3 at C = 0.70 except mRCA (5) and pLCx (4). This is on 1,077 plaque-free people before the image-quality exclusion. — [CGPS_data/segment_k_budget.py:1-16,85](CGPS_data/segment_k_budget.py); [CGPS_data/saved.md:7-17](CGPS_data/saved.md)

**Which segments, and how scores are used**
- Decision (2026-11-04): "Main who model uses mean curvature (turning) per segment, one number. FPCA of the sliding-T5 profile (50 normalised positions, rad/mm) is run only on the proximal and mid LAD, each with its own descriptive cloglog model (SCORE2 + shape scores), not pooled and not part of the prespecified LR test." Also: "real φ1 is flat ('never crosses the mean'), so one-shape models equal mean curvature". And: "`turning_profile_shapes.py` still computes all 9 + 3 as exploration only." — [memory curvature-fpca-plad-mlad-only.md](~/.claude/projects/-Users-mathildebrinchsorensen-Desktop-ImageCAS-X/memory/curvature-fpca-plad-mlad-only.md)
- The planned model is cloglog(p_i) = a + g·SCORE2_i + Σ b_k z_ik, with z = c/SD. Here "$e^{b_k}$ is the hazard ratio per SD of pattern $k$", the model "is not coded yet", and its weights map back to $\beta_j = \sum_k (b_k/\mathrm{SD}_k)\varphi_{kj}$. — [week10/fpca_explained.tex:242-255](thesis/week10/fpca_explained.tex)
- Agreement between the shape score and mean turning: "Here the first shape is only nearly flat, yet the score on it and the mean turning correlate 0.998". This holds in made-up data. In the Medis centerlines "the first shape has the same sign along the whole segment and is close to a straight line ... this must be confirmed in the plaque-free cohort". — [week10/fpca_from_plots.tex](thesis/week10/fpca_from_plots.tex)
- The code docstring says: "The tracer trees are read with thesis_final/split_check.tracer_tree, which is not written yet; until then this runs on the Medis trees, whose people had plaque at baseline." `--trees` defaults to `medis`. — [turning_profile_shapes.py:29-31,304](CGPS_data/turning_profile_shapes.py)
- `CGPS_data/thesis_final/` holds only `README.md` and `split_check.py`; no FPCA or curvature code. — (directory listing)

**Mismatches to report**
1. Profile definition. Methodology 06_curvature defines the curvature profile $\kappa_j = \theta_j/\ell$ on vertices respaced at 5 mm "Starting at the ostium", and $T_\ell$ from those vertices. FPCA uses the sliding-window profile centred on every original point (`profile_thesis`), which is "Same chord and angle ... but centred on each point instead of on vertices laid from P[0]". The text describes no sliding profile. — [06_curvature.tex:9-40](thesis/methodology/06_curvature.tex); [curvature.py:70-75](tortuosity/curvature.py)
2. Origin. 05_features says "Every artery was traversed from [the ostium], so that distance along an artery ... [is] counted from the ostium". The code starts the LAD and LCx at the LM bifurcation. This does not change normalized FPCA positions, but it does change which part of the profile is lost in the first 5 mm. — [05_features.tex:12-13](thesis/methodology/05_features.tex); [split_trunks.py:11-13,103](CGPS_data/split_trunks.py)
3. Smoothing. 06_curvature states "No smoothing was applied beyond the respacing", while the tracer smoothing is an open question to Kit — [06_curvature.tex:15](thesis/methodology/06_curvature.tex); [01a_inhouse_tracer.tex:16](thesis/methodology/01a_inhouse_tracer.tex). The FPCA code adds no smoothing (`smooth=0.0`); the sliding window itself acts as a 5 mm scale.
4. Data. The FPCA has only been run on Medis trees (people with plaque at baseline). The tracer loader does not exist, so no FPCA on the plaque-free cohort exists yet.
5. Stale drafts.
   - `methodology_long_draft.tex:211` reads "The profile was summarized by functional principal component analysis fitted on ImageCAS-X". Its Model 2 replaces $\bar\kappa$ with PC scores in a tested LR comparison. This contradicts the current decision (descriptive only, CGPS, pLAD/mLAD) and should not be used.
   - `week5/risk_model_plan.tex:69` reads "$K$ (3 to 5) functional principal component scores".
   - The 05_risk_models plan, with its logistic model and 1D CNN, is likewise stale.

   — [methodology_long_draft.tex:195-265](thesis/methodology/methodology_long_draft.tex)
6. Standardised scores and the descriptive pLAD/mLAD models are described in the week-10 notes but not implemented.
7. Final K rule, as listed above: three different written versions, and none is implemented.
8. 06_curvature says $T_\ell$ is missing when there are "fewer than two turning angles", while FPCA requires ≥ 5 profile points and length ≥ 10 mm. These are different inclusion rules.

**Figures that could be reused**
- `thesis/week10/week_figure/fpca/` holds made-up data from 300 people "run through the same code":
  - f1_turning_geometry (the turning angle at one point)
  - f3_grid (a segment in mm and on 50 places)
  - f4_profiles_deviations (curves, mean, deviations)
  - f5_covariance (covariance and the first three components)
  - f6_steps, f6b_score, f6c_spread
  - f7_mean_pm (mean ± 2 SD per component)
  - f8a_rebuild (reconstruction)
  - f9_scree, f10_boot_cv
  - f11_model, f12_budget (f12_budget uses CGPS counts)

  — [week10/fpca_explained.tex:24-27,46-260](thesis/week10/fpca_explained.tex); scripts [week10/fpca_explained_figures.py](thesis/week10/fpca_explained_figures.py), [week10/fpca_steps_figures.py](thesis/week10/fpca_steps_figures.py) ("made-up data, local"). There is also `week_figure/fpca_steps/fake/` (p3_story.png etc.).
- The week-10 figures are PNG with a custom palette. The thesis figures are PDF, e.g. `content/background/figures/rq_curvature.pdf` in 04_curvature. For a background section, made-up-data figures (f4, f7, f8a) suit the rule "no cohort, no results". f12_budget and any Medis-based figure (turning_profile_shapes_phi_*.png) are results and Methodology material.
- `turning_profile_example.{png,pdf}` "shows one person's anatomy ... check with Kit before it leaves the server" and must not be reused without clearance. — [turning_profile_shapes.py:26-29](CGPS_data/turning_profile_shapes.py)

**References already in refs.bib (183 entries)**
- `sangalli2009aneurisk`: Sangalli, Secchi, Vantini, Veneziani, "A Case Study in Exploratory Functional Data Analysis: Geometrical Features of the Internal Carotid Artery", JASA 104(485):37–48, 2009, marked "[BIBLIOGRAPHY VERIFIED]". The note reads "radius and curvature profiles of ICA centerlines (free-knot regression splines), registered along the vessel, then functional PCA". It is the only FDA/FPCA reference in the file. — [refs.bib:1711-1724](thesis/refs.bib)
- Absent: Ramsay & Silverman (FDA book), Yao/Müller/Wang 2005 (PACE), Horn 1965 (parallel analysis), Jolliffe (PCA) and Karhunen/Loève. The file has no entry matching "ramsay", "silverman", "horn", "jolliffe" or "principal component".
- Related keys that exist: `telloayala2026tortuosity`, `kashyap2022tortuosity`, `araki2020plaques`, `vanzandwijk2019curvature`, `zhang2024curvature`, `riley2020samplesize`, `hoerl1970ridge`, `prentice1978grouped`, `pavlou2015marginal`, `statacorp2025mecloglog`.
- `sangalli2009aneurisk` is not cited in any chapter .tex under thesis/ (the grep over .tex returned no chapter hits).

### Inferences
- The background section can be written generally (FPCA of curves on a common domain, discretized by SVD). It must leave all of the following to the Methodology: the grid of 50, linear interpolation, normalization to [0,1], the 5 mm sliding window, the K rules and the pLAD/mLAD scope. The Methodology text for those does not exist and would currently describe code that runs only on Medis trees, so it must not yet be written as done.
- The background should present FPCA as a description of between-person variation in profile shape that does not use the outcome. Claims that it "keeps where along the artery the bend lies" are accurate only relative to the normalized position within a segment, since segment length is removed.
- The code weights grid points equally and normalizes length, so the "functional" part is the common-domain interpolation. The discrete PCA approximates FPCA with eigenfunctions $\phi_k(t_g) \approx \sqrt{G}\,V_{kg}$ on a uniform grid (standard result; not stated in repo).

### Gaps
- No `turning_profile_shapes.md` output (shares of variance, K per rule) was found locally. It lives on dtu-gpu-7, so the claim that real φ1 is flat rests only on memory and week-10 prose.
- Which final K rule will be used is undecided (three written versions).
- Whether the tracer centerlines are smoothed before output is open, per the question to Kit in 01a_inhouse_tracer.tex:16.
