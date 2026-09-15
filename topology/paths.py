"""Locations and case bookkeeping for the ImageCAS-X dataset.

The dataset is read-only input (see CLAUDE.md): nothing here writes to it.
"""

from __future__ import annotations

import functools
import os
from pathlib import Path

import pandas as pd

# One env var for both halves of the repo: the benchmark framework reads
# ImageCAS_X_data_path in utils/config.py, and so do we. It points at the composed
# root (symlinks to the read-only dataset, plus volumes/ and the caches), so the
# topology code and the segmentation code always see the same cohort.
DATA_ROOT = Path(
    os.environ.get("ImageCAS_X_data_path")
    or os.environ.get("IMAGECASX_ROOT")
    or "/dtu/blackhole/0a/224426/imagecasx_data"
)

SEGMENTATIONS = DATA_ROOT / "segmentations"
CENTERLINES = DATA_ROOT / "centerlines"
SURFACES = DATA_ROOT / "surfaces"
#: CT volumes, from the base ImageCAS cohort rather than the ImageCAS-X delivery.
#: Note the suffix differs from every other directory: "<id>.img.nii.gz".
VOLUMES = DATA_ROOT / "volumes"
FILELIST = DATA_ROOT / "filelist"
DESCRIPTORS = DATA_ROOT / "Descriptors.xlsx"

# Repo-side output locations.
REPO_ROOT = Path(__file__).resolve().parents[1]
FIGURES = REPO_ROOT / "figures"
# Thesis docs live in docs_thesis/; docs/ is the upstream GitHub Pages site.
DOCS = REPO_ROOT / "docs_thesis"
LABEL_MAP = DOCS / "label_map.json"

# Derived artifacts go to blackhole, never to /zhome (94% full) and never into the
# read-only dataset. Treat it as scratch: anything here must be re-derivable by code.
OUTPUT_ROOT = Path(os.environ.get("IMAGECASX_OUT", "/dtu/blackhole/0a/224426/imagecasx_derived"))


def output_dir(name: str) -> Path:
    """A named subdirectory of the derived-artifact tree, created on demand."""
    d = OUTPUT_ROOT / name
    d.mkdir(parents=True, exist_ok=True)
    return d


def code_version() -> str:
    """Short git description of the working tree, recorded alongside outputs so a
    number in the thesis can be traced back to the code that produced it."""
    import subprocess

    try:
        out = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "describe", "--always", "--dirty", "--abbrev=12"],
            capture_output=True, text=True, timeout=10, check=True,
        )
        return out.stdout.strip()
    except (subprocess.SubprocessError, OSError):
        return "unknown"


def segmentation_path(case_id: int) -> Path:
    return SEGMENTATIONS / f"{case_id}.coronary.nii.gz"


def centerline_path(case_id: int, side: str) -> Path:
    if side not in ("left", "right"):
        raise ValueError(f"side must be 'left' or 'right', got {side!r}")
    return CENTERLINES / f"{case_id}.coronary_{side}_centerline.vtk"


def surface_path(case_id: int) -> Path:
    return SURFACES / f"{case_id}.coronary_surface.vtk"


def volume_path(case_id: int) -> Path:
    """The CT volume. Unlike the other three, this comes from base ImageCAS and is
    only present for cases that were downloaded -- check ``.exists()`` before use."""
    return VOLUMES / f"{case_id}.img.nii.gz"


@functools.lru_cache(maxsize=None)
def split_ids(name: str) -> tuple[int, ...]:
    """Case ids in a split: 'train', 'val', 'test' or 'exclude'."""
    text = (FILELIST / f"{name}.txt").read_text().split()
    return tuple(int(x) for x in text)


@functools.lru_cache(maxsize=1)
def usable_ids() -> tuple[int, ...]:
    """The 800 non-excluded cases, sorted."""
    return tuple(sorted(set(split_ids("train")) | set(split_ids("val")) | set(split_ids("test"))))


@functools.lru_cache(maxsize=1)
def descriptors() -> pd.DataFrame:
    """Per-case descriptors indexed by Scan ID.

    All 1000 ImageCAS cases. The 200 with ``Image Quality == 0`` are exactly the
    ids in ``exclude.txt`` and have NaN Dominance/Disease.
    """
    return pd.read_excel(DESCRIPTORS).set_index("Scan ID")


def has_all_files(case_id: int) -> bool:
    return (
        segmentation_path(case_id).exists()
        and centerline_path(case_id, "left").exists()
        and centerline_path(case_id, "right").exists()
        and surface_path(case_id).exists()
    )
