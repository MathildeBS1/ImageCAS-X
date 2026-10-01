"""Advanced tortuosity descriptors for two RCAs (training scans 662 and 518), a worked case study.

    source env.sh; python -m tortuosity.research.case_study.advanced

Input: only the delivered centerlines ($ImageCAS_X_data_path/centerlines/{id}.coronary_right_centerline.vtk),
RCA = segment label 9, longest labelled geodesic path (tortuosity/vessels.py, as in
research/simple/compute_simple.py), oriented ostium -> distal with the file's start_points.

One curve per case: C0 = C = delivered centerline, arc-length resampled at H = 0.25 mm, no extra
smoothing (the file already carries a 0.5 mm Gaussian smoothing). Used for everything, including
the derivatives (psi, tangent indicatrix, turns, persistence).
Outputs in /work3/s254124/imagecasx_results/tortuosity_research/case_study/:
  advanced_metrics.json, advanced_pointwise.npz, srvf_warp.png, advanced.log
"""
import json
import os

import matplotlib
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import minimize

from tortuosity.research.unified.bishop import H, arc_resample, bcs, bishop_psi, seglen
from tortuosity.research.unified.cohort import start_point
from tortuosity.vessels import longest_path, read

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

DATA = os.environ["ImageCAS_X_data_path"]
RES = "/work3/s254124/imagecasx_results/tortuosity_research"
OUT = f"{RES}/case_study"
IDS = ("662", "518")
W = 5.0                       # mm, local-plane window (BCS W)
DELTAS = (2, 5, 10, 20, 40)   # mm, multiscale arc/chord windows


def load_rca(cid):
    pts, label, edges = read(f"{DATA}/centerlines/{cid}.coronary_right_centerline.vtk")
    m = (label[edges[:, 0]] == 9) & (label[edges[:, 1]] == 9)
    P = longest_path(pts, edges[m])
    sp = start_point(cid, "right")
    if np.linalg.norm(sp - P[-1], axis=1).min() < np.linalg.norm(sp - P[0], axis=1).min():
        P = P[::-1]
    return P


def tangents(C):
    T = np.gradient(C, H, axis=0)
    return T / np.linalg.norm(T, axis=1, keepdims=True)


def gauss(x, sd):
    return gaussian_filter1d(x, sd / H, mode="reflect")


def local_axis(psi, w=W):
    """Local dominant bending direction e^{i phi(s)} over a Gaussian window, phi continuous in s."""
    q = gauss(psi.real ** 2 - psi.imag ** 2, w) + 1j * gauss(2 * psi.real * psi.imag, w)
    return np.exp(0.5j * np.unwrap(np.angle(q))), q


def turn_barcode(psi):
    """Constant-sign turns of the curvature component along the continuous local bending axis.
    Planar curve: exactly Grisan's constant-sign turns. Angle = total turning int |psi| ds."""
    ax, _ = local_axis(psi)
    ks = (psi * np.conj(ax)).real
    sgn = np.sign(ks)
    cut = np.r_[0, np.flatnonzero(sgn[1:] != sgn[:-1]) + 1, len(ks)]
    s = np.arange(len(ks)) * H
    return np.array([[s[a], s[b - 1], np.degrees(H * np.abs(psi[a:b]).sum())] for a, b in zip(cut[:-1], cut[1:])]), ks


