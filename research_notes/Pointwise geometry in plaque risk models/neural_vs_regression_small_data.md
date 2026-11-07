# Neural networks on point-wise coronary geometry vs regression on engineered summaries (small cohort)

Context: CGPS (Herlev–Østerbro), plaque-free baseline CCTA, incident coronary plaque about 10 years later, roughly 1,000–1,200 people and about 450 events. Current model: segment-level cloglog GLMM over 9 trunk segments with a person random intercept, pooled to a person risk. It has one prespecified LR test of the geometry block, ΔC and calibration are estimated and not tested, CV is split by person, and the base is the SCORE2 factors.

Search budget: about 16 tool calls. Most findings come from abstracts, PMC pages and search snippets, not full texts. Each item says which.

## 1. What do systematic comparisons say about ML/DL vs logistic regression in small/medium samples? How much data does a neural network need?

### Takeaway
Comparisons with low risk of bias find no discrimination gain for ML over logistic regression on clinical prediction. Simulations find that neural networks need far more events per variable than LR to become stable, and still show instability and optimism above 200 EPV. With about 450 events, a neural network on raw point sequences is very unlikely to beat a well-specified regression, and its estimates would be unstable.

### Cited Findings
- Christodoulou et al. 2019 (J Clin Epidemiol 110:12–22) reviewed 71 studies with binary outcomes. In 145 comparisons at low risk of bias, the logit(AUC) difference between LR and ML was 0.00. In 137 comparisons at high risk of bias, ML looked better (logit(AUC) +0.34). 48/71 (68%) studies had potentially biased validation, and 56/71 (79%) did not address calibration. — [Christodoulou 2019, ORA Oxford](https://ora.ox.ac.uk/objects/uuid:4167c905-5171-4fc7-b157-ff36d56a73db/files/m0c822b1760523fd587b9a6769e616049); [PDF](https://med.mahidol.ac.th/ceb/sites/default/files/public/pdf/Repository/1-s2.0-S0895435618310813-main.pdf)
- Van der Ploeg, Austin and Steyerberg 2014 (BMC Med Res Methodol 14:137) simulated on three clinical cohorts. LR reached a stable AUC at about 20–50 events per variable. SVM, neural nets and random forests "showed instability and a high optimism even with >200 events per variable" and "may need over 10 times as many events per variable". The authors conclude these methods should be used only when very large data sets are available. — [van der Ploeg 2014, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4289553)
- Riley et al. 2020 (BMJ 368) give sample-size criteria for developing regression prediction models (overfitting/shrinkage, optimism in R², precise intercept). — [Riley 2020 sample size, Utrecht repository](https://dspace.library.uu.nl/handle/1874/457642)
- Riley et al. 2023, "Clinical prediction models and the multiverse of madness" (BMC Medicine 21:502): one development sample is one of many possible universes. Small development datasets give divergent models and unstable individual predictions. The authors ask for instability plots from bootstrapping. Their example compares a lasso LR fitted on n = 40,830 with one fitted on a subsample of 500. — [Riley 2023, PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10729337/)
- Riley et al. 2025 (arXiv 2504.18730, **preprint, not peer reviewed**) propose a simulation-based sample-size framework for "any statistical or machine learning method". It gives assurance probabilities and instability and degradation metrics, and "the required sample size depends on the users' key estimands". The worked example uses LR variants and random forests. The abstract says nothing about deep learning and gives no numeric thresholds. — [arXiv 2504.18730](https://arxiv.org/abs/2504.18730v1)
- TRIPOD+AI (Collins et al., BMJ 2024;385:e078378) is a single 27-item reporting checklist for prediction models that use either regression or machine learning, and it replaces TRIPOD 2015. — [TRIPOD+AI, PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11025451/)
- Grinsztajn, Oyallon and Varoquaux (NeurIPS 2022) benchmarked 45 datasets of medium size (about 10K samples). Tree-based models stayed state of the art over deep learning on tabular data, and the authors partly attribute this to neural networks lacking robustness to uninformative features. — [arXiv 2207.08815](https://arxiv.org/abs/2207.08815)
- Kapoor and Narayanan 2023 (Patterns 4:100804) found leakage in at least 294 papers across 17 fields. In their civil-war case study, complex ML models "no longer perform substantively better than decades-old LR models" once leakage was corrected. — [Kapoor & Narayanan, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10499856)

### Inferences
- Rough budget: about 450 events gives at most about 9–22 well-behaved regression parameters at 20–50 EPV, and fewer if the base model must be fitted too. A 1D CNN, RNN or transformer over point sequences has thousands to millions of weights. By the van der Ploeg result it would need more than 10 times the events of LR to stabilise. This is an extrapolation: van der Ploeg used tabular predictors, not sequences.
- Neither study gives a published sample size at which neural networks reliably beat regression on clinical outcomes. Christodoulou's null result at low risk of bias is the closest thing to a general answer.
- The thesis's one prespecified LR test has a defined null and degrees of freedom. A neural model has no comparable test.

### Gaps
- I found no paper that gives the number of events at which a neural network on 1D sequences (as opposed to tabular data) overtakes LR for a clinical binary outcome.
- I did not retrieve the full text of Christodoulou 2019, so I cannot say how many of the comparisons were neural networks specifically.

## 2. Weak supervision: per-segment or per-person labels with point-sequence inputs. What do MIL and attention pooling offer, and how much data do they need?

### Takeaway
Attention-based MIL (Ilse et al. 2018) handles a bag-level label with instance-level inputs and gives attention weights that show which instances drive the label. It worked well with 50–500 bags only on a synthetic MNIST-bags task with strong, clean signals. No source gives a sample size for weak, noisy clinical signals like geometry-to-incident-plaque. The pooled cloglog GLMM already pools segment risks into a person risk, which is a parametric form of MIL.

### Cited Findings
- Ilse, Tomczak and Welling (ICML 2018, PMLR 80:2127–2136) model the bag label's Bernoulli distribution with a neural network and a permutation-invariant attention pooling operator. The attention weights show each instance's contribution. The method matched the best MIL methods on benchmarks and beat them on MNIST-bags and two histopathology datasets. — [PMLR](https://proceedings.mlr.press/v80/ilse18a.html); [arXiv 1802.04712](https://arxiv.org/abs/1802.04712)
- In Ilse et al.'s MNIST-bags experiments (50 to 500 training bags), attention MIL "performs much better than other methods in the small sample size regime", described as 50–150 bags with about 10 instances per bag. The positive instance there is a specific digit, a clean and deterministic signal. — [Ilse 2018 PDF](https://arxiv.org/pdf/1802.04712)
- Pathology MIL work (Campanella et al. 2018, terabyte-scale MIL) argued that earlier MIL studies "used small datasets which precludes a proper estimation of the clinical relevance of the models". — [arXiv 1805.06983 via arxiv-vanity](https://www.arxiv-vanity.com/papers/1805.06983/)
- One end-to-end MIL paper says it "can be hard to know in advance the percent of key instances in real data and, consequently, to estimate the sample size". — [arXiv 2203.03981](https://arxiv.org/pdf/2203.03981.pdf)

### Inferences
- Plaque onset is driven mostly by systemic risk. Geometry likely changes the hazard modestly, and the label is noisy: minimal plaque counts, and CCTA misses small lesions. That is very different from MNIST-bags, so the 50–150-bag result does not carry over.
- The present design already handles the weak-label problem: segment features → segment cloglog risk → pooled person risk, with segment intercepts and a person random intercept. Under a cloglog link, the pooled risk 1 − ∏(1 − p_s) is the noisy-OR form of the standard MIL assumption. Attention MIL would replace this fixed, interpretable pooling with a learned one, at a large cost in parameters.
- Attention weights are not significance tests and are known to be unstable. They could be shown as an exploratory map along the centerline, but they cannot replace the geometry hazard ratios.

### Gaps
- I found no MIL study on coronary centerlines or any vascular geometry with a clinical outcome.
- I did not retrieve the 2025 ML4H synthetic correlated-MIL scaling results.

## 3. Hybrid approaches: learned representation as a few covariates, deep survival/cloglog, regression with a neural offset. Can the prespecified LR test survive?

### Takeaway
A defensible hybrid compresses the point sequences without using the outcome: functional PCA, or an autoencoder or self-supervised encoder trained on unlabeled centerlines (including the plaque-at-baseline people or the Medis trees). The first few scores enter the cloglog GLMM as a prespecified covariate block. The LR test then remains valid with known df. Supervised representations, deep survival and neural-offset models break the standard LR test, unless the representation is learned on separate data or the test is done by sample splitting or permutation. Semi-structured regression (Rügamer et al.) keeps the regression coefficients identifiable, but it does not give a classical test of a neural block.

### Cited Findings
- Functional logistic regression: project each curve on a few orthonormal functional principal components, then fit a logistic model on the scores. This is standard (Escabias et al. 2004, and later), with software in R `refund::fpcr` and `logitFD`. — [Escabias et al., J Nonparametr Stat](https://informahealthcare.com/doi/full/10.1080/10485250310001624738); [refund fpcr](https://rdrr.io/cran/refund/man/fpcr.html); [logitFD manual](https://cran.r-universe.dev/logitFD/doc/manual.html)
- Plain FPCA ignores the response, so supervised FPCA variants exist for functional logistic regression. — [Nie et al., SFU](https://www.sfu.ca/science/stat/cao/Papers/SFPCA.pdf)
- A clinical example: an accelerometry mortality study fits logistic regression on selected FPC scores plus survey covariates. — [arXiv 2105.14649](https://arxiv.org/pdf/2105.14649)
- Semi-structured deep distributional regression (Rügamer, Kolb and Klein; The American Statistician 2024, 78(1):88–99) combines a structured regression predictor with a deep network. An orthogonalization cell projects the network into the orthogonal complement of the structured predictor, so the structured coefficients stay identifiable and interpretable. A later post-hoc orthogonalization (ICML 2023) reports better estimation. — [arXiv 2002.05777](https://arxiv.org/abs/2002.05777v4); [RePEc](https://econpapers.repec.org/RePEc:taf:amstat:v:78:y:2024:i:1:p:88-99); [mcml.ai PHO](https://mcml.ai/publications/rkk23/)
- In Lin et al. (Lancet Digital Health 2022), deep learning measured plaque volume on CCTA, and prognosis was then modelled with that one engineered summary in a regression (MI hazard ratio 5.36, 95% CI 1.70–16.86, 41 events in 1,611 SCOT-HEART patients). Deep learning served as a measurement tool, and the risk model stayed a regression. — [Lin 2022, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9047317)

### Inferences
- **Option A, recommended if any learned features are used:** fit FPCA, an autoencoder or a self-supervised encoder on curvature, taper and diameter profiles without the outcome (unlabeled people can be included). Prespecify k scores per artery (for example k = 2–3) and add them as a block to the cloglog GLMM. The representation does not depend on Y, so the LR test of the block has df = k (times arteries/segments), as for engineered features. This holds only if k and the encoder are fixed before the outcome is seen. That fits the memory note "freeze method before outcome".
- **Option B, supervised representation** (a network trained on the outcome, its output used as a covariate): the LR test is anti-conservative on the same data. It is valid only with sample splitting (learn on one part, test on the held-out part, which loses power) or a permutation test that retrains the network on every permutation (expensive). This must run inside person-split CV, or it leaks.
- **Option C, deep cloglog, deep survival or a neural offset:** the "geometry block" is a function, not a parameter vector. A likelihood ratio has no χ² reference distribution with known df, so the prespecified test would have to be replaced by a permutation or split test. Hazard ratios per unit of curvature or taper are lost. Orthogonalization keeps the SCORE2 coefficients interpretable, but not the geometry effect.
- For a thesis with one prespecified test, Option A keeps inference, interpretability and the pooled GLMM unchanged. It costs little and adds a "learned shape" block that can be compared with the engineered block (as a secondary analysis, ΔC estimated and not tested).

### Gaps
- I found no published coronary-geometry study that used an outcome-free learned representation as regression covariates with a formal block test. The design follows from general principles, not from a precedent.
- I did not verify whether Rügamer et al. provide any hypothesis test for the deep part.

## 4. Leakage, nested CV split by person, calibration and optimism for neural models in small data

### Takeaway
Leakage and weak validation are the main reason ML appears to beat LR in the literature. Neural models need nested, person-split CV that includes every data-dependent step (scaling, FPCA, encoder fitting if it is supervised, hyperparameters, early stopping). Calibration is the usual failure point and must be reported.

### Cited Findings
- In Christodoulou 2019, the ML advantage existed only in comparisons with high risk of bias, 68% of studies had potentially biased validation, and 79% ignored calibration. — [Christodoulou 2019](https://ora.ox.ac.uk/objects/uuid:4167c905-5171-4fc7-b157-ff36d56a73db/files/m0c822b1760523fd587b9a6769e616049)
- Kapoor and Narayanan 2023: leakage affects at least 294 papers in 17 fields, and correcting it removed the claimed ML advantage over LR in their case study. — [Patterns 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10499856)
- Van Calster et al. 2019 ("Calibration: the Achilles heel of predictive analytics", BMC Med 17:230): regression and flexible ML can both be poorly calibrated, overfitting is a common cause, and external calibration curves need large samples. — [Van Calster 2019, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6912996)
- Varoquaux and Cheplygina 2022 (npj Digit Med 5:48) warn that test data must reflect the target population rather than be a random subset of the same pool, and that benchmark winners can fail in practice. — [Varoquaux & Cheplygina, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9005663)
- Roberts et al. 2021 (Nat Mach Intell 3:199–217) screened 2,212 studies, quality-checked 415 and included 62 on COVID-19 imaging ML. None were of potential clinical use, because of methodological flaws and biases, including confounded data sources (for example, children as controls). — [Cambridge news](https://www.cam.ac.uk/research/news/machine-learning-models-for-diagnosing-covid-19-are-not-yet-suitable-for-clinical-use); [Dundee repository](https://discovery.dundee.ac.uk/en/publications/common-pitfalls-and-recommendations-for-using-machine-learning-to/)
- Riley 2023: report individual-level prediction instability (bootstrap instability plots), which grows as the sample shrinks. — [Riley 2023](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10729337/)

### Inferences
- Leakage routes specific to this design: (a) points or segments of one person in both train and test, which the person split already prevents; (b) baseline and follow-up scans of the same person, or Medis/plaque-at-baseline people, used to pretrain an encoder whose outputs are then evaluated on the same people. This is harmless if pretraining uses no outcome, but must be stated. (c) Tuning hyperparameters or early stopping on the outer test fold. (d) Normalising sequences, such as resampling length or standardising curvature, with statistics from all people. This is minor if done without the outcome, but should be inside folds when supervised.
- With about 450 events and 5–10 outer folds, each test fold has about 45–90 events. AUC/C and calibration slopes will be noisy, and fold-to-fold variation can hide differences of the size expected from geometry (likely ΔC of a few hundredths). This hits any model, but neural models add variation from random seeds and initialisation, so repeated CV and seed averaging would be needed.
- Calibration: neural nets trained with cross-entropy and early stopping on small data tend to be miscalibrated, and recalibration needs yet another held-out layer. The GLMM's calibration can be checked directly with the existing slope and intercept framework.

### Gaps
- I did not find a small-sample (<2,000) cardiovascular study with a direct nested-CV comparison of a neural sequence model and LR, with calibration reported.

## 5. Neural networks on small cardiovascular imaging cohorts (<2,000) for prognosis, and their external validation

### Takeaway
I found no deep-learning model on coronary centerline geometry that predicts incident plaque. Reviews of AI cardiovascular risk models report high risk of bias and almost no independent external validation. Successful CCTA deep-learning work mostly uses deep learning to measure (segmentation, plaque volume) and keeps prognosis in a regression on the measured summary.

### Cited Findings
- A systematic review in BMC Medicine 2024 of 486 AI cardiovascular risk prediction models: 380 were in development, none had independent external validation, and all were at high PROBAST risk of bias, "primarily due to the incorrect use of statistical methods". Sample sizes ranged from 80 to 3,660,000 (median 4,466). — [BMC Med 2024, PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10845808/)
- Lin et al. 2022 (Lancet Digital Health): a deep-learning CCTA plaque-quantification system was externally validated against experts (ICC 0.964 for total plaque volume, external cohort of 175 patients and 1,081 lesions). The prognostic part used a DL-measured plaque-volume cutoff in a regression in 1,611 SCOT-HEART patients with only 41 MIs (HR 5.36, 95% CI 1.70–16.86, which is wide). — [Lin 2022, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9047317)
- Patents (for example US 9,805,463 / 9,679,374 / 11,663,715) claim prediction of lesion location and onset from centerline features (lumen area, curvature) with SVM, MLP or regression. They are patents, not validated results. — [USPTO 11663715](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11663715)
- A review of DL in coronary anatomy imaging (Alskaf et al.) found most applications had not been externally validated. A review of thoracic imaging for cardiovascular diagnosis reported a median AUC drop of 0.045 on external validation (range −0.130 to +0.033, 6 studies). **The second source (geneticsmr.com) is of uncertain quality and could not be verified. Do not cite it in the thesis.** — [geneticsmr.com (unverified)](https://geneticsmr.com/index.php/gmr/article/view/4907); [Alskaf et al., PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7614252)
- Centerline deep learning for FFR was trained on 110 patients and 112 arteries. It estimates functional severity, not future plaque. — [ar5iv 2310.11297](https://ar5iv.labs.arxiv.org/html/2310.11297)

### Inferences
- The pattern that works in CCTA is deep learning as an instrument and regression as the risk model. That is the thesis's present structure: the in-house tracer produces centerlines and lumen, and engineered geometry enters a cloglog GLMM.
- There is no external validation cohort for CGPS incident plaque. Any neural model would rest on internal CV alone, which the reviews above identify as the weakest evidence tier.

### Gaps
- I found no peer-reviewed deep-learning prognosis study on <2,000 people in cardiovascular imaging that reports paired internal and external performance. A targeted search (for example ECG-AI or echo-AI external validation cohorts) would be needed.
- I could not verify the Alskaf et al. bibliographic details (the PMC link came from the search listing, not a full-text check).

## Overall assessment (inference, for the report writer)
- **Feasibility:** technically possible. Statistically, it is not a sensible primary analysis with about 450 events. The evidence (Christodoulou 2019, van der Ploeg 2014, Riley 2023) predicts no discrimination gain, worse stability and worse calibration. It would also give up the one prespecified LR test, which is a decided design element.
- **Expected benefit:** small to none for prediction. Learned representations could find shape information that the engineered features miss, but any such signal is diluted by systemic risk, and fold-level C with about 45–90 events per fold cannot resolve small ΔC.
- **Sensible hybrid:** outcome-free functional PCA or an autoencoder on the per-artery curvature, taper and diameter profiles, frozen before the outcome is seen, with k prespecified scores as a secondary covariate block in the same pooled cloglog GLMM. This keeps the LR test valid (df known), stays inside person-split CV, and keeps hazard-ratio interpretation per score, though the scores are less intuitive than curvature or taper.
- **Avoid as primary:** attention MIL, sequence transformers, deep cloglog or survival models, and neural offsets. If any of them is run, label it exploratory, nest every tuning step inside person-split CV, average over seeds, report calibration and instability (Riley 2023), and follow TRIPOD+AI.
