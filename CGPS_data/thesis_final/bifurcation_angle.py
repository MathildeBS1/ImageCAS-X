"""Left main bifurcation angle: the bifurcation feature of the who model (sec:method-angle, 05b_bifurcation_angle.tex).

    from bifurcation_angle import tree_angle
    tree_angle(tree)  # degrees, or nan

    python CGPS_data/thesis_final/bifurcation_angle.py --check   # synthetic shapes, needs no data

The angle between the LAD and the LCx (angle B of the European Bifurcation Club, the distal angle of
Medrano-Gracia et al. 2016) is measured in 3D from the LM bifurcation point O, the first point that
split_trunks.split gives both arteries (arc length 0 on each). At depth d, an arc length along the
artery, each artery is represented by the point at that depth (point_at_depth, linear interpolation
between centerline points), i.e. by the line from O to it, and theta(d) is the angle between the two
lines. The feature is the mean of theta(d) over DEPTHS, 5 to 10 mm in 0.5 mm steps, the depth interval
and step of Medrano-Gracia et al. (the angle falls slowly with depth, so one interval is fixed).
Fewer than 10 mm of either artery, or two arteries with no shared start (the LAD and LCx paths of
split_trunks.split start after a labelled LM then): nan. No smoothing of the points.

Replaces who_where_readiness.lm_bifurcation_angle (Medis labels, a 2 to 8 mm centroid direction, a
bifurcation point per daughter). The depth lines are the reading of "linear approximations of the
centrelines" of Medrano-Gracia et al.; the paper does not say how its lines were fitted.
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


def lm_angle(lad, cx, depths=DEPTHS):
    """Mean over depths of the angle at the bifurcation point between the LAD and the LCx, in degrees.
    lad and cx are (Y, s): centerline points (n, 3) and arc length (n,) from the bifurcation point."""
    (Yl, sl), (Yc, sc) = lad, cx
    if not np.allclose(Yl[0], Yc[0]):
        return np.nan  # no shared bifurcation point
    O = Yl[0]
    theta = []
    for d in depths:
        L, C = point_at_depth(Yl, sl, d), point_at_depth(Yc, sc, d)
        if L is None or C is None:
            return np.nan
        theta.append(angle_between(L - O, C - O))
    return float(np.mean(theta))


def tree_angle(tree, depths=DEPTHS):
    """LM bifurcation angle (degrees) of one tree, nan where the LAD or the LCx is missing."""
    from split_trunks import graph, split  # imported here so --check runs without the shared modules

    arteries = split(*graph(tree))
    if "LAD" not in arteries or "CX" not in arteries:
        return np.nan
    (*_, Yl, sl), (*_, Yc, sc) = arteries["LAD"], arteries["CX"]
    return lm_angle((Yl, sl), (Yc, sc), depths)


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


def check():
    """Known answers. Prints the angle against depth for circular daughters."""
    rng = np.random.default_rng(0)
    for deg in (40, 75, 90, 120, 160):
        lad, cx = _straight(deg)
        Q = np.linalg.qr(rng.normal(size=(3, 3)))[0]
        lad_r, cx_r = (lad[0] @ Q.T + 3.0, lad[1]), (cx[0] @ Q.T + 3.0, cx[1])
        assert abs(lm_angle(lad, cx) - deg) < 1e-6, f"straight daughters at {deg} degrees"
        assert abs(lm_angle(lad_r, cx_r) - deg) < 1e-6, "a rigid motion must not change the angle"

    # unevenly spaced points on the same lines give the same angle
    lad, cx = _straight(75, n=4000)
    sub = []
    for Y, s in (lad, cx):
        k = np.unique(np.r_[0, np.sort(rng.choice(np.arange(1, 3999), 120, replace=False)), 3999])
        sub.append((Y[k], s[k]))
    assert abs(lm_angle(*sub) - 75) < 1e-3, "the angle must not depend on point spacing"

    # circular daughters bending away from each other: the angle widens with depth
    print("daughters on circles of radius 30 mm, 60 degrees apart at the start: angle at depth d")
    t = np.linspace(0, 20 / 30, 4000)
    a = np.radians(30)
    arcs = []
    for sign in (1, -1):
        phi = sign * a
        # circle of radius 30 mm through the origin, leaving at angle phi and curving away from the other
        centre = 30 * np.array([-np.sin(phi), np.cos(phi), 0.0]) * sign
        ang = np.arctan2(-centre[1], -centre[0])
        Y = np.c_[centre[0] + 30 * np.cos(ang + sign * t), centre[1] + 30 * np.sin(ang + sign * t), 0 * t]
        arcs.append((Y, _arc(Y)))
    for d in (2, 5, 7.5, 10, 15):
        L, C = point_at_depth(*arcs[0], d), point_at_depth(*arcs[1], d)
        print(f"  d {d:>4} mm: {angle_between(L, C):.1f} deg")
    print(f"  mean over 5 to 10 mm: {lm_angle(*arcs):.1f} deg")

    short, other = _straight(60, length=9.0)
    assert np.isnan(lm_angle(short, other)), "an artery shorter than 10 mm must give nan"
    lad, cx = _straight(60)
    cx = (cx[0] + 1.0, cx[1])
    assert np.isnan(lm_angle(lad, cx)), "two arteries without a shared start must give nan"
    print("all checks passed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="run the synthetic-shape checks")
    if ap.parse_args().check:
        check()
    else:
        ap.print_help()
