"""Loaders for the three representations of each coronary tree.

Frames: segmentations come back in voxel space plus their RAS affine; centerlines
and surfaces come back in LPS (see ``coords``). Nothing here converts frames for
you -- do it explicitly so it stays visible at the call site.
"""

from __future__ import annotations

from dataclasses import dataclass

import nibabel as nib
import numpy as np
import pyvista as pv

from . import paths


@dataclass
class Segmentation:
    """Multi-label coronary segmentation. ``labels`` is (X, Y, Z) uint8, 0 = background."""

    case_id: int
    labels: np.ndarray
    affine: np.ndarray  # voxel -> RAS

    @property
    def spacing(self) -> np.ndarray:
        """Voxel size in mm. Varies per case and is anisotropic -- never assume."""
        return np.linalg.norm(self.affine[:3, :3], axis=0)

    def present_labels(self) -> np.ndarray:
        u = np.unique(self.labels)
        return u[u > 0]


@dataclass
class Centerline:
    """One side's centerline tree, in LPS.

    ``segment_label`` / ``segment_name`` give the artery each point belongs to.
    ``branch_points`` / ``end_points`` / ``start_points`` are 0/1 flags marking
    tree topology, precomputed by whoever produced the dataset.
    """

    case_id: int
    side: str
    points: np.ndarray  # (N, 3) LPS
    segment_label: np.ndarray
    segment_name: np.ndarray
    branch_points: np.ndarray
    end_points: np.ndarray
    start_points: np.ndarray
    lines: list[np.ndarray]  # point-index polylines

    def label_to_name(self) -> dict[int, str]:
        return {
            int(lbl): str(self.segment_name[self.segment_label == lbl][0])
            for lbl in np.unique(self.segment_label)
        }


@dataclass
class Surface:
    """Triangulated lumen surface, in LPS."""

    case_id: int
    points: np.ndarray  # (N, 3) LPS
    faces: np.ndarray  # (M, 3) triangle vertex indices


def load_segmentation(case_id: int) -> Segmentation:
    img = nib.load(paths.segmentation_path(case_id))
    return Segmentation(
        case_id=case_id,
        labels=np.asarray(img.dataobj, dtype=np.uint8),
        affine=img.affine,
    )


def _polylines(mesh: pv.PolyData) -> list[np.ndarray]:
    """Split the VTK line connectivity into individual polylines."""
    out, lines = [], mesh.lines
    i = 0
    while i < len(lines):
        n = int(lines[i])
        out.append(np.asarray(lines[i + 1 : i + 1 + n], dtype=int))
        i += n + 1
    return out


def load_centerline(case_id: int, side: str) -> Centerline:
    mesh = pv.read(paths.centerline_path(case_id, side))
    pd_ = mesh.point_data
    return Centerline(
        case_id=case_id,
        side=side,
        points=np.asarray(mesh.points, dtype=float),
        segment_label=np.asarray(pd_["segment_label"]),
        segment_name=np.asarray(pd_["segment_name"]),
        branch_points=np.asarray(pd_["branch_points"]),
        end_points=np.asarray(pd_["end_points"]),
        start_points=np.asarray(pd_["start_points"]),
        lines=_polylines(mesh),
    )


def load_centerlines(case_id: int) -> dict[str, Centerline]:
    """Both sides. Left and right use disjoint segment_label ranges."""
    return {side: load_centerline(case_id, side) for side in ("left", "right")}


def load_surface(case_id: int) -> Surface:
    mesh = pv.read(paths.surface_path(case_id)).triangulate()
    return Surface(
        case_id=case_id,
        points=np.asarray(mesh.points, dtype=float),
        faces=mesh.faces.reshape(-1, 4)[:, 1:],
    )
