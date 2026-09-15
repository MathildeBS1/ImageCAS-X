#!/usr/bin/env python
"""Resolve the segmentation label -> artery name mapping.

The centerlines carry both ``segment_label`` and ``segment_name``, and those labels
turn out to be the same integers used in the segmentation volumes. So the mapping
can be read straight off the centerlines and verified against the voxel data.

A single case is not enough: the variable labels (the ones that depend on an
individual's anatomy) only appear in some people, so this samples across cases
spanning all three dominance types.

Usage:  python scripts/derive_label_map.py [--n 30]
"""

from __future__ import annotations

import argparse
import collections
import json

import numpy as np

from topology import coords, io, paths


def sample_cases(n_per_dominance: int) -> list[int]:
    """Cases spanning R/L/Co dominance, so variant-dependent labels show up."""
    desc = paths.descriptors()
    usable = set(paths.usable_ids())
    out = []
    for dom in ("R", "L", "Co"):
        ids = [i for i in desc.index[desc["Dominance"] == dom] if i in usable]
        out.extend(sorted(ids)[:n_per_dominance])
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10, help="cases per dominance type")
    args = ap.parse_args()

    cases = sample_cases(args.n)
    print(f"Sampling {len(cases)} cases across R/L/Co dominance\n")

    names: dict[int, collections.Counter] = collections.defaultdict(collections.Counter)
    label_cases: dict[int, set[int]] = collections.defaultdict(set)
    dom_by_label: dict[int, collections.Counter] = collections.defaultdict(collections.Counter)
    checked = matched = 0
    desc = paths.descriptors()

    for cid in cases:
        seg = io.load_segmentation(cid)
        dom = desc.loc[cid, "Dominance"]
        for cl in io.load_centerlines(cid).values():
            for lbl in np.unique(cl.segment_label):
                sel = cl.segment_label == lbl
                names[int(lbl)].update(np.asarray(cl.segment_name)[sel].tolist())
                label_cases[int(lbl)].add(cid)
                dom_by_label[int(lbl)][dom] += 1

            # verify the centerline labels really are the voxel labels
            ijk = coords.lps_to_voxel(cl.points, seg.affine)
            ok = np.all((ijk >= 0) & (ijk < np.array(seg.labels.shape)), axis=1)
            vox = np.zeros(len(ijk), dtype=int)
            vox[ok] = seg.labels[ijk[ok, 0], ijk[ok, 1], ijk[ok, 2]]
            checked += len(vox)
            matched += int((vox == cl.segment_label).sum())

    print(f"Voxel/centerline label agreement: {matched}/{checked} = {matched / checked:.2%}\n")

    mapping = {}
    print(f"{'label':>5}  {'artery':<8} {'purity':>7}  {'cases':>5}  dominance of cases seen in")
    print("-" * 72)
    for lbl in sorted(names):
        cnt = names[lbl]
        name, hits = cnt.most_common(1)[0]
        purity = hits / sum(cnt.values())
        doms = ", ".join(f"{d}:{n}" for d, n in sorted(dom_by_label[lbl].items()))
        mapping[lbl] = name
        print(f"{lbl:>5}  {name:<8} {purity:>6.1%}  {len(label_cases[lbl]):>5}  {doms}")

    seg_labels = set()
    for cid in cases:
        seg_labels |= set(io.load_segmentation(cid).present_labels().tolist())
    missing = sorted(seg_labels - set(mapping))
    print(f"\nLabels in segmentations but not named by any centerline: {missing or 'none'}")

    out = paths.LABEL_MAP
    out.write_text(json.dumps({str(k): v for k, v in sorted(mapping.items())}, indent=2) + "\n")
    print(f"Wrote {out.relative_to(paths.REPO_ROOT)}")


if __name__ == "__main__":
    main()
