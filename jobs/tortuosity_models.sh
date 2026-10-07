#!/bin/sh

#BSUB -q hpc
#BSUB -J tortuosity_models
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 2:00
#BSUB -o logs/tortuosity_models_%J.out
#BSUB -e logs/tortuosity_models_%J.err

# Both arms of the tortuosity-against-Disease comparison, for LAD, LCX and RCA: the logistic
# regression on T_5 and length, and the transformer on the ordered per-point profile. CPU only.
#   bsub < jobs/tortuosity_models.sh
# Needs the score CSVs that jobs/tortuosity_deciles.sh writes, and torch in the venv
# (uv pip install torch --index-url https://download.pytorch.org/whl/cpu).
# Measured at 7 minutes per vessel on one core, so about 25 minutes single-threaded; the speed-up
# from the four cores asked for here has not been measured. The login node is capped at one core,
# which is the only reason this is a job at all.
# The log holds the numbers to quote: both AUCs with CIs and the paired difference, per vessel.
# Writes tortuosity_disease/ and tortuosity_transformer_disease/ under RESULTS.

source env.sh
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4  # env.sh pins these to 1 for the fan-out precompute jobs
python -m tortuosity.regression_model
python -m tortuosity.transformer_model
