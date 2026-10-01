"""Simple, literature-comparable tortuosity measures per vessel, ImageCAS-X TRAIN split only.

Reads only centerline VTKs (+ Dominance / Image Quality columns of Descriptors.xlsx).
Writes one row per (case, vessel) to $OUT/simple_measures.csv.

Pipeline per vessel (LM, LAD, LCX, RCA; longest geodesic path of the label, tortuosity/vessels.py):
  arc-length resample 0.25 mm -> measures below. No extra smoothing: the delivered centerline
  already carries a 0.5 mm Gaussian smoothing.
3D:  L, D, DM = L/D (Bullitt distance metric), TI = DM - 1
     kappa_a  = sum of chord turning angles at chord 5 mm / L       (rad/mm, earlier report's primary)
     soam     = Bullitt SOAM at 1 mm steps: sum sqrt(IP^2 + TP^2) / L   (rad/cm, as in Bullitt 2003)
     soam_ip  = in-plane part only, sum IP / L                      (rad/cm)
     n_infl   = Frenet normal flips (dN.dN > 2) at 1 mm steps, significant-curvature vertices only
     icm      = DM * (n_infl + 1)
     bends    = runs of vertices (chord 1 mm) turning > KFLOOR*1 mm, split at binormal flips;
                bend angle = cumulative turning over the run; counts >= 45, 90, 180 deg
2D:  same DM and bend counts on the projection onto a standard angiographic view (LPS frame,
     +x left, +y posterior, +z superior), plus DM averaged over 256 anterior-hemisphere views
     and DM at the view with least foreshortening (max projected length).
"""
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from tortuosity.merged import chord_resample  # noqa: E402
from tortuosity.vessels import longest_path, read  # noqa: E402

DATA = os.environ["ImageCAS_X_data_path"]
OUT = "/work3/s254124/imagecasx_results/tortuosity_research/simple"
H = 0.25          # resample step, mm
KFLOOR = 0.02     # 1/mm, a vertex is "bending" if turning > KFLOOR * chord
LABELS = {"LM": (1, "left"), "LAD": (2, "left"), "LCX": (3, "left"), "RCA": (9, "right")}
# (primary angle, LAO > 0; secondary angle, cranial > 0), degrees
VIEWS = {"LM": (0, 0), "LAD": (-20, 30), "LCX": (-20, -30), "RCA": (30, 0)}


def resample(P):
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
    t = np.arange(0, s[-1] + 1e-9, H)
    return np.stack([np.interp(t, s, P[:, k]) for k in range(P.shape[1])], 1)


def length(P):
    return np.linalg.norm(np.diff(P, axis=0), axis=1).sum()


def turns(V):
    u = np.diff(V, axis=0)
    u /= np.linalg.norm(u, axis=1, keepdims=True)
    return u, np.arccos(np.clip((u[:-1] * u[1:]).sum(1), -1, 1))


def bends(P, kfloor=KFLOOR, l=1.0):
    """Cumulative turning angle (deg) of each bend."""
    if P.shape[1] == 2:
        P = np.c_[P, np.zeros(len(P))]
    V = chord_resample(P, l)
    if len(V) < 4:
        return np.array([])
    u, th = turns(V)
    b = np.cross(u[:-1], u[1:])
    sig = th > kfloor * l
    out, cur, prev_b = [], 0.0, None
    for k in range(len(th)):
        if not sig[k]:
            if cur:
                out.append(cur)
            cur, prev_b = 0.0, None
            continue
        bk = b[k] / np.linalg.norm(b[k])
        if prev_b is not None and bk @ prev_b < 0:  # inflection: new bend
            out.append(cur)
            cur = 0.0
        cur += th[k]
        prev_b = bk
    if cur:
        out.append(cur)
    return np.degrees(out)


def soam_icm(P, L):
    V = chord_resample(P, 1.0)
    if len(V) < 5:
        return np.nan, np.nan, 0
    u, ip = turns(V)
    b = np.cross(u[:-1], u[1:])
    nb = np.linalg.norm(b, axis=1)
    ok = nb > 1e-9
    b[ok] /= nb[ok, None]
    tp = np.arccos(np.clip((b[:-1] * b[1:]).sum(1), -1, 1))
    tp[~(ok[:-1] & ok[1:])] = 0
    cp = np.sqrt(ip[1:] ** 2 + tp ** 2)
    # Frenet normal N = b x u; flip if dN.dN > 2 (N rotates > 90 deg) between significant vertices
    N = np.cross(b, u[1:])
    sig = np.flatnonzero(ip > KFLOOR * 1.0)
    dn = N[sig[1:]] - N[sig[:-1]]
    n_infl = int(((dn * dn).sum(1) > 2).sum())
    return cp.sum() / (L / 10), ip.sum() / (L / 10), n_infl


