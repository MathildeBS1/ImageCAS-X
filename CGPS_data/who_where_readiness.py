"""Can the HØ_10Y data answer the two thesis questions, and how much room is there?

    python CGPS_data/who_where_readiness.py              # tables only (spreadsheets + file lists)
    python CGPS_data/who_where_readiness.py --pilot      # + pilot geometry from the Medis trees

- Who:   does baseline geometry predict which people develop plaque, beyond SCORE2?
- Where: within a person, does a segment's geometry predict which segments develop plaque,
         beyond the segment's anatomical position?
Outcome: any plaque at FU (minimal or worse), per person and per segment, in the clean-baseline
cohort (BL ct_cag_sis == 0 and the new ct_cag_sss == 0, read at BL = ct_cag_visual_read).
Cross-validation folds are split by person. Geometry: curvature, taper, LM bifurcation angle,
LM->LAD and LM->LCx diameter ratios (GEOMETRY_PARAMS), later from the in-house pipeline.

Sections of who_where.md:
1. Cohort flow down to the analysable cohort (read at BL, FU read, BL volume available).
2. Who: events, outcome reliability (FU unevaluable segments, agreement with FU ct_cag_sis),
   follow-up time, event rates by sex/age/SCORE2/CAC, SCORE2 availability, the AUC that geometry
   has to improve on (SCORE2, age, CAC) with a rough smallest detectable AUC gain, the parameter
   budget (events per parameter), and events per artery for the per-artery models.
3. Where: events per segment, PDA/PLA by dominance (absent segments are filled in as "none"),
   clustering within persons (ICC, events per person), the cross-validated position-only baseline
   (pooled AUC, per-artery AUC and the within-person C statistic, which is the "where" question).
4. Reference: how many cohort patients have a Medis tree, which segments those trees label, and
   for how many the LM bifurcation can be measured. Medis contours exist only for diseased
   segments, so none are in the clean cohort (the diameter ratios cannot be checked there).
5. --pilot: curvature per segment and the LM bifurcation angle computed from the Medis trees of
   the cohort, and their cross-validated added value over the baselines. Exploratory only: Medis
   trees are not the thesis pipeline, and only part of the cohort has one.

Privacy: aggregates only, small counts suppressed with the cgps_stats.py rules, no study_id. The
file is written to OUT_FILE (copy it to CGPS_data/who_where.md like the other reports).
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

from cgps_stats import (BL_PATH, FU_PATH, MIN_CELL, OUT_DIR, SEGMENTS, auc, cell, count, count_of,
                        decode_segments, describe, icc, load, num, pct, suppress, yes)
from clean_baseline_count import read_at_bl

ROOT = "/data/kimbr/HØ_10Y"
OUT_FILE = str(Path(OUT_DIR) / "who_where.md")
FOLDS = 5
SEED = 0
GEOMETRY_PARAMS = 5    # curvature, taper, LM bifurcation angle, LM->LAD and LM->LCx diameter ratio
EPV = (10, 20)         # events per parameter rules of thumb
ARTERIES = {"LAD": ("plad", "mlad", "dlad", "d1", "d2"), "CX": ("pcx", "mcx", "dcx", "om1", "om2"),
            "RCA": ("prca", "mrca", "drca"), "LM": ("lm",), "IM": ("im",), "PDA/PLA": ("pda", "pla")}
TRUNKS = {"LAD": ("plad", "mlad", "dlad"), "CX": ("pcx", "mcx", "dcx"), "RCA": ("prca", "mrca", "drca")}
SCORE2_INPUTS = ("scan_age", "male", "hist_smoking_current", "clin_bp_sys_mean", "tot_cholesterol", "hdl")
DOMINANT_DEPENDENT = ("pda", "pla")


# ---------------------------------------------------------------- output helpers
class Report:
    def __init__(self):
        self.lines = []

    def __call__(self, *text):
        self.lines += list(text) + [""]

    def table(self, rows, header):
        self.lines += ["| " + " | ".join(map(str, header)) + " |", "|" + "---|" * len(header)]
        self.lines += ["| " + " | ".join("" if x is None else str(x) for x in r) + " |" for r in rows]
        self.lines.append("")


def fmt(v, nd=3):
    return "n/a (too few)" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.{nd}f}"


def desc_row(name, x):
    d = describe(x)
    return [name] + [d.get(k) if not isinstance(d.get(k), float) else round(d[k], 2)
                     for k in ("n", "mean", "p25", "median", "p75")]


def hanley_mcneil_se(a, n1, n0):
    q1, q2 = a / (2 - a), 2 * a * a / (1 + a)
    return np.sqrt((a * (1 - a) + (n1 - 1) * (q1 - a * a) + (n0 - 1) * (q2 - a * a)) / (n1 * n0))


# ---------------------------------------------------------------- models (no sklearn needed)
def logit_fit(X, y, l2=1e-2):
    w = np.zeros(X.shape[1])
    for _ in range(100):
        p = 1 / (1 + np.exp(-np.clip(X @ w, -30, 30)))
        H = X.T @ (X * (p * (1 - p))[:, None]) + l2 * np.eye(len(w))
        step = np.linalg.solve(H, X.T @ (y - p) - l2 * w)
        w += step
        if np.abs(step).max() < 1e-8:
            break
    return w


def design(df, cols, levels):
    """Intercept + one-hot of 'pos' (levels from training) + standardised numeric cols."""
    X = [np.ones(len(df))] + [(df["pos"] == l).to_numpy(float) for l in levels[1:]]
    X += [df[c].to_numpy(float) for c in cols]
    return np.column_stack(X)


def folds_by_person(ids, y_person, k=FOLDS, seed=SEED):
    """{id: fold}, stratified on the person outcome."""
    rng = np.random.default_rng(seed)
    out = {}
    for val in (0, 1):
        grp = np.array(sorted(i for i in ids if y_person.get(i) == val), dtype=object)
        rng.shuffle(grp)
        out.update({i: n % k for n, i in enumerate(grp)})
    return out


def cv_predict(df, extra=(), fold=None):
    """Out-of-fold predicted risk. Position-only (extra = ()) or position + numeric columns,
    each standardised within position on the training folds."""
    pred = pd.Series(np.nan, index=df.index)
    for f in sorted(set(fold.values())):
        test = df["id"].map(fold) == f
        tr, te = df[~test].copy(), df[test].copy()
        for c in extra:
            mu, sd = tr.groupby("pos")[c].mean(), tr.groupby("pos")[c].std().replace(0, np.nan)
            for d in (tr, te):
                d[c] = ((d[c] - d["pos"].map(mu)) / d["pos"].map(sd)).fillna(0.0)
        levels = sorted(tr["pos"].unique())
        w = logit_fit(design(tr, extra, levels), tr["y"].to_numpy(float))
        pred[te.index] = 1 / (1 + np.exp(-design(te, extra, levels) @ w))
    return pred


def within_person_c(df, pred):
    """Among persons with >= 1 event and >= 1 non-event segment: share of (event, non-event)
    segment pairs in the same person where the event segment has the higher prediction."""
    num_, den, persons = 0.0, 0, 0
    for _, g in df.assign(p=pred).groupby("id"):
        e, ne = g.p[g.y == 1].to_numpy(), g.p[g.y == 0].to_numpy()
        if len(e) and len(ne):
            d = e[:, None] - ne[None]
            num_ += (d > 0).sum() + 0.5 * (d == 0).sum()
            den += d.size
            persons += 1
    return (num_ / den if den else None), persons


# ---------------------------------------------------------------- data
def build(args):
    bl = load(args.bl).drop_duplicates("study_id").set_index("study_id")
    fu = load(args.fu).drop_duplicates("study_id").set_index("study_id")
    bl_dec, _ = decode_segments(bl)
    fu_dec, _ = decode_segments(fu)
    return bl, fu, bl_dec, fu_dec


def discover_files(root):
    from hoe10y_qc import discover, norm_id
    found = discover(root)
    bl_nifti = {x["id"] for x in found["niftis"] if x["visit"] == "BL" and x["id"]}
    trees = {}
    for t in found["trees"]:
        if t["id"]:
            trees.setdefault(t["id"], t["path"])
    contour_segs = Counter(seg for (v, _, seg) in found["contours"] if v == "BL")
    return {"bl_nifti": bl_nifti, "trees": trees, "contour_segs": contour_segs, "norm_id": norm_id}


# ---------------------------------------------------------------- sections
def cohort(rep, bl, fu, bl_dec, fu_dec, files, include_unread):
    sis, sss = num(bl["ct_cag_sis"]), num(bl["ct_cag_sss"])
    read = read_at_bl(bl.reset_index()).set_axis(bl.index)
    clean = (sis == 0) & (sss == 0)
    fu_segs = fu_dec[[f"ct_cag_{s}_stenosis" for s in SEGMENTS if f"ct_cag_{s}_stenosis" in fu_dec]]
    fu_read = fu_segs.notna().any(axis=1).reindex(bl.index, fill_value=False)
    steps = [("BL patients", pd.Series(True, index=bl.index)), ("clean baseline (SIS = SSS = 0)", clean)]
    if not include_unread:
        steps.append(("... read at BL (ct_cag_visual_read)", clean & read))
    steps.append(("... FU segments read", steps[-1][1] & fu_read))
    base = steps[-1][1]
    if files:
        has_vol = pd.Series([files["norm_id"](i) in files["bl_nifti"] for i in bl.index], index=bl.index)
        steps.append(("... BL CT volume available", base & has_vol))
    if "bad_quality" in bl:
        bad = yes(bl["bad_quality"]) == 1
        steps.append(("... not bad image quality (bad_quality)", steps[-1][1] & ~bad))
    rep("## 1. Cohort",
        "Each row keeps the patients of the row above that also meet its condition. The analyses below "
        f"use the cohort '{'clean + FU read (unread BL included)' if include_unread else 'clean, read at BL, FU read'}'"
        " (image volume and quality are not required, so the numbers show the ceiling).")
    rep.table([(name, count(m.sum())) for name, m in steps], ["step", "patients"])
    if include_unread:
        rep(f"Of the analysis cohort, {count((base & read).sum())} were read at BL; the rest have "
            "SIS = SSS = 0 only because their segments were filled in as 'none'.")
    return base[base].index


def who(rep, ids, bl, fu, fu_dec):
    segs = [s for s in SEGMENTS if f"ct_cag_{s}_stenosis" in fu_dec]
    g = fu_dec.loc[ids, [f"ct_cag_{s}_stenosis" for s in segs]]
    g.columns = segs
    y = (g >= 1).any(axis=1).astype(float).where(g.notna().any(axis=1))
    uncertain = (y == 0) & g.isna().any(axis=1)
    rep("## 2. Who - person level")
    n, k = int(y.notna().sum()), int((y == 1).sum())
    rows = [("patients with an outcome", count(n)), ("developed plaque (any segment >= minimal)", count_of(k, n)),
            ("% developed plaque", pct(k, n)),
            ("no plaque but >= 1 FU segment unevaluable (outcome uncertain)", count(uncertain.sum()))]
    if "ct_cag_sis" in fu:
        fsis = num(fu.loc[ids, "ct_cag_sis"])
        rows.append(("disagree with FU ct_cag_sis > 0", count(((fsis > 0).astype(float) != y)[y.notna() & fsis.notna()].sum())))
    rep.table(rows, ["", "n"])

    # follow-up time
    yrs = (pd.to_datetime(fu.loc[ids, "scandate"], errors="coerce") -
           pd.to_datetime(bl.loc[ids, "scandate"], errors="coerce")).dt.days / 365.25
    rep("Follow-up time (years) and event rate by follow-up tertile. Longer follow-up gives more time "
        "for plaque, so follow-up time belongs in every model (or as an offset/stratum).")
    rep.table([desc_row("BL -> FU years", yrs)], ["", "n", "mean", "p25", "median", "p75"])
    groups = {}
    if yrs.notna().sum() >= 3 * MIN_CELL:
        groups["follow-up tertile"] = pd.qcut(yrs, 3, labels=["short", "middle", "long"])
    groups["sex"] = num(bl.loc[ids, "male"]).map({0: "female", 1: "male"})
    age = num(bl.loc[ids, "scan_age"])
    groups["age at BL"] = pd.cut(age, [0, 50, 60, 70, 200], labels=["<50", "50-59", "60-69", ">=70"], right=False)
    s2 = num(bl.loc[ids, "score2"]).fillna(num(bl.loc[ids, "score2_op"])) if "score2" in bl else None
    if s2 is not None and s2.notna().sum() >= 3 * MIN_CELL:
        groups["SCORE2 tertile"] = pd.qcut(s2, 3, labels=["low", "middle", "high"], duplicates="drop")
    cac = num(bl.loc[ids, "ct_cacs_sum"]) if "ct_cacs_sum" in bl else None
    if cac is not None:
        groups["BL calcium score"] = pd.cut(cac, [-1, 0, 10, 100, np.inf], labels=["0", "1-10", "11-100", ">100"])
    rows = []
    for name, lab in groups.items():
        for lv in lab.cat.categories if hasattr(lab, "cat") else sorted(lab.dropna().unique()):
            rows.append((name, lv, cell(y[lab == lv])))
    rep("Event rate (events/patients) by group:")
    rep.table(rows, ["group", "level", "developed plaque"])
    if cac is not None:
        rep("Calcium > 0 without visible plaque at BL is a known early sign; if it predicts strongly, "
            "decide whether CAC is a covariate (it is not part of SCORE2).")

    # SCORE2
    rows = [(c, count(num(bl.loc[ids, c]).notna().sum()) if c in bl else "column missing")
            for c in ("score2", "score2_op") + SCORE2_INPUTS]
    rows.append(("score2 or score2_op", count(s2.notna().sum()) if s2 is not None else "n/a"))
    rep("SCORE2 availability in the cohort (score2_op is SCORE2-OP for age >= 70):")
    rep.table(rows, ["column", "patients with a value"])

    # baselines to beat
    rows = []
    for name, x in (("SCORE2 (score2, else score2_op)", s2), ("age", age),
                    ("BL calcium score", cac), ("BL calcium > 0", None if cac is None else (cac > 0).astype(float))):
        if x is None:
            continue
        a = auc(x, y)
        rows.append((name, count(pd.concat([x, y], axis=1).dropna().shape[0]), fmt(a)))
    rep("Discrimination of single baseline variables (AUC, no fitting). The 'who' model has to improve "
        "on SCORE2 (and is honest only if it also beats age, which drives SCORE2):")
    rep.table(rows, ["predictor", "patients", "AUC"])
    a = auc(s2, y) if s2 is not None else None
    n1, n0 = k, n - k
    if a is not None and min(n1, n0) >= MIN_CELL:
        se = hanley_mcneil_se(a, n1, n0)
        rep(f"Rough smallest detectable AUC gain over SCORE2 (80 % power, two-sided 5 %, correlation 0.5 "
            f"between the two models' AUCs; Hanley-McNeil SE {se:.3f}): about {2.8 * se:.3f}. Gains smaller "
            "than this cannot be told apart from noise in this cohort.")
    params = 1 + GEOMETRY_PARAMS + 1  # SCORE2 linear predictor + geometry + follow-up time
    rows = [(f"{e} events per parameter", int(k // e), "yes" if k // e >= params else "no") for e in EPV]
    rep(f"Parameter budget for the person model ({count(k)} events). Planned: SCORE2 as one linear "
        f"predictor + {GEOMETRY_PARAMS} geometry features + follow-up time = {params} parameters.")
    rep.table(rows, ["rule", "parameters allowed", f"{params} fit?"])

    # per artery (separate models per artery)
    rows = []
    for art, tsegs in TRUNKS.items():
        yy = (g[list(tsegs)] >= 1).any(axis=1).astype(float).where(g[list(tsegs)].notna().any(axis=1))
        ev = int((yy == 1).sum())
        rows.append((f"{art} trunk", cell(yy), int(ev // EPV[0])))
    rep("Per artery (new plaque anywhere in the trunk; for separate LAD/CX/RCA models):")
    rep.table(rows, ["artery", "events/patients", "parameters at 10 EPV"])
    return y, g


def where(rep, ids, bl, y_person, g):
    rep("## 3. Where - segment level")
    dom = bl.loc[ids, "ct_cag_dominance"].astype(str).str.strip().str.lower() if "ct_cag_dominance" in bl else None
    long = g.stack(future_stack=True).rename("y").reset_index()
    long.columns = ["id", "segment", "code"]
    long["y"] = (long["code"] >= 1).astype(float).where(long["code"].notna())
    long = long.dropna(subset=["y"])
    long["dominance"] = long["id"].map(dom) if dom is not None else "unknown"
    long["pos"] = np.where(long["segment"].isin(DOMINANT_DEPENDENT),
                           long["segment"] + "|" + long["dominance"].fillna("unknown"), long["segment"])
    rows = [(s, ART_OF.get(s, ""), cell(long.loc[long.segment == s, "y"])) for s in SEGMENTS if (long.segment == s).any()]
    rep("Units are person x segment with an FU read. Events per segment (the position baseline and how "
        "much signal each segment can carry):")
    rep.table(rows, ["segment", "artery", "events/units"])
    if dom is not None:
        rows = []
        for s in DOMINANT_DEPENDENT:
            for dv in sorted(long.loc[long.segment == s, "dominance"].dropna().unique()):
                rows.append((s, dv, cell(long.loc[(long.segment == s) & (long.dominance == dv), "y"])))
        rep("PDA/PLA by dominance. In a left-dominant system the RCA PDA/PLA may not exist but are "
            "filled in as 'none'; such units are not true negatives and should be dropped or modelled "
            "with dominance (the position baseline below uses segment x dominance for PDA/PLA):")
        rep.table(rows, ["segment", "dominance", "events/units"])

    per = long.groupby("id")["y"].sum()
    per = per[per > 0]
    vc = per.clip(upper=4).value_counts().sort_index()
    rep("New-plaque segments per person who developed plaque (4 = 4 or more). Many single-segment "
        "persons means 'where' has few within-person contrasts:")
    rep.table([(int(k_) if k_ < 4 else ">=4", v) for k_, v in zip(vc.index, suppress([vc.to_numpy()])[0])],
              ["segments with new plaque", "persons"])
    y_seg = long.set_index(["segment", "id"])["y"]
    i = icc(y_seg)
    rep(f"Within-person clustering (ICC of the segment outcome): {fmt(i)}. Segments of one person are "
        "not independent: keep folds by person and report person-clustered uncertainty.")

    fold = folds_by_person(set(long["id"]), y_person.to_dict())
    pred = cv_predict(long, (), fold)
    c, persons = within_person_c(long, pred)
    rows = [("all segments (pooled AUC)", count(len(long)), fmt(auc(pred, long["y"])))]
    for art, segs in ARTERIES.items():
        m = long["segment"].isin(segs)
        if long.loc[m, "pos"].nunique() > 1:  # position cannot rank within a single segment
            rows.append((f"{art} segments (AUC)", count(m.sum()), fmt(auc(pred[m], long.loc[m, "y"]))))
    rows.append((f"within person (C over {count(persons)} persons with events and non-events)", "", fmt(c)))
    rep(f"Position-only baseline, {FOLDS}-fold cross-validated by person (logistic on segment, PDA/PLA x "
        "dominance). This is what segment geometry has to beat. The within-person C is the 'where' "
        "question itself: how often the segment that developed plaque was ranked above one that did "
        "not, in the same person.")
    rep.table(rows, ["", "units", "value"])
    return long, fold


ART_OF = {s: a for a, segs in ARTERIES.items() for s in segs}


def reference(rep, ids, bl, files, all_bl_ids):
    rep("## 4. Reference data (Medis)")
    if not files:
        rep("_skipped (--no-files)_")
        return {}
    norm = files["norm_id"]
    tree_ids = {i for i in all_bl_ids if norm(i) in files["trees"]}
    in_cohort = [i for i in ids if i in tree_ids]
    sis = num(bl["ct_cag_sis"])
    rows = [("Medis trees (all)", count(len(files["trees"]))),
            ("trees of patients in the BL sheet", count(len(tree_ids))),
            ("... with plaque at BL (SIS > 0)", count(sum(sis.get(i, np.nan) > 0 for i in tree_ids))),
            ("... in the analysis cohort", count(len(in_cohort)))]
    rep("Kit exported only scans a reader analysed, so the trees may come mostly from patients with "
        "plaque at BL. Then they validate the pipeline on diseased anatomy, not on the clean cohort "
        "the models use.")
    rep.table(rows, ["", "patients"])
    cs = files["contour_segs"]
    rep("Medis contour segments (diseased segments only, so none in the clean cohort). The diameter "
        "ratios need LM, pLAD and pCX lumen; contours there exist for:")
    rep.table([(s, count(cs.get(s, 0))) for s in ("lm", "plad", "pcx")], ["segment", "contoured segments"])
    return {i: files["trees"][norm(i)] for i in tree_ids}


# ---------------------------------------------------------------- pilot geometry from Medis trees
def segment_runs(tree):
    """{segment: longest contiguous run of points with that label} from hoe10y_qc.tree_points."""
    from hoe10y_qc import arclen
    runs = defaultdict(list)
    for pts, labs in tree:
        start = 0
        for j in range(1, len(labs) + 1):
            if j == len(labs) or labs[j] != labs[start]:
                if labs[start] and j - start >= 3:
                    runs[labs[start]].append(pts[start:j])
                start = j
    return {k: max(v, key=lambda r: arclen(r)[-1]) for k, v in runs.items()}


def mean_curvature(pts, step=1.0, smooth=5):
    from hoe10y_qc import arclen
    s = arclen(pts)
    if s[-1] < 3 * smooth * step:
        return np.nan
    q = np.stack([np.interp(np.arange(0, s[-1], step), s, pts[:, k]) for k in range(3)], 1)
    kern = np.ones(smooth) / smooth
    q = np.stack([np.convolve(q[:, k], kern, mode="valid") for k in range(3)], 1)
    d1, d2 = np.gradient(q, axis=0), np.gradient(np.gradient(q, axis=0), axis=0)
    k = np.linalg.norm(np.cross(d1, d2), axis=1) / np.maximum(np.linalg.norm(d1, axis=1) ** 3, 1e-9)
    return float(np.mean(k[2:-2])) if len(k) > 4 else np.nan


def lm_bifurcation_angle(runs, lo=2.0, hi=8.0):
    """Angle (deg) between the first lo-hi mm of LAD and of CX, measured from the LM end."""
    from hoe10y_qc import arclen
    lm = runs.get("lm")
    lad = runs.get("plad", runs.get("lad"))
    cx = runs.get("pcx", runs.get("cx"))
    if lm is None or lad is None or cx is None:
        return np.nan
    dirs = []
    for br in (lad, cx):
        d0 = np.linalg.norm(lm[:, None] - br[[0, -1]][None], axis=2).min(0)
        br = br if d0[0] <= d0[1] else br[::-1]  # start at the end touching LM
        bif = lm[np.linalg.norm(lm - br[0], axis=1).argmin()]
        s = arclen(br)
        seg = br[(s >= lo) & (s <= hi)]
        if not len(seg):
            return np.nan
        v = seg.mean(0) - bif
        dirs.append(v / np.linalg.norm(v))
    return float(np.degrees(np.arccos(np.clip(np.dot(*dirs), -1, 1))))


def pilot(rep, ids, trees, long, y_person, fold):
    import centerline_qc as cq
    from hoe10y_qc import tree_points, tree_topology
    rep("## 5. Pilot: geometry from the Medis trees (exploratory)")
    in_cohort = [i for i in ids if i in trees]
    if len(in_cohort) < 3 * MIN_CELL:
        rep(f"Only {count(len(in_cohort))} cohort patients have a Medis tree: too few for a pilot.")
        return
    tree_topology([{"visit": "BL", "id": str(i), "path": trees[i]} for i in in_cohort])  # sets label coding
    feats, angles, failed = [], {}, 0
    for i in in_cohort:
        try:
            runs = segment_runs(tree_points(Path(trees[i])))
        except Exception:  # noqa: BLE001 - counted
            failed += 1
            continue
        angles[i] = lm_bifurcation_angle(runs)
        feats += [{"id": i, "segment": s, "curvature": mean_curvature(r)} for s, r in runs.items() if s in SEGMENTS]
    F = pd.DataFrame(feats)
    rep(f"{count(len(in_cohort))} cohort patients with a tree ({count(failed)} not readable). Label coding "
        f"as in centerline_qc.py ({cq._numbering}).")
    present = F.groupby("segment")["curvature"].apply(lambda x: x.notna().sum()) if len(F) else pd.Series(dtype=int)
    rep("Segments with a measurable curvature (labelled run >= 15 mm):")
    rep.table([(s, count(present.get(s, 0))) for s in SEGMENTS], ["segment", "patients"])

    ang = pd.Series(angles, dtype=float)
    y = y_person.reindex(ang.index)
    rep(f"LM bifurcation angle measurable in {count(ang.notna().sum())} patients; "
        f"median {fmt(ang.median(), 1)} deg; AUC for developing plaque {fmt(auc(ang, y))} "
        "(values below 0.5 mean wider angles go with less plaque).")

    d = long.merge(F, on=["id", "segment"], how="inner").dropna(subset=["curvature"])
    if d["y"].sum() < 2 * MIN_CELL or d["id"].nunique() < 3 * MIN_CELL:
        rep("Too few segment events with a curvature for the segment pilot.")
        return
    d = d.reset_index(drop=True)
    p0, p1 = cv_predict(d, (), fold), cv_predict(d, ("curvature",), fold)
    c0, n0 = within_person_c(d, p0)
    c1, _ = within_person_c(d, p1)
    rep("Segment pilot, same person folds, restricted to segments with a curvature:")
    rep.table([("pooled AUC", fmt(auc(p0, d["y"])), fmt(auc(p1, d["y"]))),
               (f"within-person C ({count(n0)} persons)", fmt(c0), fmt(c1))],
              ["", "position only", "position + curvature"])
    rows = []
    for s in SEGMENTS:
        m = d.segment == s
        if m.sum():
            ev, ne = d.loc[m & (d.y == 1), "curvature"], d.loc[m & (d.y == 0), "curvature"]
            show = len(ev) >= MIN_CELL and len(ne) >= MIN_CELL
            rows.append((s, cell(d.loc[m, "y"]), fmt(ev.median() * 100, 2) if show else "n/a",
                         fmt(ne.median() * 100, 2) if show else "n/a"))
    rep("Median curvature (1/100 mm) by FU outcome, per segment:")
    rep.table(rows, ["segment", "events/units", "new plaque", "no new plaque"])


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bl", default=BL_PATH)
    ap.add_argument("--fu", default=FU_PATH)
    ap.add_argument("--root", default=ROOT, help="HØ_10Y folder (for BL volumes and Medis trees)")
    ap.add_argument("--out", default=OUT_FILE)
    ap.add_argument("--no-files", action="store_true", help="spreadsheets only, no file discovery")
    ap.add_argument("--include-unread", action="store_true", help="keep clean patients not read at BL")
    ap.add_argument("--pilot", action="store_true", help="pilot geometry from the Medis trees")
    args = ap.parse_args()

    bl, fu, bl_dec, fu_dec = build(args)
    files = None if args.no_files else discover_files(args.root)
    rep = Report()
    rep("# Who and where: is the data ready?",
        "Aggregates only; small counts suppressed as in cgps_stats.py. Outcome: any plaque (>= minimal) "
        "at FU. Cohort: clean baseline (SIS = 0, new SSS = 0).")
    ids = cohort(rep, bl, fu, bl_dec, fu_dec, files, args.include_unread)
    ids = ids.intersection(fu.index)
    y_person, g = who(rep, ids, bl, fu, fu_dec)
    long, fold = where(rep, ids, bl, y_person, g)
    trees = reference(rep, ids, bl, files, bl.index)
    if args.pilot and files:
        pilot(rep, ids, trees, long, y_person, fold)

    text = "\n".join(rep.lines)
    print(text)
    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
