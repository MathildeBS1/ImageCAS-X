#!/bin/sh

#BSUB -q gpuh100
#BSUB -J cas_net_infer
#BSUB -n 8
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=6GB]"
#BSUB -W 12:00
#BSUB -o logs/cas_net_infer_%J.out
#BSUB -e logs/cas_net_infer_%J.err

# Predict the test split, then score it. See docs_thesis/cas_net_walkthrough.md.
#
#   bsub -env "all, RUN_DIR=cas_net_pretrained" < jobs/infer_eval_cas_net.sh
#   bsub -env "all, RUN_DIR=cas_net_2026-.."    < jobs/infer_eval_cas_net.sh
#
# RUN_DIR is a folder under $ImageCAS_X_results_path. inference.py defaults
# model.checkpoint to <RUN_DIR>/cas_net_best.pt, so no config edit is needed.
#
# Inference resumes by default: scans already in predictions/ are skipped, so a job
# that hits the walltime can simply be resubmitted. Pass OVERWRITE=1 to redo them all,
# which you must do after retraining into an existing run dir.
#
# 160 test scans, each tiled at 50% overlap and run 4x for mirror TTA over X and Y.
# evaluate.py needs no GPU but is left in the same job so the two stay in step.
#
# SPLIT=val predicts the 80 val scans instead and skips evaluate.py (which scores
# test scans only). Use a separate run dir so val and test predictions never mix:
#
#   mkdir -p $ImageCAS_X_results_path/cas_net_pretrained_val
#   ln -s $ImageCAS_X_weights_path/cas_net.pt $ImageCAS_X_results_path/cas_net_pretrained_val/cas_net_best.pt
#   bsub -env "all, RUN_DIR=cas_net_pretrained_val, SPLIT=val" < jobs/infer_eval_cas_net.sh

cd /zhome/e2/6/224426/project/ImageCAS-X || exit 1
. ./env.sh
mkdir -p logs

CONFIG="${CONFIG:-configs/cas_net.json}"
SPLIT="${SPLIT:-test}"

if [ -z "$RUN_DIR" ]; then
    echo "RUN_DIR is required, e.g. -env \"all, RUN_DIR=cas_net_pretrained\"" >&2
    exit 1
fi

nvidia-smi
echo "=== config: $CONFIG   run_dir: $RUN_DIR   split: $SPLIT ==="

if [ -n "$OVERWRITE" ]; then
    python -m inference -c "$CONFIG" -r "$RUN_DIR" --split "$SPLIT" --overwrite || exit 1
else
    python -m inference -c "$CONFIG" -r "$RUN_DIR" --split "$SPLIT" || exit 1
fi

if [ "$SPLIT" = "test" ]; then
    python -m evaluate -c "$CONFIG" -r "$RUN_DIR" -j 8
fi
