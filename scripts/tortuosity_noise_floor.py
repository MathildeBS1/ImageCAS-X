#!/usr/bin/env python
"""Settles the open question in tortuosity_and_representation.tex Sec.\ 6: at the smoothing scale
this codebase actually uses, how much of a real vessel's curvature (and torsion) is distinguishable
from what pure position jitter would produce on a perfectly straight line?

Calibration: a synthetic straight line at ImageCAS-X's own fixed 0.5mm through-plane (z) voxel
spacing (verified from the NIfTI headers, not assumed; see position_noise_lower_bound.tex), with
independent per-coordinate Gaussian position noise (eps = h/sqrt(12), the quantisation-noise floor
derived there), is put through the exact same resample-then-
smooth-then-differentiate pipeline as topology.tortuosity.measure (topology/tortuosity.py's
curvature_profile). Since the line is straight, every nonzero value the pipeline reports there is
noise; the 95th percentile of that pooled, repeated-trial distribution is the noise floor at that
sigma. A real vessel's own curvature (torsion) profile then "clears its own noise floor" wherever it
exceeds that same-sigma threshold; the fraction of arc length where it does is what actually
licenses a reported curvature value as signal rather than measurement noise.

Usage:
  python scripts/tortuosity_noise_floor.py                 # calibrate + case 1, all sigmas
  python scripts/tortuosity_noise_floor.py --n 50           # + cohort check, first 50 usable cases
  python scripts/tortuosity_noise_floor.py --case 1 --figure
"""

from __future__ import annotations

import argparse
import json

import numpy as np

from topology import graph, paths, tortuosity

GRID_MM = 0.5  # ImageCAS-X's own fixed z-spacing (verified from NIfTI headers, every scan
                # checked), giving eps = h/sqrt(12) as a lower bound, not an assumption
                # (position_noise_lower_bound.tex)
EPS_MM = GRID_MM / np.sqrt(12)
SIGMAS = (0.0, 0.5, 1.0, 2.0)
FLOOR_PERCENTILE = 95.0
N_TRIALS = 500
LINE_LENGTH_MM = 150.0
#: Boundary points where np.gradient falls back to one-sided differencing are excluded from both
#: the calibration pool and the real-vessel fraction, at a margin that scales with the smoothing.
EDGE_MARGIN_STEPS = 5


def _margin(sigma_mm: float, step_mm: float) -> int:
    return max(EDGE_MARGIN_STEPS, int(round(2 * sigma_mm / step_mm)))


def _trim(arc: np.ndarray, values: np.ndarray, sigma_mm: float, step_mm: float) -> tuple[np.ndarray, np.ndarray]:
    m = _margin(sigma_mm, step_mm)
    if len(values) <= 2 * m:
        return arc, values
    return arc[m:-m], values[m:-m]


def calibrate(step_mm: float = tortuosity.RESAMPLE_MM, rng: np.random.Generator | None = None) -> dict:
    """Pooled curvature/torsion noise distribution per sigma, from repeated noisy straight lines."""
    rng = rng or np.random.default_rng(42)
    n_native = int(round(LINE_LENGTH_MM / GRID_MM))
    axis = np.zeros((n_native, 3))
    axis[:, 0] = np.arange(n_native) * GRID_MM

    pooled = {sigma: {"curvature": [], "torsion": []} for sigma in SIGMAS}
    for _ in range(N_TRIALS):
        noisy = axis + rng.normal(0.0, EPS_MM, axis.shape)
        for sigma in SIGMAS:
            result = tortuosity.curvature_profile(noisy, sigma_mm=sigma, step_mm=step_mm)
            if isinstance(result, str):
                continue
            arc, curvature, torsion = result
            _, curvature = _trim(arc, curvature, sigma, step_mm)
            _, torsion = _trim(arc, torsion, sigma, step_mm)
            pooled[sigma]["curvature"].append(curvature)
            pooled[sigma]["torsion"].append(np.abs(torsion))

    floors = {}
    for sigma in SIGMAS:
        curvature_all = np.concatenate(pooled[sigma]["curvature"])
        torsion_all = np.concatenate(pooled[sigma]["torsion"])
        floors[sigma] = {
            "curvature_floor": float(np.percentile(curvature_all, FLOOR_PERCENTILE)),
            "torsion_floor": float(np.percentile(torsion_all, FLOOR_PERCENTILE)),
            "curvature_median": float(np.median(curvature_all)),
            "torsion_median": float(np.median(torsion_all)),
        }
    return floors


