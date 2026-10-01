"""Out-of-plane scalars per vessel: reliable, and not redundant with ka5?

    python -m tortuosity.research.unified.planarity [--n 150]
Same sample, vessels, orientation and perturbation seeds as cohort.py (first n train ids; LAD, LCX, RCA;
iid006 / iid05 / corr05 x3, trunc20 x1), so f_twist from cohort_train<n>.csv joins row for row.
Candidates, on the delivered centerline resampled at 0.25 mm (bishop.arc_resample, no extra smoothing):
  nonpl      3rd PCA eigenvalue / trace of the whole vessel                    (0 derivatives)
  plane_rms  RMS distance to the vessel's own best-fit plane / arc length      (0 derivatives)
  plane_ang  mean |angle| between unit tangent and that plane, deg            (1 derivative)
  winpl20    mean over 20 mm windows (5 mm stride) of window RMS distance to the window's own plane / 20 mm
             (0 derivatives, local)
  tors       mean |torsion| where curvature >= 0.1 x vessel max, 1/mm       (3 derivatives, comparator)
Noise floor: a planar 100 mm arc (R 40 mm) with corr05 / iid05 noise, 20 reps, gives each metric's value for
a vessel with zero true out-of-plane shape.
Output: OUT/planarity_train<n>.csv and OUT/planarity_train<n>.txt. Disease is never read.
"""
import argparse
import csv
import os

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from tortuosity.vessels import ARTERIES, load_vessels
from .analyze import ci, icc
from .bishop import H, arc_chord, arc_resample, kappa_a, seglen
from .cohort import MIN_MM, OUT, perturb, start_point

CANDS = ("nonpl", "plane_rms", "plane_ang", "winpl20", "tors")
FAMS = ("iid006", "iid05", "corr05", "trunc20")
WIN, STRIDE = 20.0, 5.0


def _plane(X):
    c = X - X.mean(0)
    _, s, vt = np.linalg.svd(c, full_matrices=False)
    return s ** 2, vt[2], c


def planarity(P):
    C = arc_resample(P)
    L = seglen(C).sum()
    eig, n3, c = _plane(C)
    d = c @ n3
    T = np.gradient(C, H, axis=0)
    T /= np.linalg.norm(T, axis=1, keepdims=True)
    w, st = int(WIN / H), int(STRIDE / H)
    win = []
    for i in range(0, len(C) - w + 1, st):
        _, nw, cw = _plane(C[i:i + w])
        win.append(np.sqrt(np.mean((cw @ nw) ** 2)) / WIN)
    d1 = np.gradient(C, H, axis=0); d2 = np.gradient(d1, H, axis=0); d3 = np.gradient(d2, H, axis=0)
    x = np.cross(d1, d2); xn = np.linalg.norm(x, axis=1)
    kap = xn / np.maximum(np.linalg.norm(d1, axis=1) ** 3, 1e-12)
    tau = (x * d3).sum(1) / np.maximum(xn ** 2, 1e-12)
    m = kap >= 0.1 * kap.max()
    return {"nonpl": eig[2] / eig.sum(),
            "plane_rms": np.sqrt(np.mean(d ** 2)) / L,
            "plane_ang": np.degrees(np.abs(np.arcsin(np.clip(T @ n3, -1, 1)))).mean(),
            "winpl20": np.mean(win) if win else np.nan,
            "tors": np.abs(tau[m]).mean()}


def metrics(P):
    return {"length": seglen(P).sum(), "arc_chord": arc_chord(P), "ka5": kappa_a(P, 5), **planarity(P)}


