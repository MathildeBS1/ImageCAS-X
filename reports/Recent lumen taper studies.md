# Three recent papers extend Johnston's taper argument

Only **three post-2010 papers** earn a place after the Johnston 2009 sentence. **Schultz et al. 2023** is CFD in plaque-free CCTA arteries; WSS rises as the lumen narrows, and the authors link the flat WSS along the right coronary artery to its nearly constant diameter. **Kandangwa et al. 2022** removed the taper from one healthy volunteer's right coronary artery model and the highest WSS moved from distal to proximal. **Pacheco et al. 2021** is the one clinical study in which a taper measure went with atherosclerosis, in a small, referred, cross-sectional angiographic sample. A fourth, **Choi et al. 2020** (CCTA diameter scales with the tree it supplies), is relevant but fits Methods better than this paragraph. Since 2010, none of the three search streams found a study that **varies taper on its own in non-diseased human arteries and reports WSS**, or that **tests baseline taper against plaque that develops later**. Johnston 2009 is still the only direct tapered-versus-uniform comparison. The added sentences should therefore extend Johnston's idealised result to patient geometry and add one honest clinical data point. They should not suggest that taper is a known predictor. Every other candidate fails at least one test: it is about diseased or treated arteries, it measures tree-level scaling rather than segment slope, it uses taper only as a reference for detecting stenosis or computing FFR, or it could not be verified.

## The recent taper literature is mostly taper as a nuisance

