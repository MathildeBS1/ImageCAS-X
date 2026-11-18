"""Agreement of the geometric features between the in-house tracer and Medis (sec:method-medis-agreement).

    python CGPS_data/thesis_final/medis_compare.py [--limit N] [--boot 2000] [--out MD] [--rows DIR]
    python CGPS_data/thesis_final/medis_compare.py --check   # synthetic shapes, needs no data

Baseline only. Each Medis participant's tracer tree (tracer_io.tracer_tree) and Medis tree
(hoe10y_qc.tree_points) are divided with split_trunks.split, and the LAD, LCx and RCA are paired by name.
Both are in LPS mm (tracer_probe.md), so no mapping is applied.

Per artery pair:
  shared stretch  each centerline's first and last point is projected onto the other at the closest point;
                  the stretch runs from the later start to the earlier end (shared_stretch). Pairs with a
                  shared stretch under MIN_SHARED mm are left out.
  alignment       median distance from the tracer points of the shared stretch to the Medis centerline; pairs
                  above MAX_OFFSET mm are left out (a wrong vessel or a failed trace). Fixed on 2026-11-18,
                  before any feature difference was looked at.
  curvature       the Menger profile (curvature_feature.curvature_profile) on each full artery, averaged over
                  the shared stretch (segment_mean). Per segment: the tracer's segment boundaries, projected
                  onto the Medis centerline, so both averages cover the same stretch of artery.
Per participant:
  angle           bifurcation_angle.lm_angle on each tree's own LAD and LCx (full trees).
  asymmetry       ln(D_LCx / D_LAD), diameters the median area-equivalent diameter over 5 to 10 mm from O.
                  Medis: lumen rings of the BL contour files (split_check.contour_files) attached to the
                  nearest point of the Medis LAD or LCx. Tracer: needs a lumen contour reader; the delivered
                  tracer files hold none (tracer_io), so the tracer side is reported as not available.

Agreement per feature: difference tracer - Medis in the feature's own unit (curvature also as the log
ratio), bias, SD of the differences, 95% limits of agreement (bias +- 1.96 SD), 95% intervals from a
bootstrap over participants, and the slope of |difference| on the pair mean (a slope away from 0 means the
error grows with size; then use the log ratio). Plaque check: segment curvature differences by the BL
stenosis grade of that segment. against_cohort() reads the limits against the plaque-free cohort SD later.

Writes medis_compare.md next to this script (aggregates only: counts 1-4 hidden, statistics only from
MIN_CELL pairs) and, in --rows (server only, contains study ids), one CSV per level and Bland-Altman plots.
"""
import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/
sys.path.insert(0, str(Path(__file__).resolve().parent))
from curvature_feature import CHORD, curvature_profile, segment_mean  # noqa: E402
from bifurcation_angle import lm_angle  # noqa: E402
from daughter_ratio import DEPTHS, contour_diameter  # noqa: E402

MAX_OFFSET = 2.0  # mm: median tracer-to-Medis distance over the shared stretch above this = not the same vessel
MIN_SHARED = 10.0  # mm: shorter shared stretches are left out
MIN_SEG = 2.0  # mm: a segment needs this much shared stretch for its average
OFF_ARTERY = 2.0  # mm: a Medis lumen ring belongs to the LAD or LCx if its centre lies this close to it
COVER_TOL = 1.0  # mm: the rings must reach within this of both ends of the 5 to 10 mm window
ARTERIES = ("LAD", "CX", "RCA")
NAME = {"LAD": "LAD", "CX": "LCx", "RCA": "RCA"}


# ---------------------------------------------------------------- geometry

def arc(Y):
    return np.r_[0, np.cumsum(np.linalg.norm(np.diff(Y, axis=0), axis=1))]


