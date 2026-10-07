#!/bin/bash

#BSUB -q hpc
#BSUB -J download_imagecas
#BSUB -n 4
#BSUB -R "rusage[mem=4GB] span[hosts=1]"
#BSUB -W 12:00
#BSUB -o logs/download_imagecas_%J.out
#BSUB -e logs/download_imagecas_%J.err

# Fetch raw ImageCAS (Kaggle xiaoweixumedicalai/imagecas, ~89 GB of split zips) to work3, then
# unpack it into $ImageCAS_X_data_path/{volumes,imagecas_orig_labels}/ (1000 + 1000 .nii.gz). CPU only.
#   bsub < jobs/download_imagecas.sh
# Auth: ~/.kaggle/access_token. The Kaggle copy stays under $KAGGLEHUB_CACHE as the untouched original.
# Each block of 200 scans is a split zip whose last part is shipped renamed to .change2zip.

set -euo pipefail
source env.sh
export KAGGLEHUB_CACHE=/work3/s254124/kagglehub_cache

SRC=$(uv run --no-project --with kagglehub python -c \
  'import kagglehub; print(kagglehub.dataset_download("xiaoweixumedicalai/imagecas"))' | tail -1)
echo "Kaggle download: $SRC"

STAGE=/work3/s254124/imagecas_unpack
VOL=$ImageCAS_X_data_path/volumes
LAB=$ImageCAS_X_data_path/imagecas_orig_labels
mkdir -p "$STAGE/parts" "$STAGE/extract" "$VOL" "$LAB"

for block in 1-200 201-400 401-600 601-800 801-1000; do
  ln -sf "$SRC/$block.change2zip" "$STAGE/parts/$block.zip"
  for p in "$SRC/$block".z0*; do ln -sf "$p" "$STAGE/parts/"; done
  7za x -y -o"$STAGE/extract" "$STAGE/parts/$block.zip"
done

find "$STAGE/extract" -name '*.img.nii.gz' -exec mv -t "$VOL" {} +
find "$STAGE/extract" -name '*.label.nii.gz' -exec mv -t "$LAB" {} +
echo "volumes: $(ls "$VOL" | wc -l)  labels: $(ls "$LAB" | wc -l)  (expect 1000 each)"
echo "left in $STAGE/extract:"; find "$STAGE/extract" -type f
