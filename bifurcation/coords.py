"""Coordinate-frame conversions between the dataset's two representations.

The NIfTI segmentations and the VTK centerlines do NOT share a coordinate frame:

- NIfTI affines (``srow``) are RAS by definition (x=Right, y=Anterior, z=Superior).
- The VTK centerlines and surfaces are LPS (x=Left, y=Posterior, z=Superior), the
  ITK/VTK convention.

The two differ by a sign flip on x and y. Overlaying them without converting produces a
figure that looks plausible but is wrong, and silently corrupts any feature that mixes
voxel and mesh data, which is exactly what ``radius.py`` does. Always go through these.
"""
from __future__ import annotations

import numpy as np

# LPS = diag(-1, -1, 1) @ RAS, and the transform is its own inverse.
_FLIP = np.diag([-1.0, -1.0, 1.0])


def ras_to_lps(points: np.ndarray) -> np.ndarray:
    """Convert (N, 3) points from RAS (NIfTI) to LPS (VTK)."""
    return np.asarray(points, dtype=float) @ _FLIP


def voxel_to_ras(ijk: np.ndarray, affine: np.ndarray) -> np.ndarray:
    """Map (N, 3) voxel indices to RAS world coordinates via the NIfTI affine."""
    ijk = np.asarray(ijk, dtype=float)
    return ijk @ affine[:3, :3].T + affine[:3, 3]


def voxel_to_lps(ijk: np.ndarray, affine: np.ndarray) -> np.ndarray:
    """Map (N, 3) voxel indices straight to LPS, the frame the centerlines live in."""
    return ras_to_lps(voxel_to_ras(ijk, affine))
