"""Per-vessel tortuosity panel, computed on a smoothed, arc-length-resampled centerline
(objective 7).

Every classical measure here needs a derivative of the vessel's coordinates: the distance metric
needs none, SOAM and the inflection count need one, curvature needs two, torsion needs three. Each
extra derivative amplifies whatever position noise sits in the centerline, so the panel also
carries a second family that needs at most one derivative: ``plane_d_*`` is the signed distance of
each point to the vessel's own best-fit plane (zero derivatives -- a projection of raw position),
and ``plane_angle_*`` is that distance's rate of change, the unit tangent's component along the
plane normal (one derivative, the tangent). Both stay close to a straight readout of the actual
geometry at any smoothing scale; curvature and torsion do not. Report both families and let the
sensitivity study (``scripts/tortuosity_sensitivity.py``) decide which one a downstream claim can
actually lean on.

A vessel is ``topology.graph.Vessel.points``: same-named segments already chained proximal to
distal with shared junction points counted once, for LM, LAD, LCX and RCA. A vessel that cannot be
found, or is too short to differentiate, comes back as an all-NaN row with a ``reason``, never
silently dropped -- ``extract_trees`` always returns exactly one row per name.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.ndimage import gaussian_filter1d

from . import graph

RESAMPLE_MM = 0.25
DEFAULT_SIGMA_MM = 1.0
DEFAULT_WINDOW_MM = 20.0
MIN_RESAMPLED_POINTS = 7

#: Torsion is undefined where the bending plane is undefined (kappa ~ 0); points below this
#: fraction of the vessel's own peak curvature are excluded from ``torsion_mean_abs`` rather than
#: left to blow it up with noise (``extra`` records how many were dropped).
TORSION_KAPPA_FRACTION = 0.1

#: Below this ratio of the 2nd to the 1st PCA eigenvalue, the vessel is close enough to a straight
#: line that its own best-fit plane (hence its normal, hence every plane_* field) is not
#: meaningfully defined; those fields are left NaN and ``extra["plane_degenerate"]`` is set.
PLANE_MIN_EIG_RATIO = 0.01

#: Clinical-style bend threshold (Groves, Nannini): a bend is a run between two inflections whose
#: summed turning exceeds this angle.
BEND_ANGLE_DEG = 45.0

#: Which side each named vessel's main run lives on.
VESSEL_SIDES = {"LM": "left", "LAD": "left", "LCX": "left", "RCA": "right"}


@dataclass
class VesselTortuosity:
    """One named vessel's tortuosity panel for one case, or the reason it could not be measured."""

    side: str | None
    name: str
    vessel: int | None = None
    n_segments: int = 0
    sigma_mm: float = float("nan")
    step_mm: float = float("nan")
    window_mm: float = float("nan")

    length_mm: float = float("nan")
    chord_mm: float = float("nan")
    n_points: int = 0
    distance_metric: float = float("nan")  # L/D, the classical tortuosity index
    soam_per_mm: float = float("nan")
    total_turning_deg: float = float("nan")
    inflections: int = 0
    icm: float = float("nan")  # (inflections + 1) * distance_metric
    curvature_mean: float = float("nan")
    curvature_max: float = float("nan")
    curvature_rms: float = float("nan")
    torsion_mean_abs: float = float("nan")  # masked where curvature is near zero, see extra
    non_planarity: float = float("nan")  # 3rd PCA eigenvalue's share of the vessel's own spread
    bends_over_45: int = 0  # clinical-style bend count, cross-walkable to Groves/Nannini

    plane_d_max_mm: float = float("nan")
    plane_d_rms_mm: float = float("nan")
    plane_d_rms_norm: float = float("nan")  # rms(d) / length_mm
    plane_d_max_pos: float = float("nan")  # normalised arc position, 0 = proximal, 1 = distal
    plane_angle_mean_deg: float = float("nan")
    plane_angle_max_deg: float = float("nan")

    soam_window_max_per_mm: float = float("nan")
    soam_window_max_pos: float = float("nan")
    curvature_rms_window_max: float = float("nan")
    curvature_rms_window_max_pos: float = float("nan")

    reason: str | None = None
    extra: dict = field(default_factory=dict)


def _missing(name: str, side: str | None, reason: str, **extra) -> VesselTortuosity:
    return VesselTortuosity(side=side, name=name, reason=reason, extra=extra)


