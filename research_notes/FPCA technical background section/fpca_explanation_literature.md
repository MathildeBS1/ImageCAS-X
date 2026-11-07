# How to explain functional principal component analysis (FPCA) in a technical background section for biomedical readers

Scope note: these notes cover how good expositions explain FPCA, the core equations, the practical computation on a common grid, preprocessing, choosing the number of components, interpretation, pitfalls, and figures. Sources read in full text: Wang, Chiou & Müller (arXiv version of the 2016 Annual Review) and the Warmenhoven et al. (2021) accepted manuscript. Ramsay & Silverman (2005) ch. 8 was reached only through a secondary summary (statKim lecture notes); check its exact notation against the book before citing equations to it. The Shang (2014) survey and the Ullah & Finch (2013) review were checked only for bibliographic details and abstract-level content (the Shang PDF download was blocked).

### Reference list (full bibliographic details)

| Short | Full reference | DOI | Verified how |
|---|---|---|---|
| RS2005 | Ramsay, J.O. & Silverman, B.W. (2005). *Functional Data Analysis*, 2nd ed. Springer Series in Statistics. Springer, New York. (FPCA = ch. 8; registration = ch. 7) | 10.1007/b98888 | DOI quoted in scikit-fda FPCA docstring |
| WCM2016 | Wang, J.-L., Chiou, J.-M. & Müller, H.-G. (2016). Functional data analysis. *Annual Review of Statistics and Its Application* 3, 257–295. arXiv preprint 1507.05135 ("Review of Functional Data Analysis") | 10.1146/annurev-statistics-041715-033624 | search results; the arXiv text was read in full (whether it is identical to the published version was not checked) |
| YMW2005 | Yao, F., Müller, H.-G. & Wang, J.-L. (2005). Functional data analysis for sparse longitudinal data. *JASA* 100(470), 577–590 (PACE) | 10.1198/016214504000001745 | search results (several sources agree) |
| W2021 | Warmenhoven, J., Bargary, N., Liebl, D., Harrison, A., Robinson, M.A., Gunning, E. & Hooker, G. (2021). PCA of waveforms and functional PCA: A primer for biomechanics. *Journal of Biomechanics* 116, 110106 (technical note) | 10.1016/j.jbiomech.2020.110106 | ANU repository record + accepted manuscript read |
| Shang2014 | Shang, H.L. (2014). A survey of functional principal component analysis. *AStA Advances in Statistical Analysis* 98(2), 121–142 | 10.1007/s10182-013-0213-1 | RePEc/IDEAS records |
| UF2013 | Ullah, S. & Finch, C.F. (2013). Applications of functional data analysis: A systematic review. *BMC Medical Research Methodology* 13, 43. PMC3626842 | 10.1186/1471-2288-13-43 | search results |
| RHH2006 | Ryan, W., Harrison, A. & Hayes, K. (2006). Functional data analysis of knee joint kinematics in the vertical jump. *Sports Biomechanics* 5(1), 121–138 | 10.1080/14763141.2006.9628228 | Bohrium listing / UL repository |
| MRSS2015 | Marron, J.S., Ramsay, J.O., Sangalli, L.M. & Srivastava, A. (2015). Functional data analysis of amplitude and phase variation. *Statistical Science* 30(4), 468–484 | 10.1214/15-STS524 | Project Euclid record |
| Silverman1996 | Silverman, B.W. (1996). Smoothed functional principal components analysis by choice of norm. *Annals of Statistics* 24, 1–24 | (not verified) | cited in W2021 reference list |
| JR1992 | Jones, M.C. & Rice, J.A. (1992). Displaying the important features of large collections of similar curves. *The American Statistician* 46(2), 140–145 | 10.1080/00031305.1992.10475870 (from memory, NOT verified) | cited by WCM2016 as the origin of "modes of variation" |
| RHG2009 | Ramsay, J.O., Hooker, G. & Graves, S. (2009). *Functional Data Analysis with R and MATLAB*. Use R! Springer | 10.1007/978-0-387-98185-7 (from memory, NOT verified) | not checked this session |
| KR2017 | Kokoszka, P. & Reimherr, M. (2017). *Introduction to Functional Data Analysis*. Chapman & Hall/CRC | 10.1201/9781315117416 (from memory, NOT verified) | not checked this session |
| GWHB2024 | Gunning, E., Warmenhoven, J., Harrison, A.J. & Bargary, N. (2024/25). *Functional Data Analysis in Biomechanics*. Springer (ISBN 9783031688614) | not checked | search results (book covers smoothing, registration, fPCA, regression, with R code) |
| (avoid) | Dabo-Niang, S. & Frévent, C. (2024). Uncovering data across continua: an introduction to FDA. arXiv 2404.16598 | 10.48550/arXiv.2404.16598 | **preprint, not peer reviewed**; aimed at mathematically strong readers |

