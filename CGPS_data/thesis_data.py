"""The numbers the thesis needs from HØ_10Y, and how good the Medis reference is.

    python CGPS_data/thesis_data.py --workers 8      # everything (reads the BL volumes with Medis files)
    python CGPS_data/thesis_data.py --no-voxels      # tables, file coverage and contour geometry only

A. Data for who/where (definitions as decided in ~/Desktop/Speciale/CGPS_statistics-/CLAUDE.md):
   cohort flow, outcome = any new plaque in the 9 trunk segments, where-informative people,
   events per segment, follow-up, dominance, covariate completeness, parameter budget.
B. Medis reference: coverage of the cohort, tree labels and connections, centerline on the lumen
   (inside volume, HU, brighter than 3 mm off), contours (lumen inside wall, centred, contrast,
   size), contour centerline vs tree. "Usable" = passes every check; it is agreement with the
   CT, not ground truth.

Writes OUT_DIR/thesis_data.md. Aggregates only (cgps_stats.py suppression), no study_id.
"""
from __future__ import annotations

import argparse
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

import centerline_qc as cq
import hoe10y_qc as hq
from cgps_stats import OUT_DIR, count, describe, num, pct, yes
from clean_baseline_count import read_at_bl

TRUNK = ("prca", "mrca", "drca", "plad", "mlad", "dlad", "pcx", "mcx", "dcx")
OTHER = ("lm", "d1", "d2", "im", "om1", "om2", "pda", "pla")
COVARIATES = ("scan_age", "male", "hist_smoking_current", "clin_bp_sys_mean", "tot_cholesterol", "hdl",
              "score2", "score2_op", "hist_diabetes", "clin_bmi", "clin_height", "med_lipid_lowering_any",
              "ct_cag_dominance", "scandate")
PARAMS = 1 + 5 + 1 + 1  # SCORE2 block as one predictor, 5 geometry numbers, follow-up, dominance


def table(rows, header):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    return "\n".join(out + ["| " + " | ".join("" if v is None else str(v) for v in r) + " |" for r in rows]) + "\n"


def dist(name, x, nd=2):
    d = describe(x)
    r = lambda k: None if d.get(k) is None else round(float(d[k]), nd)
    return [name, d["n"], r("p25"), r("median"), r("p75")]


def grades(df, segs):
    g = pd.DataFrame({s: df[f"ct_cag_{s}_stenosis"].map(hq.grade_of) for s in segs
                      if f"ct_cag_{s}_stenosis" in df}, index=df.index)
    return g.where(g.isin(hq.GRADES)).replace({k: i for i, k in enumerate(hq.GRADES)}).astype(float)


