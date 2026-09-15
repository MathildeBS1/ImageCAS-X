#!/bin/sh

#BSUB -q hpc
#BSUB -J extract_topology
#BSUB -n 8
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 4:00
#BSUB -o logs/extract_topology_%J.out
#BSUB -e logs/extract_topology_%J.err

# Radius-aware bifurcation angles on GT, the same on centerlines built from a run's predicted
# masks, the GT-vs-prediction validation, and the direction sensitivity sweep. CPU only.
#
#   bsub < jobs/extract_topology.sh
#   bsub -env "all, RUN=cas_net_2026-.." < jobs/extract_topology.sh
#
# Every step skips or overwrites cleanly, so a job killed at the walltime can be resubmitted:
# the radius cache and the predicted centerlines are per case and resume by default.
# Outputs go to $IMAGECASX_OUT (default /dtu/blackhole/0a/224426/imagecasx_derived).

cd /zhome/e2/6/224426/project/ImageCAS-X || exit 1
. ./env.sh
mkdir -p logs
set -e

RUN="${RUN:-cas_net_pretrained}"
echo "=== run: $RUN   code: $(git describe --always --dirty) ==="

echo "=== 1/6 radius cache for the 800 GT cases ==="
python scripts/compute_centerline_radius.py --workers 8

echo "=== 2/6 centerlines from $RUN's predicted masks (oracle ostium and names) ==="
python scripts/build_predicted_centerlines.py --run "$RUN" --workers 8

echo "=== 3/6 GT angles ==="
python scripts/extract_bifurcation_angles.py --source gt

echo "=== 4/6 predicted angles ==="
python scripts/extract_bifurcation_angles.py --source pred --run "$RUN"

echo "=== 5/6 validation: prediction vs GT ==="
python scripts/validate_extraction.py --run "$RUN"

echo "=== 6/6 direction sensitivity on GT ==="
python scripts/angle_sensitivity.py

python scripts/make_tree_figure.py 1
