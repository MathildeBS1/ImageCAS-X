#!/bin/sh

#BSUB -q hpc
#BSUB -J qiu_reconnect
#BSUB -n 8
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 6:00
#BSUB -o logs/qiu_reconnect_%J.out
#BSUB -e logs/qiu_reconnect_%J.err

# Repair an existing run's predictions with Qiu et al. 2025 stage 2, then score them.
# CPU only. See docs_thesis/qiu_reconnection.md.
#
#   RUN_DIR   output run dir under $ImageCAS_X_results_path (required)
#   CONFIG    default configs/cas_net_qiu.json
#   SRC_RUN   run dir holding the predictions to repair, default cas_net_pretrained
#   SPLIT     default test; evaluate.py only runs for test
#   SET       one reconnection param override, e.g. eval_threshold=99
#   OVERWRITE redo scans already written
#
#   bsub -env "all, RUN_DIR=cas_net_pretrained_keep2, CONFIG=configs/cas_net_keep2.json" < jobs/qiu_reconnect.sh
#   bsub -env "all, RUN_DIR=cas_net_pretrained_val_qiu_calib, SRC_RUN=cas_net_pretrained_val, SPLIT=val, SET=eval_threshold=99" < jobs/qiu_reconnect.sh
#   bsub -env "all, RUN_DIR=cas_net_pretrained_qiu" < jobs/qiu_reconnect.sh
#   bsub -env "all, RUN_DIR=cas_net_pretrained_qiu_noremove, CONFIG=configs/cas_net_qiu_noremove.json" < jobs/qiu_reconnect.sh
#
# Resumes by default. A scan that fails gets no prediction and an .error.txt log; the
# job still evaluates, and evaluate.py reports the gap under "coverage".

cd /zhome/e2/6/224426/project/ImageCAS-X || exit 1
. ./env.sh
mkdir -p logs

CONFIG="${CONFIG:-configs/cas_net_qiu.json}"
SRC_RUN="${SRC_RUN:-cas_net_pretrained}"
SPLIT="${SPLIT:-test}"

if [ -z "$RUN_DIR" ]; then
    echo "RUN_DIR is required, e.g. -env \"all, RUN_DIR=cas_net_pretrained_qiu\"" >&2
    exit 1
fi

EXTRA_ARGS=""
[ -n "$SET" ] && EXTRA_ARGS="$EXTRA_ARGS --set $SET"
[ -n "$OVERWRITE" ] && EXTRA_ARGS="$EXTRA_ARGS --overwrite"

echo "=== config: $CONFIG  src: $SRC_RUN  run_dir: $RUN_DIR  split: $SPLIT  extra: $EXTRA_ARGS ==="

python scripts/qiu_reconnect.py -c "$CONFIG" --src "$SRC_RUN" -r "$RUN_DIR" \
    --split "$SPLIT" --workers 8 $EXTRA_ARGS \
    || echo "[warn] some scans failed; see $RUN_DIR/reconnection_logs/*.error.txt" >&2

if [ "$SPLIT" = "test" ]; then
    python -m evaluate -c "$CONFIG" -r "$RUN_DIR" -j 8
fi
