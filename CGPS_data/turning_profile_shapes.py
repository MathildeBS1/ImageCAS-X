"""How many distinct turning-profile shapes do the trunk segments and full trunks hold? Outcome-blind.

    python CGPS_data/turning_profile_shapes.py [--src TREE_FOLDER] [--trees medis|tracer] [--chord 5]
                                               [--seed 0] [--grid 50] [--boot 200] [--perm 200] [--out MD]

The turning profile is the sliding-window T5 (tortuosity.curvature.profile_thesis): the turning angle
over a 5 mm chord before and after every centerline point, in rad/mm, computed on the whole trunk and
then cut at the split_trunks boundaries. Each profile is put on --grid points of normalised position
(0 = its first, 1 = its last profile point) and an FPCA (SVD of the centred people x grid matrix) is run
per segment (9) and per full trunk (3). No visual read or outcome is loaded.

K, the number of shapes, by four rules with no cap from a parameter budget:
  var80 / var90  components needed for 80 % / 90 % of the variance;
  horn           leading components above the 95th percentile of the same component after permuting
                 people independently at each grid position (Horn's parallel analysis);
  shift          the same against each person's deviation from the mean profile shifted circularly by a
                 random amount. This keeps the smoothness the 5 mm window gives, which alone makes
                 neighbouring values correlate and inflates horn, and removes only the alignment across
                 people: K counts shapes tied to a position along the vessel (strict);
  boot           leading components whose shape returns in bootstrap resamples of people
                 (median |cosine| with the best-matching resampled component >= 0.9);
  cv             the K with the lowest 5-fold person-split prediction error, each held-out profile
                 predicted one fifth of the grid at a time from the other four fifths (a plain
                 reconstruction error only falls with K and cannot pick one).

Part A draws one random tree's RCA, LAD and LCx profile (sliding T5 as a line, the vertex T5 of
progression_turning.profile as dots). That figure shows one person's anatomy: the ID is printed to the
terminal only, never put in the image or its file name; check with Kit before it leaves the server.
Everything else is aggregate (counts 1-4 hidden). Runs on dtu-gpu-7. The tracer trees are read with
thesis_final/split_check.tracer_tree, which is not written yet; until then this runs on the Medis trees,
whose people had plaque at baseline.
"""
import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import hoe10y_qc as hq
from cgps_stats import OUT_DIR, QUARTILE_MIN, count, describe
from progression_turning import profile as vertex_profile
from split_trunks import NAMES, graph, split

try:
    from tortuosity.curvature import profile_thesis
except ImportError:  # flat copy on the server: curvature.py next to this file
    from curvature import profile_thesis

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e4e3df"
COLORS = ("#2a78d6", "#eb6834", "#1baf7a")  # p / m / d, as in split_example_figure.py
ARTERIES = ("LAD", "CX", "RCA")
PRETTY = {"LAD": "LAD", "CX": "LCx", "RCA": "RCA"}
KMAX = 15
STABLE = 0.9
MIN_PTS = 5
RULES = ("var80", "var90", "horn", "shift", "boot", "cv")


# ---------------------------------------------------------------- profiles
def load_fn(kind):
    if kind == "medis":
        return hq.tree_points
    sys.path.insert(0, str(Path(__file__).resolve().parent / "thesis_final"))
    from split_check import tracer_tree
    return tracer_tree


def build(files, load, chord):
    """[(file, {artery: (pm, md, end, Y, s, pos, T)})] for every tree that splits."""
    trees, skipped = [], 0
    for f in files:
        try:
            res = split(*graph(load(f)))
        except Exception:  # noqa: BLE001 - tree skipped, counted
            skipped += 1
            continue
        arts = {}
        for a, (pm, md, end, _, Y, s) in res.items():
            pos, T = profile_thesis(Y, chord, s)
            arts[a] = (pm, md, end, Y, s, pos, T)
        if arts:
            trees.append((f, arts))
    return trees, skipped


def on_grid(pos, T, lo, hi, n_grid):
    """The profile inside [lo, hi) on n_grid points of normalised position, or None if too few points."""
    k = (pos >= lo) & (pos < hi)
    if k.sum() < MIN_PTS:
        return None
    p, t = pos[k], T[k]
    g = (np.arange(n_grid) + 0.5) / n_grid
    return np.interp(g, (p - p[0]) / (p[-1] - p[0]), t)


