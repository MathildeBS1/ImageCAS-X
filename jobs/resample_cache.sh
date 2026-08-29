#!/bin/sh

#BSUB -q hpc
#BSUB -J imagecasx_resample
#BSUB -n 8
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=8GB]"
#BSUB -W 24:00
#BSUB -o logs/resample_%J.out
#BSUB -e logs/resample_%J.err

# Step 4: the 0.5 mm isotropic .npy cache every method shares. CPU-only, run once.
# float32 volumes + uint8 masks -> budget ~100-150 GB for 800 cases.

cd /zhome/e2/6/224426/project/ImageCAS-X
source env.sh

python -m utils.offline_resample_images_to_disk -c configs/cas_net.json --workers 8

echo "=== cache size ==="
du -sh "$ImageCAS_X_data_path"/volumes_resampled "$ImageCAS_X_data_path"/segmentations_resampled