def indicatrix(T):
    ang = np.arccos(np.clip((T[1:] * T[:-1]).sum(1), -1, 1))
    rbar = np.linalg.norm(T.mean(0))
    # smallest spherical cap containing every tangent (minimax angle), multistart on the sphere
    f = lambda v: np.arccos(np.clip(T @ (v / np.linalg.norm(v)), -1, 1)).max()
    rng = np.random.default_rng(0)
    starts = np.vstack([T.mean(0), rng.normal(size=(40, 3))])
    best = min((minimize(f, x0, method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-8, maxiter=4000))
                for x0 in starts), key=lambda r: r.fun)
    # coverage: fraction of the sphere within 10 deg of the indicatrix (Fibonacci grid, 20000 points)
    n = 20000
    k = np.arange(n) + 0.5
    z, ph = 1 - 2 * k / n, np.pi * (1 + 5 ** 0.5) * k
    G = np.c_[np.sqrt(1 - z * z) * np.cos(ph), np.sqrt(1 - z * z) * np.sin(ph), z]
    cover = ((G @ T[::2].T).max(1) >= np.cos(np.radians(10))).mean()
    octs = np.unique((T > 0) @ [4, 2, 1], return_counts=True)
    n_oct = int((octs[1] * H >= 1.0).sum())  # octants holding >= 1 mm of arc
    ev, evec = np.linalg.eigh(T.T @ T / len(T))
    return dict(total_turn_deg=np.degrees(ang.sum()), rbar=rbar, cap_deg=np.degrees(best.fun),
                cover=cover, n_oct=n_oct, out_plane=ev[0], plane_normal=evec[:, 0])


def writhe_acn(C0, seg=1.0):
    """Open-curve writhe and average crossing number, exact segment-pair Gauss integral
    (Klenin and Langowski 2000) on the polyline with ~1 mm segments."""
    V = C0[::int(round(seg / H))]
    p1, p2 = V[:-1], V[1:]
    n = len(p1)
    i, j = np.triu_indices(n, 2)
    a, b, c, d = p1[i], p2[i], p1[j], p2[j]
    r13, r14, r23, r24 = c - a, d - a, c - b, d - b
    nv = lambda x, y: (lambda z: z / np.maximum(np.linalg.norm(z, axis=1, keepdims=True), 1e-15))(np.cross(x, y))
    n1, n2, n3, n4 = nv(r13, r14), nv(r14, r24), nv(r24, r23), nv(r23, r13)
    asn = lambda x, y: np.arcsin(np.clip((x * y).sum(1), -1, 1))
    om = asn(n1, n2) + asn(n2, n3) + asn(n3, n4) + asn(n4, n1)
    om *= np.sign((np.cross(d - c, b - a) * r13).sum(1))
    return 2 * om.sum() / (4 * np.pi), 2 * np.abs(om).sum() / (4 * np.pi)


