"""Synthetic checks of the Bishop curvature spectrum (bishop.py).

    python -m tortuosity.research.unified.synthetic
Curves are built dense (0.05 mm) then sampled at RAW = 0.45 mm, the ImageCAS-X point spacing.
"""
import numpy as np
from scipy.ndimage import gaussian_filter1d

from .bishop import H, bcs, arc_resample, bishop_psi, band_split, kappa_a, arc_chord, seglen

RAW = 0.45


def from_heading(kappa_fn, L, ds=0.05, plane_fn=None):
    """Planar-by-parts curve from a signed curvature function of s (turning in the xy plane)."""
    s = np.arange(0, L, ds)
    th = np.cumsum(kappa_fn(s)) * ds
    P = np.c_[np.cumsum(np.cos(th)) * ds, np.cumsum(np.sin(th)) * ds, 0 * s]
    return P


def raw(P):
    return arc_resample(P, RAW) if True else P


def sine(A, lam, L=100):
    x = np.arange(0, L, 0.02)
    return np.c_[x, A * np.sin(2 * np.pi * x / lam), 0 * x]


def helix(r, pitch, turns=3):
    t = np.linspace(0, 2 * np.pi * turns, 20000)
    return np.c_[r * np.cos(t), r * np.sin(t), pitch * t / (2 * np.pi)]


def rot(P, seed=0):
    Q, _ = np.linalg.qr(np.random.default_rng(seed).normal(size=(3, 3)))
    return P @ Q.T + np.array([3.0, -7.0, 11.0])


def true_rms(P):
    """RMS curvature of the dense curve (no smoothing), from finite differences."""
    C = arc_resample(P, 0.02)
    T = np.gradient(C, 0.02, axis=0)
    T /= np.linalg.norm(T, axis=1, keepdims=True)
    k = np.linalg.norm(np.gradient(T, 0.02, axis=0), axis=1)[5:-5]
    return np.sqrt((k ** 2).mean()), k.mean()


def row(name, P, **kw):
    d = bcs(raw(P), **kw)
    print(f"  {name:38s} kB={d['kB']:.4f} course={d['kB_course']:.4f} wiggle={d['kB_wiggle']:.4f} "
          f"f_twist={d['f_twist']:.3f} f_wiggle={d['f_wiggle']:.3f} | ka5={kappa_a(raw(P)):.4f} TI={arc_chord(raw(P)):.3f}")
    return d


