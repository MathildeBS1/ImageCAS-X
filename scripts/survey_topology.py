#!/usr/bin/env python
"""Build every centerline into a rooted tree and validate the result.

The tree in ``topology.graph`` is what all topological features are computed on,
so it needs checking against something independent before it is trusted. The
dataset supplies exactly that: ``end_points`` and ``branch_points`` are per-point
flags produced by whoever built the centerlines, entirely separate from the line
connectivity this package reads. If the graph is right, the two must agree.

Also reports every side that is not one clean rooted tree, because those are the
cases downstream code has to reason about -- and most of them turn out to be
anatomy (absent left main) rather than bad data.

Usage:  python scripts/survey_topology.py [--n 800] [--out DIR]
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import time

import numpy as np

from topology import graph, io, paths


def check_side(centerline: io.Centerline, tree: graph.CoronaryTree) -> tuple[dict, list[str]]:
    """Cross-check one tree against the dataset's own topology flags."""
    failures: list[str] = []

    flagged_ends = {int(i) for i in np.flatnonzero(centerline.end_points)}
    flagged_branches = {int(i) for i in np.flatnonzero(centerline.branch_points)}
    # Ostia are flagged as end points too, so degree-1 nodes are termini plus roots.
    degree_one = {n.index for n in tree.nodes.values() if n.degree == 1}
    degree_many = {n.index for n in tree.nodes.values() if n.degree >= 3}

    if degree_one != flagged_ends:
        failures.append(f"degree-1 nodes != end_points (±{len(degree_one ^ flagged_ends)})")
    if degree_many != flagged_branches:
        failures.append(f"degree-3+ nodes != branch_points (±{len(degree_many ^ flagged_branches)})")
    if not set(np.flatnonzero(centerline.start_points)) <= flagged_ends:
        failures.append("start_points not a subset of end_points")

    # Every centerline point must land in the tree exactly once, junctions aside:
    # a dropped point is a silently lost piece of vessel.
    covered = collections.Counter()
    for seg in tree.segments:
        covered.update(int(i) for i in seg.point_indices)
    for chain in tree.chords:
        covered.update(int(i) for i in chain)
    missing = len(centerline.points) - len(covered)
    if missing:
        failures.append(f"{missing} centerline point(s) not covered by any segment")

    # Arc length must be conserved: the merge and orientation steps only relabel.
    raw = sum(
        float(np.linalg.norm(np.diff(centerline.points[line], axis=0), axis=1).sum())
        for line in centerline.lines
    )
    built = tree.total_length + sum(
        float(np.linalg.norm(np.diff(centerline.points[c], axis=0), axis=1).sum())
        for c in tree.chords
    )
    if raw > 0 and abs(built - raw) / raw > 1e-9:
        failures.append(f"length not conserved: {built:.3f} vs {raw:.3f} mm")

    generations = [s.generation for s in tree.segments]
    row = {
        "case_id": tree.case_id,
        "side": tree.side,
        "n_points": len(centerline.points),
        "n_segments": len(tree.segments),
        "n_nodes": len(tree.nodes),
        "n_roots": len(tree.roots),
        "n_bifurcations": len(tree.bifurcations()),
        "n_termini": len(tree.termini()),
        "n_chords": len(tree.chords),
        "max_generation": max(generations) if generations else -1,
        "total_length_mm": round(tree.total_length, 3),
        "arteries": "|".join(sorted({s.name for s in tree.segments if s.is_named})),
        "single_tree": tree.is_single_tree,
        "warnings": "; ".join(tree.warnings),
        "check_failures": "; ".join(failures),
    }
    return row, failures


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=0, help="limit to the first N cases (0 = all)")
    ap.add_argument("--out", default=None, help="output directory (default: derived tree on blackhole)")
    args = ap.parse_args()

    ids = paths.usable_ids()
    if args.n:
        ids = ids[: args.n]
    out_dir = paths.output_dir("topology_survey") if args.out is None else __import__("pathlib").Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    rows, failed_sides, errored = [], [], []
    for cid in ids:
        for side in ("left", "right"):
            try:
                c = io.load_centerline(cid, side)
                row, failures = check_side(c, graph.build_tree(c))
            except Exception as exc:  # a per-case failure must be reported, not swallowed
                errored.append((cid, side, f"{type(exc).__name__}: {exc}"))
                continue
            rows.append(row)
            if failures:
                failed_sides.append(row)

    csv_path = out_dir / "topology_survey.csv"
    with csv_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    n = len(rows)
    odd = [r for r in rows if not r["single_tree"]]
    summary = {
        "code_version": paths.code_version(),
        "n_cases": len(ids),
        "n_sides": n,
        "validation_failures": len(failed_sides),
        "load_errors": errored,
        "clean_single_trees": sum(r["single_tree"] for r in rows),
        "sides_with_multiple_roots": sum(r["n_roots"] > 1 for r in rows),
        "sides_with_cycles": sum(r["n_chords"] > 0 for r in rows),
        "anomalies": [
            {k: r[k] for k in ("case_id", "side", "n_roots", "n_chords", "arteries", "warnings")}
            for r in odd
        ],
    }
    (out_dir / "topology_survey.json").write_text(json.dumps(summary, indent=2) + "\n")

    print(f"{n} sides from {len(ids)} cases in {time.time() - t0:.1f}s  (code {summary['code_version']})")
    print(f"\nValidation against the dataset's own end_points / branch_points flags:")
    print(f"  sides passing every check : {n - len(failed_sides)}/{n}")
    for r in failed_sides[:20]:
        print(f"    case {r['case_id']:>5} {r['side']:<5} {r['check_failures']}")
    for cid, side, err in errored:
        print(f"    case {cid:>5} {side:<5} FAILED TO LOAD: {err}")

    print(f"\nStructure:")
    print(f"  single clean rooted tree  : {summary['clean_single_trees']}/{n}")
    print(f"  multiple ostia (forest)   : {summary['sides_with_multiple_roots']}")
    print(f"  cycle-closing edge dropped: {summary['sides_with_cycles']}")

    seg = np.array([r["n_segments"] for r in rows])
    bif = np.array([r["n_bifurcations"] for r in rows])
    gen = np.array([r["max_generation"] for r in rows])
    ln = np.array([r["total_length_mm"] for r in rows])
    print(f"\n{'':>26}{'median':>9}{'min':>8}{'max':>8}")
    for name, arr in (("segments per side", seg), ("bifurcations per side", bif),
                      ("max generation", gen), ("total length (mm)", ln)):
        print(f"  {name:<24}{np.median(arr):>9.1f}{arr.min():>8.0f}{arr.max():>8.0f}")

    # The absent-left-main variant: no LM label and two ostia should be the same sides.
    no_lm = {r["case_id"] for r in rows if r["side"] == "left" and "LM" not in r["arteries"].split("|")}
    two_ostia = {r["case_id"] for r in rows if r["side"] == "left" and r["n_roots"] > 1}
    print(f"\nLeft sides with no LM label : {len(no_lm)} {sorted(no_lm)}")
    print(f"Left sides with two ostia    : {len(two_ostia)} {sorted(two_ostia)}")
    print(f"  identical (absent left main, not a data defect): {no_lm == two_ostia}")
    if two_ostia - no_lm:
        print(f"  fragmented with an LM present (genuine defects): {sorted(two_ostia - no_lm)}")
    print(f"\nWrote {csv_path}\n      {out_dir / 'topology_survey.json'}")


if __name__ == "__main__":
    main()