def _resample(points: np.ndarray, step_mm: float) -> np.ndarray:
    """Arc-length resampling to a uniform grid, so every derivative-based measure is comparable
    between vessels sampled at different point densities."""
    deltas = np.linalg.norm(np.diff(points, axis=0), axis=1)
    arc = np.concatenate([[0.0], np.cumsum(deltas)])
    keep = np.concatenate([[True], deltas > 1e-9])
    arc, points = arc[keep], points[keep]
    if arc[-1] < 2 * step_mm:
        return points
    grid = np.arange(0.0, arc[-1], step_mm)
    return np.column_stack([np.interp(grid, arc, points[:, d]) for d in range(3)])


def _sliding_mean(values: np.ndarray, window_n: int) -> np.ndarray:
    csum = np.concatenate([[0.0], np.cumsum(values)])
    return (csum[window_n:] - csum[:-window_n]) / window_n


def curvature_profile(points: np.ndarray, sigma_mm: float = DEFAULT_SIGMA_MM,
                      step_mm: float = RESAMPLE_MM) -> tuple[np.ndarray, np.ndarray, np.ndarray] | str:
    """Arc length, pointwise curvature and pointwise torsion after the same resample-then-smooth
    pipeline ``measure`` uses, exposed on its own for noise-floor studies
    (``scripts/tortuosity_noise_floor.py``) that need the profile rather than its summary stats.
    """
    curve = _resample(points, step_mm)
    if len(curve) < MIN_RESAMPLED_POINTS:
        return f"fewer than {MIN_RESAMPLED_POINTS} points after resampling to {step_mm:g}mm"
    if sigma_mm > 0:
        curve = gaussian_filter1d(curve, sigma_mm / step_mm, axis=0, mode="nearest")
    arc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(curve, axis=0), axis=1))])
    d1 = np.gradient(curve, step_mm, axis=0)
    d2 = np.gradient(d1, step_mm, axis=0)
    d3 = np.gradient(d2, step_mm, axis=0)
    cross = np.cross(d1, d2)
    cross_norm = np.linalg.norm(cross, axis=1)
    curvature = cross_norm / np.maximum(np.linalg.norm(d1, axis=1) ** 3, 1e-12)
    torsion = np.einsum("ij,ij->i", cross, d3) / np.maximum(cross_norm ** 2, 1e-12)
    return arc, curvature, torsion


