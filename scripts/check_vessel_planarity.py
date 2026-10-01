"""How planar are named coronary vessels, and how noisy is torsion relative to that
near-zero out-of-plane signal?

Read-only, login-node, CPU: runs topology.tortuosity.extract_case (default sigma=1mm
smoothing) over the test split's 160 cases and summarises the per-vessel planarity
fields (plane_d_rms_norm, plane_angle_mean_deg, non_planarity) against torsion_mean_abs.
Backs the numbers in reports/Vessel planarity and the case against torsion.md.
"""
from __future__ import annotations

import collections

import numpy as np

from topology import paths, tortuosity

FIELDS = ("plane_d_rms_norm", "plane_angle_mean_deg", "non_planarity", "torsion_mean_abs")


def main() -> None:
    ids = paths.split_ids("test")
    rows = []
    for cid in ids:
        try:
            rows.extend(tortuosity.extract_case(cid))
        except Exception as e:
            print(f"{cid}: FAILED {e}")

    by_name = collections.defaultdict(list)
    for r in rows:
        by_name[r.name].append(r)

    print(f"{len(ids)} cases, {len(rows)} vessel rows\n")
    header = f"{'vessel':6} {'n_ok':>5}" + "".join(f" {f + ' (med/mean)':>26}" for f in FIELDS)
    print(header)
    for name in ("LM", "LAD", "LCX", "RCA"):
        rs = [r for r in by_name[name] if r.reason is None]
        stats = []
        for f in FIELDS:
            vals = np.array([getattr(r, f) for r in rs])
            vals = vals[~np.isnan(vals)]
            stats.append((np.nan, np.nan) if len(vals) == 0 else (float(np.median(vals)), float(np.mean(vals))))
        line = f"{name:6} {len(rs):5d}" + "".join(f" {m:10.4f}/{a:<10.4f}" for m, a in stats)
        print(line)
        missing = [r.reason for r in by_name[name] if r.reason is not None]
        if missing:
            print(f"       {len(missing)} missing: {collections.Counter(missing)}")


if __name__ == "__main__":
    main()