def vessel_clearance(points: np.ndarray, floors: dict, step_mm: float = tortuosity.RESAMPLE_MM) -> dict:
    """Per sigma, the fraction of this vessel's arc length whose curvature (torsion) exceeds the
    noise floor calibrated at that same sigma."""
    out = {}
    for sigma in SIGMAS:
        result = tortuosity.curvature_profile(points, sigma_mm=sigma, step_mm=step_mm)
        if isinstance(result, str):
            out[sigma] = {"reason": result}
            continue
        arc, curvature, torsion = result
        arc_t, curvature = _trim(arc, curvature, sigma, step_mm)
        _, torsion = _trim(arc, torsion, sigma, step_mm)
        floor = floors[sigma]
        out[sigma] = {
            "curvature_clear_frac": float(np.mean(curvature > floor["curvature_floor"])),
            "torsion_clear_frac": float(np.mean(np.abs(torsion) > floor["torsion_floor"])),
            "n_points": int(len(curvature)),
            "arc_length_mm": float(arc_t[-1] - arc_t[0]) if len(arc_t) else 0.0,
        }
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--case", type=int, default=1, help="case id used for the headline numbers")
    ap.add_argument("--n", type=int, default=0, help="also check the first N usable cases (0 = skip cohort check)")
    args = ap.parse_args()

    print(f"Calibrating noise floor: {N_TRIALS} straight lines, {LINE_LENGTH_MM:g}mm, "
          f"grid={GRID_MM:g}mm, eps={EPS_MM:.4f}mm, floor=p{FLOOR_PERCENTILE:g}")
    floors = calibrate()
    for sigma in SIGMAS:
        f = floors[sigma]
        print(f"  sigma={sigma:g}mm  curvature_floor={f['curvature_floor']:.4f} mm^-1  "
              f"torsion_floor={f['torsion_floor']:.4f} mm^-1")

    trees = graph.load_trees(args.case)
    print(f"\nCase {args.case}, fraction of arc length clearing its own noise floor:")
    case_rows = {}
    for name, side in tortuosity.VESSEL_SIDES.items():
        vessel, reason, _extra = tortuosity._select_vessel(trees[side], name)
        if vessel is None:
            print(f"  {name}: {reason}")
            continue
        clearance = vessel_clearance(vessel.points, floors)
        case_rows[name] = clearance
        for sigma in SIGMAS:
            c = clearance[sigma]
            if "reason" in c:
                print(f"  {name}  sigma={sigma:g}: {c['reason']}")
                continue
            print(f"  {name}  sigma={sigma:g}mm  curvature clears floor for "
                  f"{100 * c['curvature_clear_frac']:.1f}% of arc length, "
                  f"torsion for {100 * c['torsion_clear_frac']:.1f}%  (n={c['n_points']})")

    out = paths.output_dir("tortuosity/noise_floor")
    payload = {"code_version": paths.code_version(), "grid_mm": GRID_MM, "eps_mm": EPS_MM,
              "n_trials": N_TRIALS, "floor_percentile": FLOOR_PERCENTILE, "sigmas": SIGMAS,
              "floors": {str(s): v for s, v in floors.items()},
              "case": args.case, "case_vessels": {name: {str(s): v for s, v in c.items()}
                                                  for name, c in case_rows.items()}}

    if args.n:
        print(f"\nCohort check, first {args.n} usable cases, sigma={tortuosity.DEFAULT_SIGMA_MM:g}mm:")
        cohort = {name: {"curvature": [], "torsion": []} for name in tortuosity.VESSEL_SIDES}
        for cid in paths.usable_ids()[: args.n]:
            try:
                trees = graph.load_trees(cid)
            except Exception:
                continue
            for name, side in tortuosity.VESSEL_SIDES.items():
                vessel, reason, _extra = tortuosity._select_vessel(trees[side], name)
                if vessel is None:
                    continue
                c = vessel_clearance(vessel.points, floors)[tortuosity.DEFAULT_SIGMA_MM]
                if "reason" not in c:
                    cohort[name]["curvature"].append(c["curvature_clear_frac"])
                    cohort[name]["torsion"].append(c["torsion_clear_frac"])
        cohort_summary = {}
        for name, values in cohort.items():
            if not values["curvature"]:
                continue
            arr = np.array(values["curvature"])
            tarr = np.array(values["torsion"])
            print(f"  {name}: curvature median {100 * np.median(arr):.1f}%  "
                  f"IQR [{100 * np.percentile(arr, 25):.1f}, {100 * np.percentile(arr, 75):.1f}]%  "
                  f"| torsion median {100 * np.median(tarr):.1f}%  (n={len(arr)})")
            cohort_summary[name] = {"curvature_median": float(np.median(arr)), "n": len(arr),
                                    "curvature_p25": float(np.percentile(arr, 25)),
                                    "curvature_p75": float(np.percentile(arr, 75)),
                                    "torsion_median": float(np.median(tarr))}
        payload["cohort_n"] = args.n
        payload["cohort_curvature_clear_frac"] = cohort_summary

    (out / "tortuosity_noise_floor.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(f"\nWrote {out / 'tortuosity_noise_floor.json'}")


if __name__ == "__main__":
    main()