def measure(points: np.ndarray, sigma_mm: float = DEFAULT_SIGMA_MM, step_mm: float = RESAMPLE_MM,
           window_mm: float = DEFAULT_WINDOW_MM) -> dict | str:
    """The tortuosity panel for one vessel's points, proximal to distal, or a reason string if it
    is too short to differentiate. Pure geometry: takes an ``(n, 3)`` array, not a ``Vessel``, so
    the sensitivity study can call it repeatedly on the same points under different settings.

    The returned dict's keys match ``VesselTortuosity``'s numeric fields, plus an ``"extra"`` key
    the caller merges into the row's own ``extra``.
    """
    curve = _resample(points, step_mm)
    if len(curve) < MIN_RESAMPLED_POINTS:
        return f"fewer than {MIN_RESAMPLED_POINTS} points after resampling to {step_mm:g}mm"
    if sigma_mm > 0:
        curve = gaussian_filter1d(curve, sigma_mm / step_mm, axis=0, mode="nearest")
    n = len(curve)
    extra: dict = {}

    arc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(curve, axis=0), axis=1))])
    arc_length = float(arc[-1])
    chord = float(np.linalg.norm(curve[-1] - curve[0]))
    distance_metric = arc_length / chord if chord > 1e-9 else float("nan")

    tangents = np.diff(curve, axis=0)
    tangents /= np.maximum(np.linalg.norm(tangents, axis=1, keepdims=True), 1e-12)
    step_angles = np.arccos(np.clip(np.einsum("ij,ij->i", tangents[:-1], tangents[1:]), -1.0, 1.0))
    soam_per_mm = float(step_angles.sum() / arc_length) if arc_length > 0 else float("nan")
    total_turning_deg = float(np.degrees(step_angles.sum()))

    d1 = np.gradient(curve, step_mm, axis=0)
    d2 = np.gradient(d1, step_mm, axis=0)
    d3 = np.gradient(d2, step_mm, axis=0)
    cross = np.cross(d1, d2)
    cross_norm = np.linalg.norm(cross, axis=1)
    curvature = cross_norm / np.maximum(np.linalg.norm(d1, axis=1) ** 3, 1e-12)
    curvature_mean = float(np.mean(np.abs(curvature)))
    curvature_max = float(np.max(np.abs(curvature)))
    curvature_rms = float(np.sqrt(np.mean(curvature ** 2)))

    torsion = np.einsum("ij,ij->i", cross, d3) / np.maximum(cross_norm ** 2, 1e-12)
    kappa_thresh = TORSION_KAPPA_FRACTION * curvature_max
    torsion_mask = curvature >= kappa_thresh
    torsion_mean_abs = float(np.mean(np.abs(torsion[torsion_mask]))) if torsion_mask.any() else float("nan")
    extra["torsion_n_masked"] = int((~torsion_mask).sum())
    extra["torsion_n_total"] = int(n)

    # Inflections: the osculating-plane normal flips side. Reused below to segment the vessel
    # into individual bends for the clinical-style bend count.
    normal_vec = d2 - (np.einsum("ij,ij->i", d2, d1) /
                       np.maximum(np.einsum("ij,ij->i", d1, d1), 1e-12))[:, None] * d1
    norms = np.linalg.norm(normal_vec, axis=1, keepdims=True)
    usable = norms[:, 0] > 1e-6
    normal_vec = normal_vec / np.maximum(norms, 1e-12)
    dots = np.einsum("ij,ij->i", normal_vec[:-1], normal_vec[1:])
    infl_mask = (dots < 0) & usable[:-1] & usable[1:]
    inflections = int(np.sum(infl_mask))
    icm = (inflections + 1) * distance_metric

    infl_idx = np.flatnonzero(infl_mask)
    infl_idx = infl_idx[infl_idx < len(step_angles)]
    boundaries = np.clip(np.concatenate([[0], infl_idx + 1, [len(step_angles)]]), 0, len(step_angles))
    bend_degrees = [float(np.degrees(step_angles[boundaries[i]:boundaries[i + 1]].sum()))
                    for i in range(len(boundaries) - 1) if boundaries[i + 1] > boundaries[i]]
    bends_over_45 = int(sum(1 for b in bend_degrees if b > BEND_ANGLE_DEG))

    centered = curve - curve.mean(axis=0)
    _u, s, vt = np.linalg.svd(centered, full_matrices=False)
    eig = s ** 2
    non_planarity = float(eig[2] / eig.sum()) if eig.sum() > 0 else float("nan")
    plane_ratio = float(eig[1] / eig[0]) if eig[0] > 0 else 0.0
    extra["plane_eig_ratio"] = round(plane_ratio, 5)
    plane_fields = dict(plane_d_max_mm=float("nan"), plane_d_rms_mm=float("nan"),
                        plane_d_rms_norm=float("nan"), plane_d_max_pos=float("nan"),
                        plane_angle_mean_deg=float("nan"), plane_angle_max_deg=float("nan"))
    if plane_ratio < PLANE_MIN_EIG_RATIO:
        extra["plane_degenerate"] = True
    else:
        normal = vt[2]
        d_signed = centered @ normal
        tangent_unit = d1 / np.maximum(np.linalg.norm(d1, axis=1, keepdims=True), 1e-12)
        angle_deg = np.degrees(np.arcsin(np.clip(tangent_unit @ normal, -1.0, 1.0)))
        rms_d = float(np.sqrt(np.mean(d_signed ** 2)))
        plane_fields = dict(
            plane_d_max_mm=float(np.max(np.abs(d_signed))),
            plane_d_rms_mm=rms_d,
            plane_d_rms_norm=rms_d / arc_length if arc_length > 0 else float("nan"),
            plane_d_max_pos=float(arc[int(np.argmax(np.abs(d_signed)))] / arc_length) if arc_length > 0 else float("nan"),
            plane_angle_mean_deg=float(np.mean(np.abs(angle_deg))),
            plane_angle_max_deg=float(np.max(np.abs(angle_deg))),
        )

    window_n = max(int(round(window_mm / step_mm)), 1)
    if len(step_angles) >= window_n:
        soam_window = _sliding_mean(step_angles, window_n) / step_mm
        idx = int(np.argmax(soam_window))
        soam_window_max_per_mm = float(soam_window[idx])
        soam_window_max_pos = float(arc[min(idx + window_n // 2, n - 1)] / arc_length) if arc_length > 0 else float("nan")
    else:
        soam_window_max_per_mm, soam_window_max_pos = soam_per_mm, float("nan")
        extra["soam_window_clipped"] = True
    if n >= window_n:
        curv_rms_window = np.sqrt(_sliding_mean(curvature ** 2, window_n))
        idx = int(np.argmax(curv_rms_window))
        curvature_rms_window_max = float(curv_rms_window[idx])
        curvature_rms_window_max_pos = float(arc[min(idx + window_n // 2, n - 1)] / arc_length) if arc_length > 0 else float("nan")
    else:
        curvature_rms_window_max, curvature_rms_window_max_pos = curvature_rms, float("nan")
        extra["curvature_window_clipped"] = True

    return {
        "length_mm": arc_length, "chord_mm": chord, "n_points": n,
        "distance_metric": distance_metric, "soam_per_mm": soam_per_mm,
        "total_turning_deg": total_turning_deg, "inflections": inflections, "icm": icm,
        "curvature_mean": curvature_mean, "curvature_max": curvature_max, "curvature_rms": curvature_rms,
        "torsion_mean_abs": torsion_mean_abs, "non_planarity": non_planarity,
        "bends_over_45": bends_over_45,
        "soam_window_max_per_mm": soam_window_max_per_mm, "soam_window_max_pos": soam_window_max_pos,
        "curvature_rms_window_max": curvature_rms_window_max,
        "curvature_rms_window_max_pos": curvature_rms_window_max_pos,
        **plane_fields,
        "extra": extra,
    }


def _select_vessel(tree: graph.CoronaryTree, name: str) -> tuple[graph.Vessel | None, str | None, dict]:
    """The main vessel of ``name`` in ``tree``, or the reason there isn't a usable one."""
    candidates = tree.main_vessels(name)
    if not candidates:
        return None, f"no {name} in the tree", {}
    if len(candidates) == 1:
        return candidates[0], None, {}
    candidates = sorted(candidates, key=lambda v: -v.length)
    return candidates[0], None, {"note": f"{len(candidates)} main {name} vessels; longest used"}


def extract_trees(left: graph.CoronaryTree, right: graph.CoronaryTree,
                  sigma_mm: float = DEFAULT_SIGMA_MM, step_mm: float = RESAMPLE_MM,
                  window_mm: float = DEFAULT_WINDOW_MM) -> list[VesselTortuosity]:
    """The tortuosity panel for LM, LAD, LCX and RCA in one case's two trees. Always four rows,
    even where a vessel is absent or unmeasurable -- see ``_missing``."""
    trees = {"left": left, "right": right}
    rows = []
    for name, side in VESSEL_SIDES.items():
        tree = trees[side]
        vessel, reason, extra = _select_vessel(tree, name)
        if vessel is None:
            rows.append(_missing(name, side, reason, **extra))
            continue
        if tree.warnings:
            extra["tree_warnings"] = "; ".join(tree.warnings)
        result = measure(vessel.points, sigma_mm=sigma_mm, step_mm=step_mm, window_mm=window_mm)
        if isinstance(result, str):
            extra["vessel"] = vessel.index
            rows.append(_missing(name, side, result, **extra))
            continue
        extra.update(result.pop("extra"))
        rows.append(VesselTortuosity(side=side, name=name, vessel=vessel.index,
                                     n_segments=len(vessel.segments), sigma_mm=sigma_mm,
                                     step_mm=step_mm, window_mm=window_mm, extra=extra, **result))
    return rows


def extract_case(case_id: int, root=None, sigma_mm: float = DEFAULT_SIGMA_MM,
                 step_mm: float = RESAMPLE_MM, window_mm: float = DEFAULT_WINDOW_MM) -> list[VesselTortuosity]:
    """Every named vessel's tortuosity panel for one case. ``root`` selects predicted centerlines
    (see ``graph.load_trees``)."""
    trees = graph.load_trees(case_id, root)
    return extract_trees(trees["left"], trees["right"], sigma_mm, step_mm, window_mm)
