"""Figures for fpca_from_plots.tex: FPCA of the turning profile step by step, on made-up or Medis data.

    python3 thesis/week10/fpca_steps_figures.py                                    # made-up data, local
    python3 thesis/week10/fpca_steps_figures.py --data medis --segment plad [--src TREE_FOLDER] [--out DIR]

The FPCA, the scores and the K rules are the functions of CGPS_data/turning_profile_shapes.py
(pca, shape_count); the Medis profiles are built as there (build, matrices: sliding T5, 50 places).
K = the smallest of the Horn, bootstrap and block-CV counts, capped at the Riley maximum of the segment
(saved.md, C = 0.70). No outcome is loaded: the table and the weights b in p2 are made up.

--data medis runs on dtu-gpu-7 only. f4, f6 and p1 then draw individual people (25 profiles and one
person), so their output stays on the server; f9 is aggregate.
"""
import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "CGPS_data")]
import turning_profile_shapes as tps  # noqa: E402

INK, INK2, GRID, SURF, MUTED = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb", "#8a8984"
C = ("#2a78d6", "#eb6834", "#1baf7a", "#9b59b6", "#c9a227", "#16a2b8", "#d6336c", "#5c7cfa", "#8d6e63", "#2f9e44")
G = 50
g = (np.arange(G) + 0.5) / G
POS = "normalised position u (0 = proximal)"
KMAX_RILEY = {"plad": 10, "mlad": 8, "fake": 10}  # saved.md, C = 0.70
SEG_KEY = {"plad": ("LAD", 0), "mlad": ("LAD", 1)}
PRETTY = {"plad": "pLAD", "mlad": "mLAD", "fake": "made-up"}
B_EXAMPLE = (0.15, 0.10, 0.25)  # made-up weights b_k for p2


def style(ax, title=None, xlabel=None, ylabel=None):
    ax.set_facecolor(SURF)
    ax.grid(color=GRID, lw=0.6)
    ax.tick_params(colors=INK2, labelsize=8)
    for sp in ax.spines.values():
        sp.set_color(GRID)
    if title:
        ax.set_title(title, fontsize=9.5, color=INK, loc="left")
    if xlabel:
        ax.set_xlabel(xlabel, color=INK2, fontsize=8.5)
    if ylabel:
        ax.set_ylabel(ylabel, color=INK2, fontsize=8.5)


def save(fig, out, name):
    fig.tight_layout()
    fig.savefig(out / f"{name}.png", dpi=170, facecolor=SURF)
    plt.close(fig)


# ------------------------------------------------------------ data
def made_up():
    """The made-up group of fpca_explained_figures.py: 300 people, 3 true shapes, seed 4."""
    rng = np.random.default_rng(4)
    N, sd_true = 300, 0.006
    base = np.array([np.ones(G), np.cos(np.pi * g), np.cos(2 * np.pi * g)])
    avg_true = 0.03 + 0.025 * np.exp(-g / 0.12) + 0.01 * np.exp(-(1 - g) / 0.15)
    z_true = rng.normal(size=(N, 3)) * np.array([1.0, 0.7, 0.45])
    noise = np.array([np.convolve(rng.normal(0, 0.0025, G + 6), np.ones(7) / 7, "valid") for _ in range(N)])
    M = avg_true + sd_true * z_true @ (base / np.sqrt((base ** 2).mean(1, keepdims=True))) + noise
    return M, rng.choice(N, 25, replace=False)


def medis(src, segment):
    """The people x 50 matrix of one LAD segment from the Medis trees (as turning_profile_shapes.py)."""
    import hoe10y_qc as hq
    files = sorted(Path(src).rglob("*.vtk"))
    if not files:
        sys.exit(f"no .vtk trees under {src}: --data medis runs on dtu-gpu-7")
    hq.read_label_codes((f, f) for f in files)
    trees, _ = tps.build(files, tps.load_fn("medis"), 5.0)
    M = tps.matrices(trees, 5.0, G)[SEG_KEY[segment]][0]
    return M, np.random.default_rng(0).choice(len(M), min(25, len(M)), replace=False)


def choose_k(res, segment):
    """Smallest of the Horn, bootstrap and CV counts, capped at the Riley maximum."""
    return min(res["K"]["horn"], res["K"]["boot"], res["K"]["cv"], KMAX_RILEY[segment])


