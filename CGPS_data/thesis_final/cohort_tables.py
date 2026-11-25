"""Every number of Results §Study Cohort (Thesis_coronary/content/results/01_cohort.tex, sec:results-cohort).

    python CGPS_data/thesis_final/cohort_tables.py [--limit N] [--workers 8] [--out MD] [--rows DIR] [--from-rows]
    python CGPS_data/thesis_final/cohort_tables.py --check   # synthetic numbers, needs no data

One report whose sections follow the section one to one: the flowchart (fig:results-flow), the missing values
(tab:results-missing), the participant characteristics (tab:results-characteristics), where plaque developed
(tab:results-location) and the geometric features (tab:results-features). Written 2026-11-25 to replace the \\mock{}
numbers of the section.

Rules (user, 2026-11-25, for this script):
  cohort        plaque-free baseline: BL ct_cag_sis == 0 and ct_cag_sss == 0 (CGPS_data/CLAUDE.md).
  image quality a participant is excluded when FU ct_cag_uneval or ct_cag_incomplete is set (the whole-scan flag),
                or has no FU row.
  tracer        excluded without both pruned BL tracer files (tracer_io.tracer_ids).
  outcome       a segment developed plaque when its FU grade is minimal or worse; unevaluable or missing = no
                outcome. A participant developed plaque when any of the 17 FU segments is minimal or worse. The
                bifurcation outcome is the proximal LAD or proximal LCx minimal or worse, and is missing when either
                of the two is not graded. Mild or worse (the sensitivity outcome) is any segment mild or worse.
  missing       complete cases in both models: a segment without curvature leaves the curvature model as a row; a
                participant without the angle or the asymmetry leaves the bifurcation model. Both models also need
                the six risk factors and the follow-up time.
  features      the cohort's own functions on the tracer tree, split once per participant (as
                medis_compare.tree_features): curvature_feature.artery_curvature per segment,
                bifurcation_angle.angle_with_reason and daughter_ratio.tree_asymmetry on the tree's own lumen surface.
Follow-up years are FU minus BL scandate (progression_who_pooled.build). The risk factors are the columns of
progression_who_pooled.SCORE2_COLS, copied here so the model script is not imported.

The feature run is slow (meshes), so the feature rows are saved in --rows (cohort_features.csv, individual data,
stays on the server) and --from-rows rebuilds the report from them and the sheets.

Writes cohort_tables.md next to this script: aggregates only, counts 1-4 shown as <5 with their percentage kept
(user), means and SDs only from MIN_CELL values, medians and IQRs only from QUARTILE_MIN (cgps_stats).
"""
import argparse
import os
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/
sys.path.insert(0, str(Path(__file__).resolve().parent))

ARTERIES = ("LAD", "CX", "RCA")
ARTERY_LABEL = {"LAD": "LAD", "CX": "LCx", "RCA": "RCA"}
NAMES = {"LAD": ("plad", "mlad", "dlad"), "CX": ("pcx", "mcx", "dcx"), "RCA": ("prca", "mrca", "drca")}  # split_trunks.NAMES
PARTS = ("Proximal", "Mid", "Distal")
SEGS = tuple(s for a in ARTERIES for s in NAMES[a])
SEG_LABEL = {s: f"{p} {ARTERY_LABEL[a]}" for a in ARTERIES for p, s in zip(PARTS, NAMES[a])}
BIF_SEGS = ("plad", "pcx")
RISK = {"age": "scan_age", "male": "male", "smoking": "hist_smoking_current", "sbp": "clin_bp_sys_mean",
        "tc": "tot_cholesterol", "hdl": "hdl"}  # progression_who_pooled.SCORE2_COLS
FU_QUALITY = ("ct_cag_uneval", "ct_cag_incomplete")
MINIMAL, MILD = 1, 2  # ranks in hoe10y_qc.GRADES


# ---------------------------------------------------------------- features (server)

