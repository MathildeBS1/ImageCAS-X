"""Build centerlines from masks with ``skeleton.py``, in the delivered file layout.

    python -m bifurcation.extract --fit-cap                                  # once, train split
    python -m bifurcation.extract --source cas_net_pretrained --split val --t 3
    python -m bifurcation.extract --source gt --split val --t 3 --oracle-ostia

``--source gt`` reads the delivered segmentations, anything else is a run under
``$ImageCAS_X_results_path`` with a ``predictions/`` folder. Ostia come from the TotalSegmentator heartchambers_highres
aorta (``jobs/totalseg_heart.sh``) within the cap fitted on train; ``--oracle-ostia`` uses the
delivered start points instead, for replication checks only, and says so in the output name.

Writes ``EXTRACTED/<source>_t<t>[_oracle]/<id>.coronary_{left,right}_centerline.vtk`` plus
``<id>.json`` per case and ``failed.json``.
"""

from __future__ import annotations

import argparse
import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import nibabel as nib
import numpy as np

from . import io, paths, skeleton

CAP_FILE = paths.EXTRACTED / "ostium_cap.json"


def _aorta(case_id: int) -> np.ndarray:
    img = nib.load(paths.totalseg_path(case_id, "aorta"))
    return skeleton.surface_points(np.asarray(img.dataobj), img.affine)


def fit_cap() -> None:
    """Distance from each delivered train start point to the TotalSegmentator aorta surface; the
    99th percentile becomes the ostium cap. Bransby used 5 mm with this same model, but Lee
    thinning retracts our tips by about a radius, so the cap is measured rather than assumed."""
    from scipy.spatial import cKDTree

    d, failed = [], []
    for case in paths.split_ids("train"):
        try:
            tree = cKDTree(_aorta(case))
            for cl in io.load_centerlines(case).values():
                d.extend(tree.query(cl.points[cl.start_points == 1])[0])
        except Exception as exc:
            failed.append((case, repr(exc)))
    d = np.asarray(d)
    out = {"cap_mm": float(np.percentile(d, 99)), "n_start_points": int(len(d)),
           "percentiles_mm": {p: float(np.percentile(d, p)) for p in (50, 90, 95, 99, 100)},
           "failed": failed}
    paths.EXTRACTED.mkdir(parents=True, exist_ok=True)
    CAP_FILE.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


def _one(case_id: int, source: str, split: str, out_dir: str, t: float, cap: float, oracle: bool):
    try:
        t0 = time.time()
        img = nib.load(paths.segmentation_path(case_id) if source == "gt"
                       else paths.prediction_path(source, case_id, split))
        mask = np.asarray(img.dataobj) > 0
        if oracle:
            aorta = np.concatenate([c.points[c.start_points == 1] for c in io.load_centerlines(case_id).values()])
        else:
            aorta = _aorta(case_id)
        cls, notes = skeleton.centerlines_from_mask(case_id, mask, img.affine, aorta, t, cap)
        for side, cl in cls.items():
            skeleton.write_centerline_vtk(cl, io.centerline_file(case_id, side, out_dir))
        notes.update(source=source, t=t, cap_mm=cap, oracle_ostia=oracle, seconds=round(time.time() - t0, 1))
        (Path(out_dir) / f"{case_id}.json").write_text(json.dumps(notes, indent=2) + "\n")
        return case_id, None
    except Exception as exc:  # reported per case, never swallowed
        return case_id, f"{type(exc).__name__}: {exc}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fit-cap", action="store_true", help="fit the ostium cap on train and exit")
    ap.add_argument("--source", default="cas_net_pretrained", help="'gt' or a run dir name")
    ap.add_argument("--split", default="val", choices=["train", "val", "test"])
    ap.add_argument("--t", type=float, default=3.0, help="bulge-size pruning threshold")
    ap.add_argument("--oracle-ostia", action="store_true")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--n", type=int, default=0, help="first N cases only (0 = all)")
    args = ap.parse_args()
    if args.fit_cap:
        return fit_cap()

    cap = 5.0 if args.oracle_ostia else json.loads(CAP_FILE.read_text())["cap_mm"]
    name = f"{args.source}_t{args.t:g}" + ("_oracle" if args.oracle_ostia else "")
    out_dir = paths.EXTRACTED / name
    out_dir.mkdir(parents=True, exist_ok=True)
    ids = paths.split_ids(args.split)[: args.n or None]
    todo = [c for c in ids if args.overwrite or not (out_dir / f"{c}.json").exists()]
    print(f"{len(ids)} {args.split} cases, {len(todo)} to build -> {out_dir} (cap {cap:.2f} mm)")

    t0, failed = time.time(), []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(_one, c, args.source, args.split, str(out_dir), args.t, cap, args.oracle_ostia) for c in todo]
        for fut in as_completed(futs):
            cid, err = fut.result()
            if err:
                failed.append((cid, err))
    print(f"done in {time.time() - t0:.0f}s; {len(failed)} failed")
    for cid, err in failed:
        print(f"  case {cid}: {err}")
    (out_dir / f"failed_{args.split}.json").write_text(json.dumps(failed, indent=2) + "\n")


if __name__ == "__main__":
    main()
