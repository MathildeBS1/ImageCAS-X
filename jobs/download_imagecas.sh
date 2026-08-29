#!/bin/sh

#BSUB -q hpc
#BSUB -J imagecas_download
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 12:00
#BSUB -o logs/download_%J.out
#BSUB -e logs/download_%J.err

# Step 1: fetch the base ImageCAS CTA volumes. The ImageCAS-X labels we already have
# are an extension of this cohort -- same 1000 case ids, same geometry.
# Needs ~/.config/kaggle/kaggle.json (kaggle.com -> Settings -> Create New Token).
# Budget 60-100 GB and several hours; never run this on the login node.

cd /zhome/e2/6/224426/project/ImageCAS-X
source env.sh

RAW=/dtu/blackhole/0a/224426/imagecas_raw
mkdir -p "$RAW"

uv tool run --from kaggle kaggle datasets download \
    -d xiaoweixumedicalai/imagecas -p "$RAW"

echo "=== unzipping ==="
cd "$RAW"
for z in *.zip; do
    unzip -n -q "$z" && echo "unzipped $z"
done

echo "=== what landed ==="
find "$RAW" -name "*.nii.gz" | head -5
find "$RAW" -name "*.nii.gz" | wc -l