def participant(pid):
    """Feature row of one participant: curvature T_<seg> (1/mm) and length L_<seg> (mm) of the nine segments, the
    angle, a, D_LAD and D_CX, and the reason behind every missing value. One task of the pool."""
    import tracer_io
    from bifurcation_angle import angle_with_reason
    from curvature_feature import artery_curvature
    from daughter_ratio import surface, tree_asymmetry
    from split_trunks import graph, split

    out = {"id": pid, **{f"{k}_{s}": np.nan for s in SEGS for k in ("T", "L")},
           "angle": np.nan, "asym": np.nan, "D_LAD": np.nan, "D_CX": np.nan}
    try:
        tree, roots = tracer_io.tracer_tree(pid), tracer_io.tracer_ostia(pid)
        arts = split(*graph(tree), roots=roots)
    except Exception as ex:  # noqa: BLE001 - counted
        err = f"error:{type(ex).__name__}"
        return out | {f"reason_{a}": err for a in ARTERIES} | {"reason_angle": err, "reason_asym": err}
    for a in ARTERIES:
        if a not in arts:
            out[f"reason_{a}"] = "artery missing"
            continue
        pm, md, end, _, Y, s = arts[a]
        bounds = (0.0, pm, md, end)
        try:
            T, out[f"reason_{a}"] = artery_curvature(Y, s, bounds), "ok"
        except Exception as ex:  # noqa: BLE001 - counted
            T, out[f"reason_{a}"] = [np.nan] * 3, f"error:{type(ex).__name__}"
        for seg, lo, hi, t in zip(NAMES[a], bounds[:-1], bounds[1:], T):
            out[f"T_{seg}"], out[f"L_{seg}"] = t, hi - lo
    try:
        out["angle"], out["reason_angle"] = angle_with_reason(tree, arts)
    except Exception as ex:  # noqa: BLE001 - counted
        out["reason_angle"] = f"error:{type(ex).__name__}"
    f = tracer_io.tracer_lumen(pid)
    if not f.exists():
        out["reason_asym"] = "no lumen surface"
    else:
        try:
            res = tree_asymmetry(tree, surface(f), roots, arts)
            out |= {k: res.get(k, np.nan) for k in ("asym", "D_LAD", "D_CX")}
            out["reason_asym"] = res.get("reason", "ok")
        except Exception as ex:  # noqa: BLE001 - counted
            out["reason_asym"] = f"error:{type(ex).__name__}"
    return out


def features(ids, workers=1):
    if workers > 1:
        from multiprocessing import Pool
        with Pool(workers) as pool:
            return pd.DataFrame(pool.map(participant, ids, chunksize=4))
    return pd.DataFrame([participant(pid) for pid in ids])


# ---------------------------------------------------------------- cohort (pure pandas, tested by --check)

def by_id(df):
    import hoe10y_qc as hq
    return df.assign(id=df["study_id"].map(hq.norm_id)).drop_duplicates("id").set_index("id")


def ranks(df, segs):
    """FU grade per segment as a rank 0 (none) .. 5 (occlusion); NaN when unevaluable, missing or unrecognised."""
    import hoe10y_qc as hq
    rank = {g: i for i, g in enumerate(hq.GRADES)}
    return pd.DataFrame({s: (df[f"ct_cag_{s}_stenosis"].map(hq.grade_of).map(rank) if f"ct_cag_{s}_stenosis" in df
                             else np.nan) for s in segs}, index=df.index).astype(float)


