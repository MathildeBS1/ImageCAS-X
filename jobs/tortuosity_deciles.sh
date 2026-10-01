#!/bin/sh

#BSUB -q hpc
#BSUB -J tortuosity_deciles
#BSUB -n 1
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 1:00
#BSUB -o logs/tortuosity_deciles_%J.out
#BSUB -e logs/tortuosity_deciles_%J.err

# RCA scores T_l for all 800 scans (train, val, test), then the decile groups and figures. CPU only.
#   bsub < jobs/tortuosity_deciles.sh
# Scores: $ImageCAS_X_results_path/tortuosity_scores/{train,val,test}_vessels.csv
# Groups: $ImageCAS_X_results_path/tortuosity_deciles/groups.csv, figures/rca_tortuosity_{deciles,examples}.pdf
# The log prints the cut-offs and group sizes quoted in thesis/week5/rca_tortuosity.tex.

source env.sh
python -m tortuosity.check
for s in train val test; do python -m tortuosity.score --split $s; done
python -m tortuosity.deciles make
