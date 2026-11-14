"""Left main diameter ratios: the two ratio features of the who model (sec:method-ratio, 05c_daughter_ratio.tex).

    from daughter_ratio import tree_ratios
    tree_ratios(tree, rings_of)  # {"asymmetry": ln(D_LCx / D_LAD), "finet": D_LM / (D_LAD + D_LCx)}, nan where missing

    python CGPS_data/thesis_final/daughter_ratio.py --check   # synthetic shapes, needs no data

Diameter of one cross-section: the area-equivalent diameter 2 sqrt(A / pi) of the lumen contour, A the area
of the contour polygon in 3D (contour_diameter), the "effective radius" (A = pi R^2) of Medrano-Gracia et
al. 2016. Diameter of one vessel (reference_diameter), the median of these diameters over a stretch:
  LAD, LCx  5 to 10 mm downstream of the LM bifurcation point O (DEPTHS). O and the interval are those of
            bifurcation_angle.py, so the angle and the diameters describe the same stretch, clear of the
            widened confluence at O.
  LM        0 to 2 mm downstream of the ostium (LM_OSTIUM). The atlas reports the LM at the ostium, one
            cross-section; the 2 mm median over a few contours is this thesis's extension of it (2026-11-11,
            user), so one contour at the aortic junction does not set the value.
The median, so one cross-section widened by a side-branch origin does not move the value.

The features (lm_ratios):
    asymmetry = ln(D_LCx / D_LAD)            0 for equal daughters, < 0 when the LCx is the narrower
    finet     = D_LM / (D_LAD + D_LCx)       Finet et al. 2008 report 0.678 on average
The LM diameter enters Finet's ratio only, so its error (the ostium contour is the least certain in the
tree, and a left main of under about 4 mm puts the ostium window in the confluence) does not reach the
asymmetry. Missing: a daughter shorter than 10 mm, or no shared start of the LAD and the LCx (as for the
angle) -> both nan; a left main shorter than 2 mm or with fewer than 2 contours in its first 2 mm -> Finet
nan, asymmetry kept.

Not used (header of 05c_daughter_ratio.tex): the LM->LAD and LM->LCx ratios planned before 2026-11-11.
Open: the tracer contour format is unknown, so tracer_rings raises NotImplementedError (as
split_check.tracer_tree); every other function takes arrays and is checked here.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/

DEPTHS = (5.0, 10.0)  # mm from O along the LAD and the LCx, the interval of bifurcation_angle.DEPTHS
LM_OSTIUM = (0.0, 2.0)  # mm from the ostium along the left main, sec:method-ratio


def contour_area(ring):
    """Area of the closed lumen contour ring (m, 3) in 3D: half the norm of the summed cross products of
    consecutive vertices about the centroid (exact for a planar polygon)."""
    r = np.asarray(ring, float)
    r = r - r.mean(axis=0)
    return 0.5 * float(np.linalg.norm(np.cross(r, np.roll(r, -1, axis=0)).sum(axis=0)))


def contour_diameter(ring):
    """Area-equivalent diameter 2 sqrt(A / pi) of one lumen contour, in the unit of the points (mm)."""
    return 2.0 * np.sqrt(contour_area(ring) / np.pi)


def reference_diameter(s, D, lo=DEPTHS[0], hi=DEPTHS[1]):
    """Median of the diameters D over the points with arc length s in [lo, hi]; nan when the vessel does not
    reach hi or fewer than 2 points with a diameter fall in the interval."""
    s, D = np.asarray(s, float), np.asarray(D, float)
    if len(s) == 0 or s[-1] < hi:
        return np.nan
    d = D[(s >= lo) & (s <= hi) & np.isfinite(D)]
    return float(np.median(d)) if len(d) >= 2 else np.nan


def lm_ratios(lad, cx, lm, depths=DEPTHS, lm_window=LM_OSTIUM):
    """The two features from (s, D) of the LAD, the LCx and the LM: arc length from O for the daughters,
    from the ostium for the LM. The asymmetry is kept when the LM diameter is missing."""
    d_lad, d_cx = (reference_diameter(s, D, *depths) for s, D in (lad, cx))
    d_lm = reference_diameter(*lm, *lm_window)
    asym = float(np.log(d_cx / d_lad)) if np.isfinite(d_lad) and np.isfinite(d_cx) else np.nan
    finet = float(d_lm / (d_lad + d_cx)) if np.isfinite(asym) and np.isfinite(d_lm) else np.nan
    return {"asymmetry": asym, "finet": finet}


def _arc(Y):
    return np.r_[0, np.cumsum(np.linalg.norm(np.diff(Y, axis=0), axis=1))]


def tracer_rings(path):
    """Lumen contour per centerline point of a tracer tree."""
    raise NotImplementedError(
        "tracer_rings: file format of the tracer lumen contours is not known yet (as split_check.tracer_tree); "
        "return a callable Y (n, 3) -> list of n contour rings (m, 3) in LPS mm")


def tree_ratios(tree, rings_of):
    """Asymmetry and Finet's ratio of one tree. rings_of(Y) gives the lumen contour (m, 3) of each
    centerline point of Y (n, 3), or None where there is none."""
    from split_trunks import graph, split, trunk_path  # imported here so --check runs without the shared modules

    nan = {"asymmetry": np.nan, "finet": np.nan}
    X, lab, G = graph(tree)
    arteries = split(X, lab, G)
    if "LAD" not in arteries or "CX" not in arteries:
        return nan
    (*_, Yl, sl), (*_, Yc, sc) = arteries["LAD"], arteries["CX"]
    if not np.allclose(Yl[0], Yc[0]):
        return nan  # no shared bifurcation point, as in bifurcation_angle.lm_angle
    pl, pc = trunk_path(X, lab, G, "LAD"), trunk_path(X, lab, G, "CX")
    common = sum(1 for a, b in zip(pl, pc) if a == b)
    Ym = X[pl[:common]]  # left main from the ostium down to O
    out = []
    for Y, s in ((Yl, sl), (Yc, sc), (Ym, _arc(Ym))):
        rings = rings_of(Y)
        out.append((s, [contour_diameter(r) if r is not None else np.nan for r in rings]))
    return lm_ratios(*out)


# ---------------------------------------------------------------- checks on synthetic shapes (no data)

def _ring(centre, normal, a, b, m=720):
    """Ellipse with semi-axes a and b around centre, in the plane perpendicular to normal."""
    n = normal / np.linalg.norm(normal)
    e1 = np.cross(n, [1.0, 0, 0] if abs(n[0]) < 0.9 else [0, 1.0, 0])
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(n, e1)
    t = np.linspace(0, 2 * np.pi, m, endpoint=False)
    return centre + a * np.cos(t)[:, None] * e1 + b * np.sin(t)[:, None] * e2


def _tube(direction, D, length, rng, widen_at=None):
    """Straight vessel from the origin with unevenly spaced points and circular contours of diameter D;
    widen_at (mm) widens the one contour nearest to it to 1.6 D."""
    s = np.r_[0, np.cumsum(rng.uniform(0.3, 1.2, 400))]
    s = s[s <= length]
    u = np.asarray(direction, float) / np.linalg.norm(direction)
    Y = s[:, None] * u
    Ds = np.full(len(s), D)
    if widen_at is not None:
        Ds[np.argmin(np.abs(s - widen_at))] = 1.6 * D
    rings = [_ring(y, u, d / 2, d / 2) for y, d in zip(Y, Ds)]
    return s, np.array([contour_diameter(r) for r in rings])


def check():
    """Known answers."""
    rng = np.random.default_rng(0)
    # contours: circle and ellipse of known area, under a rigid motion
    for a, b in ((1.5, 1.5), (2.0, 1.0), (1.8, 1.2)):
        Q = np.linalg.qr(rng.normal(size=(3, 3)))[0]
        ring = _ring(np.zeros(3), np.array([0.3, -0.5, 1.0]), a, b)
        for r in (ring, ring @ Q.T + np.array([10.0, -4.0, 2.5])):
            assert abs(contour_diameter(r) - 2 * np.sqrt(a * b)) < 1e-4, f"ellipse {a} x {b}"
    sq = np.array([[0, 0, 0], [2, 0, 0], [2, 2, 0], [0, 2, 0.0]])
    assert abs(contour_area(sq) - 4.0) < 1e-12 and abs(contour_area(sq[::-1]) - 4.0) < 1e-12, "orientation"

    # tubes of known diameter, unevenly spaced points: exact asymmetry and Finet's ratio
    d_lm, d_lad, d_cx = 3.39, 2.75, 2.25  # Finet's ratio 3.39 / 5.00 = 0.678, the mean of Finet et al. 2008
    lad = _tube([1, 0.4, 0], d_lad, 30, rng)
    cx = _tube([1, -0.6, 0.2], d_cx, 30, rng)
    lm = _tube([-1, 0, 0.1], d_lm, 14, rng, widen_at=13.0)  # widened at its O end: outside the ostium window
    r = lm_ratios(lad, cx, lm)
    assert abs(r["asymmetry"] - np.log(d_cx / d_lad)) < 1e-4, "asymmetry of known tubes"
    assert abs(r["finet"] - 0.678) < 1e-4, "Finet's ratio of known tubes"
    print(f"tubes LM {d_lm}, LAD {d_lad}, LCx {d_cx} mm: asymmetry {r['asymmetry']:.4f} "
          f"(ln {d_cx}/{d_lad} = {np.log(d_cx / d_lad):.4f}), Finet {r['finet']:.4f}")
    assert abs(lm_ratios(cx, cx, lm)["asymmetry"]) < 1e-12, "equal daughters must give asymmetry 0"

    # one cross-section widened (side-branch origin) inside the window leaves the median unchanged
    lad_w = _tube([1, 0.4, 0], d_lad, 30, rng, widen_at=7.0)
    assert np.max(lad_w[1]) > 1.5 * d_lad, "the widened contour must be in the data"
    assert abs(reference_diameter(*lad_w) - d_lad) < 1e-4, "one widened cross-section must not move the median"

    # missing rules
    lm_short = _tube([-1, 0, 0], d_lm, 1.5, rng)
    r = lm_ratios(lad, cx, lm_short)
    assert np.isnan(r["finet"]) and np.isfinite(r["asymmetry"]), "LM under 2 mm: Finet nan, asymmetry kept"
    r = lm_ratios(lad, cx, _tube([-1, 0, 0], d_lm, 4.0, rng))
    assert abs(r["finet"] - 0.678) < 1e-4, "a 4 mm LM still has its ostium window"
    cx_short = _tube([1, -0.6, 0.2], d_cx, 9, rng)
    r = lm_ratios(lad, cx_short, lm)
    assert np.isnan(r["finet"]) and np.isnan(r["asymmetry"]), "short daughter: both nan"
    assert np.isnan(reference_diameter([0.0, 5.0, 10.0], [2.0, np.nan, np.nan])), "fewer than 2 points"

    # the window must not depend on point spacing: a dense and a sparse sampling of one tapering vessel
    s_dense = np.linspace(0, 20, 4001)
    s_sparse = np.unique(np.r_[0, np.sort(rng.uniform(0, 20, 60)), 20])
    taper = lambda s: 3.0 - 0.02 * s  # noqa: E731
    a, b = reference_diameter(s_dense, taper(s_dense)), reference_diameter(s_sparse, taper(s_sparse))
    assert abs(a - taper(7.5)) < 1e-9 and abs(b - taper(7.5)) < 0.03, "median of a linear taper is mid-window"
    print("all checks passed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="run the synthetic-shape checks")
    if ap.parse_args().check:
        check()
    else:
        ap.print_help()
