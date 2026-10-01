"""Does f_twist earn a slot in the risk model? Pre-declared gates, written before any number below was seen.

    python -m tortuosity.research.unified.ftwist_gates [--n 150]
Primary metric f_twist (bishop.bcs, lam_c 20, W 5, on the delivered centerline with no extra smoothing;
amended 2026-09-30, originally f_twist@2 at sigma0 2 mm with f_twist@3 as sensitivity variant).
Comparators: ka5 (the locked primary) and nonpl (whole-vessel PCA non-planarity, the zero-derivative
out-of-plane rival).
Vessels LAD, LCX, RCA, oriented and filtered exactly as cohort.py.

G1 noise tolerance (first n train ids). Jitter of per-coordinate SD s in NOISE mm, iid per point or
   white noise Gaussian-filtered over 1 mm of arc then rescaled (corr), 2 reps, seed [42, case, vessel,
   family, level, rep]. Reported: ICC(2,1) vs orig (rep 0) and the tolerance s* = largest level whose
   vs-orig ICC is still >= 0.75 on all three vessels.
   PASS: vs-orig ICC >= 0.75 at s = 0.2 mm in both families on all three vessels.
G2 not a proxy for something else (all 560 train ids, orig only; Image Quality and Dominance from
   Descriptors.xlsx; Disease is never read).
   PASS: rank R^2 of f_twist on (ka5, length, nonpl) <= 0.5 on every vessel, AND
         |Spearman(f_twist, Image Quality)| <= 0.15 on every vessel (a noise reader rises as quality falls).
   Dominance medians are reported, not gated: dominance is anatomy, not an artefact.
G3 outcome (not run here, needs an explicit decision to unblind Disease): on train only, repeated
   stratified 5-fold CV logistic regression, base (ka5, log length per vessel, dominance) vs base +
   f_twist per vessel; PASS iff the 95 % CI of the CV delta-AUC excludes 0. val and test stay untouched.
G4 extractor (needs CAS-Net predictions and a centerline extractor, neither exists yet): ICC of f_twist
   between delivered and CAS-Net-derived centerlines >= 0.75, which replaces G1's assumed 0.2 mm with the
   measured error.
Output: OUT/ftwist_gates_train<n>.csv (G1), OUT/ftwist_gates_train_all.csv (G2), OUT/ftwist_gates_train<n>.txt.
"""
import argparse
import csv
import os

import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d
from scipy.stats import spearmanr

from tortuosity.vessels import ARTERIES, load_vessels
from .analyze import ci, icc
from .bishop import arc_resample, bcs, kappa_a, seglen
from .cohort import MIN_MM, OUT, start_point
from .planarity import _plane, rank_r2

NOISE = (0.06, 0.1, 0.15, 0.2, 0.3, 0.5)
FAMS = ("iid", "corr")
V = ("LAD", "LCX", "RCA")
METRICS = ("f_twist", "ka5", "nonpl")


def jitter(P, fam, s, rng):
    n = rng.normal(0, 1, P.shape)
    if fam == "corr":
        n = gaussian_filter1d(n, 1.0 / seglen(P).mean(), axis=0, mode="nearest")
        n /= n.std(0)
    return P + s * n


def metrics(P):
    eig, _, _ = _plane(arc_resample(P))
    return {"length": seglen(P).sum(), "ka5": kappa_a(P, 5), "nonpl": eig[2] / eig.sum(),
            "f_twist": bcs(P)["f_twist"]}


def vessels(c):
    Vs = load_vessels(c)
    sp = {side: start_point(c, side) for side in ("left", "right")}
    for vi, name in enumerate(V):
        P = Vs.get(name)
        if P is None or seglen(P).sum() < MIN_MM:
            continue
        s0 = sp[ARTERIES[name][1]]
        if len(s0) and np.linalg.norm(s0 - P[-1], axis=1).min() < np.linalg.norm(s0 - P[0], axis=1).min():
            P = P[::-1]
        yield vi, name, P


def compute(ids, noisy, path):
    rows, fails = [], []
    for c in ids:
        try:
            for vi, name, P in vessels(c):
                rows.append({"case": c, "vessel": name, "family": "orig", "level": 0, "rep": 0, **metrics(P)})
                for fi, fam in enumerate(FAMS if noisy else ()):
                    for li, s in enumerate(NOISE):
                        for rep in range(2):
                            Q = jitter(P, fam, s, np.random.default_rng([42, int(c), vi, fi, li, rep]))
                            rows.append({"case": c, "vessel": name, "family": fam, "level": s, "rep": rep, **metrics(Q)})
        except Exception as e:
            fails.append(f"{c}\t{e!r}")
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return fails


