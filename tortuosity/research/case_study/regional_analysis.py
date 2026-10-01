"""Which regional descriptors carry information beyond kappa_a5? (560 training RCAs or LADs)

Reads $OUT/regional_train560.csv (regional.py train) and only the Dominance and Image Quality
columns of Descriptors.xlsx. Per region: distribution, floor fraction, correlation with length,
dominance and Image Quality, redundancy with kappa_a5, and the share of each descriptor's rank
variance not explained by (kappa_a5, vessel length). Across regions: how independent the
regional kappa_a5 values are.

Run: source env.sh && python tortuosity/research/case_study/regional_analysis.py [lad]
Writes $OUT/regional[_lad]_train560_analysis.txt.
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, rankdata, spearmanr

DATA = os.environ["ImageCAS_X_data_path"]
OUT = "/work3/s254124/imagecasx_results/tortuosity_research/case_study"
DESC = ("arc_chord", "arc_chord_2D", "kappa_a5", "total_turning_deg", "bends_ge45", "bends_ge90",
        "max_bend_deg", "ti10_mean", "kB", "f_twist", "f_wiggle")


def rank_r2(y, X):
    """R^2 of the rank of y on the ranks of the columns of X (ordinary least squares)."""
    Y = rankdata(y)
    A = np.c_[np.ones(len(Y)), np.column_stack([rankdata(x) for x in X])]
    res = Y - A @ np.linalg.lstsq(A, Y, rcond=None)[0]
    return 1 - res.var() / Y.var()


def main(tag):
    REGIONS = ("whole", "whole_trim", "proximal", "mid", "distal") if tag else \
        ("whole", "proximal", "proximal_trim", "mid", "crux")
    df = pd.read_csv(f"{OUT}/regional{tag}_train560.csv", dtype={"id": str})
    if "crux_ok" not in df:
        df["crux_ok"] = True
    dsc = pd.read_excel(f"{DATA}/Descriptors.xlsx", usecols=["Scan ID", "Image Quality", "Dominance"])
    dsc["id"] = dsc["Scan ID"].astype(str)
    df = df.merge(dsc[["id", "Image Quality", "Dominance"]], on="id", how="left")
    lines = []
    p = lines.append

    w = df[df.region == "whole"]
    p(f"scans {df.id.nunique()}; whole rows with values {w.kappa_a5.notna().sum()}")
    if tag:
        p(f"first branch found {w.b1_mm.notna().sum()}, second used as mid end {int(w.b2_used.sum())}; "
          f"first take-off median {w.b1_mm.median():.1f} mm (IQR {w.b1_mm.quantile(.25):.1f} to {w.b1_mm.quantile(.75):.1f})")
        p("first branch found by dominance:\n" + w.groupby("Dominance").b1_mm.agg(lambda x: f"{x.notna().sum()}/{len(x)}").to_string())
    else:
        p("crux_ok (RCA ends at R-PDA/R-PLA) by dominance:")
        p(w.groupby("Dominance").crux_ok.agg(["sum", "count"]).to_string())
    p("rows skipped: " + df[df.reason.fillna("") != ""].groupby(["region", "reason"]).size().to_string())

    for reg in REGIONS:
        d = df[(df.region == reg) & df.kappa_a5.notna()]
        if reg == "crux":
            d = d[d.crux_ok]
        p(f"\n==== {reg}  n = {len(d)}  length median {d.length_mm.median():.1f} mm")
        p(f"{'descriptor':18s} {'median':>8s} {'IQR':>17s} {'p2.5':>8s} {'p97.5':>8s} {'floor%':>6s} "
          f"{'rho_len':>7s} {'rho_ka':>7s} {'R2|ka,len':>9s} {'domR_vs_L/C p':>13s} {'rho_IQ':>6s}")
        for c in DESC:
            x = d[c].astype(float)
            q = x.quantile([.25, .5, .75, .025, .975])
            floor = (x == 0).mean() * 100
            r_len = spearmanr(x, d.vessel_length_mm)[0]
            r_ka = spearmanr(x, d.kappa_a5)[0]
            r2 = rank_r2(x, [d.kappa_a5, d.vessel_length_mm]) if c != "kappa_a5" else rank_r2(x, [d.vessel_length_mm])
            pd_ = mannwhitneyu(x[d.Dominance == "R"], x[d.Dominance != "R"]).pvalue
            r_iq = spearmanr(x, d["Image Quality"])[0]
            p(f"{c:18s} {q[.5]:8.3f} {q[.25]:8.3f}-{q[.75]:<8.3f} {q[.025]:8.3f} {q[.975]:8.3f} {floor:6.1f} "
              f"{r_len:7.2f} {r_ka:7.2f} {r2:9.2f} {pd_:13.1e} {r_iq:6.2f}")
        # redundancy among descriptors, |rho| >= 0.85
        C = d[list(DESC)].astype(float).corr(method="spearman")
        pairs = [(a, b, C.loc[a, b]) for i, a in enumerate(DESC) for b in DESC[i + 1:] if abs(C.loc[a, b]) >= 0.85]
        p("redundant pairs |rho| >= 0.85: " + ("; ".join(f"{a}~{b} {r:.2f}" for a, b, r in pairs) or "none"))

    p("\n==== kappa_a5 across regions (Spearman, scans with all regions; crux only if crux_ok)")
    k = df[df.kappa_a5.notna()].pivot(index="id", columns="region", values="kappa_a5")
    ok = set(w[w.crux_ok].id)
    k = k[k.index.isin(ok)].dropna()
    p(f"n = {len(k)}")
    p(k[list(REGIONS)].corr(method="spearman").round(2).to_string())
    p("\n==== f_twist and kB across regions (Spearman, same scans)")
    for c in ("f_twist", "kB", "arc_chord"):
        t = df.pivot(index="id", columns="region", values=c).loc[k.index, list(REGIONS)]
        p(f"{c}:\n" + t.corr(method="spearman").round(2).to_string())
    p("\n==== f_twist vs kB within region (does f_twist blow up where bending is small?)")
    for reg in REGIONS[2:]:
        d = df[(df.region == reg) & df.kB.notna()]
        lo = d.kB <= d.kB.quantile(.25)
        p(f"{reg:14s} rho(f_twist,kB) {spearmanr(d.f_twist, d.kB)[0]:.2f}; f_twist median lowest-kB quartile "
          f"{d.f_twist[lo].median():.2f} vs rest {d.f_twist[~lo].median():.2f}")

    open(f"{OUT}/regional{tag}_train560_analysis.txt", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main(f"_{sys.argv[1]}" if sys.argv[1:] else "")