def cohort(bl, fu, have, F):
    """(flow, person table P of the plaque-free cohort, segment table S of the analysed cohort). bl and fu are
    indexed by id (by_id), have is the set of ids with tracer files, F the feature rows (participant)."""
    from cgps_stats import SEGMENTS, num, yes
    from dominance_check import dominance_group

    clean = (num(bl["ct_cag_sis"]) == 0) & (num(bl["ct_cag_sss"]) == 0)
    P = pd.DataFrame(index=bl.index[clean])
    fu_c = fu.reindex(P.index)
    bad = pd.Series(False, index=P.index)
    for c in FU_QUALITY:
        if c in fu_c:
            bad |= yes(fu_c[c]).fillna(0) > 0
    bad |= ~P.index.isin(fu.index)
    tracer = P.index.isin(list(have))
    P["status"] = np.where(bad, "fu_quality", np.where(~tracer, "no_tracer", "analysed"))

    for k, c in RISK.items():
        P[k] = (yes if k in ("male", "smoking") else num)(bl.loc[P.index, c]) if c in bl else np.nan
    P["years"] = ((pd.to_datetime(fu_c["scandate"], errors="coerce") if "scandate" in fu_c else pd.NaT)
                  - pd.to_datetime(bl.loc[P.index, "scandate"], errors="coerce")).dt.days / 365.25
    P["risk_ok"] = P[list(RISK) + ["years"]].notna().all(axis=1)
    P["dominance"] = dominance_group(bl.loc[P.index, "ct_cag_dominance"])[0] if "ct_cag_dominance" in bl else None

    R = ranks(fu_c, SEGMENTS)
    graded = R.notna().any(axis=1)
    P["developed"] = (R >= MINIMAL).any(axis=1).astype(float).where(graded & ~bad)
    P["mild"] = (R >= MILD).any(axis=1).astype(float).where(graded & ~bad)
    P["bif_y"] = (R[list(BIF_SEGS)] >= MINIMAL).any(axis=1).astype(float).where(R[list(BIF_SEGS)].notna().all(axis=1) & ~bad)
    P["bif_any"] = (R[list(BIF_SEGS)] >= MINIMAL).any(axis=1).astype(float).where(~bad)  # location table: plaque in either
    for s in SEGS:
        P[f"y_{s}"] = (R[s] >= MINIMAL).astype(float).where(R[s].notna() & ~bad)

    F = F.copy()
    F["id"] = F["id"].astype(str)
    P = P.join(F.set_index("id"), how="left")
    A = P[P["status"] == "analysed"]
    S = pd.DataFrame([{"id": i, "seg": s, "T": A.at[i, f"T_{s}"], "L": A.at[i, f"L_{s}"], "y": A.at[i, f"y_{s}"],
                       "risk_ok": A.at[i, "risk_ok"]} for i in A.index for s in SEGS],
                     columns=["id", "seg", "T", "L", "y", "risk_ok"])

    flow = Counter()
    flow["BL participants"] = len(bl)
    flow["plaque at baseline"] = int((~clean).sum())
    flow["plaque-free at baseline"] = len(P)
    flow["follow-up image quality too low (or no FU row)"] = int(bad.sum())
    flow["follow-up scan gradable"] = int((~bad).sum())
    flow["no tracer centerlines"] = int((P["status"] == "no_tracer").sum())
    flow["analysed cohort"] = len(A)
    return flow, P, S


def models(P, S):
    """(curvature model segment rows, bifurcation model person rows), complete cases."""
    A = P[P["status"] == "analysed"]
    curv = S[S["T"].notna() & S["y"].notna() & S["risk_ok"].astype(bool)]
    bif = A[A["angle"].notna() & A["asym"].notna() & A["bif_y"].notna() & A["risk_ok"]]
    return curv, bif


# ---------------------------------------------------------------- report

def n_pct(k, n):
    """'k (pct)' with k hidden as <5 or 'hidden' (cgps_stats.count_of) and the percentage kept (user)."""
    from cgps_stats import count_of
    k, n = int(k), int(n)
    return "-" if n == 0 else f"{count_of(k, n)} ({100 * k / n:.1f})"


def share(y):
    """'pct (k/n)' of a 0/1 series without NaN; empty below MIN_CELL values."""
    from cgps_stats import MIN_CELL, count, count_of
    y = pd.Series(y).dropna()
    n, k = len(y), int(y.sum())
    return "" if n < MIN_CELL else f"{100 * k / n:.1f} ({count_of(k, n)}/{count(n)})"


def mean_sd(x, nd=1):
    from cgps_stats import MIN_CELL
    x = pd.Series(x, dtype=float).dropna()
    return "" if len(x) < MIN_CELL else f"{x.mean():.{nd}f} ({x.std(ddof=1):.{nd}f})"


