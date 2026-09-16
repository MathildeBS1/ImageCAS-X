"""Figure: the curvature noise floor from scripts/tortuosity_noise_floor.py, made visible.

Left panel: the pooled curvature distribution from repeated noisy straight lines at
sigma=1.0mm (500 trials) -- since the true curve is straight, every nonzero value here is
measurement noise, not shape. The 95th percentile is the noise floor. Right panel: the real
RCA's own curvature profile along arc length (case 1, same sigma), with the same floor line;
the shaded fraction is what actually clears it.

    uv run python scripts/make_noise_floor_figure.py images/1

Writes figures/tortuosity_noise_floor_<case>.{pdf,png}.
"""

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

from discover_common import resolve
from tortuosity_noise_floor import _margin, _trim, calibrate
from topology import graph, tortuosity

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
INK = "#1f2933"
MUTED = "#7b8794"
CURVE = "#2a78d6"
FLOOR = "#d83d29"
SIGMA_MM = 1.0


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case", nargs="?", default="images/1", help="case prefix, e.g. images/1")
    args = parser.parse_args()

    prefix = resolve(args.case)
    case = os.path.basename(prefix)
    case_id = int(case)

    floors = calibrate()
    floor = floors[SIGMA_MM]["curvature_floor"]

    rng = np.random.default_rng(0)
    from tortuosity_noise_floor import EPS_MM, GRID_MM, LINE_LENGTH_MM
    n_native = int(round(LINE_LENGTH_MM / GRID_MM))
    axis = np.zeros((n_native, 3))
    axis[:, 0] = np.arange(n_native) * GRID_MM
    noisy = axis + rng.normal(0.0, EPS_MM, axis.shape)
    _arc_n, curvature_n, _torsion_n = tortuosity.curvature_profile(
        noisy, sigma_mm=SIGMA_MM, step_mm=tortuosity.RESAMPLE_MM)
    _, curvature_n = _trim(_arc_n, curvature_n, SIGMA_MM, tortuosity.RESAMPLE_MM)

    trees = graph.load_trees(case_id)
    vessel, reason, _extra = tortuosity._select_vessel(trees["right"], "RCA")
    if vessel is None:
        raise SystemExit(f"no RCA in case {case}: {reason}")
    arc, curvature, _torsion = tortuosity.curvature_profile(
        vessel.points, sigma_mm=SIGMA_MM, step_mm=tortuosity.RESAMPLE_MM)
    arc, curvature = _trim(arc, curvature, SIGMA_MM, tortuosity.RESAMPLE_MM)
    clear_frac = float(np.mean(curvature > floor))

    plt.rcParams.update({"font.size": 9, "font.family": "sans-serif"})
    fig, (ax_hist, ax_profile) = plt.subplots(1, 2, figsize=(9.5, 3.6))

    ax_hist.hist(curvature_n, bins=60, color=MUTED, edgecolor="none")
    ax_hist.axvline(floor, color=FLOOR, lw=1.4, label=f"p95 floor = {floor:.3f} mm$^{{-1}}$")
    ax_hist.set_title(f"500 noisy straight lines, $\\sigma$={SIGMA_MM:g}mm\n"
                      "every nonzero value here is noise", fontsize=9, color=INK)
    ax_hist.set_xlabel("measured curvature (mm$^{-1}$)", fontsize=8)
    ax_hist.set_ylabel("count", fontsize=8)
    ax_hist.legend(fontsize=7, loc="upper right")

    ax_profile.plot(arc, curvature, color=CURVE, lw=1.2)
    ax_profile.axhline(floor, color=FLOOR, lw=1.2, ls="--",
                       label=f"same floor = {floor:.3f} mm$^{{-1}}$")
    ax_profile.fill_between(arc, floor, curvature, where=curvature > floor,
                            color=CURVE, alpha=0.25, interpolate=True)
    ax_profile.set_title(f"RCA, case {case}: {100 * clear_frac:.1f}% of arc length clears it",
                         fontsize=9, color=INK)
    ax_profile.set_xlabel("arc length from ostium end (mm)", fontsize=8)
    ax_profile.set_ylabel("curvature (mm$^{-1}$)", fontsize=8)
    ax_profile.legend(fontsize=7, loc="upper right")

    fig.suptitle("Curvature's noise floor at the codebase's default smoothing scale", fontsize=9.5,
                color=INK)
    fig.tight_layout(rect=[0, 0, 1, 0.93])

    os.makedirs(OUT_DIR, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT_DIR, f"tortuosity_noise_floor_{case}.{ext}"), dpi=300)
    print(f"wrote figures/tortuosity_noise_floor_{case}.{{pdf,png}}")
    print(f"floor={floor:.4f} mm^-1  clear_frac={clear_frac:.4f}")


if __name__ == "__main__":
    main()
