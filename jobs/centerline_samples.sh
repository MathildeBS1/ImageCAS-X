#!/bin/sh

#BSUB -q hpc
#BSUB -J imagecasx_clsamples
#BSUB -n 8
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=8GB]"
#BSUB -W 8:00
#BSUB -o logs/clsamples_%J.out
#BSUB -e logs/clsamples_%J.err

# Step 4: GT centerline sample points + covariates (dist_mm, segment_name,
# diameter_mm, hu). Feeds evaluate.py's per-segment / per-diameter / per-HU local Dice
# -- the stratified breakdown that makes the benchmark table reproducible.

cd /zhome/e2/6/224426/project/ImageCAS-X
source env.sh

python -m utils.precompute_centerline_samples -c configs/cas_net.json --split test --workers 8
