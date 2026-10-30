"""Does segment turning follow known LAD anatomy (proximal < mid < distal) in the Medis trees?

    python lad_turning_validity.py [--src TREE_FOLDER] [--boot 2000]

A positive control for the turning feature, run without the outcome. The distal LAD runs down the
interventricular groove and around the apex, so it should turn more than the mid LAD, and the mid more
than the proximal. If mean turning cannot show that, a null prediction result could come from the feature.

Prespecified (2026-10-30, before looking): within person, mean T5 rises plad < mlad < dlad
(Page's trend test, people with all three LAD segments). Repeated at T2.5 and T10 as the scale check:
a real bend still shows over a 10 mm chord, while centerline noise shrinks as the chord grows, so a
gradient that is there at T2.5 but gone at T10 is noise. The LCx and RCA are not tested here.

Rows: the plad, mlad and dlad segments of each Medis tree (progression_turning.build), any BL grade.
1. Per segment: n, median and IQR of mean T2.5 / T5 / T10 (rad/mm).
2. Within person, per scale: Page's trend test; paired differences (median, person-bootstrap 95% CI,
   Wilcoxon p, share of people where the more distal segment turns more) for mlad-plad, dlad-mlad,
   dlad-plad; concordance (share of a person's segment pairs where the more distal one turns more).
3. Sensitivity: Page's test on people whose three LAD segments are all graded none at BL.
4. Stability within position: Spearman correlation of T2.5, T5 and T10 across people per segment.
5. Clustering, external metrics: k-means (k = 3) on the segment values alone, without the labels, scored
   against the true position by the adjusted Rand index (ARI) and normalized mutual information (NMI).
   0 = no better than chance, 1 = the clusters are exactly the positions. Positions overlap, so expect a
   low ARI even when the trend test is clear: the ARI asks whether position can be read off one value.
Private figure: a strip plot, one dot per segment coloured by position, with the k-means cut points, in
--private (default: results/../private). It shows individual values: look at it on the server, never export it.
Figure (thesis style, no title; the caption goes in LaTeX): top row, one ridge per segment and scale, the
density of its central 95% (no single segment is drawn) with median and IQR, and the k-means cut points
dashed; bottom row, the share of each segment in each cluster. Aggregates only (counts 1-4 hidden); writes
lad_turning_validity.md and lad_turning_validity.png.
"""
import argparse
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde, page_trend_test, spearmanr, wilcoxon
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

import hoe10y_qc as hq
import progression_turning as pt
from cgps_stats import OUT_DIR, count, pct

SEGS = ("plad", "mlad", "dlad")  # proximal to distal
SCALES = ("mean_T2.5", "mean_T5", "mean_T10")
PREFIX = "lad_turning_validity"
# Ordinal ramp, ostium to apex (dataviz reference blue, steps 250 / 450 / 650; validated --ordinal).
RAMP = {"plad": "#86b6ef", "mlad": "#2a78d6", "dlad": "#104281"}
LABEL = {"plad": "proximal", "mlad": "mid", "dlad": "distal"}
CHORD = {"mean_T2.5": "2.5 mm chord", "mean_T5": "5 mm chord", "mean_T10": "10 mm chord"}


def fmt(v):
    return "" if pd.isna(v) else f"{v:.4f}"


def pval(p):
    return "<0.0001" if p < 1e-4 else f"{p:.4f}"


def wide(d, col):
    """One row per person, one column per LAD segment, people with all three only."""
    return d.pivot_table(index="id", columns="segment", values=col)[list(SEGS)].dropna()


def boot_median(x, B, rng):
    x = np.asarray(x)
    m = np.median(x[rng.integers(0, len(x), (B, len(x)))], axis=1)
    return np.percentile(m, [2.5, 97.5])


def concordance(d, col):
    """Per person, every pair of present LAD segments: share where the more distal one turns more."""
    k = n = 0
    for _, g in d.dropna(subset=[col]).groupby("id"):
        v = g.set_index("segment")[col]
        for a, b in combinations([s for s in SEGS if s in v.index], 2):
            n += 1
            k += v[b] > v[a]
    return k, n


def kmeans_scores(d, col):
    """k-means (k = 3) on one value per segment, scored against the true position. Clusters are numbered
    by their centre, low to high turning; in one dimension they are cut at the midpoints between centres."""
    g = d.dropna(subset=[col])
    km = KMeans(n_clusters=len(SEGS), n_init=20, random_state=0).fit(g[[col]].to_numpy())
    order = np.argsort(km.cluster_centers_.ravel())
    lab = np.argsort(order)[km.labels_]  # 0 = lowest centre
    centres = km.cluster_centers_.ravel()[order]
    share = pd.crosstab(g["segment"], lab, normalize="index").reindex(index=list(SEGS), columns=range(len(SEGS)),
                                                                      fill_value=0)
    return {"ari": adjusted_rand_score(g["segment"], lab), "nmi": normalized_mutual_info_score(g["segment"], lab),
            "n": len(g), "cuts": (centres[:-1] + centres[1:]) / 2, "share": share}


