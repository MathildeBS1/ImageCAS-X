#!/bin/sh

#BSUB -q gpua100
#BSUB -J cas_net
#BSUB -n 14
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=8GB]"
#BSUB -R "select[gpu80gb]"
#BSUB -W 24:00
#BSUB -o logs/cas_net_%J.out
#BSUB -e logs/cas_net_%J.err

# Step 7: train CAS-Net from scratch (objective 5).
#
# 1000 epochs x 250 iterations will not fit in one 24 h walltime, so this script is
# written to be resubmitted. First submission trains fresh; every later one continues
# the same run folder:
#
#     bsub < jobs/train_cas_net.sh                    # fresh, prints run_dir
#     RUN_DIR=cas_net_2026-... bsub < jobs/train_cas_net.sh    # continue
#
# Chain them without babysitting:
#     bsub -w "ended(<jobid>)" -env "all, RUN_DIR=<run_dir>" < jobs/train_cas_net.sh
#
# Patch is [128,160,160] at batch 5 -- this needs an 80 GB A100. If you land on a 40 GB
# card, lower training.batch_size in configs/cas_net.json and record the deviation:
# the benchmark's fairness claim rests on matched settings.

cd /zhome/e2/6/224426/project/ImageCAS-X
source env.sh
mkdir -p logs

nvidia-smi

if [ -n "$RUN_DIR" ]; then
    echo "=== resuming $RUN_DIR ==="
    python -m train -c configs/cas_net.json --resume "$RUN_DIR"
else
    echo "=== fresh run ==="
    python -m train -c configs/cas_net.json
fi
