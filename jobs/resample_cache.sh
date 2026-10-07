#!/bin/sh

#BSUB -q hpc
#BSUB -J resample_cache
#BSUB -n 8
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=6GB]"
#BSUB -W 24:00
#BSUB -o logs/resample_cache_%J.out
#BSUB -e logs/resample_cache_%J.err

# Build the shared 0.5 mm isotropic cache (volumes_resampled/ + segmentations_resampled/, 800
# scans, ~128 GB) that every config's dataloader reads. CPU only; run once, then resubmit
# jobs/infer_eval_cas_net.sh.
#   bsub < jobs/resample_cache.sh
# Writes into $ImageCAS_X_data_path. Without --overwrite, existing files are skipped, so a
# killed job can simply be resubmitted.

source env.sh
python -m utils.offline_resample_images_to_disk -c configs/cas_net.json --workers 8
