"""Do the three tortuosity metrics separate the proximal, mid and distal LAD? (Medis trees)

    python lad_tortuosity_position.py [--src TREE_FOLDER] [--boot 2000]

A known-groups check without the outcome, on the LAD only: the distal LAD runs down the interventricular
groove and around the apex, so it should be more tortuous than the mid, and the mid more than the proximal.
Prespecified: within person, each metric rises plad < mlad < dlad (Page's trend test, people with all three).

The three metrics of Bullitt et al. (2003, IEEE TMI), per LAD segment (split_trunks.py boundaries):
  DM   distance metric, segment arc length / chord between its ends (1 = straight)
  ICM  inflection count metric, (inflections + 1) x DM; an inflection is where the bending direction flips,
       on the whole-trunk centerline at a 5 mm chord, counted in the segment it falls in
  SOAM sum of angles metric, mean turning per mm at a 5 mm chord (= mean T5 of progression_turning.py)
The profiles are computed on the whole trunk and cut afterwards, so a short plad still gets angles. DM and
ICM grow with segment length (a longer stretch has more room to detour and flip); the median lengths are
reported next to them.

1. Per segment: n, median length, median (IQR) of each metric.
2. Within person: Page's test, concordance (share of a person's segment pairs where the more distal one is
   more tortuous), and the same Page test on LADs with no plaque in any segment at BL.
3. Clustering: k-means (k = 3), blind to position, on each metric alone and on all three together
   (z-scored log values), scored against the true position by the adjusted Rand index (0 = chance,
   1 = the clusters are the positions); silhouette of the position groups (1 = separate, 0 = overlapping).
Private figure (individual values, never export): one panel per metric, the segments as three jittered
clouds with their medians. Aggregates only (counts 1-4 hidden); writes lad_tortuosity_position.md.
"""
import argparse
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import page_trend_test
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score

import hoe10y_qc as hq
import progression_turning as pt
from cgps_stats import OUT_DIR, count, pct
from hypertension_tortuosity import CHORD, METRICS, z
from lad_turning_validity import LABEL, RAMP, SEGS, pval
from split_trunks import graph, split

try:
    from tortuosity.curvature import chord_resample, turning_angles
except ImportError:  # flat copy on the server: curvature.py next to this file
    from curvature import chord_resample, turning_angles

PREFIX = "lad_tortuosity_position"


# ---------------------------------------------------------------- metrics
def segment_metrics(Y, s, cuts):
    """DM, ICM and SOAM for the proximal, mid and distal stretch of one trunk (cuts = pm, md, end in mm)."""
    V = chord_resample(Y, CHORD)
    if len(V) < 4:
        return []
    pos = s[np.argmin(np.linalg.norm(Y[None] - V[1:-1, None], axis=2), axis=1)]  # arc position of each angle
    theta = turning_angles(V) / CHORD
    k = np.diff(np.diff(V, axis=0) / CHORD, axis=0)  # curvature vectors, one per interior vertex
    bent = np.linalg.norm(k, axis=1) > 1e-6  # a straight run has no bending direction
    flip = bent[:-1] & bent[1:] & ((k[:-1] * k[1:]).sum(1) < 0)  # between vertex i and i + 1
    at = lambda x: np.array([np.interp(x, s, Y[:, c]) for c in range(3)])  # noqa: E731 - point at arc x
    rows = []
    for lo, hi in zip((0, *cuts[:2]), cuts):
        chord = np.linalg.norm(at(hi) - at(lo))
        seg = (pos >= lo) & (pos < hi)
        if hi - lo < 1.0 or chord < 1.0 or seg.sum() < 2:
            rows.append(None)
            continue
        dm = (hi - lo) / chord
        rows.append({"length": hi - lo, "DM": dm, "ICM": (int(flip[seg[1:]].sum()) + 1) * dm,
                     "SOAM": theta[seg].mean()})
    return rows


