# ImageCAS-X thesis environment. Source this before any run:  source env.sh
# Data + results roots (read by every config via utils/config.py)
export ImageCAS_X_data_path=/work3/s254124/ImageCAS-X_dataset
export ImageCAS_X_results_path=/work3/s254124/imagecasx_results

# /zhome is at 26/30 GB quota -- keep the venv and the uv cache off it.
export UV_CACHE_DIR=/work3/s254124/uv_cache
export UV_PROJECT_ENVIRONMENT=/work3/s254124/venvs/imagecasx
# uv venv/sync/run read UV_PROJECT_ENVIRONMENT; `uv pip` only reads VIRTUAL_ENV.
export VIRTUAL_ENV="$UV_PROJECT_ENVIRONMENT"
export PATH="$VIRTUAL_ENV/bin:$PATH"

# Thread pinning: train.py sets these itself, but they matter for the offline
# precompute scripts, which fan out with --workers.
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1

# Pretrained weights delivered with the dataset (Zenodo 21887809), staged on work3
# 2026-08-31. Referenced from configs as ${ImageCAS_X_weights_path}/... and expanded by
# utils/config.py, so no machine-local absolute path is ever committed.
export ImageCAS_X_weights_path=/work3/s254124/pretrained_weights