def matrices(trees, chord, n_grid):
    """{(artery, part): (people x grid matrix, lengths)}, part = 0/1/2 for p/m/d and 'full'."""
    rows = {}
    for _, arts in trees:
        for a, (pm, md, end, _, _, pos, T) in arts.items():
            for part, (lo, hi) in enumerate(zip((0, pm, md), (pm, md, end))):
                if hi - lo >= 2 * chord and (x := on_grid(pos, T, lo, hi, n_grid)) is not None:
                    rows.setdefault((a, part), []).append((x, hi - lo))
            if end >= 4 * chord and (x := on_grid(pos, T, 0, np.inf, n_grid)) is not None:
                rows.setdefault((a, "full"), []).append((x, end))
    return {k: (np.array([x for x, _ in v]), np.array([L for _, L in v])) for k, v in rows.items()}


# ---------------------------------------------------------------- shape count
def pca(M):
    mean = M.mean(0)
    _, S, Vt = np.linalg.svd(M - mean, full_matrices=False)
    Vt *= np.where(Vt.sum(1) < 0, -1, 1)[:, None]  # fixed sign: each shape sums to >= 0
    return mean, S ** 2 / (S ** 2).sum(), Vt


def leading(ok):
    """Number of leading True values."""
    return int(np.argmin(np.r_[ok, False]))


def null_ev(M, rng, n_perm, how):
    out = []
    for _ in range(n_perm):
        if how == "horn":
            Mp = rng.permuted(M, axis=0)
        else:
            idx = (np.arange(M.shape[1])[None] + rng.integers(0, M.shape[1], len(M))[:, None]) % M.shape[1]
            Mp = np.take_along_axis(M - M.mean(0), idx, axis=1)  # deviations from the mean, so the shift
            # does not turn the mean shape itself into variation between people
        out.append(pca(Mp)[1])
    return np.quantile(out, 0.95, axis=0)


def cv_error(M, rng, kmax, folds=5):
    """Prediction error per K = 0..kmax for held-out people: each fifth of the grid, a contiguous block,
    predicted from the other four (interleaved points would be predictable from smoothness alone)."""
    fold = rng.permutation(len(M)) % folds
    err = np.zeros(kmax + 1)
    block = np.arange(M.shape[1]) * 5 // M.shape[1]
    splits = [(block != b, block == b) for b in range(5)]
    for f in range(folds):
        mean, _, Vt = pca(M[fold != f])
        X = M[fold == f] - mean
        for k in range(kmax + 1):
            for seen, hid in splits:
                if k == 0:
                    err[k] += (X[:, hid] ** 2).sum()
                    continue
                sc = np.linalg.lstsq(Vt[:k, seen].T, X[:, seen].T, rcond=None)[0]
                err[k] += ((X[:, hid] - (Vt[:k, hid].T @ sc).T) ** 2).sum()
    return err / err[0]


def shape_count(M, rng, args):
    mean, ev, Vt = pca(M)
    kmax = min(KMAX, len(ev) - 1, len(M) - 2)
    horn, shift = null_ev(M, rng, args.perm, "horn"), null_ev(M, rng, args.perm, "shift")
    match = np.zeros((args.boot, kmax))
    for b in range(args.boot):
        Vb = pca(M[rng.integers(0, len(M), len(M))])[2][: kmax + 3]
        match[b] = np.abs(Vt[:kmax] @ Vb.T).max(1)
    stab = np.median(match, 0)
    cv = cv_error(M, rng, kmax)
    cum = np.cumsum(ev)
    K = {"var80": int(np.searchsorted(cum, 0.8) + 1), "var90": int(np.searchsorted(cum, 0.9) + 1),
         "horn": leading(ev > horn), "shift": leading(ev > shift),
         "boot": leading(stab >= STABLE), "cv": int(np.argmin(cv))}
    scores = (M - mean) @ Vt[:3].T
    return {"n": len(M), "ev": ev, "horn": horn, "shift": shift, "stab": stab, "cv": cv, "K": K,
            "mean": mean, "phi": Vt[:3], "sd": scores.std(0), "kmax": kmax}


# ---------------------------------------------------------------- figures
def style(ax):
    ax.set_facecolor(SURF)
    ax.grid(color=GRID, lw=0.6)
    ax.tick_params(colors=INK2, labelsize=8)
    for sp in ax.spines.values():
        sp.set_color(GRID)


