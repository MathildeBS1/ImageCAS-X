"""Per-vessel distributions of the simple measures (reads compute_simple.py's CSVs).

Reference limits: nonparametric 2.5th / 97.5th percentiles with 90 % CIs from the binomial
rank method (CLSI EP28-A3c style). Spearman rho with length L.
"""
import numpy as np
import pandas as pd
from scipy.stats import binom, mannwhitneyu, spearmanr

OUT = "/work3/s254124/imagecasx_results/tortuosity_research/simple"
COLS = ["L", "DM", "kappa_a5", "soam_ip", "soam", "n_infl", "icm", "nb45", "nb90", "nb180",
        "max_bend", "DM2_std", "nb45_2d", "nb90_2d", "DM2_mean", "DM2_best", "fs_std"]


def rank_ci(n, p, conf=0.90):
    """1-based order-statistic ranks (lo, hi) bracketing the p-quantile with >= conf coverage."""
    a = (1 - conf) / 2
    lo = int(binom.ppf(a, n, p))
    hi = int(binom.ppf(1 - a, n, p)) + 1
    return max(lo, 1), min(hi, n)


def ref(x):
    x = np.sort(x[np.isfinite(x)])
    n = len(x)
    out = {"n": n, "median": np.median(x), "q25": np.quantile(x, .25), "q75": np.quantile(x, .75),
           "p2.5": np.quantile(x, .025), "p97.5": np.quantile(x, .975), "p95": np.quantile(x, .95)}
    for p, k in ((0.025, "p2.5"), (0.975, "p97.5")):
        lo, hi = rank_ci(n, p)
        out[k + "_ci"] = f"[{x[lo - 1]:.3g}, {x[hi - 1]:.3g}]"
    return out


def main(tag=""):
    df = pd.read_csv(f"{OUT}/simple_measures{tag}.csv", dtype={"id": str})
    print(f"== tag '{tag}'; frame_ok false: {(df.frame_ok == False).sum()}, "
          f"missing vessels: {df[df.missing].groupby('vessel').size().to_dict()}")
    print(f"runtime per case: median {df.groupby('id').sec.first().median():.3f} s")
    d = df[~df.missing]
    rows = []
    for v in ["LM", "LAD", "LCX", "RCA"]:
        dv = d[d.vessel == v]
        for c in COLS:
            r = ref(dv[c].to_numpy(float))
            rho = spearmanr(dv[c], dv.L, nan_policy="omit")[0] if c != "L" else np.nan
            rows.append(dict(vessel=v, metric=c, rho_L=rho, **r))
    t = pd.DataFrame(rows)
    t.to_csv(f"{OUT}/summary{tag}.csv", index=False)
    with pd.option_context("display.width", 250, "display.max_rows", 200):
        print(t.round(3).to_string(index=False))
    print("\n-- prevalence of angiographic-style criteria (fraction of vessels)")
    for v in ["LAD", "LCX", "RCA"]:
        dv = d[d.vessel == v]
        eleid = np.select([dv.nb180 >= 2, dv.nb90_180 >= 3, dv.nb45_90 >= 3], [3, 2, 1], 0)
        print(f"{v}: >=3 bends>=45 3D {np.mean(dv.nb45 >= 3):.3f} | 2D std view {np.mean(dv.nb45_2d >= 3):.3f}"
              f" | >=2 bends>=180 3D {np.mean(dv.nb180 >= 2):.3f} | Eleid-like grade dist 0/1/2/3 "
              f"{np.bincount(eleid, minlength=4) / len(dv)}")
    pt = d[d.vessel.isin(["LAD", "LCX", "RCA"])].groupby("id")
    print(f"patient-level: any of LAD/LCX/RCA with >=3 bends>=45 (3D): {pt.apply(lambda g: (g.nb45 >= 3).any()).mean():.3f};"
          f" 2D: {pt.apply(lambda g: (g.nb45_2d >= 3).any()).mean():.3f}")
    print("\n-- dominance partitions (n) and DM / kappa_a medians, Mann-Whitney R vs L")
    for v in ["LAD", "LCX", "RCA"]:
        dv = d[d.vessel == v]
        for c in ["L", "DM", "kappa_a5", "nb45"]:
            g = {k: dv[dv.Dominance == k][c] for k in dv.Dominance.dropna().unique()}
            p = mannwhitneyu(g["R"], g["L"])[1] if "R" in g and "L" in g and len(g["L"]) > 2 else np.nan
            print(f"{v} {c}: " + ", ".join(f"{k} n={len(x)} med={x.median():.3g}" for k, x in sorted(g.items()))
                  + f"  p(R vs L)={p:.2g}")
    print("\n-- Image Quality: Spearman rho with measures")
    for v in ["LAD", "LCX", "RCA"]:
        dv = d[d.vessel == v]
        print(v, {c: round(spearmanr(dv[c], dv["Image Quality"], nan_policy="omit")[0], 2)
                  for c in ["DM", "kappa_a5", "soam_ip", "nb45"]})
    print("\n-- 2D vs 3D agreement (Spearman) per vessel")
    for v in ["LAD", "LCX", "RCA"]:
        dv = d[d.vessel == v]
        print(v, "DM2_std~DM", round(spearmanr(dv.DM2_std, dv.DM)[0], 2),
              "DM2_mean~DM", round(spearmanr(dv.DM2_mean, dv.DM)[0], 2),
              "nb45_2d~nb45", round(spearmanr(dv.nb45_2d, dv.nb45)[0], 2),
              "kappa~DM", round(spearmanr(dv.kappa_a5, dv.DM)[0], 2),
              "kappa~nb45", round(spearmanr(dv.kappa_a5, dv.nb45)[0], 2),
              "soam_ip~kappa", round(spearmanr(dv.soam_ip, dv.kappa_a5)[0], 2),
              "median foreshortening std view", round(dv.fs_std.median(), 3))
    print("\n-- normality of log(DM-1) and log kappa (skew)")
    for v in ["LAD", "LCX", "RCA"]:
        dv = d[d.vessel == v]
        print(v, "skew DM-1", round((dv.DM - 1).skew(), 2), "skew log(DM-1)", round(np.log(dv.DM - 1).skew(), 2),
              "skew kappa", round(dv.kappa_a5.skew(), 2), "skew log kappa", round(np.log(dv.kappa_a5).skew(), 2))


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "")
