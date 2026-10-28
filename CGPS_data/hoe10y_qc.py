"""Quality check of the HØ_10Y dataset that Kit uploaded to dtu-gpu-7:/data/kimbr/HØ_10Y/:
spreadsheets (visual analysis + patient characteristics), BL/FU NIfTI volumes, Medis BL centerline
trees and Medis vessel-wall contours (lumen + outer wall, diseased segments only), and the
extraction log.

    python CGPS_data/hoe10y_qc.py --inspect          # 1. what is there and how it is named (fast)
    python CGPS_data/hoe10y_qc.py --limit 20         # 2. trial run on 20 patients
    python CGPS_data/hoe10y_qc.py --workers 8        # 3. full run
    python CGPS_data/hoe10y_qc.py --no-voxels        # tables/files/geometry only, no volumes read
    python CGPS_data/hoe10y_qc.py --out /other/dir   # results somewhere else than OUT_DIR

Run it from the repo root (it imports centerline_qc.py from the same folder). Needs numpy, pandas,
matplotlib, openpyxl, nibabel and scipy. Start with --inspect and read inventory.md: if a file kind
is not recognised (0 trees, 0 contours, IDs that do not match study_id), fix the patterns under
"file naming" below before the full run.

Checks (Kit's questions in brackets)
1. Spreadsheets: rows, duplicate study_id, BL/FU overlap, columns vs header_BL/FU.xlsx, missingness,
   implausible values, BL->FU interval, SIS recomputed from the segment reads, clean baseline count.
2. Coverage per patient: spreadsheet vs NIfTI (BL, FU) vs Medis tree vs Medis contours, and the
   extraction-log lines of the patients whose files are missing ("why is a file missing").
3. Volumes: header (shape, spacing, orientation, scaling), HU range, contrast, read errors.
4. Medis trees: topology from centerline_qc.analyse_case [unlabelled length, connections,
   components, impossible contacts], kinks, coordinate convention, fraction inside the volume
   [fit inside the volume], HU along the centerline, HU 3 mm off the centerline, longest dark run
   [overlay with the volume, identify errors].
5. Medis contours per segment: rings closed/planar/perpendicular to and centred on the segment
   centerline, lumen inside outer wall, areas, ring spacing; HU in lumen core, wall and 1 mm outside
   [overlay]; distance and label agreement with the tree [does it connect]; derived Medis
   quantification (MLA, diameter stenosis, plaque burden, plaque volume, calcified wall fraction).
6. Visual analysis vs Medis: visual grade x contours present [diseased visually but no contours,
   contours but visually normal], visual grade vs Medis stenosis/plaque burden, visual plaque type
   vs calcified wall fraction, *_medis_finished/*_medis_egnet vs contours.

Outputs (OUT_DIR = /home/s254124/thesis/data_exploration/results/hoe10y_qc, or --out):
- inventory.md     folder layout, file kinds, example of every file kind (header/arrays), log head.
- report.md        all checks as aggregate tables. No study_id and no row-level values, but it still
                   describes clinical data: check it against the data agreement before copying it
                   off the DTU machine.
- figures/         aggregate distributions.
- cases/           STAYS ON THE DTU MACHINE: per-patient/per-segment CSVs with study_id, ID lists per
                   problem (cases/lists/*.txt), overlay images (cases/overlays/*.png).

Coordinates: Medis exports world coordinates in mm; NIfTI maps voxels to RAS mm. The convention
(points are RAS, LPS = DICOM, z flipped, or voxel indices) is calibrated on the first CALIB_N
patients by which one puts the centerline on bright (contrast-filled) voxels, then used for all;
per patient the best convention is also stored, so a patient that disagrees is flagged.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import traceback
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import centerline_qc as cq  # noqa: E402 - tree parsing and topology metrics

# ---- edit these before running (or override with --root / --out) ----
ROOT = "/data/kimbr/HØ_10Y"
OUT_DIR = "/home/s254124/thesis/data_exploration/results/hoe10y_qc"  # own subfolder: report.md would clash with cgps_stats.py
HEADER_DIR = Path(__file__).resolve().parent  # header_BL.xlsx / header_FU.xlsx for the column check

# ---- file naming (check against inventory.md) ----
SHEETS = {"BL": "Visual_Analysis_and_Patient_Characteristics/BL_anonymised.xlsx",
          "FU": "Visual_Analysis_and_Patient_Characteristics/FU_anonymised.xlsx"}
NIFTI_DIR = "NIFTI"
MEDIS_DIR = "Medis"
ID_COL = "study_id"
# per-segment contour files, e.g. Medis/Analysis_Processed/contours/BL_996_pLAD_lumen.vtk
CONTOUR_RE = re.compile(r"^(?P<visit>BL|FU)_(?P<id>\d+)_(?P<seg>.+)_(?P<kind>centerline|lumen|outer)\.vtk$", re.I)
TREE_EXT = (".vtk", ".vtp")  # every other Medis .vtk/.vtp is read as a centerline tree
LOG_EXT = (".log", ".txt", ".csv")
VISIT_TOKENS = {"bl": "BL", "baseline": "BL", "fu": "FU", "followup": "FU", "10y": "FU"}

# ---- thresholds ----
CONVENTIONS = ("ras", "lps", "ras_negz", "lps_negz", "voxel")
CONVENTION = "auto"     # or one of CONVENTIONS once known
CALIB_N = 20            # patients used to calibrate the convention
DARK_HU = 150           # centerline point below this is not in contrast-filled lumen
OFF_MM = 3.0            # HU is also sampled this far off the centerline (should be darker)
PERI_MM = 1.0           # perivascular sample this far outside the outer wall
CALC_HU = 350           # wall sample above this counts as calcified
KINK_DEG = 60           # turn per 1 mm step that counts as a kink
REF_RINGS = 3           # rings at each end used as the reference lumen area
FIG_RANDOM = 10         # random patients with overlay images
FIG_WORST = 10          # worst patients (centerline contrast) with overlay images
PLAUSIBLE = {"scan_age": (18, 110), "clin_bmi": (12, 70), "clin_bp_sys_mean": (60, 260),
             "clin_bp_dia_mean": (30, 150), "hr_during_scan": (30, 150), "creatinine": (20, 1500),
             "egfr": (3, 200), "hba1c": (15, 200), "tot_cholesterol": (1, 20), "hdl": (0.1, 6),
             "ldl": (0.1, 15), "triglyceride": (0.1, 50), "ct_cacs_sum": (0, 10000)}
NAME_RANGES = {"height": (120, 220), "weight": (30, 250)}

SEGMENTS = ("lm", "plad", "mlad", "dlad", "d1", "d2", "im", "pcx", "om1", "mcx", "om2", "dcx",
            "prca", "mrca", "drca", "pda", "pla")
STENOSIS_CODES = {"none": 0, "minimal": 1, "mild": 2, "moderate": 3, "severe": 4, "occlusion": 5}
GRADES = ("none", "minimal", "mild", "moderate", "severe", "occlusion")
PLAQUE_CODES = {"calcified": 1, "mostly_calcified": 2, "mostly_noncalcified": 3, "noncalcified": 4}
TERR = {k.lower(): v for k, v in cq.TERRITORY.items()}


# ============================================================ small helpers
def norm_id(v):
    """study_id / file-name ID -> canonical string (leading zeros and '.0' dropped)."""
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return None
    if isinstance(v, (int, np.integer)) or (isinstance(v, float) and v.is_integer()):
        return str(int(v))
    m = re.search(r"\d+", str(v))
    return str(int(m.group())) if m else None


def id_from_name(name):
    stem = re.sub(r"(\.[A-Za-z0-9]+)+$", "", Path(name).name)
    stem = re.sub(r"(?i)(^|[_\-\s])(bl|fu|baseline|followup)(?=$|[_\-\s])", "_", stem)
    return norm_id(stem)


def visit_from_path(rel):
    for tok in re.split(r"[/_\-.\s]+", str(rel).lower()):
        if tok in VISIT_TOKENS:
            return VISIT_TOKENS[tok]
    return "?"


def seg_key(tok):
    """Segment name from a file name or tree label -> spreadsheet segment key (plad, mcx, ...)."""
    if tok is None:
        return None
    name = cq.ALIASES.get(cq.norm_key(tok))
    if name is None and str(tok)[:1] not in "?#":
        name = cq.normalise_label(tok)
    return (name or str(tok)).lower()


def label_text(s):
    return s.astype(str).str.strip().str.lower().str.replace(r"[\s-]+", "_", regex=True)


def num(s):
    if not pd.api.types.is_numeric_dtype(s):
        s = s.astype(str).str.strip().str.replace(",", ".", regex=False)
    return pd.to_numeric(s, errors="coerce")


def grade_of(raw):
    """Visual stenosis cell -> 'none'..'occlusion', 'unevaluable', 'missing' or 'unrecognised'."""
    if raw is None or (isinstance(raw, float) and np.isnan(raw)):
        return "missing"
    t = re.sub(r"[\s-]+", "_", str(raw).strip().lower())
    if t.startswith("uneval"):
        return "unevaluable"
    if t in STENOSIS_CODES:
        return t
    try:
        return GRADES[int(float(t))]
    except (ValueError, IndexError):
        return "unrecognised"


def dist(x, nd=1):
    x = pd.Series(x, dtype=float).dropna()
    if x.empty:
        return {"n": 0}
    q = x.quantile([0, .05, .25, .5, .75, .95, 1]).round(nd).tolist()
    return {"n": len(x), "mean": round(float(x.mean()), nd), "min": q[0], "p5": q[1], "q1": q[2],
            "median": q[3], "q3": q[4], "p95": q[5], "max": q[6]}


def dist_table(df, cols, nd=1):
    return pd.DataFrame({c: dist(df[c], nd) for c in cols if c in df}).T.reset_index(names="metric")


def pct(k, n):
    return f"{k} ({100 * k / n:.1f}%)" if n else f"{k}"


def md(df, index=False):
    if df is None or len(df) == 0:
        return "_(none)_"
    d = df.reset_index() if index else df
    return cq.md_table(d)


# ============================================================ discovery
def discover(root):
    root = Path(root)
    files = [p for p in root.rglob("*") if p.is_file() and not p.name.startswith((".", "._"))]
    medis = root / MEDIS_DIR
    niftis, trees, contours, logs, other = [], [], defaultdict(dict), [], []
    for p in files:
        rel = p.relative_to(root)
        n = p.name.lower()
        if n.endswith((".nii", ".nii.gz")):
            niftis.append({"visit": visit_from_path(rel), "id": id_from_name(p.name), "path": p})
        elif medis in p.parents and (m := CONTOUR_RE.match(p.name)):
            contours[(m["visit"].upper(), norm_id(m["id"]), seg_key(m["seg"]))][m["kind"].lower()] = p
        elif medis in p.parents and n.endswith(TREE_EXT):
            v = visit_from_path(rel)
            trees.append({"visit": "BL" if v == "?" else v, "id": id_from_name(p.name), "path": p})
        elif (n.endswith(".log") or ("log" in n and n.endswith(LOG_EXT))) and p.stat().st_size < 500e6:
            logs.append(p)
        else:
            other.append(p)
    return {"files": files, "niftis": niftis, "trees": trees, "contours": dict(contours),
            "logs": logs, "other": other}


def masked(rel):
    return re.sub(r"\d+", "#", str(rel))


def inventory(root, found, sheets):
    root = Path(root)
    out = [f"# Inventory of {root}", ""]
    by_dir = Counter((str(p.relative_to(root).parent), "".join(p.suffixes[-2:]).lower()) for p in found["files"])
    out += ["## Files per folder and extension", "",
            md(pd.DataFrame([(d, e, n) for (d, e), n in sorted(by_dir.items())], columns=["folder", "ext", "files"])), ""]
    pats = Counter(masked(p.relative_to(root)) for p in found["files"])
    out += ["## Name patterns (digits masked as #)", "",
            md(pd.DataFrame(pats.most_common(60), columns=["pattern", "files"])), ""]
    out += ["## Recognised", "",
            f"- NIfTI: {len(found['niftis'])} (visits {dict(Counter(x['visit'] for x in found['niftis']))}, "
            f"no ID: {sum(x['id'] is None for x in found['niftis'])})",
            f"- Medis trees: {len(found['trees'])}",
            f"- Medis contour segments: {len(found['contours'])} "
            f"(file kinds {dict(Counter(k for v in found['contours'].values() for k in v))})",
            f"- logs: {[str(p.relative_to(root)) for p in found['logs']]}",
            f"- other files: {len(found['other'])} (extensions {dict(Counter(''.join(p.suffixes[-2:]).lower() for p in found['other']).most_common(10))})",
            ""]
    out += ["## Examples", ""]
    examples = []
    if found["trees"]:
        examples.append(("tree", found["trees"][0]["path"]))
    for kind in ("centerline", "lumen", "outer"):
        p = next((v[kind] for v in found["contours"].values() if kind in v), None)
        if p:
            examples.append((f"contour {kind}", p))
    for label, p in examples:
        out.append(f"### {label}: `{masked(p.relative_to(root))}` ({p.stat().st_size:,} bytes)")
        try:
            v = cq.read_vtk_legacy(p.read_bytes())
            arr = lambda d: {k: list(np.shape(a)) for k, a in d.items()}
            out.append(f"- header {v['header']}; keywords {v['keywords']}")
            out.append(f"- points {v['points'].shape}, extent min {np.round(v['points'].min(0), 1).tolist()} "
                       f"max {np.round(v['points'].max(0), 1).tolist()}")
            out.append(f"- cells {{type: (n cells, median points per cell)}}: "
                       f"{ {t: (len(c), int(np.median([len(x) for x in c])) if c else 0) for t, c in v['cells'].items()} }")
            out.append(f"- point arrays {arr(v['point_data'])}; cell arrays {arr(v['cell_data'])}; "
                       f"field data {[(k, (list(a)[:20] if np.asarray(a).dtype == object else list(np.shape(a)))) for k, a in v['field_data'].items()]}")
        except Exception as ex:  # noqa: BLE001
            out.append(f"- **could not parse**: {type(ex).__name__}: {ex}")
        out.append("")
    if found["niftis"]:
        try:
            import nibabel as nib
            p = found["niftis"][0]["path"]
            img = nib.load(str(p))
            out += [f"### NIfTI `{masked(p.relative_to(root))}`",
                    f"- shape {img.shape}, zooms {tuple(round(float(z), 3) for z in img.header.get_zooms())}, "
                    f"dtype {img.get_data_dtype()}, axcodes {nib.aff2axcodes(img.affine)}, "
                    f"slope/inter {img.header.get_slope_inter()}, qform/sform code "
                    f"{int(img.header['qform_code'])}/{int(img.header['sform_code'])}",
                    "```", np.array2string(img.affine, precision=3), "```", ""]
        except Exception as ex:  # noqa: BLE001
            out.append(f"NIfTI header not read: {ex}")
    for p in found["logs"]:
        lines = p.read_text(errors="replace").splitlines()
        out += [f"### log `{p.relative_to(root)}` ({len(lines):,} lines, digits masked)", "```",
                *[masked(ln)[:200] for ln in lines[:25]], "```", ""]
    for v, df in sheets.items():
        out += [f"### {v} spreadsheet: {df.shape[0]} rows x {df.shape[1]} columns",
                f"`{', '.join(map(str, df.columns[:400]))}`", ""]
    return "\n".join(out)


# ============================================================ spreadsheets
def load_sheets(root):
    out = {}
    for v, rel in SHEETS.items():
        p = Path(root) / rel
        if p.exists():
            df = pd.read_excel(p)
            df.columns = [str(c).strip() for c in df.columns]
            out[v] = df.replace(r"^\s*$", np.nan, regex=True).copy()
    return out


def sheet_checks(sheets):
    rep, lists = [], {}
    ids = {}
    for v, df in sheets.items():
        if ID_COL not in df:
            rep.append(f"**{v}: no `{ID_COL}` column** - columns start {list(df.columns[:10])}")
            continue
        sid = df[ID_COL].map(norm_id)
        ids[v] = set(sid.dropna())
        dup = sid[sid.duplicated(keep=False) & sid.notna()]
        lists[f"sheet_{v}_duplicate_id"] = sorted(set(dup))
        rep += [f"### {v}", "",
                f"- {len(df)} rows, {sid.nunique()} unique study_id, {sid.isna().sum()} rows without ID, "
                f"{dup.nunique()} IDs on more than one row"]
        hdr = HEADER_DIR / f"header_{v}.xlsx"
        if hdr.exists():
            expected = [str(c).strip() for c in pd.read_excel(hdr, nrows=0).columns]
            new, gone = sorted(set(df.columns) - set(expected)), sorted(set(expected) - set(df.columns))
            rep.append(f"- columns: {df.shape[1]} (header_{v}.xlsx: {len(expected)}); "
                       f"new: {len(new)} `{', '.join(new[:60])}`; missing: {len(gone)} `{', '.join(gone[:60])}`")
        miss = df.isna().mean().mul(100).round(1)
        rep.append(f"- columns fully empty: {(miss == 100).sum()}; > 50% empty: {(miss > 50).sum()}")
        rows = []
        for c, (lo, hi) in {**PLAUSIBLE, **{c: r for c in df.columns for k, r in NAME_RANGES.items()
                                             if k in c.lower()}}.items():
            if c in df:
                x = num(df[c])
                rows.append({"column": c, "n": int(x.notna().sum()), "range": f"{lo}-{hi}",
                             "below": int((x < lo).sum()), "above": int((x > hi).sum()),
                             "text (not numeric)": int((df[c].notna() & x.isna()).sum())})
                lists[f"sheet_{v}_implausible_{c}"] = sorted(set(sid[(x < lo) | (x > hi)].dropna()))
        rep += ["", "Implausible values:", "", md(pd.DataFrame(rows)), ""]
        # segment reads
        g = pd.DataFrame({s: df[f"ct_cag_{s}_stenosis"].map(grade_of) for s in SEGMENTS
                          if f"ct_cag_{s}_stenosis" in df})
        if len(g.columns):
            vc = g.apply(lambda c: c.value_counts()).fillna(0).astype(int).T
            rep += ["Segment stenosis reads (segments x grade):", "", md(vc, index=True), ""]
            code = g.apply(lambda c: c.map({k: i for i, k in enumerate(GRADES)}))
            any_read = g.isin(GRADES).any(axis=1)
            sis = (code >= 1).sum(axis=1).where(any_read)
            if "ct_cag_sis" in df:
                s0 = num(df["ct_cag_sis"])
                both = sis.notna() & s0.notna()
                agree = (sis[both] == s0[both])
                rep.append(f"- SIS recomputed (segments with >= minimal) equals `ct_cag_sis`: "
                           f"{pct(int(agree.sum()), int(both.sum()))}")
                lists[f"sheet_{v}_sis_mismatch"] = sorted(set(sid[both & (sis != s0)].dropna()))
                no_read = ~any_read & s0.notna()
                rep.append(f"- rows with SIS but no segment read: {int(no_read.sum())} "
                           f"(of which SIS = 0: {int((no_read & (s0 == 0)).sum())})")
            if "ct_cag_sss" in df:
                s0 = num(df["ct_cag_sss"])
                both = code.sum(axis=1).where(any_read).notna() & s0.notna()
                rep.append(f"- Spearman(sum of segment grades, `ct_cag_sss`) = "
                           f"{code.sum(axis=1)[both].corr(s0[both], method='spearman'):.3f}")
            if v == "BL" and {"ct_cag_sis", "ct_cag_sss"} <= set(df):
                clean = (num(df["ct_cag_sis"]) == 0) & (num(df["ct_cag_sss"]) == 0)
                rep.append(f"- clean baseline (SIS = SSS = 0): {int(clean.sum())} of {len(df)} "
                           f"(with a segment read: {int((clean & any_read).sum())})")
            rep.append("")
    if {"BL", "FU"} <= set(ids):
        rep.append(f"- BL and FU: {len(ids['BL'] & ids['FU'])} in both, {len(ids['BL'] - ids['FU'])} BL only, "
                   f"{len(ids['FU'] - ids['BL'])} FU only")
        b, f = sheets["BL"], sheets["FU"]
        if "scandate" in b and "scandate" in f:
            d = pd.merge(b[[ID_COL, "scandate"]].assign(k=b[ID_COL].map(norm_id)),
                         f[[ID_COL, "scandate"]].assign(k=f[ID_COL].map(norm_id)), on="k")
            yrs = (pd.to_datetime(d["scandate_y"], errors="coerce") -
                   pd.to_datetime(d["scandate_x"], errors="coerce")).dt.days / 365.25
            rep.append(f"- BL->FU interval (years): {dist(yrs)}; FU before BL: {int((yrs < 0).sum())}")
            lists["sheet_FU_before_BL"] = sorted(set(d["k"][yrs < 0]))
    return "\n".join(rep), lists, ids


# ============================================================ geometry helpers
def to_voxel(pts, inv, conv):
    p = np.asarray(pts, float).copy()
    if conv == "voxel":
        return p
    if conv.startswith("lps"):
        p[:, :2] *= -1
    if conv.endswith("negz"):
        p[:, 2] *= -1
    return p @ inv[:3, :3].T + inv[:3, 3]


def sample(vol, ijk):
    from scipy.ndimage import map_coordinates
    if vol is None or len(ijk) == 0:
        return np.full(len(ijk), np.nan)
    return map_coordinates(vol, np.asarray(ijk).T, order=1, mode="constant", cval=np.nan)


def inside(vol_shape, ijk):
    s = np.asarray(vol_shape[:3]) - 1
    return np.all((ijk >= 0) & (ijk <= s), axis=1)


def tangents(pts):
    t = np.gradient(pts, axis=0) if len(pts) > 1 else np.array([[0, 0, 1.0]])
    n = np.linalg.norm(t, axis=1, keepdims=True)
    return t / np.where(n > 0, n, 1)


def perp_offsets(pts, mm):
    """Four points mm away from each centerline point, perpendicular to the local tangent."""
    t = tangents(pts)
    a = np.where(np.abs(t[:, [0]]) < 0.9, [[1, 0, 0]], [[0, 1, 0]])
    u = np.cross(t, a); u /= np.linalg.norm(u, axis=1, keepdims=True)
    v = np.cross(t, u)
    return [pts + s * mm * d for d in (u, v) for s in (1, -1)]


def arclen(pts):
    return np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])


def kinks(pts, step=1.0):
    """Turns > KINK_DEG between consecutive 1 mm steps (and > 150 deg: back-and-forth)."""
    s = arclen(pts)
    if s[-1] < 3 * step:
        return 0, 0
    q = np.stack([np.interp(np.arange(0, s[-1], step), s, pts[:, k]) for k in range(3)], 1)
    d = np.diff(q, axis=0)
    d /= np.maximum(np.linalg.norm(d, axis=1, keepdims=True), 1e-9)
    ang = np.degrees(np.arccos(np.clip((d[1:] * d[:-1]).sum(1), -1, 1)))
    return int((ang > KINK_DEG).sum()), int((ang > 150).sum())


def longest_run(mask, s):
    best = cur = 0.0
    for i in range(1, len(mask)):
        cur = cur + (s[i] - s[i - 1]) if mask[i] and mask[i - 1] else 0.0
        best = max(best, cur)
    return best


def ring_geom(r):
    c = r.mean(0)
    _, S, Vt = np.linalg.svd(r - c, full_matrices=False)
    uv = (r - c) @ Vt[:2].T
    x, y = uv[:, 0], uv[:, 1]
    area = 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))
    step = np.linalg.norm(np.diff(r, axis=0), axis=1)
    return {"c": c, "normal": Vt[2], "basis": Vt, "uv": uv, "area": area,
            "planarity": S[2] / S[0] if S[0] > 0 else np.nan,
            "open_gap": np.linalg.norm(r[0] - r[-1]) / max(np.median(step) if len(step) else 1, 1e-6)}


def read_rings(path, cl=None):
    """Contour file -> list of rings (n,3), and how they were found."""
    v = cq.read_vtk_legacy(Path(path).read_bytes())
    pts = v["points"]
    cells = [c for t in ("POLYGONS", "LINES") for c in v["cells"].get(t, []) if len(c) >= 3]
    if len(cells) > 1:
        return [pts[np.asarray(c)] for c in cells], "cells"
    for name, a in v["point_data"].items():  # an integer per-point ring index
        a = np.asarray(a)
        if a.ndim == 1 and len(a) == len(pts) and np.all(np.mod(a, 1) == 0) and 2 < len(np.unique(a)) < len(a) / 4:
            return [pts[a == k] for k in np.unique(a)], f"array {name}"
    if cl is not None and len(cl) > 1:  # group points by their nearest segment-centerline point
        _, j = cq.nearest(pts, cl)
        j = np.ravel(j)
        rings = []
        for k in np.unique(j):
            r = pts[j == k]
            if len(r) >= 6:  # order around the centroid
                g = ring_geom(r)
                r = r[np.argsort(np.arctan2(g["uv"][:, 1], g["uv"][:, 0]))]
                rings.append(r)
        return rings, "nearest centerline"
    return [pts], "single"


# ============================================================ per-patient worker
_W = {}


def init_worker(numbering, code_names, conv, out):
    cq._numbering = numbering
    cq._code_names.update(code_names)
    _W["conv"], _W["out"] = conv, out


def load_volume(path, voxels=True):
    import nibabel as nib
    img = nib.load(str(path))
    h = img.header
    info = {"shape": "x".join(map(str, img.shape)), "ndim": len(img.shape),
            "dx": float(h.get_zooms()[0]), "dy": float(h.get_zooms()[1]), "dz": float(h.get_zooms()[2]),
            "dtype": str(img.get_data_dtype()), "axcodes": "".join(nib.aff2axcodes(img.affine)),
            "qform_code": int(h["qform_code"]), "sform_code": int(h["sform_code"]),
            "slope": h.get_slope_inter()[0], "inter": h.get_slope_inter()[1],
            "affine_det": float(np.linalg.det(img.affine[:3, :3])), "size_mb": round(Path(path).stat().st_size / 1e6, 1)}
    info["fov_x_mm"] = img.shape[0] * info["dx"]
    info["fov_z_mm"] = img.shape[2] * info["dz"]
    vol = None
    if voxels:
        vol = img.get_fdata(dtype=np.float32)
        if vol.ndim > 3:
            vol = vol[..., 0]
        sub = vol[::2, ::2, ::2]
        q = np.nanpercentile(sub, [0.1, 1, 50, 99, 99.9])
        info.update({"hu_min": float(np.nanmin(sub)), "hu_p0.1": q[0], "hu_p1": q[1], "hu_p50": q[2],
                     "hu_p99": q[3], "hu_p99.9": q[4], "hu_max": float(np.nanmax(sub)),
                     "frac_at_min": float((sub == np.nanmin(sub)).mean()),
                     "n_nan": int(np.isnan(sub).sum())})
    return vol, img.affine, info


def volume_flags(i):
    f = []
    if i["ndim"] != 3: f.append("not_3d")
    if max(i["dx"], i["dy"]) > 1.0: f.append("xy_spacing>1mm")
    if i["dz"] > 3.0: f.append("z_spacing>3mm")
    if int(i["shape"].split("x")[2]) < 40: f.append("few_slices")
    if abs(i["affine_det"]) < 1e-6: f.append("degenerate_affine")
    if "hu_min" in i:
        if i["hu_min"] >= 0: f.append("min>=0(HU_offset?)")
        if i["hu_p1"] > -500: f.append("p1>-500(no_air?)")
        if i["hu_p99.9"] < 300: f.append("p99.9<300(no_contrast?)")
        if i["hu_max"] > 10000: f.append("max>10000")
        if i["n_nan"]: f.append("nan_voxels")
    return f


def tree_points(path):
    polys, _ = cq.parse_member(path.name, path.read_bytes())
    return [(p.pts, [seg_key(cq.normalise_label(l)) if cq.normalise_label(l) else None for l in p.labels])
            for p in polys if len(p.pts) >= 2]


def calibrate(task):
    """Per convention: fraction of Medis points inside the volume and their median HU."""
    try:
        pts = []
        if task.get("tree"):
            pts += [p for p, _ in tree_points(task["tree"])]
        for files in task["contours"].values():
            if "centerline" in files:
                pts.append(cq.read_vtk_legacy(files["centerline"].read_bytes())["points"])
        if not pts or not task.get("nifti"):
            return None
        P = np.concatenate(pts)
        vol, aff, _ = load_volume(task["nifti"])
        inv = np.linalg.inv(aff)
        out = {}
        for conv in CONVENTIONS:
            out[conv] = conv_score(vol, inv, P, conv)
        return out
    except Exception as ex:  # noqa: BLE001 - shown by main() if no patient calibrates
        return {"error": f"{task['visit']} {task['id']}: {type(ex).__name__}: {ex}"[:400],
                "trace": traceback.format_exc()[-1500:]}


def conv_score(vol, inv, P, conv):
    """(fraction inside the volume, fraction on bright voxels >= DARK_HU, median HU inside)."""
    ijk = to_voxel(P, inv, conv)
    ins = inside(vol.shape, ijk)
    hu = sample(vol, ijk[ins])
    return (float(ins.mean()), float((hu >= DARK_HU).sum() / len(P)) if len(P) else 0.0,
            float(np.nanmedian(hu)) if ins.any() else np.nan)


def best_conv(scores):
    return max(scores, key=lambda c: (scores[c][1], scores[c][0]))


def process(task):
    """One patient-visit: volume stats, tree HU/geometry, contour rings. Never raises."""
    pid, visit = task["id"], task["visit"]
    res = {"id": pid, "visit": visit, "volume": None, "tree": None, "segments": [], "rings": [], "errors": []}
    vol = inv = None
    try:
        if task.get("nifti"):
            vol, aff, info = load_volume(task["nifti"], task["voxels"])
            inv = np.linalg.inv(aff)
            info["flags"] = ";".join(volume_flags(info))
            res["volume"] = {"id": pid, "visit": visit, "file": task["nifti"].name, **info}
    except Exception as ex:  # noqa: BLE001
        res["errors"].append(f"volume: {type(ex).__name__}: {ex}"[:300])
    conv = _W.get("conv", "ras")

    tree, tree_P, tree_L = None, None, None
    if task.get("tree"):
        try:
            tree = tree_points(task["tree"])
            tree_P = np.concatenate([p for p, _ in tree])
            tree_L = [l for _, ls in tree for l in ls]
            r = {"id": pid, "visit": visit}
            k = [kinks(p) for p, _ in tree]
            r["n_kinks"], r["n_reversals"] = sum(a for a, _ in k), sum(b for _, b in k)
            if vol is not None:
                scores = {c: conv_score(vol, inv, tree_P, c) for c in CONVENTIONS}
                r["best_convention"] = best_conv(scores)
                r["inside_frac"] = round(scores[conv][0], 4)
                hu_all, off_all, dark_run, per_lab = [], [], 0.0, defaultdict(list)
                for pts, labs in tree:
                    hu = sample(vol, to_voxel(pts, inv, conv))
                    off = np.nanmedian(np.stack([sample(vol, to_voxel(q, inv, conv)) for q in perp_offsets(pts, OFF_MM)]), 0)
                    hu_all.append(hu); off_all.append(off)
                    dark_run = max(dark_run, longest_run(~(hu >= DARK_HU), arclen(pts)))
                    for h, l in zip(hu, labs):
                        per_lab[TERR.get(l, "unlabelled" if l is None else "other")].append(h)
                hu, off = np.concatenate(hu_all), np.concatenate(off_all)
                r.update({"hu_median": np.nanmedian(hu), "hu_p10": np.nanpercentile(hu, 10) if np.isfinite(hu).any() else np.nan,
                          "dark_frac": float(np.mean(~(hu >= DARK_HU))), "longest_dark_mm": round(dark_run, 1),
                          "off3mm_hu_median": np.nanmedian(off), "center_minus_off3mm": np.nanmedian(hu - off)})
                for t in ("LM", "LAD", "CX", "RCA", "unlabelled"):
                    r[f"hu_{t}"] = np.nanmedian(per_lab[t]) if per_lab[t] else np.nan
                if task.get("figs"):
                    fig_tree(task, vol, inv, conv, tree)
            res["tree"] = r
        except Exception as ex:  # noqa: BLE001
            res["errors"].append(f"tree: {type(ex).__name__}: {ex}"[:300])

    for seg, files in task["contours"].items():
        try:
            s, rings = contour_segment(pid, visit, seg, files, vol, inv, conv, tree_P, tree_L, task.get("figs"))
            res["segments"].append(s)
            res["rings"] += rings
        except Exception as ex:  # noqa: BLE001
            res["errors"].append(f"contour {seg}: {type(ex).__name__}: {ex}"[:300])
            res["segments"].append({"id": pid, "visit": visit, "segment": seg, "error": str(ex)[:200],
                                    "files": ",".join(sorted(files))})
    return res


def contour_segment(pid, visit, seg, files, vol, inv, conv, tree_P, tree_L, figs=False):
    s = {"id": pid, "visit": visit, "segment": seg, "files": ",".join(sorted(files))}
    cl = cq.read_vtk_legacy(files["centerline"].read_bytes())["points"] if "centerline" in files else None
    if cl is not None:
        s["cl_points"], s["cl_length_mm"] = len(cl), round(float(arclen(cl)[-1]), 2)
        s["cl_n_kinks"] = kinks(cl)[0]
        if tree_P is not None:
            d, j = cq.nearest(cl, tree_P)
            d, j = np.ravel(d), np.ravel(j)
            s["cl_to_tree_median_mm"], s["cl_to_tree_max_mm"] = float(np.median(d)), float(d.max())
            labs = [tree_L[k] for k in j]
            s["tree_label_same_segment"] = float(np.mean([l == seg for l in labs]))
            s["tree_label_same_artery"] = float(np.mean([TERR.get(l) == TERR.get(seg) and l is not None for l in labs]))
            s["tree_label_unlabelled"] = float(np.mean([l is None for l in labs]))
            s["tree_label_mode"] = Counter(labs).most_common(1)[0][0]
        if vol is not None:
            ijk = to_voxel(cl, inv, conv)
            s["cl_inside_frac"] = float(inside(vol.shape, ijk).mean())
            hu = sample(vol, ijk)
            s["cl_hu_median"] = float(np.nanmedian(hu)) if np.isfinite(hu).any() else np.nan
    rings = {}
    for kind in ("lumen", "outer"):
        if kind in files:
            rr, how = read_rings(files[kind], cl)
            rings[kind] = [ring_geom(r) | {"pts": r} for r in rr if len(r) >= 3]
            s[f"n_{kind}_rings"], s[f"{kind}_ring_source"] = len(rings[kind]), how
    lum, out = rings.get("lumen", []), rings.get("outer", [])
    if cl is not None:
        s["rings_per_cl_point"] = round(len(lum) / len(cl), 3) if lum else np.nan
    ring_rows = []
    if lum:
        oc = np.array([o["c"] for o in out]) if out else None
        s_cl = arclen(cl) if cl is not None else None
        for i, L in enumerate(lum):
            row = {"id": pid, "segment": seg, "ring": i, "lumen_area": L["area"],
                   "lumen_eq_diam": 2 * np.sqrt(L["area"] / np.pi), "lumen_planarity": L["planarity"],
                   "lumen_open_gap": L["open_gap"], "lumen_n_pts": len(L["pts"])}
            if cl is not None:
                d, j = cq.nearest(L["c"][None], cl)
                j = int(np.ravel(j)[0])
                row["centroid_to_cl_mm"] = float(np.ravel(d)[0])
                row["pos_mm"] = float(s_cl[j])
                row["cos_normal_tangent"] = float(abs(np.dot(L["normal"], tangents(cl)[j])))
            if oc is not None:
                d, k = cq.nearest(L["c"][None], oc)
                O = out[int(np.ravel(k)[0])]
                row["lumen_to_outer_centroid_mm"] = float(np.ravel(d)[0])
                row["outer_area"] = O["area"]
                row["plaque_burden"] = 100 * (1 - L["area"] / O["area"]) if O["area"] > 0 else np.nan
                from matplotlib.path import Path as MPath
                luv = (L["pts"] - O["c"]) @ O["basis"][:2].T
                row["lumen_inside_outer_frac"] = float(MPath(O["uv"]).contains_points(luv).mean()) if len(O["uv"]) >= 3 else np.nan
                if vol is not None:
                    core = L["c"] + 0.5 * (L["pts"] - L["c"])
                    _, m = cq.nearest(O["pts"], L["pts"])
                    wall = 0.5 * (O["pts"] + L["pts"][np.ravel(m)])
                    dirs = O["pts"] - O["c"]
                    peri = O["pts"] + PERI_MM * dirs / np.maximum(np.linalg.norm(dirs, axis=1, keepdims=True), 1e-6)
                    hc, hw, hp = (sample(vol, to_voxel(x, inv, conv)) for x in (core, wall, peri))
                    row.update({"hu_lumen_core": np.nanmedian(hc), "hu_wall": np.nanmedian(hw), "hu_peri": np.nanmedian(hp),
                                "wall_calc_frac": float(np.mean(hw > CALC_HU)) if np.isfinite(hw).any() else np.nan})
            ring_rows.append(row)
    R = pd.DataFrame(ring_rows)
    if len(R):
        if "pos_mm" in R:
            R = R.sort_values("pos_mm")
            sp = np.diff(R["pos_mm"].to_numpy())
            s["ring_spacing_median_mm"] = float(np.median(sp)) if len(sp) else np.nan
            s["ring_spacing_max_mm"] = float(sp.max()) if len(sp) else np.nan
        a = R["lumen_area"].to_numpy()
        ref = max(a[:REF_RINGS].mean(), a[-REF_RINGS:].mean())
        s.update({"mla_mm2": a.min(), "max_lumen_area_mm2": a.max(), "ref_area_mm2": ref,
                  "medis_area_stenosis_pct": 100 * (1 - a.min() / ref) if ref > 0 else np.nan,
                  "medis_diam_stenosis_pct": 100 * (1 - np.sqrt(a.min() / ref)) if ref > 0 else np.nan,
                  "min_lumen_eq_diam": R["lumen_eq_diam"].min(), "max_lumen_eq_diam": R["lumen_eq_diam"].max(),
                  "max_planarity": R["lumen_planarity"].max(), "n_open_rings": int((R["lumen_open_gap"] > 3).sum())})
        for c, agg in (("centroid_to_cl_mm", "median"), ("centroid_to_cl_mm", "max"), ("cos_normal_tangent", "min"),
                       ("cos_normal_tangent", "median"), ("lumen_inside_outer_frac", "min"), ("plaque_burden", "max"),
                       ("plaque_burden", "median"), ("lumen_to_outer_centroid_mm", "max"), ("hu_lumen_core", "median"),
                       ("hu_wall", "median"), ("hu_peri", "median"), ("wall_calc_frac", "mean")):
            if c in R:
                s[f"{c}_{agg}"] = float(getattr(R[c], agg)())
        if "outer_area" in R:
            s["n_rings_lumen>outer"] = int((R["lumen_area"] > R["outer_area"]).sum())
            step = s.get("ring_spacing_median_mm", np.nan)
            s["plaque_volume_mm3"] = float(((R["outer_area"] - R["lumen_area"]).clip(lower=0) * step).sum()) if np.isfinite(step) else np.nan
        if "hu_lumen_core" in R:
            s["lumen_minus_peri_hu"] = float((R["hu_lumen_core"] - R["hu_peri"]).median())
        if figs and vol is not None and out:
            fig_ring(pid, seg, lum, out, R, vol, inv, conv)
    s["flags"] = ";".join(segment_flags(s))
    return s, R.to_dict("records")


def segment_flags(s):
    f = []
    g = lambda k: s.get(k, np.nan)
    if not {"centerline", "lumen", "outer"} <= set(s["files"].split(",")): f.append("incomplete_file_set")
    if g("cl_to_tree_median_mm") > 1: f.append("cl_off_tree>1mm")
    if g("tree_label_same_artery") < 0.5: f.append("tree_label_other_artery")
    if g("cl_inside_frac") < 1: f.append("cl_outside_volume")
    if g("cl_hu_median") < DARK_HU: f.append("cl_dark")
    if g("centroid_to_cl_mm_max") > 2: f.append("ring_off_centerline>2mm")
    if g("cos_normal_tangent_min") < 0.7: f.append("ring_tilted>45deg")
    if g("lumen_inside_outer_frac_min") < 0.9: f.append("lumen_outside_outer")
    if g("n_rings_lumen>outer") > 0: f.append("lumen_area>outer")
    if g("min_lumen_eq_diam") < 0.5 or g("max_lumen_eq_diam") > 7: f.append("lumen_diam_odd")
    if g("n_open_rings") > 0: f.append("open_rings")
    if g("max_planarity") > 0.2: f.append("non_planar_ring")
    if g("ring_spacing_max_mm") > 3: f.append("ring_gap>3mm")
    if g("lumen_minus_peri_hu") < 100: f.append("low_lumen_contrast(misregistered?)")
    if g("n_lumen_rings") != g("n_outer_rings") and "outer" in s["files"]: f.append("lumen_outer_ring_count_differ")
    return f


# ============================================================ overlay figures (stay on server)
def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt


def fig_tree(task, vol, inv, conv, tree):
    plt = _plt()
    out = Path(task["out"]) / "cases" / "overlays"
    out.mkdir(parents=True, exist_ok=True)
    pts = np.concatenate([to_voxel(p, inv, conv) for p, _ in tree])
    labs = [TERR.get(l, "none") for _, ls in tree for l in ls]
    colors = {"LM": "#6b6b6b", "LAD": "#2a6fdb", "CX": "#d9822b", "RCA": "#1f9e74", "none": "#c0392b"}
    lo, hi = np.floor(pts.min(0)).astype(int), np.ceil(pts.max(0)).astype(int)
    lo, hi = np.maximum(lo - 10, 0), np.minimum(hi + 10, np.array(vol.shape) - 1)
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    for a, (axis, (u, v)) in zip(ax, ((2, (0, 1)), (1, (0, 2)))):
        sl = [slice(None)] * 3
        sl[axis] = slice(lo[axis], hi[axis] + 1)
        mip = np.clip(vol[tuple(sl)].max(axis), -200, 800)
        a.imshow(mip.T, cmap="gray", origin="lower")
        for t, c in colors.items():
            m = np.array([l == t for l in labs])
            if m.any():
                a.scatter(pts[m, u], pts[m, v], s=1, c=c, label="unlabelled" if t == "none" else t)
        a.set_title(f"MIP over axis {axis}")
        a.axis("off")
    ax[0].legend(markerscale=6, loc="upper right", fontsize=8)
    fig.suptitle(f"{task['visit']} {task['id']} tree ({conv})")
    fig.tight_layout()
    fig.savefig(out / f"{task['visit']}_{task['id']}_tree.png", dpi=110)
    plt.close(fig)


def fig_ring(pid, seg, lum, out_rings, R, vol, inv, conv):
    plt = _plt()
    out = Path(_W.get("out", ".")) / "cases" / "overlays"
    out.mkdir(parents=True, exist_ok=True)
    i = int(R.loc[R["lumen_area"].idxmin(), "ring"])
    L = lum[i]
    _, k = cq.nearest(L["c"][None], np.array([o["c"] for o in out_rings]))
    O = out_rings[int(np.ravel(k)[0])]
    half, n = 8.0, 161
    g = np.linspace(-half, half, n)
    U, V = np.meshgrid(g, g)
    plane = O["c"] + U.ravel()[:, None] * O["basis"][0] + V.ravel()[:, None] * O["basis"][1]
    img = sample(vol, to_voxel(plane, inv, conv)).reshape(n, n)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(np.clip(img, -200, 800), cmap="gray", origin="lower", extent=(-half, half, -half, half))
    for ring, c, name in ((L, "#e74c3c", "lumen"), (O, "#f1c40f", "outer")):
        uv = (ring["pts"] - O["c"]) @ O["basis"][:2].T
        uv = np.vstack([uv, uv[:1]])
        ax.plot(uv[:, 0], uv[:, 1], c=c, lw=1.5, label=name)
    ax.legend(fontsize=8)
    ax.set_title(f"BL {pid} {seg}: MLA ring {i}, mm")
    fig.tight_layout()
    fig.savefig(out / f"BL_{pid}_{seg}_mla.png", dpi=110)
    plt.close(fig)


# ============================================================ tree topology (main process)
def tree_topology(trees):
    raw, code_use, parsed, errors = Counter(), defaultdict(lambda: {"names": Counter(), "files": 0, "unnamed": 0, "points": 0}), {}, {}
    for t in trees:
        try:
            polys, meta = cq.parse_member(t["path"].name, t["path"].read_bytes())
            cq.count_codes(polys, meta, code_use)
            raw.update(str(l) for p in polys for l in p.labels)
            parsed[t["id"]] = polys
        except Exception as ex:  # noqa: BLE001
            errors[t["id"]] = f"{type(ex).__name__}: {ex}"[:300]
    cq.decide_numbering(raw)
    for c, u in code_use.items():
        if u["names"]:
            cq._code_names[c] = u["names"].most_common(1)[0][0]
    cq._code_names.update(cq.CODE_NAMES)
    rows, seg_rows = [], []
    for pid, polys in parsed.items():
        try:
            m, seg = cq.analyse_case(polys)
        except Exception as ex:  # noqa: BLE001
            errors[pid] = f"analysis: {type(ex).__name__}: {ex}"[:300]
            continue
        rows.append({"id": pid, **m, "flags": ";".join(cq.flags_for(m, seg))})
        seg_rows += [{"id": pid, "segment": s, "length_mm": round(v, 2)} for s, v in seg.items()]
    df = pd.DataFrame(rows)
    seg = pd.DataFrame(seg_rows, columns=["id", "segment", "length_mm"])
    lv = pd.DataFrame([(r, cq.normalise_label(r if r != "None" else None), n) for r, n in raw.most_common()],
                      columns=["raw_label", "mapped_to", "n_points"])
    return df, seg, lv, errors


# ============================================================ extraction log
def log_lines(logs, known_ids):
    """{id: Counter(masked line pattern)} for log lines that mention a known ID, and overall patterns."""
    per_id, overall = defaultdict(Counter), Counter()
    for p in logs:
        for ln in p.read_text(errors="replace").splitlines():
            if not ln.strip():
                continue
            pat = re.sub(r"\s+", " ", masked(re.sub(r"\S*[/\\]\S*", lambda m: Path(m.group().replace("\\", "/")).name, ln)))[:160]
            overall[pat] += 1
            for tok in re.findall(r"(?<![\d.])\d+(?![\d.])", ln):
                k = norm_id(tok)
                if k in known_ids:
                    per_id[k][pat] += 1
    return per_id, overall


def why_missing(ids, per_id, top=8):
    c = Counter()
    for i in ids:
        pats = per_id.get(i)
        c.update(set(pats) if pats else {"(no log line mentions this ID)"})
    return pd.DataFrame(c.most_common(top), columns=["log line (digits masked)", "patients"])


# ============================================================ figures (aggregate)
def hist(ax, x, title, vline=None, bins=40):
    x = pd.Series(x, dtype=float).dropna()
    if len(x):
        bins = bins if x.max() - x.min() > 1e-6 * max(1, abs(x.max())) else 1
        ax.hist(x, bins=bins, color="#2a6fdb", edgecolor="white", linewidth=0.5)
    if vline is not None:
        ax.axvline(vline, color="#6b6b6b", lw=1, ls="--")
    ax.set_title(f"{title} (n={len(x)})", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)


def figures(out, vols, trees, segs):
    plt = _plt()
    fd = out / "figures"
    fd.mkdir(exist_ok=True)
    if len(vols) and "hu_p99.9" in vols:
        fig, ax = plt.subplots(2, 3, figsize=(13, 7))
        for a, (c, t, v) in zip(ax.ravel(), (("dx", "in-plane spacing (mm)", None), ("dz", "slice spacing (mm)", None),
                                             ("fov_z_mm", "z coverage (mm)", None), ("hu_p1", "HU p1", -500),
                                             ("hu_p50", "HU median", None), ("hu_p99.9", "HU p99.9", 300))):
            hist(a, vols[c], t, v)
        fig.tight_layout(); fig.savefig(fd / "volumes.png", dpi=110); plt.close(fig)
    if len(trees):
        cols = [("unlabelled_pct", "unlabelled length (%)", 20), ("total_mm", "total tree length (mm)", None),
                ("n_components", "connected components", None), ("inside_frac", "fraction inside volume", None),
                ("hu_median", "median HU on centerline", DARK_HU), ("center_minus_off3mm", f"HU centre - {OFF_MM:g} mm off", 0),
                ("dark_frac", f"fraction of points < {DARK_HU} HU", None), ("longest_dark_mm", "longest dark run (mm)", None),
                ("n_kinks", f"kinks > {KINK_DEG} deg", None)]
        cols = [c for c in cols if c[0] in trees]
        fig, ax = plt.subplots(3, 3, figsize=(13, 10))
        for a, (c, t, v) in zip(ax.ravel(), cols):
            hist(a, trees[c], t, v)
        for a in ax.ravel()[len(cols):]:
            a.axis("off")
        fig.tight_layout(); fig.savefig(fd / "trees.png", dpi=110); plt.close(fig)
    if len(segs):
        cols = [("cl_to_tree_median_mm", "contour CL to tree (mm)", 1), ("centroid_to_cl_mm_max", "max ring centroid to CL (mm)", 2),
                ("cos_normal_tangent_min", "min |cos(ring normal, tangent)|", 0.7), ("lumen_inside_outer_frac_min", "min lumen-in-outer fraction", 0.9),
                ("mla_mm2", "MLA (mm2)", None), ("plaque_burden_max", "max plaque burden (%)", None),
                ("hu_lumen_core_median", "HU lumen core", None), ("hu_peri_median", f"HU {PERI_MM:g} mm outside wall", None),
                ("lumen_minus_peri_hu", "lumen - perivascular HU", 100)]
        cols = [c for c in cols if c[0] in segs]
        fig, ax = plt.subplots(3, 3, figsize=(13, 10))
        for a, (c, t, v) in zip(ax.ravel(), cols):
            hist(a, segs[c], t, v)
        for a in ax.ravel()[len(cols):]:
            a.axis("off")
        fig.tight_layout(); fig.savefig(fd / "contours.png", dpi=110); plt.close(fig)
        if "visual_grade" in segs and "medis_diam_stenosis_pct" in segs:
            d = segs[segs["visual_grade"].isin(GRADES)]
            groups = [g for g in GRADES if (d["visual_grade"] == g).any()]
            if groups:
                fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
                for a, c, t in ((ax[0], "medis_diam_stenosis_pct", "Medis diameter stenosis (%)"),
                                (ax[1], "plaque_burden_max", "Medis max plaque burden (%)")):
                    data = [d.loc[d["visual_grade"] == g, c].dropna() for g in groups]
                    a.boxplot(data, widths=0.5, medianprops={"color": "#2a6fdb"})
                    a.set_xticks(range(1, len(groups) + 1), groups)
                    a.set_xlabel("visual stenosis grade"); a.set_title(t, fontsize=9)
                    a.spines[["top", "right"]].set_visible(False)
                fig.tight_layout(); fig.savefig(fd / "visual_vs_medis.png", dpi=110); plt.close(fig)


# ============================================================ main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--out", default=OUT_DIR)
    ap.add_argument("--inspect", action="store_true", help="only write inventory.md")
    ap.add_argument("--limit", type=int, help="only the first N patients with Medis data (+ their volumes)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--no-voxels", action="store_true", help="read NIfTI headers only, no HU checks")
    ap.add_argument("--convention", default=CONVENTION, choices=("auto",) + CONVENTIONS)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    root, out = Path(args.root), Path(args.out).expanduser()
    try:
        (out / "cases" / "lists").mkdir(parents=True, exist_ok=True)
    except PermissionError:
        sys.exit(f"cannot create {out}: no write permission. Pass --out with a folder you own.")
    _W["out"] = str(out)

    found = discover(root)
    sheets = load_sheets(root)
    (out / "inventory.md").write_text(inventory(root, found, sheets), encoding="utf-8")
    print(f"{len(found['files']):,} files: {len(found['niftis'])} NIfTI, {len(found['trees'])} trees, "
          f"{len(found['contours'])} contour segments, {len(found['logs'])} logs -> {out / 'inventory.md'}")
    if args.inspect:
        return

    rep = [f"# HØ_10Y data quality check", "", f"Root: `{root}`. Generated by `CGPS_data/hoe10y_qc.py`. "
           "Aggregate only; per-patient results are in `cases/` (keep on the DTU machine).", ""]
    lists = {}

    # ---- 1. spreadsheets
    sheet_rep, sheet_lists, sheet_ids = sheet_checks(sheets)
    lists.update(sheet_lists)
    rep += ["## 1. Spreadsheets", "", sheet_rep, ""]

    # ---- 2. coverage
    nifti = defaultdict(list)
    no_id = [x["path"] for x in found["niftis"] + found["trees"] if x["id"] is None]
    for x in found["niftis"]:
        if x["id"] is not None:
            nifti[(x["visit"], x["id"])].append(x["path"])
    tree_of = {}
    for t in found["trees"]:
        if t["id"] is not None:
            tree_of.setdefault(t["id"], []).append(t["path"])
    contours_of = defaultdict(dict)
    for (v, pid, seg), files in found["contours"].items():
        contours_of[(v, pid)][seg] = files
    if no_id:
        rep.append(f"**{len(no_id)} NIfTI/tree files without an ID in the name were skipped** "
                   f"(patterns: {dict(Counter(masked(p.name) for p in no_id).most_common(5))})\n")
    all_ids = set().union(*sheet_ids.values(), {i for _, i in nifti}, tree_of, {i for _, i in contours_of}) - {None}
    P = pd.DataFrame({"id": sorted(all_ids, key=lambda s: int(s))})
    P["in_BL_sheet"] = P["id"].isin(sheet_ids.get("BL", set()))
    P["in_FU_sheet"] = P["id"].isin(sheet_ids.get("FU", set()))
    for v in ("BL", "FU", "?"):
        P[f"nifti_{v}"] = P["id"].map(lambda i: len(nifti.get((v, i), [])))
    P["medis_tree"] = P["id"].map(lambda i: len(tree_of.get(i, [])))
    P["medis_contour_segments"] = P["id"].map(lambda i: len(contours_of.get(("BL", i), {})))
    known = set(P["id"])
    per_id, overall = log_lines(found["logs"], known)
    P["log_lines"] = P["id"].map(lambda i: sum(per_id.get(i, Counter()).values()))
    cov = []
    sheet_bl = P["in_BL_sheet"]
    for name, cond in (("in BL sheet", sheet_bl), ("in FU sheet", P["in_FU_sheet"]),
                       ("BL NIfTI", P["nifti_BL"] > 0), ("FU NIfTI", P["nifti_FU"] > 0),
                       ("NIfTI with unknown visit", P["nifti_?"] > 0), ("Medis tree", P["medis_tree"] > 0),
                       ("Medis contours", P["medis_contour_segments"] > 0),
                       ("BL sheet + BL NIfTI", sheet_bl & (P["nifti_BL"] > 0)),
                       ("BL sheet + FU sheet + BL & FU NIfTI", sheet_bl & P["in_FU_sheet"] & (P["nifti_BL"] > 0) & (P["nifti_FU"] > 0)),
                       ("Medis tree + BL NIfTI", (P["medis_tree"] > 0) & (P["nifti_BL"] > 0)),
                       ("Medis contours + BL NIfTI", (P["medis_contour_segments"] > 0) & (P["nifti_BL"] > 0)),
                       ("Medis contours + tree", (P["medis_contour_segments"] > 0) & (P["medis_tree"] > 0))):
        cov.append({"set": name, "patients": int(cond.sum())})
    problems = {
        "BL sheet, no BL NIfTI": sheet_bl & (P["nifti_BL"] == 0),
        "FU sheet, no FU NIfTI": P["in_FU_sheet"] & (P["nifti_FU"] == 0),
        "BL NIfTI, not in BL sheet": (P["nifti_BL"] > 0) & ~sheet_bl,
        "FU NIfTI, not in FU sheet": (P["nifti_FU"] > 0) & ~P["in_FU_sheet"],
        "Medis files, no BL NIfTI": ((P["medis_tree"] > 0) | (P["medis_contour_segments"] > 0)) & (P["nifti_BL"] == 0),
        "Medis files, not in BL sheet": ((P["medis_tree"] > 0) | (P["medis_contour_segments"] > 0)) & ~sheet_bl,
        "Medis contours, no tree": (P["medis_contour_segments"] > 0) & (P["medis_tree"] == 0),
        "BL sheet + BL NIfTI, no Medis tree": sheet_bl & (P["nifti_BL"] > 0) & (P["medis_tree"] == 0),
        "more than one BL NIfTI": P["nifti_BL"] > 1, "more than one tree": P["medis_tree"] > 1,
    }
    rep += ["## 2. Coverage", "", md(pd.DataFrame(cov)), "",
            md(pd.DataFrame([{"problem": k, "patients": int(v.sum())} for k, v in problems.items()])), ""]
    if not sheet_ids or not (P["in_BL_sheet"] & ((P["nifti_BL"] > 0) | (P["medis_tree"] > 0))).any():
        rep.append("**No overlap between spreadsheet IDs and file IDs: check ID_COL / id_from_name() against inventory.md.**\n")
    if found["logs"]:
        rep += ["### Why files are missing (extraction log)", "",
                f"Most common log lines overall ({sum(overall.values()):,} lines, digits masked):", "",
                md(pd.DataFrame(overall.most_common(25), columns=["log line", "count"])), ""]
        for k in ("BL sheet, no BL NIfTI", "FU sheet, no FU NIfTI", "BL sheet + BL NIfTI, no Medis tree", "Medis contours, no tree"):
            ids = P.loc[problems[k], "id"]
            if len(ids):
                rep += [f"**{k}** ({len(ids)} patients): log lines mentioning them", "", md(why_missing(ids, per_id)), ""]
        pd.DataFrame([{"id": i, "pattern": p, "n": n} for i, c in per_id.items() for p, n in c.items()]).to_csv(
            out / "cases" / "log_by_id.csv", index=False)
    if "FU" in sheets and "scandate" in sheets["FU"]:
        f = sheets["FU"].assign(id=sheets["FU"][ID_COL].map(norm_id))
        f["year"] = pd.to_datetime(f["scandate"], errors="coerce").dt.year
        f["has_nifti"] = f["id"].map(lambda i: len(nifti.get(("FU", i), [])) > 0)
        t = f.groupby("year", dropna=False)["has_nifti"].agg(["size", "sum"]).rename(columns={"size": "FU patients", "sum": "with FU NIfTI"})
        rep += ["FU NIfTI availability by FU scan year (late scans were not yet pulled):", "", md(t, index=True), ""]
    for k, v in problems.items():
        lists["coverage_" + re.sub(r"\W+", "_", k).strip("_")] = sorted(P.loc[v, "id"], key=int)
    P.to_csv(out / "cases" / "patients.csv", index=False)

    # ---- 3/4/5. per patient
    trees_main = [{"visit": "BL", "id": i, "path": ps[0]} for i, ps in tree_of.items()]
    medis_ids = sorted(set(tree_of) | {i for (v, i) in contours_of if v == "BL"}, key=int)
    if args.limit:
        medis_ids = medis_ids[: args.limit]
        trees_main = [t for t in trees_main if t["id"] in set(medis_ids)]
    print(f"tree topology for {len(trees_main)} trees ...")
    topo, seg_len, label_vals, tree_err = tree_topology(trees_main)
    topo.to_csv(out / "cases" / "tree_topology.csv", index=False)
    seg_len.to_csv(out / "cases" / "tree_segment_lengths.csv", index=False)
    label_vals.to_csv(out / "tree_label_values.csv", index=False)

    tasks = []
    vol_keys = [(v, i) for (v, i) in nifti if v in ("BL", "FU")]
    if args.limit:
        vol_keys = [k for k in vol_keys if k[1] in set(medis_ids)]
    keys = set(vol_keys) | {("BL", i) for i in medis_ids}
    for v, i in sorted(keys, key=lambda k: (k[0], int(k[1]))):
        tasks.append({"id": i, "visit": v, "nifti": (nifti.get((v, i)) or [None])[0], "voxels": not args.no_voxels,
                      "tree": tree_of[i][0] if v == "BL" and i in tree_of else None,
                      "contours": contours_of.get((v, i), {}) if v == "BL" else {}, "out": str(out), "figs": False})
    conv = args.convention
    if conv == "auto":
        calib = [t for t in tasks if t["nifti"] and (t["tree"] or t["contours"])][:CALIB_N]
        if calib and not args.no_voxels:
            with Pool(args.workers) as pool:
                results = [s for s in pool.map(calibrate, calib) if s]
            scores = [s for s in results if "error" not in s]
            failed = [s for s in results if "error" in s]
            if failed:
                print(f"calibration failed for {len(failed)} of {len(calib)} patients, e.g.:")
                for f in failed[:3]:
                    print("  " + f["error"])
                print(failed[0]["trace"])
            if not scores:
                sys.exit("no patient could be calibrated - fix the error above, or pass --convention "
                         "(ras, lps, ...) if you know the coordinate convention")
            votes = Counter(best_conv(s) for s in scores)
            conv = votes.most_common(1)[0][0] if votes else "ras"
            calib_tab = pd.DataFrame({c: [f"{np.median([s[c][0] for s in scores]):.2f} / {np.median([s[c][1] for s in scores]):.2f} / "
                                          f"{np.nanmedian([s[c][2] for s in scores]):.0f}"] for c in CONVENTIONS},
                                     index=[f"median: inside fraction / fraction >= {DARK_HU} HU / HU"]) if scores else None
            print(f"coordinate convention: {conv} (votes {dict(votes)})")
        else:
            conv, votes, calib_tab = "ras", Counter(), None
    else:
        votes, calib_tab = Counter(), None
    rng = random.Random(args.seed)
    fig_ids = set(rng.sample(medis_ids, min(FIG_RANDOM, len(medis_ids))))
    for t in tasks:
        t["figs"] = t["visit"] == "BL" and t["id"] in fig_ids and not args.no_voxels

    vols, trees, segs, rings, errors = [], [], [], [], {}
    init = (cq._numbering, dict(cq._code_names), conv, str(out))
    with Pool(args.workers, initializer=init_worker, initargs=init) as pool:
        for k, r in enumerate(pool.imap_unordered(process, tasks, chunksize=1), 1):
            vols += [r["volume"]] if r["volume"] else []
            trees += [r["tree"]] if r["tree"] else []
            segs += r["segments"]
            rings += r["rings"]
            if r["errors"]:
                errors[f"{r['visit']}_{r['id']}"] = r["errors"]
            if k % 50 == 0 or k == len(tasks):
                print(f"  {k}/{len(tasks)} patient-visits")
    V, T, S, Rg = pd.DataFrame(vols), pd.DataFrame(trees), pd.DataFrame(segs), pd.DataFrame(rings)
    if len(T) and len(topo):
        T = topo.merge(T.drop(columns="visit"), on="id", how="outer")
    elif len(topo):
        T = topo

    # worst trees get overlays too
    if not args.no_voxels and "center_minus_off3mm" in T:
        worst = T.nsmallest(FIG_WORST, "center_minus_off3mm")["id"].tolist()
        redo = [dict(t, figs=True, contours={}) for t in tasks if t["visit"] == "BL" and t["id"] in worst]
        with Pool(args.workers, initializer=init_worker, initargs=init) as pool:
            pool.map(process, redo)

    # ---- visual analysis per segment
    if "BL" in sheets and len(S):
        b = sheets["BL"].assign(id=sheets["BL"][ID_COL].map(norm_id)).set_index("id")
        b = b[~b.index.duplicated()]
        def vis(row, suffix):
            c = f"ct_cag_{row['segment']}_{suffix}"
            return b.at[row["id"], c] if c in b and row["id"] in b.index else np.nan
        S["visual_grade"] = S.apply(lambda r: grade_of(vis(r, "stenosis")), axis=1)
        S["visual_plaque_type"] = S.apply(lambda r: vis(r, "plaque_type"), axis=1)
    for d, name in ((V, "volumes"), (T, "trees"), (S, "segments"), (Rg, "rings")):
        d.to_csv(out / "cases" / f"{name}.csv", index=False)

    # ---- report 3: volumes
    rep += ["## 3. Volumes", ""]
    if len(V):
        rep += [f"{len(V)} volumes read ({V['visit'].value_counts().to_dict()}); read errors: "
                f"{sum(any(e.startswith('volume') for e in es) for es in errors.values())}", "",
                "Orientation (axcodes):", "", md(V.groupby(['visit', 'axcodes']).size().rename('n').reset_index()), "",
                "dtype / scaling:", "", md(V.groupby(['dtype', 'slope', 'inter'], dropna=False).size().rename('n').reset_index()), "",
                md(dist_table(V, ["dx", "dy", "dz", "fov_x_mm", "fov_z_mm", "size_mb", "hu_min", "hu_p1", "hu_p50", "hu_p99", "hu_p99.9", "hu_max", "frac_at_min"], 2)), "",
                "Flags:", "", md(flag_counts(V)), ""]
        add_flag_lists(lists, "volume", V)
    # ---- report 4: trees
    rep += ["## 4. Medis centerline trees", ""]
    if len(T):
        rep += [f"{len(T)} trees analysed, {len(tree_err)} unreadable. Label values and how they were mapped: "
                "`tree_label_values.csv`.", ""]
        if conv:
            rep += [f"Coordinate convention used: **{conv}** "
                    f"(calibration votes over {sum(votes.values())} patients: {dict(votes)}).", ""]
            if calib_tab is not None:
                rep += [md(calib_tab, index=True), ""]
            if "best_convention" in T:
                rep += ["Best convention per patient:", "", md(T["best_convention"].value_counts().rename_axis("convention").rename("patients").reset_index()), ""]
                lists["tree_other_convention"] = sorted(T.loc[T["best_convention"].notna() & (T["best_convention"] != conv), "id"], key=int)
        rep += [md(dist_table(T, ["total_mm", "unlabelled_mm", "unlabelled_pct", "n_components", "n_tiny_components",
                                  "n_branch_points", "n_end_points", "n_gaps", "overlap_mm", "median_spacing_mm", "n_kinks", "n_reversals",
                                  "inside_frac", "hu_median", "hu_p10", "dark_frac", "longest_dark_mm", "off3mm_hu_median",
                                  "center_minus_off3mm", "hu_LM", "hu_LAD", "hu_CX", "hu_RCA", "hu_unlabelled"], 2)), ""]
        conn = [c for c in T.columns if c.startswith("conn_")]
        if conn:
            ct = pd.DataFrame({c[5:]: T[c].value_counts() for c in conn}).fillna(0).astype(int).T
            rep += ["Expected connections (child -> parent):", "", md(ct, index=True), ""]
        if len(seg_len):
            sl = seg_len.pivot_table(index="id", columns="segment", values="length_mm", aggfunc="sum")
            rep += ["Tree segment present / length (mm):", "",
                    md(pd.DataFrame({"present": sl.notna().sum(), "median_mm": sl.median().round(1)}), index=True), ""]
        extra = T.apply(lambda r: ";".join(tree_hu_flags(r)), axis=1)
        T["flags"] = (T.get("flags", pd.Series("", index=T.index)).fillna("") + ";" + extra).str.strip(";")
        T.to_csv(out / "cases" / "trees.csv", index=False)
        rep += ["Flags:", "", md(flag_counts(T)), ""]
        add_flag_lists(lists, "tree", T)
    # ---- report 5: contours
    rep += ["## 5. Medis vessel-wall contours", ""]
    if len(S):
        rep += [f"{len(S)} contoured segments in {S['id'].nunique()} patients; unreadable: {int(S.get('error', pd.Series(dtype=object)).notna().sum())}", "",
                "Segments contoured:", "", md(S["segment"].value_counts().rename_axis("segment").rename("n").reset_index()), "",
                "File sets:", "", md(S["files"].value_counts().rename_axis("files").rename("n").reset_index()), ""]
        for c in ("lumen_ring_source", "outer_ring_source"):
            if c in S:
                rep += [f"{c}: {S[c].value_counts().to_dict()}", ""]
        rep += [md(dist_table(S, ["cl_length_mm", "cl_points", "n_lumen_rings", "n_outer_rings", "rings_per_cl_point",
                                  "ring_spacing_median_mm", "ring_spacing_max_mm", "cl_to_tree_median_mm", "cl_to_tree_max_mm",
                                  "tree_label_same_segment", "tree_label_same_artery", "tree_label_unlabelled",
                                  "cl_inside_frac", "cl_hu_median", "centroid_to_cl_mm_median", "centroid_to_cl_mm_max",
                                  "cos_normal_tangent_median", "cos_normal_tangent_min", "lumen_inside_outer_frac_min",
                                  "max_planarity", "mla_mm2", "ref_area_mm2", "min_lumen_eq_diam", "max_lumen_eq_diam",
                                  "medis_diam_stenosis_pct", "medis_area_stenosis_pct", "plaque_burden_max",
                                  "plaque_burden_median", "plaque_volume_mm3", "hu_lumen_core_median", "hu_wall_median",
                                  "hu_peri_median", "lumen_minus_peri_hu", "wall_calc_frac_mean"], 2)), ""]
        if "tree_label_mode" in S:
            ct = pd.crosstab(S["segment"], S["tree_label_mode"].fillna("unlabelled"))
            rep += ["Contour segment (file name) x most common tree label along it:", "", md(ct, index=True), ""]
        rep += ["Flags:", "", md(flag_counts(S)), ""]
        add_flag_lists(lists, "contour", S, key=lambda r: f"{r['id']}\t{r['segment']}")

    # ---- report 6: visual vs Medis
    rep += ["## 6. Visual analysis vs Medis", ""]
    if "BL" in sheets:
        rep += visual_vs_medis(sheets["BL"], S, set(tree_of) | {i for (v, i) in contours_of if v == "BL"}, lists,
                               set(medis_ids) if args.limit else None)

    if tree_err or errors:
        rep += ["## Errors", "", f"- tree files not parsed: {len(tree_err)}; patient-visits with errors: {len(errors)} "
                "(details in cases/errors.json)", ""]
        msgs = Counter(re.sub(r"\d+", "#", e)[:120] for es in errors.values() for e in es)
        msgs.update(re.sub(r"\d+", "#", e)[:120] for e in tree_err.values())
        rep += [md(pd.DataFrame(msgs.most_common(15), columns=["error", "n"])), ""]
        (out / "cases" / "errors.json").write_text(json.dumps({"trees": tree_err, "patients": {str(k): v for k, v in errors.items()}}, indent=1))

    try:
        figures(out, V, T, S)
    except Exception as ex:  # noqa: BLE001 - figures must not cost the report
        rep.append(f"Figures failed: {type(ex).__name__}: {ex}")
    rep += ["## Files", "", "- figures/volumes.png, trees.png, contours.png, visual_vs_medis.png",
            "- cases/patients.csv, volumes.csv, tree_topology.csv, trees.csv, segments.csv, rings.csv, log_by_id.csv",
            "- cases/lists/*.txt: one ID (or ID + segment) per line per problem",
            f"- cases/overlays/: tree MIP overlays and MLA cross-sections for {FIG_RANDOM} random + {FIG_WORST} worst patients", ""]
    n_lists = 0
    for k, v in lists.items():
        if len(v):
            (out / "cases" / "lists" / f"{k}.txt").write_text("\n".join(map(str, v)) + "\n")
            n_lists += 1
    (out / "report.md").write_text("\n".join(rep), encoding="utf-8")
    print(f"wrote {out / 'report.md'}, {n_lists} ID lists, figures and cases/")


def tree_hu_flags(r):
    f = []
    g = lambda k: r.get(k, np.nan)
    if g("inside_frac") < 1: f.append("points_outside_volume")
    if g("hu_median") < 200: f.append("median_HU<200")
    if g("center_minus_off3mm") < 100: f.append("not_brighter_than_surroundings(misregistered?)")
    if g("longest_dark_mm") > 10: f.append(f"dark_run>10mm")
    if g("n_reversals") > 0: f.append("back_and_forth")
    if g("n_kinks") > 5: f.append("kinks>5")
    return f


def flag_counts(df):
    c = Counter(f for fl in df.get("flags", pd.Series(dtype=str)).fillna("") for f in fl.split(";") if f)
    n = len(df)
    return pd.DataFrame([{"flag": k, "n": pct(v, n)} for k, v in c.most_common()])


def add_flag_lists(lists, prefix, df, key=None):
    for fl in {f for x in df.get("flags", pd.Series(dtype=str)).fillna("") for f in x.split(";") if f}:
        m = df["flags"].fillna("").str.split(";").map(lambda x: fl in x)
        ids = df[m].apply(key, axis=1).tolist() if key else df.loc[m, "id"].tolist()
        lists[f"{prefix}_{re.sub(r'[^A-Za-z0-9]+', '_', fl).strip('_')}"] = ids


def visual_vs_medis(bl, S, analysed, lists, limit_ids=None):
    rep = []
    b = bl.assign(id=bl[ID_COL].map(norm_id))
    b = b[b["id"].isin(analysed if limit_ids is None else analysed & limit_ids)].drop_duplicates("id")
    has = set(zip(S["id"], S["segment"])) if len(S) else set()
    rows = []
    for s in SEGMENTS:
        if f"ct_cag_{s}_stenosis" not in b:
            continue
        for pid, raw in zip(b["id"], b[f"ct_cag_{s}_stenosis"]):
            row = {"id": pid, "segment": s, "visual_grade": grade_of(raw), "contours": (pid, s) in has}
            for suf in ("medis_finished", "medis_egnet", "eval", "plaque_type"):
                c = f"ct_cag_{s}_{suf}"
                row[suf] = b.loc[b["id"] == pid, c].iloc[0] if c in b else np.nan
            rows.append(row)
    D = pd.DataFrame(rows)
    if not len(D):
        return ["_no segment reads for the analysed patients_", ""]
    rep += [f"Restricted to the {b['id'].nunique()} BL patients with any Medis file (Kit only exported scans a reader "
            f"analysed), {len(D)} patient-segments.", "",
            "Visual stenosis grade x Medis contours present:", "",
            md(pd.crosstab(D["visual_grade"], D["contours"].map({True: "contours", False: "no contours"}), margins=True), index=True), ""]
    diseased = D["visual_grade"].isin(GRADES[1:])
    lists["visual_diseased_no_contours"] = [f"{r.id}\t{r.segment}\t{r.visual_grade}" for r in D[diseased & ~D["contours"]].itertuples()]
    lists["contours_visual_none"] = [f"{r.id}\t{r.segment}" for r in D[(D["visual_grade"] == "none") & D["contours"]].itertuples()]
    lists["contours_visual_missing_or_uneval"] = [f"{r.id}\t{r.segment}\t{r.visual_grade}" for r in D[D["visual_grade"].isin(["missing", "unevaluable", "unrecognised"]) & D["contours"]].itertuples()]
    rep += [f"- visually diseased (>= minimal) but no contours: {pct(len(lists['visual_diseased_no_contours']), int(diseased.sum()))}",
            f"- contours but visual grade none: {len(lists['contours_visual_none'])}", ""]
    t = D[diseased].groupby("segment")["contours"].agg(["size", "sum"]).rename(columns={"size": "visually diseased", "sum": "with contours"})
    rep += ["Per segment:", "", md(t, index=True), ""]
    # contours only exist for main-vessel segments?
    nonseg = S.loc[~S["segment"].isin(SEGMENTS), "segment"].value_counts() if len(S) else pd.Series(dtype=int)
    if len(nonseg):
        rep += [f"Contour files whose segment name is not a spreadsheet segment (not matched above): {nonseg.to_dict()}", ""]
    for suf in ("medis_finished", "medis_egnet"):
        if D[suf].notna().any():
            rep += [f"`ct_cag_<seg>_{suf}` x contours present:", "",
                    md(pd.crosstab(D[suf].astype(str), D["contours"].map({True: "contours", False: "no contours"})), index=True), ""]
    if len(S) and "medis_diam_stenosis_pct" in S and "visual_grade" in S:
        d = S[S["visual_grade"].isin(GRADES)]
        g = d.groupby("visual_grade")[["medis_diam_stenosis_pct", "plaque_burden_max", "mla_mm2", "plaque_volume_mm3"]].median().round(1)
        g.insert(0, "n", d["visual_grade"].value_counts())
        rep += ["Medis quantification (derived from the contours) by visual grade, medians:", "",
                md(g.reindex([x for x in GRADES if x in g.index]), index=True), ""]
        code = d["visual_grade"].map({k: i for i, k in enumerate(GRADES)})
        for c in ("medis_diam_stenosis_pct", "plaque_burden_max"):
            rep.append(f"- Spearman(visual grade, {c}) = {code.corr(d[c], method='spearman'):.3f} (n={d[c].notna().sum()})")
        # visual 'mild' (grade 2, 25-49 %?) vs Medis: show how often Medis DS falls in each CAD-RADS band
        bands = pd.cut(d["medis_diam_stenosis_pct"], [-np.inf, 1, 25, 50, 70, 100, np.inf],
                       labels=["0", "1-24", "25-49", "50-69", "70-99", "100"], right=False)
        rep += ["", "Visual grade x Medis diameter stenosis band (%):", "", md(pd.crosstab(d["visual_grade"], bands), index=True), ""]
        if "wall_calc_frac_mean" in S:
            pt = label_text(S["visual_plaque_type"].astype(str)).map(lambda x: x if x in PLAQUE_CODES else ("missing" if x in ("nan", "none") else x))
            g = S.groupby(pt)["wall_calc_frac_mean"].describe()[["count", "25%", "50%", "75%"]].round(2)
            rep += [f"Visual plaque type vs fraction of wall samples > {CALC_HU} HU:", "", md(g, index=True), ""]
    return rep


if __name__ == "__main__":
    main()
