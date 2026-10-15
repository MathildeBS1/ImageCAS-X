"""Checks of T_l on synthetic curves with known answers. Needs no data.

    python -m tortuosity.check
"""
import numpy as np

from .curvature import chord_resample, mean_abs_curvature, profile
from .taper import branch_keep, cross_section_radius, resample_arc, tangents, taper


def voxel_tube(r_of_s, length, rot, spacing=(0.45, 0.45, 0.6), branch_at=None):
    """A multi-label mask of a straight tube (label 2) of radius r_of_s(s), on a rotated, anisotropic grid.

    Returns (labels, affine, P): P is the tube axis in LPS, the frame the centerlines use. With
    branch_at, a 1.5 mm side branch (label 4) leaves the tube at that arc position, at right angles.
    """
    d, e = rot[:, 0], rot[:, 1]  # tube direction and branch direction, LPS
    p0 = np.array([3.0, -2.0, 5.0])
    P = p0 + np.outer(np.linspace(0, length, 400), d)
    A = rot @ np.diag(spacing)  # voxel -> LPS linear part
    corners = np.array([p0 - 8, p0 + length * d + 8, p0 + length * d - 8, p0 + 8])
    lo = np.floor(np.linalg.solve(A, (corners - p0).T).min(1)) - 25
    hi = np.ceil(np.linalg.solve(A, (corners - p0).T).max(1)) + 25
    lps_of = lambda ijk: p0 + (ijk + lo) @ A.T
    shape = (hi - lo).astype(int)
    ijk = np.stack(np.meshgrid(*map(np.arange, shape), indexing="ij"), -1).reshape(-1, 3)
    X = lps_of(ijk)
    s = (X - p0) @ d
    rho = np.linalg.norm(X - p0 - np.outer(s, d), axis=1)
    lab = np.where((s >= 0) & (s <= length) & (rho <= r_of_s(np.clip(s, 0, length))), 2, 0)
    if branch_at is not None:
        q0 = p0 + branch_at * d
        sb = (X - q0) @ e
        rb = np.linalg.norm(X - q0 - np.outer(sb, e), axis=1)
        lab = np.where((lab == 0) & (sb >= 0) & (sb <= 15) & (rb <= 1.5), 4, lab)
    flip = np.diag([-1.0, -1.0, 1.0])
    affine = np.eye(4)
    affine[:3, :3] = flip @ A  # voxel -> RAS
    affine[:3, 3] = flip @ (p0 + lo @ A.T)
    return lab.reshape(shape).astype(np.uint8), affine, P


def tube_taper(r_of_s, rot, branch_at=None, masked=True):
    labels, affine, P = voxel_tube(r_of_s, 60.0, rot, branch_at=branch_at)
    Q, s = resample_arc(P)
    r, touch = cross_section_radius(Q, tangents(Q), labels, affine, {2})
    keep = branch_keep(s, [] if branch_at is None else [branch_at], r) & ~touch if masked else np.ones(len(s), bool)
    return taper(s, r, keep)[0], s, r, touch


def check_taper():
    rng = np.random.default_rng(1)
    rots = [np.linalg.qr(rng.normal(size=(3, 3)))[0] for _ in range(2)]

    T, s, r, _ = tube_taper(lambda s: 2.0 + 0 * s, rots[0])
    inner = (s > 5) & (s < 55)
    print(f"taper: cylinder r 2.0 mm -> median r {np.nanmedian(r[inner]):.3f} mm, T {T:.4f}")
    assert abs(T) < 0.01, "a cylinder must not taper"
    assert np.all(np.abs(r[inner] - 2.0) < 0.225), "cross-section radius must be within half a voxel"

    b = 0.006  # per mm, so T = 0.06
    for rot in rots:  # two rigid motions of the same tube
        T = tube_taper(lambda s: 2.5 * np.exp(-b * s), rot)[0]
        print(f"taper: exponential taper, true T {10 * b:.3f} -> {T:.4f}")
        assert abs(T - 10 * b) < 0.01, "exponential taper must give T = 10 b, whatever the pose"

    T_m, s, _, touch = tube_taper(lambda s: 2.5 * np.exp(-b * s), rots[0], branch_at=30.0)
    T_u = tube_taper(lambda s: 2.5 * np.exp(-b * s), rots[0], branch_at=30.0, masked=False)[0]
    print(f"taper: with a side branch at 30 mm, masked {T_m:.4f}, unmasked {T_u:.4f}")
    assert touch[np.abs(s - 30) < 1].any(), "sections through the branch origin must be flagged"
    assert abs(T_m - 10 * b) < 0.01, "branch masking must recover the trunk's taper"


def circle(R, n=4000):
    t = np.linspace(0, 1.5 * np.pi, n)
    return np.c_[R * np.cos(t), R * np.sin(t), 0 * t]


def main():
    line = np.c_[np.linspace(0, 100, 400), np.zeros(400), np.zeros(400)]
    assert mean_abs_curvature(line, 5) < 1e-12, "a straight line must score 0"

    V = chord_resample(circle(20), 5)
    steps = np.linalg.norm(np.diff(V, axis=0), axis=1)
    assert np.allclose(steps, 5), "every chord must be exactly l"

    # on a circle of radius R every chord l turns by 2 asin(l / 2R), so T_l = 2 asin(l / 2R) / l -> 1/R
    for R, l in ((10, 2), (20, 5), (40, 8)):
        expected = 2 * np.arcsin(l / (2 * R)) / l
        assert np.isclose(mean_abs_curvature(circle(R), l), expected, rtol=1e-6), (R, l)

    # rigid motion must not change the score
    s = np.linspace(0, 100, 400)
    P = np.c_[s, 4 * np.sin(2 * np.pi * s / 25), np.cos(s / 7)]
    Q, _ = np.linalg.qr(np.random.default_rng(0).normal(size=(3, 3)))
    assert np.isclose(mean_abs_curvature(P, 5), mean_abs_curvature(P @ Q.T + 5.0, 5))

    # the per-point profile is the same measurement as T_l, only not yet collapsed to its mean
    assert np.isclose(profile(P, 5).mean(), mean_abs_curvature(P, 5)), "profile mean must give T_l"

    # point jitter sigma on a straight line adds about 3 sigma / l^2 of false turning per mm
    rng = np.random.default_rng(0)
    print("jitter on a straight 100 mm line: measured T_l vs predicted 3 sigma / l^2 (rad/mm)")
    for sigma in (0.25, 0.5):
        for l in (2, 5, 8):
            T = np.mean([mean_abs_curvature(line[::2] + rng.normal(0, sigma, (200, 3)), l) for _ in range(20)])
            print(f"  sigma {sigma} mm, l {l} mm: {T:.4f} vs {3 * sigma / l**2:.4f}")
    check_taper()
    print("all checks passed")


if __name__ == "__main__":
    main()
