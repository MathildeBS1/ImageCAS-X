"""Mean turning per segment: the curvature feature of the who model (sec:method-curvature, 06_curvature.tex).

    from turning_feature import segment_turning
    segment_turning(tree)  # {(artery, 0/1/2 for p/m/d): rad/mm or nan}

Each trunk of split_trunks.split is given the sliding-window turning profile of tortuosity.curvature
(profile_thesis): at every centerline point with a point CHORD mm (straight line) before and after it,
the turning angle between the two chords divided by CHORD, in rad/mm. No extra smoothing (smooth=0).
The profile is computed on the whole trunk and then cut at the segment boundaries, and each segment
gets the arc-length-weighted mean of its profile points (trapezoid rule over arc length), so densely
sampled stretches do not count more. Fewer than two profile points in a segment: nan.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # tortuosity/ in the repo root
from split_trunks import graph, split

try:
    from tortuosity.curvature import profile_thesis
except ImportError:  # flat copy on the server: curvature.py next to the shared modules
    from curvature import profile_thesis

CHORD = 5.0  # mm, sec:method-curvature


def mean_turning(pos, kappa, lo, hi):
    """Arc-length-weighted mean of the profile points with lo <= pos < hi, in rad/mm; nan below two points."""
    k = (pos >= lo) & (pos < hi)
    if k.sum() < 2:
        return np.nan
    p, t = pos[k], kappa[k]
    return ((t[1:] + t[:-1]) / 2 * np.diff(p)).sum() / (p[-1] - p[0])


def trunk_turning(Y, s, bounds, chord=CHORD):
    """Mean turning of each segment [lo, hi) of one trunk, bounds = (0, pm, md, end) in mm along it."""
    pos, kappa = profile_thesis(Y, chord, s)
    return [mean_turning(pos, kappa, lo, hi) for lo, hi in zip(bounds[:-1], bounds[1:])]


def segment_turning(tree, chord=CHORD):
    """{(artery, part): mean turning in rad/mm} for the trunk segments of one tree, part 0/1/2 = p/m/d."""
    out = {}
    for a, (pm, md, end, _, Y, s) in split(*graph(tree)).items():
        for part, T in enumerate(trunk_turning(Y, s, (0, pm, md, end), chord)):
            out[(a, part)] = T
    return out