# ------------------------------------------------------------ figures
def f4(M, mean, show, out, who):
    D = M - mean
    fig, ax = plt.subplots(2, 1, figsize=(5.2, 4.6), facecolor=SURF, sharex=True)
    style(ax[0], f"Matrix M: profiles of {len(show)} of the {len(M)} {who} people, average $m$", None,
          "$T_5$ (rad/mm)")
    for r in show:
        ax[0].plot(g, M[r], color=MUTED, lw=0.8, alpha=0.7)
    ax[0].plot(g, mean, color=INK, lw=2.2, label="average $m_j$")
    ax[0].legend(frameon=False, fontsize=8)
    style(ax[1], "Matrix D = M − m: deviations (only these are used)", POS, "$D_{ij}$ (rad/mm)")
    for r in show:
        ax[1].plot(g, D[r], color=MUTED, lw=0.8, alpha=0.7)
    ax[1].axhline(0, color=INK, lw=1)
    save(fig, out, "f4_profiles_deviations")


def f6(M, mean, Vt, show, K, out):
    R = M - mean
    total = (R ** 2).sum()
    fig, ax = plt.subplots(K, 2, figsize=(5.4, 2.2 * K), facecolor=SURF, sharex=True, sharey=True, squeeze=False)
    for kk in range(K):
        c = R @ Vt[kk]
        sd = c.std()
        col = C[kk % len(C)]
        a = ax[kk, 0]
        style(a, rf"step {kk + 1}: unexplained, {(R ** 2).sum() / total:.0%}")
        for r in show:
            a.plot(g, R[r], color=MUTED, lw=0.7, alpha=0.7)
        a.plot(g, 2 * sd * Vt[kk], color=col, lw=2.2, label=rf"$\pm 2$SD$\cdot\varphi_{{{kk + 1}}}$")
        a.legend(frameon=False, fontsize=7, loc="upper right")
        a.plot(g, -2 * sd * Vt[kk], color=col, lw=2.2, ls="--")
        R = R - np.outer(c, Vt[kk])
        a = ax[kk, 1]
        style(a, rf"minus $c_{{i{kk + 1}}}\varphi_{{{kk + 1}}}$: {(R ** 2).sum() / total:.0%} left")
        for r in show:
            a.plot(g, R[r], color=col, lw=0.7, alpha=0.8)
    for a in ax[-1]:
        a.set_xlabel(POS, color=INK2, fontsize=8)
    save(fig, out, "f6_steps")


def f9(res, K, segment, out):
    kx = np.arange(1, res["kmax"] + 1)
    fig, ax = plt.subplots(1, 3, figsize=(10.5, 3.0), facecolor=SURF)
    style(ax[0], f"1. Horn: K = {res['K']['horn']}", "shape k", "share of the differences")
    ax[0].semilogy(kx, res["ev"][: res["kmax"]], "o-", color=INK, ms=3.5, label="data")
    ax[0].semilogy(kx, res["horn"][: res["kmax"]], "--", color=C[1], label="by chance (95th pct)")
    ax[0].legend(frameon=False, fontsize=7.5)
    style(ax[1], f"2. bootstrap: K = {res['K']['boot']}", "shape k", "median |cosine|")
    ax[1].bar(np.arange(1, len(res["stab"]) + 1), res["stab"], color=MUTED)
    ax[1].axhline(tps.STABLE, color=C[1], ls="--", lw=1.2, label="stable: 0.9")
    ax[1].legend(frameon=False, fontsize=7.5, loc="lower left")
    style(ax[2], f"3. block CV: K = {res['K']['cv']}", "number of shapes K", "prediction error / at K = 0")
    ax[2].plot(np.arange(len(res["cv"])), res["cv"], "o-", color=INK, ms=3)
    ax[2].axvline(res["K"]["cv"], color=C[1], ls="--", lw=1.2)
    for a in ax:
        a.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    fig.suptitle(f"K = smallest of the three, at most {KMAX_RILEY[segment]} (Riley) → K = {K}",
                 fontsize=10, color=INK)
    save(fig, out, "f9_k_choice")


def pick_person(z):
    """The person whose |z| is largest on a shape other than the first, with no shape near 0: a clear mix."""
    zk = z[:, : max(2, min(3, z.shape[1]))]
    ok = np.abs(zk).min(1) > 0.4
    score = np.abs(zk[:, 1:]).max(1) * ok
    return int(np.argmax(score)) if ok.any() else int(np.argmax(np.abs(zk).max(1)))


