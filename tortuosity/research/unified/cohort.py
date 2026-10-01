"""Bishop curvature spectrum on ImageCAS-X TRAIN centerlines, with perturbation replicates.

    python -m tortuosity.research.unified.cohort [--n 150]
Sample: the first n ids of filelist/train.txt (default 150). Vessels LAD, LCX, RCA (tortuosity/vessels.py),
oriented proximal -> distal with the file's start_points. Perturbations (seed = [42, case, vessel, family, rep]):
  iid05  0.5 mm iid Gaussian per coordinate, 3 reps
  iid006 0.06 mm iid (the measured residual of the earlier reports), 3 reps
  corr05 0.5 mm, white noise Gaussian-filtered over 1 mm of arc then rescaled (earlier jit_pc05), 3 reps
  trunc20 distal 20 mm removed (1 rep); vessels with < 15 mm left give NaN
Output: /work3/s254124/imagecasx_results/tortuosity_research/unified/cohort_train<n>.csv (+ _failed.txt)
"""
import argparse
import csv
import os
import time

import numpy as np
from scipy.ndimage import gaussian_filter1d

from tortuosity.vessels import ARTERIES, load_vessels, start_point
from .bishop import arc_chord, bcs, kappa_a, seglen

OUT = "/work3/s254124/imagecasx_results/tortuosity_research/unified"
KEYS = ("kB", "kB_course", "kB_wiggle", "kB_planar", "kB_twist", "f_twist", "f_wiggle")
SENS = (("lc15", dict(lam_c=15)), ("lc30", dict(lam_c=30)), ("w10", dict(w_sd=10)), ("w2", dict(w_sd=2.5)))
MIN_MM = 15


def truncate(P, x):
    a = np.r_[0, np.cumsum(seglen(P))]
    keep = a < a[-1] - x
    end = np.array([np.interp(a[-1] - x, a, P[:, k]) for k in range(3)])
    return np.vstack([P[keep], end])


def perturb(P, fam, rng):
    if fam == "trunc20":
        return truncate(P, 20)
    s, corr = {"iid05": (0.5, 0), "iid006": (0.06, 0), "corr05": (0.5, 1.0)}[fam]
    n = rng.normal(0, 1, P.shape)
    if corr:
        n = gaussian_filter1d(n, corr / seglen(P).mean(), axis=0, mode="nearest")
        n /= n.std(0)
    return P + s * n


def metrics(P, sens=False):
    r = {"length": seglen(P).sum(), "arc_chord": arc_chord(P), "ka5": kappa_a(P, 5)}
    t0 = time.perf_counter()
    d = bcs(P)
    r["t_bcs_ms"] = 1e3 * (time.perf_counter() - t0)
    r.update({k: d[k] for k in KEYS})
    if sens:
        for tag, kw in SENS:
            d = bcs(P, **kw)
            r.update({f"{k}@{tag}": d[k] for k in KEYS})
    return r


def main(n):
    ids = [x.strip() for x in open(f"{os.environ['ImageCAS_X_data_path']}/filelist/train.txt") if x.strip()][:n]
    os.makedirs(OUT, exist_ok=True)
    rows, fails, t0 = [], [], time.time()
    for ci, c in enumerate(ids):
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
                rows.append({"case": c, "vessel": name, "family": "orig", "rep": 0})
                continue
            s0 = sp[ARTERIES[name][1]]
            if len(s0) and np.linalg.norm(s0 - P[-1], axis=1).min() < np.linalg.norm(s0 - P[0], axis=1).min():
                P = P[::-1]
            rows.append({"case": c, "vessel": name, "family": "orig", "rep": 0, **metrics(P, sens=True)})
            for fi, fam in enumerate(("iid05", "iid006", "corr05", "trunc20")):
                for rep in range(1 if fam == "trunc20" else 3):
                    Q = perturb(P, fam, np.random.default_rng([42, int(c), vi, fi, rep]))
                    ok = seglen(Q).sum() >= MIN_MM
                    rows.append({"case": c, "vessel": name, "family": fam, "rep": rep, **(metrics(Q) if ok else {})})
        if ci % 25 == 0:
            print(f"{ci}/{len(ids)} {time.time() - t0:.0f} s", flush=True)
    cols = sorted({k for r in rows for k in r}, key=lambda k: (k not in ("case", "vessel", "family", "rep"), k))
    with open(f"{OUT}/cohort_train{n}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, cols)
        w.writeheader()
        w.writerows(rows)
    with open(f"{OUT}/cohort_train{n}_failed.txt", "w") as fh:
        fh.writelines(f"{a}\t{b}\t{e}\n" for a, b, e in fails)
    print(f"{len(ids)} cases, {len(rows)} rows, {len(fails)} failures, {time.time() - t0:.0f} s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=150)
    main(ap.parse_args().n)
