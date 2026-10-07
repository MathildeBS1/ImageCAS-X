#!/bin/sh

#BSUB -q hpc
#BSUB -J radius_cache
#BSUB -n 1
#BSUB -R "rusage[mem=8GB] span[hosts=1]"
#BSUB -W 2:00
#BSUB -o logs/radius_cache_%J.out
#BSUB -e logs/radius_cache_%J.err

# GT lumen radius at every delivered centerline point, all splits (about 1 s per case). Needed
# by score_extraction.py (tolerances) and the labeller (radius features).
#   bsub < jobs/radius_cache.sh

source env.sh
for s in train val test; do python -m bifurcation.radius --split $s; done
