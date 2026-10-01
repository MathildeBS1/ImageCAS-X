#!/bin/sh

#BSUB -q gpua100
#BSUB -J cas_net
#BSUB -n 14
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=5GB]"
#BSUB -R "select[gpu80gb]"
#BSUB -W 72:00
#BSUB -o logs/cas_net_%J.out
#BSUB -e logs/cas_net_%J.err

# Train CAS-Net (thesis objective 5). See docs_thesis/cas_net_walkthrough.md.
#
# 1000 epochs x 250 iterations does not fit one walltime, so this script is written to
# be resubmitted. The first submission trains fresh and prints its run_dir; every later
# submission continues that same folder via --resume.
#
#   bsub < jobs/train_cas_net.sh                                    # fresh
#   bsub -env "all, RUN_DIR=cas_net_2026-.." < jobs/train_cas_net.sh # continue
#
# Chain without babysitting, so the next job is queued before the current one ends:
#   bsub -w "ended(<jobid>)" -env "all, RUN_DIR=<run_dir>" < jobs/train_cas_net.sh
#
# Override the config for the 5-epoch timing run, and send it to a shorter, less
# contended queue (command-line bsub options beat the #BSUB lines above):
#   bsub -q gpuh100 -W 4:00 -env "all, CONFIG=configs/cas_net_smoke.json" \
#        < jobs/train_cas_net.sh
#
# -n 14 matches training.num_workers=14 in configs/pipeline.json. select[gpu80gb] is
# not optional: batch 5 at 128x160x160 runs in fp32 (amp is false for CAS-Net) and will
# OOM on a 40 GB card.

cd /zhome/e2/6/224426/project/ImageCAS-X || exit 1
. ./env.sh
mkdir -p logs

CONFIG="${CONFIG:-configs/cas_net.json}"

nvidia-smi
echo "=== config: $CONFIG ==="

if [ -n "$RUN_DIR" ]; then
    echo "=== resuming $RUN_DIR ==="
    python -m train -c "$CONFIG" --resume "$RUN_DIR"
else
    echo "=== fresh run ==="
    python -m train -c "$CONFIG"
fi
