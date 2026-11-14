# Phase 1: scope and research plan

Question: is the pooled segment-level cloglog GLMM (random person intercept, segment risks
pooled to a person risk) the right primary model for the thesis, and is there a better one?

Source of the model description: Thesis_coronary/content/technical/01_prediction_model.tex
(notes only; model marked "not yet confirmed"), plus Methods 03_prediction_model.tex and
04_model_size.tex.

## Already covered by earlier reports (not repeated, passed on as background)
- reports/Pooled segment GLMM background.md: how the model works
- reports/Models to beat pooled cloglog GLMM.md: neural and flexible challengers
- reports/Plaque risk model choice.md: regression vs XGBoost vs profile network
- reports/Neural networks for segment plaque.md
- reports/Geometry feature budget cloglog GLMM.md: parameter budget

So this round leaves machine learning out and asks the statistical question the earlier
reports did not: is this GLMM the best *regression* formulation?

## Three research strands (one researcher each, about 5 to 6 searches each)
1. Weaknesses of the model itself. Cloglog versus logit at this event rate, the
   log-length offset, the normal random intercept with few events per person, quadrature,
   marginal versus conditional prediction and calibration, the dilution of the block test
   in the person risk, sample size for clustered binary data.
2. Statistical alternatives. GEE or marginal models, beta-binomial, a person-level model
   on aggregated features, penalised or Bayesian hierarchical GLMM, segment-position
   random or fixed effects, interval-censored frailty survival. Evidence from simulation
   and methods papers on which predicts better with clustered binary data at this size.
3. Practice and expectations. What segment- or lesion-level coronary plaque studies
   (CCTA and IVUS) actually fit, and what TRIPOD-Cluster and prediction-model guidance
   expect, so the choice can be defended to examiners.

## Phases and pauses
- Phase 1 (this file): plan. PAUSE.
- Phase 2: research, one notes file per strand in this folder, plus 01_phase2_summary.md. PAUSE.
- Phase 3: report at reports/Pooled cloglog GLMM evaluation.md.