def p1(M, mean, Vt, sd, K, r, out):
    z = (M[r] - mean) @ Vt[:K].T / sd[:K]
    fit = mean + (z * sd[:K]) @ Vt[:K]
    fig, ax = plt.subplot_mosaic([["a", "a"], ["b", "c"]], figsize=(5.4, 5.2), facecolor=SURF,
                                 gridspec_kw=dict(width_ratios=[1.4, 1]))
    ax = [ax["a"], ax["b"], ax["c"]]
    style(ax[0], "one person's turning profile", POS, "$T_5$ (rad/mm)")
    ax[0].plot(g, mean, color=MUTED, lw=1.6, label="average person")
    ax[0].plot(g, M[r], color=INK, lw=1.4, label="this person")
    ax[0].plot(g, fit, color=C[1], lw=2, ls="--", label=rf"average + $\sum_{{k\leq{K}}}$ score$_k\cdot\varphi_k$")
    ax[0].legend(frameon=False, fontsize=7)
    style(ax[1], "the shapes (shared by all)", "u", r"weight $\varphi_k$")
    for kk in range(K):
        ax[1].plot(g, Vt[kk], color=C[kk % len(C)], lw=1.8, label=rf"$\varphi_{{{kk + 1}}}$")
    ax[1].axhline(0, color=INK2, lw=0.8)
    ax[1].legend(frameon=False, fontsize=6.5)
    style(ax[2], "this person's scores", None, "$z_{ik}$ (SD)")
    xx = np.arange(1, K + 1)
    ax[2].bar(xx, z, color=[C[kk % len(C)] for kk in range(K)])
    for x, v in zip(xx, z):
        ax[2].annotate(f"{v:+.1f}", (x, v), xytext=(0, 3 if v >= 0 else -10), textcoords="offset points",
                       ha="center", fontsize=8, color=INK)
    ax[2].axhline(0, color=INK2, lw=0.8)
    ax[2].set_xticks(xx, [rf"$\varphi_{{{k}}}$" for k in xx])
    lim = max(2.5, np.abs(z).max() + 0.6)
    ax[2].set_ylim(-lim, lim)
    save(fig, out, "p1_person_scores")
    return z


def p2(z_person, K, out):
    """Scores as columns of the model's data, and the person through the cloglog link. Made-up numbers."""
    rng = np.random.default_rng(1)
    Kt = min(K, 3)
    b = np.array(B_EXAMPLE[:Kt])
    a0, g0 = -2.6, 0.12  # made-up intercept and SCORE2 weight
    rows = [(4.1, z_person[:Kt])] + [(round(rng.uniform(1.5, 9), 1), rng.normal(size=Kt)) for _ in range(4)]
    fig = plt.figure(figsize=(5.4, 5.0), facecolor=SURF)
    axt = fig.add_axes([0.02, 0.56, 0.96, 0.38])
    axt.axis("off")
    cols = ["person", "SCORE2 (%)"] + [rf"$z_{{{k + 1}}}$" for k in range(Kt)] + ["plaque at FU"]
    cells = [["this person" if i == 0 else f"{i + 1}", f"{s:.1f}"] + [f"{v:+.1f}" for v in zz] + ["?"]
             for i, (s, zz) in enumerate(rows)]
    tab = axt.table(cellText=cells, colLabels=cols, loc="center", cellLoc="center")
    tab.auto_set_font_size(False)
    tab.set_fontsize(8.5)
    tab.scale(1, 1.5)
    for (i, j), cell in tab.get_celld().items():
        cell.set_edgecolor(GRID)
        cell.set_facecolor(SURF if i else "#efeeea")
        if 2 <= j < 2 + Kt and i:
            cell.set_text_props(color=C[(j - 2) % len(C)], weight="bold")
    axt.set_title("the scores are columns of the data", fontsize=9.5, color=INK, loc="left")
    axc = fig.add_axes([0.13, 0.09, 0.83, 0.38])
    eta = np.linspace(-5, 1.5, 200)
    style(axc, r"cloglog link: $p = 1 - \exp(-e^{\eta})$, made-up weights", r"$\eta = a + g\,$SCORE2 + $\sum b_k z_k$", "risk p")
    axc.plot(eta, 1 - np.exp(-np.exp(eta)), color=INK, lw=2)
    e0 = a0 + g0 * rows[0][0]
    e1 = e0 + b @ z_person[:Kt]
    for e, lab, col in ((e0, "SCORE2 only", MUTED), (e1, "+ shape scores", C[1])):
        axc.plot(e, 1 - np.exp(-np.exp(e)), "o", color=col, ms=7, label=f"{lab}: p = {1 - np.exp(-np.exp(e)):.2f}")
    axc.legend(frameon=False, fontsize=7, loc="upper left")
    fig.savefig(out / "p2_scores_to_model.png", dpi=170, facecolor=SURF)
    plt.close(fig)


