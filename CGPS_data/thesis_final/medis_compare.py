"""Agreement of the geometric features between the in-house tracer and Medis (sec:method-medis-agreement).

    python CGPS_data/thesis_final/medis_compare.py [--limit N] [--boot 2000] [--out MD] [--rows DIR]
    python CGPS_data/thesis_final/medis_compare.py --check   # synthetic shapes, needs no data

Baseline only. Each Medis participant's tracer tree (tracer_io.tracer_tree) and Medis tree
(hoe10y_qc.tree_points) are divided with split_trunks.split, and the LAD, LCx and RCA are paired by name.
The tracer tree starts at the tracer's own ostia (tracer_io.tracer_ostia, passed as roots); the Medis tree
starts at its LM label.
Both are in LPS mm (tracer_probe.md), so no mapping is applied.

Curvature, per artery pair, in this order:
  shared stretch  each centerline's first and last point is projected onto the other at the closest point;
                  the stretch runs from the later start to the earlier end (shared_stretch). Pairs with a
                  shared stretch under MIN_SHARED mm are left out.
  alignment       each line's shared stretch is resampled every DENSE mm (stretch); the distances run from the
                  points of each to the other, and the larger of the two 90th percentiles is the offset. Pairs
                  above MAX_OFFSET mm are left out (a wrong vessel or a failed trace). MAX_OFFSET was fixed on
                  2026-11-18 before any feature difference was looked at. Until the code review of 2026-11-18
                  the rule used the median, one way (tracer to Medis): a branch could then take up nearly half
                  the stretch and still pass. The median (tracer to Medis) stays as the column offset_median.
                  Code review 2026-11-19, after the 2026-11-18 results were seen and for the code's reasons,
                  not the numbers: both ends of the distances are the shared stretches resampled by arc length.
                  Before, the query was the raw points (unevenly spaced Medis points weighted the percentile by
                  sampling density) and the reference the whole other line (an end could match a loop outside
                  the overlap, so mismatched stretches passed).
  averaged part   the shared stretch without CHORD mm at each end, on both lines: a profile has no points
                  within CHORD of its own line's ends, so without this the line that ends first would lose
                  up to CHORD mm at an end that the other keeps (code review 2026-11-18). Pairs whose averaged
                  part is under MIN_SHARED mm are left out, with this reason ahead of the offset (2026-11-19:
                  before, offset failures skipped the length rule and entered the sensitivity row with
                  averages over a few mm).
  curvature       the Menger profile (curvature_feature.curvature_profile) on each full artery, averaged over
                  the averaged part (segment_mean). T is also computed for pairs that fail only the alignment
                  check, for the sensitivity row "including offset failures", which so meets the same length
                  rules as the main row. aligned_artery = passed the alignment check (whatever the averaged
                  part); False when the shared stretch is too short for the check.
Angle, per participant: bifurcation_angle.angle_with_reason (the rule of the cohort feature) on each tree's
own LAD and LCx (full trees), compared only where the LAD and the LCx both passed the alignment check
(aligned_artery, so not the averaged-part length, which concerns curvature only; decided 2026-11-18, as for
curvature: a failed pair is probably a different vessel) and both pass near_o: the 90th percentile of the
distances from each tree's first DEPTHS[-1] mm of the daughter from its own O to the other tree's left main
(split_trunks.left_main) and whole daughter, the larger of the two directions, at most MAX_OFFSET (added
2026-11-19, code review: the whole-artery stretch starts at the later O and can miss the 5-10 mm the angle
uses). The left main is in the reference so that an O placed further along the same vessel in one tree does
not fail the check: the first version (also 2026-11-19, never run on the data) took the other daughter's
first 15 mm only, and so cut on the O distance once it exceeded about 3 mm. near_o runs only where the
whole-artery check passed. o_dist, the distance between the
tracer's and Medis' bifurcation point O, is saved and reported, not used as a cut (code review 2026-11-18: a
cut chosen after the angle results were seen would be tuned on them). An angle is missing for a tree without
an LM label (bifurcation_angle.has_lm, 2026-11-18). The CSV keeps every angle with the columns aligned_whole,
aligned and the reasons.
Daughter asymmetry, per participant (2026-11-19, rule fixed before any result): only where the angle is
compared (aligned). Each tree's own lumen surface is cut across its own LAD and LCx at SECTION_DEPTHS (5 to
10 mm from its own O, every 0.5 mm; daughter_ratio.surface_diameters): the tracer's
lumen_surface_ostium_pruned.vtk (tracer_io.tracer_lumen, the same centerlines as TRACER_DIR, lumen_probe.md)
and the participant's BL Medis lumen meshes of the left tree, merged. A daughter's D is the median of its
cuts, kept only when every cut has a diameter (strict rule: the Medis lumen ends where Medis stopped
contouring). a = ln(D_LCx / D_LAD); reported as the signed a and as D_LAD and D_LCx. Medis contoured almost
only diseased segments, so every participant compared has plaque at the bifurcation.
A pair or participant whose computation raises is kept with the reason error:<type> (2026-11-19).

Reliability per feature (2026-11-19), on the same pairs: SD of each method, SD of the differences and the
ICC of the two methods, consistency ICC(C,1) and absolute agreement ICC(A,1) (McGraw and Wong 1996), with
bootstrap intervals over participants; for the asymmetry also abs(a), the model feature. It sets the
measurement error against the spread between people, which is what weakens a per-SD hazard ratio.
Agreement per feature: difference tracer - Medis in the feature's own unit, bias, SD of the differences,
95% limits of agreement (bias +- 1.96 SD) and 95% intervals from a bootstrap over participants. Curvature
is compared as a plain difference only (fixed 2026-11-18, before the results).
The share of pairs left out, and why, is reported next to the limits: the limits describe only the traces
that passed, while the plaque-free cohort uses every trace.

Writes medis_compare.md next to this script (aggregates only: counts 1-4 hidden, statistics only from
MIN_CELL pairs) and, in --rows (server only, contains study ids), the per-pair CSVs and Bland-Altman plots.
"""
import argparse
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bifurcation_angle import DEPTHS, angle_with_reason
from curvature_feature import CHORD, curvature_profile, segment_mean
from daughter_ratio import SECTION_DEPTHS, merge, surface, surface_diameters

