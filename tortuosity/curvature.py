"""Mean absolute curvature T_l of a 3D centerline, measured at chord length l.

The centerline is respaced so that every step is a straight chord of exactly l mm. At each
interior vertex the turning angle theta between the arriving and the leaving chord is
atan2(|a x b|, a . b), in [0, pi]. T_l is the summed turning divided by the length the
angles cover, l times the number of angles, in rad/mm.
"""
import numpy as np


def chord_resample(P, l):
    """Vertices along the polyline P (n, 3), each exactly l mm (straight line) from the previous one.

    Starts at P[0]; a remainder shorter than l at the far end is dropped.
    """
    out, cur, i = [P[0]], P[0], 0
    while i + 1 < len(P):
        hit = np.linalg.norm(P[i + 1:] - cur, axis=1) >= l  # straight-line (not along-the-path) distance from cur to each later point
        if not hit.any():
            break
        j = int(np.argmax(hit))  # P[i + 1 + j] is the first point l or more away
        a = cur if j == 0 else P[i + j]
        v, w = P[i + 1 + j] - a, a - cur
        # solve |a + t v - cur| = l for t in [0, 1]: the point on segment a -> P[i + 1 + j] at distance l
        A, B, C = v @ v, 2 * v @ w, w @ w - l * l
        t = (-B + np.sqrt(max(B * B - 4 * A * C, 0.0))) / (2 * A)
        cur = a + min(max(t, 0.0), 1.0) * v  # new vertex, exactly l mm from the previous one
        out.append(cur)
        i += j
    return np.array(out)


def turning_angles(V):
    """Turning angle (rad) at each interior vertex of the polyline V (n, 3), length n - 2."""
    a, b = np.diff(V, axis=0)[:-1], np.diff(V, axis=0)[1:]
    return np.arctan2(np.linalg.norm(np.cross(a, b), axis=1), (a * b).sum(1))


def profile(P, l):
    """T_l before it is averaged: the turning per mm at each interior vertex, in rad/mm.

    The ordered form of Equation (2) of the method note, so its mean is exactly mean_abs_curvature(P, l).
    Tello Ayala et al. divide the angle by pi instead, which drops the per-millimetre meaning.
    """
    return turning_angles(chord_resample(P, l)) / l


def _at_chord(P, i, l, step):
    """The point on P, walking from P[i] in direction step (+1 / -1), exactly l mm (straight line) from
    P[i], solved as in chord_resample; None when the polyline ends first."""
    Q = P[i::step]
    hit = np.linalg.norm(Q[1:] - Q[0], axis=1) >= l
    if not hit.any():
        return None
    j = int(np.argmax(hit))  # Q[1 + j] is the first point l or more away
    a, v = Q[j], Q[1 + j] - Q[j]
    w = a - Q[0]
    A, B, C = v @ v, 2 * v @ w, w @ w - l * l
    t = (-B + np.sqrt(max(B * B - 4 * A * C, 0.0))) / (2 * A)
    return a + min(max(t, 0.0), 1.0) * v


def smooth_points(P, s, w):
    """Each point of P replaced by the mean of the points within w mm of arc length (fewer at the ends)."""
    lo, hi = np.searchsorted(s, s - w, "left"), np.searchsorted(s, s + w, "right")
    C = np.vstack([np.zeros(P.shape[1]), np.cumsum(P, axis=0)])
    return (C[hi] - C[lo]) / (hi - lo)[:, None]


def profile_thesis(P, l, s=None, smooth=0.0):
    """Sliding-window T_l: (arc length, rad/mm) at every point of P that has a point l mm (straight
    line) before and after it, the turning angle between P_i - B_i and F_i - P_i divided by l.

    Same chord and angle as profile, but centred on each point instead of on vertices laid from P[0],
    so it does not depend on where the respacing starts. s is the arc length of P (default: summed steps).
    Off by default: the tracer centerlines are expected to arrive smoothed already. smooth > 0 first
    averages the points over +-smooth mm (smooth_points), for unsmoothed trees: the centre point enters
    each angle in full, so its jitter gives a spike, and since angles are >= 0 the spikes raise T_l most
    in the noisiest centerlines.
    """
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))] if s is None else np.asarray(s)
    if smooth > 0:
        P = smooth_points(P, s, smooth)
    pos, theta = [], []
    for i in range(1, len(P) - 1):
        b, f = _at_chord(P, i, l, -1), _at_chord(P, i, l, 1)
        if b is None or f is None:
            continue
        a, c = P[i] - b, f - P[i]
        pos.append(s[i])
        theta.append(np.arctan2(np.linalg.norm(np.cross(a, c)), a @ c))
    return np.array(pos), np.array(theta) / l


def mean_abs_curvature(P, l):
    """T_l in rad/mm, or nan when the centerline holds fewer than two angles at chord l."""
    V = chord_resample(P, l)  # l is the smoothing scale: bends smaller than l are skipped
    if len(V) < 4:
        return np.nan
    theta = turning_angles(V)
    return theta.sum() / (l * len(theta))  # total turning per mm covered (each angle spans about l mm)
