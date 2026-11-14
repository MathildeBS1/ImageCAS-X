"""Figure for Section sec:method-ratio (fig:method-ratio): from lumen contours to the daughter asymmetry.

    python Thesis_coronary/content/methodology/figures/daughter_ratio_figure.py

A made-up left main bifurcation (no patient data) with unevenly spaced points and irregular lumen contours, run
through the real code of CGPS_data/thesis_final/daughter_ratio.py (contour_area, contour_diameter,
reference_diameter, lm_ratios). The lumen widens towards the bifurcation point O (the confluence) and the LAD
has one cross-section widened by a side-branch origin inside the window.
A, the left main, LAD and LCx with O and the stretch shaded on the LAD and LCx (5 to 10 mm from O); inset, one
LAD lumen contour with its equal-area circle and D = 2 sqrt(A / pi). B, the two daughter diameters as circles to
scale with the asymmetry and its number. Finet's ratio and the LM window removed 2026-11-13 (feature dropped).
Writes daughter_ratio_figure.{pdf,png} next to this file. Thesis style as curvature_figure.py: serif, white,
no title.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "CGPS_data" / "thesis_final"))
from daughter_ratio import DEPTHS, LM_OSTIUM, contour_area, contour_diameter, lm_ratios, reference_diameter  # noqa: E402

INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#dcdbd6", "white"
LUMEN = "#e4e3de"
COL = {"LM": "#52514e", "LAD": "#2a78d6", "LCx": "#eb6834"}
LO, HI = DEPTHS

plt.rcParams.update({"font.family": "serif", "font.serif": ["STIX Two Text", "STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix", "font.size": 8.5, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF})
rng = np.random.default_rng(3)


# ---------------------------------------------------------------- made-up bifurcation
def vessel(heading0, bend, length, diam):
    """Centerline from O (2D, z = 0) leaving at heading0 (rad) and turning by bend (rad/mm), with unevenly
    spaced points; diam(s) the nominal lumen diameter. Returns points (n, 3), arc length, tangents."""
    u = np.linspace(0, length, 4000)
    h = heading0 + bend * u
    dense = np.c_[np.r_[0, np.cumsum(np.cos(h[:-1]) * np.diff(u))], np.r_[0, np.cumsum(np.sin(h[:-1]) * np.diff(u))]]
    s = np.r_[0, np.cumsum(rng.uniform(0.4, 1.1, 200))]
    s = s[s <= length]
    Y = np.c_[np.interp(s, u, dense[:, 0]), np.interp(s, u, dense[:, 1]), np.zeros(len(s))]
    T = np.c_[np.cos(np.interp(s, u, h)), np.sin(np.interp(s, u, h)), np.zeros(len(s))]
    return Y, s, T, diam(s)


def ring(y, t, d, m=180):
    """Irregular closed lumen contour around y in the plane perpendicular to the tangent t, nominal diameter d."""
    e1 = np.cross(t, [0, 0, 1.0])
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(t, e1)
    a = np.linspace(0, 2 * np.pi, m, endpoint=False)
    ph = rng.uniform(0, 2 * np.pi, 2)
    r = d / 2 * (1 + 0.09 * np.cos(2 * a + ph[0]) + 0.04 * np.sin(3 * a + ph[1]))
    return y + r[:, None] * (np.cos(a)[:, None] * e1 + np.sin(a)[:, None] * e2), (e1, e2)


confluence = lambda s, w: w * np.exp(-s / 1.8)  # noqa: E731  widening towards O
V = {
    "LM": vessel(np.radians(160), 0.0, 13.0, lambda s: 3.45 + confluence(s, 1.0)),
    "LAD": vessel(np.radians(-25), -0.012, 26.0, lambda s: 3.0 - 0.015 * s + confluence(s, 1.2)),
    "LCx": vessel(np.radians(-110), 0.02, 22.0, lambda s: 2.55 - 0.015 * s + confluence(s, 1.0)),
}
s_lad = V["LAD"][1]
i_side = int(np.argmin(np.abs(s_lad - 7.2)))  # LAD cross-section widened by a side-branch origin
V["LAD"][3][i_side] *= 1.45

rings, D = {}, {}
for k, (Y, s, T, d) in V.items():
    rings[k] = [ring(y, t, dd) for y, t, dd in zip(Y, T, d)]
    D[k] = np.array([contour_diameter(r) for r, _ in rings[k]])  # the real code
L_LM = V["LM"][1][-1]  # the LM is built from O; the code measures it from the ostium
lm_from_ostium = (L_LM - V["LM"][1][::-1], D["LM"][::-1])
Dref = {k: reference_diameter(V[k][1], D[k]) for k in ("LAD", "LCx")}
Dref["LM"] = reference_diameter(*lm_from_ostium, *LM_OSTIUM)
feat = lm_ratios((V["LAD"][1], D["LAD"]), (V["LCx"][1], D["LCx"]), lm_from_ostium)
WIN = {"LAD": (LO, HI), "LCx": (LO, HI)}  # mm from O


def letter(ax, c):
    top = ax.get_subplotspec().get_position(ax.figure).y1
    ax.figure.text(0.015, top, c, fontsize=11, color=INK, va="top", ha="left")


def band(Y, s, T, d, m=None):
    """Polygon of the lumen drawn in the plane: the centerline offset by +-d/2 along the normal."""
    m = np.ones(len(s), bool) if m is None else m
    N = np.c_[-T[:, 1], T[:, 0]]
    P = Y[:, :2]
    up, dn = P + N * d[:, None] / 2, P - N * d[:, None] / 2
    return np.r_[up[m], dn[m][::-1]]


fig = plt.figure(figsize=(6.4, 5.4))
gs = fig.add_gridspec(2, 1, height_ratios=[1.30, 0.62], hspace=0.08, left=0.06, right=0.99, top=0.99, bottom=0.02)

# ---------------------------------------------------------------- A: vessels, O, windows, one contour
ax = fig.add_subplot(gs[0])
letter(ax, "A")
Ddraw = {k: v.copy() for k, v in D.items()}  # drawing only: the widened contour is shown as a side branch
Ddraw["LAD"][i_side] = (D["LAD"][i_side - 1] + D["LAD"][i_side + 1]) / 2
Yl, _, Tl, _ = V["LAD"]
nl = np.r_[-Tl[i_side, 1], Tl[i_side, 0], 0]
h = np.arctan2(*(-nl[:2] * 0.8 + Tl[i_side, :2])[::-1])
u = np.linspace(0, 7, 50)
stub = np.c_[Yl[i_side, 0] + u * np.cos(h), Yl[i_side, 1] + u * np.sin(h), 0 * u]
Ts = np.c_[np.cos(h) + 0 * u, np.sin(h) + 0 * u, 0 * u]
ax.fill(*band(stub, u, Ts, np.full(len(u), 1.6)).T, color=LUMEN, lw=0, zorder=1)
ax.add_patch(plt.Circle((0, 0), 2.3, color=LUMEN, lw=0, zorder=1))  # the confluence at O
for k, (Y, s, T, _) in V.items():
    ax.fill(*band(Y, s, T, Ddraw[k]).T, color=LUMEN, lw=0, zorder=1)
for k, (Y, s, T, _) in V.items():
    ax.plot(*Y[:, :2].T, color=INK, lw=0.9, zorder=3)
    ax.plot(*Y[:, :2].T, "o", color=SURF, mec=INK2, ms=1.8, mew=0.5, zorder=3)
    if k not in WIN:
        continue
    w = (s >= WIN[k][0]) & (s <= WIN[k][1])
    ax.fill(*band(Y, s, T, Ddraw[k], w).T, color=COL[k], alpha=0.30, lw=0, zorder=2)
    for d_ in WIN[k]:  # window ends, across the lumen
        j = int(np.argmin(np.abs(s - d_)))
        n = np.array([-T[j, 1], T[j, 0]])
        q = Y[j, :2]
        ax.plot(*np.c_[q - n * (D[k][j] / 2 + 0.5), q + n * (D[k][j] / 2 + 0.5)], color=COL[k], lw=0.9, zorder=4)
lab_pos = {"LM": (-6.5, 6.4), "LAD": tuple(V["LAD"][0][-1, :2] + [2.5, -1.0]), "LCx": (-1.0, -23.0)}
for k, xy in lab_pos.items():
    ax.text(*xy, f"{'left main' if k == 'LM' else k}", color=COL[k], fontsize=9, ha="center", va="center")
ax.plot(0, 0, "o", color=INK, ms=4.5, zorder=6)
Ym, sm, Tm, _ = V["LM"]
ax.text(*(Ym[-1, :2] + [-0.8, -2.6]), "ostium", fontsize=7.5, color=INK2, ha="right", va="center")
ax.text(1.2, 1.4, "$O$", fontsize=10, ha="left", va="bottom", zorder=6)
# depth labels on the LAD window ends
Y, s, T, _ = V["LAD"]
for d_, txt in ((LO, "5 mm"), (HI, "10 mm")):
    j = int(np.argmin(np.abs(s - d_)))
    n = np.array([-T[j, 1], T[j, 0]])
    ax.text(*(Y[j, :2] + n * (D["LAD"][j] / 2 + 1.6)), txt, fontsize=7.5, color=COL["LAD"], ha="center",
            va="bottom", rotation=np.degrees(np.arctan2(T[j, 1], T[j, 0])) + 0)
ax.annotate(f"side-branch origin: one cross-section\nwidened to {D['LAD'][i_side]:.2f} mm", stub[30, :2],
            xytext=(5.0, -19.5), fontsize=7.5, color=INK2, ha="left",
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
ax.annotate("lumen widens towards $O$", (-1.5, 1.6), xytext=(-21.0, -6.5), fontsize=7.5, color=INK2, ha="left",
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
# the contour shown in the inset
i_c = int(np.argmin(np.abs(s - 8.6)))
ax.plot(*Y[i_c, :2], "o", color=INK, ms=3.5, zorder=6)
ax.set(aspect="equal", xlim=(-24, 41), ylim=(-25, 9))
ax.axis("off")

ins = ax.inset_axes([0.66, 0.50, 0.33, 0.48])
(r, (e1, e2)) = rings["LAD"][i_c]
c = Y[i_c]
uv = np.c_[(r - c) @ e1, (r - c) @ e2]
A = contour_area(r)
Dc = contour_diameter(r)
ins.fill(*uv.T, color=COL["LAD"], alpha=0.18, lw=0)
ins.plot(*np.r_[uv, uv[:1]].T, color=COL["LAD"], lw=1.3)
t = np.linspace(0, 2 * np.pi, 300)
ins.plot(Dc / 2 * np.cos(t), Dc / 2 * np.sin(t), color=INK, lw=0.9, ls=(0, (3, 2)))
ins.plot([-Dc / 2, Dc / 2], [0, 0], color=INK, lw=0.8)
ins.text(0, 0.12, "$D$", fontsize=8.5, ha="center", va="bottom")
ins.text(0, -Dc / 2 - 0.35, f"$A$ = {A:.2f} mm$^2$\n$D = 2\\sqrt{{A/\\pi}}$ = {Dc:.2f} mm", fontsize=8,
         ha="center", va="top", linespacing=1.5)
ins.text(0, Dc / 2 + 0.3, f"LAD lumen contour at {s[i_c]:.1f} mm", fontsize=7.5, color=INK2, ha="center", va="bottom")
ins.set(aspect="equal", xlim=(-2.6, 2.6), ylim=(-3.6, 2.3))
ins.axis("off")
ax.annotate("", c[:2], xytext=(25.8, 3.0), arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6, ls=(0, (2, 2))))

# ---------------------------------------------------------------- B: diameters to scale and the two features
ax = fig.add_subplot(gs[1])
letter(ax, "B")
x = 0.0
top = max(Dref["LAD"], Dref["LCx"])
for k in ("LAD", "LCx"):
    d = Dref[k]
    x += d / 2
    ax.add_patch(plt.Circle((x, 0), d / 2, fc=COL[k], alpha=0.25, ec=COL[k], lw=1.3))
    ax.plot([x - d / 2, x + d / 2], [0, 0], color=COL[k], lw=0.9)
    name = k
    ax.text(x, -top / 2 - 0.35, f"{name}\n$D_{{\\mathrm{{{k}}}}}$ = {d:.2f} mm", ha="center", va="top", fontsize=8,
            color=COL[k], linespacing=1.4)
    x += d / 2 + 2.0
ax.text(x + 0.6, 0.0,
        r"asymmetry $= \ln\dfrac{D_{\mathrm{LCx}}}{D_{\mathrm{LAD}}}$"
        + f" = ln({Dref['LCx']:.2f} / {Dref['LAD']:.2f}) = {feat['asymmetry']:.3f}",
        fontsize=8.5, ha="left", va="center")
ax.text(0, top / 2 + 0.45, "median diameter over the shaded stretch, to scale", fontsize=7.5, color=INK2,
        ha="left", va="bottom")
ax.set(aspect="equal", xlim=(-0.3, x + 17.5), ylim=(-3.4, 2.6))
ax.axis("off")

out = Path(__file__).with_suffix("")
for ext in ("pdf", "png"):
    fig.savefig(f"{out}.{ext}", dpi=220)
print(f"wrote {out}.pdf/.png")
print("D", {k: round(v, 3) for k, v in Dref.items() if k != "LM"}, "asymmetry", round(feat["asymmetry"], 4))
print("widened LAD contour", round(D["LAD"][i_side], 2), "mm at", round(s_lad[i_side], 1), "mm")