def p3(M, mean, Vt, sd, K, r, out):
    """The story in one figure. Top: one person's curve = average + score x shape, as a visual sum.
    Bottom: the model's weights read back along the segment, beta(u) = sum_k (b_k / SD_k) phi_k(u),
    with the made-up b: where more turning goes with higher or lower risk."""
    Kt = min(K, 3)
    z = (M[r] - mean) @ Vt[:Kt].T / sd[:Kt]
    fig = plt.figure(figsize=(5.4, 4.6), facecolor=SURF)
    curves = [(M[r], INK, "this person"), (mean, MUTED, "average")] + \
             [(Vt[k], C[k], rf"$\varphi_{{{k + 1}}}$") for k in range(Kt)]
    ops = ["="] + [("+ " if v >= 0 else "− ") + f"{abs(v):.1f}" + r"$\,\times$" for v in z]
    n = len(curves)
    w, gap, x0 = 0.125, 0.085, 0.02
    for q, (y, col, lab) in enumerate(curves):
        x = x0 + q * (w + gap)
        a = fig.add_axes([x, 0.70, w, 0.19])
        a.plot(g, y, color=col, lw=1.6)
        if q >= 2:
            a.axhline(0, color=INK2, lw=0.5)
        a.set_xticks([])
        a.set_yticks([])
        a.set_facecolor(SURF)
        for sp in a.spines.values():
            sp.set_color(GRID)
        a.set_title(lab, fontsize=8.5, color=INK)
        if q:
            fig.text(x - gap / 2, 0.795, ops[q - 1], ha="center", va="center", fontsize=11 if q == 1 else 8.5,
                     color=C[q - 2] if q >= 2 else INK)
    fig.text(0.02, 0.965, "1. A person is described by K scores (the amounts of each shape)",
             fontsize=9.5, color=INK)
    beta = (np.array(B_EXAMPLE[:Kt]) / sd[:Kt]) @ Vt[:Kt]
    a = fig.add_axes([0.13, 0.10, 0.84, 0.36])
    style(a, None, POS, r"weight $\beta(u)$")
    fig.text(0.02, 0.585, r"2. Example only: the weight per place, $\beta(u)$, from made-up $b_k$",
             fontsize=9.5, color=INK)
    a.plot(g, beta, color=INK, lw=2)
    a.fill_between(g, beta, where=beta > 0, color=C[1], alpha=0.35, lw=0, label="above 0: more turning here, higher risk")
    a.fill_between(g, beta, where=beta < 0, color=C[0], alpha=0.35, lw=0, label="below 0: more turning here, lower risk")
    a.axhline(0, color=INK2, lw=0.8)
    a.legend(frameon=False, fontsize=7, loc="lower center")
    fig.text(0.02, 0.535, "Not yet known: the signs and sizes of $b_k$, and so which parts of each shape raise\n"
             "or lower the risk, come only from fitting the model.", fontsize=7.5, color=C[1], va="top")
    fig.savefig(out / "p3_story.png", dpi=170, facecolor=SURF)
    plt.close(fig)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", choices=("fake", "medis"), default="fake")
    ap.add_argument("--segment", choices=("plad", "mlad"), default="plad")
    ap.add_argument("--src", default="/data/kimbr/HØ_10Y/Medis/Analysis_Processed/centerline_tree")
    ap.add_argument("--out", default=None, help="default: week_figure/fpca_steps/fake locally; "
                    "/home/s254124/thesis/data_exploration/results/fpca_steps/<segment> for medis")
    ap.add_argument("--boot", type=int, default=200)
    ap.add_argument("--perm", type=int, default=200)
    args = ap.parse_args()

    if args.data == "fake":
        M, show = made_up()
        segment, who = "fake", "made-up"
        out = Path(args.out or Path(__file__).resolve().parent / "week_figure" / "fpca_steps" / "fake")
    else:
        M, show = medis(args.src, args.segment)
        segment, who = args.segment, f"Medis {PRETTY[args.segment]}"
        out = Path(args.out or f"/home/s254124/thesis/data_exploration/results/fpca_steps/{args.segment}")
    out.mkdir(parents=True, exist_ok=True)

    mean, ev, Vt = tps.pca(M)
    res = tps.shape_count(M, np.random.default_rng(0), argparse.Namespace(perm=args.perm, boot=args.boot))
    K = max(1, choose_k(res, segment))
    sd = ((M - mean) @ Vt.T).std(0)
    z = (M - mean) @ Vt[:K].T / sd[:K]

    f4(M, mean, show, out, who)
    f6(M, mean, Vt, show, K, out)
    f9(res, K, segment, out)
    r = pick_person(z)
    z_person = p1(M, mean, Vt, sd, K, r, out)
    p2(z_person, K, out)
    p3(M, mean, Vt, sd, K, r, out)
    print(f"{who}: n = {len(M)}, K counts {res['K']}, K = {K}; shares "
          + ", ".join(f"{100 * v:.1f}%" for v in ev[:5]))
    print("wrote", sorted(p.name for p in out.glob("*.png")), "to", out)


if __name__ == "__main__":
    main()
