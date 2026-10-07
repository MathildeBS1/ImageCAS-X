"""Every file the bifurcation code reads or writes. Edit the two roots after moving machines.

The dataset is read-only input (see CLAUDE.md): nothing here writes to it.
"""
from __future__ import annotations

import functools
import os
from pathlib import Path

import pandas as pd

DATA = Path(os.environ.get("ImageCAS_X_data_path", "/work3/s254124/ImageCAS-X_dataset"))
RESULTS = Path("/work3/s254124/imagecasx_results")  # everything this code writes
REPO = Path(__file__).resolve().parents[1]

# inputs
CENTERLINES = DATA / "centerlines"      # <case>.coronary_{left,right}_centerline.vtk, LPS mm
SEGMENTATIONS = DATA / "segmentations"  # <case>.coronary.nii.gz, multi-label, voxel space + RAS affine
FILELIST = DATA / "filelist"            # <split>.txt
DESCRIPTORS = DATA / "Descriptors.xlsx" # per-case Image Quality, Dominance, Disease
LABEL_MAP = REPO / "knowledge" / "docs_thesis" / "label_map.json"  # segment_label -> artery name

# outputs
RADIUS = RESULTS / "centerline_radius"  # radius.py: <case>_<side>.npy, one per centerline
TOTALSEG = RESULTS / "totalseg"  # jobs/totalseg_heart.sh: <case>/<structure>.nii.gz, native geometry
EXTRACTED = RESULTS / "extracted_centerlines"  # extract.py: <source>_t<t>/, delivered file layout


def centerline_path(case_id: int, side: str) -> Path:
    if side not in ("left", "right"):
        raise ValueError(f"side must be 'left' or 'right', got {side!r}")
    return CENTERLINES / f"{case_id}.coronary_{side}_centerline.vtk"


def segmentation_path(case_id: int) -> Path:
    return SEGMENTATIONS / f"{case_id}.coronary.nii.gz"


def prediction_path(run: str, case_id: int, split: str = "test") -> Path:
    """Binary mask ``inference.py`` wrote for a run, in the scan's native geometry. Test goes to
    ``predictions/``, any other split to ``predictions_<split>/``."""
    return RESULTS / run / ("predictions" if split == "test" else f"predictions_{split}") / f"{case_id}.nii.gz"


def totalseg_path(case_id: int, structure: str) -> Path:
    return TOTALSEG / str(case_id) / f"{structure}.nii.gz"


def radius_cache_path(case_id: int, side: str) -> Path:
    """Per-point lumen radius for one delivered centerline, written by ``radius.py``.
    Not created here: absence means "not computed"."""
    return RADIUS / f"{case_id}_{side}.npy"


@functools.lru_cache(maxsize=None)
def split_ids(name: str) -> tuple[int, ...]:
    """Case ids in a split: 'train', 'val', 'test' or 'exclude'. Never a directory glob."""
    return tuple(int(x) for x in (FILELIST / f"{name}.txt").read_text().split())


@functools.lru_cache(maxsize=1)
def descriptors() -> pd.DataFrame:
    """Per-case descriptors indexed by Scan ID.

    All 1000 ImageCAS cases. The 200 with ``Image Quality == 0`` are exactly the ids in
    ``exclude.txt`` and have NaN Dominance/Disease.
    """
    return pd.read_excel(DESCRIPTORS).set_index("Scan ID")
