#!/bin/sh

#BSUB -q hpc
#BSUB -J extract_centerlines
#BSUB -n 16
#BSUB -R "rusage[mem=4GB] span[hosts=1]"
#BSUB -W 6:00
#BSUB -o logs/extract_centerlines_%J.out
#BSUB -e logs/extract_centerlines_%J.err

# Centerlines from masks (bifurcation/skeleton.py) and their scores against the delivered ones.
# About 15 s per case per setting. Needs jobs/totalseg_heart.sh (train for the cap, plus the split)
# and jobs/radius_cache.sh.
#
#   bsub -env "all, STEP=calibrate" < jobs/extract_centerlines.sh
#       fit the ostium cap on train, then the pruning grid on CAS-Net val predictions; pick t at
#       the knee of term_spurious_mm vs term_missed_mm in summary_val.json
#   bsub -env "all, STEP=test, T=<chosen t>" < jobs/extract_centerlines.sh
#       frozen t on test: CAS-Net predictions, GT masks (implementation floor), paired Wilcoxon,
#       plus the replication check on val GT masks with oracle ostia

source env.sh
W=16
if [ "$STEP" = "calibrate" ]; then
    python -m bifurcation.extract --fit-cap
    for t in 1.5 2 3 4 5; do
        python -m bifurcation.extract --source cas_net_pretrained --split val --t $t --workers $W
        python -m bifurcation.score_extraction --dir cas_net_pretrained_t$t --split val
    done
else
    python -m bifurcation.extract --source gt --split val --t $T --oracle-ostia --workers $W
    python -m bifurcation.score_extraction --dir gt_t${T}_oracle --split val
    python -m bifurcation.extract --source gt --split test --t $T --workers $W
    python -m bifurcation.score_extraction --dir gt_t$T --split test
    python -m bifurcation.extract --source cas_net_pretrained --split test --t $T --workers $W
    python -m bifurcation.score_extraction --dir cas_net_pretrained_t$T --split test --against gt_t$T
    for t in 1.5 2 3 4 5; do   # pruning sensitivity on test, secondary
        [ "$t" = "$T" ] && continue
        python -m bifurcation.extract --source cas_net_pretrained --split test --t $t --workers $W
        python -m bifurcation.score_extraction --dir cas_net_pretrained_t$t --split test
    done
fi
