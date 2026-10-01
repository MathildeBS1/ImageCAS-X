"""Score every LAD, LCX and RCA of one ImageCAS-X split with T_l at each chord in CHORDS.

    python -m tortuosity.score --split train

Writes $ImageCAS_X_results_path/tortuosity_scores/<split>_vessels.csv, one row per vessel, and
<split>_failed.txt listing every case or vessel that could not be scored, with the reason.
"""
import argparse
import csv
import os
import time

import numpy as np

from .curvature import mean_abs_curvature
from .vessels import ARTERIES, load_vessels

CHORDS = (2, 5, 8)  # mm; 5 is the reported score, 2 and 8 the chord sensitivity check
MIN_LENGTH_MM = 15


def score(split, out_dir):
    data = os.environ["ImageCAS_X_data_path"]
    ids = [x.strip() for x in open(f"{data}/filelist/{split}.txt") if x.strip()]
    os.makedirs(out_dir, exist_ok=True)
    fails, n_rows, t0 = [], 0, time.time()
    with open(f"{out_dir}/{split}_vessels.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["case", "vessel", "length_mm"] + [f"T_{l}" for l in CHORDS])
        for case in ids:
            try:
                vessels = load_vessels(case, data)
            except Exception as e:
                fails.append((case, "all", repr(e)))
                continue
            for name in ARTERIES:
                P = vessels.get(name)
                length = np.linalg.norm(np.diff(P, axis=0), axis=1).sum() if P is not None else 0
                if length < MIN_LENGTH_MM:
                    fails.append((case, name, f"missing or shorter than {MIN_LENGTH_MM} mm"))
                    continue
                w.writerow([case, name, length] + [mean_abs_curvature(P, l) for l in CHORDS])
                n_rows += 1
    with open(f"{out_dir}/{split}_failed.txt", "w") as fh:
        fh.writelines(f"{a}\t{b}\t{c}\n" for a, b, c in fails)
    print(f"{split}: {len(ids)} cases, {n_rows} vessels, {len(fails)} failures, {time.time() - t0:.0f} s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="train", choices=["train", "val", "test"])
    ap.add_argument("--out", default=f"{os.environ.get('ImageCAS_X_results_path', '.')}/tortuosity_scores")
    a = ap.parse_args()
    score(a.split, a.out)
