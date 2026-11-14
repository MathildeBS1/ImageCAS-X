"""Left main bifurcation angle: the bifurcation feature of the who model (sec:method-angle, 05b_bifurcation_angle.tex).

    from bifurcation_angle import tree_angle
    tree_angle(tree)  # degrees, or nan

    python CGPS_data/thesis_final/bifurcation_angle.py --check   # synthetic shapes, needs no data

The angle between the LAD and the LCx (angle B of the European Bifurcation Club, the distal angle of
Medrano-Gracia et al. 2016), in 3D. Depth is arc length from the LM bifurcation point O, the first point
that split_trunks.split gives both arteries (arc length 0 on each). Each artery is represented by its
eleven points at DEPTHS, 5 to 10 mm in 0.5 mm steps (point_at_depth, linear interpolation between
centerline points), and its direction is the least-squares line through them, pointing away from O
(artery_direction). The feature is the angle between the two directions (method="fit", the default).
Fewer than 10 mm of either artery, or two arteries with no shared start (the LAD and LCx paths of
split_trunks.split start after a labelled LM then): nan. No smoothing of the points.

method="origin" keeps the previous definition, the mean over DEPTHS of the angle between the lines from
O to the two points at each depth; for a sensitivity run only. Fitted line chosen 2026-11-11 (with the
user, bifurcation_plan.md): with lines from O a true 75 deg reads about 65 deg when O sits 1 mm upstream
of the real split and 54 deg at 2 mm, while the fitted line stays at 75 deg (check()). Its costs: more
sensitive to point noise, and bends within 5 to 10 mm enter more (arteries curving apart from 60 deg).
It is also the closer reading of the atlas ("linear approximations of the centrelines", "average in the
5-10 mm depth interval"); the paper does not say how its lines were fitted.
Angles not used: LM-LAD and LM-LCx (only LAD-LCx was associated with stenosis when all three were
measured in the same patients, Cui et al. 2017), the inflow angle (no difference between stenosed and
stenosis-free bifurcations, Zhang et al. 2024). The LM is 10.5 +- 5.3 mm long in the atlas, so LM-based
angles often lack a 5 to 10 mm stretch.

Replaces who_where_readiness.lm_bifurcation_angle (Medis labels, a 2 to 8 mm centroid direction, a
bifurcation point per daughter).
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/

DEPTHS = np.arange(5.0, 10.0 + 1e-9, 0.5)  # mm along the artery, sec:method-angle


def point_at_depth(Y, s, d):
    """The point on the polyline Y (n, 3) at arc length d, by linear interpolation; None when the
    artery is shorter than d."""
    s = np.asarray(s, float)
    if s[-1] < d:
        return None
    return np.array([np.interp(d, s, Y[:, j]) for j in range(3)])


def angle_between(u, v):
    """The angle in degrees between the 3D vectors u and v, atan2(|u x v|, u . v)."""
    return float(np.degrees(np.arctan2(np.linalg.norm(np.cross(u, v)), u @ v)))


def artery_direction(Y, s, depths=DEPTHS):
    """Unit direction of the least-squares line through the points of (Y, s) at depths, pointing from the
    first depth towards the last; None when the artery is shorter than the last depth."""
    pts = [point_at_depth(Y, s, d) for d in depths]
    if any(q is None for q in pts):
        return None
    pts = np.array(pts)
    u = np.linalg.svd(pts - pts.mean(axis=0))[2][0]  # first principal axis of the points
    return u if u @ (pts[-1] - pts[0]) >= 0 else -u


def lm_angle(lad, cx, depths=DEPTHS, method="fit"):
    """Angle in degrees between the LAD and the LCx at the bifurcation point. lad and cx are (Y, s):
    centerline points (n, 3) and arc length (n,) from the bifurcation point.
    method "fit": the angle between the lines fitted to each artery's points at depths (the feature);
    "origin": the mean over depths of the angle between the lines from the bifurcation point."""
    (Yl, sl), (Yc, sc) = lad, cx
    if not np.allclose(Yl[0], Yc[0]):
        return np.nan  # no shared bifurcation point
    if method == "fit":
        ul, uc = artery_direction(Yl, sl, depths), artery_direction(Yc, sc, depths)
        return np.nan if ul is None or uc is None else angle_between(ul, uc)
    O = Yl[0]
    theta = []
    for d in depths:
        L, C = point_at_depth(Yl, sl, d), point_at_depth(Yc, sc, d)
        if L is None or C is None:
            return np.nan
        theta.append(angle_between(L - O, C - O))
    return float(np.mean(theta))


def tree_angle(tree, depths=DEPTHS, method="fit"):
    """LM bifurcation angle (degrees) of one tree, nan where the LAD or the LCx is missing."""
    from split_trunks import graph, split  # imported here so --check runs without the shared modules

    arteries = split(*graph(tree))
    if "LAD" not in arteries or "CX" not in arteries:
        return np.nan
    (*_, Yl, sl), (*_, Yc, sc) = arteries["LAD"], arteries["CX"]
    return lm_angle((Yl, sl), (Yc, sc), depths, method)


# ---------------------------------------------------------------- checks on synthetic shapes (no data)

def _arc(s):
    return np.r_[0, np.cumsum(np.linalg.norm(np.diff(s, axis=0), axis=1))]


def _straight(deg, n=200, length=30.0, plane_tilt=0.0):
    """Two straight daughters from the origin with `deg` between them, in a plane tilted by plane_tilt."""
    t = np.linspace(0, length, n)
    a = np.radians(deg / 2)
    u = np.array([np.cos(a), np.sin(a), 0.0])
    v = np.array([np.cos(a), -np.sin(a), 0.0])
    out = []
    for w in (u, v):
        Y = t[:, None] * w
        c, s_ = np.cos(plane_tilt), np.sin(plane_tilt)
        Y = Y @ np.array([[1, 0, 0], [0, c, -s_], [0, s_, c]]).T
        out.append((Y, _arc(Y)))
    return out


def _upstream(lad, cx, delta):
    """The same two daughters with a shared straight stem of delta mm before the true split, so the
    bifurcation point O sits delta mm upstream of it."""
    stem = np.linspace(-delta, 0, 50)[:-1, None] * np.array([1.0, 0.0, 0.0])
    out = []
    for Y, _ in (lad, cx):
        Z = np.r_[stem, Y]
        out.append((Z, _arc(Z)))
    return out


def _circles(start_deg=60, R=30.0, length=20.0):
    """Two daughters on circles of radius R through the origin, start_deg apart, curving away from each other."""
    t = np.linspace(0, length / R, 4000)
    a = np.radians(start_deg / 2)
    arcs = []
    for sign in (1, -1):
        phi = sign * a
        centre = R * np.array([-np.sin(phi), np.cos(phi), 0.0]) * sign
        ang = np.arctan2(-centre[1], -centre[0])
        Y = np.c_[centre[0] + R * np.cos(ang + sign * t), centre[1] + R * np.sin(ang + sign * t), 0 * t]
        arcs.append((Y, _arc(Y)))
    return arcs


def check():
    """Known answers for both methods. Prints the effect of a misplaced bifurcation point and of bends."""
    rng = np.random.default_rng(0)
    for method in ("fit", "origin"):
        for deg in (40, 75, 90, 120, 160):
            lad, cx = _straight(deg)
            Q = np.linalg.qr(rng.normal(size=(3, 3)))[0]
            lad_r, cx_r = (lad[0] @ Q.T + 3.0, lad[1]), (cx[0] @ Q.T + 3.0, cx[1])
            assert abs(lm_angle(lad, cx, method=method) - deg) < 1e-6, f"{method}: straight daughters at {deg} deg"
            assert abs(lm_angle(lad_r, cx_r, method=method) - deg) < 1e-6, f"{method}: rigid motion changed the angle"

        # unevenly spaced points on the same lines give the same angle
        lad, cx = _straight(75, n=4000)
        sub = []
        for Y, s in (lad, cx):
            k = np.unique(np.r_[0, np.sort(rng.choice(np.arange(1, 3999), 120, replace=False)), 3999])
            sub.append((Y[k], s[k]))
        assert abs(lm_angle(*sub, method=method) - 75) < 1e-3, f"{method}: the angle depends on point spacing"

        short, other = _straight(60, length=9.0)
        assert np.isnan(lm_angle(short, other, method=method)), f"{method}: an artery under 10 mm must give nan"
        lad, cx = _straight(60)
        cx = (cx[0] + 1.0, cx[1])
        assert np.isnan(lm_angle(lad, cx, method=method)), f"{method}: no shared start must give nan"

    # bifurcation point placed upstream of the true split of two straight daughters 75 degrees apart
    print("straight daughters 75 deg apart, bifurcation point delta mm upstream of the true split")
    for delta in (0.0, 0.5, 1.0, 2.0, 3.0):
        arms = _upstream(*_straight(75), delta) if delta else _straight(75)
        fit, orig = lm_angle(*arms), lm_angle(*arms, method="origin")
        print(f"  delta {delta:>3} mm: fit {fit:.1f} deg, from O {orig:.1f} deg")
        assert abs(fit - 75) < 1e-6, "the fitted angle must not depend on where O sits before the split"

    # circular daughters bending away from each other: the angle widens with depth
    arcs = _circles()
    print("daughters on circles of radius 30 mm, 60 deg apart at the start: angle from O at depth d")
    for d in (2, 5, 7.5, 10, 15):
        L, C = point_at_depth(*arcs[0], d), point_at_depth(*arcs[1], d)
        print(f"  d {d:>4} mm: {angle_between(L, C):.1f} deg")
    print(f"  fit {lm_angle(*arcs):.1f} deg, from O (mean over 5 to 10 mm) {lm_angle(*arcs, method='origin'):.1f} deg")
    print("all checks passed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="run the synthetic-shape checks")
    if ap.parse_args().check:
        check()
    else:
        ap.print_help()