def project(Y, s, q):
    """Arc length along the polyline (Y, s) of its point closest to q (on the line pieces, not only the points)."""
    A, AB = Y[:-1], np.diff(Y, axis=0)
    L2 = (AB ** 2).sum(1)
    t = np.clip(((q - A) * AB).sum(1) / np.where(L2 > 0, L2, 1), 0, 1)
    k = int(np.argmin(((A + t[:, None] * AB - q) ** 2).sum(1)))
    return float(s[k] + t[k] * (s[k + 1] - s[k]))


def point_at(Y, s, x):
    return np.array([np.interp(x, s, Y[:, j]) for j in range(3)])


def shared_stretch(Ya, sa, Yb, sb):
    """(lo, hi) in arc length on line a and on line b of the stretch both lines cover: each line's first and
    last point projected onto the other, from the later start to the earlier end."""
    a = (max(sa[0], project(Ya, sa, Yb[0])), min(sa[-1], project(Ya, sa, Yb[-1])))
    b = (max(sb[0], project(Yb, sb, Ya[0])), min(sb[-1], project(Yb, sb, Ya[-1])))
    return a, b


def compare_artery(tr, me, nearest):
    """One artery pair. tr and me are split_trunks.split entries (pm, md, end, rule, Y, s). Returns the artery
    row and the three segment rows (curvature of the tracer and of Medis over the same stretch)."""
    pm, md, end, _, Yt, st = tr
    *_, Ym, sm = me
    (t0, t1), (m0, m1) = shared_stretch(Yt, st, Ym, sm)
    row = {"shared_tracer": t1 - t0, "shared_medis": m1 - m0, "length_tracer": st[-1], "length_medis": sm[-1]}
    if min(t1 - t0, m1 - m0) < MIN_SHARED:
        return row | {"reason": f"shared stretch < {MIN_SHARED:g} mm"}, []
    keep = (st >= t0) & (st <= t1)
    row["offset"] = float(np.median(np.ravel(nearest(Yt[keep], Ym)[0])))
    if row["offset"] > MAX_OFFSET:
        return row | {"reason": f"offset > {MAX_OFFSET:g} mm"}, []
    pt, kt = curvature_profile(Yt, CHORD, st)
    pmed, kmed = curvature_profile(Ym, CHORD, sm)
    row |= {"reason": "ok", "T_tracer": segment_mean(pt, kt, t0, t1), "T_medis": segment_mean(pmed, kmed, m0, m1)}
    segs = []
    for part, (lo, hi) in enumerate(zip((0, pm, md), (pm, md, end))):
        lo, hi = max(lo, t0), min(hi, t1)
        if hi - lo < MIN_SEG:
            segs.append({"part": part, "reason": f"segment shared < {MIN_SEG:g} mm"})
            continue
        a, b = (min(max(project(Ym, sm, point_at(Yt, st, x)), m0), m1) for x in (lo, hi))
        segs.append({"part": part, "reason": "ok", "T_tracer": segment_mean(pt, kt, lo, hi),
                     "T_medis": segment_mean(pmed, kmed, a, b)})
    return row, segs


def daughter_diameter(Y, s, rings, nearest, depths=(DEPTHS[0], DEPTHS[1])):
    """Median area-equivalent diameter of the rings whose centres lie within OFF_ARTERY of the daughter (Y, s)
    and 5 to 10 mm from O, as daughter_ratio.reference_diameter; nan unless the rings reach within COVER_TOL
    of both window ends (contours are discrete, so the window ends are met to this tolerance)."""
    if not rings:
        return np.nan, "no lumen contour"
    c = np.array([r.mean(0) for r in rings])
    d, j = nearest(c, Y)
    on = np.ravel(d) <= OFF_ARTERY
    if not on.any():
        return np.nan, "no contour on the artery"
    sr = s[np.ravel(j)[on]]
    D = np.array([contour_diameter(r) for r, k in zip(rings, on) if k])
    if sr.min() > depths[0] + COVER_TOL or sr.max() < depths[1] - COVER_TOL:
        return np.nan, "contours do not cover 5-10 mm"
    w = (sr >= depths[0]) & (sr <= depths[1])
    if w.sum() < 2:
        return np.nan, "fewer than 2 contours in 5-10 mm"
    return float(np.median(D[w])), "ok"


