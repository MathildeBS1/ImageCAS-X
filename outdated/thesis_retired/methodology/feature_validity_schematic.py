"""Schematic for Section sec:method-validity: a feature that groups people a little and varies a lot.

    python thesis/methodology/feature_validity_schematic.py

Two synthetic normal curves (no patient data): men and women differ by a small shift in the mean, and
each group keeps a large spread. The shift is the validity, the spread the individual information.
Writes feature_validity_schematic.pdf next to this file. Thesis style: serif, white, no title.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

MEN, WOMEN = "#2a78d6", "#eb6834"  # validated categorical pair (dataviz validator, light surface)
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#8a8984"
SHIFT, SD = 0.6, 1.0  # group difference of 0.6 SD: a clear but modest shift

plt.rcParams.update({"font.family": "serif", "font.serif": ["STIX Two Text", "STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix", "font.size": 9, "figure.facecolor": "white",
                     "axes.facecolor": "white", "savefig.facecolor": "white"})

x = np.linspace(-3.6, 4.2, 600)
pdf = lambda m: np.exp(-0.5 * ((x - m) / SD) ** 2) / (SD * np.sqrt(2 * np.pi))  # noqa: E731
fig, ax = plt.subplots(figsize=(5.6, 2.6))
for m, col, lab in ((0.0, MEN, "men"), (SHIFT, WOMEN, "women")):
    y = pdf(m)
    ax.fill_between(x, y, color=col, alpha=0.18, lw=0)
    ax.plot(x, y, color=col, lw=2)
    ax.plot([m, m], [0, y.max()], color=col, lw=1, ls=(0, (3, 2)))  # group mean
    xl = m - 1.7 if m == 0 else m + 1.7  # label on the outer shoulder of each curve
    ax.text(xl + (-0.1 if m == 0 else 0.1), pdf(m)[np.argmin(abs(x - xl))], lab, color=INK,
            ha="right" if m == 0 else "left", va="bottom")

top = pdf(0).max()
ax.annotate("", xy=(SHIFT, top * 1.08), xytext=(0, top * 1.08),
            arrowprops={"arrowstyle": "->", "color": INK, "lw": 1.2})
ax.text(SHIFT / 2, top * 1.14, "shift between the groups\n(validity)", ha="center", va="bottom", color=INK2,
        fontsize=8)
lo, hi = -1.96 * SD, 1.96 * SD  # central 95% of the men
ax.annotate("", xy=(lo, -0.035), xytext=(hi, -0.035),
            arrowprops={"arrowstyle": "<->", "color": INK, "lw": 1.2}, annotation_clip=False)
ax.text(0, -0.06, "spread within one group (individual information)", ha="center", va="top", color=INK2,
        fontsize=8)

ax.set_xlim(x[0], x[-1])
ax.set_ylim(-0.11, top * 1.42)
ax.set_yticks([])
ax.set_xticks([])
for s in ("left", "top", "right"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_position(("data", 0))
ax.spines["bottom"].set_color(MUTED)
ax.set_xlabel("geometric feature, e.g. curvature", color=INK2, labelpad=26)
fig.tight_layout()
fig.savefig(Path(__file__).with_suffix(".pdf"))
