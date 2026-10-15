"""Score every LAD, LCX and RCA of one ImageCAS-X split with every feature in FEATURES, plus taper.

    python -m tortuosity.score --split train
    python -m tortuosity.score --split train --skip-taper   # centerline features only, under a minute

Writes the SCORES directory of paths.py: <split>_vessels.csv, one row per vessel with one
column per feature, and <split>_failed.txt listing every case or vessel that could not be
scored, with the reason. A vessel whose taper cannot be measured keeps its row, with NaN taper
columns and a line in the failure list.

To add a feature, write a function of the centerline P, an (n, 3) array of LPS mm with the
ostium first, and add one line to FEATURES. Rerun score for all three splits; the new column
is then available to `tortuosity.regression_model --features` by its name here.

Taper (taper.py) also needs the lumen mask and the junctions on the trunk, so it is scored
outside FEATURES, in TAPER_COLUMNS:
  T_taper          primary: area-equivalent cross-section radius
  T_taper_edt      sensitivity: the same fit on the distance-transform radius (bifurcation.radius)
  taper_mm_used    arc span of the samples the fit used, mm
  taper_frac_used  share of the trunk's 0.5 mm samples the fit used
The r(s) profile behind each value goes to TAPER_PROFILES as <case>_<vessel>.npz.
"""
import argparse
import csv
import os
import time
from functools import partial

import nibabel as nib
import numpy as np

from bifurcation.radius import radius_at

from . import paths
from .curvature import mean_abs_curvature
from .taper import branch_keep, cross_section_radius, resample_arc, tangents, taper
from .vessels import ARTERIES, load_vessels


def length_mm(P):
    return np.linalg.norm(np.diff(P, axis=0), axis=1).sum()


CHORDS = (2, 5, 8)  # mm; 5 is the reported score, 2 and 8 the chord sensitivity check
FEATURES = {"length_mm": length_mm, **{f"T_{l}": partial(mean_abs_curvature, l=l) for l in CHORDS}}
MIN_LENGTH_MM = 15
TAPER_COLUMNS = ("T_taper", "T_taper_edt", "taper_mm_used", "taper_frac_used")
STEP_MM, TANGENT_MM = 0.5, 5.0  # sample spacing; tangent scale, the same as T_5


def score_taper(case, name, P, junction_s, labels, affine):
    """(row of TAPER_COLUMNS, reason or None) for one trunk; also writes its profile."""
    Q, s = resample_arc(P, STEP_MM)
    r, touch = cross_section_radius(Q, tangents(Q, STEP_MM, TANGENT_MM), labels, affine, {ARTERIES[name][0]})
    keep = branch_keep(s, junction_s, r) & ~touch
    T, span, frac, reason = taper(s, r, keep)
    r_edt = radius_at(Q, labels > 0, affine)
    T_edt = taper(s, r_edt, keep)[0]
    os.makedirs(paths.TAPER_PROFILES, exist_ok=True)
    np.savez_compressed(f"{paths.TAPER_PROFILES}/{case}_{name}.npz", s=s, r=r, r_edt=r_edt, keep=keep,
                        touch=touch, junction_s=np.asarray(junction_s, float))
    return {"T_taper": T, "T_taper_edt": T_edt, "taper_mm_used": span, "taper_frac_used": frac}, reason


def score(split, with_taper=True):
    out_dir = paths.SCORES
    ids = [x.strip() for x in open(paths.FILELIST.format(split=split)) if x.strip()]
    os.makedirs(out_dir, exist_ok=True)
    columns = list(FEATURES) + (list(TAPER_COLUMNS) if with_taper else [])
    fails, n_rows, t0 = [], 0, time.time()
    with open(f"{out_dir}/{split}_vessels.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["case", "vessel"] + columns)
        for case in ids:
            try:
                vessels = load_vessels(case, with_junctions=True)
                if with_taper:
                    img = nib.load(paths.SEGMENTATION.format(case=case))
                    labels, affine = np.asarray(img.dataobj, dtype=np.uint8), img.affine
            except Exception as e:
                fails.append((case, "all", repr(e)))
                continue
            for name in ARTERIES:
                if name not in vessels:
                    fails.append((case, name, "missing"))
                    continue
                P, junction_s = vessels[name]
                row = {k: f(P) for k, f in FEATURES.items()}
                if row["length_mm"] < MIN_LENGTH_MM:
                    fails.append((case, name, f"shorter than {MIN_LENGTH_MM} mm"))
                    continue
                if with_taper:
                    try:
                        extra, reason = score_taper(case, name, P, junction_s, labels, affine)
                    except Exception as e:
                        extra, reason = dict.fromkeys(TAPER_COLUMNS, np.nan), repr(e)
                    row.update(extra)
                    if reason:
                        fails.append((case, name, f"taper: {reason}"))
                w.writerow([case, name] + [row[k] for k in columns])
                n_rows += 1
    with open(f"{out_dir}/{split}_failed.txt", "w") as fh:
        fh.writelines(f"{a}\t{b}\t{c}\n" for a, b, c in fails)
    print(f"{split}: {len(ids)} cases, {n_rows} vessels, {len(fails)} failures, {time.time() - t0:.0f} s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="train", choices=["train", "val", "test"])
    ap.add_argument("--skip-taper", action="store_true", help="centerline features only; no segmentation is read")
    a = ap.parse_args()
    score(a.split, with_taper=not a.skip_taper)
