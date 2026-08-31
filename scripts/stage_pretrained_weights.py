"""Stage the delivered pretrained weights as run directories inference.py can read.

The weights shipped with ImageCAS-X (Zenodo 21887809) arrived on blackhole 2026-08-31
as bare state_dicts. `inference.py` defaults `model.checkpoint` to
`<run_dir>/<method>_best.pt`, so laying each file out under that name makes every
single-checkpoint method runnable with no config change at all:

    python -m inference -c configs/cas_net.json -r cas_net_pretrained --split test
    python -m evaluate  -c configs/cas_net.json -r cas_net_pretrained

**Why not just set `model.checkpoint` in the method config.** `train.py` builds its
model through the same `build_model(cfg)` that `inference.py` uses, and `build_model`
loads `config.model.checkpoint` whenever it is set. A checkpoint left in
`configs/cas_net.json` would therefore turn every later "fresh" training run into a
silent fine-tune of the published weights, and the run would look normal in the logs.
Staging run dirs keeps the training path untouched.

The ImageCAS 3-stage baseline is the exception: it loads five checkpoints by name
rather than one, so it is wired directly in `configs/imagecas_inference.json`, which is
an inference-only config and never trains anything.

Each file is loaded into the model its config builds, with strict=True, before the link
is made -- a weight file staged under the wrong method fails here rather than three
hours into an inference run.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

from models.registry import _MODEL_REGISTRY
import models.registry  # noqa: F401  -- fires the @register_model decorators
from utils.config import BenchmarkConfig, RESULTS_PATH_ENV, WEIGHTS_PATH_ENV

# method config -> weight file, relative to $ImageCAS_X_weights_path.
# Keyed by the config because that is what names the architecture the file has to fit.
SINGLE_CHECKPOINT_METHODS = {
    "configs/cas_net.json": "cas_net.pt",
    "configs/ffr_unet.json": "ffr_unet.pt",
    "configs/swin_unetr.json": "swin_unetr.pt",
    "configs/ade_htl.json": "ade_htl/ade_htl_stage2.pt",
    "configs/ade_htl_stage1_coarse.json": "ade_htl/ade_htl_stage1.pt",
    "configs/imagecas_stage2_coarse_dilated.json": "imagecas/imagecas_stage2_coarse_dilated.pt",
    "configs/imagecas_stage3_patch_16.json": "imagecas/imagecas_stage3_patch_16.pt",
    "configs/imagecas_stage3_patch_32.json": "imagecas/imagecas_stage3_patch_32.pt",
    "configs/imagecas_stage3_patch_64.json": "imagecas/imagecas_stage3_patch_64.pt",
}

# Not staged here, and why:
#   nnunet/    native nnU-Net layout (nnUNetTrainer__nnUNetPlans__3d_fullres, 5 folds).
#              No model is registered for "nnunet" -- it runs under its own CLI and
#              drops predictions into <run_dir>/predictions/ for evaluate.py to score.
#   imagecas/  the four files above are also reachable as one assembled method via
#              configs/imagecas_inference.json; see that config for the Stage-1 gap.


def verify(config_path: str, weight_path: str) -> str:
    """Build the model this config declares and load the weights into it strictly.
    Returns the model name on success; raises otherwise."""
    cfg = BenchmarkConfig.from_json(config_path)
    cls = _MODEL_REGISTRY.get(cfg.model.name)
    if cls is None:
        raise ValueError(f"no model registered as '{cfg.model.name}' for {config_path}")
    model = cls(**cfg.model.params)
    state = torch.load(weight_path, map_location="cpu", weights_only=True)
    model.load_state_dict(state, strict=True)
    return cfg.model.name


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--weights-root", default=os.environ.get(WEIGHTS_PATH_ENV, ""),
                        help=f"defaults to ${WEIGHTS_PATH_ENV}")
    parser.add_argument("--results-root", default=os.environ.get(RESULTS_PATH_ENV, ""),
                        help=f"defaults to ${RESULTS_PATH_ENV}")
    parser.add_argument("--suffix", default="_pretrained",
                        help="run dir is <method_name><suffix> (default: _pretrained)")
    parser.add_argument("--dry-run", action="store_true",
                        help="verify the weights load, but create nothing")
    args = parser.parse_args()

    if not args.weights_root:
        parser.error(f"set ${WEIGHTS_PATH_ENV} (source env.sh) or pass --weights-root")
    if not args.results_root:
        parser.error(f"set ${RESULTS_PATH_ENV} (source env.sh) or pass --results-root")

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    failures = []

    for config_rel, weight_rel in sorted(SINGLE_CHECKPOINT_METHODS.items()):
        config_path = os.path.join(repo_root, config_rel)
        weight_path = os.path.join(args.weights_root, weight_rel)
        name = os.path.basename(config_rel)

        if not os.path.exists(weight_path):
            print(f"[skip] {name:42s} no weight file at {weight_path}")
            failures.append((name, "missing weight file"))
            continue

        try:
            model_name = verify(config_path, weight_path)
        except Exception as exc:  # noqa: BLE001 -- report every method, don't stop at the first
            print(f"[FAIL] {name:42s} {type(exc).__name__}: {str(exc)[:110]}")
            failures.append((name, type(exc).__name__))
            continue

        method_name = BenchmarkConfig.from_json(config_path).method_name
        run_dir = os.path.join(args.results_root, f"{method_name}{args.suffix}")
        link = os.path.join(run_dir, f"{method_name}_best.pt")

        if args.dry_run:
            print(f"[ok]   {name:42s} {model_name:16s} -> would link {link}")
            continue

        os.makedirs(run_dir, exist_ok=True)
        # Replace rather than fail, so re-running after a weights refresh is safe.
        if os.path.islink(link) or os.path.exists(link):
            os.remove(link)
        os.symlink(weight_path, link)
        print(f"[ok]   {name:42s} {model_name:16s} -> {method_name}{args.suffix}/")

    print()
    staged = len(SINGLE_CHECKPOINT_METHODS) - len(failures)
    print(f"{staged}/{len(SINGLE_CHECKPOINT_METHODS)} methods staged under {args.results_root}")
    if failures:
        for name, why in failures:
            print(f"  unstaged: {name} ({why})")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