MAX_OFFSET = 2.0  # mm: 90th percentile of the point distances, both ways, above this = not the same vessel
MIN_SHARED = 10.0  # mm: minimum shared stretch, and minimum averaged part (shared stretch less CHORD at each end)
DENSE = 0.25  # mm: the other centerline is resampled this finely for the distances
O_FAR = 5.0  # mm: o_dist above this is counted in the report (not a cut)
ARTERIES = ("LAD", "CX", "RCA")
RIGHT = {"prca", "mrca", "drca", "rca", "pda", "pla"}  # Medis lumen sets of the right tree, not read for the asymmetry
NAME = {"LAD": "LAD", "CX": "LCx", "RCA": "RCA"}


# ---------------------------------------------------------------- geometry

def arc(Y):
    return np.r_[0, np.cumsum(np.linalg.norm(np.diff(Y, axis=0), axis=1))]


def stretch(Y, s, lo, hi, step=DENSE):
    """The part of the polyline (Y, s) from arc length lo to hi, resampled linearly every step mm (ends kept)."""
    q = np.r_[np.arange(lo, hi, step), hi]
    return np.column_stack([np.interp(q, s, Y[:, k]) for k in range(Y.shape[1])])


def p90(A, B, nearest):
    """(90th percentile, median) of the distances from each point of A to the nearest point of B (resampled lines)."""
    d = np.ravel(nearest(A, B)[0])
    return float(np.percentile(d, 90)), float(np.median(d))


def project(Y, s, q):
    """Arc length along the polyline (Y, s) of its point closest to q (on the line pieces, not only the points)."""
    A, AB = Y[:-1], np.diff(Y, axis=0)
    L2 = (AB ** 2).sum(1)
    t = np.clip(((q - A) * AB).sum(1) / np.where(L2 > 0, L2, 1), 0, 1)
    k = int(np.argmin(((A + t[:, None] * AB - q) ** 2).sum(1)))
    return float(s[k] + t[k] * (s[k + 1] - s[k]))


def shared_stretch(Ya, sa, Yb, sb):
    """(lo, hi) in arc length on line a and on line b of the stretch both lines cover: each line's first and
    last point projected onto the other, from the later start to the earlier end."""
    a = (max(sa[0], project(Ya, sa, Yb[0])), min(sa[-1], project(Ya, sa, Yb[-1])))
    b = (max(sb[0], project(Yb, sb, Ya[0])), min(sb[-1], project(Yb, sb, Ya[-1])))
    return a, b


def compare_artery(Yt, st, Ym, sm, nearest):
    """Average curvature of one artery from the tracer (Yt, st) and from Medis (Ym, sm) over their shared stretch."""
    (t0, t1), (m0, m1) = shared_stretch(Yt, st, Ym, sm)
    row = {"shared_tracer": t1 - t0, "shared_medis": m1 - m0}
    if min(t1 - t0, m1 - m0) < MIN_SHARED:
        return row | {"reason": f"shared stretch < {MIN_SHARED:g} mm", "aligned_artery": False}
    A, B = stretch(Yt, st, t0, t1), stretch(Ym, sm, m0, m1)
    (p_t, med_t), (p_m, _) = p90(A, B, nearest), p90(B, A, nearest)
    off = max(p_t, p_m)
    row |= {"offset": off, "offset_median": med_t, "aligned_artery": off <= MAX_OFFSET}
    if min(t1 - t0, m1 - m0) - 2 * CHORD < MIN_SHARED:
        return row | {"reason": f"averaged part < {MIN_SHARED:g} mm"}
    reason = "ok" if off <= MAX_OFFSET else f"offset > {MAX_OFFSET:g} mm"
    return row | {"reason": reason, "T_tracer": segment_mean(*curvature_profile(Yt, CHORD, st), t0 + CHORD, t1 - CHORD),
                  "T_medis": segment_mean(*curvature_profile(Ym, CHORD, sm), m0 + CHORD, m1 - CHORD)}