def asymmetry(arteries, rings_of_artery, nearest):
    """ln(D_LCx / D_LAD) from split arteries and {"LAD": rings, "CX": rings}; (value, reason)."""
    if "LAD" not in arteries or "CX" not in arteries:
        return np.nan, "LAD or LCx missing"
    (*_, Yl, sl), (*_, Yc, sc) = arteries["LAD"], arteries["CX"]
    if not np.allclose(Yl[0], Yc[0]):
        return np.nan, "no shared bifurcation point"
    dl, rl = daughter_diameter(Yl, sl, rings_of_artery.get("LAD", []), nearest)
    dc, rc = daughter_diameter(Yc, sc, rings_of_artery.get("CX", []), nearest)
    if not (np.isfinite(dl) and np.isfinite(dc)):
        return np.nan, f"LAD: {rl}; LCx: {rc}" if rl != "ok" and rc != "ok" else rl if rl != "ok" else rc
    return float(np.log(dc / dl)), "ok"


# ---------------------------------------------------------------- agreement

def agreement(diff, mean, pid, boot=2000, seed=0):
    """Bias, SD, limits of agreement, bootstrap-over-participants 95% intervals and the slope of |diff| on mean."""
    diff, mean, pid = np.asarray(diff, float), np.asarray(mean, float), np.asarray(pid)
    bias, sd = diff.mean(), diff.std(ddof=1)
    out = {"n": len(diff), "people": len(set(pid)), "bias": bias, "sd": sd,
           "loa_lo": bias - 1.96 * sd, "loa_hi": bias + 1.96 * sd,
           "slope": np.polyfit(mean, np.abs(diff), 1)[0] if len(diff) > 2 else np.nan}
    groups = [diff[pid == p] for p in dict.fromkeys(pid)]
    rng = np.random.default_rng(seed)
    stats = []
    for _ in range(boot):
        d = np.concatenate([groups[k] for k in rng.integers(0, len(groups), len(groups))])
        b, s = d.mean(), d.std(ddof=1)
        stats.append((b, b - 1.96 * s, b + 1.96 * s))
    if boot:
        q = np.percentile(np.array(stats), [2.5, 97.5], axis=0)
        out |= {"bias_ci": q[:, 0], "lo_ci": q[:, 1], "hi_ci": q[:, 2]}
    return out


def against_cohort(sd_diff, loa, sd_cohort):
    """Limits of agreement in cohort SDs, and the reliability R = SD_c^2 / (SD_c^2 + SD_err^2) the tracer error
    would give in the plaque-free cohort, SD_err = SD_diff / sqrt(2) (assumes the two methods err about equally)."""
    sd_err = sd_diff / np.sqrt(2)
    return {"loa_in_sd": (loa[0] / sd_cohort, loa[1] / sd_cohort),
            "R": sd_cohort ** 2 / (sd_cohort ** 2 + sd_err ** 2)}


# ---------------------------------------------------------------- data run (server)

