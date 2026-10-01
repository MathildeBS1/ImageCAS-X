"""Regional tortuosity for the RCA (two case-study scans, or all 560 training scans) and the LAD.

Regions along the RCA (label 9, ostium to distal, same path as easy.py):
  proximal  0 to 40 mm
  mid       40 mm to L - 20 mm
  crux      last 20 mm before the RCA label ends, where it splits into R-PDA / R-PLA
plus "proximal_trim" 5 to 40 mm, to show the effect of the ostial take-off.

Regions along the LAD (label 2) and LCx (label 3), LM bifurcation to distal, SCCT-style landmarks:
  proximal  0 to the first side branch take-off (D1 label 4 / OM1 label 6)
  mid       to the second take-off (D2 label 5 / OM2 label 7), or halfway to the trunk end if absent
  distal    the rest
plus "whole_trim" 5 mm to the end, to test for a take-off hook at the LM bifurcation.
Regions shorter than 10 mm or without their landmark give a NaN row with the reason.

Everything is computed once on the whole vessel and then attributed to regions, so regional
totals add up to the whole-vessel value and no region loses its edges to a chord or a filter:
  easy (delivered centerline, 0.25 mm resampled, no extra smoothing, as easy.py):
    arc/chord of the region sub-curve (3D and LAO 30 shadow), kappa_a5 = sum of 5 mm chord
    turning angles with their vertex in the region / region length, total turning, bends >= 45
    and >= 90 deg with their centre in the region, largest bend, mean 10 mm window arc/chord.
  advanced (same curve, as bishop.py): kB = RMS |psi| over the region, f_twist from the
    windowed planar / total energy densities summed over the region, f_wiggle from the
    DCT high band summed over the region.

Run: source env.sh && python tortuosity/research/case_study/regional.py [train | lad | lcx]
Two cases: $OUT/regional_metrics.csv, $OUT/regional_lao30.png.
'train': 560 training RCAs to $OUT/regional_train560.csv; 'lad' / 'lcx': 560 training LADs /
LCxs to $OUT/regional_{lad,lcx}_train560.csv (each + _failed.txt).
"""
import os
import sys

import matplotlib
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d

sys.path.insert(0, os.path.dirname(__file__))
from easy import IDS, LAO30, OUT, arcpos, basis, bends_pos, chord_resample, load_rca, ti10, turns, view_dir  # noqa: E402
from tortuosity.research.unified.bishop import H, W, arc_resample, band_split, bishop_psi  # noqa: E402
from tortuosity.vessels import longest_path, read  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

DATA = os.environ["ImageCAS_X_data_path"]
PROX, CRUX, TRIM = 40.0, 20.0, 5.0
LAD_VIEW = view_dir(-20, 30)  # RAO 20 / CRA 30, the standard LAD angiographic view
LCX_VIEW = view_dir(-20, -30)  # RAO 20 / CAU 30, the standard LCx view


def regions(L):
    return {"whole": (0, L), "proximal": (0, PROX), "proximal_trim": (TRIM, PROX),
            "mid": (PROX, L - CRUX), "crux": (L - CRUX, L)}


def crux_labels(cid, end):
    """Labels of centerline points within 3 mm of the RCA distal end: checks the crux assumption."""
    pts, lab, _ = read(f"{DATA}/centerlines/{cid}.coronary_right_centerline.vtk")
    return sorted(set(lab[np.linalg.norm(pts - end, axis=1) < 3.0].tolist()))


def advanced_density(P):
    """Pointwise |psi|^2, planar and total windowed densities, high-band |psi_hi|^2."""
    C = arc_resample(P)
    psi = bishop_psi(C)
    q = psi ** 2
    sd = W / H
    gq = np.abs(gaussian_filter1d(q.real, sd, mode="reflect") + 1j * gaussian_filter1d(q.imag, sd, mode="reflect"))
    ga = gaussian_filter1d(np.abs(psi) ** 2, sd, mode="reflect")
    lo, hi, _, _ = band_split(psi)
    return np.arange(len(C)) * H, np.abs(psi) ** 2, gq, ga, np.abs(lo) ** 2, np.abs(hi) ** 2


