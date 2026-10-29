"""Do segment turning and the LM bifurcation angle predict plaque progression in the proximal LAD and LCx?

    python progression_angle.py [--src TREE_FOLDER] [--folds 10] [--boot 200]

Rows: the proximal LAD and proximal LCx segments of each Medis tree (progression_turning.build), the two
segments the LM bifurcation angle can act on. Same outcome, base models, person folds and seed as
progression_turning.py. Taper and the LM->LAD / LM->LCx diameter ratios wait for a lumen radius.

Geometry, z-scored in the training folds (missing -> 0, the mean):
  turning = mean T5 of the segment, within segment;
  angle   = LM bifurcation angle (who_where_readiness.lm_bifurcation_angle), one value per person, over people.
Models: base, + turning, + angle, + turning + angle (all features), + turning x angle.
Within person (clogit) the angle enters as angle x pLAD row: a person-level main effect cancels.

1. Between people (logistic, base = position + BL grade + log SCORE2 + log follow-up): OR per SD (robust),
   LR p vs base, stratified C, ΔC, pooled AUC; ROC, AUC bars, confusion matrices; drop-one LR tests in the
   full model; complete-case sensitivity.
2. Within person (base = position + BL grade + log length): within-person C, top segment progressed, LR p.
3. Reclassification per model (position + time vs + geometry), and which segment the raised risk fell on.
4. Swaps and top-k% levels per model; per-segment effects (pLAD vs pCX).
Aggregates only (counts 1-4 hidden); writes progression_angle.md and progression_angle_*.png.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, norm

import hoe10y_qc as hq
import progression_turning as pt
from cgps_stats import OUT_DIR, count, suppress
from who_where_readiness import lm_bifurcation_angle, segment_runs

ROWS = ("plad", "pcx")
PREFIX = "progression_angle"
MODELS = {"base": (), "turning": ("turning",), "angle": ("angle",), "turning + angle": ("turning", "angle"),
          "turning × angle": ("turning", "angle", "turning × angle")}
TAG = {"turning": "turning", "angle": "angle", "turning + angle": "turning_angle", "turning × angle": "turning_x_angle"}
FULL = "turning + angle"  # every geometric feature active
DROPS = (("turning, given angle", FULL, "angle"), ("angle, given turning", FULL, "turning"),
         ("turning × angle, given both", "turning × angle", FULL))


# ---------------------------------------------------------------- features
def angles(src):
    """{id: LM bifurcation angle (deg)} per Medis tree; NaN where the LM, LAD or LCx has no run."""
    files = sorted(Path(src).rglob("*.vtk"))
    hq.tree_topology([{"visit": "BL", "id": hq.id_from_name(f.name), "path": f} for f in files])  # label coding
    out = {}
    for f in files:
        try:
            out[hq.id_from_name(f.name)] = lm_bifurcation_angle(segment_runs(hq.tree_points(f)))
        except Exception:  # noqa: BLE001 - counted as missing
            out[hq.id_from_name(f.name)] = np.nan
    return pd.Series(out, dtype=float)


def geometry(d, terms, train, within=False):
    """Geometry columns (n, k) of one model, z-scored on the training rows; None for the base."""
    if not terms:
        return None
    t = pt.zscore(d, "mean_T5", train)
    people = d[train].drop_duplicates("id")["angle"]
    a = ((d["angle"] - people.mean()) / people.std()).fillna(0).to_numpy()
    col = {"turning": t, "angle": a * (d["segment"] == "plad").to_numpy() if within else a, "turning × angle": t * a}
    return np.column_stack([col[k] for k in terms])


def rows_of(Z, m):
    return None if Z is None else Z[m]


# ---------------------------------------------------------------- models
def cv(d, y, fold, folds, terms, person=True, grade=True):
    p, thr = np.zeros(len(d)), np.zeros(len(d))
    for k in range(folds):
        tr, te = fold != k, fold == k
        Z = geometry(d, terms, tr)
        w = pt.fit(pt.design(d[tr], rows_of(Z, tr), person, grade), y[tr])[0]
        p[te] = pt.predict(pt.design(d[te], rows_of(Z, te), person, grade), w)
        thr[te] = y[tr].mean()
    return p, thr


def cv_within(d, y, fold, folds, terms):
    grp, eta = d["id"].to_numpy(), np.zeros(len(d))
    for k in range(folds):
        tr, te = fold != k, fold == k
        Z = geometry(d, terms, tr, within=True)
        b, _ = pt.clogit(pt.within_design(d[tr], rows_of(Z, tr)), y[tr], grp[tr])
        eta[te] = pt.within_design(d[te], rows_of(Z, te)) @ b
    return eta


def between_fit(d, y, terms):
    """Log-likelihood, geometry coefficients and their person-clustered robust SEs."""
    Z = geometry(d, terms, np.ones(len(d), bool))
    X = pt.design(d, Z)
    w, p, ll, H = pt.fit(X, y)
    U = pd.DataFrame(X * (y - p)[:, None]).groupby(d["id"].to_numpy()).sum().to_numpy()
    Hi = np.linalg.inv(H)
    se = np.sqrt(np.diag(Hi @ (U.T @ U) @ Hi))
    k = len(terms)
    return ll, w[len(w) - k:], se[len(se) - k:]


def within_ll(d, y, terms):
    Z = geometry(d, terms, np.ones(len(d), bool), within=True)
    return pt.clogit(pt.within_design(d, Z), y, d["id"].to_numpy())[1]


def lr_p(ll1, ll0, df):
    return chi2.sf(max(2 * (ll1 - ll0), 0.0), df)


# ---------------------------------------------------------------- figures
def auc_bars(d, y, preds, B, rng, out_dir):
    """Pooled AUC and position-stratified C per model, with person-bootstrap 95% intervals."""
    idx_of, people = d.groupby("id").indices, d["id"].unique()
    boot = {n: [] for n in preds}
    for _ in range(B):
        idx = np.concatenate([idx_of[i] for i in rng.choice(people, len(people))])
        db = d.iloc[idx].reset_index(drop=True)
        for n, p in preds.items():
            boot[n].append((pt.auc(y[idx], p[idx])[0], pt.strat_c(db, p[idx], "segment")))
    T = pd.DataFrame([{"model": n, "auc": pt.auc(y, p)[0], "c": pt.strat_c(d, p, "segment"),
                       **dict(zip(("auc_lo", "c_lo"), np.nanpercentile(boot[n], 2.5, axis=0))),
                       **dict(zip(("auc_hi", "c_hi"), np.nanpercentile(boot[n], 97.5, axis=0)))} for n, p in preds.items()])

    plt = pt._plt()
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 3.8), sharey=True)
    yy = np.arange(len(T))[::-1]
    cols = [pt.MODEL_COLOR.get(m, pt.INK) for m in T["model"]]
    for ax, key, title in ((axes[0], "auc", "Pooled AUC (also rewards position)"),
                           (axes[1], "c", "Position-stratified C (people at the same segment)")):
        pt._grid(ax, "x")
        v, lo, hi = T[key].to_numpy(), T[f"{key}_lo"].to_numpy(), T[f"{key}_hi"].to_numpy()
        for y_, val, a, b, c in zip(yy, v, lo, hi, cols):
            ax.plot([a, b], [y_, y_], color=c, lw=2.2, solid_capstyle="round")
            ax.plot(val, y_, "o", color=c, ms=8, mec="white", mew=1)
            ax.text(b + 0.004, y_, f" {val:.3f}", va="center", fontsize=8, color=pt.INK)
        ax.axvline(v[0], color=pt.MODEL_COLOR["base"], lw=1.2, ls="--")
        x0, x1 = min(lo.min(), 0.5) - 0.02, max(hi.max(), 0.5) + 0.05
        ax.axvline(0.5, color=pt.MUTED, lw=1, ls=":")
        ax.set_xlim(x0, x1)
        ax.set_ylim(-0.6, len(T) - 0.4)
        ax.set_xlabel("out-of-fold (dotted = 0.5, coin flip)")
        ax.set_title(title)
    axes[0].set_yticks(yy, T["model"])
    for lab, col in zip(axes[0].get_yticklabels(), cols):
        lab.set_color(col)
        lab.set_fontweight("bold")
    fig.suptitle("Proximal LAD + LCx: discrimination per model  (dashed = base, lines = person bootstrap 95%)",
                 x=0.01, ha="left", fontsize=12, fontweight="bold", color=pt.INK)
    pt._save(fig, out_dir / f"{PREFIX}_auc.png")
    return T


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / "progression_angle.md"))
    ap.add_argument("--folds", type=int, default=10)
    ap.add_argument("--boot", type=int, default=200)
    args = ap.parse_args()
    out_dir = Path(args.out).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    # the same rows, person folds and seed as progression_turning.py, then only pLAD + pCX
    d0, graded, _ = pt.build(args.src)
    keep = graded & d0["mean_T5"].notna() & (d0["score2"] > 0) & (d0["years"] > 0)
    d = d0[keep].assign(grade=lambda x: x["bl"].map(pt.GRADE)).reset_index(drop=True)
    rng = np.random.default_rng(0)
    people = d["id"].unique()
    fold_of = dict(zip(rng.permutation(people), np.arange(len(people)) % args.folds))
    ang = angles(args.src)
    d = d[d["segment"].isin(ROWS)].assign(angle=lambda x: x["id"].map(ang)).reset_index(drop=True)
    fold = d["id"].map(fold_of).to_numpy()
    y = d["y"].to_numpy()
    n_ang = d.drop_duplicates("id")["angle"].notna().sum()
    seg_n = d.groupby("segment")["y"].agg(["size", "sum"])
    rep = ["# Turning and the LM bifurcation angle: progression in the proximal LAD and LCx (Medis trees)\n",
           "Aggregates only; counts 1-4 shown as <5. Outcome = higher visual grade at FU. Medis trees are mostly "
           "patients with plaque at baseline: this is progression, not new plaque in a clean cohort. Taper and the "
           "LM->LAD / LM->LCx diameter ratios are not in yet: the Medis trees have no lumen radius.\n",
           f"Rows: proximal LAD and proximal LCx only, the segments the LM angle can act on. Segments: {count(len(d))} "
           f"from {count(d['id'].nunique())} people; progressed: {count(int(y.sum()))} "
           f"(pLAD {count(seg_n.loc['plad', 'sum'])} / {count(seg_n.loc['plad', 'size'])}, "
           f"pCX {count(seg_n.loc['pcx', 'sum'])} / {count(seg_n.loc['pcx', 'size'])}). "
           f"LM bifurcation angle measurable in {count(n_ang)} of {count(d['id'].nunique())} people "
           f"(median {d.drop_duplicates('id')['angle'].median():.0f} deg); missing angles get z = 0.\n",
           "Models: *turning* = mean T5 of the segment; *angle* = LM bifurcation angle; *turning + angle* = every "
           "geometric feature active; *turning × angle* = that plus their product. Same person folds and seed as "
           "progression_turning.md.\n"]

    # 1. between people
    preds, conf, fits, thr = {}, {}, {}, None
    for name, terms in MODELS.items():
        p, thr = cv(d, y, fold, args.folds, terms)
        preds[name], conf[name], fits[name] = p, pt.confusion(y, p, thr), between_fit(d, y, terms)
    c_base = pt.strat_c(d, preds["base"], "segment")
    rows = []
    for name, terms in list(MODELS.items())[1:]:
        ll, w, se = fits[name]
        ors = "; ".join(f"{t} {np.exp(b):.2f} ({np.exp(b - 1.96 * s):.2f}–{np.exp(b + 1.96 * s):.2f}), "
                        f"p {2 * norm.sf(abs(b / s)):.3g}" for t, b, s in zip(terms, w, se))
        c1 = pt.strat_c(d, preds[name], "segment")
        lo, hi = pt.boot_delta(d, preds["base"], preds[name], "segment", args.boot, rng)
        rows.append(f"| {name} | {ors} | {lr_p(ll, fits['base'][0], len(terms)):.3g} ({len(terms)} df) | {c1:.3f} | "
                    f"{c1 - c_base:+.3f} ({lo:+.3f} to {hi:+.3f}) | {pt.auc(y, preds[name])[0]:.3f} |")
    rep += ["## 1. Between people: does geometry add to SCORE2 + follow-up (+ position, BL grade)?\n",
            f"Base: position-stratified C {c_base:.3f}, pooled AUC {pt.auc(y, preds['base'])[0]:.3f}.\n",
            "### Each model against the base\n",
            "| model | OR per SD (95% CI, robust), robust p | LR p vs base | stratified C | ΔC (95% person bootstrap) | pooled AUC |",
            "|---|---|---|---|---|---|", *rows, "",
            "Stratified C = pairs of different people at the same segment (the fair test); pooled AUC also rewards "
            "position. The interaction OR is per SD of turning per SD of angle. Four models are tested against the "
            "base: expect a p < 0.05 now and then by chance alone.\n"]

    wll = {name: within_ll(d, y, terms) for name, terms in MODELS.items()}
    rep += ["### Each feature with the others already in (drop-one LR tests)\n",
            f"Does a feature still add once every other feature is in the model? Full model = {FULL} "
            "(the interaction is tested on top of it).\n",
            "| feature | between people p | within person p |", "|---|---|---|"]
    for lab, big, small in DROPS:
        df = len(MODELS[big]) - len(MODELS[small])
        rep.append(f"| {lab} | {lr_p(fits[big][0], fits[small][0], df):.3g} | {lr_p(wll[big], wll[small], df):.3g} |")

    cc = d["angle"].notna().to_numpy()
    dc, yc = d[cc].reset_index(drop=True), y[cc]
    fc = {name: between_fit(dc, yc, terms)[0] for name, terms in MODELS.items()}
    wc = {name: within_ll(dc, yc, terms) for name, terms in MODELS.items()}
    rep += ["", f"### Complete cases (angle measured): {count(int(cc.sum()))} segments, "
            f"{count(dc['id'].nunique())} people, {count(int(yc.sum()))} progressed\n",
            "| model | between people LR p vs base | within person LR p vs base |", "|---|---|---|"]
    for name, terms in list(MODELS.items())[1:]:
        rep.append(f"| {name} | {lr_p(fc[name], fc['base'], len(terms)):.3g} | {lr_p(wc[name], wc['base'], len(terms)):.3g} |")

    T = auc_bars(d, y, preds, args.boot, rng, out_dir)
    rep += ["", "### Discrimination per model (person bootstrap 95%)\n",
            "| model | pooled AUC | stratified C |", "|---|---|---|",
            *[f"| {r.model} | {r.auc:.3f} ({r.auc_lo:.3f}–{r.auc_hi:.3f}) | {r.c:.3f} ({r.c_lo:.3f}–{r.c_hi:.3f}) |"
              for r in T.itertuples()],
            "", "Confusion matrices (call \"progresses\" above the training-fold progression rate):\n",
            "| model | TP | FN | FP | TN | sensitivity | specificity |", "|---|---|---|---|---|---|---|"]
    for name, (tp, fn, fp, tn) in conf.items():
        s = suppress([[tp, fn, fp, tn]])[0]
        rep.append(f"| {name} | " + " | ".join(map(str, s)) +
                   f" | {100 * tp / max(tp + fn, 1):.0f}% | {100 * tn / max(tn + fp, 1):.0f}% |")
    pt.plots(y, preds, conf, out_dir, prefix=PREFIX)
    rep.append(f"\nFigures: {PREFIX}_auc.png, {PREFIX}_roc.png, {PREFIX}_confusion.png.\n")

    # 2. within person
    informative = d.groupby("id")["y"].agg(lambda v: 0 < v.sum() < len(v))
    n_inf = int(informative.sum())

    def top1(eta):
        top = d.assign(eta=eta).loc[lambda x: x["id"].isin(informative[informative].index)]
        return top.loc[top.groupby("id")["eta"].idxmax()].set_index("id")

    etas = {name: cv_within(d, y, fold, args.folds, terms) for name, terms in MODELS.items()}
    t0, c0w = top1(etas["base"]), pt.strat_c(d, etas["base"], "id")
    within = [{"model": "base", "C": c0w, "hit": t0["y"].mean(), "hits": int(t0["y"].sum()), "p": np.nan,
               "changed": 0, "new_ok": 0, "old_ok": 0}]
    for name, terms in list(MODELS.items())[1:]:
        t1 = top1(etas[name])
        changed = t1.index[t1["segment"] != t0.loc[t1.index, "segment"]]
        within.append({"model": name, "C": pt.strat_c(d, etas[name], "id"), "hit": t1["y"].mean(),
                       "hits": int(t1["y"].sum()), "p": lr_p(wll[name], wll["base"], len(terms)),
                       "changed": len(changed), "new_ok": int(t1.loc[changed, "y"].sum()),
                       "old_ok": int(t0.loc[changed, "y"].sum())})
    W = pd.DataFrame(within)
    rep += ["## 2. Within one person: pLAD or pLCx, which one progresses?\n",
            "Each person has two rows, so only people with exactly one of the two progressed can be ranked: "
            f"{count(n_inf)} people. Within-person C and *top segment progressed* are then the same thing. "
            "SCORE2 and follow-up cancel; the angle enters as angle × pLAD, so a wider angle shifts the risk "
            "between the two daughters.\n",
            "| model | within-person C | vs base | top segment progressed | top changed | new top progressed | old top progressed | LR p vs base |",
            "|---|---|---|---|---|---|---|---|"]
    for r in W.itertuples():
        base = r.model == "base"
        rep.append(f"| {r.model} | {r.C:.3f} | {'' if base else f'{r.C - c0w:+.3f}'} | {100 * r.hit:.0f}% "
                   f"({count(r.hits)} of {count(n_inf)}) | {'' if base else count(r.changed)} | "
                   f"{'' if base else count(r.new_ok)} | {'' if base else count(r.old_ok)} | {'' if base else f'{r.p:.3g}'} |")
    rep.append(f"\nFigure: {PREFIX}_within.png.\n")

    # 3. reclassification: position + time vs + geometry, and where the raised risk fell
    p_pt, thr_pt = cv(d, y, fold, args.folds, (), person=False, grade=False)
    p_g = {name: cv(d, y, fold, args.folds, terms, person=False, grade=False)[0] for name, terms in list(MODELS.items())[1:]}
    rep += ["## 3. When geometry changes a segment's risk, is it right, and on which segment?\n",
            "Each segment's risk is predicted twice, out-of-fold: position + follow-up time only, and with the "
            "geometry of the model added. The 10% it pushed up most and the 10% it pushed down most are compared with "
            "what happened. Geometry is right when the pushed-up segments progress more often than position + time "
            "expected, and the pushed-down ones less often.\n",
            "| model | segments | n | progressed | observed | expected, position + time | expected, + geometry |",
            "|---|---|---|---|---|---|---|"]
    by_seg, R_full = [], None
    for name, pg in p_g.items():
        delta = pg - p_pt
        q10, q90 = np.percentile(delta, [10, 90])
        groups = {"raised most (top 10%)": delta >= q90, "little change (middle 80%)": (delta > q10) & (delta < q90),
                  "lowered most (bottom 10%)": delta <= q10}
        R = pd.DataFrame([{"group": g, "n": int(m.sum()), "k": int(y[m].sum()), "obs": y[m].mean(),
                           "pt": p_pt[m].mean(), "ptg": pg[m].mean()} for g, m in groups.items()])
        R_full = R if name == FULL else R_full
        for r in R.itertuples():
            rep.append(f"| {name} | {r.group} | {count(r.n)} | {count(r.k)} | {100 * r.obs:.0f}% | {100 * r.pt:.0f}% | "
                       f"{100 * r.ptg:.0f}% |")
        for g in ("raised most (top 10%)", "lowered most (bottom 10%)"):
            for sg in ROWS:
                m = groups[g] & (d["segment"] == sg).to_numpy()
                by_seg.append({"model": name, "group": g, "segment": sg, "n": int(m.sum()), "k": int(y[m].sum()),
                               "share": m.sum() / max(groups[g].sum(), 1), "pt": p_pt[m].mean() if m.any() else np.nan})
    rep += ["", "**Which segment did geometry raise or lower?** The top and bottom 10% split by segment: how many "
            "of them are pLAD or pLCx, and how many of those progressed (observed vs position + time expected).\n",
            "| model | segments | segment | n (share of the group) | progressed | observed | expected, position + time |",
            "|---|---|---|---|---|---|---|"]
    for r in pd.DataFrame(by_seg).itertuples():
        obs = f"{100 * r.k / r.n:.0f}%" if r.n else ""
        exp = f"{100 * r.pt:.0f}%" if r.n else ""
        rep.append(f"| {r.model} | {r.group} | {r.segment} | {count(r.n)} ({100 * r.share:.0f}%) | {count(r.k)} | {obs} | {exp} |")
    rep.append(f"\nFigure: {PREFIX}_reclass.png ({FULL}).\n")
    pt.extra_plots(W, R_full.assign(group=lambda x: "geometry " + x["group"]), n_inf, out_dir, prefix=PREFIX, label=FULL)

    # 4. per model: swaps within a person and the top-k% levels; then per segment
    sec = 4
    for name in p_g:
        rep += pt.swaps(d, etas["base"], etas[name], name, sec, out_dir, prefix=PREFIX, tag=TAG[name])
        rep += pt.top_levels(d, y, p_pt, p_g[name], thr_pt, out_dir, name, sec + 1, prefix=PREFIX, tag=TAG[name])
        sec += 2
    rep += pt.per_segment(d, y, fold, args.folds, min(args.boot, 300), rng, out_dir,
                          cols=(("mean_T5", "turning"), ("angle", "angle")), prefix=PREFIX, sec=sec,
                          what="geometry", unit="feature",
                          note="Turning is the segment's own mean T5; the angle is the person's LM bifurcation angle.")
    Path(args.out).write_text("\n".join(rep), encoding="utf-8")
    print("\n".join(rep))
    print(f"wrote {args.out} and {PREFIX}_*.png in {out_dir}")


if __name__ == "__main__":
    main()
