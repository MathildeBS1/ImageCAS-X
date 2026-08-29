#!/bin/sh

#BSUB -q hpc
#BSUB -J imagecas_dl
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=8GB]"
#BSUB -W 24:00
#BSUB -o logs/download_%J.out
#BSUB -e logs/download_%J.err

# Step 1: fetch the base ImageCAS CTA volumes (Zeng et al., arXiv:2211.01607).
# The ImageCAS-X labels we already hold are an extension of this cohort: same 1000
# case ids, same geometry. Licence: CC BY-NC 4.0 (non-commercial) -- fine for thesis
# work, cite the ImageCAS paper alongside ImageCAS-X.
#
# The dataset is NOT plain zips. It is five split (multi-volume) zip archives of
# ~18 GB each, and the final segment of each -- the one carrying the central
# directory -- was uploaded as `.change2zip` because Kaggle would not take a second
# `.zip`. So: download all 25 parts, rename `.change2zip` -> `.zip`, then extract.
# Info-ZIP's unzip cannot read split archives at all; 7za can, without first having
# to concatenate them into a second 18 GB file.
#
# Idempotent: parts already present at their expected size are skipped, so this can
# be resubmitted after a walltime kill and will pick up where it left off.
#
#   bsub < jobs/download_imagecas.sh

set -u

cd /zhome/e2/6/224426/project/ImageCAS-X
. ./env.sh

SLUG=xiaoweixumedicalai/imagecas
RAW=/dtu/blackhole/0a/224426/imagecas_raw
ZIPS="$RAW/archives"
EXTRACT="$RAW/extracted"
mkdir -p "$ZIPS" "$EXTRACT"

# name:expected_bytes, from `kaggle datasets files`. Sizes are checked so a truncated
# transfer is retried rather than silently feeding a corrupt archive to the extractor.
MANIFEST="
1-200.change2zip:807139732
1-200.z01:4293918720
1-200.z02:4293918720
1-200.z03:4293918720
1-200.z04:4293918720
201-400.change2zip:705922295
201-400.z01:4293918720
201-400.z02:4293918720
201-400.z03:4293918720
201-400.z04:4293918720
401-600.change2zip:738690684
401-600.z01:4293918720
401-600.z02:4293918720
401-600.z03:4293918720
401-600.z04:4293918720
601-800.change2zip:285553993
601-800.z01:4293918720
601-800.z02:4293918720
601-800.z03:4293918720
601-800.z04:4293918720
801-1000.change2zip:669980273
801-1000.z01:4293918720
801-1000.z02:4293918720
801-1000.z03:4293918720
801-1000.z04:4293918720
"

echo "=== downloading 25 parts (~83 GB) to $ZIPS ==="
for entry in $MANIFEST; do
    name=${entry%%:*}
    want=${entry##*:}
    target="$ZIPS/$name"

    if [ -f "$target" ]; then
        have=$(stat -c %s "$target")
        if [ "$have" = "$want" ]; then
            echo "  ok   $name ($have bytes)"
            continue
        fi
        echo "  redo $name (have $have, want $want)"
        rm -f "$target"
    fi

    echo "  get  $name"
    kaggle datasets download -d "$SLUG" -f "$name" -p "$ZIPS" --force || {
        echo "FAILED to download $name"; exit 1; }

    # Kaggle sometimes wraps a single file in its own .zip; unwrap if so.
    if [ ! -f "$target" ] && [ -f "$target.zip" ]; then
        unzip -o -q "$target.zip" -d "$ZIPS" && rm -f "$target.zip"
    fi

    have=$(stat -c %s "$target" 2>/dev/null || echo 0)
    [ "$have" = "$want" ] || { echo "SIZE MISMATCH $name: $have != $want"; exit 1; }
done

kaggle datasets download -d "$SLUG" -f imageCAS_data_split.xlsx -p "$RAW" --force

echo "=== renaming final segments .change2zip -> .zip ==="
for f in "$ZIPS"/*.change2zip; do
    [ -e "$f" ] || continue
    mv -f "$f" "${f%.change2zip}.zip" && echo "  ${f##*/} -> $(basename "${f%.change2zip}.zip")"
done

echo "=== extracting ==="
for grp in 1-200 201-400 401-600 601-800 801-1000; do
    echo "--- $grp ---"
    7za x -y -o"$EXTRACT" "$ZIPS/$grp.zip" > "$RAW/7za_$grp.log" 2>&1 \
        && echo "  extracted $grp" \
        || { echo "  FAILED $grp -- see $RAW/7za_$grp.log"; tail -20 "$RAW/7za_$grp.log"; exit 1; }
done

echo "=== what landed ==="
find "$EXTRACT" -name "*.nii.gz" | wc -l
find "$EXTRACT" -name "*.nii.gz" | head -5
du -sh "$EXTRACT" "$ZIPS"
