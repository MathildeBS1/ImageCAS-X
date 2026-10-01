"""The merged method from knowledge/reports/Merged tortuosity methods for coronaries.md.

Slope-chain substrate: resample at constant chord l (mm), turning angle per vertex.
  scc_density   sum(theta) / L over the interior vertices, rad/mm: the threshold-free companion.
  grisan3d      Grisan's index with the curvature-sign twist replaced by a binormal flip.
  arc_chord     arc / chord - 1 over the whole vessel, the trivial baseline.
"""
import numpy as np

KAPPA_FLOOR = 0.02  # 1/mm; a turn is significant when theta > KAPPA_FLOOR * l (3D hysteresis floor)


def chord_resample(P, l):
    """Vertices on the polyline P (n, 3), each exactly l mm (Euclidean) from the last."""
    out, cur, i = [P[0]], P[0], 0
    while i + 1 < len(P):
        d = np.linalg.norm(P[i + 1:] - cur, axis=1)
        hit = d >= l
        if not hit.any():
            break
        j = int(np.argmax(hit))  # P[i+1+j] is the first point l or more away
        a = cur if j == 0 else P[i + j]
        b = P[i + 1 + j]
        v, w = b - a, a - cur
        A, B, C = v @ v, 2 * v @ w, w @ w - l * l
        t = (-B + np.sqrt(max(B * B - 4 * A * C, 0.0))) / (2 * A)
        cur = a + min(max(t, 0.0), 1.0) * v
        out.append(cur)
        i += j
    return np.array(out)


def _turns(V):
    u = np.diff(V, axis=0)
    u /= np.linalg.norm(u, axis=1, keepdims=True)
    return u, np.arctan2(np.linalg.norm(np.cross(u[:-1], u[1:]), axis=1), (u[:-1] * u[1:]).sum(1))


def scc_density(P, l):
    V = chord_resample(P, l)
    if len(V) < 4:
        return np.nan
    _, th = _turns(V)
    return th.sum() / (l * (len(V) - 2))  # len(V) - 2 angles, one per interior vertex


def grisan3d(P, l, kappa_floor=KAPPA_FLOOR):
    """(tau, n_turns). tau in 1/mm as in Grisan eq. 19; n_turns = 1 means no twist found."""
    V = chord_resample(P, l)
    if len(V) < 4:
        return np.nan, 0
    u, th = _turns(V)
    sig = np.flatnonzero(th > kappa_floor * l)
    b = np.cross(u[sig], u[sig + 1])
    b /= np.linalg.norm(b, axis=1, keepdims=True)
    flip = np.flatnonzero((b[:-1] * b[1:]).sum(1) < 0)
    cuts = [0] + [(sig[k] + sig[k + 1]) // 2 + 1 for k in flip] + [len(V) - 1]
    n = len(cuts) - 1
    arc = l * np.diff(cuts)
    chord = np.linalg.norm(V[cuts[1:]] - V[cuts[:-1]], axis=1)
    return (n - 1) / n / (l * (len(V) - 1)) * (arc / chord - 1).sum(), n


def arc_chord(P):
    arc = np.linalg.norm(np.diff(P, axis=0), axis=1).sum()
    return arc / np.linalg.norm(P[-1] - P[0]) - 1
