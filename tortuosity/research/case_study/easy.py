"""Classical (easy) tortuosity measures for two RCAs, scans 662 and 518 (ImageCAS-X train).

Reads only the delivered right centerline VTKs. RCA = label 9, longest geodesic path
(tortuosity/vessels.py), oriented ostium to distal using the VTK start_points array.
Resample 0.25 mm arc length, no extra smoothing (the file already carries a 0.5 mm Gaussian
smoothing). Percentiles among the 560 training RCAs from compute_simple.py (simple_measures.csv).

Writes $OUT/easy_metrics.json and $OUT/easy_pointwise.npz; prints a bend table.
Run: source env.sh && python tortuosity/research/case_study/easy.py
"""
import json
import os
import sys

import numpy as np
import pandas as pd
from vtk.util.numpy_support import vtk_to_numpy

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "simple"))
from compute_simple import H, KFLOOR, basis, length, resample, soam_icm, turns, view_dir  # noqa: E402
from tortuosity.merged import chord_resample  # noqa: E402
from tortuosity.vessels import longest_path  # noqa: E402
import vtk  # noqa: E402

DATA = os.environ["ImageCAS_X_data_path"]
SIMPLE = "/work3/s254124/imagecasx_results/tortuosity_research/simple"
OUT = "/work3/s254124/imagecasx_results/tortuosity_research/case_study"
IDS = ["662", "518"]
LAO30, RAO30 = view_dir(30, 0), view_dir(-30, 0)


def load_rca(cid):
    r = vtk.vtkPolyDataReader()
    r.SetFileName(f"{DATA}/centerlines/{cid}.coronary_right_centerline.vtk")
    r.ReadAllScalarsOn()
    r.ReadAllFieldsOn()
    r.Update()
    p = r.GetOutput()
    pts = vtk_to_numpy(p.GetPoints().GetData()).astype(np.float64)
    lab = vtk_to_numpy(p.GetPointData().GetArray("segment_label"))
    start = pts[vtk_to_numpy(p.GetPointData().GetArray("start_points")) > 0][0]
    lines, ids, edges = p.GetLines(), vtk.vtkIdList(), []
    lines.InitTraversal()
    while lines.GetNextCell(ids):
        c = [ids.GetId(i) for i in range(ids.GetNumberOfIds())]
        edges += zip(c[:-1], c[1:])
    edges = np.array(edges)
    P = longest_path(pts, edges[(lab[edges[:, 0]] == 9) & (lab[edges[:, 1]] == 9)])
    if np.linalg.norm(P[-1] - start) < np.linalg.norm(P[0] - start):
        P = P[::-1]
    return P, np.linalg.norm(P[0] - start)


def arcpos(S, s, V):
    """Arc length on S of each chord vertex V (monotone nearest-point search)."""
    out, k = [], 0
    for v in V:
        j = k + int(np.argmin(np.linalg.norm(S[k:k + 400] - v, axis=1)))
        out.append(s[j])
        k = j
    return np.array(out)


def bends_pos(S, s, l=1.0):
    """Bends as (start mm, centre mm, end mm, angle deg). Same rule as compute_simple.bends:
    runs of 1 mm chord vertices turning > KFLOOR * l, split at binormal flips."""
    Q = S if S.shape[1] == 3 else np.c_[S, np.zeros(len(S))]
    V = chord_resample(Q, l)
    sv = arcpos(Q, s, V)[1:-1]  # arc position of each turning vertex
    u, th = turns(V)
    b = np.cross(u[:-1], u[1:])
    out, run, prev_b = [], [], None
    for k in range(len(th)):
        if th[k] <= KFLOOR * l:
            if run:
                out.append(run)
            run, prev_b = [], None
            continue
        bk = b[k] / np.linalg.norm(b[k])
        if prev_b is not None and bk @ prev_b < 0:
            out.append(run)
            run = []
        run.append(k)
        prev_b = bk
    if run:
        out.append(run)
    return [(sv[r[0]], (th[r] * sv[r]).sum() / th[r].sum(), sv[r[-1]], np.degrees(th[r].sum()))
            for r in out]


def turn5(S, s, l=5.0):
    """Per point: angle between the chords to the points l mm (Euclidean) behind and ahead,
    divided by half the arc between them (rad/mm). NaN where either point does not exist."""
    out = np.full(len(S), np.nan)
    for i in range(len(S)):
        db = np.linalg.norm(S[:i + 1][::-1] - S[i], axis=1)
        df = np.linalg.norm(S[i:] - S[i], axis=1)
        if not ((db >= l).any() and (df >= l).any()):
            continue
        b, f = i - int(np.argmax(db >= l)), i + int(np.argmax(df >= l))
        u1, u2 = S[i] - S[b], S[f] - S[i]
        c = u1 @ u2 / np.linalg.norm(u1) / np.linalg.norm(u2)
        out[i] = np.arccos(np.clip(c, -1, 1)) / ((s[f] - s[b]) / 2)
    return out


