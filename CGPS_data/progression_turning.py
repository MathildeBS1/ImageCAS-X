"""Does segment turning predict plaque progression (BL -> FU visual grade) in the Medis trees?

    python progression_turning.py [--src TREE_FOLDER] [--folds 10] [--boot 200]

Rows: the 9 split trunk segments of each Medis tree (split_trunks.py) with a visual grade at BL and FU;
occluded-at-BL segments are dropped. Outcome: higher grade at FU (none -> minimal counts).
Turning comes from the whole-trunk turning-angle profile (thesis Section 5.1.1, chord l mm, rad/mm).

Six geometry variants, each added on its own to the same base model and z-scored within position
in the training folds (missing -> 0, the position mean):
  mean T5, 90th percentile of T5 (sharpest bend), fraction of the segment above the cohort 75th
  percentile of T5, mean T2.5, mean T10, mean T5 over the 20 mm upstream of the segment.

1. Between people (logistic): base = position + BL grade + log SCORE2 + log follow-up.
   Per variant: OR per SD, robust p, out-of-fold position-stratified C and ΔC (person bootstrap),
   pooled AUC, confusion matrix (call "progresses" above the training-fold progression rate).
   Figures: progression_roc.png, progression_confusion.png.
2. Within person (conditional logistic, stratified on person): base = position + BL grade + log length.
   Per variant: out-of-fold within-person C, ΔC, top-1 hit rate (the person's highest-ranked segment
   progressed), and how often geometry changes the top-ranked segment and whether the new one progressed.
3. Reclassification: position + follow-up vs + mean T5. Segments whose risk geometry raised most
   (top 10% of the out-of-fold risk change) or lowered most (bottom 10%): did they progress?
Aggregates only (counts 1-4 hidden, also when they could be worked out); writes progression_turning.md.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import chi2, norm

import hoe10y_qc as hq
from cgps_stats import OUT_DIR, count, num, suppress
from split_trunks import NAMES, graph, split

try:
    from tortuosity.curvature import chord_resample, turning_angles
except ImportError:  # flat copy on the server: curvature.py next to this file
    from curvature import chord_resample, turning_angles

GRADE = {"none": "none", "minimal": "minimal", "mild": "mild", "moderate": ">=moderate", "severe": ">=moderate"}
VARIANTS = {"mean_T5": "mean T5", "p90_T5": "90th pct T5", "frac_T5": "fraction above p75",
            "mean_T2.5": "mean T2.5", "mean_T10": "mean T10", "up_T5": "upstream 20 mm T5"}
UPSTREAM = 20.0


# ---------------------------------------------------------------- features
def profile(Y, s, chord):
    V = chord_resample(Y, chord)
    if len(V) < 3:
        return np.zeros(0), np.zeros(0)
    pos = s[np.argmin(np.linalg.norm(Y[None] - V[1:-1, None], axis=2), axis=1)]
    return pos, turning_angles(V) / chord


def segment_features(Y, s, cuts):
    prof = {c: profile(Y, s, c) for c in (2.5, 5.0, 10.0)}
    rows = []
    for lo, hi in zip((0, *cuts[:2]), cuts):
        f = {"length": hi - lo}
        for c, (pos, th) in prof.items():
            seg = th[(pos >= lo) & (pos < hi)]
            f[f"mean_T{c:g}"] = seg.mean() if len(seg) >= 2 else np.nan
            if c == 5.0:
                f["p90_T5"] = np.percentile(seg, 90) if len(seg) >= 2 else np.nan
                f["t5_values"] = seg
                up = th[(pos >= lo - UPSTREAM) & (pos < lo)]
                f["up_T5"] = up.mean() if len(up) >= 2 else np.nan
        rows.append(f)
    return rows


def build(src):
    sheets = hq.load_sheets(hq.ROOT)
    bl, fu = (sheets[v].assign(id=sheets[v]["study_id"].map(hq.norm_id)).drop_duplicates("id").set_index("id")
              for v in ("BL", "FU"))
    score2 = num(bl["score2"]).fillna(num(bl["score2_op"])) if "score2_op" in bl else num(bl["score2"])
    years = (pd.to_datetime(fu["scandate"], errors="coerce").reindex(bl.index)
             - pd.to_datetime(bl["scandate"], errors="coerce")).dt.days / 365.25
    rows = []
    for f in sorted(Path(src).rglob("*.vtk")):
        pid = hq.id_from_name(f.name)
        try:
            res = split(*graph(hq.tree_points(f)))
        except Exception:  # noqa: BLE001 - tree skipped
            continue
        for a, (pm, md, end, _, Y, s) in res.items():
            for seg, feat in zip(NAMES[a], segment_features(Y, s, (pm, md, end))):
                g = [hq.grade_of(d.at[pid, f"ct_cag_{seg}_stenosis"]) if pid in d.index else "missing" for d in (bl, fu)]
                rows.append({"id": pid, "segment": seg, "bl": g[0], "fu": g[1], **feat,
                             "score2": score2.get(pid, np.nan), "years": years.get(pid, np.nan)})
    d = pd.DataFrame(rows)
    thr = np.percentile(np.concatenate([v for v in d["t5_values"] if len(v)]), 75)  # outcome-free threshold
    d["frac_T5"] = [np.mean(v > thr) if len(v) >= 2 else np.nan for v in d["t5_values"]]
    rank = {g: i for i, g in enumerate(hq.GRADES)}
    d["y"] = (d["fu"].map(rank) > d["bl"].map(rank)).astype(float)
    return d.drop(columns="t5_values"), d["bl"].isin(GRADE) & d["fu"].isin(rank)


# ---------------------------------------------------------------- models
def zscore(d, col, train):
    m, sd = d[train].groupby("segment")[col].mean(), d[train].groupby("segment")[col].std()
    return ((d[col] - d["segment"].map(m)) / d["segment"].map(sd).replace(0, np.nan)).fillna(0).to_numpy()


def dummies(d, col, levels):
    return [(d[col] == v).to_numpy(float) for v in levels]


def design(d, z=None, person=True, grade=True):
    """Between-person design. person: log SCORE2 + log follow-up; else only log follow-up."""
    segs = sorted(d["segment"].unique())
    X = [np.ones(len(d)), np.log(d["years"])] + ([np.log(d["score2"])] if person else [])
    X += dummies(d, "segment", segs[1:]) + (dummies(d, "grade", ("minimal", "mild", ">=moderate")) if grade else [])
    return np.column_stack(X + ([z] if z is not None else []))


def fit(X, y, l2=1e-6):
    w = np.zeros(X.shape[1])
    for _ in range(100):
        p = 1 / (1 + np.exp(-np.clip(X @ w, -30, 30)))
        H = X.T @ (X * (p * (1 - p))[:, None]) + l2 * np.eye(len(w))
        step = np.linalg.solve(H, X.T @ (y - p) - l2 * w)
        w += step
        if np.abs(step).max() < 1e-9:
            break
    p = 1 / (1 + np.exp(-np.clip(X @ w, -30, 30)))
    return w, p, np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)), H


def predict(X, w):
    return 1 / (1 + np.exp(-np.clip(X @ w, -30, 30)))


def within_design(d, z=None):
    """Within-person design: no intercept, person terms cancel."""
    X = dummies(d, "segment", sorted(d["segment"].unique())[1:]) + dummies(d, "grade", ("minimal", "mild", ">=moderate"))
    X += [np.log(d["length"].clip(lower=1.0))]
    return np.column_stack(X + ([z] if z is not None else []))


def clogit(X, y, groups, l2=1e-4):
    """Exact conditional logistic regression (strata = persons with some but not all segments progressed)."""
    strata = [np.where(groups == g)[0] for g in np.unique(groups)]
    strata = [i for i in strata if 0 < y[i].sum() < len(i)]

    def nll(b):
        total = l2 * b @ b
        for i in strata:
            eta, k = X[i] @ b, int(y[i].sum())
            E = np.full(k + 1, -np.inf); E[0] = 0.0  # log elementary symmetric polynomials
            for e in eta:
                E[1:] = np.logaddexp(E[1:], E[:-1] + e)
            total -= eta[y[i] == 1].sum() - E[k]
        return total
    r = minimize(nll, np.zeros(X.shape[1]), method="BFGS")
    return r.x, -r.fun


def strat_c(d, p, by):
    """Concordance over (progressed, not progressed) pairs within each group of `by`."""
    num_, den = 0.0, 0
    for _, g in d.assign(p=p).groupby(by):
        e, ne = g.p[g.y == 1].to_numpy(), g.p[g.y == 0].to_numpy()
        if len(e) and len(ne):
            diff = e[:, None] - ne[None]
            num_ += (diff > 0).sum() + 0.5 * (diff == 0).sum()
            den += diff.size
    return num_ / den if den else np.nan


def auc(y, p):
    order = np.argsort(-p)
    tpr = np.r_[0, np.cumsum(y[order] == 1) / max((y == 1).sum(), 1)]
    fpr = np.r_[0, np.cumsum(y[order] == 0) / max((y == 0).sum(), 1)]
    return float(np.sum(np.diff(fpr) * (tpr[1:] + tpr[:-1]) / 2)), fpr, tpr


def boot_delta(d, p0, p1, by, B, rng):
    rows_of, people = d.groupby("id").indices, d["id"].unique()
    out = []
    for _ in range(B):
        idx = np.concatenate([rows_of[i] for i in rng.choice(people, len(people))])
        db = d.iloc[idx].reset_index(drop=True)
        out.append(strat_c(db, p1[idx], by) - strat_c(db, p0[idx], by))
    return np.nanpercentile(out, [2.5, 97.5])


def confusion(y, p, thr):
    c = p > thr
    return [int(x) for x in ((c & (y == 1)).sum(), (~c & (y == 1)).sum(), (c & (y == 0)).sum(), (~c & (y == 0)).sum())]


# ---------------------------------------------------------------- figures
# Validated categorical palette (dataviz skill); one fixed colour per model in every figure.
SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e4e3df"
MODEL_COLOR = {"base": "#8a8984", "mean T5": "#2a78d6", "90th pct T5": "#eb6834", "fraction above p75": "#1baf7a",
               "mean T2.5": "#eda100", "mean T10": "#e87ba4", "upstream 20 mm T5": "#008300"}
VERDICT_COLOR = {"correct": "#1baf7a", "wrong": "#e34948", "neutral": "#c8c7c2"}
FLAGGED, MISSED = "#86b6ef", "#eb6834"


def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 9, "figure.facecolor": SURF, "axes.facecolor": SURF,
        "savefig.facecolor": SURF, "axes.edgecolor": MUTED, "axes.labelcolor": INK2, "xtick.color": INK2,
        "ytick.color": INK2, "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.titlecolor": INK, "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False})
    return plt


def _grid(ax, axis="y"):
    ax.grid(axis=axis, color=GRID, lw=0.8)
    ax.set_axisbelow(True)


def _save(fig, path, rect=None):
    fig.tight_layout(rect=rect)
    fig.savefig(path, dpi=170)
    import matplotlib.pyplot as plt
    plt.close(fig)


def plots(y, preds, conf, out_dir):
    plt = _plt()
    grid = np.linspace(0, 1, 21)  # binned so no single segment is a visible step
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    _grid(ax, "both")
    ax.plot([0, 1], [0, 1], lw=1, ls=":", color=MUTED)
    ax.text(0.62, 0.55, "chance", color=MUTED, fontsize=8, rotation=38)
    for name, p in preds.items():
        a, fpr, tpr = auc(y, p)
        ax.plot(grid, [tpr[fpr <= g].max() for g in grid], lw=2.6 if name == "base" else 1.8,
                color=MODEL_COLOR.get(name, INK), label=f"{name}  (AUC {a:.2f})", zorder=3 if name == "base" else 2)
    ax.set(xlabel="False positive rate (1 - specificity)", ylabel="True positive rate (sensitivity)", xlim=(0, 1), ylim=(0, 1.02))
    ax.set_title("ROC: which segments progress? (out-of-fold)")
    ax.legend(fontsize=8, loc="lower right", title="model", title_fontsize=8)
    _save(fig, out_dir / "progression_roc.png")

    fig, axes = plt.subplots(2, 4, figsize=(12, 6.2))
    cell_col = np.array([["#1baf7a", MISSED], ["#e34948", "#1baf7a"]])  # TP, FN / FP, TN
    for ax, (name, (tp, fn, fp, tn)) in zip(axes.ravel(), conf.items()):
        m = np.array([[tp, fn], [fp, tn]])
        share = m / np.maximum(m.sum(axis=1, keepdims=True), 1)
        shown = suppress(m)
        for (i, j), v in np.ndenumerate(shown):
            ax.add_patch(plt.Rectangle((j - 0.48, i - 0.48), 0.96, 0.96, color=cell_col[i, j], alpha=0.18 + 0.75 * share[i, j]))
            ax.text(j, i - 0.08, v, ha="center", va="center", fontsize=13, fontweight="bold", color=INK)
            if not isinstance(v, str):
                ax.text(j, i + 0.22, f"{100 * share[i, j]:.0f}% of row", ha="center", va="center", fontsize=7.5, color=INK2)
        ax.set_xlim(-0.5, 1.5); ax.set_ylim(1.5, -0.5)
        ax.set_xticks([0, 1], ["called\nprogress", "called\nstable"], fontsize=8)
        ax.set_yticks([0, 1], ["progressed", "stable"], fontsize=8)
        ax.tick_params(length=0)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.set_title(name, color=MODEL_COLOR.get(name, INK), fontsize=10)
    legend_ax = axes.ravel()[-1]
    legend_ax.axis("off")
    for k, (lab, col) in enumerate((("correct (TP, TN)", "#1baf7a"), ("missed progression (FN)", MISSED),
                                    ("false alarm (FP)", "#e34948"))):
        legend_ax.add_patch(plt.Rectangle((0.05, 0.75 - 0.18 * k), 0.12, 0.12, color=col, alpha=0.8, transform=legend_ax.transAxes))
        legend_ax.text(0.22, 0.81 - 0.18 * k, lab, transform=legend_ax.transAxes, va="center", fontsize=9, color=INK)
    legend_ax.text(0.05, 0.12, "Darker = larger share of its row.\nCut-off: training-fold progression rate.",
                   transform=legend_ax.transAxes, fontsize=8, color=INK2)
    for ax in axes.ravel()[len(conf):-1]:
        ax.axis("off")
    fig.suptitle("Confusion matrices per model (out-of-fold)", x=0.01, ha="left", fontsize=12, fontweight="bold", color=INK)
    _save(fig, out_dir / "progression_confusion.png")


VESSEL = {"plad": "LAD", "mlad": "LAD", "dlad": "LAD", "pcx": "LCx", "mcx": "LCx", "dcx": "LCx",
          "prca": "RCA", "mrca": "RCA", "drca": "RCA"}


def swaps(d, eta0, eta1, label, sec, out_dir):
    """Within each person: which segments changed rank when the turning variant was added, and was the swap right?"""
    pairs, changed, total = [], 0, 0
    for _, g in d.assign(e0=eta0, e1=eta1).groupby("id"):
        if len(g) < 2:
            continue
        r0, r1 = g["e0"].rank(ascending=False), g["e1"].rank(ascending=False)
        changed += int((r0 != r1).sum()); total += len(g)
        segs, e0, e1, yy = g["segment"].to_numpy(), g["e0"].to_numpy(), g["e1"].to_numpy(), g["y"].to_numpy()
        for i in range(len(g)):
            for j in range(i + 1, len(g)):
                if np.sign(e0[i] - e0[j]) * np.sign(e1[i] - e1[j]) < 0:  # order flipped
                    up = i if e1[i] > e1[j] else j  # the segment geometry moved above the other
                    dn = j if up == i else i
                    verdict = "neutral" if yy[up] == yy[dn] else "correct" if yy[up] == 1 else "wrong"
                    a, b = sorted((segs[i], segs[j]))
                    pairs.append({"segments": f"{a} <-> {b}", "vessels": " <-> ".join(sorted((VESSEL[a], VESSEL[b]))),
                                  "verdict": verdict})
    P = pd.DataFrame(pairs, columns=["segments", "vessels", "verdict"])
    fname = f"progression_swaps_{label.split()[-1]}.png"
    rep = [f"## {sec}. Which segments swapped places in a person's ranking when geometry was added ({label})?\n",
           "Each person's segments are ranked from highest to lowest within-person score (section 2), once without and "
           f"once with {label}. A swap is a pair of the person's segments whose order flipped. It is *correct* when the "
           "segment moved up progressed and the one moved down did not, *wrong* the other way round, and *neutral* "
           "when both progressed or both stayed stable.\n",
           f"Segments whose rank changed: {count(changed)} of {count(total)}. Swapped pairs: {count(len(P))}. "
           f"Figure: {fname}.\n"]
    tables = {}
    for by, title in (("vessels", "By vessel pair"), ("segments", "By segment pair (most frequent 12)")):
        t = pd.crosstab(P[by], P["verdict"]).reindex(columns=["correct", "wrong", "neutral"], fill_value=0) if len(P) else pd.DataFrame()
        if not len(t):
            continue
        t = t.assign(_n=t.sum(axis=1)).sort_values("_n", ascending=False).drop(columns="_n").head(12)
        tables[by] = t
        shown = suppress(t.to_numpy())
        rep += [f"{title}:\n", "| pair | swaps | correct | wrong | neutral |", "|---|---|---|---|---|",
                *[f"| {k} | {count(sum(r))} | " + " | ".join(map(str, sr)) + " |"
                  for k, r, sr in zip(t.index, t.to_numpy(), shown)], ""]
    if tables:
        plt = _plt()
        fig, axes = plt.subplots(1, len(tables), figsize=(12, 4.6), gridspec_kw={"width_ratios": [1, 1.4][:len(tables)]})
        for ax, (by, t) in zip(np.atleast_1d(axes), tables.items()):
            t = t.iloc[::-1]
            yy = np.arange(len(t))
            ok = ~np.array([any(0 < v < 5 for v in r) for r in t.to_numpy()])  # rows with a 1-4 cell: total only
            left = np.zeros(len(t))
            for v in ("correct", "wrong", "neutral"):
                ax.barh(yy[ok], t[v].to_numpy()[ok], left=left[ok], color=VERDICT_COLOR[v], height=0.62, label=v)
                left += t[v].to_numpy()
            tot = t.sum(axis=1).to_numpy()
            big = ~ok & (tot >= 5)  # split hidden but the total itself may be shown
            if big.any():
                ax.barh(yy[big], tot[big], color="#ecebe7", hatch="//", edgecolor=MUTED,
                        height=0.62, label="split hidden (a part is under 5)")
            for y_, n in zip(yy, tot):  # a total under 5 gets no bar at all, only the label
                ax.text(n if n >= 5 else 0, y_, f" {count(n)}", va="center", fontsize=8, color=INK)
            ax.set_yticks(yy, t.index)
            ax.set_xlabel("swapped pairs")
            _grid(ax, "x")
            ax.set_title("by vessel pair" if by == "vessels" else "by segment pair")
        handles = [plt.Rectangle((0, 0), 1, 1, color=VERDICT_COLOR[v]) for v in VERDICT_COLOR]
        handles.append(plt.Rectangle((0, 0), 1, 1, facecolor="#ecebe7", hatch="//", edgecolor=MUTED))
        fig.legend(handles, ["correct: moved-up segment progressed", "wrong: moved-up segment stayed stable",
                             "neutral: both progressed or both stable", "split hidden (a part is under 5)"],
                   loc="lower center", ncol=4, fontsize=8, frameon=False)
        fig.suptitle(f"Ranking swaps within a person when {label} is added: correct, wrong or neutral?",
                     x=0.01, ha="left", fontsize=12, fontweight="bold", color=INK)
        _save(fig, out_dir / fname, rect=(0, 0.08, 1, 1))
    return rep


def top_levels(d, y, p_pt, p_ptg, thr, out_dir, label, sec, levels=(5, 10, 15, 20, 25, 30)):
    """Segments whose risk geometry raised most: at each top-k% level, how many progressed, and how many of
    those the position + time model had missed (false negatives)."""
    delta = p_ptg - p_pt
    base_neg = p_pt <= thr
    rows = []
    for k in levels:
        m = delta >= np.percentile(delta, 100 - k)
        prog = m & (y == 1)
        rows.append({"level": k, "n": int(m.sum()), "trees": d.loc[m, "id"].nunique(), "prog": int(prog.sum()),
                     "rescued": int((prog & base_neg).sum()), "base_tp": int((prog & ~base_neg).sum()),
                     "expected": p_pt[m].sum(), "overall": y.mean() * m.sum()})
    T = pd.DataFrame(rows)
    fname = f"progression_toplevels_{label.split()[-1]}.png"
    rep = [f"## {sec}. Segments whose risk {label} raised most: how many progressed?\n",
           f"Segments are sorted by how much adding {label} raised their risk (position + time vs + {label}, out-of-fold). "
           "At each level the top k% is taken. *Missed by position + time* = progressed although the position + time "
           "model called them stable (risk at or below the training progression rate): these are the base model's false "
           "negatives that geometry flagged. *Expected* = how many position + time alone predicted would progress.\n",
           "| top | segments | trees | progressed | of which missed by position + time | expected by position + time | at the overall rate |",
           "|---|---|---|---|---|---|---|"]
    for r in T.itertuples():
        rep.append(f"| {r.level}% | {count(r.n)} | {count(r.trees)} | {count(r.prog)} ({100 * r.prog / max(r.n, 1):.0f}%) | "
                   f"{count(r.rescued)} | {r.expected:.0f} | {r.overall:.0f} |")
    rep.append("\nIf geometry helps, 'progressed' stays above 'expected by position + time' at every level. "
               f"Figure: {fname}.\n")

    plt = _plt()
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    _grid(ax)
    x = np.arange(len(T))
    small = lambda v: 0 < v < 5
    split_ok = ~(T["rescued"].map(small) | T["base_tp"].map(small))  # never show a count of 1-4 as a bar height
    ax.bar(x[split_ok], T["base_tp"][split_ok], width=0.62, color=FLAGGED, label="progressed - position + time already flagged it")
    ax.bar(x[split_ok], T["rescued"][split_ok], width=0.62, bottom=T["base_tp"][split_ok], color=MISSED,
           label="progressed - position + time missed it, geometry caught it")
    if (~split_ok).any():
        ax.bar(x[~split_ok], T["prog"][~split_ok], width=0.62, color="#ecebe7", hatch="//", edgecolor=MUTED,
               label="progressed (split hidden: a part is under 5)")
    ax.plot(x, T["expected"], "o-", color=INK, lw=1.8, ms=6, label="expected by position + time", zorder=4)
    ax.plot(x, T["overall"], "s--", color=MUTED, lw=1.2, ms=4, label="expected at the overall progression rate", zorder=4)
    for xi, r in zip(x, T.itertuples()):
        ax.text(xi, r.prog + 0.3, f"{count(r.prog)} of {count(r.n)}\n({100 * r.prog / max(r.n, 1):.0f}%)",
                ha="center", va="bottom", fontsize=8, color=INK)
    ax.set_xticks(x, [f"top {k}%" for k in T["level"]])
    ax.set_ylabel("segments that progressed")
    ax.set_ylim(0, max(T["prog"].max(), T["expected"].max()) * 1.35 + 1)
    ax.set_title(f"Segments whose risk {label} raised most: how many progressed?",
                 color=MODEL_COLOR.get(label, INK))
    ax.legend(fontsize=8, loc="upper left")
    _save(fig, out_dir / fname)
    return rep


def extra_plots(W, R, n_inf, out_dir):
    plt = _plt()
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.6), sharey=True, gridspec_kw={"width_ratios": [1, 1.5]})
    yy = np.arange(len(W))[::-1]
    cols = [MODEL_COLOR.get(m, INK) for m in W["model"]]
    for ax, key, title, ref in ((axes[0], "C", "Within-person C", 0.5), (axes[1], "hit", "Top-ranked segment progressed", None)):
        _grid(ax, "x")
        vals = W[key].to_numpy() * (100 if key == "hit" else 1)
        ax.barh(yy, vals, color=cols, height=0.62)
        ax.axvline(vals[0], color=MODEL_COLOR["base"], lw=1.2, ls="--")
        if ref is not None:
            ax.axvline(ref, color=MUTED, lw=1, ls=":")
            ax.text(ref, len(W) - 0.45, " coin flip", color=MUTED, fontsize=8, va="bottom")
        notes = [""] + [f"   top changed in {count(r.changed)}: new {count(r.new_ok)} vs old {count(r.old_ok)} progressed"
                        for r in W.iloc[1:].itertuples()]
        for y_, v, note in zip(yy, vals, notes):
            ax.text(v, y_, (f" {v:.2f}" if key == "C" else f" {v:.0f}%" + note), va="center", fontsize=8, color=INK)
        if key == "hit":
            ax.set_xlim(0, 175)
            ax.set_xticks([0, 25, 50, 75, 100])
            ax.set_xlabel(f"% of {count(n_inf)} people with some but not all segments progressed")
        ax.set_title(title)
    axes[0].set_yticks(yy, W["model"])
    for lab, col in zip(axes[0].get_yticklabels(), cols):  # tick labels follow W's row order
        lab.set_color(col)
        lab.set_fontweight("bold")
    fig.suptitle("Within one person: does geometry rank the progressing segments first?  (dashed = base level)",
                 x=0.01, ha="left", fontsize=12, fontweight="bold", color=INK)
    _save(fig, out_dir / "progression_within.png")

    fig, ax = plt.subplots(figsize=(9, 4.8))
    _grid(ax)
    x = np.arange(len(R))
    for off, key, col, lab in ((-0.28, "pt", MODEL_COLOR["base"], "expected: position + time"),
                               (0, "ptg", MODEL_COLOR["mean T5"], "expected: + mean T5"), (0.28, "obs", MISSED, "observed")):
        ax.bar(x + off, 100 * R[key], width=0.26, color=col, label=lab)
        for xi, v in zip(x + off, 100 * R[key]):
            ax.text(xi, v + 0.4, f"{v:.0f}%", ha="center", va="bottom", fontsize=8, color=INK)
    ax.set_xticks(x, [f"{g}\n(n = {count(n)})" for g, n in zip(R["group"], R["n"])], fontsize=8.5)
    ax.set_ylabel("segments that progressed (%)")
    ax.set_ylim(0, 100 * R[["pt", "ptg", "obs"]].to_numpy().max() * 1.25)
    ax.set_title("When geometry changes a segment's risk, does the segment do what geometry says?")
    ax.legend(fontsize=8, loc="upper center", ncol=3)
    _save(fig, out_dir / "progression_reclass.png")


SEG_ORDER = [sg for segs in NAMES.values() for sg in segs]


def per_segment(d, y, fold, folds, B, rng, out_dir, cols=(("mean_T5", "mean T5"), ("mean_T2.5", "mean T2.5"))):
    """Does turning predict progression better in some segments? One model per variant with a separate
    turning effect for each segment (turning x segment), adjusted for the same base as section 1."""
    segs = [sg for sg in SEG_ORDER if sg in set(d["segment"])]
    seg = d["segment"].to_numpy()
    X0 = design(d)

    def oof(col):
        p = np.zeros(len(d))
        for k in range(folds):
            tr, te = fold != k, fold == k
            if col is None:
                Xtr, Xte = design(d[tr]), design(d[te])
            else:
                z = zscore(d, col, tr)
                inter = lambda m: np.column_stack([z[m] * (seg[m] == sg) for sg in segs])
                Xtr, Xte = np.column_stack([design(d[tr]), inter(tr)]), np.column_stack([design(d[te]), inter(te)])
            p[te] = predict(Xte, fit(Xtr, y[tr])[0])
        return p

    p_base = oof(None)
    res, het = {}, {}
    for col, label in cols:
        z = zscore(d, col, np.ones(len(d), bool))
        X = np.column_stack([X0, *[z * (seg == sg) for sg in segs]])
        w, p_fit, ll1, H = fit(X, y)
        ll_shared = fit(design(d, z), y)[2]
        het[label] = chi2.sf(2 * (ll1 - ll_shared), len(segs) - 1)
        U = pd.DataFrame(X * (y - p_fit)[:, None]).groupby(d["id"].to_numpy()).sum().to_numpy()
        V = np.linalg.inv(H) @ (U.T @ U) @ np.linalg.inv(H)
        p_int = oof(col)
        for i, sg in enumerate(segs):
            m = seg == sg
            k, n = int(y[m].sum()), int(m.sum())
            j = X0.shape[1] + i
            r = {"n": n, "k": k, "ok": min(k, n - k) >= 5 and np.std(z[m]) > 1e-9,
                 "why": "too few events or non-events" if min(k, n - k) < 5 else "turning does not vary here"}
            if r["ok"]:
                b, se = w[j], np.sqrt(V[j, j])
                c0, c1 = auc(y[m], p_base[m])[0], auc(y[m], p_int[m])[0]
                idx = np.where(m)[0]  # one row per person within a segment: resample rows
                bd = []
                for _ in range(B):
                    bi = rng.choice(idx, len(idx))
                    if 0 < y[bi].sum() < len(bi):
                        bd.append(auc(y[bi], p_int[bi])[0] - auc(y[bi], p_base[bi])[0])
                r.update(OR=np.exp(b), lo=np.exp(b - 1.96 * se), hi=np.exp(b + 1.96 * se), p=2 * norm.sf(abs(b / se)),
                         c0=c0, c1=c1, dlo=np.percentile(bd, 2.5), dhi=np.percentile(bd, 97.5))
            res[(label, sg)] = r

    rep = ["## 8. Is geometry better at predicting some segments than others?\n",
           "One model per turning scale gives every segment its own turning effect (turning x segment), adjusted for "
           "SCORE2, follow-up time, position and BL grade as in section 1. T5 and T2.5 are per-segment values: the "
           "turning angles inside that segment's own stretch of the trunk, averaged.\n",
           "- *OR per SD*: odds of progressing per SD more turning than usual for that segment.",
           "- *AUC within segment*: comparing people at that segment only; base vs + turning (out-of-fold), "
           "with the change and a bootstrap interval.",
           "- *Different between segments?*: one test of whether the turning effect varies across the 9 segments "
           "(8 df). Read single segments with care: 18 estimates means some will look strong by chance.\n"]
    for label in het:
        rep.append(f"{label}: different between segments? p = {het[label]:.3g}")
    rep += ["", "| segment | events / segments | scale | OR per SD (95% CI) | p | AUC base | AUC + turning | ΔAUC (95% bootstrap) |",
            "|---|---|---|---|---|---|---|---|"]
    for sg in segs:
        for col, label in cols:
            r = res[(label, sg)]
            ev = f"{count(r['k'])} / {count(r['n'])}"
            if not r["ok"]:
                rep.append(f"| {sg} | {ev} | {label} | {r['why']} | | | | |")
                continue
            rep.append(f"| {sg} | {ev} | {label} | {r['OR']:.2f} ({r['lo']:.2f}–{r['hi']:.2f}) | {r['p']:.3g} | "
                       f"{r['c0']:.3f} | {r['c1']:.3f} | {r['c1'] - r['c0']:+.3f} ({r['dlo']:+.3f} to {r['dhi']:+.3f}) |")
    rep.append("\nFigure: progression_per_segment.png.\n")

    plt = _plt()
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 6.2), sharey=True)
    yy = np.arange(len(segs))[::-1].astype(float)
    for k, (col, label) in enumerate(cols):
        off = (k - 0.5) * 0.28
        colr = MODEL_COLOR[label]
        for y_, sg in zip(yy, segs):
            r = res[(label, sg)]
            if not r["ok"]:
                continue
            axes[0].plot([r["lo"], r["hi"]], [y_ + off] * 2, color=colr, lw=2)
            axes[0].plot(r["OR"], y_ + off, "o", color=colr, ms=7, mec="white", mew=1, label=label if sg == segs[0] else None)
            axes[1].plot([r["dlo"], r["dhi"]], [y_ + off] * 2, color=colr, lw=2)
            axes[1].plot(r["c1"] - r["c0"], y_ + off, "D", color=colr, ms=6, mec="white", mew=1)
    axes[0].axvline(1, color=MUTED, lw=1, ls=":")
    axes[1].axvline(0, color=MUTED, lw=1, ls=":")
    axes[0].set_xscale("log")
    from matplotlib.ticker import FixedLocator, NullLocator
    axes[0].xaxis.set_major_locator(FixedLocator([0.25, 0.5, 1, 2, 4, 8]))
    axes[0].xaxis.set_minor_locator(NullLocator())
    axes[0].set_xticklabels(["0.25", "0.5", "1", "2", "4", "8"])
    vess = [VESSEL[sg] for sg in segs]
    for ax in axes:
        _grid(ax, "x")
        for i in range(1, len(segs)):  # a line between LAD / LCx / RCA groups
            if vess[i] != vess[i - 1]:
                ax.axhline((yy[i] + yy[i - 1]) / 2, color=MUTED, lw=0.8, alpha=0.6)
    labels = [f"{sg}  ({count(res[(cols[0][1], sg)]['k'])}/{count(res[(cols[0][1], sg)]['n'])})" for sg in segs]
    axes[0].set_yticks(yy, labels)
    for lab, sg in zip(axes[0].get_yticklabels(), segs):
        lab.set_color({"LAD": "#2a78d6", "LCx": "#1baf7a", "RCA": "#e34948"}[VESSEL[sg]])
        lab.set_fontweight("bold")
    axes[0].set_xlabel("odds ratio per SD more turning (log scale)")
    axes[0].set_title("Effect of turning, per segment")
    axes[1].set_xlabel("change in AUC within the segment (+ turning vs base)")
    axes[1].set_title("Gain in discrimination, per segment")
    axes[0].legend(fontsize=8, loc="lower right", title="scale", title_fontsize=8)
    het_txt = ", ".join(f"{l}: p = {v:.2g}" for l, v in het.items())
    fig.suptitle(f"Is turning a better predictor in some segments?  Different between segments: {het_txt}",
                 x=0.01, ha="left", fontsize=12, fontweight="bold", color=INK)
    fig.text(0.01, 0.01, "Segment label colour = vessel (LAD blue, LCx aqua, RCA red); (events/segments). "
             "Segments with fewer than 5 events or non-events, or no variation in turning, are left out.", fontsize=8, color=INK2)
    _save(fig, out_dir / "progression_per_segment.png", rect=(0, 0.03, 1, 1))
    return rep


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / "progression_turning.md"))
    ap.add_argument("--folds", type=int, default=10)
    ap.add_argument("--boot", type=int, default=200)
    args = ap.parse_args()
    out_dir = Path(args.out).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    d0, graded = build(args.src)
    keep = graded & d0["mean_T5"].notna() & (d0["score2"] > 0) & (d0["years"] > 0)
    d = d0[keep].assign(grade=lambda x: x["bl"].map(GRADE)).reset_index(drop=True)
    y = d["y"].to_numpy()
    rng = np.random.default_rng(0)
    people = d["id"].unique()
    fold = d["id"].map(dict(zip(rng.permutation(people), np.arange(len(people)) % args.folds))).to_numpy()
    rep = ["# Segment turning and plaque progression (Medis trees)\n",
           "Aggregates only; counts 1-4 shown as <5. Outcome = higher visual grade at FU. Medis trees are mostly "
           "patients with plaque at baseline: this is progression, not new plaque in a clean cohort.\n",
           f"Segments: {count(len(d))} from {count(d['id'].nunique())} people; progressed: {count(int(y.sum()))}. "
           f"Left out: {count(int((~graded).sum()))} without a usable grade or occluded at BL, "
           f"{count(int((graded & ~keep).sum()))} too short for two T5 angles or without SCORE2 / follow-up.\n"]

    # 1. between people
    def cv(z_col, person=True, grade=True):
        p, thr = np.zeros(len(d)), np.zeros(len(d))
        for k in range(args.folds):
            tr, te = fold != k, fold == k
            z = zscore(d, z_col, tr) if z_col else None
            w = fit(design(d[tr], None if z is None else z[tr], person, grade), y[tr])[0]
            p[te] = predict(design(d[te], None if z is None else z[te], person, grade), w)
            thr[te] = y[tr].mean()
        return p, thr

    p_base, thr = cv(None)
    preds, conf = {"base": p_base}, {"base": confusion(y, p_base, thr)}
    c_base = strat_c(d, p_base, "segment")
    rows = []
    _, _, ll0, _ = fit(design(d), y)
    for col, name in VARIANTS.items():
        z = zscore(d, col, np.ones(len(d), bool))
        X = design(d, z)
        w, p_fit, ll1, H = fit(X, y)
        U = pd.DataFrame(X * (y - p_fit)[:, None]).groupby(d["id"].to_numpy()).sum().to_numpy()
        se = np.sqrt((np.linalg.inv(H) @ (U.T @ U) @ np.linalg.inv(H))[-1, -1])
        p_cv, _ = cv(col)
        preds[name], conf[name] = p_cv, confusion(y, p_cv, thr)
        c1 = strat_c(d, p_cv, "segment")
        lo, hi = boot_delta(d, p_base, p_cv, "segment", args.boot, rng)
        rows.append(f"| {name} | {np.exp(w[-1]):.2f} ({np.exp(w[-1] - 1.96 * se):.2f}–{np.exp(w[-1] + 1.96 * se):.2f}) | "
                    f"{2 * norm.sf(abs(w[-1] / se)):.3g} | {chi2.sf(2 * (ll1 - ll0), 1):.3g} | {c1:.3f} | "
                    f"{c1 - c_base:+.3f} ({lo:+.3f} to {hi:+.3f}) | {auc(y, p_cv)[0]:.3f} |")
    rep += ["## 1. Between people: does geometry add to SCORE2 + follow-up (+ position, BL grade)?\n",
            f"Base: position-stratified C {c_base:.3f}, pooled AUC {auc(y, p_base)[0]:.3f}. Each row adds one variant.\n",
            "| variant | OR per SD (95% CI, robust) | robust p | LR p | stratified C | ΔC (95% person bootstrap) | pooled AUC |",
            "|---|---|---|---|---|---|---|", *rows, "",
            "Stratified C = pairs of different people at the same position (the fair test); pooled AUC also rewards "
            "position. Read the robust p as the test and ΔC as an estimate. Six variants are tested: expect about "
            "one p < 0.05 in six by chance alone.\n",
            "Confusion matrices (call \"progresses\" above the training-fold progression rate):\n",
            "| model | TP | FN | FP | TN | sensitivity | specificity |", "|---|---|---|---|---|---|---|"]
    for name, (tp, fn, fp, tn) in conf.items():
        s = suppress([[tp, fn, fp, tn]])[0]
        rep.append(f"| {name} | " + " | ".join(map(str, s)) +
                   f" | {100 * tp / max(tp + fn, 1):.0f}% | {100 * tn / max(tn + fp, 1):.0f}% |")
    plots(y, preds, conf, out_dir)
    rep.append("\nFigures: progression_roc.png (all models), progression_confusion.png.\n")

    # 2. within person
    grp = d["id"].to_numpy()
    informative = d.groupby("id")["y"].agg(lambda v: 0 < v.sum() < len(v))
    n_inf = int(informative.sum())

    def cv_within(z_col):
        eta = np.zeros(len(d))
        for k in range(args.folds):
            tr, te = fold != k, fold == k
            z = zscore(d, z_col, tr) if z_col else None
            b, _ = clogit(within_design(d[tr], None if z is None else z[tr]), y[tr], grp[tr])
            eta[te] = within_design(d[te], None if z is None else z[te]) @ b
        return eta

    def top1(eta):
        top = d.assign(eta=eta).loc[lambda x: x["id"].isin(informative[informative].index)]
        return top.loc[top.groupby("id")["eta"].idxmax()].set_index("id")

    eta0 = cv_within(None)
    etas = {}
    t0 = top1(eta0)
    c0w = strat_c(d, eta0, "id")
    _, ll_w0 = clogit(within_design(d), y, grp)
    within = [{"model": "base", "C": c0w, "hit": t0["y"].mean(), "hits": int(t0["y"].sum()), "p": np.nan,
               "changed": 0, "new_ok": 0, "old_ok": 0}]
    for col, name in VARIANTS.items():
        _, ll_w1 = clogit(within_design(d, zscore(d, col, np.ones(len(d), bool))), y, grp)
        eta1 = cv_within(col)
        etas[col] = eta1
        t1 = top1(eta1)
        changed = t1.index[t1["segment"] != t0.loc[t1.index, "segment"]]
        within.append({"model": name, "C": strat_c(d, eta1, "id"), "hit": t1["y"].mean(), "hits": int(t1["y"].sum()), "p": chi2.sf(2 * (ll_w1 - ll_w0), 1),
                       "changed": len(changed), "new_ok": int(t1.loc[changed, "y"].sum()),
                       "old_ok": int(t0.loc[changed, "y"].sum())})
    W = pd.DataFrame(within)
    rep += ["## 2. Within one person: does geometry pick the right segment?\n",
            "**Question.** Take one person. Their segments differ in position, baseline grade and length, and in "
            "geometry. Does knowing the geometry help rank *that person's* segments, so the ones that progressed come "
            "first? SCORE2 and follow-up time are the same for all of a person's segments, so they play no role here.\n",
            f"**Who counts.** Only people with some but not all segments progressed can be ranked: {count(n_inf)} people.\n",
            "**How to read the columns.**",
            "- *within-person C*: pick one progressed and one stable segment from the same person; the share of such pairs "
            "where the model ranks the progressed one higher. 0.5 = coin flip, 1 = always right.",
            "- *top segment progressed*: share of people whose highest-ranked segment really progressed.",
            "- *top changed / new top progressed / old top progressed*: for how many people adding geometry moved a "
            "different segment to the top, and in how many of those the new top vs the old top had progressed. "
            "Geometry helps if 'new' is larger than 'old'.",
            "- *p*: does geometry improve the within-person fit (likelihood-ratio test)?\n",
            "| model | within-person C | vs base | top segment progressed | top changed | new top progressed | old top progressed | p |",
            "|---|---|---|---|---|---|---|---|"]
    for r in W.itertuples():
        base = r.model == "base"
        rep.append(f"| {r.model} | {r.C:.3f} | {'' if base else f'{r.C - c0w:+.3f}'} | {100 * r.hit:.0f}% "
                   f"({count(r.hits)} of {count(n_inf)}) | {'' if base else count(r.changed)} | "
                   f"{'' if base else count(r.new_ok)} | {'' if base else count(r.old_ok)} | {'' if base else f'{r.p:.3g}'} |")
    best = W.iloc[1:].loc[W.iloc[1:]["C"].idxmax()]
    rep.append(f"\n**In short:** position, baseline grade and length rank the right segment first for "
               f"{100 * W['hit'][0]:.0f}% of people (within-person C {c0w:.2f}). The best geometry variant "
               f"({best['model']}) gives C {best['C']:.2f} ({best['C'] - c0w:+.2f}). Figure: progression_within.png.\n")

    # 3. reclassification: position + time vs + mean T5
    p_pt, thr_pt = cv(None, person=False, grade=False)
    p_ptg, _ = cv("mean_T5", person=False, grade=False)
    delta = p_ptg - p_pt
    q10, q90 = np.percentile(delta, [10, 90])
    groups = {"geometry raised the risk most (top 10%)": delta >= q90, "little change (middle 80%)": (delta > q10) & (delta < q90),
              "geometry lowered the risk most (bottom 10%)": delta <= q10}
    R = pd.DataFrame([{"group": g, "n": int(m.sum()), "k": int(y[m].sum()), "obs": y[m].mean(),
                       "pt": p_pt[m].mean(), "ptg": p_ptg[m].mean()} for g, m in groups.items()])
    rep += ["## 3. When geometry changes a segment's risk, is it right?\n",
            "**Question.** Predict each segment's risk twice, out-of-fold: with position + follow-up time only, and with "
            "mean T5 added. For most segments geometry barely changes the risk. Look at the 10% it pushed up most and the "
            "10% it pushed down most, and check what actually happened.\n",
            "**How to read it.** If geometry is right, segments it pushed *up* progress more often than the position + time "
            "model expected (observed above the grey bar), and segments it pushed *down* progress less often.\n",
            "| segments | n | progressed | observed | expected, position + time | expected, + geometry |",
            "|---|---|---|---|---|---|"]
    for r in R.itertuples():
        rep.append(f"| {r.group} | {count(r.n)} | {count(r.k)} | {100 * r.obs:.0f}% | {100 * r.pt:.0f}% | {100 * r.ptg:.0f}% |")
    up, down = R.iloc[0], R.iloc[2]
    verdict = ("geometry moved the risk in the right direction in both groups" if up.obs > up.pt and down.obs < down.pt
               else "geometry did not consistently move the risk in the right direction")
    rep.append(f"\n**In short:** where geometry raised the risk, {100 * up.obs:.0f}% progressed (position + time expected "
               f"{100 * up.pt:.0f}%); where it lowered the risk, {100 * down.obs:.0f}% progressed (expected "
               f"{100 * down.pt:.0f}%): {verdict}. Figure: progression_reclass.png.\n")
    extra_plots(W, R, n_inf, out_dir)
    for k, (col, label) in enumerate((("mean_T5", "mean T5"), ("mean_T2.5", "mean T2.5"))):
        rep += swaps(d, eta0, etas[col], label, 4 + 2 * k, out_dir)
        p_g = p_ptg if col == "mean_T5" else cv(col, person=False, grade=False)[0]
        rep += top_levels(d, y, p_pt, p_g, thr_pt, out_dir, label, 5 + 2 * k)

    rep += per_segment(d, y, fold, args.folds, min(args.boot, 300), rng, out_dir)
    Path(args.out).write_text("\n".join(rep), encoding="utf-8")
    print("\n".join(rep))
    print(f"wrote {args.out} and progression_*.png in {out_dir}")


if __name__ == "__main__":
    main()
