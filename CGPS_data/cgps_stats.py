"""Aggregate statistics on the CGPS baseline (BL) and follow-up (FU) tables, for choosing the
outcome(s) of the risk prediction model.

    python CGPS_data/cgps_stats.py

Set BL_PATH, FU_PATH and OUT_DIR below first (or override them with --bl, --fu, --out).

Inputs may be .csv/.tsv/.txt, .xlsx/.xls, .parquet, .dta or .sas7bdat, one row per patient, with
the column names of header_BL.xlsx / header_FU.xlsx. Patients are paired on ``study_id``.

Privacy: the script only reads the two input files and only writes aggregate statistics to
``--out``: report.md, stats.json, columns_bl.csv and columns_fu.csv. Nothing else is written (no
cache, pickle or temp file) and the inputs are never modified or copied. It never writes study_id,
any row-level value, any text value (free text, initials, labels; only numeric codes are listed)
or exact dates (dates are reduced to years and intervals). Disclosure control:
- counts from 1 to MIN_CELL-1 are written as "<MIN_CELL", and summaries need MIN_CELL values;
- "k of n" is also hidden when n - k is from 1 to MIN_CELL-1 (it could be worked out), or when
  k = n in a group smaller than GROUP_MIN ("all of them" says something about each one);
- in value counts and cross-tables no row or column keeps a single hidden cell, so it cannot be
  recovered from the total (secondary suppression, shown as "hidden");
- median/quartiles need QUARTILE_MIN values and 5th/95th percentiles TAIL_MIN; never min/max.
Counts may still be combined across different tables, so have the output checked against your
data agreement before taking it out of the secure environment.

Coding assumptions, to check against the value counts in the report: yes/no fields are 1/0 (or
yes/no, ja/nej) and any value > 0 counts as yes. Segment stenosis and plaque type are text labels
decoded with STENOSIS_CODES / PLAQUE_CODES (section 5 counts any label that was not recognised);
plaque is present when stenosis is minimal or worse.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

# ---- edit these three paths before running ----
BL_PATH = "/path/to/baseline.xlsx"    # baseline Excel file (data on the first sheet)
FU_PATH = "/path/to/followup.xlsx"    # follow-up Excel file (data on the first sheet)
OUT_DIR = "/path/to/cgps_results"     # folder for the aggregate results (created if missing)

MIN_CELL = 5
QUARTILE_MIN = 10  # values needed before median/quartiles are shown
TAIL_MIN = 20  # values needed before 5th/95th percentiles are shown
GROUP_MIN = 20  # in smaller groups "all of them" (k = n) is hidden, as it tells something about each one
MAX_LEVELS = 20  # value counts are reported for columns with at most this many distinct values
NO_PLAQUE = (0,)
# segment stenosis and plaque type are stored as text labels; "uneval_*" stenosis = not evaluable
STENOSIS_CODES = {"none": 0, "minimal": 1, "mild": 2, "moderate": 3, "severe": 4, "occlusion": 5}
PLAQUE_CODES = {"calcified": 1, "mostly_calcified": 2, "mostly_noncalcified": 3, "noncalcified": 4}
TYPE_NOT_RECORDED = 9  # plaque present (stenosis minimal or worse) but no plaque type given
SEGMENTS = ("lm", "plad", "mlad", "dlad", "d1", "d2", "im", "pcx", "om1", "mcx", "om2", "dcx",
            "prca", "mrca", "drca", "pda", "pla")
VESSELS = ("lad", "cx", "rca")
CACS_VESSELS = ("lm", "lad", "cx", "rca")
CATEGORIES = ("none", "minimal", "mild", "moderate", "severe", "occlusion")  # ascending severity
OBSTRUCTIVE = ("moderate", "severe", "occlusion")
DATE_COLS = ("scandate", "ae_date_discovered", "ae_date_onset", "recover_date")
FREE_TEXT = ("ae_description", "ae_outcome_description", "Image_Quality_reason_1", "Image_Quality_reason_2")
# history columns in both files: negative at BL and positive at FU = event between the scans
EVENT_COLS = ("demo_hist_myocardial_infarction", "demo_hist_coronary_revasc", "demo_hist_stroke_tia",
              "hist_angina", "hist_diabetes", "ct_cag_stent", "ct_cag_cabg")
HARD_EVENT_COLS = ("demo_hist_myocardial_infarction", "demo_hist_coronary_revasc", "ct_cag_stent", "ct_cag_cabg")
FU_ONLY_HISTORY = ("demo_hist_afib", "demo_hist_heart_failure", "demo_hist_icd_pm", "demo_hist_pad",
                   "demo_hist_dm", "demo_hist_cag", "demo_hist_rheumatoid_arthritis",
                   "demo_hist_systemic_lupus_erythematosus", "demo_hypertension_deriv",
                   "demo_hypercholesterolemia_deriv", "demo_smoker_status")
MEDS_BOTH = ("med_lipid_lowering_any", "med_antihypertensive_any", "med_diuretic", "med_asa",
             "med_insulin", "med_anticoagulant_any", "med_diabetes_other", "med_arthritis")
MEDS_FU_ONLY = ("med_statin", "med_statin_duration_above_2_years", "preparation_betablocker",
                "med_platelet_agg_inhibitors", "med_doac_noac", "med_warfarin", "med_metformin")
PREDICTORS = ("male", "scan_age", "clin_bmi", "clin_bp_sys_mean", "clin_bp_dia_mean", "hr_during_scan",
              "creatinine", "egfr", "hba1c", "tot_cholesterol", "hdl", "ldl", "triglyceride",
              "hist_smoking_current", "hist_smoking_former", "hist_smoking_years", "hist_diabetes",
              "demo_hist_family_cvd", "demo_hist_family_hypercholesterolemia", "med_lipid_lowering_any",
              "med_antihypertensive_any", "ct_cacs_sum", "ct_cag_sis", "ct_cag_sss", "ct_cag_plaque_type_score")
QUALITY_BL = ("bad_quality", "scan_qualitative_quality", "ct_cag_incomplete", "ct_cag_uneval",
              "PM", "Phd_Subjektiv_finished", "Readers_Plaque_analyses_finished")
QUALITY_FU = ("ct_cag_incomplete", "ct_cag_uneval", "ct_cag_uneval_motion", "ct_cag_uneval_noise",
              "ct_cag_uneval_scanfield", "ct_cag_uneval_contrastdefect", "ct_cag_uneval_pm",
              "ct_cag_uneval_other", "ct_cacs_eval_all", "ct_angio_heart_done", "ct_noncontrast_heart_done")
OBSTRUCTIVE_GRADE = 3  # moderate (STENOSIS_CODES) or worse counts as obstructive
LEVELS = {  # anatomical units, from single segments up to the whole tree. IM (ramus) is in no vessel.
    "segment": {s: (s,) for s in SEGMENTS},
    "position": {"proximal (LM, pLAD, pCX, pRCA)": ("lm", "plad", "pcx", "prca"), "mid": ("mlad", "mcx", "mrca"),
                 "distal": ("dlad", "dcx", "drca"), "side branches": ("d1", "d2", "om1", "om2", "im", "pda", "pla")},
    "vessel": {"LM": ("lm",), "LAD": ("plad", "mlad", "dlad", "d1", "d2"), "CX": ("pcx", "mcx", "dcx", "om1", "om2"),
               "RCA": ("prca", "mrca", "drca", "pda", "pla")},
    "tree": {"whole tree": SEGMENTS},
}
TRUNKS = {"LAD": ("plad", "mlad", "dlad"), "CX": ("pcx", "mcx", "dcx"), "RCA": ("prca", "mrca", "drca")}
DESIGN_PREDICTORS = ("scan_age", "male", "hist_smoking_current", "clin_bp_sys_mean", "tot_cholesterol", "hdl",
                     "hist_diabetes", "med_lipid_lowering_any", "med_antihypertensive_any", "demo_hist_family_cvd")
CAC_COLS = {"LM": "ct_cacs_lm", "LAD": "ct_cacs_lad", "CX": "ct_cacs_cx", "RCA": "ct_cacs_rca", "whole tree": "ct_cacs_sum"}
AUC_PREDICTORS = ("scan_age", "male", "ldl", "hdl", "clin_bp_sys_mean", "hist_smoking_current", "hist_diabetes",
                  "med_lipid_lowering_any", "ct_cacs_sum")
TRAJECTORIES = ("no plaque -> no plaque", "no plaque -> plaque", "plaque -> same", "plaque -> more",
                "plaque -> less")
KEY_CONTINUOUS = ("delta_sss", "delta_sis", "delta_sss_per_year", "delta_sqrt_cac", "delta_cac_per_year",
                  "n_segments_new_plaque")


# ---------------------------------------------------------------- disclosure-safe primitives

SMALL = f"<{MIN_CELL}"  # a count from 1 to MIN_CELL-1
HIDDEN = "hidden"      # a larger count hidden so that a small one cannot be worked out from a total


def small(k):
    return 0 < k < MIN_CELL


def count(n):
    n = int(n)
    return SMALL if small(n) else n


def disclosive(k, n):
    """k out of n reveals too much: the rest (n - k) is small, or all of a small group."""
    return small(n - k) or (k == n and 0 < n < GROUP_MIN)


def count_of(k, n):
    k, n = int(k), int(n)
    return SMALL if small(k) else HIDDEN if disclosive(k, n) else k


def pct(k, n):
    k, n = int(k), int(n)
    if n == 0:
        return None
    return SMALL if small(k) else HIDDEN if disclosive(k, n) else round(100 * k / n, 1)


def frac(flag):
    """Events among non-missing values of a 0/1 series."""
    valid = flag.dropna()
    k, n = int(valid.sum()), len(valid)
    return {"n": count(n), "events": count_of(k, n), "pct": pct(k, n)}


def suppress(t):
    """Counts table -> displayed values. Small cells become SMALL; then, while any row or column
    has exactly one hidden cell (recoverable from its total), its smallest other non-zero cell
    is hidden too."""
    t = np.asarray(t, dtype=int)
    primary = (t > 0) & (t < MIN_CELL)
    hide = primary.copy()
    lines = [np.s_[i, :] for i in range(t.shape[0])] + [np.s_[:, j] for j in range(t.shape[1])]
    changed = True
    while changed:
        changed = False
        for line in lines:
            h, v = hide[line], t[line]
            others = np.where(~h & (v > 0))[0]
            if h.sum() == 1 and len(others):
                h[others[np.argmin(v[others])]] = True  # h is a view into hide
                changed = True
    out = t.astype(object)
    out[primary] = SMALL
    out[hide & ~primary] = HIDDEN
    return out


def has_text(s):
    return bool((s.notna() & num(s).isna()).any())


def key(v):
    if pd.isna(v):
        return "missing"
    if isinstance(v, (float, np.floating)) and float(v).is_integer():
        return str(int(v))
    return str(v)


def order(k):
    """Sort labels numerically where possible, "missing" last."""
    m = re.match(r"[<>]?(-?\d+(?:\.\d+)?)", k)  # also orders ranges such as "11-100" and ">400"
    if m:
        return (0, float(m.group(1)), k)
    return (2 if k == "missing" else 1, 0.0, k)


def levels(s, allow_text=False):
    """Value counts. Not listed for text values (unless they are this script's own labels) or many
    distinct values, as the labels themselves could identify someone."""
    if not allow_text and has_text(s):
        return {"(text values, not listed)": count(s.notna().sum())}
    if s.nunique() > MAX_LEVELS:
        return {f"(more than {MAX_LEVELS} distinct values, not listed)": count(s.notna().sum())}
    vc = s.map(key).value_counts()
    labels = sorted(vc.index, key=order)
    return dict(zip(labels, suppress([[vc[k] for k in labels]])[0]))


def crosstab(a, b, allow_text=False):
    """BL value (rows) x FU value (columns)."""
    n = count((a.notna() & b.notna()).sum())
    if not allow_text and (has_text(a) or has_text(b)):
        return {"(text values, not tabulated)": {"n": n}}
    if a.nunique() > MAX_LEVELS or b.nunique() > MAX_LEVELS:
        return {f"(more than {MAX_LEVELS} distinct values, not tabulated)": {"n": n}}
    t = pd.crosstab(a.map(key), b.map(key))
    rows, cols = sorted(t.index, key=order), sorted(t.columns, key=order)
    shown = suppress(t.loc[rows, cols].to_numpy())
    return {r: dict(zip(cols, shown[i])) for i, r in enumerate(rows)}


def describe(x):
    """Mean/SD from MIN_CELL values, quartiles from QUARTILE_MIN, 5th/95th percentiles from TAIL_MIN
    (in small groups these lie close to single patients' values). Never min/max."""
    x = num(x).dropna()
    n = len(x)
    if n < MIN_CELL:
        return {"n": count(n)}
    q = x.quantile([0.05, 0.25, 0.5, 0.75, 0.95])
    quart, tail = n >= QUARTILE_MIN, n >= TAIL_MIN
    return {"n": n, "mean": x.mean(), "sd": x.std(), "p5": q[0.05] if tail else None,
            "p25": q[0.25] if quart else None, "median": q[0.5] if quart else None,
            "p75": q[0.75] if quart else None, "p95": q[0.95] if tail else None}


# ---------------------------------------------------------------- parsing

def num(s):
    if not pd.api.types.is_numeric_dtype(s):
        s = s.astype(str).str.strip().str.replace(",", ".", regex=False)
    return pd.to_numeric(s, errors="coerce")


def yes(s):
    if pd.api.types.is_numeric_dtype(s):
        return s.where(s.isna(), (s > 0).astype(float)).astype(float)
    words = {"1": 1.0, "yes": 1.0, "ja": 1.0, "true": 1.0, "y": 1.0,
             "0": 0.0, "no": 0.0, "nej": 0.0, "false": 0.0, "n": 0.0}
    t = s.astype(str).str.strip().str.lower()
    out = t.map(words)
    numeric = num(s)
    return out.fillna(numeric.where(numeric.isna(), (numeric > 0).astype(float)))


def dates(s, dayfirst):
    if pd.api.types.is_datetime64_any_dtype(s):
        return s
    if pd.api.types.is_numeric_dtype(s):
        if s.median() > 1e7:  # yyyymmdd
            return pd.to_datetime(s.astype("Int64").astype(str), format="%Y%m%d", errors="coerce")
        return pd.to_datetime(s, unit="D", origin="1899-12-30", errors="coerce")  # Excel serial
    return pd.to_datetime(s, errors="coerce", dayfirst=dayfirst)


def flag(cond, valid):
    return cond.astype(float).where(valid)


def load(path):
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in (".csv", ".tsv", ".txt"):
        df = pd.read_csv(path, sep=None, engine="python")
    elif suffix in (".xlsx", ".xls"):
        df = pd.read_excel(path)
    elif suffix == ".parquet":
        df = pd.read_parquet(path)
    elif suffix == ".dta":
        df = pd.read_stata(path)
    elif suffix == ".sas7bdat":
        df = pd.read_sas(path)
    else:
        raise SystemExit(f"unsupported file type: {path}")
    df.columns = [str(c).strip() for c in df.columns]
    return df.replace(r"^\s*$", np.nan, regex=True)


def label(s):
    return s.astype(str).str.strip().str.lower().str.replace(r"[\s-]+", "_", regex=True)


def decode_segments(df):
    """Segment stenosis/plaque-type text labels -> numeric codes (numbers already present are kept).
    Plaque type becomes 0 (no plaque) where stenosis is none, and TYPE_NOT_RECORDED where there is
    plaque without a type. Returns the decoded table and counts per column (no labels)."""
    df = df.copy()
    counts = {}
    for s in SEGMENTS:
        sc, pc = f"ct_cag_{s}_stenosis", f"ct_cag_{s}_plaque_type"
        if sc in df:
            raw, text = df[sc], label(df[sc])
            codes = text.map(STENOSIS_CODES).fillna(num(raw))
            uneval = raw.notna() & text.str.startswith("uneval")
            counts[sc] = {"recognised": count(codes.notna().sum()), "unevaluable (uneval_*)": count(uneval.sum()),
                          "unrecognised label": count((raw.notna() & codes.isna() & ~uneval).sum()),
                          "empty": count(raw.isna().sum())}
            df[sc] = codes
        if pc in df:
            raw = df[pc]
            codes = label(raw).map(PLAQUE_CODES).fillna(num(raw))
            unrecognised = raw.notna() & codes.isna()
            if sc in df:
                codes = codes.mask(df[sc] == 0, 0).mask(codes.isna() & ~unrecognised & (df[sc] >= 1), TYPE_NOT_RECORDED)
            counts[pc] = {"recognised": count((raw.notna() & ~unrecognised).sum()),
                          "unrecognised label": count(unrecognised.sum()),
                          "set to no plaque (stenosis none)": count((raw.isna() & (codes == 0)).sum()),
                          "plaque, type not recorded": count((codes == TYPE_NOT_RECORDED).sum()),
                          "empty": count(codes.isna().sum())}
            df[pc] = codes
    return df, counts


def col(df, name):
    return df[name] if name in df.columns else None


# ---------------------------------------------------------------- sections

def column_summary(df, dayfirst):
    rows, value_counts = [], {}
    for c in df.columns:
        s = df[c]
        n_missing = int(s.isna().sum())
        row = {"column": c, "n_nonmissing": count_of(len(s) - n_missing, len(s)), "n_missing": count_of(n_missing, len(s)),
               "pct_missing": pct(n_missing, len(s))}
        if c == "study_id":
            row["kind"] = "identifier"
            row["n_distinct"] = s.nunique()
        elif c in DATE_COLS or pd.api.types.is_datetime64_any_dtype(s):
            d = dates(s, dayfirst)
            row["kind"] = "date"
            row["n_unparsed"] = count((s.notna() & d.isna()).sum())
            value_counts[c] = levels(d.dt.year)
        else:
            x = num(s)
            non_numeric = int((s.notna() & x.isna()).sum())
            if c in FREE_TEXT or (non_numeric and s.nunique() > MAX_LEVELS):
                row["kind"] = "free text (values not reported)"
            else:
                row["kind"] = "categorical" if non_numeric else "numeric"
                row["n_distinct"] = s.nunique()
                if s.nunique() <= MAX_LEVELS:
                    value_counts[c] = levels(s)
                if not non_numeric and s.nunique() > 2:
                    row.update({k: v for k, v in describe(x).items() if k != "n"})
        rows.append(row)
    return rows, value_counts


def cohort(bl, fu, B, F, years, dup_bl, dup_fu):
    ids_bl, ids_fu = set(bl.index), set(fu.index)
    return {
        "patients": {"BL rows": count(len(bl) + dup_bl), "FU rows": count(len(fu) + dup_fu),
                     "duplicate study_id in BL (dropped, first kept)": count(dup_bl),
                     "duplicate study_id in FU (dropped, first kept)": count(dup_fu),
                     "in both BL and FU (paired)": count(len(B)), "BL only": count(len(ids_bl - ids_fu)),
                     "FU only": count(len(ids_fu - ids_bl)),
                     "BL columns": bl.shape[1], "FU columns": fu.shape[1]},
        "follow-up interval (years, paired)": describe(years),
        "follow-up interval checks": {"paired with interval": count(years.notna().sum()),
                                      "interval missing/unparsed": count(years.isna().sum()),
                                      "interval <= 0": count((years <= 0).sum()),
                                      "interval < 1 year": count((years < 1).sum()),
                                      "interval >= 5 years": count((years >= 5).sum())},
    }


def cac(B, F, years, cont, binary):
    out = {}
    cb, cf = col(B, "ct_cacs_sum"), col(F, "ct_cacs_sum")
    if cb is None or cf is None:
        return {"note": "ct_cacs_sum missing in BL or FU"}
    cb, cf = num(cb), num(cf)
    pos_years = years.where(years > 0)
    out["total CAC"] = {"BL": describe(cb), "FU": describe(cf)}
    out["CAC = 0"] = {"BL": frac(flag(cb == 0, cb.notna())), "FU": frac(flag(cf == 0, cf.notna()))}
    out["CAC BL category -> FU category"] = crosstab(
        pd.cut(cb, [-0.1, 0, 10, 100, 400, np.inf], labels=["0", "1-10", "11-100", "101-400", ">400"]).astype(object),
        pd.cut(cf, [-0.1, 0, 10, 100, 400, np.inf], labels=["0", "1-10", "11-100", "101-400", ">400"]).astype(object), allow_text=True)
    if "ct_cacs_groups" in B and "ct_cacs_groups" in F:
        out["ct_cacs_groups BL -> FU"] = crosstab(B["ct_cacs_groups"], F["ct_cacs_groups"])

    cont["delta_cac"] = cf - cb
    cont["delta_cac_per_year"] = (cf - cb) / pos_years
    cont["delta_sqrt_cac"] = np.sqrt(cf.clip(lower=0)) - np.sqrt(cb.clip(lower=0))
    cont["delta_log1p_cac"] = np.log1p(cf.clip(lower=0)) - np.log1p(cb.clip(lower=0))
    both = cb.notna() & cf.notna()
    binary["incident_cac (BL=0 -> FU>0)"] = flag(cf > 0, both & (cb == 0))
    binary["cac_any_increase"] = flag(cf > cb, both)
    binary["cac_progression_hokanson (dsqrt >= 2.5)"] = flag(cont["delta_sqrt_cac"] >= 2.5, both)
    annual = (cf / cb) ** (1 / pos_years) - 1
    binary["cac_annual_change_ge_15pct (BL>0)"] = flag(annual >= 0.15, both & (cb > 0) & pos_years.notna())
    binary["cac_decrease (data check)"] = flag(cf < cb, both)

    out["change"] = {k: describe(cont[k]) for k in ("delta_cac", "delta_cac_per_year", "delta_sqrt_cac", "delta_log1p_cac")}
    out["change among BL CAC > 0"] = {k: describe(cont[k][cb > 0]) for k in ("delta_cac_per_year", "delta_sqrt_cac")}
    out["per vessel"] = {}
    for v in CACS_VESSELS:
        vb, vf = col(B, f"ct_cacs_{v}"), col(F, f"ct_cacs_{v}")
        if vb is None or vf is None:
            continue
        vb, vf = num(vb), num(vf)
        ok = vb.notna() & vf.notna()
        out["per vessel"][v] = {"BL > 0": frac(flag(vb > 0, vb.notna())), "FU > 0": frac(flag(vf > 0, vf.notna())),
                                "increase": frac(flag(vf > vb, ok)), "new (0 -> >0)": frac(flag(vf > 0, ok & (vb == 0)))}
    return out


def scores(B, F, years, cont, binary):
    out = {}
    names = [("sis", "ct_cag_sis"), ("sss", "ct_cag_sss"), ("plaque_type_score", "ct_cag_plaque_type_score")]
    names += [(f"{v}_{s}", f"ct_cag_{v}_{s}") for v in VESSELS for s in ("sis", "sss", "plaque_type_score")]
    for name, c in names:
        b, f = col(B, c), col(F, c)
        if b is None or f is None:
            continue
        b, f = num(b), num(f)
        d = f - b
        ok = d.notna()
        cont[f"delta_{name}"] = d
        out[name] = {"BL": describe(b), "FU": describe(f), "delta": describe(d),
                     "delta value counts": levels(d.round().clip(-5, 10)),
                     "increase (delta > 0)": frac(flag(d > 0, ok)), "delta >= 2": frac(flag(d >= 2, ok)),
                     "decrease (delta < 0)": frac(flag(d < 0, ok)),
                     "BL = 0": frac(flag(b == 0, b.notna())), "FU = 0": frac(flag(f == 0, f.notna()))}
    if "delta_sss" in cont:
        cont["delta_sss_per_year"] = cont["delta_sss"] / years.where(years > 0)
        out["sss"]["delta per year"] = describe(cont["delta_sss_per_year"])
        binary["sss_increase"] = flag(cont["delta_sss"] > 0, cont["delta_sss"].notna())
        binary["sss_increase_ge2"] = flag(cont["delta_sss"] >= 2, cont["delta_sss"].notna())
    if "delta_sis" in cont:
        binary["sis_increase"] = flag(cont["delta_sis"] > 0, cont["delta_sis"].notna())
    if "delta_plaque_type_score" in cont:
        d = cont["delta_plaque_type_score"]
        binary["plaque_type_score_change"] = flag(d != 0, d.notna())
    return out


def segments(B, F, cont, binary):
    out, pooled = {}, {"stenosis progression": [], "new plaque": [], "new spotty calcification": [],
                       "new napkin-ring": []}
    progressed, new_plaque, new_hrp = {}, {}, {}
    for s in SEGMENTS:
        seg = {}
        if f"ct_cag_{s}_eval" in B:
            seg["evaluable at BL"] = levels(B[f"ct_cag_{s}_eval"])
        sb, sf = col(B, f"ct_cag_{s}_stenosis"), col(F, f"ct_cag_{s}_stenosis")
        if sb is not None and sf is not None:
            sb, sf = num(sb), num(sf)
            ok = sb.notna() & sf.notna()
            progressed[s] = flag(sf > sb, ok)
            pooled["stenosis progression"].append(progressed[s])
            seg["stenosis BL -> FU"] = crosstab(sb, sf)
            seg["stenosis progression (>= 1 grade)"] = frac(progressed[s])
            seg["stenosis regression (data check)"] = frac(flag(sf < sb, ok))
        pb, pf = col(B, f"ct_cag_{s}_plaque_type"), col(F, f"ct_cag_{s}_plaque_type")
        if pb is not None and pf is not None:
            pb, pf = num(pb), num(pf)
            free = pb.isin(NO_PLAQUE)
            new_plaque[s] = flag(~pf.isin(NO_PLAQUE), free & pf.notna())
            pooled["new plaque"].append(new_plaque[s])
            seg["plaque type BL -> FU"] = crosstab(pb, pf)
            seg["new plaque (among plaque-free at BL)"] = frac(new_plaque[s])
        hrp = []
        for feat, label in (("spotcalc", "new spotty calcification"), ("napring", "new napkin-ring")):
            fb, ff = col(B, f"ct_cag_{s}_feat_{feat}"), col(F, f"ct_cag_{s}_feat_{feat}")
            if fb is None or ff is None:
                continue
            fb, ff = yes(fb), yes(ff)
            new = flag(ff == 1, (fb == 0) & ff.notna())
            hrp.append(new)
            pooled[label].append(new)
            seg[f"{feat} BL -> FU"] = crosstab(fb, ff)
            seg[label] = frac(new)
        if hrp:
            new_hrp[s] = pd.concat(hrp, axis=1).max(axis=1)
        for feat in ("lap", "posrem"):
            if f"ct_cag_{s}_feat_{feat}" in F:
                seg[f"{feat} at FU (FU only)"] = levels(F[f"ct_cag_{s}_feat_{feat}"])
        if f"ct_cag_{s}_medis_finished" in B:
            seg["Medis plaque analysis finished (BL)"] = levels(B[f"ct_cag_{s}_medis_finished"])
        out[s] = seg

    pooled_out = {}
    for label, flags in pooled.items():
        if flags:
            stacked = pd.concat(flags, ignore_index=True)
            pooled_out[label] = frac(stacked)
    patient = {}
    for name, d in (("any segment stenosis progression", progressed), ("any new plaque", new_plaque),
                    ("any new high-risk feature", new_hrp)):
        if d:
            binary[name] = pd.concat(d.values(), axis=1).max(axis=1)
            patient[name] = frac(binary[name])
    if new_plaque:
        cont["n_segments_new_plaque"] = pd.concat(new_plaque.values(), axis=1).sum(axis=1, min_count=1)
        patient["segments with new plaque per patient"] = levels(cont["n_segments_new_plaque"])
    sten_b = [num(B[f"ct_cag_{s}_stenosis"]) for s in SEGMENTS if f"ct_cag_{s}_stenosis" in B]
    sten_f = [num(F[f"ct_cag_{s}_stenosis"]) for s in SEGMENTS if f"ct_cag_{s}_stenosis" in F]
    if sten_b and sten_f:
        patient["max segment stenosis BL -> FU"] = crosstab(pd.concat(sten_b, axis=1).max(axis=1),
                                                            pd.concat(sten_f, axis=1).max(axis=1))
    return {"pooled over segments (segment-level model)": pooled_out, "patient level": patient, "per segment": out}


def trajectory(b, f, has_b=None, has_f=None):
    """Plaque amount at BL and FU -> one of TRAJECTORIES, "missing" if either is. Plaque is present
    when the amount is > 0, or when has_b / has_f (e.g. the extent, for a stenosis-sum amount) is."""
    hb = (b > 0) if has_b is None else (has_b > 0)
    hf = (f > 0) if has_f is None else (has_f > 0)
    ok = b.notna() & f.notna()
    labels = np.select([ok & ~hb & ~hf, ok & ~hb & hf, ok & hb & (f == b), ok & hb & (f > b), ok & hb & (f < b)],
                       TRAJECTORIES, default="missing")
    return pd.Series(labels, index=b.index)


def group_sizes(t):
    n = int((t != "missing").sum())
    out = {g: {"n": count_of((t == g).sum(), n), "pct": pct((t == g).sum(), n)} for g in TRAJECTORIES}
    out["missing"] = {"n": count((t == "missing").sum()), "pct": None}
    return out


def plaque_trajectories(B, F, binary):
    """Patients (and segments) as no plaque -> no plaque / -> plaque, or plaque -> same / more / less."""
    patient = {}
    for name, c in [("extent: SIS (number of segments with plaque)", "ct_cag_sis"),
                    ("burden: SSS (summed stenosis grades)", "ct_cag_sss")] + \
                   [(f"{v.upper()} extent: {v} SIS", f"ct_cag_{v}_sis") for v in VESSELS]:
        if c in B and c in F:
            patient[name] = trajectory(num(B[c]), num(F[c]))
    plaque_b = [num(B[f"ct_cag_{s}_plaque_type"]) for s in SEGMENTS if f"ct_cag_{s}_plaque_type" in B and f"ct_cag_{s}_plaque_type" in F]
    plaque_f = [num(F[f"ct_cag_{s}_plaque_type"]) for s in SEGMENTS if f"ct_cag_{s}_plaque_type" in B and f"ct_cag_{s}_plaque_type" in F]
    if plaque_b:
        def n_with_plaque(cols):
            d = pd.concat(cols, axis=1)
            return (d.notna() & ~d.isin(NO_PLAQUE)).sum(axis=1).where(d.notna().any(axis=1))
        patient["extent: segments with plaque, counted from segment plaque types"] = \
            trajectory(n_with_plaque(plaque_b), n_with_plaque(plaque_f))
    out = {"patient level": {name: group_sizes(t) for name, t in patient.items()}}

    main = next(iter(patient.values()), None)  # SIS if present
    if main is not None:
        known = main != "missing"
        for g in TRAJECTORIES[1:2] + TRAJECTORIES[3:]:
            base = ("no plaque" if g.startswith("no plaque") else "plaque") + " ->"
            binary[f"{g} (SIS, among '{base}')"] = flag(main == g, known & main.str.startswith(base))
        preds = {p: num(B[p]) for p in PREDICTORS if p in B}
        out["BL predictor mean by SIS trajectory group"] = {
            p: {g: describe(x[main == g]).get("mean") for g in TRAJECTORIES} for p, x in preds.items()}

    # segment level: plaque presence from plaque type, more/less from the stenosis grade
    seg, pooled = {}, []
    for s in SEGMENTS:
        cols = [f"ct_cag_{s}_plaque_type", f"ct_cag_{s}_stenosis"]
        if not all(c in B and c in F for c in cols):
            continue
        amount = []
        for df in (B, F):
            p, st = num(df[cols[0]]), num(df[cols[1]])
            amount.append(pd.Series(np.where(p.isin(NO_PLAQUE), 0, st + 1), index=df.index).where(p.notna()))
        t = trajectory(*amount)
        pooled.append(t)
        seg[s] = {g: v["n"] for g, v in group_sizes(t).items()}
    if pooled:
        out["segment level (more/less = stenosis grade change)"] = {
            "pooled over segments": group_sizes(pd.concat(pooled, ignore_index=True)), "per segment (n)": seg}
    return out


# ---------------------------------------------------------------- outcome definitions per anatomical level

def segment_long(B, F):
    """One row per patient and segment assessed (plaque type and stenosis known) at both visits."""
    rows = []
    for s in SEGMENTS:
        need = (f"ct_cag_{s}_plaque_type", f"ct_cag_{s}_stenosis")
        if not all(c in B and c in F for c in need):
            continue
        d = pd.DataFrame({"pid": B.index, "seg": s})
        for tag, df in (("b", B), ("f", F)):
            p = num(df[need[0]]).to_numpy()
            d[f"p{tag}"] = np.where(np.isnan(p), np.nan, (~np.isin(p, NO_PLAQUE)).astype(float))
            d[f"s{tag}"] = num(df[need[1]]).to_numpy()
            h = [yes(df[c]).to_numpy() for c in (f"ct_cag_{s}_feat_spotcalc", f"ct_cag_{s}_feat_napring") if c in df]
            d[f"h{tag}"] = np.fmax.reduce(np.vstack(h)) if h else np.nan
        rows.append(d)
    if not rows:
        return None
    long = pd.concat(rows, ignore_index=True)
    return long[long[["pb", "pf", "sb", "sf"]].notna().all(axis=1)]


def unit_outcomes(d, unit, B, F):
    """Candidate outcomes for one anatomical unit (a group of segments), one value per patient.
    Returns progression outcomes, their regression counterparts, continuous changes, BL state and
    trajectory groups."""
    d = d.assign(newp=flag(d.pf == 1, d.pb == 0), lostp=flag(d.pf == 0, d.pb == 1),
                 newh=flag(d.hf == 1, (d.hb == 0) & d.hf.notna()), losth=flag(d.hf == 0, (d.hb == 1) & d.hf.notna()))
    a = d.groupby("pid").agg(eb=("pb", "sum"), ef=("pf", "sum"), bb=("sb", "sum"), bf=("sf", "sum"),
                             mb=("sb", "max"), mf=("sf", "max"), newp=("newp", "max"), lostp=("lostp", "max"),
                             newh=("newh", "max"), losth=("losth", "max"))
    every = pd.Series(True, index=a.index)
    prog = {
        "new plaque in a plaque-free segment": a.newp,
        "plaque-free -> plaque": flag(a.ef > 0, a.eb == 0),
        "extent increase (+1 segment with plaque)": flag(a.ef > a.eb, every),
        "burden increase (sum of stenosis grades)": flag(a.bf > a.bb, every),
        "burden increase >= 2": flag(a.bf - a.bb >= 2, every),
        "max stenosis +1 grade": flag(a.mf > a.mb, every),
        "incident obstructive": flag(a.mf >= OBSTRUCTIVE_GRADE, a.mb < OBSTRUCTIVE_GRADE),
        "new high-risk feature": a.newh,
    }
    reg = {
        "new plaque in a plaque-free segment": a.lostp,
        "plaque-free -> plaque": flag(a.ef == 0, a.eb > 0),
        "extent increase (+1 segment with plaque)": flag(a.ef < a.eb, every),
        "burden increase (sum of stenosis grades)": flag(a.bf < a.bb, every),
        "burden increase >= 2": flag(a.bb - a.bf >= 2, every),
        "max stenosis +1 grade": flag(a.mf < a.mb, every),
        "incident obstructive": flag(a.mf < OBSTRUCTIVE_GRADE, a.mb >= OBSTRUCTIVE_GRADE),
        "new high-risk feature": a.losth,
    }
    plaque_keys = list(prog)[:6]
    prog["any plaque progression"] = pd.concat([prog[k].fillna(0) for k in plaque_keys], axis=1).max(axis=1)
    reg["any plaque progression"] = pd.concat([reg[k].fillna(0) for k in plaque_keys], axis=1).max(axis=1)
    cont = {"change in extent": a.ef - a.eb, "change in burden": a.bf - a.bb, "change in max stenosis": a.mf - a.mb}
    base = {"BL extent": a.eb, "BL burden": a.bb, "BL max stenosis": a.mb}
    traj = {"extent": trajectory(a.eb, a.ef), "burden (presence from extent)": trajectory(a.bb, a.bf, a.eb, a.ef)}
    c = CAC_COLS.get(unit)
    if c and c in B and c in F:
        cb, cf = num(B[c]).clip(lower=0), num(F[c]).clip(lower=0)
        ok = cb.notna() & cf.notna()
        dsqrt = np.sqrt(cf) - np.sqrt(cb)
        prog["CAC increase"], reg["CAC increase"] = flag(cf > cb, ok), flag(cf < cb, ok)
        prog["CAC progression (Hokanson)"], reg["CAC progression (Hokanson)"] = flag(dsqrt >= 2.5, ok), flag(dsqrt <= -2.5, ok)
        prog["incident CAC"], reg["incident CAC"] = flag(cf > 0, ok & (cb == 0)), flag(cf == 0, ok & (cb > 0))
        cont["change in sqrt CAC"] = dsqrt
    return prog, reg, cont, base, traj


def icc(y):
    """One-way ANOVA intra-class correlation of a 0/1 outcome within patients."""
    y = y.dropna()
    g = y.groupby(level=-1)
    n_i, p_i = g.size(), g.mean()
    k, n = len(n_i), len(y)
    if k < 2 or n - k < 1:
        return None
    p = y.mean()
    n0 = (n - (n_i ** 2).sum() / n) / (k - 1)
    msb = (n_i * (p_i - p) ** 2).sum() / (k - 1)
    msw = (n_i * p_i * (1 - p_i)).sum() / (n - k)
    den = msb + (n0 - 1) * msw
    return (msb - msw) / den if den > 0 else None


def auc(x, y):
    d = pd.concat([x, y], axis=1, keys=["x", "y"]).dropna()
    n1 = int((d.y == 1).sum())
    n0 = len(d) - n1
    if min(n1, n0) < MIN_CELL:
        return None
    r = d.x.rank()
    return (r[d.y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


def kappa(a, b):
    d = pd.concat([a, b], axis=1, keys=["a", "b"]).dropna()
    if len(d) < MIN_CELL:
        return None
    po = (d.a == d.b).mean()
    pe = d.a.mean() * d.b.mean() + (1 - d.a.mean()) * (1 - d.b.mean())
    return (po - pe) / (1 - pe) if pe < 1 else None


def cell(y):
    v = y.dropna()
    k, n = int(v.sum()), len(v)
    p = pct(k, n)
    return f"{count_of(k, n)}/{count(n)}" + (f" ({p}%)" if isinstance(p, float) else "")


def by_patient(x, index):
    """A per-patient series spread onto a (unit, patient) index."""
    return pd.Series(x.reindex(index.get_level_values(-1)).to_numpy(), index=index)


def rate_by(outcomes, labels):
    """Event % of each outcome per label group (labels on the same index as the outcomes)."""
    groups = sorted(labels.dropna().unique(), key=lambda g: order(str(g)))
    out = {}
    for o, y in outcomes.items():
        d = pd.concat([y, labels.reindex(y.index)], axis=1, keys=["y", "g"]).dropna()
        out[o] = {str(g): cell(d.y[d.g == g]) for g in groups}
    return out


def level_stats(units, long, B, F, years, tree):
    res = {u: unit_outcomes(long[long.seg.isin(segs)], u, B, F) for u, segs in units.items()}
    outcomes = list(dict.fromkeys(k for r in res.values() for k in r[0]))

    def pool(part, k):
        parts = {u: r[part][k] for u, r in res.items() if k in r[part]}
        return pd.concat(parts, names=["unit", "pid"]) if parts else None

    P, R = {o: pool(0, o) for o in outcomes}, {o: pool(1, o) for o in outcomes}
    multi = len(units) > 1
    summary = {}
    for o in outcomes:
        v, r = P[o].dropna(), R[o].dropna()
        k, n, rk = int(v.sum()), len(v), int(r.sum())
        ic = icc(P[o]) if multi else None
        n_pat = v.index.get_level_values(-1).nunique()
        summary[o] = {"n units": count(n), "events": count_of(k, n), "pct": pct(k, n),
                      "regression events": count_of(rk, len(r)), "regression pct": pct(rk, len(r)),
                      "progression : regression": round(k / rk, 2) if min(k, rk) >= MIN_CELL else None,
                      "patients with event": count_of(v[v == 1].index.get_level_values(-1).nunique(), n_pat),
                      "ICC within patient": ic,
                      "design effect": 1 + (n / max(v.index.get_level_values(-1).nunique(), 1) - 1) * ic if ic is not None else None,
                      "max predictors at 10 EPV": min(k, n - k) // 10 if min(k, n - k) >= MIN_CELL else 0}
    out = {"units (segments in each)": {u: ", ".join(s) for u, s in units.items()},
           "outcome summary (all units pooled)": summary}
    if multi:
        out["events / n (%) per unit"] = {u: {o: cell(r[0][o]) if o in r[0] else "" for o in outcomes}
                                          for u, r in res.items()}
    out["agreement between outcomes (Cohen's kappa)"] = {o1: {o2: kappa(P[o1], P[o2]) for o2 in outcomes} for o1 in outcomes}
    max_b, ext_b = pool(3, "BL max stenosis"), pool(3, "BL extent")
    out["event % by BL max stenosis grade (ceiling/floor)"] = rate_by(P, max_b.map(key))
    out["event % by BL plaque"] = rate_by(P, pd.Series(np.where(ext_b > 0, "plaque at BL", "no plaque at BL"), index=ext_b.index))
    if years.notna().sum() >= 3 * MIN_CELL:
        tert = pd.qcut(years, 3, labels=["1 short", "2 middle", "3 long"]).astype(object)
        out["event % by follow-up interval tertile (should rise with time)"] = {
            o: rate_by({o: y}, by_patient(tert, y.index))[o] for o, y in P.items()}
    preds = {p: num(B[p]) for p in AUC_PREDICTORS if p in B}
    preds["follow-up years"] = years
    out["AUC of single BL predictors (0.5 = no signal)"] = {
        o: {**{b: auc(pool(3, b), y) for b in ("BL extent", "BL burden", "BL max stenosis")},
            **{p: auc(by_patient(x, y.index), y) for p, x in preds.items()}} for o, y in P.items()}
    changes = {}
    for c in dict.fromkeys(k for r in res.values() for k in r[2]):
        x = pool(2, c).dropna()
        changes[c] = {**describe(x), "pct zero": pct((x == 0).sum(), len(x)), "pct negative": pct((x < 0).sum(), len(x))}
    out["continuous change (zero-inflation, skew)"] = changes
    out["trajectory groups (pooled)"] = {t: group_sizes(pool(4, t)) for t in res[next(iter(res))][4]}
    if tree is not None:
        cond = {}
        for u, r in res.items():
            cond[u] = {}
            for o in outcomes:
                if o not in r[0] or o not in tree:
                    cond[u][o] = None
                    continue
                d = pd.concat([tree[o], r[0][o]], axis=1, keys=["t", "y"]).dropna()
                d = d[d.t == 1]
                cond[u][o] = pct(d.y.sum(), len(d))
        out["% of whole-tree events that occur in this unit"] = cond
    return out


def score_consistency(long, B, F):
    """Do extent/burden summed from the segments reproduce the recorded SIS/SSS? (checks the coding)"""
    out = {}
    pairs = [("tree", SEGMENTS, "")] + [(v, LEVELS["vessel"][v.upper()], f"{v}_") for v in VESSELS]
    lad = LEVELS["vessel"]["LAD"]  # which segments do the recorded LAD/CX scores include?
    pairs += [("lad+lm", ("lm",) + lad, "lad_"), ("lad+im", lad + ("im",), "lad_"), ("lad+lm+im", ("lm",) + lad + ("im",), "lad_"),
              ("cx+im", LEVELS["vessel"]["CX"] + ("im",), "cx_")]
    for label, segs, prefix in pairs:
        d = long[long.seg.isin(segs)].groupby("pid")
        for measure, col_b, col_f, rec in (("extent", "pb", "pf", "sis"), ("burden", "sb", "sf", "sss")):
            c = f"ct_cag_{prefix}{rec}"
            for tag, df, src in (("BL", B, col_b), ("FU", F, col_f)):
                if c not in df:
                    continue
                derived = d[src].sum()
                both = pd.concat([derived, num(df[c]).reindex(derived.index)], axis=1, keys=["d", "r"]).dropna()
                if len(both) < MIN_CELL:
                    continue
                out[f"{label} {measure} vs {c} ({tag})"] = {
                    "n": len(both), "Spearman rho": both.rank().corr().iloc[0, 1],
                    "pct exactly equal": pct((both.d == both.r).sum(), len(both))}
    return out


def outcome_levels(B, F, years):
    long = segment_long(B, F)
    if long is None or long.empty:
        return {"note": "segment plaque type / stenosis columns missing"}
    out = {"how to read": {
        "levels": "segment -> position (proximal/mid/distal/side branch) -> vessel -> whole tree; "
                  "each unit counts only segments assessed at both visits",
        "regression": "the opposite change (plaque or stenosis decreasing); mostly reader variability, "
                      "so a high progression:regression ratio means more signal than noise",
        "ICC / design effect": "how much events cluster within patients at sub-patient levels; "
                               "inflates the variance, so the effective sample is n units / design effect",
        "EPV": "max predictors at 10 events per variable, ignoring clustering",
        "OBSTRUCTIVE_GRADE": OBSTRUCTIVE_GRADE}}
    tree = level_stats(LEVELS["tree"], long, B, F, years, None)
    tree_prog = unit_outcomes(long, "whole tree", B, F)[0]
    for name in ("segment", "position", "vessel"):
        out[f"level: {name}"] = level_stats(LEVELS[name], long, B, F, years, tree_prog)
    out["level: whole tree"] = tree
    out["derived vs recorded scores (coding check)"] = score_consistency(long, B, F)
    return out


# ---------------------------------------------------------------- chosen design: plaque-free artery trunks

def artery_design(B, F, years):
    """The thesis design: LAD / CX / RCA trunks (no side branches) that are plaque-free at baseline,
    with the LM also plaque-free upstream of the LAD and CX; outcome = new plaque anywhere in the trunk."""
    if not all(f"ct_cag_{s}_stenosis" in B and f"ct_cag_{s}_stenosis" in F for t in TRUNKS.values() for s in t):
        return {"note": "trunk stenosis columns missing"}
    lm_free = num(B["ct_cag_lm_stenosis"]) == 0 if "ct_cag_lm_stenosis" in B else pd.Series(False, index=B.index)
    plaque_bl = pd.concat([num(B[c]) >= 1 for c in (f"ct_cag_{s}_stenosis" for s in SEGMENTS) if c in B], axis=1)
    preds = {p: num(B[p]) for p in DESIGN_PREDICTORS if p in B}
    if "tot_cholesterol" in B and "hdl" in B:
        preds["non-HDL cholesterol"] = num(B["tot_cholesterol"]) - num(B["hdl"])
    if "ct_cacs_sum" in B:
        preds["log(1 + total calcium)"] = np.log1p(num(B["ct_cacs_sum"]).clip(lower=0))
    preds["segments with plaque elsewhere"] = plaque_bl.sum(axis=1).where(plaque_bl.notna().any(axis=1))
    preds["follow-up years"] = years

    out = {"definition": {
        "units": "; ".join(f"{a}: {', '.join(s)}" for a, s in TRUNKS.items()),
        "eligible": "all trunk segments evaluable and 'none' at baseline; for LAD and CX also LM 'none'",
        "outcome": "any trunk segment minimal or worse at follow-up (unknown if no plaque seen and a segment is unevaluable)"}}
    flow, outcomes, where, calcium, auc_tab, tert_tab = {}, {}, {}, {}, {}, {}
    events = {}
    variants = list(TRUNKS) + ["RCA (also LM plaque-free)"]
    for name in variants:
        art = name.split(" ")[0]
        segs = TRUNKS[art]
        sb = pd.concat([num(B[f"ct_cag_{s}_stenosis"]) for s in segs], axis=1, keys=segs)
        sf = pd.concat([num(F[f"ct_cag_{s}_stenosis"]) for s in segs], axis=1, keys=segs)
        evaluable = sb.notna().all(axis=1)
        free = evaluable & (sb == 0).all(axis=1)
        needs_lm = art != "RCA" or "LM" in name
        eligible = free & lm_free if needs_lm else free
        complete_fu = sf.notna().all(axis=1)

        def outcome(threshold):
            hit = (sf >= threshold).any(axis=1)
            return flag(hit, eligible & (hit | complete_fu))

        ev = outcome(1)
        flow[name] = {"patients": count(len(B)), "trunk read at BL": count(sb.notna().any(axis=1).sum()),
                      "all trunk segments evaluable at BL": count(evaluable.sum()),
                      "trunk plaque-free at BL": count(free.sum()),
                      "and LM plaque-free": count(eligible.sum()) if needs_lm else "not required",
                      "eligible": count(eligible.sum()), "outcome known at FU": count(ev.notna().sum())}
        outcomes[name] = {"new plaque (>= minimal)": cell(ev), "new plaque >= mild": cell(outcome(2)),
                          "new obstructive (>= moderate)": cell(outcome(OBSTRUCTIVE_GRADE))}
        lost = flag((sf == 0).all(axis=1), evaluable & (sb >= 1).any(axis=1) & complete_fu & (lm_free if needs_lm else True))
        outcomes[name]["opposite: trunk plaque at BL -> none at FU (noise check)"] = cell(lost)
        hit_any = ev == 1
        where[name] = {s: cell(flag(sf[s] >= 1, hit_any & sf[s].notna())) for s in segs}
        where[name]["plaque in more than one trunk segment"] = cell(flag((sf >= 1).sum(axis=1) > 1, hit_any))
        c = CAC_COLS[art]
        if c in B and c in F:
            cb, cf = num(B[c]), num(F[c])
            calcium[name] = {"eligible with vessel calcium 0 at BL": count((eligible & (cb == 0)).sum()),
                             "eligible but vessel calcium > 0 at BL (plaque missed?)": count((eligible & (cb > 0)).sum()),
                             "new calcium (0 -> > 0) among eligible": cell(flag(cf > 0, eligible & (cb == 0) & cf.notna())),
                             "new plaque if also calcium 0 at BL (combined definition)": cell(ev.where(cb == 0))}
        auc_tab[name] = {p: auc(x, ev) for p, x in preds.items()}
        if years.notna().sum() >= 3 * MIN_CELL:
            tert = pd.qcut(years, 3, labels=["1 short", "2 middle", "3 long"]).astype(object)
            tert_tab[name] = {g: cell(ev[tert == g]) for g in ("1 short", "2 middle", "3 long")}
        if name in TRUNKS:
            events[name] = ev

    pooled = pd.concat(events, names=["artery", "pid"])
    v = pooled.dropna()
    ic = icc(pooled)
    n_pat = v.index.get_level_values(-1).nunique()
    out["eligibility flow per artery"] = flow
    out["outcomes per artery"] = outcomes
    out["pooled LAD + CX + RCA"] = {
        "eligible arteries with known outcome": count(len(v)), "new plaque": cell(v),
        "patients contributing": count(n_pat),
        "patients with an event": count_of(v[v == 1].index.get_level_values(-1).nunique(), n_pat),
        "ICC within patient": ic, "design effect": 1 + (len(v) / max(n_pat, 1) - 1) * ic if ic is not None else None,
        "max predictors at 10 events per predictor (ignoring clustering)": int(min(v.sum(), len(v) - v.sum()) // 10)}
    per_patient = v.groupby(level=-1).size()
    out["eligible arteries per patient"] = levels(per_patient.reindex(B.index, fill_value=0))
    out["where the new plaque appeared (among arteries with an event)"] = where
    out["calcium check per artery"] = calcium
    out["AUC of single BL predictors for new plaque (0.5 = no signal)"] = auc_tab
    if tert_tab:
        out["new plaque by follow-up tertile (should rise with time)"] = tert_tab
    if "rand_group" in F:
        groups = F["rand_group"].map(key)
        out["new plaque by randomisation group (pooled)"] = {
            g: cell(pooled[pooled.index.get_level_values(-1).isin(groups.index[groups == g])])
            for g in sorted(groups.unique(), key=order)}
    return out


def worst_category(df):
    flags = {c: yes(df[f"ct_cag_{c}"]) for c in CATEGORIES if f"ct_cag_{c}" in df}
    if not flags:
        return None
    worst = pd.Series(np.nan, index=df.index, dtype=object)
    for c in CATEGORIES:
        if c in flags:
            worst[flags[c] == 1] = c
    return worst


def categories(B, F, binary):
    wb, wf = worst_category(B), worst_category(F)
    if wb is None or wf is None:
        return {"note": "ct_cag_none ... ct_cag_occlusion missing"}
    ob = flag(wb.isin(OBSTRUCTIVE), wb.notna())
    of = flag(wf.isin(OBSTRUCTIVE), wf.notna())
    binary["incident_obstructive_cad"] = flag(of == 1, (ob == 0) & of.notna())
    order = [c for c in CATEGORIES] + ["missing"]
    rank = {c: i for i, c in enumerate(CATEGORIES)}
    binary["worst_category_worsened"] = flag(wf.map(rank) > wb.map(rank), wb.notna() & wf.notna())
    t = crosstab(wb, wf, allow_text=True)
    return {"worst stenosis category BL -> FU (highest flag set)": {
                r: {c: t[r].get(c, 0) for c in order} for r in order if r in t},
            "obstructive (moderate+) at BL": frac(ob), "obstructive at FU": frac(of),
            "incident obstructive CAD": frac(binary["incident_obstructive_cad"]),
            "worst category worsened": frac(binary["worst_category_worsened"])}


def events(B, F, binary):
    out, hard = {}, []
    for c in EVENT_COLS:
        if c not in B or c not in F:
            continue
        b, f = yes(B[c]), yes(F[c])
        new = flag(f == 1, (b == 0) & f.notna())
        binary[f"incident {c}"] = new
        if c in HARD_EVENT_COLS:
            hard.append(new)
        out[c] = {"BL -> FU": crosstab(b, f), "incident (no at BL, yes at FU)": frac(new),
                  "yes at BL, no at FU (data check)": count(((b == 1) & (f == 0)).sum())}
    if hard:
        binary["incident hard composite (MI/revasc/stent/CABG)"] = pd.concat(hard, axis=1).max(axis=1)
        out["incident hard composite (MI/revasc/stent/CABG)"] = frac(binary["incident hard composite (MI/revasc/stent/CABG)"])
    out["FU-only history (cannot separate new from pre-existing)"] = {
        c: levels(F[c]) for c in FU_ONLY_HISTORY if c in F}
    ae = {c: levels(F[c]) for c in ("ae_serious", "ae_grade", "ae_criteria", "ae_intervention_related",
                                    "ae_outcome_status") if c in F}
    if ae:
        out["adverse events (trial, FU)"] = ae
    return out


def medication(B, F):
    out = {c: crosstab(yes(B[c]), yes(F[c])) for c in MEDS_BOTH if c in B and c in F}
    out["FU only"] = {c: levels(F[c]) for c in MEDS_FU_ONLY if c in F}
    return out


def lipid_change(B, F):
    if "med_lipid_lowering_any" not in B or "med_lipid_lowering_any" not in F:
        return None
    b, f = yes(B["med_lipid_lowering_any"]), yes(F["med_lipid_lowering_any"])
    labels = np.select([(b == 0) & (f == 0), (b == 0) & (f == 1), (b == 1) & (f == 0), (b == 1) & (f == 1)],
                       ["never", "started", "stopped", "continued"], default="missing")
    return pd.Series(labels, index=B.index)


def stratified(strata, cont, binary, B, years):
    """Outcomes per group, plus what differs between the groups at BL (follow-up time, risk factors,
    which variables were collected) - a group difference in outcome may come from these."""
    missing_cols = [c for c in PREDICTORS + EVENT_COLS + tuple(f"ct_cag_{c}" for c in CATEGORIES) if c in B]
    out = {}
    for sname, groups in strata.items():
        if groups is None:
            continue
        groups = groups.map(key)
        gs = sorted(groups.unique(), key=order)
        out[sname] = {
            "group sizes": levels(groups, allow_text=True),
            "follow-up years": {g: describe(years[groups == g]) for g in gs},
            "BL predictor mean": {p: {g: describe(num(B[p])[groups == g]).get("mean") for g in gs}
                                  for p in PREDICTORS if p in B},
            "% missing at BL (were variables collected in every group?)": {
                c: {g: pct(B[c][groups == g].isna().sum(), (groups == g).sum()) for g in gs} for c in missing_cols},
            "binary outcomes (% events)": {o: {g: frac(y[groups == g])["pct"] for g in sorted(groups.unique())}
                                           for o, y in binary.items()},
            "continuous outcomes (median)": {o: {g: describe(cont[o][groups == g]).get("median", f"<{MIN_CELL}")
                                                 for g in sorted(groups.unique())}
                                             for o in KEY_CONTINUOUS if o in cont},
        }
    return out


def smd(a, b):
    a, b = a.dropna(), b.dropna()
    if len(a) < MIN_CELL or len(b) < MIN_CELL:
        return None
    sd = np.sqrt((a.var() + b.var()) / 2)
    return (a.mean() - b.mean()) / sd if sd > 0 else None


def associations(B, cont, binary):
    preds = {p: num(B[p]) for p in PREDICTORS if p in B}
    spearman, by_outcome = {}, {}
    for o in KEY_CONTINUOUS:
        if o not in cont:
            continue
        spearman[o] = {}
        for p, x in preds.items():
            d = pd.concat([x, cont[o]], axis=1).dropna()
            spearman[o][p] = d.rank().corr().iloc[0, 1] if len(d) >= MIN_CELL else None
    for o, y in binary.items():
        by_outcome[o] = {p: smd(x[y == 1], x[y == 0]) for p, x in preds.items()}
    return {"Spearman rho, BL predictor vs continuous outcome": spearman,
            "standardised mean difference of BL predictor, events vs non-events": by_outcome}


def feasibility(binary, cont, B):
    rows = {}
    for o, y in binary.items():
        valid = y.dropna()
        k, n = int(valid.sum()), len(valid)
        minority = min(k, n - k)
        rows[o] = {"n": count(n), "events": count_of(k, n), "pct": pct(k, n),
                   "max predictors at 10 EPV": minority // 10 if minority >= MIN_CELL else 0,
                   "max predictors at 20 EPV": minority // 20 if minority >= MIN_CELL else 0}
    present = [p for p in PREDICTORS if p in B]
    complete = B[present].notna().all(axis=1) if present else pd.Series(False, index=B.index)
    usable = [p for p in present if B[p].isna().mean() < 0.2]
    complete_usable = B[usable].notna().all(axis=1) if usable else pd.Series(False, index=B.index)
    return {"binary outcomes": rows,
            "continuous outcomes (n available)": {o: count(cont[o].notna().sum()) for o in cont},
            "BL predictors (paired patients)": {
                "predictors present": len(present), "predictors absent": ", ".join(p for p in PREDICTORS if p not in B) or "none",
                "complete cases on all present predictors": count(complete.sum()),
                "predictors with >= 20% missing": ", ".join(p for p in present if p not in usable) or "none",
                "complete cases on predictors with < 20% missing": count(complete_usable.sum()),
                "missing per predictor": {p: count_of(B[p].isna().sum(), len(B)) for p in present}}}


def attrition(bl, paired_ids):
    has_fu = pd.Series(bl.index.isin(paired_ids), index=bl.index)
    out = {}
    for p in PREDICTORS:
        if p not in bl:
            continue
        x = num(bl[p])
        out[p] = {"with FU: mean": describe(x[has_fu]).get("mean"), "without FU: mean": describe(x[~has_fu]).get("mean"),
                  "SMD": smd(x[has_fu], x[~has_fu])}
    return out


def quality(B, F):
    out = {"BL": {c: levels(B[c]) for c in QUALITY_BL if c in B},
           "FU": {c: levels(F[c]) for c in QUALITY_FU if c in F}}
    for v in VESSELS:
        for c in [f"ct_cag_{v}_uneval"] + [f"ct_cag_{v}_uneval_{r}" for r in ("contrast", "scanfield", "pm", "noise")]:
            if c in F:
                out["FU"][c] = levels(F[c])
            if c in B:
                out["BL"][c] = levels(B[c])
    if "ct_cag_eval_n" in B:
        out["BL"]["ct_cag_eval_n (evaluable segments)"] = describe(B["ct_cag_eval_n"])
    return out


# ---------------------------------------------------------------- output

def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        return None if not np.isfinite(o) else round(float(o), 4)
    return o


def scalar(v):
    return not isinstance(v, dict)


def fmt(v):
    if v is None:
        return ""
    if isinstance(v, float):
        return f"{v:.3g}" if abs(v) < 1e4 else f"{v:.0f}"
    return str(v)


def render(obj, depth, lines):
    flat = {k: v for k, v in obj.items() if scalar(v)}
    if flat:
        lines += ["| | |", "|---|---|"] + [f"| {k} | {fmt(v)} |" for k, v in flat.items()] + [""]
    for k, v in obj.items():
        if scalar(v):
            continue
        lines.append(f"{'#' * min(depth, 6)} {k}\n")
        rows = list(v.values())
        if rows and all(isinstance(r, dict) and all(scalar(x) for x in r.values()) and r.keys() == rows[0].keys()
                        for r in rows):  # rows sharing the same columns -> one table
            cols = list(rows[0])
            lines += ["| | " + " | ".join(map(str, cols)) + " |", "|---" * (len(cols) + 1) + "|"]
            lines += [f"| {r} | " + " | ".join(fmt(v[r].get(c)) for c in cols) + " |" for r in v] + [""]
        else:
            render(v, depth + 1, lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--bl", default=BL_PATH, help="baseline data file (default BL_PATH)")
    ap.add_argument("--fu", default=FU_PATH, help="follow-up data file (default FU_PATH)")
    ap.add_argument("--out", default=OUT_DIR, help="folder for the aggregate results (default OUT_DIR)")
    ap.add_argument("--monthfirst", action="store_true", help="text dates are mm/dd (default dd/mm)")
    args = ap.parse_args()
    for name, path in (("BL_PATH", args.bl), ("FU_PATH", args.fu)):
        if not Path(path).is_file():
            raise SystemExit(f"{name} not found: {path} (set it at the top of {Path(__file__).name})")
    dayfirst = not args.monthfirst

    (bl_raw, decoded_bl), (fu_raw, decoded_fu) = decode_segments(load(args.bl)), decode_segments(load(args.fu))
    for name, df in (("BL", bl_raw), ("FU", fu_raw)):
        if "study_id" not in df:
            raise SystemExit(f"{name} file has no study_id column")
    columns_bl, values_bl = column_summary(bl_raw, dayfirst)
    columns_fu, values_fu = column_summary(fu_raw, dayfirst)

    dup_bl, dup_fu = int(bl_raw["study_id"].duplicated().sum()), int(fu_raw["study_id"].duplicated().sum())
    bl = bl_raw.drop_duplicates("study_id").set_index("study_id")
    fu = fu_raw.drop_duplicates("study_id").set_index("study_id")
    ids = bl.index.intersection(fu.index)
    B, F = bl.loc[ids], fu.loc[ids]
    if "scandate" in B and "scandate" in F:
        years = (dates(F["scandate"], dayfirst) - dates(B["scandate"], dayfirst)).dt.days / 365.25
    else:
        years = pd.Series(np.nan, index=ids)

    cont, binary = {}, {}
    sections = {
        "1. Cohort and follow-up": cohort(bl, fu, B, F, years, dup_bl, dup_fu),
        "3. Coronary calcium (CAC) progression": cac(B, F, years, cont, binary),
        "4. Segment involvement / stenosis / plaque-type scores": scores(B, F, years, cont, binary),
        "5. Segment-level stenosis, plaque and high-risk features": {
            "text labels decoded (BL)": decoded_bl, "text labels decoded (FU)": decoded_fu,
            **segments(B, F, cont, binary)},
        "6. Plaque trajectory groups (none->none, none->plaque, plaque->same/more/less)": plaque_trajectories(B, F, binary),
        "0. Chosen design: plaque-free LAD / CX / RCA trunks, new plaque anywhere in the trunk": artery_design(B, F, years),
        "7. Outcome definitions by anatomical level (segment, position, vessel, whole tree)": outcome_levels(B, F, years),
        "8. Patient-level stenosis category": categories(B, F, binary),
        "9. Clinical events between the scans": events(B, F, binary),
        "10. Medication BL -> FU": medication(B, F),
    }
    sten_bl = [c for c in (f"ct_cag_{s}_stenosis" for s in SEGMENTS) if c in B]
    read_bl = pd.Series(np.where(B[sten_bl].notna().any(axis=1), "read", "not read"), index=B.index) if sten_bl else None
    scan_year = dates(B["scandate"], dayfirst).dt.year if "scandate" in B else None
    strata = {"rand_group (FU)": col(F, "rand_group"), "lipid-lowering BL -> FU": lipid_change(B, F),
              "male (BL)": col(B, "male"), "BL segment reads present": read_bl, "BL scan year": scan_year}
    sections["2. Outcome feasibility (events and events-per-variable)"] = feasibility(binary, cont, B)
    sections["11. Outcomes by randomisation group, lipid-lowering change and sex"] = stratified(strata, cont, binary, B, years)
    sections["12. Baseline predictor vs outcome associations"] = associations(B, cont, binary)
    sections["13. Loss to follow-up: BL characteristics with vs without FU"] = attrition(bl, ids)
    sections["14. Image quality and evaluability (paired patients)"] = quality(B, F)
    sections = dict(sorted(sections.items(), key=lambda kv: int(kv[0].split(".")[0])))
    stats = clean({"settings": {"MIN_CELL": MIN_CELL, "MAX_LEVELS": MAX_LEVELS, "NO_PLAQUE": list(NO_PLAQUE),
                                "dayfirst": dayfirst},
                   **sections,
                   "15. Value counts per column": {"BL": values_bl, "FU": values_fu}})

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    lines = ["# CGPS outcome statistics\n",
             f"Aggregates only. Counts 1-{MIN_CELL - 1} are shown as <{MIN_CELL}. "
             "Per-column summaries are in columns_bl.csv / columns_fu.csv, value counts in stats.json.\n"]
    render({k: v for k, v in stats.items() if not k.startswith("15.")}, 2, lines)
    written = [out / "report.md", out / "stats.json", out / "columns_bl.csv", out / "columns_fu.csv"]
    written[0].write_text("\n".join(lines))
    written[1].write_text(json.dumps(stats, indent=1, ensure_ascii=False))
    pd.DataFrame(clean(columns_bl)).to_csv(written[2], index=False)
    pd.DataFrame(clean(columns_fu)).to_csv(written[3], index=False)
    print("wrote (aggregates only):")
    for p in written:
        print(f"  {p}")


if __name__ == "__main__":
    main()