def ti10(S, w=10.0):
    h = int(round(w / 2 / H))
    out = np.full(len(S), np.nan)
    out[h:len(S) - h] = w / np.linalg.norm(S[2 * h:] - S[:len(S) - 2 * h], axis=1)
    return out


def dm2(S, d):
    S2 = S @ basis(d)
    return length(S2) / np.linalg.norm(S2[-1] - S2[0]), S2


def eleid(bd):
    """Eleid-like grade from bend angles in arc order, ignoring the 2 mm diameter qualifier.
    'consecutive' = adjacent in the bend list. Returns (loose grade, strict grade)."""
    a = np.array([x[3] for x in bd])

    def maxrun(m):
        best = cur = 0
        for v in m:
            cur = cur + 1 if v else 0
            best = max(best, cur)
        return best

    def grade(n):
        return 3 if n(a >= 180) >= 2 else 2 if n((a >= 90) & (a < 180)) >= 3 else \
            1 if n((a >= 45) & (a < 90)) >= 3 else 0
    return grade(lambda m: int(m.sum())), grade(maxrun)


def case(cid):
    P, off = load_rca(cid)
    S = resample(P)
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(S, axis=0), axis=1))]
    L, D = s[-1], np.linalg.norm(S[-1] - S[0])
    V5 = chord_resample(S, 5.0)
    th5 = turns(V5)[1]
    soam, soam_ip, n_infl = soam_icm(S, L)
    bd = bends_pos(S, s)
    dmL, S2 = dm2(S, LAO30)
    dmR, _ = dm2(S, RAO30)
    bd2 = bends_pos(S2, s)
    a = np.array([x[3] for x in bd])
    mx = max(bd, key=lambda x: x[3]) if bd else (np.nan, np.nan, np.nan, 0.0)
    t5, t10 = turn5(S, s), ti10(S)
    return dict(P=P, S=S, s=s, L=L, D=D, DM=L / D, ka=th5.sum() / L, tot=th5.sum(), soam=soam,
                soam_ip=soam_ip, n_infl=n_infl, bd=bd, bd2=bd2, a=a, mx=mx, dmL=dmL, dmR=dmR,
                t5=t5, t10=t10, eleid=eleid(bd), eleid2=eleid(bd2), off=off,
                n45=int((a >= 45).sum()), n90=int((a >= 90).sum()))


def pct(df, col, v, ids_ref=None):
    x = df[col].dropna().to_numpy()
    return round(float((x < v).mean() * 100 + (x == v).mean() * 50), 1)


MEANING = {
    "L": "centreline arc length; matched by design so it should not drive the contrast",
    "D": "straight ostium-to-distal distance; the shorter it is for a given L, the more the course folds back",
    "DM": "Bullitt distance metric = arc/chord; whole-course winding, dominated by the large C shape of the RCA",
    "TI": "tortuosity index = DM - 1, the extra path length per mm of straight distance",
    "DM2_LAO30": "arc/chord of the shadow in the standard RCA view (LAO 30), what an angiographer would measure",
    "DM2_RAO30": "arc/chord of the shadow in RAO 30, the orthogonal-ish view; shows how view choice moves 2D DM",
    "kappa_a5": "mean turning per mm at 5 mm chord; local bendiness, blind to how the bends add up globally",
    "total_turning_rad": "sum of 5 mm chord turning angles over the whole vessel = kappa_a5 x L",
    "total_turning_deg": "same total turning in degrees; 360 would be one full loop",
    "SOAM_inplane": "Bullitt SOAM in-plane term at 1 mm steps (rad/cm); like kappa_a but at a 1 mm scale, so noise-sensitive",
    "n_inflections": "Frenet normal flips at 1 mm steps; at 1 mm scale mostly counts centreline wobble, not bends",
    "ICM": "Bullitt inflection count metric = DM x (inflections + 1); inherits the noise of the inflection count",
    "n_bends_ge45": "bends (runs of >0.02 rad/mm turning, split at binormal flips) with cumulative angle >= 45 deg",
    "n_bends_ge90": "bends with cumulative angle >= 90 deg",
    "max_bend_deg": "largest single bend angle; one tight turn, independent of the rest of the vessel",
    "max_bend_at_mm": "arc-length centre of the largest bend, measured from the ostium",
    "n_bends_ge45_LAO30": "bend count >= 45 deg on the LAO 30 projection (angiography-like)",
    "n_bends_ge90_LAO30": "bend count >= 90 deg on the LAO 30 projection",
    "eleid_grade_3D": "Eleid-like grade 0-3 from 3D bends (count rule, no diameter or consecutive check)",
    "eleid_grade_3D_consecutive": "same grade, but bends must be adjacent in the bend list",
    "eleid_grade_LAO30": "Eleid-like grade from the LAO 30 projection bends (closest to the angiographic original)",
    "ti10_max": "largest arc/chord in any 10 mm window; where the single most folded 10 mm stretch sits",
    "ti10_max_at_mm": "arc-length centre of that 10 mm window",
    "ti10_max_beyond10mm": "same, ignoring the first 10 mm so the ostial take-off hook does not win",
    "ti10_max_beyond10mm_at_mm": "arc-length centre of that window",
    "turn5_max_at_mm": "arc-length position of the sharpest local turning at 5 mm chord",
}