CLUSTER = ("#d9d8d3", "#9a9993", "#52514e")  # k-means clusters, low to high turning: grey, kept apart from the positions


def _style():
    """Thesis style: serif, white, no title (the caption goes in LaTeX)."""
    plt = pt._plt()
    plt.rcParams.update({"font.family": "serif", "font.serif": ["STIX Two Text", "STIXGeneral", "DejaVu Serif"],
                         "mathtext.fontset": "stix", "font.size": 9, "axes.titlesize": 9.5,
                         "axes.titleweight": "normal", "figure.facecolor": "white", "axes.facecolor": "white",
                         "savefig.facecolor": "white"})
    return plt


def strip_plot(d, stats, path):
    """One dot per segment, coloured by position, with the k-means cut points. INDIVIDUAL DATA: written to
    the private folder only, never to the results folder, never exported from the server."""
    plt = _style()
    rng = np.random.default_rng(0)
    fig, axes = plt.subplots(len(SCALES), 1, figsize=(7.2, 6.2))
    for j, (ax, col) in enumerate(zip(axes, SCALES)):
        for s in SEGS:
            x = d.loc[d["segment"] == s, col].dropna()
            ax.scatter(x, rng.uniform(-1, 1, len(x)), s=14, color=RAMP[s], edgecolor="white", lw=0.5,
                       alpha=0.9, zorder=3)
        for c in stats[col]["km"]["cuts"]:
            ax.axvline(c, color=pt.INK, lw=0.8, ls=(0, (4, 3)), zorder=1)
        ax.set_ylim(-1.4, 1.4)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.tick_params(labelsize=8)
        ax.set_title(f"({'abc'[j]}) {CHORD[col]}", loc="left")
        ax.text(0.99, 0.99, f"ARI {stats[col]['km']['ari']:.2f}", transform=ax.transAxes, ha="right", va="top",
                fontsize=7.5, color=pt.INK2, zorder=8, bbox={"fc": "white", "ec": "none", "pad": 1.5})
    axes[-1].set_xlabel("mean turning (rad/mm)")
    handles = [plt.Line2D([], [], marker="o", ls="", mfc=RAMP[s], mec="white", ms=6, label=LABEL[s]) for s in SEGS]
    handles.append(plt.Line2D([], [], color=pt.INK, lw=0.8, ls=(0, (4, 3)), label="k-means cut ($k = 3$)"))
    fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=8, bbox_to_anchor=(0.5, 0.0))
    pt._save(fig, path, rect=(0, 0.05, 1, 1))


