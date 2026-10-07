"""Bifurcation geometry from the ImageCAS-X centerlines and segmentations (objective 7).

``radius`` measures the lumen radius the centerlines do not carry; ``graph`` builds the rooted
vessel tree the junctions are found in; ``angles`` turns every splitting node into a row of
angles and caliber ratios. ``radius``, ``angles``, ``graph``, ``io`` and ``coords`` started as
``outdated_code/topology``; the first two were moved here, the rest copied, so nothing live
imports that frozen tree.
"""

from . import angles, coords, graph, io, paths, radius

__all__ = ["angles", "coords", "graph", "io", "paths", "radius"]