def med_iqr(x, nd=1):
    from cgps_stats import QUARTILE_MIN
    x = pd.Series(x, dtype=float).dropna()
    if len(x) < QUARTILE_MIN:
        return ""
    q1, m, q3 = np.percentile(x, [25, 50, 75])
    return f"{m:.{nd}f} ({q1:.{nd}f} to {q3:.{nd}f})"


def md_table(header, rows):
    return ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] + \
           ["| " + " | ".join(str(c) for c in r) + " |" for r in rows] + [""]


def report(flow, P, S):
    from cgps_stats import MIN_CELL, count

    A = P[P["status"] == "analysed"]
    curv, bif = models(P, S)
    dev = A[A["developed"] == 1]
    L = ["# Study cohort: every number of sec:results-cohort (cohort_tables.py)\n",
         ("Plaque-free baseline; FU whole-scan quality flag; pruned BL tracer files; complete cases in both models. "
          f"Counts 1-4 shown as <5 with their percentage kept; means from {MIN_CELL} values. Rules in the script header.\n")]

    # 1 flow
    L += ["## 1. Flow (fig:results-flow)\n"] + md_table(["step", "participants"], [(k, count(v)) for k, v in flow.items()])
    no_curv = A[A[[f"T_{s}" for s in SEGS]].isna().all(axis=1)]
    L += md_table(["analysed cohort", "value"], [
        ("developed plaque, n (%)", n_pct(A["developed"].sum(), A["developed"].notna().sum())),
        ("developed plaque: outcome missing (all segments ungraded)", count(A["developed"].isna().sum())),
        ("follow-up, years, median (IQR)", med_iqr(A["years"])),
        ("curvature model: participants", count(curv["id"].nunique())),
        ("curvature model: segments", count(len(curv))),
        ("curvature model: segments with plaque", count(int(curv["y"].sum()))),
        ("left out of the curvature model: no curvature in any segment", count(len(no_curv))),
        ("bifurcation model: participants", count(len(bif))),
        ("bifurcation model: plaque in the proximal LAD or LCx", count(int(bif["bif_y"].sum()))),
        ("left out of the bifurcation model: no asymmetry", count(A["asym"].isna().sum())),
        ("left out of the bifurcation model: no angle", count(A["angle"].isna().sum())),
    ])

    # 2 missing values
    rows = [("Follow-up image quality too low", "-", count((P["status"] == "fu_quality").sum()),
             share(A["developed"]), "not graded"),
            ("No tracer centerlines", "any segment", count((P["status"] == "no_tracer").sum()),
             share(A["developed"]), share(P.loc[P["status"] == "no_tracer", "developed"])),
            ("Missing risk factor or follow-up", "any segment", count((~A["risk_ok"]).sum()),
             share(A.loc[A["risk_ok"], "developed"]), share(A.loc[~A["risk_ok"], "developed"]))]
    B = A[A["risk_ok"] & A["bif_y"].notna()]
    for col, name in (("angle", "No bifurcation angle"), ("asym", "No LAD/LCx asymmetry")):
        rows.append((name, "proximal LAD or LCx", count(B[col].isna().sum()),
                     share(B.loc[B[col].notna(), "bif_y"]), share(B.loc[B[col].isna(), "bif_y"])))
    C = S[S["risk_ok"].astype(bool) & S["y"].notna()]
    for s in SEGS:
        c = C[C["seg"] == s]
        rows.append((f"No curvature: {SEG_LABEL[s]}", "same segment", count(c["T"].isna().sum()),
                     share(c.loc[c["T"].notna(), "y"]), share(c.loc[c["T"].isna(), "y"])))
    L += ["## 2. Missing values (tab:results-missing)\n",
          "Developed plaque, % (k/n), among those kept and those left out, on the outcome of the model.\n"]
    L += md_table(["left out", "outcome", "n left out", "kept", "left out"], rows)
    unevaluable = [(SEG_LABEL[s], count(A[f"y_{s}"].isna().sum())) for s in SEGS]
    L += ["Segments without an FU grade in the analysed cohort (no outcome, not in the curvature model):\n"]
    L += md_table(["segment", "n"], unevaluable)
    reasons = [("angle", r, count(n)) for r, n in A.loc[A["angle"].isna(), "reason_angle"].fillna("unknown").value_counts().items()]
    reasons += [("asymmetry", r, count(n)) for r, n in A.loc[A["asym"].isna(), "reason_asym"].fillna("unknown").value_counts().items()]
    for a in ARTERIES:
        miss = A[A[[f"T_{s}" for s in NAMES[a]]].isna().any(axis=1)]
        why = miss[f"reason_{a}"].fillna("unknown").replace("ok", "fewer than two profile points")
        reasons += [(f"curvature {ARTERY_LABEL[a]} (a segment missing)", r, count(n)) for r, n in why.value_counts().items()]
    L += ["Reasons for a missing feature (analysed cohort):\n"] + md_table(["feature", "reason", "participants"], reasons)

    # 3 characteristics
    groups = {"developed plaque": A[A["developed"] == 1], "did not develop plaque": A[A["developed"] == 0],
              "excluded, image quality": P[P["status"] == "fu_quality"]}
    rows = [("n", *(count(len(g)) for g in groups.values()))]
    for k, name, nd in (("age", "Age, years, mean (SD)", 1), ("male", "Men, n (%)", None),
                        ("smoking", "Current smoking, n (%)", None), ("sbp", "Systolic blood pressure, mmHg, mean (SD)", 0),
                        ("tc", "Total cholesterol, mmol/L, mean (SD)", 1), ("hdl", "HDL cholesterol, mmol/L, mean (SD)", 1)):
        rows.append((name, *(n_pct(g[k].sum(), g[k].notna().sum()) if nd is None else mean_sd(g[k], nd)
                             for g in groups.values())))
    rows.append(("Follow-up, years, median (IQR)", *(med_iqr(g["years"]) for g in groups.values())))
    for d in ("right", "co-dominant", "left"):
        rows.append((f"Dominance {d}, n (%)", *(n_pct((g["dominance"] == d).sum(), g["dominance"].notna().sum())
                                                 for g in groups.values())))
    rows.append(("missing values (any row)", *(count((~g[list(RISK) + ["years"]].notna().all(axis=1)).sum())
                                               for g in groups.values())))
    L += ["## 3. Participant characteristics (tab:results-characteristics)\n"] + md_table(["", *groups], rows)

    # 4 location
    n_dev = len(dev)
    grid = [(ARTERY_LABEL[a], *(n_pct((dev[f"y_{s}"] == 1).sum(), n_dev) for s in NAMES[a]),
             n_pct((dev[[f"y_{s}" for s in NAMES[a]]] == 1).any(axis=1).sum(), n_dev)) for a in ARTERIES]
    in_three = (dev[[f"y_{s}" for s in SEGS]] == 1).any(axis=1)
    L += ["## 4. Where plaque developed (tab:results-location)\n",
          f"n (% of the {count(n_dev)} in the analysed cohort who developed plaque).\n"]
    L += md_table(["artery", *PARTS, "any segment"], grid)
    L += md_table(["", "n (%)"], [
        ("LAD, LCx or RCA", n_pct(in_three.sum(), n_dev)),
        ("LM or side branch only", n_pct((~in_three).sum(), n_dev)),
        ("proximal LAD or proximal LCx (bifurcation outcome)", n_pct((dev["bif_any"] == 1).sum(), n_dev)),
        ("mild or worse (sensitivity outcome)", n_pct((dev["mild"] == 1).sum(), n_dev)),
    ])

    # 5 features
    rows = [("Bifurcation angle, degrees", count(A["angle"].notna().sum()), mean_sd(A["angle"]), med_iqr(A["angle"])),
            ("abs(a)", count(A["asym"].notna().sum()), mean_sd(A["asym"].abs(), 3), med_iqr(A["asym"].abs(), 3)),
            ("a = ln(D_LCx / D_LAD)", count(A["asym"].notna().sum()), mean_sd(A["asym"], 3), med_iqr(A["asym"], 3))]
    rows += [(f"Curvature {SEG_LABEL[s]}, 1e-3/mm", count(A[f"T_{s}"].notna().sum()),
              mean_sd(1e3 * A[f"T_{s}"]), med_iqr(1e3 * A[f"T_{s}"])) for s in SEGS]
    L += ["## 5. Geometric features (tab:results-features)\n", f"The {count(len(A))} participants of the analysed cohort.\n"]
    L += md_table(["feature", "available", "mean (SD)", "median (IQR)"], rows)
    return "\n".join(L)


