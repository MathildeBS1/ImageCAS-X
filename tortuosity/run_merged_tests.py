"""Tests of the merged method against the criteria in tortuosity/CLAUDE.md.

    python -m tortuosity.run_merged_tests synthetic
    python -m tortuosity.run_merged_tests cohort [--split train] [--n 0]
    python -m tortuosity.run_merged_tests floor [--split train] [--n 200]

Thresholds are fixed here, before any cohort number was seen.
"""
import argparse
import csv
import os
import time

import numpy as np
from scipy.stats import spearmanr

from .merged import arc_chord, grisan3d, scc_density
from .vessels import load_vessels

LS = [2, 3, 4, 5, 6, 8]  # chord lengths, mm
L_REF, JITTER_SIGMA, JITTER_REPS = 4, 0.5, 5
MIN_RHO_STABLE = 0.8  # criterion 2: rank correlation across l in 3..6 vs l = 4
MIN_ICC = 0.75  # criterion 3
MAX_FLOOR = 0.2  # criterion 5: fraction of vessels scoring exactly 0
MAX_ABS_LENGTH_RHO = 0.5  # criterion 6
MIN_LENGTH_MM = 15


# ---------------- synthetic (criterion 1) ----------------

def curve(kind, n=400, **k):
    """Dense planar/space curves, ~0.25 mm spacing."""
    if kind == "line":
        s = np.linspace(0, 100, n)
        return np.c_[s, 0 * s, 0 * s]
    if kind == "sin":  # amplitude A, wavelength lam, length 100
        s = np.linspace(0, 100, n)
        return np.c_[s, k["A"] * np.sin(2 * np.pi * s / k["lam"]), 0 * s]
    if kind == "arcs":  # m alternating arcs of turning phi each, total arc length 60 mm
        m, phi = k["m"], k["phi"]
        R, ds = 60 / (m * phi), 0.25
        heading, p, out = 0.0, np.zeros(2), [np.zeros(2)]
        for a in range(m):
            for _ in range(int(60 / m / ds)):
                heading += (-1) ** a * ds / R
                p = p + ds * np.array([np.cos(heading), np.sin(heading)])
                out.append(p)
        out = np.array(out)
        return np.c_[out, 0 * out[:, 0]]
    if kind == "helix":  # radius r, pitch per turn, ~3 turns
        t = np.linspace(0, 6 * np.pi, n)
        return np.c_[k["r"] * np.cos(t), k["r"] * np.sin(t), k["pitch"] * t / (2 * np.pi)]


def rot(P, seed=0):
    Q, _ = np.linalg.qr(np.random.default_rng(seed).normal(size=(3, 3)))
    return P @ Q.T + 5.0


def synthetic():
    l = 4
    row = lambda name, P: print(f"  {name:34s} scc={scc_density(P, l):8.4f}  grisan={grisan3d(P, l)[0]:8.5f}"
                                f" (n={grisan3d(P, l)[1]})  arc/chord-1={arc_chord(P):7.4f}")
    print(f"l = {l} mm, kappa_floor default")
    print("line and invariance")
    row("line", curve("line"))
    P = curve("sin", A=4, lam=25)
    row("sinusoid A=4 lam=25", P)
    row("  same, rotated+translated", rot(P))
    print("amplitude sweep (lam=25): expect monotone increase")
    for A in (1, 2, 4, 6, 8):
        row(f"  A={A}", curve("sin", A=A, lam=25))
    print("frequency sweep (A=3): expect monotone increase")
    for lam in (50, 25, 15, 10):
        row(f"  lam={lam}", curve("sin", A=3, lam=lam))
    print("one wide arc vs several tight bends (60 mm of vessel)")
    for m, phi in ((1, np.pi / 2), (1, np.pi), (3, np.pi / 2), (5, np.pi / 2)):
        row(f"  {m} arc(s) of {np.degrees(phi):.0f} deg", curve("arcs", m=m, phi=phi))
    print("shapes the two outputs should disagree on")
    row("helix r=8 pitch=20", curve("helix", r=8, pitch=20))
    print("jitter on a straight 100 mm line (report: spurious density ~ 3 sigma / l^2)")
    rng = np.random.default_rng(0)
    for sigma in (0.25, 0.5):
        for ll in (2, 4, 5, 8):
            vals = [scc_density(curve("line", n=200) + rng.normal(0, sigma, (200, 3)), ll) for _ in range(20)]
            print(f"  sigma={sigma} l={ll}: scc={np.mean(vals):.4f}   predicted={3 * sigma / ll**2:.4f}")


# ---------------- cohort (criteria 2, 3, 5, 6) ----------------

def icc1(x):
    """One-way ICC(1,1); x is (vessels, replicates)."""
    n, k = x.shape
    msb = k * x.mean(1).var(ddof=1)
    msw = ((x - x.mean(1, keepdims=True)) ** 2).sum() / (n * (k - 1))
    return (msb - msw) / (msb + (k - 1) * msw)


