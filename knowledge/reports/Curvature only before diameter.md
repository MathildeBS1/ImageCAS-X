# Start curvature-only, with diameter as the planned second arm

**Build the first small sequence model on the curvature profile alone, but design its input as a multi-channel tensor from day one and register curvature-only against curvature-plus-diameter as a planned comparison.** Diameter is not an optional later extra: it is the candidate second channel with the strongest outcome evidence, and the curvature-only versus multi-channel ablation has never been published for any vascular bed ([Expanding report](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Expanding%20local%20tortuosity%20vector%20features.md)). The curvature-only model is therefore one half of a result, not a throwaway prototype. The case for ordering it first is practical: it replicates the only published profile-versus-scalar contrast, it isolates pipeline bugs, and it avoids feeding the network a channel whose measurement error on CAS-Net output is still unknown. The case against waiting long is that diameter may carry most of the signal, and it brings a size confound that has to be handled by covariates fixed from the first model onward.

## Curvature-only is the baseline the literature actually supplies

Tello Ayala et al.'s transformer reading the per-point RCA curvature profile reached AUROC 0.67 (95% CI 0.65 to 0.69), against 0.60 (0.58 to 0.63) for logistic regression on the same metric's patient-level mean ([PMC13308244](https://pmc.ncbi.nlm.nih.gov/articles/PMC13308244/)). Both arms use one geometric channel, so the gap is a representation effect, not a feature-count effect. A curvature-only profile model on ImageCAS-X is the direct analogue of that comparison, and it is the fair single-feature baseline against which any added channel must be judged; comparing a two-channel model against a scalar mean would overstate what the second channel contributes ([Feature count report](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Tortuosity%20feature%20count%20for%20CAD%20prediction.md)).

One channel also makes the first model debuggable. Arc-length resampling, sequence alignment from the ostium, padding and masking of short vessels, and fold assignment in cross-validation are all new code. Errors in any of them are easy to see when the input is a single curve and hard to separate from channel scaling or redundancy when it is two.

## Diameter needs its own measurement check before it enters the model

Curvature depends only on the centerline. Diameter needs a radius estimate from the segmentation, and distal RCA radii are around 1 to 1.5 mm, which is only two to three voxels at the 0.5 mm cache resolution. Voxel quantization and boundary errors in the CAS-Net prediction are therefore a larger fraction of the quantity being measured for diameter than for curvature. The agreement between reference and CAS-Net-derived features on the 160 test scans has not been measured for any descriptor yet, and it is already item 5 in the priority list ([Priorities report](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Investigation%20priorities%20across%20reports.md)). Adding diameter as a channel before that agreement is known would leave no way to tell a real diameter effect from segmentation error. The natural order is to extend the item 5 agreement study to radius, then add the channel.

## Waiting too long for diameter risks understating the geometry

Diameter has more direct outcome evidence than any other candidate channel. In an RCA-specific FFR-CT study, vessels with FFRCT ≤ 0.80 had smaller proximal (3.9 vs 4.6 mm) and distal (2.4 vs 2.9 mm) diameters, and proximal diameter was an independent multivariable predictor ([PMC10873436](https://pmc.ncbi.nlm.nih.gov/articles/PMC10873436/)). In 39 ASOCA trees, diameter was the only geometric correlate of wall shear stress that survived multiple-comparison correction ([Shen et al. 2025, arXiv 2502.06161](https://arxiv.org/abs/2502.06161)). If diameter carries most of the signal, a curvature-only model reported alone would make the geometric approach look weaker than the data support.

Adding the channel is cheap in parameters. In GRU, LSTM or transformer encoders the channel count only widens the input projection, which is a small fraction of the total parameter count ([Expanding report](file:///zhome/e2/6/224426/project/ImageCAS-X/reports/Expanding%20local%20tortuosity%20vector%20features.md)). The real cost is confounding: diameter scales with heart size and sex, which is exactly the "heart size, dominance, number of branches" axis a supervisor predicted learned representations would separate on ([supervisor emails](file:///zhome/e2/6/224426/project/ImageCAS-X/from_superviser.tex)). Age, sex and dominance should therefore enter the first curvature-only model as covariates, so that the second arm changes only one thing.

## Sample size and blinding constrain the design more than channel choice

ImageCAS-X has 800 scans. In the one benchmarking study found that measured convergence directly, neural networks needed around N ≈ 1500 to stabilise, and at N ≤ 300 up to 70% of cross-validated results exceeded AUC 0.61 for a model with no true signal ([PMC11655521](https://pmc.ncbi.nlm.nih.gov/articles/PMC11655521/)). The network must be small, evaluated with nested or repeated cross-validation, and always reported beside the logistic-regression-on-mean baseline. If the label is the `Descriptors.xlsx` Disease column, the model, channels, covariates and the two-arm comparison should be written down and dated before any AUROC is seen. The priorities report records that the Disease column was already looked at in an earlier session, and the pre-registration should say so rather than claim a clean blind.

## A concrete order of work

1. Build the sequence input as `[B, C, L]` with a channel list, age, sex and dominance as late-fused covariates, and the logistic-regression-on-mean baseline in the same evaluation loop.
2. Train and evaluate the curvature-only arm (C = 1).
3. Extend the reference-versus-CAS-Net agreement study (ICC, Bland-Altman) to per-point radius.
4. Run a Spearman correlation check between curvature and diameter profiles inside each training fold, following the carotid pruning precedent ([arXiv 2607.14195](https://arxiv.org/html/2607.14195)).
5. Train and evaluate the curvature-plus-diameter arm (C = 2) with identical folds, covariates and hyperparameters, and report both arms.

Torsion stays out of both arms; if tested at all, it is a separately reported third arm.

## Conclusion

Curvature-only first is the right order, not because diameter is less important but because the curvature profile is the published baseline, the simpler model exposes pipeline errors, and diameter's measurement error on CAS-Net output is still unmeasured. Framing the two as arms of one pre-registered comparison turns the order of work into a contribution: the curvature-only versus multi-channel ablation for coronary CAD is an open gap. Two things outrank the channel decision. The 800-scan cohort sits below where neural networks have been shown to stabilise, and the priority list places reproducibility, Herlev-Østerbro access and the extractor agreement study ahead of new modelling, so this model should not take time from those.