def near_o(Yt, st, Ym, sm, lm_t, lm_m, nearest, depth=DEPTHS[-1]):
    """Alignment of one daughter at the bifurcation: the larger 90th percentile of the distances from each
    tree's first depth mm from its own O to the other tree's left main (lm_t, lm_m: ostium to O) and whole
    daughter. The left main is in the reference so that O placed further along the same vessel in one tree
    does not fail the check (the two O are not compared, o_dist is reported only); nan when either daughter
    is shorter than depth."""
    if min(st[-1] - st[0], sm[-1] - sm[0]) < depth:
        return np.nan
    whole = lambda Y: stretch(Y, arc(Y), 0, arc(Y)[-1]) if len(Y) > 1 else Y  # noqa: E731
    ref_t, ref_m = np.r_[whole(lm_t), whole(Yt)], np.r_[whole(lm_m), whole(Ym)]
    return max(p90(stretch(Yt, st, st[0], st[0] + depth), ref_m, nearest)[0],
               p90(stretch(Ym, sm, sm[0], sm[0] + depth), ref_t, nearest)[0])


def guarded(fn, *args):
    """(fn(*args), None), or (None, "error:<type>") when it raises: counted in the report, not a stopped run."""
    try:
        return fn(*args), None
    except Exception as ex:  # noqa: BLE001 - counted
        return None, f"error:{type(ex).__name__}"


def asymmetry_pair(trc, med, trc_surf, med_surf):
    """Lumen diameters at the SECTION_DEPTHS of each tree's own LAD and LCx (daughter_ratio.surface_diameters on
    its own surface) and the asymmetry ln(D_LCx / D_LAD), with the reason. Strict rule (2026-11-19, before any
    result): a daughter's D is the median over all its cuts, and only when every cut has a diameter."""
    row, short = {}, []
    for name, arts, surf in (("medis", med, med_surf), ("tracer", trc, trc_surf)):
        (*_, Yl, sl), (*_, Yc, sc) = arts["LAD"], arts["CX"]
        for a, D in (("LAD", surface_diameters(*surf, Yl, sl, Yc)), ("CX", surface_diameters(*surf, Yc, sc, Yl))):
            row[f"n_cut_{a}_{name}"] = int(np.isfinite(D).sum())
            row[f"D_{a}_{name}"] = float(np.median(D)) if np.isfinite(D).all() else np.nan
            short += [name] if not np.isfinite(D).all() else []
        row[f"asym_{name}"] = float(np.log(row[f"D_CX_{name}"] / row[f"D_LAD_{name}"]))
    reason = ("Medis lumen does not cover 5-10 mm of both daughters" if "medis" in short
              else "tracer cut missing" if "tracer" in short else "ok")
    return row | {"asym_reason": reason}


# ---------------------------------------------------------------- agreement

def agreement(diff, pid, boot=2000, seed=0):
    """Bias, SD, limits of agreement and their 95% intervals from a bootstrap over participants."""
    diff, pid = np.asarray(diff, float), np.asarray(pid)
    bias, sd = diff.mean(), diff.std(ddof=1)
    out = {"n": len(diff), "bias": bias, "sd": sd, "loa_lo": bias - 1.96 * sd, "loa_hi": bias + 1.96 * sd}
    groups = [g.to_numpy() for _, g in pd.Series(diff).groupby(pid, sort=False)]
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


def icc(x, y):
    """(consistency, absolute agreement) ICC of two methods measuring the same n subjects: ICC(C,1) and ICC(A,1)
    of McGraw and Wong 1996, from the two-way ANOVA mean squares (rows = pairs, columns = tracer, Medis)."""
    X = np.c_[x, y]
    n, k = X.shape
    g, r, c = X.mean(), X.mean(axis=1), X.mean(axis=0)
    msr = k * ((r - g) ** 2).sum() / (n - 1)
    msc = n * ((c - g) ** 2).sum() / (k - 1)
    mse = ((X - r[:, None] - c[None] + g) ** 2).sum() / ((n - 1) * (k - 1))
    return (msr - mse) / (msr + (k - 1) * mse), (msr - mse) / (msr + (k - 1) * mse + k * (msc - mse) / n)


