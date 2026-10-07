#!/bin/sh

#BSUB -q gpul40s
#BSUB -J totalseg_heart
#BSUB -n 4
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=8GB]"
#BSUB -W 48:00
#BSUB -o logs/totalseg_heart_%J.out
#BSUB -e logs/totalseg_heart_%J.err

# TotalSegmentator heartchambers_highres (aorta, 4 chambers, myocardium, pulmonary artery) on the
# native volumes of one split -> $RESULTS/totalseg/<id>/<structure>.nii.gz. The aorta places the
# ostia (bifurcation/extract.py), the chambers give the labeller its heart frame. Same model as
# Bransby et al. 2026. Resumes: cases with an aorta file are skipped. Failures go to
# $RESULTS/totalseg/failed_<split>.txt.
#   bsub -env "all, SPLIT=train" < jobs/totalseg_heart.sh      # also val, test
#
# One-time setup on the login node (separate venv: isolates nnunetv2's dependencies; weights on
# /work3 because /zhome is nearly full):
#   uv venv /work3/s254124/venvs/totalseg --python 3.11
#   VIRTUAL_ENV=/work3/s254124/venvs/totalseg uv pip install TotalSegmentator
#   export TOTALSEG_HOME_DIR=/work3/s254124/totalseg_home
#   /work3/s254124/venvs/totalseg/bin/totalseg_set_license -l <your licence key>
#   /work3/s254124/venvs/totalseg/bin/totalseg_download_weights -t heartchambers_highres

source env.sh
export TOTALSEG_HOME_DIR=/work3/s254124/totalseg_home
TS=/work3/s254124/venvs/totalseg/bin
SPLIT=${SPLIT:-test}
OUT=$ImageCAS_X_results_path/totalseg
mkdir -p "$OUT"
: > "$OUT/failed_$SPLIT.txt"
$TS/pip show TotalSegmentator | grep -i '^version' > "$OUT/version.txt"

for id in $(cat "$ImageCAS_X_data_path/filelist/$SPLIT.txt"); do
    [ -f "$OUT/$id/aorta.nii.gz" ] && continue
    $TS/TotalSegmentator -i "$ImageCAS_X_data_path/volumes/$id.img.nii.gz" -o "$OUT/$id" \
        --task heartchambers_highres || echo "$id" >> "$OUT/failed_$SPLIT.txt"
done
echo "failed: $(wc -l < "$OUT/failed_$SPLIT.txt")"
