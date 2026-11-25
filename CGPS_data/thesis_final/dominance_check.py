"""Known-groups check of the daughter asymmetry: does a = ln(D_LCx / D_LAD) differ by coronary dominance as anatomy
says it should?

    python CGPS_data/thesis_final/dominance_check.py [--cohort clean|all] [--limit N] [--boot 2000] [--out MD]
    python CGPS_data/thesis_final/dominance_check.py --check   # synthetic numbers, needs no data

The check needs no reference: it asks whether the cohort feature carries the one difference that is known in
advance. In a left-dominant heart the LCx supplies the inferior wall and the posterior descending artery, so it is
larger than in a right-dominant heart, and a is higher. Set 2026-11-20, before the tracer cohort is linked to the
outcome; it reads only baseline dominance and the sheet columns of the clean-baseline definition.

Expected (written before the run):
  primary    mean a is higher in left-dominant than in right-dominant hearts (difference left - right > 0).
  secondary  co-dominant hearts lie between the two; the difference comes mainly from D_LCx, not from D_LAD.
A difference in the expected direction supports that the tracer asymmetry measures the size of the daughters. It
does not show that it measures them accurately: an error that differs by dominance could give the same result.

Cohort: the plaque-free baseline (ct_cag_sis == 0 and ct_cag_sss == 0, CGPS_data/CLAUDE.md), the participants the
model uses, with the pruned tracer centerlines and the tracer lumen surface. --cohort all uses every participant
with tracer files and adds the primary row by baseline plaque (plaque narrows the lumen, so a diameter can
reflect disease as well as dominance). Every value is the cohort's own: daughter_ratio.tree_asymmetry on the tracer tree and its own
lumen surface, roots from tracer_io.tracer_ostia, as in medis_compare.tree_features. Dominance is ct_cag_dominance
(BL), grouped by its first letter (r right, l left, c or b co-dominant); the raw levels are listed in the report.

Statistics: per group n, mean, SD and median of a, |a|, D_LAD and D_LCx, and how many in the group have no
asymmetry (the tracer's missingness may differ by dominance). Primary: mean a left - right, 95% interval from a
bootstrap over participants within each group, and a one-sided permutation test of left > right (group labels
shuffled; user, 2026-11-25, as in the plot). The difference is also given in
units of the SD of a over all participants with a value, the scale of the model feature.

Plot (one dot per participant, allowed off the server: user, 2026-11-25; thesis colours): a by dominance group
with each group's mean and 95% interval and the one-sided permutation p of left - right (expected > 0), and D_LCx
against D_LAD coloured by group, the line of equal daughters (a = 0) drawn. With --cohort all the participants with
plaque at baseline are hollow. Written to --rows (default <OUT_DIR>/dominance_check).

Writes dominance_check.md next to this script: aggregates only, counts 1-4 shown as <5, statistics only from groups
of MIN_CELL, medians only from QUARTILE_MIN (cgps_stats).
"""
import argparse
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "Thesis_coronary" / "setup"))
from figure_colours import GRID, INK, INK2, SERIES  # noqa: E402  (the thesis colour scheme)

GROUPS = ("right", "left", "co-dominant")
ORDER = ("right", "co-dominant", "left")  # plot order: the expected rise of a
GROUP_LABEL = {"right": "Right-dominant", "co-dominant": "Co-dominant", "left": "Left-dominant"}
COLOR = dict(zip(ORDER, SERIES))  # the three series colours of the thesis scheme, in plot order
FIRST = {"r": "right", "l": "left", "c": "co-dominant", "b": "co-dominant"}  # first letter of ct_cag_dominance
COLS = (("asym", "a = ln(D_LCx / D_LAD)", ""), ("abs", "abs(a)", ""), ("D_LAD", "D_LAD", "mm"), ("D_CX", "D_LCx", "mm"))