---

## 1. Canonical didactic sequence

### Takeaway
Good expositions all follow the same order: curves as data, then the mean function, the covariance function or operator, its eigenfunctions and eigenvalues (Mercer), the scores as projections, the Karhunen–Loève expansion and its truncation to K terms, variance explained, and finally interpretation by "modes of variation" (mean ± c·√λ_k·φ_k). Applied primers (W2021, RHH2006) put "PCA of waveforms" first, then generalise to functions, and add smoothing as the extra step.

### Cited Findings
- FDA treats a sample of real-valued curves X_1(t),…,X_n(t) on a compact interval I as realisations of an L² stochastic process, i.e. $E\int_I X^2(t)\,dt<\infty$; the earlier literature calls these "curve data". — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- In practice the process is latent and observed only at discrete points, often with noise. A common simplifying assumption is "the same dense time grid $t_1,\dots,t_p$ for all n subjects", and smoothness of the curves serves as regularisation so that "information from measurements at neighboring time points can be pooled". — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- The mean function is $\mu(t)=E X(t)$. The covariance function is $\Sigma(s,t)=\operatorname{cov}(X(s),X(t))$, and the covariance operator is $\Sigma(g)=\int_I \Sigma(s,t)\,g(s)\,ds$. The operator is symmetric, non-negative definite and compact, so it has real non-negative eigenvalues. — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- Mercer's theorem gives $\Sigma(s,t)=\sum_{k=1}^{\infty}\lambda_k\,\phi_k(s)\,\phi_k(t)$, with eigenvalues $\lambda_1\ge\lambda_2\ge\dots\ge0$ and orthonormal eigenfunctions $\phi_k$, i.e. $\int_I \Sigma(s,t)\phi_k(s)\,ds=\lambda_k\phi_k(t)$ and $\int\phi_j\phi_k=\delta_{jk}$. — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- The Karhunen–Loève expansion is $X_i(t)=\mu(t)+\sum_{k=1}^{\infty}A_{ik}\,\phi_k(t)$, with scores (FPCs) $A_{ik}=\int_I (X_i(t)-\mu(t))\,\phi_k(t)\,dt$. These satisfy $E(A_{ik})=0$ and $\operatorname{var}(A_{ik})=\lambda_k$, are uncorrelated across k, and are independent across i for independent curves. The series converges in L². — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- The truncation is $X_i^K(t)=\mu(t)+\sum_{k=1}^{K}A_{ik}\phi_k(t)$. What distinguishes FPCA from expanding in any fixed basis (spline, Fourier, wavelet) is that "for a given number of K components the expansion … explains most of the variation in X in the L² sense". — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- FPCA "facilitates the conversion of inherently infinite-dimensional functional data to a finite-dimensional vector of random scores". The usual multivariate tools are then applied to the score vector. FPCA is "the most prevalent tool in FDA". — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- History for a short background paragraph: the ideas go back to Karhunen (1946), Loève (1946), Grenander (1950) and Rao (1958). The first comprehensive inferential framework is Dauxois & Pousse (1976) / Dauxois et al. (1982). — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- The "k-th mode of variation" is the set $\{\mu(t)\pm\alpha\sqrt{\lambda_k}\,\phi_k(t),\ \alpha\in[-A,A]\}$, viewed over a range of α, "usually for A = 2". It comes from Jones & Rice (1992). — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- Applied primer order (W2021): (1) PCA of waveforms. Time points are the p variables. The PCs are mutually uncorrelated, ordered by decreasing variance, and the loadings are eigenvectors of the covariance matrix: $Z=U^{\top}X$, and since U is orthonormal, $X=UZ$ (the data can be reconstructed from the PCs). (2) Scores "measure the degree to which the shape of their waveform corresponds to each feature". (3) fPCA adds representing each curve as a basis expansion (B-splines, Fourier, wavelets) with a roughness penalty chosen by GCV, then "eigenfunctions rather than eigenvectors" are the PCs. — [W2021 manuscript](https://researchonline.ljmu.ac.uk/id/eprint/14271/1/Warmenhoven%202021.pdf)
- RHH2006 is an introductory FDA paper for sports biomechanists. Its keywords are smoothing, landmark registration, functional PCA and discriminant analysis, i.e. it teaches the pipeline smooth → register → FPCA. — [UL repository record](https://pure.ul.ie/en/publications/functional-data-analysis-of-knee-joint-kinematics-in-the-vertical/)
- In the 84 FDA application studies reviewed (PRISMA, 1995 onward), FPCA was the most common technique (51/84, 60.7%). This is useful to motivate FPCA as the standard tool. — [UF2013 (search result summary of PMC3626842)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3626842/)
- Shang (2014) surveys FPCA for exploratory analysis, modelling/forecasting and classification of functional data. — [IDEAS/RePEc](https://ideas.repec.org/a/spr/alstar/v98y2014i2p121-142.html)

### Inferences
- A suggested order for a biomedical reader, each step one short paragraph or equation. (a) A curve per person/segment on a common domain. (b) The mean curve. (c) The covariance surface, i.e. how deviations at two positions co-vary. (d) Eigenfunctions = the dominant shapes of deviation, eigenvalues = how much variance each carries. (e) Score = how much of that shape a given curve has (projection). (f) The KL expansion: curve ≈ mean + Σ score × shape. (g) Fraction of variance explained and the choice of K. (h) Interpretation plots (mean ± 2√λ_k φ_k). Then the practical computation (Section 2).
- The analogy "a PCA in which the variables are the positions along the curve" (W2021) is the most accessible bridge for engineers and clinicians. The functional notation can then be introduced as the continuous limit.
- It helps to say explicitly that the eigenfunctions are estimated from the data, unlike a Fourier or spline basis. This is what makes FPCA optimal in the L² sense, and also what makes it sample-specific (Section 5).

### Gaps
- Ramsay & Silverman (2005) ch. 8 could not be read directly. Its exact notation (they write ξ for eigenfunctions, ρ for eigenvalues and f_i for scores) and section numbers come from a secondary lecture summary. Check them before citing equation-level detail to RS2005.
- The full texts of Shang (2014) and Ullah & Finch (2013) were not read. Their didactic order is not documented here.

---

## 2. Relation to multivariate PCA, and computation on a common grid

### Takeaway
On a fine common grid, FPCA reduces to an ordinary PCA of the n × p matrix of curve values, with the integrals replaced by quadrature. With equal spacing w, the eigenfunctions are $w^{-1/2}$ × the PCA eigenvectors and the eigenvalues are w × the PCA eigenvalues. "PCA on a common grid" is a legitimate (the most rudimentary) implementation of FPCA, provided you state the grid and resampling, the quadrature weights or normalisation, whether and how the curves were smoothed, and that the eigenfunctions are interpolated between grid points. PACE (YMW2005) is the method for sparse or irregular data and is not needed for dense common-grid curves.

### Cited Findings
- Estimating the eigencomponents "is straightforward once the mean and covariance … have been obtained": "one simply approximates the estimated auto-covariance surface … on a finite grid, thus reducing the problem to the corresponding matrix spectral decomposition". — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- RS2005 §8.4.1 (discretisation), via secondary notes. Evaluate the N curves at n equally spaced points to form X (N × n). Set $V=N^{-1}X^{\top}X$ (centred), solve $Vu=\lambda u$, and use the SVD when n ≫ N. With spacing $w=T/n$, the functional eigen-equation becomes $wV\tilde\xi=\rho\tilde\xi$, so $\rho=w\lambda$ and $\tilde\xi=w^{-1/2}u$. The normalisation $\int\xi^2=1$ corresponds to $w\lVert\tilde\xi\rVert^2=1$. Discrete values are turned into a function by interpolation, and "with a fine grid, the choice of interpolation method matters little". — [statKim notes on RS2005 §8.3–8.5](https://statkim.github.io/2019/05/fda-book-chapter-8.3-~-8.5) (secondary; confirmed in substance by [arXiv 1811.08793](https://arxiv.org/pdf/1811.08793), which cites RS2005 §8.4 for $\rho=w\lambda$, $\phi=w^{-1/2}u$)
- RS2005 §8.4.3 (quadrature), via secondary notes. $\int f(s)\,ds\approx\sum_j w_j f(s_j)$. With $W=\operatorname{diag}(w_j)$, solve $W^{1/2}VW^{1/2}u=\rho u$ and set $\tilde\xi_m=W^{-1/2}u_m$. The trapezoidal weights are $h/2,h,\dots,h,h/2$. At most n eigenfunctions can be obtained from n grid points. — [statKim notes](https://statkim.github.io/2019/05/fda-book-chapter-8.3-~-8.5) (secondary)
- RS2005 §8.4.2 (basis expansion), via secondary notes. With $x_i(t)=\sum_k c_{ik}\phi_k(t)$ (coefficient matrix C), Gram matrix $W=\int\phi\phi^{\top}$ and $\xi=\phi^{\top}b$, solve $N^{-1}W^{1/2}C^{\top}CW^{1/2}u=\rho u$ with $b=W^{-1/2}u$. For an orthonormal basis (W = I), this is plain PCA of C. — [statKim notes](https://statkim.github.io/2019/05/fda-book-chapter-8.3-~-8.5) (secondary)
- W2021 Exp. 1 (gait knee angle, 39 children): PCA of waveforms (no smoothing) and B-spline fPCA (roughness penalty by GCV) gave "clear descriptive similarities", and the PC and fPC scores agreed with R² = 0.99 for both of the first two modes. The authors conclude: "PCA of waveforms is the most rudimentary form of FDA", i.e. "one method of implementing fPCA", "the most basic form of fPCA". Small differences are attributed to the smoothing during function fitting. — [W2021 manuscript](https://researchonline.ljmu.ac.uk/id/eprint/14271/1/Warmenhoven%202021.pdf)
- W2021 Exp. 2: smoothing the fPCs (roughness penalty α chosen by leave-one-curve-out CV) lowered the held-out reconstruction error for most K, e.g. by 14% with 4 PCs (SSE 0.155 → 0.134), but not with 2 PCs (0.169 → 0.170). "Smoothing has benefits both for visual interpretation as well as for representing future data". "How much improvement is obtained will depend on the smoothness of the underlying functional data". — [W2021 manuscript](https://researchonline.ljmu.ac.uk/id/eprint/14271/1/Warmenhoven%202021.pdf); method from [Silverman 1996, cited in W2021]
- W2021 lists the advantages of treating data as functions beyond plain PCA: data at different sampling rates/resolutions, derivatives, and alignment of event timing. — [W2021 manuscript](https://researchonline.ljmu.ac.uk/id/eprint/14271/1/Warmenhoven%202021.pdf)
- Dense vs sparse: "dense" data have a growing number of grid points per subject. In sparse longitudinal data each subject has few, irregular measurements. Sparse data "require more effort in theory and methodology". — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- PACE ("principal components analysis through conditional expectation") estimates the mean, the covariance and the measurement-error variance by pooling across subjects. It predicts the scores by conditional expectation instead of numerical integration, which fails when the points per curve are few. The model dimension is chosen by AIC. — [YMW2005 summary](https://www.math.pku.edu.cn/teachers/yaof/papers/2005-jasa.pdf); WCM2016 notes software (Matlab PACE, R `fdapace`/`refund`) — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- scikit-fda `FPCA` "implements functional principal component analysis for both basis and grid representations of the data". It has the parameters `n_components`, `centering` (default True), `regularization` (an L2 roughness penalty), `components_basis` (basis input only) and `_weights` (undocumented), and the attributes `components_`, `explained_variance_`, `explained_variance_ratio_`, `singular_values_` and `mean_`. The grid case is called "discretized functional PCA", and the docstring cites RS2005 for the computation. — [scikit-fda FPCA docs](https://fda.readthedocs.io/en/stable/modules/preprocessing/autosummary/skfda.preprocessing.dim_reduction.FPCA.html)

### Inferences
- What must be stated when the implementation is "PCA on a common grid". (i) How the curves were put on the common grid: the domain, the number of points, and the resampling/interpolation method. (ii) That the grid is dense enough relative to the curve features. (iii) Whether the curves were smoothed before PCA, and how. (iv) The quadrature weights or normalisation. With equal spacing, uniform weights only rescale the eigenvalues (by w) and the scores and eigenfunctions (by √w and 1/√w). The eigenfunction shapes and the fraction of variance explained are unchanged, but this should be said so that reported eigenvalues and scores have known units. With unequal spacing, or trapezoid end weights, the weights change the solution slightly. (v) Centring by the sample mean. (vi) Whether the mean and eigenfunctions were estimated within cross-validation folds when the scores enter a prediction model (otherwise there is leakage; see Section 5).
- Derivation of the scaling: $A_{ik}=\int(X_i-\mu)\phi_k\approx w\sum_j(x_{ij}-\bar x_j)\tilde\xi_{kj}=\sqrt{w}\,(u_k^{\top}(x_i-\bar x))$, so a functional score is √w × the PCA score. This is my own derivation from the RS2005 relations above. It is not quoted from a source.
- PACE is not needed when every curve is densely sampled on a common grid. It is worth one sentence in the background to show awareness and to justify not using it.

### Gaps
- The scikit-fda docs do not say how `_weights` / quadrature are applied for FDataGrid. Check the source code (`skfda/preprocessing/dim_reduction/_fpca.py`) before stating that it uses trapezoid or Simpson weights.
- No source was found that gives a formal rule for "how dense is dense enough" for grid-based FPCA. WCM2016 states that no formal definition of dense functional data exists.

---

## 3. Preprocessing: common domain, registration, centring, smoothing

### Takeaway
FPCA assumes that position t means the same thing on every curve. If features occur at different positions (phase variation), the cross-sectional mean blurs them, the variance is inflated, and the leading components describe timing shifts mixed with amplitude. Registration (landmark or continuous warping) separates the two, but amplitude and phase are not identifiable without extra assumptions. Centring is part of PCA. Smoothing is optional and can be applied to the raw curves or to the eigenfunctions.

### Cited Findings
- Many functional data show "time variation", i.e. the time axis is distorted by a smooth random process (classic example: human growth curves with child-specific timing). — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- "If both amplitude and time variation are jointly present, they cannot be separately identified, so additional assumptions that break the non-identifiability are crucial". — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- Consequence of not registering: time warping "renders the cross-sectional mean function inefficient and uninterpretable … if functions have important features such as peaks at different times, ignoring the differences in timing when taking a cross-sectional mean will distort these features. Then the mean curve will not resemble any of the sample curves" (citing Ramsay & Li 1998). — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- Warping model: $Y_i(t)=X_i\{h_i^{-1}(t)\}$, with amplitude process $X_i$ and strictly monotone warping functions $h_i$, $h_i(0)=0$, $h_i(T)=T$. — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- Landmark registration aligns identifiable features (e.g. peaks) to their average locations with smooth transformations. It is a "gold standard" when well-expressed landmarks are present in all curves, but it requires all landmarks to be present and identifiable, which noisy data often violate. — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- Unaddressed phase variability "artificially often inflates data variance, blurs underlying data structures, and distorts principal components". Aligning by minimising L² distance does not give satisfactory results. Alternatives are elastic / Fisher–Rao metrics. — [MRSS2015 (Project Euclid / search summary)](https://projecteuclid.org/journals/statistical-science/volume-30/issue-4/Functional-Data-Analysis-of-Amplitude-and-Phase-Variation/10.1214/15-STS524.short)
- Smoothing the raw curves: a basis expansion (B-splines, Fourier, wavelets) plus a roughness penalty λ, with GCV "as a starting point … before a final subjective choice". Smoothing the fPCs instead: a roughness penalty α chosen by leave-one-curve-out CV. — [W2021 manuscript](https://researchonline.ljmu.ac.uk/id/eprint/14271/1/Warmenhoven%202021.pdf)
- Measurement error is accommodated in FDA "because for each subject one observes repeated measurements". Smoothing acts as regularisation. — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- FPCA is not robust to outliers ("involves second order moments"). Outliers can be single points or whole outlying shapes. Robust FPCA and functional boxplots exist. — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)

### Inferences
- For curves along a vessel, the "time" axis is position along the centreline. Resampling by normalised arc length (s ∈ [0,1]) is itself a simple linear registration. It aligns the start and end of the segment but not internal features, e.g. a bend at a different relative position in different people. This should be stated as a choice. Without further registration, the components mix "where the bend is" (phase) with "how sharp it is" (amplitude). This applies the WCM2016/MRSS2015 argument to this setting; it is not stated in those sources.
- Using absolute arc length (mm) rather than normalised length changes the domain across people (curves of different lengths). One must then truncate to a common length or normalise, and say which.
- Whatever the domain choice, describe it as the definition of what a component means, not as a neutral preprocessing step.

### Gaps
- No source found on FPCA specifically for coronary centreline curvature or tortuosity profiles, or on registering such curves. Its absence here is only a gap in this search, not a finding.
- The RS2005 ch. 7 registration details (continuous registration criterion) were not accessed.

---

## 4. Choosing the number of components and interpreting signs and scales

### Takeaway
The choice of K is an open problem. Scree plots and fraction-of-variance-explained (FVE) thresholds are ad hoc but standard, and pseudo-AIC/BIC (PACE) and CV are alternatives. Report the FVE per component and cumulatively, and justify the threshold. Eigenfunctions are unique only up to sign (and up to rotation within tied eigenvalues). Scores have mean zero, variance λ_k and are uncorrelated across components, so the positive and negative ends of a component are interpreted only together with the plotted mode of variation.

### Cited Findings
- Choosing K "is an open question". Scree plots and FVE "can be directly extended to the functional setting". Pseudo-AIC and BIC (Yao et al. 2005a) are options, "where the latter selects fewer components". Leave-one-curve-out CV (Rice & Silverman 1991) "tends to overfit functional data by selecting too large K". — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- Choosing K is a bias–variance trade-off: a larger K means less approximation error but more estimated components and more random error. — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- Example of FVE use: "if the first two principal components explain over 90% of the variation … one can approximate the original functional data with only two terms". — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- Fraction of variance explained (standard definition, consistent with var(A_k) = λ_k above): $\mathrm{FVE}(K)=\sum_{k=1}^{K}\lambda_k\big/\sum_{k\ge1}\lambda_k$. In the sample the denominator is the sum of all estimated eigenvalues, which equals $\int\hat\Sigma(t,t)\,dt$, the total pointwise variance integrated over the domain. — definition follows from [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135); scikit-fda reports it as `explained_variance_ratio_` ([docs](https://fda.readthedocs.io/en/stable/modules/preprocessing/autosummary/skfda.preprocessing.dim_reduction.FPCA.html))
- Score properties: $E(A_{ik})=0$, $\operatorname{var}(A_{ik})=\lambda_k$, uncorrelated across k. — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- W2021 interprets components by "positive scorers" (+) and "negative scorers" (−) drawn around the mean. For example, positive scorers on PC1 had more knee flexion in the first half of the gait cycle, and on PC2 a uniformly greater flexion angle. — [W2021 manuscript](https://researchonline.ljmu.ac.uk/id/eprint/14271/1/Warmenhoven%202021.pdf)
- Rotation (RS2005 §8.3, via secondary notes): VARIMAX rotation of the first K eigenfunctions can make them easier to interpret, but it loses the ordering by variance and the uncorrelatedness of the scores. The total sum of squares is preserved. — [statKim notes](https://statkim.github.io/2019/05/fda-book-chapter-8.3-~-8.5) (secondary)

### Inferences
- Sign arbitrariness follows from the eigen-equation: if φ_k solves it, so does −φ_k (with score −A_ik). Software can return either sign, and the sign can flip between CV folds or bootstrap resamples. A thesis should fix a sign convention (e.g. choose the sign so that ∫φ_k > 0, or so that the positive end means "more curvature") and state it. Fold-specific components must be sign-aligned before scores are compared or pooled. The standard math implies this, but I found no peer-reviewed source this session that explicitly states the sign convention advice. Cite it as following from the eigen-equation rather than from a reference.
- Scale: eigenfunctions have unit L² norm, so they are dimensionless shapes on a normalised domain, and the scores carry the units of the curve (times √length of the domain). Expressing scores in SD units ($A_{ik}/\sqrt{\lambda_k}$) makes hazard ratios "per SD of component k" comparable, a common choice in risk models. This is a design inference, not from a source.
- If eigenvalues are close, the corresponding eigenfunctions are poorly determined (they can mix or rotate between samples). This is standard perturbation theory, alluded to by WCM2016's reference to Kato; flag it as a reason not to over-interpret component 3 and beyond.

### Gaps
- No peer-reviewed source found giving a recommended FVE threshold (80/90/95%). The values are conventions. WCM2016 explicitly calls these procedures "ad hoc".

---

## 5. Pitfalls and honest limitations

### Takeaway
Components describe variance, not risk. They are estimated from (and specific to) the sample and preprocessing. Their verbal interpretation is subjective. They are unstable with few curves or close eigenvalues. They are not robust to outliers and are distorted by unregistered phase variation. When scores enter a prediction model, the FPCA must be refitted inside each training fold.

### Cited Findings
- FPCA rests on second moments and is "not robust against outliers". — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- Unregistered phase variation inflates variance and "distorts principal components". — [MRSS2015](https://projecteuclid.org/journals/statistical-science/volume-30/issue-4/Functional-Data-Analysis-of-Amplitude-and-Phase-Variation/10.1214/15-STS524.short); the cross-sectional mean can "not resemble any of the sample curves". — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- Estimation error grows with K (more components to estimate), and choosing the smoothing parameters "remains a challenge due to the auto-correlations within a subject". — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- "Often the eigencomponents and associated modes of variation have compelling and sometimes striking interpretations". This is a positive claim. The interpretation is a reading of plots, not a test. — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- Roughness in unsmoothed fPCs may "reflect random variation in the data that was used to obtain them and that might therefore be different in new data". Smoothing improved held-out reconstruction in most but not all cases. — [W2021 manuscript](https://researchonline.ljmu.ac.uk/id/eprint/14271/1/Warmenhoven%202021.pdf)
- Smoothing parameter choice in W2021: GCV "as a starting point" then "a final subjective choice". — [W2021 manuscript](https://researchonline.ljmu.ac.uk/id/eprint/14271/1/Warmenhoven%202021.pdf)

### Inferences
- "Components describe variance, not risk." FPCA is unsupervised. The leading components are the directions of largest variance in shape, not the shapes most related to the outcome. A low-variance component can matter more for risk, and a high-variance one can be irrelevant. (Supervised alternatives exist, e.g. functional PLS; scikit-fda lists FPLS. Do not claim more than this.)
- Sample specificity: eigenfunctions estimated in one cohort, segment or preprocessing pipeline are not the same coordinates as in another. Scores are comparable only within one fitted FPCA.
- Leakage: if the FPCA (mean and eigenfunctions) is fitted on all participants and the scores then enter a cross-validated risk model, information from the test folds leaks into the features. FPCA is unsupervised, so the leakage is mild, but it is avoidable by fitting the FPCA inside each training fold and projecting the test curves. Sign alignment across folds is then needed (Section 4).
- Few curves: the n × n Gram / SVD route gives at most n − 1 non-trivial components, and leading components with close eigenvalues are unstable. A bootstrap of the eigenfunctions (resample curves, refit, align signs, overlay) is a simple, honest stability check. This is not from the sources read; suggest it as a check, not as standard practice.
- Interpretation language: write "component 1 mainly captures …" with the mode-of-variation figure as evidence, not "component 1 is …".

### Gaps
- No source read this session gives sample-size guidance (number of curves) for stable FPCA eigenfunctions.

---

## 6. Effective figures

### Takeaway
The standard set is (1) spaghetti plot of curves with the mean overlaid; (2) the leading eigenfunctions φ_k(t) with their FVE in the legend; (3) modes of variation: mean ± c·√λ_k·φ_k (c = 2 or a range of α), drawn with "+" and "−" markers; (4) scree / cumulative FVE plot; (5) score scatter (A_1 vs A_2), optionally coloured by a group or outcome. Optionally (6) the covariance surface as a heat map.

### Cited Findings
- Modes of variation, $\mu(t)\pm\alpha\sqrt{\lambda_k}\phi_k(t)$, α ∈ [−2, 2], "a most useful tool to visualize and describe the variation … contributed by each eigenfunction". — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- RS2005 §8.3 (secondary notes): plot the mean together with mean ± a constant multiple of each PC function, using the same constant for every PC so the modes can be compared. The notes give $C^2=T^{-1}\lVert\hat\mu-\bar\mu\rVert^2$ and a factor 0.2. **Caution:** this specific constant comes from a secondary summary and differs from the √λ_k scaling used by WCM2016/Jones & Rice. Check it in the book before using it. — [statKim notes](https://statkim.github.io/2019/05/fda-book-chapter-8.3-~-8.5)
- W2021 figures: GCV curve for λ; first and second modes of variation for PCA vs fPCA with +/− scorers; a scatter comparing PC and fPC scores; unsmoothed vs smoothed PC1. — [W2021 manuscript](https://researchonline.ljmu.ac.uk/id/eprint/14271/1/Warmenhoven%202021.pdf)
- A scree plot / FVE plot is listed by WCM2016 as a standard tool for choosing K. — [WCM2016 arXiv](https://arxiv.org/pdf/1507.05135)
- scikit-fda provides an `FPCAPlot` visualisation (modes of variation). — [scikit-fda docs (search result)](https://fda.readthedocs.io/en/latest/modules/ml.html)

### Inferences
- For a clinical audience, the mode-of-variation plot is the key figure. Readers do not need the eigenfunction itself (whose sign and scale are arbitrary). They need to see what a curve looks like at +2 SD and −2 SD of each component. Use √λ_k scaling (so ±2 means ±2 SD of the score) and say so in the caption.
- Adding a few real example curves with high and low scores beside the synthetic ±2 SD curves grounds the interpretation and guards against over-reading the smooth synthetic curves.
- In a technical background chapter (before any data), a schematic with simulated curves is appropriate, so as not to show cohort results before the methods; the real-data versions belong in Results.

### Gaps
- No empirical study found comparing which FPCA figures readers understand best. The recommendations above rest on convention in the cited expositions.
