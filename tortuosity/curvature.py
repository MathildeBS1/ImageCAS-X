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


def mean_abs_curvature(P, l):
    """T_l in rad/mm, or nan when the centerline holds fewer than two angles at chord l."""
    V = chord_resample(P, l)  # l is the smoothing scale: bends smaller than l are skipped
    if len(V) < 4:
        return np.nan
    theta = turning_angles(V)
    return theta.sum() / (l * len(theta))  # total turning per mm covered (each angle spans about l mm)
