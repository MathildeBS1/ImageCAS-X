#!/bin/sh

#BSUB -q gpua40
#BSUB -J cas_net_infer
#BSUB -n 8
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=8GB]"
#BSUB -W 12:00
#BSUB -o logs/cas_net_infer_%J.out
#BSUB -e logs/cas_net_infer_%J.err

# CAS-Net inference + evaluation on the 160 test scans with the delivered pretrained weights.
#   bsub -env "all, RUN_DIR=cas_net_pretrained" < jobs/infer_eval_cas_net.sh
#   bsub -env "all, RUN_DIR=cas_net_pretrained, SPLIT=val" < jobs/infer_eval_cas_net.sh
# RUN_DIR is a directory under $ImageCAS_X_results_path holding cas_net_best.pt
# (cas_net_pretrained/ symlinks it to the delivered weights). Inference resumes by default.
# Results: $ImageCAS_X_results_path/$RUN_DIR/{predictions/,cas_net_results.json}

source env.sh
RUN_DIR=${RUN_DIR:-cas_net_pretrained}
SPLIT=${SPLIT:-test}   # val -> predictions_val/, for calibrating centerline extraction; not evaluated
python -m inference -c configs/cas_net.json -r "$ImageCAS_X_results_path/$RUN_DIR" --split $SPLIT
[ "$SPLIT" = "test" ] && python -m evaluate -c configs/cas_net.json -r "$ImageCAS_X_results_path/$RUN_DIR"
