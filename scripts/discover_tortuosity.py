"""Tortuosity of a case's centerlines.

Structure comes from discover_centerline.py; this is the geometry built on top
of it. Every path is oriented proximal-to-distal by a traversal rooted at the
ostium, resampled to uniform arc length, and optionally smoothed before any
derivative is taken.

Metrics, per path:

  distance_metric  arc / chord. 1.0 is a straight line. A ratio of two lengths,
                   so it is the one number here that survives a change of
                   smoothing scale.
  soam_per_mm      summed turning angle per mm of arc -- catches many small
                   bends that leave arc/chord almost unchanged.
  inflections      reversals of the normal vector: how often the curve changes
                   the side it bends towards.
  icm              (inflections + 1) x distance_metric.
  curvature        mean and max |kappa|, 1/mm.
  torsion_mean_abs mean |tau|, the out-of-plane twist.
  non_planarity    3rd PCA eigenvalue fraction; 0 is a curve lying in a plane.

Centerline points sit at roughly the voxel scale, and curvature is a second
derivative, so everything except distance_metric depends on how much the curve
is smoothed first. `--sweep` shows that dependence rather than hiding it.

    uv run python scripts/discover_tortuosity.py images/1
    uv run python scripts/discover_tortuosity.py images/1 --sweep
    uv run python scripts/discover_tortuosity.py images/* --csv > tortuosity.csv
"""

import argparse
import csv
import os
import sys

import numpy as np
from scipy.ndimage import gaussian_filter1d

from discover_common import (case_files, orient_edges, read_centerline,
                             read_polydata, resolve, segment_names,
                             segment_paths, tip_paths)

# Arc-length spacing every path is resampled to before differentiation, so that
# metrics are comparable between vessels sampled at different densities.
RESAMPLE_MM = 0.25
DEFAULT_SIGMA_MM = 1.0
SMOOTHING_SWEEP_MM = (0.0, 0.5, 1.0, 2.0)
PLANARITY_EPS = 1e-6


def resample(path_points, step_mm=RESAMPLE_MM):
    """Uniform arc-length resampling; SOAM and curvature are sampling-dependent."""
    deltas = np.linalg.norm(np.diff(path_points, axis=0), axis=1)
    arc = np.concatenate([[0.0], np.cumsum(deltas)])
    keep = np.concatenate([[True], deltas > 1e-9])
    arc, path_points = arc[keep], path_points[keep]
    if arc[-1] < 2 * step_mm:
        return path_points, float(arc[-1])
    grid = np.arange(0.0, arc[-1], step_mm)
    curve = np.column_stack([np.interp(grid, arc, path_points[:, d]) for d in range(3)])
    return curve, float(arc[-1])


