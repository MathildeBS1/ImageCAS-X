"""Prevalence of '>= 3 bends >= 45 deg' (Li 2011 / Zebic Mihic 2023 style) vs curvature floor.

A higher floor keeps only tight ("abrupt") bends: floor k means the vessel turns faster than
1/k mm radius of curvature inside the bend. Train split only.
"""
import numpy as np

import compute_simple as c

ids = open(f"{c.DATA}/filelist/train.txt").read().split()
FLOORS = (0.02, 0.05, 0.1)
res = {}
for cid in ids:
    g = {s: c.read(f"{c.DATA}/centerlines/{cid}.coronary_{s}_centerline.vtk") for s in ("left", "right")}
    for name in ("LAD", "LCX", "RCA"):
        lab, side = c.LABELS[name]
        pts, label, edges = g[side]
        m = (label[edges[:, 0]] == lab) & (label[edges[:, 1]] == lab)
        P = c.longest_path(pts, edges[m])
        S = c.resample(P)
        S2 = S @ c.basis(c.view_dir(*c.VIEWS[name]))
        for k in FLOORS:
            res.setdefault((name, k, "3D"), []).append((c.bends(S, k) >= 45).sum())
            res.setdefault((name, k, "2D"), []).append((c.bends(S2, k) >= 45).sum())
print("vessel floor dim  median_n45  frac>=3")
for (v, k, d), x in sorted(res.items()):
    x = np.array(x)
    print(f"{v:4s} {k:5.2f} {d}  {np.median(x):4.1f}  {np.mean(x >= 3):.3f}")