def dominance_group(s):
    """ct_cag_dominance -> right / left / co-dominant, None when missing or another level."""
    s = s.astype(str).str.strip().str.lower().where(s.notna())
    return s.str[:1].map(FIRST).where(s.notna()), s


def diff_ci(x, y, boot=2000, seed=0):
    """(mean(x) - mean(y), 95% bootstrap interval with each group resampled on its own, one-sided permutation p for
    mean(x) > mean(y) from as many relabellings as bootstrap samples: (1 + #permuted difference >= d) / (1 + boot))."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    d = x.mean() - y.mean()
    rng = np.random.default_rng(seed)
    b = [rng.choice(x, len(x)).mean() - rng.choice(y, len(y)).mean() for _ in range(boot)]
    lo, hi = np.percentile(b, [2.5, 97.5]) if boot else (np.nan, np.nan)
    z, n = np.r_[x, y], len(x)
    perm = [(q := rng.permutation(z))[:n].mean() - q[n:].mean() for _ in range(boot)]
    return d, (lo, hi), (1 + sum(v >= d for v in perm)) / (1 + boot)


# ---------------------------------------------------------------- data run (server)

def run(cohort="clean", limit=None):
    """(flow, one row per participant with a tracer pair: id, dominance group, plaque_free, asym, D_LAD, D_CX, reason, raw levels)."""
    import hoe10y_qc as hq
    import tracer_io
    from cgps_stats import BL_PATH, load, num
    from daughter_ratio import surface, tree_asymmetry

    bl = load(BL_PATH)
    bl = bl.assign(id=bl["study_id"].map(hq.norm_id)).drop_duplicates("id").set_index("id")
    group, raw = dominance_group(bl["ct_cag_dominance"])
    clean = (num(bl["ct_cag_sis"]) == 0) & (num(bl["ct_cag_sss"]) == 0)
    keep = clean if cohort == "clean" else pd.Series(True, index=bl.index)

    flow = Counter()
    flow["BL participants"] = len(bl)
    flow["in the cohort" if cohort == "clean" else "all"] = int(keep.sum())
    have = tracer_io.tracer_ids()
    ids = sorted((i for i in bl.index[keep] if i in have), key=int)[:limit]
    flow["with tracer centerlines"] = len(ids)
    rows = []
    for pid in ids:
        row = {"id": pid, "group": group.get(pid), "raw": raw.get(pid), "plaque_free": bool(clean.get(pid))}
        f = tracer_io.tracer_lumen(pid)
        if not f.exists():
            rows.append(row | {"reason": "no lumen surface"})
            continue
        try:
            res = tree_asymmetry(tracer_io.tracer_tree(pid), surface(f), tracer_io.tracer_ostia(pid))
        except Exception as ex:  # noqa: BLE001 - counted
            res = {"reason": f"error:{type(ex).__name__}"}
        rows.append(row | res)
    return flow, pd.DataFrame(rows)


# ---------------------------------------------------------------- report

def report(flow, R, cohort, boot):
    from cgps_stats import MIN_CELL, QUARTILE_MIN, count, count_of

    def fmt(x, nd=3):
        return "-" if x is None or not np.isfinite(x) else f"{x:.{nd}g}"

    R = R.copy()
    for c in ("asym", "D_LAD", "D_CX"):
        R[c] = pd.to_numeric(R[c], errors="coerce") if c in R else np.nan
    R["abs"] = R["asym"].abs()
    ok = R[R["asym"].notna()]
    sd_all = ok["asym"].std(ddof=1) if len(ok) >= MIN_CELL else np.nan

    L = ["# Asymmetry by coronary dominance: known-groups check (dominance_check.py)\n",
         (f"Cohort: {'plaque-free baseline' if cohort == 'clean' else 'all participants with tracer files'}. "
          "Tracer asymmetry a = ln(D_LCx / D_LAD) from the tracer tree and its own lumen surface, as in the cohort. "
          "Expected before the run: a higher in left- than in right-dominant hearts; co-dominant between; the "
          f"difference mainly from D_LCx. Counts 1-4 shown as <5; statistics only from {MIN_CELL} participants.\n"),
         "## Flow\n", "| step | participants |", "|---|---|"]
    L += [f"| {k} | {count(v)} |" for k, v in flow.items()]
    L += [f"| with an asymmetry | {count(len(ok))} |", ""]

    L += ["## ct_cag_dominance levels (participants with tracer centerlines)\n", "| level | group | participants |",
          "|---|---|---|"]
    for lev, n in R["raw"].fillna("(missing)").value_counts().items():
        L.append(f"| {lev} | {FIRST.get(str(lev)[:1], '-') if lev != '(missing)' else '-'} | {count(n)} |")

    L += ["\n## Missing asymmetry by group\n", "| group | with tracer centerlines | with an asymmetry |", "|---|---|---|"]
    for g in GROUPS:
        d = R[R["group"] == g]
        n, k = len(d), int(d["asym"].notna().sum())
        L.append(f"| {g} | {count(n)} | {count_of(k, n)}" + (f" ({100 * k / n:.0f}%)" if n >= MIN_CELL else "") + " |")
    reasons = R.loc[R["asym"].isna(), "reason"].fillna("unknown").value_counts()
    L += ["", "Reasons for no asymmetry (all groups): " + (", ".join(f"{r} {count(n)}" for r, n in reasons.items()) or "none"), ""]

    L += ["## Per group\n", "| group | feature | n | mean | SD | median | unit |", "|---|---|---|---|---|---|---|"]
    for g in GROUPS:
        d = ok[ok["group"] == g]
        for c, name, unit in COLS:
            x = d[c].dropna().to_numpy(float)
            if len(x) < MIN_CELL:
                L.append(f"| {g} | {name} | {count(len(x))} | | | | {unit} |")
                continue
            med = np.median(x) if len(x) >= QUARTILE_MIN else None
            L.append(f"| {g} | {name} | {len(x)} | {fmt(x.mean())} | {fmt(x.std(ddof=1))} | {fmt(med)} | {unit} |")

    L += ["\n## Primary: left - right\n", "| feature | left | right | difference (95% CI) | one-sided p (left > right) | difference / SD of a |",
          "|---|---|---|---|---|---|"]
    for c, name, unit in COLS:
        x = ok.loc[ok["group"] == "left", c].dropna().to_numpy(float)
        y = ok.loc[ok["group"] == "right", c].dropna().to_numpy(float)
        if min(len(x), len(y)) < MIN_CELL:
            L.append(f"| {name} | {count(len(x))} | {count(len(y))} | | | |")
            continue
        d, (lo, hi), p = diff_ci(x, y, boot)
        std = fmt(d / sd_all, 2) if c == "asym" else ""
        L.append(f"| {name} | {len(x)} | {len(y)} | {fmt(d)} ({fmt(lo)} to {fmt(hi)}) {unit} | {p:.2g} | {std} |")
    L += ["", ("Primary row: a. The expected direction is a positive difference. The diameters show which daughter "
               "carries it; abs(a), the model feature, has no expected direction (left dominance can make the "
               "daughters more or less unequal). The p is one-sided (left > right) in every row and a test only in the "
               "primary row.")]

    if "plaque_free" in ok and ok["plaque_free"].nunique() > 1:  # --cohort all: the primary row by baseline plaque
        L += ["\n## a, left - right, by baseline plaque\n",
              ("Plaque at the bifurcation narrows the lumen, so in participants with plaque a diameter can reflect "
               "disease as well as dominance. Same statistics as the primary row.\n"),
              "| participants | left | right | difference (95% CI) | one-sided p (left > right) | difference / SD of a |",
              "|---|---|---|---|---|---|"]
        for name, sub in (("all", ok), ("plaque-free", ok[ok["plaque_free"].astype(bool)]),
                          ("plaque at baseline", ok[~ok["plaque_free"].astype(bool)])):
            x = sub.loc[sub["group"] == "left", "asym"].to_numpy(float)
            y = sub.loc[sub["group"] == "right", "asym"].to_numpy(float)
            if min(len(x), len(y)) < MIN_CELL:
                L.append(f"| {name} | {count(len(x))} | {count(len(y))} | | | |")
                continue
            d, (lo, hi), p = diff_ci(x, y, boot)
            L.append(f"| {name} | {len(x)} | {len(y)} | {fmt(d)} ({fmt(lo)} to {fmt(hi)}) | {p:.2g} | {fmt(d / sd_all, 2)} |")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- plot

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


def plot(R, path, boot=2000):
    """Strip plot of a by dominance group (median and interquartile range beside each group, as in
    hypertension_curvature.py) and D_LCx against D_LAD by group, with the one-sided permutation p of mean a left - right."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    thesis_rc()

    R = R.copy()
    for c in ("asym", "D_LAD", "D_CX"):
        R[c] = pd.to_numeric(R[c], errors="coerce") if c in R else np.nan
    ok = R[R["asym"].notna() & R["group"].isin(GROUPS)]
    free = ok["plaque_free"].astype(bool) if "plaque_free" in ok else pd.Series(True, index=ok.index)
    split = free.nunique() > 1
    rng = np.random.default_rng(0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={"width_ratios": [1, 1.15]})
    for i, g in enumerate(ORDER):
        d, f = ok[ok["group"] == g], free[ok["group"] == g]
        x = i + rng.uniform(-0.18, 0.18, len(d))
        for m, hollow in ((f, False), (~f, True)):
            if m.any():
                ax1.scatter(x[m.to_numpy()], d.loc[m, "asym"], s=16, alpha=0.7, linewidths=1,
                            facecolors="none" if hollow else COLOR[g], edgecolors=COLOR[g])
                ax2.scatter(d.loc[m, "D_LAD"], d.loc[m, "D_CX"], s=16, alpha=0.7, linewidths=1,
                            facecolors="none" if hollow else COLOR[g], edgecolors=COLOR[g],
                            label=None if hollow else f"{GROUP_LABEL[g]} ($n$ = {len(d)})")
        if len(d) >= 2:
            q1, med, q3 = np.percentile(d["asym"].to_numpy(float), [25, 50, 75])
            ax1.errorbar(i + 0.3, med, yerr=[[med - q1], [q3 - med]], fmt="o", color=INK, ms=6, capsize=3, lw=1.5)
    ax1.axhline(0, color=INK2, lw=1, ls="--")
    ax1.set_xticks(range(len(ORDER)), [f"{GROUP_LABEL[g]}\n($n$ = {int((ok['group'] == g).sum())})" for g in ORDER])
    ax1.set_xlim(-0.6, len(ORDER) - 0.4)
    ax1.set_ylabel(r"Asymmetry, $a = \ln(D_{\mathrm{LCx}} / D_{\mathrm{LAD}})$")  # cmr10 has no underscore
    ax1.set_title("LAD/LCx asymmetry by dominance", fontsize=10, color=INK)  # black marker (median, IQR): caption
    x, y = (ok.loc[ok["group"] == g, "asym"].to_numpy(float) for g in ("left", "right"))
    if min(len(x), len(y)) >= 2:
        ax1.text(0.02, 0.98, "Left vs right: " + p_text(diff_ci(x, y, boot)[2]), transform=ax1.transAxes,
                 ha="left", va="top", fontsize=8.5, color=INK,
                 bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.5))

    lim = [np.nanmin(ok[["D_LAD", "D_CX"]].to_numpy()), np.nanmax(ok[["D_LAD", "D_CX"]].to_numpy())] if len(ok) else [0, 1]
    ax2.plot(lim, lim, color=INK2, lw=1, ls="--", label="equal diameters ($a$ = 0)")
    ax2.set_xlabel(r"LAD diameter, $D_{\mathrm{LAD}}$ (mm)")
    ax2.set_ylabel(r"LCx diameter, $D_{\mathrm{LCx}}$ (mm)")
    ax2.set_aspect("equal", adjustable="datalim")
    ax2.set_title("LAD and LCx diameters by dominance", fontsize=10, color=INK)
    if split:
        ax2.scatter([], [], s=16, facecolors="none", edgecolors=INK2, label="hollow: plaque at baseline")
    ax2.legend(frameon=False, fontsize=8, loc="upper left")
    for ax in (ax1, ax2):
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(colors=INK2, labelsize=8)
        ax.grid(color=GRID, lw=0.5)
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


