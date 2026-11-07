"""Where the 541 progressed Medis patients progressed: a donut of the worsened segments, and a tree
with the 9 trunk segments in the same colours (LM and side branches grey).

    python CGPS_data/Medis_and_outcome/progression_pie.py

Counts are the aggregates from medis_match.md (dtu-gpu-7, 2026-10-29). The tree is only an anatomical
illustration (images/1, a local example tree, not a CGPS patient); its trunks are split into
proximal / mid / distal with the split_trunks.py rules: LAD at D1 and half the rest, LCx at OM1 and
OM2, RCA half way to the acute margin, the acute margin, then the end.
"""

from collections import defaultdict
from pathlib import Path

import heapq
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
COUNTS = {"pLAD": 268, "mLAD": 283, "dLAD": 174, "pCX": 234, "mCX": 116, "dCX": 51,
          "pRCA": 204, "mRCA": 233, "dRCA": 184, "LM and side branches": 729}
# one hue per artery, proximal darkest; LM and side branches neutral
COLORS = {"pLAD": "#174a8a", "mLAD": "#2a78d6", "dLAD": "#7fb0ec",
          "pCX": "#9c3a12", "mCX": "#eb6834", "dCX": "#f29a74",
          "pRCA": "#08603f", "mRCA": "#1baf7a", "dRCA": "#74cfa8",
          "LM and side branches": "#c9c8c3"}
INK, MUTED, SURFACE = "#0b0b0b", "#52514e", "#ffffff"


def load(side):
    m = pv.read(ROOT / "images" / f"1.coronary_{side}_centerline.vtk")
    nbr = defaultdict(list)
    for c in range(m.n_cells):
        ids = list(m.get_cell(c).point_ids)
        for a, b in zip(ids, ids[1:]):
            d = float(np.linalg.norm(m.points[a] - m.points[b]))
            nbr[a].append((b, d))
            nbr[b].append((a, d))
    return np.asarray(m.points), np.asarray(m.point_data["segment_name"]).astype(str), nbr


def path(nbr, src, dst):
    dist, prev, q = {src: 0.0}, {}, [(0.0, src)]
    while q:
        d, u = heapq.heappop(q)
        if u == dst:
            break
        for v, w in nbr[u]:
            if d + w < dist.get(v, np.inf):
                dist[v], prev[v] = d + w, u
                heapq.heappush(q, (d + w, v))
    out = [dst]
    while out[-1] != src:
        out.append(prev[out[-1]])
    return out[::-1]


def end_of(nbr, names, name):
    return next(p for p in nbr if len(nbr[p]) == 1 and names[p] == name)


def arc(P, idx):
    return np.r_[0, np.cumsum(np.linalg.norm(np.diff(P[idx], axis=0), axis=1))]


def origin(P, idx, names, branch):
    """Arc position on the trunk path where a side branch leaves (nearest trunk point)."""
    B = P[names == branch]
    return int(np.argmin(np.min(np.linalg.norm(P[idx][:, None] - B[None], axis=2), axis=1)))


def cut(s, *marks):
    return np.digitize(s, sorted(marks))  # 0 = proximal, 1 = mid, 2 = distal


def split_left(P, names, nbr):
    ost = end_of(nbr, names, "LM")
    color = {}
    for art, end, (b1, b2) in (("LAD", "LAD", ("D1", None)), ("CX", "LCX", ("OM1", "OM2"))):
        idx = [i for i in path(nbr, ost, end_of(nbr, names, end)) if names[i] != "LM"]
        s = arc(P, idx)
        k1 = s[origin(P, idx, names, b1)]
        k2 = s[origin(P, idx, names, b2)] if b2 else k1 + (s[-1] - k1) / 2
        for i, z in zip(idx, cut(s, k1, k2)):
            color[i] = "pmd"[z] + art
    return color


def split_right(P, names, nbr):
    tips = [p for p in nbr if len(nbr[p]) == 1 and names[p] == "RCA"]
    ost = tips[0]
    crux = max((p for p in nbr if len(nbr[p]) >= 3), key=lambda p: len(path(nbr, ost, p)))
    idx = path(nbr, ost, crux)
    s = arc(P, idx)
    a, b = P[idx[0]], P[idx[-1]]
    off = np.linalg.norm(np.cross(P[idx] - a, b - a), axis=1) / np.linalg.norm(b - a)
    am = s[int(np.argmax(off))]
    return {i: "pmd"[z] + "RCA" for i, z in zip(idx, cut(s, am / 2, am))}


LABEL_SHIFT = {"pLAD": (-9, 3), "mLAD": (9, 0), "dLAD": (9, 0), "pCX": (-4, -7), "mCX": (8, 0),
               "dCX": (-9, 0), "pRCA": (0, 7), "mRCA": (-9, 0), "dRCA": (0, 6)}


def draw_tree(ax):
    for side, splitter in (("left", split_left), ("right", split_right)):
        P, names, nbr = load(side)
        seg = splitter(P, names, nbr)
        done = set()
        for u in nbr:
            for v, _ in nbr[u]:
                if (v, u) in done:
                    continue
                done.add((u, v))
                key = seg.get(u) if seg.get(u) == seg.get(v) else None
                xy = P[[u, v]][:, [0, 2]]
                ax.plot(xy[:, 0], xy[:, 1], color=COLORS.get(key, COLORS["LM and side branches"]),
                        lw=4.5 if key else 2.5, solid_capstyle="round", zorder=3 if key else 2)
        for key in set(seg.values()):
            pts = [i for i in seg if seg[i] == key]
            x, y = P[pts[len(pts) // 2]][[0, 2]]
            dx, dy = LABEL_SHIFT[key]
            ax.text(x + dx, y + dy, key, fontsize=8.5, color=INK, ha="center", va="center")
    ax.text(0.02, 0.02, "grey: LM and side branches", transform=ax.transAxes, fontsize=8.5, color=MUTED)
    ax.set_aspect("equal")
    ax.axis("off")


def draw_donut(ax):
    total = sum(COUNTS.values())
    labels, vals = list(COUNTS), list(COUNTS.values())
    wedges, _ = ax.pie(vals, colors=[COLORS[k] for k in labels], startangle=90, counterclock=False,
                       wedgeprops={"width": 0.38, "edgecolor": SURFACE, "linewidth": 2})
    for w, k, v in zip(wedges, labels, vals):
        t = np.deg2rad((w.theta1 + w.theta2) / 2)
        x, y = np.cos(t), np.sin(t)
        ax.annotate(f"{k}  {100 * v / total:.1f}%", xy=(0.98 * x, 0.98 * y), xytext=(1.28 * x, 1.2 * y),
                    ha="left" if x >= 0 else "right", va="center", fontsize=9, color=INK,
                    arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.6})
    ax.text(0, 0.07, f"{total:,}", ha="center", va="center", fontsize=17, color=INK, weight="bold")
    ax.text(0, -0.13, "worsened\nsegments", ha="center", va="center", fontsize=8.5, color=MUTED)
    ax.set_aspect("equal")


def main():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5.2), gridspec_kw={"width_ratios": [1.25, 1]})
    fig.patch.set_facecolor(SURFACE)
    draw_donut(a1)
    draw_tree(a2)
    a1.set_title("Which segments worsened between baseline and follow-up", fontsize=11, color=INK, loc="left")
    a2.set_title("Colour key: the nine trunk segments", fontsize=11, color=INK, loc="left")
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(HERE / f"progression_pie.{ext}", dpi=200, facecolor=SURFACE)


if __name__ == "__main__":
    main()