def reliability(x, y, pid, boot=2000, seed=0):
    """SD of each method, SD of the differences and both ICCs, with 95% intervals from a bootstrap over
    participants (all pairs of a participant together, as in agreement)."""
    x, y, pid = np.asarray(x, float), np.asarray(y, float), np.asarray(pid)
    out = {"n": len(x), "sd_t": x.std(ddof=1), "sd_m": y.std(ddof=1), "sd_d": (x - y).std(ddof=1)}
    out["icc_c"], out["icc_a"] = icc(x, y)
    idx = [g.to_numpy() for _, g in pd.Series(np.arange(len(x))).groupby(pid, sort=False)]
    rng = np.random.default_rng(seed)
    stats = []
    for _ in range(boot):
        k = np.concatenate([idx[j] for j in rng.integers(0, len(idx), len(idx))])
        stats.append(icc(x[k], y[k]))
    if boot:
        q = np.percentile(np.array(stats), [2.5, 97.5], axis=0)
        out |= {"icc_c_ci": q[:, 0], "icc_a_ci": q[:, 1]}
    return out


# ---------------------------------------------------------------- data run (server)

def run(limit=None, src=None, lumen=None, medis=None):
    import centerline_qc as cq
    import hoe10y_qc as hq
    import tracer_io
    from split_trunks import graph, left_main, split

    from split_check import contour_files

    src, lumen = src or tracer_io.TRACER_DIR, lumen or tracer_io.LUMEN_DIR
    med_lumen = {}  # id -> the participant's BL Medis lumen files of the left tree
    for (i, seg), fs in contour_files(medis or Path(hq.ROOT) / hq.MEDIS_DIR).items():
        if "lumen" in fs and seg not in RIGHT:
            med_lumen.setdefault(i, []).append(fs["lumen"])
    trees = {hq.id_from_name(p.name): p for p in tracer_io.MEDIS_TREES.rglob("*.vtk")}
    hq.read_label_codes((f, f) for f in trees.values())
    have = tracer_io.tracer_ids(src)
    ids = sorted(trees, key=int)[:limit]

    flow, A, P = Counter(), [], []
    flow["Medis trees"] = len(ids)
    for pid in ids:
        if pid not in have:
            flow["no tracer pair"] += 1
            continue
        flow["with a tracer pair"] += 1
        try:
            med_tree, trc_tree = hq.tree_points(trees[pid]), tracer_io.tracer_tree(pid, src)
            roots, med_g, trc_g = tracer_io.tracer_ostia(pid, src), graph(med_tree), graph(trc_tree)
            med, trc = split(*med_g), split(*trc_g, roots=roots)
        except Exception:  # noqa: BLE001 - counted
            flow["tree not divided"] += 1
            continue
        flow["both trees divided"] += 1
        ok = set()
        for a in ARTERIES:
            if a not in med or a not in trc:
                missing = " and ".join(n for n, t in (("Medis", med), ("tracer", trc)) if a not in t)
                A.append({"id": pid, "artery": a, "reason": f"missing in {missing}"})
                continue
            res, err = guarded(compare_artery, *trc[a][4:], *med[a][4:], cq.nearest)
            A.append({"id": pid, "artery": a} | (res or {"reason": err, "aligned_artery": False}))
            ok |= {a} if A[-1]["aligned_artery"] else set()
        row = {"id": pid, "aligned_whole": {"LAD", "CX"} <= ok}
        for name, tree, arts in (("tracer", trc_tree, trc), ("medis", med_tree, med)):
            res, err = guarded(angle_with_reason, tree, arts)
            row[f"theta_{name}"], row[f"reason_{name}"] = res or (np.nan, err)
        if row["aligned_whole"]:  # near_o can change "aligned" only then
            lms, err = guarded(lambda: (left_main(*trc_g, roots), left_main(*med_g)))
            for a in ("LAD", "CX"):
                res, err = (None, err) if err else guarded(near_o, *trc[a][4:], *med[a][4:], *lms, cq.nearest)
                row[f"near_o_{a}"], row[f"near_o_reason_{a}"] = (np.nan, err) if err else (res, "ok")
        row["o_dist"] = float(np.linalg.norm(trc["LAD"][4][0] - med["LAD"][4][0])) if "LAD" in trc and "LAD" in med else np.nan
        row["aligned"] = row["aligned_whole"] and all(row[f"near_o_{a}"] <= MAX_OFFSET for a in ("LAD", "CX"))
        if not row["aligned"]:
            row["asym_reason"] = "not aligned"
        elif pid not in med_lumen:
            row["asym_reason"] = "no Medis lumen in the left tree"
        else:
            res, err = guarded(lambda: asymmetry_pair(trc, med, surface(tracer_io.tracer_lumen(pid, lumen)),
                                                      merge([surface(f) for f in med_lumen[pid]])))
            row |= res or {"asym_reason": err}
        P.append(row)
    return flow, pd.DataFrame(A), pd.DataFrame(P)


# ---------------------------------------------------------------- report

def fmt(x, nd=3):
    return "-" if x is None or not np.isfinite(x) else f"{x:.{nd}g}"