# ---------------------------------------------------------------- checks

def check():
    """Known answers on synthetic numbers."""
    s = pd.Series(["Right", " left ", "Co-dominant", "balanced", None, "unknown"])
    g, _ = dominance_group(s)
    assert list(g.iloc[:4]) == ["right", "left", "co-dominant", "co-dominant"] and g.iloc[4:].isna().all(), list(g)

    rng = np.random.default_rng(1)
    x, y = rng.normal(0.2, 0.15, 400), rng.normal(-0.1, 0.15, 4000)
    d, (lo, hi), p = diff_ci(x, y, 500)
    assert abs(d - 0.3) < 0.03 and lo < 0.3 < hi and p < 0.01, (d, lo, hi, p)
    assert diff_ci(y, x, 500)[2] > 0.99  # one-sided: the wrong direction gives p near 1
    d, (lo, hi), p = diff_ci(rng.normal(0, 0.15, 400), rng.normal(0, 0.15, 400), 500)
    assert lo < 0 < hi, (d, lo, hi)

    R = pd.DataFrame({"id": [str(i) for i in range(60)], "group": ["right"] * 40 + ["left"] * 12 + ["co-dominant"] * 8,
                      "raw": ["right"] * 40 + ["left"] * 12 + ["co-dominant"] * 8,
                      "asym": np.r_[rng.normal(-0.1, 0.1, 40), rng.normal(0.2, 0.1, 12), [np.nan] * 8],
                      "D_LAD": 3.5, "D_CX": 3.2, "reason": ["ok"] * 52 + ["no shared O"] * 8})
    text = report(Counter({"BL participants": 60}), R, "clean", 200)
    assert "## Primary: left - right" in text and "| co-dominant | 8 | <5 |" not in text, text
    assert "by baseline plaque" not in text
    R["plaque_free"] = np.arange(60) % 2 == 0
    text_all = report(Counter({"BL participants": 60}), R, "all", 200)
    assert "| plaque-free | 6 | 20 |" in text_all and "| plaque at baseline | 6 | 20 |" in text_all, text_all
    assert "| co-dominant | 8 | 0 (0%) |" in text and "| left | 12 | hidden (100%) |" in text, text
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        plot(R, Path(tmp) / "p.png", 100)
        assert (Path(tmp) / "p.png").stat().st_size > 0
    print("dominance_check: all checks passed")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="run the synthetic checks")
    ap.add_argument("--cohort", choices=("clean", "all"), default="clean")
    ap.add_argument("--limit", type=int, default=None, help="only the first N participants")
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "dominance_check.md"))
    ap.add_argument("--rows", default=None, help="folder for the plot")
    args = ap.parse_args()
    if args.check:
        check()
        return
    from cgps_stats import OUT_DIR

    flow, R = run(args.cohort, args.limit)
    text = report(flow, R, args.cohort, args.boot)
    Path(args.out).write_text(text, encoding="utf-8")
    rows = Path(args.rows or Path(OUT_DIR) / "dominance_check")
    rows.mkdir(parents=True, exist_ok=True)
    png = rows / f"dominance_scatter_{args.cohort}.png"
    plot(R, png, args.boot)
    print(text)
    print(f"written to {args.out}; plot in {png}")


if __name__ == "__main__":
    main()