def trunk(cid, t, b1, b2):
    """Left trunk path (label t) oriented from the LM, arc positions of the first / second side
    branch take-offs (labels b1, b2: D1/D2 for the LAD, OM1/OM2 for the LCx), and regions."""
    pts, lab, E = read(f"{DATA}/centerlines/{cid}.coronary_left_centerline.vtk")
    P = longest_path(pts, E[(lab[E[:, 0]] == t) & (lab[E[:, 1]] == t)])
    lm = pts[lab == 1]
    if len(lm) and np.linalg.norm(lm - P[-1], axis=1).min() < np.linalg.norm(lm - P[0], axis=1).min():
        P = P[::-1]
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
    take = {}
    for name, k in (("b1", b1), ("b2", b2)):
        e = E[((lab[E[:, 0]] == t) & (lab[E[:, 1]] == k)) | ((lab[E[:, 0]] == k) & (lab[E[:, 1]] == t))]
        q = pts[[a if lab[a] == t else b for a, b in e]] if len(e) else pts[lab == k]
        d = np.linalg.norm(P[:, None] - q[None], axis=2).min(1) if len(q) else np.array([np.inf])
        take[name] = s[d.argmin()] if d.min() < 3 else np.nan
    L, d1, d2 = s[-1], take["b1"], take["b2"]
    mid_end = d2 if d2 > d1 else (d1 + L) / 2
    regs = {"whole": (0, L), "whole_trim": (TRIM, L), "proximal": (0, d1), "mid": (d1, mid_end),
            "distal": (mid_end, L)}
    return P, regs, dict(b1_mm=d1, b2_mm=d2, b2_used=bool(d2 > d1))


def lad(cid):
    return trunk(cid, 2, 4, 5)


def lcx(cid):
    return trunk(cid, 3, 6, 7)


def rca(cid):
    P = load_rca(cid)[0]
    L = np.linalg.norm(np.diff(P, axis=0), axis=1).sum()
    return P, regions(L), dict(crux_ok=bool({10, 11} & set(crux_labels(cid, P[-1]))))


def measure(cid, vessel=rca, view=LAO30):
    """Regional rows for one scan. Everything is computed on the whole vessel, then attributed."""
    P, regs, info = vessel(cid)
    S = arc_resample(P)
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(S, axis=0), axis=1))]
    L = s[-1]
    V5 = chord_resample(S, 5.0)
    th5 = turns(V5)[1]
    s5 = arcpos(S, s, V5)[1:-1]
    sa, e2, gq, ga, elo, ehi = advanced_density(P)
    bd, t10a = bends_pos(S, s), ti10(S)
    rows = []
    for name, (a, b) in regs.items():
        m = (s >= a) & (s <= b)
        if not b - a >= 10 or m.sum() < 41:
            rows.append(dict(id=cid, region=name, start_mm=a, end_mm=b, **info,
                             reason="no landmark" if np.isnan(b - a) else "region < 10 mm"))
            continue
        R = S[m]
        R2 = R @ basis(view)
        len3 = s[m][-1] - s[m][0]
        tt = th5[(s5 >= a) & (s5 < b)].sum()
        ang = np.array([x[3] for x in bd if a <= x[1] < b])
        ma = (sa >= a) & (sa <= b)
        t10 = t10a[m]
        rows.append(dict(
            id=cid, region=name, start_mm=round(a, 1), end_mm=round(b, 1), **info, reason="",
            vessel_length_mm=L, length_mm=len3,
            arc_chord=len3 / np.linalg.norm(R[-1] - R[0]),
            arc_chord_2D=np.linalg.norm(np.diff(R2, axis=0), axis=1).sum() / np.linalg.norm(R2[-1] - R2[0]),
            kappa_a5=tt / len3, total_turning_deg=np.degrees(tt),
            bends_ge45=int((ang >= 45).sum()), bends_ge90=int((ang >= 90).sum()),
            max_bend_deg=ang.max() if len(ang) else 0.0,
            ti10_mean=np.nanmean(t10) - 1 if np.isfinite(t10).any() else np.nan,
            kB=np.sqrt(e2[ma].mean()), f_twist=1 - gq[ma].sum() / ga[ma].sum(),
            f_wiggle=ehi[ma].sum() / (elo[ma].sum() + ehi[ma].sum())))
    return rows, (S @ basis(view), s, L)


