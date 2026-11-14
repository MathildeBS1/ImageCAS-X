"""Lumen taper per segment: the taper feature of the who model (sec:method-taper, 05d_taper.tex).

    from taper_feature import tree_taper
    tree_taper(tree, rings_of)  # {(artery, 0/1/2 for p/m/d): fractional loss of diameter per 10 mm, or nan}

    python CGPS_data/thesis_final/taper_feature.py --check   # synthetic shapes, needs no data

Diameter of one cross-section: the area-equivalent diameter D = 2 sqrt(A / pi) of the tracer lumen contour
(daughter_ratio.contour_diameter, eq:method-diameter of sec:method-ratio).

Taper of one segment (segment_taper): tau = -10 b, b the Theil-Sen slope of ln D against arc length s (mm),
fitted over the kept points of the segment. tau is the fractional loss of diameter per 10 mm: 0.05 means the
lumen narrows by about 5 % per 10 mm, 0 a segment that holds its calibre, < 0 one that widens. ln D and ln r
have the same slope. The log makes tau unchanged when the whole artery is scaled, so it describes shape, not
calibre (which differs with sex and dominance). Theil-Sen (the median of the slopes between all pairs of
points) so a few widened or narrowed contours do not move the slope; least squares is printed for comparison
in --check.

Kept points (keep_mask): the lumen steps down at every side-branch origin, and normal taper (about 0.25 mm per
10 mm, Medrano-Gracia et al. 2016) is far smaller than such a step, so the fit must follow the narrowing
between branches. Dropped: points within K median radii (K = 2, about one parent diameter) of any side-branch
origin, and the first START_MM of each artery (the ostium of the RCA; for the LAD and the LCx the other
daughter leaves at s = 0 and is a branch origin there, so the confluence at O is dropped by the same rule).
The branch origins are those of split_trunks.branches on the artery path; segment boundaries sit at branches
(D1, OM, ...), so the rule also trims the segment ends.

Missing: fewer than MIN_MM of arc length between the first and last kept point in the segment (or fewer than
2 kept points). Decided per segment with 10 mm on 2026-11-11 (user); tortuosity/taper.py fitted one value
per artery over >= 20 mm and is kept as the per-artery sensitivity fit, artery_level_taper (20 mm).

Replaces tortuosity/taper.py for the thesis: that code cut ImageCAS-X voxel masks with planes; CGPS has the
tracer lumen contours. Open: the tracer contour format is unknown (daughter_ratio.tracer_rings raises).
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from scipy.stats import theilslopes

sys.path.insert(0, str(Path(__file__).resolve().parent))  # daughter_ratio
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/

from daughter_ratio import contour_diameter  # noqa: E402

K = 2.0  # median radii either side of a side-branch origin
START_MM = 3.0  # mm at the start of each artery
MIN_MM = 10.0  # mm of kept arc length per segment
MIN_MM_ARTERY = 20.0  # mm, the per-artery sensitivity fit (as tortuosity/taper.py)


def keep_mask(s, branch_s, D, k=K, start_mm=START_MM):
    """True where a point is past the first start_mm of the artery and more than k median radii from every
    side-branch origin (arc positions branch_s, same axis as s)."""
    s, D = np.asarray(s, float), np.asarray(D, float)
    keep = (s >= start_mm) & np.isfinite(D) & (D > 0)
    reach = k * np.nanmedian(D) / 2 if np.isfinite(D).any() else 0.0
    for b in np.atleast_1d(np.asarray(branch_s, float)):
        keep &= np.abs(s - b) > reach
    return keep


def fit_taper(s, D, keep, lo=-np.inf, hi=np.inf, min_mm=MIN_MM):
    """tau = -10 x Theil-Sen slope of ln D on s over the kept points with lo <= s < hi; nan when they span
    less than min_mm or are fewer than 2."""
    s, D = np.asarray(s, float), np.asarray(D, float)
    m = keep & (s >= lo) & (s < hi)
    if m.sum() < 2 or s[m].max() - s[m].min() < min_mm:
        return np.nan
    return float(-10.0 * theilslopes(np.log(D[m]), s[m])[0])


def segment_taper(s, D, keep, lo, hi, min_mm=MIN_MM):
    """Taper of the segment [lo, hi) of one artery."""
    return fit_taper(s, D, keep, lo, hi, min_mm)


def artery_taper(s, D, branch_s, bounds):
    """Taper of each segment [lo, hi) of one artery, bounds = (0, pm, md, end) in mm along it."""
    keep = keep_mask(s, branch_s, D)
    return [segment_taper(s, D, keep, lo, hi) for lo, hi in zip(bounds[:-1], bounds[1:])]


def artery_level_taper(s, D, branch_s):
    """One taper over the whole artery (>= 20 mm kept): the sensitivity fit of sec:method-validity-definitions."""
    return fit_taper(s, D, keep_mask(s, branch_s, D), min_mm=MIN_MM_ARTERY)


def _paths(X, Y):
    """Node indices of the points Y (rows of X)."""
    row = {tuple(x): i for i, x in enumerate(np.asarray(X))}
    return [row[tuple(y)] for y in np.asarray(Y)]


def tree_taper(tree, rings_of, artery_level=False):
    """{(artery, part): tau} for the LAD, LCx and RCA segments of one tree, part 0/1/2 = p/m/d. rings_of(Y)
    gives the lumen contour (m, 3) of each centerline point of Y (n, 3), or None where there is none. With
    artery_level=True: {artery: tau} from one fit over the whole artery instead."""
    from split_trunks import branches, graph, split  # imported here so --check runs without the shared modules

    X, lab, G = graph(tree)
    out = {}
    for a, (pm, md, end, _, Y, s) in split(X, lab, G).items():
        br, _ = branches(_paths(X, Y), G, lab)
        D = np.array([contour_diameter(r) if r is not None else np.nan for r in rings_of(Y)])
        bs = [b[0] for b in br]
        if artery_level:
            out[a] = artery_level_taper(s, D, bs)
        else:
            for part, tau in enumerate(artery_taper(s, D, bs, (0, pm, md, end))):
                out[(a, part)] = tau
    return out


# ---------------------------------------------------------------- checks on synthetic shapes (no data)

def _spacing(rng, length, h=0.5):
    s = np.r_[0, np.cumsum(rng.uniform(0.4 * h, 1.6 * h, int(4 * length / h)))]
    return s[s <= length]


def check():
    """Known answers."""
    rng = np.random.default_rng(0)
    c = 0.006  # 1/mm: 6 % per 10 mm, about 0.2 mm per 10 mm on a 3.5 mm artery
    s = _spacing(rng, 80)
    D = 3.5 * np.exp(-c * s)
    keep = keep_mask(s, [], D)
    tau = segment_taper(s, D, keep, 0, 80)
    print(f"exponential tube, c = {c} /mm: tau {tau:.5f} (10 c = {10 * c:.5f})")
    assert abs(tau - 10 * c) < 1e-9, "exponential tube must give tau = 10 c"
    assert abs(segment_taper(s, np.full(len(s), 3.0), keep, 0, 80)) < 1e-12, "straight tube must give 0"
    assert abs(segment_taper(s, 0.6 * D, keep, 0, 80) - tau) < 1e-12, "scaling the artery must not change tau"
    assert segment_taper(s, 3.5 * np.exp(c * s), keep, 0, 80) < 0, "a widening tube must give tau < 0"

    # segments on unevenly spaced points: same tau at every density
    for h in (0.25, 0.5, 1.0):
        u = _spacing(rng, 80, h)
        t = artery_taper(u, 3.5 * np.exp(-c * u), [], (0, 25, 50, 80))
        assert np.allclose(t, 10 * c, atol=1e-9), f"point spacing {h} mm"

    # a step down at each side-branch origin: the exclusion keeps it out of the slope
    br = [20.0, 45.0]
    step = np.where(s > br[0], 0.85, 1.0) * np.where(s > br[1], 0.85, 1.0)
    Ds = D * step
    naive = fit_taper(s, Ds, np.ones(len(s), bool) & (s >= 3), 0, 80)
    seg = artery_taper(s, Ds, br, (0, br[0], br[1], 80))
    print(f"steps of 15 % at {br} mm: whole artery, no exclusion {naive:.4f}; per segment with exclusion "
          + ", ".join(f"{x:.4f}" for x in seg))
    assert np.allclose(seg, 10 * c, atol=1e-9), "the branch steps must not enter the segment slopes"
    assert naive > 1.5 * 10 * c, "without the exclusion the steps inflate the taper"

    # a few widened contours (side-branch origin missed, calcium) do not move Theil-Sen; least squares moves
    Dn = D * np.exp(rng.normal(0, 0.03, len(s)))
    k2 = keep_mask(s, [], Dn)
    lo, hi = 25.0, 45.0
    m = k2 & (s >= lo) & (s < hi)
    base = segment_taper(s, Dn, k2, lo, hi)
    Dw = Dn.copy()
    idx = np.flatnonzero(m)[-4:]
    Dw[idx] *= 1.4
    ts = segment_taper(s, Dw, k2, lo, hi)
    ls = lambda d: -10 * np.polyfit(s[m], np.log(d[m]), 1)[0]  # noqa: E731
    print(f"4 widened contours in a 20 mm segment: Theil-Sen {base:.4f} -> {ts:.4f}, "
          f"least squares {ls(Dn):.4f} -> {ls(Dw):.4f} (true {10 * c:.4f})")
    assert abs(ts - base) < abs(ls(Dw) - ls(Dn)) / 3, "Theil-Sen must move less than least squares"

    # missing rules
    assert np.isnan(segment_taper(s, D, keep, 30, 39)), "less than 10 mm kept must give nan"
    assert np.isfinite(segment_taper(s, D, keep, 30, 41)), "a 11 mm segment is fitted"
    kb = keep_mask(s, [35.0], D)  # branch in the middle: the span is first to last kept point, still 18 mm
    assert abs(segment_taper(s, D, kb, 26, 44) - 10 * c) < 1e-9, "a cut inside the segment keeps its span"
    kb = keep_mask(s, [24.0, 36.0], D)  # branches at both ends of a 12 mm segment: under 10 mm kept
    assert np.isnan(segment_taper(s, D, kb, 24, 36)), "kept span under 10 mm after the branch cuts"
    assert not keep_mask(s, [], D)[s < START_MM].any(), "first 3 mm dropped"
    assert np.isnan(artery_level_taper(s[s < 22], D[s < 22], [])), "per-artery fit needs 20 mm"
    print("all checks passed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="run the synthetic-shape checks")
    if ap.parse_args().check:
        check()
    else:
        ap.print_help()