def tortuosity(path_points, sigma_mm=DEFAULT_SIGMA_MM, step_mm=RESAMPLE_MM):
    """The descriptor set above, for one open curve. None if too short to fit."""
    curve, raw_arc = resample(path_points, step_mm)
    if len(curve) < 7:
        return None
    if sigma_mm > 0:
        curve = gaussian_filter1d(curve, sigma_mm / step_mm, axis=0, mode="nearest")

    arc_length = float(np.linalg.norm(np.diff(curve, axis=0), axis=1).sum())
    chord = float(np.linalg.norm(curve[-1] - curve[0]))

    tangents = np.diff(curve, axis=0)
    tangents /= np.maximum(np.linalg.norm(tangents, axis=1, keepdims=True), 1e-12)
    angles = np.arccos(np.clip(np.einsum("ij,ij->i", tangents[:-1], tangents[1:]), -1.0, 1.0))

    d1 = np.gradient(curve, step_mm, axis=0)
    d2 = np.gradient(d1, step_mm, axis=0)
    d3 = np.gradient(d2, step_mm, axis=0)
    cross = np.cross(d1, d2)
    cross_norm = np.linalg.norm(cross, axis=1)
    curvature = cross_norm / np.maximum(np.linalg.norm(d1, axis=1) ** 3, 1e-12)
    torsion = np.einsum("ij,ij->i", cross, d3) / np.maximum(cross_norm ** 2, 1e-12)

    # Normal direction; a sign flip between neighbours is an inflection.
    normal = d2 - (np.einsum("ij,ij->i", d2, d1) /
                   np.maximum(np.einsum("ij,ij->i", d1, d1), 1e-12))[:, None] * d1
    norms = np.linalg.norm(normal, axis=1, keepdims=True)
    usable = norms[:, 0] > PLANARITY_EPS
    normal = normal / np.maximum(norms, 1e-12)
    dots = np.einsum("ij,ij->i", normal[:-1], normal[1:])
    inflections = int(np.sum((dots < 0) & usable[:-1] & usable[1:]))

    eigenvalues = np.linalg.eigvalsh(np.cov((curve - curve.mean(axis=0)).T))[::-1]
    distance_metric = arc_length / chord if chord > 1e-9 else float("nan")
    return {
        "n_points": len(curve),
        "raw_arc_mm": raw_arc,
        "arc_mm": arc_length,
        "chord_mm": chord,
        "distance_metric": distance_metric,
        "soam_per_mm": float(angles.sum() / arc_length) if arc_length > 0 else float("nan"),
        "total_turning_deg": float(np.degrees(angles.sum())),
        "inflections": inflections,
        "icm": (inflections + 1) * distance_metric,
        "curvature_mean": float(np.mean(np.abs(curvature))),
        "curvature_max": float(np.max(np.abs(curvature))),
        "torsion_mean_abs": float(np.mean(np.abs(torsion))),
        "non_planarity": float(eigenvalues[2] / max(eigenvalues.sum(), 1e-12)),
    }


def measured_paths(centerline, oriented, root):
    """(unit, name, points) for every path worth a row."""
    names = segment_names()
    out = []
    for label_id, pieces in segment_paths(centerline, oriented).items():
        longest = max(pieces, key=len)
        out.append(("segment", names.get(label_id, str(label_id)), longest, len(pieces)))
    for i, path in enumerate(tip_paths(centerline, oriented, root)):
        out.append(("tip_path", f"path{i}", path, 1))
    return out


def report(centerline, oriented, root, sigma, side):
    print(f"\n-- {side}: tortuosity at sigma = {sigma} mm")
    print("  A 'segment' row measures the longest contiguous run of that label; where")
    print("  'runs' is above 1 the label is split by the traversal and only partly")
    print("  described. The tip_path rows run ostium-to-tip and have no such gap.")
    print(f"  {'unit':<9} {'name':<8} {'runs':>4} {'arc':>7} {'chord':>7} {'L/D':>6} "
          f"{'SOAM':>7} {'infl':>5} {'ICM':>6} {'kap_max':>8} {'nonplan':>8}")
    for unit, name, points, runs in measured_paths(centerline, oriented, root):
        result = tortuosity(points, sigma_mm=sigma)
        if result is None:
            print(f"  {unit:<9} {name:<8} {runs:>4}   too short to differentiate")
            continue
        print(f"  {unit:<9} {name:<8} {runs:>4} {result['arc_mm']:>7.1f} "
              f"{result['chord_mm']:>7.1f} {result['distance_metric']:>6.3f} "
              f"{result['soam_per_mm']:>7.4f} {result['inflections']:>5} "
              f"{result['icm']:>6.2f} {result['curvature_max']:>8.3f} "
              f"{result['non_planarity']:>8.4f}")


