#!/bin/sh

#BSUB -q hpc
#BSUB -J postproc_sweep
#BSUB -n 8
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=8GB]"
#BSUB -W 4:00
#BSUB -o logs/postproc_sweep_%J.out
#BSUB -e logs/postproc_sweep_%J.err

# Full test-split (160 scans) screen of postprocessing/variants.py against an
# existing run's saved predictions. CPU only, no GPU needed. See
# scripts/sweep_postprocessing.py and docs_thesis/postprocessing_sweep.md.
#
# A login-node screen on 32 of 160 test scans (2026-09-14, this task) already ranked
# the variants; this job re-runs the same set on the full cohort for the numbers
# that go in the thesis. --metrics full adds hd95 and cl_dice on top of the fast
# screen's dice + betti errors.
#
#   SRC       run dir holding the source predictions, default cas_net_pretrained
#   VARIANTS  comma-separated variant names, default = the ones the login-node
#             screen ran (excludes close_r3/close_r5, too slow for too little
#             signal there -- see docs_thesis/postprocessing_sweep.md)
#   METRICS   fast | full, default full (this job has the walltime budget)
#   WORKERS   default 8
#
#   bsub < jobs/sweep_postprocessing.sh
#   bsub -env "all, VARIANTS=size_500,close_r2_top2" < jobs/sweep_postprocessing.sh

cd /zhome/e2/6/224426/project/ImageCAS-X || exit 1
. ./env.sh
mkdir -p logs

SRC="${SRC:-cas_net_pretrained}"
VARIANTS="${VARIANTS:-baseline,size_200,size_500,size_1000,size_2000,keep_top2,close_r1,close_r2,open_r1,fill_holes,close_r2_top2,close_r3_top2}"
METRICS="${METRICS:-full}"
WORKERS="${WORKERS:-8}"

echo "=== src: $SRC  variants: $VARIANTS  metrics: $METRICS  workers: $WORKERS ==="

python scripts/sweep_postprocessing.py -c configs/cas_net.json --src "$SRC" \
    --variants "$VARIANTS" --workers "$WORKERS" --metrics "$METRICS"
