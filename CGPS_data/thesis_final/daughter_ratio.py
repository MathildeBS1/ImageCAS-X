"""Left main diameter ratios: the two ratio features of the who model (sec:method-ratio, 03c_daughter_ratio.tex).

    from daughter_ratio import tree_ratios
    tree_ratios(tree, rings_of)  # {"asymmetry": ln(D_LCx / D_LAD), "finet": D_LM / (D_LAD + D_LCx)}, nan where missing
    narrower_rows(asymmetry)     # {"plad": ..., "pcx": ...}, the asymmetry's value on the two model rows

    python CGPS_data/thesis_final/daughter_ratio.py --check   # synthetic shapes, needs no data

Diameter of one cross-section: the area-equivalent diameter 2 sqrt(A / pi) of the lumen contour, A the area
of the contour polygon in 3D (contour_diameter), the "effective radius" (A = pi R^2) of Medrano-Gracia et
al. 2016. Diameter of one vessel (reference_diameter), the median of these diameters over a stretch, taken
every 0.5 mm (STEP, the depths of bifurcation_angle.py) by linear interpolation between contours, so densely
sampled parts of the stretch do not count more (2026-11-18; before, the median over the points):
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

Model rows (narrower_rows, decided 2026-11-18): |asymmetry| enters only the proximal segment of the narrower
daughter, 0 on the wider one, so pLAD = max(a, 0) and pCX = max(-a, 0). Garcha and Grande Gutierrez 2025
(p. 6, Fig. 4) found low wall shear stress "in the smaller-of-the-two branches". The model scales the value
by its SD over persons but does not centre it, so 0 keeps meaning equal daughters or the wider one.

Not used (header of 03c_daughter_ratio.tex): the LM->LAD and LM->LCx ratios planned before 2026-11-11.
Diameters from a lumen surface (surface_diameters, 2026-11-19). The lumen predictions hold no contour per
step, only a triangle mesh (lumen_probe.md: lumen_surface_ostium_pruned.vtk). The surface is cut with the plane
through the centerline point at each depth of SECTION_DEPTHS (5 to 10 mm from O every STEP mm), perpendicular
to the centerline (the direction from the point 1 mm before to the point 1 mm after). Of the closed loops of
the cut, the one that encloses the centerline point is the cross-section (the smallest, if several do), and
its area-equivalent diameter is taken. No diameter at that depth when no closed loop encloses the point (the
surface ends, or the cut leaves CUT_RADIUS), or when the loop also encloses the point where the other
daughter's centerline crosses the plane (both daughters in one loop near O). The same function is used for
the tracer and the Medis lumen in medis_compare.py, so both diameters come from one method.
Open: tracer_rings (a contour per point) stays unimplemented; the cohort asymmetry is to be computed with
surface_diameters (not yet wired into progression_who_pooled.py).
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bifurcation_angle import point_at_depth

DEPTHS = (5.0, 10.0)  # mm from O along the LAD and the LCx, the interval of bifurcation_angle.DEPTHS
LM_OSTIUM = (0.0, 2.0)  # mm from the ostium along the left main, sec:method-ratio
STEP = 0.5  # mm between the depths the median is taken at, the step of bifurcation_angle.DEPTHS
SECTION_DEPTHS = np.arange(DEPTHS[0], DEPTHS[1] + 1e-9, STEP)  # the 11 cuts of surface_diameters
TANGENT = 1.0  # mm before and after the point for the direction of the cut's normal
CUT_RADIUS = 10.0  # mm: only triangles with a vertex this close to the centerline point take part in a cut


def contour_area(ring):
    """Area of the closed lumen contour ring (m, 3) in 3D: half the norm of the summed cross products of
    consecutive vertices about the centroid (exact for a planar polygon)."""
    r = np.asarray(ring, float)
    r = r - r.mean(axis=0)
    return 0.5 * float(np.linalg.norm(np.cross(r, np.roll(r, -1, axis=0)).sum(axis=0)))


def contour_diameter(ring):
    """Area-equivalent diameter 2 sqrt(A / pi) of one lumen contour, in the unit of the points (mm)."""
    return 2.0 * np.sqrt(contour_area(ring) / np.pi)


def reference_diameter(s, D, lo=DEPTHS[0], hi=DEPTHS[1], step=STEP):
    """Median of D taken every step mm over [lo, hi] (linear interpolation between the contours with a
    diameter), so the value does not depend on how densely the points are spaced; nan when the vessel does
    not reach hi or fewer than 2 points with a diameter fall in the interval."""
    s, D = np.asarray(s, float), np.asarray(D, float)
    if len(s) == 0 or s[-1] < hi:
        return np.nan
    ok = np.isfinite(D)
    if ((s >= lo) & (s <= hi) & ok).sum() < 2:
        return np.nan
    return float(np.median(np.interp(np.arange(lo, hi + 1e-9, step), s[ok], D[ok])))


def lm_ratios(lad, cx, lm, depths=DEPTHS, lm_window=LM_OSTIUM):
    """The two features from (s, D) of the LAD, the LCx and the LM: arc length from O for the daughters,
    from the ostium for the LM. The asymmetry is kept when the LM diameter is missing."""
    d_lad, d_cx = (reference_diameter(s, D, *depths) for s, D in (lad, cx))
    d_lm = reference_diameter(*lm, *lm_window)
    asym = float(np.log(d_cx / d_lad)) if np.isfinite(d_lad) and np.isfinite(d_cx) else np.nan
    finet = float(d_lm / (d_lad + d_cx)) if np.isfinite(asym) and np.isfinite(d_lm) else np.nan
    return {"asymmetry": asym, "finet": finet}


def narrower_rows(asym):
    """Value of the asymmetry a = ln(D_LCx / D_LAD) on the pLAD and pCX rows: |a| on the narrower daughter,
    0 on the wider one (a > 0: the LAD is the narrower). nan on both when a is missing."""
    if not np.isfinite(asym):
        return {"plad": np.nan, "pcx": np.nan}
    return {"plad": max(asym, 0.0), "pcx": max(-asym, 0.0)}


def _arc(Y):
    return np.r_[0, np.cumsum(np.linalg.norm(np.diff(Y, axis=0), axis=1))]


def surface(path):
    """(vertices (n, 3), triangles (m, 3)) of a legacy VTK surface: POLYGONS fan-triangulated, TRIANGLE_STRIPS
    unrolled; ValueError when the file has neither (a contour file of rings or lines, not a surface)."""
    import centerline_qc as cq

    v = cq.read_vtk_legacy(Path(path).read_bytes())
    tris = [(c[0], c[k], c[k + 1]) for c in v["cells"].get("POLYGONS", []) for k in range(1, len(c) - 1)]
    tris += [(c[k], c[k + 1], c[k + 2]) for c in v["cells"].get("TRIANGLE_STRIPS", []) for k in range(len(c) - 2)]
    if not tris:
        raise ValueError("no POLYGONS or TRIANGLE_STRIPS: not a surface")
    return np.asarray(v["points"], float), np.asarray(tris, int)


def merge(surfaces):
    """One (vertices, triangles) from several, e.g. the Medis lumen meshes of one participant."""
    V, F, k = [], [], 0
    for v, f in surfaces:
        V.append(v)
        F.append(f + k)
        k += len(v)
    return np.concatenate(V), np.concatenate(F)


def section_loops(V, F, p, n):
    """Closed loops (points (k, 3)) in which the plane through p with normal n cuts the mesh (V, F), using the
    triangles with a vertex within CUT_RADIUS of p. A vertex on the plane counts as on its positive side.
    Chains that do not close (a mesh border, or the radius) are dropped."""
    F = F[(np.linalg.norm(V - p, axis=1) <= CUT_RADIUS)[F].any(axis=1)]
    d = (V - p) @ n
    pos = d[F] >= 0
    point, links = {}, {}
    for tri in F[pos.any(axis=1) & ~pos.all(axis=1)]:
        ends = []
        for a, b in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])):
            if (d[a] >= 0) != (d[b] >= 0):
                e = (min(a, b), max(a, b))
                point.setdefault(e, V[a] + d[a] / (d[a] - d[b]) * (V[b] - V[a]))
                ends.append(e)
        links.setdefault(ends[0], []).append(ends[1])
        links.setdefault(ends[1], []).append(ends[0])
    loops, seen = [], set()
    for start in links:
        if start in seen:
            continue
        chain, prev, cur, closed = [start], None, start, False
        seen.add(start)
        while len(links[cur]) == 2:
            nxt = links[cur][0] if links[cur][0] != prev else links[cur][1]
            if nxt == start:
                closed = True
                break
            if nxt in seen:
                break
            chain.append(nxt)
            seen.add(nxt)
            prev, cur = cur, nxt
        if closed and len(chain) >= 3:
            loops.append(np.array([point[e] for e in chain]))
    return loops


def _inside(loop, q, p, n):
    """Whether q (in the plane) lies inside the closed loop, in the plane's own 2D coordinates (ray casting)."""
    e1 = np.cross(n, [1.0, 0, 0] if abs(n[0]) < 0.9 else [0, 1.0, 0])
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(n, e1)
    x, y = (loop - q) @ e1, (loop - q) @ e2
    x2, y2 = np.roll(x, -1), np.roll(y, -1)
    cross = (y > 0) != (y2 > 0)
    xs = x[cross] + (0 - y[cross]) * (x2[cross] - x[cross]) / (y2[cross] - y[cross])
    return bool((xs > 0).sum() % 2)


