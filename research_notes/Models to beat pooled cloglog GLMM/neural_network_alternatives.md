# Neural-network alternatives to the pooled segment cloglog GLMM

Scope: NN models that keep training on the 9 per-segment binary outcomes, allow non-linear effects, and produce one person risk, judged against P(s) = 1 − exp(−exp(η_s + u_i)), P(person) = 1 − ∫∏_s(1 − p_s(u)) φ(u) du. Builds on `reports/Neural networks for segment plaque.md` (GNN ladder, data budget, Christodoulou/Grinsztajn/van der Ploeg, LMMNN/ARMED in brief) and `reports/Pooled segment GLMM background.md` (aggregation identity, b = 0 and naive-product errors, allocation information). Those findings are not repeated, only referenced.

Labels: **[preprint]** = arXiv only, not peer reviewed as far as found; **[unverified]** = citation details recalled, not opened in this research; **[inference]** = this note's reasoning, not a source claim.

## 1. Mixed-effects / random-effects neural networks

### Takeaway
Mixed-effects NNs exist (LMMNN, MC-GMENN, GLMMNet, ARMED, DeepGLMM, MeNets), but they were built for many clusters with *high-cardinality categorical* effects and large n, and binary support is the weakest part of each. None has been shown to beat a correctly specified GLMM on ~1,000 clusters of size 9 with ~10 covariates; and at prediction for a new person the random effect must be integrated out anyway, so the "mixed" part adds nothing the pooled GLMM's integration does not already do.

