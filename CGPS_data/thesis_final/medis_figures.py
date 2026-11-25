"""One appendix figure per feature: the largest difference (a) above the closest agreement (b), so three files
leave the server for the examples (user, 2026-11-25: the Bland-Altman plots in Results sec:results-medis, the
examples in an appendix).

    python CGPS_data/thesis_final/medis_figures.py [--rows DIR]

Run after the three *_view.py --examples. Reads the six *_bad.png and *_good.png from the medis_compare folder
and writes examples_curvature.png, examples_angle.png and examples_asymmetry.png next to them. Each part keeps its
own size (all are 300 dpi), so the text has the size of the other thesis figures.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

DPI = 300
LABEL = 0.22  # inches above each part for its letter
FIGURES = {"examples_curvature.png": ("curvature_bad.png", "curvature_good.png"),
           "examples_angle.png": ("bifurcation_bad.png", "bifurcation_good.png"),
           "examples_asymmetry.png": ("asymmetry_bad.png", "asymmetry_good.png")}


def combine(paths, out):
    """Stack the PNGs at their own size, centred, each with its letter at the top left."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.image as mpimg
    from matplotlib.figure import Figure
    from medis_compare import thesis_rc
    thesis_rc()

    imgs = [mpimg.imread(p) for p in paths]
    sizes = [(im.shape[1] / DPI, im.shape[0] / DPI) for im in imgs]  # inches
    W = max(w for w, _ in sizes)
    H = sum(h + LABEL for _, h in sizes)
    fig = Figure(figsize=(W, H))
    top = H
    for i, (im, (w, h)) in enumerate(zip(imgs, sizes)):
        top -= LABEL
        left = (W - w) / 2
        ax = fig.add_axes((left / W, (top - h) / H, w / W, h / H))
        ax.imshow(im, interpolation="none")
        ax.axis("off")
        fig.text(left / W, (top + 0.04) / H, f"({'abc'[i]})", fontsize=10, ha="left", va="bottom")
        top -= h
    fig.savefig(out, dpi=DPI, facecolor="white")
    return out


def main():
    from cgps_stats import OUT_DIR
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rows", default=str(Path(OUT_DIR) / "medis_compare"), help="the medis_compare folder")
    rows = Path(ap.parse_args().rows)
    for name, parts in FIGURES.items():
        missing = [p for p in parts if not (rows / p).exists()]
        if missing:
            print(f"skipped {name}: missing {', '.join(missing)}")
            continue
        print(f"-> {combine([rows / p for p in parts], rows / name)}")


if __name__ == "__main__":
    main()
