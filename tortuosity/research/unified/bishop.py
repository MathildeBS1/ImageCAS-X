"""Bishop curvature spectrum (BCS): a band- and shape-decomposed bending energy of a centerline.

Definition (see research_notes/Centerline tortuosity normal ranges/unified_2d3d_method.md):
  1. resample the polyline at H = 0.25 mm; no extra smoothing, the delivered centerline already
     carries a 0.5 mm Gaussian smoothing;
  2. psi(s) = k1 + i k2, the curvature vector T' written in a rotation-minimising (Bishop)
     frame (M1, M2) carried by parallel transport; psi is fixed up to one global phase;
  3. E = int |psi|^2 ds (elastic bending energy). Orthonormal DCT of psi and a power-complementary
     Gaussian split at half-power wavelength lam_c give E = E_course + E_wiggle exactly;
  4. inside each band, E_band = E_planar + E_twist with
       E_planar = int |g_W * psi^2| ds   (coherent single-plane bending over a window of sd W)
       E_twist  = int (g_W * |psi|^2 - |g_W * psi^2|) ds   (energy outside the local dominant plane)
     E_twist = 0 exactly for any planar curve (psi real up to phase), whatever its inflections.
Reported per unit length as RMS curvatures (mm^-1): kB = sqrt(E / L), etc.
"""
import numpy as np
from scipy.fft import dct, idct
from scipy.ndimage import gaussian_filter1d

H = 0.25
LAM_C, W = 20.0, 5.0  # mm, pre-declared before any cohort number (see notes)


def seglen(P):
    return np.linalg.norm(np.diff(P, axis=0), axis=1)


def arc_resample(P, step=H):
    a = np.r_[0, np.cumsum(seglen(P))]
    g = np.arange(0, a[-1], step)
    return np.column_stack([np.interp(g, a, P[:, k]) for k in range(3)])


def bishop_psi(C):
    """Complex Bishop curvature psi (mm^-1) at the interior samples of a curve sampled every H mm."""
    T = np.gradient(C, H, axis=0)
    T /= np.linalg.norm(T, axis=1, keepdims=True)
    K = np.gradient(T, H, axis=0)
    K -= (K * T).sum(1, keepdims=True) * T  # curvature vector, normal to T
    a = np.eye(3)[np.argmin(np.abs(T[0]))]
    M = np.empty_like(T)
    M[0] = np.cross(T[0], a) / np.linalg.norm(np.cross(T[0], a))
    for i in range(1, len(T)):  # rotation-minimising transport: rotate M by the rotation T[i-1] -> T[i]
        t0, t1 = T[i - 1], T[i]
        v, c = np.cross(t0, t1), t0 @ t1
        m = M[i - 1]
        M[i] = m * c + np.cross(v, m) + v * (v @ m) / (1 + c)
        M[i] -= (M[i] @ t1) * t1
        M[i] /= np.linalg.norm(M[i])
    M2 = np.cross(T, M)
    return (K * M).sum(1) + 1j * (K * M2).sum(1)


def band_split(psi, lam_c=LAM_C):
    """Orthonormal DCT split psi = psi_course + psi_wiggle with |H_L|^2 + |H_H|^2 = 1 per coefficient."""
    n = len(psi)
    w = np.pi * np.arange(n) / (n * H)
    s_c = np.sqrt(np.log(2)) * lam_c / (2 * np.pi)
    hl2 = np.exp(-(w * s_c) ** 2)
    c = dct(psi.real, norm="ortho") + 1j * dct(psi.imag, norm="ortho")
    lo, hi = np.sqrt(hl2) * c, np.sqrt(1 - hl2) * c
    back = lambda x: idct(x.real, norm="ortho") + 1j * idct(x.imag, norm="ortho")
    return back(lo), back(hi), w, np.abs(c) ** 2


def shape_split(psi, w_sd=W):
    """(E_planar, E_twist) in mm^-1 (integrals over s); they sum to int |psi|^2 ds."""
    s = w_sd / H
    q = psi ** 2
    gq = gaussian_filter1d(q.real, s, mode="reflect") + 1j * gaussian_filter1d(q.imag, s, mode="reflect")
    ga = gaussian_filter1d(np.abs(psi) ** 2, s, mode="reflect")
    e = H * (np.abs(psi) ** 2).sum()
    fp = np.abs(gq).sum() / ga.sum()
    return e * fp, e * (1 - fp)


def bcs(P, lam_c=LAM_C, w_sd=W):
    """Per-vessel descriptors. Energies are per unit length and reported as sqrt (mm^-1)."""
    C = arc_resample(P)
    L = H * (len(C) - 1)
    psi = bishop_psi(C)
    lo, hi, _, _ = band_split(psi, lam_c)
    E = H * (np.abs(psi) ** 2).sum()
    cp, ct = shape_split(lo, w_sd)
    wp, wt = shape_split(hi, w_sd)
    r = lambda e: np.sqrt(max(e, 0) / L)
    return {"L_s": L, "kB": r(E), "kB_course": r(cp + ct), "kB_wiggle": r(wp + wt),
            "kB_planar": r(cp + wp), "kB_twist": r(ct + wt),
            "f_twist": (ct + wt) / E, "f_wiggle": (wp + wt) / E,
            "E_cp": cp / L, "E_ct": ct / L, "E_wp": wp / L, "E_wt": wt / L, "E": E / L}


# ---------------- baselines, same pipeline as the earlier P100/P150 reports ----------------

def chord_resample(P, ell):
    out, cur, i, n = [P[0]], P[0], 0, len(P)
    m = int(4 * ell / H) + 8
    while i + 1 < n:
        d = np.linalg.norm(P[i + 1:i + 1 + m] - cur, axis=1)
        hit = np.flatnonzero(d >= ell)
        if len(hit) == 0 and i + 1 + m < n:
            hit = np.flatnonzero(np.linalg.norm(P[i + 1:] - cur, axis=1) >= ell)
        if len(hit) == 0:
            break
        j = hit[0]
        a = cur if j == 0 else P[i + j]
        b = P[i + 1 + j]
        v, w = b - a, a - cur
        A, B, Cq = v @ v, 2 * v @ w, w @ w - ell * ell
        t = (-B + np.sqrt(max(B * B - 4 * A * Cq, 0.0))) / (2 * A)
        cur = a + min(max(t, 0.0), 1.0) * v
        out.append(cur)
        i += j
    return np.array(out)


def kappa_a(P, ell=5.0):
    V = chord_resample(arc_resample(P), ell)
    if len(V) < 3:
        return np.nan
    u = np.diff(V, axis=0)
    u /= np.linalg.norm(u, axis=1, keepdims=True)
    return np.arccos(np.clip((u[:-1] * u[1:]).sum(1), -1, 1)).mean() / ell


def arc_chord(P):
    C = arc_resample(P)
    return seglen(C).sum() / np.linalg.norm(C[-1] - C[0]) - 1