# ---------------------------------------------------------------- run

def load_sheets():
    from cgps_stats import BL_PATH, FU_PATH, load
    return by_id(load(BL_PATH)), by_id(load(FU_PATH))


def run(limit=None, workers=1):
    """(bl, fu, have, F): the sheets, the tracer ids and the feature rows of the plaque-free participants with tracer
    files that pass the image-quality rule."""
    import tracer_io
    bl, fu = load_sheets()
    have = tracer_io.tracer_ids()
    _, P, _ = cohort(bl, fu, have, pd.DataFrame({"id": []}))
    ids = sorted(P.index[P["status"] == "analysed"], key=int)[:limit]
    return bl, fu, have, features(ids, workers)


def save_rows(have, F, folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    F.to_csv(folder / "cohort_features.csv", index=False)
    (folder / "cohort_tracer_ids.txt").write_text("\n".join(sorted(have)), encoding="utf-8")


def load_rows(folder):
    folder = Path(folder)
    F = pd.read_csv(folder / "cohort_features.csv", dtype={"id": str})
    have = set((folder / "cohort_tracer_ids.txt").read_text(encoding="utf-8").split())
    return have, F


# ---------------------------------------------------------------- checks

def synthetic(seed=0, n=120):
    """BL and FU sheets, tracer ids and feature rows with known answers."""
    rng = np.random.default_rng(seed)
    from cgps_stats import SEGMENTS
    ids = np.arange(1, n + 1)
    bl = pd.DataFrame({"study_id": ids, "ct_cag_sis": (ids > 100).astype(int), "ct_cag_sss": 0,
                       "scan_age": rng.normal(58, 9, n), "male": rng.integers(0, 2, n),
                       "hist_smoking_current": rng.integers(0, 2, n), "clin_bp_sys_mean": rng.normal(134, 18, n),
                       "tot_cholesterol": rng.normal(5.5, 1, n), "hdl": rng.normal(1.6, 0.5, n),
                       "ct_cag_dominance": np.where(ids % 10 == 0, "Left", "Right"),
                       "scandate": pd.Timestamp("2012-01-01")})
    bl.loc[bl["study_id"] == 7, "hdl"] = np.nan  # one missing risk factor
    fu = pd.DataFrame({"study_id": ids, "ct_cag_uneval": (ids <= 4).astype(int), "ct_cag_incomplete": 0,
                       "scandate": pd.Timestamp("2022-03-01")})
    for s in SEGMENTS:
        fu[f"ct_cag_{s}_stenosis"] = "none"
    fu.loc[fu["study_id"] % 2 == 0, "ct_cag_plad_stenosis"] = "minimal"  # even ids develop plaque in the pLAD
    fu.loc[fu["study_id"] % 5 == 0, "ct_cag_mlad_stenosis"] = "mild"
    fu.loc[fu["study_id"] == 9, "ct_cag_om1_stenosis"] = "minimal"  # side branch only
    fu.loc[fu["study_id"] == 11, "ct_cag_plad_stenosis"] = "uneval_motion"  # no bifurcation outcome
    have = {str(i) for i in ids if i not in (5, 6)}  # 5 and 6 without tracer files
    F = pd.DataFrame({"id": [str(i) for i in ids], "angle": rng.normal(75, 24, n), "asym": rng.normal(0, 0.2, n),
                      **{f"T_{s}": rng.normal(0.06, 0.02, n) for s in SEGS},
                      **{f"L_{s}": 20.0 for s in SEGS},
                      "reason_angle": "ok", "reason_asym": "ok", **{f"reason_{a}": "ok" for a in ARTERIES}})
    F.loc[F["id"].isin(["13", "15", "17"]), ["asym", "reason_asym"]] = [np.nan, "a cut without a cross-section"]
    F.loc[F["id"] == "19", ["angle", "reason_angle"]] = [np.nan, "no LM label"]
    F.loc[F["id"] == "21", "T_dcx"] = np.nan
    return by_id(bl), by_id(fu), have, F


def check():
    bl, fu, have, F = synthetic()
    flow, P, S = cohort(bl, fu, have, F)
    assert flow["BL participants"] == 120 and flow["plaque at baseline"] == 20 and flow["plaque-free at baseline"] == 100
    assert flow["follow-up image quality too low (or no FU row)"] == 4 and flow["no tracer centerlines"] == 2
    assert flow["analysed cohort"] == 94 == 100 - 4 - 2, flow
    assert P.loc["9", "developed"] == 1 and P.loc["9", "y_plad"] == 0, "side branch only develops plaque"
    assert np.isnan(P.loc["11", "bif_y"]) and np.isnan(P.loc["11", "y_plad"]), "unevaluable pLAD: no outcome"
    assert np.isnan(P.loc["2", "developed"]), "excluded for image quality: no outcome"
    assert P.loc["10", "mild"] == 1 and P.loc["10", "bif_y"] == 1
    assert not P.loc["7", "risk_ok"] and len(S) == 94 * 9
    curv, bif = models(P, S)
    assert "7" not in set(curv["id"]) and not ((curv["id"] == "21") & (curv["seg"] == "dcx")).any()
    assert len(curv) == 93 * 9 - 1 - 1, len(curv)  # 7 out (risk factor), 21 dcx (curvature), 11 plad (no grade)
    out = {"7", "11", "13", "15", "17", "19"}  # risk factor, no bif outcome, three without a, one without the angle
    assert set(bif.index) == set(P.index[P["status"] == "analysed"]) - out, sorted(set(P.index) - set(bif.index))
    assert n_pct(3, 40) == "<5 (7.5)" and n_pct(38, 40) == "hidden (95.0)" and n_pct(20, 40) == "20 (50.0)"
    assert share([1, 0, 1]) == "" and share([1, 0, 0, 0, 1, 0]) == "33.3 (<5/6)"
    text = report(flow, P, S)
    for sec in ("fig:results-flow", "tab:results-missing", "tab:results-characteristics", "tab:results-location",
                "tab:results-features"):
        assert sec in text, sec
    assert "| No LAD/LCx asymmetry | proximal LAD or LCx | <5 |" in text, text
    assert "| LM or side branch only | <5 (" in text
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        save_rows(have, F, tmp)
        have2, F2 = load_rows(tmp)
        assert have2 == have and report(*cohort(bl, fu, have2, F2)) == text, "rows round trip"
    print("cohort_tables: all checks passed")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="run the synthetic checks")
    ap.add_argument("--limit", type=int, default=None, help="only the first N participants")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "cohort_tables.md"))
    ap.add_argument("--rows", default=None, help="folder for the saved feature rows")
    ap.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 1), help="parallel participants (1: no pool)")
    ap.add_argument("--from-rows", action="store_true", help="report from the feature rows of an earlier run")
    args = ap.parse_args()
    if args.check:
        check()
        return
    from cgps_stats import OUT_DIR

    rows = Path(args.rows or Path(OUT_DIR) / "cohort_tables")
    if args.from_rows:
        bl, fu = load_sheets()
        have, F = load_rows(rows)
    else:
        bl, fu, have, F = run(args.limit, args.workers)
        save_rows(have, F, rows)
    text = report(*cohort(bl, fu, have, F))
    Path(args.out).write_text(text, encoding="utf-8")
    print(text)
    print(f"written to {args.out}; feature rows in {rows}")


if __name__ == "__main__":
    main()
