"""Run all four discovery scripts over a case, in order.

The information retrieval lives in one script per data type:

    scripts/discover_mask.py         <scan>.coronary.nii.gz         the annotation
    scripts/discover_surface.py      <scan>_surface.vtk             the mesh
    scripts/discover_centerline.py   <scan>_*_centerline.vtk        the graph
    scripts/discover_tortuosity.py   the same centerlines           the geometry

Shared loaders live in scripts/discover_common.py. Each of the four stands alone
and can be run directly; this just calls them in sequence.

    uv run python scripts/discover_data.py images/1
    uv run python scripts/discover_data.py images/1 --only centerline
"""

import argparse
import os
import subprocess
import sys

STAGES = ("mask", "surface", "centerline", "tortuosity")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case", nargs="+", help="case prefix, e.g. images/1")
    parser.add_argument("--only", choices=STAGES, action="append",
                        help="run just this stage (repeatable)")
    args = parser.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    failed = 0
    for stage in (args.only or STAGES):
        print(f"\n{'=' * 68}\n=== discover_{stage}\n{'=' * 68}")
        result = subprocess.run(
            [sys.executable, os.path.join(here, f"discover_{stage}.py"), *args.case])
        failed += result.returncode != 0
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