def ti_multiscale(C0, delta):
    k = int(round(delta / H))
    if k >= len(C0):
        return np.nan, np.nan, np.nan, None
    ch = np.linalg.norm(C0[k:] - C0[:-k], axis=1)
    ti = delta / ch - 1
    centre = np.full(len(C0), np.nan)
    centre[k // 2:k // 2 + len(ti)] = ti
    return ti.mean(), ti.max(), (np.argmax(ti) + k / 2) * H, centre


def peak_persistence(f):
    """H0 persistence of superlevel sets of a 1D function: (birth=peak, death=merge level) per peak."""
    order = np.argsort(-f)
    parent = -np.ones(len(f), int)
    peak = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    pairs = []
    for x in order:
        parent[x] = x
        peak[x] = f[x]
        for y in (x - 1, x + 1):
            if 0 <= y < len(f) and parent[y] >= 0:
                rx, ry = find(x), find(y)
                if rx == ry:
                    continue
                lo, hi = (rx, ry) if peak[rx] < peak[ry] else (ry, rx)
                if peak[lo] > f[x]:
                    pairs.append((peak[lo], f[x]))
                parent[lo] = hi
    pairs.append((f.max(), f.min()))
    return np.array(pairs)


def box_dim(C0, eps=(1, 2, 4, 8, 16)):
    rng = np.random.default_rng(0)
    N = [np.mean([len(np.unique(np.floor((C0 + rng.uniform(0, e, 3)) / e), axis=0)) for _ in range(20)]) for e in eps]
    return -np.polyfit(np.log(eps), np.log(N), 1)[0]


# ---------------- SRVF (Srivastava et al. 2011), unit-length curves, q = T for arc-length sampling ----------------

def srvf(C0, n=200):
    a = np.r_[0, np.cumsum(seglen(C0))]
    t = np.linspace(0, a[-1], n)
    X = np.column_stack([np.interp(t, a, C0[:, k]) for k in range(3)]) / a[-1]
    d = np.diff(X, axis=0) * (n - 1)
    q = d / np.sqrt(np.linalg.norm(d, axis=1, keepdims=True))  # (n-1, 3) at interval midpoints
    return q / np.sqrt((q * q).sum(1).mean())  # unit L2 norm (chords are slightly shorter than arcs)


def dist_to_line(q):
    """Elastic: closed form arccos sqrt(max_e int (q.e)_+^2) (line reparametrisation may stall where q.e < 0).
    Non-elastic (arc-length fixed, rotation only): arccos |int q|."""
    f = lambda v: -(np.clip(q @ (v / np.linalg.norm(v)), 0, None) ** 2).mean()
    rng = np.random.default_rng(0)
    best = min((minimize(f, x0, method="Nelder-Mead") for x0 in np.vstack([q.mean(0), rng.normal(size=(20, 3))])),
               key=lambda r: r.fun)
    return np.arccos(np.sqrt(-best.fun)), np.arccos(np.linalg.norm(q.mean(0)))


def dp_warp(q1, q2, m=6):
    """gamma maximising int <q1(t), q2(gamma(t))> sqrt(gamma'(t)) dt; piecewise linear on the grid,
    slopes dj/di with di, dj in 1..m (Srivastava et al. DP)."""
    n = len(q1) + 1
    x = np.arange(n - 1) + 0.5  # q samples live at interval midpoints

    def q2at(u):
        return np.column_stack([np.interp(u, x, q2[:, k]) for k in range(3)])
    Wt = {}
    for di in range(1, m + 1):
        for dj in range(1, m + 1):
            sl = dj / di
            v = np.zeros((n - di, n - dj))
            for u in range(di):
                a = q1[u:n - di + u]                                  # q1 on [i+u, i+u+1]
                b = q2at(np.arange(n - dj) + sl * (u + 0.5))
                v += a @ b.T
            Wt[di, dj] = v * np.sqrt(sl) / (n - 1)
    E = np.full((n, n), -np.inf)
    E[0, 0] = 0
    arg = np.zeros((n, n, 2), int)
    for k in range(1, n):
        for (di, dj), v in Wt.items():
            if k - di < 0:
                continue
            cand = np.full(n, -np.inf)
            cand[dj:] = E[k - di, :n - dj] + v[k - di, :]
            better = cand > E[k]
            E[k, better] = cand[better]
            arg[k, better] = (di, dj)
    path = [(n - 1, n - 1)]
    while path[-1] != (0, 0):
        k, l = path[-1]
        di, dj = arg[k, l]
        path.append((k - di, l - dj))
    path = np.array(path[::-1]) / (n - 1)
    return E[-1, -1], path


def elastic_distance(q1, q2, iters=6, rotate=True):
    O = np.eye(3)
    for _ in range(iters):
        ip, path = dp_warp(q1, q2 @ O.T)
        if not rotate:
            break
        t = (np.arange(len(q1)) + 0.5) / len(q1)
        g = np.interp(t, path[:, 0], path[:, 1])
        dg = np.gradient(g, t)
        q2g = np.column_stack([np.interp(g * len(q2) - 0.5, np.arange(len(q2)), q2[:, k]) for k in range(3)]) \
            * np.sqrt(np.clip(dg, 0, None))[:, None]
        U, _, Vt = np.linalg.svd(q1.T @ q2g)
        O = U @ np.diag([1, 1, np.sign(np.linalg.det(U @ Vt))]) @ Vt
    ip, path = dp_warp(q1, q2 @ O.T)
    return np.arccos(np.clip(ip, -1, 1)), path, O


def pct(ref, v):
    ref = np.asarray(ref, float)
    ref = ref[np.isfinite(ref)]
    return float(100 * ((ref < v).sum() + 0.5 * (ref == v).sum()) / len(ref))


def main():
    simple = pd.read_csv(f"{RES}/simple/simple_measures.csv", dtype={"id": str})
    simple = simple[(simple.vessel == "RCA") & ~simple.missing.astype(bool)]
    uni = pd.read_csv(f"{RES}/unified/cohort_train150.csv", dtype={"case": str})
    uni = uni[(uni.vessel == "RCA") & (uni.family == "orig")]
    log = [f"reference n: simple RCA {len(simple)}, BCS cohort RCA {len(uni)} "
           f"(cases in BCS cohort: {sorted(set(IDS) & set(uni.case))})"]
    res, npz, qs = {}, {}, {}
    for cid in IDS:
        P = load_rca(cid)
        C0 = C = arc_resample(P)
        L = H * (len(C) - 1)
        T = tangents(C)
        psi = bishop_psi(C)
        psi *= np.exp(-0.5j * np.angle((psi ** 2).sum()))  # global phase: dominant bending along k1
        b = bcs(P)
        ind = indicatrix(T)
        wr, acn = writhe_acn(C0)
        tb, ks = turn_barcode(psi)
        ax, q = local_axis(psi)
        ga = gauss(np.abs(psi) ** 2, W)
        tw_loc = 1 - np.abs(q) / np.maximum(ga, 1e-12)
        per = peak_persistence(np.abs(psi))
        pers = per[:, 0] - per[:, 1]
        qs[cid] = srvf(C0)
        dl_el, dl_l2 = dist_to_line(qs[cid])
        ms = {d: ti_multiscale(C0, d) for d in DELTAS}
        L0, D0 = seglen(C0).sum(), np.linalg.norm(C0[-1] - C0[0])
        sr = simple[simple.id == cid].iloc[0]
        ur = uni[uni.case == cid]
        up = lambda k, v: pct(uni[k], v)
        sp = lambda k, v: pct(simple[k], v)
        big = tb[tb[:, 2] >= 20]
        m = [
            ("baseline arc/chord L/D (compute_simple)", sr.DM, "-", sp("DM", sr.DM),
             "whole-vessel path length over end-to-end distance"),
            ("baseline kappa_a at 5 mm chord", sr.kappa_a5, "mm^-1", sp("kappa_a5", sr.kappa_a5),
             "mean turning per mm at a 5 mm chord"),
            ("BCS kB", b["kB"], "mm^-1", up("kB", b["kB"]),
             "RMS curvature: square root of bending energy per mm"),
            ("BCS kB_course (lambda_c 20 mm)", b["kB_course"], "mm^-1", up("kB_course", b["kB_course"]),
             "RMS curvature carried by wavelengths longer than 20 mm (the vessel's overall course)"),
            ("BCS kB_wiggle (lambda_c 20 mm)", b["kB_wiggle"], "mm^-1", up("kB_wiggle", b["kB_wiggle"]),
             "RMS curvature carried by wavelengths shorter than 20 mm (local bends)"),
            ("BCS f_wiggle", b["f_wiggle"], "fraction", up("f_wiggle", b["f_wiggle"]),
             "share of bending energy in short-wavelength bends rather than the course"),
            ("BCS f_twist (W 5 mm)", b["f_twist"], "fraction", up("f_twist", b["f_twist"]),
             "share of bending energy outside the locally dominant bending plane (12 mm FWHM window)"),
            ("tangent indicatrix length (total turning)", ind["total_turn_deg"], "deg", None,
             "total angle the direction of travel sweeps from ostium to distal end"),
            ("tangent resultant length |mean T|", ind["rbar"], "-", None,
             "1 = all tangents point one way; 0 = directions cancel (equals D/L)"),
            ("tangent smallest enclosing cap half-angle", ind["cap_deg"], "deg", None,
             "every direction the vessel takes lies within this angle of one axis; > 90 means no hemisphere holds them"),
            ("tangent sphere coverage within 10 deg", ind["cover"], "fraction of sphere", None,
             "how much of the sphere of directions the vessel visits"),
            ("tangent octants visited (LPS axes, >= 1 mm each)", ind["n_oct"], "count of 8", None,
             "how many of the 8 LPS sign-combinations of direction the vessel travels in"),
            ("tangent out-of-plane variance (smallest eigenvalue of <T T^T>)", ind["out_plane"], "fraction", None,
             "0 = tangents on one great circle (planar course); 1/3 = isotropic; normal "
             f"({ind['plane_normal'][0]:+.2f}, {ind['plane_normal'][1]:+.2f}, {ind['plane_normal'][2]:+.2f}) LPS"),
            ("writhe (open curve, 1 mm segments)", wr, "-", None,
             "signed mean self-crossing count over all viewing directions: net 3D coiling handedness"),
            ("average crossing number (ACN)", acn, "-", None,
             "unsigned mean self-crossings over all views: how often the vessel overlaps itself in a projection"),
        ]
        for d in DELTAS:
            mean, mx, at, _ = ms[d]
            m.append((f"multiscale arc/chord TI({d} mm), mean", mean, "-", None,
                      f"mean (arc/chord - 1) over all {d} mm windows"))
            m.append((f"multiscale arc/chord TI({d} mm), max", mx, "-", None,
                      f"most tortuous {d} mm window, centred at s = {at:.1f} mm from the ostium"))
        m.append(("whole-vessel TI = L/D - 1", L0 / D0 - 1, "-", None,
                  "TI at Delta = full length"))
        kap = np.abs(psi)
        m += [
            ("mean curvature on C (total turning / L)", kap.mean(), "mm^-1", None,
             "mean |kappa|, the continuous analogue of kappa_a"),
            ("curvature peakedness kB / mean kappa", b["kB"] / kap.mean(), "-", None,
             "RMS over mean curvature: 1 = bending spread evenly, larger = concentrated in a few sharp bends"),
            ("maximum curvature", kap.max(), "mm^-1", None,
             f"sharpest point (radius {1 / kap.max():.1f} mm) at s = {kap.argmax() * H:.1f} mm"),
            ("arc length with kappa > 0.1 (radius < 10 mm)", H * (kap > 0.1).sum(), "mm", None,
             "how much of the vessel is in a tight bend"),
            ("turn barcode: turns (all)", len(tb), "count", None, "constant-sign turns along the local bending axis"),
            ("turn barcode: turns >= 20 deg", int((tb[:, 2] >= 20).sum()), "count", None, "turns of at least 20 deg"),
            ("turn barcode: turns >= 45 deg", int((tb[:, 2] >= 45).sum()), "count", None, "turns of at least 45 deg"),
            ("turn barcode: turns >= 90 deg", int((tb[:, 2] >= 90).sum()), "count", None, "turns of at least 90 deg"),
            ("turn barcode: largest turn", tb[:, 2].max(), "deg", None,
             f"largest single turn, s {tb[tb[:, 2].argmax(), 0]:.1f} to {tb[tb[:, 2].argmax(), 1]:.1f} mm"),
            ("turn barcode: mean length of turns >= 20 deg", (big[:, 1] - big[:, 0]).mean() if len(big) else np.nan,
             "mm", None, "typical arc length of one bend"),
            ("curvature persistence: peaks with persistence >= 0.02", int((pers >= 0.02).sum()), "count", None,
             "curvature peaks standing at least 0.02 mm^-1 above the saddle that joins them to a higher peak"),
            ("curvature persistence: peaks with persistence >= 0.05", int((pers >= 0.05).sum()), "count", None,
             "sharp bends (peak at least 0.05 mm^-1 above its saddle)"),
            ("curvature persistence: total persistence", pers.sum(), "mm^-1", None,
             "sum of peak prominences of kappa(s)"),
            ("box-counting dimension (1 to 16 mm boxes)", box_dim(C0), "-", None,
             "1 = smooth line at these scales; > 1 = the curve fills space more densely"),
            ("SRVF elastic distance to a straight line", dl_el, "rad", None,
             "elastic shape distance (unit length) to a straight segment, 0 = straight, pi/2 = maximal"),
            ("SRVF L2 distance to a straight line (no warping)", dl_l2, "rad", None,
             "same without reparametrisation, = arccos(D/L) for arc-length curves"),
        ]
        a0 = np.r_[0, np.cumsum(seglen(P))]
        bt = bcs(P[a0 >= 5.0])  # sensitivity: first 5 mm (ostial take-off) removed
        m += [("BCS kB, first 5 mm removed", bt["kB"], "mm^-1", None,
               "kB without the ostial take-off; percentile omitted (cohort is untrimmed)"),
              ("BCS f_twist, first 5 mm removed", bt["f_twist"], "fraction", None,
               "f_twist without the ostial take-off"),
              ("BCS f_wiggle, first 5 mm removed", bt["f_wiggle"], "fraction", None,
               "f_wiggle without the ostial take-off")]
        res[cid] = [dict(name=a, value=None if v is None or (isinstance(v, float) and np.isnan(v)) else float(v),
                         unit=u, percentile=None if p is None else round(p, 1), meaning=mm)
                    for a, v, u, p, mm in m]
        npz.update({f"{cid}_xyz": C, f"{cid}_s": np.arange(len(C)) * H, f"{cid}_k1": psi.real, f"{cid}_k2": psi.imag,
                    f"{cid}_twist_local": tw_loc, f"{cid}_turns": tb, f"{cid}_tangent": T,
                    f"{cid}_ti10": ms[10][3],
                    f"{cid}_signed_k": ks})
        log.append(f"{cid}: L {L:.1f} mm, N {len(C)}, BCS {b}")
    # pairwise elastic distance with and without rotation, and anatomical frame
    d_rot, path, O = elastic_distance(qs["662"], qs["518"])
    d_anat, path_a, _ = elastic_distance(qs["662"], qs["518"], rotate=False)
    d_id = np.arccos(np.clip((qs["662"] * qs["518"]).sum(1).mean(), -1, 1))
    ang = np.degrees(np.arccos(np.clip((np.trace(O) - 1) / 2, -1, 1)))
    for cid in IDS:
        res[cid] += [
            dict(name="SRVF elastic distance 662 vs 518 (rotation + warping)", value=float(d_rot), unit="rad",
                 percentile=None, meaning=f"shape distance after best rotation ({ang:.0f} deg) and reparametrisation"),
            dict(name="SRVF elastic distance 662 vs 518 (anatomical frame, warping only)", value=float(d_anat),
                 unit="rad", percentile=None, meaning="shape distance in the shared LPS frame, only arc-length warped"),
            dict(name="SRVF distance 662 vs 518 (no rotation, no warping)", value=float(d_id), unit="rad",
                 percentile=None, meaning="direction mismatch at equal fractional arc length"),
        ]
    npz.update(warp_662_to_518=path, warp_662_to_518_anat=path_a)
    os.makedirs(OUT, exist_ok=True)
    json.dump(res, open(f"{OUT}/advanced_metrics.json", "w"), indent=1)
    np.savez(f"{OUT}/advanced_pointwise.npz", **npz)
    fig, a = plt.subplots(figsize=(4, 4))
    a.plot([0, 1], [0, 1], "k:", lw=0.8)
    a.plot(path[:, 0], path[:, 1], label=f"rotation + warp, d = {d_rot:.3f}")
    a.plot(path_a[:, 0], path_a[:, 1], label=f"LPS frame, d = {d_anat:.3f}")
    a.set_xlabel("fraction of arc length, 662")
    a.set_ylabel("matched fraction of arc length, 518")
    a.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(f"{OUT}/srvf_warp.png", dpi=150)
    log.append(f"SRVF: rot {d_rot:.4f} (rotation {ang:.1f} deg), anat {d_anat:.4f}, identity {d_id:.4f}")
    open(f"{OUT}/advanced.log", "w").write("\n".join(log) + "\n")
    print("\n".join(log))
    for cid in IDS:
        print(f"--- {cid}")
        for r in res[cid]:
            print(f"{r['name'][:62]:62s} {r['value'] if r['value'] is None else round(r['value'], 4)!s:>10} "
                  f"{r['unit']:>8} p={r['percentile']}")


if __name__ == "__main__":
    main()
