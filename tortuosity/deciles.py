"""RCA tortuosity groups at the 10th and 90th percentiles, their figures, and a blinded visual check.

Follows Tello Ayala et al., JACC: Advances 2026 (their Figure 2 and 300-angiogram visual check).

    python -m tortuosity.deciles make     # groups, figures, blinded labelling sample
    python -m tortuosity.deciles score    # after filling labels_todo.csv (and repeat_todo.csv)

Both take an optional vessel, `make LAD` or `make LCX`, written to their own subfolder and figure names.

Reads T_5 from `python -m tortuosity.score --split <s>` for train, val and test, so all 800
ImageCAS-X RCAs are grouped: low = bottom decile, average = middle eight deciles, high = top decile.

Labelling: open label_imgs/<token>.png in token order and write 1 (tortuous) or 0 in the
`tortuous` column of labels_todo.csv. Do not open key.csv until you are done. At least a week
later, label the tokens in repeat_todo.csv the same way; `score` uses them as your own agreement.
`make` never redraws the sample once key.csv exists, so labels are not overwritten.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from . import paths  # noqa: E402
from .score import CHORDS  # noqa: E402
from .vessels import load_vessels  # noqa: E402

SPLITS = ("train", "val", "test")
SEED = 42
N_PER_GROUP, N_REPEAT = 50, 20  # Tello Ayala et al. sampled 100 from each group
GROUPS = ("low", "average", "high")
COLORS = {"low": "#2a78d6", "average": "#b5b3ad", "high": "#e34948"}
INK, MUTED = "#0b0b0b", "#52514e"


def view_dir(a, c):
    """LPS viewer direction for primary angle a (LAO > 0) and secondary angle c (cranial > 0), degrees."""
    a, c = np.radians(a), np.radians(c)
    return np.array([np.sin(a) * np.cos(c), -np.cos(a) * np.cos(c), np.sin(c)])


def basis(d):
    """Screen axes (patient right, inferior) for viewing direction d, as a (3, 2) matrix."""
    e1 = np.cross(d, [0, 0, 1.0])
    if np.linalg.norm(e1) < 1e-6:
        e1 = np.array([1.0, 0, 0])
    e1 /= np.linalg.norm(e1)
    return np.stack([e1, np.cross(d, e1)], 1)


VIEWS = {"AP": view_dir(0, 0), "LAO 30": view_dir(30, 0), "Left lateral": view_dir(90, 0), "Axial": view_dir(0, 90)}
PAPER = "Tello Ayala et al. 2026: tortuous precision 75.3 %, recall 58.0 %; non-tortuous 85.6 % / 83.5 %; kappa 0.52 (0.41-0.63), n = 300"


def groups(x):
    lo, hi = np.quantile(x, [0.1, 0.9])
    return np.where(x <= lo, "low", np.where(x >= hi, "high", "average")), lo, hi


def draw(axes, P, color):
    """The vessel in each of VIEWS, all at one mm scale, ostium as a dot, 10 mm scale bar in the first."""
    # basis gives screen axes (patient right, inferior); negating is a 180 degree
    # turn to the radiological view (patient right on screen left, superior up)
    Q = {k: -(P - P.mean(0)) @ basis(d) for k, d in VIEWS.items()}
    r = max(np.abs(q).max() for q in Q.values()) * 1.05
    for ax, (k, q) in zip(axes, Q.items()):
        ax.plot(q[:, 0], q[:, 1], color=color, lw=2, solid_capstyle="round")
        ax.plot(*q[0], "o", ms=5, color=INK)
        ax.set(xlim=(-r, r), ylim=(-r, r), aspect="equal", xticks=[], yticks=[])
        ax.set_title(k, fontsize=8, color=MUTED)
        for s in ax.spines.values():
            s.set_visible(False)
    axes[0].plot([-r * 0.95, -r * 0.95 + 10], [-r * 0.95] * 2, color=INK, lw=1.5)
    axes[0].text(-r * 0.95 + 5, -r * 0.97, "10 mm", fontsize=7, color=MUTED, ha="center", va="top")


def outdir(V):
    return paths.DECILES if V == "RCA" else f"{paths.DECILES}/{V}"  # RCA keeps the top level, so its key.csv and labels are never touched


def make(V="RCA"):
    out = outdir(V)
    fig_d = paths.DECILE_FIG.format(vessel=V.lower())
    fig_e = paths.EXAMPLE_FIG.format(vessel=V.lower())
    os.makedirs(f"{out}/label_imgs", exist_ok=True)
    df = pd.concat([pd.read_csv(f"{paths.SCORES}/{s}_vessels.csv").assign(split=s) for s in SPLITS])
    df = df[df.vessel == V].reset_index(drop=True)
    n_scans = sum(1 for s in SPLITS for _ in open(paths.FILELIST.format(split=s)) if _.strip())
    df["group"], lo, hi = groups(df.T_5.values)
    df[["case", "split", "length_mm", "T_5", "group"]].to_csv(f"{out}/groups.csv", index=False)
    print(f"{len(df)} {V}s of {n_scans} scans; cut-offs T_5 {lo:.4f} / {hi:.4f} 1/mm")
    print(df.group.value_counts().reindex(GROUPS).to_string())
    tr = df[df.split == "train"]
    print("chord choice, median over", len(tr), f"training {V}s:", ", ".join(f"T_{l} {tr[f'T_{l}'].median():.4f}" for l in CHORDS))

    plt.rcParams.update({"font.size": 9, "font.family": "sans-serif", "axes.edgecolor": MUTED})
    fig, ax = plt.subplots(figsize=(4.0, 5.0), facecolor="white")
    t5 = df.T_5
    bins = np.linspace(t5.min(), t5.max(), 36)
    ax.hist([t5[df.group == g] for g in GROUPS], bins, stacked=True, color=[COLORS[g] for g in GROUPS],
            edgecolor="white", lw=0.6, label=[f"{g} (n = {(df.group == g).sum()})" for g in GROUPS])
    top = ax.get_ylim()[1] * 1.12
    for x, t in ((lo, "10th\npercentile"), (hi, "90th\npercentile")):
        ax.axvline(x, color=MUTED, lw=1, ls=(0, (3, 2)))
        ax.text(x, top, f" {t}", fontsize=7.5, color=MUTED, va="top")
    ax.set_ylim(0, top)
    ax.set(xlabel=r"mean absolute curvature $T_5$ (rad/mm)", ylabel=f"{V}s")
    deg = ax.secondary_xaxis("top", functions=(np.degrees, np.radians))
    deg.set_xlabel("(\u00b0/mm)", fontsize=8, color=MUTED)
    deg.tick_params(labelsize=7.5, colors=MUTED)
    ax.legend(frameon=False, fontsize=8, loc="center right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(f"{fig_d}.png", dpi=200, bbox_inches="tight")
    fig.savefig(f"{fig_d}.pdf", bbox_inches="tight")
    plt.close(fig)

    fig = plt.figure(figsize=(5.2, 6.2), facecolor="white")
    gs = fig.add_gridspec(3, 1, hspace=0.95)
    for row, g in enumerate(GROUPS):
        sub = df[df.group == g]
        cells = gs[row].subgridspec(1, len(VIEWS), wspace=0.05)
        r = sub.loc[(sub.T_5 - sub.T_5.median()).abs().idxmin()]
        axes = [fig.add_subplot(cells[j]) for j in range(len(VIEWS))]
        draw(axes, load_vessels(r.case)[V], COLORS[g])
        axes[0].text(0, 1.32, f"{g}: scan {r.case}\n$T_5$ = {r.T_5:.3f} rad/mm ({np.degrees(r.T_5):.1f}\u00b0/mm)",
                     transform=axes[0].transAxes, fontsize=8, color=INK, va="bottom")
    fig.savefig(f"{fig_e}.png", dpi=200, bbox_inches="tight")
    fig.savefig(f"{fig_e}.pdf", bbox_inches="tight")
    plt.close(fig)

    if os.path.exists(f"{out}/key.csv"):
        print("key.csv exists: labelling sample kept as is")
        return
    rng = np.random.default_rng(SEED)
    sample = pd.concat([df[df.group == g].sample(N_PER_GROUP, random_state=rng) for g in GROUPS])
    sample["token"] = [f"r{k:03d}" for k in rng.permutation(len(sample)) + 1]
    fails = []
    for _, r in sample.iterrows():
        try:
            fig, axes = plt.subplots(1, len(VIEWS), figsize=(10, 2.8), facecolor="white")
            draw(axes, load_vessels(r.case)[V], INK)
            fig.savefig(f"{out}/label_imgs/{r.token}.png", dpi=110, bbox_inches="tight")
            plt.close(fig)
        except Exception as e:
            fails.append(f"{r.token}\t{r.case}\t{e!r}\n")
    open(f"{out}/label_failed.txt", "w").writelines(fails)
    sample.sort_values("token")[["token", "case", "group", "T_5"]].to_csv(f"{out}/key.csv", index=False)
    pd.DataFrame({"token": sorted(sample.token), "tortuous": ""}).to_csv(f"{out}/labels_todo.csv", index=False)
    pd.DataFrame({"token": rng.choice(sample.token, N_REPEAT, replace=False), "tortuous": ""}).to_csv(
        f"{out}/repeat_todo.csv", index=False)
    print(f"{len(sample)} label images, {len(fails)} failed (label_failed.txt)")


def kappa(a, b):
    pe = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
    return ((a == b).mean() - pe) / (1 - pe)


def score(V="RCA"):
    out = outdir(V)
    key = pd.read_csv(f"{out}/key.csv")
    lab = pd.read_csv(f"{out}/labels_todo.csv").merge(key, on="token")
    missing = lab.tortuous.isna().sum()
    lab = lab.dropna(subset=["tortuous"])
    y, t = lab.tortuous.astype(int).values, (lab.group == "high").astype(int).values
    lines = [f"{len(lab)} labelled, {missing} blank",
             pd.crosstab(pd.Series(t, name="score high"), pd.Series(y, name="you tortuous")).to_string()]
    for name, a, b in (("tortuous", t, y), ("non-tortuous", 1 - t, 1 - y)):
        lines.append(f"{name}: precision {100 * (a & b).sum() / a.sum():.1f} %, recall {100 * (a & b).sum() / b.sum():.1f} %")
    rng = np.random.default_rng(SEED)
    boot = [kappa(t[i], y[i]) for i in (rng.integers(0, len(y), len(y)) for _ in range(2000))]
    lines.append(f"kappa {kappa(t, y):.2f} (95 % CI {np.nanpercentile(boot, 2.5):.2f}-{np.nanpercentile(boot, 97.5):.2f}), "
                 "bootstrap over scans")
    rep = pd.read_csv(f"{out}/repeat_todo.csv").dropna(subset=["tortuous"]).merge(lab[["token", "tortuous"]], on="token")
    if len(rep):
        lines.append(f"your repeat agreement: kappa {kappa(rep.tortuous_x.astype(int).values, rep.tortuous_y.astype(int).values):.2f} "
                     f"on {len(rep)} vessels (the ceiling for the score)")
    lines.append(PAPER)
    open(f"{out}/score.txt", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    {"make": make, "score": score}[sys.argv[1]](*sys.argv[2:])