def plot(d, stats, out_dir):
    """Top row: ridgelines per LAD segment with the k-means cut points. Bottom row: how each segment's
    values fall into the three clusters. One column per chord. No title: the caption goes in the thesis."""
    plt = _style()
    fig, axes = plt.subplots(2, len(SCALES), figsize=(7.2, 4.4), gridspec_kw={"height_ratios": [3, 1.25]})
    for j, col in enumerate(SCALES):
        ax, bx = axes[0, j], axes[1, j]
        km = stats[col]["km"]
        v = d[col].dropna()
        lo, hi = v.quantile([0.01, 0.99])
        lo, hi = max(0.0, lo - 0.15 * (hi - lo)), hi + 0.05 * (hi - lo)  # room for the tails to reach zero
        grid = np.linspace(lo, hi, 300)
        dens = {}
        for s in SEGS:
            x = d.loc[d["segment"] == s, col].dropna()
            if len(x) < 5:
                continue
            a, b = x.quantile([0.025, 0.975])  # fitted to the central 95%: no single extreme segment is drawn
            dens[s] = (gaussian_kde(x[(x >= a) & (x <= b)])(grid), x.quantile([0.25, 0.5, 0.75]).to_numpy())
        top = max(y.max() for y, _ in dens.values())
        for i, s in enumerate(SEGS):
            if s not in dens:
                continue
            base = len(SEGS) - 1 - i
            y, (q1, med, q3) = dens[s]
            y = 0.78 * y / top  # ridges stay apart, the IQR bar sits in the gap
            ax.axhline(base, color=pt.GRID, lw=0.6, zorder=2)
            ax.fill_between(grid, base, base + y, color=RAMP[s], alpha=0.9, lw=0, zorder=3)
            ax.plot(grid, base + y, color=pt.INK, lw=0.6, zorder=4)
            ax.plot([q1, q3], [base - 0.12] * 2, color=pt.INK, lw=1.2, zorder=6)
            ax.plot(med, base - 0.12, "o", ms=4.5, mfc="white", mec=pt.INK, mew=0.9, zorder=7)
            if j == 0:
                ax.text(-0.04, base + 0.3, LABEL[s], ha="right", va="center", transform=ax.get_yaxis_transform())
        for c in km["cuts"]:
            ax.axvline(c, color=pt.INK, lw=0.8, ls=(0, (4, 3)), zorder=5)
        ax.set_xlim(lo, hi)
        ax.set_ylim(-0.3, len(SEGS) - 0.1)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.tick_params(labelsize=8)
        p = stats[col]["page"]
        ax.set_title(f"({'abc'[j]}) {CHORD[col]}", loc="left")
        ax.text(0.99, 0.99, f"Page $p$ {pval(p) if not pd.isna(p) else 'n/a'}\nARI {km['ari']:.2f}",
                transform=ax.transAxes, ha="right", va="top", fontsize=7.5, color=pt.INK2, linespacing=1.3,
                zorder=8, bbox={"fc": "white", "ec": "none", "pad": 1.5})
        if j == 1:
            ax.set_xlabel("mean turning (rad/mm)")

        # how each segment splits over the clusters
        share = km["share"]
        for i, s in enumerate(SEGS):
            left = 0.0
            for k in range(len(SEGS)):
                w = share.at[s, k]
                bx.barh(len(SEGS) - 1 - i, w, left=left, height=0.62, color=CLUSTER[k], edgecolor="white", lw=1)
                if w >= 0.12:
                    bx.text(left + w / 2, len(SEGS) - 1 - i, f"{100 * w:.0f}", ha="center", va="center",
                            fontsize=7, color="white" if k == 2 else pt.INK)
                left += w
            if j == 0:
                bx.text(-0.04, len(SEGS) - 1 - i, LABEL[s], ha="right", va="center", fontsize=8,
                        transform=bx.get_yaxis_transform())
        bx.set_xlim(0, 1)
        bx.set_yticks([])
        bx.set_xticks([0, 0.5, 1], ["0", "50", "100"])
        bx.tick_params(labelsize=8)
        bx.spines["left"].set_visible(False)
        bx.set_title(f"({'def'[j]})", loc="left")
        if j == 1:
            bx.set_xlabel("share of the segment in each k-means cluster (%)")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in CLUSTER]
    fig.legend(handles, ["cluster 1 (low turning)", "cluster 2", "cluster 3 (high turning)"], loc="lower center",
               ncol=3, fontsize=8, bbox_to_anchor=(0.5, 0.0), handlelength=1.2)
    pt._save(fig, out_dir / f"{PREFIX}.png", rect=(0.06, 0.05, 1, 1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / f"{PREFIX}.md"))
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--private", default=str(Path(OUT_DIR).parent / "private"),
                    help="folder for the individual-level strip plot; never export it")
    args = ap.parse_args()
    out_dir = Path(args.out).parent
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(0)

    d0, _, skipped = pt.build(args.src)
    d = d0[d0["segment"].isin(SEGS)].reset_index(drop=True)
    full = wide(d, "mean_T5")
    rep = ["# Does LAD turning follow anatomy? (Medis trees)\n",
           "Aggregates only; counts 1-4 shown as <5. Positive control without the outcome: within person, "
           "mean turning should rise from the proximal to the distal LAD. Prespecified test: Page's trend test "
           "at T5; T2.5 and T10 check the scale (a real bend persists at 10 mm, noise does not).\n",
           f"LAD segments: {count(len(d))} from {count(d['id'].nunique())} people; "
           f"{count(len(full))} people have all three. Trees that could not be split: {count(skipped)}.\n"]

    # 1. per segment
    rep += ["## 1. Turning per LAD segment (rad/mm)\n",
            "| segment | n | " + " | ".join(f"{c[5:]} median (IQR)" for c in SCALES) + " |",
            "|---|---|" + "---|" * len(SCALES)]
    for s in SEGS:
        g = d[d["segment"] == s]
        cells = [f"{fmt(g[c].median())} ({fmt(g[c].quantile(.25))}–{fmt(g[c].quantile(.75))})" for c in SCALES]
        rep.append(f"| {s} | {count(g['mean_T5'].notna().sum())} | " + " | ".join(cells) + " |")
    rep.append("\nFigure: lad_turning_validity.png.\n")

    # 2. within person
    rep += ["## 2. Within person: does the more distal segment turn more?\n",
            "| scale | Page's test p (plad < mlad < dlad) | n people | concordant pairs | distal / proximal median ratio |",
            "|---|---|---|---|---|"]
    diffs, page = [], {}
    for c in SCALES:
        w = wide(d, c)
        p = page_trend_test(w.to_numpy()).pvalue if len(w) >= 5 else np.nan
        page[c] = p
        k, n = concordance(d, c)
        ratio = (w["dlad"] / w["plad"].replace(0, np.nan)).median()
        rep.append(f"| {c[5:]} | {pval(p) if not pd.isna(p) else ''} | {count(len(w))} | "
                   f"{pct(k, n)}% of {count(n)} | {ratio:.2f} |")
        for a, b in (("plad", "mlad"), ("mlad", "dlad"), ("plad", "dlad")):
            x = (w[b] - w[a]).to_numpy()
            lo, hi = boot_median(x, args.boot, rng)
            diffs.append(f"| {c[5:]} | {b} − {a} | {fmt(np.median(x))} ({fmt(lo)} to {fmt(hi)}) | "
                         f"{pval(wilcoxon(x).pvalue)} | {pct(int((x > 0).sum()), len(x))}% |")
    rep += ["\nConcordant pairs: of all pairs of one person's LAD segments, the share where the more distal one "
            "turns more (0.5 = no order). A ratio that stays well above 1 at T10 points to anatomy, "
            "one that falls towards 1 as the chord grows points to noise.\n",
            "| scale | difference | median (95% person-bootstrap CI), rad/mm | Wilcoxon p | more distal turns more |",
            "|---|---|---|---|---|", *diffs, ""]

    # 3. sensitivity: plaque-free LADs
    clean = d.groupby("id")["bl"].apply(lambda g: len(g) == len(SEGS) and (g == "none").all())
    dc = d[d["id"].map(clean)]
    rep += ["## 3. Sensitivity: LADs with no plaque in any segment at BL\n",
            "Plaque can bend a Medis centerline; this repeats the Page test where none of the three segments "
            "has plaque.\n", "| scale | Page's test p | n people |", "|---|---|---|"]
    for c in SCALES:
        w = wide(dc, c)
        p = page_trend_test(w.to_numpy()).pvalue if len(w) >= 5 else np.nan
        rep.append(f"| {c[5:]} | {pval(p) if not pd.isna(p) else 'too few'} | {count(len(w))} |")

    # 4. stability within position
    rep += ["\n## 4. Stability within position: Spearman correlation across people\n",
            "The outcome models compare people at the same position, so the feature must rank people the same "
            "way at every scale there, not only separate the positions.\n",
            "| segment | n | T2.5 vs T5 | T5 vs T10 | T2.5 vs T10 |", "|---|---|---|---|---|"]
    for s in SEGS:
        g = d[d["segment"] == s].dropna(subset=list(SCALES))
        r = [spearmanr(g[a], g[b]).statistic if len(g) >= 5 else np.nan
             for a, b in (("mean_T2.5", "mean_T5"), ("mean_T5", "mean_T10"), ("mean_T2.5", "mean_T10"))]
        rep.append(f"| {s} | {count(len(g))} | " + " | ".join("" if pd.isna(v) else f"{v:.2f}" for v in r) + " |")

    # 5. clustering, external metrics
    rep += ["\n## 5. Do unlabelled clusters recover the position? (k-means, k = 3)\n",
            "External metrics against the known label: ARI and NMI, 0 = chance, 1 = clusters are the positions. "
            "The positions overlap, so a clear trend (section 2) can still give a low ARI.\n",
            "| scale | segments | ARI | NMI |", "|---|---|---|---|"]
    stats = {}
    shares = []
    for c in SCALES:
        km = kmeans_scores(d, c)
        stats[c] = {"page": page[c], "km": km}
        rep.append(f"| {c[5:]} | {count(km['n'])} | {km['ari']:.3f} | {km['nmi']:.3f} |")
        cuts = ", ".join(fmt(x) for x in km["cuts"])
        shares += [f"| {c[5:]} | {s} | " + " | ".join(f"{100 * km['share'].at[s, k]:.0f}%" for k in range(len(SEGS)))
                   + f" | {cuts if s == SEGS[0] else ''} |" for s in SEGS]
    rep += ["\nWhere each segment lands (clusters numbered by centre, low to high turning; k-means on one value "
            "cuts at the midpoints between centres):\n",
            "| scale | segment | cluster 1 | cluster 2 | cluster 3 | cut points (rad/mm) |",
            "|---|---|---|---|---|---|", *shares]

    plot(d, stats, out_dir)
    private = Path(args.private)
    private.mkdir(parents=True, exist_ok=True)
    strip_plot(d, stats, private / f"{PREFIX}_strip.png")
    print(f"individual-level strip plot (do not export): {private / f'{PREFIX}_strip.png'}")
    Path(args.out).write_text("\n".join(rep) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