def run(limit=None, src=None):
    import centerline_qc as cq
    import hoe10y_qc as hq
    import tracer_io
    from split_check import contour_files
    from split_trunks import ARTERY_OF, NAMES, graph, split

    src = src or tracer_io.TRACER_DIR
    trees = {hq.id_from_name(p.name): p for p in tracer_io.MEDIS_TREES.rglob("*.vtk")}
    hq.read_label_codes((f, f) for f in trees.values())
    have = tracer_io.tracer_ids(src)
    ids = sorted(trees, key=int)[:limit]
    contours = defaultdict(dict)
    for (pid, name), files in contour_files(Path(hq.ROOT) / hq.MEDIS_DIR).items():
        contours[pid][name] = files
    bl = hq.load_sheets(hq.ROOT)["BL"]
    bl = bl.assign(id=bl["study_id"].map(hq.norm_id)).drop_duplicates("id").set_index("id")

    flow, A, S, P = Counter(), [], [], []
    flow["Medis trees"] = len(ids)
    for pid in ids:
        if pid not in have:
            flow["no tracer pair"] += 1
            continue
        flow["with a tracer pair"] += 1
        try:
            med = split(*graph(hq.tree_points(trees[pid])))
        except Exception:  # noqa: BLE001 - counted
            flow["Medis tree not divided"] += 1
            continue
        try:
            trc = split(*graph(tracer_io.tracer_tree(pid, src)))
        except NotImplementedError:
            raise
        except Exception:  # noqa: BLE001 - counted
            flow["tracer tree not divided"] += 1
            continue
        flow["both trees divided"] += 1
        for a in ARTERIES:
            row = {"id": pid, "artery": a}
            if a not in med or a not in trc:
                A.append(row | {"reason": "missing in " + " and ".join(
                    n for n, t in (("Medis", med), ("tracer", trc)) if a not in t)})
                continue
            r, segs = compare_artery(trc[a], med[a], cq.nearest)
            A.append(row | r)
            for g in segs:
                seg = NAMES[a][g["part"]]
                col = f"ct_cag_{seg}_stenosis"
                grade = hq.grade_of(bl.at[pid, col]) if pid in bl.index and col in bl else None
                S.append({"id": pid, "artery": a, "segment": seg, "grade": grade} | g)
        rings = {"LAD": [], "CX": []}
        for name, files in contours.get(pid, {}).items():
            art = ARTERY_OF.get(name, "").upper()
            if art in rings and "lumen" in files:
                cl = cq.read_vtk_legacy(files["centerline"].read_bytes())["points"] if "centerline" in files else None
                rings[art] += [r for r in hq.read_rings(files["lumen"], cl)[0] if len(r) >= 3]
        a_m, why_m = asymmetry(med, rings, cq.nearest)

        def angle(t):
            if "LAD" not in t or "CX" not in t:
                return np.nan
            return lm_angle(t["LAD"][4:], t["CX"][4:])

        P.append({"id": pid, "theta_tracer": angle(trc), "theta_medis": angle(med), "a_medis": a_m,
                  "a_medis_reason": why_m, "a_tracer": np.nan,
                  "a_tracer_reason": "tracer contours not available"})
    return flow, pd.DataFrame(A), pd.DataFrame(S), pd.DataFrame(P)


# ---------------------------------------------------------------- report

def fmt(x, nd=4):
    return "-" if x is None or not np.isfinite(x) else f"{x:.{nd}g}"


def stat_row(label, diff, mean, pid, boot, unit, nd=3):
    from cgps_stats import MIN_CELL, count

    ok = np.isfinite(diff) & np.isfinite(mean)
    if ok.sum() < MIN_CELL:
        return f"| {label} | {count(ok.sum())} | | | | | | |"
    g = agreement(diff[ok], mean[ok], pid[ok], boot)
    ci = (lambda k: f"{fmt(g[k][0], nd)} to {fmt(g[k][1], nd)}") if boot else (lambda k: "-")
    return (f"| {label} | {g['n']} | {fmt(g['bias'], nd)} ({ci('bias_ci')}) | {fmt(g['sd'], nd)} | "
            f"{fmt(g['loa_lo'], nd)} ({ci('lo_ci')}) | {fmt(g['loa_hi'], nd)} ({ci('hi_ci')}) | "
            f"{fmt(g['slope'], 2)} | {unit} |")


