"""Known-groups check of the curvature: is the tracer curvature higher with long-standing hypertension?

    python CGPS_data/thesis_final/hypertension_curvature.py [--limit N] [--boot 2000] [--out MD]
    python CGPS_data/thesis_final/hypertension_curvature.py --check   # synthetic numbers, needs no data

Coronary tortuosity is reported to be higher with hypertension, so a curvature that measures the bending of the
artery should be higher in hypertensive people. Rerun of hypertension_tortuosity.py (git 449e6ae, Medis trees,
almost all with plaque: no separation) on the cohort's own curvature and the plaque-free cohort. Set 2026-11-25,
before the tracer cohort is linked to the outcome.

Design, fixed before the run so that the expected direction gets its best fair chance:
  cohort      plaque-free baseline (BL ct_cag_sis == 0 and ct_cag_sss == 0) with both pruned BL tracer files.
  groups      hypertension is recorded at each visit, so the two visits pick out the extremes.
              long-standing hypertension: at BL clin_bp_sys_mean >= 140 or clin_bp_dia_mean >= 90 or
                med_antihypertensive_any, and at FU demo_hypertension_deriv == 1.
              normotensive: at BL no antihypertensive and sys < 130 and dia < 85, and at FU
                demo_hypertension_deriv == 0.
              Everyone else (status changed, borderline BL pressure, missing) is left out and counted.
  curvature   per artery the cohort's whole-artery mean, curvature_feature.artery_curvature over (0, end) as in
              medis_compare.tree_features, on the BL trees only. The tree average is the mean of the LAD, LCx and
              RCA values after z-scoring each artery over the people in the check (people with all three values
              only).
  primary     one test: BL tree average, one-sided (higher with hypertension). OR per SD of curvature from a
              logistic regression of group on curvature, age, sex and BSA (Wald 95% CI, one-sided p), and the AUC
              with a bootstrap 95% CI. The single arteries are estimates beside it, not further tests.
No FU scans and no plaque outcome are used (2026-11-25): FU enters only through demo_hypertension_deriv.

Plots (one dot per participant, allowed off the server: user, 2026-11-25), in the thesis colours, BL curvature by
group with each panel's one-sided p: the tree average alone (hypertension_curvature_combined.png, main text) and
the LAD, LCx and RCA side by side (hypertension_curvature_arteries.png, appendix), written to --rows (default <OUT_DIR>/hypertension_curvature). Writes
hypertension_curvature.md next to this script: aggregates only, counts 1-4 shown as <5, statistics only from
groups of MIN_CELL, medians only from QUARTILE_MIN (cgps_stats).
"""
import argparse
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm, rankdata

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "Thesis_coronary" / "setup"))
from figure_colours import GRID, INK, INK2, SERIES  # noqa: E402  (the thesis colour scheme)

ARTERIES = ("LAD", "CX", "RCA")
PANELS = {"LAD": "LAD", "CX": "LCx", "RCA": "RCA", "avg": "tree average"}
GROUPS = ("normotensive", "hypertension")
GROUP_LABEL = {"normotensive": "Normotensive", "hypertension": "Long-standing hypertension"}
TITLE = {"LAD": "LAD", "CX": "LCx", "RCA": "RCA", "avg": "LAD, LCx and RCA combined"}
COLOR = dict(zip(GROUPS, SERIES[:2]))  # first two series colours of the thesis scheme
HTN_SYS, HTN_DIA = 140, 90  # BL hypertension
NORMO_SYS, NORMO_DIA = 130, 85  # BL normotensive: below both
COVARIATES = ("scan_age", "male", "clin_bsa")


# ---------------------------------------------------------------- groups

def hypertension_group(sys_, dia, med, fu):
    """(group, reason) per person: long-standing hypertension, normotensive, or None with why it is left out.
    sys_, dia: BL mmHg; med: BL antihypertensive 0/1; fu: FU demo_hypertension_deriv 0/1 (nan = unknown)."""
    h_bl = (sys_ >= HTN_SYS) | (dia >= HTN_DIA) | (med == 1)
    n_bl = (med == 0) & (sys_ < NORMO_SYS) & (dia < NORMO_DIA)  # nan compares False: all three must be known
    group = pd.Series(None, index=sys_.index, dtype=object)
    group[h_bl & (fu == 1)] = "hypertension"
    group[n_bl & (fu == 0)] = "normotensive"
    reason = pd.Series("ok", index=sys_.index, dtype=object)
    out = group.isna()
    reason[out & ((h_bl & (fu == 0)) | (n_bl & (fu == 1)))] = "status changed between the visits"
    reason[out & ~h_bl & ~n_bl & fu.notna() & (sys_.notna() | dia.notna())] = "borderline or incomplete BL pressure"
    reason[out & ~h_bl & ~n_bl & (fu == 1) & (sys_ < HTN_SYS) & (dia < HTN_DIA)] = "status changed between the visits"
    reason[out & (reason == "ok")] = "missing"
    return group, reason