def cohort(split, n_cases, out_dir):
    ids = [x.strip() for x in open(f"{os.environ['ImageCAS_X_data_path']}/filelist/{split}.txt") if x.strip()]
    ids = ids[:n_cases] if n_cases else ids
    os.makedirs(out_dir, exist_ok=True)
    rng = np.random.default_rng(42)
    cols = ["case", "vessel", "length_mm", "arc_chord"] + [f"{m}_{l}" for l in LS for m in ("scc", "gri", "turns")] \
        + [f"jit_{m}_{r}" for m in ("scc", "gri") for r in range(JITTER_REPS)]
    fails, rows, t0 = [], [], time.time()
    with open(f"{out_dir}/{split}_vessels.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for c in ids:
            try:
                vessels = load_vessels(c)
            except Exception as e:
                fails.append((c, "all", repr(e)))
                continue
            for name in ("LAD", "LCX", "RCA"):
                P = vessels.get(name)
                length = np.linalg.norm(np.diff(P, axis=0), axis=1).sum() if P is not None else 0
                if length < MIN_LENGTH_MM:
                    fails.append((c, name, f"missing or shorter than {MIN_LENGTH_MM} mm"))
                    continue
                r = [c, name, length, arc_chord(P)]
                for l in LS:
                    g, n = grisan3d(P, l)
                    r += [scc_density(P, l), g, n]
                J = [P + rng.normal(0, JITTER_SIGMA, P.shape) for _ in range(JITTER_REPS)]
                r += [scc_density(Q, L_REF) for Q in J] + [grisan3d(Q, L_REF)[0] for Q in J]
                w.writerow(r)
                rows.append(r)
    with open(f"{out_dir}/{split}_failed.txt", "w") as fh:
        fh.writelines(f"{a}\t{b}\t{c}\n" for a, b, c in fails)
    print(f"{split}: {len(ids)} cases, {len(rows)} vessels, {len(fails)} failures, {time.time() - t0:.0f} s")
    report(np.array(rows, dtype=object), cols)


def floor_sweep(split, n_cases):
    """How many twists Grisan 3D finds as the hysteresis floor rises, and how the ranking moves."""
    ids = [x.strip() for x in open(f"{os.environ['ImageCAS_X_data_path']}/filelist/{split}.txt") if x.strip()][:n_cases]
    V = [load_vessels(c) for c in ids]
    floors = (0.01, 0.02, 0.04, 0.06, 0.08, 0.12)
    for name in ("LAD", "LCX", "RCA"):
        Ps = [v[name] for v in V if name in v]
        res = {f: [grisan3d(P, L_REF, f) for P in Ps] for f in floors}
        ref = [g[0] for g in res[0.02]]
        print(f"{name} ({len(Ps)} vessels), l={L_REF}: floor -> median turns, turns per 100 mm, zero-fraction, rho vs floor 0.02")
        for f in floors:
            t = np.array([g[0] for g in res[f]])
            n = np.array([g[1] for g in res[f]])
            L = np.array([np.linalg.norm(np.diff(P, axis=0), axis=1).sum() for P in Ps])
            print(f"  {f:.2f}: {np.median(n):4.0f} {np.median(n / L * 100):5.1f} {np.mean(t == 0):.2f} {spearmanr(t, ref)[0]:.2f}")


def report(rows, cols):
    col = lambda k: rows[:, cols.index(k)].astype(float)
    names = rows[:, 1]
    for name in ("LAD", "LCX", "RCA"):
        m = names == name
        print(f"\n== {name}: {m.sum()} vessels, median length {np.median(col('length_mm')[m]):.0f} mm")
        for meth, key in (("SCC density", "scc"), ("Grisan 3D", "gri")):
            ref = col(f"{key}_{L_REF}")[m]
            rho = {l: spearmanr(col(f"{key}_{l}")[m], ref, nan_policy="omit")[0] for l in LS}
            floor = {l: np.mean(col(f"{key}_{l}")[m] == 0) for l in LS}
            icc = icc1(np.c_[[col(f"jit_{key}_{r}")[m] for r in range(JITTER_REPS)]].T)
            lrho = spearmanr(ref, col("length_mm")[m], nan_policy="omit")[0]
            stable = min(rho[l] for l in (3, 5, 6))
            print(f"  {meth:12s} rho vs l={L_REF}: " + " ".join(f"l{l}={rho[l]:.2f}" for l in LS)
                  + f"\n{'':15s}zero-fraction: " + " ".join(f"l{l}={floor[l]:.2f}" for l in LS)
                  + f"\n{'':15s}ICC(jitter {JITTER_SIGMA} mm, l={L_REF})={icc:.2f}  rho(length)={lrho:.2f}"
                  + f"\n{'':15s}PASS stable={stable >= MIN_RHO_STABLE} icc={icc >= MIN_ICC}"
                    f" floor={floor[L_REF] <= MAX_FLOOR} length={abs(lrho) <= MAX_ABS_LENGTH_RHO}")
        print(f"  Grisan n_turns at l={L_REF}: median {np.median(col(f'turns_{L_REF}')[m]):.0f}, "
              f"share with 1 turn {np.mean(col(f'turns_{L_REF}')[m] == 1):.2f}")
        print(f"  Spearman SCC vs Grisan: {spearmanr(col(f'scc_{L_REF}')[m], col(f'gri_{L_REF}')[m])[0]:.2f}; "
              f"SCC vs arc/chord: {spearmanr(col(f'scc_{L_REF}')[m], col('arc_chord')[m])[0]:.2f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["synthetic", "cohort", "floor"])
    ap.add_argument("--split", default="train")
    ap.add_argument("--n", type=int, default=0, help="first n cases only; 0 = all")
    ap.add_argument("--out", default=f"{os.environ.get('ImageCAS_X_results_path', '.')}/tortuosity_merged")
    a = ap.parse_args()
    if a.mode == "synthetic":
        synthetic()
    elif a.mode == "floor":
        floor_sweep(a.split, a.n or 200)
    else:
        cohort(a.split, a.n, a.out)