### Cited Findings
- LMMNN (Simchoni & Rosset, "Integrating Random Effects in Deep Neural Networks", JMLR 24, 2023; arXiv 2206.03314) is mainly regression on tabular data; classification is a GLMM-style section described as a preliminary attempt, compared with ignoring the cluster, one-hot, entity embeddings and `lme4::glmer` on test AUC — [arXiv 2206.03314](https://arxiv.org/pdf/2206.03314)
- The LMMNN author states classification supports only a single high-cardinality categorical feature and is a proof of concept, because the non-Gaussian likelihood has no closed form (would need VI or sampling) — [GitHub issue #14](https://github.com/gsimchoni/lmmnn/issues/14)
- MC-GMENN (Tschalzev, Nitschke, Kirchdorfer, Lüdtke, Bartelt, Stuckenschmidt) trains generalized mixed-effects NNs by Monte Carlo (MCMC for the random effects), separating cluster-specific random effects from cluster-invariant fixed effects; it states prior mixed-effects NNs were "limited to regression and binary targets with only one clustering feature" — [arXiv 2407.01115](https://arxiv.org/abs/2407.01115); peer-reviewed version at [IJCAI 2024](https://www.ijcai.org/proceedings/2024/555)
- MC-GMENN's simulations reuse LMMNN's data-generating scheme, vary number of clusters and noise, compare with target encoding and ARMED, and report ARMED underperforming in high-cardinality settings; a replication of LMMNN's binary experiments with a 4-hidden-layer ReLU net gave results close to the originals — [arXiv 2407.01115](https://arxiv.org/pdf/2407.01115)
- GLMMNet (Avanzi, Taylor, Wang, Wong, ASTIN Bulletin 54(2):213–238, 2024) combines a GLMM-like random-effect part for a high-cardinality categorical feature with a deep net for fixed effects, any exponential-dispersion family, fitted by variational inference; it "often outperforms or at least performs comparably with an entity embedded neural network"; code at agi-lab/glmmnet; it extends LMMNN — [arXiv 2301.12710](https://arxiv.org/pdf/2301.12710); [RePEc record](https://ideas.repec.org/a/cup/astinb/v54y2024i2p213-238_1.html)
- ARMED (Nguyen, Treacher, Montillo, IEEE TPAMI 45(7):8081–8093, 2023) adds a random-effects subnetwork plus an adversary that forces the fixed-effects subnetwork to be cluster-invariant; reported 5–28% relative improvement on seen clusters and 2–9% on unseen clusters vs conventional models, in dementia, cell imaging and simulated data — [PMC10644386](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10644386/); [arXiv 2202.11783](https://arxiv.org/abs/2202.11783v3); code [ARMED-MixedEffectsDL](https://gitfront.io/r/DeepLearningForPrecisionHealthLab/54f18307815dfb2148fbc2d14368c1268b63825e/ARMED-MixedEffectsDL)
- DeepGLMM (Tran, Nguyen, Nott, Kohn, "Bayesian Deep Net GLM and GLMM") uses a feed-forward net as basis functions inside a GLM/GLMM, fitted with Gaussian variational approximation with factor covariance and natural gradients; compares favourably with BART; Matlab/R/Python code at github.com/VBayesLab — [arXiv 1805.10157](https://arxiv.org/pdf/1805.10157) (journal venue, reportedly JCGS 2020, not confirmed by the search [unverified])
- GNMM theory/simulations for longitudinal/clustered data comparing with GLMMs and plain NNs on a schizophrenia dataset — [arXiv 2610.15270, via papers.cool](https://papers.cool/arxiv/2610.15270) [preprint]
- A 2021 simulation (Hapugoda & Sooriyarachchi) compared a GLMM with a generalized regression NN at n = 20, 100, 500: the NN fit better overall, but the GLMM did better at large n with high response correlation — [Tropical Agricultural Research](https://tar.sljol.info/articles/10.4038/tar.v32i1.8441) (low-profile venue; small simulation)
- MeNets (Xiong, Kim, Singh, CVPR 2019, mixed-effects CNN for gaze estimation) — not opened in this research [unverified]

### Inferences
- [inference] All these methods target a "many levels of a categorical variable" problem (users, occupations, sites) where the NN learns a large fixed-effect function from tens of thousands of rows. Here the cluster is the person (~1,000–1,200), each of size ≤ 9, and the fixed part has ~10–15 inputs. The GLMM's random intercept is already the exact "mixed" part; replacing the linear η with an MLP is the only change, which is DeepGLMM/GLMMNet in spirit.
- [inference] For a held-out person, every mixed-effects NN must integrate u_i over N(0, σ̂²) for the person risk, exactly as the background report derives. Several of these packages predict with u = 0 for unseen clusters (LMMNN/ARMED "fixed-effects" prediction), which gives the median-person risk, the error the pooled-GLMM report flags. Any adoption needs a custom Gauss–Hermite aggregation layer.
- [inference] Practical recipe that keeps the cloglog identity: a PyTorch model η_ij = f_θ(x_ij, z_i) (small MLP), marginal likelihood per person ∫∏_j Bern(y_ij; 1 − exp(−e^{η_ij + σb}))φ(b)db by 20–40-node Gauss–Hermite inside the loss (differentiable, 1-D, cheap). This is a "DeepGLMM by quadrature" and needs no special package; it reduces exactly to the current GLMM when f is linear. That makes it the cleanest nested comparison.
- [inference] Evidence that these beat a GLMM in small binary data: none found. Reported gains are vs encoding/embedding NNs, not vs glmer on matched linear truth.

### Gaps
- No head-to-head of LMMNN/GLMMNet/MC-GMENN against a GLMM with ~1,000 clusters of size ~9 and binary outcome was found.
- No mixed-effects NN with a cloglog link was found.
- MeNets and DeepGLMM journal details were not verified.

## 2. Multi-task / shared-backbone networks, set/graph pooling, noisy-OR or cloglog aggregation layer

### Takeaway
The architecture "shared backbone → 9 segment hazards → cloglog/noisy-OR aggregation → person risk, trained on segment labels" is well-founded algebraically (multiple-instance learning, discrete-time survival NNs) but no medical or coronary example with *observed* instance labels and a person frailty was found. Its realistic form is a small shared MLP with a segment embedding (= multi-task heads with parameter sharing) plus the GLMM's integrated random intercept.

### Cited Findings
- Noisy-OR multiple-instance learning: bag positive if any instance positive; p(y = 1 | x) = 1 − ∏[1 − σ(w'x_j)] (Raykar et al., ICML 2008); Liao et al. combined the top 5 lung nodules into a subject cancer probability by leaky noisy-OR (arXiv 1711.08324); mixed-model MIL aggregation in MixMIL (AISTATS 2024) — as summarised and linked in [Pooled segment GLMM background.md](../../reports/Pooled%20segment%20GLMM%20background.md) ([Raykar](https://icml.cc/imls/conferences/2008/papers/587.pdf); [Liao](https://arxiv.org/pdf/1711.08324); [MixMIL](https://arxiv.org/abs/2311.02455))
- Discrete-time hazard output layers for NNs exist and are trained by maximum likelihood with minibatches: Nnet-survival (Gensheimer & Narasimhan, PeerJ 7:e6257, 2019), Keras code, compared with Cox-nnet and DeepSurv — [PMC6348952](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6348952/); [code](https://github.com/MGensheimer/nnet-survival)
- Coronary GNNs (segments as nodes) exist only for labelling; recommended size 2–3 layers, ~32 hidden units; no future-plaque GNN found — [Neural networks for segment plaque.md](../../reports/Neural%20networks%20for%20segment%20plaque.md) citing [Hampe et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11095121/) and [Yang et al. 2020](https://ar5iv.labs.arxiv.org/html/2003.08560)

### Inferences
- [inference] With exactly 9 fixed, named segments, the tree is not a variable-size set: permutation invariance (Deep Sets) is *wrong*, because segment identity matters (position is part of the base). A shared MLP with a learned segment embedding, or 9 heads on a shared trunk, is the appropriate "multi-task" form. Attention or GNN message passing across 9 fixed nodes can be emulated by passing each segment's parent/neighbour features (rung 3 of the existing ladder).
- [inference] Plain noisy-OR (product of independent segment risks) is the naive product that the background report proves overestimates person risk. A NN aggregation layer must keep the integrated frailty: P_i = 1 − E_b[exp(−e^b Σ_j exp(η_ij))]. With cloglog, the NN only has to output η_ij; the aggregation is a fixed, parameter-free layer (log-sum-exp + Gauss–Hermite).
- [inference] Cross-segment attention or a GNN learns *within-person dependence*, which the random intercept already models as exchangeable. It could add value only if dependence is structured (e.g. adjacent segments share more than distant ones), i.e. a vessel-within-person effect, which a nested GLMM can capture with one more variance parameter.
- [inference] Because the "who" information is mostly in S_i = Σ exp(η_ij) and most segment-model information is allocation ("where", 93.8% in the project's own calculation for local features), a flexible segment network will mainly improve within-person ranking, not person-level C. The person-level ΔC ceiling for any segment-level NN is therefore lower than its segment-level gain suggests.

### Gaps
- No published medical model was found that trains on observed per-instance binary labels and aggregates with a cloglog/noisy-OR plus random effect to a person risk.
- No coronary multi-task network for incident plaque was found (consistent with the earlier report's search).

## 3. Interpretable non-linear NNs and GLM+NN hybrids

### Takeaway
The best-matched NN for this thesis is not a deep net but a constrained one: a GLMM skeleton with a small neural (or spline) residual, i.e. CANN-style "GLM with neural boost", or a neural additive model per continuous feature, both on the cloglog scale with the person intercept integrated. These nest the current model, so a gain can be attributed. The literature shows they match, not beat, ordinary GAMs; a penalised spline GLMM is the non-NN equivalent and is likely just as good at n ≈ 1,000.

### Cited Findings
- Neural Additive Models (Agarwal et al., NeurIPS 2021): one subnetwork per feature, summed; "more accurate than widely used intelligible models such as logistic regression and shallow decision trees" and "perform similarly to existing state-of-the-art generalized additive models" — [NeurIPS 2021](https://papers.nips.cc/paper/2021/hash/251bd0442dfcc53b5a761e050f8022b8-Abstract.html); [arXiv 2004.13912](https://arxiv.org/abs/2004.13912v2). No small-sample results were found in the abstracts.
- NODE-GAM (Chang, Caruana, Goldenberg, ICLR 2022 spotlight): neural GAM/GA²M "perform better than other GAMs on large datasets"; improves with self-supervised pre-training; `nodegam` on PyPI — [arXiv 2106.01613](https://arxiv.org/abs/2106.01613); [docs](https://nodegam.readthedocs.io)
- CANN (Wüthrich & Merz, "Yes, we CANN!", ASTIN Bulletin editorial 2019): the GLM's linear predictor enters the output via a skip connection, so the net learns only a correction; this is "model blending or ... neural net boosting of the actuarial model"; gradient descent is initialised at the GLM MLE with the network's output weights at zero, so training starts exactly at the GLM — [Cambridge editorial PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/66E8BEC373B5CCEF3BF3303D442D6B75/S0515036118000429a.pdf/editorial-yes-we-cann.pdf); [Wüthrich 2019 slides](https://www.zhaw.ch/storage/engineering/institute-zentren/iamp/upload/AI_conference_2019/Wuthrich_2019.pdf)
- CANN used for interaction detection: if the CANN deviance drops significantly below the GLM's, an interaction is deemed missing; benchmarked in insurance frequency/severity — [Holvoet et al., arXiv 2310.12671](https://arxiv.org/pdf/2310.12671) [preprint at time of the search result]
- GAMI-Net (Yang, Zhang, Sudjianto, Pattern Recognition 120:108192, 2021), LassoNet (Lemhadri, Ruan, Abraham, Tibshirani, JMLR 22(127), 2021), NAMLSS (Thielmann et al., AISTATS 2024) — the search did not return these; details recalled [unverified]

### Inferences
- [inference] Concrete hybrid: η_ij = x_ij'β (current GLMM) + g_θ(x_ij, z_i), g a 1-hidden-layer MLP (8–16 units) with output weights initialised at 0 and weight decay tuned in inner person-grouped folds; marginal likelihood by Gauss–Hermite over b. Because g ≡ 0 is the GLMM, (a) training starts at the GLMM, (b) the out-of-fold person log-likelihood difference is an interpretable "non-linearity gain", (c) heavy shrinkage simply returns the GLMM. This is the lowest-risk NN in this note.
- [inference] A NAM version (g = Σ_k g_k(x_k), one tiny net per geometry feature) keeps the effect of each feature plottable as a shape function, which matters for a thesis question about *which* geometry. A natural-spline cloglog GLMM (2–3 df per feature) is the statistical equivalent; at ~1,000 people it will almost certainly match the NAM, so the NAM should be justified only as a check, not as the primary model.
- [inference] LassoNet's hierarchy (a feature enters the hidden layer only if its linear term is active) is a principled way to keep the skip connection = GLM, but adds a path/tuning layer; not worth it with ~15 inputs.
- [inference] Main risk across all: the prespecified test is one LR test of the geometry block in a parametric model. A neural residual has no valid χ² reference, so it cannot replace the primary test; it can only be a secondary, estimated comparison (ΔC, Δlog-likelihood, calibration out of fold), in line with "ΔC and calibration are estimated, never tested".

### Gaps
- No NAM/CANN applied with a random intercept or cloglog link in medicine was found.
- No small-sample (n ≈ 1,000) evaluation of NAM/NODE-GAM vs spline GAM was found.

## 4. Small tabular data: TabPFN and the evidence that NNs rarely beat LR

### Takeaway
TabPFN v2 is the only "neural" option with evidence of strength on small tables, and TabPFN-2.5 nominally covers ~10k segment rows. But it is a row-wise i.i.d. classifier: it has no person random effect, no cloglog, no offset, and its per-segment probabilities cannot be aggregated correctly into a person risk. It is suited as a black-box benchmark at the person level, not as a replacement for the segment model.

### Cited Findings
- TabPFN v2 (Hollmann et al., Nature 637:319–326, 2025, doi:10.1038/s41586-024-08328-6) "outperforms all previous methods on datasets with up to 10,000 samples by a wide margin" — [Freiburg release](https://uni-freiburg.de/en/new-ai-model-tabpfn-enables-faster-and-more-accurate-predictions-on-small-tabular-data-sets/); the package docs say it is optimised for ≤ 10,000 rows — [PyPI](https://pypi.org/project/tabpfn/)
- Scope of TabPFN v2 described as ≤ 10,000 samples, 500 features, 10 classes — [arXiv 2502.17361](https://arxiv.org/pdf/2502.17361v1) [preprint]; a critical reanalysis vs specialised statistical methods exists — [arXiv 2505.20003](https://arxiv.org/abs/2505.20003v2) [preprint, findings not opened]
- TabPFN-2.5 (Prior Labs technical report, Nov 2025): up to 50,000 rows and 2,000 features; 18 transformer layers; reported to lead TabArena and match AutoGluon 1.4; weights research/non-commercial licence; "designed for datasets up to 50K samples" — [arXiv 2511.08667](https://arxiv.org/pdf/2511.08667) [technical report, not peer reviewed]; [docs](https://docs.priorlabs.ai/models/overview)
- Christodoulou et al. (J Clin Epidemiol 110:12–22, 2019): 71 studies, logit(AUC) difference ML vs LR 0.00 in low-risk-of-bias comparisons; Grinsztajn et al. (NeurIPS 2022 Datasets & Benchmarks): trees beat NNs on medium tabular data; van der Ploeg et al. (BMC Med Res Methodol 14:137, 2014): NNs needed > 100 events per variable for stable AUC vs 20–50 for LR — all as cited in [Neural networks for segment plaque.md](../../reports/Neural%20networks%20for%20segment%20plaque.md) ([Christodoulou](https://ora.ox.ac.uk/objects/uuid:4167c905-5171-4fc7-b157-ff36d56a73db); [Grinsztajn](https://arxiv.org/abs/2207.08815v1); [van der Ploeg](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289553))

### Inferences
- [inference] Segment rows: ~1,100 people × 9 = ~10,000 rows, inside TabPFN-2.5's range and at the edge of v2's. But TabPFN treats rows as exchangeable. Within-person correlation is ignored in training (fine for prediction if folds are person-grouped) and, critically, its segment probabilities are *marginal*; combining them as 1 − ∏(1 − p) is the naive product that overestimates person risk and can re-rank people (background report). Person risk from TabPFN must therefore come from a separate person-level fit (one row per person, ~1,100 rows, outcome "developed plaque"), which is exactly the person-level model the CLAUDE.md says is not the decision model.
- [inference] Useful role: a person-level TabPFN with SCORE2 factors + aggregated geometry as a "how much non-linearity is the pooled GLMM leaving on the table" benchmark. If TabPFN does not beat the pooled GLMM's out-of-fold person C/calibration, no tuned NN realistically will.
- [inference] Events-per-variable: with "a few hundred" people developing plaque and ~15 inputs, EPV ≈ 15–30, below van der Ploeg's > 100 for NNs. A segment-level NN has more segment events but its information about person-level inputs (SCORE2, LM angle, diameter ratios) is bounded by the number of people, not segments.

### Gaps
- No evaluation of TabPFN on grouped/clustered data or with a link/offset was found.
- Findings of the critical TabPFN reanalysis (2505.20003) were not opened.

## 5. Coronary/CCTA ML for plaque progression or incident plaque

### Takeaway
No coronary study found used a neural network to predict incident or progressing plaque per segment; ML models are boosted trees or random forests on hand-crafted features, and the largest well-designed comparison found no significant gain over logistic regression.

### Cited Findings
- PARADIGM (Han et al. 2020, 1,083 patients): ML model for rapid plaque progression AUC 0.83 vs logistic regression 0.81, P = 0.128 — [PMC7335586](https://pmc.ncbi.nlm.nih.gov/articles/PMC7335586); [Emory record](https://open.library.emory.edu/concern/publications/bb2318c5-d880-476f-8c71-8fc18b8021f5?locale=en)
- Serial CT + computational modelling in 32 patients: gradient-boosted trees AUC 0.76 for plaque area increase, reported to beat logistic regression (very small n) — [University of Galway](https://research.universityofgalway.ie/en/publications/prediction-of-atherosclerotic-disease-progression-combining-compu/)
- MACE (not plaque) in 361 patients: RUSBoost AUC 0.96 vs LR 0.92 (p = 0.024), authors note external validation needed — [Eur Radiol 2020](https://link.springer.com/article/10.1007/s00330-020-07083-2)
- Segment-level incident plaque in PARADIGM (Lee et al. 2024): 9,583 plaque-free segments, 9.8% developed plaque, test C 0.767 with clinical + radiomic features, clinical alone 0.696; Su et al. 2026 random forest 0.875 in 664 non-obstructive patients — as cited in [Neural networks for segment plaque.md](../../reports/Neural%20networks%20for%20segment%20plaque.md) ([Lee 2024](https://pubmed.ncbi.nlm.nih.gov/38378314/); [Su 2026](https://pubmed.ncbi.nlm.nih.gov/41349607/))

### Inferences
- [inference] All precedents are referral/selected, mostly Asian, 2–5-year intervals; none is a plaque-free general-population 10-year cohort. Small-n ML "wins" (32 or 361 patients) are the biased-validation pattern Christodoulou describes.

### Gaps
- No 2025–2026 deep-learning coronary plaque-progression paper with a regression comparator was found in these searches (PubMed/MICCAI not exhaustively searched).

## 6. Per-model design: random effect, regularisation, minimum data, implementation, risks

### Takeaway
Ranked by realism at n ≈ 1,100 people / few hundred events: (A) cloglog GLMM + neural residual (CANN-style) with integrated intercept; (B) cloglog NAM-GLMM; (C) person-level TabPFN benchmark; (D) mixed-effects NN packages (LMMNN/GLMMNet/MC-GMENN); (E) GNN/attention over segments. Only A and B nest the current model; expected gain over the GLMM is small to nil, and the honest framing is a prespecified secondary check of non-linearity, not a replacement.

### Cited Findings
- CANN initialisation at the GLM MLE with zero output weights — [Wüthrich 2019 slides](https://www.zhaw.ch/storage/engineering/institute-zentren/iamp/upload/AI_conference_2019/Wuthrich_2019.pdf)
- Code: LMMNN [gsimchoni/lmmnn](https://github.com/gsimchoni/lmmnn/issues/14); GLMMNet agi-lab/glmmnet ([arXiv 2301.12710](https://arxiv.org/pdf/2301.12710)); ARMED ([gitfront](https://gitfront.io/r/DeepLearningForPrecisionHealthLab/54f18307815dfb2148fbc2d14368c1268b63825e/ARMED-MixedEffectsDL)); DeepGLMM VBayesLab ([arXiv 1805.10157](https://arxiv.org/pdf/1805.10157)); nodegam ([docs](https://nodegam.readthedocs.io)); tabpfn ([PyPI](https://pypi.org/project/tabpfn/))

### Inferences (design table, all [inference])

| Model | Random effect | Regularisation | Min. data (rough) | Implementation | Main risks |
|---|---|---|---|---|---|
| A. GLMM + neural residual, cloglog, GH-integrated b | Exact: same N(0,σ²) intercept, 20–40 GH nodes in loss; prediction integrates b | Zero-init output, weight decay + early stopping tuned in inner person-grouped folds, 1 layer × 8–16 units, 5–10 seed ensemble | Works at any n because it shrinks to the GLMM; gain needs non-linearity strong enough to show at a few hundred events | ~150 lines PyTorch (`numpy.polynomial.hermite.hermgauss` nodes) | Overfitting via person-level inputs; no valid LR test; σ can collapse to 0 (log σ bound trap noted in background report); interaction with dominance × vessel base |
| B. NAM-GLMM (per-feature subnets, cloglog, b integrated) | As A | Per-subnet weight decay/smoothness; few units; ensemble | As A; each shape function needs ~100s of events to be stable | PyTorch, or `nam`/`nodegam` adapted with custom loss | Wiggly, unstable shape functions; a spline GLMM likely equal and simpler |
| C. Person-level TabPFN v2/2.5 | None (one row per person) | None to tune (in-context) | ~1,100 rows: in range | `tabpfn` package; GPU helpful | Not the decision model; no segment outcomes used; black box; licence for 2.5 |
| D. LMMNN / GLMMNet / MC-GMENN | Learned, but prediction for new person often u = 0 (median risk) unless re-implemented | Package defaults tuned for large n | Designed for 10⁴–10⁶ rows, high-cardinality clusters | TF/Keras (LMMNN, ARMED), PyTorch/Pyro-style VI (GLMMNet), MCMC (MC-GMENN) | Binary is proof-of-concept (LMMNN); no cloglog; wrong person aggregation; heavy engineering for no expected gain |
| E. GNN / attention over 9 segments + cloglog aggregation | Integrate b at output as in A | 2 layers × ~16–32 units, dropout, ensemble | Earlier report: needs pretraining/thousands of trees for learned structure | PyTorch Geometric | 9 fixed nodes add little beyond explicit neighbour features; information is "where", not "who" |

- [inference] Expected performance: the pooled GLMM is already a correctly structured likelihood with ~15–25 parameters. Given Christodoulou (0.00 logit-AUC difference under low bias), van der Ploeg (NN EPV > 100) and PARADIGM (0.83 vs 0.81, ns), the realistic out-of-fold person-level ΔC of A/B over the GLMM is around 0 with a person-bootstrap CI spanning ± 0.02–0.03; a significant improvement would be surprising and should prompt a leakage check first.
- [inference] Where NN-style flexibility could matter most is in non-linear SCORE2 terms (age) and geometry thresholds; both can be tested inside the GLMM with natural splines at 2–3 df, which keeps the LR test valid. This is the statistically preferable route; the NN is the robustness check.
- [inference] Every comparison must use identical person-grouped outer folds, the same base inputs, inner-fold tuning only, and evaluate the integrated person risk (C, calibration intercept/slope, Brier), plus calibration stratified by number of evaluable segments, since C cannot detect aggregation errors (background report).

### Gaps
- No published study runs any of A–E on clustered binary segment data at this scale, so all sample-size statements above are extrapolations, not citations.
- GAMI-Net, LassoNet, NAMLSS, MeNets citations need verification before use.