def view_dir(a, c):
    a, c = np.radians(a), np.radians(c)
    return np.array([np.sin(a) * np.cos(c), -np.cos(a) * np.cos(c), np.sin(c)])


def basis(d):
    e1 = np.cross(d, [0, 0, 1.0])
    if np.linalg.norm(e1) < 1e-6:
        e1 = np.array([1.0, 0, 0])
    e1 /= np.linalg.norm(e1)
    return np.stack([e1, np.cross(d, e1)], 1)


rng = np.random.default_rng(0)
_D = rng.normal(size=(256, 3))
_D /= np.linalg.norm(_D, axis=1, keepdims=True)
_D[:, 1] = -np.abs(_D[:, 1])  # anterior hemisphere
HEMI = np.stack([basis(d) for d in _D])  # (256, 3, 2)


def measures(P, vessel):
    S = resample(P)
    L, D = length(S), np.linalg.norm(S[-1] - S[0])
    V5 = chord_resample(S, 5.0)
    ka = turns(V5)[1].sum() / L if len(V5) >= 3 else np.nan
    soam, soam_ip, n_infl = soam_icm(S, L)
    bd = bends(S)
    # 2D, standard view
    S2 = S @ basis(view_dir(*VIEWS[vessel]))
    L2, D2 = length(S2), np.linalg.norm(S2[-1] - S2[0])
    bd2 = bends(S2)
    # all views
    Pr = np.einsum("nk,vkj->vnj", S, HEMI)
    Lv = np.linalg.norm(np.diff(Pr, axis=1), axis=2).sum(1)
    Dv = np.linalg.norm(Pr[:, -1] - Pr[:, 0], axis=1)
    best = np.argmax(Lv)
    return dict(
        L=L, D=D, DM=L / D, kappa_a5=ka, soam=soam, soam_ip=soam_ip, n_infl=n_infl,
        icm=L / D * (n_infl + 1),
        nb45=int((bd >= 45).sum()), nb90=int((bd >= 90).sum()), nb180=int((bd >= 180).sum()),
        nb45_90=int(((bd >= 45) & (bd < 90)).sum()), nb90_180=int(((bd >= 90) & (bd < 180)).sum()),
        max_bend=bd.max() if len(bd) else 0.0,
        DM2_std=L2 / D2, fs_std=L2 / L, nb45_2d=int((bd2 >= 45).sum()), nb90_2d=int((bd2 >= 90).sum()),
        nb180_2d=int((bd2 >= 180).sum()),
        DM2_mean=np.mean(Lv / Dv), DM2_best=Lv[best] / Dv[best], fs_best=Lv[best] / L,
    )


def run(ids=None, tag=""):
    ids = ids or open(f"{DATA}/filelist/train.txt").read().split()
    rows, t0 = [], time.time()
    for cid in ids:
        t1 = time.time()
        g = {s: read(f"{DATA}/centerlines/{cid}.coronary_{s}_centerline.vtk") for s in ("left", "right")}
        ost = {}
        for name, (lab, side) in LABELS.items():
            pts, label, edges = g[side]
            m = (label[edges[:, 0]] == lab) & (label[edges[:, 1]] == lab)
            if m.sum() < 2:
                rows.append(dict(id=cid, vessel=name, missing=True))
                continue
            P = longest_path(pts, edges[m])
            ost[name] = P
            rows.append(dict(id=cid, vessel=name, missing=False, **measures(P, name)))
        # frame sanity: left system to patient left (+x) of RCA, LAD distal end below LM
        chk = ("LM" in ost and "RCA" in ost and "LAD" in ost)
        for r in rows[-4:]:
            r["sec"] = time.time() - t1
            r["frame_ok"] = bool(chk and ost["LM"][:, 0].mean() > ost["RCA"][:, 0].mean()
                                 and min(ost["LAD"][[0, -1], 2]) < ost["LM"][:, 2].mean()) if chk else None
    df = pd.DataFrame(rows)
    dsc = pd.read_excel(f"{DATA}/Descriptors.xlsx", usecols=["Scan ID", "Image Quality", "Dominance"])
    dsc["id"] = dsc["Scan ID"].astype(str)
    df = df.merge(dsc[["id", "Image Quality", "Dominance"]], on="id", how="left")
    os.makedirs(OUT, exist_ok=True)
    df.to_csv(f"{OUT}/simple_measures{tag}.csv", index=False)
    print(f"{len(ids)} cases, {time.time() - t0:.1f} s total")
    return df


if __name__ == "__main__":
    run(tag=sys.argv[1] if len(sys.argv) > 1 else "")