def report(n, fails):
    g1 = pd.read_csv(f"{OUT}/ftwist_gates_train{n}.csv")
    g2 = pd.read_csv(f"{OUT}/ftwist_gates_train_all.csv")
    desc = pd.read_excel(f"{os.environ['ImageCAS_X_data_path']}/Descriptors.xlsx", usecols=["Scan ID", "Image Quality", "Dominance"])
    g2 = g2.merge(desc.rename(columns={"Scan ID": "case"}), on="case", how="left")
    lines = [f"# G1 first {n} train ids, G2 {g2.case.nunique()} train ids; failures {len(fails)}"]
    pr = lines.append

    pr("\n## G1. ICC(2,1) vs orig by jitter SD (mm), LAD/LCX/RCA; s* = largest level with ICC >= 0.75 on all vessels")
    verdict = {}
    for fam in FAMS:
        pr(f"### {fam}   levels " + " ".join(f"{s:g}" for s in NOISE))
        for m in METRICS:
            cells, ok = [], []
            for s in NOISE:
                r = []
                for v in V:
                    pv = g1[(g1.vessel == v) & g1.family.isin(["orig", fam]) & g1.level.isin([0, s])].pivot_table(
                        index="case", columns=["family", "rep"], values=m)
                    r.append(icc(np.c_[pv["orig"].iloc[:, 0], pv[fam].iloc[:, 0]]))
                cells.append("/".join(f"{x:.2f}" for x in r))
                ok.append(min(r) >= 0.75)
            star = max([s for s, k in zip(NOISE, ok) if k], default=0)
            verdict[(m, fam)] = ok[NOISE.index(0.2)]
            pr(f"  {m:10s} " + "  ".join(cells) + f"   s* {star:g}")
        pr(f"  replicate ICC at 0.2 mm (both noisy reps, CI), f_twist: " + " | ".join(
            ci(g1[(g1.vessel == v) & (g1.family == fam) & (g1.level == 0.2)].pivot(index="case", columns="rep", values="f_twist").values)
            for v in V))
    pr("  G1 PASS at 0.2 mm (iid, corr): " + "; ".join(f"{m} {verdict[(m, 'iid')]}/{verdict[(m, 'corr')]}" for m in METRICS))

    pr("\n## G2. orig, all train. rank R^2 on (ka5, length, nonpl); Spearman with Image Quality; LAD/LCX/RCA")
    o = {v: g2[g2.vessel == v].dropna(subset=list(METRICS)) for v in V}
    for m in METRICS:
        refs = [r for r in ("ka5", "length", "nonpl") if r != m]
        r2 = [rank_r2(o[v][m], [o[v][r] for r in refs]) for v in V]
        iq = [spearmanr(o[v][m], o[v]["Image Quality"])[0] for v in V]
        pr(f"  {m:10s} R^2 on ({', '.join(refs)}) " + "/".join(f"{x:.2f}" for x in r2)
           + "   rho IQ " + "/".join(f"{x:+.2f}" for x in iq)
           + ("" if not m.startswith("f_twist") else f"   PASS {max(r2) <= 0.5 and max(map(abs, iq)) <= 0.15}"))
    pr("  median by Image Quality 1/2/3/4 (n per level: "
       + "/".join(str(k) for k in o["LAD"]["Image Quality"].value_counts().sort_index().values) + ")")
    for m in ("f_twist", "ka5"):
        pr(f"  {m:10s} " + " | ".join(
            v + " " + "/".join(f"{x:.3g}" for x in o[v].groupby("Image Quality")[m].median().values) for v in V))
    pr("  f_twist median by Dominance R/L/Co: " + " | ".join(
        v + " " + "/".join(f"{o[v][o[v].Dominance == d]['f_twist'].median():.3f}" for d in ("R", "L", "Co")) for v in V))

    text = "\n".join(lines)
    with open(f"{OUT}/ftwist_gates_train{n}.txt", "w") as fh:
        fh.write(text + "\n")
        fh.writelines(f"# failed {f}\n" for f in fails)
    print(text)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=150)
    n = ap.parse_args().n
    ids = [x.strip() for x in open(f"{os.environ['ImageCAS_X_data_path']}/filelist/train.txt") if x.strip()]
    os.makedirs(OUT, exist_ok=True)
    fails = compute(ids[:n], True, f"{OUT}/ftwist_gates_train{n}.csv")
    fails += compute(ids, False, f"{OUT}/ftwist_gates_train_all.csv")
    report(n, fails)
