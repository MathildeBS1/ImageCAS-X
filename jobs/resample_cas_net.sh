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
#
#   bsub < jobs/resample_cas_net.sh                            # skip already-cached scans
#   bsub -env "all, OVERWRITE=1" < jobs/resample_cas_net.sh    # reprocess every scan

cd /zhome/e2/6/224426/project/ImageCAS-X || exit 1
. ./env.sh
mkdir -p logs

CONFIG="${CONFIG:-configs/cas_net.json}"
EXTRA_ARGS=""
if [ -n "$OVERWRITE" ]; then
    EXTRA_ARGS="--overwrite"
fi

echo "=== config: $CONFIG  overwrite: ${OVERWRITE:-0} ==="

python -m utils.offline_resample_images_to_disk -c "$CONFIG" --workers 8 $EXTRA_ARGS

echo "=== cache size ==="
du -sh "$ImageCAS_X_data_path"/volumes_resampled "$ImageCAS_X_data_path"/segmentations_resampled