def example_figure(trees, chord, rng, out):
    full = [t for t in trees if all(a in t[1] for a in ARTERIES)]
    if not full:
        print("example: no tree with all three trunks")
        return
    f, arts = full[rng.integers(len(full))]
    print(f"example tree (do not share): {hq.id_from_name(f.name)}")
    fig, axes = plt.subplots(3, 1, figsize=(8, 7.5), facecolor=SURF)
    for ax, a in zip(axes, ("RCA", "LAD", "CX")):
        pm, md, end, Y, s, pos, T = arts[a]
        for c, lo, hi, seg in zip(COLORS, (0, pm, md), (pm, md, end), NAMES[a]):
            ax.axvspan(lo, hi, color=c, alpha=0.10, lw=0)
            ax.text((lo + hi) / 2, 0.97, seg.replace(a.lower(), PRETTY[a]), transform=ax.get_xaxis_transform(),
                    ha="center", va="top", fontsize=8, color=c)
        vp, vT = vertex_profile(Y, s, chord)
        ax.plot(pos, T, color=INK, lw=1.2, label=f"sliding T{chord:g} (every point)")
        ax.plot(vp, vT, "o", ms=3.5, color=COLORS[1], label=f"vertex T{chord:g} (every {chord:g} mm)")
        style(ax)
        ax.set_xlim(0, end)
        ax.set_ylabel(f"{PRETTY[a]}\nT{chord:g} (rad/mm)", color=INK2, fontsize=9)
    axes[0].legend(frameon=False, fontsize=8, loc="upper right", bbox_to_anchor=(1, 0.88))
    axes[-1].set_xlabel("mm along the trunk (RCA: ostium; LAD, LCx: LM bifurcation)", color=INK2, fontsize=9)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(out / f"turning_profile_example.{ext}", dpi=200)
    plt.close(fig)


def grid_axes():
    fig, axes = plt.subplots(3, 4, figsize=(13, 8.5), facecolor=SURF, sharex="col")
    keys = [[(a, part) for part in (0, 1, 2, "full")] for a in ARTERIES]
    return fig, axes, keys


def title(a, part):
    return f"full {PRETTY[a]}" if part == "full" else NAMES[a][part].replace(a.lower(), PRETTY[a])


def scree_figure(res, out):
    fig, axes, keys = grid_axes()
    for ax_row, key_row in zip(axes, keys):
        for ax, key in zip(ax_row, key_row):
            style(ax)
            if key not in res:
                ax.set_title(f"{title(*key)}: too few", fontsize=9, color=MUTED)
                continue
            r = res[key]
            k = np.arange(1, r["kmax"] + 1)
            ax.semilogy(k, r["ev"][: r["kmax"]], "o-", color=INK, ms=3, lw=1, label="data")
            ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
            ax.semilogy(k, r["horn"][: r["kmax"]], "--", color=COLORS[1], lw=1, label="horn null 95%")
            ax.semilogy(k, r["shift"][: r["kmax"]], "--", color=COLORS[0], lw=1, label="shift null 95%")
            K = r["K"]
            ax.set_title(f"{title(*key)} (n={count(r['n'])})\nK: horn {K['horn']}, shift {K['shift']}, "
                         f"boot {K['boot']}, cv {K['cv']}", fontsize=8.5, color=INK)
    axes[0, 0].legend(frameon=False, fontsize=7)
    for ax in axes[-1]:
        ax.set_xlabel("component", color=INK2, fontsize=9)
    for ax in axes[:, 0]:
        ax.set_ylabel("share of variance", color=INK2, fontsize=9)
    fig.tight_layout()
    fig.savefig(out / "turning_profile_shapes_scree.png", dpi=200)
    plt.close(fig)