def cohort(tag="", vessel=rca, view=LAO30):
    """All 560 training scans; per-case failures logged, not dropped silently."""
    ids = open(f"{DATA}/filelist/train.txt").read().split()
    rows, failed = [], []
    for k, cid in enumerate(ids):
        try:
            rows += measure(cid, vessel, view)[0]
        except Exception as e:  # noqa: BLE001
            failed.append(f"{cid}\t{type(e).__name__}: {e}")
            rows.append(dict(id=cid, region="whole", reason=f"failed: {type(e).__name__}"))
        if k % 50 == 0:
            print(k, cid, flush=True)
    os.makedirs(OUT, exist_ok=True)
    pd.DataFrame(rows).to_csv(f"{OUT}/regional{tag}_train560.csv", index=False)
    open(f"{OUT}/regional{tag}_train560_failed.txt", "w").write("\n".join(failed) + "\n")
    print(f"{len(ids)} scans, {len(failed)} failed")


def main():
    rows, curves = [], {}
    for cid in IDS:
        r, curves[cid] = measure(cid)
        rows += r
    df = pd.DataFrame(rows)
    os.makedirs(OUT, exist_ok=True)
    df.to_csv(f"{OUT}/regional_metrics.csv", index=False)
    with pd.option_context("display.width", 200, "display.max_columns", 30):
        print(df.round(3).to_string(index=False))

    col = {"proximal": "#2f6fb0", "mid": "#8a8f98", "crux": "#b0487a"}
    fig, axs = plt.subplots(1, 2, figsize=(11, 5.5), dpi=200)
    for ax, cid in zip(axs, IDS):
        X, s, L = curves[cid]
        X = X - (X.max(0) + X.min(0)) / 2
        for name in ("proximal", "mid", "crux"):
            a, b = regions(L)[name]
            m = (s >= a) & (s <= b)
            ax.plot(X[m, 0], X[m, 1], color=col[name], lw=3, label=name)
        ax.plot(*X[0], "ko")
        ax.annotate("ostium", X[0], textcoords="offset points", xytext=(6, 4), fontsize=8)
        r = df[df.id == cid].set_index("region")
        txt = "\n".join(f"{n:<9s} κa {r.kappa_a5[n]:.3f}  A/C {r.arc_chord[n]:.2f}  "
                        f"≥45° {r.bends_ge45[n]}  f_twist {r.f_twist[n]:.2f}" for n in ("proximal", "mid", "crux"))
        ax.text(0.01, 0.01, txt, transform=ax.transAxes, fontsize=7.5, family="monospace", va="bottom")
        ax.set(title=f"Scan {cid} RCA, LAO 30 shadow", xlim=(-40, 40), ylim=(-40, 40), aspect="equal", xlabel="mm")
        ax.grid(alpha=0.3)
    axs[0].legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(f"{OUT}/regional_lao30.png")


if __name__ == "__main__":
    arg = sys.argv[1:]
    runs = {"train": ("", rca, LAO30), "lad": ("_lad", lad, LAD_VIEW), "lcx": ("_lcx", lcx, LCX_VIEW)}
    cohort(*runs[arg[0]]) if arg else main()