# ---------------------------------------------------------------- A. data for the thesis
def data_section(bl, fu, bl_vol):
    sis, sss = num(bl["ct_cag_sis"]), num(bl["ct_cag_sss"])
    clean, read = (sis == 0) & (sss == 0), read_at_bl(bl.reset_index()).set_axis(bl.index)
    t = grades(fu, TRUNK).reindex(bl.index)
    o = grades(fu, OTHER).reindex(bl.index)
    fu_read = t.notna().any(axis=1)
    has_vol = pd.Series(bl.index.isin(bl_vol), index=bl.index)
    good = ~(yes(bl["bad_quality"]) == 1) if "bad_quality" in bl else pd.Series(True, index=bl.index)
    steps = [("BL patients", pd.Series(True, index=bl.index)), ("clean baseline (SIS = 0, new SSS = 0)", clean),
             ("... read at BL (ct_cag_visual_read)", clean & read), ("... trunk segments read at FU", clean & read & fu_read),
             ("... BL CT volume on disk", clean & read & fu_read & has_vol),
             ("... not bad image quality", clean & read & fu_read & has_vol & good)]
    C = steps[3][1]
    rep = ["## A. Data for the who and where questions\n", "### Cohort flow\n",
           table([(n, count(m.sum())) for n, m in steps], ["step", "patients"]),
           f"Clean but not read at BL (unread segments filled 'none'): {count((clean & ~read).sum())}. "
           "The analyses below use the 'trunk segments read at FU' row; volume and quality decide the final n.\n"]

    tc, oc = t[C], o[C]
    y = (tc >= 1).any(axis=1).astype(float)
    n, k = len(y), int(y.sum())
    vol = has_vol[C]
    rep += ["### Who: any new plaque in the 9 trunk segments\n", table([
        ("people", count(n), count(vol.sum())),
        ("developed trunk plaque", f"{count(k)} ({pct(k, n)}%)", count(y[vol].sum())),
        ("plaque only in LM / side branches (counted as no plaque)", count(((y == 0) & (oc >= 1).any(axis=1)).sum()), ""),
        ("no plaque seen but a trunk segment ungraded (outcome uncertain)", count(((y == 0) & tc.isna().any(axis=1)).sum()), ""),
        ("≥ mild trunk plaque (secondary outcome)", count((tc >= 2).any(axis=1).sum()), "")],
        ["", "all", "with BL volume"]),
        f"Parameter budget: {count(k)} events = {min(k, n - k) // 10} parameters at 10 events/parameter, "
        f"{min(k, n - k) // 20} at 20. Planned who model: {PARAMS} (SCORE2 block, 5 geometry numbers, follow-up, "
        "dominance); confirm with pmsampsize.\n"]

    per_seg = [(s, count((tc[s] >= 1).sum()), count(tc[s].notna().sum())) for s in TRUNK if s in tc]
    pos = (tc >= 1).sum(axis=1)
    graded = tc.notna().sum(axis=1)
    informative = (pos >= 1) & (pos < graded)
    nper = pos[pos >= 1].clip(upper=4).value_counts().sort_index()
    rep += ["### Where: segments within a person\n", table(per_seg, ["segment", "new plaque", "graded at FU"]),
            f"Informative people (plaque in some but not all graded trunk segments): {count(informative.sum())} — "
            "the effective sample of the conditional logistic model.\n",
            table([(int(i) if i < 4 else "≥4", count(v)) for i, v in nper.items()],
                  ["trunk segments with plaque", "people"])]

    dom = bl.loc[C, "ct_cag_dominance"].astype(str).str.lower() if "ct_cag_dominance" in bl else None
    yrs = (pd.to_datetime(fu.reindex(bl.index).loc[C, "scandate"], errors="coerce")
           - pd.to_datetime(bl.loc[C, "scandate"], errors="coerce")).dt.days / 365.25
    rep += ["### Follow-up, dominance and covariates\n",
            table([dist("BL -> FU years", yrs)], ["", "n", "p25", "median", "p75"])]
    if dom is not None:
        rep.append(table([(d, count(v)) for d, v in dom.value_counts().items()], ["dominance", "people"]))
    age = num(bl.loc[C, "scan_age"])
    rows = [(c, count(bl.loc[C, c].notna().sum()) if c in bl else "not in table") for c in COVARIATES]
    rep += [table(rows, ["covariate", "people with a value"]),
            f"Outside the SCORE2 age range 40–69: {count(((age < 40) | (age >= 70)).sum())} "
            "(score2_op covers ≥ 70). Baseline statin = med_lipid_lowering_any (med_statin is FU only).\n"]
    return rep, C[C].index