def main():
    print("## 1. invariance (sine A=3 lam=20 bent into 3D by a slow helix of the axis)")
    s = np.arange(0, 100, 0.02)
    P = np.c_[s, 3 * np.sin(2 * np.pi * s / 20) + 0.002 * s ** 2, 2 * np.sin(2 * np.pi * s / 45)]
    d0 = row("reference", P)
    d1 = row("rotated + translated", rot(P, 1))
    d2 = row("mirrored (z -> -z)", P * np.array([1, 1, -1]))
    d3 = row("reversed direction", P[::-1])
    d4 = row("scaled x2 with scales x2 (kB*2 shown)", 2 * P, lam_c=40, w_sd=10)
    print(f"    scaled kB*2 = {2 * d4['kB']:.4f} vs {d0['kB']:.4f}; twist {d4['f_twist']:.3f} vs {d0['f_twist']:.3f}")
    Q = arc_resample(P, 0.3)
    row("resampled at 0.3 mm instead of 0.45", Q)

    print("\n## 2. line, C vs S, one wide arc vs tight bends (planar => f_twist must be 0)")
    row("straight line 100 mm", np.c_[np.arange(0, 100, 0.05), 0 * np.arange(0, 100, 0.05), 0 * np.arange(0, 100, 0.05)])
    for name, f in (("C: 180 deg over 60 mm", lambda s: np.where((s > 20) & (s < 80), np.pi / 60, 0)),
                    ("S: +90 then -90 deg over 60 mm", lambda s: np.where((s > 20) & (s < 50), np.pi / 60, np.where((s >= 50) & (s < 80), -np.pi / 60, 0))),
                    ("3 x 60 deg tight bends R=3 same way", lambda s: sum(np.where((s > c) & (s < c + np.pi), 1 / 3, 0) for c in (25, 48, 71))),
                    ("3 x 60 deg tight bends alternating", lambda s: sum(sg * np.where((s > c) & (s < c + np.pi), 1 / 3, 0) for c, sg in ((25, 1), (48, -1), (71, 1))))):
        row(name, from_heading(f, 100))

    print("\n## 3. amplitude sweep, planar sine lam = 20 mm (truth = dense RMS curvature)")
    for A in (0.5, 1, 2, 3, 4, 6, 8, 12):
        d = row(f"A={A}", sine(A, 20))
        print(f"      truth rms={true_rms(sine(A, 20))[0]:.4f} mean|k|={true_rms(sine(A, 20))[1]:.4f}")
    print("\n## 4. frequency sweep, A = 2 mm")
    for lam in (60, 40, 30, 20, 15, 10, 8, 6):
        row(f"lam={lam}", sine(2, lam))
        print(f"      truth rms={true_rms(sine(2, lam))[0]:.4f}")

    print("\n## 5. helix: truth kappa = r/(r^2+b^2), tau = b/(r^2+b^2); predicted f_twist = 1-exp(-2 tau^2 W^2)")
    for r, p in ((2, 10), (4, 20), (8, 20), (8, 60), (20, 60)):
        b = p / (2 * np.pi)
        k, t = r / (r * r + b * b), b / (r * r + b * b)
        row(f"helix r={r} pitch={p}", helix(r, p))
        print(f"      truth kappa={k:.4f} tau={t:.4f} predicted f_twist={1 - np.exp(-2 * t * t * 25):.3f}")

    print("\n## 6. plane hop: two 90-deg C bends (R=10) in perpendicular planes, 20 mm apart")
    ds = 0.05
    seg = lambda n, u: np.cumsum(np.tile(u, (n, 1)) * ds, axis=0)
    def bend(P, t, nrm, R=10, ang=np.pi / 2):
        out, T = [], t.copy()
        for _ in range(int(R * ang / ds)):
            T = T + ds / R * nrm
            nrm = nrm - (nrm @ T) * T / (T @ T)
            T /= np.linalg.norm(T); nrm /= np.linalg.norm(nrm)
            P = P + ds * T
            out.append(P)
        return np.array(out), T
    P0 = seg(400, np.array([1., 0, 0]))
    B1, T1 = bend(P0[-1], np.array([1., 0, 0]), np.array([0., 1, 0]))
    S1 = B1[-1] + seg(400, T1)
    for label, n2 in (("same plane, same way (C+C)", np.array([-1., 0, 0])),
                      ("same plane, opposite (S)", np.array([1., 0, 0])),
                      ("perpendicular plane", np.array([0., 0, 1]))):
        B2, T2 = bend(S1[-1], T1, n2)
        P = np.vstack([P0, B1, S1, B2, B2[-1] + seg(400, T2)])
        row(label, P)

    print("\n## 7. noise on a straight 100 mm line at 0.45 mm spacing (10 reps)")
    rng = np.random.default_rng(42)
    x = np.arange(0, 100, RAW)
    line = np.c_[x, 0 * x, 0 * x]
    for sn, corr in ((0.06, 0), (0.25, 0), (0.5, 0), (0.25, 1.0), (0.5, 1.0)):
        e = []
        for _ in range(10):
            n = rng.normal(0, 1, line.shape)
            if corr:
                n = gaussian_filter1d(n, corr / RAW, axis=0, mode="nearest"); n /= n.std(0)
            e.append(bcs(line + sn * n)["E"])
        print(f"  noise={sn:.2f} corr={corr:.0f}mm  mean kB^2={np.mean(e):.2e}  kB={np.sqrt(np.mean(e)):.4f}")

    print("\n## 8. additivity: E*L of whole vs sum over halves (smooth 3D curve of section 1)")
    C = arc_resample(P if False else np.c_[s, 3 * np.sin(2 * np.pi * s / 20), 2 * np.sin(2 * np.pi * s / 45)], RAW)
    a = np.r_[0, np.cumsum(seglen(C))]
    whole = bcs(C)["E"] * bcs(C)["L_s"]
    halves = sum(bcs(C[m])["E"] * bcs(C[m])["L_s"] for m in (a <= 50, a >= 50))
    print(f"  whole {whole:.4f}  halves {halves:.4f}  rel diff {halves / whole - 1:+.3%}")
    d = bcs(C)
    print(f"  2x2 parts sum: {d['E_cp'] + d['E_ct'] + d['E_wp'] + d['E_wt']:.6f} vs E {d['E']:.6f}")

    print("\n## 9. spectral moments: TI ~ (1/2L) sum P_k / w_k^2 (moment -2); Grisan sum ~ (1/24L) sum_turns l_t E_t")
    for A, lam in ((1, 30), (2, 20), (4, 20), (6, 15)):
        Cs = arc_resample(raw(sine(A, lam)))
        psi = bishop_psi(Cs)
        _, _, w, Pk = band_split(psi)
        L = H * (len(Cs) - 1)
        ti_spec = 0.5 * H * (Pk[1:] / w[1:] ** 2).sum() / L
        ti = seglen(Cs).sum() / np.linalg.norm(Cs[-1] - Cs[0]) - 1
        print(f"  sine A={A} lam={lam}: TI={ti:.4f}  spectral moment -2 = {ti_spec:.4f}  (finite-window leakage at low w inflates it)")
    for m in (2, 4, 6, 8):  # m alternating arcs, each 180/m... use constant turn angle 90 deg, length 60/m
        lt = 60 / m
        k = (np.pi / 2) / lt
        f = lambda s, lt=lt, k=k, m=m: np.where((s > 20) & (s < 80), k * (-1.0) ** np.floor((s - 20) / lt), 0)
        P = from_heading(f, 100)
        gr_turn = m * (np.pi / 2 / (2 * np.sin(np.pi / 4)) - 1) / 100
        approx = m * lt ** 2 * k ** 2 / 24 / 100  # = (1/24L) sum_t l_t E_t, E_t = k^2 l_t
        print(f"  {m} alternating 90-deg turns: sum(arc/chord-1)/L = {gr_turn:.5f}, (1/24L) sum_t l_t E_t = {approx:.5f}")


if __name__ == "__main__":
    main()
