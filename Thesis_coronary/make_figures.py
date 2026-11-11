"""Regenerate every scripted thesis figure in one colour scheme (setup/figure_colours.py).

    python Thesis_coronary/make_figures.py                   # the ACTIVE scheme
    python Thesis_coronary/make_figures.py --scheme original
    python Thesis_coronary/make_figures.py --list

A new figure script joins by reading its colours from figure_colours and being added to SCRIPTS.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "setup"))
import figure_colours  # noqa: E402

SCRIPTS = (
    "content/methodology/figures/turning_angle_3d.py",
    "content/methodology/figures/turning_feature_schematic.py",
    "content/technical/figures/fpca_figures.py",
)

ap = argparse.ArgumentParser()
ap.add_argument("--scheme", default=figure_colours.ACTIVE, choices=sorted(figure_colours.SCHEMES))
ap.add_argument("--list", action="store_true", help="print the schemes and exit")
args = ap.parse_args()
if args.list:
    for name, s in figure_colours.SCHEMES.items():
        print(f"{name:10s}{' (active)' if name == figure_colours.ACTIVE else '':10s} series {', '.join(s['series'])}")
    sys.exit()

env = dict(os.environ, THESIS_FIG_SCHEME=args.scheme)
for script in SCRIPTS:
    print(f"[{args.scheme}] {script}")
    subprocess.run([sys.executable, str(HERE / script)], env=env, check=True)