def stat_row(label, diff, pid, boot, unit):
    from cgps_stats import MIN_CELL, count

    ok = np.isfinite(diff)
    if ok.sum() < MIN_CELL:
        return f"| {label} | {count(ok.sum())} | | | | | |"
    g = agreement(diff[ok], pid[ok], boot)
    ci = (lambda k: f" ({fmt(g[k][0])} to {fmt(g[k][1])})") if boot else (lambda _: "")
    return (f"| {label} | {g['n']} | {fmt(g['bias'])}{ci('bias_ci')} | {fmt(g['sd'])} | "
            f"{fmt(g['loa_lo'])}{ci('lo_ci')} | {fmt(g['loa_hi'])}{ci('hi_ci')} | {unit} |")


def report(flow, A, P, boot):
    from cgps_stats import MIN_CELL, QUARTILE_MIN, TAIL_MIN, count

    def med(x):
        x = np.asarray(x, float)
        x = x[np.isfinite(x)]
        return np.median(x) if len(x) >= QUARTILE_MIN else None

    head = ("| | pairs | bias (95% CI) | SD of differences | lower limit (95% CI) | upper limit (95% CI) | unit |\n"
            "|---|---|---|---|---|---|---|")
    L = ["# Tracer against Medis: agreement of the geometric features (medis_compare.py)\n",
         (f"Baseline. Differences are tracer - Medis. Limits of agreement = bias +- 1.96 SD; 95% intervals from "
          f"{boot} bootstrap samples of participants. Alignment cut: 90th percentile of the distances, both ways, "
          f"at most {MAX_OFFSET:g} mm. Curvature averaged over the shared stretch less {CHORD:g} mm at each end, "
          f"at least {MIN_SHARED:g} mm. Counts 1-4 shown as <5; statistics only from 5 pairs.\n"),
         "## Flow\n", "| step | participants |", "|---|---|"]
    L += [f"| {k} | {count(v)} |" for k, v in flow.items()]

    if len(A):
        reasons = sorted(A["reason"].unique())
        L += ["\nPer artery, pairs by reason (share of the artery's pairs). The limits below describe only the "
              "pairs kept.\n", "| artery | " + " | ".join(reasons) + " |", "|---|" + "---|" * len(reasons)]
        for a in ARTERIES:
            c = A[A["artery"] == a]["reason"].value_counts()
            L.append(f"| {NAME[a]} | " + " | ".join(f"{count(c.get(r, 0))} ({100 * c.get(r, 0) / c.sum():.0f}%)"
                                                    for r in reasons) + " |")
        if "offset" in A:
            ok = A[A["reason"] == "ok"]
            L.append(f"\nPairs kept, alignment distance (mm), median over pairs of the per-pair median (tracer to "
                     f"Medis) / of the per-pair 90th percentile (both ways), from {QUARTILE_MIN} pairs: "
                     + ", ".join(f"{NAME[a]} {fmt(med(ok[ok['artery'] == a]['offset_median']), 2)} / "
                                 f"{fmt(med(ok[ok['artery'] == a]['offset']), 2)}" for a in ARTERIES))
        short = A[A["reason"].str.startswith("shared stretch")]
        if len(short):
            lo, hi = short[["shared_tracer", "shared_medis"]].min(1), short[["shared_tracer", "shared_medis"]].max(1)
            L.append(f"\nShort shared stretch: {count(len(short))} pairs, of which {count(int((hi > 2 * lo).sum()))} "
                     f"have a tracer and a Medis length that differ more than twofold (an end projected onto "
                     f"another turn of the artery), per artery: "
                     + ", ".join(f"{NAME[a]} {count(int(((hi > 2 * lo) & (short['artery'] == a)).sum()))}"
                                 for a in ARTERIES))

    L += [f"\n## Curvature (average over the shared stretch less {CHORD:g} mm at each end)\n", head]
    if len(A) and "T_tracer" in A:
        kept = A[A["reason"] == "ok"]
        for a in ARTERIES + ("all",):
            d = kept if a == "all" else kept[kept["artery"] == a]
            diff = d["T_tracer"].to_numpy(float) - d["T_medis"].to_numpy(float)
            L.append(stat_row("all arteries" if a == "all" else NAME[a], diff, d["id"].to_numpy(), boot, "1/mm"))
        d = A[A["reason"].eq("ok") | A["reason"].str.startswith("offset")]
        L.append(stat_row("all arteries, including offset failures (sensitivity)",
                          d["T_tracer"].to_numpy(float) - d["T_medis"].to_numpy(float), d["id"].to_numpy(), boot, "1/mm"))

    L += ["\n## Bifurcation angle\n", head]
    if len(P):
        Q = P[P["aligned"]]
        t, m = Q["theta_tracer"].to_numpy(float), Q["theta_medis"].to_numpy(float)
        L.append(stat_row("LAD-LCx angle", t - m, Q["id"].to_numpy(), boot, "degrees"))
        both = np.isfinite(t) & np.isfinite(m)
        W = P[P["aligned_whole"]]
        L.append(f"\nFlow: both trees divided {count(len(P))}; LAD and LCx both passed the alignment check on the "
                 f"whole artery {count(len(W))} ({100 * len(W) / len(P):.0f}%); and within the first "
                 f"{DEPTHS[-1]:g} mm from O (near_o) {count(len(Q))} ({100 * len(Q) / len(P):.0f}%); angle in both "
                 f"{count(int(both.sum()))} ({100 * both.sum() / len(P):.0f}%). near_o not computed (error) for "
                 f"{count(int(W.filter(like='near_o_reason').ne('ok').any(axis=1).sum()))} of the whole-artery "
                 f"aligned. Among the aligned, angle missing:")
        L += ["\n| reason | tracer | Medis |", "|---|---|---|"]
        for r in sorted(set(Q["reason_tracer"]) | set(Q["reason_medis"])):
            if r != "ok":
                L.append(f"| {r} | {count((Q['reason_tracer'] == r).sum())} | {count((Q['reason_medis'] == r).sum())} |")
        if "o_dist" in Q:
            o, d = Q["o_dist"].to_numpy(float)[both], np.abs(t - m)[both]
            if len(o) >= MIN_CELL:
                p90 = np.percentile(o, 90) if len(o) >= TAIL_MIN else None
                L.append(f"\nDistance between the tracer's and Medis' bifurcation point O, angles compared "
                         f"(reported only, not a cut): median {fmt(med(o), 2)} mm, 90th percentile {fmt(p90, 2)} mm, "
                         f"{count(int((o > O_FAR).sum()))} ({100 * (o > O_FAR).mean():.0f}%) above {O_FAR:g} mm.")
                top = d >= np.percentile(d, 90)
                if top.sum() >= QUARTILE_MIN:
                    L.append(f"Median O distance among the 10% largest |angle differences| {fmt(med(o[top]), 2)} mm, "
                             f"among the rest {fmt(med(o[~top]), 2)} mm.")

    L += ["\n## Daughter asymmetry ln(D_LCx / D_LAD)\n", head]
    if len(P) and "asym_reason" in P:
        Q = P[P["asym_reason"] == "ok"]
        for col, label, unit in (("asym", "asymmetry", "ln ratio"), ("D_LAD", "LAD diameter", "mm"),
                                 ("D_CX", "LCx diameter", "mm")):
            if f"{col}_tracer" in Q:
                diff = Q[f"{col}_tracer"].to_numpy(float) - Q[f"{col}_medis"].to_numpy(float)
                L.append(stat_row(label, diff, Q["id"].to_numpy(), boot, unit))
        L.append(f"\nDiameters from plane cuts of each tree's own lumen surface at {len(SECTION_DEPTHS)} depths, "
                 f"{SECTION_DEPTHS[0]:g} to {SECTION_DEPTHS[-1]:g} mm from its own O (daughter_ratio.surface_diameters); "
                 f"a daughter counts only when every cut has a diameter. Participants by reason:")
        L += ["\n| reason | participants |", "|---|---|"]
        L += [f"| {r} | {count(n)} |" for r, n in P["asym_reason"].value_counts().items()]
        L.append("\nMedis lumen exists only where Medis contoured, almost always diseased segments: every participant "
                 "compared here has plaque at the bifurcation, unlike the plaque-free cohort.")

    L += ["\n## Reliability: measurement error against the spread between people\n",
          ("Same pairs as the agreement rows above. ICC(C,1) (consistency) ignores a constant bias, which does not "
           "change a per-SD hazard ratio; ICC(A,1) (absolute agreement) also counts the bias (McGraw and Wong 1996). "
           "With no ground truth, Medis is a second error-prone measurement, not the truth; the ICC is the share of "
           "the variance between pairs that the two methods agree on.\n"),
          "| | pairs | SD tracer | SD Medis | SD of differences | ICC(C,1) (95% CI) | ICC(A,1) (95% CI) | unit |",
          "|---|---|---|---|---|---|---|---|"]
    sets = []
    if len(A) and "T_tracer" in A:
        kept = A[A["reason"] == "ok"]
        sets += [(f"curvature, {NAME[a]}", kept[kept["artery"] == a], "T", "1/mm") for a in ARTERIES]
        sets.append(("curvature, all arteries", kept, "T", "1/mm"))
    if len(P):
        sets.append(("LAD-LCx angle", P[P["aligned"]], "theta", "degrees"))
    if len(P) and "asym_reason" in P:
        Q = P[P["asym_reason"] == "ok"]
        Q = Q.assign(absasym_tracer=Q["asym_tracer"].abs(), absasym_medis=Q["asym_medis"].abs())
        sets += [("asymmetry a", Q, "asym", "ln ratio"), ("abs(a), the model feature", Q, "absasym", "ln ratio"),
                 ("LAD diameter", Q, "D_LAD", "mm"), ("LCx diameter", Q, "D_CX", "mm")]
    for label, d, col, unit in sets:
        x, y = d[f"{col}_tracer"].to_numpy(float), d[f"{col}_medis"].to_numpy(float)
        ok = np.isfinite(x) & np.isfinite(y)
        if ok.sum() < MIN_CELL:
            L.append(f"| {label} | {count(ok.sum())} | | | | | | {unit} |")
            continue
        g = reliability(x[ok], y[ok], d["id"].to_numpy()[ok], boot)
        ci = (lambda k: f" ({fmt(g[k][0], 2)} to {fmt(g[k][1], 2)})") if boot else (lambda _: "")
        L.append(f"| {label} | {g['n']} | {fmt(g['sd_t'])} | {fmt(g['sd_m'])} | {fmt(g['sd_d'])} | "
                 f"{fmt(g['icc_c'], 2)}{ci('icc_c_ci')} | {fmt(g['icc_a'], 2)}{ci('icc_a_ci')} | {unit} |")
    return "\n".join(L) + "\n"


