"""Summaries of cohort_train<n>.csv.  python -m tortuosity.research.unified.analyze [--n 150]

ICC(2,1) absolute agreement. Jitter families: the 3 replicates (orig excluded), as in the earlier
P100 analysis, plus 'vs orig' = (orig, rep 0), which also charges the additive noise bias.
Truncation: (orig, trunc20). 95 % CI: 1000 bootstrap resamples of vessels, seed 0.
"""
import argparse

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

OUT = "/work3/s254124/imagecasx_results/tortuosity_research/unified"
MAIN = ["arc_chord", "ka5", "kB", "kB_course", "kB_wiggle", "kB_twist", "f_twist", "f_wiggle"]


def icc(Y):
    Y = Y[~np.isnan(Y).any(1)]
    n, k = Y.shape
    g = Y.mean()
    ssr = k * ((Y.mean(1) - g) ** 2).sum(); ssc = n * ((Y.mean(0) - g) ** 2).sum()
    sse = ((Y - g) ** 2).sum() - ssr - ssc
    msr, msc, mse = ssr / (n - 1), ssc / (k - 1), sse / ((n - 1) * (k - 1))
    return (msr - mse) / (msr + (k - 1) * mse + k * (msc - mse) / n)


def ci(Y, B=1000):
    Y = Y[~np.isnan(Y).any(1)]
    rng = np.random.default_rng(0)
    b = [icc(Y[rng.integers(0, len(Y), len(Y))]) for _ in range(B)]
    return f"{icc(Y):.2f} [{np.percentile(b, 2.5):.2f},{np.percentile(b, 97.5):.2f}]"


def main(n):
    d = pd.read_csv(f"{OUT}/cohort_train{n}.csv")
    o = d[d.family == "orig"].set_index(["case", "vessel"])
    pr = lambda *a: print(*a)
    pr(f"# sample: first {n} train ids; vessels measurable per name:",
       o.groupby("vessel")["kB"].count().to_dict())
    pr("\n## A. distributions on orig (median [IQR])")
    for v in ("LAD", "LCX", "RCA"):
        x = o.xs(v, level="vessel")
        pr(f"{v}: " + "; ".join(f"{m} {x[m].median():.4g} [{x[m].quantile(.25):.3g},{x[m].quantile(.75):.3g}]"
                                for m in ["length"] + MAIN))
    pr("\n## B. ICC(2,1) with bootstrap CI, per vessel")
    for fam in ("iid006", "iid05", "corr05", "trunc20"):
        pr(f"### {fam}")
        for m in MAIN:
            cells = []
            for v in ("LAD", "LCX", "RCA"):
                x = d[d.vessel == v]
                pv = x.pivot_table(index="case", columns=["family", "rep"], values=m, dropna=False)
                if fam == "trunc20":
                    cells.append(ci(np.c_[pv["orig"].iloc[:, 0], pv[fam].iloc[:, 0]]))
                else:
                    reps = pv[fam].values
                    cells.append(f"{ci(reps)} vs-orig {icc(np.c_[pv['orig'].iloc[:, 0], reps[:, 0]]):.2f}")
            pr(f"  {m:16s} " + " | ".join(cells))
    pr("\n## C. median relative change perturbed/orig - 1 (LAD/LCX/RCA)")
    for fam in ("iid006", "iid05", "corr05", "trunc20"):
        cells = []
        for m in MAIN:
            r = []
            for v in ("LAD", "LCX", "RCA"):
                x = d[(d.vessel == v)]
                pv = x.pivot_table(index="case", columns=["family", "rep"], values=m)
                r.append(np.nanmedian(pv[fam].iloc[:, 0] / pv["orig"].iloc[:, 0] - 1))
            cells.append(f"{m} " + "/".join(f"{q:+.0%}" for q in r))
        pr(f"  {fam}: " + "; ".join(cells))
    pr("\n## D. Spearman on orig (LAD/LCX/RCA): with length, arc_chord, ka5")
    for m in MAIN:
        c = []
        for ref in ("length", "arc_chord", "ka5"):
            c.append(ref + " " + "/".join(f"{spearmanr(o.xs(v, level='vessel')[m], o.xs(v, level='vessel')[ref], nan_policy='omit')[0]:+.2f}"
                                           for v in ("LAD", "LCX", "RCA")))
        pr(f"  {m:16s} " + "; ".join(c))
    pr("\n## E. sensitivity of kB_wiggle, f_twist to lam_c and W: Spearman vs default (LAD/LCX/RCA)")
    for tag in ("lc15", "lc30", "w10", "w2"):
        for m in ("kB_wiggle", "f_twist", "kB_course"):
            pr(f"  {m}@{tag}: " + "/".join(f"{spearmanr(o.xs(v, level='vessel')[f'{m}@{tag}'], o.xs(v, level='vessel')[m], nan_policy='omit')[0]:.2f}"
                                             for v in ("LAD", "LCX", "RCA"))
               + "   median " + "/".join(f"{o.xs(v, level='vessel')[f'{m}@{tag}'].median():.3g}" for v in ("LAD", "LCX", "RCA")))
    pr("\n## F. does the decomposition add information beyond ka5? rank-regress each part on ka5 + log length, residual share")
    for m in ("kB", "kB_course", "kB_wiggle", "f_twist", "f_wiggle", "kB_twist"):
        cells = []
        for v in ("LAD", "LCX", "RCA"):
            x = o.xs(v, level="vessel")[[m, "ka5", "length"]].dropna().rank()
            X = np.c_[np.ones(len(x)), x["ka5"], x["length"]]
            beta, *_ = np.linalg.lstsq(X, x[m].values, rcond=None)
            res = x[m].values - X @ beta
            cells.append(f"{1 - res.var() / x[m].var():.2f}")
        pr(f"  {m:14s} rank R^2 on (ka5, length): " + "/".join(cells))
    pr("\n## G. runtime: bcs, ms per vessel (orig): median "
       f"{o['t_bcs_ms'].median():.1f}, max {o['t_bcs_ms'].max():.1f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=150)
    main(ap.parse_args().n)