def crossings(Y, p, n):
    """Points where the polyline Y crosses the plane through p with normal n, within CUT_RADIUS of p."""
    d = (Y - p) @ n
    k = np.flatnonzero((d[:-1] >= 0) != (d[1:] >= 0))
    q = Y[k] + (d[k] / (d[k] - d[k + 1]))[:, None] * (Y[k + 1] - Y[k])
    return q[np.linalg.norm(q - p, axis=1) <= CUT_RADIUS]


def surface_diameters(V, F, Y, s, other, depths=SECTION_DEPTHS):
    """Area-equivalent lumen diameter (mm) at each depth of one daughter (Y, s: arc length from O), from the
    mesh (V, F); other: the other daughter's centerline points. nan at a depth without a clean cross-section."""
    out = []
    for dep in depths:
        p, a, b = (point_at_depth(Y, s, x) for x in (dep, max(dep - TANGENT, 0.0), dep + TANGENT))
        if p is None or b is None:
            out.append(np.nan)
            continue
        n = (b - a) / np.linalg.norm(b - a)
        inner = [lp for lp in section_loops(V, F, p, n) if _inside(lp, p, p, n)]
        if not inner:
            out.append(np.nan)
            continue
        lp = min(inner, key=contour_area)
        merged = any(_inside(lp, q, p, n) for q in crossings(np.asarray(other, float), p, n))
        out.append(np.nan if merged else contour_diameter(lp))
    return np.array(out)