def plots(A, P, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sets = [("curvature", A.get("T_tracer"), A.get("T_medis"), "average curvature (1/mm)"),
            ("angle", P.get("theta_tracer"), P.get("theta_medis"), "bifurcation angle (degrees)"),
            ("asymmetry", P.get("asym_tracer"), P.get("asym_medis"), "asymmetry ln(D_LCx / D_LAD)")]
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

    # curvature of one made-up artery, traced twice
    Y = _wavy(np.linspace(0, 90, 400))
    row = compare_artery(Y, arc(Y), Y, arc(Y), _nearest)
    assert row["reason"] == "ok" and abs(row["T_tracer"] - row["T_medis"]) < 1e-12, "identical lines: no difference"
    Ym = _wavy(np.sort(rng.uniform(8, 80, 600)))  # Medis: starts later, ends earlier, uneven points
    row = compare_artery(Y, arc(Y), Ym, arc(Ym), _nearest)
    assert row["reason"] == "ok" and row["offset"] < 0.2, row
    assert abs(row["T_tracer"] / row["T_medis"] - 1) < 0.02, "same artery, other sampling and ends: within 2%"
    print(f"same artery, other ends and sampling: T tracer {row['T_tracer']:.4f}, Medis {row['T_medis']:.4f} 1/mm, "
          f"shared {row['shared_tracer']:.1f} / {row['shared_medis']:.1f} mm")
    Yr = Y + [0, 0, 3.0]
    assert compare_artery(Yr, arc(Yr), Y, arc(Y), _nearest)["reason"].startswith("offset"), "3 mm moved copy left out"
    short = Y[arc(Y) <= 15]
    row = compare_artery(short, arc(short), Y, arc(Y), _nearest)
    assert row["aligned_artery"] and row["reason"].startswith("averaged part"), row
    far = Y + [0, 5.0, 0]
    assert compare_artery(Y, arc(Y), far, arc(far), _nearest)["reason"].startswith("offset"), "5 mm away left out"
    s = arc(Y)
    branch = Y + np.c_[np.zeros(len(Y)), np.zeros(len(Y)), np.clip(s - 0.6 * s[-1], 0, None)]  # leaves after 60%
    row = compare_artery(branch, arc(branch), Y, s, _nearest)
    assert row["offset_median"] < MAX_OFFSET and row["reason"].startswith("offset"), row
    print(f"branch leaving over the last 40%: median {row['offset_median']:.2f} mm (passed the old rule), "
          f"90th percentile {row['offset']:.1f} mm -> left out")

    # an offset failure with a short averaged part is left out for its length and gets no T (2026-11-19)
    row = compare_artery(short + [0, 0, 3.0], arc(short), Y, arc(Y), _nearest)
    assert row["reason"].startswith("averaged part") and not row["aligned_artery"] and "T_tracer" not in row, row
    # the offset does not depend on how unevenly Medis is sampled
    x = np.r_[np.linspace(0, 54, 1500), np.linspace(54.5, 90, 8)]  # dense first 60%, 8 points over the rest
    Ye, Yu = _wavy(np.linspace(0, 90, 300)) + [0, 1.0, 0], _wavy(x) + [0, 1.0, 0]
    oe, ou = (compare_artery(Y, s, Z, arc(Z), _nearest)["offset"] for Z in (Ye, Yu))
    assert abs(oe - ou) < 0.15, (oe, ou)
    # a tracer end that turns back along the line: the end projects onto Medis 25 mm early (finding 6)
    m = np.c_[np.linspace(0, 50, 101), np.zeros(101), np.zeros(101)]
    back = np.c_[np.linspace(49.5, 25, 50), np.full(50, 1.5), np.zeros(50)]
    t = np.r_[m, [[50.5, 0.4, 0], [50.8, 0.75, 0], [50.5, 1.1, 0]], back]
    row = compare_artery(t, arc(t), m, arc(m), _nearest)
    assert row["reason"].startswith("offset"), row
    print(f"tracer turning back 1.5 mm beside its own artery: shared {row['shared_tracer']:.0f} / "
          f"{row['shared_medis']:.0f} mm, offset {row['offset']:.1f} mm -> left out")
    # near O: left main along x up to O, daughter on along x
    line = lambda a, b: np.c_[np.linspace(a, b, int(2 * (b - a)) + 1), np.zeros(int(2 * (b - a)) + 1), np.zeros(int(2 * (b - a)) + 1)]  # noqa: E731
    lm_t, lad_t = line(-8, 0), line(0, 30)
    assert near_o(lad_t, arc(lad_t), lad_t, arc(lad_t), lm_t, lm_t, _nearest) < 1e-9, "same daughter"
    lm_m, lad_m = line(-8, -4), line(-4, 30)  # Medis O 4 mm further up the same vessel: passes (o_dist is no cut)
    assert near_o(lad_t, arc(lad_t), lad_m, arc(lad_m), lm_t, lm_m, _nearest) < 0.2, "O shifted along the vessel"
    d = np.linspace(0, 30, 61)
    other = np.c_[d * np.cos(0.8), d * np.sin(0.8), 0 * d]  # the tracer daughter enters a vessel 46 deg off
    assert near_o(other, arc(other), lad_t, arc(lad_t), lm_t, lm_t, _nearest) > MAX_OFFSET, "other vessel"
    assert np.isnan(near_o(lad_t[:10], arc(lad_t[:10]), lad_t, arc(lad_t), lm_t, lm_t, _nearest)), "under 10 mm"
    # a raising computation is counted, not a stopped run
    assert guarded(compare_artery, Y[:1], arc(Y[:1]), Y, arc(Y), _nearest)[1].startswith("error:")
    assert guarded(near_o, lad_t, arc(lad_t), lad_t, arc(lad_t), lm_t, np.zeros((2, 2)), _nearest)[1].startswith("error:")

    # ICC on simulated pairs: true SD 1, error SD 0.5 in each method, tracer shifted by 0.3
    truth = rng.normal(size=4000)
    xs, ys = truth + 0.3 + rng.normal(0, 0.5, 4000), truth + rng.normal(0, 0.5, 4000)
    c, a = icc(xs, ys)
    assert abs(c - 0.8) < 0.02 and a < c, (c, a)  # 1 / (1 + 0.25)
    print(f"ICC of simulated pairs (true 0.8): consistency {c:.3f}, absolute agreement {a:.3f}")

    # agreement on simulated pairs: bias 0.2, SD 1, three pairs per participant
    pid = np.repeat(np.arange(700), 3)
    g = agreement(0.2 + rng.normal(size=len(pid)), pid, boot=300)
    assert abs(g["bias"] - 0.2) < 0.08 and abs(g["sd"] - 1) < 0.05, g
    assert g["bias_ci"][0] < 0.2 < g["bias_ci"][1], g
    print(f"simulated bias 0.2, SD 1: bias {g['bias']:.3f} ({g['bias_ci'][0]:.3f} to {g['bias_ci'][1]:.3f}), "
          f"limits {g['loa_lo']:.2f} to {g['loa_hi']:.2f}")
    print("all checks passed")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="run the synthetic-shape checks")
    ap.add_argument("--limit", type=int, default=None, help="only the first N Medis participants")
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--src", default=None, help="tracer folder (default tracer_io.TRACER_DIR)")
    ap.add_argument("--lumen", default=None, help="lumen prediction folder (default tracer_io.LUMEN_DIR)")
    ap.add_argument("--medis", default=None, help="Medis contour folder (default <ROOT>/<MEDIS_DIR>)")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "medis_compare.md"))
    ap.add_argument("--rows", default=None, help="folder for the per-pair CSVs and plots (server only)")
    args = ap.parse_args()
    if args.check:
        check()
        return
    from cgps_stats import OUT_DIR

    flow, A, P = run(args.limit, args.src, args.lumen, args.medis)
    rows = Path(args.rows or Path(OUT_DIR) / "medis_compare")
    rows.mkdir(parents=True, exist_ok=True)
    A.to_csv(rows / "medis_compare_arteries.csv", index=False)
    P.to_csv(rows / "medis_compare_participants.csv", index=False)
    plots(A[A["reason"] == "ok"], P[P["aligned"]], rows)
    text = report(flow, A, P, args.boot)
    Path(args.out).write_text(text, encoding="utf-8")
    print(text)
    print(f"written to {args.out}; per-pair rows and plots (with ids, keep on the server) in {rows}")


if __name__ == "__main__":
    main()
