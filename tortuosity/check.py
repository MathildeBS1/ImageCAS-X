"""Checks of T_l on synthetic curves with known answers. Needs no data.

    python -m tortuosity.check
"""
import numpy as np

from .curvature import chord_resample, mean_abs_curvature


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

    # point jitter sigma on a straight line adds about 3 sigma / l^2 of false turning per mm
    rng = np.random.default_rng(0)
    print("jitter on a straight 100 mm line: measured T_l vs predicted 3 sigma / l^2 (rad/mm)")
    for sigma in (0.25, 0.5):
        for l in (2, 5, 8):
            T = np.mean([mean_abs_curvature(line[::2] + rng.normal(0, sigma, (200, 3)), l) for _ in range(20)])
            print(f"  sigma {sigma} mm, l {l} mm: {T:.4f} vs {3 * sigma / l**2:.4f}")
    print("all checks passed")


if __name__ == "__main__":
    main()