def report(flow, A, S, P, boot):
    from cgps_stats import count

    head = ("| | pairs | bias (95% CI) | SD of differences | lower limit (95% CI) | upper limit (95% CI) | "
            "slope of abs. difference on mean | unit |\n|---|---|---|---|---|---|---|---|")
    L = ["# Tracer against Medis: agreement of the geometric features (medis_compare.py)\n",
         f"Baseline. Differences are tracer - Medis. Limits of agreement = bias +- 1.96 SD; 95% intervals from "
         f"{boot} bootstrap samples of participants. Alignment cut {MAX_OFFSET:g} mm, shared stretch at least "
         f"{MIN_SHARED:g} mm. Counts 1-4 shown as <5; statistics only from 5 pairs.\n",
         "## Flow\n", "| step | participants |", "|---|---|"]
    L += [f"| {k} | {count(v)} |" for k, v in flow.items()]
    if len(A):
        L += ["\n### Arteries\n", "| artery | " + " | ".join(sorted(A["reason"].unique())) + " |",
              "|---|" + "---|" * A["reason"].nunique()]
        for a in ARTERIES:
            c = A[A["artery"] == a]["reason"].value_counts()
            L.append(f"| {NAME[a]} | " + " | ".join(str(count(c.get(r, 0))) for r in sorted(A["reason"].unique())) + " |")
        ok = A[A["reason"] == "ok"]
        if len(ok):
            L.append("\nMedian tracer-to-Medis distance over the shared stretch (mm), pairs kept: "
                     + ", ".join(f"{NAME[a]} {fmt(ok[ok['artery'] == a]['offset'].median(), 2)}" for a in ARTERIES))

    L += ["\n## Curvature, whole artery (shared stretch)\n", head]
    if len(A) and "T_tracer" in A:
        for a in ARTERIES + ("all",):
            d = A if a == "all" else A[A["artery"] == a]
            t, m = d["T_tracer"].to_numpy(float), d["T_medis"].to_numpy(float)
            lab = "all arteries" if a == "all" else NAME[a]
            L.append(stat_row(lab, t - m, (t + m) / 2, d["id"].to_numpy(), boot, "1/mm", 3))
            with np.errstate(divide="ignore", invalid="ignore"):
                L.append(stat_row(lab + ", log ratio", np.log(t / m), (np.log(t) + np.log(m)) / 2,
                                  d["id"].to_numpy(), boot, "ln(T_t / T_M)", 3))

    L += ["\n## Curvature, per segment\n", head]
    if len(S) and "T_tracer" in S:
        for seg in [s for a in ARTERIES for s in S[S["artery"] == a]["segment"].unique()]:
            d = S[S["segment"] == seg]
            t, m = d["T_tracer"].to_numpy(float), d["T_medis"].to_numpy(float)
            L.append(stat_row(seg, t - m, (t + m) / 2, d["id"].to_numpy(), boot, "1/mm", 3))
        L += ["\n### Plaque check: segment curvature difference by BL stenosis grade\n", head]
        grp = S["grade"].map(lambda g: g if g in ("none", "minimal") else "mild or worse"
                             if g in ("mild", "moderate", "severe", "occlusion") else "not graded")
        for gname in ("none", "minimal", "mild or worse", "not graded"):
            d = S[grp == gname]
            t, m = d["T_tracer"].to_numpy(float), d["T_medis"].to_numpy(float)
            L.append(stat_row(gname, t - m, (t + m) / 2, d["id"].to_numpy(), boot, "1/mm", 3))

    L += ["\n## Bifurcation angle\n", head]
    if len(P):
        t, m = P["theta_tracer"].to_numpy(float), P["theta_medis"].to_numpy(float)
        L.append(stat_row("LAD-LCx angle", t - m, (t + m) / 2, P["id"].to_numpy(), boot, "degrees", 3))
        L.append(f"\nAngle missing: tracer {count(np.isnan(t).sum())}, Medis {count(np.isnan(m).sum())}.")

        L += ["\n## Daughter asymmetry\n", "| Medis side | participants |", "|---|---|"]
        L += [f"| {k} | {count(v)} |" for k, v in P["a_medis_reason"].value_counts().items()]
        L.append("\nTracer side: " + "; ".join(f"{k} ({count(v)})" for k, v in
                                                P["a_tracer_reason"].value_counts().items()) + ".")
        ok = np.isfinite(P["a_tracer"].to_numpy(float)) & np.isfinite(P["a_medis"].to_numpy(float))
        if ok.any():
            t, m = P["a_tracer"].to_numpy(float), P["a_medis"].to_numpy(float)
            L += [head, stat_row("ln(D_LCx / D_LAD)", t - m, (t + m) / 2, P["id"].to_numpy(), boot, "log ratio", 3)]
            k, n = int((np.sign(t[ok]) != np.sign(m[ok])).sum()), int(ok.sum())
            L.append(f"\nNarrower daughter differs between the methods: {count(k)} of {count(n)}.")
    return "\n".join(L) + "\n"