def phi_figure(res, out):
    """One figure per artery: rows φ1-φ3, columns p / m / d / full trunk; each panel the mean profile and
    the mean ± 2 SD of that one component."""
    for a in ARTERIES:
        fig, axes = plt.subplots(3, 4, figsize=(13, 8), facecolor=SURF, sharex=True)
        for j, part in enumerate((0, 1, 2, "full")):
            key = (a, part)
            for i, ax in enumerate(axes[:, j]):
                style(ax)
                if key not in res or res[key]["n"] < QUARTILE_MIN:
                    ax.set_title(f"{title(*key)}: too few", fontsize=9, color=MUTED)
                    continue
                r = res[key]
                g = (np.arange(len(r["mean"])) + 0.5) / len(r["mean"])
                c, d = COLORS[i], 2 * r["sd"][i] * r["phi"][i]
                ax.plot(g, r["mean"], color=INK, lw=1.4, label="mean")
                ax.plot(g, r["mean"] + d, color=c, lw=1.2, label="high score (+2 SD)")
                ax.plot(g, r["mean"] - d, color=c, lw=1.2, ls="--", label="low score (−2 SD)")
                ax.set_title(f"{title(*key)}  φ{i + 1}: {100 * r['ev'][i]:.0f}% of variance", fontsize=9,
                             color=INK)
                if j == 0:
                    ax.legend(frameon=False, fontsize=7, loc="upper right")
        for ax in axes[-1]:
            ax.set_xlabel("normalised position (0 = proximal)", color=INK2, fontsize=9)
        for i, ax in enumerate(axes[:, 0]):
            ax.set_ylabel(f"φ{i + 1}\nT5 (rad/mm)", color=INK2, fontsize=9)
        fig.suptitle(f"{PRETTY[a]}: what a high and a low score on each component look like", color=INK)
        fig.tight_layout()
        fig.savefig(out / f"turning_profile_shapes_phi_{PRETTY[a].lower()}.png", dpi=200)
        plt.close(fig)


# ---------------------------------------------------------------- report
def table(res, keys):
    L = ["| profile | n | median length (mm) | " + " | ".join(f"K {r}" for r in RULES)
         + " | var φ1 | φ2 | φ3 | φ4 | φ5 |",
         "|" + "---|" * (3 + len(RULES) + 5)]
    for key in keys:
        if key not in res:
            L.append(f"| {title(*key)} | too few |" + " |" * (len(RULES) + 6))
            continue
        r = res[key]
        med = describe(pd.Series(r["lengths"])).get("median")
        L.append(f"| {title(*key)} | {count(r['n'])} | {'' if med is None else f'{med:.0f}'} | "
                 + " | ".join(str(r["K"][x]) for x in RULES) + " | "
                 + " | ".join(f"{100 * v:.1f}%" for v in r["ev"][:5]) + " |")
    return L


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"))
    ap.add_argument("--trees", choices=("medis", "tracer"), default="medis")
    ap.add_argument("--chord", type=float, default=5.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--grid", type=int, default=50)
    ap.add_argument("--boot", type=int, default=200)
    ap.add_argument("--perm", type=int, default=200)
    ap.add_argument("--out", default=str(Path(OUT_DIR) / "turning_profile_shapes.md"))
    args = ap.parse_args()
    out = Path(args.out).parent
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)

    files = sorted(Path(args.src).rglob("*.vtk"))
    if args.trees == "medis":
        hq.read_label_codes((f, f) for f in files)  # names for codes a file leaves unnamed
    trees, skipped = build(files, load_fn(args.trees), args.chord)
    example_figure(trees, args.chord, rng, out)

    res = {}
    for key, (M, lengths) in matrices(trees, args.chord, args.grid).items():
        if len(M) >= QUARTILE_MIN:
            res[key] = {**shape_count(M, rng, args), "lengths": lengths}
    scree_figure(res, out)
    phi_figure(res, out)

    seg_keys = [(a, p) for a in ARTERIES for p in (0, 1, 2)]
    rep = ["# Turning-profile shapes per segment and per trunk\n",
           f"{args.trees} trees: {count(len(files))} files, {count(len(trees))} split, {count(skipped)} not readable. "
           f"Sliding T{args.chord:g} at every centerline point, {args.grid} grid points of normalised position, "
           f"{args.perm} permutations per null, {args.boot} bootstrap resamples, seed {args.seed}. "
           f"Segments need >= {2 * args.chord:g} mm and >= {MIN_PTS} profile points, full trunks >= "
           f"{4 * args.chord:g} mm. K is capped at {KMAX} only by the search, not by a parameter budget. "
           "No outcome or visual read is used.\n",
           "## Segments\n", *table(res, seg_keys), "",
           "## Full trunks\n", *table(res, [(a, "full") for a in ARTERIES]), "",
           "Figures: turning_profile_shapes_scree.png (variance per component against both nulls), "
           "turning_profile_shapes_phi_{lad,lcx,rca}.png (per artery: mean profile ± 2 SD of φ1–φ3, one "
           "component per row). turning_profile_example.{png,pdf} "
           "shows one person's trunks and is not to leave the server unchecked.\n"]
    Path(args.out).write_text("\n".join(rep))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