def compute(n):
    ids = [x.strip() for x in open(f"{os.environ['ImageCAS_X_data_path']}/filelist/train.txt") if x.strip()][:n]
    rows, fails = [], []
    for c in ids:
        try:
            V = load_vessels(c)
            sp = {side: start_point(c, side) for side in ("left", "right")}
        except Exception as e:
            fails.append((c, "all", repr(e)))
            continue
        for vi, name in enumerate(("LAD", "LCX", "RCA")):
            P = V.get(name)
            if P is None or seglen(P).sum() < MIN_MM:
                fails.append((c, name, f"missing or < {MIN_MM} mm"))
                continue
            s0 = sp[ARTERIES[name][1]]
            if len(s0) and np.linalg.norm(s0 - P[-1], axis=1).min() < np.linalg.norm(s0 - P[0], axis=1).min():
                P = P[::-1]
            rows.append({"case": c, "vessel": name, "family": "orig", "rep": 0, **metrics(P)})
            for fi, fam in enumerate(FAMS):
                for rep in range(1 if fam == "trunc20" else 3):
                    Q = perturb(P, fam, np.random.default_rng([42, int(c), vi, fi, rep]))
                    ok = seglen(Q).sum() >= MIN_MM
                    rows.append({"case": c, "vessel": name, "family": fam, "rep": rep, **(metrics(Q) if ok else {})})
    cols = sorted({k for r in rows for k in r}, key=lambda k: (k not in ("case", "vessel", "family", "rep"), k))
    with open(f"{OUT}/planarity_train{n}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, cols)
        w.writeheader()
        w.writerows(rows)
    return fails


def noise_floor():
    t = np.arange(0, 100, 0.45) / 40.0
    arc = np.c_[40 * np.cos(t), 40 * np.sin(t), 0 * t]
    out = {}
    for fam in ("iid05", "corr05"):
        vals = [planarity(perturb(arc, fam, np.random.default_rng([7, k]))) for k in range(20)]
        out[fam] = {m: np.median([v[m] for v in vals]) for m in CANDS}
    out["clean"] = {m: planarity(arc)[m] for m in CANDS}
    return out


def rank_r2(y, X):
    r = lambda a: pd.Series(a).rank().values
    A = np.c_[np.ones(len(y)), *[r(x) for x in X]]
    yr = r(y)
    res = yr - A @ np.linalg.lstsq(A, yr, rcond=None)[0]
    return 1 - res.var() / yr.var()


def report(n, fails):
    d = pd.read_csv(f"{OUT}/planarity_train{n}.csv")
    ft = pd.read_csv(f"{OUT}/cohort_train{n}.csv", usecols=["case", "vessel", "family", "rep", "f_twist"])
    d = d.merge(ft, on=["case", "vessel", "family", "rep"], how="left")
    o = d[d.family == "orig"]
    V = ("LAD", "LCX", "RCA")
    lines = [f"# first {n} train ids; measurable: {o.groupby('vessel').size().to_dict()}; failures {len(fails)}"]
    pr = lines.append

    pr("\n## A. distributions on orig (median [5th, 95th]) LAD | LCX | RCA")
    for m in CANDS:
        pr(f"  {m:14s} " + " | ".join(
            f"{o[o.vessel == v][m].median():.4g} [{o[o.vessel == v][m].quantile(.05):.3g},{o[o.vessel == v][m].quantile(.95):.3g}]"
            for v in V))

    pr("\n## B. noise floor: planar 100 mm arc, true value 0 for every metric")
    for fam, vals in noise_floor().items():
        pr(f"  {fam:7s} " + "  ".join(f"{m} {x:.4g}" for m, x in vals.items()))

    pr("\n## C. ICC(2,1) [95% CI] between replicates, and vs-orig; LAD | LCX | RCA")
    for fam in FAMS[1:]:
        pr(f"### {fam}")
        for m in CANDS + ("ka5", "f_twist"):
            cells = []
            for v in V:
                pv = d[d.vessel == v].pivot_table(index="case", columns=["family", "rep"], values=m, dropna=False)
                if fam == "trunc20":
                    cells.append(ci(np.c_[pv["orig"].iloc[:, 0], pv[fam].iloc[:, 0]]))
                else:
                    reps = pv[fam].values
                    cells.append(f"{ci(reps)} vs-orig {icc(np.c_[pv['orig'].iloc[:, 0], reps[:, 0]]):.2f}")
            pr(f"  {m:14s} " + " | ".join(cells))

    pr("\n## D. redundancy on orig. Spearman with length, arc_chord, ka5, f_twist (LAD/LCX/RCA)")
    for c in CANDS:
        cells = []
        for ref in ("length", "arc_chord", "ka5", "f_twist"):
            cells.append(f"{ref} " + "/".join(f"{spearmanr(o[o.vessel == v][c], o[o.vessel == v][ref], nan_policy='omit')[0]:+.2f}" for v in V))
        pr(f"  {c:12s} " + "; ".join(cells))
    pr("  rank R^2 explained by (ka5, length) | by (ka5, length, arc_chord)   LAD/LCX/RCA")
    for c in CANDS + ("f_twist",):
        a = [o[o.vessel == v].dropna(subset=[c, "ka5"]) for v in V]
        pr(f"  {c:12s} " + "/".join(f"{rank_r2(x[c], [x.ka5, x.length]):.2f}" for x in a) + " | " +
           "/".join(f"{rank_r2(x[c], [x.ka5, x.length, x.arc_chord]):.2f}" for x in a))
    pr("  candidate x candidate Spearman, pooled over vessels within vessel ranks (median over LAD/LCX/RCA)")
    cs = CANDS + ("f_twist",)
    for i, a in enumerate(cs):
        pr(f"  {a:12s} " + " ".join(
            f"{np.median([spearmanr(o[o.vessel == v][a], o[o.vessel == v][b], nan_policy='omit')[0] for v in V]):+.2f}"
            for b in cs))
    pr("  (column order: " + ", ".join(cs) + ")")

    text = "\n".join(lines)
    with open(f"{OUT}/planarity_train{n}.txt", "w") as fh:
        fh.write(text + "\n")
        fh.writelines(f"# failed {a}\t{b}\t{e}\n" for a, b, e in fails)
    print(text)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=150)
    a = ap.parse_args()
    report(a.n, compute(a.n))
