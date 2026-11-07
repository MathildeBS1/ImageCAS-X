# Teach FPCA as PCA of curves

The best way to explain functional principal component analysis (FPCA) in this thesis is the standard didactic chain, written in the thesis's own notation. It runs from curves on a common domain to the mean, the covariance, the eigenfunctions and eigenvalues, the scores, the truncated Karhunen–Loève expansion, the variance explained and the modes of variation. One grid section then states plainly that FPCA on an equally spaced grid is ordinary PCA with positions as variables, up to stated scale factors. **This order is the one every major exposition uses, and the grid equivalence is exactly what the code computes** ([Wang, Chiou & Müller](https://arxiv.org/pdf/1507.05135); [Warmenhoven et al. 2021](https://researchonline.ljmu.ac.uk/id/eprint/14271/1/Warmenhoven%202021.pdf)). The section must also cover three limitations that matter more for this thesis than the equations do. First, mapping a segment onto [0, 1] is itself a registration choice, so the components mix where a bend lies with how sharp it is. Second, no rule for choosing K is established. Third, components rank variance, not risk. The drafted section is saved at `thesis/technical_background/08_fpca.tex` and reproduced in full below. **It cannot be adopted yet.** No Methodology section points back to it, the label `sec:tech-fpca` clashes with the parked placeholder in `05_risk_models.tex`, and the FPCA code still disagrees with the Methodology text on how the profile is built, where distance is measured from, which K rule is used and which data are used. These must be settled before the matching Methodology text can be written.

## The didactic chain earns its place for a clinical reader

Every exposition the notes reviewed builds FPCA the same way. Curves are treated as realizations of a random function. The mean function and covariance function come next. The eigenfunctions and eigenvalues follow from Mercer's theorem, and the scores are projections. The Karhunen–Loève expansion, truncated after K terms, ties them together, and interpretation is by modes of variation, μ(t) ± α√λ_k φ_k(t) with α usually up to 2 ([Wang, Chiou & Müller](https://arxiv.org/pdf/1507.05135)). Applied primers for non-statisticians reach the same place from the other direction: they start with PCA of waveforms, where the time points are the variables, and only then generalize to functions ([Warmenhoven et al. 2021](https://researchonline.ljmu.ac.uk/id/eprint/14271/1/Warmenhoven%202021.pdf)). The draft keeps the functional order, so that the definitions are exact and match the thesis's other derivation chains (the cloglog GLMM section opens with a definition, chains numbered equations and follows each with a "where" sentence). The PCA analogy goes into the grid subsection, where it is a statement of fact rather than a teaching device.

Two points decide the content. First, **FPCA is presented as the answer to a regression-input problem**: a profile has many correlated values per segment, too many to enter a model one by one. That is reason-first, and it states no setting. Second, **the mode-of-variation plot is the reader's real handle on a component**. An eigenfunction has unit norm and an arbitrary sign, so a clinician learns nothing from φ_k alone, but a curve drawn at +2 and −2 SD of the score is readable ([Wang, Chiou & Müller](https://arxiv.org/pdf/1507.05135)). The draft therefore defines the mode explicitly. It adds that a verbal label such as "sharp proximal bend" is a reading of a plot, not a tested property, which follows the user's rule to never overstate.

The notation follows the vocabulary notes and avoids every clash. The GLMM uses j for the segment, b_i for the random intercept and β for the coefficients. The curvature Methodology uses j for the vertex and s for both arc length and segment index. The centerline is **c**(s), and the week-10 notes use S for the covariance, which clashes with S_i in the aggregation equation. The draft therefore uses x_i(t) on t ∈ [0, 1], μ, Γ(t, u) for the covariance, φ_k, λ_k, ξ_ik, the grid t_g with g = 1, …, G, the centered matrix **D** with rows **d**_i, eigenvectors **v**_k and spacing w = 1/G.

## Grid computation is PCA, and the scale factors must be written down

