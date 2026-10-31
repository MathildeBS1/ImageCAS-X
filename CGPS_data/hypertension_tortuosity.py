"""Which of the three tortuosity metrics separates hypertensive from normotensive people? (Medis trees)

    python hypertension_tortuosity.py [--src TREE_FOLDER] [--clean] [--boot 2000]

A known-groups check without the outcome: coronary tortuosity is reported to be higher with hypertension,
so a metric that measures tortuosity should separate the two groups. Rows: one per person and trunk
(LAD, LCx, RCA, from the LM bifurcation or ostium to the end of the distal segment, split_trunks.py).

The three metrics of Bullitt et al. (2003, IEEE TMI):
  DM   distance metric, arc length / chord (1 = straight)
  ICM  inflection count metric, (inflections + 1) x DM; an inflection is where the bending direction
       flips (consecutive discrete curvature vectors point away from each other), at a 5 mm chord
  SOAM sum of angles metric, total turning / length = mean T5 (rad/mm, tortuosity/curvature.py)

The two hypertension measures, each analysed in full:
  BL    clin_bp_sys_mean >= 140 or clin_bp_dia_mean >= 90 or med_antihypertensive_any (at the scan)
  FU    demo_hypertension_deriv (about 10 years after the scan)
Section 1 also counts "both" (hypertensive at both visits vs at neither) for reference.
--clean keeps only clean-baseline people (BL ct_cag_sis == 0 and ct_cag_sss == 0).

1. Group sizes per hypertension measure.
2. Per hypertension measure, trunk and metric: median (IQR) per group, AUC for hypertension (person
   bootstrap 95% CI), OR per SD of log(metric) adjusted for age, sex and BSA (age goes with both, BSA sets
   the scale), silhouette of the hypertension groups on the z-scored log metric (1 = two separate
   clusters, 0 = overlapping).
3. Per hypertension measure and trunk, all three metrics together: silhouette of the groups, and k-means
   (k = 2) scored against hypertension by the adjusted Rand index (0 = chance).
Private figure (individual values, never export): 6 scatters, one per hypertension measure (rows) and
metric (columns); in each, the people of every trunk as two jittered clouds, normotensive and
hypertensive. Aggregate figure: AUC per metric, trunk and hypertension measure. Aggregates only (counts
1-4 hidden); writes hypertension_tortuosity.md and hypertension_tortuosity.png.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score

import hoe10y_qc as hq
import progression_turning as pt
from cgps_stats import MIN_CELL, OUT_DIR, count, num, yes
from split_trunks import graph, split

try:
    from tortuosity.curvature import chord_resample, mean_abs_curvature
except ImportError:  # flat copy on the server: curvature.py next to this file
    from curvature import chord_resample, mean_abs_curvature

PREFIX = "hypertension_tortuosity"
METRICS = {"DM": "DM (arc / chord)", "ICM": "ICM", "SOAM": "SOAM (rad/mm)"}
TRUNKS = {"LAD": "LAD", "CX": "LCx", "RCA": "RCA"}
CHORD = 5.0
HTN_COLOR = {0: "#2a78d6", 1: "#eb6834"}  # validated pair (dataviz validator, light surface)
HTN_LABEL = {0: "normotensive", 1: "hypertensive"}
DEFS = ("bl", "fu")  # the two hypertension measures analysed


# ---------------------------------------------------------------- metrics
def inflections(Y, chord=CHORD):
    """Number of flips of the bending direction along Y, at chord length chord."""
    V = chord_resample(Y, chord)
    if len(V) < 4:
        return np.nan
    u = np.diff(V, axis=0) / chord  # unit chords: each is exactly chord mm long
    k = np.diff(u, axis=0)  # discrete curvature vectors, one per interior vertex
    k = k[np.linalg.norm(k, axis=1) > 1e-6]  # a straight run has no bending direction
    return int(((k[:-1] * k[1:]).sum(1) < 0).sum())


def trunk_metrics(Y, s, end):
    Y = Y[s <= end]
    chord = np.linalg.norm(Y[-1] - Y[0])
    if len(Y) < 3 or chord < 1.0:
        return None
    dm = (s[s <= end][-1] - s[0]) / chord
    return {"DM": dm, "ICM": (inflections(Y) + 1) * dm, "SOAM": mean_abs_curvature(Y, CHORD)}


# ---------------------------------------------------------------- hypertension
def hypertension(bl, fu):
    """{definition: 0/1 series by person id, nan where unknown}."""
    sys_, dia = num(bl["clin_bp_sys_mean"]), num(bl["clin_bp_dia_mean"])
    med = yes(bl["med_antihypertensive_any"])
    known = sys_.notna() | dia.notna() | med.notna()
    h_bl = ((sys_ >= 140) | (dia >= 90) | (med == 1)).astype(float).where(known)
    h_fu = yes(fu["demo_hypertension_deriv"]).reindex(bl.index)
    both = h_bl.where(h_bl == h_fu)  # changed between the visits -> nan
    return {"bl": h_bl, "fu": h_fu, "both": both}


# ---------------------------------------------------------------- data
def build(src, clean_only):
    sheets = hq.load_sheets(hq.ROOT)
    bl, fu = (sheets[v].assign(id=sheets[v]["study_id"].map(hq.norm_id)).drop_duplicates("id").set_index("id")
              for v in ("BL", "FU"))
    htn = hypertension(bl, fu)
    clean = (num(bl["ct_cag_sis"]) == 0) & (num(bl["ct_cag_sss"]) == 0)
    files = sorted(Path(src).rglob("*.vtk"))
    hq.read_label_codes((f, f) for f in files)  # names for codes a file leaves unnamed
    rows, skipped = [], 0
    for f in files:
        pid = hq.id_from_name(f.name)
        if pid not in bl.index or (clean_only and not clean.get(pid, False)):
            continue
        try:
            res = split(*graph(hq.tree_points(f)))
        except Exception:  # noqa: BLE001 - tree skipped, counted
            skipped += 1
            continue
        for a, (_, _, end, _, Y, s) in res.items():
            m = trunk_metrics(Y, s, end)
            if m is None:
                continue
            rows.append({"id": pid, "trunk": a, **m, "age": num(bl["scan_age"]).get(pid),
                         "male": yes(bl["male"]).get(pid), "bsa": num(bl["clin_bsa"]).get(pid),
                         **{f"htn_{k}": v.get(pid, np.nan) for k, v in htn.items()}})
    return pd.DataFrame(rows), skipped


# ---------------------------------------------------------------- statistics
def fmt(v, nd=3):
    return "" if pd.isna(v) else f"{v:.{nd}f}"


def z(x):
    x = np.log(np.asarray(x, float))
    return (x - x.mean()) / x.std()


def auc(x, y):
    r = pd.Series(x).rank().to_numpy()
    n1 = int(y.sum())
    n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


def boot_auc(x, y, B, rng):
    out = []
    for _ in range(B):
        i = rng.integers(0, len(x), len(x))  # one row per person within a trunk: resampling rows = people
        if 0 < y[i].sum() < len(i):
            out.append(auc(x[i], y[i]))
    return np.percentile(out, [2.5, 97.5])


def adjusted_or(g, col, h):
    """OR per SD of log(metric) for hypertension, adjusted for age, sex and BSA (Wald 95% CI)."""
    g = g.dropna(subset=["age", "male", "bsa"])
    X = np.column_stack([np.ones(len(g)), z(g[col]), *(((g[c] - g[c].mean()) / g[c].std()).to_numpy()
                                                      for c in ("age", "bsa")), g["male"].to_numpy()])
    w, _, _, H = pt.fit(X, g[h].to_numpy())
    se = np.sqrt(np.diag(np.linalg.inv(H)))[1]
    return np.exp(w[1]), np.exp(w[1] - 1.96 * se), np.exp(w[1] + 1.96 * se), len(g)


def enough(y):
    return min(int(y.sum()), int(len(y) - y.sum())) >= MIN_CELL


# ---------------------------------------------------------------- figures
def scatter(d, path):
    """6 scatters: hypertension measure (rows) x metric (columns); per trunk, normotensive and hypertensive
    side by side as jittered clouds. INDIVIDUAL DATA: private folder only, never export."""
    plt = pt._plt()
    rng = np.random.default_rng(0)
    fig, axes = plt.subplots(len(DEFS), len(METRICS), figsize=(11, 6.6))
    for i, h in enumerate(DEFS):
        for j, m in enumerate(METRICS):
            ax = axes[i, j]
            ticks, labels = [], []
            for k, a in enumerate(TRUNKS):
                g = d[(d["trunk"] == a) & d[f"htn_{h}"].notna()]
                for v in (0, 1):
                    x = g.loc[g[f"htn_{h}"] == v, m].to_numpy()
                    ax.scatter(3 * k + v + rng.uniform(-0.32, 0.32, len(x)), x, s=10, color=HTN_COLOR[v],
                               edgecolor=pt.SURF, lw=0.4, alpha=0.7, zorder=3)
                    if len(x):
                        ax.plot([3 * k + v - 0.38, 3 * k + v + 0.38], [np.median(x)] * 2, color=pt.INK, lw=2,
                                solid_capstyle="round", zorder=4)
                y = g[f"htn_{h}"].to_numpy().astype(int)
                ticks.append(3 * k + 0.5)
                labels.append(f"{TRUNKS[a]}\nAUC {auc(g[m].to_numpy(), y):.2f}" if enough(y) else TRUNKS[a])
            ax.set_xticks(ticks, labels, fontsize=8)
            ax.set_xlim(-0.7, 3 * len(TRUNKS) - 1.3)
            pt._grid(ax, "y")
            ax.set_title(f"({'abcdef'[3 * i + j]}) {m}, {h.upper()} hypertension")
            ax.set_ylabel(METRICS[m])
    handles = [plt.Line2D([], [], marker="o", ls="", mfc=HTN_COLOR[v], mec=pt.SURF, ms=7, label=HTN_LABEL[v])
               for v in (0, 1)]
    handles.append(plt.Line2D([], [], color=pt.INK, lw=2, label="median"))
    fig.legend(handles=handles, loc="lower center", ncol=3, bbox_to_anchor=(0.5, 0.0))
    pt._save(fig, path, rect=(0, 0.04, 1, 1))


def auc_plot(res, path):
    """AUC (95% CI) per metric and hypertension measure, one panel per trunk. Aggregates only."""
    plt = pt._plt()
    fig, axes = plt.subplots(1, len(TRUNKS), figsize=(9, 3.0), sharex=True)
    for ax, a in zip(axes, TRUNKS):
        for k, m in enumerate(METRICS):
            for h, off in zip(DEFS, (0.15, -0.15)):
                r = res.get((h, a, m))
                if r is None:
                    continue
                y = len(METRICS) - 1 - k + off
                ax.plot(r["ci"], [y, y], color=pt.INK2, lw=2, solid_capstyle="round", zorder=2)
                ax.plot(r["auc"], y, "o", ms=7, mfc=pt.INK if h == "bl" else pt.SURF, mec=pt.INK, mew=1.5,
                        zorder=3)
        ax.axvline(0.5, color=pt.MUTED, lw=1, ls=(0, (4, 3)), zorder=1)
        ax.set_yticks(range(len(METRICS)), list(METRICS)[::-1])
        ax.set_ylim(-0.6, len(METRICS) - 0.4)
        ax.set_title(TRUNKS[a])
        ax.set_xlabel("AUC for hypertension")
        pt._grid(ax, "x")
    handles = [plt.Line2D([], [], marker="o", ls="", mfc=pt.INK if h == "bl" else pt.SURF, mec=pt.INK, ms=7,
                          label=f"{h.upper()} hypertension") for h in DEFS]
    fig.legend(handles=handles, loc="lower center", ncol=2, bbox_to_anchor=(0.5, 0.0))
    pt._save(fig, path, rect=(0, 0.08, 1, 1))


# ---------------------------------------------------------------- main
def analyse(d, h, B, rng, res):
    """Sections 2 and 3 for one hypertension measure; fills res[(h, trunk, metric)] for the AUC figure."""
    col = f"htn_{h}"
    rows, joint = [], []
    for a in TRUNKS:
        g = d[(d["trunk"] == a) & d[col].notna()].reset_index(drop=True)
        y = g[col].to_numpy().astype(int)
        if not enough(y):
            rows.append(f"| {TRUNKS[a]} | all | too few in a group | | | | | |")
            continue
        for m in METRICS:
            x = g[m].to_numpy()
            ci = boot_auc(x, y, B, rng)
            res[(h, a, m)] = {"auc": auc(x, y), "ci": ci}
            o, lo, hi, _ = adjusted_or(g, m, col)
            q = {v: g.loc[y == v, m].quantile([0.25, 0.5, 0.75]).to_numpy() for v in (0, 1)}
            nd = 4 if m == "SOAM" else 2
            rows.append(f"| {TRUNKS[a]} | {m} | {count(y.sum())} / {count(len(y) - y.sum())} | "
                        f"{fmt(q[1][1], nd)} ({fmt(q[1][0], nd)}–{fmt(q[1][2], nd)}) | "
                        f"{fmt(q[0][1], nd)} ({fmt(q[0][0], nd)}–{fmt(q[0][2], nd)}) | "
                        f"{res[(h, a, m)]['auc']:.3f} ({ci[0]:.3f}–{ci[1]:.3f}) | {o:.2f} ({lo:.2f}–{hi:.2f}) | "
                        f"{silhouette_score(z(x)[:, None], y):.3f} |")
        Z = np.column_stack([z(g[m]) for m in METRICS])
        km = KMeans(n_clusters=2, n_init=20, random_state=0).fit_predict(Z)
        joint.append(f"| {TRUNKS[a]} | {count(len(g))} | {silhouette_score(Z, y):.3f} | "
                     f"{adjusted_rand_score(y, km):.3f} | {silhouette_score(Z, km):.3f} |")
    return rows, joint


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / f"{PREFIX}.md"))
    ap.add_argument("--clean", action="store_true", help="clean-baseline people only")
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--private", default=str(Path(OUT_DIR).parent / "private"),
                    help="folder for the individual-level scatter; never export it")
    args = ap.parse_args()
    out_dir = Path(args.out).parent
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(0)

    d, skipped = build(args.src, args.clean)
    d = d.replace([np.inf, -np.inf], np.nan).dropna(subset=list(METRICS))
    rep = ["# Does tortuosity separate hypertensive from normotensive people? (Medis trees)\n",
           "Aggregates only; counts 1-4 shown as <5. Known-groups check without the outcome. Metrics of "
           f"Bullitt et al. (2003) per trunk; inflections and SOAM at a {CHORD:g} mm chord. Two hypertension "
           f"measures, BL (BP >= 140/90 or medication at the scan) and FU (demo_hypertension_deriv)"
           f"{'; clean-baseline people only' if args.clean else ''}. Medis trees are mostly people with plaque "
           "at BL.\n",
           f"Trunks: {count(len(d))} from {count(d['id'].nunique())} people. "
           f"Trees that could not be split: {count(skipped)}.\n"]

    # 1. group sizes
    rep += ["## 1. Hypertension measures (people with a Medis tree)\n",
            "| measure | hypertensive | normotensive | unknown or changed |", "|---|---|---|---|"]
    people = d.drop_duplicates("id")
    for k in (*DEFS, "both"):
        v = people[f"htn_{k}"]
        rep.append(f"| {k.upper()}{' (reference only)' if k == 'both' else ''} | {count((v == 1).sum())} | "
                   f"{count((v == 0).sum())} | {count(v.isna().sum())} |")

    res, joints = {}, {}
    for n, h in enumerate(DEFS):
        rows, joints[h] = analyse(d, h, args.boot, rng, res)
        rep += [f"\n## 2{'ab'[n]}. Per trunk and metric, {h.upper()} hypertension\n",
                "AUC: chance that a hypertensive person's trunk is more tortuous than a normotensive one's "
                "(0.5 = no separation). OR per SD of log(metric), adjusted for age, sex and BSA. Silhouette of "
                "the two groups on the metric alone: near 0 means the groups overlap, not separate clusters.\n",
                "| trunk | metric | n (hyp / norm) | median (IQR), hypertensive | median (IQR), normotensive | "
                "AUC (95% CI) | adjusted OR per SD (95% CI) | silhouette |",
                "|---|---|---|---|---|---|---|---|", *rows]

    # 3. all three together
    rep += ["\n## 3. All three metrics together (z-scored log values)\n",
            "Silhouette of the hypertension groups in the 3-metric space, and whether k-means (k = 2), "
            "blind to hypertension, finds it (ARI 0 = chance). The last column is how clustered the data are "
            "on their own: a low value means there are no natural groups to find.\n",
            "| hypertension | trunk | n | silhouette, hypertension groups | ARI, k-means vs hypertension | "
            "silhouette, k-means clusters |", "|---|---|---|---|---|---|"]
    rep += [f"| {h.upper()} {r}" for h in DEFS for r in joints[h]]

    auc_plot(res, out_dir / f"{PREFIX}.png")
    rep.append("\nFigure: hypertension_tortuosity.png (AUC per metric, trunk and hypertension measure).")
    private = Path(args.private)
    private.mkdir(parents=True, exist_ok=True)
    scatter(d, private / f"{PREFIX}_scatter.png")
    print(f"individual-level scatter (do not export): {private / f'{PREFIX}_scatter.png'}")
    Path(args.out).write_text("\n".join(rep) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
