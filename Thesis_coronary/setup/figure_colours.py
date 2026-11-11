"""One place for the colours of every scripted thesis figure.

Each figure script reads its colours from here, so switching scheme is one change and a rerun:

    python Thesis_coronary/make_figures.py                  # the ACTIVE scheme below
    python Thesis_coronary/make_figures.py --scheme original

or edit ACTIVE and rerun. THESIS_FIG_SCHEME in the environment overrides ACTIVE (make_figures.py sets it).

Roles, the same in every scheme:
    ink, ink2, muted, grid, surf   text, secondary text and ticks, background curves, grid and frames, background
    series                         three ordered colours: proximal/mid/distal, FPCA components 1-3,
                                   arriving and leaving chord (series[0], series[1])
    shadow                         the 2D projection in turning_angle_3d
    diverging                      colour stops of the covariance colour map (low, ..., high), or a matplotlib name
    fills                          light fills matching series (not used yet)
    palette                        the full categorical set, for figures with more than three groups

"caroline" is taken from the figures of Caroline Korsbæk Nørby's BA thesis (2025), sampled from the embedded
plots: the healthy/CCS yellow and pink with their light fills, the purple of the RNA-purity plot, and the
eight-colour donut of her Figure 3. Her yellow and pink are light, so thin lines on white are faint.
"original" is the scheme the figures had until 2026-11-10.
"""
import os

SCHEMES = {
    "original": dict(
        ink="#0b0b0b", ink2="#52514e", muted="#8a8984", grid="#dcdbd6", surf="white",
        series=("#2a78d6", "#eb6834", "#1baf7a"),
        shadow="#9a9994",
        diverging="RdBu_r",
        fills=("#c9dcf3", "#f8d2c1", "#bfe8d8"),
        palette=("#2a78d6", "#eb6834", "#1baf7a", "#8a5cc2", "#d6a12a", "#d4477e", "#3fa9b8", "#6b6a66"),
    ),
    "caroline": dict(
        ink="#0b0b0b", ink2="#52514e", muted="#8a8984", grid="#dcdbd6", surf="white",
        series=("#fab72c", "#f292b9", "#9c50cc"),  # yellow (healthy), pink (CCS), purple
        shadow="#9a9994",
        diverging=("#1e90ff", "#71a4cf", "white", "#f292b9", "#c71585"),
        fills=("#ffd76e", "#f9d0e0", "#dec5ee"),
        palette=("#fab72c", "#f292b9", "#00a676", "#9c50cc", "#71a4cf", "#6a0dad", "#c71585", "#1e90ff"),
    ),
}

ACTIVE = "caroline"

NAME = os.environ.get("THESIS_FIG_SCHEME", ACTIVE)
if NAME not in SCHEMES:
    raise SystemExit(f"unknown colour scheme {NAME!r}; choose from {', '.join(SCHEMES)}")
S = SCHEMES[NAME]

INK, INK2, MUTED, GRID, SURF = S["ink"], S["ink2"], S["muted"], S["grid"], S["surf"]
SERIES, SHADOW, FILLS, PALETTE = S["series"], S["shadow"], S["fills"], S["palette"]


def diverging_cmap():
    """The covariance colour map: a matplotlib name, or a map through the scheme's colour stops."""
    if isinstance(S["diverging"], str):
        return S["diverging"]
    from matplotlib.colors import LinearSegmentedColormap
    return LinearSegmentedColormap.from_list(f"{NAME}_diverging", S["diverging"])
