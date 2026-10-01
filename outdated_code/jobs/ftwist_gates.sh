#!/bin/sh

#BSUB -q hpc
#BSUB -J ftwist_gates
#BSUB -n 1
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 1:00
#BSUB -o logs/ftwist_gates_%J.out
#BSUB -e logs/ftwist_gates_%J.err

# f_twist gates G1 (noise tolerance) and G2 (not a proxy), CPU only, ~20 min.
# Gates and thresholds are declared in tortuosity/research/unified/ftwist_gates.py.
#   bsub < jobs/ftwist_gates.sh
# Report: $ImageCAS_X_results_path/tortuosity_research/unified/ftwist_gates_train150.txt

source env.sh
python -m tortuosity.research.unified.ftwist_gates --n 150
