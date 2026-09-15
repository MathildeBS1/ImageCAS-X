"""Render one training crop under each augmentation step, for the training-chapter
figure. Runs on the login node (CPU, reads one cached .npy crop, no GPU needed) --
same class of job as utils.verify_dataloaders.

Usage:
    python -m utils.make_augmentation_figure -c configs/cas_net.json
"""
import argparse
import copy
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from utils.config import BenchmarkConfig
from utils.seeding import seed_everything
from preprocessing.pipeline import build_preprocessing
from dataloading.random_crop_dataset import RandomCropDataset
from augmentation.steps import (
    RandomFlip, GaussianNoise, GaussianBlur, MultiplicativeBrightness,
    Contrast, SimulateLowResolution, GammaTransform,
)

# One panel per configured step, each forced to p=1.0 so it is visible; params
# otherwise copied from configs/pipeline.json's "augmentation" block.
_PANELS = [
    ("random_flip", RandomFlip),
    ("gaussian_noise", GaussianNoise),
    ("gaussian_blur", GaussianBlur),
    ("multiplicative_brightness", MultiplicativeBrightness),
    ("contrast", Contrast),
    ("simulate_low_resolution", SimulateLowResolution),
    ("gamma", GammaTransform),
    ("gamma_invert", GammaTransform),
]


def _extreme(range_pair, neutral=None):
    """Collapse a (lo, hi) range to its most visible single value: the endpoint
    farthest from `neutral` (for parameters centred on "no change"), or the
    largest value (for parameters where more is simply more visible)."""
    lo, hi = range_pair
    if neutral is None:
        return (hi, hi)
    return (lo, lo) if abs(lo - neutral) >= abs(hi - neutral) else (hi, hi)


# Each configured step is a random draw within its training range, which can land
# near the weak end and look almost invisible in a single still image. For this
# illustrative figure only (never for actual training) each step is instead pushed
# to the most visible extreme of its own configured range.
_RANGE_OVERRIDES = {
    "random_flip": lambda p: {"p_per_axis": 1.0},
    "gaussian_noise": lambda p: {"variance_range": _extreme(p.get("variance_range", (0.0, 0.1)))},
    "gaussian_blur": lambda p: {"sigma_range": _extreme(p.get("sigma_range", (0.1, 1.0)))},
    "multiplicative_brightness": lambda p: {
        "multiplier_range": _extreme(p.get("multiplier_range", (0.75, 1.25)), neutral=1.0)},
    "contrast": lambda p: {"contrast_range": _extreme(p.get("contrast_range", (0.75, 1.25)), neutral=1.0)},
    "simulate_low_resolution": lambda p: {
        "zoom_range": (p.get("zoom_range", (0.5, 1.0))[0],) * 2},
    "gamma": lambda p: {"gamma_range": _extreme(p.get("gamma_range", (0.7, 1.5)), neutral=1.0)},
    "gamma_invert": lambda p: {"gamma_range": _extreme(p.get("gamma_range", (0.7, 1.5)), neutral=1.0)},
}


def make_figure(config_path: str, out_path: str, seed: int) -> None:
    seed_everything(seed)
    cfg = BenchmarkConfig.from_json(config_path)
    cfg.validate()

    preprocessing = build_preprocessing(cfg)
    # augmentation=None: this dataset instance returns the raw, preprocessed crop:
    # the "original" panel, and the input every other panel is built from.
    dataset = RandomCropDataset(cfg, split="train", preprocessing=preprocessing,
                                 augmentation=None)
    sample = dataset[True]  # True = force a foreground-containing crop
    vol0 = sample["volume"][0].numpy()
    scan_id = sample["scan_id"]
    z = vol0.shape[2] // 2

    aug_params = cfg.augmentation.get("params", {})
    panels = [("original", vol0)]
    for name, cls in _PANELS:
        params = dict(aug_params.get(name, {}))
        params["p"] = 1.0
        if name in _RANGE_OVERRIDES:
            params.update(_RANGE_OVERRIDES[name](params))
        step = cls(**params)
        out = step.apply({"volume": vol0.copy(), "mask": sample["mask"].numpy().copy(),
                          "spacing": sample["spacing"]})
        label = name if name != "gamma_invert" else "gamma_invert"
        panels.append((label, out["volume"]))

    n = len(panels)
    ncols = 3
    nrows = -(-n // ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(3.2 * ncols, 3.2 * nrows))
    axes = axes.reshape(-1)
    for ax, (label, vol) in zip(axes, panels):
        ax.imshow(vol[:, :, z].T, cmap="gray", origin="lower", vmin=0, vmax=1)
        ax.set_title(label, fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    for ax in axes[n:]:
        ax.axis("off")

    fig.suptitle(f"Augmentation steps on one training crop ({scan_id})")
    plt.tight_layout()
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"-> saved {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default="configs/cas_net.json")
    parser.add_argument("--out", default="figures/augmentation_examples.png")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    make_figure(args.config, args.out, args.seed)
