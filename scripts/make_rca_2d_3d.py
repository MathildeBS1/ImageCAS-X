"""Figure: one RCA centerline, in its actual 3D shape, its best possible 2D view,
and the rate it rotates out of that view.

The 2D panel is not an arbitrary projection: it is the vessel's own best-fit
plane (top two PCA components of its points), i.e. the least-foreshortened
view any single 2D projection (an angiographic view, say) could give it. Points
are coloured by signed distance out of that plane -- exactly what a 2D
reading discards, whichever angle it is taken from. non-planarity is the
third PCA eigenvalue's share of the total, the same number reported in
tortuosity_and_representation.tex's case-1 table.

The bottom panel adds the out-of-plane rotation rate, d'(s) = T(s).normal
(the unit tangent's component along the plane normal, one derivative, not
three like torsion), read as sin(angle between the tangent and the plane).
Unlike curvature or torsion this needs no smoothing to be trustworthy: d(s)
uses zero derivatives and d'(s) only one, so both stay well clear of the
position-noise floor that swamps curvature-based measures on a raw
centerline (see docs_thesis -- the noise-floor checks behind this figure).

    uv run python scripts/make_rca_2d_3d.py images/1

Writes figures/rca_2d_3d_<case>.{pdf,png}. Upload the PDF to
content/background/figures/ in Overleaf.
"""

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers the 3d projection)
from scipy.ndimage import gaussian_filter1d

from discover_common import case_files, orient_edges, read_centerline, resolve, segment_names, segment_paths
from discover_tortuosity import DEFAULT_SIGMA_MM, RESAMPLE_MM, resample

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
INK = "#1f2933"
MUTED = "#7b8794"
CURVE = "#2a78d6"
RATE_COLOR = "#d83d29"


def rca_points(prefix):
    files = case_files(prefix)
    names = segment_names()
    label_id = {v: k for k, v in names.items()}["RCA"]
    centerline = read_centerline(files["right"])
    oriented, _root = orient_edges(centerline)
    pieces = segment_paths(centerline, oriented)[label_id]
    return max(pieces, key=len)  # longest contiguous run, (n, 3) LPS mm


def best_fit_plane(points):
    """PCA plane through the points: (2d coords in-plane, signed out-of-plane distance,
    non-planarity = 3rd eigenvalue's share of total variance, centroid, normal)."""
    centroid = points.mean(axis=0)
    centered = points - centroid
    _u, s, vt = np.linalg.svd(centered, full_matrices=False)
    eigenvalues = s ** 2
    coords_2d = centered @ vt[:2].T
    out_of_plane = centered @ vt[2]
    non_planarity = float(eigenvalues[2] / eigenvalues.sum())
    return coords_2d, out_of_plane, non_planarity, centroid, vt[2]