Recent coronary papers mostly treat taper as a fixed normal reference, not as an exposure. CCTA lesion detection fits an "expected" linear taper over the proximal and mid artery and flags departures from it as plaque ([Kang et al. 2013](https://doi.org/10.1118/1.4794480)). Angiographic flow computation has replaced "a linear tapering of the reference vessel size" with a Murray-law step-down reference diameter ([Tu et al. 2021](https://doi.org/10.1002/ccd.29592)), and this has since been carried over to CCTA ([Weng et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11472136/)). The longitudinal CCTA geometry studies do not include taper. ICONIC used distance from the ostium, bifurcation location and tortuosity ([Han et al. 2022](https://doi.org/10.1001/jamacardio.2021.5705)). The one serial CCTA study with plaque-free segments at baseline used radiomic cross-section and centreline-motion features around myocardial bridges, and the main text names no taper feature ([Chen et al. 2024](https://doi.org/10.1093/ehjci/jeae135)). **Taper on a plaque-free baseline is therefore still untested as a plaque predictor.** That gap is already stated in `sec:lit-risk`, which the content map makes the only place for it. The new sentences must not restate it.

## Patient-geometry simulations carry Johnston's idealised result forward

**Schultz et al. 2023 is the strongest addition.** It is the only post-2010 study that matches the thesis setting: CCTA, arteries free of plaque, and the LAD, LCx and right coronary artery reported separately. In 349 normal vessels from 168 referred patients, "ESS values increase rapidly and become widely scattered with decreasing lumen diameter". The authors explain the smaller variation of WSS along the right coronary artery by noting that "the LAD and LCx taper more rapidly in diameter while the RCA remains fairly constant until very distally" ([Schultz et al. 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9870961/)). This is diameter-wise evidence, not a slope analysis. Every vessel received the **same fixed outflow and no side branches**, which the authors say gives unrealistically high distal ESS, so part of the proximal-to-distal gradient is built into the model. That caveat has to stay in the prose. The key is already in `refs.bib`, but its author list is cut off after five names without "and others" (fix below).

**Kandangwa et al. 2022 is the only post-2010 paper found that switches taper off in a non-idealised coronary artery.** The geometry is the right coronary artery of one healthy 31-year-old volunteer, reconstructed from 4-D MRI. In a sensitivity analysis reported in its limitations section, removing the taper (using a method that assumes constant mean axial velocity) meant that "the largest values of the dimensional TAWSS and transWSS metrics occur in the proximal rather than distal parts", while OSI changed less ([Kandangwa et al. 2022](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2022.962687/full)). The authors also say that the side branches were not modelled, so flow is "increasingly too high" down the vessel and WSS magnitudes are not yet suitable for comparison with lesions. The paper therefore shows that taper alone moves where WSS peaks in a real artery shape. It does **not** show that taper sets low WSS in vivo. It is n = 1, MRI and not CCTA, and the effect is reported as a side result.

Alamir et al. 2024 is a tempting addition and should be left out. The full text says "the radius and inlet velocity are the most important features" of a U-net WSS surrogate and that "Curvature as Menger curvature is not shown as significant" ([Alamir et al. 2024](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2024.1360330/full)). But the vessels are stenosed and reconstructed from invasive angiography, the ranking is the surrogate's attribution rather than a physical sensitivity, and the paper treats taper only as a check ("the tapering is not substantial"). It adds a diseased-artery echo of Johnston 2007, which the paragraph already cites.

## The one clinical association is weak and probably reversed

**Pacheco et al. 2021 is the only 2010–2026 human study found that relates a coronary taper metric to atherosclerosis.** It enrolled 51 symptomatic women referred for invasive coronary function testing, with suspected ischaemia and no obstructive stenosis. Its QCA taper z-scores were referenced to pooled angiographic norms. The maximal absolute antegrade and retrograde tapering z-scores correlated weakly with an angiographic atherosclerosis score (r = 0.29 and 0.33). They were **not** related to coronary flow reserve, although the abstract suggests that "atheroma burden, size and tapering are related to CFR" ([Pacheco et al. 2021, full text](https://europepmc.org/article/PMC/PMC10976284)). The study is cross-sectional, in a referred sample of women only. Taper is scored as an absolute deviation, so the direction is lost, and plaque can easily have changed the taper. For the thesis it marks where the evidence stands: taper and atherosclerosis go together only in a design that cannot separate cause from effect, which a plaque-free baseline can. Cite the full text, not the abstract. Crossref gives volume 6, not volume 1 as in the notes.

## Scaling-law work belongs to Methods, not this paragraph

**Choi et al. 2020** is the best human CCTA support for the premise that taper follows flow loss. In 43 patients without obstructive lesions (638 arteries), lumen diameter followed power laws of downstream length and myocardial mass, fitted with OLS, Deming and **Theil–Sen** regression. The exponents were lower than the Huo–Kassab theory (diameter–length about 0.28 against 3/7), which the authors attribute mainly to small arteries that CT cannot resolve ([Choi et al. 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7387886/)). It is a precedent for the thesis's estimator and its scale-free framing. However, the current paragraph no longer states the flow-loss premise (Gijsen was cut), and the content map gives scaling exponents to Methods 05c and the taper rationale to 05d. Choi therefore fits better as a cite in `05d_taper.tex` than in the review. The Huo et al. 2013 scaling-deviation papers are tree-level. In humans they flag lumens *too small* for their tree in metabolic syndrome ([Huo et al. 2013, Radiology](https://pmc.ncbi.nlm.nih.gov/articles/PMC3750415/)). Only in pigs do they flag lumens *too large*, after positive remodelling, i.e. as a consequence of disease ([Huo et al. 2013, J R Soc Interface](https://pmc.ncbi.nlm.nih.gov/articles/PMC3627114/)). Neither fits the direction or the timing of the thesis hypothesis.

## Conclusion

The literature since 2010 has not tested the taper hypothesis, so the paragraph cannot report progress on it. What the new papers add is a change in setting: from rigid idealised tubes (Johnston 2009) to real artery shapes (Kandangwa) and to plaque-free CCTA arteries (Schultz). In both, the WSS distribution along the artery tracks how the lumen narrows. The single clinical association (Pacheco) shows why the plaque-free design matters, because in diseased arteries taper is as likely an effect of plaque as a cause. Every patient-geometry simulation shares one weakness: side branches are missing, so flow loss, which is what taper is thought to match, is never modelled. That limitation belongs in the prose of Schultz's sentence and later in the Discussion. It is the reason the thesis's raw log-radius slope is at best a noisy proxy for a flow-matched taper.

## (a) Ranked shortlist

| Rank | Paper | Why it earns its place for the thesis's taper | Caveats | DOI | Access |
|---|---|---|---|---|---|
| 1 | Schultz et al. 2023, *Int J Cardiovasc Imaging* 39:441–450 | Plaque-free CCTA arteries, LAD/LCx/RCA separately; WSS rises as the lumen narrows; the authors tie the RCA's uniform WSS to its near-constant diameter, the closest thing to taper vs WSS in the thesis setting | Referred patients; fixed 1 ml/s outflow, no side branches, so the distal gradient is partly built in; diameter per 3 mm segment, not a slope | [10.1007/s10554-022-02739-0](https://doi.org/10.1007/s10554-022-02739-0) | Open access (PMC9870961), full text read |
| 2 | Kandangwa et al. 2022, *Front Bioeng Biotechnol* 10:962687 | Only post-2010 test that removes taper from a real coronary geometry; the WSS peak moves proximally, extending Johnston 2009 beyond idealised tubes | n = 1 healthy volunteer; MRI, not CCTA; sensitivity analysis in the limitations; no side branches; authors say magnitudes are not yet comparable to lesions | [10.3389/fbioe.2022.962687](https://doi.org/10.3389/fbioe.2022.962687) | Open access, full text read (2026-11-07) |
| 3 | Pacheco et al. 2021, *Am Heart J Plus* 6:100027 | Only human study relating a taper measure to atherosclerosis; shows the reverse-causation problem a plaque-free baseline avoids | n = 51 referred women with INOCA; cross-sectional; angiographic; absolute deviation (no sign); weak correlation; abstract misstates the CFR result | [10.1016/j.ahjo.2021.100027](https://doi.org/10.1016/j.ahjo.2021.100027) | Open access (PMC10976284), full text read |
| 4 (optional, Methods 05d) | Choi et al. 2020, *Physiol Rep* 8(14):e14514 | CCTA diameter follows the downstream tree; Theil–Sen precedent | Referred, n = 43; exponents below theory; tree-level, not along one artery; scaling content is owned by Methods | [10.14814/phy2.14514](https://doi.org/10.14814/phy2.14514) | Open access (PMC7387886), full text read |

Ownership note: Pacheco is about atherosclerosis rather than WSS. If the section must stay strictly geometry → WSS, move its sentence to `sec:lit-risk` (`03_geometry_risk.tex`), next to Han 2022. Either way it must not be written as a gap statement, because the gap is stated once, in `sec:lit-risk`.

## (b) Draft LaTeX (insert directly after "...complementary rather than redundant information.")

```latex
Schultz et al.\ (2023) \cite{schultz2023ess} simulated the flow in plaque-free arteries
reconstructed from the CCTA of referred patients and found that WSS rose steeply as the lumen
narrowed, and that it varied least along the right coronary artery, whose diameter the authors
noted stayed nearly constant while the LAD and LCx tapered.
The same outflow was, however, imposed on every artery without its side branches, which builds part
of this gradient into the model.
Kandangwa et al.\ (2022) \cite{kandangwa2022rca} removed the taper from a model of the right
coronary artery of a single healthy volunteer imaged with MRI and found the highest WSS in the
proximal rather than the distal part of the artery, showing that taper alone shifts where WSS is
high or low along a real artery.
Clinically, Pacheco et al.\ (2021) \cite{pacheco2021taper} found in symptomatic women referred for
invasive testing without obstructive disease that larger deviations of the angiographic taper from
population reference values went with more extensive atherosclerosis, but the cross-sectional
design cannot tell whether the taper preceded the plaque or was altered by it.
```

Four sentences, no numbers, no lists, no forward references, no sentence opening with "Since" or "Because". The cohorts are marked: referred (Schultz, Pacheco), single healthy volunteer and MRI (Kandangwa), cross-sectional (Pacheco). "Right coronary artery" is written out, because RCA is not defined in this section. If space allows only three sentences, drop the Pacheco sentence or move it to `sec:lit-risk`.

Matching edit to the "Collectively" closing sentence: it now says "a lumen that narrowed less or widened was associated with low WSS in idealised coronary models". To keep it true, either leave it as is (it still describes Johnston 2009 correctly), or change "in idealised coronary models" to "in idealised and patient-based coronary models" and add `schultz2023ess,kandangwa2022rca` to that \cite. Do not add Pacheco there.

Suggested file-header comment: `% 2026-11-07 (reports/Recent lumen taper studies.md): after Johnston 2009, added Schultz 2023 (full text; referred, plaque-free CCTA; fixed outflow, no side branches, caveat kept in prose), Kandangwa 2022 (full text; n = 1 healthy MRI RCA; taper removal is a limitations-section sensitivity analysis), Pacheco 2021 (full text; n = 51 referred women, cross-sectional, absolute taper z-score; abstract misstates CFR result). Not used: Alamir 2024 (stenosed, QCA, surrogate attribution), Huo 2013 x2, Kang 2013, Tu 2021, Weng 2024, Wellnhofer 2010 (DOI unverified), Choi 2020 (-> Methods 05d).`

## (c) BibTeX

All three new entries were checked against Crossref (api.crossref.org) on 2026-11-07, for title, authors, journal, volume, issue and article number.

```bibtex
@article{kandangwa2022rca,
  title   = {Influence of right coronary artery motion, flow pulsatility and non-{N}ewtonian
             rheology on wall shear stress metrics},
  author  = {Kandangwa, Pratik and Torii, Ryo and Gatehouse, Peter D. and Sherwin, Spencer J.
             and Weinberg, Peter D.},
  journal = {Frontiers in Bioengineering and Biotechnology},
  volume  = {10},
  pages   = {962687},
  year    = {2022},
  doi     = {10.3389/fbioe.2022.962687},
  note    = {[VERIFIED] Crossref 2026-11-07. Full text: one healthy volunteer, 4-D MRI RCA;
             taper removal is a sensitivity analysis in the Limitations.}
}

@article{pacheco2021taper,
  title   = {Coronary atheroma burden predicts flow reserve in women with ischemia and
             nonobstructive coronary artery disease},
  author  = {Pacheco, C. and AlBadri, A. and Anderson, R. D. and Petersen, J. and Marpuri, S.
             and Cook-Wiens, G. and Pepine, C. J. and Mancini, G. B. J. and Bairey Merz, C. N.
             and Wei, J.},
  journal = {American Heart Journal Plus: Cardiology Research and Practice},
  volume  = {6},
  pages   = {100027},
  year    = {2021},
  doi     = {10.1016/j.ahjo.2021.100027},
  note    = {[VERIFIED] Crossref 2026-11-07. Full text PMC10976284: tapering z-scores correlated
             with CSS, not with CFR (abstract wording misleading).}
}

@article{choi2020allometric,
  title   = {Allometric scaling patterns among the human coronary artery tree, myocardial mass,
             and coronary artery flow},
  author  = {Choi, Jin-Ho and Kim, Eunsoo and Kim, Hyung Yoon and Lee, Seung-Hwa and
             Kim, Sung Mok},
  journal = {Physiological Reports},
  volume  = {8},
  number  = {14},
  pages   = {e14514},
  year    = {2020},
  doi     = {10.14814/phy2.14514},
  note    = {[VERIFIED] Crossref 2026-11-07 (article number e14514 from PMC7387886; Crossref
             lists no page). Optional, for Methods 05d.}
}
```

Replacement for the existing `schultz2023ess`. The current entry lists five authors and does not mark them as incomplete. Crossref lists 17 authors and dates the issue as online 2022, in print 2023 (volume 39, issue 2).

```bibtex
@article{schultz2023ess,
  title   = {Coronary computed tomography angiography-based endothelial wall shear stress in
             normal coronary arteries},
  author  = {Schultz, Jussi and van den Hoogen, Inge J. and Kuneman, Jurrien H. and
             de Graaf, Michiel A. and Kamperidis, Vasileios and Broersen, Alexander and
             Jukema, J. Wouter and Sakellarios, Antonis and Nikopoulos, Sotirios and
             Tsarapatsani, Konstantina and Naka, Katerina and Michalis, Lampros and
             Fotiadis, Dimitrios I. and Maaniitty, Teemu and Saraste, Antti and
             Bax, Jeroen J. and Knuuti, Juhani},
  journal = {The International Journal of Cardiovascular Imaging},
  volume  = {39},
  number  = {2},
  pages   = {441--450},
  year    = {2023},
  doi     = {10.1007/s10554-022-02739-0}
}
```

`refs.bib` already contains `johnston2007diameter`, `johnston2009taper`, `bijari2014flare`, `schultz2023ess`, `gijsen2019wss`, `seiler1992structure`, `han2022plaque` and `chen2024bridge`. It has no Kandangwa, Pacheco, Choi, Alamir or Gharleghi entry. `shen2026geometry` and `shen2025helical` are in `refs.bib`, but neither should be cited here.

## (d) Leave out, and why

**Diseased, stented or not about taper as an exposure.** Alamir 2024 uses stenosed QCA vessels, its ranking is a neural surrogate's attribution, and it repeats Johnston 2007. Kang 2013 and Shahzad 2013 use taper as the healthy reference for finding stenoses. They are useful at most in Methods or the Discussion as reverse-causation support. Tu 2021 and Weng 2024 are about step-down reference diameters for computing FFR. Schrauwen 2014 is about pressure drop, not WSS. The 2022 conical-stent paper and the MDPI 2026 parametric stenosis model concern treated or stenosed arteries, and their full texts were not read.

**Wrong level or direction.** Huo 2013 Radiology is tree-level and flags lumens that are too small, in metabolic syndrome. Huo 2013 Interface is in pigs, and the lumen is too wide after remodelling. Gong 2016 (pigs, heart failure), Chen 2015 (mice) and the Huo & Kassab 2016 review (abstract only) are left out for the same reasons. Choi 2020 belongs to Methods 05d. Skowronski 2018 gives normal point diameters, not slopes, and belongs to Methods as dominance and sex context.

**Longitudinal, but no taper.** Han 2022 (ICONIC, referred, existing plaque) is already in `sec:lit-risk`. Chen 2024 (bridged LADs, radiomics; no taper named in the main text, supplement unseen) is listed as still owed elsewhere. van Rosendael 2023 (PARADIGM) uses lumen volume, not taper.

**Unverified.** Wellnhofer 2010: DOI not verified, abstract seen only through a secondary listing, and no taper statement. Serafini 2025 and De Nisco 2021: full text not reached, and it is unknown whether taper was a descriptor.

**Preprints, flagged, never cite.** arXiv 1912.06075 (Denzinger), arXiv 2312.00257, Gharleghi arXiv 2401.12504 and Shen arXiv 2502.06161. **Excluded by rule:** `shen2026geometry` and its preprint arXiv 2507.17109.

**Content to keep out of the new sentences.** Leave out any statement that taper predicts plaque or that the thesis is the first to test it; that belongs to `sec:lit-risk` alone. Also leave out any expected sign, the Poiseuille relation and the scaling exponents (Methods 05c and 05d), and every number, including Pacheco's r values and Schultz's Pa values. Leave out the derived "flow-matched taper residual" arithmetic, which is the researchers' own inference and not a published result.