def report_sweep(centerline, oriented, root, side):
    paths = segment_paths(centerline, oriented)
    if not paths:
        return
    label_id = max(paths, key=lambda k: max(len(p) for p in paths[k]))
    longest = max(paths[label_id], key=len)
    print(f"\n-- {side}: smoothing sensitivity, longest segment "
          f"({segment_names().get(label_id, label_id)})")
    print(f"  {'sigma':>6} {'L/D':>7} {'SOAM':>8} {'infl':>5} {'kap_mean':>9} {'kap_max':>9}")
    for sigma in SMOOTHING_SWEEP_MM:
        result = tortuosity(longest, sigma_mm=sigma)
        if result:
            print(f"  {sigma:>6.1f} {result['distance_metric']:>7.3f} "
                  f"{result['soam_per_mm']:>8.4f} {result['inflections']:>5} "
                  f"{result['curvature_mean']:>9.3f} {result['curvature_max']:>9.3f}")
    print("  L/D is a ratio of lengths and barely moves. SOAM, the inflection count and")
    print("  curvature are derivative-based and do. Fix one sigma and justify it, or")
    print("  report the sweep -- an unqualified curvature here is not reproducible.")


def report_radius(centerlines, surface_path):
    """Lumen radius: the distance from the centerline to the surface.

    Neither file holds this on its own, and it is the scale tortuosity needs --
    a bend of a given curvature means something different in a 3 mm trunk than
    in a 1 mm distal branch.
    """
    import vtk

    distance = vtk.vtkImplicitPolyDataDistance()
    distance.SetInput(read_polydata(surface_path))
    names = segment_names()
    by_label = {}
    for centerline in centerlines:
        for point, label in zip(centerline["points"], centerline["label"]):
            by_label.setdefault(int(label), []).append(
                abs(distance.EvaluateFunction([float(v) for v in point])))

    print("\n-- lumen radius, from the centerline and the surface together")
    print(f"  {'seg':<8} {'points':>7} {'median':>8} {'p5':>7} {'p95':>7}  (mm)")
    for label_id in sorted(by_label):
        radii = np.array(by_label[label_id])
        print(f"  {names.get(label_id, label_id):<8} {len(radii):>7} "
              f"{np.median(radii):>8.3f} {np.percentile(radii, 5):>7.3f} "
              f"{np.percentile(radii, 95):>7.3f}")
    print("  Signed distance to the nearest surface point, so it is the inscribed")
    print("  radius: it under-reads where the centerline sits off-axis or a branch")
    print("  passes close by.")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case", nargs="+", help="case prefix, e.g. images/1")
    parser.add_argument("--side", choices=("left", "right", "both"), default="both")
    parser.add_argument("--sigma", type=float, default=DEFAULT_SIGMA_MM,
                        help=f"smoothing in mm along the curve (default {DEFAULT_SIGMA_MM})")
    parser.add_argument("--sweep", action="store_true",
                        help="show how the metrics move with the smoothing scale")
    parser.add_argument("--no-radius", action="store_true",
                        help="skip the radius table (it needs the surface mesh)")
    parser.add_argument("--csv", action="store_true",
                        help="write one row per measured path to stdout instead")
    args = parser.parse_args()

    sides = ("left", "right") if args.side == "both" else (args.side,)
    rows = []
    for raw in args.case:
        prefix = resolve(raw)
        files = case_files(prefix)
        case = os.path.basename(prefix)
        loaded = []
        if not args.csv:
            print(f"\n{'#' * 68}\n# case {case}\n{'#' * 68}")
        for side in sides:
            if not os.path.exists(files[side]):
                continue
            centerline = read_centerline(files[side])
            oriented, root = orient_edges(centerline)
            if oriented is None:
                continue
            loaded.append(centerline)
            if args.csv:
                for unit, name, points, runs in measured_paths(centerline, oriented, root):
                    result = tortuosity(points, sigma_mm=args.sigma)
                    if result:
                        rows.append(dict(case=case, side=side, unit=unit, name=name,
                                         runs=runs, sigma_mm=args.sigma, **result))
            else:
                report(centerline, oriented, root, args.sigma, side)
                if args.sweep:
                    report_sweep(centerline, oriented, root, side)
        if not args.csv and loaded and not args.no_radius \
                and os.path.exists(files["surface"]):
            report_radius(loaded, files["surface"])

    if args.csv and rows:
        writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
