#!/bin/sh

#BSUB -q hpc
#BSUB -J tortuosity_deciles
#BSUB -n 1
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 4:00
#BSUB -o logs/tortuosity_deciles_%J.out
#BSUB -e logs/tortuosity_deciles_%J.err

# RCA scores T_l for all 800 scans (train, val, test), then the decile groups and figures. CPU only.
#   bsub < jobs/tortuosity_deciles.sh
# Scores: $ImageCAS_X_results_path/tortuosity_merged/{train,val,test}_vessels.csv
# Groups: $ImageCAS_X_results_path/tortuosity_deciles/groups.csv, figures/rca_tortuosity_{deciles,examples}.pdf
# The log prints the cut-offs and group sizes quoted in thesis/week5/rca_tortuosity.tex.

source env.sh
for s in train val test; do python -m tortuosity.run_merged_tests cohort --split $s; done
python scripts/tortuosity_deciles.py make
