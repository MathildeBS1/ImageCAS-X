"""Figure for the worked turning-angle example in thesis/week5/rca_tortuosity.tex.

Three centerline points (0,0,0), (4,3,0), (8,3,3) mm, spaced l = 5 mm. The vessel arrives
in the xy-plane and leaves through the xz-plane, turning 50.2 degrees; its shadow on the
xy-plane turns only 36.9 degrees, the part a 2D projection would see.

    uv run python scripts/make_turning_angle_3d.py

Writes figures/turning_angle_3d.{pdf,png}.
"""

import os

import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
INK, MUTED = "#1f2933", "#7b8794"
LOW, HIGH = "#e8590c", "#2a78d6"


def save(fig, name):
    os.makedirs(OUT_DIR, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT_DIR, f"{name}.{ext}"), dpi=300)
    plt.close(fig)
    print(f"wrote figures/{name}.{{pdf,png}}")


P = np.array([[0, 0, 0], [4, 3, 0], [8, 3, 3]], dtype=float)


def angle_deg(a, b):
    return np.degrees(np.arctan2(np.linalg.norm(np.cross(a, b)), a @ b))


def arc(ax, o, a, b, r, **kw):
    """Great-circle arc of radius r at o, from direction a to direction b."""
    u, v = a / np.linalg.norm(a), b / np.linalg.norm(b)
    th = np.arccos(np.clip(u @ v, -1, 1))
    t = np.linspace(0, 1, 40)[:, None]
    pts = o + r * (np.sin((1 - t) * th) * u + np.sin(t * th) * v) / np.sin(th)
    ax.plot(*pts.T, **kw)
    return pts[len(pts) // 2]


def main():
    a, b = P[1] - P[0], P[2] - P[1]
    b_xy = b * [1, 1, 0]
    theta, theta_xy = angle_deg(a, b), angle_deg(a, b_xy)

    fig = plt.figure(figsize=(5.2, 3.6))
    ax = fig.add_subplot(projection="3d")

    # Shadow on the xy-plane: where the third point projects and the angle a 2D view measures.
    ax.plot(*np.array([P[2], P[2] * [1, 1, 0]]).T, ls=":", lw=1.0, color=MUTED)
    ax.plot(*np.array([P[1], P[1] + b_xy]).T, ls="--", lw=1.2, color=MUTED)
    ax.scatter(*(P[2] * [1, 1, 0]), s=18, color=MUTED, depthshade=False)
    m = arc(ax, P[1], a, b_xy, 1.4, color=MUTED, lw=1.2)
    ax.text(*(m + [0.5, -0.9, 0]), f"{theta_xy:.1f}°\n(xy shadow)", color=MUTED, fontsize=8,
            ha="left", va="top")

    # Straight-on continuation of the arriving step, the reference the turn is measured from.
    ax.plot(*np.array([P[1], P[1] + 0.6 * a]).T, ls="--", lw=1.0, color=INK, alpha=0.6)

    # The two steps and the true 3D turn.
    for s, e, c, lab in ((P[0], P[1], HIGH, "$\\mathbf{a}_j = (4,3,0)$"),
                         (P[1], P[2], LOW, "$\\mathbf{b}_j = (4,0,3)$")):
        ax.quiver(*s, *(e - s), color=c, lw=2.2, arrow_length_ratio=0.07)
        ax.text(*((s + e) / 2 + [0, 0.4, 0.4]), lab, color=c, fontsize=9, ha="right")
    m = arc(ax, P[1], a, b, 2.0, color=LOW, lw=1.6)
    ax.text(*(m + [0.3, 0, 0.3]), f"$\\theta_j = {theta:.1f}^\\circ$", color=LOW, fontsize=10,
            weight="bold")

    ax.scatter(*P.T, s=28, color=INK, depthshade=False, zorder=5)
    for p, off in zip(P, ([0, -0.5, -0.6], [0, -0.5, -0.6], [0, 0, 0.35])):
        ax.text(*(p + off), f"({p[0]:g}, {p[1]:g}, {p[2]:g})", color=INK, fontsize=8,
                ha="center")

    ax.set_xlim(0, 9)
    ax.set_ylim(-1, 6)
    ax.set_zlim(0, 4)
    ax.set_box_aspect((9, 7, 4), zoom=1.15)
    ax.set_xlabel("x (mm)", fontsize=8)
    ax.set_ylabel("y (mm)", fontsize=8)
    ax.set_zlabel("z (mm)", fontsize=8)
    ax.tick_params(labelsize=7, colors=INK)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((1, 1, 1, 0))
    ax.view_init(elev=22, azim=-62)
    fig.subplots_adjust(left=-0.05, right=0.9, top=1.08, bottom=0.0)
    save(fig, "turning_angle_3d")


if __name__ == "__main__":
    plt.rcParams.update({"font.size": 9, "font.family": "sans-serif"})
    main()
