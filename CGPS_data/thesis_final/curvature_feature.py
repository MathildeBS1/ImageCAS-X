"""Average curvature per segment: the curvature feature of the who model (sec:method-curvature, 05a_curvature.tex).

    from curvature_feature import segment_curvature
    segment_curvature(tree)  # {(artery, 0/1/2 for p/m/d): 1/mm or nan}

    python CGPS_data/thesis_final/curvature_feature.py --check   # synthetic shapes, needs no data

Each artery of split_trunks.split gets a curvature profile. At every centerline point P_i with a point
CHORD mm away in a straight line both before (B_i) and after (F_i) it, the chord ends are found by
linear interpolation between centerline points (chord_point), and the curvature is the inverse radius
of the circle through B_i, P_i and F_i, by Menger's formula (menger_curvature):
kappa = 4 A / (|P_i - B_i| |F_i - P_i| |F_i - B_i|), A the area of the triangle, in 1/mm. In 3D the
three points span one plane and A = |a x b| / 2 with a = P_i - B_i, b = F_i - P_i. Three points on a
line give 0. This is the curvature van Zandwijk et al. 2020 computed at 5 mm on CCTA. On a circle it is
exactly 1/R for every radius; the turning angle per mm, theta / CHORD, overestimates it on tight bends
(+4.7 % at R = 5 mm). With both chords CHORD long, kappa = 2 sin(theta / 2) / CHORD, theta the angle
between the chords (the form used until 2026-11-10; same values). No extra smoothing of the points.

The profile is computed on the whole artery and then cut at the segment boundaries, and each segment
gets the arc-length mean of its profile points (trapezoid rule over arc length), so densely sampled
stretches do not count more. Fewer than two profile points in a segment: nan.

Replaces turning_feature.py (theta / CHORD, 2026-11-09). The chord solver is the one of
tortuosity/curvature.py (_at_chord), copied here so thesis_final/ imports nothing from that package.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/

CHORD = 5.0  # mm, sec:method-curvature


def chord_point(P, i, l, step):
    """The point on the polyline P (n, 3), walking from P[i] in direction step (+1 ahead, -1 behind),
    exactly l mm from P[i] in a straight line, by linear interpolation on the first polyline step that
    crosses that distance; None when the polyline ends first."""
    Q = P[i::step]
    hit = np.linalg.norm(Q[1:] - Q[0], axis=1) >= l
    if not hit.any():
        return None
    j = int(np.argmax(hit))  # Q[1 + j] is the first point l or more away
    a, v = Q[j], Q[1 + j] - Q[j]
    w = a - Q[0]
    A, B, C = v @ v, 2 * v @ w, w @ w - l * l  # |a + t v - Q[0]| = l, solved for t in [0, 1]
    t = (-B + np.sqrt(max(B * B - 4 * A * C, 0.0))) / (2 * A)
    return a + min(max(t, 0.0), 1.0) * v


def menger_curvature(b, p, f):
    """Inverse radius of the circle through the 3D points b, p and f (Menger's formula), in 1/length:
    4 * triangle area / product of the three side lengths, with 4 * area = 2 |(p - b) x (f - p)|.
    0 for three points on a line. If b and f coincide (the artery doubles back on itself), the circle
    with diameter |p - b| is taken, 2 / |p - b|, the limit of the formula."""
    a, c = p - b, f - p
    ab, ac, bf = np.linalg.norm(a), np.linalg.norm(c), np.linalg.norm(f - b)
    if bf == 0:
        return 2 / ab
    return 2 * np.linalg.norm(np.cross(a, c)) / (ab * ac * bf)


def curvature_profile(P, l=CHORD, s=None):
    """(arc length, curvature in 1/mm) at every point of P with a chord end l mm before and after it.
    s is the arc length of P (default: the summed point-to-point steps)."""
    P = np.asarray(P, float)
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))] if s is None else np.asarray(s, float)
    pos, kappa = [], []
    for i in range(1, len(P) - 1):
        b, f = chord_point(P, i, l, -1), chord_point(P, i, l, 1)
        if b is not None and f is not None:
            pos.append(s[i])
            kappa.append(menger_curvature(b, P[i], f))
    return np.array(pos), np.array(kappa)


def segment_mean(pos, kappa, lo, hi):
    """Arc-length mean (trapezoid rule) of the profile points with lo <= pos < hi, in 1/mm; nan below two points."""
    k = (pos >= lo) & (pos < hi)
    if k.sum() < 2:
        return np.nan
    p, t = pos[k], kappa[k]
    return ((t[1:] + t[:-1]) / 2 * np.diff(p)).sum() / (p[-1] - p[0])


def artery_curvature(Y, s, bounds, chord=CHORD):
    """Average curvature of each segment [lo, hi) of one artery, bounds = (0, pm, md, end) in mm along it."""
    pos, kappa = curvature_profile(Y, chord, s)
    return [segment_mean(pos, kappa, lo, hi) for lo, hi in zip(bounds[:-1], bounds[1:])]


def segment_curvature(tree, chord=CHORD):
    """{(artery, part): average curvature in 1/mm} for the LAD, LCx and RCA segments of one tree, part 0/1/2 = p/m/d."""
    from split_trunks import graph, split  # imported here so --check runs without the shared modules

    out = {}
    for a, (pm, md, end, _, Y, s) in split(*graph(tree)).items():
        for part, T in enumerate(artery_curvature(Y, s, (0, pm, md, end), chord)):
            out[(a, part)] = T
    return out


# ---------------------------------------------------------------- checks on synthetic shapes (no data)

def _circle(R, n=6000):
    t = np.linspace(0, 1.5 * np.pi, n)
    return np.c_[R * np.cos(t), R * np.sin(t), 0 * t]


def _wavy(s):
    """A made-up 3D artery: a sideways wave with a slow upward drift, sampled at arc-length-ish positions s."""
    return np.c_[s, 4 * np.sin(2 * np.pi * s / 25), 3 * np.cos(s / 9)]


def check():
    """Known answers. Prints the theta / l vs kappa table used in the 05a header comment."""
    line = np.c_[np.linspace(0, 100, 400), np.zeros(400), np.zeros(400)]
    _, k = curvature_profile(line)
    assert np.abs(k).max() < 1e-12, "a straight line must have curvature 0"

    print("circle of radius R, chord 5 mm: mean of theta / l and of kappa against 1/R (1/mm)")
    for R in (3, 5, 10, 20, 40):
        P = _circle(R)
        _, kappa = curvature_profile(P)
        theta_l = 2 * np.arcsin(kappa * CHORD / 2) / CHORD  # the turning angle per mm, from kappa (equal chords)
        print(f"  R {R:>2} mm: theta/l {theta_l.mean():.4f} ({100 * (theta_l.mean() * R - 1):+.1f}%), "
              f"kappa {kappa.mean():.4f} ({100 * (kappa.mean() * R - 1):+.2f}%), 1/R {1 / R:.4f}")
        assert np.allclose(kappa, 1 / R, rtol=1e-4), f"kappa must be 1/R on a circle (R = {R})"

    a, b = 8.0, 3.0  # helix: curvature a / (a^2 + b^2), a 3D curve with torsion
    t = np.linspace(0, 6 * np.pi, 8000)
    _, kappa = curvature_profile(np.c_[a * np.cos(t), a * np.sin(t), b * t])
    true = a / (a * a + b * b)
    print(f"helix a {a}, b {b}: kappa {kappa.mean():.4f} vs true {true:.4f}")
    assert abs(kappa.mean() / true - 1) < 0.01, "helix curvature must be within 1%"

    rng = np.random.default_rng(0)
    s = np.linspace(0, 90, 300)
    P = _wavy(s)
    Q = np.linalg.qr(rng.normal(size=(3, 3)))[0]
    T0 = artery_curvature(P, None, (0, 30, 60, 90))
    T1 = artery_curvature(P @ Q.T + 5.0, None, (0, 30, 60, 90))
    assert np.allclose(T0, T1), "a rigid motion must not change T"

    # Unevenly spaced points (each step 0.4 to 1.6 times the mean spacing h). The boundaries are set on
    # the true arc length, so the check isolates the averaging from where the boundaries fall. Asserted
    # for mean spacings up to 0.5 mm; the 1 mm row is printed only: there the straight polyline steps
    # cut the bends, which shifts T by a few percent whatever the averaging does.
    print("same made-up artery traced at different point densities: T per segment (1/mm)")
    dense = _wavy(np.linspace(0, 90, 20000))
    ds = np.r_[0, np.cumsum(np.linalg.norm(np.diff(dense, axis=0), axis=1))]
    Ts = {}
    for h in (0.125, 0.25, 0.5, 1.0):
        u = np.r_[0, np.cumsum(rng.uniform(0.4 * h, 1.6 * h, int(2 * ds[-1] / h)))]
        u = u[u <= ds[-1]]
        Y = np.c_[[np.interp(u, ds, dense[:, j]) for j in range(3)]].T
        Ts[h] = artery_curvature(Y, u, (0, 40, 80, u[-1]))
        print(f"  mean spacing {h:<5} mm, {len(u):>4} points: " + ", ".join(f"{x:.4f}" for x in Ts[h]))
    fine = np.array([Ts[h] for h in (0.125, 0.25, 0.5)])
    spread = (fine.max(0) - fine.min(0)) / fine.mean(0)
    print(f"  largest spread, mean spacing 0.125 to 0.5 mm: {100 * spread.max():.1f}%")
    assert spread.max() < 0.03, f"T must not depend on point density (spread {spread.max():.3f})"

    pos, kappa = curvature_profile(P)
    assert np.isnan(segment_mean(pos, kappa, 45.0, 45.1)), "fewer than two profile points must give nan"
    print("all checks passed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="run the synthetic-shape checks")
    if ap.parse_args().check:
        check()
    else:
        ap.print_help()