def tracer_rings(path):
    """Lumen contour per centerline point of a tracer tree."""
    raise NotImplementedError(
        "tracer_rings: the lumen predictions hold a surface mesh, no contour per step (lumen_probe.md, "
        "2026-11-19); use surface_diameters on tracer_io.tracer_lumen")


def tree_ratios(tree, rings_of, roots=None):
    """Asymmetry and Finet's ratio of one tree. rings_of(Y) gives the lumen contour (m, 3) of each
    centerline point of Y (n, 3), or None where there is none. nan without an LM label (bifurcation_angle.has_lm).
    roots: the tree's own ostia, as split_trunks.split takes them (tracer_io.tracer_ostia)."""
    from bifurcation_angle import has_lm
    from split_trunks import graph, left_main, split  # here so --check runs without the shared modules

    nan = {"asymmetry": np.nan, "finet": np.nan}
    if not has_lm(tree):
        return nan
    X, lab, G = graph(tree)
    roots = roots or {}
    arteries = split(X, lab, G, roots=roots)
    if "LAD" not in arteries or "CX" not in arteries:
        return nan
    (*_, Yl, sl), (*_, Yc, sc) = arteries["LAD"], arteries["CX"]
    if not np.allclose(Yl[0], Yc[0]):
        return nan  # no shared bifurcation point, as in bifurcation_angle.lm_angle
    Ym = left_main(X, lab, G, roots)
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

    # model rows: |a| on the narrower daughter only
    rows = narrower_rows(r["asymmetry"])  # the LCx (2.25 mm) is the narrower
    assert rows["plad"] == 0.0 and abs(rows["pcx"] - np.log(d_lad / d_cx)) < 1e-4, "narrower LCx: pCX row only"
    rows = narrower_rows(lm_ratios(cx, lad, lm)["asymmetry"])  # swapped: the LAD is the narrower
    assert rows["pcx"] == 0.0 and abs(rows["plad"] - np.log(d_lad / d_cx)) < 1e-4, "narrower LAD: pLAD row only"
    assert narrower_rows(lm_ratios(cx, cx, lm)["asymmetry"]) == {"plad": 0.0, "pcx": 0.0}, "equal daughters: 0, 0"
    assert all(np.isnan(v) for v in narrower_rows(np.nan).values()), "missing asymmetry: nan on both rows"

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
    assert abs(a - taper(7.5)) < 1e-9 and abs(b - taper(7.5)) < 1e-9, "median of a linear taper is mid-window"
    # points crowded into the first millimetre of the window must not pull the median there
    s_crowd = np.r_[np.linspace(0, 5, 11), np.linspace(5, 6, 200), np.linspace(6.5, 20, 28)]
    assert abs(reference_diameter(s_crowd, taper(s_crowd)) - taper(7.5)) < 1e-9, "crowded points must not count more"
    check_surface()
    print("all checks passed")


