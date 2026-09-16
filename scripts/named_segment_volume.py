#!/usr/bin/env python
"""Total lumen volume and mean radius of each of the 13 named coronary arteries
(docs_thesis/label_map.json, labels 1-13; label 14 "Other" is a catch-all, not a vessel, and is
skipped), over the whole cohort.

Unlike scripts/bifurcation_volume.py, this is not read from a 3 mm window past a junction: every
point of every tree Segment carrying that name is used, over the segment's full length, so it is
the whole named artery's volume, not a local reading near one bifurcation. Volume is still the
same frustum sum (see bifurcation_volume.py's _branch_volume): consecutive centerline points
treated as a cone with the tip cut off, summed along the segment. Radius is the plain mean of
every point's measured radius (topology/radius.py) over that name's points.

A named artery can be cut into more than one tree Segment (e.g. the LAD split wherever a diagonal
branches off); every segment sharing a name in a tree is summed into that tree's one number for
that name, since Segment boundaries are the tree's own edges and never overlap.

Healthy vs. diseased uses ImageCAS-X's own per-case binary Disease label (Descriptors.xlsx),
the same label and the same test (Mann-Whitney U, Benjamini-Hochberg FDR across every
name x field test run together) as scripts/bifurcation_volume.py -- but the population here is
the whole named artery, not a 3 mm window past one bifurcation, so this is not a local reading
and the two are not directly comparable.

Usage:  python scripts/named_segment_volume.py [--n N]
"""

from __future__ import annotations

import argparse
import json

import numpy as np
from scipy import stats

from topology import graph, paths

LABEL_ORDER = ("LM", "LAD", "LCX", "D1", "D2", "OM1", "OM2", "IM",
               "RCA", "R-PDA", "R-PLA", "L-PDA", "L-PLA")


def _segment_volume(points: np.ndarray, radii: np.ndarray) -> float:
    ds = np.linalg.norm(np.diff(points, axis=0), axis=1)
    r0, r1 = radii[:-1], radii[1:]
    return float(np.sum((np.pi / 3.0) * ds * (r0**2 + r0 * r1 + r1**2)))


def _extract(ids) -> list[dict]:
    desc = paths.descriptors()
    rows = []
    for cid in ids:
        try:
            trees = graph.load_trees(cid)
        except Exception as exc:
            print(f"  case {cid} FAILED: {type(exc).__name__}: {exc}")
            continue
        disease = desc.loc[cid, "Disease"] if cid in desc.index else None
        disease = disease if isinstance(disease, str) else None
        for side, tree in trees.items():
            per_name: dict[str, list[int]] = {}
            for seg in tree.segments:
                if not seg.is_named or seg.radii is None:
                    continue
                per_name.setdefault(seg.name, []).append(seg.index)
            for name, seg_idxs in per_name.items():
                if name not in LABEL_ORDER:
                    continue
                volume = sum(_segment_volume(tree.segments[i].points, tree.segments[i].radii)
                             for i in seg_idxs)
                radii_all = np.concatenate([tree.segments[i].radii for i in seg_idxs])
                rows.append({"case_id": cid, "name": name, "disease": disease,
                             "volume": volume, "radius": float(radii_all.mean())})
    return rows


def _fdr(tests: list[dict]) -> None:
    ps = np.array([t["p"] for t in tests])
    order = np.argsort(ps)
    m = len(ps)
    q = np.empty(m)
    prev = 1.0
    for rank, idx in enumerate(order[::-1], start=1):
        i = m - rank + 1
        prev = min(prev, ps[idx] * m / i)
        q[idx] = prev
    for t, qv in zip(tests, q):
        t["q"] = float(qv)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=0, help="first N cases only (0 = all)")
    args = ap.parse_args()

    ids = paths.usable_ids()[: args.n or None]
    print(f"=== extracting named-artery volume and radius, {len(ids)} cases ===")
    rows = _extract(ids)

    print(f"\n{'artery':<8}{'n_h':>6}{'n_d':>6}{'vol healthy':>13}{'vol diseased':>15}"
          f"{'rad healthy':>13}{'rad diseased':>15}{'q(vol)':>9}{'q(rad)':>9}")
    entries, tests = [], []
    for name in LABEL_ORDER:
        h = [r for r in rows if r["name"] == name and r["disease"] == "no"]
        d = [r for r in rows if r["name"] == name and r["disease"] == "yes"]
        entry = {"name": name, "n_h": len(h), "n_d": len(d)}
        if len(h) >= 5 and len(d) >= 5:
            for field in ("volume", "radius"):
                vh = np.array([r[field] for r in h])
                vd = np.array([r[field] for r in d])
                _, p = stats.mannwhitneyu(vh, vd, alternative="two-sided")
                entry[f"{field}_h"] = float(vh.mean())
                entry[f"{field}_d"] = float(vd.mean())
                t = {"name": name, "field": field, "p": float(p)}
                entry[f"{field}_test"] = t
                tests.append(t)
        entries.append(entry)
    _fdr(tests)

    for entry in entries:
        if "volume_test" not in entry:
            print(f"{entry['name']:<8}{entry['n_h']:>6}{entry['n_d']:>6}  too few cases")
            continue
        qv, qr = entry["volume_test"]["q"], entry["radius_test"]["q"]
        print(f"{entry['name']:<8}{entry['n_h']:>6}{entry['n_d']:>6}"
              f"{entry['volume_h']:>13.2f}{entry['volume_d']:>15.2f}"
              f"{entry['radius_h']:>13.3f}{entry['radius_d']:>15.3f}"
              f"{qv:>9.3g}{'*' if qv < 0.05 else '':<1}{qr:>8.3g}{'*' if qr < 0.05 else '':<1}")

    out = paths.output_dir("named_segment_volume")
    (out / "summary.json").write_text(json.dumps(entries, indent=2) + "\n")
    print(f"\nWrote {out / 'summary.json'}")


if __name__ == "__main__":
    main()
