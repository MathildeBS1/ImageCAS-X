"""Score every LAD, LCX and RCA of one ImageCAS-X split with every feature in FEATURES.

    python -m tortuosity.score --split train

Writes the SCORES directory of paths.py: <split>_vessels.csv, one row per vessel with one
column per feature, and <split>_failed.txt listing every case or vessel that could not be
scored, with the reason.

To add a feature, write a function of the centerline P, an (n, 3) array of LPS mm with the
ostium first, and add one line to FEATURES. Rerun score for all three splits; the new column
is then available to `tortuosity.regression_model --features` by its name here.
"""
import argparse
import csv
import os
import time
from functools import partial

import numpy as np

from . import paths
from .curvature import mean_abs_curvature
from .vessels import ARTERIES, load_vessels


def length_mm(P):
    return np.linalg.norm(np.diff(P, axis=0), axis=1).sum()


CHORDS = (2, 5, 8)  # mm; 5 is the reported score, 2 and 8 the chord sensitivity check
FEATURES = {"length_mm": length_mm, **{f"T_{l}": partial(mean_abs_curvature, l=l) for l in CHORDS}}
MIN_LENGTH_MM = 15


def score(split):
    out_dir = paths.SCORES
    ids = [x.strip() for x in open(paths.FILELIST.format(split=split)) if x.strip()]
    os.makedirs(out_dir, exist_ok=True)
    fails, n_rows, t0 = [], 0, time.time()
    with open(f"{out_dir}/{split}_vessels.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["case", "vessel"] + list(FEATURES))
        for case in ids:
            try:
                vessels = load_vessels(case)
            except Exception as e:
                fails.append((case, "all", repr(e)))
                continue
            for name in ARTERIES:
                P = vessels.get(name)
                if P is None:
                    fails.append((case, name, "missing"))
                    continue
                row = {k: f(P) for k, f in FEATURES.items()}
                if row["length_mm"] < MIN_LENGTH_MM:
                    fails.append((case, name, f"shorter than {MIN_LENGTH_MM} mm"))
                    continue
                w.writerow([case, name] + list(row.values()))
                n_rows += 1
    with open(f"{out_dir}/{split}_failed.txt", "w") as fh:
        fh.writelines(f"{a}\t{b}\t{c}\n" for a, b, c in fails)
    print(f"{split}: {len(ids)} cases, {n_rows} vessels, {len(fails)} failures, {time.time() - t0:.0f} s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="train", choices=["train", "val", "test"])
    a = ap.parse_args()
    score(a.split)
