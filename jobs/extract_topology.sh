#!/bin/sh

#BSUB -q hpc
#BSUB -J extract_topology
#BSUB -n 8
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 4:00
#BSUB -o logs/extract_topology_%J.out
#BSUB -e logs/extract_topology_%J.err

# Radius-aware bifurcation angles on the GT centerlines, plus the direction sensitivity
# sweep. GT-tree-building + feature extraction only -- no predicted masks, no postprocessing
# extension. CPU only.
#
#   bsub < jobs/extract_topology.sh
#
# Every step skips or overwrites cleanly, so a job killed at the walltime can be resubmitted:
# the radius cache is per case and resumes by default.
# Outputs go to $IMAGECASX_OUT (default /dtu/blackhole/0a/224426/imagecasx_derived).

cd /zhome/e2/6/224426/project/ImageCAS-X || exit 1
. ./env.sh
mkdir -p logs
set -e

echo "=== code: $(git describe --always --dirty) ==="

echo "=== 1/3 radius cache for the 800 GT cases ==="
python scripts/compute_centerline_radius.py --workers 8

echo "=== 2/3 GT bifurcation angles ==="
python scripts/extract_bifurcation_angles.py --source gt

echo "=== 3/3 direction sensitivity on GT ==="
python scripts/angle_sensitivity.py

python scripts/make_tree_figure.py 1
