"""Agreement of the geometric features between the in-house tracer and Medis (sec:method-medis-agreement).

    python CGPS_data/thesis_final/medis_compare.py [--limit N] [--boot 2000] [--out MD] [--rows DIR]
    python CGPS_data/thesis_final/medis_compare.py --check   # synthetic shapes, needs no data

Baseline only, the Medis participants (all have plaque at baseline). Tracer and Medis points are both in LPS mm
(tracer_probe.md), so no mapping is applied.

The rule (2026-11-19, replaces the comparison over the stretch both centerlines cover, 2026-11-18): every tracer
value is the value the plaque-free cohort gets. tree_features computes it with the cohort's own functions from the
tracer tree and the tracer's own lumen surface alone; no start, end, stretch, cut or check on the tracer side comes
from Medis. The same functions run unchanged on the Medis tree and the Medis lumen meshes. Until 2026-11-19 the
curvature was averaged over the stretch both centerlines cover (ends projected onto Medis), and pairs whose two
traces were more than MAX_OFFSET mm apart were left out of the main rows. Neither can be done without Medis, so the
limits described traces the cohort cannot pick out, over stretches the cohort does not use.

A pair is compared when both trees give a value. For curvature the Medis artery must also be full
(split_trunks.full_artery, 2026-11-19, set after curvature_view.png showed 14-27 mm Medis fragments compared with
whole tracer arteries, before the outcome was linked): along its path, the first label of the artery is its
proximal segment, the last its distal segment, and all its segments occur. It must also be at least as long as the
shortest tracer artery of the same kind with a curvature value in the run (reference_rows; the tracer sets the
minimum, decided 2026-11-19 with the user). This is a rule
on the reference only: a Medis artery that is not full is no reference for a whole-artery average, and the tracer
side is unchanged. A missing Medis value (an artery missing in the Medis tree, Medis
lumen that does not reach every cut) only means there is no reference there. A missing tracer value where Medis has one is
the tracer's own missingness, as in the cohort, and is reported next to the limits.

Features, each tree on its own (tree_features):
  curvature   per artery (LAD with LAD, LCx with LCx, RCA with RCA): the profile of the cohort feature
              (curvature_feature.artery_curvature, Menger, CHORD mm) on the tree's own artery, averaged over the
              whole artery, from its start to its end in split_trunks.split (the three segments together; the
              tracer from its own ostia, tracer_io.tracer_ostia). Each tree keeps its own start and end, so a
              difference in where the two traces stop is part of the difference.
  angle       bifurcation_angle.angle_with_reason.
  asymmetry   daughter_ratio.tree_asymmetry on the tree's own lumen surface: the tracer's
              lumen_surface_ostium_pruned.vtk (tracer_io.tracer_lumen) and the participant's BL Medis lumen meshes
              of the left tree, merged. Medis contoured almost only diseased segments, so every participant compared
              has plaque at the bifurcation.
A feature whose computation raises is missing with the reason error:<type> (guarded); the others are kept.

Same-vessel check, a condition of the main rows (2026-11-19, with the user: compare the same centerline, but
without cutting the features to the stretch both cover; before, the check was only descriptive, since the cohort
cannot apply it). The pairs that fail it are kept in one sensitivity row per feature, which is the closer estimate
of the error in the cohort, where every trace is used. Per artery, the stretch both centerlines cover (each line's ends projected onto the other at the closest point,
from the later start to the earlier end, at least MIN_SHARED mm), both stretches resampled every DENSE mm, the 90th
percentile of the distances from each to the other, the larger of the two, at most MAX_OFFSET mm (artery_offset).
For the angle and the asymmetry also near_o on the LAD and the LCx: the same distance from each tree's first
DEPTHS[-1] mm of the daughter from its own O to the other tree's left main and whole daughter. o_dist, the distance
between the two bifurcation points O, is reported. Curvature needs the artery to pass; the angle and the
asymmetry need the LAD and the LCx to pass and to pass near_o (aligned). The check only selects pairs: every
feature value is still the whole-artery value of each tree on its own.

Agreement per feature: difference tracer - Medis in the feature's own unit, bias, SD of the differences, 95% limits
of agreement (bias +- 1.96 SD) and 95% intervals from a bootstrap over participants. Reliability per feature, on the
same pairs: SD of each method, SD of the differences, consistency ICC(C,1) and absolute agreement ICC(A,1) (McGraw
and Wong 1996), with bootstrap intervals over participants; for the asymmetry also abs(a), the model feature.

Writes medis_compare.md next to this script (aggregates only: counts 1-4 hidden, statistics only from MIN_CELL
pairs) and, in --rows (server only, contains study ids), the per-pair CSVs and Bland-Altman plots.
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
from curvature_feature import CHORD, artery_curvature
from daughter_ratio import SECTION_DEPTHS, merge, surface, tree_asymmetry

MAX_OFFSET = 2.0  # mm: 90th percentile of the point distances, both ways, above this = not the same vessel
MIN_SHARED = 10.0  # mm: shortest stretch both centerlines cover on which the same-vessel check is made
DENSE = 0.25  # mm: both stretches are resampled this finely for the distances
O_FAR = 5.0  # mm: o_dist above this is counted in the report
ARTERIES = ("LAD", "CX", "RCA")
RIGHT = {"prca", "mrca", "drca", "rca", "pda", "pla"}  # Medis lumen sets of the right tree, not read for the asymmetry
NAME = {"LAD": "LAD", "CX": "LCx", "RCA": "RCA"}
NAN_ASYM = {"asym": np.nan, "D_LAD": np.nan, "D_CX": np.nan}


# ---------------------------------------------------------------- features: one tree, nothing from the other

def guarded(fn, *args):
    """(fn(*args), None), or (None, "error:<type>") when it raises: counted in the report, not a stopped run."""
    try:
        return fn(*args), None
    except Exception as ex:  # noqa: BLE001 - counted
        return None, f"error:{type(ex).__name__}"


def tree_features(tree, roots=None, surf=None):
    """Every feature of one tree from the cohort's functions, on this tree and its own lumen surface alone:
    {"arteries": split_trunks.split, "T": {artery: 1/mm}, "theta", "reason_theta", "asym": {...}}.
    roots: the tree's own ostia (tracer_io.tracer_ostia), None for Medis. surf: a callable that loads the tree's
    lumen surface (V, F), None when the tree has none. Raises only when the tree cannot be divided."""
    from split_trunks import graph, split

    info = {}
    arts = split(*graph(tree), info=info, roots=roots)
    T, err = guarded(lambda: {a: artery_curvature(Y, s, (0.0, end), CHORD)[0]
                              for a, (_, _, end, _, Y, s) in arts.items()})
    out = {"arteries": arts, "info": info, "T": T or {}, "T_reason": err or "ok"}
    res, err = guarded(angle_with_reason, tree, arts)
    out["theta"], out["reason_theta"] = res or (np.nan, err)
    if surf is None:
        out["asym"] = NAN_ASYM | {"reason": "no lumen surface"}
    else:
        res, err = guarded(lambda: tree_asymmetry(tree, surf(), roots, arts))
        out["asym"] = res or NAN_ASYM | {"reason": err}
    return out


# ---------------------------------------------------------------- same-vessel check (descriptive)

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


def artery_offset(Yt, st, Ym, sm, nearest):
    """Same-vessel check of one artery, tracer (Yt, st) against Medis (Ym, sm): the larger 90th percentile of the
    distances between the two shared stretches, with the reason. Changes no feature value."""
    (t0, t1), (m0, m1) = shared_stretch(Yt, st, Ym, sm)
    row = {"shared_tracer": t1 - t0, "shared_medis": m1 - m0}
    if min(t1 - t0, m1 - m0) < MIN_SHARED:
        return row | {"reason": f"shared stretch < {MIN_SHARED:g} mm"}
    A, B = stretch(Yt, st, t0, t1), stretch(Ym, sm, m0, m1)
    (p_t, med_t), (p_m, _) = p90(A, B, nearest), p90(B, A, nearest)
    off = max(p_t, p_m)
    return row | {"offset": off, "offset_median": med_t, "reason": "ok" if off <= MAX_OFFSET else f"offset > {MAX_OFFSET:g} mm"}


def near_o(Yt, st, Ym, sm, lm_t, lm_m, nearest, depth=DEPTHS[-1]):
    """Same-vessel check of one daughter at the bifurcation: the larger 90th percentile of the distances from each
    tree's first depth mm from its own O to the other tree's left main (lm_t, lm_m: ostium to O) and whole
    daughter. The left main is in the reference so that O placed further along the same vessel in one tree does
    not fail the check; nan when either daughter is shorter than depth."""
    if min(st[-1] - st[0], sm[-1] - sm[0]) < depth:
        return np.nan
    whole = lambda Y: stretch(Y, arc(Y), 0, arc(Y)[-1]) if len(Y) > 1 else Y  # noqa: E731
    ref_t, ref_m = np.r_[whole(lm_t), whole(Yt)], np.r_[whole(lm_m), whole(Ym)]
    return max(p90(stretch(Yt, st, st[0], st[0] + depth), ref_m, nearest)[0],
               p90(stretch(Ym, sm, sm[0], sm[0] + depth), ref_t, nearest)[0])


def medis_lumen_files(medis=None):
    """{id: [the participant's BL Medis lumen files of the left tree]} (split_check.contour_files)."""
    import hoe10y_qc as hq
    from split_check import contour_files

    out = {}
    for (i, seg), fs in contour_files(medis or Path(hq.ROOT) / hq.MEDIS_DIR).items():
        if "lumen" in fs and seg not in RIGHT:
            out.setdefault(i, []).append(fs["lumen"])
    return out


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
    from split_trunks import full_artery, graph, left_main

    src, lumen = src or tracer_io.TRACER_DIR, lumen or tracer_io.LUMEN_DIR
    med_lumen = medis_lumen_files(medis)
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
        f_lumen = Path(tracer_io.tracer_lumen(pid, lumen))
        try:
            med_tree, trc_tree = hq.tree_points(trees[pid]), tracer_io.tracer_tree(pid, src)
            roots = tracer_io.tracer_ostia(pid, src)
            trc = tree_features(trc_tree, roots, (lambda: surface(f_lumen)) if f_lumen.exists() else None)
            med = tree_features(med_tree, None, (lambda: merge([surface(f) for f in med_lumen[pid]]))
                                if pid in med_lumen else None)
        except Exception:  # noqa: BLE001 - counted
            flow["tree not divided"] += 1
            continue
        flow["both trees divided"] += 1

        ta, ma = trc["arteries"], med["arteries"]
        same = set()
        for a in ARTERIES:
            row = {"id": pid, "artery": a, "T_tracer": trc["T"].get(a, np.nan), "T_medis": med["T"].get(a, np.nan)}
            row["medis_full"], row["medis_full_reason"] = (
                full_artery(a, med["info"][a]["path_labels"]) if a in ma else (False, "missing in Medis"))
            row["L_tracer"] = float(ta[a][5][-1]) if a in ta else np.nan  # artery length (mm), from its own start
            row["L_medis"] = float(ma[a][5][-1]) if a in ma else np.nan
            if a in ta and a in ma:
                res, err = guarded(artery_offset, *ta[a][4:], *ma[a][4:], cq.nearest)
                row |= res or {"reason": err}
            else:
                row["reason"] = "missing in " + " and ".join(n for n, t in (("Medis", ma), ("tracer", ta)) if a not in t)
            A.append(row)
            same |= {a} if row["reason"] == "ok" else set()

        row = {"id": pid, "theta_tracer": trc["theta"], "reason_tracer": trc["reason_theta"],
               "theta_medis": med["theta"], "reason_medis": med["reason_theta"], "aligned_whole": {"LAD", "CX"} <= same}
        if row["aligned_whole"]:  # near_o is checked only then
            lms, err = guarded(lambda: (left_main(*graph(trc_tree), roots), left_main(*graph(med_tree))))
            for a in ("LAD", "CX"):
                res, err_a = (None, err) if err else guarded(near_o, *ta[a][4:], *ma[a][4:], *lms, cq.nearest)
                row[f"near_o_{a}"], row[f"near_o_reason_{a}"] = (np.nan, err_a) if err_a else (res, "ok")
        row["o_dist"] = float(np.linalg.norm(ta["LAD"][4][0] - ma["LAD"][4][0])) if "LAD" in ta and "LAD" in ma else np.nan
        row["aligned"] = row["aligned_whole"] and all(row[f"near_o_{a}"] <= MAX_OFFSET for a in ("LAD", "CX"))
        for name, f in (("tracer", trc), ("medis", med)):
            row |= {f"{k}_{name}": v for k, v in f["asym"].items() if k != "reason"}
            row[f"asym_reason_{name}"] = f["asym"]["reason"]
        rm, rt = row["asym_reason_medis"], row["asym_reason_tracer"]
        row["asym_reason"] = "ok" if rm == rt == "ok" else f"Medis: {rm}" if rm != "ok" else f"tracer: {rt}"
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


def reference_rows(A):
    """(rows whose Medis artery is a reference for curvature, {artery: minimum length in mm}). A reference is full
    (split_trunks.full_artery) and at least as long as the shortest tracer artery of the same kind that has a
    curvature value in A (decided 2026-11-19 with the user: the tracer sets the minimum length Medis must reach).
    Rules on the Medis side only; the tracer values are those of the cohort."""
    if not len(A) or "medis_full" not in A:
        return A.iloc[:0], {}
    min_len = {a: float(A.loc[(A["artery"] == a) & A["T_tracer"].notna(), "L_tracer"].min()) for a in ARTERIES}
    keep = A["medis_full"].astype(bool) & (A["L_medis"] >= A["artery"].map(min_len))
    return A[keep], min_len


def coverage(t, m):
    """Pairs with a Medis value, and how many of them also have a tracer value: the tracer's own missingness
    where there is a reference."""
    from cgps_stats import count

    t, m = np.isfinite(np.asarray(t, float)), np.isfinite(np.asarray(m, float))
    n, both = int(m.sum()), int((t & m).sum())
    return f"{count(n)} | {count(both)} ({100 * both / n:.0f}%)" if n else "0 | -"


def report(flow, A, P, boot):
    from cgps_stats import MIN_CELL, QUARTILE_MIN, TAIL_MIN, count

    def med(x):
        x = np.asarray(x, float)
        x = x[np.isfinite(x)]
        return np.median(x) if len(x) >= QUARTILE_MIN else None

    def both(d, col):
        return d[np.isfinite(d[f"{col}_tracer"].astype(float)) & np.isfinite(d[f"{col}_medis"].astype(float))]

    def diff(d, col):
        return d[f"{col}_tracer"].to_numpy(float) - d[f"{col}_medis"].to_numpy(float)

    head = ("| | pairs | bias (95% CI) | SD of differences | lower limit (95% CI) | upper limit (95% CI) | unit |\n"
            "|---|---|---|---|---|---|---|")
    L = ["# Tracer against Medis: agreement of the geometric features (medis_compare.py)\n",
         (f"Baseline. Differences are tracer - Medis. Every value is computed on its own tree by the cohort's "
          f"functions (tree_features), so the tracer values are those the plaque-free cohort gets; nothing on the "
          f"tracer side comes from Medis. A pair is compared when both trees give a value. Limits of agreement = "
          f"bias +- 1.96 SD; 95% intervals from {boot} bootstrap samples of participants. Counts 1-4 shown as <5; "
          f"statistics only from 5 pairs.\n"),
         "## Flow\n", "| step | participants |", "|---|---|"]
    L += [f"| {k} | {count(v)} |" for k, v in flow.items()]

    F, min_len = reference_rows(A)
    L += ["\n## Curvature per artery (average over each tree's whole artery)\n",
          ("Compared only where the Medis artery is full (split_trunks.full_artery, 2026-11-19): along its path the "
           "first label of the artery is its proximal segment, the last its distal segment, and the proximal, mid and "
           "distal segments all occur. It must also be at least as long as the shortest tracer artery of the same kind "
           "with a curvature value in this run (reference_rows): "
           + ", ".join(f"{NAME[a]} {fmt(min_len.get(a), 3)} mm" for a in ARTERIES)
           + ". Rules on the reference only; the tracer side is unchanged.\n"),
          "| artery | Medis artery | reference (full, long enough) | left out, by reason |", "|---|---|---|---|"]
    if len(A):
        for a in ARTERIES:
            d = A[(A["artery"] == a) & A["T_medis"].notna()]
            nf = d[~d["medis_full"].astype(bool)]["medis_full_reason"].value_counts()
            short = int((d["medis_full"].astype(bool) & ~d["id"].isin(F[F["artery"] == a]["id"])).sum())
            L.append(f"| {NAME[a]} | {count(len(d))} | {count(int(d['medis_full'].astype(bool).sum()) - short)} | "
                     + "; ".join([f"{r} {count(n)}" for r, n in nf.items()]
                                 + ([f"full but shorter than the shortest tracer {NAME[a]} {count(short)}"] if short else []))
                     + " |")
        L += ["", "| artery | full Medis artery with a value | tracer value too (share) |", "|---|---|---|"]
        for a in ARTERIES:
            d = F[F["artery"] == a]
            L.append(f"| {NAME[a]} | {coverage(d['T_tracer'], d['T_medis'])} |")
        L += ["", head]
        B = both(F, "T")
        S = B[B["reason"] == "ok"]  # same vessel
        for a in ARTERIES:
            d = S[S["artery"] == a]
            L.append(stat_row(NAME[a], diff(d, "T"), d["id"].to_numpy(), boot, "1/mm"))
        L.append(stat_row("all arteries", diff(S, "T"), S["id"].to_numpy(), boot, "1/mm"))
        L.append(stat_row("all arteries, also pairs failing the same-vessel check (sensitivity)", diff(B, "T"),
                          B["id"].to_numpy(), boot, "1/mm"))

    L += ["\n## Bifurcation angle (bifurcation_angle.angle_with_reason on each tree)\n", head]
    if len(P):
        B = both(P, "theta")
        d = B[B["aligned"].astype(bool)]
        L.append(stat_row("LAD-LCx angle", diff(d, "theta"), d["id"].to_numpy(), boot, "degrees"))
        L.append(stat_row("LAD-LCx angle, also pairs failing the same-vessel check (sensitivity)", diff(B, "theta"),
                          B["id"].to_numpy(), boot, "degrees"))
        L.append(f"\nParticipants with both trees divided {count(len(P))}; Medis angle "
                 f"{coverage(P['theta_tracer'], P['theta_medis']).replace(' | ', ', tracer angle too ')}. "
                 f"Angle missing, by reason (all divided participants):")
        L += ["\n| reason | tracer | Medis |", "|---|---|---|"]
        for r in sorted(set(P["reason_tracer"]) | set(P["reason_medis"])):
            if r != "ok":
                L.append(f"| {r} | {count((P['reason_tracer'] == r).sum())} | {count((P['reason_medis'] == r).sum())} |")
        o = B["o_dist"].to_numpy(float)
        o = o[np.isfinite(o)]
        if len(o) >= MIN_CELL:
            p90_ = np.percentile(o, 90) if len(o) >= TAIL_MIN else None
            L.append(f"\nDistance between the tracer's and Medis' bifurcation point O, angles compared: median "
                     f"{fmt(med(o), 2)} mm, 90th percentile {fmt(p90_, 2)} mm, {count(int((o > O_FAR).sum()))} "
                     f"({100 * (o > O_FAR).mean():.0f}%) above {O_FAR:g} mm.")

    L += ["\n## Daughter asymmetry ln(D_LCx / D_LAD) (daughter_ratio.tree_asymmetry on each tree)\n", head]
    if len(P) and "asym_tracer" in P:
        B = both(P, "asym")
        d = B[B["aligned"].astype(bool)]
        for col, label, unit in (("asym", "asymmetry", "ln ratio"), ("D_LAD", "LAD diameter", "mm"),
                                 ("D_CX", "LCx diameter", "mm")):
            L.append(stat_row(label, diff(d, col), d["id"].to_numpy(), boot, unit))
        L.append(stat_row("asymmetry, also pairs failing the same-vessel check (sensitivity)", diff(B, "asym"),
                          B["id"].to_numpy(), boot, "ln ratio"))
        L.append(f"\nPlane cuts of each tree's own lumen surface at {len(SECTION_DEPTHS)} depths, {SECTION_DEPTHS[0]:g} "
                 f"to {SECTION_DEPTHS[-1]:g} mm from its own O; a daughter counts only when every cut has a diameter. "
                 f"Medis asymmetry {coverage(P['asym_tracer'], P['asym_medis']).replace(' | ', ', tracer asymmetry too ')}. "
                 f"Asymmetry missing, by reason (all divided participants):")
        L += ["\n| reason | tracer | Medis |", "|---|---|---|"]
        for r in sorted(set(P["asym_reason_tracer"]) | set(P["asym_reason_medis"])):
            if r != "ok":
                L.append(f"| {r} | {count((P['asym_reason_tracer'] == r).sum())} | "
                         f"{count((P['asym_reason_medis'] == r).sum())} |")
        L.append("\nMedis lumen exists only where Medis contoured, almost always diseased segments: every participant "
                 "compared here has plaque at the bifurcation, unlike the plaque-free cohort.")

    if len(A):
        reasons = sorted(A["reason"].unique())
        L += ["\n## Same-vessel check (a condition of the main rows above)\n",
              (f"Per artery: 90th percentile of the distances between the two centerlines over the stretch both cover, "
               f"both ways, at most {MAX_OFFSET:g} mm, the stretch at least {MIN_SHARED:g} mm. Pairs by reason (share "
               f"of the artery's pairs):\n"),
              "| artery | " + " | ".join(reasons) + " |", "|---|" + "---|" * len(reasons)]
        for a in ARTERIES:
            c = A[A["artery"] == a]["reason"].value_counts()
            L.append(f"| {NAME[a]} | " + " | ".join(f"{count(c.get(r, 0))} ({100 * c.get(r, 0) / c.sum():.0f}%)"
                                                    for r in reasons) + " |")
        if "offset" in A:
            ok = A[A["reason"] == "ok"]
            L.append(f"\nSame-vessel pairs, distance (mm), median over pairs of the per-pair median (tracer to Medis) / "
                     f"of the per-pair 90th percentile (both ways), from {QUARTILE_MIN} pairs: "
                     + ", ".join(f"{NAME[a]} {fmt(med(ok[ok['artery'] == a]['offset_median']), 2)} / "
                                 f"{fmt(med(ok[ok['artery'] == a]['offset']), 2)}" for a in ARTERIES))
        if len(P):
            L.append(f"\nAngle and asymmetry: LAD and LCx both same vessel {count(int(P['aligned_whole'].sum()))} "
                     f"({100 * P['aligned_whole'].mean():.0f}%), and within the first {DEPTHS[-1]:g} mm from O (near_o) "
                     f"{count(int(P['aligned'].sum()))} ({100 * P['aligned'].mean():.0f}%) of {count(len(P))}.")

    L += ["\n## Reliability: measurement error against the spread between people\n",
          ("Same pairs as the main agreement rows above. ICC(C,1) (consistency) ignores a constant bias, which does "
           "not change a per-SD hazard ratio; ICC(A,1) (absolute agreement) also counts the bias (McGraw and Wong "
           "1996). With no ground truth, Medis is a second error-prone measurement, not the truth; the ICC is the "
           "share of the variance between pairs that the two methods agree on.\n"),
          "| | pairs | SD tracer | SD Medis | SD of differences | ICC(C,1) (95% CI) | ICC(A,1) (95% CI) | unit |",
          "|---|---|---|---|---|---|---|---|"]
    sets = []
    S = F[F["reason"] == "ok"] if len(F) else F
    if len(S):
        sets += [(f"curvature, {NAME[a]}", S[S["artery"] == a], "T", "1/mm") for a in ARTERIES]
        sets.append(("curvature, all arteries", S, "T", "1/mm"))
    if len(P):
        sets.append(("LAD-LCx angle", P[P["aligned"].astype(bool)], "theta", "degrees"))
    if len(P) and "asym_tracer" in P:
        Q = P[P["aligned"].astype(bool)]
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

    sets = [("curvature", A.get("T_tracer"), A.get("T_medis"), "average curvature per artery (1/mm)"),
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


def _left_tree(shift=0.0, cx_turn=0.6):
    """A made-up left tree in the structure of hoe10y_qc.tree_points: an LM of 10 mm, then a wavy LAD and an LCx
    that leaves at cx_turn rad. shift moves the whole tree."""
    lm = np.c_[np.linspace(-10, 0, 21), np.zeros(21), np.zeros(21)]
    lad = _wavy(np.linspace(0, 90, 361)) - _wavy(np.zeros(1))
    t = np.linspace(0, 60, 241)
    cx = np.c_[t * np.cos(cx_turn), -t * np.sin(cx_turn), 2 * np.sin(t / 8)]
    labs = lambda n, a: [f"p{a}"] * (n // 3) + [f"m{a}"] * (n // 3) + [f"d{a}"] * (n - 2 * (n // 3))  # noqa: E731
    return [(np.r_[lm, lad[1:]] + shift, ["lm"] * 21 + labs(360, "lad")),
            (cx + shift, ["lm"] + labs(240, "cx"))]


def check():
    """Known answers."""
    from bifurcation_angle import tree_angle

    rng = np.random.default_rng(0)
    # the features of a tree depend on that tree only: the cohort's functions give the same values
    tree = _left_tree()
    f = tree_features(tree)
    from split_trunks import graph, split
    arts = split(*graph(tree))
    assert set(f["T"]) == {"LAD", "CX"} and all(
        f["T"][a] == artery_curvature(Y, s, (0.0, end))[0] for a, (_, _, end, _, Y, s) in arts.items()), f["T"]
    pm, md, end, _, Y, s = arts["LAD"]
    parts = artery_curvature(Y, s, (0.0, pm, md, end))
    assert min(parts) <= f["T"]["LAD"] <= max(parts), "the artery mean lies among its segment means"
    assert f["theta"] == tree_angle(tree) and f["reason_theta"] == "ok", (f["theta"], f["reason_theta"])
    assert f["asym"]["reason"] == "no lumen surface" and np.isnan(f["asym"]["asym"]), f["asym"]
    g = tree_features(_left_tree(shift=np.array([3.0, -2.0, 1.0])))
    assert np.allclose([f["T"][k] for k in sorted(f["T"])], [g["T"][k] for k in sorted(g["T"])]), "moved tree"
    assert abs(f["theta"] - g["theta"]) < 1e-9, "moved tree: same angle"
    f = tree_features(tree, surf=lambda: (_ for _ in ()).throw(OSError("unreadable")))
    assert f["asym"]["reason"] == "error:OSError" and np.isfinite(f["theta"]), "a failed surface hides nothing else"
    print(f"made-up left tree: angle {f['theta']:.1f} deg, curvature LAD {f['T']['LAD']:.4f} 1/mm")

    # shared stretch of two straight lines that overlap from x = 10 to x = 50
    a = np.c_[np.linspace(0, 50, 101), np.zeros(101), np.zeros(101)]
    b = np.c_[np.linspace(10, 70, 121), np.full(121, 0.3), np.zeros(121)]
    (a0, a1), (b0, b1) = shared_stretch(a, arc(a), b, arc(b))
    assert np.allclose((a0, a1, b0, b1), (10, 50, 0, 40)), (a0, a1, b0, b1)
    assert np.isclose(project(a, arc(a), np.array([12.3, 5.0, 0])), 12.3), "projection onto a piece"

    # same-vessel check
    Y = _wavy(np.linspace(0, 90, 400))
    s = arc(Y)
    assert artery_offset(Y, s, Y, s, _nearest)["reason"] == "ok", "identical lines"
    Ym = _wavy(np.sort(rng.uniform(8, 80, 600)))  # Medis: starts later, ends earlier, uneven points
    row = artery_offset(Y, s, Ym, arc(Ym), _nearest)
    assert row["reason"] == "ok" and row["offset"] < 0.2, row
    assert artery_offset(Y + [0, 0, 3.0], s, Y, s, _nearest)["reason"].startswith("offset"), "3 mm moved copy"
    short = Y[s <= 8]
    assert artery_offset(short, arc(short), Y, s, _nearest)["reason"].startswith("shared stretch"), "under 10 mm"
    branch = Y + np.c_[np.zeros(len(Y)), np.zeros(len(Y)), np.clip(s - 0.6 * s[-1], 0, None)]  # leaves after 60%
    row = artery_offset(branch, arc(branch), Y, s, _nearest)
    assert row["offset_median"] < MAX_OFFSET and row["reason"].startswith("offset"), row
    print(f"branch leaving over the last 40%: median {row['offset_median']:.2f} mm, 90th percentile "
          f"{row['offset']:.1f} mm -> not the same vessel")
    # the offset does not depend on how unevenly Medis is sampled
    x = np.r_[np.linspace(0, 54, 1500), np.linspace(54.5, 90, 8)]  # dense first 60%, 8 points over the rest
    Ye, Yu = _wavy(np.linspace(0, 90, 300)) + [0, 1.0, 0], _wavy(x) + [0, 1.0, 0]
    oe, ou = (artery_offset(Y, s, Z, arc(Z), _nearest)["offset"] for Z in (Ye, Yu))
    assert abs(oe - ou) < 0.15, (oe, ou)
    # a tracer end that turns back along the line: the end projects onto Medis 25 mm early
    m = np.c_[np.linspace(0, 50, 101), np.zeros(101), np.zeros(101)]
    back = np.c_[np.linspace(49.5, 25, 50), np.full(50, 1.5), np.zeros(50)]
    t = np.r_[m, [[50.5, 0.4, 0], [50.8, 0.75, 0], [50.5, 1.1, 0]], back]
    assert artery_offset(t, arc(t), m, arc(m), _nearest)["reason"].startswith("offset"), "turning back"
    # near O: left main along x up to O, daughter on along x
    line = lambda a, b: np.c_[np.linspace(a, b, int(2 * (b - a)) + 1), np.zeros(int(2 * (b - a)) + 1), np.zeros(int(2 * (b - a)) + 1)]  # noqa: E731
    lm_t, lad_t = line(-8, 0), line(0, 30)
    assert near_o(lad_t, arc(lad_t), lad_t, arc(lad_t), lm_t, lm_t, _nearest) < 1e-9, "same daughter"
    lm_m, lad_m = line(-8, -4), line(-4, 30)  # Medis O 4 mm further up the same vessel: passes
    assert near_o(lad_t, arc(lad_t), lad_m, arc(lad_m), lm_t, lm_m, _nearest) < 0.2, "O shifted along the vessel"
    d = np.linspace(0, 30, 61)
    other = np.c_[d * np.cos(0.8), d * np.sin(0.8), 0 * d]  # the tracer daughter enters a vessel 46 deg off
    assert near_o(other, arc(other), lad_t, arc(lad_t), lm_t, lm_t, _nearest) > MAX_OFFSET, "other vessel"
    assert np.isnan(near_o(lad_t[:10], arc(lad_t[:10]), lad_t, arc(lad_t), lm_t, lm_t, _nearest)), "under 10 mm"
    # a raising computation is counted, not a stopped run
    assert guarded(artery_offset, Y[:1], arc(Y[:1]), Y, s, _nearest)[1].startswith("error:")
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
    plots(A, P, rows)
    text = report(flow, A, P, args.boot)
    Path(args.out).write_text(text, encoding="utf-8")
    print(text)
    print(f"written to {args.out}; per-pair rows and plots (with ids, keep on the server) in {rows}")


if __name__ == "__main__":
    main()
