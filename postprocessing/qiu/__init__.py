"""Stage 2 of Qiu et al. 2025 (CorSegRec), "vascular reconnection", as post-processing.

    Qiu, Shan, Wang, Dong, Wu, Yang, Hong, Shen. A topology-preserving three-stage
    framework for fully-connected coronary artery extraction. MedIA 103:103578 (2025).
    arXiv:2504.01597. No code has been released (github.com/YH-Qiu/CorSegRec holds
    only a readme), so this is a reimplementation from the paper text, section 3.3.

Modules, in the order the method uses them:

    skeleton.py    prediction component -> centerline branches, endpoints, directions
    classifier.py  the centerline classifier P (a cascade forest on two image patches)
    walk.py        the DPC (Distance-Probability-Cosine) walk, eqs. 6-11
    reconnect.py   candidate selection (types 1-3), evaluation (P + ADF), mask repair

Stage 1 (the NSDT soft-clDice training loss) is out of scope: the thesis does not
retrain the network. Stage 3 (INR lumen reconstruction) is replaced by a tube whose
radius is interpolated between the two joined ends. See docs_thesis/qiu_reconnection.md
for every deviation from the paper.
"""
