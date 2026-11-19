"""Agreement of the geometric features between the in-house tracer and Medis (sec:method-medis-agreement).

    python CGPS_data/thesis_final/medis_compare.py [--limit N] [--boot 2000] [--out MD] [--rows DIR]
    python CGPS_data/thesis_final/medis_compare.py --check   # synthetic shapes, needs no data

Baseline only. Each Medis participant's tracer tree (tracer_io.tracer_tree) and Medis tree
(hoe10y_qc.tree_points) are divided with split_trunks.split, and the LAD, LCx and RCA are paired by name.
The tracer tree starts at the tracer's own ostia (tracer_io.tracer_ostia, passed as roots); the Medis tree
starts at its LM label.
Both are in LPS mm (tracer_probe.md), so no mapping is applied.

Curvature, per artery pair:
  shared stretch  each centerline's first and last point is projected onto the other at the closest point;
                  the stretch runs from the later start to the earlier end (shared_stretch). Pairs with a
                  shared stretch under MIN_SHARED mm are left out.
  averaged part   the shared stretch without CHORD mm at each end, on both lines: a profile has no points
                  within CHORD of its own line's ends, so without this the line that ends first would lose
                  up to CHORD mm at an end that the other keeps (code review 2026-11-18). Pairs whose averaged
                  part is under MIN_SHARED mm are left out.
  alignment       90th percentile of the distances from the points of each centerline's shared stretch to the
                  other centerline (resampled every DENSE mm, so the distance is to the line, not only to its
                  points; code review 2026-11-18), the larger of the two directions; pairs above MAX_OFFSET mm are left out
                  (a wrong vessel or a failed trace). MAX_OFFSET was fixed on 2026-11-18 before any feature
                  difference was looked at. Until the code review of 2026-11-18 the rule used the median, one
                  way (tracer to Medis): a branch could then take up nearly half the stretch and still pass.
                  The change was made for that reason, not because of the feature differences. The median
                  (tracer to Medis) stays as the column offset_median.
  curvature       the Menger profile (curvature_feature.curvature_profile) on each full artery, averaged over
                  the averaged part (segment_mean). T is also computed for pairs that fail only the alignment
                  check, for the sensitivity row "including offset failures". Order: shared stretch, alignment,
                  averaged part; aligned_artery = passed the alignment check (whatever the averaged part).
Angle, per participant: bifurcation_angle.lm_angle on each tree's own LAD and LCx (full trees), compared
only where the LAD and the LCx both passed the alignment check (aligned_artery, so not the averaged-part
length, which concerns curvature only: the angle uses 5-10 mm from O; decided 2026-11-18, as for curvature: a
failed pair is probably a different vessel). o_dist, the distance between the tracer's and Medis'
bifurcation point O, is saved and reported, not used as a cut (code review 2026-11-18: a cut chosen after the
angle results were seen would be tuned on them). An angle is missing for a tree without an LM label
(bifurcation_angle.has_lm, 2026-11-18). The CSV keeps every angle with the column aligned and the reasons.
The daughter asymmetry is added once the tracer lumen contours exist (the delivered files hold none).

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
from bifurcation_angle import has_lm, lm_angle
from curvature_feature import CHORD, curvature_profile, segment_mean

MAX_OFFSET = 2.0  # mm: 90th percentile of the point distances, both ways, above this = not the same vessel
MIN_SHARED = 10.0  # mm: minimum shared stretch, and minimum averaged part (shared stretch less CHORD at each end)
DENSE = 0.25  # mm: the other centerline is resampled this finely for the distances
O_FAR = 5.0  # mm: o_dist above this is counted in the report (not a cut)
ARTERIES = ("LAD", "CX", "RCA")
NAME = {"LAD": "LAD", "CX": "LCx", "RCA": "RCA"}


# ---------------------------------------------------------------- geometry

def arc(Y):
    return np.r_[0, np.cumsum(np.linalg.norm(np.diff(Y, axis=0), axis=1))]


def densify(Y, step=DENSE):
    """Y resampled linearly along its arc every step mm (ends kept)."""
    s = arc(Y)
    q = np.r_[np.arange(0, s[-1], step), s[-1]]
    return np.column_stack([np.interp(q, s, Y[:, k]) for k in range(Y.shape[1])])


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
    dt = np.ravel(nearest(Yt[(st >= t0) & (st <= t1)], densify(Ym))[0])
    dm = np.ravel(nearest(Ym[(sm >= m0) & (sm <= m1)], densify(Yt))[0])
    off = float(max(np.percentile(dt, 90), np.percentile(dm, 90)))
    row |= {"offset": off, "offset_median": float(np.median(dt)), "aligned_artery": off <= MAX_OFFSET}
    if off > MAX_OFFSET:
        reason = f"offset > {MAX_OFFSET:g} mm"
    elif min(t1 - t0, m1 - m0) - 2 * CHORD < MIN_SHARED:
        return row | {"reason": f"averaged part < {MIN_SHARED:g} mm"}
    else:
        reason = "ok"
    return row | {"reason": reason, "T_tracer": segment_mean(*curvature_profile(Yt, CHORD, st), t0 + CHORD, t1 - CHORD),
                  "T_medis": segment_mean(*curvature_profile(Ym, CHORD, sm), m0 + CHORD, m1 - CHORD)}


def angle(tree, arteries):
    """(angle in degrees or nan, reason)."""
    if not has_lm(tree):
        return np.nan, "no LM label"
    if "LAD" not in arteries or "CX" not in arteries:
        return np.nan, "LAD or LCx missing"
    theta = lm_angle(arteries["LAD"][4:], arteries["CX"][4:])
    return theta, "ok" if np.isfinite(theta) else "no shared O or a daughter under 10 mm"


# ---------------------------------------------------------------- agreement

def agreement(diff, pid, boot=2000, seed=0):
    """Bias, SD, limits of agreement and their 95% intervals from a bootstrap over participants."""
    diff, pid = np.asarray(diff, float), np.asarray(pid)
    bias, sd = diff.mean(), diff.std(ddof=1)
    out = {"n": len(diff), "bias": bias, "sd": sd, "loa_lo": bias - 1.96 * sd, "loa_hi": bias + 1.96 * sd}
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


# ---------------------------------------------------------------- data run (server)

def run(limit=None, src=None):
    import centerline_qc as cq
    import hoe10y_qc as hq
    import tracer_io
    from split_trunks import graph, split

    src = src or tracer_io.TRACER_DIR
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
            med = split(*graph(med_tree))
            trc = split(*graph(trc_tree), roots=tracer_io.tracer_ostia(pid, src))
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
            A.append({"id": pid, "artery": a} | compare_artery(*trc[a][4:], *med[a][4:], cq.nearest))
            ok |= {a} if A[-1]["aligned_artery"] else set()
        (tt, rt), (tm, rm) = angle(trc_tree, trc), angle(med_tree, med)
        o_dist = float(np.linalg.norm(trc["LAD"][4][0] - med["LAD"][4][0])) if "LAD" in trc and "LAD" in med else np.nan
        P.append({"id": pid, "theta_tracer": tt, "theta_medis": tm, "reason_tracer": rt, "reason_medis": rm,
                  "aligned": {"LAD", "CX"} <= ok, "o_dist": o_dist})
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

    L += ["\n## Curvature (average over the shared stretch)\n", head]
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
        L.append(f"\nFlow: both trees divided {count(len(P))}; LAD and LCx both passed the alignment check "
                 f"{count(len(Q))} ({100 * len(Q) / len(P):.0f}%); angle in both {count(int(both.sum()))} "
                 f"({100 * both.sum() / len(P):.0f}%). Among the aligned, angle missing:")
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
    return "\n".join(L) + "\n"


def plots(A, P, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sets = [("curvature", A.get("T_tracer"), A.get("T_medis"), "average curvature (1/mm)"),
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
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "medis_compare.md"))
    ap.add_argument("--rows", default=None, help="folder for the per-pair CSVs and plots (server only)")
    args = ap.parse_args()
    if args.check:
        check()
        return
    from cgps_stats import OUT_DIR

    flow, A, P = run(args.limit, args.src)
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
