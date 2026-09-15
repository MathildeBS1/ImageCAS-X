#!/usr/bin/env python
"""Cache the per-point lumen radius of every delivered GT centerline.

The radius-aware bifurcation direction (graph.Segment.outgoing_direction) skips a core of one
local radius around each junction, and the delivered centerlines carry no radius, so it is
measured on the GT mask (topology/radius.py). One .npy per case and side under
$IMAGECASX_OUT/centerline_radius/, so an interrupted run loses nothing already done.

Usage:  python scripts/compute_centerline_radius.py [--workers 8] [--n N] [--overwrite]
"""

from __future__ import annotations

import argparse
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from topology import paths, radius


def _one(case_id: int) -> tuple[int, str | None]:
    try:
        radius.compute_gt_radius(case_id)
        return case_id, None
    except Exception as exc:  # reported per case, never swallowed
        return case_id, f"{type(exc).__name__}: {exc}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--n", type=int, default=0, help="first N cases only (0 = all)")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    ids = paths.usable_ids()[: args.n or None]
    todo = [c for c in ids if args.overwrite or not all(
        paths.radius_cache_path(c, s).exists() for s in ("left", "right"))]
    print(f"{len(ids)} cases, {len(ids) - len(todo)} already cached, {len(todo)} to do")

    t0, failed = time.time(), []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        for k, fut in enumerate(as_completed([ex.submit(_one, c) for c in todo]), 1):
            cid, err = fut.result()
            if err:
                failed.append((cid, err))
            if k % 50 == 0:
                print(f"  {k}/{len(todo)}  ({time.time() - t0:.0f}s)")
    print(f"done in {time.time() - t0:.0f}s; {len(failed)} failed")
    for cid, err in failed:
        print(f"  case {cid}: {err}")


if __name__ == "__main__":
    main()
