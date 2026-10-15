"""Normalised lumen taper T of a coronary trunk: the fractional loss of lumen radius per 10 mm.

T = -b * 10, where b is the Theil-Sen slope of ln r(s) against arc length s (mm) over the whole
trunk. Positive T is normal tapering; T near zero or negative means the trunk holds its calibre or
widens, the hypothesised low-shear state. The log form makes T unitless per mm and unchanged when
the whole tree is scaled, so it describes shape, not calibre
(reports/Fourth centerline feature for plaque.md; one value per trunk, not per window).

Normal trunks lose about 0.25 mm of diameter per 10 mm, roughly one voxel across a 30 mm stretch,
so no single cross-section can resolve it. T is only usable because the fit pools hundreds of
sections and ignores the radius jumps at side-branch origins:

1. The centerline is resampled every 0.5 mm. Each sample gets a tangent taken over 5 mm of arc,
   the same physical scale as T_5 (curvature.py), so taper and turning angle use one smoothing.
2. The lumen mask is cut with the plane orthogonal to that tangent. The section's area A is the
   connected component containing the centre, and r = sqrt(A / pi). This is an area-equivalent
   radius; the distance-transform radius (bifurcation.radius) follows the minor axis of
   non-circular sections and is kept only as a sensitivity check.
3. Samples are dropped when they lie within k median radii of a junction or in the first 3 mm,
   when the centre is outside the lumen, or when the section runs into another labelled vessel
   or off the sampling grid.
4. ln r is fitted against s with Theil-Sen. The trunk is missing (NaN, with a reason) when fewer
   than 20 mm of arc or fewer than 60% of the samples remain.
"""
import numpy as np
from scipy import ndimage
from scipy.stats import theilslopes

_FLIP = np.diag([-1.0, -1.0, 1.0])  # LPS <-> RAS, as in bifurcation.coords


def resample_arc(P, step=0.5):
    """Points every step mm of arc along the polyline P (n, 3), and their arc length s."""
    arc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
    s = np.arange(0.0, arc[-1] + 1e-9, step)
    return np.column_stack([np.interp(s, arc, P[:, k]) for k in range(3)]), s


def tangents(Q, step=0.5, l=5.0):
    """Unit tangent at each point of Q (spaced step mm apart), from the points l/2 mm either side.

    Near the ends the window is cut short rather than shifted.
    """
    h, n = max(int(round(l / (2 * step))), 1), len(Q)
    i = np.arange(n)
    d = Q[np.minimum(i + h, n - 1)] - Q[np.maximum(i - h, 0)]
    return d / np.linalg.norm(d, axis=1, keepdims=True)


def _plane_basis(t):
    """Two unit vectors (n, 3) orthogonal to each tangent t and to each other."""
    ref = np.where(np.abs(t[:, [0]]) < 0.9, [[1.0, 0, 0]], [[0, 1.0, 0]])  # any axis not parallel to t
    u = np.cross(t, ref)
    u /= np.linalg.norm(u, axis=1, keepdims=True)
    return u, np.cross(t, u)


def cross_section_radius(Q, t, labels, affine, own_labels, half_width=6.0, px=0.1, chunk=64):
    """Area-equivalent lumen radius (mm) at each point of Q (n, 3, LPS) on the plane normal to t.

    labels is the multi-label segmentation in voxel space (0 = background) and affine its
    voxel -> RAS matrix. The lumen is the union of all labels, read with trilinear interpolation
    and cut at 0.5, so the area resolves below one voxel. Returns (r, touch): r is NaN where the
    centre is outside the lumen; touch is True where the centre's component reaches the edge of
    the half_width grid or contains a voxel labelled outside own_labels (it has run into another
    vessel, typically at a branch origin).
    """
    Q, t = np.asarray(Q, float), np.asarray(t, float)
    inv = np.linalg.inv(affine)
    to_vox = lambda X: (X @ _FLIP) @ inv[:3, :3].T + inv[:3, 3]  # LPS -> RAS -> voxel

    # crop to the trunk plus the grid's reach, so the float copy of the mask stays small
    vox = to_vox(Q)
    reach = half_width / np.linalg.norm(affine[:3, :3], axis=0).min() + 2
    lo = np.maximum(np.floor(vox.min(0) - reach).astype(int), 0)
    hi = np.minimum(np.ceil(vox.max(0) + reach).astype(int) + 1, labels.shape)
    lab = np.asarray(labels[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]])
    lumen = (lab > 0).astype(np.float32)

    g = np.arange(-half_width, half_width + px / 2, px)
    m, c = len(g), len(g) // 2  # grid size and the index of its centre
    a, b = np.meshgrid(g, g, indexing="ij")
    u, v = _plane_basis(t)
    own = np.asarray(sorted(own_labels))
    r, touch = np.full(len(Q), np.nan), np.zeros(len(Q), bool)
    for k0 in range(0, len(Q), chunk):
        sl = slice(k0, k0 + chunk)
        X = Q[sl, None, None] + a[None, ..., None] * u[sl, None, None] + b[None, ..., None] * v[sl, None, None]
        ijk = (to_vox(X.reshape(-1, 3)) - lo).T
        occ = ndimage.map_coordinates(lumen, ijk, order=1, mode="constant").reshape(-1, m, m) >= 0.5
        near = ndimage.map_coordinates(lab, ijk, order=0, mode="constant").reshape(-1, m, m)
        for j in range(len(occ)):
            comp, _ = ndimage.label(occ[j])
            if comp[c, c] == 0:
                continue  # centre outside the lumen
            inside = comp == comp[c, c]
            r[k0 + j] = np.sqrt(inside.sum() * px * px / np.pi)
            edge = inside[0].any() or inside[-1].any() or inside[:, 0].any() or inside[:, -1].any()
            seen = near[j][inside]
            touch[k0 + j] = edge or bool(np.isin(seen[seen > 0], own, invert=True).any())
    return r, touch


def branch_keep(s, junction_s, r, k=2.0, ostium_mm=3.0):
    """True where a sample is clear of every junction (by k median radii) and past the first ostium_mm.

    junction_s are arc positions on the same axis as s; they may lie before 0 (the LM split for
    a trunk whose LM was cut off). k = 2 is about one parent diameter.
    """
    keep = s >= ostium_mm
    reach = k * np.nanmedian(r) if np.isfinite(r).any() else 0.0
    for sj in np.atleast_1d(junction_s):
        keep &= np.abs(s - sj) > reach
    return keep


def taper(s, r, keep, min_mm=20.0, min_frac=0.6):
    """(T, mm_used, frac_used, reason): T = -10 x Theil-Sen slope of ln r on s over the kept samples.

    T is NaN, with a reason, when the kept samples span less than min_mm or are fewer than
    min_frac of all samples.
    """
    keep = keep & np.isfinite(r) & (r > 0)
    n = int(keep.sum())
    span = float(s[keep].max() - s[keep].min()) if n else 0.0
    frac = n / len(s) if len(s) else 0.0
    if span < min_mm:
        return np.nan, span, frac, f"usable span {span:.1f} mm < {min_mm:g} mm"
    if frac < min_frac:
        return np.nan, span, frac, f"usable fraction {frac:.2f} < {min_frac:g}"
    slope = theilslopes(np.log(r[keep]), s[keep])[0]
    return -10.0 * slope, span, frac, None
