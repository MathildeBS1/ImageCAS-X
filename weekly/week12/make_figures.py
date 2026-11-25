"""Crop the figure rows of the week 12 report: from asymmetry_view.png, bifurcation_view.png and curvature_view.png,
the worst difference (row 1) and the closest agreement (last row) of each. A figure not yet copied here is skipped.

    python weekly/week12/make_figures.py

Rows are found from the white bands of the images:
  asymmetry_view.png   a row starts at its topmost ink (the title of its diameter panel) after a white gap of
                       at least GAP px, and ends with its diameter panel (the right 30% of the width): the
                       next row's title sits above that row's left panels, inside the white band below.
  bifurcation_view.png a row ends with the "mm" labels under its two panels: a short ink run (under SHORT px)
                       that follows the panels after a gap of LABEL_GAP px. The next row starts at the first
                       ink after it (its title).
  curvature_view.png   one subfigure per row: rows are split at white gaps of at least ROW_GAP px (within a row
                       the gaps are at most about 35 px, between rows about 70).
The wide white space between panels is cut to KEEP px, so each row is printed larger.
It also copies the three method figures (curvature, angle, plane cut) from Thesis_coronary/content/methodology/figures.
"""
import shutil
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
FIGS = HERE.parents[1] / "CGPS_data" / "thesis_final"
METHOD = HERE.parents[1] / "Thesis_coronary" / "content" / "methodology" / "figures"
METHOD_FIGS = ("curvature_steps_figure.png", "angle_steps_figure.png", "surface_cut_figure.png")
GAP = 25  # px: white rows between two rows of asymmetry_view (within a row the gaps are at most about 20)
LABEL_GAP = (14, 20)  # px: white rows between the panels and their "mm" label in bifurcation_view
ROW_GAP = 50  # px: white rows between two rows of curvature_view
SHORT = 20  # px: an ink run lower than this is a line of text
PAD = 8  # px kept above and below a row
WIDE = 60  # px: a white column run wider than this lies between two panels
KEEP = 30  # px of it kept


def ink_runs(im):
    """(start, end) of the runs of image rows that hold ink."""
    ink = ~(im > 250).all(axis=1)
    runs, s = [], None
    for y, k in enumerate(ink):
        if k and s is None:
            s = y
        if not k and s is not None:
            runs.append((s, y))
            s = None
    return runs + ([(s, len(ink))] if s is not None else [])


def asymmetry_rows(im):
    """(top, bottom) of each row of asymmetry_view.png."""
    runs = ink_runs(im)
    starts = [runs[0][0]] + [b[0] for a, b in zip(runs, runs[1:]) if b[0] - a[1] >= GAP] + [im.shape[0]]
    rows = []
    for top, nxt in zip(starts, starts[1:]):
        right = np.flatnonzero(~(im[top:nxt, int(0.7 * im.shape[1]):] > 250).all(axis=1))  # diameter panel
        rows.append((top, top + right[-1] + 1))
    return rows


def angle_rows(im):
    """(top, bottom) of each row of bifurcation_view.png."""
    runs = ink_runs(im)
    ends = [b[1] for a, b in zip(runs, runs[1:])
            if LABEL_GAP[0] <= b[0] - a[1] <= LABEL_GAP[1] and b[1] - b[0] < SHORT]
    tops = [runs[0][0]] + [next(r[0] for r in runs if r[0] > e) for e in ends[:-1]]
    return list(zip(tops, ends))


def curvature_rows(im):
    """(top, bottom) of each row of curvature_view.png."""
    runs = ink_runs(im)
    cuts = [k for k, (a, b) in enumerate(zip(runs, runs[1:]), 1) if b[0] - a[1] >= ROW_GAP]
    return [(runs[i][0], runs[j - 1][1]) for i, j in zip([0] + cuts, cuts + [len(runs)])]


def keep_columns(band, gap=WIDE, keep=KEEP):
    """Columns to keep: white column runs wider than gap (the space between panels) shrink to keep px."""
    white = (band > 250).all(axis=0)
    out, x = np.ones(len(white), bool), 0
    while x < len(white):
        if white[x]:
            end = x
            while end < len(white) and white[end]:
                end += 1
            if end - x > gap:
                out[x + keep:end] = False
            x = end
        else:
            x += 1
    return out


def save(src, rows, names, worst=0):
    img = Image.open(src)
    rgb, im = np.asarray(img.convert("RGB")), np.asarray(img.convert("L"))
    for name, (top, bottom) in zip(names, (rows[worst], rows[-1])):
        lo, hi = max(top - PAD, 0), min(bottom + PAD, im.shape[0])
        Image.fromarray(rgb[lo:hi][:, keep_columns(im[lo:hi])]).save(HERE / "week12_figures" / name)
        print(f"{name}: rows {lo}-{hi} of {im.shape[0]} ({len(rows)} figure rows found in {src.name})")


def copy_method_figures():
    """Copy the method figures of the thesis (how each feature is computed, made-up shapes) next to the report."""
    for name in METHOD_FIGS:
        src = METHOD / name
        if not src.exists():
            print(f"{name}: not found, skipped")
            continue
        shutil.copyfile(src, HERE / "week12_figures" / name)
        print(f"{name}: copied")


def main():
    copy_method_figures()
    # the updated angle and asymmetry figures of 2026-11-19 ("(1)" copies); the second-worst row is shown (user)
    for src, finder, names, worst in (
            (FIGS / "asymmetry_view (1).png", asymmetry_rows, ("asym_bad.png", "asym_good.png"), 1),
            (FIGS / "bifurcation_view (1).png", angle_rows, ("angle_bad.png", "angle_good.png"), 1),
            (FIGS / "curvature_view (1).png", curvature_rows, ("curv_bad.png", "curv_good.png"), 1)):
        if not src.exists():
            print(f"{src.name}: not found, skipped")
            continue
        save(src, finder(np.asarray(Image.open(src).convert("L"))), names, worst)
    # the run before the full-artery rule (1,661 pairs): its worst row, a Medis fragment, shows how curvature goes wrong
    src = FIGS / "curvature_view.png"
    if src.exists():
        save(src, curvature_rows(np.asarray(Image.open(src).convert("L"))), ("curv_worst.png",), 0)


if __name__ == "__main__":
    main()