def main():
    R = pd.read_csv(f"{SIMPLE}/simple_measures.csv", dtype={"id": str})
    R = R[R.vessel == "RCA"].copy()
    R["tot"] = R.kappa_a5 * R.L
    R["TI"] = R.DM - 1
    js, npz = {}, {}
    for cid in IDS:
        rows = []
        c = case(cid)
        i10 = int(np.nanargmax(c["t10"]))
        i5 = int(np.nanargmax(c["t5"]))
        j10 = int(np.nanargmax(np.where(c["s"] > 10, c["t10"], np.nan)))
        vals = [
            ("L", c["L"], "mm", "L"), ("D", c["D"], "mm", "D"), ("DM", c["DM"], "ratio", "DM"),
            ("TI", c["DM"] - 1, "ratio", "TI"),
            ("DM2_LAO30", c["dmL"], "ratio", "DM2_std"), ("DM2_RAO30", c["dmR"], "ratio", None),
            ("kappa_a5", c["ka"], "rad/mm", "kappa_a5"),
            ("total_turning_rad", c["tot"], "rad", "tot"),
            ("total_turning_deg", np.degrees(c["tot"]), "deg", "tot_deg"),
            ("SOAM_inplane", c["soam_ip"], "rad/cm", "soam_ip"),
            ("n_inflections", c["n_infl"], "count", "n_infl"),
            ("ICM", c["DM"] * (c["n_infl"] + 1), "ratio", "icm"),
            ("n_bends_ge45", c["n45"], "count", "nb45"), ("n_bends_ge90", c["n90"], "count", "nb90"),
            ("max_bend_deg", c["mx"][3], "deg", "max_bend"),
            ("max_bend_at_mm", c["mx"][1], "mm", None),
            ("n_bends_ge45_LAO30", sum(x[3] >= 45 for x in c["bd2"]), "count", "nb45_2d"),
            ("n_bends_ge90_LAO30", sum(x[3] >= 90 for x in c["bd2"]), "count", "nb90_2d"),
            ("eleid_grade_3D", c["eleid"][0], "grade 0-3", None),
            ("eleid_grade_3D_consecutive", c["eleid"][1], "grade 0-3", None),
            ("eleid_grade_LAO30", c["eleid2"][0], "grade 0-3", None),
            ("ti10_max", c["t10"][i10], "ratio", None), ("ti10_max_at_mm", c["s"][i10], "mm", None),
            ("ti10_max_beyond10mm", c["t10"][j10], "ratio", None),
            ("ti10_max_beyond10mm_at_mm", c["s"][j10], "mm", None),
            ("turn5_max_at_mm", c["s"][i5], "mm", None),
        ]
        for name, v, unit, col in vals:
            p = None
            if col == "tot_deg":
                p = pct(R, "tot", c["tot"])
            elif col is not None:
                p = pct(R, col, v)
            rows.append(dict(name=name, value=round(float(v), 4), unit=unit, percentile=p,
                             meaning=MEANING[name]))
        print(f"\n== {cid}: path starts {c['off']:.2f} mm from start_point; "
              f"mean(turn5) {np.nanmean(c['t5']):.4f} vs kappa_a5 {c['ka']:.4f}")
        for lab_, bd in (("3D", c["bd"]), ("LAO30", c["bd2"])):
            big = [x for x in bd if x[3] >= 20]
            print(f"  {lab_} bends >= 20 deg (start, centre, end mm, angle deg):")
            for x in big:
                print("    %6.1f %6.1f %6.1f  %6.1f" % x)
        npz[f"{cid}_xyz"] = c["S"]
        npz[f"{cid}_s"] = c["s"]
        npz[f"{cid}_turn5"] = c["t5"]
        npz[f"{cid}_bends45"] = np.array([x[1] for x in c["bd"] if x[3] >= 45])
        npz[f"{cid}_bends45_deg"] = np.array([x[3] for x in c["bd"] if x[3] >= 45])
        npz[f"{cid}_ti10"] = c["t10"]
        # 10 mm profile summary
        prof = [(a, np.nanmean(c["t10"][(c["s"] >= a) & (c["s"] < a + 10)]),
                 np.nanmean(c["t5"][(c["s"] >= a) & (c["s"] < a + 10)])) for a in range(0, int(c["L"]), 10)]
        print("  profile per 10 mm bin (start mm, mean ti10, mean turn5 rad/mm):")
        for a, x, y in prof:
            print(f"    {a:4d} {x:6.3f} {y:7.4f}")
        js[cid] = rows
    os.makedirs(OUT, exist_ok=True)
    json.dump(js, open(f"{OUT}/easy_metrics.json", "w"), indent=1)
    np.savez(f"{OUT}/easy_pointwise.npz", **npz)
    for cid in IDS:
        print(f"\n{cid}")
        for r in js[cid]:
            print(f"  {r['name']:40s} {r['value']:10.4f} {r['unit']:10s} p={r['percentile']}")


if __name__ == "__main__":
    main()
