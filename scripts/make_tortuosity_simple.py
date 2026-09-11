"""Figure: three vessels, one tortuosity index (the simple version).

Three synthetic centerlines, each between end points 40 mm apart and each 50 mm
long, so all three have tau = L / D = 1.25. The six-panel version with
curvature colouring is make_tortuosity_ambiguity.py.

    uv run python scripts/make_tortuosity_simple.py

Writes figures/tortuosity_simple.{pdf,png}. Upload the PDF to
content/background/figures/ in Overleaf.
"""

import os

import matplotlib.pyplot as plt
import numpy as np

from make_tortuosity_ambiguity import CHORD_MM, INK, MUTED, OUT_DIR, TAU, build, bump, solve_amplitude

CURVE = "#2a78d6"
# (label, unit profile, height of this row's chord in mm)
ROWS = [
    ("one wide bend", lambda s: (np.sin(np.pi * s), 0 * s), 0.0),
    ("many small bends", lambda s: (np.sin(6 * np.pi * s), 0 * s), -10.0),
    ("one sharp bend,\nnear the start", lambda s: (bump(0.25, 0.11)(s), 0 * s), -27.0),
]


def main():
    plt.rcParams.update({"font.size": 9, "font.family": "sans-serif"})
    fig, ax = plt.subplots(figsize=(5.2, 3.6))

    for row, (label, profile, base) in enumerate(ROWS):
        points = build(profile, solve_amplitude(profile))
        ax.plot([0, CHORD_MM], [base, base], ls=(0, (3, 2)), lw=0.9, color=MUTED, zorder=1)
        ax.plot(points[:, 0], points[:, 1] + base, lw=2.2, color=CURVE,
                solid_capstyle="round", zorder=2)
        ax.plot(0, base, "o", ms=5, color=INK, zorder=3)
        ax.plot(CHORD_MM, base, "o", ms=5, mfc="white", mec=INK, mew=1.2, zorder=3)
        ax.text(CHORD_MM + 5, base + 1.2, label, ha="left", va="bottom", fontsize=8,
                color=INK, linespacing=1.2)
        ax.text(CHORD_MM + 5, base - 0.4, f"$\\tau = {TAU:.2f}$", ha="left", va="top",
                fontsize=9, color=INK)
        if row == 0:
            ax.text(0, base - 1.8, "start", ha="center", va="top", fontsize=7, color=MUTED)
            ax.text(CHORD_MM, base - 1.8, "end", ha="center", va="top", fontsize=7, color=MUTED)
            ax.text(CHORD_MM / 2, base - 1.2, "$D$", ha="center", va="top", fontsize=8,
                    color=MUTED)

    ax.text(CHORD_MM / 2 + 8, -31.5, f"all three: $L = {TAU * CHORD_MM:.0f}$ mm and "
            f"$D = {CHORD_MM:.0f}$ mm, so $\\tau = L/D = {TAU:.2f}$",
            ha="center", va="top", fontsize=8, color=INK)

    ax.set_xlim(-3, CHORD_MM + 24)
    ax.set_ylim(-35, 15)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

    os.makedirs(OUT_DIR, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT_DIR, f"tortuosity_simple.{ext}"), dpi=300)
    print("wrote figures/tortuosity_simple.{pdf,png}")


if __name__ == "__main__":
    main()
