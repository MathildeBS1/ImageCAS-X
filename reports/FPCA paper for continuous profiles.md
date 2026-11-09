# Goldsmith's tract profiles best fit the sentence

**Cite Goldsmith, Crainiceanu, Caffo and Reich (2011, NeuroImage) for the placeholder sentence in `sec:lit-measure`.** Of every peer-reviewed paper the searches turned up, it comes closest to the way the thesis uses FPCA. It measures a continuous quantity (diffusion indices) along an anatomical path (white-matter tracts). It puts position on a normalised [0,1] scale. It enters the whole profile, through an FPCA-based penalized functional regression, into a logistic model for a binary outcome beside base covariates. Above all, it compares that model against a nested model with the **tract mean of the same profile**, on a held-out test set ([PMC3114268](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268)). The full text was read. The alternative is Sangalli et al. (2009, JASA), the only vascular-geometry precedent. It is already in `refs.bib` and was read in full, but it has no base model and no comparison with the mean ([author PDF](https://sangalli.faculty.polimi.it/wp-content/uploads/2023/01/2009_Sangalli-Secchi-Vantini-Veneziani-JASA_compresso.pdf)). Neither paper is coronary, prospective or population-based. The searches found **no peer-reviewed FPCA of coronary curvature profiles related to plaque** and no prospective vascular FPCA study, so the sentence has to borrow from another field and keep its claim small. One practical point: `goldsmith2011pfr` was removed from `refs.bib` earlier, when only an abstract had been read, so the entry must be added again and the header comment in `02_quantifying_geometry.tex` corrected.

## Goldsmith 2011 matches the thesis design point by point

The design lines up with the thesis on almost every axis the question names. The profile is defined on tract position "defined on the interval [0,1]", after subtracting the population mean, as the thesis does with segment position ([PMC3114268](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268)). The models are nested, which matches the thesis comparison of mean turning against shape. Model 1 holds age, sex and a whole-brain MRI index. Model 2 adds "the tract-specific index average". Model 3 is the full profile model. All three are logistic models for case status ([PMC3114268](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268)). The profile enters through FPCA: the companion method paper projects the functional predictor "onto a large number of smooth eigenvectors" and estimates the coefficient function with penalized splines ([Goldsmith et al. 2011, JCGS](https://europepmc.org/article/PMC/PMC3285536)).

The paper also gives the mechanism the thesis argument needs. In the optic radiation, the weight function that best separated the groups "emphasizes the contrast between the middle portion of the tract and its termini", which the average "by construction" mixes together ([PMC3114268](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268)). That is the same point the review makes about curvature: a single value loses where along the path the signal lies.

| Thesis feature | Goldsmith et al. 2011 | Sangalli et al. 2009 |
|---|---|---|
| Profile along an anatomical path | Yes (white-matter tracts) | Yes (internal carotid artery) |
| Normalised position | Yes, [0,1] | No: registered arc length in mm |
| FPCA | FPCA-based penalized regression, smooth β(p) | FPC scores |
| Binary outcome beside a base model | Logistic, with age, sex and a whole-brain index | Quadratic discriminant analysis, no covariates |
| Compared with the mean of the same profile | Yes, nested model | No |
| Held-out evaluation | Train/test split | Leave-one-out |
| Vascular or coronary | No | Vascular, not coronary |
| Read | Full text (PMC author manuscript) | Full text (author PDF) |

## The caveats limit what the sentence may claim

The evidence is weaker than the abstract makes it sound. The design is **cross-sectional and case-control**, multiple sclerosis cases against healthy volunteers, a strong disease contrast unlike plaque-free people followed for a decade ([PMC3114268](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268)). The gain is reported as "up to 15%" improvement in discrimination with a mean of 6.4% across tracts and indices, so the typical gain is modest ([PMC3114268](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268)). The authors say themselves that in the corpus callosum the mean-only model did better than the profile model on the test set, and they put that down to a small test set ([PMC3114268](https://pmc.ncbi.nlm.nih.gov/articles/PMC3114268)). The profile also enters as a smooth coefficient function, not as a few FPC scores, so the paper supports "the whole profile, through FPCA" and not "a few scores" specifically. The AUC values in its Table 2 did not come through the full-text extraction and were not checked. The wording below therefore says the profile model separated the groups better in most tracts, with no numbers, and does not say that profiles beat means in general.

Two other candidates were set aside. Passerini et al. (2012) apply FPCA to carotid radius, curvature and WSS in 52 referral patients and relate the scores to aneurysm location. They do not compare against a scalar summary, and their first radius component "measures the average radius", so it is essentially the mean ([MOX Report 19/2011](https://www.mate.polimi.it/biblioteca/add/qmox/19-2011.pdf)). Only the preprint was read, not the journal version. Hatfield et al. (2015) show in 54 knee osteoarthritis patients that a waveform PCA shape feature, not captured by peak or impulse, belonged to a baseline model associated with later knee replacement ([PMC4654242](https://pmc.ncbi.nlm.nih.gov/articles/PMC4654242/)). It is prospective, but it uses PCA of discretised waveforms, the comparison with discrete measures sits in a companion paper read only as an abstract, and it takes two papers to make the point. The large accelerometry cohorts (UK Biobank, MrOS) enter FPC scores into Cox models but do not compare them against a scalar model of the same curve ([PMC10472628](https://pmc.ncbi.nlm.nih.gov/articles/PMC10472628)).

## Ready wording and bibliography entry

The sentence replaces the placeholder line "Paper on FPCA for a continues measure otherwise hard to quantiy." It follows the chapter rules: author and year as subject, `\cite` after the year, no numbers, no explanation of FPCA, no em dashes.

```latex
Goldsmith et al.\ (2011) \cite{goldsmith2011pfr} measured diffusion along white-matter tracts in
patients with multiple sclerosis and in healthy volunteers, and found that the whole tract profile,
entered through its functional principal components beside age and sex, separated the two groups
better than the tract average in most tracts.
```

A shorter version, if space is tight:

```latex
Goldsmith et al.\ (2011) \cite{goldsmith2011pfr} found that FPCA of diffusion profiles along
white-matter tracts separated patients with multiple sclerosis from healthy volunteers better than
the tract average in most tracts.
```

If Sangalli is used instead (it is already cited at the end of the paragraph, so the closing citation would then repeat it):

```latex
Sangalli et al.\ (2009) \cite{sangalli2009aneurisk} applied FPCA to the radius and curvature
profiles of the internal carotid artery and used the resulting scores to separate patients by
aneurysm location.
```

Entry to add to `refs.bib` again (DOI checked on Crossref in the notes):

```bibtex
@article{goldsmith2011pfr,
  author  = {Goldsmith, Jeff and Crainiceanu, Ciprian M. and Caffo, Brian S. and Reich, Daniel S.},
  title   = {Penalized functional regression analysis of white-matter tract profiles in multiple sclerosis},
  journal = {NeuroImage},
  year    = {2011},
  volume  = {57},
  number  = {2},
  pages   = {431--439},
  doi     = {10.1016/j.neuroimage.2011.04.044}
}
```

The header comment in `02_quantifying_geometry.tex` currently says "goldsmith2011pfr ABSTRACT ONLY (Europe PMC, PMC3285536 has no full text)" and lists it among the dropped sources. PMC3285536 is the JCGS method paper. The NeuroImage application paper has an open author manuscript, PMC3114268, and that full text was read. The comment should record this, together with the caveats above, so the claim is not strengthened later. You have not read the paper yourself, so it is worth checking Table 2 before submission.

## What was read in full and what only as an abstract

Read in full: Goldsmith et al. 2011 NeuroImage (PMC3114268 author manuscript); Sangalli et al. 2009 JASA (authors' posted PDF, which may differ slightly from the typeset version); Passerini et al. 2012 (MOX preprint only, not the journal PDF); Hatfield et al. 2015 Arthritis Care Res (PMC4654242); Stein et al. 2023 and Shi et al. 2021 (PMC). Abstract or record only: the Goldsmith et al. 2011 JCGS method paper (the source for the FPCA link), Goldsmith et al. 2012 JRSS-C, Greven et al. 2010, Hatfield et al. 2015 Clin Biomech, Richter et al. 2014, Deluzio and Astephen 2007, and Zeitzer et al. 2018. The search was not systematic: it used Europe PMC, PMC, Crossref and web search, not Scopus or Web of Science.

## Conclusion

The literature supports a narrow claim: in another field, an FPCA-based model of a whole profile along an anatomical path separated groups better than the mean of the same profile, though not every time and not by much. Goldsmith 2011 is the one paper that makes that claim with the same design as the thesis. Its case-control setting and its corpus callosum reversal are good reasons for the thesis to keep FPCA secondary to mean turning. The same evidence also shows the opening the thesis fills: the searches found no study, coronary or otherwise vascular, that compared a profile with its mean prospectively.