def _tube_mesh(origin, direction, D, length, step=0.25, m=64):
    """Triangle mesh of a straight open tube of diameter D (rings of m points every step mm)."""
    u = np.asarray(direction, float) / np.linalg.norm(direction)
    rings = [_ring(np.asarray(origin, float) + x * u, u, D / 2, D / 2, m) for x in np.arange(0, length + 1e-9, step)]
    V = np.concatenate(rings)
    F = [(i * m + j, i * m + (j + 1) % m, (i + 1) * m + j) for i in range(len(rings) - 1) for j in range(m)]
    F += [(i * m + (j + 1) % m, (i + 1) * m + (j + 1) % m, (i + 1) * m + j) for i in range(len(rings) - 1) for j in range(m)]
    return V, np.array(F)


def check_surface():
    """Known diameters from plane cuts of tube meshes."""
    d_lad, d_cx = 2.75, 2.25
    u_lad, u_cx = np.array([1, 0.4, 0.0]), np.array([1, -0.6, 0.2])
    V, F = merge([_tube_mesh(0.5 * u_lad / np.linalg.norm(u_lad), u_lad, d_lad, 30),
                  _tube_mesh(0.5 * u_cx / np.linalg.norm(u_cx), u_cx, d_cx, 30)])
    line = lambda u, L: np.linspace(0, L, 121)[:, None] * u / np.linalg.norm(u)  # noqa: E731
    lad, cx = line(u_lad, 30), line(u_cx, 30)
    D_lad = surface_diameters(V, F, lad, _arc(lad), cx)
    D_cx = surface_diameters(V, F, cx, _arc(cx), lad)
    poly = np.sqrt(64 * np.sin(2 * np.pi / 64) / (2 * np.pi))  # a 64-gon's area-equivalent diameter / D
    assert np.allclose(D_lad, d_lad * poly, rtol=2e-3) and np.allclose(D_cx, d_cx * poly, rtol=2e-3), (D_lad, D_cx)
    a = np.log(reference_diameter(SECTION_DEPTHS, D_cx) / reference_diameter(SECTION_DEPTHS, D_lad))
    assert abs(a - np.log(d_cx / d_lad)) < 1e-3, a
    print(f"plane cuts of tube meshes: LAD {np.median(D_lad):.3f}, LCx {np.median(D_cx):.3f} mm "
          f"(64-gons of {d_lad}, {d_cx}); asymmetry {a:.4f}")
    # the mesh ends at 8 mm: no closed loop beyond it
    V8, F8 = _tube_mesh(np.zeros(3), u_lad, d_lad, 8)
    D8 = surface_diameters(V8, F8, lad, _arc(lad), cx)
    assert np.isfinite(D8[SECTION_DEPTHS <= 7.5]).all() and np.isnan(D8[SECTION_DEPTHS >= 8.5]).all(), D8
    # one wide tube around both daughters (they run 0.75 mm apart at 5 mm): no diameter
    near_cx = line([1, 0.15, 0], 30)
    Vw, Fw = _tube_mesh(np.zeros(3), [1, 0, 0], 8.0, 30)
    assert np.isnan(surface_diameters(Vw, Fw, line([1, 0, 0], 30), _arc(line([1, 0, 0], 30)), near_cx)).all()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="run the synthetic-shape checks")
    if ap.parse_args().check:
        check()
    else:
        ap.print_help()
