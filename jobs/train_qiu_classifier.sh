#!/bin/sh

#BSUB -q hpc
#BSUB -J qiu_classifier
#BSUB -n 16
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 8:00
#BSUB -o logs/qiu_classifier_%J.out
#BSUB -e logs/qiu_classifier_%J.err

# Train the centerline classifier P of Qiu et al. 2025 (eq. 7). CPU only, run once.
# See docs_thesis/qiu_reconnection.md, step 1.
#
#   bsub < jobs/train_qiu_classifier.sh
#
# Samples 40 train scans + 10 val scans (for reporting only) from the 0.5 mm cache,
# fits a cascade forest, writes $ImageCAS_X_results_path/qiu_centerline_classifier/
# {model.joblib, report.json}. Check report.json's val_auc and val_mean_p_by_region
# before running anything that depends on P.

cd /zhome/e2/6/224426/project/ImageCAS-X || exit 1
. ./env.sh
mkdir -p logs

CONFIG="${CONFIG:-configs/cas_net_qiu.json}"
echo "=== config: $CONFIG ==="

python scripts/train_centerline_classifier.py -c "$CONFIG" --workers 16