# ---------------------------------------------------------------- statistics

def auc(x, y):
    """P(a hypertensive value > a normotensive one), ties count half: x hypertensive, y normotensive."""
    r = rankdata(np.r_[x, y])
    return (r[:len(x)].sum() - len(x) * (len(x) + 1) / 2) / (len(x) * len(y))


def auc_ci(x, y, boot=2000, seed=0):
    """(AUC, 95% bootstrap interval, each group resampled on its own)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    rng = np.random.default_rng(seed)
    b = [auc(rng.choice(x, len(x)), rng.choice(y, len(y))) for _ in range(boot)]
    return auc(x, y), (np.percentile(b, [2.5, 97.5]) if boot else (np.nan, np.nan))


def logistic(X, y, iters=50):
    """(beta, SE) of a logistic regression by Newton-Raphson; X holds the intercept column."""
    beta = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ beta))
        H = X.T @ (X * (p * (1 - p))[:, None])
        step = np.linalg.solve(H, X.T @ (y - p))
        beta += step
        if np.abs(step).max() < 1e-10:
            break
    p = 1 / (1 + np.exp(-X @ beta))
    return beta, np.sqrt(np.diag(np.linalg.inv(X.T @ (X * (p * (1 - p))[:, None]))))


def adjusted_or(d, col):
    """OR per SD of d[col] for hypertension, adjusted for age, sex and BSA: (OR, lo, hi, one-sided p, n)."""
    d = d.dropna(subset=[col, *COVARIATES])
    if d["group"].nunique() < 2:
        return None
    z = (d[col] - d[col].mean()) / d[col].std(ddof=1)
    cov = [(d[c] - d[c].mean()) / (d[c].std(ddof=1) or 1) for c in COVARIATES]
    X = np.column_stack([np.ones(len(d)), z, *cov])
    beta, se = logistic(X, (d["group"] == "hypertension").to_numpy(float))
    b, s = beta[1], se[1]
    return np.exp(b), np.exp(b - 1.96 * s), np.exp(b + 1.96 * s), norm.sf(b / s), len(d)


def tree_average(R):
    """Column avg: the mean of the three artery values, each z-scored over the rows."""
    R = R.copy()
    for a in ARTERIES:
        R[f"z_{a}"] = (R[a] - R[a].mean()) / R[a].std(ddof=1)
    R["avg"] = R[[f"z_{a}" for a in ARTERIES]].mean(axis=1, skipna=False)
    return R


# ---------------------------------------------------------------- data run (server)

def run(limit=None):
    """(flow, one row per participant with BL curvature: id, group, covariates, LAD, CX, RCA)."""
    import hoe10y_qc as hq
    import tracer_io
    from cgps_stats import BL_PATH, FU_PATH, load, num, yes
    from curvature_feature import CHORD, artery_curvature
    from split_trunks import graph, split

    bl, fu = (load(p).pipe(lambda df: df.assign(id=df["study_id"].map(hq.norm_id)))
              .drop_duplicates("id").set_index("id") for p in (BL_PATH, FU_PATH))
    fu = fu.reindex(bl.index)
    clean = (num(bl["ct_cag_sis"]) == 0) & (num(bl["ct_cag_sss"]) == 0)
    group, reason = hypertension_group(num(bl["clin_bp_sys_mean"]), num(bl["clin_bp_dia_mean"]),
                                       yes(bl["med_antihypertensive_any"]), yes(fu["demo_hypertension_deriv"]))

    flow = Counter()
    flow["BL participants"] = len(bl)
    flow["plaque-free at BL"] = int(clean.sum())
    have = tracer_io.tracer_ids(visit="BL")
    ids = sorted((i for i in bl.index[clean] if i in have), key=int)[:limit]
    flow["with BL tracer centerlines"] = len(ids)
    for r, n in reason[ids].value_counts().items():
        flow[f"left out: {r}" if r != "ok" else "in a hypertension group"] = n
    ids = [i for i in ids if pd.notna(group[i])]  # pandas may store the missing group as None or nan
    for g in GROUPS:
        flow[f"  {g}"] = sum(group[i] == g for i in ids)

    rows, fails = [], Counter()
    for pid in ids:
        row = {"id": pid, "group": group[pid], **{c: num(bl[c]).get(pid) for c in COVARIATES}}
        try:
            arts = split(*graph(tracer_io.tracer_tree(pid, visit="BL")), roots=tracer_io.tracer_ostia(pid, visit="BL"))
            T = {a: artery_curvature(Y, s, (0.0, end), CHORD)[0] for a, (_, _, end, _, Y, s) in arts.items()}
        except Exception as ex:  # noqa: BLE001 - counted
            fails[f"error:{type(ex).__name__}"] += 1
            T = {}
        rows.append(row | {a: T.get(a, np.nan) for a in ARTERIES})
    for r, n in fails.items():
        flow[f"BL trees that could not be divided ({r})"] = n
    return flow, tree_average(pd.DataFrame(rows))


# ---------------------------------------------------------------- report

def report(flow, R, boot=2000):
    from cgps_stats import MIN_CELL, QUARTILE_MIN, count

    def fmt(x, nd=3):
        return "-" if x is None or not np.isfinite(x) else f"{x:.{nd}g}"

    def mediqr(x):
        return f"{fmt(np.median(x))} ({fmt(np.percentile(x, 25))}-{fmt(np.percentile(x, 75))})" \
            if len(x) >= QUARTILE_MIN else ""

    L = ["# Curvature by long-standing hypertension: known-groups check (hypertension_curvature.py)\n",
         ("Plaque-free baseline cohort, BL tracer curvature (whole-artery mean, 1/mm; tree average in z units). "
          f"Long-standing hypertension: BL sys >= {HTN_SYS} or dia >= {HTN_DIA} or antihypertensive, and FU "
          f"demo_hypertension_deriv. Normotensive: BL no antihypertensive, sys < {NORMO_SYS} and dia < {NORMO_DIA}, "
          "and not hypertensive at FU. Expected before the run: higher curvature with hypertension (OR > 1, "
          f"AUC > 0.5). Primary: BL tree average. Counts 1-4 shown as <5; statistics only from {MIN_CELL} per "
          "group.\n"),
         "## Flow\n", "| step | participants |", "|---|---|"]
    L += [f"| {k} | {count(v)} |" for k, v in flow.items()]

    L += ["\n## Curvature by group\n",
          "| panel | n normo | n hyp | median (IQR) normo | median (IQR) hyp | AUC (95% CI) | "
          "OR per SD, adj. (95% CI) | one-sided p |",
          "|---|---|---|---|---|---|---|---|"]
    for col, name in PANELS.items():
        x = R.loc[R["group"] == "hypertension", col].dropna().to_numpy(float)
        y = R.loc[R["group"] == "normotensive", col].dropna().to_numpy(float)
        lead = f"| {name}{' (primary)' if col == 'avg' else ''} | {count(len(y))} | {count(len(x))} |"
        if min(len(x), len(y)) < MIN_CELL:
            L.append(lead + " | | | | |")
            continue
        a, (lo, hi) = auc_ci(x, y, boot)
        o = adjusted_or(R, col)
        ors = f"{fmt(o[0])} ({fmt(o[1])}-{fmt(o[2])}) | {o[3]:.2g}" if o else " | "
        L.append(f"{lead} {mediqr(y)} | {mediqr(x)} | {fmt(a)} ({fmt(lo)}-{fmt(hi)}) | {ors} |")
    L += ["", "OR per SD of the panel's curvature over the people in the model, adjusted for age, sex and BSA; "
              "the p is one-sided (OR > 1) and is a test only in the primary row."]

    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- plots

def p_text(p):
    """One-sided p for a figure: two significant digits, a power of ten below 0.001."""
    if p >= 0.001:
        return f"one-sided $p$ = {p:.2g}"
    m, e = f"{p:.1e}".split("e")
    return rf"one-sided $p$ = ${m} \times 10^{{{int(e)}}}$"


def thesis_rc():
    """Fonts of the thesis figures (as Thesis_coronary/content/methodology/figures/curvature_steps_figure.py)."""
    import matplotlib as mpl
    mpl.rcParams.update({"font.family": "serif", "font.serif": ["cmr10"], "mathtext.fontset": "cm",
                         "axes.unicode_minus": False, "axes.formatter.use_mathtext": True, "font.size": 9,
                         "text.color": INK, "pdf.fonttype": 42})


def panel(ax, R, col):
    """One panel: BL curvature by group, the median and IQR beside each group, the one-sided p of the adjusted OR."""
    d = R[R[col].notna()]
    rng = np.random.default_rng(0)
    for i, g in enumerate(GROUPS):
        dg = d[d["group"] == g]
        x = i + rng.uniform(-0.18, 0.18, len(dg))
        ax.scatter(x, dg[col], s=12, alpha=0.7, color=COLOR[g], linewidths=0)
        if len(dg) >= 2:
            q1, med, q3 = np.percentile(dg[col], [25, 50, 75])
            ax.errorbar(i + 0.3, med, yerr=[[med - q1], [q3 - med]], fmt="o", color=INK, ms=6, capsize=3, lw=1.5)
    ax.set_xticks(range(len(GROUPS)), [f"{GROUP_LABEL[g]}\n($n$ = {int((d['group'] == g).sum())})" for g in GROUPS])
    ax.set_xlim(-0.6, len(GROUPS) - 0.4)
    ax.set_ylabel("Mean curvature ($z$-score)" if col == "avg" else "Mean curvature (mm$^{-1}$)")
    ax.set_title(TITLE[col], fontsize=10, color=INK)  # black marker (median, IQR) is explained in the caption
    o = adjusted_or(d, col)
    if o:
        ax.text(0.98, 0.98, p_text(o[3]), transform=ax.transAxes, ha="right", va="top", fontsize=8.5,
                color=INK, bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.5))
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.grid(color=GRID, lw=0.5)


def plot(R, folder):
    """Two figures: the combined panel (main text) and the LAD, LCx and RCA side by side (appendix)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    thesis_rc()

    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    out = []
    fig, ax = plt.subplots(figsize=(4.8, 4.4))
    panel(ax, R, "avg")
    out.append(folder / "hypertension_curvature_combined.png")
    fig.tight_layout()
    fig.savefig(out[-1], dpi=300)
    plt.close(fig)

    fig, axes = plt.subplots(1, len(ARTERIES), figsize=(12, 4.4))
    for ax, col in zip(axes, ARTERIES):
        panel(ax, R, col)
    out.append(folder / "hypertension_curvature_arteries.png")
    fig.tight_layout()
    fig.savefig(out[-1], dpi=300)
    plt.close(fig)
    return out