The code (`CGPS_data/turning_profile_shapes.py`) column-centers an N × 50 matrix and takes `numpy.linalg.svd` with equal grid weights. **That is a legitimate FPCA, "the most rudimentary form", provided the grid, the resampling, the smoothing and the scaling are stated** ([Warmenhoven et al. 2021](https://researchonline.ljmu.ac.uk/id/eprint/14271/1/Warmenhoven%202021.pdf)). With equal spacing w, the functional eigenvalues are w times the matrix eigenvalues and the eigenfunctions are w^(−1/2) times the unit eigenvectors. The secondary notes on Ramsay & Silverman §8.4 give this, and a second paper that cites the same section confirms it ([statKim notes](https://statkim.github.io/2019/05/fda-book-chapter-8.3-~-8.5); [arXiv 1811.08793](https://arxiv.org/pdf/1811.08793)). It follows that the functional score is w^(1/2) times the PCA score. That last step is derived in the notes, not quoted, and it is checked here from the rectangle rule. The shares of variance and the shapes of the eigenfunctions do not change. Only the units of the eigenvalues and scores do, so the draft says exactly that rather than implying the code's scores are functional scores. The code's eigenvectors have unit Euclidean norm in ℝ^50, so its components differ from L²-normalized eigenfunctions by a factor √50.

The empirical anchor is a knee-angle study of **39 children**. Scores from PCA of waveforms and from a smoothed B-spline FPCA agreed with **R² = 0.99** on each of the first two components. Smoothing the components lowered held-out reconstruction error for most K, for example by **14% at K = 4**, but not at K = 2 ([Warmenhoven et al. 2021](https://researchonline.ljmu.ac.uk/id/eprint/14271/1/Warmenhoven%202021.pdf)). The draft reports the agreement and the "most but not all" result, and gives no smoothing recommendation, since whether the tracer centerlines arrive smoothed is still an open question to Kit.

## Normalized position is a registration choice the text must own

**FPCA assumes position t means the same thing on every curve.** When a feature appears at different positions in different curves (phase variation), the cross-sectional mean "will not resemble any of the sample curves". The variance is inflated, and the leading components describe shifts mixed with amplitude ([Wang, Chiou & Müller](https://arxiv.org/pdf/1507.05135); [Marron et al. 2015](https://projecteuclid.org/journals/statistical-science/volume-30/issue-4/Functional-Data-Analysis-of-Amplitude-and-Phase-Variation/10.1214/15-STS524.short)). When both are present, amplitude and phase are not identifiable without extra assumptions ([Wang, Chiou & Müller](https://arxiv.org/pdf/1507.05135)). Sangalli et al. state that the chosen warp class "jointly defines what is meant by phase variability" ([Sangalli et al. 2009](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)). The draft carries this to the coronary setting as reasoning, not as a cited finding: mapping each segment onto [0, 1] is a linear warp anchored at both ends. It removes segment length and aligns the ends, but leaves a bend at different relative positions in different people, and it discards distance in millimeters from a landmark.

AneuRisk is the vascular example and is cited with the skepticism it needs. The sample was **65 patients referred with suspected cerebral aneurysm**. The ICA centerlines were smoothed, arc length was measured from the terminal bifurcation and registered by an affine warp, and FPCA was run separately on radius and curvature. **Curvature PC1 explained 33.4%** (sharpness at the last siphon peak) and **PC2 18.2%** (curvature between the peaks, possibly residual phase). A QDA on the leading scores had a **leave-one-out error of 21.5%**, with K chosen on the same data and no external validation ([Sangalli et al. 2009](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)). The draft calls it an illustration of the method, not evidence that geometry predicts disease. The notes found **no peer-reviewed FPCA of coronary curvature, tortuosity or taper profiles linked to plaque**. Coronary shape work uses mesh PCA, for example on 211 normal CTCA patients with no outcome ([Medrano-Gracia et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5323506)). That absence comes from limited searching, so it belongs in the literature review, if anywhere, and not in a background section.

## K, sign and the variance-versus-risk closer

**The choice of K "is an open question".** Scree plots and FVE thresholds are ad hoc conventions, pseudo-BIC selects fewer components than pseudo-AIC, and leave-one-curve-out CV "tends to overfit … by selecting too large K" ([Wang, Chiou & Müller](https://arxiv.org/pdf/1507.05135)). The draft states this as fact and leaves the thesis's rule to the Methodology. The sign sentence follows from the eigen-equation: if φ_k solves it, so does −φ_k. The notes found no peer-reviewed source that gives the convention advice, so the draft states it as a consequence and cites nothing. Two further sentences rest on reasoning, not on a citation. One says that components with nearly equal eigenvalues are unstable, which is standard perturbation theory. The other says that the mean and eigenfunctions should be refitted inside training folds to avoid leakage, an inference from the notes. Leave them uncited, or cut them if the examiner expects a source for every claim. The section closes on the fact the week-10 notes already phrase well: **FPCA is unsupervised, so components describe variance, not risk.** A low-variance shape can matter more for plaque, and a leading one can be irrelevant. This also explains the 2026-11-04 decision that the main model uses mean turning: if the real φ1 is flat, its score is close to mean curvature. That is so far shown only in made-up data and Medis trees, and the claim that the real φ1 is flat rests on memory and week-10 prose, because the output sits on dtu-gpu-7.

## The drafted section

Saved verbatim at `/Users/mathildebrinchsorensen/Desktop/ImageCAS-X/thesis/technical_background/08_fpca.tex`. The file is new; no existing file was edited.

```latex
% Technical Background, FPCA section (drafted 2026-11-06, standalone; not yet input anywhere).
% Pointed back to by: NOTHING YET. No Methodology section describes FPCA, and the chapter rule says
%   a background section without a Methodology section pointing back to it is cut. Write the
%   Methodology FPCA text (descriptive shape scores, proximal and mid LAD) first, or drop this file.
% LABEL CLASH: sec:tech-fpca is also defined in the parked 05_risk_models.tex. Never input both;
%   delete the placeholder subsection there when this file is adopted.
% Order: common domain, mean, covariance, eigenfunctions and eigenvalues, scores, Karhunen-Loeve
%   truncation, variance explained, modes of variation, grid computation (scaling stated),
%   registration, choice of K, sign, closer on variance versus risk.
% Notation: x_i(t), t in [0,1], mu, Gamma, phi_k, lambda_k, xi_ik, grid t_g (g = 1..G), D, d_i,
%   v_k, w. Avoids j, s, S, b, beta, c (taken by the GLMM, the curvature section and the centerline).
% LEFT OUT on purpose (Methodology): the grid size, interpolation, the 5 mm chord, the sliding
%   profile, the K rule, the segments analysed, the sign convention chosen, software.
% CITE KEYS NOT YET IN refs.bib: ramsay2005fda, wang2016fda, warmenhoven2021pca,
%   jones1992displaying, marron2015amplitude (entries in reports/FPCA technical background section.md).
% wordlist.txt lacks: FPCA, eigenfunction(s), Karhunen, Loeve, realizations may need checking.
% Figure candidates (made-up data only, re-render as PDF): week10 f4_profiles_deviations,
%   f5_covariance, f7_mean_pm, f8a_rebuild, f9_scree. Never f12_budget or any Medis or tracer figure.

\section{Functional Principal Component Analysis}
\label{sec:tech-fpca}

Functional principal component analysis (FPCA) is principal component analysis applied to a sample of curves, and it represents each curve by its deviation from the mean curve expressed in a few scores \cite{ramsay2005fda, wang2016fda}.
A curve sampled at many positions has many strongly correlated values, too many to enter a regression model one by one, whereas a few scores can.
The curves analyzed here are curvature profiles, curvature against position along a coronary segment (Section~\ref{sec:tech-curvature}).

\subsection{Curves on a Common Domain}
\label{sec:tech-fpca-domain}

A comparison of curves position by position requires a position to mean the same on every curve, so all curves are first defined on one common domain.
Let $x_i(t)$, $i = 1, \dots, N$, denote the curve of unit $i$ at normalized position $t \in [0, 1]$, where $t = 0$ and $t = 1$ are the start and the end of the segment.
The curves are treated as realizations of a random function $X(t)$ with finite mean squared size, $\mathrm{E}\int_0^1 X(t)^2 \, dt < \infty$ \cite{wang2016fda}.

\subsection{Mean, Covariance and Eigenfunctions}
\label{sec:tech-fpca-eigen}

The mean function $\mu(t) = \mathrm{E}\,X(t)$ is the average curve, and the variation around it is described by the covariance function
\begin{equation}
  \Gamma(t, u) = \mathrm{cov}\{X(t), X(u)\},
  \label{eq:tech-fpca-cov}
\end{equation}
where $t, u \in [0, 1]$ are two positions on the domain.
$\Gamma(t, u)$ is large when curves that lie above the mean at $t$ also tend to lie above it at $u$, so a bend that spreads over neighboring positions appears as a band of high covariance around the diagonal $t = u$.
The covariance function is symmetric and non-negative definite, and it therefore decomposes into eigenfunctions $\phi_k$ and eigenvalues $\lambda_k$ that solve
\begin{equation}
  \int_0^1 \Gamma(t, u)\, \phi_k(u)\, du = \lambda_k \phi_k(t),
  \qquad
  \int_0^1 \phi_k(t)\, \phi_{k'}(t)\, dt =
  \begin{cases} 1, & k = k', \\ 0, & k \neq k', \end{cases}
  \label{eq:tech-fpca-eigen}
\end{equation}
where $\lambda_1 \ge \lambda_2 \ge \dots \ge 0$, and the second condition makes the eigenfunctions orthonormal \cite{wang2016fda}.
Each eigenfunction is a shape of deviation from the mean, and its eigenvalue is the variance of the curves along that shape, so $\phi_1$ is the single shape along which the curves differ most.
The covariance function is rebuilt from these pairs as $\Gamma(t, u) = \sum_{k \ge 1} \lambda_k \phi_k(t) \phi_k(u)$, which is Mercer's theorem \cite{wang2016fda}.

\subsection{Scores and the Karhunen--Lo\`eve Expansion}
\label{sec:tech-fpca-scores}

The amount of each shape in a given curve is its score, the projection of the curve's deviation from the mean onto the eigenfunction,
\begin{equation}
  \xi_{ik} = \int_0^1 \{x_i(t) - \mu(t)\}\, \phi_k(t)\, dt ,
  \label{eq:tech-fpca-score}
\end{equation}
where $\xi_{ik}$ is the score of unit $i$ on component $k$.
The scores have mean zero and variance $\lambda_k$, and scores on different components are uncorrelated \cite{wang2016fda}.
Each curve is recovered from the mean and its scores by the Karhunen--Lo\`eve expansion, truncated after $K$ terms,
\begin{equation}
  x_i(t) = \mu(t) + \sum_{k=1}^{\infty} \xi_{ik} \phi_k(t)
  \approx \mu(t) + \sum_{k=1}^{K} \xi_{ik} \phi_k(t),
  \label{eq:tech-fpca-kl}
\end{equation}
where the truncated sum replaces the curve by $K$ numbers.
For a given $K$, no other set of $K$ basis functions approximates the curves with a smaller expected squared error, which distinguishes the eigenfunctions from a fixed spline or Fourier basis and also makes them specific to the sample from which they are estimated \cite{wang2016fda}.
The share of the total variance that the first $K$ components retain is the fraction of variance explained,
\begin{equation}
  \mathrm{FVE}(K) = \frac{\sum_{k=1}^{K} \lambda_k}{\sum_{k \ge 1} \lambda_k},
  \label{eq:tech-fpca-fve}
\end{equation}
where the denominator equals $\int_0^1 \Gamma(t, t)\, dt$, the variance at each position summed over the domain.

\subsection{Modes of Variation}
\label{sec:tech-fpca-modes}

An eigenfunction on its own has unit size and an arbitrary sign, so a component is read from its mode of variation, the mean shifted along the eigenfunction by a multiple of the standard deviation of the score,
\begin{equation}
  \mu(t) \pm \alpha \sqrt{\lambda_k}\, \phi_k(t),
  \label{eq:tech-fpca-mode}
\end{equation}
where $\alpha$ is commonly 1 or 2, so that the curve with $+\alpha$ is that of a unit whose score on component $k$ lies $\alpha$ standard deviations above the mean and whose other scores are zero \cite{jones1992displaying, wang2016fda}.
Plotting the two curves of Eq.~\eqref{eq:tech-fpca-mode} on either side of the mean shows what a high and a low score look like, such as a bend that is sharper or flatter in one part of the segment.
The verbal label given to a component is a reading of this plot and not a tested property of the curves.

\subsection{Computation on a Grid}
\label{sec:tech-fpca-grid}

Curves are observed at discrete points, so the integrals above are replaced by sums over a common grid of positions $t_g$, $g = 1, \dots, G$, onto which every curve is interpolated \cite{ramsay2005fda}.
Let $\mathbf{D}$ be the $N \times G$ matrix with rows $\mathbf{d}_i$ and entries $d_{ig} = x_i(t_g) - \hat\mu(t_g)$, where $\hat\mu(t_g)$ is the sample mean at position $t_g$.
On an equally spaced grid with spacing $w = 1/G$, the eigenproblem~\eqref{eq:tech-fpca-eigen} becomes the eigenproblem of the sample covariance matrix $N^{-1}\mathbf{D}^\top\mathbf{D}$, with unit-length eigenvectors $\mathbf{v}_k \in \mathbb{R}^G$ and eigenvalues $\tilde\lambda_k$, and the functional quantities follow as
\begin{equation}
  \hat\lambda_k = w\, \tilde\lambda_k,
  \qquad
  \hat\phi_k(t_g) = w^{-1/2}\, v_{kg},
  \qquad
  \hat\xi_{ik} = w^{1/2}\, \mathbf{v}_k^\top \mathbf{d}_i ,
  \label{eq:tech-fpca-grid}
\end{equation}
where $v_{kg}$ is entry $g$ of $\mathbf{v}_k$ and $\hat\xi_{ik}$ is the score~\eqref{eq:tech-fpca-score} computed by the rectangle rule \cite{ramsay2005fda}.
FPCA on an equally spaced grid is therefore ordinary principal component analysis with the grid positions as variables, computed from the singular value decomposition of $\mathbf{D}$, and the factors in Eq.~\eqref{eq:tech-fpca-grid} rescale the eigenvalues, eigenfunctions and scores without changing the shape of the eigenfunctions or the fraction of variance explained.
The scale of the scores depends on whether these factors are applied, so their units are defined only once the scaling is stated.
On knee-angle curves from 39 children, scores from this discrete form and from a smoothed spline-based FPCA agreed with $R^2 = 0.99$ on each of the first two components, with the remaining differences attributed to smoothing \cite{warmenhoven2021pca}.
Smoothing the eigenfunctions with a roughness penalty lowered the error of reconstructing held-out curves for most but not all values of $K$ in the same study \cite{warmenhoven2021pca}.
Curves observed at only a few irregular points per unit cannot be put on a common grid this way and require estimators that pool information across units \cite{wang2016fda}.

\subsection{Registration: Amplitude and Phase}
\label{sec:tech-fpca-registration}

The mean at position $t$ summarizes the curves only if their features lie at the same $t$, and curves differ both in amplitude, how large a feature is, and in phase, where along the domain it lies.
Unaligned phase variation inflates the variance, blurs the mean until it may resemble none of the curves, and produces leading components that mix a shift of a feature with a change of its size \cite{wang2016fda, marron2015amplitude}.
Registration separates the two by warping the domain of each curve with a strictly increasing function, either to align landmarks such as peaks or to minimize the distance to a common template \cite{ramsay2005fda, wang2016fda}.
Amplitude and phase cannot be told apart from the curves alone when both are present, so the chosen class of warping functions defines what counts as phase \cite{wang2016fda, sangalli2009aneurisk}.
Mapping each segment onto $[0, 1]$ is itself such a choice, a linear warp anchored at the two ends of the segment, which removes the length of the segment and aligns its ends but leaves a bend at different relative positions in different curves, so that phase within the segment remains in the components and the distance in millimeters from a landmark is no longer represented.

The analysis of the internal carotid artery by Sangalli et al.\ \cite{sangalli2009aneurisk} is the vascular example of this sequence.
Centerlines from 65 patients referred with suspected cerebral aneurysm were smoothed, their arc length was measured from the terminal bifurcation and registered by an affine warp, and FPCA was run separately on the radius and the curvature profiles.
The first curvature component explained 33.4\% of the variance and described how sharply the artery bends at its last curvature peak, while the second explained 18.2\% and described curvature between the two peaks, a pattern that may also reflect a residual shift of the peak position.
The leading scores separated patients by aneurysm location with a leave-one-out error of 21.5\%, in a small cross-sectional sample in which the number of components was chosen on the same data, so the study illustrates the method rather than showing that geometry predicts disease \cite{sangalli2009aneurisk}.

\subsection{Number of Components and Sign}
\label{sec:tech-fpca-k}

The choice of $K$ balances the approximation error of a short expansion against the estimation error of the added components, and no rule for it is established \cite{wang2016fda}.
Scree plots and thresholds on the fraction of variance explained, such as 80 or 90\%, are conventions without a theoretical basis, information criteria tend to select fewer components, and leave-one-curve-out cross-validation tends to select too many \cite{wang2016fda}.
Components with nearly equal eigenvalues are poorly determined and can exchange or mix between samples, which makes components beyond the first few the least stable.
The sign of a component is arbitrary, since $-\phi_k$ solves Eq.~\eqref{eq:tech-fpca-eigen} whenever $\phi_k$ does and reverses the sign of every score $\xi_{ik}$.
A convention therefore fixes the sign, and components estimated again on bootstrap samples or cross-validation folds are aligned to it before they are compared, which is also needed when the mean and eigenfunctions are estimated within training folds so that the scores entering a validated model do not draw on the test units.

FPCA does not use any outcome: its components are ordered by how much of the variance of the curves they explain in the sample, not by their association with disease, so a low-variance component can carry more risk information than a leading one, and a leading one can carry none.
The components are also specific to the sample, the domain and the preprocessing from which they are estimated, and they rest on second moments that are sensitive to outlying curves \cite{wang2016fda}.

% FIGURE (suggested, not yet rendered as PDF): made-up curves only, e.g. week10 f7_mean_pm.
% \begin{figure}[h]
%   \centering
%   \includegraphics[width=0.85\textwidth]{content/background/figures/fpca_modes.pdf}
%   \caption{Modes of variation of simulated curvature profiles. The black curve is the mean
%     $\mu(t)$; the colored curves are $\mu(t) \pm 2\sqrt{\lambda_k}\,\phi_k(t)$ for the first
%     three components, with the fraction of variance explained in each panel title. The curves
%     are simulated and are not data from any cohort.}
%   \label{fig:tech-fpca-modes}
% \end{figure}
```

### BibTeX entries to add to refs.bib (not added)

`sangalli2009aneurisk` is already in `refs.bib`. The other five are below. Check the two marked UNVERIFIED before adding them. Ramsay & Silverman's chapter 8 was reached only through secondary lecture notes, so the grid relations cited to it should be checked against §8.4 of the book itself ([statKim notes](https://statkim.github.io/2019/05/fda-book-chapter-8.3-~-8.5)).

```bibtex
@book{ramsay2005fda,
  author    = {Ramsay, James O. and Silverman, Bernard W.},
  title     = {Functional Data Analysis},
  edition   = {2},
  series    = {Springer Series in Statistics},
  publisher = {Springer},
  address   = {New York},
  year      = {2005},
  doi       = {10.1007/b98888},
  note      = {DOI as quoted in the scikit-fda FPCA docstring. FPCA ch. 8, registration ch. 7;
               ch. 8 seen only via secondary notes, check section 8.4 before citing equations}
}

@article{wang2016fda,
  author  = {Wang, Jane-Ling and Chiou, Jeng-Min and M{\"u}ller, Hans-Georg},
  title   = {Functional Data Analysis},
  journal = {Annual Review of Statistics and Its Application},
  volume  = {3},
  pages   = {257--295},
  year    = {2016},
  doi     = {10.1146/annurev-statistics-041715-033624},
  note    = {Read as arXiv:1507.05135; identity with the published version not checked}
}

@article{warmenhoven2021pca,
  author  = {Warmenhoven, John and Bargary, Norma and Liebl, Dominik and Harrison, Andrew and
             Robinson, Mark A. and Gunning, Edward and Hooker, Giles},
  title   = {{PCA} of Waveforms and Functional {PCA}: A Primer for Biomechanics},
  journal = {Journal of Biomechanics},
  volume  = {116},
  pages   = {110106},
  year    = {2021},
  doi     = {10.1016/j.jbiomech.2020.110106}
}

@article{jones1992displaying,
  author  = {Jones, M. C. and Rice, John A.},
  title   = {Displaying the Important Features of Large Collections of Similar Curves},
  journal = {The American Statistician},
  volume  = {46},
  number  = {2},
  pages   = {140--145},
  year    = {1992},
  doi     = {10.1080/00031305.1992.10475870},
  note    = {UNVERIFIED DOI (from memory); origin of "modes of variation" per Wang et al. 2016}
}

@article{marron2015amplitude,
  author  = {Marron, J. S. and Ramsay, James O. and Sangalli, Laura M. and Srivastava, Anuj},
  title   = {Functional Data Analysis of Amplitude and Phase Variation},
  journal = {Statistical Science},
  volume  = {30},
  number  = {4},
  pages   = {468--484},
  year    = {2015},
  doi     = {10.1214/15-STS524},
  note    = {Bibliographic record checked on Project Euclid; full text not read}
}
```

Also add `FPCA`, `eigenfunction`, `eigenfunctions`, `Karhunen` and `Loève` to `thesis/wordlist.txt`, or hunspell will flag them.

## Figures: four made-up-data panels from week 10

**Use only the simulated week-10 figures.** `thesis/week10/week_figure/fpca/` holds made-up data from 300 people run through the same code. The best fits, in reading order, are these:

| Figure | Illustrates | Subsection |
|---|---|---|
| `f4_profiles_deviations` | Curves on [0, 1], the mean, deviations | Curves on a common domain / mean |
| `f5_covariance` | Covariance surface Γ(t, u) beside φ_1–φ_3 | Mean, covariance and eigenfunctions |
| `f7_mean_pm` | Modes of variation μ ± 2√λ_k φ_k | Modes of variation (the key figure) |
| `f8a_rebuild` | Truncated Karhunen–Loève reconstruction for growing K | Scores and expansion |
| `f9_scree` (optional) | FVE per component and cumulative | Scores and expansion / choice of K |

**Do not use** `f12_budget`, which uses CGPS event counts, any `turning_profile_shapes_phi_*` figure (Medis data) or `turning_profile_example`, which shows one person's anatomy and has no clearance to leave the server. `f10_boot_cv` and `f3_grid` show the thesis's own K rules and grid of 50, so they are Methodology material. The week-10 figures are PNGs in a custom palette. Re-render them as PDF in the thesis style, under `content/background/figures/`, and keep "simulated" in every caption. The `.tex` file includes a commented-out figure block for the modes plot.

## Eleven text/code mismatches block the Methodology FPCA text

The Methodology must describe exactly what `CGPS_data/thesis_final/` does, but **no FPCA or curvature code exists there yet**. The only FPCA code is the exploratory `CGPS_data/turning_profile_shapes.py`. The user must settle each item below before writing the Methodology section that would point back to `sec:tech-fpca`.

| # | Issue | Text says | Code does | Decision needed |
|---|---|---|---|---|
| 1 | **Profile definition** | `06_curvature.tex`: κ_j = θ_j/ℓ on vertices respaced at ℓ = 5 mm "starting at the ostium" | `tortuosity/curvature.profile_thesis`: sliding 5 mm chord centered on every original centerline point ("instead of on vertices laid from P[0]") | Which profile FPCA uses, and describe it in 06_curvature (the text has no sliding profile) |
| 2 | **Distance origin** | `05_features.tex`: distance "counted from the ostium" | `split_trunks.py`: LAD and LCx from the LM bifurcation, RCA from the ostium | One origin, stated per artery; it changes which first 5 mm are lost |
| 3 | **K rule undecided** | week-10 `fpca_explained`: pass Horn and bootstrap, capped by budget; `fpca_from_plots`: smallest of Horn, bootstrap, CV; `saved.md`: min(shapes that pass, K_max) | Reports six rules (var80, var90, Horn, shift, boot, CV), picks none, KMAX = 15 | One prespecified rule, frozen before the outcome is seen |
| 4 | **Data source** | Thesis is about the plaque-free CGPS cohort with tracer geometry | `--trees` defaults to `medis`; the tracer loader (`thesis_final/split_check.tracer_tree`) "is not written yet", so FPCA has run only on people with plaque at baseline | Write the tracer loader; rerun FPCA on the plaque-free cohort before any FPCA claim (including "φ_1 is flat") |
| 5 | **Normalization endpoints** | Background draft: t = 0, 1 at the segment ends | `on_grid` maps the first and last profile point inside [lo, hi) to 0 and 1, not the segment boundaries | State it as such, or change the code |
| 6 | **Smoothing** | `06_curvature.tex`: "No smoothing was applied beyond the respacing"; tracer smoothing is an open question to Kit | `smooth=0.0`; the sliding window acts as a 5 mm scale | Settle after Kit answers; say so in Methodology |
| 7 | **Inclusion rules** | T_ℓ missing if fewer than two turning angles | FPCA needs ≥ 5 profile points, segment ≥ 10 mm (trunk ≥ 20 mm), ≥ 10 people per matrix | One rule, or report both |
| 8 | **Scaling and scores** | Week 10: standardized z = c/SD, hazard ratio per SD | Unit-norm eigenvectors in ℝ^50 (no quadrature weight, factor √50 from L²); scores neither standardized nor exported; sign fixed so each component sums to ≥ 0 | State the scaling and the sign convention; implement export of the standardized scores |
| 9 | **Descriptive models** | Memory (2026-11-04): FPCA only on pLAD and mLAD, each with its own descriptive cloglog (SCORE2 + shape scores), outside the LR test | Not coded; script runs all 9 segments + 3 trunks | Code the two descriptive models; state if FPCA is refitted inside CV folds (leakage, sign alignment) |
| 10 | **Stale drafts** | `methodology_long_draft.tex:211` (FPCA "fitted on ImageCAS-X", tested Model 2); `week5/risk_model_plan.tex:69` (K 3 to 5); `05_risk_models.tex` plan (logistic, 1D CNN) | — | Delete or mark obsolete so they are not reused |
| 11 | **Chapter wiring** | Chapter rule: every background section needs a Methodology section pointing back; `00_chapter_intro.tex` map has no FPCA entry; `sec:tech-fpca` also defined in parked `05_risk_models.tex` | — | Add the Methodology section and map line, delete the placeholder subsection, then `\input` `08_fpca.tex` |

The pLAD/mLAD budget numbers (275 and 201 events) come from `segment_k_budget.py`. They were computed on 1,077 plaque-free people before the image-quality exclusion, so they will change once the analysed cohort is fixed ([local file: CGPS_data/saved.md]).

## Conclusion

The background section is the easy part, and it is now drafted. FPCA is general mathematics, and stating it exactly costs nothing. The hard part is that FPCA has become a descriptive side analysis, run on two LAD segments with a K rule that is not yet chosen and on data the thesis does not use. **The section's value depends on the Methodology text that will point back to it, and that text cannot honestly be written until the four core choices are frozen: the profile, the origin, K and the tracer data.** Settling them before the outcome is examined is also what makes the shape scores defensible as prespecified rather than tuned. The background's closer, that components rank variance and not risk, is also the honest answer to anyone who asks why mean turning, not FPCA, sits in the tested model.

If the descriptive pLAD/mLAD analysis is dropped, cut this file. The chapter rule leaves no place for a background section that nothing points back to. The decision costs little either way, since the main who model does not depend on it.
