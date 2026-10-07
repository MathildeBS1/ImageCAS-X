#!/bin/sh

#BSUB -q hpc
#BSUB -J train_labeller
#BSUB -n 4
#BSUB -R "rusage[mem=8GB] span[hosts=1]"
#BSUB -W 12:00
#BSUB -o logs/train_labeller_%J.out
#BSUB -e logs/train_labeller_%J.err

# Segment labeller end to end on CPU (trees are tens of nodes): prepare the delivered trees and the
# extracted test trees, train the GNN and its no-message-passing reference, evaluate both on
# delivered and extracted test trees. Needs jobs/totalseg_heart.sh (all splits),
# jobs/radius_cache.sh and the frozen extraction from jobs/extract_centerlines.sh.
#   bsub -env "all, T=<chosen t>" < jobs/train_labeller.sh

source env.sh
EXT=cas_net_pretrained_t$T
for s in train val test; do python -m labelling.data --source delivered --split $s; done
python -m labelling.data --source $EXT --split test
python -m labelling.train --run gnn3 --layers 3
python -m labelling.train --run gnn0 --layers 0
for run in gnn3 gnn0; do
    python -m labelling.evaluate --run $run --source delivered
    python -m labelling.evaluate --run $run --source $EXT
done
