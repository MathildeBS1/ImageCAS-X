"""Shared plotting helpers: consistent artery colours across every figure.

Rendering is matplotlib-only and headless (Agg). PyVista is used elsewhere purely
as a file parser -- the login node has no DISPLAY and no guaranteed OSMesa.
"""

from __future__ import annotations

import json

import matplotlib

matplotlib.use("Agg")

import numpy as np
from matplotlib.colors import to_rgba

from . import paths

# Left-sided arteries get cool colours, right-sided warm ones, so which system a
# branch belongs to is readable at a glance. L-PDA/L-PLA are the posterior vessels
# in left-dominant hearts, coloured magenta to set them apart from both systems.
ARTERY_COLORS: dict[str, str] = {
    "LM": "#1f3b73",
    "LAD": "#2f6fd0",
    "D1": "#5aa9e6",
    "D2": "#8ecae6",
    "LCX": "#0f8a7a",
    "OM1": "#2eb086",
    "OM2": "#7fd8a8",
    "IM": "#7b52ab",
    "RCA": "#a01c26",
    "R-PDA": "#e8622a",
    "R-PLA": "#f2a541",
    "L-PDA": "#c2379a",
    "L-PLA": "#e07bc4",
    "Other": "#9aa0a6",
}

ARTERY_ORDER = list(ARTERY_COLORS)


def load_label_map() -> dict[int, str]:
    """Segmentation label -> artery name, as derived by scripts/derive_label_map.py."""
    path = paths.LABEL_MAP
    return {int(k): v for k, v in json.loads(path.read_text()).items()}


def color_for(name: str) -> str:
    return ARTERY_COLORS.get(name, "#9aa0a6")


def label_rgba_table(label_map: dict[int, str], alpha: float = 1.0) -> np.ndarray:
    """(max_label+1, 4) RGBA lookup; index 0 (background) is transparent."""
    table = np.zeros((max(label_map) + 1, 4))
    for lbl, name in label_map.items():
        table[lbl] = to_rgba(color_for(name), alpha)
    return table


def set_axes_equal(ax) -> None:
    """Equal aspect for 3D axes -- anatomy must not be visually distorted."""
    limits = np.array([ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()])
    centre = limits.mean(axis=1)
    radius = 0.5 * (limits[:, 1] - limits[:, 0]).max()
    ax.set_xlim3d(centre[0] - radius, centre[0] + radius)
    ax.set_ylim3d(centre[1] - radius, centre[1] + radius)
    ax.set_zlim3d(centre[2] - radius, centre[2] + radius)


def legend_handles(names, **kw):
    from matplotlib.lines import Line2D

    return [
        Line2D([0], [0], color=color_for(n), lw=3, label=n)
        for n in sorted(set(names), key=lambda x: ARTERY_ORDER.index(x) if x in ARTERY_ORDER else 99)
    ]


def first_hit_projection(labels: np.ndarray, axis: int, flip: bool = False) -> np.ndarray:
    """Front-face projection: the label of the first non-zero voxel along ``axis``.

    A plain max-projection would be meaningless here -- label values are nominal,
    so 'largest label' says nothing about what is nearest the viewer.
    """
    vol = np.flip(labels, axis=axis) if flip else labels
    mask = vol > 0
    any_hit = mask.any(axis=axis)
    first = np.argmax(mask, axis=axis)
    out = np.take_along_axis(vol, np.expand_dims(first, axis), axis=axis).squeeze(axis)
    return np.where(any_hit, out, 0)


def shade_faces(points: np.ndarray, tris: np.ndarray, base_color: str,
                light=(0.3, 0.4, 0.85), ambient: float = 0.35) -> np.ndarray:
    """Lambertian per-face shading, so a mesh reads as 3D instead of a flat blob."""
    v = points[tris]
    normals = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0])
    norms = np.linalg.norm(normals, axis=1, keepdims=True)
    normals = normals / np.maximum(norms, 1e-12)
    light = np.asarray(light, dtype=float)
    light /= np.linalg.norm(light)
    intensity = ambient + (1 - ambient) * np.clip(np.abs(normals @ light), 0, 1)
    rgba = np.tile(np.asarray(to_rgba(base_color)), (len(tris), 1))
    rgba[:, :3] *= intensity[:, None]
    return rgba


def crop_to_foreground(labels: np.ndarray, pad: int = 8) -> tuple[np.ndarray, tuple]:
    """Crop a label volume to its foreground bounding box; the volume is mostly air."""
    idx = np.argwhere(labels > 0)
    lo = np.maximum(idx.min(0) - pad, 0)
    hi = np.minimum(idx.max(0) + pad + 1, labels.shape)
    sl = tuple(slice(int(a), int(b)) for a, b in zip(lo, hi))
    return labels[sl], sl
