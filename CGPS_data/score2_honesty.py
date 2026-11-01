"""Is published SCORE2, without refitting, an honest base for the 'who' question?

    python CGPS_data/score2_honesty.py                  # 20 CV repeats, 200 bootstrap replicates
    python CGPS_data/score2_honesty.py --boot 0         # point estimates only (fast)

Compares, in the clean-baseline cohort (who_where_readiness.cohort), person-level cloglog models
for any new plaque (>= minimal) in the 9 trunk segments at FU:
- follow-up only (null),
- age + sex,
- SCORE2 recalibrated: cloglog(SCORE2 risk) with a free intercept and slope (score2, else score2_op),
- SCORE2 + age + sex (catches SCORE2 weighting age and sex differently for plaque than for CVD),
- refitted SCORE2 factors (age, sex, current smoking, SBP, total cholesterol, HDL, diabetes).
Every model has log(follow-up years) and uses the same complete-case rows.

Reported: apparent and out-of-fold C (person-split, stratified 5-fold CV, repeated), out-of-fold
calibration intercept and slope, Brier score and log-loss, refit - SCORE2 delta C with a person
bootstrap interval (CV redone inside each replicate, folds assigned by original person so a
duplicated person never sits in both training and test), the SCORE2 slope with a Wald interval,
and observed vs predicted risk by fifth of out-of-fold risk. Delta C is estimated, not tested.

DECISION_DC is the prespecified rule: if refit - SCORE2 out-of-fold delta C >= DECISION_DC, the
refitted factors are the primary 'who' base; otherwise recalibrated SCORE2 is. Fix it before running.

Privacy: aggregates only, small counts suppressed with the cgps_stats.py rules, no study_id.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from cgps_stats import BL_PATH, FU_PATH, MIN_CELL, OUT_DIR, auc, cell, count, count_of, num, pct, yes
from who_where_readiness import TRUNKS, Report, build, cohort, fmt

OUT_FILE = str(Path(OUT_DIR) / "score2_honesty.md")
FOLDS = 5
REPEATS = 20
BOOT = 200
SEED = 0
DECISION_DC = 0.02  # prespecified: refit - SCORE2 delta C at or above this makes the refit the primary base
TRUNK_SEGMENTS = tuple(s for segs in TRUNKS.values() for s in segs)
FACTORS = ("age", "male", "smoking", "sbp", "tot_chol", "hdl", "diabetes")
MODELS = {  # name: predictors besides the intercept and log(follow-up)
    "follow-up only": (),
    "age + sex": ("age", "male"),
    "SCORE2 recalibrated": ("score2_cll",),
    "SCORE2 + age + sex": ("score2_cll", "age", "male"),
    "refitted SCORE2 factors": FACTORS,
}
SCORE2_MODEL, REFIT_MODEL = "SCORE2 recalibrated", "refitted SCORE2 factors"


# ---------------------------------------------------------------- cloglog fit (no statsmodels needed)
def cloglog_fit(X, y, offset=None, l2=1e-6):
    """Fisher scoring for P(y = 1) = 1 - exp(-exp(X w + offset)). Returns (w, covariance)."""
    off = np.zeros(len(y)) if offset is None else offset
    w = np.zeros(X.shape[1])
    w[0] = np.log(-np.log(1 - np.clip(y.mean(), 1e-3, 1 - 1e-3)))
    for _ in range(100):
        eta = np.clip(X @ w + off, -30, 5)
        mu = np.clip(1 - np.exp(-np.exp(eta)), 1e-10, 1 - 1e-10)
        d = np.exp(eta - np.exp(eta))
        W = d * d / (mu * (1 - mu))
        H = X.T @ (X * W[:, None]) + l2 * np.eye(len(w))
        step = np.linalg.solve(H, X.T @ ((y - mu) * d / (mu * (1 - mu))) - l2 * w)
        w += step
        if np.abs(step).max() < 1e-8:
            break
    return w, np.linalg.inv(H)


def risk(eta):
    return 1 - np.exp(-np.exp(np.clip(eta, -30, 5)))


def design(d, cols, ref):
    """Intercept + log(follow-up) + cols, standardised with the training rows `ref`."""
    cols = ("log_fu",) + tuple(cols)
    Z = [(d[c].to_numpy(float) - ref[c].mean()) / (ref[c].std() or 1.0) for c in cols]
    return np.column_stack([np.ones(len(d))] + Z)


def calibration(lp, y):
    """Calibration intercept (offset lp, intercept only) and slope (y on lp)."""
    one = np.ones((len(y), 1))
    a, _ = cloglog_fit(one, y, offset=lp)
    b, _ = cloglog_fit(np.column_stack([one, lp]), y)
    return a[0], b[1]


def folds(ids, y, seed):
    """{id: fold}, stratified on the outcome."""
    rng = np.random.default_rng(seed)
    out = {}
    for val in (0, 1):
        grp = np.array(sorted(ids[y == val]), dtype=object)
        rng.shuffle(grp)
        out.update({i: n % FOLDS for n, i in enumerate(grp)})
    return out


def oof_lp(d, cols, fold):
    """Out-of-fold linear predictor. `fold` is per row (bootstrap duplicates share a fold)."""
    lp = np.empty(len(d))
    for k in range(FOLDS):
        te = fold == k
        tr = d[~te]
        w, _ = cloglog_fit(design(tr, cols, tr), tr["y"].to_numpy(float))
        lp[te] = design(d[te], cols, tr) @ w
    return lp


def c_stat(lp, y):
    return auc(pd.Series(lp), pd.Series(y))


# ---------------------------------------------------------------- data
def person_table(rep, bl, fu, fu_dec, ids):
    g = fu_dec.loc[ids, [f"ct_cag_{s}_stenosis" for s in TRUNK_SEGMENTS]]
    y = (g >= 1).any(axis=1).astype(float).where(g.notna().any(axis=1))
    segs_all = [c for c in fu_dec.columns if c.startswith("ct_cag_") and c.endswith("_stenosis")]
    elsewhere = (fu_dec.loc[ids, segs_all] >= 1).any(axis=1) & (y == 0)
    uncertain = (y == 0) & g.isna().any(axis=1)

    years = (pd.to_datetime(fu.loc[ids, "scandate"], errors="coerce") -
             pd.to_datetime(bl.loc[ids, "scandate"], errors="coerce")).dt.days / 365.25
    s2 = num(bl.loc[ids, "score2"]).fillna(num(bl.loc[ids, "score2_op"]))
    s2 = s2 / 100 if s2.median() > 1 else s2  # stored as % or as a fraction
    d = pd.DataFrame({
        "y": y,
        "log_fu": np.log(years.where(years > 0)),
        "score2_cll": np.log(-np.log(1 - s2.clip(1e-4, 0.999))),
        "age": num(bl.loc[ids, "scan_age"]),
        "male": num(bl.loc[ids, "male"]),
        "smoking": yes(bl.loc[ids, "hist_smoking_current"]),
        "sbp": num(bl.loc[ids, "clin_bp_sys_mean"]),
        "tot_chol": num(bl.loc[ids, "tot_cholesterol"]),
        "hdl": num(bl.loc[ids, "hdl"]),
        "diabetes": yes(bl.loc[ids, "diabetes"]),
    }, index=ids)

    rep("## 2. Outcome and complete cases",
        "Outcome: any trunk segment (LAD, CX, RCA proximal/mid/distal) >= minimal at FU. Plaque only in "
        "the LM or side branches counts as no plaque.")
    n, k = int(y.notna().sum()), int((y == 1).sum())
    rows = [("people with an outcome", count(n)), ("new trunk plaque", count_of(k, n)), ("%", pct(k, n)),
            ("no trunk plaque, but plaque in LM / side branch (counted 0)", count(int(elsewhere.sum()))),
            ("no trunk plaque, >= 1 trunk segment unevaluable", count(int(uncertain.sum())))]
    rows += [(f"missing {c}", count(int(d[c].isna().sum()))) for c in d.columns if c != "y"]
    full = d.dropna()
    rows.append(("complete cases (used by every model)", count(len(full))))
    rep.table(rows, ["", "n"])
    rep(f"SCORE2 risk in the complete cases: median {fmt(s2.loc[full.index].median(), 3)} "
        f"(as a fraction); new plaque {cell(full['y'])}.")
    return full


# ---------------------------------------------------------------- analyses
def point_estimates(rep, d, repeats):
    y = d["y"].to_numpy(float)
    ids = d.index.to_numpy()
    res = {m: {"app": None, "c": [], "a": [], "b": [], "brier": [], "ll": []} for m in MODELS}
    lps = {m: [] for m in MODELS}
    for m, cols in MODELS.items():
        w, _ = cloglog_fit(design(d, cols, d), y)
        res[m]["app"] = c_stat(design(d, cols, d) @ w, y)
    for r in range(repeats):
        fmap = folds(ids, y, SEED + r)
        fold = np.array([fmap[i] for i in ids])
        for m, cols in MODELS.items():
            lp = oof_lp(d, cols, fold)
            p = np.clip(risk(lp), 1e-10, 1 - 1e-10)
            a, b = calibration(lp, y)
            res[m]["c"].append(c_stat(lp, y))
            res[m]["a"].append(a)
            res[m]["b"].append(b)
            res[m]["brier"].append(np.mean((p - y) ** 2))
            res[m]["ll"].append(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))
            lps[m].append(lp)

    rep("## 3. Discrimination and calibration",
        f"Out-of-fold values are means over {repeats} repeats of person-split, outcome-stratified "
        f"{FOLDS}-fold CV. Calibration slope 1 and intercept 0 are perfect; a slope below 1 means "
        "the predictions are too extreme (overfitting). Apparent C uses the same rows it was fitted on.")
    rows = []
    for m, cols in MODELS.items():
        v = res[m]
        rows.append((m, 2 + len(cols), fmt(v["app"]), fmt(np.mean(v["c"])), fmt(np.mean(v["a"])),
                     fmt(np.mean(v["b"])), fmt(np.mean(v["brier"]), 4), fmt(np.mean(v["ll"]), 4)))
    rep.table(rows, ["model", "parameters", "apparent C", "OOF C", "calibration intercept",
                     "calibration slope", "Brier", "log-loss"])
    return res, {m: np.mean(v, axis=0) for m, v in lps.items()}


def score2_slope(rep, d):
    """SCORE2 slope on its own cloglog scale (unstandardised), with log(follow-up)."""
    y = d["y"].to_numpy(float)
    X = np.column_stack([np.ones(len(d)), d["log_fu"] - d["log_fu"].mean(), d["score2_cll"]])
    w, cov = cloglog_fit(X, y)
    se = np.sqrt(cov[2, 2])
    rep("## 4. SCORE2 slope",
        "Slope of plaque cloglog on cloglog(SCORE2 risk). Both are log cumulative hazards, so slope 1 "
        "means SCORE2 ranks plaque hazard on the same scale as CVD hazard; below 1, SCORE2 spreads "
        "people more than their plaque risk differs.")
    rep.table([("SCORE2 slope", fmt(w[2]), f"{fmt(w[2] - 1.96 * se)} to {fmt(w[2] + 1.96 * se)}")],
              ["", "estimate", "95 % Wald interval"])

    Xr = design(d, FACTORS, d)
    wr, covr = cloglog_fit(Xr, y)
    rep("Refitted factors: hazard ratio per SD of each term (0/1 terms are standardised too, so the weights "
        "can be compared). Compare the age weight with SCORE2's, which is built for CVD.")
    rows = []
    for j, c in enumerate(("log_fu",) + FACTORS, start=1):
        se = np.sqrt(covr[j, j])
        rows.append((c, fmt(np.exp(wr[j]), 2), f"{fmt(np.exp(wr[j] - 1.96 * se), 2)} to {fmt(np.exp(wr[j] + 1.96 * se), 2)}"))
    rep.table(rows, ["term", "HR per SD", "95 % Wald interval"])


def bootstrap(rep, d, res, boot):
    pairs = [(REFIT_MODEL, SCORE2_MODEL), ("SCORE2 + age + sex", SCORE2_MODEL), (SCORE2_MODEL, "age + sex")]
    point = {p: np.mean(res[p[0]]["c"]) - np.mean(res[p[1]]["c"]) for p in pairs}
    draws = {p: [] for p in pairs}
    if boot:
        ids = d.index.to_numpy()
        y = d["y"].to_numpy(float)
        fmap = folds(ids, y, SEED)  # folds by original person: duplicates stay together
        rng = np.random.default_rng(SEED + 1)
        for _ in range(boot):
            idx = rng.integers(0, len(d), len(d))
            db = d.iloc[idx]
            fold = np.array([fmap[i] for i in db.index])
            yb = db["y"].to_numpy(float)
            cs = {m: c_stat(oof_lp(db, MODELS[m], fold), yb) for m in {x for p in pairs for x in p}}
            for p in pairs:
                if cs[p[0]] is not None and cs[p[1]] is not None:
                    draws[p].append(cs[p[0]] - cs[p[1]])

    rep("## 5. Delta C (estimated, not tested)",
        f"Point estimate: difference of the mean OOF C in section 3. Interval: 2.5th-97.5th percentile "
        f"over {boot} person-bootstrap replicates with the CV redone inside each (approximate).")
    rows = []
    for p in pairs:
        lo, hi = (np.percentile(draws[p], [2.5, 97.5]) if len(draws[p]) >= 20 else (None, None))
        rows.append((f"{p[0]} - {p[1]}", fmt(point[p]), "n/a" if lo is None else f"{fmt(lo)} to {fmt(hi)}"))
    rep.table(rows, ["comparison", "delta C", "95 % bootstrap interval"])

    dc = point[(REFIT_MODEL, SCORE2_MODEL)]
    base = REFIT_MODEL if dc >= DECISION_DC else SCORE2_MODEL
    rep(f"Prespecified rule: refit - SCORE2 delta C {fmt(dc)} {'>=' if dc >= DECISION_DC else '<'} "
        f"{DECISION_DC}, so the primary 'who' base is **{base}**. Either way, report the geometry "
        "increment over the other base as a sensitivity analysis.")


def calibration_table(rep, d, lps):
    rep("## 6. Observed vs predicted by fifth of OOF risk",
        "Predicted: mean OOF risk (averaged over the CV repeats) in each fifth; observed: events/people.")
    y = d["y"]
    for m in (SCORE2_MODEL, REFIT_MODEL):
        p = pd.Series(risk(lps[m]), index=d.index)
        q = pd.qcut(p.rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
        rows = [(int(k), fmt(p[q == k].mean()), cell(y[q == k])) for k in range(1, 6)]
        rep(f"**{m}**")
        rep.table(rows, ["fifth", "mean predicted", "observed"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bl", default=BL_PATH)
    ap.add_argument("--fu", default=FU_PATH)
    ap.add_argument("--out", default=OUT_FILE)
    ap.add_argument("--repeats", type=int, default=REPEATS)
    ap.add_argument("--boot", type=int, default=BOOT)
    args = ap.parse_args()

    bl, fu, bl_dec, fu_dec = build(args)
    rep = Report()
    rep("# Is unrefitted SCORE2 an honest 'who' base?",
        "Aggregates only; small counts suppressed as in cgps_stats.py. No geometry is used. Cohort: clean "
        "baseline (SIS = 0, new SSS = 0), read at BL, FU read.")
    ids = cohort(rep, bl, fu, bl_dec, fu_dec, None, False).intersection(fu.index)
    d = person_table(rep, bl, fu, fu_dec, ids)
    if min(int(d["y"].sum()), int((1 - d["y"]).sum())) < MIN_CELL:
        rep("Too few events or non-events to fit models.")
    else:
        res, lps = point_estimates(rep, d, args.repeats)
        score2_slope(rep, d)
        bootstrap(rep, d, res, args.boot)
        calibration_table(rep, d, lps)

    text = "\n".join(rep.lines)
    print(text)
    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