# ---------------------------------------------------------------- checks

def check():
    """Known answers on synthetic numbers."""
    s = pd.Series([150, 120, 135, 120, 120, np.nan, 125])
    d = pd.Series([80, 70, 80, 70, 95, np.nan, 80])
    med = pd.Series([0, 0, 0, 0, 0, np.nan, 0])
    fu = pd.Series([1, 0, 0, 1, 0, 1, np.nan])
    g, r = hypertension_group(s, d, med, fu)
    assert [None if pd.isna(v) else v for v in g] == ["hypertension", "normotensive", None, None, None, None, None], list(g)
    assert list(r) == ["ok", "ok", "borderline or incomplete BL pressure", "status changed between the visits",
                       "status changed between the visits", "missing", "missing"], list(r)

    assert auc([2, 3], [0, 1]) == 1 and auc([1], [1]) == 0.5
    rng = np.random.default_rng(1)
    n = 1500
    age, male, bsa = rng.normal(60, 8, n), rng.integers(0, 2, n), rng.normal(1.9, 0.2, n)
    k = rng.normal(0, 1, n)
    p = 1 / (1 + np.exp(-(-0.3 + 0.5 * k + 0.04 * (age - 60))))
    D = pd.DataFrame({"group": np.where(rng.random(n) < p, "hypertension", "normotensive"), "k": k,
                      "scan_age": age, "male": male, "clin_bsa": bsa})
    o = adjusted_or(D, "k")
    assert o[1] < np.exp(0.5) < o[2] and o[3] < 0.001, o

    R = pd.DataFrame({"id": [str(i) for i in range(80)],
                      "group": ["hypertension"] * 30 + ["normotensive"] * 50,
                      "LAD": rng.normal(0.1, 0.02, 80), "CX": rng.normal(0.1, 0.02, 80),
                      "RCA": rng.normal(0.1, 0.02, 80), "scan_age": 60.0, "male": 1.0, "clin_bsa": 1.9})
    R.loc[3, "RCA"] = np.nan
    R = tree_average(R)
    assert np.isnan(R.loc[3, "avg"]) and abs(R["z_LAD"].mean()) < 1e-12
    R["scan_age"] += rng.normal(0, 5, 80)
    R["male"] = rng.integers(0, 2, 80).astype(float)
    R["clin_bsa"] += rng.normal(0, 0.2, 80)
    text = report(Counter({"BL participants": 80, "small": 3}), R, 200)
    assert "| small | <5 |" in text and "| tree average (primary)" in text, text
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        files = plot(R, tmp)
        assert len(files) == 2 and all(f.stat().st_size > 0 for f in files)
    print("hypertension_curvature: all checks passed")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="run the synthetic checks")
    ap.add_argument("--limit", type=int, default=None, help="only the first N participants")
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "hypertension_curvature.md"))
    ap.add_argument("--rows", default=None, help="folder for the plots")
    args = ap.parse_args()
    if args.check:
        check()
        return
    from cgps_stats import OUT_DIR

    flow, R = run(args.limit)
    text = report(flow, R, args.boot)
    Path(args.out).write_text(text, encoding="utf-8")
    files = plot(R, args.rows or Path(OUT_DIR) / "hypertension_curvature")
    print(text)
    print(f"written to {args.out}; plots in {files[0].parent}")


if __name__ == "__main__":
    main()