def plots(A, P, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sets = [("curvature_artery", A.get("T_tracer"), A.get("T_medis"), "average curvature (1/mm)"),
            ("angle", P.get("theta_tracer"), P.get("theta_medis"), "bifurcation angle (degrees)")]
    for name, t, m, lab in sets:
        if t is None:
            continue
        t, m = np.asarray(t, float), np.asarray(m, float)
        ok = np.isfinite(t) & np.isfinite(m)
        if ok.sum() < 3:
            continue
        d, mu = t[ok] - m[ok], (t[ok] + m[ok]) / 2
        b, s = d.mean(), d.std(ddof=1)
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.scatter(mu, d, s=8, alpha=0.5)
        for y, ls in ((b, "-"), (b - 1.96 * s, "--"), (b + 1.96 * s, "--")):
            ax.axhline(y, ls=ls, lw=1, color="k")
        ax.set_xlabel(f"mean of tracer and Medis, {lab}")
        ax.set_ylabel("tracer - Medis")
        fig.tight_layout()
        fig.savefig(out / f"bland_altman_{name}.png", dpi=150)
        plt.close(fig)


# ---------------------------------------------------------------- checks on synthetic shapes (no data)

def _nearest(q, ref):
    d = np.linalg.norm(np.asarray(q)[:, None] - np.asarray(ref)[None], axis=2)
    return d.min(1), d.argmin(1)


def _wavy(x):
    return np.c_[x, 4 * np.sin(2 * np.pi * x / 25), 3 * np.cos(x / 9)]


def check():
    """Known answers."""
    rng = np.random.default_rng(0)
    # shared stretch of two straight lines that overlap from x = 10 to x = 50
    a = np.c_[np.linspace(0, 50, 101), np.zeros(101), np.zeros(101)]
    b = np.c_[np.linspace(10, 70, 121), np.full(121, 0.3), np.zeros(121)]
    (a0, a1), (b0, b1) = shared_stretch(a, arc(a), b, arc(b))
    assert np.allclose((a0, a1, b0, b1), (10, 50, 0, 40)), (a0, a1, b0, b1)
    assert np.isclose(project(a, arc(a), np.array([12.3, 5.0, 0])), 12.3), "projection onto a piece"

    # curvature of one made-up artery, traced twice: identical, rigidly moved, resampled and cut differently
    x = np.linspace(0, 90, 400)
    Y = _wavy(x)
    tr = (30.0, 60.0, arc(Y)[-1], "", Y, arc(Y))
    row, segs = compare_artery(tr, tr, _nearest)
    assert row["reason"] == "ok" and abs(row["T_tracer"] - row["T_medis"]) < 1e-12, "identical lines: no difference"
    assert all(abs(g["T_tracer"] - g["T_medis"]) < 1e-12 for g in segs), "identical lines: no segment difference"
    Q = np.linalg.qr(rng.normal(size=(3, 3)))[0]
    Q *= np.sign(np.linalg.det(Q))
    Ym = _wavy(np.sort(rng.uniform(8, 80, 600)))  # Medis: starts later, ends earlier, uneven points
    row, segs = compare_artery(tr, (0, 0, 0, "", Ym, arc(Ym)), _nearest)
    assert row["reason"] == "ok" and row["offset"] < 0.2, row
    assert abs(row["T_tracer"] / row["T_medis"] - 1) < 0.02, "same artery, other sampling and ends: within 2%"
    print(f"same artery, other ends and sampling: T tracer {row['T_tracer']:.4f}, Medis {row['T_medis']:.4f} 1/mm, "
          f"shared {row['shared_tracer']:.1f} / {row['shared_medis']:.1f} mm")
    Yr = Y @ Q.T + 7.0
    row, _ = compare_artery((30.0, 60.0, arc(Yr)[-1], "", Yr, arc(Yr)), tr, _nearest)
    assert row["reason"].startswith("offset"), "a moved copy is not the same vessel"
    far = Y + [0, 5.0, 0]
    row, _ = compare_artery(tr, (0, 0, 0, "", far, arc(far)), _nearest)
    assert row["reason"].startswith("offset"), "a parallel line 5 mm away is left out"

    # agreement on simulated pairs: bias 0.2, SD 1, three pairs per participant
    pid = np.repeat(np.arange(700), 3)
    d = 0.2 + rng.normal(size=len(pid))
    g = agreement(d, rng.normal(size=len(pid)), pid, boot=300)
    assert abs(g["bias"] - 0.2) < 0.08 and abs(g["sd"] - 1) < 0.05, g
    assert g["bias_ci"][0] < 0.2 < g["bias_ci"][1] and abs(g["slope"]) < 0.1, g
    print(f"simulated bias 0.2, SD 1: bias {g['bias']:.3f} ({g['bias_ci'][0]:.3f} to {g['bias_ci'][1]:.3f}), "
          f"limits {g['loa_lo']:.2f} to {g['loa_hi']:.2f}")
    r = against_cohort(np.sqrt(2), (-2.0, 2.0), 2.0)
    assert np.isclose(r["R"], 0.8) and np.allclose(r["loa_in_sd"], (-1, 1)), r

    # asymmetry, Medis side: tubes of known diameter with rings every 0.5 mm
    def tube(u, D, length=20):
        s = np.arange(0, length + 1e-9, 0.5)
        u = np.asarray(u, float) / np.linalg.norm(u)
        Yt = s[:, None] * u
        e1 = np.cross(u, [0, 0, 1.0])
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(u, e1)
        t = np.linspace(0, 2 * np.pi, 360, endpoint=False)
        rings = [y + D / 2 * (np.cos(t)[:, None] * e1 + np.sin(t)[:, None] * e2) for y in Yt]
        return Yt, s, rings
    (Yl, sl, rl), (Yc, sc, rc) = tube([1, 0.4, 0], 2.75), tube([1, -0.6, 0.2], 2.25)
    arts = {"LAD": (0, 0, 0, "", Yl, sl), "CX": (0, 0, 0, "", Yc, sc)}
    val, why = asymmetry(arts, {"LAD": rl, "CX": rc}, _nearest)
    assert why == "ok" and abs(val - np.log(2.25 / 2.75)) < 1e-3, (val, why)
    val, why = asymmetry(arts, {"LAD": rl[16:], "CX": rc}, _nearest)  # LAD rings start at 8 mm
    assert np.isnan(val) and "cover" in why, why
    print("all checks passed")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="run the synthetic-shape checks")
    ap.add_argument("--limit", type=int, default=None, help="only the first N Medis participants")
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--src", default=None, help="tracer folder (default tracer_io.TRACER_DIR)")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "medis_compare.md"))
    ap.add_argument("--rows", default=None, help="folder for the per-pair CSVs and plots (server only)")
    args = ap.parse_args()
    if args.check:
        check()
        return
    from cgps_stats import OUT_DIR

    flow, A, S, P = run(args.limit, args.src)
    rows = Path(args.rows or Path(OUT_DIR) / "medis_compare")
    rows.mkdir(parents=True, exist_ok=True)
    for name, df in (("arteries", A), ("segments", S), ("participants", P)):
        df.to_csv(rows / f"medis_compare_{name}.csv", index=False)
    plots(A, P, rows)
    text = report(flow, A, S, P, args.boot)
    Path(args.out).write_text(text, encoding="utf-8")
    print(text)
    print(f"written to {args.out}; per-pair rows and plots (with ids, keep on the server) in {rows}")


if __name__ == "__main__":
    main()