def build(src):
    bl = hq.load_sheets(hq.ROOT)["BL"]
    bl = bl.assign(id=bl["study_id"].map(hq.norm_id)).drop_duplicates("id").set_index("id")
    files = sorted(Path(src).rglob("*.vtk"))
    hq.read_label_codes((f, f) for f in files)  # names for codes a file leaves unnamed
    rows, skipped = [], 0
    for f in files:
        pid = hq.id_from_name(f.name)
        try:
            res = split(*graph(hq.tree_points(f)))
        except Exception:  # noqa: BLE001 - tree skipped, counted
            skipped += 1
            continue
        if "LAD" not in res:
            continue
        pm, md, end, _, Y, s = res["LAD"]
        for seg, m in zip(SEGS, segment_metrics(Y, s, (pm, md, end))):
            if m is not None:
                grade = hq.grade_of(bl.at[pid, f"ct_cag_{seg}_stenosis"]) if pid in bl.index else "missing"
                rows.append({"id": pid, "segment": seg, "bl": grade, **m})
    return pd.DataFrame(rows).replace([np.inf, -np.inf], np.nan), skipped


# ---------------------------------------------------------------- statistics
def fmt(v, m):
    return "" if pd.isna(v) else f"{v:.4f}" if m == "SOAM" else f"{v:.2f}"


def wide(d, col):
    """One row per person, one column per LAD segment, people with all three only."""
    return d.pivot_table(index="id", columns="segment", values=col)[list(SEGS)].dropna()


def concordance(w):
    pairs = list(combinations(SEGS, 2))
    k = sum(int((w[b] > w[a]).sum()) for a, b in pairs)
    return k, len(w) * len(pairs)


def page(w):
    return page_trend_test(w.to_numpy()).pvalue if len(w) >= 5 else np.nan


def clusters(X, y):
    """k-means (k = 3) blind to position, scored against it; silhouette of the true position groups."""
    km = KMeans(n_clusters=len(SEGS), n_init=20, random_state=0).fit_predict(X)
    return adjusted_rand_score(y, km), silhouette_score(X, y)


