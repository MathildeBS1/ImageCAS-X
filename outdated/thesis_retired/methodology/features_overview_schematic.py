"""Overview figure for Section sec:method-features: the four geometric features on one made-up left
coronary tree, in the manner of a 3D lumen render with labelled landmarks.

    python thesis/methodology/features_overview_schematic.py

A made-up LM, LAD and LCx with D1, D2 and OM1 stubs (no patient data). Every number in the figure
comes from the code the thesis describes, run on this tree:
  A  curvature   profile_thesis / _at_chord (tortuosity/curvature.py) and mean_turning
                 (CGPS_data/thesis_final/turning_feature.py), on the whole LAD, cut at made-up p/m/d
                 boundaries placed at the D1 and D2 origins.
  B  angle       lm_bifurcation_angle (CGPS_data/who_where_readiness.py): directions from the LM point
                 nearest each daughter start to the mean of its 2-8 mm stretch.
  C  ratios      NO CODE YET: the diameters are drawn at made-up positions (sec:method-ratio is open).
  D  taper       resample_arc, tangents, cross_section_radius, branch_keep and taper
                 (tortuosity/taper.py) on a voxel label volume of the tree, the LAD as one artery.
The lumen is a smooth union of tubes, voxelised at 0.3 mm for the taper code and drawn as its 0-level
surface. Writes features_overview_schematic.{pdf,png} next to this file. Thesis style: serif, white,
no title. Needs pyvista (off-screen VTK).
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv
from matplotlib.patches import FancyArrowPatch
from scipy.interpolate import CubicSpline
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "CGPS_data"))
sys.path.insert(0, str(ROOT / "CGPS_data" / "thesis_final"))
from tortuosity.curvature import _at_chord, profile_thesis  # noqa: E402
from tortuosity.taper import branch_keep, cross_section_radius, resample_arc, taper, tangents  # noqa: E402
from turning_feature import CHORD, trunk_turning  # noqa: E402
from who_where_readiness import lm_bifurcation_angle  # noqa: E402

OUT = Path(__file__).with_suffix("")
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#dcdbd6", "white"
PMD = ("#2a78d6", "#eb6834", "#1baf7a")  # proximal / mid / distal, as in turning_feature_schematic.py
HI = ("#5b3cc4", "#b8327a")  # as P_i and P_i+1 there: here LAD and LCx, and the measured quantity
LUMEN = "#9db4c0"
plt.rcParams.update({"font.family": "serif", "font.serif": ["STIX Two Text", "STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix", "font.size": 8.5, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF})


# ---------------------------------------------------------------- made-up tree (LPS-like mm)
def curve(ctrl, step=0.1):
    """Dense polyline (step mm) through the control points, and its arc length."""
    ctrl = np.asarray(ctrl, float)
    t = np.r_[0, np.cumsum(np.linalg.norm(np.diff(ctrl, axis=0), axis=1))]
    f = CubicSpline(t, ctrl, bc_type="natural")
    fine = f(np.linspace(0, t[-1], int(t[-1] / 0.02)))
    P, _ = resample_arc(fine, step)
    return P, np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]


def at(P, s, x):
    return P[int(np.argmin(np.abs(s - x)))]


# Laid out in view coordinates (x right, z up, y depth away from the viewer), with some depth on
# every bend so that the curvature is three-dimensional.
LM, s_lm = curve([(0, 0, 0), (5, 0.8, -0.6), (10, 1.2, -2.2)])
BIF = LM[-1]
LAD, s_lad = curve([BIF, (14, -1.5, -6.5), (18.5, -3.5, -13), (21.5, -5.5, -20.5), (22.6, -4.8, -27.5),
                    (21, -2.5, -33.5), (21.8, -1.2, -39.5), (25.5, -2.8, -45.5), (28.8, -4.6, -53),
                    (30.6, -3.8, -61.5), (31.4, -1, -70), (30.4, 2.2, -78), (28.5, 5, -84.5)])
LCX, s_lcx = curve([BIF, (8.6, 3.8, -6.2), (5.8, 6.6, -11.8), (1.8, 8.8, -17.6), (-2.6, 10, -23.8),
                    (-6.2, 10.2, -30.8), (-8.8, 9.4, -38.4), (-10.4, 8.2, -46)])
D1_S, D2_S, OM1_S = 21.0, 47.0, 23.0  # mm along the LAD / LCx where the side branches leave
BOUNDS = (0.0, D1_S, D2_S, s_lad[-1])  # made-up p/m/d boundaries of the LAD, at the D1 and D2 origins


def branch(P, s, x, d, n, length):
    """A side-branch stub from P at arc x: leaves along the tangent turned by d, bending toward n."""
    o, t = at(P, s, x), at(P, s, x + 1) - at(P, s, x - 1)
    t /= np.linalg.norm(t)
    d0 = t + np.asarray(d, float)
    d0 /= np.linalg.norm(d0)
    n = np.asarray(n, float)
    return curve([o, o + 0.4 * length * d0, o + 0.75 * length * d0 + 0.2 * length * n,
                  o + length * d0 + 0.45 * length * n])


D1, s_d1 = branch(LAD, s_lad, D1_S, (1.6, 0.4, 0.5), (0.1, 0.2, -1), 28)
D2, s_d2 = branch(LAD, s_lad, D2_S, (1.5, 0.4, 0.5), (0.1, 0.2, -1), 22)
OM1, s_om1 = branch(LCX, s_lcx, OM1_S, (0.9, 0.3, -0.8), (0.5, 0.1, -0.6), 25)


def steps(s, at_mm, factor):
    """Radius factor that drops smoothly by factor over 3 mm after each branch origin."""
    out = np.ones_like(s)
    for x, f in zip(at_mm, factor):
        out *= 1 - (1 - f) / (1 + np.exp(-(s - x - 1.5) / 0.5))
    return out


R = {"LM": 2.25 - 0.012 * s_lm,
     "LAD": 1.92 * np.exp(-0.0062 * s_lad) * steps(s_lad, (D1_S, D2_S), (0.91, 0.93)),
     "LCx": 1.68 * np.exp(-0.0055 * s_lcx) * steps(s_lcx, (OM1_S,), (0.9,)),
     "D1": 1.08 * np.exp(-0.012 * s_d1), "D2": 0.92 * np.exp(-0.014 * s_d2), "OM1": 1.0 * np.exp(-0.012 * s_om1)}
VESSELS = {"LM": LM, "LAD": LAD, "LCx": LCX, "D1": D1, "D2": D2, "OM1": OM1}
LABEL = {k: i + 1 for i, k in enumerate(VESSELS)}


# ---------------------------------------------------------------- voxel lumen (smooth union of tubes)
H = 0.3  # mm
allp = np.vstack(list(VESSELS.values()))
ORIG = allp.min(0) - 4
DIMS = np.ceil((allp.max(0) + 4 - ORIG) / H).astype(int) + 1
grid = np.stack(np.meshgrid(*[ORIG[k] + H * np.arange(DIMS[k]) for k in range(3)], indexing="ij"), -1).reshape(-1, 3)
fields = []
for k, P in VESSELS.items():
    d, j = cKDTree(P).query(grid, distance_upper_bound=4.5, workers=-1)
    f = np.full(len(grid), 9.0)
    ok = np.isfinite(d)
    f[ok] = d[ok] - R[k][j[ok]]
    fields.append(f)
fields = np.array(fields)
KS = 0.35  # mm, blend width at the junctions
union = -KS * np.log(np.exp(-fields / KS).sum(0))
labels = np.where(union < 0, np.argmin(fields, 0) + 1, 0).reshape(DIMS).astype(np.int16)
FLIP = np.diag([-1.0, -1.0, 1.0])
affine = np.eye(4)
affine[:3, :3], affine[:3, 3] = FLIP * H, FLIP @ ORIG  # voxel -> RAS, the points above being LPS
img = pv.ImageData(dimensions=DIMS, spacing=(H, H, H), origin=ORIG)
img.point_data["f"] = union.reshape(DIMS).ravel(order="F")  # VTK points run x fastest
surface = img.contour([0.0], scalars="f").smooth_taubin(n_iter=40, pass_band=0.05).compute_normals()


# ---------------------------------------------------------------- tracer-like centerline points
rng = np.random.default_rng(11)


def tracer_points(P, s):
    """Unevenly spaced points (0.4-1.4 mm apart) on the dense curve, as a tracer would step."""
    t = np.r_[0, np.cumsum(rng.uniform(0.4, 1.4, 400))]
    t = t[t <= s[-1]]
    return np.column_stack([np.interp(t, s, P[:, k]) for k in range(3)])


def arc(P):
    return np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]


LMp, LADp, LCXp = tracer_points(LM, s_lm), tracer_points(LAD, s_lad), tracer_points(LCX, s_lcx)
LADs = arc(LADp)



# ---------------------------------------------------------------- the four features, by the thesis code
# A: curvature profile on the whole LAD, then the arc-length mean per segment
pos, kappa = profile_thesis(LADp, CHORD, LADs)
T_seg = trunk_turning(LADp, LADs, BOUNDS)
mid = (pos > D1_S + 4) & (pos < D2_S - 4)
i0 = int(np.flatnonzero(np.isclose(LADs, pos[mid][np.argmax(kappa[mid])]))[0])  # P_i on the sharpest mid bend
B0, F0 = _at_chord(LADp, i0, CHORD, -1), _at_chord(LADp, i0, CHORD, 1)
a0, b0 = LADp[i0] - B0, F0 - LADp[i0]
theta0 = np.arctan2(np.linalg.norm(np.cross(a0, b0)), a0 @ b0)

# B: LM bifurcation angle; the drawing repeats the steps of lm_bifurcation_angle (lo = 2, hi = 8 mm)
RUNS = {"lm": LMp, "plad": LADp[LADs <= D1_S], "pcx": LCXp[arc(LCXp) <= OM1_S]}
ALPHA = lm_bifurcation_angle(RUNS)
ANG = {}
for name, br in (("LAD", RUNS["plad"]), ("LCx", RUNS["pcx"])):
    bif = LMp[np.linalg.norm(LMp - br[0], axis=1).argmin()]
    sb = arc(br)
    stretch = br[(sb >= 2) & (sb <= 8)]
    ANG[name] = (bif, stretch, stretch.mean(0))
u_ = [(m - b) / np.linalg.norm(m - b) for b, _, m in ANG.values()]
assert np.isclose(np.degrees(np.arccos(np.clip(u_[0] @ u_[1], -1, 1))), ALPHA)

# C: diameter ratios. No thesis code yet: made-up radii read at made-up positions.
RATIO_AT = {"LM": (LM, s_lm, 3.5), "LAD": (LAD, s_lad, 6.0), "LCx": (LCX, s_lcx, 7.5)}
DIAM = {k: 2 * float(np.interp(x, s, R[k])) for k, (_, s, x) in RATIO_AT.items()}

# D: taper of the whole LAD from its voxel lumen
Q, sq = resample_arc(LADp, 0.5)
tq = tangents(Q)
rq, touch = cross_section_radius(Q, tq, labels, affine, {LABEL["LAD"]})
JUNC = [0.0] + [float(sq[np.linalg.norm(Q - at(LAD, s_lad, x), axis=1).argmin()]) for x in (D1_S, D2_S)]
keep = branch_keep(sq, JUNC, rq) & ~touch
TAPER, span, frac, why = taper(sq, rq, keep)
used = keep & np.isfinite(rq) & (rq > 0)
from scipy.stats import theilslopes  # noqa: E402
slope, icpt = theilslopes(np.log(rq[used]), sq[used])[:2]
print(f"T_s (LAD p/m/d) = {np.round(T_seg, 4)} rad/mm; theta_i = {np.degrees(theta0):.1f} deg at s = {LADs[i0]:.1f} mm")
print(f"alpha = {ALPHA:.1f} deg; diameters {DIAM}")
print(f"taper T = {TAPER:.3f} over {span:.0f} mm, {frac:.0%} of {len(sq)} samples kept ({why})")


# ---------------------------------------------------------------- 3D rendering
def tube(P, r):
    return pv.Spline(P, max(len(P) * 3, 50)).tube(radius=r, n_sides=16)


def ring(c, t, r, w):
    """A torus-like ring of radius r around c in the plane normal to t."""
    t = t / np.linalg.norm(t)
    u = np.cross(t, [0, 0, 1.0] if abs(t[2]) < 0.9 else [1.0, 0, 0])
    u /= np.linalg.norm(u)
    v = np.cross(t, u)
    a = np.linspace(0, 2 * np.pi, 73)
    return pv.Spline(c + r * (np.cos(a)[:, None] * u + np.sin(a)[:, None] * v), 73).tube(radius=w, n_sides=8)


def ring_pts(c, t, r):
    """A closed circle of radius r around c in the plane normal to t, as points."""
    t = t / np.linalg.norm(t)
    u = np.cross(t, [0, 0, 1.0] if abs(t[2]) < 0.9 else [1.0, 0, 0])
    u /= np.linalg.norm(u)
    a = np.linspace(0, 2 * np.pi, 73)
    return c + r * (np.cos(a)[:, None] * u + np.sin(a)[:, None] * np.cross(t, u))


def arc_pts(c, d1, d2, rad, n=40):
    """Points on the circular arc of radius rad around c from direction d1 to d2 (in their plane)."""
    d1, d2 = d1 / np.linalg.norm(d1), d2 / np.linalg.norm(d2)
    ang = np.arccos(np.clip(d1 @ d2, -1, 1))
    w = d2 - (d1 @ d2) * d1
    w /= np.linalg.norm(w)
    return np.array([c + rad * (np.cos(x) * d1 + np.sin(x) * w) for x in np.linspace(0, ang, n)])


def tangent_at(P, s, x, h=1.0):
    d = at(P, s, x + h) - at(P, s, x - h)
    return d / np.linalg.norm(d)


def render(draw, focal, direction, scale, size, marks):
    """Render one panel off-screen with parallel projection; return the RGBA image and the pixel
    position of each named 3D point in marks."""
    pl = pv.Plotter(off_screen=True, window_size=size)
    pl.set_background("white")
    draw(pl)
    pl.enable_parallel_projection()
    d = np.asarray(direction, float)
    pl.camera.focal_point, pl.camera.position, pl.camera.up = focal, focal + 300 * d / np.linalg.norm(d), (0, 0, 1)
    pl.camera.parallel_scale = scale
    pl.enable_depth_peeling(12)
    img = pl.screenshot(transparent_background=True, return_img=True)
    ren, px = pl.renderer, {}
    for k, X in marks.items():
        ren.SetWorldPoint(*X, 1.0)
        ren.WorldToDisplay()
        x, y, _ = ren.GetDisplayPoint()
        px[k] = (x, size[1] - y)
    pl.close()
    return img, px


def lumen(pl, opacity=0.28):
    pl.add_mesh(surface, color=LUMEN, opacity=opacity, smooth_shading=True, specular=0.25, specular_power=20)


VIEW = (-45, -240, 35)  # from the front, slightly from the left and above
VIEW_C = (-110, -220, 120)  # C: more from the left and above, so the rings open up
SIZE = (1300, 1300)
C_ALL = allp.mean(0) + np.array([0, 0, 2])


def draw_A(pl):
    lumen(pl)
    for P, s in ((LMp, arc(LMp)), (LCXp, arc(LCXp))):
        pl.add_mesh(tube(P, 0.16), color=INK2)
    for P in (D1, D2, OM1):
        pl.add_mesh(tube(P[::6], 0.12), color=MUTED)
    for k in range(3):
        sel = (LADs >= BOUNDS[k] - 0.6) & (LADs <= BOUNDS[k + 1] + 0.6)
        pl.add_mesh(tube(LADp[sel], 0.32), color=PMD[k])
    for x in BOUNDS[1:3]:
        pl.add_mesh(ring(at(LAD, s_lad, x), tangent_at(LAD, s_lad, x), np.interp(x, s_lad, R["LAD"]) + 0.55, 0.16), color=INK)
    P0 = LADp[i0]
    pl.add_mesh(tube(np.array([B0, P0]), 0.3), color=HI[0])
    pl.add_mesh(tube(np.array([P0, F0]), 0.3), color=HI[0])
    pl.add_mesh(pv.Sphere(radius=0.75, center=P0), color=HI[0])
    for X in (B0, F0):
        pl.add_mesh(pv.Sphere(radius=0.6, center=X), color="white", specular=0.2)
        pl.add_mesh(tube(ring_pts(X, np.asarray(VIEW, float), 0.62), 0.12), color=HI[0])


def draw_B(pl):
    lumen(pl, 0.22)
    for P in (LMp, LADp[LADs < 16], LCXp[arc(LCXp) < 16]):
        pl.add_mesh(tube(P, 0.07), color=INK2)
        pl.add_mesh(pv.PolyData(P).glyph(geom=pv.Sphere(radius=0.16), scale=False), color=INK2)
    for (name, (bif, stretch, m)), c in zip(ANG.items(), HI):
        pl.add_mesh(tube(stretch, 0.16), color=c)
        d = (m - bif) / np.linalg.norm(m - bif)
        tip = bif + 11.5 * d
        pl.add_mesh(tube(np.array([bif, tip - 1.1 * d]), 0.1), color=c)
        pl.add_mesh(pv.Cone(center=tip - 0.55 * d, direction=d, height=1.1, radius=0.38, resolution=24), color=c)
        pl.add_mesh(pv.Sphere(radius=0.42, center=m), color="white", specular=0.2)
        pl.add_mesh(tube(ring_pts(m, np.asarray(VIEW, float), 0.44), 0.07), color=c)
    bif = ANG["LAD"][0]
    pl.add_mesh(pv.Sphere(radius=0.45, center=bif), color=INK)
    pl.add_mesh(tube(arc_pts(bif, *[ANG[k][2] - bif for k in ANG], 4.2), 0.07), color=INK)


def draw_C(pl):
    lumen(pl, 0.22)
    for P in (LMp, LADp[LADs < 16], LCXp[arc(LCXp) < 16]):
        pl.add_mesh(tube(P, 0.07), color=MUTED)
    for k, (P, s, x) in RATIO_AT.items():
        c, tn, r = at(P, s, x), tangent_at(P, s, x), DIAM[k] / 2
        pl.add_mesh(ring(c, tn, r, 0.09), color=HI[1])
        side = np.cross(tn, np.asarray(VIEW_C, float))  # in the ring plane, across the view: full length
        side /= np.linalg.norm(side)
        pl.add_mesh(tube(np.array([c - r * side, c + r * side]), 0.06), color=INK)
        for e in (c - r * side, c + r * side):
            pl.add_mesh(pv.Sphere(radius=0.14, center=e), color=INK)


def draw_D(pl):
    lumen(pl, 0.2)
    pl.add_mesh(tube(LADp, 0.09), color=INK2)
    for k in range(len(Q)):
        ok = used[k]
        pl.add_mesh(ring(Q[k], tq[k], rq[k] if np.isfinite(rq[k]) else 1.0, 0.035 if ok else 0.03),
                    color=HI[1] if ok else "#b9b8b3")


def mid_of(P, s, a, b):
    return at(P, s, (a + b) / 2)


# A: overview
imgA, pxA = render(draw_A, C_ALL + np.array([0, 0, -6]), VIEW, 52, SIZE, {
    "ostium": LM[0], "LM": at(LM, s_lm, 4), "LCx": at(LCX, s_lcx, 30), "D1": D1[-1], "D2": D2[-1], "OM1": OM1[-1],
    "p": mid_of(LAD, s_lad, 0, D1_S), "m": mid_of(LAD, s_lad, D1_S, D2_S), "d": mid_of(LAD, s_lad, D2_S, s_lad[-1]),
    "P": LADp[i0], "B": B0, "F": F0, "lad": at(LAD, s_lad, 76)})
# B and C: the left main bifurcation
C_BIF = BIF + np.array([0.5, 0, -4.5])
imgB, pxB = render(draw_B, C_BIF, VIEW, 9.5, SIZE, {
    "bif": ANG["LAD"][0], "mLAD": ANG["LAD"][2], "mLCx": ANG["LCx"][2],
    "LAD2": ANG["LAD"][1][0], "LAD8": ANG["LAD"][1][-1], "LCx2": ANG["LCx"][1][0], "LCx8": ANG["LCx"][1][-1],
    "tipLAD": ANG["LAD"][0] + 11.5 * u_[0], "tipLCx": ANG["LCx"][0] + 11.5 * u_[1],
    "alpha": arc_pts(ANG["LAD"][0], *[ANG[k][2] - ANG["LAD"][0] for k in ANG], 5.4)[20], "LM": at(LM, s_lm, 3)})
imgC, pxC = render(draw_C, C_BIF + np.array([0, 0, 0.8]), VIEW_C, 10.5, SIZE, {k: at(P, s, x) for k, (P, s, x) in RATIO_AT.items()})
# D: the LAD as one artery
C_LAD = LAD.mean(0) + np.array([3, 0, 0])
imgD, pxD = render(draw_D, C_LAD + np.array([9, 0, -3]), (-90, -230, 70), 52, SIZE, {
    "start": Q[0], "D1": at(LAD, s_lad, D1_S), "D2": at(LAD, s_lad, D2_S), "end": Q[-1]})


# ---------------------------------------------------------------- composition
def tag(ax, xy, text, dx, dy, color=INK2, fs=7.5, box=True, ha="center"):
    """A landmark label with a thin leader line, boxed as in a 3D viewer."""
    kw = dict(boxstyle="round,pad=0.18,rounding_size=0.1", fc="white", ec=GRID, lw=0.6) if box else None
    ax.annotate(text, xy, xytext=(xy[0] + dx, xy[1] + dy), fontsize=fs, color=color, ha=ha, va="center",
                bbox=kw, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6, shrinkA=0, shrinkB=2))


CELL = 1.17  # height / width of one panel cell


def panel(ax, img, letter, title, x0, x1, y0):
    """Show img cropped to [x0, x1] from y0 down, at the cell aspect; y0 may lie above the image to
    leave room for the title."""
    ax.imshow(img, interpolation="lanczos")
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0 + CELL * (x1 - x0), y0)
    ax.set_axis_off()
    ax.text(0.035, 0.985, letter, transform=ax.transAxes, fontsize=12, color=INK, va="top")
    ax.text(0.105, 0.982, title, transform=ax.transAxes, fontsize=8.5, color=INK2, va="top", linespacing=1.25)


fig = plt.figure(figsize=(6.5, 6.5 * CELL))
gs = fig.add_gridspec(2, 2, left=0.004, right=0.996, bottom=0.004, top=0.996, wspace=0.0, hspace=0.0)
axA, axB, axC, axD = (fig.add_subplot(gs[i, j]) for i in range(2) for j in range(2))

# A
panel(axA, imgA, "A", "Curvature: turning angle $\\theta$ between\n5 mm chords, averaged per segment", 150, 1250, -60)
tag(axA, pxA["ostium"], "ostium", -60, -60)
tag(axA, pxA["LM"], "LM", 60, -70)
tag(axA, pxA["LCx"], "LCx", -90, 20)
tag(axA, pxA["OM1"], "OM1", -10, 50)
tag(axA, pxA["D1"], "D1", 45, 0)
tag(axA, pxA["D2"], "D2", 45, 0)
for k, (key, dx) in enumerate((("p", -190), ("m", -205), ("d", -205))):
    tag(axA, pxA[key], f"{('proximal', 'mid', 'distal')[k]}\n$T_s$ = {T_seg[k]:.3f}", dx, 25, color=PMD[k], fs=8, box=False)
tag(axA, pxA["P"], "$P_i$", 85, 0, color=HI[0], fs=9, box=False)
tag(axA, pxA["B"], "$B_i$", 75, -35, color=HI[0], fs=9, box=False)
tag(axA, pxA["F"], "$F_i$", -75, 35, color=HI[0], fs=9, box=False)
axA.text(0.97, 0.03, rf"$\theta_i$ = {np.degrees(theta0):.1f}° at $P_i$" + "\n" + r"$T_s$ in rad/mm",
         transform=axA.transAxes, ha="right", va="bottom", fontsize=8, color=INK2)

# B
panel(axB, imgB, "B", "Bifurcation angle $\\alpha$: directions to the\nmean of the 2–8 mm points of each daughter", 60, 1240, -40)
tag(axB, pxB["LM"], "LM", 30, 90)
tag(axB, pxB["tipLAD"], "LAD", -10, 90, color=HI[0])
tag(axB, pxB["tipLCx"], "LCx", -60, 40, color=HI[1])
tag(axB, pxB["bif"], "LM point nearest\nthe daughter start", 190, -110, fs=7)
tag(axB, pxB["LAD2"], "2 mm", 85, -25, color=HI[0], box=False)
tag(axB, pxB["LAD8"], "8 mm", 90, -10, color=HI[0], box=False)
tag(axB, pxB["LCx2"], "2 mm", -85, -25, color=HI[1], box=False)
tag(axB, pxB["LCx8"], "8 mm", -95, 5, color=HI[1], box=False)
tag(axB, pxB["mLCx"], "mean of the\n2–8 mm points", -260, -150, fs=7)
axB.text(*pxB["alpha"], r"$\alpha$", fontsize=11, color=INK, ha="center", va="center")
axB.text(0.97, 0.03, rf"$\alpha$ = {ALPHA:.1f}°", transform=axB.transAxes, ha="right", va="bottom", fontsize=8.5, color=INK)

# C
panel(axC, imgC, "C", "Diameter ratios: daughter over LM diameter\n(positions made up, method open)", 60, 1240, -40)
for k, (dx, dy) in (("LM", (60, -190)), ("LAD", (60, -230)), ("LCx", (-110, 230))):
    tag(axC, pxC[k], rf"$d_{{\mathrm{{{k}}}}}$ = {DIAM[k]:.1f} mm", dx, dy, color=HI[1], fs=8, box=False)
axC.text(0.97, 0.03, rf"$d_{{\mathrm{{LAD}}}}/d_{{\mathrm{{LM}}}}$ = {DIAM['LAD'] / DIAM['LM']:.2f}" + "\n"
         + rf"$d_{{\mathrm{{LCx}}}}/d_{{\mathrm{{LM}}}}$ = {DIAM['LCx'] / DIAM['LM']:.2f}",
         transform=axC.transAxes, ha="right", va="bottom", fontsize=8.5, color=INK, linespacing=1.5)

# D
panel(axD, imgD, "D", "Taper: lumen sections every 0.5 mm,\nTheil–Sen slope of ln $r$ along the LAD; grey: excluded", 100, 1200, -60)
tag(axD, pxD["D1"], "D1 origin ± 2\nmedian radii", 190, -60, fs=7)
tag(axD, pxD["D2"], "D2 origin ± 2\nmedian radii", 190, -40, fs=7)
tag(axD, pxD["start"], "first 3 mm", 150, -30, fs=7)
ins = axD.inset_axes([0.6, 0.09, 0.36, 0.28])
ins.scatter(sq[~used], np.log(rq[~used]), s=2, color="#b9b8b3", lw=0)
ins.scatter(sq[used], np.log(rq[used]), s=2, color=HI[1], lw=0)
xx = np.array([sq[used].min(), sq[used].max()])
ins.plot(xx, icpt + slope * xx, color=INK, lw=1)
ins.set_xlabel("$s$ (mm)", fontsize=7, labelpad=1)
ins.set_ylabel("ln $r$", fontsize=7, labelpad=1)
ins.tick_params(labelsize=6, length=2, colors=INK2, pad=1)
for k, sp in ins.spines.items():
    sp.set_visible(k in ("left", "bottom"))
    sp.set_color(MUTED)
ins.set_facecolor("none")
ins.text(0.98, 1.0, rf"$T = -10\,b$ = {TAPER:.3f}", transform=ins.transAxes, ha="right", va="top", fontsize=7.5, color=INK)

for ax in (axA, axB, axC, axD):  # thin panel frames, as in a 3D-viewer montage
    fig.add_artist(plt.Rectangle(ax.get_position().p0, ax.get_position().width, ax.get_position().height,
                                 transform=fig.transFigure, fill=False, ec=INK2, lw=0.6))
for ext in ("pdf", "png"):
    fig.savefig(f"{OUT}.{ext}", dpi=300)
print(f"wrote {OUT}.pdf/.png")
