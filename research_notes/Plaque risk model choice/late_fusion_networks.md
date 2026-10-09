# Late-fusion neural networks (curvature profile + risk factors) vs XGBoost on summary features, for new-plaque prediction in Herlev–Østerbro

Scope note: ~22 tool calls. Several full texts (PMC, nature.com) were blocked by captcha/redirects, so some numbers come from abstracts or search-result summaries; these are flagged. Items marked "[not verified this session]" are from background knowledge and must be checked before thesis use.

## 1. Fusion taxonomy and evidence for multimodal gains

### Takeaway
The standard taxonomy (early / joint-intermediate / late) is well established; reviews report that multimodal models usually beat single-modality ones, but the evidence base is thin (few studies run proper unimodal baselines), the average gain is modest (~6% accuracy), and none of the reviews establish a sample size at which deep fusion starts paying off. Early fusion, not deep joint fusion, is the most common strategy in practice.

### Cited Findings
- Huang, Pareek, Seyyedi, Banerjee, Lungren (npj Digit Med, Oct 2020): systematic review of imaging + EHR fusion with deep learning, literature 2012–2020; 985 studies screened, data extracted from 17 papers; defines early, joint and late fusion and gives implementation guidelines. — [Huang 2020, PMC7567861](https://pmc.ncbi.nlm.nih.gov/articles/PMC7567861/)
  - [not verified this session, full text blocked] Definitions as usually cited from this paper: early fusion = concatenating input features (type I: raw/original features; type II: extracted features) before one model; joint (intermediate) fusion = learned feature representations from a neural branch are concatenated with other modality and the loss is propagated back into the feature extractor; late fusion = separate models per modality whose predictions are aggregated (averaging, voting, or a meta-model).
- Kline et al. (npj Digit Med, 2022), PRISMA-ScR scoping review of multimodal ML in health, 2011–2021, 128 articles: early fusion was the most common strategy; few papers compared multimodal against a unimodal baseline, but those that did reported an average increase of 6.4% in predictive accuracy. — [Kline 2022, PMC9640667](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9640667/); [PubMed 36344814](https://pubmed.ncbi.nlm.nih.gov/36344814/)
- Mohsen, Ali, El Hajj, Shah (Sci Rep, 2022), scoping review of AI fusion of EHR + imaging, 34 studies: early fusion used in 22/34; multimodal models outperformed single-modality models for the same task; conventional ML was more common (19 studies) than DL (16). — [Mohsen 2022, PMC9605975](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9605975/); [arXiv 2210.13462](https://arxiv.org/pdf/2210.13462)
- Stahlschmidt, Ulfenborg, Synnergren (Brief Bioinform, Jan 2022): proposes a more detailed taxonomy of fusion (early, intermediate with sub-types, late) for biomedical data and concludes that deep (intermediate) fusion strategies often outperform unimodal and shallow approaches. — [Stahlschmidt 2022 (search summary, PMC8921642)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8921642)
- A 2024 systematic review focused specifically on intermediate fusion in biomedical multimodal DL exists (arXiv 2408.02686), useful for the "joint fusion" end of the taxonomy. — [arXiv 2408.02686](https://arxiv.org/html/2408.02686v1)

### Inferences
- "Multimodal beats unimodal" in these reviews is mostly driven by studies with large imaging inputs (MRI, CT, histology) and often thousands of patients; it does not transfer to a 10–40 point curvature signal with tens–low hundreds of events. Also, the reviews compare multimodal vs unimodal, not "deep fusion" vs "handcrafted summary + tabular", which is the comparison this thesis actually needs.
- Publication bias and weak baselines (Kline: few unimodal comparisons) mean the 6.4% average gain is an upper-bound style number.
- In the taxonomy, the thesis plan (CNN on profile -> scalar score, then logistic layer with risk factors) is late fusion if the CNN is trained separately and frozen, and joint/intermediate fusion if trained end to end with the logistic head.

### Gaps
- None of the four reviews gives a quantitative sample-size threshold below which fusion networks stop helping. Could not extract per-study sample sizes from Huang 2020 (full text blocked).

## 2. Small-sample deep learning on tabular + signal data: failure modes and mitigations

### Takeaway
On tabular data, tree ensembles beat deep nets up to ~10k samples (Grinsztajn 2022); for clinical prediction, flexible methods (NN, RF, SVM) need far more events per parameter than logistic regression, and systematic reviews find no average benefit of ML over LR. With tens to low hundreds of events per domain, a CNN branch is at high risk of overfitting and seed instability; the defensible framing is exploratory, with heavy constraint (tiny model, weight sharing, repeated CV, ensembling).

### Cited Findings
- Grinsztajn, Oyallon, Varoquaux (NeurIPS 2022 Datasets & Benchmarks): 45 tabular datasets; tree-based models (XGBoost, RF) remain state of the art on medium-sized data (~10K samples) even ignoring speed. NNs struggle because they are (1) not robust to uninformative features, (2) rotationally invariant (do not preserve feature orientation), (3) biased to smooth functions and struggle with irregular targets. — [Grinsztajn 2022, arXiv 2207.08815](https://arxiv.org/abs/2207.08815v1); [NeurIPS page](https://neurips.cc/virtual/2022/poster/55627)
- Christodoulou et al. (J Clin Epidemiol 2019): systematic review of 71 studies comparing ML vs logistic regression for clinical prediction: no performance benefit of ML over LR; median sample size 1,250 (range 72–3,994,872), median 19 predictors, median 8 events per predictor; 48/71 (68%) had potential validation bias. — [Christodoulou 2019 (PDF)](https://med.mahidol.ac.th/ceb/sites/default/files/public/pdf/Repository/1-s2.0-S0895435618310813-main.pdf)
- van der Ploeg, Austin, Steyerberg (BMC Med Res Methodol 2014), simulation of data hungriness for dichotomous endpoints (SVM, NN, RF vs LR, CART), defined by AUC plateau and optimism < 0.01. — [van der Ploeg 2014, PMC4289553](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4289553/)
  - [not verified this session, full text and abstract fetch blocked] Commonly cited conclusion: modern techniques (SVM, NN, RF) may need over 10 times as many events per variable as LR to reach stable AUC/small optimism; LR roughly 20–50 EPV, NN/RF/SVM over 200 EPV.
- Riley et al. (BMJ 2020): sample size for clinical prediction models should be set by three criteria: global shrinkage factor ≥ 0.9, absolute difference ≤ 0.05 between apparent and adjusted Nagelkerke R², and precise estimate of overall risk; implemented in R `pmsampsize`. Replaces the 10 EPV rule of thumb. — [Riley 2020 BMJ, Oxford repository](https://ora.ox.ac.uk/objects/uuid:743761e7-58a5-4968-9195-2b266abe6ad3); [pmsampsize docs](https://rdrr.io/pkg/pmsampsize/man/pmsampsize.html)
- An empirical study (JMIR 2024) of sample size requirements for popular classifiers on tabular clinical data exists and is relevant for justifying n per algorithm. — [JMIR 2024, PMC11688588](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11688588/)
- Ismail Fawaz et al. (Data Min Knowl Discov 2019), review of deep learning for time series classification: 8,730 models trained on 97 datasets (UCR + 12 multivariate); ResNet best on average (won 34/85), and the authors note deep architectures generally need large amounts of data to generalise. — [arXiv 1809.04356](https://arxiv.org/abs/1809.04356v1)
- "Does deep learning really outperform non-deep ML for clinical prediction on physiological time series?" (arXiv 2022) systematically questions DL superiority on clinical time series. — [arXiv 2211.06034](https://arxiv.org/pdf/2211.06034)
- TabPFN v2 (Hollmann et al., Nature 2025): a pretrained tabular transformer reported to outperform previous methods (including tuned gradient boosting) on datasets up to 10,000 samples; relevant as a small-n tabular baseline that is "deep" but not trained from scratch. — [Univ. Freiburg release](https://uni-freiburg.de/en/new-ai-model-tabpfn-enables-faster-and-more-accurate-predictions-on-small-tabular-data-sets/); critical reappraisal: [arXiv 2505.20003](https://arxiv.org/pdf/2505.20003)

### Inferences
- With ~5–10 risk factors plus ~5 scalar geometry features, a logistic or XGBoost model is already near the event budget for some domains (LM events will be very few). Even a minimal 1D CNN (e.g. two conv layers of 4–8 channels, global pooling, one output) has hundreds of weights; it cannot be justified by EPV logic, only by heavy regularisation and honest out-of-sample evaluation.
- Mitigations that are defensible here (mostly general-ML practice, not sourced to a specific trial in this session):
  - Tiny architecture with global pooling (length-invariant, handles 10–40 points).
  - Weight sharing across LAD/LCx/RCA (one profile encoder, artery as an input indicator), multiplying training examples per parameter about 3x; consider a per-participant clustered split so the same person never appears in train and test.
  - Augmentation consistent with physics: reversal is not valid (proximal-distal matters), but small jitter of chord start position, curvature noise at segmentation-error scale, and random cropping of the distal tail are plausible.
  - Self-supervised or auxiliary pretraining of the profile encoder on ImageCAS centerlines (e.g. predict masked curvature, or contrastive across left/right) gives an encoder whose weights are not fitted on the outcome. This is the strongest argument for including a network at all.
  - Repeated stratified CV (e.g. 5x5 or 10x10) with the full pipeline inside each fold, reporting spread over seeds; deep ensembles over seeds to reduce variance; calibration checked (slope, intercept), since NNs are often miscalibrated.
- TabPFN is a reasonable additional baseline for the tabular-only arm, but its handling of a variable-length signal requires summary features anyway.

### Gaps
- No source found that quantifies seed instability (variance of AUC across seeds) for small CNNs on clinical signals at n of a few hundred. No coronary-specific source on augmentation of curvature profiles.

## 3. Using the profile without a deep net: fPCA, summary stats, ROCKET/MiniRocket, tsfresh

### Takeaway
For short univariate series and small n, random-convolution transforms (ROCKET/MiniRocket) + ridge/logistic regression match deep TSC models on the UCR archive at a fraction of the cost and with only a linear model fitted to the outcome, making them the natural "CNN-like but non-deep" comparator. Functional PCA and handcrafted summaries are the most interpretable options.

### Cited Findings
- MiniRocket (Dempster, Schmidt, Webb; KDD 2021): evaluated on 30 resamples of 109 UCR datasets; essentially the same accuracy as ROCKET, up to 75x faster, almost deterministic; trains and tests on all 109 datasets in under 10 minutes; significantly more accurate than any method of similar computational expense; compared against HIVE-COTE/TDE, TS-CHIEF, InceptionTime, ROCKET, TDE, CIF, cBOSS, Proximity Forest. — [MiniRocket arXiv 2012.08791](https://arxiv.org/pdf/2012.08791)
- ROCKET/MiniRocket are somewhat less accurate than HIVE-COTE variants (HIVE-COTE 2.0 is top-ranked on 112 UCR datasets) but far cheaper. — [MultiRocket, arXiv 2102.00457](https://arxiv.org/pdf/2102.00457v2)
- [not verified this session] ROCKET (Dempster, Petitjean, Webb; Data Min Knowl Discov 2020): 10,000 random convolutional kernels, PPV and max pooling features, ridge classifier; accuracy on the UCR archive comparable to InceptionTime/HIVE-COTE at much lower cost.
- Deep TSC models (ResNet, InceptionTime) do well on UCR on average, but the authors note they need large training sets. — [Ismail Fawaz 2019, arXiv 1809.04356](https://arxiv.org/abs/1809.04356v1)

### Inferences
- MiniRocket produces ~10k features; with a few hundred participants these must go into a strongly penalised model (ridge/L2-logistic with CV-tuned penalty), and then the resulting profile score can be fused with risk factors exactly as a CNN score would be. This gives a "learned profile score" with only one tuned hyperparameter, so it is a better-matched control for the CNN than XGBoost-on-summaries alone.
- Functional PCA on arc-length-registered profiles (padding/truncating to a common length, or registering by fraction of artery length) gives 2–5 scores per artery, which slot directly into logistic regression or XGBoost and are interpretable as modes of shape variation.
- Handcrafted summaries (mean, max, integral of curvature, number of bends above threshold, location of maximum) plus tsfresh-style features fed to XGBoost is the "summary" arm. tsfresh generates hundreds of features with built-in hypothesis-test filtering, which is risky at small n (selection must be inside CV).
- UCR datasets are mostly classification of shape class with clean labels and balanced classes; a weak, noisy prognostic signal with rare events is a harder regime, so UCR rankings are only indicative.

### Gaps
- Found no head-to-head of fPCA vs CNN vs ROCKET on short biomedical profiles with n of a few hundred and a prognostic (not diagnostic) label.

## 4. Precedent: deep learning on coronary centerlines, geometry or CCTA profiles

### Takeaway
Deep models along the centerline exist for diagnosis (plaque/stenosis detection) with ~100–500 patients, but prognostic ML for plaque progression in CCTA (PARADIGM) has used tabular plaque features with gradient boosting, not deep nets on geometry. No study was found that uses a deep net on a curvature profile to predict new plaque in plaque-free arteries; that is a gap and also a warning that there is no precedent for the sample size needed.

### Cited Findings
- Zreik et al. (IEEE TMI 2019; 38(7):1588–1598): recurrent CNN on multiplanar reformatted images along extracted coronary centerlines (3D CNN features per position, aggregated by RNN), multi-task for plaque type and stenosis; trained on 98 and tested on 65 patients; accuracy 0.77 for plaque detection/characterisation and 0.80 for stenosis detection/significance. — [Zreik 2019, arXiv 1804.04360](https://ar5iv.arxiv.org/html/1804.04360)
- Candemir et al. (Radiol Artif Intell 2020): 3D CNN for automated atherosclerosis detection and weakly supervised localisation on CCTA. — [arXiv 1911.13219](https://arxiv.org/pdf/1911.13219). Follow-up from the same group (White et al. 2020): vessel-centerline-based classification; development n = 500 (50% prevalence), simulated clinical test n = 100 (28% prevalence); AUC 0.96 for excluding atherosclerosis. — [arXiv 2008.04802](https://arxiv.org/abs/2008.04802v1)
- Han et al. (JAHA, Mar 2020), PARADIGM registry: 1,083 patients with serial CCTA, 224 (21%) with rapid plaque progression (annual PAV increase ≥ 1.0%); ML (boosting) model 1 clinical only AUC 0.62, model 2 + qualitative plaque AUC 0.73, model 3 + quantitative plaque AUC 0.83 (0.78–0.89); ASCVD risk score 0.60, Duke CAD score 0.74. — [Han 2020 JAHA, DOAJ](https://doaj.org/article/636830fb82c14cdaaff903a3ea5e9d51); [Emory repository](https://open.library.emory.edu/concern/publications/bb2318c5-d880-476f-8c71-8fc18b8021f5)
- García-García, Bulant, Boroni et al. (EuroIntervention 2026; 22(9)): biLSTM + two fully connected layers on sequential IVUS frames to classify plaque progression vs regression; derivation 1,960 ROIs (IBIS-4), external test 5,283 ROIs (PACMAN-AMI); test accuracy 0.84, MCC 0.68, F1 0.84. Note: IVUS, existing plaque, ROI-level n. — [EuroIntervention 2026](https://eurointervention.pcronline.com/article/derivation-and-external-validation-of-a-deep-learning-model-to-predict-changes-in-coronary-plaque-burden)
- Systematic review (2025) of DL-enabled CCTA for plaque/stenosis quantification and cardiac risk prediction summarises the field; DL is mostly used for segmentation/quantification, with downstream risk models. — [PMC12123344](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12123344/)
- Geometric studies (non-DL): centerline curvature (Frenet) higher in segments with stenosis (16.7%) and arteries with stenosis (13.8%), and associated with plaque presence per segment and per artery. — [Frontiers in Physiology 2023 (search summary)](https://www.frontiersin.org/articles/10.3389/fphys.2023.1162436) [summary attribution uncertain: the Frontiers article itself is an ANN for mechanical properties trained on FE simulations; the curvature numbers appeared in the same search result and should be traced to their primary geometry paper before citing.]

### Inferences
- The most relevant prognostic precedent (PARADIGM, n = 1,083, 224 events, patient level) used tabular features and gradient boosting, and the largest gain came from quantitative plaque features, which by design do not exist in a plaque-free baseline cohort. Expect a smaller added value from geometry than plaque features gave in PARADIGM.
- Diagnostic centerline DL (Zreik, Candemir) works with ~100–500 patients because the label is local and visible in the image (many positive positions per patient). Prognostic labels (new plaque years later) carry far less signal per sample, so these sample sizes do not transfer.
- Patent families (HeartFlow, "predicting location, onset and/or change of coronary lesions") claim ML on geometry for lesion onset but are not peer-reviewed evidence. — [US patent 9,805,463](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9805463)

### Gaps
- Did not find peer-reviewed DL on coronary curvature profiles, PointNet, or GNN on coronary trees for plaque onset/progression with reported sample sizes in this session. CT-FFR geometry networks (e.g. Itu 2016 J Appl Physiol, trained on synthetic trees) were not checked. Lin/Dey "plaque progression ML" beyond Han 2020 was not separately retrieved.

## 5. Showing the profile adds information beyond its summary

### Takeaway
The cleanest test is nested model comparison under identical resampling: (risk factors) vs (risk factors + summary features) vs (risk factors + summary + profile score), with the profile score learned out-of-fold. Paired differences in out-of-sample log-loss/AUC across repeated CV, and refitting without a feature family, are preferable to permutation importance when features are correlated.

### Cited Findings
- The Grinsztajn benchmark shows NNs are hurt by uninformative features, so adding a weak profile branch can lower performance even if the profile carries some signal; a non-improvement is not proof of no information. — [Grinsztajn 2022](https://arxiv.org/abs/2207.08815v1)
- Han 2020 is a template for nested model comparison (clinical, + qualitative, + quantitative) with AUCs reported per stage. — [Han 2020 JAHA](https://doaj.org/article/636830fb82c14cdaaff903a3ea5e9d51)
- [not verified this session] Permutation importance breaks correlation structure and extrapolates into implausible regions when features are correlated (Hooker, Mentch, Zhou, "Unrestricted permutation forces extrapolation", Stat Comput 2021); refit-without-feature (drop-column / leave-one-covariate-out) and conditional importance are recommended alternatives.

### Inferences
- Recommended ablation ladder, all with the same folds and seeds:
  1. LR(risk factors).
  2. LR or XGBoost (risk factors + scalar geometry + curvature summaries).
  3. Same + fPCA scores.
  4. Same + MiniRocket-ridge profile score (out-of-fold).
  5. Same + CNN profile score (out-of-fold), and a control CNN fed only the summaries (or a shuffled-order profile) to separate "the profile's order matters" from "the CNN is just a different learner".
- Report differences as paired deltas over repeats with intervals; also report calibration and decision-curve net benefit, since AUC deltas at this n will have wide intervals.
- Because curvature summaries and the profile are strongly correlated by construction, attribute value by refit-without-family rather than by SHAP/permutation of individual summaries.

### Gaps
- No source retrieved on formal tests for incremental value in repeated CV (e.g. corrected resampled t-test, Nadeau and Bengio 2003); worth adding.

## 6. Is late fusion equivalent to "learned feature + logistic regression"? Two-stage design

### Takeaway
Yes, structurally: a late-fusion model whose profile branch outputs one scalar that enters a logistic layer alongside risk factors is a logistic regression with one learned covariate. Training the branch separately (two-stage, out-of-fold stacking) keeps the final model interpretable, makes the effective parameter count in the outcome model small, and lets any profile encoder (fPCA, MiniRocket, CNN) be swapped in under the same evaluation.

### Cited Findings
- Taxonomy: late fusion aggregates per-modality model outputs; joint fusion backpropagates the final loss into the feature extractor. — [Huang 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7567861/); [Stahlschmidt 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8921642)
- Christodoulou 2019 found no average gain of ML over LR in clinical prediction, supporting LR as the final layer. — [Christodoulou 2019](https://med.mahidol.ac.th/ceb/sites/default/files/public/pdf/Repository/1-s2.0-S0895435618310813-main.pdf)
- Riley 2020 sample-size criteria apply directly to the final logistic stage if the profile score counts as one parameter, but only if the score was produced out-of-sample; otherwise its parameters count too. — [Riley 2020](https://ora.ox.ac.uk/objects/uuid:743761e7-58a5-4968-9195-2b266abe6ad3)

### Inferences
- End-to-end (joint) training lets the CNN absorb information already in risk factors (e.g. age-related tortuosity), which makes the profile coefficient hard to interpret; two-stage training with the CNN trained on outcome residual or with risk factors as fixed offset is a cleaner design if the question is "does geometry add to risk factors".
- If the profile encoder is trained on the outcome, the score must be generated by cross-fitting (out-of-fold predictions) before the logistic stage, otherwise the logistic coefficient for the score is optimistic. Nested CV is needed around the whole two-stage pipeline to report performance.
- If the encoder is pretrained without outcome (self-supervised on ImageCAS) and frozen, the score is a fixed feature and the outcome model's parameter count is just the logistic coefficients: this is the configuration most defensible under EPV/Riley arguments and is the recommended route if a NN is kept.
- Net position: the late-fusion NN is defensible only as exploratory, in the frozen-pretrained or cross-fitted two-stage form, compared under identical resampling against LR and XGBoost on summaries and against MiniRocket/fPCA profile scores. The primary analysis should remain LR (and XGBoost as a flexible check) on prespecified summary features.

### Gaps
- No empirical study found that directly compares end-to-end joint fusion vs two-stage stacking for small clinical cohorts.