# ---------------------------------------------------------------- figure
def scatter(d, stats, path):
    """One panel per metric, the LAD segments as jittered clouds with medians. INDIVIDUAL DATA: private
    folder only, never export."""
    plt = pt._plt()
    rng = np.random.default_rng(0)
    fig, axes = plt.subplots(1, len(METRICS), figsize=(11, 3.9))
    for j, (ax, m) in enumerate(zip(axes, METRICS)):
        for k, s in enumerate(SEGS):
            x = d.loc[d["segment"] == s, m].dropna().to_numpy()
            ax.scatter(k + rng.uniform(-0.3, 0.3, len(x)), x, s=10, color=RAMP[s], edgecolor=pt.SURF, lw=0.4,
                       alpha=0.75, zorder=3)
            if len(x):
                ax.plot([k - 0.36, k + 0.36], [np.median(x)] * 2, color=pt.INK, lw=2, solid_capstyle="round",
                        zorder=4)
        ax.set_xticks(range(len(SEGS)), [LABEL[s] for s in SEGS])
        ax.set_xlim(-0.6, len(SEGS) - 0.4)
        pt._grid(ax, "y")
        ax.set_title(f"({'abc'[j]}) {m}")
        ax.set_ylabel(METRICS[m])
        p, ari = stats[m]
        ax.text(0.02, 0.98, f"Page p {pval(p) if not pd.isna(p) else 'n/a'}\nARI {ari:.2f}", transform=ax.transAxes,
                ha="left", va="top", fontsize=8, color=pt.INK2, zorder=8,
                bbox={"fc": pt.SURF, "ec": "none", "pad": 1.5})
    handles = [plt.Line2D([], [], marker="o", ls="", mfc=RAMP[s], mec=pt.SURF, ms=7, label=LABEL[s]) for s in SEGS]
    handles.append(plt.Line2D([], [], color=pt.INK, lw=2, label="median"))
    fig.legend(handles=handles, loc="lower center", ncol=4, bbox_to_anchor=(0.5, 0.0))
    pt._save(fig, path, rect=(0, 0.08, 1, 1))


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / f"{PREFIX}.md"))
    ap.add_argument("--private", default=str(Path(OUT_DIR).parent / "private"),
                    help="folder for the individual-level scatter; never export it")
    args = ap.parse_args()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)

    d, skipped = build(args.src)
    d = d.dropna(subset=list(METRICS))
    rep = ["# Do DM, ICM and SOAM separate the proximal, mid and distal LAD? (Medis trees)\n",
           "Aggregates only; counts 1-4 shown as <5. Known-groups check without the outcome: the distal LAD "
           "wraps around the apex, so tortuosity should rise plad < mlad < dlad. Metrics of Bullitt et al. "
           f"(2003); inflections and SOAM at a {CHORD:g} mm chord. Medis trees are mostly people with plaque "
           "at BL.\n",
           f"LAD segments: {count(len(d))} from {count(d['id'].nunique())} people; "
           f"{count(len(wide(d, 'SOAM')))} people have all three. Trees that could not be split: "
           f"{count(skipped)}.\n"]

    # 1. per segment
    rep += ["## 1. Per segment\n",
            "| segment | n | median length (mm) | " + " | ".join(f"{m} median (IQR)" for m in METRICS) + " |",
            "|---|---|---|" + "---|" * len(METRICS)]
    for s in SEGS:
        g = d[d["segment"] == s]
        cells = [f"{fmt(g[m].median(), m)} ({fmt(g[m].quantile(.25), m)}–{fmt(g[m].quantile(.75), m)})"
                 for m in METRICS]
        rep.append(f"| {LABEL[s]} | {count(len(g))} | {g['length'].median():.1f} | " + " | ".join(cells) + " |")

    # 2. within person
    clean = d.groupby("id")["bl"].apply(lambda g: len(g) == len(SEGS) and (g == "none").all())
    dc = d[d["id"].map(clean)]
    rep += ["\n## 2. Within person: is the more distal segment more tortuous?\n",
            "Concordant pairs: of all pairs of one person's LAD segments, the share where the more distal one "
            "scores higher (0.5 = no order). The last two columns repeat the Page test on LADs with no plaque "
            "in any segment at BL (plaque can bend a Medis centerline).\n",
            "| metric | Page's test p | n people | concordant pairs | Page p, plaque-free LADs | n people |",
            "|---|---|---|---|---|---|"]
    stats = {}
    for m in METRICS:
        w, wc = wide(d, m), wide(dc, m)
        k, n = concordance(w)
        stats[m] = [page(w)]
        pc = page(wc)
        rep.append(f"| {m} | {pval(stats[m][0]) if not pd.isna(stats[m][0]) else ''} | {count(len(w))} | "
                   f"{pct(k, n)}% of {count(n)} | {pval(pc) if not pd.isna(pc) else 'too few'} | {count(len(wc))} |")

    # 3. clustering
    rep += ["\n## 3. Do unlabelled clusters recover the position? (k-means, k = 3)\n",
            "ARI: k-means blind to position, scored against it (0 = chance, 1 = the clusters are the positions). "
            "Silhouette: how well the three true positions separate (near 0 = overlapping clouds). Positions "
            "overlap, so a clear Page trend can still give a low ARI.\n",
            "| metric | segments | ARI | silhouette, positions |", "|---|---|---|---|"]
    y = d["segment"].map({s: i for i, s in enumerate(SEGS)}).to_numpy()
    for m in METRICS:
        ari, sil = clusters(z(d[m])[:, None], y)
        stats[m].append(ari)
        rep.append(f"| {m} | {count(len(d))} | {ari:.3f} | {sil:.3f} |")
    ari, sil = clusters(np.column_stack([z(d[m]) for m in METRICS]), y)
    rep.append(f"| all three together | {count(len(d))} | {ari:.3f} | {sil:.3f} |")

    private = Path(args.private)
    private.mkdir(parents=True, exist_ok=True)
    scatter(d, stats, private / f"{PREFIX}_scatter.png")
    print(f"individual-level scatter (do not export): {private / f'{PREFIX}_scatter.png'}")
    Path(args.out).write_text("\n".join(rep) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
