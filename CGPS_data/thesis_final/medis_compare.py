"""Agreement of the geometric features between the in-house tracer and Medis (sec:method-medis-agreement).

    python CGPS_data/thesis_final/medis_compare.py [--limit N] [--boot 2000] [--out MD] [--rows DIR]
    python CGPS_data/thesis_final/medis_compare.py --check   # synthetic shapes, needs no data

Baseline only. Each Medis participant's tracer tree (tracer_io.tracer_tree) and Medis tree
(hoe10y_qc.tree_points) are divided with split_trunks.split, and the LAD, LCx and RCA are paired by name.
Both are in LPS mm (tracer_probe.md), so no mapping is applied.

Curvature, per artery pair:
  shared stretch  each centerline's first and last point is projected onto the other at the closest point;
                  the stretch runs from the later start to the earlier end (shared_stretch). Pairs with a
                  shared stretch under MIN_SHARED mm are left out.
  alignment       median distance from the tracer points of the shared stretch to the Medis centerline; pairs
                  above MAX_OFFSET mm are left out (a wrong vessel or a failed trace). Fixed on 2026-11-18,
                  before any feature difference was looked at.
  curvature       the Menger profile (curvature_feature.curvature_profile) on each full artery, averaged over
                  the shared stretch (segment_mean).
Angle, per participant: bifurcation_angle.lm_angle on each tree's own LAD and LCx (full trees), compared
only where the LAD and the LCx both passed the alignment check (decided 2026-11-18, as for curvature: a
failed pair is probably a different vessel). The CSV keeps every angle with the column aligned.
The daughter asymmetry is added once the tracer lumen contours exist (the delivered files hold none).

Agreement per feature: difference tracer - Medis in the feature's own unit, bias, SD of the differences,
95% limits of agreement (bias +- 1.96 SD) and 95% intervals from a bootstrap over participants. If the
Bland-Altman plot of curvature shows the spread growing with size, add the log ratio then.

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
from bifurcation_angle import lm_angle
from curvature_feature import CHORD, curvature_profile, segment_mean

MAX_OFFSET = 2.0  # mm: median tracer-to-Medis distance over the shared stretch above this = not the same vessel
MIN_SHARED = 10.0  # mm: shorter shared stretches are left out
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
        return row | {"reason": f"shared stretch < {MIN_SHARED:g} mm"}
    keep = (st >= t0) & (st <= t1)
    row["offset"] = float(np.median(np.ravel(nearest(Yt[keep], Ym)[0])))
    if row["offset"] > MAX_OFFSET:
        return row | {"reason": f"offset > {MAX_OFFSET:g} mm"}
    return row | {"reason": "ok", "T_tracer": segment_mean(*curvature_profile(Yt, CHORD, st), t0, t1),
                  "T_medis": segment_mean(*curvature_profile(Ym, CHORD, sm), m0, m1)}


def angle(arteries):
    if "LAD" not in arteries or "CX" not in arteries:
        return np.nan
    return lm_angle(arteries["LAD"][4:], arteries["CX"][4:])


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
            med = split(*graph(hq.tree_points(trees[pid])))
            trc = split(*graph(tracer_io.tracer_tree(pid, src)))
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
            ok |= {a} if A[-1]["reason"] == "ok" else set()
        P.append({"id": pid, "theta_tracer": angle(trc), "theta_medis": angle(med), "aligned": {"LAD", "CX"} <= ok})
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
    from cgps_stats import count

    head = ("| | pairs | bias (95% CI) | SD of differences | lower limit (95% CI) | upper limit (95% CI) | unit |\n"
            "|---|---|---|---|---|---|---|")
    L = ["# Tracer against Medis: agreement of the geometric features (medis_compare.py)\n",
         (f"Baseline. Differences are tracer - Medis. Limits of agreement = bias +- 1.96 SD; 95% intervals from "
          f"{boot} bootstrap samples of participants. Alignment cut {MAX_OFFSET:g} mm, shared stretch at least "
          f"{MIN_SHARED:g} mm. Counts 1-4 shown as <5; statistics only from 5 pairs.\n"),
         "## Flow\n", "| step | participants |", "|---|---|"]
    L += [f"| {k} | {count(v)} |" for k, v in flow.items()]

    if len(A):
        reasons = sorted(A["reason"].unique())
        L += ["\n| artery | " + " | ".join(reasons) + " |", "|---|" + "---|" * len(reasons)]
        for a in ARTERIES:
            c = A[A["artery"] == a]["reason"].value_counts()
            L.append(f"| {NAME[a]} | " + " | ".join(str(count(c.get(r, 0))) for r in reasons) + " |")
        if "offset" in A:
            ok = A[A["reason"] == "ok"]
            L.append("\nMedian tracer-to-Medis distance over the shared stretch (mm), pairs kept: "
                     + ", ".join(f"{NAME[a]} {fmt(ok[ok['artery'] == a]['offset'].median(), 2)}" for a in ARTERIES))

    L += ["\n## Curvature (average over the shared stretch)\n", head]
    if len(A) and "T_tracer" in A:
        for a in ARTERIES + ("all",):
            d = A if a == "all" else A[A["artery"] == a]
            diff = d["T_tracer"].to_numpy(float) - d["T_medis"].to_numpy(float)
            L.append(stat_row("all arteries" if a == "all" else NAME[a], diff, d["id"].to_numpy(), boot, "1/mm"))

    L += ["\n## Bifurcation angle\n", head]
    if len(P):
        Q = P[P["aligned"]]
        t, m = Q["theta_tracer"].to_numpy(float), Q["theta_medis"].to_numpy(float)
        L.append(stat_row("LAD-LCx angle", t - m, Q["id"].to_numpy(), boot, "degrees"))
        L.append(f"\nCompared only where the LAD and LCx both passed the alignment check: "
                 f"{count(len(Q))} participants, {count(len(P) - len(Q))} left out. "
                 f"Among those compared, angle missing: tracer {count(np.isnan(t).sum())}, "
                 f"Medis {count(np.isnan(m).sum())}.")
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
    Q = np.linalg.qr(rng.normal(size=(3, 3)))[0]
    Yr = Y @ Q.T + 7.0
    assert compare_artery(Yr, arc(Yr), Y, arc(Y), _nearest)["reason"].startswith("offset"), "moved copy left out"
    far = Y + [0, 5.0, 0]
    assert compare_artery(Y, arc(Y), far, arc(far), _nearest)["reason"].startswith("offset"), "5 mm away left out"

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
    plots(A, P[P["aligned"]], rows)
    text = report(flow, A, P, args.boot)
    Path(args.out).write_text(text, encoding="utf-8")
    print(text)
    print(f"written to {args.out}; per-pair rows and plots (with ids, keep on the server) in {rows}")


if __name__ == "__main__":
    main()