# ---------------------------------------------------------------- B. reference quality
def reference_section(found, bl, cohort, args):
    tree_of = {t["id"]: t["path"] for t in found["trees"] if t["id"]}
    cont = {}
    for (v, i, s), files in found["contours"].items():
        if v == "BL":
            cont.setdefault(i, {})[s] = files
    nifti = {x["id"]: x["path"] for x in found["niftis"] if x["visit"] == "BL" and x["id"]}
    sis = num(bl["ct_cag_sis"])
    ids = sorted(set(tree_of) | set(cont), key=int)
    rep = ["## B. Medis reference (centerlines and lumen)\n", table([
        ("patients with a Medis tree", count(len(tree_of)), count(len(set(tree_of) & set(cohort)))),
        ("... of which plaque at BL (SIS > 0)", count((sis.reindex(list(tree_of)) > 0).sum()), ""),
        ("patients with contours", count(len(cont)), count(len(set(cont) & set(cohort)))),
        ("contoured segments", count(sum(len(v) for v in cont.values())), ""),
        ("Medis patients with a BL volume", count(len(set(ids) & set(nifti))), "")],
        ["", "all", "in the analysis cohort"]),
        "Contours exist only for diseased segments, so they cannot reach the clean cohort; trees can.\n"]

    topo, seg_len, _, terr = hq.tree_topology([{"visit": "BL", "id": i, "path": p} for i, p in tree_of.items()])
    tasks = [{"id": i, "visit": "BL", "nifti": nifti.get(i), "voxels": not args.no_voxels, "tree": tree_of.get(i),
              "contours": cont.get(i, {}), "out": args.out, "figs": False} for i in ids]
    with Pool(args.workers, hq.init_worker, (cq._numbering, dict(cq._code_names), "lps", args.out)) as pool:
        res = pool.map(hq.process, tasks, chunksize=1)
    T = pd.DataFrame([r["tree"] for r in res if r["tree"]])
    S = pd.DataFrame([s for r in res for s in r["segments"]])
    if len(T) and len(topo):
        T = topo.merge(T.drop(columns="visit"), on="id", how="left")
    elif len(topo):
        T = topo

    if len(T):
        names = {"pRCA", "mRCA", "dRCA", "pLAD", "mLAD", "dLAD", "pCX", "mCX", "dCX", "CX", "LM"}
        sl = seg_len[seg_len.segment.isin(names)].pivot_table(index="id", columns="segment", values="length_mm")
        rows = [dist(c, T[c]) for c in ("unlabelled_pct", "total_mm", "n_components", "inside_frac", "hu_median",
                                         "dark_frac", "center_minus_off3mm", "n_kinks") if c in T]
        rep += ["### Centerline trees\n", f"{count(len(T))} trees read ({count(len(terr))} unreadable). Coordinates LPS; "
                f"best convention per tree: { {k: count(v) for k, v in T['best_convention'].value_counts().items()} if 'best_convention' in T else 'not checked'}.\n",
                table(rows, ["metric", "n", "p25", "median", "p75"]),
                table([dist(s, sl[s], 1) for s in sl.columns], ["labelled segment (length mm)", "trees", "p25", "median", "p75"])]
        conn = [c for c in ("conn_pLAD", "conn_pCX", "conn_mLAD", "conn_mRCA", "conn_CX") if c in T]
        rep.append(table([(c[5:], *[count((T[c] == v).sum()) for v in ("direct", "via_unlabelled", "missing")]) for c in conn],
                         ["child -> parent", "direct", "via unlabelled", "missing"]))
        ok = ~T["impossible_contacts"].astype(bool) & (T["unlabelled_pct"] <= 20) & (T["n_components"] <= 2)
        if "center_minus_off3mm" in T:
            ok &= (T["inside_frac"] >= 1) & (T["center_minus_off3mm"] > 100)
        rep.append(f"**Trees usable as reference** (no impossible contact, ≤ 20% unlabelled, ≤ 2 components"
                   f"{', fully inside the volume, centre > 100 HU brighter than 3 mm off' if 'center_minus_off3mm' in T else ''}): "
                   f"{count(ok.sum())} of {count(len(T))}; in the analysis cohort {count(ok[T['id'].isin(cohort)].sum())}.\n")

    if len(S):
        rows = [dist(c, S[c]) for c in ("cl_to_tree_median_mm", "tree_label_same_artery", "centroid_to_cl_mm_max",
                                         "cos_normal_tangent_min", "lumen_inside_outer_frac_min", "min_lumen_eq_diam",
                                         "plaque_burden_max", "hu_lumen_core_median", "hu_peri_median",
                                         "lumen_minus_peri_hu") if c in S]
        bad = S["flags"].fillna("").str.contains("lumen_outside_outer|ring_off_centerline|low_lumen_contrast|cl_off_tree|"
                                                 "lumen_area>outer|incomplete_file_set|cl_outside_volume")
        rep += ["### Lumen and wall contours\n", table(rows, ["metric", "n", "p25", "median", "p75"]),
                f"**Contoured segments usable as reference** (complete file set, inside the volume, rings centred and "
                f"lumen inside the wall, contour centerline on the tree, lumen brighter than surroundings): "
                f"{count((~bad).sum())} of {count(len(S))}.\n"]
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=hq.ROOT)
    ap.add_argument("--out", default=OUT_DIR)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--no-voxels", action="store_true")
    args = ap.parse_args()

    found = hq.discover(args.root)
    sheets = hq.load_sheets(args.root)
    bl, fu = (sheets[v].assign(id=sheets[v]["study_id"].map(hq.norm_id)).drop_duplicates("id").set_index("id")
              for v in ("BL", "FU"))
    bl_vol = {x["id"] for x in found["niftis"] if x["visit"] == "BL"}
    rep_a, cohort = data_section(bl, fu, bl_vol)
    rep = ["# HØ_10Y: data for the thesis and the Medis reference\n",
           "Aggregates only; counts 1–4 shown as <5. Generated by `CGPS_data/thesis_data.py`.\n",
           *rep_a, *reference_section(found, bl, set(cohort), args)]
    out = Path(args.out).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    (out / "thesis_data.md").write_text("\n".join(rep), encoding="utf-8")
    print("\n".join(rep))
    print(f"wrote {out / 'thesis_data.md'}")


if __name__ == "__main__":
    main()
