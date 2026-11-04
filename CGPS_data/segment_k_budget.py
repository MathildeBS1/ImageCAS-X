"""How many curvature FPCA scores (K, each with its own weight) can each of the 9 per-segment models carry?

    python CGPS_data/segment_k_budget.py [--bl BL_FILE] [--fu FU_FILE] [--base-df 1] [--out MD]

One model per trunk segment (plad mlad dlad pcx mcx dcx prca mrca drca), one row per plaque-free
participant (BL ct_cag_sis == 0 and ct_cag_sss == 0): did this segment have plaque at FU (decoded
stenosis minimal or worse)? Predictors would be the base (--base-df, default 1 = recalibrated SCORE2)
and the segment's own K FPCA scores; no other geometry. Only the outcome counts are read here, no
geometry, so nothing is linked yet.

Per segment: n graded at FU, events, and the largest number of parameters by Riley et al. 2020
criteria (i) (expected shrinkage S >= 0.9) and (ii) (optimism in Nagelkerke R2 <= 0.05), with R2_CS from
an anticipated C by the binormal conversion of Riley, Van Calster & Collins 2021 (as in
research_notes/Geometry feature budget cloglog GLMM/budget_sim.py). K_max = floor(P_max) - base df.
Criterion (iii) (mean risk within 0.05) is checked. Events/10 and /15 are shown for comparison.
Aggregates only (counts 1-4 hidden, and the K that would reveal them).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from scipy import optimize, stats
from scipy.special import expit, logit

from cgps_stats import BL_PATH, FU_PATH, MIN_CELL, OUT_DIR, count, count_of, decode_segments, load, num, pct
from clean_baseline_count import read_at_bl

SEGS = ("plad", "mlad", "dlad", "pcx", "mcx", "dcx", "prca", "mrca", "drca")
C_VALUES = (0.65, 0.70, 0.75)


def r2cs_from_c(C, phi, nodes=200):
    """Binormal conversion: LP ~ N(mu, 1) in events and N(0, 1) in non-events, mu = sqrt(2) Phi^-1(C);
    a logistic model of y on LP fitted to the whole population (by quadrature), R2_CS = 1 - exp(-LR/n)."""
    mu = np.sqrt(2) * stats.norm.ppf(C)
    x, w = np.polynomial.hermite_e.hermegauss(nodes)
    w = w / w.sum()

    def nll(t):
        a, b = t
        return -(phi * np.sum(w * np.log(expit(a + b * (x + mu))))
                 + (1 - phi) * np.sum(w * np.log(expit(-(a + b * x)))))

    res = optimize.minimize(nll, [logit(phi), 1.0], method="Nelder-Mead",
                            options=dict(xatol=1e-10, fatol=1e-13, maxiter=5000))
    l_null = phi * np.log(phi) + (1 - phi) * np.log(1 - phi)
    return 1 - np.exp(-2 * (-res.fun - l_null))


def pmax(n, r2, phi):
    """Largest P meeting Riley criteria (i) S = 0.9 and (ii) optimism <= 0.05: n = P / ((S - 1) ln(1 - R2/S))."""
    l_null = phi * np.log(phi) + (1 - phi) * np.log(1 - phi)
    s_vh = r2 / (r2 + 0.05 * (1 - np.exp(2 * l_null)))
    return min(n * (S - 1) * np.log(1 - r2 / S) for S in (0.9, s_vh))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bl", default=BL_PATH)
    ap.add_argument("--fu", default=FU_PATH)
    ap.add_argument("--base-df", type=int, default=1, help="1 = recalibrated SCORE2; 6 = refitted factors")
    ap.add_argument("--out", default=str(Path(OUT_DIR) / "segment_k_budget.md"))
    args = ap.parse_args()

    bl = load(args.bl).drop_duplicates("study_id").set_index("study_id")
    fu = load(args.fu).drop_duplicates("study_id").set_index("study_id")
    fu, _ = decode_segments(fu)
    clean = (num(bl["ct_cag_sis"]) == 0) & (num(bl["ct_cag_sss"]) == 0)
    ids = clean[clean].index.intersection(fu.index)
    n_read = int(read_at_bl(bl).loc[ids].sum())

    head = ["segment", "n graded", "events", "% events", "events/10", "events/15",
            *[f"K_max C={c:.2f}" for c in C_VALUES], "mean risk ±0.05"]
    rows = []
    for s in SEGS:
        g = num(fu.loc[ids, f"ct_cag_{s}_stenosis"]).dropna()
        n, k = len(g), int((g >= 1).sum())
        shown = count_of(k, n)
        if not isinstance(shown, int) or min(k, n - k) < MIN_CELL:  # K would give the hidden count away
            rows.append([s, count(n), shown, pct(k, n), "", "", *[""] * len(C_VALUES), ""])
            continue
        phi = k / n
        ks = [int(np.floor(pmax(n, r2cs_from_c(c, phi), phi))) - args.base_df for c in C_VALUES]
        ok = n >= (1.96 / 0.05) ** 2 * phi * (1 - phi)
        rows.append([s, n, k, pct(k, n), k // 10 - args.base_df, k // 15 - args.base_df,
                     *[max(x, 0) for x in ks], "met" if ok else "not met"])

    rep = ["# Curvature scores per segment model: parameter budget\n",
           f"Plaque-free at BL with a FU row: {count(len(ids))} (read at BL: {count(n_read)}). "
           "An event is plaque (minimal or worse) in that segment at FU; n counts the segments graded at FU. "
           f"Base: {args.base_df} df. K_max = largest P by Riley criteria (i) and (ii) minus the base df, "
           "at three anticipated C of the segment model; events/10 and /15 minus the base df for comparison. "
           "No image-quality exclusion yet. The outcome-blind shape count (turning_profile_shapes.md) caps K "
           "from the other side: K = min(shapes that pass, K_max).\n",
           "| " + " | ".join(head) + " |", "|" + "---|" * len(head),
           *["| " + " | ".join(str(v) for v in r) + " |" for r in rows], ""]
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(rep))
    print("\n".join(rep))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