def out_of_plane_rate(points, centroid, normal, sigma_mm=DEFAULT_SIGMA_MM, step_mm=RESAMPLE_MM):
    """d(s) and d'(s) = T(s).normal along arc length, against the same plane
    best_fit_plane fit on the raw points -- d needs no derivative, d' needs
    only the tangent, so both stay usable without the heavy smoothing
    curvature or torsion would need."""
    curve, _raw_arc = resample(points, step_mm)
    if sigma_mm > 0:
        curve = gaussian_filter1d(curve, sigma_mm / step_mm, axis=0, mode="nearest")
    arc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(curve, axis=0), axis=1))])
    d = (curve - centroid) @ normal
    tangent = np.gradient(curve, step_mm, axis=0)
    tangent /= np.maximum(np.linalg.norm(tangent, axis=1, keepdims=True), 1e-12)
    angle_deg = np.degrees(np.arcsin(np.clip(tangent @ normal, -1.0, 1.0)))
    return arc, d, angle_deg


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case", nargs="?", default="images/1", help="case prefix, e.g. images/1")
    args = parser.parse_args()

    prefix = resolve(args.case)
    case = os.path.basename(prefix)
    points = rca_points(prefix)
    coords_2d, out_of_plane, non_planarity, centroid, normal = best_fit_plane(points)
    arc, d_profile, angle_deg = out_of_plane_rate(points, centroid, normal)

    plt.rcParams.update({"font.size": 9, "font.family": "sans-serif"})
    fig = plt.figure(figsize=(9.5, 7.2))
    grid = fig.add_gridspec(2, 2, height_ratios=(2.2, 1), hspace=0.4, wspace=0.3)

    ax3d = fig.add_subplot(grid[0, 0], projection="3d")
    ax3d.plot(points[:, 0], points[:, 1], points[:, 2], color=CURVE, lw=2.0)
    ax3d.scatter(*points[0], color=INK, s=30, label="ostium end")
    ax3d.scatter(*points[-1], color="white", edgecolor=INK, s=30, linewidth=1.2, label="distal end")
    ax3d.set_title(f"RCA, case {case} -- actual 3D shape", fontsize=10, color=INK)
    ax3d.set_xlabel("x (mm)", fontsize=8)
    ax3d.set_ylabel("y (mm)", fontsize=8)
    ax3d.set_zlabel("z (mm)", fontsize=8)
    ax3d.legend(fontsize=7, loc="upper left")

    ax2d = fig.add_subplot(grid[0, 1])
    vmax = np.abs(out_of_plane).max()
    sc = ax2d.scatter(coords_2d[:, 0], coords_2d[:, 1], c=out_of_plane, cmap="coolwarm",
                       s=8, vmin=-vmax, vmax=vmax)
    ax2d.plot(coords_2d[:, 0], coords_2d[:, 1], color=MUTED, lw=0.8, zorder=1)
    ax2d.plot(coords_2d[0, 0], coords_2d[0, 1], "o", color=INK, ms=6)
    ax2d.plot(coords_2d[-1, 0], coords_2d[-1, 1], "o", mfc="white", mec=INK, mew=1.2, ms=6)
    ax2d.set_aspect("equal")
    ax2d.set_title(f"same vessel, 2D: its own best-fit plane\n"
                    f"non-planarity = {non_planarity:.4f}", fontsize=10, color=INK)
    ax2d.set_xlabel("in-plane (mm)", fontsize=8)
    ax2d.set_ylabel("in-plane (mm)", fontsize=8)
    cbar = fig.colorbar(sc, ax=ax2d, shrink=0.8)
    cbar.set_label("distance out of the plane (mm)\n= what the 2D view hides", fontsize=7)

    ax_rate = fig.add_subplot(grid[1, :])
    ax_rate.axhline(0, color=MUTED, lw=0.8, zorder=1)
    ax_rate.plot(arc, d_profile, color=CURVE, lw=1.6, label="d(s): distance out of plane (mm)")
    ax_rate.set_xlabel("arc length from ostium end (mm)", fontsize=8)
    ax_rate.set_ylabel("d(s)  (mm)", color=CURVE, fontsize=8)
    ax_rate.tick_params(axis="y", labelcolor=CURVE)

    ax_angle = ax_rate.twinx()
    ax_angle.plot(arc, angle_deg, color=RATE_COLOR, lw=1.2, alpha=0.85,
                  label="d'(s): out-of-plane rotation rate (deg)")
    ax_angle.set_ylabel("out-of-plane angle  (deg)", color=RATE_COLOR, fontsize=8)
    ax_angle.tick_params(axis="y", labelcolor=RATE_COLOR)
    ax_angle.set_ylim(-95, 95)

    ax_rate.set_title("d(s) needs no derivative, d'(s) needs one -- both stay "
                       "readable without the smoothing curvature or torsion need",
                       fontsize=9, color=INK)
    lines = [l for l in ax_rate.get_lines() + ax_angle.get_lines() if not l.get_label().startswith("_")]
    ax_rate.legend(lines, [l.get_label() for l in lines], fontsize=7, loc="upper right")

    fig.suptitle(f"RCA centerline, case {case}: the 2D view is this vessel's best possible "
                 "projection, and still hides real 3D structure", fontsize=9.5, color=INK)
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    os.makedirs(OUT_DIR, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT_DIR, f"rca_2d_3d_{case}.{ext}"), dpi=300)
    print(f"wrote figures/rca_2d_3d_{case}.{{pdf,png}}")
    print(f"non_planarity={non_planarity:.5f}  max |out_of_plane|={vmax:.2f} mm  "
          f"max |angle|={np.abs(angle_deg).max():.1f} deg")


if __name__ == "__main__":
    main()
